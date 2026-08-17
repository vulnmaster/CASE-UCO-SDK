"""Focused checks for the hand-maintained topology / semantic-spine docs."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs" / "SDK_TOPOLOGY.md"
SCRIPT_PATH = REPO_ROOT / "scripts" / "print_sdk_topology.py"
SPINE_TTL = REPO_ROOT / "ontology" / "cac" / "ontology" / "ontology" / "cacontology-core-spine.ttl"

FORBIDDEN_SUBSTRINGS = (
    "photodna",
    "photo-dna",
    "vics",
    "court-defensible",
    "court defensible",
    "2.0.0",
    "2.0.1",
    "investigationworkflow",
    "model_csam",
)

INVENTORY_NAMES = (
    "class-and-facet-inventory.json",
    "class-and-facet-inventory.md",
    "module-dependency-dag.json",
    "module-dependency-dag.md",
    "sdk-layers.json",
    "semantic-spine.json",
)

EXPECTED_KIND_NAMES = (
    "Entity",
    "EnduringEntity",
    "Occurrent",
    "Event",
    "Situation",
    "Role",
    "Phase",
)


def _load_printer():
    spec = importlib.util.spec_from_file_location("print_sdk_topology", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_topology_doc_exists_and_is_concise() -> None:
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert 40 < len(lines) < 220
    assert "documentation only" in text.lower()
    assert "does not change runtime" in text.lower() or "documentation only" in text.lower()
    for name in EXPECTED_KIND_NAMES:
        assert f"`{name}`" in text, f"doc missing spine kind {name}"
    for name in ("UcoThing", "UcoObject", "Facet", "UcoType"):
        assert f"`{name}`" in text


def test_docs_and_script_are_public_safe() -> None:
    blob = DOC_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + SCRIPT_PATH.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"topology docs contain forbidden substring {needle!r}"


def test_no_generated_inventories_committed() -> None:
    topology_dir = REPO_ROOT / "topology"
    if topology_dir.is_dir():
        names = {path.name for path in topology_dir.rglob("*") if path.is_file()}
        overlap = names.intersection(INVENTORY_NAMES)
        assert not overlap, f"committed inventory files: {sorted(overlap)}"
    for name in INVENTORY_NAMES:
        assert not (REPO_ROOT / name).exists()
        assert not (REPO_ROOT / "docs" / name).exists()


def test_printer_matches_registry() -> None:
    printer = _load_printer()
    summary = printer.build_summary(REPO_ROOT)
    assert summary["documentation_only"] is True
    assert summary["writes_files"] is False
    assert printer.missing_iris(summary) == []
    assert set(summary["spine_kinds"]) == set(EXPECTED_KIND_NAMES)
    for unique in ("Entity", "EnduringEntity", "Occurrent", "Situation", "Phase"):
        assert summary["spine_kinds"][unique]["in_registry"] is True
    for homonym in ("Event", "Role"):
        assert summary["spine_kinds"][homonym]["in_registry"] is False
        assert "collision" in summary["spine_kinds"][homonym].get("note", "")
    families = set(summary["registry_module_families"])
    assert {"uco", "case", "ext"}.issubset(families)


def test_printer_stdout_only(capsys) -> None:
    printer = _load_printer()
    rc = printer.main([])
    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["writes_files"] is False
    assert captured.err == ""


def test_spine_ttl_contains_documented_kinds_when_present() -> None:
    if not SPINE_TTL.is_file():
        return
    printer = _load_printer()
    names = printer.extract_spine_classes(SPINE_TTL.read_text(encoding="utf-8"))
    for kind in EXPECTED_KIND_NAMES:
        assert kind in names
    summary = printer.build_summary(REPO_ROOT)
    assert summary["spine_ttl"] is not None
    assert summary["spine_ttl_class_count"] == len(names)
    # Compact docs must stay smaller than the full spine class list.
    assert summary["spine_ttl_class_count"] > len(EXPECTED_KIND_NAMES)


def test_registry_iris_match_documented_spine() -> None:
    sys.path.insert(0, str(REPO_ROOT / "python"))
    from case_uco.registry import get_class

    printer = _load_printer()
    for name, iri in printer.SPINE_REGISTRY_UNIQUE.items():
        info = get_class(name)
        assert info is not None, name
        assert info["iri"] == iri
        assert info["module"] == "ext.cac.cac-core"
    for name, iri in printer.DOCUMENTED_UCO_CORE.items():
        info = get_class(name)
        assert info is not None, name
        assert info["iri"] == iri
        assert info["module"] == "uco.core"
    # Homonyms: registry local name is UCO; CAC IRI is documented separately.
    assert get_class("Event")["iri"].endswith("/uco/core/Event")
    assert get_class("Role")["iri"].endswith("/uco/role/Role")
