#!/usr/bin/env python3
"""Remodel CaseLinker cases from their original public press releases.

Encode only what each source establishes. Do not copy CaseLinker private
vocab, empty ContentDataFacet markers, invented statutes, CyberTips that
the source does not assign to this matter, or victim-role counts.

The first two builders are kept as written so existing recipe-execution
IDs stay stable. Later cases share ``_build_from_record``.
"""

from __future__ import annotations

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Authorization, Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Organization, Person
from case_uco.uco.location import Location, SimpleAddressFacet
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject, URLFacet
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
for ancestor in HERE.parents:
    mcp = ancestor / "mcp_server"
    if mcp.is_dir():
        sys.path.insert(0, str(mcp))
        break

from tools.caselinker_icac_remodel import (  # noqa: E402
    join_cybertip_investigation,
    refuse_caselinker_vocab,
    set_phase_clock,
)

CONTEXT = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
    "cac": "https://cacontology.projectvic.org#",
    "ncmec": "https://cacontology.projectvic.org/us/ncmec#",
    "taskforce": "https://cacontology.projectvic.org/taskforce#",
    "legal": "https://cacontology.projectvic.org/legal-outcomes#",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
}

RETRIEVED = datetime(2026, 8, 27, 19, 14, tzinfo=timezone.utc)


def _lit(datatype: str, value: str) -> dict[str, str]:
    return {"@type": datatype, "@value": value}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _new_graph(prefix: str) -> CASEGraph:
    return CASEGraph(kb_prefix=prefix, extra_context=CONTEXT)


def _add_source(
    graph: CASEGraph,
    *,
    source_id: str,
    url: str,
    file_name: str,
    published: str,
    source_path: Path,
) -> ObservableObject:
    digest = _sha256(source_path)
    source = graph.create(
        ObservableObject,
        id=source_id,
        name="Public press release (CaseLinker source document)",
        has_facet=[
            URLFacet(full_value=url),
            FileFacet(file_name=file_name, size_in_bytes=source_path.stat().st_size),
            ContentDataFacet(
                hash=[Hash(hash_method="SHA256", hash_value=digest)],
                mime_type="text/plain",
                size_in_bytes=source_path.stat().st_size,
            ),
        ],
        object_created_time=RETRIEVED,
    )
    graph.add_property(source_id, "legalproc:sourcePublicationTime", _lit("xsd:dateTime", published))
    graph.add_property(
        source_id,
        "legalproc:sourceRetrievalTime",
        _lit("xsd:dateTime", RETRIEVED.replace(microsecond=0).isoformat()),
    )
    return source


def build_ncmec_2025_356() -> CASEGraph:
    source_path = HERE / "sources" / "ncmec_2025_356-doj.txt"
    graph = _new_graph("http://example.org/kb/ncmec-2025-356/")
    graph.create(
        Investigation,
        id="kb:investigation",
        name="NDIA 24-CR-4047 CyberTip prosecution",
        object_created_time=RETRIEVED,
    )
    graph.add_type("kb:investigation", "cac:CACInvestigation")
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "24-CR-4047")
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", "omitted")

    source = _add_source(
        graph,
        source_id="kb:source",
        url="https://www.justice.gov/usao-ndia/pr/mapleton-iowa-man-who-possessed-child-pornography-sentenced-federal-prison",
        file_name="ncmec_2025_356-doj.txt",
        published="2025-05-21T00:00:00Z",
        source_path=source_path,
    )
    graph.add_property("kb:investigation", "uco-core:object", {"@id": "kb:source"})

    graph.create(Person, id="kb:defendant", name="Gregory William Douglas McCormick")
    graph.upsert_node(
        "kb:jurisdiction",
        types="legalproc:FederalJurisdiction",
        properties={"uco-core:name": "United States, Northern District of Iowa"},
    )

    graph.create(
        ObservableObject,
        id="kb:cybertip",
        name="NCMEC CyberTip assigned to Iowa ICAC (Kik report)",
        object_created_time=RETRIEVED,
    )
    graph.add_type("kb:cybertip", "ncmec:NCMECCybertipReport")
    join_cybertip_investigation(
        graph,
        tip_id="kb:cybertip",
        investigation_id="kb:investigation",
        trigger_id="kb:trigger",
    )

    graph.create(Organization, id="kb:tf", name="Iowa Internet Crimes Against Children Task Force")
    graph.add_type("kb:tf", "taskforce:ICACtaskForce")
    graph.create(Organization, id="kb:dci", name="Iowa Division of Criminal Investigation Cyber Crime Bureau")
    graph.create(Tool, id="kb:tool-cybertipline", name="NCMEC CyberTipline", version="public")

    receive = graph.create(
        InvestigativeAction,
        id="kb:action-receive-tip",
        name="Receive Kik-originated CyberTip",
        object_created_time=RETRIEVED,
    )
    graph.add_property("kb:action-receive-tip", "uco-action:object", {"@id": "kb:cybertip"})
    graph.add_property("kb:action-receive-tip", "uco-action:instrument", {"@id": "kb:tool-cybertipline"})
    graph.add_property("kb:action-receive-tip", "uco-action:performer", {"@id": "kb:tf"})
    graph.add_property(
        "kb:action-receive-tip",
        "uco-core:description",
        "Kik reported an account to NCMEC in 2022. A CyberTip was assigned to the Iowa ICAC Task Force. Iowa DCI Cyber Crime Bureau later investigated. The source does not give a tip timestamp more precise than 2022. CAC SHACL allows one performer.",
    )
    graph.create_relationship(
        "kb:tf",
        "kb:dci",
        "Related_To",
        description="Iowa ICAC partners with Iowa DCI Cyber Crime Bureau.",
        assertion_id="kb:rel-partner-dci",
    )

    graph.create(
        Authorization,
        id="kb:authorization",
        name="Search warrant for the reported residence",
        object_created_time=RETRIEVED,
    )
    warrant = graph.create(
        InvestigativeAction,
        id="kb:action-warrant",
        name="Execute search warrant and interview",
        object_created_time=RETRIEVED,
    )
    graph.add_property(
        "kb:action-warrant",
        "case-investigation:relevantAuthorization",
        {"@id": "kb:authorization"},
    )
    graph.add_property("kb:action-warrant", "uco-action:performer", {"@id": "kb:dci"})
    graph.add_property(
        "kb:action-warrant",
        "uco-core:description",
        "Law enforcement executed a search warrant at the Mapleton residence. The defendant confirmed responsibility for the CyberTip-connected receipts and distribution. The source does not state warrant time, resistance, or weapons.",
    )

    exam = graph.create(
        InvestigativeAction,
        id="kb:action-exam",
        name="Forensic search of cell phones and Kik account",
        object_created_time=RETRIEVED,
    )
    graph.add_property("kb:action-exam", "uco-action:performer", {"@id": "kb:dci"})
    graph.add_property(
        "kb:action-exam",
        "uco-core:description",
        "Source reports 120 images and 7 videos. No cryptographic hash, PhotoDNA value, file name, or MIME type is published. No ContentDataFacet is emitted.",
    )

    graph.upsert_node(
        "kb:charge-possession",
        types=["legal:CriminalCharge", "legal:CSAM_Possession", "uco-core:UcoObject"],
        properties={
            "uco-core:name": "Possession of child pornography",
            "uco-core:description": "Guilty plea January 6, 2025. The press release does not cite a United States Code section, so legalproc:FederalCharge is not emitted.",
        },
    )
    graph.create_relationship(
        "kb:defendant",
        "kb:charge-possession",
        "Related_To",
        description="Defendant pleaded guilty to possession of child pornography.",
        assertion_id="kb:rel-charged",
    )
    graph.add_property("kb:defendant", "legal:chargedWith", {"@id": "kb:charge-possession"})

    graph.upsert_node(
        "kb:plea",
        types="legalproc:Plea",
        properties={
            "uco-core:name": "Guilty plea",
            "uco-core:description": "Entered January 6, 2025.",
            "legalproc:pleaType": "guilty",
            "legalproc:outcomeScope": "current-case",
        },
    )
    graph.upsert_node(
        "kb:sentence-prison",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Imposed custodial sentence",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "60 months",
            "legalproc:outcomeScope": "current-case",
        },
    )
    graph.upsert_node(
        "kb:sentence-supervised",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Imposed supervised release",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "supervised-release",
            "legalproc:sentenceTerm": "5 years",
            "legalproc:outcomeScope": "current-case",
        },
    )
    graph.upsert_node(
        "kb:restitution",
        types="legalproc:RestitutionOrder",
        properties={
            "uco-core:name": "Restitution and assessments",
            "legalproc:monetaryAmount": _lit("xsd:decimal", "10100"),
            "legalproc:currencyCode": "USD",
            "uco-core:description": "Source states $10,100 in restitution and assessments. Assessments are not typed as Sentence.",
        },
    )

    set_phase_clock(
        graph,
        phase_id="kb:phase-legal",
        phase_type="cac:LegalProcessPhase",
        begin="2025-01-06T00:00:00Z",
        end=None,
        name="Plea and sentencing",
    )
    graph.add_property("kb:investigation", "cac:hasPhase", {"@id": "kb:phase-legal"})
    graph.add_property("kb:investigation", "cac:hasStep", {"@id": "kb:action-receive-tip"})
    graph.add_property("kb:investigation", "cac:hasStep", {"@id": "kb:action-warrant"})
    graph.add_property("kb:investigation", "cac:hasStep", {"@id": "kb:action-exam"})

    graph.create(
        ProvenanceRecord,
        id="kb:prov-source",
        name="DOJ USAO NDIA press release",
        object_created_time=RETRIEVED,
        exhibit_number="source-1",
        object=[source],
    )
    refuse_caselinker_vocab([])
    _ = (receive, warrant, exam)
    return graph


