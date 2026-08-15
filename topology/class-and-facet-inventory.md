# Class and Facet inventory

Source of truth: `python/case_uco/_registry.json` (plus the extension registries
listed in the JSON). Counts include T-Box-only CAC classes that have no
dedicated SHACL shape — they are still registered so discovery works.

## Totals

| | Count |
|---|---:|
| Modules | 78 |
| Classes | 2804 |
| Facets | 154 |
| Vocabularies | 54 |

## By family

| Family | Modules | Classes | Facets |
|---|---:|---:|---:|
| aeo | 3 | 26 | 0 |
| cac | 47 | 1992 | 0 |
| case | 1 | 10 | 0 |
| sdk-extension | 8 | 62 | 4 |
| solveit | 6 | 296 | 0 |
| uco | 13 | 418 | 150 |

## Largest modules

| Module | Family | Classes | Facets |
|---|---|---:|---:|
| `uco.observable` | uco | 323 | 122 |
| `ext.solveit.solveit-data` | solveit | 187 | 0 |
| `ext.solveit.solveit-observable` | solveit | 88 | 0 |
| `ext.cac.cacontology-prevention` | cac | 87 | 0 |
| `ext.cac.cacontology-multi-jurisdiction` | cac | 81 | 0 |
| `ext.cac.cacontology-legal-harmonization` | cac | 78 | 0 |
| `ext.cac.cacontology-grooming` | cac | 77 | 0 |
| `ext.cac.cacontology-taskforce` | cac | 69 | 0 |
| `ext.cac.cacontology-victim-impact` | cac | 67 | 0 |
| `ext.cac.cacontology-stranger-abduction` | cac | 64 | 0 |
| `ext.cac.cacontology-sex-offender-registry` | cac | 62 | 0 |
| `ext.cac.cacontology-legal-outcomes` | cac | 61 | 0 |
| `ext.cac.cacontology-street-recruitment` | cac | 61 | 0 |
| `ext.cac.cacontology-platforms` | cac | 59 | 0 |
| `ext.cac.cacontology-undercover` | cac | 58 | 0 |
| `ext.cac.cacontology-international` | cac | 53 | 0 |
| `ext.cac.cacontology-case-management` | cac | 51 | 0 |
| `ext.cac.cacontology-sextortion` | cac | 51 | 0 |
| `ext.cac.cacontology-athletic-exploitation` | cac | 50 | 0 |
| `ext.cac.cacontology-forensics` | cac | 48 | 0 |
| `ext.cac.cacontology-extremist-enterprises` | cac | 47 | 0 |
| `ext.cac.cacontology-institutional-exploitation` | cac | 45 | 0 |
| `ext.cac.cacontology-investigation-coordination` | cac | 44 | 0 |
| `ext.cac.cacontology-physical-evidence` | cac | 44 | 0 |
| `ext.cac.cacontology-specialized-units` | cac | 43 | 0 |

## Recommended Facet sets (from recipes + mapping guide)

These are the Facet bundles investigators and agents should attach to the
named host type. They are **recommendations**, not SHACL requirements —
UCO's Facet pattern is deliberately open — but omitting them is the most
common modeling error in CAC and forensic graphs.

- **Account**: `AccountFacet`, `DigitalAccountFacet`
- **AppleUnifiedLogArchive**: `ApplicationFacet`, `DeviceFacet`, `EventRecordFacet`, `FileFacet`, `SoftwareFacet`
- **ApplicationAccount**: `AccountFacet`, `ApplicationAccountFacet`, `ApplicationFacet`, `IPv4AddressFacet`, `MessageFacet`, `MessageThreadFacet`
- **Device**: `ApplicationFacet`, `DeviceFacet`, `FileFacet`, `MobileDeviceFacet`, `OperatingSystemFacet`, `SIMCardFacet`
- **Directory**: `ContentDataFacet`, `EventRecordFacet`, `FileFacet`, `FileSystemFacet`, `WindowsVolumeFacet`
- **Disk**: `ContentDataFacet`, `DataRangeFacet`, `DiskPartitionFacet`, `EncryptedStreamFacet`, `FileFacet`, `ImageFacet`
- **DiskImage**: `ImageFacet`, `FileFacet`, `ContentDataFacet`
- **EmailMessage**: `ContentDataFacet`, `DeviceFacet`, `EmailAddressFacet`, `EmailMessageFacet`, `FileFacet`, `URLFacet`
- **EventRecord**: `AccountFacet`, `ApplicationAccountFacet`, `ApplicationFacet`, `DeviceFacet`, `EventRecordFacet`, `FileFacet`
- **File**: `ContentDataFacet`, `DataRangeFacet`, `DeviceFacet`, `FileFacet`
- **Message**: `MessageFacet`, `ApplicationFacet`
- **MessageThread**: `AccountFacet`, `ApplicationAccountFacet`, `ApplicationFacet`, `MessageFacet`, `MessageThreadFacet`, `SimpleAddressFacet`
- **MobileDevice**: `DeviceFacet`, `MobileDeviceFacet`, `OperatingSystemFacet`, `SIMCardFacet`
- **NetworkConnection**: `NetworkConnectionFacet`, `IPAddressFacet`
- **ObservableObject**: `ApplicationFacet`, `ContentDataFacet`, `EmailAddressFacet`, `FileFacet`
- **RasterPicture**: `ArtifactClassificationResultFacet`, `ContentDataFacet`, `EXIFFacet`, `FileFacet`, `IPv4AddressFacet`, `RasterPictureFacet`

The JSON companion lists every class and Facet per module.
