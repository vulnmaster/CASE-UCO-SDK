#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Lam et al. (D.D.C. RICO / crypto theft).

Case 1:24-cr-00417-CKK (D.D.C., Judge Colleen Kollar-Kotelly): the
"Social Engineering Enterprise" (SE Enterprise) RICO conspiracy — an
association-in-fact enterprise of gamers-turned-fraudsters who cold-called
cryptocurrency holders while posing as exchange security staff, stole
virtual currency (including approximately $245,093,239 from Victim-7 on
2024-08-19), laundered it through peel chains, pass-through wallets, and
chain-hopping into Monero on no-KYC exchanges, and converted it to bulk
cash, exotic cars, jewelry, and rental mansions. Seventeen defendants
across three charging instruments; nine had pleaded guilty and three had
been sentenced as of the docket printout.

Sources (PACER, all five processed through the MCP document pipeline —
see mcp_outputs/):
  - Docket sheet (case opened 2024-09-17; entries through 2026-06)
  - Superseding Indictment:            Document 50  (filed 2025-04-30)
  - Second Superseding Indictment:     Document 245 (redacted; filed
    2025-11-17; the unredacted Doc 229 was returned 2025-10-29)
  - Statement of Offense (Tangeman):   Document 257 (filed 2025-12-08)
  - Government Sentencing Memorandum
    (Tangeman):                        Document 318 (filed 2026-03-27)

Extensions exercised:
  - extensions/rico — first exemplar: the SE Enterprise as
    rico:RacketeeringEnterprise (enterpriseType "association-in-fact"),
    the charged division of labor as rico:EnterpriseRole nodes
    (database hacker, organizer, target identifier, caller, money
    launderer, residential burglar), and the eight statutory predicate
    categories of the § 1962(d) count as rico:predicateStatute values on
    every RICO charge node.
  - extensions/legalproc — three charging instruments, per-defendant
    per-count charges with docket dispositions, nine guilty pleas,
    recommended and imposed sentences, the Tangeman consent order of
    forfeiture.
  - extensions/cryptoinv — forfeiture-listed USDT addresses with
    CryptocurrencyAddressFacet + VirtualAssetHoldingFacet, no-KYC
    exchanges as VirtualAssetServiceProvider, and launderingTechnique
    values on the laundering actions.

Source-fidelity conventions:
  - Court dates are date-only facts rendered at local midnight Eastern
    time with the correct seasonal UTC offset.
  - Victim identities are "Victim-1" through "Victim-9", exactly as
    charged; unindicted associates keep their charging-document
    designations (COCONSPIRATOR-1, COCONSPIRATOR M.F., MONEY
    EXCHANGER-1) without speculating about identity.
  - PACER's count-label suffixes are kept verbatim ("1s" = superseding,
    "1ss" = second superseding). Tangeman's operative RICO count is
    labeled per the plea minute entry and statement of offense (Count
    1ss / "Count One"); the docket header's terminated-count numbering
    (1, 3, 3s) is noted in the description.
  - The two forfeiture USDT addresses were transcribed by OCR from the
    redacted Second Superseding Indictment; the descriptions flag that
    they must be re-verified against the original before operational
    use.
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

CASE_ID = "lam-ddc-2024-racketeering"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "lam-ddc-2024-racketeering.jsonld"

PACER_DOCKET = "1:24-cr-00417-CKK"
LOCAL_REF = "uploads/racketeering"

SOURCE_DOCS = {
    "docket": {
        "file_name": "pacer -- racketeering -- docket.pdf",
        "sha256": "b85de5b812c7e3ba9ded460ab74c5bb1f9f4f43d4c7d2de49a892e1b29ab622a",
        "pacer_doc": "docket sheet",
        "filed": "2024-09-17 (case opened); printout includes entries through 2026-06",
    },
    "indictment_s": {
        "file_name": "pacer -- racketeering -- superseding indictment.pdf",
        "sha256": "6524fab71c8e01c7cfe0e76757b750bee5312da3e1bbad24debefce1b2158ca4",
        "pacer_doc": "50",
        "filed": "2025-04-30",
    },
    "indictment_ss": {
        "file_name": "pacer -- racketeering -- second superseding indictment.pdf",
        "sha256": "f602adbb26a36b161df15eec1975bb3340df12e41e86487bb7a8a378672a5675",
        "pacer_doc": "245 (redacted; unredacted Doc 229 returned 2025-10-29)",
        "filed": "2025-11-17",
    },
    "soo": {
        "file_name": "pacer -- racketeering -- statement of offense.pdf",
        "sha256": "0d7d3471aa975481c03f73bad1fe65ceac7645943d9f509c4155d9ae7c6ed733",
        "pacer_doc": "257",
        "filed": "2025-12-08",
    },
    "sentmemo": {
        "file_name": "pacer -- racketeering -- sentencing memorandum.pdf",
        "sha256": "82b88df86946da0d30446b54181bcc0e58137a9cd3116492f58118ffa4c40760",
        "pacer_doc": "318",
        "filed": "2026-03-27",
    },
}
# Hashes are recomputed at build time from the PDFs beside this script
# (refresh_source_hashes), so the constants above are a fallback for
# environments without the source PDFs.

PREDICATE_STATUTES = [
    "18 U.S.C. § 1028 (fraud and related activity in connection with identification documents)",
    "18 U.S.C. § 1029 (fraud and related activity in connection with access devices)",
    "18 U.S.C. § 1343 (wire fraud)",
    "18 U.S.C. § 1512 (tampering with a witness, victim, or an informant)",
    "18 U.S.C. § 1956 (laundering of monetary instruments)",
    "18 U.S.C. § 1957 (engaging in monetary transactions in property derived from specified unlawful activity)",
    "18 U.S.C. § 1960 (illegal money transmitters)",
    "18 U.S.C. § 2314 (interstate transportation of stolen property)",
]


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


