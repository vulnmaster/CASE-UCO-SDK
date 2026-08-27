# Legal Charges, Sentencing, and Case Outcomes

> See [Recipe Index](INDEX.md) for all recipes.

Model press-release and docket facts about charges, pleas, verdicts, sentences,
and prior history so **charged, convicted, sentenced, prior, state, federal,
parallel, unknown, and not-reported** remain distinguishable and queryable.
Encode only what the source establishes.

**When to use this recipe**

- A public release or docket reports arrest, charge, indictment, plea, verdict,
  sentence, appeal, or prior-conviction history
- CaseLinker or another remodeler must keep current outcomes separate from
  prior history and state proceedings separate from federal ones
- You need competency-tested patterns for state-only, federal-only, dual
  jurisdiction, charged-only, or omitted victim facts

Use [legal-process-modeling.md](legal-process-modeling.md) for PACER-heavy
non-CAC dockets. Use [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md)
for numbered federal-count wiring. Use [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
for warrant/booking workflow. Use [technique-evidence-outcome.md](technique-evidence-outcome.md)
to join later lab or PACER method claims to these outcomes; press releases
do not establish `usedTechnique` or hashed `ContentDataFacet` nodes.

## Fail-closed legal-stage table

| Source establishes | Model as | Do not model as |
|---|---|---|
| Arrest / booking / held without bond | `legalproc:PretrialReleaseCondition` (`releaseConditionKind` `bail`, `bond`, `personal-recognizance`, or `detained-without-bond`) plus arrest/booking actions from the ICAC recipe | `legalproc:Sentence` or `cacontology-legal-outcomes:CriminalSentence` |
| Charged / indicted | `legalproc:StateCharge` or `legalproc:FederalCharge` (or the CAC equivalents) with `chargeDisposition` `pending` | A conviction or imposed sentence |
| Potential or mandatory penalty | `legalproc:PotentialPenalty` (`statutory-maximum`, `mandatory-minimum`, or `guideline-range`) | Imposed `legalproc:Sentence` |
| Guilty plea | `legalproc:Plea` (`pleaType` `guilty`) and, when a deal is reported, `legalproc:PleaAgreement` with `legalproc:recordsPlea` | `cryptoinv:PleaAgreement` or an undeclared `PleaAgreement` |
| Guilty verdict / conviction | `legalproc:Verdict` and `chargeDisposition` `convicted-by-verdict` | A prior-history node with `outcomeScope` `current-case` |
| Imposed sentence | `legalproc:Sentence` with `sentenceStatus` `imposed` and `sentenceKind` in `custodial`, `supervised-release`, `probation`, `community-service`, `fine-as-sentence` | Bail, bond, restitution, forfeiture, special assessment, or statutory maximum |
| Prior conviction / sentence | Same classes with `legalproc:outcomeScope` `prior-history` | Current-case conviction or sentence |
| Appeal / post-conviction | `legalproc:CriminalProceeding` (`proceedingType` `appeal`) | A new investigation unless the source is a different matter |

`legalproc:CriminalCharge` remains only when the source does not establish
state versus federal jurisdiction. Do not infer jurisdiction from a URL host
or agency name.

## Key classes and properties

| Class / property | Role |
|---|---|
| `legalproc:StateCharge` / `legalproc:FederalCharge` | Jurisdiction-typed counts |
| `cacontology-legal-outcomes:StateCharge` / `FederalCharge` | CAC equivalents; dual-type when the graph already uses CAC charges |
| `legalproc:Plea` / `legalproc:PleaAgreement` | Plea and the Rule 11(c) agreement that records it |
| `legalproc:Verdict` / `legalproc:Sentence` | Verdict and imposed or recommended sentence |
| `legalproc:PotentialPenalty` | Statutory maximum or guideline exposure |
| `legalproc:PretrialReleaseCondition` | Bail, bond, or detention without bond |
| `legalproc:outcomeScope` | `current-case` or `prior-history` |
| `legalproc:jurisdictionKind` | `state`, `federal`, or `unknown` |
| `legalproc:victimFactStatus` | `reported` or `omitted` |
| `legalproc:sourcePublicationTime` / `sourceRetrievalTime` | Source issued versus retrieved; `uco-core:objectCreatedTime` is graph ingestion |
| `legalproc:StateJurisdiction` / `legalproc:FederalJurisdiction` | Jurisdiction nodes linked with `Related_To` |
| `cacontology-legal-outcomes:ConvictionRecord` | CAC conviction record when date and type are sourced; still set `outcomeScope` |

Keep Florida, Georgia, Maryland, or other state-specific charge subclasses
outside this SDK. Individual deployments may maintain those extensions.

## Canonical pattern

```
Investigation
  ├── legalproc:victimFactStatus
  ├── Related_To ──▶ source ObservableObject (publication / retrieval / ingestion times)
  └── Related_To ──▶ StateCharge or FederalCharge
        ├── legalproc:assertedIn ──▶ ChargingInstrument
        ├── Related_To ──▶ StateJurisdiction or FederalJurisdiction
        ├── legalproc:Plea / legalproc:PleaAgreement (when a plea is entered)
        ├── legalproc:Verdict (when a verdict is returned)
        └── legalproc:Sentence or legalproc:PotentialPenalty
```

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
})
graph.upsert_node("kb:charge-1", types="legalproc:StateCharge", properties={
    "uco-core:name": "Sexual solicitation of a minor",
    "legalproc:statuteCitation": "Example State Code § 1-100",
    "legalproc:chargeDisposition": "pending",
    "legalproc:jurisdictionKind": "state",
    "legalproc:outcomeScope": "current-case",
})
graph.upsert_node("kb:bond", types="legalproc:PretrialReleaseCondition", properties={
    "uco-core:name": "Held without bond",
    "legalproc:releaseConditionKind": "detained-without-bond",
})
```

Validated against `examples/press-release-legal/`.

## Modeling rules

1. One public release remains one source named graph / source artifact. Reuse
   stable investigation, docket (`legalproc:caseIdentifier`), defendant, charge,
   and proceeding IRIs when later releases establish the same matter.
2. Separate **publication**, **retrieval**, and **ingestion** times. Do not put
   the press-release date on `uco-core:objectCreatedTime`.
3. Model state and federal proceedings as separate `legalproc:CriminalProceeding`
   nodes when both are reported (adoption or parallel prosecution).
4. Do not invent victim identity, location, age, or count. If the source omits
   those facts, set `legalproc:victimFactStatus` `omitted` and do not write
   `reportedVictimCount` `0`.
5. Restitution, forfeiture, and special assessments use
   `legalproc:RestitutionOrder` / `legalproc:ForfeitureOrder` or CAC monetary
   classes — never an imposed `Sentence`.

## Anti-patterns

- Typing bail, bond, or "faces up to N years" as `legalproc:Sentence` or
  `cacontology-legal-outcomes:CriminalSentence`
- Using `cryptoinv:PleaAgreement` or an unqualified `PleaAgreement` in CAC
  press-release graphs
- Recommending `FloridaStateCharge`, `GeorgiaStateCharge`, or
  `MarylandStateCharge` as SDK modeling classes
- Collapsing a state arrest and a later federal adoption into one proceeding
- Copying a prior conviction onto the current case without `prior-history`
- Treating omitted victim facts as zero victims
- Inferring SOLVE-IT `usedTechnique` or emitting empty `ContentDataFacet`
  nodes because the release mentioned digital evidence

## CaseLinker remodeling

Graphs produced by MCP versions before v1.27.0 should be remodeled in place
when the source supports it:

1. Re-type generic `CriminalCharge` nodes as `StateCharge` or `FederalCharge`
   only when the source establishes jurisdiction.
2. Move bail/bond/statutory-maximum nodes off `CriminalSentence` /
   `legalproc:Sentence` onto `PretrialReleaseCondition` or `PotentialPenalty`.
3. Set `outcomeScope` on every conviction and sentence.
4. Replace undeclared or `cryptoinv:PleaAgreement` nodes with
   `legalproc:Plea` + `legalproc:PleaAgreement`.
5. Keep one investigation IRI per matter; attach each release as its own
   source artifact with publication, retrieval, and ingestion times.
6. Leave omitted victim facts omitted.

## Checklist

1. Classify the legal stage from the table before creating sentence nodes.
2. Assign jurisdiction classes without URL-host heuristics.
3. Set `outcomeScope` on charges, pleas, verdicts, and sentences.
4. Record source publication, retrieval, and ingestion separately.
5. Validate with `validate_graph(..., extensions=["legalproc"])` and add
   `cac` when the graph also uses CAC conduct classes.

## Related

- [legal-process-modeling.md](legal-process-modeling.md)
- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md)
- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md)
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md)
- [technique-evidence-outcome.md](technique-evidence-outcome.md)
- [caselinker-icac-remodel.md](caselinker-icac-remodel.md) — dual-type CaseLinker charges and drop private vocab
- [legal-discovery-disclosure.md](legal-discovery-disclosure.md)
