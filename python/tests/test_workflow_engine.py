"""Sequential Investigation Workflow Engine."""

from __future__ import annotations

import json
from pathlib import Path

from case_uco.workflow import InvestigationWorkflow, get_workflow, list_workflows
from case_uco.workflow.handlers import file_node_id, identity_key


def test_workflows_are_listed() -> None:
    ids = {w.id for w in list_workflows()}
    assert {"field-triage", "hash-intelligence-vics", "cac-csam-provenance", "cac-grooming-chat"} <= ids
    assert get_workflow("field-triage") is not None
    assert get_workflow("field-triage").air_gapped is True


def test_field_triage_end_to_end(tmp_path: Path) -> None:
    hashes = tmp_path / "hashes.json"
    hashes.write_text(
        json.dumps(
            [
                {"path": "C/DCIM/img.jpg", "boundary": "C", "hashes": [["SHA256", "aa"], ["PhotoDNA", "bb"]]},
                {"path": "D/DCIM/img.jpg", "boundary": "D", "hashes": [["SHA256", "cc"]]},
            ]
        ),
        encoding="utf-8",
    )
    run_dir = tmp_path / "run"
    wf = InvestigationWorkflow(
        "field-triage",
        scenario="seized laptop",
        working_dir=str(run_dir),
        inputs={"hash_list": str(hashes)},
    )
    result = wf.run()
    assert result.status in {"completed", "blocked"}
    assert (run_dir / "workflow-state.json").is_file()
    assert len(wf.graph) >= 3
    a = file_node_id("http://example.org/kb/", "C", "C/DCIM/img.jpg")
    b = file_node_id("http://example.org/kb/", "D", "D/DCIM/img.jpg")
    assert a != b


def test_resume_retries_running_steps(tmp_path: Path) -> None:
    hashes = tmp_path / "hashes.json"
    hashes.write_text(json.dumps([{"path": "vol/a.bin", "hashes": [["SHA256", "dd"]]}]), encoding="utf-8")
    run_dir = tmp_path / "run"
    wf = InvestigationWorkflow(
        "field-triage",
        scenario="resume test",
        working_dir=str(run_dir),
        inputs={"hash_list": str(hashes)},
    )
    wf.step()  # load
    wf.state["cursor"]["running_steps"] = ["open"]
    wf.save()
    resumed = InvestigationWorkflow.resume(str(run_dir))
    assert resumed.state["cursor"]["running_steps"] == []
    result = resumed.run()
    assert result.status in {"completed", "blocked"}


def test_two_img_jpg_different_paths_are_two_nodes() -> None:
    assert identity_key("C", "C/DCIM/img.jpg") != identity_key("D", "D/DCIM/img.jpg")


def test_hash_intelligence_workflow(tmp_path: Path) -> None:
    hashes = tmp_path / "hashes.json"
    hashes.write_text(
        json.dumps([{"path": "media/img.jpg", "file_name": "img.jpg", "hashes": [["SHA256", "ee"], ["PhotoDNA", "ff"]]}]),
        encoding="utf-8",
    )
    wf = InvestigationWorkflow(
        "hash-intelligence-vics",
        scenario="local VICS export",
        working_dir=str(tmp_path / "hi"),
        inputs={"hash_list": str(hashes)},
    )
    result = wf.run()
    assert result.status in {"completed", "blocked"}
    assert result.profile_id == "HashIntelligence"
    assert wf.builder.critique()  # may be empty if hashes present
