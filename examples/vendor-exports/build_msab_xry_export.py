#!/usr/bin/env python3
"""Build a validated CASE/UCO graph from an MSAB XRY / XAMN export.

Structural exemplar for docs/recipes/msab-xry-export.md.

XRY differs from UFED and AXIOM in one way that shapes the whole graph: the
``.xry`` container is proprietary, forensically sealed, and optionally
encrypted, and MSAB does not publish the XAMN **Extended XML** schema. There
is therefore no community parser and no public element vocabulary to key a
mapping on. Everything modelled here is derived from artifacts that are
observable without the schema:

* the sealed container itself (a file, with a digest and an encryption flag)
* the tool chain that produced it (XRY -> XAMN / XEC Export)
* the device and SIM identifiers XRY reports in every extraction
* XAMN's documented **content categories**, one CASE class per category

Because no per-artifact source path is available until the schema is in hand,
decoded artifacts are joined to the container with ``Extracted_From`` rather
than the ``Contained_Within`` chain that UFED's ``extraInfo`` and AXIOM's
``Source`` fragment support. Claims that rest on the not-yet-available schema
carry ``epistemic:*`` tags instead of being asserted flatly.

Field values are synthetic; no licensed MSAB output is redistributable.

Validated against CASE 1.4.0 with strict concept coverage.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import (
    Investigation,
    InvestigativeAction,
    ProvenanceRecord,
)
from case_uco.uco.identity import Identity, Organization
from case_uco.uco.location import LatLongCoordinatesFacet, Location
from case_uco.uco.observable import (
    Call,
    CallFacet,
    Contact,
    ContactFacet,
    ContactPhone,
    ContentDataFacet,
    DeviceFacet,
    File,
    FileFacet,
    MessageFacet,
    MobileDeviceFacet,
    MobilePhone,
    ObservableRelationship,
    OperatingSystem,
    PhoneAccount,
    PhoneAccountFacet,
    RasterPicture,
    RasterPictureFacet,
    SIMCard,
    SIMCardFacet,
    SMSMessage,
    SMSMessageFacet,
    SoftwareFacet,
)
from case_uco.uco.tool import AnalyticTool, Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "msab-xry-export.jsonld"
UTC = timezone.utc

# Byte payloads stand in for the sealed container and its export so their
# digests are real rather than invented.
XRY_CONTAINER_BYTES = b"XRY sealed container exemplar payload\n"
EXTENDED_XML_BYTES = b'<?xml version="1.0" encoding="utf-8"?><!-- XAMN Extended XML -->\n'
PICTURE_BYTES = b"\xff\xd8\xff\xe0 xry picture artifact exemplar payload"

# Controlled tags from docs/vocabularies/epistemic-tags.json. They keep the
# schema gap visible in the graph instead of hiding it in prose.
SCHEMA_PENDING = ["epistemic:reported", "epistemic:unattributed"]


def _hashes(payload: bytes) -> list[Hash]:
    return [
        Hash(hash_method="MD5", hash_value=hashlib.md5(payload).hexdigest()),
        Hash(hash_method="SHA256", hash_value=hashlib.sha256(payload).hexdigest()),
    ]


def _add_types(graph: CASEGraph, instance, *extra: str) -> None:
    """Append additional @type CURIEs to an already-created node."""
    obj_id = graph.get_id(instance)
    for obj in graph._objects:
        if obj.get("@id") == obj_id:
            current = obj["@type"]
            types = [current] if isinstance(current, str) else list(current)
            for entry in extra:
                if entry not in types:
                    types.append(entry)
            obj["@type"] = types
            return
    raise KeyError(obj_id)


def build() -> CASEGraph:
    graph = CASEGraph()
    relationships = []

    def relate(source, target, kind, description):
        edge = graph.create(
            ObservableRelationship,
            source=source,
            target=target,
            kind_of_relationship=kind,
            is_directional=True,
            description=[description],
        )
        relationships.append(edge)
        return edge

    msab = graph.create(Organization, name="MSAB")
    samsung = graph.create(Organization, name="Samsung Electronics")
    carrier = graph.create(Organization, name="Example Wireless")
    examiner = graph.create(Identity, name="J. Examiner")

    xry = graph.create(
        Tool,
        name="XRY",
        version="10.11.0",
        tool_type="Extraction",
        creator=msab,
        description=["Acquisition front end; writes the sealed .xry container."],
    )
    xamn = graph.create(
        AnalyticTool,
        name="XAMN Horizon",
        version="7.7.0",
        tool_type="Analysis",
        creator=msab,
        description=[
            "Analysis front end. Opens .xry containers and exports Extended XML, "
            "the only MSAB output shaped for downstream interoperability."
        ],
    )
    xec_export = graph.create(
        Tool,
        name="XEC Export",
        version="7.7.0",
        tool_type="Export",
        creator=msab,
        description=[
            "Batch/service converter for the same Extended XML, used when many "
            ".xry files are processed from a watched folder."
        ],
    )

    # --- the sealed container --------------------------------------------
    xry_container = graph.create(
        File,
        name="Samsung_SM-G991B_2026-05-12.xry",
        description=[
            "Proprietary forensically sealed container with an internal audit "
            "trail. XRY 10.4 and later support configurable 256-bit encryption. "
            "It is recorded as an evidence file; its interior is not modelled "
            "because no public reader exists."
        ],
        has_facet=[
            FileFacet(
                file_name="Samsung_SM-G991B_2026-05-12.xry",
                extension="xry",
                size_in_bytes=len(XRY_CONTAINER_BYTES),
            ),
            ContentDataFacet(
                mime_type="application/octet-stream",
                size_in_bytes=len(XRY_CONTAINER_BYTES),
                is_encrypted=True,
                hash=_hashes(XRY_CONTAINER_BYTES),
            ),
        ],
    )
    extended_xml = graph.create(
        File,
        name="Samsung_SM-G991B_2026-05-12_extended.xml",
        description=[
            "XAMN Extended XML. MSAB distributes the schema through the customer "
            "portal rather than publishing it, so element names are not asserted "
            "here; fill the mapping table in the recipe once the schema is held."
        ],
        tag=SCHEMA_PENDING,
        has_facet=[
            FileFacet(
                file_name="Samsung_SM-G991B_2026-05-12_extended.xml",
                extension="xml",
                size_in_bytes=len(EXTENDED_XML_BYTES),
            ),
            ContentDataFacet(
                mime_type="text/xml",
                size_in_bytes=len(EXTENDED_XML_BYTES),
                hash=_hashes(EXTENDED_XML_BYTES),
            ),
        ],
    )

    extraction = graph.create(
        InvestigativeAction,
        name="XRY logical and file system extraction",
        start_time=datetime(2026, 5, 12, 10, 5, tzinfo=UTC),
        end_time=datetime(2026, 5, 12, 11, 22, tzinfo=UTC),
        instrument=[xry],
        performer=examiner,
        result=[xry_container],
    )
    conversion = graph.create(
        InvestigativeAction,
        name="XAMN Extended XML export",
        description=[
            "XAMN opened the sealed container and wrote Extended XML. XEC Export "
            "performs the same conversion unattended for bulk caseloads."
        ],
        start_time=datetime(2026, 5, 12, 13, 40, tzinfo=UTC),
        end_time=datetime(2026, 5, 12, 13, 46, tzinfo=UTC),
        instrument=[xamn, xec_export],
        performer=examiner,
        object=[xry_container],
        result=[extended_xml],
    )
    container_provenance = graph.create(
        ProvenanceRecord,
        name="Sealed XRY container",
        exhibit_number="EX-2026-0512-01",
        object=[xry_container],
    )
    export_provenance = graph.create(
        ProvenanceRecord,
        name="XAMN Extended XML export",
        exhibit_number="EX-2026-0512-01-A",
        root_exhibit_number="EX-2026-0512-01",
        object=[extended_xml],
    )

    # --- device identifiers XRY reports in every extraction ---------------
    phone = graph.create(
        MobilePhone,
        name="Samsung Galaxy S21 (SM-G991B)",
        has_facet=[
            DeviceFacet(
                manufacturer=samsung,
                model="SM-G991B",
                device_type="Mobile Phone",
                serial_number="R5CTEXAMPLE1",
            ),
            MobileDeviceFacet(imei="356938035643809", network="LTE"),
        ],
    )
    android = graph.create(
        OperatingSystem,
        name="Android 14",
        has_facet=[SoftwareFacet(manufacturer=samsung, version="14")],
    )
    _add_types(graph, android, "uco-observable:Software")
    sim = graph.create(
        SIMCard,
        name="SIM (ICCID 8901260852280054321)",
        has_facet=[
            SIMCardFacet(
                iccid="8901260852280054321",
                imsi="310260000000001",
                carrier=carrier,
                sim_form="Nano SIM",
            )
        ],
    )
    relate(sim, phone, "Contained_Within", "SIM seated in the extracted handset.")
    relate(android, phone, "Contained_Within", "Operating system reported by XRY.")
    relate(
        xry_container,
        phone,
        "Extracted_From",
        "Sealed container produced by extracting this handset.",
    )

    # --- XAMN content categories -> one CASE class per category -----------
    owner_account = graph.create(
        PhoneAccount,
        name="+15555550100",
        has_facet=[PhoneAccountFacet(phone_number="+15555550100")],
    )
    peer_account = graph.create(
        PhoneAccount,
        name="+15555550142",
        has_facet=[PhoneAccountFacet(phone_number="+15555550142")],
    )

    # Content category: Messages
    sms = graph.create(
        SMSMessage,
        name="SMS (inbox)",
        has_facet=[
            MessageFacet(
                from_=peer_account,
                to=[owner_account],
                message_text="Boat is fuelled, leaving at six.",
                message_type="SMS",
                sent_time=datetime(2026, 5, 10, 18, 3, 27, tzinfo=UTC),
            ),
            SMSMessageFacet(is_read=True),
        ],
    )

    # Content category: Calls
    call = graph.create(
        Call,
        name="Call (outgoing)",
        has_facet=[
            CallFacet(
                call_type="Outgoing",
                from_=owner_account,
                to=[peer_account],
                start_time=datetime(2026, 5, 10, 18, 20, tzinfo=UTC),
                end_time=datetime(2026, 5, 10, 18, 23, 41, tzinfo=UTC),
                duration=221,
            )
        ],
    )

    # Content category: Contacts
    contact_number = graph.create(
        ContactPhone,
        contact_phone_number=peer_account,
        contact_phone_scope="mobile",
    )
    contact = graph.create(
        Contact,
        name="Contact",
        has_facet=[
            ContactFacet(
                display_name="R. Delgado",
                first_name="Rosa",
                last_name="Delgado",
                contact_phone=[contact_number],
            )
        ],
    )

    # Content category: Locations
    location = graph.create(
        Location,
        name="Device location fix",
        has_facet=[LatLongCoordinatesFacet(latitude=38.9784, longitude=-76.4922)],
    )

    # Content category: Pictures / Files
    picture = graph.create(
        RasterPicture,
        name="20260510_181144.jpg",
        has_facet=[
            FileFacet(
                file_name="20260510_181144.jpg",
                file_path="/storage/emulated/0/DCIM/Camera/20260510_181144.jpg",
                extension="jpg",
                size_in_bytes=len(PICTURE_BYTES),
                observable_created_time=datetime(2026, 5, 10, 18, 11, 44, tzinfo=UTC),
            ),
            ContentDataFacet(
                mime_type="image/jpeg",
                size_in_bytes=len(PICTURE_BYTES),
                hash=_hashes(PICTURE_BYTES),
            ),
            RasterPictureFacet(picture_height=3000, picture_width=4000),
        ],
    )

    # Without a documented per-artifact source path, the honest edge is
    # Extracted_From the container rather than a Contained_Within file chain.
    for artifact in (sms, call, contact, picture):
        relate(
            artifact,
            xry_container,
            "Extracted_From",
            "Decoded from the sealed container; Extended XML does not yet "
            "give a per-artifact source path to build a Contained_Within chain.",
        )

    graph.create(
        Investigation,
        name="MSAB XRY / XAMN export ingest",
        description=[
            "Structural exemplar for docs/recipes/msab-xry-export.md; field values "
            "are synthetic and no Extended XML element names are asserted."
        ],
        investigation_form="case",
        start_time=datetime(2026, 5, 12, 10, 0, tzinfo=UTC),
        object=[
            examiner,
            xry,
            xamn,
            xec_export,
            xry_container,
            extended_xml,
            extraction,
            conversion,
            container_provenance,
            export_provenance,
            phone,
            android,
            sim,
            owner_account,
            peer_account,
            sms,
            call,
            contact,
            location,
            picture,
            *relationships,
        ],
    )
    return graph


def main() -> int:
    build().write(str(OUTPUT))
    try:
        from graph_validator import report_to_dict, validate_graph_file, validator_available
    except ImportError:
        print(f"wrote {OUTPUT} (validator not importable)")
        return 0
    if not validator_available():
        print(f"wrote {OUTPUT} (validator unavailable)", file=sys.stderr)
        return 0
    payload = report_to_dict(
        validate_graph_file(str(OUTPUT), allow_warning=True, strict_concepts=True)
    )
    print(
        json.dumps(
            {
                "conforms": payload.get("conforms"),
                "violation_count": payload.get("violation_count"),
                "undeclared_concepts": payload.get("undeclared_concepts"),
            },
            indent=2,
            default=str,
        )
    )
    return 0 if payload.get("conforms") else 1


if __name__ == "__main__":
    raise SystemExit(main())
