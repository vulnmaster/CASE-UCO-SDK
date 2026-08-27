# Starter Kit: Forensic Tool Run with Provenance

> See [Recipe Index](INDEX.md) for all recipes.

Map a forensic tool execution into a CASE/UCO graph with full provenance — linking the tool, its action, input evidence, and output artifacts.

## Source Input Shape

A tool execution log or report summary:

```yaml
tool: Autopsy
version: 4.21.0
action: Hash verification of disk image
started: 2025-06-20T08:00:00Z
ended: 2025-06-20T08:47:00Z
input: evidence.E01 (SHA-256: a1b2c3d4...)
output: hash-report.txt (SHA-256: f9e8d7c6...)
exhibit: EX-2025-042
```

## Modeling Choices

| Concept | CASE/UCO Class | Why |
|---|---|---|
| Forensic software | `Tool` | Identifies the tool by name, version, and type |
| The action performed | `InvestigativeAction` | Connects tool (`instrument`), input (`object`), output (`result`), and timestamps |
| Input evidence | `ObservableObject` + `FileFacet` + `ContentDataFacet` | The artifact the tool operated on |
| Output artifact | `ObservableObject` + `FileFacet` + `ContentDataFacet` | What the tool produced |
| Provenance tracking | `ProvenanceRecord` | Groups the action and its artifacts under an exhibit number for chain-of-custody traceability |

## Anti-Patterns

- **Not linking action to tool.** An `InvestigativeAction` without `instrument` loses the record of which tool produced the results. Always set `instrument=[tool]`.
- **Missing input/output relationships.** The action's `object` field holds inputs; `result` holds outputs. Omitting either breaks the provenance chain and makes the graph unqueryable.
- **Forgetting ProvenanceRecord.** Without a `ProvenanceRecord`, there is no exhibit number or formal grouping to tie the action to a chain-of-custody workflow.
- **Detached Investigation.** An `Investigation` should reference its components via `object` so the graph is connected, not a set of floating nodes.

## Complete Code

```python
from datetime import datetime
from case_uco import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash
from case_uco.case.investigation import (
    Investigation, InvestigativeAction, ProvenanceRecord,
)
from case_uco.uco.observable import (
    ObservableObject, FileFacet, ContentDataFacet,
)

graph = CASEGraph()

tool = graph.create(Tool,
    name="Autopsy",
    version="4.21.0",
    tool_type="Forensic Analysis",
)

input_image = graph.create(ObservableObject,
    has_facet=[
        FileFacet(file_name="evidence.E01", size_in_bytes=53687091200),
        ContentDataFacet(
            hash=[Hash(hash_method="SHA256",
                        hash_value="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")],
        ),
    ],
)

output_report = graph.create(ObservableObject,
    has_facet=[
        FileFacet(file_name="hash-report.txt", size_in_bytes=2048),
        ContentDataFacet(
            hash=[Hash(hash_method="SHA256",
                        hash_value="f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4")],
        ),
    ],
)

action = graph.create(InvestigativeAction,
    name="Hash verification of disk image",
    description=["Verified SHA-256 hash of evidence.E01 using Autopsy"],
    instrument=[tool],
    object=[input_image],
    result=[output_report],
    start_time=datetime(2025, 6, 20, 8, 0, 0),
    end_time=datetime(2025, 6, 20, 8, 47, 0),
)

provenance = graph.create(ProvenanceRecord,
    description=["Provenance record for evidence.E01 hash verification"],
    exhibit_number="EX-2025-042",
    object=[action, input_image, output_report],
)

investigation = graph.create(Investigation,
    name="Case 2025-DFIR-019",
    description=["Digital forensics investigation — workstation compromise"],
    object=[tool, input_image, output_report, action, provenance],
)

graph.write("tool-run.jsonld")
```

## Expected JSON-LD Output

```json
{
    "@context": { "...": "..." },
    "@graph": [
        {
            "@id": "kb:Tool-...", "@type": "uco-tool:Tool",
            "uco-core:name": "Autopsy", "uco-tool:version": "4.21.0"
        },
        {
            "@id": "kb:ObservableObject-...",
            "uco-core:hasFacet": [
                { "@type": "uco-observable:FileFacet", "uco-observable:fileName": "evidence.E01" },
                {
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [{
                        "@type": "uco-types:Hash", "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": { "@type": "xsd:hexBinary", "@value": "a1b2c3d4..." }
                    }]
                }
            ]
        },
        {
            "@id": "kb:InvestigativeAction-...",
            "@type": "case-investigation:InvestigativeAction",
            "uco-action:instrument": [{ "@id": "kb:Tool-..." }],
            "uco-action:object": [{ "@id": "kb:ObservableObject-..." }],
            "uco-action:result": [{ "@id": "kb:ObservableObject-..." }],
            "uco-action:startTime": { "@type": "xsd:dateTime", "@value": "2025-06-20T08:00:00" }
        },
        {
            "@id": "kb:ProvenanceRecord-...",
            "@type": "case-investigation:ProvenanceRecord",
            "case-investigation:exhibitNumber": "EX-2025-042",
            "uco-core:object": [
                { "@id": "kb:InvestigativeAction-..." },
                { "@id": "kb:ObservableObject-..." }
            ]
        },
        {
            "@id": "kb:Investigation-...",
            "@type": "case-investigation:Investigation",
            "uco-core:name": "Case 2025-DFIR-019",
            "uco-core:object": ["... (references all graph objects)"]
        }
    ]
}
```

## Validation

```bash
case_validate --built-version case-1.4.0 tool-run.jsonld
```

When a lab export names the method, attach `solveit-core:usedTechnique`
and a real `ContentDataFacet` hash per
[technique-evidence-outcome.md](technique-evidence-outcome.md). Product
name alone is not enough to assert a DFT-* IRI.

## Related

- [forensic-tool.md](forensic-tool.md) — the base tool + action pattern
- [configured-tool.md](configured-tool.md) — tool configurations
- [chain-of-custody.md](chain-of-custody.md) — custody and provenance records
- [forensic-lifecycle.md](forensic-lifecycle.md) — placing runs into phases
- [technique-evidence-outcome.md](technique-evidence-outcome.md) — sourced method plus legal-outcome join
