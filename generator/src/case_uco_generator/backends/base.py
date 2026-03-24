"""Abstract base for code generation backends."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path

from case_uco_generator.schema_model import OntologySchema


class CodegenBackend(ABC):
    """Base class for language-specific code generators."""

    def __init__(self, schema: OntologySchema, output_dir: Path):
        self.schema = schema
        self.output_dir = output_dir

    @abstractmethod
    def generate(self) -> list[Path]:
        """Generate all source files. Returns list of created file paths."""
        raise NotImplementedError

    @staticmethod
    def to_snake_case(name: str) -> str:
        """Convert PascalCase or camelCase to snake_case."""
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    @staticmethod
    def to_pascal_case(name: str) -> str:
        """Ensure a name is PascalCase."""
        if "_" in name:
            return "".join(w.capitalize() for w in name.split("_"))
        if name and name[0].islower():
            return name[0].upper() + name[1:]
        return name

    @staticmethod
    def to_camel_case(name: str) -> str:
        """Convert to camelCase."""
        pascal = CodegenBackend.to_pascal_case(name)
        if pascal:
            return pascal[0].lower() + pascal[1:]
        return pascal

    @staticmethod
    def safe_identifier(name: str, lang: str) -> str:
        """Make a name safe as a language identifier, avoiding reserved words."""
        python_reserved = {
            "False", "None", "True", "and", "as", "assert", "async", "await",
            "break", "class", "continue", "def", "del", "elif", "else", "except",
            "finally", "for", "from", "global", "if", "import", "in", "is",
            "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
            "while", "with", "yield", "type", "match", "case",
        }
        csharp_reserved = {
            "abstract", "as", "base", "bool", "break", "byte", "case", "catch",
            "char", "checked", "class", "const", "continue", "decimal", "default",
            "delegate", "do", "double", "else", "enum", "event", "explicit",
            "extern", "false", "finally", "fixed", "float", "for", "foreach",
            "goto", "if", "implicit", "in", "int", "interface", "internal", "is",
            "lock", "long", "namespace", "new", "null", "object", "operator",
            "out", "override", "params", "private", "protected", "public",
            "readonly", "ref", "return", "sbyte", "sealed", "short", "sizeof",
            "stackalloc", "static", "string", "struct", "switch", "this", "throw",
            "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe",
            "ushort", "using", "virtual", "void", "volatile", "while",
        }
        java_reserved = {
            "abstract", "assert", "boolean", "break", "byte", "case", "catch",
            "char", "class", "const", "continue", "default", "do", "double",
            "else", "enum", "extends", "final", "finally", "float", "for",
            "goto", "if", "implements", "import", "instanceof", "int", "interface",
            "long", "native", "new", "package", "private", "protected", "public",
            "return", "short", "static", "strictfp", "super", "switch",
            "synchronized", "this", "throw", "throws", "transient", "try", "void",
            "volatile", "while",
        }
        rust_reserved = {
            "as", "async", "await", "break", "const", "continue", "crate", "dyn",
            "else", "enum", "extern", "false", "fn", "for", "if", "impl", "in",
            "let", "loop", "match", "mod", "move", "mut", "pub", "ref", "return",
            "self", "Self", "static", "struct", "super", "trait", "true", "type",
            "union", "unsafe", "use", "where", "while", "yield",
        }

        reserved_map = {
            "python": python_reserved,
            "csharp": csharp_reserved,
            "java": java_reserved,
            "rust": rust_reserved,
        }

        reserved = reserved_map.get(lang, set())
        if name in reserved:
            suffix = {"python": "_", "csharp": "@", "java": "_", "rust": "r#"}
            pfx = suffix.get(lang, "_")
            if lang == "rust":
                return f"r#{name}"
            return f"{name}{pfx}" if lang == "python" else f"{pfx}{name}"

        if name and name[0].isdigit():
            return f"_{name}"

        return name
