"""Regression tests for hand-written runtime APIs exposed by generated roots."""

from __future__ import annotations

from pathlib import Path

from case_uco_generator.backends.python_backend import PythonBackend
from case_uco_generator.backends.rust_backend import RustBackend
from case_uco_generator.schema_model import OntologySchema


def test_python_generation_preserves_runtime_api_exports(tmp_path: Path) -> None:
    output = tmp_path / "python" / "case_uco"
    PythonBackend(OntologySchema(), output).generate()

    generated = (output / "__init__.py").read_text(encoding="utf-8")
    for symbol in (
        "JsonLdStreamWriter",
        "PartitionBoundaryError",
        "class_registry_cache_info",
        "discover_extension_class_providers",
        "register_extension_classes",
        "unregister_extension_source",
    ):
        assert f'"{symbol}"' in generated


def test_rust_generation_preserves_runtime_module_exports(tmp_path: Path) -> None:
    output = tmp_path / "rust" / "src"
    RustBackend(OntologySchema(), output).generate()

    generated = (output / "lib.rs").read_text(encoding="utf-8")
    assert "pub mod registry;" in generated
    assert "pub mod streaming;" in generated
