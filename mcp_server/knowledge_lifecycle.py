"""Staged promotion lifecycle for learned knowledge artifacts.

The SDK lets agents grow extension ontologies, recipes, and routing indexes
during live investigations. This module defines the promotion boundary
between an experimental lesson and trusted operational guidance:

- ``candidate`` — generated or edited during an investigation. Candidate
  extensions carry ``"status": "candidate"`` in their ``manifest.json`` and
  are **excluded from routing discovery** (``route_investigation_content``
  does not advertise them). They can still be loaded *explicitly by name*
  (``validate_graph(extensions=["myext"])``) so the authoring investigation
  can keep working with them.
- ``operational`` — validated and intentionally promoted. Manifests without
  a ``status`` field are treated as operational (the nine bundled extensions
  predate the lifecycle). Promotion records provenance metadata.
- ``deprecated`` — retained with provenance, excluded from routing; the
  emergency revocation state for a bad extension.
- Any *other* status value is invalid (fail-closed, issue #55): an unknown
  status is never treated as operational and is never routable.

Extension promotion (``promote_extension``) runs validation gates before
flipping status (issue #56): manifest schema integrity, Turtle parse of
every listed ontology file, anchoring of every declared class to a class
that is *actually declared* in core CASE/UCO, a resolved operational
dependency, or the pinned upper-ontology registry, exemplar conformance
(at least one conforming exemplar is required), expected-invalid negative
fixtures (must fail validation), and declared competency queries. A failed
gate leaves the manifest untouched. The active deployment profile
(``workspace_policy``) controls promotion authority: production-review
deployments require a non-empty reviewer identity; offline-investigation
and production-authoring deployments cannot promote at all.

Recipe promotion (``promote_recipe``) is the governed counterpart of the
manual "move the file and edit two indexes" workflow: it verifies the
candidate recipe's required structure, then transactionally moves it into
``docs/recipes/``, registers it in ``docs/recipes/INDEX.md`` and
``RECIPE_INDEX`` (``mcp_server/domain_index.py``), and records promotion
provenance in ``docs/recipes/promotion-log.json``. A failed gate writes
nothing. ``deprecate_recipe`` reverses the registration and moves the file
back to ``docs/recipes/candidates/``.

Rollback is git-based — knowledge artifacts are plain files under version
control, so restoring the previous approved generation is::

    make rollback-extension EXT=<name> REF=<tag-or-commit>

which runs ``git checkout <ref> -- <root>/<name>`` (root resolved across
``extensions/`` and ``ontology/``). Recipes roll back
with ``git checkout <ref> -- docs/recipes/<file>.md``. See
docs/recipes/recipe-authoring.md.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import extension_paths
import graph_validator

try:
    import fcntl
except ImportError:  # pragma: no cover — non-POSIX
    fcntl = None  # type: ignore[assignment]

_logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STATUS_CANDIDATE = "candidate"
STATUS_OPERATIONAL = "operational"
STATUS_DEPRECATED = "deprecated"
STATUS_INVALID = "invalid"
VALID_STATUSES = {STATUS_CANDIDATE, STATUS_OPERATIONAL, STATUS_DEPRECATED}

CANDIDATE_RECIPE_DIR = "docs/recipes/candidates"
RECIPE_DIR = "docs/recipes"
RECIPE_PROMOTION_LOG = "docs/recipes/promotion-log.json"


@dataclass
class PromotionResult:
    ok: bool
    extension: str
    status: str
    gates: list[dict] = field(default_factory=list)
    error: str = ""


def extension_status(manifest: dict) -> str:
    """Lifecycle status of an extension manifest.

    An absent ``status`` field means operational (the bundled extensions
    predate the lifecycle). An *unrecognized* value is ``invalid`` — never
    operational and never routable (fail-closed, issue #55).
    """

    raw = manifest.get("status")
    if raw is None:
        return STATUS_OPERATIONAL
    status = str(raw).strip().lower()
    return status if status in VALID_STATUSES else STATUS_INVALID


def is_routable(manifest: dict) -> bool:
    """Only approved operational artifacts are advertised by routing."""

    return extension_status(manifest) == STATUS_OPERATIONAL


def _manifest_path(name: str, project_root: Path) -> Path:
    return extension_paths.extension_manifest_path(name, project_root)


def _load_manifest(name: str, project_root: Path) -> dict:
    path = _manifest_path(name, project_root)
    if not path.is_file():
        raise ValueError("extension_manifest_missing")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("extension_manifest_malformed") from exc


def _git_commit_sha(project_root: Path) -> str:
    """Best-effort current commit SHA for promotion provenance."""

    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root, capture_output=True, text=True, timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        _logger.debug("git rev-parse unavailable: %s", exc)
        return ""
    return completed.stdout.strip() if completed.returncode == 0 else ""


def _clear_concept_caches() -> None:
    """Invalidate declared-term caches after a lifecycle transition."""

    import concept_coverage

    concept_coverage.clear_declared_term_cache()


# ---------------------------------------------------------------------------
# Extension promotion gates (issue #56)
# ---------------------------------------------------------------------------


def _gate_manifest_schema(name: str, manifest: dict, project_root: Path) -> dict:
    """The manifest must carry the required fields and a valid status."""

    missing = [key for key in ("name", "version") if not manifest.get(key)]
    if missing:
        return {"gate": "manifest_schema", "ok": False,
                "detail": f"manifest missing required field(s): {', '.join(missing)}"}
    status = extension_status(manifest)
    if status == STATUS_INVALID:
        return {"gate": "manifest_schema", "ok": False,
                "detail": "manifest status value is not a recognized lifecycle status"}
    if not any(manifest.get(key) for key in ("owl_files", "shacl_files", "bridge_files")):
        return {"gate": "manifest_schema", "ok": False,
                "detail": "manifest lists no ontology files"}
    return {"gate": "manifest_schema", "ok": True, "detail": "manifest schema valid"}


def _gate_ontology_files_parse(name: str, manifest: dict, project_root: Path) -> dict:
    """Every listed ontology file must exist and parse as Turtle."""

    import rdflib

    ext_dir = extension_paths.extension_dir(name, project_root)
    checked = 0
    for key in ("owl_files", "shacl_files", "bridge_files"):
        for rel in manifest.get(key, []):
            full = ext_dir / rel
            if not full.is_file():
                return {"gate": "ontology_files_parse", "ok": False,
                        "detail": f"missing file listed in manifest: {rel}"}
            try:
                rdflib.Graph().parse(str(full), format="turtle")
            except Exception as exc:
                return {"gate": "ontology_files_parse", "ok": False,
                        "detail": f"{rel}: parse failed ({type(exc).__name__})"}
            checked += 1
    if checked == 0:
        return {"gate": "ontology_files_parse", "ok": False,
                "detail": "manifest lists no ontology files"}
    return {"gate": "ontology_files_parse", "ok": True, "detail": f"{checked} file(s) parsed"}


def _gate_classes_anchored(name: str, manifest: dict, project_root: Path) -> dict:
    """Every declared owl:Class must subclass a class that is *declared* in
    core CASE/UCO, a resolved operational dependency, the pinned
    upper-ontology registry, or this extension itself (issue #56 — a bare
    ``rdfs:subClassOf`` statement pointing at an undeclared parent no
    longer passes)."""

    import rdflib
    from rdflib import OWL, RDF, RDFS, URIRef

    import concept_coverage

    ext_dir = extension_paths.extension_dir(name, project_root)
    graph = rdflib.Graph()
    for key in ("owl_files", "bridge_files"):
        for rel in manifest.get(key, []):
            full = ext_dir / rel
            if not full.is_file():
                continue
            try:
                graph.parse(str(full), format="turtle")
            except Exception as exc:
                # The parse gate reports unparseable files with detail;
                # this gate anchors whatever does parse.
                _logger.debug("classes_anchored: skipping %s (%s)", rel, exc)

    own_classes = {
        str(cls) for cls in graph.subjects(RDF.type, OWL.Class)
        if isinstance(cls, URIRef)
    }
    dependencies = [str(dep) for dep in manifest.get("depends_on", [])]
    try:
        declared = concept_coverage.load_declared_terms(
            project_root=project_root, extensions=dependencies
        )
        declared_classes = set(declared.classes) | set(declared.unknown_role)
    except ValueError as exc:
        return {"gate": "classes_anchored", "ok": False,
                "detail": f"dependency resolution failed ({exc})"}
    upper, _upper_error = concept_coverage._load_upper_registry()
    upper_classes = set(upper["classes"]) if upper else set()

    orphans: list[str] = []
    unanchored: list[str] = []
    for cls in sorted(own_classes):
        parents = [
            str(parent)
            for parent in graph.objects(URIRef(cls), RDFS.subClassOf)
            if isinstance(parent, URIRef)
        ]
        if not parents:
            orphans.append(cls)
            continue
        if not any(
            parent in declared_classes
            or parent in upper_classes
            or parent in own_classes
            or concept_coverage._is_standard(parent)
            for parent in parents
        ):
            unanchored.append(cls)
    if orphans:
        return {"gate": "classes_anchored", "ok": False,
                "detail": f"classes without rdfs:subClassOf: {', '.join(orphans[:5])}"}
    if unanchored:
        return {"gate": "classes_anchored", "ok": False,
                "detail": ("classes whose parents are not declared in core, "
                           "an operational dependency, or the pinned upper "
                           f"ontologies: {', '.join(unanchored[:5])}")}
    return {"gate": "classes_anchored", "ok": True,
            "detail": "every declared class anchors to a declared class"}


def _gate_exemplars_validate(
    name: str,
    manifest: dict,
    project_root: Path,
    require_validator: bool,
) -> dict:
    """At least one exemplar graph is required and every listed exemplar
    must pass case_validate with the extension's own ontology files loaded
    (issue #56 — an extension with no exemplars no longer passes)."""

    ext_dir = extension_paths.extension_dir(name, project_root)
    exemplars = manifest.get("exemplar_files", [])
    if not exemplars:
        return {"gate": "exemplars_validate", "ok": False,
                "detail": ("no exemplar_files in manifest; promotion requires "
                           "at least one conforming exemplar graph")}
    for rel in exemplars:
        if not (ext_dir / rel).is_file():
            return {"gate": "exemplars_validate", "ok": False,
                    "detail": f"missing exemplar: {rel}"}
    if not graph_validator.validator_available():
        if require_validator:
            return {"gate": "exemplars_validate", "ok": False,
                    "detail": "case_validate unavailable; install case-utils or "
                              "pass require_validator=False in a dev-only context"}
        return {"gate": "exemplars_validate", "ok": True,
                "detail": (f"{len(exemplars)} exemplar(s) present; conformance "
                           "run skipped: case_validate unavailable "
                           "(require_validator=False)")}
    for rel in exemplars:
        report = graph_validator.validate_graph_file(
            ext_dir / rel, extensions=[f"{name}:full"], project_root=project_root
        )
        if report.conforms is not True:
            return {"gate": "exemplars_validate", "ok": False,
                    "detail": f"{rel}: {report.safe_summary}"}
    return {"gate": "exemplars_validate", "ok": True,
            "detail": f"{len(exemplars)} exemplar(s) conform"}


def _gate_negative_fixtures(
    name: str,
    manifest: dict,
    project_root: Path,
    require_validator: bool,
) -> dict:
    """Expected-invalid fixtures (``invalid_exemplar_files``) must exist and
    must FAIL validation — proof the extension's shapes actually constrain
    (issue #56). Required whenever the extension declares SHACL shapes
    (otherwise there is nothing to constrain and the gate passes with an
    advisory detail). A listed fixture that unexpectedly conforms is always
    a hard failure."""

    ext_dir = extension_paths.extension_dir(name, project_root)
    fixtures = manifest.get("invalid_exemplar_files", [])
    if not fixtures:
        if manifest.get("shacl_files"):
            return {"gate": "negative_fixtures", "ok": False,
                    "detail": ("extension declares SHACL shapes but lists no "
                               "invalid_exemplar_files; add at least one "
                               "expected-invalid fixture proving the shapes "
                               "constrain")}
        return {"gate": "negative_fixtures", "ok": True,
                "detail": ("no SHACL shapes and no invalid_exemplar_files "
                           "declared (advisory: add an expected-invalid "
                           "fixture once shapes exist)")}
    for rel in fixtures:
        if not (ext_dir / rel).is_file():
            return {"gate": "negative_fixtures", "ok": False,
                    "detail": f"missing invalid exemplar fixture: {rel}"}
    if not graph_validator.validator_available():
        if require_validator:
            return {"gate": "negative_fixtures", "ok": False,
                    "detail": "case_validate unavailable; install case-utils"}
        return {"gate": "negative_fixtures", "ok": True,
                "detail": (f"{len(fixtures)} fixture(s) present; conformance "
                           "run skipped (require_validator=False)")}
    for rel in fixtures:
        report = graph_validator.validate_graph_file(
            ext_dir / rel, extensions=[f"{name}:full"], project_root=project_root
        )
        if report.conforms is True:
            return {"gate": "negative_fixtures", "ok": False,
                    "detail": (f"{rel}: expected-invalid fixture CONFORMS — the "
                               "extension shapes do not constrain it")}
    return {"gate": "negative_fixtures", "ok": True,
            "detail": f"{len(fixtures)} expected-invalid fixture(s) correctly fail"}


def _gate_competency_queries(name: str, manifest: dict, project_root: Path) -> dict:
    """Declared competency queries must run and meet their expectation.

    Manifest format::

        "competency_queries": [
            {"file": "queries/q1.sparql", "against": "exemplar.ttl",
             "expect": "nonempty"}   # or "empty"
        ]
    """

    import rdflib

    ext_dir = extension_paths.extension_dir(name, project_root)
    queries = manifest.get("competency_queries", [])
    if not queries:
        return {"gate": "competency_queries", "ok": True,
                "detail": "no competency queries declared"}
    for entry in queries:
        query_rel = entry.get("file", "")
        against_rel = entry.get("against", "")
        expect = entry.get("expect", "nonempty")
        query_path = ext_dir / query_rel
        against_path = ext_dir / against_rel
        if not query_path.is_file() or not against_path.is_file():
            return {"gate": "competency_queries", "ok": False,
                    "detail": f"missing query or target graph: {query_rel} / {against_rel}"}
        graph = rdflib.Graph()
        try:
            graph.parse(str(against_path))
            results = list(graph.query(query_path.read_text(encoding="utf-8")))
        except Exception as exc:
            return {"gate": "competency_queries", "ok": False,
                    "detail": f"{query_rel}: query failed ({type(exc).__name__})"}
        nonempty = bool(results)
        if (expect == "nonempty") != nonempty:
            return {"gate": "competency_queries", "ok": False,
                    "detail": f"{query_rel}: expected {expect} result set, got "
                              f"{len(results)} row(s)"}
    return {"gate": "competency_queries", "ok": True,
            "detail": f"{len(queries)} competency quer(y/ies) verified"}


def promote_extension(
    name: str,
    project_root: Path = PROJECT_ROOT,
    reviewed_by: str = "",
    require_validator: bool = True,
) -> PromotionResult:
    """Run all promotion gates; on success mark the extension operational.

    Provenance (who approved, when, which gates ran, commit) is recorded in
    the manifest ``promotion`` block. A failed gate leaves the manifest
    untouched and reports the failure. The active deployment profile
    (``workspace_policy``) gates promotion authority: profiles without
    promotion authority are refused, and production-review requires a
    non-empty reviewer identity.
    """

    import workspace_policy

    allowed, requirement = workspace_policy.promotion_allowed()
    if not allowed:
        return PromotionResult(
            ok=False, extension=name, status="",
            error="promotion_not_permitted_in_profile",
        )
    if requirement == "reviewer_identity" and not reviewed_by.strip():
        return PromotionResult(
            ok=False, extension=name, status="",
            error="reviewer_identity_required",
        )

    manifest = _load_manifest(name, project_root)
    current = extension_status(manifest)
    if current == STATUS_OPERATIONAL:
        return PromotionResult(ok=True, extension=name, status=current,
                               error="already_operational")

    gates = [
        _gate_manifest_schema(name, manifest, project_root),
        _gate_ontology_files_parse(name, manifest, project_root),
        _gate_classes_anchored(name, manifest, project_root),
        _gate_exemplars_validate(name, manifest, project_root, require_validator),
        _gate_negative_fixtures(name, manifest, project_root, require_validator),
        _gate_competency_queries(name, manifest, project_root),
    ]
    failed = [g for g in gates if not g["ok"]]
    if failed:
        return PromotionResult(
            ok=False, extension=name, status=current, gates=gates,
            error=f"promotion_gate_failed:{failed[0]['gate']}",
        )

    manifest["status"] = STATUS_OPERATIONAL
    manifest["promotion"] = {
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "reviewed_by": reviewed_by or "unrecorded",
        "previous_status": current,
        "deployment_profile": workspace_policy.deployment_profile(),
        "commit": _git_commit_sha(project_root),
        "gates": gates,
    }
    # Invalidate declared-term caches so the promoted concepts are live
    # immediately (belt-and-braces; the fingerprint key also detects this).
    _clear_concept_caches()
    _manifest_path(name, project_root).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return PromotionResult(ok=True, extension=name, status=STATUS_OPERATIONAL, gates=gates)


def deprecate_extension(
    name: str,
    reason: str,
    project_root: Path = PROJECT_ROOT,
    deprecated_by: str = "",
) -> dict:
    """Emergency revocation: mark an extension deprecated (kept on disk with
    provenance, excluded from routing discovery)."""

    manifest = _load_manifest(name, project_root)
    manifest["status"] = STATUS_DEPRECATED
    manifest["deprecation"] = {
        "deprecated_at": datetime.now(timezone.utc).isoformat(),
        "deprecated_by": deprecated_by or "unrecorded",
        "reason": reason,
    }
    _manifest_path(name, project_root).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    _clear_concept_caches()
    return {"ok": True, "extension": name, "status": STATUS_DEPRECATED, "reason": reason}


# ---------------------------------------------------------------------------
# Recipe promotion (issue #56)
# ---------------------------------------------------------------------------

_RECIPE_INDEX_MARKER = "RECIPE_INDEX: list[dict[str, str]] = ["
_LEARNED_SECTION_HEADER = "### Learned recipes (promoted from candidates)"


def _recipe_structure_errors(text: str, recipes_dir: Path, slug: str) -> list[str]:
    """Validate the required recipe structure (docs/recipes/recipe-authoring.md)."""

    errors: list[str] = []
    if not re.search(r"^# \S", text, flags=re.MULTILINE):
        errors.append("missing title heading (# ...)")
    if "when to use" not in text.lower():
        errors.append('missing "When to use this recipe" section')
    if "```" not in text:
        errors.append("missing validated snippet (no code fence)")
    if not re.search(r"^#+ Related", text, flags=re.MULTILINE):
        errors.append("missing Related section")
    else:
        links = set(re.findall(r"\(([a-z0-9-]+\.md)\)", text)) - {f"{slug}.md"}
        existing = {p.name for p in recipes_dir.glob("*.md")}
        if not (links & existing):
            errors.append("Related section links no existing operational recipe")
    return errors


def promote_recipe(
    slug: str,
    description: str,
    keywords: str,
    project_root: Path = PROJECT_ROOT,
    reviewed_by: str = "",
) -> dict:
    """Promote a candidate recipe into the operational catalog.

    Verifies required structure, then transactionally: moves
    ``docs/recipes/candidates/<slug>.md`` to ``docs/recipes/<slug>.md``,
    appends a row to ``docs/recipes/INDEX.md``, registers an entry in
    ``RECIPE_INDEX`` (``mcp_server/domain_index.py``), and appends promotion
    provenance to ``docs/recipes/promotion-log.json``. Any gate failure
    leaves every operational file unchanged.
    """

    import workspace_policy

    allowed, requirement = workspace_policy.promotion_allowed()
    if not allowed:
        return {"ok": False, "error": "promotion_not_permitted_in_profile"}
    if requirement == "reviewer_identity" and not reviewed_by.strip():
        return {"ok": False, "error": "reviewer_identity_required"}
    if not description.strip() or not keywords.strip():
        return {"ok": False, "error": "recipe_metadata_required",
                "detail": "description and keywords are required for RECIPE_INDEX"}

    recipes_dir = project_root / RECIPE_DIR
    candidate_path = project_root / CANDIDATE_RECIPE_DIR / f"{slug}.md"
    target_path = recipes_dir / f"{slug}.md"
    index_md_path = recipes_dir / "INDEX.md"
    domain_index_path = project_root / "mcp_server" / "domain_index.py"

    if not candidate_path.is_file():
        return {"ok": False, "error": "candidate_recipe_missing"}
    if target_path.exists():
        return {"ok": False, "error": "recipe_already_operational"}

    text = candidate_path.read_text(encoding="utf-8")
    structure_errors = _recipe_structure_errors(text, recipes_dir, slug)
    if structure_errors:
        return {"ok": False, "error": "recipe_structure_invalid",
                "detail": "; ".join(structure_errors)}

    # Ontology-term gate (#123): candidate prose, tables, snippets, diagrams,
    # and relationship literals must be grounded before executable validation.
    try:
        import recipe_lint
    except ImportError:
        sys.path.insert(0, str(project_root / "mcp_server"))
        import recipe_lint

    lint_report = recipe_lint.lint_recipes(
        project_root=project_root,
        selected_paths=[candidate_path],
    )
    if not lint_report.ok:
        return {
            "ok": False,
            "error": "recipe_ontology_lint_failed",
            "detail": lint_report.to_dict(),
        }

    # Executable gate (#69 / CQ-38): candidate plus every affected shared
    # profile/extension exemplar (and preferably the full operational set).
    try:
        from tools.run_recipe_examples import (
            entries_for_promotion_gate,
            run_manifest_entries,
        )
    except ImportError:
        sys.path.insert(0, str(project_root / "mcp_server"))
        from tools.run_recipe_examples import (
            entries_for_promotion_gate,
            run_manifest_entries,
        )

    gate_entries = entries_for_promotion_gate(slug)
    if not gate_entries:
        return {
            "ok": False,
            "error": "recipe_execution_metadata_missing",
            "detail": (
                "Candidate recipes must have a validated entry in "
                "docs/recipes/recipe-execution.json before promotion."
            ),
        }
    if not graph_validator.validator_available():
        return {
            "ok": False,
            "error": "validator_unavailable",
            "detail": "case_validate is required to promote recipes with "
            "executable exemplars (fail-closed).",
        }
    gate = run_manifest_entries(gate_entries, validate=True)
    if gate["failed"]:
        return {
            "ok": False,
            "error": "recipe_execution_gate_failed",
            "detail": gate,
        }

    title_match = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else slug

    # Prepare every write in memory first (transactional).
    index_md = index_md_path.read_text(encoding="utf-8")
    if _LEARNED_SECTION_HEADER not in index_md:
        index_md = (
            index_md.rstrip("\n")
            + f"\n\n{_LEARNED_SECTION_HEADER}\n\n"
            + "Recipes promoted from `candidates/` through the governed "
            + "lifecycle (`make promote-recipe`).\n\n"
            + "| Recipe | File | Description |\n|---|---|---|\n"
        )
    index_md = (
        index_md.rstrip("\n")
        + f"\n| {title} | [{slug}.md]({slug}.md) | {description} |\n"
    )

    domain_index_src = domain_index_path.read_text(encoding="utf-8")
    marker_pos = domain_index_src.find(_RECIPE_INDEX_MARKER)
    if marker_pos < 0:
        return {"ok": False, "error": "recipe_index_marker_missing"}
    close_pos = domain_index_src.find("\n]\n", marker_pos)
    if close_pos < 0:
        return {"ok": False, "error": "recipe_index_marker_missing"}
    entry_src = (
        "    {\n"
        f'        "title": {json.dumps(title)},\n'
        f'        "description": {json.dumps(description)},\n'
        f'        "keywords": {json.dumps(keywords)},\n'
        f'        "file": {json.dumps(f"{RECIPE_DIR}/{slug}.md")},\n'
        "    },\n"
    )
    domain_index_src = (
        domain_index_src[: close_pos + 1] + entry_src + domain_index_src[close_pos + 1:]
    )

    log_path = project_root / RECIPE_PROMOTION_LOG
    log_entries = []
    if log_path.is_file():
        try:
            log_entries = json.loads(log_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"ok": False, "error": "promotion_log_malformed"}
    log_entries.append({
        "artifact": f"{RECIPE_DIR}/{slug}.md",
        "action": "promote",
        "title": title,
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "reviewed_by": reviewed_by or "unrecorded",
        "deployment_profile": workspace_policy.deployment_profile(),
        "commit": _git_commit_sha(project_root),
    })

    # CQ-37: OS lock + staging directory; commit with os.replace or roll back.
    commit_error = _commit_recipe_promotion(
        project_root=project_root,
        slug=slug,
        recipe_text=text,
        index_md=index_md,
        domain_index_src=domain_index_src,
        log_entries=log_entries,
        candidate_path=candidate_path,
        target_path=target_path,
        index_md_path=index_md_path,
        domain_index_path=domain_index_path,
        log_path=log_path,
    )
    if commit_error:
        return {"ok": False, "error": commit_error}

    return {"ok": True, "recipe": f"{RECIPE_DIR}/{slug}.md", "title": title}


def _commit_recipe_promotion(
    *,
    project_root: Path,
    slug: str,
    recipe_text: str,
    index_md: str,
    domain_index_src: str,
    log_entries: list,
    candidate_path: Path,
    target_path: Path,
    index_md_path: Path,
    domain_index_path: Path,
    log_path: Path,
) -> str | None:
    """Atomically commit promotion artifacts under an exclusive lock (CQ-37).

    Returns an error code string on failure, or ``None`` on success. On any
    failure after staging, previously-written finals are restored from
    backups when available so operational files are not left half-updated.
    """

    recipes_dir = project_root / RECIPE_DIR
    lock_path = recipes_dir / ".promotion.lock"
    staging_root = recipes_dir / ".promotion-staging" / slug
    backups: dict[Path, Path] = {}

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_fh = open(lock_path, "a+", encoding="utf-8")
    try:
        if fcntl is not None:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX)

        if staging_root.exists():
            shutil.rmtree(staging_root)
        staging_root.mkdir(parents=True)

        staged = {
            "recipe.md": recipe_text,
            "INDEX.md": index_md,
            "domain_index.py": domain_index_src,
            "promotion-log.json": json.dumps(log_entries, indent=2) + "\n",
        }
        for name, content in staged.items():
            (staging_root / name).write_text(content, encoding="utf-8")

        finals = {
            staging_root / "INDEX.md": index_md_path,
            staging_root / "domain_index.py": domain_index_path,
            staging_root / "promotion-log.json": log_path,
            staging_root / "recipe.md": target_path,
        }

        try:
            for staged_path, final_path in finals.items():
                final_path.parent.mkdir(parents=True, exist_ok=True)
                if final_path.exists():
                    backup = staging_root / f"backup-{final_path.name}"
                    shutil.copy2(final_path, backup)
                    backups[final_path] = backup
                os.replace(staged_path, final_path)
            candidate_path.unlink(missing_ok=True)
        except OSError as exc:
            for final_path, backup in backups.items():
                try:
                    os.replace(backup, final_path)
                except OSError:
                    _logger.exception("Failed to restore %s after promotion error", final_path)
            if target_path.exists() and target_path not in backups:
                try:
                    target_path.unlink()
                except OSError:
                    # Best-effort rollback cleanup; primary restore is via backups.
                    _logger.warning(
                        "Could not remove partially promoted recipe %s during rollback",
                        target_path,
                        exc_info=True,
                    )
            _logger.exception("Recipe promotion commit failed for %s: %s", slug, exc)
            return "promotion_commit_failed"
        finally:
            shutil.rmtree(staging_root, ignore_errors=True)
    finally:
        if fcntl is not None:
            try:
                fcntl.flock(lock_fh.fileno(), fcntl.LOCK_UN)
            except OSError:
                # Unlock failures are non-fatal; process exit releases the lock.
                _logger.debug("fcntl unlock failed for promotion lock", exc_info=True)
        lock_fh.close()

    return None


def deprecate_recipe(
    slug: str,
    reason: str,
    project_root: Path = PROJECT_ROOT,
    deprecated_by: str = "",
) -> dict:
    """Revoke an operational recipe: unregister it from both indexes and
    move it back to ``docs/recipes/candidates/`` with provenance."""

    recipes_dir = project_root / RECIPE_DIR
    target_path = recipes_dir / f"{slug}.md"
    candidate_path = project_root / CANDIDATE_RECIPE_DIR / f"{slug}.md"
    index_md_path = recipes_dir / "INDEX.md"
    domain_index_path = project_root / "mcp_server" / "domain_index.py"

    if not target_path.is_file():
        return {"ok": False, "error": "recipe_not_operational"}

    index_md = index_md_path.read_text(encoding="utf-8")
    index_md = "\n".join(
        line for line in index_md.splitlines() if f"({slug}.md)" not in line
    ) + "\n"

    domain_index_src = domain_index_path.read_text(encoding="utf-8")
    entry_re = re.compile(
        r"    \{\n(?:.*\n)*?"
        rf'        "file": "{re.escape(RECIPE_DIR)}/{re.escape(slug)}\.md",\n'
        r"    \},\n"
    )
    domain_index_src = entry_re.sub("", domain_index_src, count=1)

    log_path = project_root / RECIPE_PROMOTION_LOG
    log_entries = []
    if log_path.is_file():
        try:
            log_entries = json.loads(log_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"ok": False, "error": "promotion_log_malformed"}
    log_entries.append({
        "artifact": f"{RECIPE_DIR}/{slug}.md",
        "action": "deprecate",
        "reason": reason,
        "deprecated_at": datetime.now(timezone.utc).isoformat(),
        "deprecated_by": deprecated_by or "unrecorded",
    })

    index_md_path.write_text(index_md, encoding="utf-8")
    domain_index_path.write_text(domain_index_src, encoding="utf-8")
    log_path.write_text(json.dumps(log_entries, indent=2) + "\n", encoding="utf-8")
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(target_path.read_text(encoding="utf-8"), encoding="utf-8")
    target_path.unlink()

    return {"ok": True, "recipe": f"{CANDIDATE_RECIPE_DIR}/{slug}.md", "reason": reason}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Knowledge artifact lifecycle management.")
    sub = parser.add_subparsers(dest="command", required=True)

    promote = sub.add_parser("promote", help="Promote a candidate extension to operational.")
    promote.add_argument("extension")
    promote.add_argument("--reviewed-by", default="")
    promote.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    deprecate = sub.add_parser("deprecate", help="Deprecate (revoke) an extension.")
    deprecate.add_argument("extension")
    deprecate.add_argument("--reason", required=True)
    deprecate.add_argument("--deprecated-by", default="")
    deprecate.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    status = sub.add_parser("status", help="Show lifecycle status of every extension.")
    status.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    promote_r = sub.add_parser(
        "promote-recipe", help="Promote a candidate recipe into the catalog."
    )
    promote_r.add_argument("slug")
    promote_r.add_argument("--description", required=True)
    promote_r.add_argument("--keywords", required=True)
    promote_r.add_argument("--reviewed-by", default="")
    promote_r.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    deprecate_r = sub.add_parser(
        "deprecate-recipe", help="Revoke an operational recipe back to candidates."
    )
    deprecate_r.add_argument("slug")
    deprecate_r.add_argument("--reason", required=True)
    deprecate_r.add_argument("--deprecated-by", default="")
    deprecate_r.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    args = parser.parse_args(argv)
    if args.command == "promote":
        result = promote_extension(
            args.extension, project_root=args.project_root, reviewed_by=args.reviewed_by
        )
        for gate in result.gates:
            marker = "PASS" if gate["ok"] else "FAIL"
            print(f"[{marker}] {gate['gate']}: {gate['detail']}")
        if result.ok:
            print(f"{result.extension}: {result.status}"
                  + (f" ({result.error})" if result.error else ""))
            return 0
        print(f"Promotion failed: {result.error}")
        return 1
    if args.command == "deprecate":
        result = deprecate_extension(
            args.extension, reason=args.reason,
            project_root=args.project_root, deprecated_by=args.deprecated_by,
        )
        print(f"{result['extension']}: {result['status']} — {result['reason']}")
        return 0
    if args.command == "status":
        for ext_dir in extension_paths.iter_extension_dirs(args.project_root):
            manifest = json.loads((ext_dir / "manifest.json").read_text(encoding="utf-8"))
            print(f"{ext_dir.name}: {extension_status(manifest)}")
        return 0
    if args.command == "promote-recipe":
        result = promote_recipe(
            args.slug, description=args.description, keywords=args.keywords,
            project_root=args.project_root, reviewed_by=args.reviewed_by,
        )
        if result["ok"]:
            print(f"promoted: {result['recipe']}")
            return 0
        print(f"Recipe promotion failed: {result['error']}"
              + (f" — {result['detail']}" if result.get("detail") else ""))
        return 1
    if args.command == "deprecate-recipe":
        result = deprecate_recipe(
            args.slug, reason=args.reason,
            project_root=args.project_root, deprecated_by=args.deprecated_by,
        )
        if result["ok"]:
            print(f"deprecated to: {result['recipe']}")
            return 0
        print(f"Recipe deprecation failed: {result['error']}")
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
