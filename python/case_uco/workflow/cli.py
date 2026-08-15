"""case-uco-workflow — air-gapped investigation construction CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from case_uco.workflow import InvestigationWorkflow, get_workflow, list_workflows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="case-uco-workflow")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list", help="List investigation workflows")
    sub.add_parser("trajectories", help="List vendored trajectory contracts")
    sub.add_parser("adapters", help="List offline interop adapters")
    show = sub.add_parser("show", help="Show one workflow definition")
    show.add_argument("workflow_id")
    start = sub.add_parser("start", help="Start a workflow run")
    start.add_argument("workflow_id")
    start.add_argument("--profile")
    start.add_argument("--scenario", default="")
    start.add_argument("--dir", required=True)
    start.add_argument("--input", action="append", default=[], help="name=path")
    step = sub.add_parser("step", help="Run the next ready step")
    step.add_argument("--dir", required=True)
    run = sub.add_parser("run", help="Run until blocked or complete")
    run.add_argument("--dir", required=True)
    critique = sub.add_parser("critique", help="Graph-wide critique")
    critique.add_argument("--dir", required=True)
    resume = sub.add_parser("resume", help="Resume from state")
    resume.add_argument("--dir", required=True)
    args = parser.parse_args(argv)
    if args.command == "list":
        for item in list_workflows():
            print(f"{item.id:28s}  {item.profile:22s}  {item.title}")
        return 0
    if args.command == "trajectories":
        from case_uco.trajectories import list_trajectories

        for item in list_trajectories():
            print(f"{item.id:28s}  {item.title}")
        return 0
    if args.command == "adapters":
        from case_uco.adapters import list_adapters

        for item in list_adapters():
            print(f"{item['id']:28s}  {','.join(item['profile_ids'])}")
        return 0
    if args.command == "show":
        item = get_workflow(args.workflow_id)
        if item is None:
            print(f"Unknown workflow {args.workflow_id}", file=sys.stderr)
            return 1
        print(json.dumps({
            "id": item.id,
            "profile": item.profile,
            "steps": [s.id for s in item.steps],
            "inputs": list(item.inputs),
        }, indent=2))
        return 0
    if args.command == "start":
        inputs = _parse_inputs(args.input)
        wf = InvestigationWorkflow(
            args.workflow_id,
            profile_id=args.profile,
            scenario=args.scenario,
            working_dir=args.dir,
            inputs=inputs,
        )
        result = wf.run()
        print(json.dumps({"status": result.status, "state": result.state_path, "findings": len(result.findings)}, indent=2))
        return 0 if result.status in {"completed", "blocked"} else 1
    if args.command in {"step", "run", "critique", "resume"}:
        wf = InvestigationWorkflow.resume(args.dir)
        if args.command == "step":
            wf.step()
            print(json.dumps({"status": wf.state["status"], "completed": wf.state["cursor"]["completed_steps"]}))
            return 0
        if args.command == "run" or args.command == "resume":
            result = wf.run()
            print(json.dumps({"status": result.status, "findings": len(result.findings)}))
            return 0 if result.status != "failed" else 1
        report = wf.critique()
        print(json.dumps(report.to_dict(), indent=2, default=str))
        return 0
    parser.print_help()
    return 1


def _parse_inputs(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        out[key] = str(Path(value))
    return out


if __name__ == "__main__":
    sys.exit(main())
