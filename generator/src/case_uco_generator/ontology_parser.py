"""Parse UCO/CASE OWL+SHACL Turtle files and extract a typed schema model."""

from __future__ import annotations

import logging
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from case_uco_generator.schema_model import (
    Cardinality,
    OntologyClass,
    OntologyProperty,
    OntologySchema,
    OntologyVocab,
    iri_local_name,
    iri_namespace,
)

logger = logging.getLogger(__name__)

SH = Namespace("http://www.w3.org/ns/shacl#")

UCO_CORE = "https://ontology.unifiedcyberontology.org/uco/core/"
CASE_INVESTIGATION = "https://ontology.caseontology.org/case/investigation/"

FACET_IRI = UCO_CORE + "Facet"

# Namespace prefix -> ontology module name mapping
PREFIX_TO_MODULE: dict[str, tuple[str, str]] = {
    "https://ontology.unifiedcyberontology.org/uco/core/": ("uco", "core"),
    "https://ontology.unifiedcyberontology.org/uco/action/": ("uco", "action"),
    "https://ontology.unifiedcyberontology.org/uco/analysis/": ("uco", "analysis"),
    "https://ontology.unifiedcyberontology.org/uco/configuration/": ("uco", "configuration"),
    "https://ontology.unifiedcyberontology.org/uco/identity/": ("uco", "identity"),
    "https://ontology.unifiedcyberontology.org/uco/location/": ("uco", "location"),
    "https://ontology.unifiedcyberontology.org/uco/marking/": ("uco", "marking"),
    "https://ontology.unifiedcyberontology.org/uco/observable/": ("uco", "observable"),
    "https://ontology.unifiedcyberontology.org/uco/pattern/": ("uco", "pattern"),
    "https://ontology.unifiedcyberontology.org/uco/role/": ("uco", "role"),
    "https://ontology.unifiedcyberontology.org/uco/time/": ("uco", "time"),
    "https://ontology.unifiedcyberontology.org/uco/tool/": ("uco", "tool"),
    "https://ontology.unifiedcyberontology.org/uco/types/": ("uco", "types"),
    "https://ontology.unifiedcyberontology.org/uco/victim/": ("uco", "victim"),
    "https://ontology.unifiedcyberontology.org/uco/vocabulary/": ("uco", "vocabulary"),
    "https://ontology.caseontology.org/case/investigation/": ("case", "investigation"),
    "https://ontology.caseontology.org/case/vocabulary/": ("case", "vocabulary"),
}

# SPARQL: Select all OWL classes that have one or more SHACL NodeShapes targeting them.
CLASSES_QUERY = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT DISTINCT ?class ?shape ?label ?comment ?parent WHERE {
    ?class a owl:Class .
    ?shape a sh:NodeShape .
    ?shape sh:targetClass ?class .
    OPTIONAL { ?class rdfs:label ?label . }
    OPTIONAL { ?class rdfs:comment ?comment . }
    OPTIONAL { ?class rdfs:subClassOf ?parent .
               ?parent a owl:Class .
               FILTER(!isBlank(?parent))
    }
}
ORDER BY ?class
"""

# SPARQL: Select vocabulary/enum types (rdfs:Datatype with owl:oneOf)
VOCABS_QUERY = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?vocab ?label WHERE {
    ?vocab a rdfs:Datatype .
    OPTIONAL { ?vocab rdfs:label ?label . }
    ?vocab owl:equivalentClass ?equiv .
    ?equiv owl:oneOf ?list .
}
ORDER BY ?vocab
"""


def load_ontology(ontology_root: Path) -> Graph:
    """Load all UCO and CASE Turtle files into a single RDFLib graph."""
    g = Graph()

    uco_dir = ontology_root / "UCO" / "ontology" / "uco"
    case_dir = ontology_root / "CASE" / "ontology"

    ttl_count = 0
    for ttl_dir in [uco_dir, case_dir]:
        if not ttl_dir.exists():
            logger.warning("Ontology directory not found: %s", ttl_dir)
            continue
        for ttl_file in ttl_dir.rglob("*.ttl"):
            try:
                g.parse(str(ttl_file), format="turtle")
                ttl_count += 1
            except Exception as e:
                logger.warning("Failed to parse %s: %s", ttl_file, e)

    # Also load the CO ontology if present
    co_dir = ontology_root / "UCO" / "ontology" / "co"
    if co_dir.exists():
        for ttl_file in co_dir.rglob("*.ttl"):
            try:
                g.parse(str(ttl_file), format="turtle")
                ttl_count += 1
            except Exception as e:
                logger.warning("Failed to parse %s: %s", ttl_file, e)

    logger.info("Loaded %d Turtle files, %d triples total", ttl_count, len(g))
    return g


def _classify_module(
    iri: str,
    extra_modules: dict[str, tuple[str, str]] | None = None,
) -> tuple[str, str]:
    """Map a class IRI to (top-level, module) based on namespace."""
    ns = iri_namespace(iri)
    if ns in PREFIX_TO_MODULE:
        return PREFIX_TO_MODULE[ns]
    if extra_modules and ns in extra_modules:
        return extra_modules[ns]
    if iri.startswith("https://ontology.caseontology.org/"):
        return ("case", "investigation")
    return ("uco", "core")


