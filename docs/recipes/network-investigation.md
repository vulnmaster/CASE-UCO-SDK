# Network Investigation with Packet Capture

> See [Recipe Index](INDEX.md) for all recipes.

Model a complete network investigation from packet capture — case metadata, the capture action, observed network artifacts, DNS resolution chains, and a separate analysis layer for inferences. Based on [CASE-Examples/network_connection](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/network_connection).

This extends the basic [network-artifacts recipe](network-artifacts.md) with investigation context, the three-layer model, and analysis separation.

## Three-layer model

Network investigations benefit from separating concerns into three distinct layers:

| Layer | What it captures | CASE/UCO classes |
|---|---|---|
| **Acquisition** | The capture file, hashes, tool, interface, host, timestamps | `InvestigativeAction`, `Tool`, `FileFacet`, `ContentDataFacet`, `NetworkInterfaceFacet` |
| **Observed network** | Raw facts from the capture: IPs, ports, flows, DNS answers, MACs | `IPAddress`, `DomainName`, `TCPConnection`, `NetworkConnectionFacet`, `NetworkFlowFacet`, `Relationship` |
| **Analysis** | Inferences and attributions: "likely Dropbox," "update traffic" | `InvestigativeAction` (per-group analysis), `ArtifactClassification`, confidence scores |

This separation ensures that observed facts remain untainted by interpretation, and that every inference is traceable to a method and basis.

## Key classes

| Class | Role |
|---|---|
| `Investigation` | The case container — created **last** so it can link to all objects |
| `Authorization` | Legal authority (warrant, subpoena) |
| `InvestigativeAction` | The capture action _and_ separate per-group analysis actions |
| `Tool` / `AnalyticTool` | The capture tool and the analysis tool |
| `NetworkConnection` / `TCPConnection` | Captured connections (use typed subclass) |
| `NetworkConnectionFacet` | Connection details (src/dst IP refs, ports, time) |
| `NetworkFlowFacet` | Packet and byte counts per direction |
| `IPAddress` + `IPAddressFacet` | Observed IP addresses |
| `DomainName` + `DomainNameFacet` | Observed domain names |
| `WifiAddress` + `WifiAddressFacet` | WiFi MAC addresses |
| `MACAddress` + `MACAddressFacet` | Non-WiFi MACs (gateway, BSSID, infrastructure) |
| `NetworkInterface` + `NetworkInterfaceFacet` | Capture interface with MAC/IP bindings |
| `WirelessNetworkConnectionFacet` | WiFi SSID, security mode, base station |
| `Relationship` | Explicit edges: `Resolved_To`, `Connected_To`, `Contained_Within` |
| `ArtifactClassificationResultFacet` | Classification results with confidence |
| `ProvenanceRecord` | Links actions to their inputs and outputs |

## Pattern

