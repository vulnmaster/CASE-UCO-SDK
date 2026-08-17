"""Canonical graph view for deterministic critic rules (issue #75 Round 2).

Parses JSON-LD and Turtle via RDFLib, expands compact terms to IRIs, normalizes
scalar/list forms, and preserves JSON source maps for actionable findings.
Heuristics must use this API rather than substring type checks on compact JSON.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

ParseKind = Literal["jsonld", "turtle", "unknown"]
ParseStatus = Literal[
    "ok",
    "json_syntax_error",
    "rdf_parse_error",
    "unsupported_type",
    "empty",
    "too_large",
]

# Well-known prefixes (overridden by document @context when present).
DEFAULT_PREFIXES: dict[str, str] = {
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "uco-marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "case-vocabulary": "https://ontology.caseontology.org/case/vocabulary/",
    "legalproc": "https://ontology.caseontology.org/case/extension/legalproc/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
}

IRI_RELATIONSHIP = DEFAULT_PREFIXES["uco-core"] + "Relationship"
IRI_INVESTIGATION = DEFAULT_PREFIXES["case-investigation"] + "Investigation"
IRI_PERSON = DEFAULT_PREFIXES["uco-identity"] + "Person"
IRI_RELEVANT_AUTH = DEFAULT_PREFIXES["case-investigation"] + "relevantAuthorization"
IRI_SOURCE = DEFAULT_PREFIXES["uco-core"] + "source"
IRI_TARGET = DEFAULT_PREFIXES["uco-core"] + "target"
IRI_KIND = DEFAULT_PREFIXES["uco-core"] + "kindOfRelationship"
IRI_HAS_FACET = DEFAULT_PREFIXES["uco-core"] + "hasFacet"
IRI_NAME = DEFAULT_PREFIXES["uco-core"] + "name"
IRI_OBJECT = DEFAULT_PREFIXES["uco-core"] + "object"
IRI_ACTION_OBJECT = DEFAULT_PREFIXES["uco-action"] + "object"
IRI_ACTION_RESULT = DEFAULT_PREFIXES["uco-action"] + "result"
IRI_CONTENT_FACET = DEFAULT_PREFIXES["uco-observable"] + "ContentDataFacet"
IRI_HASH = DEFAULT_PREFIXES["uco-observable"] + "hash"
IRI_HASH_VALUE = DEFAULT_PREFIXES["uco-types"] + "hashValue"
IRI_FILE = DEFAULT_PREFIXES["uco-observable"] + "File"
IRI_OBSERVABLE = DEFAULT_PREFIXES["uco-observable"] + "ObservableObject"
IRI_DICT = DEFAULT_PREFIXES["uco-types"] + "Dictionary"
IRI_DICT_ENTRY_PROP = DEFAULT_PREFIXES["uco-types"] + "entry"
IRI_INVESTIGATIVE_ACTION = (
    DEFAULT_PREFIXES["case-investigation"] + "InvestigativeAction"
)
IRI_PERFORMER = DEFAULT_PREFIXES["uco-action"] + "performer"
IRI_INSTRUMENT = DEFAULT_PREFIXES["uco-action"] + "instrument"
IRI_OBJECT_MARKING = DEFAULT_PREFIXES["uco-core"] + "objectMarking"
IRI_PROVENANCE_RECORD = DEFAULT_PREFIXES["case-investigation"] + "ProvenanceRecord"
IRI_CONTEXTUAL_COMPILATION = DEFAULT_PREFIXES["uco-core"] + "ContextualCompilation"
IRI_ACCOUNT = DEFAULT_PREFIXES["uco-observable"] + "Account"
IRI_IMAGE = DEFAULT_PREFIXES["uco-observable"] + "Image"
IRI_RASTER = DEFAULT_PREFIXES["uco-observable"] + "RasterPicture"
IRI_HASH_METHOD = DEFAULT_PREFIXES["uco-types"] + "hashMethod"
IRI_TAG = DEFAULT_PREFIXES["uco-core"] + "tag"
IRI_DESCRIPTION = DEFAULT_PREFIXES["uco-core"] + "description"
IRI_ROLE = DEFAULT_PREFIXES["uco-identity"] + "Role"

MAX_GRAPH_BYTES = 50 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".json", ".jsonld", ".json-ld", ".ttl", ".turtle"}


@dataclass(frozen=True)
class SourceLocation:
    path: str | None = None
    json_pointer: str | None = None
    line: int | None = None


@dataclass
class CanonicalValue:
    raw: Any
    iris: tuple[str, ...] = ()
    literal: str | None = None


@dataclass
class CanonicalNode:
    iri: str
    types: frozenset[str]
    properties: dict[str, list[CanonicalValue]]
    location: SourceLocation
    raw_json: dict[str, Any] | None = None

    def has_type(self, *type_iris: str) -> bool:
        return any(t in self.types for t in type_iris)

    def values(self, prop_iri: str) -> list[CanonicalValue]:
        return list(self.properties.get(prop_iri) or [])

    def refs(self, prop_iri: str) -> list[str]:
        out: list[str] = []
        for value in self.values(prop_iri):
            out.extend(value.iris)
        return out

    def first_ref(self, prop_iri: str) -> str | None:
        refs = self.refs(prop_iri)
        return refs[0] if refs else None

    def literals(self, prop_iri: str) -> list[str]:
        return [v.literal for v in self.values(prop_iri) if v.literal is not None]


@dataclass
class RuleExecution:
    rule_id: str
    rule_version: str
    status: Literal["evaluated", "not_applicable", "skipped", "failed"]
    input_artifact_hash: str
    targets_examined: int = 0
    finding_ids: list[str] = field(default_factory=list)
    error_code: str | None = None
    required_for_scope: bool = True
    verifies_rule_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "status": self.status,
            "input_artifact_hash": self.input_artifact_hash,
            "targets_examined": self.targets_examined,
            "finding_ids": list(self.finding_ids),
            "error_code": self.error_code,
            "required_for_scope": self.required_for_scope,
            "verifies_rule_ids": list(self.verifies_rule_ids or [self.rule_id]),
        }


@dataclass
class CanonicalGraphView:
    path_name: str
    kind: ParseKind
    json_status: ParseStatus
    rdf_status: ParseStatus
    prefixes: dict[str, str]
    nodes: dict[str, CanonicalNode]
    top_level_order: list[str]
    rdf_graph: Graph | None
    raw_document: dict[str, Any] | None
    duplicate_json_keys: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def usable_for_heuristics(self) -> bool:
        if not self.nodes:
            return False
        if self.kind == "jsonld":
            return self.json_status == "ok" and self.rdf_status in {"ok", "rdf_parse_error"}
        return self.rdf_status == "ok"

    def get(self, iri: str) -> CanonicalNode | None:
        return self.nodes.get(iri)

    def iter_nodes(self) -> Iterable[CanonicalNode]:
        for iri in self.top_level_order:
            node = self.nodes.get(iri)
            if node:
                yield node
        # Include any embedded-only nodes not in top-level order
        seen = set(self.top_level_order)
        for iri, node in self.nodes.items():
            if iri not in seen:
                yield node

    def expand(self, term: str | None) -> str | None:
        if term is None:
            return None
        if term.startswith("http://") or term.startswith("https://") or term.startswith("urn:"):
            return term
        if "://" in term:
            return term
        if ":" in term:
            prefix, local = term.split(":", 1)
            base = self.prefixes.get(prefix) or DEFAULT_PREFIXES.get(prefix)
            if base:
                return base + local
        vocab = self.prefixes.get("@vocab")
        if vocab:
            return vocab + term
        return term


def load_canonical_graph(path: Path) -> CanonicalGraphView:
    suffix = path.suffix.lower()
    path_name = path.name
    if suffix not in SUPPORTED_EXTENSIONS:
        return CanonicalGraphView(
            path_name=path_name,
            kind="unknown",
            json_status="unsupported_type",
            rdf_status="unsupported_type",
            prefixes=dict(DEFAULT_PREFIXES),
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            errors=["unsupported_type"],
        )

    size = path.stat().st_size
    if size > MAX_GRAPH_BYTES:
        return CanonicalGraphView(
            path_name=path_name,
            kind="unknown",
            json_status="too_large",
            rdf_status="too_large",
            prefixes=dict(DEFAULT_PREFIXES),
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            errors=["too_large"],
        )

    if suffix in {".ttl", ".turtle"}:
        return _load_turtle(path)
    return _load_jsonld(path)


def load_canonical_jsonld_text(
    text: str, *, path_name: str = "memory.jsonld"
) -> CanonicalGraphView:
    """Build a canonical view from in-memory JSON-LD text.

    Applies the same size bound and offline remote-context policy as
    :func:`load_canonical_graph`. Does not read or write the filesystem.
    """
    if len(text.encode("utf-8")) > MAX_GRAPH_BYTES:
        return CanonicalGraphView(
            path_name=path_name,
            kind="jsonld",
            json_status="too_large",
            rdf_status="too_large",
            prefixes=dict(DEFAULT_PREFIXES),
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            errors=["too_large"],
        )
    return _load_jsonld_text(text, path_name=path_name)


def _load_jsonld(path: Path) -> CanonicalGraphView:
    path_name = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return CanonicalGraphView(
            path_name=path_name,
            kind="jsonld",
            json_status="json_syntax_error",
            rdf_status="rdf_parse_error",
            prefixes=dict(DEFAULT_PREFIXES),
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            errors=[type(exc).__name__],
        )
    return _load_jsonld_text(text, path_name=path_name)


def _load_jsonld_text(text: str, *, path_name: str) -> CanonicalGraphView:
    duplicate_keys: list[str] = []

    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in seen:
                duplicate_keys.append(key)
            seen.add(key)
            out[key] = value
        return out

    try:
        document = json.loads(text, object_pairs_hook=pairs_hook)
    except json.JSONDecodeError as exc:
        return CanonicalGraphView(
            path_name=path_name,
            kind="jsonld",
            json_status="json_syntax_error",
            rdf_status="rdf_parse_error",
            prefixes=dict(DEFAULT_PREFIXES),
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            duplicate_json_keys=duplicate_keys,
            errors=[type(exc).__name__],
        )

    if not isinstance(document, dict):
        return CanonicalGraphView(
            path_name=path_name,
            kind="jsonld",
            json_status="json_syntax_error",
            rdf_status="rdf_parse_error",
            prefixes=dict(DEFAULT_PREFIXES),
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            duplicate_json_keys=duplicate_keys,
            errors=["root_not_object"],
        )

    prefixes = _extract_prefixes(document.get("@context"))
    remote = _remote_context_urls(document.get("@context"))
    if remote:
        return CanonicalGraphView(
            path_name=path_name,
            kind="jsonld",
            json_status="ok",
            rdf_status="rdf_parse_error",
            prefixes=prefixes,
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=document,
            duplicate_json_keys=sorted(set(duplicate_keys)),
            errors=["critic_remote_context_disallowed:" + ",".join(remote[:5])],
        )

    nodes, order = _index_json_nodes(document, prefixes, path_name)

    rdf_graph: Graph | None = None
    rdf_status: ParseStatus = "ok"
    try:
        rdf_graph = Graph()
        # Offline: do not resolve remote contexts (already rejected above).
        rdf_graph.parse(data=json.dumps(document), format="json-ld")
        # Merge RDF-identified subjects not present in compact @graph
        _merge_rdf_subjects(rdf_graph, nodes, prefixes, path_name)
    except Exception as exc:  # noqa: BLE001
        rdf_status = "rdf_parse_error"
        errors = [f"rdf:{type(exc).__name__}"]
    else:
        errors = []

    json_status: ParseStatus = "ok" if nodes else "empty"
    return CanonicalGraphView(
        path_name=path_name,
        kind="jsonld",
        json_status=json_status,
        rdf_status=rdf_status,
        prefixes=prefixes,
        nodes=nodes,
        top_level_order=order,
        rdf_graph=rdf_graph,
        raw_document=document,
        duplicate_json_keys=sorted(set(duplicate_keys)),
        errors=errors,
    )


def _load_turtle(path: Path) -> CanonicalGraphView:
    path_name = path.name
    prefixes = dict(DEFAULT_PREFIXES)
    try:
        rdf_graph = Graph()
        rdf_graph.parse(path, format="turtle")
    except Exception as exc:  # noqa: BLE001
        return CanonicalGraphView(
            path_name=path_name,
            kind="turtle",
            json_status="ok",  # N/A
            rdf_status="rdf_parse_error",
            prefixes=prefixes,
            nodes={},
            top_level_order=[],
            rdf_graph=None,
            raw_document=None,
            errors=[type(exc).__name__],
        )

    nodes: dict[str, CanonicalNode] = {}
    order: list[str] = []
    subjects = sorted({str(s) for s in rdf_graph.subjects() if isinstance(s, URIRef)})
    for iri in subjects:
        types = frozenset(
            str(o)
            for o in rdf_graph.objects(URIRef(iri), RDF.type)
            if isinstance(o, URIRef)
        )
        props: dict[str, list[CanonicalValue]] = {}
        for pred, obj in rdf_graph.predicate_objects(URIRef(iri)):
            if pred == RDF.type:
                continue
            pred_iri = str(pred)
            value = _rdf_object_to_value(obj)
            props.setdefault(pred_iri, []).append(value)
        nodes[iri] = CanonicalNode(
            iri=iri,
            types=types,
            properties=props,
            location=SourceLocation(path=path_name),
            raw_json=None,
        )
        order.append(iri)

    return CanonicalGraphView(
        path_name=path_name,
        kind="turtle",
        json_status="ok",
        rdf_status="ok" if nodes else "empty",
        prefixes=prefixes,
        nodes=nodes,
        top_level_order=order,
        rdf_graph=rdf_graph,
        raw_document=None,
        errors=[],
    )


def _rdf_object_to_value(obj: Any) -> CanonicalValue:
    if isinstance(obj, URIRef):
        return CanonicalValue(raw=str(obj), iris=(str(obj),))
    return CanonicalValue(raw=obj, literal=str(obj))


def _extract_prefixes(context: Any) -> dict[str, str]:
    prefixes = dict(DEFAULT_PREFIXES)
    if context is None:
        return prefixes
    contexts = context if isinstance(context, list) else [context]
    for item in contexts:
        if not isinstance(item, dict):
            continue
        for key, value in item.items():
            if key == "@vocab" and isinstance(value, str):
                prefixes["@vocab"] = value
            elif isinstance(value, str) and not key.startswith("@"):
                prefixes[key] = value
            elif isinstance(value, dict) and isinstance(value.get("@id"), str):
                prefixes[key] = value["@id"]
    return prefixes



def _remote_context_urls(context: Any) -> list[str]:
    """Return remote @context / @import URLs that are not offline-vendored.

    Offline policy: only inline object contexts (and local file: URIs if ever
    registered) are allowed. HTTP(S) context URLs and @import are rejected.
    """

    remote: list[str] = []

    def walk(node: Any) -> None:
        if node is None:
            return
        if isinstance(node, str):
            if node.startswith(("http://", "https://")):
                remote.append(node)
            return
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if isinstance(node, dict):
            imp = node.get("@import")
            if isinstance(imp, str) and imp.startswith(("http://", "https://")):
                remote.append(imp)
            elif isinstance(imp, list):
                for item in imp:
                    if isinstance(item, str) and item.startswith(("http://", "https://")):
                        remote.append(item)
            for key, value in node.items():
                if key in {"@import"}:
                    continue
                # Nested context objects may still embed remote strings via lists
                if key == "@context":
                    walk(value)

    walk(context)
    # Deduplicate preserving order
    seen: set[str] = set()
    out: list[str] = []
    for url in remote:
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def lint_kind_of_relationship(
    view: "CanonicalGraphView",
    *,
    allow_open_vocabulary: bool = True,
) -> dict[str, Any]:
    """Lint kindOfRelationship via canonical graph (JSON-LD and Turtle)."""

    from relationship_kinds import known_relationship_kinds

    known = known_relationship_kinds()
    findings: list[dict[str, Any]] = []
    checked = 0
    for node in view.iter_nodes():
        values = node.literals(IRI_KIND)
        # Also accept IRI-typed kinds if any
        if not values:
            for cv in node.values(IRI_KIND):
                if cv.literal:
                    values.append(cv.literal)
                elif cv.iris:
                    values.extend(cv.iris)
        if not values:
            continue
        for text in values:
            checked += 1
            if text in known:
                continue
            findings.append({
                "node_id": node.iri,
                "kind": text,
                "severity": "warning" if allow_open_vocabulary else "error",
                "message": (
                    f"kindOfRelationship {text!r} is not in "
                    "ObservableObjectRelationshipVocab / ActionRelationshipVocab"
                ),
            })
    errors = [f for f in findings if f["severity"] == "error"]
    return {
        "ok": not errors,
        "checked": checked,
        "findings": findings,
        "known_kind_count": len(known),
    }


def _expand_term(term: Any, prefixes: dict[str, str]) -> str | None:
    if not isinstance(term, str):
        return None
    if term.startswith(("http://", "https://", "urn:")):
        return term
    if ":" in term:
        prefix, local = term.split(":", 1)
        base = prefixes.get(prefix) or DEFAULT_PREFIXES.get(prefix)
        if base:
            return base + local
    vocab = prefixes.get("@vocab")
    if vocab:
        return vocab + term
    return term


def _index_json_nodes(
    document: dict[str, Any],
    prefixes: dict[str, str],
    path_name: str,
) -> tuple[dict[str, CanonicalNode], list[str]]:
    graph = document.get("@graph")
    if isinstance(graph, list):
        raw_nodes = [n for n in graph if isinstance(n, dict)]
        pointer_prefix = "/@graph"
    elif "@type" in document or "@id" in document:
        raw_nodes = [document]
        pointer_prefix = ""
    else:
        return {}, []

    nodes: dict[str, CanonicalNode] = {}
    order: list[str] = []
    for index, raw in enumerate(raw_nodes):
        raw_iri = raw.get("@id")
        if not isinstance(raw_iri, str) or not raw_iri:
            # Placeholder anonymous — skip indexing by IRI
            continue
        iri = _expand_term(raw_iri, prefixes) or raw_iri
        pointer = f"{pointer_prefix}/{index}" if pointer_prefix else ""
        types_raw = raw.get("@type")
        type_list = types_raw if isinstance(types_raw, list) else [types_raw]
        types = frozenset(
            t
            for t in (_expand_term(x, prefixes) for x in type_list if x is not None)
            if t
        )
        props: dict[str, list[CanonicalValue]] = {}
        for key, value in raw.items():
            if key.startswith("@"):
                continue
            prop_iri = _expand_term(key, prefixes) or key
            props[prop_iri] = _normalize_values(value, prefixes)
        # Index embedded facets with @id under hasFacet
        for facet_val in props.get(IRI_HAS_FACET, []):
            for facet_iri in facet_val.iris:
                # Facet may be embedded dict in raw
                pass
        _index_embedded(raw, prefixes, nodes, path_name, pointer)

        nodes[iri] = CanonicalNode(
            iri=iri,
            types=types,
            properties=props,
            location=SourceLocation(path=path_name, json_pointer=pointer or None),
            raw_json=raw,
        )
        order.append(iri)
    return nodes, order


def _index_embedded(
    raw: dict[str, Any],
    prefixes: dict[str, str],
    nodes: dict[str, CanonicalNode],
    path_name: str,
    pointer: str,
) -> None:
    """Index nested objects that carry @id (e.g. inline facets)."""

    for key, value in raw.items():
        if key.startswith("@"):
            continue
        items = value if isinstance(value, list) else [value]
        for i, item in enumerate(items):
            if not isinstance(item, dict) or not isinstance(item.get("@id"), str):
                continue
            iri = _expand_term(item["@id"], prefixes) or item["@id"]
            if iri in nodes:
                continue
            child_pointer = f"{pointer}/{key}/{i}" if pointer else f"/{key}/{i}"
            types_raw = item.get("@type")
            type_list = types_raw if isinstance(types_raw, list) else [types_raw]
            types = frozenset(
                t
                for t in (_expand_term(x, prefixes) for x in type_list if x is not None)
                if t
            )
            props: dict[str, list[CanonicalValue]] = {}
            for ck, cv in item.items():
                if ck.startswith("@"):
                    continue
                prop_iri = _expand_term(ck, prefixes) or ck
                props[prop_iri] = _normalize_values(cv, prefixes)
            nodes[iri] = CanonicalNode(
                iri=iri,
                types=types,
                properties=props,
                location=SourceLocation(path=path_name, json_pointer=child_pointer),
                raw_json=item,
            )
            _index_embedded(item, prefixes, nodes, path_name, child_pointer)


def _normalize_values(value: Any, prefixes: dict[str, str]) -> list[CanonicalValue]:
    items = value if isinstance(value, list) else [value]
    out: list[CanonicalValue] = []
    for item in items:
        if isinstance(item, dict):
            if isinstance(item.get("@id"), str):
                expanded = _expand_term(item["@id"], prefixes) or item["@id"]
                out.append(CanonicalValue(raw=item, iris=(expanded,)))
            elif "@value" in item:
                out.append(CanonicalValue(raw=item, literal=str(item["@value"])))
            else:
                out.append(CanonicalValue(raw=item))
        elif isinstance(item, str):
            expanded = _expand_term(item, prefixes)
            if item.startswith(("http://", "https://", "urn:", "kb:", "#")) or (
                ":" in item and item.split(":", 1)[0] in prefixes
            ):
                # Compact IRI-like string used as a reference
                out.append(
                    CanonicalValue(
                        raw=item,
                        iris=((expanded or item),),
                        literal=None,
                    )
                )
            else:
                out.append(CanonicalValue(raw=item, literal=item))
        else:
            out.append(CanonicalValue(raw=item, literal=str(item)))
    return out


def _merge_rdf_subjects(
    rdf_graph: Graph,
    nodes: dict[str, CanonicalNode],
    prefixes: dict[str, str],
    path_name: str,
) -> None:
    for subject in rdf_graph.subjects():
        if not isinstance(subject, URIRef):
            continue
        iri = str(subject)
        if iri in nodes:
            continue
        types = frozenset(
            str(o)
            for o in rdf_graph.objects(subject, RDF.type)
            if isinstance(o, URIRef)
        )
        props: dict[str, list[CanonicalValue]] = {}
        for pred, obj in rdf_graph.predicate_objects(subject):
            if pred == RDF.type:
                continue
            props.setdefault(str(pred), []).append(_rdf_object_to_value(obj))
        nodes[iri] = CanonicalNode(
            iri=iri,
            types=types,
            properties=props,
            location=SourceLocation(path=path_name),
            raw_json=None,
        )


def collect_object_iris_from_rdf(view: CanonicalGraphView) -> set[str]:
    """Return IRIs that appear in RDF object position (true references)."""

    if view.rdf_graph is None:
        # Fall back to JSON @id positions only
        iris: set[str] = set()
        for node in view.nodes.values():
            for values in node.properties.values():
                for value in values:
                    iris.update(value.iris)
        return iris

    out: set[str] = set()
    for _s, _p, obj in view.rdf_graph:
        if isinstance(obj, URIRef):
            out.add(str(obj))
    return out
