#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Perry & O'Dell (W.D. Mo. militia case).

Case 2:22-cr-04065-BCW (W.D. Mo., Central Division): a 45-count prosecution
of two members of the "2nd American Militia" who conspired to travel to the
United States - Mexico border to murder Border Patrol agents and immigrants,
and who attempted to murder seven FBI Special Agents when a federal search
warrant was executed at O'Dell's residence in Warsaw, Missouri on
2022-10-07 (Perry fired ~11 rifle rounds at the agents).

Sources (PACER):
  - Criminal docket (all defendants), retrieved after termination 2025-08-27
  - Third Superseding Indictment: Document 48  (filed 2023-10-24)
  - Government Sentencing Memorandum (Perry): Document 214 (filed 2025-08-15)

MCP extraction artifacts: examples/pacer/wdmo_2022_cr_04065/mcp_outputs/*.jsonld

Extension: extensions/legalproc (Legal Process and Procedure Extension) —
local implementation of the criminal-process stub concepts proposed to CASE
in issues #191/#192, exercised here on conspiracy, attempt, and derivative
(18 U.S.C. § 924(c)) charges, jury verdicts, a mid-trial plea, dismissals,
an acquittal, count merger, life sentences, forfeiture, restitution, and
appeal.

Source-fidelity conventions:
  - Court dates are date-only facts rendered at local midnight Central time
    with the correct seasonal UTC offset (fabrication-free convention
    matching the Anchorage and Lichtenstein exemplars).
  - Quoted language ("we're out to shoot to kill", "good to go") is kept
    verbatim from the charging instrument.
  - Victim identities are initials only, exactly as charged.
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

CASE_ID = "perry-odell-wdmo-2022-militia"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "perry-odell-wdmo-2022-militia.jsonld"

PACER_DOCKET = "2:22-cr-04065-BCW"
MAGISTRATE_DOCKETS = "2:22-mj-03026-WJE; 2:22-mj-03027-WJE"
APPEAL_DOCKET = "25-2763 (8th Cir.)"
LOCAL_REF = "outside_pacer -- assault & attempted murder"

SOURCE_DOCS = {
    "docket": {
        "file_name": "pacer -- assault & attempted murder -- docket.pdf",
        "sha256": "1cb5dfa80f51aded8a13cbebb2c3da1d45cc3094155ace8c99945b9867852d0e",
        "pacer_doc": "criminal docket sheet",
        "filed": "2025-08-27",
    },
    "indictment3": {
        "file_name": "pacer -- assault & attempted murder -- third superseding indictment .pdf",
        "sha256": "843fc089cc5a311758e8803f242bdf670b14ef8d765939411c9df6494441adb9",
        "pacer_doc": "48",
        "filed": "2023-10-24",
    },
    "sentencing_memo": {
        "file_name": "pacer -- assault & attempted murder -- sentencing memorandum.pdf",
        "sha256": "38730791d0238cb9375e12ae0c92496a345040bfe0180919dc232400f5af4aac",
        "pacer_doc": "214",
        "filed": "2025-08-15",
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

    W.D. Mo.: CDT (-05:00) roughly March-November, CST (-06:00) otherwise.
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
            f"{PACER_DOCKET} (W.D. Mo.); local bundle '{LOCAL_REF}'."
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
# Charge table from the Third Superseding Indictment (Doc 48).
# Each entry: (label, count_label, count_numbers, name, statute, felony class,
#              offense form, description, dispositions-per-defendant note)
# ---------------------------------------------------------------------------
ATTEMPTED_MURDER_VICTIMS = ["J.R.", "J.C.", "R.G.", "D.H.", "C.H.", "T.R.", "T.M."]

CHARGES = [
    {
        "label": "charge-count1",
        "count_label": "Count 1",
        "counts": [1],
        "name": "Conspiracy to Murder a Federal Officer and Employee",
        "statute": "18 U.S.C. §§ 1117 & 1114",
        "felony_class": "Class A Felony",
        "offense_form": "conspiracy",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Beginning at least as early as 2022-08-20 and continuing through "
            "2022-10-07, Perry and O'Dell conspired to kill officers and "
            "employees of the United States — specifically U.S. Border Patrol "
            "agents who would attempt to stop them from shooting at immigrants "
            "at the United States - Mexico border — and to acquire supplies "
            "from murdered agents. Overt acts are detailed in paragraphs 12-42. "
            + src_ref("indictment3", "Count 1, paras. 43-49")
        ),
    },
    {
        "label": "charge-count2",
        "count_label": "Count 2",
        "counts": [2],
        "name": "Conspiracy to Assault a Federal Officer and Employee",
        "statute": "18 U.S.C. §§ 371 & 111(a)(1)",
        "felony_class": "Class D Felony",
        "offense_form": "conspiracy",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Conspiracy to forcibly assault, resist, oppose, impede, "
            "intimidate, or interfere with U.S. Border Patrol officers and "
            "employees engaged in official duties. "
            + src_ref("indictment3", "Count 2, paras. 50-56")
        ),
    },
    {
        "label": "charge-count3",
        "count_label": "Count 3",
        "counts": [3],
        "name": "Conspiracy to Injure Officer",
        "statute": "18 U.S.C. § 372",
        "felony_class": "Class D Felony",
        "offense_form": "conspiracy",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Conspiracy to injure officers and employees of the United States "
            "on account of, or during, the lawful discharge of their duties; "
            "manner and means included preparing for travel to Texas, "
            "recruiting participants, staging firearms and paramilitary gear "
            "in Warsaw, Missouri, and using force against FBI Special Agents. "
            + src_ref("indictment3", "Count 3, paras. 57-60")
        ),
    },
    {
        "label": "charge-counts4-10",
        "count_label": "Counts 4-10",
        "counts": list(range(4, 11)),
        "name": "Attempted Murder of a Federal Officer and Employee",
        "statute": "18 U.S.C. §§ 1114(a)(3), 1113 & 2",
        "felony_class": "Class C Felony",
        "offense_form": "attempt",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "On 2022-10-07 in Benton County, Missouri, the defendants "
            "attempted to kill seven FBI Special Agents (victims J.R., J.C., "
            "R.G., D.H., C.H., T.R., T.M.), one victim per count, while each "
            "agent was engaged in the performance of his duties. "
            + src_ref("indictment3", "Counts 4-10, paras. 61-62")
        ),
    },
    {
        "label": "charge-counts11-17",
        "count_label": "Counts 11-17",
        "counts": list(range(11, 18)),
        "name": "Assault of a Federal Officer and Employee with a Deadly or Dangerous Weapon",
        "statute": "18 U.S.C. §§ 111(a)(1), (b) & 2",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Forcible assault of the same seven FBI Special Agents with a "
            "deadly or dangerous weapon, one victim per count. "
            + src_ref("indictment3", "Counts 11-17, paras. 63-64")
        ),
    },
    {
        "label": "charge-count18",
        "count_label": "Count 18",
        "counts": [18],
        "name": "Assault of a Federal Officer and Employee That Inflicts Bodily Injury",
        "statute": "18 U.S.C. §§ 111(a)(1), (b) & 2",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Forcible assault of FBI Special Agent J.R. inflicting bodily "
            "injury (Perry landed at least one punch causing injury to the "
            "agent's face while resisting arrest). "
            + src_ref("indictment3", "Count 18, para. 65")
            + "; " + src_ref("sentencing_memo", "background, p. 10")
        ),
    },
    {
        "label": "charge-counts19-20",
        "count_label": "Counts 19-20",
        "counts": [19, 20],
        "name": "Assault of a Federal Officer and Employee That Involves Physical Contact",
        "statute": "18 U.S.C. §§ 111(a)(1) & 2",
        "felony_class": "Class D Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Forcible assault involving physical contact with FBI Special "
            "Agents J.A. (Count 19) and R.G. (Count 20). "
            + src_ref("indictment3", "Counts 19-20, paras. 66-67")
        ),
    },
    {
        "label": "charge-counts21-34",
        "count_label": "Counts 21-34",
        "counts": list(range(21, 35)),
        "name": "Use of Firearm in Furtherance of Crime of Violence",
        "statute": "18 U.S.C. §§ 924(c)(1)(A)(iii) & 2",
        "felony_class": "Class A Felony",
        "offense_form": "derivative",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Carrying, using, brandishing, and discharging the Voodoo "
            "Innovations multi-caliber rifle (serial 21221464) during and in "
            "relation to a crime of violence; each count is charged in "
            "furtherance of one predicate count (Counts 21-27 map to the "
            "attempted-murder Counts 4-10; Counts 28-34 map to the "
            "deadly-weapon-assault Counts 11-17). "
            + src_ref("indictment3", "Counts 21-34, paras. 68-69")
        ),
    },
    {
        "label": "charge-count35",
        "count_label": "Count 35",
        "counts": [35],
        "name": "Depredation of Government Property",
        "statute": "18 U.S.C. §§ 1361 & 2",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Perry shot a firearm at a 2016 Lenco Bearcat armored vehicle "
            "(VIN 1FDAF5HT7GEA85510) belonging to the FBI, causing damage "
            "exceeding $1,000 (trial evidence: $3,717.98). "
            + src_ref("indictment3", "Count 35, para. 70")
        ),
    },
    {
        "label": "charge-counts36-37",
        "count_label": "Counts 36-37",
        "counts": [36, 37],
        "name": "Felon in Possession of a Firearm (Perry)",
        "statute": "18 U.S.C. §§ 922(g)(1) & 924(a)(8)",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict", "merged"],
        "description": (
            "Perry, a convicted felon, knowingly possessed the Voodoo "
            "Innovations rifle (Count 36) and the Ruger Security-9 pistol "
            "with an obliterated serial number (Count 37). The government "
            "recommended merging Count 37 into Count 36 at sentencing as "
            "multiplicitous. "
            + src_ref("indictment3", "Counts 36-37, paras. 71-72")
            + "; " + src_ref("sentencing_memo", "p. 2 n.1")
        ),
    },
    {
        "label": "charge-count38",
        "count_label": "Count 38",
        "counts": [38],
        "name": "Possession of a Firearm with an Obliterated Serial Number (Perry)",
        "statute": "26 U.S.C. § 5861(h)",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["dismissed"],
        "description": (
            "Possession of the Ruger Security-9 pistol with obliterated "
            "serial number; dismissed by the United States before verdict. "
            + src_ref("indictment3", "Count 38, para. 73")
            + "; " + src_ref("sentencing_memo", "background, pp. 4-5")
        ),
    },
    {
        "label": "charge-count39",
        "count_label": "Count 39",
        "counts": [39],
        "name": "Possession of Body Armor by Violent Felon (Perry)",
        "statute": "18 U.S.C. §§ 931(a)(1) & 924(a)(7)",
        "felony_class": "Class E Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "Perry possessed an Armored Republic Level III body armor model "
            "(markers 3X12FR and A70-42) after a crime-of-violence felony "
            "conviction. " + src_ref("indictment3", "Count 39, para. 74")
        ),
    },
    {
        "label": "charge-count40",
        "count_label": "Count 40",
        "counts": [40],
        "name": "Possession of Explosive Materials (Perry)",
        "statute": "18 U.S.C. §§ 842(i)(1) & 844(a)(1)",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["acquitted"],
        "description": (
            "Alleged possession of a binary high-explosive mixture of "
            "ammonium nitrate prills and aluminum powder; the jury found "
            "Perry not guilty of this count on 2024-11-07. "
            + src_ref("indictment3", "Count 40, para. 75")
            + "; " + src_ref("docket", "D.E. 148 jury verdict")
        ),
    },
    {
        "label": "charge-count41",
        "count_label": "Count 41",
        "counts": [41],
        "name": "Communicating a Threat to Injure (Perry)",
        "statute": "18 U.S.C. § 875(c)",
        "felony_class": "Class D Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "On 2022-10-03 Perry transmitted in interstate commerce, by "
            "telephone, a communication containing a true threat to injure a "
            "person. " + src_ref("indictment3", "Count 41, para. 76")
        ),
    },
    {
        "label": "charge-count42",
        "count_label": "Count 42",
        "counts": [42],
        "name": "Possession of a Firearm While Subject to Court Order of Protection (O'Dell)",
        "statute": "18 U.S.C. §§ 922(g)(8) & 924(a)(8)",
        "felony_class": "Class C Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-plea"],
        "description": (
            "O'Dell knowingly possessed a Stevens model 320 12-gauge firearm "
            "(serial 142729C) while subject to an order of protection issued "
            "2022-03-18 by the 8th Judicial Circuit, Ray County, Missouri "
            "(case 22RY-CV00106). Pleaded guilty 2024-10-28. "
            + src_ref("indictment3", "Count 42, para. 77")
        ),
    },
    {
        "label": "charge-count43",
        "count_label": "Count 43",
        "counts": [43],
        "name": "Communicating a Threat to Injure (O'Dell)",
        "statute": "18 U.S.C. § 875(c)",
        "felony_class": "Class D Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-verdict"],
        "description": (
            "On 2022-10-02 O'Dell transmitted in interstate commerce, by "
            "telephone, a communication containing a true threat to injure a "
            "person. " + src_ref("indictment3", "Count 43, para. 78")
        ),
    },
    {
        "label": "charge-count44",
        "count_label": "Count 44",
        "counts": [44],
        "name": "False Statement (O'Dell)",
        "statute": "18 U.S.C. § 1001(a)(2)",
        "felony_class": "Class D Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-plea"],
        "description": (
            "On 2022-10-07 O'Dell falsely stated to an FBI Special Agent that "
            "he did not possess a firearm he could carry on his person. "
            "Pleaded guilty 2024-10-28. "
            + src_ref("indictment3", "Count 44, para. 79")
        ),
    },
    {
        "label": "charge-count45",
        "count_label": "Count 45",
        "counts": [45],
        "name": "Escape from Custody (O'Dell)",
        "statute": "18 U.S.C. § 751(a)",
        "felony_class": "Class D Felony",
        "offense_form": "substantive",
        "dispositions": ["convicted-by-plea"],
        "description": (
            "Between 2023-09-29 and 2023-10-01 O'Dell escaped from, and "
            "failed to return to, custody of the Phelps County Jail where he "
            "was confined under a federal detention order. Pleaded guilty "
            "2024-10-28. " + src_ref("indictment3", "Count 45, para. 80")
        ),
    },
]

PERRY_CHARGE_LABELS = [
    "charge-count1", "charge-count2", "charge-count3", "charge-counts4-10",
    "charge-counts11-17", "charge-count18", "charge-counts19-20",
    "charge-counts21-34", "charge-count35", "charge-counts36-37",
    "charge-count38", "charge-count39", "charge-count40", "charge-count41",
]
ODELL_CHARGE_LABELS = [
    "charge-count1", "charge-count2", "charge-count3", "charge-counts4-10",
    "charge-counts11-17", "charge-count18", "charge-counts19-20",
    "charge-counts21-34", "charge-count35", "charge-count42",
    "charge-count43", "charge-count44", "charge-count45",
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
            "uco-core:name": f"United States v. Perry & O'Dell, {PACER_DOCKET} (W.D. Mo.)",
            "legalproc:caseIdentifier": PACER_DOCKET,
            "uco-core:description": (
                "FBI domestic-terrorism investigation and federal prosecution "
                "of two 2nd American Militia members who conspired to travel "
                "to the United States - Mexico border to murder Border Patrol "
                "agents and immigrants, and who attempted to murder seven FBI "
                "Special Agents during execution of a federal search warrant "
                "on 2022-10-07. Docket filed 2022-10-18; terminated "
                f"2025-08-27. Magistrate cases {MAGISTRATE_DOCKETS}; appeal "
                f"{APPEAL_DOCKET}. Counts 1, 4-10, and 35 are designated "
                "'federal crimes of terrorism' under 18 U.S.C. § 2332b(g)(5). "
                + src_ref("docket", "caption") + "; "
                + src_ref("indictment3", "forfeiture allegation para. 82")
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
    perry = uid("person-perry")
    odell = uid("person-odell")
    militia = uid("org-2nd-american-militia")
    fbi = uid("org-fbi")
    border_patrol = uid("org-border-patrol")
    usao = uid("org-usao-wdmo")

    graph.extend(
        [
            {
                "@id": perry,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Bryan C. Perry",
                "uco-core:description": (
                    "Defendant (01), DOB 1985-09-24, resident of Clarksville, "
                    "Tennessee; founding member of the 2nd American Militia. "
                    "Prior felony conviction for aggravated robbery at age 18. "
                    "Convicted by jury on Counts 1-37, 39, and 41; acquitted "
                    "on Count 40. Sentenced 2025-08-27 to Life plus fourteen "
                    "consecutive Life terms (Counts 21-34). "
                    + src_ref("docket", "defendant 1 caption and dispositions")
                ),
            },
            {
                "@id": odell,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Jonathan S. O'Dell",
                "uco-core:description": (
                    "Defendant (02), DOB 1990-04-23, resident of Warsaw, "
                    "Benton County, Missouri. Pleaded guilty mid-trial "
                    "(2024-10-28) to Counts 42, 44, and 45; convicted by jury "
                    "on Counts 1-35 and 43. Sentenced 2025-08-27 to a total "
                    "term of 165 years. "
                    + src_ref("docket", "defendant 2 caption and dispositions")
                ),
            },
            {
                "@id": militia,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "2nd American Militia",
                "uco-core:description": (
                    "Anti-government militia group of which both defendants "
                    "were members (Perry a founding member); the conspiracy "
                    "was organized, recruited for, and advertised under this "
                    "group's identity and logo/patch. "
                    + src_ref("indictment3", "introduction para. 3")
                ),
            },
            {
                "@id": fbi,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Federal Bureau of Investigation",
                "uco-core:description": (
                    "Investigating agency; its Special Agents executed the "
                    "2022-10-07 search warrant, were the victims of the "
                    "attempted murders and assaults, and owned the damaged "
                    "Lenco Bearcat armored vehicle."
                ),
            },
            {
                "@id": border_patrol,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "United States Border Patrol",
                "uco-core:description": (
                    "Agency whose officers and employees were the intended "
                    "murder victims of the charged conspiracy (Counts 1-3)."
                ),
            },
            {
                "@id": usao,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Attorney's Office, Western District of Missouri",
                "uco-core:description": (
                    "Prosecuting office (U.S. Attorney R. Matthew Price; "
                    "AUSAs Casey Clark and Ashley S. Turner)."
                ),
            },
        ]
    )
    graph.append(rel(perry, militia, "Member_Of"))
    graph.append(rel(odell, militia, "Member_Of"))
    graph.append(rel(perry, investigation, "Subject_Of"))
    graph.append(rel(odell, investigation, "Subject_Of"))

    # ------------------------------------------------------------------
    # Defense counsel and representation history (from the docket)
    # ------------------------------------------------------------------
    counsel = [
        (
            "attorney-gray",
            "Benjamin J. Gray",
            perry,
            "CJA counsel appointed for Perry 2022-10-07 (D.E. 4); relieved "
            "2023-06-01 after the court found an irreconcilable conflict "
            "(D.E. 63, 64). " + src_ref("docket", "D.E. 4, 63, 64"),
        ),
        (
            "attorney-kirsch",
            "Thomas J. Kirsch (Kirsch & Kirsch, LLC)",
            perry,
            "CJA counsel appointed for Perry 2023-06-01, succeeding Benjamin "
            "J. Gray; lead attorney through trial and sentencing. The docket "
            "caption also designates Perry PRO SE for portions of the case. "
            + src_ref("docket", "D.E. 64 and caption"),
        ),
        (
            "attorney-wang",
            "Katie Ying Jung Wang (Federal Public Defender)",
            odell,
            "Appointed counsel for O'Dell from 2022-10-11 (D.E. 7) until "
            "2022-11-15, when the defendant retained counsel (D.E. 27). "
            + src_ref("docket", "D.E. 7, 27"),
        ),
        (
            "attorney-dotson",
            "Daniel Dotson",
            odell,
            "Retained counsel for O'Dell from 2022-11-15 through trial, "
            "plea, and sentencing. " + src_ref("docket", "D.E. 27 and minute entries"),
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

    # Victims: FBI Special Agents identified by initials only, as charged.
    victim_ids: dict[str, str] = {}
    for initials in ATTEMPTED_MURDER_VICTIMS + ["J.A."]:
        vid = uid(f"victim-{initials}")
        victim_ids[initials] = vid
        counts_note = (
            "attempted-murder victim (Counts 4-10) and deadly-weapon-assault "
            "victim (Counts 11-17)"
            if initials in ATTEMPTED_MURDER_VICTIMS
            else "physical-contact-assault victim (Count 19)"
        )
        graph.append(
            {
                "@id": vid,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": f"FBI Special Agent {initials}",
                "uco-core:description": (
                    f"FBI Special Agent identified by initials {initials} in "
                    f"the Third Superseding Indictment; {counts_note}. "
                    + src_ref("indictment3", "victim tables, Counts 4-20")
                ),
            }
        )
        graph.append(rel(vid, fbi, "Member_Of"))

    # ------------------------------------------------------------------
    # Firearms and other physical items from the charges.
    #
    # These are deliberately NOT uco-observable objects: firearms, body
    # armor, and vehicles are never cyber-domain items, so typing them as
    # observables would misuse UCO. They are uco-core:UcoObject (the
    # investigation-relevant thing) dual-typed with gufo:FunctionalComplex
    # from the gUFO upper ontology, which UCO maintains a CDO alignment
    # profile for (CDO-Shapes-gufo; see get_uco_profiles("gufo")). The
    # profile gives physical evidence its ontological grounding without
    # pretending it is a cyber artifact.
    # ------------------------------------------------------------------
    physical_item_type = ["uco-core:UcoObject", "gufo:FunctionalComplex"]
    rifle = uid("item-voodoo-rifle")
    ruger = uid("item-ruger-pistol")
    stevens = uid("item-stevens-shotgun")
    body_armor = uid("item-body-armor")
    bearcat = uid("item-fbi-bearcat")
    graph.extend(
        [
            {
                "@id": rifle,
                "@type": physical_item_type,
                "uco-core:name": "Voodoo Innovations multi-caliber rifle (serial 21221464)",
                "uco-core:description": (
                    "Rifle with an Anderson Manufacturing model AM-15 lower "
                    "receiver bearing serial number 21221464; obtained by "
                    "Perry on or about 2022-07-12 (stolen from his "
                    "ex-girlfriend per the sentencing memorandum), "
                    "transported to O'Dell's residence, and discharged "
                    "(~11 shots) at FBI Special Agents on 2022-10-07. "
                    "Subject of Counts 21-34 and 36 and the firearms "
                    "forfeiture allegation. "
                    + src_ref("indictment3", "paras. 11, 13, 40; Counts 21-34, 36")
                ),
            },
            {
                "@id": ruger,
                "@type": physical_item_type,
                "uco-core:name": "Ruger Security-9 9mm pistol (obliterated serial number)",
                "uco-core:description": (
                    "9mm caliber pistol with an obliterated serial number "
                    "transported by Perry from Tennessee to O'Dell's "
                    "residence; subject of Counts 37-38 and the firearms "
                    "forfeiture allegation. "
                    + src_ref("indictment3", "para. 13; Counts 37-38")
                ),
            },
            {
                "@id": stevens,
                "@type": physical_item_type,
                "uco-core:name": "Stevens model 320 12-gauge firearm (serial 142729C)",
                "uco-core:description": (
                    "12-gauge firearm possessed by O'Dell while subject to a "
                    "court order of protection; subject of Count 42 and the "
                    "firearms forfeiture allegation. "
                    + src_ref("indictment3", "Count 42, para. 77")
                ),
            },
            {
                "@id": body_armor,
                "@type": physical_item_type,
                "uco-core:name": "Armored Republic Level III body armor (markers 3X12FR, A70-42)",
                "uco-core:description": (
                    "Body armor possessed by Perry, a violent felon, and "
                    "donned by him before firing on FBI agents; subject of "
                    "Count 39 and the terrorism forfeiture allegation. "
                    + src_ref("indictment3", "Count 39, para. 74; forfeiture para. 83")
                ),
            },
            {
                "@id": bearcat,
                "@type": physical_item_type,
                "uco-core:name": "FBI 2016 Lenco Bearcat armored vehicle (VIN 1FDAF5HT7GEA85510)",
                "uco-core:description": (
                    "FBI armored vehicle struck by Perry's rifle fire on "
                    "2022-10-07; one round struck inches from an agent's "
                    "head. Damage of $3,717.98 underlies Count 35 and the "
                    "restitution request. "
                    + src_ref("indictment3", "Count 35, para. 70")
                    + "; " + src_ref("sentencing_memo", "restitution section")
                ),
            },
        ]
    )
    graph.append(rel(rifle, perry, "Possessed_By"))
    graph.append(rel(ruger, perry, "Possessed_By"))
    graph.append(rel(stevens, odell, "Possessed_By"))
    graph.append(rel(body_armor, perry, "Possessed_By"))
    graph.append(rel(bearcat, fbi, "Owned_By"))

    # ------------------------------------------------------------------
    # Digital observables alleged as overt acts (text messages, TikTok
    # posts, internet searches) — the Hermes/Link-Look-style evidence layer
    # ------------------------------------------------------------------
    msg_map = uid("obs-text-dc-map")
    msg_rifle = uid("obs-text-rifle-photo")
    tiktok_war = uid("obs-tiktok-war")
    tiktok_hunting = uid("obs-tiktok-hunting")
    searches = uid("obs-internet-searches")
    graph.extend(
        [
            {
                "@id": msg_map,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Text message: Washington D.C. map with blockade points (2022-05-15)",
                "uco-core:description": (
                    "Perry sent O'Dell, via text message, a picture of a map "
                    "of Washington, D.C. with labeled location points for a "
                    "blockade of roads. " + src_ref("indictment3", "para. 6")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("obs-text-dc-map-facet"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:messageText": (
                            "[picture of a map of Washington, D.C. with labeled "
                            "location points for a blockade of roads]"
                        ),
                        "uco-observable:sentTime": lit("xsd:dateTime", central_midnight("2022-05-15")),
                    }
                ],
            },
            {
                "@id": msg_rifle,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Text message: rifle photo, 'good to go' (2022-07-12)",
                "uco-core:description": (
                    "Perry texted O'Dell a picture of the Voodoo Innovations "
                    "rifle along with a message that he was 'good to go'. "
                    + src_ref("indictment3", "para. 11")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("obs-text-rifle-photo-facet"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:messageText": "good to go",
                        "uco-observable:sentTime": lit("xsd:dateTime", central_midnight("2022-07-12")),
                    }
                ],
            },
            {
                "@id": tiktok_war,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "TikTok video: 'we're out to shoot to kill' (2022-09-22)",
                "uco-core:description": (
                    "Perry posted a video on TikTok stating 'we're out to "
                    "shoot to kill' and that 'our group is gonna go protect "
                    "this country.' Related posts on 2022-09-12 (Border "
                    "Patrol 'committing treason', penalty 'death') and "
                    "2022-09-13 ('ready to go to war against this "
                    "government'). " + src_ref("indictment3", "paras. 17-20")
                ),
            },
            {
                "@id": tiktok_hunting,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "TikTok video: 'patriots this Saturday 10/08/2022 we are going hunting! IYKYK!!' (2022-10-02)",
                "uco-core:description": (
                    "Perry posted a recruitment video containing the typed "
                    "statement 'patriots this Saturday 10/08/2022 we are "
                    "going hunting! IYKYK!! leaving from warsaw, MO 1200 CT… "
                    "starting from country mart across from dollar general.' "
                    "with music containing the lyric 'Let's go to war.' "
                    + src_ref("indictment3", "para. 30")
                ),
            },
            {
                "@id": searches,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "O'Dell internet searches for weapons and supplies (2022-09-07/08, 2022-10-06)",
                "uco-core:description": (
                    "Internet searches conducted by O'Dell: 'sig 556' "
                    "(2022-09-07/08) and, on 2022-10-06, 'night vision "
                    "goggles payment plan', 'm14 with optic', 'sand viper "
                    "pistol', '404 bolt gun', and '6.5 xm5'. "
                    + src_ref("indictment3", "paras. 16, 37")
                ),
            },
        ]
    )
    for obs, sender in [(msg_map, perry), (msg_rifle, perry), (tiktok_war, perry), (tiktok_hunting, perry), (searches, odell)]:
        graph.append(rel(obs, sender, "Created_By"))
        graph.append(rel(obs, doc_ids["indictment3"], "Referenced_In"))

    # ------------------------------------------------------------------
    # Recruitment targets (Individuals #1-#4, identified only by number
    # and state in the indictment)
    # ------------------------------------------------------------------
    individuals: dict[str, str] = {}
    for num, detail in [
        ("1", "resident of Louisiana contacted via TikTok (paras. 19, 21)"),
        ("2", "resident of Missouri contacted via TikTok about training (para. 23)"),
        ("3", "asked to acquire ham radios and night vision goggles and to join (paras. 29, 33, 36)"),
        ("4", "told of the plan to 'start a war' at the border (paras. 32, 34, 38)"),
    ]:
        iid = uid(f"person-individual-{num}")
        individuals[num] = iid
        graph.append(
            {
                "@id": iid,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": f"Individual #{num}",
                "uco-core:description": (
                    f"Uncharged person identified only as Individual #{num} in "
                    f"the Third Superseding Indictment; recruitment target — "
                    f"{detail}. " + src_ref("indictment3", "general allegations")
                ),
            }
        )

    # ------------------------------------------------------------------
    # Overt acts (Third Superseding Indictment paras. 4-42) as actions,
    # giving the graph a queryable timeline of the conspiracy. Counts 1-3
    # incorporate these paragraphs as their overt acts (paras. 48, 55, 59).
    # Each action has a single uco-action:performer; the co-defendant's
    # involvement is a Participated_In relationship.
    # ------------------------------------------------------------------
    overt_acts = [
        {
            "label": "act-grievance-communications",
            "name": "Perry and O'Dell communicate about grievances and seek supplies (2021-11 to 2022-10)",
            "performer": perry,
            "also": [odell],
            "desc": (
                "Beginning at least as early as November 2021 the defendants "
                "communicated about grievances against the United States "
                "Government and obtained, and attempted to obtain, supplies "
                "to act on them. " + src_ref("indictment3", "para. 4")
            ),
        },
        {
            "label": "act-odell-travel-tennessee",
            "name": "O'Dell travels from Missouri to Tennessee to meet Perry (2022-06-04/05)",
            "performer": odell,
            "start": "2022-06-04",
            "desc": src_ref("indictment3", "para. 8"),
        },
        {
            "label": "act-obtain-rifle",
            "name": "Perry obtains the Voodoo Innovations rifle (2022-07-12)",
            "performer": perry,
            "start": "2022-07-12",
            "objects": [rifle],
            "results": [msg_rifle],
            "desc": (
                "Perry obtained the Voodoo Innovations multi-caliber rifle "
                "(serial 21221464) and texted a picture of it to O'Dell with "
                "the message that he was 'good to go'. "
                + src_ref("indictment3", "para. 11")
            ),
        },
        {
            "label": "act-agreement-war",
            "name": "Perry and O'Dell agree to go 'to war with border patrol' (2022-08-20)",
            "performer": perry,
            "also": [odell],
            "start": "2022-08-20",
            "desc": (
                "The agreement that anchors the conspiracy counts; the "
                "charged conspiracy period runs from this date through "
                "2022-10-07. " + src_ref("indictment3", "para. 12")
            ),
        },
        {
            "label": "act-perry-relocation",
            "name": "Perry relocates to O'Dell's residence transporting firearms and body armor (2022-09-05)",
            "performer": perry,
            "start": "2022-09-05",
            "objects": [rifle, ruger, body_armor],
            "desc": (
                "Perry traveled from Tennessee to Warsaw, Missouri to reside "
                "with O'Dell, transporting the Ruger Security-9 (obliterated "
                "serial number), the Voodoo Innovations rifle, and body "
                "armor. " + src_ref("indictment3", "para. 13")
            ),
        },
        {
            "label": "act-tiktok-campaign",
            "name": "Perry TikTok posting campaign: treason, war, 'shoot to kill', 'going hunting' (2022-09-12 to 2022-10-03)",
            "performer": perry,
            "start": "2022-09-12",
            "results": [tiktok_war, tiktok_hunting],
            "desc": (
                "Series of TikTok videos: Border Patrol 'committing treason' "
                "with penalty 'death' (09-12); 'ready to go to war against "
                "this government' (09-13); 'we're out to shoot to kill' "
                "(09-22); 'going hunting! IYKYK!!' departure announcement "
                "(10-02); 'full kits' departure video (10-03). "
                + src_ref("indictment3", "paras. 17-18, 20, 30-31")
            ),
        },
        {
            "label": "act-recruit-individual1",
            "name": "Perry recruits Individual #1 (Louisiana) via TikTok (2022-09-21/23)",
            "performer": perry,
            "start": "2022-09-21",
            "objects": [individuals["1"]],
            "desc": src_ref("indictment3", "paras. 19, 21"),
        },
        {
            "label": "act-recruit-individual2",
            "name": "O'Dell recruits Individual #2 (Missouri) via TikTok (2022-09-25)",
            "performer": odell,
            "start": "2022-09-25",
            "objects": [individuals["2"]],
            "desc": (
                "O'Dell posted a border-security TikTok video wearing a 2nd "
                "American Militia patch, stated in comments they were leaving "
                "for Texas on 2022-10-04, and asked Individual #2 how long "
                "he/she could 'come and train'. "
                + src_ref("indictment3", "paras. 22-23")
            ),
        },
        {
            "label": "act-life-insurance-call",
            "name": "Perry initiates telephone call to Fidelity Life insurance (2022-09-29)",
            "performer": perry,
            "start": "2022-09-29",
            "desc": src_ref("indictment3", "para. 24"),
        },
        {
            "label": "act-armory-visit",
            "name": "Perry travels to a firearms armory business in Warsaw (2022-09-30)",
            "performer": perry,
            "start": "2022-09-30",
            "desc": src_ref("indictment3", "para. 25"),
        },
        {
            "label": "act-gunsmithing",
            "name": "O'Dell transports a firearm for gunsmithing work (late September 2022)",
            "performer": odell,
            "desc": (
                "O'Dell transported a firearm to a gunsmithing business in "
                "Warsaw, Missouri; in the same period he purchased ammunition "
                "from a Warsaw store. " + src_ref("indictment3", "paras. 26-27")
            ),
        },
        {
            "label": "act-supply-calls-individual3",
            "name": "O'Dell phone calls with Individual #3: radios, night vision, recruitment (2022-10-02/04/06)",
            "performer": odell,
            "start": "2022-10-02",
            "objects": [individuals["3"]],
            "desc": (
                "O'Dell asked Individual #3 to acquire ham radios and night "
                "vision goggles for the border trip, attempted to recruit "
                "him/her, and said they could acquire night vision goggles "
                "from murdered federal law enforcement officers. "
                + src_ref("indictment3", "paras. 29, 33, 36")
            ),
        },
        {
            "label": "act-war-calls-individual4",
            "name": "Perry phone calls with Individual #4: plan to 'start a war' at Eagle Pass (2022-10-03/04/06)",
            "performer": perry,
            "start": "2022-10-03",
            "objects": [individuals["4"]],
            "desc": (
                "Perry stated they would go to Eagle Pass, Texas to 'start a "
                "war', shoot people crossing the border and federal agents "
                "who opposed them, and 'take a couple of 'em out' to acquire "
                "gear; on 10-06 he confirmed departure for 2022-10-08. "
                + src_ref("indictment3", "paras. 32, 34, 38")
            ),
        },
        {
            "label": "act-target-practice",
            "name": "Perry and O'Dell practice shooting at targets (2022-10-05 and other dates)",
            "performer": perry,
            "also": [odell],
            "start": "2022-10-05",
            "objects": [rifle],
            "desc": (
                "Shooting practice on land controlled by a family member of "
                "O'Dell. " + src_ref("indictment3", "para. 35")
            ),
        },
        {
            "label": "act-amass-arsenal",
            "name": "Defendants amass firearms, ammunition, and paramilitary gear at O'Dell's residence (by 2022-10-07)",
            "performer": perry,
            "also": [odell],
            "start": "2022-10-07",
            "objects": [rifle, ruger, body_armor],
            "desc": (
                "Approximately six firearms, ~23 loaded magazines, ~1,770 "
                "rounds of ammunition, two sets of body armor with plate "
                "carriers, a handheld radio, two sniper rests, two gas masks, "
                "two apparent ballistic helmets, and multiple containers of a "
                "binary explosive mixture. " + src_ref("indictment3", "para. 39")
            ),
        },
        {
            "label": "act-odell-false-statement",
            "name": "O'Dell makes a false statement to an FBI Special Agent about a firearm (2022-10-07)",
            "performer": odell,
            "start": "2022-10-07",
            "desc": (
                "During the warrant execution O'Dell falsely denied the "
                "presence and his possession of a firearm in an attempt to "
                "conceal it; basis of Count 44. "
                + src_ref("indictment3", "paras. 42, 79")
            ),
        },
    ]
    conspiracy_charge = uid("charge-count1")
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
    graph.append(rel(uid("act-odell-false-statement"), uid("charge-count44"), "Basis_Of"))

    # ------------------------------------------------------------------
    # Search warrant execution, shooting, and arrests (2022-10-07)
    # ------------------------------------------------------------------
    warrant = uid("authorization-search-warrant")
    search_action = uid("action-search-warrant-execution")
    shooting = uid("action-perry-shooting")
    arrest = uid("action-arrests")
    graph.extend(
        [
            {
                "@id": warrant,
                "@type": "case-investigation:Authorization",
                "uco-core:name": "Federal search warrant for O'Dell's residence, Warsaw, Missouri",
                "uco-core:description": (
                    "Federal search warrant issued for O'Dell's residence in "
                    "Warsaw, Missouri, executed by FBI Special Agents on "
                    "2022-10-07. " + src_ref("indictment3", "para. 40")
                ),
            },
            {
                "@id": search_action,
                "@type": "case-investigation:InvestigativeAction",
                "uco-core:name": "Execution of federal search warrant at O'Dell residence (2022-10-07)",
                "uco-core:description": (
                    "FBI Special Agents executed a federal search warrant at "
                    "O'Dell's residence, where the defendants had amassed "
                    "approximately six firearms, ~23 loaded magazines, ~1,770 "
                    "rounds of ammunition, two sets of body armor with plate "
                    "carriers, a handheld radio, two sniper rests, two gas "
                    "masks, two apparent ballistic helmets, and containers of "
                    "a binary explosive mixture. "
                    + src_ref("indictment3", "paras. 39-40")
                ),
                "uco-action:startTime": lit("xsd:dateTime", central_midnight("2022-10-07")),
                "uco-action:performer": {"@id": fbi},
                "case-investigation:relevantAuthorization": [{"@id": warrant}],
            },
            {
                "@id": shooting,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Perry fires ~11 rifle shots at FBI Special Agents (2022-10-07)",
                "uco-core:description": (
                    "During the warrant execution Perry donned his body armor "
                    "and used and discharged the Voodoo Innovations rifle to "
                    "fire approximately 11 shots at FBI Special Agents; "
                    "several rounds hit the armored FBI Bearcat, one narrowly "
                    "missing an agent's head. "
                    + src_ref("indictment3", "para. 40") + "; "
                    + src_ref("sentencing_memo", "background, p. 10")
                ),
                "uco-action:startTime": lit("xsd:dateTime", central_midnight("2022-10-07")),
                "uco-action:performer": {"@id": perry},
                "uco-action:instrument": [{"@id": rifle}],
                "uco-action:object": [{"@id": bearcat}],
            },
            {
                "@id": arrest,
                "@type": "case-investigation:InvestigativeAction",
                "uco-core:name": "Arrests of Perry and O'Dell (2022-10-07)",
                "uco-core:description": (
                    "Arrest warrants for both defendants returned executed on "
                    "2022-10-07. Perry resisted arrest from three Special "
                    "Agents and assaulted at least one agent. "
                    + src_ref("docket", "D.E. 2, 4") + "; "
                    + src_ref("indictment3", "para. 41")
                ),
                "uco-action:startTime": lit("xsd:dateTime", central_midnight("2022-10-07")),
                "uco-action:performer": {"@id": fbi},
                "uco-action:object": [{"@id": perry}, {"@id": odell}],
            },
        ]
    )
    graph.append(rel(shooting, search_action, "Occurred_During"))
    for initials in ATTEMPTED_MURDER_VICTIMS:
        graph.append(rel(victim_ids[initials], shooting, "Victim_Of"))

    # ------------------------------------------------------------------
    # Charging instruments (complaint through third superseding indictment)
    # ------------------------------------------------------------------
    instruments = [
        ("instrument-complaint", "complaint", "Criminal complaint (D.E. 1)", "2022-10-07",
         "Charged Perry with communicating a threat, felon in possession, and "
         "assault of an FBI Special Agent with a deadly or dangerous weapon."),
        ("instrument-indictment", "indictment", "Indictment (D.E. 16)", "2022-10-18",
         "Grand jury charged both defendants with firearms and threat crimes."),
        ("instrument-superseding1", "superseding-indictment", "Superseding Indictment (D.E. 28)", "2023-01-17",
         "Added a forfeiture allegation to the original charges."),
        ("instrument-superseding2", "superseding-indictment", "Second Superseding Indictment (D.E. 34)", "2023-05-30",
         "Added the conspiracy, attempted murder, assault, § 924(c), and "
         "depredation charges."),
        ("instrument-superseding3", "superseding-indictment", "Third Superseding Indictment (Doc 48)", "2023-10-24",
         "Operative 45-count charging instrument; added the escape-from-"
         "custody charge against O'Dell."),
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
    indictment3 = uid("instrument-superseding3")
    graph.append(rel(indictment3, doc_ids["indictment3"], "Derived_From"))

    # ------------------------------------------------------------------
    # Charges
    # ------------------------------------------------------------------
    for charge in CHARGES:
        node = {
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
            "legalproc:assertedIn": [{"@id": indictment3}],
        }
        graph.append(node)

    # Inchoate/derivative offense links: the § 924(c) counts are charged in
    # furtherance of the attempted-murder and deadly-weapon-assault counts.
    graph.append(
        {
            "@id": uid("charge-counts21-34"),
            "legalproc:objectOffense": [
                {"@id": uid("charge-counts4-10")},
                {"@id": uid("charge-counts11-17")},
            ],
        }
    )

    # Defendant-to-charge edges.
    for label in PERRY_CHARGE_LABELS:
        graph.append(rel(perry, uid(label), "Charged_With"))
    for label in ODELL_CHARGE_LABELS:
        graph.append(rel(odell, uid(label), "Charged_With"))

    # Victim-to-charge edges.
    for initials in ATTEMPTED_MURDER_VICTIMS:
        graph.append(rel(victim_ids[initials], uid("charge-counts4-10"), "Victim_Of"))
        graph.append(rel(victim_ids[initials], uid("charge-counts11-17"), "Victim_Of"))
    graph.append(rel(victim_ids["J.R."], uid("charge-count18"), "Victim_Of"))
    graph.append(rel(victim_ids["J.A."], uid("charge-counts19-20"), "Victim_Of"))
    graph.append(rel(victim_ids["R.G."], uid("charge-counts19-20"), "Victim_Of"))

    # Instrumentality edges.
    graph.append(rel(rifle, uid("charge-counts21-34"), "Instrument_Of"))
    graph.append(rel(rifle, uid("charge-counts36-37"), "Subject_Of"))
    graph.append(rel(ruger, uid("charge-counts36-37"), "Subject_Of"))
    graph.append(rel(ruger, uid("charge-count38"), "Subject_Of"))
    graph.append(rel(stevens, uid("charge-count42"), "Subject_Of"))
    graph.append(rel(body_armor, uid("charge-count39"), "Subject_Of"))
    graph.append(rel(bearcat, uid("charge-count35"), "Subject_Of"))

    # ------------------------------------------------------------------
    # Proceedings, plea, verdicts
    # ------------------------------------------------------------------
    trial = uid("proceeding-jury-trial")
    plea_hearing = uid("proceeding-plea-hearing-odell")
    sentencing_perry = uid("proceeding-sentencing-perry")
    sentencing_odell = uid("proceeding-sentencing-odell")
    appeal = uid("proceeding-appeal")
    graph.extend(
        [
            {
                "@id": trial,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Nine-day jury trial (2024-10-28 to 2024-11-07)",
                "uco-core:description": (
                    "Jury trial before Chief District Judge Brian C. Wimes "
                    "with testimony from over 40 witnesses and admission of "
                    "over 400 exhibits. "
                    + src_ref("sentencing_memo", "background, pp. 4-5")
                ),
                "legalproc:proceedingType": "trial",
            },
            {
                "@id": plea_hearing,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "O'Dell change-of-plea hearing (2024-10-28)",
                "uco-core:description": (
                    "On the first day of trial O'Dell pleaded guilty to "
                    "Counts 42, 44, and 45 of the Third Superseding "
                    "Indictment. " + src_ref("docket", "D.E. 134, 137")
                ),
                "legalproc:proceedingType": "plea-hearing",
            },
            {
                "@id": sentencing_perry,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Sentencing hearing for Perry (2025-08-27)",
                "uco-core:description": src_ref("docket", "D.E. 231 minute entry"),
                "legalproc:proceedingType": "sentencing-hearing",
            },
            {
                "@id": sentencing_odell,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Sentencing hearing for O'Dell (2025-08-27)",
                "uco-core:description": src_ref("docket", "D.E. 233 minute entry"),
                "legalproc:proceedingType": "sentencing-hearing",
            },
            {
                "@id": appeal,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": f"Appeal {APPEAL_DOCKET}",
                "uco-core:description": (
                    "Both defendants filed notices of appeal on 2025-09-05 "
                    "from the 2025-08-27 judgments; docketed in the Eighth "
                    "Circuit Court of Appeals. "
                    + src_ref("docket", "D.E. 238, 241, 245")
                ),
                "legalproc:proceedingType": "appeal",
            },
        ]
    )
    for proceeding in (trial, plea_hearing, sentencing_perry, sentencing_odell, appeal):
        graph.append(rel(proceeding, investigation, "part_of"))

    plea_odell = uid("plea-odell")
    graph.append(
        {
            "@id": plea_odell,
            "@type": ["legalproc:Plea", "uco-core:UcoObject"],
            "uco-core:name": "O'Dell guilty plea to Counts 42, 44, and 45 (2024-10-28)",
            "uco-core:description": src_ref("docket", "D.E. 134, 137") + "; "
            + src_ref("sentencing_memo", "background, p. 4"),
            "legalproc:pleaType": "guilty",
            "legalproc:concernsCharge": [
                {"@id": uid("charge-count42")},
                {"@id": uid("charge-count44")},
                {"@id": uid("charge-count45")},
            ],
        }
    )
    graph.append(rel(plea_odell, odell, "Relates_To"))
    graph.append(rel(plea_odell, plea_hearing, "Occurred_During"))

    verdict_perry = uid("verdict-perry")
    verdict_perry_acquittal = uid("verdict-perry-count40")
    verdict_odell = uid("verdict-odell")
    graph.extend(
        [
            {
                "@id": verdict_perry,
                "@type": ["legalproc:Verdict", "uco-core:UcoObject"],
                "uco-core:name": "Jury verdict: Perry guilty on Counts 1-37, 39, and 41 (2024-11-07)",
                "uco-core:description": src_ref("docket", "D.E. 148"),
                "legalproc:verdictType": "guilty",
                "legalproc:concernsCharge": [
                    {"@id": uid(lbl)} for lbl in PERRY_CHARGE_LABELS
                    if lbl not in ("charge-count38", "charge-count40")
                ],
            },
            {
                "@id": verdict_perry_acquittal,
                "@type": ["legalproc:Verdict", "uco-core:UcoObject"],
                "uco-core:name": "Jury verdict: Perry not guilty on Count 40 (2024-11-07)",
                "uco-core:description": src_ref("docket", "D.E. 148"),
                "legalproc:verdictType": "not-guilty",
                "legalproc:concernsCharge": [{"@id": uid("charge-count40")}],
            },
            {
                "@id": verdict_odell,
                "@type": ["legalproc:Verdict", "uco-core:UcoObject"],
                "uco-core:name": "Jury verdict: O'Dell guilty on Counts 1-35 and 43 (2024-11-07)",
                "uco-core:description": src_ref("docket", "D.E. 149"),
                "legalproc:verdictType": "guilty",
                "legalproc:concernsCharge": [
                    {"@id": uid(lbl)} for lbl in ODELL_CHARGE_LABELS
                    if lbl not in ("charge-count42", "charge-count44", "charge-count45")
                ],
            },
        ]
    )
    graph.append(rel(verdict_perry, perry, "Relates_To"))
    graph.append(rel(verdict_perry_acquittal, perry, "Relates_To"))
    graph.append(rel(verdict_odell, odell, "Relates_To"))
    for verdict in (verdict_perry, verdict_perry_acquittal, verdict_odell):
        graph.append(rel(verdict, trial, "Occurred_During"))

    # ------------------------------------------------------------------
    # Sentences (government recommendation and imposed judgments)
    # ------------------------------------------------------------------
    sentence_rec = uid("sentence-recommended-perry")
    sentence_perry = uid("sentence-imposed-perry")
    sentence_odell = uid("sentence-imposed-odell")
    graph.extend(
        [
            {
                "@id": sentence_rec,
                "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
                "uco-core:name": "Government sentencing recommendation for Perry",
                "uco-core:description": (
                    "The United States recommended consecutive life sentences "
                    "for the conspiracy-to-murder conviction and the § 924(c) "
                    "convictions, consecutive statutory maximums for each "
                    "attempted-murder and assault conviction, and restitution "
                    "of $3,717.98 to the FBI, joint and several with O'Dell. "
                    "PSR: total offense level 43 (calculated 60), criminal "
                    "history category VI via the federal-crime-of-terrorism "
                    "enhancement (U.S.S.G. §3A1.4); Guidelines range life. "
                    + src_ref("sentencing_memo", "pp. 2-3, 7")
                ),
                "legalproc:sentenceStatus": "recommended",
                "legalproc:sentenceTerm": "consecutive lifetime terms of imprisonment",
                "legalproc:concernsCharge": [
                    {"@id": uid("charge-count1")},
                    {"@id": uid("charge-counts21-34")},
                ],
            },
            {
                "@id": sentence_perry,
                "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
                "uco-core:name": "Sentence imposed on Perry (2025-08-27)",
                "uco-core:description": (
                    "Life on Count 1; concurrent terms of 5-20 years on the "
                    "remaining concurrent counts; and Life on each of Counts "
                    "21-34, consecutive to each other and to all other "
                    "counts, for a total term of Life. Supervised release 5 "
                    "years; special assessment $3,800; no fine; restitution "
                    "$3,717.98. " + src_ref("docket", "defendant 1 dispositions")
                ),
                "legalproc:sentenceStatus": "imposed",
                "legalproc:sentenceTerm": (
                    "Life (Count 1) plus fourteen consecutive Life terms (Counts 21-34)"
                ),
                "legalproc:concernsCharge": [
                    {"@id": uid(lbl)} for lbl in PERRY_CHARGE_LABELS
                    if lbl not in ("charge-count38", "charge-count40")
                ],
            },
            {
                "@id": sentence_odell,
                "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
                "uco-core:name": "Sentence imposed on O'Dell (2025-08-27)",
                "uco-core:description": (
                    "25 years on Count 1 and concurrent terms on the other "
                    "concurrent counts; 10 years on each of Counts 21-34, "
                    "consecutive to each other (140 years) and to all other "
                    "counts, for a total term of imprisonment of 165 years. "
                    "Supervised release totals 5 years. "
                    + src_ref("docket", "D.E. 233 minute entry")
                ),
                "legalproc:sentenceStatus": "imposed",
                "legalproc:sentenceTerm": "165 years (25 concurrent + 140 consecutive)",
                "legalproc:concernsCharge": [
                    {"@id": uid(lbl)} for lbl in ODELL_CHARGE_LABELS
                ],
            },
        ]
    )
    graph.append(rel(sentence_rec, doc_ids["sentencing_memo"], "Derived_From"))
    graph.append(rel(sentence_rec, perry, "Relates_To"))
    graph.append(rel(sentence_perry, perry, "Relates_To"))
    graph.append(rel(sentence_odell, odell, "Relates_To"))
    graph.append(rel(sentence_perry, sentencing_perry, "Occurred_During"))
    graph.append(rel(sentence_odell, sentencing_odell, "Occurred_During"))

    # ------------------------------------------------------------------
    # Forfeiture and restitution
    # ------------------------------------------------------------------
    forfeiture = uid("forfeiture-order")
    graph.append(
        {
            "@id": forfeiture,
            "@type": ["legalproc:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Forfeiture allegation and preliminary order of forfeiture (Perry)",
            "uco-core:description": (
                "Terrorism forfeiture (18 U.S.C. § 981(a)(1)(G), 28 U.S.C. "
                "§ 2461(c)) of assets derived from or used to commit a "
                "federal crime of terrorism — including the Armored Republic "
                "body armor, a Polymer80 PF940V4 9mm privately made pistol, "
                "a 7.62x39mm Cerro Forge privately made rifle, a lower "
                "receiver, and various ammunition — plus firearms forfeiture "
                "(18 U.S.C. § 924(d)) of the Ruger Security-9, the Voodoo "
                "Innovations rifle, and the Stevens model 320. Perry waived "
                "forfeiture by jury; the Court entered a preliminary order "
                "of forfeiture (D.E. 192). "
                + src_ref("indictment3", "forfeiture allegation paras. 81-85")
                + "; " + src_ref("sentencing_memo", "background, p. 5")
            ),
            "legalproc:concernsCharge": [
                {"@id": uid("charge-count1")},
                {"@id": uid("charge-counts4-10")},
                {"@id": uid("charge-counts21-34")},
                {"@id": uid("charge-count35")},
                {"@id": uid("charge-counts36-37")},
                {"@id": uid("charge-count42")},
            ],
        }
    )
    for item in (rifle, ruger, stevens, body_armor):
        graph.append(rel(forfeiture, item, "Forfeits"))
    graph.append(rel(forfeiture, doc_ids["indictment3"], "Derived_From"))

    restitution = uid("restitution-order")
    graph.append(
        {
            "@id": restitution,
            "@type": ["legalproc:RestitutionOrder", "uco-core:UcoObject"],
            "uco-core:name": "Restitution of $3,717.98 to the FBI (joint and several)",
            "uco-core:description": (
                "Restitution to the FBI for the damage Perry caused to the "
                "FBI Bearcat armored vehicle during the attempted murders, "
                "joint and several with O'Dell; ordered as part of the "
                "2025-08-27 judgments. "
                + src_ref("sentencing_memo", "restitution section") + "; "
                + src_ref("docket", "defendant 1 dispositions")
            ),
            "legalproc:monetaryAmount": lit("xsd:decimal", "3717.98"),
            "legalproc:currencyCode": "USD",
            "legalproc:concernsCharge": [{"@id": uid("charge-count35")}],
        }
    )
    graph.append(rel(restitution, fbi, "Relates_To"))
    graph.append(rel(restitution, bearcat, "Relates_To"))

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
