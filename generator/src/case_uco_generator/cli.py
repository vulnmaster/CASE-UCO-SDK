"""CLI entry point for the CASE/UCO code generator."""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

from case_uco_generator.ontology_parser import (
    parse_ontology,
    load_extension_manifest,
)
from case_uco_generator.backends.python_backend import PythonBackend
from case_uco_generator.backends.csharp_backend import CSharpBackend
from case_uco_generator.backends.java_backend import JavaBackend
from case_uco_generator.backends.rust_backend import RustBackend
from case_uco_generator.backends.docs_backend import DocsBackend
from case_uco_generator.mapping_guide import generate_mapping_guide
from case_uco_generator.scaffold import scaffold_extension


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="case-uco-generate",
        description="Generate CASE/UCO ontology libraries from OWL+SHACL Turtle files.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --- generate subcommand ---
    gen_parser = subparsers.add_parser("generate", help="Generate typed libraries from ontology sources")
    gen_parser.add_argument(
        "--lang",
        choices=["python", "csharp", "java", "rust", "all"],
        default="all",
        help="Target language (default: all)",
    )
    gen_parser.add_argument("--ontology-dir", type=Path, default=None)
    gen_parser.add_argument("--output-dir", type=Path, default=None)
    gen_parser.add_argument("--extensions-dir", type=Path, default=None)
    gen_parser.add_argument("--no-extensions", action="store_true")
    gen_parser.add_argument(
        "--incremental",
        action="store_true",
        default=True,
        help="Skip parse+emission when Turtle sources match the IR manifest (default).",
    )
    gen_parser.add_argument(
        "--no-incremental",
        action="store_true",
        help="Force a full re-parse even when sources are unchanged.",
    )
    gen_parser.add_argument(
        "--force",
        action="store_true",
        help="Alias for --no-incremental.",
    )

    # --- scaffold subcommand ---
    scaf_parser = subparsers.add_parser(
        "scaffold",
        help="Generate starter classes from an extension ontology TTL",
    )
    scaf_parser.add_argument(
        "--extension",
        type=Path,
        required=True,
        nargs="+",
        help="Path(s) to extension .ttl file(s) (OWL + SHACL shapes)",
    )
    scaf_parser.add_argument(
        "--lang",
        choices=["python", "csharp", "java", "rust", "all"],
        default="all",
        help="Target language(s) for scaffolded classes (default: all)",
    )
    scaf_parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for scaffolded files (default: current directory)",
    )

    # --- generate-extension subcommand ---
    ext_parser = subparsers.add_parser(
        "generate-extension",
        help="Generate complete publishable packages from an extension manifest",
    )
    ext_parser.add_argument(
        "--extension",
        type=Path,
        required=True,
        help="Path to the extension directory containing manifest.json",
    )
    ext_parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for generated packages (default: packages/case-uco-<name>)",
    )
    ext_parser.add_argument(
        "--lang",
        choices=["python", "csharp", "java", "rust", "all"],
        default="all",
        help="Target language(s) (default: all)",
    )
    ext_parser.add_argument("--ontology-dir", type=Path, default=None)

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "generate":
        return _cmd_generate(args)
    elif args.command == "scaffold":
        return _cmd_scaffold(args)
    elif args.command == "generate-extension":
        return _cmd_generate_extension(args)

    return 0


