# iOS / macOS Sysdiagnose Archives

> See [Recipe Index](INDEX.md) for all recipes.

Model an Apple **sysdiagnose** package — the on-device diagnostic archive that
bundles `system_logs.logarchive` (Unified Logging), Wi-Fi state, BatteryBDC
CSVs, crash reports, preferences dumps, and hundreds of `summaries/*.log`
files. Pair this recipe with
[apple-unified-logs.md](apple-unified-logs.md) when you parse the logarchive
into per-event CASE nodes, and with
[starter-mobile-extraction.md](starter-mobile-extraction.md) /
[mobile-device.md](mobile-device.md) for the handset itself.

Validated against `examples/sysdiagnose/ios-sysdiagnose-unified-logs.jsonld`
(`validate_graph(..., extensions=['solveit'])` → Conforms: True). Grounded in
the DFRWS USA Sysdiagnosis workshop corpus layout
(`sysdiagnose_*_iPhone-OS_*_21D50` with `system_logs.logarchive`).

**When to use this recipe**

- The submission is a sysdiagnose tarball/folder (name pattern
  `sysdiagnose_YYYY.MM.DD_*_iPhone-OS_*` or macOS equivalent)
- You see `system_logs.logarchive`, `summaries/`, `WiFi/`, `logs/`,
  `crashes_and_spins/`, `Preferences/`
- Acquisition was via device Settings → Analytics, UFADE, pymobiledevice3,
  libimobiledevice, or a companion Mac `sysdiagnose` trigger
- For **parsed** unified-log rows / iterator CSV / Notari SQLite / iLEAPP
  HTML, continue with [apple-unified-logs.md](apple-unified-logs.md)

## Fail-closed package-shape check

A `.logarchive` is not, by itself, a sysdiagnose. Before applying this recipe,
run the local classifier against the directory or a structured inventory JSON:

```text
classify_apple_package_shape(package_root="/local/evidence/apple-collect", profile="auto")
```

`auto` classifies `ios-sysdiagnose` only when there is exactly one
`system_logs.logarchive` plus strong sysdiagnose evidence: a `sysdiagnose_*`
root with multiple expected directories, or at least four expected top-level
markers (`WiFi/`, `summaries/`, `logs/`, `crashes_and_spins/`, `Preferences/`).
It fails with typed errors for lone/multiple logarchives and weak or conflicting
trees rather than guessing.

A FOSS collection containing a standalone `.logarchive`, crash pull, live
syslog, and apps list is **not** a full sysdiagnose. Route it to
[apple-unified-logs.md](apple-unified-logs.md) plus
[starter-mobile-extraction.md](starter-mobile-extraction.md), and preserve its
actual package label. An explicit profile is an operator assertion and is still
rejected when required shape evidence is absent.

## Bounded/shareable graph automation

For a verified sysdiagnose, the MCP helper builds a package-level graph without
reading full archive content:

```text
build_acquisition_package_graph(
  package_root="/local/evidence/sysdiagnose_...",
  output_path="/local/work/sysdiagnose-package.jsonld",
  profile="auto",
  max_event_records=0,
  shareable=true,
  extensions=["solveit"],
)
validate_graph(
  graph_path="/local/work/sysdiagnose-package.jsonld",
  extensions=["solveit"],
  strict_concepts=true,
)
```

The builder inventory walk, depth, file count, hashing, and optional event
sample are bounded. It models `.tracev3`/logarchive bytes as metadata-only,
samples at most three crash `.ips` files by metadata/digest, and represents an
apps inventory as a count rather than one node per identifier. Its MCP response
contains only counts, sizes, bounded named-file digests, warnings, and validation
guidance—never host paths, device identifiers, source rows, or message bodies.

With `shareable=true` (default), `filePath` values are package-relative; common
UDID/IMEI/serial/phone literals are redacted; and log messages are omitted or
replaced by a fixed placeholder. Use local-only mode only inside an approved
Tier T2 workspace, and perform a separate operator review before distributing
any graph or excerpt.

