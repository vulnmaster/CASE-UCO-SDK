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
| `python/tests/` except exhaustive / darkwatchman / attack-catalog | **163 passed, 4 skipped** |
| v2 construction floor (contracts, critique, workflow, partitions, trajectories, adapters, packaging, host resolution, critic IDs, helpers) | **57 passed** (subset of the 163) |
| `topology/tests/test_profiles.py` + `test_baseline_artifacts.py` | **12 passed** |
| C# / Java | helpers + logical surface + resume tests added; .NET SDK / JDK not installed — CI `make test` is the gate |
| Rust `cargo test` / `cargo check` | MSVC `link.exe` missing — not run; CI is the gate |
| `case_validate` / PySHACL | not installed; construction tests skip SHACL honestly (`validator_unavailable`) |
| `tests/test_exhaustive.py`, `test_darkwatchman_release.py`, `test_attack_catalog_coverage.py` | not run here (long / environment-heavy; not required for the 2.0.1 surface) |

## Semver honesty

`2.0.0` remains the recommended-path major. `2.0.1` is a quality increment. Full C#/Java/Rust workflow runners, incoming Rust `partition_by_roots`, the rest of the MCP `CRIT-H-*` set, and generating `ConditioningPhase` bindings are **2.1**.
