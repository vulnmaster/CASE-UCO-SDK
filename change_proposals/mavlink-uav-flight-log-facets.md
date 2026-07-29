<!-- Change Proposal: MAVLink / UAV flight-log facets -->
<!-- Target repository: UCO -->
<!-- Target release: 1.5.0 -->
<!-- DFRWS USA 2026 Rodeo Team: GreenLizards -->
<!-- Grounded in CASE-UCO-SDK modeling exemplar examples/uav/ -->

# Target release

**Target**: CASE/UCO 1.5.0

# Background

UCO already defines `uco-observable:Drone` (subclass of `MobileDevice`) and
geolocation track types (`GeoLocationTrack`, `GeoLocationEntry`) that cover
*some* UAV investigation needs. What is missing is any first-class way to
represent **MAVLink / autopilot flight-log structure** that digital forensics
tools actually emit when parsing ArduPilot DataFlash, PX4 ULog, or MAVLink
telemetry logs:

- MAVLink **system id** and **component id** (who sent a message — airframe vs
  GCS vs companion computer)
- Autopilot **flight mode** and mode-change reason
- Log-native **time bases** such as ArduPilot `TimeUS` (microseconds since boot)
  that are not wall-clock timestamps
- Message **type / dialect** (STATUS_TEXT, COMMAND_LONG, GPS, MODE, …)

Without these, examiners are forced to bury investigative facts in free-text
`EventRecordFacet.eventRecordText` / `eventRecordID`, which cannot be queried,
validated, or compared across tools. SOLVE-IT already enumerates drone-app
artifact extraction (`DFT-1179`); the cyber-observable layer should be able to
hold the parsed results.

This proposal was drafted after modeling DFRWS USA 2026 Rodeo UAV evidence
(`uavrodeo.BIN`) with the CASE/UCO SDK. **DFRWS Rodeo Team: GreenLizards.**

Related modeling contribution (SDK recipe + exemplar):
https://github.com/vulnmaster/CASE-UCO-SDK (PR from GreenLizards — UAV DataFlash recipe).

No open UCO issue currently proposes MAVLink system/component ids or flight-mode
facets (tracker search: drone / mavlink / UAV telemetry — only unrelated hits).

# Requirements

## Requirement 1

Define a new facet `MavlinkEndpointFacet` as a subclass of
`uco-core:Facet`, applicable to an `ObservableObject` that participates in a
MAVLink network (drone, GCS, companion computer, radio).

Properties:

- `mavlinkSystemId` (xsd:integer): MAVLink system id (0–255) of this endpoint.
- `mavlinkComponentId` (xsd:integer): MAVLink component id (0–255) of this endpoint.
- `mavlinkDialect` (xsd:string): Optional dialect/version label (e.g.,
  `MAVLink2`, `ardupilotmega`, `common`).

## Requirement 2

Define a new facet `UavFlightLogFacet` as a subclass of `uco-core:Facet` for a
flight-log **file** or container observable (DataFlash `.BIN`, ULog, `.tlog`).

Properties:

- `flightLogFormat` (xsd:string): Container format (e.g., `ArduPilot-DataFlash`,
  `PX4-ULog`, `MAVLink-tlog`).
- `autopilotFirmware` (xsd:string): Firmware identity string when present
  (e.g., `ArduCopter V4.6.0-dev`).
- `airframeType` (xsd:string): Frame description from the log when present
  (e.g., `QUAD/PLUS`).
- `logStartTime` / `logEndTime` (xsd:dateTime): Wall-clock span when resolvable
  from GPS or other timebase evidence.
- `timebase` (xsd:string): Primary log-native timebase (e.g., `TimeUS`,
  `boot-ms`).

## Requirement 3

Define a new facet `MavlinkMessageFacet` as a subclass of `uco-core:Facet` for a
single parsed MAVLink / DataFlash message row (often co-typed on
`EventRecord` / used via `EventRecordFacet`).

Properties:

- `mavlinkMessageType` (xsd:string): Message name/type (e.g., `STATUSTEXT`,
  `COMMAND_LONG`, `GPS`, `MODE`).
- `sourceSystemId` / `sourceComponentId` (xsd:integer): Sender ids for this
  message (may differ from the airframe’s own ids when the sender is a GCS).
- `targetSystemId` / `targetComponentId` (xsd:integer): Optional command target.
- `timeUs` (xsd:integer): Log-native microsecond counter when the source uses
  ArduPilot-style `TimeUS` (preserve raw value; do not force conversion).
- `flightMode` (xsd:string): Flight mode name or enum label when the message
  asserts mode (e.g., `GUIDED`, `RTL`).
