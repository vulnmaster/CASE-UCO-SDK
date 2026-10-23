# Cross-Report File Identity

Model the same file as it appears in several forensic reports — a UFED
report, an XRY/XAMN export, an AXIOM case, a re-run of any of them — so that
every report can be ingested on its own, in any order, and still converge on
shared nodes for the file's content and for the file on the exhibit. Each
report keeps exactly what its tool said, and disagreements between tools stay
visible instead of being overwritten.

**Validation basis:** `examples/recipes/build_cross_report_file_identity.py`
builds two synthetic reports of one exhibit in separate graphs, merges them,
re-ingests the first, checks that the merged graph is unchanged, and writes
`examples/recipes/cross-report-file-identity.jsonld` (`case_validate
--built-version case-1.5.0`: `Conforms: True`). Every hash is computed over
bytes defined in the builder. The queries below run against that output in
`mcp_server/tests/test_cross_report_file_identity.py`.

## When to use this recipe

- More than one report describes the same exhibit, or the same content turns
  up on several exhibits, and you need one node to join them on.
- Reports are ingested at different times or by different people, so their
  graphs must merge without coordination (no shared counter, no lookup
  service).
- One tool reports MD5 only and another reports SHA-1 or SHA-256, and you
  still need the entries to meet.
- You want to remove a report later and find what it alone supported.

For mapping one report's own structure, start with the tool recipe
([cellebrite-ufed-xml.md](cellebrite-ufed-xml.md),
[msab-xry-export.md](msab-xry-export.md),
[magnet-axiom-export.md](magnet-axiom-export.md)) and come back here for the
identity layer.

## Classes and properties

| Term | Role here |
|---|---|
| `uco-observable:ContentData` | Content core: one node per hash method, hash value, and size |
| `uco-observable:File` | Exhibit file (one per exhibit and normalized path) and report entry (one per report row) |
| `uco-observable:ContentDataFacet` | `uco-observable:hash`, `uco-observable:sizeInBytes` |
| `uco-observable:FileFacet` | `uco-observable:filePath`, `uco-observable:fileName`, `uco-observable:sizeInBytes`, `uco-observable:modifiedTime` |
| `uco-types:Hash` | `uco-types:hashMethod`, `uco-types:hashValue` |
| `uco-core:Relationship` | `Contained_Within` (content core to exhibit file), `Characterizes` (report entry to exhibit file) |
| `case-investigation:InvestigativeAction` | One per report: `uco-action:instrument` is the tool, `uco-action:result` lists the report entries |

## The three tiers

| Tier | Node | ID key | Holds |
|---|---|---|---|
| Content core | `uco-observable:ContentData` | hash method, hash value (upper-case hex), size | One hash and the size |
| Exhibit file | `uco-observable:File` | exhibit ID, normalized path | Facts every report agrees on: path, name, size, and the union of all reported hashes |
| Report entry | `uco-observable:File` | report ID, the report's own row or artifact ID | What that report said, verbatim, including timestamps and the path as the tool printed it |

A file reported with MD5 and SHA-256 links to two content cores. A second
report that only has MD5 still reaches the same exhibit file through the MD5
core, and its SHA-1 adds a third core. Content seen on two exhibits has one
core linked to two exhibit files.

### Deterministic IDs

Use `case_uco.deterministic_id(cls, *key)`. It returns
`kb:<Class>-<uuid5>` from the class name and the key parts, so the same key
gives the same IRI in every run, in every graph, and in every SDK language
that applies the same rule. Normalize every key part first — upper-case hex,
one path convention per exhibit — because `"abc"` and `"ABC"` are different
keys.

