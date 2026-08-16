use case_uco::registry;
use std::sync::Mutex;

static REGISTRY_TEST_LOCK: Mutex<()> = Mutex::new(());

const EXTENSION: &str = r#"{
  "modules": ["ext.dynamic"],
  "classes": {
    "DynamicExtension": {
      "iri": "https://example.org/dynamic/DynamicExtension",
      "module": "ext.dynamic",
      "description": "Test extension",
      "parents": [],
      "is_facet": false,
      "properties": []
    }
  },
  "vocabs": {}
}"#;

#[test]
fn dynamic_extension_registry_invalidates_and_reports_metrics() {
    let _guard = REGISTRY_TEST_LOCK.lock().expect("registry test lock");
    let source = "rust-test-dynamic";
    registry::unregister_extension(source);
    let before = registry::cache_metrics();
    let generation = registry::register_extension_json(source, EXTENSION).expect("register");
    assert!(generation > before.generation);
    let class = registry::get_class("DynamicExtension").expect("dynamic class");
    assert_eq!(class.iri, "https://example.org/dynamic/DynamicExtension");
    let after = registry::cache_metrics();
    assert!(after.hits > before.hits);
    assert_eq!(after.registered_extensions, before.registered_extensions + 1);
    registry::unregister_extension(source);
    assert!(registry::get_class("DynamicExtension").is_none());
}

#[test]
fn dynamic_extension_registry_rejects_class_iri_conflict_atomically() {
    let _guard = REGISTRY_TEST_LOCK.lock().expect("registry test lock");
    registry::unregister_extension("rust-test-conflict");
    let tool = registry::get_class("Tool").expect("built-in Tool");
    let conflicting = serde_json::json!({
        "modules": ["ext.dynamic"],
        "classes": {
            "ConflictingTool": {
                "iri": tool.iri,
                "module": "ext.dynamic",
                "description": "Conflict",
                "parents": [],
                "is_facet": false,
                "properties": []
            }
        },
        "vocabs": {}
    })
    .to_string();
    let before = registry::cache_metrics();
    let error = registry::register_extension_json("rust-test-conflict", &conflicting)
        .expect_err("duplicate IRI must fail");
    assert!(error.to_string().contains("duplicate class IRI"));
    let after = registry::cache_metrics();
    assert_eq!(after.generation, before.generation);
    assert_eq!(after.registered_extensions, before.registered_extensions);
}
