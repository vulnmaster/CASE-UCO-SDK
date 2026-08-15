"""Trajectory contracts over existing CASE/UCO/CAC terms. No new OWL."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from case_uco.registry import get_class
from case_uco.topology.paths import repo_root_candidates


@dataclass(frozen=True)
class TrajectoryContract:
    id: str
    version: str
    title: str
    phases: tuple[dict[str, Any], ...]
    air_gapped: bool = True


def trajectory_dirs() -> list[Path]:
    dirs: list[Path] = []
    for root in repo_root_candidates():
        dirs.append(root / "topology" / "trajectories")
    dirs.append(Path(__file__).resolve().parents[1] / "topology" / "data" / "trajectories")
    return [d for d in dirs if d.is_dir()]


def load_trajectory(trajectory_id: str) -> TrajectoryContract:
    for directory in trajectory_dirs():
        path = directory / f"{trajectory_id}.json"
        if path.is_file():
            raw = json.loads(path.read_text(encoding="utf-8"))
            return TrajectoryContract(
                id=raw["id"],
                version=raw.get("version") or "1.0.0",
                title=raw.get("title") or raw["id"],
                phases=tuple(raw.get("phases") or []),
                air_gapped=bool(raw.get("air_gapped", True)),
            )
    raise ValueError(f"Unknown trajectory: {trajectory_id}")


def evaluate_trajectory(graph: Any, trajectory_id: str) -> list[dict[str, Any]]:
    contract = load_trajectory(trajectory_id)
    findings: list[dict[str, Any]] = []
    blob = graph.serialize().lower()
    for phase in contract.phases:
        if not phase.get("required"):
            continue
        names = [t.split(":")[-1] for t in phase.get("types") or []]
        if not any(name.lower() in blob for name in names):
            type_name = names[0] if names else phase["id"]
            if names and get_class(names[0]) is None:
                code = "PROF-TRAJ-NOT-GENERATED"
                hint = generate_lag_hint(type_name, trajectory_id, phase["id"])
            else:
                code = "PROF-TRAJ-INCOMPLETE"
                hint = f"Advance trajectory {trajectory_id} to phase {phase['id']} with advance() or an existing OWL type."
            findings.append(
                {
                    "severity": "warning",
                    "message": f"Trajectory {trajectory_id} missing phase {phase['id']}"
                    + (f" ({type_name})" if type_name else ""),
                    "path": phase["id"],
                    "rule_id": code,
                    "repair": {
                        "hint": hint,
                        "workflow_step": "advance_trajectory",
                        "type": type_name,
                    },
                }
            )
    return findings


def advance(graph: Any, trajectory_id: str, phase_id: str, **kwargs: Any) -> Any:
    """Create an instance of an already-generated type, or record a generate-lag finding."""
    contract = load_trajectory(trajectory_id)
    phase = next((p for p in contract.phases if p["id"] == phase_id), None)
    if phase is None:
        raise ValueError(f"Unknown phase {phase_id} on {trajectory_id}")
    type_name = (phase.get("types") or ["InvestigativeAction"])[0].split(":")[-1]
    info = get_class(type_name)
    if info is None:
        placeholder_id = f"{getattr(graph, 'kb_prefix', 'http://example.org/kb/')}Phase-{phase_id}"
        graph.upsert_node(
            placeholder_id,
            types=["uco-core:UcoObject"],
            properties={
                "uco-core:name": phase_id,
                "uco-core:tag": f"trajectory:{trajectory_id}:{phase_id};generate-lag:{type_name};PROF-TRAJ-NOT-GENERATED",
                "uco-core:description": generate_lag_hint(type_name, trajectory_id, phase_id),
            },
        )
        return {
            "status": "not_generated",
            "rule_id": "PROF-TRAJ-NOT-GENERATED",
            "type": type_name,
            "phase_id": phase_id,
            "placeholder_id": placeholder_id,
            "hint": generate_lag_hint(type_name, trajectory_id, phase_id),
            "repair": {
                "hint": generate_lag_hint(type_name, trajectory_id, phase_id),
                "workflow_step": "advance_trajectory",
                "type": type_name,
            },
        }
    from case_uco.case.investigation import InvestigativeAction

    return graph.create(InvestigativeAction, name=f"{trajectory_id}:{phase_id}")


def generate_lag_hint(type_name: str, trajectory_id: str, phase_id: str) -> str:
    """Actionable generate-lag message. Not an ontology-gap / change-proposal."""
    return (
        f"{type_name} exists in OWL but is not in generated bindings "
        f"(trajectory {trajectory_id} phase {phase_id}). "
        "This is generate-lag, not a missing ontology term and not a change-proposal gap. "
        "Run the existing generator (`case-uco-generate` from the repo, or "
        "`python -m case_uco_generator`) and re-import the type. "
        "Until then, advance() upserts a tagged uco-core:UcoObject placeholder; "
        "do not invent a typed ConditioningPhase class by hand."
    )
