"""Discover and load Composition Profile guidance documents.

Profiles are investigator guidance, not ontology truth. This module only
reads local JSON; it does not change constructors, SHACL, or OWL.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

_SCHEMA_NAMES = frozenset({"profile.schema.json"})
_ENV_DIR = "CASE_UCO_PROFILES_DIR"


@dataclass(frozen=True)
class FacetSet:
    """Facet bundle recommended for one host class name."""

    host: str
    required: tuple[str, ...]
    recommended: tuple[str, ...]
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "required": list(self.required),
            "recommended": list(self.recommended),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class CompositionProfile:
    """One Composition Profile document.

    Field values are guidance for choosing existing modules and Facets.
    They are not new ontology requirements.
    """

    id: str
    version: str
    title: str
    description: str
    mission: str = ""
    air_gapped: bool = True
    required_modules: tuple[str, ...] = ()
    recommended_modules: tuple[str, ...] = ()
    facet_sets: tuple[FacetSet, ...] = ()
    spine_anchors: tuple[str, ...] = ()
    upper_ontology_profiles: tuple[str, ...] = ()
    related_recipes: tuple[str, ...] = ()
    recipe_skeleton: Mapping[str, Any] = field(default_factory=dict)
    keywords: tuple[str, ...] = ()
    source_path: str = ""

    def facet_set_for(self, host: str) -> FacetSet | None:
        key = host.lower()
        for item in self.facet_sets:
            if item.host.lower() == key:
                return item
        return None

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "title": self.title,
            "description": self.description,
            "mission": self.mission,
            "air_gapped": self.air_gapped,
            "required_modules": list(self.required_modules),
            "recommended_modules": list(self.recommended_modules),
            "facet_sets": {item.host: item.as_dict() for item in self.facet_sets},
            "spine_anchors": list(self.spine_anchors),
            "upper_ontology_profiles": list(self.upper_ontology_profiles),
            "related_recipes": list(self.related_recipes),
            "recipe_skeleton": dict(self.recipe_skeleton),
            "keywords": list(self.keywords),
            "source_path": self.source_path,
        }


def _unique_existing(paths: Iterable[Path]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for path in paths:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in seen or not path.is_dir():
            continue
        seen.add(resolved)
        out.append(path)
    return out


def profile_catalog_dirs() -> list[Path]:
    """Return existing directories that may contain profile JSON.

    Search order: ``CASE_UCO_PROFILES_DIR``, then ``topology/profiles``
    walking up from this file and the process cwd. Read-only.
    """
    candidates: list[Path] = []
    env = os.environ.get(_ENV_DIR)
    if env:
        candidates.append(Path(env))
    starts = [Path(__file__).resolve(), Path.cwd().resolve()]
    for start in starts:
        for parent in [start, *start.parents]:
            candidates.append(parent / "topology" / "profiles")
    return _unique_existing(candidates)


def default_catalog_dir() -> Path | None:
    dirs = profile_catalog_dirs()
    return dirs[0] if dirs else None


def _is_profile_document(path: Path) -> bool:
    name = path.name
    return path.suffix == ".json" and name not in _SCHEMA_NAMES and not name.endswith(".schema.json")


def _parse_profile(path: Path, raw: Mapping[str, Any]) -> CompositionProfile:
    facet_sets = []
    for host, spec in (raw.get("facet_sets") or {}).items():
        if not isinstance(spec, Mapping):
            continue
        facet_sets.append(
            FacetSet(
                host=str(host),
                required=tuple(str(item) for item in (spec.get("required") or [])),
                recommended=tuple(str(item) for item in (spec.get("recommended") or [])),
                notes=str(spec.get("notes") or ""),
            )
        )
    skeleton = raw.get("recipe_skeleton") or {}
    if not isinstance(skeleton, Mapping):
        skeleton = {}
    return CompositionProfile(
        id=str(raw["id"]),
        version=str(raw["version"]),
        title=str(raw["title"]),
        description=str(raw["description"]),
        mission=str(raw.get("mission") or ""),
        air_gapped=bool(raw.get("air_gapped", True)),
        required_modules=tuple(str(item) for item in (raw.get("required_modules") or [])),
        recommended_modules=tuple(str(item) for item in (raw.get("recommended_modules") or [])),
        facet_sets=tuple(facet_sets),
        spine_anchors=tuple(str(item) for item in (raw.get("spine_anchors") or [])),
        upper_ontology_profiles=tuple(str(item) for item in (raw.get("upper_ontology_profiles") or [])),
        related_recipes=tuple(str(item) for item in (raw.get("related_recipes") or [])),
        recipe_skeleton=dict(skeleton),
        keywords=tuple(str(item) for item in (raw.get("keywords") or [])),
        source_path=str(path),
    )


def load_profiles_from(directory: Path) -> list[CompositionProfile]:
    """Load profile documents from one local directory.

    Unreadable or non-object JSON files are skipped. Documents without an
    ``id`` are skipped. This function never opens a network resource.
    """
    loaded: list[CompositionProfile] = []
    if not directory.is_dir():
        return loaded
    for path in sorted(directory.glob("*.json")):
        if not _is_profile_document(path):
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeError):
            continue
        if not isinstance(raw, dict) or "id" not in raw:
            continue
        loaded.append(_parse_profile(path, raw))
    return loaded


@lru_cache(maxsize=1)
def _load_all() -> dict[str, CompositionProfile]:
    loaded: dict[str, CompositionProfile] = {}
    for directory in profile_catalog_dirs():
        for profile in load_profiles_from(directory):
            loaded.setdefault(profile.id, profile)
    return loaded


def clear_profile_cache() -> None:
    """Drop the process-local catalog cache (tests and overlay reloads)."""
    _load_all.cache_clear()


def list_profiles() -> list[CompositionProfile]:
    """Return all discovered Composition Profiles, sorted by id."""
    return [item for _, item in sorted(_load_all().items())]


def get_profile(profile_id: str) -> CompositionProfile | None:
    """Look up a profile by id (case-insensitive)."""
    table = _load_all()
    if profile_id in table:
        return table[profile_id]
    lowered = profile_id.lower()
    for key, profile in table.items():
        if key.lower() == lowered:
            return profile
    return None
