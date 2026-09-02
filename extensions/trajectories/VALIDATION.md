# Trajectories extension — validation log

Date: 2026-09-02 (re-validated this PR; SDK / CLI / critic tables below
retain the 2026-08-11 recorded runs where not superseded).
Branch: `feat/trajectories-only`
Status: **`candidate`** (`manifest.json` `status` key; schema enum
`candidate` / `operational` / `deprecated`).
`uco_compat`: `["1.4.0", "1.5.0"]`.

True green paths below. Upper shapes (`sh-time`, `sh-prov-o`, optional `sh-gufo`) load via the SDK profile bundle when `profiles` is set — not via ad-hoc TTL alone.

This package is a standalone domain-agnostic metamodel. Validation exercises only the exemplars shipped under `extensions/trajectories/`. `trajectories-exemplar.ttl` currently uses neither `traj:enactsAction` nor `traj:initialState` (0 / 0). `trajectories-elder-fraud-exemplar.ttl` is a **synthetic** (fictional) non-CAC trajectory that exercises both once each (1 / 1): `initialState` on Contact (s₀), and `enactsAction` on the urgency→extraction transition pointing at a fictional courier cash-envelope `uco-action:Action`.

---

## Primary: SDK `case_uco.validation` (strict coverage)

Public API since v1.22.1 (`python/case_uco/validation/`). The
`mcp_server/graph_validator` module remains a thin re-export for MCP/critic
compatibility, but extension docs should import the package.

```bash
export PATH="$PWD/.venv/bin:$PATH"
export PYTHONPATH="$PWD/python${PYTHONPATH:+:$PYTHONPATH}"
python3 <<'PY'
from case_uco.validation import validate_graph_file

def check(path, extensions, profiles=("time", "prov-o")):
    r = validate_graph_file(
        path,
        extensions=extensions,
        profiles=list(profiles),
        strict_concepts=True,
        force_rdfs_inference=True,
    )
    stages = dict(r.stage_status)
    print(path.split("/")[-1], "conforms=", r.conforms,
          "coverage=", stages.get("coverage_conformance"),
          "shacl=", stages.get("shacl_conformance"),
          "viol=", r.violation_count)

for p in (
    "extensions/trajectories/trajectories-exemplar.ttl",
    "extensions/trajectories/trajectories-elder-fraud-exemplar.ttl",
):
    check(p, ["trajectories"])
    check(p, ["trajectories"], profiles=("time", "prov-o", "gufo"))

check("extensions/trajectories/trajectories-invalid-exemplar.ttl", ["trajectories"])
PY
```

### Recorded results (SDK path; 2026-08-11 on branch `feat/trajectories-only`)

| Artifact | profiles | Conforms | coverage | SHACL | `enactsAction`/`initialState` uses |
|---|---|---|---|---|---|
| `trajectories-exemplar.ttl` | time, prov-o | **True** | ok | conforms | 0 / 0 — does not exercise v0.3.0 |
| `trajectories-exemplar.ttl` | time, prov-o, gufo | **True** | ok | conforms | 0 / 0 |
| `trajectories-elder-fraud-exemplar.ttl` | time, prov-o | **True** | ok | conforms | 1 / 1 |
| `trajectories-elder-fraud-exemplar.ttl` | time, prov-o, gufo | **True** | ok | conforms | 1 / 1 |
| `trajectories-invalid-exemplar.ttl` | time, prov-o | **False** | ok | nonconformant | 0 / 0 — 10 violations (firewall/missing-prop fixture) |

Invalid exemplar expected messages include:

- `Every PhaseAssertion MUST cite >=1 evidence node via prov:wasDerivedFrom.`
- Missing `assertsState` / `atInterval` / `sequenceIndex` on dual-typed model
- Missing `uco-core:ConfidenceFacet` via `hasFacet`
- `traj:StateMachineModel is an INFERRED analytic artifact.`

Without `profiles=['time','prov-o']`, coverage fails closed on `profile_not_selected` for `time:*` / `prov:*` even if SHACL alone would pass.

---

## Critic: deterministic pass (offline)

```bash
export PATH="$PWD/.venv/bin:$PATH"
python3 <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "mcp_server")
from critic.models import CriticArtifactRequest
from critic.deterministic import analyze_artifact

for label, path, exts in [
    ("cac", "extensions/trajectories/trajectories-exemplar.ttl", ["trajectories"]),
    ("elder-base", "extensions/trajectories/trajectories-elder-fraud-exemplar.ttl", ["trajectories"]),
]:
    req = CriticArtifactRequest(
        graph_path=str(Path(path).resolve()),
        critic_scope="graph",
        extensions=exts,
        profiles=["time", "prov-o"],
        force_rdfs_inference=True,
    )
    review = analyze_artifact(req)
    print(label, "status=", review.status,
          "findings=", len(review.deterministic_findings or []))
PY
```

