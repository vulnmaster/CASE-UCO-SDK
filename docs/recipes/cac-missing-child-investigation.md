# Missing Child Investigations

> See [Recipe Index](INDEX.md) for all recipes.

Model general missing-child investigations using `cacontology:CACInvestigation`, with separate sourced reports, sightings, tracking steps, and recovery actions. Specialize as a stranger-abduction investigation only when the source establishes stranger abduction.

## Scope

**Layer 3 — Institutional workflow** with location and communications evidence support.

## Key classes

| Class | Role |
|---|---|
| `uco-observable:Observation` | Initial missing-person report observation |
| `cacontology-stranger-abduction:StrangerAbductionInvestigation` | Additional investigation type only when the source states stranger abduction |
| `case-investigation:InvestigativeAction` with a descriptive name | AMBER alert issuance when no dedicated CAC class exists |
| `case-investigation:InvestigativeAction` | Cell-site / GPS tracking steps |
| `cacontology:VictimRescueAction` | Successful victim recovery process |
| `cacontology:CACInvestigation` | Default general missing-child investigation container |
| `CellSiteFacet` / `LatLongCoordinatesFacet` | Location evidence |

## Canonical pattern

```
uco-observable:Observation (missing-person report)
  └── Related_To ──▶ cacontology:CACInvestigation
        ├── cacontology:hasStep ──▶ InvestigativeAction (CDR / cell-site / GPS)
        ├── cacontology:hasStep ──▶ InvestigativeAction (alert issuance, only if sourced)
        └── cacontology:hasStep ──▶ cacontology:VictimRescueAction
```

## Modeling rules

- Separate **report**, **alert**, **tracking**, and **recovery** into distinct actions.
- Link location evidence via `CellSiteFacet` or `LatLongCoordinatesFacet` — see [cell-site.md](cell-site.md).
- When rescue involves extraction from ongoing danger, chain to [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md).
- Never mint an abductor/offender `uco-identity:Person`, or any other party, that the source does not state. Missing status alone does not establish an abduction or an offender.

Default to `cacontology:CACInvestigation`; CAC 3.1.0 does not declare a dedicated
general missing-child investigation class. Add
`cacontology-stranger-abduction:StrangerAbductionInvestigation` only when the
source says it is a stranger abduction, and apply that type to the investigation.
Do not type the event as `cacontology-stranger-abduction:StrangerAbduction` while
upstream required shape properties remain undeclared. The `cac:missing-child`
profile omits the stranger-abduction shapes file for this reason; its other
modules still provide SHACL validation. The profile also loads the pinned gUFO
ontology for their temporal, participation, and part-whole properties. Forensics
and physical-evidence modules remain outside this profile.

## First fields investigators need

Record only what the source states, preserving uncertainty and attribution.
These patterns use declarations in the vendored CAC 3.1.0 and UCO/CASE
ontologies; a reference from a shape alone is not a term declaration.

| Field | Declared terms and current modeling gap |
|---|---|
| Last-seen time and place | **Gap:** no dedicated last-seen properties. Represent the sourced sighting as `uco-observable:Observation`, with `uco-action:startTime` and `uco-action:location` pointing to a `uco-location:Location`. Use `uco-core:name` equal to "observe" and explain the sighting in `uco-core:description`. Keep the sighting time/place separate from the later report intake time/place. |
| AMBER or endangered-missing alert issued? | **Gap:** no declared dedicated class or issued-status property for these alerts. Record an explicitly issued alert as `case-investigation:InvestigativeAction`, with `uco-core:name`, `uco-core:description`, and a sourced `uco-action:startTime`. If explicitly not issued, record that statement in the investigation description; absence of a statement means unknown, not false. |
| NCMEC case reference | **Gap:** no dedicated missing-child NCMEC reference property. Attach `uco-core:ExternalReference` through `uco-core:externalReference`, with the exact reference in `uco-core:externalIdentifier` and "NCMEC" in `uco-core:definingContext`; include `uco-core:referenceURL` only when supplied. CAC declares `cacontology:caseNumber` for agency/court case identifiers, but an external reference preserves which organization assigned this one. |
| Reporting party | **Gap:** no general missing-child reporting-party property. Describe the source's attribution using `uco-core:description`; for a separately modeled report-submission `case-investigation:InvestigativeAction`, use `uco-action:performer` for the stated submitter. CAC declares `cacontology-hotlines:reportedBy` and `cacontology-hotlines:ReporterRole` specifically for hotline reports; those terms are outside this profile and must not be applied to an ordinary missing-child report. |

The profile does not yet model the abduction response (AMBER activation, CART
deployment, search operations). The generic alert record above preserves the
source statement; a dedicated child-abduction response profile is planned for 1.35.0.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
})
investigation = graph.upsert_node("kb:example-missing-investigation", types=["cacontology:CACInvestigation"], properties={
    "uco-core:name": "Synthetic missing-child investigation",
})
report = graph.upsert_node("kb:example-missing-report", types=["uco-observable:Observation"], properties={
    "uco-core:name": "observe",
    "uco-core:description": "Synthetic report: Synthetic Child A is missing; circumstances are not stated.",
})
graph.create_relationship(report["@id"], investigation["@id"], "Related_To")
graph.write("missing-child.jsonld")
```

## Validation

Use the named missing-child profile so abduction, case-management, and
temporal terms are in the SHACL closure. The default `cac` press-release
subset will reject those terms as a **subset miss**, not as a missing
ontology concept.

```bash
# SDK / MCP
# validate_graph(..., extensions=["cac:missing-child"])
# CASE_UCO_EXTENSIONS=cac

case_validate --built-version case-1.5.0 \
  --ontology-graph ontology/cac/ontology/ontology/cacontology-core-spine.ttl \
  --ontology-graph ontology/cac/ontology/ontology/cacontology-stranger-abduction.ttl \
  examples/cac/t0-missing-child.jsonld
```

The T0 fixture `examples/cac/t0-missing-child.jsonld` is the conformance
target for `cac:missing-child`. Use `extensions=['cac:full']` only when
the complete CAC SPARQL shapes are safe for the installed case-utils.

## Related recipes

- [cell-site.md](cell-site.md)
- [location.md](location.md)
- [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md)
