#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Jack Douglas Teixeira (D. Mass. espionage).

Case 1:23-cr-10159-IT (D. Mass., Boston): federal Espionage Act prosecution
of a Massachusetts Air National Guard Cyber Defense Operations Journeyman
who, from January 2022 through April 2023, removed classified national
defense information ("NDI") from the Sensitive Compartmented Information
Facility (SCIF) at Otis Air National Guard Base and posted it on the social
media platform Discord — first by transcribing classified text from a
classified workstation into Discord messages, then by printing hundreds of
classified documents on a seldom-used SCIF printer, removing them, and
posting photographs of the documents. Six counts of willful retention and
transmission of NDI under 18 U.S.C. § 793(e); Rule 11(c)(1)(C) plea to all
six counts; government recommendation of 200 months.

Sources (PACER, District of Massachusetts):
  - Indictment: Document 48 (filed 2023-06-15) — six § 793(e) counts
  - Plea Agreement: Document 130 (filed 2024-03-04, executed 2024-02-28)
  - Government's Sentencing Memorandum: Document 144 (filed 2024-10-29)

MCP extraction artifacts: examples/pacer/dma_2023_cr_10159/mcp_outputs/

Extensions and namespaces exercised:
  - extensions/legalproc — complaint -> indictment chain, six § 793(e)
    counts, Rule 11(c)(1)(C) plea, forfeiture allegation, recommended
    sentence. Sentencing had not occurred in the modeled record, so the
    Sentence node carries sentenceStatus 'recommended'.
  - uco-marking — this is the first exemplar in this repository to use
    UCO's Marking namespace for U.S. Government classification banners.
    Each charged NDI observable carries uco-core:objectMarking ->
    marking:MarkingDefinition -> marking:StatementMarking preserving the
    classification banner exactly as the charging instrument attests it
    ("TOP SECRET//SCI" for Counts 1, 3-6; "SECRET" for Count 2).

Marking-fidelity rule (raised during modeling review): the string
"TS//NOFORN//FVEY" appears in the record ONLY as text Teixeira typed in a
2022-03-15 Discord message (quoted in the sentencing memorandum). It is an
internally contradictory banner — NOFORN prohibits release to any foreign
national, while REL TO FVEY authorizes release to Five Eyes partners, and
the two dissemination controls are mutually exclusive under ODNI/CAPCO
marking rules. It is therefore preserved verbatim as quoted Message content
(evidence of what the defendant wrote) and is NOT promoted to a
MarkingDefinition. Only banners the charging documents attest as actually
appearing on the charged information/documents become markings.

Cyber vs. non-cyber conventions (docs/recipes/legal-process-modeling.md):
  - Cyber observables: the classified workstation, the SCIF printer (a
    networked IT device), the charged NDI items, Teixeira's Discord
    account and servers, the quoted Discord messages, the photographs
    posted to Discord, and the destroyed iPad and desktop computer.
  - The SCIF itself is a physical facility that never lives in
    cyberspace: uco-core:UcoObject dual-typed with gufo:FunctionalComplex.
    Likewise the paper printouts Teixeira carried out of the SCIF — the
    digital documents they were printed from, and the photographs of them
    posted online, are the cyber observables.
  - Court dates are date-only facts rendered at local midnight Eastern
    time; quoted language is kept verbatim from the filings.
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

CASE_ID = "teixeira-dma-2023-espionage"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "teixeira-dma-2023-espionage.jsonld"

PACER_DOCKET = "1:23-cr-10159-IT"
LOCAL_REF = "outside_pacer -- espionage"

SOURCE_DOCS = {
    "indictment": {
        "file_name": "pacer -- espionage -- indictment.pdf",
        "sha256": "5aadb9b9f7cd13aa433e308ed956fb586560861fab66eb3efe5409c30f824acf",
        "pacer_doc": "48",
        "filed": "2023-06-15",
    },
    "plea_agreement": {
        "file_name": "pacer -- espionage -- Plea Agreement.pdf",
        "sha256": "273c6d94e9e313675b614a6717726591fe544090c049a793e073ec184c75b7ee",
        "pacer_doc": "130",
        "filed": "2024-03-04",
    },
    "sentencing_memorandum": {
        "file_name": "pacer -- espionage -- Sentencing Memorandum.pdf",
        "sha256": "d971d9b2542b3a0323bcb5e569dad874a5be1dfb16689584672abece92850e0a",
        "pacer_doc": "144",
        "filed": "2024-10-29",
    },
}

# ---------------------------------------------------------------------------
# The six charged NDI items (Indictment paras. 16, 18). Counts One and Two
# charge classified *information* transcribed into Discord messages; Counts
# Three through Six charge classified Government *Documents* photographed
# and posted. Classification banners are kept exactly as charged.
# ---------------------------------------------------------------------------
CHARGED_NDI = [
    {
        "count": 1,
        "banner": "TOP SECRET//SCI",
        "kind": "information",
        "dates": "Nov. 2022 to April 2023",
        "desc": (
            "Information regarding the compromise by a foreign adversary "
            "of certain accounts belonging to a U.S. company."
        ),
    },
    {
        "count": 2,
        "banner": "SECRET",
        "kind": "information",
        "dates": "Jan. 2023 to April 2023",
        "desc": (
            "Information regarding the provision of equipment to Ukraine, "
            "how the equipment would be transferred, and how the equipment "
            "would be used upon receipt."
        ),
    },
    {
        "count": 3,
        "banner": "TOP SECRET//SCI",
        "kind": "document",
        "dates": "Feb. 2023 to April 2023",
        "desc": (
            "A Government Document that describes the status of the "
            "Russia-Ukraine conflict to include troop movements on a "
            "particular date, which Government Document is based on "
            "sensitive U.S. intelligence, gathered through classified "
            "sources and methods and reveals United States national "
            "defense information."
        ),
    },
    {
        "count": 4,
        "banner": "TOP SECRET//SCI",
        "kind": "document",
        "dates": "March 2023 to April 2023",
        "desc": (
            "A Government Document discussing a plot by a foreign "
            "adversary to target United States forces abroad and which "
            "discusses, in part, where and how the attack on United "
            "States forces would occur."
        ),
    },
    {
        "count": 5,
        "banner": "TOP SECRET//SCI",
        "kind": "document",
        "dates": "March 2023 to April 2023",
        "desc": (
            "A Government Document that describes Western deliveries of "
            "supplies to the Ukrainian battlefield, including foreign "
            "perceptions of the deliveries."
        ),
    },
    {
        "count": 6,
        "banner": "TOP SECRET//SCI",
        "kind": "document",
        "dates": "Jan. 2023 to April 2023",
        "desc": (
            "A Government Document that describes a shift in foreign and "
            "economic policy of a particular foreign government and "
            "actions that country took in an effort to repair its "
            "relationship with the United States, to the perceived "
            "detriment of a separate foreign country."
        ),
    },
]

