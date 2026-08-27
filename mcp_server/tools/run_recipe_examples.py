#!/usr/bin/env python3
"""Recipe exemplar quality gate (#69 / #124 / CQ-01–CQ-12).

Runs entries in ``docs/recipes/recipe-execution.json``. ``--all`` requires
every operational recipe to have execution metadata and, with
``--validate``, SHACL plus strict concept coverage. Builders run in
isolated temporary directories with a subprocess timeout. Outputs are
RDF-parsed (JSON-LD/Turtle via RDFLib) before validation. When
``--validate`` is set, ``case_validate`` must be available (fail-closed).

Usage:
  python mcp_server/tools/run_recipe_examples.py --category upper-ontology
  python mcp_server/tools/run_recipe_examples.py --all --validate
  python mcp_server/tools/run_recipe_examples.py --all --validate --report /tmp/report.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/recipes/recipe-execution.json"
SCHEMA = ROOT / "docs/recipes/recipe-execution.schema.json"
DEFAULT_TIMEOUT_SECONDS = 120
_logger = logging.getLogger(__name__)


def _repo_import_paths() -> tuple[str, str]:
    """Return checkout paths needed by builders and validation imports."""
    return str(ROOT / "python"), str(ROOT / "mcp_server")


def _ensure_repo_import_paths() -> None:
    """Make checkout packages importable when this file is run as a script."""
    for path in reversed(_repo_import_paths()):
        if path not in sys.path:
            sys.path.insert(0, path)


def _repo_subprocess_env() -> dict[str, str]:
    """Return a child environment with checkout packages first on PYTHONPATH."""
    env = os.environ.copy()
    repo_paths = list(_repo_import_paths())
    inherited = [
        path
        for path in env.get("PYTHONPATH", "").split(os.pathsep)
        if path and path not in repo_paths
    ]
    env["PYTHONPATH"] = os.pathsep.join([*repo_paths, *inherited])
    return env


def _package_version(dist_name: str) -> str | None:
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version(dist_name)
    except Exception:
        return None


def resolve_repo_path(rel: str, *, must_exist: bool = False, kind: str = "path") -> Path:
    """Resolve a repo-relative path and reject anything outside ROOT (CQ-08)."""
    if not isinstance(rel, str) or not rel.strip():
        raise ValueError(f"{kind}_empty")
    raw = Path(rel)
    if raw.is_absolute() or rel.startswith("/") or rel.startswith("~"):
        raise ValueError(f"path_outside_repo:{rel}")
    # Normalize and reject escape attempts before resolve().
    parts = raw.parts
    if ".." in parts:
        # Allow internal ".." only if the final resolved path stays in ROOT.
        pass
    candidate = (ROOT / raw).resolve()
    root_resolved = ROOT.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"path_outside_repo:{rel}") from exc
    if must_exist and not candidate.exists():
        raise ValueError(f"{kind}_missing:{rel}")
    return candidate


def validate_manifest_schema(data: dict) -> None:
    """Validate recipe-execution.json against its JSON Schema (CQ-07)."""
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError(
            "jsonschema is required to validate recipe-execution.json"
        ) from exc
    if not SCHEMA.is_file():
        raise FileNotFoundError(f"schema_missing:{SCHEMA}")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(instance=data, schema=schema)


def load_manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest_schema(data)
    return data


def _rdf_parse(path: Path) -> None:
    """Parse graph as RDF; raise ValueError on failure."""
    import rdflib

    g = rdflib.Graph()
    suffix = path.suffix.lower()
    if suffix in {".json", ".jsonld", ".json-ld"}:
        fmt = "json-ld"
    elif suffix in {".ttl", ".turtle"}:
        fmt = "turtle"
    else:
        raise ValueError(f"unsupported_graph_extension:{suffix}")
    g.parse(str(path), format=fmt)
    if len(g) == 0:
        raise ValueError("empty_rdf_graph")


def _load_jsonld_graph(path: Path) -> dict[str, Any]:
    """Load a JSON-LD graph document for auxiliary lint gates."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("jsonld_root_must_be_object")
    return payload


