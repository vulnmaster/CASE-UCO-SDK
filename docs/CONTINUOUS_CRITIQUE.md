# Continuous Critique Rules

A thin in-memory entry on the **existing** MCP critic.

It does not add a second rule engine. `critic.continuous.critique_jsonld`
loads the same canonical view used by `analyze_artifact` and runs the
published `CRIT-H-*` heuristics. Findings keep the critic's stable
`finding_id` values. The critic's `recommended_change` is exposed as
`repair_hint`.

## Why it exists

Callers that already have JSON-LD in memory need the same deterministic
findings the MCP critic emits in a review session, without writing a
temp file. Duplicating those rules outside `mcp_server/critic` would
drift. This entry calls `run_graph_heuristics` in-process.

## What this is not

- Not a new critic, session loop, or scorecard.
- Not a duplicate of `CRIT-H-*` / `CRIT-S-*` / `CRIT-C-*`.
- Not an SDK `CASEGraph` wrapper or `python/case_uco` public helper.
- Not a classifier. It does not classify content or inspect file bytes.
- Not licensed catalog schemas or product-internal hash algorithms.
- Not a workflow engine, adapter, hash index, or 2.x construction runtime.
- Not a C# / Java / Rust port.

## Usage

```python
from critic.continuous import critique_jsonld

document = {
    "@context": {
        "case-investigation": "https://ontology.caseontology.org/case/investigation/",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    },
    "@graph": [
        {
            "@id": "urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "@type": "case-investigation:Investigation",
            "uco-core:name": "Case 1",
        }
    ],
}

findings = critique_jsonld(document)
# [{'finding_id': 'CRIT-...', 'rule_id': 'CRIT-H-INV-NO-OBJECT',
#   'repair_hint': '...', ...}]
```

Fail-closed behavior:

- Empty or oversize JSON-LD is refused.
- A graph the existing critic cannot use for heuristics is refused.

The entry is offline. It does not write the graph to the workspace
and does not open a network resource. In-memory load uses
`load_canonical_jsonld_text`, the same size bound and offline
remote-context policy as file load.

## Compatibility

Additive 1.x critic helper. Existing MCP critic sessions, schemas, and
rule IDs are unchanged. Package versions stay on the 1.x line.
