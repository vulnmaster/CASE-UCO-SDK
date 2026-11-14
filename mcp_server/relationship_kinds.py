"""Machine-readable relationship-kind registry and lint (CQ-40)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "relationship_kinds.json"

OBSERVABLE_NS = "https://ontology.unifiedcyberontology.org/uco/observable/"
OBSERVABLE_RELATIONSHIP = OBSERVABLE_NS + "ObservableRelationship"
_DEFAULT_PREFIXES = {"uco-observable": OBSERVABLE_NS}


@lru_cache(maxsize=1)
def load_relationship_kind_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def known_relationship_kinds(*, vocab: str | None = None) -> frozenset[str]:
    reg = load_relationship_kind_registry()
    vocabs = reg.get("vocabularies") or {}
    if vocab:
        entry = vocabs.get(vocab) or {}
        return frozenset(entry.get("kinds") or [])
    kinds: set[str] = set()
    for entry in vocabs.values():
        kinds.update(entry.get("kinds") or [])
    return frozenset(kinds)


def vocabulary_names() -> list[str]:
    return sorted((load_relationship_kind_registry().get("vocabularies") or {}).keys())


def unknown_kind_message(kind: str) -> str:
    return f"kindOfRelationship {kind!r} is not in {' / '.join(vocabulary_names())}"


def is_observable_type(iri: str) -> bool:
    """An observable object class (not a facet) in the UCO observable namespace."""
    return iri.startswith(OBSERVABLE_NS) and not iri.endswith("Facet")


def in_vocabulary_scope(types: set[str], endpoint_types: list[set[str]]) -> bool:
    """Whether a relationship's kind should come from the observable vocabulary.

    The registry's governance limits the vocabulary to ObservableRelationship
    edges: a node typed ``uco-observable:ObservableRelationship``, or a
    relationship whose every source and target is an observable object.
    Identity, legal-process and state-machine relationships use open kinds.
    """
    if OBSERVABLE_RELATIONSHIP in types:
        return True
    return bool(endpoint_types) and all(
        any(is_observable_type(t) for t in ts) for ts in endpoint_types
    )


def graph_uses_relationship_kinds(graph: dict[str, Any] | list[Any]) -> bool:
    """Return True when any node carries ``uco-core:kindOfRelationship``."""
    nodes: list[Any]
    if isinstance(graph, dict):
        nodes = list(graph.get("@graph") or [])
        if not nodes and "uco-core:kindOfRelationship" in graph:
            return True
    else:
        nodes = list(graph)
    return any(
        isinstance(node, dict) and node.get("uco-core:kindOfRelationship") is not None
        for node in nodes
    )


def lint_relationship_kinds(
    graph: dict[str, Any] | list[Any],
    *,
    allow_open_vocabulary: bool = True,
) -> dict[str, Any]:
    """Lint ``uco-core:kindOfRelationship`` values against the registry.

    When ``allow_open_vocabulary`` is True (UCO default), unknown kinds are
    reported as warnings rather than errors. Returns a structured report.
    """

    nodes: list[Any]
    if isinstance(graph, dict):
        nodes = list(graph.get("@graph") or [])
        if not nodes and ("@type" in graph or "uco-core:kindOfRelationship" in graph):
            nodes = [graph]
    else:
        nodes = list(graph)

    context = graph.get("@context") if isinstance(graph, dict) else None
    prefixes = dict(_DEFAULT_PREFIXES)
    if isinstance(context, dict):
        prefixes.update({k: v for k, v in context.items() if isinstance(v, str)})

    def expand(term: Any) -> str:
        text = str(term)
        prefix, sep, local = text.partition(":")
        if sep and not local.startswith("//") and prefix in prefixes:
            return prefixes[prefix] + local
        return text

    def types_of(node: dict[str, Any]) -> set[str]:
        raw = node.get("@type") or []
        return {expand(t) for t in (raw if isinstance(raw, list) else [raw])}

    by_id = {
        expand(node["@id"]): node
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("@id"), str)
    }

    def endpoint_types(node: dict[str, Any]) -> list[set[str]]:
        out: list[set[str]] = []
        for key in ("uco-core:source", "uco-core:target"):
            refs = node.get(key) or []
            for ref in refs if isinstance(refs, list) else [refs]:
                ref_id = ref.get("@id") if isinstance(ref, dict) else ref
                target = by_id.get(expand(ref_id)) if isinstance(ref_id, str) else None
                out.append(types_of(target) if target else set())
        return out

    known = known_relationship_kinds()
    findings: list[dict[str, Any]] = []
    checked = 0
    for node in nodes:
        if not isinstance(node, dict):
            continue
        kind = node.get("uco-core:kindOfRelationship")
        if kind is None:
            continue
        if not in_vocabulary_scope(types_of(node), endpoint_types(node)):
            continue
        checked += 1
        values = kind if isinstance(kind, list) else [kind]
        for value in values:
            if isinstance(value, dict):
                value = value.get("@value", value)
            text = str(value)
            if text in known:
                continue
            findings.append({
                "node_id": node.get("@id"),
                "kind": text,
                "severity": "warning" if allow_open_vocabulary else "error",
                "message": unknown_kind_message(text),
            })

    errors = [f for f in findings if f["severity"] == "error"]
    return {
        "ok": not errors,
        "checked": checked,
        "findings": findings,
        "known_kind_count": len(known),
        "registry": str(REGISTRY_PATH.name),
    }
