# VICS / PhotoDNA Hash Intelligence

> See [Recipe Index](INDEX.md). Mapping stub: [topology/mappings/vics.json](../../topology/mappings/vics.json). Profile: `HashIntelligence`.

Project VIC VICS catalog records and PhotoDNA (or other perceptual) hashes become CASE/UCO observables. This recipe is a **mapping stub**: it does not ship a VICS network client. Air-gapped labs load a local catalog export.

## Modeling Choices

| VICS / hash concept | CASE/UCO | Notes |
|---|---|---|
| SHA-256 / MD5 | `ContentDataFacet.hash` + `Hash` | Required on every media item |
| PhotoDNA / PDNA | Additional `Hash` with `hashMethod=PhotoDNA` | Do not invent `PhotoDNAFacet` |
| Catalog match | `InvestigativeAction` + `Tool` (ContentHashingTool if CAC is loaded) + `ConfidenceFacet` or CAC `AssessmentResult` | Keep match metadata out of `description` JSON |
| Victim identifier | `PersonLikeEntity` + `Role` | Identifier is not the person |
| Series / category | `Relationship` `Member_Of` | |

## Anti-Patterns

- One Observable per hash algorithm. All hashes of one file hang off one `ContentDataFacet`.
- Storing PhotoDNA as a free-text `description`.
- Calling a network VICS API at investigation time.

## Helper

```python
from case_uco import CASEGraph, model_csam_evidence

graph = CASEGraph()
model_csam_evidence(
    graph,
    file_name="img.jpg",
    hashes=[("SHA256", "…"), ("PhotoDNA", "…")],
)
```

## Related

- [CSAM Forensic Provenance](cac-csam-forensic-provenance.md)
- [NCMEC CyberTip Reporting Workflow](cybertip-ncmec-workflow.md)
- [Starter Kit: Filesystem Report](starter-filesystem-report.md)
- [Composition Profiles](../COMPOSITION_PROFILES.md)
