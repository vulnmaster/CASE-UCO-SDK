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
    tool = graph.create(Tool, name="Tool A", version="7.0")
    assert tool.name == "Tool A"
    assert tool.version == "7.0"

    output = json.loads(graph.serialize())
    assert "@context" in output
    assert "@graph" in output
    assert len(output["@graph"]) == 1

    obj = output["@graph"][0]
    assert obj["@type"] == "uco-tool:Tool"
    assert "@id" in obj
    assert obj["@id"].startswith("kb:Tool-")
    assert obj["uco-core:name"] == "Tool A"
    assert "uco-tool:name" not in obj


def test_create_observable_with_facet():
    graph = CASEGraph()
    graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.example.app.alpha")]
    )

    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["@type"] == "uco-observable:ObservableObject"


def test_create_investigative_action():
    graph = CASEGraph()
    graph.create(
        InvestigativeAction,
        name="Parse application data",
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
        CLASS_IRI: str = "http://example.org/ontology/toolcap/ToolCapability"
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

    graph = CASEGraph(extra_context={"toolcap": "http://example.org/ontology/toolcap/"})
    graph.add(ToolCapability(supported_platform=["Android", "iOS"]))
    output = json.loads(graph.serialize())
    assert output["@context"]["toolcap"] == "http://example.org/ontology/toolcap/"
    assert output["@graph"][0]["@type"] == "toolcap:ToolCapability"
    assert output["@graph"][0]["toolcap:supportedPlatform"] == ["Android", "iOS"]


def test_multiple_objects():
    graph = CASEGraph()

    graph.create(Tool, name="Tool A")
    graph.create(Tool, name="Tool B")
    graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.example.app.alpha")]
    )
    graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.example.app.beta")]
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
    graph.create(
        ObservableObject,
        has_facet=[DeviceFacet(manufacturer="Apple", model="iPhone 15")]
    )

    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    assert obj["@type"] == "uco-observable:ObservableObject"


def test_analytic_tool_subclass():
    graph = CASEGraph()
    graph.create(AnalyticTool, name="Custom Analyzer")

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


def test_create_with_custom_id():
    graph = CASEGraph()
    tool = graph.create(Tool, id="kb:Tool-my-stable-id", name="Tool A")
    obj_id = graph.get_id(tool)
    assert obj_id == "kb:Tool-my-stable-id"

    output = json.loads(graph.serialize())
    assert output["@graph"][0]["@id"] == "kb:Tool-my-stable-id"


def test_add_with_custom_id():
    graph = CASEGraph()
    tool = Tool(name="Tool B")
    returned_id = graph.add(tool, id="kb:Tool-b-001")
    assert returned_id == "kb:Tool-b-001"
    assert graph.get_id(tool) == "kb:Tool-b-001"


def test_len():
    graph = CASEGraph()
    assert len(graph) == 0
    graph.create(Tool, name="Tool A")
    assert len(graph) == 1
    graph.create(Tool, name="Tool B")
    assert len(graph) == 2


def test_load_json_ld():
    graph = CASEGraph()
    json_ld = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
        },
        "@graph": [
            {
                "@id": "kb:Tool-existing-001",
                "@type": "uco-tool:Tool",
                "uco-core:name": "Pre-existing Tool",
            }
        ],
    })
    graph.load(json_ld)
    assert len(graph) == 1

    output = json.loads(graph.serialize())
    assert output["@graph"][0]["@id"] == "kb:Tool-existing-001"
    assert output["@graph"][0]["uco-core:name"] == "Pre-existing Tool"


def test_load_then_add():
    graph = CASEGraph()
    graph.load(json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{"@id": "kb:Tool-loaded", "@type": "uco-tool:Tool"}],
    }))
    graph.create(Tool, name="New Tool")
    assert len(graph) == 2


def test_context_parity_all_prefixes():
    """Verify Python context has all standard UCO/CASE prefixes."""
    graph = CASEGraph()
    output = json.loads(graph.serialize())
    ctx = output["@context"]
    expected = [
        "case-investigation", "uco-core", "uco-tool", "uco-observable",
        "uco-action", "uco-identity", "uco-location", "uco-types",
        "uco-vocabulary", "uco-role", "uco-victim", "uco-analysis",
        "uco-configuration", "uco-marking", "uco-pattern", "uco-time", "xsd",
    ]
    for prefix in expected:
        assert prefix in ctx, f"missing context prefix: {prefix}"


def test_estimate_triples_empty():
    graph = CASEGraph()
    assert graph.estimate_triples() == 0


def test_estimate_triples_single_object():
    graph = CASEGraph()
    graph.create(Tool, name="Tool A", version="1.0")
    triples = graph.estimate_triples()
    # @type (1) + name (1) + version (1) = 3 minimum
    assert triples >= 3


def test_estimate_triples_with_facets():
    graph = CASEGraph()
    graph.create(
        ObservableObject,
        has_facet=[ApplicationFacet(application_identifier="com.example.app")],
    )
    triples = graph.estimate_triples()
    # Should be more than a simple object due to nested facets
    assert triples >= 4


def test_estimate_triples_multiple_objects():
    graph = CASEGraph()
    graph.create(Tool, name="Tool A")
    graph.create(Tool, name="Tool B")
    single = CASEGraph()
    single.create(Tool, name="Tool A")
    assert graph.estimate_triples() > single.estimate_triples()


def test_split_basic():
    graph = CASEGraph()
    for i in range(25):
        graph.create(Tool, name=f"Tool {i}")
    assert len(graph) == 25

    chunks = graph.split(max_objects=10)
    assert len(chunks) == 3
    assert len(chunks[0]) == 10
    assert len(chunks[1]) == 10
    assert len(chunks[2]) == 5


def test_split_preserves_context():
    graph = CASEGraph(
        kb_prefix="http://example.org/test/",
        extra_context={"myext": "http://example.org/ext/"},
    )
    graph.create(Tool, name="T1")
    graph.create(Tool, name="T2")

    chunks = graph.split(max_objects=1)
    assert len(chunks) == 2
    for chunk in chunks:
        ctx = json.loads(chunk.serialize())["@context"]
        assert ctx["kb"] == "http://example.org/test/"
        assert "myext" in ctx


def test_split_single_chunk():
    graph = CASEGraph()
    graph.create(Tool, name="Only")
    chunks = graph.split(max_objects=100)
    assert len(chunks) == 1
    assert len(chunks[0]) == 1


def test_merge_files(tmp_path):
    g1 = CASEGraph()
    g1.create(Tool, name="Tool A")
    g1.write(str(tmp_path / "g1.jsonld"))

    g2 = CASEGraph()
    g2.create(Tool, name="Tool B")
    g2.create(Tool, name="Tool C")
    g2.write(str(tmp_path / "g2.jsonld"))

    merged = CASEGraph.merge_files([
        str(tmp_path / "g1.jsonld"),
        str(tmp_path / "g2.jsonld"),
    ])
    assert len(merged) == 3


def test_split_then_merge_roundtrip(tmp_path):
    graph = CASEGraph()
    for i in range(20):
        graph.create(Tool, name=f"Tool {i}")
    original_count = len(graph)

    chunks = graph.split(max_objects=7)
    paths = []
    for i, chunk in enumerate(chunks):
        p = str(tmp_path / f"chunk-{i}.jsonld")
        chunk.write(p)
        paths.append(p)

    merged = CASEGraph.merge_files(paths)
    assert len(merged) == original_count
