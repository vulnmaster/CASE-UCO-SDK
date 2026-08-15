"""Optional jsonschema validation of profile/contract documents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from case_uco.topology.paths import profile_dirs


def profile_schema_path() -> Path | None:
    for directory in profile_dirs():
        candidate = directory / "profile.schema.json"
        if candidate.is_file():
            return candidate
    return None


def validate_profile_document(raw: dict[str, Any]) -> list[str]:
    """Return a list of validation errors (empty = ok).

    Uses jsonschema when installed; otherwise checks required keys only.
    """
    required = {
        "id",
        "version",
        "title",
        "description",
        "required_modules",
        "recommended_modules",
        "facet_sets",
        "spine_anchors",
        "upper_ontology_profiles",
        "recipe_skeleton",
    }
    missing = required - set(raw)
    errors = [f"missing {name}" for name in sorted(missing)]
    schema_path = profile_schema_path()
    if schema_path is None:
        return errors
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError:
        return errors
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors.extend(f"{list(err.path)}: {err.message}" for err in validator.iter_errors(raw))
    return errors
