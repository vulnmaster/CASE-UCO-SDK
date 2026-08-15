# Topology Articulation & Optimization Framework

This document permanently articulates the logical-mechanistic topology of
the CASE/UCO SDK. The SDK exists so law-enforcement and child-protection
teams can turn raw investigative material into validated CASE/UCO + CAC
graphs and find children faster — including on air-gapped networks.

Machine-readable companions live under [`topology/`](topology/README.md).

## Five layers

| Phase | Layer | What it is now |
|---|---|---|
| 0 | Baseline | Module DAG, class/facet inventory, recipe composition patterns |
| 1 | Semantic core | CAC spine + seven Composition Profiles, queryable via runtime / CLI / MCP |
| 2 | Generation | Content-hashed IR + incremental `generate` (skip when Turtle is unchanged) + fluent helpers |
| 3 | Runtime | Hash indexes, `partition_by_profile`, streaming writers (existing) |
| 4 | Agent / control | `InvestigationBuilder`, executable recipe DAGs, inline critique |
| 5 | Interop | VICS/PhotoDNA mapping stub, topology lenses, change-proposal path |

## How to navigate

```bash
case-uco-explore profiles
case-uco-explore profile FullCACLifecycle
case-uco-explore spine
python -m case_uco_generator generate          # incremental by default
python -m case_uco_generator generate --force  # full re-parse
```

```python
from case_uco import CASEGraph, InvestigationBuilder, file_with_content_hashes

builder = InvestigationBuilder("CyberTip CSAM hashing", profile_id="HashIntelligence")
builder.add_csam_evidence("img.jpg", hashes=[("SHA256", "…"), ("PhotoDNA", "…")])
graph = builder.build()
print(graph.lookup_hash("…"))
print(builder.critique())
```

## Hard constraints

- No breaking public API changes without a major version bump.
- Investigation-time work stays offline.
- SHACL + concept coverage remain the validation contract.
- The generator remains the source of truth for typed classes.

## Contributing a gap upstream

If a live case proves a profile or mapping incomplete, do not invent
core terms. Draft a change proposal (`docs/recipes/change-proposal.md`)
and, if needed, a local extension. PhotoDNA structured payloads and
native VICS types are the first candidates.
