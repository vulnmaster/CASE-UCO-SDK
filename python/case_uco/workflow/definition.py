"""Load Investigation Workflow definitions (offline JSON)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from case_uco.topology.paths import repo_root_candidates


def workflow_dirs() -> list[Path]:
    dirs: list[Path] = []
    for root in repo_root_candidates():
        dirs.append(root / "topology" / "workflows")
    packaged = Path(__file__).resolve().parents[1] / "topology" / "data" / "workflows"
    dirs.append(packaged)
    seen: set[Path] = set()
    out: list[Path] = []
    for path in dirs:
        if path.exists() and path.resolve() not in seen:
            seen.add(path.resolve())
            out.append(path)
    return out


@dataclass(frozen=True)
class WorkflowStep:
    id: str
    kind: str
    depends_on: tuple[str, ...] = ()
    handler: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    optional: bool = False
    critique: str = "step"
    on_blocking: str = "continue"
    isolation: str = "exclusive"
    partition_scope: str = "all"


@dataclass(frozen=True)
class WorkflowDefinition:
    id: str
    version: str
    profile: str
    title: str
    description: str
    air_gapped: bool
    steps: tuple[WorkflowStep, ...]
    inputs: tuple[dict[str, Any], ...] = ()
    partition_policy: dict[str, Any] = field(default_factory=dict)
    related_dags: tuple[str, ...] = ()
    source_path: str = ""


def list_workflows() -> list[WorkflowDefinition]:
    return [item for _, item in sorted(_load_all().items())]


def get_workflow(workflow_id: str) -> WorkflowDefinition | None:
    table = _load_all()
    if workflow_id in table:
        return table[workflow_id]
    lowered = workflow_id.lower()
    for key, item in table.items():
        if key.lower() == lowered:
            return item
    return None


def _load_all() -> dict[str, WorkflowDefinition]:
    loaded: dict[str, WorkflowDefinition] = {}
    for directory in workflow_dirs():
        for path in sorted(directory.glob("*.json")):
            if path.name.endswith(".schema.json"):
                continue
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if "id" not in raw or "steps" not in raw:
                continue
            loaded.setdefault(raw["id"], _parse(raw, path))
    return loaded


def _parse(raw: dict[str, Any], path: Path) -> WorkflowDefinition:
    steps = []
    for item in raw.get("steps") or []:
        steps.append(
            WorkflowStep(
                id=item["id"],
                kind=item["kind"],
                depends_on=tuple(item.get("depends_on") or []),
                handler=item.get("handler") or item["kind"],
                args=dict(item.get("args") or {}),
                optional=bool(item.get("optional")),
                critique=item.get("critique") or "step",
                on_blocking=item.get("on_blocking") or "continue",
                isolation=item.get("isolation") or "exclusive",
                partition_scope=item.get("partition_scope") or "all",
            )
        )
    return WorkflowDefinition(
        id=raw["id"],
        version=raw.get("version") or "1.0.0",
        profile=raw["profile"],
        title=raw.get("title") or raw["id"],
        description=raw.get("description") or "",
        air_gapped=bool(raw.get("air_gapped", True)),
        steps=tuple(steps),
        inputs=tuple(raw.get("inputs") or []),
        partition_policy=dict(raw.get("partition_policy") or {}),
        related_dags=tuple(raw.get("related_dags") or []),
        source_path=str(path),
    )
