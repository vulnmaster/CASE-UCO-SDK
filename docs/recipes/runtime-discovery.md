# Discovering Classes at Runtime

> See [Recipe Index](INDEX.md) for all recipes.

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
