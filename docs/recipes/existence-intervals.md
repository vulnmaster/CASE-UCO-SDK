# Existence Intervals and Temporal Modeling

> See [Recipe Index](INDEX.md) for all recipes.

Model time-bounded existence of entities — roles held over periods, temporal relationships between events, and integration with OWL-Time, gUFO, and BFO ontologies. Based on [CASE-Examples/existence_intervals](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/existence_intervals).

This recipe covers extended ontology patterns used by the CASE/UCO community and the CAC Ontology.

## Approaches

The CASE-Examples illustrate four parallel approaches to the same concept (an entity existing over a time period). Choose based on your project's ontology stack:

| Approach | When to use |
|---|---|
| **Custom `ex:` intervals** | Lightweight; no external ontology dependency |
| **OWL-Time** (`time:Interval`, `time:Instant`) | W3C standard; broad tooling support |
| **gUFO** (`gufo:Object`, `TemporaryInstantiationSituation`) | Foundational ontology; used by CAC Ontology |
| **BFO** (`obo:BFO_*` temporal regions) | Biomedical/scientific ontology stack |

## OWL-Time pattern

The most commonly applicable pattern for forensic timelines:

```python
# This uses raw JSON-LD since OWL-Time classes are not in the SDK.
# Add the OWL-Time context and construct the objects manually.

from case_uco import CASEGraph
import json

graph = CASEGraph(extra_context={
    "time": "http://www.w3.org/2006/time#",
    "ex": "http://example.org/ontology/",
})

# A person who held a role during a specific interval
# Model as JSON-LD objects added directly to the graph

person = {
    "@id": "kb:person-1",
    "@type": "ex:Person",
    "uco-core:name": "...",
    "time:hasTime": {"@id": "kb:interval-1"},
}

interval = {
    "@id": "kb:interval-1",
    "@type": "time:Interval",
    "time:hasBeginning": {
        "@id": "kb:instant-start",
        "@type": "time:Instant",
        "time:inXSDDateTimeStamp": {
            "@type": "xsd:dateTimeStamp",
            "@value": "...",  # ISO 8601 from source
        },
    },
    "time:hasEnd": {
        "@id": "kb:instant-end",
        "@type": "time:Instant",
        "time:inXSDDateTimeStamp": {
            "@type": "xsd:dateTimeStamp",
            "@value": "...",  # from source
        },
    },
}

# Load raw JSON-LD into the graph
raw_doc = json.dumps({
    "@context": {
        "time": "http://www.w3.org/2006/time#",
        "ex": "http://example.org/ontology/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "kb": "http://example.org/kb/",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    },
    "@graph": [person, interval],
})
graph.load(raw_doc)

graph.write("existence_intervals.jsonld")
```

## gUFO pattern

For projects using the Unified Foundational Ontology (used by the CAC Ontology):

```python
graph = CASEGraph(extra_context={
    "gufo": "http://purl.org/nemo/gufo#",
    "ex": "http://example.org/ontology/",
})

# A temporary role instantiation
situation = {
    "@id": "kb:situation-1",
    "@type": "gufo:TemporaryInstantiationSituation",
    "ex:bearer": {"@id": "kb:person-1"},
    "ex:type": {"@id": "ex:StudentRole"},
    "ex:startTime": {"@type": "xsd:dateTime", "@value": "..."},
    "ex:endTime": {"@type": "xsd:dateTime", "@value": "..."},
}

raw_doc = json.dumps({
    "@context": {
        "gufo": "http://purl.org/nemo/gufo#",
        "ex": "http://example.org/ontology/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "kb": "http://example.org/kb/",
    },
    "@graph": [situation],
})
graph.load(raw_doc)
```

## Notes

- OWL-Time, gUFO, and BFO classes are **not** generated as SDK dataclasses — use raw JSON-LD dictionaries loaded via `graph.load()`.
- Add the appropriate context prefixes via `CASEGraph(extra_context={...})`.
- For simple temporal bounds on CASE/UCO objects, use the built-in `start_time`/`end_time` fields on `Action`, `Event`, and `Relationship` — no external ontology needed.
- External ontology patterns are most useful when modeling temporal roles, existence states, or interoperating with systems that already use OWL-Time/gUFO/BFO.
