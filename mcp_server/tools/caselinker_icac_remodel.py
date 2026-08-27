"""CaseLinker ICAC remodel factories for issues #128–#132."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from case_uco import CASEGraph, TypedLiteral
from case_uco.case.investigation import Authorization, Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.core import ExternalReference, UcoObject
from case_uco.uco.identity import Organization, Person
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

CASELINKER_VOCAB = "https://caselinker.up.railway.app/resource/vocab/"

CASELINKER_PREDICATE_MAP = {
    # Thematic cluster tokens (child_exploitation, …), not statute citations.
    f"{CASELINKER_VOCAB}chargeCluster": None,
    f"{CASELINKER_VOCAB}chargeOffenseEvent": "legalproc:concernsCharge",
    f"{CASELINKER_VOCAB}attributedToOffenderRole": "uco-action:performer",
    f"{CASELINKER_VOCAB}evidenceTier": None,
    f"{CASELINKER_VOCAB}admissionTheme": None,
    f"{CASELINKER_VOCAB}admissionContext": None,
    f"{CASELINKER_VOCAB}quoteType": None,
    f"{CASELINKER_VOCAB}admissionFrame": None,
}

CONTEXT = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
    "cac": "https://cacontology.projectvic.org#",
    "ncmec": "https://cacontology.projectvic.org/us/ncmec#",
    "taskforce": "https://cacontology.projectvic.org/taskforce#",
    "tactical": "https://cacontology.projectvic.org/tactical#",
    "detection": "https://cacontology.projectvic.org/detection#",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
}

SCENARIOS = (
    "cybertip-join",
    "share-safe-cvip",
    "legalproc-dual-type",
    "commander-clocks",
    "discovery-disclosure",
)


class CaselinkerVocabError(ValueError):
    """Raised when a remodeled graph would keep undeclared CaseLinker vocab."""


def _lit(datatype: str, value: str) -> dict[str, str]:
    return {"@type": datatype, "@value": value}


def _new_graph() -> CASEGraph:
    return CASEGraph(kb_prefix="http://example.org/kb/", extra_context=CONTEXT)


def map_caselinker_predicate(iri: str) -> str | None:
    """Return the declared replacement, or None when the predicate must be dropped."""
    if iri in CASELINKER_PREDICATE_MAP:
        return CASELINKER_PREDICATE_MAP[iri]
    if iri.startswith(CASELINKER_VOCAB):
        raise CaselinkerVocabError(
            f"Undeclared CaseLinker predicate has no mapping: {iri}"
        )
    return iri


def refuse_caselinker_vocab(predicates: list[str]) -> None:
    undeclared = [p for p in predicates if str(p).startswith(CASELINKER_VOCAB)]
    if undeclared:
        raise CaselinkerVocabError(
            "Remodeled graphs must not emit caselinker:/resource/vocab/* predicates: "
            + ", ".join(undeclared)
        )


def join_cybertip_investigation(
    graph: CASEGraph,
    *,
    tip_id: str,
    investigation_id: str,
    trigger_id: str,
    incident_type_id: str | None = None,
) -> None:
    graph.upsert_node(
        trigger_id,
        types=["uco-core:UcoObject", "ncmec:InvestigationTrigger"],
        properties={
            "uco-core:name": "CyberTip triggered the investigation",
            "ncmec:triggeredBy": {"@id": tip_id},
            "ncmec:resultedInInvestigation": {"@id": investigation_id},
        },
    )
    if incident_type_id:
        graph.add_property(tip_id, "ncmec:hasNCMECIncidentType", {"@id": incident_type_id})


def build_share_safe_series_match(
    graph: CASEGraph,
    *,
    file_id: str,
    file_name: str,
    sha256: str,
    series_id: str,
    photodna_present: bool,
) -> ObservableObject:
    if not sha256:
        raise ValueError("Share-safe series match requires a sourced cryptographic hash.")
    facets = [
        FileFacet(file_name=file_name),
        ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value=sha256)]),
    ]
    file_obj = graph.create(
        ObservableObject,
        id=file_id,
        name=file_name,
        has_facet=facets,
        external_reference=[
            ExternalReference(
                reference_url=TypedLiteral(
                    f"https://example.org/ncmec/series/{series_id}",
                    "http://www.w3.org/2001/XMLSchema#anyURI",
                ),
                defining_context="NCMEC known-series identifier; PhotoDNA value withheld",
            )
        ],
    )
    if photodna_present:
        graph.add_property(
            file_id,
            "uco-core:tag",
            "photodna-match-reported-value-withheld",
        )
    return file_obj


def set_phase_clock(
    graph: CASEGraph,
    *,
    phase_id: str,
    phase_type: str,
    begin: str,
    end: str | None,
    name: str,
) -> None:
    props: dict[str, Any] = {
        "uco-core:name": name,
        "cac:hasPhaseBeginPoint": _lit("xsd:dateTimeStamp", begin),
    }
    if end:
        props["cac:hasPhaseEndPoint"] = _lit("xsd:dateTimeStamp", end)
    graph.upsert_node(phase_id, types=phase_type, properties=props)


def participating_agency(
    graph: CASEGraph,
    *,
    task_force_id: str,
    agency_id: str,
    action_id: str,
    description: str,
) -> None:
    graph.create_relationship(
        task_force_id,
        agency_id,
        "Related_To",
        description="Task force partners with the participating agency.",
        assertion_id=f"kb:rel-partner-{agency_id.split('/')[-1]}",
    )
    graph.add_property(
        action_id,
        "uco-core:description",
        description,
    )


def build_and_write(scenario: str, output: Path) -> Path:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    builder = {
        "cybertip-join": _build_cybertip_join,
        "share-safe-cvip": _build_share_safe_cvip,
        "legalproc-dual-type": _build_legalproc_dual_type,
        "commander-clocks": _build_commander_clocks,
        "discovery-disclosure": _build_discovery_disclosure,
    }[scenario]
    graph = builder()
    output.parent.mkdir(parents=True, exist_ok=True)
    graph.write(str(output))
    return output


def _build_cybertip_join() -> CASEGraph:
    graph = _new_graph()
    ingested = datetime(2025, 6, 1, 12, 0, tzinfo=timezone.utc)
    inv = graph.create(
        Investigation,
        id="kb:investigation",
        name="ICAC CyberTip investigation",
        object_created_time=ingested,
    )
    graph.add_type("kb:investigation", "cac:CACInvestigation")
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "CT-2025-00001")

    graph.upsert_node(
        "kb:incident-type",
        types=["uco-core:UcoObject", "ncmec:OnlineEnticementIncident"],
        properties={"uco-core:name": "Online enticement (sourced CyberTip category)"},
    )
    graph.create(
        ObservableObject,
        id="kb:cybertip",
        name="NCMEC CyberTipline Report CT-2025-00001",
        object_created_time=ingested,
    )
    graph.add_type("kb:cybertip", "ncmec:NCMECCybertipReport")
    join_cybertip_investigation(
        graph,
        tip_id="kb:cybertip",
        investigation_id="kb:investigation",
        trigger_id="kb:trigger",
        incident_type_id="kb:incident-type",
    )

    tool = graph.create(Tool, id="kb:tool-cybertipline", name="NCMEC CyberTipline", version="public")
    receive = graph.create(
        InvestigativeAction,
        id="kb:action-receive-tip",
        name="Receive and triage CyberTip",
        start_time=datetime(2025, 4, 12, 15, 0, tzinfo=timezone.utc),
        instrument=[tool],
        object_created_time=ingested,
    )
    graph.add_property("kb:action-receive-tip", "uco-action:object", {"@id": "kb:cybertip"})
    graph.add_property("kb:investigation", "cac:hasStep", {"@id": "kb:action-receive-tip"})

    warrant = graph.create(
        Authorization,
        id="kb:authorization",
        name="Search warrant for the reported residence",
        object_created_time=ingested,
    )
    execute = graph.create(
        InvestigativeAction,
        id="kb:action-warrant",
        name="Execute search warrant",
        start_time=datetime(2025, 5, 2, 10, 0, tzinfo=timezone.utc),
        object_created_time=ingested,
    )
    graph.add_property(
        "kb:action-warrant",
        "case-investigation:relevantAuthorization",
        {"@id": "kb:authorization"},
    )
    graph.add_property("kb:investigation", "cac:hasStep", {"@id": "kb:action-warrant"})
    _ = (inv, receive, warrant, execute)
    return graph


def _build_share_safe_cvip() -> CASEGraph:
    graph = _new_graph()
    ingested = datetime(2025, 6, 1, 12, 0, tzinfo=timezone.utc)
    graph.create(
        Investigation,
        id="kb:investigation",
        name="Known-series correlation (share-safe)",
        object_created_time=ingested,
    )
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "LAB-2025-004")
    sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    file_obj = build_share_safe_series_match(
        graph,
        file_id="kb:file-1",
        file_name="exhibit-1.bin",
        sha256=sha256,
        series_id="SERIES-DEMO-001",
        photodna_present=True,
    )
    tool = graph.create(Tool, id="kb:tool-hashset", name="Laboratory hash-set matcher", version="1.0")
    action = graph.create(
        InvestigativeAction,
        id="kb:action-series",
        name="Known-series correlation",
        start_time=datetime(2025, 5, 20, 14, 0, tzinfo=timezone.utc),
        instrument=[tool],
        object_created_time=ingested,
    )
    graph.add_property("kb:action-series", "uco-action:object", {"@id": "kb:file-1"})
    graph.create(
        ProvenanceRecord,
        id="kb:prov-series",
        name="Share-safe series exhibit",
        object_created_time=ingested,
        exhibit_number="1",
        object=[file_obj],
    )
    _ = action
    return graph


def _build_legalproc_dual_type() -> CASEGraph:
    graph = _new_graph()
    ingested = datetime(2025, 6, 1, 12, 0, tzinfo=timezone.utc)
    graph.create(
        Investigation,
        id="kb:investigation",
        name="Federal ICAC adoption",
        object_created_time=ingested,
    )
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "1:25-cr-00010")
    person = graph.create(Person, id="kb:defendant", name="Defendant One")
    graph.upsert_node(
        "kb:jurisdiction",
        types="legalproc:FederalJurisdiction",
        properties={"uco-core:name": "United States"},
    )
    graph.upsert_node(
        "kb:charge",
        types=["legalproc:FederalCharge"],
        properties={
            "uco-core:name": "Possession of child pornography",
            "legalproc:statuteCitation": "18 U.S.C. § 2252A(a)(5)(B)",
            "legalproc:countNumber": _lit("xsd:nonNegativeInteger", "1"),
            "legalproc:countLabel": "Count 1",
            "legalproc:chargeDisposition": "pending",
            "legalproc:jurisdictionKind": "federal",
            "legalproc:outcomeScope": "current-case",
        },
    )
    graph.create_relationship(
        "kb:defendant",
        "kb:charge",
        "Related_To",
        description="Defendant is charged with Count 1.",
        assertion_id="kb:rel-charged-with",
    )
    graph.add_property("kb:defendant", "legalproc:chargedWith", {"@id": "kb:charge"})
    graph.upsert_node(
        "kb:plea",
        types="legalproc:Plea",
        properties={
            "uco-core:name": "Guilty plea",
            "legalproc:pleaType": "guilty",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge"},
        },
    )
    graph.upsert_node(
        "kb:plea-agreement",
        types="legalproc:PleaAgreement",
        properties={
            "uco-core:name": "Rule 11(c) plea agreement",
            "legalproc:outcomeScope": "current-case",
            "legalproc:recordsPlea": {"@id": "kb:plea"},
            "legalproc:concernsCharge": {"@id": "kb:charge"},
        },
    )
    graph.upsert_node(
        "kb:sentence",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Imposed custodial sentence",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "120 months",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge"},
        },
    )
    graph.add_property("kb:sentence", "legalproc:appliesTo", {"@id": "kb:charge"})
    refuse_caselinker_vocab([])
    _ = person
    return graph


def _build_commander_clocks() -> CASEGraph:
    graph = _new_graph()
    ingested = datetime(2025, 6, 1, 12, 0, tzinfo=timezone.utc)
    graph.create(
        Investigation,
        id="kb:investigation",
        name="State ICAC warrant arrest",
        object_created_time=ingested,
    )
    graph.add_type("kb:investigation", "cac:CACInvestigation")
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "ICAC-2025-088")
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", "reported")
    graph.add_property(
        "kb:investigation",
        "legalproc:reportedVictimCount",
        _lit("xsd:nonNegativeInteger", "2"),
    )

    set_phase_clock(
        graph,
        phase_id="kb:phase-initial",
        phase_type="cac:InitialPhase",
        begin="2025-01-15T00:00:00Z",
        end="2025-03-01T00:00:00Z",
        name="Initial investigation",
    )
    set_phase_clock(
        graph,
        phase_id="kb:phase-legal",
        phase_type="cac:LegalProcessPhase",
        begin="2025-03-01T00:00:00Z",
        end="2025-03-20T00:00:00Z",
        name="Warrant and arrest",
    )
    graph.add_property("kb:investigation", "cac:hasPhase", {"@id": "kb:phase-initial"})
    graph.add_property("kb:investigation", "cac:hasPhase", {"@id": "kb:phase-legal"})

    graph.create(Organization, id="kb:tf", name="State ICAC Task Force")
    graph.add_type("kb:tf", "taskforce:ICACtaskForce")
    graph.create(Organization, id="kb:ccu", name="State Computer Crimes Unit")
    action = graph.create(
        InvestigativeAction,
        id="kb:action-warrant",
        name="Execute search warrant",
        start_time=datetime(2025, 3, 2, 9, 0, tzinfo=timezone.utc),
        object_created_time=ingested,
    )
    participating_agency(
        graph,
        task_force_id="kb:tf",
        agency_id="kb:ccu",
        action_id="kb:action-warrant",
        description="ICAC task force and Computer Crimes Unit jointly executed the warrant. CAC SHACL allows one performer; partner is recorded on the task force.",
    )
    graph.add_property("kb:action-warrant", "uco-action:performer", {"@id": "kb:ccu"})
    graph.create(
        Authorization,
        id="kb:authorization",
        name="Residence search warrant",
        object_created_time=ingested,
    )
    graph.add_property(
        "kb:action-warrant",
        "case-investigation:relevantAuthorization",
        {"@id": "kb:authorization"},
    )
    graph.upsert_node(
        "kb:arrest",
        types=["tactical:ArrestOperation", "uco-core:UcoObject"],
        properties={
            "uco-core:name": "Warrant arrest without incident",
            "tactical:arrestType": "warrant_arrest",
            "tactical:targetCount": _lit("xsd:nonNegativeInteger", "1"),
            "tactical:resistanceExpected": _lit("xsd:boolean", "false"),
            "tactical:weaponsExpected": _lit("xsd:boolean", "false"),
        },
    )
    graph.create(Person, id="kb:victim-1", name="Minor Victim 1")
    graph.create(Person, id="kb:victim-2", name="Minor Victim 2")
    graph.upsert_node(
        "kb:victim-role-1",
        types=["uco-core:UcoObject", "cac:VictimRole"],
        properties={
            "uco-core:name": "Minor Victim 1",
            "cac:hasRoleBeginPoint": _lit("xsd:dateTimeStamp", "2025-01-15T00:00:00Z"),
        },
    )
    graph.upsert_node(
        "kb:victim-role-2",
        types=["uco-core:UcoObject", "cac:VictimRole"],
        properties={
            "uco-core:name": "Minor Victim 2",
            "cac:hasRoleBeginPoint": _lit("xsd:dateTimeStamp", "2025-01-15T00:00:00Z"),
        },
    )
    _ = action
    return graph


def _build_discovery_disclosure() -> CASEGraph:
    graph = _new_graph()
    ingested = datetime(2025, 6, 1, 12, 0, tzinfo=timezone.utc)
    graph.create(
        Investigation,
        id="kb:investigation",
        name="Federal prosecution with sourced Jencks disclosure",
        object_created_time=ingested,
    )
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", "1:25-cr-00010")
    graph.upsert_node(
        "kb:charge",
        types="legalproc:FederalCharge",
        properties={
            "uco-core:name": "Count 1",
            "legalproc:statuteCitation": "18 U.S.C. § 2252A(a)(5)(B)",
            "legalproc:countNumber": _lit("xsd:nonNegativeInteger", "1"),
            "legalproc:chargeDisposition": "pending",
            "legalproc:jurisdictionKind": "federal",
            "legalproc:outcomeScope": "current-case",
        },
    )
    memo = graph.create(
        UcoObject,
        id="kb:interview-memo",
        name="Interview memorandum of Agent A",
        object_created_time=ingested,
    )
    graph.upsert_node(
        "kb:obligation",
        types="legalproc:DisclosureObligation",
        properties={
            "uco-core:name": "Jencks obligation for Agent A",
            "legalproc:disclosureKind": "jencks",
            "legalproc:disclosureStatus": "disclosed",
            "legalproc:disclosureSourceCitation": "Discovery certificate, Doc 40",
            "legalproc:concernsEvidence": {"@id": "kb:interview-memo"},
            "legalproc:concernsCharge": {"@id": "kb:charge"},
        },
    )
    graph.upsert_node(
        "kb:production",
        types="legalproc:DiscoveryProduction",
        properties={
            "uco-core:name": "Production of Agent A memorandum",
            "legalproc:disclosureSourceCitation": "Discovery certificate, Doc 40",
            "legalproc:satisfiesObligation": {"@id": "kb:obligation"},
            "legalproc:concernsEvidence": {"@id": "kb:interview-memo"},
        },
    )
    _ = memo
    return graph
