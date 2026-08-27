# Federal Prosecution Relationship Completeness

> See [Recipe Index](INDEX.md) for all recipes.

Model **federal court prosecution graphs** from indictments, criminal complaints, superseding indictments, or hand-extracted fact files — covering single- and multi-defendant cases, **multi-district parallel prosecutions**, child exploitation **enterprise** prosecutions, and **CSAM production/possession/transport** cases.

This recipe focuses on **relationship completeness**: agents often populate typed nodes correctly but omit edges that connect defendants to counts, indictments to charges, prosecutions to districts, conduct to equipment, and forfeiture to enumerated devices. Use this recipe for **any** federal CAC prosecution graph, not only enterprise cases.

Based on validated patterns in `brooklyn-trafficking-april-2025-example.ttl`, `ceos-federal-law-example.ttl`, `rhode-island-production-case.ttl`, and community federal prosecution graphs.

## When to use this recipe

Use when the source describes:

- **Federal charges** (`FederalCharge`, `FederalProsecution`, `PreTrialPhase`)
- **Indictment or criminal complaint** with numbered counts
- **Single or multiple defendants** facing federal CAC counts
- **Multi-district parallel prosecution** (same defendant, charges in more than one federal district)
- **CSAM production, possession, transport, or receipt** under Title 18
- **Child exploitation enterprise** (18 U.S.C. § 2252A(g)) with co-conspirators
- **Forfeiture** of devices or proceeds alleged in the charging instrument

Pair with [cac-production-case.md](cac-production-case.md) for production-environment and equipment typing, and [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) for plea/sentencing follow-on. Plea facts use `legalproc:Plea` and `legalproc:PleaAgreement` (`legalproc:recordsPlea`). When the source is a press release, follow that recipe's fail-closed stage table: do not type bail, bond, or statutory maxima as imposed sentences, and keep `legalproc:outcomeScope` `current-case` versus `prior-history` distinct.

## Scope

**Layer 2 — Conduct / offense structure** composed with **Layer 3 — Federal legal workflow**:

- [cac-production-case.md](cac-production-case.md) — production equipment and produced media
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — charge nodes and sentencing
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) — forensic acquisition context
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) — ring structure when applicable
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) — enticement conduct

## Key classes

| Class | Role |
|---|---|
| `uco-core:Bundle` | Top-level case container |
| `CACInvestigation` | Investigation with `case-investigation:focus` |
| `FederalProsecution` / `PreTrialPhase` | Federal legal process (one per lead district) |
| `MultiDefendantIndictment` / charging instrument | Formal indictment or complaint node |
| `legalproc:FederalCharge` or `cacontology-legal-outcomes:FederalCharge` | Individual numbered counts; type as federal whenever the source establishes federal jurisdiction |
| `Person` / `Subject` / `OffenderRole` | Defendant and principal subject |
| `CSAMIncident` | Alleged exploitation conduct |
| `MobileRecordingDevice` | Production/forfeiture smartphones and cameras |
| `AssetForfeitureAction` | Forfeiture allegations |
| `Location` | Court and parallel-district jurisdictions |
| `ChildExploitationEnterprise` | Enterprise cases only (§ 2252A(g)) |
| `ConspiracyToCommitCSA` | Conspiracy anchor when alleged |
| `gufo:Relator` | Enterprise leadership/exploitation mediators |
| `uco-core:Relationship` | Cross-layer bridges (SHACL: UcoObject endpoints) |

## Universal relationship pattern

Agents should produce a **connected** graph, not a flat list of typed nodes inside a Bundle:

