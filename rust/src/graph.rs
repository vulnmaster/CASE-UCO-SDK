//! CaseGraph — main entry point for building and serializing CASE/UCO graphs in Rust.

use serde::Serialize;
use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashMap, HashSet, VecDeque};
use std::io::Write;
use uuid::Uuid;

const KIND_SLUG_MAX_LEN: usize = 64;

/// Named duplicate `@id` policies (parity with Python / C# / Java).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum DuplicatePolicy {
    #[default]
    Reject,
    MergeIdentical,
    MergeCompatible,
    Replace,
}

impl DuplicatePolicy {
    pub fn parse(name: &str) -> Result<Self, String> {
        match name {
            "reject" | "error" => Ok(Self::Reject),
            "merge_identical" => Ok(Self::MergeIdentical),
            "merge_compatible" => Ok(Self::MergeCompatible),
            "replace" => Ok(Self::Replace),
            other => Err(format!(
                "Unknown duplicate policy: '{other}'. Expected one of: reject, merge_identical, merge_compatible, replace (error is an alias for reject)"
            )),
        }
    }

    pub fn as_str(self) -> &'static str {
        match self {
            Self::Reject => "reject",
            Self::MergeIdentical => "merge_identical",
            Self::MergeCompatible => "merge_compatible",
            Self::Replace => "replace",
        }
    }
}

/// Raised when a node with the same `@id` conflicts with an existing node.
#[derive(Debug, Clone)]
pub struct DuplicateNodeError {
    pub node_id: String,
    pub detail: String,
}

impl std::fmt::Display for DuplicateNodeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Duplicate @id '{}'", self.node_id)?;
        if !self.detail.is_empty() {
            write!(f, ": {}", self.detail)?;
        }
        Ok(())
    }
}

impl std::error::Error for DuplicateNodeError {}

/// Graph composition and lookup errors.
#[derive(Debug)]
pub enum GraphError {
    Duplicate(DuplicateNodeError),
    NotFound(String),
    InvalidArgument(String),
    InvalidSplitSize(isize),
    PartitionBoundary {
        root_id: String,
        node_id: String,
        missing_markings: Vec<String>,
        missing_authorizations: Vec<String>,
    },
}

impl std::fmt::Display for GraphError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            GraphError::Duplicate(e) => write!(f, "{e}"),
            GraphError::NotFound(id) => write!(f, "No node with @id '{id}'"),
            GraphError::InvalidArgument(msg) => write!(f, "{msg}"),
            GraphError::InvalidSplitSize(n) => {
                write!(f, "split max_objects must be a positive integer, got {n}")
            }
            GraphError::PartitionBoundary {
                root_id,
                node_id,
                missing_markings,
                missing_authorizations,
            } => write!(
                f,
                "partition root '{root_id}' is not authorized for node '{node_id}'; missing markings={missing_markings:?}, missing authorizations={missing_authorizations:?}"
            ),
        }
    }
}

impl std::error::Error for GraphError {}

/// Errors from loading JSON-LD into a graph.
#[derive(Debug)]
pub enum LoadError {
    Json(serde_json::Error),
    Duplicate(DuplicateNodeError),
    Context(String),
    Merge(String),
    Policy(String),
}

impl std::fmt::Display for LoadError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LoadError::Json(e) => write!(f, "{e}"),
            LoadError::Duplicate(e) => write!(f, "{e}"),
            LoadError::Context(msg) | LoadError::Merge(msg) | LoadError::Policy(msg) => {
                write!(f, "{msg}")
            }
        }
    }
}

impl std::error::Error for LoadError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            LoadError::Json(e) => Some(e),
            LoadError::Duplicate(e) => Some(e),
            LoadError::Context(_) | LoadError::Merge(_) | LoadError::Policy(_) => None,
        }
    }
}

/// Trait implemented by generated CASE/UCO types so that `CaseGraph::create`
/// can read the class IRI and type name without manual arguments.
pub trait CaseObject {
    fn class_iri() -> &'static str;
    fn type_name() -> &'static str;
    /// Validate ontology-required fields. Returns `Ok(())` if all required
    /// fields are present, or `Err` with a message identifying the first
    /// missing field.
    fn validate(&self) -> Result<(), String> {
        Ok(())
    }
}

/// How overlapping dependency closures are handled in [`CaseGraph::partition_by_roots`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SharedPolicy {
    /// Copy shared nodes into every partition that references them.
    Duplicate,
    /// Fail if any node would appear in more than one partition closure.
    Reject,
    /// Assign each shared node only to the first root partition that reaches it.
    First,
    /// Put shared nodes into a dedicated support graph.
    Support,
}

impl SharedPolicy {
    fn parse(name: &str) -> Result<Self, GraphError> {
        match name {
            "duplicate" | "replicate-identical" => Ok(Self::Duplicate),
            "reject" | "error-on-cross-boundary" => Ok(Self::Reject),
            "first" | "home-partition-reference" => Ok(Self::First),
            "support-graph" | "shared" | "isolate-shared" | "_shared" => Ok(Self::Support),
            other => Err(GraphError::InvalidArgument(format!(
                "Unknown shared policy: '{other}'. Expected duplicate/replicate-identical, reject/error-on-cross-boundary, first/home-partition-reference, or support-graph"
            ))),
        }
    }
}

/// Metrics from an atomic/incremental streaming write (#71).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct StreamingWriteMetrics {
    pub nodes: usize,
    pub bytes_written: u64,
}

/// Marking and authorization scope allowed for one partition root (#79).
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct PartitionBoundary {
    pub markings: Vec<String>,
    pub authorizations: Vec<String>,
}

/// Options for marking-safe dependency partitioning (#79).
#[derive(Debug, Clone)]
pub struct PartitionOptions {
    pub shared_node_policy: String,
    pub include_incoming: bool,
    pub boundary_policy: String,
    pub cross_boundary_policy: String,
    pub root_boundaries: BTreeMap<String, PartitionBoundary>,
    pub validation_bundle: Value,
    pub manifest_detail: String,
}

impl Default for PartitionOptions {
    fn default() -> Self {
        Self {
            shared_node_policy: "replicate-identical".to_string(),
            include_incoming: true,
            boundary_policy: "none".to_string(),
            cross_boundary_policy: "error-on-cross-boundary".to_string(),
            root_boundaries: BTreeMap::new(),
            validation_bundle: Value::Null,
            manifest_detail: "full".to_string(),
        }
    }
}

/// A partition set plus its reconstruction and validation manifest.
pub struct PartitionResult {
    pub partitions: BTreeMap<String, CaseGraph>,
    pub manifest: Value,
}

/// Exact JSON-LD node-union verification evidence.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PartitionUnionVerification {
    pub equivalent: bool,
    pub source_nodes: usize,
    pub union_nodes: usize,
}

#[derive(Debug, Clone, Default)]
struct BoundarySets {
    markings: HashSet<String>,
    authorizations: HashSet<String>,
}

/// Build a CASE/UCO JSON-LD graph with typed objects.
pub struct CaseGraph {
    context: HashMap<String, String>,
    objects: Vec<Value>,
    iri_index: HashMap<String, usize>,
    /// Prefixes referenced by graph objects; maintained on create/add/load mutations (#71).
    used_prefix_set: HashSet<String>,
    /// Named duplicate policy (default [`DuplicatePolicy::Reject`]).
    pub on_duplicate: DuplicatePolicy,
}

impl CaseGraph {
    pub fn new(kb_prefix: &str) -> Self {
        let mut context = default_context();
        context.insert("kb".to_string(), kb_prefix.to_string());

        CaseGraph {
            context,
            objects: Vec::new(),
            iri_index: HashMap::new(),
            used_prefix_set: HashSet::new(),
            on_duplicate: DuplicatePolicy::Reject,
        }
    }

