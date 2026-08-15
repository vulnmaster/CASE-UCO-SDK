"""ProfileCritic — reusable construction-time critique."""

from __future__ import annotations

from typing import Any

from case_uco.contracts.profile import ProfileContract
from case_uco.contracts.repair import RepairAction, suggest_repair
from case_uco.critique.findings import ConstructionFinding
from case_uco.critique.graph_pass import evaluate_graph_pass
from case_uco.critique.incremental import evaluate_incremental
from case_uco.critique.report import CritiqueReport
from case_uco.critique.signals import evaluate_validation_signals


class ProfileCritic:
    """Profile-aware construction critique. Offline. No MCP session."""

    def __init__(self, contract: ProfileContract) -> None:
        self.contract = contract
        self.findings: list[ConstructionFinding] = []

    def observe_add(
        self,
        graph: Any,
        *,
        host: str | None = None,
        node: Any = None,
        extra: dict[str, Any] | None = None,
        source: str | None = None,
    ) -> list[ConstructionFinding]:
        added = evaluate_incremental(
            self.contract, host=host, node=node, extra=extra, source=source
        )
        self.findings.extend(added)
        return added

    def evaluate(
        self,
        graph: Any,
        *,
        when: str = "graph",
        step_id: str | None = None,
        partition: str | None = None,
        run_heuristics: bool = True,
        run_signals: bool = True,
    ) -> CritiqueReport:
        collected: list[ConstructionFinding] = []
        executions: list[dict[str, Any]] = []
        if when == "incremental":
            collected.extend(self.findings)
        else:
            collected.extend(self.findings)
            collected.extend(evaluate_graph_pass(graph, self.contract, when=when))
            if when == "graph" and run_heuristics:
                try:
                    from case_uco.critique.heuristics import evaluate_heuristics
                except ImportError:
                    executions.append(
                        {"rule_id": "CRIT-H-INV-NO-OBJECT", "status": "skipped", "error_code": "rdflib_unavailable"}
                    )
                else:
                    heur, hexec = evaluate_heuristics(graph, self.contract.profile_id)
                    collected.extend(heur)
                    executions.extend(hexec)
        shacl = None
        coverage = None
        if when == "graph" and run_signals:
            sig, shacl, coverage, sexec = evaluate_validation_signals(graph, self.contract)
            collected.extend(sig)
            executions.extend(sexec)

        # Dedup by finding_id, last write wins for status.
        by_id: dict[str, ConstructionFinding] = {}
        for item in collected:
            by_id[item.finding_id] = item
        unique = list(by_id.values())
        blocking = sum(1 for item in unique if item.blocking and item.status != "resolved")
        estimated = 0
        try:
            estimated = int(graph.estimate_triples())
        except Exception:  # noqa: BLE001
            estimated = 0
        return CritiqueReport(
            schema_version="2.0.0",
            profile_id=self.contract.profile_id,
            when=when,
            step_id=step_id,
            partition=partition,
            findings=unique,
            rule_executions=executions,
            blocking_open=blocking,
            estimated_triples=estimated,
            shacl=shacl,
            coverage=coverage,
        )

    def suggest_repair(self, finding: ConstructionFinding | dict[str, Any]) -> RepairAction:
        return suggest_repair(finding)
