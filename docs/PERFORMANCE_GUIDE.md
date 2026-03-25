# CASE/UCO Performance and Engineering Tradeoffs

This guide helps developers make informed engineering decisions when building CASE/UCO knowledge graphs. The data comes from the [pDNS Benchmarking Experiment](https://github.com/vulnmaster/pDNS-Benchmarking-Experiment), which measured serialization and validation performance across dataset sizes from 1,000 to 512,000 records (21,000 to 10.7 million RDF triples). The pDNS Benchmarking Experiment repository is a private repository as it contains some data about commercial tool benchmarks that cannot be disclosed publicly. Request access from vulnmaster if you need to see it.

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

### Validation Performance (case_validate / PyShacl)

Use [case-utils](https://github.com/casework/CASE-Utilities-Python) (`pip install case-utils`) to validate SDK output. The `case_validate` CLI wraps PyShacl with CASE-specific configuration:

```bash
case_validate --built-version case-1.4.0 my-output.jsonld
```

| Records | Triples | PyShacl (TTL) | PyShacl (JSON-LD) | Memory |
|---------|---------|--------------|-------------------|--------|
| 1,000 | 21,000 | 1.3s | 1.1s | 75 MB |
| 8,000 | 168,000 | 9.4s | 7.4s | 356 MB |
| 32,000 | 672,000 | 35.8s | 28.1s | 1,330 MB |
| 64,000 | 1,344,000 | 71.9s | 54.4s | 2,630 MB |
| 128,000 | 2,688,000 | 141.1s | 112.9s | 5,189 MB |
| 256,000 | 5,376,000 | 277.2s | 224.2s | 10,348 MB |
| 512,000 | 10,752,000 | 561.1s | 451.7s | 20,642 MB |

### Key Findings

- **JSON-LD files are 2.6x larger** than TTL but validate ~20% faster in PyShacl
- **Memory per record:** ~50 KB with PyShacl
- **Memory is the primary constraint** before CPU — plan your graph sizes accordingly
- PyShacl achieves 100% validation accuracy across all dataset sizes
- Commercial graph store validators may offer better performance at scale; evaluate options for your deployment

## The "Many Small Graphs" Pattern

The single most important engineering decision is how to partition your data into graphs. Building one massive graph for an entire disk image or case will exhaust memory on most workstations. Instead, build focused graphs and load them into a graph database for combined analysis.

### Why Not Just Split by Object Count?

A naive split — taking the first N objects, then the next N — will break relationship integrity. Digital investigation graphs are highly interconnected: an `InvestigativeAction` references the `Tool` that produced it, which references `ObservableObject` instances, which have `Facet` sub-objects. A count-based split can put a referencing object in one partition and its target in another, producing incomplete or invalid graphs.

**Partition by natural forensic boundaries instead.** Each partition should contain a self-contained unit of work where all cross-references resolve within the same graph.

### Recommended Partitioning Strategies

| Forensic Scenario | Partition By | Typical Graph Size | Rationale |
|-------------------|-------------|-------------------|-----------|
| Full disk forensics | Directory or volume | 5K-50K objects per graph | Natural hierarchy, references stay together |
| Network forensics | Time window or session | 1K-10K objects per graph | Temporal boundaries, session-complete |
| Mobile forensics | App or data type | 500-5K objects per graph | Natural app boundaries |
| Email forensics | Mailbox or date range | 1K-10K objects per graph | User-centric, chronological |
| Multi-device case | Device | Variable per device | Evidence provenance boundaries |
| IoC / catalog data | Batch of N items | 10K-50K objects per graph | Safe — objects are independent |

### Implementation with the SDK

```python
from case_uco.graph import CASEGraph

# Partition by forensic boundary (recommended for investigative graphs)
for volume in disk_image.volumes:
    graph = CASEGraph(kb_prefix="http://example.org/kb/case-001/")
    for item in volume.files:
        graph.create(ObservableObject, has_facet=[...])
    graph.write(f"volume-{volume.name}.jsonld")
```

> **`split()` safety note:** The SDK's `split()` helper divides by object index.
> It is safe for **catalog-style graphs** where objects are independent (file hash
> lists, DNS records, IoC feeds). It is **not safe** for investigative graphs with
> cross-object relationships — use source-level partitioning for those.

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
| Workstation (64 GB) | 64 GB | ~256K objects (~5.4M triples) | Large cases, multiple devices |
| Server (128+ GB) | 128+ GB | ~512K+ objects (~10M+ triples) | Enterprise, multi-device cases |
| Graph Database | Any | Unlimited (disk-backed) | Combined analysis of partitioned graphs |

### Validation Scaling

| Dataset Size | Records | Triples | PyShacl Guidance |
|-------------|---------|---------|-----------------|
| Small | < 32K | < 672K | Comfortable; single-pass validation works well |
| Medium | 32K-128K | 672K-2.7M | Usable but monitor memory; consider partitioned validation |
| Large | > 128K | > 2.7M | Partition into smaller graphs; consider a graph store validator |

Note: PyShacl cannot parallelize SHACL validation because the full UCO graph must be loaded into memory. For large datasets, the "many small graphs" pattern combined with a graph database is the recommended approach.

## Format Selection

| Format | Pros | Cons | When to Use |
|--------|------|------|-------------|
| JSON-LD | Native CASE format, 20% faster validation | 2.6x larger files | Default for CASE/UCO interchange |
| Turtle (TTL) | 2.6x smaller files, human-readable | Slower validation | Storage-constrained environments, version control |

## Practical Recommendations

1. **Estimate before building.** Use `graph.estimate_triples()` to understand your data's scale before committing to a partitioning strategy.

2. **Partition by forensic boundary, not object count.** Build one graph per volume, per app, per session, or per device — not by arbitrary batch size. This preserves the cross-object relationships that make CASE/UCO graphs useful for investigation.

3. **Keep graphs under 50K objects** for comfortable in-memory processing on a standard workstation (32 GB RAM).

4. **Use JSON-LD for interchange, TTL for storage.** JSON-LD is the standard CASE format and validates faster, but TTL is 2.6x smaller for archival.

5. **Use a graph database for cross-graph queries.** Apache Jena Fuseki is free, well-documented, and handles SPARQL natively. Load your partitioned graphs as named graphs for combined analysis.

6. **Monitor memory during serialization.** Serialization memory scales linearly — plan for ~50 KB per record with PyShacl.

7. **Validate in batches.** Use `case_validate` on each partition separately rather than the combined dataset. This keeps memory usage manageable and avoids PyShacl's scaling limitations.

8. **Consider your deployment target.** Field laptops have very different constraints than lab servers. Source-level partitioning lets you build the same quality output regardless of hardware.

9. **Reserve `split()` for catalog data.** The SDK's `split()` helper divides by object index and is appropriate for independent-object graphs (IoC lists, hash sets, DNS inventories). For investigative graphs with cross-references, partition at the data source instead.

## Further Reading

- [pDNS Benchmarking Experiment](https://github.com/vulnmaster/pDNS-Benchmarking-Experiment) — Full benchmark methodology and results
- [ONTOLOGY_REFERENCE.md](../ONTOLOGY_REFERENCE.md) — Complete class reference for triple estimation
- [MAPPING_GUIDE.md](MAPPING_GUIDE.md) — Domain mapping for forensic data types
- [ECOSYSTEM.md](ECOSYSTEM.md) — Companion tools (case-utils, Fuseki), community extensions, and ontology sources
