"""Tests for the staged promotion lifecycle of learned artifacts (issue #52).

All fixtures are Tier T0 public-safe synthetic data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import investigation_router
import knowledge_lifecycle
import graph_validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

VALID_TTL = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix candext: <http://example.org/ontology/candext/> .

candext:CandidateThing
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "CandidateThing"@en ;
    rdfs:comment "Synthetic candidate class for lifecycle tests."@en .
"""

ORPHAN_TTL = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix candext: <http://example.org/ontology/candext/> .

candext:OrphanThing
    a owl:Class ;
    rdfs:label "OrphanThing"@en .
"""

BROKEN_TTL = "@prefix broken this is not turtle at all {{{"

CORE_TTL = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
uco-core:UcoObject a owl:Class .
"""

EXEMPLAR_TTL = """\
@prefix candext: <http://example.org/ontology/candext/> .
@prefix kb: <http://example.org/kb/> .
kb:thing-11111111-1111-4111-8111-111111111111 a candext:CandidateThing .
"""


def make_core(root: Path) -> None:
    """Minimal core ontology so the classes_anchored gate can resolve
    uco-core:UcoObject as a declared parent."""

    core_dir = root / "ontology/UCO/ontology/uco/core"
    if not core_dir.is_dir():
        core_dir.mkdir(parents=True)
        (core_dir / "core.ttl").write_text(CORE_TTL, encoding="utf-8")


