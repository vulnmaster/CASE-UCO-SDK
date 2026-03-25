#!/usr/bin/env python3
"""Example: Build a forensic tool capability matrix using CASE/UCO + toolcap extension.

This demonstrates the use case of comparing which forensic tools can parse
which applications on which platforms — the core problem this project solves.

Output: A CASE/UCO-compliant JSON-LD graph representing the capability matrix.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "python"))

from case_uco.graph import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.uco.observable import ObservableObject, ApplicationFacet


# Since the toolcap extension classes aren't generated yet (they live in a
# supplemental TTL), we manually define them here as dataclasses that follow
# the same pattern as the generated classes.
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ToolCapability:
    """A tool capability asserts that a forensic tool can parse data from a specific application."""

    CLASS_IRI: str = "http://example.org/ontology/toolcap/ToolCapability"
    NAMESPACE_PREFIX: str = "toolcap"

    tool: Optional[Tool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:tool', 'required': True, 'cardinality': 'exactly_one',
        'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/Tool', 'alternate_range_iris': []})
    application: Optional[ObservableObject] = field(default=None, metadata={
        'jsonld_key': 'toolcap:application', 'required': True, 'cardinality': 'exactly_one',
        'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    supported_platform: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:supportedPlatform', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    parsed_observable_type: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:parsedObservableType', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    tool_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:toolVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_verified: Optional[bool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:isVerified', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    last_tested_date: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:lastTestedDate', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class CapabilityMatrix:
    """A collection of tool capabilities representing a comparison matrix."""

    CLASS_IRI: str = "http://example.org/ontology/toolcap/CapabilityMatrix"
    NAMESPACE_PREFIX: str = "toolcap"

    matrix_name: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:matrixName', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    matrix_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:matrixVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


def main():
    graph = CASEGraph(
        kb_prefix="http://example.org/forensic-lab/kb/",
        extra_context={
            "toolcap": "http://example.org/ontology/toolcap/",
        },
    )

    # Define forensic tools
    axiom = graph.create(Tool, name="Magnet AXIOM", version="7.0", tool_type="forensic")
    cellebrite = graph.create(Tool, name="Cellebrite Physical Analyzer", version="7.68", tool_type="forensic")

    # Define applications as observable objects with ApplicationFacet
    wechat = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.tencent.mm")],
    )
    telegram = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="org.telegram.messenger")],
    )
    outlook = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.microsoft.office.outlook")],
    )

    # Define capabilities: which tools can parse which apps
    # AXIOM supports WeChat, Telegram, and Outlook
    graph.add(ToolCapability(
        tool=axiom,
        application=wechat,
        supported_platform=["Android", "iOS"],
        parsed_observable_type=["messages", "contacts", "media"],
        tool_version="7.0",
        is_verified=True,
    ))
    graph.add(ToolCapability(
        tool=axiom,
        application=telegram,
        supported_platform=["Android", "iOS"],
        parsed_observable_type=["messages", "contacts"],
        tool_version="7.0",
        is_verified=True,
    ))
    graph.add(ToolCapability(
        tool=axiom,
        application=outlook,
        supported_platform=["Android", "iOS", "Windows"],
        parsed_observable_type=["emails", "contacts", "calendar"],
        tool_version="7.0",
        is_verified=True,
    ))

    # Cellebrite supports WeChat and Telegram
    graph.add(ToolCapability(
        tool=cellebrite,
        application=wechat,
        supported_platform=["Android"],
        parsed_observable_type=["messages", "contacts"],
        tool_version="7.68",
        is_verified=True,
    ))
    graph.add(ToolCapability(
        tool=cellebrite,
        application=telegram,
        supported_platform=["Android", "iOS"],
        parsed_observable_type=["messages", "media"],
        tool_version="7.68",
        is_verified=True,
    ))

    # Create a capability matrix compilation
    graph.add(CapabilityMatrix(
        matrix_name="Forensic Tool Messaging App Support",
        matrix_version="1.0",
    ))

    print(graph.serialize())


if __name__ == "__main__":
    main()
