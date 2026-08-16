//! Tests for CaseGraph builder and JSON-LD serialization.

use case_uco::graph::{CaseGraph, GraphError, PartitionBoundary, PartitionOptions};
use case_uco::uco::observable::ObservableObject;
use case_uco::uco::tool::Tool;
use serde_json::Value;
use std::collections::BTreeMap;

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
fn test_create_with_custom_id() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder()
        .version("7.0".to_string())
        .build();

    let id = graph.create_with_id("kb:Tool-my-stable-id", &tool);
    assert_eq!(id, "kb:Tool-my-stable-id");

    let json = graph.serialize().expect("serialization should succeed");
    assert!(json.contains("kb:Tool-my-stable-id"));
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

#[test]
fn test_context_prunes_unused_prefixes() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder()
        .version("1.0".to_string())
        .build();
    graph.create(&tool);

    let json = graph.serialize().expect("serialization should succeed");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    let ctx = parsed.get("@context").unwrap();

    assert!(ctx.get("kb").is_some(), "used prefix kb should be present");
    assert!(ctx.get("uco-tool").is_some(), "used prefix uco-tool should be present");

    let unused = vec![
        "uco-identity", "uco-location", "uco-role", "uco-victim",
        "uco-configuration", "uco-marking", "uco-pattern", "uco-time",
    ];
    for prefix in unused {
        assert!(ctx.get(prefix).is_none(), "unused prefix should be pruned: {}", prefix);
    }
}

#[test]
fn test_empty_graph_has_empty_context() {
    let graph = CaseGraph::new("http://example.org/kb/");
    let json = graph.serialize().expect("serialization should succeed");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    let ctx = parsed.get("@context").unwrap().as_object().unwrap();
    assert!(ctx.is_empty(), "empty graph should have empty context");
}

#[test]
fn test_len_and_is_empty() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    assert!(graph.is_empty());
    assert_eq!(graph.len(), 0);

    graph.create(&Tool::builder().build());
    assert!(!graph.is_empty());
    assert_eq!(graph.len(), 1);
}

#[test]
fn test_load_json_ld() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let json_ld = r#"{
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/"
        },
        "@graph": [
            {
                "@id": "kb:Tool-existing-001",
                "@type": "uco-tool:Tool"
            }
        ]
    }"#;

    graph.load(json_ld).expect("load should succeed");
    assert_eq!(graph.len(), 1);

    let output = graph.serialize().expect("serialization should succeed");
    assert!(output.contains("kb:Tool-existing-001"));
}

#[test]
fn test_load_rejects_duplicate_by_default() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node(
            "kb:x",
            Some(serde_json::json!("uco-core:UcoObject")),
            None,
        )
        .expect("upsert");
    let err = graph
        .load(r#"{"@context":{"kb":"http://example.org/kb/"},"@graph":[{"@id":"kb:x","@type":"uco-core:UcoObject"}]}"#)
        .expect_err("duplicate should fail");
    assert!(err.to_string().contains("Duplicate"));
}

#[test]
fn test_load_rejects_context_collision() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let err = graph
        .load(r#"{"@context":{"kb":"http://example.org/kb/","uco-core":"https://evil.example.org/uco/core/"},"@graph":[]}"#)
        .expect_err("context collision should fail");
    assert!(err.to_string().contains("Context prefix collision"));
}

#[test]
fn test_get_is_owned_deep_copy() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let props = serde_json::json!({
        "uco-core:name": "N",
        "uco-core:tag": ["a", "b"],
        "uco-core:hasFacet": [{"@id": "kb:f1"}]
    });
    graph
        .upsert_node(
            "kb:n1",
            Some(serde_json::json!("uco-core:UcoObject")),
            Some(props.as_object().cloned().expect("object")),
        )
        .expect("upsert");
    let mut view = graph.get("kb:n1").expect("get");
    if let Some(Value::Array(tags)) = view.get_mut("uco-core:tag") {
        tags.push(Value::String("c".into()));
    }
    if let Some(Value::Array(facets)) = view.get_mut("uco-core:hasFacet") {
        if let Some(Value::Object(f0)) = facets.get_mut(0) {
            f0.insert("@id".into(), Value::String("kb:mutated".into()));
        }
    }
    let stored = graph.get("kb:n1").expect("get again");
    assert_eq!(stored.get("uco-core:name").and_then(|v| v.as_str()), Some("N"));
    assert_eq!(
        stored.get("uco-core:tag"),
        Some(&serde_json::json!(["a", "b"]))
    );
    assert_eq!(
        stored["uco-core:hasFacet"][0]["@id"],
        serde_json::json!("kb:f1")
    );
}

