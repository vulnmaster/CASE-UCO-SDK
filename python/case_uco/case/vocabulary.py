"""Auto-generated CASE vocabularies for the CASE/UCO ontology.

Every CASE vocabulary (owl:oneOf datatype) in one namespace. Members are plain
strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string
literals checked against the vocabulary with sh:in, so pass the constants
directly rather than typing them with the vocabulary IRI.
"""

from __future__ import annotations

__all__ = [
    "InvestigationFormVocab",
    "VOCABULARIES",
]


class InvestigationFormVocab:
    """Vocabulary: InvestigationFormVocab"""
    IRI = "https://ontology.caseontology.org/case/vocabulary/InvestigationFormVocab"
    MEMBERS: frozenset[str] = frozenset({"case", "incident", "suspicious-activity"})

    CASE = "case"
    INCIDENT = "incident"
    SUSPICIOUS_ACTIVITY = "suspicious-activity"


VOCABULARIES: dict[str, type] = {
    "InvestigationFormVocab": InvestigationFormVocab,
}
