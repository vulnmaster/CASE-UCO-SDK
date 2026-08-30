#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Linwei Ding (N.D. Cal. insider threat).

Case 3:24-cr-00141-VC (N.D. Cal., San Francisco): federal prosecution of a
Google software engineer for theft of trade secrets (18 U.S.C. § 1832) and
economic espionage (18 U.S.C. § 1831). Between 2022-05-21 and 2023-05-02,
Ding uploaded more than 1,000 unique files containing Google confidential
information — including seven categories of trade secrets covering Google's
TPU chips and systems, GPU machines and systems, the supercomputing software
platform, and the custom SmartNIC — from Google's network into a personal
Google Cloud account, evading data-loss-prevention monitoring by copying
source material into Apple Notes on his Google-issued MacBook and exporting
the notes as PDFs. While still employed at Google he became CTO of the
PRC-based AI startup Beijing Rongshu Lianzhi Technology, founded and became
CEO of Shanghai Zhisuan Technology, pitched investors at the MiraclePlus
incubator conference in Beijing, applied to a PRC talent program, and
circulated materials citing PRC State Council and Cyberspace Administration
of China AI-development policies. A jury found him guilty on all fourteen
counts on 2026-01-29.

Sources (PACER):
  - Indictment: Document 1 (filed 2024-03-05) — four § 1832 counts
  - Superseding Indictment: Document 44 (filed 2025-02-04) — 14 counts
  - Second Superseding Indictment: Document 140 (filed 2025-09-09) — operative
  - English translation of WeChat thread: Document 191-1 (filed 2025-09-21)
  - Jury Verdict: Document 367 (filed 2026-01-29)

MCP extraction artifacts: examples/pacer/ndca_2024_cr_00141/mcp_outputs/

Extension: extensions/legalproc — exercised here on a superseding-indictment
chain (indictment -> superseding -> second superseding), per-category trade
secret counts, a 14-count jury verdict with per-count unanimous trade-secret
findings, and a criminal forfeiture allegation. Sentencing had not occurred
in the modeled documents, so no Sentence node is asserted.

Cyber vs. non-cyber conventions (docs/recipes/legal-process-modeling.md):
  - This case is almost entirely cyber-domain: the exfiltrated files, trade
    secret categories, personal cloud accounts, the Google-issued MacBook
    and mobile device, the Apple Notes application, the WeChat group thread,
    the resignation email, network/DLP telemetry, and surveillance footage
    are all UCO observables.
  - Ding's physical access badge never lives in cyberspace, so it is
    uco-core:UcoObject dual-typed with gufo:FunctionalComplex; the badge
    *scan records* Google analyzed are cyber observables.
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

CASE_ID = "ding-ndca-2024-insider-threat"
NS = f"https://example.org/legalproc/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "ding-ndca-2024-insider-threat.jsonld"

PACER_DOCKET = "3:24-cr-00141-VC"
LOCAL_REF = "outside_pacer -- insider threat"

SOURCE_DOCS = {
    "indictment": {
        "file_name": "pacer -- insider threat -- indictment.pdf",
        "sha256": "e85dda80cacaf7c44bec28b5eef1a75430f4bc5444ef582151815d83afc52ad0",
        "pacer_doc": "1",
        "filed": "2024-03-05",
    },
    "superseding_indictment": {
        "file_name": "pacer -- insider threat -- superseding indictment.pdf",
        "sha256": "2cdb77c1beb3fa97619deae2efcd97bc064f77de50387489f8e4cd2f7aacfdef",
        "pacer_doc": "44",
        "filed": "2025-02-04",
    },
    "second_superseding_indictment": {
        "file_name": "pacer -- insider threat --  SECOND SUPERSEDING INDICTMENT.pdf",
        "sha256": "78ac0b5ddfc1c511e2b86b33440b7ed54d553d35dd3896572a4ebef2ec8f85c0",
        "pacer_doc": "140",
        "filed": "2025-09-09",
    },
    "wechat_translation": {
        "file_name": "pacer -- insider threat -- English translation of WeChat Thread.pdf",
        "sha256": "332fb6bfb421a38119fc9d58cc2e9b0443c05387f22fbab00d95ab4016c18cff",
        "pacer_doc": "191-1",
        "filed": "2025-09-21",
    },
    "jury_verdict": {
        "file_name": "pacer -- insider threat -- Jury Verdict.pdf",
        "sha256": "2584cd4affdf7a598ef8b6c067851e27e87496a19a88ab95c3d504ef665e638e",
        "pacer_doc": "367",
        "filed": "2026-01-29",
    },
}

# ---------------------------------------------------------------------------
# Trade Secret Categories One through Seven (Second Superseding Indictment
# paras. 36-42), with exemplar exhibit file titles from the verdict form
# (Doc 367). Each category grounds one § 1832 count and one § 1831 count.
# ---------------------------------------------------------------------------
TS_CATEGORIES = [
    {
        "num": 1,
        "desc": (
            "Instruction sets, protocols, internal specifications, and "
            "implementation level details related to the four primary "
            "components of Google's custom designed TPU chip: (1) "
            "TensorCore; (2) BarnaCore/SparseCore; (3) high bandwidth "
            "memory (HBM) access interface; and (4) inter-chip-interconnect "
            "(ICI)."
        ),
        "exhibits": (
            "PFC - BarnaCore Instruction Set Architecture; PFC - TensorCore "
            "Instruction Set Architecture 1-8; PFC - Host Communication; "
            "PFC - ICI Initialization / Link Enable and Resets / "
            "Interconnect / Memory System; TPU ICI (trial exhibits 358-373)"
        ),
    },
    {
        "num": 2,
        "desc": (
            "Documents including details of the design, performance, and "
            "operation of Google's custom designed TPU chips, TPU machines, "
            "and TPU systems."
        ),
        "exhibits": (
            "Accelerators; Ghostlite; Ghostlite Multi-host Software "
            "Enablement Program Kickoff; ViperLite; ViperLitePod; "
            "ViperLitePod System Introduction (trial exhibits 374-380)"
        ),
    },
    {
        "num": 3,
        "desc": (
            "Design documents for Google's TPU software that managed the "
            "hardware and resources within a TPU, facilitated communication "
            "between TPUs, and allocated and managed collections of "
            "interconnected TPUs to different workloads."
        ),
        "exhibits": (
            "Cloud TPU; Ghostfish Software Review; ICI Resilient Slice; "
            "XLA/TPU; Slice Builder; Slice Creation Algorithms; MegaScale "
            "XLA; Megascale Networking; JAX+Pathways; XOR PRD; TPU "
            "Fungibility/ACU Roadmap (trial exhibits 381-399)"
        ),
    },
    {
        "num": 4,
        "desc": (
            "Documents including details of the design, performance, and "
            "operation of Google's custom GPU machines and GPU systems."
        ),
        "exhibits": (
            "AdAstra-Board / Hardware / Mechanical / NetworkTopology / "
            "Storage; BigRig; Endurance-B Hardware Design Doc; Endurance "
            "GPU tray fans; Rack - Jolt, Zoid2; H100 Competitive Analysis "
            "(trial exhibits 400-410)"
        ),
    },
    {
        "num": 5,
        "desc": (
            "Design documents for Google's GPU software that facilitated "
            "communication between GPUs and allocated and managed "
            "collections of interconnected GPUs to different workloads."
        ),
        "exhibits": (
            "AdAstra ML Sync / GPUDirect / LinkD / MachineManager / "
            "SuperpodSW / ControlPlane / StableFleet / XManager; Astrophel "
            "on GKE; Borg Traffic Matrix API; TCPDirect for AdAstra; GPU "
            "sharing in Borg; UCF Unified Communication Framework (trial "
            "exhibits 411-436)"
        ),
    },
    {
        "num": 6,
        "desc": (
            "Design specifications to implement Google's proprietary chip "
            "component designed to deliver low-latency and high-bandwidth "
            "transfers of data over large-scale networks on Google's "
            "SmartNIC."
        ),
        "exhibits": (
            "Diorite Architecture Overview; Diorite-uArch; RDMA; Terrazzo "
            "V2 concept phase CFR (trial exhibits 437-440)"
        ),
    },
    {
        "num": 7,
        "desc": (
            "Design documents for Google's software to implement its high "
            "performance and cloud networking on its SmartNIC."
        ),
        "exhibits": (
            "Raptor Multi-NIC; RDMA on-NIC SW architecture; Andromeda3.0; "
            "CloudRDMA Overview / Arch / DeepDive series; Diorite-gHMA / "
            "OCM / Routing / Topology; HMA RDMA Support; Pony Express Use "
            "Cases (trial exhibits 441-462)"
        ),
    },
]

