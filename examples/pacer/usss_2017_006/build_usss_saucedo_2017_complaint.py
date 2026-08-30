#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Joseph Daniel Saucedo criminal complaint.

Source: PACER Document 1, Case 3:17-cr-00095-JLS (S.D. Cal.), filed 2016-12-14.
Recipes applied:
  - cac-federal-prosecution-relationships
  - cac-grooming-chat-modeling
  - cac-production-case
  - cac-csam-forensic-provenance
  - cac-multi-jurisdiction-task-force (ECWG / ICAC / international referral)
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

CASE_ID = "usss-saucedo-2017-complaint"
NS = f"https://example.org/cac/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "usss-saucedo-2017-complaint.jsonld"
MCP_EXTRACTION = Path(__file__).resolve().parent / "case-uco-mcp-output.jsonld"
SOURCE_PDF = "pacer -- usss_2017_006 -- Criminal Complaint .pdf"
SOURCE_SHA256 = "140AD442DE74B955C8D51540DF416340B6F757C82E6DCBE08B82783F50EA7985"
PACER_DOCKET = "3:17-cr-00095-JLS"
PACER_DOC = "1"
KIK_USERNAME = "jennings6ger"
FACEBOOK_ID = "100002341282738"


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


def ip_node(label: str, address: str, description: str) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:IPAddress", "uco-core:UcoObject"],
        "uco-core:name": address,
        "uco-core:description": description,
        "uco-core:hasFacet": [
            {
                "@id": uid(f"{label}-facet"),
                "@type": ["uco-observable:IPAddressFacet", "uco-core:Facet"],
                "uco-observable:addressValue": address,
            }
        ],
    }


def csam_artifact(label: str, name: str, description: str) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": name,
        "uco-core:description": f"{description} (ALLEGED; non-graphic summary from complaint tables.)",
        "uco-core:hasFacet": [
            {
                "@id": uid(f"{label}-facet"),
                "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                "uco-core:description": description,
            }
        ],
    }


