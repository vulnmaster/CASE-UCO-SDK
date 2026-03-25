# CASE/UCO Ecosystem

The CASE/UCO SDK produces JSON-LD graphs. This guide covers the companion tools you need to validate and query those graphs, the community projects that extend CASE/UCO into specialized domains, and the upstream ontology sources.

## Companion Tools

These tools complete the developer workflow — validation, querying, and format conversion for the graphs your SDK code produces.

### case-utils — Validation & CLI Utilities

**[case-utils](https://github.com/casework/CASE-Utilities-Python)** is the primary tool for validating that your SDK output conforms to CASE/UCO SHACL constraints. It is maintained by the CASE community and provides the `case_validate` CLI.

```bash
pip install case-utils
```

Validate a graph produced by the SDK:

```bash
case_validate \
  --built-version case-1.4.0 \
  my-output.jsonld
```

Validate with a custom extension ontology:

```bash
case_validate \
  --built-version case-1.4.0 \
  --ontology-graph path/to/myext.ttl \
  --ontology-graph path/to/myext-shapes.ttl \
  my-output.jsonld
```

`case_validate` uses [PyShacl](https://github.com/RDFLib/pySHACL) under the hood. For performance characteristics at scale, see [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md).

### Apache Jena Fuseki — Graph Database & SPARQL

For combined analysis of multiple graph files, load them into a SPARQL-capable graph database. [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) is free, well-documented, and handles CASE/UCO's JSON-LD and Turtle formats natively.

Use Fuseki when:
- You need to query across multiple partitioned graphs
- Your dataset exceeds comfortable in-memory sizes (see [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md))
- You want to run SPARQL queries for cross-referencing investigation data

### PyShacl — SHACL Validation Engine

[PyShacl](https://github.com/RDFLib/pySHACL) is the SHACL validation engine used by `case_validate`. You generally don't need to call it directly — use `case_validate` instead, which wraps PyShacl with CASE-specific configuration (built version checking, ontology loading, etc.).

### RDFLib — Python RDF Library

[RDFLib](https://github.com/RDFLib/rdflib) is the Python RDF library that underpins `case-utils`, PyShacl, and this SDK's code generator. If you need to do custom RDF processing beyond what the SDK provides (SPARQL queries in Python, graph merging with custom logic, format conversion), RDFLib is the standard tool.

## Community Extensions

CASE/UCO is designed to be extended. These community projects demonstrate the ontology's reach into specialized domains. Each defines its own OWL classes and SHACL shapes that build on top of CASE/UCO, and each can be used alongside the SDK.

The SDK's `case-uco-generate scaffold` command can generate starter code from any of these extensions:

```bash
case-uco-generate scaffold \
  --extension path/to/extension.ttl path/to/extension-shapes.ttl \
  --lang python \
  --output-dir ./my-extension-classes/
```

### CAC Ontology — Crimes Against Children

**[CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology)** is a comprehensive semantic framework with 35+ specialized modules for modeling child exploitation investigations, including grooming, CSAM detection, victim services, multi-jurisdictional operations, and law enforcement coordination. Maintained by [Project VIC International](https://projectvic.org/). The CAC Ontology extends both UCO/CASE and the lightweight Unified Foundational Ontology (gUFO), and includes extensive SHACL validation, real-world example knowledge graphs, and SPARQL query templates.

**Domains covered:** investigations, hotline operations, forensics, detection, grooming, sextortion, victim impact, task force management, legal outcomes, international coordination, and more.

### SOLVE-IT — Digital Forensics Knowledge Base

**[SOLVE-IT](https://github.com/SOLVE-IT-DF)** is a CASE/UCO-based knowledge base and extension framework for digital forensics investigation workflows. SOLVE-IT provides practical tools and examples for applying CASE/UCO to real forensic scenarios, and includes an extension framework ([SOLVE-IT-X](https://github.com/SOLVE-IT-DF/solve-it-x)) for building domain-specific additions.

**Domains covered:** digital forensics workflows, investigative knowledge management, educational materials.

### Adversary Engagement Ontology — Cyber Denial & Deception

**[Adversary Engagement Ontology (AEO)](https://github.com/UNHSAILLab/Adversary-Engagement-Ontology)** is a UCO sub-ontology for standardizing information representation in cyber adversary engagement operations. It extends UCO with classes for honeypots, breadcrumbs, decoys, lure objects, deception narratives, and adversary engagement objectives, drawing on concepts from MITRE ATT&CK and MITRE ENGAGE.

**Domains covered:** cyber deception, honeypots, adversary engagement operations, red/blue/purple team coordination, cyber threat intelligence.

### toolcap — Forensic Tool Capabilities (included in SDK)

The SDK ships with the **[toolcap extension](../extensions/toolcap/)** as a worked example of extension ontology authoring. It defines classes for comparing digital forensics tool capabilities across artifact types, operating systems, and file systems.

## Ontology Sources & Standards

The canonical upstream repositories and community resources.

| Resource | Description |
|----------|-------------|
| [UCO Ontology](https://github.com/ucoProject/UCO) | Unified Cyber Ontology — the foundation for all cyber domain ontologies |
| [CASE Ontology](https://github.com/casework/CASE) | Cyber-investigation Analysis Standard Expression — investigation-specific layer on UCO |
| [CASE Examples](https://github.com/casework/CASE-Examples) | Validated example data conforming to CASE/UCO |
| [CASE Profile Example](https://github.com/casework/CASE-Profile-Example) | Extension testing infrastructure and CI patterns |
| [CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing) | Requirements and process for submitting community extensions |
| [Cyber Domain Ontology (CDO)](https://cyberdomainontology.org/) | The Linux Foundation project that governs CASE and UCO |

## Adding Your Project

If your project extends CASE/UCO and you'd like it listed here, open a pull request or issue on the [SDK repository](https://github.com/vulnmaster/CASE-UCO-SDK).
