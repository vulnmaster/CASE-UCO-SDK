# Bounded Offline Adapter Interface

A generic, air-gapped plugin boundary for **authorized local mappings**.

Adapters run against a local file and a `CASEGraph`. They do not open
sockets, do not classify content, and do not embed a licensed catalog
schema.

## Why it exists

Field workflows sometimes need to project an authorized local export
(JSON records the caller already holds) onto existing CASE/UCO
constructors. The SDK should refuse remote URIs, oversize inputs, and
any adapter that is not explicitly air-gapped — then stop.

## What this is not

- Not a licensed catalog client and not a product-internal hash
  algorithm.
- Not a classifier. It does not classify content or inspect media bytes
  beyond reading the caller-supplied record file.
- Not a licensed catalog mapping. Product-internal hash algorithms and
  vendor catalog schemas are out of scope.
- Not a workflow engine, critic, hash index, or 2.x construction runtime.
- Not a C# / Java / Rust port.

## Usage

```python
from pathlib import Path
from case_uco.graph import CASEGraph
from case_uco.offline_adapter import (
    AdapterBounds,
    apply_offline_adapter,
    get_adapter,
)

graph = CASEGraph()
apply_offline_adapter(
    "local-json-records",
    graph,
    Path("records.json"),
    bounds=AdapterBounds(max_bytes=1_000_000, max_rows=100, max_seconds=2.0),
)
```

`records.json` is a JSON array. Each object must have `file_name` and
`hashes` (a list of `[method, value]` pairs). The built-in adapter
attaches those values to `FileFacet` + `ContentDataFacet` using existing
constructors.

Callers who need a different local mapping implement `OfflineAdapter`
(`adapter_id`, `air_gapped=True`, `probe`, `apply`) and register it with
`register_adapter`. Non-air-gapped adapters are refused.

Fail-closed refusals:

- remote `http(s)` / `ftp` URIs
- missing source file
- source larger than `max_bytes`
- more than `max_rows` records
- apply time above `max_seconds`
- missing required record fields
- `air_gapped` is not true

Fixtures and examples use the public SHA-256 of the empty file. Do not
commit case data.

## Compatibility

Additive 1.x Python interface. Existing constructors, validation, and
generated bindings are unchanged.
