# Events and Authentication Logs

> See [Recipe Index](INDEX.md) for all recipes.

Model discrete events such as authentication attempts, login/logout actions, and system events with structured attributes. Based on [CASE-Examples/event](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/event).

## Key classes

| Class | Role |
|---|---|
| `Event` | A noteworthy occurrence with start/end times |
| `Action` | Sub-steps within the event (e.g., "submit credentials", "authenticate") |
| `Dictionary` + `DictionaryEntry` | Structured key-value attributes of the event |
| `ApplicationAccount` + `AccountFacet` | The account involved |
| `OnlineService` | The service being accessed |
| `Person` / `Identity` | The user performing the action |

## Pattern

```
Event
    ├── startTime / endTime
    ├── eventType = ["..."]
    ├── eventContext ──▶ Action (submit login)
    │                 ──▶ Action (authenticate)
    └── eventAttribute ──▶ Dictionary
                              └── DictionaryEntry (key="MFA", value="true")
                              └── DictionaryEntry (key="method", value="password")
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Event
from case_uco.uco.action import Action
from case_uco.uco.identity import Identity, Person
from case_uco.uco.location import Location, SimpleAddressFacet
from case_uco.uco.observable import (
    ObservableObject, AccountFacet, ApplicationAccountFacet,
)
from case_uco.uco.types import Dictionary, DictionaryEntry
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()

# The user
user = graph.create(Person, name="...")  # from source

# The service
service = graph.create(ObservableObject, name="...")  # from source

# The account used
account = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(account_identifier="..."),  # from source
        ApplicationAccountFacet(application=service),
    ],
)

# Sub-actions within the event
submit_action = graph.create(Action,
    name="...",  # e.g. "Submit login credentials"
    performer=user,
    object=[account],
)

auth_action = graph.create(Action,
    name="...",  # e.g. "Authenticate user"
    object=[account],
    result=[...],  # outcome objects if applicable
)

# The event itself
event = graph.create(Event,
    name="...",  # from source
    start_time=[datetime(..., tzinfo=tz)],
    end_time=[datetime(..., tzinfo=tz)],
    event_type=["..."],  # e.g. "Authentication" — from source
    event_context=[submit_action, auth_action],
    event_attribute=[Dictionary(
        entry=[
            DictionaryEntry(key="...", value="..."),  # from source
            DictionaryEntry(key="...", value="..."),
        ],
    )],
)

graph.write("event.jsonld")
```

</details>

## Notes

- `Event.start_time` and `Event.end_time` are `list[datetime]` (not single values like on `Action`).
- `event_type` is `list[str]` — use descriptive types from the source (e.g., "Authentication", "Login", "Logout").
- `event_context` links to `Action` objects that represent the sub-steps of the event.
- `event_attribute` uses `Dictionary` with `DictionaryEntry` key-value pairs for structured metadata (MFA status, credential type, session ID, etc.).
