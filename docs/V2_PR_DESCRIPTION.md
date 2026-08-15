# feat: v2 construction re-architecture — contracts, workflow engine, continuous critique

This pull request is a **coherent, capability-defining re-architecture** of how investigation graphs are *constructed* in the CASE/UCO SDK. It is proposed as the foundation of **v2.0.0**: a recommended-path major, not a deleted-API major.

It is written with respect for existing users and for Project VIC’s mission: turn raw investigative material into validated CASE/UCO + CAC graphs so children can be found and safeguarded faster — including on air-gapped field laptops.

## Why this is a generation, not a feature pile

The Topology Articulation Framework (upstream PR #106) made the ontology navigable. That was necessary and it remains. What it did not yet do is make **correct construction under operational pressure** the center of gravity.

v2 does:

1. **Composition Profiles are runtime contracts.** Required Facets, hash presence, tool version, mission checks, and honest SHACL/coverage signals are evaluable — not just documented.
2. **An Investigation Workflow Engine is the recommended primary path.** Operators and agents load a profile + local evidence, execute a resumable multi-step workflow, and receive a validated graph or structured remaining findings.
3. **Continuous critique is construction semantics.** It runs on each add and at every step. The MCP critic remains the acceptance loop; it is not replaced.
4. **Large cases are first-class.** Worklists partition by forensic boundary before heavy build. `partition_by_profile` default behaviour is unchanged.
5. **Trajectories and VICS/PhotoDNA sit in the same model.** JSON contracts over existing OWL. Offline adapters. No invented core terms.

Existing `InvestigationBuilder`, fluent helpers, generated classes, and Topology tests remain the floor.

## What to review

1. `docs/V2_ARCHITECTURE.md` — landed center of gravity and migration.
2. `docs/design/v2-construction-rearchitecture.md` — Phase 0 design.
3. `python/case_uco/{contracts,critique,workflow,adapters,trajectories}/`
4. `topology/{contracts,workflows,trajectories}/`
5. Language logical surface: `ProfileContract`, `InvestigationWorkflow`, CAC-prefix fix.

## Constraints honored

- Investigation-time behaviour is offline.
- Generator remains the source of truth for typed classes.
- No new core OWL terms. PhotoDNA stays `Hash.hashMethod` + action.
- PySHACL is not rewritten.
- Additive wherever possible; frozen `critique()` triples keep Topology helper tests green.

## Test results (authoring host)

| Suite | Result |
|---|---|
| `python/tests/test_helpers_and_builder.py` | passed |
| `python/tests/test_composition_profiles.py` | passed |
| `python/tests/test_profile_contracts.py` | passed |
| `python/tests/test_continuous_critique.py` | passed |
| `python/tests/test_workflow_engine.py` | passed |
| `python/tests/test_workflow_partitions.py` | passed |
| `python/tests/test_trajectories.py` | passed |
| `python/tests/test_adapters_hash_intel.py` | passed |
| `topology/tests/test_profiles.py` | passed |
| C# / Java | helpers + logical surface added; .NET SDK / JDK not installed on this host — CI `make test` is the gate |
| Rust | `cargo test` needs MSVC `link.exe` on this host — not run; CI is the gate |

## Semver honesty

`2.0.0` marks a new recommended primary interface. Constructors were not removed. Full C#/Java/Rust workflow runners are scoped as 2.1.
