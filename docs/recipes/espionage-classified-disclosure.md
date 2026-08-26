# Espionage Act and Classified-Information Disclosure

> See [Recipe Index](INDEX.md) for all recipes.

Model Espionage Act prosecutions: a security-clearance holder willfully
retains and/or transmits classified national defense information ("NDI")
to persons not entitled to receive it, charged federally under 18 U.S.C.
§ 793 (willful retention/transmission) or § 794 (delivery to a foreign
government). The distinctive modeling requirement is **U.S. Government
classification markings**: the charged information carries banners such as
`TOP SECRET//SCI` or `SECRET` that are elements of the offense narrative,
and UCO's Marking namespace (`uco-marking`) is the correct home for them —
attached to the charged NDI observables via `uco-core:objectMarking`, not
buried in free-text descriptions. The evidence is characteristically a mix
of classified-facility telemetry (SCIF access, workstation and printer
use), social media or messaging posts, the defendant's own quoted
messages, signed non-disclosure and indoctrination agreements, and
obstruction artifacts (deleted accounts, destroyed devices).

Validated against `examples/pacer/dma_2023_cr_10159/` (U.S. v. Jack
Douglas Teixeira, D. Mass. 1:23-cr-10159-IT — Air National Guardsman
posting TS//SCI documents to Discord; six § 793(e) counts, Rule
11(c)(1)(C) plea, 200-month government recommendation).

**When to use this recipe**

- Charges cite 18 U.S.C. § 793 or § 794, or filings describe unauthorized
  retention, removal, transmission, or disclosure of classified national
  defense information by a clearance holder
- Documents or information are described with USG classification banners
  (CONFIDENTIAL, SECRET, TOP SECRET, SCI compartments, dissemination
  controls such as NOFORN or REL TO FVEY)
- The removal chain runs through a SCIF, classified network (JWICS,
  SIPRNet), classified workstation, or classified printer
- For *corporate* trade secret theft and § 1831 economic espionage, use
  [insider-threat-trade-secrets.md](insider-threat-trade-secrets.md)
  instead — § 1831/1832 protects corporate proprietary information, while
  § 793/794 protects government NDI; the court-process layer shared by
  both is in [legal-process-modeling.md](legal-process-modeling.md)

## Classes and properties

| Class | Role |
|---|---|
| `case-investigation:Investigation` | Case container |
| `uco-identity:Person` | Defendant clearance holder, declarants (agency officials, case agents) |
| `uco-identity:Organization` | Defendant's unit/agency, the United States Government (owner of the NDI and victim), FBI, USAO, DOJ National Security Division, the platform operator |
| `uco-observable:ObservableObject` | Each charged NDI item (one node per count), posted document images, platform servers/chat rooms |
| `uco-marking:MarkingDefinition` + `uco-marking:StatementMarking` | The classification banner of each charged NDI item, verbatim as charged, attached via `uco-core:objectMarking` |
| `uco-observable:Computer` / `Device` / `Tablet` | Classified workstation, SCIF printer, destroyed personal devices |
| `uco-observable:ObservableObject` + `DigitalAccountFacet` | Defendant's platform account (username changes are obstruction evidence) |
| `uco-observable:Message` + `MessageFacet` | Defendant's quoted messages (consciousness of guilt, obstruction instructions) |
| `uco-location:Location` | Base/duty station, residence |
| `uco-core:UcoObject` + `gufo:FunctionalComplex` | Non-cyber items: the SCIF facility, paper printouts carried out of it |
| `uco-action:Action` | Clearance grant, indoctrination/training signings, admonitions, each transmission method, obstruction acts |
| `case-investigation:InvestigativeAction` | Arrest, seizures |
| `legalproc:*` (extension) | Complaint → indictment chain, per-count charges, plea, forfeiture, recommended/imposed sentences |

## Modeling patterns

### 1. Classification banners are markings, not descriptions

