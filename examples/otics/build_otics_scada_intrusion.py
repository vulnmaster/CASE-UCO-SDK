#!/usr/bin/env python3
"""Build Tier T0 CASE/UCO graph for Operation COOLING TOWER (ICS/SCADA intrusion).

DFRWS Rodeo Team: Victims First!
All identifiers are synthetic. See operation-cooling-tower.md.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.core import Relationship
from case_uco.uco.identity import Identity, Organization
from case_uco.uco.observable import (
    ContentDataFacet,
    Device,
    DeviceFacet,
    EmbeddedDevice,
    EventRecord,
    EventRecordFacet,
    FileFacet,
    IPAddress,
    IPAddressFacet,
    NetworkAppliance,
    NetworkConnectionFacet,
    NetworkFlowFacet,
    ObservableObject,
    TCPConnection,
)
from case_uco.uco.tool import AnalyticTool, Tool
from case_uco.uco.types import Hash

OUT = Path(__file__).with_name("otics-scada-intrusion.jsonld")
KB = "http://example.org/kb/otics/"


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def build() -> CASEGraph:
    graph = CASEGraph(kb_prefix=KB)

    utility = graph.create(
        Organization,
        id=f"{KB}org-cedar-bend-water-7407c55f-a985-51b6-8843-d1640af11fe6",
        name="Cedar Bend Water Authority",
        description="Tier T0 synthetic regional drinking-water utility.",
    )
    examiner = graph.create(
        Identity,
        id=f"{KB}identity-examiner-avery-nguyen-ec80560b-8b6b-5b2a-8443-3aa01097a092",
        name="Avery Nguyen",
        description="Synthetic digital forensics examiner (Victims First! / DFRWS Rodeo).",
    )
    vendor = graph.create(
        Organization,
        id=f"{KB}org-rockwell-synthetic-7ccf76b9-e68a-5382-bd0f-2017433fc145",
        name="Rockwell Automation (synthetic reference)",
    )

    # --- Files ---
    pcap = graph.create(
        ObservableObject,
        id=f"{KB}file-ot-segment-capture-d8593526-77f5-5db9-a471-4dbed5052e3d",
        name="ot-segment-capture.pcapng",
        has_facet=[
            FileFacet(
                file_name=["ot-segment-capture.pcapng"],
                extension="pcapng",
                size_in_bytes=2_048_576,
            ),
            ContentDataFacet(
                mime_type=["application/vnd.tcpdump.pcap"],
                size_in_bytes=2_048_576,
                hash=[
                    Hash(
                        hash_method=["SHA256"],
                        hash_value="a1b2c3d4e5f60718293a4b5c6d7e8f90112233445566778899aabbccddeeff00",
                    )
                ],
            ),
        ],
    )
    plc_project = graph.create(
        ObservableObject,
        id=f"{KB}file-plc-raw-03-project-42e10997-cf74-5546-b8bd-e59e297921fb",
        name="plc-raw-03-project.acd",
        description="Synthetic ControlLogix project export recovered from ENG-WS-07.",
        has_facet=[
            FileFacet(
                file_name=["plc-raw-03-project.acd"],
                extension="acd",
                size_in_bytes=4_194_304,
            ),
            ContentDataFacet(
                mime_type=["application/octet-stream"],
                size_in_bytes=4_194_304,
                hash=[
                    Hash(
                        hash_method=["SHA256"],
                        hash_value="00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff",
                    )
                ],
            ),
        ],
    )
    historian_csv = graph.create(
        ObservableObject,
        id=f"{KB}file-historian-alarms-2cca9a90-8402-56f4-a335-aec994c9cbc8",
        name="historian-alarms-2026-03-14.csv",
        has_facet=[
            FileFacet(
                file_name=["historian-alarms-2026-03-14.csv"],
                extension="csv",
                size_in_bytes=18_432,
            ),
            ContentDataFacet(
                mime_type=["text/csv"],
                size_in_bytes=18_432,
                hash=[
                    Hash(
                        hash_method=["SHA256"],
                        hash_value="ffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100",
                    )
                ],
            ),
        ],
    )

    # --- Devices ---
    eng_ws = graph.create(
        Device,
        id=f"{KB}device-eng-ws-07-df4e0ea7-d6fb-593f-9680-e401ac940d22",
        name="ENG-WS-07",
        description="Synthetic OT engineering workstation used for PLC programming.",
        has_facet=[
            DeviceFacet(
                device_type="engineering-workstation",
                manufacturer=utility,
                model="Latitude 5540 (synthetic)",
                serial_number="CBWA-ENG-0007",
            )
        ],
    )
    hmi = graph.create(
        NetworkAppliance,
        id=f"{KB}device-hmi-clearscada-1be7df18-54a9-554a-97a9-51fdd552fc60",
        name="HMI-CLEARSCADA-01",
        description="Synthetic supervisory HMI / SCADA server on the OT VLAN.",
        has_facet=[
            DeviceFacet(
                device_type="scada-hmi-server",
                manufacturer=utility,
                model="ClearSCADA Server (synthetic)",
                serial_number="CBWA-HMI-0001",
            )
        ],
    )
    plc = graph.create(
        EmbeddedDevice,
        id=f"{KB}device-plc-raw-03-42beef9c-3e30-5b23-9618-e5d3c4b57fc0",
        name="PLC-RAW-03",
        description=(
            "Synthetic raw-water pump PLC. Typed today as EmbeddedDevice + DeviceFacet; "
            "no core facet carries rack/slot, firmware revision, or process-tag setpoints."
        ),
        has_facet=[
            DeviceFacet(
                device_type="programmable-logic-controller",
                manufacturer=vendor,
                model="ControlLogix 1756-L83E (synthetic)",
                serial_number="SN-T0-PLC-RAW-03",
            )
        ],
    )

    # --- Network ---
    ip_eng = graph.create(
        IPAddress,
        id=f"{KB}ip-10-50-10-47-3c6c7ecd-9e70-528b-8d21-1014c5e055a0",
        has_facet=[IPAddressFacet(address_value="10.50.10.47")],
    )
    ip_hmi = graph.create(
        IPAddress,
        id=f"{KB}ip-10-50-20-10-55d8707e-39ee-5f21-aa81-bf3d650778c7",
        has_facet=[IPAddressFacet(address_value="10.50.20.10")],
    )
    ip_plc = graph.create(
        IPAddress,
        id=f"{KB}ip-10-50-30-13-371f3ad8-0b40-5e21-92a0-ad1eaf78fc2f",
        has_facet=[IPAddressFacet(address_value="10.50.30.13")],
    )

    graph.create(
        Relationship,
        id=f"{KB}rel-eng-has-ip-1647dce3-4ac3-5825-9a14-110f2bb6e4f5",
        source=eng_ws,
        target=ip_eng,
        kind_of_relationship="Connected_To",
        is_directional=True,
        start_time=_dt("2026-03-14T02:10:00"),
    )
    graph.create(
        Relationship,
        id=f"{KB}rel-hmi-has-ip-8596752d-e6ad-5a43-a471-1a0fb15f34ef",
        source=hmi,
        target=ip_hmi,
        kind_of_relationship="Connected_To",
        is_directional=True,
        start_time=_dt("2026-03-14T02:10:00"),
    )
    graph.create(
        Relationship,
        id=f"{KB}rel-plc-has-ip-0e34b5ec-b66b-59d9-8f29-dacad88138f5",
        source=plc,
        target=ip_plc,
        kind_of_relationship="Connected_To",
        is_directional=True,
        start_time=_dt("2026-03-14T02:10:00"),
    )

    modbus_write = graph.create(
        TCPConnection,
        id=f"{KB}conn-modbus-write-setpoint-d2680c79-0caf-50ae-80ee-4e54ef464caf",
        name="Modbus/TCP write to PLC-RAW-03",
        description=(
            "Synthetic Modbus/TCP session carrying unauthorized holding-register writes "
            "(function code 16) that raise pump discharge pressure setpoint. Function code "
            "and register address are described in prose because UCO has no industrial "
            "protocol facet."
        ),
        has_facet=[
            NetworkConnectionFacet(
                src=ip_eng,
                dst=ip_plc,
                source_port=49_152,
                destination_port=502,
                start_time=_dt("2026-03-14T03:41:12"),
                end_time=_dt("2026-03-14T03:41:18"),
            ),
            NetworkFlowFacet(
                src_packets=14,
                dst_packets=12,
                src_bytes=896,
                dst_bytes=640,
            ),
        ],
    )
    graph.create(
        Relationship,
        id=f"{KB}rel-modbus-in-pcap-04b03d29-bab1-5788-a65b-6c821ae5f54e",
        source=modbus_write,
        target=pcap,
        kind_of_relationship="Contained_Within",
        is_directional=True,
        start_time=_dt("2026-03-14T03:41:12"),
    )

    # --- Historian / HMI events ---
    alarm_hihi = graph.create(
        EventRecord,
        id=f"{KB}event-historian-hihi-discharge-32446779-eac4-57da-9c72-688e296fc8ae",
        name="Historian HIHI alarm — PUMP3_DISCHARGE_PSI",
        description=(
            "Synthetic ClearSCADA historian row. Tag name, engineering units, and "
            "setpoint before/after cannot be typed on EventRecordFacet today."
        ),
        has_facet=[
            EventRecordFacet(
                event_id="ALM-2026-0314-8841",
                event_type="HIHI",
                event_record_service_name="ClearSCADA-Historian",
                event_record_device=plc,
                event_record_text=(
                    "PUMP3_DISCHARGE_PSI HIHI active value=118.4 psi trip=95.0 psi "
                    "(unauthorized setpoint change suspected)"
                ),
                start_time=_dt("2026-03-14T03:41:20"),
                application=hmi,
            )
        ],
    )
    graph.create(
        Relationship,
        id=f"{KB}rel-alarm-from-csv-7dbb60fc-cbb0-5839-bfae-713383c98b72",
        source=alarm_hihi,
        target=historian_csv,
        kind_of_relationship="Contained_Within",
        is_directional=True,
        start_time=_dt("2026-03-14T03:41:20"),
    )

    logic_download = graph.create(
        EventRecord,
        id=f"{KB}event-hmi-logic-download-c4a14a74-c0d2-5bd0-975f-2423bd4c6edd",
        name="HMI audit — unauthorized PLC logic download",
        has_facet=[
            EventRecordFacet(
                event_id="AUD-2026-0314-221",
                event_type="PROGRAM_DOWNLOAD",
                event_record_service_name="HMI-Audit",
                event_record_device=plc,
                event_record_text=(
                    "User ENGTEC downloaded project to PLC-RAW-03 from ENG-WS-07 "
                    "outside approved change window"
                ),
                start_time=_dt("2026-03-14T03:38:44"),
                application=hmi,
            )
        ],
    )

    # --- Tools / actions ---
    wireshark = graph.create(
        Tool,
        id=f"{KB}tool-wireshark-cb122278-bdd1-52f7-be6d-80d31751520d",
        name="Wireshark",
        version="4.4.5",
        tool_type="Network Protocol Analyzer",
    )
    ot_parser = graph.create(
        AnalyticTool,
        id=f"{KB}tool-otis-parser-275ba659-3326-5b85-b5a0-1201a8dc7efc",
        name="OTIS Packet Annotator (synthetic)",
        version="0.3.1",
        tool_type="ICS Protocol Analysis",
    )

    capture_action = graph.create(
        InvestigativeAction,
        id=f"{KB}action-ot-span-capture-79e7d0a9-0b81-5451-8b1a-fb35ca440920",
        name="Acquire OT VLAN SPAN capture",
        start_time=_dt("2026-03-14T04:05:00"),
        end_time=_dt("2026-03-14T04:35:00"),
        performer=examiner,
        instrument=wireshark,
        object=[hmi, plc, eng_ws],
        result=[pcap],
    )
    analysis_action = graph.create(
        InvestigativeAction,
        id=f"{KB}action-modbus-setpoint-analysis-20ca6894-b775-5304-88bb-a0ecde1eb521",
        name="Analyze Modbus writes and historian correlation",
        description=(
            "Correlate unauthorized Modbus holding-register writes with HIHI alarms and "
            "HMI program-download audit events."
        ),
        start_time=_dt("2026-03-14T05:10:00"),
        end_time=_dt("2026-03-14T06:00:00"),
        performer=examiner,
        instrument=ot_parser,
        object=[pcap, historian_csv, plc_project, modbus_write, alarm_hihi, logic_download],
        result=[modbus_write, alarm_hihi],
        was_informed_by=[capture_action],
    )

    provenance = graph.create(
        ProvenanceRecord,
        id=f"{KB}prov-ot-capture-673b2f4b-7ad9-5b88-84a3-9a4ec31da219",
        object=[pcap],
        description="SPAN acquisition of OT VLAN traffic for INV-2026-OT-001.",
    )

    graph.create(
        Investigation,
        id=f"{KB}investigation-cooling-tower-2c40c01b-f509-5cff-934c-46c65ece03c1",
        name="Operation COOLING TOWER — Cedar Bend Water Authority OT intrusion",
        description=(
            "Tier T0 synthetic ICS/SCADA investigation (DFRWS Rodeo / Victims First!). "
            "Models PLC, HMI, Modbus/TCP, historian alarms, and engineering workstation "
            "artifacts with core CASE/UCO types."
        ),
        object=[
            capture_action,
            analysis_action,
            provenance,
            pcap,
            plc_project,
            historian_csv,
            eng_ws,
            hmi,
            plc,
            modbus_write,
            alarm_hihi,
            logic_download,
            utility,
            vendor,
            examiner,
            wireshark,
            ot_parser,
            ip_eng,
            ip_hmi,
            ip_plc,
        ],
        created_by=examiner,
    )

    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
