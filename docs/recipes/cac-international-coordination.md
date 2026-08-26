# International Coordination and Cross-Border Operations

> See [Recipe Index](INDEX.md) for all recipes.

Model transnational child exploitation investigations, Europol/Interpol coordination, extradition, and cross-border evidence sharing using CAC international module classes.

## Scope

**Layer 3 — Institutional workflow** extending multi-jurisdiction patterns to international boundaries.

## Key classes

| Class | Role |
|---|---|
| `cacontology-multi-jurisdiction:InternationalJurisdiction` | Foreign jurisdiction node |
| `cacontology-international:CrossBorderOperation` | Coordinated international operation |
| `cacontology-multi-jurisdiction:ExtraditionRequest` | Formal extradition request |
| `cacontology-international:InternationalEvidenceSharing` | Cross-border evidence transfer |
| `cacontology-international:InternationalCoordination` / `EuropolCoordination` | General or Europol-specific coordination events |
| `cacontology-taskforce:TaskForce` / `cacontology-multi-jurisdiction:JointInvestigation` | Domestic coordination structures |

## Canonical pattern

```
cacontology-multi-jurisdiction:JointInvestigation
  ├── cacontology-multi-jurisdiction:primaryJurisdiction ──▶ FederalJurisdiction
  ├── Related_To ──▶ InternationalJurisdiction (foreign partner)
  └── Related_To ──▶ cacontology-international:CrossBorderOperation
        ├── Related_To ──▶ InternationalCoordination / EuropolCoordination
        └── Related_To ──▶ InternationalEvidenceSharing
```

## Modeling rules

- Use `InternationalJurisdiction` for foreign partners — do not overload domestic jurisdiction classes.
- Model **evidence sharing** as its own auditable action with `ProvenanceRecord`.
- Chain domestic task-force structure from [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-international": "https://cacontology.projectvic.org/international#",
})
op = graph.add_node("kb:op-1", "cacontology-international:CrossBorderOperation", {
    "uco-core:name": "Europol coordinated takedown",
})
graph.write("international-op.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=international-op.jsonld
```

## Related recipes

- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md)
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md)
