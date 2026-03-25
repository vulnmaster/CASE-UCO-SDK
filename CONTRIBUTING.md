# Contributing to CASE/UCO Standard Libraries

Thank you for your interest in contributing! This project provides auto-generated builder libraries for the CASE/UCO ontology across Python, C#, Java, and Rust.

## Getting Started

```bash
git clone --recurse-submodules https://github.com/vulnmaster/CASE-UCO-SDK.git
cd CASE-UCO-SDK
make init
make generate
make test
```

## Project Structure

- **`generator/`** — The code generator (Python). Changes here affect all four language outputs.
- **`python/`, `csharp/`, `java/`, `rust/`** — Generated libraries. Files under `uco/` and `case/` subdirectories are **auto-generated** and should not be hand-edited.
- **Hand-maintained runtime files:**
  - `python/case_uco/graph.py`
  - `csharp/CaseUco/CaseGraph.cs`, `JsonLdPropertyAttribute.cs`, `ReferenceEqualityComparer.cs`
  - `java/src/main/java/org/caseontology/CaseGraph.java`
  - `rust/src/graph.rs`
- **`ontology/`** — Git submodules for upstream UCO and CASE ontologies.
- **`extensions/`** — Optional ontology extensions (e.g., `toolcap` for forensic tool capabilities).

## How to Contribute

### Reporting Issues

Open a GitHub issue describing:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Which language library is affected (if applicable)

### Submitting Changes

1. Fork the repository and create a feature branch from `main`.
2. Make your changes. If modifying the generator, regenerate and test all four languages.
3. Run the full test suite: `make test`
4. Ensure CI passes (all four language builds + CodeQL scanning).
5. Open a pull request with a clear description of the change.

### Generator Changes

If your change modifies how code is generated:

1. Edit files under `generator/src/case_uco_generator/`.
2. Regenerate: `python -m case_uco_generator generate --lang all`
3. Run all tests: `make test`
4. Commit both the generator change and the regenerated output.

### Adding a New Ontology Extension

1. Create a directory under `extensions/` with:
   - A Turtle (`.ttl`) file defining your OWL+SHACL extension
   - A working example script
   - A `README.md` documenting the extension
2. Follow the pattern in `extensions/toolcap/` for reference.

## Code Style

- **Python**: Follow PEP 8. No unnecessary imports in generated code.
- **C#**: Follow standard .NET naming conventions (PascalCase).
- **Java**: Follow standard Java conventions (camelCase fields, PascalCase classes).
- **Rust**: Follow standard Rust conventions (snake_case, `rustfmt`).

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.
