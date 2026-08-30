#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Lindell et al. (D.N.D. kidnapping case).

Case 3:25-cr-00005-PDW (D.N.D., Chief Judge Peter D. Welte): a six-count
prosecution of four members of a methamphetamine trafficking organization
who kidnapped Victim A at gunpoint on March 5-6, 2024 to collect a $6,000
drug debt, held him for ransom at a Moorhead, Minnesota residence, forced
him to call family and friends for money, and kept his Ford F-250 after he
escaped. Defendant Kyle Kahalehili Maez-Schaack pleaded guilty to Counts 1,
2, 4, and 6 and was sentenced to a total of 360 months.

Sources (PACER):
  - Second Superseding Indictment: Document 66  (filed 2025-09-18)
  - Plea Agreement (Maez-Schaack):  Document 101 (filed 2026-02-13)
  - Judgment (Maez-Schaack):        Document 128 (filed 2026-06-01)

MCP extraction artifacts: examples/pacer/ndnd_2025_cr_00005/mcp_outputs/*

Extensions exercised:
  - extensions/legalproc — charges (substantive, conspiracy, derivative
    924(c)), superseding indictment, guilty plea, recommended and imposed
    sentences, dismissals.
  - extensions/weapons — first exemplar: the SIG Sauer P365 9mm pistol
    (Serial Number 66F717834) as weap:Handgun and the seventeen 9mm rounds
    as weap:Ammunition, with make/model/caliber/serialNumber queryable
    instead of buried in descriptions. CCO Artifact Ontology and gUFO
    grounding come from the extension's bridge files.
  - extensions/drugs — first exemplar: the charged 500-gram
    methamphetamine mixture as drug:ControlledSubstance, chemically
    identified by ChEBI IRI reference (CHEBI_6809) and grounded as
    gufo:Quantity (amount of matter) via the bridge file.

Source-fidelity conventions:
  - Court dates are date-only facts rendered at local midnight Central time
    with the correct seasonal UTC offset.
  - Charged quantities are kept verbatim ("500 grams or more of a mixture
    and substance containing methamphetamine") with the threshold recorded
    numerically.
  - Victim identity is "Victim A", exactly as charged. The indictment
    charges the firearm possession on or about 2024-04-02 while the plea
    factual basis narrates the vehicle crash and abandonment on 2024-04-06;
    both dates are kept verbatim where each document is cited.
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

CASE_ID = "lindell-ndnd-2025-kidnapping"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "lindell-ndnd-2025-kidnapping.jsonld"

PACER_DOCKET = "3:25-cr-00005-PDW"
JUDGMENT_CASE_NUMBER = "3:25-cr-05-02"  # defendant-2 (Maez-Schaack) caption
LOCAL_REF = "uploads/kidnapping"

SOURCE_DOCS = {
    "indictment2": {
        "file_name": "pacer -- kidnapping -- second superseding indictment.pdf",
        "sha256": "a6f83b239201f30f6e6abaf7a3c912e236657ed434312027e0ae91fdfc2d45e3",
        "pacer_doc": "66",
        "filed": "2025-09-18",
    },
    "plea": {
        "file_name": "pacer -- kidnapping -- plea agreement.pdf",
        "sha256": "e58136c0d74e1cb2d5b7c21cb9d1885059c59ac1ada8432fd144f5c13126343e",
        "pacer_doc": "101",
        "filed": "2026-02-13",
    },
    "judgment": {
        "file_name": "pacer -- kidnapping -- judgment.pdf",
        "sha256": "19600f71e35603d8c08f52caf41a636ed6b4af7cebfaf1822b325161e9715a0a",
        "pacer_doc": "128",
        "filed": "2026-06-01",
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

    D.N.D. (Fargo): CDT (-05:00) roughly March-November, CST (-06:00)
    otherwise. Month-level approximation is sufficient for filing dates.
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
            f"{PACER_DOCKET} (D.N.D.); local bundle '{LOCAL_REF}'."
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


def person(label: str, name: str, description: str) -> dict:
    return {
        "@id": uid(label),
        "@type": "uco-identity:Person",
        "uco-core:name": name,
        "uco-core:description": description,
    }


def location(label: str, name: str, description: str) -> dict:
    return {
        "@id": uid(label),
        "@type": "uco-location:Location",
        "uco-core:name": name,
        "uco-core:description": description,
    }


def build_graph() -> dict:
    graph: list[dict] = []

    # ------------------------------------------------------------------
    # Source documents
    # ------------------------------------------------------------------
    doc_ids: dict[str, str] = {}
    for key, meta in SOURCE_DOCS.items():
        node = source_observable(f"doc-{key}", meta)
        doc_ids[key] = node["@id"]
        graph.append(node)

    # ------------------------------------------------------------------
    # Investigation
    # ------------------------------------------------------------------
    investigation = uid("investigation")
    graph.append(
        {
            "@id": investigation,
            "@type": "case-investigation:Investigation",
            "uco-core:name": "U.S. v. Lindell, Maez-Schaack, Altenor & Lauinger (D.N.D. kidnapping)",
            "uco-core:description": (
                "Federal prosecution in the District of North Dakota (Chief "
                "Judge Peter D. Welte) of four members of a methamphetamine "
                "trafficking organization who kidnapped Victim A at gunpoint "
                "on March 5-6, 2024 to collect a $6,000 drug debt, held him "
                "for ransom at a Moorhead, Minnesota residence, and kept his "
                "Ford F-250 after he escaped. Defendant Maez-Schaack "
                f"(judgment caption {JUDGMENT_CASE_NUMBER}, USM 70239-511) "
                "pleaded guilty to Counts 1, 2, 4, and 6 and was sentenced "
                "on 2026-06-01 to a total of 360 months."
            ),
            "uco-core:tag": [
                "kidnapping", "ransom", "drug-trafficking", "hobbs-act",
                "firearms", "violent-crime",
            ],
            "legalproc:caseIdentifier": PACER_DOCKET,
        }
    )
    for key in doc_ids:
        graph.append(rel(doc_ids[key], investigation, "part_of"))

    # ------------------------------------------------------------------
    # People and organizations
    # ------------------------------------------------------------------
    lindell = uid("person-lindell")
    maez = uid("person-maez-schaack")
    altenor = uid("person-altenor")
    lauinger = uid("person-lauinger")
    uc1 = uid("person-uc1")
    victim_a = uid("person-victim-a")
    mattern = uid("person-mattern")
    judge = uid("person-judge-welte")

    graph.extend(
        [
            person(
                "person-lindell", "Jordan Arlo Lindell",
                "Defendant 1. Led a drug trafficking organization that "
                "primarily distributed methamphetamine in the Red River "
                "Valley and Devils Lake area of North Dakota, often "
                "obtaining it from Minnesota's Twin Cities. Ordered the "
                "kidnapping of Victim A to collect a $6,000 drug debt. The "
                "grand jury found two prior final North Dakota serious-drug-"
                "felony convictions (09-2014-CR-149, judgment 2015-01-12; "
                "09-2019-CR-3820, judgment 2020-07-01). "
                + src_ref("indictment2", "caption; prior convictions; overt acts")
                + "; " + src_ref("plea", "para. 6 factual basis"),
            ),
            person(
                "person-maez-schaack", "Kyle Kahalehili Maez-Schaack",
                "Defendant 2 (USM 70239-511). One of the drug distributors "
                "for Lindell and UC-1; often used as the muscle of the group "
                "and adept at stealing cars. Kidnapped Victim A at gunpoint "
                "at Lindell's direction, pleaded guilty to Counts 1, 2, 4, "
                "and 6, and was sentenced to 360 months. "
                + src_ref("plea", "para. 6 factual basis") + "; "
                + src_ref("judgment", "Sheet 1"),
            ),
            person(
                "person-altenor", "Frankwoodson Altenor",
                "Defendant, a/k/a 'SON SON'. Obtained methamphetamine from "
                "Lindell and Maez-Schaack and often distributed smaller "
                "amounts to his associates; Victim A was held for ransom at "
                "his residence in Moorhead, Minnesota. "
                + src_ref("indictment2", "caption") + "; "
                + src_ref("plea", "para. 6 factual basis"),
            ),
            person(
                "person-lauinger", "Drew David Lauinger",
                "Defendant, charged in Count 1 (kidnapping) of the Second "
                "Superseding Indictment. "
                + src_ref("indictment2", "caption; Count 1"),
            ),
            person(
                "person-uc1", "UC-1 (unindicted co-conspirator)",
                "As-yet unindicted co-conspirator who, with Lindell, was "
                "owed the $6,000 methamphetamine debt and ordered the "
                "kidnapping of Victim A. "
                + src_ref("plea", "para. 6 factual basis"),
            ),
            person(
                "person-victim-a", "Victim A",
                "Kidnapping victim, identified only as Victim A. Owed "
                "Lindell and UC-1 $6,000 for 500 grams or more of "
                "methamphetamine; taken at gunpoint from Fargo, beaten, "
                "held for ransom in Moorhead, Minnesota, and escaped during "
                "daytime March 6, 2024 after being left unattended. "
                + src_ref("indictment2", "Count 1; overt acts 3-5") + "; "
                + src_ref("plea", "para. 6 factual basis"),
            ),
            person(
                "person-mattern", "Brandon Mattern",
                "Person the defendant must not communicate or interact with "
                "under special condition 1 of supervised release; role in "
                "the offense not stated in the reviewed documents. "
                + src_ref("judgment", "Sheet 3D special condition 1"),
            ),
            person(
                "person-judge-welte", "Peter D. Welte",
                "Chief District Judge, District of North Dakota; imposed "
                "judgment on 2026-06-01. " + src_ref("judgment", "Sheet 1"),
            ),
            person(
                "person-toay", "Brian P. Toay",
                "Defense counsel for Maez-Schaack. "
                + src_ref("plea", "preamble") + "; "
                + src_ref("judgment", "Sheet 1"),
            ),
        ]
    )

    usao = uid("org-usao-nd")
    vcrs = uid("org-doj-vcrs")
    fargo_pd = uid("org-fargo-pd")
    dto = uid("org-lindell-dto")
    graph.extend(
        [
            {
                "@id": usao,
                "@type": "uco-identity:Organization",
                "uco-core:name": "U.S. Attorney's Office, District of North Dakota",
                "uco-core:description": (
                    "Prosecuting office. Second Superseding Indictment "
                    "signed by Acting U.S. Attorney Jennifer Klemetsrud "
                    "Puhl; Plea Agreement executed by U.S. Attorney "
                    "Nicholas W. Chase and AUSA Jacob T. Rodenbiker. "
                    + src_ref("indictment2", "signature block") + "; "
                    + src_ref("plea", "preamble and signature block")
                ),
            },
            {
                "@id": vcrs,
                "@type": "uco-identity:Organization",
                "uco-core:name": "DOJ Violent Crime and Racketeering Section",
                "uco-core:description": (
                    "Department of Justice section joining the prosecution: "
                    "Chief David L. Jaffe and Trial Attorney Shriram Harid. "
                    + src_ref("plea", "preamble and signature block")
                ),
            },
            {
                "@id": fargo_pd,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Fargo Police Department",
                "uco-core:description": (
                    "Police department Maez-Schaack attempted to evade on "
                    "2024-04-06 before crashing a stolen vehicle and "
                    "abandoning the SIG Sauer P365. "
                    + src_ref("plea", "para. 6 factual basis")
                ),
            },
            {
                "@id": dto,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Lindell drug trafficking organization",
                "uco-core:description": (
                    "Organization led by Lindell that primarily distributed "
                    "methamphetamine in the Red River Valley and Devils "
                    "Lake area of North Dakota, often obtaining it from "
                    "Minnesota's Twin Cities; used U.S. currency, mobile "
                    "payment apps, social media, and cellular telephones in "
                    "its transactions. "
                    + src_ref("plea", "para. 6 factual basis") + "; "
                    + src_ref("indictment2", "overt acts 9-11")
                ),
                "uco-core:tag": ["drug-trafficking-organization"],
            },
        ]
    )
    graph.append(rel(lindell, dto, "Leader_Of"))
    graph.append(rel(maez, dto, "Member_Of"))
    graph.append(rel(altenor, dto, "Member_Of"))
    graph.append(rel(victim_a, lindell, "Indebted_To"))
    graph.append(rel(victim_a, uc1, "Indebted_To"))

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------
    fargo = uid("loc-fargo")
    moorhead = uid("loc-moorhead-residence")
    crash_site = uid("loc-crash-site")
    rrv = uid("loc-red-river-valley")
    graph.extend(
        [
            location(
                "loc-fargo", "Fargo, North Dakota",
                "City from which Victim A was taken at gunpoint on the "
                "night of 2024-03-05.",
            ),
            location(
                "loc-moorhead-residence",
                "Altenor residence, Moorhead, Minnesota",
                "Residence of co-defendant Frankwoodson Altenor where "
                "Victim A was held for ransom and from which he escaped "
                "during daytime 2024-03-06.",
            ),
            location(
                "loc-crash-site",
                "17th Avenue South and 25th Street South, Fargo, North Dakota",
                "Area where Maez-Schaack crashed a stolen vehicle on "
                "2024-04-06 while attempting to evade Fargo police, fleeing "
                "on foot and leaving behind the SIG Sauer P365 pistol and a "
                "backpack containing a loaded magazine.",
            ),
            location(
                "loc-red-river-valley",
                "Red River Valley and Devils Lake area, North Dakota",
                "Primary distribution territory of the Lindell drug "
                "trafficking organization.",
            ),
            location(
                "loc-twin-cities", "Twin Cities, Minnesota",
                "Frequent source area for the organization's "
                "methamphetamine.",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # Physical evidence.
    # Firearms and ammunition use the weapons extension (weap:) — the
    # first exemplar of extensions/weapons. Vehicles have no extension
    # class yet and keep the UcoObject + gufo:FunctionalComplex
    # dual-typing convention.
    # ------------------------------------------------------------------
    p365 = uid("item-sig-p365")
    rounds = uid("item-9mm-rounds")
    f250 = uid("item-ford-f250")
    stolen_vehicle = uid("item-stolen-vehicle")
    graph.extend(
        [
            {
                "@id": p365,
                "@type": "weap:Handgun",
                "uco-core:name": "SIG Sauer P365 9mm pistol (Serial Number 66F717834)",
                "uco-core:description": (
                    "Black SIG Sauer P365 pistol. Charged as possessed by "
                    "Maez-Schaack on or about 2024-04-02 in furtherance of "
                    "the drug conspiracy (Count 5) and as a felon in "
                    "possession (Count 6); per the plea factual basis, left "
                    "behind in the vicinity of a stolen vehicle Maez-Schaack "
                    "crashed on 2024-04-06 while evading Fargo police (the "
                    "on-or-about charge date and the narrative date are "
                    "kept verbatim from each document). "
                    + src_ref("indictment2", "Counts 5-6") + "; "
                    + src_ref("plea", "para. 6 factual basis")
                ),
                "weap:make": "SIG Sauer",
                "weap:model": "P365",
                "weap:caliber": "9mm",
                "weap:serialNumber": "66F717834",
            },
            {
                "@id": rounds,
                "@type": "weap:Ammunition",
                "uco-core:name": "Seventeen 9mm rounds in a black magazine",
                "uco-core:description": (
                    "Black magazine containing seventeen 9mm rounds, found "
                    "in a backpack Maez-Schaack left near the crashed "
                    "stolen vehicle on 2024-04-06. "
                    + src_ref("plea", "para. 6 factual basis")
                ),
                "weap:caliber": "9mm",
            },
            {
                "@id": f250,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "Ford F-250 automobile (Victim A's vehicle)",
                "uco-core:description": (
                    "Victim A's vehicle, moving in interstate commerce, "
                    "taken from his person and presence by actual and "
                    "threatened force during the kidnapping and kept by "
                    "Maez-Schaack and his co-conspirators afterward; the "
                    "property underlying the Hobbs Act robbery charge "
                    "(Count 3). "
                    + src_ref("indictment2", "Count 3") + "; "
                    + src_ref("plea", "para. 6 factual basis")
                ),
            },
            {
                "@id": stolen_vehicle,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "Stolen vehicle crashed in Fargo on 2024-04-06",
                "uco-core:description": (
                    "Stolen vehicle Maez-Schaack crashed in the area of "
                    "17th Avenue South and 25th Street South, Fargo, while "
                    "attempting to evade Fargo police, then fled on foot. "
                    + src_ref("plea", "para. 6 factual basis")
                ),
            },
        ]
    )
    graph.append(rel(maez, p365, "Possessed"))
    graph.append(rel(maez, rounds, "Possessed"))
    graph.append(rel(rounds, p365, "Related_To"))
    graph.append(rel(f250, victim_a, "Owned_By"))

    # ------------------------------------------------------------------
    # Drug evidence — first exemplar of extensions/drugs. The charged
    # quantity is a portion of matter (gufo:Quantity via the bridge),
    # chemically identified by ChEBI IRI reference.
    # ------------------------------------------------------------------
    meth = uid("item-meth-mixture")
    graph.append(
        {
            "@id": meth,
            "@type": "drug:ControlledSubstance",
            "uco-core:name": "Methamphetamine mixture charged in the Count 2 conspiracy",
            "uco-core:description": (
                "The grand jury specifically found the amount involved in "
                "the conspiracy attributable to Lindell, Maez-Schaack, and "
                "Altenor is 500 grams or more of a mixture and substance "
                "containing methamphetamine, a Schedule II controlled "
                "substance (21 U.S.C. § 841(b)(1)(A)(viii)). The $6,000 "
                "drug debt behind the kidnapping represented at least 500 "
                "grams of methamphetamine. "
                + src_ref("indictment2", "Count 2 drug quantity; overt acts 3-4")
            ),
            "drug:substance": {"@id": "obo:CHEBI_6809"},
            "drug:substanceName": (
                "a mixture and substance containing a detectable amount of "
                "methamphetamine"
            ),
            "drug:csaSchedule": "II",
            "drug:mass": lit("xsd:decimal", "500"),
            "drug:massUnit": "g",
            "drug:purityBasis": "mixture",
            "drug:quantityDescription": (
                "500 grams or more of a mixture and substance containing "
                "methamphetamine"
            ),
        }
    )

    # ------------------------------------------------------------------
    # Cyber observables from the narrative
    # ------------------------------------------------------------------
    texts = uid("obs-lindell-texts")
    screenshot = uid("obs-profile-screenshot")
    ransom_calls = uid("obs-ransom-calls")
    phones = uid("obs-cell-phones")
    apps = uid("obs-payment-apps")
    graph.extend(
        [
            {
                "@id": texts,
                "@type": "uco-observable:Message",
                "uco-core:name": "Text messages from Lindell directing the pickup of Victim A",
                "uco-core:description": (
                    "Lindell sent Maez-Schaack text messages, including a "
                    "screenshot of a social media profile of Victim A and "
                    "an address, and told Maez-Schaack to pick up Victim A "
                    "to collect on the drug debt. These telecommunication "
                    "devices are the interstate-commerce instrumentality "
                    "element of Count 1. "
                    + src_ref("plea", "para. 6 factual basis") + "; "
                    + src_ref("indictment2", "Count 1")
                ),
                "uco-core:tag": ["evidence", "communication"],
            },
            {
                "@id": screenshot,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Screenshot of Victim A's social media profile and an address",
                "uco-core:description": (
                    "Screenshot sent by Lindell to Maez-Schaack identifying "
                    "the kidnapping target and where to find him. "
                    + src_ref("plea", "para. 6 factual basis")
                ),
                "uco-core:tag": ["evidence", "targeting"],
            },
            {
                "@id": ransom_calls,
                "@type": "uco-observable:Call",
                "uco-core:name": "Ransom calls from Victim A to family and friends",
                "uco-core:description": (
                    "While held at the Moorhead residence, one or more "
                    "individuals ordered Victim A to call his friends and "
                    "family to ask for money; despite several calls, Victim "
                    "A was unable to raise any funds. "
                    + src_ref("plea", "para. 6 factual basis")
                ),
                "uco-core:tag": ["evidence", "ransom"],
            },
            {
                "@id": phones,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Cellular telephones used to facilitate methamphetamine distribution",
                "uco-core:description": (
                    "Telecommunication facilities, including cellular "
                    "telephones, used by the conspirators to facilitate the "
                    "distribution of methamphetamine and other controlled "
                    "substances. " + src_ref("indictment2", "overt act 11")
                ),
                "uco-core:tag": ["evidence", "communication"],
            },
            {
                "@id": apps,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Mobile payment apps and social media used in drug transactions",
                "uco-core:description": (
                    "The conspirators used mobile payment apps and social "
                    "media in their drug transactions. "
                    + src_ref("indictment2", "overt act 10")
                ),
                "uco-core:tag": ["evidence", "financial"],
            },
        ]
    )
    graph.append(rel(screenshot, texts, "Contained_Within"))
    graph.append(rel(texts, maez, "Sent_To"))
    graph.append(rel(texts, lindell, "Sent_From"))

    # ------------------------------------------------------------------
    # Charging instrument and charges
    # ------------------------------------------------------------------
    indictment = uid("charging-instrument")
    graph.append(
        {
            "@id": indictment,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "Second Superseding Indictment (Doc 66, filed 2025-09-18)",
            "uco-core:description": (
                "Six-count grand jury indictment against Lindell, "
                "Maez-Schaack, Altenor, and Lauinger, signed by the "
                "foreperson and Acting U.S. Attorney Jennifer Klemetsrud "
                "Puhl. " + src_ref("indictment2", "caption and true bill")
            ),
            "legalproc:instrumentType": "superseding-indictment",
            "uco-core:objectCreatedTime": lit(
                "xsd:dateTime", central_midnight("2025-09-18")
            ),
        }
    )
    graph.append(rel(indictment, doc_ids["indictment2"], "Derived_From"))

    charges = [
        {
            "label": "charge-count1",
            "count": 1,
            "name": "Count 1: Kidnapping",
            "statute": "18 U.S.C. §§ 1201(a)(1) & 2",
            "offense_form": "substantive",
            "disposition": "convicted-by-plea",
            "description": (
                "On or about March 5 and 6, 2024, all four defendants, "
                "individually and by aiding and abetting, kidnapped, "
                "abducted, carried away, seized, confined, and held Victim "
                "A for some purpose or benefit without his consent, using "
                "telecommunication devices — a means, facility, and "
                "instrumentality of interstate and foreign commerce — in "
                "committing or in furtherance of the offense. Disposition "
                "shown is Maez-Schaack's guilty plea; the docket for the "
                "remaining defendants is not among the reviewed documents. "
                + src_ref("indictment2", "Count 1")
            ),
        },
        {
            "label": "charge-count2",
            "count": 2,
            "name": (
                "Count 2: Conspiracy to Possess with Intent to Distribute "
                "and Distribute a Controlled Substance"
            ),
            "statute": "21 U.S.C. §§ 846, 841(a)(1), 841(b)(1)(C), 841(b)(1)(A)(viii)",
            "offense_form": "conspiracy",
            "disposition": "convicted-by-plea",
            "description": (
                "From late February 2024 through early April 2024, "
                "Lindell, Maez-Schaack, and Altenor conspired to possess "
                "with intent to distribute and distribute a "
                "methamphetamine mixture (Schedule II). The grand jury "
                "specifically found 500 grams or more attributable to each "
                "(§ 841(b)(1)(A)(viii)) and found Lindell's two prior "
                "serious-drug-felony convictions. Eleven overt acts "
                "include the $6,000 drug debt (at least 500 grams), "
                "Lindell ordering Maez-Schaack and Altenor to kidnap, "
                "assault, and rob Victim A to collect it, firearm "
                "possession, concealment, U.S. currency, mobile payment "
                "apps and social media, and cellular telephones. "
                + src_ref("indictment2", "Count 2, drug quantity, prior convictions, overt acts 1-11")
            ),
        },
        {
            "label": "charge-count3",
            "count": 3,
            "name": "Count 3: Interference with Commerce by Robbery (Hobbs Act)",
            "statute": "18 U.S.C. §§ 1951 & 2",
            "offense_form": "substantive",
            "disposition": "dismissed",
            "description": (
                "On or about March 5 and 6, 2024, Maez-Schaack and Altenor "
                "obstructed commerce by robbery, taking Victim A's Ford "
                "F-250 — a vehicle moving in interstate commerce — from "
                "his person and presence against his will by actual and "
                "threatened force, violence, and fear of injury. Dismissed "
                "as to Maez-Schaack on the government's motion at "
                "sentencing per the plea agreement. "
                + src_ref("indictment2", "Count 3") + "; "
                + src_ref("judgment", "Sheet 1 dismissals")
            ),
        },
        {
            "label": "charge-count4",
            "count": 4,
            "name": (
                "Count 4: Brandishing a Firearm During and in Relation to "
                "a Crime of Violence"
            ),
            "statute": "18 U.S.C. §§ 924(c)(1)(A)(ii) & 2",
            "offense_form": "derivative",
            "disposition": "convicted-by-plea",
            "object_offense": "charge-count3",
            "description": (
                "On or about March 5 and 6, 2024, Maez-Schaack and Altenor "
                "knowingly brandished firearms during and in relation to a "
                "crime of violence, namely the Hobbs Act robbery charged "
                "in Count 3. Carries a mandatory minimum of 7 years "
                "consecutive to any other sentence. "
                + src_ref("indictment2", "Count 4") + "; "
                + src_ref("plea", "para. 7 penalties")
            ),
        },
        {
            "label": "charge-count5",
            "count": 5,
            "name": (
                "Count 5: Possession of a Firearm in Furtherance of a Drug "
                "Trafficking Crime"
            ),
            "statute": "18 U.S.C. § 924(c)(1)(A)",
            "offense_form": "derivative",
            "disposition": "dismissed",
            "object_offense": "charge-count2",
            "description": (
                "On or about April 2, 2024, Maez-Schaack knowingly "
                "possessed a SIG Sauer, Model P365, 9mm pistol, bearing "
                "Serial Number 66F717834, in furtherance of the drug "
                "trafficking conspiracy charged in Count 2. Dismissed as "
                "to Maez-Schaack on the government's motion at sentencing "
                "per the plea agreement. "
                + src_ref("indictment2", "Count 5") + "; "
                + src_ref("judgment", "Sheet 1 dismissals")
            ),
        },
        {
            "label": "charge-count6",
            "count": 6,
            "name": "Count 6: Possession of a Firearm by a Convicted Felon",
            "statute": "18 U.S.C. §§ 922(g)(1), 924(a)(8) & 2",
            "offense_form": "substantive",
            "disposition": "convicted-by-plea",
            "description": (
                "On or about April 2, 2024, Maez-Schaack, knowing he had "
                "nine prior North Dakota felony convictions (reckless "
                "endangerment x3, drug paraphernalia, fleeing x3, and "
                "controlled-substance possession, judgments entered "
                "2018-12-07, 2020-11-02), knowingly possessed in and "
                "affecting commerce the SIG Sauer P365 pistol, Serial "
                "Number 66F717834. "
                + src_ref("indictment2", "Count 6")
            ),
        },
    ]

    charge_ids: dict[str, str] = {}
    for ch in charges:
        cid = uid(ch["label"])
        charge_ids[ch["label"]] = cid
        node = {
            "@id": cid,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": ch["name"],
            "uco-core:description": ch["description"],
            "legalproc:statuteCitation": ch["statute"],
            "legalproc:countNumber": lit("xsd:nonNegativeInteger", ch["count"]),
            "legalproc:countLabel": f"Count {ch['count']}",
            "legalproc:offenseForm": ch["offense_form"],
            "legalproc:chargeDisposition": ch["disposition"],
            "legalproc:assertedIn": {"@id": indictment},
        }
        if "object_offense" in ch:
            node["legalproc:objectOffense"] = {"@id": uid(ch["object_offense"])}
        graph.append(node)

    charged_with = {
        "charge-count1": [lindell, maez, altenor, lauinger],
        "charge-count2": [lindell, maez, altenor],
        "charge-count3": [maez, altenor],
        "charge-count4": [maez, altenor],
        "charge-count5": [maez],
        "charge-count6": [maez],
    }
    for label, persons in charged_with.items():
        for p in persons:
            graph.append(rel(p, charge_ids[label], "Charged_With"))

    graph.append(rel(charge_ids["charge-count2"], meth, "Relates_To"))
    graph.append(rel(charge_ids["charge-count3"], f250, "Relates_To"))
    graph.append(rel(charge_ids["charge-count5"], p365, "Relates_To"))
    graph.append(rel(charge_ids["charge-count6"], p365, "Relates_To"))

    # ------------------------------------------------------------------
    # Behavior actions
    # ------------------------------------------------------------------
    def action(label: str, name: str, description: str, performers: list[str],
               objects: list[str] | None = None,
               instruments: list[str] | None = None,
               loc: str | None = None,
               start: str | None = None, end: str | None = None) -> str:
        # uco-action:performer has max cardinality 1; the first performer is
        # the primary actor and co-actors are linked with Participated_In
        # relationships.
        node: dict = {
            "@id": uid(label),
            "@type": "uco-action:Action",
            "uco-core:name": name,
            "uco-core:description": description,
            "uco-action:performer": {"@id": performers[0]},
        }
        for co_actor in performers[1:]:
            graph.append(rel(co_actor, uid(label), "Participated_In"))
        if objects:
            node["uco-action:object"] = [{"@id": o} for o in objects]
        if instruments:
            node["uco-action:instrument"] = [{"@id": i} for i in instruments]
        if loc:
            node["uco-action:location"] = {"@id": loc}
        if start:
            node["uco-action:startTime"] = lit("xsd:dateTime", start)
        if end:
            node["uco-action:endTime"] = lit("xsd:dateTime", end)
        graph.append(node)
        return node["@id"]

    act_order = action(
        "action-order-kidnapping",
        "Order the kidnapping of Victim A to collect the drug debt",
        "From on or about March 4 through March 6, 2024, Lindell (with "
        "UC-1) ordered Maez-Schaack and Altenor to kidnap, assault, and "
        "rob Victim A in order to collect on the $6,000 methamphetamine "
        "debt, sending text messages including a screenshot of Victim A's "
        "social media profile and an address. "
        + src_ref("indictment2", "overt act 5") + "; "
        + src_ref("plea", "para. 6 factual basis"),
        performers=[lindell, uc1],
        objects=[victim_a],
        instruments=[texts, screenshot],
        start=central_midnight("2024-03-04"),
        end=central_midnight("2024-03-06"),
    )
    act_kidnap = action(
        "action-kidnapping",
        "Kidnap Victim A at gunpoint and transport him to Moorhead",
        "Beginning in the waning hours of March 5, 2024, Victim A was "
        "taken at gunpoint from Fargo by Maez-Schaack and his "
        "co-conspirators, beaten, and brought in his own Ford F-250 to "
        "Altenor's residence in Moorhead, Minnesota. "
        + src_ref("plea", "para. 6 factual basis"),
        performers=[maez, altenor],
        objects=[victim_a],
        instruments=[f250],
        loc=fargo,
        start=central_midnight("2024-03-05"),
        end=central_midnight("2024-03-06"),
    )
    act_ransom = action(
        "action-ransom-demand",
        "Hold Victim A for ransom and force calls to family and friends",
        "Victim A was held for ransom in the amount of the $6,000 debt at "
        "the Moorhead residence while one or more individuals ordered him "
        "to call his friends and family to ask for money; despite several "
        "calls he was unable to raise any funds. "
        + src_ref("plea", "para. 6 factual basis"),
        performers=[maez, altenor],
        objects=[victim_a],
        instruments=[ransom_calls],
        loc=moorhead,
        start=central_midnight("2024-03-05"),
        end=central_midnight("2024-03-06"),
    )
    act_escape = action(
        "action-escape",
        "Victim A escapes the Moorhead residence",
        "Maez-Schaack, Altenor, and others eventually left Victim A "
        "unattended at the Moorhead residence during daytime March 6, "
        "2024, whereupon Victim A escaped. "
        + src_ref("plea", "para. 6 factual basis"),
        performers=[victim_a],
        loc=moorhead,
        start=central_midnight("2024-03-06"),
        end=central_midnight("2024-03-06"),
    )
    act_keep_vehicle = action(
        "action-retain-vehicle",
        "Keep Victim A's Ford F-250 after the kidnapping",
        "Maez-Schaack and his co-conspirators kept Victim A's vehicle "
        "after the kidnapping — the taking underlying the Hobbs Act "
        "robbery charge (Count 3). "
        + src_ref("plea", "para. 6 factual basis") + "; "
        + src_ref("indictment2", "Count 3"),
        performers=[maez, altenor],
        objects=[f250],
    )
    act_distribute = action(
        "action-distribute-meth",
        "Distribute methamphetamine in North Dakota and Minnesota",
        "From late February 2024 through early April 2024, the "
        "conspirators distributed and possessed with intent to distribute "
        "methamphetamine in North Dakota, Minnesota, and elsewhere, "
        "arranging transfers into North Dakota from out of state and "
        "using currency, mobile payment apps, social media, and cellular "
        "telephones. " + src_ref("indictment2", "overt acts 1-2, 9-11"),
        performers=[lindell, maez, altenor],
        objects=[meth],
        instruments=[phones, apps],
        loc=rrv,
        start=central_midnight("2024-02-24"),
        end=central_midnight("2024-04-06"),
    )
    act_flee = action(
        "action-flee-crash",
        "Crash a stolen vehicle fleeing Fargo police and abandon the pistol",
        "On April 6, 2024, Maez-Schaack crashed a stolen vehicle in the "
        "area of 17th Avenue South and 25th Street South in Fargo after "
        "attempting to evade detection by Fargo police, fled the vehicle, "
        "and left behind the SIG Sauer P365 pistol and a backpack "
        "containing a black magazine with seventeen 9mm rounds. "
        + src_ref("plea", "para. 6 factual basis"),
        performers=[maez],
        objects=[stolen_vehicle, p365, rounds],
        loc=crash_site,
        start=central_midnight("2024-04-06"),
        end=central_midnight("2024-04-06"),
    )
    for act in (act_order, act_kidnap, act_ransom, act_escape,
                act_keep_vehicle, act_distribute, act_flee):
        graph.append(rel(act, investigation, "part_of"))
    graph.append(rel(act_kidnap, charge_ids["charge-count1"], "Relates_To"))
    graph.append(rel(act_keep_vehicle, charge_ids["charge-count3"], "Relates_To"))
    graph.append(rel(act_distribute, charge_ids["charge-count2"], "Relates_To"))
    graph.append(rel(act_flee, charge_ids["charge-count6"], "Relates_To"))

    # ------------------------------------------------------------------
    # Plea, sentencing recommendation, proceedings, judgment
    # ------------------------------------------------------------------
    plea = uid("plea-maez")
    graph.append(
        {
            "@id": plea,
            "@type": ["legalproc:Plea", "uco-core:UcoObject"],
            "uco-core:name": "Maez-Schaack guilty plea to Counts 1, 2, 4, and 6",
            "uco-core:description": (
                "Plea agreement under Fed. R. Crim. P. 11(c)(1)(A) and (B) "
                "(11(c)(1)(C) expressly inapplicable), executed 2026-02-13 "
                "by U.S. Attorney Nicholas W. Chase, AUSA Jacob T. "
                "Rodenbiker, VCRS Chief David L. Jaffe, Trial Attorney "
                "Shriram Harid, defendant Maez-Schaack, and defense counsel "
                "Brian P. Toay. Includes an admitted factual basis, appeal "
                "and collateral-attack waivers (reserving above-guidelines "
                "sentences and ineffective-assistance claims), and the "
                "government's agreement to move to dismiss Counts 3 and 5. "
                + src_ref("plea", "paras. 1-6, 17, 21-22")
            ),
            "legalproc:pleaType": "guilty",
            "legalproc:concernsCharge": [
                {"@id": charge_ids[c]} for c in
                ("charge-count1", "charge-count2", "charge-count4", "charge-count6")
            ],
            "uco-core:objectCreatedTime": lit(
                "xsd:dateTime", central_midnight("2026-02-13")
            ),
        }
    )
    graph.append(rel(plea, doc_ids["plea"], "Derived_From"))
    graph.append(rel(plea, maez, "Relates_To"))

    sentence_rec = uid("sentence-recommended")
    graph.append(
        {
            "@id": sentence_rec,
            "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
            "uco-core:name": "Agreed guideline calculation and government recommendation",
            "uco-core:description": (
                "The parties agreed to a base offense level of 32 on "
                "Counts 1, 2, and 6 (USSG § 2A4.1(a)) with a 6-level "
                "upward adjustment for a ransom demand (§ 2A4.1(b)(1)), "
                "and a 7-year consecutive guideline sentence on Count 4 "
                "(§ 2K2.4(b)). The government agreed to recommend a "
                "3-level acceptance-of-responsibility reduction "
                "(§ 3E1.1(a)-(b)), a prison sentence at the low end of the "
                "applicable guidelines range, and five years of supervised "
                "release. " + src_ref("plea", "paras. 13-17")
            ),
            "legalproc:sentenceStatus": "recommended",
            "legalproc:sentenceTerm": (
                "low end of the applicable guidelines range + 5 years "
                "supervised release (offense level 32 + 6 ransom - 3 "
                "acceptance; 84 months consecutive on Count 4)"
            ),
            "legalproc:concernsCharge": [
                {"@id": charge_ids[c]} for c in
                ("charge-count1", "charge-count2", "charge-count4", "charge-count6")
            ],
        }
    )
    graph.append(rel(sentence_rec, doc_ids["plea"], "Derived_From"))
    graph.append(rel(sentence_rec, maez, "Relates_To"))

    sentencing = uid("proceeding-sentencing")
    graph.append(
        {
            "@id": sentencing,
            "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
            "uco-core:name": "Sentencing hearing (judgment imposed 2026-06-01)",
            "uco-core:description": (
                "Sentencing before Chief Judge Peter D. Welte; judgment "
                "imposed June 1, 2026, and Counts 3 and 5 dismissed on the "
                "government's motion. " + src_ref("judgment", "Sheet 1")
            ),
            "legalproc:proceedingType": "sentencing-hearing",
            "uco-core:objectCreatedTime": lit(
                "xsd:dateTime", central_midnight("2026-06-01")
            ),
        }
    )
    graph.append(rel(sentencing, doc_ids["judgment"], "Derived_From"))

    sentence_imposed = uid("sentence-imposed")
    graph.append(
        {
            "@id": sentence_imposed,
            "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
            "uco-core:name": "Sentence imposed on Maez-Schaack (2026-06-01): 360 months",
            "uco-core:description": (
                "276 months on each of Counts 1 and 2 and 180 months on "
                "Count 6, concurrent, plus 84 months on Count 4 "
                "consecutive, for a total of 360 months with credit for "
                "time served; supervised release of 5 years on Counts 1, "
                "2, and 4 and 3 years on Count 6, concurrent; $400 special "
                "assessment ($100 per count); no fine or restitution. BOP "
                "recommendations: placement near Flagstaff, Arizona, the "
                "500-hour Residential Drug Abuse Treatment Program, "
                "educational/vocational programming, and mental health "
                "treatment. Special conditions include no contact with "
                "Brandon Mattern, total abstinence from alcohol and "
                "illegal drugs, chemical dependency and mental health "
                "treatment, and a search condition covering person, "
                "property, vehicles, computers, and electronic storage. "
                + src_ref("judgment", "Sheets 2-6")
            ),
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceTerm": (
                "360 months (276 mo Counts 1-2 and 180 mo Count 6 "
                "concurrent; 84 mo Count 4 consecutive)"
            ),
            "legalproc:concernsCharge": [
                {"@id": charge_ids[c]} for c in
                ("charge-count1", "charge-count2", "charge-count4", "charge-count6")
            ],
        }
    )
    graph.append(rel(sentence_imposed, doc_ids["judgment"], "Derived_From"))
    graph.append(rel(sentence_imposed, maez, "Relates_To"))
    graph.append(rel(sentence_imposed, sentencing, "Occurred_During"))
    graph.append(rel(sentence_imposed, mattern, "Restricts_Contact_With"))
    graph.append(rel(sentence_imposed, judge, "Imposed_By"))

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            # Namespace proposed to CASE in issue #192 (committee decides the
            # final IRI); implemented locally by extensions/legalproc/.
            "legalproc": "https://ontology.caseontology.org/case/criminal/",
            # Local extensions for physical evidence (extensions/weapons,
            # extensions/drugs); example.org namespaces are placeholders
            # pending a community namespace decision.
            "weap": "http://example.org/ontology/weapons/",
            "drug": "http://example.org/ontology/drugs/",
            # OBO Foundry IRIs (ChEBI chemical identities referenced by
            # drug:substance).
            "obo": "http://purl.obolibrary.org/obo/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            # gUFO upper ontology, used via the CDO alignment profile
            # (CDO-Shapes-gufo) for physical items without extension classes
            # (vehicles). Weapons and drugs get their gUFO grounding from
            # the extensions' bridge files.
            "gufo": "http://purl.org/nemo/gufo#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    exts = ["legalproc", "weapons", "drugs"]
    report = validate_graph_file(path, extensions=exts, project_root=ROOT)
    print(report.safe_summary)
    for ext in exts:
        paths = load_extension_ontology_paths(ext, mode="full", project_root=ROOT)
        print(f"Validated with {len(paths)} {ext} ontology files")
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
