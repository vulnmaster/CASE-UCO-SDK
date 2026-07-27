# Windows USN Journal

> See [Recipe Index](INDEX.md) for all recipes.

Model entries from the Windows NTFS Update Sequence Number (USN) Change Journal — a system-maintained log of file-level operations (create, modify, rename, delete) on an NTFS volume. Each USN record carries one or more reason flags that describe what happened, making this a rich source for timeline analysis and incident response.

## Key classes

| Class | Role |
|---|---|
| `ObservableObject` + `EventRecordFacet` | Each USN record as a raw artifact from the journal |
| `Event` | The change event itself, with structured reason flags in `eventType` |
| `ObservableObject` + `FileFacet` + `NTFSFileFacet` | The file that was changed (with MFT entry ID) |
| `ObservableObject` + `FileFacet` (directory) | Directory nodes for nested containment |
| `ObservableObject` + `WindowsVolumeFacet` + `FileSystemFacet` | The NTFS volume |
| `ObservableRelationship` | Links: containment, rename before/after |
| `Dictionary` + `DictionaryEntry` | Structured USN metadata (USN number, MFT entry, reason flags) |
| `Investigation` + `InvestigativeAction` + `Tool` | Forensic provenance for the extraction |

## Pattern

```
Investigation
    └── object ──▶ InvestigativeAction ("Parse USN Journal")
                       ├── instrument ──▶ Tool (MFTECmd)
                       ├── object ──▶ disk_image (ObservableObject + ContentDataFacet)
                       └── result ──▶ $UsnJrnl:$J
                                  ──▶ USN Record (per entry)
                                  ──▶ Event (per entry)

Volume (ObservableObject + WindowsVolumeFacet + FileSystemFacet)
    ├── Users ──▶ analyst ──▶ Documents ──▶ report.docx
    │                     ──▶ Downloads ──▶ malware.exe
    ├── ProgramData ──▶ AppConfig ──▶ config.ini
    ├── Logs ──▶ system.log
    └── $Extend ──▶ $UsnJrnl:$J
                       └── USN Record (ObservableObject + EventRecordFacet)

Event (per USN entry)
    ├── startTime = [timestamp]
    ├── eventType = ["USN_REASON_FILE_CREATE", "USN_REASON_CLOSE"]
    ├── eventContext ──▶ file (the changed file)
    │                ──▶ record (the raw USN record)
    └── eventAttribute ──▶ Dictionary
                              └── DictionaryEntry(key="USN_REASON_FILE_CREATE", value="true")
                              └── DictionaryEntry(key="USN_REASON_CLOSE", value="true")
                              └── DictionaryEntry(key="USN_NUMBER", value="109248")
                              └── DictionaryEntry(key="MFT_ENTRY_ID", value="48291")

Rename modeling (when applicable):
    old_file (ObservableObject, prior state) ◀── Renamed_From ── new_file
```

<details open><summary>Python</summary>