COUNT_WORDS = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven",
    "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
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
    """Date-only court fact rendered at local midnight Pacific time.

    N.D. Cal.: PDT (-07:00) roughly April-October, PST (-08:00) otherwise.
    Month-level approximation is sufficient for filing dates.
    """
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
            "uco-core:name": f"United States v. Linwei Ding, {PACER_DOCKET} (N.D. Cal.)",
            "legalproc:caseIdentifier": PACER_DOCKET,
            "uco-core:description": (
                "Insider-threat prosecution of Linwei Ding, a.k.a. Leon "
                "Ding, a Google software engineer hired in 2019 to work on "
                "the software platform for Google's supercomputing data "
                "centers. Between 2022-05-21 and 2023-05-02, Ding uploaded "
                "more than 1,000 unique files containing Google "
                "Confidential Information — including Trade Secret "
                "Categories One through Seven covering TPU chips and "
                "systems, GPU machines and systems, data-center management "
                "software, and Google's custom SmartNIC — from Google's "
                "network into a personal Google Cloud account, copying "
                "source files into Apple Notes on his Google-issued "
                "MacBook and exporting them as PDFs to evade data-loss-"
                "prevention detection. While still employed he became CTO "
                "of PRC-based Beijing Rongshu Lianzhi Technology, founded "
                "and led Shanghai Zhisuan Technology as CEO, pitched "
                "Zhisuan at the MiraclePlus incubator conference in "
                "Beijing, applied to a PRC talent program, and circulated "
                "materials citing PRC State Council and Cyberspace "
                "Administration of China AI policies. Google detected a "
                "further 2023-12-02 upload, interviewed Ding, and "
                "discovered the exfiltration; the FBI executed search "
                "warrants at his residence (2024-01-06) and on his cloud "
                "accounts (2024-01-13). A jury convicted Ding on all "
                "seven counts of theft of trade secrets (18 U.S.C. § 1832) "
                "and all seven counts of economic espionage (18 U.S.C. "
                "§ 1831) on 2026-01-29; sentencing is pending as of the "
                "modeled record. District Judge Vince Chhabria; U.S. "
                "Attorney Craig H. Missakian; AUSAs Casey Boome, Molly K. "
                "Priedeman, Roland Chang; NSD Trial Attorney Yifei Zheng. "
                + src_ref("second_superseding_indictment", "paras. 1-42") + "; "
                + src_ref("jury_verdict", "pp. 1-15")
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
    ding = uid("person-ding")
    rongshu_ceo = uid("person-rongshu-ceo")
    badge_colleague = uid("person-badge-colleague")
    ye_yuan = uid("person-ye-yuan")
    kunjie_jiao = uid("person-kunjie-jiao")
    zi_xiong = uid("person-zi-xiong")
    google = uid("org-google")
    rongshu = uid("org-rongshu")
    zhisuan = uid("org-zhisuan")
    miracleplus = uid("org-miracleplus")
    ir_capital = uid("org-ir-capital")
    prc_state_council = uid("org-prc-state-council")
    prc_cac = uid("org-prc-cac")
    fbi = uid("org-fbi")
    usao = uid("org-usao-ndca")

    graph.extend(
        [
            {
                "@id": ding,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Linwei Ding, a.k.a. Leon Ding",
                "uco-core:description": (
                    "Defendant. Google software engineer hired 2019 "
                    "(Employment Agreement signed 2019-02-20; started "
                    "2019-05-13; Code of Conduct signed 2019-05-14) working "
                    "on the software platform for Google's supercomputing "
                    "data centers, with authorized access to confidential "
                    "information about the hardware infrastructure, "
                    "software platform, and AI models they supported. "
                    "Secretly exfiltrated more than 1,000 confidential "
                    "files while affiliating with PRC AI companies Rongshu "
                    "(as CTO) and Zhisuan (as founder/CEO). WeChat account "
                    "'dingyong198608'. Resigned from Google effective "
                    "2024-01-05; convicted by jury on all 14 counts "
                    "2026-01-29. "
                    + src_ref("second_superseding_indictment", "paras. 15-32")
                ),
            },
            {
                "@id": rongshu_ceo,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "CEO of Beijing Rongshu Lianzhi Technology (unnamed)",
                "uco-core:description": (
                    "Emailed Ding beginning on or about 2022-06-13 — less "
                    "than one month after Ding's uploads began — offering "
                    "the CTO position at 100,000 RMB monthly (~$14,800) "
                    "plus bonus and stock; told potential investors on "
                    "2023-04-17 that Ding was Rongshu's CTO. "
                    + src_ref("second_superseding_indictment", "paras. 18-19")
                ),
            },
            {
                "@id": badge_colleague,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Google employee who scanned Ding's badge (unnamed)",
                "uco-core:description": (
                    "Scanned Ding's access badge at Ding's request on "
                    "2023-12-04, -06, and -08, making it appear Ding was "
                    "working from his U.S. Google office while Ding was in "
                    "the PRC; identified in Google's surveillance-footage "
                    "review. "
                    + src_ref("second_superseding_indictment", "para. 31")
                ),
            },
            {
                "@id": ye_yuan,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Ye Yuan",
                "uco-core:description": (
                    "Zhisuan co-founder ('Mr. Yuan') per the translated "
                    "WeChat thread; coordinated the CMS project teaser, "
                    "proposed the company name 'Zhisuan', and ran investor "
                    "meetings with Sequoia, Sinovation Ventures, Baidu "
                    "Ventures, and IDG alongside Ding. "
                    + src_ref("wechat_translation", "pp. 17, 20-22")
                ),
            },
            {
                "@id": kunjie_jiao,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Kunjie Jiao (I&R Capital)",
                "uco-core:description": (
                    "I&R Capital advisor who drafted the Zhisuan/CMS "
                    "project teaser, scheduled investor roadshow meetings "
                    "(Sinovation Ventures, Baidu Ventures, Sequoia, IDG), "
                    "and administered the WeChat group. "
                    + src_ref("wechat_translation", "pp. 3-4, 22-26")
                ),
            },
            {
                "@id": zi_xiong,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Zi Xiong (I&R Capital)",
                "uco-core:description": (
                    "I&R Capital participant in the Zhisuan WeChat group; "
                    "arranged Tencent Meeting calls with Sequoia Capital "
                    "and shared AI-industry market research, including "
                    "articles on Google's TPU supercomputer. "
                    + src_ref("wechat_translation", "pp. 9, 13, 32")
                ),
            },
            {
                "@id": google,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Google, LLC",
                "uco-core:description": (
                    "Victim technology company headquartered in Mountain "
                    "View, California; subsidiary of Alphabet Inc. Owner "
                    "of the stolen trade secrets covering TPU chips and "
                    "systems, GPU machines and systems, the supercomputing "
                    "software platform (including the Cluster Management "
                    "System), and the custom SmartNIC. Protected them with "
                    "badge-controlled physical access, device "
                    "authentication, two-factor authentication, data-loss-"
                    "prevention monitoring, an 'Impossible Location "
                    "Signal' risk analytic, employment agreements, and a "
                    "code of conduct. "
                    + src_ref("second_superseding_indictment", "paras. 1-14")
                ),
            },
            {
                "@id": rongshu,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Beijing Rongshu Lianzhi Technology Co., Ltd. (\"Rongshu\")",
                "uco-core:description": (
                    "Early-stage PRC technology company developing "
                    "acceleration software for machine learning on GPU "
                    "chips and AI federated learning platforms. Offered "
                    "Ding its CTO position in June 2022; Ding participated "
                    "in Rongshu investor meetings in the PRC from December "
                    "2022 and never informed Google of the affiliation. "
                    + src_ref("second_superseding_indictment", "paras. 18-20")
                ),
            },
            {
                "@id": zhisuan,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Shanghai Zhisuan Technology Co. Ltd. (\"Zhisuan\")",
                "uco-core:description": (
                    "PRC-based startup founded by Ding (CEO) by no later "
                    "than 2023-05-30, proposing to develop a Cluster "
                    "Management System to accelerate ML workloads on "
                    "supercomputing chips. A Zhisuan document Ding "
                    "circulated on 2023-11-29 stated: 'we have experience "
                    "with Google's ten-thousand-card computational power "
                    "platform; we just need to replicate and upgrade it - "
                    "and then further develop a computational power "
                    "platform suited to China's national conditions.' An "
                    "internal memo dated 2023-12-14 indicates Zhisuan "
                    "intended to market to and serve multiple "
                    "PRC-controlled entities, including government "
                    "agencies and universities. "
                    + src_ref("second_superseding_indictment", "paras. 21-26")
                ),
            },
            {
                "@id": miracleplus,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "MiraclePlus",
                "uco-core:description": (
                    "PRC-based startup incubation program. Zhisuan was "
                    "accepted after Ding's 2023-05-30 application; on "
                    "2023-11-20 Ding granted a 7% ownership interest in "
                    "Zhisuan to a MiraclePlus-affiliated company for "
                    "investment capital, and on 2023-11-24 pitched Zhisuan "
                    "at the MiraclePlus venture capital investor "
                    "conference in Beijing. "
                    + src_ref("second_superseding_indictment", "para. 22")
                ),
            },
            {
                "@id": ir_capital,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "I&R Capital",
                "uco-core:description": (
                    "PRC investment advisory whose staff (Kunjie Jiao, Zi "
                    "Xiong, Linfei Cai, Xiaoyi Zheng) ran the 'Zhisuan - "
                    "Internal Cooperation Group of I&R Capital' WeChat "
                    "group, drafting the fundraising teaser and arranging "
                    "meetings with Sinovation Ventures, Sequoia Capital, "
                    "Baidu Ventures, and IDG Capital while Ding was still "
                    "employed at Google. "
                    + src_ref("wechat_translation", "pp. 2, 16-26")
                ),
            },
            {
                "@id": prc_state_council,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "PRC State Council",
                "uco-core:description": (
                    "Chief administrative authority of the People's "
                    "Republic of China; its 2017 'Notice on the Development "
                    "of the New Generation of Artificial Intelligence' was "
                    "cited in the PowerPoint Ding circulated to Zhisuan "
                    "employees and investors on 2023-11-17. Relevant to the "
                    "§ 1831 economic-espionage counts' foreign-government "
                    "benefit element. "
                    + src_ref("second_superseding_indictment", "para. 24")
                ),
            },
            {
                "@id": prc_cac,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Cyberspace Administration of China (CAC)",
                "uco-core:description": (
                    "PRC government agency (State Internet Information "
                    "Office) regulating the PRC's internet and cyberspace; "
                    "co-sponsor of the 'Interim Measures for the Management "
                    "of Generative AI Services' quoted in Ding's Zhisuan "
                    "presentation (Article 6: 'Encourage independent "
                    "innovation in basic technologies such as generative "
                    "artificial intelligence algorithms, chips, and "
                    "supporting software platforms'). "
                    + src_ref("second_superseding_indictment", "para. 24")
                ),
            },
            {
                "@id": fbi,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Federal Bureau of Investigation",
                "uco-core:description": (
                    "Executed the 2024-01-06 search warrant at Ding's "
                    "residence (seizing his electronic devices) and the "
                    "2024-01-13 search warrant for the contents of Ding "
                    "Accounts 1 and 2. "
                    + src_ref("second_superseding_indictment", "paras. 33-34")
                ),
            },
            {
                "@id": usao,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "U.S. Attorney's Office, Northern District of California",
                "uco-core:description": (
                    "Prosecuting office (U.S. Attorney Craig H. Missakian; "
                    "AUSAs Casey Boome, Molly K. Priedeman, Roland Chang) "
                    "with DOJ National Security Division Trial Attorney "
                    "Yifei Zheng. "
                    + src_ref("second_superseding_indictment", "signature page")
                ),
            },
        ]
    )
    graph.append(rel(ding, investigation, "Subject_Of"))
    graph.append(rel(ding, google, "Employed_By"))
    graph.append(rel(ding, rongshu, "Member_Of"))
    graph.append(rel(ding, zhisuan, "Member_Of"))
    graph.append(rel(rongshu_ceo, rongshu, "Member_Of"))
    graph.append(rel(ye_yuan, zhisuan, "Member_Of"))
    graph.append(rel(kunjie_jiao, ir_capital, "Member_Of"))
    graph.append(rel(zi_xiong, ir_capital, "Member_Of"))
    graph.append(rel(badge_colleague, google, "Employed_By"))
    graph.append(rel(google, investigation, "Victim_Of", directional=True))

    # ------------------------------------------------------------------
    # Cyber observables: devices, accounts, the exfiltrated file set,
    # trade secret categories, the WeChat thread, security telemetry,
    # and key documents. This case is almost entirely cyber-domain.
    # ------------------------------------------------------------------
    ding_laptop = uid("observable-ding-macbook")
    ding_mobile = uid("observable-ding-mobile")
    account1 = uid("observable-ding-account-1")
    account2 = uid("observable-ding-account-2")
    apple_notes = uid("observable-apple-notes")
    exfil_fileset = uid("observable-exfiltrated-fileset")
    wechat_account = uid("observable-ding-wechat-account")
    wechat_thread = uid("observable-zhisuan-wechat-thread")
    msg_replicate = uid("observable-replicate-upgrade-message")
    zhisuan_deck = uid("observable-zhisuan-policy-deck")
    talent_application = uid("observable-talent-program-application")
    zhisuan_memo = uid("observable-zhisuan-internal-memo")
    sda_doc = uid("observable-self-deletion-affidavit")
    badge_records = uid("observable-badge-access-records")
    surveillance_footage = uid("observable-surveillance-footage")
    resignation_email = uid("observable-resignation-email")
    flight_booking = uid("observable-flight-booking")

    graph.extend(
        [
            {
                "@id": ding_laptop,
                "@type": ["uco-observable:Laptop", "uco-core:UcoObject"],
                "uco-core:name": "Ding's Google-issued MacBook laptop",
                "uco-core:description": (
                    "Corporate laptop on which Ding copied data from "
                    "Google source files into the Apple Notes application, "
                    "converted the notes to PDF files, and uploaded them "
                    "from the Google network into Ding Account 1 — a "
                    "method that helped evade immediate detection by "
                    "Google's data-loss-prevention monitoring. Remotely "
                    "locked by Google on or about 2023-12-29; retrieved "
                    "from Ding's residence by Google security personnel on "
                    "2024-01-04. "
                    + src_ref("second_superseding_indictment", "paras. 17, 30, 32")
                ),
            },
            {
                "@id": ding_mobile,
                "@type": ["uco-observable:MobileDevice", "uco-core:UcoObject"],
                "uco-core:name": "Ding's Google-issued mobile device",
                "uco-core:description": (
                    "Corporate mobile device retrieved from Ding's "
                    "residence by Google security personnel on 2024-01-04. "
                    + src_ref("second_superseding_indictment", "para. 32")
                ),
            },
            {
                "@id": account1,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "DING Account 1 (personal Google Cloud account)",
                "uco-core:description": (
                    "Personal Google Cloud account that received Ding's "
                    "periodic uploads from 2022-05-21 until 2023-05-02. "
                    "The FBI's 2024-01-13 warrant search found it "
                    "contained more than 1,000 unique files of Google "
                    "Confidential Information, including the trade secrets "
                    "in Categories One through Seven. "
                    + src_ref("second_superseding_indictment", "paras. 17, 34")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-ding-account-1"),
                        "@type": "uco-observable:DigitalAccountFacet",
                        "uco-observable:displayName": "DING Account 1",
                    }
                ],
            },
            {
                "@id": account2,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "DING Account 2 (personal Google Drive account)",
                "uco-core:description": (
                    "Second personal account controlled by Ding, to which "
                    "he uploaded additional files from the Google network "
                    "on or about 2023-12-02 while in the PRC — the upload "
                    "whose detection triggered Google's investigation. "
                    + src_ref("second_superseding_indictment", "para. 27")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-ding-account-2"),
                        "@type": "uco-observable:DigitalAccountFacet",
                        "uco-observable:displayName": "DING Account 2",
                    }
                ],
            },
            {
                "@id": apple_notes,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Apple Notes application (exfiltration staging tool)",
                "uco-core:description": (
                    "Application on Ding's Google-issued MacBook into "
                    "which he copied data from Google source files before "
                    "converting the notes to PDF and uploading them, "
                    "evading immediate detection. "
                    + src_ref("second_superseding_indictment", "para. 17")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-apple-notes"),
                        "@type": "uco-observable:ApplicationFacet",
                        "uco-observable:applicationIdentifier": "Apple Notes",
                    }
                ],
            },
            {
                "@id": exfil_fileset,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Exfiltrated file set (>1,000 unique files, PDF exports of Apple Notes)",
                "uco-core:description": (
                    "More than 1,000 unique files containing Google "
                    "Confidential Information uploaded to Ding Account 1 "
                    "between 2022-05-21 and 2023-05-02, including the "
                    "trade secrets alleged in Categories One through "
                    "Seven. Upload timestamps embedded in the recovered "
                    "file names (e.g. '-at-2022-06-01T18_10_22Z-pinned"
                    ".pdf', '-at-2023-04-16T06_09_02Z-pinned.pdf') show "
                    "upload waves on 2022-05-21, 2022-06-01, and "
                    "2023-04-16. "
                    + src_ref("second_superseding_indictment", "paras. 17, 34")
                    + "; " + src_ref("jury_verdict", "exhibit file-title tables")
                ),
            },
            {
                "@id": wechat_account,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Ding's WeChat account 'dingyong198608'",
                "uco-core:description": (
                    "WeChat account through which Ding participated in the "
                    "Zhisuan fundraising group as 'Linwei'/'Mr. Ding'. "
                    + src_ref("wechat_translation", "p. 2 (local user)")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-ding-wechat"),
                        "@type": "uco-observable:InstantMessagingAddressFacet",
                        "uco-observable:addressValue": "dingyong198608",
                        "uco-observable:displayName": "Linwei Ding",
                    }
                ],
            },
            {
                "@id": wechat_thread,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "WeChat group 'Zhisuan - Internal Cooperation Group of I&R Capital'",
                "uco-core:description": (
                    "13-participant WeChat group chat (group ID "
                    "48483066127@chatroom), 242 messages from 2023-03-20 "
                    "to 2023-05-11 (UTC), captured in the English "
                    "translation admitted as Doc 191-1 (Bates AML-0002859 "
                    "to AML-0002900). Documents Zhisuan's CMS-product "
                    "fundraising while Ding was employed at Google: teaser "
                    "drafting, naming the company 'Zhisuan', Ding's resume "
                    "circulation, and meetings with Sinovation Ventures, "
                    "Sequoia Capital, Baidu Ventures, and IDG Capital. "
                    "Ding, noted as 'on West Coast Bay Area time', "
                    "answered a 2023-05-06 status question with 'I'm in a "
                    "transition period right now and pretty busy'. "
                    + src_ref("wechat_translation", "pp. 2-43")
                ),
            },
            {
                "@id": msg_replicate,
                "@type": ["uco-observable:Message", "uco-core:UcoObject"],
                "uco-core:name": "Ding's 'replicate and upgrade' Zhisuan document circulation (2023-11-29)",
                "uco-core:description": (
                    "Zhisuan document circulated by Ding to a Zhisuan "
                    "WeChat group stating: 'we have experience with "
                    "Google's ten-thousand-card computational power "
                    "platform; we just need to replicate and upgrade it - "
                    "and then further develop a computational power "
                    "platform suited to China's national conditions.' "
                    + src_ref("second_superseding_indictment", "para. 22")
                ),
                "uco-core:hasFacet": [
                    {
                        "@id": uid("facet-replicate-message"),
                        "@type": "uco-observable:MessageFacet",
                        "uco-observable:from": {"@id": wechat_account},
                        "uco-observable:messageText": (
                            "we have experience with Google's ten-thousand-"
                            "card computational power platform; we just "
                            "need to replicate and upgrade it - and then "
                            "further develop a computational power platform "
                            "suited to China's national conditions"
                        ),
                        "uco-observable:sentTime": lit(
                            "xsd:dateTime", pacific_midnight("2023-11-29")
                        ),
                    }
                ],
            },
            {
                "@id": zhisuan_deck,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Zhisuan PowerPoint citing PRC national AI policies (2023-11-17)",
                "uco-core:description": (
                    "Presentation Ding circulated to Zhisuan employees and "
                    "potential investors citing the PRC State Council's "
                    "2017 'Notice on the Development of the New Generation "
                    "of Artificial Intelligence' and quoting Article 6 of "
                    "the CAC-sponsored 'Interim Measures for the "
                    "Management of Generative AI Services'. Central "
                    "evidence of intent to benefit a foreign government "
                    "for the § 1831 counts. "
                    + src_ref("second_superseding_indictment", "para. 24")
                ),
            },
            {
                "@id": talent_application,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "PRC talent-program application PowerPoint (December 2023)",
                "uco-core:description": (
                    "Application to a Shanghai-based PRC talent program — "
                    "programs sponsored by the PRC to incentivize "
                    "researchers abroad to transmit knowledge and research "
                    "to the PRC for salaries, research funds, or lab space "
                    "— stating Ding's product 'will help China to have "
                    "computing power infrastructure capabilities that are "
                    "on par with the international level.' "
                    + src_ref("second_superseding_indictment", "para. 25")
                ),
            },
            {
                "@id": zhisuan_memo,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Internal Zhisuan memo on PRC-controlled customers (2023-12-14)",
                "uco-core:description": (
                    "Memo indicating Zhisuan intended to market itself to "
                    "and provide services to multiple PRC-controlled "
                    "entities, including government agencies and "
                    "universities. "
                    + src_ref("second_superseding_indictment", "para. 26")
                ),
            },
            {
                "@id": sda_doc,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Self-Deletion Affidavit signed by Ding (2023-12-08)",
                "uco-core:description": (
                    "Affidavit stating: 'I have searched my personal "
                    "possessions, including all devices, accounts, and "
                    "documents in my custody or control for any non-public "
                    "information originating from my job at Google ... I "
                    "have permanently deleted and/or destroyed all copies "
                    "of such information ... As a result, I no longer have "
                    "access to such information outside the scope of my "
                    "employment.' Signed without disclosing the 1,000+ "
                    "prior uploads or the Rongshu and Zhisuan "
                    "affiliations. "
                    + src_ref("second_superseding_indictment", "para. 27")
                ),
            },
            {
                "@id": badge_records,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Google physical and network access telemetry for Ding",
                "uco-core:description": (
                    "Badge access times and locations, login IP addresses, "
                    "and two-factor authentication logs Google gathered "
                    "for risk analysis (including the 'Impossible Location "
                    "Signal' analytic). Records show Ding's badge scanned "
                    "at his U.S. office on 2023-12-04, -06, and -08 while "
                    "Ding was in the PRC — scans performed by a colleague "
                    "at Ding's request. "
                    + src_ref("second_superseding_indictment", "paras. 10, 31")
                ),
            },
            {
                "@id": surveillance_footage,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "Surveillance footage of Google building entrance (December 2023)",
                "uco-core:description": (
                    "Video reviewed by Google investigators on or about "
                    "2023-12-29 showing another employee scanning Ding's "
                    "access badge on 2023-12-04, -06, and -08. "
                    + src_ref("second_superseding_indictment", "para. 31")
                ),
            },
            {
                "@id": resignation_email,
                "@type": ["uco-observable:EmailMessage", "uco-core:UcoObject"],
                "uco-core:name": "Ding's resignation email to his Google manager (2023-12-26)",
                "uco-core:description": (
                    "Email resigning from Google and stating his last day "
                    "would be 2024-01-05 — sent twelve days after booking "
                    "a one-way ticket to Beijing and without disclosing "
                    "his PRC affiliations. "
                    + src_ref("second_superseding_indictment", "para. 29")
                ),
            },
            {
                "@id": flight_booking,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": "One-way China Southern Airlines booking, SFO to Beijing (booked 2023-12-14)",
                "uco-core:description": (
                    "One-way ticket from San Francisco to Beijing booked "
                    "2023-12-14 for a flight scheduled to depart "
                    "2024-01-07 — two days after Ding's stated last day at "
                    "Google — booked unbeknownst to Google. "
                    + src_ref("second_superseding_indictment", "para. 28")
                ),
            },
        ]
    )
    graph.append(rel(ding_laptop, ding, "Used_By"))
    graph.append(rel(ding_mobile, ding, "Used_By"))
    graph.append(rel(account1, ding, "Controlled_By"))
    graph.append(rel(account2, ding, "Controlled_By"))
    graph.append(rel(wechat_account, ding, "Used_By"))
    graph.append(rel(apple_notes, ding_laptop, "Installed_On"))
    graph.append(rel(exfil_fileset, account1, "Stored_In"))
    graph.append(rel(msg_replicate, wechat_thread, "Contained_Within"))
    graph.append(rel(wechat_thread, doc_ids["wechat_translation"], "Documented_By"))
    graph.append(rel(surveillance_footage, badge_records, "Corroborates"))

    # ------------------------------------------------------------------
    # Trade Secret Categories One through Seven: the stolen files are
    # genuinely cyber artifacts (design documents, specifications), so
    # each category is an observable collection owned by Google.
    # ------------------------------------------------------------------
    ts_ids: dict[int, str] = {}
    for cat in TS_CATEGORIES:
        tsid = uid(f"observable-ts-category-{cat['num']}")
        ts_ids[cat["num"]] = tsid
        graph.append(
            {
                "@id": tsid,
                "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
                "uco-core:name": f"Trade Secret Category {cat['num']}",
                "uco-core:description": (
                    cat["desc"] + " Exemplar exhibit file titles from the "
                    "verdict form: " + cat["exhibits"] + ". "
                    + src_ref("second_superseding_indictment",
                              f"para. {35 + cat['num']}")
                ),
            }
        )
        graph.append(rel(tsid, google, "Owned_By"))
        graph.append(rel(tsid, exfil_fileset, "Contained_Within"))

    # ------------------------------------------------------------------
    # Non-cyber physical item: Ding's access badge. The badge itself
    # never lives in cyberspace (the scan *records* above are the cyber
    # artifacts), so it is dual-typed with gufo:FunctionalComplex.
    # ------------------------------------------------------------------
    ding_badge = uid("item-ding-access-badge")
    graph.append(
        {
            "@id": ding_badge,
            "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
            "uco-core:name": "Ding's Google building access badge",
            "uco-core:description": (
                "Physical access badge required to enter Ding's Google "
                "building; scanned by a colleague at Ding's request on "
                "2023-12-04, -06, and -08 to make it appear Ding was "
                "working from his U.S. office while he was in the PRC. "
                + src_ref("second_superseding_indictment", "para. 31")
            ),
        }
    )
    graph.append(rel(ding_badge, ding, "Assigned_To"))
    graph.append(rel(badge_colleague, ding_badge, "Used"))

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------
    loc_google = uid("location-google-mountain-view")
    loc_residence = uid("location-ding-residence")
    loc_beijing = uid("location-beijing")
    graph.extend(
        [
            {
                "@id": loc_google,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Google campus, Mountain View / Northern District of California",
                "uco-core:description": (
                    "Google headquarters and the building where Ding "
                    "worked, secured with campus-wide guards, entry "
                    "cameras, and badge-controlled access. "
                    + src_ref("second_superseding_indictment", "paras. 1, 8")
                ),
            },
            {
                "@id": loc_residence,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Ding's residence (N.D. Cal.)",
                "uco-core:description": (
                    "Site of Google's 2024-01-04 device retrieval and the "
                    "FBI's 2024-01-06 search warrant execution. "
                    + src_ref("second_superseding_indictment", "paras. 32-33")
                ),
            },
            {
                "@id": loc_beijing,
                "@type": ["uco-location:Location", "uco-core:UcoObject"],
                "uco-core:name": "Beijing, People's Republic of China",
                "uco-core:description": (
                    "Site of the 2023-11-24 MiraclePlus venture capital "
                    "investor conference where Ding pitched Zhisuan, and "
                    "destination of his 2024-01-07 one-way ticket. "
                    + src_ref("second_superseding_indictment", "paras. 22, 28")
                ),
            },
        ]
    )

    # ------------------------------------------------------------------
    # Scheme timeline: exfiltration, PRC affiliations, and concealment
    # (uco-action:Action). Charged conduct spans 2022-05-21 to 2024-01-13.
    # ------------------------------------------------------------------
    overt_acts = [
        {
            "label": "act-exfiltration-uploads",
            "name": "Ding uploads 1,000+ confidential files to Ding Account 1 (2022-05-21 to 2023-05-02)",
            "performer": ding,
            "start": "2022-05-21",
            "end": "2023-05-02",
            "instruments": [ding_laptop, apple_notes],
            "objects": list(ts_ids.values()),
            "results": [exfil_fileset],
            "desc": (
                "Periodic uploads of Google Confidential Information — "
                "including all seven trade secret categories — via the "
                "Apple Notes-to-PDF method that evaded immediate "
                "detection. "
                + src_ref("second_superseding_indictment", "para. 17")
            ),
        },
        {
            "label": "act-rongshu-cto-offer",
            "name": "Rongshu CEO emails Ding a CTO offer (from 2022-06-13)",
            "performer": rongshu_ceo,
            "start": "2022-06-13",
            "desc": (
                "Emails offering the Rongshu CTO position at 100,000 RMB "
                "monthly plus bonus and stock, beginning less than one "
                "month after Ding's uploads started. "
                + src_ref("second_superseding_indictment", "para. 18")
            ),
        },
        {
            "label": "act-prc-trip-rongshu",
            "name": "Ding travels to the PRC and raises capital for Rongshu (2022-10-29 to 2023-03-25)",
            "performer": ding,
            "start": "2022-10-29",
            "end": "2023-03-25",
            "desc": (
                "Ding remained in the PRC for roughly five months, "
                "participating in Rongshu investor meetings from December "
                "2022; Rongshu's CEO identified him to investors as CTO "
                "on 2023-04-17. Google was never informed. "
                + src_ref("second_superseding_indictment", "paras. 19-20")
            ),
        },
        {
            "label": "act-wechat-fundraising",
            "name": "Zhisuan/CMS fundraising coordinated in the I&R Capital WeChat group (2023-03-20 to 2023-05-11)",
            "performer": ding,
            "start": "2023-03-20",
            "end": "2023-05-11",
            "objects": [wechat_thread],
            "desc": (
                "Ding ('dingyong198608'), co-founder Ye Yuan, and I&R "
                "Capital staff drafted the CMS project teaser, named the "
                "company 'Zhisuan', circulated Ding's resume, and met "
                "with Sinovation Ventures, Sequoia Capital, Baidu "
                "Ventures, and IDG Capital — all while Ding remained a "
                "Google employee. "
                + src_ref("wechat_translation", "pp. 2-43")
            ),
        },
        {
            "label": "act-zhisuan-founding",
            "name": "Ding founds Zhisuan and applies to MiraclePlus (by 2023-05-30)",
            "performer": ding,
            "start": "2023-05-30",
            "desc": (
                "Ding founded Shanghai Zhisuan Technology, acted as CEO, "
                "and applied on Zhisuan's behalf to the MiraclePlus "
                "startup incubation program, proposing a CMS to "
                "accelerate ML workloads on supercomputing chips. "
                + src_ref("second_superseding_indictment", "paras. 21-22")
            ),
        },
        {
            "label": "act-policy-deck",
            "name": "Ding circulates the PRC-policy PowerPoint to Zhisuan employees and investors (2023-11-17)",
            "performer": ding,
            "start": "2023-11-17",
            "objects": [zhisuan_deck],
            "desc": (
                "Presentation citing the PRC State Council's 2017 AI "
                "development notice and the CAC-sponsored Interim "
                "Measures for generative AI. "
                + src_ref("second_superseding_indictment", "para. 24")
            ),
        },
        {
            "label": "act-miracleplus-agreement",
            "name": "Ding signs the MiraclePlus investment agreement (2023-11-20)",
            "performer": ding,
            "start": "2023-11-20",
            "desc": (
                "Agreement granting a seven percent ownership interest in "
                "Zhisuan to a MiraclePlus-affiliated company in exchange "
                "for investment capital. "
                + src_ref("second_superseding_indictment", "para. 22")
            ),
        },
        {
            "label": "act-miracleplus-pitch",
            "name": "Ding pitches Zhisuan at the MiraclePlus investor conference, Beijing (2023-11-24)",
            "performer": ding,
            "start": "2023-11-24",
            "desc": (
                "Ding traveled to the PRC and presented as Zhisuan's CEO "
                "at the MiraclePlus venture capital investor conference — "
                "the appearance Google learned of on 2023-12-29. "
                + src_ref("second_superseding_indictment", "paras. 22, 30")
            ),
        },
        {
            "label": "act-replicate-circulation",
            "name": "Ding circulates the 'replicate and upgrade' Zhisuan document (2023-11-29)",
            "performer": ding,
            "start": "2023-11-29",
            "objects": [msg_replicate],
            "desc": (
                "Circulated to the members of a Zhisuan WeChat group, "
                "claiming experience with 'Google's ten-thousand-card "
                "computational power platform' to be replicated and "
                "upgraded for China's national conditions. "
                + src_ref("second_superseding_indictment", "para. 22")
            ),
        },
        {
            "label": "act-account2-upload",
            "name": "Ding uploads additional files to Ding Account 2 from the PRC (2023-12-02)",
            "performer": ding,
            "start": "2023-12-02",
            "objects": [account2],
            "desc": (
                "Upload from the Google network to a second personal "
                "Google Drive account while Ding was in the PRC — the "
                "activity Google's monitoring detected. "
                + src_ref("second_superseding_indictment", "para. 27")
            ),
        },
        {
            "label": "act-badge-scans",
            "name": "Colleague scans Ding's badge to simulate his presence (2023-12-04 to 2023-12-08)",
            "performer": badge_colleague,
            "start": "2023-12-04",
            "end": "2023-12-08",
            "instruments": [ding_badge],
            "results": [badge_records],
            "desc": (
                "At Ding's request, another Google employee scanned "
                "Ding's access badge on December 4, 6, and 8, 2023, "
                "making it appear Ding was working from his U.S. office "
                "while he was in the PRC. "
                + src_ref("second_superseding_indictment", "para. 31")
            ),
        },
        {
            "label": "act-sda-signing",
            "name": "Ding signs the Self-Deletion Affidavit without disclosing the exfiltration (2023-12-08)",
            "performer": ding,
            "start": "2023-12-08",
            "objects": [sda_doc],
            "desc": (
                "After Google detected the Account 2 upload, Ding told a "
                "Google investigator the files were evidence of his work "
                "and he had no intention of leaving Google, then signed "
                "the affidavit — concealing the 1,000+ prior uploads and "
                "his Rongshu and Zhisuan affiliations. "
                + src_ref("second_superseding_indictment", "para. 27")
            ),
        },
        {
            "label": "act-flight-booking",
            "name": "Ding books a one-way ticket from San Francisco to Beijing (2023-12-14)",
            "performer": ding,
            "start": "2023-12-14",
            "objects": [flight_booking],
            "desc": (
                "China Southern Airlines flight scheduled to depart "
                "2024-01-07, booked unbeknownst to Google. "
                + src_ref("second_superseding_indictment", "para. 28")
            ),
        },
        {
            "label": "act-resignation",
            "name": "Ding emails his resignation to his Google manager (2023-12-26)",
            "performer": ding,
            "start": "2023-12-26",
            "objects": [resignation_email],
            "desc": (
                "Resignation stating his last day would be 2024-01-05. "
                + src_ref("second_superseding_indictment", "para. 29")
            ),
        },
    ]
    for act in overt_acts:
        node: dict = {
            "@id": uid(act["label"]),
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": act["name"],
            "uco-core:description": act["desc"],
            "uco-action:performer": {"@id": act["performer"]},
        }
        if "start" in act:
            node["uco-action:startTime"] = lit("xsd:dateTime", pacific_midnight(act["start"]))
        if "end" in act:
            node["uco-action:endTime"] = lit("xsd:dateTime", pacific_midnight(act["end"]))
        if act.get("instruments"):
            node["uco-action:instrument"] = [{"@id": i} for i in act["instruments"]]
        if act.get("objects"):
            node["uco-action:object"] = [{"@id": o} for o in act["objects"]]
        if act.get("results"):
            node["uco-action:result"] = [{"@id": r} for r in act["results"]]
        graph.append(node)
        graph.append(rel(uid(act["label"]), investigation, "Relates_To"))
    graph.append(rel(uid("act-miracleplus-pitch"), loc_beijing, "Occurred_At"))
    graph.append(rel(uid("act-badge-scans"), loc_google, "Occurred_At"))

    # ------------------------------------------------------------------
    # Investigative actions: Google's internal detection chain, then the
    # FBI's warrant chain.
    # ------------------------------------------------------------------
    warrant_residence = uid("authorization-residence-warrant")
    warrant_accounts = uid("authorization-accounts-warrant")
    graph.extend(
        [
            {
                "@id": warrant_residence,
                "@type": "case-investigation:Authorization",
                "uco-core:name": "Federal search warrant for Ding's residence (executed 2024-01-06)",
                "uco-core:description": (
                    "Warrant under which the FBI seized Ding's electronic "
                    "devices and other evidence one day after his last day "
                    "at Google and one day before his scheduled flight to "
                    "Beijing. "
                    + src_ref("second_superseding_indictment", "para. 33")
                ),
            },
            {
                "@id": warrant_accounts,
                "@type": "case-investigation:Authorization",
                "uco-core:name": "Federal search warrant for Ding Accounts 1 and 2 (executed 2024-01-13)",
                "uco-core:description": (
                    "Warrant for the contents of both personal cloud "
                    "accounts; Account 1 contained more than 1,000 unique "
                    "files of Google Confidential Information including "
                    "Trade Secret Categories One through Seven. "
                    + src_ref("second_superseding_indictment", "para. 34")
                ),
            },
        ]
    )

    investigative_actions = [
        {
            "label": "ia-google-dlp-detection",
            "name": "Google detects the 2023-12-02 upload to Ding Account 2",
            "performer": google,
            "start": "2023-12-08",
            "objects": [account2],
            "desc": (
                "Google's network monitoring (data-loss-prevention "
                "logging of file transfers to platforms such as Google "
                "Drive) detected the upload; Google confronted Ding on "
                "2023-12-08. "
                + src_ref("second_superseding_indictment", "paras. 9, 27")
            ),
        },
        {
            "label": "ia-google-interview",
            "name": "Google investigator interviews Ding; Ding signs the Self-Deletion Affidavit (2023-12-08)",
            "performer": google,
            "start": "2023-12-08",
            "objects": [ding],
            "results": [sda_doc],
            "desc": (
                "Ding claimed the uploads were evidence of his work at "
                "Google and assured the investigator he had no intention "
                "of leaving. "
                + src_ref("second_superseding_indictment", "para. 27")
            ),
        },
        {
            "label": "ia-google-suspend-lock",
            "name": "Google suspends Ding's network access and remotely locks his laptop (2023-12-29)",
            "performer": google,
            "start": "2023-12-29",
            "objects": [ding_laptop],
            "desc": (
                "Triggered by Google learning that Ding had presented as "
                "Zhisuan's CEO at the MiraclePlus conference. "
                + src_ref("second_superseding_indictment", "para. 30")
            ),
        },
        {
            "label": "ia-google-network-search",
            "name": "Google searches Ding's network activity history (2023-12-29)",
            "performer": google,
            "start": "2023-12-29",
            "results": [exfil_fileset],
            "desc": (
                "Search of network activity history discovered the "
                "unauthorized uploads from May 2022 through May 2023. "
                + src_ref("second_superseding_indictment", "para. 30")
            ),
        },
        {
            "label": "ia-google-footage-review",
            "name": "Google reviews surveillance footage of the building entrance (2023-12-29)",
            "performer": google,
            "start": "2023-12-29",
            "objects": [surveillance_footage, badge_records],
            "desc": (
                "Review revealed the badge-scanning arrangement: another "
                "employee scanned Ding's badge on December 4, 6, and 8, "
                "2023 while Ding was in the PRC. "
                + src_ref("second_superseding_indictment", "para. 31")
            ),
        },
        {
            "label": "ia-google-device-retrieval",
            "name": "Google security personnel retrieve Ding's laptop and mobile device (2024-01-04)",
            "performer": google,
            "start": "2024-01-04",
            "results": [ding_laptop, ding_mobile],
            "desc": (
                "Retrieved from Ding's residence the day before his "
                "stated last day of employment. "
                + src_ref("second_superseding_indictment", "para. 32")
            ),
        },
        {
            "label": "ia-fbi-residence-search",
            "name": "FBI executes the search warrant at Ding's residence (2024-01-06)",
            "performer": fbi,
            "start": "2024-01-06",
            "authorization": warrant_residence,
            "desc": (
                "Seized Ding's electronic devices and other evidence. "
                + src_ref("second_superseding_indictment", "para. 33")
            ),
        },
        {
            "label": "ia-fbi-account-search",
            "name": "FBI executes the search warrant for Ding Accounts 1 and 2 (2024-01-13)",
            "performer": fbi,
            "start": "2024-01-13",
            "objects": [account1, account2],
            "results": [exfil_fileset],
            "authorization": warrant_accounts,
            "desc": (
                "Account 1 contained more than 1,000 unique files of "
                "Google Confidential Information, including Trade Secret "
                "Categories One through Seven. "
                + src_ref("second_superseding_indictment", "para. 34")
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
            node["uco-action:startTime"] = lit("xsd:dateTime", pacific_midnight(ia["start"]))
        if ia.get("objects"):
            node["uco-action:object"] = [{"@id": o} for o in ia["objects"]]
        if ia.get("results"):
            node["uco-action:result"] = [{"@id": r} for r in ia["results"]]
        if ia.get("authorization"):
            node["case-investigation:relevantAuthorization"] = [{"@id": ia["authorization"]}]
        graph.append(node)
        graph.append(rel(uid(ia["label"]), investigation, "part_of"))
    graph.append(rel(uid("ia-fbi-residence-search"), loc_residence, "Occurred_At"))
    graph.append(rel(uid("ia-google-device-retrieval"), loc_residence, "Occurred_At"))

    # ------------------------------------------------------------------
    # Charging instruments: indictment -> superseding -> second superseding
    # ------------------------------------------------------------------
    instruments = [
        ("instrument-indictment", "indictment", "Indictment (Doc 1)", "2024-03-05",
         "Grand jury charged Ding with four counts of theft of trade "
         "secrets (18 U.S.C. § 1832): TPU v4 specifications, TPU v6 "
         "specifications, GPU hardware/software/system-management "
         "specifications, and CMS software design specifications, on or "
         "about 2022-06-01 to 2023-04-17. Magistrate Judge Virginia K. "
         "DeMarchi (no-process); assigned to Judge Vince Chhabria.",
         "indictment"),
        ("instrument-superseding", "superseding-indictment", "Superseding Indictment (Doc 44)", "2025-02-04",
         "Restructured the case to seven counts of theft of trade secrets "
         "(18 U.S.C. § 1832) and seven counts of economic espionage "
         "(18 U.S.C. § 1831), one pair per Trade Secret Category One "
         "through Seven, spanning 2022-05-21 to 2024-01-13.",
         "superseding_indictment"),
        ("instrument-second-superseding", "superseding-indictment", "Second Superseding Indictment (Doc 140)", "2025-09-09",
         "Operative charging instrument: the same fourteen-count "
         "structure with refreshed introductory allegations (Google "
         "security measures, the exfiltration method, Rongshu and "
         "Zhisuan affiliations, PRC-government-benefit allegations, and "
         "the FBI warrant chain), plus the criminal forfeiture "
         "allegation. Returned by the grand jury before Magistrate Judge "
         "Alex G. Tse.",
         "second_superseding_indictment"),
    ]
    prev_instrument: str | None = None
    for label, itype, name, filed, desc, doc_key in instruments:
        node_id = uid(label)
        graph.append(
            {
                "@id": node_id,
                "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
                "uco-core:name": name,
                "uco-core:description": desc + " " + src_ref(doc_key, "caption and counts"),
                "legalproc:instrumentType": itype,
                "uco-core:objectCreatedTime": lit("xsd:dateTime", pacific_midnight(filed)),
            }
        )
        graph.append(rel(node_id, doc_ids[doc_key], "Derived_From"))
        if prev_instrument:
            graph.append(rel(node_id, prev_instrument, "Supersedes"))
        prev_instrument = node_id

    # ------------------------------------------------------------------
    # Charges: original four § 1832 counts (superseded), then the
    # operative fourteen counts — Counts 1-7 theft of trade secrets
    # (§ 1832) and Counts 8-14 economic espionage (§ 1831), one per
    # Trade Secret Category.
    # ------------------------------------------------------------------
    original_counts = [
        (1, "Chip architecture and software design specifications for TPU version 4"),
        (2, "Chip architecture and software design specifications for TPU version 6"),
        (3, "Hardware, software, system management, and performance specifications for GPU chips deployed in Google's data centers"),
        (4, "Software design specifications for the Google CMS that managed machine learning workloads on TPU and GPU chips"),
    ]
    for num, item in original_counts:
        label = f"charge-orig-count{num}"
        graph.append(
            {
                "@id": uid(label),
                "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                "uco-core:name": f"Original Count {COUNT_WORDS[num - 1]}: Theft of Trade Secrets ({item})",
                "uco-core:description": (
                    f"Original indictment count charging theft of {item} "
                    "on or about and between 2022-06-01 and 2023-04-17; "
                    "superseded by the category-based counts of the "
                    "superseding indictments. "
                    + src_ref("indictment", "count table")
                ),
                "legalproc:statuteCitation": "18 U.S.C. § 1832(a)(1), (2), and (3)",
                "legalproc:countLabel": f"Count {COUNT_WORDS[num - 1]} (original)",
                "legalproc:countNumber": [lit("xsd:nonNegativeInteger", num)],
                "legalproc:offenseForm": "substantive",
                "legalproc:chargeClassification": "Felony",
                "legalproc:chargeDisposition": ["superseded"],
                "legalproc:assertedIn": [{"@id": uid("instrument-indictment")}],
            }
        )
        graph.append(rel(ding, uid(label), "Charged_With"))

    operative_charges: list[tuple[str, int]] = []  # (charge label, category num)
    for cat in TS_CATEGORIES:
        num = cat["num"]
        for offset, statute, offense, extra in (
            (0, "18 U.S.C. § 1832(a)(1), (2), and (3)", "Theft of Trade Secrets", ""),
            (7, "18 U.S.C. § 1831(a)(1), (2), and (3)", "Economic Espionage",
             " intending or knowing that the offense would benefit a "
             "foreign government, foreign instrumentality, or foreign "
             "agent,"),
        ):
            count_num = num + offset
            label = f"charge-count{count_num}"
            operative_charges.append((label, num))
            graph.append(
                {
                    "@id": uid(label),
                    "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
                    "uco-core:name": (
                        f"Count {COUNT_WORDS[count_num - 1]}: {offense} "
                        f"(Trade Secret Category {num})"
                    ),
                    "uco-core:description": (
                        f"On or about and between 2022-05-21 and "
                        f"2024-01-13, in the Northern District of "
                        f"California and elsewhere, Ding,{extra} knowingly "
                        "stole, copied, transmitted, and possessed without "
                        f"authorization Trade Secret Category {num}: "
                        + cat["desc"] + " "
                        + src_ref("second_superseding_indictment",
                                  "counts table")
                    ),
                    "legalproc:statuteCitation": statute,
                    "legalproc:countLabel": f"Count {COUNT_WORDS[count_num - 1]}",
                    "legalproc:countNumber": [lit("xsd:nonNegativeInteger", count_num)],
                    "legalproc:offenseForm": "substantive",
                    "legalproc:chargeClassification": "Felony",
                    "legalproc:chargeDisposition": ["convicted-by-verdict (2026-01-29)"],
                    "legalproc:assertedIn": [
                        {"@id": uid("instrument-superseding")},
                        {"@id": uid("instrument-second-superseding")},
                    ],
                }
            )
            graph.append(rel(ding, uid(label), "Charged_With"))
            graph.append(rel(uid(label), ts_ids[num], "Concerns"))
            graph.append(rel(google, uid(label), "Victim_Of"))

    # The exfiltration action is the charged conduct for every count.
    for label, _num in operative_charges:
        graph.append(rel(uid("act-exfiltration-uploads"), uid(label), "Basis_Of"))

    # ------------------------------------------------------------------
    # Forfeiture allegation
    # ------------------------------------------------------------------
    forfeiture = uid("forfeiture-allegation")
    graph.append(
        {
            "@id": forfeiture,
            "@type": ["legalproc:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Criminal forfeiture allegation (Second Superseding Indictment)",
            "uco-core:description": (
                "Forfeiture under 18 U.S.C. §§ 981(a)(1)(C), 1834, and "
                "2323 and 28 U.S.C. § 2461(c) of any property used or "
                "intended to be used to commit or facilitate the "
                "offenses, and any property constituting or derived from "
                "proceeds, including a money judgment equal to the total "
                "proceeds; substitute assets reachable under 21 U.S.C. "
                "§ 853(p) as incorporated by 18 U.S.C. § 2323(b). "
                + src_ref("second_superseding_indictment", "paras. 47-48")
            ),
            "legalproc:concernsCharge": [
                {"@id": uid(label)} for label, _ in operative_charges
            ],
        }
    )
    graph.append(rel(forfeiture, doc_ids["second_superseding_indictment"], "Derived_From"))

    # ------------------------------------------------------------------
    # Trial and verdict: guilty on all fourteen counts (2026-01-29),
    # with per-count unanimous trade-secret findings.
    # ------------------------------------------------------------------
    trial = uid("proceeding-jury-trial")
    graph.append(
        {
            "@id": trial,
            "@type": ["legalproc:CriminalProceeding", "uco-core:UcoObject"],
            "uco-core:name": "Jury trial before Judge Vince Chhabria (verdict returned 2026-01-29)",
            "uco-core:description": (
                "Trial on the fourteen counts of the Second Superseding "
                "Indictment; the verdict form (Doc 367) records unanimous "
                "findings for Ding on each count, with per-category "
                "identification of the documents the jury unanimously "
                "agreed constitute trade secrets. Presiding juror signed "
                "2026-01-29. Sentencing had not occurred in the modeled "
                "record. " + src_ref("jury_verdict", "pp. 1-15")
            ),
            "legalproc:proceedingType": "trial",
        }
    )
    graph.append(rel(trial, investigation, "part_of"))

    for label, num in operative_charges:
        count_num = int(label.removeprefix("charge-count"))
        verdict_label = f"verdict-count{count_num}"
        graph.append(
            {
                "@id": uid(verdict_label),
                "@type": ["legalproc:Verdict", "uco-core:UcoObject"],
                "uco-core:name": (
                    f"Guilty verdict on Count {COUNT_WORDS[count_num - 1]} "
                    f"(Trade Secret Category {num})"
                ),
                "uco-core:description": (
                    "Unanimous jury finding of guilty, with the verdict "
                    f"form's Category {num} table identifying which "
                    "exhibits (and/or the combination of all documents in "
                    "the category) the jury unanimously agreed constitute "
                    "a trade secret. "
                    + src_ref("jury_verdict", f"Count {COUNT_WORDS[count_num - 1]} page")
                ),
                "legalproc:verdictType": "guilty",
                "legalproc:concernsCharge": [{"@id": uid(label)}],
            }
        )
        graph.append(rel(uid(verdict_label), trial, "Occurred_During"))
        graph.append(rel(uid(verdict_label), ding, "Relates_To"))
    for count_num in range(1, 15):
        graph.append(
            rel(uid(f"verdict-count{count_num}"), doc_ids["jury_verdict"], "Derived_From")
        )

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
