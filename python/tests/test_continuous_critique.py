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
