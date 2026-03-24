"""Auto-generated uco-tool classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from case_uco.uco.core import Facet
from case_uco.uco.core import UcoInherentCharacterizationThing
from case_uco.uco.core import UcoObject


@dataclass
class Tool(UcoObject):
    """A tool is an element of hardware and/or software utilized to carry out a particular function."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/Tool"
    NAMESPACE_PREFIX: str = "uco-tool"

    creator: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-tool:creator', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    references: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-tool:references', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#anyURI', 'alternate_range_iris': []})
    service_pack: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:servicePack', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    tool_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:toolType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class AnalyticTool(Tool):
    """An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of explanation, interpretation or logical reasoning."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/AnalyticTool"
    NAMESPACE_PREFIX: str = "uco-tool"



@dataclass
class BuildFacet(Facet):
    """A build facet is a grouping of characteristics unique to a particular version of a software."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/BuildFacet"
    NAMESPACE_PREFIX: str = "uco-tool"

    build_information: Optional[BuildInformationType] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildInformation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/BuildInformationType', 'alternate_range_iris': []})


@dataclass
class BuildInformationType(UcoInherentCharacterizationThing):
    """A build information type is a grouping of characteristics that describe how a particular version of software was converted from source code to executable code."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/BuildInformationType"
    NAMESPACE_PREFIX: str = "uco-tool"

    build_configuration: Optional[Configuration] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildConfiguration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/configuration/Configuration', 'alternate_range_iris': []})
    build_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    build_label: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildLabel', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    build_output_log: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildOutputLog', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    build_project: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildProject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    build_script: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildScript', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    build_utility: Optional[BuildUtilityType] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildUtility', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/BuildUtilityType', 'alternate_range_iris': []})
    build_version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildVersion', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    compilation_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-tool:compilationDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    compilers: list[CompilerType] = field(default_factory=list, metadata={'jsonld_key': 'uco-tool:compilers', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/CompilerType', 'alternate_range_iris': []})
    libraries: list[LibraryType] = field(default_factory=list, metadata={'jsonld_key': 'uco-tool:libraries', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/LibraryType', 'alternate_range_iris': []})


@dataclass
class BuildUtilityType(UcoInherentCharacterizationThing):
    """A build utility type characterizes the tool used to convert from source code to executable code for a particular version of software."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/BuildUtilityType"
    NAMESPACE_PREFIX: str = "uco-tool"

    build_utility_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:buildUtilityName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cpeid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:cpeid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    swid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:swid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class CompilerType(UcoInherentCharacterizationThing):
    """A compiler type is a grouping of characteristics unique to a specific program that translates computer code written in one programming language (the source language) into another language (the target """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/CompilerType"
    NAMESPACE_PREFIX: str = "uco-tool"

    compiler_informal_description: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:compilerInformalDescription', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cpeid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:cpeid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    swid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:swid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ConfiguredTool(Tool):
    """A ConfiguredTool is a Tool that is known to be configured to run in a more specified manner than some unconfigured or less-configured Tool."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/ConfiguredTool"
    NAMESPACE_PREFIX: str = "uco-tool"

    is_configuration_of: Optional[Tool] = field(default=None, metadata={'jsonld_key': 'uco-configuration:isConfigurationOf', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/Tool', 'alternate_range_iris': []})
    uses_configuration: Optional[Configuration] = field(default=None, metadata={'jsonld_key': 'uco-configuration:usesConfiguration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/configuration/Configuration', 'alternate_range_iris': []})


@dataclass
class DefensiveTool(Tool):
    """A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of guarding."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/DefensiveTool"
    NAMESPACE_PREFIX: str = "uco-tool"



@dataclass
class LibraryType(UcoInherentCharacterizationThing):
    """A library type is a grouping of characteristics unique to a collection of resources incorporated into the build of a software."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/LibraryType"
    NAMESPACE_PREFIX: str = "uco-tool"

    library_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:libraryName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    library_version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-tool:libraryVersion', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MaliciousTool(Tool):
    """A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent task or purpose."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/tool/MaliciousTool"
    NAMESPACE_PREFIX: str = "uco-tool"


