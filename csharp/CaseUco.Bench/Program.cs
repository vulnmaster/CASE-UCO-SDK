// Full synthetic C# benchmark harness (#81).
using System.Diagnostics;
using System.Text;
using System.Text.Json;
using CaseUco;

var tier = Option(args, "--tier") ?? "small";
var graphOut = Option(args, "--graph-out");
var repeatsText = Option(args, "--repeats");
var n = tier switch
{
    "small" => 1_000,
    "medium" => 10_000,
    "large" => 100_000,
    _ => throw new ArgumentException($"Unknown tier '{tier}'"),
};
var repeats = repeatsText == null ? (tier == "large" ? 1 : 3) : int.Parse(repeatsText);
if (repeats < 1) throw new ArgumentOutOfRangeException(nameof(repeats));
var workdir = Path.Join(Path.GetTempPath(), "case-uco-bench-csharp");
Directory.CreateDirectory(workdir);

var workloads = new Dictionary<string, object?>
{
    ["catalog"] = Measure(() => RunCatalog(n), repeats),
    ["relationship_rich"] = Measure(() => RunRelationshipRich(Math.Max(10, n / 10)), repeats),
    ["deserialize_roundtrip"] = Measure(() => RunDeserializeRoundtrip(n), repeats),
    ["streaming_write"] = Measure(() => RunStreamingWrite(n, workdir), repeats),
};

if (graphOut != null)
{
    var parent = Path.GetDirectoryName(Path.GetFullPath(graphOut));
    if (!string.IsNullOrEmpty(parent)) Directory.CreateDirectory(parent);
    BuildCatalog(n).WriteStreaming(graphOut);
}

var result = new Dictionary<string, object?>
{
    ["suite"] = "case-uco-synthetic-benchmark",
    ["schema_version"] = "2.0.0",
    ["tier"] = tier,
    ["language"] = "csharp",
    ["repeats"] = repeats,
    ["process_peak_rss_bytes"] = Process.GetCurrentProcess().PeakWorkingSet64,
    ["result"] = workloads,
};
if (graphOut != null) result["equivalence_graph"] = graphOut;
Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));

static string? Option(string[] arguments, string name)
{
    for (var i = 0; i + 1 < arguments.Length; i++)
        if (arguments[i] == name) return arguments[i + 1];
    return null;
}

static CaseGraph BuildCatalog(int n)
{
    var graph = new CaseGraph();
    for (var i = 0; i < n; i++)
        graph.UpsertNode($"kb:tool-{i}", "uco-tool:Tool", new Dictionary<string, object>
        {
            ["uco-core:name"] = $"Tool-{i}",
            ["uco-tool:version"] = "1.0",
        });
    return graph;
}

static Dictionary<string, object?> RunCatalog(int n)
{
    var timer = Stopwatch.StartNew();
    var graph = BuildCatalog(n);
    var buildSeconds = timer.Elapsed.TotalSeconds;
    timer.Restart();
    var step = Math.Max(1, n / 100);
    for (var i = 0; i < n; i += step)
    {
        if (!graph.Contains($"kb:tool-{i}")) throw new InvalidOperationException("lookup failed");
        graph.AddProperty($"kb:tool-{i}", "uco-core:description", $"bench-{i}");
    }
    var lookupSeconds = timer.Elapsed.TotalSeconds;
    timer.Restart();
    var payload = graph.Serialize();
    var serializeSeconds = timer.Elapsed.TotalSeconds;
    return new Dictionary<string, object?>
    {
        ["workload"] = "catalog",
        ["nodes"] = n,
        ["build_seconds"] = Round(buildSeconds),
        ["lookup_enrich_seconds"] = Round(lookupSeconds),
        ["serialize_seconds"] = Round(serializeSeconds),
        ["serialize_bytes"] = Encoding.UTF8.GetByteCount(payload),
        ["estimate_triples"] = graph.EstimateTriples(),
    };
}

static CaseGraph BuildRelationshipRich(int n)
{
    var graph = new CaseGraph();
    for (var i = 0; i < n; i++)
    {
        var device = $"kb:device-{i}";
        var file = $"kb:file-{i}";
        graph.UpsertNode(device, "uco-core:UcoObject", new Dictionary<string, object>
        {
            ["uco-core:name"] = $"D{i}",
        });
        graph.UpsertNode(file, "uco-core:UcoObject", new Dictionary<string, object>
        {
            ["uco-core:name"] = $"F{i}",
            ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = device },
        });
        graph.CreateRelationship(file, device, "Contained_Within");
    }
    return graph;
}

