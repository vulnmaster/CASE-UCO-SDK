from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship
from case_uco.uco.tool import Tool, AnalyticTool
from case_uco.uco.observable import (
    ObservableObject,
    FileFacet,
    ContentDataFacet,
    IPAddress,
    IPAddressFacet,
    DomainName,
    DomainNameFacet,
    TCPConnection,
    NetworkConnection,
    NetworkConnectionFacet,
    NetworkFlowFacet,
    NetworkInterface,
    NetworkInterfaceFacet,
    WifiAddress,
    WifiAddressFacet,
    MACAddress,
    MACAddressFacet,
    WirelessNetworkConnection,
    WirelessNetworkConnectionFacet,
)
from case_uco.uco.analysis import ArtifactClassificationResultFacet, ArtifactClassification
from case_uco.uco.types import Hash
from datetime import datetime, timezone

graph = CASEGraph()


# ═══════════════════════════════════════════════════════════
# LAYER 1: Acquisition
# ═══════════════════════════════════════════════════════════

examiner = graph.create(Identity, name="John Doe")

wireshark = graph.create(Tool,
    name="Wireshark",
    version="4.6.4",
    tool_type="Network Protocol Analyzer",
)

pcap_file = graph.create(ObservableObject,
    name="wifi_capture.pcapng",
    has_facet=[
        FileFacet(
            file_name=["wifi_capture.pcapng"],
            extension="pcapng",
            size_in_bytes=344968,
        ),
        ContentDataFacet(
            mime_type=["application/vnd.tcpdump.pcap"],
            size_in_bytes=344968,
            hash=[
                Hash(hash_method=["SHA256"],
                     hash_value="fe3fca634710858b80a4a4aa57717a6bd3399f1a0688588f07115a5c862741f8"),
                Hash(hash_method=["MD5"],
                     hash_value="dfa5f62d0c597c240ee4c934c593acc4"),
            ],
        ),
    ],
)

# --- Capture interface ---

local_mac = graph.create(WifiAddress,
    has_facet=[WifiAddressFacet(address_value="de:b5:4f:0e:ed:64")],
)

local_ip = graph.create(IPAddress,
    has_facet=[IPAddressFacet(address_value="172.20.10.3")],
)

wifi_interface = graph.create(NetworkInterface,
    name="WiFi Adapter",
    has_facet=[NetworkInterfaceFacet(
        adapter_name="Wi-Fi",
        mac_address=local_mac,
        ip=[local_ip],
    )],
)

# --- Gateway MAC ---
# The interface Connected_To the gateway (not generic Related_To).
# This preserves the semantic role: this MAC is the next-hop gateway
# through which all captured traffic was routed.

gateway_mac = graph.create(MACAddress,
    name="Default gateway",
    has_facet=[MACAddressFacet(address_value="d4:ab:61:5c:3a:69")],
)

graph.create(Relationship,
    source=[wifi_interface], target=gateway_mac,
    kind_of_relationship="Connected_To",
    is_directional=True,
    tag=["configuration"],
    description=["WiFi interface default gateway — all captured traffic routed through this MAC"],
)

# --- WiFi network context ---
# The WirelessNetworkConnectionFacet.baseStation is a string property in the
# ontology, so we keep the literal value there. But to avoid identity duplication
# and strengthen graph consistency, we also add a Relationship from the wireless
# connection to the MACAddress node so agents can traverse from one to the other.

wifi_network = graph.create(WirelessNetworkConnection,
    has_facet=[WirelessNetworkConnectionFacet(
        base_station="d4:ab:61:5c:3a:69",
    )],
)

graph.create(Relationship,
    source=[wifi_network], target=gateway_mac,
    kind_of_relationship="Connected_To",
    is_directional=True,
    tag=["configuration"],
    description=["Wireless network base station (BSSID) — links the "
                  "WirelessNetworkConnection to the same MACAddress node used "
                  "as the gateway, avoiding identity duplication"],
)

# --- The capture action ---

capture_action = graph.create(InvestigativeAction,
    name="WiFi packet capture",
    description=["Live capture of 338 packets on WiFi interface over ~3.4 seconds"],
    start_time=datetime(2026, 3, 25, 22, 30, 29, tzinfo=timezone.utc),
    end_time=datetime(2026, 3, 25, 22, 30, 33, tzinfo=timezone.utc),
    performer=examiner,
    instrument=[wireshark],
    environment=wifi_interface,
    result=[pcap_file],
)


# ═══════════════════════════════════════════════════════════
# LAYER 2: Observed Network (raw facts only)
# ═══════════════════════════════════════════════════════════

