# Background

Cryptocurrency addresses (Bitcoin, Ethereum, Litecoin, etc.) are increasingly encountered in digital forensics, financial crime investigations, and sanctions compliance. Government authorities such as OFAC (Office of Foreign Assets Control) maintain sanctions lists that include cryptocurrency addresses associated with designated persons and entities. Tools like the [Chainalysis Sanctions Screening API](https://www.chainalysis.com/free-cryptocurrency-sanctions-screening-tools/) enable investigators and compliance teams to check whether a blockchain address has been included in a sanctions designation.

Currently, the UCO ontology has no class or facet for modeling cryptocurrency addresses. The closest existing concepts are:

- **`DigitalAddress` / `DigitalAddressFacet`** — designed for "routing and management of digital communication" (IP, MAC, email, Bluetooth, etc.), not financial instruments on a distributed ledger.
- **`DigitalAccount` / `DigitalAccountFacet`** — models login-based accounts with properties like `accountLogin`, `firstLoginTime`, and `isDisabled`, none of which apply to permissionless blockchain addresses.
- **`PaymentCard`** — models physical payment cards issued by financial institutions, not decentralized cryptocurrency wallets.
- **`AccountFacet`** — has `accountType` and `accountIssuer`, but cryptocurrency addresses are not "issued" by an entity and don't fit the account-with-an-issuer model.

Additionally, there is no mechanism to model that an observable object (such as a cryptocurrency address) has been placed on a government sanctions list — including the designating authority, the specific list, the designation date, and the associated entity name.

**What do we achieve for whom and why does that matter?** We enable forensic examiners, financial investigators, and compliance analysts to model cryptocurrency addresses and their sanctions designations in CASE/UCO-compliant graphs, allowing structured querying across cases involving sanctioned blockchain activity — a rapidly growing area of digital investigation.


# Requirements


## Requirement 1

Define a new `CryptocurrencyAddressFacet` class as a subclass of `uco-observable:Facet` with properties for the blockchain address value, cryptocurrency type, and network identifier. This facet is attached to an `ObservableObject` to represent a cryptocurrency address (wallet address) observed during an investigation.


## Requirement 2

Define a new open vocabulary `CryptocurrencyTypeVocab` enumerating common cryptocurrency identifiers (e.g., BTC, ETH, LTC, XMR, ZEC, DASH, BTG, ETC) to constrain the `cryptocurrencyType` property on `CryptocurrencyAddressFacet`.


## Requirement 3

Define a new `SanctionsDesignationFacet` class as a subclass of `uco-observable:Facet` with properties for the designating authority, sanctions list name, designation category, designation name, associated entity description, designation date, and source URL. This facet captures the structured output of a sanctions screening check (such as the Chainalysis Sanctions Screening API response) and is attached to the `ObservableObject` being screened.


# Risk / Benefit analysis


## Benefits

1. **Closes a critical modeling gap**: Cryptocurrency tracing is now central to ransomware, money laundering, terrorism financing, and sanctions evasion investigations. Without dedicated classes, investigators must resort to unstructured free-text fields or non-standard extensions, undermining interoperability.

2. **Enables structured SPARQL querying**: Investigators can query across cases for all addresses of a given cryptocurrency type, all addresses flagged by OFAC, or all addresses associated with a specific sanctions designation — none of which is possible today.

3. **Aligns with real-world tooling**: The proposed `SanctionsDesignationFacet` properties map directly to the [Chainalysis Sanctions Screening API](https://files.buildwithfern.com/chainalysis-auth.docs.buildwithfern.com/221362a9139c6a05876fe6df43c6001fe2a1e6d48b602d4a3299866b00a709f3/apis/sanctions-screening/sanctions-screening-openapi.yaml) response schema (`category`, `name`, `description`, `url`), making it straightforward for tool vendors to produce compliant output.

4. **Interoperability across agencies**: A standardized representation of sanctioned cryptocurrency addresses enables cross-agency sharing (e.g., FinCEN, FBI, Europol) using a common vocabulary.

5. **Extensible to non-cryptocurrency sanctions**: While motivated by cryptocurrency, the `SanctionsDesignationFacet` is generic enough to apply to any `ObservableObject` that may appear on a sanctions list (e.g., IP addresses, domain names, email addresses).


## Risks

- The cryptocurrency ecosystem evolves rapidly. New blockchain networks and address formats emerge frequently. The open vocabulary (`CryptocurrencyTypeVocab`) mitigates this by allowing user-defined values while providing a recommended baseline.
- Sanctions designations are jurisdiction-specific (OFAC is US-based). The facet should remain jurisdiction-neutral by using `designatingAuthority` as a free-text field rather than constraining to a specific authority.
- The submitter is unaware of other risks associated with this change.


# Competencies demonstrated


## Competency 1

**Scenario**: A financial crimes unit is investigating a ransomware group that demands payment in Bitcoin. During the investigation, an analyst uses the Chainalysis Sanctions Screening API to check several Bitcoin addresses extracted from the ransom note. One address (`1da5821544e25c636c1417ba96ade4cf6d2f9b5a`) returns a positive sanctions hit — it was designated by OFAC on the SDN list in connection with "Secondeye Solution," a synthetic identity document vendor linked to the Russian Internet Research Agency (IRA). The analyst also checks Litecoin address `LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd`, which is designated under OFAC SDN for individual Dmitrii Karasavidi. A third address (`0x123`) returns no sanctions match.

The investigation models all three addresses, captures the Chainalysis screening results, and records which forensic tool performed the check.


### Competency Question 1.1

**Which cryptocurrency addresses in the case have been designated under sanctions, and by which authority?**

#### Result 1.1

| Address | Cryptocurrency | Authority | Designation |
|---|---|---|---|
| `1da5821544e25c636c1417ba96ade4cf6d2f9b5a` | ETH | OFAC | SDN — Secondeye Solution (2021-04-15) |
| `LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd` | LTC | OFAC | SDN — Dmitrii Karasavidi (2020-09-16) |

```sparql
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/>

SELECT ?address ?cryptoType ?authority ?designationName ?designationDate
WHERE {
    ?obj a uco-observable:ObservableObject ;
         uco-core:hasFacet ?cryptoFacet ;
         uco-core:hasFacet ?sanctionsFacet .
    ?cryptoFacet a proposed:CryptocurrencyAddressFacet ;
                 proposed:addressValue ?address ;
                 proposed:cryptocurrencyType ?cryptoType .
    ?sanctionsFacet a proposed:SanctionsDesignationFacet ;
                    proposed:designatingAuthority ?authority ;
                    proposed:designationName ?designationName .
    OPTIONAL { ?sanctionsFacet proposed:designationDate ?designationDate }
}
ORDER BY ?designationDate
```


### Competency Question 1.2

**Which cryptocurrency addresses were screened but found NOT to be on any sanctions list?**

This is the ground-truth negative: address `0x123` was screened by Chainalysis and returned an empty identifications array. The absence of a `SanctionsDesignationFacet` on the observable, combined with a recorded `InvestigativeAction` showing the screening was performed, distinguishes "not sanctioned" from "not yet checked."

#### Result 1.2

| Address | Cryptocurrency | Screening Tool | Screening Time |
|---|---|---|---|
| `0x123` | ETH | Chainalysis Sanctions Screening API | 2025-03-26T14:30:00Z |

```sparql
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-action: <https://ontology.unifiedcyberontology.org/uco/action/>
PREFIX case-investigation: <https://ontology.caseontology.org/case/investigation/>
PREFIX proposed: <http://example.org/ontology/proposed/>

SELECT ?address ?cryptoType ?toolName ?actionTime
WHERE {
    ?action a case-investigation:InvestigativeAction ;
            uco-action:object ?obj ;
            uco-action:instrument ?tool ;
            uco-action:startTime ?actionTime .
    ?tool uco-core:name ?toolName .
    ?obj a uco-observable:ObservableObject ;
         uco-core:hasFacet ?cryptoFacet .
    ?cryptoFacet a proposed:CryptocurrencyAddressFacet ;
                 proposed:addressValue ?address ;
                 proposed:cryptocurrencyType ?cryptoType .
    FILTER NOT EXISTS {
        ?obj uco-core:hasFacet ?sanctionsFacet .
        ?sanctionsFacet a proposed:SanctionsDesignationFacet .
    }
}
```


### Competency Question 1.3

**What is the full OFAC narrative for a given sanctioned cryptocurrency address?**

#### Result 1.3

For address `1da5821544e25c636c1417ba96ade4cf6d2f9b5a`:

> Pakistan-based Secondeye Solution (SES), also known as Forwarderz, is a synthetic identity document vendor that was added to the OFAC SDN list in April 2021. SES customers could buy fake identity documents to sign up for accounts with cryptocurrency exchanges, payment providers, banks, and more under false identities. According to the US Treasury Department, SES assisted the Internet Research Agency (IRA), the Russian troll farm that OFAC designated pursuant to E.O. 13848 in 2018 for interfering in the 2016 presidential election, in concealing its identity to evade sanctions.

Source: https://home.treasury.gov/news/press-releases/jy0126

```sparql
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/>

SELECT ?description ?sourceURL
WHERE {
    ?obj a uco-observable:ObservableObject ;
         uco-core:hasFacet ?cryptoFacet ;
         uco-core:hasFacet ?sanctionsFacet .
    ?cryptoFacet a proposed:CryptocurrencyAddressFacet ;
                 proposed:addressValue "1da5821544e25c636c1417ba96ade4cf6d2f9b5a" .
    ?sanctionsFacet a proposed:SanctionsDesignationFacet ;
                    proposed:designationDescription ?description ;
                    proposed:designationSourceURL ?sourceURL .
}
```


# Solution suggestion

## 1. Define `CryptocurrencyAddressFacet` (`uco-observable`)

New class `CryptocurrencyAddressFacet` as a subclass of `uco-observable:Facet`:

| Property | Type | Cardinality | Description |
|---|---|---|---|
| `addressValue` | `xsd:string` | 1 | The cryptocurrency address string (e.g., `1da5821544e25c636c1417ba96ade4cf6d2f9b5a`) |
| `cryptocurrencyType` | `xsd:string` (open vocab `CryptocurrencyTypeVocab`) | 0..1 | The type of cryptocurrency (e.g., BTC, ETH, LTC) |
| `blockchainNetwork` | `xsd:string` | 0..1 | The blockchain network the address belongs to (e.g., "Bitcoin Mainnet", "Ethereum") |
| `addressFormat` | `xsd:string` | 0..1 | The encoding format of the address (e.g., "Base58Check", "Bech32", "Hex") |

## 2. Define `CryptocurrencyTypeVocab` (`uco-vocabulary`)

New open vocabulary with initial members:

`BTC`, `ETH`, `LTC`, `XMR`, `ZEC`, `DASH`, `BTG`, `ETC`, `BCH`, `XRP`, `DOGE`, `SOL`, `ADA`, `DOT`, `AVAX`, `MATIC`, `USDT`, `USDC`

## 3. Define `SanctionsDesignationFacet` (`uco-observable`)

New class `SanctionsDesignationFacet` as a subclass of `uco-observable:Facet`:

| Property | Type | Cardinality | Description |
|---|---|---|---|
| `designatingAuthority` | `xsd:string` | 1 | The authority that issued the sanctions designation (e.g., "OFAC", "EU Council", "UN Security Council") |
| `designationCategory` | `xsd:string` | 0..1 | The category of designation as reported by the screening service (e.g., "sanctions") |
| `designationName` | `xsd:string` | 0..1 | The official designation name or label (e.g., "SANCTIONS: OFAC SDN Secondeye Solution 2021-04-15 ...") |
| `designationDescription` | `xsd:string` | 0..1 | A narrative description of the designation and the designated entity |
| `designationDate` | `xsd:dateTime` | 0..1 | The date the designation was issued |
| `listName` | `xsd:string` | 0..1 | The specific sanctions list (e.g., "SDN", "Consolidated Sanctions List") |
| `designationSourceURL` | `xsd:anyURI` | 0..1 | A URL to the official designation source or press release |

## 4. Add SHACL shapes

- `CryptocurrencyAddressFacet-shape`: Enforce `addressValue` as required (min 1)
- `SanctionsDesignationFacet-shape`: Enforce `designatingAuthority` as required (min 1)

## 5. Add unit tests

- Validate that a `CryptocurrencyAddressFacet` with a missing `addressValue` is rejected
- Validate that a `SanctionsDesignationFacet` with a missing `designatingAuthority` is rejected
- Validate a complete example with both facets on a single `ObservableObject`


# Example instance data

The following JSON-LD demonstrates the proposed classes modeling the Chainalysis Sanctions Screening API scenario. I am fine with my examples being transcribed and credited.

```json
{
  "@context": {
    "@vocab": "http://example.org/kb/",
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "proposed": "http://example.org/ontology/proposed/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:investigation-1",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "Ransomware Payment Tracing 2025-RC-0042"
    },
    {
      "@id": "kb:tool-chainalysis",
      "@type": "uco-tool:Tool",
      "uco-core:name": "Chainalysis Sanctions Screening API",
      "uco-tool:version": "1.0.0"
    },
    {
      "@id": "kb:address-sanctioned-eth",
      "@type": "uco-observable:ObservableObject",
      "uco-core:hasFacet": [
        {
          "@type": "proposed:CryptocurrencyAddressFacet",
          "proposed:addressValue": "1da5821544e25c636c1417ba96ade4cf6d2f9b5a",
          "proposed:cryptocurrencyType": "ETH",
          "proposed:blockchainNetwork": "Ethereum",
          "proposed:addressFormat": "Hex"
        },
        {
          "@type": "proposed:SanctionsDesignationFacet",
          "proposed:designatingAuthority": "OFAC",
          "proposed:designationCategory": "sanctions",
          "proposed:designationName": "SANCTIONS: OFAC SDN Secondeye Solution 2021-04-15 1da5821544e25c636c1417ba96ade4cf6d2f9b5a",
          "proposed:designationDescription": "Pakistan-based Secondeye Solution (SES), also known as Forwarderz, is a synthetic identity document vendor that was added to the OFAC SDN list in April 2021. SES customers could buy fake identity documents to sign up for accounts with cryptocurrency exchanges, payment providers, banks, and more under false identities.",
          "proposed:designationDate": { "@type": "xsd:dateTime", "@value": "2021-04-15T00:00:00Z" },
          "proposed:listName": "SDN",
          "proposed:designationSourceURL": { "@type": "xsd:anyURI", "@value": "https://home.treasury.gov/news/press-releases/jy0126" }
        }
      ]
    },
    {
      "@id": "kb:address-sanctioned-ltc",
      "@type": "uco-observable:ObservableObject",
      "uco-core:hasFacet": [
        {
          "@type": "proposed:CryptocurrencyAddressFacet",
          "proposed:addressValue": "LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd",
          "proposed:cryptocurrencyType": "LTC",
          "proposed:blockchainNetwork": "Litecoin",
          "proposed:addressFormat": "Base58Check"
        },
        {
          "@type": "proposed:SanctionsDesignationFacet",
          "proposed:designatingAuthority": "OFAC",
          "proposed:designationCategory": "sanctions",
          "proposed:designationName": "SANCTIONS: OFAC SDN Dmitrii Karasavidi 2020-09-16 LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd",
          "proposed:designationDescription": "This specific address LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd within the cluster has been identified as belonging to an individual on OFAC's SDN list.",
          "proposed:designationDate": { "@type": "xsd:dateTime", "@value": "2020-09-16T00:00:00Z" },
          "proposed:listName": "SDN",
          "proposed:designationSourceURL": { "@type": "xsd:anyURI", "@value": "https://home.treasury.gov/policy-issues/financial-sanctions/recent-actions/20200916" }
        }
      ]
    },
    {
      "@id": "kb:address-clean",
      "@type": "uco-observable:ObservableObject",
      "uco-core:hasFacet": [
        {
          "@type": "proposed:CryptocurrencyAddressFacet",
          "proposed:addressValue": "0x123",
          "proposed:cryptocurrencyType": "ETH",
          "proposed:blockchainNetwork": "Ethereum",
          "proposed:addressFormat": "Hex"
        }
      ]
    },
    {
      "@id": "kb:screening-action-1",
      "@type": "case-investigation:InvestigativeAction",
      "uco-core:name": "Sanctions screening of suspect cryptocurrency addresses",
      "uco-action:instrument": { "@id": "kb:tool-chainalysis" },
      "uco-action:object": [
        { "@id": "kb:address-sanctioned-eth" },
        { "@id": "kb:address-sanctioned-ltc" },
        { "@id": "kb:address-clean" }
      ],
      "uco-action:startTime": { "@type": "xsd:dateTime", "@value": "2025-03-26T14:30:00Z" },
      "uco-action:endTime": { "@type": "xsd:dateTime", "@value": "2025-03-26T14:30:05Z" }
    },
    {
      "@id": "kb:relationship-investigation-action",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:screening-action-1" },
      "uco-core:target": { "@id": "kb:investigation-1" },
      "uco-core:kindOfRelationship": "part_of",
      "uco-core:isDirectional": true
    }
  ]
}
```

# Chainalysis API reference

The proposed `SanctionsDesignationFacet` properties map directly to the [Chainalysis Sanctions Screening API v1](https://files.buildwithfern.com/chainalysis-auth.docs.buildwithfern.com/221362a9139c6a05876fe6df43c6001fe2a1e6d48b602d4a3299866b00a709f3/apis/sanctions-screening/sanctions-screening-openapi.yaml) response schema:

| API response field | Proposed property | Notes |
|---|---|---|
| `identifications[].category` | `designationCategory` | Always "sanctions" for OFAC designations |
| `identifications[].name` | `designationName` | Includes authority, list, entity name, date, and address |
| `identifications[].description` | `designationDescription` | Narrative from the designating authority |
| `identifications[].url` | `designationSourceURL` | Link to official source (e.g., Treasury press release) |
| *(not in response — from request)* | `designatingAuthority` | Inferred from the screening service; "OFAC" for Chainalysis sanctions hits |
| *(not in response — parsed from name)* | `designationDate` | Extracted from the designation name string |
| *(not in response — parsed from name)* | `listName` | Extracted from the designation name (e.g., "SDN") |

**Target repository**: **UCO** — both concepts (cryptocurrency addresses and sanctions designations) describe general cyber-observable data with utility beyond the investigation process. Cryptocurrency addresses exist on public blockchains, and sanctions designations are published by government authorities for use in compliance, banking, and law enforcement.
