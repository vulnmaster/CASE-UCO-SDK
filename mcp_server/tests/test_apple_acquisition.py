"""Tier T0 synthetic tests for Apple acquisition package tooling (issue #99)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import workspace_policy
from apple_acquisition import (
    MAX_EVENT_RECORDS,
    MAX_EVENT_LINE_BYTES,
    build_acquisition_package_graph,
    classify_apple_package_shape,
)


def _make_logarchive(root: Path, name: str = "system_logs.logarchive") -> Path:
    archive = root / name
    (archive / "Persist").mkdir(parents=True)
    (archive / "Persist" / "0000000000000001.tracev3").write_bytes(b"synthetic-trace")
    return archive


def _make_sysdiagnose(tmp_path: Path) -> Path:
    root = tmp_path / "sysdiagnose_2026.08.11_12-00-00_iPhone-OS_synthetic"
    root.mkdir()
    _make_logarchive(root)
    for directory in ("WiFi", "summaries", "logs", "crashes_and_spins", "Preferences"):
        (root / directory).mkdir()
    (root / "crashes_and_spins" / "synthetic.ips").write_text(
        '{"bug_type":"288","incident_id":"synthetic"}\n', encoding="utf-8"
    )
    return root


def _make_foss_collect(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "operator-C-drive-case-UDID-00008020-001C2D1234567890"
    root.mkdir()
    _make_logarchive(root, "standalone.logarchive")
    crashes = root / "crash_pull"
    crashes.mkdir()
    (crashes / "synthetic-crash.ips").write_text("{}\n", encoding="utf-8")
    (root / "live_syslog.txt").write_text("local-only raw syslog\n", encoding="utf-8")
    (root / "installed_apps.txt").write_text(
        "com.example.one\ncom.example.two\n", encoding="utf-8"
    )
    excerpt = root / "unifiedlog_iterator_excerpt.jsonl"
    rows = [
        {
            "subsystem": "com.apple.synthetic",
            "log_type": "Default",
            "message": "Call +1 202-555-0199 using IMEI 490154203237518",
            "mach_continuous_time": str(1000 + index),
            "boot_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "timestamp_tool": f"2026-08-11T12:00:0{index}Z",
        }
        for index in range(3)
    ]
    excerpt.write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )
    return root, excerpt


def _nodes(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["@graph"]


def _nodes_of_type(nodes: list[dict], node_type: str) -> list[dict]:
    matches = []
    for node in nodes:
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if node_type in types:
            matches.append(node)
    return matches


def test_builder_enforces_workspace_read_and_write_roots(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    evidence = tmp_path / "evidence"
    work = tmp_path / "work"
    outside = tmp_path / "outside"
    for directory in (evidence, work, outside):
        directory.mkdir()
    root, _ = _make_foss_collect(evidence)
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    monkeypatch.setenv(workspace_policy.WRITE_ROOTS_ENV, str(work))

    with pytest.raises(ValueError, match="output_outside_write_roots"):
        build_acquisition_package_graph(root, outside / "graph.jsonld")
    with pytest.raises(ValueError, match="source_outside_read_roots"):
        classify_apple_package_shape(outside)


def test_classifier_distinguishes_full_sysdiagnose_from_foss(tmp_path: Path) -> None:
    sysdiag = _make_sysdiagnose(tmp_path)
    foss, _ = _make_foss_collect(tmp_path)

    assert classify_apple_package_shape(sysdiag)["profile"] == "ios-sysdiagnose"
    assert classify_apple_package_shape(foss)["profile"] == "apple-foss-logarchive"


def test_classifier_fails_closed_for_lone_or_multiple_logarchives(tmp_path: Path) -> None:
    lone = tmp_path / "lone"
    lone.mkdir()
    _make_logarchive(lone, "standalone.logarchive")
    with pytest.raises(ValueError, match="ambiguous_apple_package_shape"):
        classify_apple_package_shape(lone)

    multiple = tmp_path / "multiple"
    multiple.mkdir()
    _make_logarchive(multiple, "one.logarchive")
    _make_logarchive(multiple, "two.logarchive")
    (multiple / "crashes").mkdir()
    (multiple / "live_syslog.txt").write_text("synthetic\n", encoding="utf-8")
    with pytest.raises(ValueError, match="ambiguous_multiple_logarchives"):
        classify_apple_package_shape(multiple)


def test_explicit_profile_mismatch_is_rejected(tmp_path: Path) -> None:
    foss, _ = _make_foss_collect(tmp_path)
    with pytest.raises(ValueError, match="profile_shape_mismatch_sysdiagnose"):
        classify_apple_package_shape(foss, profile="ios-sysdiagnose")


def test_shareable_graph_bounds_rows_and_omits_messages(tmp_path: Path) -> None:
    root, excerpt = _make_foss_collect(tmp_path)
    output = tmp_path / "shareable.jsonld"
    result = build_acquisition_package_graph(
        root,
        output,
        max_event_records=2,
        event_excerpt_path=excerpt,
        shareable=True,
    )

    assert result.event_record_count == 2
    payload = result.safe_metadata()
    assert payload["event_records"] == 2
    assert payload["redaction"]["raw_lines_included"] is False
    response_text = json.dumps(payload)
    assert "202-555-0199" not in response_text
    assert "490154203237518" not in response_text
    assert "Call +1" not in response_text

    raw = output.read_text(encoding="utf-8")
    assert str(tmp_path) not in raw
    assert root.name not in raw
    assert "202-555-0199" not in raw
    assert "490154203237518" not in raw
    assert "Call +1" not in raw
    assert "0000000000000001.tracev3" not in raw
    assert "com.example.one" not in raw

    nodes = _nodes(output)
    records = _nodes_of_type(nodes, "uco-observable:EventRecord")
    assert len(records) == 2
    assert all(
        "uco-observable:eventRecordText" not in node["uco-core:hasFacet"][0]
        for node in records
    )
    assert len(_nodes_of_type(nodes, "case-investigation:Investigation")) == 1
    assert len(_nodes_of_type(nodes, "case-investigation:ProvenanceRecord")) == 1
    archives = _nodes_of_type(nodes, "solveit-observable:AppleUnifiedLogArchive")
    assert len(archives) == 1
    assert "uco-observable:EventLog" in archives[0]["@type"]


def test_built_graph_passes_extension_aware_validation(tmp_path: Path) -> None:
    graph_validator = pytest.importorskip("graph_validator")
    if not graph_validator.validator_available():
        pytest.skip("case_validate not installed")

    root, excerpt = _make_foss_collect(tmp_path)
    output = tmp_path / "validated.jsonld"
    build_acquisition_package_graph(
        root,
        output,
        max_event_records=2,
        event_excerpt_path=excerpt,
    )
    report = graph_validator.validate_graph_file(
        output,
        extensions=["solveit"],
        project_root=Path(__file__).resolve().parents[2],
        strict_concepts=True,
    )
    assert report.conforms is True, report.safe_summary


def test_shareable_message_redaction_uses_placeholder(tmp_path: Path) -> None:
    root, excerpt = _make_foss_collect(tmp_path)
    output = tmp_path / "redacted.jsonld"
    result = build_acquisition_package_graph(
        root,
        output,
        max_event_records=1,
        event_excerpt_path=excerpt,
        shareable=True,
        event_message_policy="redact",
    )
    assert result.messages_affected == 1
    raw = output.read_text(encoding="utf-8")
    assert "[REDACTED:message]" in raw
    assert "202-555-0199" not in raw


def test_shareable_mode_rejects_unredacted_message_inclusion(tmp_path: Path) -> None:
    root, excerpt = _make_foss_collect(tmp_path)
    with pytest.raises(ValueError, match="shareable_message_policy_unsafe"):
        build_acquisition_package_graph(
            root,
            tmp_path / "unsafe.jsonld",
            max_event_records=1,
            event_excerpt_path=excerpt,
            shareable=True,
            event_message_policy="include",
        )


def test_timesync_guidance_omits_absolute_time_by_default(tmp_path: Path) -> None:
    root, excerpt = _make_foss_collect(tmp_path)
    output = tmp_path / "no-timesync.jsonld"
    result = build_acquisition_package_graph(
        root,
        output,
        max_event_records=1,
        event_excerpt_path=excerpt,
    )
    assert "timesync_missing_absolute_time_omitted" in result.warnings
    record_facet = _nodes_of_type(_nodes(output), "uco-observable:EventRecord")[0]["uco-core:hasFacet"][0]
    assert "uco-observable:observableCreatedTime" not in record_facet
    assert "uco-observable:startTime" not in record_facet


def test_inventory_json_supports_explicit_timesync_anchor(tmp_path: Path) -> None:
    package = tmp_path / "inventory-bytes"
    package.mkdir()
    archive = _make_logarchive(package, "standalone.logarchive")
    (package / "crashes").mkdir()
    (package / "live_syslog.txt").write_text("synthetic\n", encoding="utf-8")
    excerpt = package / "events.csv"
    excerpt.write_text(
        "timestamp,subsystem,message\n"
        "2026-08-11T12:00:00+00:00,com.apple.synthetic,synthetic message\n",
        encoding="utf-8",
    )
    inventory = package / "inventory.json"
    entries = []
    for path in sorted(package.rglob("*")):
        if path == inventory:
            continue
        entries.append({
            "path": path.relative_to(package).as_posix(),
            "type": "directory" if path.is_dir() else "file",
            "size": 0 if path.is_dir() else path.stat().st_size,
        })
    inventory.write_text(json.dumps({
        "root_name": "synthetic-foss-package",
        "base_path": str(package),
        "metadata": {
            "timesync_present": True,
            "timesync_anchored": True,
            "event_excerpt_path": "events.csv",
        },
        "entries": entries,
    }), encoding="utf-8")

    output = tmp_path / "anchored.jsonld"
    result = build_acquisition_package_graph(
        inventory,
        output,
        max_event_records=1,
        event_message_policy="omit",
    )
    assert result.profile == "apple-foss-logarchive"
    record_facet = _nodes_of_type(_nodes(output), "uco-observable:EventRecord")[0]["uco-core:hasFacet"][0]
    assert record_facet["uco-observable:observableCreatedTime"]["@type"] == "xsd:dateTime"
    assert record_facet["uco-observable:startTime"]["@value"].endswith("+00:00")
    assert archive.is_dir()  # fixture sanity: binary archive remained external


def test_inventory_metadata_excerpt_must_stay_inside_package(tmp_path: Path) -> None:
    package = tmp_path / "package"
    package.mkdir()
    _make_logarchive(package, "standalone.logarchive")
    (package / "crashes").mkdir()
    (package / "live_syslog.txt").write_text("synthetic\n", encoding="utf-8")
    outside = tmp_path / "outside.jsonl"
    outside.write_text('{"message":"must not be read"}\n', encoding="utf-8")
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps({
        "base_path": str(package),
        "metadata": {"event_excerpt_path": "../outside.jsonl"},
        "entries": [
            {"path": "standalone.logarchive", "type": "directory"},
            {"path": "crashes", "type": "directory"},
            {"path": "live_syslog.txt", "type": "file", "size": 10},
        ],
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="inventory_path_not_relative"):
        build_acquisition_package_graph(
            inventory,
            tmp_path / "escaped.jsonld",
            max_event_records=1,
        )


def test_inventory_entry_symlink_cannot_escape_declared_base(tmp_path: Path) -> None:
    package = tmp_path / "package"
    package.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("sensitive", encoding="utf-8")
    (package / "escape.txt").symlink_to(outside)
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps({
        "base_path": str(package),
        "entries": [{"path": "escape.txt", "type": "file", "size": 9}],
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="inventory_entry_outside_base"):
        classify_apple_package_shape(inventory)


def test_inventory_digest_is_verified_when_bytes_are_available(tmp_path: Path) -> None:
    package, _ = _make_foss_collect(tmp_path)
    inventory = tmp_path / "inventory.json"
    entries = []
    for path in sorted(package.rglob("*")):
        entry = {
            "path": path.relative_to(package).as_posix(),
            "type": "directory" if path.is_dir() else "file",
            "size": 0 if path.is_dir() else path.stat().st_size,
        }
        if path.name == "synthetic-crash.ips":
            entry["sha256"] = "0" * 64
        entries.append(entry)
    inventory.write_text(json.dumps({
        "base_path": str(package),
        "entries": entries,
    }), encoding="utf-8")

    result = build_acquisition_package_graph(
        inventory,
        tmp_path / "digest-mismatch.jsonld",
    )
    assert "crash_sample_digest_mismatch" in result.warnings
    assert not any(
        item["artifact_role"].startswith("crash-sample")
        for item in result.named_file_digests
    )


def test_string_timesync_flag_does_not_authorize_absolute_time(tmp_path: Path) -> None:
    package, excerpt = _make_foss_collect(tmp_path)
    inventory = tmp_path / "inventory.json"
    entries = [
        {
            "path": path.relative_to(package).as_posix(),
            "type": "directory" if path.is_dir() else "file",
            "size": 0 if path.is_dir() else path.stat().st_size,
        }
        for path in sorted(package.rglob("*"))
    ]
    inventory.write_text(json.dumps({
        "base_path": str(package),
        "metadata": {
            "timesync_present": "true",
            "timesync_anchored": "true",
            "event_excerpt_path": excerpt.relative_to(package).as_posix(),
        },
        "entries": entries,
    }), encoding="utf-8")

    output = tmp_path / "untrusted-timesync.jsonld"
    build_acquisition_package_graph(inventory, output, max_event_records=1)
    record_facet = _nodes_of_type(_nodes(output), "uco-observable:EventRecord")[0]["uco-core:hasFacet"][0]
    assert "uco-observable:observableCreatedTime" not in record_facet
    assert "uco-observable:startTime" not in record_facet


def test_jsonl_physical_line_is_bounded_before_parsing(tmp_path: Path) -> None:
    root, excerpt = _make_foss_collect(tmp_path)
    excerpt.write_text(
        json.dumps({"message": "x" * MAX_EVENT_LINE_BYTES}) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="event_excerpt_row_oversized"):
        build_acquisition_package_graph(
            root,
            tmp_path / "oversized-row.jsonld",
            max_event_records=1,
            event_excerpt_path=excerpt,
        )


def test_separate_package_graphs_use_disjoint_node_ids(tmp_path: Path) -> None:
    root, _ = _make_foss_collect(tmp_path)
    first = tmp_path / "first.jsonld"
    second = tmp_path / "second.jsonld"
    build_acquisition_package_graph(root, first)
    build_acquisition_package_graph(root, second)

    first_ids = {node["@id"] for node in _nodes(first)}
    second_ids = {node["@id"] for node in _nodes(second)}
    assert first_ids.isdisjoint(second_ids)


def test_server_registers_apple_tools() -> None:
    server_source = (Path(__file__).resolve().parent.parent / "server.py").read_text(encoding="utf-8")
    assert "@mcp.tool\ndef classify_apple_package_shape(" in server_source
    assert "@mcp.tool\ndef build_acquisition_package_graph(" in server_source


def test_server_wrappers_return_typed_safe_results(tmp_path: Path) -> None:
    pytest.importorskip("fastmcp")
    import server

    root, excerpt = _make_foss_collect(tmp_path)
    classified = server.classify_apple_package_shape(str(root))
    assert classified["ok"] is True
    assert classified["profile"] == "apple-foss-logarchive"

    built = server.build_acquisition_package_graph(
        str(root),
        str(tmp_path / "server-built.jsonld"),
        max_event_records=1,
        event_excerpt_path=str(excerpt),
    )
    assert built["ok"] is True
    assert built["event_records"] == 1
    assert "Call +1" not in json.dumps(built)

    ambiguous = tmp_path / "ambiguous"
    ambiguous.mkdir()
    _make_logarchive(ambiguous, "only.logarchive")
    refused = server.classify_apple_package_shape(str(ambiguous))
    assert refused["ok"] is False
    assert refused["error"] == "ambiguous_apple_package_shape"


def test_max_event_records_is_hard_bounded(tmp_path: Path) -> None:
    root, excerpt = _make_foss_collect(tmp_path)
    with pytest.raises(ValueError, match="max_event_records_out_of_range"):
        build_acquisition_package_graph(
            root,
            tmp_path / "too-many.jsonld",
            max_event_records=MAX_EVENT_RECORDS + 1,
            event_excerpt_path=excerpt,
        )
