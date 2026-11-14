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
(SOLVE-IT ontology 0.2.17 + compiled knowledge base: 24 objectives, 207
techniques, 454 weaknesses, 348 mitigations, 165 citations; see the
manifest `provenance` block for the exact commit and SHA-256 digests;
refresh with `make sync-solveit`).

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
get_solveit_details("DFT-1002")             # full record, relationships,
                                            # citations (DFCite-*) and the
                                            # inline catalog_entry_jsonld
```

Cite SOLVE-IT's own sources when you justify a technique choice:
`get_solveit_details` returns each technique's, weakness's and
mitigation's `citations` (identifier plus plain-text reference).

`search_classes(scope="solveit")` finds the ontology classes
(SolveitInvestigativeAction, PhysicalImageContainer, WeaknessEvaluation,
the DFT-* technique classes) when `CASE_UCO_EXTENSIONS=solveit`.

## Classes and properties

| Term | Role |
|---|---|
| `case-investigation:Investigation` | Case container; state the SOLVE-IT objective (DFO-*) in `description` |
| `solveit-core:SolveitInvestigativeAction` | An investigative action that records its method — subclass of `case-investigation:InvestigativeAction` |
| `solveit-data:techniqueDFT-*` | The technique performed: an `owl:Class` (subclass of `SolveitInvestigativeAction`) that is also a `uco-action:Technique`; type the action with it |
| `solveit-core:appliedMitigation` | Each mitigation actively applied (DFM-* individual) |
| `solveit-observable:PhysicalImageContainer` / `LogicalImageContainer` / `RawImage` | Acquisition outputs; SHACL requires `solveit-observable:contains` a `Bitstream`/`FileSet` |
| `solveit-observable:HashVerificationResult` | Outcome of an integrity check |
| `solveit-observable:Timeline` / `TimelineEntry` / `KeywordIndex` / `Wordlist` / ... | ~60 method-centric observables across the observable modules |
| `solveit-wa:WeaknessEvaluation` | Risk rating of one weakness (likelihood × impact, optional detectability → RPN) — subclass of `uco-analysis:AnalyticResult` |
| `solveit-wa:WeaknessEvaluationSet` | One assessment session, `scopedToTechnique`, `evaluatedBy` an Identity |
| `solveit-analysis:Hypothesis` subclasses (`HypothesisedRecord`, `HypothesisedConfiguration`, `HypothesisedTableAttribution`, ...) | Claims inferred from artefacts rather than observed, e.g. a carved SQLite record or its table attribution |

## Modeling patterns

### 1. State the objective, then type the action with the technique it performed

SOLVE-IT 0.2.x models each technique as a class: `techniqueDFT-1002` is an
`owl:Class` and `rdfs:subClassOf solveit-core:SolveitInvestigativeAction`,
and the SDK's catalog (`solveit-technique-catalog.ttl`) also types it
`uco-action:Technique`, the UCO 1.5.0 metaclass used for MITRE ATT&CK and
ATLAS. An action that performed the technique is an instance of that
class. `solveit-core:usedTechnique` is `owl:deprecated` upstream; don't
use it in new graphs.

```json
{
  "@id": "kb:acquire-action",
  "@type": [
    "solveit-core:SolveitInvestigativeAction",
    "solveit-data:techniqueDFT-1002"
  ],
  "uco-core:name": "acquire-laptop-image",
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

### 4. Restate the catalogue entry when a technique is a value

`scopedToTechnique` uses the technique as an *object*, and SOLVE-IT's
`TechniqueShape` then requires exactly one `solveit-core:techniqueID` on
it. `case_validate` loads the knowledge base as an ontology graph, and
pySHACL copies only class-level triples (types, `rdfs:subClassOf`,
labels) of `owl:Class` nodes into the data graph, so a bare IRI fails.
Do what upstream's own examples do and restate the minimal entry in the
case graph. `get_solveit_details` returns it as `catalog_entry_jsonld`,
and builders can call `solveit_index.technique_catalog_entry("DFT-1002")`:

```json
{
  "@id": "solveit-data:techniqueDFT-1002",
  "@type": ["owl:Class", "solveit-core:Technique"],
  "rdfs:subClassOf": {"@id": "solveit-core:SolveitInvestigativeAction"},
  "rdfs:label": {"@value": "DFT-1002: Copy sectors from storage media", "@language": "en"},
  "solveit-core:techniqueID": "DFT-1002",
  "solveit-core:techniqueName": "Copy sectors from storage media"
}
```

Typing an action with the technique (pattern 1) doesn't need this. The
same metaclass pattern works on a plain `uco-action:Action`
(`"@type": ["uco-action:Action", "solveit-data:techniqueDFT-1042"]`); the
technique class makes it a `SolveitInvestigativeAction` under RDFS
inference. ATT&CK and ATLAS are different vocabularies: they describe the
adversary, while SOLVE-IT describes the examiner. Add them to the same graph
only when the evidence shows the adversary's tradecraft
([cross-ontology composition](cross-ontology-composition.md), principle 6).

### 5. Validate with the solveit extension

```text
validate_graph(path, extensions=["solveit"])
```

The `uco-action:Technique` metaclass comes from UCO 1.5.0, so the extension
has no dependencies. It loads the knowledge base so referenced
DFT-*/DFW-*/DFM-* terms are typed, and adds SOLVE-IT's own
shapes (`solve_it_observable_shapes.ttl`, `solve_it_core_shapes.ttl`,
`solve_it_analysis_shapes.ttl`).

## Anti-patterns

- **Inventing technique IDs or IRIs.** Only DFT-*/DFW-*/DFM-*/DFO-*
  identifiers present in the pinned knowledge base resolve; check with
  `get_solveit_details(id)` first. If practice has outgrown the catalog,
  that is an upstream SOLVE-IT contribution, not a local IRI.
- **Asserting `appliedMitigation` for mitigations merely considered.**
  The property documents what was done; rationale text captures the rest.
- **Using the deprecated `solveit-core:usedTechnique`.** Type the action
  with the technique class instead (pattern 1). With the knowledge base
  loaded it also fails `TechniqueShape`, for the reason in pattern 4.
- **Duplicating KB metadata into the case graph.** Beyond the minimal
  catalogue entry in pattern 4, don't copy technique descriptions or
  weakness lists onto your nodes; the KB travels with the extension.
- **Using `solveit-core:Technique` as a facet or observable.** Techniques
  describe method, not evidence; evidence stays in UCO observables.
- **Auto-asserting DFT-* from a product catalog.**
  `le_tool_solveit_profiles.json` is a suggestion list. Type an action
  with a DFT-* class only when the lab report or affidavit establishes the
  method. See [technique-evidence-outcome.md](technique-evidence-outcome.md).

## Worked example

`examples/solveit/build_laptop_acquisition_solveit.py` builds
`laptop-acquisition-solveit.jsonld` (13 nodes: investigation, examiner,
tool, device, image container + bitstream, hash result, the acquisition
action typed with DFT-1002, weakness evaluation + set, the restated
DFT-1002 catalogue entry, and a `uco-action:Action` typed with DFT-1042)
and validates it with `extensions=["solveit"]`.

## Related

- [technique-evidence-outcome.md](technique-evidence-outcome.md) — join sourced techniques to hashed evidence and legal outcomes
- [starter-tool-run.md](starter-tool-run.md)
- [forensic-lifecycle.md](forensic-lifecycle.md)