## Classes and properties

| Class | Role |
|---|---|
| `uco-observable:ObservableObject` + `DeviceFacet` (+ `MobileDeviceFacet` when IMEI/ESN/network evidence exists) | The iPhone/iPad/Mac that produced the archive |
| `uco-observable:OperatingSystem` + `SoftwareFacet` (+ dual-type `Software`) | OS from `logs/SystemVersion/SystemVersion.plist` |
| `uco-observable:ObservableObject` + `FileFacet` (`isDirectory=true`) | Sysdiagnose root directory |
| `solveit-observable:AppleUnifiedLogArchive` (+ dual-type `EventLog`) | `system_logs.logarchive` container |
| `uco-observable:WirelessNetworkConnection` + `WirelessNetworkConnectionFacet` | Known Wi-Fi SSIDs/BSSIDs from `WiFi/*.plist` |
| `uco-observable:ObservableObject` + `FileFacet` | Ancillary files (BatteryBDC CSV, plists, summary logs) |
| `uco-observable:EventRecord` + `EventRecordFacet` | Optional typed rows from structured CSVs *inside* the archive |
| `case-investigation:InvestigativeAction` + `uco-tool:Tool` | Collection step (UFADE / pymobiledevice3 / …) |
| `case-investigation:ProvenanceRecord` | Exhibit grouping for the package |

Requires `CASE_UCO_EXTENSIONS=solveit` (or `extensions=['solveit']` at
validation) for `AppleUnifiedLogArchive`.

## Modeling pattern

```
Investigation
  └── object ──▶ InvestigativeAction ("Collect iOS sysdiagnose")
                     ├── instrument ──▶ Tool (UFADE / pymobiledevice3)
                     ├── object ──▶ phone (DeviceFacet model=iPhone12,1)
                     └── result ──▶ sysdiagnose_dir
                                ──▶ system_logs.logarchive

phone ── Characterized_By ──▶ OperatingSystem (SoftwareFacet version=17.3)
sysdiagnose_dir
  ├── Contained_Within ◀── system_logs.logarchive
  │                         (@type AppleUnifiedLogArchive + EventLog)
  ├── Contained_Within ◀── WiFi/com.apple.wifi-private-mac-networks.plist
  │                         ▲── Characterized_By ── WirelessNetworkConnection (ssid/BSSID)
  └── Contained_Within ◀── logs/BatteryBDC/*.csv
```

Do **not** put Wi-Fi passwords from `security.txt` (or similar) into the graph.
When workshop bytes are not hashed in-repo, tag containers with
`hash-status:not-published` / `source-bytes:not-acquired` rather than inventing digests.

### Device and OS (from SystemVersion.plist)

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity
from case_uco.uco.observable import (
    ObservableObject, DeviceFacet,
    OperatingSystem, SoftwareFacet, ObservableRelationship,
)

graph = CASEGraph()
apple = graph.create(Identity, name="Apple Inc.")
# Hardware model (e.g. "iPhone12,1") is in crashes_and_spins/*.ips headers
# ("product") and summaries. Add MobileDeviceFacet only when you have
# mobile-specific evidence to assert (IMEI, ESN, network) — not empty.
phone = graph.create(ObservableObject,
    name="iPhone (sysdiagnose 2024-08-02)",
    has_facet=[
        DeviceFacet(manufacturer=apple, model="iPhone12,1", device_type="Mobile Phone"),
    ],
)
ios = graph.create(OperatingSystem,
    name="iPhone OS 17.3 (21D50)",
    has_facet=[SoftwareFacet(manufacturer=apple, version="17.3")],
    description=["Source: logs/SystemVersion/SystemVersion.plist"],
)
# Dual-type Software for UCO 2.0 readiness (see SHACL warning on OperatingSystem).
# Use ObservableObjectRelationshipVocab only (Runs_On is not in the registry).
graph.create(ObservableRelationship, is_directional=True,
    kind_of_relationship="Characterized_By", source=[phone], target=ios)
