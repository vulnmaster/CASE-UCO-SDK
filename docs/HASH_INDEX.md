# Method-Aware Content Hash Index

Python lookup of content hashes already recorded on a `CASEGraph`, keyed by
normalized `(hashMethod, hashValue)`.

This is a graph index. It does not classify content and it is not a hash
computer. Callers supply hashes; the index only finds the nodes that
already carry them.

## Why it exists

Investigators often ask “which file already has this SHA-256?” The same
digest string can appear under more than one method. A digest-only map
collides those rows. This index stores the composite key.

The cache is rebuilt on demand and dropped on every mutation or load so
lookups never return a stale hit after `create`, `add_property`,
`set_property`, `upsert_node`, or `load`.

## What this is not

- Not new ontology terms, SHACL shapes, or vocabulary.
- Not a classifier. The index does not label media as CSAM or any other
  category.
- Not licensed catalog schemas or product-internal hash algorithms.
- Not a workflow engine, critique engine, adapter, or 2.x construction
  runtime.
- Not a C# / Java / Rust port. Those can be a later, separate 1.x PR if
  this Python surface is accepted.

## Usage

```python
from case_uco.graph import CASEGraph
from case_uco.uco.observable import ContentDataFacet, FileFacet, ObservableObject
from case_uco.uco.types import Hash

graph = CASEGraph()
empty = "e3b0c44298fc1c149afbf4c8996fb92402706899c32911cf29121339aa1a904b"
graph.create(
    ObservableObject,
    id="kb:File-empty",
    has_facet=[
        FileFacet(file_name=["empty.bin"]),
        ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value=empty)]),
    ],
)

graph.lookup_hash(empty, method="sha256")
# [{'id': 'kb:File-empty', 'method': 'SHA256', 'digest': 'e3b0c442...'}]

graph.index_content_hashes()["SHA256"][empty]
```

Normalization:

- method: trim, collapse internal whitespace, upper-case (`sha256` → `SHA256`)
- digest: strip whitespace, lower-case, drop a leading `0x`

`lookup_hash(digest)` without `method` returns every method that recorded
that digest. `lookup_hash(digest, method=...)` uses only the composite key.

The index walks `uco-observable:hash` and `uco-observable:hashes` (and the
unprefixed aliases) including nested Facets. A `{"@id": ...}` reference to
a standalone `types:Hash` node is resolved against the graph.

Fixtures and examples in this document use the public SHA-256 of the empty
file. Do not commit case data.

## Compatibility

Additive 1.x Python API. Existing constructors, validation, and generated
bindings are unchanged. C# / Java / Rust graphs do not gain these methods
in this change.