```python
from case_uco import CASEGraph, Ref, deterministic_id
from case_uco.uco.core import Relationship
from case_uco.uco.observable import ContentData, ContentDataFacet, File, FileFacet
from case_uco.uco.types import Hash


def ensure(graph, cls, node_id, **kwargs):
    """Create a shared node once; later mentions reference it by IRI."""
    if not graph.contains(node_id):
        graph.create(cls, id=node_id, **kwargs)
    return Ref(node_id)


def relate(graph, source_id, kind, target_id):
    graph.create_relationship(
        source_id, target_id, kind,
        relationship_id=deterministic_id(Relationship, source_id, kind, target_id),
    )


core_id = deterministic_id(ContentData, "MD5", md5_upper, size)
ensure(graph, ContentData, core_id, has_facet=[
    ContentDataFacet(size_in_bytes=size, hash=[Hash(hash_method="MD5", hash_value=md5_upper)]),
])
exhibit_file_id = deterministic_id(File, exhibit_id, normalized_path)
relate(graph, core_id, "Contained_Within", exhibit_file_id)
```

Pass `relationship_id` as shown. `create_relationship` also derives an ID
from source, target, and kind by default, but that ID does not end in a UUID,
and `case_validate` reports it at Info level (`Conforms: False` unless
`--allow-info`).

Facets and hashes written inline need no IDs of their own. The SDK derives a
facet's ID from its owner and its class, and a hash's ID from its owner and
its value. A deterministic owner therefore gets deterministic facets, and two
owners never share one.

### One facet per object

`uco-core:hasFacet` is inverse-functional in UCO: a facet belongs to exactly
one object. Two hash-specific cores sharing one `FileFacet` fail validation
("hasFacet must not be used to link two objects to one Facet"), and the SDK
raises `SharedFacetError` at insertion when you try. Give each core its own
`ContentDataFacet`; the owner-derived IDs keep them distinct.

### Content core

```json
{
  "@id": "kb:ContentData-fd5a8e56-f3c8-57db-b92a-52f79813478a",
  "@type": "uco-observable:ContentData",
  "uco-core:hasFacet": [
    {
      "@id": "kb:ContentDataFacet-ffa377b5-422f-58d4-a396-c00247471dd6",
      "@type": "uco-observable:ContentDataFacet",
      "uco-observable:hash": [
        {
          "@id": "kb:Hash-3dd21cae-6ec9-57ef-a646-c0be3e468280",
          "@type": "uco-types:Hash",
          "uco-types:hashMethod": "MD5",
          "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": "3232597C3C94BE4067FB3D9EE08B3FBB"}
        }
      ],
      "uco-observable:sizeInBytes": {"@type": "xsd:integer", "@value": "28"}
    }
  ]
}
```

### Exhibit file after both reports merged

Report A supplied MD5 and SHA-256, report B supplied MD5 and SHA-1. The facet
has one ID in both report graphs, so the merge unions its hashes:

```json
{
  "@id": "kb:File-e7fdd28a-7ada-580c-9d4b-fab27dcd154c",
  "@type": "uco-observable:File",
  "uco-core:hasFacet": [
    {
      "@id": "kb:FileFacet-1df51143-aeba-5fb2-a8a2-fccb4a60663d",
      "@type": "uco-observable:FileFacet",
      "uco-observable:fileName": "IMG_0001.jpg",
      "uco-observable:filePath": "/storage/1A2B-3C4D/DCIM/Camera/IMG_0001.jpg",
      "uco-observable:sizeInBytes": {"@type": "xsd:integer", "@value": "28"}
    },
    {
      "@id": "kb:ContentDataFacet-41cb3336-4abf-55ea-8df9-5e2c6e152a24",
      "@type": "uco-observable:ContentDataFacet",
      "uco-observable:hash": [
        {"@id": "kb:Hash-8a44aa8f-376c-5ff1-a6f8-354bae6afc72", "@type": "uco-types:Hash",
         "uco-types:hashMethod": "MD5",
         "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": "3232597C3C94BE4067FB3D9EE08B3FBB"}},
        {"@id": "kb:Hash-1dacf08e-7467-5e43-981f-0959a19f2e71", "@type": "uco-types:Hash",
         "uco-types:hashMethod": "SHA256",
         "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": "CA180452989882FBF20F677EA20934137D4188F339EEB28D59B6146F93369726"}},
        {"@id": "kb:Hash-6d8e3ee2-f74e-528e-91ba-f44f479a7000", "@type": "uco-types:Hash",
         "uco-types:hashMethod": "SHA1",
         "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": "E75085C47B98ACC4800AF0EA9EB2E6DF5D841FB8"}}
      ],
      "uco-observable:sizeInBytes": {"@type": "xsd:integer", "@value": "28"}
    }
  ]
}
```

