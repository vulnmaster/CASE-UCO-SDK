"""Repair hint resolution for construction findings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from case_uco.contracts.profile import RepairHint

RepairKind = Literal["call_helper", "call_builder", "advance_workflow", "human"]


@dataclass(frozen=True)
class RepairAction:
    kind: RepairKind
    target: str | None
    kwargs_template: dict[str, Any]
    note: str


def suggest_repair(finding: dict[str, Any] | Any) -> RepairAction:
    """Turn a finding (dict or ConstructionFinding) into a guide-only RepairAction."""
    if hasattr(finding, "to_compat_dict"):
        payload = finding.to_compat_dict()
    elif isinstance(finding, dict):
        payload = finding
    else:
        payload = {}
    repair = payload.get("repair") or {}
    if isinstance(repair, RepairHint):
        repair = repair.as_dict()
    helper = repair.get("helper")
    builder = repair.get("builder_method")
    step = repair.get("workflow_step")
    hint = repair.get("hint") or payload.get("recommended_change") or payload.get("message") or ""
    if helper:
        return RepairAction("call_helper", helper, {}, hint)
    if builder:
        return RepairAction("call_builder", builder, {}, hint)
    if step:
        return RepairAction("advance_workflow", step, {}, hint)
    return RepairAction("human", None, {}, hint)
