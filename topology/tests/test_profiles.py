"""Invariant checks for versioned Composition Profile documents."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILES = REPO_ROOT / "topology" / "profiles"

REQUIRED_IDS = {
    "MinimalForensics",
    "FullCACLifecycle",
    "HashIntelligence",
    "ToolMapping",
    "LegalProcess",
    "CrossOntology",
    "AirGappedFieldTriage",
}


def _profile_files() -> list[Path]:
    return sorted(
        path
        for path in PROFILES.glob("*.json")
        if path.name != "profile.schema.json"
    )


def test_expected_profiles_exist() -> None:
    ids = {json.loads(path.read_text(encoding="utf-8"))["id"] for path in _profile_files()}
    assert ids == REQUIRED_IDS


def test_profiles_satisfy_required_keys() -> None:
    required = {
        "id",
        "version",
        "title",
        "description",
        "required_modules",
        "recommended_modules",
        "facet_sets",
        "spine_anchors",
        "upper_ontology_profiles",
        "recipe_skeleton",
    }
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        missing = required - set(raw)
        assert not missing, f"{path.name} missing {missing}"
        assert raw["recipe_skeleton"].get("steps"), f"{path.name} has empty skeleton"
        assert raw.get("air_gapped") is True


def test_profiles_match_schema_when_jsonschema_available() -> None:
    schema_path = PROFILES / "profile.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        required = {
            "id", "version", "title", "description", "required_modules",
            "recommended_modules", "facet_sets", "spine_anchors",
            "upper_ontology_profiles", "recipe_skeleton",
        }
        for path in _profile_files():
            raw = json.loads(path.read_text(encoding="utf-8"))
            assert required <= set(raw)
        return
    validator = jsonschema.Draft202012Validator(schema)
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(raw))
        assert not errors, f"{path.name}: {errors}"


def test_related_recipes_exist() -> None:
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        for rel in raw.get("related_recipes") or []:
            assert (REPO_ROOT / rel).is_file(), f"{path.name} points at missing {rel}"
