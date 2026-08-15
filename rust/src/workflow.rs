//! Logical InvestigationWorkflow: persist workflow-state.json and step cursor.
//! 2.1: full hash_media / adapter / partition handlers (Python-parity).
//! [`register_handler`] is the 2.0.1 extension point.

use crate::builder::InvestigationBuilder;
use crate::graph::LoadError;
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{Mutex, OnceLock};

pub trait WorkflowStepHandler: Send + Sync {
    fn step_id(&self) -> &str;
    fn execute(&self, workflow: &mut InvestigationWorkflow);
}

fn extra_handlers() -> &'static Mutex<HashMap<String, Box<dyn WorkflowStepHandler>>> {
    static HANDLERS: OnceLock<Mutex<HashMap<String, Box<dyn WorkflowStepHandler>>>> = OnceLock::new();
    HANDLERS.get_or_init(|| Mutex::new(HashMap::new()))
}

/// 2.1 extension point. Built-in steps still advance the cursor if no handler is registered.
pub fn register_handler(handler: Box<dyn WorkflowStepHandler>) {
    extra_handlers()
        .lock()
        .expect("handler lock")
        .insert(handler.step_id().to_string(), handler);
}

pub fn clear_handlers() {
    extra_handlers().lock().expect("handler lock").clear();
}

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

    pub fn resume(working_dir: impl AsRef<Path>) -> Result<Self, LoadError> {
        let dir = working_dir.as_ref();
        let text = fs::read_to_string(dir.join("workflow-state.json"))
            .map_err(|e| LoadError::Policy(e.to_string()))?;
        let workflow_id = extract_json_string(&text, "workflow_id").unwrap_or_else(|| "field-triage".into());
        let profile_id = extract_json_string(&text, "profile_id");
        let scenario = extract_json_string(&text, "scenario").unwrap_or_else(|| workflow_id.clone());
        let mut wf = Self::new(&workflow_id, &scenario, dir, profile_id.as_deref())?;
        wf.completed_steps = extract_json_string_array(&text, "completed_steps");
        let graph_path = dir.join("default.jsonld");
        if graph_path.exists() {
            wf.builder
                .graph
                .load_file(graph_path.to_string_lossy().as_ref())
                .map_err(|e| LoadError::Policy(e.to_string()))?;
        }
        Ok(wf)
    }

    pub fn step(&mut self) -> Option<String> {
        let next = self.next_step()?;
        let has_extra = extra_handlers()
            .lock()
            .ok()
            .map(|map| map.contains_key(&next))
            .unwrap_or(false);
        if has_extra {
            if let Ok(map) = extra_handlers().lock() {
                if let Some(handler) = map.get(&next) {
                    handler.execute(self);
                }
            }
        } else if next == "open" {
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
            "{{\"schema_version\":\"1.0.0\",\"workflow_id\":\"{}\",\"profile_id\":\"{}\",\"scenario\":\"{}\",\"status\":\"running\",\"cursor\":{{\"completed_steps\":[{completed}]}}}}",
            self.workflow_id,
            self.profile_id,
            self.builder.scenario.replace('\\', "\\\\").replace('"', "\\\"")
        );
        let _ = fs::write(self.working_dir.join("workflow-state.json"), json);
        let _ = self
            .builder
            .graph
            .write(self.working_dir.join("default.jsonld").to_string_lossy().as_ref());
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

fn extract_json_string(json: &str, key: &str) -> Option<String> {
    let needle = format!("\"{key}\"");
    let idx = json.find(&needle)?;
    let rest = &json[idx + needle.len()..];
    let colon = rest.find(':')?;
    let after = rest[colon + 1..].trim_start();
    if !after.starts_with('"') {
        return None;
    }
    let body = &after[1..];
    let end = body.find('"')?;
    Some(body[..end].to_string())
}

fn extract_json_string_array(json: &str, key: &str) -> Vec<String> {
    let mut result = Vec::new();
    let needle = format!("\"{key}\"");
    let Some(idx) = json.find(&needle) else {
        return result;
    };
    let rest = &json[idx + needle.len()..];
    let Some(start) = rest.find('[') else {
        return result;
    };
    let Some(end) = rest[start + 1..].find(']') else {
        return result;
    };
    let body = &rest[start + 1..start + 1 + end];
    for part in body.split(',') {
        let trimmed = part.trim().trim_matches('"');
        if !trimmed.is_empty() {
            result.push(trimmed.to_string());
        }
    }
    result
}
