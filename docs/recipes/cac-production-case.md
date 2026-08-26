# CSAM Production and Manufacturing Cases

> See [Recipe Index](INDEX.md) for all recipes.

Model hands-on abuse and offender-produced CSAM cases including production environments, equipment, and produced-media artifacts using CAC production module classes.

When the source is a **federal court filing** (indictment, complaint) alleging production/possession/transport with enumerated devices and forfeiture, also follow [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) for legal relationship completeness.

## Scope

**Layer 2 — Behavioral / offense type** with strong **Layer 1 evidence** (images, video, devices, locations).

## Key classes

| Class | Role |
|---|---|
| `cacontology-production:ProductionOffense` | Overarching production conduct event |
| `cacontology-production:ProducedImage` / `ProducedVideo` | Offender-produced media (multi-typed observables) |
| `cacontology-production:ProductionLocation` / `ControlledEnvironment` | Location/setup where production occurred |
| `cacontology-production:MobileRecordingDevice` / `ProductionEquipment` | Cameras and phones used to produce material |
| `cacontology-production:ProductionVictim` | Victim role in the production offense |
| `cacontology-forensics:ForensicAcquisitionAction` | Evidence collection from production site |
| `cacontology:CSAMIncident` | Conduct event when modeled at incident level |
| `cacontology-asset-forfeiture:AssetForfeitureAction` | Device/proceeds forfeiture when alleged in filings |

## Canonical pattern

```
cacontology-production:ProductionOffense
  ├── cacontology-production:involvesVictim ──▶ ProductionVictim
  ├── cacontology-production:producedAt ──▶ ProductionLocation
  ├── cacontology-production:usesEquipment ──▶ MobileRecordingDevice
  └── cacontology-production:produces ──▶ ProducedImage / ProducedVideo
        └── uco-core:hasFacet ──▶ ContentDataFacet (hashes required)

AssetForfeitureAction
  ├── cacontology-asset-forfeiture:targetedAsset ──▶ each enumerated MobileRecordingDevice
  └── cacontology-asset-forfeiture:relatedCriminalCharges ──▶ FederalCharge nodes
```

## Modeling rules

- Multi-type produced media as `ObservableObject` + `ProducedImage`/`ProducedVideo`.
- Physical equipment → `MobileRecordingDevice` with `deviceBrand` and `deviceModel` when known.
- Link conduct to equipment with `cacontology-production:usesEquipment` on `ProductionOffense`. If the source only supports a generic `CSAMIncident`, use registered `Related_To` and explain the equipment basis in `uco-core:description`.
- When forfeiture is alleged, link **each named device** via `targetedAsset` — not only a generic aggregate asset stub.
- Add `relatedCriminalCharges` on `AssetForfeitureAction` linking to supporting `FederalCharge` nodes (CAC SHACL requires this).
- Always pair produced artifacts with forensic acquisition when post-seizure context exists — see [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md).
- For federal indictment graphs, apply the full checklist in [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-production": "https://cacontology.projectvic.org/production#",
    "cacontology-asset-forfeiture": "https://cacontology.projectvic.org/asset-forfeiture#",
})

device = graph.add_node("kb:device-1", [
    "uco-observable:ObservableObject",
    "cacontology-production:MobileRecordingDevice",
], {
    "uco-core:name": "Samsung Galaxy S21 Ultra",
    "cacontology-production:deviceBrand": "Samsung",
    "cacontology-production:deviceModel": "Galaxy S21 Ultra",
})

production = graph.add_node("kb:production-1", "cacontology-production:ProductionOffense", {
    "uco-core:name": "Alleged CSAM production",
    "cacontology-production:usesEquipment": {"@id": "kb:device-1"},
})

graph.write("production-case.jsonld")
```

## Validation

```bash
validate_graph("production-case.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — federal indictment relationship wiring
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md)
- [exif-data.md](exif-data.md)
- [device.md](device.md)
