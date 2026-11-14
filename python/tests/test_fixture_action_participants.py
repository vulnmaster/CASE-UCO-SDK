"""Co-actors of an action are ``uco-action:participant`` values (#109)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _nodes(value):
    if isinstance(value, list):
        for item in value:
            yield from _nodes(item)
    elif isinstance(value, dict):
        yield value
        for key, child in value.items():
            if key != "@context":
                yield from _nodes(child)


def _ids(value):
    values = value if isinstance(value, list) else [value]
    return {v["@id"] if isinstance(v, dict) else v for v in values if v}


def participated_in_findings(document):
    """Participated_In relationships that point at an action with a performer."""
    nodes = list(_nodes(document))
    performed = {n["@id"] for n in nodes if "@id" in n and "uco-action:performer" in n}
    return [
        n.get("@id", "(anonymous)")
        for n in nodes
        if n.get("uco-core:kindOfRelationship") == "Participated_In"
        and _ids(n.get("uco-core:target", [])) & performed
    ]


def test_example_co_actors_use_participant():
    findings = {
        path.relative_to(ROOT).as_posix(): errors
        for path in sorted((ROOT / "examples").rglob("*.jsonld"))
        if (errors := participated_in_findings(json.loads(path.read_text(encoding="utf-8"))))
    }
    assert not findings, findings


def test_participated_in_lint_catches_planted_fixture():
    document = {
        "@graph": [
            {"@id": "kb:act-1", "@type": "uco-action:Action",
             "uco-action:performer": {"@id": "kb:person-a"}},
            {"@id": "kb:rel-1", "@type": "uco-core:Relationship",
             "uco-core:source": [{"@id": "kb:person-b"}],
             "uco-core:target": {"@id": "kb:act-1"},
             "uco-core:kindOfRelationship": "Participated_In"},
        ]
    }
    assert participated_in_findings(document) == ["kb:rel-1"]
