"""Typed critic review contracts (issue #75 Round 2)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

CRITIC_SCHEMA_VERSION = "1.2.0"

Severity = Literal["critical", "high", "medium", "low", "info"]
FindingStatus = Literal["new", "persisting", "resolved", "regression", "disputed", "unevaluated"]
EvidenceKind = Literal["deterministic", "source", "critic_inference"]
CriticScope = Literal["graph", "serializer", "both"]
HandoffType = Literal[
    "recipe_improvement",
    "routing_gap",
    "new_recipe_candidate",
    "ontology_gap",
    "extension_gap",
    "sdk_bug",
]

VOCAB_PATH = Path(__file__).resolve().parent / "vocabularies.json"


def load_vocabularies() -> dict[str, Any]:
    return json.loads(VOCAB_PATH.read_text(encoding="utf-8"))


def make_stable_finding_id(rule_id: str, *semantic_parts: str) -> str:
    """Public stable finding ID from rule + normalized semantic target parts."""

    normalized = [rule_id.strip()]
    for part in semantic_parts:
        text = (part or "").strip()
        if text:
            normalized.append(text)
    digest = hashlib.sha256("|".join(normalized).encode("utf-8")).hexdigest()[:16]
    return f"CRIT-{digest}"


@dataclass
class CriticTarget:
    path: str | None = None
    line: int | None = None
    node_id: str | None = None
    predicate: str | None = None
    counterpart_id: str | None = None
    json_pointer: str | None = None
    qualified_name: str | None = None  # serializer class/function

    def semantic_parts(self) -> list[str]:
        # Graph findings: node + predicate + counterpart (not line/path/pointer).
        # Serializer findings: path + qualified_name (not line).
        if self.node_id or self.predicate or self.counterpart_id:
            return [
                p
                for p in (self.node_id, self.predicate, self.counterpart_id)
                if p
            ]
        return [p for p in (self.path, self.qualified_name) if p]


@dataclass
class CriticFinding:
    finding_id: str
    severity: Severity
    category: str
    confidence: float
    status: FindingStatus
    target: CriticTarget
    evidence_kind: EvidenceKind
    evidence: list[str]
    rationale: str
    recommended_change: str
    verification_method: str
    rule_id: str | None = None
    verifier_rule_id: str | None = None
    rule_version: str | None = None
    claim_type: str | None = None
    assesses_finding_id: str | None = None
    related_recipe: str | None = None
    related_validation_result: str | None = None
    identity_key: str | None = None
    suppressible: bool = True
    disputed_rationale: str | None = None
    display_index: int | None = None
    occurrence: dict[str, Any] = field(default_factory=dict)

    def ensure_identity_key(self) -> str:
        if self.finding_id and self.finding_id.startswith("CRIT-"):
            self.identity_key = self.finding_id
            return self.finding_id
        if self.identity_key and self.identity_key.startswith("CRIT-"):
            self.finding_id = self.identity_key
            return self.finding_id
        if self.rule_id:
            self.finding_id = make_stable_finding_id(
                self.rule_id, *self.target.semantic_parts()
            )
            self.identity_key = self.finding_id
            return self.finding_id
        # Fallback without calling to_dict() (would recurse).
        digest = hashlib.sha256(
            "|".join(
                [
                    self.category,
                    self.evidence_kind,
                    *self.target.semantic_parts(),
                    self.claim_type or "",
                    "|".join(self.evidence[:3]),
                ]
            ).encode("utf-8")
        ).hexdigest()[:16]
        self.finding_id = f"CRIT-{digest}"
        self.identity_key = self.finding_id
        return self.finding_id

    def to_dict(self) -> dict[str, Any]:
        self.ensure_identity_key()
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CriticFinding:
        target_raw = data.get("target") or {}
        target = CriticTarget(
            path=target_raw.get("path"),
            line=target_raw.get("line"),
            node_id=target_raw.get("node_id"),
            predicate=target_raw.get("predicate"),
            counterpart_id=target_raw.get("counterpart_id"),
            json_pointer=target_raw.get("json_pointer"),
            qualified_name=target_raw.get("qualified_name"),
        )
        finding = cls(
            finding_id=str(data.get("finding_id") or ""),
            severity=data["severity"],
            category=str(data["category"]),
            confidence=float(data["confidence"]),
            status=data.get("status", "new"),
            target=target,
            evidence_kind=data["evidence_kind"],
            evidence=list(data.get("evidence") or []),
            rationale=str(data.get("rationale") or ""),
            recommended_change=str(data.get("recommended_change") or ""),
            verification_method=str(data.get("verification_method") or ""),
            rule_id=data.get("rule_id"),
            verifier_rule_id=data.get("verifier_rule_id"),
            rule_version=data.get("rule_version"),
            claim_type=data.get("claim_type"),
            assesses_finding_id=data.get("assesses_finding_id"),
            related_recipe=data.get("related_recipe"),
            related_validation_result=data.get("related_validation_result"),
            identity_key=data.get("identity_key"),
            suppressible=bool(data.get("suppressible", True)),
            disputed_rationale=data.get("disputed_rationale"),
            display_index=data.get("display_index"),
            occurrence=dict(data.get("occurrence") or {}),
        )
        finding.ensure_identity_key()
        return finding


@dataclass
class ScoreDimension:
    score: int | None = None
    assessed: bool = False
    evidence: list[str] = field(default_factory=list)
    hard_cap: int | None = None
    cap_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ScoreDimension:
        if not data:
            return cls()
        if isinstance(data, int):
            return cls(score=data, assessed=True)
        return cls(
            score=data.get("score"),
            assessed=bool(data.get("assessed", data.get("score") is not None)),
            evidence=list(data.get("evidence") or []),
            hard_cap=data.get("hard_cap"),
            cap_reason=data.get("cap_reason"),
        )


@dataclass
class CriticScorecard:
    schema_concept_conformance: ScoreDimension = field(default_factory=ScoreDimension)
    source_fidelity: ScoreDimension = field(default_factory=ScoreDimension)
    semantic_precision: ScoreDimension = field(default_factory=ScoreDimension)
    provenance_custody: ScoreDimension = field(default_factory=ScoreDimension)
    markings_authorization: ScoreDimension = field(default_factory=ScoreDimension)
    coverage_completeness: ScoreDimension = field(default_factory=ScoreDimension)
    serializer_quality: ScoreDimension = field(default_factory=ScoreDimension)
    maintainability_reproducibility: ScoreDimension = field(
        default_factory=ScoreDimension
    )
    caps_applied: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_concept_conformance": self.schema_concept_conformance.to_dict(),
            "source_fidelity": self.source_fidelity.to_dict(),
            "semantic_precision": self.semantic_precision.to_dict(),
            "provenance_custody": self.provenance_custody.to_dict(),
            "markings_authorization": self.markings_authorization.to_dict(),
            "coverage_completeness": self.coverage_completeness.to_dict(),
            "serializer_quality": self.serializer_quality.to_dict(),
            "maintainability_reproducibility": (
                self.maintainability_reproducibility.to_dict()
            ),
            "caps_applied": list(self.caps_applied),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CriticScorecard:
        return cls(
            schema_concept_conformance=ScoreDimension.from_dict(
                data.get("schema_concept_conformance")
            ),
            source_fidelity=ScoreDimension.from_dict(data.get("source_fidelity")),
            semantic_precision=ScoreDimension.from_dict(data.get("semantic_precision")),
            provenance_custody=ScoreDimension.from_dict(
                data.get("provenance_custody")
            ),
            markings_authorization=ScoreDimension.from_dict(
                data.get("markings_authorization")
            ),
            coverage_completeness=ScoreDimension.from_dict(
                data.get("coverage_completeness")
            ),
            serializer_quality=ScoreDimension.from_dict(
                data.get("serializer_quality")
            ),
            maintainability_reproducibility=ScoreDimension.from_dict(
                data.get("maintainability_reproducibility")
            ),
            caps_applied=list(data.get("caps_applied") or []),
        )


@dataclass
class SelfImprovementHandoffCandidate:
    handoff_type: HandoffType
    finding_ids: list[str]
    summary: str
    recurrence_key: str
    validation_evidence: list[str] = field(default_factory=list)
    requires_operator_approval: bool = True
    suggestion_only: bool = True
    unverified_generalization: bool = True
    validation_bundle_fingerprint: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CriticArtifactRequest:
    graph_path: str
    serializer_path: str | None = None
    source_paths: list[str] = field(default_factory=list)
    coverage_contract_path: str | None = None
    provenance_manifest_path: str | None = None
    extensions: list[str] = field(default_factory=list)
    profiles: list[str] = field(default_factory=list)
    critic_scope: CriticScope = "both"
    project_root: str | None = None
    prior_findings: list[CriticFinding] = field(default_factory=list)
    disputed_identity_keys: dict[str, str] = field(default_factory=dict)
    serializer_mode: Literal["typed_sdk", "raw_fixture", "auto", "casegraph_raw"] = "auto"
    pass_number: int = 1
    session_id: str | None = None
    extra_ontology_graphs: list[str] = field(default_factory=list)
    force_rdfs_inference: bool = False


@dataclass
class ArtifactHashes:
    graph_sha256: str
    serializer_sha256: str | None = None
    source_sha256: dict[str, str] = field(default_factory=dict)
    coverage_contract_sha256: str | None = None
    provenance_manifest_sha256: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationSummary:
    conforms: bool | None
    verification_status: str
    violation_count: int = 0
    warning_count: int = 0
    bundle_fingerprint: str | None = None
    bundle_resource_hashes: dict[str, str] = field(default_factory=dict)
    selected_profiles: list[str] = field(default_factory=list)
    selected_extensions: list[str] = field(default_factory=list)
    stage_status: dict[str, str] = field(default_factory=dict)
    profile_not_selected: list[dict[str, Any]] = field(default_factory=list)
    role_mismatches: list[list[str]] = field(default_factory=list)
    relationship_lint_ok: bool | None = None
    relationship_lint_findings: list[dict[str, Any]] = field(default_factory=list)
    error_code: str | None = None
    safe_summary: str = ""
    violation_details: list[dict[str, str | None]] = field(default_factory=list)
    violation_details_truncated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CriticReview:
    schema_version: str
    artifact_hashes: ArtifactHashes
    validation: ValidationSummary
    deterministic_findings: list[CriticFinding]
    critic_findings: list[CriticFinding]
    merged_findings: list[CriticFinding]
    scorecard: CriticScorecard
    prompt_package: dict[str, Any]
    status: str
    analysis_status: str = "complete"  # complete|partial|failed
    rule_executions: list[dict[str, Any]] = field(default_factory=list)
    finding_diff: dict[str, Any] = field(default_factory=dict)
    model_identifier: str | None = None
    token_estimate: int | None = None
    elapsed_ms: int | None = None
    handoff_suggestions: list[SelfImprovementHandoffCandidate] = field(
        default_factory=list
    )
    errors: list[str] = field(default_factory=list)
    # Backward-compatible alias used by older callers/tests
    handoff_candidates: list[SelfImprovementHandoffCandidate] = field(
        default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        suggestions = self.handoff_suggestions or self.handoff_candidates
        return {
            "schema_version": self.schema_version,
            "artifact_hashes": self.artifact_hashes.to_dict(),
            "validation": self.validation.to_dict(),
            "deterministic_findings": [f.to_dict() for f in self.deterministic_findings],
            "critic_findings": [f.to_dict() for f in self.critic_findings],
            "merged_findings": [f.to_dict() for f in self.merged_findings],
            "scorecard": self.scorecard.to_dict(),
            "prompt_package": self.prompt_package,
            "status": self.status,
            "analysis_status": self.analysis_status,
            "rule_executions": list(self.rule_executions),
            "finding_diff": dict(self.finding_diff),
            "model_identifier": self.model_identifier,
            "token_estimate": self.token_estimate,
            "elapsed_ms": self.elapsed_ms,
            "handoff_suggestions": [h.to_dict() for h in suggestions],
            "errors": list(self.errors),
        }
