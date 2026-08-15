#!/usr/bin/env python3
"""Build Phase-0 topology artifacts from the vendored SDK sources.

Stdlib only. Offline. Re-runnable. The outputs under topology/ are the
machine-readable articulation of the SDK as observed at the current
commit — not a hand-maintained sketch.

Usage (from repository root):

    python topology/scripts/build_baseline.py
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY = REPO_ROOT / "topology"
RECIPES_DIR = REPO_ROOT / "docs" / "recipes"
DOMAIN_INDEX = REPO_ROOT / "mcp_server" / "domain_index.py"

PREFIX_RE = re.compile(
    r"@prefix\s+([A-Za-z0-9_-]+):\s+<([^>]+)>\s*\.",
    re.MULTILINE,
)
# Turtle comments of the form ``# imports: <IRI>`` used by several UCO modules.
COMMENT_IMPORT_RE = re.compile(r"^\s*#\s*imports:\s+(\S+)\s*$", re.MULTILINE)
# ``owl:imports <IRI>`` or ``owl:imports prefix:local , ... ;``
OWL_IMPORTS_BLOCK_RE = re.compile(
    r"owl:imports\s+((?:.|\n)*?)\s*;",
    re.MULTILINE,
)
IRI_OR_CURIE_RE = re.compile(
    r"<(?P<iri>[^>]+)>|(?P<curie>[A-Za-z0-9_-]+:[A-Za-z0-9._/-]+)"
)
ONTOLOGY_IRI_RE = re.compile(
    r"<(?P<iri>https?://[^>]+)>\s*\n\s*a\s+owl:Ontology\b",
    re.MULTILINE,
)
CLASS_DECL_RE = re.compile(
    r"(?:^|\n)(?P<curie>[A-Za-z0-9_-]+:[A-Za-z0-9_-]+)\s+a\s+[^\n]*owl:Class",
    re.MULTILINE,
)
SUBCLASS_RE = re.compile(
    r"(?:^|\n)(?P<curie>[A-Za-z0-9_-]+:[A-Za-z0-9_-]+)\s+"
    r"(?:a[^\n]*owl:Class[^\n]*;\s*)?rdfs:subClassOf\s+(?P<parents>[^.]*)\.",
    re.MULTILINE,
)
HAS_FACET_RE = re.compile(
    r"has_facet\s*=\s*\[(.*?)\]",
    re.DOTALL,
)
FACET_NAME_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*(?:Facet))\b")
CLASS_TOKEN_RE = re.compile(r"\b([A-Z][A-Za-z0-9]{2,})\b")
PLUS_PATTERN_RE = re.compile(
    r"`?([A-Za-z][A-Za-z0-9]*(?:\s*\+\s*[A-Za-z][A-Za-z0-9]*){1,})`?"
)

SKIP_TTL_PARTS = (
    "/dependencies/",
    "\\dependencies\\",
    "/examples/",
    "\\examples\\",
    "/examples_knowledge_graphs/",
    "\\examples_knowledge_graphs\\",
    "/example_SPARQL_queries/",
    "\\example_SPARQL_queries\\",
    "/analytics_demonstration/",
    "\\analytics_demonstration\\",
    "/tests/",
    "\\tests\\",
    "/testing/",
    "\\testing\\",
    "/exemplars/",
    "\\exemplars\\",
)

SKIP_TTL_NAME_SUFFIXES = (
    "-example.ttl",
    "-skeleton.ttl",
    "-exemplar.ttl",
)

# Well-known namespace → logical module id used in the DAG.
NS_TO_MODULE = {
    "https://ontology.unifiedcyberontology.org/uco/core/": "uco.core",
    "https://ontology.unifiedcyberontology.org/uco/action/": "uco.action",
    "https://ontology.unifiedcyberontology.org/uco/analysis/": "uco.analysis",
    "https://ontology.unifiedcyberontology.org/uco/configuration/": "uco.configuration",
    "https://ontology.unifiedcyberontology.org/uco/identity/": "uco.identity",
    "https://ontology.unifiedcyberontology.org/uco/location/": "uco.location",
    "https://ontology.unifiedcyberontology.org/uco/marking/": "uco.marking",
    "https://ontology.unifiedcyberontology.org/uco/observable/": "uco.observable",
    "https://ontology.unifiedcyberontology.org/uco/pattern/": "uco.pattern",
    "https://ontology.unifiedcyberontology.org/uco/role/": "uco.role",
    "https://ontology.unifiedcyberontology.org/uco/time/": "uco.time",
    "https://ontology.unifiedcyberontology.org/uco/tool/": "uco.tool",
    "https://ontology.unifiedcyberontology.org/uco/types/": "uco.types",
    "https://ontology.unifiedcyberontology.org/uco/victim/": "uco.victim",
    "https://ontology.unifiedcyberontology.org/uco/vocabulary/": "uco.vocabulary",
    "https://ontology.caseontology.org/case/investigation/": "case.investigation",
    "https://ontology.caseontology.org/case/vocabulary/": "case.vocabulary",
    "https://cacontology.projectvic.org/core#": "ext.cac.cac-core",
    "https://cacontology.projectvic.org#": "ext.cac.cacontology",
    "http://purl.org/nemo/gufo#": "upper.gufo",
    "http://purl.obolibrary.org/obo/": "upper.bfo",
    "http://www.w3.org/ns/prov#": "upper.prov-o",
    "http://www.w3.org/2006/time#": "upper.owl-time",
    "http://www.opengis.net/ont/geosparql#": "upper.geosparql",
    "http://xmlns.com/foaf/0.1/": "upper.foaf",
    "http://www.w3.org/ns/org#": "upper.org",
    "http://www.w3.org/ns/dx/prof/": "upper.prof",
    "http://example.org/ontology/cryptoinv/": "ext.cryptoinv.cryptoinv",
    "http://example.org/ontology/toolcap/": "ext.toolcap.toolcap",
    "http://example.org/ontology/legalproc/": "ext.legalproc.legalproc",
    "http://example.org/ontology/rico/": "ext.rico.rico",
    "http://example.org/ontology/weap/": "ext.weapons.weap",
    "http://example.org/ontology/drug/": "ext.drugs.drug",
    "https://ontology.adversaryengagement.org/ae/": "ext.aeo",
    "https://ontology.solveit-df.org/solveit/": "ext.solveit",
}

CAC_SPINE_CLASSES = [
    {
        "name": "Entity",
        "iri": "https://cacontology.projectvic.org/core#Entity",
        "kind": "root",
        "comment": "Most general CAC spine class. Do not instantiate directly.",
        "parents": [],
    },
    {
        "name": "EnduringEntity",
        "iri": "https://cacontology.projectvic.org/core#EnduringEntity",
        "kind": "enduring",
        "comment": "Persists through time: people, orgs, devices, artifacts, places, results.",
        "parents": ["Entity", "gufo:Object", "uco-core:UcoObject"],
        "children": [
            "PersonLikeEntity",
            "OrganizationLikeEntity",
            "DigitalSystemEntity",
            "Artifact",
            "PlaceLikeEntity",
            "AssessmentResult",
        ],
    },
    {
        "name": "Occurrent",
        "iri": "https://cacontology.projectvic.org/core#Occurrent",
        "kind": "occurrent",
        "comment": "Things that happen or unfold in time. Do not instantiate directly.",
        "parents": ["Entity"],
        "children": ["Event"],
    },
    {
        "name": "Event",
        "iri": "https://cacontology.projectvic.org/core#Event",
        "kind": "occurrent",
        "comment": "Action, interaction, incident, hearing, or process step.",
        "parents": ["Occurrent", "gufo:Event"],
        "children": [
            "ExploitationEvent",
            "DetectionEvent",
            "CoordinationEvent",
            "SupportEvent",
            "LegalEvent",
            "InvestigativeAction",
        ],
    },
    {
        "name": "Situation",
        "iri": "https://cacontology.projectvic.org/core#Situation",
        "kind": "situation",
        "comment": "A context or configuration that holds at a time. Aligned to gUFO Situation.",
        "parents": ["Entity", "gufo:Situation"],
    },
    {
        "name": "Role",
        "iri": "https://cacontology.projectvic.org/core#Role",
        "kind": "role",
        "comment": "Non-rigid capacity borne by an enduring entity. Aligned to gUFO Role and UCO Role.",
        "parents": ["Entity", "gufo:Role", "uco-role:Role"],
    },
    {
        "name": "Phase",
        "iri": "https://cacontology.projectvic.org/core#Phase",
        "kind": "phase",
        "comment": "Temporal stage of an entity, process, or situation. Aligned to gUFO Phase.",
        "parents": ["Entity", "gufo:Phase"],
    },
]

UCO_CORE_HIERARCHY = [
    {
        "name": "UcoThing",
        "iri": "https://ontology.unifiedcyberontology.org/uco/core/UcoThing",
        "comment": "Root of the UCO class hierarchy (disjoint from UcoType in 1.5.0).",
    },
    {
        "name": "UcoObject",
        "iri": "https://ontology.unifiedcyberontology.org/uco/core/UcoObject",
        "comment": "Identified characterization of a concept. Parent of most instance classes.",
        "parent": "UcoThing",
    },
    {
        "name": "Facet",
        "iri": "https://ontology.unifiedcyberontology.org/uco/core/Facet",
        "comment": "Duck-typed property bundle attached via hasFacet. Never a top-level evidence item.",
        "parent": "UcoObject",
    },
    {
        "name": "Item",
        "iri": "https://ontology.unifiedcyberontology.org/uco/core/Item",
        "comment": "A distinct object that can be characterized by Facets.",
        "parent": "UcoObject",
    },
    {
        "name": "Relationship",
        "iri": "https://ontology.unifiedcyberontology.org/uco/core/Relationship",
        "comment": "Directed or undirected association between UcoObjects.",
        "parent": "UcoObject",
    },
    {
        "name": "UcoType",
        "iri": "https://ontology.unifiedcyberontology.org/uco/core/UcoType",
        "comment": "Metaclass anchor added in UCO 1.5.0; disjoint from UcoThing.",
    },
    {
        "name": "ObservableObject",
        "iri": "https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject",
        "comment": "Cyber-observable evidence carrier. Compose via hasFacet.",
        "parent": "Item",
    },
    {
        "name": "Action",
        "iri": "https://ontology.unifiedcyberontology.org/uco/action/Action",
        "comment": "Something that is done. Parent of InvestigativeAction.",
        "parent": "UcoObject",
    },
    {
        "name": "Investigation",
        "iri": "https://ontology.caseontology.org/case/investigation/Investigation",
        "comment": "CASE investigation container.",
        "parent": "UcoObject",
    },
    {
        "name": "InvestigativeAction",
        "iri": "https://ontology.caseontology.org/case/investigation/InvestigativeAction",
        "comment": "A discrete investigative step with instrument, object, and result.",
        "parent": "Action",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def strip_version_iri(iri: str) -> str:
    """Drop a trailing ``/1.5.0`` (or similar) so version IRIs collapse to modules."""
    return re.sub(r"/[0-9]+(?:\.[0-9]+)*$", "/", iri if iri.endswith("/") or "#" in iri else iri + "/")


def expand_curie(curie: str, prefixes: dict[str, str]) -> str | None:
    if ":" not in curie:
        return None
    prefix, local = curie.split(":", 1)
    base = prefixes.get(prefix)
    if not base:
        return None
    return base + local


def mermaid_id(module: str) -> str:
    """Mermaid node ids may only use [A-Za-z0-9_]."""
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", module)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if cleaned and cleaned[0].isdigit():
        cleaned = "n_" + cleaned
    return cleaned or "unknown"


def module_for_iri(iri: str) -> str:
    if iri in NS_TO_MODULE:
        return NS_TO_MODULE[iri]
    # Try stripping a trailing version.
    stripped = re.sub(r"/[0-9]+(?:\.[0-9]+)+/?$", "/", iri)
    if not stripped.endswith("/") and "#" not in stripped:
        stripped = stripped + "/"
    if stripped in NS_TO_MODULE:
        return NS_TO_MODULE[stripped]
    for ns, mod in NS_TO_MODULE.items():
        if iri.startswith(ns.rstrip("#").rstrip("/")):
            return mod
    # CAC domain modules.
    m = re.match(r"https://cacontology\.projectvic\.org/([^/#]+)", iri)
    if m:
        slug = m.group(1)
        if slug in {"core", "bridge"}:
            return f"ext.cac.cacontology-{slug}" if slug != "core" else "ext.cac.cac-core"
        return f"ext.cac.cacontology-{slug}"
    if "cacontology.projectvic.org" in iri:
        return "ext.cac.cacontology"
    if "solveit-df.org" in iri or "/solveit/" in iri:
        tail = iri.rstrip("/").split("/")[-1]
        if tail and tail != "solveit":
            return f"ext.solveit.{tail}"
        return "ext.solveit"
    if "adversaryengagement.org" in iri:
        tail = iri.rstrip("/").split("/")[-1]
        if tail and tail not in {"ae", "ontology"}:
            return f"ext.aeo.{tail}"
        return "ext.aeo"
    if "unifiedcyberontology.org/uco/" in iri:
        tail = iri.split("/uco/", 1)[-1].strip("/").split("/")[0]
        return f"uco.{tail}" if tail else "uco"
    if "caseontology.org/case/" in iri:
        tail = iri.split("/case/", 1)[-1].strip("/").split("/")[0]
        return f"case.{tail}" if tail else "case"
    if "w3.org/2002/07/owl" in iri:
        return "external.owl"
    if "w3.org/2000/01/rdf-schema" in iri:
        return "external.rdfs"
    if "w3.org/1999/02/22-rdf-syntax-ns" in iri:
        return "external.rdf"
    if "w3.org/2001/XMLSchema" in iri:
        return "external.xsd"
    if "w3.org/ns/shacl" in iri:
        return "external.shacl"
    return f"external.{iri}"


def family_of(module: str) -> str:
    if module.startswith("uco."):
        return "uco"
    if module.startswith("case."):
        return "case"
    if module.startswith("ext.cac"):
        return "cac"
    if module.startswith("ext.aeo"):
        return "aeo"
    if module.startswith("ext.solveit"):
        return "solveit"
    if module.startswith("ext."):
        return "sdk-extension"
    if module.startswith("upper."):
        return "upper"
    if module.startswith("external."):
        return "external"
    return "other"


def iter_ttl_files() -> list[Path]:
    roots = [REPO_ROOT / "ontology", REPO_ROOT / "extensions"]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.ttl"):
            posix = path.as_posix()
            if any(part in posix or part.replace("/", "\\") in str(path) for part in SKIP_TTL_PARTS):
                continue
            lower_name = path.name.lower()
            if any(lower_name.endswith(sfx) for sfx in SKIP_TTL_NAME_SUFFIXES):
                continue
            files.append(path)
    return sorted(files)


# ---------------------------------------------------------------------------
# Ontology DAG
# ---------------------------------------------------------------------------

def parse_ttl_imports(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    prefixes = {m.group(1): m.group(2) for m in PREFIX_RE.finditer(text)}
    ontology_iris = [m.group("iri") for m in ONTOLOGY_IRI_RE.finditer(text)]
    imported: list[str] = []
    for m in COMMENT_IMPORT_RE.finditer(text):
        imported.append(m.group(1).rstrip("."))
    for m in OWL_IMPORTS_BLOCK_RE.finditer(text):
        block = m.group(1)
        for token in IRI_OR_CURIE_RE.finditer(block):
            if token.group("iri"):
                imported.append(token.group("iri"))
            else:
                expanded = expand_curie(token.group("curie"), prefixes)
                if expanded:
                    imported.append(expanded)
    # Dedup, preserve order.
    seen: set[str] = set()
    unique: list[str] = []
    for iri in imported:
        if iri not in seen:
            seen.add(iri)
            unique.append(iri)
    return {
        "path": rel(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "prefixes": prefixes,
        "ontology_iris": ontology_iris,
        "imports": unique,
    }


def build_module_dag(ttl_records: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    edge_set: set[tuple[str, str]] = set()

    for rec in ttl_records:
        subject_mod: str | None = None
        posix = rec["path"]
        original_stem = Path(posix).stem
        is_shapes = original_stem.endswith("-shapes") or original_stem.endswith("-extended-shapes")
        stem = original_stem
        # Collapse SHACL companion files onto their OWL module.
        if stem.endswith("-extended-shapes"):
            stem = stem[: -len("-extended-shapes")]
        elif stem.endswith("-shapes"):
            stem = stem[: -len("-shapes")]
        if rec["ontology_iris"] and not is_shapes:
            subject_mod = module_for_iri(rec["ontology_iris"][0])
        if not subject_mod:
            if "/uco/" in posix:
                parts = posix.split("/uco/")[-1].split("/")
                subject_mod = f"uco.{parts[0]}" if parts else "uco"
            elif "/CASE/" in posix and "investigation" in posix:
                subject_mod = "case.investigation"
            elif "/cac/" in posix or "cacontology" in stem:
                slug = stem.replace("cacontology-", "")
                if slug in {"core-spine", "core"}:
                    subject_mod = "ext.cac.cac-core"
                else:
                    subject_mod = f"ext.cac.cacontology-{slug}"
            elif "/extensions/" in posix:
                ext_name = posix.split("/extensions/")[1].split("/")[0]
                subject_mod = f"ext.{ext_name}.{stem}"
            elif "/solveit/" in posix:
                subject_mod = f"ext.solveit.{stem}"
            elif "/aeo/" in posix:
                subject_mod = f"ext.aeo.{stem}"
            else:
                subject_mod = stem
        # Never keep raw IRIs as module ids.
        if subject_mod.startswith("external."):
            if "/extensions/" in posix:
                ext_name = posix.split("/extensions/")[1].split("/")[0]
                subject_mod = f"ext.{ext_name}.{stem}"
            elif "cacontology" in stem:
                subject_mod = f"ext.cac.{stem}"

        node = nodes.setdefault(
            subject_mod,
            {
                "id": subject_mod,
                "family": family_of(subject_mod),
                "ontology_iris": [],
                "files": [],
                "imports": [],
            },
        )
        node["files"].append({"path": rec["path"], "sha256": rec["sha256"], "bytes": rec["bytes"]})
        for iri in rec["ontology_iris"]:
            if iri not in node["ontology_iris"]:
                node["ontology_iris"].append(iri)
        for imp in rec["imports"]:
            target = module_for_iri(imp)
            if target == subject_mod:
                continue
            if target not in node["imports"]:
                node["imports"].append(target)
            key = (subject_mod, target)
            if key not in edge_set:
                edge_set.add(key)
                edges.append({"from": subject_mod, "to": target, "via": imp})

    # Collapse short aliases (``cryptoinv``) into their namespaced id
    # (``ext.cryptoinv.cryptoinv``) when the pairing is unambiguous.
    aliases = {}
    namespaced = [mid for mid in nodes if "." in mid]
    for mid in list(nodes):
        if "." in mid:
            continue
        matches = [n for n in namespaced if n.endswith("." + mid) or n.rsplit(".", 1)[-1] == mid]
        if len(matches) == 1:
            aliases[mid] = matches[0]
    if aliases:
        for old, new in aliases.items():
            src = nodes.pop(old)
            dest = nodes[new]
            dest["files"].extend(src["files"])
            for iri in src["ontology_iris"]:
                if iri not in dest["ontology_iris"]:
                    dest["ontology_iris"].append(iri)
            for imp in src["imports"]:
                mapped = aliases.get(imp, imp)
                if mapped != new and mapped not in dest["imports"]:
                    dest["imports"].append(mapped)
        new_edges = []
        seen_e: set[tuple[str, str]] = set()
        for edge in edges:
            frm = aliases.get(edge["from"], edge["from"])
            to = aliases.get(edge["to"], edge["to"])
            if frm == to:
                continue
            key = (frm, to)
            if key in seen_e:
                continue
            seen_e.add(key)
            new_edges.append({"from": frm, "to": to, "via": edge["via"]})
        edges = new_edges
        for node in nodes.values():
            node["imports"] = [aliases.get(i, i) for i in node["imports"] if aliases.get(i, i) != node["id"]]

    # Topological-ish grouping.
    families = defaultdict(list)
    for mid, node in sorted(nodes.items()):
        families[node["family"]].append(mid)

    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_commit_hint": "see git rev-parse HEAD",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "families": {k: v for k, v in sorted(families.items())},
        "nodes": nodes,
        "edges": edges,
        "ttl_file_count": len(ttl_records),
        "ttl_files": [
            {"path": r["path"], "sha256": r["sha256"], "bytes": r["bytes"], "import_count": len(r["imports"])}
            for r in ttl_records
        ],
    }


def mermaid_for_dag(dag: dict[str, Any]) -> str:
    lines = [
        "```mermaid",
        "flowchart TB",
        "  subgraph UCO[\"UCO 1.5.0\"]",
    ]
    for mid in dag["families"].get("uco", []):
        lines.append(f"    {mermaid_id(mid)}[\"{mid}\"]")
    lines.append("  end")
    lines.append("  subgraph CASE[\"CASE 1.5.0\"]")
    for mid in dag["families"].get("case", []):
        lines.append(f"    {mermaid_id(mid)}[\"{mid}\"]")
    lines.append("  end")
    lines.append("  subgraph CAC[\"CAC 3.1.0 spine + modules\"]")
    # Spine first, then a collapsed "domain modules" node to keep the diagram readable.
    spine = [m for m in dag["families"].get("cac", []) if "cac-core" in m or m.endswith("cacontology")]
    domain = [m for m in dag["families"].get("cac", []) if m not in spine]
    for mid in spine:
        lines.append(f"    {mermaid_id(mid)}[\"{mid}\"]")
    if domain:
        lines.append(f"    cac_domain[\"{len(domain)} CAC domain modules\"]")
    lines.append("  end")
    lines.append("  subgraph EXT[\"SDK + vendored extensions\"]")
    for family in ("aeo", "solveit", "sdk-extension"):
        for mid in dag["families"].get(family, []):
            lines.append(f"    {mermaid_id(mid)}[\"{mid}\"]")
    lines.append("  end")
    lines.append("  subgraph UPPER[\"Upper-ontology profiles\"]")
    for mid in dag["families"].get("upper", []):
        lines.append(f"    {mermaid_id(mid)}[\"{mid}\"]")
    lines.append("  end")

    # Render only non-external edges. CAC domain modules collapse to cac_domain.
    spine_set = set(spine)
    domain_set = set(domain)
    rendered: set[tuple[str, str]] = set()
    for edge in dag["edges"]:
        src, dst = edge["from"], edge["to"]
        if family_of(src) == "external" or family_of(dst) == "external":
            continue
        src_id = "cac_domain" if src in domain_set else src
        dst_id = "cac_domain" if dst in domain_set else dst
        if src_id == dst_id:
            continue
        key = (src_id, dst_id)
        if key in rendered:
            continue
        rendered.add(key)
        lines.append(f"  {mermaid_id(src_id)} --> {mermaid_id(dst_id)}")
    lines.append("```")
    return "\n".join(lines)


def mermaid_uco_detail(dag: dict[str, Any]) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for edge in dag["edges"]:
        if family_of(edge["from"]) != "uco" or family_of(edge["to"]) != "uco":
            continue
        s = mermaid_id(edge["from"])
        d = mermaid_id(edge["to"])
        lines.append(f"  {s}[\"{edge['from']}\"] --> {d}[\"{edge['to']}\"]")
    lines.append("```")
    return "\n".join(lines)


def mermaid_spine() -> str:
    return "\n".join(
        [
            "```mermaid",
            "flowchart TB",
            "  Entity[\"cac-core:Entity\"]",
            "  Entity --> Enduring[\"EnduringEntity\"]",
            "  Entity --> Occurrent[\"Occurrent\"]",
            "  Entity --> Situation[\"Situation\"]",
            "  Entity --> Role[\"Role\"]",
            "  Entity --> Phase[\"Phase\"]",
            "  Enduring --> Person[\"PersonLikeEntity\"]",
            "  Enduring --> Org[\"OrganizationLikeEntity\"]",
            "  Enduring --> Digital[\"DigitalSystemEntity\"]",
            "  Enduring --> Artifact[\"Artifact ≡ ObservableObject\"]",
            "  Enduring --> Place[\"PlaceLikeEntity\"]",
            "  Enduring --> Assessment[\"AssessmentResult\"]",
            "  Occurrent --> Event[\"Event\"]",
            "  Event --> Exploitation[\"ExploitationEvent\"]",
            "  Event --> Detection[\"DetectionEvent\"]",
            "  Event --> Coordination[\"CoordinationEvent\"]",
            "  Event --> Support[\"SupportEvent\"]",
            "  Event --> Legal[\"LegalEvent\"]",
            "  Event --> Investigative[\"InvestigativeAction ≡ CASE InvestigativeAction\"]",
            "```",
        ]
    )


# ---------------------------------------------------------------------------
# Class / facet inventory
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def collect_registries() -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = []
    candidates = [
        REPO_ROOT / "python" / "case_uco" / "_registry.json",
        REPO_ROOT / "ontology" / "cac" / "_registry.json",
        REPO_ROOT / "ontology" / "aeo" / "_registry.json",
        REPO_ROOT / "ontology" / "solveit" / "_registry.json",
    ]
    for ext_dir in (REPO_ROOT / "extensions").glob("*"):
        reg = ext_dir / "_registry.json"
        if reg.exists():
            candidates.append(reg)
    for pkg in (REPO_ROOT / "packages").glob("case-uco-*/**/*_registry.json"):
        candidates.append(pkg)
    seen: set[str] = set()
    for path in candidates:
        key = rel(path)
        if key in seen or not path.exists():
            continue
        seen.add(key)
        data = load_json(path)
        if data:
            found.append((key, data))
    return found


def build_inventory(registries: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    # Prefer the generated Python core registry (already merges extensions when generated).
    primary_path, primary = registries[0] if registries else ("", {"classes": {}, "modules": []})
    for path, data in registries:
        if path.endswith("python/case_uco/_registry.json"):
            primary_path, primary = path, data
            break

    per_module: dict[str, dict[str, Any]] = {}
    classes = primary.get("classes", {})
    for name, info in classes.items():
        module = info.get("module") or "unknown"
        bucket = per_module.setdefault(
            module,
            {
                "module": module,
                "family": family_of(module),
                "class_count": 0,
                "facet_count": 0,
                "classes": [],
                "facets": [],
            },
        )
        bucket["class_count"] += 1
        bucket["classes"].append(name)
        if info.get("is_facet") or name.endswith("Facet"):
            bucket["facet_count"] += 1
            bucket["facets"].append(name)

    for bucket in per_module.values():
        bucket["classes"].sort()
        bucket["facets"].sort()

    family_totals: dict[str, dict[str, int]] = {}
    for bucket in per_module.values():
        fam = family_totals.setdefault(bucket["family"], {"modules": 0, "classes": 0, "facets": 0})
        fam["modules"] += 1
        fam["classes"] += bucket["class_count"]
        fam["facets"] += bucket["facet_count"]

    return {
        "schema_version": "1.0.0",
        "primary_registry": primary_path,
        "registries_consulted": [p for p, _ in registries],
        "totals": {
            "modules": len(per_module),
            "classes": len(classes),
            "facets": sum(1 for n, i in classes.items() if i.get("is_facet") or n.endswith("Facet")),
            "vocabs": len(primary.get("vocabs", {})),
        },
        "family_totals": family_totals,
        "per_module": dict(sorted(per_module.items())),
        "all_facets": sorted(
            name for name, info in classes.items() if info.get("is_facet") or name.endswith("Facet")
        ),
    }


# ---------------------------------------------------------------------------
# Recipe composition patterns
# ---------------------------------------------------------------------------

def ast_assign_list(tree: ast.AST, name: str) -> list[Any]:
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        return []
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            if node.value is None:
                return []
            try:
                return ast.literal_eval(node.value)
            except Exception:
                return []
    return []


def load_domain_index_lists() -> dict[str, list[Any]]:
    if not DOMAIN_INDEX.exists():
        return {}
    src = DOMAIN_INDEX.read_text(encoding="utf-8")
    tree = ast.parse(src)
    return {
        "RECIPE_INDEX": ast_assign_list(tree, "RECIPE_INDEX"),
        "MAPPING_GUIDE_INDEX": ast_assign_list(tree, "MAPPING_GUIDE_INDEX"),
        "CORE_PATTERNS": ast_assign_list(tree, "CORE_PATTERNS"),
        "TASK_TO_CLASSES": None,  # dict, handled below
    }


def load_task_to_classes() -> dict[str, list[tuple[str, str]]]:
    if not DOMAIN_INDEX.exists():
        return {}
    src = DOMAIN_INDEX.read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        target_name = None
        value = None
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TASK_TO_CLASSES":
                    target_name = target.id
                    value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "TASK_TO_CLASSES":
                target_name = node.target.id
                value = node.value
        if target_name and value is not None:
            try:
                return ast.literal_eval(value)
            except Exception:
                return {}
    return {}


def recipe_files() -> list[Path]:
    skip = {"INDEX.md", "promotion-log.json", "recipe-execution.json", "recipe-execution.schema.json"}
    files = []
    for path in sorted(RECIPES_DIR.glob("*.md")):
        if path.name in skip or path.name.startswith("candidates"):
            continue
        files.append(path)
    return files


def extract_recipe_patterns(
    known_classes: set[str],
    known_facets: set[str],
    domain_lists: dict[str, list[Any]],
) -> dict[str, Any]:
    recipes: list[dict[str, Any]] = []
    facet_pair_counter: Counter[tuple[str, ...]] = Counter()
    facet_counter: Counter[str] = Counter()
    class_counter: Counter[str] = Counter()
    observable_facet_sets: dict[str, Counter[tuple[str, ...]]] = defaultdict(Counter)

    mapping_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in domain_lists.get("MAPPING_GUIDE_INDEX") or []:
        starter = entry.get("starter_kit") or ""
        if starter:
            mapping_by_file[starter.replace("\\", "/")].append(entry)

    recipe_index_by_file = {
        e.get("file", "").replace("\\", "/"): e for e in (domain_lists.get("RECIPE_INDEX") or [])
    }

    for path in recipe_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        posix = rel(path)
        facets_in_file = sorted({m.group(1) for m in FACET_NAME_RE.finditer(text) if m.group(1) in known_facets or m.group(1).endswith("Facet")})
        classes_in_file = sorted(
            {
                m.group(1)
                for m in CLASS_TOKEN_RE.finditer(text)
                if m.group(1) in known_classes
            }
        )
        facet_sets: list[list[str]] = []
        for block in HAS_FACET_RE.findall(text):
            names = [m.group(1) for m in FACET_NAME_RE.finditer(block)]
            if names:
                uniq = tuple(sorted(set(names)))
                facet_sets.append(list(uniq))
                facet_pair_counter[uniq] += 1
                for n in uniq:
                    facet_counter[n] += 1

        for cls in classes_in_file:
            class_counter[cls] += 1

        # Associate facet sets with nearby observable-like hosts.
        hosts = [c for c in classes_in_file if c in {
            "ObservableObject", "File", "RasterPicture", "Device", "EmailMessage",
            "MessageThread", "ApplicationAccount", "Disk", "Directory",
            "AppleUnifiedLogArchive", "EventRecord",
        }]
        for host in hosts:
            for fs in facet_sets:
                observable_facet_sets[host][tuple(fs)] += 1

        plus_patterns = []
        for m in PLUS_PATTERN_RE.finditer(text):
            raw = re.sub(r"\s+", "", m.group(1))
            parts = [p for p in raw.split("+") if p]
            if len(parts) >= 2 and any(p.endswith("Facet") or p in known_classes for p in parts):
                plus_patterns.append(" + ".join(parts))

        meta = recipe_index_by_file.get(posix, {})
        mappings = mapping_by_file.get(posix, [])
        recommended_from_mapping: list[str] = []
        for entry in mappings:
            recommended_from_mapping.extend(
                [c for c in entry.get("classes", []) if c.endswith("Facet")]
            )

        recipes.append(
            {
                "file": posix,
                "title": meta.get("title") or path.stem,
                "description": meta.get("description", ""),
                "keywords": meta.get("keywords", ""),
                "is_starter_kit": bool(meta.get("is_starter_kit")),
                "is_cac": path.name.startswith("cac-") or "cac ontology" in meta.get("keywords", "").lower(),
                "classes_mentioned": classes_in_file,
                "facets_mentioned": facets_in_file,
                "has_facet_sets": facet_sets,
                "plus_patterns": sorted(set(plus_patterns)),
                "mapping_patterns": [e.get("pattern") for e in mappings if e.get("pattern")],
                "recommended_facets": sorted(set(recommended_from_mapping)),
            }
        )

    # Recommended facet sets per major ObservableObject type, from recipes + mapping guide.
    recommended: dict[str, dict[str, Any]] = {}
    for host, counter in observable_facet_sets.items():
        top = counter.most_common(5)
        recommended[host] = {
            "observed_sets": [
                {"facets": list(facets), "recipe_occurrences": count} for facets, count in top
            ],
            "union_recommended": sorted({f for facets, _ in top for f in facets}),
        }

    # Seed well-known sets even if the counter is thin.
    defaults = {
        "File": ["FileFacet", "ContentDataFacet"],
        "ObservableObject": ["FileFacet", "ContentDataFacet"],
        "RasterPicture": ["FileFacet", "ContentDataFacet", "RasterPictureFacet", "EXIFFacet"],
        "Device": ["DeviceFacet", "OperatingSystemFacet"],
        "MobileDevice": ["DeviceFacet", "MobileDeviceFacet", "OperatingSystemFacet", "SIMCardFacet"],
        "EmailMessage": ["EmailMessageFacet", "EmailAddressFacet", "ContentDataFacet"],
        "Message": ["MessageFacet", "ApplicationFacet"],
        "Account": ["AccountFacet", "DigitalAccountFacet"],
        "NetworkConnection": ["NetworkConnectionFacet", "IPAddressFacet"],
        "DiskImage": ["ImageFacet", "FileFacet", "ContentDataFacet"],
    }
    for host, facets in defaults.items():
        recommended.setdefault(
            host,
            {"observed_sets": [{"facets": facets, "recipe_occurrences": 0}], "union_recommended": facets},
        )
        for f in facets:
            if f not in recommended[host]["union_recommended"]:
                recommended[host]["union_recommended"].append(f)
                recommended[host]["union_recommended"].sort()

    mapping_patterns = []
    for entry in domain_lists.get("MAPPING_GUIDE_INDEX") or []:
        mapping_patterns.append(
            {
                "source": entry.get("source"),
                "pattern": entry.get("pattern"),
                "classes": entry.get("classes", []),
                "facets": [c for c in entry.get("classes", []) if str(c).endswith("Facet")],
                "anti_patterns": entry.get("anti_patterns", []),
                "starter_kit": entry.get("starter_kit"),
                "code_skeleton": entry.get("code_skeleton"),
            }
        )

    task_patterns = []
    for task, pairs in load_task_to_classes().items():
        classes = [p[0] for p in pairs]
        task_patterns.append(
            {
                "task": task,
                "classes": classes,
                "facets": [c for c in classes if c.endswith("Facet")],
                "notes": {p[0]: p[1] for p in pairs},
            }
        )

    return {
        "schema_version": "1.0.0",
        "recipe_count": len(recipes),
        "recipes": recipes,
        "facet_frequency_across_recipes": facet_counter.most_common(),
        "class_frequency_across_recipes": class_counter.most_common(80),
        "cooccurring_facet_sets": [
            {"facets": list(k), "occurrences": v} for k, v in facet_pair_counter.most_common(40)
        ],
        "recommended_facet_sets": recommended,
        "mapping_guide_patterns": mapping_patterns,
        "task_to_classes_patterns": task_patterns,
        "core_patterns": domain_lists.get("CORE_PATTERNS") or [],
    }


# ---------------------------------------------------------------------------
# Markdown renderers
# ---------------------------------------------------------------------------

def render_dag_md(dag: dict[str, Any]) -> str:
    fam_lines = []
    for fam, mods in dag["families"].items():
        fam_lines.append(f"- **{fam}**: {len(mods)} modules")
    top_importers = sorted(
        dag["nodes"].values(),
        key=lambda n: len(n["imports"]),
        reverse=True,
    )[:15]
    importer_rows = "\n".join(
        f"| `{n['id']}` | {n['family']} | {len(n['imports'])} | {len(n['files'])} |"
        for n in top_importers
    )
    return f"""# Module dependency DAG

