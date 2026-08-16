#!/usr/bin/env python3
"""Public synthetic CASE/UCO benchmark harness (#73).

Tiers:
  small  — PR/CI (1_000 nodes)
  medium — nightly (10_000 nodes)
  large  — release (100_000 nodes)

Workloads:
  catalog            — independent Tool nodes
  relationship_rich  — devices/files/relationships (dependency partition target)
  deserialize_roundtrip — serialize + cold/warm from_jsonld
  streaming_write    — write_streaming metrics
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import resource
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from case_uco import CASEGraph, clear_class_registry_cache  # noqa: E402


SIZES = {"small": 1_000, "medium": 10_000, "large": 100_000}


def build_catalog(n: int) -> CASEGraph:
    g = CASEGraph()
    for i in range(n):
        # Raw construction deliberately fixes the cross-language RDF fixture.
        g.upsert_node(
            f"kb:tool-{i}",
            types="uco-tool:Tool",
            properties={
                "uco-core:name": f"Tool-{i}",
                "uco-tool:version": "1.0",
            },
        )
    return g


def build_relationship_rich(n: int) -> CASEGraph:
    """n device roots, each with one file + Related_To edge."""
    g = CASEGraph()
    for i in range(n):
        device = f"kb:device-{i}"
        file_id = f"kb:file-{i}"
        g.upsert_node(
            device, types="uco-core:UcoObject", properties={"uco-core:name": f"D{i}"}
        )
        g.upsert_node(
            file_id,
            types="uco-core:UcoObject",
            properties={
                "uco-core:name": f"F{i}",
                "uco-core:object": {"@id": device},
            },
        )
        g.create_relationship(file_id, device, "Contained_Within")
    return g


def run_catalog(n: int) -> dict:
    t0 = time.perf_counter()
    g = build_catalog(n)
    t_build = time.perf_counter() - t0

    t0 = time.perf_counter()
    for i in range(0, n, max(1, n // 100)):
        assert g.contains(f"kb:tool-{i}")
        g.add_property(f"kb:tool-{i}", "uco-core:description", f"bench-{i}")
    t_lookup = time.perf_counter() - t0

    t0 = time.perf_counter()
    payload = g.serialize()
    t_ser = time.perf_counter() - t0

    return {
        "workload": "catalog",
        "nodes": n,
        "build_seconds": round(t_build, 6),
        "lookup_enrich_seconds": round(t_lookup, 6),
        "serialize_seconds": round(t_ser, 6),
        "serialize_bytes": len(payload.encode("utf-8")),
        "estimate_triples": g.estimate_triples(),
    }


def run_relationship_rich(n: int) -> dict:
    t0 = time.perf_counter()
    g = build_relationship_rich(n)
    t_build = time.perf_counter() - t0
    roots = [f"kb:file-{i}" for i in range(0, n, max(1, n // 10))]
    t0 = time.perf_counter()
    parts = g.partition(strategy="roots", roots=roots[:5])
    t_part = time.perf_counter() - t0
    return {
        "workload": "relationship_rich",
        "nodes": len(g),
        "build_seconds": round(t_build, 6),
        "partition_seconds": round(t_part, 6),
        "partition_count": len(parts),
        "estimate_triples": g.estimate_triples(),
    }


def run_deserialize_roundtrip(n: int) -> dict:
    g = build_catalog(n)
    payload = g.serialize()
    clear_class_registry_cache()
    t0 = time.perf_counter()
    cold, _ = CASEGraph.from_jsonld(payload)
    t_cold = time.perf_counter() - t0
    t0 = time.perf_counter()
    warm, _ = CASEGraph.from_jsonld(payload)
    t_warm = time.perf_counter() - t0
    assert len(cold) == n and len(warm) == n
    return {
        "workload": "deserialize_roundtrip",
        "nodes": n,
        "from_jsonld_cold_seconds": round(t_cold, 6),
        "from_jsonld_warm_seconds": round(t_warm, 6),
        "serialize_bytes": len(payload.encode("utf-8")),
    }


def run_streaming_write(n: int, tmp: Path) -> dict:
    g = build_catalog(n)
    out = tmp / "stream.jsonld"
    t0 = time.perf_counter()
    metrics = g.write_streaming(str(out), atomic=True)
    t_stream = time.perf_counter() - t0
    t0 = time.perf_counter()
    g.write(str(tmp / "full.jsonld"))
    t_full = time.perf_counter() - t0
    return {
        "workload": "streaming_write",
        "nodes": n,
        "write_streaming_seconds": round(t_stream, 6),
        "write_full_seconds": round(t_full, 6),
        "bytes_written": metrics["bytes_written"],
    }


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int((len(ordered) - 1) * fraction))]


def measure(workload, repeats: int) -> dict:
    """Run a workload repeatedly and retain medians plus dispersion/memory."""

    samples: list[dict] = []
    peaks: list[int] = []
    for _ in range(repeats):
        gc.collect()
        sample = workload()
        samples.append(sample)
        peaks.append(process_peak_rss_bytes())

    representative = dict(samples[len(samples) // 2])
    timing_keys = sorted(
        key
        for key in samples[0]
        if key.endswith("_seconds") and isinstance(samples[0][key], (int, float))
    )
    dispersion: dict[str, dict[str, float]] = {}
    for key in timing_keys:
        values = [float(sample[key]) for sample in samples]
        representative[key] = round(statistics.median(values), 6)
        dispersion[key] = {
            "min": round(min(values), 6),
            "max": round(max(values), 6),
            "median": round(statistics.median(values), 6),
            "mean": round(statistics.fmean(values), 6),
            "stdev": round(statistics.pstdev(values), 6),
            "p95": round(_percentile(values, 0.95), 6),
        }
    representative["samples"] = samples
    representative["dispersion"] = dispersion
    representative["memory"] = {
        "metric": "process_peak_rss_after_bytes",
        "peak_bytes": max(peaks),
        "median_peak_bytes": int(statistics.median(peaks)),
    }
    return representative


def run_validation_workloads(n: int, tmp: Path) -> dict:
    """Measure bundle/coverage/SHACL stages, reporting unavailable honestly."""

    from case_uco.validation import validator_available
    from case_uco.validation.bundle import clear_bundle_cache, resolve_validation_bundle
    from case_uco.validation.coverage import check_graph_concepts

    project_root = ROOT
    clear_bundle_cache()
    t0 = time.perf_counter()
    cold_bundle = resolve_validation_bundle(project_root=project_root)
    cold_seconds = time.perf_counter() - t0
    t0 = time.perf_counter()
    warm_bundle = resolve_validation_bundle(project_root=project_root)
    warm_seconds = time.perf_counter() - t0
    bundle = {
        "workload": "bundle_resolution",
        "status": "complete",
        "resources": len(cold_bundle.resources),
        "cold_seconds": round(cold_seconds, 6),
        "warm_seconds": round(warm_seconds, 6),
        "warm_cache_status": warm_bundle.cache_status,
    }

    validation_nodes = min(n, 1_000)
    graph = build_catalog(validation_nodes)
    coverage_path = tmp / "coverage.jsonld"
    graph.write_streaming(str(coverage_path))
    t0 = time.perf_counter()
    coverage = check_graph_concepts(
        coverage_path,
        extensions=[],
        selected_profiles=[],
        project_root=project_root,
    )
    coverage_seconds = time.perf_counter() - t0
    coverage_result = {
        "workload": "concept_coverage",
        "status": "complete"
        if coverage.verification_status == "complete"
        else "failed",
        "nodes": validation_nodes,
        "coverage_seconds": round(coverage_seconds, 6),
        "checked_class_count": coverage.checked_class_count,
        "checked_property_count": coverage.checked_property_count,
        "undeclared_total": coverage.undeclared_total,
    }

    shacl_result: dict[str, object] = {
        "workload": "shacl_validation",
        "nodes": min(validation_nodes, 100),
    }
    if not validator_available():
        shacl_result.update(
            status="skipped",
            reason="case_validate is not installed on PATH",
        )
    else:
        validation_graph = build_catalog(min(validation_nodes, 100))
        graph_path = tmp / "validation.jsonld"
        validation_graph.write_streaming(str(graph_path))
        t0 = time.perf_counter()
        report = validation_graph.validate_report(
            project_root=project_root,
            strict_concepts=True,
        )
        shacl_result.update(
            status=(
                "complete" if report.verification_status == "complete" else "failed"
            ),
            validation_seconds=round(time.perf_counter() - t0, 6),
            conforms=report.conforms,
            verification_status=report.verification_status,
        )
    return {
        "bundle_resolution": bundle,
        "concept_coverage": coverage_result,
        "shacl_validation": shacl_result,
    }


def run_tier(n: int, tmp: Path, repeats: int) -> dict:
    result = {
        "catalog": measure(lambda: run_catalog(n), repeats),
        "relationship_rich": measure(
            lambda: run_relationship_rich(max(10, n // 10)), repeats
        ),
        "deserialize_roundtrip": measure(lambda: run_deserialize_roundtrip(n), repeats),
        "streaming_write": measure(lambda: run_streaming_write(n, tmp), repeats),
    }
    result.update(run_validation_workloads(n, tmp))
    return result


def process_peak_rss_bytes() -> int:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(rss if sys.platform == "darwin" else rss * 1024)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=["small", "medium", "large"], default="small")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--graph-out", type=Path, default=None)
    parser.add_argument("--workdir", type=Path, default=None)
    parser.add_argument("--repeats", type=int, default=None)
    args = parser.parse_args()
    workdir = args.workdir or Path("/tmp/case-uco-bench")
    workdir.mkdir(parents=True, exist_ok=True)
    repeats = args.repeats or (1 if args.tier == "large" else 3)
    if repeats < 1:
        parser.error("--repeats must be positive")
    workloads = run_tier(SIZES[args.tier], workdir, repeats)
    result = {
        "suite": "case-uco-synthetic-benchmark",
        "schema_version": "2.0.0",
        "tier": args.tier,
        "language": "python",
        "repeats": repeats,
        "process_peak_rss_bytes": process_peak_rss_bytes(),
        "result": workloads,
    }
    if args.graph_out:
        args.graph_out.parent.mkdir(parents=True, exist_ok=True)
        build_catalog(SIZES[args.tier]).write_streaming(str(args.graph_out))
        result["equivalence_graph"] = os.path.relpath(args.graph_out, ROOT)
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
