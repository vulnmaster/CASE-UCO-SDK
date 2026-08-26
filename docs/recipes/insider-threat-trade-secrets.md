# Insider Threat, Trade Secret Theft, and Economic Espionage

> See [Recipe Index](INDEX.md) for all recipes.

Model insider-threat prosecutions: a trusted employee or contractor
exfiltrates proprietary information (trade secrets, source code, design
documents) from a corporate network, typically for a competitor, a personal
venture, or a foreign government or instrumentality. Charged federally as
theft of trade secrets (18 U.S.C. § 1832) and — when a foreign-government
benefit is intended or known — economic espionage (18 U.S.C. § 1831). The
evidence is characteristically **corporate-telemetry-heavy**: data-loss-
prevention logs, badge access records, login IP and two-factor
authentication logs, surveillance footage, personal cloud accounts, and
the exfiltrated file set itself, followed by an FBI warrant chain. This
recipe covers the exfiltration method and timeline, the victim company's
protective measures and internal detection chain, undisclosed outside
affiliations, foreign-government-benefit evidence, and per-category trade
secret counts with jury-verdict findings.

Validated against `examples/pacer/ndca_2024_cr_00141/` (U.S. v. Linwei
Ding, N.D. Cal. 3:24-cr-00141-VC — Google AI/TPU trade secrets exfiltrated
to personal cloud accounts while the defendant founded PRC startups;
convicted by jury on all 14 counts).

**When to use this recipe**

- Filings describe an employee uploading, emailing, or copying
  confidential files to personal accounts or devices, often with an
  evasion method (staging through another application, renaming,
  encryption, personal cloud storage)
- Trade secret categories are enumerated in an indictment (§ 1832), with
  or without parallel economic-espionage counts (§ 1831)
- Corporate security telemetry (DLP, badge records, "impossible travel"
  signals, surveillance footage) is the detection evidence
- Undisclosed outside employment, a competing startup, a talent-program
  application, or investor pitches evidence motive and intended
  beneficiaries
- For external network attackers (no insider), use
  [network-investigation.md](network-investigation.md) /
  [network-artifacts.md](network-artifacts.md) instead; for the court
  process layer shared by all prosecutions, see
  [legal-process-modeling.md](legal-process-modeling.md)

## Classes and properties

| Class | Role |
|---|---|
| `case-investigation:Investigation` | Case container |
| `uco-identity:Person` | Defendant insider, co-venture participants, unnamed accomplices (e.g. a badge-scanning colleague) |
| `uco-identity:Organization` | Victim company, competing/receiving companies, incubators, foreign government agencies (intended beneficiaries), FBI, USAO |
| `uco-observable:Laptop` / `MobileDevice` | Corporate-issued devices used to stage the exfiltration, later locked and retrieved |
| `uco-observable:ObservableObject` + `DigitalAccountFacet` | Personal cloud accounts receiving the uploads ("DING Account 1/2") |
| `uco-observable:ObservableObject` + `ApplicationFacet` | The staging application (e.g. Apple Notes used for note-to-PDF conversion) |
| `uco-observable:ObservableObject` | The exfiltrated file set; each enumerated Trade Secret Category; security telemetry (badge/login/2FA records); surveillance footage; pitch decks, memos, affidavits |
| `uco-observable:ObservableObject` + `InstantMessagingAddressFacet` | Defendant's messaging account (e.g. WeChat ID) |
| `uco-observable:Message` + `MessageFacet` | Key messages quoted in the charging instrument ("replicate and upgrade") |
| `uco-observable:EmailMessage` | Resignation email, job-offer emails |
| `uco-location:Location` | Victim campus, defendant residence, foreign conference sites |
| `uco-action:Action` | Exfiltration uploads (with `instrument` = laptop + staging app, `object` = trade secret categories, `result` = file set), affiliations, pitches, concealment acts |
| `case-investigation:InvestigativeAction` + `Authorization` | Corporate detection chain (DLP hit, interview, network-history search, footage review, device retrieval) and FBI warrant searches |
| `uco-core:UcoObject` + `gufo:FunctionalComplex` | Non-cyber items: the physical access badge (its scan *records* are observables) |
| `legalproc:*` (extension) | Charging-instrument chain, per-category counts, jury verdicts, forfeiture |

## Modeling patterns

### 1. The exfiltration is one Action with full instrument/object/result wiring

