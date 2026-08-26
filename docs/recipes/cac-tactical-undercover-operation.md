# Tactical Arrest and Undercover Operations

> See [Recipe Index](INDEX.md) for all recipes.

Model high-risk arrests, dynamic entry, undercover stings, threat assessments, and asset forfeiture in CAC investigations.

For **routine ICAC search warrant arrests** (custody without incident, no SWAT), use [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md) instead.

## Scope

**Layer 3 — Institutional workflow** for law-enforcement tactical execution.

## Key classes

| Class | Role |
|---|---|
| `ArrestOperation` / `HighRiskArrest` | Arrest event container |
| `DynamicEntry` | Entry tactic |
| `UndercoverOperation` | Undercover sting or persona operation |
| `SuspectProfile` / `ThreatAssessment` | Pre-operational intelligence |
| `AssetForfeitureAction` | Seizure with legal-process linkage |
| `InvestigativeAction` / `Authorization` | Warrants and operational authority |

## Canonical pattern (high-risk / undercover)

```
ThreatAssessment + SuspectProfile
  └── Related_To ──▶ HighRiskArrest (description: pre-operational assessment informs arrest)
        ├── DynamicEntry
        ├── UndercoverOperation (when applicable)
        └── AssetForfeitureAction (seized property)
```

## Routine warrant arrest (not this recipe)

When the source says **search warrant**, **taken into custody without incident**, and **no SWAT/dynamic entry**:

- Use [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
- Model `ArrestOperation` with `arrestType: warrant_arrest`
- Do **not** add `HighRiskArrest`, `DynamicEntry`, or `ThreatAssessment` unless the narrative supports them

## Modeling rules

- Keep **pre-op planning** (`ThreatAssessment`, `SuspectProfile`) separate from the entry action.
- Model seized property with `AssetForfeitureAction`, not plain `ObservableObject` alone.
- Undercover personas are **digital identities** (`ApplicationAccount` + `Identity`); physical props are `UcoObject`.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-tactical": "https://cacontology.projectvic.org/tactical#",
    "cacontology-undercover": "https://cacontology.projectvic.org/undercover#",
})
arrest = graph.add_node("kb:arrest-1", "cacontology-tactical:HighRiskArrest", {
    "uco-core:name": "Arrest of subject X",
})
graph.write("tactical-arrest.jsonld")
```

## Validation

```bash
validate_graph("tactical-arrest.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md)
- [forensic-lifecycle.md](forensic-lifecycle.md)
