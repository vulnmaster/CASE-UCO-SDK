# Apple Unified Logs and Analytic Tool Outputs

> See [Recipe Index](INDEX.md) for all recipes.

Model **Apple Unified Logging** evidence — the binary `.logarchive` /
`.tracev3` stores and the structured outputs of common forensic parsers —
as CASE/UCO `EventLog` / `EventRecord` graphs with full tool provenance.

Typical workshop / lab toolchain (as shipped under
`E:\DFRWS_USA\Sysdiagnosis\...\Tools`):

| Tool | Structured output | Model as |
|---|---|---|
| Mandiant `unifiedlog_iterator` | CSV / JSON rows (timestamp, process, subsystem, category, message, pid, …) | `AnalyticTool` → CSV `FileFacet` + per-row `EventRecord` |
| Lionel Notari iOS Unified Logs v2 | Full + filtered SQLite DBs + `.txt` forensic report | `AnalyticTool` → SQLite file + filtered `EventRecord` set |
| iLEAPP | HTML/TSV artifact modules over sysdiagnose contents | `AnalyticTool` → report directory; link derived Wi-Fi / location artifacts |
| Apple `log show` (macOS) | JSON stream feeding Notari | Intermediate file optional |

Validated against `examples/sysdiagnose/ios-sysdiagnose-unified-logs.jsonld`
(`validate_graph(..., extensions=['solveit'])` → Conforms: True).

**When to use this recipe**

- You have `system_logs.logarchive` (often inside a sysdiagnose — see
  [ios-sysdiagnose.md](ios-sysdiagnose.md)) or a standalone Unified Log archive
- You ran `unifiedlog_iterator`, Notari parsers, `log show`, or iLEAPP and
  have CSV / SQLite / HTML outputs to encode
- You need per-event timeline nodes with subsystem/category/process attributes
- For Windows USN-style journals use [usn-journal.md](usn-journal.md); for
  generic auth events use [event.md](event.md)

## Classes and properties

| Class | Role |
|---|---|
| `solveit-observable:AppleUnifiedLogArchive` (+ `EventLog`) | Input `.logarchive` |
| `uco-observable:EventRecord` + `EventRecordFacet` | One unified-log (or CSV/SQLite) row |
| `uco-core:Event` + `Dictionary` / `DictionaryEntry` | Interpreted occurrence + subsystem/category/pid/… |
| `uco-observable:ObservableObject` + `ApplicationFacet` | Process / subsystem app (e.g. `locationd`) |
| `uco-tool:AnalyticTool` | unifiedlog_iterator / Notari / iLEAPP |
| `solveit-core:SolveitInvestigativeAction` | Parse step with `usedTechnique` / `appliedMitigation` |
| `uco-observable:ObservableObject` + `FileFacet` (+ `ContentDataFacet`) | CSV / SQLite / HTML report outputs |
| `uco-observable:ObservableRelationship` | `Extracted_From` archive; `Contained_Within` CSV/SQLite |

SOLVE-IT techniques commonly recorded on the parse action:

- `DFT-1066` — Extract artifacts from operating system log files
- `DFT-1076` — Extract artifacts from log files
- Mitigations: `DFM-1027` (dual-tool verification), `DFM-1175` (examine archives),
  `DFM-1179` (timezone applicable at generation)

## Field mapping (unifiedlog_iterator → CASE)

| Iterator / `log show` field | CASE property |
|---|---|
| timestamp (only if timesync-anchored) | `EventRecordFacet.observableCreatedTime` / `startTime`; `Event.startTime` |
| mach_continuous_time, boot_uuid, timezone_name | `DictionaryEntry` on `Event.eventAttribute` (prefer when archive has no timesync) |
| message | `EventRecordFacet.eventRecordText` |
| log_type / event_type | `EventRecordFacet.eventType`; also `Event.eventType` |
| subsystem | `EventRecordFacet.eventRecordServiceName` **and** `DictionaryEntry(key="subsystem")` |
| category, process, pid, thread_id, library, activity_id | `DictionaryEntry` on `Event.eventAttribute` |
| process (as app) | `EventRecordFacet.application` → `ApplicationFacet` |
| device | `EventRecordFacet.eventRecordDevice` → phone observable |

Do **not** invent a UnifiedLogFacet — use `EventRecordFacet` + `Dictionary`.

## Modeling pattern

