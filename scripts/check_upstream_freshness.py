#!/usr/bin/env python3
"""Check vendored integrity and upstream freshness; --offline needs no network."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com/repos"
SOLVEIT = "SOLVE-IT-DF/solve-it-ontology"
CAC = "Project-VIC-International/CAC-Ontology"

# Mirrored from sync_solveit.ONTOLOGY_FILES because importing that tool mutates
# sys.path. test_ontology_files_match_sync_tool guards against list drift.
ONTOLOGY_FILES = [
    "solve_it_core.ttl",
    "solve_it_core_shapes.ttl",
    "solve_it_observable.ttl",
    "solve_it_observable_acquisition.ttl",
    "solve_it_observable_search.ttl",
    "solve_it_observable_timeline.ttl",
    "solve_it_observable_shapes.ttl",
    "solve_it_analysis.ttl",
    "solve_it_analysis_shapes.ttl",
    "solve_it_sqlite.ttl",
    "solve_it_tool_profile.ttl",
    "solve_it_weakness_assessment.ttl",
]


def api(url: str) -> dict | list:
    """The sole network boundary, replaceable with a fake in tests."""
    headers = {"User-Agent": "case-uco-sdk-freshness"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def gitlink_sha(root: Path, path: str) -> str:
    out = subprocess.run(
        ["git", "ls-tree", "HEAD", path], cwd=root,
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return out[2] if len(out) >= 3 else ""


def default_branch_head(repo: str) -> str:
    branch = api(f"{API}/{repo}").get("default_branch", "main")
    return api(f"{API}/{repo}/commits/{branch}").get("sha", "")


def latest_release(repo: str) -> str:
    try:
        return api(f"{API}/{repo}/releases/latest").get("tag_name", "")
    except urllib.error.HTTPError:
        return ""


def check_integrity(manifest_path: Path, provenance: dict) -> list[str]:
    errors = []
    checksums = provenance.get("sha256", {})
    if not checksums:
        return [f"{manifest_path}: missing provenance.sha256"]
    for name, expected in checksums.items():
        path = manifest_path.parent / name
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(f"SOLVE-IT integrity: {name}: {exc}")
            continue
        if actual != expected:
            errors.append(f"SOLVE-IT integrity: {name}: sha256 mismatch (expected {expected}, got {actual})")
    if not errors:
        print(f"SOLVE-IT integrity: all {len(checksums)} vendored sha256 checks passed.")
    return errors


def ontology_commits_ahead(comparison: dict, ont_head: str) -> int:
    """Count distinct ahead commits touching vendored upstream module files."""
    ahead = comparison["ahead_by"]
    if ahead == 0:
        return 0
    commits = comparison.get("commits", [])
    if len(commits) < ahead:
        print(f"SOLVE-IT ontology: comparison commits truncated; falling back to ahead_by={ahead}.")
        return ahead
    ahead_shas = {commit["sha"] for commit in commits}
    ontology_shas: set[str] = set()
    for name in ONTOLOGY_FILES:
        history = api(f"{API}/{SOLVEIT}/commits?sha={ont_head}&path={name}&per_page=100")
        if len(history) == 100 and all(commit["sha"] in ahead_shas for commit in history):
            print(f"SOLVE-IT ontology: {name} history may be truncated; falling back to ahead_by={ahead}.")
            return ahead
        ontology_shas.update(commit["sha"] for commit in history if commit["sha"] in ahead_shas)
    return len(ontology_shas)


def check_upstream(root: Path, provenance: dict, threshold: int) -> tuple[list[str], list[str]]:
    stale: list[str] = []
    drift: list[str] = []
    for repo, path in [
        ("ucoProject/UCO", "ontology/UCO"),
        ("casework/CASE", "ontology/CASE"),
        ("UNHSAILLab/Adversary-Engagement-Ontology", "ontology/aeo/ontology"),
    ]:
        pinned = gitlink_sha(root, path)
        head = default_branch_head(repo)
        print(f"{path}: pinned {pinned[:12]}, upstream {head[:12]}")
        if head and pinned and head != pinned:
            drift.append(f"{path}: pinned {pinned[:12]}, upstream default branch is {head[:12]}")

    cac_pinned = gitlink_sha(root, "ontology/cac/ontology")
    cac_release = latest_release(CAC)
    cac_release_sha = ""
    if cac_release:
        try:
            cac_release_sha = api(f"{API}/{CAC}/commits/{cac_release}").get("sha", "")
        except urllib.error.HTTPError:
            pass
    print(f"ontology/cac/ontology: pinned {cac_pinned[:12]}, latest release {cac_release} ({cac_release_sha[:12]})")
    if cac_release_sha and cac_pinned and cac_release_sha != cac_pinned:
        # A pin ahead of the latest release is legitimate; preserve that policy.
        try:
            comparison = api(f"{API}/{CAC}/compare/{cac_pinned}...{cac_release_sha}")
            release_ahead = comparison.get("ahead_by", 0) > 0
        except urllib.error.HTTPError:
            release_ahead = True
        if release_ahead:
            stale.append(f"CAC Ontology: pinned {cac_pinned[:12]}, upstream released {cac_release} ({cac_release_sha[:12]})")

    pinned_release = provenance["knowledge_base_release"]
    pinned_commit = provenance["ontology_commit"]
    pinned_version = provenance["ontology_version"]
    kb_release = latest_release("SOLVE-IT-DF/solve-it")
    # Upstream has no ontology tags. Resolve main once so VERSION and the
    # comparison refer to the same snapshot even if main moves during the run.
    ont_head = api(f"{API}/{SOLVEIT}/commits/main")["sha"]
    comparison = api(f"{API}/{SOLVEIT}/compare/{pinned_commit}...{ont_head}")
    ahead = comparison["ahead_by"]
    ontology_ahead = ontology_commits_ahead(comparison, ont_head)
    version_file = api(f"{API}/{SOLVEIT}/contents/VERSION?ref={ont_head}")
    if version_file["encoding"] != "base64":
        raise ValueError("Unexpected encoding for SOLVE-IT VERSION")
    version = base64.b64decode(version_file["content"]).decode("utf-8").strip()
    if not version or not pinned_commit or not pinned_version:
        raise ValueError("Missing SOLVE-IT ontology commit or VERSION")
    print(f"SOLVE-IT KB: pinned {pinned_release}, latest {kb_release}")
    print(f"SOLVE-IT ontology: pinned {pinned_commit[:12]} ({pinned_version}), upstream {ont_head[:12]} ({version}), ahead_by={ahead} (ontology-file commits={ontology_ahead})")
    if kb_release and kb_release != pinned_release:
        stale.append(f"SOLVE-IT knowledge base: pinned {pinned_release}, upstream released {kb_release}")
    if version != pinned_version:
        stale.append(f"SOLVE-IT ontology VERSION: pinned {pinned_version}, upstream {version}")
    if ontology_ahead > threshold:
        stale.append(f"SOLVE-IT ontology: upstream main is {ontology_ahead} ontology-file commits ahead (threshold {threshold})")
    elif ont_head != pinned_commit:
        drift.append(f"SOLVE-IT ontology: pinned {pinned_commit[:12]}, upstream main is {ont_head[:12]} ({ahead} commits ahead)")

    upper = json.loads((root / "ontology/upper/provenance.json").read_text())["files"]
    for rel, meta in sorted(upper.items()):
        repo_url = meta.get("source_repo", "")
        pinned_sha = meta.get("source_commit", "")
        if not repo_url or not pinned_sha:
            continue
        head = default_branch_head(repo_url.removeprefix("https://github.com/"))
        if head and head != pinned_sha:
            drift.append(f"ontology/upper/{rel}: pinned {pinned_sha[:12]}, upstream is {head[:12]}")
    return stale, drift


def nonnegative_int(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("threshold must be nonnegative")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Only check local SOLVE-IT sha256 integrity")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root (defaults to this checkout)")
    parser.add_argument(
        "--ontology-ahead-threshold", type=nonnegative_int,
        default=os.environ.get("SOLVEIT_ONTOLOGY_AHEAD_THRESHOLD", "5"),
        help="Fail above this many ontology-file commits ahead (env SOLVEIT_ONTOLOGY_AHEAD_THRESHOLD; default 5)",
    )
    args = parser.parse_args(argv)
    stale: list[str] = []
    drift: list[str] = []
    try:
        manifest_path = args.root / "ontology/solveit/manifest.json"
        provenance = json.loads(manifest_path.read_text())["provenance"]
        stale.extend(check_integrity(manifest_path, provenance))
        if not args.offline:
            upstream_stale, drift = check_upstream(args.root, provenance, args.ontology_ahead_threshold)
            stale.extend(upstream_stale)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        stale.append(f"Could not verify freshness: {exc}")
    for line in drift:
        print(f"::warning::upstream drift — {line} (refresh with `make sync-upstream` when convenient)")
    if stale:
        print("::error::Vendored integrity or freshness check failed — run `make sync-upstream` and review the diffs:")
        for line in stale:
            print(f"::error::  {line}")
        return 1
    print("Vendored integrity check passed." if args.offline else "All vendored snapshots pass freshness and integrity checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
