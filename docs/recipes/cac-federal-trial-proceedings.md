# Federal Trial Proceedings and Docket Lifecycle

> See [Recipe Index](INDEX.md) for all recipes.

Model **federal criminal case progression** from initial indictment through superseding charges, competency and detention proceedings, discovery motions, trial briefs, and anticipated trial evidence — using CASE/UCO institutional types and CAC legal workflow classes.

Pair with [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) for charge wiring and [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) for multi-device exhibit provenance.

## When to use this recipe

Use when the source includes:

- **PACER docket sheets** with hearing dates, motions, and Speedy Trial Act exclusions
- **Superseding indictments** that replace or expand original counts
- **Government trial briefs** describing anticipated facts, witnesses, and exhibit plans
- **Competency proceedings** (18 U.S.C. § 4241)
- **Detention hearings** and counsel changes
- **Motions in limine** and CSAM presentation stipulations

## Scope

**Layer 3 — Federal legal workflow** extending prosecution relationship completeness with **procedural timeline** and **trial preparation** artifacts.

## Key classes

| Class | Role |
|---|---|
| `FederalProsecution` / `PreTrialPhase` / `TrialPhase` | Legal process phases |
| `MultiDefendantIndictment` | Original and superseding charging instruments |
| `FederalCharge` | Numbered counts (linked per federal prosecution recipe) |
| `cac-core:LegalEvent` / `uco-core:Event` | Competency workflow when no dedicated class exists; describe the § 4241 proceeding |
| `cacontology-legal-outcomes:LegalProceeding` / `cacontology-tactical:BookingAction` | Detention proceeding and custody action |
| `InvestigativeAction` | Motions, orders, trial brief filing as auditable actions |
| `ProvenanceRecord` | Source PDF/docket entry → graph extraction |
| `ObservableObject` + `FileFacet` | Trial brief PDF, docket export, exhibit devices |

## Canonical pattern

```
uco-core:Bundle
  ├── CACInvestigation
  │     └── Related_To ──▶ FederalProsecution
  │
  ├── FederalProsecution
  │     ├── cacontology-usa-federal-law:hasLegalPhase ──▶ PreTrialPhase
  │     │     ├── Related_To ──▶ SupersedingIndictment (description: supersedes original)
  │     │     ├── Related_To ──▶ LegalEvent (competency proceeding)
  │     │     └── Related_To ──▶ LegalProceeding (detention order)
  │     └── cacontology-usa-federal-law:hasLegalPhase ──▶ TrialPhase
  │           └── Related_To ──▶ TrialBrief (ObservableObject)
  │
  ├── OriginalIndictment (MultiDefendantIndictment)
  │     └── Related_To ──▶ SupersedingIndictment (description: supersedes original)
  │
  ├── SupersedingIndictment
  │     └── Related_To ──▶ each FederalCharge
  │
  └── InvestigativeAction (TrialBriefFiling)
        ├── uco-action:object ──▶ TrialBrief PDF
        └── uco-action:result ──▶ anticipated exhibit list (in description or linked IRIs)
```

## Superseding indictment chain

When a case moves from an original indictment to a superseding instrument:

1. Model **both** instruments as separate `MultiDefendantIndictment` nodes with filing dates and ECF/document numbers in `uco-core:description`.
2. Link original → superseding with a directional `uco-core:Relationship` using registered kind `Related_To`; state "supersedes original indictment" in `uco-core:description`.
3. Wire **active charges** only to the superseding indictment; retain original counts as historical nodes only if the docket shows they were dismissed or replaced — otherwise omit duplicate charge nodes.
4. Update `FederalProsecution` → charging instrument edge to point at the **current** superseding indictment.
5. Record count delta in investigation focus or prosecution description (e.g., "2 counts → 12 counts superseding 2024-07-25").

```text
CHARGING_INSTRUMENTS:
  Original: Doc 1 — filed 2023-08-24 — counts 1-2 (2251, 2252 possession)
  Superseding: Doc 70 — filed 2024-07-25 — counts 1-12 (2251, 1591, 2422, 2252)
```

## Docket procedural events

Extract auditable events from PACER docket text:

| Docket signal | Graph pattern |
|---|---|
| Arraignment / plea continuance | `InvestigativeAction` or phase transition with `uco-action:startTime` |
| Competency hearing / § 4241 order | Event node linked to `Person` defendant + `PreTrialPhase` |
| Speedy Trial Act exclusion | `uco-core:description` on prosecution with date range; optional `Relationship` to exclusion order |
| Motion to compel / dismiss | `InvestigativeAction` with performer = filing party |
| Detention granted | Link to defendant `Person`; document no-bond conditions |
| Trial date set / continued | `TrialPhase` temporal bounds; link trial brief filing date |
| Counsel change / terminated | Update `Person` role description or use the declared `cacontology-legal-outcomes:DefenseAttorneyRole` when applicable |

Do not flatten the entire docket into one Bundle description — create **queryable event nodes** for milestones agents will ask about (competency resolved, superseding filed, trial scheduled).

## Trial brief and anticipated evidence

Government trial briefs (e.g., Doc 188) describe **what will be introduced at trial** before it happens:

