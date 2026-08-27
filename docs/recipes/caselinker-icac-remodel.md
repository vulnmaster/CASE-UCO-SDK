# CaseLinker ICAC Remodel

> See [Recipe Index](INDEX.md) for all recipes.

Remodel public CaseLinker CAC graphs so ICAC detective, commander, and
prosecutor questions are SPARQL-answerable. Encode only what the source
establishes. Do not copy `caselinker:/resource/vocab/*` predicates into
SDK output.

Validated against `examples/caselinker-icac-remodel/`.

Probe the live CaseLinker corpus before remodeling source documents. The
2026-08-27 snapshot and current-shape questions are in
[CURRENT_STATE_PROBE.md](../../examples/caselinker-icac-remodel/CURRENT_STATE_PROBE.md).
v1.27.0 target joins (`InvestigationTrigger`, hashed series,
`legalproc` charge–sentence, phase end, disclosure) were absent; tip,
proceeding, and phase-begin questions already answer on current CAC
shapes.

A ten-graph source-document pilot remodeled from the original CaseLinker
press-release URLs is in
[pilot/PILOT.md](../../examples/caselinker-icac-remodel/pilot/PILOT.md)
and [pilot/CORPUS.md](../../examples/caselinker-icac-remodel/pilot/CORPUS.md).
It adds `InvestigationTrigger` only when that source assigns a CyberTip
to the matter, and it refuses `legalproc` charge classes when the
release omits a statute citation. Many CaseLinker `dcterms:source` URLs
are operations, program stats, or dead links and cannot be remodeled as
one investigation.

## When to use this recipe

- A CaseLinker named graph has a CyberTip and a `CACInvestigation` but no
  `InvestigationTrigger`
- Type-only `ContentDataFacet` nodes or private CaseLinker vocab must be
  replaced before `validate_graph`
- You need generic `ICACtaskForce` clocks and victim-count integrity
- You are dual-typing CAC charges with `legalproc`

Use [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md) for new CyberTip
graphs. Use [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md)
for legal stages. Use [legal-discovery-disclosure.md](legal-discovery-disclosure.md)
for Brady / Giglio / Jencks. Use
[technique-evidence-outcome.md](technique-evidence-outcome.md) when a later
lab source names an **examiner** method (SOLVE-IT). Do not follow
`route_investigation_content` into the CTI / ATT&CK family for a CAC
press release.

## Vocabulary: CAC offender vs ATT&CK attacker

MITRE ATT&CK is **not** the language of the crimes-against-children
community. A CAC **offender** targets children and other vulnerable
people. ATT&CK models **hackers** and **attackers** — intrusion
tradecraft against systems and networks.

Do not type CAC grooming, sextortion, CyberTips, or CSAM possession as
ATT&CK techniques, and do not call the CAC subject an attacker or threat
actor. An ATT&CK mapping on a `CACInvestigation` is appropriate only on
the rare occasion the source actually describes that overlap (for
example, a sourced intrusion used to obtain the material). Even then,
keep ATT&CK on the attacker `Action` and keep examiner method in
SOLVE-IT. See [cyber-threat-intelligence.md](cyber-threat-intelligence.md).

## Source-fidelity table

| CaseLinker shape | Remodel as | Do not emit |
|---|---|---|
| Tip + investigation in one named graph | `InvestigationTrigger` with `triggeredBy` + `resultedInInvestigation` | Tip as the only `hasStep`; `usedTechnique` from `…/tech/cybertipline` |
| Tip `rdfs:label` only | Keep the report; add `hasNCMECIncidentType` only when the source names a type | Invented incident classes |
| Type-only `ContentDataFacet` | Drop the facet, or replace with hash/size/MIME from a lab source | Empty facets; invented PhotoDNA hex |
| `CriminalCharge` + `CSAM_Possession` | `legalproc:StateCharge` or `FederalCharge` when jurisdiction is sourced | `legalproc:FederalCharge` inferred from an agency name |
| Sentence type + label | `legalproc:Sentence` with `sentenceStatus`, `sentenceKind`, `appliesTo` | Label-only sentences; undeclared `chargeCluster` |
| One `VictimRole` + prose “victims” | N victim-role nodes, or `victimFactStatus` `omitted` | A zero count for omitted victims |
| Maryland-only TF class on a non-Maryland case | `ICACtaskForce` + lead unit | `MarylandICACtaskForce` unless the source is Maryland |

## CaseLinker vocab map

<!-- recipe-lint: ignore-start anti-pattern -- The Drop column names undeclared CaseLinker private predicates that must not appear in remodeled output. -->
| Drop | Replace with |
|---|---|
| `caselinker:chargeCluster` | Drop thematic tokens; emit `legalproc:statuteCitation` only when the source states a statute |
| `caselinker:chargeOffenseEvent` | `legalproc:concernsCharge` or `Related_To` |
| `caselinker:attributedToOffenderRole` | `uco-action:performer` |
| `admissionTheme` / `admissionContext` / `quoteType` / `admissionFrame` / `evidenceTier` | Drop unless a sourced CAC statement class applies |
<!-- recipe-lint: ignore-end anti-pattern -->

`map_caselinker_predicate` / `refuse_caselinker_vocab` in
`mcp_server/tools/caselinker_icac_remodel.py` enforce this.

## Factory

```python
from tools.caselinker_icac_remodel import (
    join_cybertip_investigation,
    build_share_safe_series_match,
    set_phase_clock,
    participating_agency,
    build_and_write,
)

build_and_write("cybertip-join", "cybertip-join.jsonld")
```

Share-safe series matches record a sourced SHA-256 and a series
`ExternalReference`. They tag `photodna-match-reported-value-withheld`
instead of minting a PhotoDNA hex.

Participating agencies use one `uco-action:performer` plus a `Related_To`
partner edge so CAC `maxCount 1` still validates. Phase clocks use
`xsd:dateTimeStamp`. A without-incident warrant arrest uses
`ArrestOperation` with `arrestType` `warrant_arrest` and sourced
`resistanceExpected` / `weaponsExpected` / `targetCount`.

## Anti-patterns

- Emitting `https://caselinker.up.railway.app/resource/vocab/*`
- `solveit-core:usedTechnique` for a CyberTipline method IRI
- Empty `ContentDataFacet()`
- Inferring Brady from unlabeled exam notes
- Inventing warrant or phase-end times the source does not state
- Mapping thematic CaseLinker cluster tokens to `legalproc:statuteCitation`
- Replacing empty incident `ContentDataFacet` nodes with invented file hashes
- Mapping CAC offender conduct to MITRE ATT&CK, or calling the CAC
  subject an attacker / threat actor, unless the source describes that
  rare overlap

## Related

- [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md)
- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md)
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md)
- [legal-discovery-disclosure.md](legal-discovery-disclosure.md)
- [technique-evidence-outcome.md](technique-evidence-outcome.md)
