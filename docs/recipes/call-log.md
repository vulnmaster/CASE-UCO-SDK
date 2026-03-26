# Call Log Records

> See [Recipe Index](INDEX.md) for all recipes.

Model phone call records extracted from a device or carrier data — including directional calls, multi-party calls, and conference bridges.

## Key classes

| Class | Role |
|---|---|
| `Call` | The call observable (subclass of `ObservableObject`) |
| `CallFacet` | Call metadata: type, duration, start/end, participants |
| `PhoneAccount` | A phone number account (caller or recipient) |
| `PhoneAccountFacet` | The phone number string |
| `AccountFacet` | Account identifier, issuer (carrier), active status |
| `Application` | The calling app (native dialer, VoIP app, etc.) |

## Call types

The `call_type` field on `CallFacet` typically holds values like `"Incoming"`, `"Outgoing"`, or `"Missed"`. For multi-party calls, add multiple entries to `to` or use `participant`.

## Pattern

```
PhoneAccount (caller)  ──from──▶  Call + CallFacet  ◀──to──  PhoneAccount (recipient)
                                       │
                                       └── application ──▶ Application (dialer/VoIP app)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity
from case_uco.uco.observable import (
    ObservableObject, Call, CallFacet,
    PhoneAccountFacet, AccountFacet, ApplicationFacet,
)
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# Carrier (issuer of the phone accounts)
carrier = graph.create(Identity, name="...")  # from source

# Calling application
dialer = graph.create(ObservableObject, name="...",
    has_facet=[ApplicationFacet(
        application_identifier="...",  # e.g. "com.android.dialer"
        version="...",
    )],
)

# Phone accounts (one per phone number)
caller = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(
            account_identifier="...",  # phone number from source
            account_issuer=carrier,
            is_active=True,
        ),
        PhoneAccountFacet(phone_number="..."),
    ],
)

recipient = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(
            account_identifier="...",
            account_issuer=carrier,
            is_active=True,
        ),
        PhoneAccountFacet(phone_number="..."),
    ],
)

# A phone call
call = graph.create(Call,
    has_facet=[CallFacet(
        call_type="...",  # "Incoming", "Outgoing", "Missed" from source
        start_time=datetime(..., tzinfo=tz),
        end_time=datetime(..., tzinfo=tz),
        duration=...,  # seconds, from source
        application=dialer,
        from_=caller,
        to=[recipient],
    )],
)

graph.write("call_log.jsonld")
```

</details>

## Multi-party and conference calls

For three-way calls, add multiple accounts to `to`. For conference bridges (e.g., Zoom), model the bridge as an `Application` and list all participants:

```python
call = graph.create(Call,
    has_facet=[CallFacet(
        call_type="...",
        application=conference_app,
        from_=initiator,
        to=[participant_1, participant_2, participant_3],
        start_time=datetime(..., tzinfo=tz),
        end_time=datetime(..., tzinfo=tz),
        duration=...,
    )],
)
```
