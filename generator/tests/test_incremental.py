"""Tests for the incremental generate manifest (no full OWL parse)."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from case_uco_generator.incremental import (
    build_manifest,
    collect_source_files,
    merge_registry,
    sources_unchanged,
    write_ir,
)
from case_uco_generator.schema_model import (
    Cardinality,
    OntologyClass,
    OntologyProperty,
    OntologySchema,
)


def test_collect_source_files_skips_examples(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    files = collect_source_files(root)
    assert files
    assert all("examples_knowledge_graphs" not in p.as_posix() for p in files)


def test_manifest_stable_hash(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    first = build_manifest(root)
    second = build_manifest(root)
    assert first["aggregate_sha256"] == second["aggregate_sha256"]
    assert first["file_count"] == second["file_count"]
    assert first["file_count"] > 50


def test_plan_reparse_leaf_extension_is_subset() -> None:
    root = Path(__file__).resolve().parents[2]
    from case_uco_generator.incremental import plan_reparse

    plan = plan_reparse(root, ["extensions/cryptoinv/cryptoinv.ttl"])
    assert plan["mode"] == "subset"
    assert plan["reason"] == "extension-leaf-delta"
    assert any(p.startswith("ontology/UCO/") or "/uco/" in p for p in plan["paths"])
    assert "extensions/cryptoinv/cryptoinv.ttl" in plan["paths"]
    cac_hits = [p for p in plan["paths"] if "cacontology" in p]
    assert cac_hits == []


def test_plan_reparse_core_forces_full() -> None:
    root = Path(__file__).resolve().parents[2]
    from case_uco_generator.incremental import plan_reparse

    plan = plan_reparse(root, ["ontology/UCO/ontology/uco/core/core.ttl"])
    assert plan["mode"] == "full"
    assert plan["reason"] == "core-ontology-changed"


def test_write_ir_round_trip(tmp_path: Path) -> None:
    # Write into a temp copy of the repo root structure.
    (tmp_path / "ontology").mkdir()
    ttl = tmp_path / "ontology" / "toy.ttl"
    ttl.write_text("@prefix : <http://example.org/> .\n", encoding="utf-8")
    dest = write_ir(tmp_path, schema=None)
    assert dest.is_file()
    assert (tmp_path / "generator" / "ir" / "source-manifest.json").is_file()
    assert sources_unchanged(tmp_path) is True
    ttl.write_text("# changed\n", encoding="utf-8")
    assert sources_unchanged(tmp_path) is False


def _toy_schema(*classes: OntologyClass) -> OntologySchema:
    return OntologySchema(
        classes={cls.iri: cls for cls in classes},
        modules={cls.module: [cls.iri] for cls in classes},
    )


def test_merge_registry_updates_only_ext_classes(tmp_path: Path) -> None:
    dest = tmp_path / "python" / "case_uco" / "_registry.json"
    dest.parent.mkdir(parents=True)
    rust_copy = tmp_path / "rust" / "src" / "_registry.json"
    rust_copy.parent.mkdir(parents=True)
    original = {
        "modules": ["uco.core"],
        "classes": {
            "UcoObject": {
                "iri": "https://ontology.unifiedcyberontology.org/uco/core/UcoObject",
                "module": "uco.core",
                "description": "ORIGINAL",
                "parents": [],
                "is_facet": False,
                "properties": [{"name": "name"}],
            }
        },
        "vocabs": {},
    }
    dest.write_text(json.dumps(original), encoding="utf-8")
    rust_copy.write_text(json.dumps(original), encoding="utf-8")

    core = OntologyClass(
        iri="https://ontology.unifiedcyberontology.org/uco/core/UcoObject",
        name="UcoObject",
        namespace_prefix="uco-core",
        module="uco.core",
        description="CHANGED IN SUBSET",
    )
    ext = OntologyClass(
        iri="https://example.org/ext/cryptoinv/Foo",
        name="Foo",
        namespace_prefix="cryptoinv",
        module="ext.cryptoinv",
        description="new leaf",
        parent_iris=["https://ontology.unifiedcyberontology.org/uco/core/UcoObject"],
        properties=[
            OntologyProperty(
                iri="https://example.org/ext/cryptoinv/bar",
                name="bar",
                range_iri="http://www.w3.org/2001/XMLSchema#string",
                range_is_class=False,
                cardinality=Cardinality.ZERO_OR_ONE,
                description="leaf property",
            )
        ],
    )
    merge_registry(tmp_path, _toy_schema(core, ext))
    merged = json.loads(dest.read_text(encoding="utf-8"))
    assert merged["classes"]["UcoObject"]["description"] == "ORIGINAL"
    assert merged["classes"]["UcoObject"]["properties"] == [{"name": "name"}]
    assert merged["classes"]["Foo"]["description"] == "new leaf"
    assert merged["classes"]["Foo"]["parents"] == ["UcoObject"]
    assert merged["classes"]["Foo"]["properties"][0]["type"] == "string"
    assert merged["classes"]["Foo"]["properties"][0]["type"] != "str"
    assert "ext.cryptoinv" in merged["modules"]
    rust_merged = json.loads(rust_copy.read_text(encoding="utf-8"))
    assert rust_merged["classes"]["Foo"]["iri"] == ext.iri


def test_write_ir_does_not_shrink_class_count(tmp_path: Path) -> None:
    (tmp_path / "ontology").mkdir()
    (tmp_path / "ontology" / "toy.ttl").write_text("@prefix : <http://example.org/> .\n", encoding="utf-8")
    ir_dir = tmp_path / "generator" / "ir"
    ir_dir.mkdir(parents=True)
    previous = {
        "class_count": 2804,
        "facet_count": 154,
        "module_counts": {"uco.core": 40, "ext.cryptoinv": 2},
        "inheritance_edge_count": 900,
        "recommended_facet_bundles": {"MinimalForensics": {}},
    }
    (ir_dir / "ontology-ir.json").write_text(json.dumps(previous), encoding="utf-8")
    subset = SimpleNamespace(
        classes={
            "https://example.org/A": SimpleNamespace(
                module="ext.cryptoinv",
                is_facet=False,
                parent_iris=[],
                name="A",
            )
        }
    )
    dest = write_ir(tmp_path, schema=subset)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["class_count"] == 2804
    assert data["facet_count"] == 154
    assert data["module_counts"]["uco.core"] == 40
    assert data["inheritance_edge_count"] == 900


def test_write_ir_restores_counts_from_registry_when_zeroed(tmp_path: Path) -> None:
    (tmp_path / "ontology").mkdir()
    (tmp_path / "ontology" / "toy.ttl").write_text("@prefix : <http://example.org/> .\n", encoding="utf-8")
    reg_dir = tmp_path / "python" / "case_uco"
    reg_dir.mkdir(parents=True)
    (reg_dir / "_registry.json").write_text(
        json.dumps(
            {
                "classes": {
                    "File": {"module": "uco.observable", "is_facet": False, "parents": ["ObservableObject"]},
                    "FileFacet": {"module": "uco.observable", "is_facet": True, "parents": ["Facet"]},
                }
            }
        ),
        encoding="utf-8",
    )
    dest = write_ir(tmp_path, schema=None)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["class_count"] == 2
    assert data["facet_count"] == 1
    assert data["inheritance_edge_count"] == 2
    assert data["module_counts"]["uco.observable"] == 2
