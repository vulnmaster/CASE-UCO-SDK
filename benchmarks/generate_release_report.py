#!/usr/bin/env python3
"""Validate and consolidate cross-language benchmark evidence for a release (#81)."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from typing import Any

CORE_WORKLOADS = {
    "catalog",
    "relationship_rich",
    "deserialize_roundtrip",
    "streaming_write",
}
PYTHON_VALIDATION_WORKLOADS = {
    "bundle_resolution",
    "concept_coverage",
    "shacl_validation",
}


def validate_report(path: Path) -> tuple[dict[str, Any], list[str]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    language = str(report.get("language", path.stem))
    if report.get("schema_version") != "2.0.0":
        errors.append(f"{language}: benchmark schema is not 2.0.0")
    workloads = report.get("result")
    if not isinstance(workloads, dict):
        return report, [f"{language}: result must be an object"]
    missing = sorted(CORE_WORKLOADS - set(workloads))
    if missing:
        errors.append(f"{language}: missing core workloads {missing}")
    if language == "python":
        validation_missing = sorted(PYTHON_VALIDATION_WORKLOADS - set(workloads))
        if validation_missing:
            errors.append(f"python: missing validation workloads {validation_missing}")
    repeats = report.get("repeats")
    if not isinstance(repeats, int) or repeats < 1:
        errors.append(f"{language}: repeats must be a positive integer")
    if not isinstance(report.get("process_peak_rss_bytes"), int):
        errors.append(f"{language}: process_peak_rss_bytes is missing")
    for name in CORE_WORKLOADS & set(workloads):
        workload = workloads[name]
        if not isinstance(workload, dict):
            errors.append(f"{language}/{name}: workload must be an object")
            continue
        if not isinstance(workload.get("memory"), dict):
            errors.append(f"{language}/{name}: memory metrics missing")
        if not isinstance(workload.get("dispersion"), dict):
            errors.append(f"{language}/{name}: dispersion metrics missing")
        samples = workload.get("samples")
        if not isinstance(samples, list) or len(samples) != repeats:
            errors.append(f"{language}/{name}: sample count does not match repeats")
    for name, workload in workloads.items():
        if isinstance(workload, dict) and workload.get("status") == "failed":
            errors.append(f"{language}/{name}: workload reported failure")
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="append", type=Path, required=True)
    parser.add_argument("--equivalence", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()

    reports: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    tiers: set[str] = set()
    for path in args.report:
        report, report_errors = validate_report(path)
        language = str(report.get("language", path.stem))
        if language in reports:
            errors.append(f"duplicate language report: {language}")
        reports[language] = report
        tiers.add(str(report.get("tier")))
        errors.extend(report_errors)
    expected_languages = {"python", "csharp", "java", "rust"}
    if set(reports) != expected_languages:
        errors.append(
            f"language set mismatch: expected {sorted(expected_languages)}, "
            f"found {sorted(reports)}"
        )
    if len(tiers) != 1:
        errors.append(f"reports do not share one tier: {sorted(tiers)}")

    equivalence = json.loads(args.equivalence.read_text(encoding="utf-8"))
    if equivalence.get("equivalent") is not True:
        errors.append("cross-language RDF equivalence failed")
    if set(equivalence.get("languages", {})) != expected_languages:
        errors.append("equivalence manifest does not cover all SDK languages")

    tier = next(iter(tiers), "unknown")
    summary: dict[str, Any] = {}
    for language, report in sorted(reports.items()):
        summary[language] = {
            "process_peak_rss_bytes": report.get("process_peak_rss_bytes"),
            "workloads": {
                name: {
                    key: value
                    for key, value in workload.items()
                    if key.endswith("_seconds") or key in {"nodes", "memory", "status"}
                }
                for name, workload in report.get("result", {}).items()
                if isinstance(workload, dict)
            },
        }
    release_report = {
        "suite": "case-uco-release-benchmark-report",
        "schema_version": "1.0.0",
        "tier": tier,
        "status": "ready" if not errors else "failed",
        "errors": errors,
        "host": {
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "rdf_equivalence": equivalence,
        "languages": summary,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(release_report, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# CASE/UCO {tier} benchmark release report",
        "",
        f"Status: **{release_report['status']}**",
        "",
        "| Language | Peak RSS bytes | Catalog build (s) | Catalog serialize (s) |",
        "|---|---:|---:|---:|",
    ]
    for language, report in sorted(reports.items()):
        catalog = report.get("result", {}).get("catalog", {})
        lines.append(
            f"| {language} | {report.get('process_peak_rss_bytes', '')} | "
            f"{catalog.get('build_seconds', '')} | {catalog.get('serialize_seconds', '')} |"
        )
    lines.extend(
        [
            "",
            f"Cross-language RDF equivalent: **{equivalence.get('equivalent')}**",
        ]
    )
    if errors:
        lines.extend(["", "## Errors", "", *[f"- {error}" for error in errors]])
    args.markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(release_report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