### Report entry, as the tool reported it

The path keeps the tool's own separators and the timestamp is the tool's own
rounding (report A said 10:15:13, report B said 10:15:12 for a FAT volume with
2-second resolution):

```json
{
  "@id": "kb:File-2044e96d-8331-59c9-90cd-544cd5e08dff",
  "@type": "uco-observable:File",
  "uco-core:name": "REPORT-B row files/77",
  "uco-core:hasFacet": [
    {
      "@id": "kb:FileFacet-18fd2e56-8de5-53d5-8ea7-3c76a4e183d7",
      "@type": "uco-observable:FileFacet",
      "uco-observable:fileName": "IMG_0001.jpg",
      "uco-observable:filePath": "\\storage\\1A2B-3C4D\\DCIM\\Camera\\IMG_0001.jpg",
      "uco-observable:modifiedTime": {"@type": "xsd:dateTime", "@value": "2023-01-02T10:15:12+00:00"},
      "uco-observable:sizeInBytes": {"@type": "xsd:integer", "@value": "28"}
    },
    {
      "@id": "kb:ContentDataFacet-ed313093-3a8f-54b5-8eed-628c60d7c09e",
      "@type": "uco-observable:ContentDataFacet",
      "uco-observable:hash": [
        {"@id": "kb:Hash-236fb0d7-7ee1-5b9a-8eec-2562d7cfa9da", "@type": "uco-types:Hash",
         "uco-types:hashMethod": "MD5",
         "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": "3232597C3C94BE4067FB3D9EE08B3FBB"}},
        {"@id": "kb:Hash-e08588e7-ffa6-5c77-92a2-d57fca4f410d", "@type": "uco-types:Hash",
         "uco-types:hashMethod": "SHA1",
         "uco-types:hashValue": {"@type": "xsd:hexBinary", "@value": "E75085C47B98ACC4800AF0EA9EB2E6DF5D841FB8"}}
      ],
      "uco-observable:sizeInBytes": {"@type": "xsd:integer", "@value": "28"}
    }
  ]
}
```

```json
{
  "@id": "kb:Relationship-8d6d9116-6d46-5791-a586-9837e841eb4d",
  "@type": "uco-core:Relationship",
  "uco-core:source": [{"@id": "kb:File-ce8ecd15-ed3e-5fab-bd59-563c2ecbb10e"}],
  "uco-core:target": [{"@id": "kb:File-e7fdd28a-7ada-580c-9d4b-fab27dcd154c"}],
  "uco-core:kindOfRelationship": "Characterizes",
  "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"}
}
```

## Timestamps and the identity key

Keep timestamps out of the content-core key. Content identity is the bytes,
and the hash and size already pin those down; a modified time describes one
copy of the file, not its content.

If you still want a FAT-tolerant time in a key (to tell apart two
same-content files at one path across acquisitions, say), use it in the key
only and never assert the rounded value as `uco-observable:modifiedTime`. A
graph that states a 4-second-rounded time as the file's modified time is
stating something no tool reported. Bucketing also splits at the edges:
floor-to-4 s puts 10:15:15 and 10:15:16 in different buckets, though they are
one second apart. The exemplar instead keeps each tool's own time on its
report entry, where the disagreement query below finds it.

## Merging and re-running

Build one graph per report, then merge:

```python
combined = CASEGraph()
for report_graph in report_graphs:
    combined.load(report_graph.serialize(), on_duplicate="merge_compatible")
```

- Shared nodes with one `@id` merge. Inline facets and hashes that carry the
  same `@id` in two graphs are one node, so their properties are combined (the
  exhibit file above gained SHA-1 this way).
- A conflicting single value — two sizes for one exhibit file — raises
  `DuplicateNodeError`. Read it as a finding: the exhibit-file key is too
  coarse (add the acquisition ID if the exhibit was imaged twice and the file
  changed) or one tool is wrong. Don't catch and drop it.
