"""Tests for dual-root extension directory resolution (v1.19.0)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import extension_paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class TestExtensionPaths:
    def test_upstream_vendored_extensions_live_under_ontology(self):
        for name in ("cac", "aeo", "solveit"):
            found = extension_paths.find_extension_dir(name, PROJECT_ROOT)
            assert found is not None, name
            assert found.parent.name == "ontology", name
            assert (found / "manifest.json").is_file()

    def test_sdk_native_extensions_live_under_extensions(self):
        for name in ("attack-technique", "legalproc", "toolcap", "trajectories"):
            found = extension_paths.find_extension_dir(name, PROJECT_ROOT)
            assert found is not None, name
            assert found.parent.name == "extensions", name

    def test_search_order_prefers_sdk_native_on_name_collision(self, tmp_path):
        native = tmp_path / "extensions" / "demo"
        upstream = tmp_path / "ontology" / "demo"
        native.mkdir(parents=True)
        upstream.mkdir(parents=True)
        (native / "manifest.json").write_text('{"name":"demo","version":"1.0.0"}')
        (upstream / "manifest.json").write_text('{"name":"demo","version":"9.9.9"}')
        found = extension_paths.find_extension_dir("demo", tmp_path)
        assert found == native

    def test_non_extension_ontology_dirs_are_ignored(self):
        assert extension_paths.find_extension_dir("CASE", PROJECT_ROOT) is None
        assert extension_paths.find_extension_dir("UCO", PROJECT_ROOT) is None
        assert extension_paths.find_extension_dir("upper", PROJECT_ROOT) is None

    def test_iter_extension_dirs_includes_both_roots(self):
        names = {p.name for p in extension_paths.iter_extension_dirs(PROJECT_ROOT)}
        assert {"cac", "aeo", "solveit", "legalproc", "attack-technique", "trajectories"} <= names

    def test_extension_dir_falls_back_to_native_root(self, tmp_path):
        path = extension_paths.extension_dir("brand-new", tmp_path)
        assert path == tmp_path / "extensions" / "brand-new"