Observed `owl:imports` (and UCO `# imports:` comments) across vendored Turtle
files under `ontology/` and `extensions/`. Dependency edges are **from
importer → imported**. External W3C / SHACL / XSD IRIs are recorded in the
JSON but omitted from the diagrams.

Generated: `{dag['generated_at']}`

- Turtle files scanned: **{dag['ttl_file_count']}**
- Logical modules: **{dag['node_count']}**
- Import edges: **{dag['edge_count']}**

## Families

{chr(10).join(fam_lines)}

## High-level topology

{mermaid_for_dag(dag)}

## UCO module imports (detail)

{mermaid_uco_detail(dag)}

## CAC semantic spine

The Crimes Against Children Ontology organizes every domain class under
five kinds. Domain modules (grooming, forensics, trafficking, hotlines,
legal outcomes, …) **must** anchor to one of these rather than inventing
a parallel hierarchy.

{mermaid_spine()}

## Heaviest importers

| Module | Family | Imports | Files |
|---|---|---:|---:|
{importer_rows}

See `module-dependency-dag.json` for the full edge list, per-file SHA-256,
and unresolved external IRIs.
"""


def render_inventory_md(inv: dict[str, Any], recommended: dict[str, Any]) -> str:
    fam_rows = "\n".join(
        f"| {fam} | {vals['modules']} | {vals['classes']} | {vals['facets']} |"
        for fam, vals in sorted(inv["family_totals"].items())
    )
    # Show modules with the most classes.
    top = sorted(inv["per_module"].values(), key=lambda b: b["class_count"], reverse=True)[:25]
    top_rows = "\n".join(
        f"| `{b['module']}` | {b['family']} | {b['class_count']} | {b['facet_count']} |"
        for b in top
    )
    rec_sections = []
    for host, payload in sorted(recommended.items()):
        facets = ", ".join(f"`{f}`" for f in payload.get("union_recommended", []))
        rec_sections.append(f"- **{host}**: {facets}")
    return f"""# Class and Facet inventory

