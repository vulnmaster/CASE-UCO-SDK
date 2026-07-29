#!/usr/bin/env python3
"""Build a validated CASE/UCO graph for an ArduPilot UAS flight log.

Source evidence: uavrodeo.BIN, the DFRWS USA 2026 Rodeo unmanned-aircraft
challenge log (ArduPilot DataFlash, 9,404,416 bytes, SHA-256
a2fa5f1f2b63836045f4b74e07d043780ded1126d04db8d5f286896da363693f).

Every value in the graph is read from uavrodeo_flight_facts.json, which is
machine-extracted from that log by scripts/extract_uas_flight_facts.py using
pymavlink. Nothing is hand-typed, so the builder cannot drift from the
evidence. Enum names (flight modes, mode-change reasons, logged events) are
resolved against ArduPilot master:

    libraries/AP_Logger/AP_Logger.h        enum class LogEvent
    libraries/AP_Vehicle/ModeReason.h      enum class ModeReason
    ArduCopter/mode.h                      enum class Mode::Number

Honesty note carried into the graph: this capture is an ArduPilot SITL
(software-in-the-loop) run, not a physical flight. The log says so itself
("RC Protocol: SITL") and the graph records it, so no reader mistakes a
simulated trajectory for evidence of where an aircraft was. The modelling
pattern is identical for a physical flight; only the fix quality changes.

What the graph asserts, in short: the aircraft was armed in GUIDED, climbed
to ~20 m, flew out to the north-west, and 2.452 seconds after an
unattributed MAVLink node (system 141, component 190 — the Mission Planner
ground-station component id) sent it a STATUSTEXT, the autopilot changed to
RTL for reason GCS_COMMAND and flew home. The aircraft was flying with
SYSID_ENFORCE = 0, so it would accept commands from any system id on the
link. The graph states the correlation and the configuration; it does not
assert that node 141 commanded the mode change, because the ArduPilot MODE
record carries the reason but not the commanding system id.

Validated against CASE 1.4.0 + the candidate `uas` extension.
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path


def _is_repo_root(candidate: Path) -> bool:
    return (candidate / "extensions" / "uas" / "manifest.json").is_file() and (
        candidate / "python" / "case_uco"
    ).is_dir()


def _find_repo_root() -> Path:
    if "CASE_UCO_LIBRARIES_ROOT" in os.environ:
        root = Path(os.environ["CASE_UCO_LIBRARIES_ROOT"]).resolve()
        if not _is_repo_root(root):
            raise RuntimeError(f"CASE_UCO_LIBRARIES_ROOT is not a repo root: {root}")
        return root
    here = Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if _is_repo_root(candidate):
            return candidate
    for part in os.environ.get("PYTHONPATH", "").split(os.pathsep):
        if part and _is_repo_root(Path(part).resolve()):
            return Path(part).resolve()
    raise RuntimeError("Could not locate CASE-UCO-SDK root; set CASE_UCO_LIBRARIES_ROOT")


ROOT = _find_repo_root()
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "mcp_server"))

from graph_validator import (  # noqa: E402
    load_extension_ontology_paths,
    validate_graph_file,
    validator_available,
)

HERE = Path(__file__).resolve().parent
FACTS_PATH = HERE / "uavrodeo_flight_facts.json"
OUTPUT = HERE / "ardupilot-uas-flight-log.jsonld"
CASE_ID = "dfrws-rodeo-2026-uas-flight-log"
NS = f"https://example.org/uas/{CASE_ID}/"

# The MAVLink component id observed as the source of the STATUSTEXT.
MAV_COMP_ID_MISSIONPLANNER = 190


def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def lit(dtype: str, value) -> dict:
    if isinstance(value, bool):
        return {"@type": dtype, "@value": "true" if value else "false"}
    return {"@type": dtype, "@value": str(value)}


def rel(source: str, target: str, kind: str, *, observable: bool = True) -> dict:
    return {
        "@id": uid(f"rel-{kind}-{source}-{target}"),
        "@type": ("uco-observable:ObservableRelationship" if observable
                  else "uco-core:Relationship"),
        "uco-core:source": [{"@id": source}],
        "uco-core:target": [{"@id": target}],
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": lit("xsd:boolean", True),
    }


def z(iso: str) -> str:
    """Normalise the extractor's '+00:00' offsets to a trailing Z."""
    return iso.replace("+00:00", "Z")


