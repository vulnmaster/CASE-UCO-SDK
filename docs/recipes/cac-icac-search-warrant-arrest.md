# ICAC Search Warrant Arrest (Press Release Pattern)

> See [Recipe Index](INDEX.md) for all recipes.

Model routine ICAC investigations that end in **search warrant execution**, **custody without incident**, and **booking** — the common Maryland / state police press-release pattern. This is distinct from [cac-tactical-undercover-operation.md](cac-tactical-undercover-operation.md) (SWAT, dynamic entry, undercover stings).

Based on validated patterns in `valdez-olivar-maryland-case-example.ttl` and `examples/maryland-icac-annapolis-arrest-2025.jsonld`.

## When to use this recipe

Use when the source describes:

- Maryland (or other state) **ICAC Task Force** + **Computer Crimes Unit** investigation
- **Search warrant** at a **residence**
- Suspect **taken into custody without incident**
- Transport to **county detention center**, **held without bond**
- **Online sexual solicitation** and/or **CSAM purchasing** allegations (pair with grooming + legal recipes)

Do **not** use `HighRiskArrest` or `DynamicEntry` when the narrative explicitly states no incident / peaceful custody.

## Scope

**Layer 3 — Institutional workflow** composed with:

- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md) — task force structure
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) — online solicitation (Layer 2)
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — charges (Layer 3)
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) — CSAM purchasing context (Layer 1)

## Key classes

| Class | Role |
|---|---|
| `MarylandICACtaskForce` / `ICACtaskForce` | State ICAC task force container |
| `MarylandStatePoliceComputerCrimesUnit` | Lead investigative unit |
| `GovernorsOfficeCrimePreventionFunding` | State grant funding |
| `StateLocalFundingCombination` | Combined state + federal DOJ funding |
| `Authorization` | Search warrant |
| `InvestigativeAction` | Investigation, warrant execution chain |
| `ArrestOperation` | Warrant arrest (`arrestType`: `warrant_arrest`) |
| `BookingAction` | Jail booking |
| `CorrectionalFacility` | Detention center |
| `OnlineGrooming` / `OnlinePurchase` | Behavioral / procurement context |
| `StateCharge` | Maryland charges (until `MarylandStateCharge` subclasses exist) |

## Canonical workflow

```
MarylandICACtaskForce
  └── cacontology-taskforce:partnersWith ──▶ MarylandStatePoliceComputerCrimesUnit + county PD

CACInvestigation
  ├── cacontology:hasStep ──▶ InvestigativeAction (CCU + ICAC co-performers)
  ├── Related_To ──▶ OnlineGrooming (description: investigation concerns grooming)
  ├── Related_To ──▶ OnlinePurchase (description: investigation concerns procurement)
  └── cacontology:hasPhase ──▶ InitialPhase → LegalProcessPhase → ConclusionPhase

InvestigativeAction (CCU investigation, April → December)
  └── uco-action:result ──▶ InvestigativeAction (search warrant execution)
        ├── case-investigation:relevantAuthorization ──▶ Authorization (warrant)
        ├── uco-action:performer ──▶ Child Exploitation Unit + county PD
        └── uco-action:result ──▶ ArrestOperation (warrant_arrest, resistanceExpected=false)
              └── uco-action:result ──▶ BookingAction
                    └── uco-action:location ──▶ CorrectionalFacility
```

## Modeling rules

- Use **`ArrestOperation`**, not `HighRiskArrest`, when custody was **without incident**.
- Set `arrestType` to `warrant_arrest`, `resistanceExpected` / `weaponsExpected` to `false`.
- Model **CCU performer** as one `MarylandStatePoliceComputerCrimesUnit` node with `uco-identity:Organization` + `uco-core:UcoObject` — do not duplicate a second CCU node for performer SHACL.
- Add **ICAC task force** and warrant-executing units (MSP Child Exploitation Unit, county PD) as **co-performers** when the narrative describes joint development or execution.
- Link **suspect → criminal acts**: `uco-action:performer` on `OnlineGrooming` and `OnlinePurchase` pointing to the suspect `Person`.
- Link **investigation scope → activities**: `cacontology:hasStep` to the main `InvestigativeAction`; add an **evidence-development** `InvestigativeAction` whose description references grooming/procurement IRIs and chains via `wasInformedBy` / `result`. Use registered `Related_To` only when both endpoints are `UcoObject` (SHACL), and state that the investigation concerns the activity in `uco-core:description`.
- **Populate phases**: use typed `cacontology:InitialPhase`, `LegalProcessPhase`, `ConclusionPhase` with `xsd:dateTimeStamp` on `hasPhaseBeginPoint` / `hasPhaseEndPoint`, `cacontology:occursDuringPhase` on actions, and `cacontology:transitionsTo` between phases.
- **One performer per InvestigativeAction** (CAC SHACL `maxCount 1`); document joint ICAC/county agency participation in action descriptions or `partnersWith`.
- Link **suspect residence** on suspect description and warrant `uco-action:location`.
- Link **charges → offenses** via charge `uco-core:description` IRI references to grooming/procurement nodes, plus `chargedWith` on the suspect.
- Put **charges** on the suspect via `cacontology-legal-outcomes:chargedWith` → `StateCharge` nodes.
- Attach the **press article PDF** as `ObservableObject` with `FileFacet`, `ContentDataFacet` (SHA-256), and `ExternalReference` (IRI node, not blank node).
- Keep `uco-action:object` on investigative actions to **UcoObject** / `Person` targets as appropriate; do not put grooming events in `Investigation.uco-core:object`.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-taskforce": "https://cacontology.projectvic.org/taskforce#",
    "cacontology-specialized": "https://cacontology.projectvic.org/specialized-units#",
    "cacontology-tactical": "https://cacontology.projectvic.org/tactical#",
    "cacontology-grooming": "https://cacontology.projectvic.org/grooming#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
})

inv = graph.add_node("kb:inv-1", [
    "case-investigation:Investigation", "cacontology:CACInvestigation",
], {"uco-core:name": "Maryland ICAC Annapolis Solicitation Case"})

arrest = graph.add_node("kb:arrest-1", [
    "case-investigation:InvestigativeAction",
    "cac-core:InvestigativeAction",
    "cacontology-tactical:ArrestOperation",
], {
    "cacontology-tactical:arrestType": "warrant_arrest",
    "cacontology-tactical:targetCount": {"@type": "xsd:nonNegativeInteger", "@value": "1"},
    "cacontology-tactical:resistanceExpected": {"@type": "xsd:boolean", "@value": "false"},
    "cacontology-tactical:weaponsExpected": {"@type": "xsd:boolean", "@value": "false"},
})

graph.write("icac-warrant-arrest.jsonld")
```

## Validation

SDK MCP default (recommended subset):

```bash
validate_graph("icac-warrant-arrest.jsonld", extensions=["cac"])
```

Or build script pattern:

```bash
python examples/build_maryland_icac_annapolis_arrest.py
```

Full CAC manifest (when upstream SHACL SPARQL is repaired):

```bash
make validate-extension EXT=cac DATA=icac-warrant-arrest.jsonld
```

## Related recipes

- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md)
- [cac-tactical-undercover-operation.md](cac-tactical-undercover-operation.md) — high-risk / undercover only
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md)
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md)
