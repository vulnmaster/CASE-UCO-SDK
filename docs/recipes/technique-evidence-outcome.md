# Technique, Evidence, and Legal-Outcome Join

> See [Recipe Index](INDEX.md) for all recipes.

Join **examiner method** (SOLVE-IT), **digital evidence** (observables with
real hashes), and **legal outcomes** (`legalproc`) so questions such as
“which techniques appear in imposed-sentence graphs?” are SPARQL-answerable.
Model only what the source establishes. Press releases almost never name a
forensic technique; lab exports and some PACER affidavits do.

Validated against `examples/technique-evidence-outcome/` (synthetic lab
hash-match CSV + UFED-style summary, and a PACER method-claim graph).

## When to use this recipe

- A lab, RMS, or examiner report names a tool run, hash match, or extraction
- A PACER affidavit or expert report names a product or method
- You need to keep one matter identity across a press release, PACER docket,
  and later lab graph
- You are answering effectiveness questions that require `usedTechnique`
  plus `legalproc:Sentence`

Use [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) for
press-release legal stages. Use
[solve-it-investigation-planning.md](solve-it-investigation-planning.md) for
technique selection and error mitigation. Use
[cyber-threat-intelligence.md](cyber-threat-intelligence.md) for **hacker /
attacker** ATT&CK techniques on CTI reports — do not put ATT&CK IRIs on
`solveit-core:usedTechnique`, and do not use ATT&CK as the vocabulary for
a crimes-against-children offender.

## Source-fidelity table

| Source | Record | Do not record |
|---|---|---|
| Press release | Named evidence types (`CSAMIncident`, CyberTip, statement), `legalproc` charges/outcomes, source publication vs retrieval time | `usedTechnique`, empty `ContentDataFacet`, invented tool versions |
| PACER affidavit / trial brief / expert report | Named `uco-tool:Tool` + `case-investigation:InvestigativeAction` when the filing names the method; `ProvenanceRecord` to the PACER page | A DFT-* IRI the filing does not support |
| Lab / PD export (UFED summary, hash-match CSV, FTK/Autopsy log) | `solveit-core:SolveitInvestigativeAction` + `usedTechnique` + versioned `instrument` + `object`/`result` + `ContentDataFacet` with `hash` | Placeholder facets; auto-asserted DFT-* from product name alone |
| CTI / ATT&CK report | Hacker / attacker behavior as `uco-action:Action` typed with the `attack-technique` catalog | SOLVE-IT examiner techniques; CAC offender conduct (grooming, CSAM, sextortion); LE product runs the report does not describe |

Suggested DFT-* IDs for common LE products live in
[`examples/technique-evidence-outcome/le_tool_solveit_profiles.json`](../../examples/technique-evidence-outcome/le_tool_solveit_profiles.json).
Those rows are **capability hints**. Call
`suggest_techniques_for_product(name)` to review candidates; write
`usedTechnique` only when the source establishes the technique.

## Classes and properties

| Term | Role |
|---|---|
| `case-investigation:Investigation` | Matter container; reuse `legalproc:caseIdentifier` across sources |
| `solveit-core:SolveitInvestigativeAction` | Lab execution that records method |
| `solveit-core:usedTechnique` | SOLVE-IT DFT-* individual actually performed |
| `case-investigation:InvestigativeAction` | PACER method claim when no DFT-* is sourced |
| `uco-tool:Tool` | Versioned product (`instrument`) |
| `uco-observable:ObservableObject` + `FileFacet` + `ContentDataFacet` | Evidence; `hash` is required when this facet is used |
| `uco-types:Hash` | `hashMethod` + `hashValue` |
| `legalproc:FederalCharge` / `StateCharge` | Charge the evidence supports |
| `legalproc:Sentence` | Imposed outcome (`sentenceStatus` `imposed`, `outcomeScope` `current-case`) |
| `uco-core:Relationship` (`Related_To`) | Action/evidence ↔ charge; investigation ↔ charge |
| `case-investigation:ProvenanceRecord` | Exhibit grouping for lab outputs |

## Canonical pattern

```
Investigation (legalproc:caseIdentifier)
  ├── Related_To ──▶ FederalCharge / StateCharge
  ├── SolveitInvestigativeAction
  │     ├── solveit-core:usedTechnique ──▶ DFT-1050 / DFT-1020 / …
  │     ├── uco-action:instrument ──▶ Tool
  │     ├── uco-action:object / result ──▶ ObservableObject + Hash
  │     └── Related_To ──▶ charge
  └── legalproc:Sentence (imposed, current-case)
        └── legalproc:concernsCharge ──▶ charge
```

## Bounded lab importer

```python
from tools.technique_evidence_outcome import (
    import_hashmatch_csv,
    import_ufed_summary,
    suggest_techniques_for_product,
    build_lab_join,
)

suggest_techniques_for_product("Cellebrite UFED")  # hints only
graph = build_lab_join()
```

The builder reads `hashmatch.csv` and `ufed_summary.json`. It does not parse
native Cellebrite, Magnet, or FTK export formats.

## Anti-patterns

- Minting `solveit-core:usedTechnique` because a press release mentioned a
  CyberTip or “digital evidence”
- Attaching `ContentDataFacet()` with no `hash`, size, MIME type, or payload
- Collapsing ATT&CK attacker techniques into SOLVE-IT examiner techniques
- Treating a CAC offender (someone who targets children or other
  vulnerable people) as an ATT&CK attacker unless the source describes
  that rare overlap
- Auto-asserting DFT-* from `le_tool_solveit_profiles.json` without a sourced
  method claim
- Creating a second investigation IRI for the lab report of the same docket

## Checklist

1. Classify the source with the fidelity table before creating method nodes.
2. Reuse `legalproc:caseIdentifier` and the investigation IRI for the matter.
3. If the source is a lab export, record `usedTechnique` and real hashes.
4. If the source is PACER, record a named tool only when the filing names it.
5. If the source is a press release, stop at legal outcomes and named evidence.
6. Validate with `validate_graph(..., extensions=["solveit", "legalproc"])`.

## Related

- [solve-it-investigation-planning.md](solve-it-investigation-planning.md)
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md)
- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md)
- [starter-tool-run.md](starter-tool-run.md)
- [cyber-threat-intelligence.md](cyber-threat-intelligence.md)
