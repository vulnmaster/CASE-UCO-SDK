"""The cross-report file identity exemplar converges, and the recipe's queries answer as stated."""

from __future__ import annotations

import re
import runpy
from pathlib import Path

import pytest
import rdflib
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[2]
RECIPE = ROOT / "docs/recipes/cross-report-file-identity.md"
BUILDER = ROOT / "examples/recipes/build_cross_report_file_identity.py"


@pytest.fixture(scope="module")
def builder():
    return runpy.run_path(str(BUILDER))


@pytest.fixture(scope="module")
def merged(builder):
    graph = rdflib.Graph()
    graph.parse(data=builder["build"]().serialize(), format="json-ld")
    return graph


def _recipe_queries() -> list[str]:
    return re.findall(r"```sparql\n(.*?)```", RECIPE.read_text(encoding="utf-8"), re.S)


def test_recipe_queries_return_the_rows_the_recipe_states(merged):
    queries = _recipe_queries()
    assert len(queries) == 4
    by_tool, coverage, disagreements, orphans = (list(merged.query(q)) for q in queries)

    assert [str(row.toolName) for row in by_tool] == ["Report tool A", "Report tool B"]
    assert {str(row.modified) for row in by_tool} == {
        "2023-01-02T10:15:12+00:00",
        "2023-01-02T10:15:13+00:00",
    }

    assert {
        str(row.path): (sorted(str(row.methods).split(",")), int(row.entries)) for row in coverage
    } == {
        "/storage/1A2B-3C4D/DCIM/Camera/IMG_0001.jpg": (["MD5", "SHA1", "SHA256"], 2),
        "/storage/1A2B-3C4D/Documents/notes.txt": (["MD5", "SHA256"], 1),
    }

    assert len(disagreements) == 1
    assert int(disagreements[0].values) == 2

    assert orphans == []


def test_reports_built_in_either_order_merge_to_the_same_graph(builder):
    from case_uco import CASEGraph

    def merge(order):
        graph = CASEGraph()
        for report in order:
            graph.load(builder["build_report"](report).serialize(), on_duplicate="merge_compatible")
        out = rdflib.Graph()
        out.parse(data=graph.serialize(), format="json-ld")
        return out

    forward = merge([builder["REPORT_A"], builder["REPORT_B"]])
    backward = merge([builder["REPORT_B"], builder["REPORT_A"]])
    assert isomorphic(forward, backward)


CORE = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/core/")


def _drop_relationships(rdf, *, source=None, target=None, kind):
    for rel in list(rdf.subjects(CORE.kindOfRelationship, rdflib.Literal(kind))):
        if (source is None or (rel, CORE.source, source) in rdf) and (
            target is None or (rel, CORE.target, target) in rdf
        ):
            rdf.remove((rel, None, None))


def test_retracting_a_report_orphans_only_its_unique_content(merged):
    rdf = rdflib.Graph()
    for triple in merged:
        rdf.add(triple)
    report_a_entries = [
        s for s, o in rdf.subject_objects(CORE.name) if str(o).startswith("REPORT-A row")
    ]
    for entry in report_a_entries:
        _drop_relationships(rdf, source=entry, kind="Characterizes")
    for exhibit_file in set(rdf.objects(None, CORE.target)):
        still_reported = any(
            (rel, CORE.kindOfRelationship, rdflib.Literal("Characterizes")) in rdf
            for rel in rdf.subjects(CORE.target, exhibit_file)
        )
        if not still_reported:
            _drop_relationships(rdf, target=exhibit_file, kind="Contained_Within")

    orphans = list(rdf.query(_recipe_queries()[3]))
    # The notes file was only in report A (MD5 and SHA-256 cores). The photo's
    # SHA-256 core stays: report B still places that content on the exhibit.
    assert len(orphans) == 2


@pytest.mark.parametrize(
    ("query", "source"),
    [
        ("Cellebrite .ufd extraction summary and EvidenceCollection.ufdx", "Cellebrite UFED extraction summary (.ufd / .ufdx)"),
        ("Cellebrite UFED report.xml decodedData modelType", "Cellebrite UFED XML report"),
        ("Magnet ACQUIRE image_info.txt with activity_log", "Magnet ACQUIRE imaging summary (image_info.txt)"),
        ("Magnet AXIOM Examine XML export artifact fragment", "Magnet AXIOM XML export"),
    ],
)
def test_guide_mapping_separates_summaries_from_reports(query, source):
    from server import guide_mapping

    assert guide_mapping(query)["source_type"] == source


def test_recipe_routes_from_examiner_vocabulary():
    from server import get_recipes

    result = get_recipes("deterministic ids for the same file across multiple UFED and XRY reports")
    files = [r.get("file") for r in result.get("recipes", result.get("results", []))]
    assert "docs/recipes/cross-report-file-identity.md" in files
