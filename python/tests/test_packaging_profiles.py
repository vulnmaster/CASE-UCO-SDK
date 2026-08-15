"""Wheel-oriented profile load: packaged data must be reachable without CASE_UCO_TOPOLOGY_DIR."""

from __future__ import annotations

import os
from pathlib import Path

from case_uco.topology.paths import profile_dirs
from case_uco.topology.profiles import clear_profile_cache, get_profile


def test_packaged_profiles_directory_exists() -> None:
    packaged = Path(__file__).resolve().parents[1] / "case_uco" / "topology" / "data" / "profiles"
    assert packaged.is_dir()
    assert (packaged / "MinimalForensics.json").is_file()
    assert (packaged / "profile.schema.json").is_file()


def test_get_profile_without_env(monkeypatch) -> None:
    monkeypatch.delenv("CASE_UCO_TOPOLOGY_DIR", raising=False)
    clear_profile_cache()
    profile = get_profile("MinimalForensics")
    assert profile is not None
    assert profile.id == "MinimalForensics"
    dirs = profile_dirs()
    assert any(d.name == "profiles" for d in dirs)


def test_packaged_v2_surfaces_exist() -> None:
    data = Path(__file__).resolve().parents[1] / "case_uco" / "topology" / "data"
    assert (data / "workflows" / "field-triage.json").is_file()
    assert (data / "workflows" / "hash-intelligence-vics.json").is_file()
    assert (data / "trajectories" / "grooming-phase.json").is_file()
    assert (data / "contracts" / "default-bindings.json").is_file()
    assert (data / "vics.json").is_file()


def test_load_v2_surfaces_without_env(monkeypatch) -> None:
    monkeypatch.delenv("CASE_UCO_TOPOLOGY_DIR", raising=False)
    from case_uco.adapters import list_adapters
    from case_uco.contracts import load_contract
    from case_uco.trajectories import list_trajectories, load_trajectory
    from case_uco.workflow import get_workflow, list_workflows

    assert load_contract("HashIntelligence").checks
    assert load_trajectory("grooming-phase").id == "grooming-phase"
    assert get_workflow("field-triage") is not None
    assert any(w.id == "hash-intelligence-vics" for w in list_workflows())
    assert any(t.id == "grooming-phase" for t in list_trajectories())
    assert {a["id"] for a in list_adapters()} >= {"photodna", "vics-catalog", "hash-match"}


def test_workflow_cli_lists_surfaces() -> None:
    from case_uco.workflow.cli import main

    assert main(["list"]) == 0
    assert main(["trajectories"]) == 0
    assert main(["adapters"]) == 0
