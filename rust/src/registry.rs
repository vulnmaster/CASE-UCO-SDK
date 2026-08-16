//! Runtime ontology introspection — search and discover CASE/UCO classes from Rust.
//!
//! Loads the auto-generated `_registry.json` and exposes search, listing, and
//! query functions so developers can discover the right classes programmatically.
//!
//! ```no_run
//! use case_uco::registry;
//!
//! let results = registry::search("file");
//! for cls in &results {
//!     println!("{}: {}", cls.name, cls.module);
//! }
//!
//! if let Some(info) = registry::get_class("FileFacet") {
//!     println!("{}", info.description);
//! }
//! ```

use serde::Deserialize;
use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{OnceLock, RwLock, RwLockReadGuard, RwLockWriteGuard};

static REGISTRY: OnceLock<RwLock<RegistryState>> = OnceLock::new();
static REGISTRY_HITS: AtomicU64 = AtomicU64::new(0);
static REGISTRY_MISSES: AtomicU64 = AtomicU64::new(0);
static REGISTRY_GENERATION: AtomicU64 = AtomicU64::new(0);

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
struct RawRegistry {
    #[serde(default)]
    modules: Vec<String>,
    #[serde(default)]
    classes: HashMap<String, RawClass>,
    #[serde(default)]
    vocabs: HashMap<String, RawVocab>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
struct RawClass {
    iri: String,
    module: String,
    description: String,
    parents: Vec<String>,
    is_facet: bool,
    properties: Vec<RawProperty>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
struct RawProperty {
    name: String,
    #[serde(rename = "type")]
    type_name: String,
    type_iri: String,
    cardinality: String,
    required: bool,
    description: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
struct RawVocab {
    iri: String,
    members: Vec<String>,
}

/// A resolved ontology class with its name included.
#[derive(Debug, Clone)]
pub struct OntologyClass {
    pub name: String,
    pub iri: String,
    pub module: String,
    pub description: String,
    pub parents: Vec<String>,
    pub is_facet: bool,
    pub properties: Vec<OntologyProperty>,
}

/// A property on an ontology class.
#[derive(Debug, Clone)]
pub struct OntologyProperty {
    pub name: String,
    pub type_name: String,
    pub type_iri: String,
    pub cardinality: String,
    pub required: bool,
    pub description: String,
}

/// A vocabulary type with its members.
#[derive(Debug, Clone)]
pub struct OntologyVocab {
    pub name: String,
    pub iri: String,
    pub members: Vec<String>,
}

struct Registry {
    modules: Vec<String>,
    classes: HashMap<String, RawClass>,
    classes_lower: HashMap<String, String>,
    vocabs: HashMap<String, RawVocab>,
}

struct RegistryState {
    base: RawRegistry,
    extensions: HashMap<String, RawRegistry>,
    registry: Registry,
}

/// Observable registry cache state (#82).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RegistryCacheMetrics {
    pub hits: u64,
    pub misses: u64,
    pub generation: u64,
    pub registered_extensions: usize,
    pub cached_classes: usize,
}

/// Fail-closed extension registry error (#82).
#[derive(Debug)]
pub enum RegistryError {
    InvalidJson(serde_json::Error),
    InvalidSource,
    DuplicateClassIri {
        iri: String,
        existing: String,
        conflicting: String,
    },
    DuplicateClassName(String),
    DuplicateVocab(String),
}

impl std::fmt::Display for RegistryError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidJson(e) => write!(f, "invalid extension registry JSON: {e}"),
            Self::InvalidSource => write!(f, "extension registry source must be non-empty"),
            Self::DuplicateClassIri { iri, existing, conflicting } => write!(
                f,
                "duplicate class IRI '{iri}': {existing} vs {conflicting}"
            ),
            Self::DuplicateClassName(name) => write!(f, "duplicate class name '{name}'"),
            Self::DuplicateVocab(name) => write!(f, "duplicate vocabulary '{name}'"),
        }
    }
}

impl std::error::Error for RegistryError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::InvalidJson(e) => Some(e),
            _ => None,
        }
    }
}

fn load() -> &'static RwLock<RegistryState> {
    REGISTRY.get_or_init(|| {
        REGISTRY_MISSES.fetch_add(1, Ordering::Relaxed);
        let json = load_json();
        let raw: RawRegistry = match serde_json::from_str(&json) {
            Ok(v) => v,
            Err(e) => panic!("Failed to parse _registry.json: {e}"),
        };
        let registry = Registry::from_raw(raw.clone());
        RwLock::new(RegistryState {
            base: raw,
            extensions: HashMap::new(),
            registry,
        })
    })
}

