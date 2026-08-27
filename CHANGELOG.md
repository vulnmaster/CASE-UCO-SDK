# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.27.0] - 2026-08-27

Queryable press-release legal outcomes, full operational recipe
execution coverage, and a sourced technique → evidence → outcome join.

#### Press-release legal outcomes (#125)

- Extended `legalproc` with `PleaAgreement`, `PotentialPenalty`,
  `PretrialReleaseCondition`, `StateCharge`, `FederalCharge`,
  `StateJurisdiction`, `FederalJurisdiction`, and properties for
  `outcomeScope`, `sentenceKind`, `jurisdictionKind`, `victimFactStatus`,
  and source publication versus retrieval time.
- Fail-closed SHACL rejects bail/bond and statutory maxima typed as
  imposed sentences, mixed current/prior outcome scope, fabricated
  jurisdiction, and omitted victim facts recorded as a zero count.
- Rewrote `cac-legal-sentencing-outcomes.md` with a legal-stage decision
  table, CaseLinker remodeling guidance, and `legalproc:Plea` /
  `legalproc:PleaAgreement` as the plea source of truth. Updated related
  legal and ICAC recipes. Recipe lint rejects state-specific charge
  subclasses outside anti-pattern sections.
- Added ten press-release exemplars with SPARQL competency tests for
  state-only, federal-only, dual jurisdiction, charged-only, current
  conviction, prior history, imposed sentence, and omitted victim facts.
- Regenerated `legalproc` language bindings and `_registry.json` so the
  new classes resolve through MCP search and typed packages.

#### Technique, evidence, and legal-outcome join (#126)

- Added `docs/recipes/technique-evidence-outcome.md` with a source-fidelity
  table (press / PACER / lab / CTI), a bounded hash-match CSV and UFED-style
  summary importer, and LE product → DFT-* suggestion profiles that stay
  off the graph until the source names the method.
- Lab-join exemplar records DFT-1050 and DFT-1020 with real SHA-256 hashes
  and an imposed `legalproc:Sentence`. PACER method-claim exemplar records
  a named Cellebrite tool without inventing `usedTechnique`.
- Recipe lint rejects empty `ContentDataFacet()` / JSON-LD ContentDataFacet
  objects without hash, size, MIME type, or payload outside Anti-patterns.
- Updated sentencing, PACER, SOLVE-IT, starter tool/mobile, CSAM
  provenance, CTI, and recipe-authoring guidance so ATT&CK stays offender
  method and SOLVE-IT stays examiner method.

#### Recipe execution coverage (#124)

- Every operational recipe now has schema-valid execution metadata.
  Dedicated builders remain for upper-ontology and sysdiagnose recipes;
  remaining recipes use compact catalog fragments.
- `run_recipe_examples.py --all` reports operational coverage and fails
  if a recipe is missing from the manifest. Candidate promotion continues
  to require the same gate. CI's recipe job now runs `--all --validate`
  so the coverage report is produced on every push.

#### CaseLinker ICAC remodel patterns (#128–#131)

- Added `docs/recipes/caselinker-icac-remodel.md` and
  `mcp_server/tools/caselinker_icac_remodel.py` to remodel CaseLinker CAC
  graphs: `InvestigationTrigger` joins, share-safe known-series matches,
  `legalproc` dual-typed charges with `chargedWith`/`appliesTo`, commander
  phase begin/end clocks, generic `ICACtaskForce`, and a CaseLinker private
  vocab map that fails closed. Share-safe series `referenceURL` values
  serialize as `xsd:anyURI` (SHACL `DatatypeConstraintComponent`).
- Loaded `cacontology-us-ncmec.ttl` into the CAC validation subset so
  CyberTip trigger classes pass strict concept coverage.
- Exemplars and SPARQL competency queries live under
  `examples/caselinker-icac-remodel/`.

#### Criminal discovery and disclosure (#132)

- Extended `legalproc` 0.3.0 with `DisclosureObligation`,
  `DiscoveryProduction`, `SuppressionMotion`, and fail-closed SHACL that
  requires a source citation and evidence IRI. Brady cannot be inferred
  from unlabeled exam notes.
- Added `docs/recipes/legal-discovery-disclosure.md`.

Package versions bumped to **1.27.0**.

## [1.26.0] - 2026-08-26

Fail-closed ontology grounding for the operational recipe catalog, repair of
undeclared CASE/UCO/CAC terms and non-interoperable relationship labels, and a
reviewed Rust dependency lockfile update.

#### Recipe ontology grounding (#123)

- Audited all 79 operational recipes against vendored CASE/UCO, every
  operational extension manifest in full mode, the exact pinned
  upper-ontology registry, and `relationship_kinds.json`. Corrected fake or
  mis-namespaced claims including `SextortionScheme`, `HotlineIntake`,
  `MissingChildReport`, `ProductionCase`, `ExtraditionProcess`,
  `case-investigation:name`, `gufo:hasParticipant`, and
  `uco-observable:Facet`.
- Replaced unregistered relationship strings and diagram labels with declared
  direct properties or registered vocabulary values. Generic fallback edges
  now use `Related_To` with precise descriptions that preserve role,
  ownership, derivation, venue, custody, or evidentiary-basis semantics.
- Added `mcp_server/recipe_lint.py`, a repository-wide Markdown gate that
  checks CURIE existence, class/property RDF roles, class/property tables,
  embedded snippets, canonical diagram edges, and relationship literals. It
  reports narrow, reviewable exclusions for anti-patterns, proposed terms,
  wildcard notation, instance IDs, and controlled literals; malformed or
  unbounded directives fail closed.
- Integrated recipe lint into `make test`, `make test-mcp`, CI's MCP suite, and
  candidate promotion. Promotion rejects an invalid candidate before running
  its exemplar builder.
- Corrected canonical namespace examples in the fraud/crypto and change-
  proposal recipes, removed unregistered external chemical identifiers from
  operational guidance, and made every canonical diagram property namespace-
  explicit.
- Added regression coverage proving the gate rejects `SextortionScheme`,
  `used_platform`, `case-investigation:name`, `gufo:hasParticipant`,
  `uco-observable:Facet`, `Relates_To`, and prose-only custom labels such as
  `Basis_Of`, while classifying explicit anti-pattern and wildcard examples.

#### Recipe exemplar validation

- Repaired checkout import-path handling for recipe builders and graph
  validation so `case_uco` and MCP modules resolve consistently from a clean
  checkout and validation failures remain fail-closed.
- Made relationship-kind lint strict for executable exemplars, corrected the
  FOAF/ORG account-attribution exemplar to use registered `Related_To`, and
  added regression tests for conforming/nonconforming validation and
  unregistered relationship values.
- `run_recipe_examples.py --all --validate` now passes all 11 registered
  strict-concept exemplar entries.

#### Dependency maintenance

- Included Dependabot #122, updating the Rust `uuid` lockfile entry from
  1.24.1 to 1.25.0 after its full CI, dependency-review, and Rust security
  checks passed.

Package versions bumped to **1.26.0**.

## [1.25.0] - 2026-08-25

Remote SPARQL query and analysis for the MCP server, with CaseLinker as the
first reference endpoint and a security boundary suitable for agent-facing
network access.

#### Remote SPARQL MCP workflow (#120)

- Added `execute_sparql_query(query, endpoint_url?, timeout_seconds?)`, a
  generic SPARQL 1.1 Protocol client for SELECT, ASK, CONSTRUCT, and DESCRIBE.
  It uses CaseLinker's public CASE/UCO/CAC endpoint by default and accepts
  other standards-compliant endpoints.
- Results are normalized as SPARQL JSON bindings, ASK booleans, JSON-LD, or
  RDF text with stable request/response metadata, query digest, bounded safe
  summaries, and `content_trust: untrusted-external-sparql-results`. The full
  query and remote HTTP error bodies are not reflected in tool results.
- Added the `case-uco://sparql` MCP resource with the ontology-first query
  workflow, CaseLinker endpoint profile, named-graph/default-union behavior,
  safe starter queries, and privacy guidance.
- Added query and transport controls: local rejection of SPARQL Update and
  SERVICE, query/response/timeout caps, blocked redirects and URL credentials,
  public-HTTPS-by-default endpoint validation, DNS/private-address rejection,
  optional exact host allowlists, and fail-closed SPARQL egress under secure
  deployment profiles unless explicitly enabled.
- Added 35 focused offline tests plus an opt-in live CaseLinker smoke test,
  covering query forms and lexical edge cases, SSRF and
  secure-profile policies, request protocol, SELECT/ASK/CONSTRUCT response
  normalization, HTTP errors, response bounds, and MCP tool/resource wiring.
- Added `docs/SPARQL.md` with the query/analysis guide and a separate future
  validated graph-loading contract for Oxigraph and Fuseki. Query execution
  remains read-only; graph loading will require validation provenance,
  configured write targets, dry-run/commit separation, idempotency, named-
  graph ownership, and explicit overwrite authority.
- Documented CaseLinker's current endpoint contract and identified its current
  documentation posture: a README quick start, brief OpenAPI operation, and
  executable live tests. A dedicated upstream API guide is recommended for
  GET/POST encoding, content negotiation, response/error schemas, rate-limit
  headers, namespaces, examples, and corpus/version metadata.

#### Dependency maintenance

- Merged Dependabot #117, updating the Rust `uuid` lockfile entry from 1.24.0
  to 1.24.1 after the Rust tests, security audit, dependency review, and full
  CI matrix passed.
- Merged Dependabot #118, updating the test-only `Microsoft.NET.Test.Sdk`
  dependency from 18.8.1 to 18.9.0 after the C# tests and full CI matrix
  passed.
- Merged Dependabot #119, updating the test-only
  `xunit.runner.visualstudio` adapter from 3.1.5 to 4.0.0. The adapter remains
  compatible with this .NET 8/xUnit v2 test project, and the C# tests and full
  CI matrix passed on the update.

Package versions bumped to **1.25.0**.

## [1.24.0] - 2026-08-16

Alignment to the CASE and UCO 1.5.0 releases, a SHACL cardinality fix in the
generator, repair of the extension compatibility harness, bounded Apple
acquisition-package tooling, and published deployment-compute requirements.

#### Ontology alignment (CASE/UCO 1.5.0)

- `ontology/UCO` pinned to **1.5.0** (`7ebb395`) and `ontology/CASE` to
  **1.5.0** (`8073d5a`), together with CASE's nested `dependencies/UCO`
  gitlink. Supersedes dependabot #93 and #94, applied as a pair so the two
  ontologies stay on matching releases.
- UCO 1.5.0 adds the `core:UcoType` metaclass anchor (disjoint from
  `core:UcoThing`), `action:Technique`, `action:techniqueID`, and two SHACL
  shapes; it also repairs the `MessageTread`, `withing` and `Implemetation`
  typos. Only `rdfs:label` / `rdfs:comment` strings changed — the
  `observable:MessageThread` class IRI was always spelled correctly, so no
  binding, exemplar or instance data is affected. CASE 1.5.0 carries no
  ontology changes beyond version IRIs.
