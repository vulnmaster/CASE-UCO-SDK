"""Regression tests for the fail-closed operational recipe ontology lint."""

from __future__ import annotations

from pathlib import Path

import pytest

from recipe_lint import (
    OntologyCatalog,
    build_catalog,
    lint_python_graph_methods,
    lint_recipe_text,
    lint_recipes,
)
from relationship_kinds import known_relationship_kinds

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("receiver", ["graph", "g", "case_graph"])
def test_python_snippet_rejects_nonexistent_graph_method(receiver):
    text = f'''```python
{receiver} = CASEGraph()
{receiver}.add_node("kb:example", "uco-core:UcoObject", {{}})
```'''
    findings, _ = lint_recipe_text(
        text, path="test.md", catalog=_catalog(), relationship_kinds=frozenset(),
    )
    assert any(f.code == "unknown_graph_method" and f.line == 3 for f in findings)


def test_graph_method_lint_uses_class_introspection(monkeypatch):
    from case_uco import CASEGraph

    monkeypatch.setattr(CASEGraph, "example_method", lambda self: None, raising=False)
    text = '''```python
g.example_method()
g.upsert_node("kb:example", types=["uco-core:UcoObject"], properties={})
# g.add_node()
message = "graph.add_node()"
```
```text
graph.add_node()
```'''
    assert lint_python_graph_methods(text, path="test.md") == []


def test_routing_skeletons_use_real_graph_methods():
    from domain_index import MAPPING_GUIDE_INDEX

    for entry in MAPPING_GUIDE_INDEX:
        code = entry.get("code_skeleton", "")
        assert not lint_python_graph_methods(f"```python\n{code}\n```", path="routing")


@pytest.fixture(scope="module")
def repository_catalog():
    return build_catalog(PROJECT_ROOT)


@pytest.mark.parametrize("template", [
    "| Class | Role |\n|---|---|\n| `{term}` | Recovery |",
    "| Term | Role |\n|---|---|\n| {term} | Recovery |",
    '```mermaid\ngraph TD\n  A["{term}"]\n```',
    "```\nInvestigation\n  └── cacontology:hasStep ──▶ {term}\n```",
])
def test_shape_only_recovery_term_in_tables_and_diagrams(repository_catalog, template):
    for term, valid in [
        ("cacontology-stranger-abduction:VictimRecovery", False),
        ("cacontology:VictimRescueAction", True),
    ]:
        findings, _ = lint_recipe_text(
            template.format(term=term), path="test.md", catalog=repository_catalog,
            relationship_kinds=known_relationship_kinds(),
        )
        errors = [f for f in findings if not f.excluded]
        assert (not errors) == valid, errors
        if not valid:
            assert any(f.term == term and f.code.startswith("undeclared_") for f in errors)


def _catalog() -> OntologyCatalog:
    prefixes = {
        "cacontology-sextortion": "https://cacontology.projectvic.org/sextortion#",
        "case-investigation": "https://ontology.caseontology.org/case/investigation/",
        "gufo": "http://purl.org/nemo/gufo#",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
        "solveit-data": "https://ontology.solveit-df.org/solveit/data/",
    }
    classes = frozenset(
        {
            "https://cacontology.projectvic.org/sextortion#SextortionIncident",
            "https://ontology.unifiedcyberontology.org/uco/core/Facet",
        }
    )
    properties = frozenset(
        {
            "https://cacontology.projectvic.org/sextortion#conductsOnPlatform",
            "https://ontology.unifiedcyberontology.org/uco/core/name",
            "https://ontology.unifiedcyberontology.org/uco/core/kindOfRelationship",
        }
    )
    return OntologyCatalog(
        prefixes=prefixes,
        classes=classes,
        properties=properties,
        other_terms=frozenset(),
        class_local_names=frozenset({"SextortionIncident", "Facet"}),
        property_local_names=frozenset(
            {"conductsOnPlatform", "name", "kindOfRelationship"}
        ),
    )


