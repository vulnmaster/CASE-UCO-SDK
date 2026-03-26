# Network Artifact Extraction

> See [Recipe Index](INDEX.md) for all recipes.

Model network connections, DNS resolutions, IP addresses, and URLs extracted from forensic artifacts such as packet captures or log files.

## Key classes

| Class | Role |
|---|---|
| `IPAddress` + `IPAddressFacet` | An observed IP address (typed subclass of `ObservableObject`) |
| `DomainName` + `DomainNameFacet` | A domain name observed in DNS traffic |
| `NetworkConnection` + `NetworkConnectionFacet` | A network connection with src/dst, ports, time range |
| `TCPConnection` | TCP-specific connection (subclass of `NetworkConnection`) |
| `NetworkFlowFacet` | Packet/byte counts for a connection |
| `WifiAddress` + `WifiAddressFacet` | A WiFi MAC address |
| `MACAddress` + `MACAddressFacet` | Non-WiFi MACs (gateway, BSSID, infrastructure) |
| `NetworkInterface` + `NetworkInterfaceFacet` | The capture interface with MAC and IP bindings |
| `WirelessNetworkConnection` + `WirelessNetworkConnectionFacet` | WiFi network context (SSID, security mode, BSSID) |
| `Relationship` | Explicit machine-queryable links between objects (e.g., `Resolved_To`) |

## Pattern

Use typed subclasses (`IPAddress`, `DomainName`, `TCPConnection`) rather than bare `ObservableObject` — they carry the correct `@type` IRI and make the graph queryable by class. Link objects with explicit `Relationship` edges so downstream systems can traverse the graph without parsing human-readable names.

```
DomainName ──Resolved_To [observed]──▶ DomainName (CNAME)
                                           │
                                      Resolved_To [observed]
                                           │
                                           ▼
NetworkConnection                     IPAddress
    ├── NetworkConnectionFacet             ▲
    │       ├── src ──▶ IPAddress (local)  │
    │       └── dst ──▶ IPAddress (remote) ┘
    ├── NetworkFlowFacet (packet/byte counts)
    ├── ──Contained_Within [observed]──▶ File (pcap)
    └── ──Connected_To [inferred]──▶ DomainName

NetworkInterface ──Connected_To [configuration]──▶ MACAddress (gateway)

WirelessNetworkConnection
    ├── WirelessNetworkConnectionFacet (SSID, security, baseStation)
    └── ──Connected_To [configuration]──▶ MACAddress (base station)
```

### Relationship tags

Use the `tag` property on `Relationship` to classify the evidence basis:

| Tag | Meaning | Examples |
|---|---|---|
| `observed` | Directly evidenced in packet data | DNS resolutions, `Contained_Within` to capture file |
| `inferred` | Derived from analysis of observed facts | Connection-to-domain via DNS chain, WHOIS attribution |
| `configuration` | Network topology / infrastructure context | Interface-to-gateway, wireless-to-BSSID |

This distinction lets agents filter relationships by evidence strength without parsing human-readable descriptions.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ObservableObject, FileFacet, ContentDataFacet,
    IPAddress, IPAddressFacet,
    DomainName, DomainNameFacet,
    TCPConnection, NetworkConnectionFacet, NetworkFlowFacet,
    WifiAddress, WifiAddressFacet,
    MACAddress, MACAddressFacet,
    NetworkInterface, NetworkInterfaceFacet,
    WirelessNetworkConnection, WirelessNetworkConnectionFacet,
)
from case_uco.uco.types import Hash
from datetime import datetime, timezone

graph = CASEGraph()

# --- Capture file (so connections can reference it) ---

pcap_file = graph.create(ObservableObject,
    name="...",  # filename
    has_facet=[
        FileFacet(file_name=["..."], size_in_bytes=...),
        ContentDataFacet(hash=[Hash(
            hash_method=["SHA256"], hash_value="...",
        )]),
    ],
)

# --- Local interface context ---

local_mac = graph.create(WifiAddress,
    has_facet=[WifiAddressFacet(address_value="...")],  # from source
)

local_ip = graph.create(IPAddress,
    has_facet=[IPAddressFacet(address_value="...")],  # from source
)

interface = graph.create(NetworkInterface,
    name="...",  # e.g. "Wi-Fi" — from source
    has_facet=[NetworkInterfaceFacet(
        adapter_name="...",
        mac_address=local_mac,
        ip=[local_ip],
    )],
)

# --- Gateway MAC with directional Connected_To ---
# Use Connected_To (not generic Related_To) to preserve
# the semantic role: this MAC is the next-hop gateway.

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

# --- WiFi network context (when capturing on 802.11 interface) ---
# The WirelessNetworkConnectionFacet.baseStation is a string property,
# so also add a Relationship to the MACAddress node for graph traversal.

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

# --- Remote IP address ---

remote_ip = graph.create(IPAddress,
    has_facet=[IPAddressFacet(address_value="...")],  # from source
)

# --- DNS resolution chain (domain -> CNAME -> IP) ---

domain = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="...")],
)
cname = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="...")],
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

# --- TCP connection with flow statistics ---

