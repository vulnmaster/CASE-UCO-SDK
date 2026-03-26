# Working with Extensions

> See [Recipe Index](INDEX.md) for all recipes.

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
