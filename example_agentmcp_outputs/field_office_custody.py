from case_uco import CASEGraph
from case_uco.case.investigation import (
    Investigation, InvestigativeAction, ProvenanceRecord,
)
from case_uco.uco.identity import Identity
from case_uco.uco.tool import Tool
from case_uco.uco.location import Location, SimpleAddressFacet
from case_uco.uco.observable import (
    ObservableObject, DeviceFacet, ContentDataFacet, FileFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=-6))  # CST
graph = CASEGraph()

# --- Investigation ---
investigation = graph.create(Investigation,
    name="Case 2026-1142",
    description=["Financial fraud investigation — digital evidence received "
                  "from Kansas City field office"],
)

# --- People in the custody chain ---
field_agent = graph.create(Identity, name="SA Marcus Ellison")
evidence_custodian = graph.create(Identity, name="Evidence Custodian Janet Reeves")
courier = graph.create(Identity, name="Secure Transport Spc. David Okonkwo")
lab_analyst = graph.create(Identity, name="Digital Forensic Analyst Dr. Leah Nguyen, GCFE")

# --- Locations ---
field_office = graph.create(Location,
    name="Kansas City Field Office",
    has_facet=[SimpleAddressFacet(
        street="1300 Summit Street",
        locality="Kansas City",
        region="MO",
        postal_code="64105",
        country="US",
        address_type="business",
    )],
)

regional_lab = graph.create(Location,
    name="Central Region Digital Forensics Laboratory",
    has_facet=[SimpleAddressFacet(
        street="2501 Investigation Parkway",
        locality="Denver",
        region="CO",
        postal_code="80202",
        country="US",
        address_type="business",
    )],
)

# --- Manufacturers ---
western_digital = graph.create(Identity, name="Western Digital")
apple = graph.create(Identity, name="Apple")

# --- Evidence items ---
external_hdd = graph.create(ObservableObject,
    name="Seized external hard drive",
    has_facet=[DeviceFacet(
        manufacturer=western_digital,
        model="My Passport Ultra 4TB",
        serial_number="WXA1E84P7NK2",
        device_type="External Hard Drive",
    )],
)

iphone = graph.create(ObservableObject,
    name="Suspect iPhone",
    has_facet=[DeviceFacet(
        manufacturer=apple,
        model="iPhone 15 Pro",
        serial_number="F4GDR8Q1PH",
        device_type="Mobile Phone",
    )],
)

# === Custody event 1: Collection at field office ===
collection = graph.create(InvestigativeAction,
    name="Evidence collection",
    description=["External HDD and iPhone seized during execution of search warrant "
                  "at suspect residence, transported to Kansas City field office. "
                  "Items placed in tamper-evident bag TEB-KC-004417."],
    start_time=datetime(2026, 3, 18, 9, 15, 0, tzinfo=tz),
    end_time=datetime(2026, 3, 18, 9, 52, 0, tzinfo=tz),
    performer=field_agent,
    object=[external_hdd, iphone],
    location=[field_office],
)

# === Custody event 2: Forensic imaging at field office ===
imaging_tool = graph.create(Tool,
    name="FTK Imager", version="4.7.3", tool_type="Imaging Utility",
)

hdd_image = graph.create(ObservableObject,
    name="External HDD forensic image",
    has_facet=[
        FileFacet(
            file_name="WXA1E84P7NK2.E01",
            size_in_bytes=3_841_982_464_000,
        ),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"],
            hash_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )]),
    ],
)

iphone_extraction = graph.create(ObservableObject,
    name="iPhone logical extraction",
    has_facet=[
        FileFacet(
            file_name="F4GDR8Q1PH_logical.zip",
            size_in_bytes=48_290_217_984,
        ),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"],
            hash_value="a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
        )]),
    ],
)

imaging = graph.create(InvestigativeAction,
    name="Forensic imaging and hashing",
    description=["E01 image created for external HDD, logical extraction performed "
                  "on iPhone using FTK Imager 4.7.3. SHA-256 hashes computed for "
                  "both forensic images."],
    start_time=datetime(2026, 3, 18, 10, 30, 0, tzinfo=tz),
    end_time=datetime(2026, 3, 18, 14, 45, 0, tzinfo=tz),
    performer=evidence_custodian,
    object=[external_hdd, iphone],
    result=[hdd_image, iphone_extraction],
    instrument=[imaging_tool],
    location=[field_office],
)

