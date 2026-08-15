"""Graph-wide Facet-set walk and mission checks on public graph.nodes()."""

from __future__ import annotations

from typing import Any

from case_uco.contracts.profile import ProfileContract
from case_uco.critique.findings import ConstructionFinding
from case_uco.critique.hosts import facet_names, host_matches, local_types, resolve_host

_FORBIDDEN_PHOTODNA = {"PhotoDNAFacet", "PerceptualHashFacet"}


def _node_id(node: dict[str, Any]) -> str:
    return str(node.get("@id") or "")


def _hash_entries(node: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if any(k in value for k in ("uco-types:hashValue", "hashValue", "uco-types:hashMethod", "hashMethod")):
                entries.append(value)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(node)
    return entries


def evaluate_graph_pass(
    graph: Any,
    contract: ProfileContract,
    *,
    when: str = "graph",
) -> list[ConstructionFinding]:
    findings: list[ConstructionFinding] = []
    try:
        nodes = graph.nodes()
    except Exception:  # noqa: BLE001
        return findings

    types_seen: set[str] = set()
    for node in nodes:
        types_seen |= local_types(node)

    for node in nodes:
        host = resolve_host(node)
        present = facet_names(node)
        hashes = _hash_entries(node)
        nid = _node_id(node)
        for check in contract.checks_for(when):
            if check.kind in {"shacl_signal", "concept_coverage_signal"}:
                continue
            if not host_matches(host, check.applies_to) and "*" not in check.applies_to:
                if check.kind not in {
                    "hash_intelligence_mission",
                    "cac_lifecycle_mission",
                    "legal_process_mission",
                    "airgap_partition",
                    "cross_ontology_single_foundation",
                    "spine_kind_present",
                    "spine_role_separation",
                }:
                    continue
            if check.kind == "required_facets" and contract.source_profile and host:
                facet_set = contract.source_profile.facet_set_for(host)
                if facet_set is None and host == "File":
                    facet_set = contract.source_profile.facet_set_for("ObservableObject")
                if facet_set and any(name not in present for name in facet_set.required):
                    missing = [n for n in facet_set.required if n not in present]
                    findings.append(
                        ConstructionFinding(
                            rule_id=check.id,
                            severity="error" if check.blocking else "warning",
                            message=f"{nid}: missing required Facets {missing}",
                            path=nid,
                            node_id=nid,
                            host=host,
                            blocking=check.blocking,
                            profile_id=contract.profile_id,
                            when=when,
                            category="facets",
                            repair=check.repair.as_dict(),
                        )
                    )
            elif check.kind == "hash_presence" and host in {"File", "RasterPicture", "ObservableObject"}:
                if not hashes:
                    findings.append(
                        ConstructionFinding(
                            rule_id=check.id,
                            severity="error" if check.blocking else "warning",
                            message=f"{nid}: ContentDataFacet hashes missing",
                            path=nid,
                            node_id=nid,
                            host=host,
                            blocking=check.blocking,
                            profile_id=contract.profile_id,
                            when=when,
                            category="hash_integrity",
                            repair=check.repair.as_dict(),
                        )
                    )
            elif check.kind == "no_invented_photodna_facet":
                if present & _FORBIDDEN_PHOTODNA or local_types(node) & _FORBIDDEN_PHOTODNA:
                    findings.append(
                        ConstructionFinding(
                            rule_id=check.id,
                            severity="error",
                            message="Invented PhotoDNAFacet / PerceptualHashFacet is forbidden",
                            path=nid,
                            node_id=nid,
                            host=host,
                            blocking=True,
                            profile_id=contract.profile_id,
                            when=when,
                            category="ontology_gap",
                            repair=check.repair.as_dict(),
                        )
                    )
            elif check.kind == "spine_role_separation":
                types = local_types(node)
                if "Person" in types and ("Role" in types or "Account" in types):
                    findings.append(
                        ConstructionFinding(
                            rule_id=check.id,
                            severity="error",
                            message=f"{nid}: person typed as Role/Account",
                            path=nid,
                            node_id=nid,
                            host=host,
                            blocking=True,
                            profile_id=contract.profile_id,
                            when=when,
                            category="identity_conflation",
                            repair=check.repair.as_dict(),
                        )
                    )
            elif check.kind == "tool_version" and host == "Tool":
                if not _node_has_version(node):
                    findings.append(
                        ConstructionFinding(
                            rule_id=check.id,
                            severity="error" if check.blocking else "warning",
                            message=f"{nid}: Tool has no version",
                            path=nid,
                            node_id=nid,
                            host=host,
                            blocking=check.blocking,
                            profile_id=contract.profile_id,
                            when=when,
                            category="tool_provenance",
                            repair=check.repair.as_dict(),
                        )
                    )
            elif check.kind == "action_instrument" and (
                host == "InvestigativeAction" or "InvestigativeAction" in local_types(node)
            ):
                if not _action_has_instrument(node):
                    findings.append(
                        ConstructionFinding(
                            rule_id=check.id,
                            severity="error" if check.blocking else "warning",
                            message=f"{nid}: InvestigativeAction missing instrument",
                            path=nid,
                            node_id=nid,
                            host=host,
                            blocking=check.blocking,
                            profile_id=contract.profile_id,
                            when=when,
                            category="action_grammar",
                            repair=check.repair.as_dict(),
                        )
                    )

    if when in {"step", "graph"}:
        findings.extend(_mission_checks(graph, contract, types_seen, when))
    return findings


def _mission_checks(
    graph: Any,
    contract: ProfileContract,
    types_seen: set[str],
    when: str,
) -> list[ConstructionFinding]:
    findings: list[ConstructionFinding] = []
    media_present = bool(types_seen & {"RasterPicture", "Image", "File", "ObservableObject"})
    for check in contract.checks_for(when):
        if check.kind == "hash_intelligence_mission" and media_present:
            blob = " ".join(sorted(types_seen)).lower()
            if "investigativeaction" not in blob and "tool" not in blob:
                findings.append(
                    ConstructionFinding(
                        rule_id=check.id,
                        severity="error",
                        message="HashIntelligence mission: hashing Tool + InvestigativeAction missing",
                        blocking=True,
                        profile_id=contract.profile_id,
                        when=when,
                        category="mission",
                        repair=check.repair.as_dict(),
                    )
                )
        elif check.kind == "cac_lifecycle_mission":
            findings.extend(_cac_lifecycle_mission(graph, contract, check, types_seen, when))
        elif check.kind == "legal_process_mission":
            findings.extend(_legal_process_mission(graph, contract, check, types_seen, when))
        elif check.kind == "spine_kind_present":
            findings.extend(_spine_kind_present(contract, check, types_seen, when))
        elif check.kind == "trajectory_completeness":
            findings.extend(_trajectory_completeness(graph, contract, check, types_seen, when))
        elif check.kind == "airgap_partition":
            max_triples = int(check.params.get("max_estimated_triples") or 200000)
            estimated = graph.estimate_triples()
            if estimated > max_triples:
                findings.append(
                    ConstructionFinding(
                        rule_id=check.id,
                        severity="warning",
                        message=f"Estimated triples {estimated} exceed air-gap comfort {max_triples}",
                        blocking=False,
                        profile_id=contract.profile_id,
                        when=when,
                        category="partition",
                        repair=check.repair.as_dict(),
                    )
                )
        elif check.kind == "cross_ontology_single_foundation":
            blob = " ".join(sorted(types_seen)).lower()
            if "bfo" in blob and ("gufo" in blob or "g-ufos" in blob):
                findings.append(
                    ConstructionFinding(
                        rule_id=check.id,
                        severity="error",
                        message="Dual BFO+gUFO typing is an anti-pattern",
                        blocking=True,
                        profile_id=contract.profile_id,
                        when=when,
                        category="cross_ontology",
                        repair=check.repair.as_dict(),
                    )
                )
    return findings


def _node_has_version(node: dict[str, Any]) -> bool:
    for key in (
        "uco-tool:version",
        "uco-core:version",
        "version",
        "https://ontology.unifiedcyberontology.org/uco/tool/version",
    ):
        if node.get(key):
            return True
    return False


def _action_has_instrument(node: dict[str, Any]) -> bool:
    for key in (
        "uco-action:instrument",
        "instrument",
        "https://ontology.unifiedcyberontology.org/uco/action/instrument",
        "uco-action:performer",
        "performer",
    ):
        if node.get(key):
            return True
    return False


def _cac_lifecycle_mission(
    graph: Any,
    contract: ProfileContract,
    check: Any,
    types_seen: set[str],
    when: str,
) -> list[ConstructionFinding]:
    findings: list[ConstructionFinding] = []
    media_types = types_seen & {"RasterPicture", "Image", "File", "ObservableObject"}
    if not media_types and "Person" not in types_seen and not any(
        "cac" in t.lower() or t.startswith("CAC") for t in types_seen
    ):
        return findings
    hashed = False
    cac_as_bytes = False
    for node in graph.nodes():
        host = resolve_host(node)
        types = local_types(node)
        if host in {"File", "RasterPicture", "ObservableObject"} and _hash_entries(node):
            hashed = True
        if types & {"RasterPicture", "File", "ObservableObject"} and any(
            "cac" in t.lower() or t.startswith("CAC") for t in types
        ):
            cac_as_bytes = True
    if media_types and not hashed:
        findings.append(
            ConstructionFinding(
                rule_id=check.id,
                severity="error",
                message="FullCACLifecycle mission: media present without ContentDataFacet hashes",
                blocking=True,
                profile_id=contract.profile_id,
                when=when,
                category="mission",
                repair=check.repair.as_dict(),
            )
        )
    if "Person" in types_seen and "Role" not in types_seen:
        findings.append(
            ConstructionFinding(
                rule_id=check.id,
                severity="error",
                message="FullCACLifecycle mission: Person present without a distinct Role",
                blocking=True,
                profile_id=contract.profile_id,
                when=when,
                category="mission",
                repair=check.repair.as_dict(),
            )
        )
    if cac_as_bytes:
        findings.append(
            ConstructionFinding(
                rule_id=check.id,
                severity="error",
                message="FullCACLifecycle mission: media must be RasterPicture/File, not a CAC class standing in for bytes",
                blocking=True,
                profile_id=contract.profile_id,
                when=when,
                category="mission",
                repair=check.repair.as_dict(),
            )
        )
    return findings


def _legal_process_mission(
    graph: Any,
    contract: ProfileContract,
    check: Any,
    types_seen: set[str],
    when: str,
) -> list[ConstructionFinding]:
    legal_hosts = {
        t
        for t in types_seen
        if any(token in t for token in ("Charge", "Plea", "Charging", "Indictment", "Docket"))
        or t.lower().startswith("legal")
    }
    if not legal_hosts:
        return []
    findings: list[ConstructionFinding] = []
    if "Person" not in types_seen or "Role" not in types_seen:
        findings.append(
            ConstructionFinding(
                rule_id=check.id,
                severity="error",
                message="LegalProcess mission: legal nodes require distinct Person + Role",
                blocking=True,
                profile_id=contract.profile_id,
                when=when,
                category="mission",
                repair=check.repair.as_dict(),
            )
        )
    return findings


def _spine_kind_present(
    contract: ProfileContract,
    check: Any,
    types_seen: set[str],
    when: str,
) -> list[ConstructionFinding]:
    if not types_seen:
        return []
    kinds = [str(k) for k in (check.params.get("kinds") or ["Role", "Phase", "InvestigativeAction"])]
    missing = [kind for kind in kinds if kind not in types_seen]
    if not missing:
        return []
    return [
        ConstructionFinding(
            rule_id=check.id,
            severity="warning" if not check.blocking else "error",
            message=f"Semantic spine kinds missing: {missing}",
            blocking=check.blocking,
            profile_id=contract.profile_id,
            when=when,
            category="spine",
            evidence=[f"missing={missing}"],
            repair=check.repair.as_dict(),
        )
    ]


def _trajectory_completeness(
    graph: Any,
    contract: ProfileContract,
    check: Any,
    types_seen: set[str],
    when: str,
) -> list[ConstructionFinding]:
    trigger = set(check.params.get("hosts") or ["Message", "OnlineGrooming", "InitialContactPhase"])
    if not (types_seen & trigger):
        return []
    try:
        from case_uco.trajectories import evaluate_trajectory
    except ImportError:
        return []
    traj_ids = list(check.params.get("trajectories") or contract.trajectories or ["grooming-phase"])
    findings: list[ConstructionFinding] = []
    for traj_id in traj_ids:
        try:
            items = evaluate_trajectory(graph, traj_id)
        except Exception:  # noqa: BLE001
            continue
        for item in items:
            findings.append(
                ConstructionFinding(
                    rule_id=str(item.get("rule_id") or check.id),
                    severity=str(item.get("severity") or "warning"),
                    message=str(item.get("message") or f"Trajectory {traj_id} incomplete"),
                    path=str(item.get("path") or traj_id),
                    blocking=bool(check.blocking and str(item.get("rule_id")) != "PROF-TRAJ-NOT-GENERATED"),
                    profile_id=contract.profile_id,
                    when=when,
                    category="trajectory",
                    repair=item.get("repair") if isinstance(item.get("repair"), dict) else check.repair.as_dict(),
                )
            )
    return findings
