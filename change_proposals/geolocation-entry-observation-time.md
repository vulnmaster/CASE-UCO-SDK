# Geolocation entries need a fix time, an altitude datum, and reportable accuracy

Submitted by **DFRWS USA 2026 Rodeo Team "huh"**, from modeling work done with the
[CASE/UCO SDK](https://github.com/vulnmaster/CASE-UCO-SDK) on an unmanned-aircraft
flight log.

# Target release

UCO 1.5.0 (additive; no existing term changes meaning, no existing graph becomes
invalid).

# Background

While modeling an ArduPilot flight log into CASE/UCO we hit three gaps in the
geolocation vocabulary. None is specific to drones — they affect every source
that produces a *trajectory* rather than a single point: vehicle telematics,
mobile-device location history, AIS and ADS-B feeds, fitness trackers, GPX and
KML imports, and body-worn camera metadata.

**1. A `GeoLocationEntry` cannot say when it was observed.**

`uco-observable:GeoLocationEntryFacet` has exactly two properties, `application`
and `location`. `uco-observable:GeoLocationTrackFacet` has `startTime` and
`endTime`, but they bound the whole track. So a UCO track can state that an
aircraft flew between 11:50:49Z and 11:53:00Z, and it can list fifteen positions,
but it cannot state that the aircraft was at 51.7620366, −1.2565564 *at
11:51:30.180Z*.

The inherited `uco-core:objectCreatedTime` is not a substitute. It is defined as
the time the *object* was created — the record — which for parsed evidence is the
time the analyst ran the parser, not the time the receiver computed the fix. Using
it for the fix time would silently overload a property with a different meaning,
and would break the moment a graph legitimately needs both.

The practical consequence is that the central question of any location analysis —
"where was the subject at time T?" — is not answerable by SPARQL against a
conforming UCO graph. The information is present in every source format; it is
lost at ingest.

**2. `LatLongCoordinatesFacet` carries an altitude with no datum.**

`uco-location:altitude` is a bare decimal. "20.09" can mean metres above the
WGS-84 ellipsoid (what a bare GNSS receiver outputs), above mean sea level (what
geoid-corrected and barometric figures use), above ground level (what a
rangefinder or terrain database gives), or above the takeoff point (what a
multirotor reports to its operator). These differ by tens of metres in ordinary
conditions. In our source log the same instant is 20.07 m AMSL and 19.99 m above
the launch point, and the aviation rule that matters (14 CFR 107.51, 400 ft) is
expressed against yet another datum.

Two altitudes are only comparable if they share a datum, and a graph that cannot
record the datum cannot support the comparison.

**3. `GPSCoordinatesFacet` cannot carry the accuracy its sources report.**

The facet has `hdop`, `pdop`, `tdop` and `vdop`. Dilution of precision describes
satellite *geometry*; it is not an error estimate and cannot be converted to
metres without the receiver's assumed user-equivalent range error. Meanwhile the
sources investigators actually receive report metres directly — Android
`Location.getAccuracy()`, iOS `horizontalAccuracy`/`verticalAccuracy`, NMEA GST,
ASTM F3411 Remote ID accuracy fields, and the ArduPilot GPA record we parsed
(HAcc/VAcc). That value has to be discarded or pushed into a description string.

Also missing are the satellite count and the fix type. Both matter for weight:
a small satellite count alongside optimistic reported precision is a standard
signature of a spoofed or replayed GNSS signal, and a fix type of `simulated`
means the position is not evidence of where anything physically was — which a
consumer of the graph must be able to see without reading prose.

# Requirements

## Requirement 1

`uco-observable:GeoLocationEntryFacet` shall have an optional property
`observationTime` (`xsd:dateTime`, max 1) recording when the position fix was
observed, distinct from when the record was created.

## Requirement 2

`uco-location:LatLongCoordinatesFacet` shall have an optional property
`altitudeReference` (`xsd:string`, max 1) recording the datum `altitude` is
measured from, as an open vocabulary with recommended values `WGS84 ellipsoid`,
`mean sea level`, `above ground level`, `above takeoff point`.

## Requirement 3

`uco-location:LatLongCoordinatesFacet` shall have optional properties
`horizontalAccuracy` and `verticalAccuracy` (`xsd:decimal`, metres, max 1 each)
recording the uncertainty the source reports. They are kept separate because GNSS
vertical error is characteristically two to three times the horizontal error.

## Requirement 4

`uco-location:GPSCoordinatesFacet` shall have optional properties
`satelliteCount` (`xsd:nonNegativeInteger`, max 1) and `fixQuality`
(`xsd:string`, max 1, open vocabulary: `no fix`, `2D fix`, `3D fix`, `DGPS`,
`RTK float`, `RTK fixed`, `dead reckoning`, `manual input`, `simulated`).

## Requirement 5

All five properties are optional. No existing graph becomes non-conforming, and
no existing property changes meaning.

# Risk / Benefit analysis

## Benefits

- Makes "where was the subject at time T?" answerable in SPARQL against a
  conforming graph, which is the point of modelling a track at all.
- Removes an ambiguity in `altitude` that currently makes altitude comparisons
  between two UCO graphs unsound.
- Lets UCO carry the accuracy figures that mobile operating systems, GNSS
  receivers, and the ASTM F3411 Remote ID standard already publish, instead of
  discarding them or hiding them in prose.
- Makes non-authentic positions (`fixQuality` = `simulated`) visible to a machine.
  This is not hypothetical: the source log for this proposal is a
  software-in-the-loop capture, and nothing in a conforming UCO graph could have
  said so.

## Risks

- **Overlap with `objectCreatedTime`.** Some implementers already misuse it as a
  fix time. Mitigation: the property description should state the distinction
  explicitly, as drafted.
- **Datum vocabulary drift.** An open vocabulary invites free text. Mitigation:
  recommended values are enumerated in the property definition; a controlled
  vocabulary could be added later without breaking data.
- **Relationship to GeoSPARQL.** UCO's CDO GeoSPARQL profile can express geometry
  richly, and one could argue accuracy belongs there. We think not: these
  properties describe the *measurement*, not the geometry, and forcing GeoSPARQL
  on every graph that needs a per-fix timestamp is a large dependency for a small
  need. If the committee prefers the GeoSPARQL route we would still ask for
  Requirement 1, which GeoSPARQL does not address.

# Competencies demonstrated

## Competency 1

Reconstruct a subject's position at a specific time from a track.

### Competency Question 1.1

*Where was the subject at a given moment, and how well was that known?*

#### Result 1.1

Three rows, one per fix, each with its own time — impossible today:

```
2026-07-04T11:50:49.200000+00:00 | 51.7607129 | -1.2563709 |  0.1  | mean sea level | 0.3
2026-07-04T11:51:30.180000+00:00 | 51.7620366 | -1.2565564 | 20.09 | mean sea level | 0.3
2026-07-04T11:53:00.180000+00:00 | 51.7607132 | -1.2563711 |  0.09 | mean sea level | 0.3
```

### Competency Question 2.1

*Which fixes fall inside a time window of interest?* (geofence, alibi, airspace
incursion)

#### Result 2.1

```
urn:uuid:e1d07d66-7da2-55f6-b3a4-93236028cee8 | 2026-07-04T11:51:30.180000+00:00
```

### Competency Question 3.1

*Which altitude claims are comparable with each other?*

#### Result 3.1

```
mean sea level | 3 | 20.09
```

### Competency Question 4.1

*Which fixes are trustworthy, and which are not evidence of a physical position?*

#### Result 4.1

```
simulated | 10 | 1.21 | 3
```

### Draft SPARQL

See [`geolocation-entry-observation-time.sparql`](geolocation-entry-observation-time.sparql).

# Example instance data

See [`geolocation-entry-observation-time.jsonld`](geolocation-entry-observation-time.jsonld)
— three fixes from a validated flight-log graph. One entry:

```json
{
  "@id": "urn:uuid:e1d07d66-7da2-55f6-b3a4-93236028cee8",
  "@type": "uco-observable:GeoLocationEntry",
  "uco-core:hasFacet": [{
    "@type": "uco-observable:GeoLocationEntryFacet",
    "uco-observable:location": { "@id": "urn:uuid:..." },
    "proposed-obs:observationTime": {
      "@type": "xsd:dateTime", "@value": "2026-07-04T11:51:30.180Z"
    }
  }]
},
{
  "@type": "uco-location:LatLongCoordinatesFacet",
  "uco-location:latitude":  { "@type": "xsd:decimal", "@value": "51.7620366" },
  "uco-location:longitude": { "@type": "xsd:decimal", "@value": "-1.2565564" },
  "uco-location:altitude":  { "@type": "xsd:decimal", "@value": "20.09" },
  "proposed-loc:altitudeReference": "mean sea level",
  "proposed-loc:horizontalAccuracy": { "@type": "xsd:decimal", "@value": "0.3" },
  "proposed-loc:verticalAccuracy":   { "@type": "xsd:decimal", "@value": "0.3" }
},
{
  "@type": "uco-location:GPSCoordinatesFacet",
  "uco-location:hdop": { "@type": "xsd:decimal", "@value": "1.21" },
  "uco-location:vdop": { "@type": "xsd:decimal", "@value": "2.0" },
  "proposed-loc:satelliteCount": { "@type": "xsd:nonNegativeInteger", "@value": "10" },
  "proposed-loc:fixQuality": "simulated"
}
```

Provenance of the values: DFRWS USA 2026 Rodeo UAS challenge log `uavrodeo.BIN`
(ArduPilot DataFlash, SHA-256
`a2fa5f1f2b63836045f4b74e07d043780ded1126d04db8d5f286896da363693f`), parsed with
`pymavlink`. Latitude, longitude and altitude come from `GPS` records; accuracy
from the paired `GPA` records (HAcc/VAcc); satellite count and HDOP from the `GPS`
record. `fixQuality` is `simulated` because the log records `RC Protocol: SITL`.

# Solution suggestion

Draft T-Box: [`geolocation-entry-observation-time.ttl`](geolocation-entry-observation-time.ttl).

The terms are declared under `https://proposed.ontology.unifiedcyberontology.org/uco/{observable,location}/`
so that adoption is a prefix rewrite. Suggested final IRIs:

| Proposed | Domain |
|---|---|
| `uco-observable:observationTime` | `uco-observable:GeoLocationEntryFacet` |
| `uco-location:altitudeReference` | `uco-location:LatLongCoordinatesFacet` |
| `uco-location:horizontalAccuracy` | `uco-location:LatLongCoordinatesFacet` |
| `uco-location:verticalAccuracy` | `uco-location:LatLongCoordinatesFacet` |
| `uco-location:satelliteCount` | `uco-location:GPSCoordinatesFacet` |
| `uco-location:fixQuality` | `uco-location:GPSCoordinatesFacet` |

# Pre-submission testing

## SPARQL query testing

```
$ python scripts/sparql_test.py \
    change_proposals/geolocation-entry-observation-time.jsonld \
    change_proposals/geolocation-entry-observation-time.sparql
Loaded 79 triples
  Query 1: 3 result(s) — OK
  Query 2: 1 result(s) — OK
  Query 3: 1 result(s) — OK
  Query 4: 1 result(s) — OK
SPARQL test summary: 4 passed, 0 failed
```

## Graph validation

```
$ python scripts/validate_extension.py \
    extensions/uas/manifest.json \
    change_proposals/geolocation-entry-observation-time.jsonld
Conforms: True
```

Zero violations, zero warnings, zero undeclared concepts, against CASE/UCO 1.4.0
plus the local declarations in `extensions/uas/location-pending.ttl`.

## Local pending declarations

Until this proposal is resolved, the terms are declared locally in
[`extensions/uas/location-pending.ttl`](../extensions/uas/location-pending.ttl),
which is bundled with the candidate `uas` extension and referenced from
[`docs/recipes/candidates/uas-flight-log.md`](../docs/recipes/candidates/uas-flight-log.md).

# Unresolved issues

- Should `observationTime` live on the facet (proposed here, consistent with UCO's
  facet pattern) or directly on `GeoLocationEntry`?
- Should `fixQuality` become a controlled `HashNameVocab`-style vocabulary rather
  than an open string? We suggest starting open, since receiver vendors keep
  adding fix types (RTK variants, PPP, sensor fusion).
- Is there appetite for a companion `positionSource` property distinguishing GNSS,
  cell-tower, Wi-Fi, dead-reckoning and manual entry? We did not need it for this
  case but it is the obvious neighbour.
