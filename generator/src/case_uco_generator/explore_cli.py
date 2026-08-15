"""CLI entry point for the CASE/UCO ontology explorer (case-uco-explore)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from case_uco_generator.ontology_parser import parse_ontology
from case_uco_generator.explorer import (
    search,
    get_class,
    list_modules,
    get_module_classes,
    find_by_property_type,
    format_class_list,
    format_class_detail,
    format_modules,
    format_hierarchy,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="case-uco-explore",
        description="Explore and search the CASE/UCO ontology interactively.",
    )
    parser.add_argument(
        "--ontology-dir",
        type=Path,
        default=None,
        help="Path to ontology/ directory (default: auto-detect from repo root)",
    )
    parser.add_argument(
        "--extensions-dir",
        type=Path,
        default=None,
        help="Path to extensions/ directory (default: auto-detect from repo root)",
    )
    parser.add_argument(
        "--no-extensions",
        action="store_true",
        help="Skip loading extension ontologies",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    subparsers = parser.add_subparsers(dest="command", help="Explorer command")

    sp_search = subparsers.add_parser("search", help="Search classes by keyword")
    sp_search.add_argument("query", help="Search term (substring match on names and descriptions)")

    sp_class = subparsers.add_parser("class", help="Show full details for a class")
    sp_class.add_argument("name", help="Class name (e.g. FileFacet)")

    sp_module = subparsers.add_parser("module", help="List all classes in a module")
    sp_module.add_argument("name", help="Module name (e.g. observable, uco.observable)")

    subparsers.add_parser("modules", help="List all modules with class counts")

    sp_hierarchy = subparsers.add_parser("hierarchy", help="Show inheritance tree for a class")
    sp_hierarchy.add_argument("name", help="Class name (e.g. FileFacet)")

    sp_props = subparsers.add_parser("properties", help="Find classes by property type")
    sp_props.add_argument("--type", required=True, dest="type_name", help="Property range type (e.g. Tool)")

    subparsers.add_parser("profiles", help="List Composition Profiles (no ontology parse)")
    sp_profile = subparsers.add_parser("profile", help="Show one Composition Profile")
    sp_profile.add_argument("name", help="Profile id (e.g. MinimalForensics, FullCACLifecycle)")
    subparsers.add_parser("spine", help="Show the CAC semantic spine and UCO core hierarchy")
    sp_contract = subparsers.add_parser("contract", help="Show a synthesized Profile Contract (no OWL parse)")
    sp_contract.add_argument("name", help="Profile id (e.g. HashIntelligence)")

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    if not args.command:
        parser.print_help()
        return 1

    if args.command in {"profiles", "profile", "spine", "contract"}:
        return _cmd_topology(args)

    repo_root = Path.cwd()
    ontology_dir = args.ontology_dir or repo_root / "ontology"
    if args.no_extensions:
        extensions_dir = None
    elif args.extensions_dir:
        extensions_dir = [args.extensions_dir]
    else:
        extensions_dir = [repo_root / "extensions", repo_root / "ontology"]

    if not ontology_dir.exists():
        print(f"Error: ontology directory not found: {ontology_dir}", file=sys.stderr)
        return 1

    schema = parse_ontology(ontology_dir, extensions_dir=extensions_dir)

    if args.command == "search":
        results = search(schema, args.query)
        print(f'\nSearch results for "{args.query}" ({len(results)} matches):\n')
        print(format_class_list(results))

    elif args.command == "class":
        cls = get_class(schema, args.name)
        if not cls:
            print(f'Error: class "{args.name}" not found.', file=sys.stderr)
            close = search(schema, args.name)[:5]
            if close:
                print("\nDid you mean one of these?\n")
                print(format_class_list(close))
            return 1
        print(f"\n{format_class_detail(schema, cls)}")

    elif args.command == "module":
        classes = get_module_classes(schema, args.name)
        if not classes:
            print(f'Error: module "{args.name}" not found.', file=sys.stderr)
            mods = list_modules(schema)
            mod_names = [m[0] for m in mods if args.name.lower() in m[0].lower()]
            if mod_names:
                print(f"\nDid you mean: {', '.join(mod_names)}?")
            return 1
        print(f"\nClasses in module matching '{args.name}' ({len(classes)} classes):\n")
        print(format_class_list(classes))

    elif args.command == "modules":
        mods = list_modules(schema)
        print(f"\nOntology modules:\n")
        print(format_modules(mods))

    elif args.command == "hierarchy":
        cls = get_class(schema, args.name)
        if not cls:
            print(f'Error: class "{args.name}" not found.', file=sys.stderr)
            return 1
        print(f"\nInheritance hierarchy for {cls.name}:\n")
        print(format_hierarchy(schema, cls))

    elif args.command == "properties":
        results = find_by_property_type(schema, args.type_name)
        print(f'\nClasses with properties of type "{args.type_name}" ({len(results)} matches):\n')
        print(format_class_list(results))

    print()
    return 0


def _cmd_topology(args: argparse.Namespace) -> int:
    """Composition Profiles and spine — JSON only, no OWL parse."""
    # Import from the repo checkout when the generator is run in-tree.
    repo_root = Path.cwd()
    python_dir = repo_root / "python"
    if python_dir.is_dir() and str(python_dir) not in sys.path:
        sys.path.insert(0, str(python_dir))

    from case_uco.topology import (
        get_profile,
        get_semantic_spine,
        list_profiles,
        list_spine_kinds,
    )

    if args.command == "profiles":
        profiles = list_profiles()
        print(f"\nComposition Profiles ({len(profiles)}):\n")
        for profile in profiles:
            air = "air-gapped" if profile.air_gapped else "network-ok"
            print(f"  {profile.id:24s}  v{profile.version}  [{air}]")
            print(f"    {profile.title}")
            print(f"    {profile.description}")
            print()
        return 0

    if args.command == "profile":
        profile = get_profile(args.name)
        if profile is None:
            print(f'Error: profile "{args.name}" not found.', file=sys.stderr)
            known = ", ".join(p.id for p in list_profiles())
            print(f"Known profiles: {known}", file=sys.stderr)
            return 1
        print(f"\n# {profile.id} v{profile.version} — {profile.title}\n")
        print(profile.description)
        if profile.mission:
            print(f"\nMission: {profile.mission}")
        print("\nRequired modules:")
        for module in profile.required_modules:
            print(f"  - {module}")
        print("\nRecommended Facet sets:")
        for facet_set in profile.facet_sets:
            req = ", ".join(facet_set.required) or "(none)"
            rec = ", ".join(facet_set.recommended) or "(none)"
            print(f"  {facet_set.host}: required={req}; recommended={rec}")
        print("\nSpine anchors:")
        for anchor in profile.spine_anchors:
            print(f"  - {anchor}")
        print("\nRecipe skeleton:")
        print(f"  {profile.recipe_skeleton.get('summary', '')}")
        for step in profile.recipe_skeleton.get("steps", []):
            print(f"  - {step}")
        print()
        return 0

    if args.command == "contract":
        from case_uco.contracts import load_contract

        try:
            contract = load_contract(args.name)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"\n# {contract.profile_id} v{contract.profile_version} contract {contract.contract_schema_version}\n")
        print(f"Checks ({len(contract.checks)}):")
        for check in contract.checks:
            print(f"  {check.id:20s}  {check.kind:28s}  when={check.when}  blocking={check.blocking}")
        print("\nDefault validation:", contract.default_validation)
        print("Partition policy:", contract.partition_policy)
        print()
        return 0

    spine = get_semantic_spine()
    print("\n# CAC semantic spine\n")
    print("Kinds:", ", ".join(spine.get("cac_spine", {}).get("kinds", [])))
    print()
    for kind in list_spine_kinds():
        print(f"  {kind.name:20s}  [{kind.kind}]")
        print(f"    {kind.comment}")
    print("\n# UCO core hierarchy\n")
    for node in spine.get("uco_core_hierarchy", []):
        parent = node.get("parent")
        suffix = f"  ⊂ {parent}" if parent else ""
        print(f"  {node.get('name')}{suffix}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
