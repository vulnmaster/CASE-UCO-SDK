"""Unit tests for recipe execution gate (CQ-01 through CQ-12)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest

import tools.run_recipe_examples as runner

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _minimal_entry(**overrides: Any) -> dict:
    base = {
        "id": "unit-test-entry",
        "category": "test",
        "recipe": "docs/recipes/INDEX.md",
        "builder": "examples/upper-ontology/foundational-typing/build_bfo_variant.py",
        "output": "examples/upper-ontology/foundational-typing/foundational-typing-bfo.jsonld",
        "profiles": ["bfo"],
        "extensions": None,
        "strict_concepts": True,
    }
    base.update(overrides)
    return base


def test_manifest_validates_against_schema():
    data = runner.load_manifest()
    assert data["schema_version"] == "1.0"
    assert len(data["recipes"]) >= 1


def test_every_operational_recipe_has_execution_metadata():
    coverage = runner.operational_recipe_coverage()
    assert coverage["complete"], (
        "Operational recipes missing recipe-execution.json entries: "
        + ", ".join(coverage["missing_recipes"])
    )
    assert coverage["operational_recipes"] >= 80


def test_schema_rejects_string_expect_invalid(tmp_path, monkeypatch):
    bad = {
        "schema_version": "1.0",
        "recipes": [
            {
                "id": "bad-entry",
                "category": "test",
                "recipe": "docs/recipes/INDEX.md",
                "builder": "examples/upper-ontology/foundational-typing/build_bfo_variant.py",
                "output": "examples/upper-ontology/foundational-typing/foundational-typing-bfo.jsonld",
                "expect_invalid": [
                    "examples/upper-ontology/foundational-typing/invalid_category_mistake.jsonld"
                ],
            }
        ],
    }
    with pytest.raises(Exception):
        runner.validate_manifest_schema(bad)


def test_resolve_repo_path_rejects_escape():
    with pytest.raises(ValueError, match="path_outside_repo"):
        runner.resolve_repo_path("../etc/passwd")
    with pytest.raises(ValueError, match="path_outside_repo"):
        runner.resolve_repo_path("/etc/passwd")


def test_resolve_repo_path_accepts_in_repo():
    path = runner.resolve_repo_path("docs/recipes/recipe-execution.json", must_exist=True)
    assert path.is_file()
    assert path == PROJECT_ROOT / "docs/recipes/recipe-execution.json"


def test_run_entry_catches_exceptions(monkeypatch):
    def boom(*_a, **_k):
        raise RuntimeError("simulated")

    monkeypatch.setattr(runner, "_run_entry_body", boom)
    result = runner.run_entry(_minimal_entry(), validate=False)
    assert result["ok"] is False
    assert result["error"].startswith("unhandled:RuntimeError:")
    assert "total_duration_ms" in result


def test_write_report_atomic(tmp_path):
    report = tmp_path / "nested" / "out" / "report.json"
    payload = {"total": 1, "passed": 1, "failed": 0, "results": []}
    runner.write_report_atomic(report, payload)
    assert report.is_file()
    assert json.loads(report.read_text(encoding="utf-8")) == payload
    leftovers = list(report.parent.glob(".report.json.*.tmp"))
    assert leftovers == []


def test_main_writes_report_on_manifest_failure(tmp_path, monkeypatch):
    report = tmp_path / "gate" / "report.json"

    def bad_load():
        raise ValueError("broken_manifest")

    monkeypatch.setattr(runner, "load_manifest", bad_load)
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_recipe_examples.py", "--all", "--report", str(report)],
    )
    rc = runner.main()
    assert rc == 1
    assert report.is_file()
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["error"].startswith("manifest_invalid:")


def test_keep_generated_only_after_success(monkeypatch):
    """CQ-04: failed validation must not copy output into the repo tree."""
    copied: list[tuple[str, str]] = []

    def tracking_copy2(src, dst, *a, **k):
        copied.append((str(src), str(dst)))
        return None

    monkeypatch.setattr(runner.shutil, "copy2", tracking_copy2)

    def failing_validate(entry, result, **kwargs):
        result["error"] = "validation_failed"
        result["ok"] = False

    monkeypatch.setattr(runner, "_run_entry_body", failing_validate)
    result = runner.run_entry(_minimal_entry(), validate=True, keep_generated=True)
    assert result["ok"] is False
    assert copied == []
    assert "committed_output" not in result


def test_exact_output_path_no_rglob(tmp_path, monkeypatch):
    """CQ-10: nested same-basename files must not satisfy the declared output."""
    builder = tmp_path / "build_stub.py"
    builder.write_text(
        "from pathlib import Path\n"
        "HERE = Path(__file__).resolve().parent\n"
        "(HERE / 'nested').mkdir(exist_ok=True)\n"
        "(HERE / 'nested' / 'out.jsonld').write_text('{\"@graph\":[]}\\n')\n",
        encoding="utf-8",
    )
    entry = {
        "id": "exact-path",
        "category": "test",
        "recipe": "docs/recipes/INDEX.md",
        "builder": "docs/recipes/INDEX.md",
        "output": "does-not-matter/out.jsonld",
        "profiles": ["bfo"],
    }

    def fake_resolve(rel, *, must_exist=False, kind="path"):
        if kind == "builder":
            return builder
        if kind == "output":
            return PROJECT_ROOT / rel
        if kind == "recipe":
            return PROJECT_ROOT / "docs/recipes/INDEX.md"
        return PROJECT_ROOT / rel

    monkeypatch.setattr(runner, "resolve_repo_path", fake_resolve)
    result = runner.run_entry(entry, validate=False, keep_generated=False)
    assert result["ok"] is False
    assert result["error"] == "output_missing"


def test_pythonpath_uses_os_pathsep(monkeypatch, tmp_path):
    seen: dict[str, str] = {}

    builder = tmp_path / "build_ok.py"
    out_name = "ok.jsonld"
    builder.write_text(
        "from pathlib import Path\n"
        "import json, os\n"
        "HERE = Path(__file__).resolve().parent\n"
        "Path(HERE / %r).write_text(json.dumps({'@graph':[{'@id':'kb:x','@type':'https://ontology.unifiedcyberontology.org/uco/core/UcoObject'}]}))\n"
        % out_name,
        encoding="utf-8",
    )

    def fake_resolve(rel, *, must_exist=False, kind="path"):
        if kind == "builder":
            return builder
        if kind == "recipe":
            return PROJECT_ROOT / "docs/recipes/INDEX.md"
        return PROJECT_ROOT / "tmp-output" / Path(rel).name

    real_run = runner.subprocess.run

    def capture_run(*args, **kwargs):
        seen["PYTHONPATH"] = kwargs.get("env", {}).get("PYTHONPATH", "")
        return real_run(*args, **kwargs)

    monkeypatch.setattr(runner, "resolve_repo_path", fake_resolve)
    monkeypatch.setattr(runner.subprocess, "run", capture_run)
    monkeypatch.setattr(runner, "_rdf_parse", lambda path: None)

    entry = {
        "id": "pathsep",
        "category": "test",
        "recipe": "docs/recipes/INDEX.md",
        "builder": "x/build_ok.py",
        "output": f"x/{out_name}",
    }
    result = runner.run_entry(entry, validate=False)
    assert result["ok"] is True
    assert os.pathsep in seen["PYTHONPATH"] or seen["PYTHONPATH"].count(
        str(PROJECT_ROOT / "python")
    ) == 1
    assert str(PROJECT_ROOT / "python") in seen["PYTHONPATH"]
    assert str(PROJECT_ROOT / "mcp_server") in seen["PYTHONPATH"]
    assert result["python_executable"] == sys.executable


@pytest.mark.parametrize("conforms", [True, False])
def test_validation_uses_checkout_import_paths_and_fails_closed(
    conforms, tmp_path, monkeypatch
):
    checkout = tmp_path / "checkout"
    sdk_package = checkout / "python" / "case_uco"
    sdk_package.mkdir(parents=True)
    (sdk_package / "__init__.py").write_text("MARKER = 'checkout'\n", encoding="utf-8")

    validator_module = checkout / "mcp_server" / "graph_validator.py"
    validator_module.parent.mkdir(parents=True)
    validator_module.write_text(
        "import case_uco\n"
        "from types import SimpleNamespace\n"
        "def validator_available():\n"
        "    return True\n"
        "def validate_graph_file(*args, **kwargs):\n"
        "    return SimpleNamespace(\n"
        f"        conforms={conforms!r},\n"
        "        verification_status='complete',\n"
        "        safe_summary='validator ran',\n"
        "        bundle_fingerprint='test-bundle',\n"
        "        selected_profiles=('bfo',),\n"
        f"        exit_code={0 if conforms else 1},\n"
        "    )\n",
        encoding="utf-8",
    )

    recipe = checkout / "docs" / "recipes" / "INDEX.md"
    recipe.parent.mkdir(parents=True)
    recipe.write_text("# Test recipe\n", encoding="utf-8")
    builder = checkout / "example" / "build.py"
    builder.parent.mkdir(parents=True)
    builder.write_text(
        "from pathlib import Path\n"
        "HERE = Path(__file__).resolve().parent\n"
        "(HERE / 'out.ttl').write_text(\n"
        "    '<urn:a> <urn:b> <urn:c> .\\n', encoding='utf-8'\n"
        ")\n",
        encoding="utf-8",
    )

    for name in tuple(sys.modules):
        if name == "graph_validator" or name == "case_uco" or name.startswith(
            "case_uco."
        ):
            monkeypatch.delitem(sys.modules, name, raising=False)
    checkout_sdk = (PROJECT_ROOT / "python").resolve()
    monkeypatch.setattr(
        sys,
        "path",
        [
            path
            for path in sys.path
            if not path or Path(path).resolve() != checkout_sdk
        ],
    )
    monkeypatch.setattr(runner, "ROOT", checkout)

    result = runner.run_entry(
        {
            "id": "checkout-validation",
            "category": "test",
            "recipe": "docs/recipes/INDEX.md",
            "builder": "example/build.py",
            "output": "example/out.ttl",
            "profiles": ["bfo"],
            "strict_concepts": True,
        },
        validate=True,
    )

    assert result["conforms"] is conforms
    assert result["validator_exit_code"] == (0 if conforms else 1)
    if conforms:
        assert result["ok"] is True
        assert "error" not in result
    else:
        assert result["ok"] is False
        assert result["error"] == "validation_failed"


def test_competency_bindings_not_count_alone(tmp_path):
    import rdflib

    graph = tmp_path / "g.jsonld"
    graph.write_text(
        json.dumps(
            {
                "@context": {"kb": "http://example.org/kb/"},
                "@graph": [
                    {"@id": "kb:a", "@type": "kb:Thing", "kb:name": "A"},
                    {"@id": "kb:b", "@type": "kb:Thing", "kb:name": "B"},
                ],
            }
        ),
        encoding="utf-8",
    )
    q = tmp_path / "q.sparql"
    q.write_text(
        "PREFIX kb: <http://example.org/kb/>\n"
        "SELECT ?s ?name WHERE { ?s kb:name ?name } ORDER BY ?name\n",
        encoding="utf-8",
    )

    def fake_resolve(rel, *, must_exist=False, kind="path"):
        return q

    # Patch resolve only inside competency helper via monkeypatch on module.
    import tools.run_recipe_examples as mod

    original = mod.resolve_repo_path
    mod.resolve_repo_path = fake_resolve  # type: ignore[assignment]
    try:
        wrong = mod._run_competency_queries(
            graph,
            [
                {
                    "query": "q.sparql",
                    "expected_count": 2,
                    "expected_bindings": [
                        {"s": "http://example.org/kb/a", "name": "WRONG"},
                        {"s": "http://example.org/kb/b", "name": "B"},
                    ],
                }
            ],
        )
        assert wrong[0]["ok"] is False
        assert wrong[0]["error"] == "bindings_mismatch"

        right = mod._run_competency_queries(
            graph,
            [
                {
                    "query": "q.sparql",
                    "expected_count": 2,
                    "expected_bindings": [
                        {"s": "http://example.org/kb/a", "name": "A"},
                        {"s": "http://example.org/kb/b", "name": "B"},
                    ],
                }
            ],
        )
        assert right[0]["ok"] is True
    finally:
        mod.resolve_repo_path = original


def test_negative_expectation_matcher():
    diagnostics = (
        "Constraint Violation in NotConstraintComponent "
        "(http://www.w3.org/ns/shacl#NotConstraintComponent):\n"
        "\tSource Shape: sh-bfo:BFO_0000002-disjointWith-BFO_0000003-shape\n"
    )
    assert (
        runner._match_negative_expectation(
            {
                "expected_constraint": "NotConstraintComponent",
                "expected_violation": "BFO_0000002-disjointWith-BFO_0000003-shape",
            },
            diagnostics,
        )
        is None
    )
    err = runner._match_negative_expectation(
        {"expected_constraint": "ClassConstraintComponent"},
        diagnostics,
    )
    assert err and "expected_constraint_not_found" in err
    assert runner._match_negative_expectation({}, diagnostics) == (
        "expect_invalid_missing_expectation"
    )


def test_recipe_execution_rejects_unregistered_relationship_kind(tmp_path):
    graph = tmp_path / "relationship.jsonld"
    graph.write_text(
        json.dumps(
            {
                "@context": {
                    "kb": "http://example.org/kb/",
                    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
                },
                "@graph": [
                    {
                        "@id": "kb:rel",
                        "@type": "uco-core:Relationship",
                        "uco-core:kindOfRelationship": "Relates_To",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result: dict[str, Any] = {}
    assert runner._lint_relationship_kinds_if_present(graph, result) is False
    assert result["error"] == "relationship_kind_lint_failed"
    assert result["relationship_kind_lint"]["findings"][0]["severity"] == "error"


def test_support_files_copied(tmp_path, monkeypatch):
    helper = tmp_path / "helper_mod.py"
    helper.write_text("VALUE = 42\n", encoding="utf-8")
    builder = tmp_path / "build_with_helper.py"
    builder.write_text(
        "from pathlib import Path\n"
        "import json\n"
        "import helper_mod\n"
        "HERE = Path(__file__).resolve().parent\n"
        "assert helper_mod.VALUE == 42\n"
        "(HERE / 'out.jsonld').write_text(json.dumps({'@graph':[]}))\n",
        encoding="utf-8",
    )

    def fake_resolve(rel, *, must_exist=False, kind="path"):
        if kind == "builder":
            return builder
        if kind == "support_file":
            return helper
        if kind == "recipe":
            return PROJECT_ROOT / "docs/recipes/INDEX.md"
        return PROJECT_ROOT / rel

    monkeypatch.setattr(runner, "resolve_repo_path", fake_resolve)
    monkeypatch.setattr(runner, "_rdf_parse", lambda path: None)
    entry = {
        "id": "with-support",
        "category": "test",
        "recipe": "docs/recipes/INDEX.md",
        "builder": "x/build_with_helper.py",
        "output": "x/out.jsonld",
        "support_files": ["x/helper_mod.py"],
    }
    result = runner.run_entry(entry, validate=False)
    assert result["ok"] is True, result


def test_per_entry_reproducibility_fields(tmp_path, monkeypatch):
    builder = tmp_path / "build_meta.py"
    builder.write_text(
        "from pathlib import Path\n"
        "import json\n"
        "HERE = Path(__file__).resolve().parent\n"
        "(HERE / 'meta.jsonld').write_text(json.dumps({'@graph':[]}))\n",
        encoding="utf-8",
    )

    def fake_resolve(rel, *, must_exist=False, kind="path"):
        if kind == "builder":
            return builder
        if kind == "recipe":
            return PROJECT_ROOT / "docs/recipes/INDEX.md"
        return PROJECT_ROOT / rel

    monkeypatch.setattr(runner, "resolve_repo_path", fake_resolve)
    monkeypatch.setattr(runner, "_rdf_parse", lambda path: None)
    entry = {
        "id": "meta",
        "category": "test",
        "recipe": "docs/recipes/INDEX.md",
        "builder": "x/build_meta.py",
        "output": "x/meta.jsonld",
    }
    result = runner.run_entry(entry, validate=False)
    assert result["ok"] is True
    assert result["python_executable"] == sys.executable
    assert "python_version" in result
    assert "builder_duration_ms" in result
    assert "total_duration_ms" in result
    assert "output_sha256" in result
    assert len(result["output_sha256"]) == 64
    assert "command" in result
    assert result["exit_code"] == 0
