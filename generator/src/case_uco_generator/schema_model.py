"""Internal schema model — intermediate representation between ontology parser and language backends."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Cardinality(Enum):
    """Property cardinality derived from SHACL sh:minCount / sh:maxCount."""

    ZERO_OR_ONE = "zero_or_one"  # optional single value (max 1, min 0)
    EXACTLY_ONE = "exactly_one"  # required single value (min 1, max 1)
    ZERO_OR_MORE = "zero_or_more"  # optional list (no max or max > 1)
    ONE_OR_MORE = "one_or_more"  # required list (min >= 1, no max or max > 1)

    @classmethod
    def from_counts(cls, min_count: int | None, max_count: int | None) -> Cardinality:
        mn = min_count or 0
        mx = max_count  # None means unbounded

        if mx is not None and mx <= 1:
            return cls.EXACTLY_ONE if mn >= 1 else cls.ZERO_OR_ONE
        else:
            return cls.ONE_OR_MORE if mn >= 1 else cls.ZERO_OR_MORE

    @property
    def is_required(self) -> bool:
        return self in (Cardinality.EXACTLY_ONE, Cardinality.ONE_OR_MORE)

    @property
    def is_list(self) -> bool:
        return self in (Cardinality.ZERO_OR_MORE, Cardinality.ONE_OR_MORE)


# XSD datatype IRI -> (Python type, C# type, Java type, Rust type)
XSD_TYPE_MAP: dict[str, dict[str, str]] = {
    "http://www.w3.org/2001/XMLSchema#string": {
        "python": "str", "csharp": "string", "java": "String", "rust": "String",
    },
    "http://www.w3.org/2001/XMLSchema#integer": {
        "python": "int", "csharp": "long", "java": "long", "rust": "i64",
    },
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": {
        "python": "int", "csharp": "ulong", "java": "long", "rust": "u64",
    },
    "http://www.w3.org/2001/XMLSchema#positiveInteger": {
        "python": "int", "csharp": "ulong", "java": "long", "rust": "u64",
    },
    "http://www.w3.org/2001/XMLSchema#boolean": {
        "python": "bool", "csharp": "bool", "java": "boolean", "rust": "bool",
    },
    "http://www.w3.org/2001/XMLSchema#decimal": {
        "python": "float", "csharp": "decimal", "java": "java.math.BigDecimal", "rust": "f64",
    },
    "http://www.w3.org/2001/XMLSchema#float": {
        "python": "float", "csharp": "float", "java": "float", "rust": "f32",
    },
    "http://www.w3.org/2001/XMLSchema#double": {
        "python": "float", "csharp": "double", "java": "double", "rust": "f64",
    },
    "http://www.w3.org/2001/XMLSchema#dateTime": {
        "python": "datetime", "csharp": "DateTime", "java": "java.time.ZonedDateTime", "rust": "String",
    },
    "http://www.w3.org/2001/XMLSchema#hexBinary": {
        "python": "str", "csharp": "byte[]", "java": "byte[]", "rust": "Vec<u8>",
    },
    "http://www.w3.org/2001/XMLSchema#base64Binary": {
        "python": "str", "csharp": "byte[]", "java": "byte[]", "rust": "Vec<u8>",
    },
    "http://www.w3.org/2001/XMLSchema#anyURI": {
        "python": "str", "csharp": "Uri", "java": "java.net.URI", "rust": "String",
    },
    "http://www.w3.org/2001/XMLSchema#duration": {
        "python": "str", "csharp": "TimeSpan", "java": "java.time.Duration", "rust": "String",
    },
    "http://www.w3.org/2001/XMLSchema#byte": {
        "python": "int", "csharp": "sbyte", "java": "byte", "rust": "i8",
    },
    "http://www.w3.org/2001/XMLSchema#unsignedInt": {
        "python": "int", "csharp": "uint", "java": "long", "rust": "u32",
    },
    "http://www.w3.org/2001/XMLSchema#unsignedShort": {
        "python": "int", "csharp": "ushort", "java": "int", "rust": "u16",
    },
    "http://www.w3.org/2001/XMLSchema#long": {
        "python": "int", "csharp": "long", "java": "long", "rust": "i64",
    },
    "http://www.w3.org/2001/XMLSchema#int": {
        "python": "int", "csharp": "int", "java": "int", "rust": "i32",
    },
    "http://www.w3.org/2001/XMLSchema#short": {
        "python": "int", "csharp": "short", "java": "short", "rust": "i16",
    },
    "http://www.w3.org/2001/XMLSchema#unsignedLong": {
        "python": "int", "csharp": "ulong", "java": "long", "rust": "u64",
    },
}

UNION_FALLBACK_TYPE_MAP: dict[str, str] = {
    "python": "Any",
    "csharp": "object",
    "java": "Object",
    "rust": "serde_json::Value",
}

ONTOLOGY_NAMESPACE_TO_PREFIX: dict[str, str] = {
    "https://ontology.unifiedcyberontology.org/uco/core/": "uco-core",
    "https://ontology.unifiedcyberontology.org/uco/action/": "uco-action",
    "https://ontology.unifiedcyberontology.org/uco/analysis/": "uco-analysis",
    "https://ontology.unifiedcyberontology.org/uco/configuration/": "uco-configuration",
    "https://ontology.unifiedcyberontology.org/uco/identity/": "uco-identity",
    "https://ontology.unifiedcyberontology.org/uco/location/": "uco-location",
    "https://ontology.unifiedcyberontology.org/uco/marking/": "uco-marking",
    "https://ontology.unifiedcyberontology.org/uco/observable/": "uco-observable",
    "https://ontology.unifiedcyberontology.org/uco/pattern/": "uco-pattern",
    "https://ontology.unifiedcyberontology.org/uco/role/": "uco-role",
    "https://ontology.unifiedcyberontology.org/uco/time/": "uco-time",
    "https://ontology.unifiedcyberontology.org/uco/tool/": "uco-tool",
    "https://ontology.unifiedcyberontology.org/uco/types/": "uco-types",
    "https://ontology.unifiedcyberontology.org/uco/victim/": "uco-victim",
    "https://ontology.unifiedcyberontology.org/uco/vocabulary/": "uco-vocabulary",
    "https://ontology.caseontology.org/case/investigation/": "case-investigation",
    "https://ontology.caseontology.org/case/vocabulary/": "case-vocabulary",
}


@dataclass
class OntologyProperty:
    """A property on a class, extracted from SHACL sh:property shapes."""

    iri: str
    name: str
    range_iri: str
    range_is_class: bool
    cardinality: Cardinality
    description: str = ""
    alternate_range_iris: list[str] = field(default_factory=list)

    @property
    def is_xsd_type(self) -> bool:
        return self.range_iri in XSD_TYPE_MAP

    @property
    def all_range_iris(self) -> list[str]:
        ranges = [self.range_iri, *self.alternate_range_iris]
        seen: list[str] = []
        for range_iri in ranges:
            if range_iri not in seen:
                seen.append(range_iri)
        return seen

    @property
    def is_union(self) -> bool:
        return len(self.all_range_iris) > 1

    def type_name_for(self, lang: str) -> str:
        """Return the native type name for a given language."""
        if self.is_union:
            return UNION_FALLBACK_TYPE_MAP[lang]
        if self.is_xsd_type:
            return XSD_TYPE_MAP[self.range_iri][lang]
        return iri_local_name(self.range_iri)

    @property
    def is_vocab_type(self) -> bool:
        return not self.range_is_class and not self.is_xsd_type


@dataclass
class OntologyClass:
    """An OWL class with SHACL shape, extracted from the ontology."""

    iri: str
    name: str
    namespace_prefix: str
    module: str
    parent_iris: list[str] = field(default_factory=list)
    properties: list[OntologyProperty] = field(default_factory=list)
    is_facet: bool = False
    description: str = ""

    @property
    def all_parent_names(self) -> list[str]:
        return [iri_local_name(p) for p in self.parent_iris]


@dataclass
class OntologyVocab:
    """An enumerated vocabulary (rdfs:Datatype with owl:oneOf)."""

    iri: str
    name: str
    members: list[str] = field(default_factory=list)


@dataclass
class OntologySchema:
    """Complete parsed ontology schema — input to code generation backends."""

    classes: dict[str, OntologyClass] = field(default_factory=dict)
    vocabs: dict[str, OntologyVocab] = field(default_factory=dict)
    namespaces: dict[str, str] = field(default_factory=dict)
    modules: dict[str, list[str]] = field(default_factory=dict)

    def without_extensions(self) -> OntologySchema:
        """Return a copy of this schema excluding extension (ext.*) modules."""
        filtered_modules = {k: v for k, v in self.modules.items() if not k.startswith("ext.")}
        ext_iris = set()
        for k, v in self.modules.items():
            if k.startswith("ext."):
                ext_iris.update(v)
        filtered_classes = {k: v for k, v in self.classes.items() if k not in ext_iris}
        return OntologySchema(
            classes=filtered_classes,
            vocabs=dict(self.vocabs),
            namespaces=dict(self.namespaces),
            modules=filtered_modules,
        )

    def classes_in_module(self, module: str) -> list[OntologyClass]:
        iris = self.modules.get(module, [])
        return [self.classes[iri] for iri in iris if iri in self.classes]

    def resolve_class(self, iri: str) -> OntologyClass | None:
        return self.classes.get(iri)

    def resolve_all_properties(self, cls: OntologyClass) -> list[OntologyProperty]:
        """Get all properties including inherited ones, deduplicating by IRI."""
        seen: dict[str, OntologyProperty] = {}
        self._collect_properties(cls, seen)
        return list(seen.values())

    def _collect_properties(
        self, cls: OntologyClass, seen: dict[str, OntologyProperty]
    ) -> None:
        for parent_iri in cls.parent_iris:
            parent = self.classes.get(parent_iri)
            if parent:
                self._collect_properties(parent, seen)
        for prop in cls.properties:
            seen[prop.iri] = prop


def iri_local_name(iri: str) -> str:
    """Extract the local name (fragment or last path segment) from an IRI."""
    if "#" in iri:
        return iri.rsplit("#", 1)[1]
    return iri.rsplit("/", 1)[-1]


def iri_namespace(iri: str) -> str:
    """Extract the namespace (everything before local name) from an IRI."""
    if "#" in iri:
        return iri.rsplit("#", 1)[0] + "#"
    return iri.rsplit("/", 1)[0] + "/"


def compact_ontology_iri(iri: str) -> str:
    """Compact a full ontology IRI to the CASE/UCO JSON-LD prefix form."""
    namespace = iri_namespace(iri)
    prefix = ONTOLOGY_NAMESPACE_TO_PREFIX.get(namespace)
    if prefix:
        return f"{prefix}:{iri_local_name(iri)}"
    return iri
