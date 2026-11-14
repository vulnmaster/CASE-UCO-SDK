"""Regressions for validation and document-processor issues #49, #50, #51, #58."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import document_processor as dp
import server
from case_uco.validation.coverage import check_graph_concepts
from case_uco.validation.graph import (
    parse_violation_details,
    report_to_dict,
    required_extensions_for_graph,
    validate_graph_file,
    validator_available,
)

needs_validator = pytest.mark.skipif(
    not validator_available(), reason="case_validate not installed"
)

WALLET_CSV = "wallet,amount\n1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa,1\n"


def _write_thread(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "@context": {
                    "kb": "http://example.org/kb/",
                    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
                    "co": "http://purl.org/co/",
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                },
                "@graph": [
                    {
                        "@id": "kb:thread-1",
                        "@type": "uco-types:Thread",
                        "co:size": {"@type": "xsd:nonNegativeInteger", "@value": "1"},
                        "co:index": {"@type": "xsd:positiveInteger", "@value": "1"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


# --- #50: vendored Collections Ontology terms are declared --------------------


def test_coverage_accepts_collections_ontology_terms(tmp_path: Path) -> None:
    coverage = check_graph_concepts(_write_thread(tmp_path / "thread.jsonld"))
    assert "http://purl.org/co/size" not in coverage.undeclared_properties
    assert "http://purl.org/co/index" not in coverage.undeclared_properties
    assert coverage.ok


@needs_validator
def test_validate_graph_file_conforms_for_collections_terms(tmp_path: Path) -> None:
    report = validate_graph_file(_write_thread(tmp_path / "thread.jsonld"))
    assert report.conforms is True
    assert not report.undeclared_concepts


# --- #51: extra_ontology_graphs alone feeds coverage --------------------------


@needs_validator
def test_extra_ontology_graphs_alone_share_bundle_with_coverage(tmp_path: Path) -> None:
    ontology = tmp_path / "widget.ttl"
    ontology.write_text(
        "@prefix ex: <http://example.org/ont/> .\n"
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        "@prefix sh: <http://www.w3.org/ns/shacl#> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
        'ex:Widget a owl:Class, sh:NodeShape ; rdfs:label "Widget"@en ;\n'
        "  sh:property [ sh:path ex:label ; sh:datatype xsd:string ; sh:minCount 1 ] .\n"
        'ex:label a owl:DatatypeProperty ; rdfs:label "label"@en .\n',
        encoding="utf-8",
    )
    graph = tmp_path / "widget.jsonld"
    graph.write_text(
        json.dumps(
            {
                "@context": {"kb": "http://example.org/kb/", "ex": "http://example.org/ont/"},
                "@graph": [{"@id": "kb:w1", "@type": "ex:Widget", "ex:label": "ok"}],
            }
        ),
        encoding="utf-8",
    )
    report = validate_graph_file(graph, extra_ontology_graphs=[ontology], strict_concepts=True)
    assert dict(report.stage_status)["bundle_resolution"] == "complete"
    assert not report.undeclared_concepts
    assert report.conforms is True


# --- #49: required-extension handoff ------------------------------------------


def test_required_extensions_names_extension_namespaces_only() -> None:
    document = {
        "@context": {
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "cryptoinv": "http://example.org/ontology/cryptoinv/",
        },
        "@graph": [
            {"@id": "kb:a", "@type": "uco-action:Action"},
            {
                "@id": "kb:f",
                "@type": ["cryptoinv:CryptocurrencyAddressFacet"],
                "cryptoinv:addressValue": "x",
            },
        ],
    }
    assert required_extensions_for_graph(document) == ["cryptoinv"]
    assert required_extensions_for_graph({"@graph": [document["@graph"][0]], "@context": document["@context"]}) == []


def test_required_extensions_counts_individuals_used_only_as_objects() -> None:
    """#127: fl:Control appears only as an object, and forced-labor declares it."""
    document = {
        "@context": {
            "kb": "http://example.org/kb/",
            "traj": "http://example.org/ontology/trajectories/",
            "fl": "http://example.org/ontology/forced-labor/",
        },
        "@graph": [
            {
                "@id": "kb:assertion-1",
                "@type": "traj:PhaseAssertion",
                "traj:assertsState": {"@id": "fl:Control"},
            }
        ],
    }
    assert required_extensions_for_graph(document) == ["forced-labor", "trajectories"]

    expanded = {
        "@graph": [
            {
                "@id": "http://example.org/kb/assertion-1",
                "@type": "http://example.org/ontology/trajectories/PhaseAssertion",
                "http://example.org/ontology/trajectories/assertsState": [
                    {"@id": "http://example.org/ontology/forced-labor/Control"}
                ],
            }
        ]
    }
    assert required_extensions_for_graph(expanded) == ["forced-labor", "trajectories"]

    # A top-level node's own @id is not a reference, and kb IRIs match no extension.
    own_id = {
        "@context": document["@context"],
        "@graph": [{"@id": "fl:Control", "@type": "traj:State"}],
    }
    assert required_extensions_for_graph(own_id) == ["trajectories"]


