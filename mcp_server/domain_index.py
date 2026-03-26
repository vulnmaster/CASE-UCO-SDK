"""Domain index for AI-assisted CASE/UCO development.

Maps investigative tasks to SDK classes and provides a searchable recipe index,
optimized for consumption by AI coding agents via MCP tools.
"""

from __future__ import annotations

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
    "model digital evidence for court": [
        ("Investigation", "The case container"),
        ("ProvenanceRecord", "Provenance and chain of custody"),
        ("InvestigativeAction", "Each forensic step taken"),
        ("Tool", "Tools used with version information"),
        ("ObservableObject", "Evidence items"),
        ("ContentDataFacet", "Hash values for integrity verification"),
    ],
}

DOMAIN_CATEGORIES: list[dict[str, str | list[str]]] = [
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
        "description": "Investigative actions, tool runs, observations, and analysis events.",
        "keywords": ["action", "event", "observation", "analysis", "pattern",
                     "lifecycle"],
    },
    {
        "name": "investigation_metadata",
        "title": "Investigation Metadata",
        "description": "Investigations, case metadata, provenance, and authorization.",
        "keywords": ["investigation", "case", "provenance", "authorization",
                     "exhibit", "custody"],
    },
    {
        "name": "tool_information",
        "title": "Tool Information",
        "description": "Forensic and analysis tools, their versions, and configurations.",
        "keywords": ["tool", "version", "configuration", "build"],
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
]
