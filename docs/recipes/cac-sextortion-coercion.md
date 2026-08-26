# Sextortion and Online Coercion

> See [Recipe Index](INDEX.md) for all recipes.

Model sextortion schemes where offenders coerce minors through threats to share explicit images, financial demands, or compliance pressure. Combines **Layer 1 evidence** (messages, images) with **Layer 2 CAC interpretation** and **Layer 3 federal prosecution** when indictments stack CSEA counts with cyberstalking, identity theft, and wire fraud.

## Scope

**Layer 2 — Behavioral interpretation** for coercion dynamics; link to [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) when grooming precedes sextortion.

**Layer 3 — Federal prosecution** when the source is an indictment or complaint: compose with [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) for `chargedWith`, indictment bridges, and charge stacking. Use [cac-international-coordination.md](cac-international-coordination.md) when the defendant is abroad and extradition is alleged.

## Key classes

| Class | Role |
|---|---|
| `cacontology-sextortion:SextortionIncident` | Overarching coercion event |
| `cacontology-sextortion:ExtortionDemand` / `MonetaryDemand` | Content or financial demand objects |
| `cacontology-sextortion:ProgressiveEscalation` | Escalating manipulation of the victim |
| `cacontology-sextortion:SharingThreat` / `ImageLeakThreat` | Threats to publish explicit material |
| `cacontology-grooming:ChildVictim` / `cacontology-grooming:OnlinePredator` | Role-bearing identities |
| `Message` / `RasterPicture` | Digital evidence artifacts |
| `OffenderRole` / `VictimRole` | CAC role objects linked from identities via registered `Related_To` relationships with bearer-role descriptions |
| `FederalCharge` | Numbered counts (CSEA, cyberstalking, fraud) |
| `FederalProsecution` / `MultiDefendantIndictment` | Court filing structure |
| `ChildExploitationEnterprise` | When § 2252A(g) alleged alongside sextortion |
| `cacontology-multi-jurisdiction:ExtraditionRequest` | Formal extradition request when declared by the source |
| `InternationalJurisdiction` / `Location` | Foreign residence and filing court |

## Canonical pattern (Layer 2 conduct)

```
MessageThread (evidence)
  └── Related_To ──▶ cacontology-sextortion:SextortionIncident
        ├── cacontology-sextortion:employsThreat ──▶ SharingThreat / ImageLeakThreat
        ├── cacontology-sextortion:makesDemand ──▶ ExtortionDemand / MonetaryDemand
        ├── cacontology-sextortion:usesManipulation ──▶ ProgressiveEscalation
        ├── cacontology-sextortion:involvesDeception ──▶ IdentityImpersonation
        ├── cacontology-sextortion:conductsOnPlatform ──▶ InstantMessagingPlatform
        └── uco-action:object ──▶ ChildVictim (Identity + VictimRole)
```

## Federal prosecution bridge (Layer 3)

Sextortion indictments often **stack** non-CSEA counts on top of exploitation charges. Agents must wire both behavioral and legal layers:

```
uco-core:Bundle
  ├── SextortionIncident
  │     ├── Related_To ◀── FederalCharge (cyberstalking § 2261A)
  │     ├── Related_To ◀── FederalCharge (wire fraud § 1343)
  │     └── cacontology-sextortion:conductsOnPlatform ──▶ platform nodes
  │
  ├── FederalProsecution
  │     └── Related_To ──▶ MultiDefendantIndictment
  │
  ├── FederalCharge (Count 1 — conspiracy to produce)
  │     └── Related_To ──▶ SextortionIncident / CSAMIncident
  │
  ├── FederalCharge (Count 3 — enterprise § 2252A(g))
  │     └── Related_To ──▶ ChildExploitationEnterprise
  │
  ├── FederalCharge (Count 6 — cyberstalking)
  │     └── Related_To ──▶ SextortionIncident
  │
  ├── FederalCharge (Counts 7–8 — aggravated identity theft § 1028A)
  │     └── Related_To ──▶ SextortionIncident (impersonation conduct)
  │
  ├── FederalCharge (Counts 9–13 — wire fraud § 1343)
  │     └── Related_To ──▶ SextortionIncident / MonetaryDemand
  │
  ├── Person (defendant)
  │     └── cacontology-legal-outcomes:chargedWith ──▶ all applicable FederalCharge nodes
  │
  └── ExtraditionRequest (when documented)
        ├── Related_To ──▶ Person (defendant)
        └── Related_To ──▶ FederalProsecution
```

### Relationship checklist (sextortion + federal)

