#!/usr/bin/env python3
"""Cross-report file identity: two reports of one exhibit converge on shared nodes.

Each report is ingested into its own graph with no knowledge of the other.
Deterministic IDs make the shared nodes (content cores, the exhibit file)
identical across both graphs, so loading them together merges instead of
duplicating, and re-ingesting a report changes nothing.

Tiers, per docs/recipes/cross-report-file-identity.md:

  content core   uco-observable:ContentData, one per (hash method, value, size)
  exhibit file   uco-observable:File, one per (exhibit, normalized path)
  report entry   uco-observable:File, one per (report, report row), values as reported

All bytes are defined here and every hash is computed over them.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph, Ref, deterministic_id
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.core import Relationship
from case_uco.uco.observable import (
    ContentData,
    ContentDataFacet,
    File,
    FileFacet,
    MobilePhone,
)
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cross-report-file-identity.jsonld"

EXHIBIT = "EXHIBIT-001"
PHOTO = b"\xff\xd8\xff\xe0 exemplar photo bytes \xff\xd9"
NOTES = b"exemplar notes file\n"
UTC = timezone.utc


@dataclass(frozen=True)
class ReportedFile:
    row: str
    path: str
    data: bytes
    hash_methods: tuple[str, ...]
    modified: datetime


@dataclass(frozen=True)
class Report:
    report_id: str
    tool: str
    run_at: datetime
    files: tuple[ReportedFile, ...]


# The SD card is FAT-formatted, so modified times have 2-second resolution and
# the two tools round the same timestamp differently (13 s against 12 s).
REPORT_A = Report(
    report_id="REPORT-A",
    tool="Report tool A",
    run_at=datetime(2026, 3, 2, 9, 0, tzinfo=UTC),
    files=(
        ReportedFile(
            row="1842",
            path="/storage/1A2B-3C4D/DCIM/Camera/IMG_0001.jpg",
            data=PHOTO,
            hash_methods=("MD5", "SHA256"),
            modified=datetime(2023, 1, 2, 10, 15, 13, tzinfo=UTC),
        ),
        ReportedFile(
            row="1843",
            path="/storage/1A2B-3C4D/Documents/notes.txt",
            data=NOTES,
            hash_methods=("MD5", "SHA256"),
            modified=datetime(2023, 1, 3, 8, 0, 0, tzinfo=UTC),
        ),
    ),
)
REPORT_B = Report(
    report_id="REPORT-B",
    tool="Report tool B",
    run_at=datetime(2026, 3, 4, 14, 30, tzinfo=UTC),
    files=(
        ReportedFile(
            row="files/77",
            path="\\storage\\1A2B-3C4D\\DCIM\\Camera\\IMG_0001.jpg",
            data=PHOTO,
            hash_methods=("MD5", "SHA1"),
            modified=datetime(2023, 1, 2, 10, 15, 12, tzinfo=UTC),
        ),
    ),
)

_DIGESTS = {"MD5": hashlib.md5, "SHA1": hashlib.sha1, "SHA256": hashlib.sha256}


def normalize_path(path: str) -> str:
    """One path convention per exhibit: forward slashes, no trailing slash."""
    return "/" + path.replace("\\", "/").strip("/")


def hash_value(method: str, data: bytes) -> str:
    return _DIGESTS[method](data).hexdigest().upper()


def ensure(graph: CASEGraph, cls: type, node_id: str, **kwargs) -> Ref:
    """Create a shared node once; later mentions reference it by IRI."""
    if not graph.contains(node_id):
        graph.create(cls, id=node_id, **kwargs)
    return Ref(node_id)


def relate(graph: CASEGraph, source_id: str, kind: str, target_id: str) -> None:
    graph.create_relationship(
        source_id,
        target_id,
        kind,
        relationship_id=deterministic_id(Relationship, source_id, kind, target_id),
    )


def build_report(report: Report) -> CASEGraph:
    graph = CASEGraph()
    exhibit = ensure(
        graph, MobilePhone, deterministic_id(MobilePhone, EXHIBIT), name=f"Exhibit {EXHIBIT}"
    )
    tool = ensure(graph, Tool, deterministic_id(Tool, report.tool), name=report.tool)

    entries = []
    for reported in report.files:
        size = len(reported.data)
        path = normalize_path(reported.path)
        name = path.rsplit("/", 1)[-1]
        hashes = [(m, hash_value(m, reported.data)) for m in reported.hash_methods]

        exhibit_file_id = deterministic_id(File, EXHIBIT, path)
        ensure(
            graph,
            File,
            exhibit_file_id,
            has_facet=[
                FileFacet(file_path=path, file_name=name, size_in_bytes=size),
                ContentDataFacet(
                    size_in_bytes=size,
                    hash=[Hash(hash_method=m, hash_value=v) for m, v in hashes],
                ),
            ],
        )

        for method, value in hashes:
            core_id = deterministic_id(ContentData, method, value, size)
            ensure(
                graph,
                ContentData,
                core_id,
                has_facet=[
                    ContentDataFacet(
                        size_in_bytes=size, hash=[Hash(hash_method=method, hash_value=value)]
                    )
                ],
            )
            relate(graph, core_id, "Contained_Within", exhibit_file_id)

        entry = graph.create(
            File,
            id=deterministic_id(File, report.report_id, reported.row),
            name=f"{report.report_id} row {reported.row}",
            has_facet=[
                FileFacet(
                    file_path=reported.path,
                    file_name=name,
                    size_in_bytes=size,
                    modified_time=reported.modified,
                ),
                ContentDataFacet(
                    size_in_bytes=size,
                    hash=[Hash(hash_method=m, hash_value=v) for m, v in hashes],
                ),
            ],
        )
        relate(graph, graph.get_id(entry), "Characterizes", exhibit_file_id)
        entries.append(entry)

    action = graph.create(
        InvestigativeAction,
        id=deterministic_id(InvestigativeAction, report.report_id),
        name=f"Produce {report.report_id}",
        start_time=report.run_at,
        instrument=[tool],
        object=[exhibit],
        result=entries,
    )
    graph.create(
        Investigation,
        id=deterministic_id(Investigation, EXHIBIT),
        name=f"File identity across reports for {EXHIBIT}",
        object=[exhibit, action],
    )
    return graph


def build() -> CASEGraph:
    combined = CASEGraph()
    for report in (REPORT_A, REPORT_B):
        combined.load(build_report(report).serialize(), on_duplicate="merge_compatible")

    before = combined.serialize()
    combined.load(build_report(REPORT_A).serialize(), on_duplicate="merge_compatible")
    if combined.serialize() != before:
        raise SystemExit("re-ingesting REPORT-A changed the combined graph")
    return combined


if __name__ == "__main__":
    build().write(str(OUTPUT))
    print(OUTPUT)
