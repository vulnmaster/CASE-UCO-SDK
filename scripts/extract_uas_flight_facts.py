"""Extract grounded facts from the DFRWS Rodeo ArduPilot DataFlash log.

Writes a support-file JSON consumed by the CASE/UCO exemplar builder, so no
value in the graph is hand-typed. Every field traces to a log message type.
"""
import datetime
import hashlib
import json
import pathlib
import sys

from pymavlink import mavutil

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

GPS_EPOCH = datetime.datetime(1980, 1, 6, tzinfo=datetime.timezone.utc)
LEAP_SECONDS = 18  # GPS-UTC offset in force since 2017-01-01

# libraries/AP_Logger/AP_Logger.h :: enum class LogEvent
LOG_EVENT = {11: "DISARMED", 15: "AUTO_ARMED", 17: "LAND_COMPLETE_MAYBE",
             18: "LAND_COMPLETE", 28: "NOT_LANDED",
             56: "MOTORS_INTERLOCK_DISABLED", 57: "MOTORS_INTERLOCK_ENABLED",
             62: "EKF_YAW_RESET"}
# libraries/AP_Vehicle/ModeReason.h :: enum class ModeReason
MODE_REASON = {0: "UNKNOWN", 1: "RC_COMMAND", 2: "GCS_COMMAND",
               3: "RADIO_FAILSAFE", 4: "BATTERY_FAILSAFE", 5: "GCS_FAILSAFE"}
# ArduCopter flight mode numbers (ArduCopter/mode.h :: enum class Mode::Number)
COPTER_MODE = {0: "STABILIZE", 1: "ACRO", 2: "ALT_HOLD", 3: "AUTO", 4: "GUIDED",
               5: "LOITER", 6: "RTL", 7: "CIRCLE", 9: "LAND", 16: "POSHOLD"}


def gps_to_utc(week, ms):
    return (GPS_EPOCH + datetime.timedelta(weeks=week, milliseconds=ms)
            - datetime.timedelta(seconds=LEAP_SECONDS))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


conn = mavutil.mavlink_connection(str(SRC))
msgs, params, anchors = {}, {}, []
for name in ("MSG", "MODE", "EV", "POS", "GPS", "GPA", "ORGN", "VER"):
    msgs[name] = []
while True:
    m = conn.recv_match(blocking=False)
    if m is None:
        break
    t = m.get_type()
    if t == "BAD_DATA":
        continue
    d = m.to_dict()
    if t == "PARM":
        params[d["Name"]] = d["Value"]
    if t == "GPS" and d.get("Status", 0) >= 3:
        anchors.append((d["TimeUS"], gps_to_utc(d["GWk"], d["GMS"])))
    if t in msgs:
        msgs[t].append(d)

a_us, a_utc = anchors[0]


def utc(us):
    return (a_utc + datetime.timedelta(microseconds=us - a_us)).isoformat(
        timespec="milliseconds")


ver = msgs["VER"][0]
first_gps = [g for g in msgs["GPS"] if g.get("Status", 0) >= 3][0]

# --- timeline -------------------------------------------------------------
timeline = []
for d in msgs["MSG"]:
    timeline.append({"time_us": d["TimeUS"], "utc": utc(d["TimeUS"]),
                     "record_type": "MSG", "text": d["Message"]})
for d in msgs["MODE"]:
    timeline.append({"time_us": d["TimeUS"], "utc": utc(d["TimeUS"]),
                     "record_type": "MODE", "mode_number": d["ModeNum"],
                     "mode_name": COPTER_MODE.get(d["ModeNum"], f"MODE_{d['ModeNum']}"),
                     "reason_code": d["Rsn"],
                     "reason_name": MODE_REASON.get(d["Rsn"], f"REASON_{d['Rsn']}"),
                     "text": (f"Flight mode -> {COPTER_MODE.get(d['ModeNum'])} "
                              f"(reason {MODE_REASON.get(d['Rsn'])})")})
for d in msgs["EV"]:
    timeline.append({"time_us": d["TimeUS"], "utc": utc(d["TimeUS"]),
                     "record_type": "EV", "event_id": d["Id"],
                     "event_name": LOG_EVENT.get(d["Id"], f"EVENT_{d['Id']}"),
                     "text": LOG_EVENT.get(d["Id"], f"EVENT_{d['Id']}")})
timeline.sort(key=lambda r: (r["time_us"], r["record_type"]))

# --- flight envelope ------------------------------------------------------
pos = msgs["POS"]
peak = max(pos, key=lambda d: d["Alt"])
origin = [d for d in msgs["ORGN"] if d["Type"] == 0][0]
home = [d for d in msgs["ORGN"] if d["Type"] == 1][0]
arm = [r for r in timeline if r.get("text") == "Arming motors"][0]
disarm = [r for r in timeline if r.get("text") == "Disarming motors"][0]

