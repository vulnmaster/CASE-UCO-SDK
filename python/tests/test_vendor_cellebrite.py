"""Cellebrite .ufd/.ufdx readers against public Digital Corpora extractions."""

import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from case_uco import CASEGraph
from case_uco.vendors.cellebrite import (
    parse_ufd,
    read_ufd,
    read_ufdx,
    ufd_to_graph,
)

FIXTURES = Path(__file__).parent / "fixtures" / "cellebrite"
UFED_728 = FIXTURES / "android10_ufed_7.28_Pixel3_trimmed.ufd"
PREMIUM_764 = FIXTURES / "ios15_premium_7.64_EXTRACTION_FFS.ufd"
INSEYETS_102 = FIXTURES / "android14_inseyets_10.2_EXTRACTION_FFS.ufd"


def test_ufed_728_has_no_device_info_section():
    record = read_ufd(UFED_728)
    assert record.version == "7.28.2.8"
    assert record.acquisition_tool is None
    assert record.vendor == "Google"
    assert record.model == "G013A Pixel 3"
    assert record.imeis == []
    assert record.extraction_method == "ANDROID_FS"
    assert record.file_part_sections == 2
    assert record.dump_files == ["Google_G013A Pixel 3.zip"]
    assert record.hashes[0].value.startswith("560345282323CA4F")
    assert any("[DeviceInfo]" in w for w in record.warnings)
    assert any("AcquisitionTool" in w for w in record.warnings)


def test_premium_764_withholds_passcode_by_default():
    record = read_ufd(PREMIUM_764)
    assert record.acquisition_tool == "Cellebrite Premium SaaS"
    assert record.os == "15.3.1 (19D52)"
    assert record.imeis == ["356763089830742"]
    assert record.extraction_method == "iOS_Full_Filesystem"
    assert record.passcode_present is True
    assert record.secrets == {}
    flattened = json.dumps(record.sections)
    assert "0731" not in flattened
    assert "PasscodeLength_0" not in flattened


def test_premium_764_secrets_on_request():
    record = read_ufd(PREMIUM_764, include_secrets=True)
    assert record.secrets["Passcode_0"] == "0731"
    assert record.secrets["PasscodeType_0"] == "User Code"


def test_inseyets_102_dual_imei_and_second_digest():
    record = read_ufd(INSEYETS_102)
    assert record.acquisition_tool == "Inseyets UFED_Pro_Advanced"
    assert record.imeis == ["354977438494370", "354977438494362"]
    assert record.security_patch_level == "2024-01-05"
    assert record.chipset == "GS201"
    assert {h.file_name for h in record.hashes} == {"EXTRACTION_FFS.zip", "SummaryReport.pdf"}
    assert record.dump_files == ["EXTRACTION_FFS.zip"]
    assert record.warnings == []


def test_ufd_dates_carry_their_offset():
    record = read_ufd(INSEYETS_102)
    edt = timezone(timedelta(hours=-4))
    assert record.start_time == datetime(2024, 7, 28, 7, 27, 27, tzinfo=edt)
    assert record.end_time == datetime(2024, 7, 28, 8, 38, 16, tzinfo=edt)


def test_ambiguous_date_order_is_reported():
    record = parse_ufd("[General]\nDate=05/06/2023 10:00:00 (+1)\n")
    assert record.start_time == datetime(2023, 6, 5, 10, 0, tzinfo=timezone(timedelta(hours=1)))
    assert any("ambiguous" in w for w in record.warnings)


def test_month_first_date_is_detected():
    record = parse_ufd("[General]\nDate=07/28/2024 07:27:27 (-4)\n")
    assert record.start_time.month == 7 and record.start_time.day == 28
    assert any("month-first" in w for w in record.warnings)


def test_unparseable_values_are_warnings_not_failures():
    record = parse_ufd("[General]\nDate=yesterday\n[SHA256]\nx.zip=not-hex\n")
    assert record.start_time is None
    assert record.hashes == []
    assert len(record.warnings) >= 2


def test_ufdx_lists_every_extraction():
    record = read_ufdx(FIXTURES / "ios15_EvidenceCollection.ufdx")
    assert record.vendor == "Apple"
    assert [e.path for e in record.extractions] == [
        "Password 01\\Password.ufd",
        "EXTRACTION_FFS 01\\EXTRACTION_FFS.ufd",
    ]


def _graph_of_all():
    graph = CASEGraph()
    for path in (UFED_728, PREMIUM_764, INSEYETS_102):
        ufd_to_graph(graph, read_ufd(path))
    return graph


def test_ufd_to_graph_is_deterministic_and_shares_vendor_nodes():
    first, second = _graph_of_all(), _graph_of_all()
    assert first.serialize() == second.serialize()
    nodes = json.loads(first.serialize())["@graph"]
    names = [n.get("uco-core:name") for n in nodes if n["@type"] == "uco-identity:Organization"]
    assert sorted(names) == ["Apple", "Cellebrite DI Ltd.", "Google"]


def test_ufd_to_graph_never_writes_the_passcode():
    graph = CASEGraph()
    ufd_to_graph(graph, read_ufd(PREMIUM_764, include_secrets=True))
    serialized = graph.serialize()
    assert "0731" not in serialized
    assert "withheld" in serialized


@pytest.mark.skipif(shutil.which("case_validate") is None, reason="case_validate not installed")
def test_ufd_graph_conforms(tmp_path):
    out = tmp_path / "ufd.jsonld"
    _graph_of_all().write(str(out))
    result = subprocess.run(
        ["case_validate", "--built-version", "case-1.5.0", str(out)],
        capture_output=True, text=True, timeout=600,
    )
    assert "Conforms: True" in result.stdout, result.stdout[-3000:]