remote_ips = {}
for addr in [
    "20.44.10.122", "104.18.18.125", "143.166.28.100",
    "162.125.40.1", "13.248.241.7", "99.83.165.34",
    "184.28.149.222", "13.73.244.6",
    "150.171.27.11", "150.171.28.11",
]:
    remote_ips[addr] = graph.create(IPAddress,
        has_facet=[IPAddressFacet(address_value=addr)],
    )

multicast_ip = graph.create(IPAddress,
    has_facet=[IPAddressFacet(address_value="239.255.255.250")],
)

ipv6_addrs = {}
for addr in [
    "2600:381:bd19:7986:1cad:b089:30e3:3540",
    "2603:1063:12::302",
    "2620:1ec:33::11",
    "2620:100:6017:19::a27d:213",
    "2620:100:6017:13::a27d:20d",
    "fe80::dcb5:4fff:fe0e:ed64",
    "fe80::8735:dbf2:3684:6d3a",
]:
    ipv6_addrs[addr] = graph.create(IPAddress,
        has_facet=[IPAddressFacet(address_value=addr)],
    )

# --- DNS domain names ---

edge_domain = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="edge.microsoft.com")],
)
edge_cname1 = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="edge-microsoft-com.ax-0002.ax-msedge.net")],
)
edge_cname2 = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="ax-0002.ax-msedge.net")],
)

dell_domain = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="dellupdater.dell.com")],
)
dell_cname1 = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="dellupdater.dell.com.edgekey.net")],
)
dell_cname2 = graph.create(DomainName,
    has_facet=[DomainNameFacet(value="e13665.g.akamaiedge.net")],
)

# --- DNS resolution chains (Resolved_To relationships) ---

# edge.microsoft.com -> CNAME -> CNAME -> A/AAAA
graph.create(Relationship,
    source=[edge_domain], target=edge_cname1,
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS CNAME record observed in capture"],
)
graph.create(Relationship,
    source=[edge_cname1], target=edge_cname2,
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS CNAME record observed in capture"],
)
graph.create(Relationship,
    source=[edge_cname2], target=remote_ips["150.171.27.11"],
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS A record observed in capture"],
)
graph.create(Relationship,
    source=[edge_cname2], target=remote_ips["150.171.28.11"],
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS A record observed in capture"],
)
graph.create(Relationship,
    source=[edge_cname2], target=ipv6_addrs["2620:1ec:33::11"],
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS AAAA record observed in capture"],
)

# dellupdater.dell.com -> CNAME -> CNAME -> A
graph.create(Relationship,
    source=[dell_domain], target=dell_cname1,
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS CNAME record observed in capture"],
)
graph.create(Relationship,
    source=[dell_cname1], target=dell_cname2,
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS CNAME record observed in capture"],
)
graph.create(Relationship,
    source=[dell_cname2], target=remote_ips["184.28.149.222"],
    kind_of_relationship="Resolved_To",
    is_directional=True,
    tag=["observed"],
    description=["DNS A record observed in capture"],
)

# --- TCP connections (raw facts, no interpretive names) ---

