"""Compact executable exemplars for operational recipes that lack a dedicated graph (#124)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

LEGALPROC_CONTEXT = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
}


def _core_graph(title: str) -> CASEGraph:
    graph = CASEGraph()
    tz = timezone.utc
    tool = graph.create(Tool, name="CASE-UCO-SDK", version="1.28.0")
    evidence = graph.create(
        ObservableObject,
        name=f"{title} evidence",
        has_facet=[
            FileFacet(file_name="evidence.bin", size_in_bytes=1024),
            ContentDataFacet(
                hash=[Hash(hash_method="SHA256", hash_value="00" * 32)],
                size_in_bytes=1024,
            ),
        ],
    )
    action = graph.create(
        InvestigativeAction,
        name=f"Build {title} exemplar",
        start_time=datetime(2026, 8, 1, 12, 0, tzinfo=tz),
        end_time=datetime(2026, 8, 1, 12, 5, tzinfo=tz),
        instrument=[tool],
        object=[evidence],
        result=[evidence],
    )
    graph.create(
        Investigation,
        name=title,
        description="Partial executable fragment for operational recipe coverage (#124).",
        object=[evidence, action],
    )
    return graph


def _legal_graph(title: str) -> CASEGraph:
    graph = CASEGraph(extra_context=LEGALPROC_CONTEXT)
    graph.create(Investigation, id="kb:investigation", name=title)
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "PR-CATALOG-001")
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", "omitted")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "Complaint",
            "legalproc:instrumentType": "complaint",
        },
    )
    graph.upsert_node(
        "kb:charge-1",
        types="legalproc:FederalCharge",
        properties={
            "uco-core:name": "Count 1",
            "legalproc:statuteCitation": "18 U.S.C. § 371",
            "legalproc:chargeDisposition": "pending",
            "legalproc:jurisdictionKind": "federal",
            "legalproc:outcomeScope": "current-case",
            "legalproc:assertedIn": {"@id": "kb:instrument"},
        },
    )
    return graph


_LEGAL_SLUGS = frozenset(
    {
        "legal-process-modeling",
        "cac-legal-sentencing-outcomes",
        "cac-federal-prosecution-relationships",
        "cac-federal-trial-proceedings",
        "cac-pacer-document-ingestion",
        "fraud-crypto-laundering",
        "elder-fraud-impersonation",
        "espionage-classified-disclosure",
        "export-control-sanctions",
        "insider-threat-trade-secrets",
        "racketeering-enterprise",
    }
)


def build(slug: str) -> CASEGraph:
    title = slug.replace("-", " ")
    if slug in _LEGAL_SLUGS:
        return _legal_graph(title)
    return _core_graph(title)


def build_and_write(slug: str, output: Path) -> Path:
    graph = build(slug)
    graph.write(str(output))
    return output
