"""The UCO/CASE version constants agree with the vendored ontologies in every language."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from case_uco_generator.backends.python_backend import PythonBackend
from case_uco_generator.backends.rust_backend import RustBackend
from case_uco_generator.schema_model import OntologySchema

ROOT = Path(__file__).resolve().parents[2]


def _version_info(ttl: Path) -> str:
    match = re.search(r'owl:versionInfo\s+"([^"]+)"', ttl.read_text(encoding="utf-8"))
    assert match, ttl
    return match.group(1)


UCO = _version_info(ROOT / "ontology/UCO/ontology/uco/master/uco.ttl")
CASE = _version_info(ROOT / "ontology/CASE/ontology/master/case.ttl")
PACKAGE = tomllib.loads((ROOT / "python/pyproject.toml").read_text(encoding="utf-8"))[
    "project"
]["version"]


def _constant(path: str, name: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(rf'\b{name}\s*(?::\s*&str\s*)?=\s*"([^"]+)"', text)
    assert match, f"{name} not found in {path}"
    return match.group(1)


def test_backends_emit_schema_ontology_versions(tmp_path: Path) -> None:
    schema = OntologySchema(ontology_versions={"uco": "9.8.7", "case": "6.5.4"})
    PythonBackend(schema, tmp_path / "py").generate()
    RustBackend(schema, tmp_path / "rs").generate()
    init = (tmp_path / "py" / "__init__.py").read_text(encoding="utf-8")
    lib = (tmp_path / "rs" / "lib.rs").read_text(encoding="utf-8")
    assert 'UCO_VERSION = "9.8.7"' in init and 'CASE_VERSION = "6.5.4"' in init
    assert 'UCO_VERSION: &str = "9.8.7"' in lib and 'CASE_VERSION: &str = "6.5.4"' in lib


def test_checked_in_constants_match_vendored_ontologies() -> None:
    for path, uco_name, case_name in (
        ("python/case_uco/__init__.py", "UCO_VERSION", "CASE_VERSION"),
        ("rust/src/lib.rs", "UCO_VERSION", "CASE_VERSION"),
        ("csharp/CaseUco/CaseUcoMeta.cs", "UcoVersion", "CaseVersion"),
        ("java/src/main/java/org/caseontology/CaseUcoMeta.java", "UCO_VERSION", "CASE_VERSION"),
    ):
        assert _constant(path, uco_name) == UCO, path
        assert _constant(path, case_name) == CASE, path


def test_hand_written_meta_versions_match_the_package() -> None:
    assert _constant("csharp/CaseUco/CaseUcoMeta.cs", "Version") == PACKAGE
    assert _constant("java/src/main/java/org/caseontology/CaseUcoMeta.java", "VERSION") == PACKAGE
