"""Tier T0 tests for deterministic document semantic mapping."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_semantic_mapping import extract_semantic_entities

SYNTHETIC_ARTICLE = """
11/06/2026, 20:06
38-Year-Old Riverton Man Charged With Online Solicitation

RIVERton — The Maryland State Police Internet Crimes Against Children Task Force
announced that a 38-year-old Riverton man was charged with sexual solicitation
after an investigation into online activity. Officers executed a search warrant
at a residence in Riverton on DECEMBER 12, 2025.

Contact the task force at tips@example-agency.test or call (555) 010-2000.
More information: https://example-agency.test/icac/release-001
"""


def test_semantic_mapping_extracts_typed_entities_with_anchors() -> None:
    entities = extract_semantic_entities(SYNTHETIC_ARTICLE, run_seed="t0-article")
    classes = {entity.ontology_class for entity in entities}
    assert "uco-identity:Person" in classes
    assert "uco-location:Location" in classes
    assert "uco-identity:Organization" in classes
    assert "uco-core:Event" in classes
    assert "uco-observable:EmailAddress" in classes
    assert "uco-observable:PhoneAccount" in classes
    assert "uco-observable:URL" in classes

    for entity in entities:
        assert 0 <= entity.start < entity.end <= len(SYNTHETIC_ARTICLE)
        assert SYNTHETIC_ARTICLE[entity.start : entity.end] == entity.matched_text


def test_semantic_mapping_is_bounded_and_deterministic() -> None:
    first = extract_semantic_entities(SYNTHETIC_ARTICLE, run_seed="t0-article")
    second = extract_semantic_entities(SYNTHETIC_ARTICLE, run_seed="t0-article")
    assert first == second
    assert len(first) <= 48


FRAUD_CRYPTO_WARRANT_SNIPPET = """
| Groomer | Marcus Hale, aka "Coach Mike" | Telegram @northstar_mike_synth |
Apartment 4B, **1555 Oak Street, San Jose, California 95110**, including any computers
within the control of **Dylan Reyes** (DOB 1991-07-02, synthetic).
| Applying Agent | Special Agent Jordan Ellis, FBI |
"""


def test_semantic_mapping_extracts_warrant_markdown_anchors() -> None:
    entities = extract_semantic_entities(
        FRAUD_CRYPTO_WARRANT_SNIPPET,
        run_seed="fraud-crypto-warrant-t0",
    )
    classes = {entity.ontology_class for entity in entities}
    labels = {entity.label for entity in entities}
    assert "uco-identity:Person" in classes
    assert "uco-location:Location" in classes
    assert "uco-observable:InstantMessagingAddress" in classes
    assert any("Dylan Reyes" in label for label in labels)
    assert any("1555 Oak Street" in label for label in labels)
    assert any("Telegram @northstar_mike_synth" in label for label in labels)
    assert not any(label.startswith("Location THE UNITED") for label in labels)
    assert not any(label.startswith("Location the Matter") for label in labels)
