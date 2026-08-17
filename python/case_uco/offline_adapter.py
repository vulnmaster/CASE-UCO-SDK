"""Bounded, air-gapped adapter boundary for authorized local mappings.

This is a plugin interface, not a catalog. It does not embed a licensed
data model, classify content, or open a network resource.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from case_uco.graph import CASEGraph
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.types import Hash

PUBLIC_SURFACE = (
    "AdapterBounds",
    "AdapterRefused",
    "LocalJsonRecordsAdapter",
    "OfflineAdapter",
    "apply_offline_adapter",
    "register_adapter",
    "get_adapter",
    "list_adapters",
)

DEFAULT_MAX_BYTES = 8 * 1024 * 1024
DEFAULT_MAX_ROWS = 10_000
DEFAULT_MAX_SECONDS = 5.0


class AdapterRefused(ValueError):
    """Fail-closed refusal (remote URI, missing file, bound exceeded, etc.)."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


@dataclass(frozen=True)
class AdapterBounds:
    max_bytes: int = DEFAULT_MAX_BYTES
    max_rows: int = DEFAULT_MAX_ROWS
    max_seconds: float = DEFAULT_MAX_SECONDS


@runtime_checkable
class OfflineAdapter(Protocol):
    adapter_id: str
    air_gapped: bool

    def probe(self, source: Path) -> bool: ...

    def apply(self, graph: CASEGraph, source: Path, **kwargs: Any) -> dict[str, Any]: ...


_REGISTRY: dict[str, OfflineAdapter] = {}


def _as_local_path(source: Path | str) -> Path:
    text = str(source).strip()
    if not text:
        raise AdapterRefused("adapter_source_missing", "source path is required")
    lowered = text.replace("\\", "/").lower()
    if lowered.startswith(("http://", "https://", "ftp://", "sftp://")):
        raise AdapterRefused("adapter_remote_refused", "adapters refuse non-local URIs")
    return Path(source)


def register_adapter(adapter: OfflineAdapter) -> None:
    if not getattr(adapter, "air_gapped", False):
        raise AdapterRefused(
            "adapter_not_air_gapped",
            "only air-gapped adapters may be registered",
        )
    ident = str(getattr(adapter, "adapter_id", "")).strip()
    if not ident:
        raise AdapterRefused("adapter_id_required", "adapter_id is required")
    _REGISTRY[ident] = adapter


def get_adapter(adapter_id: str) -> OfflineAdapter:
    try:
        return _REGISTRY[adapter_id]
    except KeyError as exc:
        raise AdapterRefused("adapter_unknown", f"unknown adapter {adapter_id!r}") from exc


def list_adapters() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY))


def apply_offline_adapter(
    adapter: OfflineAdapter | str,
    graph: CASEGraph,
    source: Path | str,
    *,
    bounds: AdapterBounds | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Run a registered or caller-supplied air-gapped adapter.

    Enforces local-only source, file existence, byte/row/time bounds, and
    ``air_gapped=True``. Does not classify content.
    """
    limits = bounds or AdapterBounds()
    if isinstance(adapter, str):
        adapter = get_adapter(adapter)
    if not getattr(adapter, "air_gapped", False):
        raise AdapterRefused(
            "adapter_not_air_gapped",
            "refusing an adapter that is not air-gapped",
        )
    path = _as_local_path(source)
    if not path.is_file():
        raise AdapterRefused("adapter_source_missing", "source file does not exist")
    size = path.stat().st_size
    if size > limits.max_bytes:
        raise AdapterRefused(
            "adapter_source_too_large",
            f"source exceeds max_bytes={limits.max_bytes}",
        )
    started = time.perf_counter()
    result = adapter.apply(graph, path, bounds=limits, **kwargs)
    elapsed = time.perf_counter() - started
    if elapsed > limits.max_seconds:
        raise AdapterRefused(
            "adapter_time_exceeded",
            f"adapter exceeded max_seconds={limits.max_seconds}",
        )
    if not isinstance(result, dict):
        raise AdapterRefused("adapter_result_invalid", "adapter must return a dict")
    return result


class LocalJsonRecordsAdapter:
    """Generic local JSON records → hashed ObservableObject mapping.

    Expected file shape (array of objects)::

        [{"file_name": "empty.bin", "hashes": [["SHA256", "e3b0..."]]}]

    Callers supply names and hashes. This adapter does not classify them.
    """

    adapter_id = "local-json-records"
    air_gapped = True

    def probe(self, source: Path) -> bool:
        return source.is_file() and source.suffix.lower() == ".json"

    def apply(
        self,
        graph: CASEGraph,
        source: Path,
        **kwargs: Any,
    ) -> dict[str, Any]:
        limits: AdapterBounds = kwargs.get("bounds") or AdapterBounds()
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise AdapterRefused(
                "adapter_source_invalid",
                "source is not readable JSON",
            ) from exc
        if not isinstance(payload, list):
            raise AdapterRefused(
                "adapter_source_invalid",
                "source must be a JSON array of records",
            )
        if len(payload) > limits.max_rows:
            raise AdapterRefused(
                "adapter_row_limit",
                f"source exceeds max_rows={limits.max_rows}",
            )
        created = 0
        for index, row in enumerate(payload):
            if not isinstance(row, dict):
                raise AdapterRefused(
                    "adapter_row_invalid",
                    f"record {index} is not an object",
                )
            file_name = str(row.get("file_name") or "").strip()
            hashes = row.get("hashes")
            if not file_name:
                raise AdapterRefused(
                    "adapter_row_invalid",
                    f"record {index} is missing file_name",
                )
            if not isinstance(hashes, list) or not hashes:
                raise AdapterRefused(
                    "adapter_row_invalid",
                    f"record {index} is missing hashes",
                )
            hash_objs: list[Hash] = []
            for pair in hashes:
                if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                    raise AdapterRefused(
                        "adapter_row_invalid",
                        f"record {index} has a malformed hash pair",
                    )
                method = str(pair[0]).strip()
                value = str(pair[1]).strip()
                if not method or not value:
                    raise AdapterRefused(
                        "adapter_row_invalid",
                        f"record {index} has an empty hash method or value",
                    )
                hash_objs.append(Hash(hash_method=method, hash_value=value))
            graph.create(
                ObservableObject,
                has_facet=[
                    FileFacet(file_name=[file_name]),
                    ContentDataFacet(hash=hash_objs),
                ],
            )
            created += 1
        return {"adapter": self.adapter_id, "created": created}


register_adapter(LocalJsonRecordsAdapter())
