"""Unit tests for Composition Profile loading and spine queries."""

from __future__ import annotations

from case_uco.registry import get_profile, list_profiles, recommend_profile
from case_uco.topology import (
    get_semantic_spine,
    list_spine_kinds,
    recommend_facet_set,
    spine_kind_for_class,
)
from case_uco.topology.profiles import clear_profile_cache


EXPECTED_IDS = {
    "MinimalForensics",
    "FullCACLifecycle",
    "HashIntelligence",
    "ToolMapping",
    "LegalProcess",
    "CrossOntology",
    "AirGappedFieldTriage",
}


def setup_function() -> None:
    clear_profile_cache()


def test_list_profiles_contains_all_seven() -> None:
    profiles = list_profiles()
    ids = {p["id"] for p in profiles}
    assert EXPECTED_IDS <= ids
    assert len(profiles) >= 7


def test_get_profile_round_trip() -> None:
    profile = get_profile("FullCACLifecycle")
    assert profile is not None
    assert profile["version"] == "1.0.0"
    assert "ext.cac.cac-core" in profile["required_modules"]
    assert "RasterPicture" in profile["facet_sets"]
    file_set = profile["facet_sets"]["File"]
    assert "FileFacet" in file_set["required"]
    assert "ContentDataFacet" in file_set["required"]
    assert "cac-core:Role" in profile["spine_anchors"]
    assert profile["recipe_skeleton"]["steps"]


def test_get_profile_case_insensitive() -> None:
    assert get_profile("minimalforensics") is not None
    assert get_profile("does-not-exist") is None


def test_hash_intelligence_is_photodna_ready() -> None:
    profile = get_profile("HashIntelligence")
    assert profile is not None
    picture = profile["facet_sets"]["RasterPicture"]
    assert "ContentDataFacet" in picture["required"]
    assert any("photodna" in k.lower() or k.lower() == "vics" for k in profile["keywords"])


def test_air_gapped_profiles_declare_offline() -> None:
    for profile in list_profiles():
        assert profile["air_gapped"] is True


def test_recommend_profile_ranks_cac_scenario() -> None:
    ranked = recommend_profile("NCMEC cybertip grooming CSAM victim identification")
    assert ranked
    assert ranked[0]["id"] == "FullCACLifecycle"


def test_recommend_facet_set_file() -> None:
    sets = recommend_facet_set("File", "MinimalForensics")
    assert len(sets) == 1
    assert sets[0]["required"] == ["FileFacet", "ContentDataFacet"]


def test_semantic_spine_kinds() -> None:
    spine = get_semantic_spine()
    assert spine["cac_spine"]["kinds"] == [
        "EnduringEntity",
        "Occurrent",
        "Situation",
        "Role",
        "Phase",
    ]
    names = {kind.name for kind in list_spine_kinds()}
    assert {"EnduringEntity", "Occurrent", "Situation", "Role", "Phase"} <= names
    role = spine_kind_for_class("Role")
    assert role is not None
    assert role["kind"] == "role"
    assert spine_kind_for_class("NotASpineClass") is None
