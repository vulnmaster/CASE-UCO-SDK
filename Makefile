.PHONY: all generate build test clean init lint smoke check venv \
       test-proposal validate-proposal sparql-test-proposal \
       test-extension-compat test-extension-main test-extension-develop test-extension-develop2 \
       playground-test test-docs sync-solveit sync-solveit-offline \
       sync-attack sync-attack-offline \
       rebuild-upper-registry sync-upper sync-upstream \
       topology-baseline test-topology

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Resolve an extension name to its vendoring root (v1.19.0): SDK-native
# extensions live in extensions/, upstream-vendored ontologies (cac, aeo,
# solveit) in ontology/. Mirrors mcp_server/extension_paths.py search order.
EXT_DIR = $(shell if [ -f extensions/$(EXT)/manifest.json ] || [ -d extensions/$(EXT) ]; then echo extensions/$(EXT); elif [ -f ontology/$(EXT)/manifest.json ]; then echo ontology/$(EXT); else echo extensions/$(EXT); fi)

all: init generate build test

venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

init: venv
	git submodule update --init --recursive
	$(PIP) install -e generator/
	$(PIP) install -e python/

generate:
	$(PYTHON) -m case_uco_generator generate --lang all

build: build-python build-csharp build-java build-rust

build-python:
	$(PIP) install -e python/

build-csharp:
	cd csharp && dotnet build

build-java:
	cd java && mvn package -q

build-rust:
	cd rust && cargo build

test: test-generator test-python test-csharp test-java test-rust test-topology

test-generator:
	PYTHONPATH=generator/src $(PYTHON) -m pytest generator/tests/ -v

test-python:
	cd python && $(abspath $(PYTHON)) -m pytest tests/ -v

test-csharp:
	cd csharp && dotnet test

test-java:
	cd java && mvn test -q

test-rust:
	cd rust && cargo test

test-docs:
	$(PYTHON) scripts/test_doc_snippets.py

test-mcp:
	$(PYTHON) -m pytest mcp_server/tests/ -v

# --- Knowledge artifact lifecycle (mcp_server/knowledge_lifecycle.py) ------
# Promote a candidate extension to operational after validation gates pass:
#   make promote-extension EXT=myext REVIEWER="Jane Analyst"
promote-extension:
	$(PYTHON) mcp_server/knowledge_lifecycle.py promote $(EXT) --reviewed-by "$(REVIEWER)"

# Emergency revocation of a bad extension (kept on disk with provenance):
#   make deprecate-extension EXT=myext REASON="modeling error in facet X"
deprecate-extension:
	$(PYTHON) mcp_server/knowledge_lifecycle.py deprecate $(EXT) --reason "$(REASON)"

# One-command rollback to a previously approved knowledge generation:
#   make rollback-extension EXT=myext REF=v1.15.0
rollback-extension:
	git checkout $(REF) -- $(EXT_DIR)
	@echo "Restored $(EXT_DIR) from $(REF); review and commit the rollback."

lifecycle-status:
	$(PYTHON) mcp_server/knowledge_lifecycle.py status

# Promote a candidate recipe into the operational catalog (moves the file,
# registers it in INDEX.md + RECIPE_INDEX, records provenance):
#   make promote-recipe SLUG=my-recipe DESCRIPTION="..." KEYWORDS="..." REVIEWER="Jane Analyst"
promote-recipe:
	$(PYTHON) mcp_server/knowledge_lifecycle.py promote-recipe $(SLUG) \
		--description "$(DESCRIPTION)" --keywords "$(KEYWORDS)" --reviewed-by "$(REVIEWER)"

# Revoke an operational recipe back to candidates/ (unregisters both indexes):
#   make deprecate-recipe SLUG=my-recipe REASON="taught an invalid pattern"
deprecate-recipe:
	$(PYTHON) mcp_server/knowledge_lifecycle.py deprecate-recipe $(SLUG) --reason "$(REASON)"

# Re-vendor the pinned SOLVE-IT snapshot (ontology + compiled knowledge
# base) and regenerate the punned technique catalog:
#   make sync-solveit                # pin current upstream main
#   make sync-solveit REF=<sha>      # pin a specific solve-it-ontology ref
sync-solveit:
	PYTHONPATH=python:mcp_server $(PYTHON) mcp_server/tools/sync_solveit.py --ontology-ref $(or $(REF),main)

# Regenerate the SOLVE-IT technique catalog + provenance from the
# already-vendored files (offline):
sync-solveit-offline:
	PYTHONPATH=python:mcp_server $(PYTHON) mcp_server/tools/sync_solveit.py --skip-fetch

