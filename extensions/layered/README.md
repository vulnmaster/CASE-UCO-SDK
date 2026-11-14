# Layered Exploitation State Machine Composition (`layered`)

Status: **`candidate`** · version **0.2.0**

Domain-agnostic **composition metamodel** for Exploitation State Machines
(ESMs) over [`trajectories`](../trajectories/). A case-level
`lay:ExploitationStateMachine` aggregates:

| Class | Role |
|---|---|
| `lay:Layer` | One machine slot — binds exactly one `traj:Trajectory` (+ optional per-layer `traj:StateMachineModel`) |
| `lay:Coupling` | First-class inter-layer edge (`enables`, `temporallyOverlaps`, …) |
| Factors via `lay:hasFactor` | Shared actors, instruments, locations, evidence |

**Does not flatten** multiple domain alphabets into one mega-S. Domain phase /
technique catalogs plug in (`trafficking`, `elder-fraud`, `extortion`,
`legalproc`, or `layered-vocab.ttl` for the CSEA/transit/CST alphabet used
by the Atkinson exemplar). This port depends on `trajectories` only. It
does not OWL-import `means` or `expense`.

Two optional properties on `ExploitationStateMachine`, both ranged only to
`uco-core:UcoObject`:

| Property | When to use |
|---|---|
| `lay:hasGoal` | Stable goal. Should be a `means:Goal` when `means` is loaded. Not parked only on `hasFactor`. |
| `lay:hasExpenseAssessment` | Benefit-at-expense assessment. Should be an `expense:ExploitationAssessment` when `expense` is loaded. Omit otherwise. |

## What this fills

| Need | Before | After |
|---|---|---|
| Multi-trajectory case ESM | Ad-hoc Relationships + comments | `ExploitationStateMachine` + `Layer` |
| Sequential hand-off | `kindOfRelationship "enables"` only | `Coupling` + optional `realizedBy` |
| Concurrent / parallel | Shared interval + missing edge | `temporallyOverlaps` + `concurrencyGroup` |
| Full vs partial | Narrative only | `completeness` / `coverage` |
| Shared factors | Scattered nodes | `hasFactor` register |

## Composition patterns (`lay:compositionPattern`)

| Value | Meaning |
|---|---|
| `sequential` | Layers ordered by `enables` / `feeds` hand-offs |
| `concurrent` | Temporal overlap via `temporallyOverlaps` (no enables between those tracks) |
| `parallel` | Same `concurrencyGroup`, independent (overlap assertion optional) |
| `hybrid` | Mix (typical: sequential chain + concurrent sidecar) |

## Coverage / completeness

- **`lay:coverage`** on a Layer — this trajectory runs the full modeled alphabet
  (`full`) or stops mid-alphabet (`partial`), e.g. forced labor without
  `WageAppropriation`.
- **`lay:completeness`** on the ESM — all known threads modeled (`full`) or a
  sourced subset (`partial`). Actions deliberately outside the offense ESM
  (e.g. post-arrest obstruction) keep completeness `partial`.

## Coupling kinds (`lay:couplingKind`)

`enables` · `providesLeverageFor` · `produces` · `sharesFactor` ·
`temporallyOverlaps` · `feeds`

`temporallyOverlaps` **requires** `lay:couplingInterval` (SHACL).

## Files

| File | Role |
|---|---|
| `layered.ttl` | Composition T-Box (`ExploitationStateMachine`, `Layer`, `Coupling`) |
| `layered-vocab.ttl` | CSEA / transit / child-sex-trafficking domain alphabet |
| `layered-shapes.ttl` | Composition + Technique-instrument SHACL |
| `layered-exemplar.ttl` | Atkinson — sequential multi-offense ESM (4 Layers) |
| `layered-legal-process.ttl` | Hybrid legal-process ESM (sequential + concurrent) |
| `layered-invalid-exemplar.ttl` | Expected-invalid composition fixture |

## Exemplars

### A — Sequential multi-offense (Atkinson)

`layered-exemplar.ttl` — U.S. v. Jonathan Michael Atkinson (E.D. Wash.).
Source: [Spokesman-Review, 2025-04-13](https://www.spokesman.com/stories/2025/apr/13/tri-cities-business-owner-accused-of-grooming-sex/).

| Layer | Trajectory | Alphabet | Coverage |
|---|---|---|---|
| T1 | CSEA / grooming → CSAM leverage | `lay:` grooming | `full` |
| T2 | Transit → harboring | `lay:` transit/harbor | `full` |
| T3 | Forced labor | `fl:` | `partial` |
| T4 | Child sex trafficking | `lay:` CST | `full` |

`compositionPattern sequential` · `completeness partial` · subject Atkinson ·
factors include CSAM / four-plex / Crossroad instruments + evidence nodes.

### B — Hybrid sequential + concurrent (illustrative)

`layered-legal-process.ttl` — fabricated warrant → custody chain with a
concurrent surveillance Layer. `temporallyOverlaps` Couplings + shared
`concurrencyGroup "hearing-window"`. Proves domain-agnostic composition
(no offense vocabulary).

## Validation

```python
from case_uco.validation import validate_graph_file

for path in (
    "extensions/layered/layered-exemplar.ttl",
    "extensions/layered/layered-legal-process.ttl",
):
    validate_graph_file(
        path,
        extensions=["layered"],
        profiles=["time", "prov-o"],
        strict_concepts=True,
        force_rdfs_inference=True,
    )

# Must NOT conform:
validate_graph_file(
    "extensions/layered/layered-invalid-exemplar.ttl",
    extensions=["layered"],
    profiles=["time", "prov-o"],
    strict_concepts=True,
    force_rdfs_inference=True,
)
```

`depends_on` is `trajectories` and `forced-labor`. The Atkinson exemplar's
T3 layer occupies the `fl:` alphabet that
[`forced-labor`](../forced-labor/) declares; selecting `layered` loads it.
Validate the legal-process exemplar without `expense` on the command line. Use `case-utils` 0.18.0 and
`--built-version case-1.5.0`.

## Design rules

1. **One Layer ↔ one Trajectory.** Never merge States across domains.
2. **Coupling is authoritative** for ESM composition; `realizedBy` Relationship
   is optional interop.
3. **Concurrency is explicit** (`temporallyOverlaps` + interval), not implied
   by missing edges alone.
4. **Domain vocab is optional** — process machines use local `traj:State`
   individuals; offense machines plug in domain schemes via `domainAlphabet`.

- Recipe: [`docs/recipes/candidates/layered-esm-composition.md`](../../docs/recipes/candidates/layered-esm-composition.md)
