"""UFED report.xml reader against a trimmed Digital Corpora Android 13 report."""

import io
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from case_uco import CASEGraph
from case_uco.graph import DuplicateNodeError
from case_uco.vendors.cellebrite import (
    UfedModel,
    UfedReport,
    UfedSourceLink,
    UfedTaggedFile,
    iter_report,
    read_report_summary,
    tagged_files_to_graph,
)
from case_uco.vendors.file_identity import add_reported_file, normalize_hash

REPORT = Path(__file__).parent / "fixtures" / "cellebrite" / "android13_pa_7.58_report_trimmed.xml"
CACHE = "/data/data/com.android.chrome/cache/Cache/Cache_Data/69948f86d014bea6_0"
EXHIBIT = "android13-pixel5a"


def _read():
    report = UfedReport()
    items = list(iter_report(REPORT, report=report))
    return report, items


def _files(items):
    return [i for i in items if isinstance(i, UfedTaggedFile)]


def _graph():
    graph = CASEGraph()
    tagged_files_to_graph(graph, _files(_read()[1]), exhibit=EXHIBIT, report="android13-report")
    return graph


def _nodes(graph):
    return json.loads(graph.serialize())["@graph"]


def _relations(graph, kind):
    return {
        (source["@id"], target["@id"])
        for n in _nodes(graph)
        if n.get("uco-core:kindOfRelationship") == kind
        for source in _as_list(n["uco-core:source"])
        for target in _as_list(n["uco-core:target"])
    }


def _as_list(value):
    return value if isinstance(value, list) else [value]


def _path_of(node):
    for facet in _as_list(node.get("uco-core:hasFacet", [])):
        if facet["@type"] == "uco-observable:FileFacet":
            paths = _as_list(facet.get("uco-observable:filePath", []))
            return paths[0] if paths else None
    return None


def test_report_header_distinguishes_schema_and_analyzer_versions():
    report, _ = _read()
    assert report.namespace == "http://pa.cellebrite.com/report/2.0"
    assert report.report_version == "7.48"
    assert report.item("UFED_PA_Version") == "7.58.0.66"
    assert report.extraction_type == "Legacy"
    assert report.case_information == {"Examiner name": "J. Hickman"}
    assert report.extractions[0]["deviceName"] == "G1F8F Pixel 5a"
    assert report.images[0]["verify"] == "NoSourceValues"
    assert len([m for m in report.metadata if m.name == "ICCID"]) > 1
    assert report.warnings == []


def test_related_nodes_are_full_entries_with_the_same_content():
    report, items = _read()
    files = _files(items)
    assert (report.tagged_file_count, report.related_file_count) == (4, 4)
    by_id = {f.id: f for f in files}
    related = [f for f in files if f.related_to]
    assert len(related) == 4
    for f in related:
        parent = by_id[f.related_to]
        assert f.path.startswith("/data/user/0/") and parent.path.startswith("/data/data/")
        assert (f.size, f.hashes) == (parent.size, parent.hashes)


def test_embedded_files_share_a_synthetic_path():
    files = _files(_read()[1])
    payloads = [f for f in files if f.path == CACHE + "/www.wral.com"]
    assert [f.attributes["embedded"] for f in payloads] == ["true", "true"]
    assert sorted(f.size for f in payloads) == [4212, 4235]
    assert payloads[0].local_path != payloads[1].local_path


def test_models_keep_nested_parties_and_related_models():
    report, items = _read()
    models = {m.type: m for m in items if isinstance(m, UfedModel)}
    call = models["Call"]
    assert call.value("Source") == "Facebook Messenger"
    assert call.value("Duration") == "00:01:38"
    roles = {p.value("Role") for p in call.models["Parties"]}
    assert roles == {"From", "To"}
    chat = models["Chat"]
    assert chat.related and chat.related[0].value("Id") == chat.value("Id")
    assert chat.value("Name") is None
    assert report.model_counts == {"Call": 1, "Chat": 1, "Contact": 1, "InstalledApplication": 1}


def test_source_links_name_their_target_kind():
    _, items = _read()
    links = [i for i in items if isinstance(i, UfedSourceLink)]
    file_ids = {f.id for f in _files(items)}
    model_ids = {m.id for m in items if isinstance(m, UfedModel)}
    assert {link.kind for link in links} == {"model", "node"}
    assert all(link.target_id in file_ids for link in links if link.kind == "node")
    assert all(link.target_id in model_ids for link in links if link.kind == "model")
    assert any("tableName" in node for link in links for node in link.nodes)


def test_model_type_filter_only_counts_the_rest():
    report = UfedReport()
    models = [i for i in iter_report(REPORT, report=report, model_types={"Call"}) if isinstance(i, UfedModel)]
    assert [m.type for m in models] == ["Call"]
    assert report.model_counts["Contact"] == 1


def test_node_count_mismatch_is_reported_as_truncation():
    data = REPORT.read_bytes().replace(b'NodeCount="8"', b'NodeCount="9"', 1)
    report = read_report_summary(io.BytesIO(data))
    assert any("truncated" in w for w in report.warnings)


def test_passcode_like_metadata_is_withheld():
    data = REPORT.read_bytes().replace(
        b'<metadata section="Device Info">',
        b'<metadata section="Device Info"><item name="DeviceInfoUnlockCode">4321</item>',
        1,
    )
    report = read_report_summary(io.BytesIO(data))
    assert report.secrets_withheld == 1
    assert report.item("DeviceInfoUnlockCode") is None
    assert read_report_summary(io.BytesIO(data), include_secrets=True).item("DeviceInfoUnlockCode") == "4321"


