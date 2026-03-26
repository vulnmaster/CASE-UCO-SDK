# Device and Workstation Modeling

> See [Recipe Index](INDEX.md) for all recipes.

Model computers, forensic workstations, and other hardware with detailed specifications, network addresses, and operating system relationships. Based on [CASE-Examples/device](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/device).

## Key classes

| Class | Role |
|---|---|
| `Device` + `DeviceFacet` | The hardware device (manufacturer, model, serial) |
| `ComputerSpecificationFacet` | Hardware specs (CPU, RAM, BIOS, hostname) |
| `DomainNameFacet` | Network hostname |
| `IPv4AddressFacet` | IP address |
| `OperatingSystem` + `OperatingSystemFacet` + `SoftwareFacet` | The installed OS |
| `Relationship` | Links device to OS (`Has_Operating_System`) |

## Pattern

```
Device
    ├── DeviceFacet (manufacturer, model, serial)
    ├── ComputerSpecificationFacet (CPU, RAM, BIOS, hostname)
    ├── DomainNameFacet (network name)
    └── IPv4AddressFacet (IP address)
         │
         └── Has_Operating_System ──▶ OperatingSystem + SoftwareFacet
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, Device,
    DeviceFacet, ComputerSpecificationFacet,
    DomainNameFacet, IPv4AddressFacet,
    OperatingSystemFacet, SoftwareFacet,
)

graph = CASEGraph()

mfr = graph.create(Identity, name="...")  # from source

workstation = graph.create(Device,
    has_facet=[
        DeviceFacet(
            manufacturer=mfr,
            model="...",           # from source
            serial_number="...",   # from source
            device_type="...",     # e.g. "Desktop", "Laptop", "Server"
        ),
        ComputerSpecificationFacet(
            hostname="...",        # from source
            total_ram=...,         # bytes, from source
            processor_architecture="...",  # e.g. "x86_64"
        ),
        DomainNameFacet(value="..."),       # FQDN from source
        IPv4AddressFacet(address_value="..."),  # IP from source
    ],
)

# Operating system as a separate object
os_obj = graph.create(ObservableObject, name="...",
    has_facet=[
        OperatingSystemFacet(),
        SoftwareFacet(version="..."),  # OS version from source
    ],
)

# Link device to its OS
graph.create(Relationship,
    source=[workstation], target=os_obj,
    kind_of_relationship="Has_Operating_System",
    is_directional=True,
)

graph.write("device.jsonld")
```

</details>

## Notes

- `ComputerSpecificationFacet` has many optional fields: `hostname`, `total_ram`, `available_ram`, `cpu`, `cpu_family`, `gpu`, `bios_version`, `bios_serial_number`, `processor_architecture`, etc. Populate only what the source provides.
- Use `Relationship` with `kind_of_relationship="Has_Operating_System"` to link devices to their OS.
- For forensic lab documentation, include the workstation's specs to establish the examination environment.
