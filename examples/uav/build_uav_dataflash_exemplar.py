#!/usr/bin/env python3
"""Build a CASE/UCO graph for ArduPilot DataFlash / MAVLink UAV forensics.

Grounded in the DFRWS USA 2026 Rodeo BuiltToFall track evidence file
``uavrodeo.BIN`` (ArduPilot DataFlash, header magic ``YFMT``), parsed with
pymavlink ``DFReader`` / ``mavlogdump.py``.

Tier note: field values below are taken from a real workshop DataFlash
parse (ORGN/GPS coordinates, MSG status text, MODE, firmware string).
Source bytes are not shipped in this repository; do not invent digests.

DFRWS Rodeo Team: GreenLizards

Ontology gap called out by this exemplar (see change_proposals/):
UCO has ``uco-observable:Drone`` but no MAVLink system/component id,
flight-mode, TimeUS, or status-text facets — those facts are forced into
``EventRecordFacet.eventRecordText`` until an upstream proposal lands.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path


def _is_repo_root(candidate: Path) -> bool:
    return (candidate / "docs" / "recipes").is_dir() and (candidate / "python" / "case_uco").is_dir()


def _find_repo_root() -> Path:
    if "CASE_UCO_LIBRARIES_ROOT" in os.environ:
        candidate = Path(os.environ["CASE_UCO_LIBRARIES_ROOT"]).resolve()
        if not _is_repo_root(candidate):
            raise RuntimeError(f"CASE_UCO_LIBRARIES_ROOT is not a repo root: {candidate}")
        return candidate
    here = Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if _is_repo_root(candidate):
            return candidate
    raise RuntimeError("Could not locate CASE-UCO-SDK root; set CASE_UCO_LIBRARIES_ROOT")


def dt(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


ROOT = _find_repo_root()
sys.path.insert(0, str(ROOT / "python"))

from case_uco import CASEGraph  # noqa: E402
from case_uco.case.investigation import Investigation, InvestigativeAction  # noqa: E402
from case_uco.uco.core import Relationship  # noqa: E402
from case_uco.uco.identity import Identity  # noqa: E402
from case_uco.uco.location import LatLongCoordinatesFacet, Location  # noqa: E402
from case_uco.uco.observable import (  # noqa: E402
    ApplicationFacet,
    ContentDataFacet,
    DeviceFacet,
    Drone,
    EventRecord,
    EventRecordFacet,
    FileFacet,
    GeoLocationEntry,
    GeoLocationEntryFacet,
    GeoLocationTrack,
    GeoLocationTrackFacet,
    ObservableObject,
)
from case_uco.uco.tool import Tool  # noqa: E402


def build() -> CASEGraph:
    graph = CASEGraph(kb_prefix="http://example.org/kb/dfrws-rodeo26-uav/")

    graph.create(
        Identity,
        id="kb:identity-greenlizards",
        name="GreenLizards (DFRWS USA 2026 Rodeo team)",
    )
    graph.create(Identity, id="kb:identity-analyst", name="DFRWS Rodeo examiner")

    tool = graph.create(
        Tool,
        id="kb:tool-pymavlink",
        name="pymavlink DFReader / mavlogdump.py",
        version="2.4.41",
        description="Parses ArduPilot DataFlash (.BIN) flight logs into typed message rows.",
        tool_type="extraction",
    )

    graph.create(
        Investigation,
        id="kb:investigation-rodeo26-uav",
        name="DFRWS USA 2026 Rodeo — BuiltToFall UAV track",
        description=(
            "CASE modeling of ArduPilot DataFlash evidence recovered as uavrodeo.BIN. "
            "DFRWS Rodeo Team: GreenLizards."
        ),
    )

    log_file = graph.create(
        ObservableObject,
        id="kb:file-uavrodeo-bin",
        name="uavrodeo.BIN",
        has_facet=[
            FileFacet(file_name=["uavrodeo.BIN"], extension="BIN", size_in_bytes=9_404_416),
            ContentDataFacet(mime_type=["application/octet-stream"], magic_number="YFMT"),
        ],
        description="ArduPilot DataFlash binary flight log (header magic YFMT).",
    )

    fc_sw = graph.create(
        ObservableObject,
        id="kb:app-arducopter",
        name="ArduCopter",
        has_facet=[ApplicationFacet(application_identifier="ArduCopter", version="4.6.0-dev")],
        description="Autopilot firmware string from MSG at arm: ArduCopter V4.6.0-dev (1e8e2504).",
    )

    drone = graph.create(
        Drone,
        id="kb:drone-1",
        name="SITL ArduCopter QUAD/PLUS",
        has_facet=[DeviceFacet(device_type="UAV", model="QUAD/PLUS")],
        description=(
            "UAV platform inferred from DataFlash MSG Frame: QUAD/PLUS and RC Protocol: SITL. "
            "UCO models Drone as MobileDevice subclass but has no MAVLink system-id, component-id, "
            "flight-mode, or TimeUS facets; those values are recorded as EventRecord text until an "
            "upstream proposal lands."
        ),
    )

    home = graph.create(
        Location,
        id="kb:loc-home-orgn",
        name="ORGN home / first GPS fix",
        has_facet=[
            LatLongCoordinatesFacet(latitude=51.7607129, longitude=-1.2563709, altitude=0.1)
        ],
        description=(
            "ORGN Type 0/1 and first GPS fix (Status=6, NSats=10, HDop=1.21). "
            "Oxford, UK SITL region."
        ),
    )
    last_gps_loc = graph.create(
        Location,
        id="kb:loc-last-gps",
        name="Last GPS fix",
        has_facet=[LatLongCoordinatesFacet(latitude=51.7607132, longitude=-1.2563711)],
    )

    entry_start = graph.create(
        GeoLocationEntry,
        id="kb:geo-entry-start",
        has_facet=[
            GeoLocationEntryFacet(
                location=home,
                observable_created_time=dt("2026-07-04T11:51:07Z"),
            )
        ],
    )
    entry_end = graph.create(
        GeoLocationEntry,
        id="kb:geo-entry-end",
        has_facet=[
            GeoLocationEntryFacet(
                location=last_gps_loc,
                observable_created_time=dt("2026-07-04T11:53:04Z"),
            )
        ],
    )
    track = graph.create(
        GeoLocationTrack,
        id="kb:geo-track-flight",
        name="GPS track from DataFlash GPS messages",
        has_facet=[
            GeoLocationTrackFacet(
                start_time=dt("2026-07-04T11:51:07Z"),
                end_time=dt("2026-07-04T11:53:22Z"),
                geo_location_entry=[entry_start, entry_end],
            )
        ],
        description=(
            "Contiguous GPS path; max alt ~20.1 m, max groundspeed ~10.12 m/s, "
            "span ~135.69 s TimeUS."
        ),
    )

    graph.create(
        EventRecord,
        id="kb:event-msg-dfrws26",
        name="DataFlash MSG status text",
        has_facet=[
            EventRecordFacet(
                event_record_text="SRC=141/190:DFRWS26",
                application=fc_sw,
                event_type="MAVLink.STATUS_TEXT",
                event_record_id="TimeUS=95394327",
                observable_created_time=dt("2026-07-04T11:51:59Z"),
            )
        ],
        description=(
            "Planted MAVLink status text. Source system/component 141/190 cannot be typed on a "
            "MAVLink facet (ontology gap). Free-text only until UCO gains MAVLink/UAV flight-log "
            "properties."
        ),
    )
    graph.create(
        EventRecord,
        id="kb:event-mode-guided",
        name="Flight mode GUIDED",
        has_facet=[
            EventRecordFacet(
                event_record_text="MODE ModeNum=4 GUIDED Reason=2",
                event_type="ArduPilot.MODE",
                event_record_id="TimeUS=43415960",
                observable_created_time=dt("2026-07-04T11:51:07Z"),
            )
        ],
        description=(
            "Flight mode transitions are first-class investigative facts but have no typed "
            "property on Drone."
        ),
    )

    graph.create(
        InvestigativeAction,
        id="kb:action-parse-dataflash",
        name="Parse ArduPilot DataFlash with pymavlink",
        description="Extract MSG, MODE, GPS, ORGN, MAVC from uavrodeo.BIN.",
        start_time=dt("2026-07-28T00:00:00Z"),
        instrument=[tool],
        object=[log_file],
    )

    graph.create(
        Relationship,
        id="kb:rel-log-associated-drone",
        source=[log_file],
        target=drone,
        kind_of_relationship="Contained_Within",
        is_directional=True,
        description="Flight log associated with the UAV platform under examination.",
    )
    graph.create(
        Relationship,
        id="kb:rel-track-drone",
        source=[track],
        target=drone,
        kind_of_relationship="Path_Of",
        is_directional=True,
    )

    return graph


def main() -> None:
    out = Path(__file__).resolve().parent / "uav-dataflash-greenlizards.jsonld"
    graph = build()
    graph.write(str(out))
    print(f"wrote {out} ({len(graph)} objects)")


if __name__ == "__main__":
    main()
