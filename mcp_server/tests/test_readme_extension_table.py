"""README's bundled-extension tables list every distributed extension at its manifest version."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROW = re.compile(r"^\| \[`([a-z0-9-]+)`\]\((?:extensions|ontology)/[a-z0-9-]+/\) \| ([0-9][^ |]*) \|", re.M)


def _manifests() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for path in [*ROOT.glob("extensions/*/manifest.json"), *ROOT.glob("ontology/*/manifest.json")]:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("distribution") == "private":
            continue
        found[data.get("name") or path.parent.name] = data
    return found


def test_readme_extension_tables_match_manifests() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    section = readme.split("## Bundled Extension Ontologies", 1)[1].split("\n## ", 1)[0]
    listed = dict(ROW.findall(section))
    manifests = _manifests()
    assert set(listed) == set(manifests)
    for name, version in listed.items():
        assert version == manifests[name]["version"], name