```
AppleUnifiedLogArchive (system_logs.logarchive)
        ▲
        │ Extracted_From
EventRecord ── Contained_Within ──▶ CSV / SQLite / JSONL output file
    │
    └── Event
          ├── eventType = ["unifiedlog", "Default"]
          ├── eventContext ──▶ EventRecord, Application, Device
          └── eventAttribute ──▶ Dictionary (subsystem, mach_continuous_time, boot_uuid, …)
               (omit absolute Event.startTime when the archive has no timesync)

SolveitInvestigativeAction ("Parse logarchive with unifiedlog_iterator")
  ├── usedTechnique ──▶ DFT-1066, DFT-1076
  ├── appliedMitigation ──▶ DFM-1027, DFM-1175, DFM-1179
  ├── instrument ──▶ AnalyticTool (unifiedlog_iterator)
  ├── object ──▶ AppleUnifiedLogArchive
  └── result ──▶ CSV file, EventRecord(s), Event(s)
```

### Analytic tool + CSV/SQLite outputs

```python
from case_uco.uco.tool import AnalyticTool
from case_uco.uco.observable import FileFacet, ContentDataFacet
from case_uco.uco.types import Hash
from case_uco.case.investigation import InvestigativeAction

iterator_tool = graph.create(AnalyticTool,
    name="unifiedlog_iterator", version="0.4.0",
    tool_type="Unified Log Parser")
notari_tool = graph.create(AnalyticTool,
    name="iOS Unified Logs parsing V2 (Lionel Notari)",
    tool_type="Unified Log Parser")

csv_out = graph.create(ObservableObject,
    name="unifiedlog_iterator-output.csv",
    has_facet=[
        FileFacet(file_name=["unifiedlog_iterator-output.csv"],
                  file_path=["analysis/unifiedlog_iterator-output.csv"]),
        ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="…")]),
    ],
)
sqlite_out = graph.create(ObservableObject,
    name="notari-unified-logs-filtered.sqlite",
    has_facet=[FileFacet(
        file_name=["notari-unified-logs-filtered.sqlite"],
        file_path=["analysis/notari-unified-logs-filtered.sqlite"])],
)
```

### Per-row EventRecord + Event

When the `.logarchive` has **no timesync** database (common in some
sysdiagnose packages), Mandiant `unifiedlog_iterator` wall-clock stamps stay
epoch-relative — do **not** invent absolute `startTime` values. Prefer
`mach_continuous_time` / `boot_uuid` / `timezone_name` dictionary entries
from real parse rows (see `examples/sysdiagnose/unifiedlog_iterator_sample_rows.json`).

```python
from case_uco.uco.core import Event
from case_uco.uco.observable import (
    EventRecord, EventRecordFacet, ApplicationFacet, ObservableRelationship,
)
from case_uco.uco.types import Dictionary, DictionaryEntry

analyticsd = graph.create(ObservableObject, name="analyticsd",
    has_facet=[ApplicationFacet(application_identifier="com.apple.analyticsd")])

ul_record = graph.create(EventRecord,
    name="Unified log row 1: com.apple.analyticsd",
    description=["Source: unifiedlog_iterator log-archive parse; no timesync"],
    has_facet=[EventRecordFacet(
        event_record_id="0",
        event_id="0",
        event_type="Default",
        event_record_service_name="com.apple.analyticsd",
        event_record_text="…",  # only text the parser actually resolved
        event_record_device=phone,
        application=analyticsd,
    )],
)
graph.create(ObservableRelationship, is_directional=True,
    kind_of_relationship="Extracted_From", source=[ul_record], target=logarchive)
graph.create(ObservableRelationship, is_directional=True,
    kind_of_relationship="Contained_Within", source=[ul_record], target=csv_out)

graph.create(Event,
    name="Unified log event 1",
    description=["Absolute wall-clock omitted: archive has no timesync"],
    event_type=["unifiedlog", "Default"],
    event_context=[ul_record, phone],
    event_attribute=[Dictionary(entry=[
        DictionaryEntry(key="subsystem", value="com.apple.analyticsd"),
        DictionaryEntry(key="mach_continuous_time", value="…"),
        DictionaryEntry(key="boot_uuid", value="…"),
        DictionaryEntry(key="timezone_name", value="America/New_York"),
        DictionaryEntry(key="timestamp_tool", value="1970-…"),  # unanchored
        DictionaryEntry(key="pid", value="…"),
        DictionaryEntry(key="log_type", value="Default"),
    ])],
)
```

