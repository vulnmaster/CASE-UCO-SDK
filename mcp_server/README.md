# CASE/UCO MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that gives AI coding assistants programmatic access to the CASE/UCO ontology. Instead of reading thousands of lines of documentation, your AI agent can call tools like `search_classes("mobile")` to find the right types for your forensic scenario.

## Setup

### 1. Install FastMCP

```bash
pip install fastmcp
```

If you're using a virtual environment (recommended):

```bash
source .venv/bin/activate
pip install fastmcp
```

### 2. Shared listener (any MCP client)

stdio is still the default for a single local harness. For Cursor, Hermes,
Claude Desktop, VS Code, and other agents on the same machine, start one
listener and point every client at it:

```bash
# from the repo root (Linux / WSL)
./scripts/run-mcp-server.sh
# listens on http://127.0.0.1:8765/sse
```

Client config (no authentication):

```json
{
  "mcpServers": {
    "case-uco": { "url": "http://127.0.0.1:8765/sse" }
  }
}
```

Override bind address or port with `CASE_UCO_MCP_HOST`, `CASE_UCO_MCP_PORT`,
or `CASE_UCO_MCP_TRANSPORT=http`. Keep `PATH` and `CASE_UCO_EXTENSIONS` on
the Linux server process — never put a Linux `PATH` on a Windows `wsl.exe`
stdio wrapper.

### 3. Cursor stdio (optional single-client)

The `.cursor/mcp.json` in this repo defaults to the shared SSE URL. After
the listener is up, open Cursor's MCP panel and confirm "case-uco" is
connected. Do not click Authenticate.

### 4. Verify

Open Cursor's MCP panel (Settings > Tools & MCP) and confirm the "case-uco" server shows as connected. You can also test from the command line:

```bash
cd /path/to/CASE-UCO-SDK
fastmcp dev mcp_server/server.py
```

## Available Tools

| Tool | Arguments | Description |
|------|-----------|-------------|
| `search_classes` | `query: str` | Find classes by keyword match on name or description |
| `get_class_details` | `name: str` | Full property table for a specific class |
| `find_classes_for_domain` | `domain: str` | Map a forensic task to the right classes |
| `list_all_facets` | (none) | All Facet classes for the ObservableObject pattern |
| `get_recipe` | `scenario: str` | Find a code recipe for a forensic workflow |
| `get_recipes` | `scenario: str, limit?: int, include_content?: bool` | Find multiple ranked recipes for multi-domain scenarios |
| `route_investigation_content` | `content_text?, source_path?, max_families?` | Classify ANY submission by investigation family (CAC, violent crime, financial/crypto, court filings, intrusion, mobile, email, filesystem, civil, corporate) and return recipes, extensions, namespaces, CDO upper-ontology profiles — or the extension-gap workflow for unseen data types |
| `route_cac_content` | `content_text?, source_path?, output_format?, include_recipe_content?, max_recipes?` | Detect CAC domains in submitted content and return multiple CAC recipes plus validation guidance |
| `classify_apple_package_shape` | `package_root, profile?` | Fail-closed classification of a bounded local Apple directory/inventory as full sysdiagnose or standalone FOSS logarchive package; safe metadata only |
| `build_acquisition_package_graph` | `package_root, output_path, profile?, max_event_records?, shareable?, event_excerpt_path?, event_message_policy?, extensions?` | Write a bounded Apple/SOLVE-IT package graph with optional CSV/JSONL event sample and share-safe path/identifier/message handling |
| `list_all_vocabs` | (none) | All vocabulary/enum types with members |
| `process_document_file` | `source_path, output_path, file_kind?, upload_id?, progress_output?` | Process a supported local synthetic document (receipt image, PDF, Office, CSV/table) into bounded CASE/UCO-shaped JSON-LD |
| `validate_graph` | `graph_path: str, allow_warning?: bool, extensions?: list[str]` | Run `case_validate` against JSON-LD/Turtle; `extensions=['cac']` uses the press-release subset; `extensions=['cac:full']` uses the full manifest |
| `execute_sparql_query` | `query, endpoint_url?, timeout_seconds?` | Execute bounded query-only SPARQL 1.1 against CaseLinker by default or another standards-compliant endpoint; normalizes bindings, ASK booleans, and RDF graph results |

