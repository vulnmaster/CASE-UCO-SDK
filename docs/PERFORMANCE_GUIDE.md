# CASE/UCO Performance and Engineering Tradeoffs

This guide helps developers make informed engineering decisions when building CASE/UCO knowledge graphs. The data comes from the [pDNS Benchmarking Experiment](https://github.com/vulnmaster/pDNS-Benchmarking-Experiment), which measured serialization and validation performance across dataset sizes from 1,000 to 512,000 records (21,000 to 10.7 million RDF triples).

The core lesson: **build many smaller, focused knowledge graphs instead of one giant monolith.** This works better in resource-constrained environments, parallelizes naturally, and you can still query them together in a graph database.

## Triple Count Estimation

Every CASE/UCO object produces multiple RDF triples. Understanding how many triples your data will generate is critical for capacity planning.

### Triples Per Object Type

| Object Pattern | Triples | Example |
|---------------|---------|---------|
| Simple object (type + 2 properties) | ~3-5 | A `Tool` with name and version |
| Observable + 1 Facet | ~8-12 | `ObservableObject` with `FileFacet` |
| Observable + 2 Facets | ~14-20 | `ObservableObject` with `FileFacet` + `ContentDataFacet` |
| DNS record (object + 2 facets + relationship) | ~21 | Domain + IP + resolution relationship |
| Full file entry (object + 3-4 facets) | ~25-35 | File with name, hash, permissions, timestamps |
| Email message (object + facets + relationships) | ~40-60 | Email with headers, body, attachments, sender/recipient |

### Rule of Thumb

For forensic data, plan for **15-25 triples per evidence item** as a baseline. Complex items (emails, network sessions with multiple facets) can reach 40-60 triples each.

**Use the SDK to estimate before serializing:**

```python
from case_uco.graph import CASEGraph

graph = CASEGraph()
# ... add your objects ...
estimated = graph.estimate_triples()
print(f"This graph will produce ~{estimated} triples")
```

## Memory and Performance Benchmarks

The following data was measured on commodity hardware (64GB RAM) using passive DNS records serialized as CASE/UCO graphs. Each DNS record produces exactly 21 triples.

### Serialization Performance

| Records | Triples | Serialization Time | TTL File Size | JSON-LD File Size |
|---------|---------|-------------------|---------------|-------------------|
| 1,000 | 21,000 | 0.5s | 1.1 MB | 2.9 MB |
| 2,000 | 42,000 | 1.0s | 2.2 MB | 5.8 MB |
| 4,000 | 84,000 | 2.0s | 4.5 MB | 11.7 MB |
| 8,000 | 168,000 | 4.2s | 9.0 MB | 23.5 MB |
| 16,000 | 336,000 | 8.0s | 18.1 MB | 47.1 MB |
| 32,000 | 672,000 | 16.5s | 36.3 MB | 94.3 MB |
| 64,000 | 1,344,000 | 33.1s | 72.8 MB | 188.8 MB |
| 128,000 | 2,688,000 | 64.8s | 145.6 MB | 377.5 MB |
| 256,000 | 5,376,000 | 136.1s | 291.1 MB | 755.0 MB |
| 512,000 | 10,752,000 | 276.0s | 582.3 MB | 1,510.0 MB |

### Validation Performance (PyShacl vs RDFox)

| Records | Triples | PyShacl (TTL) | PyShacl (JSON-LD) | RDFox (TTL) | PyShacl Memory | RDFox Memory |
|---------|---------|--------------|-------------------|-------------|----------------|--------------|
| 1,000 | 21,000 | 1.3s | 1.1s | 0.6s | 75 MB | 57 MB |
| 8,000 | 168,000 | 9.4s | 7.4s | 3.1s | 356 MB | 212 MB |
| 32,000 | 672,000 | 35.8s | 28.1s | 11.6s | 1,330 MB | 744 MB |
| 64,000 | 1,344,000 | 71.9s | 54.4s | 22.4s | 2,630 MB | 1,439 MB |
| 128,000 | 2,688,000 | 141.1s | 112.9s | 44.5s | 5,189 MB | 2,809 MB |
| 256,000 | 5,376,000 | 277.2s | 224.2s | 89.2s | 10,348 MB | 5,504 MB |
| 512,000 | 10,752,000 | 561.1s | 451.7s | 178.4s | 20,642 MB | 10,938 MB |

### Key Findings

- **RDFox is 3.4x faster** than PyShacl on average for SHACL validation
- **RDFox uses 46% less memory** than PyShacl
- **JSON-LD files are 2.6x larger** than TTL but validate ~20% faster in PyShacl
- **Memory per record:** ~50 KB (PyShacl) vs ~27 KB (RDFox)
- Both tools achieve 100% validation accuracy across all dataset sizes

## The "Many Small Graphs" Pattern

The single most important engineering decision is how to partition your data into graphs. Building one massive graph for an entire disk image or case will exhaust memory on most workstations. Instead, build focused graphs and load them into a graph database for combined analysis.

### Recommended Partitioning Strategies

| Forensic Scenario | Partition By | Typical Graph Size | Rationale |
|-------------------|-------------|-------------------|-----------|
| Full disk forensics | Directory or volume | 5K-50K objects per graph | Manageable chunks, natural hierarchy |
| Network forensics | Time window or session | 1K-10K objects per graph | Temporal partitioning, streamable |
| Mobile forensics | App or data type | 500-5K objects per graph | Natural app boundaries |
| Email forensics | Mailbox or date range | 1K-10K objects per graph | User-centric, chronological |
| Multi-device case | Device | Variable per device | Evidence provenance boundaries |
| Large-scale triage | Batch of N items | 10K-50K objects per graph | Predictable resource usage |

### Implementation with the SDK

```python
from case_uco.graph import CASEGraph

# Strategy 1: Partition by batch size
BATCH_SIZE = 10000

graph = CASEGraph(kb_prefix="http://example.org/kb/case-001/")
count = 0

for item in evidence_items:
    graph.create(ObservableObject, has_facet=[...])
    count += 1

    if count >= BATCH_SIZE:
        graph.write(f"batch-{count // BATCH_SIZE:04d}.jsonld")
        graph = CASEGraph(kb_prefix="http://example.org/kb/case-001/")
        count = 0

# Write remaining items
if len(graph) > 0:
    graph.write(f"batch-{count // BATCH_SIZE + 1:04d}.jsonld")
```

```python
# Strategy 2: Use the SDK's built-in split helper
graph = CASEGraph()
# ... add many objects ...

chunks = graph.split(max_objects=10000)
for i, chunk in enumerate(chunks):
    chunk.write(f"chunk-{i:04d}.jsonld")
```

```python
# Strategy 3: Merge multiple graph files for analysis
combined = CASEGraph()
combined.merge_files([
    "batch-0001.jsonld",
    "batch-0002.jsonld",
    "batch-0003.jsonld",
])
# Now analyze the combined graph in memory
print(f"Combined: {len(combined)} objects")
```

## Graph Database Integration

For querying across multiple graphs, load them into a graph database rather than merging in memory.

### Apache Jena Fuseki (Open Source)

```bash
# Load multiple graph files into Fuseki
for f in batch-*.jsonld; do
    s-put http://localhost:3030/case/data "http://example.org/graph/$f" "$f"
done

# Query across all graphs
s-query --service http://localhost:3030/case/query \
  'SELECT ?tool ?app WHERE {
     ?cap a <http://example.org/ontology/toolcap/ToolCapability> .
     ?cap <http://example.org/ontology/toolcap/tool> ?tool .
     ?cap <http://example.org/ontology/toolcap/targetApplication> ?app .
   }'
```

### Blazegraph (Open Source)

```bash
# Load via REST API
curl -X POST http://localhost:9999/blazegraph/sparql \
  --data-urlencode "update=LOAD <file:///data/batch-0001.jsonld>"
```

### Neo4j with Neosemantics (n10s)

```cypher
// Install neosemantics plugin, then:
CALL n10s.rdf.import.fetch("file:///data/batch-0001.jsonld", "JSON-LD")
```

## Hardware Sizing Guide

| Environment | RAM | Recommended Max | Best For |
|-------------|-----|----------------|----------|
| Laptop (16 GB) | 16 GB | ~32K objects (~672K triples) | Field triage, small cases |
| Workstation (32 GB) | 32 GB | ~64K objects (~1.3M triples) | Medium cases, single devices |
| Workstation (64 GB) | 64 GB | ~256K objects (~5.4M triples) | Large cases with RDFox |
| Server (128+ GB) | 128+ GB | ~512K+ objects (~10M+ triples) | Enterprise, multi-device cases |
| Graph Database | Any | Unlimited (disk-backed) | Combined analysis of partitioned graphs |

### Validation Tool Selection

| Dataset Size | Records | Triples | Recommendation |
|-------------|---------|---------|----------------|
| Small | < 32K | < 672K | Either tool works; PyShacl is simpler to deploy |
| Medium | 32K-128K | 672K-2.7M | RDFox preferred; PyShacl usable with caution |
| Large | > 128K | > 2.7M | RDFox essential |

Note: PyShacl cannot parallelize SHACL validation because the full UCO graph must be loaded into memory. For large datasets, the "many small graphs" pattern combined with a graph database is the recommended approach.

## Format Selection

| Format | Pros | Cons | When to Use |
|--------|------|------|-------------|
| JSON-LD | Native CASE format, 20% faster validation | 2.6x larger files | Default for CASE/UCO interchange |
| Turtle (TTL) | 2.6x smaller files, human-readable | Slower validation | Storage-constrained environments, version control |

## Practical Recommendations

1. **Estimate before building.** Use `graph.estimate_triples()` to understand your data's scale before committing to a partitioning strategy.

2. **Partition early.** Don't build a 500K-object graph and then try to split it. Partition at the data source level.

3. **Keep graphs under 50K objects** for comfortable in-memory processing on a standard workstation (32 GB RAM).

4. **Use JSON-LD for interchange, TTL for storage.** JSON-LD is the standard CASE format and validates faster, but TTL is 2.6x smaller for archival.

5. **Use a graph database for cross-graph queries.** Apache Jena Fuseki is free, well-documented, and handles SPARQL natively. Load your partitioned graphs as named graphs for combined analysis.

6. **Monitor memory during serialization.** Serialization memory scales linearly — plan for ~50 KB per record with PyShacl, ~27 KB with RDFox.

7. **Validate in batches.** If using PyShacl, validate each partition separately rather than the combined dataset. RDFox handles larger datasets but still benefits from partitioned validation.

8. **Consider your deployment target.** Field laptops have very different constraints than lab servers. The SDK's partitioning helpers let you build the same quality output regardless of hardware.

## Further Reading

- [pDNS Benchmarking Experiment](https://github.com/vulnmaster/pDNS-Benchmarking-Experiment) — Full benchmark methodology and results
- [ONTOLOGY_REFERENCE.md](../ONTOLOGY_REFERENCE.md) — Complete class reference for triple estimation
- [MAPPING_GUIDE.md](MAPPING_GUIDE.md) — Domain mapping for forensic data types
