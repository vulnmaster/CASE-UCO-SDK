<!-- Change Proposal: Industrial control device facet -->
<!-- Target repository: UCO -->
<!-- Target release: 1.6.0 -->
<!-- DFRWS Rodeo Team: Victims First! -->

# Target release

**Target**: CASE/UCO 1.6.0

# Background

Operational technology (OT) and industrial control system (ICS) investigations
routinely recover programmable logic controllers (PLCs), remote terminal units
(RTUs), human-machine interface (HMI) / SCADA servers, and engineering
workstations together with industrial protocol traffic (Modbus/TCP, DNP3,
EtherNet/IP/CIP, OPC UA) and historian alarm exports. Core UCO already provides
useful structural types — `uco-observable:EmbeddedDevice`,
`uco-observable:NetworkAppliance`, `uco-observable:Device`,
`uco-observable:DeviceFacet`, `uco-observable:EventRecord` /
`EventRecordFacet`, and `uco-observable:TCPConnection` — but investigators
cannot type the OT-specific fields that make these cases queryable across tools:

- controller firmware revision and vendor program / project identity
- rack, slot, or backplane addressing used to locate a CPU module
- industrial protocol function codes and object/register addresses
- process tag names, engineering units, and setpoint values before/after change

Today those facts are forced into free-text `uco-core:description` or
`eventRecordText`, which breaks cross-case SPARQL and prevents SHACL from
checking cardinality or datatype. An `IndustrialControlDeviceFacet`, composable
alongside `DeviceFacet` on `EmbeddedDevice` / `NetworkAppliance` / `Device`,
plus a small set of industrial-event properties (or a companion facet on
`EventRecord`), gives ICS DFIR tools a shared vocabulary without inventing a
parallel device hierarchy.

This proposal was developed while authoring the CASE/UCO SDK recipe
`docs/recipes/otics-scada-intrusion.md` (exemplar
`examples/otics/otics-scada-intrusion.jsonld`, Tier T0 Operation COOLING TOWER)
for DFRWS Rodeo team **Victims First!**.

# Requirements

## Requirement 1

Define a new `IndustrialControlDeviceFacet` as a subclass of `uco-core:Facet`.

Properties:

- `controllerRole` (xsd:string): OT role label (e.g., `plc`, `rtu`, `hmi`,
  `engineering-workstation`, `historian`). Prefer a future controlled vocabulary;
  string is proposed initially for breadth across vendors.
- `firmwareRevision` (xsd:string): Controller or supervisory firmware /
  OS revision as reported by the vendor tooling or device identity object.
- `programIdentity` (xsd:string): Vendor project / program identity (e.g.,
  ControlLogix project name, program checksum, or logic identity string).
- `rackNumber` (xsd:integer): Chassis / rack number when applicable.
- `slotNumber` (xsd:integer): Slot number of the CPU or communications module.
- `otNetworkZone` (xsd:string): Zone / conduit label from the site OT
  architecture (e.g., Purdue level or site VLAN name).

## Requirement 2

Define a new `IndustrialProcessEventFacet` as a subclass of `uco-core:Facet`,
intended to compose with `EventRecordFacet` on the same `EventRecord`.

Properties:

- `processTagName` (xsd:string): Historian / HMI tag or point name
  (e.g., `PUMP3_DISCHARGE_PSI`).
- `engineeringUnit` (xsd:string): Unit of measure (e.g., `psi`, `degC`).
- `processValue` (xsd:decimal): Observed process value at event time.
- `setpointValue` (xsd:decimal): Applicable setpoint when the event records a
  setpoint-related alarm or change.
- `priorSetpointValue` (xsd:decimal): Prior setpoint when a change is evidenced.
- `protocolFunctionCode` (xsd:string): Industrial protocol function / service
  identifier (e.g., Modbus `16`, CIP service code) when derived from traffic.
- `protocolObjectAddress` (xsd:string): Register, object, or point address
  (e.g., Modbus holding register `40001`).

# Risk / Benefit analysis

## Benefits

