# Unmanned Aircraft System (UAS) Extension

**Status: candidate.** Invisible to routing until a reviewer promotes it with
`make promote-extension EXT=uas REVIEWER="..."`. Load it explicitly for
validation: `validate_graph(extensions=["uas"])`.

Vendor-neutral drone-forensics concepts: the aircraft as an identifiable
networked device, the autopilot flight log, the sortie, autopilot mode
transitions with their commanding authority, and MAVLink control-link
endpoints.

## Why this exists

Core CASE/UCO already models the *evidence carriers* of a drone case well —
`uco-observable:EventLog` and `EventRecord` for the log, `GeoLocationTrack` for
the trajectory, `uco-location` facets for the fixes, `uco-core:Event` for the
timeline. What it has no term for is the part that decides the case:

- the **regulated identity** of the aircraft (ASTM F3411 Remote ID serial,
  civil-aviation registration, operator id), and
- the **control-plane semantics** that determine attribution — which MAVLink
  node commanded a mode change, and whether the autopilot was configured to
  authenticate that node at all.

Without terms for those, both end up as prose in `uco-core:description`, where
they cannot be queried, compared across cases, or validated.

## Files

| File | Role |
|---|---|
| `uas.ttl` | T-Box: 4 classes, 2 facets, 3 object properties, 16 datatype properties |
| `uas-shapes.ttl` | SHACL — permissive (recovered logs are usually partial); constrains datatypes, node kinds, cardinality, and the 0–255 ranges the MAVLink wire format bounds |
| `uas-profile-gufo.ttl` | gUFO bridge: aircraft as `gufo:FunctionalComplex`, flight and mode change as `gufo:Event` |
| `location-pending.ttl` | Local declarations of six geolocation properties **proposed to UCO** — not UAS concepts, see below |
| `uas-exemplar.ttl` | A-Box exercising every `uas:` property once |

## The pending geolocation terms

`location-pending.ttl` declares `proposed-obs:observationTime`,
`proposed-loc:altitudeReference`, `horizontalAccuracy`, `verticalAccuracy`,
`satelliteCount` and `fixQuality`. These are **not** drone concepts — they are
gaps in core UCO that every trajectory-bearing domain hits (vehicle telematics,
phone location history, AIS/ADS-B, fitness trackers, GPX). Most consequentially,
`uco-observable:GeoLocationEntryFacet` has no time property, so a UCO track can
list positions but cannot say when the subject was at any of them.

They are carried here, under a `proposed.ontology.unifiedcyberontology.org`
namespace, so that adoption upstream is a prefix rewrite. Source of truth:
[`change_proposals/geolocation-entry-observation-time.md`](../../change_proposals/geolocation-entry-observation-time.md).

## Design decisions

- **`uas:UnmannedAircraft ⊑ uco-observable:Device`** — a drone is in the cyber
  domain: it runs firmware, holds a parameter store, writes logs, and is a node
  on a command-and-control network. The class covers the airframe plus its
  avionics, not the wider system-of-systems; the ground station is a separate
  device and the link is modelled through `uas:MavlinkEndpointFacet` on each
  participant.
- **Identity is delegated, not re-invented** — ASTM F3411 defines the UAS ID
  types and ANSI/CTA-2063-A the serial format that 14 CFR Part 89 and EU
  2019/945 build on. The extension carries the values and names the standard.
- **`uas:Flight` and `uas:FlightModeChange ⊑ uco-core:Event`** — they inherit
  `startTime`/`endTime`/`eventContext` and compose with existing timeline
  recipes rather than forking a parallel event model. Note the consequence:
  edges to them must be `uco-core:Relationship`, not
  `uco-observable:ObservableRelationship`.
- **Mode names and reasons stay as open vocabularies** — ArduPilot, PX4, DJI and
  Autel name modes differently and `AUTO` does not mean the same thing on each.
  Record the vendor string plus `uas:autopilotFamily`; normalise in analysis,
  not at ingest.
- **`uas:senderAuthenticationEnforced` is deliberately prominent.** MAVLink v1
  and v2 carry no authentication by default. Whether the autopilot checked the
  source of its commands is what determines how much an observed system id
  proves, and it belongs in the graph next to the id itself.

## Validation

```
$ python scripts/validate_extension.py extensions/uas/manifest.json \
    examples/uas/ardupilot-uas-flight-log.jsonld
Conforms: True
```

Zero violations, zero warnings, zero undeclared concepts.

## Recipe and exemplar

- Recipe: [`docs/recipes/candidates/uas-flight-log.md`](../../docs/recipes/candidates/uas-flight-log.md)
- Worked example: `examples/uas/` (builder, facts file, 103-node graph)
- Extractor: `scripts/extract_uas_flight_facts.py`

Validated against the DFRWS USA 2026 Rodeo UAS challenge log `uavrodeo.BIN`
(SHA-256 `a2fa5f1f2b63836045f4b74e07d043780ded1126d04db8d5f286896da363693f`).
