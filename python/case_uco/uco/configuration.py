"""Auto-generated uco-configuration classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from case_uco.uco.core import UcoInherentCharacterizationThing
from case_uco.uco.core import UcoObject


@dataclass
class Configuration(UcoObject):
    """A configuration is a grouping of characteristics unique to a set of parameters or initial settings for the use of a tool, application, software, or other cyber object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/configuration/Configuration"
    NAMESPACE_PREFIX: str = "uco-configuration"

    configuration_entry: list[ConfigurationEntry] = field(default_factory=list, metadata={'jsonld_key': 'uco-configuration:configurationEntry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/configuration/ConfigurationEntry', 'alternate_range_iris': []})
    dependencies: list[Dependency] = field(default_factory=list, metadata={'jsonld_key': 'uco-configuration:dependencies', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/configuration/Dependency', 'alternate_range_iris': []})
    usage_context_assumptions: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-configuration:usageContextAssumptions', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ConfigurationEntry(UcoInherentCharacterizationThing):
    """A configuration entry is a grouping of characteristics unique to a particular parameter or initial setting for the use of a tool, application, software, or other cyber object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/configuration/ConfigurationEntry"
    NAMESPACE_PREFIX: str = "uco-configuration"

    item_description: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-configuration:itemDescription', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    item_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-configuration:itemName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    item_object: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-configuration:itemObject', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    item_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-configuration:itemType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    item_value: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-configuration:itemValue', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Dependency(UcoInherentCharacterizationThing):
    """A dependency is a grouping of characteristics unique to something that a tool or other software relies on to function as intended."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/configuration/Dependency"
    NAMESPACE_PREFIX: str = "uco-configuration"

    dependency_description: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-configuration:dependencyDescription', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    dependency_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-configuration:dependencyType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})

