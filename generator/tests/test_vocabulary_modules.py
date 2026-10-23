"""Core vocabularies get one namespace per top-level ontology in every language."""

from __future__ import annotations

import ast
from pathlib import Path

from case_uco_generator.backends.csharp_backend import CSharpBackend
from case_uco_generator.backends.java_backend import JavaBackend
from case_uco_generator.backends.python_backend import PythonBackend
from case_uco_generator.backends.rust_backend import RustBackend
from case_uco_generator.schema_model import OntologySchema, OntologyVocab

UCO_VOCAB = OntologyVocab(
    iri="https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionStatusTypeVocab",
    name="ActionStatusTypeVocab",
    members=["Complete/Finish", "Pending"],
)
CASE_VOCAB = OntologyVocab(
    iri="https://ontology.caseontology.org/case/vocabulary/ReservedWordVocab",
    name="ReservedWordVocab",
    members=["case", "class"],
)
EXTENSION_VOCAB = OntologyVocab(
    iri="https://example.org/ext/OtherVocab", name="OtherVocab", members=["x"]
)


def _schema() -> OntologySchema:
    return OntologySchema(
        vocabs={v.iri: v for v in (UCO_VOCAB, CASE_VOCAB, EXTENSION_VOCAB)},
    )


def test_vocabularies_are_grouped_by_top_level_ontology(tmp_path: Path) -> None:
    grouped = PythonBackend(_schema(), tmp_path).vocabularies_by_top()
    assert [v.name for v in grouped["uco"]] == ["ActionStatusTypeVocab"]
    assert [v.name for v in grouped["case"]] == ["ReservedWordVocab"]


def test_python_vocabulary_module_keeps_literal_members(tmp_path: Path) -> None:
    backend = PythonBackend(_schema(), tmp_path)
    source = backend._render_vocabulary_module("uco", backend.vocabularies_by_top()["uco"])
    tree = ast.parse(source)
    assert [n.name for n in tree.body if isinstance(n, ast.ClassDef)] == ["ActionStatusTypeVocab"]
    assert '"Complete/Finish"' in source
    assert "VOCABULARIES" in source


def test_registry_does_not_truncate_slash_members(tmp_path: Path) -> None:
    import json

    path = PythonBackend(_schema(), tmp_path)._emit_registry()
    members = json.loads(path.read_text(encoding="utf-8"))["vocabs"]["ActionStatusTypeVocab"]["members"]
    assert members == ["Complete/Finish", "Pending"]


def test_reserved_word_members_get_legal_identifiers(tmp_path: Path) -> None:
    schema = _schema()
    sources = {
        "csharp": CSharpBackend(schema, tmp_path)._render_vocabulary_file("case", [CASE_VOCAB]),
        "java": JavaBackend(schema, tmp_path)._render_vocabulary_class("case", CASE_VOCAB),
        "rust": RustBackend(schema, tmp_path)._render_vocabulary_module("case", [CASE_VOCAB]),
        "python": PythonBackend(schema, tmp_path)._render_vocabulary_module("case", [CASE_VOCAB]),
    }
    for lang, source in sources.items():
        assert '"case"' in source, lang
    assert "const string case " not in sources["csharp"]
    assert "const string @case " in sources["csharp"]
    assert "String case " not in sources["java"]
