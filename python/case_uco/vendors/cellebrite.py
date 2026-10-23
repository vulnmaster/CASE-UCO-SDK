"""Cellebrite UFED output: ``.ufd``, ``EvidenceCollection.ufdx``, and ``report.xml``.

The ``.ufd`` file is an INI-style summary UFED writes beside every extraction.
Its layout has drifted across releases; the readers here were checked against
three public Digital Corpora extractions:

* UFED 7.28.2.8 (2020, Android 10): no ``[DeviceInfo]`` section, one
  ``[Dump/...]`` section per extracted file, no ``AcquisitionTool`` key.
* Cellebrite Premium SaaS 7.64.0.271 (2023, iOS 15.3.1): ``[DeviceInfo]`` with
  ``IMEI`` and the device passcode in clear text, ``[Keychain]`` section.
* Inseyets UFED Pro Advanced 10.2.0.359 (2024, Android 14): ``IMEI1``/``IMEI2``,
  ``Chipset``, ``SecurityPatchLevel``, ``[InstalledApps]``, a second hash entry
  for ``SummaryReport.pdf``.

Passcodes and passwords are withheld from the record unless the caller asks
for them with ``include_secrets=True``; ``passcode_present`` still records that
the file held one.
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from html import unescape
from pathlib import Path
from typing import Any, Iterator

from case_uco.vendors._common import extension, shared_node, strings

__all__ = [
    "UfedField",
    "UfedMetadataItem",
    "UfedModel",
    "UfedReport",
    "UfedSourceLink",
    "UfedTaggedFile",
    "UfdHash",
    "UfdRecord",
    "UfdxExtraction",
    "UfdxRecord",
    "parse_ufd",
    "parse_ufdx",
    "read_ufd",
    "iter_report",
    "read_report_summary",
    "read_ufdx",
    "tagged_files_to_graph",
    "ufd_to_graph",
]

_HASH_SECTIONS = {
    "MD5": "MD5",
    "SHA1": "SHA1",
    "SHA-1": "SHA1",
    "SHA256": "SHA256",
    "SHA-256": "SHA256",
    "SHA512": "SHA512",
    "SHA-512": "SHA512",
}
_SECRET_KEY = re.compile(r"^(passcode|password|pin|pattern)(_\d+)?$", re.IGNORECASE)
_SECRET_DETAIL_KEY = re.compile(r"^(passcode|password|pin|pattern)", re.IGNORECASE)
_UFD_DATE = re.compile(
    r"^\s*(\d{1,2})/(\d{1,2})/(\d{4})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?"
    r"\s*(?:\(\s*([+-]?\d{1,2})(?:[.:](\d{1,2}))?\s*\))?\s*$"
)


@dataclass
class UfdHash:
    """A digest UFED recorded for one file of the extraction."""

    file_name: str
    method: str
    value: str


@dataclass
class UfdRecord:
    """Normalized content of one ``.ufd`` file."""

    source_name: str | None = None
    source_sha256: str | None = None
    ufd_version: str | None = None
    vendor: str | None = None
    model: str | None = None
    device_model: str | None = None
    full_name: str | None = None
    os: str | None = None
    chipset: str | None = None
    security_patch_level: str | None = None
    imeis: list[str] = field(default_factory=list)
    acquisition_tool: str | None = None
    version: str | None = None
    internal_build: str | None = None
    resources_version: str | None = None
    extraction_type: str | None = None
    extraction_method: str | None = None
    extraction_name: str | None = None
    extraction_status: str | None = None
    connection_type: str | None = None
    machine_name: str | None = None
    unit_id: str | None = None
    user_name: str | None = None
    guid: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    dumps: dict[str, str] = field(default_factory=dict)
    hashes: list[UfdHash] = field(default_factory=list)
    hmac: str | None = None
    passcode_present: bool = False
    secrets: dict[str, str] = field(default_factory=dict)
    sections: dict[str, dict[str, str]] = field(default_factory=dict)
    file_part_sections: int = 0
    warnings: list[str] = field(default_factory=list)

    @property
    def dump_files(self) -> list[str]:
        """Distinct container files named in ``[Dumps]``, in file order."""
        seen: list[str] = []
        for name in self.dumps.values():
            if name and name not in seen:
                seen.append(name)
        return seen

    def hashes_for(self, file_name: str) -> list[UfdHash]:
        return [h for h in self.hashes if h.file_name == file_name]


@dataclass
class UfdxExtraction:
    transfer_type: str | None
    path: str | None


@dataclass
class UfdxRecord:
    """Normalized content of an ``EvidenceCollection.ufdx`` file."""

    evidence_id: str | None = None
    vendor: str | None = None
    model: str | None = None
    device_guid: str | None = None
    extractions: list[UfdxExtraction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _decode(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            text = data.decode(encoding)
        except UnicodeDecodeError:
            continue
        if encoding == "utf-16" and "[" not in text:
            continue
        return text
    return data.decode("cp1252", errors="replace")


def _ini_sections(text: str) -> tuple[dict[str, dict[str, str]], int]:
    """Split INI text into sections, skipping per-file ``[Dump/...]`` parts.

    Repeated keys keep the first value; repeated sections are merged.
    """
    sections: dict[str, dict[str, str]] = {}
    file_parts = 0
    current: dict[str, str] | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line[0] in ";#":
            continue
        if line.startswith("[") and line.endswith("]"):
            name = line[1:-1].strip()
            if "/" in name or "\\" in name:
                file_parts += 1
                current = None
                continue
            current = sections.setdefault(name, {})
            continue
        if current is None or "=" not in line:
            continue
        key, value = line.split("=", 1)
        current.setdefault(key.strip(), unescape(value.strip()))
    return sections, file_parts


def _lookup(sections: dict[str, dict[str, str]], key: str, *order: str) -> str | None:
    """Return the first non-empty value for ``key`` across ``order`` sections."""
    for name in order:
        value = sections.get(name, {}).get(key)
        if value:
            return value
    return None


def _parse_ufd_date(value: str | None, warnings: list[str], label: str) -> datetime | None:
    """Parse ``dd/mm/yyyy HH:MM:SS (-4)``.

    UFED writes the day first in every sample seen. When both leading fields
    are 12 or less the order cannot be proven from the value, so day-first is
    assumed and a warning is recorded.
    """
    if not value:
        return None
    match = _UFD_DATE.match(value)
    if not match:
        warnings.append(f"{label}: unrecognized date {value!r}")
        return None
    a, b, year, hour, minute, second, off_h, off_m = match.groups()
    first, second_field = int(a), int(b)
    if first > 12:
        day, month = first, second_field
    elif second_field > 12:
        day, month = second_field, first
        warnings.append(f"{label}: {value!r} is month-first")
    else:
        day, month = first, second_field
        if first != second_field:
            warnings.append(f"{label}: assumed day-first for ambiguous date {value!r}")
    tz = None
    if off_h is not None:
        hours = int(off_h)
        minutes = int(off_m or 0)
        sign = -1 if off_h.startswith("-") else 1
        tz = timezone(sign * timedelta(hours=abs(hours), minutes=minutes))
    else:
        warnings.append(f"{label}: no UTC offset in {value!r}")
    try:
        return datetime(int(year), month, day, int(hour), int(minute), int(second or 0), tzinfo=tz)
    except ValueError:
        warnings.append(f"{label}: invalid date {value!r}")
        return None


def parse_ufd(
    data: bytes | str,
    *,
    source_name: str | None = None,
    include_secrets: bool = False,
) -> UfdRecord:
    """Parse the bytes or text of a ``.ufd`` file."""
    raw = data.encode("utf-8") if isinstance(data, str) else data
    text = _decode(raw)
    sections, file_parts = _ini_sections(text)
    record = UfdRecord(
        source_name=source_name,
        source_sha256=hashlib.sha256(raw).hexdigest().upper(),
        file_part_sections=file_parts,
    )
    warnings = record.warnings

    device = sections.get("DeviceInfo", {})
    if not device:
        warnings.append("no [DeviceInfo] section; device fields taken from [General]")
    for key in list(device):
        if _SECRET_DETAIL_KEY.match(key):
            if _SECRET_KEY.match(key):
                record.passcode_present = True
            value = device.pop(key)
            if include_secrets:
                record.secrets[key] = value

    record.vendor = _lookup(sections, "Vendor", "DeviceInfo", "General")
    record.model = _lookup(sections, "Model", "DeviceInfo", "General")
    record.device_model = _lookup(sections, "DeviceModel", "DeviceInfo")
    record.full_name = _lookup(sections, "FullName", "General")
    record.os = _lookup(sections, "OS", "DeviceInfo", "General")
    record.chipset = _lookup(sections, "Chipset", "DeviceInfo")
    record.security_patch_level = _lookup(sections, "SecurityPatchLevel", "DeviceInfo")
    imei_keys = sorted(
        (k for k in device if re.fullmatch(r"IMEI\d*", k)),
        key=lambda k: (len(k), k),
    )
    record.imeis = [device[k] for k in imei_keys if device[k]]

    record.ufd_version = _lookup(sections, "UfdVer", "General")
    record.acquisition_tool = _lookup(sections, "AcquisitionTool", "General")
    record.version = _lookup(sections, "Version", "General")
    record.internal_build = _lookup(sections, "InternalBuild", "General")
    record.resources_version = _lookup(sections, "EVS_ResourcesVersion", "General")
    record.extraction_type = _lookup(sections, "ExtractionType", "General")
    record.extraction_name = _lookup(sections, "ExtractionNameFromXML", "General")
    record.extraction_method = _lookup(sections, "ExtractionMethod", "FileDump", "Image")
    record.extraction_status = _lookup(sections, "ExtractionStatus", "ExtractionStatus")
    record.connection_type = _lookup(sections, "ConnectionType", "General")
    record.machine_name = _lookup(sections, "MachineName", "General")
    record.unit_id = _lookup(sections, "UnitId", "General")
    record.user_name = _lookup(sections, "UserName", "General")
    record.guid = _lookup(sections, "GUID", "General")
    record.start_time = _parse_ufd_date(_lookup(sections, "Date", "General"), warnings, "Date")
    record.end_time = _parse_ufd_date(_lookup(sections, "EndTime", "General"), warnings, "EndTime")
    if record.acquisition_tool is None:
        warnings.append("no AcquisitionTool key; the acquiring product is not named")

    record.dumps = dict(sections.get("Dumps", {}))
    for section_name, entries in sections.items():
        method = _HASH_SECTIONS.get(section_name.upper())
        if method is None:
            continue
        for file_name, value in entries.items():
            if re.fullmatch(r"[0-9A-Fa-f]+", value):
                record.hashes.append(UfdHash(file_name, method, value.upper()))
            else:
                warnings.append(f"[{section_name}] {file_name}: not a hex digest")
    record.hmac = _lookup(sections, "HMAC", "Hash")

    record.sections = sections
    return record


def read_ufd(path: str | Path, *, include_secrets: bool = False) -> UfdRecord:
    """Read a ``.ufd`` file from disk."""
    p = Path(path)
    return parse_ufd(p.read_bytes(), source_name=p.name, include_secrets=include_secrets)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_ufdx(data: bytes | str) -> UfdxRecord:
    """Parse an ``EvidenceCollection.ufdx`` document."""
    root = ET.fromstring(data.encode("utf-8") if isinstance(data, str) else data)
    record = UfdxRecord(evidence_id=root.get("EvidenceID"))
    for elem in root.iter():
        name = _local(elem.tag)
        if name == "DeviceInfo":
            record.vendor = elem.get("Vendor")
            record.model = elem.get("Model")
            record.device_guid = elem.get("Guid")
        elif name == "Extraction":
            record.extractions.append(
                UfdxExtraction(elem.get("TransferType"), elem.get("Path"))
            )
    if not record.extractions:
        record.warnings.append("no <Extraction> entries")
    return record


def read_ufdx(path: str | Path) -> UfdxRecord:
    return parse_ufdx(Path(path).read_bytes())


# --- report.xml ---------------------------------------------------------------

_REPORT_SECRET = re.compile(r"pass(code|word)|unlock|\bpin\b", re.IGNORECASE)


@dataclass
class UfedMetadataItem:
    section: str
    name: str
    value: str | None
    source_extraction: str | None = None


@dataclass
class UfedReport:
    """Project-level content of a ``report.xml``, filled while it is streamed."""

    namespace: str | None = None
    report_version: str | None = None
    project_id: str | None = None
    project_name: str | None = None
    extraction_type: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)
    extractions: list[dict[str, str]] = field(default_factory=list)
    metadata: list[UfedMetadataItem] = field(default_factory=list)
    case_information: dict[str, str] = field(default_factory=dict)
    images: list[dict[str, Any]] = field(default_factory=list)
    tagged_file_count: int = 0
    related_file_count: int = 0
    model_counts: dict[str, int] = field(default_factory=dict)
    source_link_count: int = 0
    secrets_withheld: int = 0
    warnings: list[str] = field(default_factory=list)

    def item(self, name: str, section: str | None = None) -> str | None:
        """First non-empty metadata value called ``name``, optionally within ``section``."""
        for entry in self.metadata:
            if entry.name == name and (section is None or entry.section == section) and entry.value:
                return entry.value
        return None


@dataclass
class UfedTaggedFile:
    """One ``<taggedFiles><file>`` entry, or a file nested in its ``<RelatedNodes>``.

    ``related_to`` is set on nested files: the ``id`` of the top-level file
    UFED grouped them under. In the reports examined, related files have the
    same size and MD5 as that file (``/data/user/0/...`` beside
    ``/data/data/...``, or one resource copied into several folders), appear
    nowhere else in the report, and are still the targets of ``nodeInfo``
    references, so they are full entries in their own right.
    """

    id: str | None
    path: str | None
    size: int | None
    fs: str | None
    deleted: str | None
    extraction_id: str | None
    attributes: dict[str, str] = field(default_factory=dict)
    timestamps: dict[str, str] = field(default_factory=dict)
    hashes: list[tuple[str, str]] = field(default_factory=list)
    local_path: str | None = None
    tags: str | None = None
    metadata: dict[str, dict[str, str]] = field(default_factory=dict)
    related_to: str | None = None
    jump_targets: list[str] = field(default_factory=list)
    source_models: list[dict[str, str]] = field(default_factory=list)


@dataclass
class UfedField:
    name: str
    type: str | None
    values: list[str | None] = field(default_factory=list)

    @property
    def value(self) -> str | None:
        return self.values[0] if self.values else None


@dataclass
class UfedModel:
    """One decoded ``<model>``, with nested models kept by field name."""

    type: str | None
    id: str | None
    deleted_state: str | None
    attributes: dict[str, str] = field(default_factory=dict)
    fields: dict[str, UfedField] = field(default_factory=dict)
    models: dict[str, list["UfedModel"]] = field(default_factory=dict)
    node_refs: dict[str, list[str]] = field(default_factory=dict)
    related: list["UfedModel"] = field(default_factory=list)
    jump_targets: list[str] = field(default_factory=list)

    def value(self, name: str) -> str | None:
        found = self.fields.get(name)
        return found.value if found else None


@dataclass
class UfedSourceLink:
    """``<extraInfo>``: where a model, file, or metadata item was read from.

    ``kind`` is the ``type`` attribute (``model``, ``node``, ``metaDataField``)
    and ``target_id`` the ``id`` of that model, tagged file, or project
    metadata item. Each entry of ``nodes`` is a ``<nodeInfo>``: usually
    ``id`` (a tagged file's ``id``), ``tableName`` and ``offset``; some carry
    ``path``, ``name`` and ``size`` inline instead of an ``id``.
    """

    target_id: str | None
    kind: str | None
    nodes: list[dict[str, str]] = field(default_factory=list)


def _text(elem: ET.Element) -> str | None:
    text = elem.text
    return text.strip() if text and text.strip() else None


def _report_metadata(elem: ET.Element) -> dict[str, str]:
    return {
        item.get("name", ""): (_text(item) or "")
        for item in elem
        if _local(item.tag) == "item"
    }


def _jump_targets(elem: ET.Element) -> list[str]:
    return [t for t in ((_text(j) or j.get("id")) for j in elem) if t]


def _tagged_files(
    elem: ET.Element, report: UfedReport, related_to: str | None = None
) -> list[UfedTaggedFile]:
    """The file ``elem`` followed by the files in its ``<RelatedNodes>``."""
    size = elem.get("size")
    tagged = UfedTaggedFile(
        id=elem.get("id"),
        path=elem.get("path"),
        size=int(size) if size and size.isdigit() else None,
        fs=elem.get("fs"),
        deleted=elem.get("deleted"),
        extraction_id=elem.get("extractionId"),
        attributes=dict(elem.attrib),
        related_to=related_to,
    )
    out = [tagged]
    for child in elem:
        name = _local(child.tag)
        if name == "RelatedNodes" and related_to is None:
            for nested in child:
                if _local(nested.tag) == "file":
                    out.extend(_tagged_files(nested, report, related_to=tagged.id))
        elif name == "jumptargets":
            tagged.jump_targets.extend(_jump_targets(child))
        elif name == "sourcemodels":
            tagged.source_models.extend(
                {**owner.attrib, "id": _text(owner) or ""} for owner in child
            )
        elif name == "accessInfo":
            for stamp in child:
                if _local(stamp.tag) == "timestamp" and _text(stamp):
                    tagged.timestamps[stamp.get("name", "")] = _text(stamp) or ""
        elif name == "metadata":
            section = child.get("section", "")
            items = _report_metadata(child)
            tagged.metadata[section] = items
            if section == "File":
                tagged.local_path = items.get("Local Path") or None
                tagged.tags = items.get("Tags") or None
                for key, value in items.items():
                    if key.upper().replace("-", "") in ("MD5", "SHA1", "SHA256", "SHA512") and value:
                        tagged.hashes.append((key, value))
    if tagged.path is None:
        report.warnings.append(f"tagged file {tagged.id} has no path attribute")
    return out


def _model(elem: ET.Element) -> UfedModel:
    model = UfedModel(
        type=elem.get("type"),
        id=elem.get("id"),
        deleted_state=elem.get("deleted_state"),
        attributes=dict(elem.attrib),
    )
    for child in elem:
        name = _local(child.tag)
        field_name = child.get("name", "")
        if name in ("field", "multiField", "dataField"):
            values = [_text(v) for v in child if _local(v.tag) == "value"]
            if not values and _text(child):
                values = [_text(child)]
            model.fields[field_name] = UfedField(field_name, child.get("type"), values)
        elif name in ("modelField", "multiModelField"):
            nested = [_model(m) for m in child if _local(m.tag) == "model"]
            model.models.setdefault(field_name, []).extend(nested)
        elif name == "nodeField":
            model.node_refs.setdefault(field_name, []).extend(
                ref for ref in (_text(i) for i in child) if ref
            )
        elif name == "RelatedModels":
            model.related.extend(_model(m) for m in child if _local(m.tag) == "model")
        elif name == "jumptargets":
            model.jump_targets.extend(_jump_targets(child))
    return model


def iter_report(
    source: str | Path | Any,
    *,
    report: UfedReport | None = None,
    model_types: set[str] | None = None,
    include_secrets: bool = False,
) -> Iterator[UfedTaggedFile | UfedModel | UfedSourceLink]:
    """Stream a UFED ``report.xml``, yielding tagged files, models and source links.

    Memory stays flat on multi-gigabyte reports: each record is yielded and
    then discarded. Files nested in a tagged file's ``<RelatedNodes>`` are
    yielded right after it with ``related_to`` set. Element names are matched without their namespace, so the
    ``http://pa.cellebrite.com/report/2.0`` default namespace and its variants
    all read the same way. Pass a ``UfedReport`` to collect the project
    header, counts and warnings as the stream goes; ``model_types`` limits
    which decoded models are built (the rest are only counted). Project
    metadata items whose names look like passcodes are withheld unless
    ``include_secrets`` is set.
    """
    report = report if report is not None else UfedReport()
    stack: list[ET.Element] = []
    for event, elem in ET.iterparse(source, events=("start", "end")):
        name = _local(elem.tag)
        if event == "start":
            if not stack:
                report.namespace = elem.tag[1:].split("}", 1)[0] if elem.tag.startswith("{") else None
                report.attributes = dict(elem.attrib)
                report.report_version = elem.get("reportVersion")
                report.project_id = elem.get("id")
                report.project_name = elem.get("name")
                report.extraction_type = elem.get("extractionType")
                if name != "project":
                    report.warnings.append(f"root element is <{name}>, not <project>")
                if report.report_version is None:
                    report.warnings.append("no reportVersion attribute on the root element")
            stack.append(elem)
            continue

        stack.pop()
        parent = _local(stack[-1].tag) if stack else None
        done = True
        if name == "file" and parent == "taggedFiles":
            files = _tagged_files(elem, report)
            report.tagged_file_count += 1
            report.related_file_count += len(files) - 1
            yield from files
        elif name == "model" and parent == "modelType":
            model_type = elem.get("type") or stack[-1].get("type") or ""
            report.model_counts[model_type] = report.model_counts.get(model_type, 0) + 1
            if model_types is None or model_type in model_types:
                yield _model(elem)
        elif name == "extraInfo":
            report.source_link_count += 1
            yield UfedSourceLink(
                target_id=elem.get("id"),
                kind=elem.get("type"),
                nodes=[dict(n.attrib) for n in elem.iter() if _local(n.tag) == "nodeInfo"],
            )
        elif name == "metadata" and parent == "project":
            section = elem.get("section", "")
            for item in elem:
                if _local(item.tag) != "item":
                    continue
                item_name = item.get("name", "")
                if _REPORT_SECRET.search(item_name) and not include_secrets:
                    report.secrets_withheld += 1
                    continue
                report.metadata.append(UfedMetadataItem(
                    section, item_name, _text(item), item.get("sourceExtraction")
                ))
        elif name == "extractionInfo":
            report.extractions.append(dict(elem.attrib))
        elif name == "field" and parent == "caseInformation":
            key = elem.get("name") or elem.get("fieldType") or ""
            report.case_information[key] = _text(elem) or ""
        elif name == "image" and parent == "images":
            hashes = [
                (item.get("name", ""), _text(item) or "")
                for meta in elem
                if _local(meta.tag) == "metadata"
                for item in meta
                if _local(item.tag) == "item"
            ]
            report.images.append({**elem.attrib, "hashes": hashes})
        else:
            done = False
        if done and stack:
            elem.clear()
            stack[-1].remove(elem)

    declared = report.attributes.get("NodeCount")
    seen = report.tagged_file_count + report.related_file_count
    if declared and declared.isdigit() and int(declared) != seen:
        report.warnings.append(
            f"NodeCount is {declared} but {seen} files were read; the report may be truncated"
        )


def read_report_summary(source: str | Path | Any, *, include_secrets: bool = False) -> UfedReport:
    """Read only the header, counts and warnings of a ``report.xml``."""
    report = UfedReport()
    for _ in iter_report(source, report=report, model_types=set(), include_secrets=include_secrets):
        pass
    return report


def _ufed_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def tagged_files_to_graph(
    graph: Any,
    files: Any,
    *,
    exhibit: str,
    report: str,
    warnings: list[str] | None = None,
) -> list[Any]:
    """Write tagged files with the cross-report identity tiers.

    ``exhibit`` keys the device's file system across every report of it;
    ``report`` keys this report (its SHA-256 is a good choice). Each entry's
    row key is the tagged file's ``id``. Recovered files get a
    ``RecoveredObjectFacet`` on the entry, which is this report's claim.

    A path only keys an exhibit file when the report gives it one content.
    Two cases break that, and ``files`` is read in full to find them:

    * Files marked ``embedded="true"`` were decoded out of another file and
      their paths are synthetic (two Chrome cache payloads share one). They
      are ``Extracted_From`` the nearest non-embedded file at or above their
      path.
    * Some non-embedded paths carry different content in one report: two
      versions of ``.GlobalPreferences.plist``, or emoji file names UFED wrote
      lossily as ``ð___``. Those entries keep their path and content cores
      but share no exhibit file, and each such path is added to ``warnings``.
    """
    from case_uco.uco.observable import RecoveredObjectFacet
    from case_uco.vendors.file_identity import add_reported_file, normalize_hash, normalize_path

    files = list(files)
    contents: dict[str, set[tuple[Any, ...]]] = {}
    for f in files:
        if f.path and f.attributes.get("embedded") != "true":
            digests = tuple(sorted(d for d in (normalize_hash(m, v) for m, v in f.hashes) if d))
            contents.setdefault(normalize_path(f.path), set()).add((f.size, digests))
    ambiguous = {p for p, seen in contents.items() if len(seen) > 1}
    for path in sorted(ambiguous):
        if warnings is not None:
            warnings.append(f"{len(contents[path])} different files share the path {path}")

    def container_of(path: str) -> str | None:
        current = normalize_path(path)
        while True:
            if current in contents:
                return None if current in ambiguous else current
            if "/" not in current.strip("/"):
                return None
            current = current.rsplit("/", 1)[0]

    written: list[Any] = []
    for tagged in files:
        times = {k.lower(): _ufed_time(v) for k, v in tagged.timestamps.items()}
        facets = []
        if tagged.deleted and tagged.deleted.lower() == "deleted":
            facets.append(RecoveredObjectFacet(content_recovered_status="recovered"))
        description = [f"UFED file system {tagged.fs}"] if tagged.fs else []
        if tagged.tags:
            description.append(f"UFED tags {tagged.tags}")
        if tagged.related_to:
            description.append(f"UFED lists this under RelatedNodes of tagged file {tagged.related_to}")
        embedded = tagged.attributes.get("embedded") == "true"
        container = container_of(tagged.path) if embedded and tagged.path else None
        shared = not embedded and not (tagged.path and normalize_path(tagged.path) in ambiguous)
        if embedded:
            description.append("UFED marks this file embedded: decoded from another file")
        elif not shared and tagged.path:
            description.append("UFED lists other files with different content at this path")
        written.append(add_reported_file(
            graph,
            exhibit=exhibit,
            report=report,
            row=tagged.id or tagged.path or str(len(written)),
            path=tagged.path,
            size=tagged.size,
            hashes=tagged.hashes,
            created=times.get("creationtime"),
            modified=times.get("modifytime") or times.get("modificationtime"),
            accessed=times.get("accesstime") or times.get("lastaccesstime"),
            entry_facets=facets,
            description=description,
            container_path=container,
            share_path=shared,
        ))
    return written


def ufd_to_graph(graph: Any, record: UfdRecord) -> dict[str, Any]:
    """Add the acquisition spine a ``.ufd`` describes to ``graph``.

    Node IDs come from :func:`case_uco.deterministic_id` keyed on the
    extraction GUID, so ingesting the same ``.ufd`` twice yields the same
    nodes. Returns the created instances by role.
    """
    from case_uco.case.investigation import InvestigativeAction
    from case_uco.ids import deterministic_id
    from case_uco.uco.identity import Organization
    from case_uco.uco.observable import (
        ContentDataFacet,
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

    key = record.guid or record.source_sha256 or "unknown"
    created: dict[str, Any] = {}

    cellebrite = shared_node(graph, Organization, "Cellebrite DI Ltd.", name="Cellebrite DI Ltd.")
    created["vendor"] = cellebrite

    tool_name = record.acquisition_tool or "UFED"
    tool_description = []
    if record.internal_build and record.internal_build != record.version:
        tool_description.append(f"InternalBuild {record.internal_build}")
    if record.resources_version:
        tool_description.append(f"EVS_ResourcesVersion {record.resources_version}")
    tool = shared_node(
        graph,
        Tool,
        tool_name,
        record.version or "",
        record.resources_version or "",
        name=tool_name,
        version=record.version,
        tool_type="Acquisition",
        creator=cellebrite,
        description=tool_description,
    )
    created["tool"] = tool

    manufacturer = (
        shared_node(graph, Organization, record.vendor, name=record.vendor)
        if record.vendor
        else None
    )

    device_key = record.imeis[0] if record.imeis else key
    phone = shared_node(
        graph,
        MobilePhone,
        device_key,
        has_facet=[
            DeviceFacet(
                manufacturer=manufacturer,
                model=record.model or record.full_name,
                device_type="Mobile Phone",
            ),
            *([MobileDeviceFacet(imei=list(record.imeis))] if record.imeis else []),
        ],
    )
    created["device"] = phone

    if record.os:
        # UCO 2.0.0 makes OperatingSystem a subclass of Software.
        created["operating_system"] = shared_node(
            graph,
            OperatingSystem,
            device_key,
            record.os,
            extra_types=("uco-observable:Software",),
            name=record.os,
            has_facet=[SoftwareFacet(version=record.os, manufacturer=manufacturer)],
        )

    dumps = []
    for file_name in record.dump_files:
        digests = record.hashes_for(file_name)
        facets: list[Any] = [FileFacet(file_name=strings(file_name), extension=extension(file_name))]
        if digests:
            facets.append(ContentDataFacet(
                hash=[Hash(hash_method=h.method, hash_value=h.value) for h in digests]
            ))
        dumps.append(graph.create(
            File,
            id=deterministic_id(File, key, file_name),
            name=file_name,
            has_facet=facets,
        ))
    created["dumps"] = dumps

    if record.source_name:
        created["ufd_file"] = graph.create(
            File,
            id=deterministic_id(File, key, record.source_name),
            name=record.source_name,
            has_facet=[
                FileFacet(file_name=strings(record.source_name), extension=extension(record.source_name)),
                ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value=record.source_sha256)]),
            ],
        )

    details = [
        f"{label} {value}"
        for label, value in (
            ("ExtractionType", record.extraction_type),
            ("ExtractionMethod", record.extraction_method),
            ("ExtractionNameFromXML", record.extraction_name),
            ("ExtractionStatus", record.extraction_status),
            ("ConnectionType", record.connection_type),
            ("MachineName", record.machine_name),
            ("UnitId", record.unit_id),
            ("GUID", record.guid),
        )
        if value
    ]
    if record.passcode_present:
        details.append("The .ufd records a device passcode; it is withheld from this graph.")
    label = " ".join(p for p in (record.extraction_type, "extraction") if p)
    created["action"] = graph.create(
        InvestigativeAction,
        id=deterministic_id(InvestigativeAction, key),
        name=f"UFED {label} of {record.full_name or record.model or 'device'}",
        start_time=record.start_time,
        end_time=record.end_time,
        instrument=[tool],
        object=[phone],
        result=[*dumps, *([created["ufd_file"]] if "ufd_file" in created else [])],
        description=details,
    )
    return created