```
LAYER 1: Acquisition
    InvestigativeAction (capture)
        ├── performer ──▶ Identity
        ├── instrument ──▶ Tool (Wireshark)
        ├── result ──▶ File (pcapng) with FileFacet + ContentDataFacet
        └── environment ──▶ NetworkInterface
                                ├── mac_address ──▶ WifiAddress
                                ├── ip ──▶ IPAddress (local)
                                └── ──Connected_To [configuration]──▶ MACAddress (gateway)

    WirelessNetworkConnection
        ├── WirelessNetworkConnectionFacet (SSID, security, baseStation)
        └── ──Connected_To [configuration]──▶ MACAddress (same gateway node)

LAYER 2: Observed network (raw facts only — no interpretation)
    All relationships tagged [observed]

    DomainName ──Resolved_To──▶ DomainName (CNAME)
    DomainName ──Resolved_To──▶ IPAddress  (A/AAAA)
    TCPConnection
        ├── NetworkConnectionFacet (src/dst IP refs, ports, timestamps)
        ├── NetworkFlowFacet (packet/byte counts)
        └── ──Contained_Within──▶ File (pcapng)

    Inferred from observed facts, tagged [inferred]:
    TCPConnection ──Connected_To──▶ DomainName (when DNS evidence exists)

LAYER 3: Analysis (one action per attribution group)
    InvestigativeAction (analysis)
        ├── performer ──▶ Identity
        ├── instrument ──▶ AnalyticTool
        ├── object ──▶ [connections + supporting IPs + DNS evidence]
        ├── result ──▶ ObservableObject + ArtifactClassificationResultFacet
        └── was_informed_by ──▶ InvestigativeAction (capture)

Investigation (created last — root of the navigable tree)
    ├── created_by ──▶ Identity
    ├── relevant_authorization ──▶ Authorization
    └── object ──▶ [capture action, analysis actions, provenance, key artifacts]
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import (
    Investigation, InvestigativeAction, ProvenanceRecord, Authorization,
)
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.tool import Tool, AnalyticTool
from case_uco.uco.observable import (
    ObservableObject, FileFacet, ContentDataFacet,
    IPAddress, IPAddressFacet,
    DomainName, DomainNameFacet,
    TCPConnection, NetworkConnection,
    NetworkConnectionFacet, NetworkFlowFacet,
    NetworkInterface, NetworkInterfaceFacet,
    WifiAddress, WifiAddressFacet,
    MACAddress, MACAddressFacet,
    WirelessNetworkConnection, WirelessNetworkConnectionFacet,
)
from case_uco.uco.analysis import (
    ArtifactClassificationResultFacet, ArtifactClassification,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))  # from source
graph = CASEGraph()


# ═══════════════════════════════════════════
# LAYER 1: Acquisition
# ═══════════════════════════════════════════

# Legal authorization
warrant = graph.create(Authorization,
    name="...",
    authorization_type="...",
    authorization_identifier=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
)

examiner = graph.create(Identity, name="...")  # from source

# Capture tool
wireshark = graph.create(Tool,
    name="...",     # e.g. "Wireshark" — from source
    version="...",  # from source
    tool_type="Network Protocol Analyzer",
)

# The capture file
pcap_file = graph.create(ObservableObject,
    name="...",  # filename
    has_facet=[
        FileFacet(
            file_name=["..."],
            extension="pcapng",
            size_in_bytes=...,  # from source
        ),
        ContentDataFacet(
            size_in_bytes=...,
            hash=[Hash(
                hash_method=["SHA256"],
                hash_value="...",  # from source
            )],
        ),
    ],
)

# Capture interface
local_mac = graph.create(WifiAddress,
    has_facet=[WifiAddressFacet(address_value="...")],
)
local_ip = graph.create(IPAddress,
    has_facet=[IPAddressFacet(address_value="...")],
)
interface = graph.create(NetworkInterface,
    name="...",
    has_facet=[NetworkInterfaceFacet(
        adapter_name="...",
        mac_address=local_mac,
        ip=[local_ip],
    )],
)

# Gateway MAC — use Connected_To to preserve the gateway role
gateway_mac = graph.create(MACAddress,
    name="Default gateway",
    has_facet=[MACAddressFacet(address_value="...")],
)
graph.create(Relationship,
    source=[interface], target=gateway_mac,
    kind_of_relationship="Connected_To",
    is_directional=True,
    tag=["configuration"],
    description=["WiFi interface default gateway"],
)

# WiFi network context — link to the MACAddress node for graph traversal
# rather than relying solely on the baseStation string
wifi_network = graph.create(WirelessNetworkConnection,
    has_facet=[WirelessNetworkConnectionFacet(
        ssid="...",                                     # from source
        wireless_network_security_mode=["WPA2-PSK"],    # from source
        base_station="...",                              # BSSID string
    )],
)
graph.create(Relationship,
    source=[wifi_network], target=gateway_mac,
    kind_of_relationship="Connected_To",
    is_directional=True,
    tag=["configuration"],
    description=["Wireless network base station (BSSID) — links to the "
                  "same MACAddress node used as the gateway"],
)

# The capture action
capture_action = graph.create(InvestigativeAction,
    name="Network packet capture",
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=examiner,
    instrument=[wireshark],
    environment=interface,
    result=[pcap_file],
)


# ═══════════════════════════════════════════
# LAYER 2: Observed network (raw facts)
# ═══════════════════════════════════════════

# Remote IPs
remote_ip = graph.create(IPAddress,
    has_facet=[IPAddressFacet(address_value="...")],
)

# DNS resolution: domain -> CNAME -> IP
domain = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="...")],
)
cname = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="...")],  # CNAME target
)
graph.create(Relationship,
    source=[domain], target=cname,
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS CNAME record observed in capture"],
)
graph.create(Relationship,
    source=[cname], target=remote_ip,
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS A record observed in capture"],
)

# TCP connection — raw observed fact, no interpretation in the name
connection = graph.create(TCPConnection,
    has_facet=[
        NetworkConnectionFacet(
            src=[local_ip],
            dst=[remote_ip],
            source_port=...,
            destination_port=...,
            start_time=datetime(..., tzinfo=tz),
            end_time=datetime(..., tzinfo=tz),
            is_active=False,
        ),
        NetworkFlowFacet(
            src_packets=...,
            src_bytes=...,
            dst_packets=...,
            dst_bytes=...,
        ),
    ],
)

# Connection contained within the PCAP file
graph.create(Relationship,
    source=[connection], target=pcap_file,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    tag=["observed"],
)

# Connection associated with domain (inferred from DNS evidence)
graph.create(Relationship,
    source=[connection], target=domain,
    kind_of_relationship="Connected_To",
    is_directional=True,
    tag=["inferred"],
    description=["Association inferred from DNS A-record resolution observed in capture"],
)


# ═══════════════════════════════════════════
# LAYER 3: Analysis (per-group, evidence-backed)
#
# Each attribution follows the target pattern:
#   raw observables (connections + IPs + DNS)
#     → analysis action (method, tool, performer)
#       → asserted result (classification + confidence)
# ═══════════════════════════════════════════

analysis_tool = graph.create(AnalyticTool,
    name="...",     # e.g. "IP WHOIS / DNS attribution"
    version="...",
    tool_type="Traffic Attribution",
)

# One analysis action per attribution group — each explicitly
# lists the connections, IPs, and DNS evidence it relied on.
attribution_result = graph.create(ObservableObject,
    name="...",  # e.g. "Dell Update Service attribution"
    has_facet=[ArtifactClassificationResultFacet(
        classification=[
            ArtifactClassification(
                class_=["..."],                  # e.g. "Dell Update Service"
                classification_confidence=...,   # 0.0-1.0
            ),
        ],
    )],
)

analysis_action = graph.create(InvestigativeAction,
    name="...",  # e.g. "Dell traffic attribution"
    description=["..."],  # cite the specific evidence basis
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
    performer=examiner,
    instrument=[analysis_tool],
    object=[connection, remote_ip, domain],  # connections + supporting evidence
    result=[attribution_result],
    was_informed_by=[capture_action],  # chains to the acquisition step
)


# ═══════════════════════════════════════════
# Provenance and Investigation (created last)
# ═══════════════════════════════════════════

provenance = graph.create(ProvenanceRecord,
    name="...",
    description=["..."],
    exhibit_number="...",
    object=[
        pcap_file, interface, connection, domain, remote_ip,
        capture_action, analysis_action, attribution_result,
    ],
)

# Investigation is the root node — created last so it can
# reference all actions and the provenance record via object.
investigation = graph.create(Investigation,
    name="...",
    description=["..."],
    focus=["Network Traffic Analysis"],
    investigation_form=["incident"],  # or "case", "suspicious-activity"
    created_by=examiner,
    relevant_authorization=[warrant],
    object=[
        capture_action, analysis_action,
        provenance,
        pcap_file, interface,
    ],
)

graph.write("network_investigation.jsonld")
```

