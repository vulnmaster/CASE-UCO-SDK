"""Magnet ACQUIRE imaging summaries: ``image_info.txt`` and ``activity_log.txt``.

ACQUIRE writes ``image_info.txt`` beside every image: ``Key: Value`` lines,
with untitled header lines ("Device Information", "Imaging Activities")
starting new sections. Checked against two public Digital Corpora
acquisitions of one iPhone SE by Magnet ACQUIRE 2.25.0.20236 (iOS 13.3.1 and
13.4.1, April 2020).

Times come from the ``Imaging Start UTC`` / ``Imaging End UTC`` fields, and
from their ``... Ticks`` companions (.NET ticks, 100 ns since 0001-01-01 UTC)
when present, because the ticks carry sub-second precision. The output
directory name is local time and is not used as a timestamp.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path, PureWindowsPath
from typing import Any

from case_uco.vendors._common import extension, shared_node, strings

__all__ = [
    "AcquireRecord",
    "AcquireSegment",
    "acquire_to_graph",
    "parse_acquire_image_info",
    "read_acquire_image_info",
]

_SEGMENT_KEY = re.compile(r"^(Relative|Full) Segment (\d+) Path$")
_SEGMENT_HASH_KEY = re.compile(r"^Segment (\d+) (\w+) Hash$")
_HEX = re.compile(r"^[0-9A-Fa-f]+$")
_HASH_LENGTHS = {"MD5": 32, "SHA1": 40, "SHA256": 64, "SHA512": 128}
_DOTNET_EPOCH = datetime(1, 1, 1, tzinfo=timezone.utc)


@dataclass
class AcquireSegment:
    index: int
    relative_path: str | None = None
    full_path: str | None = None
    hashes: dict[str, str] = field(default_factory=dict)


@dataclass
class AcquireRecord:
    """What one ``image_info.txt`` states, plus warnings about what it didn't."""

    source_name: str | None = None
    source_sha256: str | None = None
    product: str | None = None
    version: str | None = None
    examiner: str | None = None
    evidence_number: str | None = None
    description: str | None = None
    output_directory: str | None = None
    activity_log_path: str | None = None
    activity_log_md5: str | None = None
    activity_log_verified: bool | None = None
    segments: list[AcquireSegment] = field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    device: dict[str, str] = field(default_factory=dict)
    additional_device: dict[str, str] = field(default_factory=dict)
    activities: dict[str, str] = field(default_factory=dict)
    sections: dict[str, dict[str, str]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def device_key(self) -> str | None:
        for source, key in (
            (self.additional_device, "Unique Device ID"),
            (self.device, "Unique Identifier"),
            (self.device, "Serial Number"),
            (self.additional_device, "IMEI"),
        ):
            if source.get(key):
                return source[key]
        return None


def _decode(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1")


def _sections(text: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {"": {}}
    current = sections[""]
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        key, sep, value = line.partition(":")
        if sep and key.strip():
            current.setdefault(key.strip(), value.strip())
        else:
            current = sections.setdefault(line, {})
    return sections


def _utc(text: str | None, ticks: str | None, label: str, warnings: list[str]) -> datetime | None:
    parsed = None
    if text:
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        except ValueError:
            warnings.append(f"{label}: unrecognised date {text!r}")
    if ticks and ticks.isdigit():
        from_ticks = _DOTNET_EPOCH + timedelta(microseconds=int(ticks) // 10)
        if parsed and abs((from_ticks - parsed).total_seconds()) >= 1:
            warnings.append(f"{label}: ticks {ticks} disagree with {text!r}; using the text value")
            return parsed
        return from_ticks
    return parsed


def parse_acquire_image_info(
    data: bytes | str,
    *,
    source_name: str | None = None,
    activity_log: bytes | None = None,
) -> AcquireRecord:
    raw = data.encode("utf-8") if isinstance(data, str) else data
    record = AcquireRecord(source_name=source_name, source_sha256=hashlib.sha256(raw).hexdigest().upper())
    sections = _sections(_decode(raw))
    record.sections = sections
    top = sections[""]

    record.product = top.get("Imager Product") or None
    record.version = top.get("Imager Version") or None
    record.examiner = top.get("Examiner Name") or None
    record.evidence_number = top.get("Evidence Number") or None
    record.description = top.get("Description") or None
    record.output_directory = top.get("Output Directory") or None
    record.activity_log_path = top.get("Relative Activity Log Path") or None
    record.activity_log_md5 = (top.get("Activity Log MD5 Hash") or "").upper() or None
    if not record.product:
        record.warnings.append("no 'Imager Product' line")

    segments: dict[int, AcquireSegment] = {}
    for key, value in top.items():
        if match := _SEGMENT_KEY.match(key):
            seg = segments.setdefault(int(match[2]), AcquireSegment(int(match[2])))
            if match[1] == "Relative":
                seg.relative_path = value
            else:
                seg.full_path = value
        elif match := _SEGMENT_HASH_KEY.match(key):
            method = match[2].upper()
            seg = segments.setdefault(int(match[1]), AcquireSegment(int(match[1])))
            if _HEX.match(value) and len(value) == _HASH_LENGTHS.get(method, len(value)):
                seg.hashes[method] = value.upper()
            else:
                record.warnings.append(f"segment {match[1]}: {method} value {value!r} is not a digest")
    record.segments = [segments[i] for i in sorted(segments)]
    declared = top.get("Total Segments")
    if declared and declared.isdigit() and int(declared) != len(record.segments):
        record.warnings.append(f"Total Segments says {declared}, found {len(record.segments)}")

    record.start_time = _utc(
        top.get("Imaging Start UTC"), top.get("Imaging Start UTC Ticks"), "Imaging Start", record.warnings
    )
    record.end_time = _utc(
        top.get("Imaging End UTC"), top.get("Imaging End UTC Ticks"), "Imaging End", record.warnings
    )
    if record.start_time is None:
        record.warnings.append("no imaging start time")

    record.device = sections.get("Device Information", {})
    record.additional_device = sections.get("Additional Device Information", {})
    record.activities = sections.get("Imaging Activities", {})
    for activity, status in record.activities.items():
        if status.lower() != "success":
            record.warnings.append(f"imaging activity {activity}: {status}")

    if activity_log is not None:
        actual = hashlib.md5(activity_log).hexdigest().upper()
        record.activity_log_verified = actual == record.activity_log_md5
        if not record.activity_log_verified:
            record.warnings.append(
                f"activity log MD5 {actual} does not match the recorded {record.activity_log_md5}"
            )
    return record


def read_acquire_image_info(path: str | Path, *, verify_activity_log: bool = True) -> AcquireRecord:
    """Read ``image_info.txt``; verify the activity log beside it when present."""
    p = Path(path)
    data = p.read_bytes()
    log_bytes = None
    if verify_activity_log:
        relative = _sections(_decode(data))[""].get("Relative Activity Log Path")
        candidate = p.parent / PureWindowsPath(relative).as_posix() if relative else None
        if candidate is not None and candidate.is_file():
            log_bytes = candidate.read_bytes()
    record = parse_acquire_image_info(data, source_name=p.name, activity_log=log_bytes)
    if verify_activity_log and log_bytes is None and record.activity_log_md5:
        record.warnings.append("activity log not found beside image_info; MD5 not verified")
    return record


def acquire_to_graph(graph: Any, record: AcquireRecord) -> dict[str, Any]:
    """Add the acquisition an ``image_info.txt`` describes to ``graph``.

    IDs are deterministic: the device is keyed on its unique device ID (so two
    acquisitions of one phone share it), the acquisition on device and start
    time. Returns the created nodes by role.
    """
    from case_uco.case.investigation import InvestigativeAction, ProvenanceRecord
    from case_uco.ids import deterministic_id
    from case_uco.uco.identity import Identity, Organization
    from case_uco.uco.observable import (
        ContentDataFacet,
        Device,
        DeviceFacet,
        File,
        FileFacet,
        MobileDeviceFacet,
        MobilePhone,
        OperatingSystem,
        SoftwareFacet,
    )
    from case_uco.uco.tool import Tool
    from case_uco.uco.types import Hash

    device_key = record.device_key or record.source_sha256
    acquisition_key = (device_key, record.start_time or record.source_sha256)
    created: dict[str, Any] = {}

    magnet = shared_node(graph, Organization, "Magnet Forensics", name="Magnet Forensics")
    product = record.product or "Magnet ACQUIRE"
    created["tool"] = shared_node(
        graph,
        Tool,
        product,
        record.version or "",
        name=product,
        version=record.version,
        tool_type="Acquisition",
        creator=magnet,
    )

    vendor_name = record.device.get("Manufacturer")
    manufacturer = shared_node(graph, Organization, vendor_name, name=vendor_name) if vendor_name else None
    imei = record.additional_device.get("IMEI")
    device_class = record.additional_device.get("Device Class", "")
    is_phone = bool(imei) or "phone" in device_class.lower()
    model = record.additional_device.get("Pretty Name") or record.device.get("Product Model")
    created["device"] = shared_node(
        graph,
        MobilePhone if is_phone else Device,
        device_key,
        has_facet=[
            DeviceFacet(
                manufacturer=manufacturer,
                model=model,
                serial_number=record.device.get("Serial Number"),
                device_type=device_class or None,
            ),
            *([MobileDeviceFacet(imei=[imei])] if imei else []),
        ],
    )

    os_version = record.device.get("Operating System Version")
    if os_version:
        created["operating_system"] = shared_node(
            graph,
            OperatingSystem,
            device_key,
            os_version,
            extra_types=("uco-observable:Software",),
            name=os_version,
            has_facet=[SoftwareFacet(version=os_version, manufacturer=manufacturer)],
        )

    segments = []
    for seg in record.segments:
        name = PureWindowsPath(seg.relative_path or seg.full_path or f"segment {seg.index}").name
        facets: list[Any] = [
            FileFacet(file_name=strings(name), file_path=strings(seg.full_path), extension=extension(name))
        ]
        if seg.hashes:
            facets.append(ContentDataFacet(
                hash=[Hash(hash_method=m, hash_value=v) for m, v in sorted(seg.hashes.items())]
            ))
        segments.append(graph.create(
            File, id=deterministic_id(File, *acquisition_key, "segment", seg.index), name=name, has_facet=facets
        ))
    created["segments"] = segments

    results = list(segments)
    if record.activity_log_path:
        log_facets: list[Any] = [FileFacet(file_name=strings(PureWindowsPath(record.activity_log_path).name))]
        if record.activity_log_md5:
            log_facets.append(ContentDataFacet(hash=[Hash(hash_method="MD5", hash_value=record.activity_log_md5)]))
        verified = {
            True: ["MD5 verified against the log file."],
            False: ["MD5 does not match the log file."],
            None: [],
        }[record.activity_log_verified]
        created["activity_log"] = graph.create(
            File,
            id=deterministic_id(File, *acquisition_key, "activity log"),
            name=record.activity_log_path,
            has_facet=log_facets,
            description=verified,
        )
        results.append(created["activity_log"])

    performer = (
        shared_node(graph, Identity, "examiner", record.examiner, name=record.examiner)
        if record.examiner
        else None
    )
    details = [f"{activity}: {status}" for activity, status in record.activities.items()]
    if record.description:
        details.append(record.description)
    created["action"] = graph.create(
        InvestigativeAction,
        id=deterministic_id(InvestigativeAction, *acquisition_key),
        name=f"{product} acquisition of {model or 'device'}",
        start_time=record.start_time,
        end_time=record.end_time,
        instrument=[created["tool"]],
        performer=performer,
        object=[created["device"]],
        result=results,
        description=details,
    )

    if record.evidence_number and segments:
        created["provenance"] = graph.create(
            ProvenanceRecord,
            id=deterministic_id(ProvenanceRecord, *acquisition_key),
            exhibit_number=record.evidence_number,
            object=segments,
        )
    return created
