# Authoring and Improving Recipes

How to write a **new** recipe when an investigation pattern has no existing
recipe, and how to **improve an existing** recipe when a case exposes a gap
in one — including on the fly, mid-investigation, by an AI agent. Recipes
are the SDK's offline knowledge base: on closed systems running local
inference (Link-Look deployments), the recipe catalog is what lets the MCP
server grow with the investigator without internet access. The investigators
it serves are mostly not technical — the automation carries the modeling for
them — so the catalog is the system's accumulated judgment and must be
maintained like code: improved in place, validated before publication, and
grounded in the public ontology specifications so any graph built from it
can be shared with outside parties who can validate and use it with nothing
but public CASE/UCO/CAC releases, published extensions, and CDO profiles.

**When to use this recipe**

- `route_investigation_content` returned a weak match or extension-gap
  guidance, you completed the modeling anyway, and the pattern will recur
- `get_recipes(scenario)` returns nothing usable for a recurring evidence
  type or investigation pattern
- An existing recipe was wrong, incomplete, or required significant
  adaptation — improve it in place (see below) rather than leaving the next
  agent to rediscover the fix

**When NOT to write a new recipe**

- **Improve, don't duplicate.** If an existing recipe covers the pattern but
  is wrong, thin, or out of date, edit that recipe. A near-duplicate splits
  future routing between a good version and a stale one.
- **Compose, don't fork.** A multi-domain case (CAC + fraud + violent crime
  in one investigation) is a *composition* of existing recipes on one graph
  — see [cross-domain-extensions.md](cross-domain-extensions.md) — not a new
  recipe. Write a new recipe only when a pattern is missing, not when two
  existing patterns co-occur.
- **One-off quirks** belong in the case builder script's comments, not the
  catalog.
- If the gap is an *ontology* gap (missing class/property), follow
  [change-proposal.md](change-proposal.md) and
  [extensions.md](extensions.md) first; the recipe comes after the terms
  exist somewhere validatable.

## Improving an existing recipe

Treat a recipe like source code: when a live case proves it wrong or
incomplete, fix it at the source so every future routing benefits.

**Triggers for an improvement pass**

- A case following the recipe still failed `validate_graph` (SHACL or
  strict concept coverage) — the recipe taught an invalid pattern.
- The recipe's guidance was overridden for a good reason (e.g., a modeling
  decision this SDK later standardized, like the cyber vs. non-cyber
  evidence rule) — fold the decision into the recipe.
- A better ontology term now exists (new CASE/UCO release, newly bundled
  extension, newly profiled upper ontology) than the one the recipe uses.
- The recipe's anti-pattern list is missing a mistake an agent actually
  made while following it.
- Routing misses: the recipe applied to a case but `get_recipes` /
  `route_investigation_content` did not surface it — broaden its
  `RECIPE_INDEX` keywords or the router family keywords, not the recipe
  prose.

**Rules for editing**

1. **Never weaken grounding to make a case fit.** If the case does not fit
   the recipe's validated pattern, the fix is a better pattern (validated
   again) or an ontology change proposal — not softened language.
2. **Re-validate before publishing.** Any snippet you change must be
   re-copied from a graph that currently passes `validate_graph` /
   `case_validate`. Re-run the recipe's exemplar builder if one exists;
   update it in the same change if the pattern moved.
3. **Improve in place, preserving scope.** Do not silently broaden a
   recipe into a different domain; if the scope genuinely grows, update the
   title, INDEX.md row, and `RECIPE_INDEX` description/keywords together.
4. **Record why.** Add or update the recipe's provenance note (a short
   *"Validated against ..."* line naming the exemplar or case that drove
   the change), so later agents can weigh the guidance against its
   evidence.
5. **Keep the graph connected.** If the improvement makes the recipe
   relevant to new neighbors, update Related sections both ways.
6. **Run the catalog gates** (`make lint-recipes` and
   `python -m pytest mcp_server/tests`) — ontology grounding, index
   completeness, and cross-link guards must stay green.

The upstream loop still applies: when an improvement reveals that the
*ontology* is what's lacking, file it (`check_existing_proposals`,
`draft_change_proposal`) and note the pending proposal in the recipe rather
than inventing terms.

## Required structure

Model on [legal-process-modeling.md](legal-process-modeling.md) or a starter
kit ([starter-filesystem-report.md](starter-filesystem-report.md)):

