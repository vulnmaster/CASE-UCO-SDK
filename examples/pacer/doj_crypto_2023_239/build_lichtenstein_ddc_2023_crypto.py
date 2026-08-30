#!/usr/bin/env python3
"""Build validated JSON-LD for U.S. v. Lichtenstein & Morgan (D.D.C. crypto laundering).

The 2016 Bitfinex hack money-laundering prosecution: theft of ~119,754 BTC
via >2,000 unauthorized transactions, a multi-year laundering conspiracy
(peel chains, darknet-market pass-throughs, chain hopping to XMR, mixers,
fictitious-identity exchange accounts), the January 2022 seizure of ~94,636
BTC from Wallet 1CGA4s, guilty pleas, and the government's sentencing
recommendation with in-kind restitution to Bitfinex.

Sources (PACER, Case 1:23-cr-00239-CKK, D.D.C.):
  - Information:              Document 89  (filed 2023-07-20)
  - Statement of Facts:       Document 1-1 (filed 2022-02-07, criminal complaint affidavit)
  - Statement of the Offense: Document 95  (filed 2023-08-03)
  - Plea Agreement:           Document 96  (filed 2023-08-03)
  - Sentencing Memorandum:    Document 146 (filed 2024-10-15)

MCP extraction artifacts: examples/pacer/doj_crypto_2023_239/mcp_outputs/*.jsonld

Extension: extensions/cryptoinv (Cryptocurrency and Financial Crime
Investigation Extension) — cryptocurrency observable facets tracking UCO
issue #675 (revised, sanctions excluded) plus criminal legal process classes.

Source-fidelity conventions:
  - Court-filing dates are date-only facts; they are rendered as local
    midnight Eastern time with the correct seasonal UTC offset (documented
    fabrication-free convention, matching the Anchorage exemplar).
  - Approximate quantities from the record keep the precision printed in
    the source document (e.g. 94,643.29837084 BTC from the Information's
    forfeiture allegation; 94,636 BTC seized per the Statement of Facts).
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

CASE_ID = "lichtenstein-ddc-2023-crypto"
NS = f"https://example.org/cryptoinv/{CASE_ID}/"
OUTPUT = Path(__file__).resolve().parent / "lichtenstein-ddc-2023-crypto.jsonld"

PACER_DOCKET = "1:23-cr-00239-CKK"
MAGISTRATE_DOCKET = "22-mj-22 (RMM)"
LOCAL_REF = "outside_pacer -- crypto"

SOURCE_DOCS = {
    "information": {
        "file_name": "pacer -- crypto -- Information.pdf",
        "sha256": "45a71110d032a3c0a398695cceff0efabb0d15149c7824f5a4d031410bdcd010",
        "pacer_doc": "89",
        "filed": "2023-07-20",
    },
    "statement_of_facts": {
        "file_name": "pacer -- crypto -- statement of facts.pdf",
        "sha256": "3caca302d4278e9a17f6b56e5bf43799ae94ae1d0d5273859ababc39a2498bbe",
        "pacer_doc": "1-1",
        "filed": "2022-02-07",
    },
    "statement_of_offense": {
        "file_name": "pacer -- crypto -- Statement of Offense.pdf",
        "sha256": "45e104b86f2e72e9ed374e04dcb247d4f5f1438f1dce4a30f2d13657078bc744",
        "pacer_doc": "95",
        "filed": "2023-08-03",
    },
    "plea_agreement": {
        "file_name": "pacer -- crypto -- Plea Agreement.pdf",
        "sha256": "74a9e7b2dc38f916ebb5ffab9186ecb90eac92b428888234bdc7962d8dad6c03",
        "pacer_doc": "96",
        "filed": "2023-08-03",
    },
    "sentencing_memorandum": {
        "file_name": "pacer -- crypto -- Sentencing Memorandum.pdf",
        "sha256": "a08a7cad2028033e218036c8acaa98047e8576099d548c04fcd7883bc6fc2cc8",
        "pacer_doc": "146",
        "filed": "2024-10-15",
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


def eastern_midnight(date_str: str) -> str:
    """Date-only court-filing fact rendered at local midnight Eastern time.

    D.D.C. filings: EDT (-04:00) roughly March-November, EST (-05:00)
    otherwise. Month-level approximation is sufficient for filing dates.
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
            f"PACER Document {meta['pacer_doc']} filed {meta['filed']} in "
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