- Lets ICS DFIR and detection tools emit the same typed PLC/HMI/process fields
  instead of incompatible free-text conventions.
- Keeps using existing device subclasses (`EmbeddedDevice`, `NetworkAppliance`)
  — additive facets, no breaking hierarchy change.
- Enables SPARQL competency questions that join Modbus writes to historian
  alarms by tag / setpoint rather than brittle string matching.

## Risks

- Vendor diversity (Rockwell, Siemens, Schneider, ABB, …) may pressure the
  facet toward overly specific properties. Mitigate by keeping v1 fields
  vendor-neutral and allowing `programIdentity` / addresses as strings.
- Overlap with generic `DeviceFacet.deviceType` / `model` / `serialNumber`.
  Guidance should state that `DeviceFacet` remains the place for make/model/
  serial, while `IndustrialControlDeviceFacet` carries OT-control semantics.

# Competencies demonstrated

## Competency 1

An examiner reviews an OT VLAN PCAP and a ClearSCADA historian export from a
water utility. A Modbus/TCP write from an engineering workstation changes a pump
discharge pressure setpoint; minutes later a HIHI alarm fires on tag
`PUMP3_DISCHARGE_PSI`. The examiner needs one graph where a SPARQL query returns
the PLC firmware revision, rack/slot, the Modbus function/register, and the
alarm’s tag/setpoint values.

### Competency Question 1.1

Which PLCs have firmware revision and rack/slot populated, and what OT role do
they play?

### Competency Question 1.2

Which historian HIHI events reference process tag `PUMP3_DISCHARGE_PSI`, and what
setpoint and process values were recorded?

### Draft SPARQL

```sparql
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/>

SELECT ?plc ?fw ?rack ?slot ?tag ?setpoint ?value
WHERE {
    ?plc a uco-observable:EmbeddedDevice ;
         uco-core:hasFacet ?ics .
    ?ics a proposed:IndustrialControlDeviceFacet ;
         proposed:controllerRole "plc" ;
         proposed:firmwareRevision ?fw ;
         proposed:rackNumber ?rack ;
         proposed:slotNumber ?slot .

    ?event a uco-observable:EventRecord ;
           uco-core:hasFacet ?ef , ?pef .
    ?ef a uco-observable:EventRecordFacet ;
        uco-observable:eventRecordDevice ?plc ;
        uco-observable:eventType "HIHI" .
    ?pef a proposed:IndustrialProcessEventFacet ;
         proposed:processTagName ?tag ;
         proposed:setpointValue ?setpoint ;
         proposed:processValue ?value .
    FILTER (?tag = "PUMP3_DISCHARGE_PSI")
}
```

# Example instance data

See also `change_proposals/industrial-control-device-facet.jsonld`.

```json
{
  "@context": {
    "kb": "http://example.org/kb/",
    "proposed": "http://example.org/ontology/proposed/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:plc-1",
      "@type": "uco-observable:EmbeddedDevice",
      "uco-core:name": "PLC-RAW-03",
      "uco-core:hasFacet": [
        {
          "@id": "kb:plc-1-device-facet",
          "@type": "uco-observable:DeviceFacet",
          "uco-observable:deviceType": "programmable-logic-controller",
          "uco-observable:model": "ControlLogix 1756-L83E (synthetic)",
          "uco-observable:serialNumber": "SN-T0-PLC-RAW-03"
        },
        {
          "@id": "kb:plc-1-ics-facet",
          "@type": "proposed:IndustrialControlDeviceFacet",
          "proposed:controllerRole": "plc",
          "proposed:firmwareRevision": "32.011",
          "proposed:programIdentity": "RAW_WATER_PUMP3_v12",
          "proposed:rackNumber": 0,
          "proposed:slotNumber": 0,
          "proposed:otNetworkZone": "Purdue-L1-OT-VLAN-50"
        }
      ]
    },
    {
      "@id": "kb:event-hihi-1",
      "@type": "uco-observable:EventRecord",
      "uco-core:name": "Historian HIHI — PUMP3_DISCHARGE_PSI",
      "uco-core:hasFacet": [
        {
          "@id": "kb:event-hihi-1-core",
          "@type": "uco-observable:EventRecordFacet",
          "uco-observable:eventType": "HIHI",
          "uco-observable:eventRecordDevice": {"@id": "kb:plc-1"},
          "uco-observable:eventRecordText": "PUMP3_DISCHARGE_PSI HIHI active"
        },
        {
          "@id": "kb:event-hihi-1-process",
          "@type": "proposed:IndustrialProcessEventFacet",
          "proposed:processTagName": "PUMP3_DISCHARGE_PSI",
          "proposed:engineeringUnit": "psi",
          "proposed:processValue": 118.4,
          "proposed:setpointValue": 95.0,
          "proposed:priorSetpointValue": 72.0,
          "proposed:protocolFunctionCode": "16",
          "proposed:protocolObjectAddress": "40010"
        }
      ]
    }
  ]
}
```

