"""SHACL validation wrapper around the CASE Utilities ``case_validate`` CLI.

Gives MCP callers (AI agents, review tools, scripts) a bounded way to validate a
produced CASE/UCO graph file before it is submitted for human review. The
wrapper invokes the locally installed ``case_validate`` tool with an argument
array (no shell), parses its conformance report, and fails honestly with
typed errors when the validator or the graph file is unavailable.

This module never fabricates validation results: if ``case_validate`` is not
installed, callers receive ``validator_unavailable`` instead of a fake pass.
"""

from __future__ import annotations

import os
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from case_uco.validation.runtime import (
    ValidatorError,
    prepare_validator,
    validator_available,
    validator_error_code,
    validator_error_message,
)
from case_uco.validation.extension_paths import extension_dir as _extension_dir
from case_uco.validation.extension_paths import find_extension_dir as _find_extension_dir


def _discover_project_root() -> Path:
    """Locate the monorepo root that holds ``extensions/`` and ``ontology/``."""
    here = Path(__file__).resolve()
    candidates = [
        here.parents[3],  # .../CASE-UCO-Libraries from case_uco/validation/
        here.parents[2],
        Path.cwd(),
        *here.parents,
    ]
    for candidate in candidates:
        if (candidate / "extensions").is_dir() and (
            (candidate / "ontology").is_dir() or (candidate / "ontology").exists()
        ):
            return candidate
    return here.parents[3]


PROJECT_ROOT = _discover_project_root()
DEFAULT_BUILT_VERSION = "case-1.5.0"

VALIDATOR_NAME = "case_validate"
SUPPORTED_GRAPH_EXTENSIONS = {".json", ".jsonld", ".json-ld", ".ttl", ".turtle"}
MAX_GRAPH_BYTES = 50 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 180

# Markers shared with downstream validation-result parsers so both sides of
# the roundtrip report the same conformance semantics.
_CONFORMS_KEY = "conforms"
_VIOLATION_MARKER = "Constraint Violation"
_WARNING_MARKER = "NonExistentCDOConceptWarning"


@dataclass(frozen=True)
class GraphValidationReport:
    """Structured, redaction-safe validation result.

    ``verification_status`` is ``"complete"`` only when every required
    stage (SHACL plus, when enabled, strict concept coverage including the
    pinned upper-ontology registry) actually ran; otherwise it is
    ``"could_not_verify"`` and ``conforms`` is never ``True`` (fail-closed,
    issue #55).

    Independent stage reporting (CQ-36): ``stage_status`` lists
    ``bundle_resolution``, ``shacl_execution``, ``shacl_conformance``,
    ``coverage_execution``, and ``coverage_conformance`` separately.
    """

    conforms: bool | None
    warning_count: int
    violation_count: int
    exit_code: int
    validator_name: str
    safe_summary: str
    undeclared_concepts: tuple[str, ...] = ()
    concept_guidance: str = ""
    unknown_upper_ontology_terms: tuple[str, ...] = ()
    role_mismatches: tuple[tuple[str, str, str], ...] = ()
    profile_not_selected: tuple[dict[str, Any], ...] = ()
    verification_status: str = "complete"
    verification_errors: tuple[str, ...] = ()
    selected_profiles: tuple[str, ...] = ()
    requested_profiles: tuple[str, ...] = ()
    selected_extensions: tuple[str, ...] = ()
    bundle_fingerprint: str | None = None
    extension_versions: tuple[tuple[str, str | None], ...] = ()
    bundle_resources: tuple[dict[str, Any], ...] = ()
    compatibility_notes: tuple[str, ...] = ()
    bundle_cache_status: str | None = None
    stage_status: tuple[tuple[str, str], ...] = ()
    validator_version: str | None = None
    # Truncated case_validate stdout/stderr for negative-fixture matching
    # (expected violation / constraint identifiers). Empty when unavailable.
    validator_diagnostics: str = ""
    error_code: str | None = None
    # One {focus_node, result_path, constraint_component, severity} record
    # of IRIs per SHACL result (no values or messages), capped at
    # MAX_VIOLATION_DETAILS.
    violation_details: tuple[dict[str, str | None], ...] = ()
    violation_details_truncated: bool = False


def _case_validate_sparql_crashes(cmd: list[str], *, timeout_seconds: int) -> bool:
    """Return True when a case_validate command dies on SPARQL ParseException."""

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False
    text = f"{completed.stdout}\n{completed.stderr}"
    return "ParseException" in text or "Expected SelectQuery" in text


