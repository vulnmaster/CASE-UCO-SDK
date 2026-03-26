"""Extension scaffolding — generate starter classes from an extension ontology TTL file.

Takes an extension .ttl file (OWL + SHACL), parses its classes and properties,
and emits starter code for Python, C#, Java, and Rust that developers can
drop into their projects.
"""

from __future__ import annotations

import logging
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from case_uco_generator.schema_model import (
    OntologyClass,
    OntologySchema,
    iri_local_name,
)
from case_uco_generator.ontology_parser import (
    FACET_IRI,
    _is_subclass_of,
    _extract_properties,
)

logger = logging.getLogger(__name__)

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


def parse_extension(ttl_paths: list[Path]) -> tuple[OntologySchema, str, str]:
    """Parse extension TTL files and return (schema, prefix, namespace_uri)."""
    g = Graph()
    for p in ttl_paths:
        g.parse(str(p), format="turtle")

    schema = OntologySchema()
    ext_prefix = ""
    ext_ns = ""

    # Collect all subject IRIs to identify which namespace is the extension's own
    subject_iris: set[str] = set()
    for s in g.subjects():
        if isinstance(s, URIRef):
            subject_iris.add(str(s))

    IGNORE_NS = {"w3.org", "unifiedcyberontology", "caseontology", "purl.org",
                 "xmlns.com", "schema.org", "brickschema", "opengis", "rdfs.org",
                 "usefulinc", "linked-data"}

    for prefix, ns_uri in g.namespaces():
        ns_str = str(ns_uri)
        schema.namespaces[prefix] = ns_str
        if not prefix:
            continue
        if any(ignore in ns_str for ignore in IGNORE_NS):
            continue
        if any(subj.startswith(ns_str) for subj in subject_iris):
            if not ext_prefix:
                ext_prefix = prefix
                ext_ns = ns_str

    results = g.query(CLASSES_QUERY)
    class_data: dict[str, dict] = {}

    for row in results:
        cls_iri = str(row["class"])
        if ext_ns and not cls_iri.startswith(ext_ns):
            continue
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
                "label": label, "comment": comment,
                "parents": parents, "shapes": shapes,
            }

    for cls_iri, data in class_data.items():
        is_facet = _is_subclass_of(g, cls_iri, FACET_IRI)
        properties = _extract_properties(g, sorted(data["shapes"]))
        ont_class = OntologyClass(
            iri=cls_iri,
            name=iri_local_name(cls_iri),
            namespace_prefix=ext_prefix,
            module=f"ext.{ext_prefix}",
            parent_iris=sorted(data["parents"]),
            properties=properties,
            is_facet=is_facet,
            description=data["comment"],
        )
        schema.classes[cls_iri] = ont_class

    return schema, ext_prefix, ext_ns


