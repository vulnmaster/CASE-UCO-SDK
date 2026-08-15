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


def plan_reparse(repo_root: Path, changed: list[str] | None = None) -> dict[str, Any]:
    """Decide full vs dependent-only parse.

    Returns ``{"mode": "full"|"subset", "reason": ..., "paths": [...]}``.
    A change under ``ontology/UCO`` or ``ontology/CASE`` always forces full
    parse. Leaf extension changes re-parse UCO+CASE (ancestors) plus the
    changed modules and their DAG dependents — not the other extensions.
    """
    changed = list(changed if changed is not None else changed_files(repo_root))
    if not changed:
        return {"mode": "full", "reason": "no-delta", "paths": []}

    core_hit = any(
        path.startswith("ontology/UCO/") or path.startswith("ontology/CASE/")
        or "/ontology/UCO/" in path
        or "/ontology/CASE/" in path
        for path in changed
    )
    if core_hit:
        return {"mode": "full", "reason": "core-ontology-changed", "paths": changed}

    dag = _load_dag(repo_root)
    if dag is None:
        return {"mode": "full", "reason": "missing-module-dag", "paths": changed}

    file_to_module, module_files, dependents = _dag_indexes(dag)
    touched: set[str] = set()
    unmapped: list[str] = []
    for path in changed:
        module = file_to_module.get(path)
        if module is None:
            unmapped.append(path)
            continue
        touched.add(module)
        touched.update(_walk(dependents, module))
    if unmapped:
        return {
            "mode": "full",
            "reason": "unmapped-source-files",
            "paths": changed,
            "unmapped": unmapped,
        }

    needed: set[str] = set()
    imports = {node_id: node.get("imports") or [] for node_id, node in dag.get("nodes", {}).items()}
    for module in touched:
        needed.add(module)
        needed.update(_walk(imports, module))

    paths: set[str] = set()
    for module in needed:
        for path in module_files.get(module, []):
            paths.add(path)
    # Always include core UCO/CASE files so subclass SPARQL still resolves.
    for path, module in file_to_module.items():
        if module.startswith("uco.") or module.startswith("case."):
            paths.add(path)

    return {
        "mode": "subset",
        "reason": "extension-leaf-delta",
        "paths": sorted(paths),
        "modules": sorted(needed),
        "changed": changed,
    }


_REGISTRY_COPIES = (
    Path("csharp") / "CaseUco" / "_registry.json",
    Path("java") / "src" / "main" / "resources" / "_registry.json",
    Path("rust") / "src" / "_registry.json",
)


def _sync_language_registries(repo_root: Path, source: Path) -> None:
    """Copy the merged Python registry onto existing C#/Java/Rust copies."""
    import shutil

    for rel in _REGISTRY_COPIES:
        dest = repo_root / rel
        if dest.is_file():
            shutil.copy2(source, dest)


