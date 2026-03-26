# File Recovery and Carving

> See [Recipe Index](INDEX.md) for all recipes.

Model recovered/carved files, their recovery status, and the reconstruction process. Based on [CASE-Examples/reconstructed_file](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/reconstructed_file) and [CASE-Examples/recoverability](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/recoverability).

## Key classes

| Class | Role |
|---|---|
| `RecoveredObject` | A file or artifact that was recovered (subclass of `File`) |
| `RecoveredObjectFacet` | Recovery status for content, metadata, and name |
| `FragmentFacet` | Fragment details when carving reassembles pieces |
| `ContentDataFacet` | Hash of the recovered content |
| `InvestigativeAction` | The carving/recovery action |
| `AnalyticTool` | The recovery tool (e.g., Scalpel, PhotoRec) |

## Pattern

```
RecoveredObject + RecoveredObjectFacet
    ├── content_recovered_status = ["Complete"]
    ├── metadata_recovered_status = ["Partial"]
    └── name_recovered_status = ["None"]
         │
         └── Has_Fragment ──▶ ContentData fragments
                                └── Contained_Within ──▶ disk Image (DataRangeFacet)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.tool import AnalyticTool
from case_uco.uco.observable import (
    ObservableObject, File,
    FileFacet, ContentDataFacet, RecoveredObjectFacet,
    FragmentFacet, DataRangeFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))
graph = CASEGraph()

# Recovery tool
tool = graph.create(AnalyticTool,
    name="...",     # e.g. "Scalpel", "PhotoRec" from source
    version="...",
    tool_type="File Carving",
)

# The disk image being carved
disk_image = graph.create(File,
    has_facet=[FileFacet(file_name="...", size_in_bytes=...)],
)

# A recovered file with recovery status
recovered = graph.create(ObservableObject,
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"], hash_value="...",
        )]),
        RecoveredObjectFacet(
            content_recovered_status=["..."],   # "Complete", "Partial", "None"
            metadata_recovered_status=["..."],  # from source
            name_recovered_status=["..."],      # from source
        ),
    ],
)

# If the recovered file was assembled from fragments
fragment = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(size_in_bytes=...)],
)
graph.create(Relationship,
    source=[recovered], target=fragment,
    kind_of_relationship="Has_Fragment",
    is_directional=True,
)
graph.create(Relationship,
    source=[fragment], target=disk_image,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[DataRangeFacet(
        range_offset=...,  # byte offset from source
        range_size=...,    # from source
    )],
)

# The carving action
examiner = graph.create(Identity, name="...")
carving = graph.create(InvestigativeAction,
    name="File carving",
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=examiner,
    instrument=[tool],
    object=[disk_image],
    result=[recovered],
)

graph.write("file_recovery.jsonld")
```

</details>

## Notes

- `RecoveredObjectFacet` status fields are all `list[str]`. Common values: `"Complete"`, `"Partial"`, `"None"`, `"Unknown"`.
- For multiple recovered files, create one `ObservableObject` + `RecoveredObjectFacet` per file.
- When a recovered file was repaired (e.g., header reconstruction), model the repair as a separate `InvestigativeAction` with the original as `object` and the repaired version as `result`.
