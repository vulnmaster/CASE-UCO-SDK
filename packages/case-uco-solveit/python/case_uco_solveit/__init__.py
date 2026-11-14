"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — CASE/UCO SDK extension bindings.

Each module holds typed dataclasses that work with ``CASEGraph.create``.
Call :func:`register` (or ``case_uco.graph.discover_extension_class_providers()``)
so ``CASEGraph.from_jsonld`` rehydrates these types.
"""

from __future__ import annotations

import importlib

from case_uco_solveit._context import NAMESPACES

__version__ = "0.2.17"

MODULES: tuple[str, ...] = (
    "solveit_analysis",
    "solveit_core",
    "solveit_data",
    "solveit_observable",
    "solveit_tool_profile",
    "solveit_wa",
)

# Public so the case_uco.extensions entry point (and static analysis)
# can reference it: the SDK registry loader resolves this at runtime.
REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")


def classes() -> list[type]:
    """Every generated class; the ``case_uco.class_registry`` provider."""
    found: list[type] = []
    for name in MODULES:
        module = importlib.import_module(f"{__name__}.{name}")
        found.extend(getattr(module, cls_name) for cls_name in module.__all__)
    return found


def register() -> int:
    """Register the classes for typed ``CASEGraph.from_jsonld`` loading."""
    from case_uco.graph import register_extension_classes

    return register_extension_classes(classes(), source="solveit", context=NAMESPACES)


__all__ = ["MODULES", "NAMESPACES", "REGISTRY_PATH", "__version__", "classes", "register"]
