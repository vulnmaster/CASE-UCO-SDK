# EXIF and Image Metadata

> See [Recipe Index](INDEX.md) for all recipes.

Model image files with EXIF metadata, camera identification, and the provenance chain from extraction through analysis.

## Key classes

| Class | Role |
|---|---|
| `File` | The image file observable |
| `FileFacet` | Filename, path, size, timestamps |
| `ContentDataFacet` | Hash, MIME type, size |
| `RasterPictureFacet` | Image dimensions, bits per pixel, picture type |
| `EXIFFacet` | EXIF key-value pairs via `ControlledDictionary` |
| `Device` + `DeviceFacet` | The camera that took the photo |
| `Hash` | Integrity hash (from `uco.types`) |
| `ControlledDictionary` / `ControlledDictionaryEntry` | EXIF tag name-value pairs |

## Pattern

```
File + FileFacet + ContentDataFacet + RasterPictureFacet + EXIFFacet
    │
    └── Contained_Within ──▶ DiskPartition (with PathRelationFacet)

Device + DeviceFacet (camera)

InvestigativeAction (photo examination)
    ├── object ──▶ File
    ├── instrument ──▶ AnalyticTool (ExifTool, etc.)
    └── result ──▶ analysis outputs
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity
from case_uco.uco.tool import AnalyticTool
from case_uco.uco.observable import (
    ObservableObject, File, Device,
    FileFacet, ContentDataFacet, RasterPictureFacet, EXIFFacet,
    DeviceFacet,
)
from case_uco.uco.types import Hash, ControlledDictionary, ControlledDictionaryEntry
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# Camera device
camera_mfr = graph.create(Identity, name="...")  # from EXIF Make tag
camera = graph.create(Device,
    has_facet=[DeviceFacet(
        manufacturer=camera_mfr,
        model="...",          # from EXIF Model tag
        serial_number="...",  # from EXIF if available
        device_type="Camera",
    )],
)

# Image file with EXIF data
image = graph.create(File,
    has_facet=[
        FileFacet(
            file_name="...",       # from source
            file_path="...",       # from source
            size_in_bytes=...,     # from source
        ),
        ContentDataFacet(
            hash=[Hash(
                hash_method=["SHA256"],
                hash_value="...",  # from source
            )],
            mime_type=["image/jpeg"],
        ),
        RasterPictureFacet(
            picture_height=...,    # pixels, from EXIF
            picture_width=...,     # pixels, from EXIF
            bits_per_pixel=...,    # from EXIF
            picture_type="...",    # e.g. "JPEG"
            camera=camera,
        ),
        EXIFFacet(
            exif_data=[ControlledDictionary(
                entry=[
                    ControlledDictionaryEntry(key="Make", value="..."),
                    ControlledDictionaryEntry(key="Model", value="..."),
                    ControlledDictionaryEntry(key="DateTime", value="..."),
                    ControlledDictionaryEntry(key="GPSLatitude", value="..."),
                    ControlledDictionaryEntry(key="GPSLongitude", value="..."),
                    # add as many EXIF tags as the source provides
                ],
            )],
        ),
    ],
)

# Tool used for EXIF extraction
exiftool = graph.create(AnalyticTool,
    name="...",     # e.g. "ExifTool"
    version="...",  # from source
    tool_type="Metadata Extraction",
)

# Examination action
examination = graph.create(InvestigativeAction,
    name="EXIF metadata extraction",
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    instrument=[exiftool],
    object=[image],
)

graph.write("exif_data.jsonld")
```

</details>

## Notes

- `EXIFFacet.exif_data` takes a `list[ControlledDictionary]`. Each dictionary contains `ControlledDictionaryEntry` objects with `key`/`value` string pairs — one per EXIF tag.
- Link the image to its source partition/volume using a `Relationship` with `kind_of_relationship="Contained_Within"`.
- GPS coordinates from EXIF can also be modeled as a `Location` with `LatLongCoordinatesFacet`, linked via `Relationship`.