tcp_flows = [
    # (src_ip, sport, dst_ip, dport, s_pkts, s_bytes, d_pkts, d_bytes, start_time, end_time)
    ("172.20.10.3", 54636, "20.44.10.122",  443, 13, 3241, 12, 8060,
     datetime(2026, 3, 25, 22, 30, 29, 610579, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 32, 469575, tzinfo=timezone.utc)),
    ("172.20.10.3", 59859, "104.18.18.125", 443, 11, 2982,  9,  857,
     datetime(2026, 3, 25, 22, 30, 29, 756515, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 31, 343395, tzinfo=timezone.utc)),
    ("172.20.10.3", 59858, "104.18.18.125", 443, 10, 3315,  8,  733,
     datetime(2026, 3, 25, 22, 30, 29, 755907, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 31, 358822, tzinfo=timezone.utc)),
    ("172.20.10.3", 61105, "143.166.28.100", 443,  7, 1113, 10, 2872,
     datetime(2026, 3, 25, 22, 30, 30, 129698, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 31, 281800, tzinfo=timezone.utc)),
    ("172.20.10.3", 61106, "143.166.28.100", 443,  7, 3591,  8, 2211,
     datetime(2026, 3, 25, 22, 30, 31, 389558, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 32, 844602, tzinfo=timezone.utc)),
    ("172.20.10.3", 54635, "143.166.28.100", 443,  4,  390,  6,  993,
     datetime(2026, 3, 25, 22, 30, 29, 766878, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 32, 545487, tzinfo=timezone.utc)),
    ("172.20.10.3", 59930, "13.248.241.7",  443,  2,  147,  2,  147,
     datetime(2026, 3, 25, 22, 30, 29, 689109, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 29, 969327, tzinfo=timezone.utc)),
    ("172.20.10.3", 59940, "13.248.241.7",  443,  2,  147,  2,  147,
     datetime(2026, 3, 25, 22, 30, 30, 269639, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 30, 588915, tzinfo=timezone.utc)),
    ("172.20.10.3", 59941, "13.248.241.7",  443,  2,  147,  2,  147,
     datetime(2026, 3, 25, 22, 30, 30, 269639, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 30, 588495, tzinfo=timezone.utc)),
    ("172.20.10.3", 59944, "99.83.165.34",  443,  2,  147,  2,  147,
     datetime(2026, 3, 25, 22, 30, 30, 381768, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 30, 666606, tzinfo=timezone.utc)),
    ("172.20.10.3", 56153, "99.83.165.34",  443,  2,  147,  2,  147,
     datetime(2026, 3, 25, 22, 30, 32, 357179, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 32, 686803, tzinfo=timezone.utc)),
    ("172.20.10.3", 54632, "162.125.40.1",  443,  0,    0,  2,  132,
     datetime(2026, 3, 25, 22, 30, 29, 637530, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 31, 862263, tzinfo=timezone.utc)),
    ("172.20.10.3", 54633, "162.125.40.1",  443,  0,    0,  2,  132,
     datetime(2026, 3, 25, 22, 30, 29, 654490, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 31, 863166, tzinfo=timezone.utc)),
    ("172.20.10.3", 61107, "184.28.149.222", 443,  1,   66,  1,   66,
     datetime(2026, 3, 25, 22, 30, 32, 782179, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 33, 14248, tzinfo=timezone.utc)),
    ("172.20.10.3", 54630, "162.125.40.1",  443,  0,    0,  1,   66,
     datetime(2026, 3, 25, 22, 30, 31, 399802, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 31, 399802, tzinfo=timezone.utc)),
    ("172.20.10.3", 54634, "162.125.40.1",  443,  0,    0,  1,   54,
     datetime(2026, 3, 25, 22, 30, 29, 769328, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 29, 769328, tzinfo=timezone.utc)),
    ("172.20.10.3", 56653, "13.73.244.6",   443,  0,    0,  1,   54,
     datetime(2026, 3, 25, 22, 30, 30, 881884, tzinfo=timezone.utc),
     datetime(2026, 3, 25, 22, 30, 30, 881884, tzinfo=timezone.utc)),
]

tcp_connections = []
for src_ip, sport, dst_ip, dport, s_pkts, s_bytes, d_pkts, d_bytes, t_start, t_end in tcp_flows:
    src_obj = local_ip if src_ip == "172.20.10.3" else remote_ips.get(src_ip)
    dst_obj = remote_ips.get(dst_ip) if dst_ip != "172.20.10.3" else local_ip

    conn = graph.create(TCPConnection,
        has_facet=[
            NetworkConnectionFacet(
                src=[src_obj] if src_obj else [],
                dst=[dst_obj] if dst_obj else [],
                source_port=sport,
                destination_port=dport,
                start_time=t_start,
                end_time=t_end,
                is_active=False,
            ),
            NetworkFlowFacet(
                src_packets=s_pkts,
                src_bytes=s_bytes,
                dst_packets=d_pkts,
                dst_bytes=d_bytes,
            ),
        ],
    )
    tcp_connections.append(conn)

ws_discovery = graph.create(NetworkConnection,
    has_facet=[
        NetworkConnectionFacet(
            src=[local_ip],
            dst=[multicast_ip],
            source_port=57992,
            destination_port=3702,
            is_active=False,
        ),
        NetworkFlowFacet(
            src_packets=4,
            src_bytes=2792,
        ),
    ],
)

# --- Containment and association relationships ---

for conn in tcp_connections:
    graph.create(Relationship,
        source=[conn], target=pcap_file,
        kind_of_relationship="Contained_Within",
        is_directional=True,
        tag=["observed"],
    )

graph.create(Relationship,
    source=[ws_discovery], target=pcap_file,
    kind_of_relationship="Contained_Within",
    is_directional=True,
    tag=["observed"],
)

conn_dell = tcp_connections[13]  # idx 13 = 184.28.149.222:443
graph.create(Relationship,
    source=[conn_dell], target=dell_domain,
    kind_of_relationship="Connected_To",
    is_directional=True,
    tag=["inferred"],
    description=["Association inferred from DNS CNAME chain: dellupdater.dell.com -> "
                  "dellupdater.dell.com.edgekey.net -> e13665.g.akamaiedge.net -> 184.28.149.222"],
)


