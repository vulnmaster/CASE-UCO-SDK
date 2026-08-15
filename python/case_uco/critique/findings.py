"""Construction findings and exporters."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Literal

FindingWhen = Literal["incremental", "step", "graph"]
CompatSeverity = Literal["error", "warning", "critical", "high", "medium", "low", "info"]

_CRITIC_SEVERITY = {"critical", "high", "medium", "low", "info"}
_COMPAT_TO_NORM = {"error": "high", "warning": "medium"}


def make_stable_finding_id(rule_id: str, *semantic_parts: str) -> str:
    """Port of mcp_server.critic.models.make_stable_finding_id (no MCP import)."""
    normalized = [rule_id.strip()]
    for part in semantic_parts:
        text = (part or "").strip()
        if text:
            normalized.append(text)
    digest = hashlib.sha256("|".join(normalized).encode("utf-8")).hexdigest()[:16]
    return f"CRIT-{digest}"


@dataclass
class ConstructionFinding:
    """Internal construction finding. Not a critic-schema document."""

    rule_id: str
    severity: CompatSeverity
    message: str
    path: str = ""
    blocking: bool = True
    profile_id: str = ""
    when: str = "incremental"
    step_id: str | None = None
    partition: str | None = None
    category: str = "construction"
    confidence: float = 1.0
    status: str = "new"
    node_id: str | None = None
    predicate: str | None = None
    host: str | None = None
    evidence: list[str] = field(default_factory=list)
    rationale: str = ""
    recommended_change: str = ""
    verification_method: str = ""
    repair: dict[str, Any] = field(default_factory=dict)
    finding_id: str = ""

    def __post_init__(self) -> None:
        if not self.finding_id:
            parts = [p for p in (self.node_id, self.predicate, self.path) if p]
            self.finding_id = make_stable_finding_id(self.rule_id, *parts)
        if not self.rationale:
            self.rationale = self.message
        if not self.recommended_change:
            self.recommended_change = (self.repair or {}).get("hint") or self.message

    @property
    def severity_norm(self) -> str:
        return _COMPAT_TO_NORM.get(self.severity, self.severity)

    def to_compat_dict(self) -> dict[str, Any]:
        """InvestigationBuilder.critique() payload. Always has severity/message/path."""
        return {
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
            "schema_version": "2.0.0",
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "severity_norm": self.severity_norm,
            "category": self.category,
            "confidence": self.confidence,
            "status": self.status,
            "blocking": self.blocking,
            "profile_id": self.profile_id,
            "step_id": self.step_id,
            "partition": self.partition,
            "message_detail": self.rationale,
            "recommended_change": self.recommended_change,
            "repair": dict(self.repair or {}),
            "target": {
                "node_id": self.node_id,
                "predicate": self.predicate,
                "host": self.host,
            },
        }

    def to_critic_finding(self) -> dict[str, Any]:
        """Projection valid against critic-finding.schema.json (no extra keys)."""
        severity = self.severity_norm if self.severity_norm in _CRITIC_SEVERITY else "high"
        return {
            "finding_id": self.finding_id,
            "severity": severity,
            "category": self.category,
            "confidence": self.confidence,
            "status": self.status,
            "target": {
                "path": self.path or None,
                "line": None,
                "node_id": self.node_id,
                "predicate": self.predicate,
                "counterpart_id": None,
                "json_pointer": None,
                "qualified_name": None,
            },
            "evidence_kind": "deterministic",
            "evidence": list(self.evidence),
            "rationale": self.rationale or self.message,
            "recommended_change": self.recommended_change,
            "verification_method": self.verification_method or self.rule_id,
            "rule_id": self.rule_id,
            "verifier_rule_id": self.rule_id,
            "suppressible": True,
        }
