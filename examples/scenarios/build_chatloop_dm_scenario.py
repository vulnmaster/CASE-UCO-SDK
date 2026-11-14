#!/usr/bin/env python3
"""Build a CASE/UCO graph for the fictional ChatLoop DM transcript.

Tier T0 (fully synthetic). Addresses forensic-provenance feedback:
deterministic opaque IRIs, source transcript artifact + transform provenance,
DM visibility=false, no invented package/session/message IDs, formal Thread
ordering, specific Application/SmartPhone types, and lineage tags
(source-verbatim | source-normalized | analyst-inferred | generator-created).
"""

from __future__ import annotations

import hashlib
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from case_uco import CASEGraph
from case_uco.validation.runtime import prepare_validator
from case_uco import __version__ as CASE_UCO_VERSION
from case_uco.case.investigation import (
    Investigation,
    InvestigativeAction,
    ProvenanceRecord,
)
from case_uco.uco.action import Action
from case_uco.uco.core import Annotation, ExternalReference
from case_uco.uco.identity import Organization, Person, SimpleNameFacet
from case_uco.uco.location import Location, SimpleAddressFacet
from case_uco.uco.observable import (
    AccountFacet,
    Application,
    ApplicationAccount,
    ApplicationAccountFacet,
    ApplicationFacet,
    ContentDataFacet,
    DeviceFacet,
    FileFacet,
    Message,
    MessageFacet,
    MessageThread,
    MessageThreadFacet,
    ObservableObject,
    SmartPhone,
)
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

TZ = ZoneInfo("America/New_York")
DIR = Path(__file__).resolve().parent
REPO_ROOT = DIR.parent.parent
SOURCE_PATH = DIR / "chatloop-dm-ritchie-highway-source.md"
OUT_PATH = DIR / "chatloop-dm-ritchie-highway.jsonld"
VALIDATION_PATH = DIR / "chatloop-dm-ritchie-highway.validation.txt"
KB = "https://example.org/kb/chatloop-dm/"

SOURCE_VERBATIM = "source-verbatim"
SOURCE_NORMALIZED = "source-normalized"
ANALYST_INFERRED = "analyst-inferred"
GENERATOR_CREATED = "generator-created"

