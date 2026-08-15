//! Logical InvestigationWorkflow: persist workflow-state.json and step cursor.

use crate::builder::InvestigationBuilder;
use crate::graph::LoadError;
use std::fs;
use std::path::{Path, PathBuf};

pub struct InvestigationWorkflow {
    pub workflow_id: String,
    pub profile_id: String,
    pub working_dir: PathBuf,
    pub builder: InvestigationBuilder,
    pub completed_steps: Vec<String>,
}

impl InvestigationWorkflow {
    pub fn new(
        workflow_id: &str,
        scenario: &str,
        working_dir: impl AsRef<Path>,
        profile_id: Option<&str>,
    ) -> Result<Self, LoadError> {
        let profile = profile_id
            .map(|s| s.to_string())
            .unwrap_or_else(|| default_profile(workflow_id).to_string());
        fs::create_dir_all(working_dir.as_ref()).ok();
        Ok(Self {
            workflow_id: workflow_id.to_string(),
            profile_id: profile.clone(),
            working_dir: working_dir.as_ref().to_path_buf(),
            builder: InvestigationBuilder::new(scenario, Some(&profile))?,
            completed_steps: Vec::new(),
        })
    }

    pub fn step(&mut self) -> Option<String> {
        let next = self.next_step()?;
        if next == "open" {
            let _ = self.builder.add_tool_run("Triage Collector", "scan", Some("1.0"));
        }
        self.completed_steps.push(next.clone());
        self.save();
        Some(next)
    }

    pub fn save(&self) {
        let completed = self
            .completed_steps
            .iter()
            .map(|s| format!("\"{s}\""))
            .collect::<Vec<_>>()
            .join(",");
        let json = format!(
            "{{\"schema_version\":\"1.0.0\",\"workflow_id\":\"{}\",\"profile_id\":\"{}\",\"status\":\"running\",\"cursor\":{{\"completed_steps\":[{completed}]}}}}",
            self.workflow_id, self.profile_id
        );
        let _ = fs::write(self.working_dir.join("workflow-state.json"), json);
    }

    fn next_step(&self) -> Option<String> {
        for step in ["load", "open", "tool", "ingest", "hash", "critique", "validate", "emit"] {
            if !self.completed_steps.iter().any(|s| s == step) {
                return Some(step.to_string());
            }
        }
        None
    }
}

fn default_profile(workflow_id: &str) -> &'static str {
    match workflow_id {
        "hash-intelligence-vics" | "cac-csam-provenance" => "HashIntelligence",
        "cac-grooming-chat" => "FullCACLifecycle",
        _ => "AirGappedFieldTriage",
    }
}
