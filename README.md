# CASE/UCO SDK

**v1.0.0** · CASE 1.4.0 · UCO 1.4.0 · [Changelog](CHANGELOG.md)

A multi-language data modeling library for digital forensics, cyber-investigation, and cyber-observable data. If your software produces or consumes forensic evidence, this SDK gives you typed, validated builders in **Python**, **C#**, **Java**, and **Rust** — so you can model investigation data in your language and produce interoperable [CASE/UCO](https://caseontology.org/) JSON-LD output.

The SDK also works with AI coding assistants (Cursor, Claude Code, etc.) — see [AI-Assisted Development](#ai-assisted-development) below.

## What the SDK Does

The SDK is auto-generated from the official CASE 1.4.0 and UCO 1.4.0 ontology sources. Every class, property, and vocabulary term in the published specifications has a corresponding typed class in each language. The generated code gives you:

- **Full ontology coverage** — all 428 classes across 15 modules (including extensions)
- **Typed properties** with correct JSON-LD serialization (IRIs, typed literals, nested objects)
- **Required-field validation** — ontology-mandated properties are checked before graph insertion
- **Automatic JSON-LD context** — the standard 18 CASE/UCO namespace prefixes are built in
- **Deterministic ID support** — use auto-generated UUIDs or supply your own stable IRIs
- **Round-trip capable** — load existing JSON-LD graphs, add objects, and re-serialize

## Installation

### Python

```bash
git clone --recurse-submodules https://github.com/vulnmaster/CASE-UCO-SDK.git
cd CASE-UCO-SDK
pip install -e python/
```

### All Languages (via Makefile)

```bash
git clone --recurse-submodules https://github.com/vulnmaster/CASE-UCO-SDK.git
cd CASE-UCO-SDK
make init      # install generator + fetch submodules
make generate  # regenerate all libraries from ontology sources
make build     # build Python, C#, Java, Rust
make test      # run all test suites
```

### Prerequisites

Only install what you need for your language:

| Language | Requirement |
|----------|-------------|
| Python | Python 3.9+ |
| C# | .NET SDK 8.0+ |
| Java | JDK 11+ and Maven |
| Rust | Rust toolchain (cargo) |

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

print(graph.serialize())   # JSON-LD string
graph.write("output.jsonld")
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

Tool tool = new Tool().setName("My Forensic Tool").setVersion("3.0");
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

See the [toolcap extension](extensions/toolcap/) for a complete, validated example of this pattern, and the [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) for submission requirements.

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

### Recipes

Step-by-step patterns for common forensic workflows — disk imaging, file system analysis, network artifacts, chain of custody, mobile forensics, round-trip serialization, and managing large datasets:

- **[docs/recipes/](docs/recipes/INDEX.md)** — practical cookbook with copy-paste examples (one file per recipe)

## SDK Architecture

```
CASE-UCO-SDK/
├── generator/              Code generator + CLI explorer + docs generators
├── ontology/               Git submodules: UCO 1.4.0 + CASE 1.4.0 sources
├── python/                 Generated Python library (case-uco) + runtime registry
├── csharp/                 Generated C# library (CaseUco, netstandard2.0)
├── java/                   Generated Java library (org.caseontology)
├── rust/                   Generated Rust crate (case-uco)
├── extensions/             Extension ontologies (included in explorer + docs)
│   └── toolcap/            Forensic tool capability comparison extension
├── mcp_server/             MCP server for AI-assisted development
│   ├── server.py           FastMCP server wrapping the ontology registry
│   └── domain_index.py     Task-to-class mappings and recipe index
├── .cursor/
│   ├── rules/              AI agent guidance (SDK patterns, extension authoring)
│   └── mcp.json            MCP server configuration
├── docs/
│   ├── ECOSYSTEM.md        Companion tools, community extensions, ontology sources
│   ├── MAPPING_GUIDE.md    Domain mapping guide (auto-generated)
│   ├── PERFORMANCE_GUIDE.md  Engineering tradeoffs and benchmarks
│   └── recipes/            Practical forensic workflow cookbook (one file per recipe)
│       ├── INDEX.md         Recipe catalog and shared guidance
│       ├── chain-of-custody.md
│       ├── forensic-tool.md
│       └── ...              (10 recipe files total)
├── ONTOLOGY_REFERENCE.md   Complete class reference (auto-generated)
├── .github/workflows/      CI, CodeQL, dependency review, release workflows
└── Makefile                Build orchestration
```

## Feature Matrix

| Feature | Python | C# | Java | Rust |
|---------|--------|----|------|------|
| Full typed classes (428 classes) | Yes | Yes | Yes | Yes |
| JSON-LD serialization | Yes | Yes | Yes | Yes |
| Custom / deterministic IDs | `create(id=)` | `AddWithId()` | `addWithId()` | `create_with_id()` |
| Load existing JSON-LD | `load()` / `load_file()` | `Load()` | `load()` / `loadFile()` | `load()` / `load_file()` |
| Required-field validation | Yes | Yes | Yes | — |
| Object count | `len(graph)` | `Count` | `size()` | `len()` |
| Triple estimation | `estimate_triples()` | `EstimateTriples()` | `estimateTriples()` | `estimate_triples()` |
| Graph split (catalog data only) | `split()` | `Split()` | `split()` | `split()` |
| Multi-file merge | `merge_files()` | `MergeFiles()` | `mergeFiles()` | `merge_files()` |
| Typed deserialization | `from_jsonld()` | — | — | — |
| Runtime introspection | `case_uco.registry` | `OntologyRegistry` | `OntologyRegistry` | `registry` module |
| Provenance metadata | `UCO_VERSION` | `CaseUcoMeta` | `CaseUcoMeta` | `VERSION` |

## Ontology Versions

| Component | Version |
|-----------|---------|
| UCO | 1.4.0 |
| CASE | 1.4.0 |

To check at runtime:

```python
import case_uco
print(case_uco.UCO_VERSION)   # "1.4.0"
print(case_uco.CASE_VERSION)  # "1.4.0"
```

## AI-Assisted Development

The SDK is designed to work with AI coding assistants like Cursor, Claude Code, and similar tools. When you open this project in a supported IDE, the AI agent automatically knows how to use the SDK — which classes to pick, how to build graphs, and how to validate output.

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

### MCP Tools Reference

The MCP server exposes six tools and three resources that the AI agent calls behind the scenes:

| Tool | What it does |
|------|-------------|
| `search_classes` | Find classes by keyword match on name or description |
| `get_class_details` | Full property table for a class (types, cardinalities, required flags) |
| `find_classes_for_domain` | Map a natural-language forensic task to the right classes |
| `list_all_facets` | All Facet classes for the ObservableObject + Facet pattern |
| `get_recipe` | Find a code recipe matching a forensic workflow scenario |
| `list_all_vocabs` | All vocabulary/enum types with their valid members |

Resources (read-only context): `case-uco://domains`, `case-uco://modules`, `case-uco://patterns`.

### What You Can Say

Describe what you need in plain language. The agent uses the MCP tools to find the right classes, reads the matching recipe for the correct pattern, writes SDK code, and validates the output — all in one pass.

- "Model the results of a Cellebrite extraction from a Samsung Galaxy with WhatsApp messages and GPS data"
- "Create a chain of custody record for evidence received from a field office"
- "I captured this pcapng with Wireshark on my WiFi interface — model it"
- "Model a mobile device with SIM card, IMEI, and carrier info"
- "Create a forensic analysis result classifying a file as malware with confidence 0.92"

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

### Example Agent Outputs

The `example_agentmcp_outputs/` directory contains three complete worked examples produced by the AI agent using this SDK and MCP server:

| Example | What it demonstrates |
|---------|---------------------|
| `wifi_capture.py` / `.jsonld` | Three-layer network investigation — acquisition (Wireshark capture), observed network (17 TCP flows, DNS chains, IPv6), and analysis layer (5 service attributions with confidence scores) |
| `cellbrite_samsung_extraction.py` / `.jsonld` | Mobile device forensics — Cellebrite extraction with WhatsApp messages, GPS locations, app artifacts, and device metadata |
| `field_office_custody.py` / `.jsonld` | Chain of custody — evidence transfer from a field office with provenance records and handling documentation |

Each example includes both the Python source that builds the graph and the validated JSON-LD output.

For MCP server setup details and troubleshooting, see **[mcp_server/README.md](mcp_server/README.md)**.

## Ecosystem & Tools

The SDK builds graphs. These companion tools and community projects complete the picture.

### Companion Tools

- **[case-utils](https://github.com/casework/CASE-Utilities-Python)** — CLI tools for SHACL validation (`case_validate`), graph merging, and format conversion. Install via `pip install case-utils`.
- **[Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/)** — Free SPARQL-capable graph database for querying across multiple graph files.

### Community Extensions

Projects that extend CASE/UCO into specialized domains:

- **[CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology)** — 35+ modules for crimes against children investigations. Maintained by Project VIC International.
- **[SOLVE-IT](https://github.com/SOLVE-IT-DF)** — Knowledge base and extension framework for digital forensics workflows.
- **[Adversary Engagement Ontology](https://github.com/UNHSAILLab/Adversary-Engagement-Ontology)** — UCO sub-ontology for cyber deception, honeypots, and adversary engagement operations.

### Ontology Sources

- [UCO Ontology](https://github.com/ucoProject/UCO) — Unified Cyber Ontology source
- [CASE Ontology](https://github.com/casework/CASE) — Cyber-investigation Analysis Standard Expression source
- [CASE Examples](https://github.com/casework/CASE-Examples) — Validated CASE/UCO example data
- [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) — Requirements for community extensions

For detailed descriptions, installation guides, and additional resources, see **[docs/ECOSYSTEM.md](docs/ECOSYSTEM.md)**.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

Apache-2.0
