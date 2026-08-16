"""Bounded Apple acquisition-package classification and CASE/UCO graph building.

Issue #99 adds a deliberately narrow bridge from a local Apple artifact package
(or a structured inventory JSON file) to a package-level CASE/UCO graph.  It is
not an Apple log decoder: binary ``.tracev3`` data is inventoried by metadata
only, and event nodes can only be sampled from an external CSV/JSONL excerpt.

Security properties:

* caller-controlled paths are checked with ``workspace_policy``;
* package walks, inventory files, hashes, event rows, and string literals are
  bounded;
* ``profile='auto'`` fails closed when the tree is unsupported or ambiguous;
* shareable mode normalizes paths and redacts identifiers while omitting event
  messages by default; and
* the public result contains counts, sizes, digests, and validation guidance,
  never source rows, device identifiers, or message bodies.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import tempfile
import threading
import uuid
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, cast

import workspace_policy

TOOL_NAME = "case-uco-apple-acquisition-package"
TOOL_VERSION = "1.0.0"
CONTENT_TRUST_LABEL = "untrusted-source-content"

PROFILE_AUTO = "auto"
PROFILE_SYSDIAGNOSE = "ios-sysdiagnose"
PROFILE_FOSS = "apple-foss-logarchive"
SUPPORTED_PROFILES = frozenset({PROFILE_AUTO, PROFILE_SYSDIAGNOSE, PROFILE_FOSS})

MAX_INVENTORY_BYTES = 2 * 1024 * 1024
MAX_INVENTORY_ENTRIES = 4096
MAX_INVENTORY_DEPTH = 16
MAX_EVENT_RECORDS = 1000
MAX_EVENT_LINE_BYTES = 16 * 1024
MAX_EVENT_SCAN_BYTES = 20 * 1024 * 1024
MAX_EVENT_LITERAL = 500
MAX_HASH_BYTES = 32 * 1024 * 1024
MAX_CRASH_SAMPLES = 3
_CSV_FIELD_LIMIT_LOCK = threading.Lock()

SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"
_CONTEXT = {
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
    "solveit-observable": "https://ontology.solveit-df.org/solveit/observable/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

# These patterns intentionally target common high-risk identifiers rather than
# every number.  Hashes and ordinary timestamps must remain usable metadata.
_IDENTIFIER_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("udid", re.compile(r"(?i)\b(?:[0-9a-f]{40}|[0-9a-f]{8}-[0-9a-f]{16})\b")),
    ("uuid", re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")),
    ("imei", re.compile(r"(?<!\d)\d{15}(?!\d)")),
    ("phone", re.compile(r"(?<!\w)(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?!\w)")),
    ("labeled-serial", re.compile(r"(?i)\b(serial(?:\s+number)?|udid|imei)\s*[:=]\s*[A-Z0-9-]{6,40}\b")),
)


@dataclass(frozen=True)
class InventoryEntry:
    """One bounded package inventory entry."""

    relative_path: str
    kind: str
    size: int = 0
    source_path: Path | None = None
    sha256: str | None = None


@dataclass
class PackageInventory:
    """Normalized local-directory or inventory-JSON input."""

    root_name: str
    entries: list[InventoryEntry]
    metadata: dict[str, Any] = field(default_factory=dict)
    source_kind: str = "directory"
    source_path: Path | None = None
    base_path: Path | None = None
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ShapeDecision:
    profile: str
    logarchive_path: str
    signals: tuple[str, ...]


@dataclass(frozen=True)
class BuildResult:
    output_path: Path
    profile: str
    node_count: int
    event_record_count: int
    inventory_entry_count: int
    package_byte_size: int
    named_file_digests: tuple[dict[str, str], ...]
    shareable: bool
    identifiers_redacted: int
    messages_affected: int
    event_message_policy: str
    warnings: tuple[str, ...]

    def safe_metadata(self) -> dict[str, Any]:
        """Return the MCP-safe result contract; never include source content."""

        return {
            "ok": True,
            "output_graph_path": str(self.output_path),
            "tool_name": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "profile": self.profile,
            "node_count": self.node_count,
            "event_records": self.event_record_count,
            "inventory_entries": self.inventory_entry_count,
            "package_byte_size": self.package_byte_size,
            "named_file_digests": list(self.named_file_digests),
            "shareable": self.shareable,
            "redaction": {
                "paths_normalized": self.shareable,
                "identifiers_redacted": self.identifiers_redacted,
                "event_message_policy": self.event_message_policy,
                "messages_affected": self.messages_affected,
                "raw_lines_included": False,
            },
            "content_trust": CONTENT_TRUST_LABEL,
            "warnings": list(self.warnings),
            "validation_status": "not_validated",
            "next": "validate_graph(output_graph_path, extensions=['solveit'], strict_concepts=True)",
            "safe_summary": (
                f"Built a bounded {self.profile} package graph with "
                f"{self.node_count} nodes and {self.event_record_count} sampled "
                "event records. Source rows and message bodies are not returned; "
                "run extension-aware validation before relying on the graph."
            ),
        }


class _GraphBuilder:
    def __init__(self) -> None:
        self.nodes: list[dict[str, Any]] = []
        self._counter: int = 0
        # A per-graph namespace prevents nodes from unrelated acquisition
        # packages being conflated when their JSON-LD is later combined.
        self._namespace = uuid.uuid4()

    def new_id(self, role: str) -> str:
        self._counter += 1
        value = uuid.uuid5(
            self._namespace,
            f"case-uco-sdk:apple-package:{role}:{self._counter}",
        )
        return f"urn:uuid:{value}"

    def add(self, node_type: str | list[str], **properties: Any) -> dict[str, Any]:
        role = node_type[0] if isinstance(node_type, list) else node_type
        node: dict[str, Any] = {"@id": self.new_id(role), "@type": node_type}
        node.update({key: value for key, value in properties.items() if value is not None})
        self.nodes.append(node)
        return node

    @staticmethod
    def ref(node: dict[str, Any]) -> dict[str, str]:
        return {"@id": node["@id"]}

    def embedded(self, node_type: str, **properties: Any) -> dict[str, Any]:
        node = {"@id": self.new_id(node_type), "@type": node_type}
        node.update({key: value for key, value in properties.items() if value is not None})
        return node


def _bounded_string(value: Any, limit: int = MAX_EVENT_LITERAL) -> str:
    text = " ".join(str(value).replace("\x00", " ").split())
    return text[:limit]


def redact_identifiers(value: str) -> tuple[str, int]:
    """Redact common device/person identifiers from one string literal."""

    output = value
    count = 0
    for label, pattern in _IDENTIFIER_PATTERNS:
        output, replaced = pattern.subn(f"[REDACTED:{label}]", output)
        count += replaced
    return output, count


def _safe_literal(value: Any, *, shareable: bool, limit: int = MAX_EVENT_LITERAL) -> tuple[str, int]:
    text = _bounded_string(value, limit)
    if not shareable:
        return text, 0
    return redact_identifiers(text)


def _normalize_relative_path(raw: str) -> str:
    normalized = raw.replace("\\", "/").strip()
    path = PurePosixPath(normalized)
    if not normalized or normalized in {".", "./"}:
        return "."
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("inventory_path_not_relative")
    if len(path.parts) > MAX_INVENTORY_DEPTH:
        raise ValueError("package_inventory_depth_exceeded")
    return path.as_posix().removeprefix("./")



def _inventory_from_directory(root: Path) -> PackageInventory:
    if not root.is_dir():
        raise ValueError("package_root_not_directory_or_inventory")

    entries: list[InventoryEntry] = []
    warnings: list[str] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack:
        current, depth = stack.pop()
        if depth > MAX_INVENTORY_DEPTH:
            raise ValueError("package_inventory_depth_exceeded")
        try:
            children: list[Path] = []
            for child in current.iterdir():
                if len(entries) + len(children) >= MAX_INVENTORY_ENTRIES:
                    raise ValueError("package_inventory_limit_exceeded")
                children.append(child)
            children.sort(key=lambda item: item.name.casefold())
        except ValueError:
            raise
        except OSError as exc:
            raise ValueError("package_inventory_unreadable") from exc
        for child in children:
            if len(entries) >= MAX_INVENTORY_ENTRIES:
                raise ValueError("package_inventory_limit_exceeded")
            try:
                relative = child.relative_to(root).as_posix()
                if child.is_symlink():
                    entries.append(InventoryEntry(relative, "symlink", 0, child))
                    warnings.append("symlink_entries_not_followed")
                    continue
                if child.is_dir():
                    entries.append(InventoryEntry(relative, "directory", 0, child))
                    stack.append((child, depth + 1))
                elif child.is_file():
                    entries.append(InventoryEntry(relative, "file", child.stat().st_size, child))
                else:
                    entries.append(InventoryEntry(relative, "other", 0, child))
            except OSError as exc:
                raise ValueError("package_inventory_unreadable") from exc
    return PackageInventory(
        root_name=root.name,
        entries=entries,
        source_kind="directory",
        source_path=root,
        base_path=root,
        warnings=sorted(set(warnings)),
    )


def _inventory_entry_from_json(raw: dict[str, Any], base: Path) -> InventoryEntry:
    path_value = raw.get("path", raw.get("relative_path", raw.get("name")))
    if not isinstance(path_value, str):
        raise ValueError("inventory_entry_path_missing")
    relative = _normalize_relative_path(path_value)
    raw_kind = str(raw.get("type", raw.get("kind", ""))).strip().lower()
    if not raw_kind:
        raw_kind = "directory" if raw.get("is_directory") is True else "file"
    aliases = {"dir": "directory", "regular": "file", "regular_file": "file"}
    kind = aliases.get(raw_kind, raw_kind)
    if kind not in {"file", "directory", "symlink", "other"}:
        raise ValueError("inventory_entry_kind_unsupported")
    size_raw = raw.get("size", raw.get("size_in_bytes", 0))
    if isinstance(size_raw, bool):
        raise ValueError("inventory_entry_size_invalid")
    try:
        size = int(size_raw or 0)
    except (TypeError, ValueError) as exc:
        raise ValueError("inventory_entry_size_invalid") from exc
    if size < 0:
        raise ValueError("inventory_entry_size_invalid")
    digest = raw.get("sha256")
    if digest is not None:
        digest = str(digest).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("inventory_entry_sha256_invalid")
    resolved_base = base.resolve()
    candidate = (resolved_base / relative).resolve() if relative != "." else resolved_base
    try:
        candidate.relative_to(resolved_base)
    except ValueError as exc:
        # A relative inventory path can still escape through a symlink. The
        # inventory is untrusted and may not expand its declared package base.
        raise ValueError("inventory_entry_outside_base") from exc
    source_path = workspace_policy.check_read_path(candidate) if candidate.exists() else None
    if source_path is not None and kind == "file" and source_path.is_file():
        try:
            size = source_path.stat().st_size
        except OSError as exc:
            raise ValueError("package_inventory_unreadable") from exc
    return InventoryEntry(relative, kind, size, source_path, digest)


def _inventory_from_json(path: Path) -> PackageInventory:
    if not path.is_file():
        raise ValueError("inventory_missing")
    if path.stat().st_size > MAX_INVENTORY_BYTES:
        raise ValueError("inventory_oversized")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("inventory_json_invalid") from exc
    if isinstance(payload, list):
        raw_entries = payload
        metadata: dict[str, Any] = {}
        root_name = "inventory-package"
    elif isinstance(payload, dict):
        raw_entries = payload.get("entries", payload.get("artifacts"))
        metadata = payload.get("metadata") or {}
        root_name = str(payload.get("root_name") or payload.get("package_name") or "inventory-package")
    else:
        raise ValueError("inventory_json_invalid")
    if not isinstance(raw_entries, list) or not all(isinstance(item, dict) for item in raw_entries):
        raise ValueError("inventory_entries_invalid")
    if len(raw_entries) > MAX_INVENTORY_ENTRIES:
        raise ValueError("package_inventory_limit_exceeded")
    if not isinstance(metadata, dict):
        raise ValueError("inventory_metadata_invalid")
    base_raw = payload.get("base_path") if isinstance(payload, dict) else None
    if base_raw is not None:
        base = workspace_policy.check_read_path(str(base_raw))
        if not base.is_dir():
            raise ValueError("inventory_base_not_directory")
    else:
        base = path.parent
    entries = [_inventory_entry_from_json(item, base) for item in raw_entries]
    return PackageInventory(
        root_name=root_name,
        entries=entries,
        metadata=metadata,
        source_kind="inventory-json",
        source_path=path,
        base_path=base,
    )


def load_package_inventory(package_root: str | Path) -> PackageInventory:
    """Load a bounded local directory or structured JSON inventory."""

    source = workspace_policy.check_read_path(package_root)
    if source.is_dir():
        return _inventory_from_directory(source)
    if source.is_file() and source.suffix.lower() == ".json":
        return _inventory_from_json(source)
    raise ValueError("package_root_not_directory_or_inventory")


def _path_parts(entry: InventoryEntry) -> tuple[str, ...]:
    return tuple(part.casefold() for part in PurePosixPath(entry.relative_path).parts)


def _shape_signals(inventory: PackageInventory) -> dict[str, Any]:
    entries = inventory.entries
    logarchives = sorted(
        entry.relative_path
        for entry in entries
        if entry.kind in {"directory", "file"}
        and PurePosixPath(entry.relative_path).name.casefold().endswith(".logarchive")
    )
    top_components = {
        parts[0]
        for entry in entries
        if (parts := _path_parts(entry))
    }
    all_names = {PurePosixPath(entry.relative_path).name.casefold() for entry in entries}
    sysdiag_markers = {
        marker
        for marker in ("wifi", "summaries", "logs", "crashes_and_spins", "preferences")
        if marker in top_components
    }
    root_named = inventory.root_name.casefold().startswith("sysdiagnose_")
    system_archive = any(
        PurePosixPath(path).name.casefold() == "system_logs.logarchive"
        for path in logarchives
    )
    crash_signal = any(
        entry.relative_path.casefold().endswith(".ips")
        or any(part in {"crashes", "crash", "crash_pull", "crashreports", "crashes_and_spins"} for part in _path_parts(entry))
        for entry in entries
    )
    syslog_signal = any("syslog" in name for name in all_names)
    apps_signal = any(
        any(token in name for token in ("apps", "applications", "installed_app"))
        for name in all_names
    )
    foss_companions = {
        name
        for name, present in (
            ("crash-pull", crash_signal),
            ("live-syslog", syslog_signal),
            ("apps-inventory", apps_signal),
        )
        if present
    }
    strong_sysdiagnose = bool(
        len(logarchives) == 1
        and system_archive
        and ((root_named and len(sysdiag_markers) >= 2) or len(sysdiag_markers) >= 4)
    )
    return {
        "logarchives": logarchives,
        "sysdiag_markers": sysdiag_markers,
        "root_named": root_named,
        "strong_sysdiagnose": strong_sysdiagnose,
        "foss_companions": foss_companions,
    }


def classify_inventory(inventory: PackageInventory, profile: str = PROFILE_AUTO) -> ShapeDecision:
    """Classify an Apple package, refusing unsupported or ambiguous shapes."""

    normalized_profile = profile.strip().lower()
    if normalized_profile not in SUPPORTED_PROFILES:
        raise ValueError("unsupported_acquisition_profile")
    signals = _shape_signals(inventory)
    logarchives: list[str] = signals["logarchives"]
    if not logarchives:
        raise ValueError("apple_logarchive_missing")
    if len(logarchives) != 1:
        raise ValueError("ambiguous_multiple_logarchives")

    strong_sysdiagnose = bool(signals["strong_sysdiagnose"])
    companions: set[str] = signals["foss_companions"]
    if normalized_profile == PROFILE_SYSDIAGNOSE:
        if not strong_sysdiagnose:
            raise ValueError("profile_shape_mismatch_sysdiagnose")
        selected = PROFILE_SYSDIAGNOSE
    elif normalized_profile == PROFILE_FOSS:
        if strong_sysdiagnose:
            raise ValueError("profile_shape_mismatch_foss")
        if not companions:
            raise ValueError("profile_shape_mismatch_foss")
        selected = PROFILE_FOSS
    elif strong_sysdiagnose:
        selected = PROFILE_SYSDIAGNOSE
    elif len(companions) >= 2:
        selected = PROFILE_FOSS
    else:
        # A lone archive or archive + one generic directory is insufficient to
        # claim either a full sysdiagnose or the requested FOSS package shape.
        raise ValueError("ambiguous_apple_package_shape")

    safe_signals: list[str] = ["single-logarchive"]
    if selected == PROFILE_SYSDIAGNOSE:
        safe_signals.extend(sorted(f"sysdiagnose:{item}" for item in signals["sysdiag_markers"]))
    else:
        safe_signals.extend(sorted(f"foss:{item}" for item in companions))
    return ShapeDecision(selected, logarchives[0], tuple(safe_signals))


def apple_collect_guidance(text: str) -> dict[str, Any] | None:
    """Return fail-closed recipe guidance from a textual package description.

    This is routing guidance only.  The local classifier remains authoritative
    because prose cannot prove a filesystem shape.
    """

    normalized = " ".join(text.casefold().replace("\\", "/").split())
    apple_signal = any(token in normalized for token in ("apple", "ios", "iphone", "macos", "logarchive", "sysdiagnose"))
    if not apple_signal:
        return None
    has_archive = ".logarchive" in normalized or "logarchive" in normalized or "system_logs" in normalized
    sysdiag_markers = sum(
        token in normalized
        for token in ("wifi/", "summaries/", "crashes_and_spins", "preferences/", "batterybdc")
    )
    full_sysdiagnose = has_archive and (
        "sysdiagnose_" in normalized
        or "full sysdiagnose" in normalized
        or ("sysdiagnose" in normalized and sysdiag_markers >= 2)
    )
    foss_markers = sum(
        token in normalized
        for token in ("standalone", "foss", "crash pull", "crash_pull", "live syslog", "apps list", "installed apps")
    )
    foss_collect = has_archive and foss_markers >= 2 and not full_sysdiagnose
    timesync_missing = any(
        token in normalized
        for token in ("no timesync", "without timesync", "missing timesync", "timesync absent")
    )
    if full_sysdiagnose:
        shape = PROFILE_SYSDIAGNOSE
        recipes = ["docs/recipes/ios-sysdiagnose.md", "docs/recipes/apple-unified-logs.md"]
        summary = "Description indicates a full sysdiagnose tree; model the package with ios-sysdiagnose and use apple-unified-logs only for decoded excerpts."
    elif foss_collect:
        shape = PROFILE_FOSS
        recipes = ["docs/recipes/apple-unified-logs.md", "docs/recipes/starter-mobile-extraction.md"]
        summary = "Description indicates a standalone FOSS Apple collect, not a full sysdiagnose; use package-level mobile acquisition plus Apple unified-log guidance."
    elif has_archive:
        shape = "unconfirmed-apple-logarchive"
        recipes = ["docs/recipes/apple-unified-logs.md"]
        summary = "An Apple logarchive is described, but there is not enough evidence to claim full sysdiagnose or FOSS-package shape; run classify_apple_package_shape on the local root/inventory."
    else:
        return None
    return {
        "claimed_shape": shape,
        "authoritative_next_tool": "classify_apple_package_shape(package_root, profile='auto')",
        "builder": "build_acquisition_package_graph(..., extensions=['solveit'])",
        "recipes": recipes,
        "summary": summary,
        "timesync_guidance": (
            "Timesync is reported missing: preserve mach_continuous_time/boot_uuid and omit absolute device UTC."
            if timesync_missing else
            "Do not assert device-absolute UTC unless timesync anchoring is explicitly established; apply DFM-1179 guidance."
        ),
    }


def classify_apple_package_shape(
    package_root: str | Path,
    profile: str = PROFILE_AUTO,
) -> dict[str, Any]:
    """Public metadata-only package classifier used by MCP and tests."""

    inventory = load_package_inventory(package_root)
    decision = classify_inventory(inventory, profile)
    return {
        "ok": True,
        "profile": decision.profile,
        "signals": list(decision.signals),
        "inventory_entries": len(inventory.entries),
        "package_byte_size": sum(entry.size for entry in inventory.entries if entry.kind == "file"),
        "content_trust": CONTENT_TRUST_LABEL,
        "safe_summary": (
            f"Classified a bounded local inventory as {decision.profile}; "
            "no file contents or identifiers are included in this response."
        ),
    }


def _entry_by_path(inventory: PackageInventory, relative_path: str) -> InventoryEntry:
    for entry in inventory.entries:
        if entry.relative_path == relative_path:
            return entry
    raise ValueError("inventory_entry_missing")


def _directory_size(inventory: PackageInventory, relative_path: str) -> int:
    prefix = relative_path.rstrip("/") + "/"
    return sum(
        entry.size
        for entry in inventory.entries
        if entry.kind == "file" and entry.relative_path.startswith(prefix)
    )


def _hash_entry(entry: InventoryEntry) -> tuple[str | None, str | None]:
    if entry.kind != "file" or entry.source_path is None or not entry.source_path.is_file():
        if entry.sha256:
            return entry.sha256, "digest_inventory_supplied_unverified"
        return None, "digest_unavailable"
    if entry.size > MAX_HASH_BYTES:
        if entry.sha256:
            return entry.sha256, "digest_inventory_supplied_unverified_oversized"
        return None, "digest_skipped_oversized"
    digest = hashlib.sha256()
    total = 0
    try:
        with entry.source_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                total += len(chunk)
                if total > MAX_HASH_BYTES:
                    # Re-check the actual bytes read rather than relying only
                    # on a potentially stale or inventory-supplied size.
                    return None, "digest_skipped_oversized"
                digest.update(chunk)
    except OSError:
        return None, "digest_unavailable"
    computed = digest.hexdigest()
    if entry.sha256 and entry.sha256 != computed:
        return None, "digest_mismatch"
    return computed, None


def _file_path_literal(
    entry: InventoryEntry,
    inventory: PackageInventory,
    *,
    shareable: bool,
) -> tuple[str, int]:
    if shareable:
        return _safe_literal(entry.relative_path, shareable=True, limit=1000)
    if entry.source_path is not None:
        return str(entry.source_path), 0
    if inventory.source_path is not None:
        return str(inventory.source_path.parent / entry.relative_path), 0
    return entry.relative_path, 0


def _file_facet(
    graph: _GraphBuilder,
    entry: InventoryEntry,
    inventory: PackageInventory,
    *,
    shareable: bool,
    size_override: int | None = None,
) -> tuple[dict[str, Any], int]:
    file_name, redactions_a = _safe_literal(
        PurePosixPath(entry.relative_path).name,
        shareable=shareable,
        limit=255,
    )
    file_path, redactions_b = _file_path_literal(entry, inventory, shareable=shareable)
    props: dict[str, Any] = {
        "uco-observable:fileName": [file_name],
        "uco-observable:filePath": [file_path],
    }
    if entry.kind == "directory":
        props["uco-observable:isDirectory"] = [
            {"@type": "xsd:boolean", "@value": "true"}
        ]
    size = entry.size if size_override is None else size_override
    if size:
        props["uco-observable:sizeInBytes"] = {
            "@type": "xsd:integer",
            "@value": str(size),
        }
    return graph.embedded("uco-observable:FileFacet", **props), redactions_a + redactions_b


def _content_hash_facet(graph: _GraphBuilder, digest: str) -> dict[str, Any]:
    hash_node = graph.embedded(
        "uco-types:Hash",
        **{
            "uco-types:hashMethod": "SHA256",
            "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": digest},
        },
    )
    return graph.embedded(
        "uco-observable:ContentDataFacet",
        **{"uco-observable:hash": [hash_node]},
    )


def _relationship(
    graph: _GraphBuilder,
    source: dict[str, Any],
    target: dict[str, Any],
    kind: str,
) -> dict[str, Any]:
    return graph.add(
        "uco-observable:ObservableRelationship",
        **{
            "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
            "uco-core:kindOfRelationship": kind,
            "uco-core:source": [graph.ref(source)],
            "uco-core:target": graph.ref(target),
        },
    )


def _candidate_entries(inventory: PackageInventory, predicate: Any) -> list[InventoryEntry]:
    return sorted((entry for entry in inventory.entries if predicate(entry)), key=lambda item: item.relative_path.casefold())


def _resolve_excerpt_entry(
    inventory: PackageInventory,
    event_excerpt_path: str | Path | None,
    max_event_records: int,
) -> InventoryEntry | None:
    if event_excerpt_path is not None:
        source = workspace_policy.check_read_path(event_excerpt_path)
        if not source.is_file():
            raise ValueError("event_excerpt_missing")
        suffix = source.suffix.lower()
        if suffix not in {".jsonl", ".csv"}:
            raise ValueError("event_excerpt_format_unsupported")
        try:
            relative = source.relative_to(inventory.source_path).as_posix() if inventory.source_path and inventory.source_path.is_dir() else source.name
        except ValueError:
            relative = f"external/{source.name}"
        return InventoryEntry(_normalize_relative_path(relative), "file", source.stat().st_size, source)

    metadata_path = inventory.metadata.get("event_excerpt_path")
    if isinstance(metadata_path, str) and metadata_path:
        relative = _normalize_relative_path(metadata_path)
        base = inventory.base_path or (
            inventory.source_path
            if inventory.source_path and inventory.source_path.is_dir()
            else inventory.source_path.parent
            if inventory.source_path
            else Path.cwd()
        )
        resolved_base = base.resolve()
        source = (resolved_base / relative).resolve()
        try:
            source.relative_to(resolved_base)
        except ValueError as exc:
            raise ValueError("event_excerpt_outside_package") from exc
        return _resolve_excerpt_entry(inventory, source, max_event_records)
    if max_event_records == 0:
        return None
    candidates = _candidate_entries(
        inventory,
        lambda entry: entry.kind == "file"
        and PurePosixPath(entry.relative_path).suffix.casefold() in {".jsonl", ".csv"}
        and any(token in entry.relative_path.casefold() for token in ("unified", "iterator", "syslog", "event")),
    )
    available = [entry for entry in candidates if entry.source_path is not None and entry.source_path.is_file()]
    if not available:
        raise ValueError("event_excerpt_required")
    if len(available) > 1:
        raise ValueError("ambiguous_event_excerpt")
    return available[0]


def _iter_bounded_text_lines(path: Path, *, strip_utf8_bom: bool = False) -> Iterator[str]:
    """Yield UTF-8 physical lines without ever allocating an oversized line."""

    scanned = 0
    try:
        with path.open("rb") as handle:
            first_line = True
            while True:
                raw_line = handle.readline(MAX_EVENT_LINE_BYTES + 1)
                if not raw_line:
                    break
                if len(raw_line) > MAX_EVENT_LINE_BYTES:
                    raise ValueError("event_excerpt_row_oversized")
                scanned += len(raw_line)
                if scanned > MAX_EVENT_SCAN_BYTES:
                    raise ValueError("event_excerpt_scan_limit_exceeded")
                line = raw_line.decode("utf-8", errors="strict")
                if first_line and strip_utf8_bom:
                    line = line.removeprefix("\ufeff")
                first_line = False
                yield line
    except (OSError, UnicodeError) as exc:
        raise ValueError("event_excerpt_unreadable") from exc


def _iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    for line in _iter_bounded_text_lines(path):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("event_excerpt_jsonl_invalid") from exc
        if not isinstance(row, dict):
            raise ValueError("event_excerpt_row_invalid")
        yield row


def _iter_csv(path: Path) -> Iterator[dict[str, Any]]:
    # csv.field_size_limit is process-global. Serialize CSV iteration so one
    # concurrent MCP request cannot relax another request's bound.
    with _CSV_FIELD_LIMIT_LOCK:
        previous_limit = csv.field_size_limit()
        csv.field_size_limit(MAX_EVENT_LINE_BYTES)
        try:
            reader = csv.DictReader(_iter_bounded_text_lines(path, strip_utf8_bom=True))
            if not reader.fieldnames:
                raise ValueError("event_excerpt_csv_invalid")
            for row in reader:
                estimated = sum(len(str(key)) + len(str(value or "")) for key, value in row.items())
                if estimated > MAX_EVENT_LINE_BYTES:
                    raise ValueError("event_excerpt_row_oversized")
                yield {str(key): value for key, value in row.items() if key is not None}
        except csv.Error as exc:
            raise ValueError("event_excerpt_csv_invalid") from exc
        except (OSError, UnicodeError) as exc:
            raise ValueError("event_excerpt_unreadable") from exc
        finally:
            csv.field_size_limit(previous_limit)


def _sample_event_rows(entry: InventoryEntry, maximum: int) -> tuple[list[dict[str, Any]], bool]:
    if maximum == 0:
        return [], False
    if entry.source_path is None:
        raise ValueError("event_excerpt_bytes_unavailable")
    iterator = _iter_jsonl(entry.source_path) if entry.source_path.suffix.lower() == ".jsonl" else _iter_csv(entry.source_path)
    rows: list[dict[str, Any]] = []
    truncated = False
    for row in iterator:
        if len(rows) >= maximum:
            truncated = True
            break
        rows.append(row)
    return rows, truncated


def _row_lookup(row: dict[str, Any], *keys: str) -> Any:
    normalized = {str(key).strip().casefold().replace(" ", "_"): value for key, value in row.items()}
    for key in keys:
        value = normalized.get(key.casefold())
        if value not in {None, ""}:
            return value
    return None


def _parse_anchored_timestamp(value: Any) -> str | None:
    if value in {None, ""}:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.isoformat()


def _graph_string_redaction_pass(document: dict[str, Any]) -> int:
    """Defense-in-depth redaction over every literal except JSON-LD identifiers."""

    count = 0

    def visit(value: Any, key: str | None = None) -> Any:
        nonlocal count
        if isinstance(value, dict):
            return {child_key: visit(child, child_key) for child_key, child in value.items()}
        if isinstance(value, list):
            return [visit(child, key) for child in value]
        if isinstance(value, str) and key not in {"@id", "@type"}:
            redacted, replacements = redact_identifiers(value)
            count += replacements
            return redacted
        return value

    replaced = visit(document)
    document.clear()
    document.update(replaced)
    return count


def build_acquisition_package_graph(
    package_root: str | Path,
    output_path: str | Path,
    profile: str = PROFILE_AUTO,
    max_event_records: int = 0,
    shareable: bool = True,
    event_excerpt_path: str | Path | None = None,
    event_message_policy: str = "omit",
    extensions: list[str] | None = None,
) -> BuildResult:
    """Build a bounded Apple package graph and write it to ``output_path``.

    ``package_root`` may be a local directory or an inventory JSON file.
    ``event_excerpt_path`` must be CSV/JSONL produced by an external decoder;
    binary logarchives are never decoded or embedded.  Absolute times are only
    asserted when the inventory explicitly sets ``metadata.timesync_anchored``.
    """

    if isinstance(max_event_records, bool) or not isinstance(max_event_records, int):
        raise ValueError("max_event_records_invalid")
    if max_event_records < 0 or max_event_records > MAX_EVENT_RECORDS:
        raise ValueError("max_event_records_out_of_range")
    message_policy = event_message_policy.strip().lower()
    if message_policy not in {"omit", "redact", "include"}:
        raise ValueError("event_message_policy_unsupported")
    if shareable and message_policy == "include":
        raise ValueError("shareable_message_policy_unsafe")
    extension_set = {item.strip().lower() for item in (extensions or ["solveit"]) if item.strip()}
    if "solveit" not in extension_set:
        raise ValueError("solveit_extension_required")

    output = workspace_policy.check_write_path(output_path)
    inventory = load_package_inventory(package_root)
    if inventory.source_path is not None:
        workspace_policy.check_distinct(inventory.source_path, output)
    decision = classify_inventory(inventory, profile)
    excerpt_entry = _resolve_excerpt_entry(inventory, event_excerpt_path, max_event_records)
    rows, rows_truncated = _sample_event_rows(excerpt_entry, max_event_records) if excerpt_entry else ([], False)

    graph = _GraphBuilder()
    redaction_count = 0
    messages_affected = 0
    warnings = list(inventory.warnings)
    digests: list[dict[str, str]] = []

    apple = graph.add("uco-identity:Identity", **{"uco-core:name": "Apple Inc."})
    device_raw = inventory.metadata.get("device")
    device_meta = cast(dict[str, Any], device_raw) if isinstance(device_raw, dict) else {}
    device_props: dict[str, Any] = {
        "uco-observable:manufacturer": graph.ref(apple),
        "uco-observable:deviceType": "Apple device",
    }
    if device_meta.get("model"):
        model_value, model_redactions = _safe_literal(device_meta["model"], shareable=shareable)
        redaction_count += model_redactions
        device_props["uco-observable:model"] = model_value
    if not shareable and device_meta.get("serial_number"):
        device_props["uco-observable:serialNumber"] = _bounded_string(device_meta["serial_number"])
    device = graph.add(
        "uco-observable:ObservableObject",
        **{
            "uco-core:name": "Apple device (identifiers omitted)" if shareable else "Apple acquisition source device",
            "uco-core:hasFacet": [graph.embedded("uco-observable:DeviceFacet", **device_props)],
            "uco-core:tag": ["share-safety:identifiers-redacted"] if shareable else None,
        },
    )

    os_raw = inventory.metadata.get("os")
    os_meta = cast(dict[str, Any], os_raw) if isinstance(os_raw, dict) else {}
    os_name, os_redactions = _safe_literal(os_meta.get("name", "Apple operating system"), shareable=shareable)
    redaction_count += os_redactions
    software_props: dict[str, Any] = {
        "uco-observable:manufacturer": graph.ref(apple),
    }
    os_version = ""
    if os_meta.get("version"):
        os_version, version_redactions = _safe_literal(os_meta["version"], shareable=shareable)
        redaction_count += version_redactions
        software_props["uco-observable:version"] = os_version
    operating_system = graph.add(
        ["uco-observable:OperatingSystem", "uco-observable:Software"],
        **{
            "uco-core:name": f"{os_name} ({os_version})" if os_version else os_name,
            "uco-core:description": ["OS identity is package metadata only; no device identifier is asserted."],
            "uco-core:hasFacet": [
                graph.embedded(
                    "uco-observable:SoftwareFacet",
                    **software_props,
                )
            ],
        },
    )
    relationships: list[dict[str, Any]] = [
        _relationship(graph, device, operating_system, "Characterized_By")
    ]

    root_entry = InventoryEntry(".", "directory", 0, inventory.source_path if inventory.source_path and inventory.source_path.is_dir() else None)
    root_facet, root_redactions = _file_facet(
        graph,
        root_entry,
        inventory,
        shareable=shareable,
        size_override=sum(entry.size for entry in inventory.entries if entry.kind == "file"),
    )
    redaction_count += root_redactions
    root_facet["uco-observable:fileName"] = ["package-root"]
    package_label = "iOS sysdiagnose package" if decision.profile == PROFILE_SYSDIAGNOSE else "Apple FOSS acquisition package"
    package_tags = ["hash-status:not-published"]
    if shareable:
        package_tags.extend([
            "share-safety:paths-normalized",
            "share-safety:identifiers-redacted",
            f"share-safety:messages-{message_policy}",
        ])
    package = graph.add(
        "uco-observable:ObservableObject",
        **{
            "uco-core:name": package_label if shareable else _bounded_string(inventory.root_name, 255),
            "uco-core:description": [
                "Bounded package-level inventory; binary archive bytes and full application identifiers are not embedded."
            ],
            "uco-core:hasFacet": [root_facet],
            "uco-core:tag": package_tags,
        },
    )
    relationships.append(_relationship(graph, package, device, "Extracted_From"))

    log_entry = _entry_by_path(inventory, decision.logarchive_path)
    log_size = _directory_size(inventory, log_entry.relative_path) if log_entry.kind == "directory" else log_entry.size
    log_facet, log_redactions = _file_facet(
        graph, log_entry, inventory, shareable=shareable, size_override=log_size
    )
    redaction_count += log_redactions
    logarchive = graph.add(
        ["solveit-observable:AppleUnifiedLogArchive", "uco-observable:EventLog"],
        **{
            "uco-core:name": "Apple Unified Log archive",
            "uco-core:description": [
                "Binary Unified Logging container inventoried by metadata only; .tracev3 bytes are not embedded."
            ],
            "uco-core:hasFacet": [log_facet],
            "uco-core:tag": ["hash-status:not-computed", "content-scope:metadata-only"],
        },
    )
    relationships.append(_relationship(graph, logarchive, package, "Contained_Within"))

    # Package-level ancillary containers.  Apps are deliberately represented as
    # one inventory file with a count, never one node per application identifier.
    crash_dirs = _candidate_entries(
        inventory,
        lambda entry: entry.kind == "directory"
        and PurePosixPath(entry.relative_path).name.casefold() in {"crashes", "crash", "crash_pull", "crashreports", "crashes_and_spins"},
    )
    crash_parent: dict[str, Any] | None = None
    if crash_dirs:
        crash_entry = crash_dirs[0]
        facet, count = _file_facet(
            graph,
            crash_entry,
            inventory,
            shareable=shareable,
            size_override=_directory_size(inventory, crash_entry.relative_path),
        )
        redaction_count += count
        crash_parent = graph.add(
            "uco-observable:ObservableObject",
            **{
                "uco-core:name": "Crash-report collection",
                "uco-core:hasFacet": [facet],
                "uco-core:tag": ["content-scope:sampled"],
            },
        )
        relationships.append(_relationship(graph, crash_parent, package, "Contained_Within"))

    crash_files = _candidate_entries(
        inventory,
        lambda entry: entry.kind == "file" and entry.relative_path.casefold().endswith(".ips"),
    )[:MAX_CRASH_SAMPLES]
    for index, crash_entry in enumerate(crash_files, start=1):
        digest, digest_warning = _hash_entry(crash_entry)
        facets, count = _file_facet(graph, crash_entry, inventory, shareable=shareable)
        redaction_count += count
        facet_list = [facets]
        tags = ["content-scope:metadata-only"]
        if digest:
            facet_list.append(_content_hash_facet(graph, digest))
            safe_name, name_redactions = _safe_literal(PurePosixPath(crash_entry.relative_path).name, shareable=shareable, limit=255)
            redaction_count += name_redactions
            digests.append({"artifact_role": f"crash-sample-{index}", "file_name": safe_name, "sha256": digest})
        else:
            tags.append("hash-status:not-computed")
        if digest_warning:
            warnings.append(f"crash_sample_{digest_warning}")
        crash_node = graph.add(
            "uco-observable:ObservableObject",
            **{
                "uco-core:name": f"Crash report sample {index}",
                "uco-core:hasFacet": facet_list,
                "uco-core:tag": tags,
            },
        )
        relationships.append(_relationship(graph, crash_node, crash_parent or package, "Contained_Within"))
    if len(_candidate_entries(inventory, lambda entry: entry.kind == "file" and entry.relative_path.casefold().endswith(".ips"))) > MAX_CRASH_SAMPLES:
        warnings.append("crash_reports_sampled")

    syslog_entries = _candidate_entries(
        inventory,
        lambda entry: entry.kind == "file" and "syslog" in PurePosixPath(entry.relative_path).name.casefold(),
    )
    if syslog_entries:
        facet, count = _file_facet(graph, syslog_entries[0], inventory, shareable=shareable)
        redaction_count += count
        syslog_node = graph.add(
            "uco-observable:ObservableObject",
            **{
                "uco-core:name": "Live syslog capture",
                "uco-core:hasFacet": [facet],
                "uco-core:tag": ["content-scope:metadata-only", "message-bodies:not-embedded"],
            },
        )
        relationships.append(_relationship(graph, syslog_node, package, "Contained_Within"))

    app_entries = _candidate_entries(
        inventory,
        lambda entry: entry.kind == "file"
        and any(token in PurePosixPath(entry.relative_path).name.casefold() for token in ("apps", "applications", "installed_app")),
    )
    if app_entries:
        app_entry = app_entries[0]
        app_count: int | None = None
        if app_entry.source_path and app_entry.size <= MAX_INVENTORY_BYTES:
            try:
                with app_entry.source_path.open("r", encoding="utf-8", errors="strict") as handle:
                    app_count = sum(1 for line in handle if line.strip())
            except (OSError, UnicodeError):
                warnings.append("application_count_unavailable")
        if app_count is None:
            reported_count = inventory.metadata.get("application_count")
            if (
                isinstance(reported_count, int)
                and not isinstance(reported_count, bool)
                and reported_count >= 0
            ):
                app_count = reported_count
                warnings.append("application_count_inventory_supplied_unverified")
        facet, count = _file_facet(graph, app_entry, inventory, shareable=shareable)
        redaction_count += count
        description = "Application identifiers remain in the external inventory and are not embedded."
        if app_count is not None:
            description = f"External application inventory contains {app_count} non-empty entries; identifiers are not embedded."
        apps_node = graph.add(
            "uco-observable:ObservableObject",
            **{
                "uco-core:name": "Installed-application inventory",
                "uco-core:description": [description],
                "uco-core:hasFacet": [facet],
                "uco-core:tag": ["content-scope:count-only"],
            },
        )
        relationships.append(_relationship(graph, apps_node, package, "Contained_Within"))

    excerpt_node: dict[str, Any] | None = None
    if excerpt_entry is not None:
        excerpt_digest, digest_warning = _hash_entry(excerpt_entry)
        facet, count = _file_facet(graph, excerpt_entry, inventory, shareable=shareable)
        redaction_count += count
        facets = [facet]
        tags = ["content-scope:external-excerpt"]
        if excerpt_digest:
            facets.append(_content_hash_facet(graph, excerpt_digest))
            safe_name, name_redactions = _safe_literal(PurePosixPath(excerpt_entry.relative_path).name, shareable=shareable, limit=255)
            redaction_count += name_redactions
            digests.append({"artifact_role": "event-excerpt", "file_name": safe_name, "sha256": excerpt_digest})
        else:
            tags.append("hash-status:not-computed")
        if digest_warning:
            warnings.append(f"event_excerpt_{digest_warning}")
        excerpt_node = graph.add(
            "uco-observable:ObservableObject",
            **{
                "uco-core:name": "Decoded event excerpt",
                "uco-core:description": [
                    "External CSV/JSONL decoder output; the graph contains only the configured bounded sample."
                ],
                "uco-core:hasFacet": facets,
                "uco-core:tag": tags,
            },
        )
        relationships.append(_relationship(graph, excerpt_node, package, "Contained_Within"))

    timesync_present = inventory.metadata.get("timesync_present") is True or any(
        any("timesync" in part for part in _path_parts(entry))
        for entry in inventory.entries
    )
    # Only the JSON boolean true is an affirmative forensic assertion. Values
    # such as the strings "false" or "yes" remain untrusted metadata.
    timesync_anchored = inventory.metadata.get("timesync_anchored") is True
    if not timesync_present:
        warnings.append("timesync_missing_absolute_time_omitted")
    elif not timesync_anchored:
        warnings.append("timesync_not_confirmed_absolute_time_omitted")

    event_records: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    dictionary_keys = (
        "subsystem", "category", "process", "pid", "thread_id", "library",
        "activity_id", "mach_continuous_time", "boot_uuid", "timezone_name",
        "timestamp_tool", "log_type", "event_type",
    )
    for index, row in enumerate(rows, start=1):
        service_raw = _row_lookup(row, "subsystem", "service", "event_record_service_name") or "service not asserted"
        event_type_raw = _row_lookup(row, "log_type", "event_type", "type") or "unifiedlog"
        service, count_a = _safe_literal(service_raw, shareable=shareable)
        event_type, count_b = _safe_literal(event_type_raw, shareable=shareable)
        redaction_count += count_a + count_b
        facet_props: dict[str, Any] = {
            "uco-observable:eventRecordID": f"excerpt-row-{index}",
            "uco-observable:eventType": event_type,
            "uco-observable:eventRecordServiceName": service,
            "uco-observable:eventRecordDevice": graph.ref(device),
        }
        message = _row_lookup(row, "message", "event_record_text", "eventrecordtext")
        if message not in {None, ""}:
            messages_affected += 1
            if message_policy == "redact":
                facet_props["uco-observable:eventRecordText"] = "[REDACTED:message]"
            elif message_policy == "include":
                safe_message, message_redactions = _safe_literal(message, shareable=False)
                redaction_count += message_redactions
                facet_props["uco-observable:eventRecordText"] = safe_message
        timestamp_raw = _row_lookup(row, "timestamp", "timestamp_tool", "datetime", "date_time")
        anchored_timestamp = _parse_anchored_timestamp(timestamp_raw) if timesync_anchored else None
        if anchored_timestamp:
            typed_time = {"@type": "xsd:dateTime", "@value": anchored_timestamp}
            facet_props["uco-observable:observableCreatedTime"] = typed_time
            facet_props["uco-observable:startTime"] = typed_time
        record = graph.add(
            "uco-observable:EventRecord",
            **{
                "uco-core:name": f"Decoded event excerpt row {index}",
                "uco-core:description": [
                    "Absolute time is timesync-anchored." if anchored_timestamp else
                    "Absolute device time omitted; use retained continuous-time/timesync evidence for correlation."
                ],
                "uco-core:hasFacet": [graph.embedded("uco-observable:EventRecordFacet", **facet_props)],
                "uco-core:tag": [f"share-safety:message-{message_policy}"] if shareable else None,
            },
        )
        if excerpt_node is not None:
            relationships.append(_relationship(graph, record, excerpt_node, "Contained_Within"))
        relationships.append(_relationship(graph, record, logarchive, "Extracted_From"))

        entries: list[dict[str, Any]] = []
        for key in dictionary_keys:
            value = _row_lookup(row, key)
            if value in {None, ""}:
                continue
            safe_value, replacements = _safe_literal(value, shareable=shareable)
            redaction_count += replacements
            entries.append(
                graph.embedded(
                    "uco-types:DictionaryEntry",
                    **{"uco-types:key": key, "uco-types:value": safe_value},
                )
            )
        if timestamp_raw not in {None, ""} and not any(item.get("uco-types:key") == "timestamp_tool" for item in entries):
            safe_timestamp, replacements = _safe_literal(timestamp_raw, shareable=shareable)
            redaction_count += replacements
            entries.append(
                graph.embedded(
                    "uco-types:DictionaryEntry",
                    **{"uco-types:key": "timestamp_tool", "uco-types:value": safe_timestamp},
                )
            )
        event_props: dict[str, Any] = {
            "uco-core:name": f"Decoded unified-log event {index}",
            "uco-core:description": [
                "Absolute device time omitted because timesync anchoring was not established."
                if not anchored_timestamp else "Absolute time asserted from explicitly anchored decoder metadata."
            ],
            "uco-core:eventType": ["unifiedlog", event_type],
            "uco-core:eventContext": [graph.ref(record), graph.ref(device)],
        }
        if entries:
            event_props["uco-core:eventAttribute"] = [
                graph.embedded("uco-types:Dictionary", **{"uco-types:entry": entries})
            ]
        if anchored_timestamp:
            event_props["uco-core:startTime"] = [
                {"@type": "xsd:dateTime", "@value": anchored_timestamp}
            ]
        event = graph.add("uco-core:Event", **event_props)
        event_records.append(record)
        events.append(event)

    collect_action = graph.add(
        "solveit-core:SolveitInvestigativeAction",
        **{
            "uco-core:name": "Preserve Apple acquisition package inventory",
            "uco-core:description": [
                "SOLVE-IT DFT-1016 package-level collection record; acquisition tool and exact time are not asserted without inventory evidence."
            ],
            "uco-action:object": [graph.ref(device)],
            "uco-action:result": [graph.ref(package), graph.ref(logarchive)],
            "solveit-core:usedTechnique": [
                {"@id": SOLVEIT_DATA + "techniqueDFT-1016"}
            ],
        },
    )
    actions = [collect_action]
    if excerpt_node is not None:
        parse_action = graph.add(
            "solveit-core:SolveitInvestigativeAction",
            **{
                "uco-core:name": "Sample external Apple log decoder excerpt",
                "uco-core:description": [
                    "SOLVE-IT DFT-1066/DFT-1076; decoder identity and run time are not asserted unless separately documented. DFM-1179 timesync guidance applied."
                ],
                "uco-action:object": [graph.ref(logarchive)],
                "uco-action:result": [graph.ref(excerpt_node), *[graph.ref(item) for item in event_records], *[graph.ref(item) for item in events]],
                "solveit-core:usedTechnique": [
                    {"@id": SOLVEIT_DATA + "techniqueDFT-1066"},
                    {"@id": SOLVEIT_DATA + "techniqueDFT-1076"},
                ],
                "solveit-core:appliedMitigation": [
                    {"@id": SOLVEIT_DATA + "mitigationDFM-1179"}
                ],
            },
        )
        actions.append(parse_action)

    provenance_objects = [*actions, package, logarchive]
    if excerpt_node is not None:
        provenance_objects.append(excerpt_node)
    provenance = graph.add(
        "case-investigation:ProvenanceRecord",
        **{
            "uco-core:description": [
                "Bounded Apple acquisition package graph; source content remains external."
            ],
            "uco-core:object": [graph.ref(item) for item in provenance_objects],
        },
    )

    investigation_objects = [
        apple, device, operating_system, package, logarchive,
        *event_records, *events, *actions, provenance, *relationships,
    ]
    if excerpt_node is not None:
        investigation_objects.append(excerpt_node)
    graph.add(
        "case-investigation:Investigation",
        **{
            "uco-core:name": f"{package_label} examination",
            "uco-core:description": [
                "Package-level CASE/UCO graph with bounded metadata and optional event excerpts; full logarchive expansion is intentionally excluded."
            ],
            "uco-core:tag": package_tags if shareable else ["content-scope:package-level"],
            "uco-core:object": [graph.ref(item) for item in investigation_objects],
        },
    )

    if rows_truncated:
        warnings.append("event_excerpt_sample_truncated")
    if max_event_records == 0:
        warnings.append("event_records_not_sampled")
    if message_policy == "omit" and messages_affected:
        warnings.append("event_messages_omitted")
    elif message_policy == "redact" and messages_affected:
        warnings.append("event_messages_redacted")

    document: dict[str, Any] = {"@context": _CONTEXT, "@graph": graph.nodes}
    if shareable:
        redaction_count += _graph_string_redaction_pass(document)
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, output)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return BuildResult(
        output_path=output,
        profile=decision.profile,
        node_count=len(graph.nodes),
        event_record_count=len(event_records),
        inventory_entry_count=len(inventory.entries),
        package_byte_size=sum(entry.size for entry in inventory.entries if entry.kind == "file"),
        named_file_digests=tuple(digests),
        shareable=shareable,
        identifiers_redacted=redaction_count,
        messages_affected=messages_affected,
        event_message_policy=message_policy,
        warnings=tuple(sorted(set(warnings))),
    )
