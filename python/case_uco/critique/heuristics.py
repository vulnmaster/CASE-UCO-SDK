"""Ported construction-relevant CRIT-H-* rules over CanonicalGraphView."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from case_uco.critique.canonical import (
    IRI_ACCOUNT,
    IRI_ACTION_OBJECT,
    IRI_ACTION_RESULT,
    IRI_CONTENT_FACET,
    IRI_CONTEXTUAL_COMPILATION,
    IRI_FILE,
    IRI_HASH,
    IRI_HASH_VALUE,
    IRI_HAS_FACET,
    IRI_IMAGE,
    IRI_INSTRUMENT,
    IRI_INVESTIGATION,
    IRI_INVESTIGATIVE_ACTION,
    IRI_KIND,
    IRI_NAME,
    IRI_OBJECT,
    IRI_OBSERVABLE,
    IRI_PERFORMER,
    IRI_PERSON,
    IRI_PROVENANCE_RECORD,
    IRI_RASTER,
    IRI_RELATIONSHIP,
    IRI_ROLE,
    IRI_SOURCE,
    IRI_TAG,
    IRI_TARGET,
    CanonicalGraphView,
    CanonicalNode,
    load_canonical_graph,
)
from case_uco.critique.findings import ConstructionFinding, make_stable_finding_id

_ACTION_NAME_TOKENS = (
    "acquir", "extract", "analy", "hash", "image", "export", "ingest", "triage", "scan",
)
_ACQUISITION_NAME_TOKENS = ("acquir", "image", "export", "extract")
_FORENSIC_IMAGE_TOKENS = ("e01", "dd", "ufed", "raw image", ".raw", "aff4", "ewf")
_DERIVED_KINDS = frozenset({"Extracted_From", "Contained_Within"})
_PROVENANCE_KINDS = frozenset({"Extracted_From", "Created_By", "Contained_Within"})


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
    findings.extend(_derived_without_hash(view, profile_id))
    findings.extend(_derived_without_provenance(view, profile_id))
    findings.extend(_charged_with_reversed(view, profile_id))
    findings.extend(_image_container_mismatch(view, profile_id))
    findings.extend(_orphan_top_level(view, profile_id))
    executions.append({"rule_id": "CRIT-H-INV-NO-OBJECT", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-ACTION-COMPLETENESS", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-IDENTITY-CONFLATION", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-DERIVED-NO-HASH", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-DERIVED-NO-PROVENANCE", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-CHARGED-WITH-REVERSED", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-IMAGE-CONTAINER-MISMATCH", "status": "evaluated"})
    executions.append({"rule_id": "CRIT-H-ORPHAN-TOP-LEVEL", "status": "evaluated"})
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


def _relationship_kinds(node: CanonicalNode) -> set[str]:
    kinds = set(node.literals(IRI_KIND))
    kinds.update(ref.rsplit("/", 1)[-1] for ref in node.refs(IRI_KIND))
    return kinds


def _is_action_node(node: CanonicalNode) -> bool:
    return node.has_type(IRI_INVESTIGATIVE_ACTION) or any(
        t.endswith("Action") or t.endswith("/Action") for t in node.types
    )


def _node_hash_values(view: CanonicalGraphView, node: CanonicalNode) -> list[str]:
    out: list[str] = []
    if node.raw_json:
        facets = node.raw_json.get("uco-core:hasFacet") or []
        if not isinstance(facets, list):
            facets = [facets]
        for facet in facets:
            if not isinstance(facet, dict):
                continue
            types = facet.get("@type")
            type_list = types if isinstance(types, list) else [types]
            if not any(t and "ContentDataFacet" in str(t) for t in type_list):
                continue
            hashes = facet.get("uco-observable:hash") or []
            if not isinstance(hashes, list):
                hashes = [hashes]
            for item in hashes:
                if not isinstance(item, dict):
                    continue
                val = item.get("uco-types:hashValue")
                if isinstance(val, dict):
                    val = val.get("@value")
                if isinstance(val, str) and val:
                    out.append(val)
    for facet_iri in node.refs(IRI_HAS_FACET):
        facet = view.get(facet_iri)
        if not facet or not (
            facet.has_type(IRI_CONTENT_FACET)
            or any("ContentDataFacet" in t for t in facet.types)
        ):
            continue
        for href in facet.refs(IRI_HASH):
            hnode = view.get(href)
            if hnode:
                out.extend(hnode.literals(IRI_HASH_VALUE))
        out.extend(facet.literals(IRI_HASH_VALUE))
    return out


def _derived_file_iris(view: CanonicalGraphView) -> set[str]:
    derived: set[str] = set()
    for node in view.iter_nodes():
        if _is_action_node(node):
            for ref in node.refs(IRI_ACTION_RESULT):
                target = view.get(ref)
                if target and target.has_type(IRI_FILE, IRI_OBSERVABLE, IRI_IMAGE):
                    if not any("Facet" in t for t in target.types):
                        derived.add(ref)
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        if not (_relationship_kinds(node) & _DERIVED_KINDS):
            continue
        for src in node.refs(IRI_SOURCE):
            source_node = view.get(src)
            if source_node and source_node.has_type(IRI_FILE, IRI_OBSERVABLE, IRI_IMAGE):
                if not any("Facet" in t for t in source_node.types):
                    derived.add(src)
    return derived


def _derived_without_hash(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    out: list[ConstructionFinding] = []
    for iri in sorted(_derived_file_iris(view)):
        node = view.get(iri)
        if not node or _node_hash_values(view, node):
            continue
        out.append(
            ConstructionFinding(
                rule_id="CRIT-H-DERIVED-NO-HASH",
                severity="error",
                message="Derived File/Observable lacks ContentDataFacet hashValue",
                profile_id=profile_id,
                category="provenance",
                node_id=iri,
                predicate=IRI_HASH_VALUE,
                when="graph",
                evidence=["derived_without_ContentDataFacet_hashValue"],
                rationale="A derived File/Observable (action result or Extracted_From source) has no digest.",
                recommended_change="Attach ContentDataFacet with hashMethod/hashValue.",
                verification_method="hasFacet → ContentDataFacet → hash → hashValue.",
                finding_id=make_stable_finding_id("CRIT-H-DERIVED-NO-HASH", iri, IRI_HASH_VALUE),
            )
        )
    return out


def _derived_without_provenance(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    members: set[str] = set()
    inbound: set[str] = set()
    for node in view.iter_nodes():
        if node.has_type(IRI_INVESTIGATION, IRI_PROVENANCE_RECORD, IRI_CONTEXTUAL_COMPILATION):
            members.update(node.refs(IRI_OBJECT))
        if node.has_type(IRI_RELATIONSHIP) and (_relationship_kinds(node) & _PROVENANCE_KINDS):
            inbound.update(node.refs(IRI_SOURCE))
    out: list[ConstructionFinding] = []
    for iri in sorted(_derived_file_iris(view)):
        if iri in members or iri in inbound:
            continue
        node = view.get(iri)
        if not node:
            continue
        out.append(
            ConstructionFinding(
                rule_id="CRIT-H-DERIVED-NO-PROVENANCE",
                severity="error",
                message="Derived artifact has no inbound provenance or container membership",
                profile_id=profile_id,
                category="provenance",
                node_id=iri,
                when="graph",
                evidence=["no_container_membership_or_inbound_provenance_edge"],
                rationale="Derived artifact is not on Investigation/ProvenanceRecord.object and has no Extracted_From/Created_By/Contained_Within inbound edge.",
                recommended_change="Attach via uco-core:object or add a provenance relationship.",
                verification_method="Container membership + inbound provenance kind scan.",
                finding_id=make_stable_finding_id("CRIT-H-DERIVED-NO-PROVENANCE", iri),
            )
        )
    return out


def _charged_with_reversed(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    out: list[ConstructionFinding] = []
    for node in view.iter_nodes():
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        if "Charged_With" not in _relationship_kinds(node):
            continue
        source_refs = node.refs(IRI_SOURCE)
        target_refs = node.refs(IRI_TARGET)
        if not source_refs or not target_refs:
            continue
        source_node = view.get(source_refs[0])
        target_node = view.get(target_refs[0])
        if not source_node or not target_node:
            continue
        source_is_charge = any("Charge" in t for t in source_node.types) or any(
            "charge" in lit.lower() for lit in source_node.literals(IRI_NAME) + source_node.literals(IRI_TAG)
        )
        target_is_person = target_node.has_type(IRI_PERSON) or any(
            "Person" in t or "Identity" in t for t in target_node.types
        )
        if source_is_charge and target_is_person:
            out.append(
                ConstructionFinding(
                    rule_id="CRIT-H-CHARGED-WITH-REVERSED",
                    severity="error",
                    message="Charged_With is modeled person→charge; this edge is charge→person",
                    profile_id=profile_id,
                    category="relationship_direction",
                    node_id=node.iri,
                    predicate=IRI_KIND,
                    when="graph",
                    evidence=[f"source={source_refs[0]}", f"target={target_refs[0]}"],
                    rationale="Charged_With is modeled person→charge; this edge is charge→person.",
                    recommended_change="Reverse source and target.",
                    verification_method="CanonicalGraphView: Relationship source Charge, target Person.",
                    finding_id=make_stable_finding_id("CRIT-H-CHARGED-WITH-REVERSED", node.iri, IRI_KIND),
                )
            )
    return out


def _image_container_mismatch(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    out: list[ConstructionFinding] = []
    for node in view.iter_nodes():
        if node.has_type(IRI_RASTER):
            text = " ".join(node.literals(IRI_NAME) + node.literals(IRI_TAG)).lower()
            if any(tok in text for tok in _FORENSIC_IMAGE_TOKENS):
                out.append(
                    ConstructionFinding(
                        rule_id="CRIT-H-IMAGE-CONTAINER-MISMATCH",
                        severity="error",
                        message="RasterPicture is labeled like a forensic disk/raw image",
                        profile_id=profile_id,
                        category="facet_placement",
                        node_id=node.iri,
                        when="graph",
                        evidence=[f"raster_named_as_forensic_image={text}"],
                        rationale="RasterPicture is labeled like a forensic disk/raw image (E01/dd/UFED/raw); use Image/File instead.",
                        recommended_change="Retype forensic image as Image/File (not RasterPicture).",
                        verification_method="RasterPicture name/tag forensic-image tokens.",
                        finding_id=make_stable_finding_id("CRIT-H-IMAGE-CONTAINER-MISMATCH", node.iri),
                    )
                )
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        if "Contained_Within" not in _relationship_kinds(node):
            continue
        for src in node.refs(IRI_SOURCE):
            for tgt in node.refs(IRI_TARGET):
                source_node = view.get(src)
                target_node = view.get(tgt)
                if not source_node or not target_node:
                    continue
                if source_node.has_type(IRI_FILE, IRI_OBSERVABLE) and target_node.has_type(IRI_RASTER):
                    out.append(
                        ConstructionFinding(
                            rule_id="CRIT-H-IMAGE-CONTAINER-MISMATCH",
                            severity="error",
                            message="File Contained_Within a RasterPicture — forensic container mismatch",
                            profile_id=profile_id,
                            category="facet_placement",
                            node_id=node.iri,
                            predicate=IRI_KIND,
                            when="graph",
                            evidence=[f"file={src}", f"raster_container={tgt}"],
                            rationale="File Contained_Within a RasterPicture is a physical/logical image mismatch.",
                            recommended_change="Use Image/File as the container, not RasterPicture.",
                            verification_method="Contained_Within File→RasterPicture.",
                            finding_id=make_stable_finding_id(
                                "CRIT-H-IMAGE-CONTAINER-MISMATCH", node.iri, IRI_KIND
                            ),
                        )
                    )
    return out


def _orphan_top_level(view: CanonicalGraphView, profile_id: str) -> list[ConstructionFinding]:
    roots: set[str] = set()
    for node in view.iter_nodes():
        if node.has_type(IRI_INVESTIGATION, IRI_PROVENANCE_RECORD):
            roots.add(node.iri)
            roots.update(node.refs(IRI_OBJECT))
    if not roots:
        return []
    reachable = set(roots)
    changed = True
    while changed:
        changed = False
        before = len(reachable)
        for node in view.iter_nodes():
            if node.has_type(IRI_RELATIONSHIP):
                srcs = set(node.refs(IRI_SOURCE))
                tgts = set(node.refs(IRI_TARGET))
                if (srcs & reachable) or (tgts & reachable):
                    reachable.update(srcs)
                    reachable.update(tgts)
                    reachable.add(node.iri)
            if node.iri in reachable:
                reachable.update(node.refs(IRI_OBJECT))
                if _is_action_node(node):
                    reachable.update(node.refs(IRI_PERFORMER))
                    reachable.update(node.refs(IRI_INSTRUMENT))
                    reachable.update(node.refs(IRI_ACTION_OBJECT))
                    reachable.update(node.refs(IRI_ACTION_RESULT))
        if len(reachable) > before:
            changed = True
    out: list[ConstructionFinding] = []
    for node in view.iter_nodes():
        if node.has_type(IRI_RELATIONSHIP, IRI_INVESTIGATION, IRI_PROVENANCE_RECORD):
            continue
        if any("Facet" in t for t in node.types):
            continue
        if node.iri in reachable:
            continue
        out.append(
            ConstructionFinding(
                rule_id="CRIT-H-ORPHAN-TOP-LEVEL",
                severity="warning",
                message="Top-level node is not reachable from Investigation/ProvenanceRecord",
                profile_id=profile_id,
                category="investigation_structure",
                node_id=node.iri,
                when="graph",
                blocking=False,
                evidence=[f"reachable_count={len(reachable)}"],
                rationale="Top-level node is not reachable from any Investigation / ProvenanceRecord via object membership or connecting relationships.",
                recommended_change="Add a relationship or compilation membership under an Investigation/ProvenanceRecord.",
                verification_method="BFS from Investigation/ProvenanceRecord roots.",
                finding_id=make_stable_finding_id("CRIT-H-ORPHAN-TOP-LEVEL", node.iri),
            )
        )
    return out
