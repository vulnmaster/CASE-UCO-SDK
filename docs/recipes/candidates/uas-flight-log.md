# Unmanned Aircraft (UAS) Flight Log Modeling

How to model an unmanned aircraft's flight log — ArduPilot DataFlash (`.BIN`),
MAVLink telemetry (`.tlog`), PX4 ULog, or a DJI flight record — as a CASE/UCO
graph: the aircraft and its regulated identity, the sortie it flew, the
trajectory with per-fix times and accuracies, every state transition the
autopilot recorded, and the control-link endpoints that commanded it. The
recipe exists because the decisive question in a drone case is almost never
*where did it fly* — the log answers that plainly — but *who told it to do
that, and can the log's answer be trusted*. Modeling that requires keeping
three things separate and queryable: what the aircraft did, what authority it
believed was behind each action, and whether it was configured to verify that
authority at all.

**When to use this recipe**

- You have an autopilot or ground-station flight log and need it in a CASE
  graph: `.BIN`, `.tlog`, `.ulg`, DJI `TXT`/`DAT`.
- You are investigating an airspace incursion, an unauthorised flight, a
  fly-away, a drone-delivered contraband drop, or a UAS-enabled surveillance
  or smuggling case, and need aircraft, operator, trajectory and command
  authority in one graph.
- You need to reconcile a broadcast ASTM F3411 Remote ID observation with an
  onboard log.
- Near misses, use those instead: for a phone's stored location history see
  [location.md](../location.md); for the generic log-ingestion shape see
  [starter-filesystem-report.md](../starter-filesystem-report.md) and
  [event.md](../event.md); for the case wrapper see
  [forensic-lifecycle.md](../forensic-lifecycle.md).

**Status: candidate.** This recipe is not registered in `RECIPE_INDEX` or
`INDEX.md` and is invisible to routing until a reviewer promotes it with
`make promote-recipe RECIPE=uas-flight-log REVIEWER="..."`. It depends on the
candidate `uas` extension, which routing likewise ignores; load it explicitly
with `validate_graph(extensions=["uas"])`.

## Classes and properties

| Term | Role |
|---|---|
| `uas:UnmannedAircraft` (⊑ `uco-observable:Device`) | The aircraft as a programmable networked node |
| `uas:UASFacet` | Remote ID (ASTM F3411), registration, operator id, airframe layout, autopilot board id |
| `uas:MavlinkEndpointFacet` | System/component id, dialect, authorised GCS id, whether sender authentication was enforced |
| `uas:FlightLog` (⊑ `uco-observable:EventLog`) | The log container, with `uas:logFormat` |
| `uas:Flight` (⊑ `uco-core:Event`) | One armed-to-disarmed sortie |
| `uas:FlightModeChange` (⊑ `uco-core:Event`) | A mode transition, with `uas:flightModeChangeReason` and `uas:commandedBy` |
| `uco-observable:EventRecord` + `EventRecordFacet` | One row of the log, verbatim |
| `uco-observable:GeoLocationTrack` / `GeoLocationEntry` + facets | The trajectory |
| `uco-location:Location`, `LatLongCoordinatesFacet`, `GPSCoordinatesFacet` | Each fix and its precision |
| `uco-observable:Message` + `MessageFacet` | A MAVLink message observed on the link |
| `uco-observable:Software` + `SoftwareFacet` | Autopilot firmware and its source revision |
| `proposed-obs:observationTime`, `proposed-loc:altitudeReference`, `horizontalAccuracy`, `verticalAccuracy`, `satelliteCount`, `fixQuality` | Pending UCO terms — see [change proposal](../../../change_proposals/geolocation-entry-observation-time.md) |
| `case-investigation:InvestigativeAction`, `ProvenanceRecord`, `Investigation` | Analysis provenance and the case wrapper |

## Modeling pattern

All snippets below are copied verbatim from
`examples/uas/ardupilot-uas-flight-log.jsonld`, which passes
`validate_extension.py` with **Conforms: True**, zero violations, zero
warnings and zero undeclared concepts.

### 1. Anchor log time to wall-clock time before anything else

Autopilot logs are stamped in time-since-boot, not UTC. Anchor them to the
GNSS time in the first 3D-fix record and *say in the graph that you did*, so a
reader can re-derive or challenge every timestamp:

```json
"uco-core:description": "DataFlash records are stamped in TimeUS, microseconds since autopilot boot. Wall-clock times in this graph are derived by anchoring TimeUS 43419292 to the GNSS time in the first 3D-fix GPS record (week 2425, 561067200 ms of week), converted by GPS week/ms-of-week to UTC, minus 18 leap seconds. Any error in the leap-second constant shifts every derived time equally."
```