def test_processed_csv_reports_cryptoinv_and_validates_with_it(tmp_path: Path) -> None:
    source = tmp_path / "wallets.csv"
    source.write_text(WALLET_CSV, encoding="utf-8")
    output = tmp_path / "out" / "wallets.jsonld"
    doc = dp.process_document_file(source, output)
    assert doc.required_extensions == ("cryptoinv",)
    if validator_available():
        report = validate_graph_file(
            output, extensions=list(doc.required_extensions), strict_concepts=False
        )
        assert report.conforms is True


def test_mcp_tool_payload_carries_required_extensions(tmp_path: Path) -> None:
    source = tmp_path / "wallets.csv"
    source.write_text(WALLET_CSV, encoding="utf-8")
    tool = getattr(server.process_document_file, "fn", server.process_document_file)
    payload = tool(str(source), str(tmp_path / "out" / "wallets.jsonld"))
    assert payload["ok"] is True
    assert payload["required_extensions"] == ["cryptoinv"]
    assert "extensions=['cryptoinv']" in payload["safe_summary"]


# --- #58: the hashed bytes are the extracted bytes ----------------------------


def test_source_changed_during_extraction_keeps_hash_and_rows_consistent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "rows.csv"
    original = "name,amount\nalice,1\n"
    source.write_text(original, encoding="utf-8")
    real_extract = dp.extract_content

    def extract_after_concurrent_write(path: Path, *args, **kwargs):
        source.write_text("name,amount\nmallory,999\n", encoding="utf-8")
        return real_extract(path, *args, **kwargs)

    monkeypatch.setattr(dp, "extract_content", extract_after_concurrent_write)
    doc = dp.process_document_file(source, tmp_path / "out" / "rows.jsonld")

    assert doc.sha256 == hashlib.sha256(original.encode("utf-8")).hexdigest()
    assert doc.byte_size == len(original.encode("utf-8"))
    serialized = json.dumps(doc.graph)
    assert "alice" in serialized
    assert "mallory" not in serialized


def test_source_is_not_reread_for_hashing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "rows.csv"
    source.write_text("name,amount\nalice,1\n", encoding="utf-8")
    real_read_bytes = Path.read_bytes
    reads: list[Path] = []

    def counting_read_bytes(self: Path) -> bytes:
        if self == source:
            reads.append(self)
        return real_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", counting_read_bytes)
    dp.process_document_file(source, tmp_path / "out" / "rows.jsonld")
    assert reads == []


HUMAN_REPORT = """Validation Report
Conforms: False
Results (3):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
\tSeverity: sh:Violation
\tSource Shape: [ sh:path core:isDirectional ; sh:minCount Literal("1") ]
\tFocus Node: kb:relationship-1
\tResult Path: core:isDirectional
\tMessage: Less than 1 values on kb:relationship-1->core:isDirectional
Constraint Violation in DatatypeConstraintComponent (http://www.w3.org/ns/shacl#DatatypeConstraintComponent):
\tSeverity: sh:Violation
\tSource Shape: core:ShapeX
\tFocus Node: [ core:name Literal("private name") ]
\tValue Node: Literal("private name")
\tResult Path: [ sh:inversePath core:source ]
\tMessage: Value is not Literal with datatype xsd:string
Constraint Violation in ClassConstraintComponent (http://www.w3.org/ns/shacl#ClassConstraintComponent):
\tSeverity: sh:Violation
\tFocus Node: <http://example.org/kb/tool-1>
\tResult Path: unknown:prop
"""


