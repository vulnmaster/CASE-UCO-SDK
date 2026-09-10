# Mobile Device Forensics

> See [Recipe Index](INDEX.md) for all recipes.

Model mobile device artifacts including apps and their data.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity
from case_uco.uco.observable import (
    ObservableObject, DeviceFacet, ApplicationFacet,
    OperatingSystemFacet, SoftwareFacet, AccountFacet,
)

graph = CASEGraph()

# DeviceFacet.manufacturer expects an Identity, not a string
samsung = graph.create(Identity, name="Samsung")

phone = graph.create(ObservableObject,
    has_facet=[
        DeviceFacet(
            manufacturer=samsung, model="Galaxy S24",
            serial_number="RZ8T30EXAMPLE", device_type="Mobile Phone",
        ),
        OperatingSystemFacet(),
        SoftwareFacet(version="14"),
    ],
)

# ApplicationFacet has no "name" field — set name on the ObservableObject
messaging_app = graph.create(ObservableObject,
    name="Messenger App",
    has_facet=[ApplicationFacet(
        application_identifier="com.example.messenger",
        version="5.2.1",
    )],
)

account = graph.create(ObservableObject,
    has_facet=[AccountFacet(
        account_identifier="user@example.com",
        is_active=True,
    )],
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

var samsung = graph.Add(new Identity { Name = "Samsung" });

graph.Add(new ObservableObject {
    HasFacet = {
        new DeviceFacet {
            Manufacturer = samsung, Model = "Galaxy S24",
            SerialNumber = "RZ8T30EXAMPLE", DeviceType = "Mobile Phone"
        },
        new OperatingSystemFacet(),
        new SoftwareFacet { Version = "14" }
    }
});

graph.Add(new ObservableObject {
    Name = "Messenger App",
    HasFacet = { new ApplicationFacet {
        ApplicationIdentifier = "com.example.messenger",
        Version = "5.2.1"
    }}
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var samsung = new Identity();
samsung.setName("Samsung");
graph.add(samsung);

var device = new DeviceFacet();
device.setManufacturer(samsung);
device.setModel("Galaxy S24");
device.setSerialNumber("RZ8T30EXAMPLE");
var phone = new ObservableObject();
phone.getHasFacet().add(device);
graph.add(phone);

var appObs = new ObservableObject();
appObs.setName("Messenger App");
var app = new ApplicationFacet();
app.setApplicationIdentifier("com.example.messenger");
app.setVersion("5.2.1");
appObs.getHasFacet().add(app);
graph.add(appObs);

System.out.println(graph.serialize());
```

</details>

## Related

- [starter-mobile-extraction.md](starter-mobile-extraction.md) — end-to-end mobile extraction starter kit
- [mobile-device-sim.md](mobile-device-sim.md) — handset + SIM identifiers
- [sms-and-contacts.md](sms-and-contacts.md) — messages and contacts from the extraction
- [call-log.md](call-log.md) — call records
- [cell-site.md](cell-site.md) — tower/location data
- [cellebrite-ufed-xml.md](cellebrite-ufed-xml.md) — mapping a Cellebrite UFED `report.xml`
- [magnet-axiom-export.md](magnet-axiom-export.md) — mapping a Magnet AXIOM XML export
- [msab-xry-export.md](msab-xry-export.md) — mapping an MSAB XRY / XAMN export
