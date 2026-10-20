"""Graph parse/integrity checks over CanonicalGraphView."""

from __future__ import annotations

import hashlib
from pathlib import Path

from critic.canonical import (
    CanonicalGraphView,
    RuleExecution,
    collect_object_iris_from_rdf,
    load_canonical_graph,
)
from critic.finding_diff import make_stable_finding_id
from critic.models import CriticFinding, CriticTarget

RULE_VERSION = "1.1.1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def analyze_graph_integrity(
    path: Path,
    *,
    artifact_hash: str,
) -> tuple[CanonicalGraphView, list[CriticFinding], list[RuleExecution]]:
    view = load_canonical_graph(path)
    findings: list[CriticFinding] = []
    executions: list[RuleExecution] = []

    def _exec(rule_id: str, status: str, examined: int = 0, fids: list[str] | None = None, error: str | None = None):
        executions.append(
            RuleExecution(
                rule_id=rule_id,
                rule_version=RULE_VERSION,
                status=status,  # type: ignore[arg-type]
                input_artifact_hash=artifact_hash,
                targets_examined=examined,
                finding_ids=list(fids or []),
                error_code=error,
            )
        )

    if view.json_status == "unsupported_type" or view.rdf_status == "unsupported_type":
        f = _f(
            "CRIT-G-UNSUPPORTED-TYPE",
            "critical",
            "syntax_integrity",
            CriticTarget(path=path.name),
            [f"extension={path.suffix}"],
            "Graph file type is not supported.",
            "Provide .jsonld/.json or .ttl/.turtle.",
            "Check file extension.",
        )
        findings.append(f)
        _exec("CRIT-G-UNSUPPORTED-TYPE", "evaluated", 1, [f.finding_id])
        return view, findings, executions

    if view.json_status == "too_large" or view.rdf_status == "too_large":
        f = _f(
            "CRIT-G-SIZE-BOUND",
            "critical",
            "syntax_integrity",
            CriticTarget(path=path.name),
            ["size_bound"],
            "Graph exceeds the critic size bound.",
            "Split by forensic boundary or raise the bound deliberately.",
            "Compare file size to MAX_GRAPH_BYTES.",
        )
        findings.append(f)
        _exec("CRIT-G-SIZE-BOUND", "evaluated", 1, [f.finding_id])
        return view, findings, executions

    if view.kind == "jsonld" and view.json_status == "json_syntax_error":
        f = _f(
            "CRIT-G-PARSE-FAILED",
            "critical",
            "syntax_integrity",
            CriticTarget(path=path.name),
            view.errors or ["json_syntax_error"],
            "Graph JSON could not be parsed.",
            "Fix JSON syntax before critic review.",
            "Re-parse with json.loads.",
        )
        findings.append(f)
        _exec("CRIT-G-PARSE-FAILED", "evaluated", 1, [f.finding_id])
        _exec("CRIT-G-RDF-PARSE", "skipped", error="json_syntax_error")
        return view, findings, executions

    if view.rdf_status == "rdf_parse_error":
        f = _f(
            "CRIT-G-RDF-PARSE",
            "critical",
            "syntax_integrity",
            CriticTarget(path=path.name),
            view.errors or ["rdf_parse_error"],
            "RDF parse/expansion failed.",
            "Fix RDF/JSON-LD so RDFLib can parse the graph.",
            "rdflib Graph.parse",
        )
        findings.append(f)
        _exec("CRIT-G-RDF-PARSE", "evaluated", 1, [f.finding_id])
    else:
        _exec("CRIT-G-RDF-PARSE", "evaluated", 1)

    if view.duplicate_json_keys:
        f = _f(
            "CRIT-G-CONTEXT-COLLISION",
            "critical",
            "syntax_integrity",
            CriticTarget(path=path.name, predicate=view.duplicate_json_keys[0]),
            [f"duplicate_keys={view.duplicate_json_keys}"],
            "Raw JSON contains duplicate object keys (last value wins silently).",
            "Remove duplicate keys from @context or node objects.",
            "json.loads(..., object_pairs_hook=...)",
        )
        findings.append(f)
        _exec("CRIT-G-CONTEXT-COLLISION", "evaluated", len(view.duplicate_json_keys), [f.finding_id])
    else:
        _exec("CRIT-G-CONTEXT-COLLISION", "evaluated", 0)

    if not view.nodes:
        f = _f(
            "CRIT-G-EMPTY",
            "critical",
            "syntax_integrity",
            CriticTarget(path=path.name),
            ["node_count=0"],
            "Graph contains no identified nodes.",
            "Emit at least one typed CASE/UCO object with @id.",
            "Count indexed nodes in CanonicalGraphView.",
        )
        findings.append(f)
        _exec("CRIT-G-EMPTY", "evaluated", 0, [f.finding_id])
        _exec("CRIT-G-DUPLICATE-ID", "skipped", error="empty_graph")
        _exec("CRIT-G-DANGLING-REF", "skipped", error="empty_graph")
        return view, findings, executions

    # Duplicate top-level IDs from raw JSON (semantic)
    if view.raw_document and isinstance(view.raw_document.get("@graph"), list):
        counts: dict[str, int] = {}
        for node in view.raw_document["@graph"]:
            if isinstance(node, dict) and isinstance(node.get("@id"), str):
                counts[node["@id"]] = counts.get(node["@id"], 0) + 1
        dup_findings = []
        for node_id, count in counts.items():
            if count > 1:
                f = _f(
                    "CRIT-G-DUPLICATE-ID",
                    "high",
                    "syntax_integrity",
                    CriticTarget(node_id=node_id),
                    [f"occurrences={count}"],
                    "Duplicate top-level @id values present in @graph.",
                    "Deduplicate or use CASEGraph upsert/reject policy.",
                    "Group @graph by @id.",
                )
                findings.append(f)
                dup_findings.append(f.finding_id)
        _exec("CRIT-G-DUPLICATE-ID", "evaluated", len(counts), dup_findings)
    else:
        _exec("CRIT-G-DUPLICATE-ID", "evaluated", len(view.nodes))

    # Dangling refs from RDF object positions / JSON @id refs
    known = set(view.nodes)
    object_iris = collect_object_iris_from_rdf(view)
    dangling_ids: list[str] = []
    examined_refs = 0
    kb_base = view.prefixes.get("kb")
    for obj_iri in sorted(object_iris):
        examined_refs += 1
        if not (_is_local_resolvable(obj_iri) or (kb_base and obj_iri.startswith(kb_base))):
            continue
        if obj_iri not in known:
            f = _f(
                "CRIT-G-DANGLING-REF",
                "high",
                "syntax_integrity",
                CriticTarget(node_id=obj_iri, predicate="rdf:object"),
                [f"missing_ref={obj_iri}"],
                "Local graph reference does not resolve to an identified node.",
                "Add the referenced node or fix the IRI.",
                "Membership of RDF object IRI in node index.",
            )
            findings.append(f)
            dangling_ids.append(f.finding_id)
    _exec("CRIT-G-DANGLING-REF", "evaluated", examined_refs, dangling_ids)

    return view, findings, executions


def _is_local_resolvable(iri: str) -> bool:
    return (
        iri.startswith("urn:uuid:")
        or iri.startswith("urn:example:")
        or iri.startswith("urn:case:")
        or iri.startswith("kb:")
        or "/operation-phantom-gate" in iri
        or iri.startswith("urn:case-uco:")
    )


def _f(
    rule_id: str,
    severity: str,
    category: str,
    target: CriticTarget,
    evidence: list[str],
    rationale: str,
    recommended_change: str,
    verification_method: str,
) -> CriticFinding:
    finding_id = make_stable_finding_id(rule_id, *target.semantic_parts())
    return CriticFinding(
        finding_id=finding_id,
        severity=severity,  # type: ignore[arg-type]
        category=category,
        confidence=1.0,
        status="new",
        target=target,
        evidence_kind="deterministic",
        evidence=evidence,
        rationale=rationale,
        recommended_change=recommended_change,
        verification_method=verification_method,
        rule_id=rule_id,
        identity_key=finding_id,
    )