The core charged conduct is usually a single sustained course of uploads.
Model it as one `uco-action:Action` with a `startTime`/`endTime` span,
`uco-action:instrument` pointing at the corporate device and the staging
application, `uco-action:object` pointing at every enumerated trade secret
category, and `uco-action:result` pointing at the exfiltrated file set.
Then link it to each count with registered `Related_To` and describe the
conduct as the evidentiary basis — every § 1832 and § 1831 count rests on the
same conduct, distinguished by category.

```json
{
  "@type": ["uco-action:Action", "uco-core:UcoObject"],
  "uco-core:name": "Ding uploads 1,000+ confidential files to Ding Account 1 (2022-05-21 to 2023-05-02)",
  "uco-action:performer": {"@id": "urn:uuid:person-defendant"},
  "uco-action:instrument": [{"@id": "urn:uuid:corporate-macbook"}, {"@id": "urn:uuid:apple-notes-app"}],
  "uco-action:object": [{"@id": "urn:uuid:ts-category-1"}, {"@id": "urn:uuid:ts-category-2"}],
  "uco-action:result": [{"@id": "urn:uuid:exfiltrated-fileset"}],
  "uco-action:startTime": {"@type": "xsd:dateTime", "@value": "2022-05-21T00:00:00-07:00"},
  "uco-action:endTime": {"@type": "xsd:dateTime", "@value": "2023-05-02T00:00:00-07:00"}
}
```

Record the evasion method verbatim in the description (e.g. copying source
files into Apple Notes and exporting PDFs to defeat DLP file-transfer
logging) — the method is an element of the concealment narrative and often
of venue.

### 2. Trade secret categories are observables, one node per enumerated category

Indictments under § 1832/§ 1831 enumerate categories; verdicts return
per-category findings. Give each category its own `ObservableObject` named
exactly as charged ("Trade Secret Category 1"), describe it verbatim from
the indictment, list exemplar exhibit file titles from the verdict form
when available, and link it with registered `Related_To` to the victim
company with ownership stated in `uco-core:description`, plus
`Contained_Within` to the exfiltrated file set. Each count then links to its
category with described `Related_To` — this is what lets one graph
answer "which files ground Count Eleven?"

### 3. Paired § 1832 / § 1831 counts share categories, not nodes

Economic-espionage counts typically mirror the theft counts one-to-one per
category, adding the foreign-government-benefit element. Keep separate
`legalproc:CriminalCharge` nodes per count (each has its own verdict), but
point both members of a pair at the same category observable. Put the
benefit element in the § 1831 count descriptions, and model the intended
beneficiaries (foreign ministries, regulators) as `Organization` nodes so
the benefit evidence (policy decks, talent-program applications) can link
to them.

### 4. Corporate telemetry is cyber; the badge is not

Badge access logs, login IPs, 2FA logs, DLP transfer logs, and risk
analytics ("Impossible Location Signal") are cyber observables — model
them as an `ObservableObject` record set that the detection
`InvestigativeAction`s consume. The physical badge itself never lives in
cyberspace: `uco-core:UcoObject` + `gufo:FunctionalComplex` per the rule
in [legal-process-modeling.md](legal-process-modeling.md). A colleague
scanning the defendant's badge to simulate presence is its own `Action`
with the badge as `instrument` and the badge records as `result`.

### 5. The corporate detection chain precedes the government's

Insider-threat cases have two investigation phases with different
performers. Model the victim company's internal steps (DLP detection,
employee interview, self-deletion affidavit, network-history search,
surveillance-footage review, access suspension, device retrieval) as
`case-investigation:InvestigativeAction`s performed by the company, then
the FBI's warrant-backed searches (residence, cloud accounts) with
`case-investigation:relevantAuthorization` → `Authorization` nodes. The
handoff point (what the company knew and when it referred) is often
litigated — keep the dates precise.

### 6. Undisclosed affiliations and concealment acts are the motive timeline

Job offers, startup founding, incubator agreements, investor pitches,
talent-program applications, one-way flight bookings, and the resignation
are each dated `uco-action:Action`s. Messaging-thread exhibits (a WeChat
group export) get an `ObservableObject` for the thread, an
`InstantMessagingAddressFacet` account node for the defendant's handle,
and `Message` + `MessageFacet` nodes for messages quoted in the charging
instrument — see [threaded-messaging.md](threaded-messaging.md) when full
per-message extractions are available.

### 7. Jury verdicts with per-category findings

