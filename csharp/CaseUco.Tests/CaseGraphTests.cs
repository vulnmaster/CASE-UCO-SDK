// Tests for CaseGraph builder and JSON-LD serialization.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using CaseUco;
using CaseUco.Uco.Tool;
using CaseUco.Uco.Observable;
using Xunit;

namespace CaseUco.Tests
{
    public class CaseGraphTests
    {
        public class DynamicExtension
        {
            public const string ClassIri = "https://example.org/dynamic/DynamicExtension";
            public const string NamespacePrefix = "dyn";
            [JsonLdProperty("dyn:value")]
            public string Value { get; set; }
        }

        public class ConflictingToolExtension
        {
            public const string ClassIri = Tool.ClassIri;
        }

        [Fact]
        public void CreateTool_ProducesValidJsonLd()
        {
            var graph = new CaseGraph();
            var tool = new Tool { Name = "Tool A", Version = "7.0" };
            var id = graph.Add(tool);

            Assert.StartsWith("kb:Tool-", id);
            var json = graph.Serialize();
            Assert.Contains("uco-tool:Tool", json);
            Assert.Contains("uco-core:name", json);
            Assert.DoesNotContain("uco-tool:name", json);
            Assert.Contains("@context", json);
            Assert.Contains("@graph", json);
        }

        [Fact]
        public void GetId_ReturnsAssignedId()
        {
            var graph = new CaseGraph();
            var tool = new Tool();
            var id = graph.Add(tool);
            Assert.Equal(id, graph.GetId(tool));
        }

        [Fact]
        public void AddWithId_UsesDeterministicId()
        {
            var graph = new CaseGraph();
            var tool = new Tool { Name = "Tool A" };
            var id = graph.AddWithId(tool, "kb:Tool-my-stable-id");

            Assert.Equal("kb:Tool-my-stable-id", id);
            Assert.Equal("kb:Tool-my-stable-id", graph.GetId(tool));
            var json = graph.Serialize();
            Assert.Contains("kb:Tool-my-stable-id", json);
        }

        [Fact]
        public void CustomKbPrefix_ReflectedInContext()
        {
            var graph = new CaseGraph("http://mylab.example.org/case/");
            graph.Add(new Tool { Name = "Tool A" });
            var json = graph.Serialize();
            Assert.Contains("http://mylab.example.org/case/", json);
        }

        [Fact]
        public void MultipleObjects_AllSerialized()
        {
            var graph = new CaseGraph();
            graph.Add(new Tool());
            graph.Add(new AnalyticTool());
            var json = graph.Serialize();

            using var doc = JsonDocument.Parse(json);
            var graphArray = doc.RootElement.GetProperty("@graph");
            Assert.Equal(2, graphArray.GetArrayLength());
        }

        [Fact]
        public void BooleanProperties_AreTypedLiterals()
        {
            var graph = new CaseGraph();
            graph.Add(new ObservableObject { HasChanged = true });
            var json = graph.Serialize();
            Assert.Contains("\"@type\":\"xsd:boolean\"", json.Replace(" ", ""));
            Assert.Contains("\"uco-observable:hasChanged\"", json);
        }

        [Fact]
        public void Count_TracksObjects()
        {
            var graph = new CaseGraph();
            Assert.Equal(0, graph.Count);
            graph.Add(new Tool());
            Assert.Equal(1, graph.Count);
            graph.Add(new Tool());
            Assert.Equal(2, graph.Count);
        }

        [Fact]
        public void ContextPrunesUnusedPrefixes()
        {
            var graph = new CaseGraph();
            graph.Add(new Tool { Name = "Tool A" });
            var json = graph.Serialize();

            using var doc = JsonDocument.Parse(json);
            var ctx = doc.RootElement.GetProperty("@context");

            Assert.True(ctx.TryGetProperty("kb", out _), "used prefix kb should be present");
            Assert.True(ctx.TryGetProperty("uco-tool", out _), "used prefix uco-tool should be present");
            Assert.True(ctx.TryGetProperty("uco-core", out _), "used prefix uco-core should be present");

            var unused = new[] { "uco-identity", "uco-location", "uco-role", "uco-victim",
                                 "uco-configuration", "uco-marking", "uco-pattern", "uco-time" };
            foreach (var prefix in unused)
            {
                Assert.False(ctx.TryGetProperty(prefix, out _), $"unused prefix should be pruned: {prefix}");
            }
        }

