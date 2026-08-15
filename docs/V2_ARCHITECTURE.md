# CASE-UCO-SDK v2 — Construction Re-Architecture (landed)

**Generation:** 2.0.0 (recommended-path major; public constructors were not deleted)  
**Branch:** `feature/v2-capability-defining-rearchitecture`  
**Design (Phase 0):** [`docs/design/v2-construction-rearchitecture.md`](design/v2-construction-rearchitecture.md)

## Center of gravity

v1.23 optimized **representation and discovery** (Composition Profiles, incremental generate, InvestigationBuilder, hash indexes). v2.0 optimizes **correct, guided, scalable construction** under operational pressure.

| Layer | Landed type | Role |
|---|---|---|
| Profile Contracts | `case_uco.contracts.load_contract` | Evaluable checks synthesized from `facet_sets` + `topology/contracts/default-bindings.json` |
| Continuous critique | `case_uco.critique.ProfileCritic` | Incremental / step / graph. In the wheel. MCP critic remains acceptance. |
| Workflow Engine | `case_uco.workflow.InvestigationWorkflow` | **Recommended primary path.** Resumable `workflow-state.json`. |
| Partition-native large cases | `partition_by_profile(..., strategy=)` + `field-triage-partitioned` | Worklist split by `boundary_key` before heavy build |
| Trajectories | `case_uco.trajectories` | JSON over existing OWL (`hasPhase`, `InvestigativeAction`). No new terms. |
| Interop adapters | `case_uco.adapters` | Offline VICS / PhotoDNA / hash-match. No sockets. |

Power users keep `CASEGraph.create`, generated Facet classes, and `InvestigationBuilder`.

## Recommended construction path

```python
from case_uco.workflow import InvestigationWorkflow

wf = InvestigationWorkflow(
    "hash-intelligence-vics",
    profile_id="HashIntelligence",
    scenario="Local VICS export + lab PhotoDNA list",
    working_dir="./run",
    inputs={"hash_list": "./hashes.json"},
)
result = wf.run()
if result.status != "completed":
    for finding in result.findings:
        print(finding.get("rule_id"), finding.get("message"), finding.get("repair"))
```

CLI: `case-uco-workflow start field-triage --dir ./run --input hash_list=./hashes.json --scenario "seized laptop"`

Mid-level (unchanged call shape, richer critique):

```python
from case_uco import InvestigationBuilder

b = InvestigationBuilder("CyberTip CSAM hashing", profile_id="HashIntelligence")
b.add_csam_evidence("img.jpg", hashes=[("SHA256", "…"), ("PhotoDNA", "…")])
print(b.critique())                 # still severity / message / path
print(b.critique_report().blocking_open)
```

## Migration

1. Keep calling `InvestigationBuilder` / helpers — they still work.
2. Optionally call `builder.critique_report()` for contract findings.
3. For multi-step / large / ICAC cases, switch to `InvestigationWorkflow` or `case-uco-workflow`.
4. Agents: prefer `start_investigation_workflow` over an empty `build_investigation`. `build_investigation(..., evidence=)` is additive.

`2.0.0` is a **recommended-path major**, not a deleted-API major. Full C#/Java/Rust runners are **2.1**; 2.0 ships the logical surface (`ProfileContract`, `InvestigationWorkflow` step/state, additive `CritiqueFinding` fields).

## Air-gap and ontology constraints

- Investigation-time modules do not open sockets. Adapters refuse `http:` / `https:`.
- Profiles, workflows, trajectories, and mappings are vendored under `python/case_uco/topology/data/` and listed in `pyproject.toml` package-data.
- Generator remains the source of truth for typed classes.
- No core OWL terms were invented. PhotoDNA remains extra `Hash` + action. `ConditioningPhase` generate-lag is `PROF-TRAJ-NOT-GENERATED`, not a change-proposal gap.
- SHACL still goes through `case_validate`. Missing validator → `skipped` / `validator_unavailable`, never `conforms=True`.

## Intentional interface changes

| Change | Breaking? |
|---|---|
| Recommended primary path is the workflow engine | Recommended-path only |
| `critique()` dicts gain keys | No (`severity`/`message`/`path` frozen for original three rules) |
| `partition_by_profile` / `lookup_hash` extra kwargs | No |
| C#/Java/Rust CAC prefix no longer injected for HashIntelligence | Tiny fix; use FullCACLifecycle or extra_context when CAC types are emitted |
| New packages `contracts`, `critique`, `workflow`, `adapters`, `trajectories` | No |
