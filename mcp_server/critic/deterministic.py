"""Deterministic critic analysis entrypoint (issue #75 Round 4)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import graph_validator
import workspace_policy
from critic.canonical import RuleExecution, lint_kind_of_relationship
from critic.context_builder import (
    build_prompt_package,
    build_serializer_overview,
    excerpt_serializer,
)
from critic.coverage import (
    check_provenance_manifest,
    check_source_document_hash,
    compare_coverage_contract,
)
from critic.finding_diff import assign_display_indexes, diff_findings
from critic.graph_heuristics import run_graph_heuristics
from critic.graph_integrity import analyze_graph_integrity, sha256_file
from critic.models import (
    CRITIC_SCHEMA_VERSION,
    ArtifactHashes,
    CriticArtifactRequest,
    CriticFinding,
    CriticReview,
    CriticTarget,
    SelfImprovementHandoffCandidate,
    ValidationSummary,
)
from critic.review_schema import validate_critic_review
from critic.scorecard import build_deterministic_scorecard, merge_scorecards
from critic.serializer_python import SerializerTooComplexError, analyze_python_serializer

RULE_VERSION = "1.1.1"
MAX_SERIALIZER_AST_BYTES = 256 * 1024


class CriticError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def analyze_artifact(request: CriticArtifactRequest) -> CriticReview:
    started = time.perf_counter()
    errors: list[str] = []
    rule_executions: list[dict[str, Any]] = []

    try:
        graph_path = workspace_policy.check_read_path(
            request.graph_path, include_write_roots=True
        )
    except ValueError as exc:
        raise CriticError("critic_path_outside_workspace", str(exc)) from exc
    if not graph_path.is_file():
        raise CriticError("critic_graph_missing")

    serializer_path: Path | None = None
    if request.serializer_path and request.critic_scope in {"serializer", "both"}:
        try:
            serializer_path = workspace_policy.check_read_path(
                request.serializer_path, include_write_roots=True
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if not serializer_path.is_file():
            raise CriticError("critic_serializer_missing")

    source_paths: list[Path] = []
    for raw in request.source_paths:
        try:
            sp = workspace_policy.check_read_path(raw, include_write_roots=True)
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if not sp.is_file():
            raise CriticError("critic_graph_missing", f"source_missing:{sp.name}")
        source_paths.append(sp)

    coverage_path: Path | None = None
    if request.coverage_contract_path:
        try:
            coverage_path = workspace_policy.check_read_path(
                request.coverage_contract_path, include_write_roots=True
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if not coverage_path.is_file():
            raise CriticError("critic_graph_missing", "coverage_contract_missing")

    project_root = Path(__file__).resolve().parents[2]
    if request.project_root:
        candidate = Path(request.project_root).resolve()
        if candidate == project_root or project_root in candidate.parents:
            project_root = candidate

    source_aliases = _source_aliases(source_paths)
    provenance_manifest_sha256: str | None = None
    if request.provenance_manifest_path:
        try:
            early_manifest = workspace_policy.check_read_path(
                request.provenance_manifest_path, include_write_roots=True
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if early_manifest.is_file():
            provenance_manifest_sha256 = sha256_file(early_manifest)

    hashes = ArtifactHashes(
        graph_sha256=sha256_file(graph_path),
        serializer_sha256=sha256_file(serializer_path) if serializer_path else None,
        source_sha256={
            alias: sha256_file(path) for alias, path in source_aliases.items()
        },
        coverage_contract_sha256=(
            sha256_file(coverage_path) if coverage_path else None
        ),
        provenance_manifest_sha256=provenance_manifest_sha256,
    )

    findings: list[CriticFinding] = []
    view = None

    if request.critic_scope in {"graph", "both"}:
        view, integrity_findings, integrity_exec = analyze_graph_integrity(
            graph_path, artifact_hash=hashes.graph_sha256
        )
        findings.extend(integrity_findings)
        rule_executions.extend(e.to_dict() for e in integrity_exec)

        heur_findings, heur_exec = run_graph_heuristics(
            view,
            artifact_hash=hashes.graph_sha256,
            profiles=list(request.profiles or []),
        )
        findings.extend(heur_findings)
        rule_executions.extend(e.to_dict() for e in heur_exec)

        if coverage_path:
            cov_findings, cov_exec = compare_coverage_contract(
                view, coverage_path, artifact_hash=hashes.graph_sha256
            )
            findings.extend(cov_findings)
            rule_executions.extend(e.to_dict() for e in cov_exec)

        for alias, sp in source_aliases.items():
            src_findings, src_exec = check_source_document_hash(
                view,
                source_name=sp.name,
                expected_sha256=hashes.source_sha256[alias],
                artifact_hash=hashes.graph_sha256,
            )
            findings.extend(src_findings)
            rule_executions.extend(e.to_dict() for e in src_exec)

        if request.provenance_manifest_path:
            try:
                manifest_path = workspace_policy.check_read_path(
                    request.provenance_manifest_path, include_write_roots=True
                )
            except ValueError as exc:
                raise CriticError("critic_path_outside_workspace", str(exc)) from exc
            if not manifest_path.is_file():
                raise CriticError(
                    "critic_graph_missing", "provenance_manifest_missing"
                )
            man_findings, man_exec = check_provenance_manifest(
                manifest_path,
                project_root=project_root,
                artifact_hash=hashes.graph_sha256,
                graph_sha256=hashes.graph_sha256,
            )
            findings.extend(man_findings)
            rule_executions.extend(e.to_dict() for e in man_exec)

        if view and view.usable_for_heuristics:
            lint = lint_kind_of_relationship(view)
            lint_findings: list[CriticFinding] = []
            for item in lint.get("findings") or []:
                node_id = item.get("node_id")
                f = CriticFinding(
                    finding_id="",
                    severity="medium" if item.get("severity") == "warning" else "high",
                    category="relationship_vocabulary",
                    confidence=1.0,
                    status="new",
                    target=CriticTarget(
                        node_id=node_id if isinstance(node_id, str) else None,
                        predicate="uco-core:kindOfRelationship",
                    ),
                    evidence_kind="deterministic",
                    evidence=[str(item.get("kind") or "")],
                    rationale=str(item.get("message") or "relationship kind lint"),
                    recommended_change=(
                        "Use a vocabulary member or justify open-vocabulary kind."
                    ),
                    verification_method="canonical.lint_kind_of_relationship",
                    rule_id="CRIT-V-RELATIONSHIP-LINT",
                    verifier_rule_id="CRIT-V-RELATIONSHIP-LINT",
                    rule_version=RULE_VERSION,
                )
                f.ensure_identity_key()
                lint_findings.append(f)
            findings.extend(lint_findings)
            rule_executions.append(
                RuleExecution(
                    rule_id="CRIT-V-RELATIONSHIP-LINT",
                    rule_version=RULE_VERSION,
                    status="evaluated",
                    input_artifact_hash=hashes.graph_sha256,
                    targets_examined=int(lint.get("checked") or 0),
                    finding_ids=[f.finding_id for f in lint_findings],
                    required_for_scope=True,
                    verifies_rule_ids=["CRIT-V-RELATIONSHIP-LINT"],
                ).to_dict()
            )
        elif view is not None:
            rule_executions.append(
                RuleExecution(
                    rule_id="CRIT-V-RELATIONSHIP-LINT",
                    rule_version=RULE_VERSION,
                    status="skipped",
                    input_artifact_hash=hashes.graph_sha256,
                    error_code="graph_unavailable",
                    required_for_scope=True,
                    verifies_rule_ids=["CRIT-V-RELATIONSHIP-LINT"],
                ).to_dict()
            )

    validation, validation_execs = _run_validation(
        graph_path,
        extensions=request.extensions,
        profiles=request.profiles,
        project_root=project_root,
        errors=errors,
        artifact_hash=hashes.graph_sha256,
        extra_ontology_graphs=list(request.extra_ontology_graphs or []),
        force_rdfs_inference=bool(request.force_rdfs_inference),
    )
    findings.extend(_validation_findings(validation))
    rule_executions.extend(e.to_dict() for e in validation_execs)

    serializer_excerpts: list[dict[str, Any]] = []
    serializer_overview: dict[str, Any] | None = None
    serializer_is_python: bool | None = None
    if serializer_path and request.critic_scope in {"serializer", "both"}:
        serializer_is_python = serializer_path.suffix.lower() == ".py"
        too_large = serializer_is_python and (
            serializer_path.stat().st_size > MAX_SERIALIZER_AST_BYTES
        )
        raw_full = b"" if too_large else serializer_path.read_bytes()
        if too_large:
            errors.append("critic_serializer_too_large")
            rule_executions.append(
                RuleExecution(
                    rule_id="CRIT-S-PY-SUITE",
                    rule_version=RULE_VERSION,
                    status="skipped",
                    input_artifact_hash=hashes.serializer_sha256 or "",
                    error_code="critic_serializer_too_large",
                    required_for_scope=True,
                    verifies_rule_ids=[
                        "CRIT-S-PY-PRIVATE-OBJECTS",
                        "CRIT-S-PY-JSON-DUMPS-ONLY",
                        "CRIT-S-PY-FAIL-OPEN-VALIDATION",
                        "CRIT-S-PY-SWALLOWED-EXCEPTION",
                        "CRIT-S-PY-UNSCOPED-UUID5",
                        "CRIT-S-PY-GLOBAL-UUID-IDS",
                    ],
                ).to_dict()
            )
            serializer_overview = {
                "path": serializer_path.name,
                "note": "serializer_too_large_for_ast",
                "byte_size": serializer_path.stat().st_size,
            }
        elif serializer_is_python:
            source_text = raw_full.decode("utf-8", errors="replace")
            try:
                ser_findings, ser_exec = analyze_python_serializer(
                    serializer_path,
                    source_text,
                    serializer_mode=request.serializer_mode,
                    artifact_hash=hashes.serializer_sha256 or "",
                )
                serializer_excerpts = excerpt_serializer(
                    source_text, ser_findings, path_name=serializer_path.name
                )
                serializer_overview = build_serializer_overview(
                    source_text, path_name=serializer_path.name
                )
            except (SerializerTooComplexError, RecursionError):
                errors.append("critic_serializer_too_complex")
                ser_findings, ser_exec = [], [
                    RuleExecution(
                        rule_id="CRIT-S-PY-SUITE",
                        rule_version=RULE_VERSION,
                        status="skipped",
                        input_artifact_hash=hashes.serializer_sha256 or "",
                        error_code="critic_serializer_too_complex",
                        required_for_scope=True,
                    )
                ]
                serializer_excerpts = []
                serializer_overview = {
                    "path": serializer_path.name,
                    "note": "serializer_too_complex_for_ast",
                }
            findings.extend(ser_findings)
            rule_executions.extend(e.to_dict() for e in ser_exec)
        else:
            serializer_overview = {
                "path": serializer_path.name,
                "note": "non-python overview only",
            }

    # Map each verifier rule_id → concrete rule_version from RuleExecution.
    # Resolution must use per-verifier versions (heuristic 1.2.0 ≠ module 1.1.0).
    evaluated_rule_versions: dict[str, str] = {}
    blocking_incomplete = False
    for execution in rule_executions:
        rule_id = str(execution.get("rule_id", ""))
        status = execution.get("status")
        required = bool(execution.get("required_for_scope", True))
        version = str(execution.get("rule_version") or RULE_VERSION)
        verified = [str(v) for v in (execution.get("verifies_rule_ids") or [rule_id])]
        if status == "evaluated":
            for rid in {rule_id, *verified}:
                if rid:
                    evaluated_rule_versions[rid] = version
        elif status == "failed" and required:
            blocking_incomplete = True
        elif status == "skipped" and required:
            blocking_incomplete = True
        # not_applicable must not block acceptance

    def _rule_ids_for_finding(finding: CriticFinding) -> set[str]:
        return {rid for rid in (finding.verifier_rule_id, finding.rule_id) if rid}

    resolved_ids: set[str] = set()
    unevaluated_ids: set[str] = set()
    current_ids = {f.finding_id for f in findings}
    for old in request.prior_findings:
        if old.evidence_kind not in {"deterministic", "source"} or not old.rule_id:
            unevaluated_ids.add(old.finding_id)
            continue
        check_ids = _rule_ids_for_finding(old)
        if not check_ids:
            unevaluated_ids.add(old.finding_id)
            continue
        # Compatible when any verifier rule was evaluated at a matching version.
        version_ok = False
        evaluated = False
        for rid in check_ids:
            if rid not in evaluated_rule_versions:
                continue
            evaluated = True
            executed_version = evaluated_rule_versions[rid]
            if not old.rule_version or old.rule_version == executed_version:
                version_ok = True
                break
        if not evaluated or not version_ok:
            unevaluated_ids.add(old.finding_id)
            continue
        if old.finding_id not in current_ids:
            resolved_ids.add(old.finding_id)

    diff = diff_findings(
        list(request.prior_findings),
        findings,
        disputed_identity_keys=request.disputed_identity_keys,
        resolved_finding_ids=resolved_ids,
        unevaluated_finding_ids=unevaluated_ids,
    )
    merged = diff.all_for_review()
    _populate_occurrences(
        merged,
        pass_number=request.pass_number,
        artifact_hash=hashes.graph_sha256,
    )
    assign_display_indexes(
        [f for f in merged if f.status not in {"resolved"}]
    )

    analysis_status = _analysis_status(rule_executions, blocking_incomplete, errors)

    scorecard = build_deterministic_scorecard(
        validation,
        [f for f in merged if f.status not in {"resolved"}],
        has_sources=bool(source_paths),
        has_serializer=bool(serializer_path),
        has_coverage_contract=bool(coverage_path),
        rule_executions=rule_executions,
        serializer_is_python=serializer_is_python,
    )
    scorecard = merge_scorecards(scorecard, None)

    det_open = [
        f
        for f in merged
        if f.status not in {"resolved"} and f.evidence_kind == "deterministic"
    ]
    source_open = [
        f
        for f in merged
        if f.status not in {"resolved"} and f.evidence_kind == "source"
    ]
    critic_open = [
        f
        for f in merged
        if f.status not in {"resolved"} and f.evidence_kind == "critic_inference"
    ]

    source_excerpts = _bounded_source_excerpts(source_aliases)
    extra_ontology_sha256 = {
        f"extra-{idx}:{Path(raw).name}": sha256_file(Path(raw))
        for idx, raw in enumerate(request.extra_ontology_graphs or [], start=1)
    }
    # Bind review_config to a live disk bundle identity (not cached/stored hashes alone).
    try:
        from validation_bundle import hash_validation_bundle_identity

        live_identity = hash_validation_bundle_identity(
            extensions=list(request.extensions or []),
            profiles=list(request.profiles or []),
            extra_ontology_graphs=list(request.extra_ontology_graphs or []) or None,
            project_root=project_root,
            force_rdfs_inference=bool(request.force_rdfs_inference),
            use_cache=False,
        )
        validation.bundle_fingerprint = live_identity["bundle_fingerprint"]
        validation.bundle_resource_hashes = dict(
            live_identity["bundle_resource_hashes"]
        )
    except Exception:  # noqa: BLE001
        # Resolution failures surface later via validation / session checks.
        pass
    try:
        prompt_package = build_prompt_package(
            artifact_hashes=hashes,
            validation=validation,
            deterministic_findings=det_open,
            source_findings=source_open,
            critic_findings=critic_open,
            graph_view=view,
            serializer_excerpts=serializer_excerpts,
            serializer_overview=serializer_overview,
            source_excerpts=source_excerpts,
            prior_findings=list(request.prior_findings),
            extensions=request.extensions,
            profiles=request.profiles,
            session_id=request.session_id,
            pass_number=request.pass_number,
            critic_scope=request.critic_scope,
            serializer_mode=request.serializer_mode,
            force_rdfs_inference=bool(request.force_rdfs_inference),
            extra_ontology_sha256=extra_ontology_sha256,
        )
    except ValueError as exc:
        msg = str(exc)
        if msg == "critic_prompt_package_too_large":
            raise CriticError("critic_prompt_package_too_large") from exc
        if msg == "critic_prompt_package_size_unstable":
            raise CriticError("critic_prompt_package_size_unstable") from exc
        raise

    status = _status_from(validation, merged, errors, analysis_status)
    suggestions = _conservative_handoff_suggestions(
        merged, validation.bundle_fingerprint
    )

    review = CriticReview(
        schema_version=CRITIC_SCHEMA_VERSION,
        artifact_hashes=hashes,
        validation=validation,
        deterministic_findings=[
            f for f in merged if f.evidence_kind == "deterministic"
        ],
        critic_findings=[f for f in merged if f.evidence_kind == "critic_inference"],
        merged_findings=merged,
        scorecard=scorecard,
        prompt_package=prompt_package,
        status=status,
        analysis_status=analysis_status,
        rule_executions=rule_executions,
        finding_diff=diff.to_dict(),
        elapsed_ms=int((time.perf_counter() - started) * 1000),
        handoff_suggestions=suggestions,
        handoff_candidates=suggestions,
        errors=errors,
        token_estimate=prompt_package.get("token_estimate"),
    )
    validate_critic_review(review.to_dict())
    return review


def _source_aliases(paths: list[Path]) -> dict[str, Path]:
    """Caller-safe logical aliases (never parent/basename collision keys)."""

    aliases: dict[str, Path] = {}
    for index, path in enumerate(paths, start=1):
        aliases[f"source-{index}:{path.name}"] = path
    return aliases


def _run_validation(
    graph_path: Path,
    *,
    extensions: list[str],
    profiles: list[str],
    project_root: Path,
    errors: list[str],
    artifact_hash: str,
    extra_ontology_graphs: list[str] | None = None,
    force_rdfs_inference: bool = False,
) -> tuple[ValidationSummary, list[RuleExecution]]:
    executions: list[RuleExecution] = []
    if not graph_validator.validator_available():
        errors.append("critic_validation_unavailable")
        summary = ValidationSummary(
            conforms=None,
            verification_status="could_not_verify",
            error_code="critic_validation_unavailable",
            safe_summary="case_validate CLI is not available",
            selected_extensions=list(extensions),
            selected_profiles=list(profiles),
        )
        for rule_id in (
            "CRIT-V-SHACL",
            "CRIT-V-CONCEPT-COVERAGE",
            "CRIT-V-PROFILE-SELECTION",
        ):
            executions.append(
                RuleExecution(
                    rule_id=rule_id,
                    rule_version=RULE_VERSION,
                    status="skipped",
                    input_artifact_hash=artifact_hash,
                    error_code="critic_validation_unavailable",
                    required_for_scope=True,
                    verifies_rule_ids=[rule_id],
                )
            )
        return summary, executions

    try:
        # Critic-only profile tokens (e.g. cti-report) tune heuristics; they are
        # not CDO validation profiles and must not be passed to case_validate.
        _CRITIC_ONLY_PROFILES = {"cti-report"}
        validation_profiles = [
            p for p in (profiles or []) if str(p).strip().lower() not in _CRITIC_ONLY_PROFILES
        ]
        report = graph_validator.validate_graph_file(
            graph_path,
            extensions=extensions or None,
            profiles=validation_profiles or None,
            project_root=project_root,
            extra_ontology_graphs=extra_ontology_graphs or None,
            force_rdfs_inference=force_rdfs_inference,
        )
    except Exception as exc:  # noqa: BLE001
        errors.append("critic_validation_incomplete")
        summary = ValidationSummary(
            conforms=None,
            verification_status="could_not_verify",
            error_code="critic_validation_incomplete",
            safe_summary=type(exc).__name__,
            selected_extensions=list(extensions),
            selected_profiles=list(profiles),
        )
        for rule_id in (
            "CRIT-V-SHACL",
            "CRIT-V-CONCEPT-COVERAGE",
            "CRIT-V-PROFILE-SELECTION",
        ):
            executions.append(
                RuleExecution(
                    rule_id=rule_id,
                    rule_version=RULE_VERSION,
                    status="failed",
                    input_artifact_hash=artifact_hash,
                    error_code=type(exc).__name__,
                    required_for_scope=True,
                    verifies_rule_ids=[rule_id],
                )
            )
        return summary, executions

    stage = dict(report.stage_status)
    summary = ValidationSummary(
        conforms=report.conforms,
        verification_status=report.verification_status,
        violation_count=report.violation_count,
        warning_count=report.warning_count,
        bundle_fingerprint=report.bundle_fingerprint,
        bundle_resource_hashes={
            str(r.get("path")): str(r.get("sha256"))
            for r in (report.bundle_resources or [])
            if r.get("path") and r.get("sha256")
        },
        selected_profiles=list(report.selected_profiles),
        selected_extensions=list(report.selected_extensions),
        stage_status={k: v for k, v in stage.items()} if stage else {},
        profile_not_selected=list(report.profile_not_selected),
        role_mismatches=[list(t) for t in report.role_mismatches],
        safe_summary=report.safe_summary,
        violation_details=[dict(d) for d in report.violation_details],
        violation_details_truncated=report.violation_details_truncated,
        error_code=(
            None
            if report.verification_status == "complete"
            else "critic_validation_incomplete"
        ),
    )

    shacl_status = "evaluated"
    if report.verification_status != "complete":
        shacl_status = "failed"
    executions.append(
        RuleExecution(
            rule_id="CRIT-V-SHACL",
            rule_version=RULE_VERSION,
            status=shacl_status,  # type: ignore[arg-type]
            input_artifact_hash=artifact_hash,
            targets_examined=1,
            finding_ids=[],
            required_for_scope=True,
            verifies_rule_ids=["CRIT-V-SHACL", "CRIT-V-NONCONFORMING", "CRIT-V-UNAVAILABLE"],
        )
    )
    executions.append(
        RuleExecution(
            rule_id="CRIT-V-CONCEPT-COVERAGE",
            rule_version=RULE_VERSION,
            status="evaluated",
            input_artifact_hash=artifact_hash,
            targets_examined=1,
            finding_ids=[],
            required_for_scope=True,
            verifies_rule_ids=["CRIT-V-CONCEPT-COVERAGE"],
        )
    )
    executions.append(
        RuleExecution(
            rule_id="CRIT-V-PROFILE-SELECTION",
            rule_version=RULE_VERSION,
            status="evaluated",
            input_artifact_hash=artifact_hash,
            targets_examined=len(report.profile_not_selected or []),
            finding_ids=[],
            required_for_scope=True,
            verifies_rule_ids=[
                "CRIT-V-PROFILE-SELECTION",
                "CRIT-V-PROFILE-NOT-SELECTED",
            ],
        )
    )
    return summary, executions


def _validation_findings(validation: ValidationSummary) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    if validation.error_code == "critic_validation_unavailable":
        f = CriticFinding(
            finding_id="",
            severity="critical",
            category="validation",
            confidence=1.0,
            status="new",
            target=CriticTarget(),
            evidence_kind="deterministic",
            evidence=["validator_unavailable"],
            rationale="Required validation stage could not run (case_validate missing).",
            recommended_change="Install case-utils and re-run the critic.",
            verification_method="case_uco.validation.validator_available()",
            rule_id="CRIT-V-UNAVAILABLE",
            verifier_rule_id="CRIT-V-SHACL",
            rule_version=RULE_VERSION,
            related_validation_result="could_not_verify",
        )
        f.ensure_identity_key()
        findings.append(f)
    elif validation.verification_status != "complete" or validation.conforms is not True:
        focus_nodes = {d.get("focus_node") for d in validation.violation_details}
        f = CriticFinding(
            finding_id="",
            severity="critical",
            category="validation",
            confidence=1.0,
            status="new",
            target=CriticTarget(
                node_id=next(iter(focus_nodes)) if len(focus_nodes) == 1 else None
            ),
            evidence_kind="deterministic",
            evidence=[
                f"conforms={validation.conforms}",
                f"verification_status={validation.verification_status}",
                f"violations={validation.violation_count}",
                *(
                    "violation: focus_node={focus_node} result_path={result_path} "
                    "constraint_component={constraint_component} severity={severity}"
                    .format(**d)
                    for d in validation.violation_details
                ),
                *(
                    ["violation_details_truncated=True"]
                    if validation.violation_details_truncated
                    else []
                ),
            ],
            rationale="Graph validation is incomplete or non-conforming.",
            recommended_change="Resolve SHACL/coverage failures before acceptance.",
            verification_method="graph_validator.validate_graph_file",
            rule_id="CRIT-V-NONCONFORMING",
            verifier_rule_id="CRIT-V-SHACL",
            rule_version=RULE_VERSION,
            related_validation_result=validation.verification_status,
        )
        f.ensure_identity_key()
        findings.append(f)
    for item in validation.profile_not_selected:
        f = CriticFinding(
            finding_id="",
            severity="high",
            category="validation",
            confidence=1.0,
            status="new",
            target=CriticTarget(
                node_id=(
                    str(item.get("iri") or item.get("term"))
                    if isinstance(item, dict) and (item.get("iri") or item.get("term"))
                    else None
                )
            ),
            evidence_kind="deterministic",
            evidence=[str(item)],
            rationale="Upper-ontology term used without selecting its profile.",
            recommended_change="Pass the required profile in the validation bundle.",
            verification_method="validation.profile_not_selected",
            rule_id="CRIT-V-PROFILE-NOT-SELECTED",
            verifier_rule_id="CRIT-V-PROFILE-SELECTION",
            rule_version=RULE_VERSION,
        )
        f.ensure_identity_key()
        findings.append(f)
    return findings


def _analysis_status(
    rule_executions: list[dict[str, Any]],
    blocking_incomplete: bool,
    errors: list[str],
) -> str:
    if any(e.get("status") == "failed" and e.get("required_for_scope", True) for e in rule_executions):
        return "failed"
    if blocking_incomplete or {
        "critic_serializer_too_large",
        "critic_serializer_too_complex",
    } & set(errors):
        return "partial"
    if "critic_validation_unavailable" in errors:
        return "partial"
    return "complete"


def _status_from(
    validation: ValidationSummary,
    findings: list[CriticFinding],
    errors: list[str],
    analysis_status: str,
) -> str:
    if analysis_status != "complete":
        return "analysis_incomplete"
    open_findings = [f for f in findings if f.status not in {"resolved"}]
    if "critic_validation_unavailable" in errors:
        return "validation_incomplete"
    if validation.verification_status != "complete":
        return "validation_incomplete"
    actionable = [f for f in open_findings if f.severity in {"critical", "high"}]
    if actionable:
        return "needs_revision"
    medium = [f for f in open_findings if f.severity == "medium"]
    if medium:
        return "completed_with_findings"
    if validation.conforms is True:
        return "deterministic_clean"
    return "needs_revision"


def _populate_occurrences(
    findings: list[CriticFinding],
    *,
    pass_number: int,
    artifact_hash: str,
) -> None:
    for finding in findings:
        prior = dict(finding.occurrence or {})
        first_pass = prior.get("first_seen_pass", pass_number)
        first_hash = prior.get("first_artifact_hash", artifact_hash)
        count = int(prior.get("occurrence_count") or 0) + 1
        finding.occurrence = {
            "first_seen_pass": first_pass,
            "last_seen_pass": pass_number,
            "first_artifact_hash": first_hash,
            "last_artifact_hash": artifact_hash,
            "rule_version": finding.rule_version,
            "source_locations": [
                {
                    "path": finding.target.path,
                    "line": finding.target.line,
                    "json_pointer": finding.target.json_pointer,
                    "node_id": finding.target.node_id,
                }
            ],
            "occurrence_count": count,
        }


def _bounded_source_excerpts(
    aliases: dict[str, Path], *, max_chars: int = 800, max_read: int = 4096
) -> list[dict[str, Any]]:
    """First ``max_chars`` of each source's document text.

    ``extraction`` says where the text came from: ``<kind>_text`` from the
    document processor's extractors, ``raw_bytes`` (UTF-8 decoded) only for
    formats with no extractor, or ``no_text_extracted`` (empty text) when a
    supported document yields none, such as a scanned PDF.
    """
    import document_processor

    out: list[dict[str, Any]] = []
    for alias, path in list(aliases.items())[:5]:
        text, extraction = document_processor.review_text(path)
        if extraction == "no_extractor":
            text = path.read_bytes()[:max_read].decode("utf-8", errors="replace")
            extraction = "raw_bytes"
        if len(text) > max_chars:
            text = text[: max_chars - 1] + "…"
        out.append(
            {
                "path": alias,
                "sha256": sha256_file(path),
                "text": text,
                "extraction": extraction,
            }
        )
    return out


def _conservative_handoff_suggestions(
    findings: list[CriticFinding],
    bundle_fingerprint: str | None,
) -> list[SelfImprovementHandoffCandidate]:
    """Round 4: ordinary artifact defects are NOT persistent-learning suggestions."""

    return []
