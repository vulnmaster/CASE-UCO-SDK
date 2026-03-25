# CASE/UCO SDK

Auto-generated, full-coverage builder libraries for the [CASE](https://caseontology.org/) (Cyber-investigation Analysis Standard Expression) and [UCO](https://unifiedcyberontology.org/) (Unified Cyber Ontology) ontologies.

## Overview

This monorepo contains:

- **generator/** — A Python-based code generator that parses the UCO/CASE OWL+SHACL ontology (Turtle files) and produces idiomatic builder libraries
- **python/** — Generated Python library (`case-uco`)
- **csharp/** — Generated C# library (`CaseUco`, targeting `netstandard2.0`)
- **java/** — Generated Java library (`case-uco`)
- **rust/** — Generated Rust crate (`case-uco`)
- **ontology/** — Git submodules for the [UCO](https://github.com/ucoProject/UCO) and [CASE](https://github.com/casework/CASE) ontology sources
- **extensions/toolcap/** — A CASE/UCO extension for modeling forensic tool capabilities, compliant with the [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) (see [extensions/toolcap/README.md](extensions/toolcap/README.md))

## Quick Start

### Prerequisites

- Python 3.9+ (for the code generator and Python library)
- .NET SDK 8.0+ (for C# library)
- JDK 11+ and Maven (for Java library)
- Rust toolchain (for Rust library)

### Clone and Generate

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/vulnmaster/CASE-UCO-SDK.git
cd CASE-UCO-SDK

# Install the generator
pip install -e generator/

# Generate all libraries (Python, C#, Java, Rust)
python -m case_uco_generator generate --lang all

# Install the Python library (required before importing)
pip install -e python/
```

Or use the Makefile which handles everything:

```bash
make init      # submodules + generator install
make generate  # generate all libraries
make build     # build all languages
make test      # run all tests (including generator tests)
```

## Usage Examples

### Python

```python
from case_uco import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.uco.observable import ObservableObject, ApplicationFacet

graph = CASEGraph(kb_prefix="http://example.org/kb/")

tool_a = graph.create(Tool, name="Tool A", version="7.0")
app_alpha = graph.create(
    ObservableObject,
    has_facet=[ApplicationFacet(application_identifier="com.example.app.alpha")],
)

print(graph.serialize())
```

### C\#

```csharp
using CaseUco;
using CaseUco.Uco.Tool;
using CaseUco.Uco.Observable;

var graph = new CaseGraph("http://example.org/kb/");

var tool = new Tool { Name = "Tool A", Version = "7.0" };
graph.Add(tool);

var app = new ObservableObject();
app.HasFacet = new List<object> {
    new ApplicationFacet { ApplicationIdentifier = "com.example.app.alpha" }
};
graph.Add(app);

graph.Write("output.jsonld");
```

### Java

```java
import org.caseontology.CaseGraph;
import org.caseontology.uco.tool.Tool;
import org.caseontology.uco.observable.ObservableObject;
import org.caseontology.uco.observable.ApplicationFacet;

CaseGraph graph = new CaseGraph("http://example.org/kb/");

Tool tool = new Tool();
tool.setName("Tool A");
tool.setVersion("7.0");
graph.add(tool);

ApplicationFacet facet = new ApplicationFacet();
facet.setApplicationIdentifier("com.example.app.alpha");

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
    .version("7.0".to_string())
    .tool_type("forensic".to_string())
    .build();
let id = graph.create(&tool);

let json = graph.serialize().expect("serialization failed");
println!("{json}");
```

## Forensic Tool Capability Comparison

This project was created to help model which digital forensic tools can parse which applications, on which platforms, and for which observable types. The **[toolcap extension](extensions/toolcap/)** is a CDO Community Playground-compliant extension that includes separated OWL/SHACL files and a validated exemplar (passes `case_validate` with `Conforms: True`):

```bash
python extensions/toolcap/example_capability_matrix.py
```

This produces a CASE/UCO-compliant JSON-LD graph representing:

| | App Alpha | App Beta | App Gamma |
|---|---|---|---|
| **Tool A** | Android, iOS | Android, iOS | Android, iOS, Windows |
| **Tool B** | Android | Android, iOS | — |

## Ontology Versions

| Component | Version |
|-----------|---------|
| UCO | 1.4.0 |
| CASE | 1.4.0 |

## Related Projects

- [UCO Ontology](https://github.com/ucoProject/UCO)
- [CASE Ontology](https://github.com/casework/CASE)
- [CASE Examples](https://github.com/casework/CASE-Examples)
- [CASE Profile Example](https://github.com/casework/CASE-Profile-Example)
- [CASE Mapping Template Stubs](https://github.com/casework/CASE-Mapping-Template-Stubs)
- [CASE Mappings](https://github.com/casework/CASE-Mappings)
- [CDO Community Playground Guide - Draft](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

Apache-2.0
