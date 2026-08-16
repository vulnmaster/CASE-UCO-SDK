"""Public CASE/UCO graph validation (SHACL + concept coverage + bundles).

This package is the canonical home for the rich validator previously kept
under ``mcp_server``. MCP tools and repo examples should import from here::

    from case_uco.validation import validate_graph_file, GraphValidationReport

    report = validate_graph_file(
        "graph.jsonld",
        extensions=["attack-technique:full"],
        profiles=[],
        strict_concepts=True,
        project_root="/path/to/CASE-UCO-Libraries",  # required for named extensions
    )
    assert report.conforms

**Extension ontology contract (external-bundle):** the installable ``case-uco``
wheel ships core registries and upper-ontology registry data only. Named
extensions such as ``attack-technique`` resolve from a repository/ontology
checkout via ``project_root`` (or explicit ontology graph paths). A bare
``pip install case-uco`` without a checkout cannot load named extensions.
"""

from case_uco.validation.graph import (
    GraphValidationReport,
    report_to_dict,
    validate_graph_file,
    validator_available,
)
from case_uco.validation.partition import (
    PartitionValidationReport,
    validate_partition_set,
)

__all__ = [
    "GraphValidationReport",
    "PartitionValidationReport",
    "report_to_dict",
    "validate_graph_file",
    "validate_partition_set",
    "validator_available",
]
