"""CASE/UCO SDK MCP Server — ontology discovery tools for AI coding agents.

Exposes the SDK's registry API as MCP tools so AI agents in Cursor,
Claude Code, and similar tools can query the ontology programmatically
instead of parsing markdown documentation.

Run: python mcp_server/server.py
Or:  fastmcp dev mcp_server/server.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from fastmcp import FastMCP

from case_uco.registry import (
    search,
    get_class,
    find_facets,
    find_by_property_type,
    list_modules,
    list_vocabs,
)
from domain_index import (
    TASK_TO_CLASSES,
    DOMAIN_CATEGORIES,
    CORE_PATTERNS,
    RECIPE_INDEX,
)

mcp = FastMCP(
    "CASE/UCO SDK",
    instructions=(
        "Tools for discovering CASE/UCO ontology classes, properties, and "
        "forensic workflow patterns. Use search_classes to find classes by "
        "keyword, get_class_details for full property info, and "
        "find_classes_for_domain to map investigative tasks to the right types."
    ),
)


@mcp.tool
def search_classes(query: str) -> list[dict]:
    """Search for CASE/UCO classes by keyword.

    Case-insensitive substring match on class name and description.
    Returns matching classes with name, module, description, and property count.

    Examples: search_classes("file"), search_classes("network"),
              search_classes("mobile"), search_classes("email")
    """
    results = search(query)
    return [
        {
            "name": r["name"],
            "module": r["module"],
            "description": r.get("description", "")[:200],
            "property_count": len(r.get("properties", [])),
            "is_facet": r.get("is_facet", False),
        }
        for r in results
    ]


@mcp.tool
def get_class_details(name: str) -> dict | None:
    """Get full details for a CASE/UCO class including all properties.

    Returns the class IRI, module, description, parent classes, and a
    complete property table with types, cardinalities, and required flags.

    Examples: get_class_details("FileFacet"), get_class_details("Investigation")
    """
    cls = get_class(name)
    if cls is None:
        return None
    return {
        "name": cls["name"],
        "iri": cls.get("iri", ""),
        "module": cls.get("module", ""),
        "description": cls.get("description", ""),
        "parents": cls.get("parents", []),
        "is_facet": cls.get("is_facet", False),
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
def find_classes_for_domain(domain: str) -> dict:
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
    for cat in DOMAIN_CATEGORIES:
        title_match = q in cat["title"].lower()
        keyword_match = any(kw in q for kw in cat["keywords"])
        if title_match or keyword_match:
            matching_categories.append({
                "domain": cat["title"],
                "description": cat["description"],
            })

    return {
        "query": domain,
        "task_templates": matching_tasks,
        "related_domains": matching_categories,
        "tip": (
            "Use get_class_details(name) on any class above to see its full "
            "property table. The most common pattern is ObservableObject + "
            "Facets — create an ObservableObject and attach Facets to describe it."
        ),
    }


@mcp.tool
def list_all_facets() -> list[dict]:
    """List all Facet classes in the CASE/UCO ontology.

    Facets are attached to ObservableObjects to describe specific aspects.
    Use this when you know you need the ObservableObject + Facet pattern
    but need to find the right Facet for your data.
    """
    results = find_facets()
    return [
        {
            "name": r["name"],
            "module": r["module"],
            "description": r.get("description", "")[:200],
            "property_count": len(r.get("properties", [])),
        }
        for r in results
    ]


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

    return {
        "title": best_match["title"],
        "description": best_match["description"],
        "file": best_match["file"],
        "tip": (
            f"Read {best_match['file']} for complete code examples."
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
