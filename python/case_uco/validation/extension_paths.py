"""Central resolver for extension/ontology directories (v1.19.0).

The SDK vendors ontologies in two roots:

- ``ontology/`` — upstream-maintained ontologies synced from external
  sources: CASE and UCO (git submodules), plus the CAC Ontology, the
  Adversary Engagement Ontology (AEO), and SOLVE-IT. These are published
  by their own projects and only *mirrored* here.
- ``extensions/`` — SDK-developed extension ontologies (toolcap,
  attack-technique, rico, legalproc, cryptoinv, drugs, weapons, ...) and
  candidate extensions produced by the learning lifecycle.

Every module that needs ``<root>/<name>/manifest.json`` (or any other file
inside an extension directory) must resolve the directory through this
module instead of hardcoding ``project_root / "extensions"`` so that both
roots are searched uniformly. Name-based APIs (``CASE_UCO_EXTENSIONS=cac``)
are unaffected by which root an extension lives in.
"""

from __future__ import annotations

import os
from pathlib import Path

# Subdirectories of ontology/ that are not extension directories.
_NON_EXTENSION_DIRS = {"CASE", "UCO", "upper"}


def _discover_project_root() -> Path:
    """Locate the monorepo root that holds ``extensions/`` and ``ontology/``."""
    here = Path(__file__).resolve()
    for candidate in (here.parents[3], here.parents[2], Path.cwd(), *here.parents):
        if (candidate / "extensions").is_dir() and (candidate / "ontology").exists():
            return candidate
    return here.parents[3]


PROJECT_ROOT = _discover_project_root()


def extension_roots(
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> tuple[Path, Path]:
    """Both extension roots, in search order (SDK-native first)."""
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    return (project_root / "extensions", project_root / "ontology")


def native_extension_root(
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> Path:
    """Root for SDK-developed extensions (also where new candidates land)."""
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    return project_root / "extensions"


def find_extension_dir(
    name: str,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> Path | None:
    """Return the directory for a named extension, or None if not vendored.

    A directory qualifies when it contains a ``manifest.json``; the legacy
    manifest-less layout (pre-manifest extensions) is honored only under
    ``extensions/``.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    if not name or name in _NON_EXTENSION_DIRS:
        return None
    for root in extension_roots(project_root):
        candidate = root / name
        if (candidate / "manifest.json").is_file():
            return candidate
    legacy = native_extension_root(project_root) / name
    if legacy.is_dir():
        return legacy
    return None


def extension_dir(
    name: str,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> Path:
    """Like :func:`find_extension_dir` but falls back to the native root.

    Callers that *create* extension directories (candidate scaffolding) or
    build error messages need a concrete path even when nothing exists yet.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    found = find_extension_dir(name, project_root)
    return found if found is not None else native_extension_root(project_root) / name


def extension_manifest_path(
    name: str,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> Path:
    """Path of the manifest for a named extension (may not exist)."""
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    return extension_dir(name, project_root) / "manifest.json"


def iter_extension_dirs(
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
) -> list[Path]:
    """All vendored extension directories carrying a manifest.json.

    Sorted by directory name; when the same name appears in both roots the
    SDK-native (``extensions/``) copy wins, matching the search order of
    :func:`find_extension_dir`.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    found: dict[str, Path] = {}
    for root in extension_roots(project_root):
        if not root.is_dir():
            continue
        for manifest in root.glob("*/manifest.json"):
            ext_dir = manifest.parent
            if ext_dir.name in _NON_EXTENSION_DIRS:
                continue
            found.setdefault(ext_dir.name, ext_dir)
    return [found[name] for name in sorted(found)]


__all__ = [
    "PROJECT_ROOT",
    "extension_roots",
    "native_extension_root",
    "find_extension_dir",
    "extension_dir",
    "extension_manifest_path",
    "iter_extension_dirs",
]
