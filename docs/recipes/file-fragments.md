# File Fragments and Multipart Files

> See [Recipe Index](INDEX.md) for all recipes.

Model files split across multiple fragments, embedded data (thumbnails inside images), and reassembly relationships. Based on [CASE-Examples/multipart_file](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/multipart_file) and [CASE-Examples/raw_data](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/raw_data).

## Key classes

| Class | Role |
|---|---|
| `ContentData` + `ContentDataFacet` | The logical whole content |
| `File` + `FileFacet` | Individual fragment files |
| `FragmentFacet` | Fragment index and total count |
| `DataRangeFacet` | Byte offset/size for embedded data |
| `Relationship` | `Has_Fragment`, `Contained_Within` links |

## Two patterns

**Split file fragments** (e.g., a file split across disk sectors):

```
ContentData (logical whole)
    │
    ├── Has_Fragment ──▶ File (fragment 1) + FragmentFacet (index=0, total=3)
    ├── Has_Fragment ──▶ File (fragment 2) + FragmentFacet (index=1, total=3)
    └── Has_Fragment ──▶ File (fragment 3) + FragmentFacet (index=2, total=3)
```

**Embedded data** (e.g., thumbnail inside a JPEG):

```
RasterPicture (full image)
    ▲
    │ Contained_Within (DataRangeFacet: offset, size)
    │
ContentData (embedded thumbnail)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, File, RasterPicture,
    FileFacet, ContentDataFacet, FragmentFacet, DataRangeFacet,
)
from case_uco.uco.types import Hash

graph = CASEGraph()

# === Split file pattern ===

# The logical whole content
whole = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(
        hash=[Hash(hash_method=["SHA256"], hash_value="...")],
        size_in_bytes=...,
    )],
)

# Individual fragments
for i in range(3):  # adjust count from source
    fragment = graph.create(File,
        has_facet=[
            FileFacet(file_name="...", size_in_bytes=...),
            FragmentFacet(
                fragment_index=[i],
                total_fragments=[3],  # from source
            ),
        ],
    )
    graph.create(Relationship,
        source=[whole], target=fragment,
        kind_of_relationship="Has_Fragment",
        is_directional=True,
    )

# === Embedded data pattern ===

# Full image
full_image = graph.create(RasterPicture,
    has_facet=[ContentDataFacet(
        hash=[Hash(hash_method=["SHA256"], hash_value="...")],
        size_in_bytes=...,
    )],
)

# Embedded thumbnail at a byte range
thumbnail = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(size_in_bytes=...)],
)

graph.create(Relationship,
    source=[thumbnail], target=full_image,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[DataRangeFacet(
        range_offset=...,  # byte offset from source
        range_size=...,    # size from source
    )],
)

graph.write("file_fragments.jsonld")
```

</details>

## Notes

- `FragmentFacet.fragment_index` and `total_fragments` are both `list[int]`.
- For fragments stored on a disk image, add a second `Contained_Within` relationship from each fragment `File` to the disk `Image`.
- `DataRangeFacet` goes on the `Relationship` (via `has_facet`), not on the contained object.
