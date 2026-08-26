# Spear Phishing and Attack Narratives

> See [Recipe Index](INDEX.md) for all recipes.

Model a spear-phishing attack narrative — the delivery chain from initial email through malware execution, using both standard CASE/UCO types and extended ontology patterns. Based on [CASE-Examples/spear_phishing](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/spear_phishing).

## Key classes

| Class | Role |
|---|---|
| `Person` / `Identity` | Attacker and victim |
| `Victim` | The targeted individual (from `uco.victim`) |
| `EmailMessage` + `EmailMessageFacet` | The phishing email |
| `EmailAddress` + `EmailAddressFacet` | Sender/recipient addresses |
| `URL` + `URLFacet` | Malicious links |
| `File` + `FileFacet` | Malicious attachments/payloads |
| `Software` / `MaliciousTool` | Malware |
| `Device` | Victim's computer |
| `InvestigativeAction` | Detection and response actions |
| `Relationship` | Links between entities in the attack chain |

## Attack chain pattern

```
Person (attacker)
    │
    └── Sent ──▶ EmailMessage (phishing email)
                      ├── uco-observable:from ──▶ EmailAddress (spoofed sender)
                      ├── uco-observable:to ──▶ EmailAddress (victim)
                      └── Contains ──▶ URL (malicious link)
                                          │
                                          └── Related_To ──▶ File (description: URL delivered payload)
                                                              │
                                                              └── Related_To ──▶ Device (description: payload executed on device)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.identity import Identity, Person
from case_uco.uco.victim import Victim
from case_uco.uco.core import Relationship
from case_uco.uco.tool import MaliciousTool
from case_uco.uco.observable import (
    ObservableObject, Device, File,
    EmailMessageFacet, EmailAddressFacet,
    URLFacet, FileFacet, ContentDataFacet,
    DeviceFacet, SoftwareFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))
graph = CASEGraph()

# People
attacker = graph.create(Person, name="...")  # from source
victim_person = graph.create(Person, name="...")  # from source

# Victim role
victim_role = graph.create(Victim, name="...")

# Email addresses
sender_addr = graph.create(ObservableObject,
    has_facet=[EmailAddressFacet(
        address_value="...",  # spoofed sender from source
    )],
)
victim_addr = graph.create(ObservableObject,
    has_facet=[EmailAddressFacet(
        address_value="...",  # victim email from source
    )],
)

# The phishing email
phishing_email = graph.create(ObservableObject,
    has_facet=[EmailMessageFacet(
        subject="...",  # from source
        sent_time=datetime(..., tzinfo=tz),
        is_read=True,
        body="...",     # from source
    )],
)

# Malicious URL in the email
malicious_url = graph.create(ObservableObject,
    has_facet=[URLFacet(full_value="...")],  # from source
)

# Malware payload
malware = graph.create(MaliciousTool,
    name="...",    # malware name from source
    version="...",
)

payload = graph.create(File,
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"], hash_value="...",
        )]),
    ],
)

# Victim's device
victim_device = graph.create(Device,
    has_facet=[DeviceFacet(
        device_type="...",  # e.g. "Desktop" from source
    )],
)

# Attack chain relationships
graph.create(Relationship,
    source=[attacker], target=phishing_email,
    kind_of_relationship="Sent",
    is_directional=True,
)

graph.create(Relationship,
    source=[phishing_email], target=malicious_url,
    kind_of_relationship="Contains",
    is_directional=True,
)

graph.create(Relationship,
    source=[malicious_url], target=payload,
    kind_of_relationship="Related_To",
    description=["The source URL delivered the target payload."],
    is_directional=True,
)

graph.create(Relationship,
    source=[payload], target=victim_device,
    kind_of_relationship="Related_To",
    description=["The source payload executed on the target device."],
    is_directional=True,
)

# Link victim person to their role and device
graph.create(Relationship,
    source=[victim_person], target=victim_role,
    kind_of_relationship="Related_To",
    description=["The source person bears the target victim role."],
    is_directional=True,
)

graph.create(Relationship,
    source=[victim_person], target=victim_device,
    kind_of_relationship="Related_To",
    description=["The source person owns or controls the target device according to the evidence."],
    is_directional=True,
)

# Investigation and detection
investigation = graph.create(Investigation,
    name="...",
    description=["..."],
)

detection = graph.create(InvestigativeAction,
    name="...",  # e.g. "Malware detection" from source
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    object=[victim_device, payload],
)

graph.write("spear_phishing.jsonld")
```

</details>

## Notes

- `MaliciousTool` is a subclass of `Tool` — use it for malware, exploit kits, and offensive tools.
- `Victim` is from `case_uco.uco.victim` — it's a `Role` subclass for the targeted party.
- Use registered `Sent` and `Contains` where their semantics match. Use registered `Related_To` with a precise `description` for delivery, execution, role, and ownership assertions that lack a declared direct property.
- The CASE-Examples version uses an `ep:` (Endpoint Protection) extended ontology for `ObservableAction` and `Event` types. For standard CASE/UCO, model each attack step as a `Relationship` or `Action` instead.
- For incident response workflows, add `InvestigativeAction` nodes for detection, containment, eradication, and recovery steps.

## Related

- [network-investigation.md](network-investigation.md) — the full network investigation wrapper
- [network-artifacts.md](network-artifacts.md) — IPs, DNS, URLs in the attack chain
- [email-messaging.md](email-messaging.md) — the phishing emails themselves
- [analysis.md](analysis.md) — malware analysis of the payload
- [cyber-threat-intelligence.md](cyber-threat-intelligence.md) — APT/CTI threat reports (contrast: intelligence about an adversary across many intrusions, not a single delivery chain)
