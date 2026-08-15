"""Trajectory contracts use existing OWL types; generate-lag is not an ontology gap."""

from __future__ import annotations

from case_uco.graph import CASEGraph
from case_uco.trajectories import advance, evaluate_trajectory, load_trajectory


def test_load_grooming_trajectory() -> None:
    traj = load_trajectory("grooming-phase")
    assert traj.id == "grooming-phase"
    assert traj.air_gapped is True
    assert any(p["id"] == "conditioning" for p in traj.phases)


def test_conditioning_is_generate_lag_not_ontology_gap() -> None:
    graph = CASEGraph()
    result = advance(graph, "grooming-phase", "conditioning")
    if isinstance(result, dict):
        assert result.get("rule_id") == "PROF-TRAJ-NOT-GENERATED"
        assert "generator" in result.get("hint", "").lower()


def test_evaluate_incomplete_trajectory() -> None:
    graph = CASEGraph()
    findings = evaluate_trajectory(graph, "grooming-phase")
    assert any(f["rule_id"].startswith("PROF-TRAJ") for f in findings)
