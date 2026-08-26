# Child Sex Trafficking and Recruitment Networks

> See [Recipe Index](INDEX.md) for all recipes.

Model child sex trafficking enterprises, **solo-operator federal § 1591 prosecutions**, recruitment networks, and digital-to-physical escalation using [CAC Ontology](https://cacontology.projectvic.org/) classes on top of core CASE/UCO investigation containers. For institutional task-force response, see [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md). For victim extraction after identification, see [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md). For indictment charge wiring and superseding instruments, see [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) and [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md).

## Scope

**Layer 2 — Behavioral / enterprise structure** plus supporting **Layer 1 evidence** (locations, accounts, transport artifacts) and **Layer 3 — Federal prosecution** when § 1591 counts appear in indictments.

## Key classes

| Class | Role |
|---|---|
| `CACInvestigation` | Investigation container (multi-typed on `case-investigation:Investigation`) |
| `TraffickingEnterprise` / `TraffickingRing` / `TraffickingCell` | Structural anchor for multi-trafficker networks |
| `CommercialSexualExploitation` | In-person commercial sex acts (solo or ring) |
| `SexTraffickingOfMinors` | Federal conduct type aligned with 18 U.S.C. § 1591 |
| `MinorTraffickingVictimRole` | Per-victim role when indictment names Minor Victim 1–N |
| `VictimTransportation` | Rideshare/taxi/hotel transport to exploitation locations |
| `DigitalToPhysicalBridge` | Online contact → in-person meet transition |
| `PeerRecruitmentNetwork` / `ClassmateRecruitmentNetwork` | School-based recruitment structures |
| `TransportationOfferApproach` | Rides, hotels, money as commercial inducements |
| `FederalCharge` | § 1591, § 2422, § 2251 stacked counts per victim |
| `Location` | Hotels, apartments, vehicles, beaches |
| `ApplicationAccount` / platform nodes | Grindr, Snapchat, text messaging |

## Canonical pattern

```
CACInvestigation
  └── Related_To ──▶ TraffickingRing (or TraffickingCell)
        ├── Related_To ──▶ Identity (description: trafficker/member)
        ├── Related_To ──▶ MinorTraffickingVictimRole (description: victim targeted by ring)
        └── Related_To ──▶ PeerRecruitmentNetwork (description: recruitment network used)

SchoolBasedRecruitment
  └── Related_To ──▶ TransportationOfferApproach (description: documented approach)
        └── Related_To ──▶ DigitalToPhysicalBridge (description: IG DM to motel meet)
```

## Solo-operator federal child sex trafficking (§ 1591)

Many federal **child sex trafficking** cases involve a **single defendant** recruiting multiple minor victims through dating/social apps — not a multi-trafficker ring. Do **not** force a `TraffickingRing` when the source describes one operator and enumerated minor victims.

```
Person (defendant / Primary Trafficker Role)
  ├── cacontology-legal-outcomes:chargedWith ──▶ FederalCharge (Count 4 — § 1591) … per victim
  └── cacontology:participatesInEvent ──▶ CommercialSexualExploitation (per victim)

CommercialSexualExploitation (MV2)
  ├── uco-action:object ──▶ MinorTraffickingVictimRole (MV2)
  └── Related_To ◀── FederalCharge 3, 4, 5 (description: charge-to-conduct bridge)

DigitalToPhysicalBridge (Grindr → in-person)
  ├── uco-action:instrument ──▶ Grindr platform
  └── cac-core:precedes ──▶ CommercialSexualExploitation at Location (hotel/apartment)

VictimTransportation
  ├── cacontology-sex-trafficking:transportationMethod: Uber / Lyft / taxi
  └── cacontology-sex-trafficking:destinationLocation ──▶ hotel or defendant residence
```

Modeling rules:

1. Create one **`MinorTraffickingVictimRole`** (or anonymized victim node) per **Minor Victim N** in the indictment or trial brief.
2. Link each victim to **their specific counts** via `Related_To` from `FederalCharge` — counts often stack production (§ 2251), trafficking (§ 1591), enticement (§ 2422), and distribution/receipt (§ 2252) for the **same victim**.
3. Model **commercial inducements** (money offers, phones, hotel payment) on `CommercialSexualExploitation` or `TransportationOfferApproach` — these support the commercial sex act element of § 1591.
4. Model **Grindr → text → in-person** as `DigitalToPhysicalBridge` linked to [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) message evidence when available.
5. Model **rideshare/taxi transport** as `VictimTransportation` with origin/destination `Location` nodes when the trial brief or indictment describes arranged transport.
6. Document **substance facilitation** (drugs provided during encounters) in conduct `uco-core:description` when alleged — link to the same exploitation event.
7. For **multiple victims across years**, use separate exploitation nodes with temporal bounds rather than one aggregate CSAM incident.
8. Model **alleged criminal conduct as explicit events** (`CommercialSexualExploitation`, `RecordingAction`, `GroomingSolicitation`, `VictimTransportation`) with `uco-action:performer`, `uco-action:object`, `uco-action:instrument`, and `uco-action:location` — not only descriptive nodes linked by generic `Related_To`.
9. Type the solo operator as **`PrimaryTraffickerRole`** on the subject role and link **`controlsVictim`** to each `MinorTraffickingVictimRole` when indictment structure supports it.
10. Create **parallel incident nodes for every minor victim** in the indictment, even when public documents provide less detail for some victims — this keeps per-victim SPARQL uniform.
11. Add lightweight **`case-investigation:ProvenanceRecord`** nodes on source instruments (indictment, trial brief) when facts are **ALLEGED** from public docket documents.

### Model conduct as explicit events (preferred over descriptive stubs)

CASE/UCO/CAC favor queryable **events and actions** over summary nodes. For each victim with counts in the indictment:

```
PrimaryTraffickerRole (subject)
  ├── cacontology-sex-trafficking:controlsVictim ──▶ MinorTraffickingVictimRole (MV2)
  └── cacontology:participatesInEvent ──▶ CommercialSexualExploitation (MV2)

CommercialSexualExploitation (MV2)
  ├── uco-action:performer ──▶ subject role
  ├── uco-action:object ──▶ MV2 victim role
  ├── uco-action:location ──▶ Location (Waikiki apartment)
  └── uco-action:startTime ──▶ 2019-08-01 (when known)

RecordingAction / CSAMIncident (MV2 production)
  ├── uco-action:performer / object / instrument / location (same encounter)
  └── uco-core:hasFacet ──▶ FileFacet (artifact)

GroomingSolicitation (enticement counts)
  ├── uco-action:performer / object
  └── cacontology:participatesInEvent ──▶ subject + victim (SHACL min 2)

FederalCharge (Count 4)
  └── Related_To ──▶ CommercialSexualExploitation   # charge→conduct bridge
```

Use **`uco-action:object`** (not `uco-action:target`) for victim roles on UCO `Action`/`Crime` events. Put **`uco-action:startTime`** directly on the event node; reserve `uco-core:hasFacet` for artifact facets such as `FileFacet`.

On **`GroomingSolicitation`**, also populate **`cacontology:participatesInEvent`** with subject + victim — CAC SHACL requires at least two participants on that class. Keep **`uco-action:performer`** / **`object`** as the primary action semantics; `participatesInEvent` satisfies shape validation.

### MV2 encounter chain (precedes / part_of)

When public documents describe online contact → transport → in-person exploitation → recording, chain events explicitly:

```
DigitalToPhysicalBridge (Grindr)
  ├── uco-action:instrument ──▶ OnlineDatingPlatform
  ├── cac-core:precedes ──▶ VictimTransportation
  └── cac-core:precedes ──▶ CommercialSexualExploitation (encounter)

VictimTransportation
  └── cac-core:precedes ──▶ CommercialSexualExploitation

RecordingAction / CSAMIncident
  └── Related_To ──▶ CommercialSexualExploitation (description: same encounter)
```

Link **Count 12 (possession)** to the seized device **and** to production/receipt incidents whose material the indictment alleges was found on that device.

Reference exemplar: [`examples/hawaii-riley-trafficking-2023-example.jsonld`](../../examples/hawaii-riley-trafficking-2023-example.jsonld).

### Per-victim charge bundle matrix

Indictments often assign **different count groups per minor victim**:

```text
VICTIM_COUNTS:
  MV1: 1,2,12        # production x2 + aggregate possession
  MV2: 3,4,5          # production + trafficking + distribution
  MV3: 6,7,8          # trafficking + enticement + receipt
  MV4: 9,10           # trafficking + enticement
  MV5: 11             # trafficking only
```

Each row drives:
- `Related_To` from each `FederalCharge` → conduct event (`CSAMIncident`, `CommercialSexualExploitation`, `GroomingSolicitation`)
- `uco-action:performer` / `uco-action:object` on each conduct event (replaces charge→victim `Related_To` for query paths)
- `cacontology-sex-trafficking:controlsVictim` from `PrimaryTraffickerRole` → each victim role
- Trial brief sections → same victim IRIs for anticipated testimony

### Stacked statutes per encounter

When one encounter supports multiple counts (production video + trafficking + distribution to same victim):

```
CommercialSexualExploitation (MV2 — Aug 2019, Waikiki apartment)
  ├── uco-action:performer ──▶ subject role
  ├── uco-action:object ──▶ MV2
  ├── Related_To ◀── FederalCharge Count 4 (§ 1591)
  ├── Related_To ◀── FederalCharge Count 3 (§ 2251 production via linked CSAMIncident)
  └── Related_To ◀── FederalCharge Count 5 (§ 2252 distribution via same CSAMIncident)
```

## Modeling rules (network cases)

- Use **specific approach subclasses** (`TransportationOfferApproach`, not generic `InvestigativeAction`) so analysts can query pretext patterns.
- Split **online recruitment** and **in-person meet** into separate events linked by `DigitalToPhysicalBridge`.
- Model the ring as `TraffickingEnterprise`, not a single `Identity`.
- Physical items (condoms, hotel keys) → `uco-core:UcoObject`; digital artifacts (DMs, ads) → `uco-observable:ObservableObject`.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-sex-trafficking": "https://cacontology.projectvic.org/trafficking#",
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
})

