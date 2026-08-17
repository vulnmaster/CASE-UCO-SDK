"""Focused checks for the MCP-critic continuous-critique wrapper."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco.case.investigation import Investigation
from case_uco.continuous_critique import (
    ContinuousCritiqueUnavailable,
    critique_graph,
)
from case_uco.graph import CASEGraph
from case_uco.uco.core import UcoObject

REPO_ROOT = Path(__file__).resolve().parents[2]
WRAPPER_PATH = REPO_ROOT / "python" / "case_uco" / "continuous_critique.py"
CRITIC_PATH = REPO_ROOT / "mcp_server" / "critic" / "continuous.py"
DOC_PATH = REPO_ROOT / "docs" / "CONTINUOUS_CRITIQUE.md"

FORBIDDEN_SUBSTRINGS = (
    "photodna",
    "photo-dna",
    "vics",
    "court-defensible",
    "court defensible",
    "2.0.0",
    "2.0.1",
    "investigationworkflow",
    "model_csam",
)


def test_public_surface_does_not_duplicate_the_critic() -> None:
    import case_uco.continuous_critique as wrapper

    assert wrapper.PUBLIC_SURFACE == ("critique_graph",)
    assert not hasattr(wrapper, "ProfileCritic")
    assert not hasattr(wrapper, "evaluate_heuristics")
    assert not (REPO_ROOT / "python" / "case_uco" / "critique").exists()


def test_missing_investigation_object_is_stable_and_actionable() -> None:
    graph = CASEGraph()
    graph.create(Investigation, name="Case 1", id="kb:Investigation-1")
    first = critique_graph(graph)
    second = critique_graph(graph)
    inv = [item for item in first if item["rule_id"] == "CRIT-H-INV-NO-OBJECT"]
    assert inv
    assert inv[0]["finding_id"].startswith("CRIT-")
    assert inv[0]["repair_hint"]
    assert inv[0]["node_id"]
    assert first == second


def test_adding_object_clears_the_investigation_finding() -> None:
    graph = CASEGraph()
    subject = graph.create(UcoObject, name="Exhibit A", id="kb:Object-1")
    graph.create(
        Investigation,
        name="Case 1",
        id="kb:Investigation-1",
        object=[subject],
    )
    remaining = [
        item
        for item in critique_graph(graph)
        if item["rule_id"] == "CRIT-H-INV-NO-OBJECT"
    ]
    assert remaining == []


def test_oversize_payload_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    sys.path.insert(0, str(REPO_ROOT / "mcp_server"))
    import critic.continuous as continuous

    monkeypatch.setattr(continuous, "MAX_GRAPH_BYTES", 32)
    graph = CASEGraph()
    graph.create(Investigation, name="Case 1", id="kb:Investigation-1")
    with pytest.raises(continuous.ContinuousCritiqueError, match="exceeds"):
        continuous.critique_jsonld(graph.serialize(), max_bytes=32)


def test_unavailable_critic_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    import case_uco.continuous_critique as wrapper

    def boom() -> None:
        return None

    monkeypatch.setattr(wrapper, "_ensure_critic_on_path", boom)
    monkeypatch.setitem(sys.modules, "critic.continuous", None)
    # Force import failure on the next from-import.
    import builtins

    real_import = builtins.__import__

    def blocked(name, *args, **kwargs):
        if name == "critic.continuous":
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked)
    graph = CASEGraph()
    with pytest.raises(ContinuousCritiqueUnavailable, match="not importable"):
        wrapper.critique_graph(graph)


def test_wrapper_and_docs_are_public_safe() -> None:
    blob = WRAPPER_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + CRITIC_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + DOC_PATH.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"critique files contain forbidden substring {needle!r}"
    doc = DOC_PATH.read_text(encoding="utf-8").lower()
    assert "does not classify" in doc
    assert "does not add a second rule engine" in doc