def _lint_relationship_kinds_if_present(
    graph_path: Path, result: dict[str, Any]
) -> bool:
    """Run relationship-kind lint when the graph uses kindOfRelationship.

    Returns False when lint reports errors (strict/open per caller policy).
    """
    suffix = graph_path.suffix.lower()
    if suffix not in {".json", ".jsonld", ".json-ld"}:
        return True
    mcp_root = str(ROOT / "mcp_server")
    if mcp_root not in sys.path:
        sys.path.insert(0, mcp_root)
    from relationship_kinds import graph_uses_relationship_kinds, lint_relationship_kinds

    graph_doc = _load_jsonld_graph(graph_path)
    if not graph_uses_relationship_kinds(graph_doc):
        return True
    lint_report = lint_relationship_kinds(
        graph_doc,
        allow_open_vocabulary=False,
    )
    result["relationship_kind_lint"] = lint_report
    if not lint_report.get("ok", True):
        result["error"] = "relationship_kind_lint_failed"
        return False
    return True


def _canonicalize_term(term: Any) -> str:
    """Stable string form for SPARQL binding comparison (CQ-06).

    Manifest ``expected_bindings`` use plain IRI / lexical strings; RDFLib
    terms are reduced to the same forms so JSON expectations match query rows.
    """
    try:
        from rdflib import BNode, Literal, URIRef
    except ImportError:
        return str(term)
    if isinstance(term, URIRef):
        return str(term)
    if isinstance(term, Literal):
        lexical = str(term)
        if term.datatype:
            return f"{lexical}^^{term.datatype}"
        if term.language:
            return f"{lexical}@{term.language}"
        return lexical
    if isinstance(term, BNode):
        return f"_:{term}"
    return str(term)


def _canonicalize_bindings(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for row in rows:
        normalized.append({str(k): _canonicalize_term(v) for k, v in row.items()})
    return sorted(normalized, key=lambda d: json.dumps(d, sort_keys=True))


def _run_competency_queries(graph_path: Path, queries: list[dict]) -> list[dict]:
    """Run SPARQL SELECT queries and compare canonical expected bindings (CQ-06)."""
    import rdflib

    g = rdflib.Graph()
    fmt = (
        "json-ld"
        if graph_path.suffix.lower() in {".json", ".jsonld", ".json-ld"}
        else "turtle"
    )
    g.parse(str(graph_path), format=fmt)
    outcomes: list[dict] = []
    for spec in queries:
        qrel = spec["query"]
        detail: dict = {"query": qrel, "ok": False}
        try:
            qpath = resolve_repo_path(qrel, must_exist=True, kind="query")
            sparql = qpath.read_text(encoding="utf-8")
            result = g.query(sparql)
            var_names = [str(v) for v in result.vars] if result.vars else []
            actual_rows: list[dict[str, Any]] = []
            for row in result:
                actual_rows.append(
                    {var_names[i]: row[i] for i in range(len(var_names))}
                )
            actual_canon = _canonicalize_bindings(actual_rows)
            detail["actual_count"] = len(actual_canon)
            detail["actual_bindings"] = actual_canon

            expected_raw = spec.get("expected_bindings")
            if expected_raw is None:
                detail["error"] = "expected_bindings_required"
                outcomes.append(detail)
                continue
            expected_canon = _canonicalize_bindings(
                [{str(k): v for k, v in row.items()} for row in expected_raw]
            )
            detail["expected_bindings"] = expected_canon

            ok = actual_canon == expected_canon
            if not ok:
                detail["error"] = "bindings_mismatch"

            expected_count = spec.get("expected_count")
            if expected_count is not None and len(actual_canon) != int(expected_count):
                ok = False
                detail["error"] = f"expected_count:{expected_count}"

            min_count = spec.get("min_count")
            if min_count is not None and len(actual_canon) < int(min_count):
                ok = False
                detail["error"] = f"min_count:{min_count}"

            detail["ok"] = ok
        except Exception as exc:
            detail["error"] = f"sparql_failed:{type(exc).__name__}:{exc}"
            detail["ok"] = False
        outcomes.append(detail)
    return outcomes


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sanitize_command(argv: list[str]) -> list[str]:
    """Return argv with absolute paths relativized to ROOT when possible."""
    out: list[str] = []
    root = str(ROOT.resolve())
    for arg in argv:
        try:
            p = Path(arg).resolve()
            if str(p).startswith(root):
                out.append(str(p.relative_to(ROOT)))
            else:
                out.append(Path(arg).name if os.sep in arg else arg)
        except Exception:
            out.append(arg)
    return out


def _copy_support_into_workspace(entry: dict, tmp_dir: Path) -> None:
    """Copy declared support_files / support_dirs into the temp workspace (CQ-09)."""
    for rel in entry.get("support_files") or []:
        src = resolve_repo_path(rel, must_exist=True, kind="support_file")
        if not src.is_file():
            raise ValueError(f"support_file_not_file:{rel}")
        dest = tmp_dir / src.name
        shutil.copy2(src, dest)
    for rel in entry.get("support_dirs") or []:
        src = resolve_repo_path(rel, must_exist=True, kind="support_dir")
        if not src.is_dir():
            raise ValueError(f"support_dir_not_dir:{rel}")
        dest = tmp_dir / src.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)


