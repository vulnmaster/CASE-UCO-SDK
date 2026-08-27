"""Builders for the technique → evidence → outcome join (#126)."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, ProvenanceRecord
from case_uco.uco.identity import Person
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
PROFILES_PATH = (
    HERE.parent.parent / "examples" / "technique-evidence-outcome" / "le_tool_solveit_profiles.json"
)

DFT_1050 = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1050"
DFT_1020 = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1020"

CONTEXT = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
    "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
    "solveit-data": "https://ontology.solveit-df.org/solveit/data/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
}


def _lit(datatype: str, value: str) -> dict[str, str]:
    return {"@type": datatype, "@value": value}


def _new_graph() -> CASEGraph:
    return CASEGraph(kb_prefix="http://example.org/kb/", extra_context=CONTEXT)


def _relate(graph: CASEGraph, source: str, target: str, description: str, key: str) -> None:
    graph.create_relationship(
        source,
        target,
        "Related_To",
        description=description,
        assertion_id=f"kb:rel-{key}",
    )


def load_le_tool_profiles(path: Path | None = None) -> dict[str, Any]:
    profile_path = path or PROFILES_PATH
    return json.loads(profile_path.read_text(encoding="utf-8"))


def suggest_techniques_for_product(product_name: str) -> list[str]:
    """Return suggested DFT-* IDs. Never treat these as asserted executions."""
    data = load_le_tool_profiles()
    needle = product_name.casefold()
    for product in data.get("products") or []:
        if str(product.get("name") or "").casefold() == needle:
            return list(product.get("techniques") or [])
    return []


def import_hashmatch_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def import_ufed_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_lab_join(
    *,
    hashmatch_csv: Path | None = None,
    ufed_summary: Path | None = None,
) -> CASEGraph:
    examples = Path(__file__).resolve().parent.parent.parent / "examples" / "technique-evidence-outcome"
    rows = import_hashmatch_csv(hashmatch_csv or examples / "hashmatch.csv")
    ufed = import_ufed_summary(ufed_summary or examples / "ufed_summary.json")
    row = rows[0]

    graph = _new_graph()
    ingested = datetime(2026, 8, 27, 16, 0, tzinfo=timezone.utc)
    investigation = graph.create(
        Investigation,
        id="kb:investigation",
        name="Lab join of hash match, mobile extract, and sentence",
        object_created_time=ingested,
    )
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "2:26-cr-01001")
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", "omitted")
    defendant = graph.create(Person, id="kb:defendant", name="Defendant A")

    graph.upsert_node(
        "kb:charge-1",
        types="legalproc:FederalCharge",
        properties={
            "uco-core:name": "Possession of CSAM",
            "legalproc:statuteCitation": "18 U.S.C. § 2252A(a)(5)(B)",
            "legalproc:countNumber": _lit("xsd:nonNegativeInteger", "1"),
            "legalproc:countLabel": "Count 1",
            "legalproc:chargeDisposition": "convicted-by-plea",
            "legalproc:jurisdictionKind": "federal",
            "legalproc:outcomeScope": "current-case",
            "legalproc:offenseForm": "substantive",
        },
    )
    graph.upsert_node(
        "kb:sentence-1",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Imposed custodial sentence",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "60 months",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )

    hash_tool = graph.create(
        Tool,
        id="kb:tool-hashset",
        name=row["tool_name"],
        version=row["tool_version"],
        tool_type="Hash matching",
    )
    ufed_tool = graph.create(
        Tool,
        id="kb:tool-ufed",
        name=ufed["tool_name"],
        version=ufed["tool_version"],
        tool_type="Mobile Extraction",
    )

    evidence = graph.create(
        ObservableObject,
        id="kb:file-known-csam",
        name=row["file_name"],
        has_facet=[
            FileFacet(file_name=row["file_name"]),
            ContentDataFacet(
                hash=[Hash(hash_method=row["hash_method"], hash_value=row["hash_value"])],
            ),
        ],
    )
    extract = graph.create(
        ObservableObject,
        id="kb:file-extraction",
        name=ufed["output_file"],
        has_facet=[
            FileFacet(file_name=ufed["output_file"]),
            ContentDataFacet(
                hash=[Hash(hash_method="SHA256", hash_value=ufed["output_sha256"])],
            ),
        ],
    )

    graph.upsert_node(
        "kb:action-hashset",
        types="solveit-core:SolveitInvestigativeAction",
        properties={
            "uco-core:name": "Locate known CSAM with a hashset",
            "uco-core:description": (
                "Lab hash-match CSV: known-CSAM digest matched NCMEC set. "
                "Source: lab/hashmatch.csv."
            ),
            "solveit-core:usedTechnique": {"@id": DFT_1050},
            "uco-action:instrument": {"@id": graph.get_id(hash_tool)},
            "uco-action:object": {"@id": graph.get_id(evidence)},
            "uco-action:result": {"@id": graph.get_id(evidence)},
        },
    )
    graph.upsert_node(
        "kb:action-mobile",
        types="solveit-core:SolveitInvestigativeAction",
        properties={
            "uco-core:name": "Extract mobile file system",
            "uco-core:description": (
                f"UFED-style summary for {ufed['device_name']}. "
                "Source: lab/ufed_summary.json."
            ),
            "solveit-core:usedTechnique": {"@id": DFT_1020},
            "uco-action:instrument": {"@id": graph.get_id(ufed_tool)},
            "uco-action:result": {"@id": graph.get_id(extract)},
        },
    )
    graph.create(
        ProvenanceRecord,
        id="kb:exhibit-1",
        exhibit_number="EX-2026-001",
        object=[evidence, extract],
    )

    inv_id = graph.get_id(investigation)
    _relate(graph, inv_id, "kb:charge-1", "Investigation prosecutes this charge", "inv-charge")
    _relate(graph, graph.get_id(defendant), "kb:charge-1", "Defendant is charged in Count 1", "def-charge")
    _relate(graph, "kb:action-hashset", "kb:charge-1", "Hashset match supports Count 1", "hash-charge")
    _relate(graph, "kb:action-mobile", "kb:charge-1", "Mobile extraction supports Count 1", "mobile-charge")
    _relate(graph, "kb:sentence-1", "kb:charge-1", "Imposed sentence concerns Count 1", "sentence-charge")
    return graph


def build_pacer_method_claim() -> CASEGraph:
    graph = _new_graph()
    ingested = datetime(2026, 8, 27, 16, 5, tzinfo=timezone.utc)
    investigation = graph.create(
        Investigation,
        id="kb:investigation",
        name="PACER affidavit names a mobile extraction tool",
        object_created_time=ingested,
    )
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "2:26-cr-01001")
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", "omitted")
    graph.add_property("kb:investigation", "legalproc:sourceRetrievalTime", _lit("xsd:dateTime", "2026-08-26T18:00:00Z"))
    graph.create(Person, id="kb:defendant", name="Defendant A")
    graph.upsert_node(
        "kb:charge-1",
        types="legalproc:FederalCharge",
        properties={
            "uco-core:name": "Possession of CSAM",
            "legalproc:statuteCitation": "18 U.S.C. § 2252A(a)(5)(B)",
            "legalproc:countNumber": _lit("xsd:nonNegativeInteger", "1"),
            "legalproc:countLabel": "Count 1",
            "legalproc:chargeDisposition": "pending",
            "legalproc:jurisdictionKind": "federal",
            "legalproc:outcomeScope": "current-case",
            "legalproc:offenseForm": "substantive",
        },
    )
    tool = graph.create(
        Tool,
        id="kb:tool-ufed",
        name="Cellebrite UFED",
        version="7.65",
        tool_type="Mobile Extraction",
    )
    affidavit = graph.create(
        ObservableObject,
        id="kb:pacer-doc-12",
        name="Search-warrant affidavit (PACER Doc 12)",
        has_facet=[
            FileFacet(file_name="doc-12-affidavit.pdf"),
            ContentDataFacet(
                hash=[Hash(hash_method="SHA256", hash_value="cc" * 32)],
            ),
        ],
    )
    graph.create(
        ProvenanceRecord,
        id="kb:exhibit-affidavit",
        exhibit_number="PACER-Doc-12",
        object=[affidavit],
    )
    graph.upsert_node(
        "kb:action-affidavit",
        types="case-investigation:InvestigativeAction",
        properties={
            "uco-core:name": "Mobile extraction named in search-warrant affidavit",
            "uco-core:description": (
                "Affidavit states examiners used Cellebrite UFED to extract "
                "the seized phone. The filing does not name a SOLVE-IT "
                "technique. Source: PACER Doc 12, page 7."
            ),
            "uco-action:instrument": {"@id": graph.get_id(tool)},
        },
    )
    # Suggested DFT-* from the product catalog must stay off this graph.
    assert suggest_techniques_for_product("Cellebrite UFED")
    _relate(
        graph,
        graph.get_id(investigation),
        "kb:charge-1",
        "PACER docket prosecutes this charge",
        "inv-charge",
    )
    _relate(
        graph,
        "kb:action-affidavit",
        "kb:charge-1",
        "Affidavit method claim supports Count 1",
        "action-charge",
    )
    return graph


def build_and_write(scenario: str, dest: Path) -> Path:
    builders = {
        "lab-join": build_lab_join,
        "pacer-method-claim": build_pacer_method_claim,
    }
    graph = builders[scenario]()
    dest.parent.mkdir(parents=True, exist_ok=True)
    graph.write(dest)
    return dest
