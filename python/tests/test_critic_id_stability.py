"""CRIT-H-* finding IDs match the MCP critic when that tree is importable."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from case_uco.critique.findings import make_stable_finding_id
from case_uco.critique.heuristics import evaluate_heuristics
from case_uco.graph import CASEGraph
from case_uco.case.investigation import Investigation


def test_make_stable_finding_id_algorithm() -> None:
    a = make_stable_finding_id("CRIT-H-INV-NO-OBJECT", "http://example.org/kb/x", "https://ontology.unifiedcyberontology.org/uco/core/object")
    b = make_stable_finding_id("CRIT-H-INV-NO-OBJECT", "http://example.org/kb/x", "https://ontology.unifiedcyberontology.org/uco/core/object")
    assert a == b
    assert a.startswith("CRIT-")


def test_investigation_missing_object_emits_heuristic() -> None:
    graph = CASEGraph()
    graph.create(Investigation, name="empty case")
    findings, _ = evaluate_heuristics(graph, "MinimalForensics")
    assert any(f.rule_id == "CRIT-H-INV-NO-OBJECT" for f in findings)


def test_id_matches_mcp_critic_when_available() -> None:
    repo = Path(__file__).resolve().parents[2]
    mcp = repo / "mcp_server"
    if not mcp.is_dir():
        return
    sys.path.insert(0, str(mcp))
    try:
        from critic.models import make_stable_finding_id as mcp_id
    except Exception:
        return
    rule = "CRIT-H-INV-NO-OBJECT"
    node = "http://example.org/kb/Investigation-1"
    pred = "https://ontology.unifiedcyberontology.org/uco/core/object"
    assert make_stable_finding_id(rule, node, pred) == mcp_id(rule, node, pred)
