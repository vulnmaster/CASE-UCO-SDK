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

- UCO `EmbeddedDevice` / `NetworkAppliance` / `DeviceFacet` (structural hosts)
- MITRE ATT&CK for ICS (technique vocabulary; complementary, not a substitute for
  observable facets)
- CASE/UCO SDK recipe `otics-scada-intrusion` (Victims First! / DFRWS Rodeo)

# Submitter

DFRWS Rodeo Team: **Victims First!**
