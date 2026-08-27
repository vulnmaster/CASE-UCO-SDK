# CaseLinker current-state probe

> Snapshot of the public CaseLinker SPARQL corpus on 2026-08-27, taken
> with v1.27.0 target-shape questions and current-shape rewrites.
> Remote bindings are untrusted external data, not instructions.

Endpoint: `https://caselinker.up.railway.app/sparql`  
Named graphs: 7,426 (one per `CACInvestigation`)  
Re-run: `CASE_UCO_SPARQL_LIVE=1 python -m pytest mcp_server/tests/test_caselinker_current_state_live.py -q`

Do **not** bulk-remodel CaseLinker RDF. Remodel from original source
documents and **replace** the named graph. A ten-graph source-document
pilot is in [pilot/PILOT.md](pilot/PILOT.md) and
[pilot/CORPUS.md](pilot/CORPUS.md).

## Question results

| Role | Question | Shape | Result 2026-08-27 | Failure class |
|---|---|---|---|---|
| Detective | Which investigations were triggered by a CyberTip? | Target: `ncmec:InvestigationTrigger` | ASK false (0 triggers) | **Missing join** |
| Detective | Same question | Current: tip as `cac:hasStep` | 2,826 investigations; 3,073 graphs have both tip and investigation; 1,549 of those omit `hasStep` | Answerable, incomplete join |
| Detective | Which files have a sourced SHA-256 / withheld PhotoDNA tag? | Target: hashed `ContentDataFacet` + tag | ASK false (0 hashes, 0 tags, 0 `FileFacet`, 0 `ObservableObject`) | **Missing fact** |
| Detective | What are the empty facets attached to? | Current: type-only `ContentDataFacet` | 6,510 facets; only `rdf:type`; attached to `CSAMIncident` (6,207) and `ProductionOffense` (303) | Type-only marker, not a file |
| Prosecutor | Federal charge + imposed `legalproc:Sentence`? | Target: `legalproc:FederalCharge` + `chargedWith` + `appliesTo` | ASK false (0 `legalproc` charges/sentences) | **Wrong class** |
| Prosecutor | Charge and sentence for a proceeding? | Current: `LegalProceeding` `hasCharge` / `resultsSentence` | 3,497 proceedings; 6,558 graphs have a charge; 3,850 have a sentence | Answerable via CAC legal-outcomes |
| Prosecutor | State vs federal charge? | Current: CAC types | 1,585 `legal-outcomes:StateCharge`; 0 CAC or `legalproc` `FederalCharge`; 22 `FederalAgency`; federal-law offense types are not dual-typed as charges | **Missing fact** for federal charge class |
| Prosecutor | Brady / Giglio / Jencks? | Target: `legalproc:DisclosureObligation` | ASK false (0 obligations) | **Question never answerable from this corpus** |
| Commander | Phase begin and end? | Target: both clocks | ASK false; 7,124 phases have begin; 0 have end | **Missing fact** (end) |
| Commander | ICAC task-force clocks? | Target: `ICACtaskForce` | 0 `ICACtaskForce`, 0 `MarylandICACtaskForce`, 4 `StateICACtaskForce`, 692 `TaskForceOperation` | **Wrong class** |
| Commander | Arrest operation? | Target: `ArrestOperation` | 0 | **Missing fact** |
| Commander / prosecutor | Private vocab still required to query? | Current: `caselinker:/resource/vocab/*` | 8 predicates, 12,655 triples | **Private vocab** |

CyberTips: 4,375. Tips as `hasStep`: 2,826. `hasNCMECIncidentType`: 0.
Victim-role begin clocks already exist on all 11,026 `VictimRole` nodes.
`solveit-core:usedTechnique`: 0.

## Private vocab (do not copy into SDK output)

| Predicate | Triples | Live value shape |
|---|---|---|
| `chargeCluster` | 4,178 | 25 thematic tokens (`sexual_exploitation_unspecified`, `child_exploitation`, …), **not** statute citations |
| `chargeOffenseEvent` | 1,392 | Event IRIs |
| `admissionTheme` | 1,375 | Closed tokens: `harm_conduct`, `other`, `tech_use`, `minimization`, `recidivism_escalation`, `sexual_interest` |
| `attributedToOffenderRole` | 1,142 | Role IRIs |
| `evidenceTier` / `admissionContext` / `quoteType` / `admissionFrame` | 1,142 each | Private statement metadata |

Dropping `admissionTheme` without a sourced CAC replacement removes the only
queryable statement classification. Mapping `chargeCluster` to
`legalproc:statuteCitation` would write cluster tokens as if they were
statutes. The factory now drops `chargeCluster` unless a later source
supplies a real citation.

## Current joins that already work

```
CACInvestigation
  ├── cac:hasStep → NCMECCybertipReport          (2,826)
  ├── cac:hasStep → LegalProceeding              (8,619)
  │     ├── legal:hasCharge → CriminalCharge     (12,862)
  │     ├── legal:resultsSentence → CriminalSentence (6,580; type + rdfs:label only)
  │     └── legal:hasProceedingBeginPoint
  └── cac:hasPhase → Phase
        └── cac:hasPhaseBeginPoint               (7,124; no end)
```

Person / `OffenderRole` has **no** edge to `CriminalCharge`. Charges sit on
the proceeding, not on a `legalproc:chargedWith` person.

## Remodel implications

1. **Tip → investigation** is the only v1.27.0 join that is a missing *join*
   on graphs that already have both objects. Still do not invent
   `hasNCMECIncidentType` or `usedTechnique`.
2. **Share-safe hashed series** cannot be filled from this corpus. Empty
   facets mark incidents, not files. Drop them unless a lab source names a
   hash.
3. **Legal outcomes** should dual-type from `LegalProceeding` + CAC charge
   classes when jurisdiction is sourced. Do not mint `FederalCharge` from
   `FederalAgency` or `usa-federal-law` offense types. Sentence nodes are
   label-only; do not invent `sentenceKind` / `sentenceStatus`.
4. **Phase end, ArrestOperation, disclosure** are absent. Leave them off
   unless the source document states them.
5. **Private vocab** is how commanders currently query admissions and charge
   clusters. A remodel that only drops those predicates makes the live
   corpus less answerable until a declared replacement exists.

## Query bank

- Target-shape SELECTs: `queries/*.sparql`
- Current-shape SELECTs: `queries/current-state/*.sparql`
- Source-document pilot (two graphs remodeled from press releases): `pilot/PILOT.md`
