# This CASE/UCO SDK was funded by the nonprofit charity [Project VIC International](https://www.projectvic.org) with the view that these ontologies will be used in conjuction with the [Crimes Against Children Ontology](https://site.cacontology.projectvic.org) and other technical efforts to help the entire world find and safeguard children from sexual exploitation. While this may not be your focus, if you find this CASE/UCO SDK useful and if you use it to make money, please take a minute to become a monthly financial sponsor of Project VIC International via [Our Give Lively](https://secure.givelively.org/donate/project-vic-international-inc).

# CASE/UCO SDK

[![CI](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/ci.yml)
[![CodeQL](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/codeql.yml)
[![Rust Security](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/rust-security.yml/badge.svg?branch=main)](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/rust-security.yml)
[![Upstream Freshness](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/upstream-freshness.yml/badge.svg?branch=main)](https://github.com/vulnmaster/CASE-UCO-SDK/actions/workflows/upstream-freshness.yml)
[![Release](https://img.shields.io/github/v/release/vulnmaster/CASE-UCO-SDK)](https://github.com/vulnmaster/CASE-UCO-SDK/releases/latest)

**v1.26.0** · CASE 1.5.0 · UCO 1.5.0 · CAC 3.1.0 · [Changelog](CHANGELOG.md#1260---2026-08-26)

A multi-language data modeling library for digital forensics, cyber-investigation, and cyber-observable data. If your software produces or consumes forensic evidence, this SDK gives you typed, validated builders in **Python**, **C#**, **Java**, and **Rust** — so you can model investigation data in your language and produce interoperable [CASE/UCO](https://caseontology.org/) JSON-LD output.

The SDK is more than the four language bindings. It ships with a growing family of [extension ontologies](#bundled-extension-ontologies) (crimes against children, adversary engagement, cryptocurrency and financial crime, legal process, racketeering, weapons, controlled substances, MITRE ATT&CK techniques, the SOLVE-IT digital forensics knowledge base, forensic tool capabilities), a [recipe cookbook](docs/recipes/INDEX.md) of 79 modeling patterns, and an [MCP server](#ai-assisted-development) that gives AI agents a working knowledge of the Linux Foundation [Cyber Domain Ontology](https://cyberdomainontology.org/) ecosystem — the ontologies themselves, the upper-ontology profiles (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF), the [CDO Community Playground](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing), and the change-proposal process. Together these let an agent model **any concept adjacent to the cyber domain — or work done on, in, or through it** — and route any investigation submission to validated modeling patterns, drafting upstream ontology proposals when a concept doesn't exist yet.

The SDK works with AI coding assistants (Cursor, Claude Code, Hermes, etc.) — see [AI-Assisted Development](#ai-assisted-development) below.

## What the SDK Does

The SDK is auto-generated from the official CASE 1.5.0 and UCO 1.5.0 ontology sources. Every class, property, and vocabulary term in the published specifications has a corresponding typed class in each language. The generated code gives you:

- **Full core ontology coverage** — all 428 CASE/UCO classes across 15 modules,
  plus discoverable bundled extension classes in the runtime registry
- **Typed properties** with correct JSON-LD serialization (IRIs, typed literals, nested objects)
- **Required-field validation** — ontology-mandated properties are checked before graph insertion
- **Automatic JSON-LD context** — the standard CASE/UCO namespace prefixes are built in; serialized output includes only the prefixes actually used in the graph
- **Deterministic ID support** — use auto-generated UUIDs or supply your own stable IRIs
- **Round-trip capable** — load existing JSON-LD graphs, add objects, and re-serialize

Beyond the generated code, the repository provides:

- **Bundled extension ontologies** — queryable through the same registry and MCP tools as core CASE/UCO (see [Bundled Extension Ontologies](#bundled-extension-ontologies))
- **79 modeling recipes** — end-to-end modeling patterns for forensic workflows and whole investigation types, each grounded in example graphs ([docs/recipes/](docs/recipes/INDEX.md))
- **An MCP server for AI agents** — ontology discovery, investigation routing, document processing, SHACL + concept-coverage validation, remote SPARQL query/analysis, change-proposal drafting, and a resumable critic acceptance loop ([AI-Assisted Development](#ai-assisted-development))
- **A change-proposal pipeline** — when a concept is missing, the tooling searches the UCO, CASE, and CAC issue trackers, drafts a filled-in proposal with tested example data, and supports local extension declarations so work is never blocked on upstream adoption ([change_proposals/](change_proposals/README.md))

## Installation

### Use the SDK (Consumer Install)

Install the SDK package for your language. No need to clone the repo or run the generator.

[**v1.26.0**](https://github.com/vulnmaster/CASE-UCO-SDK/releases/tag/v1.26.0) makes operational recipes fail closed on undeclared ontology terms and unregistered relationship labels, repairs the full catalog identified in #123, and includes Dependabot #122's Rust `uuid` 1.25.0 lockfile update. Release artifacts (wheel, sdist, NuGet package, Maven JAR, and Rust crate, with checksums and attestations) are built from the reviewed tag. Registry publication to PyPI, NuGet, Maven Central, and crates.io remains opt-in. You can also build from source via the CLI or MCP (see [Getting Started](#getting-started) below).

When registry packages are published in a later release:

```bash
pip install case-uco                          # Python (PyPI)
dotnet add package CaseUco                    # C# (NuGet)
cargo add case-uco                            # Rust (crates.io)
```

For Java (once on Maven Central), add to your `pom.xml`:

```xml
<dependency>
    <groupId>org.caseontology</groupId>
    <artifactId>case-uco</artifactId>
    <version>1.26.0</version>
</dependency>
```

For graph validation, also install `case-utils`:

```bash
pip install case-utils    # enables graph.validate() across all languages
```

### Prerequisites

Only install what you need for your language:

| Language | Requirement |
|----------|-------------|
| Python | Python 3.9+ |
| C# | .NET SDK 8.0+ |
| Java | JDK 11+ and Maven |
| Rust | Rust toolchain (cargo) |

### Baseline compute requirements

The SDK does not require a GPU. These figures cover the SDK, language
toolchains, validation data, caches, and generated artifacts; evidence storage
is excluded and must be sized separately.

| Item | Minimum baseline | Recommended |
| --- | ---: | ---: |
| CPU | 4 cores | 8 or more cores for concurrent generation and validation |
| RAM | 8 GB | 16 GB; large in-memory graphs may require 32–64 GB |
| GPU | None | None |
| VRAM (if GPU) | — | — |
| App/DB disk (excluding evidence) | 20 GB | 40 GB or more for build caches and generated artifacts |

See [Compute and Platform Support](docs/COMPUTE.md) for scope, architecture
support, and the native-validation checklist. The machine-readable baseline is
[`catalog/compute.yaml`](catalog/compute.yaml).

### Contribute to the SDK (Developer Install)

If you want to modify the generator, regenerate libraries, run tests, or contribute changes:

```bash
git clone --recurse-submodules https://github.com/vulnmaster/CASE-UCO-SDK.git
cd CASE-UCO-SDK
make init      # create .venv, install Python deps, generator + SDK
make generate  # regenerate all libraries from ontology sources
make build     # build Python, C#, Java, Rust
make test      # run all test suites
make lint      # mypy (Python) + dotnet warnings-as-errors (C#) + javac -Xlint (Java) + clippy (Rust)
make smoke     # run smoke test binaries (C#, Java, Rust)
make check     # all of the above in one command
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor guide.

## Basic Usage

The workflow is the same in every language: create a graph, add typed objects, serialize to JSON-LD.

### Python

```python
from case_uco import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.uco.observable import ObservableObject, ApplicationFacet

graph = CASEGraph(kb_prefix="http://example.org/kb/")

tool = graph.create(Tool, name="My Forensic Tool", version="3.0")
app = graph.create(
    ObservableObject,
    has_facet=[ApplicationFacet(application_identifier="com.example.app")],
)

graph.write("output.jsonld")

# Validate — always validate before using the output
graph.validate()  # requires: pip install case-uco[validation]
```

### C\#

```csharp
using CaseUco;
using CaseUco.Uco.Tool;
using CaseUco.Uco.Observable;

var graph = new CaseGraph("http://example.org/kb/");

var tool = new Tool { Name = "My Forensic Tool", Version = "3.0" };
graph.Add(tool);

var app = new ObservableObject();
app.HasFacet = new List<object> {
    new ApplicationFacet { ApplicationIdentifier = "com.example.app" }
};
graph.Add(app);

graph.Write("output.jsonld");
```

### Java

```java
import org.caseontology.CaseGraph;
import org.caseontology.uco.tool.Tool;
import org.caseontology.uco.observable.*;

CaseGraph graph = new CaseGraph("http://example.org/kb/");

Tool tool = new Tool();
tool.setName("My Forensic Tool");
tool.setVersion("3.0");
graph.add(tool);

ApplicationFacet facet = new ApplicationFacet();
facet.setApplicationIdentifier("com.example.app");
ObservableObject app = new ObservableObject();
app.getHasFacet().add(facet);
graph.add(app);

graph.write("output.jsonld");
```

### Rust

```rust
use case_uco::graph::CaseGraph;
use case_uco::uco::tool::Tool;

let mut graph = CaseGraph::new("http://example.org/kb/");

let tool = Tool::builder()
    .version("3.0".to_string())
    .build();
let id = graph.create(&tool);

let json = graph.serialize().expect("serialization failed");
println!("{json}");
```

## Deterministic IDs

By default, every object gets a UUID-based `@id` like `kb:Tool-550e8400-...`. For pipelines that need stable, reproducible IRIs:

```python
# Python — pass id= to create() or add()
tool = graph.create(Tool, id="kb:Tool-my-stable-id", name="My Tool")
```

```csharp
// C# — use AddWithId()
graph.AddWithId(tool, "kb:Tool-my-stable-id");
```

```java
// Java — use addWithId()
graph.addWithId(tool, "kb:Tool-my-stable-id");
```

```rust
// Rust — use create_with_id()
let id = graph.create_with_id("kb:Tool-my-stable-id", &tool);
```

## Loading Existing Graphs

All runtimes can ingest an existing JSON-LD graph, add new objects, and re-serialize:

```python
graph = CASEGraph()
graph.load_file("existing-case-bundle.jsonld")  # merge context + objects
graph.create(Tool, name="New Tool")             # add more objects
graph.write("enriched-bundle.jsonld")           # write combined graph
```

## Working with Large Datasets

CASE/UCO investigation graphs can grow large quickly — a single DNS record produces 21 RDF triples under the hood, and a full filesystem extraction can generate millions. The SDK provides tools to help you partition, estimate, and manage graph sizes for any compute environment.

### Estimate Before Building

```python
graph = CASEGraph()
# ... add objects ...
print(f"~{graph.estimate_triples()} triples")  # estimate before serializing
```

### Build Many Focused Graphs

Rather than building one massive graph, create focused graphs at the source. Partition by natural forensic boundaries (per-app, per-volume, per-mailbox) — not by arbitrary object count — because investigation objects reference each other and naive splitting breaks those relationships.

```python
# Good: one graph per app extracted from a mobile device
for app_id in discovered_apps:
    graph = CASEGraph()
    # ... add all objects for this app (tool, observables, actions) ...
    graph.write(f"mobile-{app_id}.jsonld")

# Then merge or load into a graph database for combined analysis
combined = CASEGraph.merge_files([
    "mobile-com.example.messenger.jsonld",
    "mobile-com.example.browser.jsonld",
])
```

**When is `split()` safe?** The `split()` helper is appropriate for catalog-style graphs where objects are independent (e.g., a flat list of file hashes, DNS records, or IoC entries). It is **not safe** for graphs with cross-object relationships (e.g., investigative actions referencing tools and observables), because it splits by object index without preserving reference integrity.

### Hardware Sizing Quick Reference

| Environment | RAM | Comfortable Max |
|-------------|-----|----------------|
| Laptop (16 GB) | 16 GB | ~32K objects (~672K triples) |
| Workstation (32 GB) | 32 GB | ~64K objects (~1.3M triples) |
| Workstation (64 GB) | 64 GB | ~256K objects (~5.4M triples) |
| Graph Database | Any | Unlimited (disk-backed) |

For detailed benchmarks, partitioning strategies, validation tool comparisons, and graph database integration examples, see **[docs/PERFORMANCE_GUIDE.md](docs/PERFORMANCE_GUIDE.md)**.

## Bundled Extension Ontologies

Core CASE/UCO covers cyber-observables and investigation management, but real investigations reach into domains the core ontology doesn't cover. The SDK bundles ten extension ontologies, all queryable through the same registry, CLI explorer, and MCP tools as core classes (set `CASE_UCO_EXTENSIONS` or use the `scope` parameter to include them). Upstream-maintained ontologies (`cac`, `aeo`, `solveit`) are vendored under `ontology/` alongside CASE and UCO and refreshed with `make sync-upstream`; SDK-developed extensions live under `extensions/`:

| Extension | Version | Domain |
|-----------|---------|--------|
| [`cac`](ontology/cac/) | 3.0.0 | [Crimes Against Children Ontology](https://site.cacontology.projectvic.org) — 35+ modules for CSAM, trafficking, grooming, sextortion, hotline intake, task force operations, and federal prosecution |
| [`aeo`](ontology/aeo/) | 0.2.1 | [Adversary Engagement Ontology](https://github.com/UNHSAILLab/Adversary-Engagement-Ontology) — cyber deception, honeypots, and adversary engagement operations |
| [`attack-technique`](extensions/attack-technique/) | 0.1.0 | MITRE ATT&CK technique metaclass (forward-implementation of UCO PR #676) plus a technique catalog for CTI and APT reporting |
| [`solveit`](ontology/solveit/) | 0.1.9 | [SOLVE-IT](https://solveit-df.org) digital forensics knowledge base — objectives, techniques, weaknesses (ASTM E3016-18), mitigations; pinned upstream snapshot with `SolveitInvestigativeAction`, method-centric observables, weakness assessment, and a punned technique catalog for the UCO 1.5.0 metaclass style |
| [`cryptoinv`](extensions/cryptoinv/) | 0.1.0 | Cryptocurrency and financial-crime investigation — typed crypto facets, blockchain tracing, exchange records |
| [`legalproc`](extensions/legalproc/) | 0.1.0 | Legal process — charges, verdicts, pleas, sentences, forfeiture, restitution for any investigation type |
| [`rico`](extensions/rico/) | 0.1.0 | Racketeering and criminal enterprise — association-in-fact enterprises, enterprise roles, predicate statutes |
| [`weapons`](extensions/weapons/) | 0.1.0 | Firearms and ammunition evidence (CCO Artifact Ontology + gUFO bridges) |
| [`drugs`](extensions/drugs/) | 0.1.0 | Controlled-substance evidence — ChEBI identity, CSA schedules, mass and purity |
| [`toolcap`](extensions/toolcap/) | 0.4.0 | Forensic tool capability benchmarking — decomposed Tool → Module → Capability model with IR metrics and AutoDFBench provenance |

Extensions compose: a single graph can combine core observables with CAC victim identification, `legalproc` charges, and `cryptoinv` blockchain traces. See the [cross-ontology composition recipe](docs/recipes/cross-ontology-composition.md).

## Extending the Ontology

The SDK works with extension ontologies out of the box. If CASE/UCO doesn't cover your domain, you can define new classes in OWL Turtle and use them alongside the generated types.

### Step 1: Define Your Extension Ontology

Create a `.ttl` file with your new classes and properties. Every class must subclass an existing UCO/CASE class:

```turtle
@prefix myext: <http://example.org/ontology/myext/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

myext:MyCustomObject
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "MyCustomObject"@en ;
    rdfs:comment "A domain-specific object for my use case."@en ;
    .

myext:customProperty
    a owl:DatatypeProperty ;
    rdfs:label "customProperty"@en ;
    rdfs:comment "A property specific to my extension."@en ;
    rdfs:domain myext:MyCustomObject ;
    rdfs:range xsd:string ;
    .
```

### Step 2: Scaffold Typed Classes

Use the built-in scaffold command to auto-generate starter classes for all four languages:

```bash
# Generate starter classes from your extension TTL + validation shapes
case-uco-generate scaffold \
  --extension path/to/myext.ttl path/to/myext-shapes.ttl \
  --output-dir my_project/

# Generate for a single language
case-uco-generate scaffold \
  --extension path/to/myext.ttl \
  --lang python \
  --output-dir my_project/
```

This produces typed dataclasses (Python), C# classes, Java POJOs, and Rust structs with all properties, cardinalities, and IRIs pre-filled.

### Step 3: Use the Scaffolded Classes

Import the generated classes and use them like any built-in SDK type:

```python
from myext_classes import MyCustomObject
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "myext": "http://example.org/ontology/myext/",
})

graph.add(MyCustomObject(custom_property="my value"))
print(graph.serialize())
```

### Step 4: Validate with case_validate

If you plan to share your extension with the CDO community, validate your exemplar data:

```bash
pip install case-utils

case_validate --built-version case-1.4.0 \
  --ontology-graph path/to/myext.ttl \
  --inference rdfs --allow-info \
  path/to/myext-exemplar.ttl
```

See the [bundled extensions](#bundled-extension-ontologies) for complete, validated examples of this pattern. When an extension proves broadly useful, the next step is upstreaming: the [change-proposal pipeline](#gap-detection-and-change-proposals) turns a local extension into a formal UCO or CASE proposal. See the [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) for submission requirements.

## Discovering Classes

With 428+ classes across 15 modules, finding the right class for your use case can be challenging. The SDK provides four ways to navigate the ontology.

### CLI Ontology Explorer

Search and browse the entire ontology from your terminal:

```bash
pip install -e generator/

# Search by keyword
case-uco-explore search "file"

# Get full details for a class (properties, types, inheritance)
case-uco-explore class FileFacet

# List all modules
case-uco-explore modules

# Browse a specific module
case-uco-explore module observable

# View inheritance hierarchy
case-uco-explore hierarchy Tool

# Find classes by property type
case-uco-explore properties --type Tool
```

The explorer includes extension ontologies by default. Use `--no-extensions` to browse only core CASE/UCO.

### Runtime Introspection (All Languages)

Every language in the SDK includes a runtime registry backed by the same auto-generated `_registry.json`. Search, list, and query available object types programmatically without leaving your IDE.

**Python:**

```python
from case_uco.registry import search, get_class, find_facets, list_modules

results = search("browser")
for r in results:
    print(f"{r['name']:30s} {r['module']}")

info = get_class("FileFacet")
for prop in info["properties"]:
    print(f"  {prop['name']:20s} {prop['type']:15s} required={prop['required']}")
```

**C#:**

```csharp
using CaseUco;

var results = OntologyRegistry.Search("browser");
foreach (var r in results)
    Console.WriteLine($"{r["name"],-30} {r["module"]}");

var info = OntologyRegistry.GetClass("FileFacet");
// Also: ListModules(), ListClasses(), FindFacets(), FindByPropertyType(), ListVocabs()
```

**Java:**

```java
import org.caseontology.OntologyRegistry;

var results = OntologyRegistry.search("browser");
for (var r : results)
    System.out.printf("%-30s %s%n", r.get("name"), r.get("module"));

var info = OntologyRegistry.getClass("FileFacet");
// Also: listModules(), listClasses(), findFacets(), findByPropertyType(), listVocabs()
```

**Rust:**

```rust
use case_uco::registry;

let results = registry::search("browser");
for cls in &results {
    println!("{:30} {}", cls.name, cls.module);
}

let info = registry::get_class("FileFacet").unwrap();
// Also: list_modules(), list_classes(), find_facets(), find_by_property_type(), list_vocabs()
```

### Ontology Reference

A complete auto-generated reference of every class, property, and vocabulary type:

- **[ONTOLOGY_REFERENCE.md](ONTOLOGY_REFERENCE.md)** — full class reference with property tables, organized by module

### Domain Mapping Guide

Don't know which CASE/UCO class fits your data? The mapping guide organizes classes by forensic domain:

- **[docs/MAPPING_GUIDE.md](docs/MAPPING_GUIDE.md)** — maps common concepts (files, network, devices, email, mobile, etc.) to the right classes, with usage examples

### Cross-Language Parity

Switching between languages? The parity contract documents what is identical vs. language-idiomatic:

- **[docs/CROSS_LANGUAGE_PARITY.md](docs/CROSS_LANGUAGE_PARITY.md)** — canonical operation names, naming conventions, stability guarantees

### Recipes

79 step-by-step patterns, each grounded in example graphs. Coverage spans classic forensic workflows (disk imaging, file systems, network artifacts, chain of custody, mobile forensics including iOS/macOS sysdiagnose and Apple Unified Logs) and whole investigation types: fraud and cryptocurrency laundering, elder fraud, espionage and classified disclosure, export control and sanctions evasion, cyber threat intelligence and APT reporting, insider threat and trade secrets, racketeering, weapons and drug evidence, cargo theft, upper-ontology composition, and a 16-recipe Crimes Against Children series (trafficking networks, CSAM provenance, sextortion, hotline intake, task force operations, federal prosecution, PACER document ingestion):

- **[docs/recipes/](docs/recipes/INDEX.md)** — practical cookbook with copy-paste examples (one file per recipe)

The catalog is self-improving: the [recipe-authoring recipe](docs/recipes/recipe-authoring.md) documents how to write a new recipe — or correct an existing one that a live case proved wrong or incomplete — and register it with the MCP server's recipe index, so every investigation the tooling handles can feed improvements back into the catalog.

## SDK Architecture

```
CASE-UCO-SDK/
├── generator/              Code generator + CLI explorer + docs generators
├── ontology/               Upstream-vendored ontologies (refreshed via `make sync-upstream`)
│   ├── UCO/                UCO 1.4.0 sources (git submodule)
│   ├── CASE/               CASE 1.4.0 sources (git submodule)
│   ├── cac/                Crimes Against Children Ontology (Project VIC, submodule)
│   ├── aeo/                Adversary Engagement Ontology (submodule)
│   ├── solveit/            SOLVE-IT knowledge base + ontology (pinned snapshot)
│   └── upper/              Pinned upper-ontology sources + CDO-Shapes profiles (offline)
├── python/                 Generated Python library (case-uco) + runtime registry
│   └── tests/              pytest suite + exhaustive instantiation tests
├── csharp/                 Generated C# library (CaseUco, netstandard2.0)
│   ├── CaseUco.Tests/      xUnit tests + exhaustive instantiation tests
│   └── CaseUco.Smoke/      Smoke test binary (import + serialize)
├── java/                   Generated Java library (org.caseontology)
│   └── src/test/           JUnit tests + exhaustive instantiation tests
├── rust/                   Generated Rust crate (case-uco)
│   ├── tests/              Integration + exhaustive instantiation tests
│   └── examples/smoke.rs   Smoke test binary (import + serialize)
├── extensions/             SDK-developed extension ontologies (queryable via registry + MCP)
│   ├── attack-technique/   MITRE ATT&CK technique metaclass + catalog
│   ├── cryptoinv/          Cryptocurrency and financial-crime investigation
│   ├── legalproc/          Legal process (charges, verdicts, sentences)
│   ├── rico/               Racketeering and criminal enterprise
│   ├── weapons/            Firearms and ammunition evidence
│   ├── drugs/              Controlled-substance evidence
│   └── toolcap/            Forensic tool capability benchmarking (v0.4.0)
├── mcp_server/             MCP server for AI-assisted development
│   ├── server.py           FastMCP server: discovery, routing, validation, proposals
│   ├── sparql_client.py    Bounded query-only remote SPARQL client
│   └── domain_index.py     Task-to-class mappings, recipe index, and proposal triage
├── change_proposals/       Drafted ontology change proposals (markdown + OWL + SHACL + JSON-LD + SPARQL)
├── .cursor/
│   ├── rules/              AI agent guidance (SDK patterns, gap detection)
│   └── mcp.json            MCP server configuration
├── docs/
│   ├── ECOSYSTEM.md            Companion tools, community extensions, ontology sources
│   ├── MAPPING_GUIDE.md        Domain mapping guide (auto-generated)
│   ├── PERFORMANCE_GUIDE.md    Engineering tradeoffs and benchmarks
│   ├── CROSS_LANGUAGE_PARITY.md  API parity contract across languages
│   ├── SPARQL.md               Remote query guide and validated graph-load roadmap
│   ├── templates/              Official change proposal template
│   └── recipes/                Practical forensic workflow cookbook (one file per recipe)
│       ├── INDEX.md         Recipe catalog and shared guidance
│       ├── chain-of-custody.md
│       ├── change-proposal.md
│       ├── forensic-tool.md
│       ├── starter-*.md     End-to-end mapping starter kits (4 recipes)
│       ├── cac-*.md         Crimes Against Children recipe series (16 recipes)
│       └── ...              (77 recipes total)
├── ONTOLOGY_REFERENCE.md   Complete class reference (auto-generated)
├── SECURITY.md             Vulnerability reporting policy
├── .github/workflows/      CI, CodeQL, Rust security, dependency review, release workflows
└── Makefile                Build orchestration (make check for full verification)
```

## Feature Matrix

| Feature | Python | C# | Java | Rust |
|---------|--------|----|------|------|
| Full typed classes (428 classes) | Yes | Yes | Yes | Yes |
| JSON-LD serialization | Yes | Yes | Yes | Yes |
| Custom / deterministic IDs | `create(id=)` | `AddWithId()` | `addWithId()` | `create_with_id()` |
| Load existing JSON-LD | `load()` / `load_file()` | `Load()` | `load()` / `loadFile()` | `load()` / `load_file()` |
| Required-field validation | Yes | Yes | Yes | Yes |
| Static type checking / linting | mypy (strict) | warnings-as-errors | javac -Xlint -Werror | clippy |
| Exhaustive instantiation tests | Yes | Yes | Yes | Yes |
| Smoke test binary | — | `CaseUco.Smoke` | `SmokeTest` | `examples/smoke` |
| Object count | `len(graph)` | `Count` | `size()` | `len()` |
| Triple estimation | `estimate_triples()` | `EstimateTriples()` | `estimateTriples()` | `estimate_triples()` |
| Graph split (catalog data only) | `split()` | `Split()` | `split()` | `split()` |
| Multi-file merge | `merge_files()` | `MergeFiles()` | `mergeFiles()` | `merge_files()` |
| Typed deserialization | `from_jsonld()` | `FromJsonLd()` | `fromJsonLd()` | `from_jsonld()` |
| Graph validation (SHACL) | `validate()` | `ValidateGraph()` | `validate()` | `validate()` |
| Runtime introspection | `case_uco.registry` | `OntologyRegistry` | `OntologyRegistry` | `registry` module |
| Provenance metadata | `UCO_VERSION` | `CaseUcoMeta` | `CaseUcoMeta` | `VERSION` |

## Version Matrix

All four language packages are released in lockstep from the same ontology sources and share the same version number.

| SDK Version | UCO | CASE | Python `case-uco` | C# `CaseUco` | Java `case-uco` | Rust `case-uco` |
|-------------|-----|------|-------------------|--------------|-----------------|-----------------|
| 1.26.0 | 1.5.0 | 1.5.0 | 1.26.0 | 1.26.0 | 1.26.0 | 1.26.0 |
| 1.25.0 | 1.5.0 | 1.5.0 | 1.25.0 | 1.25.0 | 1.25.0 | 1.25.0 |
| 1.24.0 | 1.5.0 | 1.5.0 | 1.24.0 | 1.24.0 | 1.24.0 | 1.24.0 |
| 1.23.1 | 1.4.0 | 1.4.0 | 1.23.1 | 1.23.1 | 1.23.1 | 1.23.1 |
| 1.23.0 | 1.4.0 | 1.4.0 | 1.23.0 | 1.23.0 | 1.23.0 | 1.23.0 |
| 1.22.4 | 1.4.0 | 1.4.0 | 1.22.4 | 1.22.4 | 1.22.4 | 1.22.4 |
| 1.22.2 | 1.4.0 | 1.4.0 | 1.22.2 | 1.22.2 | 1.22.2 | 1.22.2 |
| 1.22.1 | 1.4.0 | 1.4.0 | 1.22.1 | 1.22.1 | 1.22.1 | 1.22.1 |
| 1.22.0 | 1.4.0 | 1.4.0 | 1.22.0 | 1.22.0 | 1.22.0 | 1.22.0 |
| 1.21.0 | 1.4.0 | 1.4.0 | 1.21.0 | 1.21.0 | 1.21.0 | 1.21.0 |
| 1.20.0 | 1.4.0 | 1.4.0 | 1.20.0 | 1.20.0 | 1.20.0 | 1.20.0 |
| 1.19.0 | 1.4.0 | 1.4.0 | 1.19.0 | 1.19.0 | 1.19.0 | 1.19.0 |
| 1.18.0 | 1.4.0 | 1.4.0 | 1.18.0 | 1.18.0 | 1.18.0 | 1.18.0 |
| 1.17.0 | 1.4.0 | 1.4.0 | 1.17.0 | 1.17.0 | 1.17.0 | 1.17.0 |
| 1.16.0 | 1.4.0 | 1.4.0 | 1.16.0 | 1.16.0 | 1.16.0 | 1.16.0 |
| 1.15.0 | 1.4.0 | 1.4.0 | 1.15.0 | 1.15.0 | 1.15.0 | 1.15.0 |
| 1.14.0 | 1.4.0 | 1.4.0 | 1.14.0 | 1.14.0 | 1.14.0 | 1.14.0 |
| 1.11.0 | 1.4.0 | 1.4.0 | 1.11.0 | 1.11.0 | 1.11.0 | 1.11.0 |
| 1.10.0 | 1.4.0 | 1.4.0 | 1.10.0 | 1.10.0 | 1.10.0 | 1.10.0 |
| 1.9.0 | 1.4.0 | 1.4.0 | 1.9.0 | 1.9.0 | 1.9.0 | 1.9.0 |
| 1.8.0 | 1.4.0 | 1.4.0 | 1.8.0 | 1.8.0 | 1.8.0 | 1.8.0 |


To check at runtime:

```python
import case_uco
print(case_uco.UCO_VERSION)   # "1.4.0"
print(case_uco.CASE_VERSION)  # "1.4.0"
```

## AI-Assisted Development

The SDK is designed to work with AI coding assistants like Cursor, Claude Code, and similar tools. When you open this project in a supported IDE, the AI agent automatically knows how to use the SDK — which classes to pick, how to build graphs, and how to validate output.

The MCP server is the centerpiece. It carries a working knowledge of the entire Linux Foundation [Cyber Domain Ontology](https://cyberdomainontology.org/) project — not just class lookup, but the ecosystem around it:

- **Core + extension discovery** — every tool accepts a `scope` parameter, so the agent can search core CASE/UCO, the CAC Ontology, the Adversary Engagement Ontology, or any bundled extension with the same calls.
- **Upper-ontology profiles** — `get_uco_profiles` surfaces UCO's alignments with BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, and FOAF, so graphs can interoperate with formal-reasoning, provenance, temporal, geospatial, and social-network tooling. Since v1.19.0 the upper-ontology sources and CDO-Shapes SHACL profiles are vendored under `ontology/upper/` (each profile reports its `local_source` / `local_shapes` paths), so profile inspection, conformance checks, and registry rebuilds all work fully offline. Remote SPARQL is an optional, explicitly controlled network capability rather than a prerequisite for local modeling or validation.
- **Investigation routing** — `route_investigation_content` classifies any submission (text, documents, partial graphs) into investigation families and returns the matching recipes, extensions, namespaces, and profiles; `route_cac_content` does deep routing within the crimes-against-children domain. Since v1.16.0 routing is hybrid: a deterministic keyword baseline plus an offline lexical-semantic stage with synonym expansion, per-family confidence scores, explainable match evidence, and calibrated abstention — colloquial phrasings route correctly, unknown content gets extension-gap guidance instead of a weak guess.
- **Forensic method planning** — `plan_solveit_workflow` maps an investigation goal to [SOLVE-IT](https://solveit-df.org) objectives, candidate techniques, and per-technique weakness/mitigation checklists (ASTM E3016-18 Error Mitigation Analysis); `search_solveit` and `get_solveit_details` query the pinned knowledge base (23 objectives, 187 techniques, 339 weaknesses, 270 mitigations), and the `solveit` extension records the method in the graph via `SolveitInvestigativeAction` or the punned technique classes — kept current against SOLVE-IT's rapid release cycle with `make sync-solveit` and a weekly CI freshness check.
- **Document processing** — `process_document_file` turns images, PDFs, Office documents, CSV tables, and PACER court filings into bounded CASE/UCO JSON-LD for human review. All extracted content is labeled untrusted evidence data, scanned for prompt-injection patterns, and confined by the configurable filesystem workspace policy (see [SECURITY.md](SECURITY.md)).
- **Remote SPARQL query and analysis** — `execute_sparql_query` combines local ontology discovery with a bounded query-only SPARQL 1.1 client. It targets CaseLinker's public CASE/UCO/CAC corpus by default, accepts other standards-compliant endpoints, normalizes bindings/ASK/RDF results, and labels every remote value as untrusted external data. See [Remote SPARQL Query and Graph-Store Roadmap](docs/SPARQL.md).
- **Validation** — the public Python API `case_uco.validation.validate_graph_file` (and MCP `validate_graph`) runs SHACL validation plus a closed-world concept-coverage check against core, loaded extensions, and profiled upper ontologies. Coverage is exact-term and role-aware: profiled upper-ontology terms (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF) are checked against pinned releases (`python/case_uco/validation/upper_ontology_registry.json`) so fabricated terms fail, and declared terms used in the wrong RDF position (a class as a predicate, a property as a type) are reported as role mismatches. The declared-term set refreshes automatically when ontology files change mid-process. Since v1.17.0 strict validation fails closed: reports carry a `verification_status`, and a missing or invalid registry, malformed extension manifest, missing dependency, or dependency cycle is a typed error rather than a silent pass. **Named extensions are an external-bundle contract:** the PyPI/GitHub wheel does not vendor `extensions/` Turtle files; pass `project_root=` (or explicit ontology paths) pointing at a CASE-UCO-Libraries checkout when using names such as `attack-technique:full`.
- **Knowledge lifecycle** — learned recipes and extension ontologies follow a staged candidate → validated → operational → deprecated lifecycle with validation-gated promotion, recorded provenance, emergency revocation, and one-command git rollback (`make promote-extension` / `promote-recipe` / `deprecate-extension` / `deprecate-recipe` / `rollback-extension` / `lifecycle-status`). Promotion gates require conforming exemplars, failing negative fixtures when SHACL shapes ship, subclass anchoring to declared classes, and (when declared) passing competency queries; promotion authority follows the deployment profile.
- **Secure deployment** — a filesystem workspace policy confines file-handling tools to configured read/write roots, and deployment profiles (`development`, `offline-investigation`, `production-authoring`, `production-review`) make it enforceable: in secure mode the server refuses to start on a misconfigured policy and fails closed at runtime, and `get_security_profile` reports the active posture. Routing quality is guarded by a held-out external evaluation corpus (`evaluation/routing/`, `make eval-routing`) that runs in CI with a governance rule preventing silent co-modification of router and corpus.
- **CDO community awareness** — the server knows the [Community Playground](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) submission requirements and the UCO/CASE/CAC change-proposal process, so its output is aimed at upstream adoption rather than one-off hacks.

The result: if a concept touches the cyber domain — or describes work done on, in, or through it — the agent can model it. When the ontology has a gap, the agent doesn't stop; it drafts a local extension to unblock the work and a formal change proposal to close the gap upstream. And because recipes are updated when live cases prove them wrong or incomplete ([recipe-authoring](docs/recipes/recipe-authoring.md)), the system improves with use.

### Critic loop and SDK self-improvement

v1.22 adds a **critic acceptance loop** that works with — but stays separate from — that self-improvement cycle. Together they let the SDK grow with the user while modeling stays grounded in, and extends, the open Cyber Domain Ontology family.

```text
Originating agent  →  builds serializer + CASE/UCO graph via MCP discovery/routing
        ↓
Critic loop (#74–#78)  →  deterministic checks + independent critic pass(es)
        ↓                 structured findings; hash-bound, tamper-evident sessions
Originating agent  →  revises the current artifact (not the SDK catalog)
        ↓
Finalize  →  accepted / completed_with_findings / blocked…
        ↘ optional operator-approved handoff only
SDK self-improvement  →  recipes, extensions, change proposals, routing index
```

- **Critic loop (artifact improvement):** MCP tools such as `start_critic_review`, `submit_critic_revision`, and `finalize_critic_review` review one immutable graph/serializer version at a time. Deterministic SHACL, coverage, heuristics, and serializer checks run before any model critique. Sampling is client-controlled and marking-aware; offline/manual modes never require a cloud provider. Sessions under `critic-sessions/` are resumable, audit-chained, and projection-bound so later passes cannot quietly rewrite prior findings or config. See [`docs/critic/RULES.md`](docs/critic/RULES.md).
- **Self-improvement loop (persistent knowledge):** gap detection, local extension playgrounds, upstream change proposals, and recipe/extension lifecycle promotion improve what the MCP server knows for the *next* investigation. The critic may emit handoff *candidates* (recipe gap, ontology gap, SDK bug), but `prepare_critic_handoff` writes only under explicit operator approval — never silent catalog mutation.

Net effect: each investigation can raise the quality of the current graph through the critic, while approved learnings feed back into recipes and ontologies so the MCP server keeps improving modeling results for the user without bypassing validation or open-ontology process.

### How It Works

1. **Cursor rules** (`.cursor/rules/`) teach the AI agent the core SDK patterns, the ObservableObject + Facet modeling approach, and common pitfalls — so it writes correct code on the first try.

2. **MCP server** (`mcp_server/`) provides programmatic ontology discovery tools. Instead of reading documentation, the AI agent can call `search_classes("mobile")` or `find_classes_for_domain("email evidence")` to find exactly the right types for your scenario.

3. **Domain-oriented task mappings** translate natural-language descriptions ("model a disk image extraction") into the specific classes needed, so you can describe your forensic workflow and get correct code.

### Setup

The Cursor rules are included automatically. To enable the MCP server:

```bash
pip install fastmcp
```

Then restart Cursor — the `.cursor/mcp.json` configuration will be detected and the server started. Open Cursor's MCP panel (Settings > Tools & MCP) and confirm the "case-uco" server shows as connected.

To load extension registries (CAC, AEO, and the rest), set `CASE_UCO_EXTENSIONS` in the server environment to a comma-separated list of extension names, e.g. `cac,aeo,cryptoinv,legalproc,rico,weapons,drugs,attack-technique,solveit`. The `scope` parameter on discovery tools then filters by `core`, an extension name, or `all`.

### MCP Tools Reference

The MCP server exposes tools and read-only context resources that the AI agent
calls behind the scenes:

| Tool | What it does |
|------|-------------|
| `search_classes` | Find classes by keyword match on name or description (core + extensions via `scope`) |
| `get_class_details` | Full property table for a class (types, cardinalities, required flags) |
| `find_classes_for_domain` | Map a natural-language forensic task to the right classes, with related recipes and starter kits |
| `list_all_facets` | All Facet classes for the ObservableObject + Facet pattern |
| `list_all_vocabs` | All vocabulary/enum types with their valid members |
| `get_uco_profiles` | UCO profile alignments with BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, and FOAF |
| `suggest_classes_for_input` | Prescriptive class suggestions with modeling warnings for a concept |
| `get_recipe` | Retrieve the single best-matching recipe with full content inline |
| `get_recipes` | Ranked multi-recipe retrieval for scenarios spanning several patterns |
| `guide_mapping` | Step-by-step mapping guidance for an evidence source with code skeleton |
| `route_investigation_content` | Classify any submission into investigation families → recipes, extensions, namespaces, profiles |
| `route_cac_content` | Deep Crimes Against Children domain routing with modeling checklists |
| `search_solveit` | Keyword search across the pinned SOLVE-IT knowledge base (objectives, techniques, weaknesses, mitigations) |
| `get_solveit_details` | Full SOLVE-IT record with relationships — technique → weaknesses → mitigations, ASTM categories, CASE I/O classes |
| `plan_solveit_workflow` | Map an investigation goal to SOLVE-IT objectives, candidate techniques, and an error-mitigation checklist |
| `execute_sparql_query` | Run bounded query-only SPARQL 1.1 against CaseLinker by default or another standards-compliant endpoint |
| `process_document_file` | Process images, PDFs, Office docs, CSV tables, and PACER filings into bounded CASE/UCO JSON-LD |
| `validate_graph` | SHACL validation plus closed-world concept-coverage check against core, extensions, and profiles |
| `check_existing_proposals` | Search open UCO/CASE/CAC GitHub issues for prior change proposals |
| `draft_change_proposal` | Generate a filled-in change proposal from concept, scenario, and proposed classes |

Resources (read-only context): `case-uco://domains`, `case-uco://profiles`, `case-uco://modules`, `case-uco://patterns`, `case-uco://sparql`.

### What You Can Say

Describe what you need in plain language. The agent uses the MCP tools to find the right classes, reads the matching recipe for the correct pattern, writes SDK code, and validates the output — all in one pass.

- "Model the results of a Cellebrite extraction from a Samsung Galaxy with WhatsApp messages and GPS data"
- "Create a chain of custody record for evidence received from a field office"
- "I captured this pcapng with Wireshark on my WiFi interface — model it"
- "Model a mobile device with SIM card, IMEI, and carrier info"
- "Create a forensic analysis result classifying a file as malware with confidence 0.92"
- "Model a two-step AI image analysis pipeline with ranked results and similarity scores"
- "I need to model a Bitcoin wallet on a sanctions list — is there a class for that?"
- "Here's a PACER indictment PDF — extract it into a CASE graph with charges and defendants"
- "Model this APT report with the threat actor, malware family, and ATT&CK techniques"
- "This is a pig-butchering fraud case with crypto tracing and an exchange subpoena — model it end to end"
- "Model the firearms and drug evidence seized in this search warrant"
- "Plan the acquisition of this seized laptop with SOLVE-IT — which techniques, what can go wrong, and which mitigations should we apply?"
- "Draft a change proposal for modeling drone telemetry data"

### Typical Agent Workflow

When you describe a forensic scenario, the agent follows this workflow:

```
1. find_classes_for_domain("network packet capture")    → relevant classes
2. get_class_details("TCPConnection")                    → property table
3. get_recipe("network investigation")                   → code pattern
4. Writes Python script using the SDK                    → output.py
5. Runs the script                                       → output.jsonld
6. Validates with case_validate                          → Conforms: True
```

The agent also applies conventions from the recipes automatically — for example, tagging `Relationship` objects with `observed`, `inferred`, or `configuration` to classify evidence basis, and using the three-layer model (acquisition, observed facts, analysis) for investigation graphs.

### Gap Detection and Change Proposals

When you ask to model something the ontology doesn't cover yet, the agent detects the gap and offers to draft a formal change proposal for the UCO or CASE ontology committees:

```
1. search_classes("cryptocurrency"), search_classes("wallet")  → no matches
2. find_classes_for_domain("blockchain forensics")             → no task templates
3. get_class_details("DigitalAddress")                         → confirm near-miss
4. check_existing_proposals("cryptocurrency wallet")           → no prior proposals
5. Agent drafts proposal with proposed classes, SPARQL, JSON-LD examples
6. Writes filled-in template to change_proposals/              → ready for review
```

The agent automatically determines whether the concept belongs in UCO (general cyber-domain) or CASE (investigation-specific), checks for existing proposals in the UCO, CASE, and CAC GitHub issue trackers, and generates a complete proposal with competency questions, tested SPARQL queries, and validated example instance data. See the [change proposal recipe](docs/recipes/change-proposal.md) for details.

Crucially, a gap never blocks the work: the agent can declare a local extension ontology (following the [Community Playground](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) rules) so the investigation graph validates today, while the formal proposal works its way through upstream review. Several of the [bundled extensions](#bundled-extension-ontologies) began exactly this way. This gap-detect → extend-locally → propose-upstream → recipe-update cycle is the SDK's self-improvement loop.

Drafted proposals are saved to `change_proposals/` and can be submitted as GitHub issues to [UCO](https://github.com/ucoProject/UCO/issues/new) or [CASE](https://github.com/casework/CASE/issues/new).

### Example Agent Outputs

The `examples/agent-outputs/` directory contains four complete worked examples produced by the AI agent using this SDK and MCP server:

| Example | What it demonstrates |
|---------|---------------------|
| `wifi_capture.py` / `.jsonld` | Three-layer network investigation — acquisition (Wireshark capture), observed network (17 TCP flows, DNS chains, IPv6), and analysis layer (5 service attributions with confidence scores) |
| `cellbrite_samsung_extraction.py` / `.jsonld` | Mobile device forensics — Cellebrite extraction with WhatsApp messages, GPS locations, app artifacts, and device metadata |
| `field_office_custody.py` / `.jsonld` | Chain of custody — evidence transfer from a field office with provenance records and handling documentation |
| `usn_journal_example.py` / `.jsonld` | Windows USN Journal — four NTFS change entries (create, modify, rename, delete) with structured reason flags, directory hierarchy, rename before/after modeling, and forensic provenance |

Each example includes both the Python source that builds the graph and the validated JSON-LD output.

The `examples/` directory goes further, with validated end-to-end investigation graphs built from real public-record sources: PACER federal case dockets processed through `process_document_file` (`examples/pacer/` — trafficking, CSAM production, cryptocurrency, and racketeering cases), cyber threat intelligence exemplars (`examples/cti/` — Lotus Blossom / Sagerunex and DarkWatchman), ICAC arrest and CyberTip workflows, and document-processing outputs.

### Cross-ontology profiles (v1.22.0+)

Use the public composition API (`upsert_node` / `add_type` / `link` / `create_relationship`) to enrich a CASE/UCO node with compatible upper-ontology types on the **same IRI**. Validate with named profiles:

```python
from case_uco.validation import validate_graph_file
validate_graph_file("graph.jsonld", profiles=["prov-o", "time"])
# Named extensions require a monorepo/ontology checkout:
# validate_graph_file(
#     "graph.jsonld",
#     extensions=["attack-technique:full"],
#     project_root="/path/to/CASE-UCO-Libraries",
# )
```

Recipes and exemplars live under [`docs/recipes/`](docs/recipes/) (see Cross-Ontology Composition) and [`examples/upper-ontology/`](examples/upper-ontology/). The CI `recipe-validation` job is the **upper-ontology exemplar quality gate** for the nine v1.21 entries in [`docs/recipes/recipe-execution.json`](docs/recipes/recipe-execution.json) (#69); full operational catalog migration is planned for v1.22. Profile discovery: MCP `get_uco_profiles` (includes ORG and PROF).

### Operation PHANTOM GATE — fictitious scenario stress test

**[`examples/scenarios/`](examples/scenarios/)** adds a deliberately **fabricated**, multipart investigation exercise — **Operation PHANTOM GATE** ([`operation-phantom-gate.md`](examples/scenarios/operation-phantom-gate.md), case ID **INV-2026-PGA-001**). This is **Tier T0 synthetic data**: every person, docket number, wallet address, and artifact identifier is invented for SDK and MCP testing. It is **not** a real investigation, not derived from operational case material, and must not be treated as exemplar evidence for production workflows.

The scenario exists to **stress-test** what this SDK can express when modeling work that is **adjacent to, in, and through the cyber domain** — often several such threads at once:

| Track | What it exercises |
|-------|-------------------|
| Elder-fraud couriers (E.D. La.) | Chain of custody, mobile extraction, location corroboration, legal process |
| RICO / crypto social engineering (D.D.C.) | Enterprise modeling, cryptocurrency tracing, FinCEN handling markings |
| Insider / export control (N.D. Cal.) | Email and messaging threads, trade-secret charges, corporate network capture |
| APT / GateRunner CTI | ATT&CK technique extension, malware handling, PCAP flow analysis |
| ICAC / CAC sextortion (D. Alaska) | CAC Ontology grooming workflow, juvenile privacy markings, CyberTip routing |
| Classified disclosure (D. Mass.) | TS//SCI markings, Discord exports, espionage charges |
| Fargo safehouse | Weapons and controlled-substance extensions |

The validated output graph ([`operation-phantom-gate.jsonld`](examples/scenarios/operation-phantom-gate.jsonld), **452 nodes**, nine extension bundles, **`Conforms: True`**) is built by [`build_phantom_gate_scenario.py`](examples/scenarios/build_phantom_gate_scenario.py) with long-tail coverage in [`phantom_gate_longtail.py`](examples/scenarios/phantom_gate_longtail.py) and post-build gates in [`phantom_gate_acceptance.py`](examples/scenarios/phantom_gate_acceptance.py). Fidelity is checked against [`phantom_gate_coverage.json`](examples/scenarios/phantom_gate_coverage.json) via [`check_phantom_gate_coverage.py`](examples/scenarios/check_phantom_gate_coverage.py) (artifact labels, scenario hash, authorization placement); [`build_phantom_gate_typed.py`](examples/scenarios/build_phantom_gate_typed.py) verifies CASEGraph round-trip. See [`examples/scenarios/README.md`](examples/scenarios/README.md) for the agent workflow.

```bash
python3 examples/scenarios/build_phantom_gate_scenario.py
python3 examples/scenarios/check_phantom_gate_coverage.py
python3 examples/scenarios/build_phantom_gate_typed.py
```

Use this scenario to evaluate MCP routing (`route_investigation_content`, `route_cac_content`, `guide_mapping`, `plan_solveit_workflow`), recipe coverage, extension interoperability, and semantic modeling — not as a template for real case data.

For MCP server setup details and troubleshooting, see **[mcp_server/README.md](mcp_server/README.md)**.

## Ecosystem & Tools

The SDK builds graphs. These companion tools and community projects complete the picture. The SDK fits into the [CDO project release flow](https://cyberdomainontology.org/resources/project_release_flow.html) as a downstream consumer of the UCO and CASE ontologies.

### Companion Tools

- **[case-utils](https://github.com/casework/CASE-Utilities-Python)** — CLI tools for SHACL validation (`case_validate`), graph merging, and format conversion. Install via `pip install case-utils`.
- **[case-validation-action](https://github.com/kchason/case-validation-action)** — GitHub Action for CASE validation in CI workflows.
- **[Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/)** — Free SPARQL-capable graph database for querying across multiple graph files.

### Community Mappings and Implementations

The CASE community maintains tool-specific mappings and working implementations. When integrating a specific forensic tool, check these first:

- **[CASE-Mappings](https://github.com/casework/CASE-Mappings)** — Concept and property mappings for SleuthKit, Cellebrite, Bulk Extractor, and NSRL
- **[CASE-Implementation-*](https://github.com/casework?q=Implementation&type=all)** — Working implementations for UFED, ExifTool, AXIOM, XRY, DC3DD, and more
- **[CASE-Mapping-Template-Stubs](https://github.com/casework/CASE-Mapping-Template-Stubs)** — JSON-LD stub generator for bootstrapping new tool mappings

### Community Extensions

Projects that extend CASE/UCO into specialized domains:

- **[CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology)** — 35+ modules for crimes against children investigations. Maintained by Project VIC International. *Bundled with this SDK* (`ontology/cac/`) and fully queryable through the registry and MCP tools.
- **[Adversary Engagement Ontology](https://github.com/UNHSAILLab/Adversary-Engagement-Ontology)** — UCO sub-ontology for cyber deception, honeypots, and adversary engagement operations. *Bundled with this SDK* (`ontology/aeo/`).
- **[SOLVE-IT](https://github.com/SOLVE-IT-DF)** — Knowledge base of digital forensic objectives, techniques, weaknesses, and mitigations, with its own CASE/UCO extension ontology. *Bundled with this SDK* (`ontology/solveit/`) as a pinned, sync-managed snapshot with dedicated MCP query tools (`search_solveit`, `get_solveit_details`, `plan_solveit_workflow`).

See [Bundled Extension Ontologies](#bundled-extension-ontologies) for the full list of extensions shipped with the SDK, including the SDK-native `cryptoinv`, `legalproc`, `rico`, `weapons`, `drugs`, `attack-technique`, and `toolcap` extensions.

### UCO Profiles — Interoperability with Other Ontologies

UCO maintains [Profile repositories](https://cyberdomainontology.org/ontology/development/#profiles) that align UCO classes with other established ontologies. If you're already familiar with BFO, PROV-O, GeoSPARQL, or another ontology, these profiles bridge the gap:

| Profile | External Ontology | Use case |
|---------|------------------|----------|
| [UCO-Profile-BFO](https://github.com/ucoProject/UCO-Profile-BFO) | Basic Formal Ontology | Top-level grounding for formal reasoning |
| [UCO-Profile-gufo](https://github.com/ucoProject/UCO-Profile-gufo) | gUFO (OntoUML) | Used by the [CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology) |
| [UCO-Profile-PROV-O](https://github.com/ucoProject/UCO-Profile-PROV-O) | W3C PROV-O | Provenance tracking and chain of custody |
| [UCO-Profile-Time](https://github.com/ucoProject/UCO-Profile-Time) | W3C OWL-Time | Temporal reasoning and intervals |
| [UCO-Profile-GeoSPARQL](https://github.com/ucoProject/UCO-Profile-GeoSPARQL) | OGC GeoSPARQL | Geospatial queries and spatial reasoning |
| [UCO-Profile-FOAF](https://github.com/ucoProject/UCO-Profile-FOAF) | Friend-of-a-Friend | Social network and identity data |

For detailed usage guidance and SDK integration patterns, see **[docs/ECOSYSTEM.md](docs/ECOSYSTEM.md#uco-profiles--interoperability-with-other-ontologies)**.

### Ontology Sources

- [UCO Ontology](https://github.com/ucoProject/UCO) — Unified Cyber Ontology source
- [CASE Ontology](https://github.com/casework/CASE) — Cyber-investigation Analysis Standard Expression source
- [CASE Examples](https://github.com/casework/CASE-Examples) — Validated CASE/UCO example data
- [CDO Project Release Flow](https://cyberdomainontology.org/resources/project_release_flow.html) — Community release pipeline and adoption status
- [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) — Requirements for community extensions

For detailed descriptions, installation guides, and additional resources, see **[docs/ECOSYSTEM.md](docs/ECOSYSTEM.md)**.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines — organized into three tracks: using the SDK, contributing to it, and extending/regenerating the ontology bindings.

## Security

See [SECURITY.md](SECURITY.md) for our vulnerability reporting and disclosure policy.

## License

Apache-2.0
