# Critic deterministic rules and session loop

Developer guide for the CASE/UCO critic package (issues #75–#78).

## Layout

| Module | Role |
|--------|------|
| `canonical.py` | RDFLib-backed `CanonicalGraphView`, exact IRIs, offline remote-context policy |
| `models.py` | Typed contracts + `make_stable_finding_id` |
| `deterministic.py` | Offline `analyze_artifact` entrypoint |
| `sessions.py` | Resumable two-pass MCP session state machine (#76) |
| `sampling.py` | Optional `Context.sample` helper + fake sampler |
| `handoff.py` | Preview-only self-improvement handoff (#78) |
| `graph_integrity.py` | Parse statuses, duplicate keys, dangling RDF object refs |
| `graph_heuristics.py` | Structural modeling heuristics (canonical API only) |
| `serializer_python.py` | Python AST serializer checks (per-rule executions) |
| `coverage.py` | Coverage contract + ContentDataFacet source-hash compare |
| `context_builder.py` | Bounded prompt package + hash + one-hop neighborhoods |
| `finding_diff.py` | Pass-to-pass ledger (`unevaluated` vs `resolved`) |
| `response_parser.py` | Authoritative model-response schema enforcement |
| `scorecard.py` | Ledger-aware dimensions + hard-cap-only model merge |
| `schemas/` | JSON Schemas (prompt, response, review, handoff, …) |
| `vocabularies.json` | Severities, categories, error codes |

Evaluation corpus and offline oracles live under `evaluation/critic/` (#77).

## Session defaults (#76)

- Required critic passes: **2**
- Additional passes: operator-approved via `extend_critic_review` + token
- Hard maximum total passes: **8**
- Model policies: `disabled` | `manual` (default) | `client_sampling`
- Finalization requires: matching hashes, complete conforming validation,
  `analysis_status=complete`, no open critical/high findings, and two completed
  critic responses (or two deterministic passes when `disabled`)

## Finding identity

`finding_id` is stable: `CRIT-` + SHA-256 of `rule_id|semantic target parts`
(or `MODEL-category|target|claim_type` for critic inferences — **no array index**).
Graph targets use expanded node/predicate/counterpart IRIs — **not** line/path/
evidence prose. Serializer targets use path + qualified name — **not** line.

## Rule-execution ledger

Every pass records `evaluated|not_applicable|skipped|failed` per concrete rule.
Failed/skipped **required** rules yield `analysis_incomplete` and block
`deterministic_clean` / finalization. `not_applicable` does not block.

Prior deterministic/source findings resolve only when a matching `rule_id` or
`verifier_rule_id` evaluated successfully and the defect is absent.

## Trust boundary

Graph literals, serializer comments, and source excerpts are **untrusted**.
Prompt packages include a trust-boundary block. Self-improvement writes require
explicit operator approval (`prepare_critic_handoff(..., approve_write=True)`).

Session `audit.jsonl` is tamper-evident against partial or out-of-band edits
(file digests, state, and the full semantic `session.json` projection are
reconciled). It is **not** a cryptographically signed external ledger against
an administrator who can rewrite the entire session directory and audit history
together. Sessions created on pre-release v1.22 builds before full-session
projection binding may fail closed after upgrade — restart them rather than
manually migrating state.

## Graph heuristics (`CRIT-H-*`, `graph_heuristics` v1.4.0)

| Rule ID | Intent |
|---------|--------|
| `CRIT-H-INV-NO-OBJECT` | Investigation missing `uco-core:object` |
| `CRIT-H-AUTH-NON-INVESTIGATION` | `relevantAuthorization` on non-Investigation |
| `CRIT-H-ACQ-INPUT-RESULT-INVERSION` | Action named with an acquisition verb (acquire, extract, export, imaging, or a leading "Image …") uses a file only as input. "Examine the disk image" is not an acquisition |
| `CRIT-H-RELATED-TO-OVERUSE` | Excessive generic `Related_To` |
| `CRIT-H-CHARGED-WITH-REVERSED` | `Charged_With` charge→person |
| `CRIT-H-DICT-ENTRY-COLLISION` | Dictionary entry IRI under multiple parents |
| `CRIT-H-FACET-PROPS-ON-OBSERVABLE` | Facet properties on ObservableObject |
| `CRIT-H-ACTION-COMPLETENESS` | Acquir/extract/analy/hash/image/export action missing performer\|instrument, object, or (acquisition) result |
| `CRIT-H-IDENTITY-CONFLATION` | Person also typed Account/`*Account`/Role |
| `CRIT-H-PROXY-DUPLICATE` | Same ContentDataFacet hashValue on distinct IRIs without Contained_Within/Extracted_From/Parent_Of/Moved_*/Copied_*/Renamed_* **or** an Action object→result transformation link |
| `CRIT-H-DERIVED-NO-HASH` | Derived artifact without hashValue — **high** for acquisition-style gaps; **medium** only when `profiles` includes `cti-report` or tags `hash-status:not-published` / `source-bytes:not-acquired` are present |
| `CRIT-H-DERIVED-NO-PROVENANCE` | Derived node with no container membership or inbound provenance |
| `CRIT-H-MARKING-INHERITANCE` | Source has `objectMarking`, derived does not |
| `CRIT-H-CUSTODY-UNPAIRED` | Custody/transfer/release/receipt action without object+result or Transferred_To |
| `CRIT-H-IMAGE-CONTAINER-MISMATCH` | RasterPicture named like a forensic image (a `.E01`/`.dd`/`.aff4`/`.ufd` suffix, an `EWF`/`UFED` token, or "disk/raw/forensic image"), or File Contained_Within RasterPicture. Camera `.raw` photos are not flagged |
| `CRIT-H-CONTEXTUAL-COMPILATION-OMISSION` | Action-result File/Observable not in Investigation/ProvenanceRecord/ContextualCompilation/Grouping |
| `CRIT-H-ACTION-ROLE-CONTRADICTION` | Action name implies victim/user execution but the performer is named or tagged as a threat actor, adversary, attacker, or `APT<n>` |
| `CRIT-H-ORPHAN-TOP-LEVEL` | Top-level `/@graph/N` node unreachable from Investigation/ProvenanceRecord/Bundle roots. Every IRI a reached node references (including through embedded facets, so email `from`/`to`, `hash`, `objectMarking`, `createdBy`) is reached; Relationship subclasses such as ObservableRelationship join their endpoints; compilations/groupings count only after reached |
| `CRIT-H-LEGAL-PROCESS-NO-INVESTIGATION` | Warrant / affidavit / attached legal-process language in graph literals without a `case-investigation:Investigation` |
| `CRIT-H-BROKEN-CRYPTO-ADDRESS-STRING` | Extracted string or description still contains a spaced/punctuated Base58-like address that was never reconstructed |

Source-path coverage (`CRIT-C-SOURCE-HASH`, coverage v1.2.0): when a submitted source file is **not** embedded as a domain-graph node, the rule is `not_applicable` — builders/recipes belong in the critic session manifest, not the investigation graph. Embedded source nodes are still hash-checked when present.

A matching hash shows the file is the one named, not that the graph agrees with its contents, so `CRIT-C-SOURCE-HASH` and `CRIT-C-PROVENANCE-MANIFEST` results score `provenance_custody`. `source_fidelity` and `coverage_completeness` are scored only from coverage rules that compare the graph with source content (the coverage contract), and stay unassessed otherwise. The prompt package's `source_excerpts` hold each source's document text from the document processor's extractors (`extraction`: `<kind>_text`), raw bytes only for formats with no extractor (`raw_bytes`), or empty text when a supported document yields none (`no_text_extracted`).

Provenance sidecar (`CRIT-C-PROVENANCE-MANIFEST*`, coverage v1.3.1): when `provenance_manifest_path` is set (one-shot or session), verify schema-1.1 `artifacts[]` (or legacy builder/recipe/output) hashes via workspace policy; require exactly one `output_artifact` whose digest equals the graph under review; empty manifests fail closed. The manifest digest is bound into `ArtifactHashes` / artifact-set / review-config hashes and replayed across multi-pass sessions.

Serializer modes: `typed_sdk` | `raw_fixture` | `casegraph_raw` | `auto`. Public `CASEGraph` builders that use `upsert_node` without generated dataclass `create()` should declare `casegraph_raw`.

## Python serializer AST (`CRIT-S-PY-*`)

| Rule ID | Intent |
|---------|--------|
| `CRIT-S-PY-TYPED-MODE-WITHOUT-TYPED-OBJECTS` | `serializer_mode=typed_sdk` but script imports no generated domain classes / never calls typed `create()` |
| `CRIT-S-PY-PRIVATE-OBJECTS` | Mutate `CASEGraph._objects` |
| `CRIT-S-PY-JSON-DUMPS-ONLY` | `json.dumps` without graph write/serialize |
| `CRIT-S-PY-FAIL-OPEN-VALIDATION` | Success when validator unavailable |
| `CRIT-S-PY-SWALLOWED-EXCEPTION` | Broad `except` swallow |
| `CRIT-S-PY-UNSCOPED-UUID5` | uuid5 ID helper without parent scope |
| `CRIT-S-PY-GLOBAL-UUID-IDS` | uuid4 `make_*/new_*/build_*` without parent |
| `CRIT-S-PY-NONEXISTENT-API` | Unknown method **or invalid call signature** on a name bound to `CASEGraph` (unknown kwargs / impossible arity via `inspect.signature`) |
| `CRIT-S-PY-REL-ID-COLLAPSE` | `create_relationship` in `for` without assertion_id |
| `CRIT-S-PY-SILENT-LOOKUP` | `.get(...)` then Return/Pass/Continue without Raise |
| `CRIT-S-PY-UNSAFE-OVERWRITE` | `open(...,"w")` / `Path.write_*` without `workspace_policy` |
| `CRIT-S-PY-SOURCE-HASH-DRIFT` | 64-hex `hash_value` literal without hashlib in function |
| `CRIT-S-PY-SYNTHETIC-HASH` | `synthetic_hash`/`fake_hash`/`placeholder_hash` feeds hash construction |
| `CRIT-S-PY-QUADRATIC-SCAN` | Nested `for` over `_objects` / `list(graph)` |