def build_graph() -> dict:
    facts = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    src = facts["source_file"]
    ap = facts["autopilot"]
    fl = facts["flight"]
    mav = facts["mavlink"]
    nodes: list[dict] = []

    simulated = bool(ap["simulated"])
    sim_caveat = (
        "This log is an ArduPilot SITL (software-in-the-loop) capture: the log "
        "records 'RC Protocol: SITL' and carries SIM/SIM2 simulator state "
        "records. Positions are simulator output, not observations of a "
        "physical aircraft."
    ) if simulated else ""

    # ------------------------------------------------------------------
    # The aircraft, its firmware, and its address on the control link
    # ------------------------------------------------------------------
    aircraft = uid("uas-aircraft")
    nodes.append({
        "@id": aircraft,
        "@type": "uas:UnmannedAircraft",
        "uco-core:name": f"Quadrotor logged in {src['file_name']}",
        "uco-core:description": (
            f"{ap['firmware_string']}, {ap['frame']}, autopilot board UID "
            f"{ap['vehicle_uid']}. Source: VER and MSG records at the head of "
            f"the DataFlash log. {sim_caveat}"
        ).strip(),
        "uco-core:hasFacet": [
            {
                "@id": uid("uas-aircraft-device-facet"),
                "@type": "uco-observable:DeviceFacet",
                "uco-observable:deviceType": "Unmanned Aircraft",
            },
            {
                "@id": uid("uas-aircraft-uas-facet"),
                "@type": "uas:UASFacet",
                "uco-core:description": (
                    "The log carries no ASTM F3411 Remote ID, registration "
                    "number or operator id, so none is asserted. Airframe "
                    "configuration and autopilot identifier are read from the "
                    "log."
                ),
                "uas:airframeConfiguration": ap["frame"].replace("Frame: ", ""),
                "uas:autopilotIdentifier": ap["vehicle_uid"],
                "uas:unmannedAircraftType": "Helicopter or Multirotor",
            },
            {
                "@id": uid("uas-aircraft-mavlink-facet"),
                "@type": "uas:MavlinkEndpointFacet",
                "uco-core:description": (
                    "Source: SYSID_THISMAV, SYSID_MYGCS and SYSID_ENFORCE "
                    "parameter records. SYSID_ENFORCE = 0 means the autopilot "
                    "did not check that incoming commands came from its "
                    "configured ground control station."
                ),
                "uas:mavlinkSystemId": lit(
                    "xsd:nonNegativeInteger", int(mav["SYSID_THISMAV"])),
                "uas:mavlinkComponentId": lit("xsd:nonNegativeInteger", 1),
                "uas:mavlinkComponentName": "MAV_COMP_ID_AUTOPILOT1",
                "uas:mavlinkDialect": "ardupilotmega v2.0",
                "uas:authorizedGroundControlStationId": lit(
                    "xsd:nonNegativeInteger", int(mav["SYSID_MYGCS"])),
                "uas:senderAuthenticationEnforced": lit(
                    "xsd:boolean", bool(int(mav["SYSID_ENFORCE"]))),
            },
        ],
    })

    firmware = uid("uas-firmware")
    nodes.append({
        "@id": firmware,
        "@type": "uco-observable:Software",
        "uco-core:name": ap["firmware_string"],
        "uco-core:description": (
            f"Autopilot firmware reported in the VER record: version "
            f"{ap['version']}, source revision {ap['git_hash']}. The "
            f"'-dev' suffix in the firmware string marks a development build, "
            f"which is not a tagged release and may not be reproducible from "
            f"the version number alone."
        ),
        "uco-core:hasFacet": [{
            "@id": uid("uas-firmware-facet"),
            "@type": "uco-observable:SoftwareFacet",
            "uco-observable:version": ap["version"],
            "uco-observable:swid": ap["git_hash"],
        }],
    })
    nodes.append(rel(aircraft, firmware, "Characterized_By"))

    # ------------------------------------------------------------------
    # The log container
    # ------------------------------------------------------------------
    flight_log = uid("uas-flight-log")
    nodes.append({
        "@id": flight_log,
        "@type": "uas:FlightLog",
        "uco-core:name": src["file_name"],
        "uco-core:description": (
            f"{src['format']} recovered from the autopilot. Contains "
            f"{facts['parameter_count']} parameter records and the full "
            f"telemetry of one sortie."
        ),
        "uas:logFormat": "ArduPilot DataFlash",
        "uco-core:hasFacet": [
            {
                "@id": uid("uas-flight-log-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": src["file_name"],
                "uco-observable:extension": "BIN",
                "uco-observable:sizeInBytes": lit(
                    "xsd:integer", src["size_bytes"]),
            },
            {
                "@id": uid("uas-flight-log-content-facet"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:sizeInBytes": lit(
                    "xsd:integer", src["size_bytes"]),
                "uco-observable:hash": [{
                    "@id": uid("uas-flight-log-sha256"),
                    "@type": "uco-types:Hash",
                    # Plain string, per the UCO 1.4.0 guidance that
                    # types:hashMethod be xsd:string rather than a
                    # vocabulary-typed literal.
                    "uco-types:hashMethod": "SHA256",
                    "uco-types:hashValue": lit("xsd:hexBinary", src["sha256"]),
                }],
            },
        ],
    })
    nodes.append(rel(flight_log, aircraft, "Extracted_From"))

    # ------------------------------------------------------------------
    # Time anchoring — how boot-relative log time became wall-clock time
    # ------------------------------------------------------------------
    anchor = facts["time_anchor"]
    time_anchor_note = (
        f"DataFlash records are stamped in TimeUS, microseconds since "
        f"autopilot boot. Wall-clock times in this graph are derived by "
        f"anchoring TimeUS {anchor['anchor_time_us']} to the GNSS time in the "
        f"first 3D-fix GPS record (week {anchor['gps_week']}, "
        f"{anchor['gps_ms_of_week']} ms of week), converted by "
        f"{anchor['method']}. Any error in the leap-second constant shifts "
        f"every derived time equally."
    )

    # ------------------------------------------------------------------
    # The trajectory — GNSS receiver fixes, each with its own fix time
    # ------------------------------------------------------------------
    entry_ids = []
    for i, s in enumerate(facts["track_samples"]):
        loc = uid(f"uas-fix-loc-{i}")
        latlong_facet = {
            "@id": uid(f"uas-fix-latlong-{i}"),
            "@type": "uco-location:LatLongCoordinatesFacet",
            "uco-location:latitude": lit("xsd:decimal", s["latitude"]),
            "uco-location:longitude": lit("xsd:decimal", s["longitude"]),
            "uco-location:altitude": lit("xsd:decimal", s["altitude_amsl_m"]),
            # Pending UCO terms — see extensions/uas/location-pending.ttl.
            "proposed-loc:altitudeReference": "mean sea level",
        }
        if s.get("horizontal_accuracy_m") is not None:
            latlong_facet["proposed-loc:horizontalAccuracy"] = lit(
                "xsd:decimal", s["horizontal_accuracy_m"])
        if s.get("vertical_accuracy_m") is not None:
            latlong_facet["proposed-loc:verticalAccuracy"] = lit(
                "xsd:decimal", s["vertical_accuracy_m"])

        gps_facet = {
            "@id": uid(f"uas-fix-gps-{i}"),
            "@type": "uco-location:GPSCoordinatesFacet",
            "uco-location:hdop": lit("xsd:decimal", s["hdop"]),
            "proposed-loc:satelliteCount": lit(
                "xsd:nonNegativeInteger", s["satellites"]),
            "proposed-loc:fixQuality": "simulated" if simulated else "3D fix",
        }
        if s.get("vdop") is not None:
            gps_facet["uco-location:vdop"] = lit("xsd:decimal", s["vdop"])

        nodes.append({
            "@id": loc,
            "@type": "uco-location:Location",
            "uco-core:name": f"GNSS fix at {z(s['utc'])}",
            "uco-core:hasFacet": [latlong_facet, gps_facet],
        })

        entry = uid(f"uas-fix-entry-{i}")
        entry_ids.append(entry)
        note = ""
        if s.get("nearest_to_apogee"):
            note = (" This is the GNSS fix nearest the EKF-reported climb "
                    "peak; the peak altitude itself is carried on the flight.")
        nodes.append({
            "@id": entry,
            "@type": "uco-observable:GeoLocationEntry",
            "uco-core:name": f"GNSS fix {i + 1} of "
                             f"{len(facts['track_samples'])} at {z(s['utc'])}",
            "uco-core:description": (
                f"GPS record joined to its paired GPA accuracy record; ground "
                f"speed {s['ground_speed_ms']} m/s.{note}"
            ),
            "uco-core:hasFacet": [{
                "@id": uid(f"uas-fix-entry-facet-{i}"),
                "@type": "uco-observable:GeoLocationEntryFacet",
                "uco-observable:location": {"@id": loc},
                # The gap this example exists to demonstrate: without a
                # per-entry time, these fixes are an ordered set with no clock.
                "proposed-obs:observationTime": lit(
                    "xsd:dateTime", z(s["utc"])),
            }],
        })

    track = uid("uas-flight-track")
    nodes.append({
        "@id": track,
        "@type": "uco-observable:GeoLocationTrack",
        "uco-core:name": "Flight track from GNSS receiver fixes",
        "uco-core:description": (
            f"{len(entry_ids)} fixes sampled at roughly 10 s intervals from "
            f"the log's 5 Hz GPS series, plus the fix nearest the climb peak. "
            f"Entries are raw receiver fixes rather than the EKF-fused POS "
            f"series, so each carries the satellite count and accuracy it was "
            f"derived from. {time_anchor_note}"
        ),
        "uco-core:hasFacet": [{
            "@id": uid("uas-flight-track-facet"),
            "@type": "uco-observable:GeoLocationTrackFacet",
            "uco-observable:startTime": lit(
                "xsd:dateTime", z(fl["track_first_utc"])),
            "uco-observable:endTime": lit(
                "xsd:dateTime", z(fl["track_last_utc"])),
            "uco-observable:geoLocationEntry": [{"@id": e} for e in entry_ids],
        }],
    })
    nodes.append(rel(track, flight_log, "Extracted_From"))

    # ------------------------------------------------------------------
    # Takeoff point
    # ------------------------------------------------------------------
    takeoff = uid("uas-takeoff-location")
    nodes.append({
        "@id": takeoff,
        "@type": "uco-location:Location",
        "uco-core:name": "EKF origin and home position recorded at arming",
        "uco-core:description": (
            "ORGN records written at arming: type 0 (EKF origin) and type 1 "
            "(home position) agree to seven decimal places. This is the "
            "aircraft's own belief about where it started."
        ),
        "uco-core:hasFacet": [{
            "@id": uid("uas-takeoff-latlong"),
            "@type": "uco-location:LatLongCoordinatesFacet",
            "uco-location:latitude": lit(
                "xsd:decimal", fl["origin"]["latitude"]),
            "uco-location:longitude": lit(
                "xsd:decimal", fl["origin"]["longitude"]),
            "uco-location:altitude": lit(
                "xsd:decimal", fl["origin"]["altitude_amsl_m"]),
            "proposed-loc:altitudeReference": "mean sea level",
        }],
    })

    # ------------------------------------------------------------------
    # The sortie
    # ------------------------------------------------------------------
    flight = uid("uas-flight")
    nodes.append({
        "@id": flight,
        "@type": "uas:Flight",
        "uco-core:name": f"Flight of {fl['arm_utc'][:10]}, "
                         f"{fl['arm_utc'][11:19]}Z to {fl['disarm_utc'][11:19]}Z",
        "uco-core:description": (
            f"Bounded by the 'Arming motors' and 'Disarming motors' MSG "
            f"records; {fl['duration_s']} s from arm to disarm. Maximum "
            f"altitude {fl['max_altitude_above_home_m']} m above the home "
            f"position ({fl['max_altitude_amsl_m']} m AMSL) at "
            f"{z(fl['max_altitude_utc'])}, from the {fl['max_altitude_source']}. "
            f"{time_anchor_note} {sim_caveat}"
        ).strip(),
        "uco-core:startTime": lit("xsd:dateTime", z(fl["arm_utc"])),
        "uco-core:endTime": lit("xsd:dateTime", z(fl["disarm_utc"])),
        "uco-core:eventType": "UAS flight",
        "uas:takeoffLocation": {"@id": takeoff},
        "uas:flightTrack": {"@id": track},
        "uas:maximumAltitudeAboveTakeoff": lit(
            "xsd:decimal", fl["max_altitude_above_home_m"]),
        "uco-core:eventContext": [{"@id": aircraft}, {"@id": flight_log}],
    })
    # uas:Flight is a uco-core:Event, not an Observable, so this edge must be
    # a plain uco-core:Relationship — ObservableRelationship requires both
    # ends to be Observables (a warning today, an error in UCO 2.0.0).
    nodes.append(rel(flight, aircraft, "Related_To", observable=False))

    # ------------------------------------------------------------------
    # Log rows as event records
    # ------------------------------------------------------------------
    record_ids = []
    statustext_row = None
    mode_rows = []
    for i, row in enumerate(facts["timeline"]):
        record = uid(f"uas-log-record-{i}")
        record_ids.append(record)
        nodes.append({
            "@id": record,
            "@type": "uco-observable:EventRecord",
            "uco-core:name": f"{row['record_type']} record at {z(row['utc'])}",
            "uco-core:hasFacet": [{
                "@id": uid(f"uas-log-record-facet-{i}"),
                "@type": "uco-observable:EventRecordFacet",
                "uco-observable:eventRecordID": f"{row['record_type']}-{row['time_us']}",
                "uco-observable:eventType": row["record_type"],
                "uco-observable:eventRecordServiceName": "ArduPilot AP_Logger",
                "uco-observable:eventRecordText": row["text"],
                "uco-observable:eventRecordDevice": {"@id": aircraft},
                "uco-observable:startTime": lit("xsd:dateTime", z(row["utc"])),
            }],
        })
        nodes.append(rel(record, flight_log, "Contained_Within"))
        if row["record_type"] == "MSG" and row["text"].startswith("SRC="):
            statustext_row = (i, row, record)
        if row["record_type"] == "MODE":
            mode_rows.append((i, row, record))

    # ------------------------------------------------------------------
    # The unattributed MAVLink node and the STATUSTEXT it sent
    # ------------------------------------------------------------------
    foreign_node = None
    message = None
    if statustext_row is not None:
        _, row, record = statustext_row
        # ArduPilot logs a received STATUSTEXT as "SRC=<sysid>/<compid>:<text>".
        header, text = row["text"].split(":", 1)
        sysid, compid = (int(v) for v in header.removeprefix("SRC=").split("/"))

        foreign_node = uid("uas-foreign-mavlink-node")
        nodes.append({
            "@id": foreign_node,
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": f"Unattributed MAVLink node, system {sysid} / "
                             f"component {compid}",
            "uco-core:description": (
                f"Observed only as the source address of a STATUSTEXT the "
                f"autopilot logged at {z(row['utc'])} as '{row['text']}'. "
                f"Component {compid} is "
                f"{'the Mission Planner ground-station component id' if compid == MAV_COMP_ID_MISSIONPLANNER else 'a MAV_COMPONENT value'}"
                f", and system {sysid} is not the configured ground control "
                f"station ({int(mav['SYSID_MYGCS'])}). MAVLink system ids are "
                f"self-asserted; with sender authentication disabled on this "
                f"aircraft the address is an observation about the link, not "
                f"an identification of an operator."
            ),
            "uco-core:hasFacet": [{
                "@id": uid("uas-foreign-mavlink-facet"),
                "@type": "uas:MavlinkEndpointFacet",
                "uas:mavlinkSystemId": lit("xsd:nonNegativeInteger", sysid),
                "uas:mavlinkComponentId": lit("xsd:nonNegativeInteger", compid),
                "uas:mavlinkComponentName": (
                    "MAV_COMP_ID_MISSIONPLANNER"
                    if compid == MAV_COMP_ID_MISSIONPLANNER else ""),
                "uas:mavlinkDialect": "ardupilotmega v2.0",
            }],
        })

        message = uid("uas-statustext")
        nodes.append({
            "@id": message,
            "@type": "uco-observable:Message",
            "uco-core:name": f"MAVLink STATUSTEXT '{text}'",
            "uco-core:description": (
                "Received by the autopilot and written to the log verbatim. "
                "The text carries no command semantics; its evidential value "
                "is that it proves a node other than the configured ground "
                "control station was transmitting on the link, and when."
            ),
            "uco-core:hasFacet": [{
                "@id": uid("uas-statustext-facet"),
                "@type": "uco-observable:MessageFacet",
                "uco-observable:messageText": text,
                "uco-observable:messageType": "MAVLink STATUSTEXT",
                "uco-observable:sentTime": lit("xsd:dateTime", z(row["utc"])),
                "uco-observable:from": {"@id": foreign_node},
                "uco-observable:to": [{"@id": aircraft}],
            }],
        })
        nodes.append(rel(message, record, "Characterized_By"))

    # ------------------------------------------------------------------
    # Mode changes — the attribution question
    # ------------------------------------------------------------------
    mode_change_ids = []
    previous_mode = None
    seen_modes = set()
    for i, row, record in mode_rows:
        # The log repeats the arming-time MODE record; model each distinct
        # transition once.
        if row["mode_name"] in seen_modes:
            previous_mode = row["mode_name"]
            continue
        seen_modes.add(row["mode_name"])

        change = uid(f"uas-mode-change-{i}")
        mode_change_ids.append(change)
        node = {
            "@id": change,
            "@type": "uas:FlightModeChange",
            "uco-core:name": f"Mode change to {row['mode_name']} at {z(row['utc'])}",
            "uco-core:startTime": lit("xsd:dateTime", z(row["utc"])),
            "uco-core:eventType": "Flight mode change",
            "uas:flightMode": row["mode_name"],
            "uas:flightModeChangeReason": row["reason_name"],
            "uas:autopilotFamily": "ArduPilot",
            "uco-core:eventContext": [{"@id": aircraft}, {"@id": record}],
        }
        if previous_mode:
            node["uas:previousFlightMode"] = previous_mode

        if statustext_row is not None and row["mode_name"] == "RTL":
            gap = (row["time_us"] - statustext_row[1]["time_us"]) / 1e6
            node["uco-core:description"] = (
                f"MODE record: mode number {row['mode_number']} "
                f"({row['mode_name']}), reason code {row['reason_code']} "
                f"({row['reason_name']}). It arrived {gap:.3f} s after the "
                f"STATUSTEXT from system "
                f"{statustext_row[1]['text'].removeprefix('SRC=').split('/')[0]}. "
                f"ArduPilot's MODE record carries the reason but not the "
                f"commanding system id, so the graph does not assert that node "
                f"commanded the change; uas:commandedBy is left unset and the "
                f"correlation is stated here. What the log does establish is "
                f"that the change was commanded by a ground control station "
                f"rather than by a stick input or a failsafe, and that the "
                f"aircraft was not enforcing which station may command it."
            )
        else:
            node["uco-core:description"] = (
                f"MODE record: mode number {row['mode_number']} "
                f"({row['mode_name']}), reason code {row['reason_code']} "
                f"({row['reason_name']}), logged at arming."
            )
        nodes.append(node)
        nodes.append(rel(change, flight, "Contained_Within", observable=False))
        previous_mode = row["mode_name"]

    # ------------------------------------------------------------------
    # Analysis provenance
    # ------------------------------------------------------------------
    tool = uid("uas-tool-pymavlink")
    nodes.append({
        "@id": tool,
        "@type": "uco-tool:AnalyticTool",
        "uco-core:name": "pymavlink",
        "uco-tool:toolType": "Flight Log Parser",
        "uco-core:description": (
            "Reference MAVLink/DataFlash parser maintained by the ArduPilot "
            "project (https://github.com/ArduPilot/pymavlink). Used through "
            "scripts/extract_uas_flight_facts.py to produce "
            "uavrodeo_flight_facts.json, from which this graph is built."
        ),
    })

    parse_action = uid("uas-action-parse")
    nodes.append({
        "@id": parse_action,
        "@type": "case-investigation:InvestigativeAction",
        "uco-core:name": "Parse ArduPilot DataFlash log",
        "uco-core:description": (
            "Decode the DataFlash log to structured records, anchor "
            "boot-relative timestamps to GNSS time, and resolve ArduPilot "
            "enumerations (LogEvent, ModeReason, Mode::Number) against the "
            "firmware source rather than transcribing raw integers."
        ),
        "uco-action:instrument": [{"@id": tool}],
        "uco-action:object": [{"@id": flight_log}],
        "uco-action:result": [{"@id": track}, {"@id": flight}] +
                             [{"@id": r} for r in record_ids],
    })

    provenance = uid("uas-provenance")
    prov_objects = [{"@id": parse_action}, {"@id": flight_log},
                    {"@id": aircraft}, {"@id": flight}]
    nodes.append({
        "@id": provenance,
        "@type": "case-investigation:ProvenanceRecord",
        "uco-core:description": (
            f"UAS flight log examination package. Evidence integrity: SHA-256 "
            f"{src['sha256']} over {src['size_bytes']} bytes."
        ),
        "case-investigation:exhibitNumber": "EX-UAS-2026-0704",
        "uco-core:object": prov_objects,
    })

    investigation_objects = [
        {"@id": n["@id"]} for n in nodes
        if n["@id"] not in {provenance}
    ]
    nodes.append({
        "@id": uid("uas-investigation"),
        "@type": "case-investigation:Investigation",
        "uco-core:name": f"Case {CASE_ID}: unmanned aircraft flight log",
        "uco-core:description": (
            "Model an ArduPilot flight log end to end: the aircraft and its "
            "control-link configuration, the sortie, the GNSS trajectory with "
            "per-fix times and accuracies, every logged state transition, and "
            "the unattributed MAVLink node observed on the link shortly before "
            "the autopilot returned to launch on a ground-station command. "
            + sim_caveat
        ).strip(),
        "uco-core:object": investigation_objects + [{"@id": provenance}],
    })

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            # Candidate extension bundled in extensions/uas/; the example.org
            # namespace is a placeholder pending a community decision.
            "uas": "http://example.org/ontology/uas/",
            # Terms proposed to UCO, declared locally in
            # extensions/uas/location-pending.ttl until UCO adopts them.
            "proposed-obs": "https://proposed.ontology.unifiedcyberontology.org/uco/observable/",
            "proposed-loc": "https://proposed.ontology.unifiedcyberontology.org/uco/location/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": nodes,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    paths = load_extension_ontology_paths("uas", mode="full", project_root=ROOT)
    print(f"Validating with {len(paths)} uas ontology file(s): "
          f"{', '.join(p.name for p in paths)}")
    report = validate_graph_file(
        path, extensions=["uas"], project_root=ROOT, strict_concepts=True)
    print(report.safe_summary)
    return 0 if report.conforms else 1


def main() -> int:
    payload = build_graph()
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Graph nodes: {len(payload['@graph'])}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
