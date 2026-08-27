"""Tests for the technique → evidence → outcome factory (#126)."""

from __future__ import annotations

from tools.technique_evidence_outcome import suggest_techniques_for_product


def test_le_tool_profiles_are_suggestions_only():
    assert suggest_techniques_for_product("Cellebrite UFED") == [
        "DFT-1020",
        "DFT-1019",
        "DFT-1044",
    ]
    assert suggest_techniques_for_product("Unknown Product") == []
