#!/usr/bin/env python3
"""Agent Layer-2 PACER investigation graphs from MCP Layer-1 hashes.

Fail-closed: statute-backed FederalCharge only; named defendants only;
no usedTechnique; no invented victims, hashes, or ATT&CK.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, ProvenanceRecord
from case_uco.uco.identity import Person
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.types import Hash

KG = Path("/mnt/d/PACER_Docs/Knowledge_Graphs")
RETRIEVED = datetime(2026, 8, 28, 16, 0, tzinfo=timezone.utc)
CONTEXT = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
    "cac": "https://cacontology.projectvic.org#",
    "legal": "https://cacontology.projectvic.org/legal-outcomes#",
}


def _lit(datatype: str, value: str) -> dict[str, str]:
    return {"@type": datatype, "@value": value}


def layer1_hash(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    for node in data.get("@graph", []):
        for facet in node.get("uco-core:hasFacet") or []:
            for item in facet.get("uco-observable:hash") or []:
                value = item.get("uco-types:hashValue") or {}
                digest = value.get("@value") if isinstance(value, dict) else value
                if digest:
                    return str(digest)
    raise ValueError(f"no hash in {path}")


def _add_source(graph: CASEGraph, *, node_id: str, layer1: Path) -> None:
    digest = layer1_hash(layer1)
    graph.create(
        ObservableObject,
        id=node_id,
        name=layer1.name.replace(".jsonld", ".pdf"),
        has_facet=[
            FileFacet(file_name=layer1.name.replace(".jsonld", ".pdf"), extension="pdf"),
            ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value=digest)]),
        ],
        object_created_time=RETRIEVED,
    )


def _charge(
    graph: CASEGraph,
    node_id: str,
    *,
    name: str,
    statute: str,
    count: int,
    offense_form: str = "substantive",
    object_offense: str | None = None,
) -> None:
    props = {
        "uco-core:name": name,
        "legalproc:statuteCitation": statute,
        "legalproc:countNumber": _lit("xsd:nonNegativeInteger", str(count)),
        "legalproc:countLabel": f"Count {count}",
        "legalproc:chargeDisposition": "pending",
        "legalproc:jurisdictionKind": "federal",
        "legalproc:outcomeScope": "current-case",
        "legalproc:offenseForm": offense_form,
    }
    if object_offense:
        props["legalproc:objectOffense"] = {"@id": object_offense}
    graph.upsert_node(node_id, types="legalproc:FederalCharge", properties=props)


def _relate(graph: CASEGraph, source: str, target: str, key: str, description: str) -> None:
    graph.create_relationship(
        source,
        target,
        "Related_To",
        description=description,
        assertion_id=f"kb:rel-{key}",
    )


def build_case(
    *,
    slug: str,
    dest: Path,
    case_id: str,
    name: str,
    sources: list[tuple[str, Path]],
    charges: list[tuple[str, str, int]],
    defendant: str | None,
    victim_status: str,
    cac: bool,
    victim_count: int | None = None,
    instrument_type: str = "indictment",
    plea: dict | None = None,
) -> Path:
    graph = CASEGraph(kb_prefix=f"http://example.org/kb/{slug}/", extra_context=CONTEXT)
    graph.create(Investigation, id="kb:investigation", name=name, object_created_time=RETRIEVED)
    if cac:
        graph.add_type("kb:investigation", "cac:CACInvestigation")
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", case_id)
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", victim_status)
    if victim_status == "reported" and victim_count is not None:
        graph.add_property(
            "kb:investigation",
            "legalproc:reportedVictimCount",
            _lit("xsd:nonNegativeInteger", str(victim_count)),
        )
    graph.add_property(
        "kb:investigation",
        "legalproc:sourceRetrievalTime",
        _lit("xsd:dateTime", RETRIEVED.replace(microsecond=0).isoformat()),
    )

    source_ids: list[str] = []
    for key, path in sources:
        node_id = f"kb:source-{key}"
        _add_source(graph, node_id=node_id, layer1=path)
        graph.add_property("kb:investigation", "uco-core:object", {"@id": node_id})
        source_ids.append(node_id)

    charge_ids: list[str] = []
    if charges:
        graph.upsert_node(
            "kb:instrument",
            types="legalproc:ChargingInstrument",
            properties={
                "uco-core:name": f"Charging instrument for {case_id}",
                "legalproc:instrumentType": instrument_type,
            },
        )
        _relate(graph, "kb:investigation", "kb:instrument", "inv-instrument", "Investigation prosecutes this instrument")
        for item in charges:
            offense_form = "substantive"
            object_count = None
            if len(item) == 3:
                charge_name, statute, count = item
            elif len(item) == 4:
                charge_name, statute, count, offense_form = item
            else:
                charge_name, statute, count, offense_form, object_count = item
            node_id = f"kb:charge-{count}"
            object_offense = f"kb:charge-{object_count}" if object_count else None
            _charge(
                graph,
                node_id,
                name=charge_name,
                statute=statute,
                count=count,
                offense_form=offense_form,
                object_offense=object_offense,
            )
            graph.add_property(node_id, "legalproc:assertedIn", {"@id": "kb:instrument"})
            _relate(graph, "kb:instrument", node_id, f"inst-c{count}", f"Instrument asserts Count {count}")
            _relate(graph, "kb:investigation", node_id, f"inv-c{count}", f"Investigation prosecutes Count {count}")
            charge_ids.append(node_id)

    if defendant:
        graph.create(Person, id="kb:defendant", name=defendant)
        for node_id in charge_ids:
            graph.add_property("kb:defendant", "legal:chargedWith", {"@id": node_id})
            suffix = node_id.split(":", 1)[-1]
            _relate(graph, "kb:defendant", node_id, f"def-{suffix}", "Defendant is charged in this count")

    if plea:
        concerns = f"kb:charge-{plea['concerns_count']}"
        graph.upsert_node(
            "kb:plea",
            types="legalproc:Plea",
            properties={
                "uco-core:name": plea.get("name", "Guilty plea"),
                "legalproc:pleaType": plea["plea_type"],
                "legalproc:outcomeScope": "current-case",
                "legalproc:concernsCharge": {"@id": concerns},
            },
        )
        graph.upsert_node(
            "kb:plea-agreement",
            types="legalproc:PleaAgreement",
            properties={
                "uco-core:name": plea.get("agreement_name", "Plea agreement"),
                "legalproc:recordsPlea": {"@id": "kb:plea"},
                "legalproc:concernsCharge": {"@id": concerns},
                "legalproc:outcomeScope": "current-case",
            },
        )
        _relate(graph, "kb:investigation", "kb:plea", "inv-plea", "Investigation records this plea")
        _relate(
            graph,
            "kb:plea-agreement",
            "kb:plea",
            "agreement-plea",
            "Plea agreement records this plea",
        )
        if defendant:
            _relate(graph, "kb:defendant", "kb:plea", "def-plea", "Defendant entered this plea")

    objects = [graph.get("kb:investigation")] + [graph.get(sid) for sid in source_ids]
    graph.create(ProvenanceRecord, id="kb:provenance", exhibit_number=slug, object=objects)
    dest.parent.mkdir(parents=True, exist_ok=True)
    graph.write(dest)
    return dest


def main() -> int:
    cases = [
        dict(
            slug="doj_ceos_2025_004",
            dest=KG / "BULK_FOLDER" / "doj_ceos_2025_004-investigation.jsonld",
            case_id="1:24-cr-00227-PTG",
            name="Federal CAC prosecution 1:24-cr-00227-PTG",
            sources=[
                ("indictment", KG / "BULK_FOLDER" / "pacer -- doj_ceos_2025_004 -- indictment.jsonld"),
                ("judgment", KG / "BULK_FOLDER" / "pacer -- doj_ceos_2025_004 -- judgment.jsonld"),
                ("sof", KG / "BULK_FOLDER" / "pacer -- doj_ceos_2025_004 -- statement of facts.jsonld"),
            ],
            charges=[
                ("Production of child pornography", "18 U.S.C. § 2251(a),(e)", 1),
                ("Coercion and enticement of a minor", "18 U.S.C. § 2422(b)", 2),
                ("Receipt of child pornography", "18 U.S.C. § 2252(a)(2)", 3),
            ],
            defendant=None,
            victim_status="omitted",
            cac=True,
        ),
        dict(
            slug="sextortion",
            dest=KG / "SEXTORTION" / "sextortion-investigation.jsonld",
            case_id="3:22-cr-00055-SLG-MMS",
            name="Federal sextortion prosecution 3:22-cr-00055",
            sources=[
                ("indictment", KG / "SEXTORTION" / "PACER -- sextortion -- indictment.jsonld"),
                ("docket", KG / "SEXTORTION" / "PACER -- sextortion -- docket.jsonld"),
            ],
            charges=[
                ("Production of child pornography", "18 U.S.C. § 2251(a),(e)", 1),
                ("Receipt of child pornography", "18 U.S.C. § 2252A(a)(2),(b)", 2),
                ("Child exploitation enterprise", "18 U.S.C. § 2252A(g)", 3),
                ("Cyberstalking", "18 U.S.C. § 2261A(2)", 4),
                ("Aggravated identity theft", "18 U.S.C. § 1028A(a)(1)", 5),
                ("Wire fraud", "18 U.S.C. § 1343", 6),
            ],
            defendant=None,
            victim_status="omitted",
            cac=True,
        ),
        dict(
            slug="production-alaska",
            dest=KG / "PRODUCTION" / "ai" / "production-alaska-investigation.jsonld",
            case_id="3:24-cr-00091-SLG-KFR",
            name="U.S. v. Seth Herrera (D. Alaska production)",
            sources=[
                ("indictment", KG / "PRODUCTION" / "ai" / "PACER -- production -- indictment -- Alaska.jsonld"),
                ("docket", KG / "PRODUCTION" / "ai" / "PACER -- production -- docket -- Alaska.jsonld"),
            ],
            charges=[
                ("Transportation of child pornography", "18 U.S.C. § 2252A(a)(1),(b)", 1),
                ("Receipt of child pornography", "18 U.S.C. § 2252A(a)(2),(b)", 2),
                ("Possession of child pornography", "18 U.S.C. § 2252A(a)(5)(B),(b)", 3),
            ],
            defendant="Seth Herrera",
            victim_status="omitted",
            cac=True,
        ),
        dict(
            slug="enticement",
            dest=KG / "ENTICEMENT" / "enticement-investigation.jsonld",
            case_id="1:23-cr-00064-CJN",
            name="Federal enticement prosecution 1:23-cr-00064-CJN",
            sources=[
                ("sof", KG / "ENTICEMENT" / "PACER -- enticement -- statement of offense.jsonld"),
                ("docket", KG / "ENTICEMENT" / "PACER -- enticement -- docket.jsonld"),
            ],
            charges=[
                ("Coercion and enticement of a minor", "18 U.S.C. § 2422(b)", 1),
            ],
            defendant=None,
            victim_status="omitted",
            cac=True,
        ),
        dict(
            slug="trafficking",
            dest=KG / "TRAFFICKING" / "trafficking-investigation.jsonld",
            case_id="1:23-cr-00071-JMS",
            name="Federal trafficking prosecution 1:23-cr-00071-JMS",
            sources=[
                ("si", KG / "TRAFFICKING" / "PACER -- trafficking -- superseding indictment.jsonld"),
                ("indictment", KG / "TRAFFICKING" / "PACER -- trafficking -- indictment.jsonld"),
                ("brief", KG / "TRAFFICKING" / "PACER -- trafficking -- Trial Brief.jsonld"),
                ("docket", KG / "TRAFFICKING" / "PACER -- trafficking -- DOCKET.jsonld"),
            ],
            charges=[
                ("Production of child pornography", "18 U.S.C. § 2251(a)", 1),
                ("Sex trafficking of a minor", "18 U.S.C. § 1591(a)", 2),
                ("Coercion and enticement of a minor", "18 U.S.C. § 2422(b)", 3),
            ],
            defendant=None,
            victim_status="reported",
            victim_count=5,
            cac=True,
        ),
    ]
    for spec in cases:
        dest = build_case(**spec)
        print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
