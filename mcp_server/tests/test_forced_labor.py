"""Strict validation of the forced-labor alphabet extension.

The extension declares the ``fl:`` phase scheme and techniques that the
layered exemplar has occupied since layered 0.2.0. Its own exemplar must
pass SHACL and strict concept coverage when selected, its invalid fixture
must fail, and selecting ``layered`` must now pull the alphabet in through
``depends_on`` so the Atkinson exemplar conforms with no inline T-Box.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXT_DIR = PROJECT_ROOT / "extensions" / "forced-labor"
MANIFEST = json.loads((EXT_DIR / "manifest.json").read_text(encoding="utf-8"))
LAYERED_EXEMPLAR = PROJECT_ROOT / "extensions" / "layered" / "layered-exemplar.ttl"

FL = "http://example.org/ontology/forced-labor/"
TECHNIQUES = {FL + n for n in ("a_deceive_recruit", "a_coerce_labor", "a_compel_labor", "a_appropriate_wages")}

from case_uco.validation import validate_graph_file  # noqa: E402
from case_uco.validation.graph import validator_available  # noqa: E402

needs_validator = pytest.mark.skipif(not validator_available(), reason="case_validate not installed")


def _validate(path: Path, extensions: list[str]):
    return validate_graph_file(
        path,
        extensions=extensions,
        profiles=["time", "prov-o"],
        strict_concepts=True,
        force_rdfs_inference=True,
    )


def test_manifest_is_a_candidate_alphabet_on_trajectories():
    assert MANIFEST["status"] == "candidate"
    assert MANIFEST["depends_on"] == ["trajectories"]
    assert MANIFEST["namespaces"] == {"fl": FL}


def test_every_technique_is_declared_and_used_by_the_exemplar():
    from rdflib import Graph, URIRef

    ont = Graph().parse(EXT_DIR / "forced-labor.ttl")
    declared = {str(s) for s in ont.subjects() if str(s).startswith(FL)}
    assert TECHNIQUES <= declared
    data = Graph().parse(EXT_DIR / "forced-labor-exemplar.ttl")
    used = {str(o) for o in data.objects(predicate=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"))}
    assert TECHNIQUES <= used, TECHNIQUES - used


def test_cac_close_matches_point_at_classes_cac_declares():
    """Recruitment and Control carry a skos:closeMatch to CAC trafficking
    classes; each target must be a declared owl:Class in the vendored CAC,
    so the crosswalk cannot dangle."""
    from rdflib import Graph, URIRef
    from rdflib.namespace import OWL, RDF, SKOS

    cac = "https://cacontology.projectvic.org/trafficking#"
    ont = Graph().parse(EXT_DIR / "forced-labor.ttl")
    matches = {(str(s), str(o)) for s, o in ont.subject_objects(SKOS.closeMatch)}
    assert matches == {
        (FL + "Recruitment", cac + "VictimRecruitment"),
        (FL + "Control", cac + "VictimControlSituation"),
    }
    assert not list(ont.subject_objects(SKOS.exactMatch))

    cac_ttl = PROJECT_ROOT / "ontology" / "cac" / "ontology" / "ontology" / "cacontology-sex-trafficking.ttl"
    if not cac_ttl.exists():
        pytest.skip("CAC submodule not checked out")
    cac_graph = Graph().parse(cac_ttl)
    for _, target in sorted(matches):
        assert (URIRef(target), RDF.type, OWL.Class) in cac_graph, target


def test_registry_local_names_do_not_collide_with_other_extensions():
    """`trafficking` already has `a_coerce`; this alphabet uses `a_coerce_labor`.

    Registry local-name collisions were a bug class (#43), so every technique
    local name must be unique across extensions/*/_registry.json and must
    resolve by bare name to the forced-labor IRI in the language registries.
    """
    own = json.loads((EXT_DIR / "_registry.json").read_text(encoding="utf-8"))["classes"]
    local_names = set(own)
    assert {n.rsplit("/", 1)[1] for n in TECHNIQUES} == local_names
    for other in sorted((PROJECT_ROOT / "extensions").glob("*/_registry.json")):
        if other.parent == EXT_DIR:
            continue
        shared = local_names & set(json.loads(other.read_text(encoding="utf-8")).get("classes", {}))
        assert not shared, f"{other.parent.name} also declares {sorted(shared)}"
    for registry in (
        PROJECT_ROOT / "python" / "case_uco" / "_registry.json",
        PROJECT_ROOT / "rust" / "src" / "_registry.json",
        PROJECT_ROOT / "java" / "src" / "main" / "resources" / "_registry.json",
        PROJECT_ROOT / "csharp" / "CaseUco" / "_registry.json",
    ):
        classes = json.loads(registry.read_text(encoding="utf-8"))["classes"]
        for name in local_names:
            assert classes[name]["iri"] == FL + name, (registry.name, name)
            assert classes[name]["module"] == "ext.forced-labor.fl"
        assert classes["a_coerce"]["iri"].startswith("http://example.org/ontology/trafficking/")


@needs_validator
@pytest.mark.parametrize("rel", MANIFEST["exemplar_files"], ids=lambda rel: Path(rel).stem)
def test_exemplar_conforms_with_strict_coverage(rel):
    report = _validate(EXT_DIR / rel, ["forced-labor"])
    assert report.conforms is True, report.safe_summary
    assert report.verification_status == "complete"
    assert report.undeclared_concepts == ()
    assert set(report.selected_extensions) == {"forced-labor", "trajectories"}


@needs_validator
@pytest.mark.parametrize("rel", MANIFEST["invalid_exemplar_files"], ids=lambda rel: Path(rel).stem)
def test_invalid_fixture_fails_for_the_stated_reasons_only(rel):
    report = _validate(EXT_DIR / rel, ["forced-labor"])
    assert report.conforms is False, rel
    assert report.undeclared_concepts == (), rel
    import re

    results = re.split(r"\n(?=Constraint Violation in|Validation Result in)", report.validator_diagnostics)
    violations = [block for block in results if "Severity: sh:Violation" in block]
    focus = sorted({line.split("Focus Node:", 1)[1].strip() for v in violations for line in v.splitlines() if "Focus Node:" in line})
    assert focus == ["ex:action-no-instrument", "ex:phase-bare"], focus
    messages = " ".join(violations)
    assert "must carry >=1 uco-action:instrument" in messages
    assert "prov:wasDerivedFrom" in messages and "ConfidenceFacet" in messages
    assert report.violation_count == 4, report.violation_count


@needs_validator
def test_chain_starting_at_control_without_recruitment_conforms(tmp_path):
    """Forced labour exists without a trafficking act. A Control -> ForcedLabor
    chain with no Recruitment occupancy must validate; that is what makes this
    a forced-labour alphabet rather than a trafficking one."""
    graph = tmp_path / "control-start.ttl"
    graph.write_text(
        """
@prefix fl: <http://example.org/ontology/forced-labor/> .
@prefix ex: <http://example.org/forced-labor/control-start/> .
@prefix traj: <http://example.org/ontology/trajectories/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix uco-action: <https://ontology.unifiedcyberontology.org/uco/action/> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:employer a uco-identity:Person ; uco-core:name "Employer (fixture)" .
ex:evidence a uco-core:UcoObject ; uco-core:name "Fixture source" .
ex:passport a uco-core:UcoObject ; uco-core:name "Withheld passport (fixture)" .
ex:interval a time:ProperInterval ; uco-core:name "Fixture interval" .
ex:c1 a uco-core:ConfidenceFacet ; uco-core:confidence "80"^^xsd:nonNegativeInteger .
ex:c2 a uco-core:ConfidenceFacet ; uco-core:confidence "80"^^xsd:nonNegativeInteger .

ex:coerce a uco-action:Action , fl:a_coerce_labor ;
    uco-core:name "Keep the passport" ;
    uco-action:performer ex:employer ; uco-action:instrument ex:passport ;
    prov:wasDerivedFrom ex:evidence .

ex:p0 a traj:PhaseAssertion ; traj:assertsState fl:Control ; traj:atInterval ex:interval ;
    traj:sequenceIndex "0"^^xsd:nonNegativeInteger ; prov:wasDerivedFrom ex:evidence ; uco-core:hasFacet ex:c1 .
ex:p1 a traj:PhaseAssertion ; traj:assertsState fl:ForcedLabor ; traj:atInterval ex:interval ;
    traj:sequenceIndex "1"^^xsd:nonNegativeInteger ; traj:isTerminal true ; traj:terminalPolarity "disrupted" ;
    prov:wasDerivedFrom ex:evidence ; uco-core:hasFacet ex:c2 .
ex:trajectory a traj:Trajectory ; uco-core:name "Control start" ; traj:hasPhaseAssertion ex:p0 , ex:p1 .
ex:trigger a uco-core:UcoObject ; uco-core:name "Trigger (fixture)" .
ex:t1 a traj:Transition ; traj:fromState fl:Control ; traj:toState fl:ForcedLabor ;
    traj:trigger ex:trigger ; traj:enactsAction ex:coerce .
""",
        encoding="utf-8",
    )
    report = _validate(graph, ["forced-labor"])
    assert report.conforms is True, report.safe_summary
    assert report.undeclared_concepts == ()


@needs_validator
def test_unselected_alphabet_fails_closed():
    report = _validate(EXT_DIR / "forced-labor-exemplar.ttl", ["trajectories"])
    assert report.conforms is not True
    assert TECHNIQUES <= set(report.undeclared_concepts)


@needs_validator
def test_layered_exemplar_conforms_through_depends_on():
    report = _validate(LAYERED_EXEMPLAR, ["layered"])
    assert report.conforms is True, report.safe_summary
    assert report.undeclared_concepts == ()
    assert "forced-labor" in report.selected_extensions