# ═══════════════════════════════════════════════════════════
# LAYER 3: Analysis (per-group, evidence-backed)
#
# Each attribution follows the target pattern:
#   raw observables (connections + IPs + DNS)
#     → analysis action (method, tool, performer)
#       → asserted result (classification + confidence)
# ═══════════════════════════════════════════════════════════

analysis_tool = graph.create(AnalyticTool,
    name="IP WHOIS / DNS attribution",
    tool_type="Traffic Attribution",
    description=["Service attribution based on IP address WHOIS registration and DNS domain names"],
)

# --- Dell attribution ---
# Evidence: connections to 143.166.28.100 (WHOIS: Dell Inc.) and
# 184.28.149.222 (DNS: dellupdater.dell.com -> ... -> 184.28.149.222)

dell_conns = [tcp_connections[i] for i in (3, 4, 5, 13)]
dell_evidence_ips = [remote_ips["143.166.28.100"], remote_ips["184.28.149.222"]]
dell_evidence_dns = [dell_domain, dell_cname1, dell_cname2]

dell_attribution = graph.create(ObservableObject,
    name="Dell Update Service attribution",
    has_facet=[ArtifactClassificationResultFacet(
        classification=[ArtifactClassification(
            class_=["Dell Update Service"],
            classification_confidence=0.85,
        )],
    )],
)

dell_analysis = graph.create(InvestigativeAction,
    name="Dell traffic attribution",
    description=["IP 143.166.28.100 registered to Dell Inc. (WHOIS). "
                  "IP 184.28.149.222 reached via DNS chain dellupdater.dell.com "
                  "-> dellupdater.dell.com.edgekey.net -> e13665.g.akamaiedge.net."],
    start_time=datetime(2026, 3, 25, 22, 35, 0, tzinfo=timezone.utc),
    end_time=datetime(2026, 3, 25, 22, 36, 0, tzinfo=timezone.utc),
    performer=examiner,
    instrument=[analysis_tool],
    object=dell_conns + dell_evidence_ips + dell_evidence_dns,
    result=[dell_attribution],
    was_informed_by=[capture_action],
)

# --- Cloudflare attribution ---
# Evidence: connections to 104.18.18.125 (WHOIS: Cloudflare, Inc.)

cf_conns = [tcp_connections[i] for i in (1, 2)]
cf_evidence_ips = [remote_ips["104.18.18.125"]]

cloudflare_attribution = graph.create(ObservableObject,
    name="Cloudflare-hosted service attribution",
    has_facet=[ArtifactClassificationResultFacet(
        classification=[ArtifactClassification(
            class_=["Cloudflare-hosted Service"],
            classification_confidence=0.7,
        )],
    )],
)

cf_analysis = graph.create(InvestigativeAction,
    name="Cloudflare traffic attribution",
    description=["IP 104.18.18.125 registered to Cloudflare, Inc. (WHOIS). "
                  "No DNS query for this IP observed in capture — "
                  "attribution based solely on IP registration."],
    start_time=datetime(2026, 3, 25, 22, 36, 0, tzinfo=timezone.utc),
    end_time=datetime(2026, 3, 25, 22, 37, 0, tzinfo=timezone.utc),
    performer=examiner,
    instrument=[analysis_tool],
    object=cf_conns + cf_evidence_ips,
    result=[cloudflare_attribution],
    was_informed_by=[capture_action],
)

# --- Microsoft attribution ---
# Evidence: connections to 20.44.10.122 and 13.73.244.6 (WHOIS: Microsoft Corporation)

msft_conns = [tcp_connections[0], tcp_connections[16]]
msft_evidence_ips = [remote_ips["20.44.10.122"], remote_ips["13.73.244.6"]]

msft_attribution = graph.create(ObservableObject,
    name="Microsoft Azure service attribution",
    has_facet=[ArtifactClassificationResultFacet(
        classification=[ArtifactClassification(
            class_=["Microsoft Azure Service"],
            classification_confidence=0.8,
        )],
    )],
)

msft_analysis = graph.create(InvestigativeAction,
    name="Microsoft traffic attribution",
    description=["IPs 20.44.10.122 and 13.73.244.6 registered to Microsoft Corporation (WHOIS). "
                  "No DNS query for these IPs observed in capture — "
                  "attribution based solely on IP registration."],
    start_time=datetime(2026, 3, 25, 22, 37, 0, tzinfo=timezone.utc),
    end_time=datetime(2026, 3, 25, 22, 38, 0, tzinfo=timezone.utc),
    performer=examiner,
    instrument=[analysis_tool],
    object=msft_conns + msft_evidence_ips,
    result=[msft_attribution],
    was_informed_by=[capture_action],
)

