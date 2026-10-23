"""Deterministic node identifiers and IRI references.

``deterministic_id`` mints the same ``kb:ClassName-<uuid>`` for the same key on
every run, so re-ingesting a report, or a second report of the same evidence,
produces nodes that merge instead of duplicating. The suffix is a UUIDv5, which
keeps the UUID-shaped IRIs ``case_validate`` expects.

``Ref`` points a property at a node by IRI when you hold the IRI rather than
the Python instance (a node loaded from another file, or one minted with
``deterministic_id`` in an earlier run).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

__all__ = [
    "SDK_ID_NAMESPACE",
    "Ref",
    "deterministic_id",
    "deterministic_uuid",
]

SDK_ID_NAMESPACE = uuid.UUID("b659737f-9839-4767-be30-2c9a4af46b9e")

_PART_SEPARATOR = "\x1f"


class Ref(str):
    """A node reference by IRI, serialized as ``{"@id": ...}``.

    Accepts a compact IRI (``kb:File-...``) or an absolute IRI. ``rdflib``
    ``URIRef`` values are treated the same way.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return f"Ref({str.__repr__(self)})"


def _key_part(part: Any) -> str:
    if isinstance(part, datetime):
        return part.isoformat()
    if isinstance(part, (bytes, bytearray, memoryview)):
        return bytes(part).hex().upper()
    if isinstance(part, type):
        return part.__name__
    return str(part)


def deterministic_uuid(*parts: Any, namespace: uuid.UUID = SDK_ID_NAMESPACE) -> uuid.UUID:
    """Return a UUIDv5 over ``parts``.

    Parts are joined with an ASCII unit separator, so ``("a|b", "c")`` and
    ``("a", "b|c")`` differ. Normalize values before passing them in (for
    example upper-case hex digests) so the same fact always yields the same key.
    """

    if not parts:
        raise ValueError("deterministic_uuid needs at least one key part")
    return uuid.uuid5(namespace, _PART_SEPARATOR.join(_key_part(p) for p in parts))


def deterministic_id(
    cls: type | str,
    *parts: Any,
    prefix: str = "kb",
    namespace: uuid.UUID = SDK_ID_NAMESPACE,
) -> str:
    """Return ``{prefix}:{ClassName}-{uuid5}`` for a class and key parts.

    The class name is part of the key, so a ``File`` and a ``ContentData``
    built from the same digest get different IRIs. Pass an organization-specific
    ``namespace`` when IDs must not coincide with another producer's.
    """

    name = cls if isinstance(cls, str) else cls.__name__
    return f"{prefix}:{name}-{deterministic_uuid(name, *parts, namespace=namespace)}"
