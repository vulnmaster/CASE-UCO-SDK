"""Compatibility shim — implementation lives in ``case_uco.validation``.

MCP tools, critic, and older examples historically imported ``graph_validator``
from this directory. Prefer::

    from case_uco.validation import validate_graph_file, GraphValidationReport
"""

from __future__ import annotations

import shutil
from typing import Any

import case_uco.validation.graph as _impl

DEFAULT_BUILT_VERSION = _impl.DEFAULT_BUILT_VERSION
DEFAULT_TIMEOUT_SECONDS = _impl.DEFAULT_TIMEOUT_SECONDS
MAX_GRAPH_BYTES = _impl.MAX_GRAPH_BYTES
PROJECT_ROOT = _impl.PROJECT_ROOT
SUPPORTED_GRAPH_EXTENSIONS = _impl.SUPPORTED_GRAPH_EXTENSIONS
VALIDATOR_NAME = _impl.VALIDATOR_NAME
GraphValidationReport = _impl.GraphValidationReport
extension_has_validation_subset = _impl.extension_has_validation_subset
extension_ontology_args = _impl.extension_ontology_args
load_extension_ontology_paths = _impl.load_extension_ontology_paths
report_to_dict = _impl.report_to_dict
resolve_extension_dependencies = _impl.resolve_extension_dependencies


def validator_available() -> bool:
    """Check the validator in the SDK interpreter."""
    return _impl.validator_available()


def validate_graph_file(*args: Any, **kwargs: Any):
    """Delegate so monkeypatches of this module's MAX_GRAPH_BYTES apply."""
    saved = _impl.MAX_GRAPH_BYTES
    try:
        _impl.MAX_GRAPH_BYTES = MAX_GRAPH_BYTES
        return _impl.validate_graph_file(*args, **kwargs)
    finally:
        _impl.MAX_GRAPH_BYTES = saved


def _parse_conforms(output: str) -> bool | None:
    """Compatibility wrapper for tests that still call the private helper."""
    return _impl._parse_conforms(output)


__all__ = [
    "DEFAULT_BUILT_VERSION",
    "DEFAULT_TIMEOUT_SECONDS",
    "MAX_GRAPH_BYTES",
    "PROJECT_ROOT",
    "SUPPORTED_GRAPH_EXTENSIONS",
    "VALIDATOR_NAME",
    "GraphValidationReport",
    "extension_has_validation_subset",
    "extension_ontology_args",
    "load_extension_ontology_paths",
    "report_to_dict",
    "resolve_extension_dependencies",
    "shutil",
    "validate_graph_file",
    "validator_available",
    "_parse_conforms",
]
