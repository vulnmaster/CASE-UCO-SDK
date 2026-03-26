# Round-Trip: Serialize and Deserialize

> See [Recipe Index](INDEX.md) for all recipes.

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
