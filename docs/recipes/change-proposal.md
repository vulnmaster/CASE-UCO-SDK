# Proposing Changes to CASE/UCO

> See [Recipe Index](INDEX.md) for all recipes.

When the CASE/UCO ontology doesn't have a class, facet, or property for the concept you need to model, you can draft a **change proposal** — a structured request for the ontology committees to consider adding or modifying a concept in a future specification release.

This recipe covers the full workflow: confirming the gap, checking for existing proposals, determining the right target repository, drafting the proposal, and creating a local extension to unblock your work.

## When to use this recipe

- **Explicit request**: You know you need a concept that doesn't exist (e.g., "there's no facet for drone telemetry data")
- **Gap detected during modeling**: `search_classes` and `find_classes_for_domain` return no adequate match for what you're trying to model
- **Agent-suggested**: While helping model data, the agent identifies that no existing class covers the concept and proactively suggests drafting a proposal

## Key tools

| Tool | Role |
|---|---|
| `search_classes` | Verify the gap — search by keyword to confirm no existing class fits |
| `get_class_details` | Inspect near-matches to confirm they don't cover the concept |
| `find_classes_for_domain` | Check if the concept is already mapped under a different name |
| `check_existing_proposals` | Search open GitHub issues in UCO and CASE for prior proposals |
| `draft_change_proposal` | Generate the filled-in proposal markdown file |

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

Before drafting a new proposal, search the open issues in both the UCO and CASE repositories. Someone may have already proposed the concept, or a related proposal may be in progress.

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

## Step 3: Determine UCO vs. CASE

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

**Examples:**

- "A facet for drone telemetry data (altitude, flight mode, GPS)" → **UCO** — it describes an observable device's data, useful beyond investigations
- "A role class for forensic lab technicians" → **CASE** — it's specific to the investigation process
- "A facet for cryptocurrency wallet data" → **UCO** — it describes observable financial data
- "A class for keyword search configuration used during examination" → **CASE** — it's part of investigative methodology

---

## Step 4: Draft the proposal

Use the `draft_change_proposal` MCP tool or manually fill in the [change proposal template](../templates/change-proposal-template.md).

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
            "parent": "uco-observable:Facet",
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
)
```

This generates a file at `change_proposals/drone-telemetry-facet.md` with the filled-in template.

</details>

### Writing each section

**Background**: Explain what you were trying to model, why current classes are insufficient, and who benefits from the addition. Answer: "What do we achieve for whom and why does that matter?"

**Requirements**: One numbered requirement per proposed change. Be specific:
- "Define a new `DroneTelemetryFacet` class as a subclass of `uco-observable:Facet`"
- "Add properties for altitude, ground speed, flight mode, battery level, gimbal orientation, and home coordinates"

**Risk / Benefit analysis**: List concrete benefits (new modeling capability, interoperability with drone forensic tools). For risks, consider backward compatibility, overlap with existing classes, and maintenance burden. If no risks are known, state: "The submitter is unaware of risks associated with this change."

**Competencies demonstrated**: This section is critical — it proves the proposal adds real value. Include:
1. A concrete scenario with enough detail to construct ground truth
2. At least one competency question the ontology can answer after the change that it couldn't before
3. The expected result
4. Optionally, a draft SPARQL query

**Solution suggestion**: Enumerate the concrete OWL changes (new class, new properties, new shapes) and any test additions.

---

## Step 5: Create example data

Create example JSON-LD showing what the proposed concept would look like in use. This serves two purposes: it unblocks your immediate work via a local extension, and it provides concrete instance data for the proposal.

<details open><summary>Python — example with local extension context</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.tool import Tool
from case_uco.uco.observable import ObservableObject, DeviceFacet, FileFacet
from case_uco.uco.core import Relationship

graph = CASEGraph(extra_context={
    "proposed": "http://example.org/ontology/proposed/",
})

investigation = graph.create(Investigation, name="Drone Surveillance Case 2025-042")
tool = graph.create(Tool, name="DJI Assistant", version="2.1.2")

drone = graph.create(ObservableObject, has_facet=[
    DeviceFacet(
        device_type="UAV",
        manufacturer="DJI",
        model="Mavic 3 Pro",
        serial="1ZNBJ...",
    ),
])

# The telemetry facet doesn't exist yet — model it as raw JSON-LD
# to demonstrate the proposed class
telemetry_data = {
    "@type": "proposed:DroneTelemetryFacet",
    "proposed:altitude": 120.5,
    "proposed:groundSpeed": 15.2,
    "proposed:flightMode": "GPS",
    "proposed:batteryLevel": 73,
    "proposed:gimbalPitch": -45.0,
    "proposed:homeLatitude": 38.8977,
    "proposed:homeLongitude": -77.0365,
}

graph.write("drone_evidence.jsonld")
```

</details>

<details><summary>Draft SPARQL — competency query</summary>

```sparql
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/>

# CQ 1.1: What was the drone's altitude and flight mode at each telemetry point?
SELECT ?drone ?altitude ?flightMode ?timestamp
WHERE {
    ?drone a uco-observable:ObservableObject ;
           uco-core:hasFacet ?telemetry .
    ?telemetry a proposed:DroneTelemetryFacet ;
               proposed:altitude ?altitude ;
               proposed:flightMode ?flightMode .
    OPTIONAL { ?telemetry uco-core:objectCreatedTime ?timestamp }
}
ORDER BY ?timestamp

# CQ 1.2: Which drones flew above 400 feet (121.92m) — the FAA regulatory limit?
SELECT ?drone ?maxAltitude
WHERE {
    ?drone a uco-observable:ObservableObject ;
           uco-core:hasFacet ?devFacet ;
           uco-core:hasFacet ?telemetry .
    ?devFacet a uco-observable:DeviceFacet ;
              uco-observable:deviceType "UAV" .
    ?telemetry a proposed:DroneTelemetryFacet ;
               proposed:altitude ?maxAltitude .
    FILTER(?maxAltitude > 121.92)
}
```

</details>

---

## Step 6: Create a local extension (optional)

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

Once the draft in `change_proposals/` is reviewed and refined:

1. Determine the target repository (UCO or CASE) — see Step 3
2. Open a new issue in the appropriate GitHub repository:
   - **UCO**: https://github.com/ucoProject/UCO/issues/new
   - **CASE**: https://github.com/casework/CASE/issues/new
3. Copy the proposal markdown into the issue body
4. Add the label "Change Proposal" if available
5. If you included example JSON-LD, add the permission statement: "I am fine with my examples being transcribed and credited"

The ontology committee will review the proposal, assign it to a milestone, and coordinate implementation.
