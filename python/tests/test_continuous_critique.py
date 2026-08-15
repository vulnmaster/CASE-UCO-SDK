"""Continuous critique: frozen builder triples, exporters, SHACL skip."""

from __future__ import annotations

from case_uco import InvestigationBuilder
from case_uco.critique.findings import ConstructionFinding


def test_frozen_builder_triples() -> None:
    builder = InvestigationBuilder("field triage of hashed images", profile_id="AirGappedFieldTriage")
    builder.add_file("nohash.txt")
    builder.add_file("ok.bin", hashes=[("SHA256", "ab")])
    builder.add_tool_run("Triage Collector", "scan", tool_version=None)
    findings = builder.critique()
    assert any(f["severity"] == "error" for f in findings)
    assert any("version" in f["message"] for f in findings)
    triples = {(f["severity"], f["path"]) for f in findings}
    assert ("error", "nohash.txt") in triples
    assert ("warning", "Triage Collector") in triples
    for item in findings:
        assert {"severity", "message", "path"} <= set(item)
    assert len(builder.build()) >= 2


def test_csam_empty_hash_message() -> None:
    builder = InvestigationBuilder("hashed CSAM", profile_id="HashIntelligence")
    builder.add_csam_evidence("img.jpg", hashes=[])
    findings = builder.critique()
    assert any(
        f["severity"] == "error" and f["path"] == "img.jpg" and "CSAM evidence must carry hashes" in f["message"]
        for f in findings
    )


def test_to_critic_finding_has_no_extra_keys() -> None:
    finding = ConstructionFinding(
        rule_id="PROF-HASH-001",
        severity="error",
        message="missing hashes",
        path="img.jpg",
        node_id="kb:File-1",
        predicate="https://ontology.unifiedcyberontology.org/uco/observable/hash",
    )
    payload = finding.to_critic_finding()
    assert payload["severity"] == "high"
    assert "message" not in payload
    assert "path" not in payload
    assert "repair" not in payload
    assert "schema_version" not in payload
    assert "blocking" not in payload
    assert payload["rule_id"] == "PROF-HASH-001"


def test_shacl_skipped_when_validator_unavailable(monkeypatch) -> None:
    import case_uco.critique.signals as signals

    monkeypatch.setattr("case_uco.validation.graph.validator_available", lambda: False)
    builder = InvestigationBuilder("triage", profile_id="MinimalForensics")
    builder.add_file("ok.bin", hashes=[("SHA256", "ab")])
    report = builder.critique_report()
    skipped = [e for e in report.rule_executions if e.get("status") == "skipped"]
    assert skipped
    assert all(e.get("error_code") == "validator_unavailable" for e in skipped)
    if report.shacl:
        assert report.shacl.get("conforms") is not True


def test_critique_report_graph_wide() -> None:
    builder = InvestigationBuilder("hashed images", profile_id="HashIntelligence")
    builder.add_csam_evidence("img.jpg", hashes=[("SHA256", "aa"), ("PhotoDNA", "bb")])
    report = builder.critique_report(when="graph")
    assert report.profile_id == "HashIntelligence"
    assert report.schema_version == "2.0.0"
    assert report.estimated_triples >= 0


def test_construction_heuristic_subset_covers_design_minimum() -> None:
    from case_uco.case.investigation import Investigation
    from case_uco.critique.heuristics import evaluate_heuristics
    from case_uco.graph import CASEGraph
    from case_uco.helpers import file_with_content_hashes

    graph = CASEGraph()
    graph.create(Investigation, name="case")
    file_with_content_hashes(graph, file_name="disk.bin", hashes=[("SHA256", "aa")], id="kb:src")
    graph.upsert_node(
        "kb:derived",
        types=["uco-observable:File"],
        properties={"uco-core:name": "carved.bin"},
    )
    graph.create_relationship("kb:derived", "kb:src", "Extracted_From")
    graph.upsert_node(
        "kb:charge",
        types=["legalproc:CriminalCharge"],
        properties={"uco-core:name": "18 USC 2251"},
    )
    graph.upsert_node(
        "kb:person",
        types=["uco-identity:Person"],
        properties={"uco-core:name": "Doe"},
    )
    graph.create_relationship("kb:charge", "kb:person", "Charged_With")
    graph.upsert_node(
        "kb:e01",
        types=["uco-observable:RasterPicture"],
        properties={"uco-core:name": "volume.e01"},
    )
    graph.upsert_node(
        "kb:orphan",
        types=["uco-observable:File"],
        properties={"uco-core:name": "loose.bin"},
    )
    findings, executions = evaluate_heuristics(graph, "LegalProcess")
    ids = {f.rule_id for f in findings}
    assert "CRIT-H-INV-NO-OBJECT" in ids
    assert "CRIT-H-DERIVED-NO-HASH" in ids
    assert "CRIT-H-CHARGED-WITH-REVERSED" in ids
    assert "CRIT-H-IMAGE-CONTAINER-MISMATCH" in ids
    assert "CRIT-H-ORPHAN-TOP-LEVEL" in ids
    executed = {e["rule_id"] for e in executions if e.get("status") == "evaluated"}
    assert "CRIT-H-DERIVED-NO-PROVENANCE" in executed


def test_graph_pass_tool_version_and_legal_mission() -> None:
    from case_uco.contracts import load_contract
    from case_uco.critique.graph_pass import evaluate_graph_pass
    from case_uco.graph import CASEGraph
    from case_uco.uco.tool import Tool

    graph = CASEGraph()
    graph.create(Tool, name="Unversioned Imager")
    graph.upsert_node(
        "kb:charge",
        types=["legalproc:CriminalCharge"],
        properties={"uco-core:name": "count 1"},
    )
    legal = load_contract("LegalProcess")
    legal_findings = evaluate_graph_pass(graph, legal, when="graph")
    assert any(f.rule_id == "PROF-LEGAL-001" for f in legal_findings)

    tools = load_contract("ToolMapping")
    tool_findings = evaluate_graph_pass(graph, tools, when="graph")
    assert any(f.rule_id == "PROF-TOOL-001" and "version" in f.message.lower() for f in tool_findings)


def test_cac_lifecycle_mission_requires_hashes_and_role() -> None:
    builder = InvestigationBuilder("lifecycle", profile_id="FullCACLifecycle")
    builder.add_file("img.jpg")
    builder.graph.upsert_node(
        "kb:person",
        types=["uco-identity:Person"],
        properties={"uco-core:name": "victim"},
    )
    report = builder.critique_report(when="graph")
    messages = [f.message for f in report.findings]
    assert any("hashes" in m.lower() or "Role" in m for m in messages)
    kinds = {c.kind for c in builder.contract.checks}
    assert "spine_kind_present" in kinds
    assert "trajectory_completeness" in kinds
    assert "cac_lifecycle_mission" in kinds
