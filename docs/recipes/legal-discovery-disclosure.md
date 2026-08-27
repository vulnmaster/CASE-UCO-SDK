# Criminal Discovery and Disclosure Obligations

> See [Recipe Index](INDEX.md) for all recipes.

Model sourced *Brady*, *Giglio*, *Jencks*, and Rule 16 disclosure duties
with `legalproc` so prosecutors can query what was disclosed, and to which
evidence IRI. Do not infer an obligation from the existence of exam notes.

Validated against `examples/caselinker-icac-remodel/discovery-disclosure.jsonld`
and `extensions/legalproc/legalproc-exemplar.ttl`.

`check_existing_proposals("Brady Giglio Jencks discovery disclosure")`
returned no UCO/CASE/CAC hits when this recipe was added (#132).

## When to use this recipe

- A discovery certificate, docket entry, or prosecutor log names a
  disclosure duty or production
- A suppression motion appears on a PACER docket
- You are remodeling CaseLinker graphs that have statements or exam objects
  but no disclosure status

Use [legal-process-modeling.md](legal-process-modeling.md) for charges and
sentences. Use [caselinker-icac-remodel.md](caselinker-icac-remodel.md) for
CaseLinker charge typing.

## Classes and properties

| Term | Role |
|---|---|
| `legalproc:DisclosureObligation` | Sourced duty (`disclosureKind`, `disclosureStatus`, `disclosureSourceCitation`, `concernsEvidence`) |
| `legalproc:DiscoveryProduction` | Sourced production that `satisfiesObligation` |
| `legalproc:SuppressionMotion` | Docketed motion (`proceedingType` `suppression-motion`) |
| `legalproc:disclosureKind` | Closed: `brady`, `giglio`, `jencks`, `rule-16`, `other` |
| `legalproc:disclosureStatus` | Closed: `not-reviewed`, `disclosed`, `withheld-pending-review` |

SHACL requires a source citation and an evidence IRI. An obligation without
`disclosureSourceCitation` does not conform.

## Canonical pattern

```
FederalCharge
DisclosureObligation
  ├── legalproc:disclosureKind jencks
  ├── legalproc:disclosureSourceCitation "Discovery certificate, Doc 40"
  ├── legalproc:concernsEvidence ──▶ interview memorandum
  └── legalproc:concernsCharge ──▶ FederalCharge
DiscoveryProduction
  └── legalproc:satisfiesObligation ──▶ DisclosureObligation
```

## Anti-patterns

- Labeling unlabeled lab notes as Brady
- `disclosureStatus` `disclosed` without a production source
- CaseLinker `admissionTheme` as a stand-in for Giglio

## Related

- [legal-process-modeling.md](legal-process-modeling.md)
- [caselinker-icac-remodel.md](caselinker-icac-remodel.md)
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md)
