"""Bounded, frozen-context JSON-LD streaming writer (#80)."""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_COMPACT_IRI = re.compile(r"^([A-Za-z][A-Za-z0-9._-]*):")
_ABSOLUTE_SCHEMES = frozenset({"http", "https", "urn", "mailto", "file", "data", "did", "tag"})


@dataclass(frozen=True)
class BoundedStreamingWriteMetrics:
    nodes: int
    bytes_written: int
    max_node_bytes_written: int


class JsonLdStreamWriter:
    """Write nodes without retaining the full graph or document in memory.

    The JSON-LD context is frozen before the first node. Property names and
    ``@id``/``@type`` compact IRIs using an undeclared prefix fail closed.
    ``max_node_bytes`` bounds the only node-sized serialization buffer. Atomic
    mode writes beside the destination and preserves prior bytes on any error.
    """

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        context: Mapping[str, str],
        indent: int | None = 2,
        atomic: bool = True,
        max_node_bytes: int = 1_048_576,
    ) -> None:
        if not isinstance(context, Mapping) or not context:
            raise ValueError("a non-empty frozen JSON-LD context is required")
        if max_node_bytes <= 0:
            raise ValueError("max_node_bytes must be positive")
        if indent is not None and indent < 0:
            raise ValueError("indent must be non-negative or None")
        self.path = Path(path)
        self.context = dict(context)
        if any(not isinstance(k, str) or not isinstance(v, str) for k, v in self.context.items()):
            raise TypeError("context prefixes and IRIs must be strings")
        self.indent = indent
        self.atomic = atomic
        self.max_node_bytes = max_node_bytes
        self._handle: Any = None
        self._tmp_path: Path | None = None
        self._nodes = 0
        self._bytes = 0
        self._max_node = 0
        self._failed = False
        self._complete = False

    def __enter__(self) -> JsonLdStreamWriter:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        output = self.path
        if self.atomic:
            fd, tmp_name = tempfile.mkstemp(
                prefix=f".{self.path.name}.", suffix=".jsonld.tmp", dir=self.path.parent
            )
            os.close(fd)
            self._tmp_path = Path(tmp_name)
            output = self._tmp_path
        self._handle = output.open("wb")
        separator = (",", ":") if self.indent is None else None
        context_json = json.dumps(
            self.context,
            indent=self.indent,
            sort_keys=True,
            separators=separator,
            ensure_ascii=False,
        ).encode("utf-8")
        self._emit(b'{"@context":')
        if self.indent is not None:
            self._emit(b" ")
        self._emit(context_json)
        self._emit(b',"@graph":[' if self.indent is None else b',\n"@graph": [\n')
        return self

    def write_node(self, node: Mapping[str, Any]) -> None:
        if self._handle is None or self._complete:
            raise RuntimeError("JsonLdStreamWriter is not open")
        if self._failed:
            raise RuntimeError("JsonLdStreamWriter is in a failed state")
        if not isinstance(node, Mapping):
            self._failed = True
            raise TypeError("JSON-LD graph nodes must be mappings")
        try:
            self._validate_prefixes(node)
            if self._nodes:
                self._emit(b"," if self.indent is None else b",\n")
            encoder = json.JSONEncoder(
                ensure_ascii=False,
                sort_keys=True,
                indent=self.indent,
                separators=(",", ":") if self.indent is None else None,
                default=str,
            )
            node_bytes = 0
            for chunk in encoder.iterencode(node):
                encoded = chunk.encode("utf-8")
                node_bytes += len(encoded)
                if node_bytes > self.max_node_bytes:
                    raise ValueError(
                        f"node exceeds max_node_bytes={self.max_node_bytes}"
                    )
                self._emit(encoded)
            self._nodes += 1
            self._max_node = max(self._max_node, node_bytes)
        except Exception:
            self._failed = True
            raise

    def complete(self) -> BoundedStreamingWriteMetrics:
        if self._complete:
            return self.metrics
        if self._handle is None:
            raise RuntimeError("JsonLdStreamWriter is not open")
        if self._failed:
            self.abort()
            raise RuntimeError("cannot complete a failed JsonLdStreamWriter")
        try:
            self._emit(b"]}" if self.indent is None else b"\n]\n}\n")
            self._handle.flush()
            os.fsync(self._handle.fileno())
            self._handle.close()
            self._handle = None
            if self.atomic and self._tmp_path is not None:
                os.replace(self._tmp_path, self.path)
                self._tmp_path = None
            self._complete = True
            return self.metrics
        except Exception:
            self._failed = True
            self.abort()
            raise

    @property
    def metrics(self) -> BoundedStreamingWriteMetrics:
        return BoundedStreamingWriteMetrics(
            nodes=self._nodes,
            bytes_written=self._bytes,
            max_node_bytes_written=self._max_node,
        )

    def abort(self) -> None:
        if self._handle is not None:
            self._handle.close()
            self._handle = None
        if self._tmp_path is not None:
            self._tmp_path.unlink(missing_ok=True)
            self._tmp_path = None

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if exc_type is not None or self._failed:
            self.abort()
        else:
            self.complete()

    def _emit(self, data: bytes) -> None:
        self._handle.write(data)
        self._bytes += len(data)

    def _validate_prefixes(self, node: Mapping[str, Any]) -> None:
        declared = set(self.context)

        def check_iri(value: str) -> None:
            match = _COMPACT_IRI.match(value)
            if match and match.group(1) not in declared and match.group(1).lower() not in _ABSOLUTE_SCHEMES:
                raise ValueError(f"undeclared JSON-LD prefix: {match.group(1)!r}")

        def walk(value: Any) -> None:
            if isinstance(value, Mapping):
                for key, nested in value.items():
                    if not isinstance(key, str):
                        raise TypeError("JSON-LD object keys must be strings")
                    if not key.startswith("@"):
                        check_iri(key)
                    if key in {"@id", "@type"}:
                        if isinstance(nested, str):
                            check_iri(nested)
                        elif isinstance(nested, list):
                            for item in nested:
                                if isinstance(item, str):
                                    check_iri(item)
                    walk(nested)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(node)
