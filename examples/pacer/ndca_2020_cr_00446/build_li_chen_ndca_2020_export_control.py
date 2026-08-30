#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Han Li and Lin Chen (N.D. Cal. export control).

Case 3:20-cr-00446-WHA (N.D. Cal., San Francisco, Judge William Alsup):
federal export-control prosecution under the International Emergency
Economic Powers Act (IEEPA). PRC nationals Han Li (a/k/a Li Han Anson) and
Lin Chen, acting for the Nanjing-based intermediary Jiangsu Hantang
International Trade Group Co., Ltd. ("JHI", a/k/a Sainty Hantang), procured
a DTX-150 Automatic Diamond Scriber Breaker — an EAR99 dual-use wafer
scribe-and-break machine used in semiconductor manufacture — from
"Company-1" (Dynatex Corporation, Santa Rosa, California) and caused its
December 2015 export to Chengdu GaStone Technology Co., Ltd., a PRC entity
on the Department of Commerce Entity List since 2014-08-01, by falsely
listing JHI as the ultimate consignee/end user on the export paperwork and
stating no license was required. Indicted under seal 2020-12-01 (four
counts); unsealed 2024-04-24; Chen was arrested entering the United States,
pleaded guilty to Count Four (willful IEEPA violation), and was sentenced
2025-01-28 to 4 months custody, 1 year supervised release, and a $5,000
fine, with Counts 1-3 dismissed on government motion. Han Li's counts
remain pending. Dynatex itself pleaded guilty to an IEEPA violation in
United States v. Dynatex Corp., 3:21-cr-00360-CRB ($100,000 fine).

Sources (PACER, N.D. Cal.):
  - Docket sheet (retrieved 2026-06-27)
  - Indictment: Document 1 (filed under seal 2020-12-01) — four counts
  - Government's Sentencing Memorandum: Document 48 (filed 2025-01-21)

MCP extraction artifacts: examples/pacer/ndca_2020_cr_00446/mcp_outputs/
(the indictment PDF carries CID-mapped text that strips digits under
pdftotext; the body was re-OCRed at 300dpi for accurate dates).

Extension: extensions/legalproc — exercised here on per-defendant charge
nodes for shared counts (Chen: three dismissals + one conviction-by-plea;
Li: four pending), a recommended-vs-imposed sentence pair that diverges
sharply (government sought 27 months / $255,000; court imposed 4 months /
$5,000), an arrest-warrant Authorization, and a forfeiture allegation.

Export-control modeling conventions (docs/recipes/export-control-sanctions.md):
  - Entity List designations are dated regulatory Actions by the
    Department of Commerce with the designated Organization as object;
    the designation dates gate what conduct was unlawful when.
  - The DTX-150 machine and its consumables are physical manufacturing
    goods that never live in cyberspace: uco-core:UcoObject dual-typed
    with gufo:FunctionalComplex. Its EAR99 classification is recorded in
    the description (it is a regulatory classification of a physical
    item, not a data marking).
  - The false Electronic Export Information (EEI) filed through the
    Automated Export System (AES) is a cyber observable — an electronic
    record whose false statements (consignee, no-license-required) are
    the charged conduct of Count Two.
  - Court dates are date-only facts rendered at local midnight Pacific
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

CASE_ID = "li-chen-ndca-2020-export-control"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "li-chen-ndca-2020-export-control.jsonld"

PACER_DOCKET = "3:20-cr-00446-WHA"
LOCAL_REF = "outside_pacer -- export control"

SOURCE_DOCS = {
    "docket": {
        "file_name": "pacer -- export control -- docket.pdf",
        "sha256": "1af610901cbae8056d9d1af420e3fa16ce220dac5b9e1a3a193742df1606927e",
        "pacer_doc": "docket sheet",
        "filed": "2026-06-27",
    },
    "indictment": {
        "file_name": "pacer -- export control -- indictment.pdf",
        "sha256": "280f19ce34ce6d162cd163ea3e6d6bb96a310c0eb3bf4ae8c11dc29c7aa2ad40",
        "pacer_doc": "1",
        "filed": "2020-12-01",
    },
    "sentencing_memorandum": {
        "file_name": "pacer -- export control -- sentencing memorandum.pdf",
        "sha256": "ad2f61a77f80e5c66e937c66d6bbb3ab615ebf089cb841c2176f99d5afea4b46",
        "pacer_doc": "48",
        "filed": "2025-01-21",
    },
}