# Refresh the pinned MITRE ATT&CK catalog labels/comments from STIX 2.1
# (partial membership: current catalog ∪ exemplar citations):
#   make sync-attack                        # ATT&CK v19.1 (or manifest pin)
#   make sync-attack ATTACK_VERSION=19.1
sync-attack:
	$(PYTHON) mcp_server/tools/sync_attack_catalog.py \
		--attack-version $(or $(ATTACK_VERSION),19.1) \
		--keep-existing --from-exemplars

# Regenerate the ATT&CK catalog from a local enterprise-attack STIX file:
#   make sync-attack-offline STIX=/path/to/enterprise-attack-19.1.json
sync-attack-offline:
	$(PYTHON) mcp_server/tools/sync_attack_catalog.py \
		--stix-file $(STIX) --keep-existing --from-exemplars

# Rebuild the strict upper-ontology term registry from the vendored
# snapshot in ontology/upper/ (offline; no network needed):
rebuild-upper-registry:
	$(PYTHON) mcp_server/tools/build_upper_ontology_registry.py

# Refresh the vendored upper-ontology snapshot from upstream, then
# rebuild the registry (network required):
sync-upper:
	$(PYTHON) mcp_server/tools/build_upper_ontology_registry.py --fetch

# Refresh every vendored upstream source: CASE + UCO submodules, CAC and
# AEO submodules, the SOLVE-IT snapshot, and the upper-ontology snapshot.
#   make sync-upstream
sync-upstream:
	git submodule update --remote --checkout ontology/UCO ontology/CASE \
		ontology/cac/ontology ontology/aeo/ontology
	$(MAKE) sync-solveit
	$(MAKE) sync-attack
	$(MAKE) sync-upper
	@echo "All upstream snapshots refreshed; review diffs, run 'make test-mcp', and commit."

# Held-out routing evaluation (issue #58) — runs separately from unit tests:
#   make eval-routing
eval-routing:
	$(PYTHON) evaluation/routing/run_evaluation.py \
		--corpus evaluation/routing/heldout-corpus-v1.json \
		--report evaluation/routing/report.json

lint: typecheck-python lint-csharp lint-java lint-rust

typecheck-python:
	cd python && $(abspath $(PYTHON)) -m mypy case_uco/ --ignore-missing-imports

lint-csharp:
	cd csharp && dotnet build --no-restore /p:TreatWarningsAsErrors=true

lint-java:
	cd java && mvn compile -q

lint-rust:
	cd rust && cargo clippy -- -D warnings

smoke: smoke-csharp smoke-java smoke-rust

smoke-csharp:
	cd csharp && dotnet run --project CaseUco.Smoke

smoke-java:
	cd java && mvn -q compile exec:java

smoke-rust:
	cd rust && cargo run --example smoke

# Topology baseline (stdlib only; offline). Regenerates topology/*.json + *.md
# from vendored Turtle, registries, recipes, and domain_index.py.
topology-baseline:
	$(PYTHON) topology/scripts/build_baseline.py

test-topology:
	PYTHONPATH=topology $(PYTHON) -m pytest topology/tests/ -v

check: generate build test lint smoke

