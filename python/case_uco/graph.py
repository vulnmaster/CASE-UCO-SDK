"""CASEGraph — the main entry point for building and serializing CASE/UCO graphs."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import uuid
import threading
import warnings
import dataclasses
from dataclasses import Field, dataclass, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, TypeVar, Type

from case_uco.typed_literal import TypedLiteral

T = TypeVar("T")

# Non-XSD RDF datatypes used as ``sh:datatype`` (lexical form + datatype IRI).
_CUSTOM_RDF_DATATYPE_IRIS = frozenset(
    {
        "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression",
    }
)

_builtin_id = id

# Duplicate @id policies — all SDK languages must default to ``reject``.
# Aliases: ``error`` → ``reject``.
DUPLICATE_POLICIES = frozenset(
    {
        "reject",
        "error",
        "merge_identical",
        "merge_compatible",
        "replace",
    }
)

_KIND_SLUG_RE = re.compile(r"[^A-Za-z0-9._-]+")
_KIND_SLUG_MAX_LEN = 64


class DuplicateNodeError(ValueError):
    """Raised when a node with the same @id conflicts with an existing node.

    Default policy is reject-on-conflict (all languages). Compatible
    multi-typing should use :meth:`CASEGraph.add_type` /
    :meth:`CASEGraph.upsert_node` instead of appending a second top-level
    object with the same IRI.
    """

    def __init__(self, node_id: str, detail: str = ""):
        self.node_id = node_id
        msg = f"Duplicate @id {node_id!r}"
        if detail:
            msg = f"{msg}: {detail}"
        super().__init__(msg)


class InvalidSplitSizeError(ValueError):
    """Raised when ``split`` receives a zero or negative chunk size."""

    def __init__(self, max_objects: int):
        self.max_objects = max_objects
        super().__init__(
            f"split max_objects must be a positive integer, got {max_objects!r}"
        )


class PartitionBoundaryError(ValueError):
    """A partition plan would widen marking or authorization access (#79)."""

    def __init__(
        self,
        root_id: str,
        node_id: str,
        missing_markings: list[str],
        missing_authorizations: list[str],
    ) -> None:
        self.root_id = root_id
        self.node_id = node_id
        self.missing_markings = missing_markings
        self.missing_authorizations = missing_authorizations
        super().__init__(
            f"partition root {root_id!r} is not authorized for node {node_id!r}; "
            f"missing markings={missing_markings}, "
            f"missing authorizations={missing_authorizations}"
        )


@dataclass(frozen=True)
class DeserializationWarning:
    """Typed diagnostic when a JSON-LD node falls back to a raw dict."""

    node_id: str | None
    reason: str
    detail: str = ""


# Standard CASE/UCO JSON-LD context prefixes
DEFAULT_CONTEXT: dict[str, str] = {
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "kb": "http://example.org/kb/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
    "uco-victim": "https://ontology.unifiedcyberontology.org/uco/victim/",
    "uco-analysis": "https://ontology.unifiedcyberontology.org/uco/analysis/",
    "uco-configuration": "https://ontology.unifiedcyberontology.org/uco/configuration/",
    "uco-marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
    "uco-pattern": "https://ontology.unifiedcyberontology.org/uco/pattern/",
    "uco-time": "https://ontology.unifiedcyberontology.org/uco/time/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

_RANGE_IRI_TO_TYPED_LITERAL = {
    "http://www.w3.org/2001/XMLSchema#boolean": "xsd:boolean",
    "http://www.w3.org/2001/XMLSchema#integer": "xsd:integer",
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": "xsd:nonNegativeInteger",
    "http://www.w3.org/2001/XMLSchema#positiveInteger": "xsd:positiveInteger",
    "http://www.w3.org/2001/XMLSchema#decimal": "xsd:decimal",
    "http://www.w3.org/2001/XMLSchema#float": "xsd:float",
    "http://www.w3.org/2001/XMLSchema#double": "xsd:double",
    "http://www.w3.org/2001/XMLSchema#dateTime": "xsd:dateTime",
    "http://www.w3.org/2001/XMLSchema#hexBinary": "xsd:hexBinary",
    "http://www.w3.org/2001/XMLSchema#anyURI": "xsd:anyURI",
}


class CASEGraph:
    """Build a CASE/UCO JSON-LD graph with typed objects.

    Usage:
        graph = CASEGraph(kb_prefix="http://example.org/kb/")
        tool = graph.create(Tool, name="Tool A")
        print(graph.serialize())
    """

    def __init__(
        self,
        kb_prefix: str = "http://example.org/kb/",
        extra_context: dict[str, str] | None = None,
    ):
        self.kb_prefix = kb_prefix
        self._context = dict(DEFAULT_CONTEXT)
        self._context["kb"] = kb_prefix
        # Uniform context-collision rejection (incl. constructor vs standard prefixes).
        if extra_context:
            self._merge_context(extra_context)
        self._objects: list[dict[str, Any]] = []
        self._id_map: dict[int, str] = {}
        self._instances: list[Any] = []
        # Expanded IRI → index into _objects (O(1) lookup).
        self._iri_index: dict[str, int] = {}
        # Compact form and expanded form both index to the same slot.
        self._iri_aliases: dict[str, str] = {}
        self._used_prefix_set: set[str] = set()
        # Default ``reject`` is required cross-language parity (C#/Java/Rust match).
        # Policies: reject|error, merge_identical, merge_compatible, replace.
        self.on_duplicate: str = "reject"
        self.deserialization_warnings: list[DeserializationWarning] = []

    def create(self, cls: Type[T], *, id: str | None = None, **kwargs: Any) -> T:
        """Create an instance of a CASE/UCO class and add it to the graph.

        Args:
            cls: The CASE/UCO class to instantiate.
            id: Optional user-supplied @id for deterministic IRIs.
                If not provided, a UUID-based @id is auto-generated.
            **kwargs: Arguments passed to the class constructor.

        Returns the created instance so it can be referenced by other objects.
        """
        instance = cls(**kwargs)
        self._validate_instance(instance)
        obj_id = id if id is not None else self._mint_id(instance)
        self._id_map[_builtin_id(instance)] = obj_id
        self._instances.append(instance)
        json_obj = self._to_jsonld(instance, obj_id)
        self._append_object(json_obj)
        return instance

    def add(self, instance: Any, *, id: str | None = None) -> str:
        """Add a pre-created instance to the graph.

        Args:
            instance: A dataclass instance of a CASE/UCO type.
            id: Optional user-supplied @id for deterministic IRIs.

        Returns the assigned @id.
        """
        self._validate_instance(instance)
        obj_id = id if id is not None else self._mint_id(instance)
        self._id_map[_builtin_id(instance)] = obj_id
        self._instances.append(instance)
        json_obj = self._to_jsonld(instance, obj_id)
        self._append_object(json_obj)
        return obj_id

    def get_id(self, instance: Any) -> str | None:
        """Get the @id for a previously added instance."""
        return self._id_map.get(_builtin_id(instance))

    def expand_iri(self, node_id: str) -> str:
        """Expand a compact IRI using this graph's context."""
        return _expand_iri(node_id, self._context)

    def contains(self, node_id: str) -> bool:
        """Return True if a node with this @id (compact or expanded) exists."""
        return self._find_object(node_id) is not None

    def get(self, node_id: str) -> dict[str, Any] | None:
        """Return a deep copy of the JSON-LD dict for a node by ``@id``.

        Nested lists/maps are not shared with the graph. Persist changes via
        :meth:`add_type`, :meth:`add_property`, :meth:`set_property`,
        :meth:`upsert_node`, or :meth:`link`.
        """
        obj = self._find_object(node_id)
        if obj is None:
            return None
        return copy.deepcopy(obj)

    def upsert_node(
        self,
        node_id: str,
        *,
        types: list[str] | str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create or update a JSON-LD node by ``@id``.

        Returns a deep copy (not a live internal map). Property merges use the
        same conflict engine as :meth:`load` / :meth:`add_property`
        (``merge_compatible``).
        """
        obj = self._find_object(node_id)
        if obj is None:
            obj = {"@id": node_id}
            if types is not None:
                obj["@type"] = self._normalize_type_value(types)
            if properties:
                for key, value in properties.items():
                    self._apply_property(
                        obj, key, value, node_id=node_id, mode="merge_compatible"
                    )
            self._append_object(obj)
            return copy.deepcopy(obj)

        if types is not None:
            merged = self._merge_types(obj.get("@type"), types)
            obj["@type"] = self._normalize_type_value(merged)
        if properties:
            for key, value in properties.items():
                self._apply_property(
                    obj, key, value, node_id=node_id, mode="merge_compatible"
                )
        self._track_prefixes_for(obj)
        return copy.deepcopy(obj)

    def add_type(self, node_id: str, type_iri: str) -> None:
        """Add an ``rdf:type`` to an existing node (same ``@id``)."""
        obj = self._require_object(node_id)
        merged = self._merge_types(obj.get("@type"), type_iri)
        obj["@type"] = self._normalize_type_value(merged)
        self._track_prefixes_for({"@type": type_iri})

    def add_property(self, node_id: str, key: str, value: Any) -> None:
        """Add or merge a property on an existing node (``merge_compatible``)."""
        obj = self._require_object(node_id)
        self._apply_property(obj, key, value, node_id=node_id, mode="merge_compatible")
        self._track_prefixes_for({key: value})

    def set_property(self, node_id: str, key: str, value: Any) -> None:
        """Replace a property value (scalar replacement / ``replace`` mode)."""
        obj = self._require_object(node_id)
        self._apply_property(obj, key, value, node_id=node_id, mode="replace")
        self._track_prefixes_for({key: value})

    def link(
        self,
        source_id: str,
        predicate: str,
        target_id: str | dict[str, Any],
    ) -> None:
        """Add a direct property edge ``source --predicate--> target``.

        Prefer :meth:`create_relationship` for ``uco-core:Relationship`` nodes.
        Use ``link`` for ontology properties such as ``prov:wasDerivedFrom``.
        """
        target_ref: dict[str, Any]
        if isinstance(target_id, str):
            target_ref = {"@id": target_id}
        else:
            target_ref = target_id
        self.add_property(source_id, predicate, target_ref)

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        kind: str,
        *,
        directional: bool = True,
        description: str | None = None,
        relationship_id: str | None = None,
        assertion_id: str | None = None,
        extra_types: list[str] | str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a ``uco-core:Relationship`` node with deterministic ``@id``.

        Validates that source and target nodes exist. Relationship IDs are
        derived from source, target, and kind unless ``relationship_id`` or
        ``assertion_id`` is set (so identical source/target/kind can coexist).
        """
        if not self.contains(source_id):
            raise KeyError(f"Relationship source not in graph: {source_id!r}")
        if not self.contains(target_id):
            raise KeyError(f"Relationship target not in graph: {target_id!r}")
        if not kind:
            raise ValueError("kindOfRelationship is required")

        rel_id = (
            relationship_id
            or assertion_id
            or self._deterministic_relationship_id(source_id, target_id, kind)
        )
        types: list[str] = ["uco-core:Relationship"]
        if extra_types:
            types = self._merge_types(types, extra_types)
        props: dict[str, Any] = {
            "uco-core:source": [{"@id": source_id}],
            "uco-core:target": [{"@id": target_id}],
            "uco-core:kindOfRelationship": kind,
            "uco-core:isDirectional": {
                "@type": "xsd:boolean",
                "@value": "true" if directional else "false",
            },
        }
        if description:
            props["uco-core:description"] = description
        if properties:
            props.update(properties)
        return self.upsert_node(rel_id, types=types, properties=props)

    def __len__(self) -> int:
        """Return the number of objects in the graph."""
        return len(self._objects)

    def serialize(self, format: str = "json-ld", indent: int | None = 4) -> str:
        """Serialize the graph to JSON-LD string."""
        if format != "json-ld":
            raise ValueError(
                f"Unsupported format: {format}. Only 'json-ld' is supported."
            )
        doc = {
            "@context": self._pruned_context(),
            "@graph": self._objects,
        }
        return json.dumps(doc, indent=indent, default=str)

    def write(self, path: str, format: str = "json-ld", indent: int = 4) -> None:
        """Write the graph to a file (materializes full string then writes)."""
        content = self.serialize(format=format, indent=indent)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def write_streaming(
        self,
        path: str,
        *,
        format: str = "json-ld",
        indent: int = 2,
        atomic: bool = True,
    ) -> dict[str, int]:
        """Stream JSON-LD to disk without building a second full document string.

        Emits ``@context`` then each ``@graph`` element incrementally. Peak
        memory is dominated by the in-memory graph itself rather than a
        duplicate serialized buffer. Retains :meth:`serialize` for callers
        that need a complete string.

        When ``atomic`` is True (default), writes through a temporary file and
        renames into place; partial temp files are removed on failure.

        Returns ``{"nodes": N, "bytes_written": B}``.
        """
        if format != "json-ld":
            raise ValueError(
                f"Unsupported format: {format}. Only 'json-ld' is supported."
            )
        import os
        import tempfile

        target = path
        out_path = path
        tmp_fd = None
        tmp_name = None
        if atomic:
            directory = os.path.dirname(os.path.abspath(path)) or "."
            os.makedirs(directory, exist_ok=True)
            tmp_fd, tmp_name = tempfile.mkstemp(
                prefix=".casegraph-", suffix=".jsonld.tmp", dir=directory
            )
            os.close(tmp_fd)
            tmp_fd = None
            out_path = tmp_name
        try:
            ctx = self._pruned_context()
            pad = " " * indent
            bytes_written = 0
            with open(out_path, "w", encoding="utf-8") as f:

                def _w(s: str) -> None:
                    nonlocal bytes_written
                    f.write(s)
                    bytes_written += len(s.encode("utf-8"))

                _w("{\n")
                _w(f'{pad}"@context": ')
                _w(json.dumps(ctx, indent=indent, default=str))
                _w(",\n")
                _w(f'{pad}"@graph": [\n')
                for i, obj in enumerate(self._objects):
                    chunk = json.dumps(obj, indent=indent, default=str)
                    indented = "\n".join(
                        pad + pad + line for line in chunk.splitlines()
                    )
                    _w(indented)
                    if i + 1 < len(self._objects):
                        _w(",\n")
                    else:
                        _w("\n")
                _w(f"{pad}]\n")
                _w("}\n")
                f.flush()
                os.fsync(f.fileno())
            if atomic and tmp_name:
                os.replace(tmp_name, target)
                tmp_name = None
            return {"nodes": len(self._objects), "bytes_written": bytes_written}
        except Exception:
            if tmp_name and os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise
        finally:
            if tmp_fd is not None:
                try:
                    os.close(tmp_fd)
                except OSError:
                    pass

    def write_stream(self, path: str, **kwargs: Any) -> dict[str, int]:
        """Alias for :meth:`write_streaming` (#71)."""
        return self.write_streaming(path, **kwargs)

    def load(self, json_str: str, *, on_duplicate: str | None = None) -> None:
        """Load a JSON-LD string, merging context and upserting objects.

        Duplicate ``@id`` handling follows ``on_duplicate`` or
        ``self.on_duplicate`` (default ``reject`` — all languages). Other
        policies: ``merge_identical``, ``merge_compatible``, ``replace``
        (``error`` is an alias for ``reject``).

        Context and node merges are staged and committed only if the entire
        document succeeds (transactional load).
        """
        policy = self._normalize_duplicate_policy(on_duplicate or self.on_duplicate)
        doc = json.loads(json_str)
        snapshot = self._snapshot_state()
        try:
            if "@context" in doc and isinstance(doc["@context"], dict):
                self._merge_context(doc["@context"])
            if "@graph" in doc and isinstance(doc["@graph"], list):
                for raw in doc["@graph"]:
                    if isinstance(raw, dict):
                        self._ingest_raw_node(dict(raw), policy=policy)
        except Exception:
            self._restore_state(snapshot)
            raise

    def load_file(self, path: str, *, on_duplicate: str | None = None) -> None:
        """Read and load a JSON-LD file into this graph."""
        with open(path, "r", encoding="utf-8") as f:
            self.load(f.read(), on_duplicate=on_duplicate)

    def validate(self, *, case_version: str = "case-1.4.0") -> str:
        """Validate this graph against CASE/UCO SHACL constraints.

        Thin CLI wrapper that returns ``case_validate`` stdout. For the rich
        structured report (extensions, profiles, concept coverage), use
        :meth:`validate_report` or ``case_uco.validation.validate_graph_file``.

        Requires ``case-utils`` to be installed::

            pip install case-uco[validation]

        Returns the validation output on success.
        Raises ``RuntimeError`` if validation fails or ``case_validate``
        is not available on PATH.
        """
        import os
        import shutil
        import subprocess
        import tempfile

        if not shutil.which("case_validate"):
            raise RuntimeError(
                "case_validate not found on PATH. "
                "Install with: pip install case-uco[validation]"
            )
        fd, tmp = tempfile.mkstemp(suffix=".jsonld")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(self.serialize())
            result = subprocess.run(
                ["case_validate", "--built-version", case_version, tmp],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                msg = result.stderr.strip() or result.stdout.strip()
                raise RuntimeError(f"Validation failed:\n{msg}")
            return result.stdout
        finally:
            os.unlink(tmp)

    def validate_report(
        self,
        *,
        extensions: list[str] | None = None,
        profiles: list[str] | None = None,
        strict_concepts: bool = True,
        project_root: str | Path | None = None,
        extra_ontology_graphs: list[str | Path] | None = None,
        force_rdfs_inference: bool = False,
        allow_warning: bool = True,
    ) -> Any:
        """Validate via the rich public API and return a structured report.

        Writes a temporary JSON-LD file and delegates to
        :func:`case_uco.validation.validate_graph_file`. Does not raise on
        SHACL non-conformance — inspect ``report.conforms``.

        Returns a :class:`case_uco.validation.GraphValidationReport`.
        """
        import os
        import tempfile

        from case_uco.validation import validate_graph_file

        fd, tmp = tempfile.mkstemp(suffix=".jsonld")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(self.serialize())
            kwargs: dict[str, Any] = {
                "allow_warning": allow_warning,
                "extensions": extensions,
                "profiles": profiles,
                "strict_concepts": strict_concepts,
                "extra_ontology_graphs": extra_ontology_graphs,
                "force_rdfs_inference": force_rdfs_inference,
            }
            if project_root is not None:
                kwargs["project_root"] = Path(project_root)
            return validate_graph_file(tmp, **kwargs)
        finally:
            os.unlink(tmp)

    def estimate_triples(self) -> int:
        """Estimate the number of RDF triples this graph will produce.

        Counts every ``rdf:type`` in multi-type arrays, each property value as
        a triple, and nested objects recursively. ``@id`` is not counted.
        Embedded nodes contribute their nested triples; ``{"@id": ...}``
        references count as one triple.
        """
        return sum(self._count_triples(obj) for obj in self._objects)

    @staticmethod
    def _count_triples(obj: dict[str, Any]) -> int:
        count = 0
        for key, value in obj.items():
            if key == "@id":
                continue
            if key == "@type":
                if isinstance(value, list):
                    count += len(value)
                else:
                    count += 1
                continue
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        if "@value" in item or (
                            "@id" in item and set(item.keys()) <= {"@id"}
                        ):
                            count += 1
                        else:
                            count += 1 + CASEGraph._count_triples(item)
                    else:
                        count += 1
            elif isinstance(value, dict):
                if "@value" in value:
                    count += 1
                elif "@id" in value and set(value.keys()) <= {"@id"}:
                    count += 1
                else:
                    count += 1 + CASEGraph._count_triples(value)
            else:
                count += 1
        return count

    def split(self, max_objects: int = 10000) -> list[CASEGraph]:
        """Split this graph into smaller chunks of at most max_objects each.

        .. warning::
            Object-count splitting is only safe for independent catalog-style
            graphs. For investigation graphs prefer a natural boundary
            partition (see :meth:`partition_by`) rather than arbitrary chunks.
        """
        if not isinstance(max_objects, int) or max_objects <= 0:
            raise InvalidSplitSizeError(max_objects)
        warnings.warn(
            "CASEGraph.split() partitions by object count and can break "
            "investigative relationships; prefer partition_by() / "
            "partition_by_label() for CASE graphs (experimental).",
            UserWarning,
            stacklevel=2,
        )
        chunks: list[CASEGraph] = []
        for i in range(0, len(self._objects), max_objects):
            chunk = CASEGraph(kb_prefix=self.kb_prefix)
            chunk._context = dict(self._context)
            for obj in self._objects[i : i + max_objects]:
                chunk._append_object(copy.deepcopy(obj))
            chunks.append(chunk)
        return chunks

    def partition_by(
        self,
        boundary_key: Callable[[dict[str, Any]], str | None],
        *,
        shared_ids: set[str] | None = None,
        include_dangling_relationships: bool = True,
    ) -> dict[str, CASEGraph]:
        """Partition by a caller-supplied label (experimental).

        .. warning::
            **Experimental / not dependency-aware.** This method groups nodes
            by ``boundary_key`` and heuristically copies cross-partition
            ``uco-core:Relationship`` endpoints. It does **not** compute a
            full dependency closure over arbitrary predicates, blank nodes,
            or nested references. Prefer natural forensic boundaries
            (per-volume, per-app, per-device) and validate partition completeness
            yourself. Alias: :meth:`partition_by_label`.

        ``boundary_key`` maps each top-level node to a partition name (or
        ``None`` to leave it unassigned until referenced). Shared nodes listed
        in ``shared_ids`` are copied into every partition that needs them.
        Relationships whose source and target fall in different partitions are
        either duplicated into both (default) or dropped.
        """
        shared_ids = shared_ids or set()
        partitions: dict[str, CASEGraph] = {}
        membership: dict[str, str] = {}

        for obj in self._objects:
            oid = obj.get("@id")
            if not oid:
                continue
            key = boundary_key(obj)
            if key is None:
                continue
            membership[oid] = key
            if key not in partitions:
                partitions[key] = CASEGraph(
                    kb_prefix=self.kb_prefix,
                    extra_context=dict(self._context),
                )
                partitions[key].on_duplicate = "merge_compatible"
            partitions[key]._append_object(dict(obj))

        # Copy shared + cross-partition relationship endpoints (heuristic only).
        by_id = {o.get("@id"): o for o in self._objects if o.get("@id")}
        for obj in self._objects:
            types = obj.get("@type", [])
            if isinstance(types, str):
                types = [types]
            if "uco-core:Relationship" not in types:
                continue
            sources = obj.get("uco-core:source") or []
            targets = obj.get("uco-core:target") or []
            if not sources or not targets:
                continue
            sid = sources[0]["@id"] if isinstance(sources[0], dict) else sources[0]
            tid = targets[0]["@id"] if isinstance(targets[0], dict) else targets[0]
            s_part = membership.get(sid)
            t_part = membership.get(tid)
            if s_part and t_part and s_part == t_part:
                continue
            if not include_dangling_relationships and s_part != t_part:
                continue
            for part_name in {s_part, t_part} - {None}:
                pg = partitions.setdefault(
                    part_name,  # type: ignore[arg-type]
                    CASEGraph(
                        kb_prefix=self.kb_prefix, extra_context=dict(self._context)
                    ),
                )
                pg.on_duplicate = "merge_compatible"
                for nid in (sid, tid, obj.get("@id")):
                    if nid and nid in by_id:
                        try:
                            pg._ingest_raw_node(
                                dict(by_id[nid]), policy="merge_compatible"
                            )
                        except DuplicateNodeError:
                            # Already present under merge_compatible; keep existing node.
                            pass

        for sid in shared_ids:
            node = by_id.get(sid)
            if not node:
                continue
            for pg in partitions.values():
                try:
                    pg._ingest_raw_node(dict(node), policy="merge_compatible")
                except DuplicateNodeError:
                    # Shared nodes may already be copied via cross-partition edges.
                    pass

        return partitions

    def partition_by_label(
        self,
        boundary_key: Callable[[dict[str, Any]], str | None],
        *,
        shared_ids: set[str] | None = None,
        include_dangling_relationships: bool = True,
    ) -> dict[str, CASEGraph]:
        """Alias for :meth:`partition_by` (experimental label partitioning)."""
        return self.partition_by(
            boundary_key,
            shared_ids=shared_ids,
            include_dangling_relationships=include_dangling_relationships,
        )

    def partition(
        self,
        *,
        strategy: str = "roots",
        roots: list[str] | None = None,
        shared_node_policy: str = "replicate-identical",
        boundary_key: Callable[[dict[str, Any]], str | None] | None = None,
        include_incoming: bool = True,
        return_manifest: bool = False,
        boundary_policy: str = "none",
        cross_boundary_policy: str = "error-on-cross-boundary",
        root_boundaries: dict[str, dict[str, list[str]]] | None = None,
        validation_bundle: dict[str, Any] | None = None,
        manifest_detail: str = "full",
    ) -> dict[str, CASEGraph] | tuple[dict[str, CASEGraph], dict[str, Any]]:
        """Dependency-aware graph partitioning (#72).

        Strategies:
        - ``roots`` (default): BFS closure from each root IRI following nested
          ``@id`` references (outgoing) and, when ``include_incoming`` is True
          (default), reverse references from other top-level objects. Shared
          nodes are either replicated into each partition
          (``replicate-identical``) or placed in a ``_shared`` partition
          (``shared`` / ``isolate-shared``).
        - ``label``: delegate to :meth:`partition_by` with ``boundary_key``.

        Prefer this over :meth:`split` for investigation graphs.
        """
        if strategy == "label":
            if boundary_key is None:
                raise ValueError("boundary_key is required for strategy='label'")
            return self.partition_by(boundary_key)
        if strategy != "roots":
            raise ValueError(f"Unsupported partition strategy: {strategy}")
        if not roots:
            raise ValueError("roots is required for strategy='roots'")
        return self.partition_by_roots(
            roots,
            shared_node_policy=shared_node_policy,
            include_incoming=include_incoming,
            return_manifest=return_manifest,
            boundary_policy=boundary_policy,
            cross_boundary_policy=cross_boundary_policy,
            root_boundaries=root_boundaries,
            validation_bundle=validation_bundle,
            manifest_detail=manifest_detail,
        )

    def partition_by_roots(
        self,
        roots: list[str],
        *,
        shared_node_policy: str = "replicate-identical",
        include_incoming: bool = True,
        return_manifest: bool = False,
        boundary_policy: str = "none",
        cross_boundary_policy: str = "error-on-cross-boundary",
        root_boundaries: dict[str, dict[str, list[str]]] | None = None,
        validation_bundle: dict[str, Any] | None = None,
        manifest_detail: str = "full",
    ) -> dict[str, CASEGraph] | tuple[dict[str, CASEGraph], dict[str, Any]]:
        """Partition by experimental root closure (#72).

        **Experimental.** Follows nested ``{"@id": ...}`` references reachable
        from each root (outgoing). When ``include_incoming`` is True (default),
        also follows reverse references: top-level objects that nest a
        ``{"@id": root}`` (or any already-seen node) are pulled into the
        closure. This includes Relationships pointing *to* a root.

        ``boundary_policy="marking-and-authorization"`` compares each node's
        ``uco-core:objectMarking`` and relevant/required authorization IRIs
        against the root's declared boundary. The default cross-boundary policy
        fails closed; ``home-partition-reference`` omits protected content from
        unauthorized partitions while recording safe routing evidence.

        Shared policies are ``replicate-identical``, ``support-graph`` (aliases
        ``shared`` / ``isolate-shared``), ``home-partition-reference``, and
        ``error-on-cross-boundary``. When ``return_manifest`` is True, returns
        ``(partitions, manifest)`` with schema_version ``2.0.0``.
        """
        supported_shared = {
            "replicate-identical",
            "shared",
            "isolate-shared",
            "support-graph",
            "home-partition-reference",
            "error-on-cross-boundary",
        }
        if shared_node_policy not in supported_shared:
            raise ValueError(f"Unsupported shared_node_policy: {shared_node_policy}")
        if boundary_policy not in {"none", "marking-and-authorization"}:
            raise ValueError(f"Unsupported boundary_policy: {boundary_policy}")
        if cross_boundary_policy not in {
            "error-on-cross-boundary",
            "home-partition-reference",
        }:
            raise ValueError(
                f"Unsupported cross_boundary_policy: {cross_boundary_policy}"
            )
        if manifest_detail not in {"full", "safe"}:
            raise ValueError("manifest_detail must be 'full' or 'safe'")
        by_id: dict[str, dict[str, Any]] = {}
        for obj in self._objects:
            oid = obj.get("@id")
            if isinstance(oid, str):
                by_id[oid] = obj
        if not by_id:
            empty: dict[str, CASEGraph] = {}
            if return_manifest:
                return empty, self._empty_partition_manifest(
                    roots,
                    shared_node_policy,
                    include_incoming,
                    boundary_policy,
                    cross_boundary_policy,
                    validation_bundle,
                )
            return empty

        def collect_refs(node: Any, out: set[str]) -> None:
            if isinstance(node, dict):
                nid = node.get("@id")
                if isinstance(nid, str) and len(node) == 1:
                    out.add(nid)
                for value in node.values():
                    collect_refs(value, out)
            elif isinstance(node, list):
                for item in node:
                    collect_refs(item, out)

        # Reverse index: target_id → top-level object ids that reference it.
        incoming: dict[str, set[str]] = {}
        outgoing: dict[str, set[str]] = {}
        for oid, obj in by_id.items():
            refs: set[str] = set()
            collect_refs(obj, refs)
            outgoing[oid] = refs
            for ref in refs:
                incoming.setdefault(ref, set()).add(oid)

        closures: dict[str, set[str]] = {}
        for root in roots:
            if root not in by_id:
                continue
            seen: set[str] = set()
            queue = [root]
            while queue:
                current = queue.pop(0)
                if current in seen or current not in by_id:
                    continue
                seen.add(current)
                for ref in outgoing.get(current, ()):
                    if ref not in seen:
                        queue.append(ref)
                if include_incoming:
                    for referrer in incoming.get(current, ()):
                        if referrer not in seen:
                            queue.append(referrer)
            closures[root] = seen

        boundary_omissions: dict[str, set[str]] = {root: set() for root in closures}
        node_boundaries = {
            node_id: self._partition_node_boundary(node)
            for node_id, node in by_id.items()
        }
        declared_boundaries: dict[str, dict[str, set[str]]] = {}
        if boundary_policy == "marking-and-authorization":
            for root in closures:
                supplied = (root_boundaries or {}).get(root)
                if supplied is None:
                    declared_boundaries[root] = {
                        "markings": set(node_boundaries[root]["markings"]),
                        "authorizations": set(node_boundaries[root]["authorizations"]),
                    }
                else:
                    declared_boundaries[root] = {
                        "markings": {
                            self.expand_iri(value)
                            for value in supplied.get("markings", [])
                        },
                        "authorizations": {
                            self.expand_iri(value)
                            for value in supplied.get("authorizations", [])
                        },
                    }

            for root, members in closures.items():
                allowed = declared_boundaries[root]
                for node_id in list(members):
                    required = node_boundaries[node_id]
                    missing_markings = sorted(
                        required["markings"] - allowed["markings"]
                    )
                    missing_authorizations = sorted(
                        required["authorizations"] - allowed["authorizations"]
                    )
                    if not missing_markings and not missing_authorizations:
                        continue
                    if (
                        node_id == root
                        or cross_boundary_policy == "error-on-cross-boundary"
                    ):
                        raise PartitionBoundaryError(
                            root,
                            node_id,
                            missing_markings,
                            missing_authorizations,
                        )
                    members.remove(node_id)
                    boundary_omissions[root].add(node_id)

        boundary_home_by_node: dict[str, str] = {}
        if any(boundary_omissions.values()):
            for omitted_id in sorted(set().union(*boundary_omissions.values())):
                candidates = sorted(
                    root for root, members in closures.items() if omitted_id in members
                )
                if not candidates:
                    required = node_boundaries[omitted_id]
                    raise PartitionBoundaryError(
                        "<no-authorized-home>",
                        omitted_id,
                        sorted(required["markings"]),
                        sorted(required["authorizations"]),
                    )
                boundary_home_by_node[omitted_id] = candidates[0]

        membership_count: dict[str, int] = {}
        for members in closures.values():
            for nid in members:
                membership_count[nid] = membership_count.get(nid, 0) + 1

        partitions: dict[str, CASEGraph] = {}
        requested_shared_policy = shared_node_policy
        shared_policy = shared_node_policy
        if shared_policy in {"shared", "isolate-shared"}:
            shared_policy = "support-graph"
        if shared_policy == "error-on-cross-boundary":
            overlap = sorted(
                nid for nid, count in membership_count.items() if count > 1
            )
            if overlap:
                raise ValueError(
                    "shared nodes cross partition boundaries under "
                    f"error-on-cross-boundary: {overlap[:5]}"
                )

        home_by_node: dict[str, str] = {}
        if shared_policy == "home-partition-reference":
            for node_id, count in membership_count.items():
                if count > 1:
                    owners = sorted(
                        root for root, members in closures.items() if node_id in members
                    )
                    if node_id in owners:
                        home_by_node[node_id] = node_id
                    else:
                        home_by_node[node_id] = owners[0]
        for root, members in closures.items():
            pg = CASEGraph(kb_prefix=self.kb_prefix, extra_context=dict(self._context))
            pg.on_duplicate = "merge_compatible"
            for nid in members:
                if membership_count.get(nid, 0) > 1:
                    if shared_policy == "support-graph":
                        continue
                    if (
                        shared_policy == "home-partition-reference"
                        and home_by_node.get(nid) != root
                    ):
                        continue
                try:
                    pg._ingest_raw_node(dict(by_id[nid]), policy="merge_compatible")
                except DuplicateNodeError:
                    # Already present under merge_compatible; ignore.
                    pass
            partitions[root] = pg

        if shared_policy == "support-graph":
            shared = CASEGraph(
                kb_prefix=self.kb_prefix, extra_context=dict(self._context)
            )
            shared.on_duplicate = "merge_compatible"
            for nid, count in membership_count.items():
                if count > 1:
                    try:
                        shared._ingest_raw_node(
                            dict(by_id[nid]), policy="merge_compatible"
                        )
                    except DuplicateNodeError:
                        # Already present under merge_compatible; ignore.
                        pass
            if len(shared) > 0:
                # Preserve the pre-1.24 key for callers using the legacy
                # aliases while giving the explicit policy its clearer name.
                support_key = (
                    "_support"
                    if requested_shared_policy == "support-graph"
                    else "_shared"
                )
                partitions[support_key] = shared

        if not return_manifest:
            return partitions

        replicated = sorted(
            nid
            for nid, count in membership_count.items()
            if count > 1 and shared_policy == "replicate-identical"
        )
        cross_rels = self._cross_partition_relationship_ids(by_id, closures)
        source_fingerprint = self._graph_fingerprint(self._objects)
        referenced_mode = shared_policy in {
            "support-graph",
            "home-partition-reference",
        } or any(boundary_omissions.values())
        manifest: dict[str, Any] = {
            "schema_version": "2.0.0",
            "dataset_id": f"urn:sha256:{source_fingerprint}",
            "source_graph_sha256": source_fingerprint,
            "strategy": (
                "outgoing_and_incoming_id_closure"
                if include_incoming
                else "outgoing_id_closure"
            ),
            "roots": list(roots),
            "shared_node_policy": shared_policy,
            "include_incoming": include_incoming,
            "boundary_policy": boundary_policy,
            "cross_boundary_policy": cross_boundary_policy,
            "validation_mode": (
                "referenced-partition-set" if referenced_mode else "self-contained"
            ),
            "validation_bundle": copy.deepcopy(validation_bundle),
            "partitions": {
                partition_key: {
                    "partition_id": f"urn:sha256:{self._graph_fingerprint(partition._objects)}",
                    "node_count": len(partition),
                    "triple_estimate": partition.estimate_triples(),
                    "sha256": self._graph_fingerprint(partition._objects),
                    "effective_markings": sorted(
                        declared_boundaries.get(partition_key, {}).get(
                            "markings", set()
                        )
                    ),
                    "authorization_scope": sorted(
                        declared_boundaries.get(partition_key, {}).get(
                            "authorizations", set()
                        )
                    ),
                    **(
                        {
                            "node_ids": sorted(
                                node.get("@id")
                                for node in partition._objects
                                if isinstance(node.get("@id"), str)
                            )
                        }
                        if manifest_detail == "full"
                        else {}
                    ),
                }
                for partition_key, partition in partitions.items()
            },
            "replicated_node_ids": replicated,
            "cross_partition_relationship_ids": cross_rels,
            "home_partition_routes": (
                dict(sorted({**home_by_node, **boundary_home_by_node}.items()))
                if manifest_detail == "full"
                else {}
            ),
            "home_partition_route_count": len(
                {**home_by_node, **boundary_home_by_node}
            ),
            "boundary_omission_counts": {
                root: len(ids) for root, ids in boundary_omissions.items()
            },
            "reconstruction": {
                "operation": "rdf-union",
                "deduplicate_by": "@id with identical assertions",
                "requires_partitions": sorted(partitions),
            },
        }
        return partitions, manifest

    def _partition_node_boundary(self, node: dict[str, Any]) -> dict[str, set[str]]:
        markings: set[str] = set()
        authorizations: set[str] = set()

        def ids(value: Any) -> list[str]:
            found: list[str] = []
            if isinstance(value, dict):
                node_id = value.get("@id")
                if isinstance(node_id, str):
                    found.append(self.expand_iri(node_id))
            elif isinstance(value, list):
                for item in value:
                    found.extend(ids(item))
            elif isinstance(value, str):
                found.append(self.expand_iri(value))
            return found

        for key, value in node.items():
            expanded_key = self.expand_iri(key)
            local = expanded_key.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
            if local == "objectMarking":
                markings.update(ids(value))
            elif local in {"relevantAuthorization", "requiredAuthorization"}:
                authorizations.update(ids(value))
        return {"markings": markings, "authorizations": authorizations}

    def _graph_fingerprint(self, objects: list[dict[str, Any]]) -> str:
        payload = json.dumps(
            {"@context": dict(sorted(self._context.items())), "@graph": objects},
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def verify_partition_union(
        self, partitions: dict[str, CASEGraph]
    ) -> dict[str, Any]:
        """Prove reconstructed partition RDF is isomorphic to the source (#79)."""

        from rdflib import Graph
        from rdflib.compare import to_isomorphic

        source = Graph()
        source.parse(data=self.serialize(indent=None), format="json-ld")
        union = Graph()
        for partition in partitions.values():
            union.parse(data=partition.serialize(indent=None), format="json-ld")
        equivalent = to_isomorphic(source) == to_isomorphic(union)
        return {
            "equivalent": equivalent,
            "source_triples": len(source),
            "union_triples": len(union),
        }

    def _empty_partition_manifest(
        self,
        roots: list[str],
        shared_node_policy: str,
        include_incoming: bool,
        boundary_policy: str,
        cross_boundary_policy: str,
        validation_bundle: dict[str, Any] | None,
    ) -> dict[str, Any]:
        source_fingerprint = self._graph_fingerprint([])
        return {
            "schema_version": "2.0.0",
            "dataset_id": f"urn:sha256:{source_fingerprint}",
            "source_graph_sha256": source_fingerprint,
            "strategy": (
                "outgoing_and_incoming_id_closure"
                if include_incoming
                else "outgoing_id_closure"
            ),
            "roots": list(roots),
            "shared_node_policy": shared_node_policy,
            "include_incoming": include_incoming,
            "boundary_policy": boundary_policy,
            "cross_boundary_policy": cross_boundary_policy,
            "validation_mode": "self-contained",
            "validation_bundle": copy.deepcopy(validation_bundle),
            "partitions": {},
            "replicated_node_ids": [],
            "cross_partition_relationship_ids": [],
            "home_partition_routes": {},
            "home_partition_route_count": 0,
            "boundary_omission_counts": {},
            "reconstruction": {
                "operation": "rdf-union",
                "deduplicate_by": "@id with identical assertions",
                "requires_partitions": [],
            },
        }

    @staticmethod
    def _is_relationship_node(obj: dict[str, Any]) -> bool:
        types = obj.get("@type")
        if isinstance(types, str):
            types = [types]
        if not isinstance(types, list):
            return False
        return any(
            t
            in (
                "uco-core:Relationship",
                "https://ontology.unifiedcyberontology.org/uco/core/Relationship",
            )
            for t in types
            if isinstance(t, str)
        )

    @staticmethod
    def _first_endpoint_id(obj: dict[str, Any], key: str) -> str | None:
        val = obj.get(key)
        if isinstance(val, dict):
            nid = val.get("@id")
            if isinstance(nid, str):
                return nid
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    nid = item.get("@id")
                    if isinstance(nid, str):
                        return nid
        return None

    def _cross_partition_relationship_ids(
        self,
        by_id: dict[str, dict[str, Any]],
        closures: dict[str, set[str]],
    ) -> list[str]:
        """Relationship @ids whose source/target fall in different root closures."""
        node_roots: dict[str, set[str]] = {}
        for root, members in closures.items():
            for nid in members:
                node_roots.setdefault(nid, set()).add(root)

        cross: list[str] = []
        for nid, obj in by_id.items():
            if not self._is_relationship_node(obj):
                continue
            source = self._first_endpoint_id(obj, "uco-core:source")
            target = self._first_endpoint_id(obj, "uco-core:target")
            if source is None or target is None:
                continue
            src_roots = node_roots.get(source, set())
            tgt_roots = node_roots.get(target, set())
            if not src_roots or not tgt_roots:
                continue
            if src_roots.isdisjoint(tgt_roots):
                cross.append(nid)
        return sorted(cross)

    @classmethod
    def merge_files(
        cls, paths: list[str], kb_prefix: str = "http://example.org/kb/"
    ) -> CASEGraph:
        """Load and merge multiple JSON-LD graph files into a single graph.

        Contexts are merged (later files override earlier ones for
        conflicting prefixes). All objects are concatenated.
        """
        merged = cls(kb_prefix=kb_prefix)
        for path in paths:
            merged.load_file(path)
        return merged

    def _mint_id(self, instance: Any) -> str:
        """Generate a UUID-based @id for an instance."""
        cls_name = type(instance).__name__
        # Convert PascalCase to kebab-case for the IRI local name
        prefix = self._get_prefix(instance)
        return f"{prefix}:{cls_name}-{uuid.uuid4()}"

    def _mint_relationship_id(self, source_id: str, predicate: str) -> str:
        local = predicate.split(":", 1)[-1] if ":" in predicate else predicate
        return f"{source_id}/{local}-{uuid.uuid4()}"

    def _deterministic_relationship_id(
        self, source_id: str, target_id: str, kind: str
    ) -> str:
        digest = hashlib.sha256(
            f"{self.expand_iri(source_id)}|{self.expand_iri(target_id)}|{kind}".encode()
        ).hexdigest()[:12]
        safe_kind = _safe_kind_slug(kind)
        return f"kb:rel-{safe_kind}-{digest}"

    def _snapshot_state(self) -> dict[str, Any]:
        return {
            "context": dict(self._context),
            "objects": copy.deepcopy(self._objects),
            "iri_index": dict(self._iri_index),
            "iri_aliases": dict(self._iri_aliases),
            "used_prefix_set": set(self._used_prefix_set),
        }

    def _restore_state(self, snapshot: dict[str, Any]) -> None:
        self._context = snapshot["context"]
        self._objects = snapshot["objects"]
        self._iri_index = snapshot["iri_index"]
        self._iri_aliases = snapshot["iri_aliases"]
        self._used_prefix_set = snapshot["used_prefix_set"]

    def _append_object(self, obj: dict[str, Any]) -> None:
        node_id = obj.get("@id")
        if node_id and self._find_object(node_id) is not None:
            raise DuplicateNodeError(
                node_id,
                "use add_type/upsert_node/merge_compatible instead of appending a second node",
            )
        self._objects.append(obj)
        if node_id:
            self._index_node(node_id, len(self._objects) - 1)
        self._track_prefixes_for(obj)

    def _index_node(self, node_id: str, index: int) -> None:
        expanded = self.expand_iri(node_id)
        self._iri_index[expanded] = index
        self._iri_aliases[node_id] = expanded
        if expanded != node_id:
            self._iri_aliases[expanded] = expanded

    def _find_object(self, node_id: str) -> dict[str, Any] | None:
        expanded = self.expand_iri(node_id)
        idx = self._iri_index.get(expanded)
        if idx is None:
            return None
        if idx >= len(self._objects):
            return None
        return self._objects[idx]

    def _require_object(self, node_id: str) -> dict[str, Any]:
        obj = self._find_object(node_id)
        if obj is None:
            raise KeyError(f"No node with @id {node_id!r}")
        return obj

    def _merge_context(self, incoming: dict[str, Any]) -> None:
        for prefix, ns in incoming.items():
            if not isinstance(ns, str):
                continue
            existing = self._context.get(prefix)
            if existing is not None and existing != ns:
                raise ValueError(
                    f"Context prefix collision for {prefix!r}: "
                    f"existing {existing!r} vs incoming {ns!r}"
                )
            self._context[prefix] = ns

    @staticmethod
    def _normalize_duplicate_policy(policy: str) -> str:
        if policy == "error":
            policy = "reject"
        if policy not in ("reject", "merge_identical", "merge_compatible", "replace"):
            raise ValueError(
                f"Unknown duplicate policy: {policy!r}. "
                f"Expected one of: reject, merge_identical, merge_compatible, replace "
                f"(error is an alias for reject)"
            )
        return policy

    def _ingest_raw_node(self, raw: dict[str, Any], *, policy: str) -> None:
        policy = self._normalize_duplicate_policy(policy)
        node_id = raw.get("@id")
        if not node_id:
            self._objects.append(raw)
            self._track_prefixes_for(raw)
            return
        existing = self._find_object(node_id)
        if existing is None:
            self._append_object(raw)
            return
        if policy == "reject":
            raise DuplicateNodeError(node_id, "conflicting duplicate during load")
        if policy == "replace":
            preserved_id = existing.get("@id", node_id)
            existing.clear()
            existing.update(raw)
            existing["@id"] = preserved_id
            self._track_prefixes_for(existing)
            return
        if policy == "merge_identical":
            self._merge_identical_node(existing, raw, node_id)
            self._track_prefixes_for(raw)
            return
        if policy == "merge_compatible":
            if "@type" in raw:
                existing["@type"] = self._normalize_type_value(
                    self._merge_types(existing.get("@type"), raw["@type"])
                )
            for key, value in raw.items():
                if key in ("@id", "@type"):
                    continue
                self._apply_property(
                    existing, key, value, node_id=node_id, mode="merge_compatible"
                )
            self._track_prefixes_for(raw)
            return
        raise ValueError(f"Unknown duplicate policy: {policy!r}")

    def _merge_identical_node(
        self, existing: dict[str, Any], raw: dict[str, Any], node_id: str
    ) -> None:
        for key, value in raw.items():
            if key == "@id":
                continue
            if key not in existing:
                existing[key] = copy.deepcopy(value)
                continue
            if not _jsonld_values_equal(existing[key], value):
                raise DuplicateNodeError(
                    node_id,
                    f"merge_identical conflict on {key!r}: "
                    f"existing={existing[key]!r} incoming={value!r}",
                )

    def _apply_property(
        self,
        obj: dict[str, Any],
        key: str,
        value: Any,
        *,
        node_id: str,
        mode: str,
    ) -> None:
        """Shared conflict engine for load / upsert / add_property / set_property."""
        if mode == "replace":
            obj[key] = copy.deepcopy(value)
            return
        if mode != "merge_compatible":
            raise ValueError(f"Unknown property merge mode: {mode!r}")
        if key not in obj:
            obj[key] = copy.deepcopy(value)
            return
        existing = obj[key]
        if _jsonld_values_equal(existing, value):
            return
        # List-like accumulation when at least one side is already multi-valued.
        if isinstance(existing, list):
            self._accumulate_list_value(existing, value)
            return
        if isinstance(value, list):
            merged = [copy.deepcopy(existing)]
            self._accumulate_list_value(merged, value)
            obj[key] = merged
            return
        # Distinct JSON-LD node references (@id objects) are multi-valued
        # assertions, not scalar conflicts (e.g. two prov:wasDerivedFrom edges).
        if (
            isinstance(existing, dict)
            and isinstance(value, dict)
            and "@id" in existing
            and "@id" in value
        ):
            if _jsonld_values_equal(existing, value):
                return
            obj[key] = [copy.deepcopy(existing), copy.deepcopy(value)]
            return
        # Conflicting plain scalars / typed literals remain an error; use
        # set_property(..., mode="replace") for explicit replacement.
        raise DuplicateNodeError(
            node_id,
            f"merge_compatible scalar conflict on {key!r}: "
            f"existing={existing!r} incoming={value!r}",
        )

    @staticmethod
    def _accumulate_list_value(existing: list[Any], value: Any) -> None:
        items = value if isinstance(value, list) else [value]
        for item in items:
            if any(_jsonld_values_equal(x, item) for x in existing):
                continue
            existing.append(copy.deepcopy(item))

    def _track_prefixes_for(self, node: Any) -> None:
        self._collect_prefixes(node, set(self._context.keys()), self._used_prefix_set)

    @staticmethod
    def _as_type_list(types: list[str] | str | None) -> list[str]:
        if types is None:
            return []
        if isinstance(types, str):
            return [types]
        return list(types)

    @staticmethod
    def _normalize_type_value(types: list[str] | str) -> list[str] | str:
        type_list = CASEGraph._as_type_list(types)
        if len(type_list) == 1:
            return type_list[0]
        return type_list

    def _merge_types(
        self,
        existing: list[str] | str | None,
        new_types: list[str] | str,
    ) -> list[str]:
        merged = self._as_type_list(existing)
        for type_iri in self._as_type_list(new_types):
            if type_iri not in merged:
                merged.append(type_iri)
        return merged

    def _get_prefix(self, instance: Any) -> str:
        """Get the namespace prefix for an instance (defaults to kb)."""
        return "kb"

    def _to_jsonld(self, instance: Any, obj_id: str) -> dict[str, Any]:
        """Convert a dataclass instance to a JSON-LD dictionary."""
        result: dict[str, Any] = {"@id": obj_id}

        cls = type(instance)
        if hasattr(cls, "CLASS_IRI"):
            # Convert full IRI to prefixed form
            class_iri = cls.CLASS_IRI
            result["@type"] = self._compact_iri(class_iri)

        if not is_dataclass(instance):
            return result

        for f in _cached_dataclass_fields(type(instance)):
            if f.name in ("CLASS_IRI", "NAMESPACE_PREFIX"):
                continue

            value = getattr(instance, f.name)
            if value is None:
                continue
            if isinstance(value, list) and len(value) == 0:
                continue

            prop_key = self._property_key(instance, f)
            range_iri = f.metadata.get("range_iri")

            if isinstance(value, list):
                result[prop_key] = [
                    self._convert_value(v, range_iri=range_iri) for v in value
                ]
            else:
                result[prop_key] = self._convert_value(value, range_iri=range_iri)

        return result

    def _property_key(self, instance: Any, field_info: Field[Any]) -> str:
        """Resolve the JSON-LD property key from generated field metadata when available."""
        metadata_key: str | None = field_info.metadata.get("jsonld_key")
        if metadata_key:
            return metadata_key

        parts = field_info.name.split("_")
        camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
        ns_prefix = getattr(type(instance), "NAMESPACE_PREFIX", "uco-core")
        return f"{ns_prefix}:{camel}"

    def _convert_value(self, value: Any, range_iri: str | None = None) -> Any:
        """Convert a Python value to JSON-LD representation."""
        if isinstance(value, TypedLiteral):
            datatype = value.datatype_iri
            compact = self._compact_iri(datatype)
            return {"@type": compact, "@value": str(value.value)}

        if is_dataclass(value) and not isinstance(value, type):
            # Nested object — create inline or reference
            self._validate_instance(value)
            if _builtin_id(value) in self._id_map:
                return {"@id": self._id_map[_builtin_id(value)]}
            # Inline as a facet-like sub-object
            inline_id = self._mint_id(value)
            return self._to_jsonld(value, inline_id)

        if range_iri in _RANGE_IRI_TO_TYPED_LITERAL:
            return self._typed_literal(_RANGE_IRI_TO_TYPED_LITERAL[range_iri], value)

        if (
            isinstance(value, str)
            and range_iri
            and range_iri in _CUSTOM_RDF_DATATYPE_IRIS
        ):
            return {
                "@type": self._compact_iri(range_iri),
                "@value": value,
            }

        if isinstance(value, datetime):
            return self._typed_literal("xsd:dateTime", value)
        if isinstance(value, date):
            return self._typed_literal(
                "xsd:dateTime", datetime.combine(value, datetime.min.time())
            )
        if isinstance(value, bool):
            return self._typed_literal("xsd:boolean", value)
        if isinstance(value, int):
            return self._typed_literal("xsd:integer", value)
        if isinstance(value, float):
            return self._typed_literal("xsd:decimal", value)

        return value

    def _typed_literal(self, xsd_type: str, value: Any) -> dict[str, str]:
        if isinstance(value, bool):
            rendered = str(value).lower()
        elif isinstance(value, datetime):
            rendered = value.isoformat()
        else:
            rendered = str(value)
        return {"@type": xsd_type, "@value": rendered}

    def _validate_instance(self, instance: Any) -> None:
        """Validate required generated fields before adding/serializing an instance."""
        if not is_dataclass(instance):
            return

        for field_info in _cached_dataclass_fields(type(instance)):
            if field_info.name in ("CLASS_IRI", "NAMESPACE_PREFIX"):
                continue

            metadata: dict[str, Any] = (
                dict(field_info.metadata) if field_info.metadata else {}
            )
            if not metadata:
                continue

            value = getattr(instance, field_info.name)
            required = bool(metadata.get("required", False))
            cardinality = metadata.get("cardinality")

            if required:
                if value is None:
                    raise ValueError(
                        f"{type(instance).__name__}.{field_info.name} is required but was not provided."
                    )
                if isinstance(value, list) and len(value) == 0:
                    raise ValueError(
                        f"{type(instance).__name__}.{field_info.name} requires at least one value."
                    )

            if cardinality in {"exactly_one", "zero_or_one"} and isinstance(
                value, list
            ):
                raise ValueError(
                    f"{type(instance).__name__}.{field_info.name} does not accept multiple values."
                )

            if isinstance(value, list):
                for item in value:
                    if is_dataclass(item):
                        self._validate_instance(item)
            elif is_dataclass(value):
                self._validate_instance(value)

    @classmethod
    def from_jsonld(
        cls,
        json_str: str,
        *,
        extra_classes: list[type] | None = None,
        kb_prefix: str = "http://example.org/kb/",
        on_duplicate: str | None = None,
    ) -> tuple[CASEGraph, list[Any]]:
        """Deserialize a JSON-LD string into typed Python objects.

        Returns a tuple of (CASEGraph, list_of_typed_objects). Each object in
        the ``@graph`` array is matched to a generated Python class by its
        ``@type`` IRI(s).  Objects whose type cannot be resolved (or whose
        multi-type set is ambiguous) are returned as plain dicts and still
        added to the graph via the IRI index.

        Duplicate ``@id`` handling defaults to ``reject`` (same as
        :meth:`load` / other languages).

        Args:
            json_str: A JSON-LD string containing ``@context`` and ``@graph``.
            extra_classes: Additional classes (e.g. extension dataclasses)
                to include in the type registry alongside the built-in ones.
            kb_prefix: Knowledge-base prefix for the returned graph.
            on_duplicate: Duplicate policy (default ``reject``).
        """
        iri_to_class = _build_class_registry(extra_classes)

        doc = json.loads(json_str)
        context = doc.get("@context", {})
        graph_items = doc.get("@graph", [])

        graph = cls(kb_prefix=kb_prefix)
        if isinstance(context, dict):
            graph._merge_context(context)

        policy = graph._normalize_duplicate_policy(on_duplicate or graph.on_duplicate)
        ctx = context if isinstance(context, dict) else {}

        typed_objects: list[Any] = []
        for raw in graph_items:
            if not isinstance(raw, dict):
                continue
            node = dict(raw)
            if isinstance(node.get("@type"), list):
                node["@type"] = list(node["@type"])
            graph._ingest_raw_node(node, policy=policy)
            # Rehydrate from the indexed node so multi-type @type is preserved.
            source = node
            node_id = node.get("@id")
            if node_id:
                stored = graph._find_object(node_id)
                if stored is not None:
                    source = stored
            obj, warn = _rehydrate_with_diagnostics(source, iri_to_class, ctx)
            if warn is not None:
                graph.deserialization_warnings.append(warn)
                warnings.warn(
                    f"Deserialization fallback for {warn.node_id!r}: "
                    f"{warn.reason} — {warn.detail}".rstrip(" —"),
                    UserWarning,
                    stacklevel=2,
                )
            typed_objects.append(obj)

            if is_dataclass(obj) and not isinstance(obj, type):
                obj_id = source.get("@id", graph._mint_id(obj))
                graph._id_map[_builtin_id(obj)] = obj_id

        return graph, typed_objects

    def _pruned_context(self) -> dict[str, str]:
        """Return a copy of the context containing only prefixes used in the graph."""
        used = self._used_prefix_set or self._used_prefixes()
        if not used:
            used = self._used_prefixes()
        return {k: v for k, v in self._context.items() if k in used}

    def _used_prefixes(self) -> set[str]:
        """Collect all namespace prefixes referenced in the graph objects."""
        prefixes: set[str] = set()
        context_keys = set(self._context.keys())
        for obj in self._objects:
            self._collect_prefixes(obj, context_keys, prefixes)
        return prefixes

    @staticmethod
    def _extract_prefix(value: str, context_keys: set[str]) -> str | None:
        if "://" in value:
            return None
        colon = value.find(":")
        if colon > 0:
            prefix = value[:colon]
            if prefix in context_keys:
                return prefix
        return None

    @staticmethod
    def _collect_prefixes(node: Any, context_keys: set[str], out: set[str]) -> None:
        if isinstance(node, dict):
            for key, val in node.items():
                p = CASEGraph._extract_prefix(key, context_keys)
                if p:
                    out.add(p)
                if isinstance(val, str):
                    p = CASEGraph._extract_prefix(val, context_keys)
                    if p:
                        out.add(p)
                else:
                    CASEGraph._collect_prefixes(val, context_keys, out)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, str):
                    p = CASEGraph._extract_prefix(item, context_keys)
                    if p:
                        out.add(p)
                else:
                    CASEGraph._collect_prefixes(item, context_keys, out)

    def _compact_iri(self, iri: str) -> str:
        """Compact a full IRI to prefixed form using the context."""
        for prefix, ns in self._context.items():
            if iri.startswith(ns):
                local = iri[len(ns) :]
                return f"{prefix}:{local}"
        return iri


_CLASS_REGISTRY_CACHE: dict[str, type] | None = None
_CLASS_FIELD_CACHE: dict[type, tuple[Any, ...]] | None = None
_CLASS_REGISTRY_LOCK = threading.RLock()
_CLASS_REGISTRY_HITS = 0
_CLASS_REGISTRY_MISSES = 0
_CLASS_REGISTRY_GENERATION = 0


@dataclass(frozen=True)
class ExtensionClassRegistration:
    """One explicitly trusted dynamic deserialization registration (#82).

    Registration priority is recorded for diagnostics and future ordering, but
    never resolves a duplicate IRI. Conflicting class IRIs always fail closed.
    """

    class_iri: str
    cls: type
    source: str
    priority: int = 0
    context: tuple[tuple[str, str], ...] = ()


_REGISTERED_EXTENSION_CLASSES: dict[str, ExtensionClassRegistration] = {}


class DuplicateClassIriError(ValueError):
    """Raised when two incompatible classes claim the same CLASS_IRI (#70)."""


def _build_class_registry(extra_classes: list[type] | None = None) -> dict[str, type]:
    """Build a mapping from CLASS_IRI -> Python dataclass for all generated classes.

    The core registry is cached process-wide (#70). Extension classes from
    ``extra_classes`` are layered on a shallow copy so callers cannot mutate
    the shared cache. Construction is thread-safe.
    """
    global _CLASS_REGISTRY_CACHE, _CLASS_REGISTRY_HITS, _CLASS_REGISTRY_MISSES
    with _CLASS_REGISTRY_LOCK:
        if _CLASS_REGISTRY_CACHE is None:
            _CLASS_REGISTRY_MISSES += 1
            registry: dict[str, type] = {}
            import importlib

            module_names = [
                "case_uco.case.investigation",
                "case_uco.uco.action",
                "case_uco.uco.analysis",
                "case_uco.uco.configuration",
                "case_uco.uco.core",
                "case_uco.uco.identity",
                "case_uco.uco.location",
                "case_uco.uco.marking",
                "case_uco.uco.observable",
                "case_uco.uco.pattern",
                "case_uco.uco.role",
                "case_uco.uco.time",
                "case_uco.uco.tool",
                "case_uco.uco.types",
                "case_uco.uco.victim",
            ]

            for mod_name in module_names:
                try:
                    mod = importlib.import_module(mod_name)
                except ImportError:
                    continue
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name)
                    if (
                        isinstance(attr, type)
                        and is_dataclass(attr)
                        and hasattr(attr, "CLASS_IRI")
                    ):
                        iri = attr.CLASS_IRI
                        existing = registry.get(iri)
                        if existing is not None and existing is not attr:
                            raise DuplicateClassIriError(
                                f"CLASS_IRI {iri!r} claimed by both "
                                f"{existing.__module__}.{existing.__name__} and "
                                f"{attr.__module__}.{attr.__name__}"
                            )
                        registry[iri] = attr
            for iri, registration in _REGISTERED_EXTENSION_CLASSES.items():
                existing = registry.get(iri)
                if existing is not None and existing is not registration.cls:
                    raise DuplicateClassIriError(
                        f"registered extension CLASS_IRI {iri!r} from "
                        f"{registration.source!r} conflicts with "
                        f"{existing.__module__}.{existing.__name__}"
                    )
                registry[iri] = registration.cls
            _CLASS_REGISTRY_CACHE = registry
        else:
            _CLASS_REGISTRY_HITS += 1

        result = dict(_CLASS_REGISTRY_CACHE)
    if extra_classes:
        for cls in extra_classes:
            if hasattr(cls, "CLASS_IRI"):
                iri = cls.CLASS_IRI
                existing = result.get(iri)
                if existing is not None and existing is not cls:
                    raise DuplicateClassIriError(
                        f"extra_classes CLASS_IRI {iri!r} conflicts with "
                        f"{existing.__module__}.{existing.__name__}"
                    )
                result[iri] = cls
    return result


def _cached_dataclass_fields(cls: type) -> tuple[Any, ...]:
    """Return dataclass fields for ``cls``, cached process-wide (#70)."""
    global _CLASS_FIELD_CACHE
    with _CLASS_REGISTRY_LOCK:
        if _CLASS_FIELD_CACHE is None:
            _CLASS_FIELD_CACHE = {}
        cached = _CLASS_FIELD_CACHE.get(cls)
        if cached is not None:
            return cached
        field_tuple: tuple[Any, ...] = tuple(dataclasses.fields(cls))
        _CLASS_FIELD_CACHE[cls] = field_tuple
        return field_tuple


def clear_class_registry_cache() -> None:
    """Invalidate caches while preserving explicit extension registrations."""
    global _CLASS_REGISTRY_CACHE, _CLASS_FIELD_CACHE, _CLASS_REGISTRY_GENERATION
    with _CLASS_REGISTRY_LOCK:
        _CLASS_REGISTRY_CACHE = None
        _CLASS_FIELD_CACHE = None
        _CLASS_REGISTRY_GENERATION += 1


def register_extension_classes(
    classes: list[type],
    *,
    source: str,
    priority: int = 0,
    context: dict[str, str] | None = None,
) -> int:
    """Register trusted extension dataclasses and invalidate typed caches (#82).

    The call is atomic: every class is validated before any registration is
    installed. Duplicate IRIs never use priority as an override; an actionable
    :class:`DuplicateClassIriError` is raised instead. Returns the new cache
    generation, or the current generation for an idempotent registration.
    """

    global _CLASS_REGISTRY_CACHE, _CLASS_FIELD_CACHE, _CLASS_REGISTRY_GENERATION
    clean_source = source.strip()
    if not clean_source:
        raise ValueError("extension registration source must be non-empty")
    normalized_context = tuple(sorted((context or {}).items()))
    candidates: list[ExtensionClassRegistration] = []
    seen: dict[str, type] = {}
    for cls in classes:
        iri = getattr(cls, "CLASS_IRI", None)
        if not isinstance(cls, type) or not is_dataclass(cls):
            raise TypeError("extension registrations must be dataclass types")
        if not isinstance(iri, str) or not iri.strip():
            raise ValueError(
                f"extension class {cls.__module__}.{cls.__name__} has no CLASS_IRI"
            )
        prior = seen.get(iri)
        if prior is not None and prior is not cls:
            raise DuplicateClassIriError(
                f"extension registration batch contains duplicate CLASS_IRI {iri!r}: "
                f"{prior.__module__}.{prior.__name__} vs {cls.__module__}.{cls.__name__}"
            )
        seen[iri] = cls
        candidates.append(
            ExtensionClassRegistration(
                class_iri=iri,
                cls=cls,
                source=clean_source,
                priority=priority,
                context=normalized_context,
            )
        )

    with _CLASS_REGISTRY_LOCK:
        # Build the current generation first so built-in conflicts are checked.
        current = _build_class_registry()
        changed = False
        for registration in candidates:
            existing_type = current.get(registration.class_iri)
            existing_registration = _REGISTERED_EXTENSION_CLASSES.get(
                registration.class_iri
            )
            if existing_type is not None and existing_type is not registration.cls:
                owner = (
                    existing_registration.source
                    if existing_registration is not None
                    else f"{existing_type.__module__}.{existing_type.__name__}"
                )
                raise DuplicateClassIriError(
                    f"CLASS_IRI {registration.class_iri!r} from "
                    f"{registration.source!r} conflicts with {owner!r}"
                )
            if existing_registration == registration:
                continue
            _REGISTERED_EXTENSION_CLASSES[registration.class_iri] = registration
            changed = True
        if changed:
            _CLASS_REGISTRY_CACHE = None
            _CLASS_FIELD_CACHE = None
            _CLASS_REGISTRY_GENERATION += 1
        return _CLASS_REGISTRY_GENERATION


def unregister_extension_source(source: str) -> int:
    """Remove all registrations from ``source`` and invalidate caches (#82)."""

    global _CLASS_REGISTRY_CACHE, _CLASS_FIELD_CACHE, _CLASS_REGISTRY_GENERATION
    with _CLASS_REGISTRY_LOCK:
        doomed = [
            iri
            for iri, registration in _REGISTERED_EXTENSION_CLASSES.items()
            if registration.source == source
        ]
        for iri in doomed:
            del _REGISTERED_EXTENSION_CLASSES[iri]
        if doomed:
            _CLASS_REGISTRY_CACHE = None
            _CLASS_FIELD_CACHE = None
            _CLASS_REGISTRY_GENERATION += 1
        return _CLASS_REGISTRY_GENERATION


def discover_extension_class_providers(
    group: str = "case_uco.class_registry",
) -> list[str]:
    """Explicitly load trusted Python entry-point class providers (#82).

    Provider entry points may return an iterable of dataclass types or an
    object exposing a ``classes`` iterable. Discovery is opt-in because loading
    an entry point executes package code. Each successful provider is recorded
    under its entry-point name and automatically invalidates the registry.
    """

    from importlib.metadata import entry_points

    try:
        providers = entry_points(group=group)
    except TypeError:  # Python <3.10 mapping API.
        providers = getattr(entry_points(), "get")(group, ())
    loaded: list[str] = []
    for entry_point in providers:
        provider = entry_point.load()
        supplied = (
            provider()
            if callable(provider) and not isinstance(provider, type)
            else provider
        )
        classes = getattr(supplied, "classes", supplied)
        register_extension_classes(list(classes), source=entry_point.name)
        loaded.append(entry_point.name)
    return loaded


def class_registry_cache_info() -> dict[str, int]:
    """Return stable process-wide cache observability counters (#82)."""

    with _CLASS_REGISTRY_LOCK:
        return {
            "hits": _CLASS_REGISTRY_HITS,
            "misses": _CLASS_REGISTRY_MISSES,
            "generation": _CLASS_REGISTRY_GENERATION,
            "registered_extensions": len(_REGISTERED_EXTENSION_CLASSES),
            "cached_classes": len(_CLASS_REGISTRY_CACHE or {}),
            "cached_field_classes": len(_CLASS_FIELD_CACHE or {}),
        }


def _expand_iri(compact: str, context: dict[str, str]) -> str:
    """Expand a prefixed IRI (e.g. 'uco-tool:Tool') to a full IRI."""
    if "://" in compact:
        return compact
    if ":" in compact:
        prefix, local = compact.split(":", 1)
        ns = context.get(prefix)
        if ns:
            return ns + local
    return compact


def _safe_kind_slug(kind: str, max_len: int = _KIND_SLUG_MAX_LEN) -> str:
    """Constrain relationship kind for IRI local-name safety."""
    slug = _KIND_SLUG_RE.sub("_", kind.strip()).strip("._-")
    if not slug:
        slug = "rel"
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("._-") or "rel"
    return slug


def _jsonld_values_equal(a: Any, b: Any) -> bool:
    """Semantic equality for JSON-LD values before conflict decisions.

    Normalizes ``@id`` references, typed literals (``@type``/``@value``), and
    set-like arrays of ``@id`` refs (order-insensitive). Other lists remain
    order-sensitive.
    """
    if a is b:
        return True
    if isinstance(a, dict) and isinstance(b, dict):
        if "@value" in a or "@value" in b:
            if "@value" not in a or "@value" not in b:
                return False
            return _normalize_literal_type(a.get("@type")) == _normalize_literal_type(
                b.get("@type")
            ) and _normalize_literal_value(
                a.get("@value"), a.get("@type")
            ) == _normalize_literal_value(b.get("@value"), b.get("@type"))
        if "@id" in a or "@id" in b:
            if "@id" not in a or "@id" not in b:
                return False
            return str(a["@id"]) == str(b["@id"])
        if set(a.keys()) != set(b.keys()):
            return False
        return all(_jsonld_values_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        if _is_id_ref_list(a) and _is_id_ref_list(b):
            return sorted(str(_id_of(x)) for x in a) == sorted(
                str(_id_of(x)) for x in b
            )
        if len(a) != len(b):
            return False
        return all(_jsonld_values_equal(x, y) for x, y in zip(a, b))
    return bool(a == b)


def _normalize_literal_type(type_iri: Any) -> str:
    if not isinstance(type_iri, str):
        return ""
    if type_iri.startswith("xsd:"):
        return type_iri
    if type_iri.startswith("http://www.w3.org/2001/XMLSchema#"):
        return "xsd:" + type_iri.rsplit("#", 1)[-1]
    return type_iri


def _normalize_literal_value(value: Any, type_iri: Any) -> str:
    rendered = value
    if isinstance(value, bool):
        rendered = "true" if value else "false"
    elif value is True or value is False:
        rendered = "true" if value else "false"
    elif isinstance(value, str) and value.lower() in ("true", "false"):
        t = _normalize_literal_type(type_iri)
        if "boolean" in t:
            rendered = value.lower()
    return str(rendered)


def _is_id_ref_list(items: list[Any]) -> bool:
    if not items:
        return False
    return all(isinstance(x, dict) and "@id" in x for x in items)


def _id_of(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("@id", ""))
    return str(item)


def _select_most_specific_class(classes: list[type]) -> type | None:
    """Pick the unique deepest subclass among registered matches, if any."""
    if not classes:
        return None
    if len(classes) == 1:
        return classes[0]
    # Keep classes that are not a superclass of another match.
    specific = [
        c for c in classes if not any(o is not c and issubclass(o, c) for o in classes)
    ]
    if len(specific) == 1:
        return specific[0]
    return None


def _rehydrate(
    raw: dict[str, Any],
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> Any:
    """Convert a JSON-LD dict back to a typed Python dataclass instance."""
    obj, _warn = _rehydrate_with_diagnostics(raw, iri_to_class, context)
    return obj


def _rehydrate_with_diagnostics(
    raw: dict[str, Any],
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> tuple[Any, DeserializationWarning | None]:
    """Convert a JSON-LD dict back to a typed instance, with fallback diagnostics.

    When ``@type`` is a list, every type is expanded and matched against the
    registry. The most specific unambiguous registered domain class is chosen
    (deepest subclass when determinable; sole registered match otherwise).
    If multiple incomparable registered classes match, returns the raw dict.
    All ``@type`` values remain on the graph node unchanged.
    """
    node_id = raw.get("@id") if isinstance(raw.get("@id"), str) else None
    type_value = raw.get("@type")
    if not type_value:
        return raw, DeserializationWarning(node_id, "missing_type", "node has no @type")

    type_list = type_value if isinstance(type_value, list) else [type_value]
    matched: list[type] = []
    seen: set[type] = set()
    for type_token in type_list:
        if not isinstance(type_token, str):
            continue
        type_iri = _expand_iri(type_token, context)
        cls = iri_to_class.get(type_iri)
        if cls is not None and cls not in seen:
            matched.append(cls)
            seen.add(cls)

    cls = _select_most_specific_class(matched)
    if cls is None:
        if not matched:
            return raw, DeserializationWarning(
                node_id,
                "unregistered_type",
                f"no registered class for @type={type_list!r}",
            )
        return raw, DeserializationWarning(
            node_id,
            "ambiguous_type",
            f"multiple incomparable types matched: {[c.__name__ for c in matched]}",
        )

    if not is_dataclass(cls):
        return raw, DeserializationWarning(
            node_id, "not_dataclass", f"{cls.__name__} is not a dataclass"
        )

    jsonld_key_to_field: dict[str, tuple[str, Field[Any]]] = {}
    for f in _cached_dataclass_fields(cls):
        key = f.metadata.get("jsonld_key")
        if key:
            jsonld_key_to_field[key] = (f.name, f)

    kwargs: dict[str, Any] = {}
    for key, value in raw.items():
        if key in ("@id", "@type"):
            continue
        field_info = jsonld_key_to_field.get(key)
        if field_info is None:
            continue
        field_name, f = field_info
        kwargs[field_name] = _coerce_value(value, f, iri_to_class, context)

    try:
        return cls(**kwargs), None
    except (TypeError, ValueError) as exc:
        return raw, DeserializationWarning(
            node_id,
            "constructor_failed",
            f"{cls.__name__}: {exc}",
        )


def _coerce_value(
    value: Any,
    field_info: Field[Any],
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> Any:
    """Coerce a JSON-LD value back to the Python type expected by the field."""
    if isinstance(value, dict):
        if "@value" in value:
            raw_val = value["@value"]
            xsd_type = value.get("@type", "")
            if "boolean" in xsd_type:
                return raw_val == "true" or raw_val is True
            if "integer" in xsd_type:
                return int(raw_val)
            if "decimal" in xsd_type or "float" in xsd_type or "double" in xsd_type:
                return float(raw_val)
            if "dateTime" in xsd_type:
                return datetime.fromisoformat(str(raw_val))
            return raw_val
        if "@type" in value:
            return _rehydrate(value, iri_to_class, context)
        if "@id" in value:
            return value["@id"]
        return value

    if isinstance(value, list):
        return [
            _coerce_value(item, field_info, iri_to_class, context) for item in value
        ]

    return value