def _match_negative_expectation(spec: dict, diagnostics: str) -> str | None:
    """Return an error string if expected identifiers are absent from diagnostics."""
    checks = (
        ("expected_violation", spec.get("expected_violation")),
        ("expected_constraint", spec.get("expected_constraint")),
        ("expected_failure_code", spec.get("expected_failure_code")),
    )
    present = [(kind, needle) for kind, needle in checks if needle]
    if not present:
        return "expect_invalid_missing_expectation"
    for kind, needle in present:
        if str(needle) not in diagnostics:
            return f"expect_invalid_{kind}_not_found:{needle}"
    return None


def _run_entry_body(
    entry: dict,
    result: dict,
    *,
    validate: bool,
    timeout_seconds: int,
    keep_generated: bool,
) -> None:
    builder_rel = entry["builder"]
    output_rel = entry["output"]
    builder = resolve_repo_path(builder_rel, must_exist=True, kind="builder")
    if not builder.is_file():
        result["error"] = "builder_missing"
        return
    # Touch output path for containment only (file may not exist yet).
    resolve_repo_path(output_rel, kind="output")
    if entry.get("recipe"):
        resolve_repo_path(entry["recipe"], must_exist=True, kind="recipe")

    output_name = Path(output_rel).name
    python_exe = sys.executable
    result["python_executable"] = python_exe
    result["python_version"] = sys.version.split()[0]
    result["rdflib_version"] = _package_version("rdflib")
    result["validator_version"] = _package_version("case-utils")

    with tempfile.TemporaryDirectory(prefix=f"recipe-{entry['id']}-") as tmp:
        tmp_dir = Path(tmp)
        tmp_builder = tmp_dir / builder.name
        shutil.copy2(builder, tmp_builder)
        _copy_support_into_workspace(entry, tmp_dir)

        inherited_pythonpath = os.environ.get("PYTHONPATH")
        env = _repo_subprocess_env()
        result["pythonpath"] = env["PYTHONPATH"]
        result["pythonpath_components"] = ["repo:python", "repo:mcp_server"]
        if inherited_pythonpath:
            result["pythonpath_components"].append("env:PYTHONPATH")

        cmd = [python_exe, str(tmp_builder)]
        result["command"] = _sanitize_command(cmd)

        builder_t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(tmp_dir),
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds,
                env=env,
            )
        except subprocess.TimeoutExpired:
            result["error"] = "builder_timeout"
            result["builder_duration_ms"] = round(
                (time.perf_counter() - builder_t0) * 1000, 3
            )
            result["exit_code"] = None
            return
        result["builder_duration_ms"] = round(
            (time.perf_counter() - builder_t0) * 1000, 3
        )
        result["exit_code"] = proc.returncode
        if proc.returncode != 0:
            result["error"] = "builder_failed"
            result["stderr"] = (proc.stderr or "")[-2000:]
            return

        # CQ-10: exact output path under temp workspace (filename next to builder).
        tmp_output = tmp_dir / output_name
        if not tmp_output.is_file():
            result["error"] = "output_missing"
            result["stdout"] = (proc.stdout or "")[-1000:]
            result["expected_output_path"] = str(tmp_output)
            return

        try:
            _rdf_parse(tmp_output)
        except Exception as exc:
            result["error"] = f"rdf_parse_failed:{type(exc).__name__}:{exc}"
            return

        if not _lint_relationship_kinds_if_present(tmp_output, result):
            return

        result["output_sha256"] = _sha256_file(tmp_output)

        if not validate:
            # CQ-04: keep only after all applicable gates (here: build + parse).
            if keep_generated:
                dest = resolve_repo_path(output_rel, kind="output")
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(tmp_output, dest)
                result["committed_output"] = str(dest.relative_to(ROOT))
            result["ok"] = True
            return

        if entry.get("profiles") is None and entry.get("extensions") is None:
            result["error"] = "validation_profiles_required"
            return

        _ensure_repo_import_paths()
        from graph_validator import validate_graph_file, validator_available

        if not validator_available():
            result["error"] = "validator_unavailable"
            return

        validation_t0 = time.perf_counter()
        report = validate_graph_file(
            tmp_output,
            project_root=ROOT,
            extensions=entry.get("extensions"),
            profiles=entry.get("profiles") or None,
            strict_concepts=bool(entry.get("strict_concepts", True)),
            allow_foundational_pair=bool(entry.get("allow_foundational_pair", False)),
        )
        result["validation_duration_ms"] = round(
            (time.perf_counter() - validation_t0) * 1000, 3
        )
        result["conforms"] = report.conforms
        result["verification_status"] = report.verification_status
        result["summary"] = report.safe_summary
        result["bundle_fingerprint"] = report.bundle_fingerprint
        result["selected_profiles"] = list(report.selected_profiles)
        result["validator_exit_code"] = report.exit_code
        if report.conforms is not True:
            result["error"] = "validation_failed"
            return
        if report.verification_status != "complete":
            result["error"] = f"verification_incomplete:{report.verification_status}"
            return

        # CQ-05: negative fixtures with strong expectations.
        for invalid_spec in entry.get("expect_invalid") or []:
            if isinstance(invalid_spec, str):
                result["error"] = (
                    "expect_invalid_must_be_object:"
                    "provide expected_violation|expected_constraint|"
                    "expected_failure_code"
                )
                return
            invalid_path = invalid_spec["path"]
            invalid_file = resolve_repo_path(
                invalid_path, must_exist=True, kind="expect_invalid"
            )
            if not invalid_file.is_file():
                result["error"] = f"expect_invalid_missing:{invalid_path}"
                return
            try:
                _rdf_parse(invalid_file)
            except Exception as exc:
                result["error"] = (
                    f"expect_invalid_rdf_parse_failed:{type(exc).__name__}:{exc}"
                )
                return
            if not validator_available():
                result["error"] = "validator_unavailable"
                return
            invalid_report = validate_graph_file(
                invalid_file,
                project_root=ROOT,
                extensions=entry.get("extensions"),
                profiles=entry.get("profiles") or None,
                strict_concepts=bool(entry.get("strict_concepts", True)),
                allow_foundational_pair=bool(
                    entry.get("allow_foundational_pair", False)
                ),
            )
            if invalid_report.verification_status != "complete":
                result["error"] = (
                    f"expect_invalid_verification_incomplete:"
                    f"{invalid_path}:{invalid_report.verification_status}"
                )
                return
            if invalid_report.conforms is True:
                result["error"] = f"expect_invalid_conforms:{invalid_path}"
                return
            match_err = _match_negative_expectation(
                invalid_spec,
                "\n".join(
                    part
                    for part in (
                        invalid_report.validator_diagnostics,
                        invalid_report.safe_summary,
                        " ".join(invalid_report.undeclared_concepts),
                    )
                    if part
                ),
            )
            if match_err:
                result["error"] = f"{match_err}:{invalid_path}"
                return
            result.setdefault("expect_invalid_results", []).append(
                {
                    "path": invalid_path,
                    "conforms": invalid_report.conforms,
                    "verification_status": invalid_report.verification_status,
                    "violation_count": invalid_report.violation_count,
                    "exit_code": invalid_report.exit_code,
                }
            )

        competency = entry.get("competency_queries") or []
        if competency:
            query_t0 = time.perf_counter()
            outcomes = _run_competency_queries(tmp_output, competency)
            result["query_duration_ms"] = round(
                (time.perf_counter() - query_t0) * 1000, 3
            )
            result["competency_queries"] = outcomes
            if any(not o.get("ok") for o in outcomes):
                result["error"] = "competency_query_failed"
                return

        # CQ-04: promote generated output only after every gate succeeds.
        if keep_generated:
            dest = resolve_repo_path(output_rel, kind="output")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_output, dest)
            result["committed_output"] = str(dest.relative_to(ROOT))

        result["ok"] = True


