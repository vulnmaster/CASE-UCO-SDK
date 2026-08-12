# Trajectories Extension (`trajectories`)

Vocabulary-agnostic **state-machine** and **per-case trajectory** metamodel
for CASE/UCO investigation graphs. Status: **`candidate`**.

## Phase 1 gaps this fills

| Gap | What existed | What `traj` adds |
|---|---|---|
| (1) Typed state | Domain-fixed CAC/AEO phase *classes* | `traj:State` instances (optionally `skos:Concept`) |
| (2) Transition + trigger/guard | CAC `PhaseTransitionEvent` (investigation-only); referral triggers | `traj:Transition` with `fromState` / `toState` / `trigger` / optional `guard` |
| (3) Ordered case occupancy + interval + evidence + confidence | Timestamps + `ConfidenceFacet` + PROV available but not bundled | `traj:Trajectory` of `traj:PhaseAssertion` (owl-time + `prov:wasDerivedFrom` + `ConfidenceFacet`) |
| (4) Learned transition probabilities | Scalar `transitionLikelihood` on one CAC class; no model artifact | `traj:StateMachineModel` + `traj:TransitionEstimate` with `prov:wasGeneratedBy` |

It does **not** re-model CAC grooming taxonomy, RICO enterprises, kill-chains, or drugs/weapons content — only the trajectory machinery.

## Contents

| File | Purpose |
|---|---|
| `trajectories.ttl` | OWL T-Box |
| `trajectories-shapes.ttl` | SHACL observed≠inferred firewall |
| `trajectories-profile-gufo.ttl` | Optional gUFO bridge (`State rdf:type gufo:Phase` metaclass; `PhaseAssertion`⊆`gufo:Situation`) |
| `trajectories-exemplar.ttl` | CAC grooming trajectory + model |
| `trajectories-elder-fraud-exemplar.ttl` | Synthetic non-CAC elder-fraud trajectory (fictional Victim V) |
| `trajectories-invalid-exemplar.ttl` | Expected-invalid firewall fixture |

## Design choices

### Ordering idiom

`traj:sequenceIndex` (xsd:nonNegativeInteger) on each `PhaseAssertion`,
referenced from `Trajectory` via `hasPhaseAssertion`.

- Preferred over `rdf:List` (awkward in SHACL/SPARQL).
- Preferred over AEO `ArrayOfAction` (planned narrative actions, not
  observed occupancy).
- Complementary to CAC `EventSequence` (investigation events), not a
  replacement.

### Confidence

Reuse **`uco-core:ConfidenceFacet`** on the assertion via
`uco-core:hasFacet` — no `traj:confidence` mint. SHACL requires ≥1
`ConfidenceFacet` on every `PhaseAssertion`.

### Terminal polarity (v0.2.0)

`traj:isTerminal` (xsd:boolean) marks the PhaseAssertion that is the final
observed occupancy in a Trajectory; `traj:terminalPolarity` (xsd:string,
SHACL `sh:in ("completed" "disrupted")`) types its realized outcome —
`completed` (the modeled chain reached its endpoint; later arrest/prosecution
does **not** flip this) vs. `disrupted` (an intervention ended the trajectory
**mid-chain**, before the modeled endpoint). SHACL requires
`isTerminal true => terminalPolarity present`; `terminalPolarity` alone never
requires a second, opposite-polarity branch to exist — single-path
trajectories that assert only one polarity are conformant.

Deliberately a property pair, not `traj:State` subclasses
(`SuccessTerminal`/`DisruptedTerminal`), so a third outcome type is a
vocabulary-list edit, not a T-Box change.

### Enacted actions and the affordance/φ seam (v0.3.0)