| # | Edge | When | Pattern |
|---|---|---|---|
| S1 | Incident → charges | Indictment sourced | `Related_To` from each `FederalCharge` to `SextortionIncident`, `CSAMIncident`, or enterprise |
| S2 | `chargedWith` | Always | Single-defendant cases still need `chargedWith` on the defendant `Person` |
| S3 | Cyberstalking count | § 2261A alleged | Dedicated `FederalCharge` linked to `SextortionIncident` (not only description text) |
| S4 | Identity theft counts | § 1028A alleged | Link to impersonation conduct node or scheme |
| S5 | Wire fraud counts | § 1343 alleged | Link to `MonetaryDemand` or incident; grouped counts (`9_13`) acceptable when indictment groups them |
| S6 | Enterprise count | § 2252A(g) in same case | Compose enterprise addendum from federal prosecution recipe |
| S7 | Co-conspirator narrative | Paragraphs name co-conspirators | Applicable declared enterprise `hasMember` property + `cacontology:participatesInEvent` on conspiracy |
| S8 | Extradition chain | Defendant abroad | `ExtraditionRequest` `Related_To` defendant + prosecution; foreign `Location` |
| S9 | Platform affordance abuse | Ban evasion / account recreation | `cacontology-sextortion:conductsOnPlatform` from incident to platform; ban-evasion detail in `uco-core:description` |
| S10 | Impersonation → incident | Posed-as-peer alleged | `cacontology-sextortion:involvesDeception` from `SextortionIncident` to `IdentityImpersonation` |

Grouped multi-count nodes (e.g., `charge-7_8`, `charge-9_13`) are acceptable when the indictment treats counts as a group **if** `chargedWith` and `Related_To` conduct links are still present.

## Modeling rules

- Keep **raw messages** in Layer 1; add CAC coercion types in Layer 2 as multi-typed interpretations.
- Document **financial vs. image-disclosure** coercion paths with the appropriate demand subclass.
- Link platform accounts and IP addresses when CyberTip reporting is in scope — see [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md).
- When platform sections in an indictment define **affordances** (DMs, stories, account recreation after ban), model platforms as nodes and link each `SextortionIncident` with `cacontology-sextortion:conductsOnPlatform`; use a registered `Related_To` relationship only when a broader enterprise has no applicable direct property.
- For **ban evasion** (dozens of recreated accounts), record counts in incident or enterprise `uco-core:description`; keep the platform link grounded as above.
- Always run the [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) checklist when building from an indictment.

## Fact-file template

```text
CASE_ID: 3:22-cr-00055-SLG-KFR
PRIMARY_COURT: U.S. District Court, District of Alaska
DEFENDANTS: 1
DEFENDANT_COUNTS:
  AMIN: 1,2,3,4,5,6,7,8,9,10,11,12,13

CHARGE_STACK:
  1-5: CSEA (conspiracy, enterprise, production, receipt/distribution)
  6: Cyberstalking — 18 U.S.C. 2261A
  7-8: Aggravated identity theft — 18 U.S.C. 1028A
  9-13: Wire fraud — 18 U.S.C. 1343

PLATFORMS: Instagram, Snapchat, Dropbox
TRANSNATIONAL: defendant citizen of Bangladesh, residing Malaysia
EXTRADITION: alleged extradition to U.S. for prosecution
```

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-sextortion": "https://cacontology.projectvic.org/sextortion#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
})

platform = graph.add_node("kb:platform-snapchat", "cacontology-sextortion:InstantMessagingPlatform", {
    "uco-core:name": "Snapchat",
})

incident = graph.add_node("kb:sextort-1", "cacontology-sextortion:SextortionIncident", {
    "uco-core:name": "Snapchat sextortion incident",
    "cacontology-sextortion:conductsOnPlatform": {"@id": "kb:platform-snapchat"},
})

charge_cyber = graph.add_node("kb:charge-6", "cacontology-legal-outcomes:FederalCharge", {
    "uco-core:name": "Count 6 — Cyberstalking (18 U.S.C. 2261A)",
    "cacontology-legal-outcomes:chargeCount": {"@type": "xsd:nonNegativeInteger", "@value": "6"},
})

defendant = graph.add_node("kb:defendant-1", "uco-identity:Person", {
    "uco-core:name": "Defendant-1",
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-6"}],
})

graph.add_node("kb:rel-charge-scheme", "uco-core:Relationship", {
    "uco-core:source": {"@id": "kb:charge-6"},
    "uco-core:target": {"@id": "kb:sextort-1"},
    "uco-core:kindOfRelationship": "Related_To",
    "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
})

graph.write("sextortion-case.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=sextortion-case.jsonld
```

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — indictment edges and charge stacking
- [cac-international-coordination.md](cac-international-coordination.md) — extradition and cross-border prosecution
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md)
- [cac-production-case.md](cac-production-case.md) — production counts in sextortion indictments
- [threaded-messaging.md](threaded-messaging.md)
- [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md)