Source of truth: `{inv['primary_registry']}` (plus the extension registries
listed in the JSON). Counts include T-Box-only CAC classes that have no
dedicated SHACL shape — they are still registered so discovery works.

## Totals

| | Count |
|---|---:|
| Modules | {inv['totals']['modules']} |
| Classes | {inv['totals']['classes']} |
| Facets | {inv['totals']['facets']} |
| Vocabularies | {inv['totals']['vocabs']} |

## By family

| Family | Modules | Classes | Facets |
|---|---:|---:|---:|
{fam_rows}

## Largest modules

| Module | Family | Classes | Facets |
|---|---|---:|---:|
{top_rows}

## Recommended Facet sets (from recipes + mapping guide)

These are the Facet bundles investigators and agents should attach to the
named host type. They are **recommendations**, not SHACL requirements —
UCO's Facet pattern is deliberately open — but omitting them is the most
common modeling error in CAC and forensic graphs.

{chr(10).join(rec_sections)}

The JSON companion lists every class and Facet per module.
"""


def render_patterns_md(patterns: dict[str, Any]) -> str:
    cac = [r for r in patterns["recipes"] if r.get("is_cac")]
    starters = [r for r in patterns["recipes"] if r.get("is_starter_kit")]
    top_facets = patterns["facet_frequency_across_recipes"][:20]
    facet_rows = "\n".join(f"| `{name}` | {count} |" for name, count in top_facets)
    top_classes = patterns["class_frequency_across_recipes"][:20]
    class_rows = "\n".join(f"| `{name}` | {count} |" for name, count in top_classes)
    cooccur = patterns["cooccurring_facet_sets"][:15]
    co_rows = "\n".join(
        f"| {' + '.join('`' + f + '`' for f in row['facets'])} | {row['occurrences']} |"
        for row in cooccur
    )
    mapping_rows = "\n".join(
        f"| {e['source']} | `{e['pattern']}` | {', '.join('`' + f + '`' for f in e['facets'][:6])} |"
        for e in patterns["mapping_guide_patterns"][:25]
        if e.get("pattern")
    )
    recipe_rows = "\n".join(
        f"| [{r['title']}](../{r['file']}) | {'CAC' if r['is_cac'] else 'core'} | {len(r['classes_mentioned'])} | {len(r['facets_mentioned'])} |"
        for r in patterns["recipes"]
    )
    return f"""# Composition patterns observed in the recipe catalog

