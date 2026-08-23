# Composition Profiles

Composition Profiles are a small, schema-validated catalog of
**investigator guidance**. Each profile names the existing CASE/UCO/CAC
modules, Facet bundles, and recipe starting points that usually belong
together for one workflow.

They do **not** add OWL classes. They do **not** relax or replace SHACL.
They do **not** change public constructors. The ontology remains the
source of truth; a profile is a map, not a new continent.

## Why they exist

The generated registry contains thousands of classes across dozens of
modules. The recipe cookbook already teaches the right Facet bundles
(most commonly `FileFacet` + `ContentDataFacet` on one
`ObservableObject`), but that knowledge lived only in markdown. Profiles
make the same advice loadable so an examiner can ask "what do I attach
to a `File` in a minimal forensics graph?" and get a deterministic answer
without re-reading the catalog. This PR ships one example:
`MinimalForensics`.

## What this is not

- Not new ontology terms, SHACL shapes, or vocabulary.
- Not a workflow engine, critique engine, or 2.x construction runtime.
- Not a classifier. Nothing here labels media as CSAM or any other
  category.
- Not a licensed data-model dump. This catalog does not include VICS
  schema details or PhotoDNA internals.
- Not a replacement for `partition_by_profile` or the generator.

## Querying

Profiles are vendored under [`topology/profiles/`](../topology/profiles/README.md)
and are intended to be used offline from a repository checkout.

```python
from case_uco.profiles import list_profiles, get_profile

for profile in list_profiles():
    print(profile.id, profile.title)

minimal = get_profile("MinimalForensics")
file_facets = minimal.facet_set_for("File") if minimal else None
```

Override the catalog directory with `CASE_UCO_PROFILES_DIR` when loading
a local copy (for example an agency-specific overlay). The loader only
reads `*.json` files and ignores `*.schema.json`.

## Compatibility

Profiles are additive 1.x documentation plus a read-only loader. Existing
builders, generated classes, recipes, and validation paths are unchanged.
Every committed profile is air-gapped: no network steps, no credentials,
and only synthetic / public-safe guidance text.

Canonical files: [`topology/profiles/`](../topology/profiles/README.md).
Schema: [`topology/profiles/profile.schema.json`](../topology/profiles/profile.schema.json).
