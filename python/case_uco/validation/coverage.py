"""Closed-world concept coverage checking for CASE/UCO/extension graphs.

SHACL validation only evaluates shapes whose target classes exist, so a graph
that types nodes with classes (or uses properties) that no supported ontology
declares can pass ``case_validate`` silently. This module closes that gap:
every class and property IRI used by a submitted graph must be declared in
the CASE/UCO core ontologies or in a supported extension ontology, otherwise
the graph is rejected with guidance to draft a change proposal or add the
concept to an extension ontology.

Three layers of checking:

1. **Declared-term membership** — every class/property must be declared in a
   supported ontology (core, extension, pinned upper-ontology registry, or a
   foundational W3C namespace).
2. **Exact upper-ontology terms** — profiled upper ontologies (BFO, gUFO,
   PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF) are validated against the
   pinned term registry (``upper_ontology_registry.json``) instead of
   whole-namespace acceptance, so fabricated terms inside a profiled
   namespace fail. **Strict mode requires an explicit profile selection**
   (CQ-29): ``profiles=None`` / empty authorizes *zero* upper profiles —
   upper-namespace terms fail as ``profile_not_selected`` rather than
   silently accepting the full registry. Recipe validation always passes
   ``profiles=[...]`` so exemplars keep working.
3. **RDF role awareness** — declarations are tracked by role (class,
   property, shape, individual). A declared class used as a predicate, or a
   declared property used as an ``rdf:type`` class, is reported as a role
   mismatch rather than silently accepted. OWL punning (e.g. the ATT&CK
   ``uco-action:Technique`` metaclass pattern where a term is both an
   ``owl:Class`` and an individual) is supported: any term declared as a
   class may be used as an ``rdf:type`` object.

**Same-bundle coverage (CQ-27/CQ-28):** when a ``ResolvedValidationBundle``
is passed via ``bundle=...``, declared extension/profile terms are loaded
*only* from that bundle's exact resources (same subset/full mode and
fingerprint as SHACL). Coverage must not accept terms from full-manifest
files that SHACL never loaded.

Foundational W3C vocabulary policy: terms in RDF, RDFS, OWL, XSD, SHACL,
SKOS, Dublin Core, and Web Annotation namespaces are accepted by namespace
because they are governed by W3C specifications outside this SDK and are
imported wholesale by the supported ontologies.

Once an extension ontology (or the upstream ontology) declares the concept,
the same graph passes without further changes — the declared-term set is
recomputed whenever the ontology files on disk change (the cache key includes
a content fingerprint of every ontology file, so a term added, removed, or
renamed during the same server process is picked up on the next check).
"""

from __future__ import annotations

import os
import hashlib
import json
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from case_uco.validation.bundle import ResolvedValidationBundle

from case_uco.validation.graph import PROJECT_ROOT

UPPER_ONTOLOGY_REGISTRY_PATH = Path(__file__).resolve().parent / "upper_ontology_registry.json"

# Namespaces whose terms are governed outside this SDK (W3C standards and
# vocabularies imported by the supported ontologies). Terms in these
# namespaces are never reported as undeclared. This is a deliberate,
# documented policy: these are foundational specification vocabularies, not
# domain ontologies, and the supported ontologies import them wholesale.
STANDARD_NAMESPACE_PREFIXES: tuple[str, ...] = (
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/2001/XMLSchema#",
    "http://www.w3.org/ns/shacl#",
    "http://www.w3.org/2004/02/skos/core#",
    "http://purl.org/dc/terms/",
    "http://purl.org/dc/elements/1.1/",
    # W3C Web Annotation Data Model (https://www.w3.org/TR/annotation-model/),
    # used by document-annotation sidecar graphs.
    "http://www.w3.org/ns/oa#",
)

# Namespaces of external/upper ontologies that UCO maintains alignment
# profiles for, published by the CDO project as CDO-Shapes-* repositories
# (https://github.com/Cyber-Domain-Ontology). Because a UCO profile exists,
# graphs may use these ontologies' terms directly — but only *exact declared
# terms* from the pinned releases recorded in upper_ontology_registry.json,
# and only when the corresponding profile is explicitly selected (CQ-29).
# Discover the profiles with the get_uco_profiles() MCP tool. See
# docs/recipes/extensions.md. Regenerate the registry with
# mcp_server/tools/build_upper_ontology_registry.py.
# Map stable profile IDs to the namespace prefixes they authorize for
# profile-selective concept coverage (issue #68).
PROFILE_ID_TO_NAMESPACE_PREFIXES: dict[str, tuple[str, ...]] = {
    "bfo": ("http://purl.obolibrary.org/obo/BFO_",),
    "gufo": ("http://purl.org/nemo/gufo#",),
    "prov-o": ("http://www.w3.org/ns/prov#",),
    "time": ("http://www.w3.org/2006/time#",),
    "owl-time": ("http://www.w3.org/2006/time#",),
    "geosparql": (
        "http://www.opengis.net/ont/geosparql#",
        "http://www.opengis.net/ont/sf#",
    ),
    "foaf": ("http://xmlns.com/foaf/0.1/",),
    "org": ("http://www.w3.org/ns/org#",),
    "prof": ("http://www.w3.org/ns/dx/prof/",),
    # SDK-pinned without a CDO-Shapes profile (#60).
    "qudt": (
        "http://qudt.org/schema/qudt/",
        "http://qudt.org/vocab/unit/",
        "http://qudt.org/vocab/quantitykind/",
        "http://qudt.org/vocab/prefix/",
    ),
    "sosa": ("http://www.w3.org/ns/sosa/",),
    "ssn": ("http://www.w3.org/ns/ssn/",),
}

