"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — CASE/UCO SDK extension bindings."""

__version__ = "0.2.0"

NAMESPACES: dict[str, str] = {
    "solveit-analysis": "https://ontology.solveit-df.org/solveit/analysis/",
    "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
    "solveit-data": "https://ontology.solveit-df.org/solveit/data/",
    "solveit-observable": "https://ontology.solveit-df.org/solveit/observable/",
    "solveit-sqlite": "https://ontology.solveit-df.org/solveit/sqlite/",
    "solveit-tool-profile": "https://ontology.solveit-df.org/solveit/tool-profile/",
    "solveit-wa": "https://ontology.solveit-df.org/solveit/weakness-assessment/",
}

# Public so the case_uco.extensions entry point (and static analysis)
# can reference it: the SDK registry loader resolves this at runtime.
REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")
