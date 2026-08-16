#!/usr/bin/env bash
# Full synthetic C# benchmark harness (#81).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER="${1:-small}"
if [[ "${1:-}" == "--tier" ]]; then
  TIER="${2:-small}"
fi
REPEATS="${CASE_UCO_BENCH_REPEATS:-}"
OUT_DIR="${ROOT}/artifacts/bench"
mkdir -p "${OUT_DIR}"
RESULT="${OUT_DIR}/csharp-${TIER}.json"
GRAPH="${OUT_DIR}/csharp-${TIER}.jsonld"
ARGS=(--tier "${TIER}" --graph-out "${GRAPH}")
if [[ -n "${REPEATS}" ]]; then ARGS+=(--repeats "${REPEATS}"); fi
dotnet run --project "${ROOT}/csharp/CaseUco.Bench/CaseUco.Bench.csproj" -c Release -v q -- "${ARGS[@]}" | tee "${RESULT}"
test -s "${RESULT}"
test -s "${GRAPH}"
echo "Wrote ${RESULT}"
