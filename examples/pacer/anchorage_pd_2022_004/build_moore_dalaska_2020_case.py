#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Jayshon Moore (D. Alaska ICAC prosecution).

Sources (PACER):
  - Indictment: Case 3:20-cr-00029-SLG-MMS Document 2 (filed 2020-02-21)
  - Government trial brief: Document 172 (filed 2022-03-28)
  - Judgment (AO 245B): Document 251 (filed 2022-09-20)

MCP extraction artifacts: output/icac_pacer/anchorage_pd_2022_004/*.jsonld

Recipes applied:
  - cac-federal-prosecution-relationships
  - cac-federal-trial-proceedings
  - cac-trafficking-recruitment-network
  - cac-production-case
  - cac-legal-sentencing-outcomes
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

CASE_ID = "moore-dalaska-2020-icac"
NS = f"https://example.org/cac/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "moore-dalaska-2020-icac.jsonld"

PACER_DOCKET = "3:20-cr-00029-SLG-MMS"
USM_NUMBER = "15966-006"
LOCAL_REF = "anchorage_pd_2022_004"

SOURCE_DOCS = {
    "indictment": {
        "file_name": "pacer -- anchorage_pd_2022_004 -- indictment.pdf",
        "sha256": "2FC4FA376F610BDB800C3C7CFBB335A5F60C09C514536BEAC43856CC8F4B1BF6",
        "pacer_doc": "2",
        "filed": "2020-02-21",
    },
    "trial_brief": {
        "file_name": "pacer -- anchorage_pd_2022_004 -- trial brief.pdf",
        "sha256": "881974299FA29B1B2966E0F1B002034036B4F307668A24546B2C39AFF9B2D01D",
        "pacer_doc": "172",
        "filed": "2022-03-28",
    },
    "judgment": {
        "file_name": "pacer -- anchorage_pd_2022_004 -- judgment.pdf",
        "sha256": "FDA8EF021E722D2B49857DE0DA18C281EC0716D1914ABBC0456D5E7DD37C49F9",
        "pacer_doc": "251",
        "filed": "2022-09-20",
    },
}


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


def src_ref(doc_key: str, page: str, *, section: str = "") -> str:
    doc = SOURCE_DOCS[doc_key]
    tail = f"; {section}" if section else ""
    return f"Source: PACER Doc {doc['pacer_doc']} ({doc_key}), page {page}{tail}"


def assertion_tags(status: str) -> list[str]:
    return [f"assertion:{status.upper()}"]


def content_facet(summary: str, *, label: str = "") -> dict:
    seed = label or summary[:120]
    return {
        "@id": uid(f"facet-{seed}"),
        "@type": ["uco-observable:ContentDataFacet", "uco-core:Facet"],
        "uco-core:description": summary,
    }


def source_observable(label: str, meta: dict) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": meta["file_name"],
        "uco-core:description": (
            f"PACER Document {meta['pacer_doc']} filed {meta['filed']}; "
            f"local bundle {LOCAL_REF}."
        ),
        "uco-core:hasFacet": [
            {
                "@id": uid(f"{label}-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": meta["file_name"],
                "uco-observable:extension": "pdf",
            },
            {
                "@id": uid(f"{label}-hash-facet"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [
                    {
                        "@id": uid(f"{label}-sha256"),
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": lit("xsd:hexBinary", meta["sha256"]),
                    }
                ],
            },
        ],
    }


def _alaska_midnight(date_str: str) -> str:
    """Date-only literal at local midnight with Alaska seasonal UTC offset."""
    month = int(date_str.split("-")[1])
    offset = "-08:00" if 4 <= month <= 10 else "-09:00"
    return f"{date_str}T00:00:00{offset}"


def media_series(
    label: str,
    name: str,
    description: str,
    *,
    capture_date: str,
    source_page: str,
    status: str = "ALLEGED",
    date_kind: str = "captureDate",
    performer_id: str | None = None,
    object_id: str | None = None,
    instrument_id: str | None = None,
) -> dict:
    # Media series are ObservableObjects, not Actions, so the sourced date is
    # recorded with uco-core:startTime (no domain restriction) instead of
    # uco-action:startTime. Midnight encodes date-only precision.
    node: dict = {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": name,
        "uco-core:description": f"{description} {src_ref('trial_brief', source_page)}",
        "uco-core:tag": assertion_tags(status) + ["evidence:csam-media-series"],
        "uco-core:startTime": lit("xsd:dateTime", _alaska_midnight(capture_date)),
        "uco-core:hasFacet": [
            content_facet(
                f"{date_kind}={capture_date}; platform=Snapchat; "
                f"nonGraphicSummary=true; status={status}",
                label=f"{label}-facet",
            )
        ],
    }
    if performer_id:
        node["uco-action:performer"] = {"@id": performer_id}
    if object_id:
        node["uco-action:object"] = {"@id": object_id}
    if instrument_id:
        node["uco-action:instrument"] = {"@id": instrument_id}
    return node


def coercion_event(
    label: str,
    name: str,
    description: str,
    *,
    source_page: str,
    approximate_period: str | None = None,
) -> dict:
    # The trial brief does not date individual coercion acts, so no
    # startTime is asserted. When the source anchors an approximate period
    # (e.g. "In around March 2019"), it is preserved as a facet string
    # rather than a fabricated xsd:dateTime.
    node: dict = {
        "@id": uid(label),
        "@type": ["uco-core:Event", "uco-core:UcoObject"],
        "uco-core:name": name,
        "uco-core:eventType": ["coercion method", "sex trafficking conduct"],
        "uco-core:description": f"{description} {src_ref('trial_brief', source_page)}",
        "uco-core:tag": assertion_tags("ALLEGED") + ["conduct:coercion"],
    }
    if approximate_period:
        node["uco-core:hasFacet"] = [
            content_facet(
                f"approximatePeriod={approximate_period}; datePrecision=as-stated-in-source",
                label=f"{label}-period-facet",
            )
        ]
    return node


def snapchat_post_evidence(
    label: str,
    name: str,
    description: str,
    *,
    source_page: str,
) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": name,
        "uco-core:description": f"{description} {src_ref('trial_brief', source_page)}",
        "uco-core:tag": assertion_tags("ALLEGED") + ["evidence:snapchat-post"],
        "uco-core:hasFacet": [content_facet("platform=Snapchat; evidenceType=social-media-post", label=f"{label}-facet")],
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
        "uco-core:description": f"{description} {src_ref('judgment', '5', section='Sheet 3D special condition')}",
        "uco-core:tag": ["supervision-condition:special", f"supervision-condition:{category}"],
        "uco-core:hasFacet": [content_facet(facet_summary, label=f"{label}-facet")],
    }


def build_graph() -> dict:
    # Core legal scaffold
    inv = uid("investigation")
    defendant = uid("defendant-moore")
    prosecution = uid("federal-prosecution")
    pretrial = uid("pretrial-phase")
    trial_phase = uid("trial-phase")
    sentencing_phase = uid("sentencing-phase")
    indictment = uid("grand-jury-indictment-doc2")
    trial_brief = uid("government-trial-brief-doc172")
    judgment = uid("criminal-judgment-doc251")
    charge1 = uid("federal-charge-1-production")
    charge2 = uid("federal-charge-2-possession")
    charge3 = uid("federal-charge-3-trafficking")
    mv1 = uid("minor-victim-1")
    forfeiture = uid("asset-forfeiture-allegation-1")
    production_incident = uid("csam-incident-production-vp")
    possession_incident = uid("csam-incident-possession-snapchat")
    trafficking_incident = uid("commercial-sex-exploitation-mv1")
    snap_vp = uid("snapchat-account-vp")
    snap_defendant = uid("snapchat-account-jayinglez80")
    court_dalaska = uid("location-d-alaska")
    mayfair_apartment = uid("location-mayfair-drive")
    judge = uid("judge-gleason")
    defense = uid("defense-elizabeth-fleming")
    ausa_ivers = uid("ausa-jennifer-ivers")
    ausa_ebell = uid("ausa-michael-ebell")
    usa_kuhn = uid("usa-john-kuhn")
    usao_ak = uid("org-usao-alaska")
    bop = uid("org-bureau-of-prisons")
    prison = uid("prison-sentence-240-months")
    supervised = uid("supervised-release-20-years")
    verdict = uid("jury-verdict-guilty-counts-1-3")
    src_indictment = uid("source-indictment-pdf")
    src_trial_brief = uid("source-trial-brief-pdf")
    src_judgment = uid("source-judgment-pdf")
    provenance = uid("provenance-pacer-bundle")
    brief_filing = uid("action-trial-brief-filing")
    interstate_stip = uid("interstate-commerce-stipulations")
    prior_record = uid("prior-alaska-felony-record")
    krista_callan = uid("witness-krista-callan")
    search_seizure = uid("search-warrant-seizure-summary")
    search_warrant = uid("action-search-warrant-mayfair-june-2019")
    le_interviews = uid("action-le-interviews-jan-feb-2020")
    skipthegames = uid("platform-skipthegames")
    payment_schedule = uid("payment-schedule-criminal-penalties")
    special_assessment = uid("monetary-special-assessment-300")
    restitution = uid("monetary-restitution-23070")
    # Granular CSAM media series
    media_april28_2019 = uid("media-series-april28-2019-oral")
    media_april28_intercourse = uid("media-series-april28-2019-intercourse")
    media_may2_2018 = uid("media-series-may2-2018-genitalia")
    media_may6_2018 = uid("media-series-may6-2018-oral")
    media_possession_dec2018 = uid("media-possession-dec25-2018")
    media_possession_jan2019 = uid("media-possession-jan7-2019")
    # Coercion / control events
    coerce_assault = uid("coercion-physical-assault")
    coerce_guns = uid("coercion-gun-possession-display")
    coerce_meth = uid("coercion-methamphetamine-fatigue")
    coerce_spenard = uid("coercion-spenard-street-walking")
    coerce_abortion = uid("coercion-forced-abortion-age15")
    coerce_rent_quota = uid("coercion-rent-quota")
    # Snapchat corroborating posts
    post_pregnancy_test = uid("snap-post-pregnancy-test")
    post_baby_supplies = uid("snap-post-baby-supplies")
    post_excited_father = uid("snap-post-excited-father")
    post_abortion_decision = uid("snap-post-abortion-decision")
    # Supervision special conditions (Sheet 3D)
    cond_minor_contact = uid("condition-minor-contact-restriction")
    cond_victim_no_contact = uid("condition-victim-no-contact")
    cond_minor_places = uid("condition-no-minor-likely-places")
    cond_polygraph = uid("condition-periodic-polygraph")
    cond_warrantless_search = uid("condition-warrantless-search-cp")
    cond_sex_offender_tx = uid("condition-sex-offender-treatment")
    cond_substance = uid("condition-substance-abuse-testing")

    graph: list[dict] = [
        {
            "@id": inv,
            "@type": ["case-investigation:Investigation", "cacontology:CACInvestigation"],
            "uco-core:name": "U.S. v. Jayshon Moore — D. Alaska ICAC Federal Case",
            "uco-core:description": (
                "Federal child exploitation and sex trafficking prosecution in the District of Alaska; "
                f"local reference {LOCAL_REF}. Trial brief Doc 172; judgment Doc 251."
            ),
            "cacontology:caseNumber": PACER_DOCKET,
            "cacontology:investigationStatus": "Sentenced",
            "uco-core:tag": [
                "caseStatus:sentenced-convicted",
                "disposition:guilty-verdict-and-sentence",
            ],
            "cacontology:jurisdiction": "District of Alaska",
            "cacontology:located_at": {"@id": court_dalaska},
            "cacontology:hasPhase": [
                {"@id": pretrial},
                {"@id": trial_phase},
                {"@id": sentencing_phase},
            ],
            "uco-core:object": [
                {"@id": src_indictment},
                {"@id": src_trial_brief},
                {"@id": src_judgment},
            ],
        },
        {
            "@id": defendant,
            "@type": ["uco-identity:Person", "cacontology:Subject", "uco-core:UcoObject"],
            "uco-core:name": "Jayshon Moore",
            "uco-core:description": (
                f"Defendant aka China; USM {USM_NUMBER}. Adjudicated guilty on counts 1–3 "
                f"after jury trial. {src_ref('judgment', '1')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "cacontology-legal-outcomes:chargedWith": [
                {"@id": charge1},
                {"@id": charge2},
                {"@id": charge3},
            ],
        },
        {
            "@id": prior_record,
            "@type": ["uco-core:Event", "uco-core:UcoObject"],
            "uco-core:name": "Prior Alaska Felony Record",
            "uco-core:description": (
                "Three prior Alaska felony convictions; most recent December 2010 felon-in-possession "
                "and controlled substance distribution (87 months + 3 years SR, case 3:10-cr-00044-TMB). "
                "SR began October 2017; violations in 2019 led to 45-day sentence. "
                f"{src_ref('trial_brief', '2', section='Section II.a')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED") + ["background:prior-convictions"],
        },
        {
            "@id": prosecution,
            "@type": ["cacontology-usa-federal:FederalProsecution", "uco-core:UcoObject"],
            "uco-core:name": f"Federal Prosecution — {PACER_DOCKET}",
            "uco-core:tag": [
                "caseStatus:sentenced-convicted",
                "disposition:guilty-verdict-and-sentence",
            ],
            "cacontology-legal-outcomes:hasLegalPhase": [
                {"@id": pretrial},
                {"@id": trial_phase},
                {"@id": sentencing_phase},
            ],
        },
        {
            "@id": pretrial,
            "@type": ["cacontology-legal-outcomes:PreTrialPhase", "uco-core:UcoObject"],
            "uco-core:name": "Pre-Trial Phase",
            "uco-core:description": (
                f"Indictment returned February 19, 2020; filed February 21, 2020. {src_ref('indictment', '1')}"
            ),
        },
        {
            "@id": trial_phase,
            "@type": ["cacontology-legal-outcomes:TrialPhase", "uco-core:UcoObject"],
            "uco-core:name": "Trial Phase",
            "uco-core:description": (
                f"Jury trial scheduled April 4, 2022 at 8:30 a.m., Courtroom 3, Anchorage. "
                f"{src_ref('trial_brief', '1')}"
            ),
            "uco-core:startTime": lit("xsd:dateTime", "2022-04-04T08:30:00-08:00"),
        },
        {
            "@id": sentencing_phase,
            "@type": ["cacontology-legal-outcomes:SentencingPhase", "uco-core:UcoObject"],
            "uco-core:name": "Sentencing Phase",
            "cacontology-legal-outcomes:phaseStatus": "judgment_entered",
            "uco-core:description": (
                f"AO 245B judgment imposed September 16, 2022. {src_ref('judgment', '1')}"
            ),
        },
        {
            "@id": indictment,
            "@type": ["cacontology:MultiDefendantIndictment", "uco-core:UcoObject"],
            "uco-core:name": "Grand Jury Indictment — Document 2",
            "uco-core:description": (
                "Three-count indictment: production (§ 2251), possession (§ 2252A), sex trafficking "
                f"of a minor (§ 1591); criminal forfeiture allegation under § 2253. {src_ref('indictment', '1-4')}"
            ),
            "cacontology:indictmentCounts": lit("xsd:nonNegativeInteger", 3),
        },
        {
            "@id": trial_brief,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Government Trial Brief — Document 172",
            "uco-core:description": (
                f"Anticipated trial evidence summary. {src_ref('trial_brief', '1-22')}"
            ),
            "uco-core:tag": ["pacer-document:trial-brief"],
        },
        {
            "@id": judgment,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Judgment in a Criminal Case (AO 245B) — Document 251",
            "uco-core:description": (
                "Adjudicated guilty counts 1–3; concurrent prison terms; 20-year supervised release; "
                f"restitution and special assessment; forfeiture dismissed. {src_ref('judgment', '1-7')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
        },
        {
            "@id": charge1,
            "@type": [
                "cacontology-legal-outcomes:FederalCharge",
                "cacontology-usa-federal:ChildPornographyProduction",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Count 1 — Production of Child Pornography (18 U.S.C. §§ 2251(a), (e))",
            "uco-core:description": (
                "Offense through June 7, 2019. Government alleges Moore used/employed V.P. to produce "
                "visual depictions via Snapchat. Interstate commerce via Snapchat and out-of-state phones. "
                f"{src_ref('trial_brief', '5-6')}; offense end {src_ref('judgment', '1')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 1),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. §§ 2251(a), (e)",
        },
        {
            "@id": charge2,
            "@type": ["cacontology-legal-outcomes:FederalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count 2 — Possession of Child Pornography (18 U.S.C. §§ 2252A(a)(5)(B), (b)(2))",
            "uco-core:description": (
                "Possession/access via Snapchat account jayinglez80; conduct December 25, 2018 through "
                f"January 7, 2019. {src_ref('indictment', '2')}; {src_ref('judgment', '1')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 2),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. §§ 2252A(a)(5)(B), (b)(2)",
        },
        {
            "@id": charge3,
            "@type": [
                "cacontology-legal-outcomes:FederalCharge",
                "cacontology-usa-federal:SexTraffickingOfMinors",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Count 3 — Sex Trafficking of a Minor (18 U.S.C. § 1591(a)(1))",
            "uco-core:description": (
                "Minor Victim 1 (V.P.). Alternative theories: knew/recklessly disregarded age OR had "
                "reasonable opportunity to observe minor status; plus force, fraud, coercion including "
                "physical assault, methamphetamine, gun possession, rent quota, Spenard street threat, "
                "and forced abortion at age 15. "
                f"{src_ref('indictment', '3')}; elements {src_ref('trial_brief', '8-10')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 3),
            "cacontology-legal-outcomes:statuteCitation": "18 U.S.C. § 1591(a)(1)",
        },
        {
            "@id": mv1,
            "@type": [
                "uco-identity:Person",
                "cacontology-trafficking:MinorTraffickingVictimRole",
                "cacontology-grooming:ChildVictim",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Minor Victim 1 (V.P.)",
            "uco-core:description": (
                "Minor female identified as Minor Victim 1 in indictment; trial brief identifies as "
                "15-year-old V.P., same individual for production, possession context, and trafficking. "
                "Turned 18 in 2020 per trial brief. "
                f"{src_ref('indictment', '3')}; {src_ref('trial_brief', '2-4')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED"),
            "uco-core:hasFacet": [
                content_facet(
                    "victimAgeAtConduct=15; minorContactProhibitedUnderAge=18; turn18Year=2020",
                    label="mv1-age-context-facet",
                )
            ],
        },
        {
            "@id": production_incident,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "Snapchat CSAM Production — V.P.",
            "uco-core:description": (
                f"Aggregate production conduct on V.P.'s Snapchat account. {src_ref('trial_brief', '2')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED"),
            "uco-action:performer": {"@id": defendant},
            "uco-action:object": {"@id": mv1},
            "uco-action:instrument": {"@id": snap_vp},
            "uco-core:hasFacet": [
                content_facet(
                    "platform=Snapchat; victimAge=15; nonGraphicSummary=true",
                    label="production-incident-facet",
                )
            ],
        },
        {
            "@id": possession_incident,
            "@type": ["cacontology:CSAMIncident", "uco-core:UcoObject"],
            "uco-core:name": "Snapchat CP Possession — jayinglez80",
            "uco-core:description": (
                f"Possession/access on defendant account jayinglez80. {src_ref('trial_brief', '2')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED"),
            "uco-action:performer": {"@id": defendant},
            "uco-action:instrument": {"@id": snap_defendant},
            "uco-core:hasFacet": [
                content_facet(
                    "accountIdentifier=jayinglez80; materialType=Snapchat account contents",
                    label="possession-incident-facet",
                )
            ],
        },
        {
            "@id": trafficking_incident,
            "@type": [
                "cacontology-trafficking:CommercialSexualExploitation",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Commercial Sex Exploitation — Minor Victim 1 / V.P.",
            "uco-core:description": (
                "Moore set prices, arranged dates, drove V.P., took earnings, imposed rent quota, "
                f"used force and substance coercion. {src_ref('trial_brief', '3-4')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED"),
            "uco-action:performer": {"@id": defendant},
            "uco-action:object": {"@id": mv1},
            "uco-action:location": {"@id": mayfair_apartment},
        },
        media_series(
            "media-series-april28-2019-oral",
            "April 28, 2019 — 13 oral sex videos (V.P. Snapchat)",
            "Moore filmed V.P. performing oral sex; 13 videos in series.",
            capture_date="2019-04-28",
            source_page="2",
            performer_id=defendant,
            object_id=mv1,
            instrument_id=snap_vp,
        ),
        media_series(
            "media-series-april28-2019-intercourse",
            "April 28, 2019 — intercourse continuation (V.P. filmed Moore)",
            "Continuation series: V.P. filmed Moore applying lube and intercourse; Moore coached performance.",
            capture_date="2019-04-28",
            source_page="2",
            performer_id=defendant,
            object_id=mv1,
            instrument_id=snap_vp,
        ),
        media_series(
            "media-series-may2-2018-genitalia",
            "May 2, 2018 — genitalia close-ups (2 videos + 1 photo)",
            "Moore filmed V.P.'s genitalia; victim covered face and breasts.",
            capture_date="2018-05-02",
            source_page="2",
            performer_id=defendant,
            object_id=mv1,
            instrument_id=snap_vp,
        ),
        media_series(
            "media-series-may6-2018-oral",
            "May 6, 2018 — five oral sex videos",
            "Moore filmed V.P. performing oral sex; five-video series.",
            capture_date="2018-05-06",
            source_page="2",
            performer_id=defendant,
            object_id=mv1,
            instrument_id=snap_vp,
        ),
        media_series(
            "media-possession-dec25-2018",
            "December 25, 2018 — V.P. masturbation video on jayinglez80",
            "Video V.P. sent to Moore's jayinglez80 account; Moore responded 'Wow.' "
            "Self-produced by V.P., possessed by Moore (count 2 conduct).",
            capture_date="2018-12-25",
            date_kind="sentDate",
            source_page="2",
            object_id=mv1,
            instrument_id=snap_defendant,
        ),
        media_series(
            "media-possession-jan7-2019",
            "January 7, 2019 — May 6 oral sex video on jayinglez80",
            "Copy of the May 6, 2018 oral sex video (filmed by Moore) sent to Moore's account.",
            capture_date="2019-01-07",
            date_kind="sentDate",
            source_page="2",
            performer_id=defendant,
            object_id=mv1,
            instrument_id=snap_defendant,
        ),
        coercion_event(
            "coercion-physical-assault",
            "Physical Assault of V.P.",
            "Moore assaulted V.P. multiple times including slamming head into wall corner and throwing her down stairs. Undated in source.",
            source_page="3",
        ),
        coercion_event(
            "coercion-gun-possession-display",
            "Gun Possession and Display",
            "Moore possessed guns in residence; Snapchat photos show Moore holding gun while hugging V.P. Undated in source.",
            source_page="2-3",
        ),
        coercion_event(
            "coercion-methamphetamine-fatigue",
            "Methamphetamine to Overcome Fatigue",
            "When V.P. was too tired for dates, Moore gave methamphetamine to wake her up. Undated in source.",
            source_page="3",
        ),
        coercion_event(
            "coercion-spenard-street-walking",
            "Spenard Street Prostitution Threat",
            "Moore forced V.P. to walk in high heels on Spenard strip known for street prostitution when she resisted. Undated in source.",
            source_page="3",
        ),
        coercion_event(
            "coercion-forced-abortion-age15",
            "Forced Abortion at Age 15",
            "While V.P. was 15 and pregnant with Moore's child, Moore forced her to have an abortion knowing her age.",
            source_page="3",
            approximate_period="while V.P. was 15 (per trial brief)",
        ),
        coercion_event(
            "coercion-rent-quota",
            "Rent Quota Commercial Sex Requirement",
            "Moore invited V.P. to move in only if she 'ho'ed' for him; set quota correlating to apartment rent.",
            source_page="3",
            approximate_period="around 2019-03 (after Callan moved out, per trial brief)",
        ),
        snapchat_post_evidence(
            "snap-post-pregnancy-test",
            "Snapchat — positive pregnancy test photo",
            "V.P. Snapchat post corroborating pregnancy.",
            source_page="3",
        ),
        snapchat_post_evidence(
            "snap-post-baby-supplies",
            "Snapchat — baby supplies purchase video",
            "V.P. video purchasing baby supplies.",
            source_page="3",
        ),
        snapchat_post_evidence(
            "snap-post-excited-father",
            "Snapchat — excited for Moore to become a father",
            "V.P. selfie message re fatherhood.",
            source_page="3",
        ),
        snapchat_post_evidence(
            "snap-post-abortion-decision",
            "Snapchat — abortion decision message",
            "Final message that they decided on abortion instead.",
            source_page="3",
        ),
        {
            "@id": krista_callan,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Krista Callan",
            "uco-core:description": (
                "Moore's adult girlfriend until ~March 2019; moved out of Mayfair Drive apartment; "
                f"expected trial witness. {src_ref('trial_brief', '3', section='Section II.c; witness list IV.d')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED") + ["role:cohabitant", "role:potential-witness"],
        },
        {
            "@id": mayfair_apartment,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "Mayfair Drive Apartment — Anchorage",
            "uco-core:description": (
                f"Shared residence; search warrant executed June 2019. {src_ref('trial_brief', '3-4')}"
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("mayfair-address-facet"),
                    "@type": "uco-location:SimpleAddressFacet",
                    "uco-location:locality": "Anchorage",
                    "uco-location:region": "Alaska",
                }
            ],
        },
        {
            "@id": search_seizure,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Mayfair Search Warrant Seizure Summary",
            "uco-core:description": (
                "Items seized: V.P. clothing, condoms, lube, price notebook; associate removal observed."
            ),
            "uco-core:hasFacet": [
                content_facet(
                    "seizedItems=clothing|condoms|lube|price-notebook; associateTamperingObserved=true",
                    label="search-seizure-facet",
                )
            ],
        },
        {
            "@id": search_warrant,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Search Warrant Execution — Mayfair Drive (June 2019)",
            "uco-core:description": (
                "Law enforcement executed search warrant after June 2019 arrests; seized V.P. clothing, "
                "condoms, lube, price notebook. Associates actively removing items when agents arrived. "
                "Source gives month precision only (June 2019); no startTime asserted. "
                f"{src_ref('trial_brief', '4')}"
            ),
            "uco-action:location": {"@id": mayfair_apartment},
            "uco-action:result": {"@id": search_seizure},
        },
        {
            "@id": le_interviews,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Law Enforcement Interviews — January/February 2020",
            "uco-core:description": (
                "Law enforcement interviewed Moore in January and February 2020. Moore admitted "
                "knowing V.P. was underage; said she 'probably could have' sent Snapchat videos; "
                "volunteered neighbors had WiFi; used terms 'turning dates/tricks,' 'in calls,' "
                "'turned out,' 'selling pussy'; denied trafficking knowledge. Source gives month "
                "precision only; no startTime asserted. "
                f"{src_ref('trial_brief', '4', section='Section II.e')}"
            ),
            "uco-action:object": {"@id": defendant},
            "uco-core:tag": assertion_tags("ALLEGED"),
        },
        {
            "@id": interstate_stip,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Interstate Commerce Stipulations (Parties)",
            "uco-core:description": (
                "Parties intend to stipulate: Skipthegames.com ads affect interstate commerce; Snapchat "
                "transports images/videos in interstate commerce; smartphones manufactured outside Alaska. "
                f"{src_ref('trial_brief', '5-6', section='Section III.b')}"
            ),
            "uco-core:tag": ["legal-element:interstate-commerce"],
        },
        {
            "@id": skipthegames,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Skipthegames.com — V.P. prostitution ads",
            "uco-core:description": (
                "Online prostitution ads with photos from Mayfair residence; associated to Moore's phone; "
                f"two ads posted via neighbor WiFi. {src_ref('trial_brief', '4')}"
            ),
            "uco-core:tag": assertion_tags("ALLEGED") + ["platform:escort-advertising"],
        },
        {
            "@id": snap_defendant,
            "@type": ["uco-observable:ApplicationAccount", "uco-core:UcoObject"],
            "uco-core:name": "Snapchat — jayinglez80",
            "uco-core:description": (
                f"Defendant account named in indictment count 2. {src_ref('indictment', '2')}"
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("snap-defendant-facet"),
                    "@type": "uco-observable:AccountFacet",
                    "uco-observable:accountIdentifier": "jayinglez80",
                }
            ],
        },
        {
            "@id": snap_vp,
            "@type": ["uco-observable:ApplicationAccount", "uco-core:UcoObject"],
            "uco-core:name": "Snapchat — V.P. account",
            "uco-core:description": (
                f"Victim account obtained by law enforcement 2019. {src_ref('trial_brief', '2')}"
            ),
        },
        {
            "@id": forfeiture,
            "@type": ["cacontology-asset-forfeiture:AssetForfeitureAction", "uco-core:UcoObject"],
            "uco-core:name": "Criminal Forfeiture Allegation 1 (18 U.S.C. § 2253)",
            "uco-core:description": (
                f"Re-alleged for counts 1–2; dismissed on motion of United States. {src_ref('judgment', '1')}"
            ),
            "cacontology-asset-forfeiture:relatedCriminalCharges": [
                {"@id": charge1},
                {"@id": charge2},
            ],
        },
        {
            "@id": verdict,
            "@type": ["cacontology-legal-outcomes:ConvictionRecord", "uco-core:UcoObject"],
            "uco-core:name": "Jury Verdict — Guilty Counts 1–3",
            "uco-core:description": (
                "Found guilty on counts 1 through 3 after not guilty plea; conviction date "
                f"recorded as date of imposition of judgment. {src_ref('judgment', '1')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "cacontology-legal-outcomes:convictionDate": lit(
                "xsd:dateTime", "2022-09-16T00:00:00-08:00"
            ),
            "cacontology-legal-outcomes:convictionType": "jury_verdict",
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 3),
        },
        {
            "@id": prison,
            "@type": ["cacontology-legal-outcomes:PrisonSentence", "uco-core:UcoObject"],
            "uco-core:name": "240-Month Concurrent Federal Prison Sentence",
            "uco-core:description": (
                "240 months count 1, 120 months count 2, 240 months count 3 — concurrent; remanded to "
                f"U.S. Marshal. {src_ref('judgment', '2')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "cacontology-legal-outcomes:sentenceDurationMonths": lit("xsd:integer", 240),
        },
        {
            "@id": supervised,
            "@type": ["cacontology-legal-outcomes:SupervisedRelease", "uco-core:UcoObject"],
            "uco-core:name": "20-Year Term of Supervised Release",
            "uco-core:description": (
                "Twenty-year supervised release on counts 1–3 concurrent, with seven special conditions "
                f"on Sheet 3D. {src_ref('judgment', '3-5')}"
            ),
            "uco-core:tag": assertion_tags("ADJUDICATED"),
            "uco-core:hasFacet": [
                content_facet("sentenceDurationYears=20; concurrentCounts=1|2|3", label="supervised-release-facet"),
            ],
        },
        supervision_condition(
            "condition-minor-contact-restriction",
            "Minor Contact Restriction (Own Children Exception)",
            "minor-contact-restriction",
            "No contact with persons under 18 without adult supervision except own minor children; "
            "advance written probation approval required.",
            "minorContactProhibitedUnderAge=18; ownChildrenException=true; requiresWrittenApproval=true",
        ),
        supervision_condition(
            "condition-victim-no-contact",
            "Victim No-Contact Order",
            "victim-no-contact",
            "No contact with victim including third-party communication; may not enter victim premises.",
            "victimContactProhibited=true; thirdPartyContactProhibited=true; premisesRestriction=true",
        ),
        supervision_condition(
            "condition-no-minor-likely-places",
            "No Places Where Children Under 18 Likely",
            "minor-places-restriction",
            "Must not go to or remain at places where children under 18 are likely (parks, schools, playgrounds, childcare).",
            "restrictedAgeUnder=18; restrictedPlaceTypes=parks|schools|playgrounds|childcare",
        ),
        supervision_condition(
            "condition-periodic-polygraph",
            "Periodic Polygraph Testing",
            "polygraph-monitoring",
            "Submit to periodic polygraph at probation officer discretion for supervision/treatment compliance.",
            "polygraphRequired=true; discretion=probationOfficer",
        ),
        supervision_condition(
            "condition-warrantless-search-cp",
            "Warrantless Search for CP Contraband",
            "probation-search-cp",
            "Warrantless search of person, residence, vehicle, employment, and electronics upon reasonable suspicion; "
            "includes computers and electronic storage that may contain CSAM.",
            "searchAuthority=federalProbationOfficer|lawEnforcement; standard=reasonableSuspicion; "
            "contrabandIncludes=electronicMedia|childPornography",
        ),
        supervision_condition(
            "condition-sex-offender-treatment",
            "Sex Offender Assessment and Treatment",
            "sex-offender-treatment",
            "Participate in sex offender assessment/treatment until released; may include polygraph; "
            "waive confidentiality; pay costs; refusal is violation.",
            "polygraph=permitted; confidentialityWaived=true; defendantPaysCost=true; refusalIsViolation=true",
            extra_types=["cacontology-registry:RegistrationRequirement"],
        ),
        supervision_condition(
            "condition-substance-abuse-testing",
            "Substance Abuse Assessment and Urinalysis",
            "substance-abuse-treatment",
            "Substance abuse assessment and treatment; up to 12 urinalysis tests per month.",
            "maxUrinalysisPerMonth=12; assessmentRequired=true; treatmentRequired=true",
        ),
        {
            "@id": special_assessment,
            "@type": ["cacontology-legal-outcomes:MonetaryPenalty", "uco-core:UcoObject"],
            "uco-core:name": "Special Assessment — $300.00",
            "uco-core:description": (
                f"Special assessment of $300.00 per judgment monetary penalties sheet. {src_ref('judgment', '6')}"
            ),
            "uco-core:hasFacet": [
                content_facet("amountUSD=300.00; penaltyType=specialAssessment", label="special-assessment-facet")
            ],
        },
        {
            "@id": restitution,
            "@type": ["cacontology-legal-outcomes:MonetaryPenalty", "uco-core:UcoObject"],
            "uco-core:name": "Restitution — $23,070.00",
            "uco-core:description": (
                f"Restitution ordered to victim(s) per judgment Sheet 5. {src_ref('judgment', '6')}"
            ),
            "uco-core:hasFacet": [
                content_facet("amountUSD=23070.00; penaltyType=restitution", label="restitution-facet")
            ],
        },
        {
            "@id": payment_schedule,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Schedule of Payments — $23,370.00 Total",
            "uco-core:description": (
                "Lump sum $23,370.00 due immediately per Sheet 6 Option A/F; unpaid balance during "
                "incarceration at 50% BOP wages and during supervision at minimum 10% gross monthly "
                "income or $25/month, whichever greater; interest not waived. "
                f"{src_ref('judgment', '7')}"
            ),
            "uco-core:tag": ["payment-schedule:hybrid-lump-sum-and-installments"],
            "uco-core:hasFacet": [
                content_facet(
                    "totalAmountUSD=23370.00; lumpSumImmediate=23370.00; "
                    "incarcerationRate=50%OfBOPWages; supervisionMinimum=10%GrossMonthlyOr25USD; "
                    "interestWaived=false",
                    label="payment-schedule-facet",
                )
            ],
        },
        {
            "@id": court_dalaska,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": "United States District Court, District of Alaska",
        },
        {
            "@id": judge,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Sharon L. Gleason",
            "uco-core:description": (
                f"Chief United States District Judge. {src_ref('judgment', '1')}"
            ),
        },
        {
            "@id": defense,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Elizabeth Fleming",
            "uco-core:description": (
                f"Defendant's attorney of record. {src_ref('judgment', '1')}"
            ),
        },
        {
            "@id": ausa_ivers,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Jennifer Ivers",
            "uco-core:description": "Assistant United States Attorney.",
        },
        {
            "@id": ausa_ebell,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Michael Ebell",
            "uco-core:description": "Assistant United States Attorney (trial brief).",
        },
        {
            "@id": usa_kuhn,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "John E. Kuhn, Jr.",
            "uco-core:description": "United States Attorney.",
        },
        {
            "@id": usao_ak,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "U.S. Attorney's Office, District of Alaska",
        },
        {
            "@id": bop,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "United States Bureau of Prisons",
        },
        source_observable("source-indictment-pdf", SOURCE_DOCS["indictment"]),
        source_observable("source-trial-brief-pdf", SOURCE_DOCS["trial_brief"]),
        source_observable("source-judgment-pdf", SOURCE_DOCS["judgment"]),
        {
            "@id": brief_filing,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Government Trial Brief Filing (Doc 172)",
            "uco-action:object": {"@id": src_trial_brief},
            "uco-action:result": {"@id": trial_brief},
            "uco-action:startTime": lit("xsd:dateTime", "2022-03-28T00:00:00-08:00"),
        },
        {
            "@id": provenance,
            "@type": ["case-investigation:ProvenanceRecord"],
            "uco-core:description": (
                "Merged PACER bundle graph from indictment, trial brief, and judgment PDFs "
                "via CASE/UCO MCP extraction plus CAC modeling with page-anchored descriptions."
            ),
            "case-investigation:wasInformedBy": [
                {"@id": src_indictment},
                {"@id": src_trial_brief},
                {"@id": src_judgment},
            ],
        },
    ]

    # Production series only — the December 2018/January 2019 items are
    # count 2 possession conduct and are wired to possession_incident below.
    production_media_nodes = [
        media_april28_2019,
        media_april28_intercourse,
        media_may2_2018,
        media_may6_2018,
    ]
    coercion_nodes = [
        coerce_assault,
        coerce_guns,
        coerce_meth,
        coerce_spenard,
        coerce_abortion,
        coerce_rent_quota,
    ]
    post_nodes = [
        post_pregnancy_test,
        post_baby_supplies,
        post_excited_father,
        post_abortion_decision,
    ]
    condition_nodes = [
        cond_minor_contact,
        cond_victim_no_contact,
        cond_minor_places,
        cond_polygraph,
        cond_warrantless_search,
        cond_sex_offender_tx,
        cond_substance,
    ]

    relationships = [
        rel(inv, prosecution, "Relates_To"),
        rel(inv, indictment, "Relates_To"),
        rel(inv, charge1, "Relates_To"),
        rel(inv, charge2, "Relates_To"),
        rel(inv, charge3, "Relates_To"),
        rel(inv, production_incident, "Relates_To"),
        rel(inv, possession_incident, "Relates_To"),
        rel(inv, trafficking_incident, "Relates_To"),
        rel(inv, search_warrant, "Relates_To"),
        rel(prosecution, indictment, "Relates_To"),
        rel(prosecution, trial_brief, "Relates_To"),
        rel(prosecution, judgment, "Relates_To"),
        rel(indictment, charge1, "Relates_To"),
        rel(indictment, charge2, "Relates_To"),
        rel(indictment, charge3, "Relates_To"),
        rel(indictment, forfeiture, "Relates_To"),
        rel(charge1, production_incident, "Relates_To"),
        rel(charge2, possession_incident, "Relates_To"),
        rel(charge3, trafficking_incident, "Relates_To"),
        rel(charge3, mv1, "Relates_To"),
        rel(charge1, interstate_stip, "Relates_To"),
        rel(charge2, interstate_stip, "Relates_To"),
        rel(charge3, interstate_stip, "Relates_To"),
        rel(trafficking_incident, mv1, "Relates_To"),
        rel(trafficking_incident, skipthegames, "Relates_To"),
        rel(production_incident, mv1, "Relates_To"),
        rel(production_incident, snap_vp, "Relates_To"),
        rel(possession_incident, snap_defendant, "Relates_To"),
        rel(defendant, prior_record, "Relates_To"),
        rel(defendant, krista_callan, "Relates_To"),
        rel(trial_brief, charge1, "Relates_To"),
        rel(trial_brief, charge2, "Relates_To"),
        rel(trial_brief, charge3, "Relates_To"),
        rel(trial_brief, production_incident, "Relates_To"),
        rel(trial_brief, trafficking_incident, "Relates_To"),
        rel(brief_filing, trial_brief, "Results_In"),
        rel(judgment, verdict, "Records"),
        rel(verdict, charge1, "Convicted_On"),
        rel(verdict, charge2, "Convicted_On"),
        rel(verdict, charge3, "Convicted_On"),
        rel(judgment, prison, "Imposes"),
        rel(judgment, supervised, "Imposes"),
        rel(judgment, special_assessment, "Imposes"),
        rel(judgment, restitution, "Imposes"),
        rel(judgment, payment_schedule, "Imposes"),
        rel(judgment, judge, "Signed_By"),
        rel(payment_schedule, special_assessment, "Includes"),
        rel(payment_schedule, restitution, "Includes"),
        rel(defendant, prison, "Sentenced_To"),
        rel(defendant, supervised, "Subject_To"),
        rel(defendant, defense, "Represented_By"),
        rel(defendant, verdict, "Subject_Of"),
        rel(defendant, le_interviews, "Subject_Of"),
        rel(prison, bop, "Relates_To"),
        rel(prosecution, usao_ak, "Relates_To"),
        rel(ausa_ivers, usao_ak, "Affiliated_With"),
        rel(ausa_ebell, usao_ak, "Affiliated_With"),
        rel(usa_kuhn, usao_ak, "Affiliated_With"),
        rel(provenance, src_indictment, "Derived_From"),
        rel(provenance, src_trial_brief, "Derived_From"),
        rel(provenance, src_judgment, "Derived_From"),
        rel(search_warrant, search_seizure, "Results_In"),
        rel(search_warrant, mayfair_apartment, "Located_At"),
        rel(krista_callan, mayfair_apartment, "Relates_To"),
    ]

    for media_id in production_media_nodes:
        relationships.append(rel(media_id, production_incident, "Part_Of"))
        relationships.append(rel(defendant, media_id, "Created"))
        relationships.append(rel(media_id, mv1, "Relates_To"))
        relationships.append(rel(media_id, snap_vp, "Relates_To"))

    for media_id in (media_possession_dec2018, media_possession_jan2019):
        relationships.append(rel(media_id, possession_incident, "Part_Of"))
        relationships.append(rel(media_id, mv1, "Relates_To"))
        relationships.append(rel(media_id, snap_defendant, "Relates_To"))
    # The January 7, 2019 item is a copy of the May 6, 2018 production series.
    relationships.append(rel(media_possession_jan2019, media_may6_2018, "Derived_From"))

    for coerce_id in coercion_nodes:
        relationships.append(rel(coerce_id, trafficking_incident, "Relates_To"))
        relationships.append(rel(coerce_id, defendant, "Relates_To"))
        relationships.append(rel(coerce_id, mv1, "Relates_To"))

    for post_id in post_nodes:
        relationships.append(rel(post_id, coerce_abortion, "Corroborates"))
        relationships.append(rel(post_id, snap_vp, "Relates_To"))
        relationships.append(rel(post_id, mv1, "Relates_To"))

    for cond_id in condition_nodes:
        relationships.append(rel(supervised, cond_id, "Requires"))

    graph.extend(relationships)

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "cacontology": "https://cacontology.projectvic.org#",
            "cacontology-asset-forfeiture": "https://cacontology.projectvic.org/asset-forfeiture#",
            "cacontology-grooming": "https://cacontology.projectvic.org/grooming#",
            "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
            "cacontology-registry": "https://cacontology.projectvic.org/sex-offender-registry#",
            "cacontology-trafficking": "https://cacontology.projectvic.org/trafficking#",
            "cacontology-usa-federal": "https://cacontology.projectvic.org/usa-federal-law#",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    node_count = len(payload["@graph"])
    print(f"Graph nodes: {node_count}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
