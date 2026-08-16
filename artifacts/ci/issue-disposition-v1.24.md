# v1.24.0 issue and code-scanning disposition

**Snapshot date:** 2026-08-16
**Release tag target:** `v1.24.0`

GitHub reported six open issues and two open code-scanning alerts when this
release review began. This file records which items are release scope and which
remain explicitly deferred; an open backlog item is not silently represented as
complete.

## Release-scoped issues

| Issue | Disposition | Release evidence |
| --- | --- | --- |
| #99 — bounded Apple acquisition packaging/share-safety | Completed for v1.24.0; close after the tagged commit is published | `mcp_server/apple_acquisition.py`, MCP wrappers/routing, Apple recipes, synthetic boundary/security tests, live SOLVE-IT SHACL + strict-concept validation |
| #100 — baseline compute requirements | Completed for v1.24.0; close after the tagged commit is published | `README.md`, `docs/COMPUTE.md`, `catalog/compute.yaml` |

## Additional release blockers

Issues #79–#82 carry the phase-two acceptance deferred from v1.22.0 and the
overdue v1.23.0 milestone. The maintainer promoted all four to mandatory
v1.24.0 release gates on 2026-08-16. The stable tag must not be created until
the implementations, cross-language parity tests, and release evidence below
are complete.

| Issue | v1.24.0 disposition | Required release evidence |
| --- | --- | --- |
| #79 — marking-safe dependency partitioning | **Implemented; local final matrix passed** | Marking/authorization boundary policy, home/support/error cross-boundary policies, portable v2 manifest, partition-set validation, and RDF-union/equivalent-assertion proofs in all four SDKs |
| #80 — phase-two bounded JSON-LD writer | **Implemented; local final matrix passed** | Frozen-context incremental writers, configurable per-node memory bound, prefix rejection, and induced-failure destination preservation tests in all four languages |
| #81 — full cross-language benchmark suite | **Implemented; small/medium/large gates passed locally** | Four shared workload families; repeated timing and memory/dispersion metrics; Python bundle/coverage/SHACL stages; scheduled/manual tiers; 1K, 10K, and 100K RDF-equivalence reports all `ready` |
| #82 — extension-registry cache invalidation | **Implemented; local final matrix passed** | Explicit extension-provider registration, deterministic conflicts, generation/invalidation semantics, and cache hit/miss tests across the applicable language runtimes |

The 100,000-node local release run produced four isomorphic 300,000-triple
catalog graphs. Its measured process peak RSS was approximately 442 MB
(Python), 558 MB (C#), 1.39 GB (Java), and 411 MB (Rust). These host-specific
outputs remain CI/release artifacts under `artifacts/bench/`; the source tree
contains the versioned generator and report schema, not one developer's
machine-specific result.

## Local release verification

The final local gate passed on 2026-08-16:

- generator and Python SDK: 133 tests passed;
- MCP server: 441 tests passed;
- C#: 33 tests passed;
- Java: 31 tests passed;
- Rust: 28 unit/integration tests and one documentation test passed;
- documentation snippets: 118 passed;
- Python type checking and changed-file Ruff checks passed;
- strict Rust Clippy security lints passed with warnings denied, including
  `unwrap_used` and `expect_used`;
- RustSec scanned 47 locked dependencies with no vulnerability findings;
- generator rerun was byte-identical for registries and reference docs;
- Python sdist/wheel and Rust crate package verification passed; C# NuGet and
  Java JAR packaging passed earlier in the same gate.

The first GitHub-hosted analysis of the merged release candidate closed alerts
#527/#528 and surfaced nine findings in the newly added v1.24 code. The tag
remains blocked until the follow-up checks pass and alerts #529–#537 are
confirmed closed by analysis.

## Code scanning

| Alert | Rule | Path | Disposition |
| --- | --- | --- | --- |
| #527 | `py/unused-local-variable` | `examples/sysdiagnose/build_ios_sysdiagnose_unified_logs.py` (`ul_record`) | Fixed by deleting the unused assignment |
| #528 | `py/unused-local-variable` | `examples/sysdiagnose/build_ios_sysdiagnose_unified_logs.py` (`ul_event`) | Fixed by deleting the unused assignment |
| #529 | `java/local-temp-file-or-directory-information-disclosure` | `java/src/main/java/org/caseontology/bench/CatalogBench.java` | Fixed by using a securely randomized temporary directory |
| #530–#533 | `java/missing-override-annotation` | `java/src/test/java/org/caseontology/CaseGraphTest.java` | Fixed by marking all anonymous service-provider method overrides |
| #534 | `py/empty-except` | `python/case_uco/streaming.py` | Fixed by using `Path.unlink(missing_ok=True)` for idempotent cleanup |
| #535 | `cs/call-to-gc` | `csharp/CaseUco.Bench/Program.cs` | Fixed by sampling live managed memory without forcing collection |
| #536 | `cs/linq/missed-where` | `csharp/CaseUco/CaseGraph.cs` | Fixed by filtering resolved weak references before enumeration |
| #537 | `cs/path-combine` | `csharp/CaseUco/JsonLdStreamWriter.cs` | Fixed by normalizing the destination and appending a generated relative temporary filename without `Path.Combine` |

Alerts #529–#537 remain visible against `main` until the follow-up commit is
merged and a new CodeQL analysis runs. They must be verified closed by
analysis, not manually dismissed.
