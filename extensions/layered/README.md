# Layered Multi-Offense ESM Composition (`layered`)

One case graph, **multiple trajectories**, composed without flattening into
one S. Companion to [forced-labor](../forced-labor/),
[trafficking](../trafficking/), and [trajectories](../trajectories/).

Two composition patterns are demonstrated in separate exemplars with
different evidentiary standards:

| Pattern | Exemplar | What it shows |
|---|---|---|
| **Sequential / layered hand-off** | `layered.ttl` (Atkinson) | `Relationship(enables)` where one machine's terminal phase enables the next machine's start |
| **Concurrent / parallel** | `layered-legal-process.ttl` (illustrative) | Two independent tracks with **no** hand-off Relationship; phases share an intentional overlap window |

## Pattern A — Sequential / layered (Atkinson)

**United States v. Jonathan Michael Atkinson** (E.D. Wash.). Source:
[Spokesman-Review, 2025-04-13](https://www.spokesman.com/stories/2025/apr/13/tri-cities-business-owner-accused-of-grooming-sex-/)
(newspaper quoting AUSA Laurel Holland — thinner than a DOJ PR; confidence
calibrated down; unnamed counts among “11 charges” are not invented).

| ID | Trajectory | Alphabet | Terminal |
|---|---|---|---|
| T1 | CSEA / grooming (Honduras) → CSAM leverage | `lay:` grooming phases | `disrupted` |
| T2 | Cross-border transit → harboring | `lay:` transit/harbor | `disrupted` |
| T3 | Forced labor at Crossroad Services | `fl:` (forced-labor) | `disrupted` at `ForcedLabor` |
| T4 | Child sex trafficking (Pasco) | `lay:` child-sex-trafficking | `disrupted` |

**Hand-offs** (`uco-core:Relationship`):

- T1 `CSAMLeverage` **enables** T2 `CrossBorderTransit`
- T2 `Harboring` **enables** T3 `Control` and T4 `PlacementControl`
- T1 CSAM action **providesLeverageFor** T4 ICE/pastor-exposure threats

This is a **sequential/layered hand-off composition** (T1 → T2 → T3, T2 → T4).
It does **not** claim genuine temporal concurrency between T3 and T4: the
source places both in post-arrival Pasco (“worked for his company for unfair
wages and would be forced to engage in sexual acts”) without interval
precision. Shared `atk:interval-pasco` is an honest source-bounded limitation
(no precise US-arrival date), not a deliberate concurrency feature.

Spouse is anonymized as `atk:person-spouse` (personal name omitted). Alleged
post-arrest obstruction (hotel removal / witness-tampering investigation) is
kept as parallel `Action`s — **not** an offense ESM — attributed to the
anonymized spouse node.

## Pattern B — Concurrent / parallel (legal-process, illustrative)

`layered-legal-process.ttl` is **illustrative / fabricated** — not grounded
in a specific PACER filing. It is the right place to demonstrate concurrency
without overclaiming a real case.

| ID | Trajectory | Coupling |
|---|---|---|
| L1 | Warrant: Application → JudicialAuthorization → WarrantExecution | **enables** L2 Arrest (sequential hand-off) |
| L2 | Custody: Arrest → ChargingDecision → Arraignment | enabled by L1 |
| L3 | Surveillance: Authorization → ActiveMonitoring → MonitoringClosed | **none** — deliberately no `Relationship` to L1/L2 |

L1→L2 is the same sequential idiom as Atkinson. L3 runs in the **same
illustrative time window** (`lp:interval`) with **no** `enables` /
hand-off edge to L1 or L2. That absence is the demonstration of concurrency,
not an oversight: surveillance/monitoring proceeds in parallel with the
warrant-to-custody chain.

### Data-model note (temporal overlap)

The trajectories metamodel asserts occupancy via `traj:atInterval` →
`time:ProperInterval`. It does **not** define a first-class property to
assert that two `traj:PhaseAssertion`s (or trajectories) temporally overlap.
Concurrency in this exemplar is therefore expressed by (1) assigning phases
to the same intentional overlap interval and (2) omitting any hand-off
`Relationship` between the concurrent machines. OWL-Time relations such as
`time:intervalOverlaps` exist at the profile layer but are not wired into
`traj:` as a composition primitive.

## Files

| File | Role |
|---|---|
| `layered-vocab.ttl` | Grooming + transit + child-sex-trafficking phases/Techniques |
| `layered-shapes.ttl` | `instrument` required on layered Techniques |
| `layered.ttl` | Crime composition — Atkinson (sequential/layered hand-offs) |
| `layered-legal-process.ttl` | Non-crime composition — sequential (L1→L2) + concurrent (L3‖L1/L2) |
| `manifest.json` | `depends_on: trajectories, attack-technique, forced-labor` |

## Domain-agnostic?

**Yes, the composition pattern is.** `traj:` machines + optional
`Relationship(enables)` do not require exploitation vocabulary.
`layered.ttl` is one crime instantiation; `layered-legal-process.ttl` is a
procedural instantiation. You can layer as many process machines as the case
needs — investigation workflows, legalproc tracks, offense ESMs — as long as
each keeps its own S/A alphabet and hand-offs stay as Relationships (do not
flatten into one mega-S). Concurrent tracks simply omit the hand-off edge.

## Validation

```python
from case_uco.validation import validate_graph_file

for path in (
    "extensions/layered/layered.ttl",
    "extensions/layered/layered-legal-process.ttl",
):
    validate_graph_file(
        path,
        extensions=["layered"],
        profiles=["time", "prov-o"],
        strict_concepts=True,
        force_rdfs_inference=True,
    )
```
