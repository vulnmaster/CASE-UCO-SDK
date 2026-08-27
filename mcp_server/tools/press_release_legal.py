"""Shared builders for press-release legal-outcome exemplars (#125)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation
from case_uco.uco.identity import Person
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject, URLFacet
from case_uco.uco.types import Hash

LEGALPROC_CONTEXT = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
}

SCENARIOS = (
    "state-arrest-charges",
    "federal-indictment",
    "state-plea-sentence",
    "federal-verdict-sentence",
    "federal-adoption",
    "parallel-prosecutions",
    "prior-conviction",
    "no-victim-details",
    "potential-vs-imposed",
    "lifecycle-releases",
)


def _lit(datatype: str, value: str) -> dict[str, str]:
    return {"@type": datatype, "@value": value}


def _new_graph() -> CASEGraph:
    return CASEGraph(
        kb_prefix="http://example.org/kb/",
        extra_context=LEGALPROC_CONTEXT,
    )


def _add_source(
    graph: CASEGraph,
    *,
    source_id: str,
    url: str,
    published: str,
    retrieved: str,
    ingested: datetime,
    hash_value: str | None = None,
) -> str:
    facets: list[Any] = [
        URLFacet(full_value=url),
        FileFacet(file_name="press-release.html"),
    ]
    if hash_value:
        facets.append(
            ContentDataFacet(
                hash=[Hash(hash_method="SHA256", hash_value=hash_value)],
            )
        )
    source = graph.create(
        ObservableObject,
        id=source_id,
        name="Public press release",
        has_facet=facets,
        object_created_time=ingested,
    )
    graph.add_property(source_id, "legalproc:sourcePublicationTime", _lit("xsd:dateTime", published))
    graph.add_property(source_id, "legalproc:sourceRetrievalTime", _lit("xsd:dateTime", retrieved))
    if hash_value is None:
        graph.add_property(
            source_id,
            "uco-core:description",
            "Source bytes were not available; source-bytes status is unavailable.",
        )
    return graph.get_id(source)


def _add_jurisdiction(graph: CASEGraph, node_id: str, kind: str, name: str) -> None:
    type_name = (
        "legalproc:FederalJurisdiction"
        if kind == "federal"
        else "legalproc:StateJurisdiction"
    )
    graph.upsert_node(
        node_id,
        types=type_name,
        properties={"uco-core:name": name},
    )


def _add_charge(
    graph: CASEGraph,
    node_id: str,
    *,
    jurisdiction: str,
    name: str,
    statute: str,
    disposition: str,
    scope: str,
    count: int = 1,
    asserted_in: str | None = None,
) -> None:
    charge_type = (
        "legalproc:FederalCharge"
        if jurisdiction == "federal"
        else "legalproc:StateCharge"
        if jurisdiction == "state"
        else "legalproc:CriminalCharge"
    )
    props: dict[str, Any] = {
        "uco-core:name": name,
        "legalproc:statuteCitation": statute,
        "legalproc:countNumber": _lit("xsd:nonNegativeInteger", str(count)),
        "legalproc:countLabel": f"Count {count}",
        "legalproc:chargeDisposition": disposition,
        "legalproc:jurisdictionKind": jurisdiction,
        "legalproc:outcomeScope": scope,
        "legalproc:offenseForm": "substantive",
    }
    if asserted_in:
        props["legalproc:assertedIn"] = {"@id": asserted_in}
    graph.upsert_node(node_id, types=charge_type, properties=props)


def _relate(graph: CASEGraph, source: str, target: str, description: str, key: str) -> None:
    graph.create_relationship(
        source,
        target,
        "Related_To",
        description=description,
        assertion_id=f"kb:rel-{key}",
    )


def _base(
    graph: CASEGraph,
    *,
    case_name: str,
    case_id: str,
    defendant_name: str,
    victim_status: str,
    victim_count: int | None = None,
) -> tuple[str, str]:
    investigation = graph.create(
        Investigation,
        id="kb:investigation",
        name=case_name,
    )
    graph.add_property("kb:investigation", "legalproc:caseIdentifier", case_id)
    graph.add_property("kb:investigation", "legalproc:victimFactStatus", victim_status)
    if victim_count is not None:
        graph.add_property(
            "kb:investigation",
            "legalproc:reportedVictimCount",
            _lit("xsd:nonNegativeInteger", str(victim_count)),
        )
    defendant = graph.create(Person, id="kb:defendant", name=defendant_name)
    return graph.get_id(investigation), graph.get_id(defendant)


def build_state_arrest_charges() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="State arrest and charges only",
        case_id="PR-STATE-ARREST-001",
        defendant_name="Defendant A",
        victim_status="omitted",
    )
    ingested = datetime(2026, 8, 1, 15, 0, tzinfo=timezone.utc)
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/state-arrest",
        published="2026-07-31T12:00:00Z",
        retrieved="2026-08-01T14:30:00Z",
        ingested=ingested,
    )
    _add_jurisdiction(graph, "kb:state-jurisdiction", "state", "Example State")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "State criminal complaint",
            "legalproc:instrumentType": "complaint",
        },
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="state",
        name="Sexual solicitation of a minor",
        statute="Example State Code § 1-100",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    graph.upsert_node(
        "kb:release-condition",
        types="legalproc:PretrialReleaseCondition",
        properties={
            "uco-core:name": "Held without bond",
            "legalproc:releaseConditionKind": "detained-without-bond",
        },
    )
    _relate(graph, defendant, "kb:charge-1", "Defendant charged in the current state matter.", "charged")
    _relate(graph, "kb:charge-1", "kb:state-jurisdiction", "Charge prosecuted under state jurisdiction.", "charge-jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    _relate(graph, defendant, "kb:release-condition", "Defendant held without bond; not an imposed sentence.", "bond")
    return graph


def build_federal_indictment() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="Federal indictment without disposition",
        case_id="1:26-cr-00001",
        defendant_name="Defendant B",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/federal-indictment",
        published="2026-06-15T16:00:00Z",
        retrieved="2026-06-16T09:00:00Z",
        ingested=datetime(2026, 6, 16, 10, 0, tzinfo=timezone.utc),
        hash_value="aaaabbbbccccddddeeeeffff0000111122223333444455556666777788889999",
    )
    _add_jurisdiction(graph, "kb:federal-jurisdiction", "federal", "United States")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "Indictment",
            "legalproc:instrumentType": "indictment",
        },
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="federal",
        name="Count 1: Distribution of child pornography",
        statute="18 U.S.C. § 2252A(a)(2)",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    _relate(graph, defendant, "kb:charge-1", "Defendant charged in the current federal matter.", "charged")
    _relate(graph, "kb:charge-1", "kb:federal-jurisdiction", "Charge prosecuted under federal jurisdiction.", "charge-jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_state_plea_sentence() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="State guilty plea and sentencing",
        case_id="PR-STATE-PLEA-001",
        defendant_name="Defendant C",
        victim_status="reported",
        victim_count=1,
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/state-plea",
        published="2026-05-01T18:00:00Z",
        retrieved="2026-05-02T11:00:00Z",
        ingested=datetime(2026, 5, 2, 12, 0, tzinfo=timezone.utc),
        hash_value="1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff",
    )
    _add_jurisdiction(graph, "kb:state-jurisdiction", "state", "Example State")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "Criminal information",
            "legalproc:instrumentType": "information",
        },
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="state",
        name="Count 1: Possession of CSAM",
        statute="Example State Code § 2-200",
        disposition="convicted-by-plea",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    graph.upsert_node(
        "kb:plea",
        types="legalproc:Plea",
        properties={
            "uco-core:name": "Guilty plea",
            "legalproc:pleaType": "guilty",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    graph.upsert_node(
        "kb:plea-agreement",
        types="legalproc:PleaAgreement",
        properties={
            "uco-core:name": "Rule 11(c) style state plea agreement",
            "legalproc:outcomeScope": "current-case",
            "legalproc:recordsPlea": {"@id": "kb:plea"},
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    graph.upsert_node(
        "kb:sentence",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Five years imprisonment imposed",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "5 years",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    _relate(graph, defendant, "kb:charge-1", "Defendant charged in the current state matter.", "charged")
    _relate(graph, "kb:charge-1", "kb:state-jurisdiction", "Charge prosecuted under state jurisdiction.", "charge-jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_federal_verdict_sentence() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="Federal guilty verdict and sentencing",
        case_id="1:25-cr-00099",
        defendant_name="Defendant D",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/federal-verdict",
        published="2026-04-10T17:00:00Z",
        retrieved="2026-04-11T08:00:00Z",
        ingested=datetime(2026, 4, 11, 9, 0, tzinfo=timezone.utc),
        hash_value="abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
    )
    _add_jurisdiction(graph, "kb:federal-jurisdiction", "federal", "United States")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "Indictment",
            "legalproc:instrumentType": "indictment",
        },
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="federal",
        name="Count 1: Production of child pornography",
        statute="18 U.S.C. § 2251(a)",
        disposition="convicted-by-verdict",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    graph.upsert_node(
        "kb:verdict",
        types="legalproc:Verdict",
        properties={
            "uco-core:name": "Jury verdict of guilty",
            "legalproc:verdictType": "guilty",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    graph.upsert_node(
        "kb:sentence",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Thirty years imprisonment imposed",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "30 years",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    _relate(graph, defendant, "kb:charge-1", "Defendant charged in the current federal matter.", "charged")
    _relate(graph, "kb:charge-1", "kb:federal-jurisdiction", "Charge prosecuted under federal jurisdiction.", "charge-jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_federal_adoption() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="State arrest followed by federal adoption",
        case_id="MATTER-ADOPT-001",
        defendant_name="Defendant E",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/federal-adoption",
        published="2026-03-20T15:00:00Z",
        retrieved="2026-03-21T10:00:00Z",
        ingested=datetime(2026, 3, 21, 11, 0, tzinfo=timezone.utc),
        hash_value="eeeeffffaaaabbbbccccdddd0000111122223333444455556666777788889999",
    )
    _add_jurisdiction(graph, "kb:state-jurisdiction", "state", "Example State")
    _add_jurisdiction(graph, "kb:federal-jurisdiction", "federal", "United States")
    graph.upsert_node(
        "kb:state-proceeding",
        types="legalproc:CriminalProceeding",
        properties={
            "uco-core:name": "State arrest and charging",
            "legalproc:proceedingType": "preliminary-hearing",
        },
    )
    graph.upsert_node(
        "kb:federal-proceeding",
        types="legalproc:CriminalProceeding",
        properties={
            "uco-core:name": "Federal adoption and indictment",
            "legalproc:proceedingType": "arraignment",
        },
    )
    graph.upsert_node(
        "kb:state-instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "State complaint",
            "legalproc:instrumentType": "complaint",
        },
    )
    graph.upsert_node(
        "kb:federal-instrument",
        types="legalproc:ChargingInstrument",
        properties={
            "uco-core:name": "Federal indictment after adoption",
            "legalproc:instrumentType": "indictment",
        },
    )
    _add_charge(
        graph,
        "kb:state-charge",
        jurisdiction="state",
        name="State CSAM possession",
        statute="Example State Code § 2-200",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:state-instrument",
    )
    _add_charge(
        graph,
        "kb:federal-charge",
        jurisdiction="federal",
        name="Count 1: Receipt of child pornography",
        statute="18 U.S.C. § 2252A(a)(2)",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:federal-instrument",
    )
    _relate(graph, defendant, "kb:state-charge", "Defendant first charged in state court.", "state-charged")
    _relate(graph, defendant, "kb:federal-charge", "Defendant later charged after federal adoption.", "fed-charged")
    _relate(graph, "kb:state-charge", "kb:state-jurisdiction", "State charge under state jurisdiction.", "state-jur")
    _relate(graph, "kb:federal-charge", "kb:federal-jurisdiction", "Federal charge under federal jurisdiction.", "fed-jur")
    _relate(
        graph,
        "kb:federal-proceeding",
        "kb:state-proceeding",
        "Federal proceeding adopted the matter after the state arrest.",
        "adoption",
    )
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_parallel_prosecutions() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="Parallel state and federal prosecutions",
        case_id="MATTER-PARALLEL-001",
        defendant_name="Defendant F",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/parallel",
        published="2026-02-01T14:00:00Z",
        retrieved="2026-02-02T09:00:00Z",
        ingested=datetime(2026, 2, 2, 10, 0, tzinfo=timezone.utc),
        hash_value="9999888877776666555544443333222211110000ffffeeeeddddccccbbbbaaaa",
    )
    _add_jurisdiction(graph, "kb:state-jurisdiction", "state", "Example State")
    _add_jurisdiction(graph, "kb:federal-jurisdiction", "federal", "United States")
    graph.upsert_node(
        "kb:state-proceeding",
        types="legalproc:CriminalProceeding",
        properties={
            "uco-core:name": "State prosecution",
            "legalproc:proceedingType": "trial",
        },
    )
    graph.upsert_node(
        "kb:federal-proceeding",
        types="legalproc:CriminalProceeding",
        properties={
            "uco-core:name": "Federal prosecution",
            "legalproc:proceedingType": "trial",
        },
    )
    graph.upsert_node(
        "kb:state-instrument",
        types="legalproc:ChargingInstrument",
        properties={"uco-core:name": "State indictment", "legalproc:instrumentType": "indictment"},
    )
    graph.upsert_node(
        "kb:federal-instrument",
        types="legalproc:ChargingInstrument",
        properties={"uco-core:name": "Federal indictment", "legalproc:instrumentType": "indictment"},
    )
    _add_charge(
        graph,
        "kb:state-charge",
        jurisdiction="state",
        name="State trafficking charge",
        statute="Example State Code § 3-300",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:state-instrument",
    )
    _add_charge(
        graph,
        "kb:federal-charge",
        jurisdiction="federal",
        name="Count 1: Sex trafficking of a minor",
        statute="18 U.S.C. § 1591",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:federal-instrument",
    )
    _relate(graph, defendant, "kb:state-charge", "Defendant charged in the parallel state case.", "state-charged")
    _relate(graph, defendant, "kb:federal-charge", "Defendant charged in the parallel federal case.", "fed-charged")
    _relate(graph, "kb:state-charge", "kb:state-jurisdiction", "State charge under state jurisdiction.", "state-jur")
    _relate(graph, "kb:federal-charge", "kb:federal-jurisdiction", "Federal charge under federal jurisdiction.", "fed-jur")
    _relate(
        graph,
        "kb:state-proceeding",
        "kb:federal-proceeding",
        "State and federal prosecutions proceed in parallel on one matter.",
        "parallel",
    )
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_prior_conviction() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="Current arrest mentioning a prior conviction",
        case_id="PR-PRIOR-001",
        defendant_name="Defendant G",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/prior-history",
        published="2026-01-15T13:00:00Z",
        retrieved="2026-01-16T09:00:00Z",
        ingested=datetime(2026, 1, 16, 10, 0, tzinfo=timezone.utc),
        hash_value="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    )
    _add_jurisdiction(graph, "kb:state-jurisdiction", "state", "Example State")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={"uco-core:name": "Current state complaint", "legalproc:instrumentType": "complaint"},
    )
    _add_charge(
        graph,
        "kb:current-charge",
        jurisdiction="state",
        name="Current solicitation charge",
        statute="Example State Code § 1-100",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    _add_charge(
        graph,
        "kb:prior-charge",
        jurisdiction="state",
        name="Prior conviction mentioned in the current arrest release",
        statute="Example State Code § 2-200",
        disposition="convicted-by-plea",
        scope="prior-history",
    )
    graph.upsert_node(
        "kb:prior-sentence",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Prior two-year sentence mentioned by the source",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "2 years",
            "legalproc:outcomeScope": "prior-history",
            "legalproc:concernsCharge": {"@id": "kb:prior-charge"},
        },
    )
    _relate(graph, defendant, "kb:current-charge", "Defendant charged in the current matter.", "current-charged")
    _relate(graph, defendant, "kb:prior-charge", "Source mentions a prior conviction of this defendant.", "prior-charged")
    _relate(graph, "kb:current-charge", "kb:state-jurisdiction", "Current charge under state jurisdiction.", "jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_no_victim_details() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="Press release with no victim details",
        case_id="PR-NO-VICTIM-001",
        defendant_name="Defendant H",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/no-victim-details",
        published="2026-01-05T12:00:00Z",
        retrieved="2026-01-05T18:00:00Z",
        ingested=datetime(2026, 1, 5, 19, 0, tzinfo=timezone.utc),
    )
    _add_jurisdiction(graph, "kb:state-jurisdiction", "state", "Example State")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={"uco-core:name": "State complaint", "legalproc:instrumentType": "complaint"},
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="state",
        name="Online solicitation charge; victim not identified in the source",
        statute="Example State Code § 1-100",
        disposition="pending",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    _relate(graph, defendant, "kb:charge-1", "Defendant charged in the current state matter.", "charged")
    _relate(graph, "kb:charge-1", "kb:state-jurisdiction", "Charge prosecuted under state jurisdiction.", "jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_potential_vs_imposed() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="Potential penalty versus imposed sentence",
        case_id="1:24-cr-00010",
        defendant_name="Defendant I",
        victim_status="omitted",
    )
    source = _add_source(
        graph,
        source_id="kb:source-release",
        url="https://example.org/press/potential-vs-imposed",
        published="2026-07-01T15:00:00Z",
        retrieved="2026-07-02T09:00:00Z",
        ingested=datetime(2026, 7, 2, 10, 0, tzinfo=timezone.utc),
        hash_value="fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210",
    )
    _add_jurisdiction(graph, "kb:federal-jurisdiction", "federal", "United States")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={"uco-core:name": "Indictment", "legalproc:instrumentType": "indictment"},
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="federal",
        name="Count 1: Murder for hire",
        statute="18 U.S.C. § 1958",
        disposition="convicted-by-verdict",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    graph.upsert_node(
        "kb:potential",
        types="legalproc:PotentialPenalty",
        properties={
            "uco-core:name": "Statutory maximum of 10 years",
            "uco-core:description": "10 years",
            "legalproc:potentialPenaltyKind": "statutory-maximum",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    graph.upsert_node(
        "kb:sentence",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Ten years imprisonment imposed",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "10 years",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    _relate(graph, defendant, "kb:charge-1", "Defendant charged in the current federal matter.", "charged")
    _relate(graph, "kb:charge-1", "kb:federal-jurisdiction", "Charge prosecuted under federal jurisdiction.", "jur")
    _relate(graph, inv, source, "Investigation characterized from this public release.", "inv-source")
    return graph


def build_lifecycle_releases() -> CASEGraph:
    graph = _new_graph()
    inv, defendant = _base(
        graph,
        case_name="One matter across two public releases",
        case_id="2:26-cr-00007",
        defendant_name="Defendant J",
        victim_status="omitted",
    )
    arrest_source = _add_source(
        graph,
        source_id="kb:source-arrest",
        url="https://example.org/press/lifecycle-arrest",
        published="2026-01-10T12:00:00Z",
        retrieved="2026-01-10T18:00:00Z",
        ingested=datetime(2026, 1, 10, 19, 0, tzinfo=timezone.utc),
        hash_value="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    sentence_source = _add_source(
        graph,
        source_id="kb:source-sentence",
        url="https://example.org/press/lifecycle-sentence",
        published="2026-08-01T12:00:00Z",
        retrieved="2026-08-01T16:00:00Z",
        ingested=datetime(2026, 8, 1, 17, 0, tzinfo=timezone.utc),
        hash_value="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    _add_jurisdiction(graph, "kb:federal-jurisdiction", "federal", "United States")
    graph.upsert_node(
        "kb:instrument",
        types="legalproc:ChargingInstrument",
        properties={"uco-core:name": "Indictment", "legalproc:instrumentType": "indictment"},
    )
    _add_charge(
        graph,
        "kb:charge-1",
        jurisdiction="federal",
        name="Count 1: Enticement",
        statute="18 U.S.C. § 2422(b)",
        disposition="convicted-by-plea",
        scope="current-case",
        asserted_in="kb:instrument",
    )
    graph.upsert_node(
        "kb:plea",
        types="legalproc:Plea",
        properties={
            "uco-core:name": "Guilty plea reported in the later release",
            "legalproc:pleaType": "guilty",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    graph.upsert_node(
        "kb:plea-agreement",
        types="legalproc:PleaAgreement",
        properties={
            "uco-core:name": "Plea agreement reported in the later release",
            "legalproc:outcomeScope": "current-case",
            "legalproc:recordsPlea": {"@id": "kb:plea"},
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    graph.upsert_node(
        "kb:sentence",
        types="legalproc:Sentence",
        properties={
            "uco-core:name": "Fifteen years imprisonment imposed",
            "legalproc:sentenceStatus": "imposed",
            "legalproc:sentenceKind": "custodial",
            "legalproc:sentenceTerm": "15 years",
            "legalproc:outcomeScope": "current-case",
            "legalproc:concernsCharge": {"@id": "kb:charge-1"},
        },
    )
    _relate(graph, defendant, "kb:charge-1", "Stable defendant-to-charge link across both releases.", "charged")
    _relate(graph, "kb:charge-1", "kb:federal-jurisdiction", "Charge prosecuted under federal jurisdiction.", "jur")
    _relate(graph, inv, arrest_source, "Arrest-stage source for the same court matter.", "arrest-source")
    _relate(graph, inv, sentence_source, "Sentencing-stage source for the same court matter.", "sentence-source")
    return graph


BUILDERS = {
    "state-arrest-charges": build_state_arrest_charges,
    "federal-indictment": build_federal_indictment,
    "state-plea-sentence": build_state_plea_sentence,
    "federal-verdict-sentence": build_federal_verdict_sentence,
    "federal-adoption": build_federal_adoption,
    "parallel-prosecutions": build_parallel_prosecutions,
    "prior-conviction": build_prior_conviction,
    "no-victim-details": build_no_victim_details,
    "potential-vs-imposed": build_potential_vs_imposed,
    "lifecycle-releases": build_lifecycle_releases,
}


def build(scenario: str) -> CASEGraph:
    try:
        builder = BUILDERS[scenario]
    except KeyError as exc:
        raise ValueError(f"unknown_press_release_scenario:{scenario}") from exc
    return builder()


def build_and_write(scenario: str, output: Path) -> Path:
    graph = build(scenario)
    graph.write(str(output))
    return output
