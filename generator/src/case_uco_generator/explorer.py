"""Ontology explorer — search, browse, and inspect CASE/UCO classes interactively."""

from __future__ import annotations

from case_uco_generator.schema_model import (
    OntologyClass,
    OntologySchema,
    iri_local_name,
)


def search(schema: OntologySchema, query: str) -> list[OntologyClass]:
    """Search classes by substring match on name or description (case-insensitive)."""
    q = query.lower()
    results: list[OntologyClass] = []
    for cls in schema.classes.values():
        if q in cls.name.lower() or q in cls.description.lower():
            results.append(cls)
    results.sort(key=lambda c: (c.module, c.name))
    return results


def get_class(schema: OntologySchema, name: str) -> OntologyClass | None:
    """Look up a class by local name (case-insensitive)."""
    name_lower = name.lower()
    for cls in schema.classes.values():
        if cls.name.lower() == name_lower:
            return cls
    return None


def list_modules(schema: OntologySchema) -> list[tuple[str, int]]:
    """Return (module_key, class_count) pairs sorted by module key."""
    return sorted(
        (key, len(iris)) for key, iris in schema.modules.items()
    )


def get_module_classes(schema: OntologySchema, module_query: str) -> list[OntologyClass]:
    """Return classes in a module. Accepts partial names like 'observable'."""
    q = module_query.lower()
    for key in sorted(schema.modules):
        if key.lower() == q or key.lower().endswith(f".{q}"):
            return sorted(
                (schema.classes[iri] for iri in schema.modules[key] if iri in schema.classes),
                key=lambda c: c.name,
            )
    return []


def get_ancestors(schema: OntologySchema, cls: OntologyClass) -> list[OntologyClass]:
    """Walk up the inheritance chain and return ancestors (nearest first)."""
    ancestors: list[OntologyClass] = []
    visited: set[str] = set()
    stack = list(cls.parent_iris)
    while stack:
        iri = stack.pop(0)
        if iri in visited:
            continue
        visited.add(iri)
        parent = schema.resolve_class(iri)
        if parent:
            ancestors.append(parent)
            stack.extend(parent.parent_iris)
    return ancestors


def get_descendants(schema: OntologySchema, cls: OntologyClass) -> list[OntologyClass]:
    """Find all classes that have cls as an ancestor."""
    descendants: list[OntologyClass] = []
    for other in schema.classes.values():
        if other.iri == cls.iri:
            continue
        if cls.iri in other.parent_iris:
            descendants.append(other)
    descendants.sort(key=lambda c: c.name)
    return descendants


def find_by_property_type(schema: OntologySchema, type_name: str) -> list[OntologyClass]:
    """Find classes with properties whose range matches type_name."""
    q = type_name.lower()
    results: list[OntologyClass] = []
    for cls in schema.classes.values():
        all_props = schema.resolve_all_properties(cls)
        for prop in all_props:
            range_name = iri_local_name(prop.range_iri).lower()
            if range_name == q:
                results.append(cls)
                break
    results.sort(key=lambda c: (c.module, c.name))
    return results


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_class_list(classes: list[OntologyClass], max_desc: int = 60) -> str:
    """Format a list of classes as an aligned table."""
    if not classes:
        return "  (no results)"
    rows: list[tuple[str, str, str]] = []
    for cls in classes:
        desc = cls.description[:max_desc]
        if len(cls.description) > max_desc:
            desc += "..."
        rows.append((cls.module, cls.name, desc))

    col1 = max(len(r[0]) for r in rows)
    col2 = max(len(r[1]) for r in rows)

    lines = [f"  {'Module':<{col1}}  {'Class':<{col2}}  Description"]
    lines.append(f"  {'-' * col1}  {'-' * col2}  {'-' * 40}")
    for mod, name, desc in rows:
        lines.append(f"  {mod:<{col1}}  {name:<{col2}}  {desc}")
    return "\n".join(lines)


def format_class_detail(schema: OntologySchema, cls: OntologyClass) -> str:
    """Format full details for a single class."""
    lines: list[str] = []
    lines.append(f"Class: {cls.name}")
    lines.append(f"IRI:   {cls.iri}")
    lines.append(f"Module: {cls.module}")
    if cls.is_facet:
        lines.append("Type:  Facet")
    lines.append("")

    if cls.description:
        lines.append("Description:")
        lines.append(f"  {cls.description}")
        lines.append("")

    if cls.parent_iris:
        parent_names = [iri_local_name(p) for p in cls.parent_iris]
        lines.append(f"Parents: {', '.join(parent_names)}")

    ancestors = get_ancestors(schema, cls)
    if ancestors:
        chain = " -> ".join(a.name for a in ancestors)
        lines.append(f"Inheritance chain: {cls.name} -> {chain}")

    descendants = get_descendants(schema, cls)
    if descendants:
        lines.append(f"Direct subclasses: {', '.join(d.name for d in descendants)}")

    lines.append("")

    all_props = schema.resolve_all_properties(cls)
    if all_props:
        lines.append("Properties (including inherited):")
        name_w = max(len(p.name) for p in all_props)
        type_w = max(len(iri_local_name(p.range_iri)) for p in all_props)
        card_w = 12

        lines.append(f"  {'Name':<{name_w}}  {'Type':<{type_w}}  {'Cardinality':<{card_w}}  Req  Description")
        lines.append(f"  {'-' * name_w}  {'-' * type_w}  {'-' * card_w}  ---  {'-' * 40}")
        for prop in all_props:
            type_name = iri_local_name(prop.range_iri)
            req = "Yes" if prop.cardinality.is_required else " No"
            desc = prop.description[:50] + "..." if len(prop.description) > 50 else prop.description
            lines.append(
                f"  {prop.name:<{name_w}}  {type_name:<{type_w}}  "
                f"{prop.cardinality.value:<{card_w}}  {req}  {desc}"
            )
    else:
        lines.append("Properties: (none)")

    return "\n".join(lines)


def format_modules(modules: list[tuple[str, int]]) -> str:
    """Format modules list as a table."""
    if not modules:
        return "  (no modules found)"
    col1 = max(len(m[0]) for m in modules)
    lines = [f"  {'Module':<{col1}}  Classes"]
    lines.append(f"  {'-' * col1}  -------")
    total = 0
    for name, count in modules:
        lines.append(f"  {name:<{col1}}  {count:>7}")
        total += count
    lines.append(f"\n  Total: {total} classes across {len(modules)} modules")
    return "\n".join(lines)


def format_hierarchy(schema: OntologySchema, cls: OntologyClass, depth: int = 0) -> str:
    """Render a tree of a class's position in the hierarchy."""
    lines: list[str] = []

    ancestors = get_ancestors(schema, cls)
    ancestors.reverse()

    for i, anc in enumerate(ancestors):
        indent = "  " * i
        lines.append(f"{indent}{anc.name}")
    target_indent = "  " * len(ancestors)
    lines.append(f"{target_indent}{cls.name}  <--")

    descendants = get_descendants(schema, cls)
    for desc in descendants:
        lines.append(f"{target_indent}  {desc.name}")
        sub_descs = get_descendants(schema, desc)
        for sd in sub_descs:
            lines.append(f"{target_indent}    {sd.name}")

    return "\n".join(lines)
