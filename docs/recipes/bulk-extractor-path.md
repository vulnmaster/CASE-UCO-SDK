# Bulk Extractor Forensic Paths

> See [Recipe Index](INDEX.md) for all recipes.

Model nested containment paths from bulk extraction tools — artifacts found within compressed streams, inside disk images, at specific byte offsets. Based on [CASE-Examples/bulk_extractor_forensic_path](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/bulk_extractor_forensic_path).

## Key classes

| Class | Role |
|---|---|
| `EmailAddress` + `EmailAddressFacet` | An extracted artifact (email, URL, etc.) |
| `ContentData` + `ContentDataFacet` | Data blocks at each nesting layer |
| `File` / `Image` | The outermost disk image |
| `Relationship` | Layered containment: `Contained_Within`, `Decompressed_From` |
| `DataRangeFacet` | Byte offset and size within a container |
| `CompressedStreamFacet` | Compression method for compressed layers |

## Pattern

Bulk extractors find artifacts buried inside nested containers. The forensic path traces from the artifact back to its source on disk:

```
EmailAddress (extracted artifact)
    │
    └── Contained_Within ──▶ ContentData (decompressed block)
                                  │
                                  └── Decompressed_From ──▶ ContentData (gzip stream)
                                                                  │  CompressedStreamFacet
                                                                  │
                                                                  └── Contained_Within ──▶ File (disk image)
                                                                           DataRangeFacet (offset, size)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, File,
    FileFacet, ContentDataFacet,
    EmailAddressFacet, DataRangeFacet,
    CompressedStreamFacet, ImageFacet,
)
from case_uco.uco.types import Hash

graph = CASEGraph()

# Outermost container: disk image
disk_image = graph.create(File,
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ImageFacet(image_type="..."),  # e.g. "dd", "E01"
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"], hash_value="...",
        )]),
    ],
)

# Compressed stream at a byte range within the image
compressed_stream = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(size_in_bytes=...)],
)
graph.create(Relationship,
    source=[compressed_stream], target=disk_image,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[DataRangeFacet(
        range_offset=...,  # byte offset from source
        range_size=...,    # from source
    )],
)

# Decompressed content
decompressed = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(size_in_bytes=...)],
)
graph.create(Relationship,
    source=[decompressed], target=compressed_stream,
    kind_of_relationship="Decompressed_From",
    is_directional=True,
    has_facet=[CompressedStreamFacet(
        compression_method="...",  # e.g. "gzip" from source
    )],
)

# The extracted artifact (e.g., an email address)
artifact = graph.create(ObservableObject,
    has_facet=[EmailAddressFacet(
        address_value="...",  # from source
    )],
)
graph.create(Relationship,
    source=[artifact], target=decompressed,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[DataRangeFacet(
        range_offset=...,  # offset within decompressed content
        range_size=...,
    )],
)

graph.write("bulk_extractor_path.jsonld")
```

</details>

## Notes

- Each layer in the forensic path is a separate `ObservableObject` linked by a `Relationship`.
- `DataRangeFacet` goes on the `Relationship` (via `has_facet`), not on the contained object.
- `CompressedStreamFacet` has `compression_method: Optional[str]` and `compression_ratio: Optional[float]`.
- Common `kind_of_relationship` values: `"Contained_Within"`, `"Decompressed_From"`, `"Decoded_From"`, `"Decrypted_From"`.
- This pattern applies to any bulk extraction tool (bulk_extractor, binwalk, foremost) that reports forensic paths.
- For additional nesting levels, add more intermediate `ContentData` objects in the chain.