```python
from datetime import datetime, timezone, timedelta
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.tool import Tool
from case_uco.uco.core import Event
from case_uco.uco.observable import (
    ObservableObject, ObservableRelationship,
    FileFacet, FileSystemFacet, NTFSFileFacet,
    WindowsVolumeFacet, ContentDataFacet, EventRecordFacet,
)
from case_uco.uco.types import Dictionary, DictionaryEntry, Hash

graph = CASEGraph()
tz = timezone(timedelta(hours=...))  # from source

# --- Evidence source and tool (created early for references) ---
disk_image = graph.create(ObservableObject,
    name="...",
    has_facet=[
        FileFacet(file_name=["..."], file_path=["..."], size_in_bytes=...),
        ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="...")]),
    ],
)

tool = graph.create(Tool,
    name="MFTECmd",  # from source
    version="1.3.2.1",
    tool_type="USN Journal Parser",
)

# --- NTFS Volume ---
volume = graph.create(ObservableObject,
    name="C: Volume",
    has_facet=[
        WindowsVolumeFacet(drive_letter="C:"),
        FileSystemFacet(file_system_type="NTFS", cluster_size=4096),
    ],
)

# --- Full directory hierarchy ---
dir_users = graph.create(ObservableObject, name="Users",
    has_facet=[FileFacet(file_name=["Users"], file_path=["C:\\Users"],
                         is_directory=[True])])
graph.create(ObservableRelationship, is_directional=True,
    kind_of_relationship="Contained_Within",
    source=[dir_users], target=volume)

dir_analyst = graph.create(ObservableObject, name="analyst",
    has_facet=[FileFacet(file_name=["analyst"],
        file_path=["C:\\Users\\analyst"], is_directory=[True])])
graph.create(ObservableRelationship, is_directional=True,
    kind_of_relationship="Contained_Within",
    source=[dir_analyst], target=dir_users)

dir_documents = graph.create(ObservableObject, name="Documents",
    has_facet=[FileFacet(file_name=["Documents"],
        file_path=["C:\\Users\\analyst\\Documents"], is_directory=[True])])
graph.create(ObservableRelationship, is_directional=True,
    kind_of_relationship="Contained_Within",
    source=[dir_documents], target=dir_analyst)

# --- USN Journal ($UsnJrnl:$J) ---
usn_journal = graph.create(ObservableObject,
    name="$UsnJrnl:$J",
    has_facet=[FileFacet(
        file_name=["$UsnJrnl:$J"],
        file_path=["C:\\$Extend\\$UsnJrnl:$J"],
    )],
)

# --- Per-entry: file + record + event ---
parsed_results = []  # collect for InvestigativeAction.result

file_obj = graph.create(ObservableObject,
    name="report.docx",  # from source
    has_facet=[
        FileFacet(file_name=["report.docx"],
                  file_path=["C:\\Users\\analyst\\Documents\\report.docx"]),
        NTFSFileFacet(entry_id=48291),  # MFT entry number from source
    ],
)
graph.create(ObservableRelationship,
    is_directional=True,
    kind_of_relationship="Contained_Within",
    source=[file_obj], target=dir_documents,
)

record = graph.create(ObservableObject,
    name="USN Record 109248",
    has_facet=[EventRecordFacet(
        event_record_id="109248",  # USN number from source
        event_type="USN_CHANGE_JOURNAL",
        observable_created_time=datetime(..., tzinfo=tz),
        event_record_text="File report.docx was created and handle closed",
        event_record_service_name="NTFS USN Journal",
        event_record_device=volume,
    )],
)
graph.create(ObservableRelationship,
    is_directional=True,
    kind_of_relationship="Contained_Within",
    source=[record], target=usn_journal,
)

reason_flags = ["USN_REASON_FILE_CREATE", "USN_REASON_CLOSE"]  # from source
event = graph.create(Event,
    name="USN Change 109248: report.docx",
    start_time=[datetime(..., tzinfo=tz)],
    event_type=reason_flags,
    event_context=[file_obj, record],
    event_attribute=[Dictionary(entry=[
        DictionaryEntry(key=flag, value="true") for flag in reason_flags
    ] + [
        DictionaryEntry(key="USN_NUMBER", value="109248"),
        DictionaryEntry(key="MFT_ENTRY_ID", value="48291"),
    ])],
)
parsed_results.extend([record, event])

# --- Rename: model both old and new file states ---
new_file = graph.create(ObservableObject,
    name="system.log",
    has_facet=[
        FileFacet(file_name=["system.log"], file_path=["C:\\Logs\\system.log"]),
        NTFSFileFacet(entry_id=33107),
    ],
)
old_file = graph.create(ObservableObject,
    name="temp.log (prior state)",
    has_facet=[
        FileFacet(file_name=["temp.log"], file_path=["C:\\Logs\\temp.log"]),
        NTFSFileFacet(entry_id=33107),  # same MFT entry
    ],
)
graph.create(ObservableRelationship,
    is_directional=True,
    kind_of_relationship="Renamed_From",
    source=[new_file], target=old_file,
)
# ... then create the Event with both files in eventContext

# --- Provenance (created last so result list is complete) ---
extraction = graph.create(InvestigativeAction,
    name="Parse USN Journal from ...",
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    instrument=[tool],
    object=[disk_image],
    result=[usn_journal] + parsed_results,
)

graph.create(Investigation,
    name="...",
    focus=["File system activity analysis"],
    investigation_form=["incident"],
    start_time=datetime(..., tzinfo=tz),
    object=[extraction],
)

graph.write("usn_journal.jsonld")
```

</details>

## Modeling decisions

### Structured reason flags, not free text

USN reason flags are the core forensic value of the journal. They are modeled in two complementary ways:

1. **`Event.eventType`** — a `list[str]` with each flag as a separate value. This makes SPARQL queries like "find all delete events" trivial:
   ```sparql
   SELECT ?event WHERE {
     ?event uco-core:eventType "USN_REASON_FILE_DELETE" .
   }
   ```

2. **`Dictionary` entries** — each flag as a unique key with value `"true"`, alongside numeric metadata (`USN_NUMBER`, `MFT_ENTRY_ID`). This avoids the SHACL key-uniqueness warning that occurs when using the same key for multiple values.

### Two-layer event model

Each USN entry produces two linked objects:

- An **`ObservableObject` + `EventRecordFacet`** — the raw USN record as a forensic artifact (with its USN number, timestamp, source device).
- A **`core:Event`** — the semantic change event with structured flags, linked to both the record and the affected file via `eventContext`.

