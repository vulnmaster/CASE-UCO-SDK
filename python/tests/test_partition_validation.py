"""Partition-set validation scope and bundle propagation (#79)."""

from __future__ import annotations

from case_uco import CASEGraph
from case_uco.validation import GraphValidationReport, validate_partition_set


def _report() -> GraphValidationReport:
    return GraphValidationReport(
        conforms=True,
        warning_count=0,
        violation_count=0,
        exit_code=0,
        validator_name="test-validator",
        safe_summary="conforms",
    )


def _partitioned_graph(shared_policy: str):
    graph = CASEGraph()
    for root in ("kb:a", "kb:b"):
        graph.upsert_node(
            root,
            types="uco-core:UcoObject",
            properties={"uco-core:object": {"@id": "kb:shared"}},
        )
    graph.upsert_node("kb:shared", types="uco-core:UcoObject")
    parts, manifest = graph.partition_by_roots(
        ["kb:a", "kb:b"],
        include_incoming=False,
        shared_node_policy=shared_policy,
        return_manifest=True,
        validation_bundle={"extensions": ["example:full"], "profiles": ["p1"]},
    )
    return graph, parts, manifest


def test_self_contained_partitions_are_validated_individually(monkeypatch):
    graph, parts, manifest = _partitioned_graph("replicate-identical")
    calls = []

    def fake_validate(path, **kwargs):
        calls.append((path, kwargs))
        return _report()

    monkeypatch.setattr(
        "case_uco.validation.partition.validate_graph_file", fake_validate
    )
    result = validate_partition_set(parts, manifest, source_graph=graph)

    assert result.conforms is True
    assert result.union_equivalent is True
    assert result.set_report is None
    assert set(result.partition_reports) == {"kb:a", "kb:b"}
    assert len(calls) == 2
    assert calls[0][1]["extensions"] == ["example:full"]
    assert calls[0][1]["profiles"] == ["p1"]


def test_referenced_partitions_are_validated_as_one_set(monkeypatch):
    graph, parts, manifest = _partitioned_graph("support-graph")
    calls = []

    def fake_validate(path, **kwargs):
        calls.append((path, kwargs))
        return _report()

    monkeypatch.setattr(
        "case_uco.validation.partition.validate_graph_file", fake_validate
    )
    result = validate_partition_set(parts, manifest, source_graph=graph)

    assert result.conforms is True
    assert result.union_equivalent is True
    assert result.partition_reports == {}
    assert result.set_report is not None
    assert len(calls) == 1


def test_partition_set_must_match_manifest():
    _, parts, manifest = _partitioned_graph("support-graph")
    parts.pop("_support")

    try:
        validate_partition_set(parts, manifest)
    except ValueError as exc:
        assert "does not match manifest" in str(exc)
    else:
        raise AssertionError("missing partition was accepted")