Give each distinct banner one `uco-marking:MarkingDefinition` node (typed also
`uco-core:UcoObject`) whose `uco-marking:definition` points to a
`uco-marking:StatementMarking` carrying the banner verbatim in
`uco-marking:statement`. Attach it to every charged NDI observable with
`uco-core:objectMarking`. UCO 1.4 has no dedicated USG-classification
MarkingModel (see [UCO #647](https://github.com/ucoProject/UCO/issues/647)),
so `StatementMarking` is the current validated carrier; when a structured
USG model is adopted upstream, migration is a re-typing of the model node.

```json
{
  "@id": "kb:marking-ts-sci-def",
  "@type": ["uco-marking:MarkingDefinition", "uco-core:UcoObject"],
  "uco-core:name": "USG classification banner: TOP SECRET//SCI",
  "uco-marking:definitionType": "statement",
  "uco-marking:definition": [{"@id": "kb:marking-ts-sci-model"}]
}
{
  "@id": "kb:marking-ts-sci-model",
  "@type": "uco-marking:StatementMarking",
  "uco-marking:definitionType": "statement",
  "uco-marking:statement": "TOP SECRET//SCI"
}
{
  "@id": "kb:ndi-count1",
  "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
  "uco-core:objectMarking": [{"@id": "kb:marking-ts-sci-def"}]
}
```

### 2. Never promote malformed or defendant-quoted banners to markings

Model only banners the charging instrument attests as actually appearing
on the charged material. Banner strings quoted from the defendant's own
messages stay as verbatim `MessageFacet` content. Real records contain
impossible combinations — in the Teixeira exemplar the defendant typed
`TS//NOFORN//FVEY`, which is internally contradictory (NOFORN prohibits
release to any foreign national; REL TO FVEY authorizes release to Five
Eyes partners; the two dissemination controls are mutually exclusive under
ODNI/CAPCO marking rules). Preserve such strings as quoted evidence with a
note explaining the contradiction; creating a `MarkingDefinition` from
them would assert a handling policy that cannot exist.

### 3. One NDI observable per count, owned by the government

Indictments charge NDI per count with a per-count classification level and
description. Give each charged item its own `ObservableObject` named with
its count and banner, described verbatim from the count chart, marked per
pattern 1, and linked with registered `Related_To` to the United States
Government organization, with ownership stated in `uco-core:description`.
Each `legalproc:CriminalCharge` links to its NDI item with registered
`Related_To` and a description stating that the charge concerns the item;
the government links to every count with
registered `Related_To` with the victim assertion in `uco-core:description`.

### 4. Each transmission method is its own Action

Espionage indictments typically distinguish transmission methods (e.g.
transcribing classified text into chat messages vs. printing, removing,
photographing, and posting documents). Model each method as one
`uco-action:Action` with `performer`, `instrument` (workstation, printer,
platform account), `object` (the charged NDI items it moved), `result`
(posted images, platform servers), `location`, and the charged date span.
Link each action to the counts it grounds with registered `Related_To` and describe the evidentiary basis.

### 5. The SCIF is physical; the workstation inside it is cyber

The SCIF facility and the paper printouts carried out of it never live in
cyberspace: `uco-core:UcoObject` + `gufo:FunctionalComplex` per the rule
in [legal-process-modeling.md](legal-process-modeling.md). The classified
workstation, the SCIF printer, the digital source documents, and the
photographs posted online are UCO observables. Wire them with
registered `Related_To` relationships with the location basis in `uco-core:description` so the physical/cyber boundary is explicit.

### 6. Trainings, agreements, and admonitions are the knowledge timeline

Willfulness is an element; the government proves it with the clearance
grant, signed SCI indoctrination memoranda, refresher trainings, signed
network user agreements, and superiors' admonitions. Model each as a dated
`uco-action:Action` quoting the signed language verbatim — these dates
frame the charged conduct window.

### 7. Obstruction acts parallel the exfiltration

Deleting servers, changing usernames, instructing associates to delete
messages, and destroying devices are each dated `Action`s with the
affected accounts/devices as `object` and quoted instructions preserved
as `Message` nodes. They ground sentencing enhancements (USSG § 3C1.1)
even when uncharged.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Classification levels only in free-text descriptions | Attach `uco-marking` MarkingDefinition + StatementMarking via `uco-core:objectMarking` so classification is queryable |
| Inventing a MarkingDefinition from a defendant-quoted or contradictory banner string (e.g. NOFORN + FVEY together) | Keep it as verbatim quoted message content with a note; only attested document banners become markings |
| Treating the case as corporate insider threat | § 793/794 protects government NDI, not trade secrets; the victim/owner is the United States Government, and classification markings — not trade-secret categories — carry the sensitivity semantics |
| Typing the SCIF or paper printouts as observables | Physical facility and paper are `uco-core:UcoObject` + `gufo:FunctionalComplex`; the devices and digital documents inside are the observables |
| One blob node for "leaked documents" | One NDI observable per charged count, each with its own banner marking and described `Related_To` link to its count |
| Fabricating classification detail (compartments, declass dates) the filings don't state | Model exactly the banner text charged; put E.O. 13526 level definitions in descriptions only when the filing recites them |

## Checklist

1. Ingest filings per
   [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md)
   (works for any PACER case); OCR scanned indictments and plea
   agreements; hash every source PDF into a source `ObservableObject`.
2. Create the `Investigation`, the defendant, the defendant's
   unit/agency, the United States Government (NDI owner and victim), the
   investigating and prosecuting agencies, and the platform operator.
3. Create one `MarkingDefinition` + `StatementMarking` pair per distinct
   banner charged; create one NDI observable per count with
   `uco-core:objectMarking`, and a registered `Related_To` ownership assertion to the government.
4. Build the knowledge timeline: clearance grant, indoctrination and
   training signings, user agreements, admonitions — each a dated
   `Action` with signed language verbatim.
5. Model each transmission method as an `Action` with full
   instrument/object/result wiring and the charged date span; model
   obstruction acts and quoted messages; type the SCIF and paper
   printouts with gUFO.
6. Model arrest and seizures as `InvestigativeAction`s; add `legalproc`
   charging instruments (complaint → indictment), per-count § 793/794
   charges, the forfeiture allegation, the plea, and
   recommended/imposed sentences (use `sentenceStatus` faithfully —
   don't assert an imposed sentence the record lacks).
7. Link each transmission action to its counts with registered `Related_To`
   and an evidentiary-basis description; link the government to every count
   with a described `Related_To` victim assertion; link each count to its
   NDI item with registered `Related_To` and a charge-concerns-item description.
8. Validate: `validate_graph(path, extensions=['legalproc'])` plus strict
   concept coverage; `Conforms: True` before presenting.

## Validated exemplar

`examples/pacer/dma_2023_cr_10159/build_teixeira_dma_2023_espionage.py`
— U.S. v. Jack Douglas Teixeira: Massachusetts Air National Guardsman
with TS//SCI clearance transcribing and photographing classified
documents from the Otis ANG Base SCIF and posting them to Discord for
over a year; six § 793(e) counts with per-count TS//SCI and SECRET
banner markings via `uco-marking`, transcription and print/photograph
transmission actions, training/admonition knowledge timeline, obstruction
(deleted server, destroyed devices), Rule 11(c)(1)(C) plea, forfeiture,
and a 200-month recommended sentence. 123 nodes; passes `case_validate`
and strict concept coverage with the `legalproc` extension.

## Related

- [legal-process-modeling.md](legal-process-modeling.md) — charges, pleas, sentences, and the cyber vs. non-cyber evidence rule
- [insider-threat-trade-secrets.md](insider-threat-trade-secrets.md) — corporate trade secrets / § 1831 economic espionage (contrast: corporate victim, no classification markings)
- [export-control-sanctions.md](export-control-sanctions.md) — IEEPA/EAR export cases (contrast: lawfully bought goods unlawfully exported; no classified information)
- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md) — PACER PDF ingestion and provenance
- [threaded-messaging.md](threaded-messaging.md) — full per-message chat extractions when available
- [email-messaging.md](email-messaging.md) — email and messaging evidence
- [event.md](event.md) — event-log style timelines
