# MSAB XRY and XAMN Export

> See [Recipe Index](INDEX.md) for all recipes.

Map an MSAB XRY extraction into CASE/UCO. XRY differs from the other two
commercial mobile formats in this catalog in a way that shapes the whole graph:
the `.xry` container is proprietary, forensically sealed, and optionally
encrypted, and MSAB distributes the **XAMN Extended XML** schema through its
customer portal rather than publishing it. The community repository
([CASE-Implementation-XRY](https://github.com/casework/CASE-Implementation-XRY))
contains no parser at all — only a three-object example graph naming the tool.

This recipe therefore models what is knowable without the schema, and marks the
boundary explicitly rather than inventing element names to fill it.

## When to use this recipe

- You have a `.xry` container and need it represented as evidence in a graph
  alongside other extractions.
- You have a XAMN or XEC Export **Extended XML** file and are building the
  mapping for it.
- You are reconciling an XRY extraction against a UFED or AXIOM extraction of the
  same device.

Use a different recipe when:

- The extraction came from Cellebrite UFED — see
  [cellebrite-ufed-xml.md](cellebrite-ufed-xml.md), which has a documented
  element vocabulary.
- The extraction came from Magnet AXIOM — see
  [magnet-axiom-export.md](magnet-axiom-export.md).

## What the format does and does not give you

| Artifact | Status | Consequence for modeling |
|---|---|---|
| `.xry` container | Proprietary, sealed, audit-trailed; 256-bit encryption available since XRY 10.4 | Model as a file with a digest and `uco-observable:isEncrypted`; do not model its interior |
| XAMN Extended XML | Schema not public | Map XAMN's documented content categories; leave element names for the mapping table until you hold the schema |
| XEC Export output | Same Extended XML, produced unattended from a watched folder | Same mapping; the difference is only which tool is the `uco-action:instrument` |
| XAMN content categories | Visible in the product UI | The stable hook a mapping can be built on today |

## Real test data and what XAMN documents

The [Digital Corpora Android 13
dataset](https://digitalcorpora.s3.amazonaws.com/s3_browser.html#corpora/mobile/android_13/)
publishes a real XRY extraction of a test phone, `Android_13_MSAB.xry`
(22.06 GB), next to the free XAMN Viewer 7.4 that opens it. The viewer's
quick start guide says it may be freely distributed within an organization,
so anyone can produce exports from that file locally. The same dataset holds
UFED output for the same phone, which makes it the natural two-tool test for
[cross-report-file-identity.md](cross-report-file-identity.md).

The container opens with the magic `XRY\0` and a run of four-letter segment
tags (`PSEC`, `MET`, `SEG`, `SEC`, `DAT`, `PSEG`) in the first 220 bytes.
After that there are no readable strings, which is consistent with a
compressed or encrypted payload. That confirms the advice below: identify
and hash the container; don't parse it.

The XAMN 7.4 help bundled with the viewer documents these export behaviours.
None of them is the Extended XML schema, but each changes how an export
should be modeled:

| XAMN 7.4 export | Documented behaviour | Modeling consequence |
|---|---|---|
| Extended XML | "The XML-tags are not translated"; extracted files are included only if the File format is also selected | Element names don't vary with report language, so they are a stable mapping key once seen. Without File export, the XML describes files it doesn't contain |
| File | One folder per data source; optional XML manifest ("Create manifest") | Hash each exported file; the manifest is a second source of paths to check against |
| File, "Reflect original path" | Exported paths mirror the exhibit; unchecked, the layout is flatter | Only with this option is the exported path a device path. Otherwise it describes the export layout and belongs in `uco-core:description`, not `uco-observable:filePath` |
| File, "Add file extension" | Extensions added "based on the actual file content" | The exported name may differ from the on-device name; record the device name |
| Excel/ODS "Adaptive" | One tab per artifact type, all properties as columns | The richest tabular export; tab and column names are the mapping key |
| Excel "HashOnly" | One sheet per hash property (SHA-1, MD5, ...) | Each sheet gives single-hash report entries; content cores in [cross-report-file-identity.md](cross-report-file-identity.md) join them |
| "Organize output by: XRY file" | Artifacts sorted per category "as in the XRY file" | Ordering reflects the container, not the examiner's view |
| VICS (Project VIC) | JSON with hash values and VIC properties for pictures and videos; VICS 1.2, 1.3, and 2.0 | A hash-set export, not an extraction report; treat it as one more report of the same content |
| Nuix | `.msabnuix` container with extracted files and XAMN tags | A derived container; hash it and relate it to the `.xry` with `Extracted_From` |
| "Export to .bin" | Raw image of a physical extraction, one per image; "Encrypted data will still be encrypted" | A derived file: hash it, set `uco-observable:isEncrypted` when applicable |

What still needs a real export to confirm: the Extended XML element names, and
whether each artifact carries a source path. Fill the mapping column below
from the file itself, not from this table.

## The tool chain

MSAB splits across three products, and which one produced a given file is a
recordable fact.

| Product | CASE/UCO | `uco-tool:toolType` |
|---|---|---|
| XRY | `uco-tool:Tool` | `Extraction` |
| XAMN Horizon / Elements | `uco-tool:AnalyticTool` | `Analysis` |
| XEC Export | `uco-tool:Tool` | `Export` |

All three take `uco-tool:creator` -> `uco-identity:Organization` "MSAB". The
extraction action produces the `.xry`; the conversion action consumes it and
produces the Extended XML.

## The sealed container

The container is the root evidence item. Hash it, flag its encryption, and say
plainly in `uco-core:description` why its interior is absent from the graph — an
unexplained gap reads as an omission, an explained one reads as a boundary.

```json
{
  "@id": "kb:File-3941536c-96a8-49ca-8590-1da2cf3cd6bf",
  "@type": "uco-observable:File",
  "uco-core:description": [
    "Proprietary forensically sealed container with an internal audit trail. XRY 10.4 and later support configurable 256-bit encryption. It is recorded as an evidence file; its interior is not modelled because no public reader exists."
  ],
  "uco-core:hasFacet": [
    {
      "@type": "uco-observable:FileFacet",
      "uco-observable:fileName": "Samsung_SM-G991B_2026-05-12.xry",
      "uco-observable:extension": "xry"
    },
    {
      "@type": "uco-observable:ContentDataFacet",
      "uco-observable:mimeType": "application/octet-stream",
      "uco-observable:isEncrypted": { "@type": "xsd:boolean", "@value": "true" },
      "uco-observable:hash": [
        {
          "@type": "uco-types:Hash",
          "uco-types:hashMethod": "SHA256",
          "uco-types:hashValue": { "@type": "xsd:hexBinary", "@value": "B034102901D8..." }
        }
      ]
    }
  ]
}
```

Pair it with the export using nested exhibit numbers, so the derived file is
visibly subordinate to the sealed original:

```json
{
  "@type": "case-investigation:ProvenanceRecord",
  "uco-core:name": "XAMN Extended XML export",
  "case-investigation:exhibitNumber": "EX-2026-0512-01-A",
  "case-investigation:rootExhibitNumber": "EX-2026-0512-01",
  "uco-core:object": [ { "@id": "kb:File-bf10e9b8-..." } ]
}
```

## Content categories to CASE class

XAMN organizes decoded data by content category rather than a published artifact
taxonomy. Those categories are the stable hook. The right-hand column is what you
fill in from the actual export once you have it; leave it blank rather than
guessing.

| XAMN content category | CASE/UCO class | Facet(s) | Extended XML element |
|---|---|---|---|
| Messages (SMS/MMS) | `uco-observable:SMSMessage` | `uco-observable:MessageFacet` + `uco-observable:SMSMessageFacet` | *to be confirmed against the schema* |
| App messages / chats | `uco-observable:Message`, `uco-observable:MessageThread` | `uco-observable:MessageFacet`, `uco-observable:MessageThreadFacet` | *to be confirmed* |
| Calls | `uco-observable:Call` | `uco-observable:CallFacet` | *to be confirmed* |
| Contacts | `uco-observable:Contact` | `uco-observable:ContactFacet` + `uco-observable:ContactPhone` | *to be confirmed* |
| Locations | `uco-location:Location` | `uco-location:LatLongCoordinatesFacet` | *to be confirmed* |
| Web history | `uco-observable:URLHistory` | `uco-observable:URLHistoryFacet` + `uco-observable:URLHistoryEntry` | *to be confirmed* |
| Pictures / Videos / Audio / Files | `uco-observable:RasterPicture`, `uco-observable:File` | `uco-observable:FileFacet` + `uco-observable:ContentDataFacet` (+ `uco-observable:RasterPictureFacet`) | *to be confirmed* |
| Device information | `uco-observable:MobilePhone` | `uco-observable:DeviceFacet` + `uco-observable:MobileDeviceFacet` | *to be confirmed* |
| SIM data | `uco-observable:SIMCard` | `uco-observable:SIMCardFacet` | *to be confirmed* |
| Installed applications | `uco-observable:Application` | `uco-observable:ApplicationFacet` | *to be confirmed* |
| Accounts | `uco-observable:DigitalAccount` | `uco-observable:DigitalAccountFacet` | *to be confirmed* |
| Wireless networks | `uco-observable:WirelessNetworkConnection` | `uco-observable:WirelessNetworkConnectionFacet` | *to be confirmed* |

Facet choices are identical to the UFED and AXIOM recipes on purpose: a
two-tool case should produce comparable graphs, and the only thing that should
differ between them is provenance.

## AI-derived classifications are analysis, not observation

XAMN ships image classifiers for categories such as weapons, drugs, and people.
A classifier result is an interpretation of a picture, not a property of it.
Model it as a separate node — see
[analysis.md](analysis.md) for classification with confidence scores, and
[ai-analysis-pipeline.md](ai-analysis-pipeline.md) for multi-step inference —
and never as a `uco-core:tag` that reads like ground truth.

## Joining artifacts without a source path

UFED gives you `extraInfo`/`nodeInfo` and AXIOM gives you the `Source` fragment,
so both support a full `Contained_Within` chain from artifact to source file to
image. Extended XML is not confirmed to carry a per-artifact source path. Until
it is, the honest edge is `Extracted_From` the container:

```json
{
  "@type": "uco-observable:ObservableRelationship",
  "uco-core:kindOfRelationship": "Extracted_From",
  "uco-core:isDirectional": { "@type": "xsd:boolean", "@value": "true" },
  "uco-core:source": { "@id": "kb:SMSMessage-..." },
  "uco-core:target": { "@id": "kb:File-3941536c-..." },
  "uco-core:description": [
    "Decoded from the sealed container; Extended XML does not yet give a per-artifact source path to build a Contained_Within chain."
  ]
}
```

If the schema turns out to carry a source path, upgrade these edges to
`Contained_Within` against a real file observable and update this recipe — that
is exactly the improvement pass described in
[recipe-authoring.md](recipe-authoring.md).

## Marking what is provisional

Claims that depend on the unpublished schema should carry controlled tags from
`docs/vocabularies/epistemic-tags.json` rather than being asserted flatly:

- `epistemic:reported` — the value came from a tool report you have not verified
  against the source bytes.
- `epistemic:unattributed` — you cannot yet name the on-device artifact the value
  was decoded from.
- `hash-status:not-published` — a digest is genuinely unavailable, as opposed to
  omitted by oversight.

A reviewer can then filter on tag to see exactly which assertions rest on the
schema gap.

## Anti-patterns

- **Do not invent Extended XML element names.** No public schema exists. A
  mapping table with plausible-looking element names is worse than an empty
  column, because the next agent will trust it. Leave it marked as unconfirmed
  and fill it from the real file.
- **Do not model the interior of the `.xry` container.** It is sealed, often
  encrypted, and has no open reader. Model it as a file with a digest.
- **Do not claim decoding you did not perform.** If you only have the container,
  the graph contains a device, a container, and a tool chain. That is a complete
  and honest graph.
- **Do not treat XAMN's AI image classifications as observations.** They are
  analysis results and need their own node with a stated method and confidence.
- **Do not use `Contained_Within` for an artifact whose source file you cannot
  name.** `Extracted_From` says what you actually know.
- **Do not assume XRY and UFED agree.** XAMN can import UFED files, so a XAMN
  case may contain artifacts that another vendor decoded. Attribute each artifact
  to the tool that decoded it, not to the tool that displayed it.
- **Do not infer a SOLVE-IT technique from the product name.** "XRY" is not
  evidence that a particular extraction technique was used; the extraction log
  is. See [technique-evidence-outcome.md](technique-evidence-outcome.md).

## Checklist

1. Hash the `.xry` container and record it as a `File` with
   `uco-observable:isEncrypted` set from the extraction settings.
2. Build the tool chain: MSAB `Organization`, XRY `Tool`, XAMN `AnalyticTool`,
   and XEC Export `Tool` if batch conversion was used.
3. Create the extraction action (result: the container) and the conversion action
   (object: the container, result: the Extended XML).
4. Nest the exhibit numbers with `case-investigation:rootExhibitNumber` so the
   export is visibly derived from the sealed original.
5. Model the device, OS, and SIM from the identifiers XRY reports in every
   extraction.
6. Map decoded artifacts by XAMN content category using the table above.
7. Join artifacts to the container with `Extracted_From` until a per-artifact
   source path is confirmed.
8. Tag schema-dependent claims `epistemic:reported` or `epistemic:unattributed`.
9. For File exports, check whether "Reflect original path" was set before
   writing any exported path into `uco-observable:filePath`. When a UFED or
   AXIOM report covers the same exhibit, key files as in
   [cross-report-file-identity.md](cross-report-file-identity.md).
10. Validate: `case_validate --built-version case-1.5.0 xry-export.jsonld`, or
   `validate_graph(path)` through the MCP server for strict concept coverage.

## When the Extended XML schema arrives

This recipe is deliberately incomplete in one column. When a real export is in
hand:

1. Fill the Extended XML element column from the actual file, not from the
   schema documentation alone — exports and schemas drift. The Digital
   Corpora `Android_13_MSAB.xry` opened in XAMN gives a shareable reference
   export; record the XAMN version, because a later release may change it.
2. Check whether a per-artifact source path exists; if so, replace the
   `Extracted_From` edges with a `Contained_Within` chain.
3. Re-run the exemplar builder and re-validate before publishing.
4. Drop the `epistemic:reported` / `epistemic:unattributed` tags from claims that
   the real export substantiates.
5. If XRY reports something core CASE/UCO cannot express, follow
   [change-proposal.md](change-proposal.md) before reaching for a local
   extension.

## Validated exemplar

`examples/vendor-exports/build_msab_xry_export.py` builds
`examples/vendor-exports/msab-xry-export.jsonld`: 32 nodes covering the MSAB tool
chain, the sealed container with its digest and encryption flag, nested exhibit
numbering across two provenance records, device, OS and SIM, and one artifact per
major XAMN content category joined with `Extracted_From`. It conforms against
CASE 1.4.0 with zero violations and zero undeclared concepts. Field values are
synthetic, and no Extended XML element name is asserted anywhere in it. A real
`.xry` for a test phone is published by Digital Corpora (see above).

```bash
python3 examples/vendor-exports/build_msab_xry_export.py
case_validate --built-version case-1.5.0 examples/vendor-exports/msab-xry-export.jsonld
```

## Related

- [cellebrite-ufed-xml.md](cellebrite-ufed-xml.md) — UFED, where the element vocabulary is documented
- [magnet-axiom-export.md](magnet-axiom-export.md) — AXIOM's `Artifact`/`Hit`/`Fragment` export
- [cross-report-file-identity.md](cross-report-file-identity.md) — joining XRY, UFED, and AXIOM reports of the same files
- [starter-mobile-extraction.md](starter-mobile-extraction.md) — the vendor-neutral starting point
- [mobile-device-sim.md](mobile-device-sim.md) — handset and SIM modeling in depth
- [chain-of-custody.md](chain-of-custody.md) — exhibit numbering and derived-evidence records
- [analysis.md](analysis.md) — classification results with confidence, for XAMN's AI categories
- [ai-analysis-pipeline.md](ai-analysis-pipeline.md) — multi-step inference and per-result scoring
- [advanced-file-patterns.md](advanced-file-patterns.md) — encrypted containers and nested evidence
- [recipe-authoring.md](recipe-authoring.md) — how to complete this recipe once the schema is held
