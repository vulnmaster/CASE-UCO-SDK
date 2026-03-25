# CASE/UCO SDK Recipes

Practical patterns for common digital forensics and cyber-investigation workflows. Each recipe shows how to model real-world data using the SDK across all four supported languages.

For the full class reference, see [ONTOLOGY_REFERENCE.md](../ONTOLOGY_REFERENCE.md). For domain-to-class mapping, see [MAPPING_GUIDE.md](MAPPING_GUIDE.md). For performance guidance, see [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md).

## Contents

- [Modeling a Forensic Tool and Its Output](#modeling-a-forensic-tool-and-its-output)
- [File System Forensics](#file-system-forensics)
- [Network Artifact Extraction](#network-artifact-extraction)
- [Mobile Device Forensics](#mobile-device-forensics)
- [Email and Messaging](#email-and-messaging)
- [Chain of Custody](#chain-of-custody)
- [Discovering Classes at Runtime](#discovering-classes-at-runtime)
- [Working with Extensions](#working-with-extensions)
- [Round-Trip: Serialize and Deserialize](#round-trip-serialize-and-deserialize)
- [Managing Large Datasets](#managing-large-datasets)

---

> **Validate your output.** After any recipe produces a `.jsonld` file, validate it with [case-utils](https://github.com/casework/CASE-Utilities-Python):
>
> ```bash
> pip install case-utils  # one-time install
> case_validate --built-version case-1.4.0 my-output.jsonld
> ```
>
> If you use an extension ontology, include its shapes:
>
> ```bash
> case_validate --built-version case-1.4.0 \
>   --ontology-graph path/to/extension.ttl \
>   --ontology-graph path/to/extension-shapes.ttl \
>   my-output.jsonld
> ```
>
> See [ECOSYSTEM.md](ECOSYSTEM.md) for more companion tools.

---

## Modeling a Forensic Tool and Its Output

Every forensic workflow starts with a tool and the investigation it supports.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.case.investigation import Investigation, InvestigativeAction

graph = CASEGraph()

investigation = graph.create(Investigation,
    name="Case 2024-001",
    description="Unauthorized access investigation",
)

tool = graph.create(Tool,
    name="Autopsy",
    version="4.21.0",
    tool_type="Forensic Analysis",
)

action = graph.create(InvestigativeAction,
    name="Full disk analysis",
    description="Analyzed suspect disk image with Autopsy",
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
using CaseUco;

var graph = new CaseGraph();

graph.Add(new Investigation {
    Name = "Case 2024-001",
    Description = "Unauthorized access investigation"
});

graph.Add(new Tool {
    Name = "Autopsy",
    Version = "4.21.0",
    ToolType = "Forensic Analysis"
});

graph.Add(new InvestigativeAction {
    Name = "Full disk analysis",
    Description = "Analyzed suspect disk image with Autopsy"
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
import org.caseontology.*;

CaseGraph graph = new CaseGraph();

var inv = new Investigation();
inv.setName("Case 2024-001");
inv.setDescription("Unauthorized access investigation");
graph.add(inv);

var tool = new Tool();
tool.setName("Autopsy");
tool.setVersion("4.21.0");
tool.setToolType("Forensic Analysis");
graph.add(tool);

var action = new InvestigativeAction();
action.setName("Full disk analysis");
action.setDescription("Analyzed suspect disk image with Autopsy");
graph.add(action);

System.out.println(graph.serialize());
```

</details>

<details><summary>Rust</summary>

```rust
use case_uco::graph::CaseGraph;
use case_uco::case::investigation::{Investigation, InvestigativeAction};
use case_uco::uco::tool::Tool;

let mut graph = CaseGraph::new("http://example.org/kb/");

let inv = Investigation::builder()
    .name("Case 2024-001".into())
    .description("Unauthorized access investigation".into())
    .build();
graph.create(&inv);

let tool = Tool::builder()
    .name("Autopsy".into())
    .version("4.21.0".into())
    .tool_type("Forensic Analysis".into())
    .build();
graph.create(&tool);

let action = InvestigativeAction::builder()
    .name("Full disk analysis".into())
    .description("Analyzed suspect disk image with Autopsy".into())
    .build();
graph.create(&action);

println!("{}", graph.serialize().unwrap());
```

</details>

## File System Forensics

Model files, directories, and their metadata extracted from a disk image.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import ObservableObject, FileFacet, ContentDataFacet
from datetime import datetime

graph = CASEGraph()

evidence_file = graph.create(ObservableObject,
    has_facet=[
        FileFacet(
            file_name="quarterly_report.xlsx",
            file_path="/Users/suspect/Documents/quarterly_report.xlsx",
            size_in_bytes=245760,
            accessed_time=datetime(2024, 3, 15, 9, 30, 0),
            modified_time=datetime(2024, 3, 14, 16, 45, 0),
            created_time=datetime(2024, 1, 10, 8, 0, 0),
        ),
        ContentDataFacet(
            hash_method="SHA-256",
            hash_value="a7ffc6f8bf1ed76651c14756a061d662...",
            size_in_bytes=245760,
            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
    ],
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

graph.Add(new ObservableObject {
    HasFacet = {
        new FileFacet {
            FileName = "quarterly_report.xlsx",
            FilePath = "/Users/suspect/Documents/quarterly_report.xlsx",
            SizeInBytes = 245760,
            AccessedTime = new DateTime(2024, 3, 15, 9, 30, 0),
            ModifiedTime = new DateTime(2024, 3, 14, 16, 45, 0),
            CreatedTime = new DateTime(2024, 1, 10, 8, 0, 0),
        },
        new ContentDataFacet {
            HashMethod = "SHA-256",
            HashValue = "a7ffc6f8bf1ed76651c14756a061d662...",
            SizeInBytes = 245760,
        }
    }
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var fileFacet = new FileFacet();
fileFacet.setFileName("quarterly_report.xlsx");
fileFacet.setFilePath("/Users/suspect/Documents/quarterly_report.xlsx");
fileFacet.setSizeInBytes(245760L);

var hashFacet = new ContentDataFacet();
hashFacet.setHashMethod("SHA-256");
hashFacet.setHashValue("a7ffc6f8bf1ed76651c14756a061d662...");
hashFacet.setSizeInBytes(245760L);

var obs = new ObservableObject();
obs.getHasFacet().add(fileFacet);
obs.getHasFacet().add(hashFacet);
graph.add(obs);

System.out.println(graph.serialize());
```

</details>

<details><summary>Rust</summary>

```rust
let mut graph = CaseGraph::new("http://example.org/kb/");

let obs = ObservableObject::default();
// Attach FileFacet and ContentDataFacet via the builder pattern
graph.create(&obs);

println!("{}", graph.serialize().unwrap());
```

</details>

## Network Artifact Extraction

Model network connections, DNS lookups, and URLs found in forensic artifacts.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import (
    ObservableObject, URLFacet, DomainNameFacet,
    IPv4AddressFacet, NetworkConnectionFacet,
)
from datetime import datetime

graph = CASEGraph()

url = graph.create(ObservableObject,
    has_facet=[URLFacet(
        full_value="https://exfil-server.example.com/upload?session=abc123",
    )],
)

domain = graph.create(ObservableObject,
    has_facet=[DomainNameFacet(value="exfil-server.example.com")],
)

ip = graph.create(ObservableObject,
    has_facet=[IPv4AddressFacet(value="198.51.100.42")],
)

connection = graph.create(ObservableObject,
    has_facet=[NetworkConnectionFacet(
        dst_port=443, src_port=52341,
        protocols=["TCP", "TLS", "HTTPS"],
        start_time=datetime(2024, 3, 15, 2, 14, 33),
        end_time=datetime(2024, 3, 15, 2, 14, 35),
    )],
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

graph.Add(new ObservableObject {
    HasFacet = { new URLFacet {
        FullValue = "https://exfil-server.example.com/upload?session=abc123"
    }}
});

graph.Add(new ObservableObject {
    HasFacet = { new IPv4AddressFacet { AddressValue = "198.51.100.42" } }
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var urlFacet = new URLFacet();
urlFacet.setFullValue("https://exfil-server.example.com/upload?session=abc123");
var urlObs = new ObservableObject();
urlObs.getHasFacet().add(urlFacet);
graph.add(urlObs);

var ipFacet = new IPv4AddressFacet();
ipFacet.setAddressValue("198.51.100.42");
var ipObs = new ObservableObject();
ipObs.getHasFacet().add(ipFacet);
graph.add(ipObs);

System.out.println(graph.serialize());
```

</details>

## Mobile Device Forensics

Model mobile device artifacts including apps and their data.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import (
    ObservableObject, DeviceFacet, ApplicationFacet,
    OperatingSystemFacet, AccountFacet,
)

graph = CASEGraph()

phone = graph.create(ObservableObject,
    has_facet=[
        DeviceFacet(
            manufacturer="Samsung", model="Galaxy S24",
            serial="RZ8T30EXAMPLE", device_type="Mobile Phone",
        ),
        OperatingSystemFacet(name="Android", version="14"),
    ],
)

messaging_app = graph.create(ObservableObject,
    has_facet=[ApplicationFacet(
        application_identifier="com.example.messenger",
        name="Messenger App", version="5.2.1",
    )],
)

account = graph.create(ObservableObject,
    has_facet=[AccountFacet(
        account_identifier="user@example.com",
        account_type="email", is_active=True,
    )],
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

graph.Add(new ObservableObject {
    HasFacet = {
        new DeviceFacet {
            Manufacturer = "Samsung", Model = "Galaxy S24",
            Serial = "RZ8T30EXAMPLE", DeviceType = "Mobile Phone"
        },
        new OperatingSystemFacet { Name = "Android", Version = "14" }
    }
});

graph.Add(new ObservableObject {
    HasFacet = { new ApplicationFacet {
        ApplicationIdentifier = "com.example.messenger",
        Name = "Messenger App", Version = "5.2.1"
    }}
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var device = new DeviceFacet();
device.setManufacturer("Samsung");
device.setModel("Galaxy S24");
device.setSerial("RZ8T30EXAMPLE");
var phone = new ObservableObject();
phone.getHasFacet().add(device);
graph.add(phone);

var app = new ApplicationFacet();
app.setApplicationIdentifier("com.example.messenger");
app.setName("Messenger App");
var appObs = new ObservableObject();
appObs.getHasFacet().add(app);
graph.add(appObs);

System.out.println(graph.serialize());
```

</details>

## Email and Messaging

Model email messages and their metadata.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import (
    ObservableObject, EmailMessageFacet, EmailAddressFacet,
)
from datetime import datetime

graph = CASEGraph()

sender = graph.create(ObservableObject,
    has_facet=[EmailAddressFacet(
        address_value="suspect@example.com",
        display_name="John Doe",
    )],
)

email = graph.create(ObservableObject,
    has_facet=[EmailMessageFacet(
        subject="Project Files",
        sent_time=datetime(2024, 3, 14, 16, 30, 0),
        is_read=True,
        content_type="text/plain",
        body="See attached files for the project deliverables.",
    )],
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

graph.Add(new ObservableObject {
    HasFacet = { new EmailAddressFacet {
        AddressValue = "suspect@example.com",
        DisplayName = "John Doe"
    }}
});

graph.Add(new ObservableObject {
    HasFacet = { new EmailMessageFacet {
        Subject = "Project Files",
        SentTime = new DateTime(2024, 3, 14, 16, 30, 0),
        IsRead = true,
        ContentType = "text/plain",
        Body = "See attached files for the project deliverables."
    }}
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var emailFacet = new EmailMessageFacet();
emailFacet.setSubject("Project Files");
emailFacet.setIsRead(true);
emailFacet.setBody("See attached files for the project deliverables.");
var emailObs = new ObservableObject();
emailObs.getHasFacet().add(emailFacet);
graph.add(emailObs);

System.out.println(graph.serialize());
```

</details>

## Chain of Custody

Model evidence provenance, including who handled it and when.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.action import Action
from case_uco.uco.identity import Identity
from case_uco.uco.observable import ObservableObject, DeviceFacet
from datetime import datetime

graph = CASEGraph()

examiner = graph.create(Identity, name="Jane Smith, CFCE")

laptop = graph.create(ObservableObject,
    has_facet=[DeviceFacet(
        manufacturer="Dell", model="Latitude 5540", serial="SVC-TAG-12345",
    )],
)

seizure = graph.create(Action,
    id="kb:action-seizure-001",
    name="Evidence seizure",
    description="Laptop seized from suspect's office, Rm 204",
    start_time=datetime(2024, 3, 10, 14, 22, 0),
    end_time=datetime(2024, 3, 10, 14, 35, 0),
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

graph.Add(new Identity { Name = "Jane Smith, CFCE" });

graph.Add(new ObservableObject {
    HasFacet = { new DeviceFacet {
        Manufacturer = "Dell", Model = "Latitude 5540", Serial = "SVC-TAG-12345"
    }}
});

graph.AddWithId(new Action {
    Name = "Evidence seizure",
    Description = "Laptop seized from suspect's office, Rm 204",
    StartTime = new DateTime(2024, 3, 10, 14, 22, 0),
    EndTime = new DateTime(2024, 3, 10, 14, 35, 0)
}, "kb:action-seizure-001");

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var examiner = new Identity();
examiner.setName("Jane Smith, CFCE");
graph.add(examiner);

var device = new DeviceFacet();
device.setManufacturer("Dell");
device.setModel("Latitude 5540");
device.setSerial("SVC-TAG-12345");
var laptop = new ObservableObject();
laptop.getHasFacet().add(device);
graph.add(laptop);

var seizure = new Action();
seizure.setName("Evidence seizure");
seizure.setDescription("Laptop seized from suspect's office, Rm 204");
graph.addWithId(seizure, "kb:action-seizure-001");

System.out.println(graph.serialize());
```

</details>

## Discovering Classes at Runtime

All four languages include a runtime registry for searching and querying the ontology programmatically.

<details open><summary>Python</summary>

```python
from case_uco.registry import search, get_class, find_facets, list_modules

# Search by keyword
results = search("browser")
for r in results:
    print(f"{r['name']:30s} {r['module']}")

# Get full class details including properties
info = get_class("FileFacet")
print(info["description"])
for prop in info["properties"]:
    print(f"  {prop['name']:20s} {prop['type']:15s} required={prop['required']}")

# Find all Facet subclasses
facets = find_facets()
print(f"{len(facets)} facet classes available")

# List modules
for mod in list_modules():
    print(mod)
```

</details>

<details><summary>C#</summary>

```csharp
using CaseUco;

// Search by keyword
var results = OntologyRegistry.Search("browser");
foreach (var r in results)
    Console.WriteLine($"{r["name"],-30} {r["module"]}");

// Get full class details
var info = OntologyRegistry.GetClass("FileFacet");
Console.WriteLine(info["description"]);

// Find all Facet subclasses
var facets = OntologyRegistry.FindFacets();
Console.WriteLine($"{facets.Count} facet classes available");

// List modules
foreach (var mod in OntologyRegistry.ListModules())
    Console.WriteLine(mod);

// Find classes by property type
var withTool = OntologyRegistry.FindByPropertyType("Tool");
```

</details>

<details><summary>Java</summary>

```java
import org.caseontology.OntologyRegistry;

// Search by keyword
var results = OntologyRegistry.search("browser");
for (var r : results)
    System.out.printf("%-30s %s%n", r.get("name"), r.get("module"));

// Get full class details
var info = OntologyRegistry.getClass("FileFacet");
System.out.println(info.get("description"));

// Find all Facet subclasses
var facets = OntologyRegistry.findFacets();
System.out.printf("%d facet classes available%n", facets.size());

// List modules
for (var mod : OntologyRegistry.listModules())
    System.out.println(mod);

// Find classes by property type
var withTool = OntologyRegistry.findByPropertyType("Tool");
```

</details>

<details><summary>Rust</summary>

```rust
use case_uco::registry;

// Search by keyword
let results = registry::search("browser");
for cls in &results {
    println!("{:30} {}", cls.name, cls.module);
}

// Get full class details
if let Some(info) = registry::get_class("FileFacet") {
    println!("{}", info.description);
    for prop in &info.properties {
        println!("  {:20} {:15} required={}", prop.name, prop.type_name, prop.required);
    }
}

// Find all Facet subclasses
let facets = registry::find_facets();
println!("{} facet classes available", facets.len());

// List modules
for mod_name in registry::list_modules() {
    println!("{}", mod_name);
}

// Find classes by property type
let with_tool = registry::find_by_property_type("Tool");
```

</details>

## Working with Extensions

Use extension ontologies (like `toolcap`) to model domain-specific concepts. The scaffold command generates starter classes for all four languages.

```bash
# Generate starter code from your extension's TTL files
case-uco-generate scaffold \
  --extension extensions/toolcap/toolcap.ttl extensions/toolcap/toolcap-shapes.ttl \
  --output-dir my_project/

# Generate for a single language
case-uco-generate scaffold \
  --extension extensions/toolcap/toolcap.ttl extensions/toolcap/toolcap-shapes.ttl \
  --lang python --output-dir my_project/
```

<details open><summary>Python — using scaffolded classes</summary>

```python
from toolcap_classes import ToolCapability, CapabilityMatrix
from case_uco import CASEGraph
from case_uco.uco.tool import Tool

graph = CASEGraph(extra_context={
    "toolcap": "http://example.org/ontology/toolcap/",
})

tool = graph.create(Tool, name="Tool A", version="4.0")

cap = ToolCapability(
    tool=tool,
    supported_platform=["Android", "iOS"],
    parsed_observable_type=["SMS", "Contacts", "Call Logs"],
    tool_version="4.0",
    is_verified=True,
)
graph.add(cap)

print(graph.serialize())
```

</details>

<details><summary>C# — using scaffolded classes</summary>

```csharp
using CaseUco;
using CaseUco.Ext.Toolcap;

var graph = new CaseGraph();
graph.AddContext("toolcap", "http://example.org/ontology/toolcap/");

var toolId = graph.Add(new Tool { Name = "Tool A", Version = "4.0" });

graph.Add(new ToolCapability {
    ToolVersion = "4.0",
    SupportedPlatform = { "Android", "iOS" },
    ParsedObservableType = { "SMS", "Contacts", "Call Logs" },
    IsVerified = true
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java — using scaffolded classes</summary>

```java
import org.caseontology.*;
import org.caseontology.ext.toolcap.*;

CaseGraph graph = new CaseGraph();
graph.addContext("toolcap", "http://example.org/ontology/toolcap/");

var tool = new Tool();
tool.setName("Tool A");
tool.setVersion("4.0");
graph.add(tool);

var cap = new ToolCapability();
cap.setToolVersion("4.0");
cap.getSupportedPlatform().add("Android");
cap.getSupportedPlatform().add("iOS");
cap.getParsedObservableType().add("SMS");
cap.getParsedObservableType().add("Contacts");
graph.add(cap);

System.out.println(graph.serialize());
```

</details>

## Round-Trip: Serialize and Deserialize

The Python SDK supports typed deserialization via `from_jsonld()`. Other languages can load JSON-LD as raw objects via `Load()`.

<details open><summary>Python — typed deserialization</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.tool import Tool

graph = CASEGraph()
graph.create(Tool, name="Tool A", version="4.0")
json_str = graph.serialize()

# Deserialize back to typed objects
graph2, objects = CASEGraph.from_jsonld(json_str)

for obj in objects:
    if isinstance(obj, Tool):
        print(f"Tool: {obj.name} v{obj.version}")
    else:
        print(f"Untyped: {type(obj).__name__}")
```

</details>

<details><summary>C# — document-level loading</summary>

```csharp
var graph = new CaseGraph();
graph.Add(new Tool { Name = "Tool A", Version = "4.0" });
var json = graph.Serialize();

// Load into a new graph (merges context and objects)
var graph2 = new CaseGraph();
graph2.Load(json);
Console.WriteLine($"Loaded {graph2.Count} objects");
```

</details>

<details><summary>Java — document-level loading</summary>

```java
CaseGraph graph = new CaseGraph();
graph.add(new Tool() {{ setName("Tool A"); setVersion("4.0"); }});
String json = graph.serialize();

CaseGraph graph2 = new CaseGraph();
graph2.load(json);
System.out.printf("Loaded %d objects%n", graph2.size());
```

</details>

<details><summary>Rust — document-level loading</summary>

```rust
let mut graph = CaseGraph::new("http://example.org/kb/");
let tool = Tool::builder().name("Tool A".into()).version("4.0".into()).build();
graph.create(&tool);
let json = graph.serialize().unwrap();

let mut graph2 = CaseGraph::new("http://example.org/kb/");
graph2.load(&json).unwrap();
println!("Loaded {} objects", graph2.len());
```

</details>

## Managing Large Datasets

Digital investigation graphs are highly interconnected. An `InvestigativeAction` references a `Tool`, which produced `ObservableObject` instances, which have `Facet` sub-objects. Naively splitting a graph by object count will break these relationships — a referencing object may end up in a different partition than the object it references.

**The recommended approach is to partition at the data source**, building one graph per natural forensic boundary (volume, app, session, device). This ensures all cross-references resolve within the same graph.

### When Is `split()` Safe?

`split()` divides by object index. Use it **only** for catalog-style graphs where objects are independent — file hash inventories, DNS record lists, IoC feeds, or any dataset where objects do not reference each other.

### Recommended: Source-Level Partitioning

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import ObservableObject, FileFacet

# One graph per volume — all objects and their relationships stay together
for volume in disk_image.volumes:
    graph = CASEGraph(kb_prefix=f"http://example.org/kb/case-001/{volume.name}/")

    for file_entry in volume.files:
        graph.create(ObservableObject,
            has_facet=[FileFacet(file_name=file_entry.name, size_in_bytes=file_entry.size)],
        )

    print(f"{volume.name}: {len(graph)} objects, ~{graph.estimate_triples()} triples")
    graph.write(f"volume-{volume.name}.jsonld")

# Merge for combined analysis or load into a graph database
combined = CASEGraph.merge_files([
    f"volume-{v.name}.jsonld" for v in disk_image.volumes
])
```

</details>

<details><summary>C#</summary>

```csharp
foreach (var volume in diskImage.Volumes)
{
    var graph = new CaseGraph($"http://example.org/kb/case-001/{volume.Name}/");

    foreach (var file in volume.Files)
        graph.Add(new ObservableObject {
            HasFacet = { new FileFacet { FileName = file.Name, SizeInBytes = file.Size } }
        });

    Console.WriteLine($"{volume.Name}: {graph.Count} objects, ~{graph.EstimateTriples()} triples");
    graph.Write($"volume-{volume.Name}.jsonld");
}

var paths = diskImage.Volumes.Select(v => $"volume-{v.Name}.jsonld").ToList();
var merged = CaseGraph.MergeFiles(paths);
```

</details>

<details><summary>Java</summary>

```java
for (Volume volume : diskImage.getVolumes()) {
    CaseGraph graph = new CaseGraph("http://example.org/kb/case-001/" + volume.getName() + "/");

    for (FileEntry file : volume.getFiles()) {
        var facet = new FileFacet();
        facet.setFileName(file.getName());
        facet.setSizeInBytes(file.getSize());
        var obs = new ObservableObject();
        obs.getHasFacet().add(facet);
        graph.add(obs);
    }

    System.out.printf("%s: %d objects, ~%d triples%n",
        volume.getName(), graph.size(), graph.estimateTriples());
    graph.write("volume-" + volume.getName() + ".jsonld");
}
```

</details>

<details><summary>Rust</summary>

```rust
for volume in &disk_image.volumes {
    let prefix = format!("http://example.org/kb/case-001/{}/", volume.name);
    let mut graph = CaseGraph::new(&prefix);

    for file in &volume.files {
        graph.create(&ObservableObject::default());
    }

    println!("{}: {} objects, ~{} triples",
        volume.name, graph.len(), graph.estimate_triples());
    graph.write(&format!("volume-{}.jsonld", volume.name)).unwrap();
}
```

</details>

### `split()` for Catalog Data

If your graph contains independent objects with no cross-references (e.g., an IoC feed), `split()` is a convenient way to batch:

```python
# Safe: each hash entry is independent, no cross-references
ioc_graph = CASEGraph()
for hash_value in ioc_hashes:
    ioc_graph.create(ObservableObject,
        has_facet=[ContentDataFacet(hash_value=hash_value)],
    )

chunks = ioc_graph.split(max_objects=10000)
for i, chunk in enumerate(chunks):
    chunk.write(f"ioc_batch_{i:03d}.jsonld")
```

See [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) for hardware sizing, memory benchmarks, and validation scaling guidance.
