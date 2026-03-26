# Mobile Device and SIM Card

> See [Recipe Index](INDEX.md) for all recipes.

Model a complete mobile handset with its SIM card, carrier account, operating system, and hardware identifiers. Based on [CASE-Examples/mobile_device_and_sim_card](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/mobile_device_and_sim_card).

This complements the [cell-site recipe](cell-site.md) (which focuses on tower connections) and the [mobile-device recipe](mobile-device.md) (which focuses on apps and accounts).

## Key classes

| Class | Role |
|---|---|
| `MobileDevice` + `DeviceFacet` + `MobileDeviceFacet` | The handset (IMEI, Bluetooth, Wi-Fi MACs) |
| `SIMCard` + `SIMCardFacet` | SIM details (ICCID, IMSI, carrier) |
| `MobileAccount` + `AccountFacet` | Subscriber identity (MSISDN/phone number) |
| `OperatingSystem` + `SoftwareFacet` | The mobile OS |
| `Relationship` | `Contained_Within`, `Has_Operating_System`, `Has_Account` |

## Pattern

```
MobileDevice
    ├── DeviceFacet (manufacturer, model, serial)
    ├── MobileDeviceFacet (IMEI)
    ├── BluetoothAddressFacet (BT MAC)
    └── WifiAddressFacet (Wi-Fi MAC)
         │
         ├── Contained_Within ◀── SIMCard + SIMCardFacet (ICCID, IMSI, carrier)
         ├── Has_Operating_System ──▶ OperatingSystem + SoftwareFacet
         └── Has_Account ──▶ MobileAccount (MSISDN)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, Device, SIMCard,
    DeviceFacet, MobileDeviceFacet,
    BluetoothAddressFacet, WifiAddressFacet,
    SIMCardFacet, AccountFacet, MobileAccountFacet,
    OperatingSystemFacet, SoftwareFacet,
)

graph = CASEGraph()

# Manufacturer and carrier
mfr = graph.create(Identity, name="...")      # from source
carrier = graph.create(Identity, name="...")   # from source

# The mobile device
phone = graph.create(Device,
    has_facet=[
        DeviceFacet(
            manufacturer=mfr,
            model="...",           # from source
            serial_number="...",   # from source
            device_type="Mobile Phone",
        ),
        MobileDeviceFacet(
            imei=["..."],               # from source (list — dual SIM has two)
        ),
        BluetoothAddressFacet(
            address_value="...",        # BT MAC from source
        ),
        WifiAddressFacet(
            address_value="...",        # Wi-Fi MAC from source
        ),
    ],
)

# Operating system
os_obj = graph.create(ObservableObject, name="...",
    has_facet=[
        OperatingSystemFacet(),
        SoftwareFacet(version="..."),  # OS version from source
    ],
)
graph.create(Relationship,
    source=[phone], target=os_obj,
    kind_of_relationship="Has_Operating_System",
    is_directional=True,
)

# SIM card
sim = graph.create(SIMCard,
    has_facet=[SIMCardFacet(
        iccid="...",     # from source
        imsi="...",      # from source
        carrier=carrier,
    )],
)
graph.create(Relationship,
    source=[sim], target=phone,
    kind_of_relationship="Contained_Within",
    is_directional=True,
)

# Subscriber account (MSISDN / phone number)
mobile_acct = graph.create(ObservableObject,
    has_facet=[AccountFacet(
        account_identifier="...",  # phone number from source
        account_issuer=carrier,
        is_active=True,
    )],
)
graph.create(Relationship,
    source=[phone], target=mobile_acct,
    kind_of_relationship="Has_Account",
    is_directional=True,
)

graph.write("mobile_device_sim.jsonld")
```

</details>

## Notes

- `MobileDeviceFacet.imei` is `list[str]` — dual-SIM devices have two IMEIs.
- `BluetoothAddressFacet` and `WifiAddressFacet` both inherit `address_value: Optional[str]` from `MACAddressFacet`.
- `SIMCardFacet.carrier` expects an `Identity` object.
- Use `Relationship` with `kind_of_relationship` values: `"Contained_Within"` (SIM in device), `"Has_Operating_System"`, `"Has_Account"`.
