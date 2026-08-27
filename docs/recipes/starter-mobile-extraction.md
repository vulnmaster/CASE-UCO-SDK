# Starter Kit: Mobile Device Extraction

> See [Recipe Index](INDEX.md) for all recipes.

Map a mobile device extraction (device info, installed apps, messages) into a CASE/UCO graph.

## Source Input Shape

A JSON report from a mobile forensic tool:

```json
{
  "device": {
    "manufacturer": "Samsung", "model": "Galaxy S24",
    "serial": "RZ8T30EXAMPLE", "imei": "353456789012345",
    "os_version": "14", "carrier": "Verizon",
    "iccid": "8901260852280054321"
  },
  "apps": [
    { "package": "com.whatsapp", "version": "2.24.8", "name": "WhatsApp" }
  ],
  "messages": [
    { "app": "com.whatsapp", "from": "+15551234567",
      "text": "Meeting at 3pm", "sent": "2025-07-01T15:04:00Z" }
  ]
}
```

## Modeling Choices

| Concept | CASE/UCO Class | Why |
|---|---|---|
| The phone | `ObservableObject` + `DeviceFacet` + `MobileDeviceFacet` | `DeviceFacet` captures make/model/serial; `MobileDeviceFacet` adds IMEI and network |
| SIM card | `ObservableObject` + `SIMCardFacet` | SIM is a separate physical artifact with its own ICCID and carrier |
| Each app | `ObservableObject` + `ApplicationFacet` | Apps are observables with a package identifier and version |
| Each message | `ObservableObject` + `MessageFacet` | `MessageFacet` captures sender, text, and timestamp |
| Extraction tool | `Tool` | Records which forensic tool performed the extraction |

## Anti-Patterns

- **Flat modeling without device hierarchy.** Do NOT put apps, messages, and the device into unrelated observables. Link messages to their app and apps to the device so consumers can reconstruct the containment tree.
- **Missing SIM/carrier info.** The SIM card is a separate observable, not a string field on the device. Model it with `SIMCardFacet` and link the carrier as an `Identity`.
- **Manufacturer as a string.** `DeviceFacet.manufacturer` expects an `Identity` object, not a plain string. Create an `Identity` and reference it.

## Complete Code

```python
from datetime import datetime
from case_uco import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.uco.identity import Identity
from case_uco.uco.observable import (
    ObservableObject, DeviceFacet, MobileDeviceFacet,
    SIMCardFacet, ApplicationFacet, MessageFacet,
)

graph = CASEGraph()

tool = graph.create(Tool, name="UFED", version="7.65", tool_type="Mobile Extraction")

samsung = graph.create(Identity, name="Samsung")
verizon = graph.create(Identity, name="Verizon")

phone = graph.create(ObservableObject,
    has_facet=[
        DeviceFacet(
            manufacturer=samsung, model="Galaxy S24",
            serial_number="RZ8T30EXAMPLE", device_type="Mobile Phone",
        ),
        MobileDeviceFacet(
            imei=["353456789012345"],
            network="LTE",
        ),
    ],
)

sim = graph.create(ObservableObject,
    has_facet=[SIMCardFacet(
        iccid="8901260852280054321",
        carrier=verizon,
        sim_type="nano-SIM",
    )],
)

whatsapp = graph.create(ObservableObject,
    name="WhatsApp",
    has_facet=[ApplicationFacet(
        application_identifier="com.whatsapp",
        version="2.24.8",
    )],
)

sender_phone = graph.create(ObservableObject, name="+15551234567")

msg = graph.create(ObservableObject,
    has_facet=[MessageFacet(
        application=whatsapp,
        from_=sender_phone,
        message_text="Meeting at 3pm",
        message_type="chat",
        sent_time=datetime(2025, 7, 1, 15, 4, 0),
    )],
)

graph.write("mobile-extraction.jsonld")
```

## Expected JSON-LD Output

```json
{
    "@context": { "...": "..." },
    "@graph": [
        {
            "@id": "kb:Tool-...", "@type": "uco-tool:Tool",
            "uco-core:name": "UFED", "uco-tool:version": "7.65"
        },
        {
            "@id": "kb:ObservableObject-...",
            "@type": "uco-observable:ObservableObject",
            "uco-core:hasFacet": [
                {
                    "@type": "uco-observable:DeviceFacet",
                    "uco-observable:manufacturer": { "@id": "kb:Identity-..." },
                    "uco-observable:model": "Galaxy S24",
                    "uco-observable:serialNumber": "RZ8T30EXAMPLE"
                },
                {
                    "@type": "uco-observable:MobileDeviceFacet",
                    "uco-observable:IMEI": ["353456789012345"]
                }
            ]
        },
        {
            "@id": "kb:ObservableObject-...",
            "uco-core:hasFacet": [{
                "@type": "uco-observable:SIMCardFacet",
                "uco-observable:ICCID": "8901260852280054321",
                "uco-observable:carrier": { "@id": "kb:Identity-..." }
            }]
        },
        {
            "@id": "kb:ObservableObject-...",
            "uco-core:hasFacet": [{
                "@type": "uco-observable:MessageFacet",
                "uco-observable:from": { "@id": "kb:ObservableObject-..." },
                "uco-observable:messageText": "Meeting at 3pm",
                "uco-observable:sentTime": { "@type": "xsd:dateTime", "@value": "2025-07-01T15:04:00" }
            }]
        }
    ]
}
```

## Validation

```bash
case_validate --built-version case-1.4.0 mobile-extraction.jsonld
```

When the extraction log establishes a filesystem extract (DFT-1020) or
another catalogued technique, record it with
[technique-evidence-outcome.md](technique-evidence-outcome.md). Do not
infer a technique from the product name "Cellebrite" or "UFED" alone.

## Related

- [mobile-device.md](mobile-device.md) — deeper mobile device patterns
- [mobile-device-sim.md](mobile-device-sim.md) — handset + SIM detail
- [sms-and-contacts.md](sms-and-contacts.md) — messages and contacts
- [call-log.md](call-log.md) — call records
- [technique-evidence-outcome.md](technique-evidence-outcome.md) — sourced method plus legal-outcome join
