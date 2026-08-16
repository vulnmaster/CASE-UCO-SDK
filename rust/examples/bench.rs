//! Full synthetic Rust benchmark harness (#81).

use case_uco::graph::CaseGraph;
use serde_json::{json, Map, Value};
use std::collections::BTreeMap;
use std::env;
use std::path::{Path, PathBuf};
use std::time::Instant;

fn option(args: &[String], name: &str) -> Option<String> {
    args.windows(2)
        .find(|pair| pair[0] == name)
        .map(|pair| pair[1].clone())
}

fn build_catalog(n: usize) -> CaseGraph {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    for i in 0..n {
        graph
            .upsert_node(
                &format!("kb:tool-{i}"),
                Some(json!("uco-tool:Tool")),
                json!({
                    "uco-core:name": format!("Tool-{i}"),
                    "uco-tool:version": "1.0"
                })
                .as_object()
                .cloned(),
            )
            .expect("catalog node");
    }
    graph
}

fn run_catalog(n: usize) -> Value {
    let started = Instant::now();
    let mut graph = build_catalog(n);
    let build_seconds = started.elapsed().as_secs_f64();
    let started = Instant::now();
    let step = (n / 100).max(1);
    for i in (0..n).step_by(step) {
        assert!(graph.contains(&format!("kb:tool-{i}")));
        graph
            .add_property(
                &format!("kb:tool-{i}"),
                "uco-core:description",
                json!(format!("bench-{i}")),
            )
            .expect("enrich");
    }
    let lookup_seconds = started.elapsed().as_secs_f64();
    let started = Instant::now();
    let payload = graph.serialize().expect("serialize");
    let serialize_seconds = started.elapsed().as_secs_f64();
    json!({
        "workload": "catalog",
        "nodes": n,
        "build_seconds": round(build_seconds),
        "lookup_enrich_seconds": round(lookup_seconds),
        "serialize_seconds": round(serialize_seconds),
        "serialize_bytes": payload.len(),
        "estimate_triples": graph.estimate_triples(),
    })
}

fn build_relationship_rich(n: usize) -> CaseGraph {
    let mut graph = CaseGraph::new("http://example.org/kb/");
    for i in 0..n {
        let device = format!("kb:device-{i}");
        let file = format!("kb:file-{i}");
        graph
            .upsert_node(
                &device,
                Some(json!("uco-core:UcoObject")),
                json!({"uco-core:name": format!("D{i}")})
                    .as_object()
                    .cloned(),
            )
            .expect("device");
        graph
            .upsert_node(
                &file,
                Some(json!("uco-core:UcoObject")),
                json!({
                    "uco-core:name": format!("F{i}"),
                    "uco-core:object": {"@id": device}
                })
                .as_object()
                .cloned(),
            )
            .expect("file");
        graph
            .create_relationship(&file, &device, "Contained_Within", true, None, None)
            .expect("relationship");
    }
    graph
}

fn run_relationship_rich(n: usize) -> Value {
    let started = Instant::now();
    let graph = build_relationship_rich(n);
    let build_seconds = started.elapsed().as_secs_f64();
    let step = (n / 10).max(1);
    let roots: Vec<String> = (0..n)
        .step_by(step)
        .take(5)
        .map(|i| format!("kb:file-{i}"))
        .collect();
    let options = case_uco::graph::PartitionOptions {
        include_incoming: false,
        ..Default::default()
    };
    let started = Instant::now();
    let parts = graph
        .partition_by_roots_with_manifest(&roots, &options)
        .expect("partition")
        .partitions;
    let partition_seconds = started.elapsed().as_secs_f64();
    json!({
        "workload": "relationship_rich",
        "nodes": graph.len(),
        "build_seconds": round(build_seconds),
        "partition_seconds": round(partition_seconds),
        "partition_count": parts.len(),
        "estimate_triples": graph.estimate_triples(),
    })
}

fn run_deserialize_roundtrip(n: usize) -> Value {
    let payload = build_catalog(n).serialize().expect("serialize");
    let started = Instant::now();
    let (cold, _) = CaseGraph::from_jsonld(&payload).expect("cold deserialize");
    let cold_seconds = started.elapsed().as_secs_f64();
    let started = Instant::now();
    let (warm, _) = CaseGraph::from_jsonld(&payload).expect("warm deserialize");
    let warm_seconds = started.elapsed().as_secs_f64();
    assert_eq!(cold.len(), n);
    assert_eq!(warm.len(), n);
    json!({
        "workload": "deserialize_roundtrip",
        "nodes": n,
        "from_jsonld_cold_seconds": round(cold_seconds),
        "from_jsonld_warm_seconds": round(warm_seconds),
        "serialize_bytes": payload.len(),
    })
}

fn run_streaming_write(n: usize, workdir: &Path) -> Value {
    let graph = build_catalog(n);
    let started = Instant::now();
    let metrics = graph
        .write_streaming(workdir.join("stream.jsonld").to_str().expect("path"))
        .expect("streaming write");
    let stream_seconds = started.elapsed().as_secs_f64();
    let started = Instant::now();
    graph
        .write(workdir.join("full.jsonld").to_str().expect("path"))
        .expect("full write");
    let full_seconds = started.elapsed().as_secs_f64();
    json!({
        "workload": "streaming_write",
        "nodes": n,
        "write_streaming_seconds": round(stream_seconds),
        "write_full_seconds": round(full_seconds),
        "bytes_written": metrics.bytes_written,
    })
}

