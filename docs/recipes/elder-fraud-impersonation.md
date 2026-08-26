# Elder Fraud and Government-Impersonation Schemes

> See [Recipe Index](INDEX.md) for all recipes.

Model elder-fraud prosecutions and government-impersonation ("agent scam")
schemes: transnational call centers whose callers pose as U.S. Treasury /
DOJ / IRS / Social Security agents, convince elderly victims their bank
accounts are implicated in crime, and collect the victims' cash "for
safekeeping" through prepaid-card transfers (Green Dot, gift cards), mailed
cash packages, and in-person courier pickups. The evidence is
characteristically **hybrid**: cyber artifacts (spoofed caller-ID calls,
courier dispatch texts, cell-site records, payment cards used for courier
logistics) interleaved with non-cyber physical handoffs (cash boxes, decoy
packages, rental cars). This recipe covers the scheme timeline, the courier
network, victim modeling, the law-enforcement sting, and the legal process
from complaint through amended judgment.

Validated against `examples/pacer/edla_2022_cr_00115/` (U.S. v. Keel &
Panchal, E.D. La. 2:22-cr-00115 — $4.5M / 31-victim Treasury-impersonation
network; conviction by plea).

**When to use this recipe**

- Warrant returns or filings describe victims directed to buy prepaid /
  gift cards, mail cash, or hand cash to a courier after calls from
  purported government agents, bank security, or tech support
- A "money mule" / courier defendant is charged (often wire-fraud
  conspiracy, 18 U.S.C. § 1349) while the callers remain overseas and
  unindicted
- A tech-support pop-up or phishing contact escalated into an
  impersonation scheme
- For investment-platform ("pig butchering") and crypto-laundering fraud,
  use [fraud-crypto-laundering.md](fraud-crypto-laundering.md) instead;
  for the court-process layer shared by all prosecutions, see
  [legal-process-modeling.md](legal-process-modeling.md)

## Classes and properties

| Class | Role |
|---|---|
| `case-investigation:Investigation` | Case container |
| `uco-identity:Person` | Defendant couriers, victims, dispatcher aliases ("King K"), detectives |
| `uco-identity:Organization` | The fraud network itself, sheriff's offices, HSI, the prepaid-card bank |
| `uco-observable:PhoneAccount` + `PhoneAccountFacet` (`phoneNumber`) | Courier and victim phone numbers recovered from records |
| `uco-observable:ObservableObject` + `CallFacet` (`callType`, `to`, `startTime`) | Spoofed caller-ID calls (e.g. caller ID tag "US Treasury") |
| `uco-observable:Message` + `MessageFacet` (`from`, `messageText`, `sentTime`) | Courier dispatch texts; package-confirmation photo messages |
| `uco-observable:MobileDevice` | The seized courier phone |
| `uco-observable:PaymentCard` | Cards funding courier logistics; victim prepaid cards |
| `uco-observable:Computer` | Victim computer hit by the tech-support pop-up |
| `uco-observable:ObservableObject` | Cell-site record sets, extracted media |
| `uco-location:Location` | Handoff parking lots, hotels, victim residences |
| `uco-action:Action` | Overt acts: dispatch texts, flights, pickups, spoofed calls |
| `case-investigation:InvestigativeAction` + `Authorization` | Sting, arrest, phone/hotel/cell-tower warrants |
| `uco-core:UcoObject` + `gufo:FunctionalComplex` | Non-cyber items: cash boxes, decoy box, rental car |
| `legalproc:*` (extension) | Charges, instruments, plea, sentence, forfeiture, restitution |

## Modeling patterns

### 1. The spoofed impersonation call is a cyber observable

Caller-ID spoofing is a cyber-domain act. Model the call with a `CallFacet`
and record the impersonation in the description, verbatim from the filing:

```json
{
  "@id": "urn:uuid:...",
  "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
  "uco-core:name": "Spoofed 'US Treasury' call to Victim A (2022-04-04)",
  "uco-core:description": "Incoming call observed live by Det. D'Amato on Victim A's phone: Washington, DC area code, caller ID tag 'US Treasury'... Source: PACER Doc 61 (factual_basis), pp. 3-4",
  "uco-core:hasFacet": [
    {
      "@id": "urn:uuid:...",
      "@type": "uco-observable:CallFacet",
      "uco-observable:callType": "incoming (caller ID spoofed as 'US Treasury')",
      "uco-observable:to": {"@id": "urn:uuid:victim-phone-account"},
      "uco-observable:startTime": {"@type": "xsd:dateTime", "@value": "2022-04-04T00:00:00-05:00"}
    }
  ]
}
```

### 2. Courier dispatch texts prove conspiracy membership

The dispatch thread ("work" texts) is often the strongest evidence that a
courier knew the scheme's scope. Quote the messages verbatim and link the
`MessageFacet` `from` to the courier's `PhoneAccount`:

```json
{
  "@type": ["uco-observable:Message", "uco-core:UcoObject"],
  "uco-core:name": "Text thread between Keel and 'King K' (2021-10-22/23)",
  "uco-core:hasFacet": [
    {
      "@type": "uco-observable:MessageFacet",
      "uco-observable:from": {"@id": "urn:uuid:courier-phone-account"},
      "uco-observable:messageText": "two calling each day ready to work",
      "uco-observable:sentTime": {"@type": "xsd:dateTime", "@value": "2021-10-22T00:00:00-05:00"}
    }
  ]
}
```

### 3. Cash boxes and rental cars are NOT observables

Physical handoff items never live in cyberspace. Per the cyber vs.
non-cyber rule in
[legal-process-modeling.md](legal-process-modeling.md), dual-type them:

