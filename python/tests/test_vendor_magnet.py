"""Magnet ACQUIRE image_info.txt reader, against two real Digital Corpora acquisitions."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from case_uco import CASEGraph
from case_uco.vendors.magnet import (
    acquire_to_graph,
    parse_acquire_image_info,
    read_acquire_image_info,
)

FIXTURES = Path(__file__).parent / "fixtures" / "magnet"
IOS_13_3 = FIXTURES / "ios13_3_1" / "image_info.txt"
IOS_13_4 = FIXTURES / "ios13_4_1" / "image_info.txt"


def test_reads_product_segments_and_hashes():
    record = read_acquire_image_info(IOS_13_3)
    assert (record.product, record.version) == ("Magnet ACQUIRE", "2.25.0.20236")
    assert record.warnings == []
    [segment] = record.segments
    assert segment.relative_path == "Apple iPhone SE (GSM) Full Image.tar"
    assert segment.hashes == {
        "MD5": "A7D9C150ED8349A43978F552BB3AD2CB",
        "SHA1": "A5D4DAA7F50DC7FB35B422099EE02F908FFD27D7",
    }
    assert record.device["Operating System Version"] == "13.3.1"


def test_times_use_dotnet_ticks_for_sub_second_precision():
    record = read_acquire_image_info(IOS_13_3)
    assert record.start_time == datetime(2020, 4, 12, 19, 9, 0, 58082, tzinfo=timezone.utc)
    assert record.end_time.replace(microsecond=0) == datetime(2020, 4, 12, 19, 32, 13, tzinfo=timezone.utc)


def test_activity_log_md5_is_verified_when_the_log_is_beside_it(tmp_path):
    assert read_acquire_image_info(IOS_13_3).activity_log_verified is True

    shutil.copy(IOS_13_3, tmp_path / "image_info.txt")
    (tmp_path / "activity_log.txt").write_bytes(b"tampered\r\n")
    tampered = read_acquire_image_info(tmp_path / "image_info.txt")
    assert tampered.activity_log_verified is False
    assert any("does not match" in w for w in tampered.warnings)

    (tmp_path / "activity_log.txt").unlink()
    missing = read_acquire_image_info(tmp_path / "image_info.txt")
    assert missing.activity_log_verified is None
    assert any("not verified" in w for w in missing.warnings)


def test_drift_becomes_warnings_not_failures():
    text = IOS_13_3.read_text(encoding="utf-8")
    text = text.replace("Total Segments: 1", "Total Segments: 2")
    text = text.replace("Segment 1 SHA1 Hash: A5D4", "Segment 1 SHA1 Hash: ZZZZ")
    text = text.replace("ImageHashing: Success", "ImageHashing: Failed")
    text = text.replace("Imaging Start UTC Ticks: 637223153400580825", "Imaging Start UTC Ticks: 1")
    record = parse_acquire_image_info(text)
    joined = " | ".join(record.warnings)
    for expected in ("Total Segments says 2", "SHA1 value", "ImageHashing: Failed", "ticks 1 disagree"):
        assert expected in joined
    assert record.start_time == datetime(2020, 4, 12, 19, 9, tzinfo=timezone.utc)


def test_two_acquisitions_of_one_phone_share_the_device():
    graph = CASEGraph()
    first = acquire_to_graph(graph, read_acquire_image_info(IOS_13_3))
    second = acquire_to_graph(graph, read_acquire_image_info(IOS_13_4))
    assert str(graph.get_id(first["device"])) == str(second["device"])
    assert graph.get_id(first["action"]) != graph.get_id(second["action"])
    nodes = json.loads(graph.serialize())["@graph"]
    oses = [n for n in nodes if "uco-observable:OperatingSystem" in n["@type"]]
    assert sorted(n["uco-core:name"] for n in oses) == ["13.3.1", "13.4.1"]

    rerun = CASEGraph()
    acquire_to_graph(rerun, read_acquire_image_info(IOS_13_3))
    graph.load(rerun.serialize(), on_duplicate="merge_identical")
    assert len(json.loads(graph.serialize())["@graph"]) == len(nodes)


@pytest.mark.skipif(shutil.which("case_validate") is None, reason="case_validate not installed")
def test_acquisition_graph_conforms(tmp_path):
    graph = CASEGraph()
    acquire_to_graph(graph, read_acquire_image_info(IOS_13_3))
    acquire_to_graph(graph, read_acquire_image_info(IOS_13_4))
    out = tmp_path / "magnet-acquire.jsonld"
    graph.write(str(out))
    result = subprocess.run(
        ["case_validate", "--built-version", "case-1.5.0", str(out)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert "Conforms: True" in result.stdout, result.stdout[-3000:]