CORE_ONTOLOGY_GLOBS: tuple[str, ...] = (
    "ontology/UCO/ontology/uco/*/*.ttl",
    "ontology/UCO/ontology/co/*.ttl",
    "ontology/CASE/ontology/*/*.ttl",
)

GUIDANCE = (
    "Undeclared classes/properties found. Every term must be declared in "
    "CASE/UCO or a supported extension ontology before the graph can be "
    "accepted. Options: (1) draft an upstream change proposal — run "
    "check_existing_proposals(concept) then draft_change_proposal(...) per "
    "docs/recipes/change-proposal.md; (2) create or update an extension "
    "ontology declaring the terms (docs/recipes/extensions.md) and register "
    "it in the extension manifest / validation subset; (3) if the concept "
    "exists in an external/upper ontology, check get_uco_profiles() — exact "
    "declared terms from ontologies with a UCO profile (BFO, gUFO, PROV-O, "
    "OWL-Time, GeoSPARQL, FOAF, ORG, PROF) or an SDK-pinned profile (QUDT, "
    "SOSA, SSN) are accepted when that profile is "
    "explicitly selected via profiles=[...]. Re-run validate_graph afterwards "
    "— the check passes as soon as the concept is declared."
)

UPPER_TERM_GUIDANCE = (
    "Terms flagged as unknown_upper_ontology_terms sit inside a profiled "
    "upper-ontology namespace (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, "
    "ORG, PROF, QUDT, SOSA, SSN) but are not declared by the pinned release of "
    "that ontology (see case_uco/validation/upper_ontology_registry.json for "
    "pinned versions). This includes values such as QUDT unit and quantity-kind "
    "IRIs. Check the ontology's specification for the correct term name (for "
    "QUDT units, use the lookup_qudt_units MCP tool); do not invent terms in "
    "external namespaces. QUDT 3 replaced qudt:unit with qudt:hasUnit and "
    "qudt:numericValue with qudt:value."
)

ROLE_MISMATCH_GUIDANCE = (
    "Terms flagged as role_mismatches are declared in a supported ontology "
    "but used in the wrong RDF position: a class cannot be used as a "
    "predicate, and a property cannot be the object of rdf:type. Punned "
    "class/individual terms (e.g. ATT&CK techniques via the "
    "uco-action:Technique metaclass) are supported — any declared owl:Class "
    "is valid as an rdf:type object."
)

PROFILE_NOT_SELECTED_GUIDANCE = (
    "Terms flagged as profile_not_selected are declared by a profiled "
    "upper ontology that was not included in this validation bundle. "
    "Add the required profile to profiles=[...] or remove the term. "
    "When profiles is omitted or empty, zero upper profiles are authorized "
    "(strict fail-closed mode)."
)

SUBSET_GAP_GUIDANCE = (
    "If a flagged CAC term exists in ontology/cac/_registry.json but was "
    "rejected here, it is outside the selected validation subset — not a "
    "missing ontology concept. Use extensions=['cac:missing-child'] for "
    "abduction, case-management, and temporal terms, or "
    "extensions=['cac:full'] for the complete manifest. Do not mint "
    "duplicate terms to work around a subset miss."
)

PARSE_ERROR_GUIDANCE = (
    "One or more ontology resources failed to parse while loading declared "
    "terms. Restore or fix the listed files; an unverifiable graph is never "
    "reported as conformant."
)


@dataclass(frozen=True)
class ProfileNotSelected:
    """Structured report for an upper-ontology term whose profile was not selected."""

    iri: str
    required_profile: str
    used_as: str  # "class" | "property" | "value"
    selected_profiles: tuple[str, ...]


@dataclass(frozen=True)
class OntologyParseError:
    path: str
    role: str
    error: str
    profile_id: str | None = None
    extension: str | None = None


