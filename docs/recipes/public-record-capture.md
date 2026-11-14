# Public-Record Capture Bundles

Map a manifest of fetched public web records — HTML, PDF, XML, JSON, and
the rows that failed — into one CASE/UCO graph. The captured bytes stay
observables. A document that the bytes are about, such as an order or a
memorandum, stays a separate object. Collector-authored links stay
annotations.

**When to use this recipe**

- A JSONL or CSV manifest lists source URL, HTTP status, retrieval time,
  byte length, and SHA-256 for each stored file
- Some rows are redirects (`final_url` differs from the requested URL)
- Some rows failed and stored no bytes
- Later pages quote, name, or retitle an earlier document
- A sidecar or catalog adds `see_also` links that the documents themselves
  do not state

For a tool that actually ran and recorded its name and version, start from
[starter-tool-run.md](starter-tool-run.md). For a file listing with no HTTP
retrieval, use [starter-filesystem-report.md](starter-filesystem-report.md).
Criminal charging instruments, pleas, and sentences stay in
[legal-process-modeling.md](legal-process-modeling.md). This recipe does not
apply to those.

## Classes

| Concept | Class | Why |
|---|---|---|
| Stored file | `uco-observable:ObservableObject` + `uco-observable:FileFacet` + `uco-observable:ContentDataFacet` | Bytes, path, recorded MIME, size |
| Digest | `uco-types:Hash` | `uco-types:hashMethod` `SHA256` (not `SHA-256`); one `Hash` node shared by byte-identical files |
| Requested address | `uco-observable:URL` + `uco-observable:URLFacet` | `uco-observable:fullValue` is the URL string |
| Retrieval | `case-investigation:InvestigativeAction` | `uco-action:object` is the URL, `uco-action:result` is the file, `uco-action:endTime` is the retrieval timestamp |
| HTTP status | `uco-action:ActionArgumentFacet` | `uco-action:argumentName` `http_status` |
| Failed row | `case-investigation:InvestigativeAction` | `uco-action:actionStatus` `Fail`; no result file |
| The work the file is about | `uco-core:UcoObject` | CASE/UCO has no executive-order or presidential-document class |
| File is a rendition of that work | `uco-core:Relationship` | `uco-core:kindOfRelationship` `Characterizes` |
| Document names another document | `uco-core:Relationship` | `uco-core:kindOfRelationship` `Related_To`, with the verified substring in `uco-core:description` |
| Redirect | `uco-core:Relationship` | `uco-core:kindOfRelationship` `Resolved_To` from the requested URL to the final URL |
| Collector `see_also` | `uco-core:Annotation` | `uco-core:statement` records `relationship_status`; `uco-core:object` lists the nodes |
| Exhibit | `case-investigation:ProvenanceRecord` | Groups the retrieval and the manifest |
| Review | `case-investigation:Investigation` | One graph for the bundle |

`uco-action:actionStatus` members used here are `Success`, `Fail`, and
`Complete/Finish`. `Failed` is not a member.

## Modeling pattern

Copied from `examples/public-record-capture/capture.jsonld`, which
`case_validate --built-version case-1.5.0 --allow-info` accepts
(`Conforms: True`; remaining results are `sh:Info` UUID suggestions).

A successful retrieval. `uco-action:endTime` is a real timestamp from the
capture record:

```json
{
  "@id": "kb:fetch-order",
  "@type": "case-investigation:InvestigativeAction",
  "uco-core:name": "HTTP GET data/order.html",
  "uco-action:actionStatus": "Success",
  "uco-action:endTime": {
    "@type": "xsd:dateTime",
    "@value": "2026-10-07T22:32:51+00:00"
  },
  "uco-action:object": { "@id": "kb:url-order" },
  "uco-action:result": { "@id": "kb:file-order-html" }
}
```

A failed retrieval stores no file. The status value is `Fail`:

```json
{
  "@id": "kb:fetch-missing",
  "@type": "case-investigation:InvestigativeAction",
  "uco-core:name": "HTTP GET missing-release",
  "uco-action:actionStatus": "Fail",
  "uco-core:description": ["No content file was stored."]
}
```

The work is a `uco-core:UcoObject`. A calendar date with no clock time stays
in `uco-core:description`. `uco-core:startTime` is `xsd:dateTime`, so writing
midnight would invent a time the record does not have:

```json
{
  "@id": "kb:work-order-1",
  "@type": "uco-core:UcoObject",
  "uco-core:name": "Example Order 1",
  "uco-core:description": [
    "Typed as uco-core:UcoObject because CASE/UCO has no executive-order class. A published signing date of 2026-09-29 is date-only and is not written to startTime."
  ]
}
```