def _cmd_generate(args) -> int:
    repo_root = args.output_dir or Path.cwd()
    ontology_dir = args.ontology_dir or repo_root / "ontology"
    if args.no_extensions:
        extensions_dir = None
    elif args.extensions_dir:
        extensions_dir = [args.extensions_dir]
    else:
        # v1.19.0: SDK-native extensions plus upstream-vendored ontologies.
        extensions_dir = [repo_root / "extensions", repo_root / "ontology"]

    if not ontology_dir.exists():
        logging.error("Ontology directory not found: %s", ontology_dir)
        return 1

    from case_uco_generator.incremental import (
        sources_unchanged,
        write_ir,
        changed_files,
    )

    incremental = not (getattr(args, "no_incremental", False) or getattr(args, "force", False))
    if incremental and sources_unchanged(repo_root):
        logging.info(
            "IR cache hit: Turtle sources unchanged. Skipping parse and emission. "
            "Pass --force to regenerate."
        )
        return 0

    if incremental:
        delta = changed_files(repo_root)
        if delta:
            logging.info(
                "Incremental generate: %d source file(s) changed; re-parsing dependents "
                "(full import closure — parse_ontology is one graph).",
                len(delta),
            )
            for path in delta[:20]:
                logging.info("  changed: %s", path)
            if len(delta) > 20:
                logging.info("  ... %d more", len(delta) - 20)

    logging.info("Parsing ontology from %s ...", ontology_dir)
    schema = parse_ontology(ontology_dir, extensions_dir=extensions_dir)
    logging.info(
        "Parsed %d classes, %d vocabs across %d modules",
        len(schema.classes), len(schema.vocabs), len(schema.modules),
    )

    languages = (
        ["python", "csharp", "java", "rust"]
        if args.lang == "all"
        else [args.lang]
    )

    core_schema = schema.without_extensions()
    output_root = repo_root
    total_files = 0
    for lang in languages:
        logging.info("Generating %s library ...", lang)
        backend = _create_backend(lang, core_schema, output_root)
        files = backend.generate()
        total_files += len(files)
        logging.info("  -> %d files generated for %s", len(files), lang)

    logging.info("Generating ontology reference ...")
    docs_backend = DocsBackend(schema, output_root)
    docs_files = docs_backend.generate()
    total_files += len(docs_files)
    logging.info("  -> %s", docs_files[0])

    logging.info("Generating mapping guide ...")
    guide_path = generate_mapping_guide(schema, output_root / "docs" / "MAPPING_GUIDE.md")
    total_files += 1
    logging.info("  -> %s", guide_path)

    logging.info("Generating runtime registry (full schema with extensions) ...")
    registry_backend = PythonBackend(schema, output_root / "python" / "case_uco")
    registry_path = registry_backend._emit_registry()
    logging.info("  -> %s", registry_path)

    registry_copies = {
        "csharp": output_root / "csharp" / "CaseUco" / "_registry.json",
        "java": output_root / "java" / "src" / "main" / "resources" / "_registry.json",
        "rust": output_root / "rust" / "src" / "_registry.json",
    }
    import shutil
    for lang_name, dest in registry_copies.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(registry_path, dest)
        total_files += 1
        logging.info("  -> %s (%s)", dest, lang_name)

    write_ir(repo_root, schema)
    logging.info("Done: %d total files generated.", total_files)
    return 0


def _cmd_scaffold(args) -> int:
    ttl_paths = [Path(p) for p in args.extension]
    for p in ttl_paths:
        if not p.exists():
            logging.error("Extension file not found: %s", p)
            return 1

    languages = (
        ["python", "csharp", "java", "rust"]
        if args.lang == "all"
        else [args.lang]
    )

    output_dir = args.output_dir or Path.cwd()
    logging.info("Scaffolding extension from %s ...", ", ".join(str(p) for p in ttl_paths))

    created = scaffold_extension(ttl_paths, output_dir, languages)

    if not created:
        logging.warning("No classes found. Ensure the TTL has OWL classes with SHACL NodeShapes.")
        return 1

    logging.info("Done: %d scaffolded files created.", len(created))
    return 0


def _create_backend(lang: str, schema, output_root: Path):
    backends = {
        "python": (PythonBackend, output_root / "python" / "case_uco"),
        "csharp": (CSharpBackend, output_root / "csharp" / "CaseUco"),
        "java": (JavaBackend, output_root / "java" / "src" / "main" / "java" / "org" / "caseontology"),
        "rust": (RustBackend, output_root / "rust" / "src"),
    }
    cls, out_dir = backends[lang]
    return cls(schema, out_dir)


