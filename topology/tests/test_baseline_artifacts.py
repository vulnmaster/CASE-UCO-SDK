"""Invariant checks for the Phase-0 topology artifacts.

These tests do not require rdflib or the generator. They pin the
machine-readable articulation so later phases cannot silently drop
the inventory, DAG, or recipe composition study.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY = REPO_ROOT / "topology"


def _load(name: str) -> dict:
    path = TOPOLOGY / name
    assert path.exists(), f"missing topology artifact: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_module_dependency_dag_shape() -> None:
    dag = _load("module-dependency-dag.json")
    assert dag["schema_version"] == "1.0.0"
    assert dag["ttl_file_count"] >= 100
    assert dag["node_count"] == len(dag["nodes"])
    assert dag["edge_count"] == len(dag["edges"])
    assert "uco.core" in dag["nodes"]
    assert "uco.observable" in dag["nodes"]
    assert "case.investigation" in dag["nodes"]
    assert "ext.cac.cac-core" in dag["nodes"]
    # Observable depends on core.
    obs_imports = dag["nodes"]["uco.observable"]["imports"]
    assert "uco.core" in obs_imports
    # No CAC instance-graph leftovers in the logical DAG.
    for mid in dag["nodes"]:
        assert not mid.endswith("-example")
        assert not mid.endswith("-skeleton")
        assert "brooklyn-" not in mid
        assert "examples_knowledge_graphs" not in mid


def test_class_and_facet_inventory_shape() -> None:
    inv = _load("class-and-facet-inventory.json")
    totals = inv["totals"]
    assert totals["modules"] >= 15
    assert totals["classes"] >= 400
    assert totals["facets"] >= 100
    assert "uco.observable" in inv["per_module"]
    observable = inv["per_module"]["uco.observable"]
    assert "FileFacet" in observable["facets"]
    assert "ContentDataFacet" in observable["facets"]
    assert "FileFacet" in inv["all_facets"]


def test_composition_patterns_cover_catalog() -> None:
    patterns = _load("composition-patterns.json")
    assert patterns["recipe_count"] >= 70
    assert len(patterns["recipes"]) == patterns["recipe_count"]
    cac = [r for r in patterns["recipes"] if r["is_cac"]]
    assert len(cac) >= 16
    starters = [r for r in patterns["recipes"] if r["is_starter_kit"]]
    assert len(starters) == 4
    assert patterns["task_to_classes_patterns"]
    facet_names = {name for name, _count in patterns["facet_frequency_across_recipes"]}
    assert "FileFacet" in facet_names
    assert "ContentDataFacet" in facet_names
    recommended = patterns["recommended_facet_sets"]
    assert "FileFacet" in recommended["File"]["union_recommended"]
    assert "ContentDataFacet" in recommended["File"]["union_recommended"]


def test_semantic_spine_kinds() -> None:
    spine = _load("semantic-spine.json")
    kinds = spine["cac_spine"]["kinds"]
    assert kinds == ["EnduringEntity", "Occurrent", "Situation", "Role", "Phase"]
    names = {c["name"] for c in spine["cac_spine"]["classes"]}
    assert {"Entity", "EnduringEntity", "Occurrent", "Situation", "Role", "Phase"} <= names
    uco_names = {c["name"] for c in spine["uco_core_hierarchy"]}
    assert {"UcoThing", "UcoObject", "Facet", "ObservableObject", "InvestigativeAction"} <= uco_names


def test_sdk_layers_enumerate_five_observed_plus_plan() -> None:
    layers = _load("sdk-layers.json")
    observed_ids = [layer["id"] for layer in layers["observed_layers"]]
    assert observed_ids == ["ontology", "generator", "runtime", "mcp", "knowledge"]
    assert len(layers["planned_layers"]) == 5


@pytest.mark.parametrize(
    "name",
    [
        "module-dependency-dag.md",
        "class-and-facet-inventory.md",
        "composition-patterns.md",
    ],
)
def test_markdown_companions_have_closed_mermaid(name: str) -> None:
    text = (TOPOLOGY / name).read_text(encoding="utf-8")
    assert text.count("```mermaid") == text.count("```") - text.count("```mermaid")
    # Every mermaid fence that opened also closed; equivalently, even fence count.
    assert text.count("```") % 2 == 0
    if name == "module-dependency-dag.md":
        assert "cac-core:Entity" in text
        assert "uco.core" in text