victim2 = graph.add_node("kb:mv2", "cacontology-sex-trafficking:MinorTraffickingVictimRole", {
    "uco-core:name": "Minor Victim 2",
})

exploitation = graph.add_node("kb:cse-mv2", "cacontology-sex-trafficking:CommercialSexualExploitation", {
    "uco-core:name": "Alleged commercial sexual exploitation — MV2",
    "uco-action:performer": {"@id": "kb:subject-riley"},
    "uco-action:object": {"@id": "kb:mv2"},
})

subject = graph.add_node("kb:subject-riley", [
    "case-investigation:Subject",
    "cacontology-sex-trafficking:PrimaryTraffickerRole",
], {
    "uco-core:name": "Defendant-1 — principal subject",
    "cacontology-sex-trafficking:controlsVictim": [{"@id": "kb:mv2"}],
})

charge_trafficking = graph.add_node("kb:charge-4", "cacontology-legal-outcomes:FederalCharge", {
    "uco-core:name": "Count 4 — Sex trafficking a minor (18 U.S.C. 1591)",
    "cacontology-legal-outcomes:chargeCount": {"@type": "xsd:nonNegativeInteger", "@value": "4"},
})

defendant = graph.add_node("kb:defendant-1", "uco-identity:Person", {
    "uco-core:name": "Defendant-1",
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-4"}],
})

