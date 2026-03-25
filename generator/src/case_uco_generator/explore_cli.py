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

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    if not args.command:
        parser.print_help()
        return 1

    repo_root = Path.cwd()
    ontology_dir = args.ontology_dir or repo_root / "ontology"
    extensions_dir = None if args.no_extensions else (args.extensions_dir or repo_root / "extensions")

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


if __name__ == "__main__":
    sys.exit(main())
