"""Opt-in CaseLinker current-state vs v1.27.0 target-shape probes.

Normal test runs remain offline. Run explicitly with:

    CASE_UCO_SPARQL_LIVE=1 python -m pytest \
        mcp_server/tests/test_caselinker_current_state_live.py -q

Target-shape ASKs are executed but not asserted false so a later remodel
does not break the suite. Current-shape ASKs assert that today's detective
and prosecutor joins remain answerable. Snapshot counts live in
``examples/caselinker-icac-remodel/CURRENT_STATE_PROBE.md``.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

import sparql_client


pytestmark = pytest.mark.skipif(
    os.environ.get("CASE_UCO_SPARQL_LIVE") != "1",
    reason="set CASE_UCO_SPARQL_LIVE=1 to query CaseLinker",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUERY_ROOT = PROJECT_ROOT / "examples" / "caselinker-icac-remodel" / "queries"
CURRENT_STATE = QUERY_ROOT / "current-state"

TARGET_ASKS = {
    "cybertip_trigger": """
        ASK {
          ?trigger a <https://cacontology.projectvic.org/us/ncmec#InvestigationTrigger> ;
                   <https://cacontology.projectvic.org/us/ncmec#triggeredBy> ?tip ;
                   <https://cacontology.projectvic.org/us/ncmec#resultedInInvestigation> ?investigation .
        }
        """,
    "hashed_series_file": """
        ASK {
          ?file <https://ontology.unifiedcyberontology.org/uco/core/hasFacet> ?facet .
          ?facet a <https://ontology.unifiedcyberontology.org/uco/observable/ContentDataFacet> ;
                 <https://ontology.unifiedcyberontology.org/uco/observable/hash> ?hash .
          ?file <https://ontology.unifiedcyberontology.org/uco/core/tag>
                "photodna-match-reported-value-withheld" .
        }
        """,
    "federal_charge_sentence": """
        ASK {
          ?charge a <https://ontology.caseontology.org/case/criminal/FederalCharge> ;
                  <https://ontology.caseontology.org/case/criminal/jurisdictionKind> "federal" .
          ?person <https://ontology.caseontology.org/case/criminal/chargedWith> ?charge .
          ?sentence a <https://ontology.caseontology.org/case/criminal/Sentence> ;
                    <https://ontology.caseontology.org/case/criminal/sentenceStatus> "imposed" ;
                    <https://ontology.caseontology.org/case/criminal/appliesTo> ?charge .
        }
        """,
    "phase_clock": """
        ASK {
          ?inv a <https://cacontology.projectvic.org#CACInvestigation> ;
               <https://cacontology.projectvic.org#hasPhase> ?phase .
          ?phase <https://cacontology.projectvic.org#hasPhaseBeginPoint> ?begin ;
                 <https://cacontology.projectvic.org#hasPhaseEndPoint> ?end .
        }
        """,
    "disclosure_jencks": """
        ASK {
          ?obligation a <https://ontology.caseontology.org/case/criminal/DisclosureObligation> ;
                      <https://ontology.caseontology.org/case/criminal/disclosureKind> "jencks" ;
                      <https://ontology.caseontology.org/case/criminal/disclosureSourceCitation> ?cite ;
                      <https://ontology.caseontology.org/case/criminal/concernsEvidence> ?evidence .
        }
        """,
}

CURRENT_ASKS = {
    "tip_as_hasStep": """
        ASK {
          ?inv a <https://cacontology.projectvic.org#CACInvestigation> ;
               <https://cacontology.projectvic.org#hasStep> ?tip .
          ?tip a <https://cacontology.projectvic.org/us/ncmec#NCMECCybertipReport> .
        }
        """,
    "proceeding_charge_sentence": """
        ASK {
          ?lp a <https://cacontology.projectvic.org/legal-outcomes#LegalProceeding> ;
              <https://cacontology.projectvic.org/legal-outcomes#hasCharge> ?ch ;
              <https://cacontology.projectvic.org/legal-outcomes#resultsSentence> ?sent .
          ?ch a <https://cacontology.projectvic.org/legal-outcomes#CriminalCharge> .
          ?sent a <https://cacontology.projectvic.org/legal-outcomes#CriminalSentence> .
        }
        """,
    "phase_begin": """
        ASK {
          ?inv a <https://cacontology.projectvic.org#CACInvestigation> ;
               <https://cacontology.projectvic.org#hasPhase> ?phase .
          ?phase <https://cacontology.projectvic.org#hasPhaseBeginPoint> ?begin .
        }
        """,
}


def _execute(query: str) -> dict:
    result = sparql_client.execute_query(query)
    assert result["ok"] is True
    assert result["endpoint"] == sparql_client.DEFAULT_ENDPOINT
    return result


@pytest.mark.parametrize("name,query", TARGET_ASKS.items())
def test_target_shape_asks_execute(name: str, query: str) -> None:
    result = _execute(query)
    assert result["result_kind"] == "boolean"
    assert "boolean" in result


@pytest.mark.parametrize("name,query", CURRENT_ASKS.items())
def test_current_shape_asks_are_answerable(name: str, query: str) -> None:
    result = _execute(query)
    assert result["result_kind"] == "boolean"
    assert result["boolean"] is True


def test_current_state_selects_execute() -> None:
    files = sorted(CURRENT_STATE.glob("*.sparql"))
    assert files, f"missing current-state queries under {CURRENT_STATE}"
    for path in files:
        result = _execute(path.read_text(encoding="utf-8"))
        assert result["result_kind"] == "bindings"
        assert result["row_count"] >= 1


def test_target_selects_execute() -> None:
    for name in TARGET_ASKS:
        path = QUERY_ROOT / f"{name}.sparql"
        result = _execute(path.read_text(encoding="utf-8"))
        assert result["result_kind"] == "bindings"
