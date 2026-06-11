"""CASE/UCO SDK MCP Server — ontology discovery tools for AI coding agents.

Exposes the SDK's registry API as MCP tools so AI agents in Cursor,
Claude Code, and similar tools can query the ontology programmatically
instead of parsing markdown documentation.

Run: python mcp_server/server.py
Or:  fastmcp dev mcp_server/server.py

Set CASE_UCO_EXTENSIONS=cac,aeo to load extension registries.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from fastmcp import FastMCP

_logger = logging.getLogger(__name__)

from case_uco.registry import (
    search,
    get_class,
    find_facets,
    list_modules,
    list_vocabs,
    suggest_for_concept,
    modeling_warnings,
)
from domain_index import (
    TASK_TO_CLASSES,
    DOMAIN_CATEGORIES,
    CORE_PATTERNS,
    RECIPE_INDEX,
    CHANGE_PROPOSAL_SECTIONS,
    UCO_PROFILES,
    MAPPING_GUIDE_INDEX,
    suggest_target_repo,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Extension registry loading
# ---------------------------------------------------------------------------

_EXTENSION_REGISTRIES: dict[str, dict[str, Any]] = {}


def _load_extension_registries() -> None:
    """Load extension _registry.json files based on CASE_UCO_EXTENSIONS env var."""
    env_val = os.environ.get("CASE_UCO_EXTENSIONS", "").strip()
    if not env_val:
        return

    ext_names = [n.strip() for n in env_val.split(",") if n.strip()]
    for ext_name in ext_names:
        reg = _find_extension_registry(ext_name)
        if reg is not None:
            _EXTENSION_REGISTRIES[ext_name] = reg

    if _EXTENSION_REGISTRIES:
        loaded = ", ".join(_EXTENSION_REGISTRIES.keys())
        print(f"[MCP] Loaded extension registries: {loaded}", file=sys.stderr)


def _find_extension_registry(ext_name: str) -> dict[str, Any] | None:
    """Locate and load a _registry.json for the given extension name."""
    search_paths = [
        PROJECT_ROOT / "extensions" / ext_name / "_registry.json",
        PROJECT_ROOT / "packages" / f"case-uco-{ext_name}" / "_registry.json",
        PROJECT_ROOT / "packages" / f"case-uco-{ext_name}" / "python" / f"case_uco_{ext_name}" / "_registry.json",
    ]

    try:
        import importlib.metadata
        for ep in importlib.metadata.entry_points(group="case_uco.extensions"):
            if ep.name == ext_name:
                reg_path_str = ep.load()
                if isinstance(reg_path_str, str):
                    search_paths.insert(0, Path(reg_path_str))
    except (ImportError, AttributeError, TypeError) as exc:
        _logger.debug("Skipping extension entry point discovery: %s", exc)

    for path in search_paths:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
    return None


def _search_extensions(query: str, scope: str = "all") -> list[dict]:
    """Search extension registries by keyword, filtered by scope."""
    q = query.lower()
    results = []
    for ext_name, reg in _EXTENSION_REGISTRIES.items():
        if scope not in ("all", ext_name):
            continue
        for name, info in reg.get("classes", {}).items():
            if q in name.lower() or q in info.get("description", "").lower():
                entry = {"name": name, **info}
                entry.setdefault("source", ext_name)
                results.append(entry)
    results.sort(key=lambda c: (c.get("module", ""), c["name"]))
    return results


def _get_class_from_extensions(name: str, scope: str = "all") -> dict | None:
    """Look up a class by name in extension registries."""
    name_lower = name.lower()
    for ext_name, reg in _EXTENSION_REGISTRIES.items():
        if scope not in ("all", ext_name):
            continue
        for cls_name, info in reg.get("classes", {}).items():
            if cls_name.lower() == name_lower:
                entry = {"name": cls_name, **info}
                entry.setdefault("source", ext_name)
                return entry
    return None


_load_extension_registries()

mcp = FastMCP(
    "CASE/UCO SDK",
    instructions=(
        "Tools for discovering CASE/UCO ontology classes, properties, and "
        "forensic workflow patterns. Use search_classes to find classes by "
        "keyword, get_class_details for full property info, and "
        "find_classes_for_domain to map investigative tasks to the right types. "
        "When a concept is missing from the ontology, use check_existing_proposals "
        "to search for prior proposals in UCO/CASE issue trackers, then "
        "draft_change_proposal to generate a filled-in change proposal. "
        "Use get_uco_profiles to find UCO Profile ontologies that align UCO "
        "with external ontologies like BFO, PROV-O, GeoSPARQL, OWL-Time, "
        "gUFO, and FOAF for cross-ontology interoperability. "
        "Use guide_mapping to get step-by-step mapping guidance for a "
        "specific evidence source (e.g., filesystem report, mobile "
        "extraction, email export, pcap). Use get_recipe to retrieve "
        "full recipe content including code examples and JSON-LD output. "
        "Extension ontologies (CAC, AEO) are loaded when CASE_UCO_EXTENSIONS "
        "is set. Use the scope parameter on search_classes, get_class_details, "
        "find_classes_for_domain, and list_all_facets to filter by 'core', "
        "a specific extension name, or 'all' (default)."
    ),
)


@mcp.tool
def search_classes(query: str, scope: str = "all") -> list[dict]:
    """Search for CASE/UCO classes by keyword.

    Case-insensitive substring match on class name and description.
    Returns matching classes with name, module, description, and property count.

    Args:
        query: Search keyword.
        scope: "all" (default) searches core + loaded extensions.
               "core" searches CASE/UCO only.
               An extension name (e.g. "cac", "aeo") searches that extension only.

    Examples: search_classes("file"), search_classes("network"),
              search_classes("engagement", scope="aeo")
    """
    results = []
    if scope in ("all", "core"):
        for r in search(query):
            entry = {
                "name": r["name"],
                "module": r["module"],
                "description": r.get("description", "")[:200],
                "property_count": len(r.get("properties", [])),
                "is_facet": r.get("is_facet", False),
                "source": "core",
            }
            results.append(entry)

    if scope != "core":
        for r in _search_extensions(query, scope):
            results.append({
                "name": r["name"],
                "module": r.get("module", ""),
                "description": r.get("description", "")[:200],
                "property_count": len(r.get("properties", [])),
                "is_facet": r.get("is_facet", False),
                "source": r.get("source", "extension"),
            })

    return results


@mcp.tool
def get_class_details(name: str, scope: str = "all") -> dict | None:
    """Get full details for a CASE/UCO class including all properties.

    Returns the class IRI, module, description, parent classes, and a
    complete property table with types, cardinalities, and required flags.

    Args:
        name: Class name (case-insensitive).
        scope: "all" (default), "core", or an extension name (e.g. "cac").

    Examples: get_class_details("FileFacet"), get_class_details("Investigation")
    """
    cls = None
    if scope in ("all", "core"):
        cls = get_class(name)
        if cls:
            cls["source"] = "core"

    if cls is None and scope != "core":
        cls = _get_class_from_extensions(name, scope)

    if cls is None:
        return None
    return {
        "name": cls["name"],
        "iri": cls.get("iri", ""),
        "module": cls.get("module", ""),
        "description": cls.get("description", ""),
        "parents": cls.get("parents", []),
        "is_facet": cls.get("is_facet", False),
        "source": cls.get("source", "core"),
        "properties": [
            {
                "name": p["name"],
                "type": p.get("type", ""),
                "cardinality": p.get("cardinality", ""),
                "required": p.get("required", False),
                "description": p.get("description", "")[:150],
            }
            for p in cls.get("properties", [])
        ],
    }


@mcp.tool
def find_classes_for_domain(domain: str, scope: str = "all") -> dict:
    """Map a forensic domain or investigative task to relevant CASE/UCO classes.

    Accepts natural-language descriptions of what the developer is modeling.
    Returns matching task templates and domain categories with relevant classes.

    Examples: find_classes_for_domain("mobile forensics"),
              find_classes_for_domain("disk image extraction"),
              find_classes_for_domain("email evidence")
    """
    q = domain.lower()

    matching_tasks = []
    for task_desc, classes in TASK_TO_CLASSES.items():
        if any(word in task_desc for word in q.split()):
            matching_tasks.append({
                "task": task_desc,
                "classes": [
                    {"name": name, "role": role} for name, role in classes
                ],
            })

    matching_categories = []
    matched_category_names = set()
    for cat in DOMAIN_CATEGORIES:
        title_match = q in cat["title"].lower()
        keyword_match = any(kw in q for kw in cat["keywords"])
        if title_match or keyword_match:
            matching_categories.append({
                "domain": cat["title"],
                "description": cat["description"],
            })
            matched_category_names.add(cat["name"])

    matching_profiles = []
    for profile in UCO_PROFILES:
        kw_match = any(kw in q for kw in profile["keywords"])
        domain_match = any(
            d in matched_category_names for d in profile.get("related_domains", [])
        )
        if kw_match or domain_match:
            matching_profiles.append({
                "name": profile["name"],
                "full_name": profile["full_name"],
                "description": profile["description"],
                "repo_url": profile["repo_url"],
                "profile_type": profile["profile_type"],
            })

    matching_recipes = []
    for recipe in RECIPE_INDEX:
        text = f"{recipe['title']} {recipe['description']} {recipe['keywords']}".lower()
        if any(word in text for word in q.split()):
            matching_recipes.append({
                "title": recipe["title"],
                "file": recipe["file"],
                "is_starter_kit": recipe.get("is_starter_kit", False),
            })

    result: dict = {
        "query": domain,
        "task_templates": matching_tasks,
        "related_domains": matching_categories,
        "related_recipes": matching_recipes,
        "tip": (
            "Use get_class_details(name) on any class above to see its full "
            "property table. The most common pattern is ObservableObject + "
            "Facets — create an ObservableObject and attach Facets to describe it."
        ),
    }

    has_starter = any(r["is_starter_kit"] for r in matching_recipes)
    if has_starter:
        result["starter_kit_tip"] = (
            "A starter kit is available for this domain. Use get_recipe() with "
            "the starter kit title for a complete end-to-end mapping example."
        )

    if matching_profiles:
        result["related_profiles"] = matching_profiles
        result["profile_tip"] = (
            "UCO Profile ontologies align UCO classes with external ontologies. "
            "Use get_uco_profiles() for full details on any profile listed above."
        )

    # Proactively suggest CAC extension for child exploitation domains
    cac_keywords = {
        "child", "csam", "grooming", "ncmec", "cybertip", "exploitation",
        "victim", "offender", "enticement", "sextortion", "predator",
        "minor", "abuse", "production", "hotline", "cac", "icac",
        "crimes against children",
        "trafficking", "trafficker", "trafficked", "ring", "cell",
        "rotation", "interstate transport",
        "recruitment", "recruiter", "school-based", "peer recruitment",
        "street recruitment", "pretext",
        "rescue", "extraction", "emergency response", "victim service",
        "safety planning", "trauma", "ongoing danger", "recantation",
        "multi-agency", "dcfs", "child protective",
        "jurisdiction", "multi-jurisdiction", "task force", "taskforce",
        "joint investigation", "joint operation", "mutual aid", "handoff",
        "tactical", "arrest", "high-risk", "dynamic entry",
        "warrant service", "undercover", "asset forfeiture", "seizure",
        "csam forensic", "csam provenance", "chain of custody",
        "evidence verification", "metadata correlation", "temporal pattern",
        "geospatial correlation", "cross-platform correlation",
        "behavioral fingerprint", "victim identification",
        "photodna", "perceptual hash",
    }
    if any(kw in q for kw in cac_keywords):
        cac_loaded = "cac" in _EXTENSION_REGISTRIES
        result["extension_suggestion"] = {
            "extension": "cac",
            "name": "Crimes Against Children (CAC) Ontology",
            "description": (
                "The CAC Ontology provides purpose-built classes for child exploitation "
                "investigations: grooming phases (InitialContactPhase, TrustBuildingPhase, "
                "IsolationPhase, SexualizationPhase, ExploitationPhase), GroomingMessage "
                "with explicitness/tone, ChildVictim/OnlinePredator roles, "
                "NCMECCybertipReport with incident types, CSAM detection tools "
                "(PhotoDNA, ML classifiers), trafficking ring/cell hierarchies and "
                "victim rotation, school/peer/street recruitment with pretext "
                "approaches, multi-jurisdictional task force operations, tactical "
                "arrest workflows, victim rescue and post-rescue services, and "
                "CSAM forensic provenance with cross-platform/behavioral correlation."
            ),
            "loaded": cac_loaded,
            "activation": (
                'Already loaded — use scope="cac" to search CAC classes directly.'
                if cac_loaded else
                'Set CASE_UCO_EXTENSIONS=cac in your MCP server config to load CAC classes. '
                'See extensions/cac/README.md for setup instructions.'
            ),
            "repo_url": "https://github.com/Project-VIC-International/CAC-Ontology",
            "relevant_modules": [
                "cacontology-grooming (grooming behaviors, phases, patterns)",
                "cacontology-detection (CSAM detection, classification scales)",
                "cacontology-us-ncmec (CyberTip reports, incident types)",
                "cacontology-platforms (ESPs, content moderation, platform cooperation)",
                "cacontology-forensics (acquisition, chain-of-custody, metadata/temporal/geospatial/cross-platform correlation, behavioral fingerprinting, victim ID)",
                "cacontology-hotlines (hotline reports, evidence items)",
                "cacontology-sex-trafficking (rings, cells, victim rotation, interstate transport)",
                "cacontology-recruitment-networks (school-based and peer recruitment hierarchies, mandatory-reporter activation)",
                "cacontology-street-recruitment (pretext approaches: help/food/transportation/phone-charging offers, rapid escalation, digital-to-physical bridge)",
                "cacontology-multi-jurisdiction (Local/State/Federal/International jurisdictions, joint investigations, mass child rescue operations, jurisdictional handoffs, mutual aid)",
                "cacontology-tactical (arrest operations, dynamic entry, suspect profiles, threat assessments)",
                "cacontology-undercover (undercover operations and personas)",
                "cacontology-taskforce (task force structure and participation)",
                "cacontology-asset-forfeiture (seizure and forfeiture actions)",
                "cacontology-victim-impact (emergency response, extraction, ongoing-danger assessment, safety planning, multi-agency victim response, trauma/help-seeking indicators)",
                "cacontology-recantation (victim recantation events and analysis)",
                "cacontology-legal-outcomes / cacontology-legal-harmonization / cacontology-multi-jurisdiction (legal outcomes and federal/state harmonization)",
            ],
        }

    return result


@mcp.tool
def get_uco_profiles(query: str = "") -> dict:
    """Find UCO Profile ontologies that align UCO with other established ontologies.

    UCO maintains profile repositories that map UCO concepts to external
    ontologies (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF). These
    profiles enable interoperability and help developers familiar with
    those ontologies use CASE/UCO effectively.

    Pass a keyword to filter (e.g., "provenance", "geospatial", "time"),
    or leave empty to list all profiles.

    Examples: get_uco_profiles("provenance"), get_uco_profiles("geospatial"),
              get_uco_profiles("foundational"), get_uco_profiles("")
    """
    q = query.lower().strip()

    if q:
        matches = []
        for profile in UCO_PROFILES:
            text = (
                f"{profile['name']} {profile['full_name']} "
                f"{profile['description']} {' '.join(profile['keywords'])}"
            ).lower()
            if any(word in text for word in q.split()):
                matches.append(profile)
    else:
        matches = list(UCO_PROFILES)

    loaded_extensions = list(_EXTENSION_REGISTRIES.keys())

    results = []
    for p in matches:
        entry: dict[str, Any] = {
            "name": p["name"],
            "full_name": p["full_name"],
            "profile_type": p["profile_type"],
            "status": p["status"],
            "description": p["description"],
            "repo_url": p["repo_url"],
            "ontology_url": p["ontology_url"],
            "ontology_file": p["ontology_file"],
            "related_recipes": p.get("related_recipes", []),
        }
        ext_compat = p.get("extension_compatibility", {})
        if loaded_extensions and ext_compat:
            compat_notes = {}
            for ext in loaded_extensions:
                status = ext_compat.get(ext, "unknown")
                if status == "included":
                    compat_notes[ext] = f"Included — {ext.upper()} already imports this alignment"
                elif status == "not_recommended":
                    compat_notes[ext] = f"Not recommended — may conflict with {ext.upper()} axioms"
                elif status == "compatible":
                    compat_notes[ext] = "Compatible"
                else:
                    compat_notes[ext] = "Unknown compatibility"
            entry["extension_compatibility"] = compat_notes
        results.append(entry)

    return {
        "query": query or "(all profiles)",
        "total": len(results),
        "profiles": results,
        "loaded_extensions": loaded_extensions,
        "rationale_url": "https://cyberdomainontology.org/ontology/development/#profiles",
        "tip": (
            "Profiles are OWL ontology files (.ttl) that add subclass axioms "
            "to align UCO classes with the external ontology. Include the "
            "profile alongside your CASE/UCO graph for cross-ontology reasoning. "
            "See docs/ECOSYSTEM.md for integration patterns."
        ),
    }


@mcp.tool
def list_all_facets(scope: str = "all") -> list[dict]:
    """List all Facet classes in the CASE/UCO ontology (and loaded extensions).

    Facets are attached to ObservableObjects to describe specific aspects.
    Use this when you know you need the ObservableObject + Facet pattern
    but need to find the right Facet for your data.

    Args:
        scope: "all" (default), "core", or an extension name.
    """
    results = []
    if scope in ("all", "core"):
        for r in find_facets():
            results.append({
                "name": r["name"],
                "module": r["module"],
                "description": r.get("description", "")[:200],
                "property_count": len(r.get("properties", [])),
                "source": "core",
            })

    if scope != "core":
        for ext_name, reg in _EXTENSION_REGISTRIES.items():
            if scope not in ("all", ext_name):
                continue
            for name, info in reg.get("classes", {}).items():
                if info.get("is_facet"):
                    results.append({
                        "name": name,
                        "module": info.get("module", ""),
                        "description": info.get("description", "")[:200],
                        "property_count": len(info.get("properties", [])),
                        "source": ext_name,
                    })
    return results


@mcp.tool
def suggest_classes_for_input(concept: str) -> dict:
    """Suggest CASE/UCO classes for a natural-language concept with modeling warnings.

    Given a forensic concept like "file", "email", or "network connection",
    returns recommended classes, the standard modeling pattern, usage notes,
    and any warnings about common modeling mistakes.

    Examples: suggest_classes_for_input("file"),
              suggest_classes_for_input("mobile device"),
              suggest_classes_for_input("malware sample")
    """
    suggestions = suggest_for_concept(concept)
    warnings_by_class: dict[str, list[str]] = {}
    for s in suggestions:
        w = modeling_warnings(s["name"])
        if w:
            warnings_by_class[s["name"]] = w

    result = {
        "query": concept,
        "suggestions": [
            {
                "name": s["name"],
                "module": s["module"],
                "pattern": s["pattern"],
                "usage_note": s["usage_note"],
            }
            for s in suggestions
        ],
        "warnings": warnings_by_class if warnings_by_class else None,
        "tip": (
            "Use get_class_details(name) on any suggested class to see its "
            "full property table."
        ) if suggestions else (
            "No concept match found. Try search_classes() with related "
            "keywords, or find_classes_for_domain() for broader discovery."
        ),
    }

    cac_concepts = {
        "grooming", "csam", "child", "exploitation", "cybertip", "ncmec",
        "sextortion", "enticement", "predator", "victim", "minor",
        "abuse", "production", "icac",
        "trafficking", "trafficker", "trafficked", "ring", "cell",
        "rotation", "interstate transport",
        "recruitment", "recruiter", "school-based", "peer recruitment",
        "street recruitment", "pretext",
        "rescue", "extraction", "emergency response", "victim service",
        "safety planning", "trauma", "ongoing danger", "recantation",
        "multi-agency", "dcfs", "child protective",
        "jurisdiction", "multi-jurisdiction", "task force", "taskforce",
        "joint investigation", "joint operation", "mutual aid", "handoff",
        "tactical", "arrest", "high-risk", "dynamic entry",
        "warrant service", "undercover", "asset forfeiture", "seizure",
        "csam forensic", "csam provenance", "chain of custody",
        "evidence verification", "metadata correlation", "temporal pattern",
        "geospatial correlation", "cross-platform correlation",
        "behavioral fingerprint", "victim identification",
        "photodna", "perceptual hash",
    }
    concept_lower = concept.lower()
    if any(kw in concept_lower for kw in cac_concepts):
        result["cac_extension_note"] = (
            "The CAC (Crimes Against Children) Ontology extension provides "
            "specialized classes for this concept. Use search_classes(query, scope='cac') "
            "to find CAC-specific classes, or set CASE_UCO_EXTENSIONS=cac to load them."
        )

    return result


@mcp.tool
def get_recipe(scenario: str) -> dict | None:
    """Find a code recipe for a common forensic workflow.

    Searches the recipe index by keyword and returns the matching recipe's
    title, description, and file location for the code examples.

    Examples: get_recipe("disk forensics"), get_recipe("chain of custody"),
              get_recipe("mobile"), get_recipe("email")
    """
    q = scenario.lower()
    best_match = None
    best_score = 0

    for recipe in RECIPE_INDEX:
        score = 0
        text = f"{recipe['title']} {recipe['description']} {recipe['keywords']}".lower()
        for word in q.split():
            if word in text:
                score += 1
        if score > best_score:
            best_score = score
            best_match = recipe

    if best_match is None or best_score == 0:
        return None

    content = None
    try:
        content = (PROJECT_ROOT / best_match["file"]).read_text(encoding="utf-8")
    except OSError:
        pass  # recipe file missing on disk — return metadata without content

    return {
        "title": best_match["title"],
        "description": best_match["description"],
        "file": best_match["file"],
        "content": content[:8000] if content else None,
        "truncated": len(content) > 8000 if content else False,
        "tip": "This recipe contains complete code examples and JSON-LD output.",
    }


@mcp.tool
def guide_mapping(evidence_source: str) -> dict:
    """Get step-by-step mapping guidance for a specific evidence source type.

    Provides the recommended CASE/UCO pattern, classes to use, common
    anti-patterns to avoid, a Python code skeleton, and a link to a
    starter kit when available.

    Examples: guide_mapping("filesystem report"), guide_mapping("email"),
              guide_mapping("mobile extraction"), guide_mapping("pcap")
    """
    q = evidence_source.lower()

    best_match = None
    best_score = 0
    for entry in MAPPING_GUIDE_INDEX:
        score = sum(1 for kw in entry["keywords"] if kw in q)
        if entry["source"].lower() in q or q in entry["source"].lower():
            score += 3
        if score > best_score:
            best_score = score
            best_match = entry

    if best_match is None or best_score == 0:
        return {
            "query": evidence_source,
            "found": False,
            "tip": (
                "No mapping guide found for this evidence source. "
                "Try find_classes_for_domain() for broader discovery, "
                "or search_classes() with related keywords."
            ),
        }

    starter_content = None
    if best_match["starter_kit"]:
        try:
            starter_content = (PROJECT_ROOT / best_match["starter_kit"]).read_text(
                encoding="utf-8"
            )[:4000]
        except OSError:
            pass  # starter kit file missing on disk — proceed without preview

    return {
        "query": evidence_source,
        "found": True,
        "source_type": best_match["source"],
        "recommended_pattern": best_match["pattern"],
        "classes": best_match["classes"],
        "anti_patterns": best_match["anti_patterns"],
        "code_skeleton": best_match["code_skeleton"],
        "starter_kit": best_match["starter_kit"],
        "starter_kit_preview": starter_content,
        "steps": [
            f"1. Create a CASEGraph and import the needed classes: {', '.join(best_match['classes'][:4])}",
            f"2. Follow the '{best_match['pattern']}' pattern",
            "3. Attach multiple facets to a single ObservableObject when describing different aspects of the same item",
            "4. Use get_class_details(name) to check required properties before creating objects",
            "5. Write the graph with graph.write('output.jsonld') and validate with case_validate",
        ],
        "tip": (
            "Use get_class_details(name) on any class to see its full property table. "
            "Avoid the listed anti-patterns — they are the most common mistakes."
        ),
    }


@mcp.tool
def list_all_vocabs() -> list[dict]:
    """List all vocabulary/enum types in the CASE/UCO ontology.

    Vocabulary types define constrained sets of allowed values for
    certain properties (e.g., ActionStatusTypeVocab, HashMethodVocab).
    """
    results = list_vocabs()
    return [
        {
            "name": r["name"],
            "members": r.get("members", []),
        }
        for r in results
    ]


@mcp.tool
def check_existing_proposals(
    concept: str,
    repos: list[str] | None = None,
) -> dict:
    """Search open CASE and UCO GitHub issues for existing change proposals.

    Checks whether someone has already proposed a concept similar to yours.
    Searches issue titles in both repositories by default.

    Falls back gracefully when GitHub is unreachable — returns a message
    asking the developer to search manually.

    Examples: check_existing_proposals("drone telemetry"),
              check_existing_proposals("smart device", repos=["UCO"])
    """
    if repos is None:
        repos = ["UCO", "CASE"]

    repo_map = {
        "UCO": "ucoProject/UCO",
        "CASE": "casework/CASE",
    }

    results: list[dict] = []
    errors: list[str] = []

    for repo_key in repos:
        full_repo = repo_map.get(repo_key.upper(), repo_key)
        query = urllib.request.quote(f"{concept} repo:{full_repo} state:open")
        url = f"https://api.github.com/search/issues?q={query}&per_page=10"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "CASE-UCO-SDK-MCP/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                for item in data.get("items", []):
                    body_text = (item.get("body") or "")[:300]
                    results.append({
                        "title": item["title"],
                        "number": item["number"],
                        "url": item["html_url"],
                        "repo": repo_key.upper(),
                        "labels": [lb["name"] for lb in item.get("labels", [])],
                        "created_at": item.get("created_at", ""),
                        "body_preview": body_text,
                    })
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            errors.append(f"{repo_key}: {exc}")

    if errors and not results:
        return {
            "available": False,
            "message": (
                "GitHub issue trackers are not reachable. Please search manually "
                "before submitting your proposal:\n"
                "  UCO: https://github.com/ucoProject/UCO/issues\n"
                "  CASE: https://github.com/casework/CASE/issues"
            ),
            "errors": errors,
        }

    return {
        "available": True,
        "query": concept,
        "repos_searched": repos,
        "total_results": len(results),
        "results": results,
        "errors": errors if errors else None,
        "tip": (
            "If a matching issue exists, consider commenting on it rather than "
            "creating a duplicate. If partially related, reference it in your proposal."
        ) if results else (
            "No existing proposals found. You can proceed with drafting a new one "
            "using draft_change_proposal()."
        ),
    }


def _slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


def _build_example_graph(proposed_classes: list[dict] | None) -> dict | None:
    """Build an example JSON-LD graph dict from proposed classes."""
    if not proposed_classes:
        return None

    cls = proposed_classes[0]
    cls_name = cls.get("name", "ProposedClass")
    example_obj: dict = {
        "@type": f"proposed:{cls_name}",
    }
    for p in cls.get("properties", []):
        p_name = p.get("name", "")
        p_type = p.get("type", "xsd:string")
        if "decimal" in p_type or "float" in p_type or "double" in p_type:
            example_obj[f"proposed:{p_name}"] = 0.0
        elif "integer" in p_type or "int" in p_type:
            example_obj[f"proposed:{p_name}"] = 0
        elif "boolean" in p_type:
            example_obj[f"proposed:{p_name}"] = False
        else:
            example_obj[f"proposed:{p_name}"] = f"example-{p_name}"

    return {
        "@context": {
            "kb": "http://example.org/kb/",
            "proposed": "http://example.org/ontology/proposed/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [
            {
                "@id": "kb:observable-1",
                "@type": "uco-observable:ObservableObject",
                "uco-core:hasFacet": [example_obj],
            }
        ],
    }


def _build_sparql_queries(proposed_classes: list[dict] | None) -> str | None:
    """Build SPARQL query text from proposed classes for testing."""
    if not proposed_classes:
        return None

    cls = proposed_classes[0]
    cls_name = cls.get("name", "ProposedClass")
    props = cls.get("properties", [])
    prop_names = [p.get("name", "") for p in props[:3]]

    if not prop_names:
        return None

    sparql_vars = " ".join(f"?{p}" for p in prop_names)
    sparql_bindings = "\n".join(
        f"           proposed:{p} ?{p} ;"
        for p in prop_names
    )
    if sparql_bindings.endswith(" ;"):
        sparql_bindings = sparql_bindings[:-2] + " ."

    query = (
        f"# CQ 1.1: What values are recorded for {cls_name} instances?\n"
        f"PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>\n"
        f"PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>\n"
        f"PREFIX proposed: <http://example.org/ontology/proposed/>\n\n"
        f"SELECT ?obj {sparql_vars}\n"
        f"WHERE {{\n"
        f"    ?obj a uco-observable:ObservableObject ;\n"
        f"         uco-core:hasFacet ?facet .\n"
        f"    ?facet a proposed:{cls_name} ;\n"
        f"{sparql_bindings}\n"
        f"}}\n"
    )

    return query


def _build_proposal_markdown(
    concept: str,
    description: str,
    scenario: str,
    proposed_classes: list[dict] | None,
    proposed_properties: list[dict] | None,
    target_repo: str,
    target_release: str,
    existing_issue_refs: list[str] | None,
    slug: str,
) -> str:
    """Render a filled-in change proposal from the official template."""

    # --- Target release ---
    target_release_section = (
        f"# Target release\n\n"
        f"**Target**: CASE/UCO {target_release}\n"
    )

    # --- Background ---
    refs_text = ""
    if existing_issue_refs:
        refs_text = "\n\n**Related issues**: " + ", ".join(existing_issue_refs)
    background = f"{description}{refs_text}"

    # --- Requirements ---
    req_lines = []
    req_num = 1
    if proposed_classes:
        for cls in proposed_classes:
            cls_name = cls.get("name", "NewClass")
            cls_type = cls.get("type", "Class")
            parent = cls.get("parent", "")
            parent_text = f" as a subclass of `{parent}`" if parent else ""
            req_lines.append(
                f"## Requirement {req_num}\n\n"
                f"Define a new `{cls_name}` {cls_type}{parent_text}."
            )
            props = cls.get("properties", [])
            if props:
                req_lines.append("\nProperties:\n")
                for p in props:
                    p_name = p.get("name", "")
                    p_type = p.get("type", "xsd:string")
                    p_desc = p.get("description", "")
                    req_lines.append(f"- `{p_name}` ({p_type}): {p_desc}")
            req_num += 1

    if proposed_properties:
        for prop in proposed_properties:
            p_name = prop.get("name", "")
            p_target = prop.get("target_class", "")
            p_type = prop.get("type", "xsd:string")
            p_desc = prop.get("description", "")
            req_lines.append(
                f"## Requirement {req_num}\n\n"
                f"Add property `{p_name}` ({p_type}) to `{p_target}`. {p_desc}"
            )
            req_num += 1

    if not req_lines:
        req_lines.append("## Requirement 1\n\n*(Describe the required change.)*")

    requirements = "\n\n".join(req_lines)

    # --- Risk / Benefit ---
    benefits_lines = [
        f"- Enables modeling of {concept} data in CASE/UCO-compliant graphs",
        "- Improves interoperability between tools that encounter this data type",
    ]
    if proposed_classes:
        for cls in proposed_classes:
            benefits_lines.append(
                f"- The `{cls.get('name', '')}` class provides a structured "
                f"representation where none currently exists"
            )
    benefits = "\n".join(benefits_lines)
    risks = "The submitter is unaware of risks associated with this change."

    # --- Competencies ---
    comp_lines = [f"## Competency 1\n\n{scenario}"]

    if proposed_classes:
        cls_name = proposed_classes[0].get("name", "ProposedClass")
        props = proposed_classes[0].get("properties", [])
        prop_names = [p.get("name", "") for p in props[:3]]

        comp_lines.append(
            f"\n### Competency Question 1.1\n\n"
            f"What {', '.join(prop_names)} values are recorded for "
            f"objects with a `{cls_name}`?"
        )
        result_parts = [f"`{p}`" for p in prop_names]
        comp_lines.append(
            f"\n#### Result 1.1\n\n"
            f"A SPARQL query selecting {', '.join(result_parts)} from instances "
            f"of `{cls_name}` returns the recorded values."
        )

        if len(props) >= 2:
            filter_prop = props[0]
            comp_lines.append(
                f"\n### Competency Question 1.2\n\n"
                f"Which objects have a `{filter_prop.get('name', '')}` value "
                f"exceeding a given threshold?"
            )
            comp_lines.append(
                f"\n#### Result 1.2\n\n"
                f"A SPARQL query with a FILTER on `{filter_prop.get('name', '')}` "
                f"returns the matching subset of objects."
            )

        # Draft SPARQL (inline in markdown)
        sparql_vars = " ".join(f"?{p}" for p in prop_names)
        sparql_bindings = "\n".join(
            f"           proposed:{p} ?{p} ;"
            for p in prop_names
        )
        if sparql_bindings.endswith(" ;"):
            sparql_bindings = sparql_bindings[:-2] + " ."
        sparql = (
            f"\n### Draft SPARQL\n\n"
            f"```sparql\n"
            f"PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>\n"
            f"PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>\n"
            f"PREFIX proposed: <http://example.org/ontology/proposed/>\n\n"
            f"SELECT ?obj {sparql_vars}\n"
            f"WHERE {{\n"
            f"    ?obj a uco-observable:ObservableObject ;\n"
            f"         uco-core:hasFacet ?facet .\n"
            f"    ?facet a proposed:{cls_name} ;\n"
            f"{sparql_bindings}\n"
            f"}}\n"
            f"```"
        )
        comp_lines.append(sparql)

    competencies = "\n".join(comp_lines)

    # --- Example instance data ---
    example_graph = _build_example_graph(proposed_classes)
    example_lines = ["\n# Example instance data\n"]
    if example_graph:
        example_lines.append(
            f"The example graph is also available as a standalone file at "
            f"`change_proposals/{slug}.jsonld` for validation and SPARQL testing.\n"
        )
        example_lines.append("```json")
        example_lines.append(json.dumps(example_graph, indent=2))
        example_lines.append("```")
    example_lines.append(
        "\nI am fine with my examples being transcribed and credited."
    )
    example_section = "\n".join(example_lines)

    # --- Solution suggestion ---
    sol_lines = []
    if proposed_classes:
        for cls in proposed_classes:
            cls_name = cls.get("name", "NewClass")
            parent = cls.get("parent", "uco-core:UcoObject")
            sol_lines.append(f"* Define new class `{cls_name}` as a subclass of `{parent}`")
            for p in cls.get("properties", []):
                sol_lines.append(
                    f"* Define property `{p.get('name', '')}` "
                    f"with range `{p.get('type', 'xsd:string')}`"
                )
            sol_lines.append(f"* Add SHACL shape for `{cls_name}` with property constraints")

    if proposed_properties:
        for prop in proposed_properties:
            sol_lines.append(
                f"* Add property `{prop.get('name', '')}` to "
                f"`{prop.get('target_class', '')}`"
            )

    sol_lines.append("* Add unit test(s) demonstrating valid and invalid usage")
    solution = "\n".join(sol_lines)

    # --- Pre-submission testing ---
    cq_count = 1
    if proposed_classes and len(proposed_classes[0].get("properties", [])) >= 2:
        cq_count = 2
    testing_rows = "\n".join(
        f"| CQ 1.{i} | Not yet | — | |"
        for i in range(1, cq_count + 1)
    )
    testing_section = (
        f"# Pre-submission testing\n\n"
        f"Run `make test-proposal PROPOSAL={slug}` to execute all tests.\n\n"
        f"## SPARQL query testing\n\n"
        f"| Query | Tested | Expected results match | Notes |\n"
        f"|-------|--------|----------------------|-------|\n"
        f"{testing_rows}\n\n"
        f"## Graph validation\n\n"
        f"```\n"
        f"$ make validate-proposal PROPOSAL={slug}\n"
        f"(results pending)\n"
        f"```\n\n"
        f"## Unresolved issues\n\n"
        f"Testing not yet run. Execute `make test-proposal PROPOSAL={slug}` "
        f"and update this section before submission.\n"
    )

    # --- Assemble ---
    sections = [
        target_release_section,
        CHANGE_PROPOSAL_SECTIONS["background"].format(background=background),
        CHANGE_PROPOSAL_SECTIONS["requirements"].format(requirements=requirements),
        CHANGE_PROPOSAL_SECTIONS["risk_benefit"].format(
            benefits=benefits, risks=risks
        ),
        CHANGE_PROPOSAL_SECTIONS["competencies"].format(competencies=competencies),
        example_section,
        CHANGE_PROPOSAL_SECTIONS["solution"].format(solution=solution),
        testing_section,
    ]

    header = (
        f"<!-- Change Proposal: {concept} -->\n"
        f"<!-- Target repository: {target_repo} -->\n"
        f"<!-- Target release: {target_release} -->\n"
        f"<!-- Generated by CASE/UCO SDK draft_change_proposal tool -->\n\n"
    )

    return header + "\n".join(sections)


@mcp.tool
def draft_change_proposal(
    concept: str,
    description: str,
    scenario: str,
    proposed_classes: list[dict] | None = None,
    proposed_properties: list[dict] | None = None,
    target_repo: str | None = None,
    target_release: str = "1.5.0",
    existing_issue_refs: list[str] | None = None,
) -> dict:
    """Draft a CASE/UCO change proposal for a concept not in the ontology.

    Generates a filled-in change proposal markdown file, a companion
    example JSON-LD graph file, and a SPARQL query file for testing.
    The agent should call check_existing_proposals first to avoid duplicates.

    After drafting, run `make test-proposal PROPOSAL=<slug>` to validate
    the example graph and test SPARQL queries before submission.

    Returns the file paths, rendered markdown, and target repository info.

    Args:
        concept: Short name for the proposed concept (e.g., "Drone telemetry facet")
        description: Why the concept is needed and what gap it fills
        scenario: A concrete forensic scenario demonstrating the concept's value
        proposed_classes: List of dicts with keys: name, type, parent, properties
            (each property: name, type, description)
        proposed_properties: List of dicts with keys: name, target_class, type, description
        target_repo: "UCO" or "CASE" — auto-detected if omitted
        target_release: Target ontology release version (e.g., "1.5.0", "2.0.0").
            Defaults to "1.5.0" (current develop branch target).
        existing_issue_refs: Links to related existing issues

    Examples:
        draft_change_proposal(
            concept="Drone telemetry facet",
            description="No existing facet captures UAV flight data...",
            scenario="An investigator extracts telemetry from a DJI drone...",
            proposed_classes=[{"name": "DroneTelemetryFacet", ...}],
            target_repo="UCO",
            target_release="1.5.0"
        )
    """
    triage = suggest_target_repo(concept, description)
    if target_repo is None:
        target_repo = triage["suggestion"]

    slug = _slugify(concept)

    content = _build_proposal_markdown(
        concept=concept,
        description=description,
        scenario=scenario,
        proposed_classes=proposed_classes,
        proposed_properties=proposed_properties,
        target_repo=target_repo if target_repo != "unsure" else "TBD",
        target_release=target_release,
        existing_issue_refs=existing_issue_refs,
        slug=slug,
    )

    out_dir = PROJECT_ROOT / "change_proposals"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write the proposal markdown
    out_path = out_dir / f"{slug}.md"
    out_path.write_text(content, encoding="utf-8")

    generated_files = [str(out_path.relative_to(PROJECT_ROOT))]

    # Write companion example JSON-LD graph
    example_graph = _build_example_graph(proposed_classes)
    if example_graph:
        jsonld_path = out_dir / f"{slug}.jsonld"
        jsonld_path.write_text(
            json.dumps(example_graph, indent=2) + "\n", encoding="utf-8"
        )
        generated_files.append(str(jsonld_path.relative_to(PROJECT_ROOT)))

    # Write companion SPARQL queries
    sparql_text = _build_sparql_queries(proposed_classes)
    if sparql_text:
        sparql_path = out_dir / f"{slug}.sparql"
        sparql_path.write_text(sparql_text, encoding="utf-8")
        generated_files.append(str(sparql_path.relative_to(PROJECT_ROOT)))

    repo_urls = {
        "UCO": "https://github.com/ucoProject/UCO/issues/new",
        "CASE": "https://github.com/casework/CASE/issues/new",
    }

    result: dict = {
        "file_path": str(out_path.relative_to(PROJECT_ROOT)),
        "generated_files": generated_files,
        "target_repo": target_repo,
        "target_release": target_release,
        "triage_reasoning": triage["reasoning"],
        "content_preview": content[:500] + "..." if len(content) > 500 else content,
    }

    if target_repo in repo_urls:
        result["submit_url"] = repo_urls[target_repo]

    if target_repo == "unsure":
        result["action_needed"] = (
            "Could not determine whether this belongs in UCO or CASE. "
            "Please review the triage reasoning and set the target manually. "
            "UCO covers general cyber-domain concepts; CASE covers "
            "investigation-specific concepts."
        )

    result["next_steps"] = [
        f"Review the draft at {out_path.relative_to(PROJECT_ROOT)}",
        f"Run `make test-proposal PROPOSAL={slug}` to validate the example graph and test SPARQL queries",
        "Update the Pre-submission testing section with test results",
        "Refine the requirements, competency questions, and example data",
        "Optionally create a local extension for immediate use (see extensions recipe)",
        f"Submit as a GitHub issue at {repo_urls.get(target_repo, 'the appropriate repo')}",
    ]

    return result


@mcp.resource("case-uco://domains")
def get_domains() -> str:
    """List all forensic domain categories with descriptions."""
    lines = ["# CASE/UCO Forensic Domains\n"]
    for cat in DOMAIN_CATEGORIES:
        lines.append(f"## {cat['title']}")
        lines.append(cat["description"])
        lines.append(f"Keywords: {', '.join(cat['keywords'])}")
        lines.append("")
    return "\n".join(lines)


@mcp.resource("case-uco://profiles")
def get_profiles_resource() -> str:
    """UCO Profile ontologies for interoperability with external ontologies."""
    lines = ["# UCO Profiles\n"]
    lines.append(
        "UCO maintains Profile repositories that align UCO classes with "
        "external ontologies. See: "
        "https://cyberdomainontology.org/ontology/development/#profiles\n"
    )
    for p in UCO_PROFILES:
        lines.append(f"## {p['name']}")
        lines.append(f"**{p['full_name']}** ({p['profile_type']} profile)")
        lines.append(f"Status: {p['status']}")
        lines.append(p["description"])
        lines.append(f"Repo: {p['repo_url']}")
        lines.append(f"Ontology file: {p['ontology_file']}")
        if p.get("related_recipes"):
            lines.append(f"Related recipes: {', '.join(p['related_recipes'])}")
        lines.append("")
    return "\n".join(lines)


@mcp.resource("case-uco://modules")
def get_modules() -> str:
    """List all ontology modules."""
    modules = list_modules()
    lines = ["# CASE/UCO Ontology Modules\n"]
    for m in sorted(modules):
        lines.append(f"- {m}")
    return "\n".join(lines)


@mcp.resource("case-uco://patterns")
def get_patterns() -> str:
    """Core modeling patterns for CASE/UCO graphs."""
    lines = ["# CASE/UCO Modeling Patterns\n"]
    for p in CORE_PATTERNS:
        lines.append(f"## {p['name']}")
        lines.append(p["description"])
        lines.append(f"\n```python\n{p['python_example']}\n```\n")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