def test_embedded_payloads_hang_off_their_container_not_a_shared_path():
    graph = _graph()
    nodes = {n["@id"]: n for n in _nodes(graph)}
    exhibit_paths = {
        _path_of(n) for n in nodes.values()
        if n["@type"] == "uco-observable:File" and "uco-core:name" not in n
    }
    assert CACHE in exhibit_paths
    assert CACHE + "/www.wral.com" not in exhibit_paths

    extracted = _relations(graph, "Extracted_From")
    container = next(i for i, n in nodes.items() if _path_of(n) == CACHE and "uco-core:name" not in n)
    payload_entries = {s for s, t in extracted if t == container and nodes[s]["@type"] == "uco-observable:File"}
    assert len(payload_entries) == 2


def test_aliases_converge_on_one_content_core():
    graph = _graph()
    contained = _relations(graph, "Contained_Within")
    nodes = {n["@id"]: n for n in _nodes(graph)}
    flags = {
        i for i, n in nodes.items()
        if "experiment-flags" in (_path_of(n) or "") and "uco-core:name" not in n
    }
    assert len(flags) == 2
    cores = {s for s, t in contained if t in flags}
    assert len(cores) == 1
    assert {t for s, t in contained if s in cores} == flags


def test_reingest_changes_nothing():
    graph = _graph()
    before = graph.serialize()
    graph.load(_graph().serialize(), on_duplicate="merge_identical")
    assert graph.serialize() == before


def test_add_reported_file_merges_hashes_within_one_graph():
    graph = CASEGraph()
    common = dict(exhibit="E", report="R", path="\\sdcard\\a.jpg", size=3)
    add_reported_file(graph, row="1", hashes=[("MD5", "900150983cd24fb0d6963f7d28e17f72")], **common)
    nodes = add_reported_file(
        graph, row="2", hashes=[("sha-1", "a9993e364706816aba3e25717850c26c9cd0d89d")], **common
    )
    methods = sorted(
        h["uco-types:hashMethod"]
        for f in _as_list(graph.get(nodes.exhibit_file)["uco-core:hasFacet"])
        if f["@type"] == "uco-observable:ContentDataFacet"
        for h in _as_list(f["uco-observable:hash"])
    )
    assert methods == ["MD5", "SHA1"]
    with pytest.raises(DuplicateNodeError):
        add_reported_file(graph, exhibit="E", report="R", row="3", path="/sdcard/a.jpg", size=4)


def test_normalize_hash_rejects_unusable_values():
    assert normalize_hash("sha-256", "ab") == ("SHA256", "AB")
    assert normalize_hash("CRC32", "ab") is None
    assert normalize_hash("MD5", "") is None
    assert normalize_hash("MD5", "not hex") is None


IOS_REPORT = REPORT.with_name("ios15_pa_7.62_report_trimmed.xml")
THREEMA = (
    "/root/private/var/mobile/Containers/Shared/AppGroup/"
    "B99D094B-85DD-40F6-ACE1-E5AA53C03C75/ThreemaData.sqlite"
)


def _ios_graph(warnings=None):
    graph = CASEGraph()
    files = [i for i in iter_report(IOS_REPORT) if isinstance(i, UfedTaggedFile)]
    tagged_files_to_graph(graph, files, exhibit="ios15-iphone8", report="ios15-report", warnings=warnings)
    return graph


def test_ios_report_has_the_same_schema_from_a_later_analyzer():
    report = read_report_summary(IOS_REPORT)
    assert (report.report_version, report.item("UFED_PA_Version")) == ("7.48", "7.62.0.40")
    assert [e["type"] for e in report.extractions] == ["PasswordExtraction", "FileSystem"]
    assert report.case_information == {"Examiner name": "Hickman"}
    assert report.warnings == []


def test_paths_with_different_content_share_no_exhibit_file():
    warnings = []
    graph = _ios_graph(warnings)
    assert len(warnings) == 2
    assert any(".GlobalPreferences.plist" in w for w in warnings)
    assert any("Zoom.app/\u00f0___.json" in w for w in warnings)

    characterized = {t for _, t in _relations(graph, "Characterizes")}
    nodes = {n["@id"]: n for n in _nodes(graph)}
    shared_paths = {_path_of(nodes[t]) for t in characterized}
    assert all(".GlobalPreferences" not in p and "Zoom.app" not in p for p in shared_paths)
    zoom_entries = [
        n for n in nodes.values()
        if "uco-core:name" in n and "Zoom.app" in (_path_of(n) or "")
    ]
    assert len(zoom_entries) == 4


def test_embedded_file_at_its_containers_own_path():
    graph = _ios_graph()
    nodes = {n["@id"]: n for n in _nodes(graph)}
    container = next(
        i for i, n in nodes.items() if _path_of(n) == THREEMA and "uco-core:name" not in n
    )
    images = {s for s, t in _relations(graph, "Extracted_From") if t == container and "uco-core:name" in nodes[s]}
    assert len(images) == 2


@pytest.mark.skipif(shutil.which("case_validate") is None, reason="case_validate not installed")
def test_ios_report_graph_conforms(tmp_path):
    out = tmp_path / "ios-report.jsonld"
    _ios_graph().write(str(out))
    result = subprocess.run(
        ["case_validate", "--built-version", "case-1.5.0", str(out)],
        capture_output=True, text=True, timeout=600,
    )
    assert "Conforms: True" in result.stdout, result.stdout[-3000:]


@pytest.mark.skipif(shutil.which("case_validate") is None, reason="case_validate not installed")
def test_report_graph_conforms(tmp_path):
    out = tmp_path / "report.jsonld"
    _graph().write(str(out))
    result = subprocess.run(
        ["case_validate", "--built-version", "case-1.5.0", str(out)],
        capture_output=True, text=True, timeout=600,
    )
    assert "Conforms: True" in result.stdout, result.stdout[-3000:]