def _cmd_generate_extension(args) -> int:
    ext_dir = Path(args.extension)
    manifest = load_extension_manifest(ext_dir)
    if manifest is None:
        logging.error("No manifest.json found in %s", ext_dir)
        return 1

    ext_name = manifest["name"]
    ext_version = manifest["version"]
    display_name = manifest["display_name"]
    pkg_name = f"case-uco-{ext_name}"
    py_pkg = f"case_uco_{ext_name}"

    repo_root = Path.cwd()
    ontology_dir = args.ontology_dir or repo_root / "ontology"
    output_dir = args.output_dir or repo_root / "packages" / pkg_name

    if not ontology_dir.exists():
        logging.error("Ontology directory not found: %s", ontology_dir)
        return 1

    logging.info("Parsing core ontology from %s ...", ontology_dir)
    ext_roots = [ext_dir.parent, repo_root / "extensions", repo_root / "ontology"]
    # Dedupe while preserving priority: the requested extension's own root first.
    unique_roots = list(dict.fromkeys(r.resolve() for r in ext_roots))
    schema = parse_ontology(ontology_dir, extensions_dir=unique_roots)

    ext_schema = _filter_extension_schema(schema, ext_name)
    if not ext_schema.classes:
        logging.warning("No SHACL-shaped classes found for extension '%s'.", ext_name)

    languages = (
        ["python", "csharp", "java", "rust"]
        if args.lang == "all"
        else [args.lang]
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    total_files = 0

    uco_compat = manifest.get("uco_compat", [])
    uco_dep = f">={uco_compat[0]}" if uco_compat else ">=1.0.0"

    for lang in languages:
        logging.info("Generating %s package for %s ...", lang, ext_name)
        count = _generate_extension_package(
            lang, ext_schema, schema, output_dir, ext_name, ext_version,
            display_name, py_pkg, uco_dep, manifest,
        )
        total_files += count
        logging.info("  -> %d files generated for %s", count, lang)

    logging.info("Generating extension registry ...")
    reg_path = _emit_extension_registry(ext_schema, schema, output_dir, ext_name)
    total_files += 1
    logging.info("  -> %s", reg_path)

    logging.info("Done: %d total files generated for extension '%s'.", total_files, ext_name)
    return 0


def _filter_extension_schema(schema, ext_name: str):
    """Extract only the classes belonging to a given extension from the full schema."""
    from case_uco_generator.schema_model import OntologySchema

    ext_prefix = f"ext.{ext_name}"
    filtered_modules = {k: v for k, v in schema.modules.items() if k.startswith(ext_prefix)}
    ext_iris = set()
    for iris in filtered_modules.values():
        ext_iris.update(iris)
    filtered_classes = {k: v for k, v in schema.classes.items() if k in ext_iris}

    return OntologySchema(
        classes=filtered_classes,
        vocabs=dict(schema.vocabs),
        namespaces=dict(schema.namespaces),
        modules=filtered_modules,
    )


def _module_display_name(module_key: str, ext_name: str) -> str:
    """Strip the internal ``ext.<name>.`` prefix from a module key.

    Internal module keys look like ``ext.cac.cacontology-sex-trafficking``;
    consumers (MCP search, language registries, documentation) expect the
    user-facing namespace prefix (``cacontology-sex-trafficking``).
    """
    expected = f"ext.{ext_name}."
    if module_key.startswith(expected):
        return module_key[len(expected):]
    return module_key


def _emit_extension_registry(ext_schema, full_schema, output_dir: Path, ext_name: str) -> Path:
    """Write _registry.json containing only the extension's classes."""
    from case_uco_generator.schema_model import iri_local_name

    module_names = sorted(
        {_module_display_name(k, ext_name) for k in ext_schema.modules.keys()}
    )

    registry: dict = {
        "extension": ext_name,
        "modules": module_names,
        "classes": {},
        "vocabs": {},
    }

    for cls in sorted(ext_schema.classes.values(), key=lambda c: c.name):
        all_props = full_schema.resolve_all_properties(cls)
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
            "module": _module_display_name(cls.module, ext_name),
            "description": cls.description,
            "parents": [iri_local_name(p) for p in cls.parent_iris],
            "is_facet": cls.is_facet,
            "properties": props_data,
            "source": ext_name,
        }

    path = output_dir / "_registry.json"
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _sanitize_module_id(name: str) -> str:
    """Convert a manifest namespace prefix to a language-safe identifier.

    Manifest prefixes (e.g. ``cacontology-sex-trafficking``) contain hyphens
    that are not valid Python/C#/Java/Rust identifiers. Hyphens become
    underscores; any other non-alphanumeric character is also normalized.
    """
    sanitized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return sanitized or "core"


