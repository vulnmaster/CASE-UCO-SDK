"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit_tool_profile module (generated; do not edit)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Optional

import case_uco.uco.core as _uco_core
import case_uco.uco.tool as _uco_tool
from case_uco_solveit._context import NAMESPACES

__all__ = ["ConditionTargetType", "MitigationCapability", "SolveitAwareInstrument", "ToolCapabilityProfile"]


@dataclass
class ConditionTargetType:
    """Enumeration of action components that conditions can evaluate against."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/ConditionTargetType"
    NAMESPACE_PREFIX: str = "solveit-tool-profile"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MitigationCapability(_uco_core.UcoObject):
    """A declared capability that a specific mitigation is provided by a tool, optionally subject to conditions expressed as SHACL shapes."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/MitigationCapability"
    NAMESPACE_PREFIX: str = "solveit-tool-profile"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    established_for_weakness: list[Weakness] = field(default_factory=list, metadata={'jsonld_key': 'solveit-tool-profile:establishedForWeakness', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/core/Weakness', 'alternate_range_iris': []})
    supporting_citation: list[Citation] = field(default_factory=list, metadata={'jsonld_key': 'solveit-tool-profile:supportingCitation', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/core/Citation', 'alternate_range_iris': []})


@dataclass
class SolveitAwareInstrument(_uco_tool.Tool):
    """A specialised tool that has been evaluated against SOLVE-IT tool capability profiles. Adds the consultedProfile property to link an instrument to the profiles used during mitigation assessment."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/SolveitAwareInstrument"
    NAMESPACE_PREFIX: str = "solveit-tool-profile"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ToolCapabilityProfile(_uco_core.UcoObject):
    """A declaration of what techniques a specific version of a tool can perform and what mitigations it implements, published by a named party. Distributed as a TTL file per tool version per publisher."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/ToolCapabilityProfile"
    NAMESPACE_PREFIX: str = "solveit-tool-profile"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    published_by: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'solveit-tool-profile:publishedBy', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