### 2. The aircraft carries its control-link configuration, not just its identity

The `senderAuthenticationEnforced` value is what tells a later reader how much
an observed system id proves. Record it even — especially — when it is `false`:

```json
{
  "@type": "uas:MavlinkEndpointFacet",
  "uas:mavlinkSystemId": { "@type": "xsd:nonNegativeInteger", "@value": "1" },
  "uas:mavlinkComponentId": { "@type": "xsd:nonNegativeInteger", "@value": "1" },
  "uas:mavlinkComponentName": "MAV_COMP_ID_AUTOPILOT1",
  "uas:mavlinkDialect": "ardupilotmega v2.0",
  "uas:authorizedGroundControlStationId": { "@type": "xsd:nonNegativeInteger", "@value": "255" },
  "uas:senderAuthenticationEnforced": { "@type": "xsd:boolean", "@value": "false" }
}
```

### 3. Track entries are receiver fixes, each with its own time and quality

Build the track from raw GNSS records rather than the autopilot's fused
position estimate, so every entry can carry the satellite count and accuracy it
was actually derived from. Where the two series must both appear, keep them in
separate nodes and say which is which.

```json
{
  "@type": "uco-observable:GeoLocationEntryFacet",
  "uco-observable:location": { "@id": "urn:uuid:..." },
  "proposed-obs:observationTime": { "@type": "xsd:dateTime", "@value": "2026-07-04T11:51:30.180Z" }
}
```

```json
{
  "@type": "uco-location:LatLongCoordinatesFacet",
  "uco-location:latitude":  { "@type": "xsd:decimal", "@value": "51.7620366" },
  "uco-location:longitude": { "@type": "xsd:decimal", "@value": "-1.2565564" },
  "uco-location:altitude":  { "@type": "xsd:decimal", "@value": "20.09" },
  "proposed-loc:altitudeReference": "mean sea level",
  "proposed-loc:horizontalAccuracy": { "@type": "xsd:decimal", "@value": "0.3" },
  "proposed-loc:verticalAccuracy": { "@type": "xsd:decimal", "@value": "0.3" }
}
```

```json
{
  "@type": "uco-location:GPSCoordinatesFacet",
  "uco-location:hdop": { "@type": "xsd:decimal", "@value": "1.21" },
  "uco-location:vdop": { "@type": "xsd:decimal", "@value": "2.0" },
  "proposed-loc:satelliteCount": { "@type": "xsd:nonNegativeInteger", "@value": "10" },
  "proposed-loc:fixQuality": "simulated"
}
```

### 4. A mode change records its authority, and stops where the log stops

This is the crux of the recipe. The autopilot logs *that* a ground station
commanded the change; it does not log *which* station. Model the reason, model
the node you observed, and let the description carry the correlation — do not
promote it to an assertion by setting `uas:commandedBy`:

```json
{
  "@type": "uas:FlightModeChange",
  "uco-core:name": "Mode change to RTL at 2026-07-04T11:51:43.627Z",
  "uco-core:startTime": { "@type": "xsd:dateTime", "@value": "2026-07-04T11:51:43.627Z" },
  "uas:flightMode": "RTL",
  "uas:previousFlightMode": "GUIDED",
  "uas:flightModeChangeReason": "GCS_COMMAND",
  "uas:autopilotFamily": "ArduPilot",
  "uco-core:description": "MODE record: mode number 6 (RTL), reason code 2 (GCS_COMMAND). It arrived 2.452 s after the STATUSTEXT from system 141. ArduPilot's MODE record carries the reason but not the commanding system id, so the graph does not assert that node commanded the change; uas:commandedBy is left unset and the correlation is stated here. What the log does establish is that the change was commanded by a ground control station rather than by a stick input or a failsafe, and that the aircraft was not enforcing which station may command it."
}
```

### 5. An unattributed node is an observable, not an identity

```json
{
  "@type": "uco-observable:ObservableObject",
  "uco-core:name": "Unattributed MAVLink node, system 141 / component 190",
  "uco-core:hasFacet": [{
    "@type": "uas:MavlinkEndpointFacet",
    "uas:mavlinkSystemId": { "@type": "xsd:nonNegativeInteger", "@value": "141" },
    "uas:mavlinkComponentId": { "@type": "xsd:nonNegativeInteger", "@value": "190" },
    "uas:mavlinkComponentName": "MAV_COMP_ID_MISSIONPLANNER"
  }]
}
```

Do not create a `uco-identity:Person` or `Organization` for it. A MAVLink
system id is self-asserted; promoting it to an identity is the modelling
equivalent of naming a suspect from a spoofable header.