MESSAGES: list[tuple[str | None, datetime, str, str]] = [
    # Friday, October 10, 2025 — afternoon
    ("evan", datetime(2025, 10, 10, 15, 42, 18, tzinfo=TZ), "Did you see the baseball cards they put out at Target?", "Chat"),
    ("tyler", datetime(2025, 10, 10, 15, 43, 2, tzinfo=TZ), "The new boxes by the toys?", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 43, 16, tzinfo=TZ), "Yeah. The Topps Chrome ones.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 15, 44, 51, tzinfo=TZ), "Those are like $40 each.", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 45, 9, tzinfo=TZ), "I know. Everybody at school is looking for them.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 15, 47, 33, tzinfo=TZ), "You buying one?", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 48, 11, tzinfo=TZ), "I only have twelve dollars.", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 49, 27, tzinfo=TZ), "We could just take a couple.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 15, 51, 6, tzinfo=TZ), "Are you serious?", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 51, 44, tzinfo=TZ), "Maybe.", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 52, 3, tzinfo=TZ), "They had a whole shelf yesterday.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 15, 55, 28, tzinfo=TZ), "My mom shops there all the time.", "Chat"),
    ("evan", datetime(2025, 10, 10, 15, 56, 10, tzinfo=TZ), "She wouldn’t be there Saturday night.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 16, 1, 49, tzinfo=TZ), "What time?", "Chat"),
    ("evan", datetime(2025, 10, 10, 16, 3, 22, tzinfo=TZ), "Maybe around 7.", "Chat"),
    ("evan", datetime(2025, 10, 10, 16, 4, 1, tzinfo=TZ), "We can meet near the front entrance and look around first.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 16, 7, 36, tzinfo=TZ), "I don’t know, dude.", "Chat"),
    ("evan", datetime(2025, 10, 10, 16, 8, 42, tzinfo=TZ), "Just think about it.", "Chat"),
    # Friday evening
    ("tyler", datetime(2025, 10, 10, 20, 14, 5, tzinfo=TZ), "Which Target are you talking about?", "Chat"),
    ("evan", datetime(2025, 10, 10, 20, 15, 47, tzinfo=TZ), "The one on Ritchie Highway.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 20, 16, 32, tzinfo=TZ), "The one next to the pet store?", "Chat"),
    ("evan", datetime(2025, 10, 10, 20, 16, 41, tzinfo=TZ), "Yeah.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 20, 18, 9, tzinfo=TZ), "Are the cards still there?", "Chat"),
    ("evan", datetime(2025, 10, 10, 20, 20, 23, tzinfo=TZ), "I checked the app. It says limited stock.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 20, 21, 4, tzinfo=TZ), "That could mean none.", "Chat"),
    ("evan", datetime(2025, 10, 10, 20, 21, 47, tzinfo=TZ), "I can stop in tomorrow afternoon and see.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 20, 23, 12, tzinfo=TZ), "Don’t do anything without me.", "Chat"),
    ("evan", datetime(2025, 10, 10, 20, 24, 19, tzinfo=TZ), "So you’re in?", "Chat"),
    ("tyler", datetime(2025, 10, 10, 20, 26, 53, tzinfo=TZ), "I didn’t say that.", "Chat"),
    ("tyler", datetime(2025, 10, 10, 20, 27, 8, tzinfo=TZ), "But message me after you check.", "Chat"),
    # Saturday morning
    ("evan", datetime(2025, 10, 11, 11, 6, 35, tzinfo=TZ), "My dad is taking me near Target after lunch.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 11, 7, 18, tzinfo=TZ), "Okay.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 11, 7, 44, tzinfo=TZ), "Just see if they have the cards.", "Chat"),
    ("evan", datetime(2025, 10, 11, 11, 8, 3, tzinfo=TZ), "That’s what I’m doing.", "Chat"),
    # Saturday afternoon recon
    ("evan", datetime(2025, 10, 11, 14, 38, 26, tzinfo=TZ), "They still have some.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 14, 39, 41, tzinfo=TZ), "How many?", "Chat"),
    ("evan", datetime(2025, 10, 11, 14, 40, 5, tzinfo=TZ), "Maybe six boxes and some individual packs.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 14, 41, 17, tzinfo=TZ), "Were there workers around?", "Chat"),
    ("evan", datetime(2025, 10, 11, 14, 42, 38, tzinfo=TZ), "There were employees in the department.", "Chat"),
    ("evan", datetime(2025, 10, 11, 14, 43, 16, tzinfo=TZ), "This is starting to feel like a bad idea.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 14, 44, 59, tzinfo=TZ), "You were the one who suggested it.", "Chat"),
    ("evan", datetime(2025, 10, 11, 14, 46, 4, tzinfo=TZ), "I know.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 14, 48, 21, tzinfo=TZ), "Are we still meeting at 7?", "Chat"),
    ("evan", datetime(2025, 10, 11, 14, 50, 13, tzinfo=TZ), "Meet me outside at 6:45. We can decide then.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 14, 51, 9, tzinfo=TZ), "My brother can drop me off.", "Chat"),
    ("evan", datetime(2025, 10, 11, 14, 52, 42, tzinfo=TZ), "Don’t tell him why.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 14, 54, 6, tzinfo=TZ), "Obviously.", "Chat"),
    # Saturday evening prep
    ("tyler", datetime(2025, 10, 11, 17, 17, 33, tzinfo=TZ), "What are you wearing?", "Chat"),
    ("evan", datetime(2025, 10, 11, 17, 18, 46, tzinfo=TZ), "Gray hoodie and jeans.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 17, 19, 12, tzinfo=TZ), "I have my Orioles sweatshirt.", "Chat"),
    ("evan", datetime(2025, 10, 11, 17, 20, 28, tzinfo=TZ), "Okay.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 17, 22, 2, tzinfo=TZ), "I’m nervous.", "Chat"),
    ("evan", datetime(2025, 10, 11, 17, 23, 49, tzinfo=TZ), "Me too.", "Chat"),
    ("evan", datetime(2025, 10, 11, 17, 24, 38, tzinfo=TZ), "We don’t have to do it.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 17, 26, 10, tzinfo=TZ), "But those boxes sell online for way more.", "Chat"),
    ("evan", datetime(2025, 10, 11, 17, 27, 44, tzinfo=TZ), "That doesn’t make it worth getting arrested.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 17, 29, 8, tzinfo=TZ), "Let’s at least go there.", "Chat"),
    # Arrival
    ("tyler", datetime(2025, 10, 11, 18, 39, 51, tzinfo=TZ), "I’m here.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 18, 40, 17, tzinfo=TZ), "By the carts outside.", "Chat"),
    ("evan", datetime(2025, 10, 11, 18, 42, 6, tzinfo=TZ), "Walking over now.", "Chat"),
    ("evan", datetime(2025, 10, 11, 18, 44, 29, tzinfo=TZ), "I see you.", "Chat"),
    # After store visit
    ("tyler", datetime(2025, 10, 11, 19, 12, 43, tzinfo=TZ), "Why did you leave?", "Chat"),
    ("evan", datetime(2025, 10, 11, 19, 13, 18, tzinfo=TZ), "That employee kept watching us.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 19, 13, 55, tzinfo=TZ), "You still have the packs?", "Chat"),
    ("evan", datetime(2025, 10, 11, 19, 14, 37, tzinfo=TZ), "No. I put mine back.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 19, 15, 6, tzinfo=TZ), "I didn’t.", "Chat"),
    ("evan", datetime(2025, 10, 11, 19, 15, 48, tzinfo=TZ), "Tyler, are you serious?", "Chat"),
    ("tyler", datetime(2025, 10, 11, 19, 16, 32, tzinfo=TZ), "I have two packs.", "Chat"),
    ("evan", datetime(2025, 10, 11, 19, 17, 11, tzinfo=TZ), "Take them back.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 19, 18, 4, tzinfo=TZ), "I’m already outside.", "Chat"),
    ("evan", datetime(2025, 10, 11, 19, 18, 39, tzinfo=TZ), "This was stupid.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 19, 19, 52, tzinfo=TZ), "Don’t tell anyone.", "Chat"),
    ("evan", datetime(2025, 10, 11, 19, 20, 26, tzinfo=TZ), "I’m not taking any of them.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 19, 21, 8, tzinfo=TZ), "Fine.", "Chat"),
    # Saturday night aftermath
    ("evan", datetime(2025, 10, 11, 21, 36, 14, tzinfo=TZ), "Did your brother see the cards?", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 38, 57, tzinfo=TZ), "No.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 39, 18, tzinfo=TZ), "They’re in my room.", "Chat"),
    ("evan", datetime(2025, 10, 11, 21, 40, 6, tzinfo=TZ), "You need to return them tomorrow.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 41, 44, tzinfo=TZ), "How am I supposed to return something I didn’t pay for?", "Chat"),
    ("evan", datetime(2025, 10, 11, 21, 43, 20, tzinfo=TZ), "Go back with your mom and tell the truth.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 44, 31, tzinfo=TZ), "Absolutely not.", "Chat"),
    ("evan", datetime(2025, 10, 11, 21, 46, 2, tzinfo=TZ), "I don’t want to be involved anymore.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 47, 15, tzinfo=TZ), "You planned the whole thing.", "Chat"),
    ("evan", datetime(2025, 10, 11, 21, 48, 3, tzinfo=TZ), "And I backed out.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 50, 39, tzinfo=TZ), "Delete this chat.", "Chat"),
    ("evan", datetime(2025, 10, 11, 21, 51, 12, tzinfo=TZ), "Deleting it doesn’t make it disappear.", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 52, 7, tzinfo=TZ), "Just do it.", "Chat"),
    (None, datetime(2025, 10, 11, 21, 54, 26, tzinfo=TZ), "Tyler Reed deleted a message.", "System"),
    ("evan", datetime(2025, 10, 11, 21, 55, 40, tzinfo=TZ), "What did you delete?", "Chat"),
    ("tyler", datetime(2025, 10, 11, 21, 57, 8, tzinfo=TZ), "Nothing important.", "Chat"),
    # Sunday morning
    ("tyler", datetime(2025, 10, 12, 10, 22, 51, tzinfo=TZ), "My mom found the packs.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 24, 13, tzinfo=TZ), "What happened?", "Chat"),
    ("tyler", datetime(2025, 10, 12, 10, 25, 47, tzinfo=TZ), "She asked where I got them.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 26, 29, tzinfo=TZ), "Did you tell her?", "Chat"),
    ("tyler", datetime(2025, 10, 12, 10, 28, 4, tzinfo=TZ), "Not yet.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 29, 16, tzinfo=TZ), "Tell her the truth.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 10, 31, 53, tzinfo=TZ), "She said we are going back to Target this afternoon.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 33, 1, tzinfo=TZ), "Good.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 10, 34, 27, tzinfo=TZ), "She might call your parents.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 35, 12, tzinfo=TZ), "I’ll tell them what happened.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 10, 36, 49, tzinfo=TZ), "You’re going to say it was all me.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 38, 33, tzinfo=TZ), "No. I’ll say I suggested it and went with you, but I put the cards back.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 10, 39, 45, tzinfo=TZ), "I wish we never talked about this.", "Chat"),
    ("evan", datetime(2025, 10, 12, 10, 41, 18, tzinfo=TZ), "Same.", "Chat"),
    # Sunday afternoon resolution
    ("tyler", datetime(2025, 10, 12, 16, 48, 7, tzinfo=TZ), "We returned the packs.", "Chat"),
    ("evan", datetime(2025, 10, 12, 16, 49, 36, tzinfo=TZ), "What did the store say?", "Chat"),
    ("tyler", datetime(2025, 10, 12, 16, 51, 22, tzinfo=TZ), "A manager talked to us. My mom paid for them because the packages were bent.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 16, 52, 8, tzinfo=TZ), "I’m grounded for a month.", "Chat"),
    ("evan", datetime(2025, 10, 12, 16, 53, 41, tzinfo=TZ), "My parents know too.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 16, 54, 19, tzinfo=TZ), "Are you grounded?", "Chat"),
    ("evan", datetime(2025, 10, 12, 16, 55, 34, tzinfo=TZ), "Two weeks and I have to apologize to the manager.", "Chat"),
    ("tyler", datetime(2025, 10, 12, 16, 57, 1, tzinfo=TZ), "Never doing anything like that again.", "Chat"),
    ("evan", datetime(2025, 10, 12, 16, 57, 46, tzinfo=TZ), "Agreed.", "Chat"),
    (
        None,
        datetime(2025, 10, 12, 16, 58, 23, tzinfo=TZ),
        'Evan Brooks changed disappearing-message duration from “24 hours” to “Off.”',
        "System",
    ),
]



def _canonical_transcript() -> str:
    """Serialize MESSAGES into a stable source transcript (UTF-8)."""
    lines = [
        "# Fictional Social-Media Chat Transcript",
        "",
        "**Application:** ChatLoop",
        "**Conversation Type:** Direct message",
        "**Device Source:** Apple iPhone 15",
        "**Participants:**",
        "",
        "* **Evan Brooks** — username: `evan_b17` — age 16",
        "* **Tyler Reed** — username: `ty_reed09` — age 15",
        "",
        "**Time Zone:** America/New_York",
        "**Target Location Referenced:** Target store on Ritchie Highway",
        "**Note:** All people, accounts, locations, and events in this transcript are fictional.",
        "",
        "---",
        "",
    ]
    current_day = None
    for sender, sent, text, msg_type in MESSAGES:
        day = sent.strftime("%A, %B ") + str(sent.day) + sent.strftime(", %Y")
        if day != current_day:
            if current_day is not None:
                lines.extend(["", "---", ""])
            lines.extend([f"## {day}", ""])
            current_day = day
        stamp = sent.strftime("%I:%M:%S %p")
        if stamp.startswith("0"):
            stamp = stamp[1:]
        if msg_type == "System":
            who = "System Message"
        else:
            who = "Evan Brooks" if sender == "evan" else "Tyler Reed"
        lines.extend([f"**{stamp} — {who}**", "", text, ""])
    return "\n".join(lines).rstrip() + "\n"


def _opaque_id(source_sha256: str, kind: str, key: str) -> str:
    u = uuid.uuid5(uuid.NAMESPACE_URL, f"{source_sha256}|{kind}|{key}")
    return f"kb:{kind}-{u}"


def build() -> Path:
    transcript = _canonical_transcript()
    SOURCE_PATH.write_text(transcript, encoding="utf-8")
    source_bytes = transcript.encode("utf-8")
    source_sha = hashlib.sha256(source_bytes).hexdigest()

    def kid(kind: str, key: str) -> str:
        return _opaque_id(source_sha, kind, key)

    graph = CASEGraph(kb_prefix=KB, extra_context={"co": "http://purl.org/co/"})

    def make_rel(
        source_id: str,
        target_id: str,
        kind: str,
        lineage: str,
        key: str,
        description: str | None = None,
    ) -> None:
        props: dict = {"uco-core:tag": [lineage]}
        if description:
            props["uco-core:description"] = [description]
        graph.create_relationship(
            source_id,
            target_id,
            kind,
            directional=True,
            relationship_id=kid("Relationship", key),
            properties=props,
        )

    tool = graph.create(
        Tool,
        id=kid("Tool", "case-uco-sdk"),
        name="case-uco (Python SDK)",
        version=CASE_UCO_VERSION,
        tool_type="CASE/UCO graph serialization",
        description=[
            f"Built with case-uco {CASE_UCO_VERSION}; validate with "
            "case_validate --built-version case-1.5.0 (CASE 1.5.0 / UCO 1.5.0)."
        ],
    )

    source_hash = Hash(hash_method="SHA256", hash_value=source_sha)
    graph.add(source_hash, id=kid("Hash", "source-transcript"))
    source_file_facet = FileFacet(
        file_name=[SOURCE_PATH.name],
        file_path=[SOURCE_PATH.relative_to(REPO_ROOT).as_posix()],
        extension="md",
        size_in_bytes=len(source_bytes),
        is_directory=[False],
    )
    source_content_facet = ContentDataFacet(
        mime_type=["text/markdown"],
        size_in_bytes=len(source_bytes),
        hash=[source_hash],
    )
    graph.add(source_file_facet, id=kid("FileFacet", "source-transcript"))
    graph.add(source_content_facet, id=kid("ContentDataFacet", "source-transcript"))
    source_artifact = graph.create(
        ObservableObject,
        id=kid("ObservableObject", "source-transcript"),
        name="ChatLoop DM source transcript (fictional)",
        description=[
            "Canonical UTF-8 markdown serialization of the fictional ChatLoop "
            "direct-message transcript used as input to this graph transform."
        ],
        tag=["synthetic", "tier-t0", SOURCE_VERBATIM],
        has_facet=[source_file_facet, source_content_facet],
    )

    apple = graph.create(
        Organization,
        id=kid("Organization", "apple"),
        name="Apple Inc.",
    )
    device_facet = DeviceFacet(
        manufacturer=apple,
        model="iPhone 15",
        device_type="Mobile Phone",
    )
    graph.add(device_facet, id=kid("DeviceFacet", "iphone-15"))
    device = graph.create(
        SmartPhone,
        id=kid("SmartPhone", "iphone-15"),
        name="Apple iPhone 15 (reported device source)",
        description=[
            "Device source stated in transcript metadata. Not a forensic image; "
            "no IMEI/serial was provided."
        ],
        tag=[SOURCE_NORMALIZED],
        has_facet=[device_facet],
    )
    graph.add_type(kid("SmartPhone", "iphone-15"), "uco-observable:AppleDevice")

    app_facet = ApplicationFacet()
    graph.add(app_facet, id=kid("ApplicationFacet", "chatloop"))
    app = graph.create(
        Application,
        id=kid("Application", "chatloop"),
        name="ChatLoop",
        description=["Application name from transcript metadata (verbatim)."],
        tag=[SOURCE_VERBATIM],
        has_facet=[app_facet],
    )

    target_org = graph.create(
        Organization,
        id=kid("Organization", "target"),
        name="Target",
        description=["Retail organization named in chat message text."],
        tag=[SOURCE_VERBATIM],
    )
    loc_facet = SimpleAddressFacet(street="Ritchie Highway")
    graph.add(loc_facet, id=kid("SimpleAddressFacet", "ritchie-highway"))
    target_location = graph.create(
        Location,
        id=kid("Location", "ritchie-highway-target"),
        name="Target store on Ritchie Highway",
        description=[
            "Location referenced in chat. Street name only; no street number, "
            "city, or coordinates were provided."
        ],
        tag=[SOURCE_NORMALIZED],
        has_facet=[loc_facet],
    )
    make_rel(
        kid("Organization", "target"),
        kid("Location", "ritchie-highway-target"),
        "Located_At",
        ANALYST_INFERRED,
        "target-located-at-ritchie",
        "Inferred from messages naming Target on Ritchie Highway.",
    )

    evan_name = SimpleNameFacet(given_name=["Evan"], family_name=["Brooks"])
    tyler_name = SimpleNameFacet(given_name=["Tyler"], family_name=["Reed"])
    graph.add(evan_name, id=kid("SimpleNameFacet", "evan-brooks"))
    graph.add(tyler_name, id=kid("SimpleNameFacet", "tyler-reed"))
    evan = graph.create(
        Person,
        id=kid("Person", "evan-brooks"),
        name="Evan Brooks",
        has_facet=[evan_name],
        tag=[SOURCE_VERBATIM],
    )
    tyler = graph.create(
        Person,
        id=kid("Person", "tyler-reed"),
        name="Tyler Reed",
        has_facet=[tyler_name],
        tag=[SOURCE_VERBATIM],
    )
    graph.create(
        Annotation,
        id=kid("Annotation", "evan-age"),
        object=[evan],
        statement=[
            "Reported age at time of chat: 16 (transcript participant metadata; "
            "birthdate not provided)."
        ],
        tag=[SOURCE_NORMALIZED],
    )
    graph.create(
        Annotation,
        id=kid("Annotation", "tyler-age"),
        object=[tyler],
        statement=[
            "Reported age at time of chat: 15 (transcript participant metadata; "
            "birthdate not provided)."
        ],
        tag=[SOURCE_NORMALIZED],
    )

    evan_acct_facet = AccountFacet(
        account_identifier="evan_b17",
        owner=evan,
    )
    tyler_acct_facet = AccountFacet(
        account_identifier="ty_reed09",
        owner=tyler,
    )
    evan_app_facet = ApplicationAccountFacet(application=app)
    tyler_app_facet = ApplicationAccountFacet(application=app)
    graph.add(evan_acct_facet, id=kid("AccountFacet", "evan_b17"))
    graph.add(tyler_acct_facet, id=kid("AccountFacet", "ty_reed09"))
    graph.add(evan_app_facet, id=kid("ApplicationAccountFacet", "evan_b17"))
    graph.add(tyler_app_facet, id=kid("ApplicationAccountFacet", "ty_reed09"))

    evan_acct = graph.create(
        ApplicationAccount,
        id=kid("ApplicationAccount", "evan_b17"),
        name="evan_b17",
        description=["Username from transcript participant metadata."],
        tag=[SOURCE_VERBATIM],
        has_facet=[evan_acct_facet, evan_app_facet],
    )
    tyler_acct = graph.create(
        ApplicationAccount,
        id=kid("ApplicationAccount", "ty_reed09"),
        name="ty_reed09",
        description=["Username from transcript participant metadata."],
        tag=[SOURCE_VERBATIM],
        has_facet=[tyler_acct_facet, tyler_app_facet],
    )
    accounts = {"evan": evan_acct, "tyler": tyler_acct}
    peer = {"evan": tyler_acct, "tyler": evan_acct}
    message_ids: list[str] = []
    msg_objs: list[Message] = []

    for idx, (sender_key, sent_time, text, msg_type) in enumerate(MESSAGES, start=1):
        ordinal = f"{idx:03d}"
        msg_id = kid("Message", ordinal)
        message_ids.append(msg_id)

        if sender_key is None:
            to_accts = [evan_acct, tyler_acct]
            name = f"System message (transcript ordinal {ordinal})"
            facet_kwargs: dict = {
                "application": app,
                "to": to_accts,
                "message_text": text,
                "message_type": msg_type,
                "sent_time": sent_time,
            }
        else:
            name = f"Chat message (transcript ordinal {ordinal})"
            facet_kwargs = {
                "application": app,
                "from_": accounts[sender_key],
                "to": [peer[sender_key]],
                "message_text": text,
                "message_type": msg_type,
                "sent_time": sent_time,
            }

        facet = MessageFacet(**facet_kwargs)
        graph.add(facet, id=kid("MessageFacet", ordinal))
        ext = ExternalReference(
            defining_context=(
                "generator-created transcript ordinal (1-based source order); "
                "not a native ChatLoop message identifier"
            ),
            external_identifier=ordinal,
        )
        graph.add(ext, id=kid("ExternalReference", f"ordinal-{ordinal}"))
        msg = graph.create(
            Message,
            id=msg_id,
            name=name,
            tag=[SOURCE_VERBATIM if msg_type == "Chat" else SOURCE_NORMALIZED],
            external_reference=[ext],
            has_facet=[facet],
        )
        msg_objs.append(msg)

    # Formal Thread / ThreadItem ordering (source order independent of timestamps).
    thread_seq_id = kid("Thread", "dm-sequence")
    item_ids = [kid("ThreadItem", f"{i:03d}") for i in range(1, len(message_ids) + 1)]
    for i, (item_id, mid) in enumerate(zip(item_ids, message_ids)):
        props: dict = {
            "co:itemContent": {"@id": mid},
            "co:index": {"@type": "xsd:positiveInteger", "@value": str(i + 1)},
        }
        if i > 0:
            props["uco-types:threadPreviousItem"] = {"@id": item_ids[i - 1]}
        if i < len(item_ids) - 1:
            props["uco-types:threadNextItem"] = {"@id": item_ids[i + 1]}
        graph.upsert_node(item_id, types="uco-types:ThreadItem", properties=props)

    graph.upsert_node(
        thread_seq_id,
        types="uco-types:Thread",
        properties={
            "co:size": {
                "@type": "xsd:nonNegativeInteger",
                "@value": str(len(message_ids)),
            },
            "co:element": [{"@id": mid} for mid in message_ids],
            "co:item": [{"@id": iid} for iid in item_ids],
            "uco-types:threadOriginItem": [{"@id": item_ids[0]}],
            "uco-types:threadTerminalItem": [{"@id": item_ids[-1]}],
        },
    )

    thread_facet = MessageThreadFacet(
        participant=[evan_acct, tyler_acct],
        visibility=False,
    )
    graph.add(thread_facet, id=kid("MessageThreadFacet", "dm"))
    thread = graph.create(
        MessageThread,
        id=kid("MessageThread", "dm"),
        name="ChatLoop DM: evan_b17 ↔ ty_reed09",
        description=[
            "Direct-message conversation (private). Source order is encoded in "
            "MessageThreadFacet.messageThread (uco-types:Thread / ThreadItem). "
            "Part_Of edges are generator-created query aids."
        ],
        tag=[SOURCE_NORMALIZED],
        has_facet=[thread_facet],
    )
    graph.set_property(
        kid("MessageThreadFacet", "dm"),
        "uco-observable:messageThread",
        {"@id": thread_seq_id},
    )

    for i, mid in enumerate(message_ids, start=1):
        make_rel(
            mid,
            kid("MessageThread", "dm"),
            "Part_Of",
            GENERATOR_CREATED,
            f"part-of-{i:03d}",
            "Graph-construction membership; source order also in ThreadItem.co:index.",
        )

    make_rel(
        kid("MessageThread", "dm"),
        kid("SmartPhone", "iphone-15"),
        "Associated_With",
        SOURCE_NORMALIZED,
        "thread-associated-device",
        "Transcript metadata lists Apple iPhone 15 as device source; not an acquisition claim.",
    )
    make_rel(
        kid("MessageThread", "dm"),
        kid("Application", "chatloop"),
        "Associated_With",
        SOURCE_VERBATIM,
        "thread-associated-app",
        "Conversation application named ChatLoop in transcript metadata.",
    )

    for ordinal in ("001", "019", "020", "021", "022"):
        make_rel(
            kid("Message", ordinal),
            kid("Location", "ritchie-highway-target"),
            "Mentions",
            ANALYST_INFERRED,
            f"mentions-location-{ordinal}",
            "Message text references Target and/or Ritchie Highway / adjacent landmark.",
        )
    make_rel(
        kid("MessageThread", "dm"),
        kid("Location", "ritchie-highway-target"),
        "Related_To",
        ANALYST_INFERRED,
        "thread-related-location",
        "Supported by Mentions edges from transcript ordinals 001 and 019–022.",
    )
    graph.create(
        Annotation,
        id=kid("Annotation", "location-evidence"),
        object=[target_location, thread],
        statement=[
            "Location inference is supported by transcript ordinals 001 and 019–022 "
            "(Target / Ritchie Highway / pet-store landmark). Not device GPS."
        ],
        tag=[ANALYST_INFERRED],
    )

    # Generated-metadata disclosure (no invented MessageFacet.messageID/sessionID).
    graph.create(
        Annotation,
        id=kid("Annotation", "generated-metadata"),
        object=[thread],
        statement=[
            (
                "Transcript ordinals 001–114 are stored only as ExternalReference "
                "externalIdentifier values (definingContext documents them as "
                "generator-created). No MessageFacet.messageID or sessionID was asserted."
            ),
            (
                "Graph @id values are opaque UUIDv5 digests of "
                "SHA256(source-transcript)|kind|key for reproducibility."
            ),
            f"Source transcript SHA-256: {source_sha}",
        ],
        tag=[GENERATOR_CREATED, "normalization"],
    )

    # Unknown deleted body placeholder + system Actions.
    unknown_deleted = graph.create(
        Message,
        id=kid("Message", "unknown-deleted"),
        name="Unknown deleted message (body unavailable)",
        description=[
            "Placeholder for content not present after a deletion tombstone. "
            "Original author, text, time, and native message identifier are unknown."
        ],
        tag=[SOURCE_NORMALIZED],
    )
    make_rel(
        kid("Message", "unknown-deleted"),
        kid("MessageThread", "dm"),
        "Part_Of",
        GENERATOR_CREATED,
        "part-of-unknown-deleted",
        "Placeholder membership for unavailable deleted content.",
    )

    del_idx = next(
        i for i, m in enumerate(MESSAGES) if m[3] == "System" and "deleted" in m[2]
    )
    disp_idx = next(
        i
        for i, m in enumerate(MESSAGES)
        if m[3] == "System" and "disappearing-message" in m[2]
    )
    del_msg = msg_objs[del_idx]
    disp_msg = msg_objs[disp_idx]

    delete_action = graph.create(
        Action,
        id=kid("Action", "message-deletion"),
        name="ChatLoop message deletion (tombstone observed)",
        description=[
            "System tombstone states Tyler Reed deleted a message. Does not "
            "establish that Tyler authored the deleted content; platform "
            "delete-own-only semantics were not stated in the source. Deleted "
            "body, original sent time, and native message ID are unavailable."
        ],
        performer=tyler_acct,
        object=[thread, unknown_deleted],
        result=[del_msg],
        start_time=MESSAGES[del_idx][1],
        tag=[SOURCE_NORMALIZED],
    )
    disappear_action = graph.create(
        Action,
        id=kid("Action", "disappearing-message-off"),
        name="Disappearing-message duration changed to Off",
        description=[
            "System message reports Evan Brooks changed disappearing-message "
            "duration from 24 hours to Off. Prior/resulting configuration "
            "captured only as rendered system text (no separate config object)."
        ],
        performer=evan_acct,
        object=[thread],
        result=[disp_msg],
        start_time=MESSAGES[disp_idx][1],
        tag=[SOURCE_NORMALIZED],
    )

    # Output artifact metadata (integrity hash recorded in validation report only —
    # embedding the graph hash inside the graph is circular).
    out_file_facet = FileFacet(
        file_name=[OUT_PATH.name],
        file_path=[OUT_PATH.relative_to(REPO_ROOT).as_posix()],
        extension="jsonld",
        is_directory=[False],
    )
    out_content_facet = ContentDataFacet(mime_type=["application/ld+json"])
    graph.add(out_file_facet, id=kid("FileFacet", "output-jsonld"))
    graph.add(out_content_facet, id=kid("ContentDataFacet", "output-jsonld"))
    output_artifact = graph.create(
        ObservableObject,
        id=kid("ObservableObject", "output-jsonld"),
        name="ChatLoop DM CASE/UCO JSON-LD (transform output)",
        description=[
            "JSON-LD graph produced by transforming the source transcript with "
            f"case-uco {CASE_UCO_VERSION}. SHA-256 of this file is recorded in "
            f"{VALIDATION_PATH.name} (not embedded here — circular otherwise)."
        ],
        tag=[GENERATOR_CREATED],
        has_facet=[out_file_facet, out_content_facet],
    )

    transform = graph.create(
        InvestigativeAction,
        id=kid("InvestigativeAction", "transform-transcript"),
        name="Transform ChatLoop transcript to CASE/UCO JSON-LD",
        description=[
            "SDK serialization / modeling step only. Does not represent a mobile "
            "device acquisition or ChatLoop server extraction."
        ],
        instrument=[tool],
        object=[source_artifact],
        result=[thread, output_artifact, delete_action, disappear_action],
        tag=[GENERATOR_CREATED],
    )

    provenance = graph.create(
        ProvenanceRecord,
        id=kid("ProvenanceRecord", "exhibit-001"),
        name="Provenance: ChatLoop DM transcript → CASE/UCO graph",
        exhibit_number="EX-CHATLOOP-DM-001",
        description=[
            "Digital artifact chain for the fictional transcript and its CASE/UCO "
            "serialization. No physical seizure or handset imaging is claimed."
        ],
        object=[
            source_artifact,
            output_artifact,
            thread,
            transform,
            tool,
            device,
        ],
        tag=["synthetic", "tier-t0"],
    )

    graph.create(
        Investigation,
        id=kid("Investigation", "chatloop-dm"),
        name="ChatLoop DM — Target / Ritchie Highway (fictional)",
        description=[
            "Fictional ChatLoop direct-message transcript (Tier T0). All persons, "
            "accounts, locations, and events are synthetic.",
            f"Builder: case-uco {CASE_UCO_VERSION}; CASE/UCO 1.5.0 validation target.",
        ],
        tag=["synthetic", "tier-t0"],
        focus=["messaging", "juvenile shoplifting discussion (fictional)"],
        investigation_form="case",
        investigation_status="open",
        object=[
            source_artifact,
            output_artifact,
            thread,
            device,
            app,
            transform,
            provenance,
            delete_action,
            disappear_action,
            target_location,
            target_org,
        ],
    )

    graph.write(str(OUT_PATH))
    out_bytes = OUT_PATH.read_bytes()
    final_sha = hashlib.sha256(out_bytes).hexdigest()

    proc = subprocess.run(
        [
            *prepare_validator("case-1.5.0").command,
            "--built-version",
            "case-1.5.0",
            str(OUT_PATH),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    report = (
        f"validator: case_validate\n"
        f"built-version: case-1.5.0\n"
        f"case-uco: {CASE_UCO_VERSION}\n"
        f"graph: {OUT_PATH.name}\n"
        f"source: {SOURCE_PATH.name}\n"
        f"source_sha256: {source_sha}\n"
        f"graph_sha256: {final_sha}\n"
        f"exit_code: {proc.returncode}\n"
        f"---\n"
        f"{proc.stdout}\n"
        f"{proc.stderr}\n"
    )
    VALIDATION_PATH.write_text(report, encoding="utf-8")
    print(report)
    if proc.returncode != 0 or "Conforms: True" not in proc.stdout:
        raise SystemExit(f"Validation failed; see {VALIDATION_PATH}")
    print(
        f"Wrote {OUT_PATH.name} ({len(MESSAGES)} transcript messages); "
        f"source={SOURCE_PATH.name}"
    )
    return OUT_PATH


if __name__ == "__main__":
    build()
