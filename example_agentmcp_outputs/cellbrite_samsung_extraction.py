from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.tool import Tool
from case_uco.uco.identity import Identity
from case_uco.uco.location import Location, LatLongCoordinatesFacet
from case_uco.uco.observable import (
    ObservableObject,
    DeviceFacet,
    OperatingSystemFacet,
    ApplicationFacet,
    AccountFacet,
    PhoneAccountFacet,
    MessageFacet,
    GeoLocationEntryFacet,
    ContentDataFacet,
    SoftwareFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime

graph = CASEGraph()

# --- Investigation ---
investigation = graph.create(Investigation,
    name="Case 2026-0142",
    description=["Cellebrite extraction of suspect Samsung Galaxy — WhatsApp and GPS analysis"],
)

# --- Examiner ---
examiner = graph.create(Identity, name="Det. Marcus Rivera, CCME")

# --- Tool: Cellebrite UFED ---
cellebrite = graph.create(Tool,
    name="Cellebrite UFED",
    version="7.70",
    tool_type="Mobile Forensic Extraction",
)

# --- Manufacturer identity (DeviceFacet.manufacturer expects Identity) ---
samsung = graph.create(Identity, name="Samsung")

# --- The Samsung Galaxy device ---
phone = graph.create(ObservableObject,
    has_facet=[
        DeviceFacet(
            manufacturer=samsung,
            model="Galaxy S24 Ultra",
            serial_number="R5CX30ABCDEF",
            device_type="Mobile Phone",
        ),
        OperatingSystemFacet(),
        SoftwareFacet(version="15"),
    ],
)

# --- Investigative action: the extraction itself ---
extraction = graph.create(InvestigativeAction,
    name="Cellebrite full filesystem extraction",
    description=["Full file system extraction of Samsung Galaxy S24 Ultra using Cellebrite UFED 7.70"],
    start_time=datetime(2026, 3, 20, 9, 15, 0),
    end_time=datetime(2026, 3, 20, 10, 42, 0),
)

# --- Extraction image hash ---
extraction_image = graph.create(ObservableObject,
    has_facet=[ContentDataFacet(
        hash=[Hash(
            hash_method=["SHA256"],
            hash_value="e3b0c44298fc1c149afb4c8996fb92427ae41e4649b934ca495991b7852b855d",
        )],
        size_in_bytes=58_720_256_000,
        mime_type=["application/octet-stream"],
    )],
)

# --- WhatsApp application ---
whatsapp = graph.create(ObservableObject,
    name="WhatsApp Messenger",
    has_facet=[ApplicationFacet(
        application_identifier="com.whatsapp",
        version="2.26.3.14",
    )],
)

# --- WhatsApp accounts (sender & recipient) ---
suspect_account = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(
            account_identifier="+15551234567",
            account_type=["WhatsApp"],
            is_active=True,
        ),
        PhoneAccountFacet(phone_number="+15551234567"),
    ],
)

contact_account = graph.create(ObservableObject,
    has_facet=[
        AccountFacet(
            account_identifier="+15559876543",
            account_type=["WhatsApp"],
            is_active=True,
        ),
        PhoneAccountFacet(phone_number="+15559876543"),
    ],
)

# --- WhatsApp messages ---
msg1 = graph.create(ObservableObject,
    has_facet=[MessageFacet(
        application=whatsapp,
        message_type="Chat",
        message_text="Meet me at the warehouse at 9pm",
        sent_time=datetime(2026, 3, 18, 20, 14, 33),
        from_=suspect_account,
        to=[contact_account],
        message_id="3EB0A7B2D1C4E5F6A8901234",
    )],
)

msg2 = graph.create(ObservableObject,
    has_facet=[MessageFacet(
        application=whatsapp,
        message_type="Chat",
        message_text="I'm here. Back entrance is open.",
        sent_time=datetime(2026, 3, 18, 21, 2, 17),
        from_=contact_account,
        to=[suspect_account],
        message_id="3EB0A7B2D1C4E5F6A8905678",
    )],
)

msg3 = graph.create(ObservableObject,
    has_facet=[MessageFacet(
        application=whatsapp,
        message_type="Chat",
        message_text="Package secured. Heading out now.",
        sent_time=datetime(2026, 3, 18, 21, 47, 5),
        from_=suspect_account,
        to=[contact_account],
        message_id="3EB0A7B2D1C4E5F6A8909012",
    )],
)

# --- GPS locations ---
location_warehouse = graph.create(Location,
    name="Warehouse location",
    has_facet=[LatLongCoordinatesFacet(
        latitude=34.0522,
        longitude=-118.2437,
        altitude=89.0,
    )],
)

location_departure = graph.create(Location,
    name="Departure point",
    has_facet=[LatLongCoordinatesFacet(
        latitude=34.0548,
        longitude=-118.2401,
        altitude=95.0,
    )],
)

# --- GPS entries from the device, tied to timestamps ---
gps_entry1 = graph.create(ObservableObject,
    has_facet=[GeoLocationEntryFacet(
        location=location_warehouse,
        observable_created_time=datetime(2026, 3, 18, 20, 58, 12),
    )],
)

gps_entry2 = graph.create(ObservableObject,
    has_facet=[GeoLocationEntryFacet(
        location=location_departure,
        observable_created_time=datetime(2026, 3, 18, 21, 52, 30),
    )],
)

# --- Provenance: link extraction to all produced artifacts ---
provenance = graph.create(ProvenanceRecord,
    name="Cellebrite extraction results",
    description=["Artifacts produced by Cellebrite UFED extraction of Samsung Galaxy S24 Ultra"],
    exhibit_number="EXH-2026-0142-001",
    object=[
        extraction_image, whatsapp, suspect_account, contact_account,
        msg1, msg2, msg3, gps_entry1, gps_entry2,
    ],
)

graph.write("cellebrite_samsung_extraction.jsonld")
print(f"Graph written: {len(graph)} objects")
print(graph.serialize())