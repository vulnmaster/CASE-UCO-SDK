# SOLVE-IT Investigation Planning and Error Mitigation

> See [Recipe Index](INDEX.md) for all recipes.

Plan and document forensic procedure with
[SOLVE-IT](https://solveit-df.org) — the Systematic Objective-based
Listing of Various Established digital Investigation Techniques — inside a
CASE/UCO graph. SOLVE-IT organizes digital forensic practice as
**objectives** (what the investigation needs to achieve) → **techniques**
(how to achieve it) → **weaknesses** (what can go wrong, classified per
ASTM E3016-18) → **mitigations** (what reduces the risk). Where most
recipes model *evidence*, this recipe models *method*: which technique was
executed, which mitigations were applied, and how residual risk was
assessed — the systematic Error Mitigation Analysis that examination
reports and quality-assurance reviews increasingly expect.

The SDK vendors a pinned SOLVE-IT snapshot in `ontology/solveit/`
(ontology + compiled knowledge base: 23 objectives, 187 techniques, 339
weaknesses, 270 mitigations; see the manifest `provenance` block for exact
versions; refresh with `make sync-solveit`).

Validated against `examples/solveit/` (synthetic laptop acquisition) and
`ontology/solveit/solveit-exemplar.ttl`.

**When to use this recipe**

- The submission concerns *how* an examination is (or was) performed:
  acquisition plans, technique selection, tool testing, dual-tool
  verification, quality assurance, lab accreditation, error rates,
  Daubert-style methodology challenges
- An examination report must document which techniques were used and which
  known weaknesses were considered and mitigated
- An agent is planning investigative steps and needs the established
  technique catalog with per-technique risk checklists —
  `plan_solveit_workflow` is the entry point
- For the evidence produced *by* those steps (files, devices, messages),
  pair this recipe with the evidence-type recipe
  ([starter-filesystem-report.md](starter-filesystem-report.md),
  [starter-mobile-extraction.md](starter-mobile-extraction.md), ...) and
  [forensic-lifecycle.md](forensic-lifecycle.md) for phase ordering

## Discovering the right techniques (MCP tools)

```text
plan_solveit_workflow("image the seized laptop and verify integrity")
  -> matched objectives (DFO-1006 Acquire data),
     candidate techniques (DFT-1002 Copy sectors from storage media, ...),
     per-technique error_mitigation_checklist (weaknesses + mitigations)

search_solveit("hash", kind="mitigation")   # keyword search, any kind
get_solveit_details("DFT-1002")             # full record + relationships
```

`search_classes(scope="solveit")` finds the ontology classes
(SolveitInvestigativeAction, PhysicalImageContainer, WeaknessEvaluation,
punned DFT-* technique classes) when `CASE_UCO_EXTENSIONS=solveit`.

## Classes and properties

| Term | Role |
|---|---|
| `case-investigation:Investigation` | Case container; state the SOLVE-IT objective (DFO-*) in `description` |
| `solveit-core:SolveitInvestigativeAction` | An investigative action that records its method — subclass of `case-investigation:InvestigativeAction` |
| `solveit-core:usedTechnique` | The knowledge-base technique executed (DFT-* individual) |
| `solveit-core:appliedMitigation` | Each mitigation actively applied (DFM-* individual) |
| `solveit-observable:PhysicalImageContainer` / `LogicalImageContainer` / `RawImage` | Acquisition outputs; SHACL requires `solveit-observable:contains` a `Bitstream`/`FileSet` |
| `solveit-observable:HashVerificationResult` | Outcome of an integrity check |
| `solveit-observable:Timeline` / `TimelineEntry` / `KeywordIndex` / `Wordlist` / ... | ~60 method-centric observables across the observable modules |
| `solveit-wa:WeaknessEvaluation` | Risk rating of one weakness (likelihood × impact, optional detectability → RPN) — subclass of `uco-analysis:AnalyticResult` |
| `solveit-wa:WeaknessEvaluationSet` | One assessment session, `scopedToTechnique`, `evaluatedBy` an Identity |
| `solveit-data:techniqueDFT-*` (punned classes) | UCO 1.5.0 metaclass style: type an Action directly with the technique class |

## Modeling patterns

### 1. State the objective, then record method with SolveitInvestigativeAction

Reference the canonical knowledge-base IRIs
(`https://ontology.solveit-df.org/solveit/data/techniqueDFT-1002` etc.) —
they are typed individuals in the vendored KB, so the graph stays
resolvable and validation sees their types:

```json
{
  "@id": "kb:acquire-action",
  "@type": "solveit-core:SolveitInvestigativeAction",
  "uco-core:name": "acquire-laptop-image",
  "solveit-core:usedTechnique": [{"@id": "solveit-data:techniqueDFT-1002"}],
  "solveit-core:appliedMitigation": [
    {"@id": "solveit-data:mitigationDFM-1003"},
    {"@id": "solveit-data:mitigationDFM-1004"}
  ],
  "uco-action:performer": {"@id": "kb:examiner"},
  "uco-action:instrument": {"@id": "kb:imaging-workstation"},
  "uco-action:object": [{"@id": "kb:laptop-ssd"}],
  "uco-action:result": [{"@id": "kb:physical-image"}]
}
```

`appliedMitigation` is a *positive assertion* — list only mitigations that
were actually performed. Mitigations that were considered and rejected
belong in the weakness evaluation rationale (pattern 3).

### 2. Type acquisition outputs with SOLVE-IT observables

The observable modules add method-centric classes UCO does not have. The
shapes enforce structure — a `PhysicalImageContainer` must `contains` a
`Bitstream`, a `TimelineEntry` must carry exactly one `timelineEntryValue`:

```json
{
  "@id": "kb:physical-image",
  "@type": "solveit-observable:PhysicalImageContainer",
  "uco-core:name": "E01 physical image of laptop SSD",
  "solveit-observable:contains": [{"@id": "kb:bitstream"}]
}
```

### 3. Error Mitigation Analysis with WeaknessEvaluation

For each selected technique, review its known weaknesses
(`get_solveit_details("DFT-1002")` returns them with their ASTM E3016-18
categories) and rate the residual risk for *this* case:

```json
{
  "@id": "kb:dfw-1004-evaluation",
  "@type": "solveit-wa:WeaknessEvaluation",
  "solveit-wa:evaluatesWeakness": {"@id": "solveit-data:weaknessDFW-1004"},
  "solveit-wa:likelihoodRating": {"@type": "xsd:integer", "@value": "1"},
  "solveit-wa:likelihoodRationale": "Write blocker in use; no damaged-media indicators.",
  "solveit-wa:impactRating": {"@type": "xsd:integer", "@value": "3"},
  "solveit-wa:impactRationale": "Missing sectors would silently omit evidence.",
  "solveit-wa:liImpactScore": {"@type": "xsd:integer", "@value": "3"}
}
```

Group a session's evaluations in a `solveit-wa:WeaknessEvaluationSet` with
`scopedToTechnique`, `evaluatedBy`, and `evaluationDate`.

### 4. Both technique styles interoperate (UCO 1.5.0 readiness)

The extension ships a generated catalog
(`solveit-technique-catalog.ttl`) punning every DFT-* individual as an
`owl:Class` typed `uco-action:Technique` (ucoProject/UCO PR #676 — the
same pattern as MITRE ATT&CK in `extensions/attack-technique/`). So an
action may equivalently be *typed with* the technique:

```json
{
  "@id": "kb:verify-hash-action",
  "@type": ["uco-action:Action", "solveit-data:techniqueDFT-1042"],
  "uco-core:name": "verify-image-hash"
}
```

Use the native style (pattern 1) when you want `appliedMitigation` on the
same node today; use the metaclass style for forward-compatibility with
UCO 1.5.0's meta `Technique` class and for graphs that already type
actions with ATT&CK techniques. The IRIs are identical, so both styles can
appear in one graph and cross-query.

### 5. Validate with the solveit extension

```text
validate_graph(path, extensions=["solveit"])
```

The manifest pulls in `attack-technique` automatically (`depends_on`) so
the `uco-action:Technique` metaclass is declared, and loads the knowledge
base so referenced DFT-*/DFW-*/DFM-* individuals are typed. Strict concept
coverage passes for both modeling styles.

## Anti-patterns

- **Inventing technique IDs or IRIs.** Only DFT-*/DFW-*/DFM-*/DFO-*
  identifiers present in the pinned knowledge base resolve; check with
  `get_solveit_details(id)` first. If practice has outgrown the catalog,
  that is an upstream SOLVE-IT contribution, not a local IRI.
- **Asserting `appliedMitigation` for mitigations merely considered.**
  The property documents what was done; rationale text captures the rest.
- **Duplicating KB metadata into the case graph.** Don't copy technique
  descriptions/weakness lists onto your action nodes — link the canonical
  individual; the KB travels with the extension.
- **Using `solveit-core:Technique` as a facet or observable.** Techniques
  describe method, not evidence; evidence stays in UCO observables.

## Worked example

`examples/solveit/build_laptop_acquisition_solveit.py` builds
`laptop-acquisition-solveit.jsonld` (12 nodes: investigation, examiner,
tool, device, image container + bitstream, hash result, native-style
acquisition action, weakness evaluation + set, metaclass-style
verification action) and validates it with `extensions=["solveit"]`.
