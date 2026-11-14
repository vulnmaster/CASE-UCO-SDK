"""Schema validation and normalization of critic model responses (Round 4)."""

from __future__ import annotations

import json
import math
import re
from typing import Any

from jsonschema import Draft202012Validator

from critic.models import (
    CriticFinding,
    CriticScorecard,
    CriticTarget,
    ScoreDimension,
    load_vocabularies,
    make_stable_finding_id,
)
from critic.schema_util import (
    SUPPORTED_SCHEMA_VERSION,
    bound_model_response_schema,
    model_response_schema,
)

HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
ALLOWED_ASSESSMENTS = frozenset({"persists", "resolved", "disputed"})
DETERMINISTIC_EVIDENCE = frozenset({"deterministic", "source"})


class CriticResponseError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def parse_critic_model_response(
    payload: dict[str, Any] | str,
    *,
    expected_graph_sha256: str,
    expected_prompt_package_hash: str,
    expected_serializer_sha256: str | None = None,
    session_id: str | None = None,
    pass_number: int | None = None,
    expected_review_request_sha256: str | None = None,
    expected_review_config_sha256: str | None = None,
    bound_schema: dict[str, Any] | None = None,
    allowed_assessments: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate and normalize a model/manual critic response against JSON Schema.

    Returns findings (new only), finding_assessments, and scorecard. Lifecycle
    changes are applied by the session merger — not by inventing finding IDs
    from ``assesses_finding_id``.
    """

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise CriticResponseError("critic_response_invalid", str(exc)) from exc

    if not isinstance(payload, dict):
        raise CriticResponseError("critic_response_invalid", "root must be object")

    # Reject legacy finding-ID hijack field if still present on finding items.
    for item in payload.get("findings") or []:
        if isinstance(item, dict) and "assesses_finding_id" in item:
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "assesses_finding_id belongs in finding_assessments, not findings",
            )
        if isinstance(item, dict) and item.get("finding_id"):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "model must not supply finding_id",
            )

    schema = bound_schema or bound_model_response_schema(
        graph_sha256=expected_graph_sha256,
        prompt_package_hash=expected_prompt_package_hash,
        serializer_sha256=expected_serializer_sha256,
        session_id=session_id,
        pass_number=pass_number,
        schema_version=SUPPORTED_SCHEMA_VERSION,
        review_request_sha256=expected_review_request_sha256,
        review_config_sha256=expected_review_config_sha256,
    )
    if "$schema" not in schema:
        base = model_response_schema()
        base_props = dict(base.get("properties") or {})
        base_props.update(schema.get("properties") or {})
        schema = {**base, **schema, "properties": base_props}

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        # Report every missing top-level field at once, not one per round trip.
        missing = [
            e.message for e in errors if e.validator == "required" and not e.path
        ]
        raise CriticResponseError(
            "critic_response_schema_mismatch",
            "; ".join(missing) if missing else errors[0].message,
        )

    if payload.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise CriticResponseError(
            "critic_response_schema_mismatch",
            f"unsupported schema_version {payload.get('schema_version')!r}",
        )

    for field in ("graph_sha256", "prompt_package_hash"):
        value = payload.get(field)
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            raise CriticResponseError(
                "critic_response_schema_mismatch", f"bad hex hash: {field}"
            )

    if payload["graph_sha256"] != expected_graph_sha256:
        raise CriticResponseError("critic_artifact_hash_mismatch", "graph_sha256")
    if payload["prompt_package_hash"] != expected_prompt_package_hash:
        raise CriticResponseError("critic_artifact_hash_mismatch", "prompt_package_hash")

    ser = payload.get("serializer_sha256")
    if expected_serializer_sha256 is None:
        if ser is not None:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "unexpected_serializer_sha256"
            )
    else:
        if ser != expected_serializer_sha256:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "serializer_sha256"
            )
        if not isinstance(ser, str) or not HEX64.fullmatch(ser):
            raise CriticResponseError(
                "critic_response_schema_mismatch", "bad hex hash: serializer_sha256"
            )

    got_session = payload.get("session_id")
    if session_id is None:
        if got_session is not None:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "unexpected_session_id"
            )
    elif got_session != session_id:
        raise CriticResponseError("critic_artifact_hash_mismatch", "session_id")

    got_pass = payload.get("pass_number")
    if pass_number is None:
        if got_pass is not None:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "unexpected_pass_number"
            )
    elif got_pass != pass_number:
        raise CriticResponseError("critic_artifact_hash_mismatch", "pass_number")

    got_req = payload.get("review_request_sha256")
    if expected_review_request_sha256 is not None:
        if got_req != expected_review_request_sha256:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "review_request_sha256"
            )
        if not isinstance(got_req, str) or not HEX64.fullmatch(got_req):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "bad hex hash: review_request_sha256",
            )
    elif got_req is not None:
        if not isinstance(got_req, str) or not HEX64.fullmatch(got_req):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "bad hex hash: review_request_sha256",
            )

    got_cfg = payload.get("review_config_sha256")
    if expected_review_config_sha256 is not None:
        if got_cfg != expected_review_config_sha256:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "review_config_sha256"
            )
        if not isinstance(got_cfg, str) or not HEX64.fullmatch(got_cfg):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "bad hex hash: review_config_sha256",
            )
    elif got_cfg is not None:
        if not isinstance(got_cfg, str) or not HEX64.fullmatch(got_cfg):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "bad hex hash: review_config_sha256",
            )

    vocab = load_vocabularies()
    categories = set(vocab["categories"])

    findings: list[CriticFinding] = []
    for item in payload["findings"]:
        category = item["category"]
        if category not in categories:
            raise CriticResponseError(
                "critic_response_schema_mismatch", f"bad category {category}"
            )
        if item.get("rule_id"):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "model must not supply rule_id",
            )
        if item.get("evidence_kind") and item["evidence_kind"] != "critic_inference":
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "model evidence_kind must be critic_inference",
            )

        claim_type = str(item.get("claim_type") or "").strip()
        if not claim_type:
            raise CriticResponseError(
                "critic_response_schema_mismatch", "claim_type required"
            )

        target_raw = item["target"]
        target = CriticTarget(
            path=target_raw.get("path"),
            line=target_raw.get("line"),
            node_id=target_raw.get("node_id"),
            predicate=target_raw.get("predicate"),
            counterpart_id=target_raw.get("counterpart_id"),
            json_pointer=target_raw.get("json_pointer"),
            qualified_name=target_raw.get("qualified_name"),
        )
        if not any(
            [
                target.path,
                target.node_id,
                target.predicate,
                target.json_pointer,
                target.qualified_name,
            ]
        ):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "target must identify a location",
            )

        finding_id = make_stable_finding_id(
            f"MODEL-{category}",
            *target.semantic_parts(),
            claim_type,
        )
        findings.append(
            CriticFinding(
                finding_id=finding_id,
                severity=item["severity"],
                category=category,
                confidence=_finite(item["confidence"], "confidence"),
                status="new",
                target=target,
                evidence_kind="critic_inference",
                evidence=[str(e) for e in item["evidence"]],
                rationale=str(item["rationale"]),
                recommended_change=str(item["recommended_change"]),
                verification_method=str(item["verification_method"]),
                related_recipe=item.get("related_recipe"),
                claim_type=claim_type,
                identity_key=finding_id,
            )
        )

    assessments = _parse_assessments(
        payload.get("finding_assessments") or [],
        allowed_assessments=allowed_assessments,
    )

    scorecard = _parse_scorecard(payload.get("scorecard") or {})
    return {
        "findings": findings,
        "finding_assessments": assessments,
        "scorecard": scorecard,
        "notes": str(payload.get("notes") or ""),
        "session_id": payload.get("session_id", session_id),
        "pass_number": payload.get("pass_number", pass_number),
        "review_request_sha256": payload.get("review_request_sha256"),
        "review_config_sha256": payload.get("review_config_sha256"),
    }


def _parse_assessments(
    raw_items: list[Any],
    *,
    allowed_assessments: dict[str, dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    assessments: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw_items:
        if not isinstance(item, dict):
            raise CriticResponseError(
                "critic_response_schema_mismatch", "assessment must be object"
            )
        assesses = str(item.get("assesses_finding_id") or "").strip()
        if not assesses:
            raise CriticResponseError(
                "critic_response_schema_mismatch", "assesses_finding_id required"
            )
        if assesses in seen:
            raise CriticResponseError(
                "critic_response_duplicate_assessment", assesses
            )
        seen.add(assesses)
        assessment = str(item.get("assessment") or "").strip()
        if assessment not in ALLOWED_ASSESSMENTS:
            raise CriticResponseError(
                "critic_response_schema_mismatch", f"bad assessment {assessment}"
            )
        ledger = (allowed_assessments or {}).get(assesses)
        if allowed_assessments is not None:
            if ledger is None:
                raise CriticResponseError(
                    "critic_assessment_unknown_finding", assesses
                )
            evidence_kind = str(ledger.get("evidence_kind") or "")
            allowed = set(ledger.get("allowed_assessments") or [])
            # Deterministic/source findings may be disputed but never model-resolved.
            if evidence_kind in DETERMINISTIC_EVIDENCE and assessment == "resolved":
                raise CriticResponseError(
                    "critic_assessment_deterministic_resolve_forbidden",
                    assesses,
                )
            if assessment not in allowed:
                raise CriticResponseError(
                    "critic_assessment_not_permitted",
                    f"{assesses}:{assessment}",
                )
        assessment_id = item.get("assessment_id")
        if assessment_id is None:
            assessment_id = make_stable_finding_id("ASSESS", assesses, assessment)
        assessments.append(
            {
                "assessment_id": str(assessment_id),
                "assesses_finding_id": assesses,
                "assessment": assessment,
                "evidence": [str(e) for e in (item.get("evidence") or [])],
                "verification_method": str(item.get("verification_method") or ""),
                "rationale": str(item.get("rationale") or ""),
            }
        )
    return assessments


def build_assessment_ledger(
    findings: list[CriticFinding] | list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build the allowed-assessment ledger for the current pass."""

    ledger: dict[str, dict[str, Any]] = {}
    for raw in findings:
        finding = (
            raw
            if isinstance(raw, CriticFinding)
            else CriticFinding.from_dict(raw)
        )
        if finding.status == "resolved":
            continue
        evidence_kind = finding.evidence_kind
        if evidence_kind in DETERMINISTIC_EVIDENCE:
            allowed = ["persists", "disputed"]
        else:
            allowed = ["persists", "resolved", "disputed"]
        ledger[finding.finding_id] = {
            "evidence_kind": evidence_kind,
            "target": {
                "path": finding.target.path,
                "line": finding.target.line,
                "node_id": finding.target.node_id,
                "predicate": finding.target.predicate,
                "counterpart_id": finding.target.counterpart_id,
                "json_pointer": finding.target.json_pointer,
                "qualified_name": finding.target.qualified_name,
            },
            "allowed_assessments": allowed,
            "severity": finding.severity,
            "status": finding.status,
        }
    return ledger


def _finite(value: Any, field_name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise CriticResponseError(
            "critic_response_schema_mismatch", f"{field_name} is not a number"
        ) from exc
    if not math.isfinite(number):
        raise CriticResponseError(
            "critic_response_non_finite_number", f"{field_name} is not finite"
        )
    return number


def _parse_scorecard(raw: dict[str, Any]) -> CriticScorecard:
    def dim(key: str) -> ScoreDimension:
        value = raw.get(key)
        if value is None:
            return ScoreDimension(assessed=False)
        if isinstance(value, int):
            return ScoreDimension(score=max(0, min(5, value)), assessed=True)
        if isinstance(value, dict):
            score = value.get("score")
            if score is None:
                return ScoreDimension(
                    assessed=bool(value.get("assessed", False)),
                    evidence=list(value.get("evidence") or []),
                    hard_cap=value.get("hard_cap"),
                    cap_reason=value.get("cap_reason"),
                )
            hard_cap = value.get("hard_cap")
            if hard_cap is not None:
                _finite(hard_cap, f"scorecard.{key}.hard_cap")
            return ScoreDimension(
                score=max(0, min(5, int(_finite(score, f"scorecard.{key}.score")))),
                assessed=True,
                evidence=list(value.get("evidence") or []),
                hard_cap=value.get("hard_cap"),
                cap_reason=value.get("cap_reason"),
            )
        raise CriticResponseError(
            "critic_response_schema_mismatch", f"bad scorecard.{key}"
        )

    return CriticScorecard(
        schema_concept_conformance=dim("schema_concept_conformance"),
        source_fidelity=dim("source_fidelity"),
        semantic_precision=dim("semantic_precision"),
        provenance_custody=dim("provenance_custody"),
        markings_authorization=dim("markings_authorization"),
        coverage_completeness=dim("coverage_completeness"),
        serializer_quality=dim("serializer_quality"),
        maintainability_reproducibility=dim("maintainability_reproducibility"),
    )


def load_review_schema() -> dict[str, Any]:
    from critic.review_schema import _load_review_schema

    return _load_review_schema()
