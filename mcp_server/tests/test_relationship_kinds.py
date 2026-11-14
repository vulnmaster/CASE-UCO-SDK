"""Tests for relationship-kind registry lint (CQ-40)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from relationship_kinds import (  # noqa: E402
    lint_relationship_kinds,
    known_relationship_kinds,
    vocabulary_names,
)

CONTEXT = {
    "kb": "http://example.org/kb/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
}


def _relationship_graph(kind: str, endpoint_type: str = "uco-observable:ObservableObject") -> dict:
    return {
        "@context": CONTEXT,
        "@graph": [
            {"@id": "kb:a", "@type": endpoint_type},
            {"@id": "kb:b", "@type": endpoint_type},
            {
                "@id": "kb:rel-1",
                "@type": "uco-core:Relationship",
                "uco-core:kindOfRelationship": kind,
                "uco-core:source": {"@id": "kb:a"},
                "uco-core:target": [{"@id": "kb:b"}],
            },
        ],
    }


def test_known_kind_ok_no_findings():
    known = next(iter(known_relationship_kinds()))
    report = lint_relationship_kinds(_relationship_graph(known))
    assert report["ok"] is True
    assert report["findings"] == []
    assert report["checked"] == 1


def test_unknown_kind_open_vocabulary_warning():
    report = lint_relationship_kinds(
        _relationship_graph("not-in-vocab-kind"),
        allow_open_vocabulary=True,
    )
    assert report["ok"] is True
    assert len(report["findings"]) == 1
    finding = report["findings"][0]
    assert finding["severity"] == "warning"
    assert finding["kind"] == "not-in-vocab-kind"
    assert finding["node_id"] == "kb:rel-1"


def test_unknown_kind_strict_mode_error():
    report = lint_relationship_kinds(
        _relationship_graph("not-in-vocab-kind"),
        allow_open_vocabulary=False,
    )
    assert report["ok"] is False
    assert len(report["findings"]) == 1
    assert report["findings"][0]["severity"] == "error"


def test_unknown_kind_message_names_only_loaded_vocabularies():
    report = lint_relationship_kinds(_relationship_graph("not-in-vocab-kind"))
    message = report["findings"][0]["message"]
    assert message.endswith(" / ".join(vocabulary_names()))
    assert "ActionRelationshipVocab" not in message or "ActionRelationshipVocab" in vocabulary_names()


def test_open_kinds_between_non_observables_are_not_checked():
    """#94: identity and legal-process relationships use open kinds by design."""
    report = lint_relationship_kinds(
        _relationship_graph("Charged_With", endpoint_type="uco-identity:Person"),
        allow_open_vocabulary=False,
    )
    assert report["ok"] is True
    assert report["checked"] == 0
    assert report["findings"] == []


def test_observable_relationship_type_is_checked_without_endpoints():
    doc = {
        "@context": CONTEXT,
        "@graph": [{
            "@id": "kb:rel-1",
            "@type": "uco-observable:ObservableRelationship",
            "uco-core:kindOfRelationship": "not-in-vocab-kind",
        }],
    }
    assert len(lint_relationship_kinds(doc)["findings"]) == 1


@pytest.mark.parametrize("path", [
    "examples/pacer/ddc_2024_cr_00417/lam-ddc-2024-racketeering.jsonld",
    "examples/pacer/ndca_2024_cr_00141/ding-ndca-2024-insider-threat.jsonld",
    "examples/scenarios/operation-phantom-gate.jsonld",
])
def test_issue_94_graphs_raise_no_findings_for_open_kinds(path):
    from critic.canonical import lint_kind_of_relationship, load_canonical_graph

    open_kinds = {"Charged_With", "Member_Of", "Victim_Of", "Has_Account", "Authorized_By"}
    report = lint_relationship_kinds(json.loads((ROOT / path).read_text(encoding="utf-8")))
    canonical = lint_kind_of_relationship(load_canonical_graph(ROOT / path))
    for result in (report, canonical):
        assert not open_kinds & {f["kind"] for f in result["findings"]}
    assert report["checked"] == canonical["checked"]


def test_layered_exemplar_coupling_kinds_are_not_checked():
    from critic.canonical import lint_kind_of_relationship, load_canonical_graph

    report = lint_kind_of_relationship(
        load_canonical_graph(ROOT / "extensions/layered/layered-exemplar.ttl")
    )
    assert report["findings"] == []
