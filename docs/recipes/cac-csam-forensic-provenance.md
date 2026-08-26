# CSAM Forensic Provenance and Victim Identification

> See [Recipe Index](INDEX.md) for all recipes.

Model CSAM acquisition, verification, hashing, correlation analysis, and victim identification workflows using CAC forensics module classes on core CASE/UCO observable types.

## Scope

**Layer 1 — Observable evidence** with forensic-process semantics. Pairs with [ai-analysis-pipeline.md](ai-analysis-pipeline.md) for ML-assisted detection.

## Key classes

| Class | Role |
|---|---|
| `ForensicAcquisitionAction` | Evidence acquisition from device or storage |
| `ChainOfCustodyAction` | Per custody-transfer event |
| `EvidenceVerificationAction` | Hash verification step |
| `MetadataCorrelation` / `TemporalPatternAnalysis` / `GeospatialCorrelation` | Analysis result types |
| `CrossPlatformCorrelation` / `BehavioralFingerprinting` | Cross-source linkage |
| `VictimIdentificationProcess` | Identification workflow |
| `cacontology-detection:ContentHashingTool` / `DatabaseMatchAction` | Tool and hash-database comparison action |
| `RasterPicture` + `FileFacet` + `ContentDataFacet` | CSAM image artifacts |
| `OnlinePurchase` | CSAM or contraband purchasing operations (press-release context) |

## CSAM purchasing operations (press releases)

When the source describes an **online child sex abuse material purchasing operation** without device forensic detail, model procurement context with `cacontology-physical-evidence:OnlinePurchase` and pair with [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md) for the law-enforcement workflow.

- Set **`uco-action:performer`** on `OnlinePurchase` to the suspect `Person`.
- Add `cacontology-physical-evidence:hasProcurementBeginPoint` when the narrative gives a start date.
- Link procurement to the investigation and evidence-development action with registered `Related_To` relationships; explain the investigative basis in `uco-core:description`.
- `cacontology-physical-evidence:OnlinePurchase` is the correct CAC class (gUFO procurement **Event** under the physical-evidence module — not a UCO observable purchase).

Add full forensic provenance ([chain-of-custody](chain-of-custody.md), hashes, `ForensicAcquisitionAction`) only when device evidence is available.

## Canonical pattern

```
ForensicAcquisitionAction
  └── uco-action:result ──▶ ChainOfCustodyAction (per transfer)
        └── uco-action:result ──▶ EvidenceVerificationAction
              └── uco-action:result ──▶ VictimIdentificationProcess
                    └── Related_To ──▶ RasterPicture (description: image used for victim identification; SHA-256 / PhotoDNA hashes)
```

## Modeling rules

- **Never merge** acquisition, verification, and analysis into one action — each needs its own tool, operator, and timestamp.
- **Always include hashes** on CSAM artifacts via `ContentDataFacet`.
- Store correlation findings in the matching CAC correlation class, not only in `uco-core:description`.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-forensics": "https://cacontology.projectvic.org/forensics#",
})
acq = graph.add_node("kb:acq-1", "cacontology-forensics:ForensicAcquisitionAction", {
    "uco-core:name": "Acquisition of seized device",
})
graph.write("csam-forensics.jsonld")
```

## Validation

```bash
validate_graph("csam-forensics.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)

- [ai-analysis-pipeline.md](ai-analysis-pipeline.md)
- [chain-of-custody.md](chain-of-custody.md)
- [exif-data.md](exif-data.md)