### SOLVE-IT-aware parse action

`case_uco_solveit.solveit_core.SolveitInvestigativeAction` (>= 0.2.0)
serializes `uco-action:*` keys and SOLVE-IT method links natively — pass
KB technique/mitigation IRIs as `{"@id": …}` references:

```python
from case_uco_solveit.solveit_core import SolveitInvestigativeAction

SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"

parse_action = graph.create(SolveitInvestigativeAction,
    name="Parse logarchive with unifiedlog_iterator",
    instrument=[iterator_tool],
    object=[logarchive],
    result=[csv_out, ul_record],
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
```

Prefer dual-tool verification: run Mandiant iterator **and** Notari (or
`log show`) and link both result files to the same archive via separate
actions that share `object=[logarchive]`.

### Structured artifacts already inside sysdiagnose

BatteryBDC daily CSVs (`logs/BatteryBDC/BDC_Daily_*.csv`) are structured
tool-like outputs *produced by the device*. Map interesting rows the same
way — `EventRecord` + `Event` with `DictionaryEntry` keys matching CSV
headers (`CycleCount`, `NominalChargeCapacity`, …) — and
`Contained_Within` the CSV file. iLEAPP HTML modules that restate Wi-Fi /
location facts should reference the same `WirelessNetworkConnection` nodes from
[ios-sysdiagnose.md](ios-sysdiagnose.md) (e.g. action `result` / shared IRIs),
not duplicate them.

## Anti-patterns

- **One EventRecord for the entire multi-GB CSV.** Partition by natural
  forensic boundaries (time window, subsystem of interest, filtered Notari
  DB) — never invent an arbitrary “first N thousand rows” split that breaks
  relationships.
- **Putting subsystem only in free-text description.** Use
  `eventRecordServiceName` and/or `DictionaryEntry`.
- **Using a pre-0.2.0 `case_uco_solveit` package.** Older
  `SolveitInvestigativeAction` dataclasses emitted `uco-core:instrument`
  (failing strict concept coverage); 0.2.0+ serializes `uco-action:*`
  keys and `usedTechnique`/`appliedMitigation` natively.
- **Claiming message text you did not parse.** Binary `.tracev3` rows need
  a parser; if you only have the archive, stop at the
  `AppleUnifiedLogArchive` node.
- **Inventing absolute wall-clock times** when the archive has no timesync —
  keep tool epoch stamps in a dictionary entry and model continuous time.
- **Embedding Wi-Fi passwords from `security.txt`.** SSIDs/BSSIDs only.

## Checklist

1. Confirm the input archive node exists ([ios-sysdiagnose.md](ios-sysdiagnose.md)).
2. Create `AnalyticTool` nodes for each parser actually run; hash output files.
3. For each retained log row: `EventRecord` + `Event` + `Dictionary` attributes.
4. Link records `Extracted_From` the logarchive and `Contained_Within` the
   CSV/SQLite/JSONL that holds them.
5. Record parse step(s) as `SolveitInvestigativeAction` with DFT-1066/1076
   and applied mitigations (at least dual-tool when both tools exist).
6. Validate with `validate_graph(..., extensions=['solveit'])`.

## Validated exemplar

```bash
PYTHONPATH=python:packages/case-uco-solveit/python:mcp_server \
  python3 examples/sysdiagnose/build_ios_sysdiagnose_unified_logs.py
```

MCP discovery helpers used while authoring:

- `guide_mapping("iOS sysdiagnose unified logarchive")`
- `search_classes("AppleUnifiedLogArchive", scope="solveit")`
- `plan_solveit_workflow("collect iOS sysdiagnose and parse Apple unified logs")`
- `get_class_details("EventRecordFacet")`

## Related

- [ios-sysdiagnose.md](ios-sysdiagnose.md) — raw archive container and Wi-Fi/Battery children
- [solve-it-investigation-planning.md](solve-it-investigation-planning.md) — method / weakness documentation
- [event.md](event.md) — Event + Dictionary pattern
- [usn-journal.md](usn-journal.md) — parallel EventRecord journal recipe
- [database-records.md](database-records.md) — Notari SQLite row containment
- [analysis.md](analysis.md) / [configured-tool.md](configured-tool.md) — analytic tooling
