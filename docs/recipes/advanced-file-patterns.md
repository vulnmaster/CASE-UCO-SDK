# Advanced File Patterns

> See [Recipe Index](INDEX.md) for all recipes.

Model complex file containment chains — archives, encrypted streams, encoded data, SQLite blobs, and nested containment with byte-level precision. Based on [CASE-Examples/file](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/file).

This extends the basic [file-system recipe](file-system.md) with layered extraction patterns.

## Key classes

| Class | Role |
|---|---|
| `File` + `FileFacet` | A file on disk |
| `ContentData` + `ContentDataFacet` | A block of data (may not be a file) |
| `Image` + `ImageFacet` | A disk image |
| `Relationship` | Containment and derivation links between layers |
| `DataRangeFacet` | Byte offset and size within a container |
| `EncodedStreamFacet` | Encoding method (e.g., BASE64) |
| `EncryptedStreamFacet` | Encryption method, mode, key, IV |
| `SQLiteBlobFacet` | A blob extracted from a SQLite database |
| `PathRelationFacet` | File path within a container (e.g., path inside a TAR) |

## Containment chain pattern

Forensic extraction often involves nested layers. Each layer is an `ObservableObject` linked to its container via a `Relationship`:

```
File (disk image)
    ▲ Contained_Within (DataRangeFacet: offset, size)
    │
ContentData (encrypted partition)
    ▲ Decrypted_From (EncryptedStreamFacet: AES-256-CBC)
    │
ContentData (decrypted volume)
    ▲ Contained_Within (PathRelationFacet: path in archive)
    │
File (TAR entry)
    ▲ Decoded_From (EncodedStreamFacet: BASE64)
    │
ContentData (decoded content)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, File,
    FileFacet, ContentDataFacet, ImageFacet,
    DataRangeFacet, PathRelationFacet,
    EncodedStreamFacet, EncryptedStreamFacet, SQLiteBlobFacet,
)
from case_uco.uco.types import Hash

graph = CASEGraph()

# Disk image (outermost container)
disk_image = graph.create(File,
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ImageFacet(image_type="..."),  # e.g. "E01", "dd"
    ],
)

# Data at a specific byte range within the image
inner_data = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(
        hash=[Hash(hash_method=["SHA256"], hash_value="...")],
        size_in_bytes=...,
    )],
)

# Containment with byte offset
contained_in_image = graph.create(Relationship,
    source=[inner_data], target=disk_image,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[DataRangeFacet(
        range_offset=...,  # byte offset from source
        range_size=...,    # size in bytes from source
    )],
)

# Encrypted stream that was decrypted
decrypted_data = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(size_in_bytes=...)],
)
graph.create(Relationship,
    source=[decrypted_data], target=inner_data,
    kind_of_relationship="Decrypted_From",
    is_directional=True,
    has_facet=[EncryptedStreamFacet(
        encryption_method="...",  # e.g. "AES" from source
        encryption_mode="...",    # e.g. "CBC" from source
    )],
)

# File inside an archive (TAR, ZIP) with path context
archive_entry = graph.create(File,
    has_facet=[FileFacet(file_name="...", size_in_bytes=...)],
)
graph.create(Relationship,
    source=[archive_entry], target=decrypted_data,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[PathRelationFacet(path=["..."])],  # path inside archive
)

# BASE64-encoded content that was decoded
decoded = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(size_in_bytes=...)],
)
graph.create(Relationship,
    source=[decoded], target=archive_entry,
    kind_of_relationship="Decoded_From",
    is_directional=True,
    has_facet=[EncodedStreamFacet(encoding_method="...")],  # e.g. "BASE64"
)

# SQLite blob extraction
blob = graph.create(ObservableObject,
    has_facet=[
        ContentDataFacet(size_in_bytes=...),
        SQLiteBlobFacet(
            table_name="...",    # from source
            column_name="...",   # from source
            row_index=[...],     # from source
        ),
    ],
)
graph.create(Relationship,
    source=[blob], target=archive_entry,
    kind_of_relationship="Contained_Within",
    is_directional=True,
)

graph.write("advanced_file_patterns.jsonld")
```

</details>

## Notes

- `DataRangeFacet` fields: `range_offset` (int), `range_size` (int), `range_offset_type` (str, e.g., "byte").
- `PathRelationFacet.path` is `list[str]` — the path within the container.
- `EncryptedStreamFacet` fields: `encryption_method`, `encryption_mode` (both `Optional[str]`), `encryption_key`, `encryption_iv` (both `list[str]`).
- `EncodedStreamFacet` has `encoding_method: Optional[str]`.
- Common `kind_of_relationship` values for file chains: `"Contained_Within"`, `"Decoded_From"`, `"Decrypted_From"`, `"Decompressed_From"`.
- Facets go on the `Relationship` itself (via `has_facet`) when they describe the relationship (e.g., byte offset), not the objects.
