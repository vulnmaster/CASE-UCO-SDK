# Trajectories extension — validation log

Date: 2026-08-11
Branch: `feat/trajectories-only` (working tree, uncommitted)
Status: `candidate`

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

### Recorded results (re-verified 2026-08-11 on branch `feat/trajectories-only`)

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
| `trajectories-exemplar.ttl` | **True** (info-level UUID IRI suggestions only) |
| `trajectories-elder-fraud-exemplar.ttl` | **True** |
| `trajectories-invalid-exemplar.ttl` | **False** |

**What this loads**

| Layer | Loaded? |
|---|---|
| traj OWL + SHACL | Yes (`--ontology-graph`) |
| UCO/CASE shapes | Yes (`--built-version case-1.4.0`) |
| `ontology/upper/shapes/sh-time.ttl`, `sh-prov-o.ttl` | **No** |
| Strict concept coverage / profile selection | **No** |

Use the SDK primary path above for PR-grade "green." CLI alone can report SHACL conformant while the SDK still fails coverage.

### `make validate-extension` — known false failure (do not "fix" by editing TTL)

`make validate-extension EXT=trajectories DATA=…` wraps
`scripts/validate_extension.py`, which currently invokes `case_validate`
with only `--ontology-graph` flags for the manifest's OWL/SHACL/bridge
files — **no** `--built-version`, **no** `--inference rdfs`, **no**
`--allow-info`. Observed on this branch (2026-08-11):

| DATA | Script result | Notes |
|---|---|---|
| `trajectories-exemplar.ttl` | **False failure** (`Conforms: False`, exit ≠ 0) | Only `sh:Info` UUID-IRI suggestions on `http://example.org/kb/…` focus nodes; no Violation. Adding `--allow-info` alone flips this to `Conforms: True`. |
| `trajectories-elder-fraud-exemplar.ttl` | `Conforms: True` | All instance IRIs are `urn:uuid:…`, so the Info constraint does not fire. |
| `trajectories-invalid-exemplar.ttl` | `Conforms: False` (expected) | Real Violation results from the firewall fixture. |

Until `scripts/validate_extension.py` is updated in a **separate** PR
(out of scope for this trajectories package), treat the SDK primary path
or the secondary CLI block above as the authoritative green path. Do not
weaken exemplars or shapes to silence the Info results.

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

## Focus-node non-vacuity (shipped exemplars, 2026-08-11)

| Shape target | CAC (base) | Elder (base, non-CAC) | Invalid |
|---|---|---|---|
| PhaseAssertion | 4 | 4 | 2 |
| Trajectory | 1 | 1 | 1 |
| Transition | 3 | 3 | 1 |
| StateMachineModel | 1 | 1 | 1 |
| TransitionEstimate | 3 | 2 | 1 |

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

## Deferred

- Language bindings under `packages/case-uco-trajectories/`
- Competency SPARQL queries (optional promote gate)
- Exemplars that exercise `traj:enactsAction` / `traj:initialState` more richly than the single wired uses in `trajectories-elder-fraud-exemplar.ttl` (CAC base exemplar still has 0 / 0)