```
uco-core:Bundle
  ├── CACInvestigation
  │     ├── Related_To ──▶ charging instrument (indictment/complaint)
  │     ├── Related_To ──▶ FederalCharge set and/or CSAMIncident
  │     ├── Related_To ──▶ primary court Location (description: filing court)
  │     └── Related_To ──▶ parallel district Location(s) (description: parallel jurisdiction)
  │
  ├── FederalProsecution (per lead district)
  │     ├── cacontology-usa-federal-law:prosecutedBy ──▶ FederalProsecutorRole
  │     ├── cacontology-usa-federal-law:hasLegalPhase ──▶ PreTrialPhase
  │     └── Related_To ──▶ charging instrument
  │
  ├── charging instrument
  │     ├── indictmentCounts (literal)
  │     └── Related_To ──▶ each FederalCharge
  │
  ├── FederalCharge (one per count; prefix by district when multi-district)
  │     ├── chargeCount (literal)
  │     ├── Related_To ──▶ CSAMIncident or conduct event
  │     └── Related_To ──▶ district Location (multi-district cases)
  │
  ├── Person (each defendant)
  │     ├── cacontology-legal-outcomes:chargedWith ──▶ FederalCharge (subset per defendant)
  │     └── Related_To ──▶ Subject / OffenderRole (description: person bears principal role)
  │
  ├── CSAMIncident
  │     ├── participatesInEvent ◀── Subject
  │     └── Related_To / cacontology-production:usesEquipment ──▶ MobileRecordingDevice(s)
  │
  └── AssetForfeitureAction
        ├── cacontology-asset-forfeiture:targetedAsset ──▶ each enumerated device (not only aggregate stub)
        └── cacontology-asset-forfeiture:relatedCriminalCharges ──▶ supporting FederalCharge nodes
```

## Relationship completeness checklist

Before calling `validate_graph`, verify every applicable row:

| # | Edge | Required when | Property / pattern |
|---|---|---|---|
| 1 | **Defendant → counts** | Always | `cacontology-legal-outcomes:chargedWith` on **each** `Person` defendant → specific `FederalCharge` nodes. Never leave orphan charges. |
| 2 | **Indictment → charges** | Charges exist | `uco-core:Relationship` (`Related_To`) from charging instrument to **each** `FederalCharge`; set `indictmentCounts` and per-charge `chargeCount` literals. |
| 3 | **Prosecution → indictment** | Both exist | `uco-core:Relationship` (`Related_To`) from `FederalProsecution` to charging instrument. |
| 4 | **Investigation → legal scope** | Always | `Related_To` from `CACInvestigation` to indictment, prosecution, charges, and/or `CSAMIncident`. Focus-area text alone is insufficient. |
| 5 | **Charge → conduct** | Conduct nodes exist | `Related_To` or charge `uco-core:description` IRI references to `CSAMIncident`, conspiracy, or platform abuse. |
| 6 | **Principal subject role** | Lead defendant | Registered `Related_To` from principal `Person` to `Subject` / `OffenderRole`, with the bearer-role assertion in `uco-core:description`; `cacontology:participatesInEvent` on conduct. |
| 7 | **Multi-district charges → court** | Parallel districts | Each district-prefixed charge (`AK_1`, `TX_1`) gets `Related_To` → that district's `Location`. Add another `Related_To` from investigation to each non-primary district with `uco-core:description` = "parallel jurisdiction". |
| 8 | **Parallel prosecution** | Multiple district cases | One `FederalProsecution` per district (or document secondary district on parallel `Location` + link its charges). Do not collapse unrelated dockets into one prosecution node without edges. |
| 9 | **Conduct → equipment** | Devices alleged | Use `cacontology-production:usesEquipment` on production offense classes; otherwise link `CSAMIncident` to `MobileRecordingDevice` with registered `Related_To` and describe the equipment use. |
| 10 | **Forfeiture → devices + charges** | Forfeiture alleged | `targetedAsset` → **each** enumerated device (not only a generic aggregate stub). Add `relatedCriminalCharges` on `AssetForfeitureAction` per CAC SHACL. |
| 11 | **Provenance** | Court document sourced | `ProvenanceRecord` + extraction `InvestigativeAction`; mark `ALLEGED` where appropriate. |
| 12 | **Per-count defendant subsets** | Multi-defendant indictment | `DEFENDANT_COUNTS` must list **different count sets per defendant** when the source assigns subsets (not one flat list for all defendants). |
| 13 | **Enterprise overt-act violations** | Count 1 embeds Violation One/Two/… | Model each embedded violation as a conduct node with its own defendant subset, venue, and `Related_To` from enterprise charge. |
| 14 | **Charge → venue Location** | Count names a judicial district | Each count or violation gets `Related_To` → the `Location` for that venue (D. New Mexico, S.D. California, etc.), not only the filing court. |
| 15 | **Forfeiture serial observables** | Devices enumerated with serials | Each forfeiture device is a typed `ObservableObject` with serial/model in `uco-core:description` or `FileFacet`; link seizure location when stated. |
| 16 | **Transnational extradition chain** | Defendant abroad / extradited | Link declared `ExtraditionRequest` → defendant `Person` and `FederalProsecution` via `Related_To`; foreign residence as `InternationalJurisdiction` or `Location`. |
| 17 | **Financial charge stacking** | Wire fraud / identity theft counts | Link non-CSEA `FederalCharge` nodes (§ 1343, § 1028A) to underlying `SextortionIncident` or `CSAMIncident` via `Related_To`. |
| 18 | **Per-victim charge bundles** | Indictment names Minor Victim 1–N | `VICTIM_COUNTS` maps each victim to their counts; `Related_To` from each charge to victim role and conduct. |
| 19 | **Superseding indictment chain** | Original + superseding filed | Link original → superseding instrument; prosecution → current instrument. See [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md). |
| 20 | **Grouped forfeiture notices** | Multiple forfeiture allegation sections | Separate `AssetForfeitureAction` or grouped `relatedCriminalCharges` per statute block (2253, 1594, 2428). |

