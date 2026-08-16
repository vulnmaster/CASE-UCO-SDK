//! Bounded frozen-context JSON-LD stream writer (#80).

use serde_json::Value;
use std::collections::{BTreeMap, HashMap};
use std::io::{BufWriter, Write};
use std::path::{Path, PathBuf};

const ABSOLUTE_SCHEMES: &[&str] = &["http", "https", "urn", "mailto", "file", "data", "did", "tag"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BoundedStreamingWriteMetrics {
    pub nodes: usize,
    pub bytes_written: u64,
    pub max_node_bytes_written: usize,
}

/// Incremental writer whose memory is bounded by `max_node_bytes` rather than
/// the total graph size. The explicit context is frozen before the first node.
pub struct JsonLdStreamWriter {
    target: PathBuf,
    temp: Option<tempfile::NamedTempFile>,
    writer: Option<BufWriter<std::fs::File>>,
    context: HashMap<String, String>,
    max_node_bytes: usize,
    atomic: bool,
    pretty: bool,
    nodes: usize,
    bytes_written: u64,
    max_node_bytes_written: usize,
    failed: bool,
}

impl JsonLdStreamWriter {
    pub fn new<P: AsRef<Path>>(
        path: P,
        context: HashMap<String, String>,
    ) -> std::io::Result<Self> {
        Self::with_options(path, context, 1_048_576, true, true)
    }

    pub fn with_options<P: AsRef<Path>>(
        path: P,
        context: HashMap<String, String>,
        max_node_bytes: usize,
        atomic: bool,
        pretty: bool,
    ) -> std::io::Result<Self> {
        if context.is_empty() {
            return Err(invalid("a non-empty frozen JSON-LD context is required"));
        }
        if max_node_bytes == 0 {
            return Err(invalid("max_node_bytes must be positive"));
        }
        let target = path.as_ref().to_path_buf();
        let parent = target.parent().unwrap_or_else(|| Path::new("."));
        std::fs::create_dir_all(parent)?;
        let (temp, file) = if atomic {
            let temp = tempfile::Builder::new()
                .prefix(&format!(".{}.", target.file_name().and_then(|s| s.to_str()).unwrap_or("casegraph")))
                .suffix(".jsonld.tmp")
                .tempfile_in(parent)?;
            let file = temp.reopen()?;
            (Some(temp), file)
        } else {
            (None, std::fs::File::create(&target)?)
        };
        let mut result = Self {
            target,
            temp,
            writer: Some(BufWriter::new(file)),
            context,
            max_node_bytes,
            atomic,
            pretty,
            nodes: 0,
            bytes_written: 0,
            max_node_bytes_written: 0,
            failed: false,
        };
        let sorted: BTreeMap<_, _> = result.context.iter().collect();
        let context_bytes = if pretty {
            serde_json::to_vec_pretty(&sorted).map_err(std::io::Error::other)?
        } else {
            serde_json::to_vec(&sorted).map_err(std::io::Error::other)?
        };
        result.emit(if pretty { b"{\"@context\": " } else { b"{\"@context\":" })?;
        result.emit(&context_bytes)?;
        result.emit(if pretty { b",\n\"@graph\": [\n" } else { b",\"@graph\":[" })?;
        Ok(result)
    }

    pub fn write_node(&mut self, node: &Value) -> std::io::Result<()> {
        if self.failed {
            return Err(invalid("writer is in a failed state"));
        }
        let outcome = (|| {
            if !node.is_object() {
                return Err(invalid("JSON-LD graph nodes must be objects"));
            }
            validate_prefixes(node, None, &self.context)?;
            if json_upper_bound(node) > self.max_node_bytes {
                return Err(invalid(&format!(
                    "node exceeds max_node_bytes={}",
                    self.max_node_bytes
                )));
            }
            let bytes = if self.pretty {
                serde_json::to_vec_pretty(node).map_err(std::io::Error::other)?
            } else {
                serde_json::to_vec(node).map_err(std::io::Error::other)?
            };
            if bytes.len() > self.max_node_bytes {
                return Err(invalid(&format!(
                    "node exceeds max_node_bytes={}",
                    self.max_node_bytes
                )));
            }
            if self.nodes > 0 {
                self.emit(if self.pretty { b",\n" } else { b"," })?;
            }
            self.emit(&bytes)?;
            self.nodes += 1;
            self.max_node_bytes_written = self.max_node_bytes_written.max(bytes.len());
            Ok(())
        })();
        if outcome.is_err() {
            self.failed = true;
        }
        outcome
    }

    pub fn metrics(&self) -> BoundedStreamingWriteMetrics {
        BoundedStreamingWriteMetrics {
            nodes: self.nodes,
            bytes_written: self.bytes_written,
            max_node_bytes_written: self.max_node_bytes_written,
        }
    }

    pub fn complete(mut self) -> std::io::Result<BoundedStreamingWriteMetrics> {
        if self.failed {
            return Err(invalid("cannot complete a failed writer"));
        }
        self.emit(if self.pretty { b"\n]\n}\n" } else { b"]}" })?;
        let mut writer = self
            .writer
            .take()
            .ok_or_else(|| invalid("writer is already closed"))?;
        writer.flush()?;
        writer.get_ref().sync_all()?;
        drop(writer);
        if self.atomic {
            let temp = self
                .temp
                .take()
                .ok_or_else(|| invalid("atomic writer is missing its temporary file"))?;
            temp.persist(&self.target).map_err(|e| e.error)?;
        }
        Ok(self.metrics())
    }

    fn emit(&mut self, bytes: &[u8]) -> std::io::Result<()> {
        self.writer
            .as_mut()
            .ok_or_else(|| invalid("writer is already closed"))?
            .write_all(bytes)?;
        self.bytes_written += bytes.len() as u64;
        Ok(())
    }
}

fn invalid(message: &str) -> std::io::Error {
    std::io::Error::new(std::io::ErrorKind::InvalidInput, message)
}

fn check_iri(value: &str, context: &HashMap<String, String>) -> std::io::Result<()> {
    let Some((prefix, _)) = value.split_once(':') else {
        return Ok(());
    };
    if !context.contains_key(prefix)
        && !ABSOLUTE_SCHEMES.iter().any(|scheme| scheme.eq_ignore_ascii_case(prefix))
    {
        return Err(invalid(&format!("undeclared JSON-LD prefix '{prefix}'")));
    }
    Ok(())
}

fn validate_prefixes(
    value: &Value,
    parent_key: Option<&str>,
    context: &HashMap<String, String>,
) -> std::io::Result<()> {
    match value {
        Value::Object(map) => {
            for (key, nested) in map {
                if !key.starts_with('@') {
                    check_iri(key, context)?;
                }
                if key == "@id" || key == "@type" {
                    if let Some(text) = nested.as_str() {
                        check_iri(text, context)?;
                    }
                }
                validate_prefixes(nested, Some(key), context)?;
            }
        }
        Value::Array(items) => {
            for item in items {
                if matches!(parent_key, Some("@id" | "@type")) {
                    if let Some(text) = item.as_str() {
                        check_iri(text, context)?;
                    }
                }
                validate_prefixes(item, parent_key, context)?;
            }
        }
        _ => {}
    }
    Ok(())
}

fn json_upper_bound(value: &Value) -> usize {
    match value {
        Value::Null => 4,
        Value::Bool(_) => 5,
        Value::Number(_) => 128,
        Value::String(s) => 2usize.saturating_add(6usize.saturating_mul(s.len())),
        Value::Array(items) => 2usize.saturating_add(
            items.iter().map(|item| json_upper_bound(item).saturating_add(1)).sum(),
        ),
        Value::Object(map) => 2usize.saturating_add(
            map.iter()
                .map(|(key, item)| {
                    json_upper_bound(&Value::String(key.clone()))
                        .saturating_add(1)
                        .saturating_add(json_upper_bound(item))
                        .saturating_add(1)
                })
                .sum(),
        ),
    }
}
