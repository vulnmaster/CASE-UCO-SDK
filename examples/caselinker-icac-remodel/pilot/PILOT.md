# CaseLinker source-document remodel pilot

Ten CaseLinker named graphs remodeled from their **original public press
releases**, not from the live RDF. Sources are untrusted evidence. The
builder is `build_pilot.py`. How a full-corpus remodel would perform is
in [CORPUS.md](CORPUS.md).

All ten graphs validate (`conforms=True`, `extensions=['cac','legalproc']`)
as of 2026-08-27.

| CaseLinker graph | Source | Remodel |
|---|---|---|
| `ncmec_2025_356` | [USAO NDIA, 2025-05-21](https://www.justice.gov/usao-ndia/pr/mapleton-iowa-man-who-possessed-child-pornography-sentenced-federal-prison) | `ncmec_2025_356.jsonld` |
| `illinois_ag_2025_001` | [Illinois AG, 2025-12-09](https://illinoisattorneygeneral.gov/news/story/attorney-general-raoul-charges-macoupin-county-man-for-disseminating-child-sexual-abuse-material) | `illinois_ag_2025_001.jsonld` |
| `usss_2022_005` | [USSS / USAO CDIL, 2022-03-25](https://www.secretservice.gov/newsroom/releases/2022/03/east-peoria-man-sentenced-151-months-prison-possession-child-sexual-abuse) | `usss_2022_005.jsonld` |
| `illinois_ag_2025_023` | [Illinois AG, 2025-06-04](https://illinoisattorneygeneral.gov/news/story/attorney-general-raoul-obtains-10-year-prison-sentence-for-greene-county-man-who-possessed-child-sexual-abuse-material) | `illinois_ag_2025_023.jsonld` |
| `usss_2017_007` | [USSS / USAO NDCA, 2017-05-25](https://www.secretservice.gov/press/releases/2017/05/mountain-view-resident-charged-production-child-pornography-and) | `usss_2017_007.jsonld` |
| `ncmec_2024_754` | [USAO WDNY, 2024-08-02](https://www.justice.gov/usao-wdny/pr/tonawanda-man-pleads-guilty-production-child-pornography-0) | `ncmec_2024_754.jsonld` |
| `ncmec_2023_609` | [USAO MDNC, 2023-11-28](https://www.justice.gov/usao-mdnc/pr/davie-county-man-sentenced-50-years-production-and-distribution-child-pornography) | `ncmec_2023_609.jsonld` |
| `ncmec_2025_619` | [USAO WDNY, 2025-03-10](https://www.justice.gov/usao-wdny/pr/rochester-man-charged-receipt-and-possession-child-pornography) | `ncmec_2025_619.jsonld` |
| `ncmec_2023_324` | [USAO SDIL, 2023-08-21](https://www.justice.gov/usao-sdil/pr/first-grade-teacher-charged-solicitation-child-sexual-abuse-material) | `ncmec_2023_324.jsonld` |
| `doj_ceos_2026_013` | [DOJ OPA, 2026-05-14](https://www.justice.gov/opa/pr/wisconsin-man-sentenced-13-years-prison-using-internet-sexually-exploit-minor-philippines) | `doj_ceos_2026_013.jsonld` |

## What the sources support

**NDIA 24-CR-4047.** Kik reported an account to NCMEC; a CyberTip was
assigned to Iowa ICAC. Federal guilty plea (2025-01-06) and imposed
60-month prison term plus 5-year supervised release and $10,100
restitution (2025-05-20). Search warrant executed. No statute section,
hash, PhotoDNA, phase-end time, or disclosure citation.

**Macoupin County charging.** Two Class X dissemination counts, each
punishable by up to 30 years. Search and arrest with Virden PD. Illinois
ICAC is named as the AG task force. The CyberTip paragraph is **program
background**, not a tip assigned to this defendant. No imposed sentence,
statute section, warrant, hash, or identified victims.

**East Peoria sentence.** Imposed 151 months plus life supervised release,
$23,000 restitution, and a concurrent 24-month supervised-release
violation term. Assessment statutes (18 U.S.C. § 3014 / § 2259A) are not
the possession count. No CyberTip. Prior 2007/2008 convictions are
history, not current `legalproc` charges.

**Greene County sentence.** Imposed 10 years after a guilty plea to two
Class 2 possession counts. Illinois ICAC CyberTip and 45-victim figures
are program background. No ILCS section.

**NDCA Ridder indictment.** The only press release in this set that cites
offense statutes. Five `legalproc:FederalCharge` groups, two reported
victims (count only), potential penalties, no imposed sentence, no
CyberTip.

**WDNY Swain plea.** Guilty plea to production; five reported victims;
15–30 year statutory range; sentencing date not yet an imposed term. No
CyberTip, no statute.

**MDNC Smith sentence.** One sourced CyberTip (September 2021). Imposed
600 months plus 20 years supervised release and $96,200 restitution plus
assessments. One reported victim. No statute. CaseLinker has two tips.

**WDNY Walsh complaint.** Google report to NCMEC is a sourced CyberTip.
Receipt and possession by complaint; released on conditions (kind not
sourced). No statute, no imposed sentence.

**SDIL Villmer complaint.** Unrelated Carmi PD investigation, not a
CyberTip. One reported victim. Up to 20 years if convicted. No statute.

**EDWI Hounsell sentence.** Imposed 13 years plus 7 years supervised
release. One reported victim in the Philippines. This press release does
not cite 18 U.S.C. § 2422(b). A PACER judgment elsewhere in the repo is
not used.

## Compared with the live CaseLinker graphs

| Fact | CaseLinker today | Pilot remodel |
|---|---|---|
| Tip → investigation | Tip as `hasStep`; `usesMethod` `…/tech/cybertipline` | `InvestigationTrigger` only when **this** source assigns a tip (3 of 10) |
| Extra / program CyberTips | Illinois graphs: 2 tips; NDIA: 2; MDNC: 2 | Extra tips **refused** |
| Illinois victims | 45 `VictimRole` nodes | `victimFactStatus` `omitted` |
| Charging releases typed as sentences | Ridder 9, Walsh 2, Swain 4, Villmer 1 | `PotentialPenalty` only |
| File hashes | Type-only `ContentDataFacet` on incidents | Dropped. Press-release **text** is hashed as provenance |
| `legalproc` charge class | 0 | 1 of 10 (Ridder). SHACL requires `statuteCitation` |
| Phase end / ArrestOperation / Brady | Absent | Still absent |
| `caselinker:` vocab | Present | Refused |

## Target-shape questions on the remodeled graphs

| Question | Count of 10 |
|---|---|
| `InvestigationTrigger` | 3 (NDIA, MDNC Smith, Walsh) |
| Hashed series / PhotoDNA tag | 0 |
| `legalproc:FederalCharge` | 1 (Ridder). None also have an imposed sentence |
| `FederalCharge` + imposed `Sentence` `appliesTo` | 0 |
| Phase begin **and** end | 0 (begin only) |
| Jencks / Brady | 0 |
| Imposed `legalproc:Sentence` | 5 |
| `PotentialPenalty` without an imposed term | 5 |

Re-run:

```bash
PYTHONPATH=python:mcp_server python3 examples/caselinker-icac-remodel/pilot/build_pilot.py
```
