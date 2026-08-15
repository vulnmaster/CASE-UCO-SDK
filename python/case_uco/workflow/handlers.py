"""Built-in sequential workflow handlers (Phase 2)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from case_uco.helpers import file_with_content_hashes, model_csam_evidence, model_tool_run


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def identity_key(boundary: str | None, relative_path: str) -> str:
    return f"{boundary or '_default'}\0{relative_path.replace(chr(92), '/')}"


def file_node_id(kb_prefix: str, boundary: str | None, relative_path: str, *, picture: bool = False) -> str:
    digest = _sha(identity_key(boundary, relative_path))
    kind = "RasterPicture" if picture else "File"
    return f"{kb_prefix}{kind}-{digest}"


def investigation_id(kb_prefix: str, scenario: str) -> str:
    return f"{kb_prefix}Investigation-{_sha(scenario)}"


def tool_id(kb_prefix: str, name: str, version: str | None) -> str:
    return f"{kb_prefix}Tool-{_sha(f'{name}|{version or ''}')}"


def ingest_hash_list(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    path = workflow.state["inputs"].get("hash_list")
    if not path:
        if args.get("optional") or True:
            return {"ingested": 0}
        raise FileNotFoundError("hash_list input is required")
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"hash_list not found: {source}")
    raw = source.read_text(encoding="utf-8")
    if source.suffix.lower() in {".tsv", ".csv"}:
        rows = _parse_tsv(raw)
    else:
        payload = json.loads(raw)
        rows = payload if isinstance(payload, list) else payload.get("items") or payload.get("files") or []
    worklist = list(workflow.state.get("worklist") or [])
    by_key = {identity_key(item.get("boundary_key"), item["path"]): item for item in worklist if item.get("path")}
    for row in rows:
        rel = str(row.get("path") or row.get("file_name") or row.get("file") or "")
        if not rel:
            continue
        boundary = row.get("boundary") or row.get("boundary_key") or "_default"
        key = identity_key(boundary, rel)
        hashes = list(row.get("hashes") or [])
        if row.get("method") and row.get("digest"):
            hashes.append([row["method"], row["digest"]])
        if key in by_key:
            existing = by_key[key].setdefault("hashes", [])
            for pair in hashes:
                if list(pair) not in [list(p) for p in existing]:
                    existing.append(list(pair))
        else:
            item = {
                "path": rel.replace("\\", "/"),
                "file_name": Path(rel).name,
                "boundary_key": boundary,
                "hashes": [list(p) for p in hashes],
                "host_hint": row.get("host_hint") or ("RasterPicture" if rel.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")) else "File"),
            }
            worklist.append(item)
            by_key[key] = item
    workflow.state["worklist"] = worklist
    return {"ingested": len(worklist)}


def _parse_tsv(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        return rows
    header = [h.strip() for h in lines[0].replace(",", "\t").split("\t")]
    for line in lines[1:]:
        cols = [c.strip() for c in line.replace(",", "\t").split("\t")]
        rec = {header[i]: cols[i] if i < len(cols) else "" for i in range(len(header))}
        hashes = []
        if rec.get("method") and rec.get("digest"):
            hashes.append([rec["method"], rec["digest"]])
        rec["hashes"] = hashes
        rows.append(rec)
    return rows


def open_investigation(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    from case_uco.case.investigation import Investigation

    nid = investigation_id(workflow.builder.graph.kb_prefix if hasattr(workflow.builder.graph, "kb_prefix") else workflow.state["kb_prefix"], workflow.state["scenario"])
    # CASEGraph stores prefix on create; use documented kb prefix.
    kb = workflow.state["kb_prefix"]
    nid = investigation_id(kb, workflow.state["scenario"])
    workflow.builder.graph.create(Investigation, id=nid, name=workflow.state["scenario"])
    return {"investigation_id": nid}


def model_tool_run_handler(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    name = args.get("tool_name") or "Unknown Tool"
    version = args.get("tool_version")
    action = args.get("action_name") or "run"
    kb = workflow.state["kb_prefix"]
    tid = tool_id(kb, name, version)
    result = model_tool_run(
        workflow.builder.graph,
        tool_name=name,
        tool_version=version,
        action_name=action,
    )
    workflow.builder.critic.observe_add(
        workflow.builder.graph,
        host="Tool",
        node=result.get("tool"),
        extra={"tool_name": name, "tool_version": version},
        source="add_tool_run",
    )
    return {"tool": tid}


def hash_media(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    csam = bool(args.get("csam"))
    created = 0
    kb = workflow.state["kb_prefix"]
    for item in workflow.state.get("worklist") or []:
        rel = item["path"]
        hashes = [tuple(p) for p in item.get("hashes") or []]
        picture = csam or item.get("host_hint") == "RasterPicture"
        nid = file_node_id(kb, item.get("boundary_key"), rel, picture=picture)
        if workflow.builder.graph.contains(nid):
            # append extra hashes if present
            continue
        if picture:
            _add_csam(workflow, item, hashes, nid)
        else:
            file_with_content_hashes(
                workflow.builder.graph,
                file_name=item.get("file_name") or Path(rel).name,
                hashes=hashes,
                id=nid,
            )
            workflow.builder.critic.observe_add(
                workflow.builder.graph,
                host="File",
                extra={"file_name": item.get("file_name") or rel, "hashes": hashes},
                source="add_file",
            )
        created += 1
    return {"created": created}


def _add_csam(workflow: Any, item: dict[str, Any], hashes: list[tuple[str, str]], nid: str) -> None:
    from case_uco.helpers import raster_picture_with_hashes

    raster_picture_with_hashes(
        workflow.builder.graph,
        file_name=item.get("file_name") or Path(item["path"]).name,
        hashes=hashes,
        id=nid,
    )
    model_tool_run(
        workflow.builder.graph,
        tool_name="PhotoDNA",
        tool_version=None,
        action_name=f"PhotoDNA hash of {item.get('file_name') or item['path']}",
    )
    workflow.builder.critic.observe_add(
        workflow.builder.graph,
        host="RasterPicture",
        extra={"file_name": item.get("file_name") or item["path"], "hashes": hashes},
        source="add_csam_evidence",
    )


def critique_graph(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    report = workflow.builder.critique_report(when="graph")
    workflow.state["findings"] = [f.to_compat_dict() for f in report.findings]
    workflow.state["partitions"]["_default"]["findings_open"] = report.blocking_open
    workflow.state["partitions"]["_default"]["estimated_triples"] = report.estimated_triples
    return {"blocking_open": report.blocking_open, "findings": len(report.findings)}


def validate_partition(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    report = workflow.builder.critique_report(when="graph")
    validation = {
        "last_run": "graph",
        "conforms": None if not report.shacl else report.shacl.get("conforms"),
        "available": None if not report.shacl else report.shacl.get("available"),
    }
    workflow.state["validation"] = validation
    return validation


def emit_jsonld(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    path = Path(workflow.state["partitions"]["_default"]["graph_path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    stats = workflow.builder.graph.write_streaming(str(path))
    workflow.state["partitions"]["_default"]["nodes"] = stats.get("nodes", 0)
    workflow.state["partitions"]["_default"]["status"] = "completed"
    return {"path": str(path), **stats}


def partition_forensic(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    from case_uco.workflow.worklist import partition_worklist

    groups = partition_worklist(list(workflow.state.get("worklist") or []))
    partitions = workflow.state.setdefault("partitions", {})
    for key, items in groups.items():
        partitions[key] = {
            "graph_path": str(Path(workflow.state["working_dir"]) / f"{key}.jsonld"),
            "status": "planned",
            "estimated_triples": 0,
            "nodes": 0,
            "findings_open": 0,
            "work_items": len(items),
        }
    return {"partitions": list(groups.keys()), "items": sum(len(v) for v in groups.values())}


def apply_adapter(workflow: Any, args: dict[str, Any]) -> dict[str, Any]:
    from case_uco.adapters import get_adapter

    adapter_id = args.get("adapter") or (
        workflow.definition.adapters[0] if getattr(workflow.definition, "adapters", None) else None
    )
    if not adapter_id:
        raise ValueError("adapter id required")
    source_key = args.get("input") or "catalog_path"
    source = workflow.state["inputs"].get(source_key) or workflow.state["inputs"].get("hash_list")
    if not source:
        raise FileNotFoundError("adapter source input missing")
    adapter = get_adapter(adapter_id)
    return adapter.apply(workflow.builder, Path(source))


HANDLERS = {
    "load_profile": lambda wf, args: {"profile_id": wf.builder.profile.id},
    "open_investigation": open_investigation,
    "model_tool_run": model_tool_run_handler,
    "ingest_hash_list": ingest_hash_list,
    "ingest_file_listing": ingest_hash_list,
    "hash_media": hash_media,
    "critique_graph": critique_graph,
    "validate_partition": validate_partition,
    "emit_jsonld": emit_jsonld,
    "partition_forensic": partition_forensic,
    "apply_adapter": apply_adapter,
}
