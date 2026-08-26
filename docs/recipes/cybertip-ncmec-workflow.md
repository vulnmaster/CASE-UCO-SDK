# NCMEC CyberTip Reporting Workflow

> See [Recipe Index](INDEX.md) for all recipes.

Model the institutional reporting and investigation workflow for NCMEC CyberTip reports using core CASE/UCO types and [CAC Ontology](https://cacontology.projectvic.org/) extension classes. This recipe covers how platform detection, ESP reporting, CyberTip generation, and law enforcement investigation are connected. For the grooming chat evidence and behavioral interpretation layers, see [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md). Based on the [snapchat-grooming-cybertip](../../examples/snapchat-grooming-cybertip.jsonld) example.

## Scope

This recipe covers **Layer 3 (Institutional Workflow)** of the three-layer pattern:

1. **Observable evidence** — see [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md)
2. **CAC behavioral interpretation** — see [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md)
3. **Institutional workflow** — *this recipe*: platform detection, ESP reporting obligations, NCMEC CyberTip lifecycle, and investigation triggering

## Key classes

| Class | Module | Role |
|---|---|---|
| `AutomatedDetectionAction` | `cacontology-detection` | Platform-side detection of exploitative content/behavior |
| `MachineLearningDetectionTool` | `cacontology-detection` | AI/ML tool used for automated detection |
| `ElectronicServiceProvider` | `cacontology-platforms` | ESP with legal reporting obligations (18 U.S.C. § 2258A) |
| `SocialMediaPlatform` | `cacontology-platforms` | Social media service (multi-typed on `ObservableObject`) |
| `NCMECCybertipReport` | `cacontology-us-ncmec` | CyberTip report artifact with incident typing |
| `OnlineEnticementIncident` | `cacontology-us-ncmec` | NCMEC incident type classification |
| `InvestigationTrigger` | `cacontology-us-ncmec` | Links CyberTip to investigation via `triggeredBy`/`resultedInInvestigation` |
| `PlatformCooperation` | `cacontology-us-ncmec` | ESP cooperation record with `cooperationLevel`, `involvesPlatform` |
| `CACInvestigation` | `cacontology` | Child-protection investigation (multi-typed on `case-investigation:Investigation`) |
| `InvestigativeAction` | `case-investigation` | Action nodes in the detection → report → CyberTip chain |

## Canonical workflow

```
Automated         T&S Human         Report to        CyberTip
Detection ─uco-action:result─▶ Review ──uco-action:result──▶ NCMEC ──uco-action:result──▶ Generation
                  (platform policy)                        │
                                                           ▼
                                                NCMECCybertipReport
                                                  ├── cacontology-us-ncmec:hasNCMECIncidentType ──▶ incident type
                                                  └── (artifact with ExternalReference)
                                                           │
                                                           ▼
                                                InvestigationTrigger
                                                  ├── cacontology-us-ncmec:triggeredBy ──▶ NCMECCybertipReport
                                                  └── cacontology-us-ncmec:resultedInInvestigation ──▶ CACInvestigation

  PlatformCooperation
      └── cacontology-us-ncmec:involvesPlatform ──▶ SocialMediaPlatform
```

### Action chain

The reporting workflow is modeled as a chain of `InvestigativeAction` nodes connected by `uco-action:result` (action → next action or artifact):

1. **`AutomatedDetectionAction`** — the platform's detection system flags content. The `performer` is the ESP identity; the `instrument` is the detection tool; `object` references the flagged threads/images; `result` links to the T&S review.
2. **Trust & Safety Review** (`InvestigativeAction`) — a human analyst on the platform's Trust & Safety team reviews the automated detection before deciding to report. This step is **platform-policy-dependent**: some ESPs auto-report all detections, others require human confirmation. Modeling it explicitly ensures the workflow can represent either policy. The `performer` is the ESP identity (the organization, not an individual analyst); `object` includes the same flagged evidence; `result` links to the NCMEC report action if the review confirms the finding.
3. **Report to NCMEC** (`InvestigativeAction`) — the ESP submits the report to NCMEC per 18 U.S.C. § 2258A. The report must include the data elements NCMEC needs to build an actionable CyberTip (see below). Uses `case-investigation:wasInformedBy` to reference the T&S review.
4. **CyberTip Generation** (`InvestigativeAction` + `ReceiveCybertipAction`) — NCMEC generates the CyberTipline report. Its `result` is the `NCMECCybertipReport` artifact.

The action chain uses `uco-action:result` as the direct property linking each step. Do not add a redundant generic Relationship for the same result edge.

### NCMEC-required data elements

NCMEC needs specific data from the ESP to build a CyberTip that law enforcement can act on. The ESP's report action (`uco-action:object`) must reference these as observable objects:

| Data element | CASE/UCO type | Purpose |
|---|---|---|
| **Offender account handle** | `ApplicationAccount` + `AccountFacet` (`accountIdentifier`) | Identify the suspect on the platform |
| **Offender IP address** | `ObservableObject` + `IPv4AddressFacet` or `IPv6AddressFacet` | Locate the suspect geographically for jurisdictional routing |
| **Victim account handle** | `ApplicationAccount` + `AccountFacet` (`accountIdentifier`) | Identify and locate the child for welfare checks |
| **Victim IP address** | `ObservableObject` + `IPv4AddressFacet` or `IPv6AddressFacet` | Determine victim jurisdiction |
| **Chat content / threads** | `MessageThread` | Evidence of the exploitative interaction |
| **CSAM images** | `RasterPicture` / `ProducedImage` | Evidence of the produced material |
| **Timestamps** | `MessageFacet` (`sentTime`), action `startTime`/`endTime` | Establish timeline for the offense |
| **Account registration data** | `AccountFacet` (`accountCreatedTime`, `owner`) | Corroborate offender identity |

The IP addresses used by the offender and victim to access the platform are essential for NCMEC to route the CyberTip to the correct law enforcement jurisdiction. Model each as an `ObservableObject` with an `IPv4AddressFacet` (or `IPv6AddressFacet`) and link them to the corresponding `ApplicationAccount` via Relationships.

### CyberTip report artifact

The `NCMECCybertipReport` is the central artifact:

- Multi-typed as `["uco-observable:ObservableObject", "cacontology-us-ncmec:NCMECCybertipReport"]`
- **`hasNCMECIncidentType`** — direct link to the incident classification (e.g., `OnlineEnticementIncident`)
- **`uco-core:externalReference`** — NCMEC report identifier and URL
- **`uco-core:hasFacet`** — `ContentDataFacet` for the report document itself

### Investigation trigger

The `InvestigationTrigger` is the domain object connecting the report to the investigation:

- **`triggeredBy`** — IRI link to the `NCMECCybertipReport`
- **`resultedInInvestigation`** — IRI link to the `CACInvestigation`
- **`triggerCriteria`** — controlled value (e.g., `victim_age`, `content_severity`)
- **`urgencyLevel`** — controlled value: `immediate`, `urgent`, `routine`

### Platform cooperation

`PlatformCooperation` records the ESP's cooperation with the investigation:

- **`involvesPlatform`** — direct link to the platform (do not add a redundant Relationship)
- **`cooperationLevel`** — controlled value: `full`, `partial`, `limited`, `none`
- **`dataProvided`** — description of preserved data categories

## Direct properties vs. generic Relationships

<!-- recipe-lint: ignore-start anti-pattern -- The first column deliberately shows unregistered relationship labels that authors must replace. -->
| Instead of `Relationship` with... | Use direct property | On class |
|---|---|---|
| `kindOfRelationship: "Resulted_In"` | `uco-action:result` | `InvestigativeAction` → next action/artifact |
| `kindOfRelationship: "Provided_By"` | `cacontology-us-ncmec:involvesPlatform` | `PlatformCooperation` → platform |
| (incident type link) | `cacontology-us-ncmec:hasNCMECIncidentType` | `NCMECCybertipReport` → incident type |
| (trigger link) | `cacontology-us-ncmec:triggeredBy` | `InvestigationTrigger` → report |
| (investigation link) | `cacontology-us-ncmec:resultedInInvestigation` | `InvestigationTrigger` → investigation |
<!-- recipe-lint: ignore-end anti-pattern -->

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import ObservableObject, ContentDataFacet
from case_uco.case.investigation import Investigation, InvestigativeAction

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-detection": "https://cacontology.projectvic.org/detection#",
    "cacontology-us-ncmec": "https://cacontology.projectvic.org/us/ncmec#",
    "cacontology-platforms": "https://cacontology.projectvic.org/platforms#",
})

