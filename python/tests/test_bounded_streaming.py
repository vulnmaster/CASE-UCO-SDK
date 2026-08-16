from __future__ import annotations

import json

import pytest

from case_uco import JsonLdStreamWriter


CONTEXT = {
    "kb": "https://example.org/kb/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
}


def test_bounded_writer_accepts_incremental_nodes(tmp_path):
    output = tmp_path / "bounded.jsonld"
    with JsonLdStreamWriter(
        output, context=CONTEXT, max_node_bytes=256
    ) as writer:
        for i in range(1_000):
            writer.write_node(
                {
                    "@id": f"kb:node-{i}",
                    "@type": "uco-core:UcoObject",
                    "uco-core:name": f"Node {i}",
                }
            )
        metrics = writer.metrics
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert len(payload["@graph"]) == 1_000
    assert metrics.nodes == 1_000
    assert metrics.max_node_bytes_written <= 256


def test_bounded_writer_rejects_unknown_prefix_and_preserves_destination(tmp_path):
    output = tmp_path / "existing.jsonld"
    output.write_bytes(b"SURVIVE")
    with pytest.raises(ValueError, match="undeclared JSON-LD prefix"):
        with JsonLdStreamWriter(output, context=CONTEXT) as writer:
            writer.write_node(
                {"@id": "kb:node", "@type": "evil:Fabricated", "evil:value": 1}
            )
    assert output.read_bytes() == b"SURVIVE"
    assert not list(tmp_path.glob("*.jsonld.tmp"))


def test_bounded_writer_enforces_node_cap_and_preserves_destination(tmp_path):
    output = tmp_path / "existing.jsonld"
    output.write_bytes(b"SURVIVE")
    with pytest.raises(ValueError, match="max_node_bytes"):
        with JsonLdStreamWriter(
            output, context=CONTEXT, max_node_bytes=128
        ) as writer:
            writer.write_node(
                {
                    "@id": "kb:oversized",
                    "@type": "uco-core:UcoObject",
                    "uco-core:name": "x" * 1_000,
                }
            )
    assert output.read_bytes() == b"SURVIVE"