### Enterprise addendum (when § 2252A(g) alleged)

| # | Edge | Property / pattern |
|---|---|---|
| E1 | Enterprise → indictment | `Related_To` from `ChildExploitationEnterprise` to charging instrument |
| E2 | Conspiracy → indictment | `cacontology:resultsInIndictment` from `ConspiracyToCommitCSA` |
| E3 | Enterprise members | `hasMember` on enterprise → each defendant `Person` |
| E4 | Relator participants | Registered `Related_To` from every `gufo:Relator` to each participant, with the mediation role in `uco-core:description` (not label-only shells) |
| E5 | Platform usage | Declared domain property such as `cacontology-sextortion:conductsOnPlatform`; otherwise `Related_To` with the platform-use basis in `uco-core:description` |
| E6 | Overt-act violations inside Count 1 | Each **Violation** paragraph → `CSAMIncident` or overt-act node with `Related_To` from Count 1 `FederalCharge` and enterprise |
| E7 | Violation defendant subsets | `chargedWith` and `participatesInEvent` reflect **only** defendants named in that violation, not all enterprise members |
| E8 | Violation venue | Each violation `Related_To` → venue `Location` when the indictment names a district (e.g., D. New Mexico, S.D. California) |

## Enterprise Count 1 overt-act / violation matrix

Many § 2252A(g) indictments embed **multiple felony violations inside Count One** before separate numbered counts begin. Each violation is a mini-count with its own defendants, venue, date range, and minor victim reference.

**Do not flatten** Count 1 into a single enterprise node with no violation subgraph.

```
FederalCharge (Count 1 — Enterprise § 2252A(g))
  ├── Related_To ──▶ ChildExploitationEnterprise
  ├── Related_To ──▶ OvertActViolation-1 (CSAMIncident or Event)
  │     ├── Related_To ──▶ Location (D. New Mexico)
  │     ├── participatesInEvent ◀── Defendant-A, Defendant-B (subset only)
  │     └── Related_To ──▶ Minor Victim reference (aggregate or anonymized)
  ├── Related_To ──▶ OvertActViolation-2
  │     ├── Related_To ──▶ Location (S.D. California)
  │     └── participatesInEvent ◀── Defendant-C, Defendant-D
  └── ...

FederalCharge (Count 4 — Access with intent)
  ├── chargedWith ◀── Defendant-A, Defendant-C, Defendant-E  (different subset)
  └── Related_To ──▶ Location (E.D.N.Y.)
```

Modeling rules:

1. Create one `FederalCharge` per **numbered count** in the instrument (Counts 2–10 remain separate nodes).
2. For Count 1, add one conduct node per **embedded violation** (name from indictment: "Violation One", "Violation Two", …).
3. Wire `Related_To` from Count 1 to each violation node and from each violation to its venue `Location`.
4. Apply `chargedWith` on each defendant for Count 1 **and** for each separate count — subsets differ per count.
5. Use `uco-core:description` on violation nodes for date ranges and victim ordinal references when individual victim nodes are out of scope.

## Per-count venue (intra-case multi-venue)

Distinct from **multi-district parallel prosecution** (separate dockets), a single indictment may allege conduct **in multiple judicial districts** within one case (e.g., E.D.N.Y. filing court with overt acts in D. New Mexico and S.D. California).