def run_entry(
    entry: dict,
    *,
    validate: bool,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    keep_generated: bool = False,
) -> dict:
    """Run one manifest entry; never raise — return a typed failed result (CQ-01)."""
    result: dict[str, Any] = {
        "id": entry.get("id", "unknown"),
        "ok": False,
        "builder": entry.get("builder"),
        "output": entry.get("output"),
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
    }
    t0 = time.perf_counter()
    try:
        _run_entry_body(
            entry,
            result,
            validate=validate,
            timeout_seconds=timeout_seconds,
            keep_generated=keep_generated,
        )
    except Exception as exc:
        result["ok"] = False
        result["error"] = f"unhandled:{type(exc).__name__}:{exc}"
    finally:
        result["total_duration_ms"] = round((time.perf_counter() - t0) * 1000, 3)
    return result


def run_manifest_entries(
    entries: list[dict],
    *,
    validate: bool,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    keep_generated: bool = False,
) -> dict:
    results = [
        run_entry(
            e,
            validate=validate,
            timeout_seconds=timeout_seconds,
            keep_generated=keep_generated,
        )
        for e in entries
    ]
    failed = [r for r in results if not r["ok"]]
    return {
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "rdflib_version": _package_version("rdflib"),
        "validator_version": _package_version("case-utils"),
    }


