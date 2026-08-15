# Composition patterns observed in the recipe catalog

The SDK currently teaches composition through 77 recipes, the mapping
guide, `TASK_TO_CLASSES`, and a handful of `CORE_PATTERNS`. There is
**no first-class Composition Profile object** yet — that is the Phase 1
gap this study measures.

## Catalog size

| | Count |
|---|---:|
| Recipe files parsed | 79 |
| Starter kits | 4 |
| CAC-series recipes | 17 |
| Mapping-guide sources | 18 |
| Task-to-class mappings | 26 |

## Dominant host classes (mentions across recipes)

| Class | Recipe files |
|---|---:|
| `ObservableObject` | 56 |
| `Role` | 55 |
| `InvestigativeAction` | 42 |
| `Relationship` | 40 |
| `FileFacet` | 33 |
| `Identity` | 31 |
| `Investigation` | 31 |
| `ContentDataFacet` | 30 |
| `Pattern` | 26 |
| `Person` | 26 |
| `Tool` | 26 |
| `Hash` | 21 |
| `ProvenanceRecord` | 21 |
| `Location` | 21 |
| `UcoObject` | 21 |
| `Action` | 20 |
| `File` | 17 |
| `Device` | 14 |
| `Event` | 14 |
| `Organization` | 14 |

## Dominant Facets (mentions across recipes)

| Facet | Recipe files |
|---|---:|
| `FileFacet` | 44 |
| `ContentDataFacet` | 31 |
| `AccountFacet` | 14 |
| `DeviceFacet` | 12 |
| `ApplicationFacet` | 8 |
| `EmailAddressFacet` | 7 |
| `MessageFacet` | 7 |
| `DataRangeFacet` | 6 |
| `SimpleAddressFacet` | 6 |
| `ApplicationAccountFacet` | 5 |
| `DomainNameFacet` | 5 |
| `PhoneAccountFacet` | 4 |
| `SoftwareFacet` | 4 |
| `IPAddressFacet` | 4 |
| `EventRecordFacet` | 3 |
| `MessageThreadFacet` | 3 |
| `MobileDeviceFacet` | 3 |
| `SIMCardFacet` | 3 |
| `LatLongCoordinatesFacet` | 3 |
| `IPv4AddressFacet` | 3 |

## Co-occurring `has_facet=[...]` sets

These are the Facet bundles that already appear together in recipe code
samples. They are the empirical seed for Composition Profiles.

| Facet set | Occurrences |
|---|---:|
| `FileFacet` | 24 |
| `ContentDataFacet` + `FileFacet` | 17 |
| `ContentDataFacet` | 11 |
| `ApplicationFacet` | 8 |
| `EmailAddressFacet` | 7 |
| `MessageFacet` | 7 |
| `DeviceFacet` | 7 |
| `DataRangeFacet` | 6 |
| `SimpleAddressFacet` | 5 |
| `AccountFacet` + `ApplicationAccountFacet` | 4 |
| `AccountFacet` + `PhoneAccountFacet` | 4 |
| `AccountFacet` | 4 |
| `IPAddressFacet` | 4 |
| `DomainNameFacet` | 4 |
| `EventRecordFacet` | 3 |

## Mapping-guide composition patterns

