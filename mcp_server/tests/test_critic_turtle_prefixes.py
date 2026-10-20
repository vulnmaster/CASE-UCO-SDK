"""Turtle namespace bindings must survive canonicalization like JSON-LD contexts."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
for entry in (ROOT / "mcp_server", ROOT / "python"):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from critic.canonical import DEFAULT_PREFIXES, load_canonical_graph
from critic.graph_integrity import analyze_graph_integrity, sha256_file


class TurtlePrefixTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write_turtle(self, text):
        path = self.root / "graph.ttl"
        path.write_text(text, encoding="utf-8")
        return path

    def test_document_prefix_is_retained(self):
        path = self.write_turtle(
            '@prefix kb: <https://example.invalid/kb/> .\n'
            'kb:one <urn:example:label> "one" .\n'
        )
        view = load_canonical_graph(path)
        self.assertEqual(view.rdf_status, "ok")
        self.assertEqual(view.prefixes.get("kb"), "https://example.invalid/kb/")
        self.assertEqual(view.expand("kb:one"), "https://example.invalid/kb/one")

    def test_default_namespace_is_retained(self):
        path = self.write_turtle(
            '@prefix : <https://example.invalid/default/> .\n'
            ':one <urn:example:label> "one" .\n'
        )
        view = load_canonical_graph(path)
        self.assertEqual(view.prefixes.get(""), "https://example.invalid/default/")
        self.assertEqual(view.expand(":one"), "https://example.invalid/default/one")

    def test_document_binding_overrides_the_fallback_for_that_prefix(self):
        path = self.write_turtle(
            '@prefix uco-core: <urn:example:custom:> .\n'
            'uco-core:one uco-core:label "one" .\n'
        )
        view = load_canonical_graph(path)
        self.assertEqual(view.expand("uco-core:one"), "urn:example:custom:one")
        self.assertIn("urn:example:custom:one", view.nodes)

    def test_undeclared_well_known_prefix_keeps_its_fallback(self):
        path = self.write_turtle('<urn:example:one> <urn:example:label> "one" .')
        view = load_canonical_graph(path)
        self.assertEqual(view.prefixes["uco-core"], DEFAULT_PREFIXES["uco-core"])

    def test_equivalent_turtle_and_jsonld_expand_kb_the_same_way(self):
        turtle = self.write_turtle(
            '@prefix kb: <https://example.invalid/kb/> .\n'
            'kb:one <urn:example:label> "one" .\n'
        )
        jsonld = self.root / "graph.jsonld"
        jsonld.write_text(json.dumps({
            "@context": {"kb": "https://example.invalid/kb/"},
            "@graph": [{"@id": "kb:one", "urn:example:label": "one"}],
        }), encoding="utf-8")
        left, right = load_canonical_graph(turtle), load_canonical_graph(jsonld)
        self.assertEqual(left.rdf_status, "ok")
        self.assertEqual(right.rdf_status, "ok")
        self.assertEqual(left.expand("kb:one"), right.expand("kb:one"))
        self.assertEqual(set(left.nodes), set(right.nodes))

    def test_kb_reference_without_a_subject_is_reported(self):
        path = self.write_turtle(
            '@prefix kb: <https://example.invalid/kb/> .\n'
            'kb:one <urn:example:related> kb:missing .\n'
        )
        _, findings, _ = analyze_graph_integrity(path, artifact_hash=sha256_file(path))
        dangling = [f for f in findings if f.rule_id == "CRIT-G-DANGLING-REF"]
        self.assertEqual([f.target.node_id for f in dangling],
                         ["https://example.invalid/kb/missing"])

    def test_kb_reference_with_a_subject_is_not_reported(self):
        path = self.write_turtle(
            '@prefix kb: <https://example.invalid/kb/> .\n'
            'kb:one <urn:example:related> kb:two .\n'
            'kb:two <urn:example:label> "two" .\n'
        )
        _, findings, _ = analyze_graph_integrity(path, artifact_hash=sha256_file(path))
        self.assertFalse([f for f in findings if f.rule_id == "CRIT-G-DANGLING-REF"])

    def test_invalid_turtle_remains_a_parse_error(self):
        path = self.write_turtle('@prefix kb: <https://example.invalid/kb/> . kb:one')
        view = load_canonical_graph(path)
        self.assertEqual(view.rdf_status, "rdf_parse_error")
        self.assertFalse(view.nodes)


if __name__ == "__main__":
    unittest.main()
