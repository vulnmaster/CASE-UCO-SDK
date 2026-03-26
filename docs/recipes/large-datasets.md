# Managing Large Datasets

> See [Recipe Index](INDEX.md) for all recipes.

Digital investigation graphs are highly interconnected. An `InvestigativeAction` references a `Tool`, which produced `ObservableObject` instances, which have `Facet` sub-objects. Naively splitting a graph by object count will break these relationships — a referencing object may end up in a different partition than the object it references.

**The recommended approach is to partition at the data source**, building one graph per natural forensic boundary (volume, app, session, device). This ensures all cross-references resolve within the same graph.

## When Is `split()` Safe?

`split()` divides by object index. Use it **only** for catalog-style graphs where objects are independent — file hash inventories, DNS record lists, IoC feeds, or any dataset where objects do not reference each other.

## Recommended: Source-Level Partitioning

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

## `split()` for Catalog Data

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

See [PERFORMANCE_GUIDE.md](../PERFORMANCE_GUIDE.md) for hardware sizing, memory benchmarks, and validation scaling guidance.
