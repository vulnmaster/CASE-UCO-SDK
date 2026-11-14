"""CASE/UCO Standard Library — construct and serialize CASE/UCO ontology graphs."""

from case_uco.graph import (
    CASEGraph,
    DeserializationWarning,
    DuplicateClassIriError,
    DuplicateNodeError,
    InvalidSplitSizeError,
    PartitionBoundaryError,
    SharedFacetError,
    class_registry_cache_info,
    clear_class_registry_cache,
    discover_extension_class_providers,
    register_extension_classes,
    unregister_extension_source,
)
from case_uco.ids import Ref, deterministic_id, deterministic_uuid
from case_uco.streaming import (
    BoundedStreamingWriteMetrics,
    JsonLdStreamWriter,
)
from case_uco.typed_literal import TypedLiteral

__all__ = [
    "BoundedStreamingWriteMetrics",
    "CASEGraph",
    "CASE_VERSION",
    "DeserializationWarning",
    "DuplicateClassIriError",
    "DuplicateNodeError",
    "InvalidSplitSizeError",
    "JsonLdStreamWriter",
    "PartitionBoundaryError",
    "Ref",
    "SharedFacetError",
    "TypedLiteral",
    "UCO_VERSION",
    "class_registry_cache_info",
    "clear_class_registry_cache",
    "deterministic_id",
    "deterministic_uuid",
    "discover_extension_class_providers",
    "register_extension_classes",
    "unregister_extension_source",
]
__version__ = "1.34.0"
UCO_VERSION = "1.5.0"
CASE_VERSION = "1.5.0"
