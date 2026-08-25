"""Opt-in smoke test for the CaseLinker reference SPARQL endpoint.

Normal test runs remain offline. Run explicitly with:

    CASE_UCO_SPARQL_LIVE=1 python -m pytest \
        mcp_server/tests/test_sparql_client_live.py -q
"""

from __future__ import annotations

import os

import pytest

import sparql_client


pytestmark = pytest.mark.skipif(
    os.environ.get("CASE_UCO_SPARQL_LIVE") != "1",
    reason="set CASE_UCO_SPARQL_LIVE=1 to query CaseLinker",
)


def test_caselinker_reports_cac_investigations() -> None:
    result = sparql_client.execute_query(
        """
        SELECT (COUNT(DISTINCT ?case) AS ?cases)
        WHERE {
          ?case a <https://cacontology.projectvic.org#CACInvestigation> .
        }
        """
    )
    assert result["ok"] is True
    assert result["endpoint"] == sparql_client.DEFAULT_ENDPOINT
    assert result["result_kind"] == "bindings"
    assert result["row_count"] == 1
    assert int(result["bindings"][0]["cases"]["value"]) > 0