The file characterizes that work. A stated citation uses `Related_To` and
puts the verified substring in the description. A collector label is an
`uco-core:Annotation`, not a relationship:

```json
{
  "@id": "kb:rel-Characterizes-92f81076e210",
  "@type": "uco-core:Relationship",
  "uco-core:source": [{ "@id": "kb:file-order-html" }],
  "uco-core:target": [{ "@id": "kb:work-order-1" }],
  "uco-core:kindOfRelationship": "Characterizes",
  "uco-core:isDirectional": { "@type": "xsd:boolean", "@value": "true" },
  "uco-core:description": "The captured HTML is a rendition of the order. The vocabulary has no rendition kind."
}
```

```json
{
  "@id": "kb:rel-Related_To-af8b173f4f53",
  "@type": "uco-core:Relationship",
  "uco-core:source": [{ "@id": "kb:work-order-1" }],
  "uco-core:target": [{ "@id": "kb:work-memo" }],
  "uco-core:kindOfRelationship": "Related_To",
  "uco-core:isDirectional": { "@type": "xsd:boolean", "@value": "true" },
  "uco-core:description": "Verified substring in the order text: Memorandum M-1. The vocabulary has no Cites kind."
}
```

```json
{
  "@id": "kb:note-curator",
  "@type": "uco-core:Annotation",
  "uco-core:name": "Curator label",
  "uco-core:statement": [
    "Collector see_also is a curator label. It is an Annotation, not a Relationship."
  ],
  "uco-core:object": [{ "@id": "kb:work-order-1" }]
}
```

Do not set `uco-core:createdBy` to the public official who signed a document.
That property is the identity that created the UCO record.

## From `process_document_file`

`process_document_file` (MCP tool, Python function, and CLI
`--source-url` / `--retrieved-at` / `--http-status`) emits the URL and
retrieval nodes above for one captured file. Pass `source_url` (absolute
`http`/`https`, no credentials), and optionally `retrieved_at` and
`http_status`. A full ISO 8601 timestamp becomes `uco-action:endTime`; a date
alone goes into the action's description. Without `source_url` the output is
unchanged. Redirects, failed rows, and the work the file is about are still
added by hand.

## Anti-patterns

- Do not type an executive order as `legalproc:ChargingInstrument`.
  Do not type it as a bill, a resolution, or a presidential signature or
  veto of legislation. Those are different acts from an executive order.
- Do not put a date-only publication or signing date into
  `uco-core:startTime` or `uco-action:endTime`.
- Do not treat a catalog `see_also` array as something the captured document
  said.
- Do not overwrite a recorded MIME type when the leading bytes sniff as
  something else. Keep the recorded type on `uco-observable:ContentDataFacet`
  and state the disagreement on an `uco-core:Annotation`.
- Do not assert a tool when the manifest has no tool name or version.

## Checklist

1. Recompute SHA-256 and byte length. Stop if they disagree with the manifest.
2. Create one `uco-observable:ObservableObject` per stored file, including
   provenance sidecars and the manifest itself.
3. Share one `uco-types:Hash` across files whose digests match.
4. Create one `case-investigation:InvestigativeAction` per manifest row.
   Use `Success` when a file was stored and `Fail` when it was not.
5. Put full retrieval timestamps on `uco-action:endTime`. Leave date-only
   official dates in descriptions.
6. Create one `uco-core:UcoObject` per work, and a `Characterizes`
   relationship from each content file to that work.
7. Add a `Related_To` relationship only when a verified substring in a
   captured file names the target. Quote that substring in
   `uco-core:description`.
8. Add an `uco-core:Annotation` for each collector-authored link.
9. Validate with `case_validate --built-version case-1.5.0 --allow-info`
   when IRIs are deterministic slugs rather than UUID suffixes.

## Validated exemplar

`examples/public-record-capture/build_capture.py` writes
`examples/public-record-capture/capture.jsonld`.

Validated against CASE/UCO built-in shapes `case-1.5.0` with
`case_validate --built-version case-1.5.0 --allow-info` (case-utils 0.18.0):
`Conforms: True`.
The only results are `sh:Info` suggestions that UcoThing IRIs end in a UUID.

## Related

- [qudt-quantities-and-units.md](qudt-quantities-and-units.md) — numbers with units in a captured record (weather readings, measurements)
- [starter-filesystem-report.md](starter-filesystem-report.md) — file, hash, and path facets
- [starter-tool-run.md](starter-tool-run.md) — when the collector names a tool
- [chain-of-custody.md](chain-of-custody.md) — provenance records
- [legal-process-modeling.md](legal-process-modeling.md) — criminal process, which this bundle is not
