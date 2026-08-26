# Racketeering (RICO) and Criminal Enterprise Investigations

Model a racketeering prosecution — the charged **enterprise** (including
association-in-fact enterprises that are not legal entities), the
**functional roles** members serve within it, the **predicate categories**
of racketeering activity enumerated in the RICO count, multi-instrument
multi-defendant charge tracking, and the enterprise's conduct — using the
`rico` extension together with `legalproc` (and `cryptoinv` when the
enterprise deals in virtual assets).

**When to use this recipe**

- 18 U.S.C. § 1962 (RICO) counts, including § 1962(d) conspiracy
- Any "criminal enterprise / organization" case where the division of
  labor matters: who hacked, who called, who laundered, who burgled
- Cases spanning several superseding indictments with per-defendant
  count suffixes (PACER's `1`, `1s`, `1ss` convention)
- State racketeering analogues (the classes are jurisdiction-neutral)

Charges, pleas, sentences, and forfeiture mechanics come from
`docs/recipes/legal-process-modeling.md` and apply unchanged. Crypto
laundering patterns come from `docs/recipes/fraud-crypto-laundering.md`.

## The extension

`extensions/rico/` adds the three concepts racketeering needs beyond
`legalproc`:

| Term | Purpose |
|---|---|
| `rico:RacketeeringEnterprise` | the charged enterprise, subclass of `uco-identity:Organization`; `enterpriseType` records the § 1961(4) branch (`association-in-fact` / `legal-entity`) |
| `rico:EnterpriseRole` | one functional position in the division of labor, subclass of `uco-role:Role`; `roleFunction` holds the function (`caller`, `money-launderer`, ...) |
| `rico:predicateStatute` | repeatable, domain-free string on the RICO charge node; one value per statutory category of racketeering activity enumerated in the count (§ 1961(1)) |

Enable with `CASE_UCO_EXTENSIONS=rico,legalproc` and validate with
`validate_graph(graph_path, extensions=["rico", "legalproc"])`.

## The enterprise is an Organization, not prose

An association-in-fact enterprise needs only a purpose, relationships
among associates, and longevity (*Boyle v. United States*, 556 U.S. 938
(2009)). Model it once, and hang everything else off it:

```json
{
  "@id": "kb:org-se-enterprise",
  "@type": ["rico:RacketeeringEnterprise", "uco-identity:Organization"],
  "uco-core:name": "The Social Engineering Enterprise (SE Enterprise)",
  "uco-core:description": "Group of individuals associated in fact although not a legal entity (18 U.S.C. § 1961(4)), engaged in and affecting interstate and foreign commerce; operated from no later than October 2023 through at least May 2025. Purposes: stealing virtual currency through fraudulent pretenses; disguising the stolen funds through virtual-currency laundering; converting laundered funds to fiat and luxury goods.",
  "rico:enterpriseType": "association-in-fact"
}
```

- Charged purposes and the commerce nexus go in `uco-core:description`,
  verbatim from the indictment's "Purposes of the Enterprise" section.
- Membership is a `uco-core:Relationship` of registered kind `Related_To`
  from each person to the enterprise, with membership stated in
  `uco-core:description`. Assert membership only where a reviewed
  document places the person in the enterprise — being a co-defendant is
  not membership (e.g. an obstruction-only defendant).
- The operating span ("began no later than X, continued through at least
  Y") maps to the enterprise-conduct action's `startTime`/`endTime`.

## Roles are nodes: the division of labor survives as graph structure

RICO indictments allege a division of labor in a dedicated section
("Defendants' Roles in the Enterprise"). Keep it queryable — one
`EnterpriseRole` node per function. Use registered `Related_To` from person
to role and role to enterprise, with bearer-role and role-within-enterprise
semantics in `uco-core:description`:

```json
{
  "@id": "kb:role-money-launderer",
  "@type": ["rico:EnterpriseRole", "uco-role:Role"],
  "uco-core:name": "SE Enterprise role: money launderer",
  "uco-core:description": "Money launderers were responsible for receiving stolen virtual currency and turning it into fiat US currency as bulk cash or wire transfer, or providing luxury services...",
  "rico:roleFunction": "money-launderer"
}
```

Several persons share one role, and one person holds several roles
(an organizer who also launders gets two described `Related_To` role edges). Unindicted
associates keep their charging-document designations
("COCONSPIRATOR M.F.", "MONEY EXCHANGER-1") as `uco-identity:Person`
nodes — never speculate about the identity behind initials, even when an
alias looks like a match for a named defendant.

Recommended `roleFunction` values (open vocabulary, keep close to the
charging language): `organizer`, `leader`, `database-hacker`,
`target-identifier`, `caller`, `money-launderer`, `money-exchanger`,
`residential-burglar`, `courier`, `enforcer`, `recruiter`,
`straw-owner`, `promoter`.

## Predicates on the RICO charge, not in a comment

The RICO count enumerates the statutory categories of racketeering
activity forming the charged pattern. Repeat `rico:predicateStatute`
once per category on the charge node:

```json
{
  "@id": "kb:charge-lam-1ss",
  "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
  "uco-core:name": "Malone Lam — Count 1ss: RICO Conspiracy",
  "legalproc:statuteCitation": "18 U.S.C. § 1962(d)",
  "legalproc:offenseForm": "conspiracy",
  "legalproc:countLabel": "Count 1ss",
  "rico:predicateStatute": [
    "18 U.S.C. § 1028 (fraud and related activity in connection with identification documents)",
    "18 U.S.C. § 1029 (fraud and related activity in connection with access devices)",
    "18 U.S.C. § 1343 (wire fraud)",
    "18 U.S.C. § 1512 (tampering with a witness, victim, or an informant)",
    "18 U.S.C. § 1956 (laundering of monetary instruments)",
    "18 U.S.C. § 1957 (engaging in monetary transactions in property derived from specified unlawful activity)",
    "18 U.S.C. § 1960 (illegal money transmitters)",
    "18 U.S.C. § 2314 (interstate transportation of stolen property)"
  ]
}
```

The predicates are properties of the count as charged — give every
defendant's RICO charge node the same list (build it once in code). The
pattern requirement (at least two acts within ten years, § 1961(5))
belongs in the charge description.

## Multi-instrument count tracking

Large RICO cases accumulate charging instruments; PACER suffixes count
labels per instrument (`1` original, `1s` superseding, `1ss` second
superseding). Conventions that keep the docket reconstructible:

- One `legalproc:ChargingInstrument` node per instrument, including a
  sealed original described only from the docket (say so in the
  description).
- Charge nodes per defendant on their **operative** instrument, with
  `countLabel` kept verbatim from the docket ("Count 1ss") and
  `countNumber` the bare integer.
- When the docket header, minute entries, and statement of offense label
  the same count differently (they do), pick the plea-colloquy label and
  record the discrepancy in the description.
- Docket dispositions map to `chargeDisposition`: `pending`,
  `convicted-by-plea`, `dismissed` ("Dismissed on Oral Motion by the
  Government" at sentencing is `dismissed`).
- The money-laundering-conspiracy count's specified unlawful activity is
  usually the wire-fraud count: link with `legalproc:objectOffense`.

## Enterprise conduct: overt acts as Actions

Model the overall pattern as one long-running `uco-action:Action`
performed by the enterprise node, and the significant overt acts as
individual Actions performed by the members. `uco-action:performer` is
max-1; use `uco-action:participant` for co-actors. Link acts to the counts
they support with registered `Related_To` and state the basis in
`uco-core:description`.
Where the enterprise launders virtual assets, put
`cryptoinv:launderingTechnique` values on the laundering actions
(`peel-chain`, `chain-hopping-to-monero`, `no-kyc-exchange`,
`crypto-to-cash`) and model no-KYC exchanges as
`cryptoinv:VirtualAssetServiceProvider`.

## Worked example

`examples/pacer/ddc_2024_cr_00417/build_lam_ddc_2024_racketeering.py`
builds the full graph for *U.S. v. Lam et al.*, No. 1:24-cr-00417-CKK
(D.D.C.) — the "SE Enterprise" RICO conspiracy (a social-engineering
enterprise that stole approximately $245M in virtual currency from a
single victim): 17 defendants, three charging instruments, 41 charge
nodes with docket dispositions, six enterprise roles, nine guilty pleas,
three imposed sentences, forfeiture-listed USDT addresses, and the
obstruction chain (phone into Biscayne Bay, remote camera surveillance
of the FBI search, directed device destruction). It validates with
`extensions=["legalproc", "rico", "cryptoinv"]` — `Conforms: True`.

## Validation

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/rico/rico.ttl \
  --ontology-graph extensions/rico/rico-shapes.ttl \
  --ontology-graph extensions/legalproc/legalproc.ttl \
  --ontology-graph extensions/legalproc/legalproc-shapes.ttl \
  --inference rdfs --allow-info \
  my-racketeering-graph.jsonld
```

Add the `cryptoinv` graphs when crypto facets are present.

## Anti-patterns

- **Enterprise as description text on the Investigation.** The
  enterprise is a first-class Organization; theft-ring cases become
  un-queryable when the enterprise exists only as prose.
- **Roles buried in person descriptions.** "X was a money launderer for
  the ring" in a description cannot answer "who laundered?"; a role node
  can.
- **Equating initials with defendants.** "COCONSPIRATOR M.F." may look
  like a named defendant post-plea, but unless a reviewed document makes
  the identification, keep separate nodes.
- **One charge node shared by all defendants.** Dispositions diverge per
  defendant (one pleads, one goes to trial, one is dismissed); charges
  must be per-defendant per-count.
- **Membership from co-defendant status.** An obstruction-only defendant
  charged in the same indictment is not thereby an enterprise member.
