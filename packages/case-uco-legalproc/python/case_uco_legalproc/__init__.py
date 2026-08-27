"""Legal Process and Procedure Extension — CASE/UCO SDK extension bindings."""

__version__ = "0.3.0"

NAMESPACES: dict[str, str] = {
    "legalproc": "https://ontology.caseontology.org/case/criminal/",
}

# Public so the case_uco.extensions entry point (and static analysis)
# can reference it: the SDK registry loader resolves this at runtime.
REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")
