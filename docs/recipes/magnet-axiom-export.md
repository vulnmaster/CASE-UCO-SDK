# Magnet AXIOM Export

> See [Recipe Index](INDEX.md) for all recipes.

Map a Magnet AXIOM case into CASE/UCO. AXIOM does not have a single canonical
export: the case database (`Case.mfdb`) has no published schema, so the
practical ingestion target is the **XML export produced by AXIOM Examine**,
whose vocabulary is just three nested elements — `Artifact`, `Hit`, and
`Fragment`. The community parser
([CASE-Implementation-AXIOM](https://github.com/casework/CASE-Implementation-AXIOM))
reads that XML, and this recipe reuses its artifact/fragment vocabulary while
supplying the investigative spine that parser builds but never emits.

## When to use this recipe

- You have an XML export from AXIOM Examine (`--type Xml`, `XmlExternalFiles`,
  or `XmlBase64`), or CSV/XLSX artifact exports from the same case.
- You received an AXIOM Portable Case folder and need to model what it contains.
- You are reconciling AXIOM output against another tool's extraction of the same
  device.

Use a different recipe when:

- The extraction came from Cellebrite UFED — see
  [cellebrite-ufed-xml.md](cellebrite-ufed-xml.md).
- The extraction came from MSAB XRY — see [msab-xry-export.md](msab-xry-export.md).
- You are modeling the AXIOM run itself as a tool execution with no artifact
  detail — [starter-tool-run.md](starter-tool-run.md) is smaller.

## Source input shape

```xml
<Artifact name="iOS WhatsApp Messages">
  <Hits>
    <Hit>
      <Fragment name="Message"><![CDATA[Pickup moved to the north lot at 4.]]></Fragment>
      <Fragment name="Message Sent Date/Time - UTC+00:00">2026-03-29 20:58:11</Fragment>
      <Fragment name="Sender">+15555550142</Fragment>
      <Fragment name="Source">.../ChatStorage.sqlite (APFS)</Fragment>
      <Fragment name="Location">0x1A2B3C</Fragment>
      <Fragment name="Recovery method">Parsing</Fragment>
    </Hit>
  </Hits>
</Artifact>
```

`Artifact/@name` selects the artifact family, `Hit` is one record, and
`Fragment/@name` is one field. Three fragments recur on nearly every artifact and
carry provenance rather than content:

| Fragment | Meaning | CASE/UCO |
|---|---|---|
| `Source` | the file the hit was recovered from | `Contained_Within` edge to a `uco-observable:File` |
| `Location` | offset or path inside that source | `uco-core:description` on the edge, or `uco-observable:DataRangeFacet` when byte-exact |
| `Recovery method` | `Parsing` (allocated) or `Carving` (unallocated) | `uco-observable:RecoveredObjectFacet` when carved; nothing when parsed |

## Two products, two actions

AXIOM Process acquires and searches; AXIOM Examine reviews and exports. Modeling
them as one tool loses the fact that the export was generated later, possibly by
a different examiner, and possibly filtered by an artifact profile.

| Artifact | CASE/UCO |
|---|---|
| AXIOM Process | `uco-tool:Tool`, `uco-tool:toolType` "Acquisition", `uco-tool:creator` -> `uco-identity:Organization` "Magnet Forensics" |
| AXIOM Examine | `uco-tool:AnalyticTool`, `uco-tool:toolType` "Analysis" |
| Image acquisition and artifact search | `case-investigation:InvestigativeAction` with the image and `Case.mfdb` as `uco-action:result` |
| XML export | a second `case-investigation:InvestigativeAction` with `Case.mfdb` as `uco-action:object` and the XML as `uco-action:result` |
| `Case.mfdb` | `uco-observable:File` only — the schema is unpublished, so record it as evidence rather than claiming to parse it |
| The XML export | `uco-observable:File` + `uco-observable:ContentDataFacet`, wrapped in a `case-investigation:ProvenanceRecord` |

```json
{
  "@id": "kb:AnalyticTool-2c0d754f-899d-4fd3-a025-70ce43d2ddf5",
  "@type": "uco-tool:AnalyticTool",
  "uco-core:name": "Magnet AXIOM Examine",
  "uco-tool:creator": { "@id": "kb:Organization-2ce6dae9-..." },
  "uco-tool:toolType": "Analysis",
  "uco-tool:version": "8.4.0.41310"
}
```

**Record the export locale.** AXIOM localizes both artifact names and fragment
names. A mapping keyed on English strings silently drops every artifact from a
non-`en-US` export — no error, just a smaller graph. Put the locale in the export
action's `uco-core:description` so a reviewer can see which vocabulary the
mapping assumed.

## Artifact family to CASE class

AXIOM organizes artifacts by platform (Windows, Android, iOS, macOS) and then by
category (Chat, Media, Web Related, Operating System, Wireless Networks, ...).
The category, not the app-specific artifact name, determines the facet set —
`iOS WhatsApp Messages` and `Signal Messages - Windows` model identically.

| Artifact family (representative `Artifact/@name`) | CASE/UCO class | Facet(s) |
|---|---|---|
| `iOS Device Information`, `Android Device Information` | `uco-observable:MobilePhone` | `uco-observable:DeviceFacet` + `uco-observable:MobileDeviceFacet` |
| `File System Information` | `uco-observable:FileSystem` | `uco-observable:FileSystemFacet` |
| `Pictures`, `Videos`, `Audio`, `PDF Documents`, `Word Documents` | `uco-observable:RasterPicture`, `uco-observable:File` | `uco-observable:FileFacet` + `uco-observable:ContentDataFacet` (+ `uco-observable:EXIFFacet`) |
| `iOS WhatsApp Messages`, `Telegram Messages - Android`, `Signal Messages` | `uco-observable:Message` | `uco-observable:MessageFacet` |
| `Android SMS`, `iOS iMessage/SMS/MMS` | `uco-observable:SMSMessage` | `uco-observable:MessageFacet` + `uco-observable:SMSMessageFacet` |
| `Android Call Logs`, `iOS Call Logs` | `uco-observable:Call` | `uco-observable:CallFacet` |
| `Android Contacts`, `Apple Contacts - iOS` | `uco-observable:Contact` | `uco-observable:ContactFacet` |
| `Apple Mail`, `Gmail Emails`, `Android Emails` | `uco-observable:EmailMessage` | `uco-observable:EmailMessageFacet` |
| `Chrome Web History`, `Safari History`, `Edge Chromium Web History` | `uco-observable:URLHistory` | `uco-observable:URLHistoryFacet` + `uco-observable:URLHistoryEntry` |
| `Chrome Cookies`, `Firefox Cookies` | `uco-observable:BrowserCookie` | `uco-observable:BrowserCookieFacet` |
| `Parsed Search Queries`, `Google Searches` | `uco-observable:URLHistory` | `uco-observable:URLHistoryEntry` with `uco-observable:keywordSearchTerm` |
| `Significant Locations`, `WiFi Locations` | `uco-location:Location` | `uco-location:LatLongCoordinatesFacet` |
| `Cell Tower Locations` | `uco-observable:CellSite` | `uco-observable:CellSiteFacet` |
| `KnowledgeC Application Usage`, `Windows Timeline Activity`, `KnowledgeC Device Lock States` | `uco-observable:EventRecord` | `uco-observable:EventRecordFacet` |
| `Android WhatsApp Accounts Information`, `SIM Card Activity` | `uco-observable:SIMCard`, `uco-observable:DigitalAccount` | `uco-observable:SIMCardFacet`, `uco-observable:DigitalAccountFacet` |

Calendar and bookmark artifacts appear in AXIOM but have no pattern in the
community parser; map them to `uco-observable:CalendarEntry` +
`uco-observable:CalendarEntryFacet` and `uco-observable:BrowserBookmark` +
`uco-observable:BrowserBookmarkFacet`.

## Media artifacts and EXIF

The `Pictures` family carries the richest fragment set: file identity, size,
three timestamps, `MD5 Hash`, and the EXIF fragments `Make`, `Model`,
`GPS Latitude`, `GPS Latitude Reference`, `GPS Longitude`,
`GPS Longitude Reference`, and `Altitude (meters)`.

`uco-observable:exifData` requires a `uco-types:ControlledDictionary`, not a
plain `uco-types:Dictionary`, and its keys should be EXIF tag names:

```json
{
  "@type": "uco-observable:EXIFFacet",
  "uco-observable:exifData": {
    "@type": "uco-types:ControlledDictionary",
    "uco-types:entry": [
      { "@type": "uco-types:ControlledDictionaryEntry", "uco-types:key": "Make", "uco-types:value": "Apple" },
      { "@type": "uco-types:ControlledDictionaryEntry", "uco-types:key": "GPSLatitude", "uco-types:value": "38.9784" },
      { "@type": "uco-types:ControlledDictionaryEntry", "uco-types:key": "GPSLatitudeRef", "uco-types:value": "N" }
    ]
  }
}
```

Then promote the coordinates to a real `uco-location:Location` with
`uco-location:LatLongCoordinatesFacet`. Leaving them only as dictionary strings
makes them invisible to geospatial queries — see
[geosparql-geospatial-evidence.md](geosparql-geospatial-evidence.md) when the
case needs geometry rather than a point.

## Recovery method

`Fragment name="Recovery method"` is the difference between a live file and a
carved one, and it is the fragment most worth preserving:

```json
{
  "@id": "kb:RasterPicture-8d270af3-a2b1-42e0-a086-a4eb71e31393",
  "@type": "uco-observable:RasterPicture",
  "uco-core:hasFacet": [
    { "@type": "uco-observable:FileFacet", "uco-observable:fileName": "carved_00417216.jpg" },
    {
      "@type": "uco-observable:RecoveredObjectFacet",
      "uco-observable:contentRecoveredStatus": "recovered",
      "uco-observable:nameRecoveredStatus": "unknown"
    }
  ]
}
```

`RecoveredObjectStatusVocab` allows `overwritten`, `partially recovered`,
`recovered`, and `unknown`. A carved file usually has recovered content and an
unknown name, because the name came from the carver, not the file system.

## Chain of evidence

`Fragment name="Source"` names the file each hit came from. Turn it into a
`Contained_Within` edge, then relate that source file to the volume and the
volume to the image. See
[cellebrite-ufed-xml.md](cellebrite-ufed-xml.md#chain-of-evidence-extrainfo-and-nodeinfo)
for the identical pattern on the UFED side; keeping both tools' chains shaped the
same way is what lets a two-tool case be queried once.

## Anti-patterns

- **Do not emit observables with no tool, action, or provenance layer.** The
  community parser contains a complete chain-of-custody block —
  `writeContextAxiom()` builds the Tool, Role, Identity, ProvenanceRecord, and
  both InvestigativeActions — but the main program never calls it, so real AXIOM
  output is observables and relationships with nothing attributing them. Build
  the spine first.
- **Do not treat an AXIOM artifact name as an ontology type.** `Significant
  Locations` is a Magnet product label, not a class. Map it to
  `uco-location:Location`; keep the label in `uco-core:tag` if it is worth
  keeping.
- **Do not assume the export is English.** See the locale note above. Record the
  locale on the export action.
- **Do not synthesize placeholder facts.** The upstream parser substitutes
  `1900-01-01T08:00:00` for missing dates and `'2' * 76` with method `MD5` for
  missing hashes. Omit the property instead; tag the object
  `hash-status:not-published` if the absence is itself significant.
- **Do not claim you parsed `Case.mfdb`.** Magnet publishes no schema for it.
  Record it as a file that the export action consumed.
- **Do not put a raw string in `uco-observable:host`.** It references a
  `uco-observable:DomainName` observable. The same applies to
  `uco-observable:manufacturer`, which references a `uco-identity:Identity`.
- **Do not merge AXIOM and UFED artifacts for the same device into one
  observable** on the strength of a matching filename. Model both, hash both, and
  relate them — agreement between two tools is a finding, not a given.

## Checklist

1. Confirm the export locale is `en-US`, or obtain the localized artifact and
   fragment names before mapping.
2. Hash the XML export; build the `ProvenanceRecord` around it.
3. Build the spine: Magnet `Organization`, AXIOM Process `Tool`, AXIOM Examine
   `AnalyticTool`, examiner `Identity`, acquisition and export actions.
4. Model `iOS/Android Device Information` and `File System Information` first so
   later artifacts have something to be contained within.
5. Walk each `Artifact` element, mapping its family to a typed observable and its
   fragments to facet properties.
6. For every hit, emit the `Source` fragment as a `Contained_Within` edge and
   apply `RecoveredObjectFacet` when `Recovery method` is `Carving`.
7. Promote EXIF GPS fragments to a `Location` with coordinates.
8. Validate: `case_validate --built-version case-1.4.0 axiom-export.jsonld`, or
   `validate_graph(path)` through the MCP server for strict concept coverage.

## Validated exemplar

`examples/vendor-exports/build_magnet_axiom_export.py` builds
`examples/vendor-exports/magnet-axiom-export.jsonld`: 36 nodes covering both
tools, the acquisition and export actions, device and OS, a file system, a parsed
picture with EXIF and a carved picture with a recovery facet, a chat message,
Safari history with a domain and URL, a cookie, and a cell site. It conforms
against CASE 1.4.0 with zero violations and zero undeclared concepts. Field
values are synthetic — no licensed Magnet output is redistributable — but every
artifact name and fragment name in this recipe is from a real AXIOM export, and
every hash in the exemplar is computed over bytes the builder defines.

```bash
python3 examples/vendor-exports/build_magnet_axiom_export.py
case_validate --built-version case-1.4.0 examples/vendor-exports/magnet-axiom-export.jsonld
```

## Related

- [cellebrite-ufed-xml.md](cellebrite-ufed-xml.md) — the same spine for UFED's `modelType` report
- [msab-xry-export.md](msab-xry-export.md) — MSAB XRY, where the export schema is not public
- [starter-mobile-extraction.md](starter-mobile-extraction.md) — the vendor-neutral starting point
- [exif-data.md](exif-data.md) — EXIF tags and camera identification in depth
- [file-recovery.md](file-recovery.md) — carved files and `RecoveredObjectFacet`
- [file-system.md](file-system.md) — volumes, file systems, and containment
- [starter-tool-run.md](starter-tool-run.md) — tool execution with input/output linking
- [chain-of-custody.md](chain-of-custody.md) — provenance records and exhibit numbering
- [geosparql-geospatial-evidence.md](geosparql-geospatial-evidence.md) — when coordinates need real geometry
