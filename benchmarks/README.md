# Public synthetic CASE/UCO benchmarks (#81)

Fully synthetic, deterministic workloads for Python / C# / Java / Rust.

## Tiers

| Tier | Nodes | When |
|------|------:|------|
| `small` | 1_000 | PR / CI |
| `medium` | 10_000 | Nightly |
| `large` | 100_000 | Release |

## Run

```bash
# Complete four-language gate: reports, graphs, RDF equivalence, release report
CASE_UCO_BENCH_REPEATS=3 ./benchmarks/run_release_benchmarks.sh --tier small

# Python-only result + legacy timing-baseline compare
python3 benchmarks/run_python_bench.py --tier small \
  --out artifacts/bench/python-small.json \
  --graph-out artifacts/bench/python-small.jsonld
python3 benchmarks/compare_baseline.py \
  --baseline benchmarks/baselines/python-small.json \
  --result artifacts/bench/python-small.json

# Individual native-language runs
./benchmarks/run_rust_bench.sh --tier small
./benchmarks/run_csharp_bench.sh --tier small
./benchmarks/run_java_bench.sh --tier small
```

Committed baseline: `benchmarks/baselines/python-small.json`. Compare fails if
any `*_seconds` timing with baseline ≥ 50ms exceeds that baseline by more than
+100% (sub-50ms keys are skipped as too noisy for CI).

Use `--tier medium` for the 10,000-node nightly profile and `--tier large`
for the 100,000-node release profile. The default repeat count is three for
small/medium and one for large; set `CASE_UCO_BENCH_REPEATS` when a release
needs more samples.

## Workloads

All four SDK languages run:

- `catalog` — independent Tool nodes
- `relationship_rich` — device/file graphs + `partition(strategy="roots")`
- `deserialize_roundtrip` — cold/warm `from_jsonld` after registry clear
- `streaming_write` — `write_streaming` vs full `write`

Python additionally records the validation stages that are implemented in the
shared validation package:

- `bundle_resolution` — cold and warm deterministic bundle planning
- `concept_coverage` — closed-world class/property coverage
- `shacl_validation` — live validation when `case_validate` is available;
  otherwise an explicit `skipped` result, never a fabricated pass

Every core workload contains raw samples, median/min/max/mean/stdev/p95 timing
dispersion, and language-appropriate memory evidence. Each language also emits
process peak RSS where the host exposes it.

## Correctness

The runners emit the same deterministic catalog as JSON-LD. The release gate
parses each output as RDF and fails unless all four graphs are isomorphic; byte
equality is intentionally not required because serializers format JSON
differently. `generate_release_report.py` also fails on a missing workload,
sample/memory/dispersion evidence, language, or equivalence result.

Artifacts are written under `artifacts/bench/`, including the versioned JSON
report and a short Markdown release summary. Benchmarks are not a language
competition; regressions are compared to prior results from the same language
and tier.