    /// Construct with extra context prefixes (rejects collisions with defaults).
    pub fn with_extra_context(
        kb_prefix: &str,
        extra: &HashMap<String, String>,
    ) -> Result<Self, LoadError> {
        let mut g = Self::new(kb_prefix);
        for (k, v) in extra {
            g.merge_context_entry(k, v)?;
        }
        Ok(g)
    }

    /// When true, [`load`](Self::load) raises on duplicate `@id` instead of merging.
    /// Prefer [`on_duplicate`](Self::on_duplicate) for full policy parity.
    pub fn reject_duplicates(&self) -> bool {
        matches!(self.on_duplicate, DuplicatePolicy::Reject)
    }

    pub fn set_reject_duplicates(&mut self, reject: bool) {
        self.on_duplicate = if reject {
            DuplicatePolicy::Reject
        } else {
            DuplicatePolicy::MergeCompatible
        };
    }

    pub fn add_context(&mut self, prefix: &str, iri: &str) -> Result<(), LoadError> {
        self.merge_context_entry(prefix, iri)
    }

    /// Add a generated CASE/UCO object to the graph, auto-generating a UUID-based @id.
    ///
    /// Panics if any ontology-required field is missing or serialization fails.
    pub fn create<T: CaseObject + Serialize>(&mut self, instance: &T) -> String {
        if let Err(msg) = instance.validate() {
            panic!("{}", msg);
        }
        let id = format!("kb:{}-{}", T::type_name(), Uuid::new_v4());
        self.add_with_id(&id, T::class_iri(), instance)
    }

    /// Add a generated CASE/UCO object with a user-supplied @id.
    pub fn create_with_id<T: CaseObject + Serialize>(&mut self, id: &str, instance: &T) -> String {
        if let Err(msg) = instance.validate() {
            panic!("{}", msg);
        }
        self.add_with_id(id, T::class_iri(), instance)
    }

    /// Add a serializable object to the graph with explicit type info.
    pub fn add<T: Serialize>(&mut self, type_name: &str, class_iri: &str, instance: &T) -> String {
        let id = format!("kb:{}-{}", type_name, Uuid::new_v4());
        self.add_with_id(&id, class_iri, instance)
    }

    /// Add a serializable object with a specific @id and class IRI.
    pub fn add_with_id<T: Serialize>(&mut self, id: &str, class_iri: &str, instance: &T) -> String {
        let compact_type = self.compact_iri(class_iri);

        let mut obj_value = match serde_json::to_value(instance) {
            Ok(v) => v,
            Err(e) => panic!("failed to serialize object into JSON-LD value: {e}"),
        };
        obj_value = self.convert_value(obj_value);
        if let Value::Object(ref mut map) = obj_value {
            map.insert("@id".to_string(), Value::String(id.to_string()));
            map.insert("@type".to_string(), Value::String(compact_type));
            map.remove("class_iri");
        }

        if let Err(e) = self.append_object(obj_value) {
            panic!("failed to add object: {e}");
        }
        id.to_string()
    }

    /// Expand a compact IRI using this graph's context.
    pub fn expand_iri(&self, node_id: &str) -> String {
        expand_compact_iri(node_id, &self.context)
    }

    /// Return true if a node with this `@id` (compact or expanded) exists.
    pub fn contains(&self, node_id: &str) -> bool {
        self.find_object_index(node_id).is_some()
    }

    /// Return an owned deep clone of the JSON-LD object for a node.
    pub fn get(&self, node_id: &str) -> Option<Map<String, Value>> {
        self.find_object_index(node_id)
            .and_then(|idx| self.objects[idx].as_object().cloned())
    }

    /// Create or update a JSON-LD node by `@id`.
    ///
    /// Returns an owned JSON [`Value`] clone (not a live internal map).
    pub fn upsert_node(
        &mut self,
        node_id: &str,
        types: Option<Value>,
        properties: Option<Map<String, Value>>,
    ) -> Result<Value, GraphError> {
        if let Some(idx) = self.find_object_index(node_id) {
            let obj = self.objects[idx]
                .as_object_mut()
                .ok_or_else(|| GraphError::InvalidArgument("indexed node must be object".into()))?;
            if let Some(types_val) = types {
                let merged = merge_types(obj.get("@type"), Some(types_val));
                obj.insert("@type".to_string(), normalize_type_value(merged));
            }
            if let Some(props) = properties {
                for (key, value) in props {
                    apply_property(obj, &key, value, node_id, PropertyMode::MergeCompatible)
                        .map_err(|ApplyError::Duplicate(d)| GraphError::Duplicate(d))?;
                }
            }
            let tracked = self.objects[idx].clone();
            self.track_prefixes_for(&tracked);
            return Ok(self.objects[idx].clone());
        }

        let mut obj = Map::new();
        obj.insert("@id".to_string(), Value::String(node_id.to_string()));
        if let Some(types_val) = types {
            obj.insert("@type".to_string(), normalize_type_value(types_val));
        }
        if let Some(props) = properties {
            for (key, value) in props {
                apply_property(&mut obj, &key, value, node_id, PropertyMode::MergeCompatible)
                    .map_err(|ApplyError::Duplicate(d)| GraphError::Duplicate(d))?;
            }
        }
        self.append_object(Value::Object(obj))
            .map_err(GraphError::Duplicate)?;
        let last = self
            .objects
            .last()
            .ok_or_else(|| GraphError::InvalidArgument("append produced empty graph".into()))?;
        Ok(last.clone())
    }

    fn track_prefixes_for(&mut self, node: &Value) {
        let context_keys: HashSet<&str> = self.context.keys().map(|k| k.as_str()).collect();
        collect_prefixes(node, &context_keys, &mut self.used_prefix_set);
    }

    /// Add an `rdf:type` to an existing node (same `@id`).
    pub fn add_type(&mut self, node_id: &str, type_iri: &str) -> Result<(), GraphError> {
        let idx = self
            .find_object_index(node_id)
            .ok_or_else(|| GraphError::NotFound(node_id.to_string()))?;
        let obj = self.objects[idx]
            .as_object_mut()
            .ok_or_else(|| GraphError::InvalidArgument("indexed node must be object".into()))?;
        let merged = merge_types(obj.get("@type"), Some(Value::String(type_iri.to_string())));
        obj.insert("@type".to_string(), normalize_type_value(merged));
        self.track_prefixes_for(&json!({ "@type": type_iri }));
        Ok(())
    }

    /// Add or merge a property on an existing node (`merge_compatible`).
    pub fn add_property(
        &mut self,
        node_id: &str,
        key: &str,
        value: Value,
    ) -> Result<(), GraphError> {
        let idx = self
            .find_object_index(node_id)
            .ok_or_else(|| GraphError::NotFound(node_id.to_string()))?;
        let obj = self.objects[idx]
            .as_object_mut()
            .ok_or_else(|| GraphError::InvalidArgument("indexed node must be object".into()))?;
        apply_property(obj, key, value.clone(), node_id, PropertyMode::MergeCompatible)
            .map_err(|ApplyError::Duplicate(d)| GraphError::Duplicate(d))?;
        self.track_prefixes_for(&json!({ key: value }));
        Ok(())
    }

    /// Replace a property value (`replace` mode / scalar overwrite).
    pub fn set_property(
        &mut self,
        node_id: &str,
        key: &str,
        value: Value,
    ) -> Result<(), GraphError> {
        let idx = self
            .find_object_index(node_id)
            .ok_or_else(|| GraphError::NotFound(node_id.to_string()))?;
        let obj = self.objects[idx]
            .as_object_mut()
            .ok_or_else(|| GraphError::InvalidArgument("indexed node must be object".into()))?;
        apply_property(obj, key, value.clone(), node_id, PropertyMode::Replace)
            .map_err(|ApplyError::Duplicate(d)| GraphError::Duplicate(d))?;
        self.track_prefixes_for(&json!({ key: value }));
        Ok(())
    }

    /// Add a direct property edge source --predicate--> target.
    pub fn link(
        &mut self,
        source_id: &str,
        predicate: &str,
        target_id: &str,
    ) -> Result<(), GraphError> {
        self.add_property(source_id, predicate, json!({ "@id": target_id }))
    }

