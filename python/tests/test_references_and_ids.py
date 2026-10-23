"""Node references by IRI, deterministic IDs, Facet ownership, and vocabularies."""

import json
from pathlib import Path

import pytest
from rdflib import BNode, URIRef

from case_uco import CASEGraph, Ref, SharedFacetError, deterministic_id, deterministic_uuid
from case_uco.uco import observable
from case_uco.uco.identity import Organization
from case_uco.uco.observable import (
    ContentDataFacet,
    DeviceFacet,
    File,
    FileFacet,
    ObservableObject,
)
from case_uco.uco.types import Hash
from case_uco.uco.vocabulary import VOCABULARIES, HashNameVocab

REGISTRY = json.loads(
    (Path(__file__).resolve().parents[1] / "case_uco" / "_registry.json").read_text()
)


def _nodes(graph):
    return json.loads(graph.serialize())["@graph"]


def _manufacturer(graph):
    return _nodes(graph)[0]["uco-core:hasFacet"][0]["uco-observable:manufacturer"]


def test_ref_with_compact_iri_serializes_as_node_reference():
    graph = CASEGraph()
    graph.create(ObservableObject, has_facet=[DeviceFacet(manufacturer=Ref("kb:Organization-1"))])
    assert _manufacturer(graph) == {"@id": "kb:Organization-1"}


def test_ref_with_absolute_iri_is_compacted():
    graph = CASEGraph()
    graph.create(
        ObservableObject,
        has_facet=[DeviceFacet(manufacturer=Ref("http://example.org/kb/Organization-1"))],
    )
    assert _manufacturer(graph) == {"@id": "kb:Organization-1"}


def test_rdflib_uriref_serializes_as_node_reference():
    graph = CASEGraph()
    graph.create(
        ObservableObject,
        has_facet=[DeviceFacet(manufacturer=URIRef("http://example.org/kb/Organization-2"))],
    )
    assert _manufacturer(graph) == {"@id": "kb:Organization-2"}


def test_rdflib_bnode_serializes_as_blank_node_reference():
    graph = CASEGraph()
    graph.create(ObservableObject, has_facet=[DeviceFacet(manufacturer=BNode("org1"))])
    assert _manufacturer(graph) == {"@id": "_:org1"}


def test_plain_string_on_node_valued_property_is_rejected():
    graph = CASEGraph()
    with pytest.raises(TypeError, match=r"case_uco\.Ref"):
        graph.create(ObservableObject, has_facet=[DeviceFacet(manufacturer="Apple")])
    assert len(graph) == 0


def test_plain_string_on_literal_property_is_unchanged():
    graph = CASEGraph()
    graph.create(File, has_facet=[FileFacet(file_name="kb:not-a-reference")])
    facet = _nodes(graph)[0]["uco-core:hasFacet"][0]
    assert facet["uco-observable:fileName"] == "kb:not-a-reference"


def test_instance_reference_still_uses_graph_id():
    graph = CASEGraph()
    org = graph.create(Organization, name="Google")
    graph.create(ObservableObject, has_facet=[DeviceFacet(manufacturer=org)])
    node = _nodes(graph)[1]
    assert node["uco-core:hasFacet"][0]["uco-observable:manufacturer"] == {
        "@id": graph.get_id(org)
    }


def test_deterministic_id_is_stable_and_uuid_shaped():
    a = deterministic_id(File, "SHA256", "AB" * 32)
    b = deterministic_id("File", "SHA256", "AB" * 32)
    assert a == b
    assert a.startswith("kb:File-")
    assert len(a.split("File-", 1)[1]) == 36


def test_deterministic_id_includes_class_name():
    assert deterministic_id("File", "x") != deterministic_id("ContentData", "x")


def test_deterministic_uuid_parts_are_unambiguous():
    assert deterministic_uuid("a|b", "c") != deterministic_uuid("a", "b|c")
    assert deterministic_uuid("ab", "c") != deterministic_uuid("a", "bc")


