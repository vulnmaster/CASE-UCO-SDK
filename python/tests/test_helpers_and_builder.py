"""Tests for fluent helpers, InvestigationBuilder, and hash indexes."""

from __future__ import annotations

from case_uco import (
    CASEGraph,
    InvestigationBuilder,
    file_with_content_hashes,
    model_csam_evidence,
)
from case_uco.helpers import model_tool_run


def test_file_with_content_hashes_indexes() -> None:
    graph = CASEGraph()
    file_with_content_hashes(
        graph,
        file_name="evidence.bin",
        hashes=[("SHA256", "e3b0c44298fc1c149afbf4c8996fb924")],
    )
    hits = graph.lookup_hash("E3B0C44298FC1C149AFBF4C8996FB924")
    assert hits
    assert hits[0]["method"]


def test_model_csam_evidence_creates_tool_and_picture() -> None:
    graph = CASEGraph()
    parts = model_csam_evidence(
        graph,
        file_name="img.jpg",
        hashes=[("SHA256", "aa"), ("PhotoDNA", "bb")],
    )
    assert parts["tool"].name == "PhotoDNA"
    assert len(graph) >= 3


def test_investigation_builder_inline_critique() -> None:
    builder = InvestigationBuilder("field triage of hashed images", profile_id="AirGappedFieldTriage")
    builder.add_file("nohash.txt")
    builder.add_file("ok.bin", hashes=[("SHA256", "ab")])
    builder.add_tool_run("Triage Collector", "scan", tool_version=None)
    assert any(f["severity"] == "error" for f in builder.critique())
    assert any("version" in f["message"] for f in builder.critique())
    assert builder.profile.id == "AirGappedFieldTriage"
    assert len(builder.build()) >= 2


def test_partition_by_profile_returns_core() -> None:
    graph = CASEGraph()
    file_with_content_hashes(graph, file_name="a.bin", hashes=[("SHA256", "cc")])
    parts = graph.partition_by_profile("MinimalForensics")
    assert "core" in parts


def test_model_tool_run() -> None:
    graph = CASEGraph()
    parts = model_tool_run(graph, tool_name="Autopsy", tool_version="4.21", action_name="ingest")
    assert parts["tool"].version == "4.21"
    assert len(graph) == 2