    /// Create a `uco-core:Relationship` node with deterministic `@id`.
    ///
    /// Pass `relationship_id` (assertion discriminator) so identical
    /// source/target/kind assertions can coexist.
    pub fn create_relationship(
        &mut self,
        source_id: &str,
        target_id: &str,
        kind: &str,
        directional: bool,
        description: Option<&str>,
        relationship_id: Option<&str>,
    ) -> Result<Value, GraphError> {
        if !self.contains(source_id) {
            return Err(GraphError::InvalidArgument(format!(
                "Relationship source not in graph: {source_id}"
            )));
        }
        if !self.contains(target_id) {
            return Err(GraphError::InvalidArgument(format!(
                "Relationship target not in graph: {target_id}"
            )));
        }
        if kind.is_empty() {
            return Err(GraphError::InvalidArgument(
                "kindOfRelationship is required".into(),
            ));
        }

        let rel_id = match relationship_id {
            Some(id) => id.to_string(),
            None => self.deterministic_relationship_id(source_id, target_id, kind),
        };
        let mut props = Map::new();
        props.insert(
            "uco-core:source".to_string(),
            json!([{ "@id": source_id }]),
        );
        props.insert(
            "uco-core:target".to_string(),
            json!([{ "@id": target_id }]),
        );
        props.insert(
            "uco-core:kindOfRelationship".to_string(),
            Value::String(kind.to_string()),
        );
        props.insert(
            "uco-core:isDirectional".to_string(),
            json!({
                "@type": "xsd:boolean",
                "@value": if directional { "true" } else { "false" },
            }),
        );
        if let Some(desc) = description {
            props.insert(
                "uco-core:description".to_string(),
                Value::String(desc.to_string()),
            );
        }

        self.upsert_node(
            &rel_id,
            Some(Value::String("uco-core:Relationship".to_string())),
            Some(props),
        )
    }

    /// Return the number of objects in the graph.
    pub fn len(&self) -> usize {
        self.objects.len()
    }

    /// Return true if the graph contains no objects.
    pub fn is_empty(&self) -> bool {
        self.objects.is_empty()
    }

    /// Load a JSON-LD string into this graph (transactional).
    pub fn load(&mut self, json: &str) -> Result<(), LoadError> {
        self.load_with_policy(json, self.on_duplicate)
    }

    pub fn load_with_policy(
        &mut self,
        json: &str,
        policy: DuplicatePolicy,
    ) -> Result<(), LoadError> {
        let doc: Value = serde_json::from_str(json).map_err(LoadError::Json)?;
        let snapshot = self.snapshot();
        let result = (|| -> Result<(), LoadError> {
            if let Some(ctx) = doc.get("@context").and_then(|c| c.as_object()) {
                self.merge_context(ctx)?;
            }
            if let Some(arr) = doc.get("@graph").and_then(|g| g.as_array()) {
                for obj in arr {
                    self.ingest_raw_node(obj.clone(), policy)?;
                }
            }
            Ok(())
        })();
        if result.is_err() {
            self.restore(snapshot);
        }
        result
    }

    fn snapshot(&self) -> GraphSnapshot {
        GraphSnapshot {
            context: self.context.clone(),
            objects: self.objects.clone(),
            iri_index: self.iri_index.clone(),
            used_prefix_set: self.used_prefix_set.clone(),
        }
    }

    fn restore(&mut self, snap: GraphSnapshot) {
        self.context = snap.context;
        self.objects = snap.objects;
        self.iri_index = snap.iri_index;
        self.used_prefix_set = snap.used_prefix_set;
    }

    fn merge_context(&mut self, incoming: &Map<String, Value>) -> Result<(), LoadError> {
        for (k, v) in incoming {
            if let Some(s) = v.as_str() {
                self.merge_context_entry(k, s)?;
            }
        }
        Ok(())
    }

    fn merge_context_entry(&mut self, prefix: &str, ns: &str) -> Result<(), LoadError> {
        if let Some(existing) = self.context.get(prefix) {
            if existing != ns {
                return Err(LoadError::Context(format!(
                    "Context prefix collision for '{prefix}': existing '{existing}' vs incoming '{ns}'"
                )));
            }
        }
        self.context.insert(prefix.to_string(), ns.to_string());
        Ok(())
    }

    /// Read and load a JSON-LD file into this graph.
    pub fn load_file(&mut self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let json = std::fs::read_to_string(path)?;
        self.load(&json)?;
        Ok(())
    }

    /// Parse a JSON-LD string and return the graph with its objects.
    ///
    /// Since Rust lacks runtime reflection, objects are returned as raw
    /// [`serde_json::Value`] items rather than typed CASE/UCO structs. Multi-type
    /// `@type` arrays are preserved. Typed registry caching (Python #70) is N/A
    /// here — there is no process-wide class registry to warm; callers that need
    /// typed views should map `Value` items to generated types themselves.
    pub fn from_jsonld(json: &str) -> Result<(CaseGraph, Vec<Value>), String> {
        let doc: Value =
            serde_json::from_str(json).map_err(|e| format!("Failed to parse JSON: {e}"))?;

        let mut graph = CaseGraph::new("http://example.org/kb/");

        if let Some(ctx) = doc.get("@context").and_then(|c| c.as_object()) {
            graph.merge_context(ctx).map_err(|e| e.to_string())?;
        }

        let mut objects = Vec::new();
        if let Some(arr) = doc.get("@graph").and_then(|g| g.as_array()) {
            for obj in arr {
                graph
                    .ingest_raw_node(obj.clone(), graph.on_duplicate)
                    .map_err(|e| e.to_string())?;
                objects.push(obj.clone());
            }
        }

        Ok((graph, objects))
    }

    /// Serialize the graph to a JSON-LD string.
    pub fn serialize(&self) -> Result<String, serde_json::Error> {
        let doc = json!({
            "@context": self.pruned_context(),
            "@graph": self.objects,
        });

        serde_json::to_string_pretty(&doc)
    }

    /// Return a copy of the context containing only prefixes used in the graph (#71).
    fn pruned_context(&self) -> Map<String, Value> {
        let used = if self.used_prefix_set.is_empty() {
            self.used_prefixes()
        } else {
            self.used_prefix_set.clone()
        };
        self.context
            .iter()
            .filter(|(k, _)| used.contains(k.as_str()))
            .map(|(k, v)| (k.clone(), Value::String(v.clone())))
            .collect()
    }

    fn used_prefixes(&self) -> HashSet<String> {
        let mut prefixes = HashSet::new();
        let context_keys: HashSet<&str> = self.context.keys().map(|k| k.as_str()).collect();
        for obj in &self.objects {
            collect_prefixes(obj, &context_keys, &mut prefixes);
        }
        prefixes
    }

    /// Write the graph incrementally without materializing a second full document (#71).
    ///
    /// Writes through a temporary file and renames into place (atomic on rename-capable
    /// filesystems). Returns nodes written and UTF-8 bytes emitted.
    pub fn write_streaming(&self, path: &str) -> std::io::Result<StreamingWriteMetrics> {
        let target = std::path::Path::new(path);
        let parent = target.parent().unwrap_or_else(|| std::path::Path::new("."));
        std::fs::create_dir_all(parent)?;
        let tmp_path = parent.join(format!(
            ".casegraph-{}.jsonld.tmp",
            std::process::id()
        ));

        let write_result = (|| -> std::io::Result<u64> {
            let file = std::fs::File::create(&tmp_path)?;
            let mut writer = std::io::BufWriter::new(file);
            let ctx = self.pruned_context();
            let mut bytes_written: u64 = 0;

            let mut emit = |buf: &[u8]| -> std::io::Result<()> {
                writer.write_all(buf)?;
                bytes_written += buf.len() as u64;
                Ok(())
            };

            emit(b"{\n")?;
            emit(b"  \"@context\": ")?;
            {
                let ctx_bytes = serde_json::to_vec(&ctx).map_err(std::io::Error::other)?;
                emit(&ctx_bytes)?;
            }
            emit(b",\n  \"@graph\": [\n")?;

            for (i, obj) in self.objects.iter().enumerate() {
                emit(b"    ")?;
                let obj_bytes = serde_json::to_vec(obj).map_err(std::io::Error::other)?;
                emit(&obj_bytes)?;
                if i + 1 < self.objects.len() {
                    emit(b",\n")?;
                } else {
                    emit(b"\n")?;
                }
            }
            emit(b"  ]\n}\n")?;
            writer.flush()?;
            Ok(bytes_written)
        })();

        match write_result {
            Ok(bytes_written) => {
                std::fs::rename(&tmp_path, target)?;
                Ok(StreamingWriteMetrics {
                    nodes: self.objects.len(),
                    bytes_written,
                })
            }
            Err(e) => {
                let _ = std::fs::remove_file(&tmp_path);
                Err(e)
            }
        }
    }

