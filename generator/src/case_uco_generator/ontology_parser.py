"""Parse UCO/CASE OWL+SHACL Turtle files and extract a typed schema model."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import replace
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
# This is the high-fidelity path: classes with SHACL shapes carry property
# constraints that produce typed bindings.
CLASSES_QUERY = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT DISTINCT ?class ?shape ?label ?comment ?parent WHERE {
    ?class a owl:Class .
    FILTER(!isBlank(?class))
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

# SPARQL: Select all OWL classes regardless of whether they have SHACL shapes.
# Many extension ontologies (especially CAC) declare large numbers of T-Box-only
# subclasses without dedicated SHACL constraints — they still need to be
# registered so search_classes / find_classes_for_domain can discover them.
ALL_CLASSES_QUERY = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?class ?label ?comment ?parent WHERE {
    ?class a owl:Class .
    FILTER(!isBlank(?class))
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


def _allowed(ttl_file: Path, allowed: set[str] | None, repo_root: Path | None) -> bool:
    if allowed is None:
        return True
    if repo_root is None:
        return True
    try:
        rel = ttl_file.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return True
    return rel in allowed


def load_ontology(
    ontology_root: Path,
    allowed: set[str] | None = None,
    repo_root: Path | None = None,
) -> Graph:
    """Load UCO and CASE Turtle files into a single RDFLib graph."""
    g = Graph()

    uco_dir = ontology_root / "UCO" / "ontology" / "uco"
    case_dir = ontology_root / "CASE" / "ontology"

    ttl_count = 0
    for ttl_dir in [uco_dir, case_dir]:
        if not ttl_dir.exists():
            logger.warning("Ontology directory not found: %s", ttl_dir)
            continue
        for ttl_file in ttl_dir.rglob("*.ttl"):
            if not _allowed(ttl_file, allowed, repo_root):
                continue
            try:
                g.parse(str(ttl_file), format="turtle")
                ttl_count += 1
            except Exception as e:
                logger.warning("Failed to parse %s: %s", ttl_file, e)

    # Also load the CO ontology if present
    co_dir = ontology_root / "UCO" / "ontology" / "co"
    if co_dir.exists():
        for ttl_file in co_dir.rglob("*.ttl"):
            if not _allowed(ttl_file, allowed, repo_root):
                continue
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
) -> tuple[str, str] | None:
    """Map a class IRI to (top-level, module) based on namespace.

    Returns None for IRIs from external/foundational ontologies (gUFO, BFO, etc.)
    that should be recorded as informational parents but not classified into a
    generated module.
    """
    ns = iri_namespace(iri)
    if ns in EXTERNAL_IGNORE_NS:
        return None
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
    # Multiple sh:property shapes on the same sh:path are conjunctive: every
    # shape must hold, so the effective bounds are max(minCount) and
    # min(maxCount). A single shape carrying sh:maxCount 1 therefore pins the
    # property to a scalar even when sibling shapes leave the count unbounded.
    required = left.is_required or right.is_required
    is_list = left.is_list and right.is_list
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


def _extract_properties(
    g: Graph,
    shape_iris: list[str],
    class_iri: str | None = None,
) -> list[OntologyProperty]:
    """Extract SHACL properties for a class from all shapes targeting it.

    When ``class_iri`` is provided, shapes whose namespace differs from the
    class's namespace are skipped.  This prevents extension validation
    profiles (for example, CAC's cacontology-synthesis-shapes:ActionSemanticsShape
    targeting uco-action:Action with sh:minCount 1 on startTime) from
    bleeding into the generated typed binding for the upstream class.  Such
    shapes still execute during SHACL validation; they simply do not redefine
    the class structure produced by code generation.
    """
    class_ns = iri_namespace(class_iri) if class_iri else None
    props: dict[str, OntologyProperty] = {}
    # Cardinality is accumulated per path independently of range extraction.
    # UCO routinely splits one property across sibling shapes, with the range
    # on one shape (sh:datatype) and the bound on another (sh:maxCount 1).
    # _extract_property_from_shape discards range-less shapes, so collecting
    # counts here is what keeps such a bound from being lost.
    path_cardinalities: dict[str, Cardinality] = {}
    for shape_iri in shape_iris:
        if class_ns is not None and iri_namespace(shape_iri) != class_ns:
            continue
        shape_ref = URIRef(shape_iri)
        for prop_shape in g.objects(shape_ref, SH.property):
            path = g.value(prop_shape, SH.path)
            if isinstance(path, URIRef):
                path_iri = str(path)
                min_raw = g.value(prop_shape, SH.minCount)
                max_raw = g.value(prop_shape, SH.maxCount)
                shape_cardinality = _cardinality_from_range(
                    int(min_raw) if min_raw else 0,
                    int(max_raw) if max_raw else None,
                )
                if path_iri in path_cardinalities:
                    shape_cardinality = _merge_cardinality(
                        path_cardinalities[path_iri], shape_cardinality
                    )
                path_cardinalities[path_iri] = shape_cardinality

            prop = _extract_property_from_shape(g, prop_shape)
            if not prop:
                continue
            if prop.iri in props:
                props[prop.iri] = _merge_property(props[prop.iri], prop)
            else:
                props[prop.iri] = prop

    resolved = [
        replace(prop, cardinality=path_cardinalities.get(iri, prop.cardinality))
        for iri, prop in props.items()
    ]
    return sorted(resolved, key=lambda p: p.iri)


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


EXTERNAL_IGNORE_NS: set[str] = {
    "http://purl.org/nemo/gufo#",
    "http://purl.org/nemo/gufo/",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
    "http://purl.obolibrary.org/obo/",
    "http://www.w3.org/ns/prov#",
    "http://www.w3.org/2006/time#",
    "http://www.opengis.net/ont/geosparql#",
    "http://xmlns.com/foaf/0.1/",
}


def _derive_submodule(ext_name: str, ns_uri: str, prefix: str) -> str:
    """Derive a sub-module name from a namespace prefix or URI."""
    stem = prefix.replace(f"{ext_name}-", "").replace(ext_name, "").strip("-")
    if stem:
        return re.sub(r"[^a-z0-9]", "_", stem.lower())
    parts = ns_uri.rstrip("#/").rsplit("/", 1)
    if len(parts) == 2 and parts[1]:
        return re.sub(r"[^a-z0-9]", "_", parts[1].lower())
    return "core"


def load_extension_manifest(ext_dir: Path) -> dict | None:
    """Load and return a manifest.json from an extension directory, or None."""
    manifest_path = ext_dir / "manifest.json"
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Failed to load manifest from %s: %s", manifest_path, e)
        return None


# Subdirectories of the ontology/ vendoring root that are core/upper
# ontologies, not extension directories.
_NON_EXTENSION_DIRS = {"CASE", "UCO", "upper"}


def load_extensions(
    g: Graph,
    extensions_dir: Path | list[Path],
    allowed: set[str] | None = None,
    repo_root: Path | None = None,
) -> dict[str, tuple[str, str]]:
    """Load extension ontology TTL files into the graph and return namespace mappings.

    ``extensions_dir`` may be a single root or a list of roots (v1.19.0:
    SDK-native extensions live in ``extensions/`` while upstream-vendored
    ontologies such as CAC, AEO, and SOLVE-IT live in ``ontology/``). When
    the same extension name appears in several roots, the first root wins.

    Uses manifest.json when present in each extension directory for explicit
    namespace-to-module mapping and file lists.  Falls back to the legacy
    heuristic for directories without a manifest (e.g., toolcap) — but only
    inside an ``extensions/`` root, so that CASE/UCO submodules and vendored
    upper ontologies under ``ontology/`` are never swept in as extensions.

    Returns a dict mapping namespace URI -> (top_level, module) for each
    extension directory found.
    """
    roots = [extensions_dir] if isinstance(extensions_dir, Path) else list(extensions_dir)

    ext_modules: dict[str, tuple[str, str]] = {}
    ttl_count = 0
    seen_names: set[str] = set()
    for root in roots:
        if not root.exists():
            logger.info("No extensions directory at %s", root)
            continue
        for ext_dir in sorted(root.iterdir()):
            if not ext_dir.is_dir():
                continue
            ext_name = ext_dir.name
            if ext_name in _NON_EXTENSION_DIRS or ext_name in seen_names:
                continue

            manifest = load_extension_manifest(ext_dir)
            if manifest is not None:
                seen_names.add(ext_name)
                ttl_count += _load_extension_from_manifest(
                    g, ext_dir, manifest, ext_modules, allowed=allowed, repo_root=repo_root
                )
            elif root.name == "extensions":
                seen_names.add(ext_name)
                ttl_count += _load_extension_legacy(
                    g, ext_dir, ext_name, ext_modules, allowed=allowed, repo_root=repo_root
                )

    logger.info("Loaded %d extension Turtle files", ttl_count)
    return ext_modules


def _build_prefix_header(namespaces: dict[str, str]) -> str:
    """Build a Turtle @prefix block from manifest namespaces.

    Upstream TTL files sometimes reference sibling-module prefixes without
    declaring them (e.g., AEO engagement.ttl uses ``objective:`` from
    objective.ttl).  Prepending these declarations ensures the Turtle
    parser can resolve all prefixes.
    """
    lines = []
    for prefix, ns_uri in sorted(namespaces.items()):
        lines.append(f"@prefix {prefix}: <{ns_uri}> .")
    return "\n".join(lines) + "\n\n" if lines else ""


def _load_extension_from_manifest(
    g: Graph,
    ext_dir: Path,
    manifest: dict,
    ext_modules: dict[str, tuple[str, str]],
    allowed: set[str] | None = None,
    repo_root: Path | None = None,
) -> int:
    """Load extension files according to its manifest.json.  Returns count of parsed files."""
    ext_name = manifest["name"]
    ttl_count = 0

    namespaces: dict[str, str] = manifest.get("namespaces", {})
    prefix_header = _build_prefix_header(namespaces)

    for file_list_key in ("owl_files", "shacl_files", "bridge_files"):
        for rel_path in manifest.get(file_list_key, []):
            ttl_file = ext_dir / rel_path
            if not ttl_file.exists():
                logger.warning("Extension %s: file not found: %s", ext_name, ttl_file)
                continue
            if not _allowed(ttl_file, allowed, repo_root):
                continue
            try:
                ttl_content = ttl_file.read_text(encoding="utf-8")
                g.parse(data=prefix_header + ttl_content, format="turtle")
                ttl_count += 1
            except Exception as e:
                logger.warning("Failed to parse extension %s file %s: %s", ext_name, ttl_file, e)

    namespaces: dict[str, str] = manifest.get("namespaces", {})
    for prefix, ns_uri in namespaces.items():
        if ns_uri not in PREFIX_TO_MODULE and ns_uri not in ext_modules:
            # Use the full manifest prefix (e.g. "cacontology-sex-trafficking")
            # as the module name. Codegen backends sanitize hyphens for
            # language-specific file/module identifiers, but the registry
            # records the prefix verbatim so MCP search and developer
            # documentation match the upstream namespace convention.
            ext_modules[ns_uri] = (f"ext.{ext_name}", prefix)

    return ttl_count


def _load_extension_legacy(
    g: Graph,
    ext_dir: Path,
    ext_name: str,
    ext_modules: dict[str, tuple[str, str]],
    allowed: set[str] | None = None,
    repo_root: Path | None = None,
) -> int:
    """Legacy loader for extension directories without manifest.json."""
    ttl_count = 0
    for ttl_file in sorted(ext_dir.glob("*.ttl")):
        if "exemplar" in ttl_file.name:
            continue
        if not _allowed(ttl_file, allowed, repo_root):
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

    return ttl_count


def parse_ontology(
    ontology_root: Path,
    extensions_dir: Path | list[Path] | None = None,
    allowed: set[str] | None = None,
    repo_root: Path | None = None,
) -> OntologySchema:
    """Parse the UCO/CASE ontology and return a typed schema model.

    If extensions_dir is provided (a single root or a list of roots),
    extension ontologies are loaded and their classes are included with
    module keys like ``ext.<name>``.

    ``allowed`` is an optional set of repo-relative POSIX paths. When set,
    only those Turtle files are parsed (used by dependent-only incremental
    generate). Pass ``repo_root`` so path checks resolve correctly.
    """
    g = load_ontology(ontology_root, allowed=allowed, repo_root=repo_root)

    ext_modules: dict[str, tuple[str, str]] = {}
    if extensions_dir is not None:
        ext_modules = load_extensions(
            g, extensions_dir, allowed=allowed, repo_root=repo_root
        )

    schema = OntologySchema()

    # Extract namespace prefixes from the graph
    for prefix, ns_uri in g.namespaces():
        if prefix:
            schema.namespaces[prefix] = str(ns_uri)

    # Extract classes — first pass: classes with SHACL NodeShapes (full property
    # detail), second pass: every remaining owl:Class so that pure T-Box
    # taxonomies (common in CAC modules) are still discoverable.
    class_data: dict[str, dict] = {}

    for row in g.query(CLASSES_QUERY):
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

    shape_class_count = len(class_data)
    logger.info("Found %d classes with SHACL shapes", shape_class_count)

    for row in g.query(ALL_CLASSES_QUERY):
        cls_iri = str(row["class"])
        if cls_iri in class_data:
            if row.parent:
                class_data[cls_iri]["parents"].add(str(row.parent))
            continue
        label = str(row.label) if row.label else iri_local_name(cls_iri)
        comment = str(row.comment) if row.comment else ""
        parents = set()
        if row.parent:
            parents.add(str(row.parent))
        class_data[cls_iri] = {
            "label": label,
            "comment": comment,
            "parents": parents,
            "shapes": set(),
        }

    logger.info(
        "Found %d total classes (%d with SHACL shapes, %d T-Box only)",
        len(class_data),
        shape_class_count,
        len(class_data) - shape_class_count,
    )

    for cls_iri, data in class_data.items():
        classification = _classify_module(cls_iri, ext_modules)
        if classification is None:
            logger.debug("Skipping external IRI (informational parent): %s", cls_iri)
            continue
        top_level, module = classification
        module_key = f"{top_level}.{module}"

        is_facet = _is_subclass_of(g, cls_iri, FACET_IRI)
        properties = _extract_properties(g, sorted(data["shapes"]), class_iri=cls_iri)

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
