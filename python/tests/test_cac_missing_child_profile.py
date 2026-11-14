"""Named CAC validation subset ``cac:missing-child`` (issue #18)."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os
import socket
import urllib.request

import pytest
from rdflib import Graph, OWL, RDF, URIRef
from rdflib.namespace import SH
from rdflib.parser import URLInputSource

from case_uco.validation import (
    DEFAULT_BUILT_VERSION,
    parse_extension_token,
    report_to_dict,
    validate_graph_file,
    validator_available,
)
from case_uco.validation.graph import load_extension_ontology_paths
from case_uco.validation.coverage import _core_ontology_paths

ROOT = Path(__file__).resolve().parents[2]
T0 = ROOT / "examples/cac/t0-missing-child.jsonld"
INVENTED = ROOT / "examples/cac/t0-missing-child-invented-term.jsonld"
ABDUCTION_IRI = "https://cacontology.projectvic.org/abduction#StrangerAbductionInvestigation"
CASE_PHASE_IRI = "https://cacontology.projectvic.org/case-management#CaseInitiationPhase"
URGENCY_IRI = "https://cacontology.projectvic.org/temporal#urgencyLevel"
INVENTED_IRI = "https://cacontology.projectvic.org#InventedMediaAuthScore"


@pytest.fixture
def blocked_network(monkeypatch, tmp_path):
    """Block URL loading and sockets in both pytest and case_validate."""
    attempts = tmp_path / "network-attempts.txt"
    child_loaded = tmp_path / "network-block-loaded.txt"

    def deny_network(*args, **kwargs):
        attempts.write_text("Network access attempted", encoding="utf-8")
        raise AssertionError("Ontology validation must stay offline")

    for target, attribute in (
        (urllib.request, "urlopen"),
        (socket, "create_connection"),
        (socket.socket, "connect"),
        (socket.socket, "connect_ex"),
        (URLInputSource, "__init__"),
    ):
        monkeypatch.setattr(target, attribute, deny_network)

    # validate_graph_file launches case_validate: parent monkeypatches alone
    # do not protect that process. Python imports this hook at child startup.
    (tmp_path / "sitecustomize.py").write_text(
        f"""from pathlib import Path
import socket
import urllib.request
from rdflib.parser import URLInputSource

def deny_network(*args, **kwargs):
    Path({str(attempts)!r}).write_text("Network access attempted", encoding="utf-8")
    raise AssertionError("Ontology validation must stay offline")