1. **Title + one-paragraph scope** — what the recipe models, in plain terms.
2. **"When to use this recipe"** — bulleted trigger conditions an agent can
   match against submitted content; point to neighboring recipes for
   near-misses.
3. **Classes and properties table** — every class/extension involved, with
   the namespace prefix visible (`uco-observable:`, `legalproc:`, ...).
4. **Modeling pattern** — at least one complete JSON-LD (or Turtle) snippet
   per key decision, taken from a *validated* graph, never invented.
5. **Anti-patterns** — the mistakes this recipe exists to prevent (e.g.,
   typing physical evidence as observables; collapsing evidence and
   interpretation into one node).
6. **Checklist** — numbered, imperative steps an agent can execute.
7. **Validated exemplar** — a builder script or example graph under
   `examples/` that `validate_graph` / `case_validate` passes. A recipe
   without a conforming exemplar is a draft, not a recipe.
8. **Related section** — links to at least the recipes an agent would need
   before (ingestion, starter kits) and after (validation, extensions) this
   one. Recipes must be navigable as a graph, not a pile.

## Grounding rules (non-negotiable)

- Every term used in snippets must be declared in core CASE/UCO, a bundled
  extension (`extensions/*/manifest.json`), or a CDO-profiled upper
  ontology (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG) — strict
  concept coverage rejects anything else, and so should recipe review.
  Verify with `search_classes(term, scope='all')` and
  `get_uco_profiles(query)`. This is what makes the models *shareable*: a
  receiving party with no access to this deployment can validate the graph
  against the public ontology releases and the published extension files
  alone.
- Cyber vs. non-cyber: follow the rule in
  [legal-process-modeling.md](legal-process-modeling.md) — observables only
  for things that exist (fully or partially) in the cyber domain; other
  items are `uco-core:UcoObject` dual-typed via an upper-ontology profile.
- Source fidelity: no fabricated dates, quotes, serial numbers, or
  precision. Snippets carry `Source:` descriptions when they derive from
  real filings.
- Keep it jurisdiction- and tool-neutral where possible; put
  jurisdiction-specific detail in the exemplar, not the pattern.

### Repository-wide ontology-term lint

Run `make lint-recipes` before review. The gate checks every operational
`docs/recipes/*.md` file (except `INDEX.md`) and fails closed on:

- undeclared CURIEs and unknown namespace prefixes;
- a declared class used as a predicate or a declared property used as a class;
- class/property table entries that do not resolve to the vendored catalog;
- unprefixed or undeclared labels on canonical diagram edges; and
- literal `kindOfRelationship` / `kind_of_relationship` values absent from
  `mcp_server/relationship_kinds.json`.

The catalog is built from the role-aware strict-concept declaration loader,
every operational extension manifest in full mode, and exact terms from the
pinned upper-ontology registry. A namespace match alone does not authorize an
upper-ontology or extension term. Vendored Turtle files that depend on sibling
prefix declarations are retried only with the exact namespace closure in their
registered manifest; an unresolved parse error blocks the lint.

Exclusions are narrow and appear in the report. Wildcard notation such as
`solveit-data:techniqueDFT-*`, generic `kb:` instance IDs, and content under an
explicit **Anti-patterns** heading are classified automatically. For a bounded
example that intentionally uses a term being proposed, surround only that
example with a rationale:

````markdown
<!-- recipe-lint: ignore-start proposed-term -- This example is the term the companion proposal ontology declares. -->
```turtle
proposed:MyFacet a owl:Class ; rdfs:subClassOf uco-core:Facet .
```
<!-- recipe-lint: ignore-end proposed-term -->
````

Allowed directive classifications are `anti-pattern`, `controlled-literal`,
`instance-id`, and `proposed-term`. Directives require a rationale, cannot be
nested, and must have a matching `ignore-end`. Never use an exclusion to make
an operational ontology claim pass; correct the term or register the extension
instead. Candidate promotion runs this same lint before its executable
exemplar gate.

## Lifecycle: candidate → validated → operational (required)

Learned knowledge follows a staged promotion lifecycle so a mistaken
modeling decision, a poisoned source document, or a one-off case cannot
silently influence future investigations:

1. **Candidate** — draft new recipes in `docs/recipes/candidates/` (see the
   README there). Candidate recipes are invisible to `RECIPE_INDEX`,
   `INDEX.md`, and all routing tools. Extension ontologies drafted during
   an investigation carry `"status": "candidate"` in their `manifest.json`;
   routing ignores them, but the authoring investigation can still load them
   explicitly by name (`validate_graph(extensions=["myext"])`).