def _generate_extension_package(
    lang: str,
    ext_schema,
    full_schema,
    output_dir: Path,
    ext_name: str,
    ext_version: str,
    display_name: str,
    py_pkg: str,
    uco_dep: str,
    manifest: dict,
) -> int:
    """Generate a complete publishable package for one language.  Returns file count."""
    if lang == "python":
        return _gen_python_extension(ext_schema, full_schema, output_dir, ext_name, ext_version, display_name, py_pkg, uco_dep, manifest)
    elif lang == "csharp":
        return _gen_csharp_extension(ext_schema, output_dir, ext_name, ext_version, display_name, uco_dep)
    elif lang == "java":
        return _gen_java_extension(ext_schema, output_dir, ext_name, ext_version, display_name, uco_dep)
    elif lang == "rust":
        return _gen_rust_extension(ext_schema, output_dir, ext_name, ext_version, display_name, uco_dep)
    return 0


def _gen_python_extension(ext_schema, full_schema, output_dir, ext_name, ext_version, display_name, py_pkg, uco_dep, manifest) -> int:
    from case_uco_generator.schema_model import iri_local_name

    py_dir = output_dir / "python" / py_pkg
    py_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    namespaces = manifest.get("namespaces", {})
    ns_lines = "\n".join(f'    "{prefix}": "{uri}",' for prefix, uri in sorted(namespaces.items()))

    init_content = (
        f'"""{display_name} — CASE/UCO SDK extension bindings."""\n\n'
        f'__version__ = "{ext_version}"\n\n'
        f"NAMESPACES: dict[str, str] = {{\n{ns_lines}\n}}\n\n"
        f'# Public so the case_uco.extensions entry point (and static analysis)\n'
        f'# can reference it: the SDK registry loader resolves this at runtime.\n'
        f'REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")\n'
    )
    (py_dir / "__init__.py").write_text(init_content, encoding="utf-8")
    count += 1

    modules_written: set[str] = set()
    for module_key, class_iris in sorted(ext_schema.modules.items()):
        parts = module_key.split(".", 2)
        prefix = parts[-1] if len(parts) > 2 else parts[-1]
        mod_name = _sanitize_module_id(prefix)
        if mod_name in modules_written:
            continue
        modules_written.add(mod_name)

        classes = [ext_schema.classes[iri] for iri in class_iris if iri in ext_schema.classes]
        classes.sort(key=lambda c: c.name)
        if not classes:
            continue

        lines = [
            f'"""{display_name} — {prefix} module."""\n',
            "from __future__ import annotations\n",
            "from dataclasses import dataclass, field",
            "from typing import Optional\n\n",
        ]

        for cls in classes:
            lines.append("@dataclass")
            lines.append(f"class {cls.name}:")
            desc = cls.description[:200] if cls.description else cls.name
            lines.append(f'    """{desc}"""\n')
            lines.append(f'    CLASS_IRI: str = "{cls.iri}"')

            all_props = full_schema.resolve_all_properties(cls)
            for prop in all_props:
                field_name = _to_snake(prop.name)
                type_str = prop.type_name_for("python")
                if prop.cardinality.is_list:
                    lines.append(f"    {field_name}: list[{type_str}] = field(default_factory=list)")
                else:
                    lines.append(f"    {field_name}: Optional[{type_str}] = field(default=None)")
            lines.append("\n")

        (py_dir / f"{mod_name}.py").write_text("\n".join(lines), encoding="utf-8")
        count += 1

    pyproject = (
        "[build-system]\n"
        'requires = ["hatchling"]\n'
        'build-backend = "hatchling.build"\n\n'
        "[project]\n"
        f'name = "case-uco-{ext_name}"\n'
        f'version = "{ext_version}"\n'
        f'description = "{display_name} bindings for CASE/UCO SDK"\n'
        'requires-python = ">=3.10"\n'
        "dependencies = [\n"
        f'    "case-uco{uco_dep}",\n'
        "]\n\n"
        '[project.entry-points."case_uco.extensions"]\n'
        f'{ext_name} = "{py_pkg}:REGISTRY_PATH"\n'
    )
    (output_dir / "python" / "pyproject.toml").write_text(pyproject, encoding="utf-8")
    count += 1
    return count


