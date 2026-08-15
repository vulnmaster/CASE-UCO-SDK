# Topology Articulation & Optimization Framework

**Draft PR title:** `feat: Topology Articulation Framework — Composition Profiles, incremental generate, and multi-language helpers`

This pull request adds a permanent, machine-readable articulation of the CASE/UCO SDK's topology and a set of additive, offline-first helpers so law-enforcement and child-protection teams can produce validated CASE/UCO + CAC graphs faster — including on air-gapped field laptops.

## Why this exists

The SDK was funded by Project VIC International so that raw investigative material can become interoperable knowledge graphs. Finding the right class among ~2,800 types, waiting ten minutes to regenerate after a one-line Turtle tweak, and re-deriving Facet bundles from 77 recipes are avoidable delays. This work removes those delays without changing the ontology or the public constructors of the four language bindings.

## Five layers

| Layer | What landed |
|---|---|
| 0. Baseline | `topology/` DAG, class/facet inventory, recipe composition patterns |
| 1. Semantic core | Seven Composition Profiles + queryable CAC spine (runtime, CLI, MCP) |
| 2. Generation | Content-hashed IR; skip-if-unchanged (~623 s → ~0.8 s); leaf-extension dependent-only re-parse |
| 3. Runtime | Hash indexes, `partition_by_profile`, hexBinary hash serialization |
| 4. Agent / control | `InvestigationBuilder` with inline critique; executable recipe DAGs |
| 5. Interop | VICS/PhotoDNA mapping stub; PhotoDNA Facet **change proposal** (not a core class) |

## User-facing surface

**Composition Profiles** (all air-gapped): `MinimalForensics`, `AirGappedFieldTriage`, `HashIntelligence`, `ToolMapping`, `LegalProcess`, `FullCACLifecycle`, `CrossOntology`.

**Fluent helpers** (identical across Python, C#, Java, Rust — see `docs/CROSS_LANGUAGE_PARITY.md`):

- `file_with_content_hashes` / `FileWithContentHashes` / `fileWithContentHashes`
- `model_csam_evidence` / `ModelCsamEvidence` / `modelCsamEvidence`
- `model_tool_run` / `ModelToolRun` / `modelToolRun`
- `InvestigationBuilder` (`profile_id`, `add_csam_evidence`, `build`, `critique`)
- `lookup_hash` / `index_content_hashes` / `partition_by_profile`

**Incremental generate**

- Unchanged Turtle → skip OWL parse and class emission.
- Leaf extension change → re-parse UCO+CASE + that module and its DAG dependents; merge into `_registry.json`; do **not** rewrite core bindings.
- `ontology/UCO` or `ontology/CASE` change, or `--force` → full parse.

## Intentionally out of scope

- **No new core OWL terms.** PhotoDNA remains extra `Hash` entries (`hashMethod=PhotoDNA`) plus a hashing `InvestigativeAction`. A structured Facet is proposed in `change_proposals/photodna-perceptual-hash-facet.md` for the UCO committee.
- **No public constructor breakage.** Existing `create`/`Add`/`add` APIs are unchanged.
- **No network at investigation time.** Profiles, IR, and helpers are vendored JSON / local code.
- **Rust Facet inheritance** is still generated as standalone structs. Helpers attach Facets via `uco-core:hasFacet` (documented idiomatic difference).

## Test results (this host)

| Suite | Result |
|---|---|
| `topology/tests` + profile tests | passed |
| `generator/tests` (including incremental plan) | passed |
| `python/tests` except pre-existing Darkwatchman Windows SHA / workspace-policy cases | passed |
| `mcp_server/tests/test_recipe_catalog.py` | passed |
| Incremental `generate --lang python` cache hit | ~0.84 s |
| Leaf extension delta (`cryptoinv.ttl` comment) | **~23 s** (24 Turtle files, not the full 156) |
| Full Python generate baseline | ~623 s |
| C# / Java | helpers + tests added; .NET SDK / JDK not installed on the authoring host — CI `make test` is the gate |
| Rust | `cargo test` on this host (see commit notes) |

## Offline / non-breaking guarantees

- Investigation-time behaviour requires no network.
- SHACL + concept coverage remain the validation contract.
- The generator remains the source of truth for typed classes.
- Topology helpers are additive wrappers around those classes.

## How to review

1. `topology/README.md` and `TOPOLOGY.md` for the framework.
2. `topology/profiles/` for the seven profiles.
3. `docs/CROSS_LANGUAGE_PARITY.md` for the new identical operations.
4. `change_proposals/photodna-perceptual-hash-facet.md` for the upstream proposal (does not alter ontology files).
5. Language-specific helper tests: `python/tests/test_helpers_and_builder.py`, `csharp/CaseUco.Tests/TopologyHelpersTests.cs`, `java/.../TopologyHelpersTest.java`, `rust/tests/topology_helpers_test.rs`.
