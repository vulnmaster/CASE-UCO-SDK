//! Tests for CaseGraph builder and JSON-LD serialization.

use case_uco::graph::CaseGraph;
use case_uco::uco::observable::ObservableObject;
use case_uco::uco::tool::Tool;

#[test]
fn test_create_tool() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder()
        .version("7.0".to_string())
        .tool_type("forensic".to_string())
        .build();

    let id = graph.create(&tool);
    assert!(id.starts_with("kb:Tool-"));
}

#[test]
fn test_legacy_add_api() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder().build();
    let id = graph.add("Tool", Tool::CLASS_IRI, &tool);
    assert!(id.starts_with("kb:Tool-"));
}

#[test]
fn test_serialize_produces_valid_json() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder().build();
    graph.create(&tool);

    let json = graph.serialize().expect("serialization should succeed");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    assert!(parsed.get("@context").is_some());
    assert!(parsed.get("@graph").is_some());
}

#[test]
fn test_prefixed_property_names() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder()
        .tool_type("forensic".to_string())
        .version("7.0".to_string())
        .build();
    graph.create(&tool);

    let json = graph.serialize().expect("serialization should succeed");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    let obj = parsed.get("@graph").unwrap().as_array().unwrap()[0].clone();
    assert!(obj.get("uco-tool:toolType").is_some());
    assert!(obj.get("tool_type").is_none());
}

#[test]
fn test_typed_boolean_literals() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let observable = ObservableObject::builder().has_changed(true).build();
    graph.create(&observable);

    let json = graph.serialize().expect("serialization should succeed");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    let obj = parsed.get("@graph").unwrap().as_array().unwrap()[0].clone();
    assert_eq!(obj["uco-observable:hasChanged"]["@type"], "xsd:boolean");
    assert_eq!(obj["uco-observable:hasChanged"]["@value"], "true");
}

#[test]
fn test_multiple_objects() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let t1 = Tool::builder().build();
    let t2 = Tool::builder().build();
    graph.create(&t1);
    graph.create(&t2);

    let json = graph.serialize().expect("serialization should succeed");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    let graph_array = parsed.get("@graph").unwrap().as_array().unwrap();
    assert_eq!(graph_array.len(), 2);
}
