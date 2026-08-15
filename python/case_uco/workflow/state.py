"""Atomic workflow-state persistence."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_run_id() -> str:
    return f"wf-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid4().hex[:8]}"


def default_state(
    *,
    workflow_id: str,
    workflow_version: str,
    profile_id: str,
    profile_version: str,
    scenario: str,
    working_dir: Path,
    kb_prefix: str,
    inputs: dict[str, Any],
) -> dict[str, Any]:
    run_id = new_run_id()
    return {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "workflow_id": workflow_id,
        "workflow_version": workflow_version,
        "profile_id": profile_id,
        "profile_version": profile_version,
        "scenario": scenario,
        "status": "planned",
        "air_gapped": True,
        "created_at": utcnow(),
        "updated_at": utcnow(),
        "kb_prefix": kb_prefix,
        "working_dir": str(working_dir),
        "inputs": dict(inputs),
        "cursor": {
            "completed_steps": [],
            "running_steps": [],
            "failed_steps": [],
            "deferred_findings": [],
        },
        "worklist": [],
        "partitions": {
            "_default": {
                "graph_path": str(working_dir / "default.jsonld"),
                "status": "planned",
                "estimated_triples": 0,
                "nodes": 0,
                "findings_open": 0,
                "sha256": None,
            }
        },
        "findings": [],
        "artifacts": [],
        "validation": {"last_run": None, "conforms": None, "available": None},
        "step_timings": {},
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".wf-", suffix=".json.tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_state(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