1. Type the brief as `ObservableObject` with `FileFacet` (fileName, document number).
2. Add `InvestigativeAction` for the filing with `uco-action:object` → brief PDF.
3. For each **minor victim section**, link anticipated testimony and exhibits to:
   - `MinorTraffickingVictimRole` or aggregate victim role
   - `FederalCharge` nodes for that victim's counts
   - `CommercialSexualExploitation` / `CSAMIncident` conduct nodes
4. For **CSAM presentation plans**, link brief statements to exhibit devices (`1B10`, `1B1`, etc.) and note multi-device duplication in `uco-core:description` per [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md).
5. Mark anticipated facts as `ALLEGED` until verdict nodes exist.

```
TrialBrief (Doc 188)
  └── Related_To ──▶ MinorVictim-2 testimony
        ├── Related_To ──▶ FederalCharge (Counts 3, 4, 5)
        ├── Related_To ──▶ Grindr messages (ObservableObject)
        └── Related_To ──▶ rideshare records (ObservableObject)
```

## Relationship checklist

| # | Edge | When | Pattern |
|---|---|---|---|
| T1 | Original → superseding indictment | Superseding filed | Directional `Related_To` between instruments with supersession stated in description |
| T2 | Active prosecution → current instrument | Always | `FederalProsecution` `Related_To` latest superseding indictment |
| T3 | Trial brief → charges | Trial brief sourced | Brief section `Related_To` each `FederalCharge` it discusses |
| T4 | Trial brief → victims | Per-victim sections | Brief `Related_To` victim role nodes |
| T5 | Competency → defendant | § 4241 docket entries | Competency event linked to defendant `Person` |
| T6 | Docket milestone dates | PACER export | Temporal literals on phase and action nodes |
| T7 | Anticipated exhibits → devices | Brief lists ECF/stems | Exhibit ID → `ObservableObject` with `FileFacet` |
| T8 | Provenance | PDF/docket sourced | `ProvenanceRecord` on source documents |

## Fact-file template

```text
CASE_ID: 1:23-cr-00071-JMS
COURT: U.S. District Court, District of Hawaii
DEFENDANT: Riley, Darren Patrick

CHARGING_INSTRUMENTS:
  Original: Doc 1 — 2023-08-24 — counts 1-2
  Superseding: Doc 70 — 2024-07-25 — counts 1-12

KEY_DOCKET_EVENTS:
  2023-08-28: arraignment continuance (defendant transport refusal)
  2023-10-19: competency hearing
  2024-06-21: competency resolved; arraignment on superseding
  2024-07-25: superseding indictment filed
  2026-02-20: government trial brief (Doc 188)

TRIAL:
  scheduled: 2026 (per brief)
  brief_anticipates: MV1-MV5 testimony/exhibits per count group
```

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
})

original = graph.add_node("kb:indictment-original", "cacontology:MultiDefendantIndictment", {
    "uco-core:name": "Original indictment — Doc 1",
    "uco-core:description": "Filed 2023-08-24; 2 counts.",
})

superseding = graph.add_node("kb:indictment-superseding", "cacontology:MultiDefendantIndictment", {
    "uco-core:name": "Superseding indictment — Doc 70",
    "uco-core:description": "Filed 2024-07-25; 12 counts.",
    "cacontology:indictmentCounts": {"@type": "xsd:nonNegativeInteger", "@value": "12"},
})

prosecution = graph.add_node("kb:prosecution-1", "cacontology-usa-federal-law:FederalProsecution", {
    "uco-core:name": "Federal prosecution — 1:23-cr-00071-JMS",
})

graph.add_node("kb:rel-supersede", "uco-core:Relationship", {
    "uco-core:source": {"@id": "kb:indictment-original"},
    "uco-core:target": {"@id": "kb:indictment-superseding"},
    "uco-core:kindOfRelationship": "Related_To",
    "uco-core:description": "The target supersedes the source indictment.",
    "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
})

graph.add_node("kb:rel-prosecution-current", "uco-core:Relationship", {
    "uco-core:source": {"@id": "kb:prosecution-1"},
    "uco-core:target": {"@id": "kb:indictment-superseding"},
    "uco-core:kindOfRelationship": "Related_To",
    "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
})

graph.write("federal-trial-proceedings.jsonld")
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Only superseding indictment, no supersession edge | Link original → superseding; record filing dates |
| Trial brief facts only in Bundle description | Per-victim sections → victim roles + charge links |
| Docket as unstructured text blob | Milestone `InvestigativeAction` / Event nodes with dates |
| Competency proceedings omitted | Model as `cac-core:LegalEvent` with `uco-action:startTime`; link to prosecution phase |
| Exhibit devices named in brief but not in graph | `ObservableObject` per device stem (`1B10`, etc.) |
| Prosecution phase without temporal bounds | Add `cacontology-usa-federal-law:hasPhaseBeginPoint` on `FederalProsecution` / `PreTrialPhase` |
| Source documents without assertion metadata | Add `case-investigation:ProvenanceRecord` on indictment and trial brief nodes |

## Validation

```bash
validate_graph("federal-trial-proceedings.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md) — MCP agent workflow for PACER PDF bundles
- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — charge and defendant wiring
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) — § 1591 conduct structure
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) — multi-device CSAM exhibits
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — post-trial disposition
- [forensic-lifecycle.md](forensic-lifecycle.md) — provenance chain
