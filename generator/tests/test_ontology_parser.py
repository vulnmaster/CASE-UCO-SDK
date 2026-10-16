"""Tests for ontology parsing edge cases."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.ontology_parser import parse_ontology


def _write_file(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def test_parse_separate_shacl_shape_and_union(tmp_path: Path) -> None:
    ontology_root = tmp_path / "ontology"

    ttl = """@prefix ex: <https://example.org/uco/test/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.org/uco/test> a owl:Ontology .

ex:Thing a owl:Class ;
    rdfs:label "Thing"@en .

ex:ThingShape a sh:NodeShape ;
    sh:targetClass ex:Thing ;
    sh:property [
        sh:path ex:identifier ;
        sh:minCount "1"^^xsd:integer ;
        sh:or (
            [ sh:datatype xsd:string ]
            [ sh:datatype xsd:anyURI ]
        )
    ] .

ex:identifier a owl:DatatypeProperty ;
    rdfs:comment "Identifier property"@en .
"""

    _write_file(ontology_root / "UCO" / "ontology" / "uco" / "core" / "core.ttl", ttl)
    (ontology_root / "CASE" / "ontology").mkdir(parents=True, exist_ok=True)

    schema = parse_ontology(ontology_root)

    thing = next(cls for cls in schema.classes.values() if cls.name == "Thing")
    assert thing is not None
    assert len(thing.properties) == 1

    prop = thing.properties[0]
    assert prop.name == "identifier"
    assert prop.cardinality.value == "one_or_more"
    assert prop.range_iri == "http://www.w3.org/2001/XMLSchema#string"
    assert prop.alternate_range_iris == ["http://www.w3.org/2001/XMLSchema#anyURI"]
    assert prop.is_union is True


def test_max_count_on_sibling_shape_pins_property_to_scalar(tmp_path: Path) -> None:
    """A sh:maxCount carried by a range-less sibling shape still bounds the property.

    UCO splits many properties this way: one sh:property shape names the
    sh:datatype and leaves the count open, while a sibling shape carries
    sh:maxCount 1 with only sh:nodeKind. Both shapes are conjunctive, so the
    property is single-valued. Mirrors observable:accountType in UCO 1.4.0+.
    """
    ontology_root = tmp_path / "ontology"

    ttl = """@prefix ex: <https://example.org/uco/test/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.org/uco/test> a owl:Ontology .

ex:Thing a owl:Class ;
    rdfs:label "Thing"@en .

ex:ThingShape a sh:NodeShape ;
    sh:targetClass ex:Thing ;
    sh:property [
        sh:datatype xsd:string ;
        sh:message "Datatype advisory, no count bound here." ;
        sh:path ex:accountType ;
        sh:severity sh:Warning ;
    ] ,
    [
        sh:maxCount "1"^^xsd:integer ;
        sh:nodeKind sh:Literal ;
        sh:path ex:accountType ;
    ] ,
    [
        sh:datatype xsd:string ;
        sh:path ex:tag ;
    ] .

ex:accountType a owl:DatatypeProperty ;
    rdfs:comment "Account type property"@en .

ex:tag a owl:DatatypeProperty ;
    rdfs:comment "Unbounded tag property"@en .
