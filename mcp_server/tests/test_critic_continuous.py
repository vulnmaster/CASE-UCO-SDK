"""Focused checks for the critic-side continuous-critique entry."""

from __future__ import annotations

from pathlib import Path

import pytest

from critic import continuous
from critic.continuous import ContinuousCritiqueError, critique_jsonld

REPO_ROOT = Path(__file__).resolve().parents[2]
CRITIC_PATH = REPO_ROOT / "mcp_server" / "critic" / "continuous.py"
DOC_PATH = REPO_ROOT / "docs" / "CONTINUOUS_CRITIQUE.md"

FORBIDDEN_SUBSTRINGS = (
    "photodna",
    "photo-dna",
    "vics",
    "court-defensible",
    "court defensible",
    "2.0.0",
    "2.0.1",
    "investigationworkflow",
    "model_csam",
    "precise shortlist",
)

INV_NO_OBJECT = {
    "@context": {
        "case-investigation": "https://ontology.caseontology.org/case/investigation/",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    },
    "@graph": [
        {
            "@id": "urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "@type": "case-investigation:Investigation",
            "uco-core:name": "Empty investigation",
        }
    ],
}

INV_WITH_OBJECT = {
    "@context": {
        "case-investigation": "https://ontology.caseontology.org/case/investigation/",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    },
    "@graph": [
        {
            "@id": "urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "@type": "case-investigation:Investigation",
            "uco-core:name": "Empty investigation",
            "uco-core:object": [
                {"@id": "urn:uuid:bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"}
            ],
        },
        {
            "@id": "urn:uuid:bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "@type": "uco-core:UcoObject",
            "uco-core:name": "Exhibit A",
        },
    ],
}


def test_public_surface_is_the_jsonld_entry() -> None:
    assert continuous.PUBLIC_SURFACE == ("critique_jsonld",)
    assert not hasattr(continuous, "ProfileCritic")
    assert not hasattr(continuous, "evaluate_heuristics")
    assert not hasattr(continuous, "critique_graph")
    assert not (REPO_ROOT / "python" / "case_uco" / "continuous_critique.py").exists()
    assert not (REPO_ROOT / "python" / "case_uco" / "critique").exists()


def test_missing_investigation_object_is_stable_and_actionable() -> None:
    first = critique_jsonld(INV_NO_OBJECT)
    second = critique_jsonld(INV_NO_OBJECT)
    inv = [item for item in first if item["rule_id"] == "CRIT-H-INV-NO-OBJECT"]
    assert inv
    assert inv[0]["finding_id"].startswith("CRIT-")
    assert inv[0]["repair_hint"]
    assert inv[0]["node_id"]
    assert first == second


def test_adding_object_clears_the_investigation_finding() -> None:
    remaining = [
        item
        for item in critique_jsonld(INV_WITH_OBJECT)
        if item["rule_id"] == "CRIT-H-INV-NO-OBJECT"
    ]
    assert remaining == []


def test_oversize_payload_fails_closed() -> None:
    with pytest.raises(ContinuousCritiqueError, match="exceeds"):
        critique_jsonld(INV_NO_OBJECT, max_bytes=32)


def test_empty_payload_fails_closed() -> None:
    with pytest.raises(ContinuousCritiqueError, match="empty"):
        critique_jsonld("")


def test_docs_and_entry_are_public_safe() -> None:
    blob = CRITIC_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + DOC_PATH.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"critique files contain forbidden substring {needle!r}"
    doc = DOC_PATH.read_text(encoding="utf-8").lower()
    assert "does not classify" in doc
    assert "does not add a second rule engine" in doc
    assert "critique_jsonld" in doc
    assert "critique_graph" not in doc
    assert "continuous_critique" not in doc