| Source | Pattern | Facets |
|---|---|---|
| filesystem report | `ObservableObject + FileFacet + ContentDataFacet` | `FileFacet`, `ContentDataFacet` |
| mobile device extraction | `ObservableObject + DeviceFacet + ApplicationFacet + MessageFacet` | `DeviceFacet`, `ApplicationFacet`, `MessageFacet`, `ContactFacet` |
| iOS sysdiagnose archive | `Device + sysdiagnose FileFacet directory + AppleUnifiedLogArchive/EventLog` | `DeviceFacet`, `MobileDeviceFacet`, `SoftwareFacet`, `FileFacet` |
| Apple unified logs | `AppleUnifiedLogArchive → EventRecord + Event + AnalyticTool outputs (CSV/SQLite)` | `EventRecordFacet`, `ApplicationFacet` |
| email export | `ObservableObject + EmailMessageFacet + EmailAddressFacet` | `EmailMessageFacet`, `EmailAddressFacet`, `EmailAccountFacet`, `ContentDataFacet` |
| forensic tool run | `Investigation + InvestigativeAction + Tool + ObservableObject` |  |
| pcap network capture | `ObservableObject + NetworkConnectionFacet + IPAddressFacet` | `NetworkConnectionFacet`, `IPAddressFacet`, `DomainNameFacet`, `URLFacet` |
| disk image | `ObservableObject + ImageFacet + ContentDataFacet + FileFacet` | `ImageFacet`, `FileFacet`, `ContentDataFacet` |
| browser history | `ObservableObject + URLHistoryFacet + BrowserBookmarkFacet + CookieFacet` | `URLHistoryFacet`, `BrowserBookmarkFacet`, `CookieFacet`, `URLFacet`, `ApplicationFacet` |
| ai ml image analysis | `InvestigativeAction (per pipeline step) + AnalyticTool + RasterPicture + ConfidenceFacet + Relationship` | `RasterPictureFacet`, `FileFacet`, `ContentDataFacet`, `ConfidenceFacet` |
| registry artifacts | `ObservableObject + WindowsRegistryKeyFacet + WindowsRegistryValueFacet` | `WindowsRegistryKeyFacet`, `WindowsRegistryValueFacet`, `FileFacet` |
| child sex trafficking ring or recruitment network | `CACInvestigation + TraffickingEnterprise + (TraffickingRing | TraffickingCell) + TraffickingVictimRole + (PeerRecruitmentNetwork | ClassmateRecruitmentNetwork) + (SchoolBasedRecruitment | StreetBasedRecruitment with pretext approach) + DigitalToPhysicalBridge` |  |
| multi-jurisdictional rescue or task force operation | `CACInvestigation + TaskForce + (LocalJurisdiction | StateJurisdiction | FederalJurisdiction | InternationalJurisdiction) + JointInvestigation + (MassChildRescueOperation | VictimExtraction) + JurisdictionalHandoff + MutualAidRequest` |  |
| tactical arrest or high-risk operation | `CACInvestigation + (ArrestOperation | HighRiskArrest) + DynamicEntry + SuspectProfile + ThreatAssessment + AssetForfeitureAction` |  |
| victim rescue extraction and post-rescue services | `CACInvestigation + EmergencyResponse + VictimExtraction + OngoingDangerAssessment + SafetyPlanning + MultiAgencyVictimResponse + TraumaIndicator + HelpSeekingBarrier` |  |
| csam provenance forensics and victim identification | `ForensicAcquisitionAction + ChainOfCustodyAction (per event) + EvidenceVerificationAction + (MetadataCorrelation | TemporalPatternAnalysis | GeospatialCorrelation | CrossPlatformCorrelation | BehavioralFingerprinting) + VictimIdentificationProcess` | `RasterPictureFacet`, `FileFacet`, `ContentDataFacet` |
| icac search warrant arrest | `CACInvestigation + MarylandICACtaskForce + InvestigativeAction chain + Authorization + ArrestOperation (warrant_arrest) + BookingAction + CorrectionalFacility + StateCharge` |  |
| cybertip grooming report | `CACInvestigation + GroomingBehavior + NCMECCybertipReport + GroomingMessage + ChildVictim + OnlinePredator` | `MessageFacet` |

## Recurring logical patterns (not yet first-class)

1. **Observable + Facets** — one `ObservableObject` (or typed subclass such
   as `RasterPicture`) carries every Facet that describes the same real-world
   thing. Never one Observable per Facet.
2. **Action / instrument / object / result** — `InvestigativeAction` points
   at a `Tool`, the evidence it consumed, and the evidence it produced.
3. **Provenance + chain of custody** — `ProvenanceRecord` groups a
   transfer; CAC adds `ChainOfCustodyAction` / `EvidenceVerificationAction`
   as auditable steps.
4. **Role ≠ person** — CAC `Role` (victim, offender, examiner) is borne by
   an `EnduringEntity`; the person is not the role.
5. **Phase ≠ investigation** — grooming / investigation / recovery phases
   hang off the enduring process via `cac-core:hasPhase`.
6. **Hash intelligence** — `ContentDataFacet` + `Hash` is the integrity
   spine; PhotoDNA / perceptual hashes are referenced in CAC recipes
   (`ContentHashingTool`) but have no first-class Facet or VICS mapping.
7. **Cross-ontology composition** — CASE/UCO + CAC + legalproc/cryptoinv
   + one upper profile (gUFO preferred for CAC). Dual BFO+gUFO typing is
   an anti-pattern.

## Every recipe (class / Facet mention counts)

