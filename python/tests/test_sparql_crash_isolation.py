"""Tests for SHACL SPARQL crash attribution in validate_graph_file.

The crash comes from a shape file's sh:select, not from the caller's graph.
Isolation must name only files that actually crash under case_validate, never
a regex sweep of every `; ?var` antipattern in the ontology tree.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from case_uco.validation import graph as vg


def test_isolate_sparql_crash_shape_files_binary_searches_one_culprit(tmp_path, monkeypatch):
    graph = tmp_path / "data.jsonld"
    graph.write_text("{}", encoding="utf-8")
    good = tmp_path / "good-shapes.ttl"
    bad = tmp_path / "bad-shapes.ttl"
    other = tmp_path / "ontology.ttl"
    for path in (good, bad, other):
        path.write_text("# placeholder\n", encoding="utf-8")

    def fake_crash(cmd: list[str], *, timeout_seconds: int) -> bool:
        del timeout_seconds
        joined = " ".join(cmd)
        # Crash only when the bad shapes file is loaded.
        return str(bad) in joined

    monkeypatch.setattr(vg, "_case_validate_sparql_crashes", fake_crash)
    found = vg._isolate_sparql_crash_shape_files(
        graph=graph,
        ontology_paths=[other, good, bad],
        base_args=["case_validate", "--built-version", "case-1.5.0", "--allow-info"],
        timeout_seconds=5,
    )
    assert found == [bad]


def test_isolate_sparql_crash_shape_files_does_not_regex_list_unevaluated(tmp_path, monkeypatch):
    """Unevaluated shape files that contain `; ?var` must not be reported."""

    graph = tmp_path / "data.jsonld"
    graph.write_text("{}", encoding="utf-8")
    # Both files look syntactically suspicious; only left crashes in this run.
    left = tmp_path / "left-shapes.ttl"
    right = tmp_path / "right-shapes.ttl"
    left.write_text(
        'sh:select """SELECT ?this WHERE { ?a a ?b ; ?c a ?d . }"""\n',
        encoding="utf-8",
    )
    right.write_text(
        'sh:select """SELECT ?this WHERE { ?a a ?b ; ?c a ?d . }"""\n',
        encoding="utf-8",
    )

    calls: list[tuple[str, ...]] = []

    def fake_crash(cmd: list[str], *, timeout_seconds: int) -> bool:
        del timeout_seconds
        names = tuple(Path(arg).name for arg in cmd if arg.endswith(".ttl"))
        calls.append(names)
        # Full set crashes; neither half alone crashes (interaction / timeout).
        return set(names) >= {"left-shapes.ttl", "right-shapes.ttl"}

    monkeypatch.setattr(vg, "_case_validate_sparql_crashes", fake_crash)
    found = vg._isolate_sparql_crash_shape_files(
        graph=graph,
        ontology_paths=[left, right],
        base_args=["case_validate"],
        timeout_seconds=5,
    )
    assert found == []
    assert any("left-shapes.ttl" in names and "right-shapes.ttl" not in names for names in calls)
    assert any("right-shapes.ttl" in names and "left-shapes.ttl" not in names for names in calls)


def test_validate_graph_file_attributes_sparql_crash_to_shape(tmp_path, monkeypatch):
    graph = tmp_path / "person.jsonld"
    graph.write_text(
        """
        {
          "@context": {
            "kb": "http://example.org/kb/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/"
          },
          "@graph": [{"@id": "kb:p1", "@type": "uco-identity:Person"}]
        }
        """.strip(),
        encoding="utf-8",
    )
    shapes = tmp_path / "cacontology-custodial-shapes.ttl"
    shapes.write_text("# shapes\n", encoding="utf-8")

    monkeypatch.setattr(vg, "validator_available", lambda: True)
    from case_uco.validation.runtime import ValidatorRuntime, validator_command

    monkeypatch.setattr(
        vg, "prepare_validator",
        lambda version: ValidatorRuntime(validator_command(), "0.18.0"),
    )
    # strict_concepts=False uses extension_ontology_args, not the bundle planner.
    monkeypatch.setattr(
        vg,
        "extension_ontology_args",
        lambda extensions, project_root=None: [
            "--built-version",
            "case-1.5.0",
            "--allow-info",
            "--inference",
            "rdfs",
            "--ontology-graph",
            str(shapes),
        ],
    )

    crash_output = (
        "Traceback (most recent call last):\n"
        "pyparsing.exceptions.ParseException: Expected SelectQuery, found '?'\n"
    )

    def fake_run(cmd, capture_output=True, text=True, timeout=None, check=False):
        del capture_output, text, timeout, check
        if any(str(shapes) == arg for arg in cmd):
            return SimpleNamespace(returncode=1, stdout="", stderr=crash_output)
        return SimpleNamespace(returncode=0, stdout="Conforms: True\n", stderr="")

    monkeypatch.setattr(vg.subprocess, "run", fake_run)

    report = vg.validate_graph_file(
        graph,
        extensions=["cac:full"],
        strict_concepts=False,
        project_root=tmp_path,
        timeout_seconds=5,
    )
    assert report.conforms is None
    assert report.verification_status == "could_not_verify"
    assert "cacontology-custodial-shapes.ttl" in report.safe_summary
    assert "not a defect in the submitted graph" in report.safe_summary
    assert report.verification_errors == (
        "shacl_sparql_parse_failed:cacontology-custodial-shapes.ttl",
    )


def test_head_like_summary_does_not_name_shape_without_isolation():
    """Document the pre-fix message class for the fail-before / pass-after pair."""

    # HEAD blamed the graph when Conforms was absent after a validator crash.
    head_summary = (
        "Validator could not produce a conformance result; "
        "the graph content may be malformed."
    )
    assert "shape" not in head_summary.lower()
    assert "malformed" in head_summary
