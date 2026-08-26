#!/usr/bin/env python3
"""FOAF/ORG identity and roles exemplar for docs/recipes/foaf-org-identity-roles.md."""

from __future__ import annotations

from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation
from case_uco.uco.core import Relationship
from case_uco.uco.identity import Organization, Person, SimpleNameFacet
from case_uco.uco.observable import AccountFacet, ObservableObject

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "foaf-org-identity.jsonld"

EXTRA_CONTEXT = {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "org": "http://www.w3.org/ns/org#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "time": "http://www.w3.org/2006/time#",
    "prov": "http://www.w3.org/ns/prov#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)

    role_id = "kb:role-dfe"
    graph.upsert_node(
        role_id,
        types=["org:Role", "skos:Concept"],
        properties={
            "skos:prefLabel": "Digital forensic examiner",
            "uco-core:description": ["ORG role node — org:role must reference this IRI, not a string."],
        },
    )

    person_id = "kb:person-1"
    person = graph.create(
        Person,
        id=person_id,
        name="Alex Morgan (synthetic)",
        has_facet=[SimpleNameFacet(given_name=["Alex"], family_name=["Morgan"])],
    )
    graph.add_type(person_id, "foaf:Person")
    graph.add_property(person_id, "foaf:mbox", "mailto:alex.morgan@example.org")
    graph.add_type(person_id, "prov:Agent")

    person2_id = "kb:person-2"
    person2 = graph.create(
        Person,
        id=person2_id,
        name="Jordan Lee (synthetic)",
        has_facet=[SimpleNameFacet(given_name=["Jordan"], family_name=["Lee"])],
    )
    graph.add_type(person2_id, "foaf:Person")
    graph.add_type(person2_id, "prov:Agent")

    org_id = "kb:org-taskforce"
    org = graph.create(Organization, id=org_id, name="Regional ICAC Task Force (synthetic)")
    graph.add_type(org_id, "org:Organization")
    graph.add_type(org_id, "foaf:Organization")
    graph.add_type(org_id, "foaf:Agent")

    unit_id = "kb:unit-digital-lab"
    graph.upsert_node(
        unit_id,
        types=["org:OrganizationalUnit", "org:Organization", "foaf:Organization", "foaf:Agent"],
        properties={
            "uco-core:name": "Digital Forensics Unit (synthetic)",
            "org:subOrganizationOf": {"@id": org_id},
        },
    )
    graph.add_property(org_id, "org:hasSubOrganization", {"@id": unit_id})

    membership_id = "kb:membership-1"
    graph.upsert_node(
        membership_id,
        types="org:Membership",
        properties={
            "org:member": {"@id": person_id},
            "org:organization": {"@id": unit_id},
            "org:role": {"@id": role_id},
        },
    )
    graph.add_property(unit_id, "org:hasMembership", {"@id": membership_id})

    contractor_id = "kb:contractor-1"
    graph.create(Person, id=contractor_id, name="Contract Analyst (synthetic)")
    graph.add_type(contractor_id, "foaf:Person")

    contractor_membership_id = "kb:membership-contractor"
    graph.upsert_node(
        contractor_membership_id,
        types="org:Membership",
        properties={
            "org:member": {"@id": contractor_id},
            "org:organization": {"@id": org_id},
            "org:role": {"@id": role_id},
        },
    )
    graph.add_property(org_id, "org:hasMembership", {"@id": contractor_membership_id})

    post_id = "kb:post-unit-lead"
    graph.upsert_node(
        post_id,
        types=["org:Post", "foaf:Agent"],
        properties={
            "uco-core:name": "Digital lab unit lead (synthetic)",
            "org:postIn": {"@id": unit_id},
            "org:role": {"@id": role_id},
        },
    )

    alex_interval_id = "kb:interval-alex-membership"
    graph.upsert_node(
        alex_interval_id,
        types="time:Interval",
        properties={
            "time:hasBeginning": {"@id": "kb:instant-alex-start"},
            "time:hasEnd": {"@id": "kb:instant-alex-end"},
        },
    )
    graph.upsert_node(
        "kb:instant-alex-start",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2024-01-01T00:00:00Z",
            },
        },
    )
    graph.upsert_node(
        "kb:instant-alex-end",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2025-05-31T23:59:59Z",
            },
        },
    )

    jordan_interval_id = "kb:interval-jordan-membership"
    graph.upsert_node(
        jordan_interval_id,
        types="time:Interval",
        properties={
            "time:hasBeginning": {"@id": "kb:instant-jordan-start"},
            "time:hasEnd": {"@id": "kb:instant-jordan-end"},
        },
    )
    graph.upsert_node(
        "kb:instant-jordan-start",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2025-06-01T00:00:00Z",
            },
        },
    )
    graph.upsert_node(
        "kb:instant-jordan-end",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2026-12-31T23:59:59Z",
            },
        },
    )

    post_occ1_id = "kb:post-occupancy-alex"
    graph.upsert_node(
        post_occ1_id,
        types="org:Membership",
        properties={
            "org:member": {"@id": person_id},
            "org:organization": {"@id": unit_id},
            "org:role": {"@id": role_id},
            "org:memberDuring": {"@id": alex_interval_id},
        },
    )
    graph.add_property(post_id, "org:heldBy", {"@id": post_occ1_id})

    post_occ2_id = "kb:post-occupancy-jordan"
    graph.upsert_node(
        post_occ2_id,
        types="org:Membership",
        properties={
            "org:member": {"@id": person2_id},
            "org:organization": {"@id": unit_id},
            "org:role": {"@id": role_id},
            "org:memberDuring": {"@id": jordan_interval_id},
        },
    )
    graph.add_property(post_id, "org:heldBy", {"@id": post_occ2_id})

    account_id = "kb:account-signal"
    account = graph.create(
        ObservableObject,
        id=account_id,
        name="Shared Signal account (synthetic)",
        has_facet=[AccountFacet(account_identifier="+15551234567", is_active=True)],
    )
    graph.add_type(account_id, "foaf:OnlineAccount")
    graph.add_property(account_id, "foaf:accountName", "+15551234567")

    graph.create(
        Relationship,
        source=[person],
        target=account,
        kind_of_relationship="Related_To",
        description=["Investigative hypothesis: Alex controlled the shared account (medium confidence)."],
        is_directional=True,
    )
    graph.create(
        Relationship,
        source=[person2],
        target=account,
        kind_of_relationship="Related_To",
        description=["Investigative hypothesis: Jordan also controlled the shared account (medium confidence)."],
        is_directional=True,
    )

    graph.create(
        Investigation,
        name="Synthetic case 2026-FOAF-001",
        description=[
            "Person, organization, unit, post, membership, and account kept distinct.",
            "org:role references a Role node; shared account attribution uses Relationship, not owl:sameAs.",
        ],
        object=[person, person2, org, account],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
