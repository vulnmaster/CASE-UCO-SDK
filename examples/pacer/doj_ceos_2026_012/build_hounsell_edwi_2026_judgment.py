#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Bradley D. Hounsell criminal judgment.

Source: PACER Document 34, Case 1:25-cr-00069-WCG (E.D. Wis.), filed 2026-05-18.
Note: Source filename references 'statement of reasons' but extracted content is AO 245B
Judgment in a Criminal Case (sentencing judgment), not a separate Statement of Reasons form.
Recipes applied:
  - cac-legal-sentencing-outcomes
  - cac-federal-prosecution-relationships (post-plea disposition)
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

CASE_ID = "hounsell-edwi-2026-judgment"
NS = f"https://example.org/cac/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "hounsell-edwi-2026-judgment.jsonld"
MCP_EXTRACTION = Path(__file__).resolve().parent / "case-uco-mcp-output.jsonld"
SOURCE_PDF = "pacer -- doj_ceos_2026_012 -- statement of reasons.pdf"
SOURCE_SHA256 = "BFCD3F77945208A4365EE361AA0C588A3BE73CC7C3EDDBD3E25255421ED5AE4F"
PACER_DOCKET = "1:25-cr-00069-WCG"
PACER_DOC = "34"
USM_NUMBER = "74726-511"


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


def condition_facet(summary: str) -> dict:
    return {
        "@id": uid(f"facet-{uuid.uuid5(uuid.NAMESPACE_URL, summary)}"),
        "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
        "uco-core:description": summary,
    }


def supervision_condition(
    label: str,
    name: str,
    category: str,
    description: str,
    facet_summary: str,
    *,
    extra_types: list[str] | None = None,
) -> dict:
    types = ["uco-observable:ObservableObject", "uco-core:UcoObject"]
    if extra_types:
        types = extra_types + types
    return {
        "@id": uid(label),
        "@type": types,
        "uco-core:name": name,
        "uco-core:description": description,
        "uco-core:tag": [f"supervision-condition:{category}"],
        "uco-core:hasFacet": [condition_facet(facet_summary)],
    }


