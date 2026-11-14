"""Offline tests for the weekly freshness gate, using a fake GitHub API."""

import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import urllib.error

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "check_upstream_freshness", ROOT / "scripts/check_upstream_freshness.py"
)
freshness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freshness)


@pytest.fixture
def checkout(tmp_path, monkeypatch):
    monkeypatch.delenv("SOLVEIT_ONTOLOGY_AHEAD_THRESHOLD", raising=False)
    directory = tmp_path / "ontology/solveit"
    directory.mkdir(parents=True)
    manifest = json.loads((ROOT / "ontology/solveit/manifest.json").read_text())
    manifest["provenance"].update(ontology_commit="0" * 40, ontology_version="0.2.17")
    data = b"# Synthetic vendored fixture\n"
    (directory / "example.ttl").write_bytes(data)
    manifest["provenance"]["sha256"] = {"example.ttl": hashlib.sha256(data).hexdigest()}
    (directory / "manifest.json").write_text(json.dumps(manifest))
    upper = tmp_path / "ontology/upper"
    upper.mkdir()
    (upper / "provenance.json").write_text(json.dumps({"files": {
        "example.ttl": {"source_repo": "https://github.com/example/shapes", "source_commit": "pinned"}
    }}))
    monkeypatch.setattr(freshness, "gitlink_sha", lambda root, path: "pinned")
    return tmp_path


def fake_api(monkeypatch, checkout, *, ahead=0, version="0.2.17", branch_drift=False,
             kb_release="v0.2026-06", cac_ahead=None, comparison_count=None,
             module_commits=None, path_error=None):
    provenance = json.loads((checkout / "ontology/solveit/manifest.json").read_text())["provenance"]
    pinned = provenance["ontology_commit"]
    head = pinned if ahead == 0 else f"{ahead:040x}"
    commits = [{"sha": f"{i:040x}"} for i in range(1, ahead + 1)]
    if module_commits is None:
        module_commits = {freshness.ONTOLOGY_FILES[0]: [commit["sha"] for commit in commits]}
    calls = []

    def api(url):
        calls.append(url)
        route = url.removeprefix(freshness.API + "/")
        if route == f"{freshness.SOLVEIT}/commits/main":
            return {"sha": head}
        if route == f"{freshness.SOLVEIT}/compare/{pinned}...{head}":
            return {"ahead_by": ahead, "commits": commits[:comparison_count]}
        for name in freshness.ONTOLOGY_FILES:
            if route == f"{freshness.SOLVEIT}/commits?sha={head}&path={name}&per_page=100":
                if name == path_error:
                    raise urllib.error.HTTPError(url, 503, "synthetic API failure", None, None)
                return [{"sha": sha} for sha in module_commits.get(name, [])]
        if route == f"{freshness.SOLVEIT}/contents/VERSION?ref={head}":
            return {"encoding": "base64", "content": base64.b64encode((version + "\n").encode()).decode()}
        if route == "SOLVE-IT-DF/solve-it/releases/latest":
            return {"tag_name": kb_release}
        if route == f"{freshness.CAC}/releases/latest":
            return {"tag_name": "v1"}
        if route == f"{freshness.CAC}/commits/v1":
            return {"sha": "pinned" if cac_ahead is None else "release"}
        if route == f"{freshness.CAC}/compare/pinned...release":
            return {"ahead_by": cac_ahead}
        branch_repos = ["ucoProject/UCO", "casework/CASE", "UNHSAILLab/Adversary-Engagement-Ontology", "example/shapes"]
        if route in branch_repos:
            return {"default_branch": "develop"}
        if route in [f"{repo}/commits/develop" for repo in branch_repos]:
            return {"sha": "new-head" if branch_drift else "pinned"}
        pytest.fail(f"Unexpected API request: {url}")

    monkeypatch.setattr(freshness, "api", api)
    return calls


def set_old_pin(checkout):
    path = checkout / "ontology/solveit/manifest.json"
    manifest = json.loads(path.read_text())
    manifest["provenance"].update(ontology_commit="f" * 40, ontology_version="0.2.11")
    path.write_text(json.dumps(manifest))


