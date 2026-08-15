"""Fluent composition helpers derived from Composition Profiles.

Additive. These functions wrap existing generated classes; they do not
replace them. They exist so common LE workflows (hashed files, CSAM
media, tool runs) are hard to get wrong.
"""

from __future__ import annotations

from typing import Any, Iterable, Sequence

from case_uco.graph import CASEGraph
from case_uco.uco.observable import (
    ContentDataFacet,
    FileFacet,
    ObservableObject,
    RasterPictureFacet,
)
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash
from case_uco.case.investigation import InvestigativeAction


def _hashes(pairs: Iterable[tuple[str, str]] | None) -> list[Hash]:
    return [Hash(hash_method=method, hash_value=value) for method, value in (pairs or [])]


def file_with_content_hashes(
    graph: CASEGraph,
    *,
    file_name: str,
    hashes: Sequence[tuple[str, str]],
    file_path: str | None = None,
    size_in_bytes: int | None = None,
    extra_facets: list[Any] | None = None,
    id: str | None = None,
    **file_kwargs: Any,
) -> ObservableObject:
    """ObservableObject + FileFacet + ContentDataFacet (MinimalForensics)."""
    facets: list[Any] = [
        FileFacet(
            file_name=file_name,
            file_path=file_path,
            size_in_bytes=size_in_bytes,
            **file_kwargs,
        ),
        ContentDataFacet(hash=_hashes(hashes), size_in_bytes=size_in_bytes),
    ]
    if extra_facets:
        facets.extend(extra_facets)
    return graph.create(ObservableObject, id=id, has_facet=facets)


def raster_picture_with_hashes(
    graph: CASEGraph,
    *,
    file_name: str,
    hashes: Sequence[tuple[str, str]],
    picture_type: str | None = None,
    extra_facets: list[Any] | None = None,
    id: str | None = None,
    **file_kwargs: Any,
) -> Any:
    """RasterPicture + FileFacet + ContentDataFacet + RasterPictureFacet."""
    from case_uco.uco.observable import RasterPicture

    facets: list[Any] = [
        FileFacet(file_name=file_name, **file_kwargs),
        ContentDataFacet(hash=_hashes(hashes)),
        RasterPictureFacet(picture_type=picture_type) if picture_type else RasterPictureFacet(),
    ]
    if extra_facets:
        facets.extend(extra_facets)
    return graph.create(RasterPicture, id=id, has_facet=facets)


def model_csam_evidence(
    graph: CASEGraph,
    *,
    file_name: str,
    hashes: Sequence[tuple[str, str]],
    hashing_tool_name: str = "PhotoDNA",
    hashing_tool_version: str | None = None,
    extra_facets: list[Any] | None = None,
) -> dict[str, Any]:
    """HashIntelligence helper: hashed RasterPicture + ContentHashingTool action.

    Does not invent a PhotoDNA Facet. Perceptual hashes are additional
    Hash entries (hashMethod e.g. ``PhotoDNA`` / ``PDNA``).
    """
    tool = graph.create(
        Tool,
        name=hashing_tool_name,
        version=hashing_tool_version,
        tool_type="Content hashing",
    )
    picture = raster_picture_with_hashes(
        graph,
        file_name=file_name,
        hashes=hashes,
        extra_facets=extra_facets,
    )
    action = graph.create(
        InvestigativeAction,
        name=f"{hashing_tool_name} hash of {file_name}",
        instrument=[tool],
        object=[picture],
        result=[picture],
    )
    return {"tool": tool, "picture": picture, "action": action}


def model_tool_run(
    graph: CASEGraph,
    *,
    tool_name: str,
    tool_version: str | None = None,
    action_name: str,
    inputs: list[Any] | None = None,
    outputs: list[Any] | None = None,
) -> dict[str, Any]:
    """ToolMapping helper: versioned Tool + InvestigativeAction."""
    tool = graph.create(Tool, name=tool_name, version=tool_version)
    action = graph.create(
        InvestigativeAction,
        name=action_name,
        instrument=[tool],
        object=inputs or [],
        result=outputs or [],
    )
    return {"tool": tool, "action": action}
