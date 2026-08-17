# SDK Topology and Semantic Spine

This is a hand-maintained map of the CASE/UCO SDK as it exists on the
1.x line. It helps an investigator or developer find the right layer and
the right organizing class without reading generated catalogs.

It is **documentation only**. It does not change runtime behavior. It
does not add OWL classes, SHACL shapes, or vocabulary. The ontology
sources and the generator remain the source of truth.

## What this is not

- Not a class, Facet, or module inventory. Those catalogs are generated
  (`ONTOLOGY_REFERENCE.md`, `python/case_uco/_registry.json`) and must
  not be copied into this file.
- Not new ontology truth. Every class named here already exists in
  vendored Turtle or generated bindings.
- Not a construction runtime, workflow engine, critic, adapter, or
  helper API.
- Not licensed catalog schemas or product-internal hash algorithms.

## Repository topology

Evidence becomes a CASE/UCO graph by moving through these existing
layers. Each layer already has a home in the tree.

```text
ontology/ + extensions/     OWL + SHACL sources (submodules are not edited here)
        |
        v
generator/                  Emits typed bindings and _registry.json
        |
        +--> python/ csharp/ java/ rust/     public constructors
                    |
                    v
            CASEGraph / CaseGraph            create, serialize, load, validate
                    |
                    +--> docs/recipes/       modeling patterns
                    +--> mcp_server/         agent discovery and validation
                    +--> change_proposals/   drafts for upstream ontology
```

| Layer | Path | What it is for |
|---|---|---|
| Ontology sources | `ontology/`, `extensions/` | Official UCO, CASE, CAC, and bundled extensions. Do not edit submodule Turtle in an SDK feature PR. |
| Generator | `generator/` | Source of typed classes. Regenerated output is not hand-edited. |
| Language bindings | `python/`, `csharp/`, `java/`, `rust/` | Same ontology, idiomatic constructors. See `docs/CROSS_LANGUAGE_PARITY.md`. |
| Runtime graph | `CASEGraph` / `CaseGraph` | `create` / `Add` / `add`, serialize, load, validate. Public constructors stay on the 1.x line. |
| Discovery | `case_uco.registry`, `case-uco-explore`, `ONTOLOGY_REFERENCE.md` | Find an existing class by name, module, or property. |
| Recipes | `docs/recipes/` | How to combine existing classes for a workflow. |
| MCP | `mcp_server/` | Offline-capable agent tools over the same registry and recipes. |
| Change proposals | `change_proposals/` | The path for a missing concept. Do not invent a core term in application code. |

Investigation-time work stays offline. Validation remains SHACL plus
concept coverage (`graph.validate()` / `case_validate`).

## CAC semantic spine

CAC domain classes are organized by **ontological kind**, not by
workflow. The spine is defined in

`ontology/cac/ontology/ontology/cacontology-core-spine.ttl`

and is already present in the generated registry as
`ext.cac.cac-core`. The table below is a reading aid for that file.

| Kind | IRI local name | Use when | Do not use when |
|---|---|---|---|
| Root | `Entity` | — | Instantiating it. Anchor to a subclass. |
| Enduring | `EnduringEntity` | The thing persists: person, org, device, artifact, place, result. | The concept is an event, situation, role, or phase. |
| Occurrent | `Occurrent` | — | Instantiating it. Use `Event` or a subclass. |
| Event | `Event` | Something happens, has time bounds, or has participants. | The concept is a persisting context (`Situation`). |
| Situation | `Situation` | A context or configuration holds for an interval. | Something occurs (`Event`). |
| Role | `Role` | A non-rigid capacity: examiner, guardian, offender, victim. | The bearer person (`PersonLikeEntity`). Role ≠ person. |
| Phase | `Phase` | A lifecycle stage of a still-identical bearer. | The investigation itself. Phase ≠ investigation. |

Immediate, already-defined children that are useful as orientation
(not an inventory):

- `EnduringEntity` → `PersonLikeEntity`, `OrganizationLikeEntity`,
  `DigitalSystemEntity`, `Artifact`, `PlaceLikeEntity`,
  `AssessmentResult`
- `Event` → `ExploitationEvent`, `DetectionEvent`,
  `CoordinationEvent`, `SupportEvent`, `LegalEvent`,
  `InvestigativeAction`

`Artifact` is also a `uco-observable:ObservableObject`.
`InvestigativeAction` is also `case-investigation:InvestigativeAction`
and `uco-action:Action`. Those alignments already exist in the spine
Turtle. This document does not add them.

`Event` and `Role` are also UCO local names. The generated registry
keeps the UCO record for those two strings. The CAC classes remain
`https://cacontology.projectvic.org/core#Event` and
`https://cacontology.projectvic.org/core#Role` in the spine Turtle.

## UCO construction spine

Most CASE/UCO instance data hangs off three existing core classes:

| Class | Module | Role |
|---|---|---|
| `UcoThing` | `uco.core` | Root of instance individuals. |
| `UcoObject` | `uco.core` | Identified characterization. Parent of most instance classes. |
| `Facet` | `uco.core` | Property bundle attached with `uco-core:hasFacet`. |
| `UcoType` | `uco.core` | Metaclass root (UCO 1.5.0). Not an instance individual. |

The usual file pattern from the recipe cookbook is unchanged: one
`ObservableObject` (or a more specific host such as `File` /
`RasterPicture`) with `FileFacet` + `ContentDataFacet` attached. Put
hashes on `ContentDataFacet`, not on a parallel object.

## How to reproduce

Do **not** commit generated inventories, timestamped dumps, or
`class-and-facet-inventory.*` / `module-dependency-dag.*` /
`sdk-layers.json` files. Re-derive the compact spine from sources:

```bash
# Stdout only. Never writes a file.
python scripts/print_sdk_topology.py

# Confirm this document still names classes that exist.
python -m pytest python/tests/test_sdk_topology_docs.py -q
```

`print_sdk_topology.py` prefers the vendored CAC spine Turtle when the
submodule is checked out, and always cross-checks documented IRIs
against `python/case_uco/_registry.json`.

To inspect the sources by hand:

1. Open `ontology/cac/ontology/ontology/cacontology-core-spine.ttl`.
2. Confirm each `cac-core:* a owl:Class` named in the tables above.
3. Confirm `UcoThing`, `UcoObject`, `Facet`, and `UcoType` in
   `uco.core` via `case-uco-explore class UcoObject` or
   `case_uco.registry.get_class("UcoObject")`.

If the spine Turtle gains or removes a kind, update the table in this
file and the expected names in the test. Do not snapshot the whole
registry.

## Compatibility

Additive documentation on the SDK 1.x line. Public constructors,
generated bindings, recipes, MCP tools, and validation paths are
unchanged.
