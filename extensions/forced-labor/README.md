# Forced-Labor Exploitation State Machine Extension (`forced-labor`)

Narrow, machine-only extension: contributes **only** what the
[trajectories](../trajectories/) Exploitation State Machine (ESM) needs to
run on a forced-labor / debt-bondage offense (18 U.S.C. § 1589 pattern) —
a victim-journey phase vocabulary and a small action catalog. No class
hierarchy beyond the `uco-action:Technique` metaclass pattern from
[attack-technique](../attack-technique/).

**CAC crosswalk policy** (shared with `layered`): no CAC class is retyped
and CAC is never `owl:imported`. `skos:exactMatch` is not used. Optional
`skos:closeMatch` may document conceptual proximity when defensible — none
are asserted here (CAC is grooming/CSAM / commercial-sex shaped; these
cases are adult forced-labor with no child-exploitation allegation).

## Cases

Two press-release-only sources (no affidavit/plea text vendored), both
carried in one exemplar sharing the machine:

| Case | Court | Source | Terminal |
|---|---|---|---|
| **Gladys Ibanez-Olea** | N.D. Ill. | [USAO-NDIL PR 2026-07-24](https://www.justice.gov/usao-ndil/pr/cartel-member-who-trafficked-victims-mexico-chicagoland-forced-labor-sentenced-more-9) | `completed` at `WageAppropriation` |
| **Thuy Tien Luong** | W.D.N.C. | [DOJ OPA PR 2021-01-08](https://www.justice.gov/opa/pr/north-carolina-nail-salon-owner-convicted-forced-labor) | `disrupted` at `ForcedLabor` (victim report + arrest June 2018) |

## Phases (`fl:PhaseScheme`)

| State | What it is |
|---|---|
| `fl:Recruitment` | Victim brought into the scheme (Mexico recruit / employment onset) |
| `fl:Control` | Harboring/captivity/workplace domination via force, threats, fraud, coercion (incl. fabricated debt) |
| `fl:ForcedLabor` | Compelled work |
| `fl:WageAppropriation` | Offender takes wages / enforces debt bondage (modeled completed endpoint) |

## Actions (`uco-action:Technique` classes)

| Class | techniqueID | What it is |
|---|---|---|
| `fl:a_smuggle` | `FL.T1` | Cross-border smuggling of victims |
| `fl:a_harbor` | `FL.T2` | Harboring / residential captivity |
| `fl:a_coerce` | `FL.T3` | Force / threats / fraud / coercion (incl. fabricated debt) |
| `fl:a_compel_labor` | `FL.T4` | Compel labor / services |
| `fl:a_seize_wages` | `FL.T5` | Wage seizure / debt-bondage collection |

## Exemplar

`forced-labor-exemplar.ttl` carries **two** real `traj:Trajectory`
instances over the same shared phase/transition vocabulary (elder-fraud
pattern):

- `ibx:trajectory-highland-park` — full run through `WageAppropriation`,
  `traj:terminalPolarity "completed"`.
- `lgx:trajectory-davidson-salon` — short run ending mid-chain at
  `ForcedLabor`, `traj:terminalPolarity "disrupted"`. Luong recruitment
  method is unspecified in the source → confidence 55 on that phase.

### `traj:enactsAction` wiring (arriving-state; multi-valued edges)

| Transition | `enactsAction` | Produces |
|---|---|---|
| `Recruitment -> Control` | `a_smuggle`, `a_harbor`, `a_coerce` (Ibanez); `a_coerce` (Luong) | `Control` |
| `Control -> ForcedLabor` | `a_compel_labor` (both) | `ForcedLabor` |
| `ForcedLabor -> WageAppropriation` | `a_seize_wages` (Ibanez only) | `WageAppropriation` |

## Validation

```python
from case_uco.validation import validate_graph_file

validate_graph_file(
    "extensions/forced-labor/forced-labor-exemplar.ttl",
    extensions=["forced-labor"],
    profiles=["time", "prov-o"],
    strict_concepts=True,
    force_rdfs_inference=True,
)
```

`depends_on: ["trajectories", "attack-technique"]` in `manifest.json` pulls
in both automatically.