def _gen_csharp_extension(ext_schema, output_dir, ext_name, ext_version, display_name, uco_dep) -> int:
    cs_dir = output_dir / "csharp" / f"CaseUco.{ext_name.upper()}"
    cs_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    csproj = (
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        "  <PropertyGroup>\n"
        "    <TargetFramework>net8.0</TargetFramework>\n"
        f"    <PackageId>CaseUco.{ext_name.upper()}</PackageId>\n"
        f"    <Version>{ext_version}</Version>\n"
        f"    <Description>{display_name} bindings for CASE/UCO SDK</Description>\n"
        "  </PropertyGroup>\n"
        "  <ItemGroup>\n"
        f'    <PackageReference Include="CaseUco" Version="{uco_dep.lstrip(">=")}"/>\n'
        "  </ItemGroup>\n"
        "</Project>\n"
    )
    (cs_dir / f"CaseUco.{ext_name.upper()}.csproj").write_text(csproj, encoding="utf-8")
    count += 1

    for module_key, class_iris in sorted(ext_schema.modules.items()):
        parts = module_key.split(".", 2)
        prefix = parts[-1] if len(parts) > 2 else parts[-1]
        mod_name = _sanitize_module_id(prefix)
        classes = [ext_schema.classes[iri] for iri in class_iris if iri in ext_schema.classes]
        if not classes:
            continue

        ns_pascal = mod_name[0].upper() + mod_name[1:]
        lines = [
            f"// {display_name} — {mod_name} module",
            f"namespace CaseUco.Ext.{ext_name.upper()}.{ns_pascal}",
            "{",
        ]
        for cls in sorted(classes, key=lambda c: c.name):
            lines.append(f"    public class {cls.name}")
            lines.append("    {")
            lines.append(f'        public static readonly string ClassIri = "{cls.iri}";')
            for prop in cls.properties:
                cs_type = prop.type_name_for("csharp")
                prop_name = prop.name[0].upper() + prop.name[1:]
                if prop.cardinality.is_list:
                    lines.append(f"        public List<{cs_type}> {prop_name} {{ get; set; }} = new();")
                else:
                    lines.append(f"        public {cs_type}? {prop_name} {{ get; set; }}")
            lines.append("    }")
            lines.append("")
        lines.append("}")

        (cs_dir / f"{ns_pascal}.cs").write_text("\n".join(lines), encoding="utf-8")
        count += 1

    return count


