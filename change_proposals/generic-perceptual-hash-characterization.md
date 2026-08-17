<!-- Change Proposal: Generic perceptual-hash characterization on types:Hash -->
<!-- Target repository: UCO -->
<!-- Target release: 1.6.0 -->

# Target release

**Target**: UCO 1.6.0

This is a backward-compatible, optional-property addition to `types:Hash`.
It does not invent a new Hash subclass, does not add proprietary algorithm
names to `HashNameVocab`, and does not alter existing graphs.

# Background

Investigators already record both cryptographic and similarity hashes as
`types:Hash` on `ContentDataFacet`. Method and value exist today
(`hashMethod`, `hashValue`). What is missing at the UCO layer is a
**public version string** so two hashes with the same method name can be
compared only when they were produced by the same published version of
that method.

The Crimes Against Children Ontology already has domain subclasses of
`types:Hash` (`cacontology-detection:PerceptualHash` and a more specific
licensed-algorithm subclass). Those terms should remain CAC-domain
specializations. UCO should stay generic: method, value, public version,
and ordinary action/tool provenance.

Until this lands, the SDK interim pattern remains `types:Hash` plus an
`InvestigativeAction` / `Tool` pair. This proposal does **not** change
vendored OWL in the SDK.

# Requirements

## Requirement 1: Optional `types:hashVersion` on `types:Hash`

Add an optional datatype property:

- IRI: `https://ontology.unifiedcyberontology.org/uco/types/hashVersion`
- Domain: `types:Hash`
- Range: `xsd:string`
- Cardinality: 0..1

The value is the **public** version identifier published by the tool or
library that computed the hash (for example `0.9.6`). It is not an
algorithm specification and not a catalog schema.

## Requirement 2: Provenance stays on Action / Tool

Do not add a parallel provenance property on `types:Hash`. Which tool
computed the hash, against which input, is already modeled by
`uco-tool:Tool` and `case-investigation:InvestigativeAction` (`instrument`,
`object`, `result`). This proposal only adds the version string that those
actions cannot attach to the hash node itself.

## Requirement 3: Keep `HashNameVocab` open; do not add proprietary names

`hashMethod` remains an open vocabulary. This proposal does not add
product-internal or licensed algorithm names to `HashNameVocab`. Domain
ontologies may continue to subclass `types:Hash` where they need tighter
local constraints.

## Requirement 4: Reconcile with existing CAC terms

CAC `PerceptualHash` already subclasses `types:Hash` and carries
`hashAlgorithm` / `perceptualHashValue`. After Requirement 1:

- UCO `hashMethod` / `hashValue` / `hashVersion` are the generic carriers
- CAC properties remain valid domain specializations and should be
  documented as aligning with, not replacing, the UCO triple
- CAC match-result classes stay in CAC; UCO does not grow a match-score
  class in this change

# Risk / Benefit analysis

## Benefits

- Two hashes with the same method name become comparable only when their
  public versions match.
- Domain ontologies keep their specializations; UCO does not absorb
  licensed catalog concepts.
- Existing `types:Hash` graphs remain valid (`hashVersion` is optional).

## Risks

- Implementations that already stuffed a version into `hashMethod`
  (for example `PHASH-0.9.6`) will need a one-time mapping note. The
  submitter is unaware of other risks.

# Competencies demonstrated

## Competency 1

An examiner records a published perceptual hash (`pHash`, version
`0.9.6`) and a SHA-256 integrity hash on the same raster file. A later
reviewer must list only the perceptual hashes that share that public
version.

### Competency Question 1.1

Which `types:Hash` nodes on `kb:file-1` have `hashMethod` `PHASH` and
`hashVersion` `0.9.6`?

#### Result 1.1

`kb:hash-phash-1` only.

### Competency Question 1.2

Which tool, via an investigative action, produced `kb:hash-phash-1`?

#### Result 1.2

`kb:tool-1` (`name` = `open-source pHash library`), through
`kb:action-1`.

# Solution

See `generic-perceptual-hash-characterization.ttl` (proposed T-Box only)
and `generic-perceptual-hash-characterization.jsonld` (synthetic
example). The example uses the public SHA-256 of the empty file and a
placeholder perceptual digest. It does not contain case data.

# Review and implementation notes

- Does not change SDK-vendored `ontology/UCO` in this repository.
- Does not classify content.
- Does not document licensed catalog schemas or product-internal hash
  algorithms.
- Ready to be copied into a UCO issue when the committee wants it.