urllib.request.urlopen = deny_network
socket.create_connection = deny_network
socket.socket.connect = deny_network
socket.socket.connect_ex = deny_network
URLInputSource.__init__ = deny_network
Path({str(child_loaded)!r}).write_text("loaded", encoding="utf-8")
""",
        encoding="utf-8",
    )
    monkeypatch.setenv(
        "PYTHONPATH", str(tmp_path) + os.pathsep + os.environ.get("PYTHONPATH", "")
    )
    yield child_loaded
    # Detect even attempted fetches whose exceptions a loader swallowed.
    assert not attempts.exists(), "Ontology loading attempted network access"


def test_missing_child_profile_loads_pinned_local_gufo_without_imports(
    blocked_network, monkeypatch,
):
    profile_path = ROOT / "ontology/cac/validation-subset-missing-child.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    paths = load_extension_ontology_paths(
        "cac", mode="missing-child", project_root=ROOT
    )
    expected = [(profile_path.parent / rel).resolve() for rel in profile["ontology_files"]]
    assert [path.resolve() for path in paths] == expected
    gufo = [path.resolve() for path in paths if path.name == "gufo.ttl"]
    assert gufo == [ROOT / "ontology/upper/gufo.ttl"]
    assert hashlib.sha256(gufo[0].read_bytes()).hexdigest() == (
        profile["module_digests_sha256"]["../upper/gufo.ttl"]
    )

    parsed = []
    original_parse = Graph.parse

    def parse_local(graph, source=None, *args, **kwargs):
        path = Path(source).resolve()
        assert path in expected, f"Unexpected import: {source}"
        parsed.append(path)
        return original_parse(graph, source, *args, **kwargs)

    monkeypatch.setattr(Graph, "parse", parse_local)
    ontology = Graph()
    for path in paths:
        ontology.parse(path, format="turtle")
    # The SDK selects files from the manifest, not the owl:imports closure.
    # RDFLib retains imports as triples without dereferencing them.
    assert list(ontology.objects(None, OWL.imports))
    assert parsed == expected


def test_parse_extension_token_named_subset():
    assert parse_extension_token("cac") == ("cac", "subset")
    assert parse_extension_token("cac:full") == ("cac", "full")
    assert parse_extension_token("cac:missing-child") == ("cac", "missing-child")
    with pytest.raises(ValueError, match="extension_unknown"):
        parse_extension_token("cac:")


def test_unknown_named_subset_fails_closed():
    with pytest.raises(ValueError, match="extension_unknown"):
        load_extension_ontology_paths(
            "cac", mode="does-not-exist", project_root=ROOT
        )


def test_missing_child_subset_loads_abduction_modules():
    paths = load_extension_ontology_paths(
        "cac", mode="missing-child", project_root=ROOT
    )
    names = {p.name for p in paths}
    assert "cacontology-stranger-abduction.ttl" in names
    assert "cacontology-stranger-abduction-shapes.ttl" not in names
    assert "cacontology-case-management.ttl" in names
    assert "cacontology-temporal.ttl" in names
    press = load_extension_ontology_paths("cac", mode="subset", project_root=ROOT)
    press_names = {p.name for p in press}
    assert "cacontology-stranger-abduction.ttl" not in press_names


def _path_predicates(shapes, path):
    if isinstance(path, URIRef):
        yield path
        return
    if (path, RDF.first, None) in shapes:
        for item in shapes.items(path):
            yield from _path_predicates(shapes, item)
        return
    for operator in (SH.inversePath, SH.alternativePath, SH.zeroOrMorePath,
                     SH.oneOrMorePath, SH.zeroOrOnePath):
        for child in shapes.objects(path, operator):
            yield from _path_predicates(shapes, child)


def _undeclared_required_paths(ontology, shapes):
    property_types = {
        RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty,
        OWL.AnnotationProperty, OWL.FunctionalProperty, OWL.InverseFunctionalProperty,
        OWL.TransitiveProperty, OWL.SymmetricProperty, OWL.AsymmetricProperty,
        OWL.ReflexiveProperty, OWL.IrreflexiveProperty,
    }
    declared = {
        subject for property_type in property_types
        for subject in ontology.subjects(RDF.type, property_type)
    }
    return sorted({
        str(predicate)
        for shape, minimum in shapes.subject_objects(SH.minCount)
        if int(minimum) >= 1
        for path in shapes.objects(shape, SH.path)
        for predicate in _path_predicates(shapes, path)
        if predicate not in declared
    })


def test_missing_child_required_shape_paths_are_declared():
    profile_path = ROOT / "ontology/cac/validation-subset-missing-child.json"
    profile = json.loads(profile_path.read_text())
    ontology, shapes = Graph(), Graph()
    for path in _core_ontology_paths(ROOT):
        ontology.parse(path)
    # Read the manifest directly so a missing file cannot silently be skipped.
    for relative in profile["ontology_files"]:
        path = profile_path.parent / relative
        (shapes if "shapes" in path.name else ontology).parse(path)
    assert list(shapes.subject_objects(SH.minCount)), "Profile must retain shapes"
    assert not _undeclared_required_paths(ontology, shapes)


@pytest.mark.parametrize("inverse", [False, True])
def test_shape_reference_does_not_declare_a_required_property(inverse):
    from rdflib import BNode, Literal

    ontology, shapes = Graph(), Graph()
    shape = BNode()
    path = URIRef("https://example.org/requiredProperty")
    if inverse:
        inverse_path = BNode()
        shapes.add((shape, SH.path, inverse_path))
        shapes.add((inverse_path, SH.inversePath, path))
    else:
        shapes.add((shape, SH.path, path))
    shapes.add((shape, SH.minCount, Literal(1)))
    assert _undeclared_required_paths(ontology, shapes) == [str(path)]
    ontology.add((path, RDF.type, OWL.DatatypeProperty))
    assert _undeclared_required_paths(ontology, shapes) == []


@pytest.mark.skipif(not validator_available(), reason="case_validate not installed")
def test_t0_missing_child_profile_conforms(blocked_network):
    report = validate_graph_file(
        T0,
        extensions=["cac:missing-child"],
        project_root=ROOT,
        strict_concepts=True,
    )
    payload = report_to_dict(report)
    assert payload["built_version"] == "case-1.5.0"
    assert payload["ontology_identity"]["case"] == "1.5.0"
    assert payload["ontology_identity"]["cac"] == "3.1.0"
    assert DEFAULT_BUILT_VERSION == "case-1.5.0"
    assert report.conforms is True
    assert report.verification_status == "complete"
    assert not report.undeclared_concepts
    assert blocked_network.is_file(), "case_validate must load the network block"


@pytest.mark.skipif(not validator_available(), reason="case_validate not installed")
def test_invented_term_fails_as_nonexistent():
    report = validate_graph_file(
        INVENTED,
        extensions=["cac:missing-child"],
        project_root=ROOT,
        strict_concepts=True,
    )
    assert report.conforms is not True
    assert INVENTED_IRI in report.undeclared_concepts
    assert "Do not mint" in report.concept_guidance


@pytest.mark.skipif(not validator_available(), reason="case_validate not installed")
def test_subset_miss_is_not_a_missing_ontology_concept():
    report = validate_graph_file(
        T0,
        extensions=["cac"],
        project_root=ROOT,
        strict_concepts=True,
    )
    undeclared = set(report.undeclared_concepts)
    assert undeclared.intersection({ABDUCTION_IRI, CASE_PHASE_IRI, URGENCY_IRI})
    assert report.conforms is not True
    assert "outside the selected validation subset" in report.concept_guidance
    assert "cac:missing-child" in report.concept_guidance
