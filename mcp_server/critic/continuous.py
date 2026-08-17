"""Construction-time critique that reuses the existing MCP critic rules.

This module does not invent a second rule engine. It loads an in-memory
JSON-LD graph with the same canonical view as ``analyze_artifact`` and
runs the existing deterministic heuristics. Findings keep the critic's
stable ``finding_id`` values and expose ``recommended_change`` as
``repair_hint``.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from critic.canonical import (
    MAX_GRAPH_BYTES,
    load_canonical_jsonld_text,
)
from critic.graph_heuristics import run_graph_heuristics
from critic.models import CriticFinding

PUBLIC_SURFACE = ("critique_jsonld",)
RULE_VERSION = "1.3.3"


class ContinuousCritiqueError(ValueError):
    """Fail-closed critique refusal (size bound, empty input, unusable graph)."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def _artifact_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _compact_finding(finding: CriticFinding) -> dict[str, str]:
    finding.ensure_identity_key()
    target = finding.target
    return {
        "finding_id": finding.finding_id,
        "rule_id": finding.rule_id or "",
        "severity": finding.severity,
        "rationale": finding.rationale,
        "repair_hint": finding.recommended_change,
        "node_id": target.node_id or "",
        "predicate": target.predicate or "",
    }


def critique_jsonld(
    document: dict[str, Any] | str,
    *,
    profiles: list[str] | None = None,
    max_bytes: int = MAX_GRAPH_BYTES,
) -> list[dict[str, str]]:
    """Run existing CRIT-H-* heuristics on an in-memory JSON-LD graph.

    Offline. Does not classify content. Does not open network resources.
    Raises :class:`ContinuousCritiqueError` when the payload is empty,
    exceeds ``max_bytes``, or cannot be used for heuristics.
    """
    if isinstance(document, str):
        text = document
    else:
        text = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    size = len(text.encode("utf-8"))
    if size == 0:
        raise ContinuousCritiqueError("critic_graph_empty", "JSON-LD payload is empty")
    if size > max_bytes:
        raise ContinuousCritiqueError(
            "critic_graph_too_large",
            f"JSON-LD payload exceeds the critique bound ({max_bytes} bytes)",
        )

    view = load_canonical_jsonld_text(text, path_name="memory.jsonld")
    if view.json_status == "too_large":
        raise ContinuousCritiqueError(
            "critic_graph_too_large",
            "JSON-LD payload exceeds the critic size bound",
        )
    if not view.usable_for_heuristics:
        detail = ",".join(view.errors) if view.errors else view.json_status
        raise ContinuousCritiqueError(
            "critic_graph_unusable",
            f"graph is not usable for existing critic heuristics ({detail})",
        )

    findings, _executions = run_graph_heuristics(
        view,
        artifact_hash=_artifact_hash(text),
        profiles=list(profiles or []),
    )
    compact = [_compact_finding(item) for item in findings]
    compact.sort(key=lambda item: (item.get("rule_id") or "", item.get("finding_id") or ""))
    return compact
