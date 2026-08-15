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