def make_extension(
    root: Path,
    name: str,
    ttl: str,
    status: str = "candidate",
    with_exemplar: bool = True,
) -> Path:
    make_core(root)
    ext_dir = root / "extensions" / name
    ext_dir.mkdir(parents=True)
    (ext_dir / f"{name}.ttl").write_text(ttl, encoding="utf-8")
    manifest = {
        "name": name,
        "display_name": f"Test {name}",
        "version": "0.0.1",
        "status": status,
        "owl_files": [f"{name}.ttl"],
        "shacl_files": [],
        "bridge_files": [],
    }
    if with_exemplar:
        (ext_dir / "exemplar.ttl").write_text(EXEMPLAR_TTL, encoding="utf-8")
        manifest["exemplar_files"] = ["exemplar.ttl"]
    (ext_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return ext_dir


def test_status_defaults_to_operational_for_bundled_manifests():
    assert knowledge_lifecycle.extension_status({}) == "operational"
    assert knowledge_lifecycle.is_routable({}) is True
    assert knowledge_lifecycle.is_routable({"status": "candidate"}) is False
    assert knowledge_lifecycle.is_routable({"status": "deprecated"}) is False


def test_candidate_extension_invisible_to_routing(tmp_path):
    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    make_extension(tmp_path, "opext", VALID_TTL, status="operational")
    installed = investigation_router._installed_extensions(tmp_path)
    assert "opext" in installed
    assert "candext" not in installed


def test_deprecated_extension_invisible_to_routing(tmp_path):
    make_extension(tmp_path, "oldext", VALID_TTL, status="deprecated")
    installed = investigation_router._installed_extensions(tmp_path)
    assert "oldext" not in installed


def test_candidate_extension_still_loadable_explicitly(tmp_path):
    """The authoring investigation can keep using a candidate by name."""

    import concept_coverage

    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    graph_path = tmp_path / "g.jsonld"
    graph_path.write_text(
        json.dumps({
            "@context": {"kb": "http://example.org/kb/"},
            "@graph": [{
                "@id": "kb:t-11111111-1111-4111-8111-111111111111",
                "@type": "http://example.org/ontology/candext/CandidateThing",
            }],
        }),
        encoding="utf-8",
    )
    report = concept_coverage.check_graph_concepts(
        graph_path, project_root=tmp_path, extensions=["candext"]
    )
    assert report.ok is True, report.undeclared_classes


def test_promotion_success_records_provenance(tmp_path):
    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "candext", project_root=tmp_path, reviewed_by="Synthetic Reviewer",
        require_validator=False,
    )
    assert result.ok is True, result.gates
    assert result.status == "operational"

    manifest = json.loads(
        (tmp_path / "extensions/candext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "operational"
    promo = manifest["promotion"]
    assert promo["reviewed_by"] == "Synthetic Reviewer"
    assert promo["previous_status"] == "candidate"
    assert promo["promoted_at"]
    assert all(g["ok"] for g in promo["gates"])

    # After promotion the extension is routable.
    installed = investigation_router._installed_extensions(tmp_path)
    assert "candext" in installed


def test_promotion_fails_on_unparseable_ontology(tmp_path):
    make_extension(tmp_path, "brokenext", BROKEN_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "brokenext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error.startswith("promotion_gate_failed:ontology_files_parse")
    manifest = json.loads(
        (tmp_path / "extensions/brokenext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "candidate", "failed promotion must not change status"
    assert "promotion" not in manifest


def test_promotion_fails_on_orphan_class(tmp_path):
    make_extension(tmp_path, "orphanext", ORPHAN_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "orphanext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:classes_anchored"


def test_promotion_fails_on_missing_exemplar(tmp_path):
    ext_dir = make_extension(tmp_path, "exemext", VALID_TTL, status="candidate")
    manifest = json.loads((ext_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest["exemplar_files"] = ["missing-exemplar.ttl"]
    (ext_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    if not graph_validator.validator_available():
        pytest.skip("case_validate CLI not installed")
    result = knowledge_lifecycle.promote_extension(
        "exemext", project_root=tmp_path, require_validator=True
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:exemplars_validate"


def test_deprecation_records_reason_and_revokes_routing(tmp_path):
    make_extension(tmp_path, "badext", VALID_TTL, status="operational")
    assert "badext" in investigation_router._installed_extensions(tmp_path)

    result = knowledge_lifecycle.deprecate_extension(
        "badext", reason="synthetic modeling error", project_root=tmp_path,
        deprecated_by="Synthetic Reviewer",
    )
    assert result["status"] == "deprecated"
    manifest = json.loads(
        (tmp_path / "extensions/badext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["deprecation"]["reason"] == "synthetic modeling error"
    assert "badext" not in investigation_router._installed_extensions(tmp_path)


def test_bundled_extensions_remain_operational():
    """The nine bundled extensions (no status field) stay routable."""

    installed = investigation_router._installed_extensions(PROJECT_ROOT)
    for name in ("legalproc", "rico", "cryptoinv"):
        if (PROJECT_ROOT / "extensions" / name / "manifest.json").is_file():
            assert name in installed


def test_candidate_recipe_directory_is_outside_catalog():
    candidates = PROJECT_ROOT / "docs/recipes/candidates"
    assert candidates.is_dir()
    sys.path.insert(0, str(PROJECT_ROOT / "mcp_server"))
    from domain_index import RECIPE_INDEX

    for entry in RECIPE_INDEX:
        assert "candidates/" not in entry["file"], entry["file"]


def test_cli_status_and_promote(tmp_path, capsys):
    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    rc = knowledge_lifecycle.main(
        ["status", "--project-root", str(tmp_path)]
    )
    assert rc == 0
    assert "candext: candidate" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Fail-closed status handling (issue #55)
# ---------------------------------------------------------------------------


def test_invalid_status_never_operational():
    assert knowledge_lifecycle.extension_status({"status": "bogus"}) == "invalid"
    assert knowledge_lifecycle.is_routable({"status": "bogus"}) is False


def test_invalid_status_reported_as_integrity_failure(tmp_path):
    make_extension(tmp_path, "weirdext", VALID_TTL, status="bogus")
    failures: list[dict] = []
    installed = investigation_router._installed_extensions(tmp_path, failures)
    assert "weirdext" not in installed
    assert {"extension": "weirdext", "error": "extension_status_invalid"} in failures


def test_malformed_manifest_reported_as_integrity_failure(tmp_path):
    ext_dir = tmp_path / "extensions" / "brokenmanifest"
    ext_dir.mkdir(parents=True)
    (ext_dir / "manifest.json").write_text("{not json", encoding="utf-8")
    failures: list[dict] = []
    installed = investigation_router._installed_extensions(tmp_path, failures)
    assert "brokenmanifest" not in installed
    assert {"extension": "brokenmanifest",
            "error": "extension_manifest_malformed"} in failures


def test_malformed_manifest_is_typed_error_on_load(tmp_path):
    ext_dir = tmp_path / "extensions" / "brokenmanifest"
    ext_dir.mkdir(parents=True)
    (ext_dir / "manifest.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="extension_manifest_malformed"):
        knowledge_lifecycle.promote_extension("brokenmanifest", project_root=tmp_path)


# ---------------------------------------------------------------------------
# Strengthened promotion gates (issue #56)
# ---------------------------------------------------------------------------

UNANCHORED_TTL = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix candext: <http://example.org/ontology/candext/> .
@prefix ghost: <http://example.org/ontology/ghost/> .

candext:FloatingThing
    a owl:Class ;
    rdfs:subClassOf ghost:UndeclaredParent ;
    rdfs:label "FloatingThing"@en .
"""


def test_promotion_fails_when_parent_class_undeclared(tmp_path):
    make_extension(tmp_path, "floatext", UNANCHORED_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "floatext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:classes_anchored"


def test_promotion_fails_without_exemplar(tmp_path):
    make_extension(tmp_path, "noexext", VALID_TTL, status="candidate",
                   with_exemplar=False)
    result = knowledge_lifecycle.promote_extension(
        "noexext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:exemplars_validate"


def test_promotion_requires_negative_fixture_when_shapes_exist(tmp_path):
    ext_dir = make_extension(tmp_path, "shapedext", VALID_TTL, status="candidate")
    manifest = json.loads((ext_dir / "manifest.json").read_text(encoding="utf-8"))
    (ext_dir / "shapes.ttl").write_text(
        "@prefix sh: <http://www.w3.org/ns/shacl#> .\n"
        "@prefix candext: <http://example.org/ontology/candext/> .\n"
        "candext:CandidateThingShape a sh:NodeShape ; "
        "sh:targetClass candext:CandidateThing .\n",
        encoding="utf-8",
    )
    manifest["shacl_files"] = ["shapes.ttl"]
    (ext_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = knowledge_lifecycle.promote_extension(
        "shapedext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:negative_fixtures"


def test_promotion_runs_competency_queries(tmp_path):
    ext_dir = make_extension(tmp_path, "queryext", VALID_TTL, status="candidate")
    manifest = json.loads((ext_dir / "manifest.json").read_text(encoding="utf-8"))
    (ext_dir / "q1.sparql").write_text(
        "SELECT ?s WHERE { ?s a <http://example.org/ontology/candext/CandidateThing> }",
        encoding="utf-8",
    )
    manifest["competency_queries"] = [
        {"file": "q1.sparql", "against": "exemplar.ttl", "expect": "empty"}
    ]
    (ext_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = knowledge_lifecycle.promote_extension(
        "queryext", project_root=tmp_path, require_validator=False
    )
    # The exemplar DOES contain a CandidateThing, so expect=empty must fail.
    assert result.ok is False
    assert result.error == "promotion_gate_failed:competency_queries"

    manifest["competency_queries"][0]["expect"] = "nonempty"
    (ext_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = knowledge_lifecycle.promote_extension(
        "queryext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is True, result.gates


def test_promotion_respects_deployment_profile(tmp_path, monkeypatch):
    import workspace_policy

    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    monkeypatch.setenv(workspace_policy.PROFILE_ENV, "offline-investigation")
    result = knowledge_lifecycle.promote_extension(
        "candext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "promotion_not_permitted_in_profile"

    monkeypatch.setenv(workspace_policy.PROFILE_ENV, "production-review")
    # Secure mode is implied by the profile; give the validator a policy
    # that covers the candidate workspace so the gates can read exemplars.
    work = tmp_path / "case-work"
    work.mkdir()
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, str(tmp_path))
    monkeypatch.setenv(workspace_policy.WRITE_ROOTS_ENV, str(work))
    result = knowledge_lifecycle.promote_extension(
        "candext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "reviewer_identity_required"

    result = knowledge_lifecycle.promote_extension(
        "candext", project_root=tmp_path, require_validator=False,
        reviewed_by="Jane Reviewer",
    )
    assert result.ok is True, result.gates
    manifest = json.loads(
        (tmp_path / "extensions/candext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["promotion"]["reviewed_by"] == "Jane Reviewer"
    assert manifest["promotion"]["deployment_profile"] == "production-review"


# ---------------------------------------------------------------------------
# Governed recipe promotion (issue #56)
# ---------------------------------------------------------------------------

class _RecipeLintResult:
    def __init__(self, ok: bool, findings: list[dict] | None = None):
        self.ok = ok
        self._findings = findings or []

    def to_dict(self) -> dict:
        return {"ok": self.ok, "findings": self._findings}


@pytest.fixture(autouse=True)
def _stub_recipe_ontology_lint(monkeypatch):
    """Minimal temp workspaces do not vendor the repository ontology closure."""

    import recipe_lint

    monkeypatch.setattr(
        recipe_lint,
        "lint_recipes",
        lambda **_kwargs: _RecipeLintResult(True),
    )


CANDIDATE_RECIPE = """\
# Synthetic Learned Pattern

One-paragraph scope for a synthetic learned modeling pattern.

**When to use this recipe**

- A synthetic trigger condition.

## Modeling pattern

```json
{"@id": "kb:x-11111111-1111-4111-8111-111111111111", "@type": "uco-core:UcoObject"}
```

## Related

- [extensions.md](extensions.md)
"""


def _recipe_workspace(tmp_path: Path) -> Path:
    recipes = tmp_path / "docs/recipes"
    candidates = recipes / "candidates"
    candidates.mkdir(parents=True)
    (recipes / "extensions.md").write_text("# Extensions\n", encoding="utf-8")
    (recipes / "INDEX.md").write_text("# CASE/UCO SDK Recipes\n", encoding="utf-8")
    mcp_dir = tmp_path / "mcp_server"
    mcp_dir.mkdir()
    (mcp_dir / "domain_index.py").write_text(
        'RECIPE_INDEX: list[dict[str, str]] = [\n'
        '    {\n'
        '        "title": "Working with Extensions",\n'
        '        "description": "x",\n'
        '        "keywords": "x",\n'
        '        "file": "docs/recipes/extensions.md",\n'
        '    },\n'
        ']\n',
        encoding="utf-8",
    )
    (candidates / "synthetic-learned-pattern.md").write_text(
        CANDIDATE_RECIPE, encoding="utf-8"
    )
    return tmp_path


def test_promote_recipe_moves_and_registers(tmp_path, monkeypatch):
    root = _recipe_workspace(tmp_path)

    def _fake_gate(_slug, **_kwargs):
        return [{"id": "synthetic-learned-pattern"}]

    def _fake_run(_entries, **_kwargs):
        return {"total": 1, "passed": 1, "failed": 0, "results": [{"ok": True}]}

    monkeypatch.setattr(
        "tools.run_recipe_examples.entries_for_promotion_gate", _fake_gate, raising=False
    )
    monkeypatch.setattr(
        "tools.run_recipe_examples.run_manifest_entries", _fake_run, raising=False
    )
    # promote_recipe imports from tools.* after sys.path insert — patch both.
    import tools.run_recipe_examples as rre

    monkeypatch.setattr(rre, "entries_for_promotion_gate", _fake_gate)
    monkeypatch.setattr(rre, "run_manifest_entries", _fake_run)
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)

    result = knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern",
        description="Synthetic learned pattern for lifecycle tests.",
        keywords="synthetic learned pattern",
        project_root=root,
        reviewed_by="Jane Reviewer",
    )
    assert result["ok"] is True, result
    assert (root / "docs/recipes/synthetic-learned-pattern.md").is_file()
    assert not (root / "docs/recipes/candidates/synthetic-learned-pattern.md").exists()
    index_md = (root / "docs/recipes/INDEX.md").read_text(encoding="utf-8")
    assert "synthetic-learned-pattern.md" in index_md
    domain_index = (root / "mcp_server/domain_index.py").read_text(encoding="utf-8")
    assert '"file": "docs/recipes/synthetic-learned-pattern.md"' in domain_index
    log = json.loads((root / "docs/recipes/promotion-log.json").read_text(encoding="utf-8"))
    assert log[-1]["action"] == "promote"
    assert log[-1]["reviewed_by"] == "Jane Reviewer"
    # The edited RECIPE_INDEX must still be valid Python.
    namespace: dict = {}
    exec(domain_index, namespace)  # noqa: S102 — test-authored content
    assert any(
        e["file"] == "docs/recipes/synthetic-learned-pattern.md"
        for e in namespace["RECIPE_INDEX"]
    )


def test_promote_recipe_rejects_ontology_lint_failure(tmp_path, monkeypatch):
    root = _recipe_workspace(tmp_path)
    import recipe_lint

    monkeypatch.setattr(
        recipe_lint,
        "lint_recipes",
        lambda **_kwargs: _RecipeLintResult(
            False,
            [{"code": "undeclared_class", "term": "cacontology-sextortion:SextortionScheme"}],
        ),
    )
    result = knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern",
        description="Synthetic learned pattern for lifecycle tests.",
        keywords="synthetic learned pattern",
        project_root=root,
        reviewed_by="Jane Reviewer",
    )
    assert result["ok"] is False
    assert result["error"] == "recipe_ontology_lint_failed"
    assert result["detail"]["findings"][0]["term"].endswith("SextortionScheme")
    assert (root / "docs/recipes/candidates/synthetic-learned-pattern.md").is_file()


def test_promote_recipe_rejects_missing_execution_metadata(tmp_path, monkeypatch):
    """Fail closed: no recipe-execution.json entry ⇒ cannot promote (#69)."""
    root = _recipe_workspace(tmp_path)
    import tools.run_recipe_examples as rre

    monkeypatch.setattr(rre, "entries_for_promotion_gate", lambda _slug, **_k: [])
    result = knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern",
        description="Synthetic learned pattern for lifecycle tests.",
        keywords="synthetic learned pattern",
        project_root=root,
        reviewed_by="Jane Reviewer",
    )
    assert result["ok"] is False
    assert result["error"] == "recipe_execution_metadata_missing"
    assert (root / "docs/recipes/candidates/synthetic-learned-pattern.md").is_file()
    assert not (root / "docs/recipes/synthetic-learned-pattern.md").exists()


def test_promote_recipe_rejects_when_validator_unavailable(tmp_path, monkeypatch):
    root = _recipe_workspace(tmp_path)
    import tools.run_recipe_examples as rre

    monkeypatch.setattr(
        rre,
        "entries_for_promotion_gate",
        lambda _slug, **_k: [{"id": "synthetic-learned-pattern"}],
    )
    monkeypatch.setattr(graph_validator, "validator_available", lambda: False)
    result = knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern",
        description="Synthetic learned pattern for lifecycle tests.",
        keywords="synthetic learned pattern",
        project_root=root,
        reviewed_by="Jane Reviewer",
    )
    assert result["ok"] is False
    assert result["error"] == "validator_unavailable"


def test_promote_recipe_rejects_failing_gate(tmp_path, monkeypatch):
    root = _recipe_workspace(tmp_path)
    import tools.run_recipe_examples as rre

    monkeypatch.setattr(
        rre,
        "entries_for_promotion_gate",
        lambda _slug, **_k: [{"id": "synthetic-learned-pattern"}],
    )
    monkeypatch.setattr(
        rre,
        "run_manifest_entries",
        lambda *_a, **_k: {
            "total": 1,
            "passed": 0,
            "failed": 1,
            "results": [{"ok": False, "error": "validation_failed"}],
        },
    )
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    result = knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern",
        description="Synthetic learned pattern for lifecycle tests.",
        keywords="synthetic learned pattern",
        project_root=root,
        reviewed_by="Jane Reviewer",
    )
    assert result["ok"] is False
    assert result["error"] == "recipe_execution_gate_failed"
    assert (root / "docs/recipes/candidates/synthetic-learned-pattern.md").is_file()


def test_promote_recipe_rejects_bad_structure(tmp_path):
    root = _recipe_workspace(tmp_path)
    bad = root / "docs/recipes/candidates/bad-recipe.md"
    bad.write_text("just some text with no structure\n", encoding="utf-8")
    result = knowledge_lifecycle.promote_recipe(
        "bad-recipe", description="d", keywords="k", project_root=root
    )
    assert result["ok"] is False
    assert result["error"] == "recipe_structure_invalid"
    # Failed promotion leaves every operational file unchanged.
    assert bad.is_file()
    assert "bad-recipe" not in (root / "docs/recipes/INDEX.md").read_text(encoding="utf-8")
    assert "bad-recipe" not in (root / "mcp_server/domain_index.py").read_text(encoding="utf-8")


def test_promote_recipe_requires_metadata(tmp_path):
    root = _recipe_workspace(tmp_path)
    result = knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern", description="", keywords="",
        project_root=root,
    )
    assert result["ok"] is False
    assert result["error"] == "recipe_metadata_required"


def test_deprecate_recipe_roundtrip(tmp_path, monkeypatch):
    root = _recipe_workspace(tmp_path)
    import tools.run_recipe_examples as rre

    monkeypatch.setattr(
        rre,
        "entries_for_promotion_gate",
        lambda _slug, **_k: [{"id": "synthetic-learned-pattern"}],
    )
    monkeypatch.setattr(
        rre,
        "run_manifest_entries",
        lambda *_a, **_k: {"total": 1, "passed": 1, "failed": 0, "results": [{"ok": True}]},
    )
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)

    knowledge_lifecycle.promote_recipe(
        "synthetic-learned-pattern",
        description="Synthetic learned pattern for lifecycle tests.",
        keywords="synthetic learned pattern",
        project_root=root,
    )
    result = knowledge_lifecycle.deprecate_recipe(
        "synthetic-learned-pattern", reason="taught an invalid pattern",
        project_root=root, deprecated_by="Jane Reviewer",
    )
    assert result["ok"] is True
    assert (root / "docs/recipes/candidates/synthetic-learned-pattern.md").is_file()
    assert not (root / "docs/recipes/synthetic-learned-pattern.md").exists()
    index_md = (root / "docs/recipes/INDEX.md").read_text(encoding="utf-8")
    assert "(synthetic-learned-pattern.md)" not in index_md
    domain_index = (root / "mcp_server/domain_index.py").read_text(encoding="utf-8")
    assert "synthetic-learned-pattern" not in domain_index
    namespace: dict = {}
    exec(domain_index, namespace)  # noqa: S102 — test-authored content
    assert all(
        e["file"] != "docs/recipes/synthetic-learned-pattern.md"
        for e in namespace["RECIPE_INDEX"]
    )
    log = json.loads((root / "docs/recipes/promotion-log.json").read_text(encoding="utf-8"))
    assert log[-1]["action"] == "deprecate"