- Re-ingesting a report produces identical nodes, so the merged graph does not
  change. The exemplar asserts this.
- Use `on_duplicate="merge_identical"` instead when a re-run should prove
  nothing changed. It raises if any shared node, including an inline facet,
  differs.

## SDK helper

`case_uco.vendors.file_identity.add_reported_file` writes one report row with
all three tiers and both relationships, using the same keys as the exemplar.
It normalizes the path and the hash spelling (`sha-1` and lower-case hex become
`SHA1` and upper-case), and when a second row in the same graph names the same
exhibit file it merges that row's hashes in. The Cellebrite `report.xml` reader
uses it through `tagged_files_to_graph`; call it directly for other tools:

```python
from case_uco import CASEGraph
from case_uco.vendors.file_identity import add_reported_file

graph = CASEGraph()
nodes = add_reported_file(
    graph,
    exhibit="EXHIBIT-001",
    report="REPORT-B",
    row="files/77",
    path="\\storage\\1A2B-3C4D\\DCIM\\Camera\\IMG_0001.jpg",
    size=29,
    hashes=[("md5", "0123456789abcdef0123456789abcdef")],
)
print(nodes.exhibit_file, nodes.entry, nodes.content_cores)
```

Pick `exhibit` and `report` keys that every ingest job can compute on its own:
an exhibit reference and the report file's SHA-256 both work, a database row
number does not.

## Competency questions

Load the merged graph (or all report graphs) into one SPARQL dataset. Each
query below returns the stated rows on the exemplar.

**Which report entries, from which tools, describe the content with this
MD5?** (2 rows: one per report, each with its own path and timestamp)

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-action: <https://ontology.unifiedcyberontology.org/uco/action/>
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-types: <https://ontology.unifiedcyberontology.org/uco/types/>
SELECT ?entry ?reportedPath ?modified ?toolName WHERE {
  ?core a uco-observable:ContentData ;
        uco-core:hasFacet/uco-observable:hash ?h .
  ?h uco-types:hashMethod "MD5" ; uco-types:hashValue ?v .
  FILTER (UCASE(STR(?v)) = "3232597C3C94BE4067FB3D9EE08B3FBB")
  ?r1 uco-core:source ?core ; uco-core:target ?file ;
      uco-core:kindOfRelationship "Contained_Within" .
  ?r2 uco-core:source ?entry ; uco-core:target ?file ;
      uco-core:kindOfRelationship "Characterizes" .
  ?entry uco-core:hasFacet ?ff .
  ?ff a uco-observable:FileFacet ; uco-observable:filePath ?reportedPath .
  OPTIONAL { ?ff uco-observable:modifiedTime ?modified }
  ?action uco-action:result ?entry ;
          uco-action:instrument/uco-core:name ?toolName .
}
ORDER BY ?toolName
```

**Which hashes does each exhibit file have, and from how many reports?**
(2 rows: the photo with MD5, SHA-1, and SHA-256 from 2 reports; the notes
file with MD5 and SHA-256 from 1)

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-types: <https://ontology.unifiedcyberontology.org/uco/types/>
SELECT ?path (GROUP_CONCAT(DISTINCT ?method; separator=",") AS ?methods)
       (COUNT(DISTINCT ?entry) AS ?entries) WHERE {
  ?file uco-core:hasFacet ?ff .
  ?ff a uco-observable:FileFacet ; uco-observable:filePath ?path .
  ?file uco-core:hasFacet/uco-observable:hash/uco-types:hashMethod ?method .
  ?r uco-core:target ?file ; uco-core:kindOfRelationship "Characterizes" ;
     uco-core:source ?entry .
}
GROUP BY ?path
ORDER BY ?path
```

