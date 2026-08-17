# Generic Fluent Helpers

Three optional Python wrappers around **existing** CASE/UCO constructors.
They assemble the Facet bundles already taught by the recipe cookbook so
hashed files, raster media, and tool-run provenance are hard to get wrong.

They do **not** add OWL classes. They do **not** relax or replace SHACL.
They do **not** change public constructors. The ontology remains the
source of truth; a helper is a shortcut, not a new type.

## Why they exist

The usual file pattern is one `ObservableObject` (or a more specific
host such as `RasterPicture`) with `FileFacet` + `ContentDataFacet`
attached. Hashes belong on `ContentDataFacet`, not on a parallel object.
A tool run is a versioned `Tool` plus an `InvestigativeAction` whose
`instrument` / `object` / `result` links record what ran, what it
consumed, and what it produced.

Those patterns already live in the recipes. The helpers make the same
advice one function call.

## What this is not

- Not new ontology terms, SHACL shapes, or vocabulary.
- Not a classifier. This layer does not classify media as CSAM or any
  other category. Callers supply hashes and names; the helpers only
  attach them.
- Not licensed catalog schemas or product-internal hash algorithms.
- Not a workflow engine, critique engine, adapter, or 2.x construction
  runtime.
- Not Composition Profiles, topology inventories, or cross-language
  ports. Those are separate 1.x changes if they are wanted later.

## Usage

```python
from case_uco import (
    CASEGraph,
    file_with_content_hashes,
    model_tool_run,
    raster_picture_with_hashes,
)

graph = CASEGraph()

empty = file_with_content_hashes(
    graph,
    file_name="empty.bin",
    hashes=[("SHA256", "e3b0c44298fc1c149afbf4c8996fb92402706899c32911cf29121339aa1a904b")],
)

picture = raster_picture_with_hashes(
    graph,
    file_name="sample.png",
    hashes=[("SHA256", "e3b0c44298fc1c149afbf4c8996fb92402706899c32911cf29121339aa1a904b")],
    picture_type="png",
)

parts = model_tool_run(
    graph,
    tool_name="Autopsy",
    tool_version="4.21.0",
    action_name="Hash verification",
    inputs=[empty],
    outputs=[picture],
)
```

`model_tool_run` does not create a `ProvenanceRecord`. Attach one with
the existing constructor when an exhibit number is needed.

Fixtures and examples in this document use the public SHA-256 of the
empty file. Do not commit case data.

## Compatibility

Additive 1.x Python helpers. Existing builders, generated classes,
recipes, and validation paths are unchanged. Callers who prefer to
construct `FileFacet` / `ContentDataFacet` / `Tool` /
`InvestigativeAction` by hand keep doing that.