Python API (v1.22 / #75): `from critic import analyze_artifact, CriticArtifactRequest` — deterministic graph/serializer critic with bounded prompt packages. MCP session tools arrive in #76.

## Available Resources

| URI | Description |
|-----|-------------|
| `case-uco://domains` | All forensic domain categories with descriptions |
| `case-uco://modules` | All ontology modules |
| `case-uco://patterns` | Core modeling patterns with code examples |
| `case-uco://sparql` | Remote SPARQL workflow, CaseLinker endpoint profile, safety rules, and starter queries |

## How AI Agents Use This

When you describe a forensic scenario in natural language, the AI agent:

1. Calls `route_investigation_content` to classify the submission (investigation family → recipes, extensions, namespaces, upper-ontology profiles)
2. Calls `find_classes_for_domain` or `search_classes` to identify relevant types
3. Calls `get_class_details` on each type to see its properties
4. For CAC content, calls `route_cac_content` to get multiple matching recipes and validation guidance
5. For Apple collection packages, calls `classify_apple_package_shape` before choosing full-sysdiagnose versus standalone-FOSS guidance, then optionally calls `build_acquisition_package_graph` for a bounded share-safe graph
6. Optionally calls `get_recipe` or `get_recipes` to find code examples
7. Writes correct SDK code using the exact class names and property names
8. Calls `validate_graph` with the matching `extensions=[...]` on the finished graph — strict concept coverage rejects undeclared terms and routes the agent to the change-proposal / extension workflow
9. For remote analysis, builds SPARQL from the exact discovered IRIs, calls `execute_sparql_query` with a bounded query, and treats returned values as untrusted external data

This is much faster and more accurate than the agent reading markdown documentation.

## Workflow for Hermes and Link-Look (any investigation type)

End-to-end pattern for warrant returns, legal filings, case files, press
releases, and investigator notes — including data types the server has
never seen:

1. **Extract** — `process_document_file(source_path="case.pdf", output_path="extract.jsonld")` for PDFs/images, or pass plain text directly.
2. **Classify** — `route_investigation_content(content_text=<clean narrative excerpt>)` detects the investigation family (CAC, violent crime/terrorism, financial/crypto, court filings, network intrusion, mobile/device, email, filesystem, civil e-discovery, corporate/internal) and returns per-family recipes, the extension ontologies to enable, core namespaces, and applicable CDO upper-ontology profiles. If nothing matches, it returns `extension_gap_guidance` — the search → proposal → local-extension workflow for previously unseen data.
3. **Compose, don't split** — when several families match (real cases are often CAC + violent crime + fraud at once), build ONE graph using `ordered_recommendations` (`primary_composition_recipe` → `docs/recipes/cross-ontology-composition.md`) with the union of matched extensions and profiles.
4. **Go deeper than the anchors** — family recipes cover the domain-interpretation layer; use `get_recipes(scenario)` for ranked matches across the full 60+ recipe catalog and `guide_mapping(evidence_source)` for each evidence type actually in hand (devices, files, messages, call logs, locations, EXIF, databases, ...).
5. **Deep-route CAC** — for CAC content, `route_cac_content(...)` adds per-domain CAC recipes and modeling checklists (steps below).
6. **Grow the catalog (self-improvement loop)** — when an agent has to work out a pattern no recipe covers, it writes one; when a live case proves an existing recipe wrong, incomplete, or invisible to routing, the agent improves that recipe (or its index keywords) in place. `docs/recipes/recipe-authoring.md` defines both paths: structure, grounding rules (validated exemplar, strict concept coverage, cyber vs. non-cyber typing), re-validation before publishing, and registration in `INDEX.md` + `RECIPE_INDEX` (+ a router family when warranted). Investigators are mostly non-technical — the recipe catalog is where the automation accumulates its modeling judgment — and because every recipe is grounded in public CASE/UCO/CAC releases, published extensions, and CDO-profiled upper ontologies, the knowledge models it produces can be shared with outside parties who can validate and reuse them independently.

CAC-specific continuation:

1. **Route** — `route_cac_content(content_text=<clean narrative excerpt>)` returns multiple matched recipes (e.g. task force + warrant arrest + grooming + legal charges + CSAM purchasing).
2. **Build** — Agent reads returned recipe files and composes JSON-LD or TTL using CAC classes (`CASE_UCO_EXTENSIONS=cac`).
3. **Validate** — `validate_graph("output.jsonld", extensions=["cac"])` uses `ontology/cac/validation-subset.json` (recommended for press-release KGs). Use `extensions=["cac:full"]` only when the full CAC manifest SHACL is repaired upstream.

For non-CAC prosecutions (violent crime, terrorism, generic federal cases), build with the `legalproc` extension and validate with `extensions=["legalproc"]` — see `docs/recipes/legal-process-modeling.md` and the exemplar at `examples/pacer/wdmo_2022_cr_04065/`.

Example Hermes tool sequence for the Maryland ICAC Annapolis arrest press article:

```text
process_document_file(
  source_path="/path/to/Maryland_ICAC_Arrest_Test_PDF.pdf",
  output_path="/tmp/maryland-extract.jsonld",
)
route_cac_content(
  content_text="Maryland State Police Computer Crimes Unit and Maryland ICAC Task Force ...",
  output_format="jsonld",
  include_recipe_content=true,
  max_recipes=6,
)
# Agent builds graph using matched recipes and modeling_checklist
validate_graph(
  graph_path="examples/maryland-icac-annapolis-arrest-2025.jsonld",
  extensions=["cac"],
)
```

Noisy PDF extraction (navigation, ads, repeated URLs) lowers routing scores. When `route_cac_content` reports `extraction_quality.noisy_extraction: true`, summarize investigative facts into `content_text` before routing. Reference builder: `examples/build_maryland_icac_annapolis_arrest.py`.

## Running under Hermes Agent

The server runs unmodified under any MCP-native agent harness. For the
[Hermes Agent](https://github.com/NousResearch/hermes-agent) (Nous Research),
register it as a stdio MCP server in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  case-uco:
    url: "http://127.0.0.1:8765/sse"
```

Or stdio against the same checkout:

```yaml
mcp_servers:
  case-uco:
    command: "/home/cory/CASE-UCO-SDK/.venv/bin/python"
    args: ["/home/cory/CASE-UCO-SDK/mcp_server/server.py"]
    env:
      PYTHONPATH: "/home/cory/CASE-UCO-SDK/python:/home/cory/CASE-UCO-SDK/mcp_server"
      PATH: "/home/cory/CASE-UCO-SDK/.venv/bin:/usr/bin:/bin"
      CASE_UCO_EXTENSIONS: "cac,legalproc,solveit,cryptoinv,rico,weapons,drugs"
```

Run `/reload-mcp` in Hermes after editing the config. All tools are then
discoverable by the agent alongside its built-in tools.

Apple package workflow (issue #99):

```text
classify_apple_package_shape(package_root="/cases/evidence/apple-collect", profile="auto")
build_acquisition_package_graph(
  package_root="/cases/evidence/apple-collect",
  output_path="/cases/workspace/apple-package.jsonld",
  profile="auto",
  max_event_records=50,
  event_excerpt_path="/cases/evidence/apple-collect/unifiedlog_excerpt.jsonl",
  shareable=true,
  event_message_policy="omit",
  extensions=["solveit"],
)
validate_graph(
  graph_path="/cases/workspace/apple-package.jsonld",
  extensions=["solveit"],
  strict_concepts=true,
)
```

`auto` intentionally refuses unsupported or ambiguous trees. A full
`sysdiagnose_*` tree requires `system_logs.logarchive` plus strong sysdiagnose
markers; standalone FOSS `logarchive` + crash pull + live syslog/apps inventory
uses separate guidance and must not be called a full sysdiagnose. Binary
`.tracev3` stores stay external. CSV/JSONL decoder output also stays external;
only the bounded `max_event_records` sample is represented as `EventRecord` /
`Event`. Shareable mode normalizes `filePath`, redacts common identifiers, and
omits messages by default. Device-absolute time is not asserted unless inventory
metadata explicitly establishes timesync anchoring.

Law-enforcement deployment notes:

- The shared listener binds `127.0.0.1` by default (stdio still works for a
  single harness). `check_existing_proposals` and the
  opt-in `execute_sparql_query` tool perform outbound HTTPS requests. Secure
  deployment profiles disable SPARQL egress unless
  `CASE_UCO_SPARQL_ALLOW_NETWORK=1` is explicitly set; production deployments
  must explicitly configure additional public targets in
  `CASE_UCO_SPARQL_ALLOWED_HOSTS`. Pair this server with
  a local model backend by default, and use external endpoints or commercial
  backends only in agency-approved, accredited environments.
  Hosting an MCP server inside an agent does not by itself satisfy CJIS or
  any other compliance obligation.
- `process_document_file` accepts bounded local files only and returns safe
  metadata; `validate_graph` requires the CASE Utilities `case_validate` CLI
  on PATH and never fabricates a passing result.
- Agents should call `validate_graph` on every produced graph before
  submitting it to downstream tools (e.g., Link-Look normalization review).

## Secure Deployment (workspace policy and trust boundary)

### Filesystem workspace policy

Production deployments should confine the file-handling tools
(`process_document_file`, `classify_apple_package_shape`,
`build_acquisition_package_graph`, `validate_graph`) to explicit directories via
environment variables on the server process:

```yaml
env:
  # Evidence/source files may only be read from these roots (read-only):
  CASE_UCO_MCP_READ_ROOTS: "/cases/evidence"
  # Outputs, extraction bundles, and progress files must land here:
  CASE_UCO_MCP_WRITE_ROOTS: "/cases/workspace"
  # Optional; under an active policy outputs never overwrite by default:
  # CASE_UCO_MCP_ALLOW_OVERWRITE: "1"
```

Multiple roots are separated by `:`/`;` (`os.pathsep`) or commas.
Containment is decided after full path resolution, so `..` traversal and
symlink escapes are rejected. Violations return typed, non-sensitive errors:
`source_outside_read_roots`, `output_outside_write_roots`,
`progress_outside_write_roots`, `output_exists`, `source_output_conflict`.
`validate_graph` may read from both root sets (it validates graphs the
server just produced). When neither variable is set, no policy is active —
acceptable for local development, not for agent-connected case work. Run
the server process under an account with no filesystem access beyond these
roots; keep evidence roots read-only at the OS level.

### Deployment profiles and secure mode

Since v1.17.0 the policy is *enforceable*, not just advisory. Select a
deployment profile (or set secure mode directly):

```yaml
env:
  # One of: development | offline-investigation | production-authoring | production-review
  CASE_UCO_MCP_PROFILE: "production-review"
  # Or, independent of a profile:
  # CASE_UCO_MCP_SECURE_MODE: "1"
```

- **`development`** (default): current permissive behavior; missing roots
  fall back to unrestricted reads/writes.
- **`offline-investigation`**, **`production-authoring`**,
  **`production-review`**: secure mode is implied. The server **refuses to
  start** (exit code 3) if read/write roots are missing, nonexistent,
  dangerously broad (`/`, a drive root, or a home directory — override
  only with `CASE_UCO_MCP_ALLOW_BROAD_ROOTS=1`), or if a write root sits
  inside an evidence read root. At runtime, unconfigured roots fail closed
  (`read_roots_unconfigured` / `write_roots_unconfigured`) instead of
  falling back to unrestricted access.
- Promotion authority follows the profile: `offline-investigation` denies
  extension/recipe promotion entirely (`promotion_not_permitted_in_profile`);
  `production-review` requires a named reviewer
  (`reviewer_identity_required`); `development` and `production-authoring`
  allow it.
- An unknown profile name fails closed as secure.
- The `get_security_profile` MCP tool returns a bounded, non-sensitive
  summary (profile, secure-mode flag, root counts, promotion authority,
  configuration errors) so operators and agents can verify the active
  posture without reading the environment.

### Untrusted evidence content (indirect prompt injection)

Everything extracted from a submitted document is **evidence data, never
instructions**. Tool responses label it (`content_trust:
untrusted-source-content`) and flag instruction-like patterns
(`injection_warnings`), but detection is heuristic — integrating hosts
(Hermes, Link-Look, Cursor, and any other agent harness) must:

1. Render extracted text and `extracted-content.json` bundles as data, not
   as part of the agent's directive context.
2. Never execute tool calls, file operations, or policy changes because
   text inside a document asked for them.
3. Gate persistent self-improvement actions (extension creation, change
   proposals, recipe edits, repository writes) on an explicit
   investigator/operator decision — see the knowledge lifecycle in
   `docs/recipes/recipe-authoring.md` (`make promote-extension`,
   `make deprecate-extension`, `make rollback-extension`).

See `SECURITY.md` for the full MCP threat model.

## Architecture

The server wraps the existing Python registry API (`case_uco.registry`) and a domain index (`domain_index.py`) that maps investigative tasks to classes.

```
mcp_server/
├── server.py          FastMCP server with tool and resource definitions
├── sparql_client.py   Bounded query-only remote SPARQL 1.1 client
├── domain_index.py    Task-to-class mappings, domain categories, recipe index
├── requirements.txt   Python dependencies (fastmcp, pypdf)
└── README.md          This file
```

### Document processor extraction dependencies

`document_processor.py` detects optional extraction tooling at runtime and
fails with typed, actionable errors when it is missing — it never shows
undecodable bytes to a reviewer:

| Capability | Tooling | Failure code when absent |
|---|---|---|
| PDF text layer (preferred) | `pdftotext` (poppler-utils) | falls back to `pypdf` |
| PDF text layer (fallback) | `pypdf` (in `requirements.txt`) | falls back to gated literal-string scrape |
| Scanned/image-only PDF OCR | `pdftoppm` (poppler-utils) or `pypdf` page-image extraction, plus `tesseract` | `pdf_text_missing` |
| Subset-font PDF with no real extractor | — | `pdf_text_unreadable` |
| Image OCR (receipts/scans) | `tesseract` | `ocr_unavailable` |

On Debian/Ubuntu: `sudo apt install poppler-utils tesseract-ocr`. Rootless
alternative: `conda create -n link-look-ocr -c conda-forge tesseract poppler`
and symlink the binaries into a `PATH` directory (e.g. `~/.local/bin`). For
air-gapped deployments, mirror these packages with your offline bundle.

The server reads from `python/case_uco/_registry.json`, which is auto-generated by `case-uco-generate generate` and contains the full ontology schema.

Remote query configuration and the validated graph-loading roadmap are in
[`docs/SPARQL.md`](../docs/SPARQL.md).

## Troubleshooting

**Server not connecting:** Make sure `fastmcp` is installed in the Python environment that Cursor uses. If using a venv, the `.cursor/mcp.json` may need its command adjusted to point to the venv Python.

**"Registry not found" error:** Run `case-uco-generate generate` from the project root to produce the `_registry.json` file, or ensure the `python/case_uco/_registry.json` file exists.

**Testing outside Cursor:** You can run the server directly for debugging:

```bash
PYTHONPATH=python:mcp_server python mcp_server/server.py
```