### Recorded results

| Exemplar | status | deterministic findings |
|---|---|---|
| CAC grooming (base) | `deterministic_clean` | `[]` |
| Elder-fraud (base, non-CAC; self-contained under `extensions/trajectories/`) | `deterministic_clean` | `[]` |

---

## Secondary: `case_validate` CLI (caveat)

```bash
.venv/bin/case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/trajectories/trajectories.ttl \
  --ontology-graph extensions/trajectories/trajectories-shapes.ttl \
  --ontology-graph ontology/upper/time.ttl \
  --ontology-graph ontology/upper/prov-o.ttl \
  --inference rdfs --allow-info \
  extensions/trajectories/<exemplar>.ttl
```

### Recorded results (2026-08-11)

| Artifact | Conforms |
|---|---|
| `trajectories-exemplar.ttl` | **True** |
| `trajectories-elder-fraud-exemplar.ttl` | **True** |
| `trajectories-invalid-exemplar.ttl` | **False** |

**What this loads**

| Layer | Loaded? |
|---|---|
| traj OWL + SHACL | Yes (`--ontology-graph`) |
| UCO/CASE shapes | Yes (`--built-version case-1.4.0` — see version note below) |
| `ontology/upper/shapes/sh-time.ttl`, `sh-prov-o.ttl` | **No** |
| Strict concept coverage / profile selection | **No** |

Use the SDK primary path above for PR-grade "green." CLI alone can report SHACL conformant while the SDK still fails coverage.

**`uco_compat` vs this CLI `--built-version`:** the recorded CLI command used
`case-1.4.0`. `manifest.json` `uco_compat` is `["1.4.0", "1.5.0"]` (neither
`Assertion` nor `AnalyticResult` is 1.5-only). This log does **not** invent
a 1.5.0 CLI re-run.

### `make validate-extension` — standard gate (2026-09-02)

`make validate-extension EXT=trajectories DATA=…` wraps
`scripts/validate_extension.py`, which invokes `case_validate` with the
manifest's OWL/SHACL/bridge files and no extra flags. Both shipped
exemplars use `urn:uuid:…` instance IRIs. Recorded this PR:

| DATA | Script result | Notes |
|---|---|---|
| `trajectories-exemplar.ttl` | `Conforms: True` | No Info-level UUID-IRI findings; no exception needed. |
| `trajectories-elder-fraud-exemplar.ttl` | `Conforms: True` | Same. |
| `trajectories-invalid-exemplar.ttl` | `Conforms: False` (expected) | Real Violation results from the firewall fixture. |

---

## Mutations (a–e) — firewall + non-vacuous `sh:class`

Mutations written under `/tmp`, validated with the same CLI base as the
secondary section above (`--inference rdfs --allow-info`). (a)–(d) mutate
the base CAC exemplar; (e) mutates the elder-fraud exemplar (the only
shipped graph that uses `traj:enactsAction`). All must fail.

| Mutation | Change | Result |
|---|---|---|
| (a) | Drop `prov:wasDerivedFrom` on first `PhaseAssertion` | Conforms **False** — missing evidence provenance |
| (b) | Drop `uco-core:hasFacet` ConfidenceFacet link | Conforms **False** — missing ConfidenceFacet |
| (c) | Dual-type `StateMachineModel` as also `PhaseAssertion` | Conforms **False** — firewall / missing required props |
| (d) | `Trajectory hasPhaseAssertion` → a `TransitionEstimate` | Conforms **False** — `sh:class` on hasPhaseAssertion |
| (e) | Elder `urgency→extraction` `traj:enactsAction` retargeted from the courier `uco-action:Action` to `SYNTHETIC Victim V` (`uco-identity:Person`) | Conforms **False** — `sh:class uco-action:Action` on enactsAction |

Mutation (e) is the non-vacuity proof for the range-less `enactsAction`
design: with `rdfs:range uco-action:Action` restored under RDFS
entailment, the same Person-valued triple reports `Conforms: True`
(range infers the Action type onto the Person). Removing the range is
what lets `sh:class` reject it. The same vacuity/range policy applies to
`hasPhaseAssertion`, `learnedFrom`, and `hasTransitionEstimate` (see
`trajectories.ttl` object-property header comment).

