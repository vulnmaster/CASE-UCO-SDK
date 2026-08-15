# Generator Intermediate Representation

`source-manifest.json` is a content-hashed inventory of every vendored
Turtle file the generator reads. `ontology-ir.json` is a compact summary
(counts, modules, recommended Facet bundles).

`case-uco-generate generate` is incremental by default:

* If the live aggregate SHA-256 matches the stored manifest, OWL parse
  and class emission are skipped (~1 s). Topology helper catalogs are
  still refreshed.
* If only a leaf extension Turtle file changed, the generator re-parses
  UCO+CASE plus that module and its DAG dependents (not every other
  extension), merges those classes into `_registry.json`, and leaves
  core language bindings untouched.
* A change under `ontology/UCO` or `ontology/CASE` still forces a full
  parse. Pass `--force` after a generator-code change.

The first run after this directory is created still does a full parse
and then writes the manifest.
