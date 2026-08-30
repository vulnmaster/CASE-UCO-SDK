#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Keel & Panchal (E.D. La. elder fraud).

Case 2:22-cr-00115-ILRL-KWR (E.D. La., Section "B"): federal prosecution of
two money couriers for a transnational elder-fraud call-center network
(headquartered in India per the factual basis). Co-conspirators cold-called
elderly victims while impersonating U.S. Department of Treasury / Department
of Justice agents, claimed the victims' bank accounts were implicated in
crime, and directed the victims to hand over cash "for safekeeping" via
Green Dot prepaid cards, mailed packages, and in-person pickups. Keel was
arrested on 2022-04-04 in a controlled-delivery sting run by the Tangipahoa
Parish Sheriff's Office; Homeland Security Investigations then attributed
the wider conspiracy ($4,498,327 in actual and attempted losses to 31 U.S.
victims since 2021-10-22) through Keel's seized phone, cell-site data, and
airline/hotel/payment-card records.

Sources (PACER):
  - Criminal docket (all defendants), retrieved 2026-06-27
  - Superseding Indictment: Document 28 (filed 2022-10-13)
  - Factual Basis (Keel): Document 61 (filed 2023-06-14)
  - Judgment (Keel): Document 80 (entered 2023-10-25/26)

MCP extraction artifacts: examples/pacer/edla_2022_cr_00115/mcp_outputs/

Extension: extensions/legalproc (Legal Process and Procedure Extension) —
exercised here on a conspiracy charge, an aiding-and-abetting count, a
superseding-indictment chain, per-defendant dispositions (guilty plea for
Keel, government dismissal for Panchal), a deferred/amended restitution
order, and a forfeiture notice with a substitute-assets money judgment.

Cyber vs. non-cyber conventions (docs/recipes/legal-process-modeling.md):
  - Genuinely cyber artifacts (the seized phone, phone accounts, spoofed
    calls, text messages, payment card, cell-site records, the victim's
    compromised computer) are UCO observables with facets.
  - Physical items that never live in cyberspace (cash boxes, the decoy
    box, the rental car) are uco-core:UcoObject dual-typed with
    gufo:FunctionalComplex via the CDO gUFO alignment profile.
  - Court dates are date-only facts rendered at local midnight Central
    time; quoted scheme language is kept verbatim from the filings.
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

CASE_ID = "keel-panchal-edla-2022-elder-fraud"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "keel-panchal-edla-2022-elder-fraud.jsonld"

PACER_DOCKET = "2:22-cr-00115-ILRL-KWR"
MAGISTRATE_DOCKET = "2:22-mj-00062-DM"
LOCAL_REF = "outside_pacer -- elder fraud"

