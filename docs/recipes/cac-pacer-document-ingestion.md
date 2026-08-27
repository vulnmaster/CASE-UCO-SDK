# PACER Document Ingestion and CAC Modeling

> See [Recipe Index](INDEX.md) for all recipes.

End-to-end workflow for agents (and Link-Look/Hermes callers) that receive **PACER PDF bundles** — indictments, trial briefs, judgments, complaints — and must return **validated CASE/UCO/CAC JSON-LD**.

This recipe composes:

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — defendant–counts, indictment–charges
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md) — trial briefs, docket milestones
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) — § 1591 solo-operator cases
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — post-trial judgment (AO 245B)

Reference exemplar: [`examples/pacer/anchorage_pd_2022_004/`](../../examples/pacer/anchorage_pd_2022_004/).

## When to use this recipe

Use when the user submits one or more local PDFs whose names or content indicate:

- PACER / ECF docket exports (`Case 3:20-cr-… Document N Filed …`)
- Federal indictments or criminal complaints with numbered counts
- Government trial briefs with anticipated evidence
- AO 245B judgments or sentencing orders
- ICAC-related federal prosecutions (§ 2251, § 2252A, § 1591, etc.)

## Agent workflow (MCP)

```
1. process_document_file(source_path, output_path)     # per PDF
2. route_cac_content(content_text=..., source_path=...)  # recipe routing
3. Build merged CAC graph (agent layer — not automatic)
4. validate_graph(graph_path, extensions=["cac"])
5. Return graph path + safe_summary to caller
```

### Step 1 — Document normalization

Call `process_document_file` once per PDF. The tool:

- Extracts text (pdftotext → pypdf → OCR ladder)
- Writes CASE/UCO JSON-LD with source `ObservableObject`, hashes, and `InvestigativeAction` provenance
- Emits `extracted-content.json` and `annotations.jsonld` beside the graph
- Maps high-confidence spans to core UCO types (Person, Organization, Location, ApplicationAccount, Event, statute references)

**Honest failures:** `pdf_text_missing`, `source_missing`, `source_oversized` — do not fabricate content.

```python
# WSL paths for Windows OneDrive uploads
source = "/mnt/c/Users/.../pacer -- case_id -- indictment.pdf"
output = "output/icac_pacer/case_id/indictment.jsonld"
process_document_file(source_path=source, output_path=output)
```

### Step 2 — CAC recipe routing

Pass extracted narrative (or the normalized graph path) to `route_cac_content`:

```python
route_cac_content(
    content_text="Case 3:20-cr-00029 … Count 1 production … Minor Victim 1 …",
    source_path="output/icac_pacer/case_id/indictment.jsonld",
    output_format="jsonld",
)
```

Review `matched_domains`, `modeling_checklist`, and `recommended_workflow` in the response. The MCP tool returns **guidance only** — the agent must build the CAC layer.

### Step 3 — Build the CAC investigation graph

The document processor produces **Layer 1** (source artifacts + extracted entities). Agents add **Layer 2–3** CAC nodes:

| Source document | Typical CAC nodes |
|---|---|
| Indictment | `MultiDefendantIndictment`, `FederalCharge`, `AssetForfeitureAction`, `MinorTraffickingVictimRole` |
| Trial brief | `TrialPhase`, anticipated `CSAMIncident`, platform accounts, `InvestigativeAction` (brief filing) |
| Judgment (AO 245B) | `SentencingPhase`, `ConvictionRecord`, `legalproc:Sentence` (`sentenceKind`, `outcomeScope`), `legalproc:Plea` / `legalproc:PleaAgreement` when a plea is recorded. Do not type restitution, forfeiture, or special assessments as `legalproc:Sentence`. |

**Merge rule:** One `CACInvestigation` per federal docket (`3:20-cr-00029-SLG-MMS`), not one graph per PDF. Link each source PDF as `uco-core:object` on the investigation and attach `ProvenanceRecord`. Keep PACER filing time, retrieval time (`legalproc:sourceRetrievalTime`), and graph `uco-core:objectCreatedTime` as separate timestamps. See [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md).

### Step 4 — Validate before returning

```bash
validate_graph("moore-dalaska-2020-icac.jsonld", extensions=["cac", "legalproc"])
```

Or:

```bash
python3 examples/pacer/<case>/build_<case>.py   # includes validation in __main__
```

Do not report success until `conforms: true`.

## PACER filename convention

Bundled ICAC/PACER drops often use:

```text
pacer -- <local_case_ref> -- <document_type>.pdf
```

Example: `pacer -- anchorage_pd_2022_004 -- indictment.pdf`

Use `<local_case_ref>` as a folder slug under `output/icac_pacer/` and in graph descriptions; use the **ECF case number** from the PDF (`3:20-cr-00029-SLG-MMS`) as `cacontology:caseNumber`.

## Fact-file template (multi-document bundle)

```text
CASE_ID: 3:20-cr-00029-SLG-MMS
LOCAL_REF: anchorage_pd_2022_004
COURT: U.S. District Court, District of Alaska
DEFENDANT: Moore, Jayshon (aka China)
USM: 15966-006

DOCUMENTS:
  indictment: Doc 2 — filed 2020-02-21 — counts 1-3 + forfeiture
  trial_brief: Doc 172 — filed 2022-03-28 — trial 2022-04-04
  judgment: Doc 251 — filed 2022-09-20 — guilty counts 1-3, 240mo concurrent

DEFENDANT_COUNTS:
  Moore: 1,2,3

VICTIM_COUNTS:
  Minor Victim 1: 3
  V.P. (trial brief): production/possession conduct for counts 1-2 (ALLEGED)

PLATFORMS:
  Snapchat jayinglez80 (defendant)
  Snapchat V.P. account (victim)
```

