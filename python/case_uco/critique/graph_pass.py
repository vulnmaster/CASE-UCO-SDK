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
            if types_seen and "Role" in types_seen and "Person" in types_seen:
                pass
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
