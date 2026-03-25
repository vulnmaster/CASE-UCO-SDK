"""Tests for the runtime ontology introspection API."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco import registry
from case_uco.registry import (
    search,
    list_modules,
    list_classes,
    get_class,
    find_by_property_type,
    find_facets,
    list_vocabs,
)


def setup_module():
    """Ensure the registry is loaded once for all tests."""
    registry._load()


def test_search_returns_results():
    results = search("Tool")
    assert len(results) > 0
    names = [r["name"] for r in results]
    assert "Tool" in names


def test_search_case_insensitive():
    upper = search("TOOL")
    lower = search("tool")
    assert len(upper) == len(lower)


def test_search_no_match():
    results = search("zzz_nonexistent_class_zzz")
    assert results == []


def test_list_modules():
    mods = list_modules()
    assert isinstance(mods, list)
    assert len(mods) > 0
    assert "uco.core" in mods
    assert "uco.observable" in mods


def test_list_classes_all():
    classes = list_classes()
    assert len(classes) > 100


def test_list_classes_by_module():
    classes = list_classes(module="uco.tool")
    assert len(classes) > 0
    assert "Tool" in classes


def test_list_classes_partial_module():
    classes = list_classes(module="tool")
    assert len(classes) > 0
    assert "Tool" in classes


def test_get_class_found():
    info = get_class("Tool")
    assert info is not None
    assert info["name"] == "Tool"
    assert "iri" in info
    assert "module" in info
    assert "properties" in info
    assert isinstance(info["properties"], list)


def test_get_class_case_insensitive():
    info = get_class("tool")
    assert info is not None
    assert info["name"] == "Tool"


def test_get_class_not_found():
    info = get_class("NonExistentClassXyz")
    assert info is None


def test_get_class_has_description():
    info = get_class("Tool")
    assert info is not None
    assert isinstance(info.get("description"), str)


def test_find_by_property_type():
    results = find_by_property_type("UcoObject")
    assert len(results) > 0


def test_find_facets():
    facets = find_facets()
    assert len(facets) > 0
    for f in facets:
        assert f["is_facet"] is True


def test_list_vocabs():
    vocabs = list_vocabs()
    assert isinstance(vocabs, list)


def test_class_properties_structure():
    info = get_class("Tool")
    assert info is not None
    for prop in info["properties"]:
        assert "name" in prop
        assert "type" in prop
        assert "cardinality" in prop
        assert "required" in prop
        assert "description" in prop
