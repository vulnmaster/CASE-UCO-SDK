# Ten-document CaseLinker remodel corpus

Test of the hypothesis that a CaseLinker administrator using the
**current SDK** (v1.27.0 factories, `validate_graph`, source-faithful
recipes) can remodel live named graphs from original press releases and
then **replace** those graphs.

This is not an automatic press-release-to-graph extractor. The SDK
encodes sourced facts the administrator (or an agent following the
recipe) extracts. Routing tools may suggest CSAM-hash or CyberTip
families; those suggestions were **not** followed into invented hashes
or tips. ATT&CK was not applied: it is not CAC community language.
CAC **offenders** target children and other vulnerable people; ATT&CK
models **hackers** and **attackers**. A CAC graph gets an ATT&CK
mapping only if the source describes that rare overlap.

Remote CaseLinker counts below are untrusted external SPARQL results
from 2026-08-27.

## Sampling, not convenience

CaseLinker `dcterms:source` HTTP URLs were fetched until ten **single-
matter** press releases were in hand. Many live “sources” are not
remodelable as one `CACInvestigation`:

| CaseLinker graph | URL class | Why it was not remodeled |
|---|---|---|
| `ncmec_2025_499` | Rochester MN news item | **404** after a site redesign |
| `lapd_2017_004` | LAPD newsroom | **Access denied** |
| `ky_sp_2026_017` | KSP news | SAKI **grant announcement**, not a case |
| `la_ag_2026_026` | LA AG Article/421 | Orleans Metro ICAC **task-force launch**; 31,000 CyberTips are program stats |
| `la_ag_2026_036` | LA AG Article/398 | **Operation Access Denied** (67 arrests) |
| `ohio_ag_2021_003` | Ohio AG | **Operation 614** (53 victims referred, 93 arrests) |
| `ncmec_2022_231` | justice.gov | USAO-MD **community-outreach** page |
| `ncmec_2025_962` / `doj_ceos_2025_022` | DOJ OPA | **Operation Restore Justice** aggregate |

A full-corpus run will hit the same classes: dead links, operations,
program stats, and generic agency pages. Those graphs cannot be
replaced from “the source URL” without a different source or a split
into per-defendant investigations.

## Live CaseLinker vs remodeled graph

| Graph | CL tips | Remodel tips | CL sentences | Remodel imposed sentences | CL victims | Remodel victims |
|---|---:|---:|---:|---:|---:|---|
| `ncmec_2025_356` | 2 | 1 | 3 | 2 (+ restitution) | 1 | omitted |
| `illinois_ag_2025_001` | 2 | 0 | 1 | 0 (potential only) | 45 | omitted |
| `usss_2022_005` | 0 | 0 | 11 | 3 (+ restitution) | 1 | omitted |
| `illinois_ag_2025_023` | 2 | 0 | 1 | 1 | 45 | omitted |
| `usss_2017_007` | 0 | 0 | 9 | 0 (potential only) | 1 | reported 2 |
| `ncmec_2024_754` | 0 | 0 | 4 | 0 (plea; sentencing not reported) | 1 | reported 5 |
| `ncmec_2023_609` | 2 | 1 | 5 | 2 (+ restitution) | 1 | reported 1 |
| `ncmec_2025_619` | 1 | 1 | 2 | 0 (complaint) | 1 | omitted |
| `ncmec_2023_324` | 0 | 0 | 1 | 0 (complaint) | 1 | reported 1 |
| `doj_ceos_2026_013` | 0 | 0 | 2 | 2 | 1 | reported 1 |

Patterns that will dominate a 7,426-graph remodel:

1. **Illinois ICAC template inflation.** Charging and sentencing releases
   reuse the same 2 CyberTips / 45 `VictimRole` program-stat block.
   Source-faithful remodel drops both.
2. **Potential penalty typed as `CriminalSentence`.** Charging and plea
   releases (Ridder 9, Walsh 2, Swain 4, Villmer 1) carry sentence nodes
   the source does not impose.
3. **Extra CyberTips.** Even when a tip is real (NDIA, MDNC), CaseLinker
   often stores two tip nodes. Remodel emits one.
4. **Victim under-count on federal production/plea releases.** Swain’s
   source states five minors; CaseLinker has one `VictimRole`. Remodel
   records `reportedVictimCount` 5 and does not invent named identities.
5. **Statute scarcity.** 1 of 10 press releases cites offense sections.
   Assessment statutes (§ 3014 / § 2259A) and a PACER judgment for
   Hounsell were **not** imported into the press-release graph.
6. **The prosecutor target join stays empty.**
   `legalproc:FederalCharge` + imposed `Sentence` + `appliesTo` needs a
   statute **and** an imposed term in the **same** source. Sentencing
   releases omit the section; charging releases omit the term.

## Target-shape answerability after replace

If the administrator **replaces** (does not merge) each named graph:

| Question | Better | Worse / empty | Unchanged empty |
|---|---|---|---|
| `InvestigationTrigger` | 3 graphs gain it | Illinois / extra-tip joins disappear | — |
| Tip as `hasStep` | — | Program-stat tips gone | — |
| Imposed vs potential | 5 graphs have typed imposed terms; charging graphs lose fake sentences | Label-only `CriminalSentence` queries | — |
| `legalproc:FederalCharge` | Ridder only | — | 9 graphs still have no statute |
| `FederalCharge` + `appliesTo` + imposed `Sentence` | — | — | **0 / 10** (needs PACER or a sentencing release that cites the section) |
| Hashed series / PhotoDNA | — | Type-only facets gone | Still 0 without a lab source |
| Phase end / Brady | — | — | Still 0 |
| `admissionTheme` / `chargeCluster` | — | **Empty** (private vocab dropped) | — |

Merge-load would keep the old inflated tips, victims, and sentences
alongside the remodeled nodes. Replace is required.

## What “using the current SDK” means at corpus scale

- **Per document:** fetch URL → confirm it is this matter → extract
  fail-closed facts → `CASEGraph` factories / `caselinker_icac_remodel`
  helpers → `validate_graph` (`cac` + `legalproc`) → CaseLinker Graph
  Store replace. The SDK query client stays read-only.
- **Throughput:** this n=10 set is agent-assisted extraction, not a
  batch NLP job. The bottleneck is source triage (dead links,
  operations, program stats) and statute/victim/tip refusal decisions,
  not `graph.write()`.
- **Yield on v1.27.0 target joins:** expect frequent `InvestigationTrigger`
  and imposed-`Sentence` gains; expect rare `legalproc` typed charges;
  expect the hashed-series, phase-end, and disclosure questions to stay
  empty until lab, docket, or discovery sources are added.
- **Do not** follow `route_cac_content` / `route_investigation_content`
  into invented PhotoDNA, a CyberTip that the release only mentions as
  task-force background, or MITRE ATT&CK. ATT&CK is attacker/hacker
  tradecraft, not the vocabulary for a CAC offender.

Re-run:

```bash
PYTHONPATH=python:mcp_server python3 examples/caselinker-icac-remodel/pilot/build_pilot.py
PATH=.venv/bin:$PATH PYTHONPATH=python:mcp_server python3 mcp_server/tools/run_recipe_examples.py --validate \
  --id cl-pilot-ncmec-2025-356 \
  --id cl-pilot-illinois-ag-2025-001 \
  --id cl-pilot-usss-2017-007 \
  --id cl-pilot-ncmec-2023-609 \
  --id cl-pilot-illinois-ag-2025-023
```
