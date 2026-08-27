# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.27.x  | Yes (current)      |
| < 1.27  | No                 |

Only the latest SDK release line receives security updates. This project
tracks the CASE 1.5.0 and UCO 1.5.0 ontology releases; profiled upper
ontologies (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF) are
pinned in `python/case_uco/validation/upper_ontology_registry.json` with
source URLs and version IRIs.

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities**, and
**never include real investigative data, case identifiers, or evidence
content in any report** — public or private. Reproduce findings with Tier T0
synthetic data (see the test fixtures for examples).

Report privately using one of these methods:

1. **GitHub Security Advisories** (preferred): use the [private vulnerability reporting](https://github.com/vulnmaster/CASE-UCO-SDK/security/advisories/new) feature on this repository.
2. **Email**: send details to the repository maintainers via the contact information in the GitHub profile.

### What to Include

- Description of the vulnerability
- Steps to reproduce (proof-of-concept with synthetic data only)
- Affected component (language library, generator, MCP server, extension ontology, CI/CD)
- Impact assessment (what an attacker could achieve)
- Any suggested fix, if you have one

### What to Expect

- **Acknowledgment** within 72 hours of your report.
- **Triage and assessment** within 7 days. We will confirm whether the report is accepted as a vulnerability or declined with explanation.
- **Fix timeline**: critical vulnerabilities will be patched within 30 days. Lower-severity issues will be addressed in the next scheduled release.
- **Disclosure**: we follow coordinated disclosure and will work with you on timing and credit in the advisory.

## Scope

This security policy covers:

- The four language SDK libraries (Python `case-uco`, C# `CaseUco`, Java `case-uco`, Rust `case-uco`)
- The code generator (`case-uco-generator`)
- The MCP server (`mcp_server/`), including document processing, graph
  validation, strict concept coverage, investigation routing, and the
  knowledge-lifecycle tooling
- **Bundled extension ontologies in `extensions/`** (CAC, AEO,
  attack-technique, cryptoinv, legalproc, rico, weapons, drugs, toolcap).
  As of v1.15.0 these are operational capabilities — routing, validation,
  recipes, and exemplars depend on them — so their manifests, registries,
  SHACL shapes, validation subsets, and package scaffolds are in scope.
- The pinned upper-ontology term registry (`mcp_server/upper_ontology_registry.json`)
  and its build tooling
- Recipes and routing indexes that steer agent behavior (`docs/recipes/`,
  `mcp_server/domain_index.py`, the routers)
- CI/CD workflows and build infrastructure

It does **not** cover:

- The upstream CASE and UCO ontology sources (report to [UCO](https://github.com/ucoProject/UCO/security) or [CASE](https://github.com/casework/CASE/security) directly)
- The upstream CAC Ontology and AEO submodule contents (report to their
  respective Cyber-Domain-Ontology repositories); the *integration* of those
  submodules here is in scope
- The pinned upper ontologies themselves (PROV-O, OWL-Time, etc. are W3C/OGC/OBO
  specifications); the *registry extraction* of them here is in scope
- Third-party tools referenced in documentation (case-utils, Apache Jena, etc.)
- Extensions or recipes that a deployment authors locally and has not
  contributed upstream

## MCP Server Threat Model and Trust Boundaries

The MCP server is designed for **local, stdio-based deployment** beside the
agent host (Cursor, Hermes, Link-Look). Its network-capable tools are
`check_existing_proposals` (GitHub API, outbound HTTPS only) and
`execute_sparql_query` (operator-selected SPARQL endpoint, with the controls
below).
Deployments should assume the connected agent is capable of calling any
exposed tool with attacker-influenced arguments.

### Outbound SPARQL and SSRF controls

`execute_sparql_query` sends the full query to a remote endpoint and returns
remote values to the agent. The client therefore enforces a query-only and
egress boundary: SELECT/ASK/CONSTRUCT/DESCRIBE only; no SPARQL Update or
SERVICE federation; bounded query, timeout, and response sizes; no redirects;
no URL credentials; public HTTPS only by default; DNS/address checks that
reject loopback, private, link-local, multicast, unspecified, and reserved
targets; and typed errors that do not echo remote error bodies.

The built-in CaseLinker host and an operator-configured default endpoint are
allowed; every other public target requires an exact
`CASE_UCO_SPARQL_ALLOWED_HOSTS` entry. Local/private endpoints such as Fuseki
require an exact `CASE_UCO_SPARQL_ALLOWED_PRIVATE_HOSTS` entry. Secure
deployment profiles deny SPARQL egress unless
`CASE_UCO_SPARQL_ALLOW_NETWORK=1` is explicitly enabled.
Every successful response is labeled
`content_trust: untrusted-external-sparql-results`; returned literals must not
be treated as instructions. Queries themselves can disclose identifiers and
literals, so sensitive investigative values must not be sent to an endpoint
that is not authorized for that data. See `docs/SPARQL.md`.

### Filesystem access controls (least privilege)

`process_document_file` and `validate_graph` accept caller-supplied paths.
Production deployments should confine them with the workspace policy
(`mcp_server/workspace_policy.py`):

- `CASE_UCO_MCP_READ_ROOTS` — directories evidence/source files may be read from
- `CASE_UCO_MCP_WRITE_ROOTS` — the writable case workspace for outputs and progress files
- `CASE_UCO_MCP_ALLOW_OVERWRITE` — opt-in; under an active policy outputs never overwrite by default

Containment is enforced on fully resolved paths, so `..` traversal and
symlink escapes are rejected with typed, non-sensitive errors
(`source_outside_read_roots`, `output_outside_write_roots`, `output_exists`,
`source_output_conflict`). Run the server process under an account with no
access beyond those roots. See `mcp_server/README.md` for the recommended
configuration.

Since v1.17.0 the policy is enforceable via deployment profiles
(`CASE_UCO_MCP_PROFILE`: `development`, `offline-investigation`,
`production-authoring`, `production-review`) or `CASE_UCO_MCP_SECURE_MODE=1`.
In secure mode the server refuses to start on a misconfigured policy
(missing/nonexistent/dangerously-broad roots, write roots inside evidence
roots), unconfigured roots fail closed at runtime instead of falling back to
unrestricted access, and unknown profile names are treated as secure. The
`get_security_profile` tool reports the active posture without exposing
paths or environment contents.

### Indirect prompt injection (untrusted evidence content)

Documents processed by this server are **evidence, not instructions**. A
PDF, chat export, or spreadsheet may contain text crafted to instruct an AI
agent to ignore its rules, disclose files, invoke tools, or modify the
repository. Mitigations in the SDK:

- All extracted content is labeled `content_trust: untrusted-source-content`
  in tool responses and extraction bundles.
- Extracted text is scanned for common injection patterns and results carry
  `injection_warnings`; warnings never echo the matched payload. **Detection
  is heuristic — absence of a warning is not a safety guarantee.**
- The server's MCP instructions explicitly prohibit treating evidence text as
  directions and require persistent changes (extensions, proposals, recipe
  edits) to originate from an investigator/operator decision, never from
  content found inside evidence.
- Agent hosts must keep this boundary on their side too: render evidence
  text as data, and gate any repository-modifying action on explicit human
  intent.

### Self-improvement governance (learned recipes and extensions)

Learned artifacts follow a staged lifecycle (`mcp_server/knowledge_lifecycle.py`,
`docs/recipes/recipe-authoring.md`): **candidate → validated → operational →
deprecated/rolled back**. Candidate recipes and candidate extensions are
excluded from routing until validation gates pass and a human promotes them;
promotion records provenance (reviewer, timestamp, git commit, deployment
profile, gate results) in the manifest. As of v1.17.0 the promotion gates
require manifest-schema validity, parseable ontologies, subclass anchoring to
*declared* classes, at least one conforming exemplar, failing negative
fixtures whenever SHACL shapes ship, and passing competency queries when
declared; recipes are promoted with the same transactional rigor
(`make promote-recipe` / `make deprecate-recipe`). Promotion authority is
profile-scoped: denied in `offline-investigation`, reviewer-identity-required
in `production-review`. Emergency revocation (`make deprecate-extension`) and
git-based rollback (`make rollback-extension EXT=... REF=...`) restore a
previous approved knowledge generation. Security review of a promotion should
treat new routing keywords, recipe guidance, and ontology terms as code
review: they steer future automated behavior.

### Validation integrity

Strict concept coverage is closed-world: every class/property must be
declared in CASE/UCO, a loaded extension, or the pinned upper-ontology
registry — fabricated terms (including inside profiled namespaces such as
`prov:`) are rejected, declared terms used in the wrong RDF role are
flagged, and the declared-term cache invalidates automatically when ontology
files change. Validation never fabricates a passing result: when the
validator or coverage check cannot run, results are reported as unavailable
or unverified. As of v1.17.0 strict validation **fails closed**: a missing,
malformed, or provenance-invalid upper-ontology registry makes any graph
using profiled upper-ontology terms non-conforming
(`verification_status: could_not_verify`); malformed extension manifests,
unknown lifecycle statuses, missing dependencies, and dependency cycles are
typed errors instead of silent skips.

## Security Measures

### Static Analysis
- **CodeQL** scanning for Python, C#, and Java on every push and pull request, plus weekly scheduled scans
- **cargo-audit** for Rust dependency vulnerability scanning in CI
- **Dependency review** on pull requests, failing on high-severity dependency changes

### Dependency Management
- **Dependabot** monitors all seven dependency ecosystems (GitHub Actions, pip/Python, pip/generator, NuGet, Maven, Cargo, git submodules) with weekly update checks
- Dependency review gate blocks PRs that introduce known-vulnerable dependencies at high severity or above
- Ontology sources are pinned git submodules; upper-ontology terms are pinned in a committed registry with source provenance

### Build Integrity
- CI builds all four languages from generated source on every push to `main` and `develop`
- CI runs the MCP server test suite (validation, coverage, routing, workspace policy, trust boundary, lifecycle)
- Generated code is reproducible from tagged ontology submodule versions
- All generated artifacts include provenance metadata (`UCO_VERSION`, `CASE_VERSION`) traceable to specific ontology commits

### Release Process
- Releases are triggered by signed tags and built in CI
- Release artifacts include Software Bill of Materials (SBOM) for supply-chain transparency
- Package manifests are version-locked to the repository release version
- **Release checklist** includes reviewing this policy's supported-version
  table and scope statements, and refreshing the upper-ontology registry when
  profiled ontologies publish supported new releases

## Handling Investigative Data

This SDK is used in criminal and civil investigations. Real case data must
never appear in this repository, its issues, its test fixtures, or
vulnerability reports. All bundled fixtures and exemplars are Tier T0
public-safe synthetic data or derive from public court records. Deployments
processing CJIS or similarly regulated data are responsible for their own
compliance assessment; document processing and validation remain local-only,
and secure profiles disable remote SPARQL unless an operator explicitly
enables it. That separation is intended to make the assessment tractable but
does not itself constitute compliance.
