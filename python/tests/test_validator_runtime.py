"""Interpreter selection and honest failures for synthetic graph validation."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from case_uco import CASEGraph
from case_uco.validation import graph, runtime

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def tiny_graph(tmp_path):
    target = tmp_path / "synthetic.jsonld"
    target.write_text(json.dumps({
        "@id": "https://example.org/kb/example",
        "http://www.w3.org/2000/01/rdf-schema#label": "Synthetic record",
    }))
    return target


@pytest.fixture
def prepared_validator(monkeypatch):
    prepared = runtime.ValidatorRuntime(
        runtime.validator_command(), "0.18.0"
    )
    monkeypatch.setattr(graph, "validator_available", lambda: True)
    monkeypatch.setattr(graph, "prepare_validator", lambda version: prepared)
    return prepared


def test_extension_validation_ignores_path_stub(tmp_path, tiny_graph, monkeypatch):
    marker = tmp_path / "stub-invoked"
    stub = tmp_path / "case_validate"
    stub.write_text(
        "#!/bin/sh\n"
        'touch "$VALIDATOR_STUB_MARKER"\n'
        'echo "usage: case_validate --built-version VERSION" >&2\n'
        'echo "case_validate: error: argument --built-version: invalid choice: '\
        "'case-1.5.0'\" >&2\n"
        "exit 2\n"
    )
    stub.chmod(0o755)
    monkeypatch.setenv("VALIDATOR_STUB_MARKER", str(marker))
    monkeypatch.setenv("PATH", str(tmp_path) + os.pathsep + os.environ.get("PATH", ""))
    calls = []
    original_run = subprocess.run

    def record_run(args, **kwargs):
        calls.append(args)
        return original_run(args, **kwargs)

    monkeypatch.setattr(subprocess, "run", record_run)
    report = graph.validate_graph_file(
        tiny_graph, extensions=["cryptoinv"], project_root=str(ROOT), timeout_seconds=45
    )
    assert not marker.exists()
    assert calls and all(args[0] == sys.executable for args in calls)
    assert "malformed" not in report.safe_summary
    assert isinstance(report.conforms, bool)
    assert report.error_code is None
    assert report.verification_status == "complete"
    assert calls[-1][:3] == list(runtime.validator_command())
    assert report.validator_version == "0.18.0"


@pytest.mark.parametrize("rc, stderr, expected", [
    (2, "usage: case_validate\nerror: argument --built-version: invalid choice: 'case-1.5.0'", "validator_version_mismatch"),
    (1, "error: argument --built-version: invalid choice: 'case-1.5.0'", "validator_version_mismatch"),
    (2, "usage: case_validate\nerror: unrecognized arguments: --built-version case-1.5.0", "validator_version_mismatch"),
    (2, "usage: case_validate\nerror: unrecognized arguments: --inference", "validator_execution_failed"),
    (1, "No module named case_utils.case_validate", "validator_unavailable"),
])
def test_argument_failure_mapping(tiny_graph, prepared_validator, monkeypatch, rc, stderr, expected):
    def fail(args, **kwargs):
        assert args[:3] == list(prepared_validator.command)
        return subprocess.CompletedProcess(args, rc, stdout="", stderr=stderr)

    monkeypatch.setattr(graph.subprocess, "run", fail)
    report = graph.validate_graph_file(tiny_graph, extensions=["cryptoinv"])
    assert report.conforms is None
    assert report.error_code == expected
    assert report.verification_status == "could_not_verify"
    assert report.verification_errors == (expected,)
    assert dict(report.stage_status)["coverage_execution"] == "skipped"
    assert "malformed" not in report.safe_summary
    payload = graph.report_to_dict(report)
    assert payload["error_code"] == expected
    assert payload["validator_version"] == prepared_validator.version


def test_launch_failure(tiny_graph, prepared_validator, monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("cannot execute")

    monkeypatch.setattr(graph.subprocess, "run", fail)
    report = graph.validate_graph_file(tiny_graph)
    assert report.conforms is None
    assert report.error_code == "validator_execution_failed"


def test_precheck_rejects_unsupported_version_before_validation(tiny_graph, monkeypatch):
    monkeypatch.setattr(graph, "validator_available", lambda: True)
    calls = []

    def probe(args, **kwargs):
        calls.append(args)
        assert args[:2] == [sys.executable, "-c"]
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps({
            "version": "0.17.0", "built_versions": ["none", "case-1.4.0"],
        }), stderr="")

    monkeypatch.setattr(subprocess, "run", probe)
    report = graph.validate_graph_file(tiny_graph, extensions=["cryptoinv"])
    assert len(calls) == 1
    assert report.conforms is None
    assert report.error_code == "validator_version_mismatch"
    assert "case-1.5.0" in report.safe_summary
    assert report.validator_version == "0.17.0"


@pytest.mark.parametrize("failure", ["missing", "timeout", "oserror", "invalid_json"])
def test_precheck_failure_codes(failure, monkeypatch):
    def probe(args, **kwargs):
        if failure == "timeout":
            raise subprocess.TimeoutExpired(args, 15)
        if failure == "oserror":
            raise OSError("cannot execute")
        return subprocess.CompletedProcess(
            args, 0,
            stdout=json.dumps({"error_code": "validator_unavailable"}) if failure == "missing" else "not JSON",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", probe)
    with pytest.raises(runtime.ValidatorError) as exc:
        runtime.prepare_validator("case-1.5.0")
    assert exc.value.code == (
        "validator_unavailable" if failure == "missing" else "validator_precheck_failed"
    )


def test_casegraph_validate_uses_interpreter(prepared_validator, monkeypatch):
    monkeypatch.setattr(runtime, "prepare_validator", lambda version: prepared_validator)
    calls = []

    def run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, stdout="Conforms: True\n", stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert "Conforms: True" in CASEGraph().validate()
    assert calls[0][:3] == list(prepared_validator.command)
    assert "--allow-info" in calls[0] and "--allow-warning" not in calls[0]

    CASEGraph().validate(allow_info=False, allow_warning=True)
    assert "--allow-info" not in calls[1] and "--allow-warning" in calls[1]


def test_casegraph_validate_accepts_info_from_sdk_relationship_ids():
    """#111: create_relationship mints a non-UUID IRI that UCO reports at sh:Info."""
    try:
        runtime.prepare_validator("case-1.5.0")
    except runtime.ValidatorError:
        pytest.skip("case_validate not installed")
    a = "kb:person-7f9c2a3e-1b4d-4c6e-9a8f-0d1e2f3a4b5c"
    b = "kb:org-2c4e6a8b-3d5f-4a7c-8e9f-1a2b3c4d5e6f"
    g = CASEGraph()
    g.upsert_node(a, types="uco-identity:Person", properties={"uco-core:name": "A"})
    g.upsert_node(b, types="uco-identity:Organization", properties={"uco-core:name": "B"})
    g.create_relationship(a, b, "Employed_By")

    assert g.validate_report().conforms is True
    assert "sh:Info" in g.validate()
    with pytest.raises(RuntimeError, match="Conforms: False"):
        g.validate(allow_info=False)