```

### Sysdiagnose root + Unified Log archive

```python
from case_uco.uco.observable import FileFacet, EventLog
from case_uco_solveit.solveit_observable import AppleUnifiedLogArchive

sysdiag = graph.create(ObservableObject,
    name="sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50",
    has_facet=[FileFacet(
        file_name=["sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50"],
        file_path=["Data/sysdiagnose_2024.08.02_16-19-26-0400_iPhone-OS_iPhone_21D50"],
        is_directory=[True],
    )],
)
logarchive = graph.create(AppleUnifiedLogArchive,
    name="system_logs.logarchive",
    has_facet=[FileFacet(
        file_name=["system_logs.logarchive"],
        file_path=[".../system_logs.logarchive"],
        is_directory=[True],
        size_in_bytes=22193292,
    )],
    description=["Persist/, Signpost/, Special/, Extra/, *.tracev3"],
)
# Also type as EventLog — the archive is a collection of event records.
```

Validated JSON-LD fragment (archive node):

```json
{
  "@id": "kb:AppleUnifiedLogArchive-…",
  "@type": [
    "solveit-observable:AppleUnifiedLogArchive",
    "uco-observable:EventLog"
  ],
  "uco-core:name": "system_logs.logarchive",
  "uco-core:hasFacet": [{
    "@type": "uco-observable:FileFacet",
    "uco-observable:fileName": ["system_logs.logarchive"],
    "uco-observable:isDirectory": [{"@type": "xsd:boolean", "@value": "true"}],
    "uco-observable:sizeInBytes": {"@type": "xsd:integer", "@value": "22193292"}
  }]
}
```

### Wi-Fi networks from sysdiagnose (not passwords)

```python
from case_uco.uco.observable import (
    WirelessNetworkConnection, WirelessNetworkConnectionFacet, MACAddressFacet,
)

wifi_plist = graph.create(ObservableObject, name="com.apple.wifi-private-mac-networks.plist",
    has_facet=[FileFacet(
        file_name=["com.apple.wifi-private-mac-networks.plist"],
        file_path=[".../WiFi/com.apple.wifi-private-mac-networks.plist"],
    )])
bssid = graph.create(ObservableObject, name="BSSID 6a:22:32:98:f4:df",
    has_facet=[MACAddressFacet(address_value="6a:22:32:98:f4:df")])
