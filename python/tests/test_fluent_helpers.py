"""Focused checks for the generic hashed-file, raster, and tool-run helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco import (  # noqa: E402
    CASEGraph,
    file_with_content_hashes,
    model_tool_run,
    raster_picture_with_hashes,
)
from case_uco import helpers as helpers_mod  # noqa: E402
from case_uco.uco.observable import EXIFFacet  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPERS_PATH = REPO_ROOT / "python" / "case_uco" / "helpers.py"
DOC_PATH = REPO_ROOT / "docs" / "FLUENT_HELPERS.md"

# Synthetic SHA-256 of the empty file. Public, not case material.
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


def _graph_blob(graph: CASEGraph) -> str:
    return graph.serialize()


def test_public_surface_is_only_the_three_generic_helpers() -> None:
    assert helpers_mod.PUBLIC_HELPERS == (
        "file_with_content_hashes",
        "raster_picture_with_hashes",
        "model_tool_run",
    )
    assert not hasattr(helpers_mod, "model_csam_evidence")
    assert not hasattr(helpers_mod, "classify")
    assert not hasattr(helpers_mod, "classify_media")


def test_file_with_content_hashes_attaches_file_and_content_facets() -> None:
    graph = CASEGraph()
    node = file_with_content_hashes(
        graph,
        file_name="empty.bin",
        file_path="/tmp/empty.bin",
        size_in_bytes=0,
        hashes=[("SHA256", EMPTY_SHA256)],
        id="kb:File-empty",
    )
    assert node.has_facet
    facet_types = {type(facet).__name__ for facet in node.has_facet}
    assert facet_types == {"FileFacet", "ContentDataFacet"}
    content = next(facet for facet in node.has_facet if type(facet).__name__ == "ContentDataFacet")
    assert content.hash[0].hash_method == "SHA256"
    assert content.hash[0].hash_value == EMPTY_SHA256

    blob = _graph_blob(graph)
    payload = json.loads(blob)
    assert len(payload["@graph"]) == 1
    assert EMPTY_SHA256 in blob
    assert "empty.bin" in blob


def test_raster_picture_with_hashes_uses_raster_host() -> None:
    graph = CASEGraph()
    picture = raster_picture_with_hashes(
        graph,
        file_name="sample.png",
        hashes=[("SHA256", EMPTY_SHA256)],
        picture_type="png",
        extra_facets=[EXIFFacet()],
    )
    assert type(picture).__name__ == "RasterPicture"
    names = [type(facet).__name__ for facet in picture.has_facet]
    assert names[:3] == ["FileFacet", "ContentDataFacet", "RasterPictureFacet"]
    assert "EXIFFacet" in names
    raster = next(facet for facet in picture.has_facet if type(facet).__name__ == "RasterPictureFacet")
    assert raster.picture_type == "png"

    blob = _graph_blob(graph)
    assert "uco-observable:RasterPicture" in blob
    assert EMPTY_SHA256 in blob


def test_model_tool_run_links_instrument_inputs_and_outputs() -> None:
    graph = CASEGraph()
    source = file_with_content_hashes(
        graph,
        file_name="disk.E01",
        hashes=[("SHA256", EMPTY_SHA256)],
    )
    report = file_with_content_hashes(
        graph,
        file_name="hash-report.txt",
        hashes=[("SHA256", EMPTY_SHA256)],
    )
    parts = model_tool_run(
        graph,
        tool_name="Autopsy",
        tool_version="4.21.0",
        tool_type="Forensic Analysis",
        action_name="Hash verification of disk image",
        inputs=[source],
        outputs=[report],
    )
    assert parts["tool"].name == "Autopsy"
    assert parts["tool"].version == "4.21.0"
    assert parts["tool"].tool_type == "Forensic Analysis"
    assert parts["action"].name == "Hash verification of disk image"
    assert parts["action"].instrument == [parts["tool"]]
    assert parts["action"].object == [source]
    assert parts["action"].result == [report]
    assert len(graph) == 4

    blob = _graph_blob(graph)
    assert "uco-tool:Tool" in blob
    assert "case-investigation:InvestigativeAction" in blob
    assert "uco-action:instrument" in blob


def test_helpers_require_real_hash_pairs() -> None:
    graph = CASEGraph()
    with pytest.raises(ValueError, match="at least one"):
        file_with_content_hashes(graph, file_name="x.bin", hashes=[])
    with pytest.raises(ValueError, match="non-empty"):
        raster_picture_with_hashes(graph, file_name="x.png", hashes=[("SHA256", "  ")])


def test_helpers_and_docs_are_public_safe() -> None:
    blob = HELPERS_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + DOC_PATH.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"helpers/docs contain forbidden substring {needle!r}"
    assert "does not classify" in DOC_PATH.read_text(encoding="utf-8").lower()