fn measure<F>(mut workload: F, repeats: usize) -> Value
where
    F: FnMut() -> Value,
{
    let mut samples = Vec::new();
    let mut memory = Vec::new();
    for _ in 0..repeats {
        samples.push(workload());
        memory.push(process_memory_bytes("VmRSS:"));
    }
    let mut representative = samples[samples.len() / 2]
        .as_object()
        .cloned()
        .expect("workload object");
    let timing_keys: Vec<String> = representative
        .keys()
        .filter(|key| key.ends_with("_seconds"))
        .cloned()
        .collect();
    let mut dispersion = Map::new();
    for key in timing_keys {
        let mut values: Vec<f64> = samples
            .iter()
            .filter_map(|sample| sample.get(&key).and_then(Value::as_f64))
            .collect();
        values.sort_by(f64::total_cmp);
        let median_value = median(&values);
        let mean = values.iter().sum::<f64>() / values.len() as f64;
        let stdev = (values
            .iter()
            .map(|value| (value - mean).powi(2))
            .sum::<f64>()
            / values.len() as f64)
            .sqrt();
        representative.insert(key.clone(), json!(round(median_value)));
        dispersion.insert(
            key,
            json!({
                "min": round(values[0]),
                "max": round(values[values.len() - 1]),
                "median": round(median_value),
                "mean": round(mean),
                "stdev": round(stdev),
                "p95": round(values[((values.len() - 1) as f64 * 0.95).floor() as usize]),
            }),
        );
    }
    let mut valid_memory: Vec<u64> = memory.iter().copied().filter(|value| *value > 0).collect();
    valid_memory.sort();
    representative.insert("samples".into(), Value::Array(samples));
    representative.insert("dispersion".into(), Value::Object(dispersion));
    representative.insert(
        "memory".into(),
        json!({
            "metric": "process_rss_after_bytes",
            "peak_bytes": valid_memory.last().copied().unwrap_or(0),
            "median_peak_bytes": valid_memory.get(valid_memory.len().saturating_sub(1) / 2).copied().unwrap_or(0),
        }),
    );
    Value::Object(representative)
}

fn process_memory_bytes(label: &str) -> u64 {
    let Ok(status) = std::fs::read_to_string("/proc/self/status") else {
        return 0;
    };
    status
        .lines()
        .find(|line| line.starts_with(label))
        .and_then(|line| line.split_whitespace().nth(1))
        .and_then(|value| value.parse::<u64>().ok())
        .map(|kib| kib * 1024)
        .unwrap_or(0)
}

fn median(values: &[f64]) -> f64 {
    if values.len() % 2 == 1 {
        values[values.len() / 2]
    } else {
        (values[values.len() / 2 - 1] + values[values.len() / 2]) / 2.0
    }
}

fn round(value: f64) -> f64 {
    (value * 1_000_000.0).round() / 1_000_000.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let tier = option(&args, "--tier").unwrap_or_else(|| "small".to_string());
    let graph_out = option(&args, "--graph-out");
    let n = match tier.as_str() {
        "small" => 1_000,
        "medium" => 10_000,
        "large" => 100_000,
        other => {
            eprintln!("Unknown tier '{other}', expected small|medium|large");
            std::process::exit(2);
        }
    };
    let repeats = option(&args, "--repeats")
        .map(|value| value.parse::<usize>().expect("positive repeat count"))
        .unwrap_or(if tier == "large" { 1 } else { 3 });
    assert!(repeats > 0, "--repeats must be positive");
    let workdir = PathBuf::from(env::temp_dir()).join("case-uco-bench-rust");
    std::fs::create_dir_all(&workdir).expect("workdir");

    let mut workloads = BTreeMap::new();
    workloads.insert("catalog", measure(|| run_catalog(n), repeats));
    workloads.insert(
        "relationship_rich",
        measure(|| run_relationship_rich((n / 10).max(10)), repeats),
    );
    workloads.insert(
        "deserialize_roundtrip",
        measure(|| run_deserialize_roundtrip(n), repeats),
    );
    workloads.insert(
        "streaming_write",
        measure(|| run_streaming_write(n, &workdir), repeats),
    );
    if let Some(path) = &graph_out {
        let path = PathBuf::from(path);
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).expect("graph parent");
        }
        build_catalog(n)
            .write_streaming(path.to_str().expect("graph path"))
            .expect("equivalence graph");
    }
    let result = json!({
        "suite": "case-uco-synthetic-benchmark",
        "schema_version": "2.0.0",
        "tier": tier,
        "language": "rust",
        "repeats": repeats,
        "process_peak_rss_bytes": process_memory_bytes("VmHWM:"),
        "result": workloads,
        "equivalence_graph": graph_out,
    });
    println!("{}", serde_json::to_string_pretty(&result).expect("json"));
}
