"""Focused checks for the bounded air-gapped adapter boundary."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco.graph import CASEGraph
from case_uco.offline_adapter import (
    AdapterBounds,
    AdapterRefused,
    LocalJsonRecordsAdapter,
    apply_offline_adapter,
    get_adapter,
    list_adapters,
    register_adapter,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER_PATH = REPO_ROOT / "python" / "case_uco" / "offline_adapter.py"
DOC_PATH = REPO_ROOT / "docs" / "OFFLINE_ADAPTER.md"

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92402706899c32911cf29121339aa1a904b"

FORBIDDEN_SUBSTRINGS = (
    "photodna",
    "photo-dna",
    "vics",
    "court-defensible",
    "court defensible",
    "2.0.0",
    "2.0.1",
    "investigationworkflow",
    "model_csam",
)


def _write_records(path: Path, rows: list[dict]) -> Path:
    path.write_text(json.dumps(rows), encoding="utf-8")
    return path


def test_public_surface_is_generic_and_air_gapped() -> None:
    from case_uco import offline_adapter as mod

    assert "LocalJsonRecordsAdapter" in mod.PUBLIC_SURFACE
    assert not hasattr(mod, "PhotoDnaAdapter")
    assert not hasattr(mod, "VicsCatalogAdapter")
    assert not hasattr(mod, "model_csam_evidence")
    assert "local-json-records" in list_adapters()
    assert get_adapter("local-json-records").air_gapped is True


def test_local_json_records_map_onto_existing_constructors(tmp_path: Path) -> None:
    source = _write_records(
        tmp_path / "records.json",
        [{"file_name": "empty.bin", "hashes": [["SHA256", EMPTY_SHA256]]}],
    )
    graph = CASEGraph()
    result = apply_offline_adapter("local-json-records", graph, source)
    assert result["created"] == 1
    assert len(graph) == 1
    blob = graph.serialize()
    assert "empty.bin" in blob
    assert EMPTY_SHA256 in blob
    assert "uco-observable:ContentDataFacet" in blob


def test_remote_and_missing_inputs_fail_closed(tmp_path: Path) -> None:
    graph = CASEGraph()
    with pytest.raises(AdapterRefused, match="non-local"):
        apply_offline_adapter(
            "local-json-records",
            graph,
            "https://example.invalid/records.json",
        )
    with pytest.raises(AdapterRefused, match="does not exist"):
        apply_offline_adapter("local-json-records", graph, tmp_path / "missing.json")
    with pytest.raises(AdapterRefused, match="unknown adapter"):
        apply_offline_adapter("not-a-real-adapter", graph, tmp_path / "missing.json")


def test_bounds_and_required_fields_fail_closed(tmp_path: Path) -> None:
    graph = CASEGraph()
    huge = tmp_path / "huge.json"
    huge.write_bytes(b"[" + (b"0," * 200) + b"0]")
    with pytest.raises(AdapterRefused, match="max_bytes"):
        apply_offline_adapter(
            "local-json-records",
            graph,
            huge,
            bounds=AdapterBounds(max_bytes=16),
        )

    rows = tmp_path / "rows.json"
    _write_records(
        rows,
        [
            {"file_name": "a.bin", "hashes": [["SHA256", EMPTY_SHA256]]},
            {"file_name": "b.bin", "hashes": [["SHA256", EMPTY_SHA256]]},
        ],
    )
    with pytest.raises(AdapterRefused, match="max_rows"):
        apply_offline_adapter(
            "local-json-records",
            graph,
            rows,
            bounds=AdapterBounds(max_rows=1),
        )

    bad = _write_records(tmp_path / "bad.json", [{"file_name": "x.bin"}])
    with pytest.raises(AdapterRefused, match="missing hashes"):
        apply_offline_adapter("local-json-records", graph, bad)


def test_non_air_gapped_adapter_cannot_register() -> None:
    class OpenAdapter:
        adapter_id = "open-net"
        air_gapped = False

        def probe(self, source: Path) -> bool:
            return True

        def apply(self, graph: CASEGraph, source: Path, **kwargs):
            return {"adapter": self.adapter_id}

    with pytest.raises(AdapterRefused, match="air-gapped"):
        register_adapter(OpenAdapter())


def test_adapter_and_docs_are_public_safe() -> None:
    blob = ADAPTER_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + DOC_PATH.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"adapter/docs contain forbidden substring {needle!r}"
    assert LocalJsonRecordsAdapter().air_gapped is True
    doc = DOC_PATH.read_text(encoding="utf-8").lower()
    assert "does not classify" in doc
    assert "do not embed a licensed catalog" in doc
