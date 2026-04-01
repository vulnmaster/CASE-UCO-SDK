#!/usr/bin/env python3
"""Test SPARQL queries from a .sparql file against a JSON-LD graph.

Queries in the .sparql file are separated by '# ---' lines.
Each query's comment lines (starting with #) are stripped before execution.
Exit code 0 if all queries return at least one result, 1 otherwise.
"""
import argparse
import sys

import rdflib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonld", help="Path to JSON-LD graph file")
    parser.add_argument("sparql", help="Path to SPARQL queries file")
    args = parser.parse_args()

    g = rdflib.Graph()
    g.parse(args.jsonld, format="json-ld")
    print(f"Loaded {len(g)} triples from {args.jsonld}")

    with open(args.sparql) as f:
        sparql_text = f.read()
    raw_queries = [q.strip() for q in sparql_text.split("# ---") if q.strip()]
    if len(raw_queries) <= 1:
        raw_queries = [sparql_text]

    passed = 0
    failed = 0

    for i, raw in enumerate(raw_queries, 1):
        title_line = ""
        for line in raw.strip().splitlines():
            if line.startswith("#"):
                title_line = line.lstrip("# ").strip()
                break

        lines = [l for l in raw.strip().splitlines() if not l.startswith("#")]
        query = "\n".join(lines)
        if not query.strip():
            continue

        try:
            results = list(g.query(query))
            status = "OK" if results else "WARNING (0 results)"
            print(f"  Query {i}: {len(results)} result(s) — {status}")
            if title_line:
                print(f"           {title_line}")
            if results:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  Query {i}: FAILED — {e}")
            if title_line:
                print(f"           {title_line}")
            failed += 1

    print(f"\nSPARQL test summary: {passed} passed, {failed} failed")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
