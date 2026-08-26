# Multi-Platform Account Linking

> See [Recipe Index](INDEX.md) for all recipes.

Model a person's online accounts across multiple platforms (social media, email, cloud services) and the relationships between them. Based on [CASE-Examples/accounts](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/accounts).

## Key classes

| Class | Role |
|---|---|
| `Identity` / `Person` | The individual who owns the accounts |
| `DigitalAccount` + `DigitalAccountFacet` | A platform-specific account (login, display name) |
| `EmailAccount` + `EmailAccountFacet` | An email account |
| `EmailAddress` + `EmailAddressFacet` | An email address observable |
| `ApplicationAccountFacet` | Links an account to its application |
| `AccountAuthenticationFacet` | Credentials (password, last changed) |
| `Relationship` | Links accounts to each other with registered `Related_To` when a cross-platform association is asserted |

## Pattern

```
DigitalAccount (Facebook)
    ├── AccountFacet ── uco-observable:owner ──▶ Person (Identity)
    ├── DigitalAccountFacet (login, display name)
    ├── AccountAuthenticationFacet (password)
    └── ApplicationAccountFacet (→ Application)

EmailAccount
    ├── AccountFacet ── uco-observable:owner ──▶ Person (Identity)
    └── EmailAccountFacet (→ EmailAddress)

DigitalAccount ── Related_To ──▶ EmailAccount
    description: source evidence supports a cross-platform association
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity, Person, SimpleNameFacet
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, ApplicationFacet,
    AccountFacet, DigitalAccountFacet, AccountAuthenticationFacet,
    ApplicationAccountFacet, EmailAccountFacet, EmailAddressFacet,
)

graph = CASEGraph()

# The person
person = graph.create(Person,
    has_facet=[SimpleNameFacet(
        given_name=["..."],   # from source
        family_name=["..."],  # from source
    )],
)

# Platform application (e.g., Facebook, Google)
platform = graph.create(ObservableObject, name="...",
    has_facet=[ApplicationFacet(
        application_identifier="...",  # from source
        version="...",
    )],
)

# Platform issuer (organization)
org = graph.create(Identity, name="...")  # from source

# A digital account on that platform
account = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(
            account_identifier="...",  # username/ID from source
            account_issuer=org,
            owner=person,
            is_active=True,
        ),
        DigitalAccountFacet(
            display_name="...",    # from source
            first_login_time=...,  # from source, if available
        ),
        ApplicationAccountFacet(
            application=platform,
        ),
        AccountAuthenticationFacet(
            password="...",  # from source, if extracted
        ),
    ],
)

# An email address
email_addr = graph.create(ObservableObject,
    has_facet=[EmailAddressFacet(
        address_value="...",  # from source
    )],
)

# An email account
email_acct = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(account_identifier="...", owner=person),
        EmailAccountFacet(email_address=email_addr),
    ],
)

# Link accounts to each other only when source evidence supports attribution.
graph.create(Relationship,
    source=[account], target=email_acct,
    kind_of_relationship="Related_To",
    description=["Source evidence supports a cross-platform account association."],
    is_directional=False,
)

graph.write("accounts.jsonld")
```

</details>

## Notes

- `Person` is a subclass of `Identity`. Use `SimpleNameFacet` for structured name parts (`given_name`, `family_name` are `list[str]`).
- `AccountAuthenticationFacet` stores credentials. Only include if the source data contains extracted passwords.
- For multiple accounts, set `uco-observable:owner` through each account's `AccountFacet`; add `Related_To` only for a separately supported cross-platform association.

## Related

- [email-messaging.md](email-messaging.md) — email account evidence behind the identities
- [sms-and-contacts.md](sms-and-contacts.md) — phone-number identities and contact entries
- [threaded-messaging.md](threaded-messaging.md) — conversations between the linked accounts
- [device.md](device.md) — the devices the accounts were used from
