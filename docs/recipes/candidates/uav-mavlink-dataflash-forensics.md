# UAV / MAVLink DataFlash Forensics (candidate)

> **Status:** candidate — not yet in `RECIPE_INDEX` / routing.  
> **Team:** GreenLizards (DFRWS USA 2026 Rodeo)  
> **Validated against:** CASE/UCO 1.4.0 core types only (exemplar builder under `examples/uav/`).

Model unmanned aerial vehicle (UAV) flight-log evidence — especially ArduPilot
**DataFlash** `.BIN` files and MAVLink status / command / GPS streams — with
existing CASE/UCO classes, and call out the semantic gaps that force free-text
encoding today.

## When to use this recipe

- Evidence is a UAV **flight log** (ArduPilot DataFlash / PX4 ULog / MAVLink
  tlog) recovered from a drone, GCS, companion computer, or seized media
- You need to assert: platform identity, home/origin, GPS track, flight mode
  changes, status text / planted or adversary messages, GCS system id
- Neighboring recipes: [device.md](../device.md), [location.md](../location.md),
  [geosparql-geospatial-evidence.md](../geosparql-geospatial-evidence.md),
  [event.md](../event.md), [forensic-tool.md](../forensic-tool.md)

## Classes and properties

| Class / facet | Role in UAV modeling |
|---|---|
| `uco-observable:Drone` + `DeviceFacet` | Airframe / UAV platform (`deviceType`, `model`) |
| `uco-observable:FileFacet` + `ContentDataFacet` | DataFlash binary (name, size, magic `YFMT`) |
| `uco-observable:ApplicationFacet` | Autopilot software (e.g. ArduCopter version) |
| `uco-location:Location` + `LatLongCoordinatesFacet` | ORGN home, GPS samples |
| `uco-observable:GeoLocationEntry` / `GeoLocationTrack` | Ordered flight path |
| `uco-observable:EventRecord` + `EventRecordFacet` | MSG / MODE / MAVC rows **without** a MAVLink facet |
| `case-investigation:InvestigativeAction` + `uco-tool:Tool` | Parse action + pymavlink (or equivalent) |
| `uco-core:Relationship` | Link log ↔ drone, track ↔ drone |

## Modeling pattern

```
Investigation
    └── InvestigativeAction ──instrument──▶ Tool (pymavlink)
              └── object ──▶ File (DataFlash .BIN)
                                   │
Drone + DeviceFacet ◀── Contained_Within ──┘
    ▲
    └── Path_Of ── GeoLocationTrack ──▶ GeoLocationEntry ──▶ Location + LatLong

EventRecord + EventRecordFacet
    eventRecordText  = "SRC=141/190:DFRWS26"   # free-text until MAVLink facet exists
    eventType        = "MAVLink.STATUS_TEXT"
    eventRecordID    = "TimeUS=95394327"
```

### Python (excerpt)

```python
from case_uco import CASEGraph
from case_uco.uco.observable import (
    Drone, DeviceFacet, EventRecord, EventRecordFacet,
    GeoLocationTrack, GeoLocationTrackFacet,
    FileFacet, ContentDataFacet, ObservableObject, ApplicationFacet,
)
from case_uco.uco.location import Location, LatLongCoordinatesFacet

graph = CASEGraph(kb_prefix="http://example.org/kb/uav/")

drone = graph.create(
    Drone,
    has_facet=[DeviceFacet(device_type="UAV", model="QUAD/PLUS")],
)
home = graph.create(
    Location,
    has_facet=[LatLongCoordinatesFacet(latitude=51.7607129, longitude=-1.2563709)],
)
# Status text / system id still forced into free text (ontology gap):
graph.create(
    EventRecord,
    has_facet=[EventRecordFacet(
        event_record_text="SRC=141/190:DFRWS26",
        event_type="MAVLink.STATUS_TEXT",
        event_record_id="TimeUS=95394327",
    )],
)
```

Full builder: [`examples/uav/build_uav_dataflash_exemplar.py`](../../../examples/uav/build_uav_dataflash_exemplar.py)  
Exemplar graph: [`examples/uav/uav-dataflash-greenlizards.jsonld`](../../../examples/uav/uav-dataflash-greenlizards.jsonld)

## Anti-patterns

- **Do not invent MAVLink IRIs** (`mavlink:SystemId`, etc.) in production graphs —
  strict concept coverage fails. Record gaps and file a UCO change proposal.
- **Do not fabricate wall-clock times** from `TimeUS` alone without GPS/timebase
  evidence; prefer GPS-derived UTC when available and keep raw `TimeUS` in
  `eventRecordID` or description.
- **Do not model the GCS as the drone.** System id 141 / component 190 may be a
  ground station; treat sender identity as a separate `Identity` /
  `ObservableObject` once typed properties exist.
- **Do not dump the entire log as one `ContentDataFacet.dataPayload`.** Use
  focused `EventRecord` / track nodes for investigative facts.

## Checklist

1. Identify log format (DataFlash `YFMT`, ULog, tlog) → `FileFacet` + magic/mime.
2. Create `Drone` + `DeviceFacet` from frame/model/serial when present.
3. Parse ORGN / home and GPS samples → `Location` + track entries.
4. Capture flight modes and status text as `EventRecord`s; document untyped
   MAVLink fields in descriptions.
5. Record the parse tool as `Tool` on an `InvestigativeAction`.
6. List semantic gaps and link any filed UCO/CASE change proposal.
7. Validate with `case_validate` / `validate_graph` before sharing.

## Semantic gaps (feeds Flag 2 / change proposal)

Confirmed via registry search (`search("MAVLink")` → empty; `Drone` has no
telemetry properties):

| Needed fact | Available today | Gap |
|---|---|---|
| MAVLink system id / component id | free text in `eventRecordText` | no property |
| Flight mode enum + reason | free text | no facet on `Drone` |
| Boot-relative `TimeUS` (µs) | stuffed into `eventRecordID` | no boot-relative microsecond property |
| Autopilot protocol dialect (MAVLink1/2, DataFlash) | description only | no vocabulary |
| GCS vs airframe roles | ambiguous | no typed link |

See `change_proposals/mavlink-uav-flight-log-facets.md` for the UCO proposal
drafted from this modeling pass.

## Provenance

- **Source investigation:** DFRWS USA 2026 Forensic Rodeo, BuiltToFall UAV
  evidence (`uavrodeo.BIN`), team **GreenLizards**
- **Authoring:** CASE-UCO SDK modeling contribution for the Rodeo community
  challenge (Flag 1)
- **Next:** promote from `candidates/` after SHACL validation + human review
