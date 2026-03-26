# Disk Partitions and Volume Recovery

> See [Recipe Index](INDEX.md) for all recipes.

Model disk partition structures, volume recovery, and the relationships between physical media, partition tables, file systems, and recovered files. Based on [CASE-Examples/partitions](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/partitions).

## Key classes

| Class | Role |
|---|---|
| `File` + `FileFacet` | Disk image file |
| `DiskPartition` + `DiskPartitionFacet` | A partition on the disk |
| `ObservableObject` + `DiskPartitionFacet` | Partition table / system |
| `ObservableObject` + `VolumeFacet` | A logical volume |
| `FileSystem` | A file system on a volume |
| `Relationship` | Containment chain (`Contained_Within`, `Has_Partition`) |
| `ConfiguredTool` | Partition recovery tools with specific configurations |
| `InvestigativeAction` | Imaging, examination, and recovery steps |
| `ProvenanceRecord` | Links actions to recovered artifacts |

## Containment hierarchy

```
File (disk image)
    ▲ Forensic_Image_Of
    │
Device (physical disk)
    │
    └── Has_Partition ──▶ DiskPartition (partition table)
                              │
                              ├── Contained_Within ◀── DiskPartition (partition 1)
                              │                            └── Contained_Within ◀── Volume
                              │                                    └── Contained_Within ◀── FileSystem
                              │                                            └── Contained_Within ◀── File
                              │
                              └── Contained_Within ◀── DiskPartition (deleted partition)
                                                           └── (recovered via tool)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.tool import Tool, ConfiguredTool
from case_uco.uco.configuration import Configuration, ConfigurationEntry
from case_uco.uco.observable import (
    ObservableObject, File, Device, DiskPartition,
    FileFacet, DeviceFacet, DiskPartitionFacet,
    ContentDataFacet, RecoveredObjectFacet, DataRangeFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))
graph = CASEGraph()

# Physical disk
mfr = graph.create(Identity, name="...")
disk = graph.create(Device,
    has_facet=[DeviceFacet(
        manufacturer=mfr,
        model="...",
        serial_number="...",
        device_type="Disk",
    )],
)

# Disk image
disk_image = graph.create(File,
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"], hash_value="...",
        )]),
    ],
)
graph.create(Relationship,
    source=[disk_image], target=disk,
    kind_of_relationship="Forensic_Image_Of",
    is_directional=True,
)

# Partition table
partition_table = graph.create(DiskPartition,
    has_facet=[DiskPartitionFacet(
        partition_id=...,  # from source, if available
    )],
)
graph.create(Relationship,
    source=[disk], target=partition_table,
    kind_of_relationship="Has_Partition",
    is_directional=True,
)

# A normal partition
partition1 = graph.create(DiskPartition,
    has_facet=[DiskPartitionFacet(
        partition_id=...,
    )],
)
graph.create(Relationship,
    source=[partition1], target=partition_table,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    has_facet=[DataRangeFacet(
        range_offset=...,  # sector offset from source
        range_size=...,    # partition size from source
    )],
)

# A deleted/recovered partition
deleted_partition = graph.create(DiskPartition,
    has_facet=[
        DiskPartitionFacet(partition_id=...),
        RecoveredObjectFacet(
            content_recovered_status=["..."],
            metadata_recovered_status=["..."],
            name_recovered_status=["..."],
        ),
    ],
)
graph.create(Relationship,
    source=[deleted_partition], target=partition_table,
    kind_of_relationship="Contained_Within",
    is_directional=True,
)

# Recovery tool
base_tool = graph.create(Tool,
    name="...",     # e.g. "TestDisk" from source
    version="...",
)
recovery_config = Configuration(
    configuration_entry=[
        ConfigurationEntry(item_name="...", item_value=["..."]),
    ],
)
recovery_tool = graph.create(ConfiguredTool,
    name="...",
    is_configuration_of=base_tool,
    uses_configuration=recovery_config,
)

# Recovery action
examiner = graph.create(Identity, name="...")
recovery = graph.create(InvestigativeAction,
    name="Partition recovery",
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=examiner,
    instrument=[recovery_tool],
    object=[disk_image],
    result=[deleted_partition],
)

# Provenance
provenance = graph.create(ProvenanceRecord,
    name="...",
    exhibit_number="...",
    object=[disk_image, partition1, deleted_partition, recovery],
)

graph.write("partitions.jsonld")
```

</details>

## Notes

- The partition hierarchy is modeled as a chain of `Contained_Within` relationships: File → Device → PartitionTable → Partition → Volume → FileSystem → File.
- `DiskPartitionFacet` has `partition_id: Optional[int]` and other optional fields. Populate from the partition table.
- Use `DataRangeFacet` on the `Relationship` to specify the partition's sector offset and size.
- `RecoveredObjectFacet` on a deleted partition records the recovery status.
- For the full partition → volume → filesystem → files chain, create intermediate objects and link them with `Contained_Within` relationships.
