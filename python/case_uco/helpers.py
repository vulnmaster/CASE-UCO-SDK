"""Generic fluent helpers for common CASE/UCO construction patterns.

Additive wrappers around existing generated classes. They do not replace
constructors, add ontology terms, or classify content.

These helpers only assemble the existing FileFacet / ContentDataFacet /
RasterPictureFacet / Tool / InvestigativeAction patterns so hashed files,
raster media, and tool-run provenance are hard to get wrong.
"""

from __future__ import annotations

from typing import Any, Sequence

from case_uco.case.investigation import InvestigativeAction
from case_uco.graph import CASEGraph
from case_uco.uco.observable import (
    ContentDataFacet,
    FileFacet,
    ObservableObject,
    RasterPicture,
    RasterPictureFacet,
)
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

PUBLIC_HELPERS = (
    "file_with_content_hashes",
    "raster_picture_with_hashes",
    "model_tool_run",
)


def _hashes(pairs: Sequence[tuple[str, str]]) -> list[Hash]:
    if not pairs:
        raise ValueError("at least one (hash_method, hash_value) pair is required")
    out: list[Hash] = []
    for method, value in pairs:
        method_s = method.strip() if isinstance(method, str) else ""
        value_s = value.strip() if isinstance(value, str) else ""
        if not method_s or not value_s:
            raise ValueError("each hash must include a non-empty method and value")
        out.append(Hash(hash_method=method_s, hash_value=value_s))
    return out


def _file_facet(
    file_name: str,
    *,
    file_path: str | None = None,
    size_in_bytes: int | None = None,
    **file_kwargs: Any,
) -> FileFacet:
    fields: dict[str, Any] = {"file_name": [file_name], **file_kwargs}
    if file_path is not None:
        fields["file_path"] = [file_path]
    if size_in_bytes is not None:
        fields["size_in_bytes"] = size_in_bytes
    return FileFacet(**fields)


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
    """ObservableObject + FileFacet + ContentDataFacet.

    Puts content hashes on ``ContentDataFacet.hash``, not on a parallel
    object. Does not classify the file.
    """
    content_fields: dict[str, Any] = {"hash": _hashes(hashes)}
    if size_in_bytes is not None:
        content_fields["size_in_bytes"] = size_in_bytes
    facets: list[Any] = [
        _file_facet(
            file_name,
            file_path=file_path,
            size_in_bytes=size_in_bytes,
            **file_kwargs,
        ),
        ContentDataFacet(**content_fields),
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
) -> RasterPicture:
    """RasterPicture + FileFacet + ContentDataFacet + RasterPictureFacet.

    Same hash placement as :func:`file_with_content_hashes`. Does not
    classify the picture.
    """
    picture_facet = (
        RasterPictureFacet(picture_type=picture_type)
        if picture_type
        else RasterPictureFacet()
    )
    facets: list[Any] = [
        _file_facet(file_name, **file_kwargs),
        ContentDataFacet(hash=_hashes(hashes)),
        picture_facet,
    ]
    if extra_facets:
        facets.extend(extra_facets)
    return graph.create(RasterPicture, id=id, has_facet=facets)


def model_tool_run(
    graph: CASEGraph,
    *,
    tool_name: str,
    action_name: str,
    tool_version: str | None = None,
    tool_type: str | None = None,
    inputs: list[Any] | None = None,
    outputs: list[Any] | None = None,
    id: str | None = None,
) -> dict[str, Any]:
    """Versioned Tool + InvestigativeAction with instrument / object / result.

    Records that a named tool ran, what it consumed, and what it produced.
    Does not invent a ``ProvenanceRecord``; attach one with the existing
    constructor when an exhibit number is needed.
    """
    tool_kwargs: dict[str, Any] = {"name": tool_name, "version": tool_version}
    if tool_type:
        tool_kwargs["tool_type"] = tool_type
    tool = graph.create(Tool, **tool_kwargs)
    action = graph.create(
        InvestigativeAction,
        id=id,
        name=action_name,
        instrument=[tool],
        object=list(inputs or []),
        result=list(outputs or []),
    )
    return {"tool": tool, "action": action}
