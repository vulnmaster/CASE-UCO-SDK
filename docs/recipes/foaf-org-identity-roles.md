# FOAF and ORG Identity, Roles, and Membership

> See [Recipe Index](INDEX.md) for all recipes.

Distinguish **person**, **identity**, **account**, **role**, **membership**, and **organization** when modeling investigators, suspects, platforms, and task forces. Enrich UCO types with [FOAF](http://xmlns.com/foaf/0.1/) and [W3C ORG](https://www.w3.org/TR/vocab-org/) on the same IRI where appropriate.

Issue: [#63](https://github.com/vulnmaster/CASE-UCO-SDK/issues/63)

## Scope

- Person vs identity vs account vs role vs membership vs organization
- No `owl:sameAs` for uncertain attribution
- Exemplar: `examples/upper-ontology/foaf-org/build_exemplar.py`

## Concept separation

| Concept | CASE/UCO | FOAF / ORG enrichment |
|---|---|---|
| **Person** (human) | `uco-identity:Person` | `foaf:Person`, `foaf:givenName`, `foaf:mbox` |
| **Identity** (abstract) | `uco-identity:Identity` | `foaf:Agent` when needed |
| **Organization** | `uco-identity:Identity` (org name) | `org:Organization`, `foaf:Organization` |
| **Account** (platform login) | `uco-observable:ObservableObject` + `AccountFacet` | `foaf:OnlineAccount`, `foaf:accountName` |
| **Membership** | — (separate node) | `org:Membership` linking member ↔ organization |
| **Role** (job/function) | `Relationship` or action `performer` | `org:role` on `org:Membership` |

## Decision rules

1. **Person ≠ account.** A `Person` holds accounts via `foaf:holdsAccount` → `foaf:OnlineAccount` on the account IRI.
2. **Organization is not a Person.** Type task forces and agencies as `Identity` + `org:Organization`.
3. **Membership is reified.** Use `org:Membership` when start/end dates or role titles matter.
4. **Uncertain linking → Relationship, not `owl:sameAs`.** When attribution is investigative hypothesis, use `uco-core:Relationship` with `kind_of_relationship` and confidence in `description` — never assert `owl:sameAs` between uncertain identities.
5. **Platform issuer** stays a separate `Identity` on `AccountFacet.account_issuer`.

## Python pattern

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.identity import Identity, Person
from case_uco.uco.observable import ObservableObject, AccountFacet
from case_uco.uco.core import Relationship

graph = CASEGraph(extra_context={
    "foaf": "http://xmlns.com/foaf/0.1/",
    "org": "http://www.w3.org/ns/org#",
})

person_id = "kb:person-1"
person = graph.create(Person, id=person_id, name="...")
graph.add_type(person_id, "foaf:Person")

org_id = "kb:org-1"
org = graph.create(Identity, id=org_id, name="...")
graph.add_type(org_id, "org:Organization")

graph.upsert_node("kb:membership-1", types="org:Membership", properties={
    "org:member": {"@id": person_id},
    "org:organization": {"@id": org_id},
    "org:role": "...",
})
graph.add_property(org_id, "org:hasMembership", {"@id": "kb:membership-1"})

account_id = "kb:account-1"
account = graph.create(ObservableObject, id=account_id, name="...",
    has_facet=[AccountFacet(account_identifier="...", is_active=True)],
)
graph.add_type(account_id, "foaf:OnlineAccount")
graph.add_property(person_id, "foaf:holdsAccount", {"@id": account_id})

# Investigative link — not owl:sameAs
graph.create(Relationship, source=[person], target=account,
    kind_of_relationship="Related_To", is_directional=True,
    description=["Evidence supports a tentative attribution of the target account to the source person."])
graph.write("foaf-org-identity.jsonld")
```

</details>

```bash
python examples/upper-ontology/foaf-org/build_exemplar.py
```

## Validation

```bash
validate_graph("foaf-org-identity.jsonld", profiles=["foaf", "org"])

case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/upper/shapes/sh-foaf.ttl \
  --ontology-graph ontology/upper/shapes/sh-org.ttl \
  --allow-info foaf-org-identity.jsonld
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| `owl:sameAs` for tentative attribution | `Relationship` + descriptive `kind_of_relationship` |
| Account typed as `foaf:Person` | `foaf:OnlineAccount` on account IRI |
| Organization as `Person` | `org:Organization` on org IRI |
| Collapsed membership (edge only) | `org:Membership` when role/period matters |
| Missing `account_issuer` | Keep UCO `AccountFacet.account_issuer` |

## Related

- [accounts.md](accounts.md) — multi-platform account linking
- [device.md](device.md) — workstation and user accounts
- [prov-o-evidence-lineage.md](prov-o-evidence-lineage.md) — `prov:Agent` for performers
- [cross-ontology-composition.md](cross-ontology-composition.md) — FOAF/ORG with other profiles
