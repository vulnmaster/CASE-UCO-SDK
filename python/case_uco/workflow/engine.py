"""Investigation Workflow Engine — sequential, resumable, profile-bound."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from case_uco.builder import InvestigationBuilder
from case_uco.contracts import load_contract
from case_uco.graph import CASEGraph
from case_uco.workflow.definition import WorkflowDefinition, WorkflowStep, get_workflow, list_workflows
from case_uco.workflow.handlers import HANDLERS
from case_uco.workflow.state import atomic_write_json, default_state, load_state, utcnow


@dataclass
class WorkflowResult:
    status: str
    profile_id: str
    partitions: dict[str, CASEGraph]
    findings: list[dict[str, Any]]
    blocking_open: int
    validation: dict[str, Any] | None
    state_path: str


class InvestigationWorkflow:
    def __init__(
        self,
        workflow_id: str,
        *,
        profile_id: str | None = None,
        scenario: str = "",
        working_dir: str,
        kb_prefix: str = "http://example.org/kb/",
        inputs: dict[str, Any] | None = None,
        partition_policy: dict[str, Any] | None = None,
    ) -> None:
        definition = get_workflow(workflow_id)
        if definition is None:
            raise ValueError(f"Unknown workflow: {workflow_id}")
        if not definition.air_gapped:
            raise ValueError("Workflow must declare air_gapped=true")
        self.definition = definition
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.working_dir / "workflow-state.json"
        resolved_profile = profile_id or definition.profile
        contract = load_contract(resolved_profile)
        self.builder = InvestigationBuilder(scenario or definition.title, profile_id=resolved_profile, kb_prefix=kb_prefix)
        # Workflow-owned graphs merge on retry.
        self.builder.graph.on_duplicate = "merge_compatible"
        self.state = default_state(
            workflow_id=definition.id,
            workflow_version=definition.version,
            profile_id=resolved_profile,
            profile_version=contract.profile_version,
            scenario=scenario or definition.title,
            working_dir=self.working_dir,
            kb_prefix=kb_prefix,
            inputs=inputs or {},
        )
        if partition_policy:
            self.state["partition_policy"] = partition_policy
        self.state["status"] = "running"
        self.save()

    @classmethod
    def resume(cls, state_path: str) -> "InvestigationWorkflow":
        path = Path(state_path)
        if path.is_dir():
            path = path / "workflow-state.json"
        raw = load_state(path)
        obj = object.__new__(cls)
        definition = get_workflow(raw["workflow_id"])
        if definition is None:
            raise ValueError(f"Unknown workflow: {raw['workflow_id']}")
        obj.definition = definition
        obj.working_dir = Path(raw["working_dir"])
        obj.state_path = path
        obj.state = raw
        obj.builder = InvestigationBuilder(
            raw.get("scenario") or definition.title,
            profile_id=raw["profile_id"],
            kb_prefix=raw.get("kb_prefix") or "http://example.org/kb/",
        )
        obj.builder.graph.on_duplicate = "merge_compatible"
        graph_path = Path(raw["partitions"]["_default"]["graph_path"])
        if graph_path.is_file():
            obj.builder.graph.load_file(str(graph_path))
        # Crash recovery: running steps become ready (retry).
        running = list(obj.state["cursor"].get("running_steps") or [])
        obj.state["cursor"]["running_steps"] = []
        if running:
            obj.state["status"] = "running"
        return obj

    @property
    def graph(self) -> CASEGraph:
        return self.builder.graph

    def save(self) -> str:
        self.state["updated_at"] = utcnow()
        atomic_write_json(self.state_path, self.state)
        return str(self.state_path)

    def step(self, step_id: str | None = None) -> Any:
        ready = self._ready_steps()
        if step_id:
            match = next((s for s in self.definition.steps if s.id == step_id), None)
            if match is None:
                raise ValueError(f"Unknown step: {step_id}")
            if match.id not in {s.id for s in ready} and match.id not in self.state["cursor"]["completed_steps"]:
                raise ValueError(f"Step {step_id} dependencies not met")
            target = match
        else:
            if not ready:
                return self.builder.critique_report(when="graph")
            target = ready[0]
        return self._run_step(target)

    def run(self, *, until: str | None = None) -> WorkflowResult:
        self.state["status"] = "running"
        while True:
            ready = self._ready_steps()
            if not ready:
                break
            current = ready[0]
            try:
                self._run_step(current)
            except Exception as exc:  # noqa: BLE001
                self.state["cursor"]["failed_steps"].append(current.id)
                self.state["status"] = "failed"
                self.state["findings"].append(
                    {
                        "severity": "error",
                        "message": f"Handler failed: {exc}",
                        "path": current.id,
                        "rule_id": "WF-HANDLER-001",
                    }
                )
                self.save()
                return self.result()
            if until and current.id == until:
                break
        completed = set(self.state["cursor"]["completed_steps"])
        if all(s.id in completed or s.optional for s in self.definition.steps):
            blocking = sum(1 for f in self.state.get("findings") or [] if f.get("blocking") and f.get("severity") in {"error", "critical", "high"})
            self.state["status"] = "blocked" if blocking else "completed"
        self.save()
        return self.result()

    def critique(self, when: str = "graph"):
        return self.builder.critique_report(when=when)

    def result(self) -> WorkflowResult:
        findings = list(self.state.get("findings") or [])
        blocking = sum(1 for f in findings if f.get("blocking") and f.get("severity") in {"error", "critical", "high"})
        return WorkflowResult(
            status=self.state["status"],
            profile_id=self.state["profile_id"],
            partitions={"_default": self.builder.graph},
            findings=findings,
            blocking_open=blocking,
            validation=self.state.get("validation"),
            state_path=str(self.state_path),
        )

    def _ready_steps(self) -> list[WorkflowStep]:
        done = set(self.state["cursor"]["completed_steps"])
        failed = set(self.state["cursor"]["failed_steps"])
        ready: list[WorkflowStep] = []
        for step in self.definition.steps:
            if step.id in done or step.id in failed:
                continue
            if all(dep in done for dep in step.depends_on):
                ready.append(step)
        return ready

    def _run_step(self, step: WorkflowStep) -> Any:
        self.state["cursor"]["running_steps"] = [step.id]
        self.save()
        handler_name = step.handler or step.kind
        if step.kind == "load_profile":
            handler_name = "load_profile"
        if step.kind == "critique":
            handler_name = "critique_graph"
        func = HANDLERS.get(handler_name)
        if func is None and step.kind in HANDLERS:
            func = HANDLERS[step.kind]
        if func is None:
            raise ValueError(f"No handler for step {step.id} ({handler_name})")
        started = utcnow()
        try:
            payload = func(self, dict(step.args))
        except FileNotFoundError:
            if step.optional:
                payload = {"skipped": True}
            else:
                raise
        self.state["step_timings"][step.id] = {"started": started, "finished": utcnow()}
        if step.critique in {"step", "graph"} and step.kind not in {"critique", "validate"}:
            report = self.builder.critique_report(when="step" if step.critique == "step" else "graph")
            compat = [f.to_compat_dict() for f in report.findings]
            self.state["findings"] = compat
            if report.blocking_open and step.on_blocking == "stop":
                self.state["status"] = "blocked"
                self.state["cursor"]["running_steps"] = []
                self.state["cursor"]["completed_steps"].append(step.id)
                self.save()
                return report
        self.state["cursor"]["running_steps"] = []
        if step.id not in self.state["cursor"]["completed_steps"]:
            self.state["cursor"]["completed_steps"].append(step.id)
        # persist graph after each step so resume is possible
        graph_path = Path(self.state["partitions"]["_default"]["graph_path"])
        if len(self.builder.graph) > 0:
            graph_path.parent.mkdir(parents=True, exist_ok=True)
            self.builder.graph.write_streaming(str(graph_path))
        self.save()
        return payload


__all__ = ["InvestigationWorkflow", "WorkflowResult", "list_workflows", "get_workflow"]
