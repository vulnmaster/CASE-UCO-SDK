#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Monico Erich Gastelo government trial brief.

Source: PACER Document 107, Case 1:20-cr-00252-JLT-BAM (E.D. Cal.), filed 2025-05-14.
Recipes applied:
  - cac-federal-trial-proceedings
  - cac-federal-prosecution-relationships
  - cac-grooming-chat-modeling
  - cac-production-case
  - cac-csam-forensic-provenance
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "mcp_server"))

from case_uco.graph import canonical_hex_binary
from graph_validator import load_extension_ontology_paths, validate_graph_file, validator_available

CASE_ID = "gastelo-edcal-2025-trial-brief"
NS = f"https://example.org/cac/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "gastelo-edcal-2025-trial-brief.jsonld"
MCP_EXTRACTION = Path(__file__).resolve().parent / "case-uco-mcp-output.jsonld"
SOURCE_PDF = "pacer -- doj_ceos_2025_014 -- trial brief.pdf"
SOURCE_SHA256 = "90C0B1A245FFBB4BE43761460D12B5DA1138C47F3FF0F0A88C9AC0A420F43A67"
PACER_DOCKET = "1:20-cr-00252-JLT-BAM"
PACER_DOC = "107"
TRIAL_DATE = "2025-05-28"


def lit(dtype: str, value: str | int | bool) -> dict:
    if isinstance(value, bool):
        rendered = str(value).lower()
    else:
        rendered = str(value)
    if dtype == "xsd:hexBinary":
        rendered = canonical_hex_binary(rendered)
    return {"@type": dtype, "@value": rendered}


def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def rel(source: str, target: str, kind: str, directional: bool = True) -> dict:
    return {
        "@id": uid(f"rel-{source}-{target}-{kind}"),
        "@type": "uco-core:Relationship",
        "uco-core:source": [{"@id": source}],
        "uco-core:target": [{"@id": target}],
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": lit("xsd:boolean", directional),
    }


def platform_account(label: str, platform: str, identifier: str, description: str) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": f"{platform} — {identifier}",
        "uco-core:description": description,
        "uco-core:hasFacet": [
            {
                "@id": uid(f"{label}-facet"),
                "@type": "uco-observable:AccountFacet",
                "uco-observable:accountIdentifier": identifier,
            }
        ],
    }