def _isolate_sparql_crash_shape_files(
    *,
    graph: Path,
    ontology_paths: list[Path],
    base_args: list[str],
    timeout_seconds: int,
) -> list[Path]:
    """Binary-search which shape file(s) make case_validate raise ParseException.

    Non-shape ontology graphs stay loaded. Only shape files are searched, so
    the reported name is the failing shapes TTL, not the caller's data graph.
    """

    shapes = [p for p in ontology_paths if "shape" in p.name.lower()]
    nons = [p for p in ontology_paths if p not in shapes]
    if not shapes:
        return []

    def cmd_with(shape_subset: list[Path]) -> list[str]:
        cmd = list(base_args)
        for path in nons + shape_subset:
            cmd.extend(["--ontology-graph", str(path)])
        cmd.append(str(graph))
        return cmd

    if not _case_validate_sparql_crashes(
        cmd_with(shapes), timeout_seconds=timeout_seconds
    ):
        return []

    remaining = list(shapes)
    # Binary-search only. Do not regex-guess across shape files: many CAC
    # modules contain the same `; ?var` antipattern in unevaluated queries,
    # and listing them implies they crashed for this graph when they did not.
    while len(remaining) > 1:
        mid = len(remaining) // 2
        left, right = remaining[:mid], remaining[mid:]
        if _case_validate_sparql_crashes(
            cmd_with(left), timeout_seconds=timeout_seconds
        ):
            remaining = left
            continue
        if _case_validate_sparql_crashes(
            cmd_with(right), timeout_seconds=timeout_seconds
        ):
            remaining = right
            continue
        return []

    if len(remaining) == 1 and _case_validate_sparql_crashes(
        cmd_with(remaining), timeout_seconds=timeout_seconds
    ):
        return remaining
    return []


def parse_extension_token(name: str) -> tuple[str, str]:
    """Split ``cac``, ``cac:full``, or ``cac:missing-child`` into (name, mode).

    ``subset`` is the default press-release subset. ``full`` uses the extension
    manifest. Any other suffix is a named subset loaded from
    ``validation-subset-<mode>.json``.
    """

    if not name or name.endswith(":"):
        raise ValueError("extension_unknown")
    if ":" not in name:
        return name, "subset"
    ext, mode = name.rsplit(":", 1)
    if not ext or not mode:
        raise ValueError("extension_unknown")
    return ext, mode


def named_subset_manifest_path(ext_dir: Path, mode: str) -> Path | None:
    """Return the named-subset JSON path when ``mode`` is not subset/full."""

    if mode in {"subset", "full"}:
        return None
    return ext_dir / f"validation-subset-{mode}.json"


