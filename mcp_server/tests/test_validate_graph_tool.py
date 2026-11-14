"""The validate_graph MCP tool accepts a local ontology and RDFS inference (issue #93).

validate_graph_file and the critic tools already take extra_ontology_graphs
and force_rdfs_inference; the validate_graph tool did not, so a graph using
a candidate T-Box conformed through the SDK and failed through the tool.
All fixtures are synthetic.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import server  # noqa: E402
import workspace_policy  # noqa: E402
from case_uco.validation.graph import validate_graph_file, validator_available  # noqa: E402

needs_validator = pytest.mark.skipif(
    not validator_available(), reason="case_validate not installed"
)

WIDGET = "http://example.org/ont/Widget"
WIDGET_TTL = """\
@prefix ex: <http://example.org/ont/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Widget a owl:Class ;
    rdfs:subClassOf <https://ontology.unifiedcyberontology.org/uco/core/UcoObject> .
"""
WIDGET_GRAPH = {
    "@context": {
        "ex": "http://example.org/ont/",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "kb": "http://example.org/kb/",
    },
    "@graph": [
        {
            "@id": "kb:widget-5f0c2a7e-3b1d-4c8e-9a6f-2d7b1e4c8a90",
            "@type": "ex:Widget",
            "uco-core:name": "one widget",
        }
    ],
}


def _write_fixtures(directory: Path) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    ontology = directory / "widget.ttl"
    ontology.write_text(WIDGET_TTL, encoding="utf-8")
    graph = directory / "widget.jsonld"
    graph.write_text(json.dumps(WIDGET_GRAPH), encoding="utf-8")
    return graph, ontology


@pytest.fixture()
def no_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(workspace_policy.READ_ROOTS_ENV, raising=False)
    monkeypatch.delenv(workspace_policy.WRITE_ROOTS_ENV, raising=False)


@needs_validator
def test_tool_agrees_with_sdk_when_given_the_local_ontology(tmp_path: Path, no_policy: None) -> None:
    graph, ontology = _write_fixtures(tmp_path)

    without = server.validate_graph(graph_path=str(graph))
    assert without["ok"] is True
    assert without["conforms"] is False
    assert without["undeclared_concepts"] == [WIDGET]
    assert "extra_ontology_graphs" not in without
    assert "force_rdfs_inference" not in without

    sdk = validate_graph_file(graph, extra_ontology_graphs=[ontology], strict_concepts=True)
    tool = server.validate_graph(graph_path=str(graph), extra_ontology_graphs=[str(ontology)])
    assert tool["ok"] is True
    assert tool["conforms"] is sdk.conforms is True
    assert not tool.get("undeclared_concepts")
    assert tool["extra_ontology_graphs"] == [str(ontology)]


def test_tool_forwards_both_parameters(
    tmp_path: Path, no_policy: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    graph, ontology = _write_fixtures(tmp_path)
    seen: dict[str, object] = {}

    def fake_validate(graph_path: str, **kwargs: object) -> object:
        seen.update(kwargs)
        raise ValueError("validator_unavailable")

    monkeypatch.setattr(server, "_validate_graph_file", fake_validate)
    result = server.validate_graph(
        graph_path=str(graph),
        extra_ontology_graphs=[str(ontology)],
        force_rdfs_inference=True,
    )
    assert result == {
        "ok": False,
        "error": "validator_unavailable",
        "validator_name": server.GRAPH_VALIDATOR_NAME,
    }
    assert seen["extra_ontology_graphs"] == [str(ontology.resolve())]
    assert seen["force_rdfs_inference"] is True

    seen.clear()
    server.validate_graph(graph_path=str(graph))
    assert seen["extra_ontology_graphs"] is None
    assert seen["force_rdfs_inference"] is False


@needs_validator
def test_force_rdfs_inference_is_echoed_in_the_result(tmp_path: Path, no_policy: None) -> None:
    graph, ontology = _write_fixtures(tmp_path)
    result = server.validate_graph(
        graph_path=str(graph),
        extra_ontology_graphs=[str(ontology)],
        force_rdfs_inference=True,
    )
    assert result["ok"] is True
    assert result["conforms"] is True
    assert result["force_rdfs_inference"] is True


def test_extra_ontology_outside_the_roots_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = tmp_path / "evidence"
    case_work = tmp_path / "case-work"
    case_work.mkdir()
    graph, _ = _write_fixtures(evidence)
    _, outside_ontology = _write_fixtures(tmp_path / "outside")
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    monkeypatch.setenv(workspace_policy.WRITE_ROOTS_ENV, str(case_work))

    def must_not_run(*args: object, **kwargs: object) -> object:
        raise AssertionError("validation ran with an ontology outside the roots")

    monkeypatch.setattr(server, "_validate_graph_file", must_not_run)
    result = server.validate_graph(
        graph_path=str(graph), extra_ontology_graphs=[str(outside_ontology)]
    )
    assert result["ok"] is False
    assert result["error"] == "extra_ontology_graph_outside_read_roots"
    assert str(tmp_path) not in json.dumps(result)


@needs_validator
def test_extra_ontology_in_a_write_root_is_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = tmp_path / "evidence"
    case_work = tmp_path / "case-work"
    graph, _ = _write_fixtures(evidence)
    _, ontology = _write_fixtures(case_work)
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    monkeypatch.setenv(workspace_policy.WRITE_ROOTS_ENV, str(case_work))

    result = server.validate_graph(graph_path=str(graph), extra_ontology_graphs=[str(ontology)])
    assert result["ok"] is True
    assert result["conforms"] is True


def test_missing_extra_ontology_is_a_typed_error(tmp_path: Path, no_policy: None) -> None:
    graph, _ = _write_fixtures(tmp_path)
    result = server.validate_graph(
        graph_path=str(graph), extra_ontology_graphs=[str(tmp_path / "absent.ttl")]
    )
    assert result["ok"] is False
    assert result["error"] == "extra_ontology_graph_missing"
    assert str(tmp_path) not in json.dumps(result)


def test_extra_ontology_reached_through_a_symlink_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = tmp_path / "evidence"
    graph, _ = _write_fixtures(evidence)
    _, outside_ontology = _write_fixtures(tmp_path / "outside")
    link = evidence / "linked.ttl"
    try:
        link.symlink_to(outside_ontology)
    except OSError:
        pytest.skip("symlinks not available")
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    monkeypatch.delenv(workspace_policy.WRITE_ROOTS_ENV, raising=False)

    result = server.validate_graph(graph_path=str(graph), extra_ontology_graphs=[str(link)])
    assert result["ok"] is False
    assert result["error"] == "extra_ontology_graph_outside_read_roots"


def test_extra_ontology_must_be_an_rdf_file_within_the_size_limit(
    tmp_path: Path, no_policy: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    graph, ontology = _write_fixtures(tmp_path)
    not_rdf = tmp_path / "notes.txt"
    not_rdf.write_text("private notes, not an ontology\n", encoding="utf-8")

    def must_not_run(*args: object, **kwargs: object) -> object:
        raise AssertionError("validation ran with a refused ontology file")

    monkeypatch.setattr(server, "_validate_graph_file", must_not_run)
    result = server.validate_graph(graph_path=str(graph), extra_ontology_graphs=[str(not_rdf)])
    assert result["ok"] is False
    assert result["error"] == "extra_ontology_graph_unsupported_extension"
    assert "private notes" not in json.dumps(result)
    assert str(tmp_path) not in json.dumps(result)

    monkeypatch.setattr(server, "_MAX_GRAPH_BYTES", 8)
    result = server.validate_graph(graph_path=str(graph), extra_ontology_graphs=[str(ontology)])
    assert result["ok"] is False
    assert result["error"] == "extra_ontology_graph_oversized"
