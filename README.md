# CASE/UCO SDK

A multi-language SDK for building [CASE](https://caseontology.org/) and [UCO](https://unifiedcyberontology.org/) compliant JSON-LD graphs. If your software produces or consumes digital forensic, cyber-investigation, or cyber-observable data, this SDK gives you typed, validated builders in **Python**, **C#**, **Java**, and **Rust** — so you can work with CASE/UCO objects in your language instead of hand-writing JSON-LD.

## What the SDK Does

The SDK is auto-generated from the official CASE 1.4.0 and UCO 1.4.0 OWL+SHACL ontology sources. Every class, property, and vocabulary term in the published specifications has a corresponding typed class in each language. The generated code gives you:

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

CASE/UCO knowledge graphs can grow large quickly — a single DNS record produces 21 triples, and a full filesystem extraction can generate millions. The SDK provides tools to help you partition, estimate, and manage graph sizes for any compute environment.

### Estimate Before Building

```python
graph = CASEGraph()
# ... add objects ...
print(f"~{graph.estimate_triples()} triples")  # estimate before serializing
```

### Partition Large Graphs

Don't build one massive graph. Split into manageable chunks and load them into a graph database for combined analysis:

```python
graph = CASEGraph()
# ... add many objects ...

# Split into chunks of 10,000 objects each
chunks = graph.split(max_objects=10000)
for i, chunk in enumerate(chunks):
    chunk.write(f"batch-{i:04d}.jsonld")
```

### Merge Multiple Graphs

```python
combined = CASEGraph.merge_files([
    "batch-0000.jsonld",
    "batch-0001.jsonld",
    "batch-0002.jsonld",
])
```

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

### Step 2: Define a Matching Dataclass

In your application code, create a dataclass that mirrors the generated SDK pattern:

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MyCustomObject:
    CLASS_IRI: str = "http://example.org/ontology/myext/MyCustomObject"
    NAMESPACE_PREFIX: str = "myext"

    custom_property: Optional[str] = field(default=None, metadata={
        'jsonld_key': 'myext:customProperty',
        'required': False,
        'cardinality': 'zero_or_one',
        'range_iri': 'http://www.w3.org/2001/XMLSchema#string',
        'alternate_range_iris': [],
    })
```

### Step 3: Use It with the SDK

Register your extension's namespace prefix and use the class like any built-in type:

```python
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

### Python Runtime Introspection

Discover classes programmatically from a Python REPL or script:

```python
from case_uco.registry import search, get_class, find_facets, list_modules

# Search by keyword
results = search("browser")
for r in results:
    print(f"{r['name']:30s} {r['module']}")

# Get full class details
info = get_class("FileFacet")
print(info["description"])
for prop in info["properties"]:
    print(f"  {prop['name']:20s} {prop['type']:15s} required={prop['required']}")

# Find all Facet subclasses
facets = find_facets()

# List modules
modules = list_modules()
```

### Ontology Reference

A complete auto-generated reference of every class, property, and vocabulary type:

- **[ONTOLOGY_REFERENCE.md](ONTOLOGY_REFERENCE.md)** — full class reference with property tables, organized by module

### Domain Mapping Guide

Don't know which CASE/UCO class fits your data? The mapping guide organizes classes by forensic domain:

- **[docs/MAPPING_GUIDE.md](docs/MAPPING_GUIDE.md)** — maps common concepts (files, network, devices, email, mobile, etc.) to the right classes, with usage examples

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
├── docs/
│   └── MAPPING_GUIDE.md    Domain mapping guide (auto-generated)
├── ONTOLOGY_REFERENCE.md   Complete class reference (auto-generated)
├── .github/workflows/      CI, CodeQL, dependency review, release workflows
└── Makefile                Build orchestration
```

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

## Related Projects

- [UCO Ontology](https://github.com/ucoProject/UCO) — Unified Cyber Ontology source
- [CASE Ontology](https://github.com/casework/CASE) — Cyber-investigation Analysis Standard Expression source
- [CASE Examples](https://github.com/casework/CASE-Examples) — Validated CASE/UCO example data
- [CASE Profile Example](https://github.com/casework/CASE-Profile-Example) — Extension testing infrastructure
- [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) — Requirements for community extensions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

Apache-2.0