        [Fact]
        public void EmptyGraphHasEmptyContext()
        {
            var graph = new CaseGraph();
            var json = graph.Serialize();

            using var doc = JsonDocument.Parse(json);
            var ctx = doc.RootElement.GetProperty("@context");
            int count = 0;
            foreach (var _ in ctx.EnumerateObject()) count++;
            Assert.Equal(0, count);
        }

        [Fact]
        public void Load_MergesContextAndObjects()
        {
            var graph = new CaseGraph();
            var inputJson = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""uco-tool"": ""https://ontology.unifiedcyberontology.org/uco/tool/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:Tool-existing-001"",
                        ""@type"": ""uco-tool:Tool""
                    }
                ]
            }";

            graph.Load(inputJson);
            Assert.Equal(1, graph.Count);

            var json = graph.Serialize();
            Assert.Contains("kb:Tool-existing-001", json);
        }

        [Fact]
        public void Load_ThenAdd_CombinesObjects()
        {
            var graph = new CaseGraph();
            graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"" }, ""@graph"": [ { ""@id"": ""kb:Tool-loaded"", ""@type"": ""uco-tool:Tool"" } ] }");
            graph.Add(new Tool { Name = "New Tool" });
            Assert.Equal(2, graph.Count);
        }

        [Fact]
        public void Get_ReturnsDeepCopy()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:n1", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "N",
                ["uco-core:tag"] = new List<object> { "a", "b" },
                ["uco-core:hasFacet"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = "kb:f1" },
                },
            });
            var view = graph.Get("kb:n1");
            view["@id"] = "kb:mutated";
            ((List<object>)view["uco-core:tag"]).Add("c");
            ((Dictionary<string, object>)((List<object>)view["uco-core:hasFacet"])[0])["@id"] = "kb:mutated-facet";
            Assert.True(graph.Contains("kb:n1"));
            Assert.False(graph.Contains("kb:mutated"));
            Assert.Equal("N", graph.Get("kb:n1")["uco-core:name"]);
            Assert.Equal(2, ((List<object>)graph.Get("kb:n1")["uco-core:tag"]).Count);
            Assert.Equal("kb:f1", ((Dictionary<string, object>)((List<object>)graph.Get("kb:n1")["uco-core:hasFacet"])[0])["@id"]);
        }

        [Fact]
        public void Split_RejectsNonPositive()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:x", "uco-core:UcoObject");
            Assert.Throws<ArgumentOutOfRangeException>(() => graph.Split(0));
        }

        [Fact]
        public void Load_RejectsDuplicateByDefault()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:x", "uco-core:UcoObject");
            Assert.Throws<InvalidOperationException>(() =>
                graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"" }, ""@graph"": [ { ""@id"": ""kb:x"", ""@type"": ""uco-core:UcoObject"" } ] }"));
        }

        [Fact]
        public void Load_RejectsContextCollision()
        {
            var graph = new CaseGraph();
            Assert.Throws<ArgumentException>(() =>
                graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"", ""uco-core"": ""https://evil.example.org/uco/core/"" }, ""@graph"": [] }"));
        }

        private const string CustomKb = "http://example.org/kb/case-42/";

        private static string CustomKbJson()
        {
            var graph = new CaseGraph(CustomKb);
            graph.Add(new Tool { Name = "Custom KB Tool" });
            return graph.Serialize();
        }

        private static string ContextKb(string json)
        {
            using var doc = JsonDocument.Parse(json);
            return doc.RootElement.GetProperty("@context").GetProperty("kb").GetString();
        }

        [Fact]
        public void FromJsonLd_CustomKbPrefixRoundTrip()
        {
            // The SDK's own output with a custom kb reads back.
            var result = CaseGraph.FromJsonLd(CustomKbJson());
            Assert.Single(result.Objects);
            Assert.Equal(CustomKb, ContextKb(result.Graph.Serialize()));
        }

        [Fact]
        public void Load_CustomKbPrefixIntoEmptyGraph()
        {
            var graph = new CaseGraph();
            graph.Load(CustomKbJson());
            Assert.Equal(1, graph.Count);
            Assert.Equal(CustomKb, ContextKb(graph.Serialize()));
        }

        [Fact]
        public void Load_CustomKbPrefixIntoPopulatedGraphStillCollides()
        {
            var graph = new CaseGraph();
            graph.Add(new Tool { Name = "Existing Tool" });
            var ex = Assert.Throws<ArgumentException>(() => graph.Load(CustomKbJson()));
            Assert.Contains("Context prefix collision for 'kb'", ex.Message);
            Assert.Equal(1, graph.Count);
        }

        [Fact]
        public void Load_MergeCompatible_ScalarConflictRaises()
        {
            var graph = new CaseGraph();
            graph.RejectDuplicates = false;
            graph.UpsertNode("kb:x", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "A",
            });
            Assert.Throws<InvalidOperationException>(() =>
                graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"" }, ""@graph"": [ { ""@id"": ""kb:x"", ""@type"": ""uco-core:UcoObject"", ""uco-core:name"": ""B"" } ] }"));
        }

        [Fact]
        public void ClearClassRegistryCache_DoesNotBreakFromJsonLd()
        {
            var json = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""uco-tool"": ""https://ontology.unifiedcyberontology.org/uco/tool/"",
                    ""uco-core"": ""https://ontology.unifiedcyberontology.org/uco/core/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:Tool-1"",
                        ""@type"": ""uco-tool:Tool"",
                        ""uco-core:name"": ""Cached""
                    }
                ]
            }";

            var first = CaseGraph.FromJsonLd(json);
            Assert.IsType<Tool>(first.Objects[0]);
            CaseGraph.ClearClassRegistryCache();
            var second = CaseGraph.FromJsonLd(json);
            Assert.IsType<Tool>(second.Objects[0]);
        }

        [Fact]
        public void PropertyBindingCache_WarmPath()
        {
            CaseGraph.ClearClassRegistryCache();
            Assert.Equal(0, CaseGraph.PropertyBindingCacheCount);

            var json = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""uco-tool"": ""https://ontology.unifiedcyberontology.org/uco/tool/"",
                    ""uco-core"": ""https://ontology.unifiedcyberontology.org/uco/core/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:Tool-warm"",
                        ""@type"": ""uco-tool:Tool"",
                        ""uco-core:name"": ""Warm""
                    }
                ]
            }";

            CaseGraph.FromJsonLd(json);
            var afterCold = CaseGraph.PropertyBindingCacheCount;
            Assert.True(afterCold > 0);
            CaseGraph.FromJsonLd(json);
            Assert.Equal(afterCold, CaseGraph.PropertyBindingCacheCount);
            CaseGraph.ClearClassRegistryCache();
            Assert.Equal(0, CaseGraph.PropertyBindingCacheCount);
        }

        [Fact]
        public void ExtensionAssemblyRegistration_InvalidatesAndReportsMetrics()
        {
            const string source = "case-uco-tests-dynamic";
            CaseGraph.UnregisterExtensionAssembly(source);
            CaseGraph.ClearClassRegistryCache();
            var before = CaseGraph.GetClassRegistryCacheMetrics();
            var generation = CaseGraph.RegisterExtensionTypes(
                new[] { typeof(DynamicExtension) }, source);
            Assert.True(generation > before.Generation);

            var json = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""dyn"": ""https://example.org/dynamic/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:dynamic"",
                        ""@type"": ""dyn:DynamicExtension"",
                        ""dyn:value"": ""loaded without restart""
                    }
                ]
            }";
            var first = CaseGraph.FromJsonLd(json);
            var second = CaseGraph.FromJsonLd(json);
            Assert.IsType<DynamicExtension>(first.Objects[0]);
            Assert.IsType<DynamicExtension>(second.Objects[0]);
            var info = CaseGraph.GetClassRegistryCacheMetrics();
            Assert.True(info.Hits > before.Hits);
            Assert.True(info.RegisteredExtensions >= 1);

            CaseGraph.UnregisterExtensionAssembly(source);
            var raw = CaseGraph.FromJsonLd(json);
            Assert.IsType<Dictionary<string, object>>(raw.Objects[0]);
        }

        [Fact]
        public void ExtensionAssemblyRegistration_RejectsBuiltinConflict()
        {
            Assert.Throws<ClassRegistryConflictException>(() =>
                CaseGraph.RegisterExtensionTypes(
                    new[] { typeof(ConflictingToolExtension) },
                    "case-uco-tests-conflict"));
            CaseGraph.UnregisterExtensionAssembly("case-uco-tests-conflict");
        }

        [Fact]
        public void WriteStreaming_Roundtrip()
        {
            var graph = new CaseGraph();
            graph.AddWithId(new Tool { Name = "Streamed" }, "kb:t-stream");
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-stream-{Guid.NewGuid()}.jsonld");
            try
            {
                var metrics = graph.WriteStreaming(path);
                Assert.Equal(1, metrics.Nodes);
                Assert.True(metrics.BytesWritten > 0);
                var loaded = new CaseGraph();
                loaded.OnDuplicate = "merge_compatible";
                loaded.Load(System.IO.File.ReadAllText(path));
                Assert.Equal("Streamed", loaded.Get("kb:t-stream")["uco-core:name"]);
            }
            finally
            {
                if (System.IO.File.Exists(path))
                    System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void BoundedWriter_StreamsFrozenContextAndCapsNodes()
        {
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-bounded-{Guid.NewGuid()}.jsonld");
            try
            {
                var context = new Dictionary<string, string>
                {
                    ["kb"] = "https://example.org/kb/",
                    ["uco-core"] = "https://ontology.unifiedcyberontology.org/uco/core/",
                };
                BoundedStreamingWriteResult metrics;
                using (var writer = new JsonLdStreamWriter(path, context, maxNodeBytes: 1024))
                {
                    for (var i = 0; i < 100; i++)
                    {
                        writer.WriteNode(new Dictionary<string, object>
                        {
                            ["@id"] = $"kb:node-{i}",
                            ["@type"] = "uco-core:UcoObject",
                            ["uco-core:name"] = $"Node {i}",
                        });
                    }
                    metrics = writer.Metrics;
                }
                using var doc = JsonDocument.Parse(System.IO.File.ReadAllText(path));
                Assert.Equal(100, doc.RootElement.GetProperty("@graph").GetArrayLength());
                Assert.Equal(100, metrics.Nodes);
                Assert.True(metrics.MaxNodeBytesWritten <= 1024);
            }
            finally
            {
                if (System.IO.File.Exists(path)) System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void BoundedWriter_FailurePreservesExistingDestination()
        {
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-bounded-fail-{Guid.NewGuid()}.jsonld");
            System.IO.File.WriteAllText(path, "SURVIVE");
            try
            {
                var context = new Dictionary<string, string>
                {
                    ["kb"] = "https://example.org/kb/",
                    ["uco-core"] = "https://ontology.unifiedcyberontology.org/uco/core/",
                };
                Assert.Throws<ArgumentException>(() =>
                {
                    using var writer = new JsonLdStreamWriter(path, context, maxNodeBytes: 128);
                    writer.WriteNode(new Dictionary<string, object>
                    {
                        ["@id"] = "kb:bad",
                        ["@type"] = "evil:Fabricated",
                    });
                });
                Assert.Equal("SURVIVE", System.IO.File.ReadAllText(path));

                Assert.Throws<InvalidOperationException>(() =>
                {
                    using var writer = new JsonLdStreamWriter(path, context, maxNodeBytes: 128);
                    writer.WriteNode(new Dictionary<string, object>
                    {
                        ["@id"] = "kb:large",
                        ["@type"] = "uco-core:UcoObject",
                        ["uco-core:name"] = new string('x', 1000),
                    });
                });
                Assert.Equal("SURVIVE", System.IO.File.ReadAllText(path));
            }
            finally
            {
                if (System.IO.File.Exists(path)) System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void WriteStreaming_ReplacesExistingWithoutDeleteFirst()
        {
            // Atomic WriteStreaming must replace in place via temp+File.Replace/Move,
            // not delete-then-write (which races readers and loses the prior file on failure).
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-replace-{Guid.NewGuid()}.jsonld");
            try
            {
                System.IO.File.WriteAllText(path, "OLD");
                Assert.Equal("OLD", System.IO.File.ReadAllText(path));

                var v1 = new CaseGraph();
                v1.AddWithId(new Tool { Name = "V1" }, "kb:t-replace");
                v1.WriteStreaming(path);
                Assert.Contains("V1", System.IO.File.ReadAllText(path));
                Assert.DoesNotContain("OLD", System.IO.File.ReadAllText(path));

                var v2 = new CaseGraph();
                v2.AddWithId(new Tool { Name = "V2" }, "kb:t-replace");
                v2.WriteStreaming(path);
                var text = System.IO.File.ReadAllText(path);
                Assert.Contains("V2", text);
                Assert.DoesNotContain("V1", text);

                // netstandard2.0: File.Replace for existing destinations; File.Move
                // only when the destination is absent. Never Delete-then-Move.
            }
            finally
            {
                if (System.IO.File.Exists(path))
                    System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void WriteStreaming_InducedReplaceFailure_PreservesOldBytes()
        {
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-fail-replace-{Guid.NewGuid()}.jsonld");
            CaseGraph.SimulateReplaceFailureForTests = null;
            try
            {
                System.IO.File.WriteAllText(path, "SURVIVE-ME");
                CaseGraph.SimulateReplaceFailureForTests = (tmp, dest) =>
                    new System.IO.IOException("induced replace failure");

                var graph = new CaseGraph();
                graph.AddWithId(new Tool { Name = "ShouldNotLand" }, "kb:t-fail");
                var ex = Assert.Throws<System.IO.IOException>(() => graph.WriteStreaming(path));
                Assert.Contains("induced replace failure", ex.Message);
                Assert.Equal("SURVIVE-ME", System.IO.File.ReadAllText(path));
            }
            finally
            {
                CaseGraph.SimulateReplaceFailureForTests = null;
                if (System.IO.File.Exists(path))
                    System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void PartitionByRoots_IncludesIncomingRelationship()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:device", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "phone",
            });
            graph.UpsertNode("kb:file", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "photo",
            });
            var rel = graph.CreateRelationship("kb:file", "kb:device", "Contained_Within");
            var relId = (string)rel["@id"];

            var withIncoming = graph.PartitionByRoots(new[] { "kb:device" }, "replicate-identical", includeIncoming: true);
            Assert.True(withIncoming["kb:device"].Contains(relId));
            Assert.True(withIncoming["kb:device"].Contains("kb:file"));

            var outgoingOnly = graph.PartitionByRoots(new[] { "kb:device" }, "replicate-identical", includeIncoming: false);
            Assert.False(outgoingOnly["kb:device"].Contains(relId));
            Assert.False(outgoingOnly["kb:device"].Contains("kb:file"));
        }

        [Fact]
        public void PartitionByRoots_ReplicatesSharedNodes()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:shared", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "Shared",
            });
            graph.UpsertNode("kb:root-a", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });
            graph.UpsertNode("kb:root-b", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });

            var parts = graph.PartitionByRoots(new[] { "kb:root-a", "kb:root-b" });
            Assert.True(parts.TryGetValue("kb:root-a", out var partA));
            Assert.True(parts.TryGetValue("kb:root-b", out var partB));
            Assert.False(parts.ContainsKey("_shared"));
            Assert.True(partA.Contains("kb:shared"));
            Assert.True(partB.Contains("kb:shared"));
        }

        [Fact]
        public void PartitionByRoots_PlacesSharedNodesInSharedPartition()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:shared", "uco-core:UcoObject");
            graph.UpsertNode("kb:root-a", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });
            graph.UpsertNode("kb:root-b", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });

            var parts = graph.PartitionByRoots(new[] { "kb:root-a", "kb:root-b" }, "shared");
            Assert.True(parts.TryGetValue("_shared", out var sharedPart));
            Assert.True(sharedPart.Contains("kb:shared"));
        }

        [Fact]
        public void PartitionByRootsWithManifest_MarkingBoundaryFailsClosed()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:public-root", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:objectMarking"] = new Dictionary<string, object> { ["@id"] = "kb:public-marking" },
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:protected" },
            });
            graph.UpsertNode("kb:protected", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:objectMarking"] = new Dictionary<string, object> { ["@id"] = "kb:secret-marking" },
            });

            var error = Assert.Throws<PartitionBoundaryException>(() =>
                graph.PartitionByRootsWithManifest(new[] { "kb:public-root" }, new PartitionOptions
                {
                    IncludeIncoming = false,
                    BoundaryPolicy = "marking-and-authorization",
                }));

            Assert.Equal("kb:public-root", error.RootId);
            Assert.Equal("kb:protected", error.NodeId);
            Assert.Contains(graph.ExpandIri("kb:secret-marking"), error.MissingMarkings);
        }

        [Fact]
        public void PartitionByRootsWithManifest_HomeRoutePreservesUnion()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:public-root", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:objectMarking"] = new Dictionary<string, object> { ["@id"] = "kb:public-marking" },
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:protected" },
            });
            graph.UpsertNode("kb:secret-root", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:objectMarking"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = "kb:public-marking" },
                    new Dictionary<string, object> { ["@id"] = "kb:secret-marking" },
                },
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:protected" },
            });
            graph.UpsertNode("kb:protected", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:objectMarking"] = new Dictionary<string, object> { ["@id"] = "kb:secret-marking" },
                ["uco-core:name"] = "protected evidence",
            });

            var result = graph.PartitionByRootsWithManifest(
                new[] { "kb:public-root", "kb:secret-root" },
                new PartitionOptions
                {
                    IncludeIncoming = false,
                    BoundaryPolicy = "marking-and-authorization",
                    CrossBoundaryPolicy = "home-partition-reference",
                    RootBoundaries = new Dictionary<string, PartitionBoundary>
                    {
                        ["kb:public-root"] = new PartitionBoundary
                        {
                            Markings = new[] { "kb:public-marking" },
                        },
                        ["kb:secret-root"] = new PartitionBoundary
                        {
                            Markings = new[] { "kb:public-marking", "kb:secret-marking" },
                        },
                    },
                    ValidationBundle = new Dictionary<string, object>
                    {
                        ["extensions"] = new List<object> { "example:full" },
                    },
                });

            Assert.False(result.Partitions["kb:public-root"].Contains("kb:protected"));
            Assert.True(result.Partitions["kb:secret-root"].Contains("kb:protected"));
            Assert.Equal("referenced-partition-set", result.Manifest["validation_mode"]);
            var routes = Assert.IsType<Dictionary<string, string>>(result.Manifest["home_partition_routes"]);
            Assert.Equal("kb:secret-root", routes["kb:protected"]);
            Assert.True(graph.VerifyPartitionUnion(result.Partitions).Equivalent);
        }

        [Fact]
        public void PartitionByRootsWithManifest_SupportGraphSafeManifest()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:shared", "uco-core:UcoObject");
            foreach (var root in new[] { "kb:a", "kb:b" })
                graph.UpsertNode(root, "uco-core:UcoObject", new Dictionary<string, object>
                {
                    ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
                });

            var result = graph.PartitionByRootsWithManifest(
                new[] { "kb:a", "kb:b" },
                new PartitionOptions
                {
                    IncludeIncoming = false,
                    SharedNodePolicy = "support-graph",
                    ManifestDetail = "safe",
                });

            Assert.True(result.Partitions.ContainsKey("_support"));
            var manifests = Assert.IsType<Dictionary<string, object>>(result.Manifest["partitions"]);
            var a = Assert.IsType<Dictionary<string, object>>(manifests["kb:a"]);
            Assert.False(a.ContainsKey("node_ids"));
            Assert.True(graph.VerifyPartitionUnion(result.Partitions).Equivalent);
        }

        [Fact]
        public void PartitionByLabel_GroupsByBoundaryKey()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:art-a", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "A",
            });
            graph.UpsertNode("kb:art-b", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "B",
            });
            graph.CreateRelationship("kb:art-a", "kb:art-b", "Related_To");

            var parts = graph.PartitionByLabel(node =>
            {
                if (node.TryGetValue("uco-core:name", out var name) && name as string == "A")
                    return "part-a";
                if (name as string == "B")
                    return "part-b";
                return null;
            });

            Assert.True(parts.ContainsKey("part-a"));
            Assert.True(parts.ContainsKey("part-b"));
            Assert.Equal(
                parts.Keys.OrderBy(x => x).ToArray(),
                graph.PartitionByLabel(node =>
                {
                    if (node.TryGetValue("uco-core:name", out var name) && name as string == "A")
                        return "part-a";
                    if (name as string == "B")
                        return "part-b";
                    return null;
                }).Keys.OrderBy(x => x).ToArray());
        }
    
        private static JsonElement FirstNode(CaseGraph graph)
        {
            using var doc = JsonDocument.Parse(graph.Serialize());
            return doc.RootElement.GetProperty("@graph")[0].Clone();
        }

        [Fact]
        public void HashValue_SerializesAsUppercaseHexBinary()
        {
            var graph = new CaseGraph();
            var hash = new CaseUco.Uco.Types.Hash
            {
                HashMethod = "SHA256",
                HashValue = new byte[] { 0xde, 0xad, 0xbe, 0xef },
            };
            graph.AddWithId(hash, "kb:hash-1");

            var literal = FirstNode(graph).GetProperty("uco-types:hashValue");
            Assert.Equal("xsd:hexBinary", literal.GetProperty("@type").GetString());
            Assert.Equal("DEADBEEF", literal.GetProperty("@value").GetString());

            var back = (CaseUco.Uco.Types.Hash)CaseGraph.FromJsonLd(graph.Serialize()).Objects[0];
            Assert.Equal(hash.HashValue, back.HashValue);
        }

        [Fact]
        public void DateTime_SerializesCanonicalLexicalForms()
        {
            Assert.Equal("2024-01-02T03:04:05Z",
                CaseGraph.FormatDateTime(new DateTime(2024, 1, 2, 3, 4, 5, DateTimeKind.Utc)));
            Assert.Equal("2024-01-02T03:04:05.25Z",
                CaseGraph.FormatDateTime(new DateTime(2024, 1, 2, 3, 4, 5, 250, DateTimeKind.Utc)));
            Assert.Equal("2024-01-02T03:04:05",
                CaseGraph.FormatDateTime(new DateTime(2024, 1, 2, 3, 4, 5, DateTimeKind.Unspecified)));

            var local = new DateTime(2024, 1, 2, 3, 4, 5, DateTimeKind.Local);
            var offset = TimeZoneInfo.Local.GetUtcOffset(local);
            var sign = offset < TimeSpan.Zero ? "-" : "+";
            Assert.Equal("2024-01-02T03:04:05" + sign + offset.Duration().ToString(@"hh\:mm"), CaseGraph.FormatDateTime(local));
        }

        [Fact]
        public void DateTime_ParsesZoneSuffixAsUtc()
        {
            var json = "{\"@context\":{\"uco-action\":\"https://ontology.unifiedcyberontology.org/uco/action/\"}," +
                "\"@graph\":[{\"@id\":\"kb:a\",\"@type\":\"uco-action:Action\"," +
                "\"uco-action:startTime\":{\"@type\":\"xsd:dateTime\",\"@value\":\"2024-01-02T03:04:05Z[UTC]\"}}]}";
            var action = (CaseUco.Uco.Action.Action)CaseGraph.FromJsonLd(json).Objects[0];
            Assert.Equal(new DateTime(2024, 1, 2, 3, 4, 5, DateTimeKind.Utc), action.StartTime);
            Assert.Equal(DateTimeKind.Utc, action.StartTime?.Kind);
        }

        [Fact]
        public void NullableValueTypes_RoundTrip()
        {
            var graph = new CaseGraph();
            graph.AddWithId(new CaseUco.Uco.Observable.FileFacet { SizeInBytes = 4096 }, "kb:ff");
            var back = (CaseUco.Uco.Observable.FileFacet)CaseGraph.FromJsonLd(graph.Serialize()).Objects[0];
            Assert.Equal(4096L, back.SizeInBytes);
        }

        [Fact]
        public void StringEscapes_RoundTrip()
        {
            var json = "{\"@context\":{\"uco-core\":\"https://ontology.unifiedcyberontology.org/uco/core/\"," +
                "\"uco-tool\":\"https://ontology.unifiedcyberontology.org/uco/tool/\"}," +
                "\"@graph\":[{\"@id\":\"kb:t\",\"@type\":\"uco-tool:Tool\",\"uco-core:name\":\"caf\\u00e9 \\/ \\b\\f\"}]}";
            var tool = (Tool)CaseGraph.FromJsonLd(json).Objects[0];
            Assert.Equal("caf\u00e9 / \b\f", tool.Name);

            var graph = new CaseGraph();
            graph.AddWithId(new Tool { Name = "ctl\u0001\b\f\"\\" }, "kb:t2");
            var reparsed = (Tool)CaseGraph.FromJsonLd(graph.Serialize()).Objects[0];
            Assert.Equal("ctl\u0001\b\f\"\\", reparsed.Name);
            using var doc = JsonDocument.Parse(graph.Serialize());
            Assert.Equal("ctl\u0001\b\f\"\\", doc.RootElement.GetProperty("@graph")[0].GetProperty("uco-core:name").GetString());
        }

        [Fact]
        public void StringEscapes_InvalidEscapeIsRejected()
        {
            Assert.Throws<FormatException>(() =>
                CaseGraph.FromJsonLd("{\"@graph\":[{\"@id\":\"kb:t\",\"uco-core:name\":\"bad\\q\"}]}"));
        }

        private static bool CaseValidateOnPath()
        {
            try
            {
                var psi = new System.Diagnostics.ProcessStartInfo("case_validate", "--help")
                {
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                };
                using var process = System.Diagnostics.Process.Start(psi);
                process.StandardOutput.ReadToEnd();
                process.WaitForExit();
                return process.ExitCode == 0;
            }
            catch (System.ComponentModel.Win32Exception)
            {
                return false;
            }
        }

        [Fact]
        public void Serialize_KeepsXsdPrefixForTypedLiterals()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:a", "uco-identity:Person");
            graph.UpsertNode("kb:b", "uco-identity:Organization");
            graph.CreateRelationship("kb:a", "kb:b", "Employed_By");

            using var doc = JsonDocument.Parse(graph.Serialize());
            Assert.Equal(
                "http://www.w3.org/2001/XMLSchema#",
                doc.RootElement.GetProperty("@context").GetProperty("xsd").GetString());
        }

        // #111: CreateRelationship mints a non-UUID IRI that UCO reports at sh:Info.
        [Fact]
        public void ValidateGraph_AcceptsInfoFromRelationshipIds()
        {
            if (!CaseValidateOnPath())
                return;
            var graph = new CaseGraph();
            var a = "kb:person-7f9c2a3e-1b4d-4c6e-9a8f-0d1e2f3a4b5c";
            var b = "kb:org-2c4e6a8b-3d5f-4a7c-8e9f-1a2b3c4d5e6f";
            graph.UpsertNode(a, "uco-identity:Person", new Dictionary<string, object> { ["uco-core:name"] = "A" });
            graph.UpsertNode(b, "uco-identity:Organization", new Dictionary<string, object> { ["uco-core:name"] = "B" });
            graph.CreateRelationship(a, b, "Employed_By");

            Assert.Contains("sh:Info", graph.ValidateGraph());
            Assert.Throws<InvalidOperationException>(() => graph.ValidateGraph(allowInfo: false));
        }
    }
}