# ---------------------------------------------------------------------------
# The four charged counts (Indictment paras. 19-28; docket count chart).
# Both defendants are charged on all four counts; dispositions diverge.
# ---------------------------------------------------------------------------
COUNTS = [
    {
        "num": 1,
        "label": "Count 1",
        "name": "Conspiracy to Violate IEEPA",
        "statute": "50 U.S.C. § 1705 and 15 C.F.R. § 764.2(d)",
        "offense_form": "conspiracy",
        "desc": (
            "Beginning no later than May 13, 2015, and continuing through "
            "at least August 13, 2018, Li, Chen, and others conspired to "
            "export, re-export, and supply goods and services from the "
            "United States to Chengdu GaStone Technology Co. and other "
            "end users in the PRC without a license and in violation of "
            "the DOC Entity List. Objects: purchase items from the United "
            "States and ship them to Entity List entities through "
            "intermediary companies such as JHI to conceal the nature of "
            "the exports and the true end users."
        ),
    },
    {
        "num": 2,
        "label": "Count 2",
        "name": "Unlawful Export Information Activities",
        "statute": "13 U.S.C. § 305 and 18 U.S.C. § 2",
        "offense_form": "substantive",
        "desc": (
            "On or about December 4, 2015, Li and Chen knowingly "
            "submitted and caused submission of false and misleading "
            "electronic export information (EEI) through the Automated "
            "Export System (AES), stating no license was required and "
            "that the ultimate consignee for the export of a DTX-150 "
            "Automatic Diamond Scriber Breaker was Jiangsu Hantang "
            "International Trade Group Corp. Ltd. in Nanjing, when the "
            "true ultimate end user and consignee was Chengdu GaStone "
            "Technology Co."
        ),
    },
    {
        "num": 3,
        "label": "Count 3",
        "name": "Smuggling of Goods",
        "statute": "18 U.S.C. §§ 554 and 2",
        "offense_form": "substantive",
        "desc": (
            "On or about December 10, 2015, Li and Chen knowingly and "
            "fraudulently exported and sent, and attempted to export and "
            "send, from the United States indirectly to Chengdu GaStone "
            "Technology Co., Ltd. in the PRC a DTX-150 Automatic Diamond "
            "Scriber Breaker, contrary to law and regulation, by "
            "submitting false and misleading export information in an "
            "SED and through the AES."
        ),
    },
    {
        "num": 4,
        "label": "Count 4",
        "name": "Willful Violations of IEEPA",
        "statute": "50 U.S.C. § 1705, 18 U.S.C. § 2, and 15 C.F.R. §§ 764.2(a), (b), (c), (e)",
        "offense_form": "substantive",
        "desc": (
            "On or about December 10, 2015, Li and Chen willfully "
            "exported, re-exported, and supplied, caused and aided and "
            "abetted the export of, a DTX-150 Automatic Diamond Scriber "
            "Breaker from the United States to Chengdu GaStone "
            "Technology Co., Ltd. in the PRC without first obtaining the "
            "required licenses from the U.S. Department of Commerce. "
            "Chen pleaded guilty to this count on 2024-10-17."
        ),
    },
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


def rel(source: str, target: str, kind: str, directional: bool = True) -> dict:
    return {
        "@id": uid(f"rel-{source}-{target}-{kind}"),
        "@type": "uco-core:Relationship",
        "uco-core:source": [{"@id": source}],
        "uco-core:target": [{"@id": target}],
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": lit("xsd:boolean", directional),
    }


def pacific_midnight(date_str: str) -> str:
    """Date-only court fact rendered at local midnight Pacific time."""
    month = int(date_str.split("-")[1])
    offset = "-07:00" if 4 <= month <= 10 else "-08:00"
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
            f"{PACER_DOCKET} (N.D. Cal.); local bundle '{LOCAL_REF}'."
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

    # ------------------------------------------------------------------
    # Investigation container and source documents
    # ------------------------------------------------------------------
    investigation = uid("investigation")
    graph.append(
        {
            "@id": investigation,
            "@type": "case-investigation:Investigation",
            "uco-core:name": f"United States v. Han Li and Lin Chen, {PACER_DOCKET} (N.D. Cal.)",
            "legalproc:caseIdentifier": PACER_DOCKET,
            "uco-core:description": (
                "IEEPA export-control prosecution before Judge William "
                "Alsup. PRC nationals Han Li (a/k/a Li Han Anson) and Lin "
                "Chen, through the Nanjing intermediary JHI, procured a "
                "DTX-150 Automatic Diamond Scriber Breaker (an EAR99 "
                "dual-use wafer scribe-and-break machine) from Dynatex "
                "Corporation of Santa Rosa, California, and caused its "
                "December 2015 export to Chengdu GaStone Technology Co., "
                "Ltd. — on the DOC Entity List since 2014-08-01 — by "
                "falsely listing JHI as ultimate consignee/end user and "
                "stating no license was required. Indicted under seal "
                "2020-12-01; unsealed 2024-04-24. Chen was arrested "
                "entering the United States on 2024-04-23, pleaded guilty "
                "to Count Four on 2024-10-17, and was sentenced "
                "2025-01-28 to 4 months custody, 1 year supervised "
                "release, and a $5,000 fine; Counts 1-3 were dismissed on "
                "government motion. Han Li's four counts remain pending. "
                "FBI was the complainant agency."
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
    li = uid("person-han-li")
    chen = uid("person-lin-chen")
    jhi = uid("org-jhi")
    gastone = uid("org-gastone")
    cetc55 = uid("org-cetc55")
    dynatex = uid("org-dynatex")
    doc_bis = uid("org-doc-bis")
    fbi = uid("org-fbi")
    usao = uid("org-usao-ndca")
    doj_nsd = uid("org-doj-nsd")
    cbp = uid("org-dhs-cbp")

    graph.extend(
        [
            {
                "@id": li,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Han Li, a/k/a Li Han Anson",
                "uco-core:description": (
                    "Defendant (1). PRC citizen. Emailed co-defendant "
                    "Chen that 'GaStone [is] listed in the black list' "
                    "and therefore could not be listed on the master "
                    "waybill for the DTX-150. All four counts remain "
                    "pending; the docket lists no counsel appearance and "
                    "no disposition. "
                    + src_ref("indictment", "para. 4")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 7 (PSR para. 12)")
                ),
            },
            {
                "@id": chen,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Lin Chen",
                "uco-core:description": (
                    "Defendant (2). PRC citizen; engineer by education; "
                    "listed as JHI's 'Chief Representative' on a May 2015 "
                    "invitation letter to Dynatex and signed a 2018 "
                    "distributor agreement as JHI's 'Import Manager'. "
                    "Acted as importer, falsely posing JHI as end user of "
                    "the DTX-150 while the true end user was Entity List "
                    "designee GaStone; earned JHI commissions. Arrested "
                    "attempting to enter the United States on 2024-04-23; "
                    "pleaded guilty to Count Four; sentenced 2025-01-28. "
                    + src_ref("indictment", "para. 5")
                    + "; "
                    + src_ref("sentencing_memorandum", "pp. 2-3, 7-8")
                ),
            },
            {
                "@id": jhi,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Jiangsu Hantang International Trade Group Co., Ltd. (JHI, a/k/a Sainty Hantang)",
                "uco-core:description": (
                    "Intermediary trading company headquartered in "
                    "Nanjing, PRC; Chen's employer. Placed in the middle "
                    "of the DTX-150 transaction and falsely listed as "
                    "ultimate consignee/end user on the contract and "
                    "export paperwork to conceal GaStone's involvement. "
                    + src_ref("indictment", "para. 3")
                    + "; "
                    + src_ref("sentencing_memorandum", "pp. 7-8")
                ),
            },
            {
                "@id": gastone,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Chengdu GaStone Technology Co., Ltd.",
                "uco-core:description": (
                    "PRC entity in Chengdu; true end user of the DTX-150. "
                    "Designated on the DOC Entity List on 2014-08-01 for "
                    "'involvement in activities contrary to the national "
                    "security and foreign policy interests of the United "
                    "States'; all items subject to the EAR required a "
                    "license for export to GaStone. "
                    + src_ref("indictment", "paras. 1, 16")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 5")
                ),
            },
            {
                "@id": cetc55,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "China Electronics Technology Group Corporation 55th Research Institute (CETC 55)",
                "uco-core:description": (
                    "PRC entity in Jiangsu; designated on the DOC Entity "
                    "List on 2018-08-01. Identified as the true end user "
                    "on another JHI-facilitated Dynatex sale (a 2015 "
                    "DTX-150 sale, before CETC 55's designation). "
                    + src_ref("indictment", "paras. 2, 17")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 2 n.1")
                ),
            },
            {
                "@id": dynatex,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Dynatex Corporation ('Company-1'), Santa Rosa, California",
                "uco-core:description": (
                    "Semiconductor-industry supplier that designed and "
                    "sold machines for processing silicon wafer "
                    "microchips, including the DTX-150 Automatic Diamond "
                    "Scriber Breaker. Referred to as 'Company-1' in the "
                    "indictment; named in the sentencing memorandum. For "
                    "its part in the export to GaStone, Dynatex pleaded "
                    "guilty to an IEEPA violation in United States v. "
                    "Dynatex Corp., 3:21-cr-00360-CRB, and paid a "
                    "$100,000 fine. "
                    + src_ref("indictment", "para. 6")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 7")
                ),
            },
            {
                "@id": doc_bis,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Department of Commerce, Bureau of Industry and Security (BIS)",
                "uco-core:description": (
                    "Administers the Export Administration Regulations "
                    "(EAR, 15 C.F.R. §§ 730-774) under IEEPA authority "
                    "(E.O. 13222, continued annually; permanent statutory "
                    "authority under the Export Control Reform Act of "
                    "2018), including the Commerce Control List and the "
                    "Entity List (15 C.F.R. § 774 Supp. No. 4). Licensing "
                    "authority whose approval was never sought for the "
                    "GaStone export. " + src_ref("indictment", "paras. 7-11")
                ),
            },
            {
                "@id": cbp,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. DHS Customs and Border Protection (CBP)",
                "uco-core:description": (
                    "Administers the Automated Export System (AES) "
                    "through which Shipper's Export Declarations and "
                    "Electronic Export Information are filed. "
                    + src_ref("indictment", "para. 12")
                ),
            },
            {
                "@id": fbi,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Federal Bureau of Investigation",
                "uco-core:description": (
                    "Complainant agency on the indictment (AO 257 "
                    "defendant information sheets). "
                    + src_ref("indictment", "AO 257 attachments")
                ),
            },
            {
                "@id": usao,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Attorney's Office, Northern District of California",
                "uco-core:description": (
                    "Prosecuting office (AUSA Colin Sampson; U.S. "
                    "Attorneys David L. Anderson at indictment, Ismail J. "
                    "Ramsey at sentencing). "
                    + src_ref("sentencing_memorandum", "signature block")
                ),
            },
            {
                "@id": doj_nsd,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Department of Justice, National Security Division",
                "uco-core:description": (
                    "Co-prosecuting component (Trial Attorney Brett "
                    "Reynolds). "
                    + src_ref("sentencing_memorandum", "signature block")
                ),
            },
        ]
    )
    graph.append(rel(chen, jhi, "Member_Of"))
    graph.append(rel(li, jhi, "Relates_To"))

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------
    santa_rosa = uid("location-santa-rosa")
    chengdu = uid("location-chengdu")
    nanjing = uid("location-nanjing")

    graph.extend(
        [
            {
                "@id": santa_rosa,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Santa Rosa, California",
                "uco-core:description": (
                    "Dynatex's location; Chen traveled from the PRC to "
                    "Santa Rosa to meet the machine's manufacturer before "
                    "the sales contract was signed. "
                    + src_ref("sentencing_memorandum", "p. 2")
                ),
            },
            {
                "@id": chengdu,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Chengdu, People's Republic of China",
                "uco-core:description": (
                    "GaStone's location and the DTX-150's true "
                    "destination. " + src_ref("sentencing_memorandum", "p. 3")
                ),
            },
            {
                "@id": nanjing,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Nanjing / Jiangsu, People's Republic of China",
                "uco-core:description": (
                    "JHI's headquarters (Nanjing) and CETC 55's province "
                    "(Jiangsu); the false paperwork destination. "
                    + src_ref("indictment", "paras. 2-3")
                ),
            },
        ]
    )
    graph.append(rel(dynatex, santa_rosa, "Located_At"))
    graph.append(rel(gastone, chengdu, "Located_At"))
    graph.append(rel(jhi, nanjing, "Located_At"))

    # ------------------------------------------------------------------
    # The controlled goods (physical, gUFO-typed) and cyber observables
    # ------------------------------------------------------------------
    dtx150 = uid("physical-dtx150")
    consumables = uid("physical-consumables")
    eei_filing = uid("obs-false-eei")
    blacklist_email = uid("msg-blacklist-email")
    invitation_letter = uid("obs-invitation-letter")

    graph.extend(
        [
            {
                "@id": dtx150,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "DTX-150 Automatic Diamond Scriber Breaker (EAR99)",
                "uco-core:description": (
                    "Wafer scribe-and-break machine manufactured and sold "
                    "by Dynatex, with applications for radio-frequency "
                    "integrated circuits, optoelectronics devices, and "
                    "LEDs, including dicing of gallium arsenide (GaAs) "
                    "wafers suited to telecommunications and "
                    "optoelectronics. Subject to the EAR and controlled "
                    "for export under classification EAR99 (dual-use: "
                    "potential military and civilian applications). Sold "
                    "for $216,750 (list price $255,000 minus a 15% "
                    "distributor discount) and delivered to GaStone. A "
                    "physical manufacturing machine outside the cyber "
                    "domain, so typed with the gUFO upper ontology; the "
                    "export records about it are the cyber observables. "
                    + src_ref("indictment", "paras. 6, 18")
                    + "; "
                    + src_ref("sentencing_memorandum", "pp. 3, 6-7")
                ),
            },
            {
                "@id": consumables,
                "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
                "uco-core:name": "DTX-150 consumables (scribe tools and lubricants)",
                "uco-core:description": (
                    "Consumables Chen continued to procure from Dynatex "
                    "for GaStone until July 2018. "
                    + src_ref("sentencing_memorandum", "p. 3")
                ),
            },
            {
                "@id": eei_filing,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "False Electronic Export Information (EEI) filed through AES (2015-12-04)",
                "uco-core:description": (
                    "Electronic export information submitted through the "
                    "Automated Export System stating that no license was "
                    "required and that the ultimate consignee of the "
                    "DTX-150 was JHI in Nanjing, when the true ultimate "
                    "end user and consignee was GaStone. EEI contents are "
                    "relied on by the Departments of State, Treasury, and "
                    "Commerce for export-control purposes; 15 C.F.R. § "
                    "764.2(g) prohibits false or misleading statements in "
                    "export control documents. The charged false record "
                    "of Count Two. "
                    + src_ref("indictment", "paras. 12-15, 24-25")
                ),
            },
            {
                "@id": blacklist_email,
                "@type": ["uco-observable:EmailMessage", "uco-core:UcoObject"],
                "uco-core:name": "Han Li email: 'GaStone [is] listed in the black list'",
                "uco-core:description": (
                    "Email from co-defendant Han Li received in Chen's "
                    "email account stating that 'GaStone [is] listed in "
                    "the black list' and therefore could not be listed on "
                    "the master waybill for the device. Chen's counsel "
                    "asserts she does not read English and that team "
                    "members had access to her account; the government "
                    "argues the correspondence supports her willfulness. "
                    + src_ref("sentencing_memorandum", "p. 7 (PSR para. 12 & n.1)")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-blacklist-email"),
                        "@type": "uco-observable:EmailMessageFacet",
                        "uco-observable:body": (
                            "GaStone [is] listed in the black list"
                        ),
                    }
                ],
            },
            {
                "@id": invitation_letter,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "JHI invitation letter to Dynatex (May 2015)",
                "uco-core:description": (
                    "Invitation letter sent to Dynatex in May 2015 "
                    "listing Chen as JHI's 'Chief Representative' — part "
                    "of the pre-contract relationship building, including "
                    "Chen's travel to Santa Rosa and arranging Dynatex "
                    "employees' travel to the PRC. "
                    + src_ref("sentencing_memorandum", "pp. 2, 7")
                ),
            },
        ]
    )
    graph.append(rel(dtx150, gastone, "Owned_By"))
    graph.append(rel(consumables, gastone, "Owned_By"))

    # ------------------------------------------------------------------
    # Entity List designations as dated regulatory actions
    # ------------------------------------------------------------------
    act_designate_gastone = uid("act-designate-gastone")
    act_designate_cetc = uid("act-designate-cetc55")

    graph.extend(
        [
            {
                "@id": act_designate_gastone,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "DOC designates GaStone on the Entity List (2014-08-01)",
                "uco-core:description": (
                    "Bureau of Industry and Security added GaStone to the "
                    "Entity List (15 C.F.R. § 774 Supp. No. 4) citing "
                    "'involvement in activities contrary to the national "
                    "security and foreign policy interests of the United "
                    "States'; thereafter all EAR-subject items required a "
                    "license for export to GaStone. This designation "
                    "predates the charged export by over a year and gates "
                    "the unlawfulness of the December 2015 shipment. "
                    + src_ref("indictment", "para. 16")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 5")
                ),
                "uco-action:performer": {"@id": doc_bis},
                "uco-action:object": [{"@id": gastone}],
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2014-08-01")),
            },
            {
                "@id": act_designate_cetc,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "DOC designates CETC 55 on the Entity List (2018-08-01)",
                "uco-core:description": (
                    "CETC 55 was designated on the DOC Entity List on "
                    "2018-08-01; the earlier JHI-facilitated sale to CETC "
                    "55 (2015) predated the designation and was not "
                    "subject to a license requirement at that time. "
                    + src_ref("indictment", "para. 17")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 2 n.1")
                ),
                "uco-action:performer": {"@id": doc_bis},
                "uco-action:object": [{"@id": cetc55}],
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2018-08-01")),
            },
        ]
    )

    # ------------------------------------------------------------------
    # The charged conduct as Actions
    # ------------------------------------------------------------------
    act_conspiracy = uid("act-conspiracy")
    act_relationship = uid("act-relationship-building")
    act_false_eei = uid("act-false-eei-filing")
    act_export = uid("act-export-dtx150")
    act_consumables = uid("act-consumables-procurement")

    graph.extend(
        [
            {
                "@id": act_conspiracy,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": (
                    "Li/Chen conspiracy: procure U.S. goods for Entity List "
                    "end users through intermediaries (2015-05-13 to 2018-08-13)"
                ),
                "uco-core:description": (
                    "Course of conduct grounding Count One: identify "
                    "devices needed by prohibited PRC client entities, "
                    "purchase them, arrange shipment through intermediary "
                    "entities they controlled (including JHI) listed as "
                    "destination entities on paperwork to conceal the "
                    "true end users, communicate by email with U.S. "
                    "companies including Dynatex, and route payments from "
                    "financial institutions outside the United States to "
                    "U.S. financial institutions to fund the purchases. "
                    + src_ref("indictment", "paras. 20-23")
                ),
                "uco-action:performer": {"@id": li},
                "uco-action:object": [{"@id": dtx150}],
                "uco-action:result": [{"@id": eei_filing}],
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2015-05-13")),
                "uco-action:endTime": lit("xsd:dateTime", pacific_midnight("2018-08-13")),
            },
            {
                "@id": act_relationship,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Chen builds the Dynatex relationship (May 2015 onward)",
                "uco-core:description": (
                    "Chen traveled from the PRC to Santa Rosa to meet the "
                    "machine's manufacturer and arranged for Dynatex "
                    "employees to travel to the PRC in the months before "
                    "the sales contract was signed; the May 2015 "
                    "invitation letter lists her as JHI's 'Chief "
                    "Representative'. She later corresponded by email "
                    "with Dynatex about price, terms, and delivery "
                    "instructions for the machine destined for Chengdu. "
                    + src_ref("sentencing_memorandum", "pp. 2-3")
                ),
                "uco-action:performer": {"@id": chen},
                "uco-action:object": [{"@id": invitation_letter}],
                "uco-action:location": {"@id": santa_rosa},
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2015-05-13")),
            },
            {
                "@id": act_false_eei,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "False EEI submitted through AES naming JHI as ultimate consignee (2015-12-04)",
                "uco-core:description": (
                    "Li and Chen knowingly submitted and caused "
                    "submission of false and misleading EEI through AES, "
                    "stating no license was required and naming JHI as "
                    "ultimate consignee when the true end user was "
                    "GaStone. Grounds Count Two and supplies the "
                    "'contrary to law' element of Count Three. "
                    + src_ref("indictment", "paras. 24-25")
                ),
                "uco-action:performer": {"@id": chen},
                "uco-action:instrument": [{"@id": cbp}],
                "uco-action:result": [{"@id": eei_filing}],
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2015-12-04")),
            },
            {
                "@id": act_export,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "DTX-150 exported from the United States to GaStone via JHI (2015-12-10)",
                "uco-core:description": (
                    "The DTX-150 was fraudulently exported from the "
                    "United States indirectly to GaStone in Chengdu, "
                    "without the required DOC license, with JHI papered "
                    "as the destination. Delivered to GaStone for "
                    "$216,750. Grounds Counts Three and Four. "
                    + src_ref("indictment", "paras. 26-28")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 3")
                ),
                "uco-action:performer": {"@id": chen},
                "uco-action:object": [{"@id": dtx150}],
                "uco-action:location": {"@id": chengdu},
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2015-12-10")),
            },
            {
                "@id": act_consumables,
                "@type": ["uco-action:Action", "uco-core:UcoObject"],
                "uco-core:name": "Chen procures DTX-150 consumables for GaStone (until July 2018)",
                "uco-core:description": (
                    "After delivery, Chen continued to correspond with "
                    "and procure consumables like scribe tools and "
                    "lubricants from Dynatex for GaStone until July 2018. "
                    + src_ref("sentencing_memorandum", "p. 3")
                ),
                "uco-action:performer": {"@id": chen},
                "uco-action:object": [{"@id": consumables}],
                "uco-action:endTime": lit("xsd:dateTime", pacific_midnight("2018-07-31")),
            },
        ]
    )

    # ------------------------------------------------------------------
    # Arrest with warrant Authorization
    # ------------------------------------------------------------------
    warrant = uid("authorization-arrest-warrant")
    ia_arrest = uid("ia-arrest-chen")

    graph.extend(
        [
            {
                "@id": warrant,
                "@type": ["case-investigation:Authorization", "uco-core:UcoObject"],
                "uco-core:name": "Arrest warrant for Lin Chen (issued with sealed indictment, 2020-12-01)",
                "uco-core:description": (
                    "Arrest warrant issued with the sealed indictment "
                    "('Bail: $ Arrest Warrant' on the indictment cover); "
                    "returned executed 2024-04-24 (Docket No. 15). "
                    + src_ref("docket", "entry 15")
                ),
            },
            {
                "@id": ia_arrest,
                "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
                "uco-core:name": "Lin Chen arrested entering the United States (2024-04-23)",
                "uco-core:description": (
                    "Chen was arrested as she attempted to enter the "
                    "United States on 2024-04-23 (warrant returned "
                    "executed 2024-04-24); initially held in the Northern "
                    "District of Illinois (Chicago), then transferred "
                    "under Rule 5(c)(3). Arraigned 2024-05-10 (not guilty, "
                    "all counts); released 2024-05-13 on a $200,000 bond "
                    "with $100,000 security, passport surrendered, "
                    "electronic monitoring, and a two-mile airport "
                    "stand-off condition. "
                    + src_ref("sentencing_memorandum", "p. 3")
                    + "; "
                    + src_ref("docket", "entries 5-15")
                ),
                "uco-action:performer": {"@id": fbi},
                "uco-action:object": [{"@id": chen}],
                "case-investigation:relevantAuthorization": [{"@id": warrant}],
                "uco-action:startTime": lit("xsd:dateTime", pacific_midnight("2024-04-23")),
            },
        ]
    )
    graph.append(rel(ia_arrest, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Charging instrument (sealed indictment, later unsealed)
    # ------------------------------------------------------------------
    indictment = uid("instrument-indictment")
    graph.append(
        {
            "@id": indictment,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "Indictment, Doc 1 (filed under seal 2020-12-01; unsealed 2024-04-24)",
            "legalproc:instrumentType": "indictment",
            "uco-core:description": (
                "Four counts against both defendants: conspiracy to "
                "violate IEEPA, unlawful export information activities, "
                "smuggling of goods, and willful IEEPA violations, plus a "
                "criminal forfeiture allegation. Filed under seal on "
                "2020-12-01 (sealing order, Magistrate Judge Laurel "
                "Beeler); unsealed on government application 2024-04-24 "
                "(Magistrate Judge Alex G. Tse), the day after Chen's "
                "arrest. " + src_ref("docket", "entries 1-4")
            ),
        }
    )
    graph.append(rel(indictment, doc_ids["indictment"], "Derived_From"))
    graph.append(rel(indictment, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Per-defendant charges (shared counts, divergent dispositions)
    # ------------------------------------------------------------------
    chen_charge_ids: list[str] = []
    li_charge_ids: list[str] = []
    for item in COUNTS:
        n = item["num"]
        for defendant, person_id, charge_list, disposition in (
            ("chen", chen, chen_charge_ids,
             "convicted-by-plea" if n == 4 else "dismissed"),
            ("li", li, li_charge_ids, "pending"),
        ):
            label = f"charge-{defendant}-count{n}"
            charge_list.append(uid(label))
            disposition_note = {
                "convicted-by-plea": (
                    " Chen pleaded guilty to this count on 2024-10-17."
                ),
                "dismissed": (
                    " Dismissed as to Chen by government oral motion at "
                    "sentencing on 2025-01-28."
                ),
                "pending": " Pending as to Han Li; no disposition on the docket.",
            }[disposition]
            graph.append(
                {
                    "@id": uid(label),
                    "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                    "uco-core:name": (
                        f"{item['label']} ({defendant.title()}): {item['name']} "
                        f"({item['statute']})"
                    ),
                    "legalproc:statuteCitation": item["statute"],
                    "legalproc:countNumber": lit("xsd:nonNegativeInteger", n),
                    "legalproc:countLabel": item["label"],
                    "legalproc:offenseForm": item["offense_form"],
                    "legalproc:chargeDisposition": disposition,
                    "legalproc:assertedIn": [{"@id": indictment}],
                    "uco-core:description": item["desc"] + disposition_note + " "
                    + src_ref("indictment", "counts") + "; "
                    + src_ref("docket", "count chart"),
                }
            )
            graph.append(rel(person_id, uid(label), "Charged_With"))

    # Conspiracy count links to the object offense (the willful IEEPA count)
    for defendant, charge_list in (("chen", chen_charge_ids), ("li", li_charge_ids)):
        graph.append(
            {
                "@id": uid(f"charge-{defendant}-count1"),
                "legalproc:objectOffense": [{"@id": uid(f"charge-{defendant}-count4")}],
            }
        )

    # Wire conduct to counts
    for charge_list in (chen_charge_ids, li_charge_ids):
        graph.append(rel(act_conspiracy, charge_list[0], "Basis_Of"))
        graph.append(rel(act_false_eei, charge_list[1], "Basis_Of"))
        graph.append(rel(act_export, charge_list[2], "Basis_Of"))
        graph.append(rel(act_export, charge_list[3], "Basis_Of"))
        for cid in charge_list:
            graph.append(rel(cid, dtx150, "Concerns"))

    # ------------------------------------------------------------------
    # Forfeiture allegation
    # ------------------------------------------------------------------
    forfeiture = uid("forfeiture-allegation")
    graph.append(
        {
            "@id": forfeiture,
            "@type": ["legalproc:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Forfeiture allegation (18 U.S.C. § 981(a)(1)(C), 28 U.S.C. § 2461(c), 13 U.S.C. § 305(a)(3))",
            "uco-core:description": (
                "Upon conviction of Counts One, Three, or Four: any "
                "property constituting or derived from proceeds traceable "
                "to the violations. Upon conviction of Count Two (13 "
                "U.S.C. § 305(a)(3)): interests in the goods that were "
                "the subject of the violation, tangible property used in "
                "the export, and proceeds; with substitute-assets "
                "provision (21 U.S.C. § 853(p)). "
                + src_ref("indictment", "forfeiture allegation")
            ),
            "legalproc:concernsCharge": [
                {"@id": cid} for cid in chen_charge_ids + li_charge_ids
            ],
        }
    )
    graph.append(rel(forfeiture, indictment, "Contained_Within"))

    # ------------------------------------------------------------------
    # Chen's plea and proceedings
    # ------------------------------------------------------------------
    plea = uid("plea-chen-guilty")
    arraignment = uid("proceeding-arraignment")
    plea_hearing = uid("proceeding-plea-hearing")
    sentencing_hearing = uid("proceeding-sentencing")

    graph.extend(
        [
            {
                "@id": arraignment,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Arraignment of Lin Chen (2024-05-10)",
                "legalproc:proceedingType": "arraignment",
                "uco-core:description": (
                    "Chen arraigned before Magistrate Judge Sallie Kim; "
                    "not-guilty plea entered on all four counts; Mandarin "
                    "interpreter required; remanded pending the "
                    "2024-05-13 detention hearing at which a $200,000 "
                    "appearance bond issued. "
                    + src_ref("docket", "entries 6-10")
                ),
            },
            {
                "@id": plea,
                "@type": ["legalproc:Plea", "uco-core:UcoObject"],
                "uco-core:name": "Lin Chen guilty plea to Count Four (2024-10-17)",
                "legalproc:pleaType": "guilty",
                "legalproc:concernsCharge": [{"@id": chen_charge_ids[3]}],
                "uco-core:description": (
                    "Chen pleaded guilty to a single count of willful "
                    "violation of IEEPA (Count Four) before Judge Alsup "
                    "on 2024-10-17 (plea agreements at Docs 35-36, dated "
                    "10/15 and 10/17). "
                    + src_ref("docket", "entries 33-36")
                    + "; "
                    + src_ref("sentencing_memorandum", "p. 3")
                ),
            },
            {
                "@id": plea_hearing,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Change-of-plea hearing (2024-10-17)",
                "legalproc:proceedingType": "plea-hearing",
                "uco-core:description": (
                    "Change of plea before Judge Alsup; Mandarin "
                    "interpreter Amanda Peeters sworn; sentencing set for "
                    "2025-01-28. " + src_ref("docket", "entry 34")
                ),
            },
            {
                "@id": sentencing_hearing,
                "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
                "uco-core:name": "Sentencing hearing (2025-01-28)",
                "legalproc:proceedingType": "sentencing-hearing",
                "uco-core:description": (
                    "Sentencing before Judge Alsup. Counts 1-3 dismissed "
                    "as to Chen by government oral motion. Court imposed "
                    "4 months BOP custody on Count 4, 1 year supervised "
                    "release ('but likely deported'), a $5,000 fine, and "
                    "a $100 special assessment, strongly recommending FCI "
                    "Waseca (Minnesota) or a facility with ready access "
                    "to a Mandarin interpreter given the defendant's "
                    "impaired health. Judgment entered 2025-02-03. "
                    + src_ref("docket", "entries 54-55")
                ),
            },
        ]
    )
    graph.append(rel(plea, plea_hearing, "Occurred_During"))
    graph.append(rel(plea, chen, "Relates_To"))
    for p in (arraignment, plea_hearing, sentencing_hearing):
        graph.append(rel(p, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Recommended vs. imposed sentence (sharply divergent)
    # ------------------------------------------------------------------
    sentence_recommended = uid("sentence-chen-recommended")
    sentence_imposed = uid("sentence-chen-imposed")

    graph.extend(
        [
            {
                "@id": sentence_recommended,
                "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
                "uco-core:name": "Government recommendation: 27 months, $255,000 fine (2025-01-21)",
                "legalproc:sentenceStatus": "recommended",
                "legalproc:sentenceTerm": "27 months",
                "legalproc:monetaryAmount": lit("xsd:decimal", "255000"),
                "legalproc:currencyCode": "USD",
                "legalproc:concernsCharge": [{"@id": chen_charge_ids[3]}],
                "uco-core:description": (
                    "Government recommendation: 27 months' imprisonment, "
                    "three years of supervised release, a $100 special "
                    "assessment, and a $255,000 fine (the DTX-150's list "
                    "price). Guidelines: base offense level 26 (USSG § "
                    "2M5.1(a)(1), evasion of national security controls), "
                    "-3 acceptance of responsibility, -2 zero-point "
                    "offender (level 21, range 37-46 months), with a "
                    "further three-level government variance to level 18 "
                    "(27-33 months). Cited United States v. Shih and "
                    "United States v. Soong for § 2M5.1(a)(1) in "
                    "analogous cases, and requested immediate remand. "
                    + src_ref("sentencing_memorandum", "pp. 1, 4-6, 10")
                ),
            },
            {
                "@id": sentence_imposed,
                "@type": ["legalproc:Sentence", "uco-core:UcoObject"],
                "uco-core:name": "Imposed sentence: 4 months custody, 1 year supervised release, $5,000 fine (2025-01-28)",
                "legalproc:sentenceStatus": "imposed",
                "legalproc:sentenceTerm": "4 months",
                "legalproc:monetaryAmount": lit("xsd:decimal", "5000"),
                "legalproc:currencyCode": "USD",
                "legalproc:concernsCharge": [{"@id": chen_charge_ids[3]}],
                "uco-core:description": (
                    "Sentence imposed on Count Four: 4 months BOP "
                    "custody, 1 year supervised release ('but likely "
                    "deported'), $5,000 fine, $100 special assessment; "
                    "FCI Waseca recommended in light of Mandarin "
                    "interpretation needs and the defendant's impaired "
                    "health. Judgment entered 2025-02-03. Special "
                    "assessment paid 2025-03-05; fine of $5,000 plus $25 "
                    "interest paid 2025-07-10; bond exonerated and "
                    "passport returned in 2025. "
                    + src_ref("docket", "entries 54-55, 57, 69")
                ),
            },
        ]
    )
    graph.append(rel(sentence_recommended, doc_ids["sentencing_memorandum"], "Derived_From"))
    graph.append(rel(sentence_recommended, usao, "Relates_To"))
    graph.append(rel(sentence_imposed, doc_ids["docket"], "Derived_From"))
    graph.append(rel(sentence_imposed, sentencing_hearing, "Occurred_During"))

    # ------------------------------------------------------------------
    # Investigation-level wiring
    # ------------------------------------------------------------------
    graph.append(rel(li, investigation, "Subject_Of"))
    graph.append(rel(chen, investigation, "Subject_Of"))
    for org in (fbi, usao, doj_nsd, doc_bis):
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
