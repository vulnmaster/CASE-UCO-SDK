"""Focused checks for the method-aware content-hash index."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from case_uco.graph import CASEGraph
from case_uco.hash_index import normalize_hash_digest, normalize_hash_method
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.types import Hash

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / "python" / "case_uco" / "hash_index.py"
DOC_PATH = REPO_ROOT / "docs" / "HASH_INDEX.md"

# Synthetic SHA-256 of the empty file. Public, not case material.
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92402706899c32911cf29121339aa1a904b"
EMPTY_MD5 = "d41d8cd98f00b204e9800998ecf8427e"

FORBIDDEN_SUBSTRINGS = (
    "photodna",
    "photo-dna",
    "vics",
    "court-defensible",
    "court defensible",
    "2.0.0",
    "2.0.1",
    "investigationworkflow",
    "model_csam",
)


def _hashed_file(
    graph: CASEGraph,
    *,
    file_id: str,
    file_name: str,
    hashes: list[tuple[str, str]],
) -> ObservableObject:
    return graph.create(
        ObservableObject,
        id=file_id,
        has_facet=[
            FileFacet(file_name=[file_name]),
            ContentDataFacet(
                hash=[
                    Hash(hash_method=method, hash_value=value) for method, value in hashes
                ]
            ),
        ],
    )


def test_normalization_is_method_and_digest_aware() -> None:
    assert normalize_hash_method(" sha256 ") == "SHA256"
    assert normalize_hash_method("SHA-256") == "SHA-256"
    assert normalize_hash_digest("  E3B0 C442  ") == "e3b0c442"
    assert normalize_hash_digest("0x" + EMPTY_SHA256.upper()) == EMPTY_SHA256


def test_lookup_distinguishes_method_on_the_same_digest_string() -> None:
    graph = CASEGraph()
    _hashed_file(
        graph,
        file_id="kb:File-a",
        file_name="a.bin",
        hashes=[("SHA256", EMPTY_SHA256), ("MD5", EMPTY_MD5)],
    )
    _hashed_file(
        graph,
        file_id="kb:File-b",
        file_name="b.bin",
        hashes=[("MD5", EMPTY_SHA256)],
    )

    sha = graph.lookup_hash(EMPTY_SHA256, method="SHA256")
    md5_same_hex = graph.lookup_hash(EMPTY_SHA256, method="MD5")
    all_hits = graph.lookup_hash("0x" + EMPTY_SHA256.upper())

    assert [hit["id"] for hit in sha] == ["kb:File-a"]
    assert [hit["id"] for hit in md5_same_hex] == ["kb:File-b"]
    assert {hit["id"] for hit in all_hits} == {"kb:File-a", "kb:File-b"}
    assert graph.index_content_hashes()["SHA256"][EMPTY_SHA256][0]["id"] == "kb:File-a"


def test_index_survives_load_and_resolves_standalone_hash_refs() -> None:
    source = CASEGraph()
    digest = EMPTY_SHA256
    source.create(Hash, id="kb:Hash-empty", hash_method="sha256", hash_value=digest)
    source.upsert_node(
        "kb:File-ref",
        types="uco-observable:ObservableObject",
        properties={
            "uco-observable:hash": [{"@id": "kb:Hash-empty"}],
        },
    )
    loaded = CASEGraph()
    loaded.load(source.serialize())

    hits = loaded.lookup_hash(digest, method="SHA256")
    assert {hit["id"] for hit in hits} == {"kb:Hash-empty", "kb:File-ref"}


def test_mutation_and_load_invalidate_stale_hits() -> None:
    graph = CASEGraph()
    _hashed_file(
        graph,
        file_id="kb:File-old",
        file_name="old.bin",
        hashes=[("SHA256", EMPTY_SHA256)],
    )
    assert graph.lookup_hash(EMPTY_SHA256, method="sha256")
    assert graph._content_hash_index is not None

    graph.set_property(
        "kb:File-old",
        "uco-core:hasFacet",
        [
            {
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [
                    {
                        "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": EMPTY_MD5,
                    }
                ],
            }
        ],
    )
    assert graph._content_hash_index is None
    assert graph.lookup_hash(EMPTY_SHA256, method="SHA256") == []
    assert graph.lookup_hash(EMPTY_MD5, method="SHA256")[0]["id"] == "kb:File-old"

    extra = CASEGraph()
    _hashed_file(
        extra,
        file_id="kb:File-new",
        file_name="new.bin",
        hashes=[("SHA256", EMPTY_SHA256)],
    )
    graph.load(extra.serialize())
    assert graph._content_hash_index is None
    ids = {hit["id"] for hit in graph.lookup_hash(EMPTY_SHA256, method="SHA256")}
    assert ids == {"kb:File-new"}


def test_index_rebuild_is_cached_and_lookup_is_cheap() -> None:
    graph = CASEGraph()
    for i in range(80):
        _hashed_file(
            graph,
            file_id=f"kb:File-{i}",
            file_name=f"{i}.bin",
            hashes=[("SHA256", f"{i:064x}")],
        )

    start = time.perf_counter()
    first = graph.lookup_hash(f"{0:064x}", method="SHA256")
    first_elapsed = time.perf_counter() - start
    cached = graph._content_hash_index
    assert cached is not None
    assert first[0]["id"] == "kb:File-0"

    start = time.perf_counter()
    for i in range(80):
        hits = graph.lookup_hash(f"{i:064x}", method="SHA256")
        assert hits[0]["id"] == f"kb:File-{i}"
    cached_elapsed = time.perf_counter() - start
    assert graph._content_hash_index is cached
    assert cached_elapsed < 0.25
    assert first_elapsed < 1.0


def test_index_and_docs_are_public_safe() -> None:
    blob = INDEX_PATH.read_text(encoding="utf-8").lower()
    blob += "\n" + DOC_PATH.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in blob, f"hash index/docs contain forbidden substring {needle!r}"
    doc = DOC_PATH.read_text(encoding="utf-8").lower()
    assert "does not classify" in doc
    assert "does not label media" in doc
    payload = json.dumps(CASEGraph().index_content_hashes())
    assert payload == "{}"