def build_illinois_ag_2025_001() -> CASEGraph:
    source_path = HERE / "sources" / "illinois_ag_2025_001-il-ag.txt"
    graph = _new_graph("http://example.org/kb/illinois-ag-2025-001/")
    graph.create(
        Investigation,
        id="kb:investigation",
        name="Macoupin County dissemination charges",
        object_created_time=RETRIEVED,
    )
    graph.add_type("kb:investigation", "cac:CACInvestigation")
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", "omitted")

    source = _add_source(
        graph,
        source_id="kb:source",
        url="https://illinoisattorneygeneral.gov/news/story/attorney-general-raoul-charges-macoupin-county-man-for-disseminating-child-sexual-abuse-material",
        file_name="illinois_ag_2025_001-il-ag.txt",
        published="2025-12-09T00:00:00Z",
        source_path=source_path,
    )
    graph.add_property("kb:investigation", "uco-core:object", {"@id": "kb:source"})

    graph.create(Person, id="kb:defendant", name="Jacob D. Monty")
    graph.upsert_node(
        "kb:jurisdiction",
        types="legalproc:StateJurisdiction",
        properties={"uco-core:name": "Illinois, Macoupin County"},
    )
    graph.create(Organization, id="kb:tf", name="Illinois Internet Crimes Against Children Task Force")
    graph.add_type("kb:tf", "taskforce:ICACtaskForce")
    graph.create(Organization, id="kb:virden-pd", name="Virden Police Department")
    graph.create(Organization, id="kb:macoupin-sa", name="Macoupin County State's Attorney")

    search = graph.create(
        InvestigativeAction,
        id="kb:action-search",
        name="Search residence and arrest",
        object_created_time=RETRIEVED,
    )
    graph.add_property("kb:action-search", "uco-action:performer", {"@id": "kb:tf"})
    graph.add_property(
        "kb:action-search",
        "uco-core:description",
        "AG investigators and Virden Police searched a residence in the 300 block of East Holden Street, Virden. The defendant was arrested after evidence was found. The source does not state a warrant, a CyberTip assigned to this matter, resistance, or weapons. CAC SHACL allows one performer.",
    )
    graph.create_relationship(
        "kb:tf",
        "kb:virden-pd",
        "Related_To",
        description="Illinois ICAC partners with Virden Police Department.",
        assertion_id="kb:rel-partner-virden",
    )
    graph.create(
        Location,
        id="kb:location-residence",
        has_facet=[
            SimpleAddressFacet(
                street="300 block of East Holden Street",
                locality="Virden",
                region="Illinois",
            )
        ],
    )
    graph.add_property("kb:action-search", "uco-action:location", {"@id": "kb:location-residence"})

    for index in (1, 2):
        charge_id = f"kb:charge-{index}"
        graph.upsert_node(
            charge_id,
            types=["legal:CriminalCharge", "legal:CSAM_Distribution", "uco-core:UcoObject"],
            properties={
                "uco-core:name": f"Dissemination of child pornography, Count {index}",
                "uco-core:description": "Class X felony. The press release does not cite an ILCS section, so legalproc:StateCharge is not emitted.",
            },
        )
        graph.add_property("kb:defendant", "legal:chargedWith", {"@id": charge_id})
        graph.create_relationship(
            "kb:defendant",
            charge_id,
            "Related_To",
            description=f"Defendant is charged with Count {index} in Macoupin County Circuit Court.",
            assertion_id=f"kb:rel-charged-{index}",
        )

    graph.upsert_node(
        "kb:potential-penalty",
        types="legalproc:PotentialPenalty",
        properties={
            "uco-core:name": "Class X statutory maximum",
            "uco-core:description": "Each count is punishable by up to 30 years. Not an imposed sentence.",
            "legalproc:potentialPenaltyKind": "statutory-maximum",
            "legalproc:outcomeScope": "current-case",
        },
    )
    graph.create_relationship(
        "kb:potential-penalty",
        "kb:charge-1",
        "Related_To",
        description="Statutory maximum applies to each dissemination count.",
        assertion_id="kb:rel-penalty",
    )

    set_phase_clock(
        graph,
        phase_id="kb:phase-legal",
        phase_type="cac:LegalProcessPhase",
        begin="2025-12-09T00:00:00Z",
        end=None,
        name="Charging",
    )
    graph.add_property("kb:investigation", "cac:hasPhase", {"@id": "kb:phase-legal"})
    graph.add_property("kb:investigation", "cac:hasStep", {"@id": "kb:action-search"})

    graph.create(
        ProvenanceRecord,
        id="kb:prov-source",
        name="Illinois Attorney General press release",
        object_created_time=RETRIEVED,
        exhibit_number="source-1",
        object=[source],
    )
    refuse_caselinker_vocab([])
    _ = search
    return graph


