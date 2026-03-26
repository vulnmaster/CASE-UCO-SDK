# Threaded Messaging (WhatsApp, Chat)

> See [Recipe Index](INDEX.md) for all recipes.

Model threaded chat conversations with ordered messages, participants, and attachments. Covers WhatsApp-style private chats and public social media threads. Based on [CASE-Examples/message](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/message).

This extends the basic [email-messaging recipe](email-messaging.md) and [SMS recipe](sms-and-contacts.md) with thread structure.

## Key classes

| Class | Role |
|---|---|
| `MessageThread` + `MessageThreadFacet` | A conversation thread |
| `Message` + `MessageFacet` | An individual message |
| `Thread` / `ThreadItem` | Ordered message sequence (from `uco.types`) |
| `ApplicationAccount` | Participant accounts |
| `ContentData` + `URLFacet` | Attachments and media |
| `Relationship` | Attachment links |

## Pattern

```
MessageThread + MessageThreadFacet
    ├── participant ──▶ ApplicationAccount (user A)
    ├── participant ──▶ ApplicationAccount (user B)
    └── messageThread ──▶ Thread
                            ├── ThreadItem → Message 1
                            ├── ThreadItem → Message 2
                            └── ThreadItem → Message 3

Message + MessageFacet
    ├── from ──▶ ApplicationAccount
    ├── to ──▶ [ApplicationAccount]
    ├── application ──▶ Application
    └── sentTime, messageText, messageType
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, Message, MessageFacet,
    ApplicationFacet, AccountFacet, ApplicationAccountFacet,
    ContentDataFacet, URLFacet,
)
from case_uco.uco.types import Thread, ThreadItem
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))
graph = CASEGraph()

# Chat application
app = graph.create(ObservableObject, name="...",
    has_facet=[ApplicationFacet(
        application_identifier="...",  # e.g. "com.whatsapp"
        version="...",
    )],
)

# Participant accounts
user_a = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(account_identifier="..."),
        ApplicationAccountFacet(application=app),
    ],
)
user_b = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(account_identifier="..."),
        ApplicationAccountFacet(application=app),
    ],
)

# Individual messages
msg1 = graph.create(Message,
    has_facet=[MessageFacet(
        application=app,
        from_=user_a,
        to=[user_b],
        message_text="...",  # from source
        message_type="...",  # e.g. "Chat"
        sent_time=datetime(..., tzinfo=tz),
    )],
)

msg2 = graph.create(Message,
    has_facet=[MessageFacet(
        application=app,
        from_=user_b,
        to=[user_a],
        message_text="...",
        message_type="...",
        sent_time=datetime(..., tzinfo=tz),
    )],
)

# Message with attachment
attachment = graph.create(ObservableObject,
    has_facet=[
        ContentDataFacet(size_in_bytes=...),
        URLFacet(full_value="..."),  # media URL from source
    ],
)
graph.create(Relationship,
    source=[attachment], target=msg2,
    kind_of_relationship="Attachment_Of",
    is_directional=True,
)

graph.write("threaded_messaging.jsonld")
```

</details>

## Notes

- `MessageFacet.from_` (with trailing underscore) is `Optional[ObservableObject]`. `to` is `list[ObservableObject]`.
- For ordered threads, the CASE ontology uses `Thread` and `ThreadItem` from `uco.types`. These use the Collections Ontology (`co:`) pattern internally. For simpler cases, you can group messages by timestamp without the formal thread structure.
- `MessageThreadFacet` has `participant: list[ObservableObject]` and `message_thread: Optional[Thread]`.
- Attachments are modeled as separate `ObservableObject`s linked via `Relationship` with `kind_of_relationship="Attachment_Of"`.
