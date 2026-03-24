"""Auto-generated uco-marking classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from case_uco.uco.core import MarkingDefinitionAbstraction
from case_uco.uco.core import UcoInherentCharacterizationThing


@dataclass
class GranularMarking(UcoInherentCharacterizationThing):
    """A granular marking is a grouping of characteristics unique to specification of marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) that apply to par"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/GranularMarking"
    NAMESPACE_PREFIX: str = "uco-marking"

    content_selectors: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:contentSelectors', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    marking: list[MarkingDefinition] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:marking', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/marking/MarkingDefinition', 'alternate_range_iris': []})


@dataclass
class MarkingModel(UcoInherentCharacterizationThing):
    """A marking model is a grouping of characteristics unique to the expression of a particular form of data marking definitions (restrictions, permissions, and other guidance for how data can be used and s"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingModel"
    NAMESPACE_PREFIX: str = "uco-marking"



@dataclass
class LicenseMarking(MarkingModel):
    """A license marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey de"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/LicenseMarking"
    NAMESPACE_PREFIX: str = "uco-marking"

    definition_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:definitionType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    license: str = field(default=None, metadata={'jsonld_key': 'uco-marking:license', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MarkingDefinition(MarkingDefinitionAbstraction):
    """A marking definition is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be used and sh"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingDefinition"
    NAMESPACE_PREFIX: str = "uco-marking"

    definition: list[MarkingModel] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:definition', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/marking/MarkingModel', 'alternate_range_iris': []})
    definition_type: str = field(default=None, metadata={'jsonld_key': 'uco-marking:definitionType', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ReleaseToMarking(MarkingModel):
    """A release-to marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/ReleaseToMarking"
    NAMESPACE_PREFIX: str = "uco-marking"

    authorized_identities: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:authorizedIdentities', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    definition_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:definitionType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class StatementMarking(MarkingModel):
    """A statement marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/StatementMarking"
    NAMESPACE_PREFIX: str = "uco-marking"

    definition_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:definitionType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    statement: str = field(default=None, metadata={'jsonld_key': 'uco-marking:statement', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class TermsOfUseMarking(MarkingModel):
    """A terms of use marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to conv"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/marking/TermsOfUseMarking"
    NAMESPACE_PREFIX: str = "uco-marking"

    definition_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-marking:definitionType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    terms_of_use: str = field(default=None, metadata={'jsonld_key': 'uco-marking:termsOfUse', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})

