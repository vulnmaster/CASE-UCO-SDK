"""Tests for CaseLinker ICAC remodel helpers (#128–#132)."""

from __future__ import annotations

import json

import pytest
from case_uco import CASEGraph

from tools.caselinker_icac_remodel import (
    CASELINKER_VOCAB,
    CaselinkerVocabError,
    build_share_safe_series_match,
    map_caselinker_predicate,
    refuse_caselinker_vocab,
)


def test_caselinker_predicates_map_or_drop():
    assert map_caselinker_predicate(f"{CASELINKER_VOCAB}chargeCluster") == (
        "legalproc:statuteCitation"
    )
    assert map_caselinker_predicate(f"{CASELINKER_VOCAB}admissionTheme") is None


def test_unknown_caselinker_predicate_fails_closed():
    with pytest.raises(CaselinkerVocabError):
        map_caselinker_predicate(f"{CASELINKER_VOCAB}inventedPredicate")


def test_refuse_caselinker_vocab():
    with pytest.raises(CaselinkerVocabError):
        refuse_caselinker_vocab([f"{CASELINKER_VOCAB}chargeCluster"])
    refuse_caselinker_vocab(["legalproc:statuteCitation"])


def test_share_safe_series_match_types_reference_url():
    graph = CASEGraph()
    build_share_safe_series_match(
        graph,
        file_id="kb:file-1",
        file_name="exhibit-1.bin",
        sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        series_id="SERIES-DEMO-001",
        photodna_present=True,
    )
    output = json.loads(graph.serialize())
    file_obj = next(n for n in output["@graph"] if n["@id"].endswith("file-1"))
    ref = file_obj["uco-core:externalReference"]
    if isinstance(ref, list):
        ref = ref[0]
    assert ref["uco-core:referenceURL"]["@type"] == "xsd:anyURI"
    assert file_obj["uco-core:tag"] == "photodna-match-reported-value-withheld"


def test_share_safe_series_match_requires_hash():
    graph = CASEGraph()
    with pytest.raises(ValueError, match="cryptographic hash"):
        build_share_safe_series_match(
            graph,
            file_id="kb:file-1",
            file_name="exhibit-1.bin",
            sha256="",
            series_id="SERIES-DEMO-001",
            photodna_present=False,
        )
