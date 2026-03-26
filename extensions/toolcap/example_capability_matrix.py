#!/usr/bin/env python3
"""Example: Build a forensic tool capability matrix using CASE/UCO + toolcap extension v0.2.0.

This demonstrates the full toolcap workflow:
  - Define forensic tools and target applications
  - Create structured PlatformSpecifications (including BFU acquisition)
  - Declare ToolCapability assertions with vendor-claim and benchmark flags
  - Attach AccessRestrictions (licensing, OPSEC)
  - Record BenchmarkObservations with completeness/accuracy metrics
  - Assemble everything into a CapabilityMatrix

Scenario: Two tools (Tool A commercial, Tool B law-enforcement-only) are
compared for their ability to parse a messaging app on mobile and Outlook
on Windows. Outlook has a legacy .pst format (both tools pass) and a new
.nst format (both tools fail).

Output: A CASE/UCO-compliant JSON-LD graph representing the capability matrix.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "python"))

from case_uco.graph import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.uco.observable import ObservableObject, ApplicationFacet

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Extension dataclasses (mirrors the toolcap TTL definitions)
# ---------------------------------------------------------------------------

@dataclass
class PlatformSpecification:
    CLASS_IRI: str = "http://example.org/ontology/toolcap/PlatformSpecification"
    NAMESPACE_PREFIX: str = "toolcap"

    operating_system: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:operatingSystem', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    os_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:osVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    device_model: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:deviceModel', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    extraction_method: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:extractionMethod', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class AccessRestriction:
    CLASS_IRI: str = "http://example.org/ontology/toolcap/AccessRestriction"
    NAMESPACE_PREFIX: str = "toolcap"

    restriction_type: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:restrictionType', 'required': True, 'cardinality': 'exactly_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    restriction_level: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:restrictionLevel', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    restriction_description: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:restrictionDescription', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ToolCapability:
    CLASS_IRI: str = "http://example.org/ontology/toolcap/ToolCapability"
    NAMESPACE_PREFIX: str = "toolcap"

    tool: Optional[Tool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:tool', 'required': True, 'cardinality': 'exactly_one',
        'range_iri': 'https://ontology.unifiedcyberontology.org/uco/tool/Tool', 'alternate_range_iris': []})
    application: Optional[ObservableObject] = field(default=None, metadata={
        'jsonld_key': 'toolcap:application', 'required': True, 'cardinality': 'exactly_one',
        'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    supports_platform: list[PlatformSpecification] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:supportsPlatform', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://example.org/ontology/toolcap/PlatformSpecification', 'alternate_range_iris': []})
    parsed_observable_type: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:parsedObservableType', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    tool_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:toolVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    application_version: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:applicationVersion', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    data_format_version: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:dataFormatVersion', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    claimed_by_vendor: Optional[bool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:claimedByVendor', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    verified_by_benchmark: Optional[bool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:verifiedByBenchmark', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_verified: Optional[bool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:isVerified', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    last_tested_date: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:lastTestedDate', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    has_access_restriction: list[AccessRestriction] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:hasAccessRestriction', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://example.org/ontology/toolcap/AccessRestriction', 'alternate_range_iris': []})


@dataclass
class BenchmarkObservation:
    CLASS_IRI: str = "http://example.org/ontology/toolcap/BenchmarkObservation"
    NAMESPACE_PREFIX: str = "toolcap"

    capability: Optional[ToolCapability] = field(default=None, metadata={
        'jsonld_key': 'toolcap:capability', 'required': True, 'cardinality': 'exactly_one',
        'range_iri': 'http://example.org/ontology/toolcap/ToolCapability', 'alternate_range_iris': []})
    benchmark_date: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:benchmarkDate', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    parse_success: Optional[bool] = field(default=None, metadata={
        'jsonld_key': 'toolcap:parseSuccess', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    completeness_score: Optional[float] = field(default=None, metadata={
        'jsonld_key': 'toolcap:completenessScore', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    accuracy_score: Optional[float] = field(default=None, metadata={
        'jsonld_key': 'toolcap:accuracyScore', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    false_positive_count: Optional[int] = field(default=None, metadata={
        'jsonld_key': 'toolcap:falsePositiveCount', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    false_negative_count: Optional[int] = field(default=None, metadata={
        'jsonld_key': 'toolcap:falseNegativeCount', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    parsed_category: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:parsedCategory', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    missed_category: list[str] = field(default_factory=list, metadata={
        'jsonld_key': 'toolcap:missedCategory', 'required': False, 'cardinality': 'zero_or_more',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    benchmark_notes: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:benchmarkNotes', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    benchmark_platform: Optional[PlatformSpecification] = field(default=None, metadata={
        'jsonld_key': 'toolcap:benchmarkPlatform', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://example.org/ontology/toolcap/PlatformSpecification', 'alternate_range_iris': []})
    tested_tool_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:testedToolVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    tested_application_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:testedApplicationVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    tested_data_format_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:testedDataFormatVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class CapabilityMatrix:
    CLASS_IRI: str = "http://example.org/ontology/toolcap/CapabilityMatrix"
    NAMESPACE_PREFIX: str = "toolcap"

    matrix_name: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:matrixName', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    matrix_version: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'toolcap:matrixVersion', 'required': False, 'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def main():
    graph = CASEGraph(
        kb_prefix="http://example.org/forensic-lab/kb/",
        extra_context={
            "toolcap": "http://example.org/ontology/toolcap/",
        },
    )

    # --- Tools ---
    tool_a = graph.create(Tool, name="Tool A", version="8.2.0", tool_type="forensic")
    tool_b = graph.create(Tool, name="Tool B", version="7.70", tool_type="forensic")

    # --- Applications ---
    app_alpha = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.example.app.alpha")],
    )
    outlook = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.microsoft.outlook")],
    )

    # --- Platforms ---
    android_physical = graph.add(PlatformSpecification(
        operating_system="Android",
        os_version="14",
        extraction_method=["physical", "file-system"],
    ))
    android_bfu = graph.add(PlatformSpecification(
        operating_system="Android",
        os_version="14",
        extraction_method=["BFU"],
    ))
    ios_logical = graph.add(PlatformSpecification(
        operating_system="iOS",
        os_version="17.4",
        device_model="iPhone 15",
        extraction_method=["logical"],
    ))
    windows_logical = graph.add(PlatformSpecification(
        operating_system="Windows",
        os_version="11 23H2",
        extraction_method=["logical"],
    ))

    # --- Access Restrictions ---
    commercial_license = graph.add(AccessRestriction(
        restriction_type="licensing",
        restriction_level="commercial-license-required",
        restriction_description="Requires an active commercial license. Annual subscription.",
    ))
    leo_only = graph.add(AccessRestriction(
        restriction_type="licensing",
        restriction_level="law-enforcement-only",
        restriction_description="Only available to sworn law enforcement and authorized government agencies.",
    ))
    opsec_bfu = graph.add(AccessRestriction(
        restriction_type="operational-security",
        restriction_level="covert-capable",
        restriction_description="BFU technique may be detectable. OPSEC review required.",
    ))

    # --- Capabilities ---
    cap_a_alpha = graph.add(ToolCapability(
        tool=tool_a,
        application=app_alpha,
        supports_platform=[android_physical, ios_logical],
        parsed_observable_type=["messages", "contacts", "media files", "call logs"],
        tool_version="8.2.0",
        application_version=["7.0.2"],
        claimed_by_vendor=True,
        verified_by_benchmark=True,
        is_verified=True,
        has_access_restriction=[commercial_license],
    ))

    cap_a_outlook = graph.add(ToolCapability(
        tool=tool_a,
        application=outlook,
        supports_platform=[windows_logical],
        parsed_observable_type=["emails", "contacts", "calendar events", "attachments"],
        tool_version="8.2.0",
        application_version=["Classic", "New (2024)"],
        data_format_version=[".pst", ".nst"],
        claimed_by_vendor=True,
        verified_by_benchmark=True,
        is_verified=True,
        has_access_restriction=[commercial_license],
    ))

    cap_b_alpha = graph.add(ToolCapability(
        tool=tool_b,
        application=app_alpha,
        supports_platform=[android_physical, android_bfu],
        parsed_observable_type=["messages", "contacts"],
        tool_version="7.70",
        application_version=["7.0.2"],
        claimed_by_vendor=True,
        verified_by_benchmark=True,
        is_verified=True,
        has_access_restriction=[leo_only, opsec_bfu],
    ))

    cap_b_outlook = graph.add(ToolCapability(
        tool=tool_b,
        application=outlook,
        supports_platform=[windows_logical],
        parsed_observable_type=["emails", "contacts", "calendar events"],
        tool_version="7.70",
        application_version=["Classic"],
        data_format_version=[".pst"],
        claimed_by_vendor=True,
        verified_by_benchmark=True,
        is_verified=True,
        has_access_restriction=[leo_only],
    ))

    # --- Benchmark Observations ---

    # Tool A / App Alpha — Android physical — pass
    graph.add(BenchmarkObservation(
        capability=cap_a_alpha,
        benchmark_date="2026-03-01T10:00:00Z",
        benchmark_platform=android_physical,
        parse_success=True,
        completeness_score=0.95,
        accuracy_score=0.98,
        false_positive_count=2,
        false_negative_count=12,
        parsed_category=["messages", "contacts", "media files", "call logs"],
        tested_tool_version="8.2.0",
        tested_application_version="7.0.2",
        benchmark_notes="Full physical image from Pixel 8. 12 deleted messages not recovered.",
    ))

    # Tool A / Outlook .pst — pass
    graph.add(BenchmarkObservation(
        capability=cap_a_outlook,
        benchmark_date="2026-03-10T09:00:00Z",
        benchmark_platform=windows_logical,
        parse_success=True,
        completeness_score=0.98,
        accuracy_score=0.99,
        parsed_category=["emails", "contacts", "calendar events", "attachments"],
        tested_tool_version="8.2.0",
        tested_application_version="Classic",
        tested_data_format_version=".pst",
        benchmark_notes="Mature parser. Near-complete recovery from legacy .pst.",
    ))

    # Tool A / Outlook .nst — FAIL
    graph.add(BenchmarkObservation(
        capability=cap_a_outlook,
        benchmark_date="2026-03-15T14:00:00Z",
        benchmark_platform=windows_logical,
        parse_success=False,
        completeness_score=0.0,
        missed_category=["emails", "contacts", "calendar events", "attachments"],
        tested_tool_version="8.2.0",
        tested_application_version="New (2024)",
        tested_data_format_version=".nst",
        benchmark_notes="Cannot recognize .nst format. Vendor plans parser update Q3 2026.",
    ))

    # Tool B / App Alpha — Android physical — pass
    graph.add(BenchmarkObservation(
        capability=cap_b_alpha,
        benchmark_date="2026-02-15T14:30:00Z",
        benchmark_platform=android_physical,
        parse_success=True,
        completeness_score=0.88,
        accuracy_score=0.96,
        false_positive_count=0,
        false_negative_count=28,
        parsed_category=["messages", "contacts"],
        missed_category=["media files"],
        tested_tool_version="7.70",
        tested_application_version="7.0.2",
        benchmark_notes="Messages and contacts recovered. Missed embedded media.",
    ))

    # Tool B / App Alpha — Android BFU — partial
    graph.add(BenchmarkObservation(
        capability=cap_b_alpha,
        benchmark_date="2026-02-20T09:00:00Z",
        benchmark_platform=android_bfu,
        parse_success=True,
        completeness_score=0.35,
        accuracy_score=0.99,
        parsed_category=["contacts"],
        missed_category=["messages", "media files"],
        tested_tool_version="7.70",
        tested_application_version="7.0.2",
        benchmark_notes="BFU: contact DB only. Messages encrypted until first unlock.",
    ))

    # Tool B / Outlook .pst — pass
    graph.add(BenchmarkObservation(
        capability=cap_b_outlook,
        benchmark_date="2026-03-10T09:00:00Z",
        benchmark_platform=windows_logical,
        parse_success=True,
        completeness_score=0.96,
        accuracy_score=0.97,
        parsed_category=["emails", "contacts", "calendar events"],
        tested_tool_version="7.70",
        tested_application_version="Classic",
        tested_data_format_version=".pst",
        benchmark_notes="Solid .pst parser. Slightly lower completeness than Tool A.",
    ))

    # Tool B / Outlook .nst — FAIL
    graph.add(BenchmarkObservation(
        capability=cap_b_outlook,
        benchmark_date="2026-03-10T11:00:00Z",
        benchmark_platform=windows_logical,
        parse_success=False,
        completeness_score=0.0,
        missed_category=["emails", "contacts", "calendar events"],
        tested_tool_version="7.70",
        tested_application_version="New (2024)",
        tested_data_format_version=".nst",
        benchmark_notes="Does not recognize .nst format. No vendor timeline for support.",
    ))

    # --- Matrix ---
    graph.add(CapabilityMatrix(
        matrix_name="DFIR Tool Comparison Q1 2026",
        matrix_version="2.0",
    ))

    print(graph.serialize())


if __name__ == "__main__":
    main()
