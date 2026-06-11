"""Runtime ontology introspection — search and discover CASE/UCO classes from Python.

This module loads a pre-generated registry of all ontology classes, properties,
and vocabulary types so developers can explore what's available without leaving
their Python REPL or IDE.

Extension packages (e.g., case-uco-cac, case-uco-aeo) are auto-discovered via
Python entry points in the ``case_uco.extensions`` group and merged into the
search index.

    >>> from case_uco.registry import search, get_class
    >>> search("file")
    [{'name': 'File', 'module': 'uco.observable', ...}, ...]
    >>> get_class("FileFacet")
    {'iri': '...', 'module': 'uco.observable', 'properties': [...], ...}
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Any

_REGISTRY: dict[str, Any] | None = None
_CONCEPT_INDEX: dict[str, Any] | None = None

_logger = logging.getLogger(__name__)


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
        _discover_extensions()
    return _REGISTRY


def _discover_extensions() -> None:
    """Scan ``case_uco.extensions`` entry points and merge extension registries."""
    if _REGISTRY is None:
        return

    try:
        from importlib.metadata import entry_points
    except ImportError:
        return

    try:
        eps: Iterable[Any] = entry_points(group="case_uco.extensions")
    except TypeError:
        selected_eps = entry_points().get("case_uco.extensions")
        eps = selected_eps if selected_eps is not None else ()

    for ep in eps:
        try:
            registry_path_ref = ep.load()
            if isinstance(registry_path_ref, str):
                reg_path = Path(registry_path_ref)
            else:
                continue

            if not reg_path.exists():
                _logger.debug("Extension %s registry not found at %s", ep.name, reg_path)
                continue

            ext_reg = json.loads(reg_path.read_text(encoding="utf-8"))
            ext_name = ext_reg.get("extension", ep.name)

            merged_classes = 0
            for cls_name, cls_info in ext_reg.get("classes", {}).items():
                if cls_name not in _REGISTRY["classes"]:
                    cls_info["source"] = ext_name
                    _REGISTRY["classes"][cls_name] = cls_info
                    merged_classes += 1

            for mod in ext_reg.get("modules", []):
                if mod not in _REGISTRY["modules"]:
                    _REGISTRY["modules"].append(mod)

            if merged_classes > 0:
                _logger.debug("Merged %d classes from extension '%s'", merged_classes, ext_name)
        except Exception as exc:
            _logger.debug("Failed to load extension entry point %s: %s", ep.name, exc)


def _load_concepts() -> dict[str, Any]:
    global _CONCEPT_INDEX
    if _CONCEPT_INDEX is None:
        path = Path(__file__).parent / "_concept_index.json"
        if not path.exists():
            raise FileNotFoundError(
                f"Concept index not found at {path}."
            )
        _CONCEPT_INDEX = json.loads(path.read_text(encoding="utf-8"))
    return _CONCEPT_INDEX


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


def suggest_for_concept(concept: str) -> list[dict[str, Any]]:
    """Given a natural-language concept, return recommended classes with usage notes.

    Matches against keys and class lists in the concept index.  Each result
    contains *name*, *module* (from the registry when available), *pattern*,
    and *usage_note*.
    """
    idx = _load_concepts()
    reg = _load()
    q = concept.lower()

    results: list[dict[str, Any]] = []
    for key, entry in idx["concepts"].items():
        if q in key or any(q in cls.lower() for cls in entry["classes"]):
            for cls_name in entry["classes"]:
                cls_info = reg["classes"].get(cls_name, {})
                results.append({
                    "name": cls_name,
                    "module": cls_info.get("module", ""),
                    "pattern": entry["pattern"],
                    "usage_note": entry["usage_note"],
                })
            break  # return the first matching concept group

    return results


def suggest_facets(class_name: str) -> list[dict[str, Any]]:
    """Return Facet classes commonly paired with *class_name*.

    For Facet classes the result explains which ObservableObject type they
    attach to.  For non-Facet classes, the concept index is searched for
    facets commonly used together with that class.
    """
    idx = _load_concepts()
    reg = _load()
    name_lower = class_name.lower()

    cls_info = None
    for cname, cinfo in reg["classes"].items():
        if cname.lower() == name_lower:
            cls_info = (cname, cinfo)
            break

    results: list[dict[str, Any]] = []

    if cls_info and cls_info[1].get("is_facet"):
        results.append({
            "name": cls_info[0],
            "module": cls_info[1].get("module", ""),
            "note": "This is already a Facet — attach it to an ObservableObject via has_facet.",
        })
        return results

    for _key, entry in idx["concepts"].items():
        if name_lower in [c.lower() for c in entry["classes"]]:
            for c in entry["classes"]:
                ci = reg["classes"].get(c, {})
                if ci.get("is_facet"):
                    results.append({
                        "name": c,
                        "module": ci.get("module", ""),
                        "note": f"Commonly paired via pattern: {entry['pattern']}",
                    })
            if results:
                return results

    facets = find_facets()
    for f in facets:
        if name_lower in f["name"].lower():
            results.append({
                "name": f["name"],
                "module": f.get("module", ""),
                "note": "Name-matched Facet — check class details to confirm relevance.",
            })

    return results


def _edit_distance(a: str, b: str) -> int:
    """Compute Levenshtein distance between two strings."""
    if len(a) < len(b):
        return _edit_distance(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            curr.append(min(curr[j] + 1, prev[j + 1] + 1, prev[j] + cost))
        prev = curr
    return prev[-1]


def did_you_mean(query: str) -> list[str]:
    """Fuzzy-match *query* against all class names and deprecated terms.

    Returns up to 5 suggestions sorted by relevance (substring matches
    first, then by edit distance).
    """
    idx = _load_concepts()
    reg = _load()
    q = query.lower()

    deprecated = idx.get("deprecated_terms", {})
    if q in deprecated:
        replacement = deprecated[q]
        return [f"{replacement} (replaces deprecated '{query}')"]

    all_names = list(reg["classes"].keys())

    substring_matches = [n for n in all_names if q in n.lower()]
    if substring_matches:
        substring_matches.sort(key=lambda n: (len(n), n))
        return substring_matches[:5]

    scored = [(n, _edit_distance(q, n.lower())) for n in all_names]
    scored.sort(key=lambda pair: pair[1])
    threshold = max(3, len(q) // 2)
    return [n for n, d in scored[:5] if d <= threshold]


_MODELING_WARNINGS: dict[str, list[str]] = {
    "_facet": [
        "This is a Facet — attach it to an ObservableObject via has_facet, "
        "don't use it as a top-level graph object.",
    ],
    "Tool": [
        "Tool represents the instrument used (e.g., Autopsy, EnCase), not "
        "the evidence item. Use ObservableObject for evidence.",
    ],
    "Investigation": [
        "Investigation is the top-level container for a case. Typically only "
        "one per graph. Use InvestigativeAction for individual forensic steps.",
    ],
    "InvestigativeAction": [
        "InvestigativeAction represents a single forensic step. Link it to "
        "the Tool used, the input evidence, and the output results.",
    ],
    "Action": [
        "Action is a generic base class. Prefer InvestigativeAction for "
        "forensic workflows unless modeling non-investigative actions.",
    ],
    "Location": [
        "Location is not an ObservableObject. Attach LatLongCoordinatesFacet "
        "or SimpleAddressFacet to provide concrete location data.",
    ],
    "Identity": [
        "Identity is an abstract class. Use the identity module's concrete "
        "subclasses or an IdentityFacet on an ObservableObject.",
    ],
}


def modeling_warnings(class_name: str) -> list[str]:
    """Return modeling warnings for *class_name*.

    Checks for class-specific warnings and generic Facet warnings based on
    the registry's ``is_facet`` flag.
    """
    reg = _load()
    warnings: list[str] = []

    cls_info = None
    canonical_name = class_name
    for cname, cinfo in reg["classes"].items():
        if cname.lower() == class_name.lower():
            cls_info = cinfo
            canonical_name = cname
            break

    if cls_info and cls_info.get("is_facet"):
        warnings.extend(_MODELING_WARNINGS["_facet"])

    if canonical_name in _MODELING_WARNINGS:
        warnings.extend(_MODELING_WARNINGS[canonical_name])

    return warnings