def _to_snake(name: str) -> str:
    import re
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def scaffold_python(schema: OntologySchema, prefix: str, ns: str) -> str:
    lines: list[str] = []
    lines.append(f'"""Scaffolded extension classes for {prefix} — customize as needed."""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("from dataclasses import dataclass, field")
    lines.append("from typing import Optional")
    lines.append("")

    for cls in sorted(schema.classes.values(), key=lambda c: c.name):
        lines.append("@dataclass")
        lines.append(f"class {cls.name}:")
        desc = cls.description[:200] if cls.description else cls.name
        lines.append(f'    """{desc}"""')
        lines.append("")
        lines.append(f'    CLASS_IRI: str = "{cls.iri}"')
        lines.append(f'    NAMESPACE_PREFIX: str = "{prefix}"')
        lines.append("")

        for prop in cls.properties:
            field_name = _to_snake(prop.name)
            type_str = prop.type_name_for("python")
            if prop.cardinality.is_list:
                lines.append(f"    {field_name}: list[{type_str}] = field(default_factory=list, metadata={{")
            else:
                lines.append(f"    {field_name}: Optional[{type_str}] = field(default=None, metadata={{")
            lines.append(f"        'jsonld_key': '{prefix}:{prop.name}',")
            lines.append(f"        'required': {prop.cardinality.is_required},")
            lines.append(f"        'cardinality': '{prop.cardinality.value}',")
            lines.append(f"        'range_iri': '{prop.range_iri}',")
            lines.append(f"        'alternate_range_iris': {prop.alternate_range_iris},")
            lines.append("    })")

        lines.append("")
        lines.append("")
    lines.append(f"# Usage:")
    lines.append(f"# from case_uco import CASEGraph")
    lines.append(f"# graph = CASEGraph(extra_context={{'{prefix}': '{ns}'}})")
    lines.append(f"# graph.add({list(schema.classes.values())[0].name}(...))")
    lines.append(f"# print(graph.serialize())")
    return "\n".join(lines)


def scaffold_csharp(schema: OntologySchema, prefix: str, ns: str) -> str:
    lines: list[str] = []
    ns_pascal = prefix[0].upper() + prefix[1:]
    lines.append(f"// Scaffolded extension classes for {prefix} — customize as needed.")
    lines.append(f"namespace CaseUco.Ext.{ns_pascal}")
    lines.append("{")
    for cls in sorted(schema.classes.values(), key=lambda c: c.name):
        lines.append(f"    /// <summary>{cls.description[:120] if cls.description else cls.name}</summary>")
        lines.append(f"    public class {cls.name}")
        lines.append("    {")
        lines.append(f'        public static readonly string ClassIri = "{cls.iri}";')
        lines.append(f'        public static readonly string NamespacePrefix = "{prefix}";')
        lines.append("")
        for prop in cls.properties:
            cs_type = prop.type_name_for("csharp")
            prop_name = prop.name[0].upper() + prop.name[1:]
            if prop.cardinality.is_list:
                lines.append(f"        public List<{cs_type}> {prop_name} {{ get; set; }} = new List<{cs_type}>();")
            else:
                lines.append(f"        public {cs_type} {prop_name} {{ get; set; }}")
        lines.append("    }")
        lines.append("")
    lines.append("}")
    return "\n".join(lines)


def scaffold_java(schema: OntologySchema, prefix: str, ns: str) -> str:
    lines: list[str] = []
    lines.append(f"// Scaffolded extension classes for {prefix} — customize as needed.")
    lines.append(f"package org.caseontology.ext.{prefix};")
    lines.append("")
    lines.append("import java.util.ArrayList;")
    lines.append("import java.util.List;")
    lines.append("")
    for cls in sorted(schema.classes.values(), key=lambda c: c.name):
        lines.append(f"/** {cls.description[:120] if cls.description else cls.name} */")
        lines.append(f"public class {cls.name} {{")
        lines.append(f'    public static final String CLASS_IRI = "{cls.iri}";')
        lines.append(f'    public static final String NAMESPACE_PREFIX = "{prefix}";')
        lines.append("")
        for prop in cls.properties:
            java_type = prop.type_name_for("java")
            if prop.cardinality.is_list:
                lines.append(f"    private List<{java_type}> {prop.name} = new ArrayList<>();")
            else:
                lines.append(f"    private {java_type} {prop.name};")
        lines.append("")
        for prop in cls.properties:
            java_type = prop.type_name_for("java")
            getter_name = "get" + prop.name[0].upper() + prop.name[1:]
            setter_name = "set" + prop.name[0].upper() + prop.name[1:]
            if prop.cardinality.is_list:
                lines.append(f"    public List<{java_type}> {getter_name}() {{ return {prop.name}; }}")
            else:
                lines.append(f"    public {java_type} {getter_name}() {{ return {prop.name}; }}")
                lines.append(f"    public {cls.name} {setter_name}({java_type} {prop.name}) {{ this.{prop.name} = {prop.name}; return this; }}")
        lines.append("}")
        lines.append("")
    return "\n".join(lines)


def scaffold_rust(schema: OntologySchema, prefix: str, ns: str) -> str:
    lines: list[str] = []
    lines.append(f"//! Scaffolded extension structs for {prefix} — customize as needed.")
    lines.append("")
    lines.append("use serde::Serialize;")
    lines.append("")
    for cls in sorted(schema.classes.values(), key=lambda c: c.name):
        lines.append(f"/// {cls.description[:120] if cls.description else cls.name}")
        lines.append("#[derive(Debug, Clone, Serialize, Default)]")
        lines.append(f"pub struct {cls.name} {{")
        for prop in cls.properties:
            rust_type = prop.type_name_for("rust")
            field_name = _to_snake(prop.name)
            if prop.cardinality.is_list:
                lines.append(f"    pub {field_name}: Vec<{rust_type}>,")
            else:
                lines.append(f"    pub {field_name}: Option<{rust_type}>,")
        lines.append("}")
        lines.append("")
        lines.append(f"impl {cls.name} {{")
        lines.append(f'    pub fn class_iri() -> &\'static str {{ "{cls.iri}" }}')
        lines.append("}")
        lines.append("")
    return "\n".join(lines)


def scaffold_extension(
    ttl_paths: list[Path],
    output_dir: Path,
    languages: list[str] | None = None,
) -> list[Path]:
    """Parse extension TTL and generate starter classes for specified languages."""
    schema, prefix, ns = parse_extension(ttl_paths)

    if not schema.classes:
        logger.warning("No SHACL-shaped classes found in extension TTL files.")
        return []

    if languages is None:
        languages = ["python", "csharp", "java", "rust"]

    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    generators = {
        "python": (scaffold_python, f"{prefix}_classes.py"),
        "csharp": (scaffold_csharp, f"{prefix[0].upper()}{prefix[1:]}Classes.cs"),
        "java": (scaffold_java, f"{prefix[0].upper()}{prefix[1:]}Classes.java"),
        "rust": (scaffold_rust, f"{prefix}_classes.rs"),
    }

    for lang in languages:
        if lang not in generators:
            continue
        gen_fn, filename = generators[lang]
        content = gen_fn(schema, prefix, ns)
        path = output_dir / filename
        path.write_text(content, encoding="utf-8")
        created.append(path)
        logger.info("  -> %s (%s)", path, lang)

    return created
