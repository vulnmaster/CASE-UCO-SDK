# Forensic Tool Capability Extension (toolcap)

A CASE/UCO extension ontology for modeling which digital forensic tools can parse which applications, on which platforms, and for which observable types. Built in compliance with the [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing).

## CDO Playground Compliance

This extension follows all CDO Community Playground requirements:

- **T-Box only** — All concepts are defined as `owl:Class`, `owl:ObjectProperty`, or `owl:DatatypeProperty` (never `owl:NamedIndividual`)
- **Mandatory subclassing** — `ToolCapability rdfs:subClassOf uco-core:UcoObject` and `CapabilityMatrix rdfs:subClassOf uco-core:ContextualCompilation`
- **Comprehensive documentation** — Every class and property includes `rdfs:label` and detailed `rdfs:comment`
- **Separate OWL and SHACL** — OWL definitions in `toolcap.ttl`, SHACL shapes in `toolcap-shapes.ttl`
- **Validated exemplar** — `toolcap-exemplar.ttl` passes `case_validate` with `Conforms: True`

## Files

| File | Purpose |
|------|---------|
| `toolcap.ttl` | OWL ontology (T-Box): class and property definitions |
| `toolcap-shapes.ttl` | SHACL shapes: property constraints for validation |
| `toolcap-exemplar.ttl` | Exemplar instances (A-Box): validated example data |
| `example_capability_matrix.py` | Python example using the CASE-UCO-Libraries builders |

## Classes

- **ToolCapability** (`toolcap:ToolCapability`, subclass of `uco-core:UcoObject`) — A formal assertion that a specific digital forensic tool can successfully parse, extract, or decode data from a specific application on one or more device platforms.
- **CapabilityMatrix** (`toolcap:CapabilityMatrix`, subclass of `uco-core:ContextualCompilation`) — A named, versioned collection of ToolCapability assertions that together represent a comprehensive comparison of which digital forensic tools support which applications.

## Properties

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `toolcap:tool` | `uco-tool:Tool` | exactly 1 | The forensic tool that has this capability |
| `toolcap:application` | `uco-observable:ObservableObject` | exactly 1 | The application whose data can be parsed |
| `toolcap:supportedPlatform` | `xsd:string` | 0..* | Platforms (Android, iOS, Windows, etc.) |
| `toolcap:parsedObservableType` | `xsd:string` | 0..* | Observable types (messages, contacts, etc.) |
| `toolcap:toolVersion` | `xsd:string` | 0..1 | Tool version tested |
| `toolcap:isVerified` | `xsd:boolean` | 0..1 | Whether independently verified |
| `toolcap:lastTestedDate` | `xsd:dateTime` | 0..1 | When last tested |
| `toolcap:matrixName` | `xsd:string` | 0..1 | Name of the capability matrix |
| `toolcap:matrixVersion` | `xsd:string` | 0..1 | Version of the capability matrix |

## Validation

Validate the exemplar with `case_validate` (from `pip install case-utils`):

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/toolcap/toolcap.ttl \
  --ontology-graph extensions/toolcap/toolcap-shapes.ttl \
  --inference rdfs --allow-info \
  extensions/toolcap/toolcap-exemplar.ttl
```

Expected output:

```
Validation Report
Conforms: True
```

## Python Builder Example

```bash
python extensions/toolcap/example_capability_matrix.py
```

See `example_capability_matrix.py` for a complete working example using the CASE-UCO-Libraries Python builder to construct a capability matrix comparing Magnet AXIOM and Cellebrite Physical Analyzer across WeChat, Telegram, and Outlook.