def build_graph() -> dict:
    inv = uid("investigation")
    defendant = uid("defendant-gastelo")
    prosecution = uid("federal-prosecution")
    pretrial = uid("pretrial-phase")
    trial_phase = uid("trial-phase")
    indictment = uid("grand-jury-indictment")
    complaint = uid("criminal-complaint-2020")
    charge1 = uid("federal-charge-1")
    charge2 = uid("federal-charge-2")
    mv1 = uid("minor-victim-1")
    trial_brief = uid("government-trial-brief-doc107")
    brief_filing = uid("action-trial-brief-filing")
    forfeiture = uid("asset-forfeiture-allegation")
    incident_mv1 = uid("csam-incident-mv1-production")
    incident_receipt = uid("csam-incident-receipt-distribution")
    grooming_grindr = uid("grooming-grindr-catfish")
    grooming_mv1_kik = uid("grooming-mv1-kik-snapchat")
    phone_note8 = uid("device-samsung-galaxy-note-8")
    phone_samsung = uid("device-samsung-cellular-phone")
    search_warrants = uid("action-search-warrants")
    forensic_kalar = uid("action-forensic-examination-kalar")
    hsi_fresno = uid("org-hsi-fresno")
    fresno_pd = uid("org-fresno-pd")
    fresno_sheriff = uid("org-fresno-county-sheriff")
    ceos = uid("org-ceos")
    usao_fresno = uid("org-usao-fresno")
    court_edcal = uid("location-ed-california")
    fresno_county = uid("location-fresno-county")
    judge = uid("judge-coughenour")
    ceos_attorney = uid("ceos-attorney-hightower")
    ausa_gappa = uid("ausa-gappa")
    acting_usa = uid("acting-usa-beckwith")
    therapy_dog_request = uid("accommodation-therapy-dog-mv1")
    expert_kalar = uid("expert-kalar")
    source_doc = uid("source-pacer-pdf")
    provenance = uid("provenance-pacer-extraction")
    meh_persona = uid("meh-unified-persona")
    account_erichmg = uid("account-erichmg")
    account_meh_eh = uid("account-meh-eh-telegram")
    account_grindr = uid("account-grindr-catfish")
    evidentiary_404b = uid("evidentiary-404b-grindr")
    prosecutor_role_hightower = uid("prosecutor-role-hightower")
    prosecutor_role_gappa = uid("prosecutor-role-gappa")
    prosecutor_role_beckwith = uid("prosecutor-role-beckwith")
    judge_role = uid("judge-role-coughenour")

    graph: list[dict] = [
        {
            "@id": inv,
            "@type": ["case-investigation:Investigation", "cacontology:CACInvestigation"],
            "uco-core:name": "U.S. v. Monico Erich Gastelo — CEOS Trial Brief Case",
            "uco-core:description": (
                "Federal child exploitation prosecution in E.D. California; government trial brief "
                f"filed 2025-05-14 for jury trial scheduled {TRIAL_DATE} (ALLEGED conduct in brief)."
            ),
            "cacontology:caseNumber": PACER_DOCKET,
            "cacontology:investigationStatus": "Trial Scheduled",
            "cacontology:jurisdiction": "Eastern District of California",
            "cacontology:located_at": {"@id": court_edcal},
            "cacontology:hasPhase": [{"@id": pretrial}, {"@id": trial_phase}],
            "uco-core:object": [
                {"@id": indictment},
                {"@id": prosecution},
                {"@id": charge1},
                {"@id": charge2},
                {"@id": trial_brief},
                {"@id": incident_mv1},
                {"@id": incident_receipt},
                {"@id": source_doc},
            ],
        },
        {
            "@id": defendant,
            "@type": ["uco-identity:Person", "cacontology:Subject", "uco-core:UcoObject"],
            "uco-core:name": "Monico Erich Gastelo",
            "uco-core:description": (
                "Defendant; Fresno County employee per trial brief factual background (ALLEGED). "
                "Joint statement of case also spells first name 'Monaco' — likely typographical variant."
            ),
            "cacontology-legal-outcomes:chargedWith": [{"@id": charge1}, {"@id": charge2}],
        },
        {
            "@id": prosecution,
            "@type": ["cacontology-legal-outcomes:FederalProsecution", "uco-core:UcoObject"],
            "uco-core:name": "Federal Prosecution — U.S. v. Gastelo",
            "cacontology-legal-outcomes:hasLegalPhase": [{"@id": pretrial}, {"@id": trial_phase}],
        },
        {
            "@id": pretrial,
            "@type": ["cacontology-legal-outcomes:PreTrialPhase", "uco-core:UcoObject"],
            "uco-core:name": "Pre-Trial Phase",
            "cacontology-legal-outcomes:phaseStatus": "discovery_and_motions_complete",
            "uco-core:description": (
                "Complaint Dec 8 2020; indictment Dec 10 2020; protective order Dec 18 2020 (Dkt 14); "
                "1647+ pages Bates discovery per brief."
            ),
        },
        {
            "@id": trial_phase,
            "@type": ["cacontology-legal-outcomes:TrialPhase", "uco-core:UcoObject"],
            "uco-core:name": "Trial Phase",
            "uco-core:description": (
                f"Jury trial scheduled May 28, 2025 at 8:30 a.m. before Judge John C. Coughenour; "
                "government estimates two full trial days."
            ),
            "uco-action:startTime": lit("xsd:dateTime", f"{TRIAL_DATE}T08:30:00-07:00"),
        },
        {
            "@id": complaint,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Criminal Complaint (Dkt 1, Dec 8 2020)",
            "uco-core:description": (
                "Initial complaint; defendant initial appearance in custody Dec 9 2020; "
                "released on conditions same day (Dkt 6, 7)."
            ),
        },
        {
            "@id": indictment,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Grand Jury Indictment (Dkt 9, Dec 10 2020)",
            "uco-core:description": (
                "Single-defendant two-count grand jury indictment with forfeiture allegation; "
                "returned Dec 10 2020."
            ),
            "uco-core:tag": ["charging-instrument:grand-jury-indictment"],
            "cacontology:indictmentCounts": lit("xsd:nonNegativeInteger", 2),
        },
        {
            "@id": meh_persona,
            "@type": ["uco-identity:Identity", "uco-core:UcoObject"],
            "uco-core:name": "Meh / Meh Eh / meheh / erichmg (unified screen identities)",
            "uco-core:description": (
                "Interchangeable screen names Meh, Meh Eh, meheh, and erichmg used across Kik, "
                "Snapchat, Telegram, and Wickr; controlled by defendant per trial brief (ALLEGED)."
            ),
        },
        {
            "@id": evidentiary_404b,
            "@type": ["uco-core:UcoObject"],
            "uco-core:name": "FRE 404(b) / Inextricably Intertwined Grindr Evidence",
            "uco-core:description": (
                "Government notice that Grindr catfish activity (Jan–Oct 2019) is offered as "
                "inextricably intertwined with Count Two or alternatively under FRE 404(b) for "
                "intent, motive, preparation, plan, and lack of mistake regarding Counts One and Two "
                "(ALLEGED)."
            ),
            "uco-core:tag": ["evidentiary-issue:404b", "evidentiary-issue:inextricably-intertwined"],
        },
        {
            "@id": charge1,
            "@type": ["cacontology-legal-outcomes:FederalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count One — Production and Attempt (18 U.S.C. §§ 2251(a), (e))",
            "uco-core:description": (
                "Actual and attempted sexual exploitation of children, at least March 2020 through "
                "May 2020 (ALLEGED)."
            ),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 1),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. §§ 2251(a), (e)",
        },
        {
            "@id": charge2,
            "@type": ["cacontology-legal-outcomes:FederalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count Two — Receipt/Distribution (18 U.S.C. § 2252(a)(2), (b)(1))",
            "uco-core:description": (
                "Receipt and distribution of visual depictions of minors, approximately January 2019 "
                "through May 2020 (ALLEGED)."
            ),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 2),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. § 2252(a)(2), (b)(1)",
        },
        {
            "@id": mv1,
            "@type": ["uco-identity:Person", "cacontology-grooming:ChildVictim", "uco-core:UcoObject"],
            "uco-core:name": "Minor Victim 1 (MV1)",
            "uco-core:description": (
                "Twelve-year-old minor victim per interview; exploited via Omegle, Kik, and Snapchat "
                "May 2020 (ALLEGED)."
            ),
        },
        {
            "@id": grooming_grindr,
            "@type": [
                "cacontology-grooming:OnlineGrooming",
                "cacontology-grooming:TeenageImpersonationGrooming",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Grindr Catfish Persona (2019)",
            "uco-core:description": (
                "Defendant pretended to be eighteen-year-old boy on Grindr Jan 30–Oct 17 2019; "
                "communicated with seventeen-year-old and solicited explicit images (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "cacontology-grooming:impersonatedRole": "eighteen-year-old boy",
            "cacontology-grooming:rolePlayingTactic": "catfish",
        },
        {
            "@id": grooming_mv1_kik,
            "@type": [
                "cacontology-grooming:OnlineGrooming",
                "cacontology-grooming:SexualSolicitation",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "MV1 Kik/Snapchat Grooming via Meh Persona",
            "uco-core:description": (
                "Kik user Meh / Meh Eh and Snapchat erichmg solicited sexually explicit images from "
                "twelve-year-old MV1 after Omegle contact (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "cacontology-grooming:targetsVictim": {"@id": mv1},
        },
        {
            "@id": incident_mv1,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "MV1 Production Conduct (May 2020)",
            "uco-core:description": (
                "MV1 sent sexually explicit images after repeated requests from Meh persona; "
                "supports Count One (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "uco-core:hasFacet": [
                {
                    "@id": uid("artifact-mv1-images"),
                    "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                    "uco-core:description": (
                        "Sexually explicit images MV1 sent via Snapchat after grooming (ALLEGED; "
                        "non-graphic summary)."
                    ),
                }
            ],
        },
        {
            "@id": incident_receipt,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "CP Receipt and Distribution on Devices",
            "uco-core:description": (
                "Approximately 788 videos and 1,035 images on Samsung cellular phone and 34 videos "
                "and 630 images on Galaxy Note 8; Telegram/Wickr/WhatsApp exchanges (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "uco-core:hasFacet": [
                {
                    "@id": uid("artifact-cp-inventory"),
                    "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                    "uco-core:description": (
                        "Suspected CSAM inventory counts from forensic review per trial brief (ALLEGED)."
                    ),
                }
            ],
        },
        platform_account(
            "account-grindr-catfish",
            "Grindr",
            "catfish-18yo-persona",
            "Grindr account used with false eighteen-year-old persona (ALLEGED).",
        ),
        platform_account(
            "account-erichmg",
            "Snapchat",
            "erichmg",
            "Snapchat username linked to defendant and MV1 communications (ALLEGED).",
        ),
        platform_account(
            "account-meh-eh-telegram",
            "Telegram/Kik",
            "Meh Eh / meheh",
            "Screen names Meh Eh, Meh, and meheh on Telegram, Kik, Wickr, Snapchat (ALLEGED).",
        ),
        {
            "@id": phone_note8,
            "@type": [
                "uco-observable:ObservableObject",
                "cacontology-production:MobileRecordingDevice",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Samsung Galaxy Note 8",
            "uco-core:description": (
                "Seized device; Grindr, Telegram Meh Eh activity; ~34 videos and 630 suspected CSAM "
                "images per forensic review (ALLEGED)."
            ),
        },
        {
            "@id": phone_samsung,
            "@type": [
                "uco-observable:ObservableObject",
                "cacontology-production:MobileRecordingDevice",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Samsung Cellular Phone",
            "uco-core:description": (
                "Seized device; WhatsApp CP group, Wickr meheh; ~788 videos and 1,035 suspected CSAM "
                "images (ALLEGED)."
            ),
        },
        {
            "@id": search_warrants,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Search Warrant Device Seizures",
            "uco-core:description": (
                "Defendant devices seized under search warrant authority referenced in trial brief."
            ),
            "uco-action:performer": {"@id": hsi_fresno},
            "uco-action:result": [{"@id": phone_note8}, {"@id": phone_samsung}],
        },
        {
            "@id": forensic_kalar,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Digital Forensic Examination — Kenneth Kalar",
            "uco-core:description": (
                "Fresno County Sheriff forensic report (Bates 1-456) detailing CSAM and artifacts "
                "corroborating MV1 statements (ALLEGED)."
            ),
            "uco-action:performer": {"@id": expert_kalar},
            "uco-action:instrument": [{"@id": phone_note8}, {"@id": phone_samsung}],
            "case-investigation:wasInformedBy": {"@id": search_warrants},
        },
        {
            "@id": forfeiture,
            "@type": ["uco-core:UcoObject"],
            "uco-core:name": "Asset Forfeiture Allegation",
            "uco-core:description": (
                "Indictment forfeiture allegation; U.S. seeks defendant residence and electronic devices "
                "used to commit offenses (Dkt 9, 71, 75) per Rule 32.2 (ALLEGED)."
            ),
        },
        {
            "@id": trial_brief,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "United States's Trial Brief (Document 107)",
            "uco-core:description": (
                "Government trial brief filed 2025-05-14 describing anticipated witnesses, exhibits "
                "(OnCue/Elmo), legal issues, and MV1 therapy-dog accommodation request. "
                "Anticipated facts marked ALLEGED until verdict."
            ),
            "uco-core:externalReference": [
                {
                    "@id": uid("trial-brief-ref"),
                    "@type": "uco-core:ExternalReference",
                    "uco-core:definingContext": "Government Trial Brief",
                    "uco-core:referenceURL": {
                        "@type": "xsd:anyURI",
                        "@value": (
                            f"https://ecf.cacd.uscourts.gov/cgi-bin/show_public_doc?"
                            f"{PACER_DOCKET}-{PACER_DOC}"
                        ),
                    },
                }
            ],
            "uco-core:hasFacet": [
                {
                    "@id": uid("trial-brief-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": SOURCE_PDF,
                    "uco-observable:extension": "pdf",
                }
            ],
        },
        {
            "@id": brief_filing,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Trial Brief Filing (Doc 107)",
            "uco-action:startTime": lit("xsd:dateTime", "2025-05-14T00:00:00-07:00"),
            "uco-action:performer": {"@id": usao_fresno},
            "uco-action:object": {"@id": trial_brief},
            "uco-action:result": {"@id": trial_phase},
        },
        {
            "@id": therapy_dog_request,
            "@type": ["uco-core:UcoObject"],
            "uco-core:name": "Therapy Dog Accommodation for MV1 Testimony",
            "uco-core:description": (
                "U.S. requests goldendoodle (Nikko or North) accompany MV1 at witness stand; "
                "FCDAO animal-assisted therapy team; defense stated no objection (ALLEGED need)."
            ),
            "uco-core:tag": ["trial-accommodation:therapy-dog"],
        },
        {
            "@id": expert_kalar,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Kenneth Kalar",
            "uco-core:description": (
                "Fresno County Sheriff Deputy IV; digital forensic examiner and Rule 702 expert "
                "witness per trial brief."
            ),
        },
        {
            "@id": judge,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "John C. Coughenour",
            "uco-core:description": "Senior United States District Judge presiding over trial.",
        },
        {
            "@id": judge_role,
            "@type": [
                "cacontology-legal-outcomes:JudgeRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Presiding Judge — John C. Coughenour",
        },
        {
            "@id": ceos_attorney,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "McKenzie Hightower",
            "uco-core:description": "DOJ CEOS Trial Attorney on government trial brief.",
        },
        {
            "@id": prosecutor_role_hightower,
            "@type": [
                "cacontology-legal-outcomes:ProsecutorRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Prosecutor — McKenzie Hightower (CEOS Trial Attorney)",
        },
        {
            "@id": ausa_gappa,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "David L. Gappa",
            "uco-core:description": "Assistant United States Attorney, Fresno.",
        },
        {
            "@id": prosecutor_role_gappa,
            "@type": [
                "cacontology-legal-outcomes:ProsecutorRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Prosecutor — David L. Gappa (AUSA)",
        },
        {
            "@id": acting_usa,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Michele Beckwith",
            "uco-core:description": "Acting United States Attorney.",
        },
        {
            "@id": prosecutor_role_beckwith,
            "@type": [
                "cacontology-legal-outcomes:ProsecutorRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Prosecutor — Michele Beckwith (Acting U.S. Attorney)",
        },
        {
            "@id": hsi_fresno,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "HSI Fresno",
            "uco-core:description": "Homeland Security Investigations Fresno office; discovery venue.",
        },
        {
            "@id": fresno_pd,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "Fresno Police Department",
        },
        {
            "@id": fresno_sheriff,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "Fresno County Sheriff's Office",
        },
        {
            "@id": ceos,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "DOJ Child Exploitation and Obscenity Section (CEOS)",
        },
        {
            "@id": usao_fresno,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "U.S. Attorney's Office, Eastern District of California (Fresno)",
        },
        {
            "@id": court_edcal,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "United States District Court, Eastern District of California",
        },
        {
            "@id": fresno_county,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "Fresno County, California",
            "uco-core:description": "Venue where crimes alleged to have occurred in part.",
        },
        {
            "@id": source_doc,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": SOURCE_PDF,
            "uco-core:description": f"PACER trial brief; MCP extraction at {MCP_EXTRACTION.name}.",
            "uco-core:hasFacet": [
                {
                    "@id": uid("source-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": SOURCE_PDF,
                    "uco-observable:extension": "pdf",
                },
                {
                    "@id": uid("source-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        {
                            "@id": uid("source-sha256"),
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": "SHA256",
                            "uco-types:hashValue": lit("xsd:hexBinary", SOURCE_SHA256),
                        }
                    ],
                },
            ],
        },
        {
            "@id": provenance,
            "@type": ["case-investigation:ProvenanceRecord"],
            "uco-core:description": (
                "Trial-brief graph derived from PACER PDF and MCP extraction; anticipated trial "
                "facts described as ALLEGED pending jury verdict."
            ),
            "case-investigation:wasDerivedFrom": {"@id": source_doc},
        },
    ]

    witnesses = [
        ("witness-adriana-sister", "Adriana [REDACTED]", "Minor Victim's Sister"),
        ("witness-cassie-stevens", "Cassie Stevens", "Detective, Fresno Police Department"),
        ("witness-kenneth-kalar", "Kenneth Kalar", "Forensic Analyst, Fresno County Sheriff's Office"),
        ("witness-snapchat", "Snapchat Representative", "Corporate records witness"),
        ("witness-comcast", "Comcast Representative", "Subscriber records witness"),
        ("witness-verizon", "Verizon Representative", "Subscriber records witness"),
        ("witness-mv1", "Minor Victim 1", "Victim witness"),
        ("witness-leandro-father", "Leandro [REDACTED]", "Minor Victim's Father"),
        ("witness-evangelina-mother", "Evangelina [REDACTED]", "Minor Victim's Mother"),
    ]
    witness_ids = []
    for label, name, desc in witnesses:
        wid = uid(label)
        witness_ids.append(wid)
        graph.append(
            {
                "@id": wid,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": name,
                "uco-core:description": f"Anticipated government trial witness — {desc}.",
                "uco-core:tag": ["anticipated-trial-witness"],
            }
        )

    graph.extend(
        [
            rel(inv, prosecution, "Relates_To"),
            rel(prosecution, indictment, "Relates_To"),
            rel(prosecution, trial_brief, "Relates_To"),
            rel(prosecution, trial_phase, "Relates_To"),
            rel(complaint, indictment, "Preceded_By"),
            rel(indictment, charge1, "Relates_To"),
            rel(indictment, charge2, "Relates_To"),
            rel(indictment, forfeiture, "Relates_To"),
            rel(trial_brief, charge1, "anticipates"),
            rel(trial_brief, charge2, "anticipates"),
            rel(trial_brief, mv1, "anticipates"),
            rel(trial_brief, therapy_dog_request, "Relates_To"),
            rel(trial_brief, expert_kalar, "anticipates"),
            rel(trial_brief, evidentiary_404b, "Relates_To"),
            rel(brief_filing, trial_brief, "Filed"),
            rel(evidentiary_404b, grooming_grindr, "Relates_To"),
            rel(evidentiary_404b, charge1, "Relates_To"),
            rel(evidentiary_404b, charge2, "Relates_To"),
            rel(charge1, incident_mv1, "Relates_To"),
            rel(charge1, grooming_mv1_kik, "Relates_To"),
            rel(charge1, mv1, "Relates_To"),
            rel(charge2, incident_receipt, "Relates_To"),
            rel(charge2, grooming_grindr, "Relates_To"),
            rel(charge1, court_edcal, "Relates_To"),
            rel(charge2, court_edcal, "Relates_To"),
            rel(charge1, fresno_county, "Relates_To"),
            rel(defendant, meh_persona, "Controls"),
            rel(defendant, account_grindr, "Controls"),
            rel(defendant, account_erichmg, "Controls"),
            rel(defendant, account_meh_eh, "Controls"),
            rel(meh_persona, account_erichmg, "Associated_With"),
            rel(meh_persona, account_meh_eh, "Associated_With"),
            rel(grooming_mv1_kik, meh_persona, "Relates_To"),
            rel(grooming_mv1_kik, account_erichmg, "Relates_To"),
            rel(grooming_mv1_kik, account_meh_eh, "Relates_To"),
            rel(grooming_grindr, account_grindr, "Relates_To"),
            rel(incident_receipt, phone_note8, "used_equipment"),
            rel(incident_receipt, phone_samsung, "used_equipment"),
            rel(incident_mv1, phone_note8, "used_equipment"),
            rel(forfeiture, phone_note8, "targetedAsset"),
            rel(forfeiture, phone_samsung, "targetedAsset"),
            rel(ceos_attorney, ceos, "Affiliated_With"),
            rel(ausa_gappa, usao_fresno, "Affiliated_With"),
            rel(acting_usa, usao_fresno, "Affiliated_With"),
            rel(ceos_attorney, prosecutor_role_hightower, "has_role"),
            rel(ausa_gappa, prosecutor_role_gappa, "has_role"),
            rel(acting_usa, prosecutor_role_beckwith, "has_role"),
            rel(judge, judge_role, "has_role"),
            rel(prosecution, ceos_attorney, "Relates_To"),
            rel(prosecution, ausa_gappa, "Relates_To"),
            rel(inv, hsi_fresno, "Relates_To"),
            rel(inv, fresno_pd, "Relates_To"),
            rel(trial_phase, judge, "Presided_By"),
            rel(trial_phase, judge_role, "Relates_To"),
            rel(provenance, source_doc, "Derived_From"),
        ]
    )
    for wid in witness_ids:
        graph.append(rel(trial_brief, wid, "anticipates"))

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "cacontology": "https://cacontology.projectvic.org#",
            "cac-core": "https://cacontology.projectvic.org/core#",
            "cacontology-grooming": "https://cacontology.projectvic.org/grooming#",
            "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
            "cacontology-production": "https://cacontology.projectvic.org/production#",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    report = validate_graph_file(path, extensions=["cac"], project_root=ROOT)
    print(report.safe_summary)
    paths = load_extension_ontology_paths("cac", mode="subset", project_root=ROOT)
    print(f"Validated with {len(paths)} CAC subset ontology files")
    return 0 if report.conforms else 1


def main() -> int:
    payload = build_graph()
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
