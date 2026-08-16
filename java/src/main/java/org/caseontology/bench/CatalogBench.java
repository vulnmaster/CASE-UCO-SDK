package org.caseontology.bench;

import org.caseontology.CaseGraph;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Full synthetic Java benchmark harness (#81). */
public final class CatalogBench {
    private CatalogBench() {}

    @FunctionalInterface
    private interface Workload {
        Map<String, Object> run() throws Exception;
    }

    public static void main(String[] args) throws Exception {
        String tier = option(args, "--tier", "small");
        String graphOut = option(args, "--graph-out", null);
        String repeatsOption = option(args, "--repeats", null);
        int n;
        if ("small".equals(tier)) n = 1_000;
        else if ("medium".equals(tier)) n = 10_000;
        else if ("large".equals(tier)) n = 100_000;
        else throw new IllegalArgumentException("Unknown tier '" + tier + "'");
        int repeats = repeatsOption == null
            ? ("large".equals(tier) ? 1 : 3)
            : Integer.parseInt(repeatsOption);
        if (repeats < 1) throw new IllegalArgumentException("--repeats must be positive");
        Path workdir = Paths.get(System.getProperty("java.io.tmpdir"), "case-uco-bench-java");
        Files.createDirectories(workdir);

        Map<String, Object> workloads = new LinkedHashMap<>();
        workloads.put("catalog", measure(() -> runCatalog(n), repeats));
        workloads.put("relationship_rich", measure(
            () -> runRelationshipRich(Math.max(10, n / 10)), repeats));
        workloads.put("deserialize_roundtrip", measure(() -> runDeserializeRoundtrip(n), repeats));
        workloads.put("streaming_write", measure(() -> runStreamingWrite(n, workdir), repeats));

        if (graphOut != null) {
            Path graphPath = Paths.get(graphOut).toAbsolutePath();
            if (graphPath.getParent() != null) Files.createDirectories(graphPath.getParent());
            buildCatalog(n).writeStreaming(graphPath.toString());
        }

        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("suite", "case-uco-synthetic-benchmark");
        doc.put("schema_version", "2.0.0");
        doc.put("tier", tier);
        doc.put("language", "java");
        doc.put("repeats", repeats);
        doc.put("process_peak_rss_bytes", processPeakRssBytes());
        doc.put("result", workloads);
        if (graphOut != null) doc.put("equivalence_graph", graphOut);
        System.out.println(toJson(doc, 0));
    }

    private static String option(String[] args, String name, String fallback) {
        for (int i = 0; i + 1 < args.length; i++) {
            if (name.equals(args[i])) return args[i + 1];
        }
        return fallback;
    }

    private static CaseGraph buildCatalog(int n) {
        CaseGraph graph = new CaseGraph();
        for (int i = 0; i < n; i++) {
            Map<String, Object> properties = new LinkedHashMap<>();
            properties.put("uco-core:name", "Tool-" + i);
            properties.put("uco-tool:version", "1.0");
            graph.upsertNode("kb:tool-" + i, "uco-tool:Tool", properties);
        }
        return graph;
    }

    private static Map<String, Object> runCatalog(int n) {
        long started = System.nanoTime();
        CaseGraph graph = buildCatalog(n);
        double buildSeconds = elapsed(started);
        started = System.nanoTime();
        int step = Math.max(1, n / 100);
        for (int i = 0; i < n; i += step) {
            if (!graph.contains("kb:tool-" + i)) throw new IllegalStateException("lookup failed");
            graph.addProperty("kb:tool-" + i, "uco-core:description", "bench-" + i);
        }
        double lookupSeconds = elapsed(started);
        started = System.nanoTime();
        String payload = graph.serialize();
        double serializeSeconds = elapsed(started);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("workload", "catalog");
        result.put("nodes", n);
        result.put("build_seconds", round(buildSeconds));
        result.put("lookup_enrich_seconds", round(lookupSeconds));
        result.put("serialize_seconds", round(serializeSeconds));
        result.put("serialize_bytes", payload.getBytes(StandardCharsets.UTF_8).length);
        result.put("estimate_triples", graph.estimateTriples());
        return result;
    }

    private static CaseGraph buildRelationshipRich(int n) {
        CaseGraph graph = new CaseGraph();
        for (int i = 0; i < n; i++) {
            String device = "kb:device-" + i;
            String file = "kb:file-" + i;
            graph.upsertNode(device, "uco-core:UcoObject", Map.of("uco-core:name", "D" + i));
            graph.upsertNode(file, "uco-core:UcoObject", Map.of(
                "uco-core:name", "F" + i,
                "uco-core:object", Map.of("@id", device)));
            graph.createRelationship(file, device, "Contained_Within");
        }
        return graph;
    }

    private static Map<String, Object> runRelationshipRich(int n) {
        long started = System.nanoTime();
        CaseGraph graph = buildRelationshipRich(n);
        double buildSeconds = elapsed(started);
        int step = Math.max(1, n / 10);
        List<String> roots = new ArrayList<>();
        for (int i = 0; i < n && roots.size() < 5; i += step) roots.add("kb:file-" + i);
        started = System.nanoTime();
        Map<String, CaseGraph> partitions = graph.partitionByRoots(
            roots, "replicate-identical", false);
        double partitionSeconds = elapsed(started);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("workload", "relationship_rich");
        result.put("nodes", graph.size());
        result.put("build_seconds", round(buildSeconds));
        result.put("partition_seconds", round(partitionSeconds));
        result.put("partition_count", partitions.size());
        result.put("estimate_triples", graph.estimateTriples());
        return result;
    }

    private static Map<String, Object> runDeserializeRoundtrip(int n) {
        String payload = buildCatalog(n).serialize();
        CaseGraph.clearClassRegistryCache();
        long started = System.nanoTime();
        CaseGraph cold = CaseGraph.fromJsonLd(payload).getGraph();
        double coldSeconds = elapsed(started);
        started = System.nanoTime();
        CaseGraph warm = CaseGraph.fromJsonLd(payload).getGraph();
        double warmSeconds = elapsed(started);
        if (cold.size() != n || warm.size() != n) throw new IllegalStateException("roundtrip failed");
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("workload", "deserialize_roundtrip");
        result.put("nodes", n);
        result.put("from_jsonld_cold_seconds", round(coldSeconds));
        result.put("from_jsonld_warm_seconds", round(warmSeconds));
        result.put("serialize_bytes", payload.getBytes(StandardCharsets.UTF_8).length);
        return result;
    }

    private static Map<String, Object> runStreamingWrite(int n, Path workdir) throws Exception {
        CaseGraph graph = buildCatalog(n);
        long started = System.nanoTime();
        CaseGraph.StreamingWriteResult metrics = graph.writeStreaming(
            workdir.resolve("stream.jsonld").toString());
        double streamSeconds = elapsed(started);
        started = System.nanoTime();
        graph.write(workdir.resolve("full.jsonld").toString());
        double fullSeconds = elapsed(started);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("workload", "streaming_write");
        result.put("nodes", n);
        result.put("write_streaming_seconds", round(streamSeconds));
        result.put("write_full_seconds", round(fullSeconds));
        result.put("bytes_written", metrics.getBytesWritten());
        return result;
    }

    private static Map<String, Object> measure(Workload workload, int repeats) throws Exception {
        List<Map<String, Object>> samples = new ArrayList<>();
        List<Long> heaps = new ArrayList<>();
        for (int run = 0; run < repeats; run++) {
            System.gc();
            samples.add(workload.run());
            Runtime runtime = Runtime.getRuntime();
            heaps.add(runtime.totalMemory() - runtime.freeMemory());
        }
        Map<String, Object> representative = new LinkedHashMap<>(samples.get(samples.size() / 2));
        Map<String, Object> dispersion = new LinkedHashMap<>();
        for (String key : samples.get(0).keySet()) {
            if (!key.endsWith("_seconds")) continue;
            List<Double> values = new ArrayList<>();
            for (Map<String, Object> sample : samples) values.add(((Number) sample.get(key)).doubleValue());
            Collections.sort(values);
            representative.put(key, round(median(values)));
            double mean = values.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
            double variance = values.stream().mapToDouble(value -> Math.pow(value - mean, 2)).average().orElse(0.0);
            Map<String, Object> metric = new LinkedHashMap<>();
            metric.put("min", round(values.get(0)));
            metric.put("max", round(values.get(values.size() - 1)));
            metric.put("median", round(median(values)));
            metric.put("mean", round(mean));
            metric.put("stdev", round(Math.sqrt(variance)));
            metric.put("p95", round(values.get((int) Math.floor((values.size() - 1) * 0.95))));
            dispersion.put(key, metric);
        }
        List<Double> heapDoubles = new ArrayList<>();
        for (Long value : heaps) heapDoubles.add(value.doubleValue());
        Collections.sort(heapDoubles);
        representative.put("samples", samples);
        representative.put("dispersion", dispersion);
        representative.put("memory", Map.of(
            "metric", "jvm_heap_after_bytes",
            "peak_bytes", Collections.max(heaps),
            "median_peak_bytes", (long) median(heapDoubles)));
        return representative;
    }

    private static double elapsed(long started) {
        return (System.nanoTime() - started) / 1_000_000_000.0;
    }

    private static double round(double value) {
        return Math.round(value * 1_000_000.0) / 1_000_000.0;
    }

    private static double median(List<Double> values) {
        int middle = values.size() / 2;
        return values.size() % 2 == 1
            ? values.get(middle)
            : (values.get(middle - 1) + values.get(middle)) / 2.0;
    }

    private static long processPeakRssBytes() {
        Path status = Paths.get("/proc/self/status");
        if (!Files.isReadable(status)) return -1L;
        try {
            for (String line : Files.readAllLines(status, StandardCharsets.UTF_8)) {
                if (line.startsWith("VmHWM:")) {
                    String digits = line.replaceAll("[^0-9]", "");
                    return Long.parseLong(digits) * 1024L;
                }
            }
        } catch (Exception ignored) {
            return -1L;
        }
        return -1L;
    }

    @SuppressWarnings("unchecked")
    private static String toJson(Object value, int indent) {
        String pad = "  ".repeat(indent);
        String childPad = "  ".repeat(indent + 1);
        if (value instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) value;
            StringBuilder sb = new StringBuilder("{\n");
            int i = 0;
            for (Map.Entry<String, Object> entry : map.entrySet()) {
                sb.append(childPad).append(quote(entry.getKey())).append(": ")
                    .append(toJson(entry.getValue(), indent + 1));
                if (++i < map.size()) sb.append(',');
                sb.append('\n');
            }
            return sb.append(pad).append('}').toString();
        }
        if (value instanceof Collection) {
            Collection<?> collection = (Collection<?>) value;
            StringBuilder sb = new StringBuilder("[\n");
            int i = 0;
            for (Object item : collection) {
                sb.append(childPad).append(toJson(item, indent + 1));
                if (++i < collection.size()) sb.append(',');
                sb.append('\n');
            }
            return sb.append(pad).append(']').toString();
        }
        if (value == null) return "null";
        if (value instanceof String) return quote((String) value);
        if (value instanceof Number || value instanceof Boolean) return String.valueOf(value);
        return quote(String.valueOf(value));
    }

    private static String quote(String value) {
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }
}
