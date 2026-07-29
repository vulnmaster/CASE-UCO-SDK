# Operation COOLING TOWER (Tier T0 synthetic)

**Case ID:** INV-2026-OT-001  
**Classification:** Tier T0 synthetic data for CASE/UCO SDK recipe development  
**DFRWS Rodeo Team:** Victims First!

This scenario is **fabricated**. Every person, IP address, serial number, docket
reference, and hash is invented for modeling exercises. It is not derived from
operational case material.

## Narrative

A regional drinking-water utility ("Cedar Bend Water Authority") reports anomalous
pump-setpoint changes on a ClearSCADA HMI during a weekend maintenance window.
ICS network packet captures, a PLC project export, and historian alarm CSV exports
are provided to digital investigators.

Suspected kill chain (synthetic):

1. Engineering workstation (`ENG-WS-07`) opens a phishing attachment.
2. Attacker establishes RDP to the OT jump host, then to the HMI server.
3. Modbus/TCP writes change a pump discharge pressure setpoint on PLC `PLC-RAW-03`.
4. Historian records out-of-band `HIHI` alarms and an unauthorized logic download.

## Source artifacts (synthetic filenames)

| Artifact | Description |
|---|---|
| `ot-segment-capture.pcapng` | SPAN capture on the OT VLAN (Modbus/TCP + engineering traffic) |
| `plc-raw-03-project.acd` | Rockwell ControlLogix project export recovered from ENG-WS-07 |
| `historian-alarms-2026-03-14.csv` | ClearSCADA/historian alarm export |
| `hmi-audit.log` | HMI operator/audit log excerpt |

## Key observables to model

- Water utility as `Organization`
- HMI server as `NetworkAppliance` + `DeviceFacet`
- PLC as `EmbeddedDevice` + `DeviceFacet` (typed via free-text `deviceType` today)
- Engineering workstation as `Device` + `DeviceFacet`
- Modbus/TCP flows as `TCPConnection` + `NetworkConnectionFacet` / `NetworkFlowFacet`
- Historian alarm rows as `EventRecord` + `EventRecordFacet`
- Project / capture / CSV files as `ObservableObject` + `FileFacet` + `ContentDataFacet`
- Acquisition and analysis as separate `InvestigativeAction` nodes with `ProvenanceRecord`

## Ontology gaps observed while modeling

Core CASE/UCO has `EmbeddedDevice` / `NetworkAppliance` but **no typed properties** for:

- PLC vendor program identity / firmware revision / rack-slot addressing
- Industrial protocol function codes (e.g., Modbus write-register)
- Process setpoints, tag names, or engineering units
- Safety-instrumented vs. basic process control role

These gaps motivate the companion UCO change proposal for an
`IndustrialControlDeviceFacet` (and related protocol/event properties).
