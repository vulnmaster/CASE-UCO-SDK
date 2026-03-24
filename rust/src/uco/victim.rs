//! Auto-generated uco-victim types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// A victim is a role played by a person or organization that is/was the target of some malicious action.
#[derive(Debug, Clone, Serialize)]
pub struct Victim {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Victim {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/victim/Victim";
    pub const NAMESPACE_PREFIX: &'static str = "uco-victim";

    pub fn builder() -> VictimBuilder {
        VictimBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct VictimBuilder {
}

impl VictimBuilder {
    pub fn build(self) -> Victim {
        Victim {
            class_iri: Victim::CLASS_IRI,
        }
    }
}

impl CaseObject for Victim {
    fn class_iri() -> &'static str { Victim::CLASS_IRI }
    fn type_name() -> &'static str { "Victim" }
}

/// A victim targeting is a grouping of characteristics unique to people or organizations that are the target of some malicious activity.
#[derive(Debug, Clone, Serialize)]
pub struct VictimTargeting {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl VictimTargeting {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/victim/VictimTargeting";
    pub const NAMESPACE_PREFIX: &'static str = "uco-victim";

    pub fn builder() -> VictimTargetingBuilder {
        VictimTargetingBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct VictimTargetingBuilder {
}

impl VictimTargetingBuilder {
    pub fn build(self) -> VictimTargeting {
        VictimTargeting {
            class_iri: VictimTargeting::CLASS_IRI,
        }
    }
}

impl CaseObject for VictimTargeting {
    fn class_iri() -> &'static str { VictimTargeting::CLASS_IRI }
    fn type_name() -> &'static str { "VictimTargeting" }
}
