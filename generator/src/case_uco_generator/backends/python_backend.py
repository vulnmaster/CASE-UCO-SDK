"""Python code generation backend — emits dataclass-based CASE/UCO classes."""

from __future__ import annotations

import json
from pathlib import Path

from case_uco_generator.backends.base import CodegenBackend
from case_uco_generator.schema_model import (
    OntologyClass,
    OntologyProperty,
    OntologyVocab,
    compact_ontology_iri,
    iri_local_name,
)


class PythonBackend(CodegenBackend):
    """Generate Python dataclass modules for CASE/UCO."""

    def generate(self) -> list[Path]:
        created: list[Path] = []

        for module_key, class_iris in sorted(self.schema.modules.items()):
            top, mod = module_key.split(".", 1)
            mod_dir = self.output_dir / top
            file_path = mod_dir / f"{mod}.py"
            mod_dir.mkdir(parents=True, exist_ok=True)

            classes = [
                self.schema.classes[iri]
                for iri in class_iris
                if iri in self.schema.classes
            ]
            classes.sort(key=lambda c: c.name)

            # Collect vocabs used by properties in this module
            module_vocabs = self._vocabs_for_module(classes)

            content = self._render_module(top, mod, classes, module_vocabs)
            file_path.write_text(content, encoding="utf-8")
            created.append(file_path)

        # Write __init__.py files — list available modules without eagerly importing
        for top in ("uco", "case"):
            init_path = self.output_dir / top / "__init__.py"
            init_path.parent.mkdir(parents=True, exist_ok=True)
            modules = sorted(set(
                k.split(".", 1)[1]
                for k in self.schema.modules
                if k.startswith(f"{top}.")
            ))
            module_list = ", ".join(f'"{m}"' for m in modules)
            init_path.write_text(
                f'"""Auto-generated {top.upper()} namespace modules."""\n\n'
                f"__all__ = [{module_list}]\n",
                encoding="utf-8",
            )
            created.append(init_path)

        # Write top-level __init__.py
        top_init = self.output_dir / "__init__.py"
        top_init.write_text(
            '"""CASE/UCO Standard Library — construct and serialize CASE/UCO ontology graphs."""\n\n'
            "from case_uco.graph import CASEGraph\n\n"
            '__all__ = ["CASEGraph"]\n'
            '__version__ = "0.1.0"\n',
            encoding="utf-8",
        )
        created.append(top_init)

        # Emit _registry.json for runtime introspection
        registry_path = self._emit_registry()
        created.append(registry_path)

        return created

    def _emit_registry(self) -> Path:
        """Serialize the ontology schema to _registry.json for runtime discovery."""
        registry: dict = {
            "modules": sorted(self.schema.modules.keys()),
            "classes": {},
            "vocabs": {},
        }

        for cls in sorted(self.schema.classes.values(), key=lambda c: c.name):
            all_props = self.schema.resolve_all_properties(cls)
            props_data = []
            for prop in all_props:
                props_data.append({
                    "name": prop.name,
                    "type": iri_local_name(prop.range_iri),
                    "type_iri": prop.range_iri,
                    "cardinality": prop.cardinality.value,
                    "required": prop.cardinality.is_required,
                    "description": prop.description,
                })
            registry["classes"][cls.name] = {
                "iri": cls.iri,
                "module": cls.module,
                "description": cls.description,
                "parents": [iri_local_name(p) for p in cls.parent_iris],
                "is_facet": cls.is_facet,
                "properties": props_data,
            }

        for vocab in sorted(self.schema.vocabs.values(), key=lambda v: v.name):
            members = [
                iri_local_name(m) if "/" in m or "#" in m else m
                for m in vocab.members
            ]
            registry["vocabs"][vocab.name] = {
                "iri": vocab.iri,
                "members": members,
            }

        path = self.output_dir / "_registry.json"
        path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def _vocabs_for_module(
        self, classes: list[OntologyClass]
    ) -> list[OntologyVocab]:
        vocab_iris: set[str] = set()
        for cls in classes:
            for prop in cls.properties:
                if prop.is_vocab_type and prop.range_iri in self.schema.vocabs:
                    vocab_iris.add(prop.range_iri)
        return [self.schema.vocabs[iri] for iri in sorted(vocab_iris)]

    def _render_module(
        self,
        top: str,
        mod: str,
        classes: list[OntologyClass],
        vocabs: list[OntologyVocab],
    ) -> str:
        current_module = f"{top}.{mod}"
        lines: list[str] = []
        lines.append(f'"""Auto-generated {top}-{mod} classes for the CASE/UCO ontology."""')
        lines.append("")
        lines.append("from __future__ import annotations")
        lines.append("")

        needs_field = any(prop for cls in classes for prop in cls.properties)
        needs_optional = any(
            not prop.cardinality.is_list and not prop.cardinality.is_required
            for cls in classes
            for prop in cls.properties
        )

        dc_parts = ["dataclass"]
        if needs_field:
            dc_parts.append("field")
        lines.append(f"from dataclasses import {', '.join(dc_parts)}")

        if needs_optional:
            lines.append("from typing import Optional")

        lines.append("")

        runtime_imports = self._collect_imports(current_module, classes)
        for imp in sorted(runtime_imports):
            lines.append(imp)
        if runtime_imports:
            lines.append("")

        lines.append("")

        # Generate vocab enums
        for vocab in vocabs:
            lines.extend(self._render_vocab(vocab))
            lines.append("")

        # Generate class definitions (topologically sorted so parents come first)
        sorted_classes = self._topo_sort(classes, current_module)
        for cls in sorted_classes:
            lines.extend(self._render_class(cls))
            lines.append("")

        return "\n".join(lines)

    def _collect_imports(
        self, current_module: str, classes: list[OntologyClass]
    ) -> set[str]:
        """Collect runtime import statements for cross-module parent classes.

        Only the parent class actually used as the Python base class is imported.
        Property-type annotations are left as forward-reference strings
        (``from __future__ import annotations`` is always present).
        """
        runtime_imports: set[str] = set()
        local_names = {c.name for c in classes}

        for cls in classes:
            parent_name = cls.all_parent_names[0] if cls.all_parent_names else None
            if parent_name and parent_name not in local_names:
                for parent_iri in cls.parent_iris:
                    parent_cls = self.schema.resolve_class(parent_iri)
                    if parent_cls and parent_cls.name == parent_name:
                        parent_top, parent_mod = parent_cls.module.split(".", 1)
                        runtime_imports.add(
                            f"from case_uco.{parent_top}.{parent_mod} import {parent_cls.name}"
                        )
                        break

        return runtime_imports

    def _topo_sort(
        self, classes: list[OntologyClass], current_module: str
    ) -> list[OntologyClass]:
        """Sort classes so parent classes appear before children within the same module."""
        local_names = {c.name: c for c in classes}
        sorted_list: list[OntologyClass] = []
        visited: set[str] = set()

        def visit(cls: OntologyClass) -> None:
            if cls.name in visited:
                return
            visited.add(cls.name)
            for parent_iri in cls.parent_iris:
                parent = self.schema.resolve_class(parent_iri)
                if parent and parent.name in local_names:
                    visit(parent)
            sorted_list.append(cls)

        for cls in classes:
            visit(cls)

        return sorted_list

    def _render_vocab(self, vocab: OntologyVocab) -> list[str]:
        lines: list[str] = []
        lines.append(f"class {vocab.name}:")
        lines.append(f'    """Vocabulary: {vocab.name}"""')
        lines.append(f'    IRI = "{vocab.iri}"')
        lines.append("")
        for member in vocab.members:
            attr_name = self._vocab_attr_name(member)
            lines.append(f'    {attr_name} = "{member}"')
        lines.append("")
        return lines

    def _vocab_attr_name(self, member: str) -> str:
        name = member.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        if name and name[0].isdigit():
            name = f"_{name}"
        return name.upper()

    def _render_class(self, cls: OntologyClass) -> list[str]:
        lines: list[str] = []

        parent_name = cls.all_parent_names[0] if cls.all_parent_names else None
        base = parent_name if parent_name else ""
        decorator = "@dataclass"

        if base:
            lines.append(decorator)
            lines.append(f"class {cls.name}({base}):")
        else:
            lines.append(decorator)
            lines.append(f"class {cls.name}:")

        # Docstring
        desc = cls.description[:200] if cls.description else cls.name
        lines.append(f'    """{desc}"""')
        lines.append("")

        # Class-level constants
        lines.append(f'    CLASS_IRI: str = "{cls.iri}"')
        lines.append(f'    NAMESPACE_PREFIX: str = "{cls.namespace_prefix}"')
        lines.append("")

        # All fields get defaults to avoid dataclass inheritance ordering issues.
        # Required fields are validated at graph creation time, not at construction.
        for prop in cls.properties:
            field_name = self.safe_identifier(self.to_snake_case(prop.name), "python")
            type_str = self._python_type(prop)
            default = self._python_default(prop)
            metadata = self._field_metadata(prop)
            lines.append(f"    {field_name}: {type_str} = {default}{metadata}")

        lines.append("")
        return lines

    def _python_type(self, prop: OntologyProperty) -> str:
        base_type = prop.type_name_for("python")
        if prop.cardinality.is_list:
            return f"list[{base_type}]"
        if not prop.cardinality.is_required:
            return f"Optional[{base_type}]"
        return base_type

    def _python_default(self, prop: OntologyProperty) -> str:
        if prop.cardinality.is_list:
            return "field(default_factory=list"
        return "field(default=None"

    def _field_metadata(self, prop: OntologyProperty) -> str:
        metadata = {
            "jsonld_key": compact_ontology_iri(prop.iri),
            "required": prop.cardinality.is_required,
            "cardinality": prop.cardinality.value,
            "range_iri": prop.range_iri,
            "alternate_range_iris": prop.alternate_range_iris,
        }
        return f', metadata={metadata})'
