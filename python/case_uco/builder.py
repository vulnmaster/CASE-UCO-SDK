"""High-level InvestigationBuilder — profile-aware graph construction."""

from __future__ import annotations

from typing import Any, Sequence

from case_uco.contracts import load_contract
from case_uco.critique import ProfileCritic
from case_uco.graph import CASEGraph
from case_uco.helpers import (
    file_with_content_hashes,
    model_csam_evidence,
    model_tool_run,
)
from case_uco.topology.profiles import CompositionProfile, get_profile, recommend_profile


class InvestigationBuilder:  # noqa: D101
    """Scenario + evidence paths → profile-aware CASEGraph.

    Inline critique runs as objects are added (missing hashes, missing
    tool version) rather than only after serialize. Offline.
    """

    def __init__(
        self,
        scenario: str,
        *,
        profile_id: str | None = None,
        kb_prefix: str = "http://example.org/kb/",
        critic: ProfileCritic | None = None,
    ) -> None:
        self.scenario = scenario
        if profile_id:
            profile = get_profile(profile_id)
        else:
            ranked = recommend_profile(scenario)
            profile = get_profile(ranked[0]["id"]) if ranked else get_profile("MinimalForensics")
        if profile is None:
            raise ValueError(f"Unknown composition profile: {profile_id}")
        self.profile: CompositionProfile = profile
        extra = {}
        if "ext.cac" in " ".join(profile.required_modules):
            extra["cac-core"] = "https://cacontology.projectvic.org/core#"
            extra["cacontology"] = "https://cacontology.projectvic.org#"
        self.graph = CASEGraph(kb_prefix=kb_prefix, extra_context=extra or None)
        self.contract = load_contract(profile.id)
        self.critic = critic or ProfileCritic(self.contract)

    def add_file(
        self,
        file_name: str,
        hashes: Sequence[tuple[str, str]] | None = None,
        **kwargs: Any,
    ) -> Any:
        hashes = hashes or []
        obj = file_with_content_hashes(self.graph, file_name=file_name, hashes=hashes, **kwargs)
        self.critic.observe_add(
            self.graph,
            host="File",
            node=obj,
            extra={"file_name": file_name, "hashes": list(hashes)},
            source="add_file",
        )
        return obj

    def add_csam_evidence(self, file_name: str, hashes: Sequence[tuple[str, str]], **kwargs: Any) -> dict[str, Any]:
        hashes = hashes or []
        result = model_csam_evidence(self.graph, file_name=file_name, hashes=hashes, **kwargs)
        self.critic.observe_add(
            self.graph,
            host="RasterPicture",
            node=result.get("picture"),
            extra={"file_name": file_name, "hashes": list(hashes)},
            source="add_csam_evidence",
        )
        return result

    def add_tool_run(self, tool_name: str, action_name: str, tool_version: str | None = None, **kwargs: Any) -> dict[str, Any]:
        result = model_tool_run(
            self.graph,
            tool_name=tool_name,
            tool_version=tool_version,
            action_name=action_name,
            **kwargs,
        )
        self.critic.observe_add(
            self.graph,
            host="Tool",
            node=result.get("tool"),
            extra={"tool_name": tool_name, "tool_version": tool_version},
            source="add_tool_run",
        )
        return result

    def build(self) -> CASEGraph:
        return self.graph

    def critique(self) -> list[dict[str, Any]]:
        return [finding.to_compat_dict() for finding in self.critic.findings]

    def critique_report(self, *, when: str = "graph"):
        return self.critic.evaluate(self.graph, when=when)
