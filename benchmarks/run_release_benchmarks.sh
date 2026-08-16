#!/usr/bin/env bash
# Run the complete cross-language benchmark/equivalence release gate (#81).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER="${1:-large}"
if [[ "${1:-}" == "--tier" ]]; then TIER="${2:-large}"; fi
OUT_DIR="${ROOT}/artifacts/bench"
mkdir -p "${OUT_DIR}"

PYTHON_BIN="${CASE_UCO_BENCH_PYTHON:-python3}"
PYTHON_ARGS=(--tier "${TIER}" --out "${OUT_DIR}/python-${TIER}.json" --graph-out "${OUT_DIR}/python-${TIER}.jsonld")
if [[ -n "${CASE_UCO_BENCH_REPEATS:-}" ]]; then PYTHON_ARGS+=(--repeats "${CASE_UCO_BENCH_REPEATS}"); fi
"${PYTHON_BIN}" "${ROOT}/benchmarks/run_python_bench.py" "${PYTHON_ARGS[@]}"
"${ROOT}/benchmarks/run_csharp_bench.sh" --tier "${TIER}"
"${ROOT}/benchmarks/run_java_bench.sh" --tier "${TIER}"
"${ROOT}/benchmarks/run_rust_bench.sh" --tier "${TIER}"

"${PYTHON_BIN}" "${ROOT}/benchmarks/check_cross_language_rdf.py" \
  --graph "python=${OUT_DIR}/python-${TIER}.jsonld" \
  --graph "csharp=${OUT_DIR}/csharp-${TIER}.jsonld" \
  --graph "java=${OUT_DIR}/java-${TIER}.jsonld" \
  --graph "rust=${OUT_DIR}/rust-${TIER}.jsonld" \
  --out "${OUT_DIR}/rdf-equivalence-${TIER}.json"

"${PYTHON_BIN}" "${ROOT}/benchmarks/generate_release_report.py" \
  --report "${OUT_DIR}/python-${TIER}.json" \
  --report "${OUT_DIR}/csharp-${TIER}.json" \
  --report "${OUT_DIR}/java-${TIER}.json" \
  --report "${OUT_DIR}/rust-${TIER}.json" \
  --equivalence "${OUT_DIR}/rdf-equivalence-${TIER}.json" \
  --out "${OUT_DIR}/release-${TIER}.json" \
  --markdown "${OUT_DIR}/release-${TIER}.md"