def operational_recipe_coverage(manifest: dict | None = None) -> dict[str, Any]:
    """Report whether every operational recipe has execution metadata (#124)."""
    from recipe_lint import operational_recipe_paths

    data = manifest or load_manifest()
    registered = {
        Path(entry["recipe"]).name
        for entry in data.get("recipes") or []
        if entry.get("recipe")
    }
    operational = [
        path.name
        for path in operational_recipe_paths(ROOT)
        if path.name != "INDEX.md"
    ]
    missing = sorted(name for name in operational if name not in registered)
    return {
        "operational_recipes": len(operational),
        "registered_recipes": len(registered & set(operational)),
        "registered_entries": len(data.get("recipes") or []),
        "missing_recipes": missing,
        "complete": not missing,
    }


def entries_for_recipe_slug(slug: str) -> list[dict]:
    """Return execution-manifest entries whose recipe path matches ``slug``."""
    manifest = load_manifest()
    needle = f"{slug}.md"
    return [
        e
        for e in manifest["recipes"]
        if Path(e.get("recipe", "")).name == needle or e.get("id") == slug
    ]


def entries_for_promotion_gate(
    slug: str,
    *,
    include_full_manifest: bool = False,
) -> list[dict]:
    """CQ-38: candidate entries plus every exemplar sharing profiles/extensions.

    Returns an empty list when the candidate has no ``recipe-execution.json``
    entry. Callers (``promote_recipe``) **must** treat an empty result as a
    fail-closed error (``recipe_execution_metadata_missing``) — promotion
    without executable metadata is not permitted.

    When the candidate *is* registered, expand to every operational entry that
    shares an extension or profile. Pass ``include_full_manifest=True`` to
    require the entire operational execution catalog before catalog mutation.
    """
    manifest = load_manifest()
    all_entries = list(manifest.get("recipes") or [])
    candidate = entries_for_recipe_slug(slug)
    if not candidate:
        return []
    if include_full_manifest:
        return all_entries

    seed_ext: set[str] = set()
    seed_prof: set[str] = set()
    candidate_ids: set[str] = set()
    for entry in candidate:
        candidate_ids.add(str(entry.get("id") or entry.get("recipe") or ""))
        seed_ext.update(str(x) for x in (entry.get("extensions") or []))
        seed_prof.update(str(x) for x in (entry.get("profiles") or []))

    affected: list[dict] = []
    seen: set[str] = set()
    for entry in all_entries:
        eid = str(entry.get("id") or entry.get("recipe") or id(entry))
        if eid in seen:
            continue
        e_ext = {str(x) for x in (entry.get("extensions") or [])}
        e_prof = {str(x) for x in (entry.get("profiles") or [])}
        if (
            eid in candidate_ids
            or entry in candidate
            or (seed_ext and seed_ext & e_ext)
            or (seed_prof and seed_prof & e_prof)
        ):
            seen.add(eid)
            affected.append(entry)

    return affected or list(candidate)

