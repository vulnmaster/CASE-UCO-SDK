<!-- Change Proposal: Structured PhotoDNA / perceptual-hash Facet -->
<!-- Target repository: UCO -->
<!-- Target release: 1.6.0 (or next develop) -->
<!-- Drafted from the CASE/UCO SDK Topology Framework; does not alter core OWL in this fork -->

# Target release

**Target**: UCO 1.6.0 (committee may reassign to the current `develop` line)

This is a backward-compatible addition: one new Facet subclass of
`uco-core:Facet` plus a small set of properties. Existing graphs that
record PhotoDNA as extra `types:Hash` entries remain valid.

# Background

ICAC and ESP hash-matching workflows need to record **perceptual** hashes
(Microsoft PhotoDNA / PDNA, and similar robust image hashes) next to
cryptographic hashes (SHA-256) on the same media object. Today the
CASE/UCO SDK HashIntelligence profile — used by this fork's
`model_csam_evidence` helper — records PhotoDNA as:

- a `types:Hash` with `hashMethod="PhotoDNA"` (or `"PDNA"`) on
  `ContentDataFacet.hash`
- an `InvestigativeAction` whose `instrument` is a `uco-tool:Tool`
  named PhotoDNA

That interim pattern is **correct and court-defensible** for the digest
bytes. It is **not** enough when a lab must also record:

- which PhotoDNA **version / coefficient set** produced the digest
- the **match distance** and **threshold** against a VICS or NCMEC catalog
- whether the digest is a **hash** or a **match result**
- the **catalog identifier** (VICS Media ID, NCMEC hash set name) without
  stuffing JSON into `uco-core:description`

`HashNameVocab` is an open vocabulary of *algorithm names*. PhotoDNA is
not just another algorithm name: it is a licensed perceptual-hash
*service* with versioned coefficients, a match distance, and a catalog
context. Crowding those facts onto `types:Hash` either invents
undeclared properties (fails strict concept coverage) or hides them in
free text (fails queryability).

**What we achieve for whom:** child-protection and ICAC teams get a
queryable, SHACL-valid way to say "this RasterPicture has PhotoDNA digest
X, computed by tool version Y, matching catalog record Z at distance D"
without inventing per-vendor extensions. That matters because hash
intelligence is how known-victim and known-offender media are correlated
across agencies — including air-gapped labs that load a local VICS
export.

## Related proposals and current interim pattern

- **Interim pattern in this SDK** — `docs/recipes/vics-hash-intelligence.md`,
  `topology/profiles/HashIntelligence.json`,
  `topology/mappings/vics.json`, and
  `model_csam_evidence` / `InvestigationBuilder.add_csam_evidence`.
- **BLAKE3 vocabulary addition** — `change_proposals/add-blake3-to-hashnamevocab.md`
  (UCO HashNameVocab). Complementary: BLAKE3 is a cryptographic
  algorithm name; PhotoDNA is a perceptual-hash *characterization*.
- **CAC forensics** — `ContentHashingTool` / `EvidenceVerificationAction`
  remain the CAC-side Action/Tool types. This proposal is a UCO Facet so
  non-CAC CASE/UCO producers can use it too.

# Requirements

## Requirement 1: Add `observable:PerceptualHashFacet`

A new `owl:Class` / `sh:NodeShape` targeting
`https://ontology.unifiedcyberontology.org/uco/observable/PerceptualHashFacet`,
subclass of `uco-core:Facet`. Attach via `uco-core:hasFacet` on the same
`ObservableObject` / `RasterPicture` that already carries `FileFacet` and
`ContentDataFacet`.

Do **not** replace `ContentDataFacet.hash`. Cryptographic hashes stay
there. The new Facet carries perceptual-hash *characterization*.

## Requirement 2: Properties

