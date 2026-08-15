"""Worklist forensic-boundary partitioning (Phase 4)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def partition_worklist(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Split WorkItems by boundary_key. Missing key → `_default`."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        key = item.get("boundary_key") or "_default"
        groups[str(key)].append(item)
    return dict(groups)
