# Layered ESM Composition

> Candidate recipe (see [candidates/README.md](README.md)); not in the [Recipe Index](../INDEX.md) until the extension is promoted. Extension docs: [`extensions/layered/`](../../../extensions/layered/).
> Related: [offense-means-set.md](offense-means-set.md), [expense-benefit-at-expense.md](expense-benefit-at-expense.md), [cross-ontology-composition.md](../cross-ontology-composition.md) (principle 6: compose offense-conduct extensions only on evidence), [cac-trafficking-recruitment-network.md](../cac-trafficking-recruitment-network.md), [elder-fraud-impersonation.md](../elder-fraud-impersonation.md).

Compose **multiple** `traj:Trajectory` machines into one case-level
`lay:ExploitationStateMachine` — sequential hand-offs, concurrent/parallel
tracks, shared factors — **without** flattening domain alphabets into one
mega-S.

## When to use

| Pattern | Example | How |
|---|---|---|
| Sequential hand-off | Trafficking → forced labor; grooming → transit → exploitation | `Coupling` `couplingKind "enables"` between Layers |
| Concurrent offenses | Trafficking **and** CSAM production overlapping in time | Two Layers + `temporallyOverlaps` + shared `concurrencyGroup` |
| Parallel process thread | Legal actions + parallel investigation/surveillance | Same hybrid pattern (`layered-legal-process.ttl`) |
| Partial machine | Forced labor without wage appropriation | Layer `coverage "partial"` |
| Shared instruments/actors | CSAM reused as leverage; shared housing | `hasFactor` + optional `sharesFactor` / `providesLeverageFor` |

## Stack (do not skip layers)

1. **`trajectories`** — occupancy (`Trajectory` / `PhaseAssertion`) + per-machine models  
2. **Domain alphabet** — phase vocabulary for that layer (`trafficking`, `elder-fraud`, `extortion`, `legalproc`, or `layered-vocab`)  
3. **`layered`** — compose those machines into one ESM  

`layered` depends on `trajectories` and on `forced-labor` (the `fl:` alphabet its Atkinson exemplar occupies). It does not import `means` or `expense`. `lay:hasGoal` and `lay:hasExpenseAssessment` are optional and ranged to `uco-core:UcoObject`. A legal-process machine omits `hasExpenseAssessment`.  

## Minimal shape

```turtle
:esm a lay:ExploitationStateMachine ;
    lay:compositionPattern "hybrid" ;   # or sequential | concurrent | parallel
    lay:completeness "partial" ;        # or full
    lay:concernsSubject :offender ;
    lay:hasLayer :layer-a , :layer-b ;
    lay:hasCoupling :coupling-enables ;
    lay:hasFactor :instrument-csam , :location-safehouse .

:layer-a a lay:Layer ;
    lay:occupiesTrajectory :traj-a ;
    lay:hasMachineModel :model-a ;      # optional
    lay:domainAlphabet :PhaseSchemeA ;  # optional
    lay:layerIndex 1 ;
    lay:coverage "full" .

:coupling-enables a lay:Coupling ;
    lay:couplingKind "enables" ;
    lay:fromLayer :layer-a ;
    lay:toLayer :layer-b ;
    lay:fromEndpoint :phase-a-terminal ;
    lay:toEndpoint :phase-b-start ;
    lay:realizedBy :rel-enables .       # optional UCO Relationship twin
```

Concurrent tracks use `lay:couplingKind "temporallyOverlaps"` and **must**
set `lay:couplingInterval` (SHACL).

## Validated exemplars

| File | What it proves |
|---|---|
| [`layered-exemplar.ttl`](../../../extensions/layered/layered-exemplar.ttl) | Atkinson: 4 sequential offense Layers + Couplings + factor register |
| [`layered-legal-process.ttl`](../../../extensions/layered/layered-legal-process.ttl) | Domain-agnostic hybrid: sequential warrant→custody **and** concurrent surveillance |

```python
from case_uco.validation import validate_graph_file

validate_graph_file(
    "extensions/layered/layered-exemplar.ttl",
    extensions=["layered"],
    profiles=["time", "prov-o"],
    strict_concepts=True,
    force_rdfs_inference=True,
)
```

CLI: pass extension OWL/shapes via `--ontology-graph` and use `--inference rdfs --allow-info` (UUID `sh:Info` hints are not violations).

## Anti-patterns

- Flattening T1∪T2∪T3 States into one `StateMachineModel.initialState`  
- Implying concurrency only by “no enables edge” — assert `temporallyOverlaps`  
- Minting Composition classes inside a domain alphabet extension — use `layered`  
- Treating post-arrest obstruction as an offense Layer unless it is modeled as its own machine  
