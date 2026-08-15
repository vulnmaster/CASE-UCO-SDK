//! Fluent composition helpers derived from Composition Profiles.

use crate::case::investigation::InvestigativeAction;
use crate::graph::{CaseGraph, GraphError};
use crate::uco::observable::{ContentDataFacet, FileFacet, RasterPicture, RasterPictureFacet};
use crate::uco::tool::Tool;
use serde_json::{json, Value};

pub struct CsamEvidence {
    pub tool_id: String,
    pub picture_id: String,
    pub action_id: String,
}

pub struct ToolRun {
    pub tool_id: String,
    pub action_id: String,
}

fn hash_entry(method: &str, value: &str) -> Value {
    json!({
        "@type": "uco-types:Hash",
        "uco-types:hashMethod": method,
        "uco-types:hashValue": { "@type": "xsd:hexBinary", "@value": value },
    })
}

fn hashes_json(hashes: &[(&str, &str)]) -> Value {
    Value::Array(hashes.iter().map(|(m, v)| hash_entry(m, v)).collect())
}

/// ObservableObject-equivalent RasterPicture + FileFacet + ContentDataFacet.
pub fn file_with_content_hashes(
    graph: &mut CaseGraph,
    file_name: &str,
    hashes: &[(&str, &str)],
) -> Result<String, GraphError> {
    let picture = RasterPicture::builder().build();
    let id = graph.create(&picture);
    let file_facet = FileFacet::builder()
        .file_name(vec![file_name.to_string()])
        .build();
    let file_id = graph.create(&file_facet);
    let content = ContentDataFacet::builder().build();
    let content_id = graph.create(&content);
    graph.add_property(&content_id, "uco-observable:hash", hashes_json(hashes))?;
    graph.add_property(
        &id,
        "uco-core:hasFacet",
        json!([{ "@id": file_id }, { "@id": content_id }]),
    )?;
    Ok(id)
}

pub fn raster_picture_with_hashes(
    graph: &mut CaseGraph,
    file_name: &str,
    hashes: &[(&str, &str)],
) -> Result<String, GraphError> {
    let picture = RasterPicture::builder().build();
    let id = graph.create(&picture);
    let file_facet = FileFacet::builder()
        .file_name(vec![file_name.to_string()])
        .build();
    let file_id = graph.create(&file_facet);
    let content = ContentDataFacet::builder().build();
    let content_id = graph.create(&content);
    graph.add_property(&content_id, "uco-observable:hash", hashes_json(hashes))?;
    let raster = RasterPictureFacet::builder().build();
    let raster_id = graph.create(&raster);
    graph.add_property(
        &id,
        "uco-core:hasFacet",
        json!([
            { "@id": file_id },
            { "@id": content_id },
            { "@id": raster_id }
        ]),
    )?;
    Ok(id)
}

pub fn model_csam_evidence(
    graph: &mut CaseGraph,
    file_name: &str,
    hashes: &[(&str, &str)],
    hashing_tool_name: &str,
    hashing_tool_version: Option<&str>,
) -> Result<CsamEvidence, GraphError> {
    let mut tool = Tool::builder().tool_type("Content hashing".to_string());
    if let Some(v) = hashing_tool_version {
        tool = tool.version(v.to_string());
    }
    let tool_id = graph.create(&tool.build());
    graph.add_property(&tool_id, "uco-core:name", json!(hashing_tool_name))?;
    let picture_id = raster_picture_with_hashes(graph, file_name, hashes)?;
    let action = InvestigativeAction::builder().build();
    let action_id = graph.create(&action);
    graph.add_property(
        &action_id,
        "uco-core:name",
        json!(format!("{hashing_tool_name} hash of {file_name}")),
    )?;
    graph.add_property(&action_id, "uco-action:instrument", json!([{ "@id": tool_id }]))?;
    graph.add_property(&action_id, "uco-action:object", json!([{ "@id": picture_id }]))?;
    graph.add_property(&action_id, "uco-action:result", json!([{ "@id": picture_id }]))?;
    Ok(CsamEvidence {
        tool_id,
        picture_id,
        action_id,
    })
}

pub fn model_tool_run(
    graph: &mut CaseGraph,
    tool_name: &str,
    action_name: &str,
    tool_version: Option<&str>,
) -> Result<ToolRun, GraphError> {
    let mut tool = Tool::builder();
    if let Some(v) = tool_version {
        tool = tool.version(v.to_string());
    }
    let tool_id = graph.create(&tool.build());
    graph.add_property(&tool_id, "uco-core:name", json!(tool_name))?;
    let action_id = graph.create(&InvestigativeAction::builder().build());
    graph.add_property(&action_id, "uco-core:name", json!(action_name))?;
    graph.add_property(&action_id, "uco-action:instrument", json!([{ "@id": tool_id }]))?;
    Ok(ToolRun { tool_id, action_id })
}
