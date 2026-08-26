# Legal Charges, Sentencing, and Case Outcomes

> See [Recipe Index](INDEX.md) for all recipes.

Model indictments, charges, plea agreements, sentencing, supervised release, and sex-offender registry outcomes using CAC legal-outcomes module classes.

## Scope

**Layer 3 — Institutional workflow** for post-investigation legal disposition.

## Key classes

| Class | Role |
|---|---|
| `cacontology-legal-outcomes:CriminalCharge` | One node per formal charge; group with the charging instrument or Bundle |
| `StateCharge` / `FloridaStateCharge` / `GeorgiaStateCharge` | Jurisdiction-specific charges |
| `PleaAgreement` | Plea disposition |
| `SentencingOutcome` / `PrisonSentence` / `SupervisedRelease` | Sentencing results |
| `cacontology-sex-offender-registry:RegistrationRecord` | Registry integration when applicable |
| `uco-core:ExternalReference` | Statutory citation and defining source |
| `CACInvestigation` | Source investigation linkage |
| `Identity` | Defendant / subject |

## Maryland press-release pattern

Maryland ICAC arrest articles often report charges before sentencing. Until `MarylandStateCharge` subclasses are added to the CAC ontology (like Florida and Georgia), model Maryland counts as generic `StateCharge`:

| Press language | Modeling |
|---|---|
| Sexual solicitation of a minor | `StateCharge` + `uco-core:name` + `skos:altLabel` "Sexual Solicitation of a Minor" |
| Knowingly permitting sexual solicitation of a minor | separate `StateCharge` node |
| Held without bond | document on `BookingAction` / `CorrectionalFacility` description |
| Transported to detention center | `BookingAction` → `CorrectionalFacility` |

```python
charge = graph.add_node("kb:charge-1", "cacontology-legal-outcomes:StateCharge", {
    "uco-core:name": "Sexual Solicitation of a Minor",
    "uco-core:description": "Maryland state charge reported in press release.",
    "cacontology-legal-outcomes:chargeLevel": "felony",
    "cacontology-legal-outcomes:chargeCount": {
        "@type": "xsd:nonNegativeInteger", "@value": "1",
    },
})
graph.add_node("kb:suspect", "uco-identity:Person", {
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-1"}],
})
```

**Ontology gap:** Consider a change proposal for `MarylandStateCharge` subclasses mirroring `ComputerSeduceSolicitLure` patterns in Florida exemplars.

## Canonical pattern

```
CACInvestigation
  └── Related_To ──▶ CriminalCharge (one node per count)
        ├── Related_To ──▶ PleaAgreement (when entered)
        └── Related_To ──▶ SentencingOutcome
              └── Related_To ──▶ RegistrationRecord (when ordered)
```

## Modeling rules

- Link charges back to the **source investigation** and relevant **exploitation events** via `uco-core:Relationship` (`Related_To`), not only `chargedWith` on the suspect.
- Use **statute references** as structured nodes when statute numbers are known.
- Registry outcomes are separate auditable events — do not bury them in sentencing description text.
- Use typed literals for `chargeCount` (`xsd:nonNegativeInteger`).

## Validation

```bash
validate_graph("sentencing-outcome.jsonld", extensions=["cac"])
```

## Federal court prosecution graphs

For indictments and criminal complaints with **numbered federal counts** — single or multi-defendant, single or **multi-district parallel prosecution**, enterprise or production/possession cases — see [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md). That recipe covers relationship edges agents often omit: per-defendant `chargedWith`, indictment→charge links, prosecution→indictment bridges, multi-district charge→court assignment, forfeiture→device linkage, and enterprise-specific relator participants.

For **superseding indictments**, PACER docket exports, competency proceedings, and **government trial briefs**, see [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md).

For **§ 1591 child sex trafficking** with per-victim count bundles (solo operator or ring), see [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md).

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md)
- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
- [cac-tactical-undercover-operation.md](cac-tactical-undercover-operation.md)
- [event.md](event.md)