This separates "what the artifact says" from "what happened," which supports both artifact-centric and event-centric queries.

### Rename before/after

Rename operations create two `ObservableObject` nodes sharing the same MFT entry ID but with different file names/paths. An `ObservableRelationship` with `kindOfRelationship="Renamed_From"` links new → old. Both file objects appear in the `Event.eventContext`, making the structural relationship queryable rather than trapped in free text.

### Directory hierarchy

Model the full directory path, not just the leaf directory. For `C:\Users\analyst\Documents\report.docx`, create separate directory objects for `Users`, `analyst`, and `Documents`, each `Contained_Within` its parent. This preserves the actual file system structure and avoids flattening paths like `C:\Users\analyst\Documents` directly under `C:`.

### Forensic provenance

The graph records how the USN data was obtained. Create the `InvestigativeAction` and `Investigation` **after** all USN entries so the `result` list is fully populated at creation time (the SDK serializes objects at `create()` time):

- **`Investigation`** — the case context, with `object=[extraction_action]` linking to the action
- **`InvestigativeAction`** — the parsing step, with `instrument=[tool]`, `object=[disk_image]`, and `result=[usn_journal] + all_records_and_events`
- **`Tool`** — the parser used (e.g., MFTECmd)
- **Evidence source** — the disk image as an `ObservableObject` with hash

This creates an explicit provenance chain: `Investigation` → `InvestigativeAction` → (`$UsnJrnl:$J` + all USN records + all Event objects), traceable back through the tool and evidence source.

## Common USN reason flags

| Flag | Meaning |
|---|---|
| `USN_REASON_DATA_OVERWRITE` | Data in the file was overwritten |
| `USN_REASON_DATA_EXTEND` | Data was appended to the file |
| `USN_REASON_DATA_TRUNCATION` | Data was removed from the end of the file |
| `USN_REASON_FILE_CREATE` | A new file was created |
| `USN_REASON_FILE_DELETE` | A file was deleted |
| `USN_REASON_RENAME_OLD_NAME` | The old name of a renamed file |
| `USN_REASON_RENAME_NEW_NAME` | The new name of a renamed file |
| `USN_REASON_SECURITY_CHANGE` | File permissions or ACLs were changed |
| `USN_REASON_BASIC_INFO_CHANGE` | File attributes or timestamps were changed |
| `USN_REASON_HARD_LINK_CHANGE` | A hard link was created or deleted |
| `USN_REASON_CLOSE` | The file handle was closed |

## Notes

- `Event.eventType` is `list[str]` — use one string per reason flag for queryability.
- Dictionary keys must be unique within a single Dictionary (SHACL validation enforces this). Use each flag name as a key rather than a repeated `USN_REASON_FLAG` key.
- `EventRecordFacet.eventRecordDevice` should reference the volume `ObservableObject`, not the disk image — the USN Journal is per-volume.
- The same MFT entry ID on two file objects (old name, new name) signals that they are the same underlying NTFS file record at different points in time.
- For high-volume USN data, partition by volume or time window rather than splitting mid-stream — USN records within a volume form a sequential log where cross-references (parent file reference numbers) need to resolve.
- See also: [Events and Authentication Logs](event.md) for the general Event/Dictionary pattern, [File System Forensics](file-system.md) for directory hierarchy patterns, and [Apple Unified Logs](apple-unified-logs.md) for the analogous OS log EventRecord recipe on Apple platforms.

## Known limitations

### Relationship labels are free strings

`kindOfRelationship` is typed as `xsd:string` in UCO — there is no controlled vocabulary for relationship types. Labels like `Contained_Within`, `Records_Change_To`, and `Renamed_From` are readable conventions (and `Contained_Within` appears in [CASE-Examples](https://github.com/casework/CASE-Examples)), but they are not ontology-grounded terms. If interoperability across tools matters, coordinate on a shared vocabulary or propose new relationship types via a [change proposal](change-proposal.md).

### Dictionary values are strings

UCO `DictionaryEntry.value` is `xsd:string`, so there is no mechanism for strongly typed values (booleans, integers) inside Dictionary entries. The reason flags are `"true"` as strings, and the USN number is `"109248"` as a string. The primary structured mechanism for querying is `Event.eventType` (a native `list[str]`), not the Dictionary.

### File identity vs. temporal state

This recipe models files as continuing objects — `malware.exe` exists as an `ObservableObject` even after a delete event records its removal. This is standard CASE/UCO practice and works for most forensic workflows, but does not distinguish "the file as a concept" from "the file's state at a specific moment." For workflows requiring explicit temporal state snapshots or validity intervals, see the [Existence Intervals and Temporal Modeling](existence-intervals.md) recipe.
