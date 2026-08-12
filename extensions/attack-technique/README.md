# Technique Metaclass Extension (`attack-technique`)

A local implementation of the `uco-action:Technique` **metaclass** and its
supporting terms, originally written ahead of release from
[ucoProject/UCO PR #676](https://github.com/ucoProject/UCO/pull/676) ("Issue
666: Add `UcoType` and `Technique`", by @ajnelson-nist), which resolves the
backwards-compatible requirements of
[issue #666](https://github.com/ucoProject/UCO/issues/666).

> **Status: superseded upstream, retained for validation.** UCO 1.5.0 ships
> `uco-core:UcoType`, `uco-action:Technique` and `uco-action:techniqueID`
> natively, and this SDK now pins UCO 1.5.0. The definitions here are
> byte-for-byte the same concepts in the same IRIs, so no instance data
> changes. They cannot be deleted yet: `case_validate` is still pinned to
> `--built-version case-1.4.0` because case-utils 0.17.0 bundles CASE only
> through 1.4.0, and that closure has no `Technique`. Passing the UCO 1.5.0
> files via `--ontology-graph` is not an alternative — two versions of one
> ontology series in the same closure trip
> `uco-owl:versionIRI-multiversion-shape`. **Retire this extension once
> case-utils publishes a release bundling CASE 1.5.0** (tracked upstream in
> [casework/CASE-Utilities-Python#182](https://github.com/casework/CASE-Utilities-Python/pull/182)).

## Why this exists

Cyber threat intelligence graphs need to carry
[MITRE ATT&CK](https://attack.mitre.org) (and
[Engage](https://engage.mitre.org) / [SOLVE-IT](https://github.com/SOLVE-IT-DF/solve-it))
technique mappings. When this extension was written, `uco-action:Technique`
was not in any released UCO version. It reproduces the PR #676 definitions
**verbatim, in their released `uco-core:` / `uco-action:` IRIs**, so CTI/APT
exemplars can model techniques and validate against the ontology closure the
validator actually loads.

## The model (per PR #676)

`uco-action:Technique` is a **metaclass**, not an ordinary class. Verbatim
from the ontology:

> A technique is a class of actions joined by some common characteristics.
> `uco-action:Technique` itself is a metaclass. A Technique instance is an
> `owl:Class` that is a subclass of `uco-action:Action`.

The PR also introduces a top-level `uco-core:UcoType` (disjoint from
`uco-core:UcoThing`) to anchor the metaclass hierarchy, and exactly one
property, `uco-action:techniqueID`. It does **not** add `techniqueFramework`,
`techniqueTactic`, or `techniquePlatform` — those were only in the issue's
early draft, not the merged model.

### Modeling pattern (punning)

```turtle
# 1. A technique is a class (instance of the metaclass + subclass of Action).
attack:T1543.003
    a owl:Class, uco-action:Technique ;
    rdfs:subClassOf uco-action:Action ;
    uco-action:techniqueID "T1543.003" .

# 2. A concrete behavior exhibiting the technique is an instance of that
#    class — the rdf:type edge IS the association.
kb:action-install-service
    a uco-action:Action, attack:T1543.003 ;
    uco-action:performer kb:lotus-blossom .
```

## Terms

| Term | Kind | Notes |
|---|---|---|
| `uco-core:UcoType` | metaclass anchor | Top-level; `owl:disjointWith uco-core:UcoThing`; instances are `owl:Class`es |
| `uco-action:Technique` | metaclass | `rdfs:subClassOf uco-core:UcoType`; a Technique instance is an `owl:Class` subclassing `uco-action:Action` |
| `uco-action:techniqueID` | datatype property | Literal-valued technique identifier (e.g. `T1543.003`); used only on Techniques |

The two standalone SHACL shapes from the PR
(`core:UcoThing-disjointWith-UcoType-shape`,
`action:techniqueID-subjects-shape`) are in `attack-technique-shapes.ttl`;
the node-shape constraints on the classes themselves are declared alongside
the classes in `attack-technique.ttl`.

## Files

| File | What it is |
|---|---|
| `attack-technique.ttl` | `uco-core:UcoType`, `uco-action:Technique`, `uco-action:techniqueID` — verbatim from PR #676 |
| `attack-technique-shapes.ttl` | The two standalone SHACL shapes from PR #676 |
| `mitre-attack-catalog.ttl` | Partial MITRE ATT&CK catalog: each technique an `owl:Class`/`uco-action:Technique` under its canonical `attack.mitre.org` IRI |
| `manifest.json` | Extension manifest (owl/shacl files, namespaces, UCO compat) |
| `_registry.json` | Class/property registry for MCP discovery |

## Validation

The metaclass constraints resolve under RDFS inference, so validate with
`--inference rdfs`:

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/attack-technique/attack-technique.ttl \
  --ontology-graph extensions/attack-technique/attack-technique-shapes.ttl \
  --ontology-graph extensions/attack-technique/mitre-attack-catalog.ttl \
  --inference rdfs --allow-info \
  path/to/graph.jsonld
```

Or via the SDK / MCP validator:
`validate_graph(path, extensions=["attack-technique:full"])`.

## Extending / refreshing the catalog

The catalog is a **generated** partial set (techniques used by exemplars).
Refresh labels and comments from the pinned MITRE ATT&CK STIX 2.1 release:

```bash
make sync-attack                        # fetch Enterprise ATT&CK v19.1
make sync-attack ATTACK_VERSION=19.1
make sync-attack-offline STIX=/path/to/enterprise-attack-19.1.json
```

The sync tool (`mcp_server/tools/sync_attack_catalog.py`) unions the current
catalog membership with technique IRIs cited under `examples/cti/`, rewrites
`mitre-attack-catalog.ttl`, and records provenance in `manifest.json`.

To add a technique manually before regenerating, include it with
`--include Txxxx` (or cite it from an exemplar and run `--from-exemplars`).
Each class must keep the punning pattern: canonical
`https://attack.mitre.org/techniques/<id>` IRI, `a owl:Class,
uco-action:Technique`, `rdfs:subClassOf uco-action:Action`,
`uco-action:techniqueID "<id>"`.

## Used by

- [`examples/cti/lotus_blossom_2025/`](../../examples/cti/lotus_blossom_2025/) —
  twelve MITRE ATT&CK techniques (G0030 / S1156) typed onto the behavior
  Actions of the Cisco Talos Lotus Blossom / Sagerunex report.
- Recipe: [`docs/recipes/cyber-threat-intelligence.md`](../../docs/recipes/cyber-threat-intelligence.md).
