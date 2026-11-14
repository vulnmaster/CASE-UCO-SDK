"""Tests for critic sessions (#76) and handoff (#78)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import graph_validator
from critic.sessions import (
    CriticSessionError,
    extend_critic_review,
    finalize_critic_review,
    get_critic_review_status,
    start_critic_review,
    submit_critic_revision,
    submit_manual_critic_response,
)
from critic.handoff import prepare_critic_handoff

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"


def _conforming_report(**kwargs) -> graph_validator.GraphValidationReport:
    return graph_validator.GraphValidationReport(
        conforms=True,
        warning_count=0,
        violation_count=0,
        exit_code=0,
        validator_name="case_validate",
        safe_summary="conforms",
        verification_status="complete",
        **kwargs,
    )


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    read = tmp_path / "read"
    write = tmp_path / "write"
    read.mkdir()
    write.mkdir()
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", str(read))
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(write))
    monkeypatch.setenv("CASE_UCO_CRITIC_SESSION_ROOT", str(write / "critic-sessions"))
    monkeypatch.setenv("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    monkeypatch.setattr(
        graph_validator,
        "validate_graph_file",
        lambda *a, **k: _conforming_report(),
    )
    return read, write


def _copy_gold(read: Path) -> Path:
    dest = read / "gold.jsonld"
    dest.write_text(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return dest


def _copy_gold_with_open_finding(read: Path) -> Path:
    """Gold plus one relationship between observables with an unregistered kind.

    CRIT-V-RELATIONSHIP-LINT reports it at medium severity, so the session
    has an open finding to carry across passes.
    """
    doc = json.loads((FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8"))
    doc["@context"]["uco-observable"] = "https://ontology.unifiedcyberontology.org/uco/observable/"
    file_a = "urn:uuid:77777777-7777-4777-8777-777777777777"
    file_b = "urn:uuid:88888888-8888-4888-8888-888888888888"
    doc["@graph"][0]["uco-core:object"].extend([{"@id": file_a}, {"@id": file_b}])
    doc["@graph"].extend([
        {"@id": file_a, "@type": "uco-observable:ObservableObject", "uco-core:name": "a.bin"},
        {"@id": file_b, "@type": "uco-observable:ObservableObject", "uco-core:name": "b.bin"},
        {
            "@id": "urn:uuid:99999999-9999-4999-8999-999999999999",
            "@type": "uco-core:Relationship",
            "uco-core:kindOfRelationship": "Synthetic_Unregistered_Kind",
            "uco-core:isDirectional": True,
            "uco-core:source": [{"@id": file_a}],
            "uco-core:target": [{"@id": file_b}],
        },
    ])
    dest = read / "gold.jsonld"
    dest.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return dest


def _empty_critic_response(started: dict) -> dict:
    package = started["prompt_package"]
    return {
        "schema_version": "1.2.0",
        "session_id": started["session_id"],
        "pass_number": package["pass_number"],
        "graph_sha256": package["artifact_hashes"]["graph_sha256"],
        "serializer_sha256": package["artifact_hashes"].get("serializer_sha256"),
        "prompt_package_hash": package["prompt_package_hash"],
        "review_request_sha256": package.get("review_request_sha256"),
        "review_config_sha256": package.get("review_config_sha256"),
        "findings": [],
        "finding_assessments": [],
        "scorecard": {
            "semantic_precision": {
                "assessed": True,
                "score": 4,
                "evidence": ["reviewed entity types against source text"],
            }
        },
    }


def _shell_critic_response(started: dict) -> dict:
    payload = _empty_critic_response(started)
    payload["scorecard"] = {}
    return payload


def _critical_critic_finding(started: dict) -> dict:
    payload = _empty_critic_response(started)
    payload["findings"] = [
        {
            "severity": "critical",
            "category": "investigation_structure",
            "confidence": 0.9,
            "claim_type": "missing_object_link",
            "target": {"node_id": "urn:example:investigation"},
            "evidence": ["model observed missing object"],
            "rationale": "Investigation lacks required object reference",
            "recommended_change": "Add uco-core:object",
            "verification_method": "re-analyze graph",
        }
    ]
    return payload


def test_two_pass_manual_finalize(workspace):
    read, _write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
    )
    assert started["state"] == "awaiting_critic_response"
    assert "extend_approval_challenge" in started
    sid = started["session_id"]

    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    assert revised["pass_number"] == 2
    submit_manual_critic_response(sid, _empty_critic_response(revised))

    status = get_critic_review_status(sid)
    assert status["completed_critic_responses"] == 2

    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"
    assert final["outcome"] in {"accepted", "completed_with_findings"}
    assert final["review_substance"] == "reviewed"


def test_empty_shell_review_is_not_accepted(workspace, monkeypatch):
    import critic.deterministic as det

    monkeypatch.setattr(
        det,
        "lint_kind_of_relationship",
        lambda *a, **k: {"ok": True, "checked": 0, "findings": []},
    )
    read, _write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
    )
    sid = started["session_id"]
    submit_manual_critic_response(sid, _shell_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _shell_critic_response(revised))
    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"
    assert final["review_substance"] == "empty_shell"
    assert final["outcome"] == "review_unattested"
    assert final["accepted"] is False


def test_two_pass_repair_charged_with_accepted(workspace, monkeypatch):
    """Degraded Charged_With → gold revision → empty critic → accepted.

    Open-vocab relationship lint on Charged_With is suppressed so the repair
    contract can assert true acceptance (no open medium findings from lint).
    """
    import critic.deterministic as det

    monkeypatch.setattr(
        det,
        "lint_kind_of_relationship",
        lambda *a, **k: {"ok": True, "checked": 0, "findings": []},
    )

    read, write = workspace
    degraded = read / "charged-with-reversed.jsonld"
    degraded.write_text(
        (FIXTURES / "seeded-defects.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    gold = write / "gold-charged-with.jsonld"
    gold.write_text(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    started = start_critic_review(
        graph_path=str(degraded),
        critic_scope="graph",
        model_policy="manual",
    )
    sid = started["session_id"]
    review1 = json.loads(
        (write / "critic-sessions" / sid / "review-pass-1.json").read_text()
    )
    assert review1.get("status") == "needs_revision"
    pass1_rules = {
        f["rule_id"]
        for f in review1.get("merged_findings") or []
        if f.get("rule_id") and f.get("status") != "resolved"
    }
    assert "CRIT-H-CHARGED-WITH-REVERSED" in pass1_rules

    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(
        sid,
        graph_path=str(gold),
        change_summary="repair charged-with direction to gold",
    )
    assert revised["pass_number"] == 2
    submit_manual_critic_response(sid, _empty_critic_response(revised))

    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"
    assert final["outcome"] == "accepted"
    assert final["accepted"] is True

    review2 = json.loads(
        (write / "critic-sessions" / sid / "review-pass-2.json").read_text()
    )
    resolved_charged = [
        f
        for f in review2.get("merged_findings") or []
        if f.get("rule_id") == "CRIT-H-CHARGED-WITH-REVERSED"
        and f.get("status") == "resolved"
    ]
    assert resolved_charged


def test_pass2_critic_critical_blocks_acceptance(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _critical_critic_finding(revised))
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_blockers_remain"


def test_overcap_additional_iterations_rejected(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    with pytest.raises(CriticSessionError) as exc:
        start_critic_review(
            graph_path=str(graph),
            critic_scope="graph",
            additional_iterations=99,
        )
    assert exc.value.code == "critic_session_pass_cap"


def test_manual_response_rejects_wrong_hash(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    bad = _empty_critic_response(started)
    bad["graph_sha256"] = "0" * 64
    with pytest.raises(CriticSessionError) as exc:
        submit_manual_critic_response(started["session_id"], bad)
    assert exc.value.code in {
        "critic_artifact_hash_mismatch",
        "critic_response_schema_mismatch",
    }


def test_manual_response_to_published_schema_lists_missing_bindings(workspace):
    """A response written to the on-disk schema omits the per-pass bindings.

    The schema says where the bound contract lives, and the rejection names
    every missing field in one message.
    """
    from critic.schema_util import model_response_schema

    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    package = started["prompt_package"]
    published = model_response_schema()
    bound_only = set(package["response_schema"]["required"]) - set(
        published["required"]
    )
    assert bound_only == {
        "session_id",
        "pass_number",
        "review_request_sha256",
        "review_config_sha256",
    }
    assert "response_schema" in published["description"]
    for name in bound_only:
        assert name in published["description"]

    response = {
        "schema_version": package["response_schema_version"],
        "graph_sha256": package["artifact_hashes"]["graph_sha256"],
        "prompt_package_hash": package["prompt_package_hash"],
        "findings": [],
        "scorecard": {},
    }
    with pytest.raises(CriticSessionError) as exc:
        submit_manual_critic_response(started["session_id"], response)
    assert exc.value.code == "critic_response_schema_mismatch"
    for name in bound_only:
        assert f"'{name}' is a required property" in str(exc.value)


def test_extend_uses_returned_challenge(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    with pytest.raises(CriticSessionError) as exc:
        extend_critic_review(sid, 1, approval_token="wrong")
    assert exc.value.code == "critic_session_extend_denied"

    challenge = started["extend_approval_challenge"]
    extended = extend_critic_review(sid, 2, approval_token=challenge)
    assert extended["max_total_passes"] == 4
    assert extended["extend_approval_challenge"] != challenge

    with pytest.raises(CriticSessionError) as exc2:
        extend_critic_review(
            sid, 20, approval_token=extended["extend_approval_challenge"]
        )
    assert exc2.value.code == "critic_session_pass_cap"


def test_finalize_rejects_open_critical(workspace, monkeypatch):
    read, _ = workspace
    seeded = read / "seeded.jsonld"
    seeded.write_text(
        (FIXTURES / "seeded-defects.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    started = start_critic_review(graph_path=str(seeded), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    mutated = json.loads(seeded.read_text())
    mutated["@graph"][0]["uco-core:name"] = "mutated"
    seeded.write_text(json.dumps(mutated), encoding="utf-8")
    revised = submit_critic_revision(sid, graph_path=str(seeded))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_blockers_remain"


def test_finalize_graph_scope_does_not_hash_unreviewed_serializer(workspace):
    """A graph-scoped review may record a serializer path without hashing it.

    Finalize must use that same empty serializer hash. Hashing the file
    anyway raises artifact-set mismatch after a clean review.
    """

    read, _write = workspace
    graph = _copy_gold(read)
    serializer = read / "build_graph.py"
    serializer.write_text("print('builder')\n", encoding="utf-8")
    started = start_critic_review(
        graph_path=str(graph),
        serializer_path=str(serializer),
        critic_scope="graph",
    )
    assert started["prompt_package"]["artifact_hashes"].get("serializer_sha256") is None
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    assert revised["prompt_package"]["artifact_hashes"].get("serializer_sha256") is None
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    finalized = finalize_critic_review(sid)
    assert finalized["state"] == "finalized"


def test_finalize_rejects_post_review_file_modification(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    graph.write_text(graph.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_hash_mismatch"


def test_handoff_preview_and_write(workspace, monkeypatch):
    read, write = workspace
    monkeypatch.setenv("CASE_UCO_CRITIC_HANDOFF_TOKEN", "handoff-secret")
    graph = _copy_gold_with_open_finding(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    finalize_critic_review(sid)

    review = json.loads(
        (write / "critic-sessions" / sid / "review-pass-2.json").read_text()
    )
    finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    if not finding_ids:
        review = json.loads(
            (write / "critic-sessions" / sid / "review-pass-1.json").read_text()
        )
        finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    assert finding_ids

    preview = prepare_critic_handoff(
        sid,
        finding_ids,
        requested_handoff_type="recipe_improvement",
        operator_id="tester",
        operator_rationale="review recipe guidance",
    )
    assert preview["preview"]["requires_operator_approval"] is True
    assert preview["written_path"] is None

    # extend_approval_challenge must NEVER authorize handoff write.
    with pytest.raises(CriticSessionError) as denied:
        prepare_critic_handoff(
            sid,
            finding_ids,
            requested_handoff_type="case_specific",
            operator_id="tester",
            approve_write=True,
            approval_token=started["extend_approval_challenge"],
        )
    assert denied.value.code == "critic_handoff_approval_denied"

    written = prepare_critic_handoff(
        sid,
        finding_ids,
        requested_handoff_type="case_specific",
        operator_id="tester",
        approve_write=True,
        approval_token="handoff-secret",
    )
    assert written["written_path"]
    assert "critic-handoffs/candidates" in written["written_path"].replace("\\", "/")
    assert Path(written["written_path"]).is_file()
    assert written["package_sha256"]
    on_disk = json.loads(Path(written["written_path"]).read_text(encoding="utf-8"))
    assert on_disk["package_sha256"] == written["package_sha256"]


def test_sampling_fake_context(workspace):
    import asyncio
    from critic.sampling import FakeSampleContext, maybe_sample_critic
    from critic_tools import tool_start_critic_review_with_sampling

    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="client_sampling",
    )
    payload = _empty_critic_response(started)
    ctx = FakeSampleContext(payload)

    async def _run():
        return await maybe_sample_critic(
            ctx, started["prompt_package"], model_policy="client_sampling"
        )

    sampled = asyncio.run(_run())
    assert sampled.status == "ok"
    messages = ctx.kwargs_history[0]["messages"]
    assert isinstance(messages, str)
    user_json = json.loads(messages)
    assert "prompt_package" in user_json
    assert "graph_neighborhoods" in user_json["prompt_package"]
    result = submit_manual_critic_response(started["session_id"], sampled.response)
    assert result["completed_critic_responses"] == 1

    async def _wired_ok():
        class Ctx:
            async def sample(self, **kwargs):
                messages_arg = kwargs["messages"]
                assert isinstance(messages_arg, str)
                content = json.loads(messages_arg)
                package = content["prompt_package"]
                resp = {
                    "schema_version": "1.2.0",
                    "session_id": package["session_id"],
                    "pass_number": package["pass_number"],
                    "graph_sha256": package["artifact_hashes"]["graph_sha256"],
                    "serializer_sha256": package["artifact_hashes"].get(
                        "serializer_sha256"
                    ),
                    "prompt_package_hash": package["prompt_package_hash"],
                    "review_request_sha256": package.get("review_request_sha256"),
                    "review_config_sha256": package.get("review_config_sha256"),
                    "findings": [],
                    "finding_assessments": [],
                    "scorecard": {},
                }
                return {"text": json.dumps(resp), "model": "fake"}

        return await tool_start_critic_review_with_sampling(
            Ctx(),
            graph_path=str(graph),
            critic_scope="graph",
        )

    wired = asyncio.run(_wired_ok())
    assert wired["ok"] is True
    assert wired["sampling"]["status"] == "ok"
    assert wired["state"] == "awaiting_revision"


def test_sampling_respects_deployment_manual_mode(workspace, monkeypatch):
    import asyncio
    from critic_tools import tool_start_critic_review_with_sampling

    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "manual")
    read, _ = workspace
    graph = _copy_gold(read)
    calls = {"n": 0}

    class Ctx:
        async def sample(self, **kwargs):
            calls["n"] += 1
            return {"text": "{}"}

    async def _run():
        return await tool_start_critic_review_with_sampling(
            Ctx(),
            graph_path=str(graph),
            critic_scope="graph",
            model_policy="client_sampling",
        )

    result = asyncio.run(_run())
    assert result["ok"] is True
    assert calls["n"] == 0
    assert result["model_policy"] == "manual"
    assert result["sampling"]["fallback"] is True
    assert result["sampling"]["status"] in {
        "critic_manual_response_required",
        "skipped_policy",
    }
    assert result["sampling"].get("reason") == "deployment_mode"


def test_revision_with_sampling_skips_manual_session(workspace):
    """with_sampling revision must not sample when session policy is manual."""

    import asyncio
    from critic.sampling import FakeSampleContext
    from critic_tools import tool_submit_critic_revision_with_sampling

    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
    )
    submit_manual_critic_response(started["session_id"], _empty_critic_response(started))
    ctx = FakeSampleContext({"schema_version": "1.2.0"})

    async def _run():
        return await tool_submit_critic_revision_with_sampling(
            ctx,
            session_id=started["session_id"],
            graph_path=str(graph),
            change_summary="manual-session revision",
        )

    result = asyncio.run(_run())
    assert result["ok"] is True
    assert ctx.calls == 0
    assert result["sampling"]["fallback"] is True
    assert result["sampling"]["status"] == "critic_manual_response_required"
    assert result["sampling"].get("reason") == "session_model_policy"


def test_deployment_mode_profile_defaults(monkeypatch):
    from critic.sessions import deployment_critic_mode

    monkeypatch.delenv("CASE_UCO_MCP_CRITIC_MODE", raising=False)
    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "offline-investigation")
    assert deployment_critic_mode() == "manual"

    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "production")
    assert deployment_critic_mode() == "disabled"

    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "secure")
    assert deployment_critic_mode() == "disabled"

    monkeypatch.delenv("CASE_UCO_MCP_PROFILE", raising=False)
    assert deployment_critic_mode() == "client_sampling"

    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "manual")
    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "development")
    assert deployment_critic_mode() == "manual"


def test_sampling_rejects_dict_model_preferences(workspace):
    import asyncio
    from critic.sampling import FakeSampleContext, maybe_sample_critic

    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="client_sampling",
    )
    ctx = FakeSampleContext(_empty_critic_response(started))

    async def _run():
        return await maybe_sample_critic(
            ctx,
            started["prompt_package"],
            model_policy="client_sampling",
            model_preferences={"hints": ["x"]},  # type: ignore[arg-type]
        )

    sampled = asyncio.run(_run())
    assert sampled.status == "critic_sampling_provider_error"
    assert sampled.error == "invalid_model_preferences_type"
    assert ctx.calls == 0


def test_sampling_schema_validate_retries_then_invalid(workspace):
    """Invalid model JSON retries; after retries returns invalid_response (not ok dict)."""

    import asyncio
    from critic.sampling import FakeSampleContext, maybe_sample_critic

    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="client_sampling",
    )
    bad_payload = {"schema_version": "1.2.0", "findings": "not-a-list"}
    ctx = FakeSampleContext(bad_payload)

    async def _run():
        return await maybe_sample_critic(
            ctx,
            started["prompt_package"],
            model_policy="client_sampling",
            retries=1,
        )

    sampled = asyncio.run(_run())
    assert sampled.status == "critic_sampling_invalid_response"
    assert sampled.fallback is True
    assert sampled.response is None
    assert ctx.calls >= 2


def test_handoff_offline_allows_preview_denies_write(workspace, monkeypatch):
    read, write = workspace
    monkeypatch.setenv("CASE_UCO_CRITIC_HANDOFF_TOKEN", "handoff-secret")
    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "offline-investigation")
    graph = _copy_gold_with_open_finding(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    finalize_critic_review(sid)
    review = json.loads(
        (write / "critic-sessions" / sid / "review-pass-2.json").read_text()
    )
    finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    if not finding_ids:
        review = json.loads(
            (write / "critic-sessions" / sid / "review-pass-1.json").read_text()
        )
        finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    assert finding_ids

    preview = prepare_critic_handoff(
        sid,
        finding_ids,
        requested_handoff_type="recipe_improvement",
        operator_id="tester",
    )
    assert preview["written_path"] is None

    with pytest.raises(CriticSessionError) as exc:
        prepare_critic_handoff(
            sid,
            finding_ids,
            requested_handoff_type="recipe_improvement",
            operator_id="tester",
            approve_write=True,
            approval_token="handoff-secret",
        )
    assert exc.value.code == "critic_handoff_profile_denied"


def test_prompt_not_persisted_by_default(workspace, monkeypatch):
    read, write = workspace
    monkeypatch.delenv("CASE_UCO_CRITIC_PERSIST_PROMPTS", raising=False)
    sentinel = "SENTINEL_PROMPT_LEAK_XYZ"
    graph = read / "sentinel.jsonld"
    payload = json.loads(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8")
    )
    # Put sentinel on Authorization name so it appears in prompt neighborhoods
    # when prompts are persisted, but not in typical deterministic finding text.
    for node in payload["@graph"]:
        if node.get("@type") == "case-investigation:Authorization":
            node["uco-core:name"] = sentinel
            break
    graph.write_text(json.dumps(payload), encoding="utf-8")

    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _empty_critic_response(revised))

    session_dir = write / "critic-sessions" / sid
    assert not list(session_dir.glob("prompt-pass-*.json"))
    for path in session_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        assert sentinel not in text, f"sentinel leaked into {path.name}"

    review = json.loads((session_dir / "review-pass-1.json").read_text(encoding="utf-8"))
    assert "prompt_package" not in review
    assert review.get("prompt_package_hash")
    assert review.get("prompt_content_sha256")


def test_write_root_graph_finalize_ok(workspace):
    import hashlib

    read, write = workspace
    source = read / "notes.md"
    source_body = "# source note\n"
    source.write_text(source_body, encoding="utf-8")
    source_hash = hashlib.sha256(source_body.encode("utf-8")).hexdigest()

    graph = write / "generated-gold.jsonld"
    payload = json.loads(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8")
    )
    # Source fidelity expects a same-named node with ContentDataFacet hash.
    payload["@context"]["uco-observable"] = (
        "https://ontology.unifiedcyberontology.org/uco/observable/"
    )
    source_node = {
        "@id": "urn:uuid:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "notes.md",
        "uco-core:hasFacet": [
            {
                "@id": "urn:uuid:cccccccc-cccc-4ccc-8ccc-cccccccccccc",
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [
                    {
                        "@id": "urn:uuid:dddddddd-dddd-4ddd-8ddd-dddddddddddd",
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": source_hash,
                    }
                ],
            }
        ],
    }
    payload["@context"]["uco-types"] = (
        "https://ontology.unifiedcyberontology.org/uco/types/"
    )
    payload["@graph"].append(source_node)
    payload["@graph"][0]["uco-core:object"].append({"@id": source_node["@id"]})
    graph.write_text(json.dumps(payload), encoding="utf-8")

    started = start_critic_review(
        graph_path=str(graph),
        source_paths=[str(source)],
        critic_scope="graph",
        model_policy="manual",
    )
    sid = started["session_id"]
    assert started["review"]["finding_counts"]["critical_high_open"] == 0
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(
        sid, graph_path=str(graph), source_paths=[str(source)], change_summary="confirm"
    )
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"


def test_target_passes_blocks_early_finalize(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
        additional_iterations=1,
    )
    assert started["target_passes"] == 3
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_passes_incomplete"

    challenge = started["extend_approval_challenge"]
    # Extend is not needed here — target already 3; do a third pass instead.
    revised2 = submit_critic_revision(
        sid, graph_path=str(graph), change_summary="pass3 confirm"
    )
    assert revised2["pass_number"] == 3
    submit_manual_critic_response(sid, _empty_critic_response(revised2))
    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"
    assert challenge  # retained for extend tests; unused here


def test_extend_increases_target_passes(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", additional_iterations=0
    )
    assert started["target_passes"] == 2
    sid = started["session_id"]
    extended = extend_critic_review(
        sid, 1, approval_token=started["extend_approval_challenge"]
    )
    assert extended["target_passes"] == 3
    assert extended["max_total_passes"] == 3
    with pytest.raises(CriticSessionError) as exc:
        extend_critic_review(
            sid, 20, approval_token=extended["extend_approval_challenge"]
        )
    assert exc.value.code == "critic_session_pass_cap"


def test_serializer_only_revision(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    serializer = read / "serializer.py"
    serializer.write_text(
        "# v1\nfrom case_uco import CASEGraph\ng = CASEGraph()\n",
        encoding="utf-8",
    )
    started = start_critic_review(
        graph_path=str(graph),
        serializer_path=str(serializer),
        critic_scope="both",
        model_policy="manual",
    )
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    serializer.write_text(
        "# v2 serializer-only change\nfrom case_uco import CASEGraph\ng = CASEGraph()\n",
        encoding="utf-8",
    )
    revised = submit_critic_revision(
        sid,
        graph_path=str(graph),
        serializer_path=str(serializer),
        change_summary="serializer-only",
    )
    assert revised["pass_number"] == 2
    assert revised["state"] == "awaiting_critic_response"
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"


def test_audit_chain_corruption_fails_finalize(workspace):
    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _empty_critic_response(revised))

    audit_path = write / "critic-sessions" / sid / "audit.jsonl"
    lines = audit_path.read_text(encoding="utf-8").splitlines()
    assert lines
    # Break previous_event_sha256 linkage on the last event.
    last = json.loads(lines[-1])
    last["previous_event_sha256"] = "a" * 64
    # Keep event_sha256 so verification fails on linkage (or recompute without fixing link).
    body = {k: v for k, v in last.items() if k != "event_sha256"}
    import hashlib

    last["event_sha256"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    lines[-1] = json.dumps(last, sort_keys=True)
    audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_audit_corrupt"


def _two_pass_awaiting_revision(workspace):
    """Drive a manual session through pass 2 completed → awaiting_revision."""

    read, write = workspace
    graph = _copy_gold_with_open_finding(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    sess_dir = write / "critic-sessions" / sid
    return sid, sess_dir


def test_completed_pass_tamper_fails_status_and_finalize(workspace):
    """Editing severity/status/counts in completed-pass must fail hash verify."""

    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    completed_path = sess_dir / "completed-pass-2.json"
    assert completed_path.is_file()
    data = json.loads(completed_path.read_text(encoding="utf-8"))
    assert data.get("finding_counts")
    # Valid JSON mutation that would otherwise greenwash blockers.
    if data.get("merged_findings"):
        data["merged_findings"][0]["severity"] = "low"
        data["merged_findings"][0]["status"] = "resolved"
    data["finding_counts"]["critical_high_open"] = 0
    data["finding_counts"]["open"] = 0
    data["status"] = "accepted"
    completed_path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_file_hash_mismatch"

    with pytest.raises(CriticSessionError) as exc2:
        finalize_critic_review(sid)
    assert exc2.value.code == "critic_session_file_hash_mismatch"


def test_completed_pass_tamper_fails_handoff(workspace, monkeypatch):
    """Handoff must not load tampered completed-pass via raw json.loads."""

    import critic.deterministic as det

    monkeypatch.setattr(
        det,
        "lint_kind_of_relationship",
        lambda *a, **k: {"ok": True, "checked": 0, "findings": []},
    )
    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"

    completed_path = sess_dir / "completed-pass-2.json"
    data = json.loads(completed_path.read_text(encoding="utf-8"))
    if data.get("merged_findings"):
        data["merged_findings"][0]["severity"] = "info"
        data["merged_findings"][0]["status"] = "resolved"
    else:
        data["finding_counts"]["merged"] = 99
    completed_path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    from critic.sessions import load_session_for_handoff

    with pytest.raises(CriticSessionError) as exc:
        load_session_for_handoff(sid)
    assert exc.value.code == "critic_session_file_hash_mismatch"


def test_review_pass_missing_review_config_sha256_schema_mismatch(workspace):
    """Removing review_config_sha256 fails Draft202012 schema validation on load."""

    import hashlib

    from critic.sessions import _load_review_pass, _session_dir

    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    review_path = sess_dir / "review-pass-2.json"
    data = json.loads(review_path.read_text(encoding="utf-8"))
    assert "review_config_sha256" in data
    del data["review_config_sha256"]
    raw = json.dumps(data, indent=2, sort_keys=True) + "\n"
    review_path.write_text(raw, encoding="utf-8")
    # Retarget stored digests so hash verify is not the first failure.
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    session_path = sess_dir / "session.json"
    session = json.loads(session_path.read_text(encoding="utf-8"))
    session["pass_file_hashes"]["review-pass-2.json"] = digest
    for item in session.get("passes") or []:
        if int(item.get("pass_number") or 0) == 2 and isinstance(item.get("files"), dict):
            item["files"]["review-pass-2.json"] = digest
    session_path.write_text(
        json.dumps(session, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with pytest.raises(CriticSessionError) as exc:
        _load_review_pass(_session_dir(sid), 2)
    assert exc.value.code == "critic_session_schema_mismatch"


def test_pass_file_hashes_recorded_on_write(workspace):
    import hashlib

    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    hashes = session["pass_file_hashes"]
    for name in (
        "review-pass-1.json",
        "config-pass-1.json",
        "completed-pass-1.json",
        "critic-pass-1.json",
        "review-pass-2.json",
        "config-pass-2.json",
        "completed-pass-2.json",
        "critic-pass-2.json",
    ):
        assert name in hashes
        actual = hashlib.sha256((sess_dir / name).read_bytes()).hexdigest()
        assert hashes[name] == actual
    pass2 = next(p for p in session["passes"] if p["pass_number"] == 2)
    assert "completed-pass-2.json" in pass2["files"]
    assert session.get("latest_audit_event_sha256")
    audit_lines = [
        ln
        for ln in (sess_dir / "audit.jsonl").read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert json.loads(audit_lines[-1])["event_sha256"] == session["latest_audit_event_sha256"]


def _rewrite_session(sess_dir: Path, session: dict) -> None:
    (sess_dir / "session.json").write_text(
        json.dumps(session, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def test_completed_pass_semantic_tamper_retargeted_session_hashes_fails(workspace):
    """Retargeting session digests without audit must fail reconcile."""

    import hashlib

    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    completed_path = sess_dir / "completed-pass-2.json"
    data = json.loads(completed_path.read_text(encoding="utf-8"))
    if data.get("merged_findings"):
        data["merged_findings"][0]["severity"] = "low"
        data["merged_findings"][0]["status"] = "resolved"
    data["finding_counts"]["critical_high_open"] = 0
    data["finding_counts"]["open"] = 0
    data["status"] = "accepted"
    raw = json.dumps(data, indent=2, sort_keys=True) + "\n"
    completed_path.write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    session["pass_file_hashes"]["completed-pass-2.json"] = digest
    for item in session.get("passes") or []:
        if int(item.get("pass_number") or 0) == 2 and isinstance(item.get("files"), dict):
            item["files"]["completed-pass-2.json"] = digest
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_reconcile_mismatch"


def test_forged_finalized_state_without_finalize_audit_fails(workspace):
    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    session["state"] = "finalized"
    session["final_outcome"] = "accepted"
    session["accepted"] = True
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_reconcile_mismatch"

    from critic.sessions import load_session_for_handoff

    with pytest.raises(CriticSessionError) as exc2:
        load_session_for_handoff(sid)
    assert exc2.value.code in {
        "critic_session_audit_reconcile_mismatch",
        "critic_session_not_finalized",
    }


def test_altered_outcome_after_finalize_fails_projection(workspace, monkeypatch):
    import critic.deterministic as det

    monkeypatch.setattr(
        det,
        "lint_kind_of_relationship",
        lambda *a, **k: {"ok": True, "checked": 0, "findings": []},
    )
    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"

    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    session["final_outcome"] = "completed_with_findings"
    session["accepted"] = False
    session["latest_review_summary"] = {
        **(session.get("latest_review_summary") or {}),
        "status": "needs_revision",
    }
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_reconcile_mismatch"


def test_session_audit_file_map_disagreement_fails(workspace):
    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    assert "completed-pass-2.json" in session["pass_file_hashes"]
    del session["pass_file_hashes"]["completed-pass-2.json"]
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_reconcile_mismatch"


def test_interrupted_transaction_latest_audit_event_sha_fails(workspace):
    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    session["latest_audit_event_sha256"] = "0" * 64
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_incomplete_transaction"


def _set_dotted(session: dict, dotted: str, value) -> None:
    """Mutate a dotted path; ``passes[0].critic`` selects the first pass entry."""

    parts = dotted.replace("passes[0]", "passes.0").split(".")
    cur: object = session
    for part in parts[:-1]:
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]  # type: ignore[index]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value  # type: ignore[index]


@pytest.mark.parametrize(
    "field_path,mutator",
    [
        ("prior_findings", lambda s: s.__setitem__("prior_findings", [])),
        ("prior_finding_ids", lambda s: s.__setitem__("prior_finding_ids", [])),
        (
            "config.source_paths",
            lambda s: _set_dotted(s, "config.source_paths", ["/tmp/forged"]),
        ),
        (
            "config.coverage_contract_path",
            lambda s: _set_dotted(
                s, "config.coverage_contract_path", "/tmp/forged-contract.json"
            ),
        ),
        (
            "config.critic_scope",
            lambda s: _set_dotted(s, "config.critic_scope", "investigation"),
        ),
        (
            "config.extensions",
            lambda s: _set_dotted(s, "config.extensions", ["forged-ext"]),
        ),
        (
            "config.profiles",
            lambda s: _set_dotted(s, "config.profiles", ["forged-profile"]),
        ),
        (
            "config.report_output",
            lambda s: _set_dotted(s, "config.report_output", "/tmp/forged-report.json"),
        ),
        (
            "config.project_root",
            lambda s: _set_dotted(s, "config.project_root", "/tmp"),
        ),
        (
            "extend_approval_token",
            lambda s: s.__setitem__("extend_approval_token", "forged-token"),
        ),
        (
            "extend_approval_challenge",
            lambda s: s.__setitem__("extend_approval_challenge", "forged-challenge"),
        ),
        (
            "passes[0].critic",
            lambda s: _set_dotted(
                s, "passes[0].critic", {"status": "accepted", "finding_count": 0}
            ),
        ),
        (
            "passes[0].completed_pass",
            lambda s: _set_dotted(
                s,
                "passes[0].completed_pass",
                {"status": "accepted", "open_finding_ids": []},
            ),
        ),
        (
            "latest_prompt_package_hash",
            lambda s: s.__setitem__("latest_prompt_package_hash", "a" * 64),
        ),
        (
            "latest_review_request_sha256",
            lambda s: s.__setitem__("latest_review_request_sha256", "b" * 64),
        ),
    ],
)
def test_full_session_projection_detects_omitted_field_tamper(
    workspace, field_path, mutator
):
    """Any semantic session.json edit must break audit projection binding."""

    sid, sess_dir = _two_pass_awaiting_revision(workspace)
    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    assert "latest_audit_event_sha256" in session
    mutator(session)
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_reconcile_mismatch"
    assert "session_projection_sha256" in str(exc.value)


def test_prior_findings_model_finding_cannot_be_erased_before_pass_two(workspace):
    """Deleting a pass-1 model finding from session.json is detected; ledger keeps it."""

    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    payload = _empty_critic_response(started)
    payload["findings"] = [
        {
            "severity": "medium",
            "category": "investigation_structure",
            "confidence": 0.85,
            "claim_type": "sampled_model_claim",
            "target": {"node_id": "urn:example:investigation"},
            "evidence": ["model observed structure"],
            "rationale": "pass-1 model finding",
            "recommended_change": "clarify object link",
            "verification_method": "re-analyze",
        }
    ]
    submit_manual_critic_response(sid, payload)

    sess_dir = write / "critic-sessions" / sid
    session = json.loads((sess_dir / "session.json").read_text(encoding="utf-8"))
    prior = list(session.get("prior_findings") or [])
    model_findings = [
        f
        for f in prior
        if f.get("evidence_kind") == "critic_inference"
        or f.get("claim_type") == "sampled_model_claim"
    ]
    assert model_findings, "expected pass-1 model finding in prior_findings"
    model_id = model_findings[0]["finding_id"]
    assert model_id in (session.get("prior_finding_ids") or [])

    # Tamper: erase model finding from the live session projection only.
    session["prior_findings"] = [
        f for f in prior if f.get("finding_id") != model_id
    ]
    session["prior_finding_ids"] = [
        fid for fid in (session.get("prior_finding_ids") or []) if fid != model_id
    ]
    _rewrite_session(sess_dir, session)

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_reconcile_mismatch"

    with pytest.raises(CriticSessionError) as exc2:
        submit_critic_revision(sid, graph_path=str(graph), change_summary="tamper")
    assert exc2.value.code == "critic_session_audit_reconcile_mismatch"

    # Untampered path: pass-1 model finding remains in the pass-2 ledger.
    clean = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    clean_payload = _empty_critic_response(clean)
    clean_payload["findings"] = list(payload["findings"])
    submit_manual_critic_response(clean["session_id"], clean_payload)
    revised = submit_critic_revision(
        clean["session_id"], graph_path=str(graph), change_summary="confirm"
    )
    ledger = revised["assessment_ledger"]
    model_open = [
        fid
        for fid, meta in ledger.items()
        if meta.get("evidence_kind") == "critic_inference"
    ]
    assert model_open, "pass-1 model finding must remain in pass-2 lifecycle"

