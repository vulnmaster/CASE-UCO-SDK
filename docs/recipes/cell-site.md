# Cell Site and Tower Data

> See [Recipe Index](INDEX.md) for all recipes.

Model cell tower connections, SIM card details, mobile carrier accounts, and captured telecommunications information (CDR data). This pattern is used for location tracking, timeline reconstruction, and carrier records analysis.

## Key classes

| Class | Role |
|---|---|
| `Device` + `DeviceFacet` + `MobileDeviceFacet` | The mobile handset (IMEI, Bluetooth, Wi-Fi) |
| `SIMCard` + `SIMCardFacet` | SIM card details (ICCID, IMSI, carrier) |
| `MobileAccount` + `MobileAccountFacet` | The subscriber account (MSISDN) |
| `CellSite` + `CellSiteFacet` | A cell tower (MCC, MNC, LAC, cell ID, type) |
| `AntennaFacet` | Antenna properties (azimuth, height, beam width, signal) |
| `Location` + `LatLongCoordinatesFacet` | Geographic position of the tower |
| `Relationship` | Links device to cell site, SIM to device, etc. |

## Pattern

```
Device + DeviceFacet + MobileDeviceFacet
    │
    ├── Contained_Within ◀── SIMCard + SIMCardFacet
    ├── Has_Account ──▶ MobileAccount (MSISDN)
    └── Connected_To ──▶ CellSite + CellSiteFacet + AntennaFacet
                              │
                              └── location ──▶ Location + LatLongCoordinatesFacet
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.location import Location, LatLongCoordinatesFacet
from case_uco.uco.observable import (
    ObservableObject, Device, SIMCard, CellSite,
    DeviceFacet, MobileDeviceFacet,
    SIMCardFacet, AccountFacet,
    CellSiteFacet, AntennaFacet,
    SoftwareFacet, OperatingSystemFacet,
)
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# Carrier
carrier = graph.create(Identity, name="...")  # from source

# Device manufacturer
mfr = graph.create(Identity, name="...")  # from source

# Mobile device
phone = graph.create(Device,
    has_facet=[
        DeviceFacet(
            manufacturer=mfr,
            model="...",            # from source
            serial_number="...",    # from source
            device_type="Mobile Phone",
        ),
        MobileDeviceFacet(
            imei=["..."],           # from source (list)
        ),
        OperatingSystemFacet(),
        SoftwareFacet(version="..."),  # OS version from source
    ],
)

# SIM card
sim = graph.create(SIMCard,
    has_facet=[SIMCardFacet(
        iccid="...",    # from source
        imsi="...",     # from source
        carrier=carrier,
    )],
)

# SIM contained within the device
graph.create(Relationship,
    source=[sim], target=phone,
    kind_of_relationship="Contained_Within",
    is_directional=True,
)

# Subscriber account (phone number / MSISDN)
mobile_acct = graph.create(ObservableObject,
    has_facet=[AccountFacet(
        account_identifier="...",  # MSISDN from source
        account_issuer=carrier,
        is_active=True,
    )],
)

# Cell site / tower
tower_location = graph.create(Location,
    name="...",  # tower name/ID from source if available
    has_facet=[LatLongCoordinatesFacet(
        latitude=...,   # from source
        longitude=...,  # from source
    )],
)

cell_tower = graph.create(CellSite,
    has_facet=[
        CellSiteFacet(
            cell_site_country_code="...",       # MCC from source
            cell_site_network_code="...",       # MNC from source
            cell_site_location_area_code="...", # LAC from source
            cell_site_identifier="...",         # Cell ID from source
            cell_site_type="...",               # e.g. "GSM", "LTE"
        ),
        AntennaFacet(
            azimuth=...,              # degrees, from source
            antenna_height=...,       # meters, from source
            horizontal_beam_width=...,
            signal_strength=...,
        ),
    ],
)

# Device connected to cell site (with time bounds)
graph.create(Relationship,
    source=[phone], target=cell_tower,
    kind_of_relationship="Connected_To",
    is_directional=True,
    start_time=[datetime(..., tzinfo=tz)],
    end_time=[datetime(..., tzinfo=tz)],
)

graph.write("cell_site.jsonld")
```

</details>

## Notes

- `MobileDeviceFacet.imei` is `list[str]` (dual-SIM devices have two).
- `SIMCardFacet.carrier` expects an `Identity` object.
- `CellSiteFacet` fields are all strings: country code (MCC), network code (MNC), location area code (LAC), cell identifier (Cell ID), and cell type.
- `AntennaFacet` fields are all `Optional[float]`: `azimuth`, `antenna_height`, `elevation`, `horizontal_beam_width`, `signal_strength`, `skew`.
- For CDR (Call Detail Records), model each connection as a time-bounded `Relationship` between the device and the cell site. Create one relationship per connection event in the source data.
- For multiple towers over time, create multiple `CellSite` objects and multiple `Relationship` objects with different time ranges.
