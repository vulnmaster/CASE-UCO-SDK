"""Public validation helpers accept filesystem paths from callers and configs."""

import json
import os
from pathlib import Path
from subprocess import CompletedProcess

import pytest

from case_uco.validation import bundle, coverage, extension_paths, graph
from case_uco.validation.runtime import ValidatorRuntime, validator_command


class CustomPath(os.PathLike[str]):
    def __init__(self, path: Path):
        self.path = path

    def __fspath__(self) -> str:
        return str(self.path)


@pytest.fixture
def synthetic_project(tmp_path):
    ext = tmp_path / "extensions" / "synthetic"
    ext.mkdir(parents=True)
    (ext / "manifest.json").write_text(json.dumps({
        "name": "synthetic", "version": "1.0.0",
        "namespaces": {"example": "https://example.org/synthetic/"},
        "owl_files": ["ontology.ttl"],
    }))
    (ext / "ontology.ttl").write_text(
        "<https://example.org/synthetic/Record> a "
        "<http://www.w3.org/2002/07/owl#Class> .\n"
    )
    target = tmp_path / "graph.jsonld"
    target.write_text(json.dumps({
        "@id": "https://example.org/kb/example",
        "@type": "https://example.org/synthetic/Record",
    }))
    return tmp_path, ext, target


@pytest.mark.parametrize("root_type", [str, CustomPath, Path])
def test_project_root_helpers(synthetic_project, root_type):
    root, ext, target = synthetic_project
    supplied = root_type(root)
    assert extension_paths.extension_roots(supplied)[0] == root / "extensions"
    assert extension_paths.native_extension_root(supplied) == root / "extensions"
    assert extension_paths.find_extension_dir("synthetic", supplied) == ext
    assert extension_paths.extension_dir("synthetic", supplied) == ext
    assert extension_paths.extension_manifest_path("synthetic", supplied) == ext / "manifest.json"
    assert extension_paths.iter_extension_dirs(supplied) == [ext]
    assert graph.resolve_extension_dependencies(["synthetic"], supplied) == ["synthetic"]
    assert graph.load_extension_ontology_paths("synthetic", project_root=supplied) == [ext / "ontology.ttl"]
    assert graph.extension_has_validation_subset("synthetic", supplied) is False
    assert str(ext / "ontology.ttl") in graph.extension_ontology_args(["synthetic"], supplied)
    assert graph.required_extensions_for_graph(json.loads(target.read_text()), supplied) == ["synthetic"]
    resolved = bundle.resolve_validation_bundle(extensions=["synthetic"], project_root=supplied)
    assert resolved.resources[0].path == "extensions/synthetic/ontology.ttl"
    identity = bundle.hash_validation_bundle_identity(extensions=["synthetic"], project_root=supplied)
    assert identity["bundle_fingerprint"] == resolved.fingerprint
    terms = coverage.load_declared_terms(project_root=supplied, extensions=["synthetic"])
    assert "https://example.org/synthetic/Record" in terms.classes
    report = coverage.check_graph_concepts(target, project_root=supplied, extensions=["synthetic"])
    assert not report.undeclared_classes


@pytest.mark.parametrize("root_type", [str, CustomPath])
def test_validate_graph_file_project_root(synthetic_project, root_type, monkeypatch):
    root, _, target = synthetic_project
    monkeypatch.setattr(graph, "validator_available", lambda: True)
    monkeypatch.setattr(graph, "prepare_validator", lambda version: ValidatorRuntime(
        validator_command(), "0.18.0"
    ))
    monkeypatch.setattr(graph.subprocess, "run", lambda args, **kwargs: CompletedProcess(
        args, 0, stdout="Conforms: True\n", stderr=""
    ))
    report = graph.validate_graph_file(
        target, project_root=root_type(root), extensions=["synthetic"]
    )
    assert report.conforms is True
    assert report.verification_status == "complete"
    assert report.bundle_fingerprint


def test_none_project_root_uses_default():
    assert extension_paths.extension_roots(None) == extension_paths.extension_roots()
    assert bundle.resolve_validation_bundle(project_root=None, use_cache=False) == bundle.resolve_validation_bundle(use_cache=False)
    assert graph.required_extensions_for_graph({}, None) == []

