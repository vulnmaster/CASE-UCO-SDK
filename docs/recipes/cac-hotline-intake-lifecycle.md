# Hotline Intake and Referral Lifecycle

> See [Recipe Index](INDEX.md) for all recipes.

Model hotline intake, triage, referral, and escalation from first report through law-enforcement handoff using CAC hotline module classes.

## Scope

**Layer 3 — Institutional workflow** for report intake organizations and referral chains.

## Key classes

| Class | Role |
|---|---|
| `cacontology-hotlines:HotlineReport` | Initial report received by a hotline |
| `cacontology-hotlines:ReportReviewAction` | Triage and urgency review |
| `cacontology-hotlines:ForwardToLEAction` | Referral to a law-enforcement agency |
| `cacontology-recruitment-networks:MandatoryReportingActivation` | Mandated-reporter trigger when that separate module applies |
| `CACInvestigation` | Investigation opened from referral |
| `InvestigativeAction` | Each intake workflow step |

## Canonical pattern

```
cacontology-hotlines:HotlineReport
  ◀── uco-action:object ── cacontology-hotlines:ReportReviewAction
        └── uco-action:result ──▶ cacontology-hotlines:ForwardToLEAction
              ├── uco-action:result ──▶ CACInvestigation
              └── Related_To ──▶ MandatoryReportingActivation (only if sourced)
```

## Modeling rules

- Model **each intake stage** as its own `InvestigativeAction` with explicit `uco-action:result` links.
- Do not collapse triage and referral into one node — urgency and routing are queryable only when separated.
- When the intake leads to NCMEC, chain into [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-hotlines": "https://cacontology.projectvic.org/hotlines#",
})
report = graph.add_node("kb:report-1", "cacontology-hotlines:HotlineReport", {
    "uco-core:name": "CyberTipline report",
})
review = graph.add_node("kb:review-1", "cacontology-hotlines:ReportReviewAction", {
    "uco-core:name": "Hotline triage review",
    "uco-action:object": {"@id": "kb:report-1"},
})
graph.write("hotline-intake.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=hotline-intake.jsonld
```

## Related recipes

- [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md)
- [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md)