</details>

## Notes

### Three-layer separation

- **Acquisition layer**: Model the capture action, tool, file, hashes, and interface. This is the "chain of custody" for the digital evidence. Use `InvestigativeAction.environment` to link the action to the `NetworkInterface` it was performed on.
- **Observed network layer**: Model only raw facts extracted from the capture — IPs, ports, flows, DNS answers. Do not embed analytic interpretation in object names (avoid naming a connection "Microsoft Update Traffic" when the observed fact is "172.20.10.3:54636 -> 20.44.10.122:443").
- **Analysis layer**: Model inferences and attributions as separate `InvestigativeAction` results. Create **one analysis action per attribution group** so each conclusion has its own scoped evidence chain. Use `ArtifactClassificationResultFacet` with confidence scores. This preserves _why_ an inference was made, _what evidence_ supports it, and _how confident_ the assertion is.

### Evidence-backed analysis assertions

Each analysis action should follow the target pattern:

```
raw observables (connections + IPs + DNS evidence)
  → InvestigativeAction (method, tool, performer, description of basis)
    → asserted result (ArtifactClassificationResultFacet + confidence)
```

Concrete steps:
1. **Scope `object`** to the specific connections, IP addresses, and domain names that support the conclusion — not all connections in the capture.
2. **Cite the basis** in `description`: "IP registered to Dell Inc. (WHOIS)" or "DNS chain resolved to this address." Note when evidence is absent: "No DNS query observed — attribution based solely on IP registration."
3. **Chain with `was_informed_by`** back to the capture action, so the provenance trail is: Investigation → analysis action → was_informed_by → capture action → result → pcap file.
4. **Set `classification_confidence`** to reflect the strength of the evidence (DNS + WHOIS = high; WHOIS-only = moderate; analyst judgment = lower).

### Relationship tagging and semantic precision

Use the `tag` property on every `Relationship` to classify its evidence basis:

| Tag | Meaning | Examples |
|---|---|---|
| `observed` | Directly evidenced in packet data | DNS `Resolved_To`, `Contained_Within` capture file |
| `inferred` | Derived from analysis of observed facts | Connection `Connected_To` domain via DNS chain |
| `configuration` | Network topology / infrastructure context | Interface `Connected_To` gateway MAC, wireless `Connected_To` BSSID |

