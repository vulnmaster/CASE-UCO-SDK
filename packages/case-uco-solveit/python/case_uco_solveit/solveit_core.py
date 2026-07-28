"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit-core module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ASTMErrorCategory:
    """An error category from ASTM E3016-18 used to classify weakness impacts."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/ASTMErrorCategory"


@dataclass
class Mitigation:
    """An action that can be performed to prevent a weakness from occurring or to minimize its impact."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Mitigation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    action_count: Optional[int] = field(default=None)
    action_status: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)


@dataclass
class Objective:
    """A goal or objective in a digital forensic investigation that can be achieved through one or more techniques."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Objective"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)


@dataclass
class SolveitInvestigativeAction:
    """A SOLVE-IT aware InvestigativeAction that links an investigative action to the SOLVE-IT technique(s) used (1..n via usedTechnique) and any mitigations applied (0..n via appliedMitigation) during its execution.

    Action-namespace fields carry explicit ``jsonld_key`` metadata so
    serialization emits ``uco-action:*`` / ``case-investigation:*`` keys
    (the metadata-less fallback would wrongly emit ``uco-core:*``).
    ``used_technique`` / ``applied_mitigation`` accept catalog IRI
    references, e.g. ``[{"@id": ".../solveit/data/techniqueDFT-1066"}]``.
    """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/SolveitInvestigativeAction"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    action_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-action:actionCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    action_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-action:actionStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-action:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    environment: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-action:environment', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    error: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:error', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    instrument: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:instrument', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    location: list[Location] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:location', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})
    object: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:object', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    participant: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:participant', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    performer: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-action:performer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    result: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:result', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-action:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    subaction: list[Action] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:subaction', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/action/Action', 'alternate_range_iris': []})
    was_informed_by: list[InvestigativeAction] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:wasInformedBy', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.caseontology.org/case/investigation/InvestigativeAction', 'alternate_range_iris': []})
    used_technique: list[Technique] = field(default_factory=list, metadata={'jsonld_key': 'solveit-core:usedTechnique', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/core/Technique', 'alternate_range_iris': []})
    applied_mitigation: list[Mitigation] = field(default_factory=list, metadata={'jsonld_key': 'solveit-core:appliedMitigation', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/core/Mitigation', 'alternate_range_iris': []})


@dataclass
class Technique:
    """A digital forensic technique representing how one might achieve an objective by performing an action. Based on the SOLVE-IT knowledge base."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Technique"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    action_count: Optional[int] = field(default=None)
    action_status: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)


@dataclass
class Weakness:
    """A potential problem resulting from using a technique, classified according to ASTM E3016-18 error categories."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Weakness"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)

