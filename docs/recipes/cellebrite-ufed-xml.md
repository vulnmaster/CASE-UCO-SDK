# Cellebrite UFED XML Report

> See [Recipe Index](INDEX.md) for all recipes.

Map a Cellebrite UFED Physical Analyzer XML report — the `report.xml` at the
root of an unzipped `.ufdr` — into CASE/UCO. UFED is the best-documented of the
three commercial mobile formats this catalog covers: its report is a single XML
tree with a stable element vocabulary, and it is the only one of the three whose
community parser
([CASE-Implementation-UFED-XML](https://github.com/casework/CASE-Implementation-UFED-XML))
runs end to end. This recipe follows that parser's structure where it is right
and departs from it where it is wrong, and every departure is called out in
Anti-patterns.

## When to use this recipe

- You have a `report.xml` from UFED Physical Analyzer 7.x, or a `.ufdr` you can
  unzip to reach one.
- You are ingesting a Cellebrite Reader package and want the decoded artifacts,
  not just the file tree.
- You need the chain of evidence that joins a decoded artifact (a message, a
  call) back to the on-device file it was decoded from.
- You only have the extraction summaries (`.ufd`, `EvidenceCollection.ufdx`)
  and need the acquisition recorded before anything is decoded.

Use a different recipe when:

- The extraction came from Magnet AXIOM — see
  [magnet-axiom-export.md](magnet-axiom-export.md).
- The extraction came from MSAB XRY — see [msab-xry-export.md](msab-xry-export.md).
- You only have a generic device summary with no vendor structure — start from
  [starter-mobile-extraction.md](starter-mobile-extraction.md).

## Source input shape

```xml
<project xmlns="http://pa.cellebrite.com/report/2.0" id="..." name="..."
         reportVersion="7.48" extractionType="Legacy" NodeCount="253625" ModelCount="117480">
  <sourceExtractions><extractionInfo id="0" type="Legacy" deviceName="..."/></sourceExtractions>
  <caseInformation><field fieldType="ExaminerName">...</field></caseInformation>
  <metadata section="Additional Fields">
    <item name="UFED_PA_Version"><![CDATA[7.58.0.66]]></item>
  </metadata>
  <metadata section="Device Info">
    <item id="..." name="ICCID" sourceExtraction="0"><![CDATA[...]]></item>
  </metadata>
  <images><image path="... - Data.tar" size="..." verify="NoSourceValues"/></images>
  <taggedFiles>
    <file id="..." fs="TarArchive" path="/data/data/..." size="..." deleted="Intact" embedded="false">
      <accessInfo><timestamp name="ModifyTime">2022-12-03T10:09:59.000+00:00</timestamp></accessInfo>
      <metadata section="File"><item name="MD5">...</item><item name="Local Path">...</item></metadata>
      <RelatedNodes><file id="..." path="/data/user/0/..." isrelated="True">...</file></RelatedNodes>
    </file>
  </taggedFiles>
  <decodedData>
    <modelType type="Chat">
      <model type="Chat" id="..." deleted_state="Intact">
        <field name="Name" type="String"><empty/></field>
        <multiModelField name="Participants" type="Party">
          <model type="Party"><field name="Identifier"/><field name="IsPhoneOwner"/></model>
        </multiModelField>
        <RelatedModels><model type="Chat" isrelated="True">...</model></RelatedModels>
      </model>
    </modelType>
  </decodedData>
  <extraInfos>
    <extraInfo type="model" id="...model id...">
      <sourceInfo><nodeInfos><nodeInfo id="...tagged file id..." tableName="messages" offset="..."/></nodeInfos></sourceInfo>
    </extraInfo>
  </extraInfos>
</project>
```

Every name above is from the Digital Corpora Android 13 report (Physical
Analyzer 7.58.0.66). Read these points before writing a parser:

- `reportVersion` is the report schema version (7.48 here), not the product
  version. The Physical Analyzer version is the `UFED_PA_Version` item.
- `NodeCount` on the root is the number of `<file>` elements, including the
  ones nested in `<RelatedNodes>`. A report with fewer files is truncated.
- Device Info items repeat. That report lists four `ICCID`s, so read the items
  as a list, not a map.
- An empty value is `<empty/>`, not an empty `<value>`.

### Reading it: `iter_report`

`case_uco.vendors.cellebrite.iter_report` streams the report and yields each
tagged file, decoded model, and `extraInfo` link once, then discards it. The
969 MB Android 13 report reads in about 15 seconds with a peak of about 100 MB
of memory. Elements are matched without their namespace, so later schema
namespaces read the same way.

```python
from case_uco.vendors.cellebrite import UfedReport, UfedModel, UfedTaggedFile, iter_report

report = UfedReport()
for item in iter_report("report.xml", report=report, model_types={"Call", "Chat"}):
    if isinstance(item, UfedTaggedFile):
        ...  # item.path, item.size, item.hashes, item.timestamps, item.related_to
    elif isinstance(item, UfedModel):
        ...  # item.value("Source"), item.models["Parties"], item.node_refs, item.related
print(report.report_version, report.item("UFED_PA_Version"), report.warnings)
```

Device Info items whose names look like a passcode or unlock code are
withheld unless you pass `include_secrets=True`. Decoded `Password` models are
evidence and are not filtered (that report has 955), so handle the output
accordingly.

## Extraction summaries: `.ufd` and `.ufdx`

UFED writes two small files next to every extraction, and they often travel
without a `report.xml`: a decoded report is optional, the summary is not.

- **`.ufd`** is INI-style text: `[General]`, `[DeviceInfo]`, `[Dumps]`,
  `[SHA256]`, and so on. It names the acquiring product and version, gives
  the extraction window, lists the dump files with their SHA-256 digests,
  and closes with an HMAC over the file.
- **`EvidenceCollection.ufdx`** is XML that groups the extractions of one
  device: an `EvidenceID`, a `<DeviceInfo>` with vendor, model, and device
  GUID, and one `<Extraction TransferType="..." Path="...">` per `.ufd`.

The layout drifts between releases while `UfdVer` stays at `1.2`, so the
version field tells you nothing about which keys to expect. Three real
summaries from the [Digital Corpora mobile
datasets](https://digitalcorpora.s3.amazonaws.com/s3_browser.html#corpora/mobile/)
show the drift:

| | UFED 7.28.2.8 (2020, Android 10) | Premium SaaS 7.64.0.271 (2023, iOS 15.3.1) | Inseyets UFED Pro 10.2.0.359 (2024, Android 14) |
|---|---|---|---|
| Acquiring product | not stated (`Version` only) | `[General] AcquisitionTool` | `[General] AcquisitionTool` |
| `[DeviceInfo]` | absent; vendor and model are in `[General]` | `IMEI`, `OS`, and the passcode in clear text | `IMEI1`, `IMEI2`, `OS`, `Chipset`, `SecurityPatchLevel` |
| Extraction method | `[Image] ExtractionMethod` | `[FileDump] ExtractionMethod` | `[Image] ExtractionMethod` |
| Hashed files | the dump | the dump | the dump and `SummaryReport.pdf` |
| `[Hash] HMAC` | absent | present | present |
| Per-file `[Dump/...]` sections | 819 | none | none |

Dates look like `14/02/2020 18:43:02 (-5)`: day first, then the UTC offset
in hours. `14/02/2020` is unambiguous; `03/04/2023` is not, so a reader must
assume day-first and say so.

**The passcode is in the file.** The 7.64 summary carries `Passcode_0`,
`PasscodeLength_0`, and `PasscodeType_0` under `[DeviceInfo]`. Never copy
them into a graph. Record that a passcode was supplied, not what it was.

### Reading them with the SDK

`case_uco.vendors.cellebrite` reads all three generations without
version-specific code. It returns a record plus a list of warnings (an
ambiguous date, a missing section, an unexpected hash format) rather than
raising, so one odd file doesn't stop a batch, and it withholds passcode
keys unless you pass `include_secrets=True`.

```python
from case_uco import CASEGraph
from case_uco.vendors.cellebrite import read_ufd, read_ufdx, ufd_to_graph

record = read_ufd("EXTRACTION_FFS 01/EXTRACTION_FFS.ufd")
for warning in record.warnings:
    print("ufd:", warning)

graph = CASEGraph()
nodes = ufd_to_graph(graph, record)
```

`ufd_to_graph` builds the acquisition spine from the summary alone, with
IDs derived from the extraction `GUID`, so ingesting the same `.ufd` twice,
or alongside its `report.xml` graph, merges rather than duplicates:

| `.ufd` source | CASE/UCO |
|---|---|
| `AcquisitionTool` (or "UFED") and `Version` | `uco-tool:Tool` with `uco-tool:version`, created by the Cellebrite `uco-identity:Organization` |
| `Vendor`, `Model`, `DeviceModel` | `uco-observable:MobilePhone` + `uco-observable:DeviceFacet` |
| `IMEI`, `IMEI1`, `IMEI2` | `uco-observable:MobileDeviceFacet`, every slot kept |
| `OS` | `uco-observable:OperatingSystem` + `uco-observable:SoftwareFacet` |
| `[Dumps]` + `[SHA256]` | `uco-observable:File` + `uco-observable:ContentDataFacet` per dump |
| `Date`, `EndTime` | `case-investigation:InvestigativeAction` `uco-action:startTime` / `uco-action:endTime` |
| `Passcode_*` | `uco-core:description` on the action says a passcode was recorded and withheld |

The reader's tests run against the real summaries above
(`python/tests/fixtures/cellebrite/`). The 7.28 file is trimmed to two of its
819 file-part sections.

## The investigative spine

Four sections of the report describe the examination rather than the evidence.
Model them before any artifact, because everything else hangs off them.

| Report location | CASE/UCO |
|---|---|
| `<metadata section="Additional Fields">` `UFED_PA_Version` | `uco-tool:Tool` "UFED Physical Analyzer" with `uco-tool:version`, `uco-tool:toolType` "Extraction", `uco-tool:creator` -> `uco-identity:Organization` "Cellebrite DI Ltd." |
| `<metadata section="Extraction Data">` start/end datetimes | `case-investigation:InvestigativeAction` with `uco-action:startTime` / `uco-action:endTime` |
| `<caseInformation><field fieldType="ExaminerName">` | `uco-identity:Identity` on `uco-action:performer` |
| `<images><image>` + `<metadata section="Hashes">` | `uco-observable:File` + `uco-observable:ContentDataFacet` with `uco-types:Hash`, as `uco-action:result` of the acquisition |
| `report.xml` itself | `uco-observable:File` wrapped in a `case-investigation:ProvenanceRecord` with `case-investigation:exhibitNumber` |

Two actions, not one: UFED 4PC (or Touch) performs the acquisition and produces
the image; Physical Analyzer decodes that image and writes `report.xml`. Chaining
them with the image as the second action's `uco-core:object` records who decoded
what, which is exactly the question a defence expert asks.

## Device, OS, and SIM

`<metadata section="Device Info">` carries the identifiers for three separate
observables. Do not fold them into one node — the SIM travels independently of
the handset and the OS version changes without the hardware changing.

| Device Info item | CASE/UCO |
|---|---|
| `DeviceInfoDetectedPhoneVendor` / `...PhoneModel` | `uco-observable:MobilePhone` + `uco-observable:DeviceFacet` (`uco-observable:manufacturer` -> `uco-identity:Organization`, `uco-observable:model`) |
| `IMEI`, network | `uco-observable:MobileDeviceFacet` (`uco-observable:IMEI`, `uco-observable:network`) |
| `DeviceInfoBluetoothDeviceAddress` | `uco-observable:BluetoothAddressFacet` |
| `DeviceInfoWiFiMACAddress` | `uco-observable:WifiAddressFacet` |
| `DeviceInfoOSType` / `DeviceInfoOSVersion` | `uco-observable:OperatingSystem` + `uco-observable:SoftwareFacet`, `Contained_Within` the phone |
| `ICCID`, `IMSI` | `uco-observable:SIMCard` + `uco-observable:SIMCardFacet`, `Contained_Within` the phone |

```json
{
  "@id": "kb:MobilePhone-938cbdad-dc1a-44e8-8967-08e79a61928e",
  "@type": "uco-observable:MobilePhone",
  "uco-core:hasFacet": [
    {
      "@type": "uco-observable:DeviceFacet",
      "uco-observable:deviceType": "Mobile Phone",
      "uco-observable:manufacturer": { "@id": "kb:Organization-81a9fe34-..." },
      "uco-observable:model": "Pixel 3",
      "uco-observable:serialNumber": "8AEX0EXAMPLE01"
    },
    {
      "@type": "uco-observable:MobileDeviceFacet",
      "uco-observable:IMEI": "356938035643809",
      "uco-observable:bluetoothDeviceName": "Pixel 3",
      "uco-observable:network": "LTE"
    },
    { "@type": "uco-observable:BluetoothAddressFacet", "uco-observable:addressValue": "00:1A:7D:DA:71:13" },
    { "@type": "uco-observable:WifiAddressFacet", "uco-observable:addressValue": "3C:5A:B4:00:11:22" }
  ]
}
```

`uco-observable:SIMForm` is drawn from `SIMFormVocab`, whose members are
`Full-size SIM`, `Micro SIM`, and `Nano SIM`. A literal such as `nano-SIM`
passes SHACL but fails the vocabulary check.

## modelType to CASE class

Each `<modelType type="X">` holds `<model type="X">` instances. Give each model a
typed observable rather than a bare `uco-observable:ObservableObject`; the typed
class is what lets a downstream SPARQL query find all calls without knowing which
facet the producer chose.

| `modelType/@type` | CASE/UCO class | Facet(s) |
|---|---|---|
| `Call` | `uco-observable:Call` | `uco-observable:CallFacet` |
| `SMS` | `uco-observable:SMSMessage` | `uco-observable:MessageFacet` + `uco-observable:SMSMessageFacet` |
| `InstantMessage` | `uco-observable:Message` | `uco-observable:MessageFacet` |
| `Chat` | `uco-observable:MessageThread` | `uco-observable:MessageThreadFacet` |
| `Email` | `uco-observable:EmailMessage` | `uco-observable:EmailMessageFacet` |
| `Contact` | `uco-observable:Contact` | `uco-observable:ContactFacet` |
| `InstalledApplication` | `uco-observable:Application` | `uco-observable:ApplicationFacet` |
| `UserAccount` | `uco-observable:DigitalAccount` | `uco-observable:DigitalAccountFacet` + `uco-observable:ApplicationAccountFacet` |
| `Location` | `uco-location:Location` | `uco-location:LatLongCoordinatesFacet` |
| `CellTower` | `uco-observable:CellSite` | `uco-observable:CellSiteFacet` |
| `WirelessNetwork` | `uco-observable:WirelessNetworkConnection` | `uco-observable:WirelessNetworkConnectionFacet` |
| `VisitedPage` | `uco-observable:URLHistory` | `uco-observable:URLHistoryFacet` + `uco-observable:URLHistoryEntry` |
| `WebBookmark` | `uco-observable:BrowserBookmark` | `uco-observable:BrowserBookmarkFacet` |
| `Cookie` | `uco-observable:BrowserCookie` | `uco-observable:BrowserCookieFacet` |
| `CalendarEntry` | `uco-observable:CalendarEntry` | `uco-observable:CalendarEntryFacet` |
| `DeviceEvent` | `uco-observable:EventRecord` | `uco-observable:EventRecordFacet` |
| `DeviceConnectivity` | `uco-observable:ObservableObject` | `uco-observable:BluetoothAddressFacet` per pairing |
| `Note` | `uco-observable:Note` | `uco-core:description` |
| `CreditCard`, `FinancialAccount`, `TransferOfFunds` | `uco-observable:PaymentCard`, `uco-observable:Account` | `uco-observable:AccountFacet`; see [fraud-crypto-laundering.md](fraud-crypto-laundering.md) |

The community parser handles eighteen model types. Physical Analyzer emits
roughly forty; `CreditCard`, `FinancialAccount`, `TransferOfFunds`, `Password`,
`Journey`, `Recording`, `Voicemail`, `Notification`, and `SIMData` are all
unhandled upstream and often the most probative in a case. Map them here rather
than dropping them.

## Party is an observable, not a string

Every messaging model nests `<model type="Party">` with `Identifier`, `Role`,
`Name`, and `IsPhoneOwner`. The identifier is an account, so it becomes its own
observable that both messages and contacts reference. That is what makes
"who talked to whom" answerable across artifact types.

```json
{
  "@type": "uco-observable:MessageFacet",
  "uco-observable:application": { "@id": "kb:Application-d2d93e8a-..." },
  "uco-observable:from": { "@id": "kb:PhoneAccount-ebd621eb-..." },
  "uco-observable:to": [ { "@id": "kb:PhoneAccount-a0159a40-..." } ],
  "uco-observable:messageText": "Pickup moved to the north lot at 4.",
  "uco-observable:messageType": "Chat",
  "uco-observable:sentTime": { "@type": "xsd:dateTime", "@value": "2026-03-02T20:58:11+00:00" }
}
```

Contacts need one more hop. `uco-observable:contactPhone` requires a
`uco-observable:ContactPhone` wrapper, and that wrapper's
`uco-observable:contactPhoneNumber` references the account observable rather
than repeating the digits:

```json
{
  "@id": "kb:ContactPhone-c4ba1da5-0da3-4d8e-a735-3d2e8f42685a",
  "@type": "uco-observable:ContactPhone",
  "uco-observable:contactPhoneNumber": { "@id": "kb:PhoneAccount-ebd621eb-..." },
  "uco-observable:contactPhoneScope": "mobile"
}
```

`contactPhoneScope` comes from `ContactPhoneScopeVocab`: `home`, `home fax`,
`main`, `mobile`, `pager`, `school`, `work`, `work fax`.

## Chain of evidence: extraInfo and nodeInfo

`<extraInfos><extraInfo type="model" id="...">` matches a decoded
`<model id="...">`, and its `nodeInfo` children give the file, table name, and
byte offset the artifact was decoded from. This is the single most valuable
structure in the report and the one most often dropped. Two details from the
Android 13 report:

- Most `nodeInfo` elements (523,620 of 530,667) carry no path, only an `id`.
  That `id` is a tagged file's `id`, so join on it. More than half the files it
  names are nested in `<RelatedNodes>` (94,728 of 181,650), so a join against
  top-level files alone drops them. The other 7,047 carry `path`, `name`, and
  `size` inline.
- `extraInfo/@type` is also `node` (source of a tagged file) or `metaDataField`
  (source of a Device Info item, joined on the item's `id`).

Join the decoded artifact to the `uco-observable:File` for that file with
`Contained_Within`:

```json
{
  "@type": "uco-observable:ObservableRelationship",
  "uco-core:kindOfRelationship": "Contained_Within",
  "uco-core:isDirectional": { "@type": "xsd:boolean", "@value": "true" },
  "uco-core:source": { "@id": "kb:Message-bd75dc3b-..." },
  "uco-core:target": { "@id": "kb:File-msgstore-db" },
  "uco-core:description": ["extraInfo/nodeInfo joins this decoded model to its source file."]
}
```

Complete the chain by relating that file to the acquired image, also with
`Contained_Within`. A reviewer can then walk message -> `msgstore.db` -> image ->
acquisition action -> tool -> examiner without leaving the graph.

## taggedFiles

`<taggedFiles><file>` entries carry `@fs`, `@path`, `@size`, `@deleted`, and
`@embedded`, plus `<accessInfo><timestamp>` children and two metadata sections.
Map `@path` to `uco-observable:filePath`, the `File` section's `MD5` / `SHA256`
items to `uco-types:Hash` inside `uco-observable:ContentDataFacet`, and the
`accessInfo` timestamps to `uco-observable:observableCreatedTime`,
`uco-observable:modifiedTime`, and `uco-observable:accessedTime`.

Note that `@path` is the original device path while
`<metadata section="File"><item name="Local Path">` is the categorized path
inside the UFDR. The device path is the forensically meaningful one; the local
path describes the container's layout and belongs in `uco-core:description` if
you keep it at all.

### Related files and embedded files

The Android 13 report had 119,816 top-level files, plus 133,809 more nested in
`<RelatedNodes>`. The nested files appear nowhere else in the report. In all
but one case they have the same size and MD5 as their parent (the remaining one
has no MD5). Usually that's because the same file is reachable at another path
(`/data/user/0/<package>` beside `/data/data/<package>`); sometimes it is one
resource copied into several folders. Treat each one as a full entry.

72,242 files carry `embedded="true"`. They were decoded out of another file:
an APK or archive member, a Chrome cache payload, or a blob from a database
that was itself decrypted from a `.crypt14` backup. Their paths are synthetic.
They hang under the container's path, and they need not be unique: one Chrome
cache entry yields two payloads of 4,212 and 4,235 bytes, both at
`.../69948f86d014bea6_0/www.wral.com`. In that report 8,252 paths are shared by
two or more embedded files with different content, and no path is shared by two
non-embedded files.

The iOS 15 report (Physical Analyzer 7.62.0.40, same schema 7.48) agrees on
related files: there are 111,984, and all of them match their parent's size and
MD5. It adds two more reasons a path is not an identity:

- Images that UFED decoded from `ThreemaData.sqlite` have the path
  `.../ThreemaData.sqlite/`, which is the database's own path.
- Nine non-embedded paths carry different content within that one report.
  `.GlobalPreferences.plist` appears as both an 89-byte 2022 version and an
  872-byte 2023 version. Emoji file names are written lossily: UFED stores the
  first byte of the UTF-8 sequence as `ð` and the rest as `_`. As a result,
  four different JSON files inside `Zoom.app` all appear as `ð___.json`.

So key a file on its path only when the report gives that path one content.
`tagged_files_to_graph` applies the tiers from
[cross-report-file-identity.md](cross-report-file-identity.md):

- Each non-embedded file gets a shared exhibit file keyed on (exhibit, path).
- Each embedded file gets a report entry and content cores that are
  `Extracted_From` the nearest non-embedded file at or above its path.
- A path with more than one content in the report gets no shared exhibit file.
  Its entries keep the path and their content cores, and the path is added to
  the `warnings` list you pass in. Picking one of them would be a guess.
- Aliases and copies converge on one content core per (hash, size), because
  that is what they share.

```python
from case_uco import CASEGraph
from case_uco.vendors.cellebrite import UfedTaggedFile, iter_report, tagged_files_to_graph

graph = CASEGraph()
files = [i for i in iter_report("report.xml") if isinstance(i, UfedTaggedFile)]
warnings = []
tagged_files_to_graph(
    graph, files, exhibit="EXHIBIT-001", report="<report.xml SHA-256>", warnings=warnings
)
```

The whole Android 13 file tree became 1,029,013 nodes in about 100 seconds and
used about 9.5 GB of memory. The tree had 181,383 exhibit files, 18,149
containers, and 107,936 distinct contents. For reports that size, build one
graph per application or partition, as the graph-splitting constraint in the
SDK rules advises, and merge with `on_duplicate="merge_compatible"`.

## Deleted state

`<model deleted_state="Deleted">` and `<file deleted="Deleted">` mean the record
was recovered from unallocated or from a tombstoned row.

- Recovered records get `uco-observable:RecoveredObjectFacet` with
  `uco-observable:contentRecoveredStatus`. Values come from
  `RecoveredObjectStatusVocab`: `overwritten`, `partially recovered`,
  `recovered`, `unknown`.
- Intact records get no recovery facet at all. Absence is the assertion.

## Anti-patterns

- **`Attached_To` is not a relationship kind.** It appears in the community
  parser but is absent from `ObservableObjectRelationshipVocab`, so a graph using
  it fails the repository's relationship-kind lint. Use `Attachment_Of` for
  attachment -> message, or `Had_Attachment` for the reverse direction.
- **Do not write the UFED tag into the MIME type.** The upstream parser sets
  `FileFacet.mimeType` from the report's `Tags` item, so an image ends up with a
  MIME type of `Image` or `Application`. Derive the MIME type from content or
  extension, and put the UFED tag in `uco-core:tag`.
- **Do not synthesize placeholder facts.** The upstream parser substitutes
  `1900-01-01T08:00:00` for missing timestamps, `'1' * 76` for missing hashes,
  and `Uncategorized` for missing tags. Those validate and are false. Omit the
  property; if the absence itself matters, tag it `hash-status:not-published`.
- **Do not put `deleted_state` in `uco-observable:state`.** That property draws
  on `ObservableObjectStateVocab` (`Active`, `Closed`, `Exists`, `Locked`, ...),
  which has no member meaning "deleted". Use `RecoveredObjectFacet`.
- **Do not adopt the upstream `drafting:` namespace.** It resolves to
  `http://example.org/ontology/drafting/`, the shipped Turtle declares one class
  while the code emits fifteen terms, and nothing outside that repository can
  validate it. If UCO genuinely lacks a term, follow
  [change-proposal.md](change-proposal.md) and [extensions.md](extensions.md).
- **Do not treat `report.xml` as the investigation.** It is a file, wrapped in a
  provenance record, produced by an action. The investigation is the case.
- **Do not infer a SOLVE-IT technique from the product name.** "UFED" is not
  evidence that DFT-1020 was performed; the extraction log is. See
  [technique-evidence-outcome.md](technique-evidence-outcome.md).

## Checklist

1. Read the `.ufd` with `read_ufd` and review its warnings; build the
   acquisition spine with `ufd_to_graph`. Confirm no passcode reached the graph.
2. Unzip the `.ufdr` and locate `report.xml`; hash it and record the digest.
   Stream it with `iter_report` and check `report.warnings`; a `NodeCount`
   mismatch means the report is truncated.
3. Build the spine: Cellebrite `Organization`, both `Tool` nodes, examiner
   `Identity`, acquisition and decode `InvestigativeAction`s, `ProvenanceRecord`.
4. Model the device, OS, and SIM as three observables joined by
   `Contained_Within`.
5. Walk `<taggedFiles>`, including `<RelatedNodes>`, into `File` observables
   with hashes and timestamps using `tagged_files_to_graph`. It keys files as in
   [cross-report-file-identity.md](cross-report-file-identity.md), and never
   on an embedded file's synthetic path.
6. Walk `<decodedData>` model by model using the mapping table; mint each
   `Party` identifier once and reuse the node.
7. Build the `extraInfo` -> `nodeInfo` join as `Contained_Within` edges from each
   decoded artifact to its source file, joining `nodeInfo/@id` to the tagged
   file `id`.
8. Apply `RecoveredObjectFacet` wherever `deleted_state="Deleted"`.
9. Validate: `case_validate --built-version case-1.5.0 ufed-report.jsonld`, or
   `validate_graph(path)` through the MCP server for strict concept coverage.

## Validated exemplar

`examples/vendor-exports/build_cellebrite_ufed_xml.py` builds
`examples/vendor-exports/cellebrite-ufed-xml.jsonld`: 33 nodes covering the tool
spine, device/OS/SIM, a tagged file, a chat with an intact and a deleted message,
a call, a contact, a location, a wireless network, URL history, and the
`extraInfo` chain of evidence. It conforms against CASE 1.4.0 with zero
violations and zero undeclared concepts. Field values are synthetic, but every
element and attribute name in this recipe is from a real `report.xml`, and every
hash in the exemplar is computed over bytes the builder defines rather than
invented. Real UFED output for test devices is published in the [Digital
Corpora mobile
datasets](https://digitalcorpora.s3.amazonaws.com/s3_browser.html#corpora/mobile/).
The `.ufd`/`.ufdx` reader is tested against summaries from there. The
`report.xml` reader is tested against a trimmed copy of the Android 13
Cellebrite Reader report
(`python/tests/fixtures/cellebrite/android13_pa_7.58_report_trimmed.xml`). The
trim keeps an alias pair, the Chrome cache container with its two
same-path payloads, and four decoded models with their `extraInfo` links. A
second trim, from the iOS 15 report, keeps the two `.GlobalPreferences.plist`
versions, the four `ð___.json` files, and `ThreemaData.sqlite` with its two
images. That report's passcode items are removed from the trim.

```bash
python3 examples/vendor-exports/build_cellebrite_ufed_xml.py
case_validate --built-version case-1.5.0 examples/vendor-exports/cellebrite-ufed-xml.jsonld
```

## Related

- [magnet-axiom-export.md](magnet-axiom-export.md) — the same spine for AXIOM's `Artifact`/`Hit`/`Fragment` export
- [msab-xry-export.md](msab-xry-export.md) — MSAB XRY, where the export schema is not public
- [cross-report-file-identity.md](cross-report-file-identity.md) — one file across UFED, XRY, AXIOM, and re-run reports
- [starter-mobile-extraction.md](starter-mobile-extraction.md) — the vendor-neutral starting point
- [mobile-device-sim.md](mobile-device-sim.md) — handset and SIM modeling in depth
- [threaded-messaging.md](threaded-messaging.md) — ordered chat threads from `<modelType type="Chat">`
- [call-log.md](call-log.md) — call records and carrier accounts
- [cell-site.md](cell-site.md) — `CellTower` models and CDR correlation
- [chain-of-custody.md](chain-of-custody.md) — provenance records and exhibit numbering
- [technique-evidence-outcome.md](technique-evidence-outcome.md) — sourcing an examiner technique instead of guessing it
