"""Nullable / evidence-backed scorecard semantics (Round 2)."""

from __future__ import annotations

from critic.models import CriticFinding, CriticScorecard, ScoreDimension, ValidationSummary

_SEVERITY_SCORE = {"critical": 1, "high": 2, "medium": 3, "low": 4, "info": 5}


def _evaluated_rule_ids(rule_executions: list[dict] | None) -> set[str]:
    evaluated: set[str] = set()
    for execution in rule_executions or []:
        if execution.get("status") != "evaluated":
            continue
        evaluated.add(str(execution["rule_id"]))
        for rule_id in execution.get("verifies_rule_ids") or []:
            evaluated.add(str(rule_id))
    return evaluated


# CRIT-C rules that check where the source file came from (its hash, the
# provenance manifest) rather than whether the graph agrees with its text.
_PROVENANCE_RULE_PREFIXES = ("CRIT-C-SOURCE-HASH", "CRIT-C-PROVENANCE-MANIFEST")


def _is_provenance_rule(rule_id: str | None) -> bool:
    return str(rule_id or "").startswith(_PROVENANCE_RULE_PREFIXES)


def _is_provenance_finding(finding: CriticFinding) -> bool:
    return _is_provenance_rule(finding.rule_id) or _is_provenance_rule(finding.verifier_rule_id)


def _coverage_rules_evaluated(rule_executions: list[dict] | None) -> bool:
    return any(
        str(execution.get("rule_id", "")).startswith("CRIT-C-")
        and not _is_provenance_rule(execution.get("rule_id"))
        and execution.get("status") == "evaluated"
        for execution in rule_executions or []
    )


def _coverage_rules_attempted(rule_executions: list[dict] | None) -> bool:
    return any(
        str(execution.get("rule_id", "")).startswith("CRIT-C-")
        and not _is_provenance_rule(execution.get("rule_id"))
        for execution in rule_executions or []
    )


def _provenance_rules_evaluated(rule_executions: list[dict] | None) -> bool:
    return any(
        _is_provenance_rule(execution.get("rule_id"))
        and execution.get("status") == "evaluated"
        for execution in rule_executions or []
    )


def _semantic_rules_evaluated(evaluated: set[str]) -> bool:
    return any(
        rule_id.startswith("CRIT-H-") or rule_id.startswith("CRIT-G-")
        for rule_id in evaluated
    )


def _python_serializer_rules_evaluated(evaluated: set[str]) -> bool:
    return any(rule_id.startswith("CRIT-S-PY-") for rule_id in evaluated)


