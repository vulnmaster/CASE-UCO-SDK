//! Auto-generated uco-types types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// A controlled dictionary is a list of (term/key, value) pairs where each term/key exists no more than once and is constrained to an explicitly defined set of values.
#[derive(Debug, Clone, Serialize)]
pub struct ControlledDictionary {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-types:entry")]
    pub entry: Vec<ControlledDictionaryEntry>,
}

impl ControlledDictionary {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> ControlledDictionaryBuilder {
        ControlledDictionaryBuilder {
            entry: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ControlledDictionaryBuilder {
    entry: Vec<ControlledDictionaryEntry>,
}

impl ControlledDictionaryBuilder {
    pub fn entry(mut self, value: Vec<ControlledDictionaryEntry>) -> Self {
        self.entry = value;
        self
    }

    pub fn build(self) -> ControlledDictionary {
        ControlledDictionary {
            class_iri: ControlledDictionary::CLASS_IRI,
            entry: self.entry,
        }
    }
}

impl CaseObject for ControlledDictionary {
    fn class_iri() -> &'static str { ControlledDictionary::CLASS_IRI }
    fn type_name() -> &'static str { "ControlledDictionary" }
}

/// A controlled dictionary entry is a single (term/key, value) pair where the term/key is constrained to an explicitly defined set of values.
#[derive(Debug, Clone, Serialize)]
pub struct ControlledDictionaryEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ControlledDictionaryEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionaryEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> ControlledDictionaryEntryBuilder {
        ControlledDictionaryEntryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ControlledDictionaryEntryBuilder {
}

impl ControlledDictionaryEntryBuilder {
    pub fn build(self) -> ControlledDictionaryEntry {
        ControlledDictionaryEntry {
            class_iri: ControlledDictionaryEntry::CLASS_IRI,
        }
    }
}

impl CaseObject for ControlledDictionaryEntry {
    fn class_iri() -> &'static str { ControlledDictionaryEntry::CLASS_IRI }
    fn type_name() -> &'static str { "ControlledDictionaryEntry" }
}

/// A dictionary is list of (term/key, value) pairs with each term/key having an expectation to exist no more than once.  types:Dictionary alone does not validate this expectation, but validation is avail
#[derive(Debug, Clone, Serialize)]
pub struct Dictionary {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-types:entry")]
    pub entry: Vec<DictionaryEntry>,
}

impl Dictionary {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/Dictionary";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> DictionaryBuilder {
        DictionaryBuilder {
            entry: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DictionaryBuilder {
    entry: Vec<DictionaryEntry>,
}

impl DictionaryBuilder {
    pub fn entry(mut self, value: Vec<DictionaryEntry>) -> Self {
        self.entry = value;
        self
    }

    pub fn build(self) -> Dictionary {
        Dictionary {
            class_iri: Dictionary::CLASS_IRI,
            entry: self.entry,
        }
    }
}

impl CaseObject for Dictionary {
    fn class_iri() -> &'static str { Dictionary::CLASS_IRI }
    fn type_name() -> &'static str { "Dictionary" }
}

/// A dictionary entry is a single (term/key, value) pair.
#[derive(Debug, Clone, Serialize)]
pub struct DictionaryEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-types:key")]
    pub key: String,
    #[serde(rename = "uco-types:value")]
    pub value: String,
}

impl DictionaryEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/DictionaryEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> DictionaryEntryBuilder {
        DictionaryEntryBuilder {
            key: None,
            value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DictionaryEntryBuilder {
    key: Option<String>,
    value: Option<String>,
}

impl DictionaryEntryBuilder {
    pub fn key(mut self, value: String) -> Self {
        self.key = Some(value);
        self
    }

    pub fn value(mut self, value: String) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> DictionaryEntry {
        DictionaryEntry {
            class_iri: DictionaryEntry::CLASS_IRI,
            key: self.key.expect("missing required field: key"),
            value: self.value.expect("missing required field: value"),
        }
    }
}

impl CaseObject for DictionaryEntry {
    fn class_iri() -> &'static str { DictionaryEntry::CLASS_IRI }
    fn type_name() -> &'static str { "DictionaryEntry" }
}

/// A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm that maps data of arbitrary size to a bit string (the 'hash') and is a one-way function, that is, a fu
#[derive(Debug, Clone, Serialize)]
pub struct Hash {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-types:hashMethod")]
    pub hash_method: Vec<String>,
    #[serde(rename = "uco-types:hashValue")]
    pub hash_value: Vec<u8>,
}

impl Hash {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/Hash";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> HashBuilder {
        HashBuilder {
            hash_method: Vec::new(),
            hash_value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct HashBuilder {
    hash_method: Vec<String>,
    hash_value: Option<Vec<u8>>,
}

impl HashBuilder {
    pub fn hash_method(mut self, value: Vec<String>) -> Self {
        self.hash_method = value;
        self
    }

    pub fn hash_value(mut self, value: Vec<u8>) -> Self {
        self.hash_value = Some(value);
        self
    }

    pub fn build(self) -> Hash {
        Hash {
            class_iri: Hash::CLASS_IRI,
            hash_method: self.hash_method,
            hash_value: self.hash_value.expect("missing required field: hash_value"),
        }
    }
}

impl CaseObject for Hash {
    fn class_iri() -> &'static str { Hash::CLASS_IRI }
    fn type_name() -> &'static str { "Hash" }
}

/// ImproperDictionary
#[derive(Debug, Clone, Serialize)]
pub struct ImproperDictionary {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-types:repeatsKey")]
    pub repeats_key: Vec<String>,
}

impl ImproperDictionary {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/ImproperDictionary";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> ImproperDictionaryBuilder {
        ImproperDictionaryBuilder {
            repeats_key: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ImproperDictionaryBuilder {
    repeats_key: Vec<String>,
}

impl ImproperDictionaryBuilder {
    pub fn repeats_key(mut self, value: Vec<String>) -> Self {
        self.repeats_key = value;
        self
    }

    pub fn build(self) -> ImproperDictionary {
        ImproperDictionary {
            class_iri: ImproperDictionary::CLASS_IRI,
            repeats_key: self.repeats_key,
        }
    }
}

impl CaseObject for ImproperDictionary {
    fn class_iri() -> &'static str { ImproperDictionary::CLASS_IRI }
    fn type_name() -> &'static str { "ImproperDictionary" }
}

/// A proper dictionary is list of (term/key, value) pairs with each term/key existing no more than once.
#[derive(Debug, Clone, Serialize)]
pub struct ProperDictionary {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ProperDictionary {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/ProperDictionary";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> ProperDictionaryBuilder {
        ProperDictionaryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProperDictionaryBuilder {
}

impl ProperDictionaryBuilder {
    pub fn build(self) -> ProperDictionary {
        ProperDictionary {
            class_iri: ProperDictionary::CLASS_IRI,
        }
    }
}

impl CaseObject for ProperDictionary {
    fn class_iri() -> &'static str { ProperDictionary::CLASS_IRI }
    fn type_name() -> &'static str { "ProperDictionary" }
}

/// A semi-ordered array of items, that can be present in multiple copies.  Implemetation of a UCO Thread is similar to a Collections Ontology List, except a Thread may fork and merge - that is, one of it
#[derive(Debug, Clone, Serialize)]
pub struct Thread {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Thread {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/Thread";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> ThreadBuilder {
        ThreadBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ThreadBuilder {
}

impl ThreadBuilder {
    pub fn build(self) -> Thread {
        Thread {
            class_iri: Thread::CLASS_IRI,
        }
    }
}

impl CaseObject for Thread {
    fn class_iri() -> &'static str { Thread::CLASS_IRI }
    fn type_name() -> &'static str { "Thread" }
}

/// A ThreadItem is a member of a thread.
#[derive(Debug, Clone, Serialize)]
pub struct ThreadItem {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ThreadItem {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/types/ThreadItem";
    pub const NAMESPACE_PREFIX: &'static str = "uco-types";

    pub fn builder() -> ThreadItemBuilder {
        ThreadItemBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ThreadItemBuilder {
}

impl ThreadItemBuilder {
    pub fn build(self) -> ThreadItem {
        ThreadItem {
            class_iri: ThreadItem::CLASS_IRI,
        }
    }
}

impl CaseObject for ThreadItem {
    fn class_iri() -> &'static str { ThreadItem::CLASS_IRI }
    fn type_name() -> &'static str { "ThreadItem" }
}
