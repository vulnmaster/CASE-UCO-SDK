# Forced-Labour Exploitation State Machine Extension (`forced-labor`)

Narrow, machine-only extension: contributes **only** what the
[trajectories](../trajectories/) Exploitation State Machine (ESM) needs to
run on a forced-labour / labour-trafficking offense — a phase vocabulary
and a small action catalog. No class hierarchy beyond the UCO 1.5.0
`uco-action:Technique` metaclass pattern. The MITRE ATT&CK catalog
(`attack-technique`) is not a dependency.

The `fl:` alphabet predates this package. [`layered`](../layered/) has
occupied `fl:Recruitment`, `fl:Control` and `fl:ForcedLabor` and typed
actions with `fl:a_coerce` (renamed `fl:a_coerce_labor` here so the registry
local name does not collide with `trafficking`'s `a_coerce`) and
`fl:a_compel_labor` since 0.2.0, declaring
the states inline in its Atkinson exemplar because no package existed and
leaving the two techniques undeclared. This extension declares that
alphabet once, keeps every IRI the layered exemplar uses, and adds the
phase (`WageAppropriation`) and techniques a complete chain needs.
`layered` now depends on it.

**CAC crosswalk.** No CAC class is retyped and CAC is never
`owl:imports`-ed. CAC has no forced-labour module, and its trafficking
module (`cacontology-sex-trafficking.ttl`, CAC 3.1.0) is scoped to sex
trafficking of children, so `skos:exactMatch` is not used. Two phases
overlap classes that module declares and carry a documentation-only
`skos:closeMatch`:

| `fl:` phase | `skos:closeMatch` | Why |
|---|---|---|
| `fl:Recruitment` | `cacontology-trafficking:VictimRecruitment` | Same act (acquiring victims), different offense scope. |
| `fl:Control` | `cacontology-trafficking:VictimControlSituation` | `fl:Control` is a state, so it matches the ongoing-control Situation rather than the `VictimControl` event. |

`fl:ForcedLabor` and `fl:WageAppropriation` have no CAC counterpart.

## Grounding

The alphabet is not derived from the two cases alone. It follows the ILO
definition of forced labour (Convention No. 29, 1930) and the [ILO
indicators of forced labour](https://www.ilo.org/publications/ilo-indicators-forced-labour)
(SAP-FL, 2012; revised edition 2025), eleven signs: abuse of
vulnerability, deception, restriction of movement, isolation, physical and
sexual violence, intimidation and threats, retention of identity documents,
withholding of wages, debt bondage, abusive working and living conditions,
excessive overtime. Forced labour is defined by Convention No. 29 and
exists with or without trafficking. The [UN Trafficking in Persons
Protocol](https://www.ohchr.org/en/instruments-mechanisms/instruments/protocol-prevent-suppress-and-punish-trafficking-persons)
(Palermo, 2000, art. 3(a)) applies when a chain also has a trafficking
act: it defines trafficking as act (recruitment, transportation, transfer,
harbouring, receipt), means (threat or use of force, coercion, fraud,
deception, abuse of a position of vulnerability) and purpose, and lists
"forced labour or services" among the purposes. A chain that includes a
recruitment-type act, carried out by a listed means, for the purpose of
forced labour, falls within that definition. Occupying `fl:Recruitment`
establishes none of those three on its own: the act is the enacted
action, the means is what its `uco-action:instrument` records, and the
purpose is the terminal state the chain reaches. A chain that starts at
`Control` with no recruitment act in the source, as the Cyprus case does,
is forced labour under Convention No. 29 and makes no trafficking claim.

| Element | Derived from |
|---|---|
| `fl:Recruitment` | Palermo act (recruitment); ILO indicator: deception when the promise is false |
| `fl:Control` | ILO indicators: retention of identity documents, intimidation and threats, restriction of movement, isolation, abuse of vulnerability, debt bondage; Palermo means |
| `fl:ForcedLabor` | ILO definition (work exacted under menace of a penalty); indicators: abusive working and living conditions, excessive overtime |
| `fl:WageAppropriation` | ILO indicator: withholding of wages; Palermo purpose ("forced labour or services") |
| `fl:a_deceive_recruit` | ILO indicator: deception; Palermo means (fraud, deception) |
| `fl:a_coerce_labor` | ILO indicators: retention of identity documents, intimidation and threats, abuse of vulnerability, debt bondage; Palermo means (coercion, abuse of a position of vulnerability) |
| `fl:a_compel_labor` | ILO definition; indicators: excessive overtime, abusive working conditions |
| `fl:a_appropriate_wages` | ILO indicator: withholding of wages |

Coverage of the eleven ILO indicators, so that gaps are explicit:

| ILO indicator | Covered by |
|---|---|
| Abuse of vulnerability | `fl:Control` (state only; no technique) |
| Deception | `fl:a_deceive_recruit` |
| Restriction of movement | `fl:Control`, `fl:a_coerce_labor` (document retention) |
| Isolation | not covered |
| Physical and sexual violence | not covered |
| Intimidation and threats | `fl:Control`, `fl:a_coerce_labor` |
| Retention of identity documents | `fl:Control`, `fl:a_coerce_labor` |
| Withholding of wages | `fl:WageAppropriation`, `fl:a_appropriate_wages` |
| Debt bondage | not covered |
| Abusive working and living conditions | `fl:ForcedLabor` (state only; recorded on the instrument) |
| Excessive overtime | `fl:ForcedLabor`, `fl:a_compel_labor` |

Isolation, violence and debt bondage have no state or technique because
neither source case describes them. They are the first candidates for
0.2.0 once a public source supplies them.

A state is an occupancy a trajectory can be in; a technique is the act
that produces it. `fl:WageAppropriation` (the worker is being underpaid or
unpaid over an interval) and `fl:a_appropriate_wages` (the offender's act
on a transition) are the same pair that `trafficking` draws between
`EarningsCollection` and `a_collect_earnings`.

## Case

**Europol/ELA action week against labour exploitation, 14–20 September
2026.** Source: Europol newsroom, ["27 arrests and 248 potential victims
identified in action week against labour
exploitation"](https://www.europol.europa.eu/media-press/newsroom/news/27-arrests-and-248-potential-victims-identified-in-action-week-against-labour-exploitation)
(2026-10-23) — cited as "PR". Two of the release's highlighted cases are
modelled: a farm worker in Cyprus whose employer kept his passport and
paid nothing for ten-hour days, and farm workers in Romania taken on under
a false promise of fair pay for twelve-hour days with no wages. No suspect, victim or employer is named
in the source, so none is named here. Neither case gives a start date, so
every interval is bounded only on the right by the end of the action week,
and both chains are terminal `disrupted`.

## Phases (`fl:PhaseScheme`)

| State | What it is | Source |
|---|---|---|
| `fl:Recruitment` | Worker engaged for the labour, often on a false basis | PR, Romania |
| `fl:Control` | Freedom to leave or seek help restricted: documents withheld, threats, dependency, irregular status | PR, Cyprus, Netherlands, Poland |
| `fl:ForcedLabor` | Labour under hours and conditions the worker cannot refuse | PR, Cyprus, Romania |
| `fl:WageAppropriation` | Wages withheld or underpaid and retained | PR, Cyprus, Romania, Netherlands |

## Actions (`uco-action:Technique` classes)

| Class | techniqueID | What it is |
|---|---|---|
| `fl:a_deceive_recruit` | `FL.T1` | Recruit by deception (affordance: the job offer) |
| `fl:a_coerce_labor` | `FL.T2` | Coerce continued labour (affordance: withheld document, threat, dependency) |
| `fl:a_compel_labor` | `FL.T3` | Compel labour (affordance: the job placement) |
| `fl:a_appropriate_wages` | `FL.T4` | Appropriate wages (affordance: control of the payroll) |

## Exemplar

`forced-labor-exemplar.ttl` carries two `traj:Trajectory` instances, one
per highlighted case, so that every phase and every technique is exercised
by at least one of them:

| Trajectory | Occupancy | Coverage |
|---|---|---|
| `flx:trajectory-cyprus` | Control → ForcedLabor → WageAppropriation | partial (recruitment not described) |
| `flx:trajectory-romania` | Recruitment → ForcedLabor → WageAppropriation | partial (no control act described) |

### `traj:enactsAction` wiring

Follows the arriving-state convention in
[`trajectories/README.md`](../trajectories/README.md#enactsaction-convention-arriving-state-not-leaving-state):
each transition's `enactsAction` is the action that *produces* its
`toState`. Where two co-occurring techniques produce the same state, both
are wired on that edge.

| Transition | `enactsAction` | Produces |
|---|---|---|
| `Control -> ForcedLabor` (Cyprus) | `fl:a_compel_labor` + `fl:a_coerce_labor` | `ForcedLabor` |
| `ForcedLabor -> WageAppropriation` (Cyprus) | `fl:a_appropriate_wages` | `WageAppropriation` |
| `Recruitment -> ForcedLabor` (Romania) | `fl:a_compel_labor` | `ForcedLabor` |
| `ForcedLabor -> WageAppropriation` (Romania) | `fl:a_appropriate_wages` | `WageAppropriation` |

`fl:a_deceive_recruit` characterises the Romania `Recruitment` state. As
with every alphabet's s₀, there is no incoming edge to attach it to, so it
is asserted as the performed action that the `Recruitment` phase assertion
cites rather than as an `enactsAction`.

The exemplar also carries one `traj:StateMachineModel` with two
illustrative `TransitionEstimate`s, as the sibling alphabets do, because
the trajectories shapes require at least one estimate per model.

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

# Must NOT conform:
validate_graph_file(
    "extensions/forced-labor/forced-labor-invalid-exemplar.ttl",
    extensions=["forced-labor"],
    profiles=["time", "prov-o"],
    strict_concepts=True,
    force_rdfs_inference=True,
)
```

CLI: pass `forced-labor.ttl`, `forced-labor-shapes.ttl` and the trajectories
OWL/shapes via `--ontology-graph` with `--inference rdfs --allow-info`.