1. Model the **filing court** as a `Location` linked from `CACInvestigation` with registered `Related_To` and `uco-core:description` = "filing court".
2. Model **each venue named in a count or violation** as its own `Location` with district name in `uco-core:name`.
3. Link each `FederalCharge` or overt-act node to the venue where that count alleges conduct occurred.
4. Do not collapse all venues into the filing court description — agents need queryable venue edges.

```
CACInvestigation
  └── cacontology:located_at ──▶ E.D.N.Y. (filing court)

FederalCharge (Count 4)
  └── Related_To ──▶ E.D.N.Y. Location

OvertActViolation-1 (inside Count 1)
  └── Related_To ──▶ D. New Mexico Location
```

## Multi-district parallel prosecution

When the same defendant faces charges in **more than one federal district** (e.g., D. Alaska `3:24-cr-00091` and W.D. Texas `3:25-cr-01046`):

1. Model **each district court** as a `Location` node with case number and filing date in `uco-core:description`.
2. Prefix charge IRIs by district (`charge-AK_1`, `charge-TX_1`) and link each charge to its district court.
3. Add registered `Related_To` from `CACInvestigation` to each non-primary district and set `uco-core:description` = "parallel jurisdiction".
4. Optionally add a **second `FederalProsecution`** node for the parallel district with its own `prosecutedBy` role.
5. Apply `chargedWith` on the defendant for **all** counts across districts in one `Person` node (same defendant, multiple dockets).

```
CACInvestigation
  ├── cacontology:located_at ──▶ D. Alaska (primary)
  ├── Related_To ──▶ W.D. Texas (description: parallel jurisdiction)
  └── Related_To ──▶ all FederalCharge nodes

FederalCharge (AK_1)
  └── Related_To ──▶ D. Alaska Location

FederalCharge (TX_1)
  └── Related_To ──▶ W.D. Texas Location
```

## Production equipment and forfeiture

When indictments enumerate **specific devices** for seizure/forfeiture:

1. Type each device as `MobileRecordingDevice` + `ObservableObject` with `deviceBrand`, `deviceModel`, `equipmentType`.
2. Record **serial numbers**, capacity, and seizure location in `uco-core:description` or `FileFacet` when the forfeiture schedule lists them (common in enterprise indictments).
3. Link conduct → device (this edge is often done correctly — preserve it).
4. Link **forfeiture → each device** via `targetedAsset` (multiple assertions allowed).
5. Link **forfeiture → charges** via `relatedCriminalCharges`.
6. Do not leave a generic `forfeiture-asset` stub disconnected from enumerated device nodes when the source names them.

Prefer `cacontology-production:usesEquipment` when the conduct node is a `ProductionOffense` subclass; use registered `Related_To` plus a precise equipment-use description for `CSAMIncident` when no direct property exists.

### Enumerated forfeiture example (serial numbers)

```text
FORFEITURE_DEVICES:
  SanDisk SSD 2TB — serial S/N-001 — seized Hawaii
  iBUYPOWER desktop tower — serial S/N-002 — seized New Mexico
  Seagate HDD 4TB — serial S/N-003 — seized New Mexico
```

Each line becomes a distinct `ObservableObject` node; `AssetForfeitureAction.targetedAsset` references all of them.

## Fact-file template for agents

```text
CASE_ID: 3:24-cr-00091-SLG-KFR
PRIMARY_COURT: U.S. District Court, District of Alaska
FILING_DATE: 2024-08-22
DEFENDANTS: 1
EVIDENTIARY_BASIS: ALLEGED

DEFENDANT_COUNTS:
  Defendant-1: AK_1,AK_2,AK_3,TX_1,TX_2

COUNTS:
  AK_1: Transportation of CSAM — 18 U.S.C. 2252A(a)(1),(b)(1) — District of Alaska
  AK_2: Receipt of CSAM — 18 U.S.C. 2252A(a)(2),(b)(1) — District of Alaska
  AK_3: Possession of CSAM — 18 U.S.C. 2252A(a)(5)(B),(b)(2) — District of Alaska
  TX_1: Attempted sexual exploitation — 18 U.S.C. 2251(a),(e) — W.D. Texas
  TX_2: Receipt of CSAM — 18 U.S.C. 2252(a)(2),(b)(1) — W.D. Texas

PARALLEL_CASES:
  W.D. Texas: 3:25-cr-01046 — filed 2025-05-14 — counts TX_1, TX_2

FORFEITURE_DEVICES:
  Samsung Galaxy S21 Ultra
  Samsung Galaxy S23 Ultra
  Samsung Galaxy S8+

FORFEITURE_STATUTE: 18 U.S.C. 2253
CONDUCT_WINDOW: 2021-03-07 to 2024-05-14
FOCUS_AREAS: CSAM Production; CSAM Possession; Multi-District Prosecution
```