| Recipe | Series | Classes | Facets |
|---|---|---:|---:|
| [Multi-Platform Account Linking](../docs/recipes/accounts.md) | core | 19 | 8 |
| [Advanced File Patterns](../docs/recipes/advanced-file-patterns.md) | core | 16 | 8 |
| [AI/ML Analysis Pipelines](../docs/recipes/ai-analysis-pipeline.md) | core | 23 | 5 |
| [Forensic Analysis and Artifact Classification](../docs/recipes/analysis.md) | core | 18 | 3 |
| [Apple Unified Logs and Analytic Tool Outputs](../docs/recipes/apple-unified-logs.md) | core | 23 | 5 |
| [Bulk Extractor Forensic Paths](../docs/recipes/bulk-extractor-path.md) | core | 16 | 6 |
| [CSAM Forensic Provenance and Victim Identification](../docs/recipes/cac-csam-forensic-provenance.md) | CAC | 23 | 2 |
| [Federal Prosecution Relationship Completeness](../docs/recipes/cac-federal-prosecution-relationships.md) | CAC | 32 | 1 |
| [Federal Trial Proceedings and Docket Lifecycle](../docs/recipes/cac-federal-trial-proceedings.md) | CAC | 21 | 1 |
| [Online Grooming Chat Modeling](../docs/recipes/cac-grooming-chat-modeling.md) | CAC | 49 | 8 |
| [Hotline Intake and Referral Lifecycle](../docs/recipes/cac-hotline-intake-lifecycle.md) | CAC | 5 | 0 |
| [ICAC Search Warrant Arrest (Press Release Pattern)](../docs/recipes/cac-icac-search-warrant-arrest.md) | CAC | 31 | 2 |
| [International Coordination and Cross-Border Operations](../docs/recipes/cac-international-coordination.md) | CAC | 9 | 0 |
| [Legal Charges, Sentencing, and Case Outcomes](../docs/recipes/cac-legal-sentencing-outcomes.md) | CAC | 18 | 0 |
| [Missing Child Investigations](../docs/recipes/cac-missing-child-investigation.md) | CAC | 8 | 2 |
| [Multi-Jurisdictional Task Force Operations](../docs/recipes/cac-multi-jurisdiction-task-force.md) | CAC | 19 | 0 |
| [PACER Document Ingestion (MCP Agent Workflow)](../docs/recipes/cac-pacer-document-ingestion.md) | CAC | 33 | 2 |
| [CSAM Production and Manufacturing Cases](../docs/recipes/cac-production-case.md) | CAC | 17 | 1 |
| [Sextortion and Online Coercion](../docs/recipes/cac-sextortion-coercion.md) | CAC | 21 | 0 |
| [Tactical Arrest and Undercover Operations](../docs/recipes/cac-tactical-undercover-operation.md) | CAC | 14 | 0 |
| [Child Sex Trafficking and Recruitment Networks](../docs/recipes/cac-trafficking-recruitment-network.md) | CAC | 34 | 1 |
| [Victim Rescue, Extraction, and Post-Rescue Services](../docs/recipes/cac-victim-rescue-extraction.md) | CAC | 14 | 0 |
| [Call Log Records](../docs/recipes/call-log.md) | core | 12 | 4 |
| [Cargo Theft, Route Staging, and Warehouse Movement](../docs/recipes/cargo-theft-route-staging.md) | core | 24 | 7 |
| [Cell Site and Tower Data](../docs/recipes/cell-site.md) | core | 21 | 10 |
| [Chain of Custody](../docs/recipes/chain-of-custody.md) | core | 18 | 5 |
| [Proposing Changes to CASE/UCO](../docs/recipes/change-proposal.md) | core | 12 | 5 |
| [Configured Tools](../docs/recipes/configured-tool.md) | core | 13 | 1 |
| [Cross-Domain Extensions](../docs/recipes/cross-domain-extensions.md) | core | 2 | 0 |
| [Cross-Ontology Composition](../docs/recipes/cross-ontology-composition.md) | core | 12 | 0 |
| [Cyber Threat Intelligence and APT Reporting](../docs/recipes/cyber-threat-intelligence.md) | core | 49 | 11 |
| [NCMEC CyberTip Reporting Workflow](../docs/recipes/cybertip-ncmec-workflow.md) | CAC | 38 | 5 |
| [Database Record Extraction](../docs/recipes/database-records.md) | core | 11 | 3 |
| [Device and Workstation Modeling](../docs/recipes/device.md) | core | 15 | 6 |
| [Elder Fraud and Government-Impersonation Schemes](../docs/recipes/elder-fraud-impersonation.md) | core | 22 | 3 |
| [Email and Messaging](../docs/recipes/email-messaging.md) | core | 4 | 3 |
| [Espionage Act and Classified-Information Disclosure](../docs/recipes/espionage-classified-disclosure.md) | core | 19 | 2 |
| [Events and Authentication Logs](../docs/recipes/event.md) | core | 16 | 3 |
| [EXIF and Image Metadata](../docs/recipes/exif-data.md) | core | 24 | 7 |
| [Existence Intervals and Temporal Modeling](../docs/recipes/existence-intervals.md) | core | 4 | 0 |
| [Export Control and Sanctions Evasion](../docs/recipes/export-control-sanctions.md) | core | 15 | 1 |
| [Working with Extensions](../docs/recipes/extensions.md) | core | 13 | 0 |
| [File Fragments and Multipart Files](../docs/recipes/file-fragments.md) | core | 12 | 4 |
| [File Recovery and Carving](../docs/recipes/file-recovery.md) | core | 18 | 5 |
| [File System Forensics](../docs/recipes/file-system.md) | core | 5 | 3 |
| [FOAF/ORG Identity Roles and Organizations](../docs/recipes/foaf-org-identity-roles.md) | core | 8 | 1 |
| [Forensic Investigation Lifecycle](../docs/recipes/forensic-lifecycle.md) | core | 15 | 0 |
| [Modeling a Forensic Tool and Its Output](../docs/recipes/forensic-tool.md) | core | 4 | 0 |
| [Foundational Typing (BFO and gUFO)](../docs/recipes/foundational-typing-bfo-gufo.md) | core | 11 | 1 |
| [Fraud, Cryptocurrency, and Money Laundering Investigations](../docs/recipes/fraud-crypto-laundering.md) | core | 39 | 12 |
| [GeoSPARQL Geospatial Evidence](../docs/recipes/geosparql-geospatial-evidence.md) | core | 5 | 2 |
| [Insider Threat, Trade Secret Theft, and Economic Espionage](../docs/recipes/insider-threat-trade-secrets.md) | core | 23 | 4 |
| [iOS / macOS Sysdiagnose Archives](../docs/recipes/ios-sysdiagnose.md) | core | 26 | 8 |
| [Managing Large Datasets](../docs/recipes/large-datasets.md) | core | 8 | 3 |
| [Legal Process Modeling (Charges, Verdicts, Sentences)](../docs/recipes/legal-process-modeling.md) | core | 19 | 0 |
| [Location Modeling](../docs/recipes/location.md) | core | 8 | 2 |
| [Mobile Device and SIM Card](../docs/recipes/mobile-device-sim.md) | core | 20 | 10 |
| [Mobile Device Forensics](../docs/recipes/mobile-device.md) | core | 8 | 6 |
| [Network Artifact Extraction](../docs/recipes/network-artifacts.md) | core | 25 | 11 |
| [Network Investigation with Bundle](../docs/recipes/network-investigation.md) | core | 35 | 11 |
| [OWL-Time Temporal Evidence](../docs/recipes/owl-time-temporal-evidence.md) | core | 2 | 0 |
| [Disk Partitions and Volume Recovery](../docs/recipes/partitions.md) | core | 24 | 7 |
| [PROF Validation Profile Metadata](../docs/recipes/prof-validation-profile-metadata.md) | core | 4 | 0 |
| [PROV-O Evidence Lineage](../docs/recipes/prov-o-evidence-lineage.md) | core | 8 | 0 |
| [Racketeering (RICO) and Criminal Enterprise](../docs/recipes/racketeering-enterprise.md) | core | 12 | 0 |
| [Authoring and Improving Recipes](../docs/recipes/recipe-authoring.md) | core | 2 | 0 |
| [Round-Trip: Serialize and Deserialize](../docs/recipes/round-trip.md) | core | 1 | 0 |
| [Discovering Classes at Runtime](../docs/recipes/runtime-discovery.md) | core | 3 | 1 |
| [SMS Messages and Contacts](../docs/recipes/sms-and-contacts.md) | core | 18 | 7 |
| [SOLVE-IT Investigation Planning and Error Mitigation](../docs/recipes/solve-it-investigation-planning.md) | core | 24 | 0 |
| [SOLVE-IT Plan versus Execution Provenance](../docs/recipes/solveit-plan-execution-provenance.md) | core | 5 | 0 |
| [Spear Phishing and Attack Narratives](../docs/recipes/spear-phishing.md) | core | 27 | 7 |
| [Starter Kit: Email Export Mapping](../docs/recipes/starter-email-export.md) | core | 7 | 4 |
| [Starter Kit: Filesystem Report Mapping](../docs/recipes/starter-filesystem-report.md) | core | 8 | 2 |
| [Starter Kit: Mobile Extraction Mapping](../docs/recipes/starter-mobile-extraction.md) | core | 10 | 5 |
| [Starter Kit: Tool Run Mapping](../docs/recipes/starter-tool-run.md) | core | 10 | 2 |
| [Threaded Messaging (WhatsApp, Chat)](../docs/recipes/threaded-messaging.md) | core | 19 | 7 |
| [Windows USN Journal](../docs/recipes/usn-journal.md) | core | 23 | 6 |
| [Weapons and Drug Evidence](../docs/recipes/weapons-drug-evidence.md) | core | 16 | 0 |

See `composition-patterns.json` for the full per-recipe class lists,
`has_facet` sets, mapping-guide anti-patterns, and task mappings.