- `flightModeReason` (xsd:string): Optional mode-change reason code/label.
- `statusText` (xsd:string): Payload of STATUS_TEXT / MSG status strings when
  present.

## Requirement 4

Add optional property `hasMavlinkEndpoint` (range: `ObservableObject` bearing
`MavlinkEndpointFacet`) on `UavFlightLogFacet` and/or document a
`Relationship` kind pattern `Communicates_With` between drone and GCS
endpoints so multi-endpoint flights are first-class.

# Risk / Benefit analysis

## Benefits

- Lets DFIR tools emit **queryable** MAVLink attribution (who sent the planted
  status text? which system id owned the GUIDED commands?) instead of opaque
  free text.
- Aligns UCO with modern UAV investigations and SOLVE-IT drone techniques
  without inventing per-tool private JSON.
- Backward-compatible: additive facets only; existing `Drone` instances remain
  valid.
- Preserves raw `TimeUS` (ASTM E3016 incorrect-data risk if tools invent
  wall-clock times from boot counters alone).

## Risks

- MAVLink dialects evolve; `mavlinkMessageType` should remain an open string
  (or open vocabulary), not a closed enum, to avoid constant ontology churn.
- Overlap with generic `EventRecordFacet`: guidance should prefer
  `MavlinkMessageFacet` for MAVLink-specific fields and keep
  `eventRecordText` for residual human-readable payload only.
- `flightMode` vocabularies differ across ArduPilot / PX4 / vendor stacks —
  open string with documented examples is safer than a closed vocabulary in
  1.5.0.

# Competencies demonstrated

## Competency 1

An examiner receives ArduPilot DataFlash evidence `uavrodeo.BIN` (DFRWS USA
2026 Rodeo). Parsing yields:

- MSG at `TimeUS=95394327` with text `SRC=141/190:DFRWS26`
- All MAVC command rows with source system/component **141/190**
- MODE transitions (`GUIDED` → `RTL`)
- ORGN/GPS home at approximately `51.7607129, -1.2563709`

The examiner must attribute the status text and guided commands to a **GCS
endpoint** (system 141 / component 190), not invent a wall-clock time from
`TimeUS` alone, and still link the GPS track to the `Drone` airframe.

### Competency Question 1.1

Which MAVLink system/component ids sent the status text `SRC=141/190:DFRWS26`?

#### Result 1.1

The `MavlinkMessageFacet` on that message reports `sourceSystemId=141` and
`sourceComponentId=190`, independent of free-text parsing.

### Competency Question 1.2

What flight modes occurred during the log, ordered by log-native time?

#### Result 1.2

`MODE` messages with `flightMode` / `timeUs` yield `GUIDED` then `RTL` ordered
by `timeUs`.

### Competency Question 1.3

Which endpoints (airframe vs GCS) participated in the flight log?

#### Result 1.3

Distinct `ObservableObject`s with `MavlinkEndpointFacet` for the airframe and
for system 141 / component 190 (GCS), related to the log and drone.

### Draft SPARQL

```sparql
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/>

SELECT ?sys ?comp ?text ?timeUs
WHERE {
  ?msg a uco-observable:EventRecord ;
       uco-core:hasFacet ?facet .
  ?facet a proposed:MavlinkMessageFacet ;
         proposed:sourceSystemId ?sys ;
         proposed:sourceComponentId ?comp ;
         proposed:statusText ?text .
  OPTIONAL { ?facet proposed:timeUs ?timeUs . }
  FILTER(CONTAINS(?text, "DFRWS26"))
}
```

# Solution sketch / draft implementation

Local SDK modeling (using only current core types + free text for gaps):

- Recipe candidate:
  `docs/recipes/candidates/uav-mavlink-dataflash-forensics.md`
- Exemplar builder:
  `examples/uav/build_uav_dataflash_exemplar.py`
- Graph:
  `examples/uav/uav-dataflash-greenlizards.jsonld`

# Support for this proposal

- DFRWS USA 2026 Forensic Rodeo community challenge (CASE/UCO SDK track)
- **Team GreenLizards**
- Real DataFlash parse facts (system/component 141/190, GUIDED/RTL, ORGN/GPS)

# Coordination notes

- Prefer open vocabularies for message type and flight mode.
- Coordinate with any future `BootSession` / boot-relative time work for a
  shared pattern on log-native counters vs wall-clock time
  (see SDK local draft `boot-session-and-boot-relative-time.md` if filed).
- CASE-specific investigation workflow terms are **not** required here; this is
  a UCO observable gap.
