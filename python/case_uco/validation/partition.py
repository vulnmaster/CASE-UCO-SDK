"""Validation orchestration for marking-safe CASEGraph partition sets (#79)."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from case_uco.graph import CASEGraph
from case_uco.validation.graph import GraphValidationReport, validate_graph_file


@dataclass(frozen=True)
class PartitionValidationReport:
    """Validation and reconstruction evidence for a partition set."""

    validation_mode: str
    conforms: bool | None
    verification_status: str
    partition_reports: Mapping[str, GraphValidationReport]
    set_report: GraphValidationReport | None
    union_equivalent: bool | None
    verification_errors: tuple[str, ...] = ()


def validate_partition_set(
    partitions: Mapping[str, CASEGraph],
    manifest: Mapping[str, Any],
    *,
    source_graph: CASEGraph | None = None,
    project_root: str | Path | None = None,
    strict_concepts: bool = True,
    allow_warning: bool = True,
) -> PartitionValidationReport:
    """Validate partitions according to their v2 reconstruction manifest.

    ``self-contained`` partitions are validated individually. A
    ``referenced-partition-set`` may intentionally contain cross-partition
    references, so it is reconstructed and validated as one RDF union. When
    ``source_graph`` is supplied, RDF isomorphism is also checked.

    Only ontology extension/profile identifiers are accepted from the
    manifest. Filesystem roots remain explicit caller inputs so an untrusted
    manifest cannot redirect validation to arbitrary local paths.
    """

    if manifest.get("schema_version") != "2.0.0":
        raise ValueError("partition manifest schema_version must be '2.0.0'")
    mode = str(manifest.get("validation_mode", ""))
    if mode not in {"self-contained", "referenced-partition-set"}:
        raise ValueError(f"unsupported partition validation_mode: {mode!r}")

    reconstruction = manifest.get("reconstruction")
    if not isinstance(reconstruction, Mapping):
        raise ValueError("partition manifest is missing reconstruction metadata")
    required = reconstruction.get("requires_partitions")
    if not isinstance(required, list) or any(
        not isinstance(key, str) for key in required
    ):
        raise ValueError("reconstruction.requires_partitions must be a list of strings")
    missing = sorted(set(required) - set(partitions))
    unexpected = sorted(set(partitions) - set(required))
    if missing or unexpected:
        raise ValueError(
            f"partition set does not match manifest; missing={missing}, "
            f"unexpected={unexpected}"
        )

    bundle = manifest.get("validation_bundle") or {}
    if not isinstance(bundle, Mapping):
        raise ValueError("validation_bundle must be an object or null")
    extensions = _string_list(bundle.get("extensions"), "extensions")
    profiles = _string_list(bundle.get("profiles"), "profiles")
    validation_kwargs: dict[str, Any] = {
        "extensions": extensions,
        "profiles": profiles,
        "strict_concepts": strict_concepts,
        "allow_warning": allow_warning,
    }
    if project_root is not None:
        validation_kwargs["project_root"] = Path(project_root)

    union_equivalent: bool | None = None
    errors: list[str] = []
    if source_graph is not None:
        union_result = source_graph.verify_partition_union(dict(partitions))
        union_equivalent = bool(union_result["equivalent"])
        if not union_equivalent:
            errors.append("partition RDF union is not isomorphic to the source graph")

    partition_reports: dict[str, GraphValidationReport] = {}
    set_report: GraphValidationReport | None = None
    with tempfile.TemporaryDirectory(prefix="case-uco-partition-validation-") as tmp:
        tmp_dir = Path(tmp)
        if mode == "self-contained":
            for index, key in enumerate(required):
                graph_path = tmp_dir / f"partition-{index}.jsonld"
                partitions[key].write_streaming(str(graph_path))
                partition_reports[key] = validate_graph_file(
                    graph_path, **validation_kwargs
                )
        else:
            union = CASEGraph()
            union.on_duplicate = "merge_compatible"
            for key in required:
                union.load(
                    partitions[key].serialize(indent=None),
                    on_duplicate="merge_compatible",
                )
            union_path = tmp_dir / "partition-set.jsonld"
            union.write_streaming(str(union_path))
            set_report = validate_graph_file(union_path, **validation_kwargs)

    reports = [*partition_reports.values()]
    if set_report is not None:
        reports.append(set_report)
    if any(report.verification_status != "complete" for report in reports):
        errors.append("one or more validation stages could not verify")
    conforms: bool | None
    if errors:
        conforms = False
    elif not reports or any(report.conforms is None for report in reports):
        conforms = None
    else:
        conforms = all(report.conforms is True for report in reports)

    return PartitionValidationReport(
        validation_mode=mode,
        conforms=conforms,
        verification_status="complete" if not errors else "could_not_verify",
        partition_reports=partition_reports,
        set_report=set_report,
        union_equivalent=union_equivalent,
        verification_errors=tuple(errors),
    )


def _string_list(value: Any, field: str) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"validation_bundle.{field} must be a list of strings")
    return list(value)
