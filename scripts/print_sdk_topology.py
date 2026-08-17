#!/usr/bin/env python3
"""Print a compact, reproducible SDK topology / semantic-spine summary.

Reads vendored sources and the generated registry. Writes to stdout only.
This script never creates inventory files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SPINE_TTL = Path("ontology/cac/ontology/ontology/cacontology-core-spine.ttl")
REGISTRY_JSON = Path("python/case_uco/_registry.json")

# Hand-maintained compact set. Keep this list short; it is not an inventory.
# Event and Role also exist as UCO local names; the generated registry keeps
# the UCO record. Confirm those two from the CAC spine Turtle.
DOCUMENTED_SPINE = {
    "Entity": "https://cacontology.projectvic.org/core#Entity",
    "EnduringEntity": "https://cacontology.projectvic.org/core#EnduringEntity",
    "Occurrent": "https://cacontology.projectvic.org/core#Occurrent",
    "Event": "https://cacontology.projectvic.org/core#Event",
    "Situation": "https://cacontology.projectvic.org/core#Situation",
    "Role": "https://cacontology.projectvic.org/core#Role",
    "Phase": "https://cacontology.projectvic.org/core#Phase",
}

SPINE_REGISTRY_UNIQUE = {
    name: iri
    for name, iri in DOCUMENTED_SPINE.items()
    if name not in {"Event", "Role"}
}

DOCUMENTED_UCO_CORE = {
    "UcoThing": "https://ontology.unifiedcyberontology.org/uco/core/UcoThing",
    "UcoObject": "https://ontology.unifiedcyberontology.org/uco/core/UcoObject",
    "Facet": "https://ontology.unifiedcyberontology.org/uco/core/Facet",
    "UcoType": "https://ontology.unifiedcyberontology.org/uco/core/UcoType",
}

_OWL_CLASS = re.compile(r"cac-core:([A-Za-z][A-Za-z0-9]*)\s+a\s+owl:Class\b")


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "python" / "case_uco" / "_registry.json").is_file():
            return parent
    raise SystemExit("Could not locate repository root from scripts/print_sdk_topology.py")


def load_registry(root: Path) -> dict[str, Any]:
    path = root / REGISTRY_JSON
    return json.loads(path.read_text(encoding="utf-8"))


def extract_spine_classes(ttl_text: str) -> list[str]:
    seen: list[str] = []
    for match in _OWL_CLASS.finditer(ttl_text):
        name = match.group(1)
        if name not in seen:
            seen.append(name)
    return seen


def _classes_by_iri(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_iri: dict[str, dict[str, Any]] = {}
    for name, info in (registry.get("classes") or {}).items():
        if not isinstance(info, dict):
            continue
        iri = info.get("iri")
        if isinstance(iri, str):
            by_iri[iri] = {"local_name": name, **info}
    return by_iri


def _check_iris(
    registry: dict[str, Any], expected: dict[str, str]
) -> dict[str, dict[str, Any]]:
    by_iri = _classes_by_iri(registry)
    classes = registry.get("classes") or {}
    out: dict[str, dict[str, Any]] = {}
    for name, iri in expected.items():
        match = by_iri.get(iri)
        if match:
            out[name] = {
                "iri": iri,
                "in_registry": True,
                "module": match.get("module"),
                "registry_local_name": match.get("local_name"),
            }
            continue
        info = classes.get(name) if isinstance(classes.get(name), dict) else None
        out[name] = {
            "iri": iri,
            "in_registry": False,
            "registry_local_name": name if info else None,
            "registry_iri": None if info is None else info.get("iri"),
            "note": "local-name collision; confirm IRI in CAC spine Turtle",
        }
    return out


def build_summary(root: Path) -> dict[str, Any]:
    registry = load_registry(root)
    ttl_path = root / SPINE_TTL
    ttl_classes: list[str] | None = None
    if ttl_path.is_file():
        ttl_classes = extract_spine_classes(ttl_path.read_text(encoding="utf-8"))

    families = sorted(
        {
            module.split(".", 1)[0]
            for module in registry.get("modules") or []
            if isinstance(module, str) and module
        }
    )
    return {
        "documentation_only": True,
        "writes_files": False,
        "spine_ttl": str(SPINE_TTL) if ttl_path.is_file() else None,
        "spine_kinds": _check_iris(registry, DOCUMENTED_SPINE),
        "uco_core": _check_iris(registry, DOCUMENTED_UCO_CORE),
        "spine_ttl_class_count": None if ttl_classes is None else len(ttl_classes),
        "registry_module_families": families,
        "registry_module_count": len(registry.get("modules") or []),
    }


def missing_iris(summary: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for name, info in summary["uco_core"].items():
        if not info.get("in_registry"):
            missing.append(name)
    for name, info in summary["spine_kinds"].items():
        if name in {"Event", "Role"}:
            continue
        if not info.get("in_registry"):
            missing.append(name)
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print a compact topology/spine summary to stdout. Never writes files."
    )
    parser.parse_args(argv)

    root = repo_root()
    summary = build_summary(root)
    json.dump(summary, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    missing = missing_iris(summary)
    if missing:
        sys.stderr.write(
            "Documented classes missing from registry or IRI mismatch: "
            + ", ".join(missing)
            + "\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