def _is_subclass_of(g: Graph, cls_iri: str, ancestor_iri: str) -> bool:
    """Check if cls_iri is (transitively) a subclass of ancestor_iri."""
    visited: set[str] = set()
    stack = [cls_iri]
    while stack:
        current = stack.pop()
        if current == ancestor_iri:
            return True
        if current in visited:
            continue
        visited.add(current)
        for parent in g.objects(URIRef(current), RDFS.subClassOf):
            if isinstance(parent, URIRef):
                stack.append(str(parent))
    return False


def _walk_rdf_list(g: Graph, head) -> list:
    """Walk an RDF list and return all members."""
    values: list = []
    current = head
    while current and str(current) != str(RDF.nil):
        first = g.value(current, RDF.first)
        if first is not None:
            values.append(first)
        current = g.value(current, RDF.rest)
    return values


def _cardinality_from_range(min_count: int, max_count: int | None) -> Cardinality:
    return Cardinality.from_counts(min_count if min_count > 0 else None, max_count)


def _merge_cardinality(left: Cardinality, right: Cardinality) -> Cardinality:
    required = left.is_required or right.is_required
    is_list = left.is_list or right.is_list
    if required and is_list:
        return Cardinality.ONE_OR_MORE
    if required:
        return Cardinality.EXACTLY_ONE
    if is_list:
        return Cardinality.ZERO_OR_MORE
    return Cardinality.ZERO_OR_ONE


def _extract_property_from_shape(g: Graph, prop_shape) -> OntologyProperty | None:
    """Extract one property definition from a SHACL property shape node."""
    path = g.value(prop_shape, SH.path)
    if not isinstance(path, URIRef):
        return None

    min_raw = g.value(prop_shape, SH.minCount)
    max_raw = g.value(prop_shape, SH.maxCount)
    min_count = int(min_raw) if min_raw else 0
    max_count = int(max_raw) if max_raw else None

    range_iris: list[str] = []
    range_is_class_map: dict[str, bool] = {}

    direct_class = g.value(prop_shape, SH["class"])
    if isinstance(direct_class, URIRef):
        range_iris.append(str(direct_class))
        range_is_class_map[str(direct_class)] = True

    direct_datatype = g.value(prop_shape, SH.datatype)
    if isinstance(direct_datatype, URIRef):
        range_iris.append(str(direct_datatype))
        range_is_class_map[str(direct_datatype)] = False

    for or_list in g.objects(prop_shape, SH["or"]):
        for option in _walk_rdf_list(g, or_list):
            option_class = g.value(option, SH["class"])
            if isinstance(option_class, URIRef):
                range_iris.append(str(option_class))
                range_is_class_map[str(option_class)] = True

            option_datatype = g.value(option, SH.datatype)
            if isinstance(option_datatype, URIRef):
                range_iris.append(str(option_datatype))
                range_is_class_map[str(option_datatype)] = False

    unique_range_iris: list[str] = []
    for range_iri in range_iris:
        if range_iri not in unique_range_iris:
            unique_range_iris.append(range_iri)

    if not unique_range_iris:
        return None

    path_iri = str(path)
    description = ""
    comment = g.value(path, RDFS.comment)
    if comment:
        description = str(comment)

    primary_range = unique_range_iris[0]
    return OntologyProperty(
        iri=path_iri,
        name=iri_local_name(path_iri),
        range_iri=primary_range,
        range_is_class=range_is_class_map.get(primary_range, False),
        cardinality=_cardinality_from_range(min_count, max_count),
        description=description,
        alternate_range_iris=unique_range_iris[1:],
    )


def _merge_property(existing: OntologyProperty, new: OntologyProperty) -> OntologyProperty:
    """Merge two property definitions for the same path coming from multiple shapes."""
    ranges: list[str] = []
    for range_iri in [*existing.all_range_iris, *new.all_range_iris]:
        if range_iri not in ranges:
            ranges.append(range_iri)

    primary_range = ranges[0]
    range_is_class = (
        existing.range_is_class if primary_range == existing.range_iri else new.range_is_class
    )

    return OntologyProperty(
        iri=existing.iri,
        name=existing.name,
        range_iri=primary_range,
        range_is_class=range_is_class,
        cardinality=_merge_cardinality(existing.cardinality, new.cardinality),
        description=existing.description or new.description,
        alternate_range_iris=ranges[1:],
    )


def _extract_properties(g: Graph, shape_iris: list[str]) -> list[OntologyProperty]:
    """Extract SHACL properties for a class from all shapes targeting it."""
    props: dict[str, OntologyProperty] = {}
    for shape_iri in shape_iris:
        shape_ref = URIRef(shape_iri)
        for prop_shape in g.objects(shape_ref, SH.property):
            prop = _extract_property_from_shape(g, prop_shape)
            if not prop:
                continue
            if prop.iri in props:
                props[prop.iri] = _merge_property(props[prop.iri], prop)
            else:
                props[prop.iri] = prop
    return sorted(props.values(), key=lambda p: p.iri)