@dataclass(frozen=True)
class ConceptCoverageReport:
    """Result of a closed-world concept coverage check.

    ``verification_status`` distinguishes a check that fully ran
    (``"complete"``) from one that could not perform a required stage
    (``"could_not_verify"``). Fail-closed policy: an inability to verify is
    never reported as a pass — when the pinned upper-ontology registry is
    missing or malformed and the graph uses profiled upper-ontology terms,
    the report is not ok and ``verification_errors`` names the failed stage.
    """

    ok: bool
    undeclared_classes: tuple[str, ...] = ()
    undeclared_properties: tuple[str, ...] = ()
    unknown_upper_ontology_terms: tuple[str, ...] = ()
    role_mismatches: tuple[tuple[str, str, str], ...] = ()  # (iri, declared_role, used_as)
    profile_not_selected: tuple[ProfileNotSelected, ...] = ()
    checked_class_count: int = 0
    checked_property_count: int = 0
    guidance: str = field(default="")
    verification_status: str = "complete"
    verification_errors: tuple[str, ...] = ()
    bundle_fingerprint: str | None = None
    ontology_parse_errors: tuple[OntologyParseError, ...] = ()

    @property
    def undeclared_total(self) -> int:
        return (
            len(self.undeclared_classes)
            + len(self.undeclared_properties)
            + len(self.unknown_upper_ontology_terms)
            + len(self.role_mismatches)
            + len(self.profile_not_selected)
        )


@dataclass(frozen=True)
class DeclaredTerms:
    """Declared ontology terms, tracked by RDF role.

    ``unknown_role`` holds subjects whose role could not be determined from
    the ontology files (annotation-only declarations, individuals, ontology
    metadata). They are accepted in any position for backward compatibility.
    """

    classes: frozenset[str]
    properties: frozenset[str]
    shapes: frozenset[str]
    unknown_role: frozenset[str]
    parse_errors: tuple[OntologyParseError, ...] = ()

    def __contains__(self, iri: str) -> bool:
        return (
            iri in self.classes
            or iri in self.properties
            or iri in self.shapes
            or iri in self.unknown_role
        )


_DECLARED_CACHE: dict[tuple[Any, ...], DeclaredTerms] = {}
_DECLARED_CACHE_MAX_ENTRIES = 16
_DECLARED_CACHE_LOCK = threading.RLock()
_UPPER_REGISTRY_CACHE: dict[str, dict[str, Any]] = {}
_UPPER_REGISTRY_LOCK = threading.RLock()


def clear_declared_term_cache() -> None:
    """Drop every cached declared-term set.

    Ontology writes performed through supported tools (extension scaffolding,
    proposal-local declarations, package generation) may call this to force a
    reload, although the content-fingerprint cache key already detects file
    additions, removals, and modifications automatically.
    """

    with _DECLARED_CACHE_LOCK:
        _DECLARED_CACHE.clear()
    with _UPPER_REGISTRY_LOCK:
        _UPPER_REGISTRY_CACHE.clear()


def _built_ontology_path() -> Path | None:
    """The case-utils build ``case_validate --built-version`` loads, if installed.

    It carries the imported dependencies (the Collections Ontology ``co:``
    terms, for example) that the vendored submodules leave uninitialized.
    """
    import importlib.util

    from case_uco.validation.graph import DEFAULT_BUILT_VERSION

    try:
        spec = importlib.util.find_spec("case_utils.ontology")
    except (ImportError, ValueError):
        return None
    if spec is None or not spec.submodule_search_locations:
        return None
    for location in spec.submodule_search_locations:
        candidate = Path(location) / f"{DEFAULT_BUILT_VERSION}.ttl"
        if candidate.is_file():
            return candidate
    return None


def _core_ontology_paths(project_root: Path) -> list[Path]:
    paths: list[Path] = []
    for pattern in CORE_ONTOLOGY_GLOBS:
        for path in sorted(project_root.glob(pattern)):
            if "master" in path.parts or "dependencies" in path.parts:
                continue
            paths.append(path)
    built = _built_ontology_path()
    if built is not None:
        paths.append(built)
    return paths


def _extension_ontology_paths(project_root: Path, extensions: list[str]) -> list[Path]:
    """Load extension ontology paths in the same mode SHACL uses (CQ-28).

    Default (no suffix) prefers ``validation-subset.json``; ``:full`` loads
    the full manifest; other suffixes load ``validation-subset-<name>.json``.
    Callers that need literal same-bundle semantics should pass ``bundle=``.
    """
    from case_uco.validation.graph import (
        load_extension_ontology_paths,
        parse_extension_token,
        resolve_extension_dependencies,
    )

    paths: list[Path] = []
    for ext_name in resolve_extension_dependencies(extensions, project_root):
        clean_name, mode = parse_extension_token(ext_name)
        paths.extend(
            load_extension_ontology_paths(clean_name, mode=mode, project_root=project_root)
        )
    return paths