fn read_state(lock: &RwLock<RegistryState>) -> RwLockReadGuard<'_, RegistryState> {
    match lock.read() {
        Ok(state) => state,
        Err(poisoned) => poisoned.into_inner(),
    }
}

fn write_state(lock: &RwLock<RegistryState>) -> RwLockWriteGuard<'_, RegistryState> {
    match lock.write() {
        Ok(state) => state,
        Err(poisoned) => poisoned.into_inner(),
    }
}

impl Registry {
    fn from_raw(raw: RawRegistry) -> Self {
        let classes_lower = raw
            .classes
            .keys()
            .map(|k| (k.to_lowercase(), k.clone()))
            .collect();
        Self {
            modules: raw.modules,
            classes: raw.classes,
            classes_lower,
            vocabs: raw.vocabs,
        }
    }
}

fn composed_raw(
    base: &RawRegistry,
    extensions: &HashMap<String, RawRegistry>,
) -> Result<RawRegistry, RegistryError> {
    let mut merged = base.clone();
    let mut iri_owners: HashMap<String, String> = merged
        .classes
        .iter()
        .map(|(name, cls)| (cls.iri.clone(), name.clone()))
        .collect();
    let mut sources: Vec<&String> = extensions.keys().collect();
    sources.sort();
    for source in sources {
        let extension = &extensions[source];
        for module in &extension.modules {
            if !merged.modules.contains(module) {
                merged.modules.push(module.clone());
            }
        }
        let mut class_names: Vec<&String> = extension.classes.keys().collect();
        class_names.sort();
        for name in class_names {
            let class = &extension.classes[name];
            if let Some(existing_name) = iri_owners.get(&class.iri) {
                let existing = &merged.classes[existing_name];
                if existing_name != name || existing != class {
                    return Err(RegistryError::DuplicateClassIri {
                        iri: class.iri.clone(),
                        existing: existing_name.clone(),
                        conflicting: name.clone(),
                    });
                }
                continue;
            }
            if let Some(existing) = merged.classes.get(name) {
                if existing != class {
                    return Err(RegistryError::DuplicateClassName(name.clone()));
                }
                continue;
            }
            iri_owners.insert(class.iri.clone(), name.clone());
            merged.classes.insert(name.clone(), class.clone());
        }
        for (name, vocab) in &extension.vocabs {
            if let Some(existing) = merged.vocabs.get(name) {
                if existing != vocab {
                    return Err(RegistryError::DuplicateVocab(name.clone()));
                }
            } else {
                merged.vocabs.insert(name.clone(), vocab.clone());
            }
        }
    }
    merged.modules.sort();
    Ok(merged)
}

/// Register or atomically replace one trusted extension metadata registry (#82).
pub fn register_extension_json(source: &str, json: &str) -> Result<u64, RegistryError> {
    let source = source.trim();
    if source.is_empty() {
        return Err(RegistryError::InvalidSource);
    }
    let extension: RawRegistry = serde_json::from_str(json).map_err(RegistryError::InvalidJson)?;
    let lock = load();
    let mut state = write_state(lock);
    let mut candidate = state.extensions.clone();
    candidate.insert(source.to_string(), extension);
    let merged = composed_raw(&state.base, &candidate)?;
    state.extensions = candidate;
    state.registry = Registry::from_raw(merged);
    Ok(REGISTRY_GENERATION.fetch_add(1, Ordering::Relaxed) + 1)
}

/// Unregister one extension source and rebuild the composite registry (#82).
pub fn unregister_extension(source: &str) -> u64 {
    let lock = load();
    let mut state = write_state(lock);
    let mut candidate = state.extensions.clone();
    if candidate.remove(source).is_none() {
        return REGISTRY_GENERATION.load(Ordering::Relaxed);
    }
    match composed_raw(&state.base, &candidate) {
        Ok(merged) => {
            state.extensions = candidate;
            state.registry = Registry::from_raw(merged);
            REGISTRY_GENERATION.fetch_add(1, Ordering::Relaxed) + 1
        }
        Err(_) => REGISTRY_GENERATION.load(Ordering::Relaxed),
    }
}

/// Reload the generated base registry while retaining registered extensions (#82).
pub fn clear_registry_cache() -> Result<u64, RegistryError> {
    let raw: RawRegistry = serde_json::from_str(&load_json()).map_err(RegistryError::InvalidJson)?;
    let lock = load();
    let mut state = write_state(lock);
    let merged = composed_raw(&raw, &state.extensions)?;
    state.base = raw;
    state.registry = Registry::from_raw(merged);
    Ok(REGISTRY_GENERATION.fetch_add(1, Ordering::Relaxed) + 1)
}