SOURCE_DOCS = {
    "docket": {
        "file_name": "pacer -- elder fraud -- docket.pdf",
        "sha256": "8bfd48d3b8bd7c23bd5df6c8977e256b8f1881df9f21a3864715c3ec76156fc0",
        "pacer_doc": "criminal docket sheet",
        "filed": "2026-06-27",
    },
    "superseding_indictment": {
        "file_name": "pacer -- elder fraud -- superseding indictment.pdf",
        "sha256": "058e5f3b83f40333ee7c0d9ce550aab3447c656e161a1c247c74e5b3c0cc5541",
        "pacer_doc": "28",
        "filed": "2022-10-13",
    },
    "factual_basis": {
        "file_name": "pacer -- elder fraud -- factual basis.pdf",
        "sha256": "6a928ed1659291f74aff47fbe448c30353a97f0a84b68e3ab0ea7bc75d2ffc32",
        "pacer_doc": "61",
        "filed": "2023-06-14",
    },
    "judgment": {
        "file_name": "pacer -- elder fraud -- judgment.pdf",
        "sha256": "002bc138648280d2c03c2428637ec4d66fb2c1ed61357beb80377d4232bba7dc",
        "pacer_doc": "80",
        "filed": "2023-10-25",
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


def central_midnight(date_str: str) -> str:
    """Date-only court fact rendered at local midnight Central time.

    E.D. La.: CDT (-05:00) roughly March-November, CST (-06:00) otherwise.
    Month-level approximation is sufficient for filing dates.
    """
    month = int(date_str.split("-")[1])
    offset = "-05:00" if 4 <= month <= 10 else "-06:00"
    return f"{date_str}T00:00:00{offset}"


def src_ref(doc_key: str, detail: str) -> str:
    doc = SOURCE_DOCS[doc_key]
    return f"Source: PACER Doc {doc['pacer_doc']} ({doc_key}), {detail}"


def source_observable(label: str, meta: dict) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": meta["file_name"],
        "uco-core:description": (
            f"PACER document ({meta['pacer_doc']}) filed {meta['filed']} in "
            f"{PACER_DOCKET} (E.D. La.); local bundle '{LOCAL_REF}'."
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


# ---------------------------------------------------------------------------
# Charge table from the Superseding Indictment (Doc 28) plus the original
# indictment (D.E. 10). Superseding counts carry per-defendant dispositions.
# ---------------------------------------------------------------------------
CHARGES = [
    {
        "label": "charge-count1s",
        "count_label": "Count 1s",
        "counts": [1],
        "instrument": "instrument-superseding",
        "name": "Conspiracy to Commit Wire Fraud",
        "statute": "18 U.S.C. § 1349 (object offense 18 U.S.C. § 1343)",
        "felony_class": "Felony",
        "offense_form": "conspiracy",
        "dispositions": [
            "convicted-by-plea (Keel, 2023-06-14)",
            "dismissed-on-government-motion (Panchal, 2023-09-05)",
        ],
        "description": (
            "Beginning at least by 2022-02-09 and continuing until at least "
            "2022-04-04, in the Eastern District of Louisiana and elsewhere, "
            "Keel and Panchal and others known and unknown conspired to "
            "devise a scheme to defraud individuals of money by making false "
            "material representations regarding their identity and the "
            "safety of the victims' funds — impersonating U.S. federal "
            "agents by phone, claiming victims' bank accounts were "
            "implicated in crime, and directing transfers via mail, Green "
            "Dot cards, and in-person cash handoffs — causing interstate "
            "wirings in furtherance of the scheme. The object offense, wire "
            "fraud (18 U.S.C. § 1343), is cited in the indictment but not "
            "charged as a separate count. "
            + src_ref("superseding_indictment", "Count 1, sections A-D")
        ),
    },
    {
        "label": "charge-count2s",
        "count_label": "Count 2s",
        "counts": [2],
        "instrument": "instrument-superseding",
        "name": "False Personation of an Employee or Officer of the United States; Aiding and Abetting",
        "statute": "18 U.S.C. §§ 912 & 2",
        "felony_class": "Felony",
        "offense_form": "substantive",
        "dispositions": [
            "convicted-by-plea (Keel, 2023-06-14)",
            "dismissed-on-government-motion (Panchal, 2023-09-05)",
        ],
        "description": (
            "On or about 2022-04-04, in the Eastern District of Louisiana, "
            "Keel and Panchal falsely assumed and pretended to be officers "
            "and employees of the United States — agents of the U.S. "
            "Department of Treasury — and in such assumed character told "
            "Victim A that she must entrust her money to them. Charged with "
            "aiding and abetting under 18 U.S.C. § 2. "
            + src_ref("superseding_indictment", "Count 2")
        ),
    },
    {
        "label": "charge-count1-orig",
        "count_label": "Count 1",
        "counts": [1],
        "instrument": "instrument-indictment",
        "name": "Conspiracy to Commit Wire Fraud (original indictment)",
        "statute": "18 U.S.C. § 1349",
        "felony_class": "Felony",
        "offense_form": "conspiracy",
        "dispositions": ["dismissed-on-government-motion (Keel, 2023-10-26)"],
        "description": (
            "Original Count 1 against Keel, superseded by Count 1s and "
            "dismissed on the government's motion after sentencing. "
            + src_ref("docket", "terminated counts; D.E. 79, 82")
        ),
    },
    {
        "label": "charge-count2-orig",
        "count_label": "Count 2",
        "counts": [2],
        "instrument": "instrument-indictment",
        "name": "False Personation; Aiding and Abetting (original indictment)",
        "statute": "18 U.S.C. §§ 912 & 2",
        "felony_class": "Felony",
        "offense_form": "substantive",
        "dispositions": ["dismissed-on-government-motion (Keel, 2023-10-26)"],
        "description": (
            "Original Count 2 against Keel, superseded by Count 2s and "
            "dismissed on the government's motion after sentencing. "
            + src_ref("docket", "terminated counts; D.E. 79, 82")
        ),
    },
]


def build_graph() -> dict:
    graph: list[dict] = []

    # ------------------------------------------------------------------
    # Investigation container and source documents
    # ------------------------------------------------------------------
    investigation = uid("investigation")
    graph.append(
        {
            "@id": investigation,
            "@type": "case-investigation:Investigation",
            "uco-core:name": f"United States v. Keel & Panchal, {PACER_DOCKET} (E.D. La.)",
            "legalproc:caseIdentifier": PACER_DOCKET,
            "uco-core:description": (
                "Elder-fraud prosecution of two money couriers for a "
                "transnational government-impersonation call-center scheme. "
                "Co-conspirators phoned elderly victims (Victim A, 77, "
                "Hammond, LA; Victim B, 76, Washington State; Victim C, 80, "
                "Bossier Parish, LA), posed as U.S. Treasury / DOJ agents, "
                "claimed the victims' bank accounts were implicated in "
                "crime, and collected cash 'for safekeeping' via Green Dot "
                "cards, mailed packages, and in-person pickups. Keel was "
                "arrested 2022-04-04 in a Tangipahoa Parish Sheriff's "
                "Office controlled-delivery sting; HSI's follow-on federal "
                "investigation attributed $4,498,327 in actual and "
                "attempted losses to 31 U.S. victims since 2021-10-22. "
                f"Docket filed 2022-06-02 (magistrate case "
                f"{MAGISTRATE_DOCKET}); terminated 2023-10-25. Judge Ivan "
                "L.R. Lemelle; Magistrate Judge Karen Wells Roby. "
                + src_ref("docket", "caption") + "; "
                + src_ref("factual_basis", "pp. 1-8")
            ),
        }
    )

    doc_ids: dict[str, str] = {}
    for key, meta in SOURCE_DOCS.items():
        node = source_observable(f"doc-{key}", meta)
        doc_ids[key] = node["@id"]
        graph.append(node)
        graph.append(rel(node["@id"], investigation, "part_of"))

    # ------------------------------------------------------------------
    # People and organizations
    # ------------------------------------------------------------------
    keel = uid("person-keel")
    panchal = uid("person-panchal")
    king_k = uid("person-king-k")
    victim_a = uid("person-victim-a")
    victim_b = uid("person-victim-b")
    victim_c = uid("person-victim-c")
    victim_a_son = uid("person-victim-a-son")
    det_damato = uid("person-det-damato")
    sa_candebat = uid("person-sa-candebat")
    fraud_network = uid("org-fraud-network")
    tpso = uid("org-tpso")
    jpso = uid("org-jpso")
    hsi = uid("org-hsi")
    usao = uid("org-usao-edla")
    green_dot = uid("org-green-dot-bank")

    graph.extend(
        [
            {
                "@id": keel,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Christopher L. Keel",
                "uco-core:description": (
                    "Defendant (1), resident of Tampa, Florida; USM number "
                    "03691-510. Money courier who collected cash boxes from "
                    "Victim A (Hammond, LA) and Victim B (South Center, WA) "
                    "while co-conspirators impersonated federal agents by "
                    "phone; texting with co-conspirators about courier "
                    "'work' since at least 2021-10-22. Arrested 2022-04-04 "
                    "in a controlled-delivery sting. Pleaded guilty "
                    "2023-06-14 to Counts 1s and 2s; sentenced 2023-10-25 "
                    "to 125 months. "
                    + src_ref("docket", "defendant 1 caption") + "; "
                    + src_ref("factual_basis", "pp. 1-8")
                ),
            },
            {
                "@id": panchal,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Jayesh J. Panchal",
                "uco-core:description": (
                    "Defendant (2), resident of Hicksville, New York; added "
                    "by the superseding indictment (Doc 28). Drove Keel to "
                    "the Hammond pickup, flew with him on courier trips, "
                    "booked both men's flights with his Citibank Master "
                    "Card ending 5885, and rented the car observed at "
                    "Victim C's residence. Charges dismissed on the "
                    "government's motion 2023-09-05 (D.E. 64, 65). "
                    + src_ref("docket", "defendant 2 caption") + "; "
                    + src_ref("factual_basis", "pp. 4-5, 7-8")
                ),
            },
            {
                "@id": king_k,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "\"King K\" (unindicted co-conspirator)",
                "uco-core:description": (
                    "Contact saved as 'King K' on Keel's phone; dispatched "
                    "courier 'work' to Keel from at least 2021-10-22 "
                    "('work resumes next week... 1 runner changed his mind "
                    "and stopped working since 9th September'). Keel also "
                    "held contact information for an individual located in "
                    "India, which agents identified as the headquarters of "
                    "the conspiracy. "
                    + src_ref("factual_basis", "p. 8")
                ),
            },
            {
                "@id": victim_a,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Victim A",
                "uco-core:description": (
                    "77-year-old woman, resident of Hammond, Tangipahoa "
                    "Parish, Louisiana (E.D. La.). Told by callers posing "
                    "as U.S. Treasury agents that her accounts were "
                    "implicated in fraud; transferred $60,000 via Green Dot "
                    "cards from 2022-03-07 and handed a $60,000 cash box to "
                    "Keel on 2022-04-03; a further $400,000 withdrawal on "
                    "2022-04-04 was halted by bank employees and her adult "
                    "son. " + src_ref("superseding_indictment", "Count 1 "
                    "paras. A.3, D.5-D.11") + "; "
                    + src_ref("factual_basis", "pp. 1-3")
                ),
            },
            {
                "@id": victim_b,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Victim B",
                "uco-core:description": (
                    "76-year-old woman, resident of Washington State, whose "
                    "husband was ill with cancer. Defrauded of $300,000 "
                    "after a tech-support pop-up scam on 2022-02-09 led to "
                    "callers posing as DOJ agents: mailed ~$140,000 cash "
                    "via UPS, handed $60,000 to an unknown female courier "
                    "on 2022-02-24 (Tukwila, WA), and handed a $100,000 "
                    "cash box to Keel on 2022-03-11 (South Center, WA). "
                    "Kept receipts and a journal of every transaction. "
                    + src_ref("superseding_indictment", "Count 1 paras. "
                    "A.4, D.3-D.4") + "; "
                    + src_ref("factual_basis", "pp. 6-7")
                ),
            },
            {
                "@id": victim_c,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Victim C",
                "uco-core:description": (
                    "80-year-old woman residing in Bossier Parish, "
                    "Louisiana. Withdrew $36,000 at purported 'agents'' "
                    "demand for a pickup at her residence on or about "
                    "2022-03-23; local police interdicted the pickup, and "
                    "the approaching vehicle — a rental car rented by "
                    "Panchal — turned around and left. "
                    + src_ref("factual_basis", "pp. 7-8")
                ),
            },
            {
                "@id": victim_a_son,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Adult son of Victim A",
                "uco-core:description": (
                    "Contacted by suspicious bank employees during Victim "
                    "A's attempted $400,000 withdrawal on 2022-04-04; "
                    "instructed the bank to halt the transaction and "
                    "contacted the Tangipahoa Parish Sheriff's Office with "
                    "his mother. " + src_ref("factual_basis", "pp. 2-3")
                ),
            },
            {
                "@id": det_damato,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Detective Michael D'Amato (TPSO)",
                "uco-core:description": (
                    "Tangipahoa Parish Sheriff's Office detective who "
                    "interviewed Victim A, monitored the live spoofed "
                    "'US Treasury' call, prepared the decoy box, and ran "
                    "the 2022-04-04 controlled-delivery operation that "
                    "captured Keel. " + src_ref("factual_basis", "pp. 3-4")
                ),
            },
            {
                "@id": sa_candebat,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Special Agent Dominick Candebat (HSI)",
                "uco-core:description": (
                    "Homeland Security Investigations complainant agent on "
                    "the criminal cover sheet for the superseding "
                    "indictment. "
                    + src_ref("superseding_indictment", "AO 257 cover sheet")
                ),
            },
            {
                "@id": fraud_network,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Transnational elder-fraud call-center network",
                "uco-core:description": (
                    "Government-impersonation fraud network headquartered "
                    "in India (per contact data on Keel's phone), operating "
                    "phone callers who posed as U.S. Treasury and DOJ "
                    "agents, dispatchers ('King K'), and U.S.-based money "
                    "couriers including Keel and Panchal. Responsible for "
                    "$4,498,327 in actual and attempted losses to 31 U.S. "
                    "victims since 2021-10-22. "
                    + src_ref("factual_basis", "p. 8")
                ),
            },
            {
                "@id": tpso,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Tangipahoa Parish Sheriff's Office",
                "uco-core:description": (
                    "Received Victim A's fraud complaint on 2022-04-04 and "
                    "ran the same-day controlled-delivery sting that "
                    "captured Keel."
                ),
            },
            {
                "@id": jpso,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Jefferson Parish Sheriff's Office",
                "uco-core:description": (
                    "Obtained and executed the search warrant for Keel's "
                    "room at the La Quinta Inn, Metairie, LA."
                ),
            },
            {
                "@id": hsi,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Homeland Security Investigations",
                "uco-core:description": (
                    "Federal investigating agency; searched Keel's phone "
                    "under warrant, obtained cell-tower data warrants, and "
                    "assembled airline, hotel, payment-card, and bank "
                    "records to attribute the conspiracy."
                ),
            },
            {
                "@id": usao,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Attorney's Office, Eastern District of Louisiana",
                "uco-core:description": (
                    "Prosecuting office (U.S. Attorney Duane A. Evans; "
                    "AUSA Matthew R. Payne)."
                ),
            },
            {
                "@id": green_dot,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Green Dot Bank",
                "uco-core:description": (
                    "Utah-based bank whose Green Dot prepaid card service "
                    "was used to move victim funds; card purchases in "
                    "Louisiana caused interstate wire transactions from the "
                    "Eastern District of Louisiana to Utah — the "
                    "jurisdictional wires for Count 1s. "
                    + src_ref("factual_basis", "p. 2")
                ),
            },
        ]
    )
    graph.append(rel(keel, fraud_network, "Member_Of"))
    graph.append(rel(panchal, fraud_network, "Member_Of"))
    graph.append(rel(king_k, fraud_network, "Member_Of"))
    graph.append(rel(keel, investigation, "Subject_Of"))
    graph.append(rel(panchal, investigation, "Subject_Of"))

    # ------------------------------------------------------------------
    # Defense counsel and representation history (from the docket)
    # ------------------------------------------------------------------
    counsel = [
        (
            "attorney-jusselin",
            "Valerie Welz Jusselin (Federal Public Defender, New Orleans)",
            keel,
            "Lead appointed counsel for Keel from 2022-06-03 through plea "
            "and sentencing. " + src_ref("docket", "defendant 1 counsel; D.E. 14"),
        ),
        (
            "attorney-kelly-keel",
            "Claude J. Kelly (Federal Public Defender's Office)",
            keel,
            "Initially appointed for Keel 2022-06-01 (D.E. 7); terminated "
            "2022-06-03. Later appointed lead counsel for Panchal "
            "2022-11-07 (D.E. 46). " + src_ref("docket", "counsel listings"),
        ),
        (
            "attorney-cimino",
            "Cynthia Marie Cimino (BrowneLaw LLC)",
            panchal,
            "CJA counsel appointed for Panchal 2022-11-07 (D.E. 44); lead "
            "attorney through the 2023-09-05 dismissal. "
            + src_ref("docket", "defendant 2 counsel; D.E. 44"),
        ),
    ]
    for label, name, client, desc in counsel:
        aid = uid(label)
        graph.append(
            {
                "@id": aid,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": name,
                "uco-core:description": desc,
            }
        )
        graph.append(rel(aid, client, "Counsel_For"))
    graph.append(rel(uid("attorney-kelly-keel"), panchal, "Counsel_For"))

    # ------------------------------------------------------------------
    # Cyber observables: the seized phone, phone accounts, spoofed calls,
    # co-conspirator messages, payment card, cell-site records, and the
    # victim's compromised computer. These are genuinely cyber-domain
    # artifacts, so UCO observables are the right modeling choice.
    # ------------------------------------------------------------------
    keel_phone = uid("observable-keel-phone")
    keel_phone_account = uid("observable-keel-phone-account")
    panchal_phone_account = uid("observable-panchal-phone-account")
    victim_a_phone = uid("observable-victim-a-phone")
    card_5885 = uid("observable-card-5885")
    greendot_cards = uid("observable-greendot-cards")
    kingk_thread = uid("observable-kingk-messages")
    package_photo_msg = uid("observable-package-photo-message")
    treasury_call = uid("observable-treasury-spoof-call")
    cell_site_records = uid("observable-cell-site-records")
    victim_b_computer = uid("observable-victim-b-computer")

    graph.extend(
        [
            {
                "@id": keel_phone,
                "@type": ["uco-observable:MobileDevice", "uco-core:UcoObject"],
                "uco-core:name": "Keel's cellular phone (seized 2022-04-04)",
                "uco-core:description": (
                    "Cell phone seized from Keel incident to arrest. Det. "
                    "D'Amato placed it in airplane mode to prevent remote "
                    "destruction of evidence. A later HSI warrant search "
                    "recovered co-conspirator messages ('King K' thread), "
                    "photographs of victim cash packages, and contact "
                    "information for an individual in India. "
                    + src_ref("factual_basis", "pp. 4, 6, 8")
                ),
            },
            {
                "@id": keel_phone_account,
                "@type": ["uco-observable:PhoneAccount", "uco-core:UcoObject"],
                "uco-core:name": "Keel's phone account 813-370-5425",
                "uco-core:description": (
                    "Phone number obtained through the warrant search of "
                    "Keel's seized phone; also Keel's contact number on "
                    "flight records. " + src_ref("factual_basis", "p. 5")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-keel-phone-number"),
                        "@type": "uco-observable:PhoneAccountFacet",
                        "uco-observable:phoneNumber": "813-370-5425",
                    }
                ],
            },
            {
                "@id": panchal_phone_account,
                "@type": ["uco-observable:PhoneAccount", "uco-core:UcoObject"],
                "uco-core:name": "Panchal's phone account 631-575-1198",
                "uco-core:description": (
                    "Panchal's contact number on United and Delta airline "
                    "records and on his Citibank account for the card "
                    "ending 5885. " + src_ref("factual_basis", "p. 5")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-panchal-phone-number"),
                        "@type": "uco-observable:PhoneAccountFacet",
                        "uco-observable:phoneNumber": "631-575-1198",
                    }
                ],
            },
            {
                "@id": victim_a_phone,
                "@type": ["uco-observable:PhoneAccount", "uco-core:UcoObject"],
                "uco-core:name": "Victim A's cell phone account",
                "uco-core:description": (
                    "Victim A's cell phone, on which Det. D'Amato observed "
                    "the incoming spoofed 'US Treasury' call on 2022-04-04. "
                    + src_ref("factual_basis", "p. 3")
                ),
            },
            {
                "@id": card_5885,
                "@type": ["uco-observable:PaymentCard", "uco-core:UcoObject"],
                "uco-core:name": "Citibank Master Card ending 5885 (Panchal)",
                "uco-core:description": (
                    "Panchal's credit card: used to reserve Keel's La "
                    "Quinta Inn room (two guests, 2022-04-03 to "
                    "2022-04-05), to purchase Keel's Delta ticket to New "
                    "Orleans, to purchase Panchal's own ticket, and on "
                    "Panchal's past flight bookings — the linchpin linking "
                    "Panchal to the courier trips. "
                    + src_ref("factual_basis", "pp. 4-5")
                ),
            },
            {
                "@id": greendot_cards,
                "@type": ["uco-observable:PaymentCard", "uco-core:UcoObject"],
                "uco-core:name": "Green Dot prepaid cards purchased by Victim A",
                "uco-core:description": (
                    "Prepaid cards Victim A was directed to purchase from "
                    "2022-03-07 ($60,000 total, receipt-verified). Green "
                    "Dot Bank's servers are in Utah, so each Louisiana "
                    "purchase caused an interstate wire from the Eastern "
                    "District of Louisiana to Utah. "
                    + src_ref("factual_basis", "p. 2")
                ),
            },
            {
                "@id": kingk_thread,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Text thread between Keel and 'King K' (2021-10-22/23)",
                "uco-core:description": (
                    "Keel: 'two calling each day ready to work'; asked for "
                    "work or 'I'mma loose them because they was ready for "
                    "me and I give them my word that it'll be some work'. "
                    "King K: 'work resumes next week', 'hopefully we will "
                    "have some work in coming week for all of us', 'then "
                    "again 1 runner changed his mind and stopped working "
                    "since 9th September, so we had to stop work...now "
                    "having some small things...but expecting more to come "
                    "next week'. Shows Keel's knowing membership in a "
                    "larger conspiracy. " + src_ref("factual_basis", "p. 8")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-kingk-message"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": keel_phone_account},
                        "uco-observable:messageText": (
                            "two calling each day ready to work"
                        ),
                        "uco-observable:sentTime": lit(
                            "xsd:dateTime", central_midnight("2021-10-22")
                        ),
                    }
                ],
            },
            {
                "@id": package_photo_msg,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Keel's photo messages of victim cash packages",
                "uco-core:description": (
                    "Photographs texted by Keel to co-conspirators to "
                    "confirm receipt of victim money, including a photo of "
                    "a box labeled with Victim B's name and Washington "
                    "State address. Cell-site data showed Keel texted such "
                    "photos from Texas and Oklahoma while Panchal's phone "
                    "was in New York, showing Keel worked with multiple "
                    "co-conspirators. " + src_ref("factual_basis", "pp. 6, 8")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-package-photo-message"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": keel_phone_account},
                        "uco-observable:messageType": "MMS photo message",
                    }
                ],
            },
            {
                "@id": treasury_call,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Spoofed 'US Treasury' call to Victim A (2022-04-04)",
                "uco-core:description": (
                    "Incoming call observed live by Det. D'Amato on Victim "
                    "A's phone: Washington, DC area code, caller ID tag "
                    "'US Treasury', male voice with an apparent Indian "
                    "accent instructing Victim A to proceed to the Hammond "
                    "Square Mall drop point. After Keel's arrest the same "
                    "number called again offering Victim A $1,000,000 to "
                    "drop the charges and release 'their guy'. "
                    + src_ref("factual_basis", "pp. 3-4")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-treasury-call"),
                        "@type": "uco-observable:CallFacet",
                        "uco-observable:callType": "incoming (caller ID spoofed as 'US Treasury')",
                        "uco-observable:to": {"@id": victim_a_phone},
                        "uco-observable:startTime": lit(
                            "xsd:dateTime", central_midnight("2022-04-04")
                        ),
                    }
                ],
            },
            {
                "@id": cell_site_records,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Cell-site records for Keel's and Panchal's phones",
                "uco-core:description": (
                    "Cell-tower data obtained by HSI search warrant: both "
                    "phones pinged towers in Seattle on 2022-04-02 and in "
                    "the New Orleans area on 2022-04-03; both were in the "
                    "vicinity of South Center, WA when Victim B handed "
                    "over cash on 2022-03-11, and near Victim C's Bossier "
                    "Parish residence on 2022-03-23. "
                    + src_ref("factual_basis", "pp. 5, 7-8")
                ),
            },
            {
                "@id": victim_b_computer,
                "@type": ["uco-observable:Computer", "uco-core:UcoObject"],
                "uco-core:name": "Victim B's home computer",
                "uco-core:description": (
                    "Reported a pop-up virus on 2022-02-09 directing Victim "
                    "B to call a phone number purporting to be 'Microsoft' "
                    "— the tech-support-scam entry point that handed her "
                    "off to co-conspirators posing as DOJ agents. "
                    + src_ref("superseding_indictment", "Count 1 para. D.3")
                    + "; " + src_ref("factual_basis", "p. 6")
                ),
            },
        ]
    )
    graph.append(rel(keel_phone_account, keel_phone, "Account_On"))
    graph.append(rel(keel_phone, keel, "Possessed_By"))
    graph.append(rel(panchal_phone_account, panchal, "Used_By"))
    graph.append(rel(card_5885, panchal, "Used_By"))
    graph.append(rel(victim_a_phone, victim_a, "Used_By"))
    graph.append(rel(victim_b_computer, victim_b, "Used_By"))
    graph.append(rel(kingk_thread, keel_phone, "Extracted_From"))
    graph.append(rel(package_photo_msg, keel_phone, "Extracted_From"))
    graph.append(rel(greendot_cards, green_dot, "Serviced_By"))

    # ------------------------------------------------------------------
    # Non-cyber physical items: cash boxes, the decoy box, the rental car.
    # These never live in cyberspace, so they are uco-core:UcoObject
    # dual-typed with gufo:FunctionalComplex (CDO gUFO alignment profile),
    # not uco-observable objects.
    # ------------------------------------------------------------------
    physical_item_type = ["uco-core:UcoObject", "gufo:FunctionalComplex"]
    box_victim_a = uid("item-cash-box-victim-a")
    box_victim_b = uid("item-cash-box-victim-b")
    decoy_box = uid("item-decoy-box")
    rental_car = uid("item-rental-car")
    graph.extend(
        [
            {
                "@id": box_victim_a,
                "@type": physical_item_type,
                "uco-core:name": "Sealed box of $60,000 cash handed to Keel by Victim A (2022-04-03)",
                "uco-core:description": (
                    "Cash box Victim A was instructed to prepare and hand "
                    "off in the Santa Fe Cattle Company parking lot at "
                    "Hammond Square Mall; Keel verified himself with a "
                    "code word supplied by the caller. "
                    + src_ref("factual_basis", "p. 2")
                ),
            },
            {
                "@id": box_victim_b,
                "@type": physical_item_type,
                "uco-core:name": "Box of $100,000 cash handed to Keel by Victim B (2022-03-11)",
                "uco-core:description": (
                    "Cash box handed to Keel at a Barnes and Noble in South "
                    "Center, WA after a password exchange; Keel texted a "
                    "photo of the box to co-conspirators to confirm "
                    "receipt. " + src_ref("factual_basis", "pp. 6-7")
                ),
            },
            {
                "@id": decoy_box,
                "@type": physical_item_type,
                "uco-core:name": "Decoy box of note cards prepared by Det. D'Amato (2022-04-04)",
                "uco-core:description": (
                    "Box prepared and sealed in the manner the spoofed "
                    "caller instructed but filled with note cards instead "
                    "of money; the bait in the controlled-delivery sting. "
                    + src_ref("factual_basis", "p. 3")
                ),
            },
            {
                "@id": rental_car,
                "@type": physical_item_type,
                "uco-core:name": "Rental car rented by Panchal (Victim C attempt, 2022-03-23)",
                "uco-core:description": (
                    "Vehicle observed approaching Victim C's Bossier Parish "
                    "residence for the aborted $36,000 pickup; an officer "
                    "recorded the plate, traced it to a rental company, and "
                    "the company identified Panchal as the renter. "
                    + src_ref("factual_basis", "pp. 7-8")
                ),
            },
        ]
    )
    graph.append(rel(rental_car, panchal, "Rented_By"))

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------
    loc_hammond = uid("location-hammond-square-mall")
    loc_southcenter = uid("location-southcenter-wa")
    loc_laquinta = uid("location-la-quinta-metairie")
    graph.extend(
        [
            {
                "@id": loc_hammond,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Hammond Square Mall, 2000 Southwest Railroad Avenue, Hammond, LA",
                "uco-core:description": (
                    "Drop site for both Victim A handoffs: the Santa Fe "
                    "Cattle Company restaurant parking lot (2022-04-03) and "
                    "the controlled-delivery sting near Best Buy "
                    "(2022-04-04). Tangipahoa Parish, Eastern District of "
                    "Louisiana. " + src_ref("factual_basis", "pp. 2-3")
                ),
            },
            {
                "@id": loc_southcenter,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "South Center / Tukwila, Washington",
                "uco-core:description": (
                    "Victim B handoff sites: the Target parking lot at 300 "
                    "Andover Park W, Tukwila, WA (2022-02-24, $60,000) and "
                    "a Barnes and Noble bookstore in South Center, WA "
                    "(2022-03-11, $100,000). "
                    + src_ref("factual_basis", "pp. 6-7")
                ),
            },
            {
                "@id": loc_laquinta,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "La Quinta Inn, 5900 Veterans Blvd., Metairie, LA",
                "uco-core:description": (
                    "Keel's hotel (reserved on Panchal's card ending 5885 "
                    "for two guests, 2022-04-03 to 2022-04-05); searched "
                    "under a JPSO warrant, recovering flight tickets "
                    "showing the Tampa-Seattle-New Orleans courier route. "
                    + src_ref("factual_basis", "pp. 4-5")
                ),
            },
        ]
    )

    # ------------------------------------------------------------------
    # Scheme timeline: overt acts and courier trips (uco-action:Action)
    # ------------------------------------------------------------------
    overt_acts = [
        {
            "label": "act-kingk-recruitment",
            "name": "Keel solicits courier 'work' from dispatcher 'King K' (2021-10-22)",
            "performer": keel,
            "start": "2021-10-22",
            "objects": [kingk_thread],
            "desc": (
                "Text exchange establishing Keel's ongoing courier role "
                "and knowledge of a larger conspiracy with other "
                "'runners'. " + src_ref("factual_basis", "p. 8")
            ),
        },
        {
            "label": "act-victimb-techsupport-scam",
            "name": "Tech-support pop-up scam initiates the fraud against Victim B (2022-02-09)",
            "performer": fraud_network,
            "start": "2022-02-09",
            "objects": [victim_b_computer],
            "desc": (
                "Victim B's computer reported a pop-up virus directing her "
                "to call a purported 'Microsoft' number; the co-conspirator "
                "answering warned her bank accounts were involved in "
                "suspicious activity, then handed her to callers posing as "
                "DOJ agents. " + src_ref("factual_basis", "p. 6")
            ),
        },
        {
            "label": "act-victimb-mails-cash",
            "name": "Victim B mails ~$140,000 cash via UPS at co-conspirators' direction (from 2022-02-10)",
            "performer": victim_b,
            "start": "2022-02-10",
            "desc": (
                "Directed by callers posing as DOJ agents to transfer her "
                "money 'for safekeeping'; Victim B kept receipts and a "
                "journal of all transactions. In total she withdrew "
                "$300,000 between 2022-02-10 and 2022-03-11. "
                + src_ref("factual_basis", "pp. 6-7")
            ),
        },
        {
            "label": "act-victimb-handoff-60k",
            "name": "Victim B hands $60,000 to an unknown female courier, Tukwila, WA (2022-02-24)",
            "performer": victim_b,
            "start": "2022-02-24",
            "desc": (
                "Handoff in the Target parking lot at 300 Andover Park W, "
                "Tukwila, WA; the courier verified herself with a password "
                "while Victim B was kept on the phone with another woman. "
                + src_ref("factual_basis", "pp. 6-7")
            ),
        },
        {
            "label": "act-victima-greendot",
            "name": "Victim A transfers $60,000 via Green Dot cards (from 2022-03-07)",
            "performer": victim_a,
            "start": "2022-03-07",
            "objects": [greendot_cards],
            "desc": (
                "Purchases at callers' direction in Hammond and elsewhere; "
                "each purchase caused an interstate wire from the Eastern "
                "District of Louisiana to Green Dot Bank in Utah — the "
                "charged wires for Count 1s. "
                + src_ref("superseding_indictment", "Count 1 para. D.6")
                + "; " + src_ref("factual_basis", "p. 2")
            ),
        },
        {
            "label": "act-flight-seattle-march",
            "name": "Keel and Panchal fly to Washington State for the Victim B pickup (2022-03-10)",
            "performer": keel,
            "also": [panchal],
            "start": "2022-03-10",
            "desc": (
                "Flight and cell-site records confirmed both men flew to "
                "Seattle on 2022-03-10 and were in the vicinity of South "
                "Center, WA for the 2022-03-11 handoff. "
                + src_ref("superseding_indictment", "Count 1 para. D.4")
                + "; " + src_ref("factual_basis", "p. 7")
            ),
        },
        {
            "label": "act-victimb-handoff-100k",
            "name": "Keel collects a $100,000 cash box from Victim B, South Center, WA (2022-03-11)",
            "performer": keel,
            "also": [panchal],
            "start": "2022-03-11",
            "objects": [box_victim_b],
            "results": [package_photo_msg],
            "desc": (
                "Keel met Victim B at a Barnes and Noble, gave the "
                "verification password, took the package, and texted a "
                "photo of it to co-conspirators to confirm receipt. "
                + src_ref("factual_basis", "pp. 6-7")
            ),
        },
        {
            "label": "act-victimc-aborted-pickup",
            "name": "Aborted $36,000 pickup at Victim C's residence, Bossier Parish, LA (2022-03-23)",
            "performer": panchal,
            "also": [keel],
            "start": "2022-03-23",
            "objects": [rental_car],
            "desc": (
                "Local police waited at Victim C's home; the rental car "
                "rented by Panchal approached, turned around, and left. "
                "Cell-site data placed both defendants' phones in the "
                "vicinity. " + src_ref("factual_basis", "pp. 7-8")
            ),
        },
        {
            "label": "act-flight-new-orleans",
            "name": "Keel and Panchal fly Seattle to New Orleans for the Victim A pickup (2022-04-02)",
            "performer": panchal,
            "also": [keel],
            "start": "2022-04-02",
            "objects": [card_5885],
            "desc": (
                "Both departed Seattle 2022-04-02 and arrived New Orleans "
                "2022-04-03 on different airlines. Panchal booked both "
                "itineraries: the card ending 5885 bought Keel's Delta "
                "ticket and the La Quinta room, and the same contact email "
                "address appears on Keel's Delta booking and Panchal's "
                "United/Alaska bookings. "
                + src_ref("superseding_indictment", "Count 1 para. D.8")
                + "; " + src_ref("factual_basis", "pp. 4-5")
            ),
        },
        {
            "label": "act-victima-handoff-60k",
            "name": "Keel collects a $60,000 cash box from Victim A, Hammond, LA (2022-04-03)",
            "performer": keel,
            "also": [panchal],
            "start": "2022-04-03",
            "objects": [box_victim_a],
            "desc": (
                "Victim A was sent to the Santa Fe Cattle Company parking "
                "lot at Hammond Square Mall with a sealed cash box; Keel "
                "(driven to the pickup by Panchal) gave the code word and "
                "took the box. "
                + src_ref("superseding_indictment", "Count 1 para. D.9")
                + "; " + src_ref("factual_basis", "pp. 2, 4")
            ),
        },
        {
            "label": "act-treasury-call-final",
            "name": "Spoofed 'US Treasury' call directs Victim A to a second handoff (2022-04-04)",
            "performer": fraud_network,
            "start": "2022-04-04",
            "objects": [treasury_call],
            "desc": (
                "Callers told Victim A to withdraw all her money because "
                "it might be seized; she attempted a $400,000 withdrawal "
                "that bank employees and her adult son halted, then "
                "reported the fraud to TPSO. Det. D'Amato monitored the "
                "follow-up call live. "
                + src_ref("superseding_indictment", "Count 1 paras. D.10-D.11")
                + "; " + src_ref("factual_basis", "pp. 2-3")
            ),
        },
        {
            "label": "act-bribe-offer",
            "name": "Post-arrest $1,000,000 offer to Victim A to drop the charges (2022-04-04)",
            "performer": fraud_network,
            "start": "2022-04-04",
            "desc": (
                "After Keel's arrest, the same spoofed number called "
                "Victim A offering $1,000,000 by wire transfer if she "
                "would drop the charges and release 'their guy'. "
                + src_ref("factual_basis", "p. 4")
            ),
        },
    ]
    conspiracy_charge = uid("charge-count1s")
    for act in overt_acts:
        node: dict = {
            "@id": uid(act["label"]),
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": act["name"],
            "uco-core:description": act["desc"],
            "uco-action:performer": {"@id": act["performer"]},
        }
        if "start" in act:
            node["uco-action:startTime"] = lit("xsd:dateTime", central_midnight(act["start"]))
        if act.get("objects"):
            node["uco-action:object"] = [{"@id": o} for o in act["objects"]]
        if act.get("results"):
            node["uco-action:result"] = [{"@id": r} for r in act["results"]]
        graph.append(node)
        graph.append(rel(uid(act["label"]), conspiracy_charge, "Overt_Act_In_Furtherance_Of"))
        for other in act.get("also", []):
            graph.append(rel(other, uid(act["label"]), "Participated_In"))

    # Location and victim edges for the scheme timeline.
    graph.append(rel(uid("act-victima-handoff-60k"), loc_hammond, "Occurred_At"))
    graph.append(rel(uid("act-victimb-handoff-100k"), loc_southcenter, "Occurred_At"))
    graph.append(rel(uid("act-victimb-handoff-60k"), loc_southcenter, "Occurred_At"))
    for victim, acts in [
        (victim_a, ["act-victima-greendot", "act-victima-handoff-60k",
                    "act-treasury-call-final", "act-bribe-offer"]),
        (victim_b, ["act-victimb-techsupport-scam", "act-victimb-mails-cash",
                    "act-victimb-handoff-60k", "act-victimb-handoff-100k"]),
        (victim_c, ["act-victimc-aborted-pickup"]),
    ]:
        for act_label in acts:
            graph.append(rel(victim, uid(act_label), "Victim_Of"))

    # The false-personation count rests on the Treasury impersonation
    # during the Victim A pickups.
    graph.append(rel(uid("act-victima-handoff-60k"), uid("charge-count2s"), "Basis_Of"))
    graph.append(rel(uid("act-treasury-call-final"), uid("charge-count2s"), "Basis_Of"))

    # ------------------------------------------------------------------
    # Investigative actions: the sting, arrest, and warrant chain
    # ------------------------------------------------------------------
    warrant_hotel = uid("authorization-hotel-warrant")
    warrant_phone = uid("authorization-phone-warrant")
    warrant_celltower = uid("authorization-celltower-warrant")
    graph.extend(
        [
            {
                "@id": warrant_hotel,
                "@type": "case-investigation:Authorization",
                "uco-core:name": "JPSO search warrant for Keel's La Quinta Inn room",
                "uco-core:description": (
                    "Search warrant obtained by Jefferson Parish Sheriff's "
                    "Office deputies for Keel's room at the La Quinta Inn, "
                    "5900 Veterans Blvd., Metairie, LA. "
                    + src_ref("factual_basis", "p. 4")
                ),
            },
            {
                "@id": warrant_phone,
                "@type": "case-investigation:Authorization",
                "uco-core:name": "Search warrant for Keel's seized cell phone",
                "uco-core:description": (
                    "Federal warrant under which agents searched Keel's "
                    "phone, recovering the 'King K' thread, package photos, "
                    "and the India contact. "
                    + src_ref("factual_basis", "pp. 5-6")
                ),
            },
            {
                "@id": warrant_celltower,
                "@type": "case-investigation:Authorization",
                "uco-core:name": "Search warrant for cell-tower data (Keel and Panchal phones)",
                "uco-core:description": (
                    "Warrant for historical cell-site data placing both "
                    "phones in Seattle (2022-04-02), New Orleans "
                    "(2022-04-03), South Center WA (2022-03-11), and near "
                    "Victim C's residence (2022-03-23). "
                    + src_ref("factual_basis", "p. 5")
                ),
            },
        ]
    )

    investigative_actions = [
        {
            "label": "ia-tpso-interview",
            "name": "TPSO complaint intake and interview of Victim A (2022-04-04)",
            "performer": tpso,
            "start": "2022-04-04",
            "objects": [victim_a_phone],
            "desc": (
                "TPSO received the formal fraud complaint; Det. D'Amato "
                "interviewed Victim A and observed the live incoming "
                "spoofed 'US Treasury' call with a Washington, DC area "
                "code. " + src_ref("factual_basis", "pp. 1, 3")
            ),
        },
        {
            "label": "ia-controlled-delivery",
            "name": "TPSO controlled-delivery sting at Hammond Square Mall (2022-04-04)",
            "performer": tpso,
            "start": "2022-04-04",
            "objects": [decoy_box],
            "desc": (
                "Det. D'Amato prepared the decoy box and investigators in "
                "unmarked vehicles followed Victim A to the drop point. "
                "Keel was observed on a cell phone near Best Buy, changed "
                "his shirt behind the store, approached Victim A's vehicle "
                "and greeted her by name, extended his arms to receive the "
                "package, and was detained. "
                + src_ref("factual_basis", "pp. 3-4")
            ),
        },
        {
            "label": "ia-arrest-keel",
            "name": "Arrest of Keel and seizure of his phone (2022-04-04)",
            "performer": tpso,
            "start": "2022-04-04",
            "objects": [keel],
            "results": [keel_phone],
            "desc": (
                "Search incident to arrest recovered Keel's Florida "
                "driver's license, his cell phone (placed into airplane "
                "mode to prevent remote wiping), and a receipt for the La "
                "Quinta Inn in Metairie. Victim A identified Keel as the "
                "man from the prior day's handoff. "
                + src_ref("factual_basis", "p. 4")
            ),
        },
        {
            "label": "ia-hotel-search",
            "name": "JPSO warrant search of Keel's La Quinta Inn room",
            "performer": jpso,
            "start": "2022-04-04",
            "authorization": warrant_hotel,
            "desc": (
                "Recovered tickets showing Keel flew Tampa Bay to Seattle "
                "on 2022-03-31 and Seattle to New Orleans arriving "
                "2022-04-03; the room was reserved for two guests on the "
                "card ending 5885. " + src_ref("factual_basis", "pp. 4-5")
            ),
        },
        {
            "label": "ia-phone-search",
            "name": "HSI warrant search of Keel's cell phone",
            "performer": hsi,
            "objects": [keel_phone],
            "results": [kingk_thread, package_photo_msg],
            "authorization": warrant_phone,
            "desc": (
                "Recovered co-conspirator messages, photographs of victim "
                "cash packages (including Victim B's labeled box, which "
                "led agents to identify her), Keel's number 813-370-5425, "
                "and contact information for an individual in India. "
                + src_ref("factual_basis", "pp. 5-6, 8")
            ),
        },
        {
            "label": "ia-celltower-warrants",
            "name": "HSI cell-tower data warrants for both defendants' phones",
            "performer": hsi,
            "objects": [keel_phone_account, panchal_phone_account],
            "results": [cell_site_records],
            "authorization": warrant_celltower,
            "desc": (
                "Cell-site data corroborated the courier trips and placed "
                "both phones at each pickup. "
                + src_ref("factual_basis", "pp. 5, 7-8")
            ),
        },
        {
            "label": "ia-records-attribution",
            "name": "HSI records attribution: airline, hotel, payment-card, and bank records",
            "performer": hsi,
            "objects": [card_5885],
            "desc": (
                "Delta/United/Alaska records, La Quinta records, Citibank "
                "records for the card ending 5885, and Victim B's bank "
                "records ($300,000 withdrawn 2022-02-10 to 2022-03-11) "
                "tied Panchal to the bookings and quantified the losses. "
                + src_ref("factual_basis", "pp. 4-5, 7")
            ),
        },
    ]
    for ia in investigative_actions:
        node = {
            "@id": uid(ia["label"]),
            "@type": "case-investigation:InvestigativeAction",
            "uco-core:name": ia["name"],
            "uco-core:description": ia["desc"],
            "uco-action:performer": {"@id": ia["performer"]},
        }
        if "start" in ia:
            node["uco-action:startTime"] = lit("xsd:dateTime", central_midnight(ia["start"]))
        if ia.get("objects"):
            node["uco-action:object"] = [{"@id": o} for o in ia["objects"]]
        if ia.get("results"):
            node["uco-action:result"] = [{"@id": r} for r in ia["results"]]
        if ia.get("authorization"):
            node["case-investigation:relevantAuthorization"] = [{"@id": ia["authorization"]}]
        graph.append(node)
        graph.append(rel(uid(ia["label"]), investigation, "part_of"))
    graph.append(rel(uid("ia-controlled-delivery"), loc_hammond, "Occurred_At"))
    graph.append(rel(uid("ia-hotel-search"), loc_laquinta, "Occurred_At"))
    graph.append(rel(det_damato, tpso, "Member_Of"))
    graph.append(rel(sa_candebat, hsi, "Member_Of"))
    graph.append(rel(det_damato, uid("ia-controlled-delivery"), "Participated_In"))
    graph.append(rel(det_damato, uid("ia-tpso-interview"), "Participated_In"))

    # ------------------------------------------------------------------
    # Charging instruments (complaint, indictment, superseding indictment)
    # ------------------------------------------------------------------
    instruments = [
        ("instrument-complaint", "complaint", "Criminal complaint (D.E. 1)", "2022-04-29",
         "Charged Keel with impersonation of a federal officer (18 U.S.C. "
         "§§ 912, 2) and conspiracy to commit wire fraud (18 U.S.C. "
         "§§ 1343, 1349); signed by Magistrate Judge Dana Douglas in "
         f"magistrate case {MAGISTRATE_DOCKET}."),
        ("instrument-indictment", "indictment", "Indictment (D.E. 10)", "2022-06-02",
         "Grand jury charged Keel with Counts 1 and 2."),
        ("instrument-superseding", "superseding-indictment", "Superseding Indictment (Doc 28)", "2022-10-13",
         "Operative charging instrument: re-charged Keel (Counts 1s, 2s) "
         "and added Panchal as defendant (2). Filed sealed; unsealed "
         "2022-10-19 (D.E. 34, 35). Complainant agency HSI (SA Dominick "
         "Candebat)."),
    ]
    prev_instrument: str | None = None
    for label, itype, name, filed, desc in instruments:
        node_id = uid(label)
        graph.append(
            {
                "@id": node_id,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": name,
                "uco-core:description": desc + " " + src_ref("docket", f"entry filed {filed}"),
                "legalproc:instrumentType": itype,
                "uco-core:objectCreatedTime": lit("xsd:dateTime", central_midnight(filed)),
            }
        )
        if prev_instrument:
            graph.append(rel(node_id, prev_instrument, "Supersedes"))
        prev_instrument = node_id
    superseding = uid("instrument-superseding")
    graph.append(rel(superseding, doc_ids["superseding_indictment"], "Derived_From"))

    # ------------------------------------------------------------------
    # Charges
    # ------------------------------------------------------------------
    for charge in CHARGES:
        graph.append(
            {
                "@id": uid(charge["label"]),
                "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                "uco-core:name": f"{charge['count_label']}: {charge['name']}",
                "uco-core:description": charge["description"],
                "legalproc:statuteCitation": charge["statute"],
                "legalproc:countLabel": charge["count_label"],
                "legalproc:countNumber": [
                    lit("xsd:nonNegativeInteger", n) for n in charge["counts"]
                ],
                "legalproc:offenseForm": charge["offense_form"],
                "legalproc:chargeClassification": charge["felony_class"],
                "legalproc:chargeDisposition": charge["dispositions"],
                "legalproc:assertedIn": [{"@id": uid(charge["instrument"])}],
            }
        )

    # Defendant-to-charge edges.
    for label in ("charge-count1s", "charge-count2s", "charge-count1-orig", "charge-count2-orig"):
        graph.append(rel(keel, uid(label), "Charged_With"))
    for label in ("charge-count1s", "charge-count2s"):
        graph.append(rel(panchal, uid(label), "Charged_With"))

    # Victim-to-charge edges.
    for victim in (victim_a, victim_b, victim_c):
        graph.append(rel(victim, uid("charge-count1s"), "Victim_Of"))
    graph.append(rel(victim_a, uid("charge-count2s"), "Victim_Of"))

    # ------------------------------------------------------------------
    # Proceedings, plea, sentence
    # ------------------------------------------------------------------
    initial_appearance = uid("proceeding-initial-appearance")
    detention_hearing = uid("proceeding-detention-hearing")
    arraignment_super = uid("proceeding-arraignment-superseding")
    arraignment_panchal = uid("proceeding-arraignment-panchal")
    rearraignment = uid("proceeding-rearraignment-plea")
    sentencing = uid("proceeding-sentencing")
    graph.extend(
        [
            {
                "@id": initial_appearance,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Initial appearance of Keel (2022-06-01)",
                "uco-core:description": (
                    "Before Magistrate Judge Dana Douglas; defendant "
                    "remanded; Federal Public Defender appointed. "
                    + src_ref("docket", "D.E. 6, 7")
                ),
                "legalproc:proceedingType": "initial-appearance",
            },
            {
                "@id": detention_hearing,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Detention hearing and arraignment of Keel (2022-06-08)",
                "uco-core:description": (
                    "Before Magistrate Judge Janis van Meerveld; order of "
                    "detention entered; Keel arraigned on Counts 1 and 2. "
                    + src_ref("docket", "D.E. 17-19")
                ),
                "legalproc:proceedingType": "detention-hearing",
            },
            {
                "@id": arraignment_super,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Arraignment of Keel on superseding Counts 1s and 2s (2022-10-24)",
                "uco-core:description": (
                    "Before Magistrate Judge Karen Wells Roby; defendant "
                    "remanded. " + src_ref("docket", "D.E. 38")
                ),
                "legalproc:proceedingType": "arraignment",
            },
            {
                "@id": arraignment_panchal,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Initial appearance and arraignment of Panchal (2022-11-07 / 2022-11-09)",
                "uco-core:description": (
                    "Panchal released on bond set in the Eastern District "
                    "of New York; arraigned 2022-11-09 before Magistrate "
                    "Judge Janis van Meerveld. "
                    + src_ref("docket", "D.E. 45, 48")
                ),
                "legalproc:proceedingType": "arraignment",
            },
            {
                "@id": rearraignment,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Rearraignment: Keel changes plea to guilty (2023-06-14)",
                "uco-core:description": (
                    "Before Judge Ivan L.R. Lemelle; Keel pleaded guilty "
                    "to Counts 1s and 2s; the Factual Basis (Doc 61) was "
                    "filed the same day. " + src_ref("docket", "D.E. 59, 61")
                ),
                "legalproc:proceedingType": "plea-hearing",
            },
            {
                "@id": sentencing,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Sentencing hearing for Keel (2023-10-25)",
                "uco-core:description": (
                    "Before Judge Ivan L.R. Lemelle. The government had "
                    "moved for a three-level reduction in offense level "
                    "(D.E. 73). " + src_ref("docket", "D.E. 78") + "; "
                    + src_ref("judgment", "p. 1")
                ),
                "legalproc:proceedingType": "sentencing-hearing",
            },
        ]
    )
    for proceeding in (initial_appearance, detention_hearing, arraignment_super,
                       arraignment_panchal, rearraignment, sentencing):
        graph.append(rel(proceeding, investigation, "part_of"))

    plea_keel = uid("plea-keel")
    graph.append(
        {
            "@id": plea_keel,
            "@type": ["legalproc:Plea", "uco-core:UcoObject"],
            "uco-core:name": "Keel guilty plea to Counts 1s and 2s (2023-06-14)",
            "uco-core:description": (
                "Supported by the Factual Basis (Doc 61), in which Keel "
                "stipulated for sentencing purposes that he is responsible "
                "for $4,498,327 in actual or intended loss based on his "
                "own acts and the reasonably foreseeable acts of his "
                "co-conspirators. " + src_ref("factual_basis", "pp. 1, 9")
                + "; " + src_ref("judgment", "p. 1")
            ),
            "legalproc:pleaType": "guilty",
            "legalproc:concernsCharge": [
                {"@id": uid("charge-count1s")},
                {"@id": uid("charge-count2s")},
            ],
        }
    )
    graph.append(rel(plea_keel, keel, "Relates_To"))
    graph.append(rel(plea_keel, rearraignment, "Occurred_During"))
    graph.append(rel(plea_keel, doc_ids["factual_basis"], "Derived_From"))

    sentence_keel = uid("sentence-imposed-keel")
    graph.append(
        {
            "@id": sentence_keel,
            "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
            "uco-core:name": "Sentence imposed on Keel (2023-10-25)",
            "uco-core:description": (
                "125 months on Count 1s and 36 months on Count 2s, "
                "concurrent, for a total of 125 months; supervised release "
                "3 years (Count 1s) and 1 year (Count 2s), concurrent, for "
                "a total of 3 years; special assessment $200 due "
                "immediately; no fine (inability to pay); determination of "
                "restitution deferred until 2023-12-06. BOP "
                "recommendations: placement near Tampa, FL, RDAP "
                "participation, and access to mental-health and drug "
                "treatment. Special conditions include full financial "
                "disclosure, no new debt without permission, substance-"
                "abuse and mental-health treatment, and warrantless "
                "search consent. Judge Ivan L.R. Lemelle, judgment entered "
                "2023-10-26. Keel's later pro se motion to reduce the "
                "sentence under Guidelines Amendment 821 was denied "
                "2025-04-16 (D.E. 90, 92). "
                + src_ref("judgment", "pp. 1-7") + "; "
                + src_ref("docket", "D.E. 80, 92")
            ),
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceTerm": "125 months (125 on Count 1s + 36 concurrent on Count 2s)",
            "legalproc:concernsCharge": [
                {"@id": uid("charge-count1s")},
                {"@id": uid("charge-count2s")},
            ],
        }
    )
    graph.append(rel(sentence_keel, keel, "Relates_To"))
    graph.append(rel(sentence_keel, sentencing, "Occurred_During"))
    graph.append(rel(sentence_keel, doc_ids["judgment"], "Derived_From"))

    # ------------------------------------------------------------------
    # Forfeiture and restitution
    # ------------------------------------------------------------------
    forfeiture = uid("forfeiture-notice")
    graph.append(
        {
            "@id": forfeiture,
            "@type": ["legalproc:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Notice of forfeiture (superseding indictment) and judgment forfeiture provision",
            "uco-core:description": (
                "Forfeiture under 18 U.S.C. § 981(a)(1)(C) and 28 U.S.C. "
                "§ 2461 of any property constituting or derived from "
                "proceeds of Count 1s, with a substitute-assets money "
                "judgment under 21 U.S.C. § 853(p) if proceeds cannot be "
                "located. The judgment orders forfeiture consistent with "
                "the superseding indictment. "
                + src_ref("superseding_indictment", "notice of forfeiture")
                + "; " + src_ref("judgment", "p. 7")
            ),
            "legalproc:concernsCharge": [{"@id": uid("charge-count1s")}],
        }
    )
    graph.append(rel(forfeiture, doc_ids["superseding_indictment"], "Derived_From"))

    restitution = uid("restitution-order")
    graph.append(
        {
            "@id": restitution,
            "@type": ["legalproc:RestitutionOrder", "uco-core:UcoObject"],
            "uco-core:name": "Restitution ordered by amended judgment (2023-12-12)",
            "uco-core:description": (
                "The 2023-10-25 judgment deferred the determination of "
                "restitution until 2023-12-06; the government moved for a "
                "restitution order on 2023-12-01 (D.E. 85), the court "
                "granted the motion, and an amended judgment issued "
                "2023-12-12 (D.E. 86, 88) with a sealed victim-payee "
                "attachment. The restitution amount is not stated in the "
                "public documents modeled here. "
                + src_ref("judgment", "p. 6 (deferral)") + "; "
                + src_ref("docket", "D.E. 85, 86, 88")
            ),
            "legalproc:currencyCode": "USD",
            "legalproc:concernsCharge": [
                {"@id": uid("charge-count1s")},
                {"@id": uid("charge-count2s")},
            ],
        }
    )
    graph.append(rel(restitution, keel, "Relates_To"))
    for victim in (victim_a, victim_b):
        graph.append(rel(restitution, victim, "Relates_To"))

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            # Namespace proposed to CASE in issue #192 (committee decides the
            # final IRI); implemented locally by extensions/legalproc/.
            "legalproc": "https://ontology.caseontology.org/case/criminal/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            # gUFO upper ontology, used via the CDO alignment profile
            # (CDO-Shapes-gufo) to type non-cyber physical evidence.
            "gufo": "http://purl.org/nemo/gufo#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    report = validate_graph_file(path, extensions=["legalproc"], project_root=ROOT)
    print(report.safe_summary)
    paths = load_extension_ontology_paths("legalproc", mode="full", project_root=ROOT)
    print(f"Validated with {len(paths)} legalproc ontology files")
    return 0 if report.conforms else 1


def main() -> int:
    payload = build_graph()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Graph nodes: {len(payload['@graph'])}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
