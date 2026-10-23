"""C# code generation backend — emits CASE/UCO classes using dotNetRdf."""

from __future__ import annotations

import json
from pathlib import Path

from case_uco_generator.backends.base import VOCABULARY_MODULE_DOC, CodegenBackend
from case_uco_generator.schema_model import (
    OntologyClass,
    OntologyProperty,
    OntologyVocab,
    compact_ontology_iri,
)


class CSharpBackend(CodegenBackend):
    """Generate C# classes for CASE/UCO."""

    def generate(self) -> list[Path]:
        created: list[Path] = []

        for module_key, class_iris in sorted(self.schema.modules.items()):
            top, mod = module_key.split(".", 1)
            ns_dir = self.output_dir / self.to_pascal_case(top)
            ns_dir.mkdir(parents=True, exist_ok=True)
            file_path = ns_dir / f"{self.to_pascal_case(mod)}.cs"

            classes = sorted(
                [self.schema.classes[iri] for iri in class_iris if iri in self.schema.classes],
                key=lambda c: c.name,
            )

            module_vocabs = self._vocabs_for_module(classes)
            content = self._render_module(top, mod, classes, module_vocabs)
            file_path.write_text(content, encoding="utf-8")
            created.append(file_path)

        for top, vocabs in self.vocabularies_by_top().items():
            ns_dir = self.output_dir / self.to_pascal_case(top)
            ns_dir.mkdir(parents=True, exist_ok=True)
            vocab_path = ns_dir / "Vocabulary.cs"
            vocab_path.write_text(self._render_vocabulary_file(top, vocabs), encoding="utf-8")
            created.append(vocab_path)

        exhaust_path = self._emit_exhaustive_test()
        created.append(exhaust_path)

        return created

    def _emit_exhaustive_test(self) -> Path:
        """Generate a test that instantiates every generated class."""
        tests_dir = self.output_dir.parent / "CaseUco.Tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        path = tests_dir / "ExhaustiveInstantiationTests.cs"

        lines: list[str] = []
        lines.append("// Auto-generated — instantiates every CASE/UCO class to verify the object model.")
        lines.append("using System.Collections.Generic;")
        lines.append("using Xunit;")
        lines.append("")
        lines.append("namespace CaseUco.Tests")
        lines.append("{")
        lines.append("    public class ExhaustiveInstantiationTests")
        lines.append("    {")
        lines.append("        [Fact]")
        lines.append("        public void AllClasses_CanBeInstantiated()")
        lines.append("        {")
        lines.append("            var instances = new List<object>();")

        core_classes = [
            c for c in self.schema.classes.values()
            if not c.module.startswith("ext.")
        ]
        for cls in sorted(core_classes, key=lambda c: (c.module, c.name)):
            ns = self._namespace_for_module(cls.module)
            lines.append(f"            instances.Add(new {ns}.{cls.name}());")

        lines.append(f"            Assert.Equal({len(core_classes)}, instances.Count);")
        lines.append("        }")
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

    def _render_module(
        self, top: str, mod: str, classes: list[OntologyClass], vocabs: list[OntologyVocab]
    ) -> str:
        ns = self._namespace_for_module(f"{top}.{mod}")
        lines: list[str] = []
        lines.append("// Auto-generated CASE/UCO ontology classes — do not edit manually.")
        lines.append(f"// Module: {top}-{mod}")
        lines.append("")
        lines.append("using System.Collections.Generic;")
        lines.append("")
        lines.append(f"namespace {ns}")
        lines.append("{")

        for vocab in vocabs:
            lines.extend(self._render_vocab(vocab, indent=1))
            lines.append("")

        for cls in classes:
            lines.extend(self._render_class(cls, indent=1))
            lines.append("")

        lines.append("}")
        return "\n".join(lines)

    def _render_vocab(self, vocab: OntologyVocab, indent: int) -> list[str]:
        pad = "    " * indent
        lines: list[str] = []
        lines.append(f"{pad}/// <summary>Vocabulary: {vocab.name}</summary>")
        lines.append(f"{pad}public static class {vocab.name}")
        lines.append(f"{pad}{{")
        lines.append(f'{pad}    public const string IRI = "{vocab.iri}";')
        for member in vocab.members:
            attr = self._vocab_attr_name(member)
            lines.append(f'{pad}    public const string {attr} = "{member}";')
        lines.append(f"{pad}}}")
        return lines

    def _render_vocabulary_file(self, top: str, vocabs: list[OntologyVocab]) -> str:
        ns = f"CaseUco.{self.to_pascal_case(top)}.Vocabulary"
        lines: list[str] = [
            "// Auto-generated CASE/UCO vocabularies — do not edit manually.",
            f"// {VOCABULARY_MODULE_DOC.format(top=top.upper())}",
            "",
            "using System.Collections.Generic;",
            "",
            f"namespace {ns}",
            "{",
        ]
        for i, vocab in enumerate(vocabs):
            if i:
                lines.append("")
            lines.append(f"    /// <summary>Vocabulary: {vocab.name}</summary>")
            lines.append(f"    public static class {vocab.name}")
            lines.append("    {")
            lines.append(f'        public const string IRI = "{vocab.iri}";')
            members = ", ".join(json.dumps(m, ensure_ascii=False) for m in vocab.members)
            lines.append(
                "        public static readonly IReadOnlyCollection<string> Members = "
                f"new HashSet<string> {{ {members} }};"
            )
            for member in vocab.members:
                attr = self._vocab_attr_name(member)
                lines.append(f"        public const string {attr} = {json.dumps(member, ensure_ascii=False)};")
            lines.append("    }")
        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def _vocab_attr_name(self, member: str) -> str:
        name = member.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        if name and name[0].isdigit():
            name = f"_{name}"
        return self.safe_identifier(name, "csharp")

    def _render_class(self, cls: OntologyClass, indent: int) -> list[str]:
        pad = "    " * indent
        lines: list[str] = []

        parent = self.schema.resolve_class(cls.parent_iris[0]) if cls.parent_iris else None
        class_name = self.safe_identifier(cls.name, "csharp")
        base = f" : {self._qualified_csharp_type_for_class(parent)}" if parent else ""
        const_prefix = "new " if parent else ""
        inherited_names = self._inherited_property_names(cls)

        lines.append(f"{pad}/// <summary>{cls.description[:200] if cls.description else cls.name}</summary>")
        lines.append(f"{pad}public class {class_name}{base}")
        lines.append(f"{pad}{{")
        lines.append(f'{pad}    public {const_prefix}const string ClassIri = "{cls.iri}";')
        lines.append(f'{pad}    public {const_prefix}const string NamespacePrefix = "{cls.namespace_prefix}";')

        for prop in cls.properties:
            cs_type = self._csharp_type(prop)
            prop_name = self._csharp_property_name(cls, prop)
            modifier = "new " if prop.name in inherited_names else ""
            if prop.cardinality.is_required:
                lines.append(f"{pad}    [global::CaseUco.CaseRequired]")
            datatype = f', Datatype = "{prop.binary_datatype}"' if prop.binary_datatype else ""
            lines.append(f'{pad}    [global::CaseUco.JsonLdProperty("{compact_ontology_iri(prop.iri)}"{datatype})]')
            lines.append(f"{pad}    public {modifier}{cs_type} {prop_name} {{ get; set; }}")

        lines.append(f"{pad}}}")
        return lines

    def _csharp_type(self, prop: OntologyProperty) -> str:
        base = self._base_csharp_type(prop)
        nullable_value_types = {
            "bool",
            "decimal",
            "double",
            "float",
            "System.DateTime",
            "System.TimeSpan",
            "long",
            "ulong",
            "sbyte",
            "uint",
            "ushort",
            "int",
            "short",
            "byte",
        }
        if prop.cardinality.is_list:
            return f"List<{base}>"
        if not prop.cardinality.is_required and base in nullable_value_types:
            return f"{base}?"
        return base

    def _base_csharp_type(self, prop: OntologyProperty) -> str:
        if prop.is_union:
            return "object"
        if prop.is_vocab_type:
            return "string"
        if prop.is_xsd_type:
            base = prop.type_name_for("csharp")
            aliases = {
                "DateTime": "System.DateTime",
                "TimeSpan": "System.TimeSpan",
                "Uri": "System.Uri",
            }
            return aliases.get(base, base)

        range_cls = self.schema.resolve_class(prop.range_iri)
        if range_cls:
            return self._qualified_csharp_type_for_class(range_cls)

        return prop.type_name_for("csharp")

    def _namespace_for_module(self, module_key: str) -> str:
        top, mod = module_key.split(".", 1)
        return f"CaseUco.{self.to_pascal_case(top)}.{self.to_pascal_case(mod)}"

    def _qualified_csharp_type_for_class(self, cls: OntologyClass | None) -> str:
        if cls is None:
            return "object"
        safe = self.safe_identifier(cls.name, "csharp")
        return f"{self._namespace_for_module(cls.module)}.{safe}"

    def _inherited_property_names(self, cls: OntologyClass) -> set[str]:
        names: set[str] = set()
        for parent_iri in cls.parent_iris:
            parent = self.schema.resolve_class(parent_iri)
            if not parent:
                continue
            names.update(prop.name for prop in parent.properties)
            names.update(self._inherited_property_names(parent))
        return names

    def _csharp_property_name(self, cls: OntologyClass, prop: OntologyProperty) -> str:
        prop_name = self.to_pascal_case(prop.name)
        prop_name = self.safe_identifier(prop_name, "csharp")
        if prop_name == cls.name:
            return f"{prop_name}Value"
        return prop_name