# ESP identity
snap_identity = graph.create("uco-identity:Identity", name="Snap Inc.",
    extra_types=["cacontology-platforms:ElectronicServiceProvider"])

# Detection tool
tool = graph.create("uco-tool:AnalyticTool", name="Safety Monitoring Service",
    extra_types=["cacontology-detection:MachineLearningDetectionTool"])

# IP addresses (essential for NCMEC jurisdictional routing)
offender_ip = graph.create(ObservableObject, name="Offender IP Address",
    has_facet=[{"@type": "uco-observable:IPv4AddressFacet",
                "uco-observable:addressValue": "198.51.100.42"}])
victim_ip = graph.create(ObservableObject, name="Victim IP Address",
    has_facet=[{"@type": "uco-observable:IPv4AddressFacet",
                "uco-observable:addressValue": "203.0.113.17"}])

# Action chain: detect → T&S review → report → cybertip
detection = graph.create(InvestigativeAction,
    name="Grooming and CSAM Detection",
    extra_types=["cacontology-detection:AutomatedDetectionAction"],
    performer=snap_identity, instrument=[tool],
    start_time="2025-04-12T16:22:00-05:00",
    end_time="2025-04-12T16:30:00-05:00")

ts_review = graph.create(InvestigativeAction,
    name="Trust & Safety Review",
    performer=snap_identity,
    start_time="2025-04-12T16:35:00-05:00",
    end_time="2025-04-12T16:55:00-05:00")
