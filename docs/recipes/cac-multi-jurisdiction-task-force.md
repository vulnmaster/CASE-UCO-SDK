# Multi-Jurisdictional Task Force Operations

> See [Recipe Index](INDEX.md) for all recipes.

Model multi-agency task forces, joint investigations, jurisdictional handoffs, and mass rescue operations using CAC Ontology coordination classes.

## Scope

**Layer 3 — Institutional workflow** for multi-agency child exploitation enforcement.

## Key classes

| Class | Role |
|---|---|
| `CACInvestigation` | Case container |
| `cacontology-multi-jurisdiction:TaskForce` | Generic multi-agency task force and structural relationships |
| `cacontology-taskforce:ICACtaskForce` | One of the OJJDP-funded Internet Crimes Against Children (ICAC) task forces, when identified by the source |
| `JointInvestigation` | Shared investigative posture across agencies |
| `LocalJurisdiction` / `StateJurisdiction` / `FederalJurisdiction` / `InternationalJurisdiction` | Jurisdiction nodes |
| `JurisdictionalHandoff` / `MutualAidRequest` | Lead transfer and aid requests |
| `MassChildRescueOperation` / `VictimExtraction` | Operational rescue events |
| `InvestigativeAction` / `ProvenanceRecord` | Per-action audit trail |

## Canonical pattern

```
cacontology-multi-jurisdiction:TaskForce
  ├── Related_To ──▶ JointInvestigation (description: task force participates in investigation)
  └── Related_To ──▶ FederalJurisdiction + StateJurisdiction + LocalJurisdiction (description: participating jurisdictions)

MassChildRescueOperation
  ├── JurisdictionalHandoff (state → federal lead)
  └── VictimExtraction (one per victim, each with ProvenanceRecord)
```

## Modeling rules

- Use `cacontology-multi-jurisdiction:TaskForce` for a generic task force. Use `cacontology-taskforce:ICACtaskForce` only when the source identifies one of the OJJDP-funded Internet Crimes Against Children task forces.
- In CAC 3.1.0, `cacontology-taskforce:ICACtaskForce` is under `uco-observable:ObservableObject` and `cac-core:OrganizationLikeEntity`; it is not a subclass of `cacontology-multi-jurisdiction:TaskForce`, which is under `uco-identity:Organization`. Do not infer one type from the other.
- Use **one node per agency** (`MarylandStatePoliceComputerCrimesUnit` + `Organization` + `UcoObject`) for performer links; avoid duplicate CCU nodes.
- Add the **ICAC task force** as co-performer on investigative actions when detectives from both CCU and task force developed evidence.
- Task force **funding** nodes attach via `uco-core:object` per validated Maryland exemplars (`valdez-olivar-maryland-case-example.ttl`).
- Record **jurisdictional transitions** as `JurisdictionalHandoff`, not description strings.
- Pair **mass rescue** with **per-victim** `VictimExtraction` nodes for provenance.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-multi-jurisdiction": "https://cacontology.projectvic.org/multi-jurisdiction#",
})
tf = graph.upsert_node("kb:example-task-force", types=["cacontology-multi-jurisdiction:TaskForce"], properties={
    "uco-core:name": "Synthetic Regional Task Force",
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