def load_extension_ontology_paths(
    ext_name: str,
    *,
    mode: str = "subset",
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> list[Path]:
    """Return ontology graph paths for an extension.

    mode ``subset`` uses the extension's ``validation-subset.json`` when present
    (recommended for MCP / press-release KGs). mode ``full`` uses the extension
    manifest (all owl/shacl/bridge files). Any other mode loads
    ``validation-subset-<mode>.json``. Extension directories are resolved
    across both vendoring roots (``extensions/`` and ``ontology/``).
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    ext_dir = _extension_dir(ext_name, project_root)
    paths: list[Path] = []
    subset_path = None
    if mode == "subset":
        candidate = ext_dir / "validation-subset.json"
        if candidate.exists():
            subset_path = candidate
    elif mode != "full":
        subset_path = named_subset_manifest_path(ext_dir, mode)
        if subset_path is None or not subset_path.is_file():
            raise ValueError("extension_unknown")
    if subset_path is not None:
        subset = json.loads(subset_path.read_text(encoding="utf-8"))
        for rel in subset.get("ontology_files", []):
            full = ext_dir / rel
            if full.exists():
                paths.append(full)
        if paths:
            return paths
        if mode not in {"subset", "full"}:
            raise ValueError("extension_unknown")
    manifest_path = ext_dir / "manifest.json"
    if not manifest_path.exists():
        return paths
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ("owl_files", "shacl_files", "bridge_files"):
        for rel_path in manifest.get(key, []):
            full_path = ext_dir / rel_path
            if full_path.exists():
                paths.append(full_path)
    return paths


def resolve_extension_dependencies(
    extension_names: list[str],
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> list[str]:
    """Expand an extension list with manifest ``depends_on`` entries.

    An extension whose exemplars/graphs reuse another extension's terms (e.g.
    ``rico`` builds on ``legalproc``) declares ``"depends_on": [...]`` in its
    manifest; callers then only need to name the top-level extension. The
    ``:full`` or a named-subset suffix (``:missing-child``) on a requested
    name is preserved; dependencies load in their default (subset-preferred)
    mode.

    Fail-closed (issue #55) — typed ``ValueError`` instead of a silently
    partial extension set: ``extension_unknown`` (a requested extension has
    no manifest), ``extension_dependency_missing`` (a ``depends_on`` entry
    has no manifest), ``extension_manifest_malformed`` (unparseable
    manifest), ``extension_dependency_cycle`` (circular ``depends_on``).
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    def _manifest_for(clean: str) -> dict[str, Any] | None:
        ext_dir = _find_extension_dir(clean, project_root)
        manifest_path = None if ext_dir is None else ext_dir / "manifest.json"
        if manifest_path is None or not manifest_path.is_file():
            return None
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("extension_manifest_malformed") from exc
        if not isinstance(payload, dict):
            raise ValueError("extension_manifest_malformed")
        return payload

    resolved: list[str] = []
    seen: set[str] = set()
    # (name, dependency chain from the requested root, requested directly?)
    queue: list[tuple[str, tuple[str, ...], bool]] = [
        (name, (), True) for name in extension_names
    ]
    while queue:
        name, chain, requested = queue.pop(0)
        clean, _mode = parse_extension_token(name)
        if clean in chain:
            raise ValueError("extension_dependency_cycle")
        if clean in seen:
            continue
        manifest = _manifest_for(clean)
        if manifest is None:
            raise ValueError(
                "extension_unknown" if requested else "extension_dependency_missing"
            )
        seen.add(clean)
        resolved.append(name)
        for dep in manifest.get("depends_on", []):
            queue.append((str(dep), chain + (clean,), False))
    return resolved


def extension_has_validation_subset(
    ext_name: str,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> bool:
    """Return True when an extension publishes a validation-subset manifest."""
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    ext_dir = _find_extension_dir(ext_name, project_root)
    return ext_dir is not None and (ext_dir / "validation-subset.json").is_file()


def _extension_namespaces(project_root: Path) -> list[tuple[str, str]]:
    """``(namespace IRI, extension name)`` pairs from every vendored manifest.

    Core CASE/UCO namespaces that a manifest re-declares (``uco-action`` in
    ``attack-technique``, for example) do not make the extension required.
    """

    from case_uco.graph import DEFAULT_CONTEXT

    core = {iri for iri in DEFAULT_CONTEXT.values() if isinstance(iri, str)}
    pairs: list[tuple[str, str]] = []
    for root in ("extensions", "ontology"):
        for manifest_path in sorted((project_root / root).glob("*/manifest.json")):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            name = manifest.get("name") or manifest_path.parent.name
            namespaces = manifest.get("namespaces") or {}
            if not isinstance(namespaces, dict):
                continue
            for iri in namespaces.values():
                if isinstance(iri, str) and iri and iri not in core:
                    pairs.append((iri, str(name)))
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return pairs


def required_extensions_for_graph(
    document: dict[str, Any],
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> list[str]:
    """Extension names whose namespaces the graph's types, properties or object references use.

    An IRI that appears only as the object of a property (``{"@id": ...}``),
    such as a state or vocabulary individual an extension declares, counts.
    Pass the result as ``extensions=`` to ``validate_graph_file`` (or one
    ``--ontology-graph`` set per extension to ``case_validate``); core-only
    validation rejects extension facets that are not ``core:Facet`` in the
    CASE closure.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    context = document.get("@context")
    prefixes = (
        {k: v for k, v in context.items() if isinstance(v, str)}
        if isinstance(context, dict)
        else {}
    )

    def expand(term: str) -> str:
        prefix, sep, local = term.partition(":")
        if sep and not local.startswith("//") and prefix in prefixes:
            return prefixes[prefix] + local
        return term

    used: set[str] = set()

    def visit(value: Any, is_object: bool = False) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item, is_object)
            return
        if not isinstance(value, dict):
            return
        node_id = value.get("@id")
        if is_object and isinstance(node_id, str):
            used.add(expand(node_id))
        for key, item in value.items():
            if key == "@type":
                for type_name in item if isinstance(item, list) else [item]:
                    if isinstance(type_name, str):
                        used.add(expand(type_name))
            elif key == "@context":
                continue
            elif not key.startswith("@"):
                used.add(expand(key))
                visit(item, is_object=True)
                continue
            visit(item, is_object)

    visit(document.get("@graph", document))
    namespaces = _extension_namespaces(project_root)
    required: set[str] = set()
    for iri in used:
        for namespace, name in namespaces:
            if iri.startswith(namespace):
                required.add(name)
                break
    return sorted(required)


def extension_ontology_args(
    extension_names: list[str] | None,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> list[str]:
    """Build case_validate flags for one or more extension manifests."""
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    if not extension_names:
        return []
    extension_names = resolve_extension_dependencies(extension_names, project_root)
    args: list[str] = [
        "--built-version",
        DEFAULT_BUILT_VERSION,
        "--allow-info",
    ]
    used_subset = False
    for ext_name in extension_names:
        clean_name, mode = parse_extension_token(ext_name)
        if mode != "full" and (
            mode != "subset" or extension_has_validation_subset(clean_name, project_root)
        ):
            used_subset = True
        rel_paths = load_extension_ontology_paths(
            clean_name, mode=mode, project_root=project_root
        )
        for full_path in rel_paths:
            args.extend(["--ontology-graph", str(full_path)])
    if used_subset:
        pass  # subset modules are self-contained; skip rdfs inference
    else:
        args.extend(["--inference", "rdfs"])
    return args


def validate_graph_file(
    graph_path: str | Path,
    allow_warning: bool = True,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    extensions: list[str] | None = None,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
    strict_concepts: bool = True,
    extra_ontology_graphs: list[str | Path] | None = None,
    force_rdfs_inference: bool = False,
    profiles: list[str] | None = None,
    allow_foundational_pair: bool = False,
    bundle_manifest_path: str | Path | None = None,
) -> GraphValidationReport:
    """Validate a CASE/UCO graph file with the local case_validate tool.

    When ``profiles`` or ``extra_ontology_graphs`` are set, or ``extensions``
    are set with ``strict_concepts``, resolution goes through
    ``resolve_validation_bundle`` so SHACL and concept coverage share one
    fingerprinted ontology set (CQ-27/CQ-28).
    Upper-ontology terms require explicit ``profiles=[...]`` (CQ-29); recipe
    validation always supplies them.

    Independent stages are reported separately (CQ-36): bundle resolution,
    SHACL execution, SHACL conformance, coverage execution, coverage
    conformance.

    Raises ValueError with a typed message for every honest-failure path:
    ``validator_unavailable``, ``graph_missing``, ``unsupported_graph_extension``,
    ``graph_oversized``, ``validation_timeout``.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    if not validator_available():
        raise ValueError("validator_unavailable")
    # Deployment filesystem policy: graph reads must stay inside configured
    # read roots (typed error "source_outside_read_roots" when violated).
    try:
        import workspace_policy  # optional MCP deployment policy

        graph = workspace_policy.check_read_path(
            graph_path, include_write_roots=True
        )
    except ImportError:
        graph = Path(graph_path).expanduser().resolve()
    if not graph.exists() or not graph.is_file():
        raise ValueError("graph_missing")
    if graph.suffix.lower() not in SUPPORTED_GRAPH_EXTENSIONS:
        raise ValueError("unsupported_graph_extension")
    if graph.stat().st_size > MAX_GRAPH_BYTES:
        raise ValueError("graph_oversized")

    validator_version = None
    args: list[str] = []
    if allow_warning:
        args.append("--allow-warning")

    resolved_bundle = None
    bundle_resolution_status = "skipped"
    # Construct one shared bundle whenever profiles, extensions, or extra
    # graphs need the same resource set for SHACL + strict coverage (CQ-27/CQ-28).
    if profiles or (extensions and strict_concepts) or extra_ontology_graphs:
        from case_uco.validation.bundle import ValidationBundleError, resolve_validation_bundle

        try:
            resolved_bundle = resolve_validation_bundle(
                extensions=extensions,
                profiles=profiles,
                project_root=project_root,
                allow_foundational_pair=allow_foundational_pair,
                extra_ontology_graphs=extra_ontology_graphs,
            )
            bundle_resolution_status = "complete"
        except ValidationBundleError as exc:
            raise ValueError(str(exc)) from exc
        if bundle_manifest_path:
            resolved_bundle.write_manifest(bundle_manifest_path)
        args.extend(["--built-version", DEFAULT_BUILT_VERSION, "--allow-info"])
        for path in resolved_bundle.ontology_graph_paths():
            args.extend(["--ontology-graph", str(path)])
        if resolved_bundle.inference:
            args.extend(["--inference", resolved_bundle.inference])
        elif force_rdfs_inference:
            args.extend(["--inference", "rdfs"])
    else:
        extension_args = extension_ontology_args(extensions, project_root=project_root)
        if extension_args:
            args.extend(extension_args)
        elif extensions:
            args.extend(["--built-version", DEFAULT_BUILT_VERSION])
        if force_rdfs_inference and "--inference" not in args:
            args.extend(["--inference", "rdfs"])

    args.append(str(graph))
    built_version = (
        args[args.index("--built-version") + 1] if "--built-version" in args else None
    )
    shacl_execution_status = "complete"
    error_code = None
    error_message = ""
    validator_command: list[str] = []
    try:
        runtime = prepare_validator(built_version)
        validator_version = runtime.version
        validator_command = list(runtime.command)
        args = validator_command + args
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except ValidatorError as exc:
        error_code = exc.code
        error_message = str(exc)
        validator_version = exc.version
        completed = subprocess.CompletedProcess(args, 2, stdout="", stderr=error_message)
    except OSError:
        error_code = "validator_execution_failed"
        error_message = validator_error_message(error_code, built_version)
        completed = subprocess.CompletedProcess(args, 127, stdout="", stderr=error_message)
    except subprocess.TimeoutExpired as exc:
        raise ValueError("validation_timeout") from exc

    error_code = error_code or validator_error_code(completed.returncode, completed.stderr)
    if error_code and not error_message:
        error_message = validator_error_message(error_code, built_version)

    combined = f"{completed.stdout}\n{completed.stderr}"
    conforms = _parse_conforms(combined)
    violation_count = combined.count(_VIOLATION_MARKER)
    warning_count = combined.count(_WARNING_MARKER)
    exit_code = completed.returncode
    violation_details: tuple[dict[str, str | None], ...] = ()
    violation_details_truncated = False
    if not error_code and violation_count:
        loaded_graphs = [
            Path(args[i + 1]) for i, arg in enumerate(args[:-1]) if arg == "--ontology-graph"
        ]
        violation_details, violation_details_truncated = parse_violation_details(
            completed.stdout, _validation_prefixes(graph, loaded_graphs)
        )

    sparql_crash_files: tuple[Path, ...] = ()
    if error_code:
        conforms = None
        shacl_execution_status = "failed"
        shacl_conformance_status = "could_not_verify"
    elif "ParseException" in combined or "Expected SelectQuery" in combined:
        # case_validate/pyshacl crashed while parsing a SHACL SPARQL constraint.
        # Blame the shape file, not the caller's graph.
        ontology_paths: list[Path] = []
        if resolved_bundle is not None:
            ontology_paths = list(resolved_bundle.ontology_graph_paths())
        else:
            for i, arg in enumerate(args):
                if arg == "--ontology-graph" and i + 1 < len(args):
                    ontology_paths.append(Path(args[i + 1]))
        # Strip trailing graph path and ontology-graph pairs for the isolator.
        base_args = list(validator_command)
        if allow_warning:
            base_args.append("--allow-warning")
        base_args.extend(["--built-version", DEFAULT_BUILT_VERSION, "--allow-info"])
        if "--inference" in args:
            # Keep the same inference flag the crashing run used.
            idx = args.index("--inference")
            base_args.extend(args[idx : idx + 2])
        sparql_crash_files = tuple(
            _isolate_sparql_crash_shape_files(
                graph=graph,
                ontology_paths=ontology_paths,
                base_args=base_args,
                timeout_seconds=timeout_seconds,
            )
        )
        conforms = None
        shacl_execution_status = "failed"
        shacl_conformance_status = "could_not_verify"
        if sparql_crash_files:
            named = ", ".join(p.name for p in sparql_crash_files)
            summary = (
                "Validator crashed while parsing SHACL SPARQL in shape file(s): "
                f"{named}. This is an ontology/shapes defect (or a case_validate "
                "SPARQL parser limit), not a defect in the submitted graph."
            )
        else:
            summary = (
                "Validator crashed with a SPARQL ParseException while evaluating "
                "SHACL constraints. The failing shape file could not be isolated; "
                "inspect case_validate stderr. Do not treat the graph as conforming."
            )
    elif conforms is True and violation_count == 0:
        shacl_conformance_status = "conforms"
    elif conforms is False or violation_count > 0:
        shacl_conformance_status = "nonconformant"
    else:
        shacl_conformance_status = "unknown"
        shacl_execution_status = "failed"

    if error_code:
        summary = error_message
    elif sparql_crash_files or (
        "ParseException" in combined or "Expected SelectQuery" in combined
    ):
        pass  # summary already set above
    elif exit_code == 0 and conforms is not False and violation_count == 0:
        if warning_count > 0:
            summary = (
                f"Graph conforms with {warning_count} validator warning(s); "
                "review warnings before relying on extension concepts."
            )
        elif extensions:
            mode_note = ""
            if any(not ext.endswith(":full") for ext in extensions):
                mode_note = " (validation-subset)"
            summary = (
                f"Graph conforms to CASE/UCO SHACL shapes with extension(s): "
                f"{', '.join(extensions)}.{mode_note}"
            )
        else:
            summary = "Graph conforms to CASE/UCO SHACL shapes."
    elif conforms is False or violation_count > 0:
        summary = (
            f"Graph does not conform: {violation_count} constraint violation(s). "
            "Fix the graph before submitting it for review."
        )
    else:
        summary = (
            "Validator could not produce a conformance result; "
            "the graph content may be malformed."
        )

    undeclared: tuple[str, ...] = ()
    concept_guidance = ""
    unknown_upper: tuple[str, ...] = ()
    role_mismatches: tuple[tuple[str, str, str], ...] = ()
    profile_not_selected: tuple[dict[str, Any], ...] = ()
    verification_status = "could_not_verify" if error_code else "complete"
    verification_errors: tuple[str, ...] = (error_code,) if error_code else ()
    coverage_execution_status = "skipped"
    coverage_conformance_status = "skipped"

    if "ParseException" in combined or "Expected SelectQuery" in combined:
        verification_status = "could_not_verify"
        crash_names = tuple(p.name for p in sparql_crash_files)
        verification_errors = (
            ("shacl_sparql_parse_failed:" + ",".join(crash_names),)
            if crash_names
            else ("shacl_sparql_parse_failed",)
        )
        # Do not claim SHACL or coverage passed after a shapes crash.
        conforms = None

    if strict_concepts and verification_status != "could_not_verify":
        coverage_execution_status = "complete"
        try:
            from case_uco.validation.coverage import check_graph_concepts

            coverage = check_graph_concepts(
                graph,
                project_root=project_root,
                extensions=extensions if resolved_bundle is None else None,
                selected_profiles=(
                    list(resolved_bundle.profiles) if resolved_bundle is not None else []
                ),
                bundle=resolved_bundle,
            )
        except Exception as exc:  # honest failure: never fake coverage
            conforms = None
            verification_status = "could_not_verify"
            verification_errors = (f"concept_coverage_failed:{type(exc).__name__}",)
            coverage_execution_status = "failed"
            coverage_conformance_status = "could_not_verify"
            summary = (
                f"{summary} Additionally, the concept coverage check could "
                f"not run ({type(exc).__name__}); treat the result as "
                "unverified."
            )
        else:
            verification_status = coverage.verification_status
            verification_errors = coverage.verification_errors
            if coverage.verification_status != "complete":
                conforms = False
                coverage_conformance_status = "could_not_verify"
            elif coverage.ok:
                coverage_conformance_status = "ok"
            else:
                coverage_conformance_status = "failed"
            if not coverage.ok:
                undeclared = coverage.undeclared_classes + coverage.undeclared_properties
                unknown_upper = coverage.unknown_upper_ontology_terms
                role_mismatches = coverage.role_mismatches
                profile_not_selected = tuple(
                    {
                        "iri": item.iri,
                        "required_profile": item.required_profile,
                        "used_as": item.used_as,
                        "selected_profiles": list(item.selected_profiles),
                    }
                    for item in coverage.profile_not_selected
                )
                concept_guidance = coverage.guidance
                shacl_passed = conforms is not False and violation_count == 0
                conforms = False
                parts: list[str] = []
                if undeclared:
                    shown = ", ".join(undeclared[:8])
                    more = f" (+{len(undeclared) - 8} more)" if len(undeclared) > 8 else ""
                    parts.append(
                        f"Graph uses {len(undeclared)} class/property term(s) not declared "
                        f"in CASE/UCO or supported extension ontologies: {shown}{more}."
                    )
                if unknown_upper:
                    shown = ", ".join(unknown_upper[:8])
                    parts.append(
                        f"Graph uses {len(unknown_upper)} term(s) inside profiled "
                        f"upper-ontology namespaces that the pinned ontology releases "
                        f"do not declare: {shown}. Use the term the pinned release "
                        f"declares (for QUDT units, lookup_qudt_units); a change "
                        f"proposal cannot add terms to an external ontology."
                    )
                if profile_not_selected:
                    shown = ", ".join(
                        f"{p['iri']} (needs {p['required_profile']})"
                        for p in profile_not_selected[:4]
                    )
                    parts.append(
                        f"Graph uses {len(profile_not_selected)} upper-ontology "
                        f"term(s) whose profile was not selected: {shown}."
                    )
                if role_mismatches:
                    shown = "; ".join(
                        f"{iri} (declared as {declared_role}, used as {used_as})"
                        for iri, declared_role, used_as in role_mismatches[:4]
                    )
                    parts.append(
                        f"Graph uses {len(role_mismatches)} declared term(s) in the "
                        f"wrong RDF role: {shown}."
                    )
                if verification_errors:
                    parts.append(
                        f"Required verification stage(s) could not run "
                        f"({', '.join(verification_errors)}); the result is "
                        "unverified, not conformant."
                    )
                elif undeclared:
                    parts.append(
                        "Draft a change proposal or add the concept(s) to an extension "
                        "ontology, then re-validate."
                    )
                concept_summary = " ".join(parts)
                summary = concept_summary if shacl_passed else f"{summary} {concept_summary}"

    # CQ-36: independent stage reporting.
    stage_status: list[tuple[str, str]] = [
        ("bundle_resolution", bundle_resolution_status),
        ("shacl_execution", shacl_execution_status),
        ("shacl_conformance", shacl_conformance_status),
        ("coverage_execution", coverage_execution_status),
        ("coverage_conformance", coverage_conformance_status),
    ]

    # Cap diagnostics so reports stay bounded while still exposing SHACL
    # Source Shape / Constraint Component identifiers for negative fixtures.
    _diag_limit = 16_384
    diagnostics = combined.strip()
    if len(diagnostics) > _diag_limit:
        diagnostics = diagnostics[:_diag_limit] + "\n…[truncated]"

    from case_uco.validation.bundle import _extension_versions

    return GraphValidationReport(
        conforms=conforms,
        warning_count=warning_count,
        violation_count=violation_count,
        exit_code=exit_code,
        validator_name=VALIDATOR_NAME,
        safe_summary=summary,
        undeclared_concepts=undeclared,
        concept_guidance=concept_guidance,
        unknown_upper_ontology_terms=unknown_upper,
        role_mismatches=role_mismatches,
        profile_not_selected=profile_not_selected,
        verification_status=verification_status,
        verification_errors=verification_errors,
        selected_profiles=tuple(resolved_bundle.profiles) if resolved_bundle else (),
        requested_profiles=(
            tuple(resolved_bundle.requested_profiles) if resolved_bundle else tuple(profiles or ())
        ),
        selected_extensions=(
            tuple(resolved_bundle.extensions) if resolved_bundle else tuple(extensions or ())
        ),
        bundle_fingerprint=resolved_bundle.fingerprint if resolved_bundle else None,
        extension_versions=(
            tuple(_extension_versions(resolved_bundle.extensions, project_root).items())
            if resolved_bundle
            else ()
        ),
        bundle_resources=tuple(resolved_bundle.to_manifest(portable=True)["resources"])
        if resolved_bundle
        else (),
        compatibility_notes=tuple(resolved_bundle.compatibility_notes) if resolved_bundle else (),
        bundle_cache_status=resolved_bundle.cache_status if resolved_bundle else None,
        stage_status=tuple(stage_status),
        validator_version=validator_version,
        validator_diagnostics=diagnostics,
        error_code=error_code,
        violation_details=violation_details,
        violation_details_truncated=violation_details_truncated,
    )


def report_to_dict(report: GraphValidationReport) -> dict[str, Any]:
    """Serialize a report into the MCP tool result shape."""

    payload: dict[str, Any] = {
        "conforms": report.conforms,
        "warning_count": report.warning_count,
        "violation_count": report.violation_count,
        "exit_code": report.exit_code,
        "validator_name": report.validator_name,
        "safe_summary": report.safe_summary,
        "verification_status": report.verification_status,
        "built_version": DEFAULT_BUILT_VERSION,
        "ontology_identity": {
            "case": "1.5.0",
            "uco": "1.5.0",
            "cac": "3.1.0",
            "case_utils": report.validator_version,
        },
    }
    if report.error_code:
        payload["error_code"] = report.error_code
    if report.validator_version:
        payload["validator_version"] = report.validator_version
    if report.verification_errors:
        payload["verification_errors"] = list(report.verification_errors)
    if report.violation_details:
        payload["violation_details"] = [dict(d) for d in report.violation_details]
        payload["violation_details_truncated"] = report.violation_details_truncated
    if report.undeclared_concepts:
        payload["undeclared_concepts"] = list(report.undeclared_concepts)
    if report.unknown_upper_ontology_terms:
        payload["unknown_upper_ontology_terms"] = list(
            report.unknown_upper_ontology_terms
        )
    if report.profile_not_selected:
        payload["profile_not_selected"] = list(report.profile_not_selected)
    if report.role_mismatches:
        payload["role_mismatches"] = [
            {"iri": iri, "declared_role": declared_role, "used_as": used_as}
            for iri, declared_role, used_as in report.role_mismatches
        ]
    if report.concept_guidance:
        payload["concept_guidance"] = report.concept_guidance
    if report.selected_profiles:
        payload["selected_profiles"] = list(report.selected_profiles)
    if report.requested_profiles:
        payload["requested_profiles"] = list(report.requested_profiles)
    if report.selected_extensions:
        payload["selected_extensions"] = list(report.selected_extensions)
    if report.bundle_fingerprint:
        payload["bundle_fingerprint"] = report.bundle_fingerprint
    if report.extension_versions:
        payload["extension_versions"] = dict(report.extension_versions)
    if report.bundle_resources:
        payload["bundle_resources"] = list(report.bundle_resources)
    if report.compatibility_notes:
        payload["compatibility_notes"] = list(report.compatibility_notes)
    if report.bundle_cache_status:
        payload["bundle_cache_status"] = report.bundle_cache_status
    if report.stage_status:
        payload["stage_status"] = [
            {"stage": stage, "status": status} for stage, status in report.stage_status
        ]
    return payload


MAX_VIOLATION_DETAILS = 20

# Prefixes the pinned case-1.5.0 build binds; pyshacl prints result paths
# with them (``core:isDirectional``).
_BUILT_ONTOLOGY_PREFIXES = {
    "action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "analysis": "https://ontology.unifiedcyberontology.org/uco/analysis/",
    "configuration": "https://ontology.unifiedcyberontology.org/uco/configuration/",
    "core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "investigation": "https://ontology.caseontology.org/case/investigation/",
    "location": "https://ontology.unifiedcyberontology.org/uco/location/",
    "marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
    "observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "pattern": "https://ontology.unifiedcyberontology.org/uco/pattern/",
    "role": "https://ontology.unifiedcyberontology.org/uco/role/",
    "time1": "https://ontology.unifiedcyberontology.org/uco/time/",
    "tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "victim": "https://ontology.unifiedcyberontology.org/uco/victim/",
    "vocab": "https://ontology.caseontology.org/case/vocabulary/",
    "vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "sh": "http://www.w3.org/ns/shacl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}
_RESULT_HEADER_RE = re.compile(r"^Constraint Violation in \S+ \((?P<component>[^()\s]+)\):", re.M)
_RESULT_FIELD_RE = re.compile(r"^\s+(Severity|Focus Node|Result Path):\s*(.*?)\s*$", re.M)
_TURTLE_PREFIX_RE = re.compile(r"@prefix\s+([A-Za-z][\w.-]*)?\s*:\s*<([^<>\s]+)>", re.I)
_CURIE_RE = re.compile(r"([A-Za-z][\w.-]*)?:([^\s\[\]()<>\"'{}|\\^`]*)")


def _file_prefixes(path: Path) -> dict[str, str]:
    """Namespace prefixes declared by a Turtle or JSON-LD file."""
    try:
        if path.suffix.lower() in {".jsonld", ".json"}:
            contexts = json.loads(path.read_text(encoding="utf-8")).get("@context", {})
            prefixes: dict[str, str] = {}
            for context in contexts if isinstance(contexts, list) else [contexts]:
                if isinstance(context, dict):
                    prefixes.update(
                        (name, value) for name, value in context.items()
                        if isinstance(value, str) and not name.startswith("@")
                        and value.endswith(("/", "#", ":"))
                    )
            return prefixes
        with path.open(encoding="utf-8", errors="replace") as handle:
            head = handle.read(1_000_000)
        return {name or "": iri for name, iri in _TURTLE_PREFIX_RE.findall(head)}
    except (OSError, ValueError, AttributeError):
        return {}


def _validation_prefixes(graph_path: Path, ontology_paths: list[Path]) -> dict[str, str]:
    prefixes = dict(_BUILT_ONTOLOGY_PREFIXES)
    for path in ontology_paths:
        prefixes.update(_file_prefixes(path))
    prefixes.update(_file_prefixes(graph_path))
    return prefixes


def _expand_term(term: str, prefixes: dict[str, str]) -> str | None:
    """Expand a printed IRI or prefixed name; ``None`` for anything else
    (blank nodes, literals, complex paths) so no values leak."""
    if term.startswith("<") and term.endswith(">") and " " not in term:
        return term[1:-1]
    if re.fullmatch(r"(?:https?|urn):[^\s\[\]()<>\"']+", term):
        return term
    match = _CURIE_RE.fullmatch(term)
    if match and match.group(1) != "_" and (match.group(1) or "") in prefixes:
        return prefixes[match.group(1) or ""] + match.group(2)
    return None


def parse_violation_details(
    output: str,
    prefixes: dict[str, str],
    *,
    limit: int = MAX_VIOLATION_DETAILS,
) -> tuple[tuple[dict[str, str | None], ...], bool]:
    """Identify each SHACL result in ``case_validate``'s human output.

    Returns up to ``limit`` ``{focus_node, result_path,
    constraint_component, severity}`` records with expanded IRIs, and
    whether more results were left out. Value nodes, messages and source
    shapes are never read, because they can echo graph literals.
    """
    headers = list(_RESULT_HEADER_RE.finditer(output))
    details: list[dict[str, str | None]] = []
    for index, header in enumerate(headers[:limit]):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(output)
        fields = dict(_RESULT_FIELD_RE.findall(output[header.end():end]))
        details.append({
            "focus_node": _expand_term(fields.get("Focus Node", ""), prefixes),
            "result_path": _expand_term(fields.get("Result Path", ""), prefixes),
            "constraint_component": _expand_term(header.group("component"), prefixes),
            "severity": _expand_term(fields.get("Severity", ""), prefixes),
        })
    return tuple(details), len(headers) > limit


def _parse_conforms(output: str) -> bool | None:
    for line in output.splitlines():
        key, sep, value = line.partition(":")
        if not sep or key.strip().lower() != _CONFORMS_KEY:
            continue
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    return None

__all__ = [
    "DEFAULT_BUILT_VERSION",
    "DEFAULT_TIMEOUT_SECONDS",
    "MAX_GRAPH_BYTES",
    "PROJECT_ROOT",
    "SUPPORTED_GRAPH_EXTENSIONS",
    "VALIDATOR_NAME",
    "GraphValidationReport",
    "extension_has_validation_subset",
    "extension_ontology_args",
    "load_extension_ontology_paths",
    "named_subset_manifest_path",
    "parse_extension_token",
    "parse_violation_details",
    "report_to_dict",
    "required_extensions_for_graph",
    "resolve_extension_dependencies",
    "validate_graph_file",
    "validator_available",
    "_parse_conforms",
]
