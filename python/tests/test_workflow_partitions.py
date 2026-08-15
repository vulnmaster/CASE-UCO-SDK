"""Phase 4: partition kwargs, hash method filter, worklist partitioning."""

from __future__ import annotations

import json
from pathlib import Path

from case_uco.graph import CASEGraph
from case_uco.helpers import file_with_content_hashes
from case_uco.workflow import InvestigationWorkflow
from case_uco.workflow.worklist import partition_worklist


def test_lookup_hash_method_filter() -> None:
    graph = CASEGraph()
    file_with_content_hashes(graph, file_name="a.bin", hashes=[("SHA256", "aa"), ("MD5", "bb")])
    all_hits = graph.lookup_hash("aa")
    sha = graph.lookup_hash("aa", method="SHA256")
    md5 = graph.lookup_hash("aa", method="MD5")
    assert all_hits
    assert sha
    assert not md5


def test_partition_by_profile_default_still_core() -> None:
    graph = CASEGraph()
    file_with_content_hashes(graph, file_name="a.bin", hashes=[("SHA256", "cc")])
    parts = graph.partition_by_profile("MinimalForensics")
    assert "core" in parts
    same = graph.partition_by_profile("MinimalForensics", strategy="module-family")
    assert "core" in same


def test_partition_worklist_by_boundary() -> None:
    groups = partition_worklist(
        [
            {"path": "C/a.bin", "boundary_key": "C"},
            {"path": "D/a.bin", "boundary_key": "D"},
            {"path": "x.bin"},
        ]
    )
    assert set(groups) == {"C", "D", "_default"}


def test_infer_boundary_from_first_path_component() -> None:
    from case_uco.workflow.worklist import infer_boundary_key, ram_guard_findings

    assert infer_boundary_key("C/DCIM/img.jpg") == "volume-C"
    assert infer_boundary_key("phone1/DCIM/img.jpg") == "phone1"
    assert infer_boundary_key("img.jpg") == "_default"
    groups = partition_worklist([{"path": "C/a.bin"}, {"path": "D/b.bin"}])
    assert set(groups) == {"volume-C", "volume-D"}
    huge = ram_guard_findings({"volume-C": [{"path": f"C/{i}.bin"} for i in range(9000)]})
    assert huge and huge[0]["rule_id"] == "PROF-PART-001"


def test_forensic_boundary_requires_key() -> None:
    import pytest

    graph = CASEGraph()
    file_with_content_hashes(graph, file_name="a.bin", hashes=[("SHA256", "cc")])
    with pytest.raises(ValueError, match="boundary_key"):
        graph.partition_by_profile("AirGappedFieldTriage", strategy="forensic-boundary")


def test_parallel_scheduler_default_off() -> None:
    from case_uco.workflow.parallel import run_partitions

    seen: list[str] = []

    def worker(key: str, items: list) -> int:
        seen.append(key)
        return len(items)

    result = run_partitions({"A": [{}, {}], "B": [{}]}, worker)
    assert result == {"A": 2, "B": 1}
    assert set(seen) == {"A", "B"}
    import pytest

    with pytest.raises(NotImplementedError, match="2.1"):
        run_partitions({"A": []}, worker, enabled=True)


def test_partitioned_field_triage(tmp_path: Path) -> None:
    hashes = tmp_path / "hashes.json"
    hashes.write_text(
        json.dumps(
            [
                {"path": "C/a.bin", "boundary": "C", "hashes": [["SHA256", "11"]]},
                {"path": "D/b.bin", "boundary": "D", "hashes": [["SHA256", "22"]]},
            ]
        ),
        encoding="utf-8",
    )
    wf = InvestigationWorkflow(
        "field-triage-partitioned",
        scenario="two volumes",
        working_dir=str(tmp_path / "run"),
        inputs={"hash_list": str(hashes)},
    )
    result = wf.run()
    assert result.status in {"completed", "blocked"}
    assert "C" in wf.state["partitions"]
    assert "D" in wf.state["partitions"]
