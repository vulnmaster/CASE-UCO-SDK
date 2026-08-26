# Legal Process Modeling (Charges, Verdicts, Sentences — Any Investigation Type)

Model the procedural skeleton of a criminal prosecution — charging
instruments, charges (including conspiracy, attempt, and predicate-linked
counts), pleas, trial proceedings, verdicts, sentences, forfeiture,
restitution, and appeals — for **any** investigation domain using the
`legalproc` extension.

**When to use this recipe**

- PACER/court-filing bundles for non-CAC cases (violent crime, terrorism,
  fraud, firearms, public corruption, ...)
- Conspiracy or attempt charges that need object/predicate offense links
- Multi-defendant cases with different counts, dispositions, and sentences
- Verdicts, mid-trial pleas, dismissals, acquittals, count mergers, appeals

For CAC-domain prosecutions, prefer the CAC legal-outcomes classes
(`docs/recipes/cac-legal-sentencing-outcomes.md`); this recipe covers the
general case. Document ingestion mechanics (hashes, OCR, fabrication-free
dates) are in `docs/recipes/cac-pacer-document-ingestion.md` and apply
unchanged.

## The extension

`extensions/legalproc/` implements the criminal-process stub concepts
proposed upstream in [CASE #192](https://github.com/casework/CASE/issues/192)
(plus `caseIdentifier` from [CASE #191](https://github.com/casework/CASE/issues/191)):

| Class | Purpose |
|---|---|
| `legalproc:ChargingInstrument` | complaint, indictment, superseding indictment, information (`instrumentType`) |
| `legalproc:CriminalCharge` | one count or count-range (`statuteCitation`, `countNumber`, `countLabel`, `chargeClassification`, `chargeDisposition`) |
| `legalproc:Plea` | `pleaType`: guilty / not-guilty / nolo-contendere |
| `legalproc:CriminalProceeding` | arraignment, trial, plea-hearing, sentencing-hearing, appeal, certiorari (`proceedingType`) |
| `legalproc:Verdict` | `verdictType`: guilty / not-guilty, per charge |
| `legalproc:Sentence` | `sentenceStatus`: recommended / imposed / vacated; `sentenceTerm` verbatim |
| `legalproc:ForfeitureOrder`, `legalproc:RestitutionOrder` | `monetaryAmount` + `currencyCode`; assets linked by Relationships |

`legalproc:concernsCharge` ties pleas, verdicts, sentences, forfeiture, and
restitution back to the charges they concern.

The extension's namespace is the one proposed to the CASE committee in
issue #192 (`https://ontology.caseontology.org/case/criminal/`); the
committee owns the final IRI. See `extensions/legalproc/README.md`.

Enable with `CASE_UCO_EXTENSIONS=legalproc` and validate with
`validate_graph(graph_path, extensions=["legalproc"])`.

## Cyber vs. non-cyber evidence: where UCO stops

Investigators work in and through cyberspace, but not everything in a case
file is a cyber artifact. Apply this rule:

- **Clearly cyber (fully or partially)** — messages, social-media posts,
  internet searches, files, devices, accounts: model as
  `uco-observable:ObservableObject` (or a subclass) with facets.
- **Never cyber** — firearms, body armor, vehicles, drugs, cash: model as
  `uco-core:UcoObject`, **not** as an observable. For **weapons and
  drugs**, use the dedicated extension classes (`weap:Handgun`,
  `weap:Ammunition`, `drug:ControlledSubstance`, ...) from
  `docs/recipes/weapons-drug-evidence.md` — their bridge files supply the
  CCO and gUFO grounding. For other physical items (vehicles, body armor,
  cash), dual-type with the matching upper-ontology class via a CDO
  alignment profile — e.g. `gufo:FunctionalComplex` for manufactured
  physical objects (CDO-Shapes-gufo; discover profiles with
  `get_uco_profiles("gufo")`). Strict concept coverage accepts profiled
  upper-ontology terms directly.

```json
{
  "@id": "kb:item-fbi-bearcat",
  "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
  "uco-core:name": "FBI 2016 Lenco Bearcat armored vehicle (VIN 1FDAF5HT7GEA85510)"
}
```

## Conspiracy, attempt, and § 924(c): `offenseForm` + `objectOffense`

Conspiracy is **not** a separate class — it is a `CriminalCharge` with a
form. Two properties capture every inchoate/derivative pattern:

```json
{
  "@id": "kb:charge-count1",
  "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
  "uco-core:name": "Count 1: Conspiracy to Murder a Federal Officer and Employee",
  "legalproc:statuteCitation": "18 U.S.C. §§ 1117 & 1114",
  "legalproc:offenseForm": "conspiracy"
}
```

```json
{
  "@id": "kb:charge-counts21-34",
  "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
  "uco-core:name": "Counts 21-34: Use of Firearm in Furtherance of Crime of Violence",
  "legalproc:statuteCitation": "18 U.S.C. §§ 924(c)(1)(A)(iii) & 2",
  "legalproc:offenseForm": "derivative",
  "legalproc:objectOffense": [
    {"@id": "kb:charge-counts4-10"},
    {"@id": "kb:charge-counts11-17"}
  ]
}
```

`offenseForm` open vocabulary: `substantive`, `conspiracy`, `attempt`,
`solicitation`, `aiding-abetting`, `derivative`. Omit `objectOffense` when
the object offense was never separately charged (common for conspiracy).

The conspiracy *organization* is a separate concern: model the group as
`uco-identity:Organization` and link reviewed members with registered
`Related_To` relationships whose descriptions state membership. Model overt
acts as `uco-action:Action`s plus UCO observables (messages, social posts,
internet searches). Keep the participation layer out of the charge nodes.

## Checklist (adapted from the Perry/O'Dell exemplar)

1. **One Investigation per docket**, with `legalproc:caseIdentifier` holding
   the docket number; magistrate/appellate dockets in the description.
2. **Instrument chain**: each complaint → indictment → superseding
   indictment as a `ChargingInstrument`, linked with registered `Related_To`
   and a supersession description; charges point at the operative instrument
   via `legalproc:assertedIn`.
3. **Defendant-charge matrix**: registered `Related_To` relationships per
   defendant with "charged with" in `uco-core:description` — defendants
   rarely share all counts (Perry: 1-41; O'Dell: 1-35, 42-45).
4. **Dispositions per charge**: `chargeDisposition` supports multiple values
   when counts diverge (Counts 36-37: `convicted-by-verdict` + `merged`).
5. **Victims as first-class nodes**: persons named by initials exactly as
   charged, linked by registered `Related_To` to charges and violent actions
   with the victim assertion in `uco-core:description`.
6. **Weapons/vehicles** as `uco-core:UcoObject` + `gufo:FunctionalComplex`
   items (never observables — see the cyber vs. non-cyber rule above) with
   serial numbers in names/descriptions. Use `uco-action:instrument` for use
   in an action; otherwise use described `Related_To` possession/subject
   assertions. Digital overt acts remain UCO observables.
7. **Overt-act timeline**: model the charging instrument's overt-act
   paragraphs as `uco-action:Action` nodes with one `uco-action:performer`,
   direct `uco-action:startTime`, `object`/`result` links to items, recruits,
   and observables, registered `Related_To` to the conspiracy charge with an
   overt-act description, and `uco-action:participant` for co-conspirators.
   This makes the graph timeline- and TTP-queryable for Link-Look exploration.
8. **Counsel**: attorneys as `uco-identity:Person` with registered
   `Related_To` links to represented people and appointment/termination
   history in descriptions.
9. **Verdicts per outcome**, not per trial: separate guilty and not-guilty
   `Verdict` nodes listing their charges via `concernsCharge`.
10. **Sentences**: keep `sentenceTerm` verbatim ("Life", "165 years (25
    concurrent + 140 consecutive)") — never convert to fabricated month
    counts; distinguish `recommended` vs `imposed`.
11. **Source fidelity**: every node description ends with a
   `Source: PACER Doc N (...)` reference; date-only facts rendered at local
   midnight with correct seasonal UTC offset.

## Validated exemplar

`examples/pacer/wdmo_2022_cr_04065/` — *U.S. v. Perry & O'Dell*,
No. 2:22-cr-04065-BCW (W.D. Mo.): 45 counts across two defendants,
conspiracy/attempt/derivative offense forms, fourteen § 924(c)
`objectOffense` links, mid-trial guilty plea, guilty and not-guilty
verdicts, count merger and dismissal, consecutive life sentences, terrorism
forfeiture, restitution, and appeal. Build and validate:

```bash
.venv/bin/python examples/pacer/wdmo_2022_cr_04065/build_perry_odell_wdmo_2022_militia.py
```

`examples/pacer/wdtn_2023_cr_20121/` — *U.S. v. Grayson et al.*,
No. 2:23-cr-20121-TLP (W.D. Tenn.): murder-for-hire (18 U.S.C. § 1958)
built from a docket report and press release only. Demonstrates
**per-defendant `CriminalCharge` nodes for one shared count** with
divergent outcomes (jury conviction vs. jury acquittal, matching how
PACER tracks counts per defendant), guilty and not-guilty `Verdict`
nodes, statutory-maximum sentence, and the **full appellate ladder** —
`proceedingType` `appeal` (Sixth Circuit affirmance) and `certiorari`
(Supreme Court review) chained with registered `Related_To` relationships
whose descriptions state which proceeding reviews which:

```bash
.venv/bin/python examples/pacer/wdtn_2023_cr_20121/build_grayson_wdtn_2023_murder_for_hire.py
```

## Related

- `docs/recipes/cac-pacer-document-ingestion.md` — document ingestion mechanics
- `docs/recipes/fraud-crypto-laundering.md` — financial-crime cases (cryptoinv + legalproc)
- `docs/recipes/racketeering-enterprise.md` — RICO / criminal-enterprise cases: the charged enterprise, member roles, and predicate statute categories (`rico` extension; worked 17-defendant multi-instrument exemplar)
- `docs/recipes/elder-fraud-impersonation.md` — impersonation call centers and money-courier schemes (worked plea/dismissal exemplar)
- `docs/recipes/insider-threat-trade-secrets.md` — trade secret theft and economic espionage (worked jury-verdict exemplar with per-category counts)
- `docs/recipes/espionage-classified-disclosure.md` — Espionage Act / classified NDI cases with `uco-marking` classification banners (worked Rule 11(c)(1)(C) plea exemplar)
- `docs/recipes/export-control-sanctions.md` — IEEPA/EAR export and sanctions cases (worked exemplar with per-defendant dispositions on shared counts and recommended-vs-imposed sentence divergence)
- `docs/recipes/extensions.md` — extension workflow and strict concept coverage
- `docs/recipes/change-proposal.md` — filing gaps upstream (CASE #191-#194)