@pytest.mark.parametrize(
    ("text", "expected_code", "expected_term"),
    [
        (
            '| Class | Purpose |\n|---|---|\n| `cacontology-sextortion:SextortionScheme` | fake |',
            "undeclared_class",
            "cacontology-sextortion:SextortionScheme",
        ),
        (
            "```text\nIncident\n  └── used_platform ──▶ Platform\n```",
            "undeclared_diagram_edge",
            "used_platform",
        ),
        (
            '{"case-investigation:name": "wrong namespace"}',
            "undeclared_property",
            "case-investigation:name",
        ),
        (
            '{"gufo:hasParticipant": {"@id": "kb:person"}}',
            "undeclared_property",
            "gufo:hasParticipant",
        ),
        (
            '{"@type": "uco-observable:Facet"}',
            "undeclared_class",
            "uco-observable:Facet",
        ),
        (
            'kind_of_relationship="Relates_To"',
            "unregistered_relationship_kind",
            "Relates_To",
        ),
        (
            "Link each action with a `Basis_Of` relationship.",
            "unregistered_relationship_reference",
            "Basis_Of",
        ),
    ],
)
def test_regression_terms_fail_closed(text, expected_code, expected_term):
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    errors = [finding for finding in findings if not finding.excluded]
    assert any(
        finding.code == expected_code and finding.term == expected_term
        for finding in errors
    )