2. **Validated** — every embedded graph snippet conforms (`validate_graph`
   with zero undeclared concepts); catalog integrity tests pass.
3. **Operational** — a human reviews and intentionally promotes:
   - recipes: `make promote-recipe RECIPE=<slug> REVIEWER="..."` —
     transactionally moves the candidate into `docs/recipes/`, validates
     recipe structure (title, Scenario/Pattern/Validation sections, code
     fence, metadata block), registers it in `INDEX.md` and `RECIPE_INDEX`,
     and records provenance in `docs/recipes/promotion-log.json`. A
     structurally invalid candidate is rejected untouched.
   - extensions: `make promote-extension EXT=<name> REVIEWER="..."` — runs
     validation gates (manifest schema, ontology parse, class anchoring to
     declared parents, at least one conforming exemplar, failing negative
     fixtures when SHACL shapes ship, competency queries when declared) and
     records provenance (`promotion` block in the manifest, including git
     commit and deployment profile). A failed gate leaves the candidate
     untouched. Promotion authority follows the deployment profile:
     `offline-investigation` denies promotion; `production-review` requires
     a named reviewer.
4. **Deprecated / rolled back** — emergency revocation keeps provenance but
   removes the artifact from routing:
   - `make deprecate-extension EXT=<name> REASON="..."`;
   - `make deprecate-recipe RECIPE=<slug> REASON="..."` — moves the recipe
     back to `docs/recipes/candidates/` and removes its index entries;
   - one-command rollback to a previous approved generation:
     `make rollback-extension EXT=<name> REF=<tag-or-commit>` (git-based —
     all knowledge artifacts are version-controlled files). Recipes roll
     back with `git checkout <ref> -- docs/recipes/<file>.md`.

`make lifecycle-status` lists every extension's lifecycle state. Offline
Link-Look deployments follow the same flow against their local clone; the
promotion gates run entirely offline (`case_validate` + rdflib).

## Registering the recipe (required — an unregistered recipe is invisible)

The MCP server routes agents by index, so a new file alone does nothing.
`make promote-recipe` performs steps 1–3 automatically for candidates; when
authoring a recipe directly (not via the candidate lifecycle) do them by
hand:

1. Save as `docs/recipes/<kebab-case-slug>.md` (promote out of
   `docs/recipes/candidates/` only after validation).
2. Add a row to the appropriate section of `docs/recipes/INDEX.md`.
3. Add an entry to `RECIPE_INDEX` in `mcp_server/domain_index.py` — title,
   one-sentence description, and generous `keywords` (this is what
   `get_recipe` / `get_recipes` match against).
4. If the recipe anchors a *new investigation family* (not just a new
   evidence type), add or extend an `InvestigationFamily` in
   `mcp_server/investigation_router.py` — keywords, recipes, extensions,
   namespaces, upper profiles. For CAC domains, extend the CAC router's
   domain table instead.
5. If it maps a new evidence *source* (a report format, an export type),
   also add a `MAPPING_GUIDE_INDEX` entry in `domain_index.py` so
   `guide_mapping` finds it.
6. Run the MCP test suite (`python -m pytest mcp_server/tests`) — index
   completeness tests fail if a recipe file and the indexes disagree.

## Checklist

1. Confirm no existing recipe covers the pattern: `get_recipes(scenario)`
   with several phrasings, then skim `docs/recipes/INDEX.md`.
2. Confirm term coverage (`search_classes`, `get_uco_profiles`); if terms
   are missing, detour to change-proposal + extension recipes first.
3. Build and validate the exemplar graph (`Conforms: True`, zero
   undeclared concepts).
4. Write the recipe following the structure above, snippets copied from the
   validated exemplar.
5. Cross-reference: add Related links out, and add a link *to* the new
   recipe from its nearest neighbors.
6. Register in `INDEX.md` + `RECIPE_INDEX` (+ router family or mapping
   guide when applicable); run the tests.

## Related

- [change-proposal.md](change-proposal.md) — when the gap is in the ontology, not the catalog
- [extensions.md](extensions.md) — local extension ontologies and strict concept coverage
- [cross-domain-extensions.md](cross-domain-extensions.md) — composing multiple domains in one graph instead of forking recipes
- [legal-process-modeling.md](legal-process-modeling.md) — a worked example of a recipe created from a live case (Perry/O'Dell)
- [starter-filesystem-report.md](starter-filesystem-report.md) — the starter-kit structure to imitate
