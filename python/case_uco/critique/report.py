"""CritiqueReport — construction-time evaluation result."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from case_uco.critique.findings import ConstructionFinding


@dataclass
class CritiqueReport:
    schema_version: str
    profile_id: str
    when: str
    step_id: str | None
    partition: str | None
    findings: list[ConstructionFinding]
    rule_executions: list[dict[str, Any]]
    blocking_open: int
    estimated_triples: int
    shacl: dict[str, Any] | None = None
    coverage: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "when": self.when,
            "step_id": self.step_id,
            "partition": self.partition,
            "findings": [f.to_compat_dict() for f in self.findings],
            "rule_executions": list(self.rule_executions),
            "blocking_open": self.blocking_open,
            "estimated_triples": self.estimated_triples,
            "shacl": self.shacl,
            "coverage": self.coverage,
        }
