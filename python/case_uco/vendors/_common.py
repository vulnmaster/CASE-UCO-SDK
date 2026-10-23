"""Helpers shared by the vendor readers."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any


def shared_node(graph: Any, cls: type, *key: Any, extra_types: tuple[str, ...] = (), **kwargs: Any) -> Any:
    """Create a node shared across extractions once; later calls reference it."""
    from case_uco.ids import Ref, deterministic_id

    node_id = deterministic_id(cls, *key)
    if graph.contains(node_id):
        return Ref(node_id)
    node = graph.create(cls, id=node_id, **kwargs)
    for type_iri in extra_types:
        graph.add_type(node_id, type_iri)
    return node


def extension(file_name: str) -> str | None:
    suffix = PurePosixPath(file_name.replace("\\", "/")).suffix
    return suffix[1:].lower() if suffix else None


def strings(*values: str | None) -> list[str]:
    """The non-empty values, for properties typed ``list[str]`` such as ``fileName``."""
    return [v for v in values if v]
