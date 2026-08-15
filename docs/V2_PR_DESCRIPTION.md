# feat: v2.0.1 quality increment — critique, resume, partitions, generate-lag

This pull request is the **2.0.1 quality increment** on the already-landed v2 construction re-architecture (2.0.0 recommended-path major). It does not invent architecture. It raises correctness, guidance, test coverage, and documentation honesty so the branch can be labeled **v2.0.1**.

The generational claim stays with **2.0.0**: Profile contracts + continuous critique + Investigation Workflow Engine as the recommended path + partition awareness + trajectories + offline adapters + four-language logical surface. Public constructors were not deleted.

## What 2.0.1 reviews

1. `docs/design/v2.0.1-refinement-plan.md` — what closed vs what stays 2.1.
2. Construction critique expansion (`CRIT-H-DERIVED-*`, `CHARGED-WITH-REVERSED`, `IMAGE-CONTAINER-MISMATCH`, `ORPHAN-TOP-LEVEL`; live mission checks).
3. C#/Java/Rust `Resume` + `RegisterHandler` (source-level; CI compiles). Full handlers remain 2.1.
4. Forensic-boundary harden, worklist inference, RAM-guard `PROF-PART-001`. Process pool stays opt-in/off.
5. Actionable `PROF-TRAJ-NOT-GENERATED`; offline hash-match / VICS tag.
6. Wheel-surface packaging tests; CLI/MCP discovery for trajectories and adapters.
7. Version metadata **2.0.1** and precise CHANGELOG / architecture docs.

## Constraints honored

- Investigation-time behaviour is offline.
- Generator remains the source of truth for typed classes.
- No new core OWL terms. PhotoDNA stays `Hash.hashMethod` + action.
- Frozen `InvestigationBuilder.critique()` triples unchanged.
- Additive wherever possible.

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
| `python/tests/test_packaging_profiles.py` | passed |
| `python/tests/test_host_resolution.py` | passed |
| `python/tests/test_critic_id_stability.py` | passed |
| `topology/tests/test_profiles.py` | passed |
| `topology/tests/test_baseline_artifacts.py` | passed |
| C# / Java | helpers + logical surface + resume tests added; .NET SDK / JDK not installed on this host — CI `make test` is the gate |
| Rust | `cargo test` needs MSVC `link.exe` on this host — not run; CI is the gate |
| `case_validate` / PySHACL | not installed; construction tests skip SHACL honestly (`validator_unavailable`) |

## Semver honesty

`2.0.0` remains the recommended-path major. `2.0.1` is a quality increment. Full C#/Java/Rust workflow runners, incoming Rust `partition_by_roots`, the rest of the MCP `CRIT-H-*` set, and generating `ConditioningPhase` bindings are **2.1**.