def test_deterministic_uuid_requires_parts():
    with pytest.raises(ValueError):
        deterministic_uuid()


def _content_file(graph, node_id):
    return graph.create(
        File,
        id=node_id,
        has_facet=[
            FileFacet(file_name="photo.jpg", size_in_bytes=4096),
            ContentDataFacet(
                hash=[Hash(hash_method=HashNameVocab.MD5, hash_value="0" * 32)]
            ),
        ],
    )


def test_inline_facets_are_deterministic_under_a_deterministic_owner():
    node_id = deterministic_id(File, "MD5", "0" * 32)
    first, second = CASEGraph(), CASEGraph()
    _content_file(first, node_id)
    _content_file(second, node_id)
    assert first.serialize() == second.serialize()


def test_owners_with_identical_facet_values_get_distinct_facets():
    graph = CASEGraph()
    _content_file(graph, deterministic_id(File, "MD5", "0" * 32))
    _content_file(graph, deterministic_id(File, "SHA1", "0" * 40))
    facet_ids = [
        f["@id"] for n in _nodes(graph) for f in n["uco-core:hasFacet"]
    ]
    assert len(facet_ids) == len(set(facet_ids)) == 4


def test_reruns_merge_identically_on_load():
    node_id = deterministic_id(File, "MD5", "0" * 32)
    first, second = CASEGraph(), CASEGraph()
    _content_file(first, node_id)
    _content_file(second, node_id)
    first.load(second.serialize(), on_duplicate="merge_identical")
    assert len(first) == 1


def test_inline_facet_ids_do_not_depend_on_facet_order():
    node_id = deterministic_id(File, "x")
    a, b = CASEGraph(), CASEGraph()
    a.create(File, id=node_id, has_facet=[FileFacet(file_name="x"), ContentDataFacet(size_in_bytes=1)])
    b.create(File, id=node_id, has_facet=[ContentDataFacet(size_in_bytes=1), FileFacet(file_name="x")])
    ids_a = sorted(f["@id"] for f in _nodes(a)[0]["uco-core:hasFacet"])
    ids_b = sorted(f["@id"] for f in _nodes(b)[0]["uco-core:hasFacet"])
    assert ids_a == ids_b


def _report_view(hashes, size=1024):
    graph = CASEGraph()
    graph.create(
        File,
        id=deterministic_id(File, "exhibit-1", "/DCIM/photo.jpg"),
        has_facet=[
            FileFacet(file_path="/DCIM/photo.jpg", size_in_bytes=size),
            ContentDataFacet(hash=[Hash(hash_method=m, hash_value=v) for m, v in hashes]),
        ],
    )
    return graph


def _hash_methods(graph):
    node = _nodes(graph)[0]
    facet = next(f for f in node["uco-core:hasFacet"] if "ContentDataFacet" in f["@type"])
    return sorted(h["uco-types:hashMethod"] for h in facet["uco-observable:hash"])


def test_merge_compatible_unions_embedded_facets_with_one_id():
    first = _report_view([("MD5", "0" * 32), ("SHA256", "A" * 64)])
    second = _report_view([("MD5", "0" * 32), ("SHA1", "B" * 40)])
    first.load(second.serialize(), on_duplicate="merge_compatible")
    assert len(first) == 1
    assert _hash_methods(first) == ["MD5", "SHA1", "SHA256"]


def test_merge_identical_detects_differing_embedded_facets():
    from case_uco import DuplicateNodeError

    first = _report_view([("MD5", "0" * 32)])
    second = _report_view([("MD5", "0" * 32), ("SHA1", "B" * 40)])
    with pytest.raises(DuplicateNodeError):
        first.load(second.serialize(), on_duplicate="merge_identical")


def test_merge_compatible_still_rejects_conflicting_embedded_scalars():
    from case_uco import DuplicateNodeError

    first = _report_view([("MD5", "0" * 32)], size=1024)
    second = _report_view([("MD5", "0" * 32)], size=2048)
    with pytest.raises(DuplicateNodeError):
        first.load(second.serialize(), on_duplicate="merge_compatible")