---

## Focus-node non-vacuity (shipped exemplars, 2026-09-02)

| Shape target | CAC (base) | Elder (base, non-CAC) | Invalid |
|---|---|---|---|
| PhaseAssertion | 4 | 4 | 2 |
| Trajectory | 1 | 1 | 1 |
| Transition | 3 | 3 | 1 |
| StateMachineModel | 1 | 1 | 1 |
| TransitionEstimate | 3 | 3 | 1 |

All nonzero on the valid exemplars.

`traj:enactsAction` / `traj:initialState` triple counts (direct count, not
shape-target count):

| Artifact | `enactsAction` uses | `initialState` uses |
|---|---|---|
| `trajectories-exemplar.ttl` (base) | 0 | 0 |
| `trajectories-elder-fraud-exemplar.ttl` (base) | 1 | 1 |
| `trajectories-invalid-exemplar.ttl` | 0 | 0 |

---

## Regression: existing SDK test suite

```bash
export PATH="$PWD/.venv/bin:$PATH"
export PYTHONPATH="$PWD/python:$PWD/mcp_server${PYTHONPATH:+:$PYTHONPATH}"
.venv/bin/python -m pytest -q \
  mcp_server/tests/test_extension_paths.py \
  python/tests/test_extension_bundle_contract.py \
  python/tests/test_validation_api.py \
  python/tests/test_darkwatchman_release.py \
  python/tests/test_attack_catalog_coverage.py
```

Result (2026-08-11): **16 passed**, 0 failed.

---

## Invalid fixtures (pyshacl, `inference=rdfs`, 2026-09-02)

Kitchen-sink `trajectories-invalid-exemplar.ttl` is recorded in the SDK /
CLI sections above. The five single-rule fixtures were run with `pyshacl`
(`inference=rdfs`, ont graph = `trajectories.ttl`, shapes =
`trajectories-shapes.ttl`). All **Conforms: False** for the stated reason:

| Fixture | Rule under test | Why it failed |
|---|---|---|
| `trajectories-invalid-exemplar.ttl` | Observed≠inferred firewall + missing required observed-layer props | Dual-typed model/assertion plus missing `wasDerivedFrom`, `ConfidenceFacet`, `assertsState`, `atInterval`, `sequenceIndex` (kitchen sink; 10 violations on the 2026-08-11 SDK run) |
| `trajectories-invalid-probability.ttl` | `traj:transitionProbability` in `[0, 1]` | `sh:maxInclusive` — value `1.5` |
| `trajectories-invalid-interval.ttl` | `traj:atInterval` must be `time:ProperInterval` | `sh:class` — value is a `uco-identity:Person` |
| `trajectories-invalid-sequence-index.ttl` | Unique `sequenceIndex` per Trajectory | SPARQL uniqueness — two assertions share index `0` |
| `trajectories-invalid-terminal.ttl` | At most one `isTerminal true` per Trajectory | SPARQL “at most one terminal” (also fires “terminal must have max `sequenceIndex`” because the index-0 terminal is not max) |
| `trajectories-invalid-estimate-membership.ttl` | Estimate `ofTransition` ∈ model's `hasTransition` (when any `hasTransition` is declared) | Membership SPARQL — estimate points at an undeclared transition |

---

## Competency SPARQL queries

Declared in `manifest.json` `competency_queries` and run against both valid
exemplars as raw A-Box (no inference). `expect: "empty"` means zero SELECT
rows (the promotion gate mishandles ASK; the firewall query is a SELECT).

| Query | Proves | CAC | Elder |
|---|---|---|---|
| `queries/observed-occupancy-chain.sparql` | Trajectory → PhaseAssertion → state + interval + `prov:wasDerivedFrom` | nonempty (4 rows) | nonempty (4 rows) |
| `queries/inference-provenance.sparql` | `StateMachineModel` + `AnalyticResult` `learnedFrom` a Trajectory, `wasGeneratedBy` an `Analysis` whose `instrument` is a `Tool` | nonempty (4 rows) | nonempty (4 rows) |
| `queries/observed-inferred-firewall.sparql` | No PhaseAssertion also typed `AnalyticResult`; no `StateMachineModel` missing `AnalyticResult`; no dual-typed model/assertion | empty (0 rows) | empty (0 rows) |

---

## Deferred

- Language bindings under `packages/case-uco-trajectories/`
- Exemplars that exercise `traj:enactsAction` / `traj:initialState` more richly than the single wired uses in `trajectories-elder-fraud-exemplar.ttl` (CAC base exemplar still has 0 / 0)