connection = graph.create(TCPConnection,
    has_facet=[
        NetworkConnectionFacet(
            src=[local_ip],
            dst=[remote_ip],
            source_port=...,       # from source
            destination_port=...,  # from source
            start_time=datetime(..., tzinfo=timezone.utc),
            end_time=datetime(..., tzinfo=timezone.utc),
            is_active=False,
        ),
        NetworkFlowFacet(
            src_packets=...,  # from source
            src_bytes=...,
            dst_packets=...,
            dst_bytes=...,
        ),
    ],
)

# Connection contained within the capture file
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

graph.write("network_artifacts.jsonld")
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

var localIp = graph.Add(new IPAddress {
    HasFacet = { new IPAddressFacet { AddressValue = "..." } }
});

var remoteIp = graph.Add(new IPAddress {
    HasFacet = { new IPAddressFacet { AddressValue = "..." } }
});

var domain = graph.Add(new DomainName {
    HasFacet = { new DomainNameFacet { Value = "..." } }
});

graph.Add(new Relationship {
    Source = { domain }, Target = remoteIp,
    KindOfRelationship = "Resolved_To",
    IsDirectional = true,
});

var conn = graph.Add(new TCPConnection {
    HasFacet = {
        new NetworkConnectionFacet {
            Src = { localIp }, Dst = { remoteIp },
            SourcePort = ..., DestinationPort = ...,
        },
        new NetworkFlowFacet {
            SrcPackets = ..., SrcBytes = ...,
            DstPackets = ..., DstBytes = ...,
        },
    }
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var localIpFacet = new IPAddressFacet();
localIpFacet.setAddressValue("...");
var localIp = new IPAddress();
localIp.getHasFacet().add(localIpFacet);
graph.add(localIp);

var remoteIpFacet = new IPAddressFacet();
remoteIpFacet.setAddressValue("...");
var remoteIp = new IPAddress();
remoteIp.getHasFacet().add(remoteIpFacet);
graph.add(remoteIp);

var domainFacet = new DomainNameFacet();
domainFacet.setValue("...");
var domain = new DomainName();
domain.getHasFacet().add(domainFacet);
graph.add(domain);

var resolution = new Relationship();
resolution.getSource().add(domain);
resolution.setTarget(remoteIp);
resolution.setKindOfRelationship("Resolved_To");
resolution.setIsDirectional(true);
graph.add(resolution);

System.out.println(graph.serialize());
```

</details>

## Notes

- **Use typed subclasses**, not bare `ObservableObject`. `IPAddress`, `DomainName`, `TCPConnection`, `WifiAddress`, etc. carry distinct `@type` IRIs that enable SPARQL queries like `?x a uco-observable:IPAddress`.
- **DNS resolution** is modeled as a `Relationship` with `kind_of_relationship="Resolved_To"` from `DomainName` to `IPAddress`. This makes the link machine-queryable rather than embedded only in human-readable names.
- **CNAME chains** are modeled as chains of `Resolved_To` relationships: `DomainName` -> `DomainName` (CNAME) -> `IPAddress` (A/AAAA). Include a `description` on each noting the record type.
- **Connection-to-domain links** use `Relationship` with `kind_of_relationship="Connected_To"`. Include a `description` noting the basis (DNS, SNI, reverse DNS, etc.) so the link is traceable.
- **`Contained_Within`** from connections to the capture file makes every connection traceable to its source artifact. Always include this when connections are extracted from a specific file.
- **`NetworkFlowFacet`** adds packet/byte counts to a connection. Attach it alongside `NetworkConnectionFacet` on the same observable.
- **Gateway/infrastructure MACs** — Use `Connected_To` (directional: interface -> gateway) rather than generic `Related_To`. This preserves the semantic role of the MAC. Give the `MACAddress` a descriptive `name` (e.g., "Default gateway") so the role is clear even without following the relationship.
- For WiFi captures, use `WifiAddress` (subclass of `MACAddress`) for WiFi-specific MACs. Use plain `MACAddress` for non-WiFi MACs (gateway, BSSID, etc.).

### Relationship tagging

**Always tag relationships** with `tag=["observed"]`, `tag=["inferred"]`, or `tag=["configuration"]` to classify their evidence basis. This is critical because the same `kind_of_relationship` (e.g., `Connected_To`) can mean very different things:

- A `Connected_To` from a TCP connection to a domain is an **inference** based on DNS evidence — the connection itself contains no domain name.
- A `Connected_To` from an interface to a gateway MAC is a **configuration** fact about network topology.
- A `Resolved_To` from a domain to an IP is an **observed** DNS response extracted from packet data.

Without tags, agents and downstream systems cannot distinguish these semantics programmatically. The `description` field should explain the specific basis in prose, but `tag` makes the distinction machine-queryable via SPARQL: `?rel uco-core:tag "observed"`.

### WiFi network context and identity deduplication

When modeling WiFi captures, avoid identity duplication between `WirelessNetworkConnectionFacet.baseStation` (a string property) and `MACAddress` nodes. The ontology requires `baseStation` as a string, so:

1. Keep the literal string value in `WirelessNetworkConnectionFacet.baseStation`.
2. **Also** create a `Relationship` from the `WirelessNetworkConnection` to the `MACAddress` node (`Connected_To`, tag `configuration`).

This gives agents a traversable graph link from the wireless connection to the same MAC object used elsewhere (e.g., as the gateway), rather than requiring string matching across disparate properties.

### Further reading

- For the full investigation pattern (case metadata, legal authorization, provenance, analysis layer), see [network-investigation.md](network-investigation.md).