`traj:enactsAction` (domain `traj:Transition`; **no** `rdfs:range`; SHACL
`sh:class uco-action:Action`) names the concrete typed action(s) that
**constitute** a transition — distinct from `traj:trigger`, which may be any
`uco-core:UcoObject` the transition merely reacts to. The OWL range is
intentionally omitted: under RDFS entailment an `rdfs:range` would infer the
required type onto whatever the property pointed at, making the `sh:class`
check vacuous. Type enforcement is therefore SHACL-only. The same range-less
+ `sh:class` pattern applies to `traj:hasPhaseAssertion`, `traj:learnedFrom`,
and `traj:hasTransitionEstimate`. It is additive (no `sh:minCount`): a
Transition with only a bare-`UcoObject` `traj:trigger` and no
`traj:enactsAction` remains fully conformant.

### Multi-valued `enactsAction` (v0.3.1)

**Multiple** `enactsAction` values are allowed when one directed edge is gated
by co-occurring techniques (affordance-labeled multi-action edges in an ESM).
SHACL `sh:maxCount` on `traj:enactsAction` was removed in **v0.3.1** so those
edges validate; this extension's version is **0.3.1** (`manifest.json`).

### enactsAction convention: arriving state, not leaving state

A Transition has two endpoints, and a domain extension's action catalog
will often contain one action that characterizes the `fromState` and a
different one that characterizes the `toState`. **The rule: `enactsAction`
names the action that *produces* the `toState`, so it is wired to the
transition *arriving at* the phase that action characterizes** — not the
transition leaving the phase the action is associated with. Domain
extensions built on this metamodel should follow this one convention; do
not mix leaving-state and arriving-state wiring within or across domains.

Two corollaries fall out of applying this rule consistently, rather than
being ad-hoc exceptions:

- **A transition with no cataloged producing action simply omits
  `enactsAction`.** `sh:minCount` is not set, so this is conformant, not
  a gap to be papered over by attaching a loosely-related action from an
  adjacent phase.
- **If several co-occurring techniques produce the same `toState`**, wire
  **all** of them as `traj:enactsAction` on that arriving edge (multi-valued).
  For example, an arriving edge into a conditioning phase might carry three
  co-occurring techniques (spoofed opener + fixed script + secrecy demand),
  and an arriving edge into a laundering phase might carry two
  (false-identity acquisition + deposit).
- **s₀ techniques that also gate the first transition** are wired on that
  first arriving edge (they produce the second state), not left unwired.
  Exogenous pre-s₀ feeders (e.g. victim-list purchase) stay outside S as
  `prov:Activity` / evidence, not as `traj:enactsAction` on a phantom
  incoming edge to s₀.

The affordance (φ) an offense abuses at a transition is **not** a bespoke
`traj:` property. It is carried on the standard **`action:instrument`**
property of the `traj:enactsAction` instance — e.g.
`:action-1 a uco-action:Action ; uco-action:instrument :the-abused-affordance .`
No `traj:affordance` mint; reuse the UCO action facet as-is.

Action **categories** (the "kind of action" a transition enacts, e.g. a
spoofing technique or a structuring technique) are minted the same way
MITRE ATT&CK techniques are in `extensions/attack-technique`: an
`owl:Class` that is also an instance of the `uco-action:Technique`
metaclass, `rdfs:subClassOf uco-action:Action`, carrying
`uco-action:techniqueID`. See
[`extensions/attack-technique/README.md`](../attack-technique/README.md)
for the punning pattern — domain extensions that need their own action
catalog should reuse that pattern rather than inventing a parallel one.

`traj:initialState` (domain `traj:StateMachineModel`, `rdfs:range traj:State`,
`sh:maxCount 1`) marks the model's s₀ at the machine level — a model with
no single natural start state simply omits it. Unlike `enactsAction` /
`hasPhaseAssertion` / `learnedFrom` / `hasTransitionEstimate`, the state
endpoint properties (`fromState`, `toState`, `assertsState`, `initialState`)
**keep** their `rdfs:range traj:State`: phase-vocabulary individuals often
live in a domain extension's ontology graph, and `case_validate` does not
merge `--ontology-graph` type assertions into the data graph, so removing
those ranges would fail every valid exemplar. See the comment block above
those properties in `trajectories.ttl`.

