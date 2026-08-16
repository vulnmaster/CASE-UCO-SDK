#!/usr/bin/env python3
"""Prove that benchmark graphs from every SDK language are RDF-isomorphic (#81)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rdflib import Graph
from rdflib.compare import to_canonical_graph, to_isomorphic


def canonical_hash(graph: Graph) -> str:
    canonical = to_canonical_graph(graph)
    statements = sorted(
        f"{subject.n3()} {predicate.n3()} {obj.n3()} ."
        for subject, predicate, obj in canonical
    )
    return hashlib.sha256(("\n".join(statements) + "\n").encode()).hexdigest()


def portable_path(path: Path) -> str:
    """Prefer a workspace-relative evidence path over a host-specific path."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph",
        action="append",
        required=True,
        metavar="LANGUAGE=PATH",
        help="language-labelled JSON-LD graph (repeat for every SDK)",
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    graphs: dict[str, Graph] = {}
    evidence: dict[str, dict[str, object]] = {}
    for specification in args.graph:
        if "=" not in specification:
            parser.error("--graph values must use LANGUAGE=PATH")
        language, path_text = specification.split("=", 1)
        if language in graphs:
            parser.error(f"duplicate language: {language}")
        path = Path(path_text)
        if not path.is_file():
            parser.error(f"graph does not exist: {path}")
        graph = Graph()
        graph.parse(path, format="json-ld")
        graphs[language] = graph
        evidence[language] = {
            "path": portable_path(path),
            "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "rdf_canonical_sha256": canonical_hash(graph),
            "triple_count": len(graph),
        }
    if len(graphs) < 2:
        parser.error("at least two language graphs are required")

    reference_language = sorted(graphs)[0]
    reference = to_isomorphic(graphs[reference_language])
    mismatches = sorted(
        language
        for language, graph in graphs.items()
        if to_isomorphic(graph) != reference
    )
    result = {
        "suite": "case-uco-cross-language-rdf-equivalence",
        "schema_version": "1.0.0",
        "reference_language": reference_language,
        "equivalent": not mismatches,
        "mismatched_languages": mismatches,
        "languages": evidence,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
