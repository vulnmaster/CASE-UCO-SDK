# Composition Profiles

Composition Profiles are the Phase-1 semantic-core topology: versioned,
documented, offline-queryable objects that tell an investigator or an AI
agent **which modules, Facet sets, and CAC spine kinds** to use for a
workflow. They do not add OWL classes and they do not relax SHACL.

## Why they exist

The generated registry contains ~2,800 classes across 78 modules. The 77
recipes already teach the right Facet bundles (most commonly
`FileFacet` + `ContentDataFacet` on one `ObservableObject`), but until
now that knowledge lived only in markdown. Profiles make it first-class
so a field examiner or an MCP agent can ask "what do I attach to a
RasterPicture in a CAC case?" and get a deterministic answer without
re-reading the catalog.

## Querying

**Python**

```python
from case_uco.topology import get_profile, recommend_profile, recommend_facet_set
from case_uco.topology import get_semantic_spine, spine_kind_for_class

profile = get_profile("FullCACLifecycle")
recommend_profile("hashed CSAM images from a CyberTip")
recommend_facet_set("RasterPicture", "HashIntelligence")
spine_kind_for_class("Role")
```

`case_uco.registry.list_profiles` / `get_profile` / `recommend_profile`
are thin aliases so existing registry-based agents do not need a new import.

**CLI** (no OWL parse — safe on a field laptop):

```bash
case-uco-explore profiles
case-uco-explore profile HashIntelligence
case-uco-explore spine
```

**MCP**

- `list_composition_profiles`
- `get_composition_profile`
- `recommend_composition_profile`
- `recommend_facet_set_for_profile`
- `get_cac_semantic_spine`
- resource `case-uco://composition-profiles`

## CAC spine

Every CAC domain class should anchor to one of:

| Kind | Use when |
|---|---|
| `EnduringEntity` | The thing persists (person, org, device, artifact, place, result) |
| `Occurrent` / `Event` | Something happened |
| `Situation` | A context or configuration holds |
| `Role` | A non-rigid capacity (victim, offender, examiner) |
| `Phase` | A lifecycle stage of a still-identical bearer |

Do not instantiate `cac-core:Entity` or `cac-core:Occurrent` directly.
Role ≠ person. Phase ≠ investigation.

## Compatibility

Profiles are additive. Existing builders, generated classes, and recipes
are unchanged. Validation is still SHACL + concept coverage. Everything
is air-gapped: profile JSON is vendored under `topology/profiles/`.

Canonical files: [`topology/profiles/`](../topology/profiles/INDEX.md).