# Track entries are raw GNSS receiver fixes (GPS records), joined to the
# paired GPA record that carries the receiver's own accuracy estimates, so
# every entry can state its satellite count and metric accuracy. Downsample
# to one fix every ~10 s.
gpa_by_us = {d["TimeUS"]: d for d in msgs["GPA"]}
fixes = [d for d in msgs["GPS"] if d.get("Status", 0) >= 3]
step_us = 10_000_000
track, next_us = [], fixes[0]["TimeUS"]
for d in fixes:
    if d["TimeUS"] >= next_us:
        track.append(d)
        next_us = d["TimeUS"] + step_us
# GNSS fix nearest in time to the EKF-reported apogee, so the track carries
# the climb peak without silently relabelling an EKF value as a receiver fix.
track.append(min(fixes, key=lambda d: abs(d["TimeUS"] - peak["TimeUS"])))
track = sorted({d["TimeUS"]: d for d in track}.values(), key=lambda d: d["TimeUS"])
apogee_fix_us = min(fixes, key=lambda d: abs(d["TimeUS"] - peak["TimeUS"]))["TimeUS"]
track_samples = []
for d in track:
    gpa = gpa_by_us.get(d["TimeUS"], {})
    track_samples.append({
        "utc": utc(d["TimeUS"]), "time_us": d["TimeUS"],
        "latitude": d["Lat"], "longitude": d["Lng"],
        "altitude_amsl_m": round(d["Alt"], 3),
        "satellites": d["NSats"], "hdop": d["HDop"],
        "vdop": gpa.get("VDop"),
        "horizontal_accuracy_m": gpa.get("HAcc"),
        "vertical_accuracy_m": gpa.get("VAcc"),
        "fix_status": d["Status"],
        "ground_speed_ms": d.get("Spd"),
        "nearest_to_apogee": d["TimeUS"] == apogee_fix_us,
    })

facts = {
    "_note": ("Machine-extracted from the DFRWS USA 2026 Rodeo UAS log with "
              "pymavlink. Enum names resolved against ArduPilot master: "
              "AP_Logger.h (LogEvent), ModeReason.h (ModeReason), "
              "ArduCopter/mode.h (Mode::Number). No value is hand-entered."),
    "source_file": {
        "file_name": SRC.name,
        "size_bytes": SRC.stat().st_size,
        "sha256": sha256(SRC),
        "format": "ArduPilot DataFlash binary log (.BIN)",
    },
    "autopilot": {
        "firmware_string": ver["FWS"],
        "version": f"{ver['Maj']}.{ver['Min']}.{ver['Pat']}",
        "git_hash": f"{ver['GH']:08x}",
        "board_type": ver["BT"],
        "frame": [r["text"] for r in timeline if r["text"].startswith("Frame:")][0],
        "vehicle_uid": [r["text"] for r in timeline
                        if len(r["text"]) == 32 and all(c in "0123456789abcdef" for c in r["text"])][0],
        "simulated": any(r["text"] == "RC Protocol: SITL" for r in timeline),
    },
    "time_anchor": {
        "method": "GPS week/ms-of-week to UTC, minus 18 leap seconds",
        "gps_week": first_gps["GWk"],
        "gps_ms_of_week": first_gps["GMS"],
        "anchor_time_us": a_us,
        "anchor_utc": a_utc.isoformat(timespec="milliseconds"),
    },
    "flight": {
        "arm_utc": arm["utc"],
        "disarm_utc": disarm["utc"],
        "duration_s": round((disarm["time_us"] - arm["time_us"]) / 1e6, 3),
        "origin": {"latitude": origin["Lat"], "longitude": origin["Lng"],
                   "altitude_amsl_m": origin["Alt"]},
        "home": {"latitude": home["Lat"], "longitude": home["Lng"],
                 "altitude_amsl_m": home["Alt"]},
        "max_altitude_above_home_m": round(peak["RelHomeAlt"], 3),
        "max_altitude_amsl_m": round(peak["Alt"], 3),
        "max_altitude_utc": utc(peak["TimeUS"]),
        "max_altitude_source": ("POS record (EKF-fused position); RelHomeAlt is "
                                "relative to the home position captured at arming"),
        "gnss_satellites": first_gps["NSats"],
        "gnss_hdop": first_gps["HDop"],
        "gnss_fix_status": first_gps["Status"],
        "track_first_utc": None,
        "track_last_utc": None,
    },
    "mavlink": {
        "SYSID_THISMAV": params.get("SYSID_THISMAV"),
        "SYSID_MYGCS": params.get("SYSID_MYGCS"),
        "SYSID_ENFORCE": params.get("SYSID_ENFORCE"),
    },
    "timeline": timeline,
    "track_samples": track_samples,
    "parameter_count": len(params),
}

facts["flight"]["track_first_utc"] = track_samples[0]["utc"]
facts["flight"]["track_last_utc"] = track_samples[-1]["utc"]

OUT.write_text(json.dumps(facts, indent=2), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
print("sha256", facts["source_file"]["sha256"])
print("track samples", len(track_samples), "timeline rows", len(timeline))
