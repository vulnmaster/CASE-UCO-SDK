#!/usr/bin/env python3
"""Fail-closed ontology-term lint for operational modeling recipes.

The graph validator can only inspect graph artifacts.  Recipes also teach terms
in prose tables, snippets, and diagrams, so this module checks the operational
Markdown catalog against the same role-aware declaration inventory used by
strict concept coverage.  Exact pinned upper-ontology terms and every
operational extension manifest are included; arbitrary namespace membership is
never accepted.

Narrow exclusions are reported, not discarded:

* terms containing ``*`` are classified as wildcard notation;
* unresolved generic ``kb:``/``ex:`` terms are classified as instance IDs;
* findings under an explicit ``Anti-pattern`` section are classified as such;
* authors may surround proposed/example-only lines with
  ``<!-- recipe-lint: ignore-start proposed-term -- rationale -->`` and the
  matching ``ignore-end`` directive.

The directives do not suppress malformed directives, relationship kinds, or
terms outside their bounded region.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from collections.abc import Iterable, Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = PROJECT_ROOT / "docs" / "recipes"

_CURIE_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])(?P<prefix>[A-Za-z][A-Za-z0-9_-]*):"
    r"(?P<local>[A-Za-z_][A-Za-z0-9._*-]*)"
)
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_JSON_KEY_RE = re.compile(r"[\"'](?P<term>[A-Za-z][A-Za-z0-9_-]*:[A-Za-z_][A-Za-z0-9._-]*)[\"']\s*:")
_REL_KIND_PATTERNS = (
    re.compile(r"\bkind_of_relationship\s*=\s*[\"'](?P<kind>[^\"']+)[\"']"),
    re.compile(r"[\"'](?:[A-Za-z][A-Za-z0-9_-]*:)?kindOfRelationship[\"']\s*:\s*[\"'](?P<kind>[^\"']+)[\"']"),
    re.compile(r"\bkindOfRelationship\s*=\s*[\"'](?P<kind>[^\"']+)[\"']"),
    re.compile(r"\bkindOfRelationship\s*:\s*[\"'](?P<kind>[^\"']+)[\"']"),
)
_IGNORE_START_RE = re.compile(
    r"^\s*<!--\s*recipe-lint:\s*ignore-start\s+"
    r"(?P<classification>[a-z][a-z0-9-]*)\s+--\s+(?P<reason>.+?)\s*-->\s*$"
)
_IGNORE_END_RE = re.compile(
    r"^\s*<!--\s*recipe-lint:\s*ignore-end\s+"
    r"(?P<classification>[a-z][a-z0-9-]*)\s*-->\s*$"
)

_ALLOWED_EXCLUSION_CLASSES = frozenset(
    {"anti-pattern", "controlled-literal", "instance-id", "proposed-term"}
)
_EMPTY_PYTHON_CONTENT_FACET_RE = re.compile(r"\bContentDataFacet\s*\(\s*\)")
_JAVA_NEW_CONTENT_FACET_RE = re.compile(r"\bnew\s+ContentDataFacet\s*\(\s*\)")
_CONTENT_FACET_TYPE_RE = re.compile(
    r"[\"'](?:[A-Za-z][A-Za-z0-9_-]*:)?ContentDataFacet[\"']"
)
_CONTENT_FACET_SUBSTANCE_RE = re.compile(
    r"(?:uco-observable:)?(?:hash|sizeInBytes|mimeType|dataPayload|"
    r"hash_method|hash_value|size_in_bytes|mime_type|data_payload)\b",
    re.IGNORECASE,
)
_STATE_SPECIFIC_CHARGE_CLASSES = frozenset(
    {
        "FloridaStateCharge",
        "GeorgiaStateCharge",
        "MarylandStateCharge",
        "TravelingToMeetAfterComputerLure",
        "DirectPromotionOfSexualPerformance",
        "ComputerSeduceSolicitLure",
        "ContributingToDelinquency",
        "TraffickingOfPersonsForSexualServitudeCharge",
        "SexualExploitationOfMinorCharge",
    }
)
_INSTANCE_PREFIXES = frozenset({"kb", "ex", "example", "urn"})
_CONTROLLED_LITERAL_PREFIXES = frozenset(
    {"confidence", "epistemic", "hash-status", "source-bytes", "REDACTED"}
)
_FOUNDATIONAL_PREFIXES = frozenset(
    {"rdf", "rdfs", "owl", "xsd", "sh", "skos", "dcterms", "dct", "dc"}
)

_STANDARD_PREFIXES: dict[str, str] = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "sh": "http://www.w3.org/ns/shacl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
    "dct": "http://purl.org/dc/terms/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "prov": "http://www.w3.org/ns/prov#",
    "time": "http://www.w3.org/2006/time#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "sf": "http://www.opengis.net/ont/sf#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "org": "http://www.w3.org/ns/org#",
    "prof": "http://www.w3.org/ns/dx/prof/",
    "gufo": "http://purl.org/nemo/gufo#",
    "obo": "http://purl.obolibrary.org/obo/",
}
_FOUNDATIONAL_NAMESPACES = frozenset(
    _STANDARD_PREFIXES[prefix] for prefix in _FOUNDATIONAL_PREFIXES
)


@dataclass(frozen=True)
class OntologyCatalog:
    prefixes: dict[str, str]
    classes: frozenset[str]
    properties: frozenset[str]
    other_terms: frozenset[str]
    class_local_names: frozenset[str]
    property_local_names: frozenset[str]
    extensions: tuple[str, ...] = ()
    profiles: tuple[str, ...] = ()
    parse_errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecipeLintFinding:
    path: str
    line: int
    code: str
    term: str
    message: str
    role: str = "term"
    excluded: bool = False
    classification: str = ""
    reason: str = ""


@dataclass
class RecipeLintReport:
    files_checked: int = 0
    terms_checked: int = 0
    findings: list[RecipeLintFinding] = field(default_factory=list)
    catalog_extensions: tuple[str, ...] = ()
    catalog_profiles: tuple[str, ...] = ()
    verification_errors: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[RecipeLintFinding]:
        return [finding for finding in self.findings if not finding.excluded]

    @property
    def exclusions(self) -> list[RecipeLintFinding]:
        return [finding for finding in self.findings if finding.excluded]

    @property
    def ok(self) -> bool:
        return not self.verification_errors and not self.errors

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "files_checked": self.files_checked,
            "terms_checked": self.terms_checked,
            "error_count": len(self.errors),
            "exclusion_count": len(self.exclusions),
            "catalog_extensions": list(self.catalog_extensions),
            "catalog_profiles": list(self.catalog_profiles),
            "verification_errors": list(self.verification_errors),
            "findings": [asdict(finding) for finding in self.findings],
        }


def _local_name(iri: str) -> str:
    return iri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def _manifest_paths(project_root: Path) -> list[Path]:
    paths = list((project_root / "extensions").glob("*/manifest.json"))
    paths.extend((project_root / "ontology").glob("*/manifest.json"))
    return sorted(paths)


def _operational_manifests(project_root: Path) -> list[tuple[Path, dict[str, object]]]:
    manifests: list[tuple[Path, dict[str, object]]] = []
    for path in _manifest_paths(project_root):
        data = json.loads(path.read_text(encoding="utf-8"))
        status = str(data.get("status", "operational")).strip().lower()
        if status == "operational":
            manifests.append((path, data))
    return manifests


def build_catalog(project_root: Path = PROJECT_ROOT) -> OntologyCatalog:
    """Build the exact role-aware declaration catalog used by recipe lint."""

    python_root = str(project_root / "python")
    mcp_root = str(project_root / "mcp_server")
    for import_path in (python_root, mcp_root):
        if import_path not in sys.path:
            sys.path.insert(0, import_path)

    from case_uco.graph import DEFAULT_CONTEXT
    from case_uco.validation import coverage

    manifests = _operational_manifests(project_root)
    extension_names = tuple(
        sorted(
            str(data["name"])
            for _path, data in manifests
            if data.get("name")
        )
    )
    prefixes = dict(DEFAULT_CONTEXT)
    prefixes.update(_STANDARD_PREFIXES)
    for _path, data in manifests:
        namespaces = data.get("namespaces") or {}
        if isinstance(namespaces, dict):
            for prefix, iri in namespaces.items():
                if isinstance(prefix, str) and isinstance(iri, str):
                    prefixes[prefix] = iri

    extension_modes = [f"{name}:full" for name in extension_names]
    declared = coverage.load_declared_terms(
        project_root=project_root,
        extensions=extension_modes,
        fail_on_parse_error=False,
    )

    classes = set(declared.classes)
    properties = set(declared.properties)
    other_terms = set(declared.shapes) | set(declared.unknown_role)

    # Some vendored modules rely on an owl:imports namespace closure and omit
    # sibling prefix declarations in the individual Turtle file.  Strict graph
    # coverage reports those files as parse errors.  Retry only those exact
    # files with prefixes from their registered manifest; an unrepairable file
    # remains a hard verification error.
    unresolved_parse_errors: list[str] = []
    prefix_block = "\n".join(
        f"@prefix {prefix}: <{iri}> ."
        for prefix, iri in sorted(prefixes.items())
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", prefix)
    )
    for error in declared.parse_errors:
        error_path = Path(error.path)
        owner_name = ""
        for manifest_path, data in manifests:
            try:
                error_path.resolve().relative_to(manifest_path.parent.resolve())
            except ValueError:
                continue
            owner_name = str(data.get("name") or "")
            break
        try:
            import rdflib

            repaired_graph = rdflib.Graph()
            repaired_graph.parse(
                data=f"{prefix_block}\n{error_path.read_text(encoding='utf-8')}",
                format="turtle",
                publicID=error_path.resolve().as_uri(),
            )
            repaired = coverage._collect_declared_from_graphs(
                [(error_path, repaired_graph, "ontology", None, owner_name or None)]
            )
        except Exception as repair_exc:  # noqa: BLE001 - surfaced fail-closed below
            unresolved_parse_errors.append(
                f"{error.path}: {error.error}; "
                f"manifest_prefix_retry_failed:{type(repair_exc).__name__}:{repair_exc}"
            )
            continue
        classes.update(repaired.classes)
        properties.update(repaired.properties)
        other_terms.update(repaired.shapes)
        other_terms.update(repaired.unknown_role)
    profiles: list[str] = []
    upper_registry_path = project_root / "mcp_server" / "upper_ontology_registry.json"
    upper = json.loads(upper_registry_path.read_text(encoding="utf-8"))
    for profile_id, entry in (upper.get("ontologies") or {}).items():
        profiles.append(str(profile_id))
        classes.update(entry.get("classes") or [])
        properties.update(entry.get("properties") or [])
        other_terms.update(entry.get("individuals") or [])
        other_terms.update(entry.get("datatypes") or [])

    parse_errors = tuple(unresolved_parse_errors)
    return OntologyCatalog(
        prefixes=prefixes,
        classes=frozenset(classes),
        properties=frozenset(properties),
        other_terms=frozenset(other_terms),
        class_local_names=frozenset(_local_name(iri) for iri in classes),
        property_local_names=frozenset(_local_name(iri) for iri in properties),
        extensions=extension_names,
        profiles=tuple(sorted(profiles)),
        parse_errors=parse_errors,
    )


def _recipe_prefixes(text: str, base: dict[str, str]) -> dict[str, str]:
    """Merge namespace declarations embedded in JSON-LD/Turtle snippets."""

    prefixes = dict(base)
    json_context = re.compile(
        r"[\"'](?P<prefix>[A-Za-z][A-Za-z0-9_-]*)[\"']\s*:\s*"
        r"[\"'](?P<iri>https?://[^\"']*[#/])[\"']"
    )
    turtle_prefix = re.compile(
        r"@prefix\s+(?P<prefix>[A-Za-z][A-Za-z0-9_-]*):\s*"
        r"<(?P<iri>https?://[^>]+)>"
    )
    for pattern in (json_context, turtle_prefix):
        for match in pattern.finditer(text):
            prefixes[match.group("prefix")] = match.group("iri")
    return prefixes


def _table_roles(lines: Sequence[str]) -> dict[int, list[tuple[str, str]]]:
    """Return line-indexed table cell values with strong class/property roles."""

    roles: dict[int, list[tuple[str, str]]] = {}
    index = 0
    while index + 1 < len(lines):
        header_line = lines[index].strip()
        separator_line = lines[index + 1].strip()
        if not (header_line.startswith("|") and separator_line.startswith("|")):
            index += 1
            continue
        separator_cells = [cell.strip() for cell in separator_line.strip("|").split("|")]
        if not separator_cells or not all(
            cell and set(cell) <= {"-", ":"} for cell in separator_cells
        ):
            index += 1
            continue
        headers = [cell.strip().lower() for cell in header_line.strip("|").split("|")]
        column_roles: dict[int, str] = {}
        for column, header in enumerate(headers):
            normalized = " ".join(header.replace("`", "").split())
            if normalized in {
                "class",
                "classes",
                "cac class",
                "case/uco class",
                "uco class",
                "class / extension",
                "class / term",
            }:
                column_roles[column] = "class"
            elif normalized in {
                "property",
                "properties",
                "predicate",
                "predicates",
                "declared property",
                "ontology property",
            }:
                column_roles[column] = "property"
        row = index + 2
        while row < len(lines) and lines[row].strip().startswith("|"):
            cells = [cell.strip() for cell in lines[row].strip().strip("|").split("|")]
            for column, role in column_roles.items():
                if column < len(cells):
                    roles.setdefault(row, []).append((role, cells[column]))
            row += 1
        index = row
    return roles


def _section_classifications(lines: Sequence[str]) -> dict[int, str]:
    classifications: dict[int, str] = {}
    anti_level: int | None = None
    for index, line in enumerate(lines):
        match = _HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).lower()
            if anti_level is not None and level <= anti_level:
                anti_level = None
            if "anti-pattern" in title or "antipattern" in title:
                anti_level = level
        if anti_level is not None:
            classifications[index] = "anti-pattern"
    return classifications


def _directive_classifications(
    lines: Sequence[str], path: str
) -> tuple[dict[int, tuple[str, str]], list[RecipeLintFinding]]:
    classifications: dict[int, tuple[str, str]] = {}
    malformed: list[RecipeLintFinding] = []
    active: tuple[str, str, int] | None = None
    for index, line in enumerate(lines):
        start = _IGNORE_START_RE.match(line)
        end = _IGNORE_END_RE.match(line)
        if start:
            classification = start.group("classification")
            reason = start.group("reason").strip()
            if active is not None:
                malformed.append(
                    RecipeLintFinding(
                        path=path,
                        line=index + 1,
                        code="nested_ignore_directive",
                        term=classification,
                        message="recipe-lint ignore regions cannot be nested",
                    )
                )
            elif classification not in _ALLOWED_EXCLUSION_CLASSES:
                malformed.append(
                    RecipeLintFinding(
                        path=path,
                        line=index + 1,
                        code="unknown_ignore_classification",
                        term=classification,
                        message="recipe-lint exclusion classification is not allowed",
                    )
                )
            elif not reason:
                malformed.append(
                    RecipeLintFinding(
                        path=path,
                        line=index + 1,
                        code="ignore_reason_required",
                        term=classification,
                        message="recipe-lint exclusion requires a rationale",
                    )
                )
            else:
                active = (classification, reason, index)
            continue
        if end:
            classification = end.group("classification")
            if active is None or active[0] != classification:
                malformed.append(
                    RecipeLintFinding(
                        path=path,
                        line=index + 1,
                        code="unmatched_ignore_end",
                        term=classification,
                        message="recipe-lint ignore-end has no matching start",
                    )
                )
            else:
                active = None
            continue
        if active is not None:
            classifications[index] = (active[0], active[1])
    if active is not None:
        malformed.append(
            RecipeLintFinding(
                path=path,
                line=active[2] + 1,
                code="unclosed_ignore_directive",
                term=active[0],
                message="recipe-lint ignore-start has no matching ignore-end",
            )
        )
    return classifications, malformed


def _empty_content_data_facet_findings(
    lines: Sequence[str],
    *,
    path: str,
    section_classes: dict[int, str],
    directive_classes: dict[int, tuple[str, str]],
) -> list[RecipeLintFinding]:
    """Reject empty ContentDataFacet constructors and JSON-LD objects (#126)."""

    findings: list[RecipeLintFinding] = []
    in_fence = False
    fence_language = ""
    fence_start = 0
    fence_lines: list[str] = []

    def exclusion_for(line_index: int) -> tuple[str, str] | None:
        if line_index in directive_classes:
            return directive_classes[line_index]
        if line_index in section_classes:
            return "anti-pattern", "explicit Anti-pattern section"
        return None

    def flush_fence() -> None:
        if fence_language in {"python", "py"}:
            for offset, line in enumerate(fence_lines):
                if _JAVA_NEW_CONTENT_FACET_RE.search(line):
                    continue
                if not _EMPTY_PYTHON_CONTENT_FACET_RE.search(line):
                    continue
                line_index = fence_start + offset
                findings.append(
                    _finding(
                        path=path,
                        line=line_index + 1,
                        code="empty_content_data_facet",
                        term="ContentDataFacet()",
                        message=(
                            "ContentDataFacet() has no hash, size, MIME type, or "
                            "payload; record a real digest or omit the facet"
                        ),
                        role="class",
                        exclusion=exclusion_for(line_index),
                    )
                )
            return
        if fence_language not in {"json", "jsonld", "json-ld"}:
            return
        text = "\n".join(fence_lines)
        for match in _CONTENT_FACET_TYPE_RE.finditer(text):
            start = text.rfind("{", 0, match.start())
            if start < 0:
                continue
            depth = 0
            end = start
            for index, char in enumerate(text[start:], start):
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        end = index
                        break
            block = text[start : end + 1]
            if _CONTENT_FACET_SUBSTANCE_RE.search(block):
                continue
            line_index = fence_start + text[: match.start()].count("\n")
            findings.append(
                _finding(
                    path=path,
                    line=line_index + 1,
                    code="empty_content_data_facet",
                    term="ContentDataFacet",
                    message=(
                        "JSON-LD ContentDataFacet has no hash, size, MIME type, "
                        "or payload; record a real digest or omit the facet"
                    ),
                    role="class",
                    exclusion=exclusion_for(line_index),
                )
            )

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_fence:
                flush_fence()
                in_fence = False
                fence_language = ""
                fence_lines = []
            else:
                in_fence = True
                fence_language = stripped[3:].strip().lower()
                fence_start = index + 1
                fence_lines = []
            continue
        if in_fence:
            fence_lines.append(line)
            continue
        if _JAVA_NEW_CONTENT_FACET_RE.search(line):
            continue
        if _EMPTY_PYTHON_CONTENT_FACET_RE.search(line):
            findings.append(
                _finding(
                    path=path,
                    line=index + 1,
                    code="empty_content_data_facet",
                    term="ContentDataFacet()",
                    message=(
                        "ContentDataFacet() has no hash, size, MIME type, or "
                        "payload; record a real digest or omit the facet"
                    ),
                    role="class",
                    exclusion=exclusion_for(index),
                )
            )
    if in_fence:
        flush_fence()
    return findings


def _state_specific_charge_finding(
    *,
    path: str,
    line: int,
    term: str,
    role: str,
    exclusion: tuple[str, str] | None,
) -> RecipeLintFinding | None:
    local = term.rsplit(":", 1)[-1]
    if local not in _STATE_SPECIFIC_CHARGE_CLASSES:
        return None
    if exclusion and exclusion[0] == "anti-pattern":
        return None
    return _finding(
        path=path,
        line=line,
        code="state_specific_charge_class",
        term=term,
        message="jurisdiction-specific charge subclasses are outside SDK recipe scope; use StateCharge or FederalCharge",
        role=role,
        exclusion=exclusion,
    )


def _role_for_curie(
    line: str,
    term: str,
    table_role: str | None,
    fence_language: str,
) -> str:
    if table_role is not None:
        return table_role
    escaped = re.escape(term)
    if re.search(rf"[\"']@type[\"']\s*:\s*(?:\[[^\]]*)?[\"']{escaped}[\"']", line):
        return "class"
    if re.search(rf"\b(?:type|types)\s*=\s*(?:\[[^\]]*)?[\"']{escaped}[\"']", line):
        return "class"
    if re.search(rf"(?:\ba\b|rdf:type)\s+{escaped}(?:\s|[;,\.]|$)", line):
        return "class"
    for key_match in _JSON_KEY_RE.finditer(line):
        if key_match.group("term") == term:
            return "property"
    stripped = line.strip()
    if fence_language in {"ttl", "turtle"} and re.match(
        rf"^(?:{escaped}|;\s*{escaped})\s+", stripped
    ):
        return "property"
    return "term"


def _exclusion_for(
    *,
    line_index: int,
    role: str,
    prefix: str,
    local: str,
    section_classes: dict[int, str],
    directive_classes: dict[int, tuple[str, str]],
) -> tuple[str, str] | None:
    if line_index in directive_classes:
        return directive_classes[line_index]
    if "*" in local:
        return "wildcard", "wildcard catalog notation"
    if line_index in section_classes:
        return "anti-pattern", "explicit Anti-pattern section"
    if role == "term" and prefix in _INSTANCE_PREFIXES:
        return "instance-id", "generic example/knowledge-base identifier"
    if role == "term" and prefix in _CONTROLLED_LITERAL_PREFIXES:
        return "controlled-literal", "documented controlled string/tag value"
    if role == "term" and re.fullmatch(r"[0-9A-Fa-f]{2}", prefix) and re.fullmatch(
        r"[0-9A-Fa-f]{2}(?:[.-][0-9A-Fa-f]{2})*", local
    ):
        return "instance-id", "literal hardware-address fragment"
    if role == "term" and local in {"full", "packages"}:
        return "controlled-literal", "CLI/configuration selector, not an RDF term"
    return None


def _finding(
    *,
    path: str,
    line: int,
    code: str,
    term: str,
    message: str,
    role: str,
    exclusion: tuple[str, str] | None,
) -> RecipeLintFinding:
    return RecipeLintFinding(
        path=path,
        line=line,
        code=code,
        term=term,
        message=message,
        role=role,
        excluded=exclusion is not None,
        classification=exclusion[0] if exclusion else "",
        reason=exclusion[1] if exclusion else "",
    )


def _bare_terms(cell: str) -> Iterable[str]:
    inline = _INLINE_CODE_RE.findall(cell)
    source = " ".join(inline) if inline else cell
    yield from re.findall(r"\b[A-Z][A-Za-z0-9]*\b", source)


def _diagram_edge_labels(line: str) -> list[str]:
    labels: list[str] = []
    patterns = (
        re.compile(r"[├└]\s*──\s*([A-Za-z][A-Za-z0-9_:-]*)\s*──[▶>]"),
        re.compile(r"--\s*([A-Za-z][A-Za-z0-9_:-]*)\s*-->"),
        re.compile(r"-\[\s*([A-Za-z][A-Za-z0-9_:-]*)\s*\]->"),
        re.compile(r"-->|──▶"),
    )
    for pattern in patterns[:3]:
        labels.extend(match.group(1) for match in pattern.finditer(line))
    return labels


def lint_recipe_text(
    text: str,
    *,
    path: str,
    catalog: OntologyCatalog,
    relationship_kinds: frozenset[str],
) -> tuple[list[RecipeLintFinding], int]:
    """Lint one recipe's Markdown text with a pre-built ontology catalog."""

    lines = text.splitlines()
    prefixes = _recipe_prefixes(text, catalog.prefixes)
    table_roles = _table_roles(lines)
    section_classes = _section_classifications(lines)
    directive_classes, findings = _directive_classifications(lines, path)
    terms_checked = 0
    in_fence = False
    fence_language = ""

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_fence:
                in_fence = False
                fence_language = ""
            else:
                in_fence = True
                fence_language = stripped[3:].strip().lower()
            continue

        role_cells = table_roles.get(index) or []
        table_role_by_term: dict[str, str] = {}
        for table_role, cell in role_cells:
            for match in _CURIE_RE.finditer(cell):
                table_role_by_term[match.group(0)] = table_role
            for term in _bare_terms(cell):
                terms_checked += 1
                known_names = (
                    catalog.class_local_names
                    if table_role == "class"
                    else catalog.property_local_names
                )
                if term in known_names:
                    state_specific = _state_specific_charge_finding(
                        path=path,
                        line=index + 1,
                        term=term,
                        role=table_role,
                        exclusion=_exclusion_for(
                            line_index=index,
                            role=table_role,
                            prefix="",
                            local=term,
                            section_classes=section_classes,
                            directive_classes=directive_classes,
                        ),
                    )
                    if state_specific is not None:
                        findings.append(state_specific)
                    continue
                exclusion = _exclusion_for(
                    line_index=index,
                    role=table_role,
                    prefix="",
                    local=term,
                    section_classes=section_classes,
                    directive_classes=directive_classes,
                )
                findings.append(
                    _finding(
                        path=path,
                        line=index + 1,
                        code=f"undeclared_bare_{table_role}",
                        term=term,
                        message=f"{table_role} table entry is not declared by the catalog",
                        role=table_role,
                        exclusion=exclusion,
                    )
                )

        seen_line_terms: set[tuple[str, str]] = set()
        for match in _CURIE_RE.finditer(line):
            term = match.group(0)
            prefix = match.group("prefix")
            local = match.group("local")
            table_role = table_role_by_term.get(term)
            role = _role_for_curie(line, term, table_role, fence_language)
            dedupe_key = (term, role)
            if dedupe_key in seen_line_terms:
                continue
            seen_line_terms.add(dedupe_key)
            terms_checked += 1
            exclusion = _exclusion_for(
                line_index=index,
                role=role,
                prefix=prefix,
                local=local,
                section_classes=section_classes,
                directive_classes=directive_classes,
            )
            namespace = prefixes.get(prefix)
            if namespace is None:
                findings.append(
                    _finding(
                        path=path,
                        line=index + 1,
                        code="unknown_prefix",
                        term=term,
                        message=f"prefix {prefix!r} is not registered by core, an operational extension, or a profiled ontology",
                        role=role,
                        exclusion=exclusion,
                    )
                )
                continue
            iri = f"{namespace}{local}"
            if namespace in _FOUNDATIONAL_NAMESPACES:
                continue
            if role == "class":
                if iri in catalog.classes or iri in catalog.other_terms:
                    state_specific = _state_specific_charge_finding(
                        path=path,
                        line=index + 1,
                        term=term,
                        role=role,
                        exclusion=exclusion,
                    )
                    if state_specific is not None:
                        findings.append(state_specific)
                    continue
                code = "role_mismatch" if iri in catalog.properties else "undeclared_class"
                message = (
                    "declared property is used as an rdf:type class"
                    if code == "role_mismatch"
                    else "class is not declared by the catalog"
                )
            elif role == "property":
                if iri in catalog.properties or iri in catalog.other_terms:
                    continue
                code = "role_mismatch" if iri in catalog.classes else "undeclared_property"
                message = (
                    "declared class is used as an RDF predicate"
                    if code == "role_mismatch"
                    else "property is not declared by the catalog"
                )
            else:
                if iri in catalog.classes or iri in catalog.properties or iri in catalog.other_terms:
                    continue
                code = "undeclared_term"
                message = "term is not declared by the catalog"
            findings.append(
                _finding(
                    path=path,
                    line=index + 1,
                    code=code,
                    term=term,
                    message=message,
                    role=role,
                    exclusion=exclusion,
                )
            )

        for pattern in _REL_KIND_PATTERNS:
            for match in pattern.finditer(line):
                kind = match.group("kind")
                terms_checked += 1
                if kind in relationship_kinds:
                    continue
                exclusion = _exclusion_for(
                    line_index=index,
                    role="relationship-kind",
                    prefix="",
                    local=kind,
                    section_classes=section_classes,
                    directive_classes=directive_classes,
                )
                findings.append(
                    _finding(
                        path=path,
                        line=index + 1,
                        code="unregistered_relationship_kind",
                        term=kind,
                        message="kindOfRelationship value is not in the vendored registry",
                        role="relationship-kind",
                        exclusion=exclusion,
                    )
                )

        # Prose and tables sometimes name a custom Relationship kind without
        # assignment syntax.  Check relationship-like inline-code labels when
        # the surrounding sentence explicitly discusses a relationship/link.
        lower_line = line.lower()
        if any(marker in lower_line for marker in ("relationship", " edge", " link")):
            for token in _INLINE_CODE_RE.findall(line):
                token = token.strip('"\' ')
                if ":" in token or token in relationship_kinds:
                    continue
                if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*(?:[_-][A-Za-z0-9]+)+", token):
                    continue
                legacy_lowercase_kinds = {
                    "attributed-account",
                    "attributed-controller",
                    "custody-transfer",
                    "has-role",
                    "supersededBy",
                    "used_equipment",
                }
                if token not in legacy_lowercase_kinds and (
                    not token[0].isupper() or token.isupper()
                ):
                    continue
                terms_checked += 1
                exclusion = _exclusion_for(
                    line_index=index,
                    role="relationship-kind",
                    prefix="",
                    local=token,
                    section_classes=section_classes,
                    directive_classes=directive_classes,
                )
                findings.append(
                    _finding(
                        path=path,
                        line=index + 1,
                        code="unregistered_relationship_reference",
                        term=token,
                        message="inline Relationship label is not in the vendored registry",
                        role="relationship-kind",
                        exclusion=exclusion,
                    )
                )

        for match in re.finditer(
            r"`(?P<token>[A-Za-z][A-Za-z0-9_-]*)`\s+"
            r"(?:relationship|relationships|edge|edges|link|links)\b",
            line,
            flags=re.IGNORECASE,
        ):
            token = match.group("token")
            if token in relationship_kinds or not token[0].isupper() or token == "Relationship":
                continue
            terms_checked += 1
            exclusion = _exclusion_for(
                line_index=index,
                role="relationship-kind",
                prefix="",
                local=token,
                section_classes=section_classes,
                directive_classes=directive_classes,
            )
            findings.append(
                _finding(
                    path=path,
                    line=index + 1,
                    code="unregistered_relationship_reference",
                    term=token,
                    message="inline Relationship label is not in the vendored registry",
                    role="relationship-kind",
                    exclusion=exclusion,
                )
            )

        if in_fence and fence_language in {"", "text", "mermaid", "ascii"}:
            for label in _diagram_edge_labels(line):
                terms_checked += 1
                label_prefix = ""
                if ":" in label:
                    label_prefix, local = label.split(":", 1)
                    namespace = prefixes.get(label_prefix)
                    valid = namespace in _FOUNDATIONAL_NAMESPACES or namespace is not None and (
                        f"{namespace}{local}" in catalog.properties
                        or f"{namespace}{local}" in catalog.other_terms
                    )
                else:
                    local = label
                    valid = label in relationship_kinds
                if valid:
                    continue
                exclusion = _exclusion_for(
                    line_index=index,
                    role="property",
                    prefix=label_prefix,
                    local=local,
                    section_classes=section_classes,
                    directive_classes=directive_classes,
                )
                findings.append(
                    _finding(
                        path=path,
                        line=index + 1,
                        code="undeclared_diagram_edge",
                        term=label,
                        message="labeled canonical diagram edge is neither a declared property nor a registered relationship kind",
                        role="property",
                        exclusion=exclusion,
                    )
                )

    findings.extend(
        _empty_content_data_facet_findings(
            lines,
            path=path,
            section_classes=section_classes,
            directive_classes=directive_classes,
        )
    )

    # Stable output and no duplicate diagnostics from overlapping extractors.
    unique: dict[tuple[object, ...], RecipeLintFinding] = {}
    for item in findings:
        key = (item.path, item.line, item.code, item.term, item.role, item.excluded)
        unique[key] = item
    return sorted(unique.values(), key=lambda item: (item.line, item.code, item.term)), terms_checked


def operational_recipe_paths(
    project_root: Path = PROJECT_ROOT,
    selected_paths: Sequence[Path] | None = None,
) -> list[Path]:
    if selected_paths:
        return sorted(path.resolve() for path in selected_paths)
    return sorted((project_root / "docs" / "recipes").glob("*.md"))


def lint_recipes(
    *,
    project_root: Path = PROJECT_ROOT,
    selected_paths: Sequence[Path] | None = None,
    catalog: OntologyCatalog | None = None,
    relationship_kinds: frozenset[str] | None = None,
) -> RecipeLintReport:
    """Lint all operational recipes (including authoring guidance, not INDEX)."""

    if catalog is None:
        try:
            catalog = build_catalog(project_root)
        except Exception as exc:  # noqa: BLE001 - fail closed with typed summary
            return RecipeLintReport(
                verification_errors=[
                    f"catalog_load_failed:{type(exc).__name__}:{exc}"
                ]
            )
    known_kinds = relationship_kinds
    if known_kinds is None:
        registry_path = project_root / "mcp_server" / "relationship_kinds.json"
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            known_kinds = frozenset(
                kind
                for entry in (registry.get("vocabularies") or {}).values()
                for kind in (entry.get("kinds") or [])
                if isinstance(kind, str)
            )
        except Exception as exc:  # noqa: BLE001 - fail closed with typed summary
            return RecipeLintReport(
                verification_errors=[
                    f"relationship_registry_load_failed:{type(exc).__name__}:{exc}"
                ]
            )

    assert known_kinds is not None
    report = RecipeLintReport(
        catalog_extensions=catalog.extensions,
        catalog_profiles=catalog.profiles,
    )
    if catalog.parse_errors:
        report.verification_errors.extend(
            f"ontology_parse_error:{error}" for error in catalog.parse_errors
        )
        return report

    for path in operational_recipe_paths(project_root, selected_paths):
        if path.name == "INDEX.md":
            continue
        try:
            relative = path.resolve().relative_to(project_root.resolve()).as_posix()
        except ValueError:
            relative = str(path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            report.verification_errors.append(
                f"recipe_read_failed:{relative}:{type(exc).__name__}:{exc}"
            )
            continue
        findings, checked = lint_recipe_text(
            text,
            path=relative,
            catalog=catalog,
            relationship_kinds=known_kinds,
        )
        report.files_checked += 1
        report.terms_checked += checked
        report.findings.extend(findings)
    return report


def _print_human(report: RecipeLintReport, *, show_exclusions: bool = False) -> None:
    for finding in report.findings:
        if finding.excluded and not show_exclusions:
            continue
        status = "EXCLUDED" if finding.excluded else "ERROR"
        suffix = (
            f" [{finding.classification}: {finding.reason}]"
            if finding.excluded
            else ""
        )
        print(
            f"{status} {finding.path}:{finding.line}: {finding.code}: "
            f"{finding.term} ({finding.role}) - {finding.message}{suffix}"
        )
    for error in report.verification_errors:
        print(f"ERROR verification: {error}")
    print(
        "Recipe ontology lint: "
        f"files={report.files_checked} terms={report.terms_checked} "
        f"errors={len(report.errors)} exclusions={len(report.exclusions)} "
        f"ok={str(report.ok).lower()}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional recipe Markdown paths (default: every operational recipe)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument(
        "--show-exclusions",
        action="store_true",
        help="Include classified exclusions in human-readable output",
    )
    args = parser.parse_args(argv)
    selected = [
        path if path.is_absolute() else (PROJECT_ROOT / path)
        for path in args.paths
    ]
    report = lint_recipes(selected_paths=selected or None)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        _print_human(report, show_exclusions=args.show_exclusions)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