@pytest.mark.parametrize("ahead,version,expected", [
    (42, "0.2.17", 1),  # Both material drift signals.
    (42, "0.2.11", 1),  # Commit lag alone.
    (1, "0.2.17", 1),   # VERSION alone, below the commit threshold.
])
def test_old_pin_fails(checkout, monkeypatch, capsys, ahead, version, expected):
    set_old_pin(checkout)
    fake_api(monkeypatch, checkout, ahead=ahead, version=version)
    assert freshness.main(["--root", str(checkout)]) == expected
    assert "::error::" in capsys.readouterr().out


def test_new_pin_passes(checkout, monkeypatch, capsys):
    calls = fake_api(monkeypatch, checkout)
    assert freshness.main(["--root", str(checkout)]) == 0
    assert not any("tags" in call for call in calls)
    assert not any("&path=" in call for call in calls)
    out = capsys.readouterr().out
    assert "ahead_by=0 (ontology-file commits=0)" in out
    assert "::warning::" not in out
    assert "::error::" not in out


def test_ontology_files_match_sync_tool(monkeypatch):
    # Keep the sync tool's import-time sys.path change local to this test.
    monkeypatch.setattr(sys, "path", sys.path.copy())
    spec = importlib.util.spec_from_file_location(
        "sync_solveit", ROOT / "mcp_server/tools/sync_solveit.py"
    )
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    assert freshness.ONTOLOGY_FILES == sync.ONTOLOGY_FILES


@pytest.mark.parametrize("module_count,expected", [(0, 0), (6, 1)])
def test_module_commits_among_automated_drift(checkout, monkeypatch, capsys, module_count, expected):
    calls = fake_api(monkeypatch, checkout, ahead=40, module_commits={
        freshness.ONTOLOGY_FILES[0]: [f"{i:040x}" for i in range(1, module_count + 1)]
    })
    assert freshness.main(["--root", str(checkout)]) == expected
    out = capsys.readouterr().out
    assert f"ahead_by=40 (ontology-file commits={module_count})" in out
    assert sum("&path=" in call for call in calls) == 12
    if expected:
        assert "6 ontology-file commits ahead (threshold 5)" in out
    else:
        assert out.count("::warning::") == 1
        assert "::warning::upstream drift — SOLVE-IT ontology" in out
        assert "::error::" not in out


def test_module_commits_are_distinct_and_only_ahead(checkout, monkeypatch, capsys):
    fake_api(monkeypatch, checkout, ahead=40, module_commits={
        freshness.ONTOLOGY_FILES[0]: [f"{1:040x}", "0" * 40],
        freshness.ONTOLOGY_FILES[1]: [f"{1:040x}", "e" * 40],
    })
    assert freshness.main(["--root", str(checkout), "--ontology-ahead-threshold", "1"]) == 0
    assert "ahead_by=40 (ontology-file commits=1)" in capsys.readouterr().out


@pytest.mark.parametrize("comparison_count", [0, 39])
def test_truncated_comparison_falls_back(checkout, monkeypatch, capsys, comparison_count):
    calls = fake_api(monkeypatch, checkout, ahead=40, comparison_count=comparison_count,
                     module_commits={})
    assert freshness.main(["--root", str(checkout)]) == 1
    out = capsys.readouterr().out
    assert "comparison commits truncated; falling back to ahead_by=40" in out
    assert "ahead_by=40 (ontology-file commits=40)" in out
    assert "40 ontology-file commits ahead (threshold 5)" in out
    assert not any("&path=" in call for call in calls)


@pytest.mark.parametrize("all_ahead,expected", [(True, 1), (False, 0)])
def test_full_path_history_fallback(checkout, monkeypatch, capsys, all_ahead, expected):
    history = [f"{i:040x}" for i in range(1, 101)]
    if not all_ahead:
        history[-1] = "0" * 40
    fake_api(monkeypatch, checkout, ahead=101, module_commits={freshness.ONTOLOGY_FILES[0]: history})
    assert freshness.main(["--root", str(checkout), "--ontology-ahead-threshold", "100"]) == expected
    out = capsys.readouterr().out
    if all_ahead:
        assert "history may be truncated; falling back to ahead_by=101" in out
        assert "101 ontology-file commits ahead (threshold 100)" in out
    else:
        assert "falling back" not in out
        assert "ahead_by=101 (ontology-file commits=99)" in out