def build_graph() -> dict:
    inv = uid("investigation")
    defendant = uid("defendant-hounsell")
    prosecution = uid("federal-prosecution")
    sentencing_phase = uid("sentencing-phase")
    judgment = uid("criminal-judgment-ao245b")
    charge1 = uid("federal-charge-2422b")
    plea = uid("guilty-plea-count-one")
    dismissal = uid("dismissal-remaining-counts")
    prison = uid("prison-sentence-156-months")
    supervised = uid("supervised-release-7-years")
    payment_schedule = uid("payment-schedule-lump-sum")
    special_assessment = uid("monetary-special-assessment")
    avaa_jvta = uid("monetary-avaa-jvta")
    court_edwi = uid("location-ed-wisconsin")
    judge = uid("judge-griesbach")
    ausa_humble = uid("ausa-daniel-humble")
    ausa_clayman = uid("ausa-william-clayman")
    prosecutor_role_humble = uid("prosecutor-role-humble")
    prosecutor_role_clayman = uid("prosecutor-role-clayman")
    defense = uid("defense-steven-richards")
    defense_role = uid("defense-attorney-role-richards")
    usao_edwi = uid("org-usao-ed-wisconsin")
    bop = uid("org-bureau-of-prisons")
    source_doc = uid("source-pacer-pdf")
    provenance = uid("provenance-pacer-extraction")
    cond_sorna = uid("condition-sorna-registration")
    cond_sex_offender_tx = uid("condition-sex-offender-treatment")
    cond_minor_contact = uid("condition-minor-contact-restriction")
    cond_computer_monitor = uid("condition-computer-internet-monitoring")
    cond_search = uid("condition-probation-search")
    cond_substance = uid("condition-drug-alcohol-treatment")

    graph: list[dict] = [
        {
            "@id": inv,
            "@type": ["case-investigation:Investigation", "cacontology:CACInvestigation"],
            "uco-core:name": "U.S. v. Bradley D. Hounsell — Federal Enticement Case",
            "uco-core:description": (
                "Federal child enticement prosecution in the Eastern District of Wisconsin; "
                "post-plea sentencing judgment entered May 18, 2026 per PACER Document 34."
            ),
            "cacontology:caseNumber": PACER_DOCKET,
            "cacontology:investigationStatus": "Sentenced",
            "cacontology:jurisdiction": "Eastern District of Wisconsin",
            "cacontology:located_at": {"@id": court_edwi},
            "cacontology:hasPhase": [{"@id": sentencing_phase}],
            "uco-core:object": [
                {"@id": judgment},
                {"@id": prosecution},
                {"@id": charge1},
                {"@id": prison},
                {"@id": supervised},
                {"@id": payment_schedule},
                {"@id": source_doc},
            ],
        },
        {
            "@id": defendant,
            "@type": ["uco-identity:Person", "cacontology:Subject", "uco-core:UcoObject"],
            "uco-core:name": "Bradley D. Hounsell",
            "uco-core:description": (
                f"Defendant in Case {PACER_DOCKET}; USM Number {USM_NUMBER}. "
                "Pled guilty to count one of the information (18 U.S.C. § 2422(b))."
            ),
            "cacontology-legal-outcomes:chargedWith": [{"@id": charge1}],
        },
        {
            "@id": prosecution,
            "@type": ["cacontology-legal-outcomes:FederalProsecution", "uco-core:UcoObject"],
            "uco-core:name": "Federal Prosecution — U.S. v. Hounsell",
            "cacontology-legal-outcomes:hasLegalPhase": {"@id": sentencing_phase},
        },
        {
            "@id": sentencing_phase,
            "@type": ["cacontology-legal-outcomes:SentencingPhase", "uco-core:UcoObject"],
            "uco-core:name": "Sentencing Phase",
            "cacontology-legal-outcomes:phaseStatus": "judgment_entered",
        },
        {
            "@id": judgment,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Judgment in a Criminal Case (AO 245B, Document 34)",
            "uco-core:description": (
                "Formal AO 245B sentencing judgment entered 2026-05-18 after guilty plea and "
                "sentencing hearing (sentence imposed 2026-05-14 by Judge William C. Griesbach). "
                "This is the sentencing judgment — not a separate Statement of Reasons, charging "
                "instrument, or plea agreement. Source filename references 'statement of reasons' "
                "but extracted document content is the judgment form."
            ),
            "uco-core:externalReference": [
                {
                    "@id": uid("judgment-external-ref"),
                    "@type": "uco-core:ExternalReference",
                    "uco-core:definingContext": "PACER Judgment in a Criminal Case (AO 245B)",
                    "uco-core:referenceURL": {
                        "@type": "xsd:anyURI",
                        "@value": (
                            f"https://ecf.wied.wi.gov/cgi-bin/show_public_doc?"
                            f"{PACER_DOCKET}-{PACER_DOC}"
                        ),
                    },
                }
            ],
        },
        {
            "@id": charge1,
            "@type": [
                "cacontology-legal-outcomes:OnlineEnticement",
                "cacontology-legal-outcomes:FederalCharge",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Count One — Coercion and Enticement of a Minor (18 U.S.C. § 2422(b))",
            "uco-core:description": (
                "Defendant adjudicated guilty of coercion and enticement of a minor; "
                "offense conduct concluded November 8, 2023."
            ),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 1),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. § 2422(b)",
        },
        {
            "@id": plea,
            "@type": ["cacontology-legal-outcomes:PleaBargaining", "uco-core:UcoObject"],
            "uco-core:name": "Guilty Plea to Count One of the Information",
            "uco-core:description": (
                "Defendant pled guilty to count one of the information."
            ),
            "uco-action:object": {"@id": charge1},
            "uco-action:performer": {"@id": defendant},
            "uco-action:result": {"@id": dismissal},
        },
        {
            "@id": dismissal,
            "@type": ["uco-core:UcoObject"],
            "uco-core:name": "Dismissal of Remaining Counts",
            "uco-core:description": (
                "All remaining counts dismissed upon motion of the United States."
            ),
        },
        {
            "@id": prison,
            "@type": ["cacontology-legal-outcomes:PrisonSentence", "uco-core:UcoObject"],
            "uco-core:name": "156-Month Federal Prison Sentence",
            "uco-core:description": (
                "Committed to U.S. Bureau of Prisons for 156 months on count one. BOP recommendations: "
                "facility as close to home as possible; participation in 500-hour drug treatment program. "
                "Defendant to surrender per BOP designation."
            ),
            "cacontology-legal-outcomes:sentenceDurationMonths": lit("xsd:integer", 156),
        },
        {
            "@id": supervised,
            "@type": ["cacontology-legal-outcomes:SupervisedRelease", "uco-core:UcoObject"],
            "uco-core:name": "7-Year Term of Supervised Release",
            "uco-core:description": (
                "Seven-year supervised release term following imprisonment, with standard Wisconsin "
                "district conditions plus six special conditions modeled as structured supervision nodes."
            ),
            "cacontology-legal-outcomes:sentenceDurationMonths": lit("xsd:integer", 84),
        },
        supervision_condition(
            "condition-sorna-registration",
            "SORNA Registration Requirement",
            "sorna-compliance",
            "Must comply with Sex Offender Registration and Notification Act (34 U.S.C. § 20901 et seq.).",
            "statute=34 U.S.C. § 20901 et seq.; complianceDirectedBy=probationOfficer|BOP|stateRegistry",
            extra_types=["cacontology-registry:RegistrationRequirement"],
        ),
        supervision_condition(
            "condition-sex-offender-treatment",
            "Sex Offender Mental Health Treatment",
            "sex-offender-treatment",
            (
                "Approved sex offender mental health assessment and treatment until released by "
                "probation officer; may include polygraph for planning and monitoring."
            ),
            (
                "polygraph=permitted; confidentialityWaived=true; defendantPaysCost=true; "
                "refusalIsViolation=true; duration=untilReleasedByProbationOfficer"
            ),
        ),
        supervision_condition(
            "condition-minor-contact-restriction",
            "Minor Contact Restriction",
            "minor-contact-restriction",
            (
                "No intentional one-on-one contact with children under 18 unless approved in writing "
                "by probation officer."
            ),
            (
                "maxVictimAge=17; requiresWrittenProbationApproval=true; "
                "requiresResponsibleAdultPresent=true; responsibleAdultAdvisedOfHistory=true; "
                "unauthorizedContactReportWithinHours=8"
            ),
        ),
        supervision_condition(
            "condition-computer-internet-monitoring",
            "Computer and Internet Monitoring",
            "computer-internet-monitoring",
            (
                "Participate in computer/internet monitoring program; defendant pays program cost."
            ),
            (
                "internetDevicesRequirePermission=true; monitoringProgramRequired=true; "
                "deviceInventoryRequired=true; pseudonymsPasswordsLogonsRequired=true; "
                "unannouncedExaminationConsent=true; encryptionProhibited=true; "
                "dataErasureToolsProhibited=true; defendantPaysCost=true"
            ),
        ),
        supervision_condition(
            "condition-probation-search",
            "Probation Search Condition",
            "probation-search",
            (
                "Submit person, property, residence, vehicle, papers, computers, and electronic "
                "storage to probation search when reasonable suspicion exists."
            ),
            (
                "searchAuthority=UnitedStatesProbationOfficer; "
                "standard=reasonableSuspicionOfViolation; searchTiming=reasonable; "
                "searchManner=reasonable; warnOtherOccupants=true; "
                "revocationGroundIfRefused=true"
            ),
        ),
        supervision_condition(
            "condition-drug-alcohol-treatment",
            "Drug and Alcohol Testing and Treatment",
            "substance-abuse-treatment",
            (
                "Substance abuse testing and treatment program approved by supervising probation officer."
            ),
            (
                "maxUrinalysisPerMonth=6; residentialOrOutpatientTreatment=true; "
                "alcoholAbstinence=true; defendantPaysCost=true; "
                "duration=untilReleasedFromProgram"
            ),
        ),
        {
            "@id": payment_schedule,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Schedule of Payments — Lump Sum $5,100.00",
            "uco-core:description": (
                "AO 245B Schedule of Payments option A: lump sum of $5,100.00 due immediately. "
                "Comprises $100.00 special assessment and $5,000.00 AVAA/JVTA assessments. "
                "No interest requirement noted on judgment form."
            ),
            "uco-core:tag": ["payment-schedule:lump-sum-immediate"],
            "uco-core:hasFacet": [
                {
                    "@id": uid("payment-schedule-facet"),
                    "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
                    "uco-core:description": (
                        "totalAmountUSD=5100.00; dueTiming=immediately; "
                        "scheduleOption=AO245B-A; interestWaived=notApplicable"
                    ),
                }
            ],
        },
        {
            "@id": special_assessment,
            "@type": ["cacontology-legal-outcomes:MonetaryPenalty", "uco-core:UcoObject"],
            "uco-core:name": "Special Assessment — $100.00",
            "uco-core:description": "Special assessment of $100.00; due immediately per payment schedule.",
            "uco-core:hasFacet": [
                condition_facet("amountUSD=100.00; penaltyType=specialAssessment; dueTiming=immediately"),
            ],
        },
        {
            "@id": avaa_jvta,
            "@type": ["cacontology-legal-outcomes:MonetaryPenalty", "uco-core:UcoObject"],
            "uco-core:name": "AVAA / JVTA Assessments — $5,000.00",
            "uco-core:description": (
                "Combined AVAA (Pub. L. 115-299) and JVTA (Pub. L. 114-22) assessments totaling "
                "$5,000.00; due immediately per payment schedule."
            ),
            "uco-core:hasFacet": [
                condition_facet(
                    "amountUSD=5000.00; penaltyType=AVAA+JVTA; "
                    "statutes=Pub.L.115-299|Pub.L.114-22; dueTiming=immediately"
                ),
            ],
        },
        {
            "@id": court_edwi,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "United States District Court, Eastern District of Wisconsin",
        },
        {
            "@id": judge,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "William C. Griesbach",
            "uco-core:description": "United States District Judge who imposed sentence May 14, 2026.",
        },
        {
            "@id": ausa_humble,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Daniel Humble",
            "uco-core:description": "Assistant United States Attorney.",
        },
        {
            "@id": ausa_clayman,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "William Clayman",
            "uco-core:description": "Assistant United States Attorney.",
        },
        {
            "@id": prosecutor_role_humble,
            "@type": [
                "cacontology-legal-outcomes:ProsecutorRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Prosecutor — Daniel Humble",
        },
        {
            "@id": prosecutor_role_clayman,
            "@type": [
                "cacontology-legal-outcomes:ProsecutorRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Prosecutor — William Clayman",
        },
        {
            "@id": defense,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Steven Richards",
            "uco-core:description": "Defendant's attorney of record on judgment.",
        },
        {
            "@id": defense_role,
            "@type": [
                "cacontology-legal-outcomes:DefenseAttorneyRole",
                "uco-role:Role",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Defense Counsel — Steven Richards",
        },
        {
            "@id": usao_edwi,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "U.S. Attorney's Office, Eastern District of Wisconsin",
        },
        {
            "@id": bop,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "United States Bureau of Prisons",
        },
        {
            "@id": source_doc,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": SOURCE_PDF,
            "uco-core:description": (
                "PACER Document 34 (AO 245B judgment); MCP extraction at "
                f"{MCP_EXTRACTION.name}."
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
            "@id": provenance,
            "@type": ["case-investigation:ProvenanceRecord"],
            "uco-core:description": (
                "Sentencing judgment graph derived from PACER PDF and CASE/UCO MCP extraction; "
                "imposed under Sentencing Reform Act of 1984."
            ),
            "case-investigation:wasDerivedFrom": {"@id": source_doc},
        },
    ]

    graph.extend(
        [
            rel(inv, judgment, "Relates_To"),
            rel(inv, prosecution, "Relates_To"),
            rel(prosecution, judgment, "Relates_To"),
            rel(prosecution, sentencing_phase, "Relates_To"),
            rel(judgment, charge1, "Relates_To"),
            rel(judgment, plea, "Relates_To"),
            rel(judgment, dismissal, "Orders"),
            rel(judgment, prison, "Imposes"),
            rel(judgment, supervised, "Imposes"),
            rel(judgment, payment_schedule, "Imposes"),
            rel(judgment, special_assessment, "Imposes"),
            rel(judgment, avaa_jvta, "Imposes"),
            rel(judgment, judge, "Signed_By"),
            rel(payment_schedule, special_assessment, "Includes"),
            rel(payment_schedule, avaa_jvta, "Includes"),
            rel(plea, dismissal, "Results_In"),
            rel(usao_edwi, dismissal, "Requested"),
            rel(charge1, court_edwi, "Relates_To"),
            rel(defendant, prison, "Sentenced_To"),
            rel(defendant, supervised, "Subject_To"),
            rel(defendant, defense, "Represented_By"),
            rel(defendant, defense_role, "has_role"),
            rel(ausa_humble, prosecutor_role_humble, "has_role"),
            rel(ausa_clayman, prosecutor_role_clayman, "has_role"),
            rel(defense, defense_role, "has_role"),
            rel(prosecution, usao_edwi, "Relates_To"),
            rel(ausa_humble, usao_edwi, "Affiliated_With"),
            rel(ausa_clayman, usao_edwi, "Affiliated_With"),
            rel(prison, bop, "Relates_To"),
            rel(supervised, cond_sorna, "Requires"),
            rel(supervised, cond_sex_offender_tx, "Requires"),
            rel(supervised, cond_minor_contact, "Requires"),
            rel(supervised, cond_computer_monitor, "Requires"),
            rel(supervised, cond_search, "Requires"),
            rel(supervised, cond_substance, "Requires"),
            rel(provenance, source_doc, "Derived_From"),
        ]
    )

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "cacontology": "https://cacontology.projectvic.org#",
            "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
            "cacontology-registry": "https://cacontology.projectvic.org/sex-offender-registry#",
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
