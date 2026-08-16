use case_uco::streaming::JsonLdStreamWriter;
use serde_json::json;
use std::collections::HashMap;

fn context() -> HashMap<String, String> {
    HashMap::from([
        ("kb".to_string(), "https://example.org/kb/".to_string()),
        (
            "uco-core".to_string(),
            "https://ontology.unifiedcyberontology.org/uco/core/".to_string(),
        ),
    ])
}

#[test]
fn bounded_writer_streams_incremental_nodes() {
    let dir = tempfile::tempdir().expect("tempdir");
    let output = dir.path().join("bounded.jsonld");
    let mut writer = JsonLdStreamWriter::with_options(&output, context(), 1024, true, true)
        .expect("writer");
    for i in 0..100 {
        writer
            .write_node(&json!({
                "@id": format!("kb:node-{i}"),
                "@type": "uco-core:UcoObject",
                "uco-core:name": format!("Node {i}")
            }))
            .expect("node");
    }
    let metrics = writer.complete().expect("complete");
    let document: serde_json::Value =
        serde_json::from_slice(&std::fs::read(output).expect("output")).expect("json");
    assert_eq!(document["@graph"].as_array().expect("graph").len(), 100);
    assert_eq!(metrics.nodes, 100);
    assert!(metrics.max_node_bytes_written <= 1024);
}

#[test]
fn bounded_writer_failure_preserves_existing_destination() {
    let dir = tempfile::tempdir().expect("tempdir");
    let output = dir.path().join("existing.jsonld");
    std::fs::write(&output, b"SURVIVE").expect("seed");

    let mut writer = JsonLdStreamWriter::with_options(&output, context(), 128, true, true)
        .expect("writer");
    let prefix_error = writer
        .write_node(&json!({"@id": "kb:bad", "@type": "evil:Fabricated"}))
        .expect_err("prefix");
    assert!(prefix_error.to_string().contains("undeclared JSON-LD prefix"));
    drop(writer);
    assert_eq!(std::fs::read(&output).expect("existing"), b"SURVIVE");

    let mut writer = JsonLdStreamWriter::with_options(&output, context(), 128, true, true)
        .expect("writer");
    let cap_error = writer
        .write_node(&json!({
            "@id": "kb:large",
            "@type": "uco-core:UcoObject",
            "uco-core:name": "x".repeat(1000)
        }))
        .expect_err("cap");
    assert!(cap_error.to_string().contains("max_node_bytes"));
    drop(writer);
    assert_eq!(std::fs::read(&output).expect("existing"), b"SURVIVE");
}
