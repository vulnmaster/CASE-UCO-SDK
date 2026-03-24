//! Auto-generated uco-configuration types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

use crate::uco::core::UcoObject;

/// A configuration is a grouping of characteristics unique to a set of parameters or initial settings for the use of a tool, application, software, or other cyber object.
#[derive(Debug, Clone, Serialize)]
pub struct Configuration {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-configuration:configurationEntry")]
    pub configuration_entry: Vec<ConfigurationEntry>,
    #[serde(rename = "uco-configuration:dependencies")]
    pub dependencies: Vec<Dependency>,
    #[serde(rename = "uco-configuration:usageContextAssumptions")]
    pub usage_context_assumptions: Vec<String>,
}

impl Configuration {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/configuration/Configuration";
    pub const NAMESPACE_PREFIX: &'static str = "uco-configuration";

    pub fn builder() -> ConfigurationBuilder {
        ConfigurationBuilder {
            configuration_entry: Vec::new(),
            dependencies: Vec::new(),
            usage_context_assumptions: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ConfigurationBuilder {
    configuration_entry: Vec<ConfigurationEntry>,
    dependencies: Vec<Dependency>,
    usage_context_assumptions: Vec<String>,
}

impl ConfigurationBuilder {
    pub fn configuration_entry(mut self, value: Vec<ConfigurationEntry>) -> Self {
        self.configuration_entry = value;
        self
    }

    pub fn dependencies(mut self, value: Vec<Dependency>) -> Self {
        self.dependencies = value;
        self
    }

    pub fn usage_context_assumptions(mut self, value: Vec<String>) -> Self {
        self.usage_context_assumptions = value;
        self
    }

    pub fn build(self) -> Configuration {
        Configuration {
            class_iri: Configuration::CLASS_IRI,
            configuration_entry: self.configuration_entry,
            dependencies: self.dependencies,
            usage_context_assumptions: self.usage_context_assumptions,
        }
    }
}

impl CaseObject for Configuration {
    fn class_iri() -> &'static str { Configuration::CLASS_IRI }
    fn type_name() -> &'static str { "Configuration" }
}

/// A configuration entry is a grouping of characteristics unique to a particular parameter or initial setting for the use of a tool, application, software, or other cyber object.
#[derive(Debug, Clone, Serialize)]
pub struct ConfigurationEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-configuration:itemDescription")]
    pub item_description: Option<String>,
    #[serde(rename = "uco-configuration:itemName")]
    pub item_name: Option<String>,
    #[serde(rename = "uco-configuration:itemObject")]
    pub item_object: Vec<UcoObject>,
    #[serde(rename = "uco-configuration:itemType")]
    pub item_type: Option<String>,
    #[serde(rename = "uco-configuration:itemValue")]
    pub item_value: Vec<String>,
}

impl ConfigurationEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/configuration/ConfigurationEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-configuration";

    pub fn builder() -> ConfigurationEntryBuilder {
        ConfigurationEntryBuilder {
            item_description: None,
            item_name: None,
            item_object: Vec::new(),
            item_type: None,
            item_value: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ConfigurationEntryBuilder {
    item_description: Option<String>,
    item_name: Option<String>,
    item_object: Vec<UcoObject>,
    item_type: Option<String>,
    item_value: Vec<String>,
}

impl ConfigurationEntryBuilder {
    pub fn item_description(mut self, value: String) -> Self {
        self.item_description = Some(value);
        self
    }

    pub fn item_name(mut self, value: String) -> Self {
        self.item_name = Some(value);
        self
    }

    pub fn item_object(mut self, value: Vec<UcoObject>) -> Self {
        self.item_object = value;
        self
    }

    pub fn item_type(mut self, value: String) -> Self {
        self.item_type = Some(value);
        self
    }

    pub fn item_value(mut self, value: Vec<String>) -> Self {
        self.item_value = value;
        self
    }

    pub fn build(self) -> ConfigurationEntry {
        ConfigurationEntry {
            class_iri: ConfigurationEntry::CLASS_IRI,
            item_description: self.item_description,
            item_name: self.item_name,
            item_object: self.item_object,
            item_type: self.item_type,
            item_value: self.item_value,
        }
    }
}

impl CaseObject for ConfigurationEntry {
    fn class_iri() -> &'static str { ConfigurationEntry::CLASS_IRI }
    fn type_name() -> &'static str { "ConfigurationEntry" }
}

/// A dependency is a grouping of characteristics unique to something that a tool or other software relies on to function as intended.
#[derive(Debug, Clone, Serialize)]
pub struct Dependency {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-configuration:dependencyDescription")]
    pub dependency_description: Option<String>,
    #[serde(rename = "uco-configuration:dependencyType")]
    pub dependency_type: Option<String>,
}

impl Dependency {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/configuration/Dependency";
    pub const NAMESPACE_PREFIX: &'static str = "uco-configuration";

    pub fn builder() -> DependencyBuilder {
        DependencyBuilder {
            dependency_description: None,
            dependency_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DependencyBuilder {
    dependency_description: Option<String>,
    dependency_type: Option<String>,
}

impl DependencyBuilder {
    pub fn dependency_description(mut self, value: String) -> Self {
        self.dependency_description = Some(value);
        self
    }

    pub fn dependency_type(mut self, value: String) -> Self {
        self.dependency_type = Some(value);
        self
    }

    pub fn build(self) -> Dependency {
        Dependency {
            class_iri: Dependency::CLASS_IRI,
            dependency_description: self.dependency_description,
            dependency_type: self.dependency_type,
        }
    }
}

impl CaseObject for Dependency {
    fn class_iri() -> &'static str { Dependency::CLASS_IRI }
    fn type_name() -> &'static str { "Dependency" }
}
