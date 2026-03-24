//! CaseGraph — main entry point for building and serializing CASE/UCO graphs in Rust.

use serde::Serialize;
use serde_json::{json, Map, Value};
use std::collections::HashMap;
use uuid::Uuid;

/// Trait implemented by generated CASE/UCO types so that `CaseGraph::create`
/// can read the class IRI and type name without manual arguments.
pub trait CaseObject {
    fn class_iri() -> &'static str;
    fn type_name() -> &'static str;
}

/// Build a CASE/UCO JSON-LD graph with typed objects.
pub struct CaseGraph {
    context: HashMap<String, String>,
    objects: Vec<Value>,
    id_map: HashMap<String, String>,
}

impl CaseGraph {
    pub fn new(kb_prefix: &str) -> Self {
        let mut context = default_context();
        context.insert("kb".to_string(), kb_prefix.to_string());

        CaseGraph {
            context,
            objects: Vec::new(),
            id_map: HashMap::new(),
        }
    }

    pub fn add_context(&mut self, prefix: &str, iri: &str) {
        self.context.insert(prefix.to_string(), iri.to_string());
    }

    /// Add a generated CASE/UCO object to the graph. Returns the assigned @id.
    ///
    /// This is the preferred API — the type name and class IRI are read from
    /// the [`CaseObject`] trait that the code generator implements on every
    /// generated struct.
    pub fn create<T: CaseObject + Serialize>(&mut self, instance: &T) -> String {
        self.add(T::type_name(), T::class_iri(), instance)
    }

    /// Add a serializable object to the graph with explicit type info.
    /// Returns the assigned @id.
    pub fn add<T: Serialize>(&mut self, type_name: &str, class_iri: &str, instance: &T) -> String {
        let id = format!("kb:{}-{}", type_name, Uuid::new_v4());
        let compact_type = self.compact_iri(class_iri);

        let mut obj_value = serde_json::to_value(instance)
            .expect("failed to serialize object into JSON-LD value");
        obj_value = self.convert_value(obj_value);
        if let Value::Object(ref mut map) = obj_value {
            map.insert("@id".to_string(), Value::String(id.clone()));
            map.insert("@type".to_string(), Value::String(compact_type));
            map.remove("class_iri");
        }

        self.objects.push(obj_value);
        id
    }

    /// Retrieve the @id that was assigned to an object by a previous
    /// `create` / `add` call, looked up by the id string itself.
    pub fn get_id(&self, id: &str) -> Option<&String> {
        self.id_map.get(id)
    }

    /// Serialize the graph to a JSON-LD string.
    ///
    /// Returns `Err` if the internal structure cannot be serialized
    /// (should not happen under normal use).
    pub fn serialize(&self) -> Result<String, serde_json::Error> {
        let context_value: Map<String, Value> = self
            .context
            .iter()
            .map(|(k, v)| (k.clone(), Value::String(v.clone())))
            .collect();

        let doc = json!({
            "@context": context_value,
            "@graph": self.objects,
        });

        serde_json::to_string_pretty(&doc)
    }

    /// Write the graph to a file.
    pub fn write(&self, path: &str) -> std::io::Result<()> {
        let json = self.serialize().map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, e))?;
        std::fs::write(path, json)
    }

    fn compact_iri(&self, iri: &str) -> String {
        for (prefix, ns) in &self.context {
            if iri.starts_with(ns.as_str()) {
                return format!("{}:{}", prefix, &iri[ns.len()..]);
            }
        }
        iri.to_string()
    }

    fn convert_value(&self, value: Value) -> Value {
        match value {
            Value::Object(map) => {
                let converted: Map<String, Value> = map
                    .into_iter()
                    .map(|(k, v)| (k, self.convert_value(v)))
                    .collect();
                Value::Object(converted)
            }
            Value::Array(items) => {
                Value::Array(items.into_iter().map(|item| self.convert_value(item)).collect())
            }
            Value::Bool(boolean) => json!({
                "@type": "xsd:boolean",
                "@value": if boolean { "true" } else { "false" },
            }),
            Value::Number(number) => {
                if number.is_i64() || number.is_u64() {
                    json!({
                        "@type": "xsd:integer",
                        "@value": number.to_string(),
                    })
                } else {
                    json!({
                        "@type": "xsd:decimal",
                        "@value": number.to_string(),
                    })
                }
            }
            other => other,
        }
    }
}

fn default_context() -> HashMap<String, String> {
    let mut ctx = HashMap::new();
    ctx.insert("case-investigation".into(), "https://ontology.caseontology.org/case/investigation/".into());
    ctx.insert("kb".into(), "http://example.org/kb/".into());
    ctx.insert("uco-action".into(), "https://ontology.unifiedcyberontology.org/uco/action/".into());
    ctx.insert("uco-core".into(), "https://ontology.unifiedcyberontology.org/uco/core/".into());
    ctx.insert("uco-identity".into(), "https://ontology.unifiedcyberontology.org/uco/identity/".into());
    ctx.insert("uco-location".into(), "https://ontology.unifiedcyberontology.org/uco/location/".into());
    ctx.insert("uco-observable".into(), "https://ontology.unifiedcyberontology.org/uco/observable/".into());
    ctx.insert("uco-tool".into(), "https://ontology.unifiedcyberontology.org/uco/tool/".into());
    ctx.insert("uco-types".into(), "https://ontology.unifiedcyberontology.org/uco/types/".into());
    ctx.insert("uco-vocabulary".into(), "https://ontology.unifiedcyberontology.org/uco/vocabulary/".into());
    ctx.insert("xsd".into(), "http://www.w3.org/2001/XMLSchema#".into());
    ctx
}