"""

    _write_file(ontology_root / "UCO" / "ontology" / "uco" / "core" / "core.ttl", ttl)
    (ontology_root / "CASE" / "ontology").mkdir(parents=True, exist_ok=True)

    schema = parse_ontology(ontology_root)
    thing = next(cls for cls in schema.classes.values() if cls.name == "Thing")
    by_name = {prop.name: prop for prop in thing.properties}

    assert by_name["accountType"].cardinality.value == "zero_or_one"
    assert by_name["accountType"].range_iri == "http://www.w3.org/2001/XMLSchema#string"
    # A property with no bounding sibling stays a list.
    assert by_name["tag"].cardinality.value == "zero_or_more"


def test_subclass_keeps_parent_min_count_and_honors_max_count_zero(tmp_path: Path) -> None:
    """Parent sh:minCount survives a subclass redeclaration (#32); sh:maxCount 0 forbids (#53).

    Mirrors uco-core:Relationship / ObservableRelationship and
    uco-action:Action / ActionLifecycle. Warning-severity maxCount 0 shapes
    (UCO deprecation notices) do not forbid.
    """
    ontology_root = tmp_path / "ontology"
    ttl = """@prefix ex: <https://example.org/uco/test/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.org/uco/test> a owl:Ontology .

ex:Parent a owl:Class , sh:NodeShape ;
    sh:property [ sh:class ex:Parent ; sh:minCount "1"^^xsd:integer ; sh:path ex:source ] ,
        [ sh:datatype xsd:dateTime ; sh:path ex:endTime ] ,
        [ sh:datatype xsd:string ; sh:path ex:version ] ;
    sh:targetClass ex:Parent .

ex:Child a owl:Class , sh:NodeShape ;
    rdfs:subClassOf ex:Parent ;
    sh:property [ sh:class ex:Child ; sh:path ex:source ] ,
        [ sh:maxCount "0"^^xsd:integer ; sh:path ex:endTime ] ,
        [ sh:maxCount "0"^^xsd:integer ; sh:path ex:version ; sh:severity sh:Warning ] ;
    sh:targetClass ex:Child .

ex:Grandchild a owl:Class ;
    rdfs:subClassOf ex:Child .

ex:source a owl:ObjectProperty .
ex:endTime a owl:DatatypeProperty .
ex:version a owl:DatatypeProperty .
"""
    _write_file(ontology_root / "UCO" / "ontology" / "uco" / "core" / "core.ttl", ttl)
    (ontology_root / "CASE" / "ontology").mkdir(parents=True, exist_ok=True)

    schema = parse_ontology(ontology_root)
    by_class = {cls.name: cls for cls in schema.classes.values()}
    child = {p.name: p for p in by_class["Child"].properties}

    assert child["source"].cardinality.is_required
    assert child["source"].cardinality.is_list
    assert child["endTime"].forbidden
    assert "version" not in child or not child["version"].forbidden

    usable = {p.name for p in schema.resolve_all_properties(by_class["Grandchild"])}
    assert "endTime" not in usable
    assert {"source", "version"} <= usable


def test_catalog_extension_is_listed_but_not_registered(tmp_path: Path) -> None:
    import json

    from case_uco_generator.backends.docs_backend import DocsBackend
    from case_uco_generator.mapping_guide import generate_mapping_guide

    ontology_root = tmp_path / "ontology"
    _write_file(
        ontology_root / "UCO" / "ontology" / "uco" / "core" / "core.ttl",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
        "<https://example.org/uco/core> a owl:Ontology .\n",
    )
    (ontology_root / "CASE" / "ontology").mkdir(parents=True, exist_ok=True)

    extensions = tmp_path / "extensions"
    for name, catalog in (("widgets", None), ("tech-catalog", False)):
        manifest = {
            "name": name,
            "display_name": f"{name} display",
            "version": "1.0.0",
            "namespaces": {name: f"https://example.org/{name}/"},
            "owl_files": [f"{name}.ttl"],
        }
        if catalog is not None:
            manifest["class_registry"] = catalog
        _write_file(extensions / name / "manifest.json", json.dumps(manifest))
        _write_file(
            extensions / name / f"{name}.ttl",
            "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
            f"<https://example.org/{name}/Thing{name.title().replace('-', '')}> a owl:Class .\n",
        )

    schema = parse_ontology(ontology_root, extensions_dir=[extensions])

    names = {cls.name for cls in schema.classes.values()}
    assert "ThingWidgets" in names
    assert "ThingTechCatalog" not in names
    assert schema.catalog_extensions == {"tech-catalog": "tech-catalog display"}

    reference = DocsBackend(schema, tmp_path).generate()[0].read_text(encoding="utf-8")
    assert "## Technique Catalogs" in reference
    assert "[`tech-catalog`](extensions/tech-catalog/)" in reference

    guide_path = generate_mapping_guide(schema, tmp_path / "docs" / "MAPPING_GUIDE.md")
    guide = Path(guide_path).read_text(encoding="utf-8")
    assert "[`tech-catalog`](../extensions/tech-catalog/)" in guide


def test_private_extension_is_neither_registered_nor_listed(tmp_path: Path) -> None:
    import json

    from case_uco_generator.backends.docs_backend import DocsBackend

    ontology_root = tmp_path / "ontology"
    _write_file(
        ontology_root / "UCO" / "ontology" / "uco" / "core" / "core.ttl",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
        "<https://example.org/uco/core> a owl:Ontology .\n",
    )
    (ontology_root / "CASE" / "ontology").mkdir(parents=True, exist_ok=True)

    extensions = tmp_path / "extensions"
    for name, distribution in (("widgets", None), ("inhouse", "private")):
        manifest = {
            "name": name,
            "display_name": f"{name} display",
            "version": "1.0.0",
            "namespaces": {name: f"https://example.org/{name}/"},
            "owl_files": [f"{name}.ttl"],
        }
        if distribution is not None:
            manifest["distribution"] = distribution
        _write_file(extensions / name / "manifest.json", json.dumps(manifest))
        _write_file(
            extensions / name / f"{name}.ttl",
            "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
            f"<https://example.org/{name}/Thing{name.title()}> a owl:Class .\n",
        )

    schema = parse_ontology(ontology_root, extensions_dir=[extensions])

    names = {cls.name for cls in schema.classes.values()}
    assert "ThingWidgets" in names
    assert "ThingInhouse" not in names
    assert schema.catalog_extensions == {}
    reference = DocsBackend(schema, tmp_path).generate()[0].read_text(encoding="utf-8")
    assert "inhouse" not in reference

    own = parse_ontology(
        ontology_root, extensions_dir=[extensions], include_private=frozenset({"inhouse"})
    )
    assert "ThingInhouse" in {cls.name for cls in own.classes.values()}


def test_shape_in_nested_namespace_is_the_classs_own(tmp_path: Path) -> None:
    """A shape kept in a sub-namespace of its class (SOLVE-IT's ``.../observable/shapes/``)
    defines the class's properties; a profile from an unrelated namespace still does not."""
    ontology_root = tmp_path / "ontology"

    ttl = """@prefix ex: <https://example.org/uco/test/> .
@prefix exshapes: <https://example.org/uco/test/shapes/> .
@prefix profile: <https://example.org/profile/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

<https://example.org/uco/test> a owl:Ontology .

ex:Set a owl:Class ;
    rdfs:label "Set"@en .

ex:Member a owl:Class .

ex:hasMember a owl:ObjectProperty .
ex:profileOnly a owl:ObjectProperty .

exshapes:SetShape a sh:NodeShape ;
    sh:targetClass ex:Set ;
    sh:property [
        sh:path ex:hasMember ;
        sh:class ex:Member
    ] .

profile:SetProfileShape a sh:NodeShape ;
    sh:targetClass ex:Set ;
    sh:property [
        sh:path ex:profileOnly ;
        sh:class ex:Member
    ] .
"""

    _write_file(ontology_root / "UCO" / "ontology" / "uco" / "core" / "core.ttl", ttl)
    (ontology_root / "CASE" / "ontology").mkdir(parents=True, exist_ok=True)

    schema = parse_ontology(ontology_root)

    set_class = next(cls for cls in schema.classes.values() if cls.name == "Set")
    assert [prop.name for prop in set_class.properties] == ["hasMember"]
    assert set_class.properties[0].range_iri == "https://example.org/uco/test/Member"
