"""Incremental (add-time) contract checks. No RDFLib, O(added node)."""

from __future__ import annotations

from typing import Any

from case_uco.contracts.profile import ContractCheck, ProfileContract
from case_uco.critique.findings import ConstructionFinding
from case_uco.critique.hosts import facet_names, host_matches, resolve_host

_FORBIDDEN_PHOTODNA = {"PhotoDNAFacet", "PerceptualHashFacet"}


def _hashes_from_extra(extra: dict[str, Any] | None) -> list[Any]:
    extra = extra or {}
    hashes = extra.get("hashes")
    if hashes is None:
        return []
    return list(hashes)


def evaluate_incremental(
    contract: ProfileContract,
    *,
    host: str | None,
    node: Any,
    extra: dict[str, Any] | None,
    source: str | None,
) -> list[ConstructionFinding]:
    findings: list[ConstructionFinding] = []
    resolved = resolve_host(node, host)
    extra = extra or {}
    hashes = _hashes_from_extra(extra)
    file_name = extra.get("file_name") or extra.get("path") or ""
    tool_name = extra.get("tool_name") or ""
    tool_version = extra.get("tool_version")

    # Frozen original InvestigationBuilder triples.
    if source == "add_file" and not hashes:
        findings.append(
            ConstructionFinding(
                rule_id="PROF-HASH-001",
                severity="error",
                message=f"{file_name}: {contract.profile_id} requires ContentDataFacet hashes",
                path=str(file_name),
                blocking=True,
                profile_id=contract.profile_id,
                host=resolved or "File",
                category="hash_integrity",
                repair={"helper": "file_with_content_hashes", "builder_method": "add_file",
                        "hint": "Provide ContentDataFacet hashes."},
            )
        )
    if source == "add_csam_evidence" and not hashes:
        findings.append(
            ConstructionFinding(
                rule_id="PROF-HASH-001",
                severity="error",
                message=f"{file_name}: CSAM evidence must carry hashes",
                path=str(file_name),
                blocking=True,
                profile_id=contract.profile_id,
                host="RasterPicture",
                category="hash_integrity",
                repair={"helper": "model_csam_evidence", "builder_method": "add_csam_evidence",
                        "hint": "Provide SHA-256; add PhotoDNA as an additional Hash."},
            )
        )
    if source == "add_tool_run" and not tool_version:
        findings.append(
            ConstructionFinding(
                rule_id="PROF-TOOL-001",
                severity="warning",
                message=f"Tool {tool_name} has no version",
                path=str(tool_name),
                blocking=False,
                profile_id=contract.profile_id,
                host="Tool",
                category="tool_provenance",
                repair={"helper": "model_tool_run", "builder_method": "add_tool_run",
                        "hint": "Set Tool.version."},
            )
        )

    present_facets = facet_names(node)
    type_names = {resolved or "", host or ""} | present_facets

    for check in contract.checks_for("incremental"):
        if check.id in {f.rule_id for f in findings} and check.kind in {"hash_presence", "tool_version"}:
            continue
        if not host_matches(resolved, check.applies_to) and "*" not in check.applies_to:
            continue
        if check.kind == "required_facets" and contract.source_profile:
            facet_set = contract.source_profile.facet_set_for(resolved or host or "")
            if facet_set is None and resolved == "File":
                facet_set = contract.source_profile.facet_set_for("ObservableObject")
            if facet_set is None:
                continue
            missing = [name for name in facet_set.required if name not in present_facets]
            if missing:
                findings.append(
                    ConstructionFinding(
                        rule_id=check.id,
                        severity="error" if check.blocking else "warning",
                        message=f"{file_name or resolved}: missing required Facets {missing}",
                        path=str(file_name),
                        blocking=check.blocking,
                        profile_id=contract.profile_id,
                        host=resolved,
                        category="facets",
                        evidence=[f"missing={missing}"],
                        repair=check.repair.as_dict(),
                    )
                )
        elif check.kind == "no_invented_photodna_facet":
            if type_names & _FORBIDDEN_PHOTODNA or present_facets & _FORBIDDEN_PHOTODNA:
                findings.append(
                    ConstructionFinding(
                        rule_id=check.id,
                        severity="error",
                        message="Do not invent PhotoDNAFacet; use Hash.hashMethod=PhotoDNA",
                        path=str(file_name),
                        blocking=True,
                        profile_id=contract.profile_id,
                        host=resolved,
                        category="ontology_gap",
                        repair=check.repair.as_dict(),
                    )
                )
        elif check.kind == "hash_presence" and source not in {"add_file", "add_csam_evidence"}:
            methods_req = [m.upper() for m in (check.params.get("methods_required") or [])]
            present_methods = []
            for item in hashes:
                if isinstance(item, (tuple, list)) and item:
                    present_methods.append(str(item[0]).upper())
            if methods_req and not any(m in present_methods for m in methods_req) and hashes:
                findings.append(
                    ConstructionFinding(
                        rule_id=check.id,
                        severity="warning",
                        message=f"{file_name}: recommended hash methods missing {methods_req}",
                        path=str(file_name),
                        blocking=False,
                        profile_id=contract.profile_id,
                        host=resolved,
                        category="hash_integrity",
                        repair=check.repair.as_dict(),
                    )
                )
    return findings