    /// Write the graph to a file.
    pub fn write(&self, path: &str) -> std::io::Result<()> {
        let json = self.serialize().map_err(std::io::Error::other)?;
        std::fs::write(path, json)
    }

    /// Validate this graph against CASE/UCO SHACL constraints using `case_validate`.
    pub fn validate(&self, case_version: &str) -> Result<String, String> {
        use std::io::Write;
        let json = self
            .serialize()
            .map_err(|e| format!("Serialization failed: {e}"))?;
        let mut tmp = tempfile::NamedTempFile::new()
            .map_err(|e| format!("Failed to create temp file: {e}"))?;
        tmp.write_all(json.as_bytes())
            .map_err(|e| format!("Failed to write temp file: {e}"))?;
        let output = std::process::Command::new("case_validate")
            .arg("--built-version")
            .arg(case_version)
            .arg(tmp.path())
            .output()
            .map_err(|e| {
                format!("case_validate not found on PATH (pip install case-utils): {e}")
            })?;
        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            let stdout = String::from_utf8_lossy(&output.stdout);
            let msg = if stderr.is_empty() { stdout } else { stderr };
            return Err(format!("Validation failed:\n{}", msg.trim()));
        }
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }

    /// Estimate the number of RDF triples this graph will produce.
    pub fn estimate_triples(&self) -> usize {
        self.objects.iter().map(count_triples).sum()
    }

    /// Partition the graph into dependency closures rooted at ``roots`` (#72).
    ///
    /// Each root's partition includes the root node and every top-level node
    /// reachable by following nested ``@id`` references. ``shared_policy``
    /// controls overlap: ``duplicate`` copies shared nodes into each partition,
    /// ``reject`` fails on overlap, ``first`` assigns shared nodes only to the
    /// earliest root partition.
    pub fn partition_by_roots(
        &self,
        roots: &[String],
        shared_policy: &str,
    ) -> Result<BTreeMap<String, CaseGraph>, GraphError> {
        let options = PartitionOptions {
            shared_node_policy: shared_policy.to_string(),
            ..PartitionOptions::default()
        };
        Ok(self.partition_by_roots_with_manifest(roots, &options)?.partitions)
    }

    /// Marking-safe root partitioning with reconstruction metadata (#79).
    pub fn partition_by_roots_with_manifest(
        &self,
        roots: &[String],
        options: &PartitionOptions,
    ) -> Result<PartitionResult, GraphError> {
        if roots.is_empty() {
            return Err(GraphError::InvalidArgument(
                "partition_by_roots requires at least one root @id".into(),
            ));
        }
        let policy = SharedPolicy::parse(&options.shared_node_policy)?;
        if options.boundary_policy != "none"
            && options.boundary_policy != "marking-and-authorization"
        {
            return Err(GraphError::InvalidArgument(format!(
                "Unknown boundary policy: '{}'",
                options.boundary_policy
            )));
        }
        if options.cross_boundary_policy != "error-on-cross-boundary"
            && options.cross_boundary_policy != "home-partition-reference"
        {
            return Err(GraphError::InvalidArgument(format!(
                "Unknown cross-boundary policy: '{}'",
                options.cross_boundary_policy
            )));
        }
        if options.manifest_detail != "full" && options.manifest_detail != "safe" {
            return Err(GraphError::InvalidArgument(
                "manifest_detail must be 'full' or 'safe'".into(),
            ));
        }

        let by_id = self.top_level_index();
        let reverse = self.reverse_id_index(&by_id);
        let mut closures: BTreeMap<String, HashSet<String>> = BTreeMap::new();
        for root in roots {
            if !self.contains(root) {
                return Err(GraphError::NotFound(root.clone()));
            }
            closures.entry(root.clone()).or_insert_with(|| {
                self.dependency_closure_with_incoming(
                    root,
                    &by_id,
                    &reverse,
                    options.include_incoming,
                )
            });
        }

        let mut boundaries: HashMap<String, BoundarySets> = HashMap::new();
        for node in &self.objects {
            if let Some(id) = node.get("@id").and_then(Value::as_str) {
                boundaries.insert(self.expand_iri(id), self.partition_node_boundary(node));
            }
        }
        let mut declared: BTreeMap<String, BoundarySets> = BTreeMap::new();
        let mut omissions: BTreeMap<String, HashSet<String>> = closures
            .keys()
            .map(|root| (root.clone(), HashSet::new()))
            .collect();
        if options.boundary_policy == "marking-and-authorization" {
            for root in closures.keys() {
                let scope = if let Some(supplied) = options.root_boundaries.get(root) {
                    BoundarySets {
                        markings: supplied
                            .markings
                            .iter()
                            .map(|value| self.expand_iri(value))
                            .collect(),
                        authorizations: supplied
                            .authorizations
                            .iter()
                            .map(|value| self.expand_iri(value))
                            .collect(),
                    }
                } else {
                    boundaries
                        .get(&self.expand_iri(root))
                        .cloned()
                        .unwrap_or_default()
                };
                declared.insert(root.clone(), scope);
            }
            for (root, members) in &mut closures {
                let allowed = &declared[root];
                let mut ordered_members: Vec<String> = members.iter().cloned().collect();
                ordered_members.sort();
                for node_id in ordered_members {
                    let required = boundaries.get(&node_id).cloned().unwrap_or_default();
                    let mut missing_markings: Vec<String> = required
                        .markings
                        .difference(&allowed.markings)
                        .cloned()
                        .collect();
                    let mut missing_authorizations: Vec<String> = required
                        .authorizations
                        .difference(&allowed.authorizations)
                        .cloned()
                        .collect();
                    missing_markings.sort();
                    missing_authorizations.sort();
                    if missing_markings.is_empty() && missing_authorizations.is_empty() {
                        continue;
                    }
                    if self.expand_iri(root) == node_id
                        || options.cross_boundary_policy == "error-on-cross-boundary"
                    {
                        return Err(GraphError::PartitionBoundary {
                            root_id: root.clone(),
                            node_id: self.original_id_for(&node_id, &by_id),
                            missing_markings,
                            missing_authorizations,
                        });
                    }
                    members.remove(&node_id);
                    let omission_set = omissions.get_mut(root).ok_or_else(|| {
                        GraphError::InvalidArgument(
                            "internal partition omission root is missing".to_string(),
                        )
                    })?;
                    omission_set.insert(node_id);
                }
            }
        }

        let omitted: HashSet<String> = omissions
            .values()
            .flat_map(|values| values.iter().cloned())
            .collect();
        let mut boundary_homes: HashMap<String, String> = HashMap::new();
        let mut ordered_omitted: Vec<String> = omitted.iter().cloned().collect();
        ordered_omitted.sort();
        for node_id in ordered_omitted {
            let candidates: Vec<String> = closures
                .iter()
                .filter(|(_, members)| members.contains(&node_id))
                .map(|(root, _)| root.clone())
                .collect();
            let Some(home) = candidates.first() else {
                let required = boundaries.get(&node_id).cloned().unwrap_or_default();
                let mut missing_markings: Vec<String> = required.markings.into_iter().collect();
                let mut missing_authorizations: Vec<String> =
                    required.authorizations.into_iter().collect();
                missing_markings.sort();
                missing_authorizations.sort();
                return Err(GraphError::PartitionBoundary {
                    root_id: "<no-authorized-home>".into(),
                    node_id: self.original_id_for(&node_id, &by_id),
                    missing_markings,
                    missing_authorizations,
                });
            };
            boundary_homes.insert(node_id, home.clone());
        }

        let mut node_owners: HashMap<String, Vec<String>> = HashMap::new();
        for (root, members) in &closures {
            for node_id in members {
                node_owners.entry(node_id.clone()).or_default().push(root.clone());
            }
        }
        for owners in node_owners.values_mut() {
            owners.sort();
        }
        if policy == SharedPolicy::Reject {
            let mut overlap: Vec<String> = node_owners
                .iter()
                .filter(|(_, owners)| owners.len() > 1)
                .map(|(node_id, _)| node_id.clone())
                .collect();
            overlap.sort();
            if !overlap.is_empty() {
                return Err(GraphError::InvalidArgument(format!(
                    "shared nodes cross partition boundaries: {:?}",
                    overlap.into_iter().take(5).collect::<Vec<_>>()
                )));
            }
        }
        let mut homes: HashMap<String, String> = HashMap::new();
        if policy == SharedPolicy::First {
            for (node_id, owners) in &node_owners {
                if owners.len() > 1 {
                    let original = self.original_id_for(node_id, &by_id);
                    let home = if owners.contains(&original) {
                        original
                    } else {
                        owners[0].clone()
                    };
                    homes.insert(node_id.clone(), home);
                }
            }
        }

        let mut partitions: BTreeMap<String, CaseGraph> = BTreeMap::new();
        for (root, members) in &closures {
            let mut part = self.partition_shell();
            let mut ordered: Vec<String> = members.iter().cloned().collect();
            ordered.sort();
            for node_id in ordered {
                let owner_count = node_owners[&node_id].len();
                if owner_count > 1 && policy == SharedPolicy::Support {
                    continue;
                }
                if owner_count > 1
                    && policy == SharedPolicy::First
                    && homes.get(&node_id) != Some(root)
                {
                    continue;
                }
                if let Some(node) = self.resolve_top_level(&node_id, &by_id) {
                    part.append_object(node.clone()).map_err(GraphError::Duplicate)?;
                }
            }
            partitions.insert(root.clone(), part);
        }
        if policy == SharedPolicy::Support {
            let mut support = self.partition_shell();
            let mut shared: Vec<String> = node_owners
                .iter()
                .filter(|(_, owners)| owners.len() > 1)
                .map(|(node_id, _)| node_id.clone())
                .collect();
            shared.sort();
            for node_id in shared {
                if let Some(node) = self.resolve_top_level(&node_id, &by_id) {
                    support
                        .append_object(node.clone())
                        .map_err(GraphError::Duplicate)?;
                }
            }
            if !support.objects.is_empty() {
                let key = if options.shared_node_policy == "support-graph" {
                    "_support"
                } else {
                    "_shared"
                };
                partitions.insert(key.into(), support);
            }
        }

        let mut partition_metadata = Map::new();
        for (key, partition) in &partitions {
            let hash = partition.graph_fingerprint(&partition.objects);
            let mut metadata = Map::new();
            metadata.insert("partition_id".into(), json!(format!("urn:sha256:{hash}")));
            metadata.insert("node_count".into(), json!(partition.objects.len()));
            metadata.insert("triple_estimate".into(), json!(partition.estimate_triples()));
            metadata.insert("sha256".into(), json!(hash));
            let scope = declared.get(key).cloned().unwrap_or_default();
            metadata.insert("effective_markings".into(), json!(sorted_set(&scope.markings)));
            metadata.insert(
                "authorization_scope".into(),
                json!(sorted_set(&scope.authorizations)),
            );
            if options.manifest_detail == "full" {
                let mut ids: Vec<String> = partition
                    .objects
                    .iter()
                    .filter_map(|node| node.get("@id").and_then(Value::as_str).map(str::to_string))
                    .collect();
                ids.sort();
                metadata.insert("node_ids".into(), json!(ids));
            }
            partition_metadata.insert(key.clone(), Value::Object(metadata));
        }
        let mut routes = BTreeMap::new();
        for (node_id, root) in homes.iter().chain(boundary_homes.iter()) {
            routes.insert(self.original_id_for(node_id, &by_id), root.clone());
        }
        let omission_counts: BTreeMap<String, usize> = omissions
            .iter()
            .map(|(root, values)| (root.clone(), values.len()))
            .collect();
        let required: Vec<String> = partitions.keys().cloned().collect();
        let source_hash = self.graph_fingerprint(&self.objects);
        let referenced = policy == SharedPolicy::Support
            || policy == SharedPolicy::First
            || !omitted.is_empty();
        let manifest = json!({
            "schema_version": "2.0.0",
            "dataset_id": format!("urn:sha256:{source_hash}"),
            "source_graph_sha256": source_hash,
            "strategy": if options.include_incoming { "outgoing_and_incoming_id_closure" } else { "outgoing_id_closure" },
            "roots": closures.keys().cloned().collect::<Vec<_>>(),
            "shared_node_policy": match policy {
                SharedPolicy::Duplicate => "replicate-identical",
                SharedPolicy::Reject => "error-on-cross-boundary",
                SharedPolicy::First => "home-partition-reference",
                SharedPolicy::Support => "support-graph",
            },
            "include_incoming": options.include_incoming,
            "boundary_policy": options.boundary_policy,
            "cross_boundary_policy": options.cross_boundary_policy,
            "validation_mode": if referenced { "referenced-partition-set" } else { "self-contained" },
            "validation_bundle": options.validation_bundle,
            "partitions": Value::Object(partition_metadata),
            "home_partition_routes": if options.manifest_detail == "full" { json!(routes) } else { json!({}) },
            "home_partition_route_count": routes.len(),
            "boundary_omission_counts": omission_counts,
            "reconstruction": {
                "operation": "rdf-union",
                "deduplicate_by": "@id with identical assertions",
                "requires_partitions": required,
            }
        });
        Ok(PartitionResult { partitions, manifest })
    }

    /// Verify that the exact JSON-LD node union reconstructs this graph.
    pub fn verify_partition_union(
        &self,
        partitions: &BTreeMap<String, CaseGraph>,
    ) -> PartitionUnionVerification {
        let mut source: BTreeMap<String, Value> = BTreeMap::new();
        for node in &self.objects {
            if let Some(id) = node.get("@id").and_then(Value::as_str) {
                source.insert(self.expand_iri(id), node.clone());
            }
        }
        let mut union: BTreeMap<String, Value> = BTreeMap::new();
        let mut conflict = false;
        for partition in partitions.values() {
            for node in &partition.objects {
                if let Some(id) = node.get("@id").and_then(Value::as_str) {
                    let expanded = self.expand_iri(id);
                    if let Some(existing) = union.get(&expanded) {
                        if existing != node {
                            conflict = true;
                        }
                    } else {
                        union.insert(expanded, node.clone());
                    }
                }
            }
        }
        PartitionUnionVerification {
            equivalent: !conflict && source == union,
            source_nodes: source.len(),
            union_nodes: union.len(),
        }
    }

    /// Split the graph into smaller chunks of at most `max_objects` each.
    pub fn split(&self, max_objects: usize) -> Result<Vec<CaseGraph>, GraphError> {
        if max_objects == 0 {
            return Err(GraphError::InvalidSplitSize(0));
        }
        let mut parts = Vec::new();
        for chunk in self.objects.chunks(max_objects) {
            let mut part = CaseGraph {
                context: self.context.clone(),
                objects: Vec::new(),
                iri_index: HashMap::new(),
                used_prefix_set: HashSet::new(),
                on_duplicate: self.on_duplicate,
            };
            for obj in chunk {
                part.append_object(obj.clone())
                    .map_err(GraphError::Duplicate)?;
            }
            parts.push(part);
        }
        Ok(parts)
    }

    /// Load and merge multiple JSON-LD files into a single graph.
    pub fn merge_files(
        paths: &[&str],
        kb_prefix: &str,
    ) -> Result<CaseGraph, Box<dyn std::error::Error>> {
        let mut merged = CaseGraph::new(kb_prefix);
        for path in paths {
            merged.load_file(path)?;
        }
        Ok(merged)
    }

    fn compact_iri(&self, iri: &str) -> String {
        for (prefix, ns) in &self.context {
            if iri.starts_with(ns.as_str()) {
                return format!("{}:{}", prefix, &iri[ns.len()..]);
            }
        }
        iri.to_string()
    }

    fn top_level_index(&self) -> HashMap<String, usize> {
        let mut by_id = HashMap::new();
        for (idx, obj) in self.objects.iter().enumerate() {
            if let Some(oid) = obj.get("@id").and_then(|v| v.as_str()) {
                by_id.insert(oid.to_string(), idx);
                let expanded = self.expand_iri(oid);
                if expanded != oid {
                    by_id.insert(expanded, idx);
                }
            }
        }
        by_id
    }

    fn partition_shell(&self) -> CaseGraph {
        CaseGraph {
            context: self.context.clone(),
            objects: Vec::new(),
            iri_index: HashMap::new(),
            used_prefix_set: HashSet::new(),
            on_duplicate: DuplicatePolicy::MergeCompatible,
        }
    }

    fn reverse_id_index(
        &self,
        by_id: &HashMap<String, usize>,
    ) -> HashMap<String, HashSet<String>> {
        let mut reverse: HashMap<String, HashSet<String>> = HashMap::new();
        for node in &self.objects {
            let Some(owner) = node.get("@id").and_then(Value::as_str) else {
                continue;
            };
            let owner = self.expand_iri(owner);
            let mut refs = HashSet::new();
            collect_nested_id_refs(node, &mut refs);
            for referenced in refs {
                let expanded = self.expand_iri(&referenced);
                if expanded != owner && by_id.contains_key(&expanded) {
                    reverse.entry(expanded).or_default().insert(owner.clone());
                }
            }
        }
        reverse
    }

    fn dependency_closure_with_incoming(
        &self,
        root: &str,
        by_id: &HashMap<String, usize>,
        reverse: &HashMap<String, HashSet<String>>,
        include_incoming: bool,
    ) -> HashSet<String> {
        let mut closure = HashSet::new();
        let mut queue = VecDeque::new();
        queue.push_back(self.expand_iri(root));
        while let Some(id) = queue.pop_front() {
            if !closure.insert(id.clone()) {
                continue;
            }
            let Some(node) = self.resolve_top_level(&id, by_id) else {
                continue;
            };
            let mut refs = HashSet::new();
            collect_nested_id_refs(node, &mut refs);
            for referenced in refs {
                let expanded = self.expand_iri(&referenced);
                if by_id.contains_key(&expanded) && !closure.contains(&expanded) {
                    queue.push_back(expanded);
                }
            }
            if include_incoming {
                if let Some(referrers) = reverse.get(&id) {
                    for referrer in referrers {
                        if !closure.contains(referrer) {
                            queue.push_back(referrer.clone());
                        }
                    }
                }
            }
        }
        closure
    }

    fn partition_node_boundary(&self, node: &Value) -> BoundarySets {
        fn collect(graph: &CaseGraph, value: &Value, output: &mut HashSet<String>) {
            match value {
                Value::String(text) => {
                    output.insert(graph.expand_iri(text));
                }
                Value::Object(map) => {
                    if let Some(id) = map.get("@id").and_then(Value::as_str) {
                        output.insert(graph.expand_iri(id));
                    }
                }
                Value::Array(values) => {
                    for value in values {
                        collect(graph, value, output);
                    }
                }
                _ => {}
            }
        }

        let mut result = BoundarySets::default();
        let Some(map) = node.as_object() else {
            return result;
        };
        for (key, value) in map {
            let expanded = self.expand_iri(key);
            let local = expanded
                .rsplit(['/', '#'])
                .next()
                .unwrap_or(expanded.as_str());
            if local == "objectMarking" {
                collect(self, value, &mut result.markings);
            } else if local == "relevantAuthorization" || local == "requiredAuthorization" {
                collect(self, value, &mut result.authorizations);
            }
        }
        result
    }

    fn original_id_for(&self, node_id: &str, by_id: &HashMap<String, usize>) -> String {
        self.resolve_top_level(node_id, by_id)
            .and_then(|node| node.get("@id"))
            .and_then(Value::as_str)
            .unwrap_or(node_id)
            .to_string()
    }

    fn graph_fingerprint(&self, nodes: &[Value]) -> String {
        let context: BTreeMap<&String, &String> = self.context.iter().collect();
        let document = json!({"@context": context, "@graph": nodes});
        let encoded = document.to_string().into_bytes();
        Sha256::digest(encoded)
            .iter()
            .map(|byte| format!("{byte:02x}"))
            .collect()
    }

    fn resolve_top_level<'a>(
        &'a self,
        node_id: &str,
        by_id: &HashMap<String, usize>,
    ) -> Option<&'a Value> {
        if let Some(&idx) = by_id.get(node_id) {
            return Some(&self.objects[idx]);
        }
        let expanded = self.expand_iri(node_id);
        by_id.get(&expanded).map(|&idx| &self.objects[idx])
    }

    fn append_object(&mut self, obj: Value) -> Result<(), DuplicateNodeError> {
        let node_id = obj
            .as_object()
            .and_then(|map| map.get("@id"))
            .and_then(|id| id.as_str())
            .map(str::to_string);

        if let Some(ref id) = node_id {
            if self.find_object_index(id).is_some() {
                return Err(DuplicateNodeError {
                    node_id: id.clone(),
                    detail: "use add_type/upsert_node or merge-compatible load instead of appending a second node".into(),
                });
            }
        }

        self.objects.push(obj);
        let idx = self.objects.len() - 1;
        if let Some(id) = node_id {
            self.index_node(&id, idx);
        }
        let tracked = self.objects[idx].clone();
        self.track_prefixes_for(&tracked);
        Ok(())
    }

    fn index_node(&mut self, node_id: &str, index: usize) {
        let expanded = self.expand_iri(node_id);
        self.iri_index.insert(expanded, index);
    }

    fn find_object_index(&self, node_id: &str) -> Option<usize> {
        let expanded = self.expand_iri(node_id);
        self.iri_index
            .get(&expanded)
            .copied()
            .filter(|index| *index < self.objects.len())
    }

    fn ingest_raw_node(&mut self, raw: Value, policy: DuplicatePolicy) -> Result<(), LoadError> {
        let node_id = raw
            .as_object()
            .and_then(|map| map.get("@id"))
            .and_then(|id| id.as_str())
            .map(str::to_string);

        let Some(node_id) = node_id else {
            self.objects.push(raw);
            if let Some(node) = self.objects.last().cloned() {
                self.track_prefixes_for(&node);
            }
            return Ok(());
        };

        if let Some(idx) = self.find_object_index(&node_id) {
            match policy {
                DuplicatePolicy::Reject => {
                    return Err(LoadError::Duplicate(DuplicateNodeError {
                        node_id,
                        detail: "conflicting duplicate during load".into(),
                    }));
                }
                DuplicatePolicy::Replace => {
                    let existing = self.objects[idx].as_object_mut().ok_or_else(|| {
                        LoadError::Merge("indexed node must be object".into())
                    })?;
                    let preserved = existing
                        .get("@id")
                        .cloned()
                        .unwrap_or_else(|| Value::String(node_id.clone()));
                    existing.clear();
                    if let Some(raw_map) = raw.as_object() {
                        for (k, v) in raw_map {
                            existing.insert(k.clone(), v.clone());
                        }
                    }
                    existing.insert("@id".to_string(), preserved);
                    self.track_prefixes_for(&raw);
                    return Ok(());
                }
                DuplicatePolicy::MergeIdentical => {
                    let existing = self.objects[idx].as_object_mut().ok_or_else(|| {
                        LoadError::Merge("indexed node must be object".into())
                    })?;
                    if let Some(raw_map) = raw.as_object() {
                        for (key, value) in raw_map {
                            if key == "@id" {
                                continue;
                            }
                            if !existing.contains_key(key) {
                                existing.insert(key.clone(), value.clone());
                                continue;
                            }
                            if !jsonld_values_equal(existing.get(key), Some(value)) {
                                return Err(LoadError::Duplicate(DuplicateNodeError {
                                    node_id,
                                    detail: format!(
                                        "merge_identical conflict on '{key}': existing and incoming values differ"
                                    ),
                                }));
                            }
                        }
                    }
                    self.track_prefixes_for(&raw);
                    return Ok(());
                }
                DuplicatePolicy::MergeCompatible => {
                    let existing = self.objects[idx].as_object_mut().ok_or_else(|| {
                        LoadError::Merge("indexed node must be object".into())
                    })?;
                    if let Some(types) = raw.get("@type") {
                        let merged = merge_types(existing.get("@type"), Some(types.clone()));
                        existing.insert("@type".to_string(), normalize_type_value(merged));
                    }
                    if let Some(raw_map) = raw.as_object() {
                        for (key, value) in raw_map {
                            if key == "@id" || key == "@type" {
                                continue;
                            }
                            apply_property(
                                existing,
                                key,
                                value.clone(),
                                &node_id,
                                PropertyMode::MergeCompatible,
                            )
                            .map_err(|ApplyError::Duplicate(d)| LoadError::Duplicate(d))?;
                        }
                    }
                    self.track_prefixes_for(&raw);
                    return Ok(());
                }
            }
        }

        self.append_object(raw).map_err(LoadError::Duplicate)
    }

    fn deterministic_relationship_id(&self, source_id: &str, target_id: &str, kind: &str) -> String {
        let payload = format!(
            "{}|{}|{}",
            self.expand_iri(source_id),
            self.expand_iri(target_id),
            kind
        );
        let digest = Sha256::digest(payload.as_bytes());
        let hex: String = digest.iter().take(6).map(|b| format!("{b:02x}")).collect();
        let safe_kind = safe_kind_slug(kind);
        format!("kb:rel-{safe_kind}-{hex}")
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

struct GraphSnapshot {
    context: HashMap<String, String>,
    objects: Vec<Value>,
    iri_index: HashMap<String, usize>,
    used_prefix_set: HashSet<String>,
}

#[derive(Clone, Copy)]
enum PropertyMode {
    MergeCompatible,
    Replace,
}

enum ApplyError {
    Duplicate(DuplicateNodeError),
}

fn apply_property(
    obj: &mut Map<String, Value>,
    key: &str,
    value: Value,
    node_id: &str,
    mode: PropertyMode,
) -> Result<(), ApplyError> {
    match mode {
        PropertyMode::Replace => {
            obj.insert(key.to_string(), value);
            Ok(())
        }
        PropertyMode::MergeCompatible => {
            if !obj.contains_key(key) {
                obj.insert(key.to_string(), value);
                return Ok(());
            }
            let existing = match obj.get(key) {
                Some(v) => v.clone(),
                None => Value::Null,
            };
            if jsonld_values_equal(Some(&existing), Some(&value)) {
                return Ok(());
            }
            if let Value::Array(mut list) = existing.clone() {
                accumulate_list_value(&mut list, value);
                obj.insert(key.to_string(), Value::Array(list));
                return Ok(());
            }
            if let Value::Array(_) = &value {
                let mut merged = vec![existing];
                accumulate_list_value(&mut merged, value);
                obj.insert(key.to_string(), Value::Array(merged));
                return Ok(());
            }
            // Distinct JSON-LD node references are multi-valued, not scalar conflicts.
            if let (Value::Object(eo), Value::Object(vo)) = (&existing, &value) {
                if eo.contains_key("@id") && vo.contains_key("@id") {
                    if jsonld_values_equal(Some(&existing), Some(&value)) {
                        return Ok(());
                    }
                    obj.insert(
                        key.to_string(),
                        Value::Array(vec![existing, value]),
                    );
                    return Ok(());
                }
            }
            Err(ApplyError::Duplicate(DuplicateNodeError {
                node_id: node_id.to_string(),
                detail: format!(
                    "merge_compatible scalar conflict on '{key}': existing and incoming values differ"
                ),
            }))
        }
    }
}

fn accumulate_list_value(existing: &mut Vec<Value>, value: Value) {
    let items = match value {
        Value::Array(arr) => arr,
        other => vec![other],
    };
    for item in items {
        if existing.iter().any(|x| jsonld_values_equal(Some(x), Some(&item))) {
            continue;
        }
        existing.push(item);
    }
}

fn jsonld_values_equal(a: Option<&Value>, b: Option<&Value>) -> bool {
    match (a, b) {
        (None, None) => true,
        (Some(a), Some(b)) => values_equal(a, b),
        _ => false,
    }
}

fn values_equal(a: &Value, b: &Value) -> bool {
    match (a, b) {
        (Value::Object(ao), Value::Object(bo)) => {
            if ao.contains_key("@value") || bo.contains_key("@value") {
                if !(ao.contains_key("@value") && bo.contains_key("@value")) {
                    return false;
                }
                let at = normalize_literal_type(ao.get("@type").and_then(|v| v.as_str()));
                let bt = normalize_literal_type(bo.get("@type").and_then(|v| v.as_str()));
                let av = normalize_literal_value(
                    ao.get("@value"),
                    ao.get("@type").and_then(|v| v.as_str()),
                );
                let bv = normalize_literal_value(
                    bo.get("@value"),
                    bo.get("@type").and_then(|v| v.as_str()),
                );
                return at == bt && av == bv;
            }
            if ao.contains_key("@id") || bo.contains_key("@id") {
                return ao.get("@id") == bo.get("@id");
            }
            if ao.len() != bo.len() {
                return false;
            }
            ao.iter()
                .all(|(k, v)| bo.get(k).is_some_and(|bv| values_equal(v, bv)))
        }
        (Value::Array(aa), Value::Array(ba)) => {
            if is_id_ref_list(aa) && is_id_ref_list(ba) {
                let mut asort: Vec<&str> = aa
                    .iter()
                    .filter_map(|v| v.get("@id").and_then(|i| i.as_str()))
                    .collect();
                let mut bsort: Vec<&str> = ba
                    .iter()
                    .filter_map(|v| v.get("@id").and_then(|i| i.as_str()))
                    .collect();
                asort.sort_unstable();
                bsort.sort_unstable();
                return asort == bsort;
            }
            if aa.len() != ba.len() {
                return false;
            }
            aa.iter().zip(ba.iter()).all(|(x, y)| values_equal(x, y))
        }
        _ => a == b,
    }
}

fn normalize_literal_type(type_iri: Option<&str>) -> String {
    match type_iri {
        None => String::new(),
        Some(t) if t.starts_with("xsd:") => t.to_string(),
        Some(t) if t.starts_with("http://www.w3.org/2001/XMLSchema#") => {
            format!("xsd:{}", t.rsplit('#').next().unwrap_or(""))
        }
        Some(t) => t.to_string(),
    }
}

fn normalize_literal_value(value: Option<&Value>, type_iri: Option<&str>) -> String {
    match value {
        Some(Value::Bool(b)) => {
            if *b {
                "true".into()
            } else {
                "false".into()
            }
        }
        Some(Value::String(s)) => {
            let t = normalize_literal_type(type_iri);
            if t.contains("boolean") {
                s.to_lowercase()
            } else {
                s.clone()
            }
        }
        Some(other) => other.to_string(),
        None => String::new(),
    }
}

fn is_id_ref_list(items: &[Value]) -> bool {
    !items.is_empty() && items.iter().all(|v| v.get("@id").is_some())
}

fn safe_kind_slug(kind: &str) -> String {
    let mut slug = String::new();
    for ch in kind.trim().chars() {
        if ch.is_ascii_alphanumeric() || ch == '.' || ch == '_' || ch == '-' {
            slug.push(ch);
        } else {
            slug.push('_');
        }
    }
    let slug = slug.trim_matches(|c| c == '.' || c == '_' || c == '-').to_string();
    let mut slug = if slug.is_empty() {
        "rel".to_string()
    } else {
        slug
    };
    if slug.len() > KIND_SLUG_MAX_LEN {
        slug.truncate(KIND_SLUG_MAX_LEN);
        while slug.ends_with(['.', '_', '-']) {
            slug.pop();
        }
        if slug.is_empty() {
            slug = "rel".into();
        }
    }
    slug
}

fn expand_compact_iri(compact: &str, context: &HashMap<String, String>) -> String {
    if compact.contains("://") {
        return compact.to_string();
    }
    if let Some(colon) = compact.find(':') {
        if colon > 0 {
            let prefix = &compact[..colon];
            if let Some(ns) = context.get(prefix) {
                return format!("{}{}", ns, &compact[colon + 1..]);
            }
        }
    }
    compact.to_string()
}

fn as_type_list(types: Option<&Value>) -> Vec<String> {
    match types {
        None => Vec::new(),
        Some(Value::String(s)) => vec![s.clone()],
        Some(Value::Array(arr)) => arr
            .iter()
            .filter_map(|v| v.as_str().map(str::to_string))
            .collect(),
        Some(other) => vec![other.to_string()],
    }
}

fn normalize_type_value(types: Value) -> Value {
    match types {
        Value::Array(arr) if arr.len() == 1 => arr
            .into_iter()
            .next()
            .unwrap_or(Value::Null),
        other => other,
    }
}

fn merge_types(existing: Option<&Value>, new_types: Option<Value>) -> Value {
    let mut merged = as_type_list(existing);
    for type_iri in as_type_list(new_types.as_ref()) {
        if !merged.contains(&type_iri) {
            merged.push(type_iri);
        }
    }
    if merged.len() == 1 {
        Value::String(merged[0].clone())
    } else {
        Value::Array(merged.into_iter().map(Value::String).collect())
    }
}

fn count_triples(value: &Value) -> usize {
    match value {
        Value::Object(map) => {
            let mut count = 0;
            for (key, val) in map {
                if key == "@id" {
                    continue;
                }
                if key == "@type" {
                    count += match val {
                        Value::Array(items) => items.len(),
                        _ => 1,
                    };
                    continue;
                }
                match val {
                    Value::Array(items) => {
                        for item in items {
                            if item.is_object() {
                                let obj = item.as_object();
                                let is_ref_or_literal = obj.is_some_and(|m| {
                                    m.contains_key("@value")
                                        || (m.contains_key("@id") && m.len() == 1)
                                });
                                if is_ref_or_literal {
                                    count += 1;
                                } else {
                                    count += 1 + count_triples(item);
                                }
                            } else {
                                count += 1;
                            }
                        }
                    }
                    Value::Object(inner) => {
                        if inner.contains_key("@value")
                            || (inner.contains_key("@id") && inner.len() == 1)
                        {
                            count += 1;
                        } else {
                            count += 1 + count_triples(val);
                        }
                    }
                    _ => {
                        count += 1;
                    }
                }
            }
            count
        }
        _ => 0,
    }
}

fn collect_nested_id_refs(value: &Value, out: &mut HashSet<String>) {
    match value {
        Value::Object(map) => {
            if let Some(id) = map.get("@id").and_then(|v| v.as_str()) {
                out.insert(id.to_string());
            }
            for val in map.values() {
                collect_nested_id_refs(val, out);
            }
        }
        Value::Array(items) => {
            for item in items {
                collect_nested_id_refs(item, out);
            }
        }
        _ => {}
    }
}

fn extract_prefix<'a>(value: &'a str, context_keys: &HashSet<&str>) -> Option<&'a str> {
    if value.contains("://") {
        return None;
    }
    if let Some(colon) = value.find(':') {
        if colon > 0 {
            let prefix = &value[..colon];
            if context_keys.contains(prefix) {
                return Some(prefix);
            }
        }
    }
    None
}

