#!/usr/bin/env python3
"""Attach the WeChat-translation Layer-1 hash to the insider-threat investigation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.types import Hash

KG = Path("/mnt/d/PACER_Docs/Knowledge_Graphs/BULK_FOLDER/outside")
INV = KG / "insider-threat-investigation.jsonld"
LAYER1 = KG / "pacer -- insider threat -- English translation of WeChat Thread.jsonld"
RETRIEVED = datetime(2026, 8, 28, 16, 0, tzinfo=timezone.utc)


def layer1_hash(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    for node in data.get("@graph", []):
        for facet in node.get("uco-core:hasFacet") or []:
            for item in facet.get("uco-observable:hash") or []:
                value = item.get("uco-types:hashValue") or {}
                digest = value.get("@value") if isinstance(value, dict) else value
                if digest:
                    return str(digest)
    raise ValueError(f"no hash in {path}")


def main() -> None:
    # The copied exemplar declares its own kb: base, so adopt it rather than
    # letting the default collide on load.
    context = json.loads(INV.read_text(encoding="utf-8")).get("@context") or {}
    entries = context if isinstance(context, list) else [context]
    kb_prefix = next(
        (
            entry["kb"]
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("kb"), str)
        ),
        "http://example.org/kb/",
    )
    graph = CASEGraph(kb_prefix=kb_prefix)
    graph.load_file(INV)
    node_id = "kb:source-wechat-translation"
    if graph.get(node_id):
        print("already attached")
        return
    digest = layer1_hash(LAYER1)
    graph.create(
        ObservableObject,
        id=node_id,
        name="pacer -- insider threat -- English translation of WeChat Thread.pdf",
        has_facet=[
            FileFacet(
                file_name="pacer -- insider threat -- English translation of WeChat Thread.pdf",
                extension="pdf",
            ),
            ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value=digest)]),
        ],
        object_created_time=RETRIEVED,
    )
    # Investigation @id in the copied exemplar may not be kb:investigation.
    inv_id = None
    data = json.loads(INV.read_text(encoding="utf-8"))
    for node in data.get("@graph", []):
        types = node.get("@type")
        if isinstance(types, str):
            types = [types]
        if types and any(str(t).endswith("Investigation") for t in types):
            inv_id = node.get("@id")
            break
    if not inv_id:
        raise SystemExit("no Investigation node")
    graph.add_property(inv_id, "uco-core:object", {"@id": node_id})
    graph.write(INV)
    print(f"attached {node_id} to {inv_id}")


if __name__ == "__main__":
    main()
