"""Tests for the bundled trajectories extension.

Covers SHACL conformance of the two valid exemplars and six expected-invalid
fixtures (pyshacl, RDFS inference), plus the manifest-declared competency
SPARQL queries run as raw A-Box (no inference).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXT_DIR = PROJECT_ROOT / "extensions" / "trajectories"
MANIFEST = json.loads((EXT_DIR / "manifest.json").read_text(encoding="utf-8"))

pyshacl = pytest.importorskip("pyshacl")


def _pyshacl_conforms(data_path: Path) -> bool:
    """Validate ``data_path`` against traj OWL + SHACL with RDFS inference."""
    from rdflib import Graph

    data = Graph()
    data.parse(data_path)
    ont = Graph()
    ont.parse(EXT_DIR / "trajectories.ttl")
    shapes = Graph()
    shapes.parse(EXT_DIR / "trajectories-shapes.ttl")
    conforms, _report_graph, _report_text = pyshacl.validate(
        data_graph=data,
        shacl_graph=shapes,
        ont_graph=ont,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )
    return bool(conforms)


def _select_row_count(query_text: str, graph_path: Path) -> int:
    """Row count for a SELECT (or ASK-as-0/1). Does not use list(ASK)."""
    from rdflib import Graph

    graph = Graph()
    graph.parse(graph_path)
    result = graph.query(query_text)
    if result.type == "ASK":
        return 1 if result.askAnswer else 0
    return len(list(result))


# ---------------------------------------------------------------------------
# Exemplar conformance (pyshacl + RDFS)
# ---------------------------------------------------------------------------
class TestExemplarConformance:
    @pytest.mark.parametrize(
        "rel",
        MANIFEST["exemplar_files"],
        ids=lambda rel: Path(rel).name,
    )
    def test_exemplar_conforms(self, rel: str):
        path = EXT_DIR / rel
        assert path.is_file(), path
        assert _pyshacl_conforms(path) is True, rel

    @pytest.mark.parametrize(
        "rel",
        MANIFEST["invalid_exemplar_files"],
        ids=lambda rel: Path(rel).name,
    )
    def test_invalid_fixture_fails(self, rel: str):
        path = EXT_DIR / rel
        assert path.is_file(), path
        assert _pyshacl_conforms(path) is False, (
            f"{rel} unexpectedly conforms — shapes no longer catch this fixture"
        )


# ---------------------------------------------------------------------------
# Competency queries (raw A-Box; SELECT row counts, not list(ASK))
# ---------------------------------------------------------------------------
class TestCompetencyQueries:
    @pytest.mark.parametrize(
        "entry",
        MANIFEST["competency_queries"],
        ids=lambda e: f"{Path(e['file']).name}::{e['against']}",
    )
    def test_competency_query_matches_manifest_expect(self, entry: dict):
        query_path = EXT_DIR / entry["file"]
        against_path = EXT_DIR / entry["against"]
        expect = entry.get("expect", "nonempty")
        assert query_path.is_file(), query_path
        assert against_path.is_file(), against_path
        nrows = _select_row_count(
            query_path.read_text(encoding="utf-8"), against_path
        )
        if expect == "empty":
            assert nrows == 0, (
                f"{query_path.name} against {against_path.name}: "
                f"expected 0 rows, got {nrows}"
            )
        else:
            assert nrows > 0, (
                f"{query_path.name} against {against_path.name}: "
                f"expected nonempty, got {nrows} row(s)"
            )