def build_graph() -> dict:
    inv = uid("investigation")
    defendant = uid("defendant-saucedo")
    offender_role = uid("offender-role-saucedo")
    mv1 = uid("minor-victim-1")
    mv2 = uid("minor-victim-2")
    complaint = uid("criminal-complaint")
    prosecution = uid("federal-prosecution")
    pretrial = uid("pretrial-phase")
    court_sdca = uid("location-sd-california")
    vista = uid("location-vista-ca")
    calgary = uid("location-calgary-ab")
    hsi_ceg = uid("org-hsi-san-diego-ceg")
    ecwg = uid("org-ecwg")
    usss = uid("org-usss")
    calgary_pd = uid("org-calgary-police")
    icac = uid("org-icac-task-force")
    charge1 = uid("federal-charge-1")
    charge2 = uid("federal-charge-2")
    charge3 = uid("federal-charge-3")
    incident_mv1 = uid("csam-incident-mv1-facetime")
    incident_mv2 = uid("csam-incident-mv2-production")
    grooming_mv1 = uid("grooming-mv1-amy-jennings")
    grooming_mv2 = uid("grooming-mv2-modeling-coercion")
    receipt_conduct = uid("receipt-conduct-kik-cp")
    amy_persona = uid("persona-amy-jennings")
    fabricated_teen_role = uid("role-fabricated-teen-peer")
    kik_account = uid(f"kik-{KIK_USERNAME}")
    facebook_account = uid("facebook-joe-saucedo")
    phone_primary = uid("phone-760-672-1937")
    iphone_6s = uid("device-iphone-6s-plus")
    iphone_5 = uid("device-iphone-5")
    ip_72 = uid("ip-72-192-152-109")
    ip_172 = uid("ip-172-56-16-238")
    ip_208 = uid("ip-208-54-4-165")
    csam_video_14yo = uid("csam-artifact-video-14yo")
    csam_video_pubescent = uid("csam-artifact-video-pubescent")
    csam_image_prepubescent = uid("csam-artifact-image-prepubescent")
    csam_lure_breast = uid("csam-artifact-lure-breast-exposure")
    csam_lure_money_adult = uid("csam-artifact-lure-money-adult-male")
    prior_conviction = uid("prior-conviction-2012")
    source_doc = uid("source-pacer-pdf")
    provenance = uid("provenance-pacer-extraction")
    mcp_action = uid("mcp-extraction-action")
    calgary_referral = uid("action-calgary-referral")
    calgary_kik_order = uid("action-calgary-kik-production-order")
    tmobile_subpoena = uid("action-tmobile-records")
    facebook_order = uid("action-facebook-court-order")
    ip_correlation = uid("action-ip-correlation-analysis")
    search_warrant = uid("action-search-warrant-2016-11-21")
    mv2_victim_id = uid("action-mv2-victim-identification")
    warrant_auth = uid("authorization-search-warrant")

    graph: list[dict] = [
        {
            "@id": inv,
            "@type": ["case-investigation:Investigation", "cacontology:CACInvestigation"],
            "uco-core:name": "U.S. v. Joseph Daniel Saucedo — ECWG / ICAC Investigation",
            "uco-core:description": (
                "HSI San Diego Child Exploitation Group and ECWG (HSI + USSS) investigation "
                "into online child exploitation linked to fabricated Kik persona Amy Jennings "
                f"({KIK_USERNAME}) and defendant Joseph Daniel SAUCEDO; referred from Calgary "
                "Police Service regarding MV1."
            ),
            "cacontology:caseNumber": PACER_DOCKET,
            "cacontology:investigationStatus": "Criminal Complaint Filed",
            "cacontology:startDate": lit("xsd:date", "2015-10-01"),
            "cacontology:leadAgency": "HSI San Diego Child Exploitation Group",
            "cacontology:jurisdiction": "Southern District of California",
            "cacontology:located_at": {"@id": court_sdca},
            "cacontology:hasPhase": [{"@id": pretrial}],
            "uco-core:object": [
                {"@id": complaint},
                {"@id": prosecution},
                {"@id": charge1},
                {"@id": charge2},
                {"@id": charge3},
                {"@id": incident_mv1},
                {"@id": incident_mv2},
                {"@id": receipt_conduct},
                {"@id": search_warrant},
                {"@id": source_doc},
            ],
        },
        {
            "@id": defendant,
            "@type": ["uco-identity:Person", "cacontology:Subject", "uco-core:UcoObject"],
            "uco-core:name": "Joseph Daniel SAUCEDO",
            "uco-core:description": (
                "Defendant named in magistrate criminal complaint Document 1, Case "
                f"{PACER_DOCKET}. Operated Kik username {KIK_USERNAME} using fabricated "
                "minor female persona Amy Jennings per complaint statement of facts (ALLEGED)."
            ),
            "cacontology-legal-outcomes:chargedWith": [
                {"@id": charge1},
                {"@id": charge2},
                {"@id": charge3},
            ],
        },
        {
            "@id": offender_role,
            "@type": ["case-investigation:Subject", "uco-core:UcoObject"],
            "uco-core:name": "Principal Offender — Saucedo",
            "uco-core:description": "Principal subject role for defendant in this complaint (ALLEGED).",
        },
        {
            "@id": mv1,
            "@type": ["uco-identity:Person", "cacontology-grooming:ChildVictim", "uco-core:UcoObject"],
            "uco-core:name": "Minor Victim 1 (MV1)",
            "uco-core:description": (
                "Eleven-year-old minor victim in Alberta, Canada; contacted via Kik and FaceTime "
                "in late 2015 and early 2016 per complaint Count One (ALLEGED)."
            ),
        },
        {
            "@id": mv2,
            "@type": ["uco-identity:Person", "cacontology-grooming:ChildVictim", "uco-core:UcoObject"],
            "uco-core:name": "Minor Victim 2 (MV2)",
            "uco-core:description": (
                "Sixteen-year-old female victim identified through text exchanges on defendant's "
                "iPhone 6s Plus; saved in contacts as Young Tits per complaint Count Two (ALLEGED)."
            ),
        },
        {
            "@id": complaint,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Magistrate Criminal Complaint (Document 1)",
            "uco-core:description": (
                "Sworn magistrate criminal complaint filed 2016-12-14 in Case "
                f"{PACER_DOCKET}; incorporates statement of facts by HSI Special Agent Stirling "
                "Campbell. Probable-cause charging instrument — not a grand-jury indictment. "
                "Three federal counts (ALLEGED)."
            ),
            "uco-core:externalReference": [
                {
                    "@id": uid("complaint-external-ref"),
                    "@type": "uco-core:ExternalReference",
                    "uco-core:definingContext": "Magistrate Criminal Complaint",
                    "uco-core:referenceURL": {
                        "@type": "xsd:anyURI",
                        "@value": (
                            f"https://ecf.cacd.uscourts.gov/cgi-bin/show_public_doc?"
                            f"{PACER_DOCKET}-{PACER_DOC}"
                        ),
                    },
                }
            ],
        },
        {
            "@id": prosecution,
            "@type": ["cacontology-legal-outcomes:FederalProsecution", "uco-core:UcoObject"],
            "uco-core:name": "Federal Prosecution — U.S. v. Saucedo",
            "uco-core:description": "Pre-trial federal prosecution in the Southern District of California.",
            "cacontology-legal-outcomes:hasLegalPhase": {"@id": pretrial},
        },
        {
            "@id": pretrial,
            "@type": ["cacontology-legal-outcomes:PreTrialPhase", "uco-core:UcoObject"],
            "uco-core:name": "Pre-Trial Phase",
            "cacontology-legal-outcomes:phaseStatus": "complaint_filed",
        },
        {
            "@id": court_sdca,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "United States District Court, Southern District of California",
        },
        {
            "@id": vista,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "Vista, California",
            "uco-core:description": "Defendant subscriber address and search warrant location per complaint.",
        },
        {
            "@id": calgary,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "Calgary, Alberta, Canada",
            "uco-core:description": "Jurisdiction of Calgary Police Service referral regarding MV1.",
        },
        {
            "@id": hsi_ceg,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "HSI San Diego Child Exploitation Group",
        },
        {
            "@id": ecwg,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "San Diego Electronic Crimes Working Group (ECWG)",
            "uco-core:description": "Multi-agency working group including HSI CEG and USSS.",
        },
        {
            "@id": usss,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "United States Secret Service",
        },
        {
            "@id": calgary_pd,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "Calgary Police Service",
        },
        {
            "@id": icac,
            "@type": [
                "cacontology-taskforce:ICACtaskForce",
                "uco-identity:Organization",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Internet Crimes Against Children Task Force",
        },
        {
            "@id": charge1,
            "@type": ["cacontology-legal-outcomes:FederalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count One — Attempted Production (18 U.S.C. §§ 2251(a), 2251(e))",
            "uco-core:description": (
                "Attempted use of MV1, an 11-year-old minor, to produce a visual depiction "
                "of sexually explicit conduct, October 1, 2015 through January 31, 2016 (ALLEGED)."
            ),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 1),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. §§ 2251(a), 2251(e)",
        },
        {
            "@id": charge2,
            "@type": ["cacontology-legal-outcomes:FederalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count Two — Production (18 U.S.C. § 2251(a))",
            "uco-core:description": (
                "Use of MV2, a 16-year-old minor, to produce visual depictions of sexually "
                "explicit conduct, August 1, 2015 through June 12, 2016 (ALLEGED)."
            ),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 2),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. § 2251(a)",
        },
        {
            "@id": charge3,
            "@type": ["cacontology-legal-outcomes:FederalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count Three — Receipt (18 U.S.C. § 2252(a)(2))",
            "uco-core:description": (
                "Knowingly receiving visual depictions involving minors engaging in sexually "
                "explicit conduct via interstate commerce, August 1, 2015 through November 21, 2016 "
                "(ALLEGED)."
            ),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 3),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. § 2252(a)(2)",
        },
        {
            "@id": amy_persona,
            "@type": ["uco-identity:Identity", "uco-core:UcoObject"],
            "uco-core:name": "Amy Jennings (fabricated persona)",
            "uco-core:description": (
                "Fabricated minor female persona (~15-16 years old) used on Kik to groom victims, "
                "send CSAM lures, and introduce an adult male coercing FaceTime contact (ALLEGED). "
                "Controlled by defendant per complaint statement of facts."
            ),
        },
        {
            "@id": fabricated_teen_role,
            "@type": ["uco-role:Role", "uco-core:UcoObject"],
            "uco-core:name": "Fabricated teenage female peer",
            "uco-core:description": "Impersonated peer role used in TeenageImpersonationGrooming of MV1 (ALLEGED).",
        },
        {
            "@id": grooming_mv1,
            "@type": [
                "cacontology-grooming:OnlineGrooming",
                "cacontology-grooming:TeenageImpersonationGrooming",
                "cacontology-grooming:SexualSolicitation",
                "cacontology-grooming:InitiatorContentSending",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Amy Jennings Kik Grooming of MV1",
            "uco-core:description": (
                f"Defendant, via Kik username {KIK_USERNAME} posing as Amy Jennings, groomed MV1, "
                "sent CSAM lures, and introduced an adult male coercing FaceTime genital exposure "
                "(ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "cacontology-grooming:targetsVictim": {"@id": mv1},
            "cacontology-grooming:impersonatedRole": "teenage female peer (~15-16 years old)",
            "cacontology-grooming:impersonatesRole": {"@id": fabricated_teen_role},
            "cacontology-grooming:rolePlayingTactic": "peer",
        },
        {
            "@id": incident_mv1,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "MV1 FaceTime Solicitation Attempt",
            "uco-core:description": (
                "December 2015 FaceTime contacts where adult male solicited MV1 to expose genitals; "
                "MV1 declined. Underlies Count One attempted production allegation (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "uco-core:hasFacet": [
                {
                    "@id": uid("artifact-mv1-facetime"),
                    "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                    "uco-core:description": "FaceTime video contact solicitation attempt, December 2015.",
                }
            ],
        },
        {
            "@id": grooming_mv2,
            "@type": [
                "cacontology-grooming:OnlineGrooming",
                "cacontology-grooming:ExplicitCommercialOfferGrooming",
                "cacontology-grooming:NormalizationGrooming",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "MV2 Modeling Coercion and Amy Jennings Blackmail",
            "uco-core:description": (
                "Defendant posed as modeling agent on Instagram/iMessage, offered paid modeling, "
                "coerced nude images and FaceTime, used nut challenge ($1,000) incentive, and "
                "leveraged Amy Jennings persona for blackmail/threats to distribute images and "
                "dox address via Google Maps photo (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "cacontology-grooming:targetsVictim": {"@id": mv2},
            "cacontology-grooming:rolePlayingTactic": "modeling agent",
            "cacontology-grooming:usesThreats": lit("xsd:boolean", True),
            "cacontology-grooming:contentType": "images and FaceTime sessions",
            "cacontology-grooming:exchangesContent": {"@id": amy_persona},
        },
        {
            "@id": incident_mv2,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "MV2 Produced Visual Depictions",
            "uco-core:description": (
                "Defendant received multiple nude photographs and FaceTime sessions from MV2 after "
                "coercion; text exchanges and contact entry Young Tits recovered from iPhone 6s Plus "
                "(ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "uco-core:hasFacet": [
                {
                    "@id": uid("artifact-mv2-photos"),
                    "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                    "uco-core:description": (
                        "Nude photographs and FaceTime sessions recovered from iPhone 6s Plus; "
                        "includes image with Joe written on victim's chest per complaint."
                    ),
                }
            ],
        },
        {
            "@id": receipt_conduct,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "Kik CP Receipt and Distribution",
            "uco-core:description": (
                f"Kik user {KIK_USERNAME} exchanged approximately 130 images and 66 videos; "
                "69 images and 63 videos determined to depict child pornography per SA review (ALLEGED)."
            ),
            "uco-action:performer": {"@id": defendant},
            "uco-core:hasFacet": [
                {
                    "@id": uid("artifact-kik-cp-batch"),
                    "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                    "uco-core:description": (
                        f"Approximately 69 images and 63 videos depicting child pornography "
                        f"exchanged via Kik username {KIK_USERNAME}."
                    ),
                }
            ],
        },
        csam_artifact(
            "csam-artifact-video-14yo",
            "Kik video — minor states age 14",
            "Video depicts fully nude pubescent female before mirror stating she is 14 years old.",
        ),
        csam_artifact(
            "csam-artifact-video-pubescent",
            "Kik video — pubescent female masturbation",
            "Video depicts nude pubescent female minor from waist down masturbating.",
        ),
        csam_artifact(
            "csam-artifact-image-prepubescent",
            "Kik image — pre-pubescent minor mirror exposure",
            "Image depicts nude pre-pubescent female leaning before mirror exposing vagina.",
        ),
        csam_artifact(
            "csam-artifact-lure-breast-exposure",
            "Kik lure photo — partial breast exposure",
            (
                "Photograph sent January 2 or 9, 2016 via IP 72.192.152.109 depicting a "
                "pubescent female minor lifting shirt halfway and partially exposing breasts "
                "(CSAM lure per complaint)."
            ),
        ),
        csam_artifact(
            "csam-artifact-lure-money-adult-male",
            "Kik lure photos — money and adult male",
            (
                "Photographs sent January 2 or 9, 2016 via IP 72.192.152.109 depicting money "
                "and a partially clothed adult male, used as grooming lures per complaint."
            ),
        ),
        {
            "@id": kik_account,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": f"Kik account {KIK_USERNAME}",
            "uco-core:description": (
                f"Kik username linked to defendant via T-Mobile records, IP correlation, and "
                f"seized iPhone 5 (ALLEGED). Spelling '{KIK_USERNAME}' is verbatim from PACER "
                "Document 1 extracted text; record transcription variants in fusion metadata if "
                "external sources differ."
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("kik-facet"),
                    "@type": "uco-observable:AccountFacet",
                    "uco-observable:accountIdentifier": KIK_USERNAME,
                }
            ],
        },
        {
            "@id": facebook_account,
            "@type": ["uco-observable:DigitalAccount", "uco-core:UcoObject"],
            "uco-core:name": f"Facebook account Joe SAUCEDO (ID {FACEBOOK_ID})",
            "uco-core:description": (
                "Facebook subscriber Joe SAUCEDO; phone 760-672-1937 verified 2014-01-30; "
                "IP access logs correlated with Kik activity (ALLEGED)."
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("facebook-facet"),
                    "@type": "uco-observable:DigitalAccountFacet",
                    "uco-observable:accountIdentifier": FACEBOOK_ID,
                }
            ],
        },
        {
            "@id": phone_primary,
            "@type": ["uco-observable:PhoneAccount", "uco-core:UcoObject"],
            "uco-core:name": "T-Mobile 760-672-1937",
            "uco-core:hasFacet": [
                {
                    "@id": uid("phone-facet"),
                    "@type": "uco-observable:PhoneAccountFacet",
                    "uco-observable:accountIdentifier": "760-672-1937",
                }
            ],
        },
        ip_node(
            "ip-72-192-152-109",
            "72.192.152.109",
            "Cox subscriber IP used by Kik user and to access defendant Facebook page (ALLEGED).",
        ),
        ip_node(
            "ip-172-56-16-238",
            "172.56.16.238",
            "IP used by Kik user to send CP video January 15, 2016; same IP accessed Facebook (ALLEGED).",
        ),
        ip_node(
            "ip-208-54-4-165",
            "208.54.4.165",
            "IP used by Kik user to send CP video January 24, 2016; same IP accessed Facebook (ALLEGED).",
        ),
        {
            "@id": iphone_6s,
            "@type": [
                "uco-observable:ObservableObject",
                "cacontology-production:MobileRecordingDevice",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Apple iPhone 6s Plus (760-672-1937)",
            "uco-core:description": (
                "Seized from defendant's pocket during November 21, 2016 search warrant; associated "
                "with Facebook page and MV2 text exchanges including contact Young Tits (ALLEGED)."
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("contact-young-tits"),
                    "@type": ["uco-observable:ContactFacet", "uco-core:Facet"],
                    "uco-observable:contactNote": ["Young Tits — MV2 contact label in defendant phone (ALLEGED)."],
                }
            ],
        },
        {
            "@id": iphone_5,
            "@type": [
                "uco-observable:ObservableObject",
                "cacontology-production:MobileRecordingDevice",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Apple iPhone 5 (760-672-1937)",
            "uco-core:description": (
                f"Seized from defendant's car; associated with Kik {KIK_USERNAME} and Amy Jennings "
                "persona (ALLEGED)."
            ),
        },
        {
            "@id": prior_conviction,
            "@type": ["uco-core:UcoObject"],
            "uco-core:name": "2012 San Diego Superior Court Conviction",
            "uco-core:description": (
                "California law enforcement databases show Joseph SAUCEDO convicted in San Diego "
                "County Superior Court in 2012 for Unlawful Sex with a Minor more than 3 years "
                "younger; defendant age 20, victim age 14. Background context in complaint — "
                "not a charge in this case."
            ),
        },
        {
            "@id": calgary_referral,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Calgary Police Service Referral and MV1 Timeline",
            "uco-core:description": (
                "ECWG investigation opened summer 2016 based on Calgary Police reports regarding MV1."
            ),
            "uco-action:performer": {"@id": calgary_pd},
            "uco-action:object": {"@id": mv1},
            "uco-action:result": {"@id": calgary_kik_order},
            "uco-action:location": {"@id": calgary},
        },
        {
            "@id": calgary_kik_order,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Calgary Kik Production Order (Alberta)",
            "uco-core:description": (
                f"Justice of the Peace J. K. Conly production order for Kik username {KIK_USERNAME}; "
                "data log received April 26, 2016 showing T-Mobile MSISDN 760-672-1937."
            ),
            "uco-action:performer": {"@id": calgary_pd},
            "uco-action:object": {"@id": kik_account},
            "uco-action:result": {"@id": tmobile_subpoena},
            "case-investigation:wasInformedBy": {"@id": calgary_referral},
        },
        {
            "@id": tmobile_subpoena,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "T-Mobile and Kik Records Analysis",
            "uco-core:description": (
                f"Subscriber records and Kik data log for {KIK_USERNAME} linked MSISDN 7606721937 "
                "to Joseph SAUCEDO in Vista, California."
            ),
            "uco-action:performer": {"@id": hsi_ceg},
            "uco-action:object": {"@id": kik_account},
            "uco-action:result": {"@id": facebook_order},
            "case-investigation:wasInformedBy": {"@id": calgary_kik_order},
        },
        {
            "@id": facebook_order,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Facebook Subscriber and IP Log Production",
            "uco-core:description": (
                f"Court order August 4, 2016; Facebook identified subscriber Joe SAUCEDO for ID "
                f"{FACEBOOK_ID} with phone 760-672-1937."
            ),
            "uco-action:performer": {"@id": ecwg},
            "uco-action:object": {"@id": facebook_account},
            "uco-action:result": {"@id": ip_correlation},
            "case-investigation:wasInformedBy": {"@id": tmobile_subpoena},
        },
        {
            "@id": ip_correlation,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Kik–Facebook IP Correlation Analysis",
            "uco-core:description": (
                f"Comparative analysis: 13 of 20 IP addresses used by {KIK_USERNAME} (Dec 20, 2015–"
                "Jan 24, 2016) matched IPs accessing defendant Facebook page at same dates/times "
                "(ALLEGED attribution evidence)."
            ),
            "uco-action:performer": {"@id": hsi_ceg},
            "uco-action:object": {"@id": kik_account},
            "uco-action:result": {"@id": search_warrant},
            "case-investigation:wasInformedBy": {"@id": facebook_order},
        },
        {
            "@id": warrant_auth,
            "@type": ["case-investigation:Authorization", "uco-core:UcoObject"],
            "uco-core:name": "Search Warrant — Vista Residence",
            "uco-core:description": (
                "Search warrant executed November 21, 2016 at girlfriend's parents' house in Vista."
            ),
        },
        {
            "@id": search_warrant,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Search Warrant Execution (2016-11-21)",
            "uco-core:description": (
                "ECWG executed search warrant; seized iPhone 6s Plus and iPhone 5; recovered MV2 "
                "text exchanges from iPhone 6s Plus."
            ),
            "uco-action:startTime": lit("xsd:dateTime", "2016-11-21T00:00:00Z"),
            "case-investigation:relevantAuthorization": {"@id": warrant_auth},
            "uco-action:performer": {"@id": ecwg},
            "uco-action:location": {"@id": vista},
            "uco-action:object": {"@id": defendant},
            "uco-action:result": [{"@id": iphone_6s}, {"@id": iphone_5}, {"@id": mv2_victim_id}],
            "case-investigation:wasInformedBy": {"@id": ip_correlation},
        },
        {
            "@id": mv2_victim_id,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "MV2 Victim Identification (Open Source + DMV)",
            "uco-core:description": (
                "MV2 identified through open-source phone number search and California DMV photo "
                "comparison confirming date of birth from text exchanges on seized iPhone 6s Plus "
                "(ALLEGED)."
            ),
            "uco-action:performer": {"@id": hsi_ceg},
            "uco-action:object": {"@id": mv2},
            "uco-action:instrument": {"@id": iphone_6s},
            "case-investigation:wasInformedBy": {"@id": search_warrant},
        },
        {
            "@id": source_doc,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": SOURCE_PDF,
            "uco-core:description": (
                "PACER criminal complaint Document 1 with incorporated statement of facts; "
                f"MCP extraction at {MCP_EXTRACTION.name}."
            ),
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
            "@id": mcp_action,
            "@type": ["case-investigation:InvestigativeAction"],
            "uco-core:name": "CASE/UCO MCP document extraction",
            "uco-action:instrument": {"@id": uid("tool-case-uco-mcp")},
            "uco-action:object": {"@id": source_doc},
        },
        {
            "@id": uid("tool-case-uco-mcp"),
            "@type": ["uco-tool:Tool"],
            "uco-core:name": "case-uco-document-normalize",
            "uco-tool:version": "0.6.0",
        },
        {
            "@id": provenance,
            "@type": ["case-investigation:ProvenanceRecord"],
            "uco-core:description": (
                "Investigative graph derived from PACER criminal complaint PDF and MCP semantic "
                "extraction bundle; counts and conduct described as ALLEGED in complaint."
            ),
            "uco-core:createdBy": {"@id": hsi_ceg},
            "case-investigation:wasDerivedFrom": {"@id": source_doc},
        },
    ]

    graph.extend(
        [
            rel(inv, complaint, "Relates_To"),
            rel(inv, prosecution, "Relates_To"),
            rel(prosecution, complaint, "Relates_To"),
            rel(complaint, charge1, "Relates_To"),
            rel(complaint, charge2, "Relates_To"),
            rel(complaint, charge3, "Relates_To"),
            rel(charge1, incident_mv1, "Relates_To"),
            rel(charge1, grooming_mv1, "Relates_To"),
            rel(charge1, mv1, "Relates_To"),
            rel(charge2, incident_mv2, "Relates_To"),
            rel(charge2, grooming_mv2, "Relates_To"),
            rel(charge2, mv2, "Relates_To"),
            rel(charge3, receipt_conduct, "Relates_To"),
            rel(charge3, kik_account, "Relates_To"),
            rel(charge1, court_sdca, "Relates_To"),
            rel(charge2, court_sdca, "Relates_To"),
            rel(charge3, court_sdca, "Relates_To"),
            rel(defendant, offender_role, "has_role"),
            rel(defendant, kik_account, "Associated_With"),
            rel(defendant, facebook_account, "Associated_With"),
            rel(defendant, phone_primary, "Associated_With"),
            rel(defendant, amy_persona, "Controls"),
            rel(defendant, prior_conviction, "Prior_Conviction"),
            rel(amy_persona, kik_account, "Associated_With"),
            rel(amy_persona, fabricated_teen_role, "Impersonates"),
            rel(grooming_mv1, amy_persona, "Relates_To"),
            rel(grooming_mv2, amy_persona, "Relates_To"),
            rel(grooming_mv2, amy_persona, "Coerces_Via"),
            rel(amy_persona, grooming_mv2, "Used_For_Blackmail"),
            rel(incident_mv2, iphone_6s, "used_equipment"),
            rel(grooming_mv2, iphone_6s, "used_equipment"),
            rel(receipt_conduct, iphone_5, "used_equipment"),
            rel(receipt_conduct, kik_account, "Associated_With"),
            rel(receipt_conduct, csam_video_14yo, "Relates_To"),
            rel(receipt_conduct, csam_video_pubescent, "Relates_To"),
            rel(receipt_conduct, csam_image_prepubescent, "Relates_To"),
            rel(receipt_conduct, csam_lure_breast, "Relates_To"),
            rel(receipt_conduct, csam_lure_money_adult, "Relates_To"),
            rel(receipt_conduct, ip_72, "Relates_To"),
            rel(kik_account, ip_72, "Used_By"),
            rel(kik_account, ip_172, "Used_By"),
            rel(kik_account, ip_208, "Used_By"),
            rel(facebook_account, ip_72, "Accessed_By"),
            rel(facebook_account, ip_172, "Accessed_By"),
            rel(facebook_account, ip_208, "Accessed_By"),
            rel(ip_correlation, ip_72, "Relates_To"),
            rel(ip_correlation, facebook_account, "Relates_To"),
            rel(ip_correlation, kik_account, "Relates_To"),
            rel(ecwg, usss, "partnersWith"),
            rel(ecwg, hsi_ceg, "partnersWith"),
            rel(ecwg, icac, "partnersWith"),
            rel(inv, calgary, "parallel_jurisdiction"),
            rel(provenance, source_doc, "Derived_From"),
        ]
    )

    context = {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "cacontology": "https://cacontology.projectvic.org#",
            "cac-core": "https://cacontology.projectvic.org/core#",
            "cacontology-grooming": "https://cacontology.projectvic.org/grooming#",
            "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
            "cacontology-production": "https://cacontology.projectvic.org/production#",
            "cacontology-taskforce": "https://cacontology.projectvic.org/taskforce#",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }
    return context


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