# === Custody event 3: Release from field office ===
release = graph.create(InvestigativeAction,
    name="Custody release",
    description=["Evidence released from Kansas City field office evidence room "
                  "to secure transport. Tamper-evident bag TEB-KC-004417 verified "
                  "intact, seal unbroken. Forensic images transferred on encrypted "
                  "transport drive."],
    start_time=datetime(2026, 3, 19, 7, 0, 0, tzinfo=tz),
    end_time=datetime(2026, 3, 19, 7, 20, 0, tzinfo=tz),
    performer=evidence_custodian,
    participant=[courier],
    object=[external_hdd, iphone],
    location=[field_office],
)

# === Custody event 4: Receipt at forensic lab ===
receipt = graph.create(InvestigativeAction,
    name="Custody receipt",
    description=["Evidence received at Central Region Digital Forensics Laboratory. "
                  "Tamper-evident bag TEB-KC-004417 inspected — seal intact, no signs "
                  "of tampering. Items logged into lab evidence management system."],
    start_time=datetime(2026, 3, 19, 15, 10, 0, tzinfo=tz),
    end_time=datetime(2026, 3, 19, 15, 35, 0, tzinfo=tz),
    performer=lab_analyst,
    participant=[courier],
    object=[external_hdd, iphone],
    location=[regional_lab],
)

# === Custody event 5: Hash verification at lab ===
hash_tool = graph.create(Tool,
    name="hashdeep", version="4.4", tool_type="Hashing Utility",
)

hdd_verify_hash = graph.create(ObservableObject,
    name="HDD image verification hash",
    has_facet=[ContentDataFacet(hash=[Hash(
        hash_method=["SHA256"],
        hash_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )])],
)

iphone_verify_hash = graph.create(ObservableObject,
    name="iPhone extraction verification hash",
    has_facet=[ContentDataFacet(hash=[Hash(
        hash_method=["SHA256"],
        hash_value="a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
    )])],
)

verification = graph.create(InvestigativeAction,
    name="Intake hash verification",
    description=["SHA-256 hashes recomputed for both forensic images using hashdeep 4.4 "
                  "and confirmed matching values recorded at Kansas City field office."],
    start_time=datetime(2026, 3, 19, 16, 0, 0, tzinfo=tz),
    end_time=datetime(2026, 3, 19, 16, 48, 0, tzinfo=tz),
    performer=lab_analyst,
    object=[hdd_image, iphone_extraction],
    result=[hdd_verify_hash, iphone_verify_hash],
    instrument=[hash_tool],
    location=[regional_lab],
)

# === Custody event 6: Evidence storage in lab vault ===
storage = graph.create(InvestigativeAction,
    name="Evidence storage",
    description=["Physical evidence and transport drive secured in lab evidence vault, "
                  "locker DFL-V12-B, shelf 3. Access log entry DFL-2026-0319-008 created."],
    start_time=datetime(2026, 3, 19, 17, 0, 0, tzinfo=tz),
    end_time=datetime(2026, 3, 19, 17, 15, 0, tzinfo=tz),
    performer=lab_analyst,
    object=[external_hdd, iphone],
    location=[regional_lab],
)

# === Provenance records — one per evidence item ===
hdd_provenance = graph.create(ProvenanceRecord,
    name="External HDD chain of custody",
    description=["Full custody record for Western Digital My Passport Ultra 4TB "
                  "(S/N WXA1E84P7NK2) — seizure at suspect residence through "
                  "intake and storage at Central Region forensic lab"],
    exhibit_number="EXH-2026-1142-001",
    object=[external_hdd, hdd_image, hdd_verify_hash,
            collection, imaging, release, receipt, verification, storage],
)

iphone_provenance = graph.create(ProvenanceRecord,
    name="iPhone chain of custody",
    description=["Full custody record for Apple iPhone 15 Pro "
                  "(S/N F4GDR8Q1PH) — seizure at suspect residence through "
                  "intake and storage at Central Region forensic lab"],
    exhibit_number="EXH-2026-1142-002",
    object=[iphone, iphone_extraction, iphone_verify_hash,
            collection, imaging, release, receipt, verification, storage],
)

graph.write("field_office_custody.jsonld")
print(f"Graph written: {len(graph)} objects")
