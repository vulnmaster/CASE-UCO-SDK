"""Auto-generated uco-core classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from case_uco.uco.types import Dictionary


@dataclass
class UcoThing:
    """UcoThing is the top-level class within UCO."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/UcoThing"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class UcoObject(UcoThing):
    """A UCO object is a representation of a fundamental concept either directly inherent to the cyber domain or indirectly related to the cyber domain and necessary for contextually characterizing cyber dom"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/UcoObject"
    NAMESPACE_PREFIX: str = "uco-core"

    created_by: Optional[IdentityAbstraction] = field(default=None, metadata={'jsonld_key': 'uco-core:createdBy', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/IdentityAbstraction', 'alternate_range_iris': []})
    description: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:description', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    external_reference: list[ExternalReference] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:externalReference', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/ExternalReference', 'alternate_range_iris': []})
    has_facet: list[Facet] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:hasFacet', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/Facet', 'alternate_range_iris': []})
    modified_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:modifiedTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    object_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-core:objectCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:objectMarking', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/MarkingDefinitionAbstraction', 'alternate_range_iris': []})
    object_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:objectStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    spec_version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:specVersion', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    tag: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:tag', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Assertion(UcoObject):
    """An assertion is a statement declared to be true."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Assertion"
    NAMESPACE_PREFIX: str = "uco-core"

    statement: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:statement', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Annotation(Assertion):
    """An annotation is an assertion made in relation to one or more objects."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Annotation"
    NAMESPACE_PREFIX: str = "uco-core"

    object: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:object', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})


@dataclass
class AttributedName(UcoObject):
    """An attributed name is a name of an entity issued by some attributed naming authority."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/AttributedName"
    NAMESPACE_PREFIX: str = "uco-core"

    naming_authority: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:namingAuthority', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Compilation(UcoObject):
    """A compilation is a grouping of things."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Compilation"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class EnclosingCompilation(Compilation):
    """An enclosing compilation is a container for a grouping of things."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/EnclosingCompilation"
    NAMESPACE_PREFIX: str = "uco-core"

    object: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:object', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})


@dataclass
class Bundle(EnclosingCompilation):
    """A bundle is a container for a grouping of UCO content with no presumption of shared context."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Bundle"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class UcoInherentCharacterizationThing(UcoThing):
    """A UCO inherent characterization thing is a grouping of characteristics unique to a particular inherent aspect of a UCO domain object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/UcoInherentCharacterizationThing"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class Facet(UcoInherentCharacterizationThing):
    """A facet is a grouping of characteristics singularly unique to a particular inherent aspect of a UCO domain object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Facet"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class ConfidenceFacet(Facet):
    """A confidence is a grouping of characteristics unique to an asserted level of certainty in the accuracy of some information."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/ConfidenceFacet"
    NAMESPACE_PREFIX: str = "uco-core"

    confidence: int = field(default=None, metadata={'jsonld_key': 'uco-core:confidence', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})


@dataclass
class ContextualCompilation(Compilation):
    """A contextual compilation is a grouping of things sharing some context (e.g., a set of network connections observed on a given day, all accounts associated with a given person)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/ContextualCompilation"
    NAMESPACE_PREFIX: str = "uco-core"

    object: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:object', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})


@dataclass
class ControlledVocabulary(UcoObject):
    """A controlled vocabulary is an explicitly constrained set of string values."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/ControlledVocabulary"
    NAMESPACE_PREFIX: str = "uco-core"

    constraining_vocabulary_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:constrainingVocabularyName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    constraining_vocabulary_reference: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:constrainingVocabularyReference', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#anyURI', 'alternate_range_iris': []})
    value: str = field(default=None, metadata={'jsonld_key': 'uco-core:value', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Event(UcoObject):
    """An Event is a noteworthy occurrence (something that happens or might happen)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Event"
    NAMESPACE_PREFIX: str = "uco-core"

    end_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:endTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    event_attribute: list[Dictionary] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:eventAttribute', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    event_context: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:eventContext', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    event_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:eventType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    start_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:startTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class ExternalReference(UcoInherentCharacterizationThing):
    """Characteristics of a reference to a resource outside of the UCO."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/ExternalReference"
    NAMESPACE_PREFIX: str = "uco-core"

    defining_context: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:definingContext', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    external_identifier: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:externalIdentifier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    reference_url: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:referenceURL', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#anyURI', 'alternate_range_iris': []})


@dataclass
class Grouping(ContextualCompilation):
    """A grouping is a compilation of referenced UCO content with a shared context."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Grouping"
    NAMESPACE_PREFIX: str = "uco-core"

    context: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:context', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class IdentityAbstraction(UcoObject):
    """An identity abstraction is a grouping of identifying characteristics unique to an individual or organization. This class is an ontological structural abstraction for this concept. Implementations of t"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/IdentityAbstraction"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class Item(UcoObject):
    """An item is a distinct article or unit."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Item"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class MarkingDefinitionAbstraction(UcoObject):
    """A marking definition abstraction is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/MarkingDefinitionAbstraction"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class ModusOperandi(UcoObject):
    """A modus operandi is a particular method of operation (how a particular entity behaves or the resources they use)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/ModusOperandi"
    NAMESPACE_PREFIX: str = "uco-core"



@dataclass
class Relationship(UcoObject):
    """A relationship is a grouping of characteristics unique to an assertion that one or more objects are related to another object in some way."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/core/Relationship"
    NAMESPACE_PREFIX: str = "uco-core"

    end_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:endTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_directional: bool = field(default=None, metadata={'jsonld_key': 'uco-core:isDirectional', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    kind_of_relationship: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:kindOfRelationship', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    source: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:source', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    start_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:startTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    target: UcoObject = field(default=None, metadata={'jsonld_key': 'uco-core:target', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})