# Data structures affected

| Directory | Impact |
|---|---|
| `ontology/uco/observable/` | New facet classes + datatype properties |
| CASE | None required for v1 (investigation wrapping unchanged) |

# Prior art / related work

## Specifications that ground the proposed properties

The proposed facets are deliberately thin wrappers over fields that already
exist in published OT/ICS specifications and information models. They do **not**
attempt to re-encode full protocol stacks; they capture the forensic-relevant
identity and process facts those specs already define.

| Proposed property | Real-world source | What the specification already models |
|---|---|---|
| `controllerRole` (`plc`, `rtu`, `hmi`, `historian`, …) | [NIST SP 800-82 Rev. 3](https://doi.org/10.6028/NIST.SP.800-82r3) *Guide to Operational Technology (OT) Security* (§2 topologies: SCADA, DCS, PLC, HMI, RTU) | Canonical OT asset roles investigators name in evidence |
| `otNetworkZone` | [ISA/IEC 62443](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) zones & conduits; Purdue Enterprise Reference Architecture / DOE [Purdue Model Framework](https://www.energy.gov/sites/default/files/2022-10/Infra_Topic_Paper_4-14_FINAL.pdf) | Site segmentation labels used on architecture diagrams and SPAN evidence |
| `firmwareRevision` | ODVA CIP **Identity Object** (class `0x01`) Attribute 4 *Revision* (major/minor); see [ODVA EtherNet/IP Developers Guide](https://www.odva.org/wp-content/uploads/2020/05/PUB00213R0_EtherNetIP_Developers_Guide.pdf) / CIP Networks Library Vol. 1 | Mandatory device identity revision every EtherNet/IP device exposes |
| `programIdentity` | IEC 61131-3 PLC program / project identity; vendor engineering uploads (e.g., Rockwell project / program identity recovered in PLC DFIR) | Control-logic identity recovered from engineering software or memory |
| `rackNumber` / `slotNumber` | Vendor chassis addressing (e.g., ControlLogix 1756 rack/slot used by engineering software and CIP path addressing) | Physical module location recorded in project files and online path strings |
| `protocolFunctionCode` | [MODBUS Application Protocol Specification V1.1b3](https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf) §5–6 (function codes `01`–`17`/`16` write multiple registers, etc.); analogous CIP service codes | Function/service identifier on industrial PDUs |
| `protocolObjectAddress` | Modbus V1.1b3 PDU *Starting Address* / register numbering; CIP class/instance/attribute paths | Object or register address targeted by a write/read |
| `processTagName` | OPC UA / historian point names; OPC 40001-2 *Process Values* `SignalTag`; SCADA tag databases | Named process points correlated across HMI, historian, and controller |
| `engineeringUnit` | OPC UA Part 8 *Data Access* `EUInformation` / `EngineeringUnits` ([OPC 10000-8](https://reference.opcfoundation.org/Core/Part8/v104/docs/5.6.4)); UN/CEFACT / IEC CDD units | Typed unit metadata on analog process values |
| `processValue` / `setpointValue` / `priorSetpointValue` | OPC UA for Machinery Part 2 *Process Values* ([OPC 40001-2](https://reference.opcfoundation.org/Machinery/ProcessValues/v100/docs/)) process value + setpoint variables; historian alarm payloads | Observed PV and SP before/after unauthorized changes |

### Normative / standards references

1. **NIST SP 800-82 Rev. 3** (2023), *Guide to Operational Technology (OT) Security* — https://doi.org/10.6028/NIST.SP.800-82r3 — defines PLC, RTU, HMI, SCADA/DCS roles and OT topologies that motivate `controllerRole`.
2. **ISA/IEC 62443** series — industrial automation and control systems security; **zones and conduits** motivate `otNetworkZone` as a forensic label for where an asset was observed.
3. **Purdue Enterprise Reference Architecture** / DOE *Purdue Model Framework for ICS & Cybersecurity Segmentation* (2019) — https://www.energy.gov/sites/default/files/2022-10/Infra_Topic_Paper_4-14_FINAL.pdf — widely used Level 0–5 vocabulary appearing in architecture and SPAN documentation.
4. **MODBUS Application Protocol Specification V1.1b3** — https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf — function codes and register addressing for `protocolFunctionCode` / `protocolObjectAddress`.
5. **ODVA CIP / EtherNet/IP** — Identity Object (class `0x01`) attributes Vendor ID, Device Type, Product Code, **Revision**, Serial Number, Product Name — grounds `firmwareRevision` (and complements existing `DeviceFacet` serial/model).
6. **IEC 61131-3** — PLC programming languages (ladder, ST, FBD, …); grounds treating control logic / project identity as first-class forensic content via `programIdentity`.
7. **OPC UA Part 8 (IEC 62541-8)** *Data Access* — `EngineeringUnits` / `EUInformation` for `engineeringUnit`.
8. **OPC UA for Machinery – Part 2: Process Values (OPC 40001-2)** — process value, setpoint, and `SignalTag` concepts aligning with `processTagName`, `processValue`, `setpointValue`.

### Publications showing these classes in real investigations

These peer-reviewed DFIR works recover the same artifact classes the facets are meant to hold — firmware, control logic / program identity, and process state — from live PLC memory and engineering-network traffic:

1. Ahmed, I., et al. (2022). *Memory forensic analysis of a programmable logic controller in industrial control systems.* Forensic Science International: Digital Investigation (DFRWS EU 2022). https://doi.org/10.1016/j.fsidi.2022.301339 — recovers **firmware**, **control logic**, and **physical process state** from Allen-Bradley ControlLogix memory dumps.
2. Zubair, M., et al. (2023). *Towards generic memory forensic framework for programmable logic controllers.* FSI:DI. https://doi.org/10.1016/j.fsidi.2023.301513 — generalizes PLC memory profiles; ladder/control-logic extraction as primary forensic artifact.
3. Zubair, M., et al. (2020). *Control Logic Forensics Framework using Built-in Decompiler of Engineering Software in Industrial Control Systems* (Reditus). DFRWS USA 2020. https://doi.org/10.1016/j.fsidi.2020.301013 — recovers control-logic source from **network traffic** of engineering upload/download (program identity + logic change evidence).
4. Senthivel, S., Ahmed, I., & Roussev, V. (2017). *SCADA network forensics of the PCCC protocol.* Digital Investigation / DFRWS — extracts forensic artifacts (including control-logic binaries) from Allen-Bradley PCCC traffic.

Complementary (technique vocabulary, not observable schema): **MITRE ATT&CK for ICS**.

### Relationship to existing UCO

- UCO `EmbeddedDevice` / `NetworkAppliance` / `DeviceFacet` remain the structural hosts; these facets are **additive**.
- MITRE ATT&CK for ICS remains the technique vocabulary; it does not replace typed observable properties for firmware, rack/slot, Modbus function/register, or historian tag/setpoint fields.
- CASE/UCO SDK recipe `otics-scada-intrusion` (Victims First! / DFRWS Rodeo; PR https://github.com/vulnmaster/CASE-UCO-SDK/pull/95) demonstrates the modeling gap with only core types today.

# Submitter

DFRWS Rodeo Team: **Victims First!**
