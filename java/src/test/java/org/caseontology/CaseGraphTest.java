// Tests for CaseGraph builder and JSON-LD serialization.
package org.caseontology;

import org.caseontology.uco.tool.Tool;
import org.caseontology.uco.observable.ObservableObject;
import org.junit.Test;
import static org.junit.Assert.*;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.util.List;
import java.util.LinkedHashMap;
import java.util.Collection;

public class CaseGraphTest {
    public static final class DynamicExtension {
        public static final String CLASS_IRI = "https://example.org/dynamic/DynamicExtension";
        public static final String NAMESPACE_PREFIX = "dyn";
        private String value;
        public DynamicExtension() {}
        public String getValue() { return value; }
        public void setValue(String value) { this.value = value; }
    }

    public static final class ConflictingToolExtension {
        public static final String CLASS_IRI = Tool.CLASS_IRI;
        public ConflictingToolExtension() {}
    }

    @Test
    public void testCreateTool() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Tool A");
        tool.setVersion("7.0");
        tool.setToolType("forensic");

        String id = graph.add(tool);
        assertTrue(id.startsWith("kb:Tool-"));
        Map<String, Object> doc = graph.toMap();
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> graphList = (List<Map<String, Object>>) doc.get("@graph");
        assertTrue(graphList.get(0).containsKey("uco-core:name"));
        assertFalse(graphList.get(0).containsKey("uco-tool:name"));
    }

    @Test
    public void testGetId() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        String id = graph.add(tool);
        assertEquals(id, graph.getId(tool));
    }

    @Test
    public void testAddWithDeterministicId() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Tool A");

        String id = graph.addWithId(tool, "kb:Tool-my-stable-id");
        assertEquals("kb:Tool-my-stable-id", id);
        assertEquals("kb:Tool-my-stable-id", graph.getId(tool));

        String json = graph.serialize();
        assertTrue(json.contains("kb:Tool-my-stable-id"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testMultipleObjects() {
        CaseGraph graph = new CaseGraph();
        graph.add(new Tool());
        graph.add(new Tool());

        Map<String, Object> doc = graph.toMap();
        List<Map<String, Object>> graphList = (List<Map<String, Object>>) doc.get("@graph");
        assertEquals(2, graphList.size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testContextPrunesUnusedPrefixes() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Tool A");
        graph.add(tool);

        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");

        assertTrue("used prefix kb should be present", context.containsKey("kb"));
        assertTrue("used prefix uco-tool should be present", context.containsKey("uco-tool"));
        assertTrue("used prefix uco-core should be present", context.containsKey("uco-core"));

        String[] unused = {
            "uco-identity", "uco-location", "uco-role", "uco-victim",
            "uco-configuration", "uco-marking", "uco-pattern", "uco-time",
        };
        for (String prefix : unused) {
            assertFalse("unused prefix should be pruned: " + prefix, context.containsKey(prefix));
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testEmptyGraphHasEmptyContext() {
        CaseGraph graph = new CaseGraph();
        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");
        assertTrue("empty graph should have empty context", context.isEmpty());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testCustomKbPrefix() {
        CaseGraph graph = new CaseGraph("http://mylab.example.org/case/");
        Tool tool = new Tool();
        graph.add(tool);
        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");
        assertEquals("http://mylab.example.org/case/", context.get("kb"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testBooleanTypedLiteral() {
        CaseGraph graph = new CaseGraph();
        ObservableObject observable = new ObservableObject();
        observable.setHasChanged(Boolean.TRUE);
        graph.add(observable);

        Map<String, Object> doc = graph.toMap();
        List<Map<String, Object>> graphList = (List<Map<String, Object>>) doc.get("@graph");
        Map<String, Object> observableJson = graphList.get(0);
        Map<String, String> typedLiteral = (Map<String, String>) observableJson.get("uco-observable:hasChanged");
        assertEquals("xsd:boolean", typedLiteral.get("@type"));
        assertEquals("true", typedLiteral.get("@value"));
    }

    @Test
    public void testSize() {
        CaseGraph graph = new CaseGraph();
        assertEquals(0, graph.size());
        graph.add(new Tool());
        assertEquals(1, graph.size());
        graph.add(new Tool());
        assertEquals(2, graph.size());
    }

    @Test
    public void testSerializeProducesJsonString() {
        CaseGraph graph = new CaseGraph();
        graph.add(new Tool());
        String json = graph.serialize();
        assertTrue(json.contains("@context"));
        assertTrue(json.contains("@graph"));
    }

    @Test
    public void testLoadMergesContextAndObjects() {
        CaseGraph graph = new CaseGraph();
        String inputJson = "{\n" +
            "  \"@context\": {\n" +
            "    \"kb\": \"http://example.org/kb/\",\n" +
            "    \"uco-tool\": \"https://ontology.unifiedcyberontology.org/uco/tool/\"\n" +
            "  },\n" +
            "  \"@graph\": [\n" +
            "    {\n" +
            "      \"@id\": \"kb:Tool-existing-001\",\n" +
            "      \"@type\": \"uco-tool:Tool\"\n" +
            "    }\n" +
            "  ]\n" +
            "}";

        graph.load(inputJson);
        assertEquals(1, graph.size());

        String json = graph.serialize();
        assertTrue(json.contains("kb:Tool-existing-001"));
    }

    @Test
    public void testLoadThenAddCombinesObjects() {
        CaseGraph graph = new CaseGraph();
        graph.load("{\"@context\":{\"kb\":\"http://example.org/kb/\"},\"@graph\":[{\"@id\":\"kb:Tool-loaded\",\"@type\":\"uco-tool:Tool\"}]}");
        graph.add(new Tool());
        assertEquals(2, graph.size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testGetReturnsDeepCopy() {
        CaseGraph graph = new CaseGraph();
        Map<String, Object> props = new LinkedHashMap<>();
        props.put("uco-core:name", "N");
        props.put("uco-core:tag", new ArrayList<>(List.of("a", "b")));
        Map<String, Object> facet = new LinkedHashMap<>();
        facet.put("@id", "kb:f1");
        props.put("uco-core:hasFacet", new ArrayList<>(List.of(facet)));
        graph.upsertNode("kb:n1", "uco-core:UcoObject", props);
        Map<String, Object> view = graph.get("kb:n1");
        view.put("@id", "kb:mutated");
        ((List<Object>) view.get("uco-core:tag")).add("c");
        ((Map<String, Object>) ((List<Object>) view.get("uco-core:hasFacet")).get(0)).put("@id", "kb:mutated-facet");
        assertTrue(graph.contains("kb:n1"));
        assertFalse(graph.contains("kb:mutated"));
        assertEquals("N", graph.get("kb:n1").get("uco-core:name"));
        assertEquals(2, ((List<?>) graph.get("kb:n1").get("uco-core:tag")).size());
        assertEquals("kb:f1", ((Map<?, ?>) ((List<?>) graph.get("kb:n1").get("uco-core:hasFacet")).get(0)).get("@id"));
    }

    @Test
    public void testSplitRejectsNonPositive() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:x", "uco-core:UcoObject", null);
        try {
            graph.split(0);
            fail("expected IllegalArgumentException");
        } catch (IllegalArgumentException expected) {
            assertTrue(expected.getMessage().contains("positive"));
        }
    }

    @Test
    public void testLoadRejectsDuplicateByDefault() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:x", "uco-core:UcoObject", null);
        try {
            graph.load("{\"@context\":{\"kb\":\"http://example.org/kb/\"},\"@graph\":[{\"@id\":\"kb:x\",\"@type\":\"uco-core:UcoObject\"}]}");
            fail("expected IllegalStateException");
        } catch (IllegalStateException expected) {
            assertTrue(expected.getMessage().contains("Duplicate"));
        }
    }

    @Test
    public void testLoadRejectsContextCollision() {
        CaseGraph graph = new CaseGraph();
        try {
            graph.load("{\"@context\":{\"kb\":\"http://example.org/kb/\",\"uco-core\":\"https://evil.example.org/uco/core/\"},\"@graph\":[]}");
            fail("expected IllegalArgumentException");
        } catch (IllegalArgumentException expected) {
            assertTrue(expected.getMessage().contains("Context prefix collision"));
        }
    }

    @Test
    public void testClearClassRegistryCacheAndFromJsonLd() {
        CaseGraph.clearClassRegistryCache();
        String json = "{\n" +
            "  \"@context\": {\n" +
            "    \"kb\": \"http://example.org/kb/\",\n" +
            "    \"uco-tool\": \"https://ontology.unifiedcyberontology.org/uco/tool/\",\n" +
            "    \"uco-core\": \"https://ontology.unifiedcyberontology.org/uco/core/\"\n" +
            "  },\n" +
            "  \"@graph\": [\n" +
            "    {\n" +
            "      \"@id\": \"kb:Tool-stream-1\",\n" +
            "      \"@type\": \"uco-tool:Tool\",\n" +
            "      \"uco-core:name\": \"Registry Tool\"\n" +
            "    }\n" +
            "  ]\n" +
            "}";
        CaseGraph.FromJsonLdResult first = CaseGraph.fromJsonLd(json);
        assertEquals(1, first.getObjects().size());
        assertTrue(first.getObjects().get(0) instanceof Tool);

        CaseGraph.clearClassRegistryCache();
        CaseGraph.FromJsonLdResult second = CaseGraph.fromJsonLd(json);
        assertEquals(1, second.getObjects().size());
        assertTrue(second.getObjects().get(0) instanceof Tool);
    }

    @Test
    public void testWriteStreamingRoundtrip() throws Exception {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Streamed");
        graph.addWithId(tool, "kb:Tool-stream");

        java.nio.file.Path out = Files.createTempFile("case-graph-stream", ".jsonld");
        try {
            CaseGraph.StreamingWriteResult metrics = graph.writeStreaming(out.toString());
            assertEquals(1, metrics.getNodes());
            assertTrue(metrics.getBytesWritten() > 0);
            CaseGraph loaded = new CaseGraph();
            loaded.load(Files.readString(out), "merge_compatible");
            assertEquals("Streamed", loaded.get("kb:Tool-stream").get("uco-core:name"));
        } finally {
            Files.deleteIfExists(out);
        }
    }

    @Test
    public void testBoundedStreamWriterFrozenContextAndNodeCap() throws Exception {
        java.nio.file.Path out = Files.createTempFile("case-graph-bounded", ".jsonld");
        try {
            Map<String, String> context = Map.of(
                "kb", "https://example.org/kb/",
                "uco-core", "https://ontology.unifiedcyberontology.org/uco/core/");
            JsonLdStreamWriter.BoundedStreamingWriteResult metrics;
            try (JsonLdStreamWriter writer = new JsonLdStreamWriter(
                    out, context, 1024, true, true)) {
                for (int i = 0; i < 100; i++) {
                    Map<String, Object> node = new LinkedHashMap<>();
                    node.put("@id", "kb:node-" + i);
                    node.put("@type", "uco-core:UcoObject");
                    node.put("uco-core:name", "Node " + i);
                    writer.writeNode(node);
                }
                metrics = writer.metrics();
            }
            String json = Files.readString(out);
            CaseGraph graph = new CaseGraph("https://example.org/kb/");
            graph.load(json, "merge_compatible");
            assertEquals(100, graph.size());
            assertEquals(100, metrics.getNodes());
            assertTrue(metrics.getMaxNodeBytesWritten() <= 1024);
        } finally {
            Files.deleteIfExists(out);
        }
    }

    @Test
    public void testBoundedStreamWriterFailurePreservesDestination() throws Exception {
        java.nio.file.Path out = Files.createTempFile("case-graph-bounded-fail", ".jsonld");
        Files.writeString(out, "SURVIVE");
        Map<String, String> context = Map.of(
            "kb", "https://example.org/kb/",
            "uco-core", "https://ontology.unifiedcyberontology.org/uco/core/");
        try {
            try (JsonLdStreamWriter writer = new JsonLdStreamWriter(
                    out, context, 128, true, true)) {
                writer.writeNode(Map.of("@id", "kb:bad", "@type", "evil:Fabricated"));
                fail("unknown prefix must fail");
            } catch (IllegalArgumentException expected) {
                assertTrue(expected.getMessage().contains("undeclared JSON-LD prefix"));
            }
            assertEquals("SURVIVE", Files.readString(out));

            try (JsonLdStreamWriter writer = new JsonLdStreamWriter(
                    out, context, 128, true, true)) {
                writer.writeNode(Map.of(
                    "@id", "kb:large",
                    "@type", "uco-core:UcoObject",
                    "uco-core:name", "x".repeat(1000)));
                fail("oversized node must fail");
            } catch (IllegalArgumentException expected) {
                assertTrue(expected.getMessage().contains("maxNodeBytes"));
            }
            assertEquals("SURVIVE", Files.readString(out));
        } finally {
            Files.deleteIfExists(out);
        }
    }

    @Test
    public void testFieldBindingCacheWarmPath() {
        CaseGraph.clearClassRegistryCache();
        assertEquals(0, CaseGraph.fieldBindingCacheCount());
        String json = "{\n" +
            "  \"@context\": {\n" +
            "    \"kb\": \"http://example.org/kb/\",\n" +
            "    \"uco-tool\": \"https://ontology.unifiedcyberontology.org/uco/tool/\",\n" +
            "    \"uco-core\": \"https://ontology.unifiedcyberontology.org/uco/core/\"\n" +
            "  },\n" +
            "  \"@graph\": [\n" +
            "    {\n" +
            "      \"@id\": \"kb:Tool-warm\",\n" +
            "      \"@type\": \"uco-tool:Tool\",\n" +
            "      \"uco-core:name\": \"Warm\"\n" +
            "    }\n" +
            "  ]\n" +
            "}";
        CaseGraph.fromJsonLd(json);
        int afterCold = CaseGraph.fieldBindingCacheCount();
        assertTrue(afterCold > 0);
        CaseGraph.fromJsonLd(json);
        assertEquals(afterCold, CaseGraph.fieldBindingCacheCount());
        CaseGraph.clearClassRegistryCache();
        assertEquals(0, CaseGraph.fieldBindingCacheCount());
    }

    @Test
    public void testDynamicClassRegistryProviderInvalidationAndMetrics() {
        final String source = "java-test-dynamic-extension";
        CaseGraph.unregisterClassRegistryProvider(source);
        CaseGraph.clearClassRegistryCache();
        CaseGraph.ClassRegistryCacheMetrics before = CaseGraph.classRegistryCacheMetrics();
        ClassRegistryProvider provider = new ClassRegistryProvider() {
            public String source() { return source; }
            public Collection<Class<?>> classes() {
                return Arrays.asList(DynamicExtension.class);
            }
        };
        long generation = CaseGraph.registerClassRegistryProvider(provider);
        assertTrue(generation > before.getGeneration());

        String json = "{\"@context\":{" +
            "\"kb\":\"http://example.org/kb/\"," +
            "\"dyn\":\"https://example.org/dynamic/\"}," +
            "\"@graph\":[{\"@id\":\"kb:dynamic\"," +
            "\"@type\":\"dyn:DynamicExtension\"," +
            "\"dyn:value\":\"loaded without restart\"}]}";
        CaseGraph.FromJsonLdResult first = CaseGraph.fromJsonLd(json);
        CaseGraph.FromJsonLdResult second = CaseGraph.fromJsonLd(json);
        assertTrue(first.getObjects().get(0) instanceof DynamicExtension);
        assertTrue(second.getObjects().get(0) instanceof DynamicExtension);
        CaseGraph.ClassRegistryCacheMetrics info = CaseGraph.classRegistryCacheMetrics();
        assertTrue(info.getHits() > before.getHits());
        assertTrue(info.getRegisteredProviders() >= 1);

        CaseGraph.unregisterClassRegistryProvider(source);
        CaseGraph.FromJsonLdResult raw = CaseGraph.fromJsonLd(json);
        assertTrue(raw.getObjects().get(0) instanceof Map);
    }

    @Test
    public void testDynamicClassRegistryProviderRejectsBuiltinConflict() {
        final String source = "java-test-conflict";
        ClassRegistryProvider provider = new ClassRegistryProvider() {
            public String source() { return source; }
            public Collection<Class<?>> classes() {
                return Arrays.asList(ConflictingToolExtension.class);
            }
        };
        try {
            CaseGraph.registerClassRegistryProvider(provider);
            fail("expected ClassRegistryConflictException");
        } catch (ClassRegistryConflictException expected) {
            assertEquals(Tool.CLASS_IRI, expected.getClassIri());
        } finally {
            CaseGraph.unregisterClassRegistryProvider(source);
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testPartitionByRootsIncludeIncoming() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:device", "uco-core:UcoObject", Map.of("uco-core:name", "phone"));
        graph.upsertNode("kb:file", "uco-core:UcoObject", Map.of("uco-core:name", "photo"));
        Map<String, Object> rel = graph.createRelationship("kb:file", "kb:device", "Contained_Within");
        String relId = (String) rel.get("@id");

        Map<String, CaseGraph> withIncoming = graph.partitionByRoots(
            Arrays.asList("kb:device"), "replicate-identical", true);
        assertTrue(withIncoming.get("kb:device").contains(relId));
        assertTrue(withIncoming.get("kb:device").contains("kb:file"));

        Map<String, CaseGraph> outgoingOnly = graph.partitionByRoots(
            Arrays.asList("kb:device"), "replicate-identical", false);
        assertFalse(outgoingOnly.get("kb:device").contains(relId));
        assertFalse(outgoingOnly.get("kb:device").contains("kb:file"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testPartitionByRootsDependencyClosure() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:root-a", "uco-core:UcoObject", Map.of("uco-core:name", "A"));
        graph.upsertNode("kb:child-a", "uco-core:UcoObject", Map.of("uco-core:name", "ChildA"));
        graph.link("kb:root-a", "uco-core:hasFacet", "kb:child-a");

        Map<String, CaseGraph> parts = graph.partitionByRoots(Arrays.asList("kb:root-a"));
        assertEquals(1, parts.size());
        CaseGraph partA = parts.get("kb:root-a");
        assertNotNull(partA);
        assertTrue(partA.contains("kb:root-a"));
        assertTrue(partA.contains("kb:child-a"));
        assertEquals(2, partA.size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testPartitionByRootsReplicateShared() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:root-a", "uco-core:UcoObject", Map.of("uco-core:name", "A"));
        graph.upsertNode("kb:root-b", "uco-core:UcoObject", Map.of("uco-core:name", "B"));
        graph.upsertNode("kb:shared", "uco-core:UcoObject", Map.of("uco-core:name", "Shared"));
        graph.link("kb:root-a", "uco-core:hasFacet", "kb:shared");
        graph.link("kb:root-b", "uco-core:hasFacet", "kb:shared");

        Map<String, CaseGraph> parts = graph.partitionByRoots(
            Arrays.asList("kb:root-a", "kb:root-b"), "replicate-identical");

        assertTrue(parts.get("kb:root-a").contains("kb:shared"));
        assertTrue(parts.get("kb:root-b").contains("kb:shared"));
        assertEquals("Shared", parts.get("kb:root-a").get("kb:shared").get("uco-core:name"));
        assertEquals("Shared", parts.get("kb:root-b").get("kb:shared").get("uco-core:name"));
    }

    @Test
    public void testPartitionByRootsIsolateShared() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:root-a", "uco-core:UcoObject", Map.of("uco-core:name", "A"));
        graph.upsertNode("kb:root-b", "uco-core:UcoObject", Map.of("uco-core:name", "B"));
        graph.upsertNode("kb:shared", "uco-core:UcoObject", Map.of("uco-core:name", "Shared"));
        graph.link("kb:root-a", "uco-core:hasFacet", "kb:shared");
        graph.link("kb:root-b", "uco-core:hasFacet", "kb:shared");

        Map<String, CaseGraph> parts = graph.partitionByRoots(
            Arrays.asList("kb:root-a", "kb:root-b"), "isolate-shared");

        assertTrue(parts.containsKey("_shared"));
        assertTrue(parts.get("_shared").contains("kb:shared"));
        assertFalse(parts.get("kb:root-a").contains("kb:shared"));
        assertFalse(parts.get("kb:root-b").contains("kb:shared"));
    }

    @Test
    public void testPartitionMarkingBoundaryFailsClosed() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:public-root", "uco-core:UcoObject", Map.of(
            "uco-core:objectMarking", Map.of("@id", "kb:public-marking"),
            "uco-core:object", Map.of("@id", "kb:protected")));
        graph.upsertNode("kb:protected", "uco-core:UcoObject", Map.of(
            "uco-core:objectMarking", Map.of("@id", "kb:secret-marking")));

        try {
            graph.partitionByRootsWithManifest(
                Arrays.asList("kb:public-root"),
                new PartitionOptions()
                    .setIncludeIncoming(false)
                    .setBoundaryPolicy("marking-and-authorization"));
            fail("expected PartitionBoundaryException");
        } catch (PartitionBoundaryException expected) {
            assertEquals("kb:public-root", expected.getRootId());
            assertEquals("kb:protected", expected.getNodeId());
            assertTrue(expected.getMissingMarkings().contains(graph.expandIri("kb:secret-marking")));
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testPartitionHomeRoutePreservesUnion() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:public-root", "uco-core:UcoObject", Map.of(
            "uco-core:objectMarking", Map.of("@id", "kb:public-marking"),
            "uco-core:object", Map.of("@id", "kb:protected")));
        graph.upsertNode("kb:secret-root", "uco-core:UcoObject", Map.of(
            "uco-core:objectMarking", Arrays.asList(
                Map.of("@id", "kb:public-marking"),
                Map.of("@id", "kb:secret-marking")),
            "uco-core:object", Map.of("@id", "kb:protected")));
        graph.upsertNode("kb:protected", "uco-core:UcoObject", Map.of(
            "uco-core:objectMarking", Map.of("@id", "kb:secret-marking"),
            "uco-core:name", "protected evidence"));

        Map<String, PartitionBoundary> boundaries = new LinkedHashMap<>();
        boundaries.put("kb:public-root", new PartitionBoundary(
            Arrays.asList("kb:public-marking"), null));
        boundaries.put("kb:secret-root", new PartitionBoundary(
            Arrays.asList("kb:public-marking", "kb:secret-marking"), null));
        PartitionResult result = graph.partitionByRootsWithManifest(
            Arrays.asList("kb:public-root", "kb:secret-root"),
            new PartitionOptions()
                .setIncludeIncoming(false)
                .setBoundaryPolicy("marking-and-authorization")
                .setCrossBoundaryPolicy("home-partition-reference")
                .setRootBoundaries(boundaries)
                .setValidationBundle(Map.of("extensions", Arrays.asList("example:full"))));

        assertFalse(result.getPartitions().get("kb:public-root").contains("kb:protected"));
        assertTrue(result.getPartitions().get("kb:secret-root").contains("kb:protected"));
        assertEquals("referenced-partition-set", result.getManifest().get("validation_mode"));
        Map<String, String> routes = (Map<String, String>) result.getManifest().get("home_partition_routes");
        assertEquals("kb:secret-root", routes.get("kb:protected"));
        assertTrue(graph.verifyPartitionUnion(result.getPartitions()).isEquivalent());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testPartitionSupportGraphSafeManifest() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:shared", "uco-core:UcoObject", null);
        for (String root : Arrays.asList("kb:a", "kb:b")) {
            graph.upsertNode(root, "uco-core:UcoObject", Map.of(
                "uco-core:object", Map.of("@id", "kb:shared")));
        }

        PartitionResult result = graph.partitionByRootsWithManifest(
            Arrays.asList("kb:a", "kb:b"),
            new PartitionOptions()
                .setIncludeIncoming(false)
                .setSharedNodePolicy("support-graph")
                .setManifestDetail("safe"));

        assertTrue(result.getPartitions().containsKey("_support"));
        Map<String, Object> partitionMetadata =
            (Map<String, Object>) result.getManifest().get("partitions");
        Map<String, Object> a = (Map<String, Object>) partitionMetadata.get("kb:a");
        assertFalse(a.containsKey("node_ids"));
        assertTrue(graph.verifyPartitionUnion(result.getPartitions()).isEquivalent());
    }
}
