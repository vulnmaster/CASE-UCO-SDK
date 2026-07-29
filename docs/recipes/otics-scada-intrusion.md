# ICS/SCADA and OT Network Intrusion Modeling

> See [Recipe Index](INDEX.md) for all recipes.

Model industrial control system (ICS) and supervisory control and data
acquisition (SCADA) intrusion investigations — PLC/HMI assets, OT VLAN packet
captures, Modbus/TCP (or similar) process writes, historian alarm exports, and
engineering-workstation project files — using core CASE/UCO types.

**Validated against** `examples/otics/otics-scada-intrusion.jsonld` (Tier T0
synthetic Operation COOLING TOWER; DFRWS Rodeo team **Victims First!**).

## When to use this recipe

- Submitted content mentions PLC, RTU, HMI, SCADA, DCS, historian, Modbus,
  DNP3, EtherNet/IP, OPC UA, setpoints, ladder logic, or OT/ICS segmentation
- `route_investigation_content` returns a weak network/intrusion match but the
  evidence is process-control oriented rather than enterprise IT
- Neighboring recipes: [network-investigation.md](network-investigation.md) for
  general PCAP workflows; [cyber-threat-intelligence.md](cyber-threat-intelligence.md)
  for ATT&CK narrative; [spear-phishing.md](spear-phishing.md) when the initial
  access vector is email

## Scope

| Layer | What it captures | Primary classes |
|---|---|---|
| **Acquisition** | OT SPAN/pcap, tool, examiner | `InvestigativeAction`, `Tool`, `FileFacet`, `ContentDataFacet`, `ProvenanceRecord` |
| **OT assets** | PLC, HMI/SCADA server, engineering workstation | `EmbeddedDevice`, `NetworkAppliance`, `Device` + `DeviceFacet` |
| **Process traffic** | Industrial protocol sessions (e.g. Modbus/TCP :502) | `TCPConnection`, `NetworkConnectionFacet`, `NetworkFlowFacet`, `IPAddress` |
| **Process events** | Historian alarms, HMI audit / logic-download rows | `EventRecord`, `EventRecordFacet` |
| **Analysis** | Correlation of writes ↔ alarms ↔ project files | Separate `InvestigativeAction` + `AnalyticTool` |
| **Case** | Investigation container | `Investigation` |

## Key classes

| Class | Role |
|---|---|
| `Investigation` | Case container (create last) |
| `InvestigativeAction` | Capture action and separate analysis action |
| `EmbeddedDevice` | PLC / RTU / dedicated controllers |
| `NetworkAppliance` | HMI / SCADA servers and similar supervisory hosts |
| `Device` + `DeviceFacet` | Engineering workstations; `deviceType` carries free-text role labels |
| `EventRecord` + `EventRecordFacet` | Historian alarms and HMI audit events |
| `TCPConnection` + network facets | Industrial protocol sessions observed in PCAP |
| `Relationship` | `Contained_Within`, `Connected_To` (directional) |
| `ProvenanceRecord` | Links acquired exhibits to the acquisition action |

## Pattern

```
Investigation
  ├── InvestigativeAction (OT SPAN capture)
  │     ├── instrument ──▶ Tool (Wireshark)
  │     ├── object ──▶ HMI / PLC / ENG-WS
  │     └── result ──▶ File (pcapng)
  ├── InvestigativeAction (Modbus ↔ historian analysis)
  │     ├── instrument ──▶ AnalyticTool
  │     ├── object ──▶ pcap, CSV, project file, connections, events
  │     └── was_informed_by ──▶ capture action
  ├── EmbeddedDevice (PLC) ──Connected_To──▶ IPAddress
  ├── NetworkAppliance (HMI) ──Connected_To──▶ IPAddress
  ├── Device (ENG-WS) ──Connected_To──▶ IPAddress
  ├── TCPConnection (Modbus/TCP) ──Contained_Within──▶ pcap
  └── EventRecord (HIHI / PROGRAM_DOWNLOAD) ──Contained_Within──▶ CSV
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import (
    EmbeddedDevice, NetworkAppliance, Device, DeviceFacet,
    TCPConnection, NetworkConnectionFacet, NetworkFlowFacet,
    EventRecord, EventRecordFacet, IPAddress, IPAddressFacet,
)
from case_uco.uco.identity import Organization

graph = CASEGraph(kb_prefix="http://example.org/kb/")
vendor = graph.create(Organization, name="PLC Vendor (synthetic)")

plc = graph.create(
    EmbeddedDevice,
    name="PLC-RAW-03",
    has_facet=[DeviceFacet(
        device_type="programmable-logic-controller",
        manufacturer=vendor,
        model="ControlLogix 1756-L83E (synthetic)",
        serial_number="SN-T0-PLC-RAW-03",
    )],
)
hmi = graph.create(
    NetworkAppliance,
    name="HMI-CLEARSCADA-01",
    has_facet=[DeviceFacet(device_type="scada-hmi-server")],
)
# Full end-to-end builder:
#   python examples/otics/build_otics_scada_intrusion.py
```