static Dictionary<string, object?> RunRelationshipRich(int n)
{
    var timer = Stopwatch.StartNew();
    var graph = BuildRelationshipRich(n);
    var buildSeconds = timer.Elapsed.TotalSeconds;
    var step = Math.Max(1, n / 10);
    var roots = Enumerable.Range(0, n).Where(i => i % step == 0)
        .Take(5).Select(i => $"kb:file-{i}").ToArray();
    timer.Restart();
    var parts = graph.PartitionByRoots(roots, "replicate-identical", includeIncoming: false);
    var partitionSeconds = timer.Elapsed.TotalSeconds;
    return new Dictionary<string, object?>
    {
        ["workload"] = "relationship_rich",
        ["nodes"] = graph.Count,
        ["build_seconds"] = Round(buildSeconds),
        ["partition_seconds"] = Round(partitionSeconds),
        ["partition_count"] = parts.Count,
        ["estimate_triples"] = graph.EstimateTriples(),
    };
}

static Dictionary<string, object?> RunDeserializeRoundtrip(int n)
{
    var payload = BuildCatalog(n).Serialize();
    CaseGraph.ClearClassRegistryCache();
    var timer = Stopwatch.StartNew();
    var cold = CaseGraph.FromJsonLd(payload).Graph;
    var coldSeconds = timer.Elapsed.TotalSeconds;
    timer.Restart();
    var warm = CaseGraph.FromJsonLd(payload).Graph;
    var warmSeconds = timer.Elapsed.TotalSeconds;
    if (cold.Count != n || warm.Count != n) throw new InvalidOperationException("roundtrip failed");
    return new Dictionary<string, object?>
    {
        ["workload"] = "deserialize_roundtrip",
        ["nodes"] = n,
        ["from_jsonld_cold_seconds"] = Round(coldSeconds),
        ["from_jsonld_warm_seconds"] = Round(warmSeconds),
        ["serialize_bytes"] = Encoding.UTF8.GetByteCount(payload),
    };
}

static Dictionary<string, object?> RunStreamingWrite(int n, string workdir)
{
    var graph = BuildCatalog(n);
    var timer = Stopwatch.StartNew();
    var metrics = graph.WriteStreaming(Path.Join(workdir, "stream.jsonld"));
    var streamSeconds = timer.Elapsed.TotalSeconds;
    timer.Restart();
    graph.Write(Path.Join(workdir, "full.jsonld"));
    var fullSeconds = timer.Elapsed.TotalSeconds;
    return new Dictionary<string, object?>
    {
        ["workload"] = "streaming_write",
        ["nodes"] = n,
        ["write_streaming_seconds"] = Round(streamSeconds),
        ["write_full_seconds"] = Round(fullSeconds),
        ["bytes_written"] = metrics.BytesWritten,
    };
}

static Dictionary<string, object?> Measure(Func<Dictionary<string, object?>> workload, int repeats)
{
    var samples = new List<Dictionary<string, object?>>();
    var heapSamples = new List<long>();
    for (var run = 0; run < repeats; run++)
    {
        GC.Collect();
        GC.WaitForPendingFinalizers();
        samples.Add(workload());
        heapSamples.Add(GC.GetGCMemoryInfo().HeapSizeBytes);
    }
    var representative = new Dictionary<string, object?>(samples[samples.Count / 2]);
    var dispersion = new Dictionary<string, object?>();
    foreach (var key in samples[0].Keys.Where(key => key.EndsWith("_seconds", StringComparison.Ordinal)))
    {
        var values = samples.Select(sample => Convert.ToDouble(sample[key])).OrderBy(value => value).ToArray();
        representative[key] = Round(Median(values));
        dispersion[key] = new Dictionary<string, object?>
        {
            ["min"] = Round(values[0]),
            ["max"] = Round(values[^1]),
            ["median"] = Round(Median(values)),
            ["mean"] = Round(values.Average()),
            ["stdev"] = Round(Math.Sqrt(values.Select(value => Math.Pow(value - values.Average(), 2)).Average())),
            ["p95"] = Round(values[(int)Math.Floor((values.Length - 1) * 0.95)]),
        };
    }
    representative["samples"] = samples;
    representative["dispersion"] = dispersion;
    representative["memory"] = new Dictionary<string, object?>
    {
        ["metric"] = "dotnet_managed_heap_after_bytes",
        ["peak_bytes"] = heapSamples.Max(),
        ["median_peak_bytes"] = (long)Median(heapSamples.Select(value => (double)value).OrderBy(value => value).ToArray()),
    };
    return representative;
}

static double Median(double[] values) => values.Length % 2 == 1
    ? values[values.Length / 2]
    : (values[values.Length / 2 - 1] + values[values.Length / 2]) / 2.0;
static double Round(double value) => Math.Round(value, 6);
