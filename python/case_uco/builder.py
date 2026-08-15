"""High-level InvestigationBuilder — profile-aware graph construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from case_uco.graph import CASEGraph
from case_uco.helpers import (
    file_with_content_hashes,
    model_csam_evidence,
    model_tool_run,
)
from case_uco.topology.profiles import CompositionProfile, get_profile, recommend_profile


@dataclass
class CritiqueFinding:
    severity: str
    message: str
    path: str = ""


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
        self.findings: list[CritiqueFinding] = []

    def add_file(
        self,
        file_name: str,
        hashes: Sequence[tuple[str, str]] | None = None,
        **kwargs: Any,
    ) -> Any:
        if not hashes:
            self.findings.append(
                CritiqueFinding(
                    "error",
                    f"{file_name}: {self.profile.id} requires ContentDataFacet hashes",
                    file_name,
                )
            )
            hashes = []
        return file_with_content_hashes(self.graph, file_name=file_name, hashes=hashes, **kwargs)

    def add_csam_evidence(self, file_name: str, hashes: Sequence[tuple[str, str]], **kwargs: Any) -> dict[str, Any]:
        if not hashes:
            self.findings.append(
                CritiqueFinding("error", f"{file_name}: CSAM evidence must carry hashes", file_name)
            )
        return model_csam_evidence(self.graph, file_name=file_name, hashes=hashes, **kwargs)

    def add_tool_run(self, tool_name: str, action_name: str, tool_version: str | None = None, **kwargs: Any) -> dict[str, Any]:
        if not tool_version:
            self.findings.append(
                CritiqueFinding("warning", f"Tool {tool_name} has no version", tool_name)
            )
        return model_tool_run(
            self.graph,
            tool_name=tool_name,
            tool_version=tool_version,
            action_name=action_name,
            **kwargs,
        )

    def build(self) -> CASEGraph:
        return self.graph

    def critique(self) -> list[dict[str, str]]:
        return [
            {"severity": f.severity, "message": f.message, "path": f.path}
            for f in self.findings
        ]
