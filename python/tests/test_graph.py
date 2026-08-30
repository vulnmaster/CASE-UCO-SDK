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
from case_uco.uco.core import ConfidenceFacet, ExternalReference


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


def test_hex_binary_literal_is_canonical_uppercase():
    """hashlib.hexdigest() is lowercase; XSD canonical hexBinary is uppercase.

    SPARQL joins compare literals as terms, so a lowercase digest will not
    join to the same digest written uppercase by another producer.
    """
    from case_uco.uco.observable import ContentDataFacet
    from case_uco.uco.types import Hash

    digest = "d747a7183ed4cfc29e68781469adcd43098fa319e6093ed3da416f20fe6c2178"
    graph = CASEGraph()
    graph.create(
        ObservableObject,
        has_facet=[ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value=digest)])],
    )
    serialized = graph.serialize()
    assert digest.upper() in serialized
    assert digest not in serialized


def test_non_hex_value_is_not_uppercased():
    """A value that is not valid hexBinary is passed through, not mangled."""
    from case_uco.uco.observable import ContentDataFacet
    from case_uco.uco.types import Hash

    graph = CASEGraph()
    graph.create(
        ObservableObject,
        has_facet=[ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="not-a-hash")])],
    )
    assert "not-a-hash" in graph.serialize()


def test_typed_anyuri_literal():
    graph = CASEGraph()
    graph.create(
        ObservableObject,
        external_reference=[
            ExternalReference(reference_url="https://example.org/ncmec/series/1")
        ],
    )
    output = json.loads(graph.serialize())
    obj = output["@graph"][0]
    ref = obj["uco-core:externalReference"]
    if isinstance(ref, list):
        ref = ref[0]
    assert ref["uco-core:referenceURL"] == {
        "@type": "xsd:anyURI",
        "@value": "https://example.org/ncmec/series/1",
    }


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
    graph.create(Tool, name="Tool A")
    graph.create(InvestigativeAction, name="Action A")
    graph.create(ObservableObject, has_changed=True,
                 has_facet=[ApplicationFacet(application_identifier="com.app")])

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
    graph.create(Tool, name="Tool A")
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
    """Verify Python DEFAULT_CONTEXT has all standard UCO/CASE prefixes."""
    from case_uco.graph import DEFAULT_CONTEXT
    expected = [
        "case-investigation", "uco-core", "uco-tool", "uco-observable",
        "uco-action", "uco-identity", "uco-location", "uco-types",
        "uco-vocabulary", "uco-role", "uco-victim", "uco-analysis",
        "uco-configuration", "uco-marking", "uco-pattern", "uco-time", "xsd",
    ]
    for prefix in expected:
        assert prefix in DEFAULT_CONTEXT, f"missing context prefix: {prefix}"


def test_context_pruning_only_used_prefixes():
    """Serialized context should only contain prefixes actually used in @graph."""
    graph = CASEGraph()
    graph.create(Tool, name="Tool A", version="1.0")

    output = json.loads(graph.serialize())
    ctx = output["@context"]
    assert "kb" in ctx
    assert "uco-tool" in ctx
    assert "uco-core" in ctx

    for prefix in ["uco-identity", "uco-location", "uco-role", "uco-victim",
                    "uco-configuration", "uco-marking", "uco-pattern", "uco-time"]:
        assert prefix not in ctx, f"unused prefix should be pruned: {prefix}"


def test_context_pruning_empty_graph():
    """An empty graph should have no context entries."""
    graph = CASEGraph()
    output = json.loads(graph.serialize())
    assert output["@context"] == {}


def test_context_pruning_preserves_extension_prefix():
    """User-added extension prefixes should be preserved when used."""
    graph = CASEGraph(extra_context={"myext": "http://example.org/ext/"})
    graph.load(json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{"@id": "kb:Foo-1", "@type": "myext:Foo", "myext:bar": "baz"}],
    }))
    output = json.loads(graph.serialize())
    assert "myext" in output["@context"]


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
        assert "myext" in chunk._context


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


# --- from_jsonld tests ---

def test_from_jsonld_basic():
    graph = CASEGraph()
    graph.create(Tool, name="Round Trip Tool", version="2.0")
    json_str = graph.serialize()

    graph2, objects = CASEGraph.from_jsonld(json_str)
    assert len(graph2) == 1
    assert len(objects) == 1
    assert isinstance(objects[0], Tool)
    assert objects[0].name == "Round Trip Tool"
    assert objects[0].version == "2.0"


def test_from_jsonld_multiple_types():
    graph = CASEGraph()
    graph.create(Tool, name="T1")
    graph.create(AnalyticTool, name="AT1")
    json_str = graph.serialize()

    graph2, objects = CASEGraph.from_jsonld(json_str)
    assert len(objects) == 2
    types = {type(o).__name__ for o in objects}
    assert "Tool" in types
    assert "AnalyticTool" in types


def test_from_jsonld_unknown_type():
    json_str = json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [
            {"@id": "kb:Unknown-1", "@type": "http://example.org/unknown/FooBar"},
        ],
    })
    graph2, objects = CASEGraph.from_jsonld(json_str)
    assert len(objects) == 1
    assert isinstance(objects[0], dict)


def test_from_jsonld_preserves_ids():
    json_str = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [
            {
                "@id": "kb:Tool-stable-id",
                "@type": "uco-tool:Tool",
                "uco-core:name": "Stable Tool",
            },
        ],
    })
    graph2, objects = CASEGraph.from_jsonld(json_str)
    assert isinstance(objects[0], Tool)
    assert graph2.get_id(objects[0]) == "kb:Tool-stable-id"


def test_from_jsonld_typed_literals():
    json_str = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [
            {
                "@id": "kb:Tool-lit-1",
                "@type": "uco-tool:Tool",
                "uco-core:name": "Literal Test",
                "uco-tool:version": "3.0",
            },
        ],
    })
    graph2, objects = CASEGraph.from_jsonld(json_str)
    assert isinstance(objects[0], Tool)
    assert objects[0].version == "3.0"


def test_from_jsonld_extra_classes():
    @dataclass
    class CustomExt:
        CLASS_IRI: str = "http://example.org/ext/Custom"
        NAMESPACE_PREFIX: str = "ext"
        value: str = field(default="", metadata={
            "jsonld_key": "ext:value",
            "required": False, "cardinality": "zero_or_one",
            "range_iri": "http://www.w3.org/2001/XMLSchema#string",
            "alternate_range_iris": [],
        })

    json_str = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "ext": "http://example.org/ext/",
        },
        "@graph": [
            {"@id": "kb:Custom-1", "@type": "ext:Custom", "ext:value": "hello"},
        ],
    })
    graph2, objects = CASEGraph.from_jsonld(json_str, extra_classes=[CustomExt])
    assert isinstance(objects[0], CustomExt)
    assert objects[0].value == "hello"


def test_from_jsonld_roundtrip_context():
    """Unused extra context prefixes are pruned during serialization."""
    graph = CASEGraph(
        kb_prefix="http://mylab.example.org/kb/",
        extra_context={"myext": "http://example.org/myext/"},
    )
    graph.create(Tool, name="Context Test")
    json_str = graph.serialize()

    output = json.loads(json_str)
    assert "myext" not in output["@context"], "unused prefix should be pruned"
    assert "uco-tool" in output["@context"]


# --- validate tests ---

def test_validate_raises_when_case_validate_missing(monkeypatch):
    import shutil
    monkeypatch.setattr(shutil, "which", lambda _name: None)

    graph = CASEGraph()
    graph.create(Tool, name="Tool A")
    try:
        graph.validate()
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert "case_validate not found" in str(exc)