## Relationship checklist (PACER bundle)

| # | Edge | When |
|---|---|---|
| P1 | Investigation → each source PDF | Always (`uco-core:object`) |
| P2 | ProvenanceRecord → source PDFs | Always (`wasInformedBy`) |
| P3 | FederalProsecution → indictment | Charging doc processed |
| P4 | Indictment → each FederalCharge | Counts extracted |
| P5 | Defendant → chargedWith → counts | Always |
| P6 | Charge → conduct (`CSAMIncident`, `CommercialSexualExploitation`) | Brief/indictment allege conduct |
| P7 | Trial brief → charges + conduct | Trial brief processed |
| P8 | Judgment → Conviction + PrisonSentence | Post-trial judgment |
| P9 | CSAMIncident → hasFacet artifact | CAC SHACL requires digital artifact facet |

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Stop after `process_document_file` | Document normalize is Layer 1 only; build CAC graph and validate |
| Three disconnected graphs (one per PDF) | Single `CACInvestigation` per docket with linked source observables |
| Defendant/charges only in ExtractedStringsFacet | Add typed `Person`, `FederalCharge`, `Relationship` nodes |
| Trial brief facts in Bundle description only | Per-victim conduct nodes + charge links |
| `derivedFrom` on ProvenanceRecord | Use `case-investigation:wasInformedBy` |
| CSAMIncident without `hasFacet` | Add `ContentDataFacet` summary (non-graphic) for SHACL |
| Aggregated CSAM only, no queryable series | Add per-series `ObservableObject` nodes with capture dates linked via registered `Related_To` to the parent incident |
| Pre-trial allegations without status | Tag with `assertion:ALLEGED`; adjudicated nodes with `assertion:ADJUDICATED` |
| Judgment supervision as prose only | Model each special condition as a structured `ObservableObject` linked from `SupervisedRelease` with registered `Related_To` and a descriptive relationship note |
| Duplicate facet `@id` across nodes | Give each `hasFacet` a unique `@id` (one facet per object) |
| Fabricated timestamps | Never invent a day or clock time the filing does not state. "June 2019" or "January and February 2020" → record the period in the description or an `approximatePeriod=` facet string, not an `xsd:dateTime` |
| `uco-action:startTime` on non-Actions | `uco-action:*` properties belong on `Action` subclasses (`InvestigativeAction`, `CSAMIncident`). Events, legal phases, and media observables use `uco-core:startTime` (media capture dates encoded as local midnight for date-only precision) |
| Invented class/property names | Use only terms declared in the CAC TTLs: charge subtypes come from `cacontology-usa-federal` (`ChildPornographyProduction`, `SexTraffickingOfMinors`), forfeiture from `cacontology-asset-forfeiture:AssetForfeitureAction` + `relatedCriminalCharges`, verdicts as `cacontology-legal-outcomes:ConvictionRecord` with `convictionDate`, `convictionType` (`jury_verdict`), `chargeCount` |
| Invented SOLVE-IT technique | If the filing names Cellebrite, FTK, PhotoDNA, or a hash match, record a versioned `uco-tool:Tool` and `InvestigativeAction`. Do not mint `solveit-core:usedTechnique` unless the filing identifies that method. See [technique-evidence-outcome.md](technique-evidence-outcome.md) |
| Defendant as interview performer | Law enforcement performs the interview; the defendant is `uco-action:object` on the `InvestigativeAction` |
| Possession media wired into production incident | Count 2 items received on the defendant's account link `Related_To` → possession incident only; if an item is a documented copy of a production series, add registered `Copied_From` → that series |

## Granular trial-brief modeling (Moore exemplar)

Reference: [`examples/pacer/anchorage_pd_2022_004/build_moore_dalaska_2020_case.py`](../../examples/pacer/anchorage_pd_2022_004/build_moore_dalaska_2020_case.py)

When a government trial brief lists specific video/photo series, coercion methods, and corroborating social posts:

1. Keep one aggregate `CSAMIncident` / `CommercialSexualExploitation` per conduct type.
2. Add child `ObservableObject` nodes per dated media series; link `Related_To` → aggregate incident. Set `uco-core:startTime` only for dates the brief states (local midnight = date-only precision); production series also get `Created` edges from the defendant.
3. Model coercion as `uco-core:Event` nodes with `eventType` including `coercion method`; link to trafficking incident. Most coercion acts are undated in trial briefs — say "Undated in source" in the description instead of inventing dates; use `approximatePeriod=` facet strings when the brief anchors a rough period.
4. Model corroborating Snapchat posts as evidence observables; link them to the related coercion event with registered `Related_To` and describe the corroboration basis.
5. Unify victim identifiers (`Minor Victim 1` + trial brief alias `V.P.`) on one `MinorTraffickingVictimRole` node.
6. Add `InvestigativeAction` for search warrants and LE interviews with page-anchored descriptions (`Source: PACER Doc N, page X`). The defendant is the interview's `uco-action:object`, never its performer.
7. From AO 245B judgment: model `SupervisedRelease`, each special condition, restitution, assessment, and payment schedule separately. Record the jury verdict as `ConvictionRecord` (`convictionType=jury_verdict`, `convictionDate`, `chargeCount`) with registered `Related_To` edges to each count and a description stating that the conviction is on that count.

## Python skeleton

See [`examples/pacer/anchorage_pd_2022_004/build_moore_dalaska_2020_case.py`](../../examples/pacer/anchorage_pd_2022_004/build_moore_dalaska_2020_case.py).

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md)
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md)
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md)
- [forensic-lifecycle.md](forensic-lifecycle.md)
- [technique-evidence-outcome.md](technique-evidence-outcome.md)
