"""Offline VICS / PhotoDNA adapters. No network. No PhotoDNAFacet."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from case_uco.adapters import get_adapter
from case_uco.builder import InvestigationBuilder


def test_photodna_adapter_local_list(tmp_path: Path) -> None:
    source = tmp_path / "pdna.json"
    source.write_text(
        json.dumps([{"file": "img.jpg", "sha256": "aa", "photodna": "bb"}]),
        encoding="utf-8",
    )
    builder = InvestigationBuilder("hash intel", profile_id="HashIntelligence")
    result = get_adapter("photodna").apply(builder, source)
    assert result["created"] == 1
    serialized = builder.build().serialize()
    assert "PhotoDNA" in serialized
    assert "PhotoDNAFacet" not in serialized


def test_vics_adapter_local_export(tmp_path: Path) -> None:
    source = tmp_path / "vics.json"
    source.write_text(
        json.dumps({"media": [{"MediaId": "M1", "SHA256": "cc", "PhotoDNA": "dd"}]}),
        encoding="utf-8",
    )
    builder = InvestigationBuilder("vics", profile_id="HashIntelligence")
    result = get_adapter("vics-catalog").apply(builder, source)
    assert result["created"] == 1
    assert "SHA256" in builder.build().serialize()


def test_adapter_refuses_http() -> None:
    builder = InvestigationBuilder("vics", profile_id="HashIntelligence")
    with pytest.raises(ValueError, match="non-local"):
        get_adapter("photodna").apply(builder, "https://example.invalid/export.json")


def test_adapter_malformed_json(tmp_path: Path) -> None:
    source = tmp_path / "bad.json"
    source.write_text("{not json", encoding="utf-8")
    builder = InvestigationBuilder("vics", profile_id="HashIntelligence")
    with pytest.raises(ValueError, match="malformed JSON"):
        get_adapter("photodna").apply(builder, source)


def test_hash_match_records_existing_graph_hits(tmp_path: Path) -> None:
    builder = InvestigationBuilder("hash intel", profile_id="HashIntelligence")
    builder.add_csam_evidence("img.jpg", hashes=[("SHA256", "aa"), ("PhotoDNA", "bb")])
    catalog = tmp_path / "matches.json"
    catalog.write_text(
        json.dumps([{"sha256": "aa", "method": "SHA256", "distance": 0}]),
        encoding="utf-8",
    )
    result = get_adapter("hash-match").apply(builder, catalog)
    assert result["matches"] == 1
    assert result["hits"][0]["digest"] == "aa"
    serialized = builder.build().serialize()
    assert "hash-match" in serialized
    assert "AnalyticResult" in serialized or "analyticresult" in serialized.lower()


def test_vics_tags_media_id(tmp_path: Path) -> None:
    source = tmp_path / "vics.json"
    source.write_text(
        json.dumps({"media": [{"MediaId": "M99", "SHA256": "ee"}]}),
        encoding="utf-8",
    )
    builder = InvestigationBuilder("vics", profile_id="HashIntelligence")
    get_adapter("vics-catalog").apply(builder, source)
    assert "vics-media-id:M99" in builder.build().serialize()
