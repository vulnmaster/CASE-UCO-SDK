//! Auto-generated CASE vocabularies for the CASE/UCO ontology.
//!
//! Every CASE vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.

/// Vocabulary: InvestigationFormVocab
#[derive(Debug, Clone, Copy)]
pub struct InvestigationFormVocab;

impl InvestigationFormVocab {
    pub const IRI: &'static str = "https://ontology.caseontology.org/case/vocabulary/InvestigationFormVocab";
    pub const MEMBERS: &'static [&'static str] = &["case", "incident", "suspicious-activity"];
    pub const CASE: &'static str = "case";
    pub const INCIDENT: &'static str = "incident";
    pub const SUSPICIOUS_ACTIVITY: &'static str = "suspicious-activity";
}
