# Cross-Language Parity Contract

This document defines what is intentionally identical across all four SDK languages (Python, C#, Java, Rust) and what is intentionally language-idiomatic. It serves as a reference for contributors, AI coding assistants, and developers switching between languages.

## Canonical Mental Model

Every language follows the same three-step workflow:

1. **Create a graph** — a container for CASE/UCO objects with a JSON-LD context
2. **Add typed objects** — instantiate ontology classes and insert them into the graph
3. **Serialize** — write the graph as JSON-LD

## Identical Across All Languages

### Core Operations

These operations exist in every language with parallel naming (adjusted only for language casing conventions):

| Operation | Python | C# | Java | Rust |
|-----------|--------|----|------|------|
| Create graph | `CASEGraph()` | `new CaseGraph()` | `new CaseGraph()` | `CaseGraph::new()` |
| Add object | `graph.create(Type, ...)` | `graph.Add(obj)` | `graph.add(obj)` | `graph.create(&obj)` |
| Add with ID | `graph.create(Type, id=...)` | `graph.AddWithId(obj, id)` | `graph.addWithId(obj, id)` | `graph.create_with_id(id, &obj)` |
| Serialize | `graph.serialize()` | `graph.Serialize()` | `graph.serialize()` | `graph.serialize()` |
| Write to file | `graph.write(path)` | `graph.Write(path)` | `graph.write(path)` | `graph.write(path)` |
| Load from string | `graph.load(json)` | `graph.Load(json)` | `graph.load(json)` | `graph.load(json)` |
| Load from file | `graph.load_file(path)` | `graph.LoadFile(path)` | `graph.loadFile(path)` | `graph.load_file(path)` |
| Object count | `len(graph)` | `graph.Count` | `graph.size()` | `graph.len()` |
| Estimate triples | `graph.estimate_triples()` | `graph.EstimateTriples()` | `graph.estimateTriples()` | `graph.estimate_triples()` |
| Split graph | `graph.split(n)` | `graph.Split(n)` | `graph.split(n)` | `graph.split(n)` |
| Merge files | `CASEGraph.merge_files(paths)` | `CaseGraph.MergeFiles(paths)` | `CaseGraph.mergeFiles(paths)` | `CaseGraph::merge_files(paths)` |
| Get node by @id | `graph.get(id)` | `graph.Get(id)` | `graph.get(id)` | `graph.get(id)` |
| Contains node | `graph.contains(id)` | `graph.Contains(id)` | `graph.contains(id)` | `graph.contains(id)` |
| Expand IRI | `graph.expand_iri(id)` | `graph.ExpandIri(id)` | `graph.expandIri(id)` | `graph.expand_iri(id)` |
| Upsert node | `graph.upsert_node(id, ...)` | `graph.UpsertNode(id, ...)` | `graph.upsertNode(id, ...)` | `graph.upsert_node(id, ...)` |
| Add type | `graph.add_type(id, type)` | `graph.AddType(id, type)` | `graph.addType(id, type)` | `graph.add_type(id, type)` |
| Add property | `graph.add_property(id, k, v)` | `graph.AddProperty(id, k, v)` | `graph.addProperty(id, k, v)` | `graph.add_property(id, k, v)` |
| Link (property edge) | `graph.link(src, pred, tgt)` | `graph.Link(src, pred, tgt)` | `graph.link(src, pred, tgt)` | `graph.link(src, pred, tgt)` |
| Create Relationship | `graph.create_relationship(...)` | `graph.CreateRelationship(...)` | `graph.createRelationship(...)` | `graph.create_relationship(...)` |
| Reject duplicates on load (**default**) | `on_duplicate="reject"` (default) | `RejectDuplicates = true` (default) | `rejectDuplicates = true` (default) | `reject_duplicates = true` (default) |
| Merge on load (opt-in) | `on_duplicate="merge_compatible"` | `RejectDuplicates = false` | `setRejectDuplicates(false)` | `set_reject_duplicates(false)` |
| Duplicate node error | `DuplicateNodeError` | `InvalidOperationException` | `IllegalStateException` | `DuplicateNodeError` / `GraphError` / `LoadError` |
| Validate | `graph.validate()` | `graph.ValidateGraph()` | `graph.validate()` | `graph.validate()` |
| File + hashes | `file_with_content_hashes(graph, …)` | `CompositionHelpers.FileWithContentHashes(graph, …)` | `CompositionHelpers.fileWithContentHashes(graph, …)` | `helpers::file_with_content_hashes(&mut graph, …)` |
| CSAM / PhotoDNA evidence | `model_csam_evidence(graph, …)` | `CompositionHelpers.ModelCsamEvidence(graph, …)` | `CompositionHelpers.modelCsamEvidence(graph, …)` | `helpers::model_csam_evidence(&mut graph, …)` |
| Tool run | `model_tool_run(graph, …)` | `CompositionHelpers.ModelToolRun(graph, …)` | `CompositionHelpers.modelToolRun(graph, …)` | `helpers::model_tool_run(&mut graph, …)` |
| Investigation builder | `InvestigationBuilder(scenario, profile_id=…)` | `new InvestigationBuilder(scenario, profileId)` | `new InvestigationBuilder(scenario, profileId)` | `InvestigationBuilder::new(scenario, Some(id))` |
| Add CSAM on builder | `builder.add_csam_evidence(…)` | `builder.AddCsamEvidence(…)` | `builder.addCsamEvidence(…)` | `builder.add_csam_evidence(…)` |
| Build / critique | `builder.build()` / `builder.critique()` | `builder.Build()` / `builder.Critique()` | `builder.build()` / `builder.critique()` | `builder.build()` / `builder.critique()` |
| Hash index | `graph.index_content_hashes()` | `graph.IndexContentHashes()` | `graph.indexContentHashes()` | `graph.index_content_hashes()` |
| Lookup hash | `graph.lookup_hash(digest)` | `graph.LookupHash(digest)` | `graph.lookupHash(digest)` | `graph.lookup_hash(digest)` |
| Partition by profile | `graph.partition_by_profile(id)` | `graph.PartitionByProfile(id)` | `graph.partitionByProfile(id)` | `graph.partition_by_profile(id)` |
| Profile ids | `get_profile("HashIntelligence")` | `CompositionProfiles.HashIntelligence` | `CompositionProfiles.HASH_INTELLIGENCE` | `"HashIntelligence"` |
| Load profile contract | `load_contract(id)` | `ProfileContract.Load(id)` | `ProfileContract.load(id)` | `contracts::load_contract(id)` |
| Profile critic | `ProfileCritic` | `ProfileCritic` | `ProfileCritic` | (builder critique + contract) |
| Workflow | `InvestigationWorkflow` | `InvestigationWorkflow` | `InvestigationWorkflow` | `InvestigationWorkflow` |
| Workflow step / save | `step()` / `save()` | `Step()` / `Save()` | `step()` / `save()` | `step()` / `save()` |
| Workflow resume | `resume(dir)` | `Resume(dir)` | `resume(dir)` | `resume(dir)` |
| Workflow handler hook | (Python built-ins) | `RegisterHandler` | `registerHandler` | `register_handler` |

### Registry / Discovery

| Operation | Python | C# | Java | Rust |
|-----------|--------|----|------|------|
| Search classes | `search(query)` | `OntologyRegistry.Search(query)` | `OntologyRegistry.search(query)` | `registry::search(query)` |
| Get class details | `get_class(name)` | `OntologyRegistry.GetClass(name)` | `OntologyRegistry.getClass(name)` | `registry::get_class(name)` |
| List modules | `list_modules()` | `OntologyRegistry.ListModules()` | `OntologyRegistry.listModules()` | `registry::list_modules()` |
| List classes | `list_classes()` | `OntologyRegistry.ListClasses()` | `OntologyRegistry.listClasses()` | `registry::list_classes()` |
| Find facets | `find_facets()` | `OntologyRegistry.FindFacets()` | `OntologyRegistry.findFacets()` | `registry::find_facets()` |
| Find by property type | `find_by_property_type(t)` | `OntologyRegistry.FindByPropertyType(t)` | `OntologyRegistry.findByPropertyType(t)` | `registry::find_by_property_type(t)` |
| List vocabs | `list_vocabs()` | `OntologyRegistry.ListVocabs()` | `OntologyRegistry.listVocabs()` | `registry::list_vocabs()` |

### Provenance Metadata

Every language exposes the ontology versions used to generate the SDK:

| Metadata | Python | C# | Java | Rust |
|----------|--------|----|------|------|
| UCO version | `case_uco.UCO_VERSION` | `CaseUcoMeta.UcoVersion` | `CaseUcoMeta.UCO_VERSION` | `case_uco::UCO_VERSION` |
| CASE version | `case_uco.CASE_VERSION` | `CaseUcoMeta.CaseVersion` | `CaseUcoMeta.CASE_VERSION` | `case_uco::CASE_VERSION` |

### JSON-LD Output

All four languages produce **RDF-equivalent / deterministic** JSON-LD for the
same logical input where the feature is implemented. Parity is **not**
byte-identical serialization across languages (key order, whitespace, and
UUID `@id` minting may differ). Shared contracts include:

- The same namespace prefixes in the `@context` (pruned to used prefixes)
- The same `@type` IRIs
- The same property names (JSON-LD key names are ontology IRIs, not language-native names)
- The same `@id` format pattern (`kb:TypeName-UUID`) when IDs are auto-minted
- Default duplicate `@id` policy of **reject** on load / typed deserialize

### Validation Behavior

- **Required-field validation** is enforced at graph insertion time in all four languages. If an ontology-mandated property is missing, the `create()`/`add()` call raises an error.
- Fields are optional at construction time; validation is deferred to graph insertion.

## Intentionally Language-Idiomatic

These differences follow each language's conventions and are not bugs:

### Object Construction

| Language | Pattern | Rationale |
|----------|---------|-----------|
| Python | `graph.create(Tool, name="My Tool")` | Keyword arguments; class passed as first arg |
| C# | `var t = new Tool { Name = "..." }; graph.Add(t);` | Object initializer syntax; PascalCase properties |
| Java | `var t = new Tool(); t.setName("..."); graph.add(t);` | JavaBean setter pattern; camelCase methods |
| Rust | `let t = Tool::builder().build(); graph.create(&t);` | Builder pattern; snake_case; borrow semantics |

### Naming Conventions

| Convention | Python | C# | Java | Rust |
|------------|--------|----|------|------|
| Methods | `snake_case` | `PascalCase` | `camelCase` | `snake_case` |
| Properties | `snake_case` | `PascalCase` | `camelCase` (getters/setters) | `snake_case` |
| Types/Classes | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` |
| Modules/Namespaces | `snake_case` | `PascalCase` | `lowercase.dot.separated` | `snake_case` |

### Features with Asymmetric Support

| Feature | Python | C# | Java | Rust | Notes |
|---------|--------|----|------|------|-------|
| Typed deserialization | `from_jsonld()` | `FromJsonLd()` | `fromJsonLd()` | `from_jsonld()` | Python returns typed objects; C#/Java use reflection; Rust returns serde_json::Value |
| Property metadata cache (#70) | dataclass field cache | Type→property attr map | Class→field map | N/A | Cleared via `clear_*_class_registry_cache` |
| Streaming write metrics (#71) | `dict` return | `StreamingWriteResult` | `StreamingWriteResult` | `StreamingWriteMetrics` | Atomic temp+rename default |
| Root partition incoming closure (#72) | `include_incoming=True` | `includeIncoming=true` | `includeIncoming=true` | outgoing-only today | Python also supports `return_manifest` |
| Graph validation wrapper | `graph.validate()` | `graph.ValidateGraph()` | `graph.validate()` | `graph.validate()` | Wraps case_validate; requires case-utils on PATH |
| Smoke test binary | — | `CaseUco.Smoke` | `SmokeTest` | `examples/smoke` | Python uses pytest instead |
| Catalog bench harness (#73) | `run_python_bench.py` | `run_csharp_bench.sh` | `run_java_bench.sh` | `run_rust_bench.sh` | Python has full workload suite + baseline compare |
| Helper construction | kwargs | object initializers | JavaBean setters | builders + `add_property` for inherited `hasFacet`/`name` | Rust generated types do not inherit `UcoObject.has_facet`; helpers attach Facets via `uco-core:hasFacet` |

**#72 note:** Python, C#, and Java `partition_by_roots` / `PartitionByRoots` /
`partitionByRoots` follow **outgoing and incoming** nested `@id` references when
`include_incoming` is enabled (default). Rust currently implements outgoing
closure only; incoming reverse-ref parity is **2.1** (authoring host has no
MSVC linker).

**v2 workflow note:** Python ships the full sequential engine. C#/Java/Rust
ship the logical surface (load/save state, step cursor, `Resume`, handler
extension point). Full `hash_media` / adapter / partition *handlers* are **2.1**.
Do not advertise `CRIT-H-*` ID stability outside Python.

### Why `create()` vs `Add()`

Python's `graph.create(Tool, ...)` both constructs and inserts in one call. C# and Java separate construction from insertion because their object initializer / setter patterns make single-call construction less natural. Rust uses `graph.create(&tool)` with a borrow because Rust's ownership model requires the caller to own the object.

The operation count differs (1 call in Python, 2+ in C#/Java, 2 in Rust), but the mental model is the same: build an object, put it in the graph.

## Stability Guarantees

- **Stable**: All operations listed in "Identical Across All Languages" above. These will not be renamed or removed without a major version bump.
- **Stable**: JSON-LD output format. The `@context`, `@type`, and property key names are defined by the ontology and will not change within an ontology version.
- **Unstable**: Internal module structure (e.g., which generated file a class lives in). Import paths may change between releases.
- **Unstable**: Features listed as asymmetric above may be added to additional languages in future releases.

## Migration Notes

When upgrading between SDK versions:
- Check the [CHANGELOG.md](../CHANGELOG.md) for breaking changes
- Regenerated code may move classes between internal modules — update import paths accordingly
- New required properties added by ontology updates will cause validation errors on existing code