/// Return cache hit/miss and generation counters (#82).
pub fn cache_metrics() -> RegistryCacheMetrics {
    let lock = load();
    let state = read_state(lock);
    RegistryCacheMetrics {
        hits: REGISTRY_HITS.load(Ordering::Relaxed),
        misses: REGISTRY_MISSES.load(Ordering::Relaxed),
        generation: REGISTRY_GENERATION.load(Ordering::Relaxed),
        registered_extensions: state.extensions.len(),
        cached_classes: state.registry.classes.len(),
    }
}

fn load_json() -> String {
    let candidates = vec![
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src/_registry.json"),
        PathBuf::from("src/_registry.json"),
        PathBuf::from("_registry.json"),
    ];
    for path in &candidates {
        if path.exists() {
            return std::fs::read_to_string(path)
                .unwrap_or_else(|e| panic!("Failed to read {}: {}", path.display(), e));
        }
    }
    panic!(
        "Ontology registry not found. Run 'case-uco-generate generate' to produce it. \
         Searched: {:?}",
        candidates
    );
}

fn raw_to_class(name: &str, raw: &RawClass) -> OntologyClass {
    OntologyClass {
        name: name.to_string(),
        iri: raw.iri.clone(),
        module: raw.module.clone(),
        description: raw.description.clone(),
        parents: raw.parents.clone(),
        is_facet: raw.is_facet,
        properties: raw
            .properties
            .iter()
            .map(|p| OntologyProperty {
                name: p.name.clone(),
                type_name: p.type_name.clone(),
                type_iri: p.type_iri.clone(),
                cardinality: p.cardinality.clone(),
                required: p.required,
                description: p.description.clone(),
            })
            .collect(),
    }
}

/// Search for classes by keyword (case-insensitive substring match on name and description).
pub fn search(query: &str) -> Vec<OntologyClass> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let q = query.to_lowercase();
    let mut results: Vec<OntologyClass> = reg
        .classes
        .iter()
        .filter(|(name, cls)| {
            name.to_lowercase().contains(&q) || cls.description.to_lowercase().contains(&q)
        })
        .map(|(name, cls)| raw_to_class(name, cls))
        .collect();
    results.sort_by(|a, b| (&a.module, &a.name).cmp(&(&b.module, &b.name)));
    results
}

/// List all module names.
pub fn list_modules() -> Vec<String> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let mut modules = reg.modules.clone();
    modules.sort();
    modules
}

/// List class names, optionally filtered by module (partial match).
pub fn list_classes(module: Option<&str>) -> Vec<String> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let mut results: Vec<String> = match module {
        None => reg.classes.keys().cloned().collect(),
        Some(m) => {
            let ml = m.to_lowercase();
            reg.classes
                .iter()
                .filter(|(_, cls)| cls.module.to_lowercase().contains(&ml))
                .map(|(name, _)| name.clone())
                .collect()
        }
    };
    results.sort();
    results
}

/// Get full details for a class by name (case-insensitive).
pub fn get_class(name: &str) -> Option<OntologyClass> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let canonical = reg.classes_lower.get(&name.to_lowercase())?;
    let raw = reg.classes.get(canonical)?;
    Some(raw_to_class(canonical, raw))
}

/// Find classes that have a property of the given type (case-insensitive).
pub fn find_by_property_type(type_name: &str) -> Vec<OntologyClass> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let t = type_name.to_lowercase();
    let mut results: Vec<OntologyClass> = reg
        .classes
        .iter()
        .filter(|(_, cls)| {
            cls.properties
                .iter()
                .any(|p| p.type_name.to_lowercase().contains(&t))
        })
        .map(|(name, cls)| raw_to_class(name, cls))
        .collect();
    results.sort_by(|a, b| a.name.cmp(&b.name));
    results
}

/// Find all Facet classes.
pub fn find_facets() -> Vec<OntologyClass> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let mut results: Vec<OntologyClass> = reg
        .classes
        .iter()
        .filter(|(_, cls)| cls.is_facet)
        .map(|(name, cls)| raw_to_class(name, cls))
        .collect();
    results.sort_by(|a, b| a.name.cmp(&b.name));
    results
}

/// List all vocabulary types with their members.
pub fn list_vocabs() -> Vec<OntologyVocab> {
    let lock = load();
    REGISTRY_HITS.fetch_add(1, Ordering::Relaxed);
    let state = read_state(lock);
    let reg = &state.registry;
    let mut results: Vec<OntologyVocab> = reg
        .vocabs
        .iter()
        .map(|(name, v)| OntologyVocab {
            name: name.clone(),
            iri: v.iri.clone(),
            members: v.members.clone(),
        })
        .collect();
    results.sort_by(|a, b| a.name.cmp(&b.name));
    results
}