detection.result = [ts_review]

report_action = graph.create(InvestigativeAction,
    name="Report to NCMEC",
    performer=snap_identity,
    start_time="2025-04-12T17:00:00-05:00")
ts_review.result = [report_action]

cybertip_action = graph.create(InvestigativeAction,
    name="NCMEC CyberTipline Report Generation",
    extra_types=["cacontology:ReceiveCybertipAction"],
    start_time="2025-04-12T18:00:00-05:00")
report_action.result = [cybertip_action]

# CyberTip artifact with direct incident-type link
incident_type = graph.add_node("kb:incident-type-1", [
    "uco-core:UcoObject", "cacontology-us-ncmec:OnlineEnticementIncident",
], {"uco-core:name": "Online Enticement of Children for Sexual Acts"})

cybertip = graph.add_node("kb:cybertip-1", [
    "uco-observable:ObservableObject", "cacontology-us-ncmec:NCMECCybertipReport",
], {
    "uco-core:name": "CyberTipline Report #CT-2025-04-12-00001",
    "cacontology-us-ncmec:hasNCMECIncidentType": {"@id": "kb:incident-type-1"},
})
cybertip_action.result = [cybertip]

# Investigation
investigation = graph.create(Investigation,
    name="Snapchat Grooming Investigation",
    extra_types=["cacontology:CACInvestigation"])

# Investigation trigger
trigger = graph.add_node("kb:trigger-1", [
    "uco-core:UcoObject", "cacontology-us-ncmec:InvestigationTrigger",
], {
    "cacontology-us-ncmec:triggeredBy": {"@id": "kb:cybertip-1"},
    "cacontology-us-ncmec:resultedInInvestigation": {"@id": investigation.id},
    "cacontology-us-ncmec:triggerCriteria": "victim_age",
    "cacontology-us-ncmec:urgencyLevel": "urgent",
})

# Platform cooperation with direct property
cooperation = graph.add_node("kb:coop-1", [
    "uco-observable:ObservableObject", "cacontology-us-ncmec:PlatformCooperation",
], {
    "uco-core:name": "Snap Inc. Platform Cooperation",
    "cacontology-us-ncmec:cooperationLevel": "full",
    "cacontology-us-ncmec:dataProvided": "account_info, content, metadata",
    "cacontology-us-ncmec:involvesPlatform": {"@id": snap_identity.id},
})

graph.write("cybertip_workflow.jsonld")
```

</details>

## Notes

- **18 U.S.C. § 2258A** requires ESPs to report apparent child sexual exploitation to NCMEC. The `AutomatedDetectionAction` → `Trust & Safety Review` → `Report to NCMEC` chain models this legal obligation.
- **Trust & Safety review** is platform-policy-dependent. NCMEC wants high-quality reports, and most platforms have T&S teams that review automated detections before filing. Always model this step explicitly to maintain workflow fidelity, even if a given platform auto-reports without human review (in that case, note the policy in the action's description).
- **`NCMECCybertipReport`** maps to the [NCMEC CyberTip API](https://www.missingkids.org/gethelpnow/cybertipline). Use `hasNCMECIncidentType` to directly link to incident classification rather than a generic Relationship.
- **`InvestigationTrigger`** is the proper domain class for `triggeredBy` and `resultedInInvestigation` properties. Always create an explicit trigger node to connect the CyberTip to the CACInvestigation.
- **Action chain linking** uses `uco-action:result` exclusively. Do not duplicate the direct property with a generic Relationship.
- **Platform cooperation** uses `cacontology-us-ncmec:involvesPlatform` as a direct property. Do not duplicate it with a generic Relationship.
- **Controlled vocabularies:**
  - `cooperationLevel`: `full`, `partial`, `limited`, `none`
  - `urgencyLevel`: `immediate`, `urgent`, `routine`
  - `triggerCriteria`: `victim_age`, `content_severity`, `cross_jurisdictional`, `repeat_offender`

### Validation

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/cac/ontology/ontology/cacontology-core-spine.ttl \
  --ontology-graph ontology/cac/ontology/ontology/cacontology-us-ncmec.ttl \
  --ontology-graph ontology/cac/ontology/ontology/cacontology-detection.ttl \
  --ontology-graph ontology/cac/ontology/ontology/cacontology-platforms.ttl \
  --inference rdfs --allow-infos \
  cybertip_workflow.jsonld
```

## Related

- [cac-hotline-intake-lifecycle.md](cac-hotline-intake-lifecycle.md) — hotline intake, triage, and referral before/alongside the CyberTip