`DEFENDANT_COUNTS` and `PARALLEL_CASES` are the highest-value inputs for edge completeness.

### Multi-defendant enterprise example (per-count subsets)

```text
CASE_ID: 1:25-cr-00361-PKC
PRIMARY_COURT: U.S. District Court, Eastern District of New York
FILING_DATE: 2025-11-18
DEFENDANTS: 6
EVIDENTIARY_BASIS: ALLEGED

DEFENDANT_COUNTS:
  BERMUDEZ: 1,2,3,4,5,6,7,8,9,10
  BRILHANTE: 1,2,3
  DOSCH: 1,2,3,5,7
  RODRIGUEZ: 1,2,3,4,6,8
  VALDEZ: 1,2,3,4,5,6,7,8,9
  Defendant-6: 1,2,3

COUNT_VENUES:
  1-Violation-1: District of New Mexico
  1-Violation-3: Southern District of California
  4: Eastern District of New York
  5: Eastern District of New York

FORFEITURE_DEVICES:
  SanDisk SSD 2TB — serial per schedule
  iBUYPOWER desktop — serial per schedule
```

Note how **each defendant's count list differs** — agents must not assign all ten counts to every defendant.

### Per-victim charge bundle example (solo defendant)

```text
CASE_ID: 1:23-cr-00071-JMS
DEFENDANTS: 1
DEFENDANT_COUNTS:
  RILEY: 1,2,3,4,5,6,7,8,9,10,11,12

VICTIM_COUNTS:
  MV1: 1,2,12
  MV2: 3,4,5
  MV3: 6,7,8
  MV4: 9,10
  MV5: 11

CHARGING_INSTRUMENTS:
  Original: Doc 1 — 2023-08-24 — counts 1-2
  Superseding: Doc 70 — 2024-07-25 — counts 1-12 (active)
```

`VICTIM_COUNTS` drives charge→victim and charge→conduct edges when one defendant faces stacked statutes across multiple minors.

## Python skeleton (multi-district production case)

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
    "cacontology-production": "https://cacontology.projectvic.org/production#",
    "cacontology-asset-forfeiture": "https://cacontology.projectvic.org/asset-forfeiture#",
})

inv = graph.add_node("kb:inv-1", [
    "case-investigation:Investigation", "cacontology:CACInvestigation",
], {
    "uco-core:name": "U.S. v. Defendant-1 — 3:24-cr-00091",
    "case-investigation:focus": ["CSAM Production", "Multi-District Prosecution"],
})

court_ak = graph.add_node("kb:court-ak", "uco-location:Location", {
    "uco-core:name": "U.S. District Court, District of Alaska",
})
court_tx = graph.add_node("kb:court-tx", "uco-location:Location", {
    "uco-core:name": "U.S. District Court, Western District of Texas (El Paso)",
})

indictment = graph.add_node("kb:indictment-1", "cacontology:MultiDefendantIndictment", {
    "uco-core:name": "Federal indictment — D. Alaska and W.D. Texas",
    "cacontology:indictmentCounts": {"@type": "xsd:nonNegativeInteger", "@value": "5"},
})

prosecution = graph.add_node("kb:prosecution-1", "cacontology-usa-federal-law:FederalProsecution", {
    "uco-core:name": "Federal prosecution — D. Alaska",
})

charge_ak1 = graph.add_node("kb:charge-ak-1", "cacontology-legal-outcomes:FederalCharge", {
    "uco-core:name": "Count AK-1 — Transportation of CSAM",
    "cacontology-legal-outcomes:chargeCount": {"@type": "xsd:nonNegativeInteger", "@value": "1"},
})

device = graph.add_node("kb:device-1", [
    "uco-observable:ObservableObject",
    "cacontology-production:MobileRecordingDevice",
], {
    "uco-core:name": "Samsung Galaxy S21 Ultra",
    "cacontology-production:deviceBrand": "Samsung",
    "cacontology-production:deviceModel": "Galaxy S21 Ultra",
})

