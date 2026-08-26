# Multi-Jurisdictional Task Force Operations

> See [Recipe Index](INDEX.md) for all recipes.

Model ICAC task forces, joint investigations, jurisdictional handoffs, and mass rescue operations using CAC Ontology coordination classes.

## Scope

**Layer 3 — Institutional workflow** for multi-agency child exploitation enforcement.

## Key classes

| Class | Role |
|---|---|
| `CACInvestigation` | Case container |
| `TaskForce` | Participating agencies and structural relationships |
| `JointInvestigation` | Shared investigative posture across agencies |
| `LocalJurisdiction` / `StateJurisdiction` / `FederalJurisdiction` / `InternationalJurisdiction` | Jurisdiction nodes |
| `JurisdictionalHandoff` / `MutualAidRequest` | Lead transfer and aid requests |
| `MassChildRescueOperation` / `VictimExtraction` | Operational rescue events |
| `InvestigativeAction` / `ProvenanceRecord` | Per-action audit trail |

## Canonical pattern

```
TaskForce
  ├── Related_To ──▶ JointInvestigation (description: task force participates in investigation)
  └── Related_To ──▶ FederalJurisdiction + StateJurisdiction + LocalJurisdiction (description: participating jurisdictions)

MassChildRescueOperation
  ├── JurisdictionalHandoff (state → federal lead)
  └── VictimExtraction (one per victim, each with ProvenanceRecord)
```

## Modeling rules

- Do not model a task force as a generic `Identity` — use `TaskForce`.
- Use **one node per agency** (`MarylandStatePoliceComputerCrimesUnit` + `Organization` + `UcoObject`) for performer links; avoid duplicate CCU nodes.
- Add the **ICAC task force** as co-performer on investigative actions when detectives from both CCU and task force developed evidence.
- Task force **funding** nodes attach via `uco-core:object` per validated Maryland exemplars (`valdez-olivar-maryland-case-example.ttl`); prefer `cacontology-taskforce:fundingSource` when the ontology property is available in your build.
- Record **jurisdictional transitions** as `JurisdictionalHandoff`, not description strings.
- Pair **mass rescue** with **per-victim** `VictimExtraction` nodes for provenance.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-taskforce": "https://cacontology.projectvic.org/taskforce#",
    "cacontology-multi-jurisdiction": "https://cacontology.projectvic.org/multi-jurisdiction#",
})
tf = graph.add_node("kb:tf-1", "cacontology-taskforce:TaskForce", {
    "uco-core:name": "Regional ICAC Task Force",
})
graph.write("task-force-op.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=task-force-op.jsonld
```

## Related recipes

- [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md)
- [cac-tactical-undercover-operation.md](cac-tactical-undercover-operation.md)
- [cac-international-coordination.md](cac-international-coordination.md)
