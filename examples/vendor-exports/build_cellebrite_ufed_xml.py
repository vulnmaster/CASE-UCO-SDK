#!/usr/bin/env python3
"""Build a validated CASE/UCO graph from a Cellebrite UFED Physical Analyzer XML report.

Structural exemplar for docs/recipes/cellebrite-ufed-xml.md. Every node here
corresponds to a named construct in a real ``report.xml`` (the XML at the root
of an unzipped ``.ufdr``):

* ``<metadata section="Device Info">`` / ``"Extraction Data"`` -> device, OS, SIM
* ``<caseInformation>`` -> examiner Identity, Investigation
* ``<images><image>`` -> the acquired image file + acquisition action
* ``<taggedFiles><file>`` -> File observables with hashes from
  ``<metadata section="File"><item name="MD5">``
* ``<decodedData><modelType type="..."><model>`` -> one typed observable per model
* ``<extraInfo><nodeInfo>`` -> the Contained_Within chain of evidence that joins
  a decoded artifact back to the file it was decoded from

Field *values* are synthetic (no licensed Cellebrite output is redistributable),
but every element/attribute name reproduced in the recipe is real. Hash values
are computed over byte payloads this builder defines, so no digest is invented.

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
    Application,
    ApplicationFacet,
    BluetoothAddressFacet,
    Call,
    CallFacet,
    Contact,
    ContactFacet,
    ContactPhone,
    ContentDataFacet,
    DeviceFacet,
    File,
    FileFacet,
    Message,
    MessageFacet,
    MobileDeviceFacet,
    MobilePhone,
    ObservableRelationship,
    OperatingSystem,
    PhoneAccount,
    PhoneAccountFacet,
    RecoveredObjectFacet,
    SIMCard,
    SIMCardFacet,
    SoftwareFacet,
    URLHistory,
    URLHistoryEntry,
    URLHistoryFacet,
    WifiAddressFacet,
    WirelessNetworkConnection,
    WirelessNetworkConnectionFacet,
)
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cellebrite-ufed-xml.jsonld"
UTC = timezone.utc

# Byte payloads stand in for the extracted files so their digests are real
# rather than invented. A live run hashes the bytes UFED wrote into the UFDR.
REPORT_XML_BYTES = b'<?xml version="1.0" encoding="utf-8"?><project id="ufed-exemplar"/>\n'
CHAT_DB_BYTES = b"SQLite format 3\x00msgstore.db exemplar payload\n"


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

    # --- caseInformation / vendor identities -----------------------------
    cellebrite = graph.create(Organization, name="Cellebrite DI Ltd.")
    google = graph.create(Organization, name="Google LLC")
    carrier = graph.create(Organization, name="Example Wireless")
    # <caseInformation><field fieldType="ExaminerName">
    examiner = graph.create(Identity, name="J. Examiner")

    # --- <metadata section="Additional Fields"> UFED_PA_Version ----------
    ufed_4pc = graph.create(
        Tool,
        name="UFED 4PC",
        version="7.60.0.114",
        tool_type="Acquisition",
        creator=cellebrite,
    )
    ufed_pa = graph.create(
        Tool,
        name="UFED Physical Analyzer",
        version="7.60.0.114",
        tool_type="Extraction",
        creator=cellebrite,
    )

    # --- <images><image path=... size=...> -------------------------------
    image_file = graph.create(
        File,
        name="Google_G013A Pixel 3.zip",
        has_facet=[
            FileFacet(
                file_name="Google_G013A Pixel 3.zip",
                file_path="Google_G013A Pixel 3.zip",
                extension="zip",
                size_in_bytes=16965760332,
            ),
            ContentDataFacet(
                mime_type="application/zip",
                size_in_bytes=16965760332,
                # <metadata section="Hashes"><item name="SHA256">
                hash=[
                    Hash(
                        hash_method="SHA256",
                        hash_value=hashlib.sha256(b"ufed-image-exemplar").hexdigest(),
                    )
                ],
            ),
        ],
    )

    report_file = graph.create(
        File,
        name="report.xml",
        has_facet=[
            FileFacet(
                file_name="report.xml",
                file_path="/report.xml",
                extension="xml",
                size_in_bytes=len(REPORT_XML_BYTES),
            ),
            ContentDataFacet(
                mime_type="text/xml",
                size_in_bytes=len(REPORT_XML_BYTES),
                hash=_hashes(REPORT_XML_BYTES),
            ),
        ],
    )

    # --- <metadata section="Extraction Data"> ----------------------------
    acquisition = graph.create(
        InvestigativeAction,
        name="UFED physical acquisition of mobile device",
        start_time=datetime(2026, 3, 4, 9, 12, tzinfo=UTC),
        end_time=datetime(2026, 3, 4, 11, 48, tzinfo=UTC),
        instrument=[ufed_4pc],
        performer=examiner,
        result=[image_file],
    )
    decoding = graph.create(
        InvestigativeAction,
        name="UFED Physical Analyzer decode and XML report generation",
        description=[
            "Physical Analyzer parsed the acquisition into decodedData model "
            "instances and serialized report.xml into the UFDR."
        ],
        start_time=datetime(2026, 3, 4, 13, 5, tzinfo=UTC),
        end_time=datetime(2026, 3, 4, 13, 41, tzinfo=UTC),
        instrument=[ufed_pa],
        performer=examiner,
        object=[image_file],
        result=[report_file],
    )
    provenance = graph.create(
        ProvenanceRecord,
        name="UFED XML report",
        exhibit_number="EX-2026-0304-01",
        description=["report.xml extracted from the UFDR container."],
        object=[report_file],
    )

    # --- <metadata section="Device Info"> --------------------------------
    phone = graph.create(
        MobilePhone,
        name="Pixel 3 (DeviceInfoDetectedPhoneModel)",
        has_facet=[
            DeviceFacet(
                manufacturer=google,
                model="Pixel 3",
                device_type="Mobile Phone",
                serial_number="8AEX0EXAMPLE01",
            ),
            MobileDeviceFacet(
                imei="356938035643809",
                bluetooth_device_name="Pixel 3",
                network="LTE",
                storage_capacity_in_bytes=64000000000,
            ),
            # DeviceInfoBluetoothDeviceAddress / DeviceInfoWiFiMACAddress
            BluetoothAddressFacet(address_value="00:1A:7D:DA:71:13"),
            WifiAddressFacet(address_value="3C:5A:B4:00:11:22"),
        ],
    )
    # DeviceInfoOSType / DeviceInfoOSVersion. UCO 2.0.0 moves manufacturer and
    # version off OperatingSystemFacet, so carry them on SoftwareFacet now.
    android = graph.create(
        OperatingSystem,
        name="Android 12",
        has_facet=[SoftwareFacet(manufacturer=google, version="12")],
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
    relate(sim, phone, "Contained_Within", "SIM card seated in the acquired handset.")
    relate(
        android,
        phone,
        "Contained_Within",
        "Operating system reported by DeviceInfoOSType / DeviceInfoOSVersion.",
    )

    # --- <taggedFiles><file> ---------------------------------------------
    # <file deleted="Intact" ...> — an intact file carries no recovery facet.
    chat_db = graph.create(
        File,
        name="msgstore.db",
        has_facet=[
            FileFacet(
                file_name="msgstore.db",
                file_path="/data/data/com.whatsapp/databases/msgstore.db",
                extension="db",
                size_in_bytes=len(CHAT_DB_BYTES),
                modified_time=datetime(2026, 3, 2, 21, 14, 3, tzinfo=UTC),
            ),
            ContentDataFacet(
                mime_type="application/vnd.sqlite3",
                size_in_bytes=len(CHAT_DB_BYTES),
                hash=_hashes(CHAT_DB_BYTES),
            ),
        ],
    )
    relate(
        chat_db,
        image_file,
        "Contained_Within",
        "taggedFiles entry carved from the acquired image.",
    )

    # --- <modelType type="InstalledApplication"> --------------------------
    whatsapp = graph.create(
        Application,
        name="WhatsApp",
        has_facet=[
            ApplicationFacet(
                application_identifier="com.whatsapp",
                version="2.26.3.14",
                operating_system=android,
            )
        ],
    )

    # --- <model type="Party"> participants --------------------------------
    owner_account = graph.create(
        PhoneAccount,
        name="+15550100 (IsPhoneOwner=True)",
        has_facet=[PhoneAccountFacet(phone_number="+15555550100")],
    )
    peer_account = graph.create(
        PhoneAccount,
        name="+15555550142",
        has_facet=[PhoneAccountFacet(phone_number="+15555550142")],
    )

    # --- <modelType type="Chat"> / nested InstantMessage ------------------
    message_in = graph.create(
        Message,
        name="InstantMessage (incoming)",
        has_facet=[
            MessageFacet(
                application=whatsapp,
                from_=peer_account,
                to=[owner_account],
                message_text="Pickup moved to the north lot at 4.",
                message_type="Chat",
                sent_time=datetime(2026, 3, 2, 20, 58, 11, tzinfo=UTC),
            )
        ],
    )
    # <model type="InstantMessage" deleted_state="Deleted">
    message_deleted = graph.create(
        Message,
        name="InstantMessage (deleted_state=Deleted)",
        has_facet=[
            MessageFacet(
                application=whatsapp,
                from_=owner_account,
                to=[peer_account],
                message_text="Understood.",
                message_type="Chat",
                sent_time=datetime(2026, 3, 2, 21, 2, 40, tzinfo=UTC),
            ),
            RecoveredObjectFacet(content_recovered_status="recovered"),
        ],
    )
    for message in (message_in, message_deleted):
        relate(
            message,
            chat_db,
            "Contained_Within",
            "extraInfo/nodeInfo joins this decoded model to its source file.",
        )

    # --- <modelType type="Call"> ------------------------------------------
    call = graph.create(
        Call,
        name="Call (Direction=Incoming)",
        has_facet=[
            CallFacet(
                application=whatsapp,
                call_type="Incoming",
                from_=peer_account,
                to=[owner_account],
                start_time=datetime(2026, 3, 2, 19, 30, tzinfo=UTC),
                end_time=datetime(2026, 3, 2, 19, 34, 12, tzinfo=UTC),
                duration=252,
            )
        ],
    )

    # --- <modelType type="Contact"> / nested PhoneNumber entries ----------
    # observable:contactPhone requires an observable:ContactPhone wrapper, and
    # that wrapper's contactPhoneNumber must reference the account observable
    # rather than repeat the digits as a literal.
    contact_number = graph.create(
        ContactPhone,
        contact_phone_number=peer_account,
        contact_phone_scope="mobile",
    )
    contact = graph.create(
        Contact,
        name="Contact (Name field)",
        has_facet=[
            ContactFacet(
                display_name="R. Delgado",
                first_name="Rosa",
                last_name="Delgado",
                contact_phone=[contact_number],
            )
        ],
    )

    # --- <modelType type="Location"> / nested Coordinate ------------------
    location = graph.create(
        Location,
        name="Location (Category=Significant)",
        has_facet=[LatLongCoordinatesFacet(latitude=38.9784, longitude=-76.4922)],
    )

    # --- <modelType type="WirelessNetwork"> -------------------------------
    wifi = graph.create(
        WirelessNetworkConnection,
        name="WirelessNetwork (SSId/BSSId)",
        has_facet=[WirelessNetworkConnectionFacet(ssid="MarinaGuest")],
    )
    relate(phone, wifi, "Connected_To", "Handset associated with this SSID/BSSID.")

    # --- <modelType type="VisitedPage"> -----------------------------------
    history = graph.create(
        URLHistory,
        name="VisitedPage entries",
        has_facet=[
            URLHistoryFacet(
                browser_information=whatsapp,
                url_history_entry=[
                    URLHistoryEntry(
                        page_title="Marina tide chart",
                        visit_count=3,
                        last_visit=datetime(2026, 3, 1, 14, 22, tzinfo=UTC),
                    )
                ],
            )
        ],
    )

    graph.create(
        Investigation,
        name="Cellebrite UFED XML report ingest",
        description=[
            "Structural exemplar for docs/recipes/cellebrite-ufed-xml.md; "
            "field values are synthetic, element names are from a real report.xml."
        ],
        investigation_form="case",
        start_time=datetime(2026, 3, 4, 9, 0, tzinfo=UTC),
        object=[
            examiner,
            ufed_4pc,
            ufed_pa,
            image_file,
            report_file,
            acquisition,
            decoding,
            provenance,
            phone,
            android,
            sim,
            chat_db,
            whatsapp,
            owner_account,
            peer_account,
            message_in,
            message_deleted,
            call,
            contact,
            location,
            wifi,
            history,
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