def test_path_api_failure_does_not_pass(checkout, monkeypatch, capsys):
    fake_api(monkeypatch, checkout, ahead=40, module_commits={},
             path_error=freshness.ONTOLOGY_FILES[-1])
    assert freshness.main(["--root", str(checkout)]) == 1
    assert "::error::  Could not verify freshness" in capsys.readouterr().out


def test_old_version_fails_without_module_drift(checkout, monkeypatch, capsys):
    set_old_pin(checkout)
    fake_api(monkeypatch, checkout, ahead=40, module_commits={})
    assert freshness.main(["--root", str(checkout)]) == 1
    assert "::error::  SOLVE-IT ontology VERSION:" in capsys.readouterr().out


@pytest.mark.parametrize("ahead", [1, 4, 5])
def test_small_drift_warns_including_threshold(checkout, monkeypatch, capsys, ahead):
    fake_api(monkeypatch, checkout, ahead=ahead)
    assert freshness.main(["--root", str(checkout)]) == 0
    out = capsys.readouterr().out
    assert "::warning::upstream drift — SOLVE-IT ontology" in out
    assert "::error::" not in out


def test_threshold_env_and_cli_override(checkout, monkeypatch):
    fake_api(monkeypatch, checkout, ahead=6)
    assert freshness.main(["--root", str(checkout)]) == 1
    monkeypatch.setenv("SOLVEIT_ONTOLOGY_AHEAD_THRESHOLD", "6")
    assert freshness.main(["--root", str(checkout)]) == 0
    assert freshness.main(["--root", str(checkout), "--ontology-ahead-threshold", "0"]) == 1


@pytest.mark.parametrize("damage", ["mismatch", "missing"])
def test_integrity_failure_is_offline(checkout, monkeypatch, capsys, damage):
    def no_network(url):
        pytest.fail("Offline mode must never call the API")
    monkeypatch.setattr(freshness, "api", no_network)
    path = checkout / "ontology/solveit/example.ttl"
    if damage == "mismatch":
        path.write_text("# Modified synthetic fixture\n")
    else:
        path.unlink()
    assert freshness.main(["--root", str(checkout), "--offline"]) == 1
    assert "::error::  SOLVE-IT integrity: example.ttl" in capsys.readouterr().out


def test_real_manifest_passes_offline(monkeypatch):
    def no_network(url):
        pytest.fail("Offline mode must never call the API")
    monkeypatch.setattr(freshness, "api", no_network)
    assert freshness.main(["--root", str(ROOT), "--offline"]) == 0


def test_other_branch_pins_remain_warnings(checkout, monkeypatch, capsys):
    fake_api(monkeypatch, checkout, branch_drift=True)
    assert freshness.main(["--root", str(checkout)]) == 0
    out = capsys.readouterr().out
    assert out.count("::warning::") == 4
    assert "::error::" not in out


@pytest.mark.parametrize("ahead,expected", [(0, 0), (1, 1)])
def test_cac_release_ancestry_policy(checkout, monkeypatch, ahead, expected):
    fake_api(monkeypatch, checkout, cac_ahead=ahead)
    assert freshness.main(["--root", str(checkout)]) == expected


def test_kb_release_staleness(checkout, monkeypatch, capsys):
    fake_api(monkeypatch, checkout, kb_release="v0.2026-07")
    assert freshness.main(["--root", str(checkout)]) == 1
    assert "SOLVE-IT knowledge base: pinned" in capsys.readouterr().out


def test_api_failure_does_not_pass(checkout, monkeypatch, capsys):
    def unavailable(url):
        raise urllib.error.URLError("synthetic offline failure")
    monkeypatch.setattr(freshness, "api", unavailable)
    assert freshness.main(["--root", str(checkout)]) == 1
    assert "::error::  Could not verify freshness" in capsys.readouterr().out
