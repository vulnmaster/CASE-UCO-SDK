// Tests for CaseGraph builder and JSON-LD serialization.
package org.caseontology;

import org.caseontology.uco.tool.Tool;
import org.caseontology.uco.observable.ObservableObject;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Map;
import java.util.List;

public class CaseGraphTest {

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
    public void testContextHasAllPrefixes() {
        CaseGraph graph = new CaseGraph();
        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");

        String[] expected = {
            "uco-core", "uco-tool", "uco-observable", "uco-action",
            "uco-identity", "uco-location", "uco-types", "uco-vocabulary",
            "uco-role", "uco-victim", "uco-analysis", "uco-configuration",
            "uco-marking", "uco-pattern", "uco-time", "xsd",
            "case-investigation",
        };
        for (String prefix : expected) {
            assertTrue("missing context prefix: " + prefix, context.containsKey(prefix));
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testCustomKbPrefix() {
        CaseGraph graph = new CaseGraph("http://mylab.example.org/case/");
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
}