wifi = graph.create(WirelessNetworkConnection,
    name="Wi-Fi network Matt_Foley",
    has_facet=[WirelessNetworkConnectionFacet(
        ssid="Matt_Foley", base_station="6a:22:32:98:f4:df")],
)
```

Do **not** copy AirPort keychain password material from `WiFi/security.txt`
into the graph — model SSID/BSSID/join times only.

### Crash reports and stackshots (`crashes_and_spins/*.ips`)

Apple `.ips` reports are JSON: a one-line header (`bug_type`, `timestamp`,
`os_version`, `incident_id`) plus a payload. In the workshop corpus,
`stacks-2024-08-02-161926.ips` (`bug_type` 288) is the stackshot taken *by*
the sysdiagnose trigger itself — `"reason": "stackshot via sysdiagnose (XPC)"`
with `crashReporterKey`, `product` (`iPhone12,1`), `kernel` build, and a
boot-relative `absoluteTime` in mach ticks.

Model each retained report as a file plus an `EventRecord`:

```python
crash_ips = graph.create(ObservableObject,
    name="stacks-2024-08-02-161926.ips",
    has_facet=[FileFacet(
        file_name=["stacks-2024-08-02-161926.ips"],
        file_path=[".../crashes_and_spins/stacks-2024-08-02-161926.ips"],
    )],
)
crash_record = graph.create(EventRecord,
    name="Stackshot via sysdiagnose (bug_type 288)",
    has_facet=[EventRecordFacet(
        event_record_id="F7A78B41-4507-43CA-9E76-62CD057EFD77",  # incident_id
        event_type="stackshot",
        event_record_service_name="crash_reporter",
        event_record_device=phone,
        observable_created_time=datetime(2024, 8, 2, 16, 19, 26, tzinfo=tz),
    )],
)
# Contained_Within → sysdiagnose dir; keep bug_type / crashReporterKey /
# absoluteTime (mach ticks) as DictionaryEntry values on a companion Event.
```

The header `timestamp` on `.ips` files **is** wall-clock (unlike unresolved
unified-log rows), so `observableCreatedTime` is safe here when the retained
report header is actually parsed and its timezone is present. The bounded
package helper does not parse crash bodies; its sampled crash nodes therefore
remain metadata-only.

For unified-log CSV/JSONL excerpts, finding a timesync file is not enough to
assert device-absolute UTC. Only emit absolute event times when decoder/inventory
metadata explicitly establishes timesync anchoring; otherwise preserve
`mach_continuous_time`, `boot_uuid`, and tool-reported timestamps as attributes
and apply DFM-1179 guidance.

## Anti-patterns

- **Flattening the archive into one blob.** Keep the sysdiagnose directory,
  the logarchive, and high-value children (WiFi plists, BatteryBDC CSVs) as
  separate observables linked with `Contained_Within` / `Extracted_From`.
- **Typing the phone as the InvestigativeAction.** The device is an
  observable; collection is the action (`instrument` = UFADE/pymobiledevice3).
- **Inventing Unified Log Facet classes.** Core UCO already has `EventLog` /
  `EventRecord` / `EventRecordFacet`; SOLVE-IT adds `AppleUnifiedLogArchive`.
  Do not invent `SysdiagnoseFacet`.
- **Modeling every `summaries/*.log` as an Event.** Treat the summary dump as
  files unless a row is analytically relevant — then use `EventRecord`.
- **Skipping solveit validation.** If you type `AppleUnifiedLogArchive`,
  validate with MCP `validate_graph(..., extensions=['solveit'], strict_concepts=True)`;
  plain `case_validate` does not provide an `--extension solveit` shortcut.
- **Sharing absolute local paths, device identifiers, or syslog bodies.** Build
  in shareable mode and review redaction metadata before moving a Tier T2 graph
  into a review/exemplar channel.

## Checklist

1. Create the device + OS from `SystemVersion.plist` (ProductVersion / Build).
2. Create the sysdiagnose directory observable; link `Extracted_From` → device.
3. Create `system_logs.logarchive` as `AppleUnifiedLogArchive` (+ `EventLog`).
4. Attach high-value children (WiFi networks, BatteryBDC CSV,
   `crashes_and_spins/*.ips` reports) with containment relationships.
5. Record collection as `InvestigativeAction` with `instrument` / `object` /
   `result` and a `ProvenanceRecord`.
6. Hand off parsing to [apple-unified-logs.md](apple-unified-logs.md).
7. For review/sharing, run the share-safety mode and verify relative paths,
   identifier redaction, and message omission.
8. Validate: `validate_graph(path, extensions=['solveit'], strict_concepts=True)`.

## Validated exemplar

```bash
PYTHONPATH=python:packages/case-uco-solveit/python:mcp_server \
  python3 examples/sysdiagnose/build_ios_sysdiagnose_unified_logs.py
# → examples/sysdiagnose/ios-sysdiagnose-unified-logs.jsonld
case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/solveit/solve_it_core.ttl \
  # (or: validate_graph(..., extensions=['solveit']))
```

## Related

- [apple-unified-logs.md](apple-unified-logs.md) — parse logarchive → EventRecords + tool CSV/SQLite
- [starter-mobile-extraction.md](starter-mobile-extraction.md) — handset / apps / messages
- [forensic-tool.md](forensic-tool.md) / [starter-tool-run.md](starter-tool-run.md) — tool provenance
- [solve-it-investigation-planning.md](solve-it-investigation-planning.md) — DFT-1016 / DFT-1066 method documentation
- [event.md](event.md) — Event + Dictionary pattern reused for log rows
- [usn-journal.md](usn-journal.md) — analogous OS change-journal EventRecord pattern (Windows)
