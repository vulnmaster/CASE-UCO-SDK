# Modeling a Forensic Tool and Its Output

> See [Recipe Index](INDEX.md) for all recipes.

Every forensic workflow starts with a tool and the investigation it supports.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.tool import Tool
from case_uco.case.investigation import Investigation, InvestigativeAction

graph = CASEGraph()

investigation = graph.create(Investigation,
    name="Case 2024-001",
    description=["Unauthorized access investigation"],
)

tool = graph.create(Tool,
    name="Autopsy",
    version="4.21.0",
    tool_type="Forensic Analysis",
)

action = graph.create(InvestigativeAction,
    name="Full disk analysis",
    description=["Analyzed suspect disk image with Autopsy"],
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
