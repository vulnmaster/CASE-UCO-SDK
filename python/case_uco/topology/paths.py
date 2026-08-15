"""Locate topology artifacts without network access."""

from __future__ import annotations

import os
from pathlib import Path


def _unique(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen or not path.exists():
            continue
        seen.add(resolved)
        out.append(path)
    return out


def repo_root_candidates() -> list[Path]:
    starts = [Path(__file__).resolve(), Path.cwd()]
    found: list[Path] = []
    for start in starts:
        for parent in [start, *start.parents]:
            if (parent / "topology").is_dir() and (parent / "python" / "case_uco").is_dir():
                found.append(parent)
                break
    return _unique(found)


def profile_dirs() -> list[Path]:
    dirs: list[Path] = []
    env = os.environ.get("CASE_UCO_TOPOLOGY_DIR")
    if env:
        dirs.append(Path(env) / "profiles" if not env.endswith("profiles") else Path(env))
    for root in repo_root_candidates():
        dirs.append(root / "topology" / "profiles")
    packaged = Path(__file__).resolve().parent / "data" / "profiles"
    dirs.append(packaged)
    return _unique(dirs)


def topology_file(name: str) -> Path | None:
    env = os.environ.get("CASE_UCO_TOPOLOGY_DIR")
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env) / name)
    for root in repo_root_candidates():
        candidates.append(root / "topology" / name)
    packaged = Path(__file__).resolve().parent / "data" / name
    candidates.append(packaged)
    for path in candidates:
        if path.is_file():
            return path
    return None