csam = graph.add_node("kb:csam-1", "cacontology:CSAMIncident", {
    "uco-core:name": "Alleged CSAM production and possession",
})

defendant = graph.add_node("kb:defendant-1", "uco-identity:Person", {
    "uco-core:name": "Defendant-1",
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-ak-1"}],
})

forfeiture = graph.add_node("kb:forfeiture-1", "cacontology-asset-forfeiture:AssetForfeitureAction", {
    "uco-core:name": "Alleged asset forfeiture under 18 U.S.C. 2253",
    "cacontology-asset-forfeiture:targetedAsset": {"@id": "kb:device-1"},
    "cacontology-asset-forfeiture:relatedCriminalCharges": [{"@id": "kb:charge-ak-1"}],
})

# Relationship edges (representative set)
for rel_id, src, tgt, description in [
    ("rel-inv-indictment", "kb:inv-1", "kb:indictment-1", "Investigation charging instrument"),
    ("rel-prosecution-indictment", "kb:prosecution-1", "kb:indictment-1", "Current prosecution charging instrument"),
    ("rel-indictment-charge", "kb:indictment-1", "kb:charge-ak-1", "Charge alleged by indictment"),
    ("rel-charge-court", "kb:charge-ak-1", "kb:court-ak", "Venue for this charge"),
    ("rel-charge-conduct", "kb:charge-ak-1", "kb:csam-1", "Underlying alleged conduct"),
    ("rel-inv-parallel", "kb:inv-1", "kb:court-tx", "Parallel jurisdiction"),
    ("rel-conduct-device", "kb:csam-1", "kb:device-1", "Equipment allegedly used in conduct"),
]:
    graph.add_node(f"kb:{rel_id}", "uco-core:Relationship", {
        "uco-core:source": {"@id": src},
        "uco-core:target": {"@id": tgt},
        "uco-core:kindOfRelationship": "Related_To",
        "uco-core:description": description,
        "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
    })

graph.write("federal-prosecution-relationships.jsonld")
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| 5 `FederalCharge` nodes, 0 `chargedWith` | Add `chargedWith` from `DEFENDANT_COUNTS` |
| Charges and indictment in Bundle only | Add indictment `Related_To` each charge |
| `FederalProsecution` disconnected from indictment | Add prosecution `Related_To` indictment |
| Parallel district in description only | Add `Related_To` jurisdiction + per-charge district links, each with a precise description |
| Generic forfeiture stub, enumerated devices elsewhere | `targetedAsset` → each device; add `relatedCriminalCharges` |
| Devices linked to conduct but not forfeiture | Bridge forfeiture to same device nodes |
| `MultiDefendantIndictment` for single defendant | Acceptable when instrument type is unknown; still wire all charge edges |
| Empty `gufo:Relator` (enterprise cases) | Add registered `Related_To` participant links with a mediation description |
| Count 1 enterprise with no violation subgraph | Add overt-act nodes + venue + defendant subsets per violation |
| All defendants charged on all counts | Parse per-count defendant lists from indictment |
| Filing court only, no per-count venue | Add `Location` per count/violation + `Related_To` |
| Forfeiture stub, serial numbers in text only | One `ObservableObject` per enumerated device with serial in description |
| Wire fraud / identity theft counts isolated | `Related_To` from financial charges to underlying exploitation conduct |
| Charge→victim only via `Related_To` | Prefer conduct events with `uco-action:performer`/`object`; link charges to conduct |
| Device seizure implied but not modeled | Add `EquipmentSeizureAction` + `AssetForfeitureAction` with `targetedAsset` |

## Validation

```bash
validate_graph("federal-prosecution-relationships.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-production-case.md](cac-production-case.md) — production environments and produced media
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — press-release and sentencing patterns
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) — recruitment ring structure
- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md) — pre-indictment ICAC pattern
- [cac-sextortion-coercion.md](cac-sextortion-coercion.md) — sextortion conduct + federal charge stacking
- [cac-international-coordination.md](cac-international-coordination.md) — extradition and transnational defendants
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md) — superseding indictment, docket lifecycle, trial brief
- [forensic-lifecycle.md](forensic-lifecycle.md) — provenance and extraction actions
