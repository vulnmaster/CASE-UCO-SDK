"""Auto-generated uco-action classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from case_uco.uco.core import Facet
from case_uco.uco.core import UcoInherentCharacterizationThing
from case_uco.uco.core import UcoObject


@dataclass
class Action(UcoObject):
    """An action is something that may be done or performed."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/Action"
    NAMESPACE_PREFIX: str = "uco-action"

    action_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-action:actionCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    action_status: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:actionStatus', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
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


@dataclass
class ActionArgumentFacet(Facet):
    """An action argument facet is a grouping of characteristics unique to a single parameter of an action."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/ActionArgumentFacet"
    NAMESPACE_PREFIX: str = "uco-action"

    argument_name: str = field(default=None, metadata={'jsonld_key': 'uco-action:argumentName', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    value: str = field(default=None, metadata={'jsonld_key': 'uco-action:value', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ActionEstimationFacet(Facet):
    """An action estimation facet is a grouping of characteristics unique to decision-focused approximation aspects for an action that may potentially be performed."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/ActionEstimationFacet"
    NAMESPACE_PREFIX: str = "uco-action"

    estimated_cost: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-action:estimatedCost', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    estimated_efficacy: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-action:estimatedEfficacy', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    estimated_impact: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-action:estimatedImpact', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    objective: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-action:objective', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ActionFrequencyFacet(Facet):
    """An action frequency facet is a grouping of characteristics unique to the frequency of occurrence for an action."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/ActionFrequencyFacet"
    NAMESPACE_PREFIX: str = "uco-action"

    rate: float = field(default=None, metadata={'jsonld_key': 'uco-action:rate', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    scale: str = field(default=None, metadata={'jsonld_key': 'uco-action:scale', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    trend: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:trend', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    units: str = field(default=None, metadata={'jsonld_key': 'uco-action:units', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ActionLifecycle(Action):
    """An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action lifecycles."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/ActionLifecycle"
    NAMESPACE_PREFIX: str = "uco-action"

    action_count: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:actionCount', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    end_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:endTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    error: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:error', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    phase: ArrayOfAction = field(default=None, metadata={'jsonld_key': 'uco-action:phase', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/action/ArrayOfAction', 'alternate_range_iris': []})
    start_time: list[datetime] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:startTime', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class ActionPattern(Action):
    """An action pattern is a grouping of characteristics unique to a combination of actions forming a consistent or characteristic arrangement."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/ActionPattern"
    NAMESPACE_PREFIX: str = "uco-action"



@dataclass
class ArrayOfAction(UcoInherentCharacterizationThing):
    """An array of action is an ordered list of references to things that may be done or performed."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/action/ArrayOfAction"
    NAMESPACE_PREFIX: str = "uco-action"

    action: list[Action] = field(default_factory=list, metadata={'jsonld_key': 'uco-action:action', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/action/Action', 'alternate_range_iris': []})