clean:
	rm -rf python/case_uco/uco/*.py python/case_uco/case/*.py
	rm -rf csharp/CaseUco/Uco/*.cs csharp/CaseUco/Case/*.cs
	find java/src/main/java/org/caseontology -name "*.java" -not -name "CaseGraph.java" -not -name "SmokeTest.java" -delete
	rm -rf rust/src/uco/*.rs rust/src/case/*.rs

clean-venv:
	rm -rf $(VENV)

# ---------------------------------------------------------------------------
# Change proposal testing
# ---------------------------------------------------------------------------
# Usage:
#   make test-proposal PROPOSAL=cryptocurrency-address-and-sanctions-designation
#
# Expects:
#   change_proposals/<PROPOSAL>.md          — the proposal markdown
#   change_proposals/<PROPOSAL>.jsonld      — example instance data (JSON-LD)
#   change_proposals/<PROPOSAL>.sparql      — SPARQL queries (optional, one per file or multi-query)
#   change_proposals/<PROPOSAL>.ttl         — extension ontology (optional, for validation)
#   change_proposals/<PROPOSAL>-shapes.ttl  — SHACL shapes (optional, for validation)

PROPOSAL ?= example
PROPOSAL_DIR := change_proposals
PROPOSAL_JSONLD := $(PROPOSAL_DIR)/$(PROPOSAL).jsonld
PROPOSAL_SPARQL := $(PROPOSAL_DIR)/$(PROPOSAL).sparql
PROPOSAL_TTL := $(PROPOSAL_DIR)/$(PROPOSAL).ttl
PROPOSAL_SHAPES := $(PROPOSAL_DIR)/$(PROPOSAL)-shapes.ttl

validate-proposal:
	@echo "=== Validating proposal graph: $(PROPOSAL_JSONLD) ==="
	@if [ -f "$(PROPOSAL_JSONLD)" ]; then \
		VALIDATE_ARGS="--built-version case-1.4.0 --inference rdfs --allow-info"; \
		if [ -f "$(PROPOSAL_TTL)" ]; then \
			VALIDATE_ARGS="$$VALIDATE_ARGS --ontology-graph $(PROPOSAL_TTL)"; \
		fi; \
		if [ -f "$(PROPOSAL_SHAPES)" ]; then \
			VALIDATE_ARGS="$$VALIDATE_ARGS --ontology-graph $(PROPOSAL_SHAPES)"; \
		fi; \
		$(VENV)/bin/case_validate $$VALIDATE_ARGS $(PROPOSAL_JSONLD); \
	else \
		echo "No .jsonld file found at $(PROPOSAL_JSONLD) — skipping validation"; \
	fi

sparql-test-proposal:
	@echo "=== Testing SPARQL queries for proposal: $(PROPOSAL) ==="
	@if [ -f "$(PROPOSAL_SPARQL)" ] && [ -f "$(PROPOSAL_JSONLD)" ]; then \
		$(PYTHON) scripts/sparql_test.py $(PROPOSAL_JSONLD) $(PROPOSAL_SPARQL); \
	else \
		echo "No .sparql or .jsonld file found for proposal $(PROPOSAL) — skipping SPARQL tests"; \
	fi

test-proposal: validate-proposal sparql-test-proposal
	@echo ""
	@echo "=== Proposal testing complete for: $(PROPOSAL) ==="

# ---------------------------------------------------------------------------
# Extension compatibility testing
# ---------------------------------------------------------------------------
# Tests extension ontologies against multiple CASE/UCO branches to help
# ontologists review change proposals.
#
# Usage:
#   make test-extension-compat EXT_TTL=extensions/toolcap/toolcap.ttl EXT_SHAPES=extensions/toolcap/toolcap-shapes.ttl EXT_DATA=extensions/toolcap/toolcap-exemplar.ttl
#
# Runs validation against:
#   - CASE/UCO main branch (current stable release, 1.5.0)
#   - CASE/UCO develop branch (next backward-compatible release)
#   - CASE/UCO develop-2.0.0 branch (targeting v2.0.0)
#
# The checked-out branch supplies the ontology closure directly via
# --built-version none plus every module .ttl, rather than case-utils'
# bundled monolith. case-utils pins its newest bundle at CASE 1.4.0, so
# --built-version would silently validate all three branches against the
# same stale closure and report identical results. The per-module
# enumeration is required because ontology/*/master/*.ttl are owl:imports
# stubs (~23 triples) that carry no class or shape definitions.

EXT_TTL ?= extensions/toolcap/toolcap.ttl
EXT_SHAPES ?= extensions/toolcap/toolcap-shapes.ttl
EXT_DATA ?= extensions/toolcap/toolcap-exemplar.ttl
UCO_REPO := ontology/UCO
CASE_REPO := ontology/CASE

define test_extension_branch
	@echo ""
	@echo "=== Testing extension against $(1) branch ==="
	@CURRENT_UCO=$$(cd $(UCO_REPO) && git rev-parse HEAD); \
	CURRENT_CASE=$$(cd $(CASE_REPO) && git rev-parse HEAD); \
	cd $(UCO_REPO) && git fetch origin $(1) 2>/dev/null && git checkout FETCH_HEAD --quiet 2>/dev/null; \
	cd ../../$(CASE_REPO) && git fetch origin $(1) 2>/dev/null && git checkout FETCH_HEAD --quiet 2>/dev/null; \
	cd ../..; \
	echo "UCO branch: $(1) ($$(cd $(UCO_REPO) && git rev-parse --short HEAD))"; \
	echo "CASE branch: $(1) ($$(cd $(CASE_REPO) && git rev-parse --short HEAD))"; \
	VALIDATE_ARGS="--built-version none"; \
	for f in $(UCO_REPO)/ontology/*/*.ttl $(UCO_REPO)/ontology/uco/*/*.ttl $(CASE_REPO)/ontology/*/*.ttl; do \
		case "$$f" in */master/*) continue;; esac; \
		[ -f "$$f" ] && VALIDATE_ARGS="$$VALIDATE_ARGS --ontology-graph $$f"; \
	done; \
	if [ -f "$(EXT_TTL)" ]; then VALIDATE_ARGS="$$VALIDATE_ARGS --ontology-graph $(EXT_TTL)"; fi; \
	if [ -f "$(EXT_SHAPES)" ]; then VALIDATE_ARGS="$$VALIDATE_ARGS --ontology-graph $(EXT_SHAPES)"; fi; \
	if [ -f "$(EXT_DATA)" ]; then \
		$(VENV)/bin/case_validate $$VALIDATE_ARGS --inference rdfs --allow-info $(EXT_DATA) && \
		echo "  Result: PASS" || echo "  Result: FAIL"; \
	else \
		echo "  No exemplar data file found at $(EXT_DATA) — skipping"; \
	fi; \
	cd $(UCO_REPO) && git checkout $$CURRENT_UCO --quiet 2>/dev/null; \
	cd ../../$(CASE_REPO) && git checkout $$CURRENT_CASE --quiet 2>/dev/null
endef

test-extension-main:
	$(call test_extension_branch,main)

test-extension-develop:
	$(call test_extension_branch,develop)

test-extension-develop2:
	$(call test_extension_branch,develop-2.0.0)

test-extension-compat: test-extension-main test-extension-develop test-extension-develop2
	@echo ""
	@echo "=== Extension compatibility testing complete ==="
	@echo "Tested: $(EXT_TTL)"
	@echo "Against: main (v1.5.0), develop, develop-2.0.0 (v2.0.0)"

# ---------------------------------------------------------------------------
# CDO Community Playground testing
# ---------------------------------------------------------------------------
# Usage: make playground-test EXT_OWL=path/to/ext.ttl EXT_SHAPES=path/to/ext-shapes.ttl
#
# Clones CASE-Profile-Example, injects the extension ontology and shapes,
# then runs `make -j check` per the CDO Community Playground Guide.

PLAYGROUND_DIR := .playground-test
EXT_OWL ?=
EXT_SHAPES ?=

playground-test:
ifndef EXT_OWL
	$(error EXT_OWL is required. Usage: make playground-test EXT_OWL=path/to/ext.ttl EXT_SHAPES=path/to/ext-shapes.ttl)
endif
	@echo "=== CDO Community Playground Testing ==="
	@echo "Extension OWL:    $(EXT_OWL)"
	@echo "Extension SHAPES: $(EXT_SHAPES)"
	@echo ""
	@rm -rf $(PLAYGROUND_DIR)
	git clone --quiet https://github.com/casework/CASE-Profile-Example $(PLAYGROUND_DIR)
	@echo "--- Injecting extension ontology ---"
	cp $(EXT_OWL) $(PLAYGROUND_DIR)/ontology/case-example.ttl
	@if [ -n "$(EXT_SHAPES)" ] && [ -f "$(EXT_SHAPES)" ]; then \
		echo "--- Injecting SHACL shapes ---"; \
		cp $(EXT_SHAPES) $(PLAYGROUND_DIR)/shapes/sh-case-example.ttl; \
	fi
	@echo "--- Running make -j check ---"
	cd $(PLAYGROUND_DIR) && make -j check
	@echo ""
	@echo "=== Playground testing PASSED ==="
	@echo "Your extension is ready for CDO Community Playground submission."
	@echo "Place it in a public GitHub repo and notify the Ontology Committee."
	@rm -rf $(PLAYGROUND_DIR)

# ---------------------------------------------------------------------------
# Per-extension validation and generation (manifest-driven)
# ---------------------------------------------------------------------------
# Usage:
#   make validate-extension EXT=cac DATA=path/to/data.jsonld
#   make test-ext-cac
#   make test-ext-aeo
#   make generate-ext EXT=cac

EXT ?= cac
DATA ?=

validate-extension:
ifndef DATA
	$(error DATA is required. Usage: make validate-extension EXT=$(EXT) DATA=path/to/data.jsonld)
endif
	$(VENV)/bin/python scripts/validate_extension.py $(EXT_DIR)/manifest.json $(DATA)

test-ext-cac:
	$(MAKE) test-extension-compat \
	  EXT_TTL=ontology/cac/ontology/ontology/cacontology-core-spine.ttl \
	  EXT_SHAPES=ontology/cac/ontology/ontology/cacontology-core-spine-shapes.ttl \
	  EXT_DATA=ontology/cac/ontology/ontology/cacontology-core-spine-shapes.ttl

test-ext-aeo:
	$(MAKE) test-extension-compat \
	  EXT_TTL=ontology/aeo/ontology/ontology/engagement/engagement.ttl \
	  EXT_SHAPES=ontology/aeo/ontology/ontology/engagement/engagement.ttl \
	  EXT_DATA=ontology/aeo/ontology/ontology/engagement/engagement.ttl

generate-ext:
	$(VENV)/bin/case-uco-generate generate-extension \
	  --extension $(EXT_DIR)/ \
	  --output-dir packages/case-uco-$(EXT)/ \
	  --lang all
