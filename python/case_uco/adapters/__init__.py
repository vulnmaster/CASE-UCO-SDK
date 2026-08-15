"""Offline interop adapters (VICS / PhotoDNA / hash-match). No sockets."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Protocol

from case_uco.builder import InvestigationBuilder


class Adapter(Protocol):
    id: str
    profile_ids: tuple[str, ...]
    air_gapped: bool

    def probe(self, source: Path) -> bool: ...
    def apply(self, builder: InvestigationBuilder, source: Path, **kwargs: Any) -> dict[str, Any]: ...


def _refuse_remote(source: Path | str) -> None:
    text = str(source).replace("\\", "/")
    if text.startswith(("http://", "https://", "http:/", "https:/")):
        raise ValueError("Adapters refuse non-local URIs")


class PhotoDnaAdapter:
    id = "photodna"
    profile_ids = ("HashIntelligence", "FullCACLifecycle")
    air_gapped = True

    def probe(self, source: Path) -> bool:
        return source.is_file()

    def apply(self, builder: InvestigationBuilder, source: Path, **kwargs: Any) -> dict[str, Any]:
        _refuse_remote(source)
        rows = _load_rows(source)
        created = 0
        for row in rows:
            name = row.get("file") or row.get("file_name") or row.get("path") or "media.bin"
            hashes = []
            if row.get("sha256"):
                hashes.append(("SHA256", row["sha256"]))
            if row.get("photodna") or row.get("PhotoDNA"):
                hashes.append(("PhotoDNA", row.get("photodna") or row.get("PhotoDNA")))
            for pair in row.get("hashes") or []:
                hashes.append(tuple(pair))
            builder.add_csam_evidence(name, hashes=hashes)
            created += 1
        return {"adapter": self.id, "created": created}


class VicsCatalogAdapter:
    id = "vics-catalog"
    profile_ids = ("HashIntelligence", "FullCACLifecycle")
    air_gapped = True

    def probe(self, source: Path) -> bool:
        return source.is_file()

    def apply(self, builder: InvestigationBuilder, source: Path, **kwargs: Any) -> dict[str, Any]:
        _refuse_remote(source)
        rows = _load_rows(source)
        created = 0
        for row in rows:
            media_id = row.get("MediaId") or row.get("media_id")
            name = media_id or row.get("file_name") or row.get("path") or "vics-media"
            hashes = []
            if row.get("SHA256") or row.get("sha256"):
                hashes.append(("SHA256", row.get("SHA256") or row.get("sha256")))
            if row.get("MD5") or row.get("md5"):
                hashes.append(("MD5", row.get("MD5") or row.get("md5")))
            if row.get("PhotoDNA") or row.get("photodna"):
                hashes.append(("PhotoDNA", row.get("PhotoDNA") or row.get("photodna")))
            created_obj = builder.add_csam_evidence(str(name), hashes=hashes)
            picture = created_obj.get("picture") if isinstance(created_obj, dict) else None
            node_id = builder.graph.get_id(picture) if picture is not None else None
            if media_id and node_id:
                builder.graph.add_property(str(node_id), "uco-core:tag", f"vics-media-id:{media_id}")
            created += 1
        return {"adapter": self.id, "created": created}


class HashMatchAdapter:
    id = "hash-match"
    profile_ids = ("HashIntelligence",)
    air_gapped = True

    def probe(self, source: Path) -> bool:
        return source.is_file()

    def apply(self, builder: InvestigationBuilder, source: Path, **kwargs: Any) -> dict[str, Any]:
        _refuse_remote(source)
        rows = _load_rows(source)
        from case_uco.case.investigation import InvestigativeAction
        from case_uco.uco.analysis import AnalyticResult
        from case_uco.uco.core import ConfidenceFacet

        recorded: list[dict[str, Any]] = []
        for row in rows:
            digest = str(
                row.get("digest")
                or row.get("sha256")
                or row.get("SHA256")
                or row.get("hash")
                or ""
            ).strip()
            if not digest:
                continue
            method = row.get("method") or row.get("hashMethod") or "SHA256"
            hits = builder.graph.lookup_hash(digest, method=str(method))
            if not hits:
                continue
            hit = hits[0]
            statement = f"Offline hash-match {method}={digest} → {hit.get('id')}"
            facets = []
            distance = row.get("distance") or row.get("match_distance")
            if distance is not None:
                try:
                    conf = max(0, min(100, 100 - int(float(distance))))
                except (TypeError, ValueError):
                    conf = 100
                facets.append(ConfidenceFacet(confidence=conf))
            result = builder.graph.create(
                AnalyticResult,
                name=f"hash-match {Path(str(row.get('file') or row.get('file_name') or digest[:12])).name}",
                statement=[statement],
                has_facet=facets,
            )
            builder.graph.create(
                InvestigativeAction,
                name=f"hash-match lookup {method}",
                object=[{"@id": hit.get("id")}] if hit.get("id") else [],
                result=[result],
            )
            recorded.append(
                {
                    "digest": digest,
                    "method": str(method),
                    "node_id": hit.get("id"),
                    "result": builder.graph.get_id(result),
                }
            )
        return {"adapter": self.id, "matches": len(recorded), "hits": recorded}


_ADAPTERS = {
    "photodna": PhotoDnaAdapter(),
    "vics-catalog": VicsCatalogAdapter(),
    "hash-match": HashMatchAdapter(),
}


def get_adapter(adapter_id: str) -> Any:
    if adapter_id not in _ADAPTERS:
        raise ValueError(f"Unknown adapter: {adapter_id}")
    return _ADAPTERS[adapter_id]


def _load_rows(source: Path) -> list[dict[str, Any]]:
    path = Path(source)
    if not path.is_file():
        raise ValueError(f"Adapter source is not a local file: {source}")
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Adapter source unreadable: {source}: {exc}") from exc
    if not text.strip():
        raise ValueError(f"Adapter source is empty: {source}")
    if path.suffix.lower() in {".csv", ".tsv"}:
        delim = "\t" if path.suffix.lower() == ".tsv" else ","
        return list(csv.DictReader(text.splitlines(), delimiter=delim))
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Adapter source is malformed JSON: {source}: {exc}") from exc
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        raise ValueError(f"Adapter source JSON must be a list or object: {source}")
    return payload.get("items") or payload.get("media") or payload.get("files") or []
