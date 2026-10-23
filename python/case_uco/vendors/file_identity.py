"""Cross-report file identity: the three tiers of docs/recipes/cross-report-file-identity.md.

``add_reported_file`` writes one report row so that any number of reports of
the same exhibit, ingested separately and merged with
``on_duplicate="merge_compatible"``, converge on shared nodes:

* content core: ``uco-observable:ContentData``, one per (hash method, value, size)
* exhibit file: ``uco-observable:File``, one per (exhibit, normalized path),
  holding only facts the reports agree on plus the union of their hashes
* report entry: ``uco-observable:File``, one per (report, row), holding the
  report's values verbatim, timestamps included

Cores are ``Contained_Within`` the exhibit file; entries ``Characterizes`` it.

Files a tool decoded out of another file (a cache payload, an archive
member, a database blob) have synthetic paths that need not be unique, so
they get no exhibit file. Pass ``container_path``, the real file they came
from: the entry and its cores are then ``Extracted_From`` that file's
exhibit file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable

from case_uco.vendors._common import extension, strings

__all__ = ["ReportedFileNodes", "add_reported_file", "normalize_hash", "normalize_path"]

_METHODS = {
    "MD5": "MD5",
    "SHA1": "SHA1",
    "SHA-1": "SHA1",
    "SHA224": "SHA224",
    "SHA-224": "SHA224",
    "SHA256": "SHA256",
    "SHA-256": "SHA256",
    "SHA384": "SHA384",
    "SHA-384": "SHA384",
    "SHA512": "SHA512",
    "SHA-512": "SHA512",
}


@dataclass
class ReportedFileNodes:
    """IRIs written for one report row."""

    entry: str
    exhibit_file: str | None
    content_cores: list[str] = field(default_factory=list)
    container: str | None = None


def normalize_path(path: str) -> str:
    """One path convention per exhibit: forward slashes, one leading slash, no trailing slash."""
    return "/" + path.replace("\\", "/").strip("/")


def normalize_hash(method: str, value: str) -> tuple[str, str] | None:
    """Return ``(HashNameVocab member, upper-case hex)``, or ``None`` if either is unusable."""
    name = _METHODS.get(method.strip().upper())
    digest = value.strip().upper()
    if name is None or not digest or any(c not in "0123456789ABCDEF" for c in digest):
        return None
    return name, digest


def _ensure(graph: Any, cls: type, node_id: str, **kwargs: Any) -> str:
    """Create ``node_id`` or merge these properties into it (``merge_compatible``)."""
    if not graph.contains(node_id):
        graph.create(cls, id=node_id, **kwargs)
        return node_id
    from case_uco.graph import CASEGraph

    scratch = CASEGraph()
    scratch.create(cls, id=node_id, **kwargs)
    node = scratch.get(node_id) or {}
    graph.upsert_node(
        node_id,
        types=node.get("@type"),
        properties={k: v for k, v in node.items() if not k.startswith("@")},
    )
    return node_id


def _relate(graph: Any, source: str, kind: str, target: str) -> None:
    from case_uco.ids import deterministic_id
    from case_uco.uco.core import Relationship

    rel_id = deterministic_id(Relationship, source, kind, target)
    if not graph.contains(rel_id):
        graph.create_relationship(source, target, kind, relationship_id=rel_id)


def add_reported_file(
    graph: Any,
    *,
    exhibit: str,
    report: str,
    row: str,
    path: str | None,
    size: int | None = None,
    hashes: Iterable[tuple[str, str]] = (),
    created: datetime | None = None,
    modified: datetime | None = None,
    accessed: datetime | None = None,
    entry_facets: Iterable[Any] = (),
    name: str | None = None,
    description: Iterable[str] = (),
    container_path: str | None = None,
    share_path: bool = True,
) -> ReportedFileNodes:
    """Add one report row and the shared nodes it identifies.

    ``exhibit`` and ``report`` are stable keys the caller owns (an exhibit
    reference, a report file digest); ``row`` is the report's own identifier
    for the entry. Hashes that are not a recognized method with a hex value
    are skipped. Without a ``path``, with a ``container_path``, or with
    ``share_path=False`` (a synthetic path with no known container), there is
    no exhibit file for this row.
    """
    from case_uco.ids import deterministic_id
    from case_uco.uco.observable import ContentData, ContentDataFacet, File, FileFacet
    from case_uco.uco.types import Hash

    digests: list[tuple[str, str]] = []
    for method, value in hashes:
        normalized = normalize_hash(method, value)
        if normalized and normalized not in digests:
            digests.append(normalized)

    def content_facet(pairs: list[tuple[str, str]]) -> ContentDataFacet:
        return ContentDataFacet(
            size_in_bytes=size,
            hash=[Hash(hash_method=m, hash_value=v) for m, v in pairs],
        )

    exhibit_path = normalize_path(path) if path else None
    file_name = exhibit_path.rsplit("/", 1)[-1] if exhibit_path else None

    exhibit_file = None
    container = None
    if container_path:
        container_norm = normalize_path(container_path)
        container_name = container_norm.rsplit("/", 1)[-1]
        container = _ensure(
            graph,
            File,
            deterministic_id(File, exhibit, container_norm),
            has_facet=[
                FileFacet(
                    file_path=strings(container_norm),
                    file_name=strings(container_name),
                    extension=extension(container_name),
                )
            ],
        )
    elif exhibit_path and share_path:
        exhibit_file = _ensure(
            graph,
            File,
            deterministic_id(File, exhibit, exhibit_path),
            has_facet=[
                FileFacet(
                    file_path=strings(exhibit_path),
                    file_name=strings(file_name),
                    extension=extension(file_name) if file_name else None,
                    size_in_bytes=size,
                ),
                *([content_facet(digests)] if digests else []),
            ],
        )

    cores = []
    if size is not None:
        for method, value in digests:
            core = _ensure(
                graph,
                ContentData,
                deterministic_id(ContentData, method, value, size),
                has_facet=[content_facet([(method, value)])],
            )
            cores.append(core)
            if exhibit_file:
                _relate(graph, core, "Contained_Within", exhibit_file)
            elif container:
                _relate(graph, core, "Extracted_From", container)

    entry_id = deterministic_id(File, report, row)
    if not graph.contains(entry_id):
        graph.create(
            File,
            id=entry_id,
            name=name or f"{report} row {row}",
            description=list(description),
            has_facet=[
                FileFacet(
                    file_path=strings(path),
                    file_name=strings(file_name),
                    size_in_bytes=size,
                    observable_created_time=created,
                    modified_time=modified,
                    accessed_time=accessed,
                ),
                *([content_facet(digests)] if digests else []),
                *entry_facets,
            ],
        )
    if exhibit_file:
        _relate(graph, entry_id, "Characterizes", exhibit_file)
    elif container:
        _relate(graph, entry_id, "Extracted_From", container)
    return ReportedFileNodes(
        entry=entry_id, exhibit_file=exhibit_file, content_cores=cores, container=container
    )
