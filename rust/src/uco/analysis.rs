//! Auto-generated uco-analysis types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// An analytic result facet is a grouping of characteristics unique to the results of an analysis action.
#[derive(Debug, Clone, Serialize)]
pub struct AnalyticResultFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AnalyticResultFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/analysis/AnalyticResultFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-analysis";

    pub fn builder() -> AnalyticResultFacetBuilder {
        AnalyticResultFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AnalyticResultFacetBuilder {
}

impl AnalyticResultFacetBuilder {
    pub fn build(self) -> AnalyticResultFacet {
        AnalyticResultFacet {
            class_iri: AnalyticResultFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for AnalyticResultFacet {
    fn class_iri() -> &'static str { AnalyticResultFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AnalyticResultFacet" }
}

/// An artifact classification is a single specific assertion that a particular class of a classification taxonomy applies to something.
#[derive(Debug, Clone, Serialize)]
pub struct ArtifactClassification {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-analysis:class")]
    pub class: Vec<String>,
    #[serde(rename = "uco-analysis:classificationConfidence")]
    pub classification_confidence: Option<f64>,
}

impl ArtifactClassification {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassification";
    pub const NAMESPACE_PREFIX: &'static str = "uco-analysis";

    pub fn builder() -> ArtifactClassificationBuilder {
        ArtifactClassificationBuilder {
            class: Vec::new(),
            classification_confidence: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ArtifactClassificationBuilder {
    class: Vec<String>,
    classification_confidence: Option<f64>,
}

impl ArtifactClassificationBuilder {
    pub fn class(mut self, value: Vec<String>) -> Self {
        self.class = value;
        self
    }

    pub fn classification_confidence(mut self, value: f64) -> Self {
        self.classification_confidence = Some(value);
        self
    }

    pub fn build(self) -> ArtifactClassification {
        ArtifactClassification {
            class_iri: ArtifactClassification::CLASS_IRI,
            class: self.class,
            classification_confidence: self.classification_confidence,
        }
    }
}

impl CaseObject for ArtifactClassification {
    fn class_iri() -> &'static str { ArtifactClassification::CLASS_IRI }
    fn type_name() -> &'static str { "ArtifactClassification" }
}

/// An artifact classification result facet is a grouping of characteristics unique to the results of an artifact classification analysis action.
#[derive(Debug, Clone, Serialize)]
pub struct ArtifactClassificationResultFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-analysis:classification")]
    pub classification: Vec<ArtifactClassification>,
}

impl ArtifactClassificationResultFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassificationResultFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-analysis";

    pub fn builder() -> ArtifactClassificationResultFacetBuilder {
        ArtifactClassificationResultFacetBuilder {
            classification: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ArtifactClassificationResultFacetBuilder {
    classification: Vec<ArtifactClassification>,
}

impl ArtifactClassificationResultFacetBuilder {
    pub fn classification(mut self, value: Vec<ArtifactClassification>) -> Self {
        self.classification = value;
        self
    }

    pub fn build(self) -> ArtifactClassificationResultFacet {
        ArtifactClassificationResultFacet {
            class_iri: ArtifactClassificationResultFacet::CLASS_IRI,
            classification: self.classification,
        }
    }
}

impl CaseObject for ArtifactClassificationResultFacet {
    fn class_iri() -> &'static str { ArtifactClassificationResultFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ArtifactClassificationResultFacet" }
}
