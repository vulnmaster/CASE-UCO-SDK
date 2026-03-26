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

### Forensic workflows

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Modeling a Forensic Tool and Its Output | [forensic-tool.md](forensic-tool.md) | Create an investigation with a tool and investigative action | — |
| Configured Tools | [configured-tool.md](configured-tool.md) | Tool configurations, rulesets, ConfiguredTool | [configured_tool](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/configured_tool) |
| Chain of Custody | [chain-of-custody.md](chain-of-custody.md) | Track evidence handling, transfers, and provenance records | — |
| Forensic Analysis and Classification | [analysis.md](analysis.md) | Malware RE, automated artifact classification with confidence scores | [analysis](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/analysis) |
| Forensic Investigation Lifecycle | [forensic-lifecycle.md](forensic-lifecycle.md) | Ordered phases (survey, preservation, examination, analysis, reporting) | [forensic_lifecycle](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/forensic_lifecycle) |
| Network Investigation with Bundle | [network-investigation.md](network-investigation.md) | Full investigation with warrant, PCAP extraction, provenance | [network_connection](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/network_connection) |
| Spear Phishing and Attack Narratives | [spear-phishing.md](spear-phishing.md) | Attack chain modeling with extended ontology patterns | [spear_phishing](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/spear_phishing) |

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
| Round-Trip: Serialize and Deserialize | [round-trip.md](round-trip.md) | Write a graph to JSON-LD and load it back with typed deserialization | — |
| Managing Large Datasets | [large-datasets.md](large-datasets.md) | Partition large evidence sets by forensic boundary | — |
| Existence Intervals and Temporal Modeling | [existence-intervals.md](existence-intervals.md) | OWL-Time, gUFO, and BFO temporal patterns | [existence_intervals](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/existence_intervals) |

### Contributing to the ontology

| Recipe | File | Description | CASE-Example |
|---|---|---|---|
| Proposing Changes to CASE/UCO | [change-proposal.md](change-proposal.md) | Identify gaps, check existing proposals, and draft change proposals | — |
