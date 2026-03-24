"""Tests for the CASEGraph builder and JSON-LD serialization."""

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco.graph import CASEGraph
from case_uco.uco.tool import Tool, AnalyticTool
from case_uco.uco.tool import BuildInformationType
from case_uco.uco.observable import ObservableObject, ApplicationFacet, DeviceFacet
from case_uco.case.investigation import InvestigativeAction
from case_uco.uco.core import ConfidenceFacet


def test_create_tool():
    graph = CASEGraph()
    tool = graph.create(Tool, name="Magnet AXIOM", version="7.0")
    assert tool.name == "Magnet AXIOM"
    assert tool.version == "7.0"

    output = json.loads(graph.serialize())
    assert "@context" in output
    assert "@graph" in output
    assert len(output["@graph"]) == 1

    obj = output["@graph"][0]
    assert obj["@type"] == "uco-tool:Tool"
    assert "@id" in obj
    assert obj["@id"].startswith("kb:Tool-")
    assert obj["uco-core:name"] == "Magnet AXIOM"
    assert "uco-tool:name" not in obj


def test_create_observable_with_facet():
    graph = CASEGraph()
    _obs = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.tencent.mm")]
    )

    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["@type"] == "uco-observable:ObservableObject"


def test_create_investigative_action():
    graph = CASEGraph()
    _action = graph.create(
        InvestigativeAction,
        name="Parse WeChat data",
    )

    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["@type"] == "case-investigation:InvestigativeAction"


def test_required_field_validation():
    graph = CASEGraph()
    try:
        graph.add(ConfidenceFacet())
        assert False, "Expected ValueError for missing required field"
    except ValueError as exc:
        assert "ConfidenceFacet.confidence" in str(exc)


def test_typed_boolean_literal():
    graph = CASEGraph()
    graph.create(ObservableObject, has_changed=True)
    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["uco-observable:hasChanged"] == {"@type": "xsd:boolean", "@value": "true"}


def test_typed_datetime_literal():
    graph = CASEGraph()
    graph.add(BuildInformationType(compilation_date=datetime(2024, 1, 2, 3, 4, 5)))
    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["uco-tool:compilationDate"]["@type"] == "xsd:dateTime"
    assert obj["uco-tool:compilationDate"]["@value"].startswith("2024-01-02T03:04:05")


def test_inherited_core_property_prefix():
    graph = CASEGraph()
    graph.create(AnalyticTool, name="Analyzer")
    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["uco-core:name"] == "Analyzer"
    assert "uco-tool:name" not in obj


def test_extension_handling():
    @dataclass
    class ToolCapability:
        CLASS_IRI: str = "https://example.org/ontology/toolcap/ToolCapability"
        NAMESPACE_PREFIX: str = "toolcap"
        supported_platform: list[str] = field(
            default_factory=list,
            metadata={
                "jsonld_key": "toolcap:supportedPlatform",
                "required": False,
                "cardinality": "zero_or_more",
                "range_iri": "http://www.w3.org/2001/XMLSchema#string",
                "alternate_range_iris": [],
            },
        )

    graph = CASEGraph(extra_context={"toolcap": "https://example.org/ontology/toolcap/"})
    graph.add(ToolCapability(supported_platform=["Android", "iOS"]))
    output = json.loads(graph.serialize())
    assert output["@context"]["toolcap"] == "https://example.org/ontology/toolcap/"
    assert output["@graph"][0]["@type"] == "toolcap:ToolCapability"
    assert output["@graph"][0]["toolcap:supportedPlatform"] == ["Android", "iOS"]


def test_multiple_objects():
    graph = CASEGraph()

    _axiom = graph.create(Tool, name="Magnet AXIOM")
    _cellebrite = graph.create(Tool, name="Cellebrite Physical Analyzer")
    _wechat = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.tencent.mm")]
    )
    _telegram = graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="org.telegram.messenger")]
    )

    output = json.loads(graph.serialize())
    assert len(output["@graph"]) == 4

    types = [obj["@type"] for obj in output["@graph"]]
    assert types.count("uco-tool:Tool") == 2
    assert types.count("uco-observable:ObservableObject") == 2


def test_context_has_required_prefixes():
    graph = CASEGraph()
    output = json.loads(graph.serialize())
    ctx = output["@context"]
    assert "uco-core" in ctx
    assert "uco-tool" in ctx
    assert "uco-observable" in ctx
    assert "case-investigation" in ctx
    assert "xsd" in ctx
    assert "kb" in ctx


def test_custom_kb_prefix():
    graph = CASEGraph(kb_prefix="http://mylab.example.org/case/")
    output = json.loads(graph.serialize())
    assert output["@context"]["kb"] == "http://mylab.example.org/case/"


def test_device_facet():
    graph = CASEGraph()
    _device = graph.create(
        ObservableObject,
        has_facet=[DeviceFacet(manufacturer="Apple", model="iPhone 15")]
    )

    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["@type"] == "uco-observable:ObservableObject"


def test_analytic_tool_subclass():
    graph = CASEGraph()
    _tool = graph.create(AnalyticTool, name="Custom Analyzer")

    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["@type"] == "uco-tool:AnalyticTool"


def test_serialize_is_valid_json():
    graph = CASEGraph()
    graph.create(Tool, name="Test Tool")
    serialized = graph.serialize()
    parsed = json.loads(serialized)
    assert isinstance(parsed, dict)


def test_unsupported_format_raises():
    graph = CASEGraph()
    try:
        graph.serialize("turtle")
        assert False, "Expected ValueError for unsupported format"
    except ValueError as exc:
        assert "Unsupported format" in str(exc)


def test_get_id():
    graph = CASEGraph()
    tool = graph.create(Tool, name="Test Tool")
    obj_id = graph.get_id(tool)
    assert obj_id is not None
    assert obj_id.startswith("kb:Tool-")
