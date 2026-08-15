"""Load and query versioned Composition Profiles."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from case_uco.topology.paths import profile_dirs


@dataclass(frozen=True)
class FacetSet:
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
    recipe_skeleton: dict[str, Any] = field(default_factory=dict)
    keywords: tuple[str, ...] = ()
    source_path: str = ""
    contract: dict[str, Any] = field(default_factory=dict)

    def facet_set_for(self, host: str) -> FacetSet | None:
        key = host.lower()
        for item in self.facet_sets:
            if item.host.lower() == key:
                return item
        return None

    def as_dict(self) -> dict[str, Any]:
        payload = {
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
        if self.contract:
            payload["contract"] = dict(self.contract)
        return payload


def _parse_profile(path: Path, raw: dict[str, Any]) -> CompositionProfile:
    facet_sets = []
    for host, spec in (raw.get("facet_sets") or {}).items():
        facet_sets.append(
            FacetSet(
                host=host,
                required=tuple(spec.get("required") or []),
                recommended=tuple(spec.get("recommended") or []),
                notes=spec.get("notes") or "",
            )
        )
    return CompositionProfile(
        id=raw["id"],
        version=raw["version"],
        title=raw["title"],
        description=raw["description"],
        mission=raw.get("mission") or "",
        air_gapped=bool(raw.get("air_gapped", True)),
        required_modules=tuple(raw.get("required_modules") or []),
        recommended_modules=tuple(raw.get("recommended_modules") or []),
        facet_sets=tuple(facet_sets),
        spine_anchors=tuple(raw.get("spine_anchors") or []),
        upper_ontology_profiles=tuple(raw.get("upper_ontology_profiles") or []),
        related_recipes=tuple(raw.get("related_recipes") or []),
        recipe_skeleton=dict(raw.get("recipe_skeleton") or {}),
        keywords=tuple(raw.get("keywords") or []),
        source_path=str(path),
        contract=dict(raw.get("contract") or {}),
    )


@lru_cache(maxsize=1)
def _load_all() -> dict[str, CompositionProfile]:
    loaded: dict[str, CompositionProfile] = {}
    for directory in profile_dirs():
        for path in sorted(directory.glob("*.json")):
            if path.name.endswith(".schema.json") or path.name == "profile.schema.json":
                continue
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if "id" not in raw:
                continue
            profile = _parse_profile(path, raw)
            loaded.setdefault(profile.id, profile)
    return loaded


def clear_profile_cache() -> None:
    _load_all.cache_clear()


def list_profiles() -> list[CompositionProfile]:
    """Return all Composition Profiles, sorted by id."""
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


def recommend_profile(scenario: str) -> list[dict[str, Any]]:
    """Rank profiles for a free-text investigative scenario.

    Offline lexical match against id, title, description, keywords, and
    mission. Always air-gapped — no embeddings required.
    """
    query = (scenario or "").strip().lower()
    if not query:
        return []
    tokens = {tok for tok in query.replace("/", " ").replace("-", " ").split() if len(tok) > 2}
    ranked: list[tuple[int, CompositionProfile]] = []
    for profile in list_profiles():
        hay = " ".join(
            [
                profile.id,
                profile.title,
                profile.description,
                profile.mission,
                " ".join(profile.keywords),
            ]
        ).lower()
        score = 0
        if query in hay:
            score += 8
        score += sum(2 for tok in tokens if tok in hay)
        if "cac" in tokens or "csam" in tokens or "grooming" in tokens:
            if profile.id == "FullCACLifecycle":
                score += 6
        if "photo" in hay and ("hash" in tokens or "photodna" in query or "vics" in tokens):
            if profile.id == "HashIntelligence":
                score += 6
        if "air" in tokens or "offline" in tokens or "field" in tokens or "triage" in tokens:
            if profile.id == "AirGappedFieldTriage":
                score += 4
        if score:
            ranked.append((score, profile))
    ranked.sort(key=lambda pair: (-pair[0], pair[1].id))
    return [
        {"score": score, "id": profile.id, "title": profile.title, "description": profile.description}
        for score, profile in ranked
    ]


def recommend_facet_set(host: str, profile_id: str | None = None) -> list[dict[str, Any]]:
    """Return recommended Facet sets for a host type, optionally scoped to one profile."""
    profiles = [get_profile(profile_id)] if profile_id else list_profiles()
    results: list[dict[str, Any]] = []
    for profile in profiles:
        if profile is None:
            continue
        facet_set = profile.facet_set_for(host)
        if facet_set is None:
            continue
        payload = facet_set.as_dict()
        payload["profile_id"] = profile.id
        results.append(payload)
    return results
