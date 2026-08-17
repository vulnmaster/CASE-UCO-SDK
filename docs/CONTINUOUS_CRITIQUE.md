# Continuous Critique Rules

A thin construction-time wrapper around the **existing** MCP critic.

It does not add a second rule engine. It serializes a `CASEGraph`, loads
the same canonical view used by `analyze_artifact`, and runs the
published `CRIT-H-*` heuristics. Findings keep the critic's stable
`finding_id` values. The critic's `recommended_change` is exposed as
`repair_hint`.

## Why it exists

Investigators and builders need the same deterministic findings during
graph construction that the MCP critic already emits in a review
session. Duplicating those rules in `python/case_uco/critique/` would
drift. This wrapper calls the critic in-process.

## What this is not

- Not a new critic, session loop, or scorecard.
- Not a duplicate of `CRIT-H-*` / `CRIT-S-*` / `CRIT-C-*`.
- Not a classifier. It does not classify content or inspect file bytes.
- Not licensed catalog schemas or product-internal hash algorithms.
- Not a workflow engine, adapter, hash index, or 2.x construction runtime.
- Not a C# / Java / Rust port.

## Usage

```python
from case_uco.case.investigation import Investigation
from case_uco.continuous_critique import critique_graph
from case_uco.graph import CASEGraph

graph = CASEGraph()
graph.create(Investigation, name="Case 1", id="kb:Investigation-1")

findings = critique_graph(graph)
# [{'finding_id': 'CRIT-...', 'rule_id': 'CRIT-H-INV-NO-OBJECT',
#   'repair_hint': '...', ...}]
```

Fail-closed behavior:

- Empty or oversize JSON-LD is refused.
- A graph the existing critic cannot use for heuristics is refused.
- If `mcp_server/critic` cannot be imported, `critique_graph` raises
  `ContinuousCritiqueUnavailable` instead of inventing local rules.

The wrapper is offline. It does not write the graph to the workspace
and does not open a network resource.

## Compatibility

Additive 1.x Python helper. Existing MCP critic sessions, schemas, and
rule IDs are unchanged. C# / Java / Rust graphs do not gain this helper
in this change.
