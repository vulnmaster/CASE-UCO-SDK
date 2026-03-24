"""Python code generation backend — emits dataclass-based CASE/UCO classes."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.backends.base import CodegenBackend
from case_uco_generator.schema_model import (
    OntologyClass,
    OntologyProperty,
    OntologyVocab,
    compact_ontology_iri,
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

        return created

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
        lines.append("from dataclasses import dataclass, field")
        lines.append("from typing import TYPE_CHECKING, Any, Optional")
        lines.append("")

        # Collect cross-module imports needed by parent classes and property types
        runtime_imports, type_imports = self._collect_imports(current_module, classes)
        for imp in sorted(runtime_imports):
            lines.append(imp)
        if runtime_imports:
            lines.append("")

        if type_imports:
            lines.append("if TYPE_CHECKING:")
            for imp in sorted(type_imports):
                lines.append(f"    {imp}")
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
    ) -> tuple[set[str], set[str]]:
        """Collect import statements for cross-module references.

        Returns (runtime_imports, type_checking_imports) to avoid circular imports.
        Runtime imports are for parent class inheritance (required at class definition).
        Type-checking imports are for property type annotations (only needed for mypy).
        """
        runtime_imports: set[str] = set()
        type_imports: set[str] = set()
        local_names = {c.name for c in classes}

        for cls in classes:
            # Parent classes from other modules — MUST be runtime imports
            for parent_iri in cls.parent_iris:
                parent_cls = self.schema.resolve_class(parent_iri)
                if parent_cls and parent_cls.name not in local_names:
                    parent_top, parent_mod = parent_cls.module.split(".", 1)
                    runtime_imports.add(
                        f"from case_uco.{parent_top}.{parent_mod} import {parent_cls.name}"
                    )

            # Property types from other modules — can be TYPE_CHECKING only
            for prop in cls.properties:
                if prop.range_is_class:
                    range_cls = self.schema.resolve_class(prop.range_iri)
                    if range_cls and range_cls.name not in local_names:
                        range_top, range_mod = range_cls.module.split(".", 1)
                        imp = f"from case_uco.{range_top}.{range_mod} import {range_cls.name}"
                        if imp not in runtime_imports:
                            type_imports.add(imp)

        return runtime_imports, type_imports

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