def _gen_java_extension(ext_schema, output_dir, ext_name, ext_version, display_name, uco_dep) -> int:
    java_base = output_dir / "java" / "src" / "main" / "java" / "org" / "caseontology" / "ext" / ext_name
    java_base.mkdir(parents=True, exist_ok=True)
    count = 0

    pom = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<project xmlns="http://maven.apache.org/POM/4.0.0"\n'
        '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        '         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">\n'
        "  <modelVersion>4.0.0</modelVersion>\n"
        f"  <groupId>org.caseontology</groupId>\n"
        f"  <artifactId>case-uco-{ext_name}</artifactId>\n"
        f"  <version>{ext_version}</version>\n"
        f"  <name>{display_name}</name>\n"
        "  <dependencies>\n"
        "    <dependency>\n"
        "      <groupId>org.caseontology</groupId>\n"
        "      <artifactId>case-uco</artifactId>\n"
        f"      <version>{uco_dep.lstrip('>=')}</version>\n"
        "    </dependency>\n"
        "  </dependencies>\n"
        "</project>\n"
    )
    (output_dir / "java" / "pom.xml").write_text(pom, encoding="utf-8")
    count += 1

    for module_key, class_iris in sorted(ext_schema.modules.items()):
        parts = module_key.split(".", 2)
        prefix = parts[-1] if len(parts) > 2 else parts[-1]
        mod_name = _sanitize_module_id(prefix)
        classes = [ext_schema.classes[iri] for iri in class_iris if iri in ext_schema.classes]
        if not classes:
            continue

        for cls in sorted(classes, key=lambda c: c.name):
            lines = [
                f"package org.caseontology.ext.{ext_name}.{mod_name};",
                "",
                "import java.util.ArrayList;",
                "import java.util.List;",
                "",
                f"public class {cls.name} {{",
                f'    public static final String CLASS_IRI = "{cls.iri}";',
                "",
            ]
            for prop in cls.properties:
                java_type = prop.type_name_for("java")
                if prop.cardinality.is_list:
                    lines.append(f"    private List<{java_type}> {prop.name} = new ArrayList<>();")
                else:
                    lines.append(f"    private {java_type} {prop.name};")
            lines.append("")
            for prop in cls.properties:
                java_type = prop.type_name_for("java")
                getter = "get" + prop.name[0].upper() + prop.name[1:]
                setter = "set" + prop.name[0].upper() + prop.name[1:]
                if prop.cardinality.is_list:
                    lines.append(f"    public List<{java_type}> {getter}() {{ return {prop.name}; }}")
                else:
                    lines.append(f"    public {java_type} {getter}() {{ return {prop.name}; }}")
                    lines.append(f"    public void {setter}({java_type} {prop.name}) {{ this.{prop.name} = {prop.name}; }}")
            lines.append("}")

            mod_dir = java_base / mod_name
            mod_dir.mkdir(parents=True, exist_ok=True)
            (mod_dir / f"{cls.name}.java").write_text("\n".join(lines), encoding="utf-8")
            count += 1

    return count


def _gen_rust_extension(ext_schema, output_dir, ext_name, ext_version, display_name, uco_dep) -> int:
    rust_dir = output_dir / "rust" / "src"
    rust_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    cargo = (
        "[package]\n"
        f'name = "case-uco-{ext_name}"\n'
        f'version = "{ext_version}"\n'
        'edition = "2021"\n'
        f'description = "{display_name} bindings for CASE/UCO SDK"\n\n'
        "[dependencies]\n"
        f'case-uco = "{uco_dep.lstrip(">=")}"\n'
        'serde = {{ version = "1", features = ["derive"] }}\n'
    )
    (output_dir / "rust" / "Cargo.toml").write_text(cargo, encoding="utf-8")
    count += 1

    mod_names: list[str] = []
    for module_key, class_iris in sorted(ext_schema.modules.items()):
        parts = module_key.split(".", 2)
        prefix = parts[-1] if len(parts) > 2 else parts[-1]
        mod_name = _sanitize_module_id(prefix)
        if mod_name in mod_names:
            continue
        mod_names.append(mod_name)

        classes = [ext_schema.classes[iri] for iri in class_iris if iri in ext_schema.classes]
        if not classes:
            continue

        lines = [
            f"//! {display_name} — {prefix} module\n",
            "use serde::Serialize;\n",
        ]
        for cls in sorted(classes, key=lambda c: c.name):
            desc = cls.description[:120] if cls.description else cls.name
            lines.append(f"/// {desc}")
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

        (rust_dir / f"{mod_name}.rs").write_text("\n".join(lines), encoding="utf-8")
        count += 1

    lib_lines = [f"pub mod {m};" for m in mod_names]
    (rust_dir / "lib.rs").write_text("\n".join(lib_lines) + "\n", encoding="utf-8")
    count += 1

    return count


if __name__ == "__main__":
    sys.exit(main())