def test_extension_script_uses_interpreter(tiny_graph, prepared_validator, monkeypatch, tmp_path, capsys):
    spec = importlib.util.spec_from_file_location("validate_extension_script", ROOT / "scripts/validate_extension.py")
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"name": "synthetic", "owl_files": []}))
    monkeypatch.setattr(sys, "argv", [str(script.__file__), str(manifest), str(tiny_graph)])
    monkeypatch.setattr(script, "prepare_validator", lambda: prepared_validator)
    calls = []

    def run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, stdout="Conforms: True\n", stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert script.main() == 0
    assert calls[0][:3] == list(prepared_validator.command)
    assert "Validator version: 0.18.0" in capsys.readouterr().out


@pytest.mark.parametrize("version_arg", [["--built-version", "case-1.5.0"], ["--built-version=case-1.5.0"]])
def test_runtime_cli_checks_requested_version(prepared_validator, monkeypatch, version_arg):
    def prepare(version):
        assert version == "case-1.5.0"
        return prepared_validator

    monkeypatch.setattr(sys, "argv", ["runtime.py", *version_arg, "synthetic.jsonld"])
    monkeypatch.setattr(runtime, "prepare_validator", prepare)

    def run(args, **kwargs):
        assert args == [*prepared_validator.command, *version_arg, "synthetic.jsonld"]
        return subprocess.CompletedProcess(args, 0, stdout="Conforms: True\n", stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert runtime.main() == 0


def test_precheck_uses_console_entry_point_without_main_module(monkeypatch):
    def probe(args, **kwargs):
        assert "__main__" not in args[2]
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps({
            "version": "0.18.0", "built_versions": ["case-1.5.0"],
        }), stderr="")

    monkeypatch.setattr(subprocess, "run", probe)
    prepared = runtime.prepare_validator("case-1.5.0")
    assert prepared.command == (
        sys.executable, "-c",
        "import sys; from case_utils.case_validate import main; "
        "sys.argv[0] = 'case_validate'; sys.exit(main())",
    )
    assert prepared.version == "0.18.0"


def test_validator_unavailable_when_import_fails(monkeypatch):
    def missing(name):
        assert name == "case_utils.case_validate"
        raise ImportError("missing validator dependency")

    monkeypatch.setattr(runtime.importlib, "import_module", missing)
    assert runtime.validator_available() is False