def test_empty_content_data_facet_fails_closed_outside_anti_patterns():
    findings, _checked = lint_recipe_text(
        "```python\ngraph.create(ObservableObject, has_facet=[ContentDataFacet()])\n```\n",
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    errors = [finding for finding in findings if not finding.excluded]
    assert any(
        finding.code == "empty_content_data_facet"
        and finding.term == "ContentDataFacet()"
        for finding in errors
    )


def test_empty_jsonld_content_data_facet_fails_closed():
    text = """```json
{
  "@id": "kb:empty-facet",
  "@type": "uco-observable:ContentDataFacet"
}
```
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    errors = [finding for finding in findings if not finding.excluded]
    assert any(
        finding.code == "empty_content_data_facet"
        and finding.term == "ContentDataFacet"
        for finding in errors
    )


def test_java_content_data_facet_constructor_is_not_empty_facet():
    text = """```java
var contentFacet = new ContentDataFacet();
contentFacet.getHash().add(hash);
```
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    assert not [
        finding
        for finding in findings
        if finding.code == "empty_content_data_facet" and not finding.excluded
    ]


def test_empty_content_data_facet_in_anti_pattern_is_excluded():
    text = """## Anti-patterns

- Attaching `ContentDataFacet()` with no hash
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    empty = [
        finding for finding in findings if finding.code == "empty_content_data_facet"
    ]
    assert empty
    assert all(finding.excluded for finding in empty)


def test_state_specific_charge_class_fails_closed_outside_anti_patterns():
    catalog = _catalog()
    catalog = OntologyCatalog(
        prefixes=catalog.prefixes,
        classes=catalog.classes
        | {"https://cacontology.projectvic.org/legal-outcomes#FloridaStateCharge"},
        properties=catalog.properties,
        other_terms=catalog.other_terms,
        class_local_names=catalog.class_local_names | {"FloridaStateCharge"},
        property_local_names=catalog.property_local_names,
    )
    text = "| Class | Role |\n|---|---|\n| `FloridaStateCharge` | Do not use in SDK recipes. |\n"
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=catalog,
        relationship_kinds=known_relationship_kinds(),
    )
    errors = [finding for finding in findings if not finding.excluded]
    assert any(
        finding.code == "state_specific_charge_class"
        and finding.term == "FloridaStateCharge"
        for finding in errors
    )


def test_declared_terms_and_registered_relationship_kind_pass():
    text = """| Class | Property |
|---|---|
| `cacontology-sextortion:SextortionIncident` | `cacontology-sextortion:conductsOnPlatform` |

```json
{
  "@type": "uco-core:Facet",
  "uco-core:name": "Example",
  "uco-core:kindOfRelationship": "Related_To"
}
```
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    assert [finding for finding in findings if not finding.excluded] == []


def test_subset_tokens_dotted_properties_and_class_diagram_labels_pass():
    catalog = _catalog()
    catalog = OntologyCatalog(
        prefixes={**catalog.prefixes, "cac": "https://cacontology.projectvic.org#"},
        classes=catalog.classes,
        properties=catalog.properties,
        other_terms=catalog.other_terms,
        class_local_names=catalog.class_local_names,
        property_local_names=catalog.property_local_names,
        validation_subsets=frozenset({"cac:missing-child", "cac:full"}),
    )
    text = """Validate with `extensions=["cac:missing-child"]`.

| Field | Pattern |
|---|---|
| Platform | `cacontology-sextortion:SextortionIncident.conductsOnPlatform` |

```text
Incident
  └── Facet ──▶ exhibit number
```
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=catalog,
        relationship_kinds=known_relationship_kinds(),
    )
    assert [finding for finding in findings if not finding.excluded] == []

    findings, _checked = lint_recipe_text(
        "| Field | Pattern |\n|---|---|\n| x | `cacontology-sextortion:SextortionIncident.madeUp` |",
        path="docs/recipes/test.md",
        catalog=catalog,
        relationship_kinds=known_relationship_kinds(),
    )
    assert any(not finding.excluded for finding in findings)


def test_explicit_anti_pattern_and_wildcard_are_reported_as_exclusions():
    text = """## Anti-patterns

| Class | Why invalid |
|---|---|
| `cacontology-sextortion:SextortionScheme` | Never invent this class. |

Use wildcard catalog notation `solveit-data:techniqueDFT-*` only for discovery.
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    assert not [finding for finding in findings if not finding.excluded]
    classifications = {finding.classification for finding in findings}
    assert classifications == {"anti-pattern", "wildcard"}


def test_bounded_proposed_term_directive_requires_rationale_and_does_not_leak():
    text = """<!-- recipe-lint: ignore-start proposed-term -- Demonstrates the term being proposed, not an available term. -->
`proposal:ProposedClass`
<!-- recipe-lint: ignore-end proposed-term -->
`proposal:StillFake`
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    proposed = next(finding for finding in findings if finding.term == "proposal:ProposedClass")
    leaked = next(finding for finding in findings if finding.term == "proposal:StillFake")
    assert proposed.excluded is True
    assert proposed.classification == "proposed-term"
    assert leaked.excluded is False


def test_ignore_directive_accepts_html_comment_end_bang():
    text = """<!-- recipe-lint: ignore-start proposed-term -- Demonstrates the term being proposed, not an available term. --!>
`proposal:ProposedClass`
<!-- recipe-lint: ignore-end proposed-term --!>
`proposal:StillFake`
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    proposed = next(finding for finding in findings if finding.term == "proposal:ProposedClass")
    leaked = next(finding for finding in findings if finding.term == "proposal:StillFake")
    assert proposed.excluded is True
    assert leaked.excluded is False


def test_malformed_exclusion_directive_fails_closed():
    text = """<!-- recipe-lint: ignore-start everything -- Too broad. -->
`proposal:Fake`
<!-- recipe-lint: ignore-end everything -->
"""
    findings, _checked = lint_recipe_text(
        text,
        path="docs/recipes/test.md",
        catalog=_catalog(),
        relationship_kinds=known_relationship_kinds(),
    )
    codes = {finding.code for finding in findings if not finding.excluded}
    assert "unknown_ignore_classification" in codes
    assert "unmatched_ignore_end" in codes
    assert "unknown_prefix" in codes


def test_every_operational_recipe_passes_repository_lint():
    report = lint_recipes(project_root=PROJECT_ROOT)
    details = "\n".join(
        f"{finding.path}:{finding.line}: {finding.code}: {finding.term}"
        for finding in report.errors
    )
    assert not report.verification_errors, report.verification_errors
    assert report.files_checked >= 80
    assert report.ok, details