# --- Dropbox attribution ---
# Evidence: connections to 162.125.40.1 (WHOIS: Dropbox, Inc.)

dropbox_conns = [tcp_connections[i] for i in (11, 12, 14, 15)]
dropbox_evidence_ips = [remote_ips["162.125.40.1"]]

dropbox_attribution = graph.create(ObservableObject,
    name="Dropbox attribution",
    has_facet=[ArtifactClassificationResultFacet(
        classification=[ArtifactClassification(
            class_=["Dropbox"],
            classification_confidence=0.9,
        )],
    )],
)

dropbox_analysis = graph.create(InvestigativeAction,
    name="Dropbox traffic attribution",
    description=["IP 162.125.40.1 registered to Dropbox, Inc. (WHOIS). "
                  "High confidence — Dropbox uses dedicated IP space."],
    start_time=datetime(2026, 3, 25, 22, 38, 0, tzinfo=timezone.utc),
    end_time=datetime(2026, 3, 25, 22, 39, 0, tzinfo=timezone.utc),
    performer=examiner,
    instrument=[analysis_tool],
    object=dropbox_conns + dropbox_evidence_ips,
    result=[dropbox_attribution],
    was_informed_by=[capture_action],
)

# --- AWS Global Accelerator attribution ---
# Evidence: connections to 13.248.241.7 and 99.83.165.34 (WHOIS: Amazon)

aws_conns = [tcp_connections[i] for i in (6, 7, 8, 9, 10)]
aws_evidence_ips = [remote_ips["13.248.241.7"], remote_ips["99.83.165.34"]]

aws_attribution = graph.create(ObservableObject,
    name="AWS Global Accelerator attribution",
    has_facet=[ArtifactClassificationResultFacet(
        classification=[ArtifactClassification(
            class_=["AWS Global Accelerator Service"],
            classification_confidence=0.75,
        )],
    )],
)

aws_analysis = graph.create(InvestigativeAction,
    name="AWS traffic attribution",
    description=["IPs 13.248.241.7 and 99.83.165.34 registered to Amazon Technologies "
                  "(WHOIS). Both in AWS Global Accelerator range. No DNS query observed — "
                  "attribution based on IP registration and known AWS anycast ranges."],
    start_time=datetime(2026, 3, 25, 22, 39, 0, tzinfo=timezone.utc),
    end_time=datetime(2026, 3, 25, 22, 40, 0, tzinfo=timezone.utc),
    performer=examiner,
    instrument=[analysis_tool],
    object=aws_conns + aws_evidence_ips,
    result=[aws_attribution],
    was_informed_by=[capture_action],
)


# ═══════════════════════════════════════════════════════════
# Provenance and Investigation (created last for full linkage)
# ═══════════════════════════════════════════════════════════

all_connections = tcp_connections + [ws_discovery]
all_domains = [edge_domain, edge_cname1, edge_cname2, dell_domain, dell_cname1, dell_cname2]
all_remote_ips = list(remote_ips.values()) + [multicast_ip]
all_analysis_actions = [dell_analysis, cf_analysis, msft_analysis, dropbox_analysis, aws_analysis]
all_attributions = [dell_attribution, cloudflare_attribution, msft_attribution,
                    dropbox_attribution, aws_attribution]

provenance = graph.create(ProvenanceRecord,
    name="WiFi capture analysis provenance",
    description=["All objects produced by capture and analysis of wifi_capture.pcapng"],
    object=[
        pcap_file, wifi_interface, local_mac, gateway_mac, local_ip,
        capture_action, *all_analysis_actions,
        *all_domains, *all_remote_ips, *all_connections, *all_attributions,
    ],
)

# Investigation is the root node — created last so it can reference
# all actions, the provenance record, and key objects.
investigation = graph.create(Investigation,
    name="WiFi Packet Capture Analysis",
    description=["Analysis of WiFi interface pcapng collection captured via Wireshark"],
    focus=["Network Traffic Analysis"],
    investigation_form=["incident"],
    created_by=examiner,
    object=[
        capture_action, *all_analysis_actions,
        provenance,
        pcap_file, wifi_interface,
    ],
)

graph.write("wifi_capture.jsonld")
print(f"Graph written: {len(graph)} objects, ~{graph.estimate_triples()} triples")