#[test]
fn test_named_duplicate_policies_and_split() {
    use case_uco::graph::DuplicatePolicy;
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph.on_duplicate = DuplicatePolicy::MergeCompatible;
    graph
        .upsert_node(
            "kb:x",
            Some(serde_json::json!("uco-core:UcoObject")),
            Some(
                serde_json::json!({"uco-core:name": "A"})
                    .as_object()
                    .cloned()
                    .expect("object"),
            ),
        )
        .expect("upsert");
    graph
        .load_with_policy(
            r#"{"@context":{"kb":"http://example.org/kb/"},"@graph":[{"@id":"kb:x","@type":"uco-core:UcoObject","uco-core:description":"d"}]}"#,
            DuplicatePolicy::MergeCompatible,
        )
        .expect("merge");
    assert!(graph.get("kb:x").unwrap().contains_key("uco-core:description"));
    assert!(matches!(
        graph.split(0),
        Err(case_uco::graph::GraphError::InvalidSplitSize(0))
    ));
}

#[test]
fn test_set_property_and_relationship_id() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node("kb:src", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("src");
    graph
        .upsert_node("kb:tgt", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("tgt");
    graph
        .set_property("kb:src", "uco-core:name", serde_json::json!("S"))
        .expect("set");
    let r1 = graph
        .create_relationship("kb:src", "kb:tgt", "Derived_From", true, None, Some("kb:rel-a"))
        .expect("rel a");
    let r2 = graph
        .create_relationship("kb:src", "kb:tgt", "Derived_From", true, None, Some("kb:rel-b"))
        .expect("rel b");
    assert_ne!(r1.get("@id"), r2.get("@id"));
    assert_eq!(graph.len(), 4);
}

#[test]
fn test_write_streaming_roundtrip() {
    use std::fs;

    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node(
            "kb:t",
            Some(serde_json::json!("uco-tool:Tool")),
            Some(
                serde_json::json!({"uco-core:name": "X"})
                    .as_object()
                    .cloned()
                    .expect("object"),
            ),
        )
        .expect("upsert");

    let path = std::env::temp_dir().join("case_uco_rust_stream_test.jsonld");
    let metrics = graph
        .write_streaming(path.to_str().expect("temp path"))
        .expect("write_streaming");
    assert_eq!(metrics.nodes, 1);
    assert!(metrics.bytes_written > 0);

    let mut loaded = CaseGraph::new("http://example.org/kb/");
    let json = fs::read_to_string(&path).expect("read streamed file");
    loaded.load(&json).expect("load streamed file");
    assert_eq!(
        loaded.get("kb:t").unwrap()["uco-core:name"],
        serde_json::json!("X")
    );
    let _ = fs::remove_file(path);
}

#[test]
fn test_partition_by_roots_dependency_closure() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node("kb:root-a", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("root a");
    graph
        .upsert_node("kb:child-a", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("child a");
    graph
        .upsert_node("kb:root-b", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("root b");
    graph
        .link("kb:root-a", "uco-core:hasFacet", "kb:child-a")
        .expect("link");

    let parts = graph
        .partition_by_roots(
            &["kb:root-a".to_string(), "kb:root-b".to_string()],
            "duplicate",
        )
        .expect("partition");

    assert_eq!(parts.get("kb:root-a").unwrap().len(), 2);
    assert_eq!(parts.get("kb:root-b").unwrap().len(), 1);
    assert!(parts.get("kb:root-a").unwrap().contains("kb:child-a"));
}

#[test]
fn test_partition_by_roots_reject_shared() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node("kb:shared", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("shared");
    graph
        .upsert_node("kb:root-a", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("root a");
    graph
        .upsert_node("kb:root-b", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("root b");
    graph
        .link("kb:root-a", "uco-core:relatedTo", "kb:shared")
        .expect("link a");
    graph
        .link("kb:root-b", "uco-core:relatedTo", "kb:shared")
        .expect("link b");

    let err = graph
        .partition_by_roots(
            &["kb:root-a".to_string(), "kb:root-b".to_string()],
            "reject",
        )
        .err()
        .expect("overlap should fail");
    assert!(err.to_string().contains("shared node"));
}

#[test]
fn test_partition_marking_boundary_fails_closed() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node(
            "kb:public-root",
            Some(serde_json::json!("uco-core:UcoObject")),
            serde_json::json!({
                "uco-core:objectMarking": {"@id": "kb:public-marking"},
                "uco-core:object": {"@id": "kb:protected"}
            })
            .as_object()
            .cloned(),
        )
        .expect("public root");
    graph
        .upsert_node(
            "kb:protected",
            Some(serde_json::json!("uco-core:UcoObject")),
            serde_json::json!({
                "uco-core:objectMarking": {"@id": "kb:secret-marking"}
            })
            .as_object()
            .cloned(),
        )
        .expect("protected");
    let options = PartitionOptions {
        include_incoming: false,
        boundary_policy: "marking-and-authorization".into(),
        ..PartitionOptions::default()
    };

    let error = graph
        .partition_by_roots_with_manifest(&["kb:public-root".into()], &options)
        .err()
        .expect("boundary must fail");
    match error {
        GraphError::PartitionBoundary {
            root_id,
            node_id,
            missing_markings,
            ..
        } => {
            assert_eq!(root_id, "kb:public-root");
            assert_eq!(node_id, "kb:protected");
            assert!(missing_markings.contains(&graph.expand_iri("kb:secret-marking")));
        }
        other => panic!("unexpected error: {other}"),
    }
}

#[test]
fn test_partition_home_route_preserves_union() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    for (id, properties) in [
        (
            "kb:public-root",
            serde_json::json!({
                "uco-core:objectMarking": {"@id": "kb:public-marking"},
                "uco-core:object": {"@id": "kb:protected"}
            }),
        ),
        (
            "kb:secret-root",
            serde_json::json!({
                "uco-core:objectMarking": [
                    {"@id": "kb:public-marking"},
                    {"@id": "kb:secret-marking"}
                ],
                "uco-core:object": {"@id": "kb:protected"}
            }),
        ),
        (
            "kb:protected",
            serde_json::json!({
                "uco-core:objectMarking": {"@id": "kb:secret-marking"},
                "uco-core:name": "protected evidence"
            }),
        ),
    ] {
        graph
            .upsert_node(
                id,
                Some(serde_json::json!("uco-core:UcoObject")),
                properties.as_object().cloned(),
            )
            .expect("node");
    }
    let mut root_boundaries = BTreeMap::new();
    root_boundaries.insert(
        "kb:public-root".into(),
        PartitionBoundary {
            markings: vec!["kb:public-marking".into()],
            authorizations: vec![],
        },
    );
    root_boundaries.insert(
        "kb:secret-root".into(),
        PartitionBoundary {
            markings: vec!["kb:public-marking".into(), "kb:secret-marking".into()],
            authorizations: vec![],
        },
    );
    let options = PartitionOptions {
        include_incoming: false,
        boundary_policy: "marking-and-authorization".into(),
        cross_boundary_policy: "home-partition-reference".into(),
        root_boundaries,
        validation_bundle: serde_json::json!({"extensions": ["example:full"]}),
        ..PartitionOptions::default()
    };

    let result = graph
        .partition_by_roots_with_manifest(
            &["kb:public-root".into(), "kb:secret-root".into()],
            &options,
        )
        .expect("partition");
    assert!(!result.partitions["kb:public-root"].contains("kb:protected"));
    assert!(result.partitions["kb:secret-root"].contains("kb:protected"));
    assert_eq!(
        result.manifest["validation_mode"],
        serde_json::json!("referenced-partition-set")
    );
    assert_eq!(
        result.manifest["home_partition_routes"]["kb:protected"],
        serde_json::json!("kb:secret-root")
    );
    assert!(graph.verify_partition_union(&result.partitions).equivalent);
}

#[test]
fn test_partition_support_graph_safe_manifest() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    graph
        .upsert_node("kb:shared", Some(serde_json::json!("uco-core:UcoObject")), None)
        .expect("shared");
    for root in ["kb:a", "kb:b"] {
        graph
            .upsert_node(
                root,
                Some(serde_json::json!("uco-core:UcoObject")),
                serde_json::json!({"uco-core:object": {"@id": "kb:shared"}})
                    .as_object()
                    .cloned(),
            )
            .expect("root");
    }
    let options = PartitionOptions {
        include_incoming: false,
        shared_node_policy: "support-graph".into(),
        manifest_detail: "safe".into(),
        ..PartitionOptions::default()
    };

    let result = graph
        .partition_by_roots_with_manifest(&["kb:a".into(), "kb:b".into()], &options)
        .expect("partition");
    assert!(result.partitions.contains_key("_support"));
    assert!(result.manifest["partitions"]["kb:a"].get("node_ids").is_none());
    assert!(graph.verify_partition_union(&result.partitions).equivalent);
}

#[test]
fn test_used_prefix_set_maintained_on_create() {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    let tool = Tool::builder()
        .tool_type("forensic".to_string())
        .version("1.0".to_string())
        .build();
    graph.create(&tool);

    let json = graph.serialize().expect("serialize");
    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    let ctx = parsed.get("@context").unwrap().as_object().unwrap();
    assert!(ctx.contains_key("uco-tool"));
    assert!(!ctx.contains_key("uco-identity"));
}
