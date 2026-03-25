"""Documentation backend — generates ONTOLOGY_REFERENCE.md from the parsed schema."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.backends.base import CodegenBackend
from case_uco_generator.schema_model import (
    OntologyClass,
    OntologyVocab,
    iri_local_name,
)


class DocsBackend(CodegenBackend):
    """Generate a comprehensive markdown reference index from the ontology schema."""

    def generate(self) -> list[Path]:
        lines: list[str] = []
        self._render_header(lines)
        self._render_toc(lines)
        self._render_modules(lines)
        self._render_vocabs(lines)

        out_path = self.output_dir / "ONTOLOGY_REFERENCE.md"
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return [out_path]

    def _render_header(self, lines: list[str]) -> None:
        total_classes = len(self.schema.classes)
        total_modules = len(self.schema.modules)
        total_vocabs = len(self.schema.vocabs)
        total_props = sum(len(c.properties) for c in self.schema.classes.values())

        lines.append("# CASE/UCO Ontology Reference")
        lines.append("")
        lines.append(
            "Auto-generated reference for all classes, properties, and vocabulary types "
            "in the CASE/UCO ontology. Use this document to discover which classes model "
            "your domain and what properties they expose."
        )
        lines.append("")
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Classes | {total_classes} |")
        lines.append(f"| Direct properties | {total_props} |")
        lines.append(f"| Modules | {total_modules} |")
        lines.append(f"| Vocabulary types | {total_vocabs} |")
        lines.append("")

    def _render_toc(self, lines: list[str]) -> None:
        lines.append("## Table of Contents")
        lines.append("")
        for module_key in sorted(self.schema.modules):
            count = len(self.schema.modules[module_key])
            anchor = module_key.replace(".", "").lower()
            lines.append(f"- [{module_key}](#{anchor}) ({count} classes)")
        lines.append(f"- [Vocabulary Types](#vocabulary-types) ({len(self.schema.vocabs)} types)")
        lines.append("")

    def _render_modules(self, lines: list[str]) -> None:
        for module_key in sorted(self.schema.modules):
            classes = sorted(
                (self.schema.classes[iri]
                 for iri in self.schema.modules[module_key]
                 if iri in self.schema.classes),
                key=lambda c: c.name,
            )
            lines.append(f"## {module_key}")
            lines.append("")

            for cls in classes:
                self._render_class(lines, cls)

    def _render_class(self, lines: list[str], cls: OntologyClass) -> None:
        lines.append(f"### {cls.name}")
        lines.append("")
        if cls.description:
            lines.append(f"*{cls.description}*")
            lines.append("")

        meta_parts: list[str] = []
        if cls.parent_iris:
            parent_names = [iri_local_name(p) for p in cls.parent_iris]
            meta_parts.append(f"**Parents:** {', '.join(parent_names)}")
        if cls.is_facet:
            meta_parts.append("**Type:** Facet")
        meta_parts.append(f"**IRI:** `{cls.iri}`")
        lines.append(" | ".join(meta_parts))
        lines.append("")

        all_props = self.schema.resolve_all_properties(cls)
        if all_props:
            lines.append("| Property | Type | Cardinality | Required | Description |")
            lines.append("|----------|------|-------------|----------|-------------|")
            for prop in all_props:
                type_name = iri_local_name(prop.range_iri)
                req = "Yes" if prop.cardinality.is_required else "No"
                desc = prop.description.replace("|", "\\|").replace("\n", " ")
                if len(desc) > 120:
                    desc = desc[:117] + "..."
                lines.append(f"| {prop.name} | {type_name} | {prop.cardinality.value} | {req} | {desc} |")
            lines.append("")
        else:
            lines.append("*No direct or inherited properties.*")
            lines.append("")

    def _render_vocabs(self, lines: list[str]) -> None:
        if not self.schema.vocabs:
            return

        lines.append("## Vocabulary Types")
        lines.append("")
        lines.append(
            "Enumerated vocabulary types define constrained sets of allowed values "
            "for certain properties."
        )
        lines.append("")

        for vocab in sorted(self.schema.vocabs.values(), key=lambda v: v.name):
            lines.append(f"### {vocab.name}")
            lines.append("")
            lines.append(f"**IRI:** `{vocab.iri}`")
            lines.append("")
            if vocab.members:
                lines.append("| Member |")
                lines.append("|--------|")
                for member in vocab.members:
                    member_name = iri_local_name(member) if "/" in member or "#" in member else member
                    lines.append(f"| `{member_name}` |")
                lines.append("")
