# Composition Profiles

Versioned JSON documents that help an investigator choose **existing**
CASE/UCO/CAC modules and Facet bundles for a common workflow.

**Profiles are investigator guidance, not ontology truth.** They do not
add OWL classes, change SHACL, or alter public constructors. Validation
is still SHACL plus concept coverage. The ontology remains the source of
truth.

Canonical documents live in this directory and are checked against
[`profile.schema.json`](profile.schema.json). Load them from a repository
checkout with `case_uco.profiles.list_profiles` / `get_profile`, or point
`CASE_UCO_PROFILES_DIR` at a directory of profile JSON files.

| Id | When to use it |
|---|---|
| `MinimalForensics` | File listing → hashed observables + one tool-backed action |
| `AirGappedFieldTriage` | Same, plus offline / laptop-scale graph discipline |
| `HashIntelligence` | Cryptographic (and optional perceptual) hashes + match results |
| `ToolMapping` | Versioned tools, ConfiguredTool, SOLVE-IT methods |
| `LegalProcess` | Charges, pleas, sentences, docket |
| `FullCACLifecycle` | Hotline → conduct → media provenance → rescue → court |
| `CrossOntology` | CASE/UCO + CAC + legal/crypto + one upper profile |

See [docs/COMPOSITION_PROFILES.md](../../docs/COMPOSITION_PROFILES.md).
