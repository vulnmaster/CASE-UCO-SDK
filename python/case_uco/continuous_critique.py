"""SDK wrapper around the existing MCP critic heuristics.

Does not reimplement CRIT-H-* rules. When the MCP critic package is
importable, this module serializes a ``CASEGraph`` and delegates to
``critic.continuous.critique_jsonld``. When it is not, the call fails
closed instead of inventing a parallel engine.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PUBLIC_SURFACE = ("critique_graph",)


class ContinuousCritiqueUnavailable(RuntimeError):
    """Raised when the existing MCP critic cannot be imported."""


def _ensure_critic_on_path() -> None:
    try:
        import critic.continuous  # noqa: F401

        return
    except ImportError:
        pass
    here = Path(__file__).resolve()
    # python/case_uco/continuous_critique.py → repo root → mcp_server
    repo_root = here.parents[2]
    mcp = repo_root / "mcp_server"
    if mcp.is_dir() and str(mcp) not in sys.path:
        sys.path.insert(0, str(mcp))


def critique_graph(
    graph: Any,
    *,
    profiles: list[str] | None = None,
) -> list[dict[str, str]]:
    """Return existing critic findings for ``graph``.

    Each finding includes a stable ``finding_id`` and a ``repair_hint``
    taken from the critic's ``recommended_change``. This is not a
    classifier and does not inspect file bytes.
    """
    _ensure_critic_on_path()
    try:
        from critic.continuous import critique_jsonld
    except ImportError as exc:
        raise ContinuousCritiqueUnavailable(
            "existing MCP critic is not importable; "
            "install/run from a CASE-UCO-SDK checkout that includes mcp_server/critic"
        ) from exc
    return critique_jsonld(graph.serialize(), profiles=profiles)
