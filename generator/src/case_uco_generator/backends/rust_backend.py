"""Rust code generation backend — emits CASE/UCO structs with builder pattern."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.backends.base import CodegenBackend
from case_uco_generator.schema_model import (
    OntologyClass,
    OntologyVocab,
    compact_ontology_iri,
)


class RustBackend(CodegenBackend):
    """Generate Rust structs for CASE/UCO."""

    def generate(self) -> list[Path]:
        created: list[Path] = []

        for module_key, class_iris in sorted(self.schema.modules.items()):
            top, mod = module_key.split(".", 1)
            mod_dir = self.output_dir / top
            mod_dir.mkdir(parents=True, exist_ok=True)
            file_path = mod_dir / f"{mod}.rs"

            classes = sorted(
                [self.schema.classes[iri] for iri in class_iris if iri in self.schema.classes],
                key=lambda c: c.name,
            )

            module_vocabs = self._vocabs_for_module(classes)
            content = self._render_module(top, mod, classes, module_vocabs)
            file_path.write_text(content, encoding="utf-8")
            created.append(file_path)

        # Generate mod.rs for each top-level
        for top in ("uco", "case"):
            mod_dir = self.output_dir / top
            mod_dir.mkdir(parents=True, exist_ok=True)
            mods = sorted(set(
                k.split(".", 1)[1]
                for k in self.schema.modules
                if k.startswith(f"{top}.")
            ))
            mod_rs = mod_dir / "mod.rs"
            mod_rs.write_text(
                "// Auto-generated module declarations\n\n"
                + "\n".join(f"pub mod {m};" for m in mods)
                + "\n",
                encoding="utf-8",
            )
            created.append(mod_rs)

        # Generate top-level lib.rs
        lib_rs = self.output_dir / "lib.rs"
        lib_rs.write_text(
            "// Auto-generated CASE/UCO standard library for Rust\n\n"
            "pub mod graph;\n"
            "pub mod uco;\n"
            "pub mod case;\n",
            encoding="utf-8",
        )
        created.append(lib_rs)

        return created

    def _vocabs_for_module(self, classes: list[OntologyClass]) -> list[OntologyVocab]:
        vocab_iris: set[str] = set()
        for cls in classes:
            for prop in cls.properties:
                if prop.is_vocab_type and prop.range_iri in self.schema.vocabs:
                    vocab_iris.add(prop.range_iri)
        return [self.schema.vocabs[iri] for iri in sorted(vocab_iris)]

    def _render_module(
        self, top: str, mod: str, classes: list[OntologyClass], vocabs: list[OntologyVocab]
    ) -> str:
        current_module = f"{top}.{mod}"
        lines: list[str] = []
        lines.append(f"//! Auto-generated {top}-{mod} types for the CASE/UCO ontology.")
        lines.append("")
        lines.append("use serde::Serialize;")
        lines.append("use crate::graph::CaseObject;")
        imports = self._collect_imports(current_module, classes, vocabs)
        if imports:
            lines.append("")
            for imp in sorted(imports):
                lines.append(imp)
        lines.append("")

        for vocab in vocabs:
            lines.extend(self._render_vocab(vocab))
            lines.append("")

        for cls in classes:
            lines.extend(self._render_struct(cls))
            lines.append("")

        return "\n".join(lines)

    def _collect_imports(
        self,
        current_module: str,
        classes: list[OntologyClass],
        vocabs: list[OntologyVocab],
    ) -> set[str]:
        imports: set[str] = set()
        local_names = {cls.name for cls in classes} | {vocab.name for vocab in vocabs}

        for cls in classes:
            for prop in cls.properties:
                if prop.is_xsd_type or prop.is_union:
                    continue

                type_name = prop.type_name_for("rust")
                if type_name in local_names:
                    continue

                module_path = self._module_path_for_iri(prop.range_iri)
                if module_path and module_path != current_module:
                    imports.add(f"use crate::{module_path}::{type_name};")

        return imports

    def _module_path_for_iri(self, iri: str) -> str | None:
        compact = compact_ontology_iri(iri)
        if ":" not in compact or "-" not in compact.split(":", 1)[0]:
            return None
        prefix = compact.split(":", 1)[0]
        top, mod = prefix.split("-", 1)
        return f"{top}::{mod}"

    def _render_vocab(self, vocab: OntologyVocab) -> list[str]:
        lines: list[str] = []
        lines.append(f"/// Vocabulary: {vocab.name}")
        lines.append("#[derive(Debug, Clone, Serialize)]")
        lines.append(f"pub struct {vocab.name};")
        lines.append("")
        lines.append(f"impl {vocab.name} {{")
        lines.append(f'    pub const IRI: &\'static str = "{vocab.iri}";')
        for member in vocab.members:
            attr = self._vocab_attr_name(member)
            lines.append(f'    pub const {attr}: &\'static str = "{member}";')
        lines.append("}")
        return lines

    def _vocab_attr_name(self, member: str) -> str:
        name = member.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        if name and name[0].isdigit():
            name = f"_{name}"
        return name.upper()

    def _render_struct(self, cls: OntologyClass) -> list[str]:
        lines: list[str] = []
        desc = cls.description[:200] if cls.description else cls.name

        lines.append(f"/// {desc}")
        lines.append("#[derive(Debug, Clone, Serialize)]")
        lines.append(f"pub struct {cls.name} {{")
        lines.append("    #[serde(skip_serializing)]")
        lines.append(f"    pub class_iri: &'static str,")

        for prop in cls.properties:
            field_name = self.to_snake_case(prop.name)
            field_name = self.safe_identifier(field_name, "rust")
            rs_type = self._rust_type(prop)
            lines.append(f'    #[serde(rename = "{compact_ontology_iri(prop.iri)}")]')
            lines.append(f"    pub {field_name}: {rs_type},")

        lines.append("}")
        lines.append("")

        # Builder impl
        lines.append(f"impl {cls.name} {{")
        lines.append(f'    pub const CLASS_IRI: &\'static str = "{cls.iri}";')
        lines.append(f'    pub const NAMESPACE_PREFIX: &\'static str = "{cls.namespace_prefix}";')
        lines.append("")
        lines.append(f"    pub fn builder() -> {cls.name}Builder {{")
        lines.append(f"        {cls.name}Builder {{")
        for prop in cls.properties:
            field_name = self.to_snake_case(prop.name)
            field_name = self.safe_identifier(field_name, "rust")
            default_value = "Vec::new()" if prop.cardinality.is_list else "None"
            lines.append(f"            {field_name}: {default_value},")
        lines.append("        }")
        lines.append("    }")
        lines.append("}")
        lines.append("")

        # Builder struct
        lines.append(f"#[derive(Debug, Default, Clone)]")
        lines.append(f"pub struct {cls.name}Builder {{")
        for prop in cls.properties:
            field_name = self.to_snake_case(prop.name)
            field_name = self.safe_identifier(field_name, "rust")
            rs_type = self._rust_builder_type(prop)
            lines.append(f"    {field_name}: {rs_type},")
        lines.append("}")
        lines.append("")

        lines.append(f"impl {cls.name}Builder {{")
        for prop in cls.properties:
            field_name = self.to_snake_case(prop.name)
            field_name = self.safe_identifier(field_name, "rust")
            base_type = prop.type_name_for("rust")

            if prop.cardinality.is_list:
                param_type = f"Vec<{base_type}>"
            else:
                param_type = base_type

            lines.append(f"    pub fn {field_name}(mut self, value: {param_type}) -> Self {{")
            if prop.cardinality.is_list:
                lines.append(f"        self.{field_name} = value;")
            else:
                lines.append(f"        self.{field_name} = Some(value);")
            lines.append("        self")
            lines.append("    }")
            lines.append("")

        lines.append(f"    pub fn build(self) -> {cls.name} {{")
        lines.append(f"        {cls.name} {{")
        lines.append(f'            class_iri: {cls.name}::CLASS_IRI,')
        for prop in cls.properties:
            field_name = self.to_snake_case(prop.name)
            field_name = self.safe_identifier(field_name, "rust")
            if prop.cardinality.is_list:
                lines.append(f"            {field_name}: self.{field_name},")
            elif prop.cardinality.is_required:
                lines.append(
                    f'            {field_name}: self.{field_name}.expect("missing required field: {field_name}"),'
                )
            else:
                lines.append(f"            {field_name}: self.{field_name},")
        lines.append("        }")
        lines.append("    }")
        lines.append("}")
        lines.append("")

        lines.append(f"impl CaseObject for {cls.name} {{")
        lines.append(f'    fn class_iri() -> &\'static str {{ {cls.name}::CLASS_IRI }}')
        lines.append(f'    fn type_name() -> &\'static str {{ "{cls.name}" }}')
        lines.append("}")

        return lines

    def _rust_type(self, prop: OntologyProperty) -> str:
        base = prop.type_name_for("rust")
        if prop.cardinality.is_list:
            return f"Vec<{base}>"
        if not prop.cardinality.is_required:
            return f"Option<{base}>"
        return base

    def _rust_builder_type(self, prop: OntologyProperty) -> str:
        base = prop.type_name_for("rust")
        if prop.cardinality.is_list:
            return f"Vec<{base}>"
        return f"Option<{base}>"
