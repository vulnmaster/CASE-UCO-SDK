# SMS Messages and Contacts

> See [Recipe Index](INDEX.md) for all recipes.

Model SMS/MMS messages and contact list entries extracted from a mobile device, including the relationships between contacts and their accounts.

## Key classes

| Class | Role |
|---|---|
| `SMSMessage` | The SMS observable (subclass of `Message`) |
| `MessageFacet` | Message text, sender, recipient(s), timestamp |
| `Contact` | A contact list entry |
| `ContactFacet` | Contact details: name, phone, email, nickname |
| `PhoneAccount` / `EmailAccount` | Accounts linked to the contact |
| `ObservableRelationship` | Links contacts to accounts with registered `Related_To` and an attribution description |

## Pattern

```
Contact + ContactFacet
    │
    ├── Related_To ──▶ PhoneAccount + PhoneAccountFacet (description: contact phone account)
    └── Related_To ──▶ EmailAccount + EmailAddressFacet (description: contact email account)

SMSMessage + MessageFacet
    ├── uco-observable:from ──▶ PhoneAccount (sender)
    ├── uco-observable:to ──▶ PhoneAccount (recipient)
    └── uco-observable:application ──▶ Application (messaging app)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, SMSMessage, Contact,
    MessageFacet, ContactFacet,
    PhoneAccountFacet, AccountFacet,
    ApplicationFacet,
)
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# Messaging application
sms_app = graph.create(ObservableObject, name="...",
    has_facet=[ApplicationFacet(
        application_identifier="...",  # e.g. "com.android.mms"
        version="...",
    )],
)

# Phone accounts (one per number)
sender_acct = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(account_identifier="..."),
        PhoneAccountFacet(phone_number="..."),  # from source
    ],
)

recipient_acct = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(account_identifier="..."),
        PhoneAccountFacet(phone_number="..."),
    ],
)

# SMS message
sms = graph.create(SMSMessage,
    has_facet=[MessageFacet(
        application=sms_app,
        from_=sender_acct,
        to=[recipient_acct],
        message_text="...",        # from source
        sent_time=datetime(..., tzinfo=tz),
        message_type="SMS",
    )],
)

# Contact entry
contact = graph.create(Contact,
    has_facet=[ContactFacet(
        first_name="...",   # from source
        last_name="...",    # from source
        display_name="...", # from source
        nickname=["..."],   # from source, if present
    )],
)

# Link contact to their phone account
graph.create(Relationship,
    source=[contact], target=recipient_acct,
    kind_of_relationship="Related_To",
    description=["The target phone account is attributed to the source contact entry."],
    is_directional=True,
)

graph.write("sms_and_contacts.jsonld")
```

</details>

## Notes

- `ContactFacet` has many optional fields: `first_name`, `last_name`, `middle_name`, `display_name`, `nickname`, `birthdate`, `contact_phone`, `contact_email`, etc. Populate only what the source provides.
- Use registered `Related_To` to link a `Contact` to `PhoneAccount` or `EmailAccount` entries and state the attribution basis in `description`.
- For MMS with attachments, add a `ContentDataFacet` to the message or create a separate `ObservableObject` for the attachment linked via a `Relationship`.

## Related

- [call-log.md](call-log.md) — call records from the same handset
- [threaded-messaging.md](threaded-messaging.md) — ordered chat threads
- [accounts.md](accounts.md) — linking numbers to platform identities
- [starter-mobile-extraction.md](starter-mobile-extraction.md) — end-to-end mobile mapping starter kit