</details>

## Anti-patterns

- **Do not invent ICS ontology terms** (`otics:PLC`, `modbus:functionCode`, …) in
  graphs meant for public CASE/UCO validation. Capture vendor/protocol detail in
  `description` / `eventRecordText` until a proposal lands, or declare a local
  extension per [extensions.md](extensions.md).
- **Do not collapse acquisition and analysis** into one `InvestigativeAction`.
  Keep PCAP facts separate from setpoint-change inferences.
- **Do not type a PLC as `SmartDevice`** solely because it is networked — prefer
  `EmbeddedDevice` (purpose-built controller) or `NetworkAppliance` (supervisory
  host). Record the OT role in `DeviceFacet.deviceType`.
- **Do not put process setpoints only in free-text** without also linking the
  `EventRecord` / `TCPConnection` nodes that justify the inference.

## Ontology gaps (self-improvement input)

While this recipe validates today, core UCO lacks typed properties for:

1. PLC firmware revision, rack/slot addressing, and controller program identity
2. Industrial protocol function codes / object addresses (Modbus, DNP3, CIP, …)
3. Process tag names, engineering units, and setpoint before/after values

See the companion change proposal
`change_proposals/industrial-control-device-facet.md` and file/ upstream against
[ucoProject/UCO](https://github.com/ucoProject/UCO/issues).

## Checklist

1. Create utility `Organization` and examiner `Identity`
2. Model PLC as `EmbeddedDevice`, HMI as `NetworkAppliance`, ENG-WS as `Device`
3. Attach `DeviceFacet` with OT role in `deviceType` and serial/model when known
4. Model IPs and `Connected_To` relationships (set `is_directional=True`)
5. Model industrial sessions as `TCPConnection` with ports (e.g. 502) and flows
6. Model historian/HMI rows as `EventRecord` + `EventRecordFacet`
7. Separate capture vs analysis `InvestigativeAction`s; add `ProvenanceRecord`
8. Create `Investigation` last, linking actions and key observables
9. Validate: `case_validate --built-version case-1.4.0 --allow-info <graph.jsonld>`

## Validated exemplar

| Artifact | Path |
|---|---|
| Scenario (Tier T0) | [examples/otics/operation-cooling-tower.md](../../examples/otics/operation-cooling-tower.md) |
| Builder | [examples/otics/build_otics_scada_intrusion.py](../../examples/otics/build_otics_scada_intrusion.py) |
| Graph | [examples/otics/otics-scada-intrusion.jsonld](../../examples/otics/otics-scada-intrusion.jsonld) |

```bash
python examples/otics/build_otics_scada_intrusion.py
case_validate --built-version case-1.4.0 --allow-info examples/otics/otics-scada-intrusion.jsonld
```

## Related

- [network-investigation.md](network-investigation.md) — PCAP three-layer pattern
- [cyber-threat-intelligence.md](cyber-threat-intelligence.md) — threat narrative / ATT&CK
- [change-proposal.md](change-proposal.md) — upstreaming ICS facet gaps
- [recipe-authoring.md](recipe-authoring.md) — catalog registration rules