for rel_id, src, tgt in [
    ("rel-charge-conduct", "kb:charge-4", "kb:cse-mv2"),
]:
    graph.add_node(f"kb:{rel_id}", "uco-core:Relationship", {
        "uco-core:source": {"@id": src},
        "uco-core:target": {"@id": tgt},
        "uco-core:kindOfRelationship": "Related_To",
        "uco-core:description": "Charge concerns the target alleged exploitation conduct.",
        "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
    })

graph.write("trafficking-solo-operator.jsonld")
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Conduct only in victim `uco-core:description` | Add per-victim `CommercialSexualExploitation` / `CSAMIncident` event nodes |
| MV2 rich subgraph, other victims description-only | Parallel lightweight incident nodes for every minor victim |
| Generic `Related_To` charge→victim only | Add `uco-action:performer`/`object` on conduct; use `controlsVictim` on trafficker role |
| `uco-action:target` on UCO actions | Use canonical `uco-action:object` for victim roles |
| `ActionReferences` inside `uco-core:hasFacet` | Put `uco-action:startTime` on the event; keep facets for artifacts |
| Grooming enticement without participants | Add `cacontology:participatesInEvent` (subject + victim) on `GroomingSolicitation` |
| Grindr as generic `ObservableObject` only | Type as `OnlineDatingPlatform`; set `uco-action:instrument` on bridge event |
| Alleged PACER facts without source pointer | Add `ProvenanceRecord` on indictment / trial brief / seizure nodes |
| MV2 bridge/transport disconnected from encounter | Chain with `precedes`; link production `part_of` exploitation |
| Possession count linked to device only | Also link Count 12 to production/receipt CSAM incidents on the device |
| Trial brief linked to one victim only | Link Doc 188 to prosecution and each anticipated victim (MV1–MV5) |

## Validation

```bash
make validate-extension EXT=cac DATA=trafficking-ring.jsonld
```

Or via MCP: `validate_graph("trafficking-ring.jsonld", extensions=["cac"])`.

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — defendant→counts, forfeiture, indictment bridges
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md) — superseding indictment, docket, trial brief
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) — Grindr/messaging evidence layer
- [cac-production-case.md](cac-production-case.md) — production counts stacked with trafficking
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) — multi-device CSAM exhibits
- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md) — joint enforcement response
- [cross-domain-extensions.md](cross-domain-extensions.md) — extension setup