def _ontology_fingerprint(paths: list[Path]) -> str:
    """Content-addressed fingerprint: path + sha256 of every ontology file (CQ-32)."""

    hasher = hashlib.sha256()
    for path in paths:
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            hasher.update(f"{path}:missing;".encode())
            continue
        hasher.update(f"{path}:{digest};".encode())
    return hasher.hexdigest()


def _parse_ontology_file(
    path: Path,
    *,
    role: str = "ontology",
    profile_id: str | None = None,
    extension: str | None = None,
) -> tuple[Any | None, OntologyParseError | None]:
    """Parse one ontology file; fail closed on errors (CQ-31)."""
    import rdflib

    graph = rdflib.Graph()
    suffix = path.suffix.lower()
    if suffix in {".owl", ".rdf", ".xml"}:
        fmt = "xml"
    elif suffix in {".jsonld", ".json-ld", ".json"}:
        fmt = "json-ld"
    else:
        fmt = "turtle"
    try:
        graph.parse(str(path), format=fmt)
    except Exception as exc:  # noqa: BLE001 — surface every parse failure
        return None, OntologyParseError(
            path=str(path),
            role=role,
            error=f"{type(exc).__name__}: {exc}",
            profile_id=profile_id,
            extension=extension,
        )
    return graph, None


def _collect_declared_from_graphs(
    parsed: list[tuple[Path, Any, str, str | None, str | None]],
) -> DeclaredTerms:
    import rdflib
    from rdflib import OWL, RDF, RDFS, URIRef
    from rdflib.namespace import SH

    class_types = {OWL.Class, RDFS.Class}
    property_types = {
        OWL.ObjectProperty,
        OWL.DatatypeProperty,
        OWL.AnnotationProperty,
        OWL.FunctionalProperty,
        OWL.InverseFunctionalProperty,
        OWL.TransitiveProperty,
        OWL.SymmetricProperty,
        RDF.Property,
    }
    shape_types = {SH.NodeShape, SH.PropertyShape}

    classes: set[str] = set()
    properties: set[str] = set()
    shapes: set[str] = set()
    subjects_seen: set[str] = set()
    parse_errors: list[OntologyParseError] = []

    for path, graph, role, profile_id, extension in parsed:
        if graph is None:
            continue
        for subject in graph.subjects():
            if isinstance(subject, URIRef):
                subjects_seen.add(str(subject))

        for subject, rdf_type in graph.subject_objects(RDF.type):
            if not isinstance(subject, URIRef):
                continue
            iri = str(subject)
            if rdf_type in class_types or rdf_type == RDFS.Datatype:
                classes.add(iri)
            elif rdf_type in property_types:
                properties.add(iri)
            elif rdf_type in shape_types:
                shapes.add(iri)

        for subject in graph.subjects(RDFS.subClassOf):
            if isinstance(subject, URIRef):
                classes.add(str(subject))
        for obj in graph.objects(None, RDFS.subClassOf):
            if isinstance(obj, URIRef):
                classes.add(str(obj))
        for pred in (RDFS.subPropertyOf, RDFS.domain, RDFS.range):
            for subject in graph.subjects(pred):
                if isinstance(subject, URIRef):
                    properties.add(str(subject))
        for pred in (RDFS.domain, RDFS.range):
            for obj in graph.objects(None, pred):
                if isinstance(obj, URIRef):
                    classes.add(str(obj))
        for obj in graph.objects(None, SH.targetClass):
            if isinstance(obj, URIRef):
                classes.add(str(obj))
        for obj in graph.objects(None, SH.path):
            if isinstance(obj, URIRef):
                properties.add(str(obj))
        sh_class = URIRef("http://www.w3.org/ns/shacl#class")
        for obj in graph.objects(None, sh_class):
            if isinstance(obj, URIRef):
                classes.add(str(obj))

    shapes -= classes | properties
    unknown_role = subjects_seen - classes - properties - shapes

    return DeclaredTerms(
        classes=frozenset(classes),
        properties=frozenset(properties),
        shapes=frozenset(shapes),
        unknown_role=frozenset(unknown_role),
        parse_errors=tuple(parse_errors),
    )


