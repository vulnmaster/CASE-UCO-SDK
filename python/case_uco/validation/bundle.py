"""Profile-aware validation bundle planner (#68).

Resolves a deterministic, offline ontology/profile bundle from stable
extension names and upper-ontology profile IDs. SHACL validation and
strict concept coverage must consume the **same** resolved resources and
fingerprint (CQ-27–CQ-36).
"""

from __future__ import annotations

import os
import hashlib
import json
import os
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from case_uco.validation.graph import (
    PROJECT_ROOT,
    load_extension_ontology_paths,
    resolve_extension_dependencies,
)

RESOLVER_SCHEMA_VERSION = "1.0"

# Stable profile IDs → vendored source + CDO-Shapes paths.
PROFILE_REGISTRY: dict[str, dict[str, Any]] = {
    "bfo": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/bfo",
        "sources": ["ontology/upper/bfo.owl"],
        "shapes": ["ontology/upper/shapes/sh-bfo.ttl"],
        "depends_on": [],
        "incompatible_with": ["gufo"],
        "extension_policy": {"cac": "not_recommended"},
        "inference": "rdfs",
    },
    "gufo": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/gufo",
        "sources": ["ontology/upper/gufo.ttl"],
        "shapes": ["ontology/upper/shapes/sh-gufo.ttl"],
        "depends_on": [],
        "incompatible_with": ["bfo"],
        "extension_policy": {"cac": "included"},
        "inference": "rdfs",
    },
    "prov-o": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/prov-o",
        "sources": ["ontology/upper/prov-o.ttl"],
        "shapes": ["ontology/upper/shapes/sh-prov-o.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "time": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/owl-time",
        "sources": ["ontology/upper/time.ttl"],
        "shapes": ["ontology/upper/shapes/sh-time.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "owl-time": {  # alias
        "alias_of": "time",
    },
    "geosparql": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/geosparql",
        "sources": ["ontology/upper/geo.ttl", "ontology/upper/sf.ttl"],
        "shapes": ["ontology/upper/shapes/sh-geo.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "foaf": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/foaf",
        "sources": ["ontology/upper/foaf.rdf"],
        "shapes": ["ontology/upper/shapes/sh-foaf.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "org": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/org",
        "sources": ["ontology/upper/org.ttl"],
        "shapes": ["ontology/upper/shapes/sh-org.ttl"],
        # Offline import closure from sh-org.ttl (FOAF + PROV-O shapes;
        # SKOS is covered by standard RDF namespaces).
        "depends_on": ["foaf", "prov-o"],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "prof": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/prof",
        "sources": ["ontology/upper/prof.ttl"],
        "shapes": ["ontology/upper/shapes/sh-prof.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    # SDK-pinned ontologies without a CDO-Shapes profile (#60). Only the QUDT
    # schema joins the SHACL run; unit and quantity-kind IRIs are checked
    # against the term registry by concept coverage.
    "qudt": {
        "canonical_id": "urn:case-uco-sdk:profile:qudt",
        "sources": ["ontology/upper/qudt-schema.ttl"],
        "shapes": ["ontology/upper/sdk-shapes/sh-qudt-sdk.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "sosa": {
        "canonical_id": "urn:case-uco-sdk:profile:sosa",
        "sources": ["ontology/upper/sosa.ttl"],
        "shapes": ["ontology/upper/sdk-shapes/sh-sosa-sdk.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "ssn": {
        "canonical_id": "urn:case-uco-sdk:profile:ssn",
        "sources": ["ontology/upper/ssn.ttl", "ontology/upper/ssn-systems.ttl"],
        "shapes": [],
        # SSN imports SOSA.
        "depends_on": ["sosa"],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
}

# Foundational profiles that must not be selected together without an
# explicit allow_foundational_pair=True override.
FOUNDATIONAL_EXCLUSIVE = frozenset({"bfo", "gufo"})

# Inference escalation order (deterministic combine across profiles).
_INFERENCE_RANK = {None: 0, "none": 0, "rdfs": 1, "owlrl": 2, "both": 3}

_BUNDLE_CACHE: dict[str, "ResolvedValidationBundle"] = {}
_CACHE_MAX = 32
_BUNDLE_CACHE_LOCK = threading.RLock()


class ValidationBundleError(ValueError):
    """Typed fail-closed error for profile/extension bundle resolution."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class BundleResource:
    role: str  # ontology | shapes | bridge | auxiliary
    path: str  # repository-relative
    absolute_path: str
    sha256: str
    profile_id: str | None = None
    extension: str | None = None


@dataclass(frozen=True)
class ResolvedValidationBundle:
    extensions: tuple[str, ...]
    profiles: tuple[str, ...]  # normalized (aliases resolved + depends_on closure)
    resources: tuple[BundleResource, ...]
    inference: str | None
    compatibility_notes: tuple[str, ...]
    fingerprint: str
    built_version: str = "case-1.5.0"
    requested_profiles: tuple[str, ...] = ()  # as supplied by the caller (pre-normalize)
    cache_status: str = "miss"  # hit | miss | stale | disabled
    resolver_schema_version: str = RESOLVER_SCHEMA_VERSION

    def ontology_graph_paths(self) -> list[Path]:
        return [Path(r.absolute_path) for r in self.resources]

    def declared_term_paths(self) -> list[Path]:
        """Ontology/shapes/bridge/auxiliary paths used for concept coverage."""
        return [
            Path(r.absolute_path)
            for r in self.resources
            if r.role in {"ontology", "shapes", "bridge", "auxiliary"}
        ]

    def to_manifest(self, *, portable: bool = True) -> dict[str, Any]:
        resources = []
        for r in self.resources:
            entry = {
                "role": r.role,
                "path": r.path,
                "sha256": r.sha256,
                "profile_id": r.profile_id,
                "extension": r.extension,
            }
            if not portable:
                entry["absolute_path"] = r.absolute_path
            resources.append(entry)
        return {
            "resolver_schema_version": self.resolver_schema_version,
            "built_version": self.built_version,
            "requested_profiles": list(self.requested_profiles),
            "extensions": list(self.extensions),
            "profiles": list(self.profiles),
            "inference": self.inference,
            "compatibility_notes": list(self.compatibility_notes),
            "fingerprint": self.fingerprint,
            "resources": resources,
        }

    def write_manifest(self, path: str | Path) -> None:
        """Atomically write a portable JSON manifest (no absolute paths)."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.to_manifest(portable=True), indent=2, sort_keys=True) + "\n"
        fd, tmp_name = tempfile.mkstemp(
            dir=str(target.parent),
            prefix=f".{target.name}.",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            Path(tmp_name).replace(target)
        except Exception:
            try:
                os.unlink(tmp_name)
            except OSError:
                # Best-effort cleanup of the staging file after a failed write.
                pass
            raise


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalize_profile_id(profile_id: str) -> str:
    entry = PROFILE_REGISTRY.get(profile_id)
    if entry is None:
        raise ValidationBundleError("unknown_profile", f"Unknown profile id {profile_id!r}")
    if "alias_of" in entry:
        alias = entry["alias_of"]
        if not isinstance(alias, str):
            raise ValidationBundleError(
                "unknown_profile", f"Invalid alias for profile id {profile_id!r}"
            )
        return alias
    return profile_id


def list_profile_ids() -> list[str]:
    return sorted(pid for pid, meta in PROFILE_REGISTRY.items() if "alias_of" not in meta)


def _canonical_cache_key(
    extensions: list[str],
    profiles: list[str],
    *,
    allow_foundational_pair: bool,
    extra_ontology_graphs: list[str | Path] | None,
    project_root: Path,
) -> str:
    """Normalize aliases and sort set-like inputs for stable cache keys (CQ-33)."""
    norm_profiles = sorted({_normalize_profile_id(p) for p in profiles})
    # Preserve :full / named-subset suffixes; sort by clean name for stability.
    from case_uco.validation.graph import parse_extension_token

    norm_ext = sorted(extensions, key=lambda e: parse_extension_token(e))
    extras = sorted(str(Path(p).resolve()) for p in (extra_ontology_graphs or []))
    return json.dumps(
        {
            "ext": norm_ext,
            "prof": norm_profiles,
            "pair": allow_foundational_pair,
            "extra": extras,
            "root": str(project_root.resolve()),
            "schema": RESOLVER_SCHEMA_VERSION,
        },
        sort_keys=True,
    )


def _expand_profile_dependencies(
    seed_profiles: list[str],
) -> tuple[list[str], list[str]]:
    """Transitive depends_on with cycle detection (CQ-34).

    Returns ``(ordered_profiles, notes)``. Order is deterministic: BFS from
    the seed list (already sorted by the caller for cache stability) with
    dependencies appended in registry declaration order.
    """
    notes: list[str] = []
    resolved: list[str] = []
    seen: set[str] = set()
    # (profile_id, dependency chain from the requesting root)
    queue: list[tuple[str, tuple[str, ...]]] = [(pid, ()) for pid in seed_profiles]
    while queue:
        pid, chain = queue.pop(0)
        if pid in chain:
            cycle = " → ".join(chain + (pid,))
            raise ValidationBundleError(
                "profile_dependency_cycle",
                f"Circular profile depends_on: {cycle}",
            )
        if pid in seen:
            continue
        seen.add(pid)
        resolved.append(pid)
        meta = PROFILE_REGISTRY[pid]
        for dep in meta.get("depends_on", []):
            dep_norm = _normalize_profile_id(dep)
            next_chain = chain + (pid,)
            if dep_norm in next_chain:
                cycle = " → ".join(next_chain + (dep_norm,))
                raise ValidationBundleError(
                    "profile_dependency_cycle",
                    f"Circular profile depends_on: {cycle}",
                )
            notes.append(f"Profile {pid!r} depends_on {dep_norm!r}")
            if dep_norm not in seen:
                queue.append((dep_norm, next_chain))
    return resolved, notes


def _enforce_incompatible_with(profiles: list[str]) -> None:
    selected = set(profiles)
    for pid in profiles:
        meta = PROFILE_REGISTRY[pid]
        for other in meta.get("incompatible_with", []):
            other_norm = _normalize_profile_id(other)
            if other_norm in selected:
                raise ValidationBundleError(
                    "incompatible_profiles",
                    f"Profile {pid!r} is incompatible_with {other_norm!r}",
                )


def _combine_inference(
    profiles: list[str],
    expanded_ext: list[str],
    *,
    project_root: Path = PROJECT_ROOT,
) -> str | None:
    """Deterministically combine per-profile inference requirements (CQ-34).

    Matches ``extension_ontology_args``: skip rdfs only when at least one
    extension actually loads via ``validation-subset.json``. A ``:full``
    root with subset-mode dependencies still gets rdfs.
    """
    from case_uco.validation.graph import extension_has_validation_subset

    rank = 0
    chosen: str | None = None
    for pid in profiles:
        meta = PROFILE_REGISTRY[pid]
        inf = meta.get("inference")
        if inf is None:
            continue
        r = _INFERENCE_RANK.get(inf, 0)
        if r > rank:
            rank = r
            chosen = None if inf in (None, "none") else inf
    if profiles:
        return chosen or "rdfs"
    used_subset = False
    from case_uco.validation.graph import parse_extension_token

    for ext_name in expanded_ext:
        clean, mode = parse_extension_token(ext_name)
        if mode != "full" and (
            mode != "subset" or extension_has_validation_subset(clean, project_root)
        ):
            used_subset = True
            break
    if used_subset:
        return None
    if expanded_ext:
        return "rdfs"
    return None


def resolve_validation_bundle(
    extensions: list[str] | None = None,
    profiles: list[str] | None = None,
    *,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
    allow_foundational_pair: bool = False,
    extra_ontology_graphs: list[str | Path] | None = None,
    use_cache: bool = True,
) -> ResolvedValidationBundle:
    """Resolve extension + profile ontology graphs into one fingerprinted bundle."""
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    extensions = list(extensions or [])
    profiles = list(profiles or [])
    requested_profiles = tuple(profiles)

    if not use_cache:
        bundle = _build_bundle(
            extensions=extensions,
            profiles=profiles,
            requested_profiles=requested_profiles,
            project_root=project_root,
            allow_foundational_pair=allow_foundational_pair,
            extra_ontology_graphs=extra_ontology_graphs,
            cache_status="disabled",
        )
        return bundle

    cache_key = _canonical_cache_key(
        extensions,
        profiles,
        allow_foundational_pair=allow_foundational_pair,
        extra_ontology_graphs=extra_ontology_graphs,
        project_root=project_root,
    )

    with _BUNDLE_CACHE_LOCK:
        cached = _BUNDLE_CACHE.get(cache_key)
        if cached is not None:
            try:
                for resource in cached.resources:
                    path = Path(resource.absolute_path)
                    if not path.exists() or _sha256_file(path) != resource.sha256:
                        del _BUNDLE_CACHE[cache_key]
                        # Fall through to rebuild; mark stale.
                        break
                else:
                    return ResolvedValidationBundle(
                        extensions=cached.extensions,
                        profiles=cached.profiles,
                        resources=cached.resources,
                        inference=cached.inference,
                        compatibility_notes=cached.compatibility_notes,
                        fingerprint=cached.fingerprint,
                        built_version=cached.built_version,
                        requested_profiles=cached.requested_profiles,
                        cache_status="hit",
                        resolver_schema_version=cached.resolver_schema_version,
                    )
            except KeyError:
                # Cache entry shape drifted (partial/corrupt); rebuild below.
                pass
            # Reaching here means stale invalidation occurred.
            stale_rebuild = True
        else:
            stale_rebuild = False

        bundle = _build_bundle(
            extensions=extensions,
            profiles=profiles,
            requested_profiles=requested_profiles,
            project_root=project_root,
            allow_foundational_pair=allow_foundational_pair,
            extra_ontology_graphs=extra_ontology_graphs,
            cache_status="stale" if stale_rebuild else "miss",
        )
        if len(_BUNDLE_CACHE) >= _CACHE_MAX:
            _BUNDLE_CACHE.pop(next(iter(_BUNDLE_CACHE)))
        # Store without ephemeral cache_status so hits re-stamp cleanly.
        _BUNDLE_CACHE[cache_key] = ResolvedValidationBundle(
            extensions=bundle.extensions,
            profiles=bundle.profiles,
            resources=bundle.resources,
            inference=bundle.inference,
            compatibility_notes=bundle.compatibility_notes,
            fingerprint=bundle.fingerprint,
            built_version=bundle.built_version,
            requested_profiles=bundle.requested_profiles,
            cache_status="miss",
            resolver_schema_version=bundle.resolver_schema_version,
        )
        return bundle


def _build_bundle(
    *,
    extensions: list[str],
    profiles: list[str],
    requested_profiles: tuple[str, ...],
    project_root: Path,
    allow_foundational_pair: bool,
    extra_ontology_graphs: list[str | Path] | None,
    cache_status: str,
) -> ResolvedValidationBundle:
    notes: list[str] = []
    # Normalize aliases first; sort for deterministic depends_on expansion.
    seed = sorted({_normalize_profile_id(pid) for pid in profiles})
    normalized_profiles, dep_notes = _expand_profile_dependencies(seed)
    notes.extend(dep_notes)

    foundational = [p for p in normalized_profiles if p in FOUNDATIONAL_EXCLUSIVE]
    if len(set(foundational)) > 1 and not allow_foundational_pair:
        raise ValidationBundleError(
            "incompatible_profiles",
            "BFO and gUFO are alternative foundational profiles; select one, "
            "or pass allow_foundational_pair=True with an explicit rationale "
            "and a dedicated compatibility fixture.",
        )
    if len(set(foundational)) > 1 and allow_foundational_pair:
        notes.append(
            "allow_foundational_pair=True: BFO and gUFO co-selected; "
            "caller must supply a compatibility fixture."
        )
    else:
        _enforce_incompatible_with(normalized_profiles)

    expanded_ext = resolve_extension_dependencies(extensions, project_root) if extensions else []

    for pid in normalized_profiles:
        meta = PROFILE_REGISTRY[pid]
        from case_uco.validation.graph import parse_extension_token

        for ext in expanded_ext:
            clean, _mode = parse_extension_token(ext)
            policy = meta.get("extension_policy", {}).get(clean)
            if policy == "not_recommended":
                notes.append(
                    f"Profile {pid!r} is marked not_recommended with extension {clean!r}"
                )
                raise ValidationBundleError(
                    "incompatible_extension_profile",
                    f"Profile {pid!r} is not_recommended with extension {clean!r}. "
                    f"Choose gUFO for CAC graphs, or omit the foundational profile.",
                )
            if policy == "included":
                notes.append(f"Profile {pid!r} is included/compatible with {clean!r}")

    resources: list[BundleResource] = []
    seen_abs: set[str] = set()

    def _add(
        path: Path,
        role: str,
        *,
        profile_id: str | None = None,
        extension: str | None = None,
    ) -> None:
        if not path.exists():
            raise ValidationBundleError(
                "missing_resource",
                f"Required ontology/shape file missing: {path}",
            )
        abs_s = str(path.resolve())
        if abs_s in seen_abs:
            return
        seen_abs.add(abs_s)
        try:
            rel = str(path.resolve().relative_to(project_root.resolve()))
        except ValueError:
            # Non-portable absolute fallback only for out-of-tree extras;
            # portable manifests still omit absolute_path.
            rel = path.name
        resources.append(
            BundleResource(
                role=role,
                path=rel,
                absolute_path=abs_s,
                sha256=_sha256_file(path),
                profile_id=profile_id,
                extension=extension,
            )
        )

    from case_uco.validation.graph import parse_extension_token

    for ext_name in expanded_ext:
        clean, mode = parse_extension_token(ext_name)
        for full in load_extension_ontology_paths(clean, mode=mode, project_root=project_root):
            role = "shapes" if "shape" in full.name.lower() else "ontology"
            if "bridge" in full.name.lower():
                role = "bridge"
            _add(full, role, extension=clean)

    for pid in normalized_profiles:
        meta = PROFILE_REGISTRY[pid]
        for rel in meta.get("sources", []):
            _add(project_root / rel, "ontology", profile_id=pid)
        for rel in meta.get("shapes", []):
            _add(project_root / rel, "shapes", profile_id=pid)

    for extra in extra_ontology_graphs or []:
        _add(Path(extra), "auxiliary")

    inference = _combine_inference(
        normalized_profiles, expanded_ext, project_root=project_root
    )

    fingerprint_material = json.dumps(
        [
            {
                "path": r.path,
                "sha256": r.sha256,
                "role": r.role,
                "profile": r.profile_id,
                "ext": r.extension,
            }
            for r in resources
        ],
        sort_keys=True,
    ).encode()
    fingerprint = hashlib.sha256(fingerprint_material).hexdigest()

    return ResolvedValidationBundle(
        extensions=tuple(expanded_ext),
        profiles=tuple(normalized_profiles),
        resources=tuple(resources),
        inference=inference,
        compatibility_notes=tuple(notes),
        fingerprint=fingerprint,
        requested_profiles=requested_profiles,
        cache_status=cache_status,
        resolver_schema_version=RESOLVER_SCHEMA_VERSION,
    )


def clear_bundle_cache() -> None:
    with _BUNDLE_CACHE_LOCK:
        _BUNDLE_CACHE.clear()


def hash_validation_bundle_identity(
    *,
    extensions: list[str] | None = None,
    profiles: list[str] | None = None,
    extra_ontology_graphs: list[str | Path] | None = None,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
    force_rdfs_inference: bool = False,
    use_cache: bool = False,
) -> dict[str, Any]:
    """Resolve a validation bundle from disk and return identity fields.

    Defaults to ``use_cache=False`` so callers that reverify at finalization
    always rehash selected ontology/shapes/bridge/auxiliary resources.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    bundle = resolve_validation_bundle(
        extensions=list(extensions or []),
        profiles=list(profiles or []),
        project_root=project_root,
        extra_ontology_graphs=extra_ontology_graphs,
        use_cache=use_cache,
    )
    inference = bundle.inference
    if not inference and force_rdfs_inference:
        inference = "rdfs"
    try:
        import importlib.metadata as metadata

        validator_version: str | None = metadata.version("case-utils")
    except Exception:  # noqa: BLE001
        validator_version = None
    return {
        "bundle_fingerprint": bundle.fingerprint,
        "bundle_resource_hashes": {r.path: r.sha256 for r in bundle.resources},
        "bundle_resources": list(bundle.to_manifest(portable=True)["resources"]),
        "inference": inference,
        "resolver_schema_version": bundle.resolver_schema_version,
        "built_version": bundle.built_version,
        "validator_version": validator_version,
        "extensions": list(bundle.extensions),
        "extension_versions": _extension_versions(bundle.extensions, project_root),
        "profiles": list(bundle.profiles),
    }


def _extension_versions(extensions: tuple[str, ...], project_root: Path) -> dict[str, str | None]:
    """Manifest ``version`` of each selected extension (None when unreadable)."""
    from case_uco.validation.extension_paths import find_extension_dir
    from case_uco.validation.graph import parse_extension_token

    versions: dict[str, str | None] = {}
    for token in extensions:
        name, _mode = parse_extension_token(token)
        ext_dir = find_extension_dir(name, project_root)
        version = None
        if ext_dir is not None:
            try:
                version = json.loads((ext_dir / "manifest.json").read_text(encoding="utf-8")).get("version")
            except (OSError, json.JSONDecodeError, AttributeError):
                version = None
        versions[name] = version
    return versions

__all__ = [
    "FOUNDATIONAL_EXCLUSIVE",
    "PROFILE_REGISTRY",
    "RESOLVER_SCHEMA_VERSION",
    "BundleResource",
    "ResolvedValidationBundle",
    "ValidationBundleError",
    "_normalize_profile_id",
    "clear_bundle_cache",
    "hash_validation_bundle_identity",
    "list_profile_ids",
    "resolve_validation_bundle",
]
