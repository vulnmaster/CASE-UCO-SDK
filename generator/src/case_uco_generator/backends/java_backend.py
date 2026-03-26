"""Java code generation backend — emits CASE/UCO classes using Apache Jena."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.backends.base import CodegenBackend
from case_uco_generator.schema_model import (
    OntologyClass,
    OntologyProperty,
    OntologyVocab,
    compact_ontology_iri,
)


class JavaBackend(CodegenBackend):
    """Generate Java classes for CASE/UCO."""

    def generate(self) -> list[Path]:
        created: list[Path] = []

        for module_key, class_iris in sorted(self.schema.modules.items()):
            top, mod = module_key.split(".", 1)
            safe_top = self.safe_identifier(top, "java")
            safe_mod = self.safe_identifier(mod, "java")
            pkg_dir = self.output_dir / safe_top / safe_mod
            pkg_dir.mkdir(parents=True, exist_ok=True)

            classes = sorted(
                [self.schema.classes[iri] for iri in class_iris if iri in self.schema.classes],
                key=lambda c: c.name,
            )

            module_vocabs = self._vocabs_for_module(classes)

            for cls in classes:
                file_path = pkg_dir / f"{cls.name}.java"
                content = self._render_class_file(top, mod, cls, module_vocabs)
                file_path.write_text(content, encoding="utf-8")
                created.append(file_path)

            for vocab in module_vocabs:
                file_path = pkg_dir / f"{vocab.name}.java"
                content = self._render_vocab_file(top, mod, vocab)
                file_path.write_text(content, encoding="utf-8")
                created.append(file_path)

        exhaust_path = self._emit_exhaustive_test()
        created.append(exhaust_path)

        return created

    def _emit_exhaustive_test(self) -> Path:
        """Generate a test that instantiates every generated class."""
        test_dir = self.output_dir.parent.parent.parent.parent / "test" / "java" / "org" / "caseontology"
        test_dir.mkdir(parents=True, exist_ok=True)
        path = test_dir / "ExhaustiveInstantiationTest.java"

        lines: list[str] = []
        lines.append("// Auto-generated — instantiates every CASE/UCO class to verify the object model.")
        lines.append("package org.caseontology;")
        lines.append("")

        core_classes = [
            c for c in self.schema.classes.values()
            if not c.module.startswith("ext.")
        ]

        imports: list[str] = []
        for cls in sorted(core_classes, key=lambda c: (c.module, c.name)):
            top, mod = cls.module.split(".", 1)
            safe_top = self.safe_identifier(top, "java")
            safe_mod = self.safe_identifier(mod, "java")
            imports.append(f"import org.caseontology.{safe_top}.{safe_mod}.{cls.name};")

        for imp in sorted(set(imports)):
            lines.append(imp)
        lines.append("import org.junit.Test;")
        lines.append("import static org.junit.Assert.*;")
        lines.append("")
        lines.append("public class ExhaustiveInstantiationTest {")
        lines.append("")
        lines.append("    @Test")
        lines.append("    public void testAllClassesCanBeInstantiated() {")
        lines.append("        CaseGraph graph = new CaseGraph();")

        for cls in sorted(core_classes, key=lambda c: (c.module, c.name)):
            lines.append(f"        graph.add(new {cls.name}());")

        lines.append(f"        assertEquals({len(core_classes)}, graph.size());")
        lines.append("    }")
        lines.append("}")

        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def _vocabs_for_module(self, classes: list[OntologyClass]) -> list[OntologyVocab]:
        vocab_iris: set[str] = set()
        for cls in classes:
            for prop in cls.properties:
                if prop.is_vocab_type and prop.range_iri in self.schema.vocabs:
                    vocab_iris.add(prop.range_iri)
        return [self.schema.vocabs[iri] for iri in sorted(vocab_iris)]

    def _render_class_file(
        self,
        top: str,
        mod: str,
        cls: OntologyClass,
        module_vocabs: list[OntologyVocab],
    ) -> str:
        pkg = f"org.caseontology.{self.safe_identifier(top, 'java')}.{self.safe_identifier(mod, 'java')}"
        current_module = f"{top}.{mod}"
        lines: list[str] = []
        lines.append(f"// Auto-generated CASE/UCO ontology class — do not edit manually.")
        lines.append(f"package {pkg};")
        lines.append("")
        lines.append("import java.util.ArrayList;")
        lines.append("import java.util.List;")
        for imp in sorted(self._collect_imports(current_module, cls, module_vocabs)):
            lines.append(imp)
        lines.append("")

        parent_name = cls.all_parent_names[0] if cls.all_parent_names else None
        extends = f" extends {parent_name}" if parent_name else ""
        desc = cls.description[:200] if cls.description else cls.name

        lines.append(f"/** {desc} */")
        lines.append(f"public class {cls.name}{extends} {{")
        lines.append(f'    public static final String CLASS_IRI = "{cls.iri}";')
        lines.append(f'    public static final String NAMESPACE_PREFIX = "{cls.namespace_prefix}";')
        lines.append("")

        for prop in cls.properties:
            java_type = self._java_type(prop)
            field_name = self.to_camel_case(prop.name)
            field_name = self.safe_identifier(field_name, "java")
            if prop.cardinality.is_required:
                lines.append(f"    @org.caseontology.CaseRequired")
            lines.append(f"    private {java_type} {field_name};")

        lines.append("")

        # Constructor
        lines.append(f"    public {cls.name}() {{")
        for prop in cls.properties:
            if prop.cardinality.is_list:
                field_name = self.to_camel_case(prop.name)
                field_name = self.safe_identifier(field_name, "java")
                lines.append(f"        this.{field_name} = new ArrayList<>();")
        lines.append("    }")
        lines.append("")

        inherited_property_names = self._inherited_property_names(cls)

        # Getters/setters
        for prop in cls.properties:
            java_type = self._java_type(prop)
            field_name = self.to_camel_case(prop.name)
            field_name = self.safe_identifier(field_name, "java")
            accessor_base = self._java_accessor_base(prop.name, inherited_property_names)
            getter_name = f"get{accessor_base}"
            setter_name = f"set{accessor_base}"

            lines.append(f"    public {java_type} {getter_name}() {{ return this.{field_name}; }}")
            lines.append(f"    public {cls.name} {setter_name}({java_type} value) {{ this.{field_name} = value; return this; }}")
            lines.append("")

        lines.append("}")
        return "\n".join(lines)

    def _collect_imports(
        self,
        current_module: str,
        cls: OntologyClass,
        module_vocabs: list[OntologyVocab],
    ) -> set[str]:
        imports: set[str] = set()
        local_vocab_names = {vocab.name for vocab in module_vocabs}

        for parent_iri in cls.parent_iris:
            parent_cls = self.schema.resolve_class(parent_iri)
            if parent_cls and parent_cls.module != current_module:
                imports.add(self._java_import(parent_cls.module, parent_cls.name))

        for prop in cls.properties:
            if prop.is_xsd_type or prop.is_union:
                continue

            range_cls = self.schema.resolve_class(prop.range_iri)
            if range_cls:
                if range_cls.module != current_module:
                    imports.add(self._java_import(range_cls.module, range_cls.name))
                continue

            if prop.range_iri in self.schema.vocabs:
                vocab_name = prop.type_name_for("java")
                if vocab_name in local_vocab_names:
                    continue
                module = self._module_path_for_iri(prop.range_iri)
                if module and module != current_module:
                    imports.add(self._java_import(module, vocab_name))

        return imports

    def _inherited_property_names(self, cls: OntologyClass) -> set[str]:
        names: set[str] = set()
        for parent_iri in cls.parent_iris:
            parent = self.schema.resolve_class(parent_iri)
            if not parent:
                continue
            names.update(prop.name for prop in parent.properties)
            names.update(self._inherited_property_names(parent))
        return names

    def _java_accessor_base(self, prop_name: str, inherited_property_names: set[str]) -> str:
        base = self.to_pascal_case(prop_name)
        if prop_name in inherited_property_names or prop_name in {"class"}:
            return f"{base}Value"
        return base

    def _module_path_for_iri(self, iri: str) -> str | None:
        compact = compact_ontology_iri(iri)
        if ":" not in compact or "-" not in compact.split(":", 1)[0]:
            return None
        prefix = compact.split(":", 1)[0]
        top, mod = prefix.split("-", 1)
        return f"{top}.{mod}"

    def _java_import(self, module_key: str, type_name: str) -> str:
        top, mod = module_key.split(".", 1)
        safe_top = self.safe_identifier(top, "java")
        safe_mod = self.safe_identifier(mod, "java")
        return f"import org.caseontology.{safe_top}.{safe_mod}.{type_name};"

    def _render_vocab_file(self, top: str, mod: str, vocab: OntologyVocab) -> str:
        pkg = f"org.caseontology.{top}.{mod}"
        lines: list[str] = []
        lines.append(f"// Auto-generated CASE/UCO vocabulary — do not edit manually.")
        lines.append(f"package {pkg};")
        lines.append("")
        lines.append(f"/** Vocabulary: {vocab.name} */")
        lines.append(f"public final class {vocab.name} {{")
        lines.append(f'    public static final String IRI = "{vocab.iri}";')
        for member in vocab.members:
            attr = self._vocab_attr_name(member)
            lines.append(f'    public static final String {attr} = "{member}";')
        lines.append("")
        lines.append(f"    private {vocab.name}() {{}}")
        lines.append("}")
        return "\n".join(lines)

    def _vocab_attr_name(self, member: str) -> str:
        name = member.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        if name and name[0].isdigit():
            name = f"_{name}"
        return name.upper()

    def _java_type(self, prop: OntologyProperty) -> str:
        base = prop.type_name_for("java")
        # Box primitives for nullable
        boxed = {
            "boolean": "Boolean", "int": "Integer", "long": "Long",
            "float": "Float", "double": "Double", "short": "Short", "byte": "Byte",
        }
        if prop.cardinality.is_list:
            return f"List<{boxed.get(base, base)}>"
        if not prop.cardinality.is_required and base in boxed:
            return boxed[base]
        return base
