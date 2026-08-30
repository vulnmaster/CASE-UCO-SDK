#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Grayson et al. (W.D. Tenn. murder-for-hire).

Case 2:23-cr-20121-TLP (W.D. Tenn., Memphis): Ashley Grayson, who ran an
internet-based business and gained notoriety online, offered a Memphis
couple at least $20,000 per killing to murder three people — a Southaven,
Mississippi woman she blamed for fake online profiles criticizing her, her
former boyfriend, and a Texas woman who had made negative social media
posts about her. On 2022-09-10 the Memphis woman video-recorded a call in
which Grayson confirmed she wanted the Southaven woman killed as soon as
possible and offered an extra $5,000 to do it within a week. The couple
later staged a failed "attempt" with a photo of police lights from an
unrelated Memphis incident and collected $10,000 from the Graysons in
Dallas. A jury convicted Ashley Grayson on the single 18 U.S.C. § 1958
count and acquitted her husband Joshua; she was sentenced to the 120-month
statutory maximum. The Sixth Circuit affirmed (24-5988) and the Supreme
Court granted certiorari (25-851, writ issued 2026-06-24).

Sources:
  - PACER criminal docket, 2:23-cr-20121-TLP (retrieved 2026-06-27)
  - USAO W.D. Tenn. press release, "Texas Woman Sentenced to 10 Years of
    Imprisonment in Connection with Murder-for-Hire Plot" (2024-11-18)