def _build_from_record(rec: dict) -> CASEGraph:
    """Fail-closed remodel from a sourced fact record (not live CaseLinker RDF)."""
    source_path = HERE / "sources" / rec["source_file"]
    graph = _new_graph(rec["kb_prefix"])
    graph.create(
        Investigation,
        id="kb:investigation",
        name=rec["investigation_name"],
        object_created_time=RETRIEVED,
    )
    graph.add_type("kb:investigation", "cac:CACInvestigation")
    if rec.get("case_identifier"):
        graph.add_property("kb:investigation", "legalproc:caseIdentifier", rec["case_identifier"])
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", rec["victim_status"])
    if rec.get("victim_count") is not None:
        graph.add_property(
            "kb:investigation",
            "legalproc:reportedVictimCount",
            _lit("xsd:nonNegativeInteger", str(rec["victim_count"])),
        )

    source = _add_source(
        graph,
        source_id="kb:source",
        url=rec["source_url"],
        file_name=rec["source_file"],
        published=rec["published"],
        source_path=source_path,
    )
    graph.add_property("kb:investigation", "uco-core:object", {"@id": "kb:source"})
    graph.create(Person, id="kb:defendant", name=rec["defendant_name"])
    graph.upsert_node(
        "kb:jurisdiction",
        types=rec["jurisdiction_type"],
        properties={"uco-core:name": rec["jurisdiction_name"]},
    )

    for org in rec.get("organizations", []):
        graph.create(Organization, id=org["id"], name=org["name"])
        if org.get("extra_type"):
            graph.add_type(org["id"], org["extra_type"])

    if rec.get("cybertip_name"):
        graph.create(
            ObservableObject,
            id="kb:cybertip",
            name=rec["cybertip_name"],
            object_created_time=RETRIEVED,
        )
        graph.add_type("kb:cybertip", "ncmec:NCMECCybertipReport")
        join_cybertip_investigation(
            graph,
            tip_id="kb:cybertip",
            investigation_id="kb:investigation",
            trigger_id="kb:trigger",
        )

    if rec.get("authorization_name"):
        graph.create(
            Authorization,
            id="kb:authorization",
            name=rec["authorization_name"],
            object_created_time=RETRIEVED,
        )

    if rec.get("location"):
        loc = rec["location"]
        graph.create(
            Location,
            id="kb:location",
            has_facet=[
                SimpleAddressFacet(
                    street=loc.get("street"),
                    locality=loc.get("locality"),
                    region=loc.get("region"),
                )
            ],
        )

    action_ids: list[str] = []
    for action in rec.get("actions", []):
        action_ids.append(action["id"])
        graph.create(
            InvestigativeAction,
            id=action["id"],
            name=action["name"],
            object_created_time=RETRIEVED,
        )
        graph.add_property(action["id"], "uco-action:performer", {"@id": action["performer"]})
        graph.add_property(action["id"], "uco-core:description", action["description"])
        if action.get("instrument"):
            graph.add_property(action["id"], "uco-action:instrument", {"@id": action["instrument"]})
        if action.get("object"):
            graph.add_property(action["id"], "uco-action:object", {"@id": action["object"]})
        if action.get("authorization"):
            graph.add_property(
                action["id"],
                "case-investigation:relevantAuthorization",
                {"@id": action["authorization"]},
            )
        if action.get("location"):
            graph.add_property(action["id"], "uco-action:location", {"@id": action["location"]})
        graph.add_property("kb:investigation", "cac:hasStep", {"@id": action["id"]})

    for rel in rec.get("relationships", []):
        graph.create_relationship(
            rel["source"],
            rel["target"],
            "Related_To",
            description=rel["description"],
            assertion_id=rel["id"],
        )

    for charge in rec.get("charges", []):
        types = list(charge["types"])
        props = {
            "uco-core:name": charge["name"],
            "uco-core:description": charge["description"],
        }
        if charge.get("statute"):
            props["legalproc:statuteCitation"] = charge["statute"]
            props["legalproc:countNumber"] = _lit(
                "xsd:nonNegativeInteger", str(charge.get("count", 1))
            )
            props["legalproc:countLabel"] = charge.get(
                "count_label", f"Count {charge.get('count', 1)}"
            )
            props["legalproc:chargeDisposition"] = charge.get("disposition", "pending")
            props["legalproc:jurisdictionKind"] = charge["jurisdiction_kind"]
            props["legalproc:outcomeScope"] = charge.get("scope", "current-case")
        graph.upsert_node(charge["id"], types=types, properties=props)
        graph.add_property("kb:defendant", "legal:chargedWith", {"@id": charge["id"]})
        if charge.get("statute"):
            graph.add_property("kb:defendant", "legalproc:chargedWith", {"@id": charge["id"]})
        graph.create_relationship(
            "kb:defendant",
            charge["id"],
            "Related_To",
            description=charge.get("rel_description", "Defendant is charged."),
            assertion_id=f"kb:rel-{charge['id'].split(':')[-1]}",
        )

    if rec.get("plea"):
        plea = rec["plea"]
        plea_props = {
            "uco-core:name": plea["name"],
            "legalproc:pleaType": plea["plea_type"],
            "legalproc:outcomeScope": plea.get("scope", "current-case"),
        }
        if plea.get("description"):
            plea_props["uco-core:description"] = plea["description"]
        if plea.get("concerns"):
            plea_props["legalproc:concernsCharge"] = {"@id": plea["concerns"]}
        graph.upsert_node("kb:plea", types="legalproc:Plea", properties=plea_props)

    for sentence in rec.get("sentences", []):
        props = {
            "uco-core:name": sentence["name"],
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": sentence["kind"],
            "legalproc:sentenceTerm": sentence["term"],
            "legalproc:outcomeScope": sentence.get("scope", "current-case"),
        }
        if sentence.get("description"):
            props["uco-core:description"] = sentence["description"]
        if sentence.get("applies_to"):
            props["legalproc:appliesTo"] = {"@id": sentence["applies_to"]}
        graph.upsert_node(sentence["id"], types="legalproc:Sentence", properties=props)

    if rec.get("restitution"):
        rest = rec["restitution"]
        graph.upsert_node(
            rest["id"],
            types="legalproc:RestitutionOrder",
            properties={
                "uco-core:name": rest["name"],
                "legalproc:monetaryAmount": _lit("xsd:decimal", rest["amount"]),
                "legalproc:currencyCode": "USD",
                "uco-core:description": rest["description"],
            },
        )

    for penalty in rec.get("potential_penalties", []):
        graph.upsert_node(
            penalty["id"],
            types="legalproc:PotentialPenalty",
            properties={
                "uco-core:name": penalty["name"],
                "uco-core:description": penalty["description"],
                "legalproc:potentialPenaltyKind": penalty["kind"],
                "legalproc:outcomeScope": penalty.get("scope", "current-case"),
            },
        )
        if penalty.get("related_charge"):
            graph.create_relationship(
                penalty["id"],
                penalty["related_charge"],
                "Related_To",
                description=penalty.get(
                    "rel_description", "Potential penalty applies to this charge."
                ),
                assertion_id=f"kb:rel-{penalty['id'].split(':')[-1]}",
            )

    set_phase_clock(
        graph,
        phase_id="kb:phase-legal",
        phase_type="cac:LegalProcessPhase",
        begin=rec["phase_begin"],
        end=None,
        name=rec["phase_name"],
    )
    graph.add_property("kb:investigation", "cac:hasPhase", {"@id": "kb:phase-legal"})

    graph.create(
        ProvenanceRecord,
        id="kb:prov-source",
        name=rec["provenance_name"],
        object_created_time=RETRIEVED,
        exhibit_number="source-1",
        object=[source],
    )
    refuse_caselinker_vocab([])
    _ = action_ids
    return graph