| Property | Type | Card. | Purpose |
|---|---|---|---|
| `observable:perceptualHashMethod` | `xsd:string` (open vocab; suggested members `PhotoDNA`, `PDNA`, `pHash`, `dHash`) | 1 | Which family |
| `observable:perceptualHashValue` | `xsd:hexBinary` or `xsd:string` | 1 | The digest / coefficient payload |
| `observable:perceptualHashVersion` | `xsd:string` | 0..1 | Tool / coefficient-set version |
| `observable:matchDistance` | `xsd:decimal` | 0..1 | Distance to catalog hit |
| `observable:matchThreshold` | `xsd:decimal` | 0..1 | Threshold used |
| `observable:catalogIdentifier` | `xsd:string` | 0..1 | VICS / NCMEC / local catalog id |
| `observable:hash` | `types:Hash` | 0..* | Optional link to the same digest also recorded as `types:Hash` |

## Requirement 3: Suggested ownership

- **UCO Observable** owns the Facet (it characterizes cyber-observable
  media, not a CAC-only concept).
- CAC may later add a thin subclass or recommended Action pairing
  (`ContentHashingTool`) in the forensics module. That is a separate CAC
  proposal.

# Risk / Benefit analysis

## Benefits

- Queryable match metadata for VICS/NCMEC hash intelligence.
- Stops producers stuffing match JSON into `description`.
- Leaves existing HashIntelligence graphs valid.
- Aligns with the Facet duck-typing pattern (one host, many Facets).

## Risks

- PhotoDNA is a licensed technology. The Facet records *results*, not
  the algorithm. The proposal must not require shipping PhotoDNA
  coefficients or a network client (air-gap constraint).
- Vocabulary members for `perceptualHashMethod` should be an *open*
  list so labs can record `pHash` without another proposal.
- Dual recording (`ContentDataFacet.hash` + Facet) could drift. SHACL
  should not require both; the SDK HashIntelligence profile will
  recommend both until producers migrate.

# Competencies demonstrated

## Scenario

An ICAC lab hashes a seized JPEG with SHA-256 and PhotoDNA, then matches
the PhotoDNA digest against a local VICS export. After this change, the
graph records cryptographic integrity on `ContentDataFacet` and the
PhotoDNA characterization + catalog hit on `PerceptualHashFacet`.

See `photodna-perceptual-hash-facet.jsonld` (after) and the "before"
block below.

### Before (current interim pattern — keep working)

```json
"uco-observable:hash": [
  { "uco-types:hashMethod": "SHA256", "uco-types:hashValue": { "@type": "xsd:hexBinary", "@value": "aa" } },
  { "uco-types:hashMethod": "PhotoDNA", "uco-types:hashValue": { "@type": "xsd:hexBinary", "@value": "bb" } }
]
```

plus `InvestigativeAction` / `Tool` name PhotoDNA.

### After (proposed)

Same SHA-256 Hash on `ContentDataFacet`, plus:

```json
{
  "@type": "uco-observable:PerceptualHashFacet",
  "uco-observable:perceptualHashMethod": "PhotoDNA",
  "uco-observable:perceptualHashValue": { "@type": "xsd:hexBinary", "@value": "bb" },
  "uco-observable:perceptualHashVersion": "2.0",
  "uco-observable:matchDistance": 0.0,
  "uco-observable:catalogIdentifier": "vics:media-123"
}
```

# Solution suggestion

Add `ontology/uco/observable/observable.ttl` class + SHACL as sketched in
`photodna-perceptual-hash-facet.ttl`. No existing shapes are narrowed.

# Impact on this SDK (when adopted)

| Surface | Change |
|---|---|
| Generator | Emits `PerceptualHashFacet` like any other Facet |
| `HashIntelligence` profile | Adds the Facet to the RasterPicture recommended set |
| `model_csam_evidence` | Optionally attaches the Facet when version/catalog/distance are supplied |
| `InvestigationBuilder` | Same optional kwargs; critique warns if PhotoDNA Hash is present without the Facet *after* adoption |
| Recipes | `docs/recipes/vics-hash-intelligence.md` gains an "after adoption" section |
| This proposal | Does **not** land the class in this fork's core OWL |

# Suggested SPARQL

See `photodna-perceptual-hash-facet.sparql`.
