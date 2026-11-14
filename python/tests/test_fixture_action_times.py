"""Action fixtures must use the UCO action timing predicates."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CORE = "https://ontology.unifiedcyberontology.org/uco/core/"
ACTION = "https://ontology.unifiedcyberontology.org/uco/action/"
INVESTIGATION = "https://ontology.caseontology.org/case/investigation/"
ACTION_TYPES = {ACTION + "Action", INVESTIGATION + "InvestigativeAction"}


def action_time_findings(value, context=None):
    """Walk nested JSON-LD nodes, expanding inline contexts and full IRIs."""
    context = {
        "uco-core": CORE, "uco-action": ACTION,
        "case-investigation": INVESTIGATION, **(context or {}),
    }
    if isinstance(value, list):
        return [finding for item in value for finding in action_time_findings(item, context)]
    if not isinstance(value, dict):
        return []
    local_context = value.get("@context", {})
    for entry in local_context if isinstance(local_context, list) else [local_context]:
        if isinstance(entry, dict):
            context.update(entry)

    def expand(term):
        mapping = context.get(term, term)
        if isinstance(mapping, dict):
            mapping = mapping.get("@id", term)
        if not isinstance(mapping, str):
            return term
        prefix, separator, local = mapping.partition(":")
        namespace = context.get(prefix)
        if isinstance(namespace, dict):
            namespace = namespace.get("@id")
        return namespace + local if separator and isinstance(namespace, str) else mapping

    types = value.get("@type", [])
    if isinstance(types, str):
        types = [types]
    findings = []
    if ACTION_TYPES.intersection(expand(term) for term in types):
        findings.extend(
            (value.get("@id", "(anonymous)"), key)
            for key in value if expand(key) in {CORE + "startTime", CORE + "endTime"}
        )
    for key, child in value.items():
        if key != "@context":
            findings.extend(action_time_findings(child, context))
    return findings


def test_example_actions_use_action_times():
    findings = {
        path.relative_to(ROOT).as_posix(): errors
        for path in sorted((ROOT / "examples").rglob("*.jsonld"))
        if (errors := action_time_findings(json.loads(path.read_text(encoding="utf-8"))))
    }
    assert not findings, findings


@pytest.mark.parametrize("action_type", ["uco-action:Action", "case-investigation:InvestigativeAction", *sorted(ACTION_TYPES)])
@pytest.mark.parametrize("key", ["uco-core:startTime", "uco-core:endTime", CORE + "startTime", CORE + "endTime"])
def test_action_time_lint_catches_planted_fixture(action_type, key):
    document = {
        "@context": {"uco-core": CORE, "uco-action": ACTION, "case-investigation": INVESTIGATION},
        "@graph": [{"@id": "kb:example-action", "@type": [action_type], key: "2026-01-01T00:00:00Z"}],
    }
    assert action_time_findings(document) == [("kb:example-action", key)]


def test_action_times_and_non_action_time_ranges_are_allowed():
    assert not action_time_findings({"@type": ACTION + "Action", ACTION + "startTime": "2026-01-01T00:00:00Z"})
    assert not action_time_findings({"@type": CORE + "UcoObject", CORE + "startTime": "2026-01-01T00:00:00Z"})


def test_action_time_lint_checks_partial_and_nested_examples():
    node = {"@type": "uco-action:Action", "uco-core:startTime": "2026-01-01T00:00:00Z"}
    assert action_time_findings({"uco-core:object": [node]}) == [("(anonymous)", "uco-core:startTime")]
