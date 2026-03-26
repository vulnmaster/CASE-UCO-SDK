# File System Forensics

> See [Recipe Index](INDEX.md) for all recipes.

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
