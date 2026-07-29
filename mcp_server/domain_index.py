"""Domain index for AI-assisted CASE/UCO development.

Maps investigative tasks to SDK classes and provides a searchable recipe index,
optimized for consumption by AI coding agents via MCP tools.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# UCO vs. CASE triage
# ---------------------------------------------------------------------------

CASE_INDICATORS: list[str] = [
    "investigation", "investigative", "forensic lifecycle", "examiner",
    "exhibit", "custody", "authorization", "warrant", "provenance",
    "analyst", "technician", "role", "case metadata", "chain of custody",
    "investigator", "examination", "reporting phase", "case management",
]

UCO_INDICATORS: list[str] = [
    "observable", "facet", "device", "file", "network", "account",
    "identity", "action", "tool", "location", "marking", "pattern",
    "configuration", "hash", "address", "application", "software",
    "email", "message", "url", "domain", "disk", "partition",
    "process", "service", "credential", "browser", "registry",
    "mobile", "sim", "bluetooth", "wifi", "gps", "telemetry",
    "crypto", "malware", "artifact", "content", "data", "log",
]


def suggest_target_repo(concept: str, description: str = "") -> dict[str, str]:
    """Suggest whether a proposed concept belongs in UCO or CASE.

    Returns ``{"suggestion": "UCO"|"CASE"|"unsure", "reasoning": "..."}``.
    """
    text = f"{concept} {description}".lower()

    case_score = sum(1 for kw in CASE_INDICATORS if kw in text)
    uco_score = sum(1 for kw in UCO_INDICATORS if kw in text)

    if case_score > 0 and uco_score == 0:
        return {
            "suggestion": "CASE",
            "reasoning": (
                f"The concept matches investigation-specific indicators "
                f"({', '.join(k for k in CASE_INDICATORS if k in text)}). "
                f"CASE covers concepts specific to the cyber-investigation process."
            ),
        }

    if uco_score > 0 and case_score == 0:
        return {
            "suggestion": "UCO",
            "reasoning": (
                f"The concept matches general cyber-domain indicators "
                f"({', '.join(k for k in UCO_INDICATORS if k in text)}). "
                f"UCO covers observables, identities, actions, and data structures "
                f"with broad utility across the cyber domain."
            ),
        }

    if uco_score > case_score:
        return {
            "suggestion": "UCO",
            "reasoning": (
                f"The concept matches both UCO ({uco_score}) and CASE ({case_score}) "
                f"indicators, but leans toward UCO. UCO covers general cyber-domain "
                f"concepts; CASE covers investigation-specific concepts."
            ),
        }

    if case_score > uco_score:
        return {
            "suggestion": "CASE",
            "reasoning": (
                f"The concept matches both CASE ({case_score}) and UCO ({uco_score}) "
                f"indicators, but leans toward CASE. CASE covers investigation-specific "
                f"concepts; UCO covers general cyber-domain concepts."
            ),
        }

    return {
        "suggestion": "unsure",
        "reasoning": (
            "Unable to determine whether this concept belongs in UCO (general "
            "cyber-domain) or CASE (investigation-specific). Please consider: "
            "Is this concept specific to the process of conducting an investigation "
            "(roles, exhibits, authorization, case metadata)? If so, target CASE. "
            "Is it a general observable, identity, tool, or data structure with "
            "utility beyond investigation? If so, target UCO."
        ),
    }


# ---------------------------------------------------------------------------
# Change proposal template sections
# ---------------------------------------------------------------------------

CHANGE_PROPOSAL_SECTIONS: dict[str, str] = {
    "background": (
        "# Background\n\n"
        "{background}\n"
    ),
    "requirements": (
        "# Requirements\n\n"
        "{requirements}\n"
    ),
    "risk_benefit": (
        "# Risk / Benefit analysis\n\n"
        "## Benefits\n\n{benefits}\n\n"
        "## Risks\n\n{risks}\n"
    ),
    "competencies": (
        "# Competencies demonstrated\n\n"
        "{competencies}\n"
    ),
    "solution": (
        "# Solution suggestion\n\n"
        "{solution}\n"
    ),
}

TASK_TO_CLASSES: dict[str, list[tuple[str, str]]] = {
    "model a forensic disk image extraction": [
        ("Investigation", "The case container"),
        ("InvestigativeAction", "The extraction action performed"),
        ("Tool", "The forensic tool used (e.g., FTK Imager, dd)"),
        ("ObservableObject", "The disk or device being imaged"),
        ("ImageFacet", "Disk image metadata (format, size)"),
        ("FileFacet", "Output image file details"),
        ("ContentDataFacet", "Hash values of the image"),
    ],
    "model mobile app data extraction": [
        ("Investigation", "The case container"),
        ("InvestigativeAction", "The extraction action"),
        ("Tool", "The extraction tool (e.g., Cellebrite, GrayKey)"),
        ("ObservableObject", "The mobile device"),
        ("DeviceFacet", "Device make, model, serial number"),
        ("ApplicationFacet", "The app being examined"),
        ("MessageFacet", "Chat messages found"),
        ("ContactFacet", "Contacts extracted"),
    ],
    "model network traffic capture": [
        ("Investigation", "The case container"),
        ("InvestigativeAction", "The capture action"),
        ("Tool", "The capture tool (e.g., Wireshark, tcpdump)"),
        ("ObservableObject", "Network connection or packet capture"),
        ("NetworkConnectionFacet", "Connection details (src/dst IP, ports)"),
        ("IPAddressFacet", "IP address details"),
        ("DomainNameFacet", "Domain name resolution"),
        ("URLFacet", "URLs observed in traffic"),
    ],
    "model email evidence": [
        ("Investigation", "The case container"),
        ("ObservableObject", "The email message"),
        ("EmailMessageFacet", "Email headers, subject, body"),
        ("EmailAddressFacet", "Sender/recipient addresses"),
        ("EmailAccountFacet", "Email account details"),
        ("ContentDataFacet", "Attachments and content hashes"),
    ],
    "model file system analysis": [
        ("Investigation", "The case container"),
        ("InvestigativeAction", "The analysis action"),
        ("Tool", "The analysis tool (e.g., Autopsy, EnCase)"),
        ("ObservableObject", "Files and directories found"),
        ("FileFacet", "File name, path, size, timestamps"),
        ("ContentDataFacet", "File hash values"),
        ("FileSystemFacet", "File system type and metadata"),
    ],
    "model browser history": [
        ("ObservableObject", "Browser artifact"),
        ("BrowserBookmarkFacet", "Bookmarked URLs"),
        ("URLHistoryFacet", "Browsing history entries"),
        ("URLFacet", "URL details"),
        ("CookieFacet", "Browser cookies"),
        ("ApplicationFacet", "The browser application"),
    ],
    "model chain of custody": [
        ("Investigation", "The case container"),
        ("ProvenanceRecord", "Custody transfer record"),
        ("InvestigativeAction", "Each custody event (receipt, transfer, analysis)"),
        ("Role", "Role of the person in custody chain"),
        ("Identity", "Person involved in custody"),
        ("ObservableObject", "The evidence item"),
    ],
    "model user account activity": [
        ("ObservableObject", "The account"),
        ("AccountFacet", "Account username, creation date"),
        ("DigitalAccountFacet", "Digital account details"),
        ("ApplicationAccountFacet", "App-specific account info"),
        ("Identity", "The account owner"),
    ],
    "model GPS or location data": [
        ("ObservableObject", "The location-bearing artifact"),
        ("LatLongCoordinatesFacet", "GPS coordinates"),
        ("GeoLocationEntryFacet", "Location log entry"),
        ("CellSiteFacet", "Cell tower connection data"),
    ],
    "model fraud or cryptocurrency laundering investigation": [
        ("Investigation", "The case container"),
        ("Person", "Victims, groomers, mules, exchange account holders"),
        ("Organization", "Exchanges and fake investment platforms"),
        ("MessageThread", "Coercion and grooming chat evidence"),
        ("InstantMessagingAddress", "Telegram or messaging handles"),
        ("InvestigativeAction", "Blockchain trace and exchange analysis actions"),
        ("ObservableObject", "Wallet addresses and exchange account IDs"),
        ("Location", "Registered addresses and meetup sites"),
        ("Relationship", "Links between people, wallets, and locations"),
        ("CryptocurrencyAddressFacet", "Blockchain address details (cryptoinv extension)"),
        ("CryptocurrencyTransactionFacet", "On-chain transaction details (cryptoinv extension)"),
        ("CryptocurrencyWalletFacet", "Wallet / address-cluster details (cryptoinv extension)"),
        ("VirtualAssetHoldingFacet", "Point-in-time asset holdings and fiat value (cryptoinv extension)"),
        ("CriminalCharge", "Charged counts with statute citations (cryptoinv extension)"),
        ("ForfeitureOrder", "Forfeited property and money judgments (cryptoinv extension)"),
    ],
    "model violent crime or criminal prosecution": [
        ("Investigation", "The case container (legalproc:caseIdentifier holds the docket number)"),
        ("Person", "Defendants and victims (initials only when charged that way)"),
        ("Organization", "Investigating agencies, prosecuting offices, criminal organizations"),
        ("InvestigativeAction", "Warrant executions, arrests, forensic actions"),
        ("Action", "Criminal conduct (shootings, assaults) distinct from investigative actions"),
        ("ObservableObject", "Digital overt acts: messages, social posts, internet searches"),
        ("Relationship", "Charged_With, Victim_Of, Possessed_By, Member_Of edges"),
        ("ChargingInstrument", "Complaints, indictments, superseding indictments (legalproc extension)"),
        ("CriminalCharge", "Counts with statute, offenseForm (conspiracy/attempt/derivative), disposition (legalproc extension)"),
        ("Verdict", "Guilty / not-guilty findings per charge (legalproc extension)"),
        ("Plea", "Guilty / not-guilty / nolo pleas (legalproc extension)"),
        ("Sentence", "Recommended and imposed sentences, verbatim terms (legalproc extension)"),
        ("ForfeitureOrder", "Forfeited weapons and property (legalproc extension)"),
        ("RestitutionOrder", "Victim compensation amounts (legalproc extension)"),
    ],
    "model cargo theft route staging investigation": [
        ("Investigation", "The case container"),
        ("Vehicle", "Tractors and trailers with telematics identifiers"),
        ("MessageThread", "Route planning communications"),
        ("File", "Manifests and bills of lading"),
        ("Location", "Corridor geofences and staging warehouses"),
        ("Event", "Route deviation or arrival alerts"),
        ("InvestigativeAction", "Geofence analysis and warehouse search"),
        ("Organization", "Carriers and warehouse lessees"),
        ("Relationship", "Links between vehicles, locations, and events"),
    ],
    "model malware analysis": [
        ("Investigation", "The case container"),
        ("InvestigativeAction", "The analysis action"),
        ("Tool", "The analysis tool"),
        ("ObservableObject", "The malware sample"),
        ("FileFacet", "File details of the sample"),
        ("ContentDataFacet", "Hash values"),
        ("WindowsPEBinaryFileFacet", "PE header details"),
        ("OperatingSystemFacet", "Target OS"),
    ],
    "model social media evidence": [
        ("ObservableObject", "Social media content"),
        ("MessageFacet", "Messages or posts"),
        ("AccountFacet", "Social media account"),
        ("ProfileFacet", "User profile data"),
        ("URLFacet", "Links to content"),
        ("ApplicationFacet", "The social media platform"),
    ],
    "model registry or configuration artifacts": [
        ("ObservableObject", "The registry or config artifact"),
        ("WindowsRegistryKeyFacet", "Registry key path and values"),
        ("WindowsRegistryValueFacet", "Specific registry value"),
        ("ConfigurationEntryFacet", "Configuration setting"),
    ],
    "model wireless network evidence": [
        ("ObservableObject", "The wireless network"),
        ("WifiAddressFacet", "WiFi MAC address"),
        ("NetworkConnectionFacet", "Connection details"),
        ("SSIDFacet", "Network name / SSID"),
    ],
    "model a forensic tool and its capabilities": [
        ("Tool", "The forensic tool"),
        ("ObservableObject", "Tool-related observable"),
        ("ConfigurationEntryFacet", "Tool configuration"),
    ],
    "model AI image analysis or ML inference pipeline": [
        ("Investigation", "The case container"),
        ("InvestigativeAction", "Each step in the analysis pipeline (one per model/tool)"),
        ("AnalyticTool", "The AI/ML model or analysis tool"),
        ("RasterPicture", "Image files (use instead of File for .jpg, .png, etc.)"),
        ("RasterPictureFacet", "Image dimensions, compression, picture type"),
        ("FileFacet", "Filename, path, size, timestamps"),
        ("ContentDataFacet", "Hashes and MIME type for evidentiary integrity"),
        ("ConfidenceFacet", "Per-result similarity/confidence score"),
        ("Relationship", "Explicit input/output links (Selected_From, Derived_From)"),
        ("ProvenanceRecord", "Groups the pipeline and its artifacts"),
    ],
    "model digital evidence for court": [
        ("Investigation", "The case container"),
        ("ProvenanceRecord", "Provenance and chain of custody"),
        ("InvestigativeAction", "Each forensic step taken"),
        ("Tool", "Tools used with version information"),
        ("ObservableObject", "Evidence items"),
        ("ContentDataFacet", "Hash values for integrity verification"),
    ],
    "model online grooming and cybertip workflow": [
        ("CACInvestigation", "The CAC-specific investigation container (from cac extension)"),
        ("GroomingBehavior", "The grooming behavior event with phases (from cac extension)"),
        ("OnlineGrooming", "Online grooming behavior subclass (from cac extension)"),
        ("GroomingMessage", "Grooming-specific message with explicitness/tone (from cac extension)"),
        ("ChildVictim", "Child victim role with vulnerability modeling (from cac extension)"),
        ("OnlinePredator", "Online predator role (from cac extension)"),
        ("NCMECCybertipReport", "NCMEC CyberTipline report structure (from cac extension)"),
        ("OnlineEnticementIncident", "NCMEC incident type for enticement (from cac extension)"),
        ("MessageThread", "Core UCO chat thread container"),
        ("MessageFacet", "Core UCO message metadata"),
        ("ApplicationAccount", "Core UCO social media account"),
        ("RasterPicture", "Core UCO image for CSAM evidence"),
        ("Relationship", "Core UCO links between entities"),
    ],
    "model child sex trafficking ring or recruitment network": [
        ("CACInvestigation", "The CAC investigation container (from cac extension)"),
        ("TraffickingEnterprise", "Trafficking ring / network organization (from cac extension)"),
        ("TraffickingRing", "Specific ring structure with role hierarchy (from cac extension)"),
        ("TraffickingCell", "Sub-cell within a ring (from cac extension)"),
        ("TraffickingVictimRole", "Victim role in the trafficking enterprise (from cac extension)"),
        ("MinorTraffickingVictimRole", "Minor-specific trafficking victim role (from cac extension)"),
        ("TraffickingVictimRescue", "Rescue event tied to a trafficking victim (from cac extension)"),
        ("VictimRotation", "Movement of victims between locations/buyers (from cac extension)"),
        ("InterstateVictimTransport", "Cross-state movement of victims (from cac extension)"),
        ("InterstateTraffickingNetwork", "Trafficking network spanning multiple states (from cac extension)"),
        ("PeerRecruitmentNetwork", "Peer-to-peer recruitment chains (from cac extension)"),
        ("ClassmateRecruitmentNetwork", "Classmate-to-classmate recruitment chains (from cac extension)"),
        ("SchoolBasedRecruitment", "Recruitment occurring at or via schools (from cac extension)"),
        ("StreetBasedRecruitment", "Pretext-based street recruitment (from cac extension)"),
        ("HelpOfferApproach", "'Need help?' pretext approach (from cac extension)"),
        ("FoodOfferApproach", "Food-offer pretext approach (from cac extension)"),
        ("TransportationOfferApproach", "Transportation-offer pretext approach (from cac extension)"),
        ("PhoneChargingOffer", "Phone-charging pretext approach (from cac extension)"),
        ("RapidEscalationRecruitment", "Compressed-timeline recruitment pattern (from cac extension)"),
        ("DigitalToPhysicalBridge", "Online-to-offline meet event (from cac extension)"),
        ("MandatoryReportingActivation", "Triggering of mandatory-reporter obligations (from cac extension)"),
        ("Identity", "Core UCO identity for traffickers, recruiters, victims"),
        ("Relationship", "Core UCO link between participants and the enterprise"),
    ],
    "model multi-jurisdictional task force operation or rescue": [
        ("CACInvestigation", "The CAC investigation container (from cac extension)"),
        ("Jurisdiction", "Jurisdiction at any level (from cac extension)"),
        ("LocalJurisdiction", "City/county-level jurisdiction (from cac extension)"),
        ("StateJurisdiction", "State-level jurisdiction (from cac extension)"),
        ("FederalJurisdiction", "Federal jurisdiction (e.g., FBI, HSI) (from cac extension)"),
        ("InternationalJurisdiction", "Cross-border jurisdiction (from cac extension)"),
        ("TaskForce", "Multi-agency task force (e.g., ICAC) (from cac extension)"),
        ("JointInvestigation", "Investigation spanning agencies (from cac extension)"),
        ("JurisdictionalHandoff", "Transfer of investigative lead between agencies (from cac extension)"),
        ("MutualAidRequest", "Cross-jurisdiction request for assistance (from cac extension)"),
        ("MassChildRescueOperation", "Coordinated multi-victim rescue (from cac extension)"),
        ("InvestigativeAction", "Core CASE action for each operational step"),
        ("ProvenanceRecord", "Provenance binding the operation's evidence"),
    ],
    "model tactical arrest or high-risk operation": [
        ("CACInvestigation", "The CAC investigation container (from cac extension)"),
        ("ArrestOperation", "Arrest operation event (from cac extension)"),
        ("HighRiskArrest", "High-risk arrest sub-type (from cac extension)"),
        ("DynamicEntry", "Forced/dynamic entry event (from cac extension)"),
        ("SuspectProfile", "Pre-operation suspect threat/profile (from cac extension)"),
        ("ThreatAssessment", "Pre-operation threat assessment (from cac extension)"),
        ("UndercoverOperation", "Undercover operation context (from cac extension)"),
        ("AssetForfeitureAction", "Property seizure tied to CSE/trafficking (from cac extension)"),
        ("InvestigativeAction", "Core CASE action wrapper"),
        ("Tool", "Core UCO tool for tactical equipment, where applicable"),
        ("Identity", "Core UCO identity for officers and suspects"),
    ],
    "model victim rescue extraction and post-rescue services": [
        ("CACInvestigation", "The CAC investigation container (from cac extension)"),
        ("EmergencyResponse", "Initial emergency response to identified victim (from cac extension)"),
        ("VictimExtraction", "Physical extraction of a victim (from cac extension)"),
        ("OngoingDangerAssessment", "Post-rescue danger assessment (from cac extension)"),
        ("SafetyPlanning", "Victim safety plan (from cac extension)"),
        ("MultiAgencyVictimResponse", "DCFS / medical / mental-health coordination (from cac extension)"),
        ("TraumaIndicator", "Observed trauma indicator on victim (from cac extension)"),
        ("HelpSeekingBarrier", "Barrier preventing victim from seeking help (from cac extension)"),
        ("RecantationAssessment", "Victim recantation assessment (from cac extension)"),
        ("PartialRecantationStatement", "Partial recantation statement (from cac extension)"),
        ("ReaffirmedDisclosureStatement", "Disclosure reaffirmed after pressure to recant (from cac extension)"),
        ("PostRecantationForensicInterview", "Forensic interview following recantation (from cac extension)"),
        ("ChildVictim", "Child victim role with vulnerability modeling (from cac extension)"),
        ("InvestigativeAction", "Core CASE action wrapper"),
    ],
    "model CSAM provenance forensics and victim identification": [
        ("ForensicAcquisitionAction", "Forensic acquisition of CSAM evidence (from cac extension)"),
        ("ChainOfCustodyAction", "Each chain-of-custody event (from cac extension)"),
        ("EvidenceVerificationAction", "Hash/signature verification (from cac extension)"),
        ("MetadataCorrelation", "EXIF / file-system / app metadata correlation (from cac extension)"),
        ("TemporalPatternAnalysis", "Temporal-pattern analysis across artifacts (from cac extension)"),
        ("GeospatialCorrelation", "Geospatial correlation of CSAM/related evidence (from cac extension)"),
        ("CrossPlatformCorrelation", "Same actor/victim across multiple platforms (from cac extension)"),
        ("BehavioralFingerprinting", "Behavioral pattern fingerprinting of an offender (from cac extension)"),
        ("VictimIdentificationProcess", "Victim ID workflow against known-victim data (from cac extension)"),
        ("ContentHashingTool", "PhotoDNA / perceptual hashing tool (from cac extension)"),
        ("RasterPicture", "Core UCO image for the CSAM artifact"),
        ("ContentDataFacet", "Core UCO hashes for evidentiary integrity"),
        ("ProvenanceRecord", "Core CASE provenance record"),
        ("Relationship", "Core UCO links between artifacts, actors, and actions"),
    ],
    "model CSAM detection and platform reporting to NCMEC": [
        ("AutomatedDetectionAction", "Platform CSAM detection action (from cac extension)"),
        ("ContentHashingTool", "PhotoDNA or perceptual hashing tool (from cac extension)"),
        ("MachineLearningDetectionTool", "ML-based CSAM classifier (from cac extension)"),
        ("DetectionResult", "Detection confidence and classification (from cac extension)"),
        ("NCMECCybertipReport", "NCMEC CyberTipline report (from cac extension)"),
        ("PlatformCooperation", "ESP cooperation with law enforcement (from cac extension)"),
        ("ElectronicServiceProvider", "The reporting platform organization (from cac extension)"),
        ("ContentModerationAction", "Platform content moderation event (from cac extension)"),
        ("InvestigativeAction", "Core CASE investigative action"),
        ("AnalyticTool", "Core UCO analytic tool"),
    ],
}

DOMAIN_CATEGORIES: list[dict[str, Any]] = [
    {
        "name": "files_and_filesystem",
        "title": "Files and Filesystem",
        "description": "Files, directories, file systems, and their metadata.",
        "keywords": ["file", "path", "directory", "content", "filesystem", "volume",
                     "disk", "partition", "ntfs", "ext", "fragment"],
    },
    {
        "name": "network_activity",
        "title": "Network Activity",
        "description": "Network connections, IP addresses, DNS records, URLs, and traffic captures.",
        "keywords": ["network", "ip", "address", "dns", "url", "domain", "tcp", "udp",
                     "http", "socket", "connection", "port", "packet"],
    },
    {
        "name": "devices_and_hardware",
        "title": "Devices and Hardware",
        "description": "Computers, phones, storage devices, and hardware components.",
        "keywords": ["device", "computer", "phone", "sim", "storage", "hardware",
                     "disk", "usb", "bluetooth"],
    },
    {
        "name": "applications_and_software",
        "title": "Applications and Software",
        "description": "Software applications, operating systems, and installed programs.",
        "keywords": ["application", "software", "operating system", "browser",
                     "program", "process", "service"],
    },
    {
        "name": "user_accounts_and_identity",
        "title": "User Accounts and Identity",
        "description": "User accounts, digital identities, authentication credentials.",
        "keywords": ["account", "identity", "user", "credential", "authentication",
                     "password", "profile", "digital account"],
    },
    {
        "name": "email_and_messaging",
        "title": "Email and Messaging",
        "description": "Email messages, chat messages, SMS, and messaging platforms.",
        "keywords": ["email", "message", "sms", "chat", "attachment", "messaging",
                     "calendar", "contact"],
    },
    {
        "name": "mobile_forensics",
        "title": "Mobile Forensics",
        "description": "Mobile device data, apps, call logs, GPS, and cell tower data.",
        "keywords": ["mobile", "phone", "call", "sms", "gps", "location", "cell",
                     "sim", "app", "android", "ios", "wifi"],
    },
    {
        "name": "actions_and_events",
        "title": "Actions and Events",
        "description": "Investigative actions, tool runs, observations, analysis events, and AI/ML inference pipelines.",
        "keywords": ["action", "event", "observation", "analysis", "pattern",
                     "lifecycle", "pipeline", "inference", "ai", "ml",
                     "prediction", "detection"],
    },
    {
        "name": "investigation_metadata",
        "title": "Investigation Metadata",
        "description": "Investigations, case metadata, provenance, and authorization.",
        "keywords": ["investigation", "case", "provenance", "authorization",
                     "exhibit", "custody"],
    },
    {
        "name": "child_exploitation",
        "title": "Child Exploitation and Crimes Against Children",
        "description": "Online grooming, CSAM detection, CyberTip reports, NCMEC workflows, sextortion, victim identification, and platform reporting.",
        "keywords": ["child", "csam", "grooming", "ncmec", "cybertip", "exploitation",
                     "victim", "offender", "enticement", "sextortion", "predator",
                     "minor", "abuse", "production", "hotline", "cac",
                     "icac", "crimes against children"],
    },
    {
        "name": "child_trafficking",
        "title": "Child Sex Trafficking and Exploitation Networks",
        "description": (
            "Trafficking rings, cells, and role hierarchies; victim rotation and "
            "interstate transport; recruitment networks (school-based, peer, "
            "street pretexts such as help/food/transportation/phone-charging "
            "offers); rapid-escalation recruitment; vulnerability indicators; "
            "digital-to-physical bridge events; mass child rescue operations."
        ),
        "keywords": ["trafficking", "traffic", "trafficker", "trafficked",
                     "ring", "cell", "rotation", "transport", "interstate",
                     "recruitment", "recruit", "recruiter", "pretext",
                     "school-based", "peer", "street", "vulnerability",
                     "digital-to-physical", "bridge", "rescue",
                     "mass rescue", "csec", "cse"],
    },
    {
        "name": "victim_rescue_response",
        "title": "Victim Rescue, Extraction, and Post-Rescue Response",
        "description": (
            "Emergency response to identified victims, victim extraction, "
            "ongoing-danger and threat assessments, safety planning, "
            "trauma indicators, help-seeking barriers, recantation, and "
            "multi-agency victim response (DCFS, medical, mental health)."
        ),
        "keywords": ["rescue", "extraction", "extract", "emergency",
                     "safety", "safe", "trauma", "victim impact",
                     "victim service", "victim response", "recantation",
                     "danger", "threat assessment", "help-seeking",
                     "multi-agency", "dcfs", "child protective"],
    },
    {
        "name": "multi_jurisdictional_operations",
        "title": "Multi-Jurisdictional Operations and Task Forces",
        "description": (
            "Local/State/Federal/International jurisdictions, joint "
            "investigations, ICAC and HSI task forces, jurisdictional "
            "handoffs, mutual aid requests, federal/state legal "
            "harmonization, and international cooperation."
        ),
        "keywords": ["jurisdiction", "jurisdictional", "multi-jurisdiction",
                     "taskforce", "task force", "joint investigation",
                     "joint operation", "handoff", "mutual aid",
                     "federal", "state", "local", "international",
                     "interpol", "hsi", "fbi", "icac", "harmonization",
                     "cooperation"],
    },
    {
        "name": "tactical_operations",
        "title": "Tactical and Arrest Operations",
        "description": (
            "Arrest operations (high-risk and standard), dynamic entry, "
            "suspect profiling, threat assessment, undercover operations, "
            "specialized units, and asset forfeiture tied to CSE/trafficking."
        ),
        "keywords": ["tactical", "arrest", "high-risk", "dynamic entry",
                     "suspect profile", "undercover", "specialized unit",
                     "swat", "warrant service", "asset forfeiture",
                     "seizure", "operation", "raid"],
    },
    {
        "name": "csam_provenance",
        "title": "CSAM Forensics, Chain of Custody, and Provenance",
        "description": (
            "Forensic acquisition of CSAM evidence, chain-of-custody actions, "
            "evidence verification, metadata correlation, temporal pattern "
            "analysis, geospatial correlation, cross-platform correlation, "
            "behavioral fingerprinting, and victim identification processes."
        ),
        "keywords": ["acquisition", "chain of custody", "evidence verification",
                     "metadata correlation", "temporal pattern",
                     "geospatial correlation", "cross-platform",
                     "behavioral fingerprint", "victim identification",
                     "provenance", "csam forensic", "image hashing",
                     "perceptual hash", "photodna"],
    },
    {
        "name": "tool_information",
        "title": "Tool Information",
        "description": "Forensic and analysis tools, AI/ML models, their versions, and configurations.",
        "keywords": ["tool", "version", "configuration", "build", "model",
                     "analytic", "classifier", "neural", "embedding"],
    },
    {
        "name": "time_and_temporal",
        "title": "Time and Temporal Data",
        "description": "Timestamps, time ranges, and temporal relationships.",
        "keywords": ["time", "date", "timestamp", "temporal", "instant", "interval"],
    },
    {
        "name": "marking_and_access_control",
        "title": "Marking and Access Control",
        "description": "Data markings, classification, TLP, and access restrictions.",
        "keywords": ["marking", "classification", "tlp", "access", "license",
                     "restriction"],
    },
]

UCO_PROFILES: list[dict[str, Any]] = [
    {
        "id": "bfo",
        "name": "CDO-Shapes-BFO",
        "full_name": "Basic Formal Ontology (BFO 2020)",
        "ontology_url": "https://github.com/BFO-ontology/BFO-2020",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-BFO",
        "profile_type": "top-level",
        "ontology_file": "uco-bfo.ttl",
        "local_source": "ontology/upper/bfo.owl",
        "local_shapes": "ontology/upper/shapes/sh-bfo.ttl",
        "status": "exploratory",
        "description": (
            "Grounds UCO in BFO's Endurant/Perdurant distinction. "
            "Useful for formal reasoning, biomedical and scientific ontology interop."
        ),
        "keywords": ["bfo", "foundational", "upper", "top-level", "endurant",
                      "perdurant", "formal", "reasoning", "biomedical", "scientific"],
        "related_domains": ["actions_and_events", "time_and_temporal"],
        "related_recipes": ["docs/recipes/foundational-typing-bfo-gufo.md",
                            "docs/recipes/existence-intervals.md"],
        "extension_compatibility": {
            "cac": "not_recommended",
            "aeo": "compatible",
        },
    },
    {
        "id": "gufo",
        "name": "CDO-Shapes-gufo",
        "full_name": "gentle Unified Foundational Ontology (gUFO)",
        "ontology_url": "https://github.com/nemo-ufes/gufo",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-gufo",
        "profile_type": "top-level",
        "ontology_file": "uco-gufo.ttl",
        "local_source": "ontology/upper/gufo.ttl",
        "local_shapes": "ontology/upper/shapes/sh-gufo.ttl",
        "status": "exploratory",
        "description": (
            "Grounds UCO in gUFO types and relators (OntoUML-based). "
            "The CAC Ontology extends both UCO/CASE and gUFO."
        ),
        "keywords": ["gufo", "ontouml", "foundational", "upper", "top-level",
                      "relator", "cac", "children", "project vic"],
        "related_domains": ["actions_and_events", "time_and_temporal"],
        "related_recipes": ["docs/recipes/foundational-typing-bfo-gufo.md",
                            "docs/recipes/existence-intervals.md"],
        "extension_compatibility": {
            "cac": "included",
            "aeo": "compatible",
        },
    },
    {
        "id": "prov-o",
        "name": "CDO-Shapes-PROV-O",
        "full_name": "W3C PROV-O (Provenance Ontology)",
        "ontology_url": "https://www.w3.org/TR/prov-o/",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-PROV-O",
        "profile_type": "adopting",
        "ontology_file": "uco-prov-o.ttl",
        "local_source": "ontology/upper/prov-o.ttl",
        "local_shapes": "ontology/upper/shapes/sh-prov-o.ttl",
        "status": "exploratory",
        "description": (
            "Aligns UCO actions and provenance concepts with PROV-O Activities, "
            "Entities, and Agents for W3C provenance tooling interop."
        ),
        "keywords": ["provenance", "prov-o", "prov", "w3c", "activity", "entity",
                      "agent", "custody", "chain", "lineage", "derivation"],
        "related_domains": ["investigation_metadata", "actions_and_events"],
        "related_recipes": ["docs/recipes/prov-o-evidence-lineage.md",
                            "docs/recipes/chain-of-custody.md"],
        "extension_compatibility": {
            "cac": "compatible",
            "aeo": "compatible",
        },
    },
    {
        "id": "time",
        "name": "CDO-Shapes-Time",
        "full_name": "W3C OWL-Time",
        "ontology_url": "https://www.w3.org/TR/owl-time/",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-Time",
        "profile_type": "adopting",
        "ontology_file": "uco-time.ttl",
        "local_source": "ontology/upper/time.ttl",
        "local_shapes": "ontology/upper/shapes/sh-time.ttl",
        "status": "exploratory",
        "description": (
            "Aligns UCO temporal concepts with OWL-Time instants and intervals "
            "for temporal reasoning, calendar/clock time modeling."
        ),
        "keywords": ["time", "temporal", "owl-time", "w3c", "instant", "interval",
                      "duration", "calendar", "clock", "period"],
        "related_domains": ["time_and_temporal"],
        "related_recipes": ["docs/recipes/owl-time-temporal-evidence.md",
                            "docs/recipes/existence-intervals.md"],
        "extension_compatibility": {
            "cac": "compatible",
            "aeo": "compatible",
        },
    },
    {
        "id": "geosparql",
        "name": "CDO-Shapes-GeoSPARQL",
        "full_name": "OGC GeoSPARQL 1.1",
        "ontology_url": "https://github.com/opengeospatial/ogc-geosparql",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-GeoSPARQL",
        "profile_type": "adopting",
        "ontology_file": "uco-geo.ttl",
        "local_source": "ontology/upper/geo.ttl",
        "local_shapes": "ontology/upper/shapes/sh-geo.ttl",
        "status": "exploratory",
        "description": (
            "Aligns UCO locations with GeoSPARQL Features and Geometries "
            "for geospatial queries, CRS, and spatial reasoning."
        ),
        "keywords": ["geosparql", "geospatial", "geo", "spatial", "gps",
                      "location", "coordinate", "geometry", "feature", "ogc", "gis"],
        "related_domains": ["mobile_forensics"],
        "related_recipes": ["docs/recipes/geosparql-geospatial-evidence.md",
                            "docs/recipes/location.md", "docs/recipes/cell-site.md"],
        "extension_compatibility": {
            "cac": "compatible",
            "aeo": "compatible",
        },
    },
    {
        "id": "foaf",
        "name": "CDO-Shapes-FOAF",
        "full_name": "Friend-of-a-Friend (FOAF)",
        "ontology_url": "http://xmlns.com/foaf/0.1/",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-FOAF",
        "profile_type": "adopting",
        "ontology_file": "uco-foaf.ttl",
        "local_source": "ontology/upper/foaf.rdf",
        "local_shapes": "ontology/upper/shapes/sh-foaf.ttl",
        "status": "exploratory",
        "description": (
            "Aligns UCO identities with FOAF Persons, Organizations, and Agents "
            "for social network data and Linked Data interop."
        ),
        "keywords": ["foaf", "friend", "social", "identity", "person",
                      "organization", "agent", "linked data", "social network"],
        "related_domains": ["user_accounts_and_identity"],
        "related_recipes": ["docs/recipes/foaf-org-identity-roles.md",
                            "docs/recipes/accounts.md"],
        "extension_compatibility": {
            "cac": "compatible",
            "aeo": "compatible",
        },
    },
    {
        "id": "org",
        "name": "CDO-Shapes-ORG",
        "full_name": "W3C Organization Ontology (ORG)",
        "ontology_url": "https://www.w3.org/TR/vocab-org/",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-ORG",
        "profile_type": "adopting",
        "ontology_file": "uco-org.ttl",
        "local_source": "ontology/upper/org.ttl",
        "local_shapes": "ontology/upper/shapes/sh-org.ttl",
        "status": "exploratory",
        "description": (
            "Aligns UCO organizations, memberships, and posts with the W3C ORG "
            "vocabulary for agencies, task forces, and corporate structure."
        ),
        "keywords": ["org", "organization", "membership", "post", "unit",
                      "agency", "task force", "employer", "w3c"],
        "related_domains": ["user_accounts_and_identity"],
        "related_recipes": ["docs/recipes/foaf-org-identity-roles.md"],
        "extension_compatibility": {
            "cac": "compatible",
            "aeo": "compatible",
        },
    },
    {
        "id": "prof",
        "name": "CDO-Shapes-PROF",
        "full_name": "W3C Profiles Vocabulary (PROF)",
        "ontology_url": "https://www.w3.org/TR/dx-prof/",
        "repo_url": "https://github.com/Cyber-Domain-Ontology/CDO-Shapes-PROF",
        "profile_type": "adopting",
        "ontology_file": "uco-prof.ttl",
        "local_source": "ontology/upper/prof.ttl",
        "local_shapes": "ontology/upper/shapes/sh-prof.ttl",
        "status": "exploratory",
        "description": (
            "Declares the ontology/profile bundle a graph is intended to satisfy "
            "and records validation resources without treating PROF as conformance proof."
        ),
        "keywords": ["prof", "profile", "validation", "metadata", "bundle",
                      "shapes", "conformance", "w3c", "dx-prof"],
        "related_domains": ["investigation_metadata"],
        "related_recipes": ["docs/recipes/prof-validation-profile-metadata.md"],
        "extension_compatibility": {
            "cac": "compatible",
            "aeo": "compatible",
        },
    },
]

CORE_PATTERNS: list[dict[str, str]] = [
    {
        "name": "ObservableObject + Facets",
        "description": (
            "The most common pattern. Create an ObservableObject and attach "
            "one or more Facets to describe it. A single observable can have "
            "multiple facets (e.g., FileFacet + ContentDataFacet for a file "
            "with its hash)."
        ),
        "python_example": (
            "graph.create(ObservableObject, has_facet=[\n"
            "    FileFacet(file_name='evidence.dd', size_in_bytes=1073741824),\n"
            "    ContentDataFacet(hash_method='SHA-256', hash_value='abc123...'),\n"
            "])"
        ),
    },
    {
        "name": "Investigation + Action + Tool",
        "description": (
            "Model a forensic workflow: an Investigation contains "
            "InvestigativeActions, each performed by a Tool that produces "
            "ObservableObjects as output."
        ),
        "python_example": (
            "inv = graph.create(Investigation, name='Case 2024-001')\n"
            "tool = graph.create(Tool, name='Autopsy', version='4.21.0')\n"
            "action = graph.create(InvestigativeAction, name='Disk analysis')"
        ),
    },
    {
        "name": "Identity + Role",
        "description": (
            "Associate a person or organization with a role in the "
            "investigation (examiner, subject, witness)."
        ),
        "python_example": (
            "person = graph.create(Identity, name='Jane Smith')\n"
            "role = graph.create(Role, name='Lead Examiner')"
        ),
    },
    {
        "name": "Provenance + Chain of Custody",
        "description": (
            "Track evidence handling with ProvenanceRecord and sequential "
            "InvestigativeActions for each custody event."
        ),
        "python_example": (
            "record = graph.create(ProvenanceRecord,\n"
            "    description='Evidence received from field office')"
        ),
    },
]

RECIPE_INDEX: list[dict[str, str]] = [
    {
        "title": "Modeling a Forensic Tool and Its Output",
        "description": "Create an investigation with a tool and investigative action.",
        "keywords": "tool investigation action forensic workflow",
        "file": "docs/recipes/forensic-tool.md",
    },
    {
        "title": "File System Forensics",
        "description": "Model files, directories, and file system metadata from a disk analysis.",
        "keywords": "file directory filesystem disk analysis extraction",
        "file": "docs/recipes/file-system.md",
    },
    {
        "title": "Network Artifact Extraction",
        "description": "Model network connections, DNS records, IP addresses, and URLs.",
        "keywords": "network dns ip url connection traffic capture packet",
        "file": "docs/recipes/network-artifacts.md",
    },
    {
        "title": "Mobile Device Forensics",
        "description": "Model mobile device extractions, app data, messages, and contacts.",
        "keywords": "mobile phone device app message contact sms call cellebrite graykey",
        "file": "docs/recipes/mobile-device.md",
    },
    {
        "title": "Email and Messaging",
        "description": "Model email messages, attachments, and messaging platform data.",
        "keywords": "email message attachment chat messaging calendar",
        "file": "docs/recipes/email-messaging.md",
    },
    {
        "title": "Chain of Custody",
        "description": "Track evidence handling, transfers, and provenance records.",
        "keywords": "custody chain provenance evidence handling transfer",
        "file": "docs/recipes/chain-of-custody.md",
    },
    {
        "title": "Discovering Classes at Runtime",
        "description": "Use the registry API to search for classes and inspect their properties.",
        "keywords": "search discover find class registry introspection",
        "file": "docs/recipes/runtime-discovery.md",
    },
    {
        "title": "Working with Extensions",
        "description": "Use extension ontology classes alongside the core SDK.",
        "keywords": "extension custom ontology scaffold toolcap",
        "file": "docs/recipes/extensions.md",
    },
    {
        "title": "Round-Trip: Serialize and Deserialize",
        "description": "Write a graph to JSON-LD and load it back with typed deserialization.",
        "keywords": "serialize deserialize load save round-trip json-ld",
        "file": "docs/recipes/round-trip.md",
    },
    {
        "title": "Managing Large Datasets",
        "description": "Partition large evidence sets by forensic boundary, estimate graph sizes.",
        "keywords": "large dataset partition split merge performance volume",
        "file": "docs/recipes/large-datasets.md",
    },
    {
        "title": "Call Log Records",
        "description": "Model phone call records, carrier accounts, and conference bridges.",
        "keywords": "call log phone carrier voip conference bridge dialer incoming outgoing missed",
        "file": "docs/recipes/call-log.md",
    },
    {
        "title": "SMS Messages and Contacts",
        "description": "Model SMS/MMS messages and contact list entries with account linking.",
        "keywords": "sms mms text message contact phone number account sim",
        "file": "docs/recipes/sms-and-contacts.md",
    },
    {
        "title": "EXIF and Image Metadata",
        "description": "Model image files with EXIF metadata, camera identification, and provenance.",
        "keywords": "exif image photo jpeg camera metadata gps picture raster",
        "file": "docs/recipes/exif-data.md",
    },
    {
        "title": "Database Record Extraction",
        "description": "Model SQLite records, table fields, and containment relationships.",
        "keywords": "database sqlite record table field row column wal journal sql",
        "file": "docs/recipes/database-records.md",
    },
    {
        "title": "Cell Site and Tower Data",
        "description": "Model cell tower connections, SIM cards, CDR data, and location tracking.",
        "keywords": "cell site tower cdr sim card imei imsi carrier antenna location tracking mobile",
        "file": "docs/recipes/cell-site.md",
    },
    {
        "title": "Forensic Analysis and Artifact Classification",
        "description": "Model malware analysis, automated classification with confidence scores.",
        "keywords": "analysis malware reverse engineering classification confidence artifact yara ida",
        "file": "docs/recipes/analysis.md",
    },
    {
        "title": "AI/ML Analysis Pipelines",
        "description": "Model AI/ML analysis workflows — multi-step inference, image search, per-result scoring, ranked outputs, and full provenance.",
        "keywords": "ai ml machine learning inference pipeline image search semantic embedding clip model scoring ranking similarity confidence raster picture photo detection prediction neural network",
        "file": "docs/recipes/ai-analysis-pipeline.md",
    },
    {
        "title": "Multi-Platform Account Linking",
        "description": "Model cross-platform identity correlation across social media, email, and cloud accounts.",
        "keywords": "account identity person facebook google email digital platform social media linking",
        "file": "docs/recipes/accounts.md",
    },
    {
        "title": "Configured Tools",
        "description": "Model forensic tools with specific configurations, command-line flags, and rulesets.",
        "keywords": "configured tool configuration ruleset flag parameter ida volatility",
        "file": "docs/recipes/configured-tool.md",
    },
    {
        "title": "Device and Workstation Modeling",
        "description": "Model computers and workstations with hardware specs, network addresses, and OS.",
        "keywords": "device workstation computer hardware cpu ram bios hostname ip address server desktop",
        "file": "docs/recipes/device.md",
    },
    {
        "title": "Events and Authentication Logs",
        "description": "Model authentication events, login/logout actions, and system events.",
        "keywords": "event authentication login logout mfa credential session log audit",
        "file": "docs/recipes/event.md",
    },
    {
        "title": "Location Modeling",
        "description": "Model geospatial locations with street addresses and GPS coordinates.",
        "keywords": "location address gps latitude longitude coordinates geolocation place site",
        "file": "docs/recipes/location.md",
    },
    {
        "title": "Advanced File Patterns",
        "description": "Model archives, encryption, SQLite blobs, and nested containment chains.",
        "keywords": "archive tar zip encrypted encoded base64 sqlite blob nested containment layer stream",
        "file": "docs/recipes/advanced-file-patterns.md",
    },
    {
        "title": "File Fragments and Multipart Files",
        "description": "Model split files, fragment reassembly, and embedded data like thumbnails.",
        "keywords": "fragment multipart split carve reassemble thumbnail embedded raw data",
        "file": "docs/recipes/file-fragments.md",
    },
    {
        "title": "File Recovery and Carving",
        "description": "Model recovered and carved files with recovery status and reconstruction workflows.",
        "keywords": "recovery carve carved reconstruct recovered scalpel photorec foremost deleted",
        "file": "docs/recipes/file-recovery.md",
    },
    {
        "title": "Windows Thumbnail Cache",
        "description": "Model thumbnails recovered from Windows Explorer thumbcache_*.db databases, keyed by ThumbnailCacheID, including images whose original files were deleted from the volume.",
        "keywords": "thumbnail thumbcache thumbcache.db thumbnail cache windows explorer cache deleted image recovery iconcache ThumbnailCacheID CMMM size bucket raster picture recovered object",
        "file": "docs/recipes/windows-thumbnail-cache.md",
    },
    {
        "title": "Threaded Messaging (WhatsApp, Chat)",
        "description": "Model ordered chat conversations with threads, participants, and attachments.",
        "keywords": "thread chat whatsapp messenger conversation participant attachment media social",
        "file": "docs/recipes/threaded-messaging.md",
    },
    {
        "title": "Mobile Device and SIM Card",
        "description": "Model a mobile handset with SIM card, carrier, IMEI/IMSI, and OS.",
        "keywords": "mobile device sim card imei imsi iccid carrier bluetooth wifi mac handset smartphone",
        "file": "docs/recipes/mobile-device-sim.md",
    },
    {
        "title": "Network Investigation with Bundle",
        "description": "Model a complete network investigation with warrant, PCAP extraction, and provenance.",
        "keywords": "network investigation bundle warrant authorization pcap capture connection host",
        "file": "docs/recipes/network-investigation.md",
    },
    {
        "title": "Forensic Investigation Lifecycle",
        "description": "Model ordered investigation phases: survey, preservation, examination, analysis, reporting.",
        "keywords": "lifecycle phase survey preservation examination analysis reporting ordered action",
        "file": "docs/recipes/forensic-lifecycle.md",
    },
    {
        "title": "Disk Partitions and Volume Recovery",
        "description": "Model disk partition structures, volumes, file systems, and deleted partition recovery.",
        "keywords": "partition disk volume filesystem recovery deleted sector offset table gpt mbr",
        "file": "docs/recipes/partitions.md",
    },
    {
        "title": "Bulk Extractor Forensic Paths",
        "description": "Model nested containment paths from bulk extraction tools with byte offsets.",
        "keywords": "bulk extractor forensic path nested containment compressed gzip offset binwalk",
        "file": "docs/recipes/bulk-extractor-path.md",
    },
    {
        "title": "Existence Intervals and Temporal Modeling",
        "description": "Model time-bounded existence with OWL-Time, gUFO, and BFO ontology patterns.",
        "keywords": "temporal interval time owl-time gufo bfo existence period duration role cac",
        "file": "docs/recipes/existence-intervals.md",
    },
    {
        "title": "Spear Phishing and Attack Narratives",
        "description": "Model spear-phishing attack chains with malware delivery and victim targeting.",
        "keywords": "spear phishing attack malware email payload exploit victim threat narrative incident",
        "file": "docs/recipes/spear-phishing.md",
    },
    {
        "title": "Online Grooming Chat Modeling",
        "description": "Model grooming chat evidence and CAC behavioral interpretation with phase progression, role separation, and message-level classification.",
        "keywords": "grooming csam child exploitation victim offender snapchat chat message phase escalation cac ontology crimes against children sexual solicitation soliciting a minor",
        "file": "docs/recipes/cac-grooming-chat-modeling.md",
    },
    {
        "title": "NCMEC CyberTip Reporting Workflow",
        "description": "Model platform detection, ESP reporting, NCMEC CyberTip lifecycle, investigation triggering, and platform cooperation using CAC Ontology classes.",
        "keywords": "cybertip ncmec platform reporting enticement detection investigation trigger esp cooperation cac ontology crimes against children",
        "file": "docs/recipes/cybertip-ncmec-workflow.md",
    },
    {
        "title": "Child Sex Trafficking and Recruitment Networks",
        "description": "Model trafficking enterprises, recruitment networks, pretext approaches, and digital-to-physical bridges using CAC Ontology classes.",
        "keywords": "trafficking recruitment ring csec cse peer recruitment school street pretext cac ontology crimes against children",
        "file": "docs/recipes/cac-trafficking-recruitment-network.md",
    },
    {
        "title": "Multi-Jurisdictional Task Force Operations",
        "description": "Model ICAC task forces, joint investigations, jurisdictional handoffs, and mass rescue operations.",
        "keywords": "task force icac multi-jurisdiction joint investigation mutual aid handoff mass rescue cac ontology crimes against children",
        "file": "docs/recipes/cac-multi-jurisdiction-task-force.md",
    },
    {
        "title": "ICAC Search Warrant Arrest (Press Release Pattern)",
        "description": "Model routine ICAC search warrant execution, custody without incident, booking, and Maryland/state police press-release arrests.",
        "keywords": "icac search warrant arrest without incident detention center held without bond child exploitation unit computer crimes unit annapolis anne arundel cac ontology crimes against children",
        "file": "docs/recipes/cac-icac-search-warrant-arrest.md",
    },
    {
        "title": "Victim Rescue, Extraction, and Post-Rescue Services",
        "description": "Model emergency response, victim extraction, safety planning, and multi-agency victim services.",
        "keywords": "rescue extraction victim service safety planning trauma recantation dcfs cac ontology crimes against children",
        "file": "docs/recipes/cac-victim-rescue-extraction.md",
    },
    {
        "title": "Tactical Arrest and Undercover Operations",
        "description": "Model high-risk arrests, dynamic entry, undercover stings, and asset forfeiture in CAC investigations.",
        "keywords": "tactical arrest undercover swat dynamic entry warrant asset forfeiture cac ontology crimes against children",
        "file": "docs/recipes/cac-tactical-undercover-operation.md",
    },
    {
        "title": "Sextortion and Online Coercion",
        "description": "Model sextortion schemes, coercion demands, and compliance pressure on minor victims.",
        "keywords": "sextortion coercion blackmail explicit images financial extortion cac ontology crimes against children",
        "file": "docs/recipes/cac-sextortion-coercion.md",
    },
    {
        "title": "Hotline Intake and Referral Lifecycle",
        "description": "Model hotline intake, triage, referral, and escalation to investigations.",
        "keywords": "hotline intake referral cybertipline mandatory reporting cac ontology crimes against children",
        "file": "docs/recipes/cac-hotline-intake-lifecycle.md",
    },
    {
        "title": "CSAM Forensic Provenance and Victim Identification",
        "description": "Model CSAM acquisition, chain of custody, hashing, correlation, and victim identification.",
        "keywords": "csam forensic provenance photodna hash chain of custody victim identification cac ontology crimes against children purchasing operation csam purchasing",
        "file": "docs/recipes/cac-csam-forensic-provenance.md",
    },
    {
        "title": "Legal Charges, Sentencing, and Case Outcomes",
        "description": "Model indictments, charges, plea agreements, sentencing, and sex-offender registry outcomes.",
        "keywords": "sentencing plea conviction charges registry legal outcome cac ontology crimes against children charged with without bond detention center",
        "file": "docs/recipes/cac-legal-sentencing-outcomes.md",
    },
    {
        "title": "Federal Prosecution Relationship Completeness",
        "description": "Model federal indictment relationship wiring: defendant–counts, indictment–charges, multi-district prosecution, forfeiture–devices, and enterprise relators.",
        "keywords": "federal prosecution indictment multi-defendant multi-district parallel jurisdiction co-conspirator 2252a federal charge conspiracy child exploitation enterprise csam production possession forfeiture cac ontology crimes against children",
        "file": "docs/recipes/cac-federal-prosecution-relationships.md",
    },
    {
        "title": "Federal Trial Proceedings and Docket Lifecycle",
        "description": "Model superseding indictments, PACER docket milestones, competency proceedings, and government trial briefs with anticipated evidence.",
        "keywords": "superseding indictment trial brief pacer docket competency 4241 speedy trial act jury trial anticipated evidence cac ontology crimes against children",
        "file": "docs/recipes/cac-federal-trial-proceedings.md",
    },
    {
        "title": "PACER Document Ingestion (MCP Agent Workflow)",
        "description": "Submit PACER PDF bundles via process_document_file, route CAC recipes, build merged validated investigation graphs for agents and Link-Look.",
        "keywords": "pacer pdf indictment judgment trial brief process_document_file validate_graph icac federal court ecf docket ao 245b agent workflow cac ontology crimes against children",
        "file": "docs/recipes/cac-pacer-document-ingestion.md",
    },
    {
        "title": "Missing Child Investigations",
        "description": "Model missing-child reports, AMBER alerts, tracking, and recovery operations.",
        "keywords": "missing child amber alert abduction runaway recovery cac ontology crimes against children",
        "file": "docs/recipes/cac-missing-child-investigation.md",
    },
    {
        "title": "International Coordination and Cross-Border Operations",
        "description": "Model transnational investigations, Europol/Interpol coordination, and cross-border evidence sharing.",
        "keywords": "international cross-border europol interpol extradition cac ontology crimes against children",
        "file": "docs/recipes/cac-international-coordination.md",
    },
    {
        "title": "CSAM Production and Manufacturing Cases",
        "description": "Model hands-on abuse and offender-produced CSAM with production environments and equipment.",
        "keywords": "production manufactured produced image video hands-on abuse cac ontology crimes against children",
        "file": "docs/recipes/cac-production-case.md",
    },
    {
        "title": "Proposing Changes to CASE/UCO",
        "description": "Identify gaps, research existing proposals, and draft change proposals for new ontology concepts.",
        "keywords": "change proposal gap missing concept extension contribute upstream issue ontology committee",
        "file": "docs/recipes/change-proposal.md",
    },
    {
        "title": "Fraud, Cryptocurrency, and Money Laundering Investigations",
        "description": "Model pig-butchering scams, blockchain tracing, exchange returns, and location correlation.",
        "keywords": "fraud crypto cryptocurrency blockchain wallet exchange laundering pig butchering investment scam telegram geofence subpoena kyc trace",
        "file": "docs/recipes/fraud-crypto-laundering.md",
    },
    {
        "title": "Elder Fraud and Government-Impersonation Schemes",
        "description": "Model agent-impersonation call-center schemes: money couriers, prepaid-card and cash-handoff flows, spoofed calls, controlled-delivery stings, and records attribution.",
        "keywords": "elder fraud impersonation false personation government agent scam treasury irs social security money mule courier runner green dot gift card prepaid card cash handoff controlled delivery tech support scam pop-up grandparent scam wire fraud conspiracy call center spoofed caller id",
        "file": "docs/recipes/elder-fraud-impersonation.md",
    },
    {
        "title": "Espionage Act and Classified-Information Disclosure",
        "description": "Model Espionage Act prosecutions: classified national defense information with uco-marking classification banners, SCIF removal chains, transmission actions, obstruction, and 793/794 counts.",
        "keywords": "espionage act 793 794 classified national defense information ndi top secret sci security clearance scif sensitive compartmented noforn fvey unauthorized disclosure marking classification banner jwics leak discord clearance holder executive order 13526 obstruction destroyed devices",
        "file": "docs/recipes/espionage-classified-disclosure.md",
    },
    {
        "title": "Export Control and Sanctions Evasion",
        "description": "Model export-control and sanctions prosecutions: IEEPA/EAR counts, dated Entity List designations, gUFO-typed controlled goods, false EEI/AES filings, and the papered-consignee vs. true-end-user concealment chain.",
        "keywords": "export control ieepa 1705 entity list ear eccn ear99 export license bis bureau of industry and security commerce sdn ofac sanctions embargo itar smuggling 554 false export information 305 shipper's export declaration electronic export information automated export system aes ultimate consignee end user transshipment freight forwarder dual use prc procurement intermediary",
        "file": "docs/recipes/export-control-sanctions.md",
    },
    {
        "title": "Cyber Threat Intelligence and APT Reporting",
        "description": "Model an open-source CTI/APT threat report: the report and its graphics captured by hash, the threat actor as an Organization (no ThreatActor class), malware families/variants and toolkit, registry/service-DLL persistence (native UCO coverage), third-party cloud C2, victimology, IOCs, and MITRE ATT&CK techniques via the uco-action:Technique metaclass (UCO PR #676: a technique is an owl:Class subclassing uco-action:Action with techniqueID, punned onto the exhibiting Action; forward-implemented by the attack-technique extension for UCO 1.5.0).",
        "keywords": "apt advanced persistent threat threat actor cyber espionage group nation-state sagerunex darkwatchman fileless registry buffer keylogger dga tordwm spearphishing pony express backdoor implant rat malware family variant loader dll injection vmprotect command and control c2 beacon exfiltration lateral movement impacket wmi persistence service dll servicedll registry reg add windows service scheduled task cookie stealer venom proxy port relay htran mtrain victimology campaign threat spotlight ttp ttps mitre att&ck technique ioc yara clamav snort talos mandiant prevailion pact dropbox twitter zimbra cloud c2 windowsregistrykey registrydatatype",
        "file": "docs/recipes/cyber-threat-intelligence.md",
    },
    {
        "title": "SOLVE-IT Investigation Planning and Error Mitigation",
        "description": "Plan and document forensic method with the pinned SOLVE-IT knowledge base (23 objectives, 187 techniques, 339 weaknesses, 270 mitigations): state objectives, record SolveitInvestigativeAction with usedTechnique/appliedMitigation, type acquisition outputs with SOLVE-IT observables, rate weaknesses (ASTM E3016-18) with solveit-wa:WeaknessEvaluation, and optionally type actions with punned DFT-* technique classes (UCO 1.5.0 metaclass style). Discover techniques with plan_solveit_workflow / search_solveit / get_solveit_details.",
        "keywords": "solve-it solveit technique selection objective forensic method methodology error mitigation analysis weakness mitigation astm e3016 disk imaging acquisition plan hash verification write blocker dual-tool verification tool testing quality assurance qa lab accreditation error rate daubert examination report investigative action dft dfw dfm dfo weakness evaluation rpn likelihood impact",
        "file": "docs/recipes/solve-it-investigation-planning.md",
    },
    {
        "title": "Insider Threat, Trade Secret Theft, and Economic Espionage",
        "description": "Model insider exfiltration of trade secrets: corporate telemetry, personal cloud accounts, per-category 1832/1831 counts, foreign-government-benefit evidence, and jury verdicts.",
        "keywords": "insider threat trade secret economic espionage 1832 1831 exfiltration data loss prevention dlp badge access personal cloud account proprietary confidential employee resignation talent program foreign instrumentality startup competitor source code wechat jury verdict",
        "file": "docs/recipes/insider-threat-trade-secrets.md",
    },
    {
        "title": "Legal Process Modeling (Charges, Verdicts, Sentences)",
        "description": "Model charging instruments, conspiracy/attempt/derivative charges, pleas, verdicts, sentences, forfeiture, and restitution for any investigation type via the legalproc extension.",
        "keywords": "legal process charge criminal charge conspiracy attempt indictment superseding verdict plea sentence sentencing forfeiture restitution appeal docket count statute 924(c) violent crime prosecution legalproc",
        "file": "docs/recipes/legal-process-modeling.md",
    },
    {
        "title": "Racketeering (RICO) and Criminal Enterprise",
        "description": "Model racketeering prosecutions via the rico extension: the charged enterprise (rico:RacketeeringEnterprise with enterpriseType 'association-in-fact' or 'legal-entity'), functional member roles as rico:EnterpriseRole nodes with roleFunction, statutory predicate categories as rico:predicateStatute on RICO counts, multi-instrument per-defendant count tracking (PACER 1/1s/1ss suffixes), and enterprise conduct as Actions.",
        "keywords": "racketeering rico 1962 1961 1963 criminal enterprise association-in-fact organized crime pattern of racketeering predicate act enterprise role organizer caller money launderer database hacker residential burglar target identifier gang syndicate mob crew division of labor social engineering enterprise",
        "file": "docs/recipes/racketeering-enterprise.md",
    },
    {
        "title": "Weapons and Drug Evidence",
        "description": "Model firearms, ammunition, and edged weapons with queryable make/model/caliber/serialNumber via the weapons extension (class tree mirrors the CCO Artifact Ontology weapon hierarchy, BFO 2020; gUFO FunctionalComplex bridge; NIEM-aligned properties), and seized/charged controlled-substance portions via the drugs extension (drug:ControlledSubstance with ChEBI IRI reference for chemical identity, CSA schedule, mass, purity basis 'mixture' vs 'actual', verbatim quantityDescription; grounded as gufo:Quantity).",
        "keywords": "weapon firearm handgun pistol revolver rifle shotgun long gun ammunition magazine caliber serial number obliterated 922(g) 924(c) 922(k) felon in possession brandish drug controlled substance methamphetamine fentanyl cocaine heroin narcotics schedule ii 841 846 drug quantity mixture actual purity gram kilogram chebi cco common core ontologies gufo quantity seizure forfeiture",
        "file": "docs/recipes/weapons-drug-evidence.md",
    },
    {
        "title": "Cargo Theft, Route Staging, and Warehouse Movement",
        "description": "Model freight route theft, geofence deviations, manifest anomalies, and warehouse staging.",
        "keywords": "cargo theft freight route staging warehouse geofence manifest trailer tractor logistics supply chain",
        "file": "docs/recipes/cargo-theft-route-staging.md",
    },
    {
        "title": "Starter Kit: Filesystem Report Mapping",
        "description": "End-to-end mapping of a filesystem report to CASE/UCO.",
        "keywords": "starter kit filesystem file report triage mapping end-to-end hash",
        "file": "docs/recipes/starter-filesystem-report.md",
        "is_starter_kit": True,
    },
    {
        "title": "Starter Kit: Mobile Extraction Mapping",
        "description": "End-to-end mapping of a mobile device extraction to CASE/UCO.",
        "keywords": "starter kit mobile phone extraction cellebrite graykey mapping end-to-end",
        "file": "docs/recipes/starter-mobile-extraction.md",
        "is_starter_kit": True,
    },
    {
        "title": "Starter Kit: Email Export Mapping",
        "description": "End-to-end mapping of an email export to CASE/UCO.",
        "keywords": "starter kit email export pst mbox mapping end-to-end",
        "file": "docs/recipes/starter-email-export.md",
        "is_starter_kit": True,
    },
    {
        "title": "Starter Kit: Tool Run Mapping",
        "description": "End-to-end mapping of a forensic tool run to CASE/UCO.",
        "keywords": "starter kit tool run action autopsy encase mapping end-to-end",
        "file": "docs/recipes/starter-tool-run.md",
        "is_starter_kit": True,
    },
    {
        "title": "Windows USN Journal",
        "description": "Model NTFS change journal entries with structured reason flags, rename modeling, and provenance.",
        "keywords": "usn journal ntfs change journal windows filesystem timeline rename reason flags",
        "file": "docs/recipes/usn-journal.md",
    },
    {
        "title": "iOS / macOS Sysdiagnose Archives",
        "description": "Model Apple sysdiagnose packages: device/OS, archive tree, system_logs.logarchive as AppleUnifiedLogArchive, Wi-Fi and BatteryBDC children, collection provenance.",
        "keywords": "sysdiagnose sys diagnosis apple ios macos iphone logarchive system_logs unified logging ufade pymobiledevice3 libimobiledevice crash wifi batterybdc summaries tracev3 ips stackshot crashes_and_spins crash_reporter runningboard ioreg brctl incident_id crashreporterkey",
        "file": "docs/recipes/ios-sysdiagnose.md",
    },
    {
        "title": "Apple Unified Logs and Analytic Tool Outputs",
        "description": "Model Apple Unified Logging EventRecords and structured parser outputs from unifiedlog_iterator CSV, Notari SQLite, and iLEAPP with SOLVE-IT DFT-1066/1076 provenance.",
        "keywords": "unified log unified logs apple oslog logarchive tracev3 unifiedlog_iterator mandiant notari ileapp sqlite csv eventrecord subsystem category locationd signpost persist timesync boot_uuid mach_continuous_time simpledump log show activity_id",
        "file": "docs/recipes/apple-unified-logs.md",
    },
    {
        "title": "Cross-Ontology Composition",
        "description": "Authoritative composition policy for CASE/UCO, CAC, SOLVE-IT, SDK extensions, and upper profiles (BFO/gUFO/PROV-O/OWL-Time/GeoSPARQL/FOAF/ORG/PROF).",
        "keywords": "cross-domain cross-ontology extension composition cac aeo multi-domain combine namespaces packages profile bfo gufo prov geosparql foaf org prof",
        "file": "docs/recipes/cross-ontology-composition.md",
    },
    {
        "title": "Foundational Typing (BFO and gUFO)",
        "description": "Select and apply BFO or gUFO as an additional foundational layer on CASE/UCO nodes without replacing domain classes.",
        "keywords": "bfo gufo foundational upper ontology endurant perdurant continuant occurrent relator role typing",
        "file": "docs/recipes/foundational-typing-bfo-gufo.md",
    },
    {
        "title": "PROV-O Evidence Lineage",
        "description": "Combine PROV-O Entity/Activity/Agent multi-typing with CASE ProvenanceRecord and UCO actions without duplicating real-world things.",
        "keywords": "prov-o provenance lineage derivation activity entity agent wasgeneratedby wasderivedfrom",
        "file": "docs/recipes/prov-o-evidence-lineage.md",
    },
    {
        "title": "OWL-Time Temporal Evidence",
        "description": "Model exact timestamps with native CASE/UCO properties and qualified temporal resources with OWL-Time instants and intervals.",
        "keywords": "owl-time temporal instant interval duration clock skew timezone approximate time",
        "file": "docs/recipes/owl-time-temporal-evidence.md",
    },
    {
        "title": "GeoSPARQL Geospatial Evidence",
        "description": "Enrich UCO Location with GeoSPARQL Feature/Geometry, WKT, CRS, and derived analytic geometries with provenance.",
        "keywords": "geosparql geospatial geometry feature wkt crs polygon cell sector geofence route",
        "file": "docs/recipes/geosparql-geospatial-evidence.md",
    },
    {
        "title": "FOAF/ORG Identity Roles and Organizations",
        "description": "Integrate UCO people, accounts, and roles with FOAF agents and W3C ORG memberships, posts, and organizational units.",
        "keywords": "foaf org identity account role membership post organization agency task force",
        "file": "docs/recipes/foaf-org-identity-roles.md",
    },
    {
        "title": "PROF Validation Profile Metadata",
        "description": "Declare intended ontology/profile bundles with PROF and record validation execution separately from conformance claims.",
        "keywords": "prof profile validation metadata bundle shapes conformance validator fingerprint",
        "file": "docs/recipes/prof-validation-profile-metadata.md",
    },
    {
        "title": "SOLVE-IT Plan versus Execution Provenance",
        "description": "Distinguish planned forensic methods from executed SolveitInvestigativeAction occurrences with PROV-O and OWL-Time.",
        "keywords": "solve-it plan execution provenance deviation mitigation weakness re-execution",
        "file": "docs/recipes/solveit-plan-execution-provenance.md",
    },
    {
        "title": "Cross-Domain Extensions",
        "description": "Legacy redirect to Cross-Ontology Composition; retained for routing compatibility.",
        "keywords": "cross-domain extension composition cac aeo multi-domain combine namespaces packages",
        "file": "docs/recipes/cross-domain-extensions.md",
    },
    {
        "title": "Authoring and Improving Recipes",
        "description": "Write a new recipe when an investigation pattern has no existing recipe, or improve an existing recipe a live case proved wrong or incomplete: structure, grounding rules, re-validation, cross-references, and registration in the MCP indexes.",
        "keywords": "recipe authoring improve update fix existing new recipe write recipe template pattern documentation contribute unseen novel workflow self-improving maintain catalog",
        "file": "docs/recipes/recipe-authoring.md",
    },
]

# ---------------------------------------------------------------------------
# Mapping guide index — step-by-step guidance for common evidence sources
# ---------------------------------------------------------------------------

MAPPING_GUIDE_INDEX: list[dict] = [
    {
        "source": "filesystem report",
        "keywords": ["file", "directory", "triage", "listing", "report", "csv", "hash", "filesystem"],
        "pattern": "ObservableObject + FileFacet + ContentDataFacet",
        "classes": ["ObservableObject", "FileFacet", "ContentDataFacet", "InvestigativeAction", "Tool"],
        "anti_patterns": [
            "Don't create a separate ObservableObject for each facet — one object can have multiple facets",
            "Don't use Tool as a top-level evidence item — it describes the instrument, not the evidence",
        ],
        "starter_kit": "docs/recipes/starter-filesystem-report.md",
        "code_skeleton": "graph.create(ObservableObject, has_facet=[FileFacet(file_name=...), ContentDataFacet(hash_method=..., hash_value=...)])",
    },
    {
        "source": "mobile device extraction",
        "keywords": ["mobile", "phone", "cellebrite", "graykey", "ufed", "extraction", "android", "ios", "smartphone"],
        "pattern": "ObservableObject + DeviceFacet + ApplicationFacet + MessageFacet",
        "classes": ["ObservableObject", "DeviceFacet", "ApplicationFacet", "MessageFacet", "ContactFacet", "InvestigativeAction", "Tool"],
        "anti_patterns": [
            "Don't model the phone as an InvestigativeAction — the phone is an ObservableObject, the extraction is the action",
            "Don't flatten app data into one facet — use separate facets for messages, contacts, call logs",
        ],
        "starter_kit": "docs/recipes/starter-mobile-extraction.md",
        "code_skeleton": "device = graph.create(ObservableObject, has_facet=[DeviceFacet(manufacturer=..., model=...)])",
    },
    {
        "source": "iOS sysdiagnose archive",
        "keywords": [
            "sysdiagnose", "system_logs", "logarchive", "iphone-os", "ufade",
            "pymobiledevice3", "summaries", "batterybdc", "tracev3",
            "ips", "stackshot", "crashes_and_spins", "runningboard",
        ],
        "pattern": "Device + sysdiagnose FileFacet directory + AppleUnifiedLogArchive/EventLog",
        "classes": [
            "ObservableObject", "DeviceFacet", "MobileDeviceFacet", "OperatingSystem",
            "SoftwareFacet", "FileFacet", "AppleUnifiedLogArchive", "EventLog",
            "WirelessNetworkConnection", "InvestigativeAction", "Tool",
        ],
        "anti_patterns": [
            "Don't flatten the sysdiagnose tree into one File observable — keep logarchive and high-value children linked",
            "Don't invent a SysdiagnoseFacet — use FileFacet directories plus AppleUnifiedLogArchive",
        ],
        "starter_kit": "docs/recipes/ios-sysdiagnose.md",
        "code_skeleton": "logarchive = graph.create(AppleUnifiedLogArchive, name='system_logs.logarchive', has_facet=[FileFacet(is_directory=[True])])",
    },
    {
        "source": "Apple unified logs",
        "keywords": [
            "unified log", "unified logs", "oslog", "unifiedlog_iterator", "notari",
            "ileapp", "signpost", "subsystem", "category", "tracev3",
            "timesync", "boot_uuid", "mach_continuous_time", "simpledump",
        ],
        "pattern": "AppleUnifiedLogArchive → EventRecord + Event + AnalyticTool outputs (CSV/SQLite)",
        "classes": [
            "AppleUnifiedLogArchive", "EventLog", "EventRecord", "EventRecordFacet",
            "Event", "Dictionary", "DictionaryEntry", "AnalyticTool",
            "SolveitInvestigativeAction", "ApplicationFacet",
        ],
        "anti_patterns": [
            "Don't invent UnifiedLogFacet — map rows with EventRecordFacet and Dictionary attributes",
            "Don't claim message text without running a parser on the binary logarchive",
        ],
        "starter_kit": "docs/recipes/apple-unified-logs.md",
        "code_skeleton": "record = graph.create(EventRecord, has_facet=[EventRecordFacet(event_record_text=..., event_record_service_name=...)])",
    },
    {
        "source": "email export",
        "keywords": ["email", "pst", "mbox", "eml", "outlook", "thunderbird", "gmail", "exchange", "mail"],
        "pattern": "ObservableObject + EmailMessageFacet + EmailAddressFacet",
        "classes": ["ObservableObject", "EmailMessageFacet", "EmailAddressFacet", "EmailAccountFacet", "ContentDataFacet"],
        "anti_patterns": [
            "Don't model sender and recipient as the same ObservableObject — use separate EmailAddressFacet instances",
            "Don't skip the EmailAccountFacet when account-level metadata is available",
        ],
        "starter_kit": "docs/recipes/starter-email-export.md",
        "code_skeleton": "graph.create(ObservableObject, has_facet=[EmailMessageFacet(subject=..., sent_time=...)])",
    },
    {
        "source": "forensic tool run",
        "keywords": ["tool", "autopsy", "encase", "ftk", "volatility", "sleuthkit", "run", "execution", "scan"],
        "pattern": "Investigation + InvestigativeAction + Tool + ObservableObject",
        "classes": ["Investigation", "InvestigativeAction", "Tool", "ObservableObject", "ProvenanceRecord"],
        "anti_patterns": [
            "Don't omit the Tool object — always record which tool (and version) performed the action",
            "Don't model tool output without linking it to the InvestigativeAction that produced it",
        ],
        "starter_kit": "docs/recipes/starter-tool-run.md",
        "code_skeleton": "tool = graph.create(Tool, name=..., version=...)\naction = graph.create(InvestigativeAction, name=..., instrument=tool)",
    },
    {
        "source": "pcap network capture",
        "keywords": ["pcap", "packet", "capture", "wireshark", "tcpdump", "network", "traffic", "sniff"],
        "pattern": "ObservableObject + NetworkConnectionFacet + IPAddressFacet",
        "classes": ["ObservableObject", "NetworkConnectionFacet", "IPAddressFacet", "DomainNameFacet", "URLFacet", "InvestigativeAction", "Tool"],
        "anti_patterns": [
            "Don't model each packet as a separate ObservableObject — group by connection or flow",
            "Don't put IP addresses in NetworkConnectionFacet text fields — use separate IPAddressFacet objects",
        ],
        "starter_kit": None,
        "code_skeleton": "graph.create(ObservableObject, has_facet=[NetworkConnectionFacet(src_ip=..., dst_ip=..., dst_port=...)])",
    },
    {
        "source": "disk image",
        "keywords": ["disk", "image", "dd", "e01", "raw", "ewf", "forensic", "acquisition", "clone"],
        "pattern": "ObservableObject + ImageFacet + ContentDataFacet + FileFacet",
        "classes": ["ObservableObject", "ImageFacet", "FileFacet", "ContentDataFacet", "InvestigativeAction", "Tool"],
        "anti_patterns": [
            "Don't confuse ImageFacet (disk image metadata) with picture/photo image data",
            "Don't skip ContentDataFacet — hash values are critical for disk image integrity",
        ],
        "starter_kit": None,
        "code_skeleton": "graph.create(ObservableObject, has_facet=[ImageFacet(image_type=...), ContentDataFacet(hash_method='SHA-256', hash_value=...)])",
    },
    {
        "source": "browser history",
        "keywords": ["browser", "history", "bookmark", "cookie", "chrome", "firefox", "safari", "edge", "url", "web"],
        "pattern": "ObservableObject + URLHistoryFacet + BrowserBookmarkFacet + CookieFacet",
        "classes": ["ObservableObject", "URLHistoryFacet", "BrowserBookmarkFacet", "CookieFacet", "URLFacet", "ApplicationFacet"],
        "anti_patterns": [
            "Don't model each URL visit as a separate ObservableObject — use URLHistoryFacet entries",
            "Don't forget ApplicationFacet to identify which browser produced the history",
        ],
        "starter_kit": None,
        "code_skeleton": "graph.create(ObservableObject, has_facet=[URLHistoryFacet(browser_info=..., url=..., last_visited=...)])",
    },
    {
        "source": "ai ml image analysis",
        "keywords": ["ai", "ml", "machine learning", "inference", "model", "image", "search",
                     "semantic", "embedding", "clip", "neural", "prediction", "detection",
                     "classification", "scoring", "ranking", "similarity", "pipeline",
                     "photo", "picture", "raster", "rescuebox"],
        "pattern": "InvestigativeAction (per pipeline step) + AnalyticTool + RasterPicture + ConfidenceFacet + Relationship",
        "classes": ["InvestigativeAction", "AnalyticTool", "RasterPicture", "RasterPictureFacet",
                    "FileFacet", "ContentDataFacet", "ConfidenceFacet", "Relationship",
                    "ProvenanceRecord", "Directory"],
        "anti_patterns": [
            "Don't hide structured facts (model name, query, thresholds, scores) inside uco-core:description as JSON strings — use explicit properties or ConfiguredTool",
            "Don't use ArtifactClassification for tool endpoint names — classification describes what the artifact IS (content label), not which tool processed it",
            "Don't model a multi-step pipeline as a single InvestigativeAction — each model/step gets its own action with its own inputs, outputs, and timestamps",
            "Don't use generic File or ObservableObject for image files — use RasterPicture with RasterPictureFacet",
            "Don't omit per-result scores — use ConfidenceFacet on each result for ranking and explainability",
            "Don't omit hashes and sizes on evidence files — without them the graph is a workflow log, not an evidentiary record",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# One InvestigativeAction per pipeline step\n"
            "step = graph.create(InvestigativeAction, name=..., instrument=[tool], object=[inputs], result=[outputs])\n"
            "# RasterPicture with score\n"
            "img = graph.create(RasterPicture, has_facet=[FileFacet(...), ContentDataFacet(hash=[...]), RasterPictureFacet(...), ConfidenceFacet(confidence=0.87)])\n"
            "# Explicit relationship\n"
            "graph.create(Relationship, source=[img], target=input_dir, kind_of_relationship='Selected_From', is_directional=True)"
        ),
    },
    {
        "source": "registry artifacts",
        "keywords": ["registry", "windows", "hive", "regedit", "sam", "ntuser", "system", "software", "key", "value"],
        "pattern": "ObservableObject + WindowsRegistryKeyFacet + WindowsRegistryValueFacet",
        "classes": ["ObservableObject", "WindowsRegistryKeyFacet", "WindowsRegistryValueFacet", "FileFacet"],
        "anti_patterns": [
            "Don't model registry values without their parent key — always include the key path",
            "Don't use generic FileFacet for registry hive content — use the specific registry facets",
        ],
        "starter_kit": None,
        "code_skeleton": "graph.create(ObservableObject, has_facet=[WindowsRegistryKeyFacet(key=...)])",
    },
    {
        "source": "child sex trafficking ring or recruitment network",
        "keywords": ["trafficking", "trafficker", "trafficked", "ring", "cell",
                     "rotation", "interstate transport", "recruitment",
                     "recruiter", "school-based", "peer recruitment",
                     "street recruitment", "pretext", "help offer",
                     "food offer", "transportation offer", "phone charging",
                     "rapid escalation", "digital-to-physical", "csec", "cse",
                     "icac"],
        "pattern": (
            "CACInvestigation + TraffickingEnterprise + (TraffickingRing | TraffickingCell) "
            "+ TraffickingVictimRole + (PeerRecruitmentNetwork | "
            "ClassmateRecruitmentNetwork) + (SchoolBasedRecruitment | "
            "StreetBasedRecruitment with pretext approach) + DigitalToPhysicalBridge"
        ),
        "classes": ["CACInvestigation", "TraffickingEnterprise", "TraffickingRing",
                    "TraffickingCell", "TraffickingVictimRole",
                    "MinorTraffickingVictimRole", "TraffickingVictimRescue",
                    "VictimRotation", "InterstateVictimTransport",
                    "InterstateTraffickingNetwork",
                    "PeerRecruitmentNetwork", "ClassmateRecruitmentNetwork",
                    "SchoolBasedRecruitment", "StreetBasedRecruitment",
                    "HelpOfferApproach", "FoodOfferApproach",
                    "TransportationOfferApproach", "PhoneChargingOffer",
                    "RapidEscalationRecruitment", "DigitalToPhysicalBridge",
                    "MandatoryReportingActivation", "Identity", "Location",
                    "Relationship"],
        "anti_patterns": [
            "Don't model a trafficking ring as a single Identity — use TraffickingEnterprise (or TraffickingRing/TraffickingCell) so role hierarchy and victim relationships have a structural anchor",
            "Don't reuse generic InvestigativeAction for each pretext approach — use the specific *OfferApproach subclass so analysts can query approach patterns",
            "Don't treat 'online recruitment then in-person meet' as one event — split it: one online behavior event plus a DigitalToPhysicalBridge for the meet, so the timeline shows the transition",
            "Don't forget to set CASE_UCO_EXTENSIONS=cac so trafficking and recruitment classes load",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "ring = graph.create(TraffickingRing, name='Ring 2026-014')\n"
            "victim_role = graph.create(MinorTraffickingVictimRole, name='Victim A role')\n"
            "approach = graph.create(TransportationOfferApproach, name='Bus-stop ride offer')\n"
            "bridge = graph.create(DigitalToPhysicalBridge, name='IG DM -> motel meet')\n"
            "graph.create(Relationship, source=[approach], target=[victim_role], kind_of_relationship='Targeted')"
        ),
    },
    {
        "source": "multi-jurisdictional rescue or task force operation",
        "keywords": ["multi-jurisdiction", "jurisdiction", "task force", "taskforce",
                     "joint investigation", "joint operation", "rescue",
                     "mass rescue", "mutual aid", "handoff", "icac", "hsi",
                     "fbi", "interpol", "federal", "interstate"],
        "pattern": (
            "CACInvestigation + TaskForce + (LocalJurisdiction | StateJurisdiction | "
            "FederalJurisdiction | InternationalJurisdiction) + JointInvestigation + "
            "(MassChildRescueOperation | VictimExtraction) + JurisdictionalHandoff + "
            "MutualAidRequest"
        ),
        "classes": ["CACInvestigation", "TaskForce", "JointInvestigation",
                    "Jurisdiction", "LocalJurisdiction", "StateJurisdiction",
                    "FederalJurisdiction", "InternationalJurisdiction",
                    "JurisdictionalHandoff", "MutualAidRequest",
                    "MassChildRescueOperation", "VictimExtraction",
                    "EmergencyResponse", "InvestigativeAction",
                    "ProvenanceRecord", "Identity", "Location"],
        "anti_patterns": [
            "Don't model the task force as a generic Identity — use TaskForce so participating jurisdictions/agencies have a structural relationship",
            "Don't bury jurisdictional transitions in a description string — use JurisdictionalHandoff (and MutualAidRequest where relevant) so the chain is queryable",
            "Don't lose per-victim provenance during a mass rescue — pair MassChildRescueOperation with one VictimExtraction per victim, each with its own ProvenanceRecord",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "tf = graph.create(TaskForce, name='Regional ICAC Task Force')\n"
            "op = graph.create(MassChildRescueOperation, name='Operation Lighthouse')\n"
            "fed = graph.create(FederalJurisdiction, name='HSI - Field Office X')\n"
            "state = graph.create(StateJurisdiction, name='State Police')\n"
            "graph.create(JurisdictionalHandoff, source=[state], target=[fed], name='Lead transferred to HSI')"
        ),
    },
    {
        "source": "tactical arrest or high-risk operation",
        "keywords": ["tactical", "arrest", "high-risk", "dynamic entry",
                     "warrant service", "swat", "raid", "undercover",
                     "asset forfeiture", "seizure"],
        "pattern": (
            "CACInvestigation + (ArrestOperation | HighRiskArrest) + DynamicEntry "
            "+ SuspectProfile + ThreatAssessment + AssetForfeitureAction"
        ),
        "classes": ["CACInvestigation", "ArrestOperation", "HighRiskArrest",
                    "DynamicEntry", "SuspectProfile", "ThreatAssessment",
                    "UndercoverOperation", "AssetForfeitureAction",
                    "InvestigativeAction", "Tool", "Identity", "Location"],
        "anti_patterns": [
            "Don't collapse pre-op planning and the entry into one action — pre-op SuspectProfile/ThreatAssessment justify the operational posture and need their own records",
            "Don't model seized property as plain ObservableObject — use AssetForfeitureAction so the legal-process linkage is explicit",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "ta = graph.create(ThreatAssessment, name='Pre-op threat assessment')\n"
            "arrest = graph.create(HighRiskArrest, name='Arrest of subject X')\n"
            "entry = graph.create(DynamicEntry, name='Front-door dynamic entry')\n"
            "forfeiture = graph.create(AssetForfeitureAction, name='Vehicle and electronics seizure')"
        ),
    },
    {
        "source": "victim rescue extraction and post-rescue services",
        "keywords": ["rescue", "extraction", "extract", "emergency response",
                     "victim service", "safety planning", "trauma",
                     "ongoing danger", "recantation", "multi-agency",
                     "dcfs", "child protective"],
        "pattern": (
            "CACInvestigation + EmergencyResponse + VictimExtraction + "
            "OngoingDangerAssessment + SafetyPlanning + MultiAgencyVictimResponse "
            "+ TraumaIndicator + HelpSeekingBarrier"
        ),
        "classes": ["CACInvestigation", "EmergencyResponse", "VictimExtraction",
                    "OngoingDangerAssessment", "SafetyPlanning",
                    "MultiAgencyVictimResponse", "TraumaIndicator",
                    "HelpSeekingBarrier", "RecantationAssessment",
                    "PartialRecantationStatement", "ReaffirmedDisclosureStatement",
                    "PostRecantationForensicInterview", "ChildVictim",
                    "InvestigativeAction"],
        "anti_patterns": [
            "Don't treat post-rescue services as out-of-scope — model MultiAgencyVictimResponse and SafetyPlanning so downstream services are auditable",
            "Don't conflate recantation with case closure — RecantationAssessment is its own event and may coexist with an ongoing investigation; pair it with ReaffirmedDisclosureStatement when the disclosure is later reaffirmed",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "extraction = graph.create(VictimExtraction, name='Victim extraction at motel')\n"
            "danger = graph.create(OngoingDangerAssessment, name='Trafficker still at-large')\n"
            "plan = graph.create(SafetyPlanning, name='Initial safety plan with DCFS')"
        ),
    },
    {
        "source": "csam provenance forensics and victim identification",
        "keywords": ["csam forensic", "csam provenance", "chain of custody",
                     "evidence verification", "metadata correlation",
                     "temporal pattern", "geospatial correlation",
                     "cross-platform correlation", "behavioral fingerprint",
                     "victim identification", "photodna",
                     "perceptual hash", "image hashing"],
        "pattern": (
            "ForensicAcquisitionAction + ChainOfCustodyAction (per event) + "
            "EvidenceVerificationAction + (MetadataCorrelation | TemporalPatternAnalysis "
            "| GeospatialCorrelation | CrossPlatformCorrelation | "
            "BehavioralFingerprinting) + VictimIdentificationProcess"
        ),
        "classes": ["ForensicAcquisitionAction", "ChainOfCustodyAction",
                    "EvidenceVerificationAction", "MetadataCorrelation",
                    "TemporalPatternAnalysis", "GeospatialCorrelation",
                    "CrossPlatformCorrelation", "BehavioralFingerprinting",
                    "VictimIdentificationProcess", "ContentHashingTool",
                    "RasterPicture", "RasterPictureFacet", "FileFacet",
                    "ContentDataFacet", "ProvenanceRecord", "Relationship"],
        "anti_patterns": [
            "Don't merge acquisition, verification, and analysis into one action — each is its own auditable step with its own tool, operator, and timestamp",
            "Don't omit hashes on CSAM artifacts — without ContentDataFacet entries the chain of custody is unverifiable",
            "Don't store correlation findings only in description text — use the matching CAC correlation class so the result is queryable",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "acq = graph.create(ForensicAcquisitionAction, name='Acquisition of seized device')\n"
            "verify = graph.create(EvidenceVerificationAction, name='SHA-256 verification')\n"
            "img = graph.create(RasterPicture, has_facet=[FileFacet(file_name=...), ContentDataFacet(hash_method='SHA-256', hash_value='...'), RasterPictureFacet(...)])\n"
            "vid = graph.create(VictimIdentificationProcess, name='Match against known-victim DB')"
        ),
    },
    {
        "source": "icac search warrant arrest",
        "keywords": [
            "search warrant", "warrant", "arrest", "without incident", "taken into custody",
            "detention center", "held without bond", "child exploitation unit",
            "computer crimes unit", "icac", "anne arundel", "annapolis", "booking",
            "maryland state police", "internet crimes against children",
        ],
        "pattern": (
            "CACInvestigation + MarylandICACtaskForce + InvestigativeAction chain "
            "+ Authorization + ArrestOperation (warrant_arrest) + BookingAction "
            "+ CorrectionalFacility + StateCharge"
        ),
        "classes": [
            "CACInvestigation", "MarylandICACtaskForce", "MarylandStatePoliceComputerCrimesUnit",
            "InvestigativeAction", "Authorization", "ArrestOperation", "BookingAction",
            "CorrectionalFacility", "StateCharge", "OnlineGrooming", "OnlinePurchase",
            "Identity", "Organization", "Location",
        ],
        "anti_patterns": [
            "Don't use HighRiskArrest or DynamicEntry when the narrative says custody was without incident",
            "Don't duplicate MSP CCU as both a specialized unit and a separate performer Organization",
            "Don't leave OnlineGrooming or OnlinePurchase isolated — add uco-action:performer (suspect) and investigation Concerns links",
            "Don't create empty Phase nodes — use typed phases with occursDuringPhase on actions or omit phases",
            "Don't embed ExternalReference as a blank node — give it an explicit @id IRI",
            "Don't put grooming events in Investigation.uco-core:object — reserve object for ObservableObject evidence",
        ],
        "starter_kit": "docs/recipes/cac-icac-search-warrant-arrest.md",
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "grooming = graph.add_node('kb:grooming-1', 'cacontology-grooming:OnlineGrooming', {\n"
            "    'uco-action:performer': {'@id': 'kb:suspect'},\n"
            "    'cacontology-grooming:targetsVictim': {'@id': 'kb:minor-victim'},\n"
            "})\n"
            "graph.add_node('kb:rel-1', 'uco-core:Relationship', {\n"
            "    'uco-core:source': [{'@id': 'kb:investigation'}],\n"
            "    'uco-core:target': [{'@id': 'kb:grooming-1'}],\n"
            "    'uco-core:kindOfRelationship': 'Concerns',\n"
            "})"
        ),
    },
    {
        "source": "cybertip grooming report",
        "keywords": ["cybertip", "ncmec", "grooming", "csam", "child", "exploitation",
                     "victim", "offender", "enticement", "snapchat", "platform", "reporting",
                     "detection", "cac", "crimes against children", "hotline", "sextortion"],
        "pattern": "CACInvestigation + GroomingBehavior + NCMECCybertipReport + GroomingMessage + ChildVictim + OnlinePredator",
        "classes": ["CACInvestigation", "GroomingBehavior", "OnlineGrooming", "GroomingMessage",
                    "ChildVictim", "OnlinePredator", "NCMECCybertipReport", "OnlineEnticementIncident",
                    "AutomatedDetectionAction", "ElectronicServiceProvider", "MessageThread",
                    "MessageFacet", "ApplicationAccount", "RasterPicture", "Relationship"],
        "anti_patterns": [
            "Don't use generic InvestigativeAction for grooming phases — use GroomingBehavior with grooming stage properties from the CAC extension",
            "Don't model the CyberTip as a plain ObservableObject — use NCMECCybertipReport with incident type and annotations from the CAC extension",
            "Don't use freetext descriptions for grooming phases — use the structured GroomingPhase classes (InitialContactPhase, TrustBuildingPhase, etc.)",
            "Don't forget to set CASE_UCO_EXTENSIONS=cac to load CAC classes in the MCP server",
        ],
        "starter_kit": None,
        "code_skeleton": (
            "# Requires CASE_UCO_EXTENSIONS=cac\n"
            "# CAC grooming + NCMEC classes\n"
            "grooming = graph.create(OnlineGrooming, name=..., grooming_stage='trust_building')\n"
            "victim = graph.create(ChildVictim, name=...)\n"
            "offender = graph.create(OnlinePredator, name=...)\n"
            "cybertip = graph.create(NCMECCybertipReport, name=...)\n"
            "# Link to core UCO messaging\n"
            "thread = graph.create(MessageThread, has_facet=[MessageThreadFacet(participant=[offender_acct, victim_acct])])"
        ),
    },
]
