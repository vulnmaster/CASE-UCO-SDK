"""SHACL + concept-coverage signals. Never fabricate conforms=True."""

from __future__ import annotations

from typing import Any

from case_uco.contracts.profile import ProfileContract
from case_uco.critique.findings import ConstructionFinding


def evaluate_validation_signals(
    graph: Any,
    contract: ProfileContract,
) -> tuple[list[ConstructionFinding], dict[str, Any] | None, dict[str, Any] | None, list[dict[str, Any]]]:
    findings: list[ConstructionFinding] = []
    executions: list[dict[str, Any]] = []
    shacl: dict[str, Any] | None = None
    coverage: dict[str, Any] | None = None

    try:
        from case_uco.validation.graph import validator_available
    except Exception:  # noqa: BLE001
        validator_available = lambda: False  # noqa: E731

    wants_shacl = any(c.kind == "shacl_signal" for c in contract.checks)
    wants_cov = any(c.kind == "concept_coverage_signal" for c in contract.checks)
    if not wants_shacl and not wants_cov:
        return findings, None, None, executions

    if not validator_available():
        executions.append(
            {
                "rule_id": "PROF-SHACL-001",
                "status": "skipped",
                "error_code": "validator_unavailable",
            }
        )
        if wants_cov:
            executions.append(
                {
                    "rule_id": "PROF-COV-001",
                    "status": "skipped",
                    "error_code": "validator_unavailable",
                }
            )
        shacl = {"available": False, "conforms": None, "error_code": "validator_unavailable"}
        return findings, shacl, coverage, executions

    validation = contract.default_validation or {}
    try:
        report = graph.validate_report(
            extensions=list(validation.get("extensions") or []),
            profiles=list(validation.get("profiles") or []),
            strict_concepts=bool(validation.get("strict_concepts", True)),
        )
    except ValueError as exc:
        text = str(exc)
        code = "validator_unavailable" if "validator_unavailable" in text else "validation_error"
        executions.append({"rule_id": "PROF-SHACL-001", "status": "skipped", "error_code": code})
        shacl = {"available": False, "conforms": None, "error_code": code}
        return findings, shacl, coverage, executions
    except Exception as exc:  # noqa: BLE001
        executions.append(
            {"rule_id": "PROF-SHACL-001", "status": "failed", "error_code": type(exc).__name__}
        )
        shacl = {"available": False, "conforms": None, "error_code": type(exc).__name__}
        return findings, shacl, coverage, executions

    shacl = {
        "available": True,
        "conforms": report.conforms,
        "violation_count": getattr(report, "violation_count", 0),
        "warning_count": getattr(report, "warning_count", 0),
    }
    coverage = {
        "undeclared_concepts": list(getattr(report, "undeclared_concepts", ()) or ()),
        "role_mismatches": list(getattr(report, "role_mismatches", ()) or ()),
        "profile_not_selected": list(getattr(report, "profile_not_selected", ()) or ()),
    }
    executions.append({"rule_id": "PROF-SHACL-001", "status": "evaluated"})
    executions.append({"rule_id": "PROF-COV-001", "status": "evaluated"})

    if report.conforms is False:
        findings.append(
            ConstructionFinding(
                rule_id="PROF-SHACL-001",
                severity="error",
                message=f"SHACL non-conformant ({shacl['violation_count']} violations)",
                blocking=True,
                profile_id=contract.profile_id,
                category="shacl",
                when="graph",
                evidence=[str(shacl["violation_count"])],
                repair={"hint": "Fix SHACL violations before emit."},
            )
        )
    undeclared = coverage["undeclared_concepts"]
    if undeclared:
        findings.append(
            ConstructionFinding(
                rule_id="PROF-COV-001",
                severity="error",
                message=f"Undeclared concepts: {undeclared[:8]}",
                blocking=True,
                profile_id=contract.profile_id,
                category="coverage",
                when="graph",
                evidence=[str(c) for c in undeclared[:16]],
                repair={"hint": "Use generated classes or draft a change proposal."},
            )
        )
    return findings, shacl, coverage, executions
