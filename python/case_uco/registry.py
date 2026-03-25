"""Runtime ontology introspection — search and discover CASE/UCO classes from Python.

This module loads a pre-generated registry of all ontology classes, properties,
and vocabulary types so developers can explore what's available without leaving
their Python REPL or IDE.

    >>> from case_uco.registry import search, get_class
    >>> search("file")
    [{'name': 'File', 'module': 'uco.observable', ...}, ...]
    >>> get_class("FileFacet")
    {'iri': '...', 'module': 'uco.observable', 'properties': [...], ...}
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_REGISTRY: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _REGISTRY
    if _REGISTRY is None:
        registry_path = Path(__file__).parent / "_registry.json"
        if not registry_path.exists():
            raise FileNotFoundError(
                f"Ontology registry not found at {registry_path}. "
                "Run 'case-uco-generate generate' to produce it."
            )
        _REGISTRY = json.loads(registry_path.read_text(encoding="utf-8"))
    return _REGISTRY


def search(query: str) -> list[dict[str, Any]]:
    """Search classes by substring match on name or description (case-insensitive).

    Returns a list of class info dicts sorted by module and name.
    """
    reg = _load()
    q = query.lower()
    results = []
    for name, info in reg["classes"].items():
        if q in name.lower() or q in info.get("description", "").lower():
            results.append({"name": name, **info})
    results.sort(key=lambda c: (c["module"], c["name"]))
    return results


def list_modules() -> list[str]:
    """Return all ontology module names."""
    return list(_load()["modules"])


def list_classes(module: str | None = None) -> list[str]:
    """Return class names, optionally filtered by module.

    The module parameter accepts partial names (e.g. "observable" matches
    "uco.observable").
    """
    reg = _load()
    names = []
    for name, info in reg["classes"].items():
        if module is None:
            names.append(name)
        else:
            m = module.lower()
            mod = info["module"].lower()
            if mod == m or mod.endswith(f".{m}"):
                names.append(name)
    return sorted(names)


def get_class(name: str) -> dict[str, Any] | None:
    """Look up a class by name (case-insensitive). Returns full info dict or None."""
    reg = _load()
    name_lower = name.lower()
    for cls_name, info in reg["classes"].items():
        if cls_name.lower() == name_lower:
            return {"name": cls_name, **info}
    return None


def find_by_property_type(type_name: str) -> list[dict[str, Any]]:
    """Find classes that have a property whose type matches type_name."""
    reg = _load()
    q = type_name.lower()
    results = []
    for name, info in reg["classes"].items():
        for prop in info.get("properties", []):
            if prop.get("type", "").lower() == q:
                results.append({"name": name, **info})
                break
    results.sort(key=lambda c: (c["module"], c["name"]))
    return results


def find_facets() -> list[dict[str, Any]]:
    """Return all Facet subclasses."""
    reg = _load()
    results = []
    for name, info in reg["classes"].items():
        if info.get("is_facet"):
            results.append({"name": name, **info})
    results.sort(key=lambda c: (c["module"], c["name"]))
    return results


def list_vocabs() -> list[dict[str, Any]]:
    """Return all vocabulary types with their members."""
    reg = _load()
    results = []
    for name, info in reg.get("vocabs", {}).items():
        results.append({"name": name, **info})
    results.sort(key=lambda v: v["name"])
    return results