```json
{
  "@type": ["uco-core:UcoObject", "gufo:FunctionalComplex"],
  "uco-core:name": "Sealed box of $60,000 cash handed to Keel by Victim A (2022-04-03)"
}
```

The **photograph of the box** texted to co-conspirators, by contrast, *is*
an observable (`Message` + `MessageFacet`) — the photo is cyber even though
the box is not.

### 4. Scheme timeline as overt acts linked to the conspiracy count

Every dated step (dispatch text, victim withdrawal, courier flight,
handoff, spoofed call) is a `uco-action:Action`. Link it to the conspiracy
`legalproc:CriminalCharge` with registered `Related_To` and describe it as an
overt act in furtherance. Use `uco-action:participant` for co-participants and
`uco-action:location` for handoff locations. Link victims to acts and counts
with registered `Related_To` and describe the victim relationship explicitly.

### 5. The sting and the attribution chain are InvestigativeActions

Model the controlled delivery (decoy box as `uco-action:object`), the
arrest (seized phone as `uco-action:result`), and each warrant-backed
search (`case-investigation:relevantAuthorization` →
`case-investigation:Authorization`). The records attribution — airline,
hotel, payment-card, cell-site — is what ties the second courier to the
scheme; give it its own action with the payment card as `object` and the
cell-site record set as `result`.

### 6. Per-defendant dispositions on shared counts

When one defendant pleads and another is dismissed, keep one
`legalproc:CriminalCharge` per count and record both outcomes in
`chargeDisposition` (it accepts multiple values):

```json
{
  "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
  "legalproc:statuteCitation": "18 U.S.C. § 1349 (object offense 18 U.S.C. § 1343)",
  "legalproc:offenseForm": "conspiracy",
  "legalproc:chargeDisposition": [
    "convicted-by-plea (Keel, 2023-06-14)",
    "dismissed-on-government-motion (Panchal, 2023-09-05)"
  ]
}
```

A deferred restitution determination (common in multi-victim fraud) is
still one `legalproc:RestitutionOrder`: describe the deferral date and the
amended judgment; omit `monetaryAmount` when the amount is sealed rather
than inventing one.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Typing cash boxes, decoy packages, or rental cars as `uco-observable:Device` | They are never cyber-domain items: `uco-core:UcoObject` + `gufo:FunctionalComplex` |
| One "the scammers" Person for the whole call center | Keep the network as an `Organization`; give named aliases ("King K") their own `Person` nodes; leave unknown callers attributed to the organization |
| Recording the spoofed caller ID as the caller's real `PhoneAccount` | The spoofed tag ("US Treasury") is a property of the call, not an account; keep it in `callType`/description |
| Collapsing victim loss events into one lump sum | Each withdrawal, card purchase, mailing, and handoff is its own dated `Action` — the wires and the venue depend on them |
| Fabricating a restitution amount when the attachment is sealed | Model the order with its procedural history and omit `monetaryAmount` |
| Dropping the dismissed co-defendant from the graph | Keep their charges with `dismissed-on-government-motion` dispositions — the docket history is evidence |

## Checklist

1. Ingest filings per
   [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md)
   (works for any PACER case, not just CAC); OCR scanned charging
   documents; hash every source PDF into a source `ObservableObject`.
2. Create the `Investigation`, defendants, victims (age and district as
   charged — elder-fraud counts often turn on victim age), the fraud
   network `Organization`, and the law-enforcement agencies.
3. Model the cyber evidence: seized phones (`MobileDevice`), phone
   accounts, spoofed calls (`CallFacet`), dispatch and photo-confirmation
   messages (`MessageFacet`), payment cards, cell-site record sets, and
   any tech-support-scam entry point (`Computer`).
4. Model physical handoff items as `uco-core:UcoObject` +
   `gufo:FunctionalComplex`; add `uco-location:Location` nodes for drop
   sites, hotels, and victim residences.
5. Build the overt-act timeline with `uco-action:Action`, direct
   `uco-action:participant` / `uco-action:location` properties, and registered
   `Related_To` links to conspiracy charges and victims with precise
   descriptions.
6. Model the sting/arrest/warrant chain as `InvestigativeAction`s with
   `Authorization` nodes and result links to the seized/extracted
   observables.
7. Add `legalproc` charging instruments (complaint → indictment →
   superseding), charges with per-defendant dispositions, proceedings,
   plea, sentence, forfeiture, and (possibly deferred) restitution.
8. Validate: `validate_graph(path, extensions=['legalproc'])` plus strict
   concept coverage; `Conforms: True` before presenting.

## Validated exemplar

`examples/pacer/edla_2022_cr_00115/build_keel_panchal_edla_2022_elder_fraud.py`
— U.S. v. Keel & Panchal: two-courier / three-victim Treasury-impersonation
scheme with a controlled-delivery sting, phone/cell-tower/hotel warrants,
payment-card attribution, guilty plea, co-defendant dismissal, and deferred
restitution. 176 nodes; passes `case_validate` and strict concept coverage
with the `legalproc` extension.

## Related

- [legal-process-modeling.md](legal-process-modeling.md) — charges, pleas, sentences, and the cyber vs. non-cyber evidence rule
- [fraud-crypto-laundering.md](fraud-crypto-laundering.md) — investment-platform and crypto-laundering fraud
- [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md) — PACER PDF ingestion and provenance
- [threaded-messaging.md](threaded-messaging.md) — ordered chat threads when full message extractions are available
- [location.md](location.md) — richer address/geolocation modeling for drop sites
- [event.md](event.md) — event-log style timelines