- **`case_validate` deliberately stays on `--built-version case-1.4.0`.**
  case-utils 0.17.0 is the newest PyPI release and bundles CASE only through
  1.4.0, so `case-1.5.0` is not a selectable target
  ([casework/CASE-Utilities-Python#182](https://github.com/casework/CASE-Utilities-Python/pull/182)
  is still open). Supplying the UCO 1.5.0 files through `--ontology-graph`
  is not a workaround: it puts two versions of one ontology series in the
  import closure and trips `uco-owl:versionIRI-multiversion-shape`.
- `extensions/attack-technique/` is now **superseded upstream but retained**.
  Its `core:UcoType` / `action:Technique` / `action:techniqueID` declarations
  are the same concepts in the same IRIs that UCO 1.5.0 ships, and were
  verified removable: against a real 1.5.0 closure the MITRE ATT&CK catalog
  reports `Conforms: True` with both the shim and its shapes deleted. It stays
  only because the pinned `case-1.4.0` closure has no `Technique`. Retirement
  condition recorded in the extension README and TTL header.
- `uco_compat` extended to `["1.4.0", "1.5.0"]` for `attack-technique`,
  `cryptoinv`, `drugs`, `legalproc`, `rico`, `toolcap` and `weapons`, each
  confirmed `Conforms: True` against the 1.5.0 closure rather than assumed
  from UCO's `owl:backwardCompatibleWith`.
- Regenerated the ontology reference, mapping guide, and four runtime
  registries from the complete pinned recursive checkout. They now expose
  2,933 core and extension classes across 79 modules, matching the sources
  used by the release workflow.

#### Generator

- Preserve `sh:maxCount` carried by range-less sibling shapes. UCO routinely
  splits a property across sibling `sh:property` shapes — one naming the
  `sh:datatype` with no bound, another carrying `sh:maxCount 1` with only
  `sh:nodeKind`. `_extract_property_from_shape` discards any shape lacking a
  `sh:class` or `sh:datatype`, so the bounding shape was dropped before its
  cardinality was read and the property was emitted as an unbounded
  collection. Cardinality is now accumulated per path independently of range
  extraction and merged conjunctively (max of `minCount`, min of `maxCount`).
- **Breaking for Java, C# and Rust consumers.** 54 Rust fields and their
  counterparts collapse from collections to scalars, including
  `AutonomousSystemFacet.regionalInternetRegistry`, `AccountFacet.accountType`
  and `ContactAddress.contactAddressScope`. Every change is list-to-scalar;
  nothing widens. These properties are single-valued in UCO 1.4.0 too, so this
  corrects long-standing generated output rather than tracking an ontology
  change. Python is unaffected at runtime.
- Regression test covers both the bounded and genuinely-unbounded cases.

#### Extension compatibility harness

- `make test-extension-compat` actually tested nothing branch-specific: it
  checked out `main`, `develop` and `develop-2.0.0` in the submodules but
  never passed their Turtle to `case_validate`, which fell back to its default
  bundled `case-1.4.0` closure and returned the same answer three times. It
  now validates with `--built-version none` against every module `.ttl` from
  the checked-out branch. Per-module enumeration is required because
  `ontology/*/master/*.ttl` are ~23-triple `owl:imports` stubs.
- This is also what makes 1.5.0 validation possible today, ahead of case-utils.

#### Code scanning

- Removed the unused `ul_record` / `ul_event` locals in
  `examples/sysdiagnose/build_ios_sysdiagnose_unified_logs.py`, clearing the
  last two open CodeQL alerts (`py/unused-local-variable` #527, #528).
- Resolved nine findings surfaced when CodeQL analyzed the new v1.24 code
  (#529–#537): benchmark temporary directories are securely randomized,
  Java service-provider overrides are explicit, Python cleanup no longer uses
  an empty exception handler, benchmark memory sampling avoids forced garbage
  collection, C# cache pruning uses an explicit filter, and streaming output
  paths are normalized before use.

#### Marking-safe partitioning (#79)

- Added matching marking/authorization boundary policies to all four SDKs.
  Partition plans fail closed by default; explicit home-reference and support
  graph modes preserve a reconstructable union without copying protected node
  content into an unauthorized partition.
- Added v2 manifests with dataset/partition hashes, effective scopes, safe
  manifest mode, routing/omission counts, validation-bundle identity, and
  declared RDF-union reconstruction. Python performs an RDF-isomorphism proof;
  native SDKs verify the exact JSON-LD assertion union.
- Added partition-set validation orchestration: self-contained partitions are
  validated independently, while referenced sets are reconstructed and
  validated together.

#### Bounded streaming writer (#80)

- Added frozen-context, incremental JSON-LD writers with a configurable
  per-node allocation cap in Python, C#, Java, and Rust. Unknown prefixes and
  oversized nodes fail before atomic destination replacement; induced-failure
  tests prove existing destination bytes survive.

#### Cross-language benchmark release gate (#81)

- Expanded C#, Java, and Rust from catalog-only timing to the same catalog,
  relationship-rich partition, deserialization roundtrip, and streaming-write
  workload families as Python, across 1K/10K/100K tiers.
- Added repeated samples, min/max/median/mean/stdev/p95 dispersion, workload
  memory metrics, process peak RSS, Python bundle/coverage/SHACL stages, and a
  consolidated machine-readable/Markdown release report.
- Every language now emits the same deterministic catalog fixture; the release
  gate parses all four as RDF and fails unless their graphs are isomorphic.
- Removed redundant fallback linear node scans after IRI-index misses in all
  four runtimes, eliminating quadratic construction exposed by the
  medium/large workloads. All supported mutation/load paths maintain the index.

#### Extension registry invalidation (#82)

- Added explicit extension registration/unregistration, deterministic
  Class-IRI conflict rejection, cache generations, and hit/miss metrics across
  the applicable runtimes. Python supports opt-in entry points, Java supports
  `ServiceLoader`, C# supports explicit assemblies/types, and Rust exposes an
  honest metadata registry rather than simulating runtime reflection.

#### Apple acquisition packaging (#99)

- Added fail-closed classification for full iOS `sysdiagnose_*` trees versus
  standalone FOSS `.logarchive` collections. Ambiguous and unsupported package
  layouts return typed errors instead of being mislabeled as sysdiagnose.
- Added `build_acquisition_package_graph` for bounded package-level CASE/UCO +
  SOLVE-IT JSON-LD. Binary `.tracev3` data and full decoder output remain
  external; CSV/JSONL event samples are capped at 1,000 records.
- Shareable mode normalizes paths, removes common device/person identifiers,
  omits or replaces message bodies, and returns safe counts/digests rather than
  source rows. Inventory walks, hashes, input lines, and output writes are
  bounded, package-base containment is enforced, and graph writes are atomic.
- Updated MCP routing and Apple recipes to distinguish acquisition shapes,
  retain timebase caveats, and require extension-aware SOLVE-IT validation.

#### Compute requirements (#100)

- Published the minimum baseline (4 CPU cores, 8 GB RAM, no GPU/VRAM, and
  20 GB application/database disk excluding evidence) in `README.md`,
  `docs/COMPUTE.md`, and machine-readable `catalog/compute.yaml`.
- Documented an 8-core/16 GB recommended tier and the 32–64 GB RAM range for
  large in-memory graphs; evidence storage remains separately sized.

#### Docs

- Change-proposal guidance no longer presents 1.5.0 as an upcoming target and
  now says to read the version off `develop` rather than assume it — after the
  1.5.0 release `develop` still carried `owl:versionIRI core:1.5.0`.
- `draft_change_proposal` defaults `target_release` to `1.6.0`; `1.5.0` is
  released and can no longer be proposed against.

Package versions bumped to **1.24.0**.

## [1.23.1] - 2026-07-28

CI version-consistency fix, native SOLVE-IT action serialization in
`case-uco-solveit` 0.2.0, a quality pass on the sysdiagnose exemplar, and four
draft UCO change proposals grounded in the DFRWS USA workshop corpus.

#### CI

- Fix the failing **Version Consistency Check** from the v1.23.0 push:
  `python/case_uco/__init__.py` (`__version__` still 1.22.4) and the
  `case-uco` entry in `rust/Cargo.lock` were missed by the 1.23.0 bump. All
  six checked sources now agree (verified locally with the workflow script).

#### case-uco-solveit 0.2.0

- `SolveitInvestigativeAction` serializes natively: explicit `jsonld_key`
  metadata emits `uco-action:*` keys (was `uco-core:*`), and new
  `used_technique` / `applied_mitigation` fields emit
  `solveit-core:usedTechnique` / `solveit-core:appliedMitigation` directly —
  no more post-creation `@type` retargeting in builders.
- `hasChanged` / `state` on all 85 observable dataclasses now serialize in
  the `uco-observable:` namespace; `_registry.json` updated.

#### Sysdiagnose exemplar (`examples/sysdiagnose/`)

- `euid` and tool-reported `activity_id` retained as `DictionaryEntry` values
  on each unified-log `Event`; `library` captured when present.
- Honest `eventRecordID` semantics (`excerpt-row-N`); dropped the
  `uco-observable:eventID` property, which does not exist in built CASE
  1.4.0 — `case_validate` is now 0 violations / **0 warnings**.
- Notari and iLEAPP parse steps typed `SolveitInvestigativeAction` with
  DFT-1066 / DFT-1076 links (Notari also carries the DFM-1027 dual-tool
  mitigation); empty `MobileDeviceFacet` removed and `DeviceFacet.model`
  asserts the real hardware identifier `iPhone12,1` from the stackshot
  `.ips` header.
- `unifiedlog_iterator_excerpt.sha256` now standard `sha256sum -c` format.
- `critic-review.json` refreshed on the new graph bytes (deterministic
  two-pass session; only the accepted `hash-status:not-published`
  medium findings remain open).

#### Recipes / MCP

- `ios-sysdiagnose.md`: real hardware model on `DeviceFacet`;
  `MobileDeviceFacet` only when IMEI/ESN/network evidence exists.
- `apple-unified-logs.md`: native `SolveitInvestigativeAction` pattern.
- `domain_index.py`: expanded keywords (`.ips`, `stackshot`, `timesync`,
  `boot_uuid`, `mach_continuous_time`, `activity_id`, ...) for both recipes.

#### Change proposals (drafts, not yet submitted upstream)

- Four corpus-grounded UCO proposals under `change_proposals/`, each with
  example JSON-LD, SPARQL competency queries, and a `proposed:` extension
  ontology, all passing `make test-proposal`: boot session + boot-relative
  time, `OperatingSystemLogRecordFacet`, cross-platform
  `ProcessThreadFacet`, and UNIX numeric `uid` / `euid` properties.

Package versions bumped to **1.23.1**.

## [1.23.0] - 2026-07-27

Apple sysdiagnose / Unified Logging recipes and a validated SOLVE-IT exemplar
grounded in DFRWS USA workshop corpus layout, plus recipe-execution coverage
for mobile-forensics builders.

#### Recipes / mobile forensics

- New recipes: [`ios-sysdiagnose.md`](docs/recipes/ios-sysdiagnose.md) and
  [`apple-unified-logs.md`](docs/recipes/apple-unified-logs.md) — model raw
  sysdiagnose packages (`AppleUnifiedLogArchive` + Wi-Fi / BatteryBDC) and
  parser outputs (`unifiedlog_iterator`, Notari, iLEAPP) as
  `EventRecord` / `Event` graphs with `SolveitInvestigativeAction`
  (DFT-1066 / DFT-1076 + mitigations).
- Validated exemplar + builder:
  `examples/sysdiagnose/ios-sysdiagnose-unified-logs.jsonld` (real iterator
  sample rows; timesync caveat; vocab relationship kinds only;
  `hash-status:not-published` when workshop bytes are not shipped).
- Registered in `docs/recipes/INDEX.md`, `RECIPE_INDEX`, investigation router
  (`device-mobile-forensics`), and
  [`recipe-execution.json`](docs/recipes/recipe-execution.json) mobile-forensics
  gate entries with `support_files`.
- Promotion provenance in `docs/recipes/promotion-log.json`; deterministic
  critic review artifact under `examples/sysdiagnose/critic-review.json`.

Package versions bumped to **1.23.0**.

## [1.22.4] - 2026-07-15

SDK hardening from the v1.22.1 CTI review: provenance-manifest integrity across
critic sessions, installed-wheel extension contract, tighter heuristics,
signature-aware serializer AST checks, TypedLiteral custom datatypes,
DarkWatchman release gates, controlled epistemic tags, and a pinned ATT&CK
STIX catalog synchronizer. Registry publication remains opt-in (**disabled**
for this tag).

#### Docs

- README status badges for CI, CodeQL, Rust Security, Upstream Freshness, and
  the latest GitHub Release (live from Actions / shields.io).

#### Security

- CodeQL `py/empty-except`: log and skip when optional epistemic-tags vocab
  cannot be read (`list_all_vocabs`).

#### Critic / provenance

- Bind `provenance_manifest_path` through resumable sessions (`SessionConfig`,
  pass rebuild, MCP tools).
- `ArtifactHashes.provenance_manifest_sha256` in artifact-set and
  `review_config_sha256`; JSON schemas updated.
- Schema-1.1 `artifacts[]` parsing; workspace-policy on every referenced path;
  exactly one `output_artifact` matching the graph under review; empty
  manifests fail closed.
- Heuristics **v1.3.3**: missing-hash medium only for `cti-report` /
  explicit hash tags; proxy-duplicate = Action object→result only; orphan
  BFS roots = Investigation / ProvenanceRecord / Bundle.
- `CRIT-S-PY-NONEXISTENT-API` checks `inspect.signature` (kwargs/arity).

#### Validation / packaging

- Document **external-bundle** contract: named extensions require
  `project_root` (or explicit ontology paths); wheel does not vendor
  `extensions/`.
- Tests for empty-root failure and DarkWatchman validate-with-`project_root`.

#### Typed literals

- `case_uco.TypedLiteral` + `LogicalPattern.patternExpression` as
  `pattern:PatternExpression`; generator emits `Union[str, TypedLiteral]`
  for custom RDF datatypes.

#### ATT&CK + epistemic vocabulary

- `make sync-attack` / `mcp_server/tools/sync_attack_catalog.py` regenerates
  `mitre-attack-catalog.ttl` from pinned Enterprise ATT&CK STIX (v19.1).
- Controlled epistemic-tag vocabulary:
  `docs/vocabularies/epistemic-tags.{md,json}`; exposed via MCP
  `list_all_vocabs`.

#### DarkWatchman exemplar

- Structured MITRE `ExternalReference`s; observed `<uid>1` with
  `content:not-reproduced`; `ConfiguredTool` links; collision-resistant
  source-reference IDs.
- Release tests: rebuild ↔ committed digest, manifest, critic
  `casegraph_raw` + provenance sidecar, validate complete.

Package versions bumped to **1.22.4**.

## [1.22.3] - 2026-07-15

mypy clean-up for the public `case_uco.validation` package moved in v1.22.1
(typed dict/tuple annotations, `validate_report` return type). No behavioral
change.

Package versions bumped to **1.22.3**.

## [1.22.2] - 2026-07-15

CI/CodeQL recovery after the v1.22.1 validation-module move, plus routine
dependency bumps. Registry publication remains opt-in (**disabled** for this
tag).

#### Fixes

- MCP / routing / Windows critic jobs can import `case_uco.validation`
  (`PYTHONPATH=python:mcp_server`, conftest + routing harness path fixes).
- Replace polluting star-import shims with explicit re-exports and `__all__`
  (CodeQL `py/polluting-import`, `py/unused-import`, unused `_parse_conforms`).
- Correct `extension_paths.PROJECT_ROOT` discovery after the package move.
- Orphan reachability follows `case-investigation:relevantAuthorization`.
- Concept-coverage fail-closed tests monkeypatch the implementation module;
  heuristic resolution tests track current `RULE_VERSION`.

#### Dependencies

- `sha2` 0.10 → 0.11 (Rust).
- `Microsoft.NET.Test.Sdk` 18.7.0 → 18.8.1.
- `ontology/UCO` submodule `748aea0` → `8335d32`.

Package versions bumped to **1.22.2**.

## [1.22.1] - 2026-07-14

Public Python validation API, CTI epistemic modeling for DarkWatchman, critic
policy alignment, and ATT&CK catalog coverage for the exemplar. Patch release
on the v1.22 line; registry publication remains opt-in (**disabled** for this
tag).

#### Public validation API

- Move the fail-closed SHACL + concept-coverage validator into
  `python/case_uco/validation/` (`validate_graph_file`,
  `validator_available`, `GraphValidationReport`, bundle/coverage helpers).
- MCP modules (`graph_validator`, `validation_bundle`, `concept_coverage`,
  `extension_paths`) become thin re-exports of the package implementation.
- `CASEGraph.validate_report()` delegates to the public API.
- Upper-ontology registry lives with the package
  (`case_uco/validation/upper_ontology_registry.json`);
  `mcp_server/upper_ontology_registry.json` is a symlink for compatibility.
- Import-level tests: `python/tests/test_validation_api.py`.

#### DarkWatchman CTI exemplar + recipe

- Add `examples/cti/darkwatchman_2021/` — Prevailion PACT DarkWatchman report
  (2021-12-14) as a `casegraph_raw` CASEGraph exemplar with unattributed
  `Grouping` activity cluster, capability vs observed Actions, VT `Event`s,
  registry/DGA `Configuration`, `WindowsTask`, `LogicalPattern` detections,
  source-contradiction Annotations, and `build-manifest.json` sidecar.
- Rewrite [`docs/recipes/cyber-threat-intelligence.md`](docs/recipes/cyber-threat-intelligence.md)
  for the three-branch actor model (Organization / unattributed Grouping /
  omit), claim provenance, and anti-pattern updates.

#### Critic and ATT&CK catalog

- `serializer_mode=casegraph_raw`; rule
  `CRIT-S-PY-TYPED-MODE-WITHOUT-TYPED-OBJECTS` when `typed_sdk` lacks typed
  `create()`.
- CTI-aware `CRIT-H-DERIVED-NO-HASH` (medium with identity/containment or
  `hash-status:not-published` / `source-bytes:not-acquired`).
- Proxy-duplicate accepts Action object/result and Moved/Copied/Renamed links.
- `provenance_manifest_path` verifies builder/recipe/output sidecar hashes
  without requiring implementation files in the Investigation graph.
- Extend `extensions/attack-technique/mitre-attack-catalog.ttl` with
  DarkWatchman techniques; CI test
  `python/tests/test_attack_catalog_coverage.py` fails when exemplars cite
  undeclared ATT&CK IRIs.

Package versions bumped to **1.22.1**.

## [1.22.0] - 2026-07-14

Critic acceptance loop (#74–#78), performance foundations (#70–#73), and
trust-boundary hardening. Installable packages ship on the GitHub Release;
registry publication remains opt-in via `PUBLISH_PACKAGES` (**disabled** for
this tag).

- **Executable SHA:** `2a859060e9e3b16f5a5365fe33bdf6b4663efbd3`
  ([CI](https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29362720114)
  green, 11/11 jobs;
  [CodeQL](https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29362720174)
  green for python/csharp/java-kotlin; code-scanning open alerts **0** at
  `2026-07-14T20:13:15Z`; 116 critic tests; 11/11 oracles; accepted repair
  replay; Windows critic smoke; advisory bench).
- **Oracle / repair CI artifacts** (exact-SHA): `critic-oracle-report`
  id `8323033763`; `critic-repair-charged-with-accepted` id `8323034246`.
- **Package preflight:** [`artifacts/ci/package-preflight-v1.22.md`](artifacts/ci/package-preflight-v1.22.md)
  (Python wheel/sdist clean install, NuGet consumer, Maven consumer, cargo
  package + publish `--dry-run`, local `cargo audit` clean).
- **Release/tag commit:** this documentation/evidence commit (descendant of the
  executable SHA; annotated tag `v1.22.0` points here).

#### Critic-loop security and trust-boundary hardening

- **#75/#76/#78 session↔audit reconciliation**: audit history is authoritative for
  pass-file digests and state; each transition binds `session_projection_sha256`
  over the **complete** semantic `session.json` (excluding only
  `latest_audit_event_sha256`) and stamps that event hash (audit-then-save).
  Retargeting hashes, forging `state=finalized`, altering control fields
  (`prior_findings`, `config`, extend approval, pass metadata), or interrupting
  the transaction fails closed (`critic_session_audit_reconcile_mismatch` /
  `critic_session_incomplete_transaction`). Integrity also gates extend/cancel.
- **#75 bundle finalization**: re-resolve and rehash OWL/SHACL/bridge/auxiliary
  resources from disk at finalize; compare to `config-pass-N.json`; include
  validator/built/resolver versions in `review_config_sha256`; fail
  `critic_session_bundle_drift` on mutation; prefer final complete+conforming
  validation.
- **#76 marking-aware sampling**: `sampling_disclosure` + egress decisions;
  marked/unknown → manual; CAC/juvenile/classified/SAR →
  `critic_sampling_restricted_content` unless
  `CASE_UCO_CRITIC_SAMPLING_RESTRICTED_ALLOW=1`; Phantom Gate marked fixture test.
- **#76 ledger-aware sampling**: `allowed_assessments` in `maybe_sample_critic`
  retry loop; assessment failures fall back to manual (`ok: true`); lifecycle
  tests for forbidden deterministic resolve / model finding assessments.
- **#78/#75 session integrity**: Draft 2020-12 schemas for session/config/
  review/critic/completed passes; pass-file SHA-256 in session+audit; verify
  before response/revision/status/finalize/handoff; tamper tests.
- **#76 report transaction**: resolve `report_output` at start; write report
  before committing `state=finalized`; never fail after irreversible finalize.
- **#77 reports**: stop committing mutable `*-latest.json`; CI artifacts only.

**Operational limitations**

- Session `audit.jsonl` is tamper-evident against partial or out-of-band
  modification. It is **not** a cryptographically signed external ledger against
  an administrator who can rewrite the session directory, audit history, and all
  related storage together.
- Critic sessions created on pre-release v1.22 commits before the full-session
  projection binding may fail closed after upgrade; restart those sessions
  rather than manually migrating them.

### Fixed

#### Critic loop P0 hardening

- **#75 resolution**: build `evaluated_rule_versions` from per-verifier
  `RuleExecution` so heuristic findings (`rule_version` 1.2.0) can resolve on
  repair; stamp `rule_version`/`verifier_rule_id` on heuristic findings;
  resolution/repair tests for CRIT-H rules + accepted two-pass charged-with session.
- **#76 sessions**: finalize rehash accepts generated graphs under write roots
  (sources stay read-only); prompts not persisted by default
  (`CASE_UCO_CRITIC_PERSIST_PROMPTS`); strip `prompt_package` from
  `review-pass-N.json`; rebuild prompts from hash-matching artifacts;
  `target_passes` for finalize/extend; full artifact-set revision comparison;
  `serializer_mode` / `extra_ontology_graphs` / `force_rdfs_inference` in
  SessionConfig + MCP tools; audit-chain verification on finalize.
- **#76 sampling**: non-bypassable `CASE_UCO_MCP_CRITIC_MODE`; schema-validate
  inside sampling retry loop; FastMCP pin `fastmcp==3.4.4`; session-policy
  gates so `*_with_sampling` cannot sample unless the existing session is
  `client_sampling`; profile defaults (`offline-investigation` → manual,
  production-like → disabled); string/`SamplingMessage` sample inputs.
- **#75 serializer AST**: dynamic CASEGraph public-API allowlist; tighter
  rel-id-collapse and unsafe-overwrite heuristics.
- **#77 eval**: repair-charged-with case with `--require-accepted`; truthful
  repair metrics (`repair_precision`); oracle detection precision; sanitized
  repo-relative harness reports with reproducibility metadata; Phantom Gate
  gold labeled `baseline-known-debt`.
- **#78 handoff**: dedicated `CASE_UCO_CRITIC_HANDOFF_TOKEN` only (never reuse
  extend challenge); `relative_to(candidates)` + `O_CREAT|O_EXCL` atomic create.
- **#71 C#**: `WriteStreaming` uses `File.Replace` (no delete-before-move).

#### Post-hardening follow-ups

- **C# netstandard2.0**: remove `File.Move(..., overwrite:)` (unsupported);
  keep `File.Replace` / Move-when-absent; never delete destination before
  successful replace; induced replacement-failure test proves old bytes survive.
- **`review_config_sha256`**: canonical fingerprint over critic_scope,
  serializer_mode, extensions, profiles, force_rdfs_inference, extra ontology
  hashes, bundle fingerprint, and bundle resource hashes; bound into
  `review_request_sha256` / response schema / artifact set / audit / revision
  / finalize; immutable `config-pass-N.json` snapshots; extension-, profile-,
  inference-, bundle-, and session-config-tamper tests.
- **Prompt rebuild verification**: before accepting a critic response, rebuilt
  package hashes must match stored pass metadata (typed mismatch errors);
  schema-validate session/review/completed files on load; status no longer
  hides audit-chain corruption.
- **Sampling gates**: deployment + existing session `model_policy` must both
  allow `client_sampling` before `Context.sample`; offline-investigation
  defaults to manual; production-like profiles default to disabled; FastMCP
  string/`SamplingMessage` inputs; `model_preferences` is `str | list[str] |
  None`; pin `fastmcp==3.4.4`; in-memory FastMCP sampling test.
- **CI**: Python bench+compare isolated in advisory `bench-python` job;
  `test-python` always runs MCP/critic/oracles/`--require-accepted`/mypy;
  Windows critic FileLock/session smoke; oracle and accepted-replay reports
  uploaded as artifacts.
- **Report sanitization**: absolute paths stripped to repo-relative;
  `repair_precision` + oracle detection precision; repository SHA / fixture
  hashes / rule-schema versions / env / dependency metadata.

#### Performance scope

- **#70–#73**: scoped experimental completion for v1.22; deferred contracts
  tracked as v1.23 follow-ups #79–#82.

### Added

#### Performance / scalability (#70–#73)

- **#70**: Thread-safe process-wide class/field registry caches with
  `clear_class_registry_cache()` / `ClearClassRegistryCache()` /
  `clearClassRegistryCache()` and duplicate-`CLASS_IRI` rejection (Python/C#/Java;
  Rust documents N/A for typed rehydration). C# caches Type→property attribute
  maps; Java caches Class→field maps (cleared with the same cache APIs).
- **#71**: Incremental used-prefix tracking + `write_streaming` /
  `WriteStreaming` / `writeStreaming` across Python/C#/Java/Rust. All four
  languages support atomic temp+rename and return/expose `{nodes, bytes_written}`
  metrics (`StreamingWriteResult` / `StreamingWriteMetrics`). Phase-2 bounded
  writer remains deferred (see `docs/PERFORMANCE_GUIDE.md`).
- **#72**: Experimental root closure via `partition` /
  `PartitionByRoots` / `partitionByRoots` / `partition_by_roots` with
  **outgoing + incoming** `@id` closure (`include_incoming=True` by default)
  and optional Python partition manifest (`return_manifest=True`).
  `split()` retained as catalog-only with warnings.
- **#73**: Expanded `benchmarks/run_python_bench.py` (catalog, relationship-rich
  partition, cold/warm `from_jsonld`, streaming write); committed
  `benchmarks/baselines/python-small.json`; `benchmarks/compare_baseline.py`
  (+100% CI gate); Rust/C#/Java bench runners; CI small-tier Python bench +
  compare step; `benchmarks/README.md`.

#### Critic loop (#74–#78)

- **#75 contracts**: authoritative model-response schema, bound per-pass consts,
  final `byte_size`/`max_bytes`, non-circular `prompt_content_sha256` →
  `review_request_sha256`, per-rule ledger with `verifier_rule_id` /
  `analysis_status`, offline remote `@context` rejection, Turtle relationship
  lint, occurrence/`unevaluated`, outgoing review schema validation,
  ledger-aware scorecards, serializer too-large AST skip. Graph heuristics
  v1.2.0 add action completeness, identity conflation, proxy duplicates,
  derived hash/provenance, marking inheritance, custody pairing, image-container
  mismatch, and compilation omission. Python AST adds nonexistent-API,
  relationship-ID collapse, silent lookup, unsafe overwrite, source-hash drift,
  synthetic hash, and quadratic-scan checks. CAC validation-subset includes
  detection terms so Phantom Gate gold can fully conform.
- **#76 sessions**: resumable workspace-confined `critic-sessions/` store with
  cross-platform locks, hash-chained audit, full artifact-set rehash at
  finalize, completed-pass merge of critic findings/assessments into blockers,
  outcomes (`accepted` / `completed_with_findings` / `blocked_with_findings` /
  …), MCP tools including async `start_critic_review_with_sampling` /
  `submit_critic_revision_with_sampling` (full prompt package + typed sampling
  fallbacks), returned `extend_approval_challenge`, reject over-cap iterations;
  FastMCP pinned to `fastmcp==3.4.4`.
- **#77 evaluation**: conforming gold oracles (micro Charged_With + Phantom
  Gate), micro cases for new heuristics, real session state-machine replay,
  oracle + session-replay harnesses, CI critic job with workspace roots.
- **#78 handoff**: explicit operator-selected type, approval token, preview by
  default, atomic no-overwrite writes under `critic-handoffs/candidates/` (no
  auto category promotion / GitHub / recipe promotion).

Docs: `docs/critic/RULES.md`, `docs/CROSS_LANGUAGE_PARITY.md`,
`docs/PERFORMANCE_GUIDE.md`.

Package versions bumped to **1.22.0**.

## [1.21.0] - 2026-07-12

Cross-ontology composition: IRI-indexed graph enrichment API, profile-aware
validation planner, upper-ontology recipes and exemplars, upper-ontology
exemplar quality gate, and experimental v1.22 performance foundations
(streaming write, boundary partitioning helpers, class-registry cache,
synthetic benchmarks). Issues #59–#69 closed as scoped-complete for this
release; #70–#73 remain open on the **v1.22.0** milestone as experimental
foundations (not completed v1.21 functionality).

Verified executable-code SHA: `d5b6987bce18a2797fd0f53ebedfd438e03e2a9d`
(CI + CodeQL green; zero open code-scanning alerts). Installable packages
ship on the GitHub Release; registry publication remains opt-in via
`PUBLISH_PACKAGES` (disabled for this tag).

### Added

#### Graph composition API (#67)

- Public IRI-indexed methods on `CASEGraph` / `CaseGraph` in **Python, C#,
  Java, and Rust**: `get`/`contains`/`expand_iri`, `upsert_node`, `add_type`,
  `add_property`, `link`, `create_relationship` (deterministic UCO
  Relationship IDs), plus `DuplicateNodeError` / reject-duplicates policy.
- Domain-first multi-typing on the **same IRI** without proxy duplicates.

#### Profile-aware validation planner (#68)

- `mcp_server/validation_bundle.py` — `resolve_validation_bundle(extensions,
  profiles)` with offline fingerprinting, BFO/gUFO exclusivity, CAC↔BFO
  fail-closed policy, GeoSPARQL→Simple Features dependency, ORG→FOAF/PROV-O
  `depends_on` closure (with cycle errors), `incompatible_with` enforcement,
  content-addressed lock-guarded cache (`hit`/`miss`/`stale`/`disabled`), and
  portable atomic manifests (`resolver_schema_version`, no absolute paths).
- `validate_graph_file(..., profiles=[...])` and MCP `validate_graph(profiles=...)`
  share one `ResolvedValidationBundle` object between SHACL and strict concept
  coverage (exact resources + fingerprint); coverage accepts only bundle
  subset/full terms; unselected upper-profile terms fail as structured
  `profile_not_selected`. `profiles=None` authorizes zero upper profiles.
- `GraphValidationReport` exposes selected/requested profiles, bundle
  fingerprint, resources, compatibility notes, validator version, cache
  status, and independent stage statuses (bundle / SHACL execution /
  SHACL conformance / coverage execution / coverage conformance).
- ORG and PROF added to `get_uco_profiles` / `UCO_PROFILES` (paths/deps synced
  from `PROFILE_REGISTRY`).

#### Upper-ontology recipes and exemplars (#59–#66)

- Recipes: foundational BFO/gUFO, PROV-O lineage, OWL-Time, GeoSPARQL, FOAF/ORG,
  PROF metadata, SOLVE-IT plan vs execution, and **cross-ontology-composition**
  (replaces competing cross-domain guidance; legacy file redirects).
- Builders and JSON-LD under `examples/upper-ontology/` (local + CI gate via
  `run_recipe_examples.py --validate`; require `conforms` and
  `verification_status == complete`).
- MCP `route_investigation_content` returns `ordered_recommendations` for
  multi-domain / cross-ontology matches (`primary_composition_recipe`,
  supporting recipes, extensions, profile tiers, `validation_bundle_preview`,
  compatibility warnings, and `ontology_gap_workflow` when nothing matches).

#### Relationship kind registry and lint (CQ-40)

- `mcp_server/relationship_kinds.json` machine-readable vocabulary snapshot,
  `lint_relationship_kinds()` lint API, and recipe-gate invocation in
  `run_recipe_examples.py` (open-vocabulary warnings by default; strict errors
  only when `allow_open_vocabulary=False`). Relationship governance is
  **registry + lint API + recipe-gate invocation**, not a closed enforcement
  layer.

#### Upper-ontology exemplar quality gate (#69)

- Executable gate for the **nine upper-ontology exemplars** listed in
  `docs/recipes/recipe-execution.json` (not repository-wide catalog migration —
  that remains **v1.22**). `mcp_server/tools/run_recipe_examples.py` runs those
  builders in isolated temp dirs with timeouts, RDFLib parse, profile SHACL +
  strict coverage, expected-invalid fixtures, optional competency queries, and
  machine-readable reports (CI uploads the report artifact; do not commit
  workstation-local paths).
- CI job `recipe-validation` installs `case-utils`, fails closed without
  `case_validate`, and uploads the report artifact. Path filters include
  `docs/**`, `examples/**`, `benchmarks/**`, `scripts/**`.
- `promote_recipe` fails closed when `recipe-execution.json` metadata is
  absent (`recipe_execution_metadata_missing`), when `case_validate` is
  unavailable, or when the executable gate fails; then invokes the same
  gate before catalog writes.

#### Performance / scalability foundations (#70–#73) — experimental v1.22

These are early **experimental v1.22 foundations**, not finished production
features:

- Process-wide class-registry cache for `from_jsonld` (#70) — experimental.
- `write_streaming()` incremental JSON-LD writer (#71) — experimental.
- `partition_by()` / `partition_by_label()` experimental label partitioning
  by a caller-supplied boundary key (not a full dependency closure);
  `split()` warns that object-count splits are unsafe for investigation
  graphs (#72).
- `benchmarks/run_python_bench.py` small-tier synthetic harness (#73) —
  experimental.

### Fixed (ChatGPT Pro second review)

- CI root causes on `ed0c7f9`: geosparql recipe snippet syntax; generator
  `__init__.py` export of composition types; Rust clippy `unwrap_used`.
- Recipe gate hardened (CQ-01–CQ-12); literal same-bundle coverage
  (CQ-27–CQ-36); graph deep-copy / named policies / multi-`@id` accumulation
  (CQ-13–CQ-26); promotion/routing (CQ-37–CQ-40, including relationship-kind
  lint in the recipe gate).
- Code-scanning quality: **72** findings across two passes (**40** initial +
  **32** follow-up), all dispositioned as fixed (see
  `artifacts/ci/REVIEW-DISPOSITION.md`).

### Changed

- Graph composition (#67): default duplicate policy is **reject** in all
  languages; Python adds `merge_identical` / `merge_compatible` / `replace`
  with scalar-conflict diagnostics; `get()` returns a deep copy;
  `from_jsonld` uses the IRI index; multi-type `@type` rehydration picks the
  most specific unambiguous class; context prefix collisions are rejected.
- README and CROSS_LANGUAGE_PARITY document the composition and profile APIs
  (RDF-equivalent / deterministic parity, not byte-identical JSON-LD).
- Package versions bumped to **1.21.0**.

## [1.20.0] - 2026-07-11

Add **Operation PHANTOM GATE** — a fictitious, multipart investigation stress-test
scenario with a validated 452-node JSON-LD graph, acceptance gates, coverage
contract, and CASEGraph round-trip — plus graph-validator hooks for SOLVE-IT KB
individuals when CAC validation-subset is active.

### Added

#### Operation PHANTOM GATE — fictitious multipart investigation stress test (`examples/scenarios/`)

- **`operation-phantom-gate.md`** — Tier **T0 (fully synthetic)** multipart
  investigation narrative (**INV-2026-PGA-001**). All persons, docket numbers,
  identifiers, and evidence content are **fabricated for SDK/MCP exercise only**
  — not a real case, not derived from live investigative data, and not suitable
  for operational use. The scenario is designed to **stress-test** the SDK's
  ability to model investigations that are **adjacent to, in, and through the
  cyber domain**: elder-fraud couriers, RICO/crypto social engineering,
  insider/export tracks, APT/ATT&CK CTI, ICAC/CAC sextortion, classified
  disclosure, weapons/drugs takedown, chain of custody, data-handling markings,
  SOLVE-IT acquisition workflows, and AI/ML analysis pipelines — in one
  interoperable graph.
- **`build_phantom_gate_scenario.py`** → **`operation-phantom-gate.jsonld`**
  (452 nodes, **`Conforms: True`**) — validated builder exercising nine
  extension bundles (`legalproc`, `rico`, `cryptoinv`, `attack-technique:full`,
  `solveit`, `weapons`, `drugs`, `cac`) with fail-closed validation (raises
  if `case_validate` is unavailable or non-conformant).
- **`phantom_gate_acceptance.py`** — post-build acceptance gates: strip
  `relevantAuthorization` from actions (use `Authorized_By` relationships
  instead), multi-pass marking inheritance (`Derived_From`, `Contained_Within`,
  `Part_Of`, `Attachment_Of`, action inputs→results, SOLVE-IT `contains`),
  duplicate `@id` deduplication, embedded scenario SHA-256 verification, and
  four SOLVE-IT `WeaknessEvaluationSet` chains (ART-002 imaging, ART-001 logical
  acquisition, ART-006 partial juvenile scope, DFT-1046 redaction).
- **`phantom_gate_longtail.py`** — long-tail coverage module (per-docket
  sub-investigations, ART-003..008, MSG/EMAIL/FS/NET/PROC depth, COC-003/004,
  AI-003/004, expanded authorizations and charging instruments) wired into the
  main builder.
- **`phantom_gate_coverage.json`** + **`check_phantom_gate_coverage.py`** —
  machine-readable fidelity contract (69 artifact labels, six docketed
  sub-tracks + CTI wing, authorization and node-count gates, scenario hash
  and authorization-placement assertions).
- **`build_phantom_gate_typed.py`** — CASEGraph load/serialize round-trip smoke
  test with post-roundtrip SHACL validation.
- **`examples/scenarios/README.md`** — scenario index and agent workflow.
- Sample MCP routing outputs under `examples/scenarios/mcp_outputs/`.

The scenario is structurally grounded in validated exemplars under
`examples/pacer/`, `examples/cti/`, and `examples/solveit/` but combines them
into a single composite exercise for recipe routing, extension interop, and
semantic modeling review.

### Changed

- **README.md** — documents the fictitious scenario stress test, its purpose,
  and the `examples/scenarios/` workflow.
- **Operation PHANTOM GATE (round 2 modeling review)** — authorization
  semantics corrected (`relevantAuthorization` only on `Investigation`; actions
  use `performer`/`instrument`/`object`/`result` plus `Authorized_By` edges);
  stable scenario IRIs consolidated (no duplicate UUID proxies for ART-003/007,
  FS-004/008, ART-002 E01/container); scenario markdown synced with graph facts
  (iPhone 13 Pro, APFS FS-006, prepaid-card 11:45) and auto-embedded SHA-256;
  marking inheritance fixed (parent→derived direction); redundant reverse
  `part_of` containment removed (`Investigation.object` is canonical); MSG-004
  direction and Mei Chen WeChat account; AI-002 full ranked result set; AI-004
  structured action; COC-003 performers/instruments/hash verification.
- **`mcp_server/graph_validator.py`** — optional `extra_ontology_graphs` and
  `force_rdfs_inference` for graphs that need SOLVE-IT KB individuals when CAC
  validation-subset disables default RDFS inference.

## [1.19.0] - 2026-07-11

Reorganize vendored upstream ontologies under `ontology/`, vendor upper-ontology
sources and CDO-Shapes profiles for fully offline operation, consolidate example
directories, and unify upstream freshness checks — without breaking name-based
extension APIs (`CASE_UCO_EXTENSIONS=cac`, `validate_graph(extensions=[...])`,
`search_classes(scope="solveit")`).

### Changed

#### Ontology directory layout

- **Upstream-maintained ontologies moved to `ontology/`** — `cac`, `aeo`, and
  `solveit` now live alongside CASE and UCO git submodules under `ontology/`
  instead of `extensions/`. SDK-developed extensions (`attack-technique`,
  `cryptoinv`, `legalproc`, `rico`, `weapons`, `drugs`, `toolcap`) remain in
  `extensions/`.
- **`mcp_server/extension_paths.py`** — central resolver searches both roots
  (`extensions/` first, then `ontology/`) for `manifest.json`-bearing
  directories. All MCP, validation, lifecycle, routing, and generator code
  paths updated to use it; name-based APIs are unchanged.
- **Git submodule paths updated** — CAC and AEO submodule entries now point at
  `ontology/cac/ontology` and `ontology/aeo/ontology` (was
  `extensions/cac/ontology` / `extensions/aeo/ontology`).
- **Makefile `EXT_DIR` and `rollback-extension`** — resolve the correct root per
  extension name.

### Added

#### Offline upper-ontology vendoring (`ontology/upper/`)

- **Pinned source files** for all eight profiled upper ontologies (BFO, gUFO,
  PROV-O, OWL-Time, GeoSPARQL core + Simple Features, FOAF, ORG, PROF) plus
  `provenance.json` recording source URL, SHA-256, and fetch timestamp.
- **CDO-Shapes SHACL profiles** vendored under `ontology/upper/shapes/`
  (`sh-bfo.ttl` through `sh-prof.ttl`), pinned to specific upstream commits.
- **`build_upper_ontology_registry.py`** defaults to the vendored snapshot
  (offline rebuild); `--fetch` refreshes sources then rebuilds the registry.
  `make rebuild-upper-registry` (offline) and `make sync-upper` (network).
- **`get_uco_profiles`** reports `local_source` and `local_shapes` paths for
  each profile so agents can reference offline files without fetching URLs.

#### Unified upstream freshness

- **`.github/workflows/upstream-freshness.yml`** replaces the SOLVE-IT-only
  weekly check: compares CASE, UCO, AEO, CAC, and SOLVE-IT pins against
  upstream (release lag fails the job for CAC/SOLVE-IT; branch drift on
  CASE/UCO/AEO emits warnings only).
- **`make sync-upstream`** — one command to refresh all submodule pins, the
  SOLVE-IT snapshot, and the upper-ontology vendored files.

#### Examples consolidation

- **`example_agentmcp_outputs/` merged into `examples/agent-outputs/`** — four
  early MCP worked examples (Cellebrite extraction, chain of custody, USN
  journal, WiFi capture) now live under the main examples tree.

### Migration notes

- Scripts that hardcoded filesystem paths like
  `extensions/cac/ontology/...` or `extensions/solveit/solve-it-kb.ttl`
  should switch to `ontology/cac/...` and `ontology/solveit/...`. The SDK
  APIs that take extension *names* (`cac`, `solveit`, etc.) are unaffected.
- After upgrading, run `git submodule update --init --recursive` so CAC/AEO
  submodules resolve at their new paths.

### Tests

- `mcp_server/tests/test_extension_paths.py` — dual-root resolution, search
  order, and non-extension directory filtering.

## [1.18.0] - 2026-07-10

SOLVE-IT support: the SDK bundles a pinned, sync-managed snapshot of the
[SOLVE-IT](https://solveit-df.org) digital forensics knowledge base and its
CASE/UCO extension ontology, with dedicated MCP query tools, a modeling
recipe, routing, and a validated exemplar — so investigators can state
objectives, select techniques, and work through weaknesses and mitigations
(ASTM E3016-18 Error Mitigation Analysis) inside CASE/UCO graphs.

### Added

#### Bundled `solveit` extension (`extensions/solveit/`)

- **Vendored pinned snapshot** of upstream
  [solve-it-ontology](https://github.com/SOLVE-IT-DF/solve-it-ontology)
  (v0.1.9, commit-pinned; MIT): the core module
  (`solveit-core:Objective/Technique/Weakness/Mitigation`,
  `SolveitInvestigativeAction` with `usedTechnique`/`appliedMitigation`),
  four observable modules (~60 method-centric classes: image containers,
  bitstreams, timelines, keyword search artifacts, acquisition records),
  SHACL shapes, analysis (Hypothesis), SQLite internals, tool capability
  profiles, and weakness assessment (`solveit-wa:WeaknessEvaluation` with
  likelihood/impact/RPN ratings).
- **Compiled knowledge base** (`solve-it-kb.ttl`, from the
  [SOLVE-IT](https://github.com/SOLVE-IT-DF/solve-it) `v0.2026-06` release
  line): 23 objectives, 187 techniques, 339 weaknesses (ASTM E3016-18
  categorized), 270 mitigations, fully cross-linked with CASE/UCO
  input/output class annotations.
- **Generated punned technique catalog**
  (`solveit-technique-catalog.ttl`): every technique punned as an
  `owl:Class` typed `uco-action:Technique` and subclassing
  `uco-action:Action` with `techniqueID` — the UCO 1.5.0 metaclass pattern
  (ucoProject/UCO PR #676), identical in shape to the bundled MITRE ATT&CK
  catalog. Catalog IRIs are the canonical knowledge-base IRIs, so the
  native individuals and the punned classes coexist in one graph; the
  manifest declares `depends_on: ["attack-technique"]` for the metaclass.
- **Promotion-gate-quality manifest**: full upstream provenance (repos,
  commit SHA, release tag, ontology version, sync timestamp), a conforming
  exemplar (`solveit-exemplar.ttl` — disk imaging with applied mitigations
  and a weakness evaluation, demonstrating both modeling styles), an
  expected-invalid fixture proving the SHACL shapes constrain, and two
  competency queries (technique → weakness → mitigation chain; exemplar
  uses-technique). All six v1.17.0 lifecycle gates pass. A small SDK-local
  bridge (`solveit-local-anchors.ttl`) anchors three upstream
  enumeration classes that ship without `rdfs:subClassOf`.
- **Class registry** (`_registry.json`, 296 classes including the punned
  techniques) so `search_classes(scope="solveit")` and the other discovery
  tools cover SOLVE-IT, plus a `packages/case-uco-solveit/` Python package
  scaffold exposing the registry via the `case_uco.extensions` entry point.

#### MCP knowledge-base tools (`mcp_server/solveit_index.py`)

- **`search_solveit(query, kind?, limit?)`** — ranked keyword search across
  objectives/techniques/weaknesses/mitigations with exact-identifier
  lookup, kind filtering, bounded results, and a knowledge-base provenance
  stamp on every response.
- **`get_solveit_details(id)`** — the full record for a DFO-/DFT-/DFW-/DFM-
  identifier with cross-references: objective → techniques; technique →
  objectives, subtechniques, weaknesses and each weakness's mitigations
  (the Error Mitigation Analysis view), example tools, synonyms, CASE/UCO
  input/output classes, and modeling guidance; weakness → mitigations and
  affected techniques; mitigation → what it mitigates.
- **`plan_solveit_workflow(text)`** — maps free-text investigation goals to
  matched objectives (own-text match lifted by best member-technique
  scores), ranked candidate techniques, and per-technique
  weakness/mitigation checklists, with step-by-step workflow guidance.
  Submitted text is treated as untrusted content; responses contain only
  pinned knowledge-base metadata.

#### Sync tooling for SOLVE-IT's rapid release cycle

- **`mcp_server/tools/sync_solveit.py`** re-vendors every upstream file at
  a named ref, regenerates the punned technique catalog from the knowledge
  base, verifies every TTL parses, and rewrites manifest provenance —
  `make sync-solveit [REF=<sha>]`, or `make sync-solveit-offline` to
  regenerate from already-vendored files (air-gapped `--source-dir`
  supported).
- **Weekly CI freshness check** (`.github/workflows/solveit-freshness.yml`)
  compares the pinned knowledge-base release and ontology commit against
  upstream and fails when the snapshot is behind — the "keeping pace"
  signal.

#### Recipe, routing, and exemplar

- **New recipe** `docs/recipes/solve-it-investigation-planning.md` (69
  recipes total): state the objective, record method with
  `SolveitInvestigativeAction`, type acquisition outputs with SOLVE-IT
  observables, rate residual risk with `WeaknessEvaluation`, and use both
  technique styles (native today, metaclass for UCO 1.5.0) — registered in
  `docs/recipes/INDEX.md` and `RECIPE_INDEX`.
- **New routing family** `forensic-process-qa` (technique selection, tool
  testing/validation, quality assurance, Daubert-style methodology
  challenges, error mitigation) plus `solveit` extension/recipe wiring on
  the `device-mobile-forensics` and `filesystem-media` families. The
  held-out routing evaluation passes unchanged (no corpus modification, no
  governance tag needed).
- **Validated worked example** `examples/solveit/` — a synthetic laptop
  acquisition (DFT-1002 with DFM-1003/DFM-1004 applied, weakness
  evaluation of DFW-1004, and a metaclass-style hash-verification action)
  that builds and conforms via `validate_graph(extensions=["solveit"])`.

### Tests

- `mcp_server/tests/test_solveit.py` (23 tests): index integrity and
  bounds, exact-ID/keyword/kind search, detail cross-references, workflow
  planning (including injection-styled input), punned catalog completeness
  and shape, dependency resolution pulling `attack-technique`, strict
  concept coverage for both modeling styles (fabricated `solveit-core:`
  terms fail), exemplar conformance, and the expected-invalid fixture.

## [1.17.0] - 2026-07-10

Fail-closed validation, enforceable secure deployment, hardened knowledge
promotion, and an external routing evaluation harness — addressing the four
follow-on review issues [#55](https://github.com/vulnmaster/CASE-UCO-SDK/issues/55)–[#58](https://github.com/vulnmaster/CASE-UCO-SDK/issues/58)
plus all 35 open CodeQL code-scanning alerts.

### Added

#### Fail-closed strict validation (issue #55)

- **Upper-ontology registry verification status** (closes [#55](https://github.com/vulnmaster/CASE-UCO-SDK/issues/55)):
  concept coverage and `validate_graph` reports now carry `verification_status`
  (`complete` / `could_not_verify`) and `verification_errors`. When a graph
  uses profiled upper-ontology terms and `upper_ontology_registry.json` is
  missing, unparseable, or lacks per-ontology provenance (`source_url` plus
  `version_iri`/`version_info`), the graph is reported **non-conforming**
  instead of the terms being silently namespace-accepted. Graphs that use no
  upper terms are unaffected by registry absence. The registry cache key now
  includes a file fingerprint so registry edits invalidate immediately.
- **Typed extension-resolution errors**: `resolve_extension_dependencies`
  raises `extension_unknown`, `extension_dependency_missing`,
  `extension_manifest_malformed`, and `extension_dependency_cycle` (explicit
  cycle detection with chain reporting) instead of silently skipping bad
  inputs; diamond dependencies still resolve once.
- **Lifecycle status integrity**: an unrecognized manifest `status` is now
  `invalid` — never routable, never treated as operational — and
  `route_investigation_content` reports malformed manifests and invalid
  statuses in a new bounded `integrity_failures` payload field rather than
  omitting the extension without a trace.

#### Hardened promotion gates and recipe lifecycle (issue #56)

- **Strengthened extension promotion gates** (closes [#56](https://github.com/vulnmaster/CASE-UCO-SDK/issues/56)),
  all enforced by `make promote-extension`: `manifest_schema` (required
  fields, listed files exist, status recognized), `ontology_files_parse`,
  `classes_anchored` (every declared class must subclass a class *explicitly
  declared* in core, an operational dependency, the pinned upper-ontology
  registry, or the extension itself — an anchor to a nonexistent parent now
  fails), `exemplars_validate` (**at least one conforming exemplar is now
  required**), `negative_fixtures` (extensions shipping SHACL shapes must
  ship `invalid_exemplar_files` that *fail* validation, proving the shapes
  actually constrain), and `competency_queries` (declared SPARQL queries must
  return results against the exemplars). Promotion provenance now records the
  git commit and active deployment profile alongside reviewer, timestamp, and
  gate results.
- **Recipe promotion/deprecation** (`make promote-recipe RECIPE=<slug>
  REVIEWER=...`, `make deprecate-recipe`): transactionally moves a candidate
  from `docs/recipes/candidates/` into `docs/recipes/`, validates recipe
  structure (title, Scenario/Pattern/Validation sections, code fence,
  metadata block), registers it in `docs/recipes/INDEX.md` and the
  `RECIPE_INDEX` in `mcp_server/domain_index.py`, and records provenance in
  `docs/recipes/promotion-log.json`; deprecation reverses all of it. A
  structurally invalid candidate is rejected untouched.

#### Enforceable MCP secure production mode (issue #57)

- **Deployment profiles** (`CASE_UCO_MCP_PROFILE`, closes [#57](https://github.com/vulnmaster/CASE-UCO-SDK/issues/57)):
  `development` (permissive, backward compatible), `offline-investigation`,
  `production-authoring`, and `production-review` — the latter three imply
  secure mode (also settable directly via `CASE_UCO_MCP_SECURE_MODE=1`);
  unknown profile names fail closed as secure.
- **Fail-closed startup validation**: in secure mode the server validates its
  configuration at startup and **refuses to start** (exit 3) on missing or
  nonexistent roots, dangerously broad roots (filesystem/drive roots and home
  directories, override only via `CASE_UCO_MCP_ALLOW_BROAD_ROOTS=1` with the
  acknowledgement recorded), or write roots nested inside evidence read
  roots. At runtime, unconfigured roots return `read_roots_unconfigured` /
  `write_roots_unconfigured` instead of falling back to unrestricted access.
- **Profile-scoped promotion authority**: `offline-investigation` denies
  extension/recipe promotion (`promotion_not_permitted_in_profile`);
  `production-review` requires a named reviewer
  (`reviewer_identity_required`).
- **`get_security_profile` MCP tool**: bounded, non-sensitive summary of the
  active posture (profile, secure-mode flag, root counts, promotion
  authority, configuration errors) — no paths or environment contents.

#### Held-out routing evaluation harness (issue #58)

- **External evaluation corpus** (`evaluation/routing/heldout-corpus-v1.json`,
  closes [#58](https://github.com/vulnmaster/CASE-UCO-SDK/issues/58)): 39
  synthetic held-out cases (paraphrase, multi-domain, negative/abstention,
  adversarial phrasing) with per-case provenance, kept apart from the
  development benchmark and governed by a written co-modification rule: a
  change touching both router logic and the corpus requires the
  `[eval-governance-approved]` commit tag, enforced by a CI guard.
- **Evaluation harness** (`evaluation/routing/run_evaluation.py`,
  `make eval-routing`): reports macro-F1, multi-label exact match and mean
  Jaccard, paraphrase recall, negative-family rate, abstention accuracy, and
  hybrid-vs-baseline family recall against thresholds pinned in the corpus
  file; exits nonzero when any threshold regresses. Runs in CI on every
  router/corpus change with the report uploaded as an artifact. Because the
  MCP server is always operated by an LLM host (from small local models to
  frontier models), the corpus targets the *deterministic routing layer* —
  the floor every host model inherits — and the README documents how to
  extend it with host-LLM end-to-end cases.

### Changed

- `SECURITY.md`: supported line is now 1.17.x; documented fail-closed
  validation semantics, secure deployment profiles, and the hardened
  promotion gates.
- `mcp_server/README.md`: new "Deployment profiles and secure mode" section.
- `docs/recipes/recipe-authoring.md`: recipe promotion now uses
  `make promote-recipe` / `make deprecate-recipe` instead of manual editing.
- All language package versions synchronized to **1.17.0**.
- MCP server test suite grown from 183 to 218 tests (secure mode, fail-closed
  coverage, typed dependency errors, promotion gates, recipe lifecycle).

### Fixed

- **All 35 open CodeQL code-scanning alerts**: empty exception handlers in
  `knowledge_lifecycle.py` replaced with specific handling and debug logging;
  implicit string concatenations in `investigation_router.py` list literals
  made explicit; unused imports removed (`dataclasses.field`, test-module
  duplicates, `datetime`/`timezone` in the Lotus Blossom example); unused
  local variables removed from the Lam, Lindell, and Grayson PACER example
  builders (side-effecting calls preserved); the generated packages'
  `_REGISTRY_PATH` module global renamed to the public `REGISTRY_PATH` it
  actually is (referenced by tool entry points), with the generator template
  updated to match.
- FOAF entry in the upper-ontology registry now carries pinned
  `version_info` (FOAF 0.99 publishes no `owl:versionIRI`), so registry
  provenance validation passes for all nine profiled ontologies.

## [1.16.0] - 2026-07-10

Validation-integrity and security-hardening release addressing the eight
review issues [#47](https://github.com/vulnmaster/CASE-UCO-SDK/issues/47)–[#54](https://github.com/vulnmaster/CASE-UCO-SDK/issues/54).

### Added

#### Validation integrity (issues #47, #48, #49)

- **Pinned upper-ontology term registry** (`mcp_server/upper_ontology_registry.json`, closes [#47](https://github.com/vulnmaster/CASE-UCO-SDK/issues/47)): strict concept coverage now validates profiled upper-ontology terms (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL + Simple Features, FOAF, ORG, PROF) against the exact declared terms of pinned releases (543 terms with source URL and `owl:versionIRI` provenance) instead of accepting whole namespaces — a fabricated `prov:CompletelyImaginaryProperty` now fails with the distinct `unknown_upper_ontology_terms` report category. Regenerate with `mcp_server/tools/build_upper_ontology_registry.py` (supports `--source-dir` for air-gapped rebuilds). Foundational W3C vocabularies (RDF/RDFS/OWL/XSD/SHACL/SKOS/DC/OA) remain namespace-accepted under an explicitly documented policy.
- **RDF-role-aware concept coverage** (closes [#48](https://github.com/vulnmaster/CASE-UCO-SDK/issues/48)): declared terms are tracked by role (class, property, SHACL shape, unknown) from explicit typing plus structural inference (`rdfs:subClassOf`, `rdfs:domain`/`range`, `sh:targetClass`, `sh:path`). A declared class used as a predicate — or a property used as an `rdf:type` class — is reported as a `role_mismatches` entry (`declared_role` / `used_as`) distinct from `undeclared`. OWL punning is supported: the ATT&CK `uco-action:Technique` metaclass pattern (technique = `owl:Class` + instance) has explicit tests.
- **Content-fingerprint cache invalidation** (closes [#49](https://github.com/vulnmaster/CASE-UCO-SDK/issues/49)): the declared-term cache key now includes an mtime/size fingerprint of every ontology file, so a concept added, removed, or renamed in an extension mid-process is recognized on the next validation without restarting the MCP server — completing the self-improvement loop. A bounded cache (16 entries) plus an explicit `clear_declared_term_cache()` are provided; single-process cache-refresh tests included.
- `extensions=[...]` lists now resolve manifest `depends_on` entries transitively (`resolve_extension_dependencies`): `rico` declares `depends_on: ["legalproc"]`, so its exemplar validates standalone.

#### MCP security hardening (issues #50, #51)

- **Filesystem workspace policy** (`mcp_server/workspace_policy.py`, closes [#50](https://github.com/vulnmaster/CASE-UCO-SDK/issues/50)): deployments confine `process_document_file` and `validate_graph` with `CASE_UCO_MCP_READ_ROOTS` / `CASE_UCO_MCP_WRITE_ROOTS` / `CASE_UCO_MCP_ALLOW_OVERWRITE`. Containment is enforced on fully resolved paths (`..` traversal and symlink escapes rejected), outputs never overwrite by default under an active policy, source and destination may never resolve to the same file, and violations return typed, non-sensitive errors (`source_outside_read_roots`, `output_outside_write_roots`, `progress_outside_write_roots`, `output_exists`, `source_output_conflict`). No policy configured = unchanged behavior. 14 tests in `mcp_server/tests/test_workspace_policy.py`; deployment guidance in `mcp_server/README.md`.
- **Untrusted-evidence trust boundary** (closes [#51](https://github.com/vulnmaster/CASE-UCO-SDK/issues/51)): all extracted/submitted content is labeled `content_trust: untrusted-source-content` in `process_document_file` results, extraction bundles (`extracted-content.json`), and both routing tools. Extracted text is scanned for prompt-injection indicators (instruction override, role reassignment, prompt disclosure, tool invocation, persistence/exfiltration requests, chat markup) and results carry bounded `injection_warnings` that never echo the payload. The server's MCP instructions and the workspace agent rules now explicitly prohibit treating evidence text as directions and require persistent changes to originate from an operator decision. Tests in `mcp_server/tests/test_untrusted_content.py` demonstrate injection-bearing documents produce warnings and no writes beyond the declared output artifacts.

#### Knowledge lifecycle (issue #52)

- **Staged promotion for learned artifacts** (`mcp_server/knowledge_lifecycle.py`, closes [#52](https://github.com/vulnmaster/CASE-UCO-SDK/issues/52)): extensions carry a manifest `status` — `candidate` (excluded from routing discovery, still loadable explicitly by name), `operational` (default for the bundled nine), `deprecated` (emergency revocation, provenance retained). `make promote-extension EXT=... REVIEWER=...` runs validation gates (ontology parse, class subclass-anchoring, exemplar `case_validate` conformance) and records reviewer/timestamp/gate provenance in the manifest; a failed gate leaves the candidate untouched. `make deprecate-extension`, `make rollback-extension EXT=... REF=<git-ref>` (one-command git-based restore), and `make lifecycle-status` complete the workflow. Candidate recipes live in `docs/recipes/candidates/` (invisible to `RECIPE_INDEX` and routing) until promoted per the updated `docs/recipes/recipe-authoring.md`. 12 tests in `mcp_server/tests/test_knowledge_lifecycle.py`.

#### Hybrid routing (issue #53)

- **Hybrid retrieval with calibrated abstention** (`mcp_server/semantic_retrieval.py`, closes [#53](https://github.com/vulnmaster/CASE-UCO-SDK/issues/53)): `route_investigation_content` now layers an offline, deterministic lexical-semantic stage (token normalization, curated synonym-group expansion, bounded overlap scoring) over the keyword baseline. Every match reports `match_stages`, `scoring` (`keyword_score`, `semantic_score`, calibrated `confidence`), and `semantic_evidence`; the keyword-only result is always returned as `deterministic_baseline` for auditability. Below the abstention threshold the router returns `extension_gap_guidance` plus `abstained_candidates` instead of a weak guess; `routing_confidence` reports the level and thresholds. Colloquial paraphrases now route ("my daughter was blackmailed into sending photos" → CAC; "somebody hacked our network and encrypted our files, demanding bitcoin" → network intrusion + crypto). A labeled benchmark corpus (`mcp_server/tests/test_routing_benchmark.py`) proves recall improvement over the keyword baseline with zero precision regression on negatives. Adjusted from the issue: embeddings/LLM re-ranking were deliberately not built in — the semantic stage is curated-lexical so closed/offline Link-Look deployments work unchanged and generative steps cannot bypass validation or promotion controls.

#### Extensions

- `toolcap` gained `manifest.json` (and a bundled `capability-pending.ttl` declaring the proposed UCO capability namespace from [UCO #682](https://github.com/ucoProject/UCO/issues/682)), so it now participates in extension loading, strict concept coverage (`extensions=['toolcap']`), lifecycle status, and registry generation like the other bundled extensions.

#### CI

- The MCP server test suite (now 183 tests) runs in CI (`.github/workflows/ci.yml`), and `mcp_server/**` / `extensions/**` changes trigger the pipeline; new `make test-mcp` target.

### Changed

- **`SECURITY.md` rewritten for v1.16.0** (closes [#54](https://github.com/vulnmaster/CASE-UCO-SDK/issues/54)): supported-version table now names the current release line (1.16.x); bundled extension ontologies, manifests, registries, shapes, and the upper-ontology registry are in scope as operational capabilities (no longer "examples, not production dependencies"); documented MCP trust boundaries (filesystem policy, indirect prompt injection, self-improvement governance, validation integrity), upstream-vs-SDK reporting split, sensitive-investigative-data handling, and a release checklist item for the policy itself.
- `process_document_file` MCP results now report `validation_status: "not_validated"` (the tool never ran SHACL — the previous hardcoded `"valid"` was misleading) and expose `extracted_content_path` / `annotations_path` so callers can find the extraction bundle.
- `validate_graph` reports gained `unknown_upper_ontology_terms` and `role_mismatches` categories alongside `undeclared_concepts`, with per-category guidance.
- The Python generator now sources `__version__` from `python/pyproject.toml` during generation instead of hardcoding `0.1.0` — fixes the CI Version Consistency Check failure introduced by regeneration during the v1.15.0 release (`generator/src/case_uco_generator/backends/python_backend.py`).
- All language package versions synchronized to **1.16.0** (`python/pyproject.toml`, `python/case_uco/__init__.py`, `csharp/CaseUco/CaseUco.csproj`, `java/pom.xml`, `rust/Cargo.toml`, README header and version matrix).
- Language registries (`_registry.json`) regenerated; they now include the `toolcap` and proposed-capability modules.

### Fixed

- Fabricated terms inside profiled upper-ontology namespaces no longer pass strict concept coverage (#47).
- Declared terms used in the wrong RDF role no longer pass silently (#48).
- Stale declared-term caches no longer hide mid-process ontology edits (#49).
- `rico-exemplar.ttl` and `toolcap-exemplar.ttl` now pass strict concept coverage standalone (dependency resolution + toolcap manifest).

## [1.15.0] - 2026-07-10

### Added

#### Extension ontologies (five new, all bundled with the SDK)

- **`cryptoinv`** — cryptocurrency and financial-crime investigation (`extensions/cryptoinv/`): crypto address/transaction/wallet and point-in-time holding facets (tracking [UCO #675](https://github.com/ucoProject/UCO/issues/675)), financial-crime infrastructure (VASPs, darknet markets, mixing services, aligned with the INTERPOL DW-VA Taxonomy), and criminal legal process classes. Grounded in and validated against *U.S. v. Lichtenstein & Morgan* (D.D.C. `1:23-cr-00239-CKK`, Bitfinex hack laundering). Python package scaffold in `packages/case-uco-cryptoinv/`.
- **`legalproc`** — jurisdiction-neutral criminal legal process (`extensions/legalproc/`): charging instruments, criminal charges with `offenseForm`/`objectOffense` (conspiracy, attempt, § 924(c)-style derivative counts), pleas, proceedings, verdicts, sentences, forfeiture, and restitution, usable by any investigation domain. Local implementation of the CASE stub-namespace proposals ([CASE #192](https://github.com/casework/CASE/issues/192), `caseIdentifier` from [#191](https://github.com/casework/CASE/issues/191)). Grounded in *U.S. v. Perry & O'Dell* (W.D. Mo. `2:22-cr-04065-BCW`, 45-count militia conspiracy). Multi-language package scaffolds in `packages/case-uco-legalproc/`.
- **`rico`** — racketeering and criminal enterprise (`extensions/rico/`): `RacketeeringEnterprise` (subclass of `uco-identity:Organization` with § 1961(4) `enterpriseType`), `EnterpriseRole` (subclass of `uco-role:Role` with `roleFunction`), and repeatable `predicateStatute` for § 1961(1) categories. Grounded in *U.S. v. Lam et al.* (D.D.C. `1:24-cr-00417-CKK`, the "SE Enterprise" $245M crypto-theft RICO conspiracy). Package scaffolds in `packages/case-uco-rico/`.
- **`weapons`** — weapons and firearms evidence (`extensions/weapons/`): `Weapon`/`Firearm`/`Handgun`/`LongGun`/`Rifle`/`Shotgun`/`CuttingWeapon`/`Ammunition` class tree mirroring the Common Core Ontologies Artifact Ontology, NIEM-aligned properties (make, model, caliber, serial number, obliterated-serial flag), with CCO and gUFO bridge profiles. Grounded in *U.S. v. Lindell et al.* (D.N.D. `3:25-cr-00005`).
- **`drugs`** — controlled substances (`extensions/drugs/`): `ControlledSubstance` portions with ChEBI chemical identity by IRI reference, CSA schedule, mass, purity, mixture-vs-actual basis (USSG § 2D1.1), and verbatim charged quantity; gUFO bridge grounds portions as `gufo:Quantity`. Same grounding case as `weapons`.
- **`attack-technique`** — forward-implementation of the `uco-action:Technique` metaclass (`extensions/attack-technique/`), reproducing [UCO PR #676](https://github.com/ucoProject/UCO/pull/676) feature-branch definitions verbatim in released `uco-core:`/`uco-action:` IRIs so CTI graphs can carry MITRE ATT&CK technique mappings today; includes a MITRE ATT&CK technique catalog (`mitre-attack-catalog.ttl`). Retires automatically when UCO 1.5.0 lands.
- All five prosecution-grounded extensions pass the CDO Community Playground test suite; each ships OWL, SHACL shapes, validated exemplar, `_registry.json`, and manifest.
- CAC local pending declarations (`extensions/cac/local/cacontology-sdk-pending.ttl`), mirroring filed CAC-Ontology proposals #36/#40/#41 so strict concept coverage passes while upstream adoption is pending; registered in the CAC manifest and validation subset.

#### MCP server

- `route_investigation_content` tool (`mcp_server/investigation_router.py`) — general entry point that classifies **any** investigation submission (warrant returns, legal filings, case files, extraction reports, free text) into investigation families and returns per-family recipes, extension ontologies to enable, core namespaces, and applicable CDO profiles; falls back to extension-gap guidance (search → profiles → proposals → local extension → recipe authoring) for previously unseen data types. Tests in `mcp_server/tests/test_investigation_router.py`.
- Strict closed-world concept coverage in `validate_graph` (`mcp_server/concept_coverage.py`, `strict_concepts=True` by default): every class/property IRI in a graph must be declared in CASE/UCO, a supported extension, or a profiled upper ontology (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG); undeclared concepts force `conforms=False` with `undeclared_concepts` and `concept_guidance` in the report. Tests in `mcp_server/tests/test_concept_coverage.py`.
- `validate_graph` extension manifests: `extensions=['cryptoinv']` and `extensions=['legalproc']` join the existing `cac`/`cac:full` options.
- PACER semantic mapping in `document_semantic_mapping.py`: ECF case numbers, docket filing events, and indictment count references are mapped to typed graph nodes with anchors; regression tests extended.
- `pacer-document-ingestion` CAC routing family with layer-3 modeling checklists (one investigation per docket, etc.) in `cac_content_router.py`; router tests extended.
- Recipe catalog integrity tests (`mcp_server/tests/test_recipe_catalog.py`) and shared pytest fixtures (`mcp_server/tests/conftest.py`).

#### Recipes (10 new; `docs/recipes/INDEX.md` catalogs 68)

- PACER Document Ingestion agent workflow (`cac-pacer-document-ingestion.md`): `process_document_file` → `route_investigation_content`/`route_cac_content` → build script → `validate_graph`.
- Legal Process Modeling (`legal-process-modeling.md`), Racketeering / RICO (`racketeering-enterprise.md`), Weapons and Drug Evidence (`weapons-drug-evidence.md`), Elder Fraud and Government-Impersonation (`elder-fraud-impersonation.md`), Espionage Act and Classified-Information Disclosure (`espionage-classified-disclosure.md`), Export Control and Sanctions Evasion (`export-control-sanctions.md`), Insider Threat and Trade Secret Theft (`insider-threat-trade-secrets.md`), Cyber Threat Intelligence and APT Reporting (`cyber-threat-intelligence.md`).
- Recipe authoring guide (`recipe-authoring.md`): how agents write, ground, re-validate, and register new recipes — the router's self-improvement surface.

#### Examples

- Ten new PACER federal-case exemplars under `examples/pacer/` (see `examples/pacer/README.md` catalog), each with agent build script, validated merged graph, and MCP extraction bundles: Anchorage PD ICAC (`anchorage_pd_2022_004`), SE Enterprise RICO (`ddc_2024_cr_00417`), Teixeira Espionage Act (`dma_2023_cr_10159` — first exemplar using `uco-marking` classification banners), Bitfinex crypto laundering (`doj_crypto_2023_239`), elder fraud couriers (`edla_2022_cr_00115`), export control (`ndca_2020_cr_00446`), Google AI insider threat (`ndca_2024_cr_00141`), kidnapping-for-ransom (`ndnd_2025_cr_00005` — first `weapons`/`drugs` exemplars), militia conspiracy (`wdmo_2022_cr_04065`), and murder-for-hire (`wdtn_2023_cr_20121`).
- CTI exemplar `examples/cti/lotus_blossom_2025/`: 278-node validated graph of the Cisco Talos Lotus Blossom / Sagerunex APT report with 24 hashed report graphics, backing the CTI recipe and `attack-technique` extension.

#### Change proposals

- Capability namespace proposal (`change_proposals/capability-namespace.md`) finalized — attribution section (joint effort between Vulnmaster and sbarnum), passing SPARQL competency tests and graph validation recorded — and **submitted upstream as [UCO #682](https://github.com/ucoProject/UCO/issues/682)**.
- Filed upstream: CASE stub-namespace proposals for criminal ([CASE #192](https://github.com/casework/CASE/issues/192)), civil ([CASE #193](https://github.com/casework/CASE/issues/193)), and corporate ([CASE #194](https://github.com/casework/CASE/issues/194)) process and procedure; case-number/related-investigation representation (comment on [CASE #191](https://github.com/casework/CASE/issues/191)); CAC legal-outcomes charging properties ([CAC-Ontology #40](https://github.com/Project-VIC-International/CAC-Ontology/issues/40)) and core case-identification properties ([CAC-Ontology #41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41)); conspiracy-as-property recommendation (comment on CASE #192). Each ships with tested `.jsonld`/`.ttl`/`.sparql` companions passing `make test-proposal`.
- Drafted, not yet filed: racketeering enterprise and enterprise roles (`racketeering-enterprise-and-enterprise-roles.md`, CASE 1.5.0 target).
- `change_proposals/README.md` now tracks filed UCO/CASE/CAC proposals with issue links and local pending-declaration files.

### Changed

- All language package versions synchronized to **1.15.0** (`python/pyproject.toml`, `python/case_uco/__init__.py`, `csharp/CaseUco/CaseUco.csproj`, `java/pom.xml`, `rust/Cargo.toml`, README header and version matrix).
- `uploads/` (local document staging / OCR intermediates) and PACER source PDFs under `examples/pacer/` are excluded from the repository via `.gitignore`; extracted text, extraction bundles, and validated graphs remain tracked. The C# `packages/` ignore rule was scoped to `csharp/**/packages/` so the new extension package scaffolds under `packages/case-uco-*` are tracked.
- MCP server module docstring and FastMCP instructions rewritten to describe the server's full capability surface (ontology discovery, recipes/mapping guidance, content routing, document processing, validation, change proposals, MCP resources, and the full loadable-extension list) instead of only ontology discovery (`mcp_server/server.py`).
- `UCO #675` proposal (`cryptocurrency-address-and-sanctions-designation.md`) retitled to *Cryptocurrency Address and Transaction Representation*; sanctions coverage removed per ontology committee feedback, to be re-proposed against CASE.
- `ontology/UCO` submodule updated `8335d32` → `748aea0` (upstream master, PR #661 merge).
- ~30 existing recipes gained "Related" cross-link sections connecting starter kits, device, messaging, and CAC recipes into a navigable graph.
- `docs/ECOSYSTEM.md` documents the five new bundled extensions with grounding cases; `mcp_server/README.md` tool tables updated.
- `domain_index.py`: new task templates for cryptocurrency/financial-crime and violent-crime/criminal-prosecution modeling; recipe index entries for all ten new recipes.
- Dependency updates: rust `uuid` 1.23.3 → 1.23.4 (#46), `Microsoft.NET.Test.Sdk` 18.6.0 → 18.7.0 (#45), `actions/checkout` 6 → 7 (#44).

### Fixed

- `check_existing_proposals` now uses `urllib.parse.quote` instead of `urllib.request.quote` (the latter only works via an incidental re-export) and `urllib.parse` is imported explicitly (`mcp_server/server.py`).
- Seven static type errors in `mcp_server/server.py` and `mcp_server/domain_index.py`: `validate_graph` result dict annotated `dict[str, Any]`, and `DOMAIN_CATEGORIES`/`UCO_PROFILES` annotations widened to match their heterogeneous entries (keywords lists, nested compatibility dicts).

## [1.14.0] - 2026-06-23

### Added

- Fraud / crypto / laundering investigation recipe (`docs/recipes/fraud-crypto-laundering.md`): messaging coercion, blockchain trace actions, exchange subpoena returns, wallet hops, and location correlation with validation SPARQL and anti-patterns (closes #37).
- Cargo theft / route staging / warehouse movement recipe (`docs/recipes/cargo-theft-route-staging.md`): geofence deviation events, manifest handling, planning chats, and warehouse search workflows (closes #39).
- Document semantic mapping extensions for fraud-crypto markdown sources (`mcp_server/document_semantic_mapping.py`; closes #41):
  - Chat-log speaker lines (`Display Name (@handle):`) → `Person` plus `InstantMessagingAddress` with `InstantMessagingAddressFacet`
  - Markdown table value cells (including `aka "alias"` parsing) for role-labeled rows
  - Exchange account-holder prose (`Account holder:`, `Registered user:`)
  - Expanded role-table labels (`Account Holder`, `Exchange User`, `Registered User`)
  - Tier T0 regression fixtures in `mcp_server/tests/test_document_semantic_mapping.py`
- Markdown table canonical output (`kind: table`) in `extract_markdown_content` when pipe-style tables are present; `table_sheet_count` recorded in extraction summary fields (`mcp_server/document_processor.py`).
- PACER-derived CAC federal case exemplars under `examples/pacer/` — each folder includes a validated hand-built JSON-LD graph, MCP extraction bundle (`case-uco-mcp-output.jsonld`, `extracted-content.json`, `annotations.jsonld`), extracted text, and a build script that runs CAC subset validation via `validate_graph`:
  - **U.S. v. Gastelo** (`examples/pacer/doj_ceos_2025_014/`): E.D. Cal. `1:20-cr-00252-JLT-BAM`, Doc 107 government trial brief — federal trial proceedings, prosecution relationships, grooming chat modeling, production case, and CSAM forensic provenance recipes; per-victim conduct events, Grindr/Kik/Snapchat platform accounts, anticipated witness testimony, Rule 404(b) evidentiary framing, and separate plea-agreement MCP extraction bundle
  - **U.S. v. Hounsell** (`examples/pacer/doj_ceos_2026_012/`): E.D. Wis. `1:25-cr-00069-WCG`, Doc 34 AO 245B sentencing judgment — legal sentencing outcomes and post-plea federal prosecution wiring; prison term, supervised-release conditions (SORNA, sex-offender treatment, computer monitoring), and monetary assessments
  - **U.S. v. Saucedo** (`examples/pacer/usss_2017_006/`): S.D. Cal. `3:17-cr-00095-JLS`, Doc 1 criminal complaint — ECWG/ICAC multi-jurisdiction task-force referral from Calgary, fabricated Kik persona grooming, per-victim CSAM conduct events, IP/account correlation actions, and non-graphic CSAM artifact summaries from complaint tables

### Changed

- All language package versions synchronized to **1.14.0** (`python/pyproject.toml`, `python/case_uco/__init__.py`, `csharp/CaseUco/CaseUco.csproj`, `java/pom.xml`, `rust/Cargo.toml`, README version matrix) — fixes stale `1.9.0` metadata on current release tags (closes #35).
- Java `central-publishing-maven-plugin` bumped to **0.11.0** (incorporates [PR #36](https://github.com/vulnmaster/CASE-UCO-SDK/pull/36)).
- `docs/recipes/INDEX.md` catalogs 58 recipes; MCP `RECIPE_INDEX` and `TASK_TO_CLASSES` updated for fraud-crypto and cargo-theft domains.
- README header, Java dependency snippet, and version compatibility matrix updated to **1.14.0**.

## [1.13.4] - 2026-06-22

### Added

- Markdown document processing in `document_processor_cli` (`--file-kind markdown`) with warrant-oriented `return_kinds` filtering and extraction bundle output aligned with Link-Look document review.
- Semantic entity extraction for investigation markdown: US street addresses, bold/table person names, Telegram `@handle`, ETH/Tron wallet addresses, and `.example.invalid`-style domains; regression test `test_semantic_mapping_extracts_warrant_markdown_anchors`.

### Changed

- Tightened markdown `Location` heuristics with locality stopword filtering so legal boilerplate (`IN THE UNITED STATES`, `in the Matter`) no longer produces bogus location entities.

## [1.13.3] - 2026-06-17

### Added

- Federal trial proceedings recipe (`docs/recipes/cac-federal-trial-proceedings.md`): superseding indictment chains, PACER docket milestone events, competency/detention proceedings, government trial briefs, and anticipated per-victim evidence wiring.
- Solo-operator § 1591 federal child sex trafficking guidance in `cac-trafficking-recruitment-network.md`: per-victim charge bundles (`VICTIM_COUNTS`), `DigitalToPhysicalBridge` (Grindr), `VictimTransportation`, stacked statute-per-encounter patterns, and distinction from multi-trafficker ring cases.
- Validated reference exemplar `examples/hawaii-riley-trafficking-2023-example.jsonld` (U.S. v. Riley, D. Hawaii `1:23-cr-00071-JMS`): 12-count superseding indictment, five minor victims, prosecution relationship edges, per-victim conduct event subgraphs, and explicit action/event modeling.
- MCP `federal-trial-proceedings` domain family and six new checklist items: `per-victim-charge-bundles`, `trafficking-conduct-charge-bridge`, `stacked-statute-per-encounter`, `superseding-indictment-chain`, `trial-brief-anticipated-evidence`, and `docket-procedural-milestones`.
- CAC content router test for Hawaii solo-operator trafficking narrative (`mcp_server/tests/test_cac_content_router.py`).

### Changed

- `examples/hawaii-riley-trafficking-2023-example.jsonld` refactored per external review: explicit `RecordingAction`/`CommercialSexualExploitation`/`GroomingSolicitation` events with `uco-action:performer`/`object`/`instrument`/`location`; parallel incident nodes for MV1–MV5; `PrimaryTraffickerRole` + `controlsVictim`; `LegalEvent` competency hearing; `ProvenanceRecord` on source documents; `OnlineDatingPlatform` for Grindr; `EquipmentSeizureAction` and `EvidenceReviewAction` for device 1B10; prosecution phase `hasPhaseBeginPoint`; MV2 `precedes`/`part_of` event chain; Count 12 linked to CSAM incidents; trial brief linked to all victims.
- `cac-trafficking-recruitment-network.md` extended with conduct-as-event modeling guidance, anti-patterns, and reference to the Hawaii exemplar.
- `cac-federal-prosecution-relationships.md` extended with `VICTIM_COUNTS` fact-file template, superseding indictment checklist rows, grouped forfeiture notice guidance, and charge→conduct event wiring anti-patterns.
- `cac-federal-trial-proceedings.md` anti-patterns extended for `LegalEvent` competency modeling, prosecution phase timestamps, and provenance on docket source documents.
- `cac-trafficking-recruitment-network.md` keyword routing expanded for § 1591, Grindr, commercial sex act, rideshare transport, and minor victim bundles; related recipes now include federal prosecution and trial proceedings.
- `cac-legal-sentencing-outcomes.md` cross-links federal trial proceedings and solo-operator trafficking recipes.
- `docs/recipes/INDEX.md` catalogs 56 recipes (added Federal Trial Proceedings).

## [1.13.2] - 2026-06-16

### Added

- Federal prosecution recipe extensions for complex indictment patterns from real PACER enterprise and sextortion cases: **enterprise Count 1 overt-act/violation matrix** (per-violation defendant subsets and venues), **intra-case per-count venue** `Location` nodes, **enumerated forfeiture with serial numbers**, and multi-defendant `DEFENDANT_COUNTS` examples showing per-count subsets (`docs/recipes/cac-federal-prosecution-relationships.md`).
- Layer 3 federal prosecution bridge in `cac-sextortion-coercion.md`: cyberstalking (§ 2261A), aggravated identity theft (§ 1028A), wire fraud (§ 1343) charge stacking, extradition chain, platform affordance/ban-evasion modeling, co-conspirator narrative wiring, and sextortion fact-file template.
- Six new MCP modeling checklist items: `enterprise-overt-act-violations`, `charge-venue-locations`, `transnational-extradition-chain`, and `financial-charge-stacking` (federal prosecution); `sextortion-federal-prosecution-bridge` and `platform-affordance-abuse` (sextortion).
- CAC content router tests for enterprise overt-act and sextortion federal-stacking narratives (`mcp_server/tests/test_cac_content_router.py`).

### Changed

- `cac_content_router.py` keyword routing expanded for overt acts, judicial venues, serial-number forfeiture, cyberstalking, wire fraud, identity theft, extradition, ban evasion, and platform names; `sextortion-coercion` domain now links to federal prosecution and international coordination recipes.
- `defendant-charge-matrix` checklist text clarifies that count subsets vary per defendant in multi-defendant indictments.

## [1.13.1] - 2026-06-16

### Added

- Federal prosecution relationship recipe (`docs/recipes/cac-federal-prosecution-relationships.md`): relationship-completeness guidance for federal court prosecution graphs — defendant→count `chargedWith`, indictment→charge links, prosecution→indictment bridges, multi-district parallel prosecution, production equipment, and forfeiture→device wiring. Includes fact-file templates (`DEFENDANT_COUNTS`, `PARALLEL_CASES`, `FORFEITURE_DEVICES`) and enterprise addendum for § 2252A(g) relators.
- MCP `federal-prosecution-relationships` domain family in `cac_content_router.py` with expanded keyword routing (multi-district, CSAM production/possession/transport, forfeiture) and seven relationship checklist items: `defendant-charge-matrix`, `indictment-charge-links`, `prosecution-indictment-link`, `investigation-legal-scope`, `multi-district-charge-jurisdiction`, `forfeiture-device-linkage`, and `enterprise-indictment-bridge`.
- CAC content router tests for federal enterprise and multi-district production prosecution narratives (`mcp_server/tests/test_cac_content_router.py`).

### Changed

- `docs/recipes/INDEX.md` now catalogs all 55 recipe files (alphabetized CAC section, fixed `cac-grooming-chat-modeling.md` link). Grooming recipe path corrected from obsolete `grooming-chat-modeling.md` across MCP router, domain index, and cross-recipe references.
- `cac-production-case.md` expanded with federal filing cross-links, `MobileRecordingDevice` forfeiture patterns, and `relatedCriminalCharges` on `AssetForfeitureAction`.
- `cac-legal-sentencing-outcomes.md` now points federal indictment graphs to the prosecution-relationships recipe.
- `charge-offense-links` modeling checklist now requires `chargedWith` on every defendant, not only the principal suspect.
- `production-case` domain keywords and `domain_index` recipe catalog updated for federal CSAM production filing narratives.

## [1.13.0] - 2026-06-15

### Added

- Document processor semantic mapping stage (tool 0.5.0): after text extraction, `document_semantic_mapping.py` maps bounded high-confidence spans in canonical document text to verified CASE/UCO classes (Person, Location, Organization, Event, EmailAddress, PhoneAccount, URL, and monetary references) with `TextPositionSelector` anchors for the Spec026 extraction bundle. Typed graph nodes use class-appropriate facets and properties; full extracted text is retained on the source upload node's `ExtractedStringsFacet`; charge/arrest narrative windows become `uco-core:Event` nodes with `eventContext` links to other mapped entities. Pattern mapping is deterministic and offline-safe (no LLM). Tests in `mcp_server/tests/test_document_semantic_mapping.py` and updated bundle tests in `mcp_server/tests/test_document_processor.py`.

- Document processor PDF extraction ladder (tool 0.4.0): `pdftotext` (poppler) → `pypdf` → built-in literal-string scrape gated by a readability check → OCR fallback for scanned/image-only PDFs (`pdftoppm` page render, or `pypdf` embedded-image extraction when poppler is absent, then `tesseract`, bounded to 25 pages). The previous Latin-1 literal-string scrape showed glyph-index mojibake to reviewers for subset-font PDFs and produced nothing for scanned PDFs; mojibake is now structurally refused (`text_looks_readable` gate applies to the untrusted scrape only) with a new typed `pdf_text_unreadable` error, and `pdf_text_missing` keeps meaning scanned/no-text-layer with OCR tooling absent. `extraction_method` (`pdftotext`/`pypdf`/`literal_strings`/`ocr_tesseract`) is recorded in extracted summary fields for provenance. All optional dependencies (`poppler-utils`, `pypdf`, `tesseract`) are detected at runtime and their absence fails honestly (`mcp_server/document_processor.py`; ladder, gate, and honest-failure tests in `mcp_server/tests/test_document_processor.py`).
- `pypdf` added to `mcp_server/requirements.txt` as the pure-Python, offline-safe PDF extraction fallback.
- MCP server `validate_graph` tool: wraps the local CASE Utilities `case_validate` SHACL validator for produced JSON-LD/Turtle graph files and returns a bounded conformance report (`conforms`, `warning_count`, `violation_count`, `safe_summary`); fails honestly with typed errors (`validator_unavailable`, `graph_missing`, `unsupported_graph_extension`, `graph_oversized`, `validation_timeout`) and never fabricates a passing result (`mcp_server/graph_validator.py`, tests in `mcp_server/tests/test_graph_validator.py`).
- MCP server README: `process_document_file`/`validate_graph` tool table entries and a "Running under Hermes Agent" deployment section with stdio config example and law-enforcement egress posture notes (supports Link-Look Spec025 agent-teaming planning).
- Document processor extraction breadth with honest failure modes (Link-Look #103): real PDF text extraction (pypdf), OCR for receipt/scan images when an OCR engine is present (typed `ocr_unavailable` otherwise), per-record CSV row nodes, and real DOCX/XLSX extraction in `mcp_server/document_processor.py`; pytest coverage per document kind and per failure mode in `mcp_server/tests/test_document_processor.py`.

### Changed

- Canonical reviewable document text (PDF/Office/image OCR) is now bounded by `MAX_DOCUMENT_TEXT` (100,000 chars, line breaks preserved, same printable/number-redaction cleaning) instead of being truncated to the 500-char summary bound — full reports are reviewable in extraction-bundle consumers while summary fields stay tightly bounded (`sanitize_document_text` in `mcp_server/document_processor.py`).

- Document processor extraction bundle (Link-Look Spec026 contract 1.0): `process_document_file` now writes `extracted-content.json` (canonical extracted content — text sections or table model — with `content_sha256`, tool identity, and typed `failures[]`) and `annotations.jsonld` (W3C Web Annotation companion graph anchoring each extracted-record case-graph node into the content via `TextPositionSelector`+`TextQuoteSelector` for text kinds and RFC 7111 `FragmentSelector` row selectors for tabular kinds) beside the existing `case-uco-mcp-output.jsonld`. Anchors are never fabricated: unanchorable nodes are simply absent. Repeated identical values get distinct per-occurrence anchors. The case graph vocabulary is unchanged. CLI JSON output gains additive `extracted_content_path`/`annotations_path` keys; tool version bumped to 0.3.0 (`mcp_server/document_processor.py`, bundle contract tests in `mcp_server/tests/test_document_processor.py`).

- Document processor output now uses canonical CASE/UCO terms instead of invented predicates (Link-Look #102; every term verified via the registry tools, output passes `validate_graph` with zero `NonExistentCDOConceptWarning`s): `uco-action:object`/`instrument`/`result`/`startTime`/`endTime` on `case-investigation:InvestigativeAction` (replacing ad-hoc `case-investigation:*` action properties), `uco-observable:FileFacet` (fileName/extension/sizeInBytes) plus `uco-observable:ContentDataFacet` with `uco-types:Hash` (SHA256, hexBinary) replacing `link-look:*` vocabulary, `uco-tool:version`, `uco-observable:ExtractedStringsFacet`/`ExtractedString` per extracted record, and directional `uco-core:Relationship` `Derived_From` edges. Consumers parsing the previous ad-hoc predicates must migrate (Link-Look migrated in Spec025 T007/T009).
- CAC content routing for Hermes/Link-Look: `route_cac_content` and `get_recipes` MCP tools, `cac_content_router.py` multi-recipe domain detection, `modeling_checklist` completeness guidance, and CAC press-release validation subset (`extensions/cac/validation-subset.json`) with `validate_graph(..., extensions=['cac'])` defaulting to subset mode (`cac:full` for full manifest).
- Twelve CAC recipe family markdown files (`docs/recipes/cac-*.md`), ICAC search-warrant-arrest press-release recipe, Maryland ICAC Annapolis exemplar graph (`examples/maryland-icac-annapolis-arrest-2025.jsonld`), and `pyrightconfig.json` for IDE resolution of the local `python/case_uco` package.
- CAC Ontology submodule (`extensions/cac/ontology`) updated to `ce95084` (upstream [CAC-Ontology#30](https://github.com/Project-VIC-International/CAC-Ontology/pull/30) on `main`, atop v3.0.0) so v1.13.0 checkouts include ontology files for CAC validation and the resolved Python CodeQL warnings in demonstration/test scripts.

### Fixed

- Resolved eight open CodeQL findings in `mcp_server/`: implicit string concatenation in `cac_content_router.py` modeling steps, duplicate `import`/`from` patterns in document-processor and graph-validator tests, unused local in CSV bundle test, and a `document_processor` ↔ `document_semantic_mapping` import cycle by extracting shared `ExtractedRecord` into `document_models.py`.
- `graph_validator.extension_ontology_args()` now omits `--inference rdfs` whenever a CAC `validation-subset.json` is configured (even before submodule ontology files are present on disk); CAC validator tests skip cleanly when the CAC ontology submodule is uninitialized ([#34](https://github.com/vulnmaster/CASE-UCO-SDK/issues/34)).
- Python packaging: added `python/README.md`, explicit `[tool.setuptools]` package discovery (`where = ["."]`), and `setuptools>=69` so `pip install ./python` builds `case-uco` instead of `UNKNOWN-0.0.0` and editable installs work on PEP 660-capable pip/setuptools ([#33](https://github.com/vulnmaster/CASE-UCO-SDK/issues/33)).
- CAC Ontology submodule Python CodeQL alerts (unused imports/locals, `exit()` usage in demonstration scripts) resolved by pinning `extensions/cac/ontology` to upstream `ce95084` ([#30](https://github.com/Project-VIC-International/CAC-Ontology/pull/30)).

## [1.12.0] - 2026-06-10

### Changed

- Release workflow now pulls GitHub Release notes directly from the matching `CHANGELOG.md` section instead of using generic generated notes.
- Package-registry publishing jobs in the release workflow are gated behind the `PUBLISH_PACKAGES` repository variable so tagged releases can build and attest artifacts without requiring all registry credentials to be enabled.
- CodeQL scans now ignore the external Adversary Engagement Ontology submodule path; that upstream repository is not owned by this SDK and cannot be remediated from here.

### Fixed

- Restored Python registry compatibility with current `mypy` by removing stale `type: ignore` comments and typing extension entry-point discovery without the unused `_EXTENSIONS_LOADED` global.
- Replaced silent MCP extension registry entry-point discovery failures with typed best-effort handling and debug logging.
- Updated the CAC Ontology submodule to include upstream Python CodeQL cleanup for unused imports, unused demonstration locals, and `exit()` usage in validation scripts.
- Resolved all open GitHub code scanning alerts for the SDK repository.

### Dependencies

- Bump `actions/dependency-review-action` from 4 to 5.
- Bump `Microsoft.NET.Test.Sdk` from 18.4.0 to 18.6.0 in `/csharp`.
- Bump `uuid` from 1.23.1 to 1.23.3 in `/rust`.
- Bump `serde_json` from 1.0.149 to 1.0.150 in `/rust`.

## [1.11.0] - 2026-04-25

### Added

- Extension plugin architecture with `manifest.json` schema (`extensions/manifest-schema.json`) for declaring extension ontology metadata, namespaces, CDO Shapes compatibility, and version constraints
- CAC Ontology (v3.0.0) extension: git submodule, manifest, README, and integration with generator/MCP
- Adversary Engagement Ontology (v0.2.1) extension: git submodule, manifest, README, and integration with generator/MCP
- `case-uco-generate generate-extension` CLI subcommand for producing publishable extension binding packages (Python, C#, Java, Rust) with package manifests, multi-module code, and `_registry.json`
- MCP server `CASE_UCO_EXTENSIONS` environment variable for opt-in extension class loading
- `scope` parameter on `search_classes`, `get_class_details`, `find_classes_for_domain`, and `list_all_facets` MCP tools for filtering by `"core"`, extension name, or `"all"`
- CDO Shapes profile compatibility annotations per extension in `get_uco_profiles` results
- Python entry-point-based extension auto-discovery in `case_uco.registry` (group `case_uco.extensions`)
- Per-extension Makefile validation targets (`test-ext-cac`, `test-ext-aeo`, `validate-extension`, `generate-ext`)
- Manifest-driven validation helper script (`scripts/validate_extension.py`)
- Cross-domain extension usage recipe (`docs/recipes/cross-domain-extensions.md`)
- Extension Packages section in ECOSYSTEM.md with installation guide and CDO Shapes compatibility matrix

### Changed

- `load_extensions()` in generator now reads `manifest.json` when present instead of heuristic namespace detection; falls back to legacy behavior for directories without manifests
- CDO Shapes profile URLs corrected from `ucoProject/UCO-Profile-*` to `Cyber-Domain-Ontology/CDO-Shapes-*` in `domain_index.py` and `docs/ECOSYSTEM.md`
- `_classify_module()` now returns `None` for external/foundational ontology IRIs (gUFO, BFO, PROV-O, etc.) to skip code generation for those namespaces
- `IGNORE_NS` in `scaffold.py` expanded with gUFO, BFO, and related foundational ontology domains

### Fixed

- **CAC extension registry coverage** — `extensions/cac/_registry.json` previously indexed only 9 of 47 ontology modules (~80 of 1,993 OWL classes), silently missing entire domains: `cacontology-sex-trafficking`, `recruitment-networks`, `tactical`, `victim-impact`, `legal-outcomes`, `multi-jurisdiction`, `asset-forfeiture`, `analyst-wellbeing`, `educational-exploitation`, `physical-evidence`, `custodial`, `temporal`, `prevention`, `training`, `synthesis`, `bridge-case`, `bridge-uco`, `bridge-gufo`, `integration-patterns`, and others. Agents and SDKs relying on `search_classes` / `find_classes_for_domain` were therefore blind to ~81% of the CAC vocabulary.
  - `extensions/cac/manifest.json` — corrected several namespace URIs that did not match the IRIs declared in the upstream TTL submodule (e.g., `cacontology-sex-trafficking` was mapped to a non-existent `/sex-trafficking#` IRI; the actual TTL uses `/trafficking#`). Added explicit entries for all 47 modules including bridge ontologies.
  - `generator/src/case_uco_generator/ontology_parser.py` — added a second SPARQL pass (`ALL_CLASSES_QUERY`) that selects every `owl:Class` regardless of whether a `sh:NodeShape` targets it. T-Box-only classes (no SHACL shape) are now indexed without enforced property cardinalities; previously they were dropped entirely.
  - `generator/src/case_uco_generator/ontology_parser.py` — extension manifest loader now stores the full manifest prefix (e.g., `cacontology-sex-trafficking`) as the canonical module identifier so MCP search results and registry entries match the upstream namespace convention.
  - `generator/src/case_uco_generator/cli.py` — added `_sanitize_module_id()` helper that converts hyphenated manifest prefixes to language-safe identifiers (e.g., `cacontology_sex_trafficking`) when generating Python/C#/Java/Rust file paths and module names. The registry retains the original hyphenated prefix for human-friendly search.
  - `generator/src/case_uco_generator/cli.py` — `_emit_extension_registry` now emits the manifest prefix as the `module` field instead of the internal `ext.<name>.<prefix>` key, making the registry directly usable for documentation and search.
  - `extensions/cac/_registry.json` — regenerated; now contains 47 modules and 1,993 classes (was 9 modules / ~80 classes).
- **CAC domain-keyword coverage in `find_classes_for_domain` / `guide_mapping`** — even with the registry restored, several high-value query terms (`trafficking`, `recruitment`, `rescue`, `multi-jurisdiction`, `tactical arrest`, `csam provenance`, `task force`, `asset forfeiture`, `undercover`, `recantation`) returned no useful results because the keyword maps that back those tools were grooming/CSAM-only.
  - `mcp_server/domain_index.py` — added five new `DOMAIN_CATEGORIES` (`child_trafficking`, `victim_rescue_response`, `multi_jurisdictional_operations`, `tactical_operations`, `csam_provenance`) and expanded the existing `child_exploitation` keywords with `icac` and `crimes against children`.
  - `mcp_server/domain_index.py` — added five new `TASK_TO_CLASSES` templates (trafficking ring/recruitment network, multi-jurisdictional task force / rescue, tactical arrest / high-risk operation, victim rescue extraction and post-rescue services, CSAM provenance forensics and victim identification). Each template lists 11–20 concrete CAC classes with usage roles. All class references were validated against the registry.
  - `mcp_server/domain_index.py` — added five new `MAPPING_GUIDE_INDEX` entries (same five sources) with patterns, anti-patterns, and runnable code skeletons so `guide_mapping` returns `found=True` for these evidence sources.
  - `mcp_server/server.py` — expanded the `cac_keywords` set in `find_classes_for_domain` and the `cac_concepts` set in `suggest_classes_for_input` so the proactive CAC extension hint fires for the new query vocabulary; expanded the `relevant_modules` list returned in the extension suggestion to surface the now-discoverable modules (sex-trafficking, recruitment-networks, street-recruitment, multi-jurisdiction, tactical, undercover, taskforce, asset-forfeiture, victim-impact, recantation, legal-outcomes/legal-harmonization).

### Dependencies

- Bump `org.apache.maven.plugins:maven-javadoc-plugin` from 3.11.2 to 3.12.0 in `/java`
- Bump `org.apache.maven.plugins:maven-source-plugin` from 3.3.1 to 3.4.0 in `/java`
- Bump `actions/attest-build-provenance` from 2 to 4
- Bump `org.sonatype.central:central-publishing-maven-plugin` from 0.7.0 to 0.10.0 in `/java`
- Bump `org.apache.maven.plugins:maven-gpg-plugin` from 3.2.7 to 3.2.8 in `/java`
- Bump `Microsoft.NET.Test.Sdk` from 18.3.0 to 18.4.0
- Bump `softprops/action-gh-release` from 2 to 3 (Node 24 runtime)
- Bump `uuid` from 1.23.0 to 1.23.1 in `/rust`

## [1.10.0] - 2026-04-02

### Added

#### Windows USN Journal Recipe

- **`docs/recipes/usn-journal.md`** — new recipe for modeling Windows NTFS
  Update Sequence Number (USN) Change Journal entries. Covers structured
  reason flags, rename before/after modeling, directory hierarchy, and
  forensic provenance. Demonstrates the two-layer event model pattern:
  `ObservableObject` + `EventRecordFacet` for the raw artifact, and
  `core:Event` with structured `eventType` flags for queryable semantics.
  Includes a common USN reason flags reference table, SHACL validation
  notes for dictionary key uniqueness, and a "Known limitations" section
  documenting relationship vocabulary, string-typed dictionary values,
  and file identity vs. temporal state trade-offs.

#### USN Journal Example

- **`example_agentmcp_outputs/usn_journal_example.py`** and
  **`example_agentmcp_outputs/usn_journal.jsonld`** — complete worked
  example modeling four USN Journal entries (file create, data modify,
  rename, delete) with:
  - Structured `Event.eventType` reason flags (queryable via SPARQL)
  - `Dictionary`/`DictionaryEntry` metadata with unique keys per flag
  - Rename modeled as two `ObservableObject` nodes linked by
    `Renamed_From` relationship (same MFT entry ID, different names)
  - Full directory hierarchy: `C:` → `Users` → `analyst` → `Documents`,
    `C:` → `ProgramData` → `AppConfig`, etc. (no flattened paths)
  - Explicit provenance chain: `Investigation` →(`object`)→
    `InvestigativeAction` →(`result`)→ all 9 parsed outputs (journal +
    4 USN records + 4 Event objects) + `Tool` (MFTECmd) + evidence
    source disk image with SHA256 hash
  - Validated with `case_validate --built-version case-1.4.0`

### Changed

#### Recipe Index

- **`docs/recipes/INDEX.md`** — added Windows USN Journal recipe entry
  in the "Devices, locations, and identity" section

## [1.9.0] - 2026-04-02

### Added

#### AI/ML Analysis Pipeline Recipe

- **`docs/recipes/ai-analysis-pipeline.md`** — new comprehensive recipe for
  modeling AI and machine-learning analysis workflows (image search, object
  detection, content classification, embedding-based retrieval, multi-step
  inference pipelines). Covers seven common modeling mistakes:
  1. Structured facts hidden in JSON description strings
  2. Missing explicit input/output relationships
  3. No per-result ranking or scoring metadata
  4. Multi-step pipelines collapsed into a single action
  5. ArtifactClassification misused for tool endpoint identity
  6. Missing file-level evidence metadata (hashes, sizes, MIME types)
  7. Generic File used for known image formats instead of RasterPicture

#### MCP Server AI/ML Guidance

- **`guide_mapping`** now returns targeted anti-patterns and code skeletons
  when queried about AI, ML, image analysis, semantic search, or inference
  pipeline workflows — 6 anti-patterns covering JSON blob misuse, per-result
  scoring, multi-step pipeline modeling, RasterPicture usage, and evidence
  metadata requirements
- **`RECIPE_INDEX`** — new entry for the AI/ML Analysis Pipeline recipe with
  keywords: ai, ml, machine learning, inference, pipeline, image, search,
  semantic, embedding, clip, model, scoring, ranking, similarity, confidence,
  raster, picture, photo, detection, prediction, neural network
- **`TASK_TO_CLASSES`** — new entry mapping "model AI image analysis or ML
  inference pipeline" to the correct classes (RasterPicture, ConfidenceFacet,
  Relationship, AnalyticTool, etc.)
- **`MAPPING_GUIDE_INDEX`** — new "ai ml image analysis" evidence source
  entry with 6 anti-patterns and a code skeleton
- Updated `actions_and_events` and `tool_information` domain categories with
  AI/ML-related keywords (pipeline, inference, ai, ml, prediction, detection,
  model, analytic, classifier, neural, embedding)

### Changed

#### Context Pruning in Serialized Graphs

- **All four languages** (Python, C#, Java, Rust) — the `@context` section
  of serialized JSON-LD graphs now contains only namespace prefixes that are
  actually used in the `@graph` body. Previously, all 17+ default CASE/UCO
  namespace prefixes were emitted regardless of usage, bloating the context
  with unused entries. The full prefix set is still available internally for
  IRI compaction; only serialization output is pruned.

#### Analysis Recipe Anti-Patterns

- **`docs/recipes/analysis.md`** — added an explicit "Anti-patterns" section
  covering: JSON blobs in description fields, ArtifactClassification misuse
  for tool identity, missing input/output links, and generic File for known
  media types. Added cross-reference to the new AI/ML Analysis Pipeline recipe.

## [1.8.0] - 2026-04-01

### Added

#### Graph Validation Across All Languages

- **`graph.validate()`** (Python), **`graph.ValidateGraph()`** (C#),
  **`graph.validate()`** (Java), **`graph.validate()`** (Rust) — all four
  languages can now validate graphs against CASE/UCO SHACL constraints by
  wrapping `case_validate`. Requires `case-utils` on PATH. The Python
  README documented `graph.validate()` since v1.7.0 but the method was
  never implemented — it now exists and works.

#### Typed Deserialization Parity

- **`CaseGraph.FromJsonLd()`** (C#), **`CaseGraph.fromJsonLd()`** (Java),
  **`CaseGraph::from_jsonld()`** (Rust) — all three languages can now
  deserialize JSON-LD strings back into typed objects, matching the
  existing Python `from_jsonld()`. C# and Java use reflection to match
  `@type` IRIs to generated classes. Rust returns `serde_json::Value`
  objects since it lacks runtime reflection.

#### Prescriptive Registry Guidance

- **`suggest_for_concept()`** — given a natural-language concept (e.g.,
  "file", "email"), returns recommended classes with usage patterns and
  notes. Powered by a curated `_concept_index.json`.
- **`suggest_facets()`** — given a class name, returns commonly paired
  Facet classes for the ObservableObject + Facet pattern.
- **`did_you_mean()`** — fuzzy matching for misspelled or deprecated class
  names (e.g., "Trace" → "ObservableObject").
- **`modeling_warnings()`** — returns modeling warnings for a class (e.g.,
  "This is a Facet — attach it to an ObservableObject, don't use it as a
  top-level graph object").

#### End-to-End Mapping Starter Kits

Four new recipes with complete input-to-output mapping workflows:

- **`starter-filesystem-report.md`** — map a file listing/triage report
  with hashes into ObservableObject + FileFacet + ContentDataFacet
- **`starter-mobile-extraction.md`** — map a mobile extraction with
  device, SIM, app data, and messages
- **`starter-email-export.md`** — map an email export with headers,
  sender/recipient addresses, and attachments
- **`starter-tool-run.md`** — map a forensic tool execution with
  provenance, input/output linkage, and investigation context

Each includes: source input shape, modeling choices, anti-patterns,
complete Python code, expected JSON-LD output, and validation step.

#### MCP Server Mapping Enhancements

- **`guide_mapping`** tool — provides step-by-step mapping guidance for
  a given evidence source (e.g., "UFED CSV export", "Wireshark pcap"),
  returning recommended classes, anti-patterns, a code skeleton, and
  a link to the relevant starter kit recipe
- **`suggest_classes_for_input`** tool — wraps the new prescriptive
  registry functions, returning concept suggestions with per-class
  modeling warnings
- **`get_recipe`** now returns full recipe content (up to 8000 chars)
  inline, so AI agents get code examples in a single tool call instead
  of needing a separate file read
- **`find_classes_for_domain`** now also returns related recipes and
  starter kits alongside class matches, with tips when starter kits
  are available
- Added `MAPPING_GUIDE_INDEX` — 8-entry evidence source → mapping
  strategy index used by `guide_mapping`

#### Docs-as-Tests Infrastructure

- **`scripts/test_doc_snippets.py`** — extracts Python code blocks from
  README.md, MAPPING_GUIDE.md, and all recipe files, compiles them for
  syntax correctness, and reports pass/fail/skip per file
- **`test-docs`** CI job in `ci.yml` — runs the snippet test harness on
  every push and PR, failing if any documented code example has invalid
  syntax
- **`make test-docs`** Makefile target

#### Trusted Publisher Workflows (Pre-Publishing)

- **`publish-pypi`** job — PyPI Trusted Publisher via OIDC (no API keys),
  gated behind a `publish` environment with manual approval
- **`publish-nuget`** job — NuGet push via API key
- **`publish-maven`** job — Maven Central via Central Publishing Portal
  with GPG signing, source/javadoc JARs
- **`publish-crates`** job — crates.io publish via registry token
- All four publish jobs require the `publish` GitHub environment to be
  configured with appropriate secrets before they will run

#### Package Manifest Enrichment

- **Python `pyproject.toml`** — added `readme`, `keywords`, `classifiers`,
  and `[project.urls]` (Homepage, Repository, Documentation, Changelog)
- **Rust `Cargo.toml`** — added `repository`, `homepage`, `readme`,
  `keywords`, `categories`
- **C# `CaseUco.csproj`** — added `RepositoryUrl`, `ProjectUrl`,
  `PackageTags`, `Authors`
- **Java `pom.xml`** — added `<url>`, `<scm>`, `<developers>`, and a
  `release` profile with `maven-source-plugin`, `maven-javadoc-plugin`,
  `maven-gpg-plugin`, and `central-publishing-maven-plugin`

#### CI Improvements

- **Version consistency check** — new `version-sync` CI job verifies
  `python/case_uco/__init__.py __version__` matches `pyproject.toml`
  version on every push and PR, preventing version drift

### Changed

#### Version Bump to 1.8.0

- All four package manifests bumped from 1.7.0 to 1.8.0
- README header, install instructions, and version matrix updated
- CONTRIBUTING.md wheel filename updated
- SECURITY.md supported versions updated to 1.8.x

#### README Install Section

- Package registry install lines (`pip install case-uco`, `dotnet add
  package CaseUco`, `cargo add case-uco`) are now the primary install
  path, no longer hidden behind an HTML comment
- GitHub Release install is now secondary ("Alternatively, install from
  GitHub Release artifacts")
- Version matrix now includes both 1.8.0 and 1.7.0 rows for history

#### Updated Feature Matrix and Parity Contract

- Feature Matrix now shows `FromJsonLd()` / `fromJsonLd()` / `from_jsonld()`
  for C#, Java, and Rust (previously marked "—")
- New "Graph validation (SHACL)" row in Feature Matrix
- `docs/CROSS_LANGUAGE_PARITY.md` updated: Validate row shows all four
  languages; asymmetric features section shows full parity for both
  typed deserialization and graph validation

#### MCP Server Instructions

- Updated FastMCP instructions to mention `guide_mapping` and enhanced
  `get_recipe` behavior
- Updated `.cursor/rules/case-uco-sdk.mdc` to reference `guide_mapping`
  and prescriptive registry functions

### Fixed

- **`__version__` mismatch** — `python/case_uco/__init__.py` was stuck at
  `"0.1.0"` while `pyproject.toml` was at `1.7.0`. Now both are `1.8.0`,
  and a CI check prevents future drift.
- **Rust examples in MAPPING_GUIDE.md** — all 7 Rust code examples built
  a Facet but then called `graph.create(&ObservableObject::default())`
  without attaching the facet. Fixed to use the builder pattern with
  `has_facet(vec![facet])`.
- **SECURITY.md supported versions** — updated from `1.6.x` to `1.8.0`
  (was stale since the 1.6.0 release).

#### Recipe Validation Fixes

All recipe code examples now produce `Conforms: True` from
`case_validate --built-version case-1.4.0`.

- **`starter-filesystem-report.md`**, **`starter-email-export.md`**,
  **`starter-tool-run.md`** — changed `hash_method="SHA-256"` to
  `"SHA256"` per `HashNameVocab` controlled vocabulary
- **`file-system.md`** — three fixes:
  - `ContentDataFacet(hash_method=..., hash_value=...)` replaced with
    `ContentDataFacet(hash=[Hash(...)])` (correct API)
  - `created_time` replaced with `observable_created_time` on `FileFacet`
  - `"SHA-256"` changed to `"SHA256"` per `HashNameVocab`
  - C# and Java code blocks updated to match
- **`change-proposal.md`** — `serial` renamed to `serial_number` on
  `DeviceFacet`; `manufacturer` changed from bare string to `Identity`
  object; `telemetry_data` dict now loaded into graph via `graph.load()`
- **`large-datasets.md`** — second code block fixed: added missing
  imports, replaced `ContentDataFacet(hash_value=...)` with
  `ContentDataFacet(hash=[Hash(...)])`
- **`existence-intervals.md`** — added missing `CASEGraph` and `json`
  imports to gUFO pattern block
- **`mobile-device.md`** — removed `account_type=["email"]` (not in
  `AccountTypeVocab`)

## [1.7.0] - 2026-04-01

### Added

#### Security Policy and Supply-Chain Hardening

- **`SECURITY.md`** — vulnerability reporting policy with private disclosure
  via GitHub Security Advisories, 72-hour acknowledgment SLA, and coordinated
  disclosure process. Documents all security measures (CodeQL, cargo-audit,
  dependency review, Dependabot) and defines scope.

#### Rust Security Scanning

- **`rust-security.yml`** workflow — dedicated CI pipeline for Rust
  supply-chain security, running on push/PR to `main`/`develop` plus weekly
  schedule:
  - `cargo audit` for dependency vulnerability scanning (filling the gap
    left by CodeQL, which does not support Rust)
  - `clippy` with `unwrap_used` and `expect_used` security-focused lints

#### Hardened Release Pipeline

- **`release.yml`** completely rewritten from a simple GitHub Release creator
  to a full build-and-attest pipeline:
  - Builds all four language packages from generated source (Python wheel/sdist,
    C# NuGet, Java JAR, Rust crate)
  - Generates Python SBOM in CycloneDX format via `pip-audit`
  - Produces SHA256 checksums (`SHA256SUMS.txt`) for all release assets
  - Creates SLSA build provenance attestations via
    `actions/attest-build-provenance@v2`
  - Requests `id-token: write` and `attestations: write` permissions for
    OIDC-based trusted provenance
  - Uses a `release` environment for deployment protection rules

#### Change Proposal Improvements (Ontology Committee Feedback)

Based on feedback from the CASE/UCO Ontology Committee, the change
proposal workflow now includes:

- **Target release** — every proposal must specify which CASE/UCO release
  it targets (e.g., 1.5.0, 2.0.0). Added to the template, recipe, and
  MCP tool (`target_release` parameter, defaults to "1.5.0")
- **Example graph generation** — `draft_change_proposal` now generates a
  companion `.jsonld` file alongside the proposal markdown, containing
  the example instance data that the submitter wants to build and share
- **SPARQL query file** — `draft_change_proposal` now generates a companion
  `.sparql` file with the competency queries for automated testing
- **Pre-submission testing** section added to the template requiring
  submitters to report SPARQL test results, graph validation output,
  and any unresolved issues before the proposal goes to manual review
- **`make test-proposal PROPOSAL=<slug>`** — new Makefile target that
  validates the example `.jsonld` graph with `case_validate` and tests
  all SPARQL queries against the example data using RDFLib
- **`make validate-proposal`** and **`make sparql-test-proposal`** —
  individual Makefile targets for running validation or SPARQL tests
  separately
- **Extension compatibility testing** against multiple CASE/UCO branches:
  - `make test-extension-compat` — tests an extension ontology against
    `main` (current stable), `develop` (v1.5.0), and `develop-2.0.0`
    (v2.0.0) branches
  - Individual targets: `test-extension-main`, `test-extension-develop`,
    `test-extension-develop2`
  - This helps ontologists review change proposals by showing
    compatibility across release targets
- Updated `docs/templates/change-proposal-template.md` with Target
  release, Example instance data, and Pre-submission testing sections
- Updated `docs/recipes/change-proposal.md` with new Steps 3 (target
  release selection), 5 (example data), and 6 (test before submission)
- File convention documentation for proposal artifacts: `.md`, `.jsonld`,
  `.sparql`, `.ttl`, `-shapes.ttl`

#### Change Proposal Workflow Hardening

Lessons learned from the first real change proposal
(`change_proposals/cryptocurrency-address-and-sanctions-designation.md`)
drove several improvements to ensure proposals are fully tested before
submission:

- **Testing is now a hard gate** — the recipe and template make clear
  that a proposal is not finished until `make test-proposal` passes and
  the Pre-submission testing section contains actual results (not
  placeholders)
- **`scripts/sparql_test.py`** — extracted SPARQL testing into a
  standalone script, replacing the inline Python in the Makefile that
  broke due to Make tab/space indentation issues. Displays query titles,
  warns on zero-result queries, and exits non-zero on failures
- **`validate-proposal` now passes `--inference rdfs --allow-info`** —
  required for proposals introducing new Facet/UcoObject subclasses
  where SHACL needs to infer class hierarchy, and to allow informational
  UUID IRI suggestions without causing validation failure
- **Extension `.ttl` documented as required (not optional)** for any
  proposal that introduces new Facet or UcoObject subclasses. Without
  it, `case_validate` cannot verify the proposed class satisfies
  `sh:class core:Facet` constraints
- **Facet IRI requirement documented** — SHACL requires
  `sh:nodeKind sh:IRI` for facet objects; blank nodes cause validation
  failure. Recipe now includes the `@id` naming convention
  (`kb:<parent>-facet`)
- **Common validation failures table** added to the recipe covering the
  four most frequent issues: blank-node facets, missing extension `.ttl`,
  missing `--inference rdfs`, and missing `--allow-info`
- **"Related proposals and references"** section added to both the
  template and recipe, ensuring proposals cite related GitHub issues,
  prior proposals, and evaluated external ontologies
- **JSON-LD sync requirement** — recipe now requires the embedded
  JSON-LD in the `.md` to match the tested `.jsonld` file
- **`.cursor/rules/case-uco-sdk.mdc`** updated with expanded change
  proposal steps (6–9): create extension `.ttl`, ensure facet IRIs,
  run `make test-proposal` as a hard gate, and sync `.md` with results

#### UCO Profile Ontology Integration

UCO maintains [Profile repositories](https://cyberdomainontology.org/ontology/development/#profiles)
that align UCO classes with established external ontologies. The SDK now
surfaces all six profiles to developers:

- **New MCP tool `get_uco_profiles()`** — search and browse UCO Profile
  ontologies (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF) with
  descriptions, repo links, related recipes, and integration guidance
- **New MCP resource `case-uco://profiles`** — browsable profile catalog
  for AI agent context
- **`find_classes_for_domain` now returns matching profiles** — when a
  domain query matches a profile's keywords or related domains, the
  response includes `related_profiles` with links and descriptions
- **`UCO_PROFILES` data structure** in `domain_index.py` — complete
  metadata for all six profiles including keywords, related domains,
  related recipes, ontology file names, and profile types (top-level
  vs. adopting)
- **`docs/ECOSYSTEM.md`** — new "UCO Profiles — Interoperability with
  Other Ontologies" section with:
  - Profile table with descriptions and use cases
  - "For Developers Coming from Other Ontologies" cross-reference table
  - SDK integration code example
  - Profile repository structure reference
- **`README.md`** — new "UCO Profiles" subsection in Ecosystem & Tools
  with quick-reference table
- **`docs/MAPPING_GUIDE.md`** — new Tip #8 connecting domain mappings
  to relevant profile ontologies with concrete examples

#### CDO Community Playground Guide Integration

Aligned the SDK's extension authoring workflow with the updated
[CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing):

- **`.cursor/rules/extension-authoring.mdc`** rewritten with Playground
  Guide constraints: T-Box vs. A-Box rules (never `owl:NamedIndividual`
  for schema elements), mandatory subclassing, descriptive documentation,
  `case_validate` flags (`--inference rdfs`, `--allow-info`,
  `--ontology-graph`), CASE-Profile-Example testing workflow, and
  recommended chain of thought for AI agents generating extensions
- **`.cursor/rules/case-uco-sdk.mdc`** updated validation section with
  extension-specific `case_validate` flags and new "Extension Ontology
  Authoring" section summarizing Playground Guide rules
- **`docs/recipes/extensions.md`** expanded with extension file structure
  guidance, critical rules for extension classes, validation examples
  (basic, subclass inference, multiple namespaces), CDO Community
  Playground testing workflow (manual and via `make playground-test`),
  and links to existing community playground extensions
- **`docs/ECOSYSTEM.md`** — new "CDO Community Playground Extensions"
  subsection listing AI-generated CASE and UCO extensions from
  Project VIC International's ICAC taskforce work
- **`make playground-test`** — new Makefile target that clones
  [CASE-Profile-Example](https://github.com/casework/CASE-Profile-Example),
  injects the extension ontology and shapes, and runs `make -j check`
  per the Playground Guide submission requirements

#### Rust Security Lint Fix

- Replaced `.expect()` calls in `rust/src/graph.rs` and
  `rust/src/registry.rs` with `match` + `panic!` to satisfy
  `clippy::expect_used` security lint in the `rust-security` CI workflow

#### Cross-Language Parity Contract

- **`docs/CROSS_LANGUAGE_PARITY.md`** — formal specification of what is
  intentionally identical across all four languages (operation names, registry
  API, JSON-LD output, validation behavior) vs. what is intentionally
  language-idiomatic (object construction, naming conventions). Includes
  stability guarantees and migration guidance.

### Changed

#### Version Alignment

- All four package manifests now track the repository release version:
  - Python `pyproject.toml`: 0.1.0 → 1.7.0
  - Rust `Cargo.toml`: 0.1.0 → 1.7.0
  - Java `pom.xml`: 0.1.0 → 1.7.0
  - C# `CaseUco.csproj`: 0.1.0 → 1.7.0
- Previously, package versions were stuck at 0.1.0 while the repo was at
  v1.6.0, creating a provenance and support-expectation mismatch

#### README Restructured for Consumer vs. Contributor Paths

- **Installation section** split into "Use the SDK (Consumer Install)" and
  "Contribute to the SDK (Developer Install)" — consumers no longer need to
  clone the repo or run the generator
- Added install-from-release-artifact instructions with placeholder for
  future package registry lines (PyPI, NuGet, Maven Central, crates.io)
- Python quickstart example now ends with `graph.validate()` instead of
  just `graph.write()`, making validation part of the default developer path
- Added **Version Matrix** section showing lockstep package versions across
  all four languages and their corresponding ontology versions
- Added **Cross-Language Parity** section linking to the parity contract
- Added **Security** section linking to `SECURITY.md`
- Architecture diagram updated to reflect new files

#### Community Integration (ECOSYSTEM.md and MAPPING_GUIDE.md)

- **CDO Project Release Flow** section in `ECOSYSTEM.md` — documents the
  established community release pipeline (UCO → CASE → case-utils → case-
  validation-action → downstream projects) and positions the SDK within it,
  per guidance from the CASE/UCO Ontology Committee
- **Community Mappings and Implementations** section in `ECOSYSTEM.md` —
  references the full landscape of existing community mapping work:
  - Mapping specifications: CASE-Mappings (SleuthKit, Cellebrite, Bulk
    Extractor, NSRL), CASE-Mapping-Template-Stubs, CASE-Mapping-Template-
    Python, CASE-Mapping-Python (INSPECTr)
  - 10 tool implementation repositories (UFED-XML, ExifTool, AXIOM, XRY,
    DC3DD, GNU-Time, Plaso, Volatility, macOS System Profiler, PROV-O)
  - Templates for new implementations
- **Community Mapping Resources** section in `MAPPING_GUIDE.md` — links the
  auto-generated domain mapping guide to the community's hand-written tool
  mappings, noting the v0.1.0-era terminology differences and the
  complementary relationship between the two

#### CONTRIBUTING.md Reorganized into Three Tracks

- **Track 1: Use the SDK** — for developers who just want to consume the
  package (install, resources, bug reporting)
- **Track 2: Contribute to the SDK** — for developers fixing bugs or adding
  features (setup, project structure, CI checks, code style)
- **Track 3: Extend or Regenerate** — for advanced users adding extension
  ontologies, modifying the generator, or updating ontology versions
- Each track links to the relevant docs without requiring knowledge of the
  other tracks

## [1.6.0] - 2026-03-27

### Added

#### Rust — Required-Field Validation

The Rust library now validates ontology-required fields when adding objects
to a graph via `create()` and `create_with_id()`, matching the existing
behavior in Python, C#, and Java.

- Added `validate()` method to the `CaseObject` trait with a default no-op
  implementation
- Generated structs with required properties now implement `validate()`,
  checking that `Option` fields are `Some` and required `Vec` fields are
  non-empty
- `CaseGraph::create()` and `CaseGraph::create_with_id()` call `validate()`
  before insertion, panicking with a descriptive error if a required field
  is missing
- Updated the Rust code generator (`rust_backend.py`) to emit `validate()`
  implementations based on `prop.cardinality.is_required`
- Updated the Rust exhaustive test to instantiate without adding to graph
  (matching the C# and Java exhaustive test pattern)

#### C# — Static Analysis (Warnings-as-Errors)

- Enabled `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` and
  `<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>` in
  `CaseUco.csproj`, so all Roslyn compiler warnings are treated as
  build-breaking errors
- Added `lint-csharp` Makefile target (`dotnet build /p:TreatWarningsAsErrors=true`)
- Fixed pre-existing CS0108 warning in `ReferenceEqualityComparer.Equals()`
  (missing `new` modifier)

#### Java — Static Analysis (javac -Xlint + -Werror)

- Added `maven-compiler-plugin` configuration with `-Xlint:all,-options`
  and `-Werror`, so all javac warnings (unused imports, unchecked casts,
  deprecations, etc.) are treated as compilation errors
- Added `lint-java` Makefile target (`mvn compile`)
- Updated `pom.xml` to use `maven-compiler-plugin` 3.12.1

### Changed

- The `make lint` target now runs all four linters: mypy (Python),
  dotnet warnings-as-errors (C#), javac -Xlint -Werror (Java), and
  clippy (Rust)

## [1.5.0] - 2026-03-27

### Changed

#### CLI Ontology Explorer — Terminal-Width-Adaptive Output

The `case-uco-explore` CLI now dynamically adjusts table output to fit the
current terminal width, instead of truncating descriptions at a fixed character
limit regardless of available space.

- **`format_class_detail`** property table — the Description column now expands
  to fill remaining terminal width after the Name, Type, Cardinality, and Req
  columns, replacing the previous hard-coded 50-character truncation
- **`format_class_list`** (used by `search`, `module`, and `properties`
  commands) — the Description column similarly expands to fill remaining width
  after the Module and Class columns, replacing the previous 60-character limit
- Both formatters enforce a minimum description width of 20 characters for
  narrow terminals and fall back to 80 columns when terminal size cannot be
  detected (e.g., piped output)
- The `max_desc` parameter remains available for callers who need to override
  automatic width detection

## [1.4.1] - 2026-03-26

### Changed

#### Toolcap Extension v0.3.1 — Semantic Tightening

A cleanup pass focused on semantic precision and validation constraints,
informed by peer review feedback.

- **`owl:imports`** — explicit imports added for `uco-core`, `uco-tool`,
  `uco-observable`, and `case-investigation` modules to improve reasoning,
  validation, and reuse reliability
- **SHACL `sh:or` constraint** on `ToolCapability-Shape` — every
  `ToolCapability` must now declare at least one of `application` (for
  app-level capabilities) or `forensicTaskType` (for CFTT task-level
  capabilities). Prevents underspecified instances with neither property.
- **SHACL SPARQL constraint** on `BenchmarkObservation-Shape` — when
  `submittedCount`, `truePositiveCount`, and `falsePositiveCount` are all
  present, validates that `submittedCount == TP + FP`
- **Clarified metric semantics** in `rdfs:comment` for three properties:
  - `parseSuccess` — now explicitly defines "true = produced usable output"
    vs "false = total failure"; documents expected relationship with other
    metrics when false
  - `completenessScore` — distinguished from `recallScore`: completeness is
    a holistic data recovery measure (including partial records, structural
    integrity), while recall is the strict IR metric `TP / (TP + FN)` based
    on binary item-level matching
  - `accuracyScore` — distinguished from `precisionScore`: accuracy measures
    content-level fidelity of recovered items (timestamps, metadata correct),
    while precision is the strict IR metric `TP / (TP + FP)` measuring what
    fraction of reported items are real
- **Refreshed class comments** on `CapabilityMatrix` and
  `BenchmarkObservation` to reflect the v0.3.0+ scope (forensic tasks, IR
  metrics, benchmark provenance) rather than app-parsing only
- **Version bumped** to `owl:versionIRI toolcap:0.3.1` with
  `owl:priorVersion toolcap:0.3.0`
- All exemplar data validated with `case_validate --built-version case-1.4.0`
  (`Conforms: True`)

## [1.4.0] - 2026-03-26

### Added

#### Toolcap Extension v0.3.0 — NIST CFTT Task-Level Capabilities and IR Metrics

The `extensions/toolcap/` extension ontology has been expanded to support NIST
CFTT-style forensic task benchmarking. Tools can now declare task-level
capabilities (string search, file carving, deleted file recovery, Windows
registry recovery, SQLite recovery) in addition to app-level capabilities.
Benchmark observations now capture standard information retrieval metrics and
benchmark provenance for reproducibility and cross-framework comparison.

- **New property on `ToolCapability`:**
  - `forensicTaskType` — CFTT task category (e.g., `string-search`,
    `deleted-file-recovery`, `file-carving`, `windows-registry-recovery`,
    `sqlite-recovery`); enables task-level capabilities without a specific
    target application
  - `application` relaxed from required (1..1) to optional (0..1) in SHACL
    shapes to accommodate task-level capabilities

- **6 new IR metrics on `BenchmarkObservation`:**
  - `precisionScore` — TP / (TP + FP), 0.0–1.0
  - `recallScore` — TP / (TP + FN), 0.0–1.0
  - `f1Score` — harmonic mean of precision and recall, 0.0–1.0
  - `truePositiveCount` — number of correctly identified items
  - `groundTruthCount` — total items in reference dataset
  - `submittedCount` — total items reported by the tool (TP + FP)

- **3 new provenance properties on `BenchmarkObservation`:**
  - `benchmarkFramework` — framework name (e.g., `AutoDFBench`, `NIST-CFTT`)
  - `testCaseIdentifier` — unique test case ID within the framework
  - `benchmarkSuiteScore` — overall composite score, 0.0–1.0

- **New property on `PlatformSpecification`:**
  - `fileSystemType` — filesystem type (e.g., `FAT32`, `NTFS`, `ext4`, `HFS+`)
    for forensic tasks where tool performance varies by filesystem

- **SHACL shapes** updated with constraints for all new properties including
  `sh:minInclusive`/`sh:maxInclusive` range constraints on score properties

- **Updated exemplar** (`toolcap-exemplar.ttl`) with three new CFTT-style
  scenarios: Tool A file carving on NTFS, Tool A deleted file recovery on
  FAT32, and Tool B string search on ext4 — all with full AutoDFBench IR
  metrics and provenance

- **Updated Python example** (`example_capability_matrix.py`) demonstrating
  task-level capabilities, filesystem-aware platforms, and AutoDFBench
  benchmark observations with IR metrics

- All exemplar data validated with `case_validate --built-version case-1.4.0`
  (`Conforms: True`)

## [1.3.0] - 2026-03-26

### Added

#### Toolcap Extension v0.2.0 — Forensic Tool Benchmarking and Access Control

The `extensions/toolcap/` extension ontology has been expanded from a simple
capability matrix into a full benchmarking and access-control framework for
forensic tool evaluation. The extension now supports vendor-claimed vs.
independently benchmarked capability data, structured platform specifications,
point-in-time benchmark observations, and security/licensing access restrictions.

- **3 new classes:**
  - `BenchmarkObservation` (`uco-core:UcoObject`) — a single point-in-time
    record of testing a forensic tool against an application, with optional
    metrics for pass/fail, completeness, accuracy, false positives/negatives,
    processing duration, dataset size, and parsed/missed observable categories
  - `PlatformSpecification` (`uco-core:UcoObject`) — structured replacement for
    the deprecated `supportedPlatform` string, capturing operating system, OS
    version, device model, and extraction method(s) including BFU (Before First
    Unlock) acquisition
  - `AccessRestriction` (`uco-core:UcoObject`) — security, licensing,
    classification, operational security, or legal authority constraints on tool
    usage, with optional link to `case-investigation:Authorization`
- **New properties on `ToolCapability`:**
  - `claimedByVendor` / `verifiedByBenchmark` — distinguish vendor-reported
    capabilities from independently tested ones
  - `applicationVersion` — target application version(s) the capability applies to
  - `dataFormatVersion` — data storage format version(s) (e.g., `.pst` vs `.nst`)
  - `supportsPlatform` — object property linking to `PlatformSpecification`
    instances (replaces the deprecated `supportedPlatform` string)
  - `hasAccessRestriction` — links to `AccessRestriction` instances
  - `hasObservation` — links to `BenchmarkObservation` instances (append-only)
- **Inverse property pair:** `hasObservation` / `capability` declared with
  `owl:inverseOf` for bidirectional traversal between capabilities and their
  benchmark evidence
- **`hasCapability`** — new object property on `CapabilityMatrix`, declared as
  `rdfs:subPropertyOf uco-core:object` for semantically precise matrix membership
- **Deprecated** `supportedPlatform` datatype property with `owl:deprecated true`;
  retained for backward compatibility with v0.1.0 data
- **14 benchmark metric properties** (all optional): `parseSuccess`,
  `completenessScore`, `accuracyScore`, `falsePositiveCount`,
  `falseNegativeCount`, `processingDuration`, `datasetSizeInBytes`,
  `parsedCategory`, `missedCategory`, `benchmarkNotes`, `benchmarkDate`,
  `testedToolVersion`, `testedApplicationVersion`, `testedDataFormatVersion`
- **SHACL shapes** for all new classes with value range constraints
  (`sh:minInclusive`/`sh:maxInclusive` for score properties)
- **Updated exemplar** (`toolcap-exemplar.ttl`) with a realistic scenario:
  two tools, a messaging app, and Microsoft Outlook with both `.pst` (pass)
  and `.nst` (fail) data format benchmarks, BFU acquisition, and
  law-enforcement-only access restrictions
- **Updated Python example** (`example_capability_matrix.py`) demonstrating all
  new classes including benchmark observations, platform specifications, and
  access restrictions
- All exemplar data validated with `case_validate --built-version case-1.4.0`
  (`Conforms: True`)

## [1.2.0] - 2026-03-26

### Added

#### Gap Detection and Change Proposals

- **Agent-assisted gap detection** — when `search_classes`, `find_classes_for_domain`,
  or `get_class_details` returns no adequate match, the AI agent proactively suggests
  drafting a change proposal for the missing concept
- **Two new MCP tools** for the change proposal workflow:
  - `check_existing_proposals(concept)` — searches open GitHub issues in both the
    [UCO](https://github.com/ucoProject/UCO/issues) and
    [CASE](https://github.com/casework/CASE/issues) repositories for prior proposals
    matching the concept; falls back gracefully when GitHub is unreachable
  - `draft_change_proposal(concept, description, scenario, ...)` — generates a
    filled-in change proposal markdown file using the official CDO template, including
    auto-generated competency questions, draft SPARQL queries, and example JSON-LD;
    writes the result to `change_proposals/`
- **UCO vs. CASE auto-triage** — `suggest_target_repo()` in `domain_index.py`
  determines whether a proposed concept belongs in UCO (general cyber-domain) or CASE
  (investigation-specific) based on keyword analysis, with reasoning explanation
- **Change proposal template** at `docs/templates/change-proposal-template.md` —
  the official CDO issue template for structured proposal submissions
- **Change proposal recipe** at `docs/recipes/change-proposal.md` — step-by-step
  workflow covering gap confirmation, existing proposal checks, UCO vs. CASE
  determination, proposal drafting, example data creation, and local extension
  scaffolding
- **`change_proposals/` directory** for locally-drafted proposals with README
  explaining the workflow and submission process
- Updated Cursor rules (`.cursor/rules/case-uco-sdk.mdc`) with gap detection
  guidance and change proposal workflow integration
- Updated recipe index with "Contributing to the ontology" section

#### Example Change Proposal

- `change_proposals/cryptocurrency-address-and-sanctions-designation.md` — a complete
  worked example proposing `CryptocurrencyAddressFacet`, `CryptocurrencyTypeVocab`,
  and `SanctionsDesignationFacet` for modeling blockchain addresses placed on
  government sanctions lists, with properties mapped to the
  [Chainalysis Sanctions Screening API](https://www.chainalysis.com/free-cryptocurrency-sanctions-screening-tools/)

## [1.1.0] - 2026-03-25

### Added

#### Testing & Quality

- **Exhaustive class instantiation tests** for all four languages — every generated class is constructed with defaults to catch broken imports, missing defaults, and inheritance issues across the entire object model (428 classes)
  - Python: dynamic test using the registry (`test_exhaustive.py`)
  - C#, Java, Rust: auto-generated by the code generator, stays in sync with the ontology
- **Smoke test binaries** for compiled languages — standalone executables that
  import the library, create objects, and serialize, proving the built artifacts
  actually link and run (C# `CaseUco.Smoke`, Java `SmokeTest`, Rust `examples/smoke.rs`)
- **Python strict type checking** with mypy (`[tool.mypy]` in `pyproject.toml`)
  - PEP 561 `py.typed` marker for downstream type checker support
  - `TYPE_CHECKING` imports for cross-module type references in generated code
  - `datetime` and `Any` imports added to generated modules where needed
- **Rust clippy** lint integration (`cargo clippy -- -D warnings`)
- New Makefile targets: `lint`, `typecheck-python`, `lint-rust`, `smoke`,
  `smoke-csharp`, `smoke-java`, `smoke-rust`, `check` (full local verification)
- CI pipeline additions: mypy type checking, clippy linting, smoke tests for
  all three compiled languages

### Fixed

- Generated Python classes now use `Optional[T]` for all non-list fields,
  matching the runtime behavior where all fields default to `None` (required-field validation is enforced by `CASEGraph`, not at construction)
- Generated Python modules now import `datetime` and cross-module types correctly
  for static type analysis
- Rust builder `build()` no longer panics on unset required fields — required-field validation is deferred to graph creation time, consistent with Python
- `graph.py` type annotation fixes: parameterized `dict`/`Field` generics, explicit metadata typing
- Rust `graph.rs` clippy fixes: `std::io::Error::other()`, redundant closure removal
- Python code generator now detects and avoids cyclic `TYPE_CHECKING` imports
  between modules with mutual dependencies (e.g., `uco.core` ↔ `uco.types`)
- C# and Java exhaustive tests use direct instantiation instead of `graph.Add()`
  to avoid required-field validation failures on classes like `SubjectActionLifecycle`
- Java `SmokeTest` no longer chains inherited setters (parent-type return breaks
  the chain); Java directory generation now applies `safe_identifier` to match
  package declarations

## [1.0.0] - 2026-03-25

Initial release of the CASE/UCO SDK — a multi-language data modeling library for
digital forensics, cyber-investigation, and cyber-observable data.

### Added

#### Core SDK

- Full typed class coverage for CASE 1.4.0 and UCO 1.4.0 (428 classes across 15 modules)
- Four language targets: **Python**, **C#**, **Java**, **Rust** — all sharing the same
  JSON-LD context and producing interoperable output
- `CASEGraph` API with `create()`, `serialize()`, `write()`, `load()`, and `load_file()`
- Required-field validation at insertion time (Python, C#, Java)
- Deterministic ID support (`create(id=...)`) for reproducible IRIs
- Round-trip serialization — load existing JSON-LD, add objects, re-serialize
- Triple estimation (`estimate_triples()`) for memory planning
- Graph splitting (`split()`) for catalog-style independent-object graphs
- Multi-file merge (`merge_files()`) for combining graphs
- Typed deserialization (`from_jsonld()`) in Python
- Automatic JSON-LD context with all 18 CASE/UCO namespace prefixes
- Runtime provenance metadata (`UCO_VERSION`, `CASE_VERSION`)

#### Runtime Registry

- `search(query)` — keyword search across all class names and descriptions
- `get_class(name)` — full property table with types, cardinalities, required flags
- `list_modules()`, `list_classes()`, `find_facets()`, `find_by_property_type()`
- `list_vocabs()` — all vocabulary/enum types with members
- Auto-generated `_registry.json` backing all four language runtimes

#### MCP Server for AI-Assisted Development

- FastMCP server (`mcp_server/server.py`) giving AI coding assistants programmatic
  ontology access
- Six tools: `search_classes`, `get_class_details`, `find_classes_for_domain`,
  `list_all_facets`, `get_recipe`, `list_all_vocabs`
- Three resources: `case-uco://domains`, `case-uco://modules`, `case-uco://patterns`
- Domain index (`domain_index.py`) mapping natural-language forensic tasks to the right
  CASE/UCO classes
- Cursor rules (`.cursor/rules/`) encoding SDK patterns, the ObservableObject + Facet
  model, validation requirements, and common pitfalls
- Pre-configured `.cursor/mcp.json` for zero-setup Cursor integration

#### Documentation

- **31 recipes** in `docs/recipes/` covering forensic workflows, devices, files,
  communication artifacts, and SDK patterns:
  - Forensic workflows: forensic tool, configured tool, chain of custody, analysis and
    classification, investigation lifecycle, network investigation, spear phishing
  - Devices and identity: device/workstation, mobile device + SIM, mobile forensics,
    cell site/tower, location, multi-platform accounts, events/auth logs
  - Files and data: file system, advanced file patterns, fragments/multipart, recovery
    and carving, partitions, bulk extractor paths, EXIF metadata, database records
  - Communication: email/messaging, threaded messaging (WhatsApp/chat), call logs,
    SMS/contacts, network artifacts
  - SDK patterns: runtime discovery, extensions, round-trip serialization, large
    datasets, existence intervals
- Recipe index (`docs/recipes/INDEX.md`) with cross-references to official CASE-Examples
- `ONTOLOGY_REFERENCE.md` — complete auto-generated class reference with property tables
- `docs/MAPPING_GUIDE.md` — maps forensic domains to the right classes
- `docs/PERFORMANCE_GUIDE.md` — benchmarks, hardware sizing, partitioning strategies
- `docs/ECOSYSTEM.md` — companion tools, community extensions, ontology sources
- `mcp_server/README.md` — MCP server setup, tool reference, troubleshooting

#### Relationship Tagging Convention

- `tag` property on `Relationship` objects to classify evidence basis:
  `observed` (from packet/artifact data), `inferred` (derived from analysis),
  `configuration` (network topology / infrastructure)
- Recipes updated with tagging guidance so agents produce semantically precise graphs

#### Example Agent/MCP Outputs

- `example_agentmcp_outputs/` — three complete worked examples showing end-to-end
  AI-assisted graph generation:
  - **WiFi packet capture** (`wifi_capture.py` / `.jsonld` / `.pcapng`) — three-layer
    network investigation with acquisition, observed network, and analysis attribution
  - **Cellebrite Samsung extraction** (`cellbrite_samsung_extraction.py` / `.jsonld`) —
    mobile device forensics with WhatsApp messages, GPS data, and app artifacts
  - **Field office custody** (`field_office_custody.py` / `.jsonld`) — chain of custody
    for evidence received from a field office

#### Extension Support

- `case-uco-generate scaffold` command for auto-generating typed classes from custom
  OWL Turtle extensions
- `extensions/toolcap/` — validated example extension for forensic tool capability
  comparison
- Extension ontology integration in the CLI explorer and documentation generators

#### Build and CI

- `Makefile` with `init`, `generate`, `build`, `test` targets
- GitHub Actions workflows: CI, CodeQL, dependency review, release
- Dependabot configuration for automated dependency updates

[Unreleased]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.27.0...HEAD
[1.27.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.26.0...v1.27.0
[1.26.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.25.0...v1.26.0
[1.25.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.24.0...v1.25.0
[1.24.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.23.1...v1.24.0
[1.23.1]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.23.0...v1.23.1
[1.23.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.22.4...v1.23.0
[1.22.4]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.22.3...v1.22.4
[1.22.3]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.22.2...v1.22.3
[1.22.2]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.22.1...v1.22.2
[1.22.1]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.22.0...v1.22.1
[1.22.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.21.0...v1.22.0
[1.21.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.20.0...v1.21.0
[1.20.0]: https://github.com/vulnmaster/CASE-UCO-SDK/compare/v1.19.0...v1.20.0
[1.8.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.8.0
[1.7.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.7.0
[1.6.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.6.0
[1.5.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.5.0
[1.4.1]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.4.1
[1.4.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.4.0
[1.3.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.3.0
[1.2.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.2.0
[1.1.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.1.0
[1.0.0]: https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.0.0