def test_violation_details_carry_identifiers_only() -> None:
    prefixes = {
        "kb": "http://example.org/kb/",
        "core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "sh": "http://www.w3.org/ns/shacl#",
    }
    details, truncated = parse_violation_details(HUMAN_REPORT, prefixes)
    assert not truncated
    assert details == (
        {
            "focus_node": "http://example.org/kb/relationship-1",
            "result_path": "https://ontology.unifiedcyberontology.org/uco/core/isDirectional",
            "constraint_component": "http://www.w3.org/ns/shacl#MinCountConstraintComponent",
            "severity": "http://www.w3.org/ns/shacl#Violation",
        },
        {
            "focus_node": None,
            "result_path": None,
            "constraint_component": "http://www.w3.org/ns/shacl#DatatypeConstraintComponent",
            "severity": "http://www.w3.org/ns/shacl#Violation",
        },
        {
            "focus_node": "http://example.org/kb/tool-1",
            "result_path": None,
            "constraint_component": "http://www.w3.org/ns/shacl#ClassConstraintComponent",
            "severity": "http://www.w3.org/ns/shacl#Violation",
        },
    )
    assert "private name" not in json.dumps(details)
    assert parse_violation_details(HUMAN_REPORT, prefixes, limit=2)[1] is True


@needs_validator
def test_nonconforming_finding_names_node_path_and_constraint(tmp_path: Path) -> None:
    from critic.deterministic import _validation_findings
    from critic.models import ValidationSummary

    graph = tmp_path / "g.jsonld"
    graph.write_text(json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
        },
        "@graph": [
            {"@id": "kb:person-7f9c2a3e-1b4d-4c6e-9a8f-0d1e2f3a4b5c",
             "@type": "uco-identity:Person", "uco-core:name": "Alice Smith"},
            {"@id": "kb:org-2c4e6a8b-3d5f-4a7c-8e9f-1a2b3c4d5e6f",
             "@type": "uco-identity:Organization", "uco-core:name": "Acme"},
            {"@id": "kb:relationship-1c4e6a8b-3d5f-4a7c-8e9f-1a2b3c4d5e6f",
             "@type": "uco-core:Relationship",
             "uco-core:source": {"@id": "kb:person-7f9c2a3e-1b4d-4c6e-9a8f-0d1e2f3a4b5c"},
             "uco-core:target": {"@id": "kb:org-2c4e6a8b-3d5f-4a7c-8e9f-1a2b3c4d5e6f"},
             "uco-core:kindOfRelationship": "Employed_By"},
        ],
    }), encoding="utf-8")
    report = validate_graph_file(graph, strict_concepts=False)
    relationship = "http://example.org/kb/relationship-1c4e6a8b-3d5f-4a7c-8e9f-1a2b3c4d5e6f"
    expected = {
        "focus_node": relationship,
        "result_path": "https://ontology.unifiedcyberontology.org/uco/core/isDirectional",
        "constraint_component": "http://www.w3.org/ns/shacl#MinCountConstraintComponent",
        "severity": "http://www.w3.org/ns/shacl#Violation",
    }
    assert report.violation_details == (expected,)
    payload = report_to_dict(report)
    assert payload["violation_details"] == [expected]
    assert payload["violation_details_truncated"] is False
    assert "Alice Smith" not in json.dumps(payload["violation_details"])

    summary = ValidationSummary(
        conforms=report.conforms,
        verification_status=report.verification_status,
        violation_count=report.violation_count,
        violation_details=[dict(d) for d in report.violation_details],
    )
    [finding] = [
        f for f in _validation_findings(summary) if f.rule_id == "CRIT-V-NONCONFORMING"
    ]
    assert finding.target.node_id == relationship
    assert any(expected["result_path"] in item for item in finding.evidence)
