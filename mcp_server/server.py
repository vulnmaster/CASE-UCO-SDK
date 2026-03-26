"""CASE/UCO SDK MCP Server — ontology discovery tools for AI coding agents.

Exposes the SDK's registry API as MCP tools so AI agents in Cursor,
Claude Code, and similar tools can query the ontology programmatically
instead of parsing markdown documentation.

Run: python mcp_server/server.py
Or:  fastmcp dev mcp_server/server.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from fastmcp import FastMCP

from case_uco.registry import (
    search,
    get_class,
    find_facets,
    list_modules,
    list_vocabs,
)
from domain_index import (
    TASK_TO_CLASSES,
    DOMAIN_CATEGORIES,
    CORE_PATTERNS,
    RECIPE_INDEX,
    CHANGE_PROPOSAL_SECTIONS,
    suggest_target_repo,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

mcp = FastMCP(
    "CASE/UCO SDK",
    instructions=(
        "Tools for discovering CASE/UCO ontology classes, properties, and "
        "forensic workflow patterns. Use search_classes to find classes by "
        "keyword, get_class_details for full property info, and "
        "find_classes_for_domain to map investigative tasks to the right types. "
        "When a concept is missing from the ontology, use check_existing_proposals "
        "to search for prior proposals in UCO/CASE issue trackers, then "
        "draft_change_proposal to generate a filled-in change proposal."
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


def _build_proposal_markdown(
    concept: str,
    description: str,
    scenario: str,
    proposed_classes: list[dict] | None,
    proposed_properties: list[dict] | None,
    target_repo: str,
    existing_issue_refs: list[str] | None,
) -> str:
    """Render a filled-in change proposal from the official template."""

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

        # Draft SPARQL
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
    sol_lines.append(
        "\nI am fine with my examples being transcribed and credited."
    )
    solution = "\n".join(sol_lines)

    # --- Example JSON-LD ---
    example_lines = ["\n# Example instance data\n"]
    if proposed_classes:
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

        example_graph = {
            "@context": {
                "proposed": "http://example.org/ontology/proposed/",
                "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
                "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            },
            "@graph": [
                {
                    "@type": "uco-observable:ObservableObject",
                    "uco-core:hasFacet": [example_obj],
                }
            ],
        }
        example_lines.append("```json")
        example_lines.append(json.dumps(example_graph, indent=2))
        example_lines.append("```")

    example_section = "\n".join(example_lines)

    # --- Assemble ---
    sections = [
        CHANGE_PROPOSAL_SECTIONS["background"].format(background=background),
        CHANGE_PROPOSAL_SECTIONS["requirements"].format(requirements=requirements),
        CHANGE_PROPOSAL_SECTIONS["risk_benefit"].format(
            benefits=benefits, risks=risks
        ),
        CHANGE_PROPOSAL_SECTIONS["competencies"].format(competencies=competencies),
        CHANGE_PROPOSAL_SECTIONS["solution"].format(solution=solution),
        example_section,
    ]

    header = (
        f"<!-- Change Proposal: {concept} -->\n"
        f"<!-- Target repository: {target_repo} -->\n"
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
    existing_issue_refs: list[str] | None = None,
) -> dict:
    """Draft a CASE/UCO change proposal for a concept not in the ontology.

    Generates a filled-in change proposal markdown file using the official
    CDO template. The agent should call check_existing_proposals first
    to avoid duplicates.

    Returns the file path, rendered markdown, and target repository info.

    Args:
        concept: Short name for the proposed concept (e.g., "Drone telemetry facet")
        description: Why the concept is needed and what gap it fills
        scenario: A concrete forensic scenario demonstrating the concept's value
        proposed_classes: List of dicts with keys: name, type, parent, properties
            (each property: name, type, description)
        proposed_properties: List of dicts with keys: name, target_class, type, description
        target_repo: "UCO" or "CASE" — auto-detected if omitted
        existing_issue_refs: Links to related existing issues

    Examples:
        draft_change_proposal(
            concept="Drone telemetry facet",
            description="No existing facet captures UAV flight data...",
            scenario="An investigator extracts telemetry from a DJI drone...",
            proposed_classes=[{"name": "DroneTelemetryFacet", ...}],
            target_repo="UCO"
        )
    """
    # Auto-detect target repo if not specified
    triage = suggest_target_repo(concept, description)
    if target_repo is None:
        target_repo = triage["suggestion"]

    content = _build_proposal_markdown(
        concept=concept,
        description=description,
        scenario=scenario,
        proposed_classes=proposed_classes,
        proposed_properties=proposed_properties,
        target_repo=target_repo if target_repo != "unsure" else "TBD",
        existing_issue_refs=existing_issue_refs,
    )

    slug = _slugify(concept)
    out_dir = PROJECT_ROOT / "change_proposals"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"
    out_path.write_text(content, encoding="utf-8")

    repo_urls = {
        "UCO": "https://github.com/ucoProject/UCO/issues/new",
        "CASE": "https://github.com/casework/CASE/issues/new",
    }

    result: dict = {
        "file_path": str(out_path.relative_to(PROJECT_ROOT)),
        "target_repo": target_repo,
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
        "Refine the requirements, competency questions, and SPARQL queries",
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
