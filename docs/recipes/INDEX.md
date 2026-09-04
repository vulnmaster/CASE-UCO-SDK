# CASE/UCO SDK Recipes

Practical patterns for common digital forensics and cyber-investigation workflows. Each recipe shows how to model real-world data using the SDK across all four supported languages.

For the full class reference, see [ONTOLOGY_REFERENCE.md](../../ONTOLOGY_REFERENCE.md). For domain-to-class mapping, see [MAPPING_GUIDE.md](../MAPPING_GUIDE.md). For performance guidance, see [PERFORMANCE_GUIDE.md](../PERFORMANCE_GUIDE.md).

---

> **Validate your output.** After any recipe produces a `.jsonld` file, validate it with [case-utils](https://github.com/casework/CASE-Utilities-Python):
>
> ```bash
> pip install case-utils  # one-time install
> case_validate --built-version case-1.4.0 my-output.jsonld
> ```
>
> If you use an extension ontology, include its shapes:
>
> ```bash
> case_validate --built-version case-1.4.0 \
>   --ontology-graph path/to/extension.ttl \
>   --ontology-graph path/to/extension-shapes.ttl \
>   my-output.jsonld
> ```
>
> See [ECOSYSTEM.md](../ECOSYSTEM.md) for more companion tools.

---

## Recipes

### Starter kits

End-to-end mapping recipes that walk through source input, modeling choices, anti-patterns, and complete runnable code. Start here if you are new to the SDK.

| Recipe | File | Description |
|---|---|---|
| Filesystem Triage Report | [starter-filesystem-report.md](starter-filesystem-report.md) | Map a file listing (names, paths, sizes, hashes) into ObservableObjects with FileFacet + ContentDataFacet |
| Mobile Device Extraction | [starter-mobile-extraction.md](starter-mobile-extraction.md) | Map a mobile extraction (device, apps, messages) with DeviceFacet, MobileDeviceFacet, and SIMCardFacet |
| Email Export | [starter-email-export.md](starter-email-export.md) | Map an email (headers, body, attachments) with EmailMessageFacet and EmailAddressFacet |
| Forensic Tool Run with Provenance | [starter-tool-run.md](starter-tool-run.md) | Map a tool execution with InvestigativeAction, input/output linking, and ProvenanceRecord |

### Forensic workflows

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Modeling a Forensic Tool and Its Output | [forensic-tool.md](forensic-tool.md) | Create an investigation with a tool and investigative action | — |
| Configured Tools | [configured-tool.md](configured-tool.md) | Tool configurations, rulesets, ConfiguredTool | [configured_tool](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/configured_tool) |
| Chain of Custody | [chain-of-custody.md](chain-of-custody.md) | Track evidence handling, transfers, and provenance records | — |
| Forensic Analysis and Classification | [analysis.md](analysis.md) | Malware RE, automated artifact classification with confidence scores | [analysis](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/analysis) |
| AI/ML Analysis Pipelines | [ai-analysis-pipeline.md](ai-analysis-pipeline.md) | Multi-step AI inference, image search, per-result scoring, ranked outputs | — |
| Forensic Investigation Lifecycle | [forensic-lifecycle.md](forensic-lifecycle.md) | Ordered phases (survey, preservation, examination, analysis, reporting) | [forensic_lifecycle](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/forensic_lifecycle) |
| SOLVE-IT Investigation Planning and Error Mitigation | [solve-it-investigation-planning.md](solve-it-investigation-planning.md) | State objectives, select techniques, record `SolveitInvestigativeAction` with `usedTechnique`/`appliedMitigation`, rate weaknesses (ASTM E3016-18) with `WeaknessEvaluation`; punned DFT-* technique classes for the UCO 1.5.0 metaclass style (`solveit` extension) | `solveit` |
| Technique, Evidence, and Legal-Outcome Join | [technique-evidence-outcome.md](technique-evidence-outcome.md) | Join sourced SOLVE-IT techniques, hashed evidence, and `legalproc` outcomes; source-fidelity table for press / PACER / lab / CTI; LE product suggestions stay off the graph until the source names the method | `solveit`, `legalproc` |
| CaseLinker ICAC Remodel | [caselinker-icac-remodel.md](caselinker-icac-remodel.md) | Remodel CaseLinker CAC graphs: CyberTip triggers, share-safe series matches, `legalproc` dual-typing, commander phase clocks, drop private vocab | `cac`, `legalproc` |
| Criminal Discovery and Disclosure | [legal-discovery-disclosure.md](legal-discovery-disclosure.md) | Sourced Brady / Giglio / Jencks / Rule 16 obligations and productions (`legalproc` 0.3.0) | `legalproc` |
| Network Investigation with Bundle | [network-investigation.md](network-investigation.md) | Full investigation with warrant, PCAP extraction, provenance | [network_connection](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/network_connection) |
| Spear Phishing and Attack Narratives | [spear-phishing.md](spear-phishing.md) | Attack chain modeling with extended ontology patterns | [spear_phishing](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/spear_phishing) |
| Fraud, Cryptocurrency, and Money Laundering | [fraud-crypto-laundering.md](fraud-crypto-laundering.md) | Pig-butchering scams, blockchain trace, exchange returns, geofence correlation; typed crypto facets + legal process via the `cryptoinv` extension | — |
| Elder Fraud and Government-Impersonation Schemes | [elder-fraud-impersonation.md](elder-fraud-impersonation.md) | Agent-impersonation call centers, money couriers, prepaid-card and cash-handoff schemes, controlled-delivery stings, records attribution | — |
| Espionage Act and Classified-Information Disclosure | [espionage-classified-disclosure.md](espionage-classified-disclosure.md) | Classified NDI with `uco-marking` classification banners, SCIF removal chains, § 793/§ 794 counts, obstruction, clearance-holder knowledge timeline | — |
| Export Control and Sanctions Evasion | [export-control-sanctions.md](export-control-sanctions.md) | IEEPA/EAR counts, dated Entity List designations, gUFO-typed controlled goods, false EEI/AES filings, papered-consignee vs. true-end-user chains | — |
| Cyber Threat Intelligence and APT Reporting | [cyber-threat-intelligence.md](cyber-threat-intelligence.md) | APT/CTI report + graphics by hash; threat actor as Organization; malware family/variants; native registry persistence (service-DLL *or* fileless registry-buffer); DGA/cloud C2; victimology; ATT&CK via `uco-action:Technique` metaclass (UCO PR #676) | `attack-technique` |
| Insider Threat, Trade Secret Theft, and Economic Espionage | [insider-threat-trade-secrets.md](insider-threat-trade-secrets.md) | Insider exfiltration, corporate detection telemetry, per-category § 1832/§ 1831 counts, foreign-government-benefit evidence, jury verdicts | — |
| Legal Process Modeling (Charges, Verdicts, Sentences) | [legal-process-modeling.md](legal-process-modeling.md) | Conspiracy/attempt/derivative charges, verdicts, pleas, sentences, forfeiture, restitution for any investigation type via the `legalproc` extension | — |
| Racketeering (RICO) and Criminal Enterprise | [racketeering-enterprise.md](racketeering-enterprise.md) | Association-in-fact enterprises, enterprise-role division of labor, predicate statute categories on RICO counts, multi-instrument count suffixes (`rico` extension + `legalproc`/`cryptoinv`) | `rico` |
| Weapons and Drug Evidence | [weapons-drug-evidence.md](weapons-drug-evidence.md) | Firearms/ammunition with make, model, caliber, serial (`weapons` extension, CCO Artifact Ontology + gUFO bridges) and controlled-substance portions with ChEBI identity, CSA schedule, mass, purity basis (`drugs` extension, `gufo:Quantity` bridge) | `weapons`, `drugs` |
| Cargo Theft and Route Staging | [cargo-theft-route-staging.md](cargo-theft-route-staging.md) | Freight theft, geofence deviation, warehouse staging, manifest anomalies | — |
| ICS/SCADA and OT Network Intrusion | [otics-scada-intrusion.md](otics-scada-intrusion.md) | PLC/HMI assets, Modbus/TCP process writes, historian alarms, engineering workstation project files | — |
| NCMEC CyberTip Reporting Workflow | [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md) | Platform detection, ESP reporting, CyberTip lifecycle, and CAC investigation | — |

### Crimes Against Children (CAC Ontology)

Requires `CASE_UCO_EXTENSIONS=cac`. Use `route_cac_content` via the MCP server to detect which recipes apply to submitted content. Validate output with `validate_graph(..., extensions=['cac'])` (uses `ontology/cac/validation-subset.json` by default) or `extensions=['cac:full']` for the complete manifest.

CAC recipes talk about **offenders** who target children and other vulnerable people. MITRE ATT&CK is not CAC community language; it models **hackers** and **attackers**. Do not emit ATT&CK techniques on a CAC graph unless the source describes that rare overlap. Use [cyber-threat-intelligence.md](cyber-threat-intelligence.md) for ATT&CK, and [technique-evidence-outcome.md](technique-evidence-outcome.md) for examiner SOLVE-IT methods.

| Recipe | File | Description |
|---|---|---|
| Child Sex Trafficking and Recruitment Networks | [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) | Solo-operator § 1591, trafficking rings, Grindr bridges, per-victim charge bundles |
| CSAM Forensic Provenance | [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) | Acquisition, custody, hashing, correlation, victim identification |
| CSAM Production Cases | [cac-production-case.md](cac-production-case.md) | Hands-on abuse, offender-produced media, production environments |
| Federal Prosecution Relationships | [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) | Federal indictment relationship wiring: defendant–counts, multi-district, forfeiture, enterprise |
| Federal Trial Proceedings | [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md) | Superseding indictments, PACER docket lifecycle, trial briefs, anticipated evidence |
| PACER Document Ingestion (MCP) | [cac-pacer-document-ingestion.md](cac-pacer-document-ingestion.md) | Agent workflow: process_document_file → route_cac_content → validated CAC graph |
| Hotline Intake and Referral Lifecycle | [cac-hotline-intake-lifecycle.md](cac-hotline-intake-lifecycle.md) | Hotline intake, triage, referral, investigation escalation |
| ICAC Search Warrant Arrest | [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md) | Routine warrant execution, custody without incident, booking (Maryland/ICAC press releases) |
| International Coordination | [cac-international-coordination.md](cac-international-coordination.md) | Cross-border operations, Europol/Interpol, evidence sharing |
| Legal Charges and Sentencing Outcomes | [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) | Indictments, pleas, sentencing, registry outcomes |
| Missing Child Investigations | [cac-missing-child-investigation.md](cac-missing-child-investigation.md) | Missing-child reports, AMBER alerts, tracking, recovery |
| Multi-Jurisdictional Task Force Operations | [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md) | ICAC task forces, joint investigations, jurisdictional handoffs, mass rescue |
| Online Grooming Chat Modeling | [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) | Grooming chat evidence, online sexual solicitation, CAC behavioral interpretation |
| Sextortion and Online Coercion | [cac-sextortion-coercion.md](cac-sextortion-coercion.md) | Sextortion schemes, coercion demands, compliance pressure |
| Tactical Arrest and Undercover Operations | [cac-tactical-undercover-operation.md](cac-tactical-undercover-operation.md) | High-risk arrests, dynamic entry, undercover stings, asset forfeiture |
| Victim Rescue and Post-Rescue Services | [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md) | Emergency response, extraction, safety planning, multi-agency services |

### Devices, locations, and identity

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Device and Workstation Modeling | [device.md](device.md) | Workstation hardware specs, network addresses, OS linking | [device](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/device) |
| Mobile Device and SIM Card | [mobile-device-sim.md](mobile-device-sim.md) | Full handset + SIM + carrier + IMEI/IMSI modeling | [mobile_device_and_sim_card](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/mobile_device_and_sim_card) |
| Mobile Device Forensics | [mobile-device.md](mobile-device.md) | Mobile device extractions, app data, messages, and contacts | — |
| Cell Site and Tower Data | [cell-site.md](cell-site.md) | Cell tower connections, SIM cards, CDR data, location tracking | [cell_site](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/cell_site) |
| Location Modeling | [location.md](location.md) | Street addresses, GPS coordinates, custom location facets | [location](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/location) |
| Multi-Platform Account Linking | [accounts.md](accounts.md) | Cross-platform identity correlation (social media, email, cloud) | [accounts](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/accounts) |
| Events and Authentication Logs | [event.md](event.md) | Authentication events with structured Dictionary attributes | [event](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/event) |
| Windows USN Journal | [usn-journal.md](usn-journal.md) | NTFS change journal entries with structured reason flags, rename modeling, and provenance | — |
| iOS / macOS Sysdiagnose Archives | [ios-sysdiagnose.md](ios-sysdiagnose.md) | Apple sysdiagnose package: device/OS, archive tree, `system_logs.logarchive` as `AppleUnifiedLogArchive`, Wi-Fi/Battery children | `solveit` |
| Apple Unified Logs and Analytic Tool Outputs | [apple-unified-logs.md](apple-unified-logs.md) | Unified log EventRecords + Mandiant iterator CSV, Notari SQLite, iLEAPP reports with SOLVE-IT DFT-1066/1076 provenance | `solveit` |

### Files and data artifacts

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| File System Forensics | [file-system.md](file-system.md) | Model files, directories, and file system metadata | — |
| Advanced File Patterns | [advanced-file-patterns.md](advanced-file-patterns.md) | Archives, encryption, SQLite blobs, nested containment chains | [file](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/file) |
| File Fragments and Multipart Files | [file-fragments.md](file-fragments.md) | Split files, fragment reassembly, embedded data (thumbnails) | [multipart_file](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/multipart_file), [raw_data](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/raw_data) |
| File Recovery and Carving | [file-recovery.md](file-recovery.md) | Carved files, RecoveredObjectFacet, reconstruction workflows | [reconstructed_file](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/reconstructed_file), [recoverability](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/recoverability) |
| Disk Partitions and Volume Recovery | [partitions.md](partitions.md) | Partition tables, volume structures, deleted partition recovery | [partitions](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/partitions) |
| Bulk Extractor Forensic Paths | [bulk-extractor-path.md](bulk-extractor-path.md) | Nested containment, byte offsets, compressed stream extraction | [bulk_extractor_forensic_path](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/bulk_extractor_forensic_path) |
| EXIF and Image Metadata | [exif-data.md](exif-data.md) | Image EXIF tags, camera identification, metadata extraction | [exif_data](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/exif_data) |
| Database Record Extraction | [database-records.md](database-records.md) | SQLite records, table fields, containment relationships | [database_records](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/database_records) |

### Communication artifacts

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Email and Messaging | [email-messaging.md](email-messaging.md) | Email messages, attachments, and messaging platform data | — |
| Threaded Messaging (WhatsApp, Chat) | [threaded-messaging.md](threaded-messaging.md) | Thread/ThreadItem for ordered chat conversations | [message](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/message) |
| Call Log Records | [call-log.md](call-log.md) | Phone call records, carrier accounts, conference bridges | [call_log](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/call_log) |
| SMS Messages and Contacts | [sms-and-contacts.md](sms-and-contacts.md) | SMS/MMS messages, contact entries, account linking | [sms_and_contacts](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/sms_and_contacts) |
| Network Artifact Extraction | [network-artifacts.md](network-artifacts.md) | Network connections, DNS records, IP addresses, and URLs | — |

### SDK patterns and extended ontologies

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Discovering Classes at Runtime | [runtime-discovery.md](runtime-discovery.md) | Use the registry API to search for classes and inspect properties | — |
| Working with Extensions | [extensions.md](extensions.md) | Use extension ontology classes alongside the core SDK | — |
| Cross-Ontology Composition | [cross-ontology-composition.md](cross-ontology-composition.md) | Compose CASE/UCO, extensions, and upper-ontology profiles (BFO/gUFO, PROV-O, Time, GeoSPARQL, FOAF, ORG, PROF) | — |
| Cross-Domain Extensions (redirect) | [cross-domain-extensions.md](cross-domain-extensions.md) | Legacy title; redirects to Cross-Ontology Composition | — |
| Foundational Typing (BFO / gUFO) | [foundational-typing-bfo-gufo.md](foundational-typing-bfo-gufo.md) | Domain-first multi-typing with one foundational profile per graph; CAC prefers gUFO | — |
| PROV-O Evidence Lineage | [prov-o-evidence-lineage.md](prov-o-evidence-lineage.md) | Entity/Activity/Agent enrichment; Tool as instrument; provenance vs acquisition | — |
| OWL-Time Temporal Evidence | [owl-time-temporal-evidence.md](owl-time-temporal-evidence.md) | Native timestamps vs OWL-Time Instant/Interval; open intervals; clock correction | — |
| GeoSPARQL Geospatial Evidence | [geosparql-geospatial-evidence.md](geosparql-geospatial-evidence.md) | Location as geo:Feature; separate Geometry; derived analytics with provenance | — |
| FOAF / ORG Identity and Roles | [foaf-org-identity-roles.md](foaf-org-identity-roles.md) | Person, account, org, membership; no owl:sameAs for uncertain attribution | — |
| PROF Profile Metadata | [prof-validation-profile-metadata.md](prof-validation-profile-metadata.md) | Profile intent vs validation result; serialize bundle metadata | — |
| SOLVE-IT Plan vs Execution | [solveit-plan-execution-provenance.md](solveit-plan-execution-provenance.md) | prov:Plan vs SolveitInvestigativeAction; deviation and re-execution | — |
| Round-Trip: Serialize and Deserialize | [round-trip.md](round-trip.md) | Write a graph to JSON-LD and load it back with typed deserialization | — |
| Managing Large Datasets | [large-datasets.md](large-datasets.md) | Partition large evidence sets by forensic boundary | — |
| Existence Intervals and Temporal Modeling | [existence-intervals.md](existence-intervals.md) | OWL-Time, gUFO, and BFO temporal patterns | [existence_intervals](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/existence_intervals) |

### Contributing to the ontology and the catalog

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Proposing Changes to CASE/UCO | [change-proposal.md](change-proposal.md) | Identify gaps, check existing proposals, and draft change proposals | — |
| Authoring and Improving Recipes | [recipe-authoring.md](recipe-authoring.md) | Write and register a new recipe, or improve an existing one a live case proved wrong or incomplete (structure, grounding rules, re-validation, MCP index registration) | — |
