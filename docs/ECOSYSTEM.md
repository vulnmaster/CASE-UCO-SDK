# CASE/UCO Ecosystem

The CASE/UCO SDK produces JSON-LD graphs. This guide covers the companion tools you need to validate and query those graphs, the community projects that extend CASE/UCO into specialized domains, and the upstream ontology sources.

The SDK's own topology — Composition Profiles, incremental generation,
fluent helpers in all four languages, and the VICS/PhotoDNA mapping stub —
is documented in [TOPOLOGY.md](../TOPOLOGY.md). Ready-to-open PR text:
[topology/PR_DESCRIPTION.md](../topology/PR_DESCRIPTION.md).

## Companion Tools

These tools complete the developer workflow — validation, querying, and format conversion for the graphs your SDK code produces.

### case-utils — Validation & CLI Utilities

**[case-utils](https://github.com/casework/CASE-Utilities-Python)** is the primary tool for validating that your SDK output conforms to CASE/UCO SHACL constraints. It is maintained by the CASE community and provides the `case_validate` CLI.

```bash
pip install case-utils
```

Validate a graph produced by the SDK:

```bash
case_validate \
  --built-version case-1.4.0 \
  my-output.jsonld
```

Validate with a custom extension ontology:

```bash
case_validate \
  --built-version case-1.4.0 \
  --ontology-graph path/to/myext.ttl \
  --ontology-graph path/to/myext-shapes.ttl \
  my-output.jsonld
```

`case_validate` uses [PyShacl](https://github.com/RDFLib/pySHACL) under the hood. For performance characteristics at scale, see [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md).

### Apache Jena Fuseki — Graph Database & SPARQL

For combined analysis of multiple graph files, load them into a SPARQL-capable graph database. [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) is free, well-documented, and handles CASE/UCO's JSON-LD and Turtle formats natively.

Use Fuseki when:
- You need to query across multiple partitioned graphs
- Your dataset exceeds comfortable in-memory sizes (see [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md))
- You want to run SPARQL queries for cross-referencing investigation data

### PyShacl — SHACL Validation Engine

[PyShacl](https://github.com/RDFLib/pySHACL) is the SHACL validation engine used by `case_validate`. You generally don't need to call it directly — use `case_validate` instead, which wraps PyShacl with CASE-specific configuration (built version checking, ontology loading, etc.).

### RDFLib — Python RDF Library

[RDFLib](https://github.com/RDFLib/rdflib) is the Python RDF library that underpins `case-utils`, PyShacl, and this SDK's code generator. If you need to do custom RDF processing beyond what the SDK provides (SPARQL queries in Python, graph merging with custom logic, format conversion), RDFLib is the standard tool.

## Community Extensions

CASE/UCO is designed to be extended. These community projects demonstrate the ontology's reach into specialized domains. Each defines its own OWL classes and SHACL shapes that build on top of CASE/UCO, and each can be used alongside the SDK.

The SDK's `case-uco-generate scaffold` command can generate starter code from any of these extensions:

```bash
case-uco-generate scaffold \
  --extension path/to/extension.ttl path/to/extension-shapes.ttl \
  --lang python \
  --output-dir ./my-extension-classes/
```

### CAC Ontology — Crimes Against Children

**[CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology)** is a comprehensive semantic framework with 35+ specialized modules for modeling child exploitation investigations, including grooming, CSAM detection, victim services, multi-jurisdictional operations, and law enforcement coordination. Maintained by [Project VIC International](https://projectvic.org/). The CAC Ontology extends both UCO/CASE and the lightweight Unified Foundational Ontology (gUFO), and includes extensive SHACL validation, real-world example knowledge graphs, and SPARQL query templates.

**Domains covered:** investigations, hotline operations, forensics, detection, grooming, sextortion, victim impact, task force management, legal outcomes, international coordination, and more.

### SOLVE-IT — Digital Forensics Knowledge Base (included in SDK)

**[SOLVE-IT](https://github.com/SOLVE-IT-DF)** (Systematic Objective-based Listing of Various Established digital Investigation Techniques, [solveit-df.org](https://solveit-df.org)) organizes digital forensic practice as objectives → techniques → weaknesses (classified per ASTM E3016-18) → mitigations, enabling systematic Error Mitigation Analysis. The [solve-it-ontology](https://github.com/SOLVE-IT-DF/solve-it-ontology) companion is a CASE/UCO extension ontology (core classes, `SolveitInvestigativeAction`, ~60 method-centric observables, analysis and weakness-assessment modules, SHACL shapes) with an hourly-compiled RDF knowledge base. SOLVE-IT also includes an extension framework ([SOLVE-IT-X](https://github.com/SOLVE-IT-DF/solve-it-x)) for building domain-specific additions.

*Bundled with this SDK* (`ontology/solveit/`) as a pinned snapshot: the ontology modules, the compiled knowledge base (23 objectives, 187 techniques, 339 weaknesses, 270 mitigations), and a generated punned technique catalog for the UCO 1.5.0 `uco-action:Technique` metaclass style. Query it with the `search_solveit` / `get_solveit_details` / `plan_solveit_workflow` MCP tools, model with the [solve-it-investigation-planning recipe](recipes/solve-it-investigation-planning.md), and keep pace with upstream's rapid release cycle via `make sync-solveit` plus a weekly CI freshness check.

**Domains covered:** forensic method and technique selection, error mitigation analysis, tool testing and quality assurance, investigative knowledge management, educational materials.

### Adversary Engagement Ontology — Cyber Denial & Deception

**[Adversary Engagement Ontology (AEO)](https://github.com/UNHSAILLab/Adversary-Engagement-Ontology)** is a UCO sub-ontology for standardizing information representation in cyber adversary engagement operations. It extends UCO with classes for honeypots, breadcrumbs, decoys, lure objects, deception narratives, and adversary engagement objectives, drawing on concepts from MITRE ATT&CK and MITRE ENGAGE.

**Domains covered:** cyber deception, honeypots, adversary engagement operations, red/blue/purple team coordination, cyber threat intelligence.

### toolcap — Forensic Tool Capabilities (included in SDK)

The SDK ships with the **[toolcap extension](../extensions/toolcap/)** as a worked example of extension ontology authoring. It defines classes for comparing digital forensics tool capabilities across artifact types, operating systems, and file systems.

### cryptoinv — Cryptocurrency & Financial Crime Investigation (included in SDK)

The SDK ships with the **[cryptoinv extension](../extensions/cryptoinv/)** covering cryptocurrency observables (address, transaction, wallet, and point-in-time holding facets tracking [UCO issue #675](https://github.com/ucoProject/UCO/issues/675)), financial-crime infrastructure (virtual asset service providers, darknet markets, mixing services — definitions aligned with the [INTERPOL DW-VA Taxonomy](https://github.com/INTERPOL-Innovation-Centre/DW-VA-Taxonomy)), and the criminal legal process (charges, plea agreements, sentencing outcomes, forfeiture and restitution orders, asset seizures). Grounded in and validated against the prosecution record of *U.S. v. Lichtenstein & Morgan* (D.D.C. `1:23-cr-00239-CKK`, the Bitfinex hack laundering case) — see `examples/pacer/doj_crypto_2023_239/`. Passes the CDO Community Playground test suite.

### legalproc — Legal Process and Procedure (included in SDK)

The SDK ships with the **[legalproc extension](../extensions/legalproc/)** — the local implementation of the jurisdiction-neutral criminal legal process stub concepts proposed upstream to CASE ([#192](https://github.com/casework/CASE/issues/192) criminal process, plus `caseIdentifier` from [#191](https://github.com/casework/CASE/issues/191)). It covers charging instruments, criminal charges (with `offenseForm`/`objectOffense` for conspiracy, attempt, and predicate-linked § 924(c) counts), pleas, proceedings, verdicts, sentences, forfeiture, and restitution, for **any** investigation domain. Grounded in and validated against the prosecution record of *U.S. v. Perry & O'Dell* (W.D. Mo. `2:22-cr-04065-BCW`, a 45-count militia conspiracy / attempted-murder case) — see `examples/pacer/wdmo_2022_cr_04065/`. Passes the CDO Community Playground test suite. When CASE adopts the proposed namespaces, these terms re-parent to the CASE terms.

### weapons — Weapons and Firearms (included in SDK)

The SDK ships with the **[weapons extension](../extensions/weapons/)** — investigation-domain classes for weapon evidence (`weap:Weapon`, `weap:Firearm`, `weap:Handgun`, `weap:LongGun`, `weap:Rifle`, `weap:Shotgun`, `weap:CuttingWeapon`, `weap:Ammunition`) with NIEM-aligned properties (`make`, `model`, `caliber`, `serialNumber`, `serialNumberObliterated`). The class tree mirrors the [Common Core Ontologies](https://github.com/CommonCoreOntology/CommonCoreOntologies) Artifact Ontology weapon hierarchy (the BFO 2020 mid-level suite endorsed as a DoD/IC ontology baseline and under IEEE P3195.1 review); bridge files align to CCO (`weapons-profile-cco.ttl`) and ground `weap:Weapon` as `gufo:FunctionalComplex` (`weapons-profile-gufo.ttl`), following the CDO profile pattern. Grounded in and validated against *U.S. v. Lindell et al.* (D.N.D. `3:25-cr-00005`, a kidnapping-for-ransom / drug-conspiracy / firearms case) — see `examples/pacer/ndnd_2025_cr_00005/`. Passes the CDO Community Playground test suite.

### drugs — Controlled Substances (included in SDK)

The SDK ships with the **[drugs extension](../extensions/drugs/)** — a single class, `drug:ControlledSubstance`, representing a seized or charged **portion** of a controlled substance, with properties for CSA schedule (21 U.S.C. § 812), mass, purity, the mixture-vs-actual basis (USSG § 2D1.1), and verbatim charged quantity. Chemical identity is delegated by IRI reference (`drug:substance`) to [ChEBI](https://obofoundry.org/ontology/chebi.html) (OBO Foundry, BFO-compatible) — e.g. `CHEBI_6809` methamphetamine — following the realist analysis of the OBO Drug Ontology (DrOn); the gUFO bridge grounds the portion as `gufo:Quantity` (an amount of matter, not a functional complex). Same grounding case and exemplar as the weapons extension. Passes the CDO Community Playground test suite.

### rico — Racketeering and Criminal Enterprise (included in SDK)

The SDK ships with the **[rico extension](../extensions/rico/)** — investigation-domain classes for racketeering (RICO) prosecutions: `rico:RacketeeringEnterprise` (subclass of `uco-identity:Organization`, with `enterpriseType` recording the 18 U.S.C. § 1961(4) branch — `legal-entity` or `association-in-fact`), `rico:EnterpriseRole` (subclass of `uco-role:Role`, with `roleFunction` for the charged division of labor — organizer, caller, money launderer, database hacker, residential burglar, ...), and the domain-free repeatable `rico:predicateStatute` for the statutory categories of racketeering activity (§ 1961(1)) enumerated in a RICO count. Complements `legalproc` (charges, pleas, sentences) and `cryptoinv` (virtual-asset observables). Grounded in and validated against *U.S. v. Lam et al.* (D.D.C. `1:24-cr-00417-CKK`, the "SE Enterprise" $245M crypto-theft RICO conspiracy) — see `examples/pacer/ddc_2024_cr_00417/`. Passes the CDO Community Playground test suite.

### CDO Community Playground Extensions

The [CDO Community Playground](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) accepts validated extension ontology submissions from the community. These extensions may be AI-generated or human-authored, and are not part of the official published specification. All submissions must validate with `case_validate` and pass the [CASE-Profile-Example](https://github.com/casework/CASE-Profile-Example) test suite.

- **[CASE Ontology Extensions (AI-Generated)](https://github.com/vulnmaster/CASE-Ontology-Extensions-AI-Generated)** — CASE extensions derived from Project VIC International's work implementing CASE/UCO into Autopsy (Rust) for Internet Crimes Against Children (ICAC) taskforce workflows
- **[UCO Extensions (AI-Generated)](https://github.com/vulnmaster/Unified-Cyber-Ontology-Extensions-AI-Generated)** — UCO extensions for the same project

See the [extensions recipe](recipes/extensions.md#cdo-community-playground-testing) for how to test and submit your own extensions to the Playground.

## Extension Packages

The SDK supports extension ontologies as separate, opt-in packages that provide typed bindings for domain-specific ontologies built on CASE/UCO. Each extension package tracks its upstream ontology version independently from the core SDK.

### Available Extension Packages

| Package | Extension | Version | Upper Ontology |
|---------|-----------|---------|----------------|
| `case-uco-cac` | [CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology) | 3.0.0 | gUFO |
| `case-uco-aeo` | [Adversary Engagement Ontology](https://github.com/UNHSAILLab/Adversary-Engagement-Ontology) | 0.2.1 | None |

### Installing Extension Packages

Install only the extensions you need alongside the core SDK:

```bash
# Core CASE/UCO only
pip install case-uco

# Core + CAC Ontology
pip install case-uco case-uco-cac

# Core + AEO
pip install case-uco case-uco-aeo

# All three
pip install case-uco case-uco-cac case-uco-aeo
```

### Cross-Domain Composition

Extension packages can be combined in a single graph:

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cac-core": "https://cacontology.projectvic.org/core#",
    "engagement": "https://ontology.adversaryengagement.org/ae/engagement/",
})
```

### CDO Shapes Compatibility Matrix

When using extensions with CDO Shapes profiles, check compatibility:

| CDO Shapes Profile | CAC Ontology | AEO |
|-------------------|--------------|-----|
| CDO-Shapes-gufo | Included (CAC imports gUFO) | Compatible |
| CDO-Shapes-BFO | Not recommended | Compatible |
| CDO-Shapes-PROV-O | Compatible | Compatible |
| CDO-Shapes-Time | Compatible | Compatible |
| CDO-Shapes-GeoSPARQL | Compatible | Compatible |
| CDO-Shapes-FOAF | Compatible | Compatible |

See the [cross-domain extensions recipe](recipes/cross-domain-extensions.md) for detailed usage examples.

## UCO Profiles — Interoperability with Other Ontologies

UCO is designed as a "mid-level" domain ontology — it deliberately avoids committing to a single top-level (foundational) ontology so that it can interoperate with multiple external ontologies. To explore and formalize these alignments, the UCO community maintains a set of **Profile** repositories that map UCO concepts to other established ontologies.

The [CDO Profile development rationale](https://cyberdomainontology.org/ontology/development/#profiles) explains three types of profiles:

- **Top-level profiles** (BFO, gUFO) — ground UCO in a foundational ontology, enabling reasoning and consistency checking
- **Adopting profiles** (PROV-O, OWL-Time, GeoSPARQL, FOAF) — improve interoperability with widely-used domain ontologies
- **Mimicking profiles** — learn from another ontology's design without importing it (when there's a compatibility issue)

All profiles are currently in **exploratory** status. They define `owl:subClassOf` alignments between UCO classes and the external ontology's classes.

### Available Profiles

| Profile | External Ontology | What it aligns | Useful when you need... |
|---------|------------------|----------------|------------------------|
| [CDO-Shapes-BFO](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-BFO) | [Basic Formal Ontology (BFO 2020)](https://github.com/BFO-ontology/BFO-2020) | UCO classes → BFO categories (Endurant, Perdurant, etc.) | Top-level grounding for formal reasoning, biomedical/scientific ontology interop |
| [CDO-Shapes-gufo](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-gufo) | [gentle Unified Foundational Ontology (gUFO)](https://github.com/nemo-ufes/gufo) | UCO classes → gUFO types and relators | OntoUML-based modeling, the [CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology) uses gUFO |
| [CDO-Shapes-PROV-O](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-PROV-O) | [W3C PROV-O](https://www.w3.org/TR/prov-o/) | UCO actions/provenance → PROV-O Activities, Entities, Agents | Provenance tracking, chain of custody, interop with W3C provenance tooling |
| [CDO-Shapes-Time](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-Time) | [W3C OWL-Time](https://www.w3.org/TR/owl-time/) | UCO temporal concepts → OWL-Time instants and intervals | Temporal reasoning, calendar/clock time modeling, time-bounded existence |
| [CDO-Shapes-GeoSPARQL](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-GeoSPARQL) | [OGC GeoSPARQL 1.1](https://github.com/opengeospatial/ogc-geosparql) | UCO locations → GeoSPARQL Features and Geometries | Geospatial queries, coordinate reference systems, spatial reasoning |
| [CDO-Shapes-FOAF](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-FOAF) | [Friend-of-a-Friend (FOAF)](http://xmlns.com/foaf/0.1/) | UCO identities → FOAF Persons, Organizations, Agents | Social network data, identity linkage, Linked Data interop |

### Using Profiles with the SDK

Profiles are OWL ontology files (`.ttl`) that you can include alongside your CASE/UCO graphs when you need alignment with an external ontology. For example, if your organization uses BFO as its top-level ontology:

```python
graph = CASEGraph(extra_context={
    "bfo": "http://purl.obolibrary.org/obo/",
})

# Your CASE/UCO data is valid on its own.
# The BFO profile adds subclass axioms so that
# UCO objects are also classified under BFO categories,
# enabling cross-ontology SPARQL queries.
graph.write("output.jsonld")

# Validate with the profile included:
# case_validate --ontology-graph uco-bfo.ttl output.jsonld
```

### For Developers Coming from Other Ontologies

If you're already familiar with another ontology and want to model cyber-domain data:

| You know... | Start with this profile | Then use these SDK resources |
|------------|------------------------|------------------------------|
| BFO (biomedical, scientific) | [CDO-Shapes-BFO](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-BFO) | The profile maps BFO's Endurant/Perdurant distinction to UCO classes |
| gUFO / OntoUML | [CDO-Shapes-gufo](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-gufo) | [Existence intervals recipe](recipes/existence-intervals.md) covers gUFO temporal patterns |
| W3C PROV-O (provenance) | [CDO-Shapes-PROV-O](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-PROV-O) | [Chain of custody recipe](recipes/chain-of-custody.md) maps CASE provenance to PROV-O concepts |
| OWL-Time (temporal) | [CDO-Shapes-Time](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-Time) | [Existence intervals recipe](recipes/existence-intervals.md) covers OWL-Time integration |
| GeoSPARQL (geospatial) | [CDO-Shapes-GeoSPARQL](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-GeoSPARQL) | [Location recipe](recipes/location.md) covers GPS and geolocation modeling |
| FOAF (social/identity) | [CDO-Shapes-FOAF](https://github.com/Cyber-Domain-Ontology/CDO-Shapes-FOAF) | [Accounts recipe](recipes/accounts.md) covers identity and account linking |

### Profile Development

The [UCO-Profile-Example](https://github.com/ucoProject/UCO-Profile-Example) repository serves as a template for creating new profiles. Each profile repo follows a consistent structure:

```
CDO-Shapes-*/
├── ontology/          OWL alignment file (e.g., uco-bfo.ttl)
├── shapes/            SHACL shapes (if applicable)
├── tests/             Validation tests
├── dependencies/      Git submodules for UCO and the external ontology
└── Makefile           Build and test automation
```

If you need alignment with an ontology not listed above, you can create a new profile following this pattern and contribute it to the UCO project.

## CDO Project Release Flow

This SDK is a downstream consumer of the CASE and UCO ontologies. Understanding the community release flow helps you know when to expect updates and how the pieces fit together.

The established [CDO project release flow](https://cyberdomainontology.org/resources/project_release_flow.html) works like this:

```
UCO Ontology (source of truth)
  └── CASE Ontology (tracks UCO as a git submodule, releases with each UCO release)
        └── case-utils (compiles monolithic ontology build, published to PyPI)
              └── case-validation-action (GitHub Action for CI validation)
                    └── Downstream tools and implementations
```

**Where this SDK fits:** The SDK tracks UCO and CASE as git submodules (same as CASE tracks UCO). When a new ontology version is released, the SDK regenerates all four language libraries from the updated sources. The SDK uses `case-utils` for validation (`graph.validate()` / `case_validate`).

When upgrading the SDK to a new ontology version:
1. Update the `ontology/UCO` and `ontology/CASE` submodules to the new tags
2. Regenerate: `make generate`
3. Verify: `make check`
4. Validate example outputs with the new `case-utils` version

## Community Mappings and Implementations

The CASE community maintains tool-specific mappings and implementation libraries that document how real forensic tools map to CASE/UCO classes. These are valuable references when building your own tool integrations.

### Mapping Specifications

| Repository | Description | Status |
|-----------|-------------|--------|
| [CASE-Mappings](https://github.com/casework/CASE-Mappings) | Tool-to-CASE concept/property mappings for SleuthKit, Cellebrite, Bulk Extractor, and NSRL | Draft (CASE v0.1.0 era) |
| [CASE-Mapping-Template-Stubs](https://github.com/casework/CASE-Mapping-Template-Stubs) | JSON-LD stub generator for any CASE/UCO class — produces minimal JSON-LD dictionaries with null-valued properties reflecting cardinality | Active (CASE 1.4.0) |
| [CASE-Mapping-Template-Python](https://github.com/casework/CASE-Mapping-Template-Python) | Template repository for adopters to create Python-based CASE mappings | Active |
| [CASE-Mapping-Python](https://github.com/casework/CASE-Mapping-Python) | Python CASE builder library from the EU INSPECTr project (UCD CCI) — a Facet/Object builder pattern similar to this SDK | Active |

> **Note:** The original [CASE-Mappings](https://github.com/casework/CASE-Mappings) were written against CASE v0.1.0 and use older terminology (e.g., `Trace` instead of `ObservableObject`, `CyberItem` instead of the modern Facet pattern). The conceptual mappings are still valuable, but the specific class names should be updated to current ontology versions. This SDK's [MAPPING_GUIDE.md](MAPPING_GUIDE.md) provides current-version class mappings organized by forensic domain.

### Tool Implementations

These repositories are working implementations that convert specific tool outputs into CASE/UCO format. They serve as real-world examples of the mapping process.

| Repository | Tool | Description |
|-----------|------|-------------|
| [CASE-Implementation-UFED-XML](https://github.com/casework/CASE-Implementation-UFED-XML) | Cellebrite UFED | Parser for UFED XML reports |
| [CASE-Implementation-ExifTool](https://github.com/casework/CASE-Implementation-ExifTool) | ExifTool | Maps ExifTool RDF metadata output to CASE/UCO |
| [CASE-Implementation-AXIOM](https://github.com/casework/CASE-Implementation-AXIOM) | Magnet AXIOM | Parser for AXIOM forensic reports |
| [CASE-Implementation-XRY](https://github.com/casework/CASE-Implementation-XRY) | MSAB XRY | Converts XRY reports to CASE format |
| [CASE-Implementation-DC3DD](https://github.com/casework/CASE-Implementation-DC3DD) | DC3DD | CLI wrapper for disk imaging with CASE output |
| [CASE-Implementation-GNU-Time](https://github.com/casework/CASE-Implementation-GNU-Time) | GNU Time | Process timing metadata in CASE format |
| [CASE-Implementation-Plaso](https://github.com/casework/CASE-Implementation-Plaso) | Plaso/log2timeline | Timeline analysis output in CASE |
| [CASE-Implementation-Volatility](https://github.com/casework/CASE-Implementation-Volatility) | Volatility | Memory forensics output in CASE |
| [CASE-Implementation-macOS-System-Profiler](https://github.com/casework/CASE-Implementation-macOS-System-Profiler) | macOS System Profiler | System hardware/software inventory |
| [CASE-Implementation-PROV-O](https://github.com/casework/CASE-Implementation-PROV-O) | PROV-O | W3C Provenance Ontology mapping |

### Templates for New Implementations

| Repository | Description |
|-----------|-------------|
| [CASE-Implementation-Template-Python-CLI](https://github.com/casework/CASE-Implementation-Template-Python-CLI) | Template for Python CLI tools that produce CASE output |
| [CASE-Mapping-Template-Python](https://github.com/casework/CASE-Mapping-Template-Python) | Template for Python-based tool mappings |
| [CASE-Mapping-Template-Stubs](https://github.com/casework/CASE-Mapping-Template-Stubs) | JSON-LD stub generation for bootstrapping new implementations |

When building a new tool integration with this SDK, consider consulting both the community mapping specifications (for conceptual guidance on what maps where) and the implementation repositories (for working code examples).

## Ontology Sources & Standards

The canonical upstream repositories and community resources.

| Resource | Description |
|----------|-------------|
| [UCO Ontology](https://github.com/ucoProject/UCO) | Unified Cyber Ontology — the foundation for all cyber domain ontologies |
| [CASE Ontology](https://github.com/casework/CASE) | Cyber-investigation Analysis Standard Expression — investigation-specific layer on UCO |
| [CASE Examples](https://github.com/casework/CASE-Examples) | Validated example data conforming to CASE/UCO |
| [CASE Profile Example](https://github.com/casework/CASE-Profile-Example) | Extension testing infrastructure and CI patterns |
| [CDO Project Release Flow](https://cyberdomainontology.org/resources/project_release_flow.html) | Interactive diagram of the community release pipeline and adoption status |
| [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) | Requirements and process for submitting community extensions |
| [Cyber Domain Ontology (CDO)](https://cyberdomainontology.org/) | The Linux Foundation project that governs CASE and UCO |

## AI Development Tools

The SDK includes built-in support for AI coding assistants (Cursor, Claude Code, and similar tools).

### Cursor Rules

The `.cursor/rules/` directory contains rules that teach AI agents how to use the SDK correctly:

- **`case-uco-sdk.mdc`** — Core SDK patterns, the ObservableObject + Facet approach, class discovery, validation, and common pitfalls. Applied automatically to every conversation.
- **`extension-authoring.mdc`** — Guidance for writing extension ontology TTL files. Applied when editing files in `extensions/`.

### MCP Server

The `mcp_server/` directory contains a [FastMCP](https://gofastmcp.com/) server that exposes ontology discovery as MCP tools. AI agents can call these tools to find the right classes programmatically:

| Tool | Description |
|------|-------------|
| `search_classes(query, scope)` | Find classes by keyword. Scope: `"all"`, `"core"`, or extension name |
| `get_class_details(name, scope)` | Full property table for a class |
| `find_classes_for_domain(domain, scope)` | Map an investigative task to relevant classes |
| `list_all_facets(scope)` | All Facet classes for the ObservableObject pattern |
| `get_recipe(scenario)` | Find a code recipe for a forensic workflow |
| `list_all_vocabs()` | All vocabulary/enum types |
| `get_uco_profiles(query)` | CDO Shapes profiles with extension compatibility annotations |

The server also exposes MCP resources (`case-uco://domains`, `case-uco://modules`, `case-uco://patterns`) that AI agents can read for orientation.

Setup: `pip install fastmcp` and restart Cursor. The `.cursor/mcp.json` configuration is included in the repository.

See [mcp_server/README.md](../mcp_server/README.md) for detailed setup and usage instructions.

## Adding Your Project

If your project extends CASE/UCO and you'd like it listed here, open a pull request or issue on the [SDK repository](https://github.com/vulnmaster/CASE-UCO-SDK).
