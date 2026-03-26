# Chain of Custody

> See [Recipe Index](INDEX.md) for all recipes.

Model evidence provenance as a series of custody events. Every chain of custody is different — the number of steps, people, locations, and handoffs varies by case. **Derive the steps from the source document or user input, not from this recipe.** This recipe defines composable building blocks, not a fixed sequence.

All values shown as `"..."` are placeholders. **Never copy placeholder values into generated output.** Populate every field from the actual source.

## How to build a custody chain

Each custody event is one `InvestigativeAction`. The `performer`/`participant` convention encodes roles:

- `performer` — the person *acting* (seizing, releasing, receiving, examining, storing)
- `participant` — the other party involved in a handoff (if any)
- `object` — the evidence item(s) affected
- `location` — where the event occurred (one location per action, not two)
- `instrument` — tool used (for hashing, imaging, analysis)
- `result` — output produced (forensic image, hash result, analysis report)

Create one `InvestigativeAction` per event that appears in the source. A simple case might have 3 steps; a complex multi-agency investigation might have 20. The building blocks below can be used in any order, repeated as many times as needed, or omitted entirely if they don't apply.

## Building blocks

These are the common event types. Mix, match, repeat, and extend based on what actually happened:

| Event type | `performer` | `participant` | Key fields | When to use |
|---|---|---|---|---|
| **Collection/seizure** | Collecting agent | — | `object`, `location`, `description` (seizure details, packaging/seal IDs) | Evidence is first taken into custody |
| **Imaging/hashing** | Imaging agent | — | `object` (source), `result` (image ObservableObject), `instrument` (tool) | A forensic image or hash is created |
| **Custody release** | Releasing custodian | Receiving party | `object`, `location`, `description` (seal condition) | Evidence leaves one person's custody |
| **Custody receipt** | Receiving custodian | Delivering party | `object`, `location`, `description` (seal condition) | Evidence enters another person's custody |
| **Hash verification** | Verifying person | — | `object` (image), `result` (verification hash), `instrument` (tool) | A hash is recomputed to confirm integrity |
| **Evidence storage** | Storing custodian | — | `object`, `location`, `description` (locker ID, shelf, access log) | Evidence is placed in a vault/locker |
| **Evidence checkout** | Retrieving custodian | — | `object`, `location`, `description` (reason, authorization) | Evidence is retrieved from storage |
| **Examination/analysis** | Examiner | — | `object`, `instrument` (forensic tool), `result` (findings) | Forensic work is performed on evidence |
| **Re-seal** | Examiner | — | `object`, `description` (new seal ID) | Evidence is repackaged after examination |
| **Return/disposal** | Releasing custodian | Receiving party | `object`, `description` (disposition, authorization) | Evidence is returned to owner or destroyed |

For event types not listed here, create an `InvestigativeAction` with a descriptive `name` and use the same `performer`/`participant`/`object`/`location` convention.

## Modeling rules

- **Derive steps from the source.** Read the custody form, report, or user description and create one `InvestigativeAction` per event recorded. Do not add steps that are not in the source. Do not omit steps that are.
- **Hash the forensic image, not the device.** A device is never "hashed" — a specific E01 image, logical extraction, or partition is. Model the image as its own `ObservableObject` with `FileFacet` + `ContentDataFacet`.
- **One action per custody transition.** Never model a transfer as one action with two locations — that loses directionality. Separate release and receipt.
- **Record the hashing tool.** Use `instrument` on hashing/imaging actions to link the `Tool` (name + version).
- **Use timezone-aware timestamps** when time zone information is available in the source.
- **Capture seal/packaging identifiers in `description`.** Bag numbers, seal IDs, and condition notes belong in action descriptions.
- **Multiple evidence items**: create one `ProvenanceRecord` per item, each with its own `exhibit_number` and the subset of actions that apply to that item.

## Connecting the graph

A chain-of-custody graph should not have disconnected nodes. Use these relationships to tie everything together explicitly:

**Investigation → its contents.** `Investigation` inherits `object` from `ContextualCompilation`. Populate it with the evidence items, actions, and provenance records so the investigation is not just a free-floating label:

```python
investigation = graph.create(Investigation,
    name="...",
    description=["..."],
    object=[evidence, provenance, action_collect, action_image, ...],
)
```

Because the `object` list references objects that must already exist, either create the `Investigation` last (after all actions and provenance records) or build the list incrementally.

**Custody release ↔ receipt pairing.** The `performer`/`participant` convention works for queryable graphs but relies on action naming to distinguish release from receipt. For stronger semantics, add `Relationship` objects that make the custodial edges explicit:

```python
from case_uco.uco.core import Relationship

graph.create(Relationship,
    source=[action_release], target=action_receipt,
    kind_of_relationship="custody-transfer",
    is_directional=True,
)
```

This gives graph consumers a typed, queryable edge between the two halves of a handoff without relying on name matching.

**Provenance record organization.** `ProvenanceRecord.object` is a flat list, but you can make it more useful to consumers by grouping entries consistently. Recommended order: primary evidence item first, then derived artifacts (images, hashes), then actions in chronological order. For complex chains, consider separate provenance records for the physical item custody vs. the digital artifact custody:

```python
# Physical custody chain
physical_provenance = graph.create(ProvenanceRecord,
    name="...",
    exhibit_number="...",
    object=[evidence, action_collect, action_release, action_receipt,
            action_store],
)

# Digital artifact chain
digital_provenance = graph.create(ProvenanceRecord,
    name="...",
    exhibit_number="...",
    object=[disk_image, verify_hash, action_image, action_verify],
)
```

## SDK field reference

| Field | Type | Notes |
|---|---|---|
| `DeviceFacet.manufacturer` | `Identity` | Must be an Identity object, not a string |
| `UcoObject.description` | `list[str]` | Always a list, even for a single description |
| `AccountFacet.account_type` | `list[str]` | Always a list |
| `Hash.hash_method` | `list[str]` | Use `HashNameVocab` values (e.g., `"SHA256"`, not `"SHA-256"`) |
| `Hash.hash_value` | `str` | Typed as `xsd:hexBinary` in output |

## Skeleton (Python)

The code below shows one building block of each type. **Select only the blocks that match the source document. Repeat blocks as needed for multiple transfers, examinations, or storage events.**

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import (
    Investigation, InvestigativeAction, ProvenanceRecord,
)
from case_uco.uco.identity import Identity
from case_uco.uco.tool import Tool
from case_uco.uco.core import Relationship
from case_uco.uco.location import Location, SimpleAddressFacet
from case_uco.uco.observable import (
    ObservableObject, DeviceFacet, ContentDataFacet, FileFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # timezone from source
graph = CASEGraph()

# --- Create one Identity per person mentioned in the source ---
person_a = graph.create(Identity, name="...")  # from source
person_b = graph.create(Identity, name="...")  # from source
# ... add as many as the source identifies

# --- Create one Location per site mentioned in the source ---
site_a = graph.create(Location, name="...",
    has_facet=[SimpleAddressFacet(
        street="...", locality="...", region="...",
        postal_code="...", country="...",
    )],
)
# ... add as many as the source identifies

# --- Evidence item (manufacturer must be an Identity) ---
mfr = graph.create(Identity, name="...")
evidence = graph.create(ObservableObject, name="...",
    has_facet=[DeviceFacet(
        manufacturer=mfr, model="...",
        serial_number="...", device_type="...",
    )],
)

# === BUILDING BLOCKS — use only what the source describes ===

# Block: Collection/seizure
action_collect = graph.create(InvestigativeAction,
    name="Evidence collection",
    description=["..."],  # seizure details, packaging/seal IDs from source
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=person_a,
    object=[evidence],
    location=[site_a],
)

# Block: Imaging/hashing (hash the IMAGE, not the device)
hash_tool = graph.create(Tool,
    name="...", version="...", tool_type="Hashing Utility",
)
disk_image = graph.create(ObservableObject, name="...",
    has_facet=[
        FileFacet(file_name="...", size_in_bytes=...),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"],
            hash_value="...",  # actual hash from source
        )]),
    ],
)
action_image = graph.create(InvestigativeAction,
    name="Forensic imaging and hashing",
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=person_a,
    object=[evidence],
    result=[disk_image],
    instrument=[hash_tool],
    location=[site_a],
)

# Block: Custody release (performer = releasing, participant = receiving)
action_release = graph.create(InvestigativeAction,
    name="Custody release",
    description=["..."],  # seal condition from source
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=person_a,
    object=[evidence],
    location=[site_a],
    participant=[person_b],
)

# Block: Custody receipt (performer = receiving, participant = delivering)
action_receipt = graph.create(InvestigativeAction,
    name="Custody receipt",
    description=["..."],  # seal condition from source
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=person_b,
    object=[evidence],
    location=[site_a],
    participant=[person_a],
)

# Block: Link release → receipt as an explicit typed edge
transfer = graph.create(Relationship,
    source=[action_release], target=action_receipt,
    kind_of_relationship="custody-transfer",
    is_directional=True,
)

# Block: Hash verification
verify_hash = graph.create(ObservableObject, name="...",
    has_facet=[ContentDataFacet(hash=[Hash(
        hash_method=["SHA256"],
        hash_value="...",  # verification hash from source
    )])],
)
action_verify = graph.create(InvestigativeAction,
    name="Intake hash verification",
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=person_b,
    object=[disk_image],
    result=[verify_hash],
    instrument=[hash_tool],
    location=[site_a],
)

# Block: Evidence storage
action_store = graph.create(InvestigativeAction,
    name="Evidence storage",
    description=["..."],  # locker ID, shelf, access log from source
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=person_b,
    object=[evidence],
    location=[site_a],
)

# === Provenance — one record per evidence item ===
provenance = graph.create(ProvenanceRecord,
    name="...",
    description=["..."],
    exhibit_number="...",  # exhibit number from source
    object=[evidence, disk_image, verify_hash,
            action_collect, action_image, action_release,
            action_receipt, action_verify, action_store],
)

# === Investigation — create last, link to all top-level objects ===
investigation = graph.create(Investigation,
    name="...",            # case number from source
    description=["..."],   # case description from source
    object=[evidence, provenance],
)

graph.write("chain_of_custody.jsonld")
```

</details>