def holding(label: str, symbol: str, quantity: str, *, fiat: str = "", fiat_date: str = "") -> dict:
    node = {
        "@id": uid(label),
        "@type": ["cryptoinv:VirtualAssetHoldingFacet", "uco-core:Facet"],
        "cryptoinv:assetSymbol": symbol,
        "cryptoinv:assetQuantity": lit("xsd:decimal", quantity),
    }
    if fiat:
        node["cryptoinv:fiatValue"] = lit("xsd:decimal", fiat)
        node["cryptoinv:fiatCurrencyCode"] = "USD"
    if fiat_date:
        node["cryptoinv:valuationDate"] = lit("xsd:dateTime", eastern_midnight(fiat_date))
    return node


def eth_address(label: str, address: str, description: str) -> dict:
    return {
        "@id": uid(label),
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": address,
        "uco-core:description": description,
        "uco-core:hasFacet": [
            {
                "@id": uid(f"{label}-addr-facet"),
                "@type": ["cryptoinv:CryptocurrencyAddressFacet", "uco-core:Facet"],
                "cryptoinv:addressValue": address,
                "cryptoinv:cryptocurrencyType": "ETH",
                "cryptoinv:blockchainNetwork": "Ethereum",
                "cryptoinv:addressFormat": "Hex",
            }
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
            "uco-core:name": f"United States v. Lichtenstein & Morgan, {PACER_DOCKET} (D.D.C.)",
            "uco-core:description": (
                "Investigation and federal prosecution of the laundering of "
                "approximately 119,754 BTC stolen in the August 2016 hack of the "
                "virtual currency exchange Bitfinex. Investigated by IRS-CI, FBI, "
                f"and HSI; charged by criminal complaint ({MAGISTRATE_DOCKET}) on "
                "2022-02-07 and by Information (Doc 89) on 2023-07-20. "
                + src_ref("statement_of_facts", "paras. 1-10")
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
    lichtenstein = uid("person-lichtenstein")
    morgan = uid("person-morgan")
    bitfinex = uid("org-bitfinex")
    alphabay = uid("org-alphabay")
    hydra = uid("org-hydra")
    mixers = {
        "bitcoin-fog": ("Bitcoin Fog", uid("org-bitcoin-fog")),
        "helix": ("Helix", uid("org-helix")),
        "chipmixer": ("ChipMixer", uid("org-chipmixer")),
    }
    fincen = uid("org-fincen")
    irs_ci = uid("org-irs-ci")

    graph.extend(
        [
            {
                "@id": lichtenstein,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Ilya Lichtenstein",
                "uco-core:description": (
                    "Also known as 'Dutch'; citizen of Russia and the United States, "
                    "resident of New York and/or California. Admitted to hacking the "
                    "victim exchange and to the money laundering conspiracy. "
                    + src_ref("statement_of_offense", "paras. 1, 12-17")
                ),
                "cryptoinv:chargedWith": [{"@id": uid("charge-count1")}],
            },
            {
                "@id": morgan,
                "@type": ["uco-identity:Person", "uco-core:UcoObject"],
                "uco-core:name": "Heather Rhiannon Morgan",
                "uco-core:description": (
                    "Citizen of the United States; married Lichtenstein in or around "
                    "January 2019. Assisted the laundering while initially unaware of "
                    "the specific origin of the funds; told no later than early 2020 "
                    "that Lichtenstein was responsible for the 2016 hack. "
                    + src_ref("statement_of_offense", "paras. 2-3, 20")
                ),
                "cryptoinv:chargedWith": [
                    {"@id": uid("charge-count2")},
                    {"@id": uid("charge-count3")},
                ],
            },
            {
                "@id": bitfinex,
                "@type": ["cryptoinv:VirtualAssetServiceProvider", "uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Bitfinex",
                "uco-core:description": (
                    "The victim virtual currency exchange ('VICTIM VCE'), one of the "
                    "world's largest virtual currency exchanges, doing business "
                    "globally. Hacked in August 2016. "
                    + src_ref("statement_of_offense", "para. 4")
                ),
            },
            {
                "@id": alphabay,
                "@type": ["cryptoinv:DarknetMarket", "uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "AlphaBay",
                "uco-core:description": (
                    "Darknet market (operated December 2014 - July 2017) used as a "
                    "pass-through to break up the stolen-BTC trail on the blockchain. "
                    + src_ref("statement_of_facts", "paras. 11-12 and n.12")
                ),
            },
            {
                "@id": hydra,
                "@type": ["cryptoinv:DarknetMarket", "uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Hydra",
                "uco-core:description": (
                    "Darknet marketplace through which stolen funds were moved using "
                    "multiple segregated input and withdrawal addresses. "
                    + src_ref("statement_of_offense", "para. 19")
                ),
            },
            {
                "@id": fincen,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "Financial Crimes Enforcement Network (FinCEN)",
                "uco-core:description": (
                    "Division of the U.S. Department of the Treasury responsible for "
                    "implementation, administration, and enforcement of the Bank "
                    "Secrecy Act; headquartered in Washington, D.C. Object of the "
                    "Count Three conspiracy to defraud the United States. "
                    + src_ref("statement_of_facts", "paras. 56-59")
                ),
            },
            {
                "@id": irs_ci,
                "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": "IRS Criminal Investigation (IRS-CI)",
                "uco-core:description": (
                    "Lead tracing agency; affiant Special Agent Christopher Janczewski. "
                    "Investigated jointly with FBI and HSI. "
                    + src_ref("statement_of_facts", "paras. 1-3")
                ),
            },
        ]
    )
    for slug, (name, org_id) in mixers.items():
        graph.append(
            {
                "@id": org_id,
                "@type": ["cryptoinv:CryptocurrencyMixingService", "uco-identity:Organization", "uco-core:UcoObject"],
                "uco-core:name": name,
                "uco-core:description": (
                    "Cryptocurrency mixing service used to launder a portion of the "
                    "stolen funds. " + src_ref("statement_of_offense", "para. 19")
                ),
            }
        )

    graph.append(rel(morgan, lichtenstein, "Married_To", directional=False))
    graph.append(rel(bitfinex, investigation, "part_of"))

    # ------------------------------------------------------------------
    # The hack (2016) and the stolen funds
    # ------------------------------------------------------------------
    hack_action = uid("action-2016-hack")
    graph.append(
        {
            "@id": hack_action,
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": "August 2016 hack of Bitfinex and theft of ~119,754 BTC",
            "uco-core:description": (
                "After online reconnaissance, Lichtenstein compromised Bitfinex "
                "servers located outside the United States using advanced hacking "
                "tools and penetration-testing software, concealing his activity via "
                "the Tor network, compromised computers purchased on an RDP "
                "marketplace, and rented SOCKS residential proxies. He gained access "
                "to the keys used to authorize transactions and in August 2016 "
                "fraudulently authorized more than 2,000 transactions transferring "
                "approximately 119,754 BTC (then valued at approximately $71 million) "
                "from Bitfinex's wallets to Wallet 1CGA4s under his custody and "
                "control, then deleted access credentials and log files. He also used "
                "stolen customer credentials for credential spraying against another "
                "exchange (VCE A). " + src_ref("statement_of_offense", "paras. 12-16")
            ),
            "uco-action:performer": [{"@id": lichtenstein}],
            "uco-action:object": [{"@id": bitfinex}],
        }
    )

    hack_wallet = uid("wallet-1cga4s")
    graph.append(
        {
            "@id": hack_wallet,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Wallet 1CGA4s",
            "uco-core:description": (
                "Unhosted (self-hosted) wallet under Lichtenstein's custody and "
                "control that received the stolen BTC; contained a list of 2,000 "
                "virtual currency addresses and corresponding private keys, saved in "
                "an encrypted file in Lichtenstein's cloud storage account. The "
                "majority of the stolen funds remained here from August 2016 until "
                "the January 2022 seizure. "
                + src_ref("statement_of_facts", "paras. 4-7, 51-52")
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("wallet-1cga4s-facet"),
                    "@type": ["cryptoinv:CryptocurrencyWalletFacet", "uco-core:Facet"],
                    "cryptoinv:walletType": "unhosted",
                    "cryptoinv:walletIdentifier": "Wallet 1CGA4s",
                    "cryptoinv:addressCount": lit("xsd:nonNegativeInteger", 2000),
                },
                holding(
                    "wallet-1cga4s-holding",
                    "BTC",
                    "94636",
                    fiat="3629000000",
                    fiat_date="2022-02-01",
                ),
            ],
        }
    )
    graph.append(rel(hack_wallet, lichtenstein, "Controlled_By"))
    graph.append(rel(hack_wallet, hack_action, "Derived_From"))

    cluster_36b6mu = uid("wallet-cluster-36b6mu")
    graph.append(
        {
            "@id": cluster_36b6mu,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Cluster 36B6mu",
            "uco-core:description": (
                "BTC cluster frequently used as an intermediary between VCE "
                "withdrawals and accounts owned by Lichtenstein and Morgan; "
                "approximately 177.116 BTC flowed through it between 2019-02-11 and "
                "2020-12-14, including 16 gift-card purchases at VCE 10. "
                + src_ref("statement_of_facts", "paras. 45-50")
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("wallet-cluster-36b6mu-facet"),
                    "@type": ["cryptoinv:CryptocurrencyWalletFacet", "uco-core:Facet"],
                    "cryptoinv:walletType": "unhosted",
                    "cryptoinv:walletIdentifier": "Cluster 36B6mu",
                },
            ],
        }
    )
    graph.append(rel(cluster_36b6mu, lichtenstein, "Controlled_By"))
    graph.append(rel(cluster_36b6mu, morgan, "Controlled_By"))

    # Representative forfeiture-listed transaction and Ethereum addresses
    # (Information, Doc 89, forfeiture allegation para. 12(a) and 12(f)).
    seized_tx = uid("tx-forfeiture-6e0d701a")
    graph.append(
        {
            "@id": seized_tx,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Seizure transaction 6e0d701a…",
            "uco-core:description": (
                "First of 24 recipient transactions listed in the Information's "
                "forfeiture allegation for approximately 94,643.29837084 BTC (after "
                "required fees) seized from wallets recovered from the defendants' "
                "online storage account. "
                + src_ref("information", "forfeiture allegation para. 12(a)")
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("tx-forfeiture-6e0d701a-facet"),
                    "@type": ["cryptoinv:CryptocurrencyTransactionFacet", "uco-core:Facet"],
                    "cryptoinv:transactionHash": (
                        "6e0d701ac2ea3ad87fc8bcaa786b994aa943f5eb9a67a1e345769bb090bf5b9e"
                    ),
                    "cryptoinv:blockchainNetwork": "Bitcoin Mainnet",
                    "cryptoinv:transactionType": "Transfer",
                    "cryptoinv:transactionStatus": "Confirmed",
                },
            ],
        }
    )
    graph.append(
        {
            "@id": uid("tx-forfeiture-input"),
            "@type": ["uco-observable:ObservableRelationship", "uco-core:UcoObject"],
            "uco-core:source": [{"@id": hack_wallet}],
            "uco-core:target": [{"@id": seized_tx}],
            "uco-core:kindOfRelationship": "Transaction_Input",
            "uco-core:isDirectional": lit("xsd:boolean", True),
        }
    )

    eth_addresses = [
        eth_address(
            "addr-eth-8ce693",
            "0x8CE693CB0626924583931F25f50AF8fC1C6517F0",
            "Stolen virtual currency wallet holding approximately 8.56 ETH and "
            "approximately 4,507.99 USDC, plus various other ERC-20 tokens. "
            + src_ref("information", "forfeiture allegation para. 12(f)"),
        ),
        eth_address(
            "addr-eth-331865",
            "0x331865e142ACA526B9f75464A2B597ECdaCAF557",
            "Stolen virtual currency wallet holding approximately 13.88 ETH, "
            "approximately 6,656,048 aUSDC, and approximately 120 WETH, plus "
            "various other tokens. "
            + src_ref("information", "forfeiture allegation para. 12(f)"),
        ),
        eth_address(
            "addr-eth-3b2cd2",
            "0x3b2Cd27cE5a8633160bC7875B35009f010a51B21",
            "Stolen virtual currency wallet holding approximately 80 WETH and "
            "approximately 0.39 ETH. "
            + src_ref("information", "forfeiture allegation para. 12(f)"),
        ),
    ]
    eth_holdings = {
        "addr-eth-8ce693": [("ETH", "8.56"), ("USDC", "4507.99")],
        "addr-eth-331865": [("ETH", "13.88"), ("aUSDC", "6656048"), ("WETH", "120")],
        "addr-eth-3b2cd2": [("WETH", "80"), ("ETH", "0.39")],
    }
    for node in eth_addresses:
        label = [k for k in eth_holdings if uid(k) == node["@id"]][0]
        for symbol, qty in eth_holdings[label]:
            node["uco-core:hasFacet"].append(holding(f"{label}-holding-{symbol}", symbol, qty))
        graph.append(node)

    # ------------------------------------------------------------------
    # Laundering conduct
    # ------------------------------------------------------------------
    laundering = uid("action-laundering")
    graph.append(
        {
            "@id": laundering,
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": "Money laundering of Bitfinex hack proceeds (2017-2022)",
            "uco-core:description": (
                "Beginning in or around January 2017, a portion of the stolen BTC "
                "moved out of Wallet 1CGA4s in a series of small, complex "
                "transactions across multiple accounts and platforms, ultimately "
                "totaling about 25,000 BTC withdrawn. Techniques: fictitious-identity "
                "accounts; thousands of small transactions; automated transaction "
                "programs; layering through VCEs and darknet markets (AlphaBay, "
                "Hydra); chain hopping to anonymity-enhanced virtual currency "
                "(Monero) and to stablecoins (USDT, USDC); coinjoins and mixers "
                "(Bitcoin Fog, Helix, ChipMixer); U.S. business accounts to "
                "legitimize activity; Russian/Ukrainian money-mule bank accounts "
                "with debit-card ATM withdrawals; purchases of gold coins (buried by "
                "Morgan and later recovered in full), NFTs, and Walmart gift cards. "
                + src_ref("statement_of_offense", "paras. 18-23")
            ),
            "uco-action:performer": [{"@id": lichtenstein}],
            "uco-action:object": [{"@id": hack_wallet}],
            "cryptoinv:launderingTechnique": [
                "peel-chain",
                "layering",
                "chain-hopping",
                "mixing",
                "coinjoin",
                "fictitious-identity-accounts",
                "automated-transactions",
                "business-account-legitimization",
                "money-mule-accounts",
                "fiat-conversion",
                "gift-card-purchase",
                "nft-purchase",
                "precious-metals-purchase",
            ],
        }
    )
    # uco-action:performer is max-1; Morgan's assistance is modeled as a
    # relationship (Statement of the Offense paras. 20-23).
    graph.append(rel(morgan, laundering, "Participated_In"))
    for org_id in (alphabay, hydra, *[m[1] for m in mixers.values()]):
        graph.append(rel(laundering, org_id, "Used"))
    graph.append(rel(laundering, hack_action, "Derived_From"))
    graph.append(rel(laundering, cluster_36b6mu, "Used"))
    graph.append(rel(laundering, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Investigative actions: tracing, decryption, seizure
    # ------------------------------------------------------------------
    tracing = uid("action-blockchain-tracing")
    graph.append(
        {
            "@id": tracing,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Blockchain tracing of stolen BTC to Lichtenstein and Morgan accounts",
            "uco-core:description": (
                "IRS-CI, FBI, and HSI traced the stolen funds from Wallet 1CGA4s "
                "through AlphaBay, seven interconnected accounts at VCE 1 and "
                "accounts at VCE 2-4 (registered with an India-based email provider "
                "in third-party names), unhosted BTC wallets, and Cluster 36B6mu to "
                "true-name accounts at VCE 5-10 and U.S. financial institutions, "
                "using public blockchain analysis and exchange records. "
                + src_ref("statement_of_facts", "paras. 5, 7-10, 13-50")
            ),
            "uco-action:performer": [{"@id": irs_ci}],
            "uco-action:object": [{"@id": hack_wallet}, {"@id": cluster_36b6mu}],
        }
    )
    graph.append(rel(tracing, investigation, "part_of"))

    cloud_account = uid("observable-cloud-storage")
    graph.append(
        {
            "@id": cloud_account,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "Lichtenstein cloud storage account",
            "uco-core:description": (
                "Cloud storage account (Lichtenstein Email 2 provider) obtained by "
                "search warrant in 2021; significant portions encrypted. On "
                "2022-01-31 law enforcement decrypted key files, including a file "
                "listing all 2,000 Wallet 1CGA4s addresses with private keys, an "
                "exchange-account spreadsheet with 'FROZEN' notations, a 'personas' "
                "folder of false identity documents, a 'passport_ideas' darknet "
                "vendor list, and financial-institution laundering reconnaissance "
                "notes. " + src_ref("statement_of_facts", "paras. 51-55")
            ),
        }
    )
    graph.append(rel(cloud_account, lichtenstein, "Controlled_By"))

    decryption = uid("action-decryption")
    graph.append(
        {
            "@id": decryption,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Decryption of cloud-stored wallet key file",
            "uco-core:description": (
                "On or about 2022-01-31, law enforcement decrypted files in "
                "Lichtenstein's cloud storage account, recovering the Wallet 1CGA4s "
                "address/private-key list that enabled the seizure. "
                + src_ref("statement_of_facts", "paras. 6, 52")
            ),
            "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2022-01-31")),
            "uco-action:object": [{"@id": cloud_account}],
            "uco-action:result": [{"@id": hack_wallet}],
        }
    )
    graph.append(rel(decryption, investigation, "part_of"))

    seizure = uid("action-seizure")
    graph.append(
        {
            "@id": seizure,
            "@type": ["cryptoinv:AssetSeizureAction", "case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "Seizure of ~94,636 BTC from Wallet 1CGA4s",
            "uco-core:description": (
                "Between 2022-01-31 and 2022-02-01, law enforcement obtained "
                "approval for a lawful seizure supported by probable cause under "
                "exigent circumstances and used the recovered private keys to seize "
                "Wallet 1CGA4s's remaining balance of approximately 94,636 BTC, "
                "worth $3.629 billion. A seizure warrant issued 2022-02-04. "
                + src_ref("statement_of_facts", "para. 6")
            ),
            "uco-action:startTime": lit("xsd:dateTime", eastern_midnight("2022-01-31")),
            "uco-action:endTime": lit("xsd:dateTime", eastern_midnight("2022-02-01")),
            "uco-action:object": [{"@id": hack_wallet}],
        }
    )
    graph.append(rel(seizure, decryption, "Derived_From"))
    graph.append(rel(seizure, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Charges (Information, Doc 89)
    # ------------------------------------------------------------------
    charges = [
        (
            "charge-count1",
            1,
            "Money Laundering Conspiracy",
            "18 U.S.C. § 1956(h)",
            "Lichtenstein conspired (August 2016 - February 2022) to conduct "
            "financial transactions involving proceeds of wire fraud (18 U.S.C. "
            "§ 1343) and computer fraud and abuse (18 U.S.C. § 1030(a)(2)(C), "
            "(a)(4)), designed to conceal the nature, location, source, ownership, "
            "and control of the proceeds. " + src_ref("information", "Count One"),
        ),
        (
            "charge-count2",
            2,
            "Conspiracy To Commit Money Laundering",
            "18 U.S.C. § 371",
            "Morgan conspired (August 2016 - February 2022) with Lichtenstein to "
            "violate 18 U.S.C. § 1956(a)(1)(B)(i) by laundering proceeds of the "
            "Bitfinex hack. " + src_ref("information", "Count Two"),
        ),
        (
            "charge-count3",
            3,
            "Conspiracy To Defraud the United States",
            "18 U.S.C. § 371",
            "Morgan conspired with Lichtenstein to defraud the United States by "
            "deceiving VCEs and financial institutions to frustrate AML/KYC due "
            "diligence and prevent transmission of Bank Secrecy Act Suspicious "
            "Activity Reports to FinCEN. " + src_ref("information", "Count Three"),
        ),
    ]
    for label, count, desc, statute, narrative in charges:
        graph.append(
            {
                "@id": uid(label),
                "@type": ["cryptoinv:CriminalCharge", "uco-core:UcoObject"],
                "uco-core:name": f"Count {count}: {desc}",
                "uco-core:description": narrative,
                "cryptoinv:statuteCitation": statute,
                "cryptoinv:countNumber": lit("xsd:nonNegativeInteger", count),
                "cryptoinv:chargeDescription": desc,
            }
        )
        graph.append(rel(uid(label), doc_ids["information"], "Derived_From"))

    # ------------------------------------------------------------------
    # Plea agreement (Doc 96) and statement of offense (Doc 95)
    # ------------------------------------------------------------------
    plea = uid("plea-agreement-lichtenstein")
    graph.append(
        {
            "@id": plea,
            "@type": ["cryptoinv:PleaAgreement", "uco-core:UcoObject"],
            "uco-core:name": "Lichtenstein plea agreement",
            "uco-core:description": (
                "Lichtenstein agreed to plead guilty to Count One (18 U.S.C. "
                "§ 1956(h)): maximum 20 years imprisonment, fine of $500,000 or "
                "twice the value of property involved, supervised release up to 3 "
                "years, mandatory restitution (18 U.S.C. § 3663A), $100 special "
                "assessment. The agreement was contingent ('wired') on Morgan also "
                "entering a guilty plea, and stipulated the attached Statement of "
                "the Offense. Plea offer dated 2023-07-13; agreement filed "
                "2023-08-03. " + src_ref("plea_agreement", "sections 1-4")
            ),
            "cryptoinv:pleadsGuiltyTo": [{"@id": uid("charge-count1")}],
            "cryptoinv:pleaDate": lit("xsd:dateTime", eastern_midnight("2023-08-03")),
        }
    )
    graph.append(rel(plea, lichtenstein, "Relates_To"))
    graph.append(rel(plea, doc_ids["plea_agreement"], "Derived_From"))
    graph.append(rel(doc_ids["statement_of_offense"], plea, "Supports"))

    # ------------------------------------------------------------------
    # Sentencing recommendation (Doc 146)
    # ------------------------------------------------------------------
    sentencing = uid("sentencing-recommendation-lichtenstein")
    graph.append(
        {
            "@id": sentencing,
            "@type": ["cryptoinv:SentencingOutcome", "uco-core:UcoObject"],
            "uco-core:name": "Government sentencing recommendation for Lichtenstein",
            "uco-core:description": (
                "Citing substantial assistance, the government moved under U.S.S.G. "
                "§ 5K1.1 for a downward departure and recommended 60 months at "
                "offense level 25. The pre-departure Guidelines range at offense "
                "level 32, Criminal History Category I, would be 121-151 months. "
                "The government also proposed in-kind restitution to Bitfinex of "
                "forfeited cryptocurrency collectively valued at more than $6 "
                "billion at current prices. "
                + src_ref("sentencing_memorandum", "pp. 1-2 and restitution section")
            ),
            "cryptoinv:sentenceStatus": "recommended-government",
            "cryptoinv:sentenceDurationMonths": lit("xsd:nonNegativeInteger", 60),
            "cryptoinv:offenseLevel": lit("xsd:integer", 25),
            "cryptoinv:guidelineRangeLowMonths": lit("xsd:nonNegativeInteger", 121),
            "cryptoinv:guidelineRangeHighMonths": lit("xsd:nonNegativeInteger", 151),
            "cryptoinv:sentencingDate": lit("xsd:dateTime", eastern_midnight("2024-10-15")),
        }
    )
    graph.append(rel(sentencing, lichtenstein, "Relates_To"))
    graph.append(rel(sentencing, uid("charge-count1"), "Relates_To"))
    graph.append(rel(sentencing, doc_ids["sentencing_memorandum"], "Derived_From"))

    # ------------------------------------------------------------------
    # Forfeiture and restitution
    # ------------------------------------------------------------------
    forfeiture = uid("forfeiture-order")
    forfeited_ids = [hack_wallet, seized_tx] + [node["@id"] for node in eth_addresses]
    graph.append(
        {
            "@id": forfeiture,
            "@type": ["cryptoinv:ForfeitureOrder", "uco-core:UcoObject"],
            "uco-core:name": "Forfeiture allegation and consent order (Lichtenstein)",
            "uco-core:description": (
                "The Information's forfeiture allegation lists specific property "
                "including approximately 94,643.29837084 BTC, 117,376.52651940 BCH, "
                "117,376.58178024 BSV, 118,102.03258447 BTG, 29,016.98 XMR, Ethereum "
                "wallets and DeFi positions (USDC, aUSDC, aUSDT, USDT, yvUSDT, WETH, "
                "Curve DAO tokens), gold coins recovered from a buried location, "
                "funds from JPMorgan Chase, Wells Fargo, and Flagstar/Signature bank "
                "accounts, and BTC/ETH from an external hard drive recovered at the "
                "defendants' New York residence. In the plea agreement Lichtenstein "
                "consented to a forfeiture money judgment of $72,618,825.60 and to "
                "forfeiture of the specific listed property. "
                + src_ref("information", "forfeiture allegation paras. 10-13")
                + "; "
                + src_ref("plea_agreement", "forfeiture section")
            ),
            "cryptoinv:forfeits": [{"@id": fid} for fid in forfeited_ids],
            "cryptoinv:moneyJudgmentAmount": lit("xsd:decimal", "72618825.60"),
            "cryptoinv:moneyJudgmentCurrencyCode": "USD",
        }
    )
    graph.append(rel(forfeiture, lichtenstein, "Relates_To"))
    graph.append(rel(forfeiture, doc_ids["information"], "Derived_From"))

    restitution = uid("restitution-proposal")
    graph.append(
        {
            "@id": restitution,
            "@type": ["cryptoinv:RestitutionOrder", "uco-core:UcoObject"],
            "uco-core:name": "Proposed in-kind restitution to Bitfinex",
            "uco-core:description": (
                "The government proposed returning forfeited cryptocurrency — "
                "collectively valued at more than $6 billion at then-current prices "
                "— to Bitfinex as in-kind restitution under the Mandatory Victims "
                "Restitution Act, 18 U.S.C. § 3663A. "
                + src_ref("sentencing_memorandum", "restitution section")
            ),
            "cryptoinv:restitutionInKind": lit("xsd:boolean", True),
            "cryptoinv:restitutionDescription": (
                "In-kind restitution of forfeited cryptocurrency to victim exchange Bitfinex."
            ),
        }
    )
    graph.append(rel(restitution, bitfinex, "Relates_To"))
    graph.append(rel(restitution, forfeiture, "Derived_From"))
    graph.append(rel(restitution, doc_ids["sentencing_memorandum"], "Derived_From"))

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "cryptoinv": "http://example.org/ontology/cryptoinv/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
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
    report = validate_graph_file(path, extensions=["cryptoinv"], project_root=ROOT)
    print(report.safe_summary)
    paths = load_extension_ontology_paths("cryptoinv", mode="full", project_root=ROOT)
    print(f"Validated with {len(paths)} cryptoinv ontology files")
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
