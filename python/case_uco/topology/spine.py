"""Queryable CAC semantic spine and UCO core hierarchy."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from case_uco.topology.paths import topology_file


@dataclass(frozen=True)
class SpineKind:
    name: str
    iri: str
    kind: str
    comment: str
    parents: tuple[str, ...] = ()
    children: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "iri": self.iri,
            "kind": self.kind,
            "comment": self.comment,
            "parents": list(self.parents),
            "children": list(self.children),
        }


@lru_cache(maxsize=1)
def get_semantic_spine() -> dict[str, Any]:
    """Return the CAC spine + UCO hierarchy document.

    Prefers ``topology/semantic-spine.json`` written by Phase 0. Falls back
    to a minimal in-process copy so an installed wheel still answers queries
    offline if the checkout is not present.
    """
    path = topology_file("semantic-spine.json")
    if path is not None:
        return json.loads(path.read_text(encoding="utf-8"))
    return _FALLBACK_SPINE


def list_spine_kinds() -> list[SpineKind]:
    spine = get_semantic_spine()
    kinds: list[SpineKind] = []
    for raw in spine.get("cac_spine", {}).get("classes", []):
        kinds.append(
            SpineKind(
                name=raw["name"],
                iri=raw.get("iri", ""),
                kind=raw.get("kind", ""),
                comment=raw.get("comment", ""),
                parents=tuple(raw.get("parents") or []),
                children=tuple(raw.get("children") or []),
            )
        )
    return kinds


def spine_kind_for_class(name: str) -> dict[str, Any] | None:
    """Return the spine class whose name matches, plus its kind.

    This is a direct name lookup on the spine document, not a full
    subclass walk of the generated registry (that arrives in later phases
    via the IR).
    """
    key = name.split(":")[-1].lower()
    for kind in list_spine_kinds():
        if kind.name.lower() == key:
            return kind.as_dict()
    return None


_FALLBACK_SPINE: dict[str, Any] = {
    "schema_version": "1.0.0",
    "cac_spine": {
        "kinds": ["EnduringEntity", "Occurrent", "Situation", "Role", "Phase"],
        "classes": [
            {
                "name": "EnduringEntity",
                "iri": "https://cacontology.projectvic.org/core#EnduringEntity",
                "kind": "enduring",
                "comment": "Persists through time.",
                "parents": ["Entity"],
            },
            {
                "name": "Occurrent",
                "iri": "https://cacontology.projectvic.org/core#Occurrent",
                "kind": "occurrent",
                "comment": "Unfolds in time.",
                "parents": ["Entity"],
            },
            {
                "name": "Situation",
                "iri": "https://cacontology.projectvic.org/core#Situation",
                "kind": "situation",
                "comment": "A holding context.",
                "parents": ["Entity"],
            },
            {
                "name": "Role",
                "iri": "https://cacontology.projectvic.org/core#Role",
                "kind": "role",
                "comment": "Non-rigid capacity.",
                "parents": ["Entity"],
            },
            {
                "name": "Phase",
                "iri": "https://cacontology.projectvic.org/core#Phase",
                "kind": "phase",
                "comment": "Temporal stage.",
                "parents": ["Entity"],
            },
        ],
    },
    "uco_core_hierarchy": [
        {"name": "UcoThing"},
        {"name": "UcoObject", "parent": "UcoThing"},
        {"name": "Facet", "parent": "UcoObject"},
        {"name": "ObservableObject", "parent": "Item"},
    ],
}