fn collect_prefixes(value: &Value, context_keys: &HashSet<&str>, out: &mut HashSet<String>) {
    match value {
        Value::Object(map) => {
            for (key, val) in map {
                if let Some(p) = extract_prefix(key, context_keys) {
                    out.insert(p.to_string());
                }
                if let Some(s) = val.as_str() {
                    if let Some(p) = extract_prefix(s, context_keys) {
                        out.insert(p.to_string());
                    }
                } else {
                    collect_prefixes(val, context_keys, out);
                }
            }
        }
        Value::Array(items) => {
            for item in items {
                if let Some(s) = item.as_str() {
                    if let Some(p) = extract_prefix(s, context_keys) {
                        out.insert(p.to_string());
                    }
                } else {
                    collect_prefixes(item, context_keys, out);
                }
            }
        }
        _ => {}
    }
}

fn sorted_set(values: &HashSet<String>) -> Vec<String> {
    let mut result: Vec<String> = values.iter().cloned().collect();
    result.sort();
    result
}

fn default_context() -> HashMap<String, String> {
    let mut ctx = HashMap::new();
    ctx.insert(
        "case-investigation".into(),
        "https://ontology.caseontology.org/case/investigation/".into(),
    );
    ctx.insert("kb".into(), "http://example.org/kb/".into());
    ctx.insert(
        "uco-action".into(),
        "https://ontology.unifiedcyberontology.org/uco/action/".into(),
    );
    ctx.insert(
        "uco-analysis".into(),
        "https://ontology.unifiedcyberontology.org/uco/analysis/".into(),
    );
    ctx.insert(
        "uco-configuration".into(),
        "https://ontology.unifiedcyberontology.org/uco/configuration/".into(),
    );
    ctx.insert(
        "uco-core".into(),
        "https://ontology.unifiedcyberontology.org/uco/core/".into(),
    );
    ctx.insert(
        "uco-identity".into(),
        "https://ontology.unifiedcyberontology.org/uco/identity/".into(),
    );
    ctx.insert(
        "uco-location".into(),
        "https://ontology.unifiedcyberontology.org/uco/location/".into(),
    );
    ctx.insert(
        "uco-marking".into(),
        "https://ontology.unifiedcyberontology.org/uco/marking/".into(),
    );
    ctx.insert(
        "uco-observable".into(),
        "https://ontology.unifiedcyberontology.org/uco/observable/".into(),
    );
    ctx.insert(
        "uco-pattern".into(),
        "https://ontology.unifiedcyberontology.org/uco/pattern/".into(),
    );
    ctx.insert(
        "uco-role".into(),
        "https://ontology.unifiedcyberontology.org/uco/role/".into(),
    );
    ctx.insert(
        "uco-time".into(),
        "https://ontology.unifiedcyberontology.org/uco/time/".into(),
    );
    ctx.insert(
        "uco-tool".into(),
        "https://ontology.unifiedcyberontology.org/uco/tool/".into(),
    );
    ctx.insert(
        "uco-types".into(),
        "https://ontology.unifiedcyberontology.org/uco/types/".into(),
    );
    ctx.insert(
        "uco-victim".into(),
        "https://ontology.unifiedcyberontology.org/uco/victim/".into(),
    );
    ctx.insert(
        "uco-vocabulary".into(),
        "https://ontology.unifiedcyberontology.org/uco/vocabulary/".into(),
    );
    ctx.insert("xsd".into(), "http://www.w3.org/2001/XMLSchema#".into());
    ctx
}
