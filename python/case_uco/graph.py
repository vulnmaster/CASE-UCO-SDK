"""CASEGraph — the main entry point for building and serializing CASE/UCO graphs."""

from __future__ import annotations

import json
import uuid
from dataclasses import Field, fields, is_dataclass
from datetime import date, datetime
from typing import Any, TypeVar, Type

T = TypeVar("T")

_builtin_id = id

# Standard CASE/UCO JSON-LD context prefixes
DEFAULT_CONTEXT: dict[str, str] = {
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "kb": "http://example.org/kb/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
    "uco-victim": "https://ontology.unifiedcyberontology.org/uco/victim/",
    "uco-analysis": "https://ontology.unifiedcyberontology.org/uco/analysis/",
    "uco-configuration": "https://ontology.unifiedcyberontology.org/uco/configuration/",
    "uco-marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
    "uco-pattern": "https://ontology.unifiedcyberontology.org/uco/pattern/",
    "uco-time": "https://ontology.unifiedcyberontology.org/uco/time/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

_RANGE_IRI_TO_TYPED_LITERAL = {
    "http://www.w3.org/2001/XMLSchema#boolean": "xsd:boolean",
    "http://www.w3.org/2001/XMLSchema#integer": "xsd:integer",
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": "xsd:nonNegativeInteger",
    "http://www.w3.org/2001/XMLSchema#positiveInteger": "xsd:positiveInteger",
    "http://www.w3.org/2001/XMLSchema#decimal": "xsd:decimal",
    "http://www.w3.org/2001/XMLSchema#float": "xsd:float",
    "http://www.w3.org/2001/XMLSchema#double": "xsd:double",
    "http://www.w3.org/2001/XMLSchema#dateTime": "xsd:dateTime",
    "http://www.w3.org/2001/XMLSchema#hexBinary": "xsd:hexBinary",
}


class CASEGraph:
    """Build a CASE/UCO JSON-LD graph with typed objects.

    Usage:
        graph = CASEGraph(kb_prefix="http://example.org/kb/")
        tool = graph.create(Tool, name="Tool A")
        print(graph.serialize())
    """

    def __init__(
        self,
        kb_prefix: str = "http://example.org/kb/",
        extra_context: dict[str, str] | None = None,
    ):
        self.kb_prefix = kb_prefix
        self._context = dict(DEFAULT_CONTEXT)
        self._context["kb"] = kb_prefix
        if extra_context:
            self._context.update(extra_context)
        self._objects: list[dict[str, Any]] = []
        self._id_map: dict[int, str] = {}
        self._instances: list[Any] = []

    def create(self, cls: Type[T], *, id: str | None = None, **kwargs: Any) -> T:
        """Create an instance of a CASE/UCO class and add it to the graph.

        Args:
            cls: The CASE/UCO class to instantiate.
            id: Optional user-supplied @id for deterministic IRIs.
                If not provided, a UUID-based @id is auto-generated.
            **kwargs: Arguments passed to the class constructor.

        Returns the created instance so it can be referenced by other objects.
        """
        instance = cls(**kwargs)
        self._validate_instance(instance)
        obj_id = id if id is not None else self._mint_id(instance)
        self._id_map[_builtin_id(instance)] = obj_id
        self._instances.append(instance)
        json_obj = self._to_jsonld(instance, obj_id)
        self._objects.append(json_obj)
        return instance

    def add(self, instance: Any, *, id: str | None = None) -> str:
        """Add a pre-created instance to the graph.

        Args:
            instance: A dataclass instance of a CASE/UCO type.
            id: Optional user-supplied @id for deterministic IRIs.

        Returns the assigned @id.
        """
        self._validate_instance(instance)
        obj_id = id if id is not None else self._mint_id(instance)
        self._id_map[_builtin_id(instance)] = obj_id
        self._instances.append(instance)
        json_obj = self._to_jsonld(instance, obj_id)
        self._objects.append(json_obj)
        return obj_id

    def get_id(self, instance: Any) -> str | None:
        """Get the @id for a previously added instance."""
        return self._id_map.get(_builtin_id(instance))

    def __len__(self) -> int:
        """Return the number of objects in the graph."""
        return len(self._objects)

    def serialize(self, format: str = "json-ld", indent: int = 4) -> str:
        """Serialize the graph to JSON-LD string."""
        if format != "json-ld":
            raise ValueError(f"Unsupported format: {format}. Only 'json-ld' is supported.")
        doc = {
            "@context": self._context,
            "@graph": self._objects,
        }
        return json.dumps(doc, indent=indent, default=str)

    def write(self, path: str, format: str = "json-ld", indent: int = 4) -> None:
        """Write the graph to a file."""
        content = self.serialize(format=format, indent=indent)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def load(self, json_str: str) -> None:
        """Load a JSON-LD string into this graph, merging context and appending objects."""
        doc = json.loads(json_str)
        if "@context" in doc and isinstance(doc["@context"], dict):
            self._context.update(doc["@context"])
        if "@graph" in doc and isinstance(doc["@graph"], list):
            self._objects.extend(doc["@graph"])

    def load_file(self, path: str) -> None:
        """Read and load a JSON-LD file into this graph."""
        with open(path, "r", encoding="utf-8") as f:
            self.load(f.read())

    def estimate_triples(self) -> int:
        """Estimate the number of RDF triples this graph will produce.

        Counts @type (1 triple), @id (implicit, not counted), and each
        property value as individual triples. Nested objects contribute
        their own triples recursively.
        """
        return sum(self._count_triples(obj) for obj in self._objects)

    @staticmethod
    def _count_triples(obj: dict) -> int:
        count = 0
        for key, value in obj.items():
            if key == "@id":
                continue
            if key == "@type":
                count += 1
                continue
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        count += 1 + CASEGraph._count_triples(item)
                    else:
                        count += 1
            elif isinstance(value, dict):
                if "@value" in value:
                    count += 1
                else:
                    count += 1 + CASEGraph._count_triples(value)
            else:
                count += 1
        return count

    def split(self, max_objects: int = 10000) -> list[CASEGraph]:
        """Split this graph into smaller chunks of at most max_objects each.

        Each chunk gets a copy of the context. The original graph is not modified.
        """
        chunks: list[CASEGraph] = []
        for i in range(0, len(self._objects), max_objects):
            chunk = CASEGraph(kb_prefix=self.kb_prefix)
            chunk._context = dict(self._context)
            chunk._objects = list(self._objects[i:i + max_objects])
            chunks.append(chunk)
        return chunks

    @classmethod
    def merge_files(cls, paths: list[str], kb_prefix: str = "http://example.org/kb/") -> CASEGraph:
        """Load and merge multiple JSON-LD graph files into a single graph.

        Contexts are merged (later files override earlier ones for
        conflicting prefixes). All objects are concatenated.
        """
        merged = cls(kb_prefix=kb_prefix)
        for path in paths:
            merged.load_file(path)
        return merged

    def _mint_id(self, instance: Any) -> str:
        """Generate a UUID-based @id for an instance."""
        cls_name = type(instance).__name__
        # Convert PascalCase to kebab-case for the IRI local name
        prefix = self._get_prefix(instance)
        return f"{prefix}:{cls_name}-{uuid.uuid4()}"

    def _get_prefix(self, instance: Any) -> str:
        """Get the namespace prefix for an instance (defaults to kb)."""
        return "kb"

    def _to_jsonld(self, instance: Any, obj_id: str) -> dict[str, Any]:
        """Convert a dataclass instance to a JSON-LD dictionary."""
        result: dict[str, Any] = {"@id": obj_id}

        cls = type(instance)
        if hasattr(cls, "CLASS_IRI"):
            # Convert full IRI to prefixed form
            class_iri = cls.CLASS_IRI
            result["@type"] = self._compact_iri(class_iri)

        if not is_dataclass(instance):
            return result

        for f in fields(instance):
            if f.name in ("CLASS_IRI", "NAMESPACE_PREFIX"):
                continue

            value = getattr(instance, f.name)
            if value is None:
                continue
            if isinstance(value, list) and len(value) == 0:
                continue

            prop_key = self._property_key(instance, f)
            range_iri = f.metadata.get("range_iri")

            if isinstance(value, list):
                result[prop_key] = [self._convert_value(v, range_iri=range_iri) for v in value]
            else:
                result[prop_key] = self._convert_value(value, range_iri=range_iri)

        return result

    def _property_key(self, instance: Any, field_info: Field[Any]) -> str:
        """Resolve the JSON-LD property key from generated field metadata when available."""
        metadata_key = field_info.metadata.get("jsonld_key")
        if metadata_key:
            return metadata_key

        parts = field_info.name.split("_")
        camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
        ns_prefix = getattr(type(instance), "NAMESPACE_PREFIX", "uco-core")
        return f"{ns_prefix}:{camel}"

    def _convert_value(self, value: Any, range_iri: str | None = None) -> Any:
        """Convert a Python value to JSON-LD representation."""
        if is_dataclass(value) and not isinstance(value, type):
            # Nested object — create inline or reference
            self._validate_instance(value)
            if _builtin_id(value) in self._id_map:
                return {"@id": self._id_map[_builtin_id(value)]}
            # Inline as a facet-like sub-object
            inline_id = self._mint_id(value)
            return self._to_jsonld(value, inline_id)

        if range_iri in _RANGE_IRI_TO_TYPED_LITERAL:
            return self._typed_literal(_RANGE_IRI_TO_TYPED_LITERAL[range_iri], value)

        if isinstance(value, datetime):
            return self._typed_literal("xsd:dateTime", value)
        if isinstance(value, date):
            return self._typed_literal("xsd:dateTime", datetime.combine(value, datetime.min.time()))
        if isinstance(value, bool):
            return self._typed_literal("xsd:boolean", value)
        if isinstance(value, int):
            return self._typed_literal("xsd:integer", value)
        if isinstance(value, float):
            return self._typed_literal("xsd:decimal", value)

        return value

    def _typed_literal(self, xsd_type: str, value: Any) -> dict[str, str]:
        if isinstance(value, bool):
            rendered = str(value).lower()
        elif isinstance(value, datetime):
            rendered = value.isoformat()
        else:
            rendered = str(value)
        return {"@type": xsd_type, "@value": rendered}

    def _validate_instance(self, instance: Any) -> None:
        """Validate required generated fields before adding/serializing an instance."""
        if not is_dataclass(instance):
            return

        for field_info in fields(instance):
            if field_info.name in ("CLASS_IRI", "NAMESPACE_PREFIX"):
                continue

            metadata = field_info.metadata or {}
            if not metadata:
                continue

            value = getattr(instance, field_info.name)
            required = bool(metadata.get("required", False))
            cardinality = metadata.get("cardinality")

            if required:
                if value is None:
                    raise ValueError(
                        f"{type(instance).__name__}.{field_info.name} is required but was not provided."
                    )
                if isinstance(value, list) and len(value) == 0:
                    raise ValueError(
                        f"{type(instance).__name__}.{field_info.name} requires at least one value."
                    )

            if cardinality in {"exactly_one", "zero_or_one"} and isinstance(value, list):
                raise ValueError(
                    f"{type(instance).__name__}.{field_info.name} does not accept multiple values."
                )

            if isinstance(value, list):
                for item in value:
                    if is_dataclass(item):
                        self._validate_instance(item)
            elif is_dataclass(value):
                self._validate_instance(value)

    @classmethod
    def from_jsonld(
        cls,
        json_str: str,
        *,
        extra_classes: list[type] | None = None,
        kb_prefix: str = "http://example.org/kb/",
    ) -> tuple[CASEGraph, list[Any]]:
        """Deserialize a JSON-LD string into typed Python objects.

        Returns a tuple of (CASEGraph, list_of_typed_objects). Each object in
        the ``@graph`` array is matched to a generated Python class by its
        ``@type`` IRI.  Objects whose type cannot be resolved are returned as
        plain dicts and still added to the graph.

        Args:
            json_str: A JSON-LD string containing ``@context`` and ``@graph``.
            extra_classes: Additional classes (e.g. extension dataclasses)
                to include in the type registry alongside the built-in ones.
            kb_prefix: Knowledge-base prefix for the returned graph.
        """
        iri_to_class = _build_class_registry(extra_classes)

        doc = json.loads(json_str)
        context = doc.get("@context", {})
        graph_items = doc.get("@graph", [])

        graph = cls(kb_prefix=kb_prefix, extra_context=context if isinstance(context, dict) else None)

        typed_objects: list[Any] = []
        for raw in graph_items:
            obj = _rehydrate(raw, iri_to_class, context if isinstance(context, dict) else {})
            typed_objects.append(obj)

            if is_dataclass(obj) and not isinstance(obj, type):
                obj_id = raw.get("@id", graph._mint_id(obj))
                graph._id_map[_builtin_id(obj)] = obj_id
                graph._objects.append(raw)
            else:
                graph._objects.append(raw)

        return graph, typed_objects

    def _compact_iri(self, iri: str) -> str:
        """Compact a full IRI to prefixed form using the context."""
        for prefix, ns in self._context.items():
            if iri.startswith(ns):
                local = iri[len(ns):]
                return f"{prefix}:{local}"
        return iri


def _build_class_registry(extra_classes: list[type] | None = None) -> dict[str, type]:
    """Build a mapping from CLASS_IRI -> Python dataclass for all generated classes."""
    registry: dict[str, type] = {}

    import importlib
    module_names = [
        "case_uco.case.investigation",
        "case_uco.uco.action",
        "case_uco.uco.analysis",
        "case_uco.uco.configuration",
        "case_uco.uco.core",
        "case_uco.uco.identity",
        "case_uco.uco.location",
        "case_uco.uco.marking",
        "case_uco.uco.observable",
        "case_uco.uco.pattern",
        "case_uco.uco.role",
        "case_uco.uco.time",
        "case_uco.uco.tool",
        "case_uco.uco.types",
        "case_uco.uco.victim",
    ]

    for mod_name in module_names:
        try:
            mod = importlib.import_module(mod_name)
        except ImportError:
            continue
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if isinstance(attr, type) and is_dataclass(attr) and hasattr(attr, "CLASS_IRI"):
                registry[attr.CLASS_IRI] = attr

    if extra_classes:
        for cls in extra_classes:
            if hasattr(cls, "CLASS_IRI"):
                registry[cls.CLASS_IRI] = cls

    return registry


def _expand_iri(compact: str, context: dict[str, str]) -> str:
    """Expand a prefixed IRI (e.g. 'uco-tool:Tool') to a full IRI."""
    if "://" in compact:
        return compact
    if ":" in compact:
        prefix, local = compact.split(":", 1)
        ns = context.get(prefix)
        if ns:
            return ns + local
    return compact


def _rehydrate(
    raw: dict[str, Any],
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> Any:
    """Convert a JSON-LD dict back to a typed Python dataclass instance."""
    type_value = raw.get("@type")
    if not type_value:
        return raw

    type_iri = _expand_iri(type_value, context)
    cls = iri_to_class.get(type_iri)
    if cls is None:
        return raw

    if not is_dataclass(cls):
        return raw

    jsonld_key_to_field: dict[str, tuple[str, Field]] = {}
    for f in fields(cls):
        key = f.metadata.get("jsonld_key")
        if key:
            jsonld_key_to_field[key] = (f.name, f)

    kwargs: dict[str, Any] = {}
    for key, value in raw.items():
        if key in ("@id", "@type"):
            continue
        field_info = jsonld_key_to_field.get(key)
        if field_info is None:
            continue
        field_name, f = field_info
        kwargs[field_name] = _coerce_value(value, f, iri_to_class, context)

    try:
        return cls(**kwargs)
    except (TypeError, ValueError):
        return raw


def _coerce_value(
    value: Any,
    field_info: Field,
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> Any:
    """Coerce a JSON-LD value back to the Python type expected by the field."""
    if isinstance(value, dict):
        if "@value" in value:
            raw_val = value["@value"]
            xsd_type = value.get("@type", "")
            if "boolean" in xsd_type:
                return raw_val == "true" or raw_val is True
            if "integer" in xsd_type:
                return int(raw_val)
            if "decimal" in xsd_type or "float" in xsd_type or "double" in xsd_type:
                return float(raw_val)
            if "dateTime" in xsd_type:
                return datetime.fromisoformat(str(raw_val))
            return raw_val
        if "@type" in value:
            return _rehydrate(value, iri_to_class, context)
        if "@id" in value:
            return value["@id"]
        return value

    if isinstance(value, list):
        return [_coerce_value(item, field_info, iri_to_class, context) for item in value]

    return value
