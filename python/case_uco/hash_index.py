"""Method-aware content-hash index.

Keyed by normalized ``(hashMethod, hashValue)``. This module only indexes
hash literals already present on a graph. It does not classify content,
compute hashes, or interpret licensed catalog algorithms.
"""

from __future__ import annotations

from typing import Any, Iterable, Iterator

HASH_PROPERTY_KEYS = frozenset(
    {
        "uco-observable:hash",
        "uco-observable:hashes",
        "hash",
        "hashes",
    }
)
METHOD_KEYS = (
    "uco-types:hashMethod",
    "hashMethod",
    "uco-observable:hashMethod",
)
VALUE_KEYS = (
    "uco-types:hashValue",
    "hashValue",
    "uco-observable:hashValue",
)
_SKIP_KEYS = frozenset({"@id", "@type", "@context"})


def normalize_hash_method(method: str) -> str:
    """Canonical method key: trimmed, collapsed whitespace, upper case."""
    return " ".join(method.strip().split()).upper()


def normalize_hash_digest(digest: str) -> str:
    """Canonical digest key: whitespace stripped, lower-case, optional ``0x`` dropped."""
    compact = "".join(digest.split()).lower()
    if compact.startswith("0x"):
        compact = compact[2:]
    return compact


def lexical_value(raw: Any) -> str | None:
    """Return a string lexical form from a JSON-LD scalar or ``@value`` map."""
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict) and "@value" in raw:
        value = raw["@value"]
        if value is None:
            return None
        return str(value)
    return None


def _first_lexical(node: dict[str, Any], keys: Iterable[str]) -> str | None:
    for key in keys:
        if key in node:
            text = lexical_value(node[key])
            if text is not None:
                return text
    return None


def is_hash_entry(node: Any) -> bool:
    return (
        isinstance(node, dict)
        and _first_lexical(node, METHOD_KEYS) is not None
        and _first_lexical(node, VALUE_KEYS) is not None
    )


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _ref_id(node: Any) -> str | None:
    if isinstance(node, dict) and set(node.keys()) <= {"@id"}:
        ident = node.get("@id")
        if isinstance(ident, str) and ident:
            return ident
    return None


def iter_hash_entries(
    node: Any,
    *,
    by_id: dict[str, dict[str, Any]],
) -> Iterator[dict[str, Any]]:
    """Yield Hash-shaped maps reachable from ``node``, resolving ``{"@id"}`` refs."""
    if isinstance(node, list):
        for item in node:
            yield from iter_hash_entries(item, by_id=by_id)
        return
    if not isinstance(node, dict):
        return
    if is_hash_entry(node):
        yield node
        return
    for key, value in node.items():
        if key in _SKIP_KEYS:
            continue
        if key in HASH_PROPERTY_KEYS:
            for entry in _as_list(value):
                ref = _ref_id(entry)
                if ref is not None:
                    resolved = by_id.get(ref)
                    if resolved is not None and is_hash_entry(resolved):
                        yield resolved
                    continue
                yield from iter_hash_entries(entry, by_id=by_id)
            continue
        yield from iter_hash_entries(value, by_id=by_id)


def build_content_hash_index(
    objects: Iterable[dict[str, Any]],
) -> dict[tuple[str, str], list[dict[str, str]]]:
    """Build ``{(method, digest): [hits...]}`` from top-level JSON-LD objects.

    Each hit is attributed to the top-level object that carries the hash
    (or that references a standalone ``types:Hash`` node).
    """
    materialised = [obj for obj in objects if isinstance(obj, dict)]
    by_id = {
        ident: obj
        for obj in materialised
        if isinstance((ident := obj.get("@id")), str) and ident
    }
    index: dict[tuple[str, str], list[dict[str, str]]] = {}
    for obj in materialised:
        owner = obj.get("@id")
        if not isinstance(owner, str) or not owner:
            continue
        seen: set[tuple[str, str]] = set()
        for entry in iter_hash_entries(obj, by_id=by_id):
            method_raw = _first_lexical(entry, METHOD_KEYS)
            digest_raw = _first_lexical(entry, VALUE_KEYS)
            if method_raw is None or digest_raw is None:
                continue
            method = normalize_hash_method(method_raw)
            digest = normalize_hash_digest(digest_raw)
            if not method or not digest:
                continue
            key = (method, digest)
            if key in seen:
                continue
            seen.add(key)
            index.setdefault(key, []).append(
                {
                    "id": owner,
                    "method": method,
                    "digest": digest,
                }
            )
    return index


def nest_content_hash_index(
    index: dict[tuple[str, str], list[dict[str, str]]],
) -> dict[str, dict[str, list[dict[str, str]]]]:
    """Present the composite key as ``{method: {digest: [hits...]}}``."""
    nested: dict[str, dict[str, list[dict[str, str]]]] = {}
    for (method, digest), hits in index.items():
        nested.setdefault(method, {})[digest] = [dict(hit) for hit in hits]
    return nested