This matters because the same `kind_of_relationship` can carry very different semantics. A `Connected_To` from a TCP connection to a domain (inferred from DNS evidence) is fundamentally different from a `Connected_To` from an interface to a gateway MAC (observed network configuration). Without `tag`, agents cannot distinguish these programmatically — they must parse prose in `description`.

### Explicit relationships

- `Resolved_To` from `DomainName` to `IPAddress` — models DNS A/AAAA resolution. Chain multiple `Resolved_To` edges for CNAME chains. Include a `description` noting the record type (CNAME, A, AAAA). Tag as `observed`.
- `Connected_To` from `TCPConnection` to `DomainName` — links a connection to the domain it was associated with. Include a `description` noting the basis (DNS, SNI, reverse DNS, etc.). Tag as `inferred` because the connection itself does not contain a domain name.
- `Connected_To` from `NetworkInterface` to `MACAddress` (gateway) — preserves the semantic role of infrastructure MACs. Use directional (interface → gateway) rather than generic `Related_To`. Give the `MACAddress` a descriptive `name` (e.g., "Default gateway"). Tag as `configuration`.
- `Contained_Within` from connection to PCAP file — makes every connection traceable to its source artifact. Tag as `observed`.

### Investigation as the navigable root

Create the `Investigation` node **last**, after all other objects exist. This lets you populate `Investigation.object` with references to the capture action, analysis actions, provenance record, and key artifacts. The investigation becomes the entry point for graph traversal — any downstream system can start at the Investigation and reach every part of the graph.

Key properties:
- `object` — references to actions, provenance, and key artifacts
- `created_by` — the examiner identity
- `relevant_authorization` — legal basis (warrant, subpoena)
- `focus` — topical focus (e.g., "Network Traffic Analysis")
- `investigation_form` — uses `InvestigationFormVocab`: `case`, `incident`, `suspicious-activity`

### WiFi-specific metadata and identity deduplication

When capturing on a WiFi interface, model the wireless network context with `WirelessNetworkConnection` + `WirelessNetworkConnectionFacet`:

- `ssid` — the network SSID
- `wireless_network_security_mode` — uses `WirelessNetworkSecurityModeVocab`: `None`, `WEP`, `WPA`, `WPA2-PSK`, `WPA2-Enterprise`, `WPA3-PSK`, `WPA3-Enterprise`
- `base_station` — the BSSID (string property in the ontology)

**Identity deduplication**: The `baseStation` property is typed as a string in the ontology, but you may also model the same MAC address as a `MACAddress` node (e.g., the gateway). To avoid identity duplication and strengthen graph consistency:

1. Keep the literal string in `WirelessNetworkConnectionFacet.baseStation` (the ontology requires it).
2. **Also** add a `Relationship` from the `WirelessNetworkConnection` to the `MACAddress` node with `kind_of_relationship="Connected_To"` and `tag=["configuration"]`.

This gives agents a traversable graph link rather than requiring string matching across disparate properties. The pattern applies whenever a string-typed facet property refers to an entity also modeled as a first-class node.

### Structured attribution evidence

The analysis layer benefits from making evidence support as explicit as possible. While `description` captures the prose rationale, structure the attribution chain so agents can traverse it programmatically:

```
observed flow/IP/domain set (scoped in object)
  → supporting Resolved_To / Contained_Within relationships (tagged [observed])
    → InvestigativeAction (method in instrument, basis in description)
      → ArtifactClassificationResultFacet (class + confidence)
        → Investigation.object membership
```

Key practices:
- **Scope `object`** to only the connections, IPs, and domains that support this specific conclusion — not the entire capture.
- **Cite negative evidence** in `description` when relevant: "No DNS query observed — attribution based solely on IP registration." This makes the basis honest and traceable.
- **Calibrate confidence** to evidence strength: DNS + WHOIS = high (~0.85+), WHOIS-only = moderate (~0.7-0.8), known IP ranges = moderate, analyst judgment alone = lower (~0.5-0.6).
- **Chain `was_informed_by`** back to the capture action so the full provenance trail is machine-traversable: Investigation → analysis action → was_informed_by → capture action → result → pcap file.

### Vocabulary values

- Hash methods must use `HashNameVocab` values: `MD5`, `SHA1`, `SHA256`, `SHA384`, `SHA512`, `SSDEEP`, etc. (not `SHA-256`).
- Relationship kinds use `ObservableObjectRelationshipVocab`: `Resolved_To`, `Connected_To`, `Contained_Within`, etc.
- Relationship tags use convention values: `observed`, `inferred`, `configuration`.
- Investigation forms use `InvestigationFormVocab`: `case`, `incident`, `suspicious-activity`.
- Wireless security modes use `WirelessNetworkSecurityModeVocab`: `None`, `WEP`, `WPA`, `WPA2-PSK`, `WPA2-Enterprise`, `WPA3-PSK`, `WPA3-Enterprise`.