def _extract_vocab_members(g: Graph, vocab_iri: str) -> list[str]:
    """Extract the enumerated members of a vocabulary type."""
    members: list[str] = []
    vocab_ref = URIRef(vocab_iri)

    for equiv in g.objects(vocab_ref, OWL.equivalentClass):
        for one_of in g.objects(equiv, OWL.oneOf):
            # Walk the RDF list
            current = one_of
            while current and str(current) != str(RDF.nil):
                first = g.value(current, RDF.first)
                if first:
                    members.append(str(first))
                current = g.value(current, RDF.rest)

    return sorted(members)


def load_extensions(g: Graph, extensions_dir: Path) -> dict[str, tuple[str, str]]:
    """Load extension ontology .ttl files into the graph and return namespace mappings.

    Returns a dict mapping namespace URI -> (top_level, module) for each
    extension directory found under extensions_dir.
    """
    ext_modules: dict[str, tuple[str, str]] = {}
    if not extensions_dir.exists():
        logger.info("No extensions directory at %s", extensions_dir)
        return ext_modules

    ttl_count = 0
    for ext_dir in sorted(extensions_dir.iterdir()):
        if not ext_dir.is_dir():
            continue
        ext_name = ext_dir.name
        for ttl_file in sorted(ext_dir.glob("*.ttl")):
            if "exemplar" in ttl_file.name:
                continue
            try:
                g.parse(str(ttl_file), format="turtle")
                ttl_count += 1
            except Exception as e:
                logger.warning("Failed to parse extension %s: %s", ttl_file, e)

        for prefix, ns_uri in g.namespaces():
            ns_str = str(ns_uri)
            if ext_name in ns_str and ns_str not in PREFIX_TO_MODULE and ns_str not in ext_modules:
                ext_modules[ns_str] = ("ext", ext_name)

    logger.info("Loaded %d extension Turtle files", ttl_count)
    return ext_modules


def parse_ontology(
    ontology_root: Path,
    extensions_dir: Path | None = None,
) -> OntologySchema:
    """Parse the UCO/CASE ontology and return a typed schema model.

    If extensions_dir is provided, extension ontologies are loaded and their
    classes are included with module keys like ``ext.<name>``.
    """
    g = load_ontology(ontology_root)

    ext_modules: dict[str, tuple[str, str]] = {}
    if extensions_dir is not None:
        ext_modules = load_extensions(g, extensions_dir)

    schema = OntologySchema()

    # Extract namespace prefixes from the graph
    for prefix, ns_uri in g.namespaces():
        if prefix:
            schema.namespaces[prefix] = str(ns_uri)

    # Extract classes
    results = g.query(CLASSES_QUERY)
    class_data: dict[str, dict] = {}

    for row in results:
        cls_iri = str(row["class"])
        if cls_iri in class_data:
            if row.shape:
                class_data[cls_iri]["shapes"].add(str(row.shape))
            if row.parent:
                class_data[cls_iri]["parents"].add(str(row.parent))
        else:
            label = str(row.label) if row.label else iri_local_name(cls_iri)
            comment = str(row.comment) if row.comment else ""
            parents: set[str] = set()
            shapes: set[str] = set()
            if row.shape:
                shapes.add(str(row.shape))
            if row.parent:
                parents.add(str(row.parent))
            class_data[cls_iri] = {
                "label": label,
                "comment": comment,
                "parents": parents,
                "shapes": shapes,
            }

    logger.info("Found %d classes with SHACL shapes", len(class_data))

    for cls_iri, data in class_data.items():
        top_level, module = _classify_module(cls_iri, ext_modules)
        module_key = f"{top_level}.{module}"

        is_facet = _is_subclass_of(g, cls_iri, FACET_IRI)
        properties = _extract_properties(g, sorted(data["shapes"]))

        ont_class = OntologyClass(
            iri=cls_iri,
            name=iri_local_name(cls_iri),
            namespace_prefix=f"{top_level}-{module}",
            module=module_key,
            parent_iris=sorted(data["parents"]),
            properties=properties,
            is_facet=is_facet,
            description=data["comment"],
        )
        schema.classes[cls_iri] = ont_class

        if module_key not in schema.modules:
            schema.modules[module_key] = []
        schema.modules[module_key].append(cls_iri)

    # Extract vocabulary types
    vocab_results = g.query(VOCABS_QUERY)
    for row in vocab_results:
        vocab_iri = str(row.vocab)
        members = _extract_vocab_members(g, vocab_iri)

        schema.vocabs[vocab_iri] = OntologyVocab(
            iri=vocab_iri,
            name=iri_local_name(vocab_iri),
            members=members,
        )

    logger.info(
        "Schema: %d classes, %d vocabs, %d modules",
        len(schema.classes),
        len(schema.vocabs),
        len(schema.modules),
    )

    return schema
