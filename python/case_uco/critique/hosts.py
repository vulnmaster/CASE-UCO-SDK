"""Host resolution for Facet-set / hash checks.

File bundle = ObservableObject or File that carries FileFacet.
Picture bundle = RasterPicture or Image.
There is no generated DiskImage type — do not require one.
"""

from __future__ import annotations

from typing import Any

_FILE_TYPES = {"File", "ObservableObject"}
_PICTURE_TYPES = {"RasterPicture", "Image"}
_TOOL_TYPES = {"Tool", "ConfiguredTool"}


def local_types(node: Any) -> set[str]:
    if node is None:
        return set()
    if isinstance(node, dict):
        raw = node.get("@type")
        items = raw if isinstance(raw, list) else [raw]
        return {_local(t) for t in items if t}
    if hasattr(node, "__class__"):
        names = {node.__class__.__name__}
        types = getattr(node, "types", None)
        if types:
            names.update(_local(t) for t in (types if isinstance(types, list) else [types]))
        return {n for n in names if n}
    return set()


def _local(term: Any) -> str:
    text = str(term)
    if "/" in text:
        text = text.rsplit("/", 1)[-1]
    if ":" in text:
        text = text.rsplit(":", 1)[-1]
    if "#" in text:
        text = text.rsplit("#", 1)[-1]
    return text


def facet_names(node: Any) -> set[str]:
    names: set[str] = set()
    facets = None
    if hasattr(node, "has_facet"):
        facets = node.has_facet
    elif isinstance(node, dict):
        facets = (
            node.get("uco-core:hasFacet")
            or node.get("hasFacet")
            or node.get("https://ontology.unifiedcyberontology.org/uco/core/hasFacet")
        )
    if not facets:
        return names
    items = facets if isinstance(facets, list) else [facets]
    for item in items:
        if hasattr(item, "__class__") and not isinstance(item, dict):
            names.add(item.__class__.__name__)
        elif isinstance(item, dict):
            names.update(local_types(item))
    return names


def resolve_host(node: Any, declared: str | None = None) -> str | None:
    """Map a created node to a Facet-set host name."""
    types = local_types(node)
    facets = facet_names(node)
    if types & _PICTURE_TYPES or declared in _PICTURE_TYPES:
        return "RasterPicture"
    if "FileFacet" in facets or declared in _FILE_TYPES or types & _FILE_TYPES:
        if types & {"File"} or declared == "File":
            return "File"
        return "File" if "FileFacet" in facets else (declared or next(iter(types), None))
    if types & _TOOL_TYPES or declared in _TOOL_TYPES:
        return "Tool"
    if declared and declared != "DiskImage":
        return declared
    if "DiskImage" in types:
        return "File"
    return next(iter(types), declared)


def host_matches(host: str | None, applies_to: tuple[str, ...]) -> bool:
    if not applies_to or "*" in applies_to:
        return True
    if host is None:
        return False
    if host in applies_to:
        return True
    if host == "File" and ("ObservableObject" in applies_to or "File" in applies_to):
        return True
    if host == "ObservableObject" and "File" in applies_to:
        return True
    if host == "RasterPicture" and ("Image" in applies_to or "RasterPicture" in applies_to):
        return True
    return False
