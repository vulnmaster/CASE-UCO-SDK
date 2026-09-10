#!/usr/bin/env python3
"""Build a validated CASE/UCO graph from a Magnet AXIOM Examine XML export.

Structural exemplar for docs/recipes/magnet-axiom-export.md. AXIOM's export
vocabulary is three nested elements, and each one maps to a distinct part of
the graph:

* ``<Artifact name="...">``  -> the artifact family, which selects the facet set
* ``<Hit>``                  -> one observable per hit
* ``<Fragment name="...">``  -> one property per fragment

Three fragments appear on nearly every artifact and carry the investigative
spine rather than artifact content:

* ``Source``          -> the file the hit was recovered from (Contained_Within)
* ``Location``        -> the offset/path within that source
* ``Recovery method`` -> "Parsing" (allocated) vs "Carving" (RecoveredObjectFacet)

Field *values* are synthetic (no licensed Magnet output is redistributable),
but every element, artifact name, and fragment name reproduced in the recipe
is real. Hash values are computed over byte payloads this builder defines.

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
    BrowserCookie,
    BrowserCookieFacet,
    CellSite,
    CellSiteFacet,
    ContentDataFacet,
    DeviceFacet,
    DomainName,
    DomainNameFacet,
    EXIFFacet,
    File,
    FileFacet,
    FileSystem,
    FileSystemFacet,
    Message,
    MessageFacet,
    MobileDeviceFacet,
    MobilePhone,
    ObservableRelationship,
    OperatingSystem,
    PhoneAccount,
    PhoneAccountFacet,
    RasterPicture,
    RasterPictureFacet,
    RecoveredObjectFacet,
    SoftwareFacet,
    URL,
    URLFacet,
    URLHistory,
    URLHistoryEntry,
    URLHistoryFacet,
)
from case_uco.uco.tool import AnalyticTool, Tool
from case_uco.uco.types import ControlledDictionary, ControlledDictionaryEntry, Hash

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "magnet-axiom-export.jsonld"
UTC = timezone.utc

# Byte payloads stand in for the exported artifacts so their digests are real
# rather than invented. A live run hashes the bytes AXIOM exported.
XML_EXPORT_BYTES = b'<?xml version="1.0" encoding="utf-8"?><Artifacts/>\n'
PICTURE_BYTES = b"\xff\xd8\xff\xe1 axiom picture artifact exemplar payload"
CHAT_DB_BYTES = b"SQLite format 3\x00ChatStorage.sqlite exemplar payload\n"


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

    magnet = graph.create(Organization, name="Magnet Forensics")
    apple = graph.create(Organization, name="Apple Inc.")
    examiner = graph.create(Identity, name="J. Examiner")

    # AXIOM splits into two products; the export names the Examine build.
    axiom_process = graph.create(
        Tool,
        name="Magnet AXIOM Process",
        version="8.4.0.41310",
        tool_type="Acquisition",
        creator=magnet,
    )
    axiom_examine = graph.create(
        AnalyticTool,
        name="Magnet AXIOM Examine",
        version="8.4.0.41310",
        tool_type="Analysis",
        creator=magnet,
        description=[
            "Artifact review and export. The XML export is produced here "
            "(--type Xml | XmlExternalFiles | XmlBase64), not by AXIOM Process."
        ],
    )

    # The acquired image and the AXIOM case folder are separate evidence items
    # from the XML export that this recipe ingests.
    image_file = graph.create(
        File,
        name="iphone-11.e01",
        has_facet=[
            FileFacet(file_name="iphone-11.e01", extension="e01", size_in_bytes=53687091200),
            ContentDataFacet(
                mime_type="application/octet-stream",
                size_in_bytes=53687091200,
                hash=[
                    Hash(
                        hash_method="SHA256",
                        hash_value=hashlib.sha256(b"axiom-image-exemplar").hexdigest(),
                    )
                ],
            ),
        ],
    )
    case_mfdb = graph.create(
        File,
        name="Case.mfdb",
        description=[
            "AXIOM Process case database. Magnet does not publish its schema; "
            "it is recorded as an evidence file, not parsed."
        ],
        has_facet=[
            FileFacet(
                file_name="Case.mfdb",
                file_path="AXIOM_Process/Case.mfdb",
                extension="mfdb",
            )
        ],
    )
    xml_export = graph.create(
        File,
        name="axiom-export.xml",
        has_facet=[
            FileFacet(
                file_name="axiom-export.xml",
                extension="xml",
                size_in_bytes=len(XML_EXPORT_BYTES),
            ),
            ContentDataFacet(
                mime_type="text/xml",
                size_in_bytes=len(XML_EXPORT_BYTES),
                hash=_hashes(XML_EXPORT_BYTES),
            ),
        ],
    )

    acquisition = graph.create(
        InvestigativeAction,
        name="AXIOM Process image acquisition and artifact search",
        start_time=datetime(2026, 4, 6, 8, 30, tzinfo=UTC),
        end_time=datetime(2026, 4, 6, 12, 5, tzinfo=UTC),
        instrument=[axiom_process],
        performer=examiner,
        result=[image_file, case_mfdb],
    )
    export = graph.create(
        InvestigativeAction,
        name="AXIOM Examine XML export (en-US)",
        description=[
            "Export locale is en-US. Artifact and Fragment names are localized, "
            "so a mapping keyed on English names silently drops artifacts from "
            "an export generated in another locale."
        ],
        start_time=datetime(2026, 4, 6, 14, 0, tzinfo=UTC),
        end_time=datetime(2026, 4, 6, 14, 9, tzinfo=UTC),
        instrument=[axiom_examine],
        performer=examiner,
        object=[case_mfdb],
        result=[xml_export],
    )
    provenance = graph.create(
        ProvenanceRecord,
        name="AXIOM XML export",
        exhibit_number="EX-2026-0406-02",
        object=[xml_export],
    )

    # --- Artifact name="iOS Device Information" ---------------------------
    phone = graph.create(
        MobilePhone,
        name="iPhone 11",
        has_facet=[
            DeviceFacet(
                manufacturer=apple,
                model="iPhone12,1",
                device_type="Mobile Phone",
                serial_number="F17EXAMPLE01",  # Fragment name="Serial Number"
            ),
            MobileDeviceFacet(imei="356938035643809", network="LTE"),
        ],
    )
    ios = graph.create(
        OperatingSystem,
        name="iOS 17.4",
        has_facet=[SoftwareFacet(manufacturer=apple, version="17.4")],
    )
    _add_types(graph, ios, "uco-observable:Software")
    relate(ios, phone, "Contained_Within", 'Fragment name="OS Version".')

    # --- Artifact name="File System Information" --------------------------
    filesystem = graph.create(
        FileSystem,
        name="APFS volume",
        has_facet=[FileSystemFacet(file_system_type="APFS", cluster_size=4096)],
    )
    relate(filesystem, image_file, "Contained_Within", 'Fragment name="Volume Offset (Bytes)".')

    # --- Artifact name="Pictures" (FILE_PATTERN family) -------------------
    # Fragment name="Recovery method" == "Parsing" -> allocated, no recovery facet.
    picture = graph.create(
        RasterPicture,
        name="IMG_0442.HEIC",
        has_facet=[
            FileFacet(
                file_name="IMG_0442.HEIC",
                file_path="/private/var/mobile/Media/DCIM/101APPLE/IMG_0442.HEIC",
                extension="HEIC",
                size_in_bytes=len(PICTURE_BYTES),
                observable_created_time=datetime(2026, 3, 29, 17, 41, 2, tzinfo=UTC),
            ),
            ContentDataFacet(
                mime_type="image/heic",
                size_in_bytes=len(PICTURE_BYTES),
                hash=_hashes(PICTURE_BYTES),
            ),
            RasterPictureFacet(picture_height=3024, picture_width=4032),
            # Fragments Make / Model / GPS Latitude / GPS Longitude / Altitude.
            # exifData requires a ControlledDictionary, not a plain Dictionary.
            EXIFFacet(
                exif_data=ControlledDictionary(
                    entry=[
                        ControlledDictionaryEntry(key="Make", value="Apple"),
                        ControlledDictionaryEntry(key="Model", value="iPhone 11"),
                        ControlledDictionaryEntry(key="GPSLatitude", value="38.9784"),
                        ControlledDictionaryEntry(key="GPSLatitudeRef", value="N"),
                        ControlledDictionaryEntry(key="GPSLongitude", value="-76.4922"),
                        ControlledDictionaryEntry(key="GPSLongitudeRef", value="W"),
                        ControlledDictionaryEntry(key="GPSAltitude", value="11"),
                    ]
                )
            ),
        ],
    )
    relate(picture, filesystem, "Contained_Within", 'Fragment name="Source".')

    # GPS fragments become a Location, not extra strings on the picture.
    picture_location = graph.create(
        Location,
        name="EXIF GPS fix for IMG_0442.HEIC",
        has_facet=[
            LatLongCoordinatesFacet(latitude=38.9784, longitude=-76.4922, altitude=11.0)
        ],
    )

    # Fragment name="Recovery method" == "Carving" -> carved, unallocated.
    carved_picture = graph.create(
        RasterPicture,
        name="carved_00417216.jpg",
        has_facet=[
            FileFacet(file_name="carved_00417216.jpg", extension="jpg", size_in_bytes=88214),
            ContentDataFacet(
                mime_type="image/jpeg",
                size_in_bytes=88214,
                hash=[
                    Hash(
                        hash_method="SHA256",
                        hash_value=hashlib.sha256(b"axiom-carved-exemplar").hexdigest(),
                    )
                ],
            ),
            RecoveredObjectFacet(
                content_recovered_status="recovered",
                name_recovered_status="unknown",
            ),
        ],
    )
    relate(
        carved_picture,
        filesystem,
        "Contained_Within",
        'Fragment name="Recovery method" == "Carving"; Location gives the byte offset.',
    )

    # --- Artifact name="iOS WhatsApp Messages" (CHAT_PATTERN) -------------
    whatsapp = graph.create(
        Application,
        name="WhatsApp",
        has_facet=[ApplicationFacet(application_identifier="net.whatsapp.WhatsApp")],
    )
    chat_db = graph.create(
        File,
        name="ChatStorage.sqlite",
        has_facet=[
            FileFacet(
                file_name="ChatStorage.sqlite",
                file_path="/private/var/mobile/Containers/Shared/AppGroup/ChatStorage.sqlite",
                extension="sqlite",
                size_in_bytes=len(CHAT_DB_BYTES),
            ),
            ContentDataFacet(
                mime_type="application/vnd.sqlite3",
                size_in_bytes=len(CHAT_DB_BYTES),
                hash=_hashes(CHAT_DB_BYTES),
            ),
        ],
    )
    sender = graph.create(
        PhoneAccount,
        name="+15555550142",
        has_facet=[PhoneAccountFacet(phone_number="+15555550142")],
    )
    receiver = graph.create(
        PhoneAccount,
        name="+15555550100",
        has_facet=[PhoneAccountFacet(phone_number="+15555550100")],
    )
    message = graph.create(
        Message,
        name="iOS WhatsApp message",
        has_facet=[
            MessageFacet(
                application=whatsapp,
                from_=sender,
                to=[receiver],
                message_text="Pickup moved to the north lot at 4.",
                message_type="Chat",
                # Fragment name="Message Sent Date/Time - UTC+00:00"
                sent_time=datetime(2026, 3, 29, 20, 58, 11, tzinfo=UTC),
            )
        ],
    )
    relate(message, chat_db, "Contained_Within", 'Fragment name="Source".')
    relate(chat_db, filesystem, "Contained_Within", "Artifact source file on the parsed volume.")

    # --- Artifact name="Safari History" (WEB_PATTERN) ---------------------
    # observable:host references a DomainName observable; it is not a string.
    visited_host = graph.create(
        DomainName,
        name="example.org",
        has_facet=[DomainNameFacet(value="example.org")],
    )
    visited_url = graph.create(
        URL,
        name="https://example.org/tides",
        has_facet=[
            URLFacet(
                full_value="https://example.org/tides",
                scheme="https",
                host=visited_host,
                path="/tides",
            )
        ],
    )
    safari = graph.create(
        Application,
        name="Safari",
        has_facet=[ApplicationFacet(application_identifier="com.apple.mobilesafari")],
    )
    history = graph.create(
        URLHistory,
        name="Safari History hits",
        has_facet=[
            URLHistoryFacet(
                browser_information=safari,
                url_history_entry=[
                    URLHistoryEntry(
                        url=visited_url,
                        page_title="Marina tide chart",  # Fragment name="Title"
                        visit_count=3,  # Fragment name="Visit Count"
                        last_visit=datetime(2026, 3, 28, 14, 22, tzinfo=UTC),
                    )
                ],
            )
        ],
    )

    # --- Artifact name="Chrome Cookies" (COOKIE_PATTERN) ------------------
    cookie = graph.create(
        BrowserCookie,
        name="__Secure-1PSID",
        has_facet=[
            BrowserCookieFacet(
                cookie_name="__Secure-1PSID",
                cookie_domain=visited_url,
                cookie_path="/",
                accessed_time=datetime(2026, 3, 28, 14, 22, 5, tzinfo=UTC),
                expiration_time=datetime(2027, 3, 28, 14, 22, 5, tzinfo=UTC),
                is_secure=True,
            )
        ],
    )

    # --- Artifact name="Cell Tower Locations" (CELL_TOWER_PATTERN) --------
    cell_site = graph.create(
        CellSite,
        name="LTE cell 21451",
        has_facet=[
            CellSiteFacet(
                cell_site_identifier="21451",
                cell_site_location_area_code="4102",
                cell_site_country_code="310",
                cell_site_network_code="260",
                cell_site_type="LTE",
            )
        ],
    )
    cell_location = graph.create(
        Location,
        name="Cell tower location",
        has_facet=[LatLongCoordinatesFacet(latitude=38.9721, longitude=-76.5015)],
    )

    graph.create(
        Investigation,
        name="Magnet AXIOM XML export ingest",
        description=[
            "Structural exemplar for docs/recipes/magnet-axiom-export.md; field "
            "values are synthetic, Artifact/Fragment names are from a real export."
        ],
        investigation_form="case",
        start_time=datetime(2026, 4, 6, 8, 0, tzinfo=UTC),
        object=[
            examiner,
            axiom_process,
            axiom_examine,
            image_file,
            case_mfdb,
            xml_export,
            acquisition,
            export,
            provenance,
            phone,
            ios,
            filesystem,
            picture,
            picture_location,
            carved_picture,
            whatsapp,
            chat_db,
            sender,
            receiver,
            message,
            safari,
            visited_host,
            visited_url,
            history,
            cookie,
            cell_site,
            cell_location,
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
