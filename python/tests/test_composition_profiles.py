"""Schema and loader checks for the Composition Profiles catalog."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco.profiles import (  # noqa: E402
    clear_profile_cache,
    get_profile,
    list_profiles,
    load_profiles_from,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILES_DIR = REPO_ROOT / "topology" / "profiles"
SCHEMA_PATH = PROFILES_DIR / "profile.schema.json"

REQUIRED_IDS = {
    "MinimalForensics",
}

# Licensed / product-internal strings must not appear in this public catalog.
FORBIDDEN_SUBSTRINGS = (
    "photodna",
    "photo-dna",
    "vics",
    "court-defensible",
    "court defensible",
)


def _profile_files() -> list[Path]:
    return sorted(
        path
        for path in PROFILES_DIR.glob("*.json")
        if path.name != "profile.schema.json" and not path.name.endswith(".schema.json")
    )


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_schema_and_profiles_exist() -> None:
    assert SCHEMA_PATH.is_file()
    ids = {json.loads(path.read_text(encoding="utf-8"))["id"] for path in _profile_files()}
    assert ids == REQUIRED_IDS


def test_profiles_validate_against_schema() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(raw))
        assert not errors, f"{path.name}: {errors}"


def test_schema_rejects_unknown_properties_and_missing_id() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    validator = jsonschema.Draft202012Validator(_load_schema())
    valid = json.loads(_profile_files()[0].read_text(encoding="utf-8"))

    extra = dict(valid)
    extra["notAField"] = "nope"
    assert list(validator.iter_errors(extra))

    missing = dict(valid)
    missing.pop("id")
    assert list(validator.iter_errors(missing))


def test_loader_lists_and_gets_profiles() -> None:
    clear_profile_cache()
    profiles = list_profiles()
    assert {item.id for item in profiles} == REQUIRED_IDS
    found = get_profile("minimalforensics")
    assert found is not None
    assert found.id == "MinimalForensics"
    assert found.facet_set_for("File") is not None
    assert get_profile("DoesNotExist") is None


def test_related_recipes_exist() -> None:
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        for rel in raw.get("related_recipes") or []:
            assert (REPO_ROOT / rel).is_file(), f"{path.name} points at missing {rel}"


def test_named_modules_exist_in_registry() -> None:
    from case_uco.registry import list_modules

    known = set(list_modules())
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        for field in ("required_modules", "recommended_modules"):
            for module in raw.get(field) or []:
                assert module in known, f"{path.name} {field} unknown module {module}"


def test_catalog_is_public_safe_guidance() -> None:
    blob = SCHEMA_PATH.read_text(encoding="utf-8").lower()
    blob += "\n".join(path.read_text(encoding="utf-8") for path in _profile_files()).lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"catalog contains forbidden substring {needle!r}"
    for path in _profile_files():
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert raw.get("air_gapped") is True
        assert raw["recipe_skeleton"].get("steps")


def test_env_override_loads_synthetic_profile(tmp_path: Path) -> None:
    synthetic = {
        "id": "SyntheticOverlay",
        "version": "0.0.1",
        "title": "Synthetic overlay",
        "description": "Public-safe fixture used only by tests.",
        "required_modules": ["uco.core"],
        "recommended_modules": [],
        "facet_sets": {
            "File": {"required": ["FileFacet"], "recommended": []}
        },
        "spine_anchors": [],
        "upper_ontology_profiles": [],
        "recipe_skeleton": {"summary": "Fixture only.", "steps": ["Do not use in production."]},
    }
    (tmp_path / "SyntheticOverlay.json").write_text(
        json.dumps(synthetic), encoding="utf-8"
    )
    (tmp_path / "profile.schema.json").write_text("{}", encoding="utf-8")
    (tmp_path / "ignore.schema.json").write_text("{}", encoding="utf-8")
    (tmp_path / "broken.json").write_text("{", encoding="utf-8")

    loaded = load_profiles_from(tmp_path)
    assert [item.id for item in loaded] == ["SyntheticOverlay"]

    previous = os.environ.get("CASE_UCO_PROFILES_DIR")
    os.environ["CASE_UCO_PROFILES_DIR"] = str(tmp_path)
    try:
        clear_profile_cache()
        overlay = get_profile("SyntheticOverlay")
        assert overlay is not None
        assert overlay.title == "Synthetic overlay"
    finally:
        if previous is None:
            os.environ.pop("CASE_UCO_PROFILES_DIR", None)
        else:
            os.environ["CASE_UCO_PROFILES_DIR"] = previous
        clear_profile_cache()