def build_usss_2022_005() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/usss-2022-005/",
            "investigation_name": "CDIL possession sentence (East Peoria)",
            "source_file": "usss_2022_005-usss.txt",
            "source_url": (
                "https://www.secretservice.gov/newsroom/releases/2022/03/"
                "east-peoria-man-sentenced-151-months-prison-possession-child-sexual-abuse"
            ),
            "published": "2022-03-25T00:00:00Z",
            "defendant_name": "Noah Joseph Smith",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Central District of Illinois",
            "victim_status": "omitted",
            "organizations": [
                {"id": "kb:usss", "name": "United States Secret Service"},
                {"id": "kb:probation", "name": "United States Probation Office"},
                {"id": "kb:peoria-so", "name": "Peoria County Sheriff's Office"},
            ],
            "location": {
                "street": "100 block of Regent Court",
                "locality": "East Peoria",
                "region": "Illinois",
            },
            "actions": [
                {
                    "id": "kb:action-home-visit",
                    "name": "Supervised-release home visit",
                    "performer": "kb:probation",
                    "location": "kb:location",
                    "description": (
                        "A U.S. Probation Officer found an unreported LG smart phone "
                        "during a March 2021 home visit. The source does not assign a "
                        "CyberTip. No ContentDataFacet is emitted for the phone."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-usss",
                    "source": "kb:probation",
                    "target": "kb:usss",
                    "description": "Probation referred the matter; USSS investigated.",
                },
                {
                    "id": "kb:rel-partner-peoria",
                    "source": "kb:usss",
                    "target": "kb:peoria-so",
                    "description": "USSS investigated with Peoria County Sheriff's Office.",
                },
            ],
            "charges": [
                {
                    "id": "kb:charge-possession",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Possession", "uco-core:UcoObject"],
                    "name": "Possession of child pornography",
                    "description": (
                        "Guilty plea September 2021 after April 2021 indictment. "
                        "The release cites 18 U.S.C. § 3014 and § 2259A only for "
                        "special assessments, not the possession count, so "
                        "legalproc:FederalCharge is not emitted."
                    ),
                    "disposition": "guilty-plea",
                    "rel_description": "Defendant pleaded guilty to possession of child pornography.",
                }
            ],
            "plea": {
                "name": "Guilty plea",
                "plea_type": "guilty",
                "description": "Entered September 2021.",
            },
            "sentences": [
                {
                    "id": "kb:sentence-prison",
                    "name": "Imposed custodial sentence",
                    "kind": "custodial",
                    "term": "151 months",
                    "description": "12 years and seven months imposed March 23, 2022.",
                },
                {
                    "id": "kb:sentence-supervised",
                    "name": "Imposed supervised release",
                    "kind": "supervised-release",
                    "term": "life",
                },
                {
                    "id": "kb:sentence-sr-violation",
                    "name": "Concurrent supervised-release violation term",
                    "kind": "custodial",
                    "term": "24 months",
                    "description": "Concurrent with the instant possession sentence.",
                },
            ],
            "restitution": {
                "id": "kb:restitution",
                "name": "Restitution",
                "amount": "23000",
                "description": "Source states $23,000 restitution. No fine was imposed. Assessments under 18 U.S.C. § 3014 / § 2259A are not typed as Sentence.",
            },
            "phase_begin": "2022-03-23T00:00:00Z",
            "phase_name": "Sentencing",
            "provenance_name": "USSS / USAO CDIL press release",
        }
    )


