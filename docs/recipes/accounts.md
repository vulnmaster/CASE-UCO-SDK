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
| `Relationship` | Links person to accounts (`Has_Account`), and accounts to each other (`Associated_Account`) |

## Pattern

```
Person (Identity)
    │
    ├── Has_Account ──▶ DigitalAccount (Facebook)
    │                        ├── DigitalAccountFacet (login, display name)
    │                        ├── AccountAuthenticationFacet (password)
    │                        └── ApplicationAccountFacet (→ Application)
    │
    ├── Has_Account ──▶ EmailAccount
    │                        ├── AccountFacet (identifier)
    │                        └── EmailAccountFacet (→ EmailAddress)
    │
    └── Associated_Account ──▶ links between accounts on different platforms
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
        AccountFacet(account_identifier="..."),
        EmailAccountFacet(email_address=email_addr),
    ],
)

# Link person to accounts
graph.create(Relationship,
    source=[person], target=account,
    kind_of_relationship="Has_Account",
    is_directional=True,
)

graph.create(Relationship,
    source=[person], target=email_acct,
    kind_of_relationship="Has_Account",
    is_directional=True,
)

# Link accounts to each other (cross-platform association)
graph.create(Relationship,
    source=[account], target=email_acct,
    kind_of_relationship="Associated_Account",
    is_directional=False,
)

graph.write("accounts.jsonld")
```

</details>

## Notes

- `Person` is a subclass of `Identity`. Use `SimpleNameFacet` for structured name parts (`given_name`, `family_name` are `list[str]`).
- `AccountAuthenticationFacet` stores credentials. Only include if the source data contains extracted passwords.
- For multiple accounts, repeat the account creation + `Has_Account` relationship pattern for each platform.
