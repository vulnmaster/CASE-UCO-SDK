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

Use a different recipe when:

- The extraction came from Magnet AXIOM — see
  [magnet-axiom-export.md](magnet-axiom-export.md).
- The extraction came from MSAB XRY — see [msab-xry-export.md](msab-xry-export.md).
- You only have a generic device summary with no vendor structure — start from
  [starter-mobile-extraction.md](starter-mobile-extraction.md).

## Source input shape

```xml
<project id="..." name="..." extractionType="Physical">
  <metadata section="Extraction Data">
    <item name="DeviceInfoExtractionStartDateTime">...</item>
  </metadata>
  <metadata section="Device Info">
    <item name="DeviceInfoDetectedPhoneModel">Pixel 3</item>
    <item name="IMEI">356938035643809</item>
  </metadata>
  <metadata section="Additional Fields">
    <item name="UFED_PA_Version">7.60.0.114</item>
  </metadata>
  <caseInformation><field fieldType="ExaminerName">...</field></caseInformation>
  <images><image path="..." size="..."><metadata section="Hashes"/></image></images>
  <taggedFiles><file fs="..." path="..." size="..." deleted="Intact"/></taggedFiles>
  <decodedData>
    <modelType type="Chat">
      <model type="Chat" id="..." deleted_state="Intact">
        <multiModelField name="Participants">
          <model type="Party"><field name="Identifier"/><field name="IsPhoneOwner"/></model>
        </multiModelField>
        <multiModelField name="Messages">
          <model type="InstantMessage"><field name="Body"/><field name="TimeStamp"/></model>
        </multiModelField>
      </model>
    </modelType>
  </decodedData>
  <extraInfo id="..."><nodeInfo id="..." path="..." tableName="..." offset="..."/></extraInfo>
</project>
```

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

`<extraInfo id="...">` matches a decoded `<model id="...">`, and its `nodeInfo`
children give the on-device path, table name, and byte offset the artifact was
decoded from. This is the single most valuable structure in the report and the
one most often dropped. Join the decoded artifact to a `uco-observable:File` for
that path with `Contained_Within`:

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

1. Unzip the `.ufdr` and locate `report.xml`; hash it and record the digest.
2. Build the spine: Cellebrite `Organization`, both `Tool` nodes, examiner
   `Identity`, acquisition and decode `InvestigativeAction`s, `ProvenanceRecord`.
3. Model the device, OS, and SIM as three observables joined by
   `Contained_Within`.
4. Walk `<taggedFiles>` into `File` observables with hashes and timestamps.
5. Walk `<decodedData>` model by model using the mapping table; mint each
   `Party` identifier once and reuse the node.
6. Build the `extraInfo` -> `nodeInfo` join as `Contained_Within` edges from each
   decoded artifact to its source file.
7. Apply `RecoveredObjectFacet` wherever `deleted_state="Deleted"`.
8. Validate: `case_validate --built-version case-1.4.0 ufed-report.jsonld`, or
   `validate_graph(path)` through the MCP server for strict concept coverage.

## Validated exemplar

`examples/vendor-exports/build_cellebrite_ufed_xml.py` builds
`examples/vendor-exports/cellebrite-ufed-xml.jsonld`: 33 nodes covering the tool
spine, device/OS/SIM, a tagged file, a chat with an intact and a deleted message,
a call, a contact, a location, a wireless network, URL history, and the
`extraInfo` chain of evidence. It conforms against CASE 1.4.0 with zero
violations and zero undeclared concepts. Field values are synthetic — no licensed
Cellebrite output is redistributable — but every element and attribute name in
this recipe is from a real `report.xml`, and every hash in the exemplar is
computed over bytes the builder defines rather than invented.

```bash
python3 examples/vendor-exports/build_cellebrite_ufed_xml.py
case_validate --built-version case-1.4.0 examples/vendor-exports/cellebrite-ufed-xml.jsonld
```

## Related

- [magnet-axiom-export.md](magnet-axiom-export.md) — the same spine for AXIOM's `Artifact`/`Hit`/`Fragment` export
- [msab-xry-export.md](msab-xry-export.md) — MSAB XRY, where the export schema is not public
- [starter-mobile-extraction.md](starter-mobile-extraction.md) — the vendor-neutral starting point
- [mobile-device-sim.md](mobile-device-sim.md) — handset and SIM modeling in depth
- [threaded-messaging.md](threaded-messaging.md) — ordered chat threads from `<modelType type="Chat">`
- [call-log.md](call-log.md) — call records and carrier accounts
- [cell-site.md](cell-site.md) — `CellTower` models and CDR correlation
- [chain-of-custody.md](chain-of-custody.md) — provenance records and exhibit numbering
- [technique-evidence-outcome.md](technique-evidence-outcome.md) — sourcing an examiner technique instead of guessing it