def load_declared_terms(
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
    extensions: list[str] | None = None,
    *,
    bundle: ResolvedValidationBundle | None = None,
    fail_on_parse_error: bool = True,
) -> DeclaredTerms:
    """Return every IRI declared in supported ontologies, tracked by role.

    When ``bundle`` is provided, extension/profile terms come **only** from
    that bundle's resources (CQ-27/CQ-28). Core CASE/UCO ontologies are always
    included. Parse failures are reported (and fail closed when
    ``fail_on_parse_error`` is True) rather than silently skipped (CQ-31).

    Results are cached under a content-addressed fingerprint (CQ-32).
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    path_meta: list[tuple[Path, str, str | None, str | None]] = []
    for path in _core_ontology_paths(project_root):
        path_meta.append((path, "ontology", None, None))

    if bundle is not None:
        for resource in bundle.resources:
            path_meta.append(
                (
                    Path(resource.absolute_path),
                    resource.role,
                    resource.profile_id,
                    resource.extension,
                )
            )
    else:
        for path in _extension_ontology_paths(project_root, extensions or []):
            path_meta.append((path, "ontology", None, None))

    # Deduplicate while preserving order.
    seen: set[str] = set()
    unique_meta: list[tuple[Path, str, str | None, str | None]] = []
    for path, role, profile_id, extension in path_meta:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        unique_meta.append((path, role, profile_id, extension))

    paths_only = [p for p, *_ in unique_meta]
    cache_key = (
        str(project_root.resolve()),
        bundle.fingerprint if bundle is not None else None,
        tuple(sorted(extensions or [])) if bundle is None else (),
        _ontology_fingerprint(paths_only),
    )

    with _DECLARED_CACHE_LOCK:
        cached = _DECLARED_CACHE.get(cache_key)
        if cached is not None:
            if fail_on_parse_error and cached.parse_errors:
                return cached
            if not cached.parse_errors or not fail_on_parse_error:
                return cached

    parsed: list[tuple[Path, Any, str, str | None, str | None]] = []
    parse_errors: list[OntologyParseError] = []
    for path, role, profile_id, extension in unique_meta:
        graph, err = _parse_ontology_file(
            path, role=role, profile_id=profile_id, extension=extension
        )
        if err is not None:
            parse_errors.append(err)
            continue
        parsed.append((path, graph, role, profile_id, extension))

    result = _collect_declared_from_graphs(parsed)
    if parse_errors:
        result = DeclaredTerms(
            classes=result.classes,
            properties=result.properties,
            shapes=result.shapes,
            unknown_role=result.unknown_role,
            parse_errors=tuple(parse_errors),
        )

    with _DECLARED_CACHE_LOCK:
        if len(_DECLARED_CACHE) >= _DECLARED_CACHE_MAX_ENTRIES:
            _DECLARED_CACHE.pop(next(iter(_DECLARED_CACHE)))
        _DECLARED_CACHE[cache_key] = result
    return result


def _load_upper_registry() -> tuple[dict[str, Any] | None, str | None]:
    """Load the pinned upper-ontology term registry (role-aware).

    Returns ``(registry, error)``. ``registry`` is ``{"classes": frozenset,
    "properties": frozenset, "individuals": frozenset, "datatypes":
    frozenset}`` unioned across all profiled ontologies. ``error`` is a typed
    code when the registry is unusable: ``upper_ontology_registry_missing``,
    ``upper_ontology_registry_malformed``, or
    ``upper_ontology_registry_provenance_invalid``.

    Fail-closed policy (issue #55): an unusable registry never degrades to
    whole-namespace acceptance. ``check_graph_concepts`` reports
    ``could_not_verify`` for any graph that uses profiled upper-ontology
    terms while the registry is unavailable.
    """

    if not UPPER_ONTOLOGY_REGISTRY_PATH.is_file():
        return None, "upper_ontology_registry_missing"
    try:
        raw_bytes = UPPER_ONTOLOGY_REGISTRY_PATH.read_bytes()
    except OSError:
        return None, "upper_ontology_registry_missing"
    content_hash = hashlib.sha256(raw_bytes).hexdigest()
    cache_key = f"{UPPER_ONTOLOGY_REGISTRY_PATH}:{content_hash}"
    with _UPPER_REGISTRY_LOCK:
        cached = _UPPER_REGISTRY_CACHE.get(cache_key)
        if cached is not None:
            return cached, None
    try:
        raw = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, "upper_ontology_registry_malformed"
    ontologies = raw.get("ontologies")
    if not isinstance(ontologies, dict) or not ontologies:
        return None, "upper_ontology_registry_malformed"
    merged: dict[str, set[str]] = {
        "classes": set(),
        "properties": set(),
        "individuals": set(),
        "datatypes": set(),
    }
    for entry in ontologies.values():
        # Provenance requirement: every pinned ontology entry must record
        # where it came from and which release it pins.
        if not isinstance(entry, dict) or not entry.get("source_url") or not (
            entry.get("version_iri") or entry.get("version_info")
        ):
            return None, "upper_ontology_registry_provenance_invalid"
        for role in merged:
            merged[role].update(entry.get(role, []))
    if not any(merged.values()):
        return None, "upper_ontology_registry_malformed"
    result = {role: frozenset(values) for role, values in merged.items()}
    with _UPPER_REGISTRY_LOCK:
        _UPPER_REGISTRY_CACHE.clear()  # single registry file; drop stale versions
        _UPPER_REGISTRY_CACHE[cache_key] = result
    return result, None


def _is_standard(iri: str) -> bool:
    """True for foundational W3C vocabulary accepted by namespace policy."""

    return iri.startswith(STANDARD_NAMESPACE_PREFIXES)


UCO_PROFILE_NAMESPACE_PREFIXES: tuple[str, ...] = tuple(
    sorted({prefix for prefixes in PROFILE_ID_TO_NAMESPACE_PREFIXES.values() for prefix in prefixes})
)


# Ontology and namespace IRIs themselves (e.g. rdfs:seeAlso <http://www.w3.org/ns/sosa/>).
_UPPER_NAMESPACE_ROOTS: frozenset[str] = frozenset(
    prefix.rstrip("/#_") for prefix in UCO_PROFILE_NAMESPACE_PREFIXES
)


def _is_upper_namespace(iri: str) -> bool:
    return iri.startswith(UCO_PROFILE_NAMESPACE_PREFIXES)


def _selected_upper_prefixes(selected_profiles: list[str] | None) -> frozenset[str]:
    """Return allowed upper-namespace prefixes for the selected profiles.

    CQ-29: ``None`` or empty authorizes **zero** upper profiles (fail closed).
    Recipe validation always passes explicit ``profiles=[...]``.
    """
    if not selected_profiles:
        return frozenset()
    allowed: set[str] = set()
    for pid in selected_profiles:
        allowed.update(PROFILE_ID_TO_NAMESPACE_PREFIXES.get(pid, ()))
    return frozenset(allowed)


def _profile_for_upper_iri(iri: str) -> str | None:
    # Prefer canonical ids (time over owl-time alias) for diagnostics.
    preferred_order = (
        "bfo",
        "gufo",
        "prov-o",
        "time",
        "geosparql",
        "foaf",
        "org",
        "prof",
        "qudt",
        "sosa",
        "ssn",
        "owl-time",
    )
    for pid in preferred_order:
        prefixes = PROFILE_ID_TO_NAMESPACE_PREFIXES.get(pid, ())
        if prefixes and iri.startswith(prefixes):
            return "time" if pid == "owl-time" else pid
    for pid, prefixes in PROFILE_ID_TO_NAMESPACE_PREFIXES.items():
        if iri.startswith(prefixes):
            return pid
    return None


def check_graph_concepts(
    graph_path: str | Path,
    project_root: str | os.PathLike[str] | None = PROJECT_ROOT,
    extensions: list[str] | None = None,
    selected_profiles: list[str] | None = None,
    *,
    bundle: ResolvedValidationBundle | None = None,
) -> ConceptCoverageReport:
    """Check that every class and property in a graph file is declared.

    Classes are the URIRef objects of ``rdf:type`` triples; properties are
    all predicates. Instance IRIs (kb:, urn:uuid:, …) never appear in either
    position, so no instance-namespace whitelist is needed.

    When ``bundle`` is provided (preferred, CQ-27), extension/profile declared
    terms come from that bundle's exact resources and fingerprint; profile
    selection is taken from ``bundle.profiles`` unless ``selected_profiles``
    is also supplied.

    When ``selected_profiles`` / bundle profiles are empty or omitted, upper
    ontology terms fail closed as ``profile_not_selected`` (CQ-29) — they are
    never silently accepted from the global registry.
    """
    project_root = PROJECT_ROOT if project_root is None else Path(project_root).expanduser()

    import rdflib
    from rdflib import RDF, URIRef

    graph = rdflib.Graph()
    path = Path(graph_path)
    fmt = "json-ld" if path.suffix.lower() in {".json", ".jsonld", ".json-ld"} else "turtle"
    graph.parse(str(path), format=fmt)

    used_classes = {
        str(obj)
        for obj in graph.objects(predicate=RDF.type)
        if isinstance(obj, URIRef)
    }
    used_properties = {str(pred) for pred in graph.predicates()}
    # IRIs in object position inside a profiled namespace must be declared
    # too, e.g. QUDT units (qudt:hasUnit unit:KiloM-PER-HR).
    used_values = {
        str(obj)
        for pred, obj in graph.predicate_objects()
        if pred != RDF.type and isinstance(obj, URIRef) and _is_upper_namespace(str(obj))
    } - used_classes - used_properties

    if bundle is not None:
        declared = load_declared_terms(project_root=project_root, bundle=bundle)
        profiles_for_check = (
            list(selected_profiles)
            if selected_profiles is not None
            else list(bundle.profiles)
        )
        bundle_fingerprint = bundle.fingerprint
    else:
        declared = load_declared_terms(project_root=project_root, extensions=extensions)
        profiles_for_check = list(selected_profiles) if selected_profiles is not None else []
        bundle_fingerprint = None

    upper, upper_error = _load_upper_registry()
    allowed_prefixes = _selected_upper_prefixes(profiles_for_check)
    selected_tuple = tuple(profiles_for_check)

    undeclared_classes: list[str] = []
    undeclared_properties: list[str] = []
    unknown_upper: set[str] = set()
    unselected: list[ProfileNotSelected] = []
    role_mismatches: list[tuple[str, str, str]] = []
    verification_errors: list[str] = []

    if declared.parse_errors:
        verification_errors.append("ontology_parse_error")
        for err in declared.parse_errors:
            verification_errors.append(
                f"ontology_parse_error:{err.path}:{err.role}:{err.error}"
            )

    def _handle_upper(iri: str, *, as_class: bool, as_value: bool = False) -> bool:
        """Return True if the IRI was handled as an upper-ontology term."""
        if not _is_upper_namespace(iri):
            return False
        used_as = "value" if as_value else ("class" if as_class else "property")
        # CQ-29: empty/None profiles authorize zero upper namespaces.
        if not allowed_prefixes or not iri.startswith(tuple(allowed_prefixes)):
            pid = _profile_for_upper_iri(iri) or "unknown"
            unselected.append(
                ProfileNotSelected(
                    iri=iri,
                    required_profile=pid,
                    used_as=used_as,
                    selected_profiles=selected_tuple,
                )
            )
            return True
        if upper is None:
            return True
        if as_value:
            if iri.rstrip("/#_") in _UPPER_NAMESPACE_ROOTS or any(
                iri in upper[role] for role in ("classes", "properties", "individuals", "datatypes")
            ):
                return True
            unknown_upper.add(iri)
            return True
        if as_class:
            if iri in upper["classes"] or iri in upper["datatypes"]:
                return True
            if iri in upper["properties"]:
                role_mismatches.append((iri, "upper-ontology property", "class (rdf:type object)"))
            else:
                unknown_upper.add(iri)
        else:
            if iri in upper["properties"]:
                return True
            if iri in upper["classes"]:
                role_mismatches.append((iri, "upper-ontology class", "property (predicate)"))
            else:
                unknown_upper.add(iri)
        return True

    for iri in sorted(used_classes):
        if _is_standard(iri):
            continue
        if _handle_upper(iri, as_class=True):
            continue
        if iri in declared.classes or iri in declared.unknown_role:
            continue
        if iri in declared.properties:
            role_mismatches.append((iri, "property", "class (rdf:type object)"))
        elif iri in declared.shapes:
            role_mismatches.append((iri, "SHACL shape", "class (rdf:type object)"))
        else:
            undeclared_classes.append(iri)

    for iri in sorted(used_properties):
        if _is_standard(iri):
            continue
        if _handle_upper(iri, as_class=False):
            continue
        if iri in declared.properties or iri in declared.unknown_role:
            continue
        if iri in declared.classes:
            role_mismatches.append((iri, "class", "property (predicate)"))
        elif iri in declared.shapes:
            role_mismatches.append((iri, "SHACL shape", "property (predicate)"))
        else:
            undeclared_properties.append(iri)

    for iri in sorted(used_values):
        _handle_upper(iri, as_class=False, as_value=True)

    # Registry is required only when at least one *selected* upper term was
    # accepted into the registry-check path (not profile_not_selected).
    upper_terms_needing_registry = bool(unknown_upper) or any(
        m[1].startswith("upper-ontology") for m in role_mismatches
    )
    # Also: selected upper terms that passed (ok path) — detect via used ∩ selected.
    selected_upper_used = False
    if allowed_prefixes:
        for iri in used_classes | used_properties | used_values:
            if _is_upper_namespace(iri) and iri.startswith(tuple(allowed_prefixes)):
                selected_upper_used = True
                break
    if selected_upper_used and upper_error is not None:
        verification_errors.append(upper_error)
    elif upper_terms_needing_registry and upper_error is not None:
        verification_errors.append(upper_error)

    ok = (
        not undeclared_classes
        and not undeclared_properties
        and not unknown_upper
        and not unselected
        and not role_mismatches
        and not verification_errors
        and not declared.parse_errors
    )
    guidance_parts: list[str] = []
    if undeclared_classes or undeclared_properties:
        guidance_parts.append(GUIDANCE)
        ext_tokens = list(extensions or [])
        if not ext_tokens and bundle is not None:
            ext_tokens = list(bundle.extensions)
        if any(token == "cac" or token.startswith("cac:") for token in ext_tokens):
            if not any(token == "cac:full" for token in ext_tokens):
                guidance_parts.append(SUBSET_GAP_GUIDANCE)
    if unknown_upper:
        guidance_parts.append(UPPER_TERM_GUIDANCE)
    if unselected:
        guidance_parts.append(PROFILE_NOT_SELECTED_GUIDANCE)
    if role_mismatches:
        guidance_parts.append(ROLE_MISMATCH_GUIDANCE)
    if declared.parse_errors:
        guidance_parts.append(PARSE_ERROR_GUIDANCE)
    if any(e.startswith("upper_ontology_registry") for e in verification_errors):
        guidance_parts.append(
            "A required verification stage could not run "
            f"({', '.join(e for e in verification_errors if e.startswith('upper_ontology_registry'))}): "
            "the pinned upper-ontology term registry "
            "(case_uco/validation/upper_ontology_registry.json) is missing, malformed, "
            "or lacks release provenance while the graph uses selected "
            "profiled upper-ontology terms. Restore or regenerate the "
            "registry (mcp_server/tools/build_upper_ontology_registry.py); "
            "an unverifiable graph is never reported as conformant."
        )

    return ConceptCoverageReport(
        ok=ok,
        undeclared_classes=tuple(undeclared_classes),
        undeclared_properties=tuple(undeclared_properties),
        unknown_upper_ontology_terms=tuple(sorted(unknown_upper)),
        role_mismatches=tuple(role_mismatches),
        profile_not_selected=tuple(unselected),
        checked_class_count=len(used_classes),
        checked_property_count=len(used_properties),
        guidance=" ".join(guidance_parts),
        verification_status="could_not_verify" if verification_errors else "complete",
        verification_errors=tuple(verification_errors),
        bundle_fingerprint=bundle_fingerprint,
        ontology_parse_errors=declared.parse_errors,
    )


def coverage_report_to_dict(report: ConceptCoverageReport) -> dict[str, Any]:
    """Serialize a coverage report into the MCP tool result shape."""

    payload: dict[str, Any] = {
        "ok": report.ok,
        "checked_class_count": report.checked_class_count,
        "checked_property_count": report.checked_property_count,
        "verification_status": report.verification_status,
    }
    if report.bundle_fingerprint:
        payload["bundle_fingerprint"] = report.bundle_fingerprint
    if not report.ok:
        payload["undeclared_classes"] = list(report.undeclared_classes)
        payload["undeclared_properties"] = list(report.undeclared_properties)
        if report.unknown_upper_ontology_terms:
            payload["unknown_upper_ontology_terms"] = list(
                report.unknown_upper_ontology_terms
            )
        if report.profile_not_selected:
            payload["profile_not_selected"] = [
                {
                    "iri": item.iri,
                    "required_profile": item.required_profile,
                    "used_as": item.used_as,
                    "selected_profiles": list(item.selected_profiles),
                }
                for item in report.profile_not_selected
            ]
        if report.role_mismatches:
            payload["role_mismatches"] = [
                {"iri": iri, "declared_role": declared_role, "used_as": used_as}
                for iri, declared_role, used_as in report.role_mismatches
            ]
        if report.verification_errors:
            payload["verification_errors"] = list(report.verification_errors)
        if report.ontology_parse_errors:
            payload["ontology_parse_errors"] = [
                {
                    "path": e.path,
                    "role": e.role,
                    "error": e.error,
                    "profile_id": e.profile_id,
                    "extension": e.extension,
                }
                for e in report.ontology_parse_errors
            ]
        payload["guidance"] = report.guidance
    return payload

__all__ = [
    "CORE_ONTOLOGY_GLOBS",
    "GUIDANCE",
    "PARSE_ERROR_GUIDANCE",
    "PROFILE_ID_TO_NAMESPACE_PREFIXES",
    "PROFILE_NOT_SELECTED_GUIDANCE",
    "ROLE_MISMATCH_GUIDANCE",
    "STANDARD_NAMESPACE_PREFIXES",
    "UCO_PROFILE_NAMESPACE_PREFIXES",
    "UPPER_ONTOLOGY_REGISTRY_PATH",
    "UPPER_TERM_GUIDANCE",
    "ConceptCoverageReport",
    "DeclaredTerms",
    "OntologyParseError",
    "ProfileNotSelected",
    "_DECLARED_CACHE",
    "_core_ontology_paths",
    "_is_standard",
    "_load_upper_registry",
    "_profile_for_upper_iri",
    "check_graph_concepts",
    "clear_declared_term_cache",
    "coverage_report_to_dict",
    "load_declared_terms",
]