def build_illinois_ag_2025_023() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/illinois-ag-2025-023/",
            "investigation_name": "Greene County possession sentence",
            "source_file": "illinois_ag_2025_023-il-ag.txt",
            "source_url": (
                "https://illinoisattorneygeneral.gov/news/story/attorney-general-raoul-obtains-10-year-prison-sentence-for-greene-county-man-who-possessed-child-sexual-abuse-material"
            ),
            "published": "2025-06-04T00:00:00Z",
            "defendant_name": "Ethan T. Seaton",
            "jurisdiction_type": "legalproc:StateJurisdiction",
            "jurisdiction_name": "Illinois, Greene County",
            "victim_status": "omitted",
            "organizations": [
                {
                    "id": "kb:tf",
                    "name": "Illinois Internet Crimes Against Children Task Force",
                    "extra_type": "taskforce:ICACtaskForce",
                },
                {"id": "kb:roodhouse-pd", "name": "Roodhouse Police Department"},
                {
                    "id": "kb:isp-taskforce",
                    "name": "Illinois State Police South Central Illinois Drug Task Force",
                },
                {"id": "kb:greene-sa", "name": "Greene County State's Attorney"},
            ],
            "actions": [
                {
                    "id": "kb:action-search",
                    "name": "Search residence and arrest",
                    "performer": "kb:tf",
                    "description": (
                        "AG investigators searched a Roodhouse residence in September "
                        "2024 with Roodhouse PD and the ISP South Central Illinois Drug "
                        "Task Force. The defendant was arrested after admitting "
                        "possession. The CyberTip and 45-victim figures in the release "
                        "are Illinois ICAC program background, not facts of this matter. "
                        "CAC SHACL allows one performer."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-roodhouse",
                    "source": "kb:tf",
                    "target": "kb:roodhouse-pd",
                    "description": "Illinois ICAC partners with Roodhouse Police Department.",
                },
                {
                    "id": "kb:rel-partner-isp",
                    "source": "kb:tf",
                    "target": "kb:isp-taskforce",
                    "description": "Illinois ICAC partners with the ISP drug task force on this search.",
                },
            ],
            "charges": [
                {
                    "id": "kb:charge-1",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Possession", "uco-core:UcoObject"],
                    "name": "Possession of child pornography, Count 1",
                    "description": "Class 2 felony. No ILCS section, so legalproc:StateCharge is not emitted.",
                    "rel_description": "Defendant pleaded guilty to Count 1.",
                },
                {
                    "id": "kb:charge-2",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Possession", "uco-core:UcoObject"],
                    "name": "Possession of child pornography, Count 2",
                    "description": "Class 2 felony. No ILCS section, so legalproc:StateCharge is not emitted.",
                    "rel_description": "Defendant pleaded guilty to Count 2.",
                },
            ],
            "plea": {
                "name": "Guilty plea",
                "plea_type": "guilty",
                "description": "Pleaded guilty to two Class 2 possession counts before sentencing.",
            },
            "sentences": [
                {
                    "id": "kb:sentence-prison",
                    "name": "Imposed custodial sentence",
                    "kind": "custodial",
                    "term": "10 years",
                    "description": "Imposed by Greene County Circuit Court Judge Zachary Schmidt.",
                }
            ],
            "phase_begin": "2025-06-03T00:00:00Z",
            "phase_name": "Plea and sentencing",
            "provenance_name": "Illinois Attorney General press release",
        }
    )