def merge_registry(repo_root: Path, schema: Any) -> Path | None:
    """Merge subset-parsed *extension* classes into the existing runtime registry.

    Subset parses include UCO/CASE ancestors so SPARQL subclass queries
    resolve. Those ancestor records are a partial extract and must not
    overwrite the last full-generate core class records.
    """
    dest = repo_root / "python" / "case_uco" / "_registry.json"
    if not dest.is_file():
        return None
    try:
        registry = json.loads(dest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    from case_uco_generator.schema_model import iri_local_name

    classes = registry.setdefault("classes", {})
    modules = set(registry.get("modules") or [])
    resolve_all = getattr(schema, "resolve_all_properties", None)
    for cls in schema.classes.values():
        if not str(getattr(cls, "module", "")).startswith("ext."):
            continue
        props = resolve_all(cls) if callable(resolve_all) else list(getattr(cls, "properties", []) or [])
        classes[cls.name] = {
            "iri": cls.iri,
            "module": cls.module,
            "description": getattr(cls, "description", "") or "",
            "parents": list(getattr(cls, "all_parent_names", None) or []),
            "is_facet": bool(getattr(cls, "is_facet", False)),
            "properties": [
                {
                    "name": prop.name,
                    "type": iri_local_name(prop.range_iri),
                    "type_iri": prop.range_iri,
                    "cardinality": prop.cardinality.value,
                    "required": prop.cardinality.is_required,
                    "description": prop.description,
                }
                for prop in props
            ],
        }
        modules.add(cls.module)
    registry["modules"] = sorted(modules)
    dest.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _sync_language_registries(repo_root, dest)
    return dest


def _load_dag(repo_root: Path) -> dict[str, Any] | None:
    path = repo_root / "topology" / "module-dependency-dag.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _dag_indexes(dag: dict[str, Any]) -> tuple[dict[str, str], dict[str, list[str]], dict[str, list[str]]]:
    file_to_module: dict[str, str] = {}
    module_files: dict[str, list[str]] = {}
    dependents: dict[str, list[str]] = {}
    for node_id, node in dag.get("nodes", {}).items():
        files = [entry.get("path") for entry in node.get("files") or [] if entry.get("path")]
        module_files[node_id] = files
        for path in files:
            file_to_module[path] = node_id
        for imported in node.get("imports") or []:
            dependents.setdefault(imported, []).append(node_id)
    return file_to_module, module_files, dependents


def _walk(edges: dict[str, list[str]], start: str) -> set[str]:
    seen: set[str] = set()
    stack = list(edges.get(start) or [])
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(edges.get(current) or [])
    return seen


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


def _registry_summary(repo_root: Path) -> dict[str, Any]:
    """Derive global IR counts from the last full-generate registry."""
    dest = repo_root / "python" / "case_uco" / "_registry.json"
    if not dest.is_file():
        return {}
    try:
        registry = json.loads(dest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    classes = registry.get("classes") or {}
    module_counts: dict[str, int] = {}
    facet_count = 0
    inheritance = 0
    for record in classes.values():
        if not isinstance(record, dict):
            continue
        module = str(record.get("module") or "unknown")
        module_counts[module] = module_counts.get(module, 0) + 1
        if record.get("is_facet"):
            facet_count += 1
        parents = record.get("parents") or []
        if isinstance(parents, list):
            inheritance += len(parents)
    return {
        "class_count": len(classes),
        "facet_count": facet_count,
        "module_counts": dict(sorted(module_counts.items())),
        "inheritance_edge_count": inheritance,
    }


def _resolve_ir_counts(
    repo_root: Path,
    previous_ir: dict[str, Any],
    *,
    class_count: int,
    facet_count: int,
    modules: dict[str, int],
    inheritance_edge_count: int,
) -> tuple[int, int, dict[str, int], int]:
    """Keep global IR counts from the last full write; never shrink on subset.

    A subset parse (or ``schema=None``) must not replace a known full
    inventory with a partial one. If the previous IR was already zeroed,
    fall back to counting the runtime registry.
    """
    prev_count = int(previous_ir.get("class_count") or 0)
    if prev_count and (not class_count or class_count < prev_count):
        prev_modules = previous_ir.get("module_counts") or modules
        return (
            prev_count,
            int(previous_ir.get("facet_count") or facet_count),
            prev_modules if isinstance(prev_modules, dict) else modules,
            int(previous_ir.get("inheritance_edge_count") or inheritance_edge_count),
        )
    if class_count == 0:
        summary = _registry_summary(repo_root)
        if summary.get("class_count"):
            return (
                int(summary["class_count"]),
                int(summary.get("facet_count") or 0),
                summary.get("module_counts") or modules,
                int(summary.get("inheritance_edge_count") or 0),
            )
    return class_count, facet_count, modules, inheritance_edge_count


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

    previous_ir: dict[str, Any] = {}
    if ir_path(repo_root).is_file():
        try:
            previous_ir = json.loads(ir_path(repo_root).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            previous_ir = {}
    class_count, facet_count, modules, inheritance_edge_count = _resolve_ir_counts(
        repo_root,
        previous_ir,
        class_count=class_count,
        facet_count=facet_count,
        modules=modules,
        inheritance_edge_count=len(inheritance),
    )

    payload = {
        "schema_version": IR_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_aggregate_sha256": manifest["aggregate_sha256"],
        "source_file_count": manifest["file_count"],
        "class_count": class_count,
        "facet_count": facet_count,
        "module_counts": dict(sorted(modules.items())) if isinstance(modules, dict) else modules,
        "inheritance_edge_count": inheritance_edge_count,
        "recommended_facet_bundles": facet_bundles or previous_ir.get("recommended_facet_bundles") or {},
        "notes": (
            "When source_aggregate_sha256 matches the live manifest, "
            "generate skips OWL parse and class emission. A change under "
            "ontology/UCO or ontology/CASE forces a full parse. A leaf "
            "extension change re-parses UCO+CASE plus the changed module "
            "and its DAG dependents, then merges those classes into the "
            "runtime registry without rewriting core language bindings."
        ),
    }
    dest = ir_path(repo_root)
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    logger.info("Wrote IR %s (aggregate=%s)", dest, manifest["aggregate_sha256"][:12])
    return dest
