# Proposing Changes to CASE/UCO

> See [Recipe Index](INDEX.md) for all recipes.

When the CASE/UCO ontology doesn't have a class, facet, or property for the concept you need to model, you can draft a **change proposal** — a structured request for the ontology committees to consider adding or modifying a concept in a future specification release.

This recipe covers the full workflow: confirming the gap, checking for existing proposals, determining the right target repository and release, drafting the proposal with testable example data, validating and testing before submission, and creating a local extension to unblock your work.

## When to use this recipe

- **Explicit request**: You know you need a concept that doesn't exist (e.g., "there's no facet for drone telemetry data")
- **Gap detected during modeling**: `search_classes` and `find_classes_for_domain` return no adequate match for what you're trying to model
- **Agent-suggested**: While helping model data, the agent identifies that no existing class covers the concept and proactively suggests drafting a proposal
- **Rejected by concept coverage**: `validate_graph` returned `conforms: False` with an `undeclared_concepts` list — the graph uses a class or property that no supported ontology declares. Do not invent terms or disable the check; file a proposal (this recipe) and/or declare the term in an extension ontology ([extensions recipe](extensions.md)) so validation passes.

## Which tracker?

| Concept namespace | Target repository |
|---|---|
| `uco-*` (general cyber-domain) | [ucoProject/UCO](https://github.com/ucoProject/UCO/issues) |
| `case-*` (investigation-specific) | [casework/CASE](https://github.com/casework/CASE/issues) |
| `cacontology*` (crimes against children) | [Project-VIC-International/CAC-Ontology](https://github.com/Project-VIC-International/CAC-Ontology/issues) |

`check_existing_proposals` searches all three by default. Precedent CAC proposals filed from this SDK: [#40](https://github.com/Project-VIC-International/CAC-Ontology/issues/40) (legal-outcomes charging/sentencing properties) and [#41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41) (core case-identification properties) — both backed locally by `ontology/cac/local/cacontology-sdk-pending.ttl` until they land upstream.

## Key tools

| Tool | Role |
|---|---|
| `search_classes` | Verify the gap — search by keyword to confirm no existing class fits |
| `get_class_details` | Inspect near-matches to confirm they don't cover the concept |
| `find_classes_for_domain` | Check if the concept is already mapped under a different name |
| `check_existing_proposals` | Search open GitHub issues in UCO and CASE for prior proposals |
| `draft_change_proposal` | Generate the filled-in proposal markdown, example graph, and SPARQL queries |

---

## Step 1: Confirm the gap

Before drafting a proposal, thoroughly verify that no existing class covers the concept. Near-misses are common — the ontology may model the concept under a different name or as a property on an existing class.

<details open><summary>Python — confirming a gap</summary>

```python
from case_uco.registry import search, get_class

# Search by several keywords related to the concept
results = search("drone")
print(f"Found {len(results)} results for 'drone'")
for r in results:
    print(f"  {r['name']:30s} {r['module']}")

# Try related terms
for term in ["uav", "unmanned", "aerial", "flight", "telemetry"]:
    hits = search(term)
    if hits:
        print(f"\n'{term}' matched:")
        for h in hits:
            print(f"  {h['name']:30s} {h['module']}")

# Inspect near-matches in detail
info = get_class("DeviceFacet")
print(f"\nDeviceFacet properties:")
for prop in info["properties"]:
    print(f"  {prop['name']:20s} {prop['type']}")
```

</details>

<details><summary>MCP — confirming a gap</summary>

```
1. search_classes("drone")          → no results
2. search_classes("uav")            → no results
3. search_classes("telemetry")      → no results
4. find_classes_for_domain("drone forensics")  → no task templates
5. get_class_details("DeviceFacet") → review properties, confirm none cover flight data
```

The gap is confirmed: no existing class models UAV/drone-specific telemetry data.

</details>

---

## Step 2: Check existing proposals

**This step is critical for proposal quality.** Before drafting a new proposal, search the open issues in both the UCO and CASE repositories. Someone may have already proposed the concept, or a related proposal may be in progress. Finding related issues provides essential context — for example, discovering a prerequisite proposal (like UCO #535 "Add Qualities") can change the entire design of your proposal.

<details open><summary>MCP — checking existing proposals</summary>

```
check_existing_proposals("drone telemetry")
```

Possible outcomes:

- **Exact match found**: "UCO Issue #700 proposes a DroneTelemetryFacet — consider commenting on that issue instead of creating a duplicate."
- **Partial match found**: "CASE Issue #190 discusses aerial surveillance evidence, which overlaps with drone telemetry. Your proposal should reference it."
- **No match found**: Proceed to Step 3.
- **GitHub unavailable**: Proceed with local drafting, but search the issue trackers manually before submitting: [UCO issues](https://github.com/ucoProject/UCO/issues), [CASE issues](https://github.com/casework/CASE/issues).

</details>

---

## Step 3: Determine UCO vs. CASE and target release

### Target repository

The concept's scope determines which repository receives the proposal:

| Scope | Target | Repository | Examples |
|---|---|---|---|
| General cyber-observable, identity, action, or data structure with utility beyond investigation | **UCO** | [ucoProject/UCO](https://github.com/ucoProject/UCO/issues/new) | New device facet, new observable type, new action property |
| Specific to the investigation process itself | **CASE** | [casework/CASE](https://github.com/casework/CASE/issues/new) | New investigator role, new case metadata, investigation workflow concepts |

**Decision logic:**

1. Is this concept specific to the process of conducting an investigation (roles, exhibits, authorization, case metadata, investigative workflows)?
   - **Yes** → **CASE**
2. Is this a general cyber-observable, identity, tool, action, location, or data structure that has utility across the broader cyber domain?
   - **Yes** → **UCO**
3. **Unsure?** → Ask the developer. Explain the distinction and let them decide.

### Target release

Every change proposal must specify which CASE/UCO release it targets. Check the current state of the ontology branches:

| Branch | Version | When to target |
|--------|---------|----------------|
| `main` | 1.5.0 | Released. CASE and UCO 1.5.0 both shipped; nothing new targets this. |
| `develop` | next backward-compatible release | Default for most proposals. Changes that are backward-compatible additions. |
| `develop-2.0.0` | 2.0.0 | For proposals that require breaking changes or major restructuring. |

If unsure, target `develop`. Read the version off the branch rather than
assuming it — after the 1.5.0 release `develop` still carried
`owl:versionIRI core:1.5.0`, so the next minor had not been opened yet:

```bash
git -C ontology/UCO show origin/develop:ontology/uco/core/core.ttl | grep versionIRI
```

The ontology committee may reassign the proposal to a different milestone
during review.

---

## Step 4: Draft the proposal

Use the `draft_change_proposal` MCP tool or manually fill in the [change proposal template](../templates/change-proposal-template.md). The tool generates three files:

1. **`<slug>.md`** — the filled-in proposal markdown
2. **`<slug>.jsonld`** — an example JSON-LD graph for validation and SPARQL testing
3. **`<slug>.sparql`** — SPARQL queries matching the competency questions

<details open><summary>MCP — drafting a proposal</summary>

```
draft_change_proposal(
    concept="Drone telemetry facet",
    description="No existing facet captures UAV flight telemetry data. Investigators "
                "increasingly encounter drones in cases involving surveillance, smuggling, "
                "and unauthorized airspace intrusion. Flight logs contain altitude, speed, "
                "GPS coordinates, flight mode, battery level, and gimbal orientation that "
                "are critical to reconstructing drone activity.",
    scenario="A law enforcement agency seizes a DJI Mavic drone from a suspect. The "
             "forensic examiner extracts the flight log using DJI Assistant and needs to "
             "model the telemetry data points — altitude, speed, coordinates, flight mode, "
             "and timestamps — alongside the device metadata already captured by DeviceFacet.",
    proposed_classes=[
        {
            "name": "DroneTelemetryFacet",
            "type": "Facet",
            "parent": "uco-core:Facet",
            "properties": [
                {"name": "altitude", "type": "xsd:decimal", "description": "Altitude in meters above ground level"},
                {"name": "groundSpeed", "type": "xsd:decimal", "description": "Ground speed in m/s"},
                {"name": "flightMode", "type": "xsd:string", "description": "Flight mode (GPS, ATTI, Sport, etc.)"},
                {"name": "batteryLevel", "type": "xsd:integer", "description": "Battery percentage at time of reading"},
                {"name": "gimbalPitch", "type": "xsd:decimal", "description": "Camera gimbal pitch angle in degrees"},
                {"name": "homeLatitude", "type": "xsd:decimal", "description": "Home point latitude"},
                {"name": "homeLongitude", "type": "xsd:decimal", "description": "Home point longitude"},
            ],
        }
    ],
    target_repo="UCO",
    target_release="1.5.0",
)
```

This generates three files in `change_proposals/`:
- `drone-telemetry-facet.md` — the proposal
- `drone-telemetry-facet.jsonld` — example instance data
- `drone-telemetry-facet.sparql` — SPARQL competency queries

</details>

### Writing each section

**Target release**: Specify the CASE/UCO version this proposal targets (e.g., 1.5.0, 2.0.0). The ontology committee uses this to assign the proposal to the correct milestone.

**Background**: Explain what you were trying to model, why current classes are insufficient, and who benefits from the addition. Answer: "What do we achieve for whom and why does that matter?"

**Requirements**: One numbered requirement per proposed change. Be specific:
- "Define a new `DroneTelemetryFacet` class as a subclass of `uco-core:Facet`"
- "Add properties for altitude, ground speed, flight mode, battery level, gimbal orientation, and home coordinates"

**Risk / Benefit analysis**: List concrete benefits (new modeling capability, interoperability with drone forensic tools). For risks, consider backward compatibility, overlap with existing classes, and maintenance burden. If no risks are known, state: "The submitter is unaware of risks associated with this change."

**Competencies demonstrated**: This section is critical — it proves the proposal adds real value. Include:
1. A concrete scenario with enough detail to construct ground truth
2. At least one competency question the ontology can answer after the change that it couldn't before
3. The expected result
4. A draft SPARQL query (will be tested in Step 6)

**Example instance data**: A concrete JSON-LD graph showing the proposed concept in use. This is what the submitter eventually wants to build and share with others. It must be complete enough to support the SPARQL queries in the Competencies section.

**Related proposals and references**: List any related GitHub issues, prior proposals, external ontologies, or specifications that informed the design. This helps reviewers understand the broader context and dependencies. Include links found during Step 2.

**Solution suggestion**: Enumerate the concrete OWL changes (new class, new properties, new shapes) and any test additions.

---

## Step 5: Create example data and extension ontology

The `draft_change_proposal` tool auto-generates a starter example graph at `change_proposals/<slug>.jsonld`. Expand this with realistic data that:

- Exercises all proposed classes and properties
- Supports the SPARQL queries in the Competencies section
- Includes both positive and negative ground truth where applicable
- Represents the kind of graph the submitter eventually wants to build and share

### JSON-LD requirements for validation

Two requirements are commonly missed and will cause `case_validate` to report `Conforms: False`:

1. **Facets MUST have IRIs (not blank nodes).** The `hasFacet` SHACL shape requires `sh:nodeKind sh:IRI`. Every facet object inside a `uco-core:hasFacet` array must include an `@id` property. Convention: use the parent's `@id` with a `-facet` suffix (e.g., `kb:addr-1` → `kb:addr-1-facet`).

   <!-- recipe-lint: ignore-start proposed-term -- The snippet demonstrates terms that the change proposal would declare; they are intentionally unavailable beforehand. -->
   ```json
   "uco-core:hasFacet": [
     {
       "@id": "kb:observable-1-facet",
       "@type": "proposed:MyNewFacet",
       "proposed:someProperty": "value"
     }
   ]
   ```
   <!-- recipe-lint: ignore-end proposed-term -->

2. **The `.jsonld` and the JSON-LD block embedded in the `.md` must stay in sync.** After fixing validation issues in the `.jsonld`, update the embedded example in the proposal markdown to match. Reviewers read the `.md`; automated tests run against the `.jsonld`.

### Extension ontology (`.ttl`) — required for new Facet subclasses

If the proposal introduces new classes that are subclasses of existing UCO/CASE classes (e.g., a new Facet), you **must** create a `<slug>.ttl` file declaring the `rdfs:subClassOf` relationship. Without this, `case_validate` cannot infer that your proposed type satisfies the `sh:class uco-core:Facet` constraint, and validation will fail.

<!-- recipe-lint: ignore-start proposed-term -- The Turtle example declares the proposed class that validation will load as a local ontology graph. -->
```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix proposed: <http://example.org/ontology/proposed/> .

proposed:MyNewFacet
    a owl:Class ;
    rdfs:subClassOf uco-core:Facet ;
    rdfs:label "MyNewFacet"@en ;
    rdfs:comment "Description of the facet."@en .
```
<!-- recipe-lint: ignore-end proposed-term -->

This file is **not optional** — it is required for any proposal that introduces Facet or UcoObject subclasses. The Makefile `validate-proposal` target automatically includes it when present.

<details open><summary>Python — building a richer example graph</summary>

<!-- recipe-lint: ignore-start proposed-term -- This example instantiates terms declared by the companion proposal ontology. -->
```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.tool import Tool
from case_uco.uco.identity import Identity
from case_uco.uco.observable import ObservableObject, DeviceFacet, FileFacet
from case_uco.uco.core import Relationship
import json

graph = CASEGraph(extra_context={
    "proposed": "http://example.org/ontology/proposed/",
})

investigation = graph.create(Investigation, name="Drone Surveillance Case 2025-042")
tool = graph.create(Tool, name="DJI Assistant", version="2.1.2")

dji = graph.create(Identity, name="DJI")

drone = graph.create(ObservableObject, has_facet=[
    DeviceFacet(
        device_type="UAV",
        manufacturer=dji,
        model="Mavic 3 Pro",
        serial_number="1ZNBJ...",
    ),
])

# The telemetry facet doesn't exist yet — model it as raw JSON-LD
# and load it into the graph via graph.load().
telemetry_data = {
    "@id": "kb:drone-1-telemetry",
    "@type": "proposed:DroneTelemetryFacet",
    "proposed:altitude": 120.5,
    "proposed:groundSpeed": 15.2,
    "proposed:flightMode": "GPS",
    "proposed:batteryLevel": 73,
    "proposed:gimbalPitch": -45.0,
    "proposed:homeLatitude": 38.8977,
    "proposed:homeLongitude": -77.0365,
}
graph.load(json.dumps({
    "@context": dict(graph._context, proposed="http://example.org/ontology/proposed/"),
    "@graph": [telemetry_data],
}))

graph.write("change_proposals/drone-telemetry-facet.jsonld")
```
<!-- recipe-lint: ignore-end proposed-term -->

</details>

---

## Step 6: Test before submission

**This step is required — a proposal is not finished until all tests pass.** The ontology committee expects proposals to include evidence that the SPARQL queries and example data have been tested prior to submission. Do not present a proposal as complete if testing has not been run or has failures.

### Run all proposal tests

```bash
make test-proposal PROPOSAL=drone-telemetry-facet
```

This runs two checks:

1. **Graph validation** — validates the example `.jsonld` against the current CASE/UCO release using `case_validate` with `--inference rdfs --allow-info`. If a local extension `.ttl` and shapes file exist, they are automatically included via `--ontology-graph`.
2. **SPARQL query testing** — executes each query in the `.sparql` file against the example graph and reports whether results were returned.

Both checks must pass. If either fails, fix the issues and re-run.

### Understanding validation flags

The `validate-proposal` Makefile target uses these flags automatically:

- **`--inference rdfs`** — Required when proposed classes are `rdfs:subClassOf` existing UCO/CASE classes (e.g., Facet, UcoObject). Without this, SHACL cannot infer that the proposed facet satisfies the `sh:class uco-core:Facet` constraint.
- **`--allow-info`** — Allows informational results (UUID IRI suggestions, vocabulary hints) without causing a non-zero exit code. These are advisory, not errors.
- **`--ontology-graph <slug>.ttl`** — Automatically included when the file exists. Declares your proposed classes so the validator knows their type hierarchy.

### Run tests individually

```bash
# Validate the example graph
make validate-proposal PROPOSAL=drone-telemetry-facet

# Test SPARQL queries
make sparql-test-proposal PROPOSAL=drone-telemetry-facet
```

### Common validation failures and fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| `NodeKindConstraintComponent: Value is not of Node Kind sh:IRI` | Facet objects are blank nodes (missing `@id`) | Add `"@id": "kb:<parent>-facet"` to each facet object |
| `ClassConstraintComponent: Value does not have class uco-core:Facet` | No `.ttl` declaring `rdfs:subClassOf` | Create `<slug>.ttl` with the class hierarchy (see Step 5) |
| `ClassConstraintComponent` despite `.ttl` present | Missing `--inference rdfs` flag | Ensure the Makefile target passes `--inference rdfs` |
| Exit code 1 with only informational results | Missing `--allow-info` flag | Ensure the Makefile target passes `--allow-info` |

### Test extensions against multiple CASE/UCO branches

If you've created a local extension ontology (`.ttl` + shapes), test it against multiple CASE/UCO branches to help the ontology committee assess compatibility:

```bash
# Test against all three branches: main (v1.5.0), develop, develop-2.0.0 (v2.0.0)
make test-extension-compat \
  EXT_TTL=change_proposals/drone-telemetry.ttl \
  EXT_SHAPES=change_proposals/drone-telemetry-shapes.ttl \
  EXT_DATA=change_proposals/drone-telemetry-facet.jsonld

# Or test against individual branches
make test-extension-main EXT_TTL=... EXT_DATA=...
make test-extension-develop EXT_TTL=... EXT_DATA=...
make test-extension-develop2 EXT_TTL=... EXT_DATA=...
```

### Update the proposal with test results

After running tests, update the **Pre-submission testing** section of the proposal markdown with:

1. Whether each SPARQL query was tested and returned expected results
2. The `case_validate` output (Conforms: True/False)
3. Any informational warnings and their disposition
4. Any unresolved issues or known failures

The proposal should state that tests have been run. If all tests pass, write "No unresolved issues." If issues remain, document them — this transparency helps the committee.

---

## Step 7: Create a local extension (optional)

If you need typed classes immediately rather than raw JSON-LD, create a local extension ontology and scaffold typed classes. See the [Working with Extensions](extensions.md) recipe for the full workflow.

This local extension can be referenced in the change proposal's "Solution suggestion" section as a working prototype.

```bash
# After defining your extension TTL files:
case-uco-generate scaffold \
  --extension extensions/proposed/proposed.ttl extensions/proposed/proposed-shapes.ttl \
  --output-dir my_project/
```

When the concept is officially added to CASE/UCO in a future release, retire the local extension and switch to the SDK's built-in class.

---

## Submitting the proposal

A proposal is **not ready for submission** until `make test-proposal PROPOSAL=<slug>` passes and the Pre-submission testing section documents the results. Once the draft is reviewed, tested, and refined:

1. Verify `make test-proposal PROPOSAL=<slug>` exits cleanly (graph validation conforms, all SPARQL queries return expected results)
2. Confirm the Pre-submission testing section in the `.md` reflects the actual test output — do not leave placeholder Yes/No values
3. Verify the JSON-LD block in the `.md` matches the tested `.jsonld` file
4. Determine the target repository (UCO or CASE) — see Step 3
5. Open a new issue in the appropriate GitHub repository:
   - **UCO**: https://github.com/ucoProject/UCO/issues/new
   - **CASE**: https://github.com/casework/CASE/issues/new
5. Copy the proposal markdown into the issue body
6. Attach or link the example `.jsonld` file
7. Add the label "Change Proposal" if available
8. If you included example JSON-LD, add the permission statement: "I am fine with my examples being transcribed and credited"

The ontology committee will review the proposal, assign it to a milestone, and coordinate implementation.

## Proposal file conventions

When `draft_change_proposal` generates a proposal, it creates files following this naming convention:

```
change_proposals/
├── <slug>.md              # The proposal markdown
├── <slug>.jsonld           # Example instance data (JSON-LD graph)
├── <slug>.sparql           # SPARQL competency queries
├── <slug>.ttl              # Extension ontology (optional, hand-written)
└── <slug>-shapes.ttl       # SHACL shapes (optional, hand-written)
```

The Makefile `test-proposal` target looks for all of these by convention. Only the `.md` is required; the others enable automated testing.