def build_usss_2017_007() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/usss-2017-007/",
            "investigation_name": "NDCA Ridder indictment",
            "source_file": "usss_2017_007-usss.txt",
            "source_url": (
                "https://www.secretservice.gov/press/releases/2017/05/"
                "mountain-view-resident-charged-production-child-pornography-and"
            ),
            "published": "2017-05-25T00:00:00Z",
            "defendant_name": "Grant Ridder",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Northern District of California",
            "victim_status": "reported",
            "victim_count": 2,
            "organizations": [
                {"id": "kb:usss", "name": "United States Secret Service"},
                {"id": "kb:ccda", "name": "Contra Costa District Attorney's Office"},
                {"id": "kb:stockton-pd", "name": "Stockton Police Department"},
                {"id": "kb:martinez-pd", "name": "Martinez Police Department"},
            ],
            "authorization_name": "Search warrant referenced in the public filing",
            "actions": [
                {
                    "id": "kb:action-arrest",
                    "name": "Arrest and remand",
                    "performer": "kb:usss",
                    "authorization": "kb:authorization",
                    "description": (
                        "Ridder was arrested and remanded to the U.S. Marshal on "
                        "May 24, 2017, after a May 18, 2017 indictment. The source "
                        "does not assign a CyberTip. CAC SHACL allows one performer."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-ccda",
                    "source": "kb:usss",
                    "target": "kb:ccda",
                    "description": "USSS investigated with Contra Costa DA's Office.",
                }
            ],
            "charges": [
                {
                    "id": "kb:charge-2251a",
                    "types": [
                        "legalproc:FederalCharge",
                        "legal:CriminalCharge",
                        "legal:CSAM_Production",
                        "uco-core:UcoObject",
                    ],
                    "name": "Production of child pornography",
                    "statute": "18 U.S.C. § 2251(a)",
                    "count": 2,
                    "count_label": "Two counts",
                    "jurisdiction_kind": "federal",
                    "disposition": "pending",
                    "description": "Indictment allegation. Presumed innocent.",
                    "rel_description": "Defendant is charged with two production counts.",
                },
                {
                    "id": "kb:charge-2252a2",
                    "types": [
                        "legalproc:FederalCharge",
                        "legal:CriminalCharge",
                        "legal:CSAM_Distribution",
                        "uco-core:UcoObject",
                    ],
                    "name": "Distribution of child pornography",
                    "statute": "18 U.S.C. § 2252(a)(2)",
                    "count": 3,
                    "count_label": "Three counts",
                    "jurisdiction_kind": "federal",
                    "disposition": "pending",
                    "description": "Indictment allegation. Presumed innocent.",
                    "rel_description": "Defendant is charged with three distribution counts.",
                },
                {
                    "id": "kb:charge-2252a4",
                    "types": [
                        "legalproc:FederalCharge",
                        "legal:CriminalCharge",
                        "legal:CSAM_Possession",
                        "uco-core:UcoObject",
                    ],
                    "name": "Possession of child pornography",
                    "statute": "18 U.S.C. § 2252(a)(4)(B)",
                    "count": 1,
                    "jurisdiction_kind": "federal",
                    "disposition": "pending",
                    "description": "Indictment allegation. Presumed innocent.",
                    "rel_description": "Defendant is charged with one possession count.",
                },
                {
                    "id": "kb:charge-2261a",
                    "types": ["legalproc:FederalCharge", "legal:CriminalCharge", "uco-core:UcoObject"],
                    "name": "Cyberstalking",
                    "statute": "18 U.S.C. § 2261A",
                    "count": 3,
                    "count_label": "Three counts",
                    "jurisdiction_kind": "federal",
                    "disposition": "pending",
                    "description": "Indictment allegation. Presumed innocent.",
                    "rel_description": "Defendant is charged with three cyberstalking counts.",
                },
                {
                    "id": "kb:charge-2422b",
                    "types": [
                        "legalproc:FederalCharge",
                        "legal:CriminalCharge",
                        "legal:OnlineEnticement",
                        "uco-core:UcoObject",
                    ],
                    "name": "Coercion and enticement of a minor",
                    "statute": "18 U.S.C. § 2422(b)",
                    "count": 1,
                    "jurisdiction_kind": "federal",
                    "disposition": "pending",
                    "description": "Indictment allegation. Presumed innocent.",
                    "rel_description": "Defendant is charged with one 2422(b) count.",
                },
            ],
            "potential_penalties": [
                {
                    "id": "kb:penalty-2251a",
                    "name": "Statutory range for 18 U.S.C. § 2251(a)",
                    "kind": "mandatory-minimum",
                    "description": "Mandatory minimum 15 years, maximum 30 years, $250,000 fine. Not an imposed sentence.",
                    "related_charge": "kb:charge-2251a",
                },
                {
                    "id": "kb:penalty-2252a2",
                    "name": "Statutory range for 18 U.S.C. § 2252(a)(2)",
                    "kind": "mandatory-minimum",
                    "description": "Mandatory minimum 5 years, maximum 20 years, $250,000 fine. Not an imposed sentence.",
                    "related_charge": "kb:charge-2252a2",
                },
                {
                    "id": "kb:penalty-2252a4",
                    "name": "Statutory maximum for 18 U.S.C. § 2252(a)(4)(B)",
                    "kind": "statutory-maximum",
                    "description": "Maximum 10 years and $250,000 fine. Not an imposed sentence.",
                    "related_charge": "kb:charge-2252a4",
                },
                {
                    "id": "kb:penalty-2261a",
                    "name": "Statutory maximum for 18 U.S.C. § 2261A",
                    "kind": "statutory-maximum",
                    "description": "Maximum 5 years and $250,000 fine. Not an imposed sentence.",
                    "related_charge": "kb:charge-2261a",
                },
                {
                    "id": "kb:penalty-2422b",
                    "name": "Statutory range for 18 U.S.C. § 2422(b)",
                    "kind": "mandatory-minimum",
                    "description": "Mandatory minimum 10 years, maximum life, $250,000 fine. Not an imposed sentence.",
                    "related_charge": "kb:charge-2422b",
                },
            ],
            "phase_begin": "2017-05-18T00:00:00Z",
            "phase_name": "Indictment and arraignment",
            "provenance_name": "USSS / USAO NDCA press release",
        }
    )


def build_ncmec_2024_754() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/ncmec-2024-754/",
            "investigation_name": "WDNY Swain production plea",
            "source_file": "ncmec_2024_754-doj.txt",
            "source_url": (
                "https://www.justice.gov/usao-wdny/pr/tonawanda-man-pleads-guilty-production-child-pornography-0"
            ),
            "published": "2024-08-02T00:00:00Z",
            "defendant_name": "Michael E. Swain",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Western District of New York",
            "victim_status": "reported",
            "victim_count": 5,
            "organizations": [
                {"id": "kb:fbi", "name": "FBI Buffalo Office Child Exploitation Human Trafficking Task Force"},
                {"id": "kb:tonawanda-pd", "name": "Tonawanda Police Department"},
                {"id": "kb:nysp", "name": "New York State Police"},
            ],
            "authorization_name": "Search warrant for the Tonawanda residence",
            "actions": [
                {
                    "id": "kb:action-warrant",
                    "name": "Execute search warrant",
                    "performer": "kb:fbi",
                    "authorization": "kb:authorization",
                    "description": (
                        "FBI executed a search warrant on February 28, 2023, and seized "
                        "a desktop, a laptop, and an external hard drive. No hashes are "
                        "published. The source does not assign a CyberTip. CAC SHACL "
                        "allows one performer."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-pd",
                    "source": "kb:fbi",
                    "target": "kb:tonawanda-pd",
                    "description": "FBI investigated with Tonawanda Police Department.",
                }
            ],
            "charges": [
                {
                    "id": "kb:charge-production",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Production", "uco-core:UcoObject"],
                    "name": "Production of child pornography",
                    "description": (
                        "Guilty plea. The press release does not cite a United States "
                        "Code section, so legalproc:FederalCharge is not emitted."
                    ),
                    "rel_description": "Defendant pleaded guilty to production of child pornography.",
                }
            ],
            "plea": {
                "name": "Guilty plea",
                "plea_type": "guilty",
                "description": "Entered August 2, 2024, before Judge Vilardo. Sentencing was scheduled for December 4, 2024; this release does not report the imposed term.",
            },
            "potential_penalties": [
                {
                    "id": "kb:potential-penalty",
                    "name": "Statutory range for production",
                    "kind": "mandatory-minimum",
                    "description": "Mandatory minimum 15 years, maximum 30 years, $250,000 fine. Not an imposed sentence.",
                    "related_charge": "kb:charge-production",
                }
            ],
            "phase_begin": "2024-08-02T00:00:00Z",
            "phase_name": "Guilty plea",
            "provenance_name": "DOJ USAO WDNY press release",
        }
    )


