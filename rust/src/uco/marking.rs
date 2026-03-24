//! Auto-generated uco-marking types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// A granular marking is a grouping of characteristics unique to specification of marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) that apply to par
#[derive(Debug, Clone, Serialize)]
pub struct GranularMarking {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-marking:contentSelectors")]
    pub content_selectors: Vec<String>,
    #[serde(rename = "uco-marking:marking")]
    pub marking: Vec<MarkingDefinition>,
}

impl GranularMarking {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/GranularMarking";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> GranularMarkingBuilder {
        GranularMarkingBuilder {
            content_selectors: Vec::new(),
            marking: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GranularMarkingBuilder {
    content_selectors: Vec<String>,
    marking: Vec<MarkingDefinition>,
}

impl GranularMarkingBuilder {
    pub fn content_selectors(mut self, value: Vec<String>) -> Self {
        self.content_selectors = value;
        self
    }

    pub fn marking(mut self, value: Vec<MarkingDefinition>) -> Self {
        self.marking = value;
        self
    }

    pub fn build(self) -> GranularMarking {
        GranularMarking {
            class_iri: GranularMarking::CLASS_IRI,
            content_selectors: self.content_selectors,
            marking: self.marking,
        }
    }
}

impl CaseObject for GranularMarking {
    fn class_iri() -> &'static str { GranularMarking::CLASS_IRI }
    fn type_name() -> &'static str { "GranularMarking" }
}

/// A license marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey de
#[derive(Debug, Clone, Serialize)]
pub struct LicenseMarking {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-marking:definitionType")]
    pub definition_type: Vec<String>,
    #[serde(rename = "uco-marking:license")]
    pub license: String,
}

impl LicenseMarking {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/LicenseMarking";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> LicenseMarkingBuilder {
        LicenseMarkingBuilder {
            definition_type: Vec::new(),
            license: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LicenseMarkingBuilder {
    definition_type: Vec<String>,
    license: Option<String>,
}

impl LicenseMarkingBuilder {
    pub fn definition_type(mut self, value: Vec<String>) -> Self {
        self.definition_type = value;
        self
    }

    pub fn license(mut self, value: String) -> Self {
        self.license = Some(value);
        self
    }

    pub fn build(self) -> LicenseMarking {
        LicenseMarking {
            class_iri: LicenseMarking::CLASS_IRI,
            definition_type: self.definition_type,
            license: self.license.expect("missing required field: license"),
        }
    }
}

impl CaseObject for LicenseMarking {
    fn class_iri() -> &'static str { LicenseMarking::CLASS_IRI }
    fn type_name() -> &'static str { "LicenseMarking" }
}

/// A marking definition is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be used and sh
#[derive(Debug, Clone, Serialize)]
pub struct MarkingDefinition {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-marking:definition")]
    pub definition: Vec<MarkingModel>,
    #[serde(rename = "uco-marking:definitionType")]
    pub definition_type: String,
}

impl MarkingDefinition {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingDefinition";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> MarkingDefinitionBuilder {
        MarkingDefinitionBuilder {
            definition: Vec::new(),
            definition_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MarkingDefinitionBuilder {
    definition: Vec<MarkingModel>,
    definition_type: Option<String>,
}

impl MarkingDefinitionBuilder {
    pub fn definition(mut self, value: Vec<MarkingModel>) -> Self {
        self.definition = value;
        self
    }

    pub fn definition_type(mut self, value: String) -> Self {
        self.definition_type = Some(value);
        self
    }

    pub fn build(self) -> MarkingDefinition {
        MarkingDefinition {
            class_iri: MarkingDefinition::CLASS_IRI,
            definition: self.definition,
            definition_type: self.definition_type.expect("missing required field: definition_type"),
        }
    }
}

impl CaseObject for MarkingDefinition {
    fn class_iri() -> &'static str { MarkingDefinition::CLASS_IRI }
    fn type_name() -> &'static str { "MarkingDefinition" }
}

/// A marking model is a grouping of characteristics unique to the expression of a particular form of data marking definitions (restrictions, permissions, and other guidance for how data can be used and s
#[derive(Debug, Clone, Serialize)]
pub struct MarkingModel {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MarkingModel {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingModel";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> MarkingModelBuilder {
        MarkingModelBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MarkingModelBuilder {
}

impl MarkingModelBuilder {
    pub fn build(self) -> MarkingModel {
        MarkingModel {
            class_iri: MarkingModel::CLASS_IRI,
        }
    }
}

impl CaseObject for MarkingModel {
    fn class_iri() -> &'static str { MarkingModel::CLASS_IRI }
    fn type_name() -> &'static str { "MarkingModel" }
}

/// A release-to marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey
#[derive(Debug, Clone, Serialize)]
pub struct ReleaseToMarking {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-marking:authorizedIdentities")]
    pub authorized_identities: Vec<String>,
    #[serde(rename = "uco-marking:definitionType")]
    pub definition_type: Vec<String>,
}

impl ReleaseToMarking {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/ReleaseToMarking";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> ReleaseToMarkingBuilder {
        ReleaseToMarkingBuilder {
            authorized_identities: Vec::new(),
            definition_type: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ReleaseToMarkingBuilder {
    authorized_identities: Vec<String>,
    definition_type: Vec<String>,
}

impl ReleaseToMarkingBuilder {
    pub fn authorized_identities(mut self, value: Vec<String>) -> Self {
        self.authorized_identities = value;
        self
    }

    pub fn definition_type(mut self, value: Vec<String>) -> Self {
        self.definition_type = value;
        self
    }

    pub fn build(self) -> ReleaseToMarking {
        ReleaseToMarking {
            class_iri: ReleaseToMarking::CLASS_IRI,
            authorized_identities: self.authorized_identities,
            definition_type: self.definition_type,
        }
    }
}

impl CaseObject for ReleaseToMarking {
    fn class_iri() -> &'static str { ReleaseToMarking::CLASS_IRI }
    fn type_name() -> &'static str { "ReleaseToMarking" }
}

/// A statement marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey 
#[derive(Debug, Clone, Serialize)]
pub struct StatementMarking {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-marking:definitionType")]
    pub definition_type: Vec<String>,
    #[serde(rename = "uco-marking:statement")]
    pub statement: String,
}

impl StatementMarking {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/StatementMarking";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> StatementMarkingBuilder {
        StatementMarkingBuilder {
            definition_type: Vec::new(),
            statement: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct StatementMarkingBuilder {
    definition_type: Vec<String>,
    statement: Option<String>,
}

impl StatementMarkingBuilder {
    pub fn definition_type(mut self, value: Vec<String>) -> Self {
        self.definition_type = value;
        self
    }

    pub fn statement(mut self, value: String) -> Self {
        self.statement = Some(value);
        self
    }

    pub fn build(self) -> StatementMarking {
        StatementMarking {
            class_iri: StatementMarking::CLASS_IRI,
            definition_type: self.definition_type,
            statement: self.statement.expect("missing required field: statement"),
        }
    }
}

impl CaseObject for StatementMarking {
    fn class_iri() -> &'static str { StatementMarking::CLASS_IRI }
    fn type_name() -> &'static str { "StatementMarking" }
}

/// A terms of use marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to conv
#[derive(Debug, Clone, Serialize)]
pub struct TermsOfUseMarking {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-marking:definitionType")]
    pub definition_type: Vec<String>,
    #[serde(rename = "uco-marking:termsOfUse")]
    pub terms_of_use: String,
}

impl TermsOfUseMarking {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/marking/TermsOfUseMarking";
    pub const NAMESPACE_PREFIX: &'static str = "uco-marking";

    pub fn builder() -> TermsOfUseMarkingBuilder {
        TermsOfUseMarkingBuilder {
            definition_type: Vec::new(),
            terms_of_use: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TermsOfUseMarkingBuilder {
    definition_type: Vec<String>,
    terms_of_use: Option<String>,
}

impl TermsOfUseMarkingBuilder {
    pub fn definition_type(mut self, value: Vec<String>) -> Self {
        self.definition_type = value;
        self
    }

    pub fn terms_of_use(mut self, value: String) -> Self {
        self.terms_of_use = Some(value);
        self
    }

    pub fn build(self) -> TermsOfUseMarking {
        TermsOfUseMarking {
            class_iri: TermsOfUseMarking::CLASS_IRI,
            definition_type: self.definition_type,
            terms_of_use: self.terms_of_use.expect("missing required field: terms_of_use"),
        }
    }
}

impl CaseObject for TermsOfUseMarking {
    fn class_iri() -> &'static str { TermsOfUseMarking::CLASS_IRI }
    fn type_name() -> &'static str { "TermsOfUseMarking" }
}