COUNT_WORDS = ["One", "Two", "Three", "Four", "Five", "Six"]


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


def eastern_midnight(date_str: str) -> str:
    """Date-only court fact rendered at local midnight Eastern time.

    D. Mass.: EDT (-04:00) roughly April-October, EST (-05:00) otherwise.
    Month-level approximation is sufficient for filing dates.
    """
    month = int(date_str.split("-")[1])
    offset = "-04:00" if 4 <= month <= 10 else "-05:00"
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
            f"{PACER_DOCKET} (D. Mass.); local bundle '{LOCAL_REF}'."
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


def marking_definition(label: str, banner: str, source_note: str) -> list[dict]:
    """A USG classification banner as a MarkingDefinition + StatementMarking.

    UCO 1.4's marking namespace has no dedicated USG-classification
    MarkingModel (see https://github.com/ucoProject/UCO/issues/647), so the
    banner is carried verbatim in a StatementMarking. When a
    USGClassificationMarking model is adopted upstream, these nodes migrate
    by re-typing the model node and structuring the banner's components
    (classification level, SCI control systems, dissemination controls).
    """
    return [
        {
            "@id": uid(f"{label}-def"),
            "@type": ["marking:MarkingDefinition", "uco-core:UcoObject"],
            "uco-core:name": f"USG classification banner: {banner}",
            "uco-core:description": (
                f"U.S. Government classification marking '{banner}' per "
                "Executive Order 13526. " + source_note
            ),
            "marking:definitionType": "statement",
            "marking:definition": [{"@id": uid(f"{label}-model")}],
        },
        {
            "@id": uid(f"{label}-model"),
            "@type": "marking:StatementMarking",
            "marking:definitionType": "statement",
            "marking:statement": banner,
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
            "uco-core:name": f"United States v. Jack Douglas Teixeira, {PACER_DOCKET} (D. Mass.)",
            "legalproc:caseIdentifier": PACER_DOCKET,
            "uco-core:description": (
                "Espionage Act prosecution of Jack Douglas Teixeira, a "
                "Massachusetts Air National Guard Cyber Defense Operations "
                "Journeyman with the 102d Intelligence Wing at Otis Air "
                "National Guard Base who held a TOP SECRET//SCI clearance. "
                "From January 2022 through April 2023 Teixeira removed "
                "classified national defense information from the Otis "
                "SCIF and posted it on the social media platform Discord: "
                "first by transcribing classified text from a classified "
                "workstation into Discord messages, then by printing "
                "hundreds of classified documents on an isolated, "
                "seldom-used SCIF printer, removing them, and posting "
                "photographs of documents bearing SECRET, TOP SECRET, and "
                "SCI markings. Arrested by the FBI on 2023-04-13; charged "
                "by complaint 2023-04-14; indicted on six counts of "
                "willful retention and transmission of national defense "
                "information (18 U.S.C. § 793(e)); pleaded guilty to all "
                "six counts on 2024-03-04 under a Rule 11(c)(1)(C) "
                "agreement binding the sentence to 132-200 months; the "
                "government recommended 200 months. The Secretary of the "
                "Air Force attested the disclosures caused 'exceptionally "
                "grave and long-lasting damage to the national security "
                "of the United States.'"
            ),
        }
    )

    doc_ids: dict[str, str] = {}
    for key, meta in SOURCE_DOCS.items():
        label = f"source-{key}"
        doc_ids[key] = uid(label)
        graph.append(source_observable(label, meta))
        graph.append(rel(uid(label), investigation, "part_of"))

    # ------------------------------------------------------------------
    # People and organizations
    # ------------------------------------------------------------------
    teixeira = uid("person-teixeira")
    kendall = uid("person-kendall")
    agent_church = uid("person-sa-church")
    usang = uid("org-usang-102iw")
    fbi = uid("org-fbi")
    usao = uid("org-usao-dma")
    doj_nsd = uid("org-doj-nsd")
    discord_platform = uid("org-discord")
    usgov = uid("org-us-government")
    air_force = uid("org-dept-air-force")

    graph.extend(
        [
            {
                "@id": teixeira,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Jack Douglas Teixeira",
                "uco-core:description": (
                    "Defendant. Resident of Dighton, Massachusetts; "
                    "enlisted in the U.S. Air National Guard in September "
                    "2019; served with the 102d Intelligence Wing at Otis "
                    "Air National Guard Base as a Cyber Defense Operations "
                    "Journeyman whose primary duty was troubleshooting "
                    "classified workstations. Held a TOP SECRET security "
                    "clearance with Sensitive Compartmented Information "
                    "access since July 2021. "
                    + src_ref("indictment", "paras. 1-2, 7")
                ),
            },
            {
                "@id": kendall,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Frank Kendall III, 26th Secretary of the Air Force",
                "uco-core:description": (
                    "Declarant. Attested in an unclassified declaration "
                    "(Doc 143-1) that Teixeira's disclosures spanned "
                    "multiple Executive Order 13526 categories — 'military "
                    "plans, foreign government information, intelligence "
                    "activities, sources and methods, foreign relations, "
                    "and vulnerabilities and capabilities of systems' — "
                    "and caused damage that was 'immediate and enduring' "
                    "and 'will continue to impact the U.S. national "
                    "security not just for weeks and years, but for "
                    "decades to come.' "
                    + src_ref("sentencing_memorandum", "pp. 5-6")
                ),
            },
            {
                "@id": agent_church,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "FBI Special Agent Luke Church",
                "uco-core:description": (
                    "FBI declarant whose declarations (Docs 34-1, 143-2) "
                    "attribute and quote Teixeira's Discord messages. "
                    + src_ref("sentencing_memorandum", "pp. 7-8")
                ),
            },
            {
                "@id": usang,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Air National Guard, 102d Intelligence Wing",
                "uco-core:description": (
                    "Teixeira's unit at Otis Air National Guard Base, "
                    "Massachusetts. The wing's intelligence mission ran on "
                    "the classified workstations Teixeira was assigned to "
                    "troubleshoot. "
                    + src_ref("sentencing_memorandum", "p. 5 (Offense Conduct)")
                ),
            },
            {
                "@id": air_force,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Department of the Air Force",
                "uco-core:description": (
                    "Department whose Secretary provided the unclassified "
                    "damage declaration supporting sentencing. "
                    + src_ref("sentencing_memorandum", "pp. 5-6")
                ),
            },
            {
                "@id": usgov,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "United States Government",
                "uco-core:description": (
                    "Owner and original classification authority of the "
                    "national security information at issue: 'National "
                    "security information was information owned by, "
                    "produced by, produced for, and under the control of "
                    "the United States government' (E.O. 12958 as amended "
                    "by E.O. 13292 and E.O. 13526). Victim of all six "
                    "counts. " + src_ref("indictment", "para. 3")
                ),
            },
            {
                "@id": fbi,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Federal Bureau of Investigation",
                "uco-core:description": (
                    "Arrested Teixeira on 2023-04-13 and holds the "
                    "property seized from his residence, vehicle, and "
                    "person. " + src_ref("plea_agreement", "para. 7")
                ),
            },
            {
                "@id": usao,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Attorney's Office, District of Massachusetts",
                "uco-core:description": (
                    "Prosecuting office (AUSAs Nadine Pellegrini, Jared C. "
                    "Dolan, Jason A. Casey). "
                    + src_ref("plea_agreement", "signature block")
                ),
            },
            {
                "@id": doj_nsd,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Department of Justice, National Security Division",
                "uco-core:description": (
                    "Co-prosecuting component (Trial Attorney Christina A. "
                    "Clark). " + src_ref("indictment", "signature block")
                ),
            },
            {
                "@id": discord_platform,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Discord (social media platform operator)",
                "uco-core:description": (
                    "Operator of the social media platform on which "
                    "Teixeira transmitted national defense information. "
                    "The indictment refers to it as 'the Social Media "
                    "Platform'; the sentencing memorandum names Discord. "
                    + src_ref("sentencing_memorandum", "p. 4")
                ),
            },
        ]
    )
    graph.append(rel(teixeira, usang, "Member_Of"))
    graph.append(rel(usang, air_force, "part_of"))

    # ------------------------------------------------------------------
    # Locations and non-cyber physical items (gUFO dual-typing)
    # ------------------------------------------------------------------
    otis_base = uid("location-otis-base")
    residence = uid("location-dighton-residence")
    scif = uid("physical-otis-scif")
    printouts = uid("physical-printouts")

    graph.extend(
        [
            {
                "@id": otis_base,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Otis Air National Guard Base, Massachusetts",
                "uco-core:description": (
                    "Base in the District of Massachusetts where Teixeira "
                    "was stationed and from which the charged NDI was "
                    "removed. " + src_ref("indictment", "para. 2")
                ),
            },
            {
                "@id": residence,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira residence, Dighton, Massachusetts",
                "uco-core:description": (
                    "Defendant's residence; site of the 2023-04-13 "
                    "seizures, with the smashed iPad recovered from a "
                    "dumpster outside. "
                    + src_ref("sentencing_memorandum", "p. 8")
                ),
            },
            {
                "@id": scif,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "Sensitive Compartmented Information Facility (SCIF), Otis ANG Base",
                "uco-core:description": (
                    "Accredited physical facility in which SCI was to be "
                    "processed, stored, used, or discussed. A physical "
                    "facility outside the cyber domain, so typed with the "
                    "gUFO upper ontology rather than as a UCO observable; "
                    "the classified workstations and printer inside it "
                    "are cyber observables. "
                    + src_ref("indictment", "para. 4")
                ),
            },
            {
                "@id": printouts,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "Paper printouts of classified documents removed from the SCIF",
                "uco-core:description": (
                    "Hundreds of printed documents containing classified "
                    "information that Teixeira carried out of the SCIF "
                    "without authorization. The paper copies are physical "
                    "artifacts (gUFO-typed); the underlying Government "
                    "Documents and the photographs of the printouts "
                    "posted to Discord are the cyber observables. "
                    + src_ref("sentencing_memorandum", "pp. 6-7")
                ),
            },
        ]
    )

    # ------------------------------------------------------------------
    # Classification markings (uco-marking) for the charged NDI
    # ------------------------------------------------------------------
    graph.extend(
        marking_definition(
            "marking-ts-sci",
            "TOP SECRET//SCI",
            "Banner attested on the charged Government Documents and "
            "information in Counts One and Three through Six: documents "
            "posted to Discord 'bore standard and conspicuous markings "
            "indicating that they contained highly classified United "
            "States government information,' including 'SECRET, TOP "
            "SECRET, and SCI designations.' "
            + src_ref("indictment", "paras. 12, 16, 18"),
        )
    )
    graph.extend(
        marking_definition(
            "marking-secret",
            "SECRET",
            "Banner attested for the Count Two information (provision of "
            "equipment to Ukraine). " + src_ref("indictment", "para. 16"),
        )
    )
    marking_by_banner = {
        "TOP SECRET//SCI": uid("marking-ts-sci-def"),
        "SECRET": uid("marking-secret-def"),
    }

    # ------------------------------------------------------------------
    # Charged NDI observables, marked with their classification banners
    # ------------------------------------------------------------------
    ndi_ids: dict[int, str] = {}
    for item in CHARGED_NDI:
        n = item["count"]
        label = f"ndi-count{n}"
        ndi_ids[n] = uid(label)
        kind_note = (
            "Classified information transcribed from a classified "
            "workstation into Discord messages."
            if item["kind"] == "information"
            else "Classified Government Document printed in the SCIF, "
            "removed, photographed, and posted to Discord."
        )
        graph.append(
            {
                "@id": uid(label),
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": (
                    f"Count {COUNT_WORDS[n - 1]} NDI ({item['banner']}): "
                    f"{item['desc'][:60].rstrip()}..."
                ),
                "uco-core:description": (
                    f"{item['desc']} Retained and transmitted {item['dates']}. "
                    f"{kind_note} "
                    + src_ref("indictment", "paras. 16, 18 (count charts)")
                ),
                "uco-core:objectMarking": [{"@id": marking_by_banner[item["banner"]]}],
            }
        )
        graph.append(rel(uid(label), usgov, "Owned_By"))

    # ------------------------------------------------------------------
    # Cyber observables: workstation, printer, Discord artifacts, devices
    # ------------------------------------------------------------------
    workstation = uid("obs-classified-workstation")
    scif_printer = uid("obs-scif-printer")
    discord_account = uid("obs-teixeira-discord-account")
    discord_server = uid("obs-discord-server")
    posted_images = uid("obs-posted-document-images")
    ipad = uid("obs-destroyed-ipad")
    desktop = uid("obs-destroyed-desktop")

    graph.extend(
        [
            {
                "@id": workstation,
                "@type": ["uco-observable:Computer", "uco-core:UcoObject"],
                "uco-core:name": "Classified workstation, Otis ANG Base SCIF (JWICS)",
                "uco-core:description": (
                    "Classified workstation from which Teixeira accessed "
                    "the classified documents he transcribed. His signed "
                    "JWICS user agreement stated: 'I will not post "
                    "sensitive systems, intelligence, or other non-public "
                    "information from JWICS to ANY social media site "
                    "which would allow unauthorized entities to obtain "
                    "information that I am not authorized to disseminate "
                    "that can possibly be exploited.' "
                    + src_ref("indictment", "para. 11")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 11 (Doc 86-4 at 4)")
                ),
            },
            {
                "@id": scif_printer,
                "@type": ["uco-observable:Device", "uco-core:UcoObject"],
                "uco-core:name": "Isolated, seldom-used printer inside the Otis SCIF",
                "uco-core:description": (
                    "Printer on which Teixeira printed hundreds of "
                    "documents containing classified information before "
                    "removing them from the SCIF. "
                    + src_ref("sentencing_memorandum", "pp. 6-7")
                ),
            },
            {
                "@id": discord_account,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira's Discord account",
                "uco-core:description": (
                    "Discord account through which Teixeira posted "
                    "transcriptions and photographs of classified "
                    "documents. Teixeira changed the username after his "
                    "conduct became a national news story. At least one "
                    "classified document was found in digital form 'in a "
                    "particular account associated with TEIXEIRA.' "
                    + src_ref("indictment", "para. 12")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 8")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-teixeira-discord-account"),
                        "@type": "uco-observable:DigitalAccountFacet",
                        "uco-observable:displayName": "Teixeira Discord account (username changed April 2023)",
                    }
                ],
            },
            {
                "@id": discord_server,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Discord server / chat rooms where NDI was posted",
                "uco-core:description": (
                    "Discord chat rooms in which Teixeira posted "
                    "classified text and images to other users not "
                    "entitled to receive them, including foreign "
                    "nationals; he later 'deleted the entire contents of "
                    "at least one of the Discord servers where he had "
                    "posted classified documents and information.' A "
                    "friend saw his disclosures recirculating on a "
                    "pro-Russian Telegram channel. "
                    + src_ref("sentencing_memorandum", "pp. 8, 15-16")
                ),
            },
            {
                "@id": posted_images,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Photographs of classified documents posted to Discord",
                "uco-core:description": (
                    "Images of classified Government Documents that "
                    "Teixeira photographed and posted, bearing 'standard "
                    "and conspicuous markings' including SECRET, TOP "
                    "SECRET, and SCI designations; images later became "
                    "'widely distributed around the globe.' "
                    + src_ref("indictment", "para. 12")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 9")
                ),
            },
            {
                "@id": ipad,
                "@type": ["uco-observable:Tablet", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira's iPad (destroyed, recovered from dumpster)",
                "uco-core:description": (
                    "iPad Teixeira destroyed during obstruction; 'found "
                    "smashed in a dumpster outside of his home.' "
                    + src_ref("sentencing_memorandum", "p. 8")
                ),
            },
            {
                "@id": desktop,
                "@type": ["uco-observable:Computer", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira's desktop computer (destroyed)",
                "uco-core:description": (
                    "Desktop computer Teixeira destroyed while "
                    "obstructing the investigation. "
                    + src_ref("sentencing_memorandum", "p. 8")
                ),
            },
        ]
    )
    graph.append(rel(discord_account, teixeira, "Used_By"))
    graph.append(rel(workstation, scif, "Located_At"))
    graph.append(rel(scif_printer, scif, "Located_At"))

    # ------------------------------------------------------------------
    # Quoted Discord messages (verbatim evidence). The 2022-03-15 message
    # preserves Teixeira's incoherent 'TS//NOFORN//FVEY' banner as quoted
    # content only — see module docstring.
    # ------------------------------------------------------------------
    msg_jail = uid("msg-2022-03-15-jail")
    msg_ud_regs = uid("msg-2022-12-ud-regs")
    msg_blog = uid("msg-2023-01-04-blog")
    msg_delete = uid("msg-2023-04-delete")

    graph.extend(
        [
            {
                "@id": msg_jail,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Discord message, 2022-03-15: 'If I want to go to jail for the rest of my life yeah'",
                "uco-core:description": (
                    "Asked by an associate whether he could post "
                    "information regarding troop losses, Teixeira "
                    "responded 'If I want to go to jail for the rest of "
                    "my life yeah' and noted the documents would be "
                    "'TS//NOFORN//FVEY.' He added: 'Not an oath, an NDA "
                    ". . . The oath is just the defense of America "
                    "against all threats and the following of orders,' "
                    "and 'Look I feed info almost verbatim from where I "
                    "read stuff, so to me that gives me ambiguity. "
                    "Leaking docs tho? That's just me asking to be "
                    "caught. Again Chelsea Manning is the perfect "
                    "example.' Note: 'TS//NOFORN//FVEY' is an internally "
                    "contradictory banner (NOFORN prohibits release to "
                    "any foreign national; REL TO FVEY authorizes "
                    "release to Five Eyes partners — the two "
                    "dissemination controls are mutually exclusive), so "
                    "it is preserved here as quoted message content and "
                    "deliberately NOT modeled as a MarkingDefinition. "
                    + src_ref("sentencing_memorandum", "pp. 7-8 (Doc 143-2 at 2)")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-msg-jail"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": discord_account},
                        "uco-observable:messageText": (
                            "If I want to go to jail for the rest of my "
                            "life yeah [...] TS//NOFORN//FVEY [...] Not an "
                            "oath, an NDA . . . The oath is just the "
                            "defense of America against all threats and "
                            "the following of orders. [...] Look I feed "
                            "info almost verbatim from where I read stuff, "
                            "so to me that gives me ambiguity. Leaking "
                            "docs tho? That's just me asking to be caught. "
                            "Again Chelsea Manning is the perfect example."
                        ),
                        "uco-observable:sentTime": lit(
                            "xsd:dateTime", eastern_midnight("2022-03-15")
                        ),
                    }
                ],
            },
            {
                "@id": msg_ud_regs,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Discord message, December 2022: 'I'm breaking a ton of UD regs'",
                "uco-core:description": (
                    "December 2022 Discord message acknowledging "
                    "unauthorized disclosure: 'I'm breaking a ton of UD "
                    "[unauthorized disclosure] regs. IDGAF what they say "
                    "I can or can't share. All of the shit I've told you "
                    "guys I'm not supposed to.' "
                    + src_ref("sentencing_memorandum", "p. 14 (Doc 34-1 at 4)")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-msg-ud-regs"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": discord_account},
                        "uco-observable:messageText": (
                            "I'm breaking a ton of UD regs. IDGAF what "
                            "they say I can or can't share. All of the "
                            "shit I've told you guys I'm not supposed to."
                        ),
                    }
                ],
            },
            {
                "@id": msg_blog,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Discord message, 2023-01-04: blog exchange",
                "uco-core:description": (
                    "Told by another user 'Maybe you should start a "
                    "blog,' Teixeira responded: 'shooting myself in the "
                    "back of the head twice isn't something im fond of. "
                    "None of this is public information and making a "
                    "blog would be the equivalent of what Chelsea "
                    "manning did.' Warned to 'Better be careful then,' "
                    "he replied 'I am.' "
                    + src_ref("sentencing_memorandum", "p. 8 (Doc 34-1 at 4)")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-msg-blog"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": discord_account},
                        "uco-observable:messageText": (
                            "shooting myself in the back of the head "
                            "twice isn't something im fond of. None of "
                            "this is public information and making a "
                            "blog would be the equivalent of what "
                            "Chelsea manning did."
                        ),
                        "uco-observable:sentTime": lit(
                            "xsd:dateTime", eastern_midnight("2023-01-04")
                        ),
                    }
                ],
            },
            {
                "@id": msg_delete,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Discord message, April 2023: 'delete all messages'",
                "uco-core:description": (
                    "Obstruction instruction sent as his conduct became "
                    "a national news story: '[i]f anyone comes looking, "
                    "don't tell them shit,' 'delete all messages,' with "
                    "direction to pass the message to other users. "
                    + src_ref("sentencing_memorandum", "p. 9 (Doc 19-8 at 6)")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-msg-delete"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": discord_account},
                        "uco-observable:messageText": (
                            "If anyone comes looking, don't tell them "
                            "shit. [...] delete all messages."
                        ),
                    }
                ],
            },
        ]
    )
    for msg in (msg_jail, msg_ud_regs, msg_blog, msg_delete):
        graph.append(rel(msg, discord_server, "Contained_Within"))

    # ------------------------------------------------------------------
    # Clearance, training, and agreement timeline (dated Actions)
    # ------------------------------------------------------------------
    act_clearance = uid("act-clearance-2021-07")
    act_indoctrination = uid("act-sci-indoctrination")
    act_refresher = uid("act-ud-refresher-2022-03")
    act_admonitions = uid("act-admonitions")

    graph.extend(
        [
            {
                "@id": act_clearance,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira granted TOP SECRET//SCI clearance (July 2021)",
                "uco-core:description": (
                    "Since in or around July 2021 Teixeira held a TOP "
                    "SECRET//SCI security clearance as required for his "
                    "USANG position. " + src_ref("indictment", "para. 7")
                ),
                "uco-action:performer": {"@id": usgov},
                "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2021-07-01")),
            },
            {
                "@id": act_indoctrination,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira signs SCI indoctrination memoranda (July 2021)",
                "uco-core:description": (
                    "Signed acknowledgment: 'I have been advised that "
                    "the unauthorized disclosure, unauthorized "
                    "retention, or negligent handling of SCI by me "
                    "could cause irreparable injury to the U.S. or be "
                    "used to advantage by a foreign nation. I hereby "
                    "agree that I will never divulge anything marked as "
                    "SCI or that I know to be SCI to anyone who is not "
                    "authorized to receive it.' "
                    + src_ref("sentencing_memorandum", "p. 6")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2021-07-01")),
            },
            {
                "@id": act_refresher,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Unauthorized-disclosure refresher training (March 2022)",
                "uco-core:description": (
                    "Refresher course on the 'Unauthorized Disclosure of "
                    "Classified Information and Controlled Unclassified "
                    "Information' completed just after Teixeira began "
                    "disclosing classified information on Discord "
                    "(certificate: Doc 143-3; student guide: Doc 143-4). "
                    + src_ref("sentencing_memorandum", "p. 6")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2022-03-01")),
            },
            {
                "@id": act_admonitions,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Superiors admonish Teixeira three times to cease viewing classified information",
                "uco-core:description": (
                    "Teixeira 'was admonished on three separate occasions "
                    "by his superiors to cease and desist viewing "
                    "classified information unrelated to his duties.' He "
                    "was undeterred. "
                    + src_ref("sentencing_memorandum", "p. 12")
                ),
                "uco-action:performer": {"@id": usang},
            },
        ]
    )

    # ------------------------------------------------------------------
    # The two charged transmission methods, as Actions with full
    # instrument/object/result wiring
    # ------------------------------------------------------------------
    act_transcribe = uid("act-transcription-exfil")
    act_print_post = uid("act-print-photograph-exfil")

    graph.extend(
        [
            {
                "@id": act_transcribe,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": (
                    "Teixeira transcribes classified text from a classified "
                    "workstation into Discord messages (Jan 2022 - Apr 2023)"
                ),
                "uco-core:description": (
                    "First transmission method: Teixeira accessed "
                    "classified documents containing NDI from a "
                    "classified workstation at Otis USANG Base, manually "
                    "transcribed portions, removed the transcriptions "
                    "from the SCIF without authorization, and, using the "
                    "messaging function on the Social Media Platform, "
                    "input and transmitted the text to users not "
                    "entitled to receive it. Grounds Counts One and Two. "
                    + src_ref("indictment", "paras. 10-11")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:instrument": [
                    {"@id": workstation},
                    {"@id": discord_account},
                ],
                "uco-action:object": [{"@id": ndi_ids[1]}, {"@id": ndi_ids[2]}],
                "uco-action:result": [{"@id": discord_server}],
                "uco-action:location": {"@id": otis_base},
                "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2022-01-01")),
                "uco-action:endTime": lit("xsd:dateTime", eastern_midnight("2023-04-13")),
            },
            {
                "@id": act_print_post,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": (
                    "Teixeira prints, removes, photographs, and posts "
                    "classified documents (2022 - Apr 2023)"
                ),
                "uco-core:description": (
                    "Second transmission method: Teixeira printed "
                    "hundreds of documents containing classified "
                    "information on an isolated, seldom-used SCIF "
                    "printer, removed them from the SCIF without "
                    "authorization, photographed them, and posted the "
                    "images to Discord where they were visible to other "
                    "users. The posted documents bore SECRET, TOP "
                    "SECRET, and SCI designations. Grounds Counts Three "
                    "through Six. "
                    + src_ref("indictment", "para. 12")
                    + "; "
                    + src_ref("sentencing_memorandum", "pp. 6-7")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:instrument": [
                    {"@id": scif_printer},
                    {"@id": discord_account},
                ],
                "uco-action:object": [
                    {"@id": ndi_ids[3]},
                    {"@id": ndi_ids[4]},
                    {"@id": ndi_ids[5]},
                    {"@id": ndi_ids[6]},
                ],
                "uco-action:result": [
                    {"@id": printouts},
                    {"@id": posted_images},
                ],
                "uco-action:location": {"@id": otis_base},
                "uco-action:endTime": lit("xsd:dateTime", eastern_midnight("2023-04-13")),
            },
        ]
    )

    # ------------------------------------------------------------------
    # Obstruction actions (April 2023)
    # ------------------------------------------------------------------
    act_obstruct_instruct = uid("act-obstruct-instruct")
    act_obstruct_delete = uid("act-obstruct-delete-server")
    act_obstruct_destroy = uid("act-obstruct-destroy-devices")

    graph.extend(
        [
            {
                "@id": act_obstruct_instruct,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira instructs Discord associates to delete evidence",
                "uco-core:description": (
                    "Instructed associates on Discord to delete "
                    "electronic evidence and not cooperate with law "
                    "enforcement. Basis (with the other obstruction "
                    "acts) of the USSG § 3C1.1 obstruction enhancement. "
                    + src_ref("sentencing_memorandum", "pp. 8-9")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:instrument": [{"@id": discord_account}],
                "uco-action:result": [{"@id": msg_delete}],
            },
            {
                "@id": act_obstruct_delete,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira changes username and deletes Discord server contents",
                "uco-core:description": (
                    "Changed his Discord username and deleted the entire "
                    "contents of at least one Discord server where he "
                    "had posted classified documents and information. "
                    + src_ref("sentencing_memorandum", "p. 8")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:object": [{"@id": discord_server}, {"@id": discord_account}],
            },
            {
                "@id": act_obstruct_destroy,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Teixeira destroys iPad and desktop computer",
                "uco-core:description": (
                    "Destroyed his electronic devices, including his "
                    "desktop computer and iPad, discarding some in a "
                    "dumpster outside his home; the iPad was found "
                    "smashed. " + src_ref("sentencing_memorandum", "p. 8")
                ),
                "uco-action:performer": {"@id": teixeira},
                "uco-action:object": [{"@id": ipad}, {"@id": desktop}],
                "uco-action:location": {"@id": residence},
            },
        ]
    )

    # ------------------------------------------------------------------
    # FBI investigative actions
    # ------------------------------------------------------------------
    ia_arrest = uid("ia-fbi-arrest")
    ia_seizure = uid("ia-fbi-seizure")

    graph.extend(
        [
            {
                "@id": ia_arrest,
                "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
                "uco-core:name": "FBI arrests Teixeira (2023-04-13)",
                "uco-core:description": (
                    "Teixeira was arrested by the FBI on April 13, 2023, "
                    "and charged by complaint the next day with violating "
                    "18 U.S.C. § 793. "
                    + src_ref("sentencing_memorandum", "p. 5")
                ),
                "uco-action:performer": {"@id": fbi},
                "uco-action:object": [{"@id": teixeira}],
                "uco-action:location": {"@id": residence},
                "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2023-04-13")),
            },
            {
                "@id": ia_seizure,
                "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
                "uco-core:name": "FBI seizes papers, digital media, and electronic devices (2023-04-13)",
                "uco-core:description": (
                    "'[A]ll papers, digital media, electronic devices, "
                    "and other items seized from Defendant's residence, "
                    "vehicle, and person on or about April 13, 2023,' "
                    "which the plea agreement stipulates were 'lawfully "
                    "seized' and remain in FBI custody; Teixeira "
                    "abandoned all claims to them. "
                    + src_ref("plea_agreement", "para. 7")
                ),
                "uco-action:performer": {"@id": fbi},
                "uco-action:result": [{"@id": ipad}, {"@id": desktop}],
                "uco-action:location": {"@id": residence},
                "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2023-04-13")),
            },
        ]
    )
    graph.append(rel(ia_arrest, investigation, "part_of"))
    graph.append(rel(ia_seizure, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Charging instruments (complaint -> indictment)
    # ------------------------------------------------------------------
    complaint = uid("instrument-complaint")
    indictment = uid("instrument-indictment")

    graph.extend(
        [
            {
                "@id": complaint,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": "Criminal complaint (2023-04-14)",
                "legalproc:instrumentType": "complaint",
                "uco-core:description": (
                    "Complaint charging a violation of 18 U.S.C. § 793, "
                    "filed the day after the FBI arrest. "
                    + src_ref("sentencing_memorandum", "p. 5")
                ),
            },
            {
                "@id": indictment,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": "Indictment, Doc 48 (filed 2023-06-15)",
                "legalproc:instrumentType": "indictment",
                "uco-core:description": (
                    "Six counts of Willful Retention and Transmission of "
                    "National Defense Information (18 U.S.C. § 793(e)) "
                    "plus a forfeiture allegation (18 U.S.C. §§ "
                    "981(a)(1)(C), 793(h); 28 U.S.C. § 2461(c)). The "
                    "sentencing memorandum describes the grand jury as "
                    "returning the indictment in May 2023; the filed "
                    "document is stamped 2023-06-15. "
                    + src_ref("indictment", "caption")
                ),
            },
        ]
    )
    graph.append(rel(indictment, complaint, "Supersedes"))
    graph.append(rel(indictment, doc_ids["indictment"], "Derived_From"))
    graph.append(rel(complaint, investigation, "part_of"))
    graph.append(rel(indictment, investigation, "part_of"))

    # ------------------------------------------------------------------
    # The six § 793(e) counts
    # ------------------------------------------------------------------
    charge_ids: list[str] = []
    for item in CHARGED_NDI:
        n = item["count"]
        label = f"charge-count{n}"
        charge_ids.append(uid(label))
        graph.append(
            {
                "@id": uid(label),
                "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                "uco-core:name": (
                    f"Count {COUNT_WORDS[n - 1]}: Willful Retention and "
                    "Transmission of National Defense Information "
                    "(18 U.S.C. § 793(e))"
                ),
                "legalproc:statuteCitation": "18 U.S.C. § 793(e)",
                "legalproc:countNumber": lit("xsd:nonNegativeInteger", n),
                "legalproc:countLabel": f"Count {COUNT_WORDS[n - 1]}",
                "legalproc:offenseForm": "substantive",
                "legalproc:chargeDisposition": "convicted-by-plea",
                "legalproc:assertedIn": [{"@id": indictment}],
                "uco-core:description": (
                    f"Charges that {item['dates']}, having unauthorized "
                    "possession of, access to, and control over "
                    f"{'information' if item['kind'] == 'information' else 'documents'} "
                    "relating to the national defense, Teixeira willfully "
                    "communicated, delivered, and transmitted it to "
                    "persons not entitled to receive it and willfully "
                    f"retained it. Charged NDI ({item['banner']}): "
                    f"{item['desc']} "
                    + src_ref("indictment", "paras. 15-18")
                ),
            }
        )
        graph.append(rel(teixeira, uid(label), "Charged_With"))
        graph.append(rel(uid(label), ndi_ids[n], "Concerns"))
        graph.append(rel(usgov, uid(label), "Victim_Of"))
        exfil_action = act_transcribe if n <= 2 else act_print_post
        graph.append(rel(exfil_action, uid(label), "Basis_Of"))

    # ------------------------------------------------------------------
    # Forfeiture allegation
    # ------------------------------------------------------------------
    forfeiture = uid("forfeiture-allegation")
    graph.append(
        {
            "@id": forfeiture,
            "@type": ["legalproc:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Forfeiture allegation (18 U.S.C. §§ 981(a)(1)(C), 793(h); 28 U.S.C. § 2461(c))",
            "uco-core:description": (
                "Forfeiture of any property constituting or derived from "
                "proceeds traceable to the offenses, and, under § 793(h), "
                "any property derived from proceeds obtained from any "
                "foreign government as the result of the offenses, with "
                "substitute-assets provision (21 U.S.C. § 853(p)). In "
                "the plea agreement Teixeira admitted the forfeiture "
                "allegations and abandoned all seized property to FBI "
                "disposal, including the items seized 2023-04-13 from "
                "his residence, vehicle, and person. "
                + src_ref("indictment", "forfeiture allegation")
                + "; "
                + src_ref("plea_agreement", "para. 7")
            ),
            "legalproc:concernsCharge": [{"@id": cid} for cid in charge_ids],
        }
    )
    graph.append(rel(forfeiture, indictment, "Contained_Within"))

    # ------------------------------------------------------------------
    # Plea and proceedings
    # ------------------------------------------------------------------
    plea = uid("plea-guilty")
    plea_hearing = uid("proceeding-plea-hearing")

    graph.extend(
        [
            {
                "@id": plea,
                "@type": ["legalproc:Plea", "uco-core:UcoObject"],
                "uco-core:name": "Guilty plea to Counts One through Six (2024-03-04)",
                "legalproc:pleaType": "guilty",
                "legalproc:concernsCharge": [{"@id": cid} for cid in charge_ids],
                "uco-core:description": (
                    "Rule 11(c)(1)(C) plea agreement executed 2024-02-28 "
                    "and filed 2024-03-04 (Doc 130); Teixeira pleaded "
                    "guilty to all six counts on 2024-03-04 (Doc 131). "
                    "Agreed disposition: incarceration of 132-200 "
                    "months, a $50,000 fine, 36 months of supervised "
                    "release, a $600 special assessment, and forfeiture. "
                    "The agreement also imposes a lifetime obligation to "
                    "protect classified and national defense "
                    "information, DoD/FBI pre-publication review of any "
                    "future writings, assignment to the United States "
                    "of any profits from publicity, and a prohibition "
                    "on contact with foreign governments or their "
                    "agents without FBI permission. The Court deferred "
                    "acceptance pending the Presentence Report (Rule "
                    "11(c)(3)(A)). "
                    + src_ref("plea_agreement", "paras. 1, 5, 8-10")
                ),
            },
            {
                "@id": plea_hearing,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Change-of-plea hearing (2024-03-04)",
                "legalproc:proceedingType": "plea-hearing",
                "uco-core:description": (
                    "Teixeira entered a guilty plea to each of the six "
                    "counts charged in the indictment (Doc 131). "
                    + src_ref("sentencing_memorandum", "p. 5")
                ),
            },
        ]
    )
    graph.append(rel(plea, plea_hearing, "Occurred_During"))
    graph.append(rel(plea, teixeira, "Relates_To"))
    graph.append(rel(plea, doc_ids["plea_agreement"], "Derived_From"))
    graph.append(rel(plea_hearing, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Recommended sentence (sentencing had not occurred in this record)
    # ------------------------------------------------------------------
    sentence = uid("sentence-recommended")
    graph.append(
        {
            "@id": sentence,
            "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
            "uco-core:name": "Government sentencing recommendation: 200 months (2024-10-29)",
            "legalproc:sentenceStatus": "recommended",
            "legalproc:sentenceTerm": "200 months",
            "legalproc:concernsCharge": [{"@id": cid} for cid in charge_ids],
            "uco-core:description": (
                "Government recommendation at the top of the Rule "
                "11(c)(1)(C) range: 200 months of incarceration, 36 "
                "months of supervised release, a $50,000 fine, and a "
                "$600 special assessment. Guidelines: base offense "
                "level 35 (USSG § 2M3.2, top-secret information), +2 "
                "abuse of a position of trust (§ 3B1.3), +2 obstruction "
                "(§ 3C1.1), -3 acceptance of responsibility (§ 3E1.1), "
                "-2 zero-point offender; total offense level 34, CHC I, "
                "advisory range 151-188 months; the government invoked "
                "USSG § 5K2.14 (significant endangerment of national "
                "security) and compared United States v. Schulte (480 "
                "months), McLean, Glenn, Martin, Winner, and Dalke. "
                + src_ref("sentencing_memorandum", "pp. 9-16")
            ),
        }
    )
    graph.append(rel(sentence, doc_ids["sentencing_memorandum"], "Derived_From"))
    graph.append(rel(sentence, usao, "Relates_To"))

    # ------------------------------------------------------------------
    # Investigation-level wiring
    # ------------------------------------------------------------------
    graph.append(rel(teixeira, investigation, "Subject_Of"))
    graph.append(rel(kendall, investigation, "Relates_To"))
    graph.append(rel(agent_church, investigation, "Relates_To"))
    for org in (fbi, usao, doj_nsd):
        graph.append(rel(org, investigation, "Relates_To"))

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
            # UCO Marking namespace: USG classification banners on the
            # charged NDI observables (see UCO issues #646/#647).
            "marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
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
