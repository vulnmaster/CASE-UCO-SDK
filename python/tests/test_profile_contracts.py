"""Profile contracts: synthesis, overlay, host resolution."""

from __future__ import annotations

from case_uco.contracts import load_contract
from case_uco.critique.hosts import resolve_host
from case_uco.graph import CASEGraph
from case_uco.helpers import file_with_content_hashes


def test_synthesize_hash_intelligence() -> None:
    contract = load_contract("HashIntelligence")
    assert contract.profile_id == "HashIntelligence"
    kinds = {c.kind for c in contract.checks}
    assert "hash_presence" in kinds
    assert "hash_intelligence_mission" in kinds
    assert "no_invented_photodna_facet" in kinds
    assert contract.default_validation.get("profiles") == ["prov-o"]


def test_synthesize_all_seven() -> None:
    for profile_id in (
        "MinimalForensics",
        "AirGappedFieldTriage",
        "HashIntelligence",
        "ToolMapping",
        "LegalProcess",
        "FullCACLifecycle",
        "CrossOntology",
    ):
        contract = load_contract(profile_id)
        assert contract.checks
        assert any(c.kind == "required_facets" for c in contract.checks)


def test_full_cac_default_validation() -> None:
    contract = load_contract("FullCACLifecycle")
    assert "cac" in contract.default_validation.get("extensions", [])


def test_file_helper_resolves_as_file_bundle() -> None:
    graph = CASEGraph()
    obj = file_with_content_hashes(graph, file_name="a.bin", hashes=[("SHA256", "aa")])
    assert resolve_host(obj, "File") == "File"
    assert resolve_host(obj) == "File"