**Where do reports disagree on a file's modified time?** (1 row: the photo,
10:15:12 against 10:15:13)

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
SELECT ?file (COUNT(DISTINCT ?t) AS ?values) (MIN(?t) AS ?earliest) (MAX(?t) AS ?latest)
WHERE {
  ?r uco-core:target ?file ; uco-core:kindOfRelationship "Characterizes" ;
     uco-core:source ?entry .
  ?entry uco-core:hasFacet/uco-observable:modifiedTime ?t .
}
GROUP BY ?file
HAVING (COUNT(DISTINCT ?t) > 1)
```

**After removing a report, which content cores are no longer in any exhibit
file?** Remove the report's `Characterizes` relationships, then the
`Contained_Within` relationships of every exhibit file left with none. On
the exemplar the query returns 0 rows before and 2 rows after retracting
report A: the notes file's MD5 and SHA-256 cores. The photo's SHA-256 core
stays, because report B still places that content on the exhibit.

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
SELECT ?core WHERE {
  ?core a uco-observable:ContentData .
  FILTER NOT EXISTS {
    ?r uco-core:source ?core ; uco-core:kindOfRelationship "Contained_Within" .
  }
}
```

This query replaces a hand-kept link count: the graph already knows what
points at a core.

## Anti-patterns

- **One facet shared by several objects.** `hasFacet` is inverse-functional;
  validation fails and the SDK raises `SharedFacetError`. One facet per
  object.
- **A node reference written as a string.** `manufacturer="kb:org-1"` or a
  bare `rdflib.URIRef` assigned before 1.33.0 serialized as a string literal.
  Pass the object returned by `graph.create()`, `case_uco.Ref("kb:...")`, or
  `rdflib.URIRef(...)`; the SDK now writes `{"@id": ...}` and rejects plain
  strings on properties that take a node.
- **`Child_Of` between tiers.** UCO uses `Child_Of` for hierarchy (a process
  and its parent, a file and its directory). A query for the children of a
  directory would return report entries. Use `Contained_Within` and
  `Characterizes`.
- **Rounded time asserted as `modifiedTime`.** Keep the rounded value in the
  key only, if at all.
- **Typing vocabulary values.** `{"@type": "uco-vocabulary:HashNameVocab",
  "@value": "MD5"}` warns in UCO 1.x and fails in 2.0. Write the plain string;
  the constants in `case_uco.uco.vocabulary` are plain strings.
- **Splitting by object count.** A report entry, its exhibit file, and its
  cores must land in graphs that are merged before querying. Partition by
  report or by exhibit, never every N nodes.
- **Overwriting tool disagreements.** Don't "fix" report B's timestamp to
  match report A on the exhibit file. Each report entry keeps its tool's
  value.

## Checklist

1. Choose the exhibit ID and one path convention per exhibit; write the
   normalizer before ingesting anything.
2. For each report, build a fresh `CASEGraph` and an `InvestigativeAction`
   whose instrument is the tool and whose result is the report entries.
3. For each reported file, upper-case the hex hashes and create the report
   entry (`deterministic_id(File, report_id, row_id)`) with the tool's values
   verbatim.
4. `ensure` the exhibit file (`deterministic_id(File, exhibit_id, path)`) with
   only the agreed facts and the hashes this report supplied.
5. `ensure` one content core per hash
   (`deterministic_id(ContentData, method, value, size)`) with its own
   `ContentDataFacet`.
6. Link core to exhibit file with `Contained_Within` and report entry to
   exhibit file with `Characterizes`, passing
   `relationship_id=deterministic_id(Relationship, source, kind, target)`.
7. Write each report graph, then merge with
   `load(..., on_duplicate="merge_compatible")`; treat `DuplicateNodeError`
   as a finding.
8. Run `case_validate --built-version case-1.5.0` on the merged graph.
9. Run the competency queries; investigate every timestamp disagreement.

## Related

- [cellebrite-ufed-xml.md](cellebrite-ufed-xml.md) — UFED reports, `.ufd`/`.ufdx` summaries, and version drift
- [msab-xry-export.md](msab-xry-export.md) — XRY and XAMN exports
- [magnet-axiom-export.md](magnet-axiom-export.md) — AXIOM exports
- [file-system.md](file-system.md) — files, directories, and their facets
- [advanced-file-patterns.md](advanced-file-patterns.md) — carved, embedded, and recovered files
- [large-datasets.md](large-datasets.md) — partitioning by forensic boundary
- [round-trip.md](round-trip.md) — loading and merging graphs
