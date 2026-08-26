# Export Control and Sanctions Evasion

> See [Recipe Index](INDEX.md) for all recipes.

Model export-control and sanctions-evasion prosecutions: defendants
procure controlled U.S. goods or technology for prohibited foreign end
users, concealing the true destination behind intermediary ("straw" or
transshipment) entities and false export paperwork. Charged federally
under IEEPA (50 U.S.C. § 1705) with the Export Administration Regulations
(EAR, 15 C.F.R. §§ 730-774), smuggling (18 U.S.C. § 554), and false
export information (13 U.S.C. § 305); ITAR/AECA (22 U.S.C. § 2778) and
OFAC sanctions programs (31 C.F.R.) cases follow the same shape. The
distinctive modeling requirements are (1) **the regulatory timeline** —
Entity List/SDN designations are dated government actions that gate what
conduct was unlawful when; (2) **the controlled item** — usually a
physical machine or component that never lives in cyberspace and takes
gUFO typing, while the *export records about it* (EEI/AES filings,
waybills, contracts, emails) are the cyber observables; and (3) **the
concealment chain** — who was papered as consignee versus who actually
received the goods.

Validated against `examples/pacer/ndca_2020_cr_00446/` (U.S. v. Han Li
and Lin Chen, N.D. Cal. 3:20-cr-00446-WHA — PRC nationals routing an
EAR99 wafer scribe-and-break machine through intermediary JHI to Entity
List designee Chengdu GaStone; four counts, one defendant convicted by
plea, co-defendant's counts pending).

**When to use this recipe**

- Charges cite 50 U.S.C. § 1705 (IEEPA), 15 C.F.R. § 764.2, 18 U.S.C.
  § 554 (smuggling), 13 U.S.C. § 305 (false export information), 22
  U.S.C. § 2778 (AECA/ITAR), or OFAC sanctions regulations
- Filings describe the Entity List, SDN list, Commerce Control List,
  ECCN or EAR99 classifications, export licenses, Shipper's Export
  Declarations, EEI, AES filings, freight forwarders, ultimate
  consignees, or end-user concealment
- Goods move to embargoed or restricted destinations/end users through
  intermediary companies or transshipment points
- For classified-information disclosure by clearance holders, use
  [espionage-classified-disclosure.md](espionage-classified-disclosure.md);
  for corporate trade-secret exfiltration, use
  [insider-threat-trade-secrets.md](insider-threat-trade-secrets.md) —
  export-control cases concern *lawfully purchased but unlawfully
  exported* items, not stolen information

## Classes and properties

| Class | Role |
|---|---|
| `case-investigation:Investigation` | Case container |
| `uco-identity:Person` | Defendants (procurement agents, brokers, intermediary employees) |
| `uco-identity:Organization` | Designated end user, intermediary/straw consignee, U.S. supplier, DOC/BIS, DHS/CBP (AES), FBI/HSI, USAO, DOJ NSD |
| `uco-action:Action` | Entity List/SDN designation (performer: the regulator; object: the designated org), conspiracy course of conduct, relationship building, false filing, the export/shipment itself, post-sale support |
| `uco-core:UcoObject` + `gufo:FunctionalComplex` | The controlled physical item (machine, component) and consumables — never observables |
| `uco-observable:ObservableObject` | False EEI/AES filing, SEDs, waybills, contracts, invitation letters, source PDFs |
| `uco-observable:EmailMessage` + `EmailMessageFacet` | Procurement and concealment correspondence (verbatim quotes) |
| `uco-location:Location` | Supplier city, true destination, papered destination |
| `case-investigation:Authorization` + `InvestigativeAction` | Arrest warrant (often issued with a sealed indictment) and border/port-of-entry arrest |
| `legalproc:*` (extension) | Sealed indictment, per-defendant charges on shared counts, plea, forfeiture, recommended/imposed sentences |

## Modeling patterns

### 1. Regulatory designations are dated Actions, not descriptions

An Entity List (or SDN) designation is a dated act by an identifiable
agency that changes the legal status of every later shipment. Model each
designation as a `uco-action:Action` with the regulator (`DOC/BIS`,
`OFAC`) as `performer`, the designated organization as `object`, and the
Federal Register designation date as `startTime`. The charged export
must postdate the designation — and when a related sale *predates* it
(in the exemplar, the CETC 55 sale preceded that entity's 2018
designation), say so explicitly: it is exculpatory for that transaction
and shows the timeline is load-bearing.

### 2. The controlled item is physical; the export records are cyber

A wafer scriber, machine tool, or aircraft part never lives in
cyberspace: type it `uco-core:UcoObject` + `gufo:FunctionalComplex` per
[legal-process-modeling.md](legal-process-modeling.md). Record its
export-control classification (ECCN or EAR99) in the description — it is
a regulatory classification of a physical good, **not** a data marking,
so `uco-marking` does not apply (contrast with classified-document
banners in
[espionage-classified-disclosure.md](espionage-classified-disclosure.md)).
The EEI/AES filing, SED, waybill, contract, and procurement emails are
`uco-observable` nodes; the false statements they carry are the charged
conduct.

### 3. The concealment chain: papered consignee vs. true end user

The core deception is a consignee mismatch. Wire it explicitly:

- link the intermediary organization (`JHI`) with registered `Related_To` to
  the papered destination and the designated end user (`GaStone`) to the true
  destination; state each location role in `uco-core:description`;
- the false-filing `Action` produces (`result`) the EEI observable whose
  description quotes the false statements (no license required; JHI as
  ultimate consignee);
- the export `Action` moves the physical item (`object`) with
  `location` set to the *true* destination;
- link the item with registered `Related_To` to the true end user and state ownership in `uco-core:description`.

A reviewer should be able to answer "who was on the paperwork?" and "who
got the machine?" from graph structure, not prose.

### 4. Per-defendant charges on shared counts

Multi-defendant export indictments charge the same counts against all
defendants, but dispositions diverge (in the exemplar: Chen pleaded to
Count 4 with Counts 1-3 dismissed; Li's four counts remain pending).
Create one `legalproc:CriminalCharge` node **per defendant per count**
with its own `chargeDisposition`, all `assertedIn` the same charging
instrument, and link each defendant only to their own charge nodes with
`Charged_With`. Never hang a single shared charge node with a merged
disposition.

### 5. Recommended vs. imposed sentences can diverge sharply

Keep the government's recommendation (`sentenceStatus: recommended`,
sourced to the sentencing memorandum) and the court's sentence
(`sentenceStatus: imposed`, sourced to the docket/judgment) as separate
`legalproc:Sentence` nodes. In the exemplar the government sought 27
months and a $255,000 fine; the court imposed 4 months and $5,000 — a
divergence that disappears if only one node is modeled.

### 6. Sealed-then-unsealed charging instruments

Export cases against foreign nationals are often indicted under seal and
unsealed years later at a border arrest. Record both dates on the
charging instrument description, model the arrest warrant as a
`case-investigation:Authorization` referenced by the arrest
`InvestigativeAction` (`relevantAuthorization`), and date the arrest —
the gap between indictment and arrest is real case structure, not noise.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Entity List/SDN status stated only in an organization's description | A dated designation `Action` by the regulator with the org as `object`; the description can summarize |
| Typing the exported machine as `uco-observable:ObservableObject` | Physical goods take `uco-core:UcoObject` + `gufo:FunctionalComplex`; the export *records* are the observables |
| Attaching ECCN/EAR99 via `uco-marking` | `uco-marking` governs data handling markings; export-control classifications of physical goods belong in descriptions |
| One shared charge node for co-defendants | One charge node per defendant per count, each with its own disposition |
| Modeling only the imposed sentence | Recommended and imposed sentences are separate nodes with `sentenceStatus` |
| Treating the case as trade-secret theft | The item was lawfully bought and unlawfully *exported*; there is no proprietary-information victim — the regulatory regime is the harmed interest |

## Checklist

1. Ingest filings per
   [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md);
   OCR scanned indictments (PACER indictment PDFs often carry CID-mapped
   text that silently strips digits — re-OCR and verify dates); hash
   every source PDF into a source `ObservableObject`.
2. Create the `Investigation`, defendants, the intermediary and
   designated organizations, the U.S. supplier, and the regulator/agency
   organizations (DOC/BIS, CBP for AES, FBI/HSI, USAO, DOJ NSD).
3. Model each Entity List/SDN designation as a dated regulatory
   `Action`; check every charged transaction against the designation
   dates and note any that predate designation.
4. Type the controlled item(s) and consumables with gUFO; record
   ECCN/EAR99 and price terms in descriptions.
5. Model the conduct: conspiracy course-of-conduct `Action` with the
   charged date span, relationship-building, the false EEI/AES filing
   (result: the EEI observable), the export itself (object: the item;
   location: true destination), and post-sale support; preserve quoted
   emails verbatim as `EmailMessage` nodes.
6. Add `legalproc` structure: sealed/unsealed charging instrument,
   per-defendant per-count charges with `offenseForm` and
   `chargeDisposition`, `objectOffense` from the conspiracy count to its
   object offense, forfeiture allegation, plea, and
   recommended + imposed sentences.
7. Model the arrest warrant `Authorization` and the border arrest
   `InvestigativeAction`; wire conduct to counts and counts to the controlled
   item with registered `Related_To`, stating evidentiary-basis and
   charge-concerns-item semantics in `uco-core:description`.
8. Validate: `validate_graph(path, extensions=['legalproc'])` plus
   strict concept coverage; `Conforms: True` before presenting.

## Validated exemplar

`examples/pacer/ndca_2020_cr_00446/build_li_chen_ndca_2020_export_control.py`
— U.S. v. Han Li and Lin Chen: PRC nationals procuring a Dynatex DTX-150
Automatic Diamond Scriber Breaker (EAR99 dual-use wafer scribe-and-break
machine) for Entity List designee Chengdu GaStone Technology Co. through
intermediary JHI, with false EEI naming JHI as ultimate consignee; two
dated Entity List designation actions (GaStone 2014, CETC 55 2018),
gUFO-typed machine and consumables, per-defendant charges on four shared
counts (plea + dismissals vs. pending), sealed indictment unsealed at a
2024 border arrest, and a 27-month/$255,000 recommendation against a
4-month/$5,000 imposed sentence. 103 nodes; passes `case_validate` and
strict concept coverage with the `legalproc` extension.

## Related

- [legal-process-modeling.md](legal-process-modeling.md) — charges, pleas, sentences, and the cyber vs. non-cyber evidence rule
- [espionage-classified-disclosure.md](espionage-classified-disclosure.md) — classified-information disclosure (contrast: government NDI with `uco-marking` banners)
- [insider-threat-trade-secrets.md](insider-threat-trade-secrets.md) — trade-secret exfiltration (contrast: stolen information, corporate victim)
- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md) — PACER PDF ingestion and provenance
- [email-messaging.md](email-messaging.md) — email evidence patterns
