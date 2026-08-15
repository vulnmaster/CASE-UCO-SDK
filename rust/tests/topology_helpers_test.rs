//! Topology helper / InvestigationBuilder parity tests.

use case_uco::builder::InvestigationBuilder;
use case_uco::graph::CaseGraph;
use case_uco::helpers::{file_with_content_hashes, model_csam_evidence};

#[test]
fn file_with_content_hashes_is_indexed() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    file_with_content_hashes(
        &mut graph,
        "evidence.bin",
        &[("SHA256", "e3b0c44298fc1c149afbf4c8996fb924")],
    )
    .expect("helper");
    let hits = graph.lookup_hash("E3B0C44298FC1C149AFBF4C8996FB924");
    assert!(!hits.is_empty());
    assert_eq!(hits[0].method, "SHA256");
}

#[test]
fn model_csam_evidence_hash_intelligence_shape() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let parts = model_csam_evidence(
        &mut graph,
        "img.jpg",
        &[("SHA256", "aa"), ("PhotoDNA", "bb")],
        "PhotoDNA",
        None,
    )
    .expect("csam");
    assert!(parts.tool_id.contains("Tool"));
    assert!(graph.len() >= 3);
    let json = graph.serialize().expect("json");
    assert!(json.contains("uco-observable:RasterPicture"));
    assert!(json.contains("SHA256"));
    assert!(json.contains("PhotoDNA"));
    assert!(json.contains("xsd:hexBinary"));
}

#[test]
fn investigation_builder_inline_critique() {
    let mut builder = InvestigationBuilder::new(
        "field triage of hashed images",
        Some("AirGappedFieldTriage"),
    )
    .expect("builder");
    builder.add_file("nohash.txt", &[]).expect("file");
    builder
        .add_file("ok.bin", &[("SHA256", "ab")])
        .expect("file2");
    builder
        .add_tool_run("Triage Collector", "scan", None)
        .expect("tool");
    assert!(builder.critique().iter().any(|f| f.severity == "error"));
    assert!(builder.critique().iter().any(|f| f.message.contains("version")));
    assert_eq!(builder.profile_id, "AirGappedFieldTriage");
    assert!(builder.build().len() >= 2);
}

#[test]
fn partition_by_profile_returns_core() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    file_with_content_hashes(&mut graph, "a.bin", &[("SHA256", "cc")]).expect("file");
    let parts = graph
        .partition_by_profile("MinimalForensics")
        .expect("parts");
    assert!(parts.contains_key("core"));
}
