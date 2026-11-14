#!/usr/bin/env python3
"""Validate extension ontology data against its manifest-declared TTL files.

Usage:
    python scripts/validate_extension.py ontology/cac/manifest.json data.jsonld
    python scripts/validate_extension.py ontology/aeo/manifest.json data.jsonld

Reads the manifest.json to discover all OWL and SHACL files, then invokes
case_validate with the appropriate --ontology-graph flags.

Manifest ``depends_on`` entries are expanded transitively. Without that, an
extension that builds on another (rico on legalproc, elder-fraud on
trajectories) validates against only its own shapes, and the borrowed
constraints never run — the graph passes because nothing checked it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "python"))

from case_uco.validation.runtime import (
    ValidatorError,
    prepare_validator,
    validator_error_code,
    validator_error_message,
)
# Extensions live under either root; see mcp_server/extension_paths.py.
EXTENSION_ROOTS = ("extensions", "ontology")


def _find_manifest(ext_name: str) -> Path | None:
    for root in EXTENSION_ROOTS:
        candidate = PROJECT_ROOT / root / ext_name / "manifest.json"
        if candidate.is_file():
            return candidate
    return None


def _collect_graphs(manifest_path: Path, seen: set[str]) -> list[str]:
    """Manifest-declared ontology files, plus those of its depends_on closure."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ext_dir = manifest_path.parent
    name = manifest.get("name", ext_dir.name)
    if name in seen:
        return []
    seen.add(name)

    graphs: list[str] = []
    for dep in manifest.get("depends_on", []):
        dep_manifest = _find_manifest(dep)
        if dep_manifest is None:
            # Fail loudly: a silently missing dependency means the shapes that
            # were supposed to constrain this graph never loaded.
            print(
                f"  ERROR: '{name}' depends_on '{dep}', which has no manifest",
                file=sys.stderr,
            )
            raise SystemExit(1)
        graphs.extend(_collect_graphs(dep_manifest, seen))

    for key in ("owl_files", "shacl_files", "bridge_files"):
        for rel_path in manifest.get(key, []):
            full_path = ext_dir / rel_path
            if full_path.exists():
                graphs.append(str(full_path))
            else:
                print(f"  Warning: {rel_path} not found (skipping)", file=sys.stderr)
    return graphs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate extension data against its manifest-declared TTL files.",
    )
    parser.add_argument("manifest", type=Path, help="path to the extension manifest.json")
    parser.add_argument("data", type=Path, help="path to the graph to validate")
    parser.add_argument(
        "--inference",
        choices=("none", "rdfs", "owlrl", "both"),
        help="entailment regime to apply before validation. Extensions whose "
        "exemplars reference vocabulary individuals declared in an ontology "
        "graph need 'rdfs'.",
    )
    parser.add_argument(
        "--allow-info",
        action="store_true",
        help="do not fail on informational results (e.g. UUID IRI suggestions).",
    )
    parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="do not fail on warning-severity results.",
    )
    ns = parser.parse_args()

    manifest_path = ns.manifest
    data_path = ns.data

    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    if not data_path.exists():
        print(f"Data file not found: {data_path}", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ext_dir = manifest_path.parent
    ext_name = manifest.get("name", ext_dir.name)

    seen: set[str] = set()
    ontology_graphs = _collect_graphs(manifest_path, seen)
    dependencies = sorted(seen - {ext_name})

    print(f"Validating with extension '{ext_name}'")
    if dependencies:
        print(f"  Dependencies: {', '.join(dependencies)}")
    print(f"  Ontology graphs: {len(ontology_graphs)}")
    print(f"  Data file: {data_path}")

    try:
        runtime = prepare_validator()
    except ValidatorError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 2
    print(f"  Validator version: {runtime.version}")
    cmd = list(runtime.command)
    for graph_path in ontology_graphs:
        cmd.extend(["--ontology-graph", graph_path])
    if ns.inference:
        cmd.extend(["--inference", ns.inference])
    if ns.allow_info:
        cmd.append("--allow-info")
    if ns.allow_warnings:
        cmd.append("--allow-warnings")
    cmd.append(str(data_path))

    print(f"  Running: {' '.join(cmd[:6])} ... ({len(cmd) - 1} args total)")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError:
        print("validator_execution_failed: CASE validator could not run", file=sys.stderr)
        return 2
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    code = validator_error_code(result.returncode, result.stderr)
    if code:
        print(f"{code}: {validator_error_message(code, None)}", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