The SDK currently teaches composition through 77 recipes, the mapping
guide, `TASK_TO_CLASSES`, and a handful of `CORE_PATTERNS`. There is
**no first-class Composition Profile object** yet — that is the Phase 1
gap this study measures.

## Catalog size

| | Count |
|---|---:|
| Recipe files parsed | {patterns['recipe_count']} |
| Starter kits | {len(starters)} |
| CAC-series recipes | {len(cac)} |
| Mapping-guide sources | {len(patterns['mapping_guide_patterns'])} |
| Task-to-class mappings | {len(patterns['task_to_classes_patterns'])} |

## Dominant host classes (mentions across recipes)

| Class | Recipe files |
|---|---:|
{class_rows}

## Dominant Facets (mentions across recipes)

| Facet | Recipe files |
|---|---:|
{facet_rows}

## Co-occurring `has_facet=[...]` sets

These are the Facet bundles that already appear together in recipe code
samples. They are the empirical seed for Composition Profiles.

| Facet set | Occurrences |
|---|---:|
{co_rows}

## Mapping-guide composition patterns

| Source | Pattern | Facets |
|---|---|---|
{mapping_rows}

## Recurring logical patterns (not yet first-class)

1. **Observable + Facets** — one `ObservableObject` (or typed subclass such
   as `RasterPicture`) carries every Facet that describes the same real-world
   thing. Never one Observable per Facet.