MCP extraction artifacts: examples/pacer/wdtn_2023_cr_20121/mcp_outputs/*

Extensions exercised:
  - extensions/legalproc — one § 1958 count charged against two defendants
    with divergent outcomes (per-defendant CriminalCharge nodes: jury
    conviction vs. jury acquittal), trial and sentencing proceedings,
    appellate and certiorari proceedings, imposed sentence.

Source-fidelity conventions:
  - Court dates are date-only facts rendered at local midnight Central time
    with the correct seasonal UTC offset.
  - The three intended victims are identified only by role (the press
    release names no victims); the judgment's no-contact initials
    D.H., S.H., and P.T. are recorded verbatim without asserting which
    initials map to which victim.
  - The Memphis couple are cooperating private parties, not law
    enforcement; nothing in the reviewed documents states when they began
    cooperating with the FBI, so no cooperation start date is asserted.
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

CASE_ID = "grayson-wdtn-2023-murder-for-hire"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "grayson-wdtn-2023-murder-for-hire.jsonld"

PACER_DOCKET = "2:23-cr-20121-TLP"
USCA_CASE = "24-5988"
SCOTUS_CASE = "25-851"
LOCAL_REF = "uploads/murder_for_hire"

SOURCE_DOCS = {
    "docket": {
        "file_name": "pacer -- murder for hire -- docket.pdf",
        "sha256": "30a244c6566c8162360672f4ca5de1019096f75c565e71e65408e48dee84f8fa",
        "detail": "PACER criminal docket report retrieved 2026-06-27",
    },
    "press": {
        "file_name": "pacer -- murder for hire -- press release.pdf",
        "sha256": "d1f9b0d329f9a5ed379c9f6cb98ce57bf9466d4199935df1bd99518d8c1907a4",
        "detail": "USAO W.D. Tenn. press release dated 2024-11-18",
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

    W.D. Tenn. (Memphis): CDT (-05:00) roughly March-November, CST
    (-06:00) otherwise. Month-level approximation is sufficient for
    filing dates.
    """
    month = int(date_str.split("-")[1])
    offset = "-05:00" if 4 <= month <= 10 else "-06:00"
    return f"{date_str}T00:00:00{offset}"


def src_ref(doc_key: str, detail: str) -> str:
    label = {"docket": "PACER docket", "press": "USAO press release"}[doc_key]
    return f"Source: {label}, {detail}"


def source_observable(label: str, meta: dict) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": meta["file_name"],
        "uco-core:description": (
            f"{meta['detail']}; case {PACER_DOCKET} (W.D. Tenn.); "
            f"local bundle '{LOCAL_REF}'."
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
            "uco-core:name": "U.S. v. Grayson et al. (W.D. Tenn. murder-for-hire)",
            "uco-core:description": (
                "Federal murder-for-hire prosecution in the Western "
                "District of Tennessee (Memphis). Ashley Grayson, an "
                "internet-based business owner, offered a Memphis couple "
                "at least $20,000 per killing to murder three people over "
                "online feuds, confirmed the first target in a "
                "video-recorded call on 2022-09-10, and paid $10,000 for "
                "a staged failed 'attempt'. A jury convicted Ashley "
                "Grayson on the single 18 U.S.C. § 1958 count on "
                "2024-03-29 and acquitted her husband Joshua Grayson. "
                "Sentenced 2024-10-31 to 120 months (statutory maximum) "
                "plus 3 years of supervised release by Judge Thomas L. "
                "Parker. Sixth Circuit affirmed 2025-08-14 (No. "
                f"{USCA_CASE}); the Supreme Court granted certiorari, "
                f"writ issued 2026-06-24 (No. {SCOTUS_CASE}). "
                "Investigated by the FBI and ATF."
            ),
            "uco-core:tag": [
                "murder-for-hire", "solicitation", "interstate-facility",
                "violent-crime", "online-feud",
            ],
            "legalproc:caseIdentifier": PACER_DOCKET,
        }
    )
    for key in doc_ids:
        graph.append(rel(doc_ids[key], investigation, "part_of"))

    # ------------------------------------------------------------------
    # People
    # ------------------------------------------------------------------
    ashley = uid("person-ashley-grayson")
    joshua = uid("person-joshua-grayson")
    memphis_woman = uid("person-memphis-woman")
    memphis_husband = uid("person-memphis-husband")
    southaven_woman = uid("person-southaven-woman")
    ex_boyfriend = uid("person-ex-boyfriend")
    texas_woman = uid("person-texas-woman")
    judge_mccalla = uid("person-judge-mccalla")
    judge_parker = uid("person-judge-parker")
    agent_hosafros = uid("person-agent-hosafros")

    graph.extend(
        [
            person(
                "person-ashley-grayson", "Ashley Grayson",
                "Defendant 1 (USM 67352-510), 35, of Dallas, Texas. Ran an "
                "internet-based business and gained notoriety from her "
                "online presence. Offered to pay a Memphis couple to kill "
                "three people, each killing valued at $20,000 or more; "
                "confirmed the Southaven target in a video-recorded call "
                "and paid $10,000 for a staged failed attempt. Convicted "
                "by a jury on 2024-03-29 and sentenced to 120 months, the "
                "statutory maximum for 18 U.S.C. § 1958. "
                + src_ref("press", "paras. 1-6") + "; "
                + src_ref("docket", "Defendant (1); minute entries 127, 211"),
            ),
            person(
                "person-joshua-grayson", "Joshua Grayson",
                "Defendant 2, husband of Ashley Grayson. Present at the "
                "September 2022 Dallas meeting where the killings were "
                "solicited and at the later Dallas meeting where the "
                "$10,000 was paid. Acquitted by the jury on 2024-03-29 "
                "and discharged by judgment of acquittal on 2024-04-04. "
                + src_ref("press", "paras. 3-5") + "; "
                + src_ref("docket", "Defendant (2); D.E. 134"),
            ),
            person(
                "person-memphis-woman", "Memphis woman (cooperating witness)",
                "Memphis woman who had worked with Ashley Grayson in the "
                "past. Asked in August 2022 to fly to Dallas for a "
                "'business opportunity'; solicited with her husband to "
                "commit three killings. Video-recorded a 2022-09-10 call "
                "in which Grayson confirmed she wanted the Southaven "
                "woman killed as soon as possible. With her husband, "
                "staged a failed attempt and collected $10,000. Identity "
                "not stated in the reviewed documents. "
                + src_ref("press", "paras. 3-5"),
            ),
            person(
                "person-memphis-husband", "Memphis woman's husband (cooperating witness)",
                "Husband of the Memphis woman; traveled with her to the "
                "Dallas meetings, participated in the staged failed "
                "attempt, and shared in the $10,000 payment. Identity not "
                "stated in the reviewed documents. "
                + src_ref("press", "paras. 3-5"),
            ),
            person(
                "person-southaven-woman", "Southaven, Mississippi woman (intended victim)",
                "Operated an online business similar to Ashley Grayson's. "
                "After a 2021 falling out, Grayson suspected her of "
                "creating fake online profiles that criticized Grayson "
                "and her business; the pair never met in person. Primary "
                "target of the murder-for-hire plot — Grayson wanted her "
                "killed as soon as possible and offered an extra $5,000 "
                "for the murder to be carried out within a week. "
                + src_ref("press", "paras. 2-4"),
            ),
            person(
                "person-ex-boyfriend", "Ashley Grayson's former boyfriend (intended victim)",
                "Second person Ashley Grayson offered to pay the Memphis "
                "couple to kill, at a value of at least $20,000. Identity "
                "not stated in the reviewed documents. "
                + src_ref("press", "para. 3"),
            ),
            person(
                "person-texas-woman", "Texas woman (intended victim)",
                "Third person Ashley Grayson offered to pay the Memphis "
                "couple to kill; she had recently made negative social "
                "media posts about Grayson. Identity not stated in the "
                "reviewed documents. " + src_ref("press", "para. 3"),
            ),
            person(
                "person-judge-mccalla", "Jon Phipps McCalla",
                "U.S. District Judge who presided over pretrial "
                "proceedings and the March 2024 jury trial, and entered "
                "Joshua Grayson's judgment of acquittal. "
                + src_ref("docket", "minute entries 114-127; D.E. 134"),
            ),
            person(
                "person-judge-parker", "Thomas L. Parker",
                "U.S. District Judge assigned 2024-07-31; imposed Ashley "
                "Grayson's sentence on 2024-10-31 and entered judgment. "
                + src_ref("docket", "judge update 2024-07-31; D.E. 211, 213"),
            ),
            person(
                "person-judge-pham", "Tu M. Pham",
                "Chief Magistrate Judge who conducted the 2023-07-07 "
                "initial appearance, set $10,000 unsecured bonds, and "
                "arraigned the defendants. "
                + src_ref("docket", "minute entries 7, 28"),
            ),
            person(
                "person-agent-hosafros", "Janelle Hosafros",
                "FBI case agent who sat with the government at trial and "
                "testified in its case-in-chief. "
                + src_ref("docket", "minute entries 114, 121, 126"),
            ),
        ]
    )

    # ------------------------------------------------------------------
    # Organizations
    # ------------------------------------------------------------------
    usao = uid("org-usao-wdtn")
    fbi = uid("org-fbi")
    atf = uid("org-atf")
    ashley_biz = uid("org-ashley-business")
    southaven_biz = uid("org-southaven-business")
    graph.extend(
        [
            {
                "@id": usao,
                "@type": "uco-identity:Organization",
                "uco-core:name": "U.S. Attorney's Office, Western District of Tennessee",
                "uco-core:description": (
                    "Prosecuting office. Acting U.S. Attorney Reagan "
                    "Fondren announced the sentence; AUSAs Neal Oldham "
                    "and Bryce Phillips prosecuted the case. "
                    + src_ref("press", "paras. 1, 8-9")
                ),
            },
            {
                "@id": fbi,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Federal Bureau of Investigation",
                "uco-core:description": (
                    "Investigating agency (Nashville Field Office, "
                    "Memphis Resident Agency; Special Agent in Charge "
                    "Joe Carrico). " + src_ref("press", "paras. 7-8")
                ),
            },
            {
                "@id": atf,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Bureau of Alcohol, Tobacco, Firearms and Explosives",
                "uco-core:description": (
                    "Co-investigating agency. " + src_ref("press", "para. 8")
                ),
            },
            {
                "@id": ashley_biz,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Ashley Grayson's internet-based business",
                "uco-core:description": (
                    "Internet-based business run by Ashley Grayson, from "
                    "which she gained notoriety online; name not stated "
                    "in the reviewed documents. "
                    + src_ref("press", "para. 2")
                ),
            },
            {
                "@id": southaven_biz,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Southaven woman's online business",
                "uco-core:description": (
                    "Online business similar to Ashley Grayson's, "
                    "operated by the Southaven, Mississippi woman; name "
                    "not stated in the reviewed documents. "
                    + src_ref("press", "para. 2")
                ),
            },
        ]
    )
    graph.append(rel(ashley, ashley_biz, "Operates"))
    graph.append(rel(southaven_woman, southaven_biz, "Operates"))
    graph.append(rel(ashley, joshua, "Married_To", directional=False))
    graph.append(rel(memphis_woman, memphis_husband, "Married_To", directional=False))

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------
    dallas = uid("loc-dallas")
    memphis = uid("loc-memphis")
    graph.extend(
        [
            location(
                "loc-dallas", "Dallas, Texas",
                "Ashley Grayson's home city; site of the early September "
                "2022 solicitation meeting and the later meeting where "
                "the Memphis couple received $10,000.",
            ),
            location(
                "loc-memphis", "Memphis, Tennessee",
                "Home of the cooperating couple, source of the unrelated "
                "police-lights photo used to stage the failed attempt, "
                "and venue of the prosecution (W.D. Tenn.).",
            ),
            location(
                "loc-southaven", "Southaven, Mississippi",
                "Home of the primary intended victim, who would have "
                "died had the plot succeeded.",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # Cyber observables — the interstate-facility evidence at the heart
    # of the § 1958 charge.
    # ------------------------------------------------------------------
    fake_profiles = uid("obs-fake-profiles")
    negative_posts = uid("obs-negative-posts")
    recorded_call = uid("obs-recorded-call")
    lights_photo = uid("obs-police-lights-photo")
    extraction = uid("obs-iphone-extraction")
    graph.extend(
        [
            {
                "@id": fake_profiles,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Fake online profiles criticizing Ashley Grayson and her business",
                "uco-core:description": (
                    "Fake online profiles that criticized Grayson and her "
                    "business. Grayson suspected the Southaven woman of "
                    "creating them after their 2021 falling out — the "
                    "grievance behind the plot. Attribution is Grayson's "
                    "suspicion as reported, not an established fact. "
                    + src_ref("press", "para. 2")
                ),
                "uco-core:tag": ["motive", "online-content"],
            },
            {
                "@id": negative_posts,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Negative social media posts about Ashley Grayson by the Texas woman",
                "uco-core:description": (
                    "Recent negative social media posts about Grayson "
                    "that made the Texas woman the third target of the "
                    "solicitation. " + src_ref("press", "para. 3")
                ),
                "uco-core:tag": ["motive", "online-content"],
            },
            {
                "@id": recorded_call,
                "@type": "uco-observable:Call",
                "uco-core:name": "Video-recorded call of 2022-09-10 confirming the murder-for-hire",
                "uco-core:description": (
                    "Call video-recorded by the Memphis woman on "
                    "2022-09-10 in which Ashley Grayson confirmed that "
                    "she wanted the Southaven woman killed as soon as "
                    "possible and offered an extra $5,000 for the murder "
                    "to be carried out in the next week. A telephone call "
                    "across state lines is a use of an interstate "
                    "facility under 18 U.S.C. § 1958. "
                    + src_ref("press", "para. 4")
                ),
                "uco-observable:startTime": lit(
                    "xsd:dateTime", central_midnight("2022-09-10")
                ),
                "uco-core:tag": ["evidence", "recording", "interstate-facility"],
            },
            {
                "@id": lights_photo,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Photo of police lights from an unrelated Memphis incident",
                "uco-core:description": (
                    "Picture of police lights from an unrelated incident "
                    "in Memphis, sent by the Memphis couple to Ashley "
                    "Grayson under the guise that they had attempted to "
                    "carry out the murder-for-hire but were unsuccessful; "
                    "used to support their demand for $10,000 (half of "
                    "the promised price). " + src_ref("press", "para. 5")
                ),
                "uco-core:tag": ["evidence", "ruse"],
            },
            {
                "@id": extraction,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Trial Exhibit 5: Extraction Report — Apple iPhone",
                "uco-core:description": (
                    "Mobile device extraction report for an Apple iPhone "
                    "admitted as Trial Exhibit 5 and filed on the docket "
                    "by the government on 2025-02-12 (D.E. 231). The "
                    "device's owner is not stated in the docket text. "
                    + src_ref("docket", "D.E. 231")
                ),
                "uco-core:tag": ["evidence", "mobile-extraction"],
            },
        ]
    )
    graph.append(rel(fake_profiles, southaven_woman, "Attributed_To"))
    graph.append(rel(negative_posts, texas_woman, "Authored_By"))
    graph.append(rel(recorded_call, memphis_woman, "Recorded_By"))
    graph.append(rel(lights_photo, ashley, "Sent_To"))
    graph.append(rel(extraction, investigation, "part_of"))

    # ------------------------------------------------------------------
    # The $10,000 payment (physical currency)
    # ------------------------------------------------------------------
    payment = uid("item-10k-payment")
    graph.append(
        {
            "@id": payment,
            "@type": ["uco-core:UcoObject"],
            "uco-core:name": "$10,000 payment for the staged 'attempt'",
            "uco-core:description": (
                "US$10,000 — half of the promised $20,000 price — "
                "demanded by the Memphis couple for the purported failed "
                "attempt and received from Ashley and Joshua Grayson at "
                "a meeting in Dallas. Consideration for the murder-for-"
                "hire under 18 U.S.C. § 1958. "
                + src_ref("press", "para. 5")
            ),
            "uco-core:tag": ["evidence", "payment"],
        }
    )

    # ------------------------------------------------------------------
    # Charging instrument and per-defendant charges. The single § 1958
    # count was charged against both defendants but resolved differently
    # (jury conviction vs. jury acquittal), so each defendant gets a
    # CriminalCharge node carrying their own disposition — mirroring how
    # PACER tracks counts per defendant.
    # ------------------------------------------------------------------
    indictment = uid("charging-instrument")
    graph.append(
        {
            "@id": indictment,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "Indictment (D.E. 1, filed 2023-06-29)",
            "uco-core:description": (
                "One-count grand jury indictment returned in the Western "
                "District of Tennessee charging Ashley Grayson and "
                "Joshua Grayson with Use of Interstate Facility in "
                "Commission of Murder-for-Hire, 18 U.S.C. § 1958. "
                + src_ref("docket", "D.E. 1") + "; "
                + src_ref("press", "para. 6")
            ),
            "legalproc:instrumentType": "indictment",
            "uco-core:objectCreatedTime": lit(
                "xsd:dateTime", central_midnight("2023-06-29")
            ),
        }
    )
    graph.append(rel(indictment, doc_ids["docket"], "Derived_From"))

    charge_ashley = uid("charge-count1-ashley")
    charge_joshua = uid("charge-count1-joshua")
    graph.extend(
        [
            {
                "@id": charge_ashley,
                "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                "uco-core:name": (
                    "Count 1 (as to Ashley Grayson): Use of Interstate "
                    "Facility in Commission of Murder-for-Hire"
                ),
                "uco-core:description": (
                    "Use of a facility of interstate commerce with intent "
                    "that a murder be committed for hire (docket offense "
                    "text: '18:1958 RACKETEERING - MURDER'). Ashley "
                    "Grayson was found guilty by the jury on 2024-03-29 "
                    "and sentenced to 120 months, the statutory maximum. "
                    + src_ref("docket", "Defendant (1) terminated counts") + "; "
                    + src_ref("press", "paras. 6-7")
                ),
                "legalproc:statuteCitation": "18 U.S.C. § 1958",
                "legalproc:countNumber": lit("xsd:nonNegativeInteger", 1),
                "legalproc:countLabel": "Count 1",
                "legalproc:offenseForm": "substantive",
                "legalproc:chargeDisposition": "convicted-at-trial",
                "legalproc:assertedIn": {"@id": indictment},
            },
            {
                "@id": charge_joshua,
                "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                "uco-core:name": (
                    "Count 1 (as to Joshua Grayson): Use of Interstate "
                    "Facility in Commission of Murder-for-Hire"
                ),
                "uco-core:description": (
                    "The same § 1958 count charged against Joshua "
                    "Grayson. The jury returned a not-guilty verdict on "
                    "2024-03-29; judgment of acquittal entered 2024-04-04 "
                    "discharging him and exonerating his bond. "
                    + src_ref("docket", "Defendant (2) pending counts; D.E. 134")
                ),
                "legalproc:statuteCitation": "18 U.S.C. § 1958",
                "legalproc:countNumber": lit("xsd:nonNegativeInteger", 1),
                "legalproc:countLabel": "Count 1",
                "legalproc:offenseForm": "substantive",
                "legalproc:chargeDisposition": "acquitted-at-trial",
                "legalproc:assertedIn": {"@id": indictment},
            },
        ]
    )
    graph.append(rel(ashley, charge_ashley, "Charged_With"))
    graph.append(rel(joshua, charge_joshua, "Charged_With"))
    graph.append(rel(charge_ashley, recorded_call, "Relates_To"))
    graph.append(rel(charge_ashley, payment, "Relates_To"))

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

    act_recruit = action(
        "action-recruit",
        "Invite the Memphis woman to Dallas for a 'business opportunity'",
        "In August 2022, Ashley Grayson asked a Memphis woman with whom "
        "she had worked in the past to fly to Dallas to discuss a "
        "'business opportunity'. " + src_ref("press", "para. 3"),
        performers=[ashley],
        objects=[memphis_woman],
        start=central_midnight("2022-08-01"),
        end=central_midnight("2022-08-31"),
    )
    act_solicit = action(
        "action-solicit-killings",
        "Offer the Memphis couple money to kill three people (Dallas meeting)",
        "In early September 2022, the Memphis woman and her husband met "
        "with Ashley Grayson and her husband in Dallas, where Ashley "
        "Grayson offered to pay the couple to kill three different "
        "people — the Southaven woman, Grayson's former boyfriend, and "
        "a Texas woman who had recently made negative social media "
        "posts about Grayson — each killing valued at $20,000 or more. "
        "Joshua Grayson's presence at the meeting is recorded here; the "
        "jury acquitted him of the § 1958 charge. "
        + src_ref("press", "para. 3"),
        performers=[ashley, joshua],
        objects=[southaven_woman, ex_boyfriend, texas_woman],
        loc=dallas,
        start=central_midnight("2022-09-01"),
        end=central_midnight("2022-09-09"),
    )
    act_confirm = action(
        "action-confirm-call",
        "Confirm the hit on the Southaven woman in a video-recorded call",
        "On 2022-09-10, the Memphis woman video-recorded a call to "
        "Ashley Grayson in which Grayson confirmed that she wanted the "
        "Southaven woman killed as soon as possible and offered an "
        "extra $5,000 for the murder to be carried out in the next "
        "week. " + src_ref("press", "para. 4"),
        performers=[ashley],
        objects=[southaven_woman],
        instruments=[recorded_call],
        start=central_midnight("2022-09-10"),
        end=central_midnight("2022-09-10"),
    )
    act_stage = action(
        "action-stage-attempt",
        "Stage a failed murder attempt with a police-lights photo and demand $10,000",
        "The Memphis couple sent Ashley Grayson a picture of police "
        "lights from an unrelated incident in Memphis under the guise "
        "that they had attempted to carry out the murder-for-hire but "
        "were unsuccessful, and demanded $10,000 — half of the promised "
        "price — for the attempt. " + src_ref("press", "para. 5"),
        performers=[memphis_woman, memphis_husband],
        objects=[ashley],
        instruments=[lights_photo],
        loc=memphis,
    )
    act_pay = action(
        "action-pay-10k",
        "Pay the Memphis couple $10,000 for the staged 'attempt' (Dallas meeting)",
        "The Memphis couple went to Dallas, met with Ashley Grayson and "
        "her husband, and received $10,000 from them for the "
        "'attempt'. " + src_ref("press", "para. 5"),
        performers=[ashley, joshua],
        objects=[payment],
        loc=dallas,
    )
    act_investigate = action(
        "action-investigate",
        "Investigate the murder-for-hire plot",
        "The case was investigated by the Federal Bureau of "
        "Investigation and the Bureau of Alcohol, Tobacco, Firearms and "
        "Explosives; FBI case agent Janelle Hosafros testified at "
        "trial. The proactive response from the investigating agencies "
        "prevented a more serious crime from occurring. "
        + src_ref("press", "paras. 7-8") + "; "
        + src_ref("docket", "minute entries 114-126"),
        performers=[fbi, atf],
        objects=[ashley, joshua],
    )
    for act in (act_recruit, act_solicit, act_confirm, act_stage,
                act_pay, act_investigate):
        graph.append(rel(act, investigation, "part_of"))
    graph.append(rel(act_solicit, charge_ashley, "Relates_To"))
    graph.append(rel(act_confirm, charge_ashley, "Relates_To"))
    graph.append(rel(act_pay, charge_ashley, "Relates_To"))
    graph.append(rel(agent_hosafros, act_investigate, "Participated_In"))
    graph.append(rel(agent_hosafros, fbi, "Member_Of"))

    # ------------------------------------------------------------------
    # Proceedings: trial, verdicts, sentencing, appeal, certiorari
    # ------------------------------------------------------------------
    trial = uid("proceeding-jury-trial")
    graph.append(
        {
            "@id": trial,
            "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
            "uco-core:name": "Jury trial (2024-03-25 through 2024-03-29)",
            "uco-core:description": (
                "Five-day jury trial before Judge Jon Phipps McCalla in "
                "Memphis. Twelve jurors and two alternates sworn "
                "2024-03-26; government witnesses included Jenny Chung, "
                "Olivia Johnson, Leslie Jones, Brandon Thomas, case "
                "agent Janelle Hosafros, and Derricka Harwell, with "
                "Exhibits 1-38; both defendants elected not to testify; "
                "Rule 29 motions denied. "
                + src_ref("docket", "minute entries 114, 116, 121, 126, 127")
            ),
            "legalproc:proceedingType": "jury-trial",
            "uco-core:objectCreatedTime": lit(
                "xsd:dateTime", central_midnight("2024-03-25")
            ),
        }
    )
    graph.append(rel(trial, doc_ids["docket"], "Derived_From"))
    graph.append(rel(trial, judge_mccalla, "Presided_Over_By"))

    verdict_ashley = uid("verdict-ashley")
    verdict_joshua = uid("verdict-joshua")
    graph.extend(
        [
            {
                "@id": verdict_ashley,
                "@type": ["legalproc:Verdict", "uco-core:UcoObject"],
                "uco-core:name": "Jury verdict: Ashley Grayson guilty on Count 1 (2024-03-29)",
                "uco-core:description": (
                    "The jury returned a guilty verdict as to Ashley "
                    "Grayson on Count 1 at 12:26 PM on 2024-03-29; jury "
                    "polled and discharged at 12:44. "
                    + src_ref("docket", "minute entry 127; D.E. 124")
                ),
                "legalproc:verdictType": "guilty",
                "legalproc:concernsCharge": [{"@id": charge_ashley}],
            },
            {
                "@id": verdict_joshua,
                "@type": ["legalproc:Verdict", "uco-core:UcoObject"],
                "uco-core:name": "Jury verdict: Joshua Grayson not guilty on Count 1 (2024-03-29)",
                "uco-core:description": (
                    "The jury returned a not-guilty verdict as to Joshua "
                    "Grayson on Count 1; judgment of acquittal entered "
                    "2024-04-04 discharging the defendant and "
                    "exonerating his bond. "
                    + src_ref("docket", "minute entry 127; D.E. 125, 134")
                ),
                "legalproc:verdictType": "not-guilty",
                "legalproc:concernsCharge": [{"@id": charge_joshua}],
            },
        ]
    )
    graph.append(rel(verdict_ashley, ashley, "Relates_To"))
    graph.append(rel(verdict_joshua, joshua, "Relates_To"))
    graph.append(rel(verdict_ashley, trial, "Occurred_During"))
    graph.append(rel(verdict_joshua, trial, "Occurred_During"))

    sentencing = uid("proceeding-sentencing")
    graph.append(
        {
            "@id": sentencing,
            "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
            "uco-core:name": "Sentencing hearing (2024-10-31)",
            "uco-core:description": (
                "Sentencing of Ashley Grayson before Judge Thomas L. "
                "Parker on 2024-10-31. Defendant's motion for release "
                "pending appeal (D.E. 209) denied; the court recommended "
                "BOP designation to Carswell Federal Medical Center in "
                "Fort Worth, Texas to be near family, and later ordered "
                "surrender to FMC Carswell by 2:00 PM on 2024-12-19. "
                + src_ref("docket", "minute entry 211; D.E. 224")
            ),
            "legalproc:proceedingType": "sentencing-hearing",
            "uco-core:objectCreatedTime": lit(
                "xsd:dateTime", central_midnight("2024-10-31")
            ),
        }
    )
    graph.append(rel(sentencing, doc_ids["docket"], "Derived_From"))
    graph.append(rel(sentencing, judge_parker, "Presided_Over_By"))

    sentence_imposed = uid("sentence-imposed")
    graph.append(
        {
            "@id": sentence_imposed,
            "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
            "uco-core:name": "Sentence imposed on Ashley Grayson (2024-10-31): 120 months",
            "uco-core:description": (
                "120 months of incarceration — the statutory maximum for "
                "a violation of 18 U.S.C. § 1958 — followed by 3 years "
                "of supervised release with standard/mandatory "
                "conditions plus special conditions: mental health "
                "testing and treatment as directed; no contact directly "
                "or indirectly with D.H., S.H., and P.T.; MRT and DNA "
                "collection. Special assessment of $100. There is no "
                "parole in the federal system. "
                + src_ref("docket", "D.E. 211, 213") + "; "
                + src_ref("press", "para. 7")
            ),
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceTerm": (
                "120 months incarceration + 3 years supervised release; "
                "$100 special assessment"
            ),
            "legalproc:concernsCharge": [{"@id": charge_ashley}],
        }
    )
    graph.append(rel(sentence_imposed, doc_ids["docket"], "Derived_From"))
    graph.append(rel(sentence_imposed, ashley, "Relates_To"))
    graph.append(rel(sentence_imposed, sentencing, "Occurred_During"))
    graph.append(rel(sentence_imposed, judge_parker, "Imposed_By"))

    appeal = uid("proceeding-appeal")
    cert = uid("proceeding-certiorari")
    graph.extend(
        [
            {
                "@id": appeal,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": f"Sixth Circuit appeal No. {USCA_CASE} (affirmed 2025-08-14)",
                "uco-core:description": (
                    "Ashley Grayson's direct appeal, noticed 2024-11-01. "
                    "The Sixth Circuit affirmed in an unpublished "
                    "opinion and judgment filed 2025-08-14; mandate "
                    "issued 2025-09-23 with no costs taxed. "
                    + src_ref("docket", "D.E. 216, 242, 243")
                ),
                "legalproc:proceedingType": "appeal",
                "uco-core:objectCreatedTime": lit(
                    "xsd:dateTime", central_midnight("2024-11-01")
                ),
            },
            {
                "@id": cert,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": f"U.S. Supreme Court No. {SCOTUS_CASE} (writ of certiorari issued 2026-06-24)",
                "uco-core:description": (
                    "Ashley Grayson petitioned for a writ of certiorari "
                    "on 2026-01-14; the Supreme Court granted review and "
                    "the writ of certiorari issued 2026-06-24. The case "
                    "remains pending before the Supreme Court as of the "
                    "docket retrieval date. "
                    + src_ref("docket", "D.E. 250, 253")
                ),
                "legalproc:proceedingType": "certiorari",
                "uco-core:objectCreatedTime": lit(
                    "xsd:dateTime", central_midnight("2026-01-14")
                ),
            },
        ]
    )
    graph.append(rel(appeal, doc_ids["docket"], "Derived_From"))
    graph.append(rel(cert, doc_ids["docket"], "Derived_From"))
    graph.append(rel(appeal, ashley, "Relates_To"))
    graph.append(rel(cert, ashley, "Relates_To"))
    graph.append(rel(appeal, sentence_imposed, "Reviews"))
    graph.append(rel(cert, appeal, "Reviews"))

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
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    exts = ["legalproc"]
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
