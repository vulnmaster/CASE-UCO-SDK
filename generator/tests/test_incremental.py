"""Tests for the incremental generate manifest (no full OWL parse)."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.incremental import (
    build_manifest,
    collect_source_files,
    sources_unchanged,
    write_ir,
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