### Firewall (observed vs inferred)

- `PhaseAssertion` **owl:disjointWith** `StateMachineModel` /
  `TransitionEstimate`.
- Every `PhaseAssertion`: ≥1 `prov:wasDerivedFrom`, confidence facet,
  state, interval, sequence index.
- Every model / estimate: ≥1 `prov:wasGeneratedBy`.
- Trajectories reference **PhaseAssertions only**; models
  `traj:learnedFrom` trajectories (never the reverse).

### Mapping CAC `PhaseTransitionEvent` → `traj:Transition`

| CAC temporal | `traj` |
|---|---|
| `PhaseTransitionEvent` | `traj:Transition` (more general; not limited to investigation lifecycle) |
| `transitionsFrom` / `transitionsTo` | `fromState` / `toState` |
| begin/end timestamps on the event | Prefer intervals on **PhaseAssertions**; put trigger-time on the trigger Action if needed |
| Fixed investigation phases | Plug-in `traj:State` vocab (SKOS), not hard subclassing |

Keep using CAC temporal classes for **investigation** lifecycle; use `traj`
for **offense / engagement / fraud** occupancy histories and analytic models.

## Plug-in vocabulary pattern

Domain phases are **instances**, not T-Box dependencies:

```turtle
:InitialContact a traj:State , skos:Concept ;
    skos:inScheme :CACGroomingPhaseScheme ;
    skos:exactMatch <https://cacontology.projectvic.org/grooming#InitialContactPhase> .
```

No dependence on unmerged CAC PRs (#33 AffordanceMisuse, #39 ConditioningPhase).

### AEO CyberKillChain plug-in (do not modify AEO)

Wrap kill-chain phase actions the same way:

```turtle
:Reconnaissance a traj:State , skos:Concept ;
    skos:inScheme :AEOCyberKillChainScheme ;
    skos:exactMatch <https://ontology.adversaryengagement.org/ae/attack/…> ;
    uco-core:description "Corresponds to a CyberKillChain phase Action." .
```

`aeo:CyberKillChain` / `Storyline` remain for **planned** adversary-engagement
narratives; `traj:Trajectory` records **observed** occupancy.

## Validation

**Primary (SDK):** `from case_uco.validation import validate_graph_file`
(public API since v1.22.1) with `extensions=['trajectories']`,
`profiles=['time','prov-o']`, `strict_concepts=True`,
`force_rdfs_inference=True`. That bundle loads upper shapes
`sh-time.ttl` / `sh-prov-o.ttl`. Add `'gufo'` to `profiles` to load
`trajectories-profile-gufo.ttl` + `sh-gufo.ttl`.

**Secondary (CLI):** `case_validate` with traj OWL/shapes plus upper
*ontology* TTL (`time.ttl` / `prov-o.ttl`), `--inference rdfs`, and
`--allow-info` does **not** load upper *shapes* or run concept coverage —
do not treat CLI-alone SHACL green as SDK green. See `VALIDATION.md` for
exact commands and results.

**`make validate-extension` caveat:** the shared
`scripts/validate_extension.py` currently invokes `case_validate` without
`--allow-info` or `--inference rdfs`. On this extension that produces a
**false failure** for `trajectories-exemplar.ttl` (Info-level UUID IRI
suggestions flip `Conforms` to False). Until the script is updated in a
separate PR, use the SDK primary path or the secondary CLI command in
`VALIDATION.md` — do not treat `make validate-extension` as authoritative
for trajectories.

Invalid exemplar must fail (observed≠inferred firewall).

## Status

Local candidate extension (`"status": "candidate"`, version **0.3.1**).
`example.org` namespace matches rico/drugs/weapons placeholders pending a
community IRI. Language bindings (`packages/case-uco-trajectories`) are
deferred.