def eastern_midnight(date_str: str) -> str:
    """Date-only court fact rendered at local midnight Eastern time.

    D.D.C. (Washington, D.C.): EDT (-04:00) roughly March-November,
    EST (-05:00) otherwise. Month-level approximation is sufficient for
    filing dates.
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
            f"{PACER_DOCKET} (D.D.C.); local bundle '{LOCAL_REF}'."
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


def build_graph() -> dict:
    graph: list[dict] = []

    def rel(source: str, target: str, kind: str, directional: bool = True) -> None:
        graph.append(
            {
                "@id": uid(f"rel-{source}-{target}-{kind}"),
                "@type": "uco-core:Relationship",
                "uco-core:source": [{"@id": source}],
                "uco-core:target": [{"@id": target}],
                "uco-core:kindOfRelationship": kind,
                "uco-core:isDirectional": lit("xsd:boolean", directional),
            }
        )

    def person(label: str, name: str, description: str) -> str:
        node = {
            "@id": uid(label),
            "@type": "uco-identity:Person",
            "uco-core:name": name,
            "uco-core:description": description,
        }
        graph.append(node)
        return node["@id"]

    def location(label: str, name: str, description: str) -> str:
        node = {
            "@id": uid(label),
            "@type": "uco-location:Location",
            "uco-core:name": name,
            "uco-core:description": description,
        }
        graph.append(node)
        return node["@id"]

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
            "uco-core:name": "U.S. v. Lam et al. (D.D.C. RICO conspiracy — the SE Enterprise)",
            "uco-core:description": (
                "Federal RICO prosecution in the District of Columbia "
                "(Judge Colleen Kollar-Kotelly) of seventeen members and "
                "associates of the 'Social Engineering Enterprise' (SE "
                "Enterprise), an association-in-fact enterprise that stole "
                "virtual currency through social-engineering cold calls — "
                "including approximately $245,093,239 from Victim-7 on "
                "2024-08-19 — laundered it through peel chains, "
                "pass-through wallets, and chain-hopping into Monero on "
                "no-KYC exchanges, and converted it to bulk cash, exotic "
                "cars, jewelry, and rental mansions in Los Angeles, the "
                "Hamptons, and Miami. Charged in a sealed two-defendant "
                "indictment (Doc 1, 2024-09-14), a fourteen-defendant "
                "superseding indictment (Doc 50, 2025-04-30), and a "
                "second superseding indictment adding three defendants "
                "(Doc 229, 2025-10-29; redacted Doc 245, 2025-11-17). "
                "Nine guilty pleas and three sentencings (Ferro 78 "
                "months, Tangeman 70 months, Desmond 36 months' "
                "probation) as of the docket printout."
            ),
            "uco-core:tag": [
                "racketeering", "rico", "criminal-enterprise",
                "social-engineering", "cryptocurrency-theft",
                "money-laundering", "wire-fraud", "obstruction",
            ],
            "legalproc:caseIdentifier": PACER_DOCKET,
        }
    )
    for key in doc_ids:
        rel(doc_ids[key], investigation, "part_of")

    # ------------------------------------------------------------------
    # The charged enterprise (rico extension) and its roles
    # ------------------------------------------------------------------
    enterprise = uid("org-se-enterprise")
    graph.append(
        {
            "@id": enterprise,
            "@type": ["rico:RacketeeringEnterprise", "uco-identity:Organization"],
            "uco-core:name": "The Social Engineering Enterprise (SE Enterprise)",
            "uco-core:description": (
                "Group of individuals based in California, Connecticut, "
                "New York, Florida, and abroad, associated in fact "
                "although not a legal entity (18 U.S.C. § 1961(4)), "
                "engaged in and affecting interstate and foreign "
                "commerce. Grew from friendships developed on online "
                "gaming platforms that evolved into agreements to commit "
                "cyber-enabled offenses. Operated from no later than "
                "October 2023 through at least May 2025. Charged "
                "purposes: (a) stealing virtual currency from victims "
                "throughout the United States through fraudulent "
                "pretenses; (b) disguising, concealing, and obfuscating "
                "the source and ownership of the stolen funds through "
                "virtual-currency laundering techniques; and (c) "
                "converting laundered virtual currency into fiat currency "
                "and wire transfers for nightclubs, exotic cars, jewelry, "
                "luxury handbags, clothing, private jet rentals, and "
                "rental mansions in Los Angeles, the Hamptons, Miami, and "
                "elsewhere. "
                + src_ref("indictment_ss", "paras. 23-27") + "; "
                + src_ref("soo", "Statement of Facts")
            ),
            "rico:enterpriseType": "association-in-fact",
            "uco-core:tag": ["criminal-enterprise"],
        }
    )

    roles = {
        "database-hacker": (
            "Database hackers were responsible for hacking websites and "
            "servers to obtain cryptocurrency-related databases or "
            "purchasing databases on the dark web."
        ),
        "organizer": (
            "Organizers were responsible (with target identifiers) for "
            "organizing and collating information across various "
            "databases to determine the most valuable targets."
        ),
        "target-identifier": (
            "Target identifiers were responsible (with organizers) for "
            "organizing and collating information across various "
            "databases to determine the most valuable targets."
        ),
        "caller": (
            "Callers ('se'ers') were responsible for cold-calling "
            "victims and convincing them their accounts were the subject "
            "of a cyber-attack and that the caller was attempting to "
            "help secure their accounts."
        ),
        "money-launderer": (
            "Money launderers were responsible for receiving stolen "
            "virtual currency and turning it into fiat US currency as "
            "bulk cash or wire transfer, or providing luxury services "
            "such as exotic car purchases, private jet rentals, "
            "international vacations, or shipping bulk cash across the "
            "United States."
        ),
        "residential-burglar": (
            "Residential burglars ('IRL (in real life) Break-in "
            "members') targeted hardware virtual currency wallets in "
            "victims' homes."
        ),
    }
    role_ids: dict[str, str] = {}
    for slug, desc in roles.items():
        rid = uid(f"role-{slug}")
        role_ids[slug] = rid
        graph.append(
            {
                "@id": rid,
                "@type": ["rico:EnterpriseRole", "uco-role:Role"],
                "uco-core:name": f"SE Enterprise role: {slug.replace('-', ' ')}",
                "uco-core:description": desc + " " + src_ref("indictment_ss", "paras. 25-26, 16, 32"),
                "rico:roleFunction": slug,
            }
        )
        rel(rid, enterprise, "Role_Within")

    # ------------------------------------------------------------------
    # People
    # ------------------------------------------------------------------
    judge = person(
        "person-judge-kollar-kotelly", "Colleen Kollar-Kotelly",
        "District Judge, District of Columbia; presides over "
        f"{PACER_DOCKET}; took the nine guilty pleas and imposed the "
        "Desmond, Tangeman, and Ferro sentences. "
        + src_ref("docket", "assignment and minute entries"),
    )

    defendants = {
        "lam": (
            "Malone Lam",
            "Defendant 1, also known as 'King Greavys', '$$$', '7', 'Kg', "
            "and 'Anne Hathaway'. Charged organizer and target identifier "
            "of the SE Enterprise; participant in the Victim-7 theft of "
            "approximately $245,093,239 on 2024-08-19; spent over "
            "$4,000,000 in stolen virtual currency at Los Angeles "
            "nightclubs between 2024-08-19 and 2024-09-10; tossed his "
            "mobile telephone into Biscayne Bay on 2024-09-18 after "
            "learning agents were coming to arrest him. Arrested in "
            "Miami, Florida on 2024-09-18 on a warrant dated 2024-09-17. "
            "Pending counts 1ss, 2ss, 3ss (plus earlier-instrument "
            "counts) as of the docket printout. "
            + src_ref("indictment_ss", "caption; paras. 29; overt acts uu-vv, yy, qqqq") + "; "
            + src_ref("docket", "Defendant (1); arrest entries"),
        ),
        "serrano": (
            "Jeandiel Serrano",
            "Defendant 2, also known as '@SKIDSTAR' and 'VERSACEGOD'. "
            "Charged in the original sealed indictment (Doc 1) with "
            "conspiracy to commit wire fraud and money laundering; "
            "identified in the Tangeman statement of offense as an SE "
            "Enterprise member for whom Tangeman procured the 'Hesby "
            "House' Los Angeles rental under a fake identity. Arrested "
            "in Los Angeles, California on 2024-09-18. "
            + src_ref("docket", "Defendant (2); arrest entries") + "; "
            + src_ref("soo", "Hesby House facts"),
        ),
        "ferro": (
            "Marlon Ferro",
            "Defendant 3, also known as 'Marlo' and 'GothFerrari'. "
            "Arrested in California on 2025-05-13; pleaded guilty to "
            "Count 1 (RICO conspiracy) on 2025-10-17 and was sentenced "
            "on 2026-05-06 to 78 months' incarceration followed by 36 "
            "months' supervised release and a $100 special assessment; "
            "Counts 2 and 3 dismissed on the government's oral motion. "
            + src_ref("docket", "Defendant (3); plea and sentencing minute entries"),
        ),
        "doost": (
            "Hamza Doost",
            "Defendant 4, also known as 'Scyllia'. Arrested in "
            "California on 2025-05-13; pleaded guilty to Count 1 (RICO "
            "conspiracy) on 2025-08-25. "
            + src_ref("docket", "Defendant (4); plea minute entry"),
        ),
        "flansburg": (
            "Conor Flansburg",
            "Defendant 5, also known as 'OO', 'Green Room', and "
            "'@D0UU0B'. Charged database hacker/organizer designated "
            "COCONSPIRATOR C.F. in later instruments; named in the "
            "Tangeman statement of offense (as 'Connor Flansburg') among "
            "the SE Enterprise members who arrived in Los Angeles. "
            "Arrested in California on 2025-05-13; pleaded guilty to "
            "Count 1 (RICO conspiracy) on 2025-09-26. "
            + src_ref("docket", "Defendant (5); plea minute entry") + "; "
            + src_ref("soo", "Statement of Facts"),
        ),
        "mehta": (
            "Kunal Mehta",
            "Defendant 6, also known as 'Papa', 'The Accountant', "
            "'Shrek', and 'Neil'. Charged money launderer for the SE "
            "Enterprise. Arrested in California on 2025-05-13; pleaded "
            "guilty to Count 1ss (RICO conspiracy, Second Superseding "
            "Indictment) on 2025-11-17. "
            + src_ref("indictment_ss", "para. 31") + "; "
            + src_ref("docket", "Defendant (6); plea minute entry"),
        ),
        "yarally": (
            "Ethan Yarally",
            "Defendant 7, also known as 'Rand' and '15%'. Charged "
            "caller for the SE Enterprise. Arrested in Sterling, "
            "Virginia on 2025-07-25; pleaded guilty to Count 1s (RICO "
            "conspiracy) on 2026-01-08. "
            + src_ref("indictment_ss", "para. 30") + "; "
            + src_ref("docket", "Defendant (7); plea minute entry"),
        ),
        "demirtas": (
            "Cody Demirtas",
            "Defendant 8, also known as 'KO' and 'Kody'. Arrested in "
            "Dulles, Virginia on 2025-07-16; pleaded guilty to Count 1 "
            "(RICO conspiracy) on 2025-10-14. "
            + src_ref("docket", "Defendant (8); plea minute entry"),
        ),
        "anand": (
            "Aakaash Anand",
            "Defendant 9, also known as 'Light' and 'Dark'. Charged "
            "caller and money launderer for the SE Enterprise; assisted "
            "with laundering the Victim-7 proceeds on no-KYC exchanges "
            "and traveled from New Zealand in September 2024 to retrieve "
            "luxury clothing purchased with stolen virtual currency. "
            "Counts 1s, 2s, 3s pending. "
            + src_ref("indictment_ss", "paras. 30-31; overt acts xx, lll") + "; "
            + src_ref("docket", "Defendant (9)"),
        ),
        "tangeman": (
            "Evan Tangeman",
            "Defendant 10, also known as 'Tate', 'E', and 'Evan | "
            "Exchanger'. Money launderer for the SE Enterprise who "
            "provided unlicensed crypto-to-cash services (typically at a "
            "7% commission), procured rental mansions under fake "
            "identities for enterprise members, watched the 2024-09-18 "
            "FBI searches of Lam's Miami homes through remote "
            "security-camera access, and directed co-defendant Tucker "
            "Desmond to destroy co-conspirators' digital devices after "
            "the Lam and Serrano arrests. Arrested in California on "
            "2025-05-13; pleaded guilty to Count One of the Second "
            "Superseding Indictment (RICO conspiracy; minute-entry label "
            "Count 1ss) on 2025-12-08; sentenced on 2026-04-24 to 70 "
            "months' incarceration followed by 36 months' supervised "
            "release and a $100 special assessment; the money-laundering "
            "conspiracy count (3ss) was dismissed on the government's "
            "oral motion. The docket header lists his terminated counts "
            "as 1, 3, and 3s. "
            + src_ref("soo", "Summary of the Plea Agreement; Statement of Facts") + "; "
            + src_ref("sentmemo", "passim") + "; "
            + src_ref("docket", "Defendant (10); plea and sentencing minute entries"),
        ),
        "cortes": (
            "Joel Cortes",
            "Defendant 11, also known as 'J'. Arrested in California on "
            "2025-05-13; pleaded guilty to Count 1 (RICO conspiracy) on "
            "2025-07-31 — the first defendant to plead. "
            + src_ref("docket", "Defendant (11); plea minute entry"),
        ),
        "lnu1": (
            "FNU LNU-1",
            "Defendant 12, name unknown, also known as '~_~', "
            "'Squiggly', and 'CHEN'. Charged database hacker for the SE "
            "Enterprise; participant in the Victim-7 theft. Counts 1s "
            "and 2s pending. "
            + src_ref("indictment_ss", "para. 28; overt acts uu-vv") + "; "
            + src_ref("docket", "Defendant (12)"),
        ),
        "lnu2": (
            "FNU LNU-2",
            "Defendant 13, name unknown, also known as 'Danny' and "
            "'Meech'. Counts 1, 2, and 3 of the Superseding Indictment "
            "pending. " + src_ref("docket", "Defendant (13)"),
        ),
        "desmond": (
            "Tucker Desmond",
            "Defendant 14. At Tangeman's direction after the Lam and "
            "Serrano arrests, traveled to Lam's Los Angeles homes, "
            "retrieved electronic devices, and destroyed them to prevent "
            "their seizure by law enforcement. Arrested in California on "
            "2025-05-13; pleaded guilty to Count 4 (obstruction of "
            "justice) on 2025-10-15 and was sentenced on 2026-03-20 to "
            "36 months' probation and a $100 special assessment; Count 3 "
            "dismissed. "
            + src_ref("sentmemo", "introduction") + "; "
            + src_ref("docket", "Defendant (14); plea and sentencing minute entries"),
        ),
        "zulfiqar": (
            "Danish Zulfiqar",
            "Defendant 15, also known as 'Danish Khan', 'Danny', 'W.', "
            "and 'Meech'. Added in the Second Superseding Indictment; "
            "Counts 1, 2, and 3 pending. "
            + src_ref("docket", "Defendant (15)"),
        ),
        "ibrahim": (
            "Mustafa Ibrahim",
            "Defendant 16, also known as 'Krust' and 'KRR'. Added in "
            "the Second Superseding Indictment; Counts 1, 2, and 3 "
            "pending. " + src_ref("docket", "Defendant (16)"),
        ),
        "dellecave": (
            "Nicolas Dellecave",
            "Defendant 17, also known as 'Nic' and 'Souja'. Added in "
            "the Second Superseding Indictment; Counts 1, 2, and 3 "
            "pending. " + src_ref("docket", "Defendant (17)"),
        ),
    }
    person_ids: dict[str, str] = {}
    for key, (name, desc) in defendants.items():
        person_ids[key] = person(f"person-{key}", name, desc)

    mf = person(
        "person-coconspirator-mf", "COCONSPIRATOR M.F.",
        "Unnamed co-conspirator designated by initials in the Second "
        "Superseding Indictment; served as the SE Enterprise's "
        "residential burglar / IRL break-in member. In July 2024 flew "
        "to New Mexico, set up a telephone with a video camera across "
        "from Victim-4's home to livestream the break-in, and on "
        "2024-07-08, in coordination with Lam and others, broke into "
        "Victim-4's home in search of hardware virtual currency "
        "devices. The identity behind the initials is not established "
        "in the reviewed documents. "
        + src_ref("indictment_ss", "para. 32; overt acts kk-mm"),
    )
    me1 = person(
        "person-money-exchanger-1", "MONEY EXCHANGER-1",
        "Unnamed unlicensed crypto-to-cash money transmitter designated "
        "in the charging documents; with Tangeman, laundered "
        "approximately $3,000,000 in cryptocurrency for Lam on "
        "2024-08-25/26 so Lam could obtain a new Los Angeles rental "
        "home, instructing Lam to send $550,000 tranches in USDT and "
        "deducting from the total owed each time. "
        + src_ref("indictment_ss", "overt act aaa") + "; "
        + src_ref("sentmemo", "Statement of Facts quotes"),
    )
    victim4 = person(
        "person-victim-4", "Victim-4",
        "Victim identified only as Victim-4. Target of a "
        "social-engineering fraud scheme; Lam accessed Victim-4's Apple "
        "iCloud account in July 2024 to monitor Victim-4's location in "
        "real time, and COCONSPIRATOR M.F. broke into Victim-4's New "
        "Mexico home on 2024-07-08 in search of hardware virtual "
        "currency devices. "
        + src_ref("indictment_ss", "overt acts ii-mm"),
    )
    victim7 = person(
        "person-victim-7", "Victim-7",
        "Victim identified only as Victim-7. On 2024-08-19, while at "
        "his home in Washington, D.C., was convinced by Lam, "
        "COCONSPIRATOR-1, COCONSPIRATOR-2, CHEN, and another to "
        "download a remote desktop connection program; the conspirators "
        "accessed his computer and stole approximately $245,093,239.00 "
        "in virtual currency — the largest single theft charged. "
        + src_ref("indictment_ss", "overt acts uu-vv"),
    )

    # Organizations
    usao = uid("org-usao-dc")
    fbi = uid("org-fbi")
    graph.extend(
        [
            {
                "@id": usao,
                "@type": "uco-identity:Organization",
                "uco-core:name": "U.S. Attorney's Office for the District of Columbia",
                "uco-core:description": (
                    "Prosecuting office. The government's Tangeman "
                    "sentencing memorandum is submitted by U.S. Attorney "
                    "Jeanine Ferris Pirro; AUSAs of record across the "
                    "docket include Kevin L. Rosenberg and William G. "
                    "Hart. "
                    + src_ref("sentmemo", "signature block") + "; "
                    + src_ref("docket", "minute entries")
                ),
            },
            {
                "@id": fbi,
                "@type": "uco-identity:Organization",
                "uco-core:name": "Federal Bureau of Investigation",
                "uco-core:description": (
                    "Investigating agency; executed the 2024-09-18 "
                    "search warrants at Lam's two Miami rental homes "
                    "(watched remotely by Tangeman through the security "
                    "camera system) and the 2025-05-13 arrests in "
                    "California. "
                    + src_ref("sentmemo", "Statement of Facts") + "; "
                    + src_ref("docket", "arrest entries")
                ),
            },
        ]
    )

    # Membership and role relationships. Membership is asserted only
    # where a reviewed document places the person in the enterprise.
    for key in ("lam", "serrano", "ferro", "doost", "flansburg", "mehta",
                "yarally", "demirtas", "anand", "tangeman", "cortes",
                "lnu1", "lnu2", "zulfiqar", "ibrahim", "dellecave"):
        rel(person_ids[key], enterprise, "Member_Of")
    rel(mf, enterprise, "Member_Of")

    has_role = {
        "lam": ["organizer", "target-identifier"],
        "lnu1": ["database-hacker"],
        "flansburg": ["database-hacker", "organizer"],
        "yarally": ["caller"],
        "anand": ["caller", "money-launderer"],
        "mehta": ["money-launderer"],
        "tangeman": ["money-launderer"],
    }
    for key, slugs in has_role.items():
        for slug in slugs:
            rel(person_ids[key], role_ids[slug], "Has_Role")
    rel(mf, role_ids["residential-burglar"], "Has_Role")

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------
    dc_home = location(
        "loc-victim7-home", "Victim-7's home, Washington, D.C.",
        "Where Victim-7 was located during the 2024-08-19 "
        "social-engineering fraud scheme and theft of approximately "
        "$245,093,239 in virtual currency.",
    )
    nm_home = location(
        "loc-victim4-home", "Victim-4's home, New Mexico",
        "Residence broken into by COCONSPIRATOR M.F. on 2024-07-08 in "
        "search of hardware virtual currency devices, while a "
        "telephone-camera livestream across the street let other "
        "enterprise members warn of the victim's return.",
    )
    miami = location(
        "loc-lam-miami-homes", "Lam's two rental homes, Miami, Florida",
        "Rental homes procured with stolen cryptocurrency through "
        "Tangeman; searched by the FBI on 2024-09-18. Lam tossed his "
        "phone from the rear boat dock into Biscayne Bay the same day.",
    )
    hesby = location(
        "loc-hesby-house", "The 'Hesby House', Los Angeles, California",
        "Los Angeles rental home procured for Serrano through Tangeman "
        "under the fake identity 'Sean McGarry', with $120,800 in cash "
        "as upfront payment and security deposit and $30,000 per month "
        "in rent. The lease listed 'Sean McGarry, Maria Gonzales, Math "
        "Ghay, Joker Ayusn, and Garth Jackson' as tenants; McGarry does "
        "not exist in any FBI systems.",
    )

    # ------------------------------------------------------------------
    # Cyber observables and crypto assets
    # ------------------------------------------------------------------
    remote_desktop = uid("obs-remote-desktop-program")
    victim7_computer = uid("obs-victim7-computer")
    telegram_msg_1 = uid("obs-msg-tangeman-500k")
    telegram_msg_2 = uid("obs-msg-tangeman-movein")
    camera_system = uid("obs-security-camera-system")
    lam_phone = uid("obs-lam-phone")
    destroyed_devices = uid("obs-destroyed-devices")
    fake_id = uid("obs-fake-id-mcgarry")
    graph.extend(
        [
            {
                "@id": remote_desktop,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Remote desktop connection program downloaded by Victim-7",
                "uco-core:description": (
                    "Program Victim-7 was convinced to download onto his "
                    "computer on 2024-08-19; the conspirators then "
                    "accessed the computer through it during the "
                    "social-engineering fraud scheme. "
                    + src_ref("indictment_ss", "overt act vv")
                ),
                "uco-core:tag": ["evidence", "remote-access"],
            },
            {
                "@id": victim7_computer,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Victim-7's computer, Washington, D.C.",
                "uco-core:description": (
                    "Computer accessed by Lam, COCONSPIRATOR-1, "
                    "COCONSPIRATOR-2, CHEN, and another through the "
                    "remote desktop connection program during the theft "
                    "of approximately $245,093,239 in virtual currency. "
                    + src_ref("indictment_ss", "overt act vv")
                ),
                "uco-core:tag": ["evidence"],
            },
            {
                "@id": telegram_msg_1,
                "@type": "uco-observable:Message",
                "uco-core:name": "Tangeman group-chat message requesting $500,000 in cash",
                "uco-core:description": (
                    "Message from Tangeman in the 2024-08-25 group chat "
                    "with Lam and MONEY EXCHANGER-1 arranging the "
                    "$3,000,000 crypto-to-cash conversion for a new Los "
                    "Angeles rental home: 'need at least $500k rn "
                    "[right now] . . . to give to the owner . . is that "
                    "doable.' MONEY EXCHANGER-1 replied with his USDT "
                    "(Tether) address and instructed Lam and others to "
                    "send $550,000 in cryptocurrency at a time, "
                    "deducting from the total owed until they "
                    "accumulated approximately $3,000,000. "
                    + src_ref("sentmemo", "Statement of Facts quotes")
                ),
                "uco-core:tag": ["evidence", "communication"],
            },
            {
                "@id": telegram_msg_2,
                "@type": "uco-observable:Message",
                "uco-core:name": "Tangeman message on the move-in date and USDT exchange",
                "uco-core:description": (
                    "Message from Tangeman to Lam in the same exchange: "
                    "'[t]he move in date all depends on how quickly i "
                    "can get the usdt because i have to get it exchanged "
                    "and wired over it all takes time ... the 500k is "
                    "going to be dropped off tonight.' Tangeman also "
                    "warned against touring the home because the realtor "
                    "had listed a fake identity on the lease documents "
                    "to conceal Lam's true ownership. "
                    + src_ref("sentmemo", "Statement of Facts quotes")
                ),
                "uco-core:tag": ["evidence", "communication"],
            },
            {
                "@id": camera_system,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Security camera system at Lam's Miami rental homes",
                "uco-core:description": (
                    "Camera system Tangeman accessed remotely from Los "
                    "Angeles on 2024-09-18 to watch FBI agents search "
                    "the residences and inventory evidence, taking "
                    "screenshots and sharing the video. "
                    + src_ref("indictment_ss", "overt act rrrr") + "; "
                    + src_ref("sentmemo", "Statement of Facts")
                ),
                "uco-core:tag": ["evidence", "surveillance"],
            },
            {
                "@id": lam_phone,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Lam's mobile telephone (tossed into Biscayne Bay)",
                "uco-core:description": (
                    "Mobile telephone Lam tossed off the boat dock at "
                    "the rear of his Miami rental home into Biscayne Bay "
                    "on 2024-09-18 to destroy incriminating evidence, "
                    "after being advised law enforcement were on their "
                    "way to arrest him. "
                    + src_ref("indictment_ss", "overt acts pppp-qqqq")
                ),
                "uco-core:tag": ["evidence", "destroyed-evidence"],
            },
            {
                "@id": destroyed_devices,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Electronic devices destroyed at Lam's Los Angeles homes",
                "uco-core:description": (
                    "Digital devices belonging to members of the "
                    "enterprise that Desmond, at Tangeman's direction "
                    "after the Lam and Serrano arrests, retrieved from "
                    "Lam's Los Angeles homes and destroyed to prevent "
                    "their seizure by law enforcement and impair their "
                    "integrity for trial — the conduct underlying "
                    "Desmond's Count 4 obstruction conviction. "
                    + src_ref("sentmemo", "introduction; Statement of Facts")
                ),
                "uco-core:tag": ["evidence", "destroyed-evidence", "obstruction"],
            },
            {
                "@id": fake_id,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Fake 'Sean McGarry' identity used on the Hesby House lease",
                "uco-core:description": (
                    "Fabricated identity (with ID card) under which the "
                    "Hesby House was rented for Serrano; 'McGarry, with "
                    "the identifiers in this ID card, does not exist in "
                    "any FBI systems.' Identification-document fraud (18 "
                    "U.S.C. § 1028) is a charged predicate category of "
                    "the racketeering pattern. "
                    + src_ref("sentmemo", "Hesby House facts")
                ),
                "uco-core:tag": ["evidence", "false-identity"],
            },
        ]
    )
    rel(remote_desktop, victim7_computer, "Installed_On")
    rel(telegram_msg_1, person_ids["tangeman"], "Sent_From")
    rel(telegram_msg_2, person_ids["tangeman"], "Sent_From")
    rel(telegram_msg_2, person_ids["lam"], "Sent_To")

    # Forfeiture-listed USDT addresses (cryptoinv extension). Addresses
    # were transcribed by OCR from the redacted Second Superseding
    # Indictment and must be re-verified against the original document
    # before operational use.
    addr_c1 = uid("obs-usdt-address-c1")
    addr_c2 = uid("obs-usdt-address-c2")
    graph.extend(
        [
            {
                "@id": addr_c1,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Forfeiture item C1: 457,997.495978 USDT at 0xc63f…a462",
                "uco-core:description": (
                    "Virtual currency address holding 457,997.495978 "
                    "USDT ($458,256.26) listed as specific property "
                    "subject to forfeiture, item C1. Address transcribed "
                    "by OCR from the redacted Second Superseding "
                    "Indictment; verify against the original before "
                    "operational use. "
                    + src_ref("indictment_ss", "forfeiture item C1")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("obs-usdt-address-c1-addr-facet"),
                        "@type": "cryptoinv:CryptocurrencyAddressFacet",
                        "cryptoinv:addressValue": "0xc63f41909DfeDEE97Cf88Ac3EfE7a5e2c3F7a462",
                        "cryptoinv:cryptocurrencyType": "USDT",
                        "cryptoinv:blockchainNetwork": "Ethereum",
                        "cryptoinv:addressFormat": "EVM (0x-prefixed hex)",
                    },
                    {
                        "@id": uid("obs-usdt-address-c1-holding-facet"),
                        "@type": "cryptoinv:VirtualAssetHoldingFacet",
                        "cryptoinv:assetSymbol": "USDT",
                        "cryptoinv:assetQuantity": lit("xsd:decimal", "457997.495978"),
                        "cryptoinv:fiatValue": lit("xsd:decimal", "458256.26"),
                        "cryptoinv:fiatCurrencyCode": "USD",
                    },
                ],
                "uco-core:tag": ["forfeiture", "cryptocurrency"],
            },
            {
                "@id": addr_c2,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Forfeiture item C2: 1,020,392 USDT at 0x588d…1e5c",
                "uco-core:description": (
                    "Virtual currency address holding 1,020,392 USDT "
                    "($1,020,968.52) listed as specific property subject "
                    "to forfeiture, item C2. Address transcribed by OCR "
                    "from the redacted Second Superseding Indictment; "
                    "verify against the original before operational use. "
                    + src_ref("indictment_ss", "forfeiture item C2")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("obs-usdt-address-c2-addr-facet"),
                        "@type": "cryptoinv:CryptocurrencyAddressFacet",
                        "cryptoinv:addressValue": "0x588d86Fb0B8d8A318aDc5cFc7Dd460E1794D1e5c",
                        "cryptoinv:cryptocurrencyType": "USDT",
                        "cryptoinv:blockchainNetwork": "Ethereum",
                        "cryptoinv:addressFormat": "EVM (0x-prefixed hex)",
                    },
                    {
                        "@id": uid("obs-usdt-address-c2-holding-facet"),
                        "@type": "cryptoinv:VirtualAssetHoldingFacet",
                        "cryptoinv:assetSymbol": "USDT",
                        "cryptoinv:assetQuantity": lit("xsd:decimal", "1020392"),
                        "cryptoinv:fiatValue": lit("xsd:decimal", "1020968.52"),
                        "cryptoinv:fiatCurrencyCode": "USD",
                    },
                ],
                "uco-core:tag": ["forfeiture", "cryptocurrency"],
            },
        ]
    )

    # No-KYC exchanges used for chain-hopping into Monero.
    thorswap = uid("org-thorswap")
    exch = uid("org-exch")
    graph.extend(
        [
            {
                "@id": thorswap,
                "@type": ["cryptoinv:VirtualAssetServiceProvider", "uco-identity:Organization"],
                "uco-core:name": "Thorswap",
                "uco-core:description": (
                    "Virtual currency exchange named in the indictment "
                    "as one the money launderers used to change stolen "
                    "cryptocurrency into privacy coins such as Monero "
                    "(XMR) to disguise and conceal the location, "
                    "ownership, and control of the stolen funds. "
                    + src_ref("indictment_ss", "para. 19; Count 3 manner and means")
                ),
                "uco-core:tag": ["no-kyc-exchange"],
            },
            {
                "@id": exch,
                "@type": ["cryptoinv:VirtualAssetServiceProvider", "uco-identity:Organization"],
                "uco-core:name": "eXch",
                "uco-core:description": (
                    "Virtual currency exchange named in the indictment "
                    "as one the money launderers used to change stolen "
                    "cryptocurrency into privacy coins such as Monero "
                    "(XMR) to disguise and conceal the location, "
                    "ownership, and control of the stolen funds. "
                    + src_ref("indictment_ss", "para. 19; Count 3 manner and means")
                ),
                "uco-core:tag": ["no-kyc-exchange"],
            },
        ]
    )

    # Physical forfeiture items (representative subset of the specific
    # property list).
    ferrari = uid("item-ferrari-sf90")
    lv_cash = uid("item-lv-bag-cash")
    graph.extend(
        [
            {
                "@id": ferrari,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "2022 Ferrari SF90 Stradale, VIN ZFF95NLA2N0274061 (forfeiture item V1)",
                "uco-core:description": (
                    "Exotic automobile listed as specific property "
                    "subject to forfeiture, item V1. The enterprise "
                    "bought exotic cars — Ferraris, Lamborghinis, "
                    "Mercedes G Wagons, Rolls Royces — with laundered "
                    "virtual currency, often held by straw owners. "
                    + src_ref("indictment_ss", "forfeiture item V1; manner and means")
                ),
                "uco-core:tag": ["forfeiture"],
            },
            {
                "@id": lv_cash,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "Cash in brown Louis Vuitton bag totaling $169,700 (forfeiture item C1, currency list)",
                "uco-core:description": (
                    "Bulk cash listed as specific property subject to "
                    "forfeiture. "
                    + src_ref("indictment_ss", "forfeiture currency list")
                ),
                "uco-core:tag": ["forfeiture", "bulk-cash"],
            },
        ]
    )

    # ------------------------------------------------------------------
    # Charging instruments
    # ------------------------------------------------------------------
    indictment1 = uid("charging-instrument-original")
    indictment_s = uid("charging-instrument-superseding")
    indictment_ss = uid("charging-instrument-second-superseding")
    graph.extend(
        [
            {
                "@id": indictment1,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": "Sealed Indictment (Doc 1, filed 2024-09-14)",
                "uco-core:description": (
                    "Original two-defendant sealed indictment against "
                    "Lam (counts 1-2) and Serrano (counts 1-2) with a "
                    "forfeiture allegation; unsealed as to Serrano on "
                    "2024-10-08 and as to Lam on 2024-11-01. Described "
                    "from the docket; the document itself is not among "
                    "the reviewed sources. "
                    + src_ref("docket", "entry 1; unsealing minute entries")
                ),
                "legalproc:instrumentType": "indictment",
                "uco-core:objectCreatedTime": lit("xsd:dateTime", eastern_midnight("2024-09-14")),
            },
            {
                "@id": indictment_s,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": "Superseding Indictment (Doc 50, filed 2025-04-30)",
                "uco-core:description": (
                    "Fourteen-defendant superseding indictment: RICO "
                    "conspiracy (Count 1), conspiracy to commit wire "
                    "fraud (Count 2), conspiracy to launder monetary "
                    "instruments (Count 3), and obstruction (Count 4, "
                    "Desmond), with forfeiture allegations. Lam's counts "
                    "carry the 's' suffix (1s, 2s, 3s) on the docket. "
                    + src_ref("indictment_s", "caption") + "; "
                    + src_ref("docket", "entry 50")
                ),
                "legalproc:instrumentType": "superseding-indictment",
                "uco-core:objectCreatedTime": lit("xsd:dateTime", eastern_midnight("2025-04-30")),
            },
            {
                "@id": indictment_ss,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": "Second Superseding Indictment (Doc 229, returned 2025-10-29; redacted Doc 245, filed 2025-11-17)",
                "uco-core:description": (
                    "Second superseding indictment adding defendants "
                    "Zulfiqar, Ibrahim, and Dellecave and restating the "
                    "RICO, wire-fraud, and money-laundering conspiracy "
                    "counts (docket suffixes 'ss' for Lam and 's' or "
                    "unsuffixed for others), with RICO forfeiture "
                    "allegations under 18 U.S.C. § 1963 listing USDT "
                    "addresses, exotic automobiles, bulk cash, and "
                    "luxury goods. The reviewed PDF is the redacted "
                    "Doc 245. "
                    + src_ref("indictment_ss", "caption; forfeiture") + "; "
                    + src_ref("docket", "entries 229, 245")
                ),
                "legalproc:instrumentType": "superseding-indictment",
                "uco-core:objectCreatedTime": lit("xsd:dateTime", eastern_midnight("2025-10-29")),
            },
        ]
    )
    rel(indictment_s, doc_ids["indictment_s"], "Derived_From")
    rel(indictment_ss, doc_ids["indictment_ss"], "Derived_From")
    rel(indictment1, doc_ids["docket"], "Derived_From")

    for item in (addr_c1, addr_c2, ferrari, lv_cash):
        rel(item, indictment_ss, "Listed_For_Forfeiture_In")

    # ------------------------------------------------------------------
    # Charges (operative instrument per defendant, dispositions from
    # the docket). RICO counts carry the eight § 1961(1) predicate
    # categories as rico:predicateStatute values.
    # ------------------------------------------------------------------
    RICO = ("18 U.S.C. § 1962(d)", "RICO Conspiracy")
    WIRE = ("18 U.S.C. § 1349", "Conspiracy to Commit Wire Fraud")
    ML_CONSP = ("18 U.S.C. § 1956(h)", "Conspiracy to Launder Monetary Instruments")

    def charge(label: str, defendant: str, instrument: str, count_label: str,
               count_num: int, statute: str, title: str, offense_form: str,
               disposition: str, description: str,
               rico_count: bool = False, object_offense: str | None = None) -> str:
        cid = uid(label)
        node: dict = {
            "@id": cid,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": f"{defendants[defendant][0]} — {count_label}: {title}",
            "uco-core:description": description,
            "legalproc:statuteCitation": statute,
            "legalproc:countNumber": lit("xsd:nonNegativeInteger", count_num),
            "legalproc:countLabel": count_label,
            "legalproc:offenseForm": offense_form,
            "legalproc:chargeDisposition": disposition,
            "legalproc:assertedIn": {"@id": instrument},
        }
        if rico_count:
            node["rico:predicateStatute"] = list(PREDICATE_STATUTES)
        if object_offense:
            node["legalproc:objectOffense"] = {"@id": uid(object_offense)}
        graph.append(node)
        rel(person_ids[defendant], cid, "Charged_With")
        return cid

    rico_desc = (
        "Knowingly and intentionally conspiring to violate 18 U.S.C. "
        "§ 1962(c) — to conduct and participate in the conduct of the "
        "affairs of the SE Enterprise through a pattern of racketeering "
        "activity (18 U.S.C. §§ 1961(1), (5)) consisting of multiple "
        "acts indictable under the eight enumerated statutory "
        "categories, each defendant agreeing that a conspirator would "
        "commit at least two acts of racketeering activity. "
        + src_ref("indictment_ss", "Count One, paras. 34-36")
    )
    wire_desc = (
        "Conspiring to commit wire fraud by devising a scheme to "
        "defraud and obtain money, property, and cryptocurrency from "
        "Victim-1 through Victim-9 and others by materially false and "
        "fraudulent pretenses, causing interstate wire transmissions in "
        "execution of the scheme. "
        + src_ref("indictment_ss", "Count Two, paras. 38-39")
    )
    ml_desc = (
        "Conspiring to violate 18 U.S.C. §§ 1956(a)(1)(B)(i) and 1957 "
        "— moving $245,093,239.00 in stolen cryptocurrency, along with "
        "other stolen cryptocurrency, through numerous financial "
        "transactions designed to conceal the nature, location, source, "
        "ownership, and control of the proceeds of the Count Two wire "
        "fraud conspiracy. "
        + src_ref("indictment_ss", "Count Three, paras. 40-41")
    )

    charge_ids: dict[str, str] = {}

    def C(label, *args, **kwargs):
        charge_ids[label] = charge(label, *args, **kwargs)

    # Lam — Second Superseding Indictment (counts 1ss, 2ss, 3ss pending).
    C("charge-lam-1ss", "lam", indictment_ss, "Count 1ss", 1, RICO[0], RICO[1],
      "conspiracy", "pending", rico_desc + " Pending as of the docket printout.",
      rico_count=True)
    C("charge-lam-2ss", "lam", indictment_ss, "Count 2ss", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending", wire_desc + " Pending as of the docket printout.")
    C("charge-lam-3ss", "lam", indictment_ss, "Count 3ss", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "pending", ml_desc + " Pending as of the docket printout.",
      object_offense="charge-lam-2ss")

    # Serrano — original sealed indictment (counts 1-2 pending).
    C("charge-serrano-1", "serrano", indictment1, "Count 1", 1, WIRE[0],
      "Conspiracy to Commit Bank and Wire Fraud", "conspiracy", "pending",
      "Conspiracy to commit wire fraud charged in the original sealed "
      "indictment (docket offense text: '18:1349; CONSPIRACY TO COMMIT "
      "BANK AND WIRE FRAUD; Conspiracy to Commit Wire Fraud'). Pending "
      "as of the docket printout. " + src_ref("docket", "Defendant (2) pending counts"))
    C("charge-serrano-2", "serrano", indictment1, "Count 2", 2,
      "18 U.S.C. § 1956(a)(1)(B)(i)", "Laundering of Monetary Instruments",
      "substantive", "pending",
      "Concealment money laundering charged in the original sealed "
      "indictment. Pending as of the docket printout. "
      + src_ref("docket", "Defendant (2) pending counts"))

    # Ferro — Superseding Indictment; guilty to Count 1, sentenced.
    C("charge-ferro-1", "ferro", indictment_s, "Count 1", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Ferro pleaded guilty 2025-10-17 and was sentenced "
      "2026-05-06 to 78 months' incarceration, 36 months' supervised "
      "release, and a $100 special assessment. "
      + src_ref("docket", "Defendant (3); sentencing minute entry"),
      rico_count=True)
    C("charge-ferro-2", "ferro", indictment_s, "Count 2", 2, WIRE[0], WIRE[1],
      "conspiracy", "dismissed",
      wire_desc + " Dismissed on the government's oral motion at Ferro's "
      "2026-05-06 sentencing. " + src_ref("docket", "sentencing minute entry"))
    C("charge-ferro-3", "ferro", indictment_s, "Count 3", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "dismissed",
      ml_desc + " Dismissed on the government's oral motion at Ferro's "
      "2026-05-06 sentencing. " + src_ref("docket", "sentencing minute entry"),
      object_offense="charge-ferro-2")

    # Doost — Superseding Indictment; guilty to Count 1, Count 3 pending.
    C("charge-doost-1", "doost", indictment_s, "Count 1", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Doost pleaded guilty 2025-08-25; sentencing not yet "
      "held as of the docket printout. " + src_ref("docket", "plea minute entry"),
      rico_count=True)
    C("charge-doost-3", "doost", indictment_s, "Count 3", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "pending",
      ml_desc + " Not-guilty plea maintained at the 2025-08-25 plea "
      "hearing; pending as of the docket printout. "
      + src_ref("docket", "plea minute entry"))

    # Flansburg — Superseding Indictment; guilty to Count 1, Count 2 pending.
    C("charge-flansburg-1", "flansburg", indictment_s, "Count 1", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Flansburg pleaded guilty 2025-09-26. "
      + src_ref("docket", "plea minute entry"), rico_count=True)
    C("charge-flansburg-2", "flansburg", indictment_s, "Count 2", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending",
      wire_desc + " Not-guilty plea maintained at the 2025-09-26 plea "
      "hearing; pending as of the docket printout. "
      + src_ref("docket", "plea minute entry"))

    # Mehta — Second Superseding Indictment (docket labels 1s, 3s).
    C("charge-mehta-1s", "mehta", indictment_ss, "Count 1s", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Mehta was arraigned and pleaded guilty to the RICO "
      "count of the Second Superseding Indictment (minute-entry label "
      "Count 1ss; docket-entry label 1s) on 2025-11-17. "
      + src_ref("docket", "entry 229; plea minute entry"), rico_count=True)
    C("charge-mehta-3s", "mehta", indictment_ss, "Count 3s", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "pending",
      ml_desc + " Not-guilty plea entered at the 2025-11-17 arraignment; "
      "pending as of the docket printout. " + src_ref("docket", "plea minute entry"))

    # Yarally — Second Superseding Indictment (labels 1s, 2s).
    C("charge-yarally-1s", "yarally", indictment_ss, "Count 1s", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Yarally pleaded guilty to Count 1s on 2026-01-08. "
      + src_ref("docket", "plea minute entry"), rico_count=True)
    C("charge-yarally-2s", "yarally", indictment_ss, "Count 2s", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending",
      wire_desc + " Not-guilty plea maintained at the 2026-01-08 plea "
      "hearing; pending as of the docket printout. "
      + src_ref("docket", "plea minute entry"))

    # Demirtas — Superseding Indictment.
    C("charge-demirtas-1", "demirtas", indictment_s, "Count 1", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Demirtas pleaded guilty 2025-10-14. "
      + src_ref("docket", "plea minute entry"), rico_count=True)
    C("charge-demirtas-2", "demirtas", indictment_s, "Count 2", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending",
      wire_desc + " Not-guilty plea maintained at the 2025-10-14 plea "
      "hearing; pending as of the docket printout. "
      + src_ref("docket", "plea minute entry"))

    # Anand — Second Superseding Indictment (labels 1s, 2s, 3s pending).
    C("charge-anand-1s", "anand", indictment_ss, "Count 1s", 1, RICO[0], RICO[1],
      "conspiracy", "pending", rico_desc + " Pending as of the docket printout.",
      rico_count=True)
    C("charge-anand-2s", "anand", indictment_ss, "Count 2s", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending", wire_desc + " Pending as of the docket printout.")
    C("charge-anand-3s", "anand", indictment_ss, "Count 3s", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "pending", ml_desc + " Pending as of the docket printout.",
      object_offense="charge-anand-2s")

    # Tangeman — Second Superseding Indictment; guilty to Count 1ss.
    C("charge-tangeman-1ss", "tangeman", indictment_ss, "Count 1ss", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Tangeman was arraigned on Counts 1ss and 3ss on "
      "2025-12-08 and pleaded guilty the same day to Count 1ss (the "
      "statement of offense describes it as Count One, RICO "
      "Conspiracy); sentenced 2026-04-24 to 70 months' incarceration, "
      "36 months' supervised release, and a $100 special assessment. "
      "The docket header lists his terminated counts as 1, 3, and 3s. "
      + src_ref("soo", "Summary of the Plea Agreement") + "; "
      + src_ref("docket", "plea and sentencing minute entries"),
      rico_count=True)
    C("charge-tangeman-3ss", "tangeman", indictment_ss, "Count 3ss", 3,
      ML_CONSP[0], ML_CONSP[1], "conspiracy", "dismissed",
      ml_desc + " Dismissed on the government's oral motion at "
      "Tangeman's 2026-04-24 sentencing. "
      + src_ref("docket", "sentencing minute entry"))

    # Cortes — Superseding Indictment.
    C("charge-cortes-1", "cortes", indictment_s, "Count 1", 1, RICO[0], RICO[1],
      "conspiracy", "convicted-by-plea",
      rico_desc + " Cortes pleaded guilty 2025-07-31, the first "
      "defendant to plead. " + src_ref("docket", "plea minute entry"),
      rico_count=True)
    C("charge-cortes-3", "cortes", indictment_s, "Count 3", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "pending",
      ml_desc + " Pending as of the docket printout. "
      + src_ref("docket", "Defendant (11) pending counts"))

    # FNU LNU-1 — Second Superseding Indictment (labels 1s, 2s).
    C("charge-lnu1-1s", "lnu1", indictment_ss, "Count 1s", 1, RICO[0], RICO[1],
      "conspiracy", "pending", rico_desc + " Pending as of the docket printout.",
      rico_count=True)
    C("charge-lnu1-2s", "lnu1", indictment_ss, "Count 2s", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending", wire_desc + " Pending as of the docket printout.")

    # FNU LNU-2 — Superseding Indictment (counts 1, 2, 3).
    C("charge-lnu2-1", "lnu2", indictment_s, "Count 1", 1, RICO[0], RICO[1],
      "conspiracy", "pending", rico_desc + " Pending as of the docket printout.",
      rico_count=True)
    C("charge-lnu2-2", "lnu2", indictment_s, "Count 2", 2, WIRE[0], WIRE[1],
      "conspiracy", "pending", wire_desc + " Pending as of the docket printout.")
    C("charge-lnu2-3", "lnu2", indictment_s, "Count 3", 3, ML_CONSP[0], ML_CONSP[1],
      "conspiracy", "pending", ml_desc + " Pending as of the docket printout.",
      object_offense="charge-lnu2-2")

    # Desmond — Superseding Indictment (count 4 guilty; count 3 dismissed).
    C("charge-desmond-4", "desmond", indictment_s, "Count 4", 4,
      "18 U.S.C. § 1512(c)(1) and (2)", "Obstruction of Justice",
      "substantive", "convicted-by-plea",
      "Tampering with a witness, victim, or an informant — corruptly "
      "destroying evidence: at Tangeman's direction after the Lam and "
      "Serrano arrests, Desmond retrieved electronic devices from Lam's "
      "Los Angeles homes and destroyed them. Pleaded guilty 2025-10-15; "
      "sentenced 2026-03-20 to 36 months' probation and a $100 special "
      "assessment. "
      + src_ref("docket", "Defendant (14); plea and sentencing minute entries") + "; "
      + src_ref("sentmemo", "introduction"))
    C("charge-desmond-3", "desmond", indictment_s, "Count 3", 3, ML_CONSP[0],
      ML_CONSP[1], "conspiracy", "dismissed",
      ml_desc + " Dismissed at Desmond's 2026-03-20 sentencing. "
      + src_ref("docket", "sentencing minute entry"))

    # Zulfiqar, Ibrahim, Dellecave — Second Superseding Indictment
    # (counts 1, 2, 3 pending).
    for key in ("zulfiqar", "ibrahim", "dellecave"):
        C(f"charge-{key}-1", key, indictment_ss, "Count 1", 1, RICO[0], RICO[1],
          "conspiracy", "pending", rico_desc + " Pending as of the docket printout.",
          rico_count=True)
        C(f"charge-{key}-2", key, indictment_ss, "Count 2", 2, WIRE[0], WIRE[1],
          "conspiracy", "pending", wire_desc + " Pending as of the docket printout.")
        C(f"charge-{key}-3", key, indictment_ss, "Count 3", 3, ML_CONSP[0], ML_CONSP[1],
          "conspiracy", "pending", ml_desc + " Pending as of the docket printout.",
          object_offense=f"charge-{key}-2")

    # ------------------------------------------------------------------
    # Enterprise conduct (uco-action:Action). uco-action:performer has
    # max cardinality 1; the primary actor is the performer and
    # co-actors are linked with Participated_In relationships.
    # ------------------------------------------------------------------
    def action(label: str, name: str, description: str, performer: str,
               participants: list[str] | None = None,
               objects: list[str] | None = None,
               instruments: list[str] | None = None,
               loc: str | None = None,
               start: str | None = None, end: str | None = None,
               action_types: list[str] | None = None,
               extra: dict | None = None) -> str:
        node: dict = {
            "@id": uid(label),
            "@type": action_types or "uco-action:Action",
            "uco-core:name": name,
            "uco-core:description": description,
            "uco-action:performer": {"@id": performer},
        }
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
        if extra:
            node.update(extra)
        graph.append(node)
        for p in participants or []:
            rel(p, node["@id"], "Participated_In")
        rel(node["@id"], investigation, "part_of")
        return node["@id"]

    act_conspiracy = action(
        "action-rico-conspiracy",
        "Conduct the affairs of the SE Enterprise through a pattern of racketeering activity",
        "From no later than October 2023 through at least May 2025, the "
        "members and associates of the SE Enterprise agreed to conduct "
        "and participate in the conduct of the enterprise's affairs "
        "through a pattern of racketeering activity spanning the eight "
        "charged predicate categories: hacking and buying "
        "cryptocurrency-holder databases, cold-calling victims while "
        "posing as exchange security staff, stealing virtual currency "
        "from Victim-1 through Victim-9 and others (approximately "
        "$600,000 from Victim-1, $2,900,000 from Victim-2, $870,000 "
        "from Victim-3, $1,740,000 from Victim-5, $14,000,000 from "
        "Victim-6, $5,800,000 from Victim-8, $2,000,000 from Victim-9, "
        "and $245,093,239 from Victim-7), laundering the proceeds, and "
        "obstructing the investigation. "
        + src_ref("indictment_ss", "Count One; overt acts a-vvvv"),
        performer=enterprise,
        start=eastern_midnight("2023-10-01"),
        end=eastern_midnight("2025-05-31"),
    )
    act_v7_theft = action(
        "action-victim7-theft",
        "Steal approximately $245,093,239 in virtual currency from Victim-7",
        "On or about 2024-08-19, Lam, COCONSPIRATOR-1, COCONSPIRATOR-2, "
        "CHEN, and another executed a social-engineering fraud scheme "
        "against Victim-7 while Victim-7 was at his home in Washington, "
        "D.C., convincing him to download a remote desktop connection "
        "program, accessing his computer through it, and stealing "
        "approximately $245,093,239.00 in virtual currency. "
        + src_ref("indictment_ss", "overt acts uu-vv"),
        performer=person_ids["lam"],
        participants=[person_ids["lnu1"]],
        objects=[victim7, victim7_computer],
        instruments=[remote_desktop],
        loc=dc_home,
        start=eastern_midnight("2024-08-19"),
        end=eastern_midnight("2024-08-19"),
    )
    act_v7_laundering = action(
        "action-victim7-laundering",
        "Launder the Victim-7 proceeds through peel chains and chain-hopping into Monero",
        "Following the Victim-7 theft, Lam, COCONSPIRATOR-1, "
        "COCONSPIRATOR-2, and CHEN used sophisticated virtual-currency "
        "laundering techniques to 'clean' the stolen currency, and "
        "Anand assisted COCONSPIRATOR-1 with laundering it on "
        "exchanges known for not requiring identity documents; the "
        "money launderers used exchanges such as Thorswap and eXch to "
        "change stolen cryptocurrency into privacy coins such as Monero "
        "(XMR) to disguise and conceal the location, ownership, and "
        "control of the stolen funds. "
        + src_ref("indictment_ss", "overt acts ww-xx; Count 3 manner and means"),
        performer=person_ids["lam"],
        participants=[person_ids["anand"], person_ids["lnu1"]],
        instruments=[thorswap, exch],
        start=eastern_midnight("2024-08-19"),
        extra={
            "cryptoinv:launderingTechnique": [
                "peel-chain",
                "pass-through-wallets",
                "chain-hopping-to-monero",
                "no-kyc-exchange",
                "crypto-to-cash",
            ]
        },
    )
    action(
        "action-victim4-icloud-monitoring",
        "Monitor Victim-4's location in real time through his Apple iCloud account",
        "In or around July 2024, Lam accessed Victim-4's Apple iCloud "
        "account to monitor Victim-4's location in real time in "
        "preparation for the break-in. "
        + src_ref("indictment_ss", "overt act jj"),
        performer=person_ids["lam"],
        objects=[victim4],
        start=eastern_midnight("2024-07-01"),
        end=eastern_midnight("2024-07-31"),
    )
    act_v4_breakin = action(
        "action-victim4-breakin",
        "Break into Victim-4's New Mexico home in search of hardware wallets",
        "On 2024-07-08, COCONSPIRATOR M.F., in coordination with Lam "
        "and others, broke into Victim-4's home in search of hardware "
        "virtual currency devices, having flown to New Mexico and set "
        "up a telephone with a video camera across from the home to "
        "livestream the break-in so other enterprise members could "
        "alert him if the victim returned. "
        + src_ref("indictment_ss", "overt acts kk-mm"),
        performer=mf,
        participants=[person_ids["lam"]],
        objects=[victim4],
        loc=nm_home,
        start=eastern_midnight("2024-07-08"),
        end=eastern_midnight("2024-07-08"),
    )
    action(
        "action-hesby-house-rental",
        "Procure the Hesby House for Serrano under the fake 'Sean McGarry' identity",
        "Tangeman procured the Los Angeles 'Hesby House' rental for "
        "Serrano under the fabricated identity 'Sean McGarry', "
        "providing $120,800 in cash as upfront payment and security "
        "deposit against $30,000 monthly rent; the lease listed five "
        "fake tenants and McGarry does not exist in any FBI systems. "
        + src_ref("soo", "Hesby House facts") + "; "
        + src_ref("sentmemo", "Hesby House facts"),
        performer=person_ids["tangeman"],
        participants=[person_ids["serrano"]],
        instruments=[fake_id],
        loc=hesby,
        extra={"cryptoinv:launderingTechnique": ["crypto-to-cash", "straw-identity-rental"]},
    )
    act_3m = action(
        "action-3m-crypto-to-cash",
        "Launder approximately $3,000,000 in cryptocurrency for a new Los Angeles rental",
        "On or about 2024-08-25/26, Lam used Tangeman and MONEY "
        "EXCHANGER-1 to launder approximately $3,000,000 in "
        "cryptocurrency to obtain a new Los Angeles rental home; MONEY "
        "EXCHANGER-1 instructed Lam and others to send $550,000 in "
        "cryptocurrency at a time to his USDT address, deducting from "
        "the total owed until approximately $3,000,000 accumulated. "
        "Two days earlier (2024-08-23) Tangeman had directed Lam to "
        "send $337,050 in USDT to Tangeman's 'exchanger', including a "
        "7% commission for unlicensed crypto-to-cash services. "
        + src_ref("indictment_ss", "overt acts zz-aaa") + "; "
        + src_ref("sentmemo", "Statement of Facts quotes"),
        performer=person_ids["tangeman"],
        participants=[person_ids["lam"], me1],
        instruments=[telegram_msg_1, telegram_msg_2],
        start=eastern_midnight("2024-08-25"),
        end=eastern_midnight("2024-08-26"),
        extra={"cryptoinv:launderingTechnique": ["crypto-to-cash", "unlicensed-money-transmission"]},
    )
    action(
        "action-xmr-exchange",
        "Exchange $196,880 through a 'cash guy' Monero address for a rental deposit",
        "In July 2024, arranging another rental home for Lam, Tangeman "
        "requested $196,880 in USDT; when Lam said he didn't have USDT "
        "and asked for an XMR (Monero) address, Tangeman shared his "
        "'cash guy's' XMR address and Lam sent the $196,880. Tangeman "
        "replied 'Waiting for cash atm ... Then going to give it to "
        "her.' " + src_ref("sentmemo", "Statement of Facts quotes"),
        performer=person_ids["tangeman"],
        participants=[person_ids["lam"]],
        start=eastern_midnight("2024-07-01"),
        end=eastern_midnight("2024-07-31"),
        extra={"cryptoinv:launderingTechnique": ["crypto-to-cash", "privacy-coin-conversion"]},
    )
    action(
        "action-nightclub-spending",
        "Spend over $4,000,000 in stolen virtual currency at Los Angeles nightclubs",
        "Between 2024-08-19 and 2024-09-10, Lam and his associates "
        "spent over $4,000,000 in stolen virtual currency at Los "
        "Angeles nightclubs. " + src_ref("indictment_ss", "overt act yy"),
        performer=person_ids["lam"],
        start=eastern_midnight("2024-08-19"),
        end=eastern_midnight("2024-09-10"),
    )
    action(
        "action-phone-toss",
        "Toss mobile telephone into Biscayne Bay ahead of arrest",
        "On or about 2024-09-18, after obtaining information from an "
        "off-duty law enforcement officer that agents were on their way "
        "to arrest him, Lam walked to the rear of his Miami rental home "
        "and tossed his mobile telephone off the boat dock into "
        "Biscayne Bay to destroy incriminating evidence. "
        + src_ref("indictment_ss", "overt acts pppp-qqqq"),
        performer=person_ids["lam"],
        objects=[lam_phone],
        loc=miami,
        start=eastern_midnight("2024-09-18"),
        end=eastern_midnight("2024-09-18"),
    )
    action(
        "action-camera-surveillance",
        "Watch the FBI searches through remote security-camera access",
        "On or about 2024-09-18, while in Los Angeles, Tangeman used "
        "his remote access to the security cameras at Lam's Miami "
        "rental homes to watch FBI agents search the residences and "
        "inventory evidence, taking screenshots and sharing the video. "
        + src_ref("indictment_ss", "overt act rrrr") + "; "
        + src_ref("sentmemo", "Statement of Facts"),
        performer=person_ids["tangeman"],
        instruments=[camera_system],
        start=eastern_midnight("2024-09-18"),
        end=eastern_midnight("2024-09-18"),
    )
    act_destruction = action(
        "action-device-destruction",
        "Destroy co-conspirators' digital devices after the first arrests",
        "Following Lam's 2024-09-18 arrest, Tangeman instructed Desmond "
        "to travel to Lam's Los Angeles homes, retrieve electronic "
        "devices, and destroy them; Desmond followed the directions and "
        "destroyed the devices, to prevent their seizure by law "
        "enforcement and impair their integrity for trial — the conduct "
        "underlying Desmond's Count 4 obstruction conviction and the "
        "obstruction enhancement in Tangeman's guideline calculation. "
        + src_ref("sentmemo", "introduction; Statement of Facts"),
        performer=person_ids["desmond"],
        participants=[person_ids["tangeman"]],
        objects=[destroyed_devices],
        start=eastern_midnight("2024-09-18"),
    )

    rel(act_conspiracy, charge_ids["charge-lam-1ss"], "Relates_To")
    rel(act_v7_theft, charge_ids["charge-lam-2ss"], "Relates_To")
    rel(act_v7_laundering, charge_ids["charge-lam-3ss"], "Relates_To")
    rel(act_3m, charge_ids["charge-tangeman-1ss"], "Relates_To")
    rel(act_destruction, charge_ids["charge-desmond-4"], "Relates_To")
    rel(act_v4_breakin, charge_ids["charge-lam-1ss"], "Relates_To")

    # ------------------------------------------------------------------
    # Law-enforcement actions
    # ------------------------------------------------------------------
    act_search = action(
        "action-fbi-search-miami",
        "Execute search warrants at Lam's two Miami rental homes",
        "On 2024-09-18, FBI agents executed search warrants at Malone "
        "Lam's two rental homes in Miami, searching the residences and "
        "inventorying evidence (watched remotely by Tangeman through "
        "the security camera system). "
        + src_ref("sentmemo", "Statement of Facts"),
        performer=fbi,
        loc=miami,
        start=eastern_midnight("2024-09-18"),
        end=eastern_midnight("2024-09-18"),
        action_types=["case-investigation:InvestigativeAction", "uco-action:Action"],
    )
    act_arrest_lam = action(
        "action-arrest-lam",
        "Arrest Malone Lam in Miami, Florida",
        "Lam was arrested in Florida on 2024-09-18 on an arrest warrant "
        "dated 2024-09-17, returned executed the same day. "
        + src_ref("docket", "entry 5; arrest entries"),
        performer=fbi,
        objects=[person_ids["lam"]],
        loc=miami,
        start=eastern_midnight("2024-09-18"),
        end=eastern_midnight("2024-09-18"),
        action_types=["case-investigation:InvestigativeAction", "uco-action:Action"],
    )
    act_arrest_serrano = action(
        "action-arrest-serrano",
        "Arrest Jeandiel Serrano in Los Angeles, California",
        "Serrano was arrested in Los Angeles, California on 2024-09-18 "
        "on an arrest warrant dated 2024-09-17, returned executed the "
        "same day. " + src_ref("docket", "entry 7; arrest entries"),
        performer=fbi,
        objects=[person_ids["serrano"]],
        start=eastern_midnight("2024-09-18"),
        end=eastern_midnight("2024-09-18"),
        action_types=["case-investigation:InvestigativeAction", "uco-action:Action"],
    )
    act_arrests_ca = action(
        "action-arrests-california",
        "Arrest seven defendants in California on the superseding indictment",
        "On 2025-05-13, following the fourteen-defendant superseding "
        "indictment, Mehta, Flansburg, Cortes, Doost, Ferro, Desmond, "
        "and Tangeman were arrested in California. "
        + src_ref("docket", "arrest entries of 2025-05-13"),
        performer=fbi,
        objects=[person_ids[k] for k in
                 ("mehta", "flansburg", "cortes", "doost", "ferro",
                  "desmond", "tangeman")],
        start=eastern_midnight("2025-05-13"),
        end=eastern_midnight("2025-05-13"),
        action_types=["case-investigation:InvestigativeAction", "uco-action:Action"],
    )
    for a in (act_search, act_arrest_lam, act_arrest_serrano, act_arrests_ca):
        pass  # already linked part_of investigation inside action()

    # ------------------------------------------------------------------
    # Pleas
    # ------------------------------------------------------------------
    pleas = [
        ("cortes", "charge-cortes-1", "2025-07-31",
         "Guilty plea to Count 1 of the Superseding Indictment (RICO "
         "conspiracy) — the first defendant to plead."),
        ("doost", "charge-doost-1", "2025-08-25",
         "Guilty plea to Count 1 (RICO conspiracy); not guilty "
         "maintained on Count 3."),
        ("flansburg", "charge-flansburg-1", "2025-09-26",
         "Guilty plea to Count 1 (RICO conspiracy); not guilty "
         "maintained on Count 2."),
        ("demirtas", "charge-demirtas-1", "2025-10-14",
         "Guilty plea to Count 1 (RICO conspiracy); not guilty "
         "maintained on Count 2."),
        ("desmond", "charge-desmond-4", "2025-10-15",
         "Guilty plea to Count 4 (obstruction of justice); not guilty "
         "maintained on Count 3."),
        ("ferro", "charge-ferro-1", "2025-10-17",
         "Guilty plea to Count 1 (RICO conspiracy); not guilty "
         "maintained on Counts 2 and 3."),
        ("mehta", "charge-mehta-1s", "2025-11-17",
         "Arraignment and guilty plea to the RICO count of the Second "
         "Superseding Indictment on the same day (minute-entry label "
         "Count 1ss)."),
        ("tangeman", "charge-tangeman-1ss", "2025-12-08",
         "Arraignment on Counts 1ss and 3ss and guilty plea to Count "
         "1ss the same day, supported by a Statement of Offense (Doc "
         "257) and Plea Agreement (Doc 258); jury-trial waiver "
         "approved."),
        ("yarally", "charge-yarally-1s", "2026-01-08",
         "Guilty plea to Count 1s (RICO conspiracy); not guilty "
         "maintained on Count 2s."),
    ]
    for key, charge_label, date, desc in pleas:
        pid = uid(f"plea-{key}")
        graph.append(
            {
                "@id": pid,
                "@type": ["legalproc:Plea", "uco-core:UcoObject"],
                "uco-core:name": f"{defendants[key][0]} guilty plea ({date})",
                "uco-core:description": (
                    desc + " Entered before Judge Colleen Kollar-Kotelly. "
                    + src_ref("docket", f"plea minute entry of {date}")
                ),
                "legalproc:pleaType": "guilty",
                "legalproc:concernsCharge": [{"@id": charge_ids[charge_label]}],
                "uco-core:objectCreatedTime": lit("xsd:dateTime", eastern_midnight(date)),
            }
        )
        rel(pid, person_ids[key], "Relates_To")
    rel(uid("plea-tangeman"), doc_ids["soo"], "Derived_From")

    # ------------------------------------------------------------------
    # Sentencing: government recommendation (Tangeman) and the three
    # imposed sentences.
    # ------------------------------------------------------------------
    tangeman_rec = uid("sentence-tangeman-recommended")
    graph.append(
        {
            "@id": tangeman_rec,
            "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
            "uco-core:name": "Government sentencing recommendation for Tangeman: 70 months",
            "uco-core:description": (
                "The government's memorandum in aid of sentencing "
                "calculates a Final Offense Level of 27 in Criminal "
                "History Category I (guidelines range 70-87 months, "
                "Zone D): base level from § 2E1.1 via the "
                "money-laundering guideline (+8 for laundered value, +4 "
                "for being in the business of laundering money under "
                "§ 2S1.1(b)(2)(C)), plus a two-level § 3C1.1 obstruction "
                "enhancement for directing Desmond to destroy digital "
                "devices, with acceptance-of-responsibility credit; "
                "recommends 70 months' incarceration, 36 months' "
                "supervised release, and forfeiture of the luxury "
                "goods. " + src_ref("sentmemo", "guidelines analysis and recommendation")
            ),
            "legalproc:sentenceStatus": "recommended",
            "legalproc:sentenceTerm": (
                "70 months' incarceration + 36 months' supervised "
                "release (guidelines 70-87 months at offense level 27, "
                "CHC I)"
            ),
            "legalproc:concernsCharge": [{"@id": charge_ids["charge-tangeman-1ss"]}],
        }
    )
    rel(tangeman_rec, doc_ids["sentmemo"], "Derived_From")
    rel(tangeman_rec, person_ids["tangeman"], "Relates_To")

    sentencing_hearing = uid("proceeding-tangeman-sentencing")
    graph.append(
        {
            "@id": sentencing_hearing,
            "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
            "uco-core:name": "Tangeman sentencing hearing (2026-04-24)",
            "uco-core:description": (
                "Sentencing before Judge Colleen Kollar-Kotelly; "
                "sentence imposed on Count 1ss, Count 3ss dismissed on "
                "the government's oral motion, and a consent order of "
                "forfeiture entered (Doc 332). "
                + src_ref("docket", "sentencing minute entry; entry 332")
            ),
            "legalproc:proceedingType": "sentencing-hearing",
            "uco-core:objectCreatedTime": lit("xsd:dateTime", eastern_midnight("2026-04-24")),
        }
    )

    imposed = [
        ("desmond", "charge-desmond-4", "2026-03-20",
         "36 months' probation + $100 special assessment",
         "Sentenced on Count 4 to 36 months' probation and a $100 "
         "special assessment; Count 3 dismissed. Judgment entered "
         "2026-04-13 (Doc 327)."),
        ("tangeman", "charge-tangeman-1ss", "2026-04-24",
         "70 months' incarceration + 36 months' supervised release + $100 special assessment",
         "Sentenced on Count 1ss to 70 months' incarceration followed "
         "by 36 months' supervised release and a $100 special "
         "assessment; Count 3ss dismissed on the government's oral "
         "motion; consent order of forfeiture entered the same day "
         "(Doc 332). Judgment entered 2026-05-05 (Doc 337)."),
        ("ferro", "charge-ferro-1", "2026-05-06",
         "78 months' incarceration + 36 months' supervised release + $100 special assessment",
         "Sentenced on Count 1 to 78 months' incarceration followed by "
         "36 months' supervised release and a $100 special assessment; "
         "Counts 2 and 3 dismissed on the government's oral motion. "
         "Judgment entered 2026-05-07 (Doc 343)."),
    ]
    for key, charge_label, date, term, desc in imposed:
        sid = uid(f"sentence-{key}-imposed")
        graph.append(
            {
                "@id": sid,
                "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
                "uco-core:name": f"Sentence imposed on {defendants[key][0]} ({date})",
                "uco-core:description": (
                    desc + " " + src_ref("docket", f"sentencing minute entry of {date}")
                ),
                "legalproc:sentenceStatus": "imposed",
                "legalproc:sentenceTerm": term,
                "legalproc:concernsCharge": [{"@id": charge_ids[charge_label]}],
            }
        )
        rel(sid, person_ids[key], "Relates_To")
        rel(sid, judge, "Imposed_By")
        rel(sid, doc_ids["docket"], "Derived_From")
    rel(uid("sentence-tangeman-imposed"), sentencing_hearing, "Occurred_During")

    # Tangeman consent order of forfeiture (Doc 332).
    forfeiture_order = uid("forfeiture-tangeman-consent")
    graph.append(
        {
            "@id": forfeiture_order,
            "@type": ["legalproc:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Consent Order of Forfeiture as to Evan Tangeman (Doc 332, 2026-04-24)",
            "uco-core:description": (
                "Consent order of forfeiture entered at Tangeman's "
                "sentencing, covering the luxury goods referenced in the "
                "government's sentencing memorandum (exotic automobiles "
                "received as compensation and luxury goods purchased "
                "with laundering commissions). "
                + src_ref("docket", "entry 332") + "; "
                + src_ref("sentmemo", "introduction")
            ),
            "uco-core:objectCreatedTime": lit("xsd:dateTime", eastern_midnight("2026-04-24")),
        }
    )
    rel(forfeiture_order, person_ids["tangeman"], "Relates_To")
    rel(forfeiture_order, sentencing_hearing, "Occurred_During")

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            # Namespace proposed to CASE in issue #192 (committee decides
            # the final IRI); implemented locally by extensions/legalproc/.
            "legalproc": "https://ontology.caseontology.org/case/criminal/",
            # Local extensions; example.org namespaces are placeholders
            # pending a community namespace decision.
            "rico": "http://example.org/ontology/rico/",
            "cryptoinv": "http://example.org/ontology/cryptoinv/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            # gUFO upper ontology, used via the CDO alignment profile
            # (CDO-Shapes-gufo) for physical forfeiture items without
            # extension classes (vehicle, bulk cash).
            "gufo": "http://purl.org/nemo/gufo#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }


def refresh_source_hashes() -> None:
    """Recompute SHA256s from the PDFs sitting next to this script."""
    import hashlib

    here = Path(__file__).resolve().parent
    for meta in SOURCE_DOCS.values():
        pdf = here / meta["file_name"]
        if pdf.exists():
            meta["sha256"] = hashlib.sha256(pdf.read_bytes()).hexdigest()


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    exts = ["legalproc", "rico", "cryptoinv"]
    report = validate_graph_file(path, extensions=exts, project_root=ROOT)
    print(report.safe_summary)
    for ext in exts:
        paths = load_extension_ontology_paths(ext, mode="full", project_root=ROOT)
        print(f"Validated with {len(paths)} {ext} ontology files")
    return 0 if report.conforms else 1


def main() -> int:
    refresh_source_hashes()
    payload = build_graph()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Graph nodes: {len(payload['@graph'])}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
