//! Auto-generated uco-role types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// A benevolent role is a role with positive and/or beneficial intent.
#[derive(Debug, Clone, Serialize)]
pub struct BenevolentRole {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BenevolentRole {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/role/BenevolentRole";
    pub const NAMESPACE_PREFIX: &'static str = "uco-role";

    pub fn builder() -> BenevolentRoleBuilder {
        BenevolentRoleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BenevolentRoleBuilder {
}

impl BenevolentRoleBuilder {
    pub fn build(self) -> BenevolentRole {
        BenevolentRole {
            class_iri: BenevolentRole::CLASS_IRI,
        }
    }
}

impl CaseObject for BenevolentRole {
    fn class_iri() -> &'static str { BenevolentRole::CLASS_IRI }
    fn type_name() -> &'static str { "BenevolentRole" }
}

/// A malicious role is a role with malevolent intent.
#[derive(Debug, Clone, Serialize)]
pub struct MaliciousRole {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MaliciousRole {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/role/MaliciousRole";
    pub const NAMESPACE_PREFIX: &'static str = "uco-role";

    pub fn builder() -> MaliciousRoleBuilder {
        MaliciousRoleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MaliciousRoleBuilder {
}

impl MaliciousRoleBuilder {
    pub fn build(self) -> MaliciousRole {
        MaliciousRole {
            class_iri: MaliciousRole::CLASS_IRI,
        }
    }
}

impl CaseObject for MaliciousRole {
    fn class_iri() -> &'static str { MaliciousRole::CLASS_IRI }
    fn type_name() -> &'static str { "MaliciousRole" }
}

/// A neutral role is a role with impartial intent.
#[derive(Debug, Clone, Serialize)]
pub struct NeutralRole {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NeutralRole {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/role/NeutralRole";
    pub const NAMESPACE_PREFIX: &'static str = "uco-role";

    pub fn builder() -> NeutralRoleBuilder {
        NeutralRoleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NeutralRoleBuilder {
}

impl NeutralRoleBuilder {
    pub fn build(self) -> NeutralRole {
        NeutralRole {
            class_iri: NeutralRole::CLASS_IRI,
        }
    }
}

impl CaseObject for NeutralRole {
    fn class_iri() -> &'static str { NeutralRole::CLASS_IRI }
    fn type_name() -> &'static str { "NeutralRole" }
}

/// A role is a usual or customary function based on contextual perspective.
#[derive(Debug, Clone, Serialize)]
pub struct Role {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Role {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/role/Role";
    pub const NAMESPACE_PREFIX: &'static str = "uco-role";

    pub fn builder() -> RoleBuilder {
        RoleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RoleBuilder {
}

impl RoleBuilder {
    pub fn build(self) -> Role {
        Role {
            class_iri: Role::CLASS_IRI,
        }
    }
}

impl CaseObject for Role {
    fn class_iri() -> &'static str { Role::CLASS_IRI }
    fn type_name() -> &'static str { "Role" }
}
