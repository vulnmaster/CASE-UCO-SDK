# Topology Articulation

This directory is the permanent, machine-readable articulation of the
CASE/UCO SDK's logical-mechanistic topology. It exists so law-enforcement
and child-protection teams — and the AI agents that assist them — can
navigate the ontology, generator, runtime, MCP control plane, and recipe
catalog without re-deriving the graph from first principles.

The ultimate purpose is unchanged: turn raw investigative material into
validated, interoperable CASE/UCO + CAC knowledge graphs so children can
be found and safeguarded faster, including in air-gapped / zero-egress
environments.

## Layers

| Layer | What it articulates | Primary artifacts |
|---|---|---|
| 0. Baseline | Observed module DAG, class/facet inventory, recipe composition patterns | `module-dependency-dag.*`, `class-and-facet-inventory.*`, `composition-patterns.*` |
| 1. Semantic core | CAC spine + UCO hierarchy + Composition Profiles | `semantic-spine.json`, [`profiles/`](profiles/INDEX.md) |
| 2. Generation | Versioned, content-hashed IR and incremental generation | `../generator/ir/` |
| 3. Runtime | Partitioning, indexes, hash-intelligence helpers | documented in `sdk-layers.json` |
| 4. Agent / control | Executable recipe DAGs and InvestigationBuilder | `recipe-dags/` |
| 5. Interop & evolution | VICS / PhotoDNA mappings and change-proposal bridges | `mappings/` |

## Regenerating baseline artifacts

Artifacts in this directory are generated, not hand-edited. From the
repository root (stdlib only; no network):

```bash
python topology/scripts/build_baseline.py
```

The builder reads vendored Turtle, generated `_registry.json` files, the
77-recipe catalog, and `mcp_server/domain_index.py`. It writes JSON plus
Markdown/Mermaid companions. It never contacts the network.

## Verification baseline

`baseline/verification.json` records the environment and the result of
the Phase 0 verification gate (`make init && make generate && make check`,
or the documented Windows-native equivalent when GNU Make is unavailable).
