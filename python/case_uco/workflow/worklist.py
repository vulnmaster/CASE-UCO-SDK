"""Worklist forensic-boundary partitioning (Phase 4)."""

from __future__ import annotations

from collections import defaultdict
from pathlib import PurePosixPath
from typing import Any


def infer_boundary_key(path: str | None, explicit: str | None = None) -> str:
    """Resolve a work-item boundary.

    Order: explicit key → first path component (drive-letter → ``volume-X``)
    → ``_default``. Never keys identity on basename alone.
    """
    if explicit:
        return str(explicit)
    text = (path or "").replace("\\", "/").strip().lstrip("./")
    if not text or "/" not in text:
        return "_default"
    first = PurePosixPath(text).parts[0] if text else ""
    if not first or first in {".", ".."}:
        return "_default"
    if len(first) == 1 and first.isalnum():
        return f"volume-{first.upper()}"
    return first


def partition_worklist(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Split WorkItems by boundary_key. Missing key is inferred, else ``_default``."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        key = infer_boundary_key(item.get("path"), item.get("boundary_key"))
        item = dict(item)
        item["boundary_key"] = key
        groups[key].append(item)
    return dict(groups)


def estimate_partition_triples(items: list[dict[str, Any]], *, per_item: int = 25) -> int:
    """Conservative RAM-guard estimate (PERFORMANCE_GUIDE: 15–25 triples/item)."""
    return max(0, len(items)) * max(1, int(per_item))


def ram_guard_findings(
    groups: dict[str, list[dict[str, Any]]],
    *,
    max_estimated_triples: int = 200000,
) -> list[dict[str, Any]]:
    """Non-blocking findings when a partition would exceed air-gap comfort."""
    findings: list[dict[str, Any]] = []
    for key, items in groups.items():
        estimated = estimate_partition_triples(items)
        if estimated <= max_estimated_triples:
            continue
        findings.append(
            {
                "severity": "warning",
                "message": (
                    f"Partition {key} estimates {estimated} triples "
                    f"(comfort {max_estimated_triples}); split the worklist further."
                ),
                "path": key,
                "rule_id": "PROF-PART-001",
                "blocking": False,
                "repair": {"hint": "One graph per forensic boundary; do not SHACL the monolith."},
            }
        )
    return findings