## Anti-patterns

1. **Asserting a commanding node the log did not name.** `GCS_COMMAND` plus a
   nearby STATUSTEXT is a correlation. Setting `uas:commandedBy` from it turns
   a defensible observation into an unfounded attribution.
2. **Treating a simulated log as evidence of position.** SITL and replay logs
   look identical to real ones apart from a few markers. Check for `RC
   Protocol: SITL` / `SIM` records and set `fixQuality` to `simulated`.
3. **Recording an altitude with no datum.** AMSL, ellipsoidal, above-ground and
   above-takeoff differ by tens of metres and the regulatory limit is expressed
   against a specific one.
4. **Putting the track's start time on every entry**, or leaving entries
   untimed and relying on document order. Use `proposed-obs:observationTime`
   until UCO adopts a core equivalent.
5. **Normalising vendor mode names at ingest.** `AUTO` does not mean the same
   thing on ArduPilot and PX4. Keep the vendor string and record
   `uas:autopilotFamily`.
6. **Typing the flight with `uco-observable:ObservableRelationship`.**
   `uas:Flight` is a `uco-core:Event`, not an Observable; edges to or from it
   must be plain `uco-core:Relationship` or they will fail in UCO 2.0.0.
7. **Inventing accuracy from DOP.** Dilution of precision is geometry, not
   metres. If the source gives no metric accuracy, omit it.
8. **Hand-typing values out of a log viewer.** Extract to a facts file with a
   parser and build the graph from that file, so the graph cannot drift from
   the evidence.

## Checklist

1. Hash the log before parsing; carry the digest on a
   `uco-observable:ContentDataFacet`.
2. Parse with a reference parser (`pymavlink` for ArduPilot/MAVLink) into a
   facts file — see `scripts/extract_uas_flight_facts.py`.
3. Resolve every numeric enumeration against the firmware source, not memory:
   `AP_Logger.h` (`LogEvent`), `ModeReason.h` (`ModeReason`), `mode.h`
   (`Mode::Number`). Record the resolved name *and* the raw code.
4. Anchor boot-relative time to GNSS time; state the method and the leap-second
   constant in the graph.
5. Model the aircraft, its firmware, and its `uas:MavlinkEndpointFacet`
   including the sender-authentication policy.
6. Model the sortie bounded by arm and disarm; attach takeoff location and
   track.
7. Build the track from receiver fixes with per-fix time, accuracy, satellite
   count and fix quality.
8. Model every log row as an `EventRecord` with verbatim text; promote only the
   forensically significant ones to typed events.
9. For each mode change, record mode, previous mode, reason and autopilot
   family; set `uas:commandedBy` only if the log names the commander.
10. Model any non-authorised endpoint observed on the link as an
    `ObservableObject` with a `uas:MavlinkEndpointFacet`.
11. Add the parse `InvestigativeAction`, the `ProvenanceRecord`, and the
    `Investigation` wrapper.
12. Validate: `python scripts/validate_extension.py extensions/uas/manifest.json
    <graph>.jsonld` must report `Conforms: True` with no warnings.

## Validated exemplar

- Builder: `examples/uas/build_ardupilot_flight_log.py`
- Graph: `examples/uas/ardupilot-uas-flight-log.jsonld` (103 nodes)
- Facts file: `examples/uas/uavrodeo_flight_facts.json`
- Extractor: `scripts/extract_uas_flight_facts.py`

Validated against the DFRWS USA 2026 Rodeo UAS challenge log `uavrodeo.BIN`
(ArduPilot DataFlash, ArduCopter V4.6.0-dev, SHA-256
`a2fa5f1f2b63836045f4b74e07d043780ded1126d04db8d5f286896da363693f`).
The capture is an ArduPilot SITL run; the modelling pattern is identical for a
physical flight, and the graph says so rather than implying otherwise.

```
$ python scripts/validate_extension.py extensions/uas/manifest.json \
    examples/uas/ardupilot-uas-flight-log.jsonld
Conforms: True
```

## Related

- [extensions.md](../extensions.md) — how candidate extensions and strict concept coverage work
- [change-proposal.md](../change-proposal.md) — the upstream loop this recipe feeds
- [location.md](../location.md) — device-stored location artifacts
- [event.md](../event.md) — the generic event/record split this recipe specialises
- [network-artifacts.md](../network-artifacts.md) — for the RF/link side of a UAS case
- [chain-of-custody.md](../chain-of-custody.md) — provenance for the seized aircraft and its media
- [forensic-lifecycle.md](../forensic-lifecycle.md) — the case wrapper