def build_ncmec_2023_609() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/ncmec-2023-609/",
            "investigation_name": "MDNC Smith production and distribution sentence",
            "source_file": "ncmec_2023_609-doj.txt",
            "source_url": (
                "https://www.justice.gov/usao-mdnc/pr/davie-county-man-sentenced-50-years-production-and-distribution-child-pornography"
            ),
            "published": "2023-11-28T00:00:00Z",
            "defendant_name": "Steven Tyler Smith",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Middle District of North Carolina",
            "victim_status": "reported",
            "victim_count": 1,
            "cybertip_name": "NCMEC CyberTip (Davie County upload, September 2021)",
            "organizations": [
                {"id": "kb:dhs", "name": "Department of Homeland Security"},
                {"id": "kb:davie-so", "name": "Davie County Sheriff's Office"},
            ],
            "actions": [
                {
                    "id": "kb:action-receive-tip",
                    "name": "Receive CyberTip",
                    "performer": "kb:dhs",
                    "object": "kb:cybertip",
                    "description": (
                        "NCMEC received a cybertip in September 2021 that an individual "
                        "in Davie County was uploading and distributing child pornography. "
                        "The source does not name a second tip. Forensic review found "
                        "more than 1,500 images and videos; no hash is published."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-davie",
                    "source": "kb:dhs",
                    "target": "kb:davie-so",
                    "description": "DHS investigated with Davie County Sheriff's Office.",
                }
            ],
            "charges": [
                {
                    "id": "kb:charge-production",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Production", "uco-core:UcoObject"],
                    "name": "Production of child pornography",
                    "description": "Guilty plea April 4, 2023. No United States Code section, so legalproc:FederalCharge is not emitted.",
                    "rel_description": "Defendant pleaded guilty to production.",
                },
                {
                    "id": "kb:charge-distribution",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Distribution", "uco-core:UcoObject"],
                    "name": "Distribution of child pornography",
                    "description": "Guilty plea April 4, 2023. No United States Code section, so legalproc:FederalCharge is not emitted.",
                    "rel_description": "Defendant pleaded guilty to distribution.",
                },
            ],
            "plea": {
                "name": "Guilty plea",
                "plea_type": "guilty",
                "description": "Entered April 4, 2023.",
            },
            "sentences": [
                {
                    "id": "kb:sentence-prison",
                    "name": "Imposed custodial sentence",
                    "kind": "custodial",
                    "term": "600 months",
                },
                {
                    "id": "kb:sentence-supervised",
                    "name": "Imposed supervised release",
                    "kind": "supervised-release",
                    "term": "20 years",
                },
            ],
            "restitution": {
                "id": "kb:restitution",
                "name": "Restitution and assessments",
                "amount": "96200",
                "description": "Source states $91,000 restitution and $5,200 special assessments. Assessments are not typed as Sentence.",
            },
            "phase_begin": "2023-04-04T00:00:00Z",
            "phase_name": "Plea and sentencing",
            "provenance_name": "DOJ USAO MDNC press release",
        }
    )


def build_ncmec_2025_619() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/ncmec-2025-619/",
            "investigation_name": "WDNY Walsh Google CyberTip complaint",
            "source_file": "ncmec_2025_619-doj.txt",
            "source_url": (
                "https://www.justice.gov/usao-wdny/pr/rochester-man-charged-receipt-and-possession-child-pornography"
            ),
            "published": "2025-03-10T00:00:00Z",
            "defendant_name": "Daniel P. Walsh",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Western District of New York",
            "victim_status": "omitted",
            "cybertip_name": "NCMEC report from Google (November 2024)",
            "organizations": [
                {"id": "kb:fbi", "name": "FBI Child Exploitation Task Force"},
                {"id": "kb:rpd", "name": "Rochester Police Department"},
            ],
            "authorization_name": "Search warrant for the Rochester residence",
            "actions": [
                {
                    "id": "kb:action-receive-tip",
                    "name": "Receive Google-originated NCMEC report",
                    "performer": "kb:rpd",
                    "object": "kb:cybertip",
                    "description": (
                        "In November 2024 NCMEC received a report from Google that an "
                        "account registered in the defendant's name uploaded images "
                        "from his IP address. CAC SHACL allows one performer."
                    ),
                },
                {
                    "id": "kb:action-warrant",
                    "name": "Execute search warrant",
                    "performer": "kb:fbi",
                    "authorization": "kb:authorization",
                    "description": (
                        "Rochester Police and the FBI executed a search warrant and "
                        "seized computers and digital devices. Forensic examination "
                        "found hundreds of images. No hash is published."
                    ),
                },
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-rpd",
                    "source": "kb:fbi",
                    "target": "kb:rpd",
                    "description": "FBI investigated with Rochester Police Department.",
                }
            ],
            "charges": [
                {
                    "id": "kb:charge-receipt",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Possession", "uco-core:UcoObject"],
                    "name": "Receipt of child pornography",
                    "description": "Criminal complaint. No United States Code section, so legalproc:FederalCharge is not emitted. Presumed innocent.",
                    "rel_description": "Defendant is charged by complaint with receipt.",
                },
                {
                    "id": "kb:charge-possession",
                    "types": ["legal:CriminalCharge", "legal:CSAM_Possession", "uco-core:UcoObject"],
                    "name": "Possession of child pornography",
                    "description": "Criminal complaint. No United States Code section, so legalproc:FederalCharge is not emitted. Presumed innocent.",
                    "rel_description": "Defendant is charged by complaint with possession.",
                },
            ],
            "potential_penalties": [
                {
                    "id": "kb:potential-penalty",
                    "name": "Statutory maximum stated for the charges",
                    "kind": "statutory-maximum",
                    "description": "Maximum 20 years and $250,000 fine. Not an imposed sentence. Released on conditions; kind of release is not sourced.",
                    "related_charge": "kb:charge-receipt",
                }
            ],
            "phase_begin": "2025-03-10T00:00:00Z",
            "phase_name": "Complaint and initial appearance",
            "provenance_name": "DOJ USAO WDNY press release",
        }
    )


