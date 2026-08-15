"""Content-hashed source manifest and incremental generate skip."""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

IR_DIRNAME = "generator/ir"
MANIFEST_NAME = "source-manifest.json"
IR_NAME = "ontology-ir.json"
IR_VERSION = "1.0.0"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_source_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for root_name in ("ontology", "extensions"):
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.ttl"):
            posix = path.as_posix()
            if "/dependencies/" in posix or "/examples_knowledge_graphs/" in posix:
                continue
            if path.name.endswith("-example.ttl") or path.name.endswith("-exemplar.ttl"):
                continue
            files.append(path)
    return sorted(files)


def build_manifest(repo_root: Path) -> dict[str, Any]:
    files = []
    hasher = hashlib.sha256()
    for path in collect_source_files(repo_root):
        digest = _sha256(path)
        rel = path.relative_to(repo_root).as_posix()
        files.append({"path": rel, "sha256": digest, "bytes": path.stat().st_size})
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(digest.encode("ascii"))
    return {
        "schema_version": IR_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "aggregate_sha256": hasher.hexdigest(),
        "files": files,
    }


def manifest_path(repo_root: Path) -> Path:
    return repo_root / IR_DIRNAME / MANIFEST_NAME


def ir_path(repo_root: Path) -> Path:
    return repo_root / IR_DIRNAME / IR_NAME


def load_manifest(repo_root: Path) -> dict[str, Any] | None:
    path = manifest_path(repo_root)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def sources_unchanged(repo_root: Path) -> bool:
    previous = load_manifest(repo_root)
    if previous is None:
        return False
    current = build_manifest(repo_root)
    return current.get("aggregate_sha256") == previous.get("aggregate_sha256")


def changed_files(repo_root: Path) -> list[str]:
    previous = load_manifest(repo_root)
    current = build_manifest(repo_root)
    if previous is None:
        return [entry["path"] for entry in current["files"]]
    old = {entry["path"]: entry["sha256"] for entry in previous.get("files", [])}
    new = {entry["path"]: entry["sha256"] for entry in current["files"]}
    changed = [path for path, digest in new.items() if old.get(path) != digest]
    changed.extend(path for path in old if path not in new)
    return sorted(changed)


def write_ir(repo_root: Path, schema: Any | None = None) -> Path:
    """Write the source manifest and a compact IR summary.

    The compact IR captures counts, modules, inheritance edges, and
    recommended Facet bundles. Full typed emission still uses OntologySchema
    from a live parse when sources changed.
    """
    ir_dir = repo_root / IR_DIRNAME
    ir_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(repo_root)
    manifest_path(repo_root).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    modules: dict[str, int] = {}
    inheritance: list[dict[str, str]] = []
    facet_count = 0
    class_count = 0
    if schema is not None:
        class_count = len(schema.classes)
        for cls in schema.classes.values():
            modules[cls.module] = modules.get(cls.module, 0) + 1
            if getattr(cls, "is_facet", False):
                facet_count += 1
            for parent in cls.parent_iris:
                inheritance.append(
                    {"class": cls.name, "parent": parent.rsplit("/", 1)[-1].rsplit("#", 1)[-1]}
                )

    facet_bundles = {}
    try:
        from case_uco.topology.profiles import list_profiles

        for profile in list_profiles():
            facet_bundles[profile.id] = {
                item.host: {"required": list(item.required), "recommended": list(item.recommended)}
                for item in profile.facet_sets
            }
    except Exception as exc:  # pragma: no cover - optional during bootstrap
        logger.debug("Profile bundles unavailable for IR: %s", exc)

    payload = {
        "schema_version": IR_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_aggregate_sha256": manifest["aggregate_sha256"],
        "source_file_count": manifest["file_count"],
        "class_count": class_count,
        "facet_count": facet_count,
        "module_counts": dict(sorted(modules.items())),
        "inheritance_edge_count": len(inheritance),
        "recommended_facet_bundles": facet_bundles,
        "notes": (
            "When source_aggregate_sha256 matches the live manifest, "
            "generate may skip parse and emission. A source change triggers "
            "a full re-parse of the changed files' import dependents "
            "(currently the whole closure, because parse_ontology loads one graph)."
        ),
    }
    dest = ir_path(repo_root)
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    logger.info("Wrote IR %s (aggregate=%s)", dest, manifest["aggregate_sha256"][:12])
    return dest
