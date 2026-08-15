//! Profile-aware InvestigationBuilder.

use crate::graph::{CaseGraph, GraphError, LoadError};
use crate::helpers::{self, CsamEvidence, ToolRun};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct CritiqueFinding {
    pub severity: String,
    pub message: String,
    pub path: String,
}

pub struct InvestigationBuilder {
    pub scenario: String,
    pub profile_id: String,
    pub graph: CaseGraph,
    findings: Vec<CritiqueFinding>,
}

impl InvestigationBuilder {
    pub fn new(scenario: &str, profile_id: Option<&str>) -> Result<Self, LoadError> {
        let resolved = resolve_profile(profile_id, scenario)?;
        let mut extra = HashMap::new();
        if requires_cac(&resolved) {
            extra.insert(
                "cac-core".to_string(),
                "https://cacontology.projectvic.org/core#".to_string(),
            );
            extra.insert(
                "cacontology".to_string(),
                "https://cacontology.projectvic.org#".to_string(),
            );
        }
        let graph = if extra.is_empty() {
            CaseGraph::new("http://example.org/kb/")
        } else {
            CaseGraph::with_extra_context("http://example.org/kb/", &extra)?
        };
        Ok(Self {
            scenario: scenario.to_string(),
            profile_id: resolved,
            graph,
            findings: Vec::new(),
        })
    }

    pub fn add_file(
        &mut self,
        file_name: &str,
        hashes: &[(&str, &str)],
    ) -> Result<String, GraphError> {
        if hashes.is_empty() {
            self.findings.push(CritiqueFinding {
                severity: "error".into(),
                message: format!(
                    "{file_name}: {} requires ContentDataFacet hashes",
                    self.profile_id
                ),
                path: file_name.into(),
            });
        }
        helpers::file_with_content_hashes(&mut self.graph, file_name, hashes)
    }

    pub fn add_csam_evidence(
        &mut self,
        file_name: &str,
        hashes: &[(&str, &str)],
    ) -> Result<CsamEvidence, GraphError> {
        if hashes.is_empty() {
            self.findings.push(CritiqueFinding {
                severity: "error".into(),
                message: format!("{file_name}: CSAM evidence must carry hashes"),
                path: file_name.into(),
            });
        }
        helpers::model_csam_evidence(&mut self.graph, file_name, hashes, "PhotoDNA", None)
    }

    pub fn add_tool_run(
        &mut self,
        tool_name: &str,
        action_name: &str,
        tool_version: Option<&str>,
    ) -> Result<ToolRun, GraphError> {
        if tool_version.is_none() {
            self.findings.push(CritiqueFinding {
                severity: "warning".into(),
                message: format!("Tool {tool_name} has no version"),
                path: tool_name.into(),
            });
        }
        helpers::model_tool_run(&mut self.graph, tool_name, action_name, tool_version)
    }

    pub fn build(&self) -> &CaseGraph {
        &self.graph
    }

    pub fn critique(&self) -> &[CritiqueFinding] {
        &self.findings
    }
}

fn requires_cac(profile_id: &str) -> bool {
    profile_id == "FullCACLifecycle" || profile_id == "HashIntelligence"
}

fn resolve_profile(profile_id: Option<&str>, scenario: &str) -> Result<String, LoadError> {
    const ALL: &[&str] = &[
        "MinimalForensics",
        "AirGappedFieldTriage",
        "HashIntelligence",
        "ToolMapping",
        "LegalProcess",
        "FullCACLifecycle",
        "CrossOntology",
    ];
    if let Some(id) = profile_id {
        for known in ALL {
            if known.eq_ignore_ascii_case(id) {
                return Ok((*known).to_string());
            }
        }
        return Err(LoadError::Policy(format!(
            "Unknown composition profile: {id}"
        )));
    }
    let query = scenario.to_ascii_lowercase();
    let mut best = ("MinimalForensics", 0);
    for id in ALL {
        let mut score = 0;
        if query.contains(&id.to_ascii_lowercase()) {
            score += 8;
        }
        for token in keywords(id) {
            if query.contains(token) {
                score += 2;
            }
        }
        if score > best.1 {
            best = (*id, score);
        }
    }
    Ok(best.0.to_string())
}

fn keywords(id: &str) -> &'static [&'static str] {
    match id {
        "HashIntelligence" => &["hash", "photodna", "vics", "csam", "sha256"],
        "FullCACLifecycle" => &["cac", "csam", "grooming", "trafficking", "cybertip"],
        "AirGappedFieldTriage" => &["air", "offline", "field", "triage"],
        "ToolMapping" => &["tool", "autopsy", "solve-it"],
        "LegalProcess" => &["charge", "indictment", "plea", "sentence"],
        "CrossOntology" => &["gufo", "prov", "cross-ontology"],
        _ => &["file", "hash", "triage"],
    }
}
