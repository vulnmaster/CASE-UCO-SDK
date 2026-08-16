#!/usr/bin/env bash
# Full synthetic Java benchmark harness (#81).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER="${1:-small}"
if [[ "${1:-}" == "--tier" ]]; then
  TIER="${2:-small}"
fi
REPEATS="${CASE_UCO_BENCH_REPEATS:-}"
OUT_DIR="${ROOT}/artifacts/bench"
mkdir -p "${OUT_DIR}"
RESULT="${OUT_DIR}/java-${TIER}.json"
GRAPH="${OUT_DIR}/java-${TIER}.jsonld"
cd "${ROOT}/java"
mvn -q -DskipTests compile
# Bypass pom exec.mainClass (SmokeTest) — run CatalogBench on the compile classpath.
ARGS=(--tier "${TIER}" --graph-out "${GRAPH}")
if [[ -n "${REPEATS}" ]]; then ARGS+=(--repeats "${REPEATS}"); fi
java -cp target/classes org.caseontology.bench.CatalogBench "${ARGS[@]}" | tee "${RESULT}"
grep -q '"language": "java"' "${RESULT}"
test -s "${RESULT}"
test -s "${GRAPH}"
echo "Wrote ${RESULT}"