def write_report_atomic(report_path: Path, summary: dict) -> None:
    """Atomically write JSON report (CQ-02 / CQ-03)."""
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{report_path.name}.",
        suffix=".tmp",
        dir=str(report_path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=2)
            fh.write("\n")
        os.replace(tmp_name, report_path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            # Temp file may already be gone; ignore cleanup race.
            _logger.debug("Could not unlink temp report %s", tmp_name, exc_info=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", default="upper-ontology")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--keep-generated",
        action="store_true",
        help="Copy builder output back into the repository tree after all "
        "gates succeed for that entry.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Write machine-readable JSON report to this path.",
    )
    args = parser.parse_args()

    summary: dict[str, Any] = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "results": [],
        "error": "not_started",
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
    }
    try:
        try:
            manifest = load_manifest()
        except Exception as exc:
            summary = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "results": [],
                "error": f"manifest_invalid:{type(exc).__name__}:{exc}",
                "python_executable": sys.executable,
                "python_version": sys.version.split()[0],
            }
            print(json.dumps(summary, indent=2))
            return 1

        entries = manifest["recipes"]
        if args.id:
            entries = [e for e in entries if e["id"] in args.id]
        elif not args.all:
            entries = [e for e in entries if e.get("category") == args.category]

        summary = run_manifest_entries(
            entries,
            validate=args.validate,
            timeout_seconds=args.timeout,
            keep_generated=args.keep_generated,
        )
        if args.all:
            summary["operational_coverage"] = operational_recipe_coverage(manifest)
            if not summary["operational_coverage"]["complete"]:
                summary["failed"] = int(summary.get("failed") or 0) + 1
                summary["error"] = "operational_coverage_incomplete"
        print(json.dumps(summary, indent=2))
        return 1 if summary["failed"] else 0
    except Exception as exc:
        summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "results": [],
            "error": f"unhandled:{type(exc).__name__}:{exc}",
            "python_executable": sys.executable,
            "python_version": sys.version.split()[0],
        }
        print(json.dumps(summary, indent=2))
        return 1
    finally:
        # CQ-02 / CQ-03: always write the aggregate report when requested.
        if args.report:
            try:
                write_report_atomic(Path(args.report), summary)
            except Exception as report_exc:
                print(
                    json.dumps(
                        {
                            "error": f"report_write_failed:{type(report_exc).__name__}",
                            "detail": str(report_exc),
                        }
                    ),
                    file=sys.stderr,
                )


if __name__ == "__main__":
    raise SystemExit(main())
