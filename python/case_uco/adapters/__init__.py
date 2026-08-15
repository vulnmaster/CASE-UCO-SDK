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
            name = row.get("MediaId") or row.get("file_name") or row.get("path") or "vics-media"
            hashes = []
            if row.get("SHA256") or row.get("sha256"):
                hashes.append(("SHA256", row.get("SHA256") or row.get("sha256")))
            if row.get("MD5") or row.get("md5"):
                hashes.append(("MD5", row.get("MD5") or row.get("md5")))
            if row.get("PhotoDNA") or row.get("photodna"):
                hashes.append(("PhotoDNA", row.get("PhotoDNA") or row.get("photodna")))
            builder.add_csam_evidence(str(name), hashes=hashes)
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
        return {"adapter": self.id, "matches": len(rows)}


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
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() in {".csv", ".tsv"}:
        delim = "\t" if source.suffix.lower() == ".tsv" else ","
        return list(csv.DictReader(text.splitlines(), delimiter=delim))
    payload = json.loads(text)
    if isinstance(payload, list):
        return payload
    return payload.get("items") or payload.get("media") or payload.get("files") or []