2. **Action / instrument / object / result** — `InvestigativeAction` points
   at a `Tool`, the evidence it consumed, and the evidence it produced.
3. **Provenance + chain of custody** — `ProvenanceRecord` groups a
   transfer; CAC adds `ChainOfCustodyAction` / `EvidenceVerificationAction`
   as auditable steps.
4. **Role ≠ person** — CAC `Role` (victim, offender, examiner) is borne by
   an `EnduringEntity`; the person is not the role.
5. **Phase ≠ investigation** — grooming / investigation / recovery phases
   hang off the enduring process via `cac-core:hasPhase`.
6. **Hash intelligence** — `ContentDataFacet` + `Hash` is the integrity
   spine; PhotoDNA / perceptual hashes are referenced in CAC recipes
   (`ContentHashingTool`) but have no first-class Facet or VICS mapping.
7. **Cross-ontology composition** — CASE/UCO + CAC + legalproc/cryptoinv
   + one upper profile (gUFO preferred for CAC). Dual BFO+gUFO typing is
   an anti-pattern.

## Every recipe (class / Facet mention counts)

| Recipe | Series | Classes | Facets |
|---|---|---:|---:|
{recipe_rows}

See `composition-patterns.json` for the full per-recipe class lists,
`has_facet` sets, mapping-guide anti-patterns, and task mappings.
"""


def render_spine_and_layers() -> tuple[dict[str, Any], dict[str, Any]]:
    spine = {
        "schema_version": "1.0.0",
        "cac_spine": {
            "source": "ontology/cac/ontology/ontology/cacontology-core-spine.ttl",
            "version": "3.0.0",
            "upper_ontology": "gufo",
            "kinds": ["EnduringEntity", "Occurrent", "Situation", "Role", "Phase"],
            "classes": CAC_SPINE_CLASSES,
            "object_properties": [
                "hasPhase",
                "isPhaseOf",
                "assesses",
                "generatedBy",
                "usesMethod",
            ],
            "alignment": {
                "EnduringEntity": ["gufo:Object", "uco-core:UcoObject"],
                "Artifact": ["uco-observable:ObservableObject"],
                "Event": ["gufo:Event"],
                "InvestigativeAction": [
                    "case-investigation:InvestigativeAction",
                    "uco-action:Action",
                ],
                "Situation": ["gufo:Situation"],
                "Role": ["gufo:Role", "uco-role:Role"],
                "Phase": ["gufo:Phase"],
            },
        },
        "uco_core_hierarchy": UCO_CORE_HIERARCHY,
        "facet_pattern": {
            "host": "ObservableObject (or typed subclass)",
            "attachment": "uco-core:hasFacet",
            "rule": "One host per real-world thing; many Facets. Facets are never top-level evidence items.",
        },
    }
    layers = {
        "schema_version": "1.0.0",
        "framework": "Topology Articulation & Optimization Framework",
        "mission": (
            "Turn raw investigative material into validated, interoperable "
            "CASE/UCO + CAC knowledge graphs so children can be found and "
            "safeguarded faster, including in air-gapped environments."
        ),
        "observed_layers": [
            {
                "id": "ontology",
                "path": ["ontology/", "extensions/"],
                "role": "Vendored UCO / CASE / CAC / AEO / SOLVE-IT / upper profiles + SDK extensions.",
                "strengths": ["offline-first", "SHACL-backed", "CAC spine"],
                "bottlenecks": ["module/class explosion", "no first-class Composition Profiles"],
            },
            {
                "id": "generator",
                "path": ["generator/"],
                "role": "Parse OWL/TTL + SHACL → OntologySchema → typed builders + registry.",
                "strengths": ["single source of truth", "four-language emission"],
                "bottlenecks": ["full re-parse / re-generation cost", "no versioned IR"],
            },
            {
                "id": "runtime",
                "path": ["python/", "csharp/", "java/", "rust/"],
                "role": "CaseGraph + Facet duck-typing + Relationships + JSON-LD + required-field validation.",
                "strengths": ["facet flexibility", "cross-language parity"],
                "bottlenecks": [
                    "memory-bound SHACL on large graphs",
                    "no topology-aware partitioning",
                    "no first-class hash/VICS indexes",
                ],
            },
            {
                "id": "mcp",
                "path": ["mcp_server/"],
                "role": "Discovery, hybrid routing, 77 recipes, document processing, SHACL, critic, proposals.",
                "strengths": ["AI-agent readiness", "offline hybrid routing", "critic loop"],
                "bottlenecks": ["sequential tool use", "recipes are documents not executable DAGs"],
            },
            {
                "id": "knowledge",
                "path": ["docs/recipes/", "mcp_server/domain_index.py", "ONTOLOGY_REFERENCE.md"],
                "role": "Human/agent cookbook, task mappings, performance guidance.",
                "strengths": ["77 grounded recipes", "CAC series", "mapping guide"],
                "bottlenecks": ["cognitive load", "duplicated guidance vs. no profile object"],
            },
        ],
        "planned_layers": [
            "Phase 1 — Semantic Core Topology (Composition Profiles)",
            "Phase 2 — Generation Topology (IR + incremental generate + fluent helpers)",
            "Phase 3 — Runtime Topology (partitioning, indexes, PhotoDNA/VICS patterns)",
            "Phase 4 — Agent / Control Topology (recipe DAGs, InvestigationBuilder, inline critic)",
            "Phase 5 — Interop & Evolution Topology (VICS mappings, lenses, TOPOLOGY.md)",
        ],
    }
    return spine, layers


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print(f"Building topology artifacts from {REPO_ROOT}")
    ttl_files = iter_ttl_files()
    print(f"  scanning {len(ttl_files)} Turtle files")
    ttl_records = [parse_ttl_imports(p) for p in ttl_files]
    dag = build_module_dag(ttl_records)

    registries = collect_registries()
    print(f"  registries: {len(registries)}")
    inventory = build_inventory(registries)

    known_classes = set()
    known_facets = set(inventory["all_facets"])
    for bucket in inventory["per_module"].values():
        known_classes.update(bucket["classes"])

    domain_lists = load_domain_index_lists()
    print(f"  recipes: {len(list(recipe_files()))}")
    patterns = extract_recipe_patterns(known_classes, known_facets, domain_lists)

    spine, layers = render_spine_and_layers()

    write_json(TOPOLOGY / "module-dependency-dag.json", dag)
    write_text(TOPOLOGY / "module-dependency-dag.md", render_dag_md(dag))
    write_json(TOPOLOGY / "class-and-facet-inventory.json", inventory)
    write_text(
        TOPOLOGY / "class-and-facet-inventory.md",
        render_inventory_md(inventory, patterns["recommended_facet_sets"]),
    )
    write_json(TOPOLOGY / "composition-patterns.json", patterns)
    write_text(TOPOLOGY / "composition-patterns.md", render_patterns_md(patterns))
    write_json(TOPOLOGY / "semantic-spine.json", spine)
    write_json(TOPOLOGY / "sdk-layers.json", layers)

    print("Wrote:")
    for path in sorted(TOPOLOGY.glob("*.json")) + sorted(TOPOLOGY.glob("*.md")):
        if path.name == "README.md":
            continue
        print(f"  {rel(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
