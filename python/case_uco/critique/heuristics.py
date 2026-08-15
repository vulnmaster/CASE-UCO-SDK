"""Ported construction-relevant CRIT-H-* rules over CanonicalGraphView."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from case_uco.critique.canonical import (
    IRI_ACCOUNT,
    IRI_ACTION_OBJECT,
    IRI_ACTION_RESULT,
    IRI_INSTRUMENT,
    IRI_INVESTIGATION,
    IRI_NAME,
    IRI_OBJECT,
    IRI_PERFORMER,
    IRI_PERSON,
    IRI_ROLE,
    CanonicalGraphView,
    load_canonical_graph,
)
from case_uco.critique.findings import ConstructionFinding, make_stable_finding_id

_ACTION_NAME_TOKENS = (
    "acquir", "extract", "analy", "hash", "image", "export", "ingest", "triage", "scan",
)
_ACQUISITION_NAME_TOKENS = ("acquir", "image", "export", "extract")


def view_from_graph(graph: Any) -> CanonicalGraphView | None:
    try:
        payload = graph.serialize()
    except Exception:  # noqa: BLE001
        return None
    with tempfile.NamedTemporaryFile("w", suffix=".jsonld", delete=False, encoding="utf-8") as handle:
        handle.write(payload)
        path = Path(handle.name)
    try:
        return load_canonical_graph(path)
    finally:
        path.unlink(missing_ok=True)


def evaluate_heuristics(graph: Any, profile_id: str) -> tuple[list[ConstructionFinding], list[dict[str, Any]]]:
    view = view_from_graph(graph)
    executions: list[dict[str, Any]] = []
    if view is None or not view.usable_for_heuristics:
        executions.append({"rule_id": "CRIT-H-INV-NO-OBJECT", "status": "skipped", "error_code": "view_unavailable"})
        return [], executions
    findings: list[ConstructionFinding] = []
    findings.extend(_investigation_without_object(view, profile_id))
    findings.extend(_action_profile_completeness(view, profile_id))
    findings.extend(_person_account_role_conflation(view, profile_id))
    executions.append({"rule_id": "CRIT-H-INV-NO-OBJECT", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-ACTION-COMPLETENESS", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-IDENTITY-CONFLATION", "status": "evaluated"})
    return findings, executions


def _investigation_without_object(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    out: list[ConstructionFinding] = []
    for node in view.iter_nodes():
        if not node.has_type(IRI_INVESTIGATION):
            continue
        if node.refs(IRI_OBJECT):
            continue
        out.append(
            ConstructionFinding(
                rule_id="CRIT-H-INV-NO-OBJECT",
                severity="error",
                message="Investigation present without uco-core:object",
                profile_id=profile_id,
                category="investigation_structure",
                node_id=node.iri,
                predicate=IRI_OBJECT,
                when="graph",
                evidence=["Investigation present without uco-core:object"],
                rationale="An Investigation container is present but does not reference contained objects via uco-core:object.",
                recommended_change="Attach evidence, actions, and related objects with uco-core:object.",
                verification_method="CanonicalGraphView: Investigation.refs(object).",
                finding_id=make_stable_finding_id("CRIT-H-INV-NO-OBJECT", node.iri, IRI_OBJECT),
            )
        )
    return out


def _action_profile_completeness(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    from case_uco.critique.canonical import IRI_INVESTIGATIVE_ACTION

    out: list[ConstructionFinding] = []
    for node in view.iter_nodes():
        if not node.has_type(IRI_INVESTIGATIVE_ACTION):
            continue
        names = " ".join(node.literals(IRI_NAME)).lower()
        if not names or not any(tok in names for tok in _ACTION_NAME_TOKENS):
            continue
        has_actor = bool(node.refs(IRI_PERFORMER) or node.refs(IRI_INSTRUMENT))
        has_object = bool(node.refs(IRI_ACTION_OBJECT))
        has_result = bool(node.refs(IRI_ACTION_RESULT))
        acquisition_like = any(tok in names for tok in _ACQUISITION_NAME_TOKENS)
        missing: list[str] = []
        if not has_actor:
            missing.append("performer|instrument")
        if not has_object:
            missing.append("object")
        if acquisition_like and not has_result:
            missing.append("result")
        if not missing:
            continue
        predicate = IRI_ACTION_OBJECT if "object" in missing else IRI_ACTION_RESULT
        out.append(
            ConstructionFinding(
                rule_id="CRIT-H-ACTION-COMPLETENESS",
                severity="error" if acquisition_like else "warning",
                message=f"Action profile incomplete: missing {missing}",
                profile_id=profile_id,
                category="action_grammar",
                node_id=node.iri,
                predicate=predicate,
                when="graph",
                evidence=[f"missing={missing}", f"name={names}"],
                rationale="Action profile roles are incomplete for an acquisition/analysis/hash/export-like InvestigativeAction.",
                recommended_change="Add performer or instrument, action object, and (for acquisition-like actions) result.",
                verification_method="CanonicalGraphView: performer/instrument + object (+ result).",
                finding_id=make_stable_finding_id("CRIT-H-ACTION-COMPLETENESS", node.iri, predicate),
            )
        )
    return out


def _person_account_role_conflation(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    out: list[ConstructionFinding] = []
    for node in view.iter_nodes():
        if not node.has_type(IRI_PERSON):
            continue
        accountish = node.has_type(IRI_ACCOUNT) or any(
            t == IRI_ROLE or t.endswith("/Role") or t.endswith("Account")
            for t in node.types
        )
        if not accountish:
            continue
        out.append(
            ConstructionFinding(
                rule_id="CRIT-H-IDENTITY-CONFLATION",
                severity="error",
                message="Person node is also typed as Account/Role",
                profile_id=profile_id,
                category="identity_conflation",
                node_id=node.iri,
                when="graph",
                evidence=[f"types={sorted(node.types)}"],
                rationale="A Person node is also typed as Account/Role; person and account/role identities should remain distinct.",
                recommended_change="Split Person from Account/Role and relate them with a governed kind.",
                verification_method="CanonicalNode types intersect Person and Account/Role.",
                finding_id=make_stable_finding_id("CRIT-H-IDENTITY-CONFLATION", node.iri),
            )
        )
    return out
