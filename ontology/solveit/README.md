# SOLVE-IT Extension (bundled)

Pinned, sync-managed snapshot of [SOLVE-IT](https://solveit-df.org) — the
Systematic Objective-based Listing of Various Established digital
Investigation Techniques — comprising the upstream
[solve-it-ontology](https://github.com/SOLVE-IT-DF/solve-it-ontology)
CASE/UCO extension ontology and the compiled RDF knowledge base from
[SOLVE-IT-DF/solve-it](https://github.com/SOLVE-IT-DF/solve-it) (MIT
licensed). Exact pinned versions are recorded in the `provenance` block of
`manifest.json`.

SOLVE-IT organizes digital forensic practice as **objectives** (what the
investigation needs to achieve) → **techniques** (how to achieve it) →
**weaknesses** (what can go wrong, classified per ASTM E3016-18) →
**mitigations** (what reduces the risk), enabling systematic Error
Mitigation Analysis alongside CASE/UCO evidence modeling.

## Contents

| File | Role |
| --- | --- |
| `solve_it_core.ttl` | Objective/Technique/Weakness/Mitigation classes, `SolveitInvestigativeAction` (subclass of `case-investigation:InvestigativeAction`) with `usedTechnique`/`appliedMitigation` |
| `solve_it_observable*.ttl` (4 files) | ~60 forensic observable classes (image containers, bitstreams, timelines, keyword search artifacts, acquisition records, ...) |
| `solve_it_observable_shapes.ttl` | SHACL shapes constraining the observables |
| `solve_it_analysis.ttl` | Hypothesis/analysis classes (subclasses of `uco-analysis` types) |
| `solve_it_sqlite.ttl` | SQLite internals observables |
| `solve_it_tool_profile.ttl` | Tool capability profiles |
| `solve_it_weakness_assessment.ttl` | `WeaknessEvaluation`/`WeaknessEvaluationSet` risk-rating classes |
| `solve-it-kb.ttl` | Compiled knowledge base: 23 objectives, 191 techniques, 339 weaknesses, 270 mitigations, cross-linked with CASE/UCO input/output classes |
| `solveit-technique-catalog.ttl` | **Generated** — every technique punned as `owl:Class` typed `uco-action:Technique` (UCO 1.5.0 metaclass pattern, ucoProject/UCO PR #676); regenerate with `make sync-solveit-offline` |
| `solveit-local-anchors.ttl` | SDK-local bridge anchoring three upstream enumeration classes to `owl:Thing` |
| `solveit-exemplar.ttl` | Validated exemplar (disk imaging with mitigations + weakness evaluation) |
| `solveit-invalid-exemplar.ttl` | Expected-invalid fixture proving the shapes constrain |
| `queries/*.sparql` | Competency queries run by the lifecycle gates |

## Two modeling styles

**Native SOLVE-IT style (works today, UCO 1.4.0):** record each executed
step as a `solveit-core:SolveitInvestigativeAction` linking the canonical
knowledge-base individuals:

```turtle
<urn:uuid:...> a solveit-core:SolveitInvestigativeAction ;
    uco-core:name "acquire-laptop-image" ;
    solveit-core:usedTechnique solveit-data:techniqueDFT-1002 ;
    solveit-core:appliedMitigation solveit-data:mitigationDFM-1004 ;
    uco-action:performer <urn:uuid:...> ;
    uco-action:result <urn:uuid:...> .
```

**UCO 1.5.0 metaclass style (forward-implemented):** type the action
directly with the punned technique class from
`solveit-technique-catalog.ttl`, exactly like a MITRE ATT&CK technique
(see `extensions/attack-technique/`):

```turtle
<urn:uuid:...> a uco-action:Action , solveit-data:techniqueDFT-1042 ;
    uco-core:name "verify-image-hash" .
```

Both styles share the same IRIs (the catalog puns the knowledge-base
individuals), coexist in one graph, and validate together. The manifest
declares `depends_on: ["attack-technique"]` so the `uco-action:Technique`
metaclass is always in scope.

## Usage

```bash
# validate a graph that uses SOLVE-IT terms (KB individuals included)
# via the MCP tool: validate_graph(path, extensions=["solveit"])

# query the knowledge base via MCP
#   search_solveit("disk imaging")
#   get_solveit_details("DFT-1002")
#   plan_solveit_workflow("image the seized laptop and verify integrity")

# load the class registry into discovery tools
CASE_UCO_EXTENSIONS=solveit  # search_classes(scope="solveit")
```

Recipe: `docs/recipes/solve-it-investigation-planning.md`.

## Keeping pace with upstream

Upstream releases monthly (knowledge base) and continuously (ontology).
Refresh the snapshot with:

```bash
make sync-solveit             # pin current upstream main
make sync-solveit REF=<sha>   # pin a specific solve-it-ontology commit
```

The sync tool re-vendors every file, regenerates the punned technique
catalog, and rewrites manifest provenance. A weekly GitHub Actions check
(`.github/workflows/upstream-freshness.yml`) fails when the pinned snapshot
falls behind the newest upstream release.

There is intentionally no `validation-subset.json`: subset mode skips RDFS
inference, which SOLVE-IT needs so core CASE/UCO shapes apply to its
subclasses. Plain `extensions=["solveit"]` therefore loads the full
manifest (ontology + shapes + catalog + knowledge base).
