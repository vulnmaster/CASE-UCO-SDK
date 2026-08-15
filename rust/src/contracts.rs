//! Logical ProfileContract surface (v2).

#[derive(Debug, Clone)]
pub struct ProfileContract {
    pub profile_id: String,
    pub profile_version: String,
    pub contract_schema_version: String,
    pub check_ids: Vec<String>,
}

pub fn load_contract(profile_id: &str) -> ProfileContract {
    let id = profile_id.to_string();
    let mut checks = vec![
        "PROF-FACET-001".into(),
        "PROF-HASH-001".into(),
        "PROF-TOOL-001".into(),
        "PROF-SHACL-001".into(),
    ];
    if id == "HashIntelligence" {
        checks.push("PROF-HI-001".into());
        checks.push("PROF-HI-002".into());
    }
    if id == "FullCACLifecycle" {
        checks.push("PROF-CAC-001".into());
        checks.push("PROF-CAC-002".into());
        checks.push("PROF-CAC-003".into());
        checks.push("PROF-CAC-004".into());
    }
    if id == "LegalProcess" {
        checks.push("PROF-LEGAL-001".into());
    }
    if id == "AirGappedFieldTriage" {
        checks.push("PROF-AIR-001".into());
    }
    ProfileContract {
        profile_id: id,
        profile_version: "1.0.0".into(),
        contract_schema_version: "1.0.0".into(),
        check_ids: checks,
    }
}
