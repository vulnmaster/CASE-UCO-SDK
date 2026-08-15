"""Load and synthesize ProfileContract from Composition Profiles."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from case_uco.topology.paths import contract_dirs
from case_uco.topology.profiles import CompositionProfile, get_profile

CheckWhen = Literal["incremental", "step", "graph"]
Severity = Literal["critical", "high", "medium", "low", "info"]


@dataclass(frozen=True)
class RepairHint:
    helper: str | None = None
    builder_method: str | None = None
    workflow_step: str | None = None
    hint: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "helper": self.helper,
            "builder_method": self.builder_method,
            "workflow_step": self.workflow_step,
            "hint": self.hint,
        }


@dataclass(frozen=True)
class ContractCheck:
    id: str
    when: CheckWhen
    severity: Severity
    blocking: bool
    applies_to: tuple[str, ...]
    kind: str
    params: dict[str, Any] = field(default_factory=dict)
    repair: RepairHint = field(default_factory=RepairHint)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "when": self.when,
            "severity": self.severity,
            "blocking": self.blocking,
            "applies_to": list(self.applies_to),
            "kind": self.kind,
            "params": dict(self.params),
            "repair": self.repair.as_dict(),
        }


@dataclass(frozen=True)
class ProfileContract:
    profile_id: str
    profile_version: str
    contract_schema_version: str
    checks: tuple[ContractCheck, ...]
    default_validation: dict[str, Any]
    partition_policy: dict[str, Any]
    workflows: tuple[str, ...] = ()
    trajectories: tuple[str, ...] = ()
    adapters: tuple[str, ...] = ()
    source_profile: CompositionProfile | None = None

    def checks_for(self, when: str) -> list[ContractCheck]:
        if when == "graph":
            return list(self.checks)
        if when == "step":
            return [c for c in self.checks if c.when in {"incremental", "step"}]
        return [c for c in self.checks if c.when == "incremental"]


def _parse_repair(raw: dict[str, Any] | None) -> RepairHint:
    raw = raw or {}
    return RepairHint(
        helper=raw.get("helper"),
        builder_method=raw.get("builder_method"),
        workflow_step=raw.get("workflow_step"),
        hint=raw.get("hint") or "",
    )


def _parse_check(raw: dict[str, Any]) -> ContractCheck:
    return ContractCheck(
        id=raw["id"],
        when=raw.get("when") or "graph",
        severity=raw.get("severity") or "high",
        blocking=bool(raw.get("blocking", True)),
        applies_to=tuple(raw.get("applies_to") or ["*"]),
        kind=raw["kind"],
        params=dict(raw.get("params") or {}),
        repair=_parse_repair(raw.get("repair") if isinstance(raw.get("repair"), dict) else None),
    )


@lru_cache(maxsize=1)
def _load_bindings() -> dict[str, Any]:
    for directory in contract_dirs():
        path = directory / "default-bindings.json"
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    return {"schema_version": "1.0.0", "all_profiles": [], "by_profile": {}}


def clear_contract_cache() -> None:
    _load_bindings.cache_clear()


def _overlay_checks(
    base: list[dict[str, Any]], extra: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {item["id"]: item for item in base}
    for item in extra:
        by_id[item["id"]] = item
    return list(by_id.values())


def _facet_required_check(profile: CompositionProfile) -> dict[str, Any]:
    hosts = [fs.host for fs in profile.facet_sets if fs.required]
    return {
        "id": "PROF-FACET-001",
        "when": "incremental",
        "severity": "high",
        "blocking": True,
        "applies_to": hosts or ["File", "ObservableObject", "RasterPicture"],
        "kind": "required_facets",
        "params": {},
        "repair": {
            "helper": "file_with_content_hashes",
            "builder_method": "add_file",
            "hint": "Attach the profile's required Facets for this host.",
        },
    }


def load_contract(profile_id: str) -> ProfileContract:
    """Load a ProfileContract, synthesizing from v1 facet_sets + default-bindings."""
    profile = get_profile(profile_id)
    if profile is None:
        raise ValueError(f"Unknown composition profile: {profile_id}")
    bindings = _load_bindings()
    checks_raw = list(bindings.get("all_profiles") or [])
    by_profile = (bindings.get("by_profile") or {}).get(profile.id) or []
    checks_raw = _overlay_checks(checks_raw, list(by_profile))

    authored = getattr(profile, "contract", None) or {}
    if authored.get("checks"):
        checks_raw = _overlay_checks(checks_raw, list(authored["checks"]))

    if not any(c.get("kind") == "required_facets" for c in checks_raw):
        checks_raw.append(_facet_required_check(profile))

    validation = dict((bindings.get("default_validation") or {}).get(profile.id) or {})
    if authored.get("default_validation"):
        validation.update(authored["default_validation"])

    partition = dict((bindings.get("partition_policy") or {}).get(profile.id)
                     or (bindings.get("partition_policy") or {}).get("*")
                     or {})
    if authored.get("partition_policy"):
        partition.update(authored["partition_policy"])

    return ProfileContract(
        profile_id=profile.id,
        profile_version=profile.version,
        contract_schema_version=str(authored.get("schema_version") or bindings.get("schema_version") or "1.0.0"),
        checks=tuple(_parse_check(c) for c in checks_raw),
        default_validation=validation,
        partition_policy=partition,
        workflows=tuple(authored.get("workflows") or []),
        trajectories=tuple(authored.get("trajectories") or []),
        adapters=tuple(authored.get("adapters") or []),
        source_profile=profile,
    )
