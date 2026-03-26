# Database Record Extraction

> See [Recipe Index](INDEX.md) for all recipes.

Model artifacts extracted from SQLite or other databases on a device — individual records, the database files themselves, and the containment relationships between them.

## Key classes

| Class | Role |
|---|---|
| `File` + `FileFacet` | The database file (e.g., `msgstore.db`) |
| `TableField` + `TableFieldFacet` | A single record/cell from a database table |
| `Message` + `MessageFacet` | A message reconstructed from database records |
| `ObservableRelationship` | Links records to their source DB (`Contained_Within`, `Derived_From`) |

## Pattern

Database forensics typically involves three layers: the database file, the individual records within it, and higher-level artifacts (messages, contacts, etc.) derived from those records.

```
File + FileFacet (msgstore.db)
    ▲
    │ Contained_Within
    │
TableField + TableFieldFacet (row/column value)
    ▲
    │ Derived_From
    │
Message + MessageFacet (reconstructed message)
```

Also model sidecar files (WAL, journal) as separate `File` objects linked to the main DB via `Related_To`.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, File, Message, TableField,
    FileFacet, MessageFacet, TableFieldFacet,
)
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# The database file
db_file = graph.create(File,
    has_facet=[FileFacet(
        file_name="...",   # e.g. "msgstore.db" — from source
        file_path="...",   # full path from source
        size_in_bytes=...,
    )],
)

# Journal/WAL sidecar file (if present in source)
wal_file = graph.create(File,
    has_facet=[FileFacet(
        file_name="...",  # e.g. "msgstore.db-wal"
        file_path="...",
        size_in_bytes=...,
    )],
)

# Link WAL to main DB
graph.create(Relationship,
    source=[wal_file], target=db_file,
    kind_of_relationship="Related_To",
    is_directional=True,
)

# A database record (row/column value)
db_record = graph.create(TableField,
    has_facet=[TableFieldFacet(
        table_name="...",          # from source
        record_row_id="...",       # row ID from source
        record_field_name="...",   # column name from source
        record_field_value="...",  # cell value from source
    )],
)

# Link record to its source database
graph.create(Relationship,
    source=[db_record], target=db_file,
    kind_of_relationship="Contained_Within",
    is_directional=True,
)

# A message reconstructed from the database record
msg = graph.create(Message,
    has_facet=[MessageFacet(
        message_text="...",  # from source
        sent_time=datetime(..., tzinfo=tz),
    )],
)

# Link message to the database record it was derived from
graph.create(Relationship,
    source=[msg], target=db_record,
    kind_of_relationship="Derived_From",
    is_directional=True,
)

graph.write("database_records.jsonld")
```

</details>

## Notes

- `TableFieldFacet` represents a single cell: `table_name` + `record_row_id` + `record_field_name` + `record_field_value`. Create one `TableField` per extracted record.
- Use `Relationship` with `kind_of_relationship` values: `"Contained_Within"` (record inside DB file), `"Derived_From"` (message derived from record), `"Related_To"` (WAL/journal related to main DB).
- For bulk extraction, create multiple `TableField` objects in a loop — one per row or per significant field.
- The database file itself should be linked to its source device/partition via another `Contained_Within` relationship if that context is available.
