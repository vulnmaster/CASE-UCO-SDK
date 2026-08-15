# Generator Intermediate Representation

`source-manifest.json` is a content-hashed inventory of every vendored
Turtle file the generator reads. `ontology-ir.json` is a compact summary
(counts, modules, recommended Facet bundles).

`case-uco-generate generate` is incremental by default: if the live
aggregate SHA-256 matches the stored manifest, parse and emission are
skipped. Pass `--force` after a generator-code change.

The first run after this directory is created still does a full parse
and then writes the manifest.