One `legalproc:Verdict` per count (`verdictType`: "guilty" /
"not-guilty"), `legalproc:concernsCharge` → the count, plus registered
`Related_To` links to the trial `CriminalProceeding` and verdict-form source
document with occurrence/provenance semantics in `uco-core:description`.
When the verdict form records which exhibits the jury unanimously found to
be trade secrets (including "combination of all documents" findings),
summarize that in the verdict description rather than inventing per-exhibit
nodes the record does not individuate.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Modeling the insider as an external "attacker" with intrusion classes | There is no unauthorized access to model — the insider was *authorized*; the crime is what they did with the access. Use `Action` + trade secret observables, not exploit/malware patterns |
| One giant "stolen data" node | One node per enumerated trade secret category + one file-set node; counts and verdicts are per-category |
| Typing the physical access badge as an observable | Badge is `uco-core:UcoObject` + `gufo:FunctionalComplex`; the scan records are the observables |
| Collapsing Google's internal investigation into the FBI's | Separate performers, separate `InvestigativeAction`s; the corporate chain has no `Authorization`, the warrant chain does |
| Omitting the foreign-government beneficiary organizations | § 1831 counts require the benefit element — model the government agencies cited in the evidence and link the policy/talent-program documents to them |
| Fabricating upload timestamps | Use only dates the record states; recovered file names often embed upload timestamps ("-at-2022-06-01T18_10_22Z-pinned.pdf") — cite them as evidence, not as invented precision |

## Checklist

1. Ingest filings per
   [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md)
   (works for any PACER case); OCR scanned verdict forms and translated
   chat exhibits; hash every source PDF into a source `ObservableObject`.
2. Create the `Investigation`, the defendant, the victim company (with
   its protective measures described — reasonable-measures is an element
   of § 1832/§ 1831), receiving/competing organizations, intended
   foreign-government beneficiaries, and the investigating agencies.
3. Model the exfiltration: corporate devices, staging application,
   personal cloud accounts (`DigitalAccountFacet`), the exfiltrated file
   set, and one observable per enumerated trade secret category
   (described `Related_To` ownership assertion, `Contained_Within` file set).
4. Build the motive/concealment timeline: outside affiliations, pitches,
   talent-program applications, badge-scan simulation, self-deletion
   affidavit, flight booking, resignation — each a dated `Action`.
5. Model the corporate detection chain and the FBI warrant chain as
   `InvestigativeAction`s (warrants get `Authorization` nodes).
6. Add `legalproc` charging instruments (indictment → superseding →
   second superseding with described `Related_To` edges), per-category
   §1832/§1831 counts (described `Related_To` → category), the forfeiture
   allegation, the trial
   proceeding, and per-count verdicts.
7. Link the exfiltration action to every count with registered `Related_To`
   and an evidentiary-basis description; link the victim company to every
   count with a described `Related_To` victim assertion.
8. Validate: `validate_graph(path, extensions=['legalproc'])` plus strict
   concept coverage; `Conforms: True` before presenting.

## Validated exemplar

`examples/pacer/ndca_2024_cr_00141/build_ding_ndca_2024_insider_threat.py`
— U.S. v. Linwei Ding: Google software engineer exfiltrating seven
categories of AI-supercomputing trade secrets (TPU/GPU chips and systems,
cluster management software, SmartNIC) via an Apple Notes-to-PDF method to
personal Google Cloud accounts while founding PRC startups Rongshu and
Zhisuan; badge-scan concealment, self-deletion affidavit, corporate
detection chain, FBI residence and cloud-account warrants, a three-
instrument charging chain, and a 14-count jury conviction (7 × § 1832,
7 × § 1831) with per-category trade-secret findings. 286 nodes; passes
`case_validate` and strict concept coverage with the `legalproc`
extension.

## Related

- [legal-process-modeling.md](legal-process-modeling.md) — charges, verdicts, sentences, and the cyber vs. non-cyber evidence rule
- [espionage-classified-disclosure.md](espionage-classified-disclosure.md) — government classified-information cases (§ 793/§ 794) with `uco-marking` classification banners (contrast: government victim, not corporate)
- [export-control-sanctions.md](export-control-sanctions.md) — IEEPA/EAR export cases (contrast: goods lawfully bought and unlawfully exported, not stolen information)
- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md) — PACER PDF ingestion and provenance
- [threaded-messaging.md](threaded-messaging.md) — ordered chat threads for messaging exhibits (WeChat, WhatsApp, Telegram)
- [network-investigation.md](network-investigation.md) — external-attacker intrusions (contrast: no insider)
- [email-messaging.md](email-messaging.md) — email evidence (offer emails, resignation)
- [event.md](event.md) — event-log style timelines
- [fraud-crypto-laundering.md](fraud-crypto-laundering.md) — when the insider monetizes through financial-crime channels
