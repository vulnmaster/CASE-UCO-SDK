#!/usr/bin/env python3
"""Build a validated CASE/UCO graph for iOS sysdiagnose + Apple Unified Logs.

Grounded in the DFRWS USA workshop corpus layout under
E:\\DFRWS_USA\\Sysdiagnosis (sysdiagnose_2024.08.02_*_iPhone-OS_*_21D50):

* Raw sysdiagnose directory with system_logs.logarchive (Persist/Signpost/
  Special/.tracev3), WiFi plists, BatteryBDC CSVs, and summaries/
* Analytic tools shipped alongside the data: Mandiant unifiedlog_iterator
  (CSV/JSON), Lionel Notari iOS Unified Logs parser (SQLite), iLEAPP

Device/OS fields (ProductVersion 17.3, ProductBuildVersion 21D50) and one
WiFi SSID/BSSID pair are taken from SystemVersion.plist and
com.apple.wifi-private-mac-networks.plist in that corpus. Unified-log
*message* rows are Tier T0 exemplars shaped like unifiedlog_iterator CSV
columns (the workshop tree contains the binary logarchive, not a pre-parsed
CSV dump). Battery CSV fields are taken from a real BDC_Daily_* file header
and first data row.

Validated against CASE 1.4.0 + solveit extension (AppleUnifiedLogArchive,
SolveitInvestigativeAction / DFT-1066, DFT-1076).
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def _is_repo_root(candidate: Path) -> bool:
    return (candidate / "docs" / "recipes" / "recipe-execution.json").is_file() and (
        candidate / "packages" / "case-uco-solveit" / "python"
    ).is_dir()


def _find_repo_root() -> Path:
    """Resolve CASE-UCO-Libraries root when run in-tree or from recipe-execution temp dirs."""
    if "CASE_UCO_LIBRARIES_ROOT" in os.environ:
        candidate = Path(os.environ["CASE_UCO_LIBRARIES_ROOT"]).resolve()
        if not _is_repo_root(candidate):
            raise RuntimeError(
                f"CASE_UCO_LIBRARIES_ROOT is not a CASE-UCO-Libraries root: {candidate}"
            )
        return candidate

    here = Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if _is_repo_root(candidate):
            return candidate

    # recipe-execution copies this script to /tmp; recover root from PYTHONPATH.
    for part in os.environ.get("PYTHONPATH", "").split(os.pathsep):
        if not part:
            continue
        p = Path(part).resolve()
        if p.name == "mcp_server" and _is_repo_root(p.parent):
            return p.parent
        if p.name == "python" and _is_repo_root(p.parent):
            return p.parent
        if _is_repo_root(p):
            return p

    raise RuntimeError(
        "Could not locate CASE-UCO-Libraries root; set CASE_UCO_LIBRARIES_ROOT"
    )


# Bytes for these workshop containers / Tier-T0 tool outputs are not shipped
# in-repo; do not invent digests — tag hash unavailability instead.
_NO_HASH_TAGS = ["hash-status:not-published", "source-bytes:not-acquired"]

_SOLVEIT_CONTEXT = {
    "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
    "solveit-observable": "https://ontology.solveit-df.org/solveit/observable/",
    "solveit-data": "https://ontology.solveit-df.org/solveit/data/",
}


ROOT = _find_repo_root()
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "packages" / "case-uco-solveit" / "python"))
sys.path.insert(0, str(ROOT / "mcp_server"))

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.core import Event
from case_uco.uco.identity import Identity
from case_uco.uco.observable import (
    ApplicationFacet,
    ContentDataFacet,
    DeviceFacet,
    EventRecord,
    EventRecordFacet,
    FileFacet,
    MACAddressFacet,
    ObservableObject,
    ObservableRelationship,
    OperatingSystem,
    SoftwareFacet,
    WirelessNetworkConnection,
    WirelessNetworkConnectionFacet,
)
from case_uco.uco.tool import AnalyticTool, Tool
from case_uco.uco.types import Dictionary, DictionaryEntry, Hash
from case_uco_solveit.solveit_core import SolveitInvestigativeAction
from case_uco_solveit.solveit_observable import AppleUnifiedLogArchive
from graph_validator import report_to_dict, validate_graph_file, validator_available

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ios-sysdiagnose-unified-logs.jsonld"
# Also refresh the in-repo exemplar when the builder is not running in a temp gate.
REPO_OUTPUT = ROOT / "examples" / "sysdiagnose" / "ios-sysdiagnose-unified-logs.jsonld"
SAMPLE_ROWS = ROOT / "examples" / "sysdiagnose" / "unifiedlog_iterator_sample_rows.json"
EXCERPT_SHA256 = (
    ROOT / "examples" / "sysdiagnose" / "unifiedlog_iterator_excerpt.sha256"
)
CASE_ID = "dfrws-sysdiagnose-2024-08-02"
TZ = timezone(timedelta(hours=-4))  # archive name ...-0400
SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"


def _load_iterator_samples() -> tuple[list[dict], str]:
    import json

    # recipe-execution copies support_files next to the builder in /tmp.
    rows_path = SAMPLE_ROWS if SAMPLE_ROWS.is_file() else HERE / SAMPLE_ROWS.name
    sha_path = EXCERPT_SHA256 if EXCERPT_SHA256.is_file() else HERE / EXCERPT_SHA256.name
    meta = json.loads(rows_path.read_text(encoding="utf-8"))
    # Standard `sha256sum` format ("<hex>  <filename>"); take the digest field.
    digest = sha_path.read_text(encoding="utf-8").split()[0]
    return list(meta.get("rows") or []), digest


def _patch_types(graph: CASEGraph, instance, *extra: str) -> None:
    """Append additional @type IRIs/curie strings on a created node."""
    obj_id = graph.get_id(instance)
    for obj in graph._objects:
        if obj.get("@id") == obj_id:
            current = obj["@type"]
            types = [current] if isinstance(current, str) else list(current)
            for t in extra:
                if t not in types:
                    types.append(t)
            obj["@type"] = types
            return
    raise KeyError(obj_id)


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=_SOLVEIT_CONTEXT)
    relationships: list = []

    def rel(**kwargs):
        edge = graph.create(ObservableRelationship, **kwargs)
        relationships.append(edge)
        return edge

    apple = graph.create(Identity, name="Apple Inc.")

    phone = graph.create(
        ObservableObject,
        name="iPhone (sysdiagnose 2024-08-02)",
        description=[
            "Hardware model iPhone12,1 (iPhone 11) from "
            "crashes_and_spins/stacks-2024-08-02-161926.ips header "
            '("product": "iPhone12,1").'
        ],
        has_facet=[
            DeviceFacet(
                manufacturer=apple,
                model="iPhone12,1",
                device_type="Mobile Phone",
            ),
        ],
    )

    ios = graph.create(
        OperatingSystem,
        name="iPhone OS 17.3 (21D50)",
        has_facet=[
            SoftwareFacet(
                manufacturer=apple,
                version="17.3",
            ),
        ],
        description=[
            "Source: logs/SystemVersion/SystemVersion.plist — "
            "ProductName=iPhone OS, ProductVersion=17.3, "
            "ProductBuildVersion=21D50",
        ],
    )
    _patch_types(graph, ios, "uco-observable:Software")
    # ObservableObjectRelationshipVocab: device characterized by its OS.
    rel(
        is_directional=True,
        kind_of_relationship="Characterized_By",
        source=[phone],
        target=ios,
    )

    # --- Raw sysdiagnose container ---
    sysdiag = graph.create(
        ObservableObject,
        name="sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50",
        tag=list(_NO_HASH_TAGS),
        has_facet=[
            FileFacet(
                file_name=["sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50"],
                file_path=[
                    "Data/sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50"
                ],
                is_directory=[True],
            ),
        ],
        description=[
            "Apple sysdiagnose archive root: summaries/, logs/, WiFi/, "
            "system_logs.logarchive, crashes_and_spins/, Preferences/, etc."
        ],
    )
    rel(
        is_directional=True,
        kind_of_relationship="Extracted_From",
        source=[sysdiag],
        target=phone,
    )

    # --- Unified log archive (SOLVE-IT typed) ---
    logarchive = graph.create(
        AppleUnifiedLogArchive,
        name="system_logs.logarchive",
        tag=list(_NO_HASH_TAGS),
        has_facet=[
            FileFacet(
                file_name=["system_logs.logarchive"],
                file_path=[
                    "Data/sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50/"
                    "system_logs.logarchive"
                ],
                is_directory=[True],
                size_in_bytes=22193292,
            ),
        ],
        description=[
            "Apple Unified Logging logarchive with Persist/, Signpost/, "
            "Special/, Extra/, and UUID-keyed .tracev3 stores "
            "(e.g. Persist/0000000000000007.tracev3)."
        ],
    )
    _patch_types(graph, logarchive, "uco-observable:EventLog")
    rel(
        is_directional=True,
        kind_of_relationship="Contained_Within",
        source=[logarchive],
        target=sysdiag,
    )

    # --- WiFi known-network artifact from sysdiagnose ---
    wifi_plist = graph.create(
        ObservableObject,
        name="com.apple.wifi-private-mac-networks.plist",
        tag=list(_NO_HASH_TAGS),
        has_facet=[
            FileFacet(
                file_name=["com.apple.wifi-private-mac-networks.plist"],
                file_path=[
                    "Data/sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50/"
                    "WiFi/com.apple.wifi-private-mac-networks.plist"
                ],
                size_in_bytes=7443,
            ),
        ],
    )
    rel(
        is_directional=True,
        kind_of_relationship="Contained_Within",
        source=[wifi_plist],
        target=sysdiag,
    )

    bssid_addr = graph.create(
        ObservableObject,
        name="BSSID 6a:22:32:98:f4:df",
        has_facet=[MACAddressFacet(address_value="6a:22:32:98:f4:df")],
    )
    wifi_net = graph.create(
        WirelessNetworkConnection,
        name="Wi-Fi network Matt_Foley",
        has_facet=[
            WirelessNetworkConnectionFacet(
                ssid="Matt_Foley",
                base_station="6a:22:32:98:f4:df",
            ),
        ],
        description=[
            "Source: WiFi/com.apple.wifi-private-mac-networks.plist entry "
            "SSID_STR=Matt_Foley, BSSID=6a:22:32:98:f4:df, "
            "lastJoined=2023-07-15 19:44:33"
        ],
    )
    rel(
        is_directional=True,
        kind_of_relationship="Characterized_By",
        source=[wifi_net],
        target=wifi_plist,
    )
    rel(
        is_directional=True,
        kind_of_relationship="Resolved_To",
        source=[wifi_net],
        target=bssid_addr,
    )

    # --- BatteryBDC structured CSV inside sysdiagnose ---
    battery_csv = graph.create(
        ObservableObject,
        name="BDC_Daily_version2.0_2023-07-01_20_16_03.csv",
        tag=list(_NO_HASH_TAGS),
        has_facet=[
            FileFacet(
                file_name=["BDC_Daily_version2.0_2023-07-01_20_16_03.csv"],
                file_path=[
                    "Data/sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50/"
                    "logs/BatteryBDC/BDC_Daily_version2.0_2023-07-01_20_16_03.csv"
                ],
            ),
        ],
        description=[
            "Battery Data Collection daily CSV: TimeStamp, WeightedRa, Qmax0, "
            "CycleCount, NominalChargeCapacity, ..."
        ],
    )
    rel(
        is_directional=True,
        kind_of_relationship="Contained_Within",
        source=[battery_csv],
        target=sysdiag,
    )

    battery_row = graph.create(
        EventRecord,
        name="BDC Daily sample 2023-07-01T20:16:03",
        has_facet=[
            EventRecordFacet(
                event_record_id="BDC-2023-07-01T20:16:03",
                event_type="information",
                event_record_service_name="BatteryBDC",
                event_record_text=(
                    "CycleCount=811 NominalChargeCapacity=2432 WeightedRa=244"
                ),
                observable_created_time=datetime(2023, 7, 1, 20, 16, 3, tzinfo=TZ),
                event_record_device=phone,
                start_time=datetime(2023, 7, 1, 20, 16, 3, tzinfo=TZ),
            ),
        ],
    )
    rel(
        is_directional=True,
        kind_of_relationship="Contained_Within",
        source=[battery_row],
        target=battery_csv,
    )
    battery_event = graph.create(
        Event,
        name="Battery health sample 2023-07-01",
        start_time=[datetime(2023, 7, 1, 20, 16, 3, tzinfo=TZ)],
        event_type=["BatteryBDC_Daily"],
        event_context=[battery_row, battery_csv],
        event_attribute=[
            Dictionary(
                entry=[
                    DictionaryEntry(key="CycleCount", value="811"),
                    DictionaryEntry(key="NominalChargeCapacity", value="2432"),
                    DictionaryEntry(key="WeightedRa", value="244"),
                    DictionaryEntry(key="Qmax0", value="2988"),
                ]
            )
        ],
    )

    # --- Acquisition / collection tools ---
    ufad = graph.create(
        Tool,
        name="UFADE",
        version="0.9.9",
        tool_type="Mobile Acquisition",
        description=["Workshop tool tree: Tools/UFADE_0.9.9_win_x64"],
    )
    pymobile = graph.create(
        Tool,
        name="pymobiledevice3",
        tool_type="Mobile Device Bridge",
        description=["Supports syslog live and crash pull; workshop Tools/pymobiledevice3-master"],
    )

    collect_action = graph.create(
        InvestigativeAction,
        name="Collect iOS sysdiagnose",
        description=[
            "Preserve sysdiagnose package containing system_logs.logarchive "
            "and ancillary logs/WiFi/summaries (SOLVE-IT DFO-1006 / DFT-1016)."
        ],
        instrument=[ufad, pymobile],
        object=[phone],
        result=[sysdiag, logarchive],
        start_time=datetime(2024, 8, 2, 16, 19, 26, tzinfo=TZ),
        end_time=datetime(2024, 8, 2, 16, 20, 10, tzinfo=TZ),
    )

    # --- Analytic tools + structured outputs ---
    iterator_tool = graph.create(
        AnalyticTool,
        name="unifiedlog_iterator",
        version="0.4.0",
        tool_type="Unified Log Parser",
        description=[
            "Mandiant/macos-unifiedlogs iterator; workshop binary "
            "Tools/unifiedlog_iterator-v0.4.0-x86_64-pc-windows-msvc"
        ],
    )
    notari_tool = graph.create(
        AnalyticTool,
        name="iOS Unified Logs parsing V2 (Lionel Notari)",
        tool_type="Unified Log Parser",
        description=[
            "Parses .logarchive via log show → JSON → SQLite full + filtered DBs "
            "and forensic report (workshop Tools/iOS Unified Logs v2)"
        ],
    )
    ileapp_tool = graph.create(
        AnalyticTool,
        name="iLEAPP",
        tool_type="Mobile Artifact Parser",
        description=["Workshop Tools/iLEAPP-main — artifact HTML/TSV reports"],
    )

    sample_rows, excerpt_sha256 = _load_iterator_samples()

    csv_out = graph.create(
        ObservableObject,
        name="unifiedlog_iterator_excerpt.jsonl",
        has_facet=[
            FileFacet(
                file_name=["unifiedlog_iterator_excerpt.jsonl"],
                file_path=["examples/sysdiagnose/unifiedlog_iterator_excerpt.jsonl"],
            ),
            ContentDataFacet(
                hash=[
                    Hash(
                        hash_method="SHA256",
                        hash_value=excerpt_sha256,
                    )
                ],
            ),
        ],
        description=[
            "Retained excerpt of Mandiant unifiedlog_iterator v0.4.0 "
            "log-archive JSONL parse of the workshop system_logs.logarchive. "
            "Full parse completed exit=0; archive has no timesync DB so tool "
            "wall-clock timestamps stay epoch-relative — model "
            "mach_continuous_time / boot_uuid / timezone_name instead."
        ],
    )

    sqlite_out = graph.create(
        ObservableObject,
        name="notari-unified-logs-filtered.sqlite",
        tag=list(_NO_HASH_TAGS),
        has_facet=[
            FileFacet(
                file_name=["notari-unified-logs-filtered.sqlite"],
                file_path=["analysis/notari-unified-logs-filtered.sqlite"],
            ),
        ],
        description=[
            "Tier T0 shape of Notari filtered SQLite DB of unified log "
            "events (rule-based / custom_rules.json) — dual-tool companion "
            "to the iterator excerpt."
        ],
    )

    ileapp_report = graph.create(
        ObservableObject,
        name="iLEAPP-sysdiagnose-report",
        tag=list(_NO_HASH_TAGS),
        has_facet=[
            FileFacet(
                file_name=["iLEAPP_Report"],
                file_path=["analysis/iLEAPP_Report"],
                is_directory=[True],
            ),
        ],
        description=["Tier T0 exemplar of iLEAPP HTML artifact report tree"],
    )

    analyticsd = graph.create(
        ObservableObject,
        name="analyticsd",
        has_facet=[
            ApplicationFacet(application_identifier="com.apple.analyticsd")
        ],
    )

    ul_records = []
    ul_events = []
    for idx, row in enumerate(sample_rows):
        service = row.get("subsystem") or "unknown"
        record = graph.create(
            EventRecord,
            name=f"Unified log row {idx + 1}: {service}",
            description=[
                "Source: unifiedlog_iterator log-archive parse of workshop "
                "system_logs.logarchive (see unifiedlog_iterator_sample_rows.json). "
                "Wall-clock timestamp_tool is unanchored (no timesync)."
            ],
            has_facet=[
                EventRecordFacet(
                    # Honest excerpt row index; the tool-reported activity_id
                    # is preserved as a DictionaryEntry on the companion Event.
                    event_record_id=f"excerpt-row-{idx}",
                    event_type=str(row.get("log_type") or row.get("event_type") or "Log"),
                    event_record_service_name=service,
                    event_record_text=str(row.get("message") or ""),
                    event_record_device=phone,
                    application=analyticsd if "analyticsd" in str(row.get("message")) else None,
                ),
            ],
        )
        rel(
            is_directional=True,
            kind_of_relationship="Extracted_From",
            source=[record],
            target=logarchive,
        )
        rel(
            is_directional=True,
            kind_of_relationship="Contained_Within",
            source=[record],
            target=csv_out,
        )
        entries = [
            DictionaryEntry(key="subsystem", value=str(service)),
            DictionaryEntry(key="mach_continuous_time", value=str(row.get("mach_continuous_time"))),
            DictionaryEntry(key="boot_uuid", value=str(row.get("boot_uuid"))),
            DictionaryEntry(key="timezone_name", value=str(row.get("timezone_name"))),
            DictionaryEntry(key="timestamp_tool", value=str(row.get("timestamp_tool"))),
            DictionaryEntry(key="pid", value=str(row.get("pid"))),
            DictionaryEntry(key="thread_id", value=str(row.get("thread_id"))),
            DictionaryEntry(key="log_type", value=str(row.get("log_type"))),
            DictionaryEntry(key="event_type", value=str(row.get("event_type"))),
        ]
        if row.get("euid") is not None:
            entries.append(DictionaryEntry(key="euid", value=str(row["euid"])))
        if row.get("activity_id") is not None:
            entries.append(DictionaryEntry(key="activity_id", value=str(row["activity_id"])))
        if row.get("library"):
            entries.append(DictionaryEntry(key="library", value=str(row["library"])))
        if row.get("category"):
            entries.append(DictionaryEntry(key="category", value=str(row["category"])))
        if row.get("process"):
            entries.append(DictionaryEntry(key="process", value=str(row["process"])))
        event = graph.create(
            Event,
            name=f"Unified log event {idx + 1}",
            description=[
                "Absolute wall-clock time omitted: archive has no timesync; "
                "see eventAttribute mach_continuous_time / boot_uuid."
            ],
            event_type=["unifiedlog", str(row.get("log_type") or "Log")],
            event_context=[record, phone],
            event_attribute=[Dictionary(entry=entries)],
        )
        ul_records.append(record)
        ul_events.append(event)

    # SolveitInvestigativeAction (case_uco_solveit >= 0.2.0) serializes
    # uco-action:* keys and SOLVE-IT method links natively.
    parse_iterator = graph.create(
        SolveitInvestigativeAction,
        name="Parse logarchive with unifiedlog_iterator",
        description=[
            "SOLVE-IT DFT-1066 / DFT-1076: extract OS unified-log artifacts "
            "from system_logs.logarchive to JSONL (DFM-1027 dual-tool verify "
            "with Notari parser). Applied DFM-1179 timezone/timesync check: "
            "archive lacks timesync — absolute times not asserted."
        ],
        instrument=[iterator_tool],
        object=[logarchive],
        result=[csv_out, *ul_records, *ul_events],
        start_time=datetime(2026, 7, 27, 15, 35, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 27, 15, 36, 0, tzinfo=timezone.utc),
        used_technique=[
            {"@id": SOLVEIT_DATA + "techniqueDFT-1066"},
            {"@id": SOLVEIT_DATA + "techniqueDFT-1076"},
        ],
        applied_mitigation=[
            {"@id": SOLVEIT_DATA + "mitigationDFM-1027"},
            {"@id": SOLVEIT_DATA + "mitigationDFM-1175"},
            {"@id": SOLVEIT_DATA + "mitigationDFM-1179"},
        ],
    )

    parse_notari = graph.create(
        SolveitInvestigativeAction,
        name="Parse logarchive with Notari Unified Logs tools",
        description=[
            "SOLVE-IT DFT-1066 / DFT-1076: build full + filtered SQLite "
            "databases and forensic report from the same .logarchive — the "
            "DFM-1027 dual-tool companion to the unifiedlog_iterator parse."
        ],
        instrument=[notari_tool],
        object=[logarchive],
        result=[sqlite_out],
        start_time=datetime(2026, 7, 25, 19, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 25, 19, 50, 0, tzinfo=timezone.utc),
        used_technique=[
            {"@id": SOLVEIT_DATA + "techniqueDFT-1066"},
            {"@id": SOLVEIT_DATA + "techniqueDFT-1076"},
        ],
        applied_mitigation=[
            {"@id": SOLVEIT_DATA + "mitigationDFM-1027"},
        ],
    )

    parse_ileapp = graph.create(
        SolveitInvestigativeAction,
        name="Run iLEAPP against sysdiagnose",
        description=[
            "SOLVE-IT DFT-1066 / DFT-1076: parse sysdiagnose-contained "
            "OS-stored artifacts (WiFi, location, powerlog, etc.) into "
            "HTML/TSV report modules."
        ],
        instrument=[ileapp_tool],
        object=[sysdiag],
        result=[ileapp_report, wifi_net],
        start_time=datetime(2026, 7, 25, 20, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 25, 20, 20, 0, tzinfo=timezone.utc),
        used_technique=[
            {"@id": SOLVEIT_DATA + "techniqueDFT-1066"},
            {"@id": SOLVEIT_DATA + "techniqueDFT-1076"},
        ],
    )

    provenance = graph.create(
        ProvenanceRecord,
        description=["Sysdiagnose + unified log examination package"],
        exhibit_number="EX-SYSDIAG-2024-0802",
        object=[
            collect_action,
            parse_iterator,
            parse_notari,
            parse_ileapp,
            sysdiag,
            logarchive,
            csv_out,
            sqlite_out,
        ],
    )

    graph.create(
        Investigation,
        name=f"Case {CASE_ID}: iOS sysdiagnose and unified logs",
        description=[
            "Model raw Apple sysdiagnose (including system_logs.logarchive) "
            "and structured analytic outputs (unifiedlog_iterator JSONL excerpt, "
            "Notari SQLite, iLEAPP reports). Grounded in DFRWS USA Sysdiagnosis "
            "workshop data; iterator rows are real parse excerpts."
        ],
        object=[
            apple,
            phone,
            ios,
            sysdiag,
            logarchive,
            wifi_plist,
            wifi_net,
            bssid_addr,
            battery_csv,
            battery_row,
            battery_event,
            ufad,
            pymobile,
            iterator_tool,
            notari_tool,
            ileapp_tool,
            analyticsd,
            csv_out,
            sqlite_out,
            ileapp_report,
            *ul_records,
            *ul_events,
            collect_action,
            parse_iterator,
            parse_notari,
            parse_ileapp,
            provenance,
            *relationships,
        ],
    )

    # Manual @type / property patches use solveit-* curies; keep those
    # prefixes in the serialized context (pruned context tracks create() only).
    graph._used_prefix_set.update(_SOLVEIT_CONTEXT.keys())
    return graph


def main() -> int:
    import json

    graph = build()
    graph.write(str(OUTPUT), indent=2)
    print(f"Wrote {OUTPUT}")
    if REPO_OUTPUT.resolve() != OUTPUT.resolve():
        REPO_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        graph.write(str(REPO_OUTPUT), indent=2)
        print(f"Wrote {REPO_OUTPUT}")

    if not validator_available():
        print("validator unavailable", file=sys.stderr)
        return 2
    result = validate_graph_file(
        str(OUTPUT),
        extensions=["solveit"],
        allow_warning=True,
        strict_concepts=True,
    )
    payload = report_to_dict(result)
    print(json.dumps({
        "conforms": payload.get("conforms"),
        "violation_count": payload.get("violation_count"),
        "warning_count": payload.get("warning_count"),
        "undeclared_concepts": payload.get("undeclared_concepts"),
        "safe_summary": payload.get("safe_summary"),
    }, indent=2, default=str))
    return 0 if payload.get("conforms") else 1


if __name__ == "__main__":
    raise SystemExit(main())