def test_reusing_a_facet_instance_on_two_objects_is_rejected():
    graph = CASEGraph()
    shared = graph.create(FileFacet, file_name="shared.bin")
    graph.create(File, has_facet=[shared])
    with pytest.raises(SharedFacetError, match="inverse-functional"):
        graph.create(File, has_facet=[shared])
    assert len(graph) == 2


def test_shared_facet_by_reference_is_rejected():
    graph = CASEGraph()
    facet = graph.create(FileFacet, id="kb:FileFacet-1", file_name="shared.bin")
    graph.create(File, id="kb:File-1", has_facet=[facet])
    with pytest.raises(SharedFacetError):
        graph.create(File, id="kb:File-2", has_facet=[Ref("kb:FileFacet-1")])


def test_shared_facet_through_add_property_is_rejected():
    graph = CASEGraph()
    graph.upsert_node("kb:File-1", types="uco-observable:File",
                      properties={"uco-core:hasFacet": [{"@id": "kb:FileFacet-1"}]})
    graph.upsert_node("kb:File-2", types="uco-observable:File")
    with pytest.raises(SharedFacetError):
        graph.add_property("kb:File-2", "uco-core:hasFacet", {"@id": "kb:FileFacet-1"})


def test_shared_facet_across_loaded_documents_is_rejected():
    graph = CASEGraph()
    graph.load(json.dumps({"@graph": [
        {"@id": "kb:File-1", "@type": "uco-observable:File",
         "uco-core:hasFacet": [{"@id": "kb:FileFacet-1"}]},
    ]}))
    with pytest.raises(SharedFacetError):
        graph.load(json.dumps({"@graph": [
            {"@id": "kb:File-2", "@type": "uco-observable:File",
             "uco-core:hasFacet": [{"@id": "http://example.org/kb/FileFacet-1"}]},
        ]}))


def test_same_owner_may_restate_its_facet():
    graph = CASEGraph()
    doc = json.dumps({"@graph": [
        {"@id": "kb:File-1", "@type": "uco-observable:File",
         "uco-core:hasFacet": [{"@id": "kb:FileFacet-1"}]},
    ]})
    graph.load(doc)
    graph.load(doc, on_duplicate="merge_identical")
    assert len(graph) == 1


def test_vocabulary_namespace_covers_every_uco_vocabulary():
    uco = {
        name for name, v in REGISTRY["vocabs"].items()
        if "ontology.unifiedcyberontology.org/uco/" in v["iri"]
    }
    assert set(VOCABULARIES) == uco
    for name, vocab in VOCABULARIES.items():
        assert vocab.IRI == REGISTRY["vocabs"][name]["iri"]
        assert vocab.MEMBERS == frozenset(REGISTRY["vocabs"][name]["members"])


def test_case_vocabulary_namespace():
    from case_uco.case.vocabulary import VOCABULARIES as CASE_VOCABULARIES
    from case_uco.case.vocabulary import InvestigationFormVocab

    assert "InvestigationFormVocab" in CASE_VOCABULARIES
    assert InvestigationFormVocab.CASE == "case"


def test_module_vocabularies_are_the_vocabulary_namespace_classes():
    from case_uco.uco import vocabulary

    assert observable.WhoisDNSSECTypeVocab is vocabulary.WhoisDNSSECTypeVocab


def test_vocabulary_members_serialize_as_plain_strings():
    graph = CASEGraph()
    graph.create(File, has_facet=[ContentDataFacet(
        hash=[Hash(hash_method=HashNameVocab.SHA256, hash_value="AB" * 32)]
    )])
    hash_node = _nodes(graph)[0]["uco-core:hasFacet"][0]["uco-observable:hash"][0]
    assert hash_node["uco-types:hashMethod"] == "SHA256"
