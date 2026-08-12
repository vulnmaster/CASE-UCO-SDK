# Investigator Work Package Profile 1.0

This profile gives Project VIC ecosystem services a stable envelope for
exchanging investigator work while keeping the semantic payload in canonical
CASE/UCO, CAC, and SOLVE-IT graphs. It does **not** define a new ontology.

## Contract

A work package contains:

- `profile`: fixed identifier `project-vic-investigator-work-package`;
- `profile_version`: semantic version of this envelope;
- `work_package_id`: stable URI identifying this package;
- `case_graph`: a JSON-LD graph containing the authoritative investigation,
  evidence, actions, authorizations, provenance, findings, and relationships;
- `workflow`: orchestration metadata whose inputs, outputs, approvals, tool
  calls, and citations point to nodes in `case_graph`;
- `artifacts`: immutable source and derived artifact references, with hashes;
- `assertions`: explicit source-fact, tool-derived, or analyst-hypothesis
  classification, confidence, and supporting graph-node references;
- `audit`: append-only event references for downstream audit systems.

The envelope is validated by `work-package.schema.json`. Semantic validation
of `case_graph` remains CASE/UCO SHACL validation. The JSON-LD and Turtle
fixtures describe the same synthetic T0 workflow.

## Canonical mapping

| Concern | Canonical model |
| --- | --- |
| Case context | `case-investigation:Investigation` |
| Work execution | `case-investigation:InvestigativeAction`; SOLVE-IT `SolveitInvestigativeAction`, `usedTechnique`, and `appliedMitigation` when applicable |
| Authority | `case-investigation:Authorization`; CAC authorization subclasses such as `JurisdictionalWarrant` when the facts warrant them |
| Inputs and outputs | `uco-action:object`, `uco-action:result` |
| Chain of custody/provenance | CASE `ProvenanceRecord`, relationships, and explicit action performer/time/tool links |
| Immutable artifacts | UCO observable objects/facets and hash facets; envelope hashes protect transfer integrity |
| Tool provenance | `uco-tool:Tool`, action instrument/performer links, and SOLVE-IT technique identifiers |
| Findings and human decisions | Existing CASE/UCO assertion, identity, role, and relationship terms where applicable; envelope `assertions` records epistemic status without minting RDF terms |
| Timeline/geospatial observations | UCO observable/location/time classes and source relationships |
| Reports/exhibits | UCO document/content observables linked as action results and related to their sources |

## Deliberate gaps

The current ontologies do not provide one universal class for an ecosystem
work order, LLM prompt/plan/approval/tool-call transcript, court exhibit
bundle, or a uniform epistemic classification of every graph assertion. These
remain envelope metadata. Consumers must not emit the envelope keys as RDF
properties. If semantic interoperability is required for them, draft and
validate upstream change proposals rather than minting private vocabulary.

## Evolution rules

- Add optional fields in minor versions; never change existing meanings.
- Require a new major version for removed/renamed fields or tighter required
  fields.
- Preserve unknown optional fields when relaying a package.
- Treat `case_graph` node IRIs and artifact SHA-256 values as immutable.
- Never place secrets, evidence bytes, or operational case data in the
  envelope; use controlled artifact references.

## Validation

```bash
python -m jsonschema -i docs/work-package/example.work-package.json \
  docs/work-package/work-package.schema.json
case_validate --built-version case-1.4.0 \
  docs/work-package/example.case.jsonld
case_validate --built-version case-1.4.0 \
  docs/work-package/example.case.ttl
```

The fixtures are T0 synthetic: names, identifiers, hashes, and events are
fabricated and do not resemble a real investigation.