def build_ncmec_2023_324() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/ncmec-2023-324/",
            "investigation_name": "SDIL Villmer solicitation complaint",
            "source_file": "ncmec_2023_324-doj.txt",
            "source_url": (
                "https://www.justice.gov/usao-sdil/pr/first-grade-teacher-charged-solicitation-child-sexual-abuse-material"
            ),
            "published": "2023-08-21T00:00:00Z",
            "defendant_name": "Jonathan C. Villmer, Jr.",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Southern District of Illinois",
            "victim_status": "reported",
            "victim_count": 1,
            "organizations": [
                {"id": "kb:hsi", "name": "Homeland Security Investigations"},
                {"id": "kb:carmi-pd", "name": "Carmi Police Department"},
                {"id": "kb:new-baden-pd", "name": "New Baden Police Department"},
            ],
            "authorization_name": "Search warrants for Snapchat account and residence",
            "actions": [
                {
                    "id": "kb:action-warrant",
                    "name": "Execute residence search warrant and arrest",
                    "performer": "kb:hsi",
                    "authorization": "kb:authorization",
                    "description": (
                        "The case began in an otherwise unrelated Carmi PD CSAM "
                        "distribution investigation that led to a Snapchat account. "
                        "On August 18, 2023, law enforcement searched the New Baden "
                        "residence, seized two cell phones and other devices, and "
                        "arrested the defendant. The source does not assign a CyberTip. "
                        "CAC SHACL allows one performer."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-carmi",
                    "source": "kb:hsi",
                    "target": "kb:carmi-pd",
                    "description": "HSI investigated with Carmi Police Department.",
                },
                {
                    "id": "kb:rel-partner-nb",
                    "source": "kb:hsi",
                    "target": "kb:new-baden-pd",
                    "description": "HSI investigated with New Baden Police Department.",
                },
            ],
            "charges": [
                {
                    "id": "kb:charge-solicitation",
                    "types": ["legal:CriminalCharge", "legal:OnlineEnticement", "uco-core:UcoObject"],
                    "name": "Solicitation of child sexual abuse material",
                    "description": (
                        "Criminal complaint. The press release does not cite a United "
                        "States Code section, so legalproc:FederalCharge is not emitted. "
                        "Presumed innocent. Other purported minors are not counted."
                    ),
                    "rel_description": "Defendant is charged by complaint with solicitation of CSAM.",
                }
            ],
            "potential_penalties": [
                {
                    "id": "kb:potential-penalty",
                    "name": "Statutory maximum if convicted",
                    "kind": "statutory-maximum",
                    "description": "Up to 20 years. Not an imposed sentence.",
                    "related_charge": "kb:charge-solicitation",
                }
            ],
            "phase_begin": "2023-08-18T00:00:00Z",
            "phase_name": "Complaint and arrest",
            "provenance_name": "DOJ USAO SDIL press release",
        }
    )


def build_doj_ceos_2026_013() -> CASEGraph:
    return _build_from_record(
        {
            "kb_prefix": "http://example.org/kb/doj-ceos-2026-013/",
            "investigation_name": "EDWI Hounsell 2422(b) sentence",
            "source_file": "doj_ceos_2026_013-doj.txt",
            "source_url": (
                "https://www.justice.gov/opa/pr/wisconsin-man-sentenced-13-years-prison-using-internet-sexually-exploit-minor-philippines"
            ),
            "published": "2026-05-14T00:00:00Z",
            "defendant_name": "Bradley D. Hounsell",
            "jurisdiction_type": "legalproc:FederalJurisdiction",
            "jurisdiction_name": "United States, Eastern District of Wisconsin",
            "victim_status": "reported",
            "victim_count": 1,
            "organizations": [
                {"id": "kb:fbi", "name": "FBI Child Exploitation Operational Unit"},
                {"id": "kb:fbi-mke", "name": "FBI Milwaukee Field Office"},
                {"id": "kb:winnebago-so", "name": "Winnebago County Sheriff's Office"},
            ],
            "authorization_name": "Warrant-authorized search of the Wisconsin residence",
            "actions": [
                {
                    "id": "kb:action-warrant",
                    "name": "Warrant-authorized search of residence",
                    "performer": "kb:fbi",
                    "authorization": "kb:authorization",
                    "description": (
                        "Law enforcement recovered a video and other evidence from the "
                        "defendant's phone during a warrant-authorized search of his "
                        "home in Wisconsin. The source does not assign a CyberTip and "
                        "does not publish a hash. A PACER judgment elsewhere in this "
                        "repository is not used. CAC SHACL allows one performer."
                    ),
                }
            ],
            "relationships": [
                {
                    "id": "kb:rel-partner-mke",
                    "source": "kb:fbi",
                    "target": "kb:fbi-mke",
                    "description": "CEOU investigated with FBI Milwaukee.",
                },
                {
                    "id": "kb:rel-partner-winnebago",
                    "source": "kb:fbi",
                    "target": "kb:winnebago-so",
                    "description": "FBI investigated with Winnebago County Sheriff's Office.",
                },
            ],
            "charges": [
                {
                    "id": "kb:charge-enticement",
                    "types": ["legal:CriminalCharge", "legal:OnlineEnticement", "uco-core:UcoObject"],
                    "name": "Coerce and entice a minor",
                    "description": (
                        "Using the internet to coerce and entice a minor in the "
                        "Philippines. This press release does not cite 18 U.S.C. "
                        "§ 2422(b), so legalproc:FederalCharge is not emitted."
                    ),
                    "rel_description": "Defendant was sentenced on the enticement offense.",
                }
            ],
            "sentences": [
                {
                    "id": "kb:sentence-prison",
                    "name": "Imposed custodial sentence",
                    "kind": "custodial",
                    "term": "13 years",
                },
                {
                    "id": "kb:sentence-supervised",
                    "name": "Imposed supervised release",
                    "kind": "supervised-release",
                    "term": "7 years",
                },
            ],
            "phase_begin": "2026-05-14T00:00:00Z",
            "phase_name": "Sentencing",
            "provenance_name": "DOJ OPA press release 26-500",
        }
    )


BUILDERS = {
    "ncmec_2025_356": (build_ncmec_2025_356, HERE / "ncmec_2025_356.jsonld"),
    "illinois_ag_2025_001": (build_illinois_ag_2025_001, HERE / "illinois_ag_2025_001.jsonld"),
    "usss_2022_005": (build_usss_2022_005, HERE / "usss_2022_005.jsonld"),
    "illinois_ag_2025_023": (build_illinois_ag_2025_023, HERE / "illinois_ag_2025_023.jsonld"),
    "usss_2017_007": (build_usss_2017_007, HERE / "usss_2017_007.jsonld"),
    "ncmec_2024_754": (build_ncmec_2024_754, HERE / "ncmec_2024_754.jsonld"),
    "ncmec_2023_609": (build_ncmec_2023_609, HERE / "ncmec_2023_609.jsonld"),
    "ncmec_2025_619": (build_ncmec_2025_619, HERE / "ncmec_2025_619.jsonld"),
    "ncmec_2023_324": (build_ncmec_2023_324, HERE / "ncmec_2023_324.jsonld"),
    "doj_ceos_2026_013": (build_doj_ceos_2026_013, HERE / "doj_ceos_2026_013.jsonld"),
}


def main() -> None:
    names = sys.argv[1:] or list(BUILDERS)
    for name in names:
        builder, output = BUILDERS[name]
        graph = builder()
        graph.write(str(output))
        print(output)


if __name__ == "__main__":
    main()