def build_deterministic_scorecard(
    validation: ValidationSummary,
    findings: list[CriticFinding],
    *,
    has_sources: bool,
    has_serializer: bool,
    has_coverage_contract: bool,
    rule_executions: list[dict] | None = None,
    serializer_is_python: bool | None = None,
) -> CriticScorecard:
    score = CriticScorecard()
    evaluated = _evaluated_rule_ids(rule_executions)

    # Schema/concept conformance — assessed from validation
    if validation.verification_status != "complete" or validation.conforms is not True:
        score.schema_concept_conformance = ScoreDimension(
            score=0,
            assessed=True,
            evidence=[
                f"conforms={validation.conforms}",
                f"verification_status={validation.verification_status}",
            ],
            hard_cap=0,
            cap_reason="validation_incomplete_or_nonconforming",
        )
        score.caps_applied.append("validation_incomplete_or_nonconforming")
    else:
        score.schema_concept_conformance = ScoreDimension(
            score=5,
            assessed=True,
            evidence=["validation_complete_conforming"],
        )

    # Source fidelity — only when CRIT-C-* rules that compare the graph with
    # source content evaluated (a matching hash is provenance, not fidelity)
    if has_sources or has_coverage_contract:
        src_findings = [
            f for f in findings
            if f.category in {"source_fidelity", "coverage"} and not _is_provenance_finding(f)
        ]
        if _coverage_rules_evaluated(rule_executions):
            if src_findings:
                score.source_fidelity = ScoreDimension(
                    score=2,
                    assessed=True,
                    evidence=[f.finding_id for f in src_findings[:5]],
                    hard_cap=2,
                    cap_reason="source_or_coverage_findings",
                )
            else:
                score.source_fidelity = ScoreDimension(
                    score=4,
                    assessed=True,
                    evidence=["no_source_coverage_findings"],
                )
            score.coverage_completeness = score.source_fidelity
        elif _coverage_rules_attempted(rule_executions):
            score.source_fidelity = ScoreDimension(assessed=False)
            score.coverage_completeness = ScoreDimension(assessed=False)
        else:
            score.source_fidelity = ScoreDimension(assessed=False)
            score.coverage_completeness = ScoreDimension(assessed=False)
    else:
        score.source_fidelity = ScoreDimension(assessed=False)
        score.coverage_completeness = ScoreDimension(assessed=False)

    # Semantic precision — only when heuristic semantic rules completed
    semantic_cats = {
        "relationship_direction",
        "action_grammar",
        "investigation_structure",
        "facet_placement",
        "generic_relationship",
        "dictionary_collision",
        "identity_conflation",
    }
    semantic = [f for f in findings if f.category in semantic_cats]
    if _semantic_rules_evaluated(evaluated):
        if semantic:
            worst = min(_SEVERITY_SCORE[f.severity] for f in semantic)
            score.semantic_precision = ScoreDimension(
                score=worst,
                assessed=True,
                evidence=[f.finding_id for f in semantic[:5]],
                hard_cap=worst,
                cap_reason="semantic_modeling_findings",
            )
        else:
            score.semantic_precision = ScoreDimension(
                score=4,
                assessed=True,
                evidence=["no_semantic_heuristic_findings"],
            )
    else:
        score.semantic_precision = ScoreDimension(assessed=False)

    # Markings / authorization
    auth = [f for f in findings if f.category in {"authorization", "markings"}]
    if auth:
        score.markings_authorization = ScoreDimension(
            score=2,
            assessed=True,
            evidence=[f.finding_id for f in auth[:5]],
            hard_cap=2,
            cap_reason="authorization_or_marking_findings",
        )
    else:
        score.markings_authorization = ScoreDimension(assessed=False)

    # Provenance / custody
    prov = [
        f for f in findings
        if f.category in {"provenance", "custody"} or _is_provenance_finding(f)
    ]
    if prov:
        score.provenance_custody = ScoreDimension(
            score=2,
            assessed=True,
            evidence=[f.finding_id for f in prov[:5]],
            hard_cap=2,
            cap_reason="provenance_or_custody_findings",
        )
    elif _provenance_rules_evaluated(rule_executions):
        score.provenance_custody = ScoreDimension(
            score=4,
            assessed=True,
            evidence=["source_hash_or_manifest_verified"],
        )
    else:
        score.provenance_custody = ScoreDimension(assessed=False)

    # Serializer quality — only when Python serializer rules evaluated
    if has_serializer and serializer_is_python is False:
        score.serializer_quality = ScoreDimension(assessed=False)
        score.maintainability_reproducibility = ScoreDimension(assessed=False)
    elif _python_serializer_rules_evaluated(evaluated):
        ser = [f for f in findings if f.category.startswith("serializer_")]
        if any(f.category == "serializer_validation" for f in ser):
            score.serializer_quality = ScoreDimension(
                score=1,
                assessed=True,
                evidence=[f.finding_id for f in ser[:5]],
                hard_cap=1,
                cap_reason="serializer_validation_findings",
            )
        elif ser:
            score.serializer_quality = ScoreDimension(
                score=2,
                assessed=True,
                evidence=[f.finding_id for f in ser[:5]],
                hard_cap=2,
                cap_reason="serializer_findings",
            )
        else:
            score.serializer_quality = ScoreDimension(
                score=4,
                assessed=True,
                evidence=["no_serializer_findings"],
            )
        score.maintainability_reproducibility = ScoreDimension(
            score=3 if ser else 4,
            assessed=True,
            evidence=["serializer_present"],
        )
    elif has_serializer:
        score.serializer_quality = ScoreDimension(assessed=False)
        score.maintainability_reproducibility = ScoreDimension(assessed=False)
    else:
        score.serializer_quality = ScoreDimension(assessed=False)
        score.maintainability_reproducibility = ScoreDimension(assessed=False)

    return score


def merge_scorecards(
    deterministic: CriticScorecard,
    model: CriticScorecard | None,
) -> CriticScorecard:
    """Apply model scores only where assessed; never exceed deterministic hard caps."""

    if model is None:
        return deterministic

    def merge_dim(det: ScoreDimension, mod: ScoreDimension) -> ScoreDimension:
        if not mod.assessed or mod.score is None:
            return det
        if not det.assessed:
            # Model may assess; still honor det hard_cap if any
            score = mod.score
            if det.hard_cap is not None:
                score = min(score, det.hard_cap)
            return ScoreDimension(
                score=score,
                assessed=True,
                evidence=list(mod.evidence),
                hard_cap=det.hard_cap,
                cap_reason=det.cap_reason,
            )
        score = mod.score
        if det.hard_cap is not None:
            score = min(score, det.hard_cap)
        return ScoreDimension(
            score=score,
            assessed=True,
            evidence=list(dict.fromkeys(det.evidence + mod.evidence)),
            hard_cap=det.hard_cap,
            cap_reason=det.cap_reason,
        )

    return CriticScorecard(
        schema_concept_conformance=merge_dim(
            deterministic.schema_concept_conformance, model.schema_concept_conformance
        ),
        source_fidelity=merge_dim(deterministic.source_fidelity, model.source_fidelity),
        semantic_precision=merge_dim(
            deterministic.semantic_precision, model.semantic_precision
        ),
        provenance_custody=merge_dim(
            deterministic.provenance_custody, model.provenance_custody
        ),
        markings_authorization=merge_dim(
            deterministic.markings_authorization, model.markings_authorization
        ),
        coverage_completeness=merge_dim(
            deterministic.coverage_completeness, model.coverage_completeness
        ),
        serializer_quality=merge_dim(
            deterministic.serializer_quality, model.serializer_quality
        ),
        maintainability_reproducibility=merge_dim(
            deterministic.maintainability_reproducibility,
            model.maintainability_reproducibility,
        ),
        caps_applied=list(
            dict.fromkeys(deterministic.caps_applied + ["model_scores_merged"])
        ),
    )
