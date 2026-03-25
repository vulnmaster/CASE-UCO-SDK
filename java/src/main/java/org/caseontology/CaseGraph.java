// CaseGraph — main entry point for building and serializing CASE/UCO graphs in Java.
package org.caseontology;

import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Build a CASE/UCO JSON-LD graph with typed objects.
 */
public class CaseGraph {

    private final Map<String, String> context;
    private final List<Map<String, Object>> objects;
    private final Map<Object, String> idMap;

    public CaseGraph() {
        this("http://example.org/kb/");
    }

    public CaseGraph(String kbPrefix) {
        this.context = new LinkedHashMap<>(defaultContext());
        this.context.put("kb", kbPrefix);
        this.objects = new ArrayList<>();
        this.idMap = new IdentityHashMap<>();
    }

    public void addContext(String prefix, String iri) {
        context.put(prefix, iri);
    }

    /**
     * Add an object to the graph with an auto-generated UUID @id.
     */
    public String add(Object instance) {
        String id = mintId(instance);
        return addWithId(instance, id);
    }

    /**
     * Add an object to the graph with a user-supplied @id for deterministic IRIs.
     */
    public String addWithId(Object instance, String id) {
        validate(instance);
        idMap.put(instance, id);
        Map<String, Object> jsonObj = toJsonLd(instance, id);
        objects.add(jsonObj);
        return id;
    }

    private void validate(Object instance) {
        if (instance == null) return;
        for (Field field : getAllFields(instance.getClass())) {
            if (!field.isAnnotationPresent(CaseRequired.class)) continue;
            field.setAccessible(true);
            try {
                Object value = field.get(instance);
                if (value == null) {
                    throw new IllegalArgumentException(
                        instance.getClass().getSimpleName() + "." + field.getName() +
                        " is required but was not provided.");
                }
                if (value instanceof List && ((List<?>) value).isEmpty()) {
                    throw new IllegalArgumentException(
                        instance.getClass().getSimpleName() + "." + field.getName() +
                        " requires at least one value.");
                }
            } catch (IllegalAccessException ignored) {}
        }
    }

    /**
     * Get the @id assigned to a previously-added instance.
     */
    public String getId(Object instance) {
        return idMap.get(instance);
    }

    /**
     * Return the number of objects in the graph.
     */
    public int size() {
        return objects.size();
    }

    /**
     * Serialize the graph to a JSON-LD-compatible map.
     */
    public Map<String, Object> toMap() {
        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("@context", context);
        doc.put("@graph", objects);
        return doc;
    }

    /**
     * Serialize the graph to a JSON-LD string.
     */
    public String serialize() {
        return toJsonString(toMap(), 0);
    }

    /**
     * Write the graph as JSON-LD to a file.
     */
    public void write(String path) throws IOException {
        try (Writer writer = new FileWriter(path)) {
            writer.write(serialize());
        }
    }

    /**
     * Load a JSON-LD string into this graph, merging context and appending objects.
     */
    @SuppressWarnings("unchecked")
    public void load(String json) {
        Map<String, Object> doc = (Map<String, Object>) parseJsonValue(json.trim(), new int[]{0});
        if (doc.containsKey("@context") && doc.get("@context") instanceof Map) {
            Map<String, Object> ctx = (Map<String, Object>) doc.get("@context");
            for (Map.Entry<String, Object> entry : ctx.entrySet()) {
                if (entry.getValue() instanceof String) {
                    context.put(entry.getKey(), (String) entry.getValue());
                }
            }
        }
        if (doc.containsKey("@graph") && doc.get("@graph") instanceof List) {
            List<Object> graphList = (List<Object>) doc.get("@graph");
            for (Object item : graphList) {
                if (item instanceof Map) {
                    objects.add((Map<String, Object>) item);
                }
            }
        }
    }

    /**
     * Read and load a JSON-LD file into this graph.
     */
    public void loadFile(String path) throws IOException {
        String json = new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(path)));
        load(json);
    }

    private String mintId(Object instance) {
        String typeName = instance.getClass().getSimpleName();
        return "kb:" + typeName + "-" + UUID.randomUUID();
    }

    private Map<String, Object> toJsonLd(Object instance, String id) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("@id", id);

        Class<?> cls = instance.getClass();
        try {
            Field classIriField = cls.getDeclaredField("CLASS_IRI");
            String iri = (String) classIriField.get(null);
            result.put("@type", compactIri(iri));
        } catch (NoSuchFieldException | IllegalAccessException ignored) {}

        for (Field field : getAllFields(cls)) {
            if (field.getName().equals("CLASS_IRI") || field.getName().equals("NAMESPACE_PREFIX")) {
                continue;
            }
            if (Modifier.isStatic(field.getModifiers())) {
                continue;
            }

            field.setAccessible(true);
            try {
                Object value = field.get(instance);
                if (value == null) continue;
                if (value instanceof List && ((List<?>) value).isEmpty()) continue;

                String nsPrefix = "uco-core";
                try {
                    Field nsPrefixField = field.getDeclaringClass().getDeclaredField("NAMESPACE_PREFIX");
                    nsPrefix = (String) nsPrefixField.get(null);
                } catch (NoSuchFieldException | IllegalAccessException ignored) {}

                String propKey = nsPrefix + ":" + field.getName();
                result.put(propKey, convertValue(value));
            } catch (IllegalAccessException ignored) {}
        }

        return result;
    }

    private List<Field> getAllFields(Class<?> type) {
        List<Field> fields = new ArrayList<>();
        Class<?> current = type;
        while (current != null && current != Object.class) {
            for (Field field : current.getDeclaredFields()) {
                fields.add(field);
            }
            current = current.getSuperclass();
        }
        return fields;
    }

    @SuppressWarnings("unchecked")
    private Object convertValue(Object value) {
        if (value == null) {
            return null;
        }
        if (value instanceof String) {
            return value;
        }
        if (value instanceof Boolean) {
            return typedLiteral("xsd:boolean", ((Boolean) value) ? "true" : "false");
        }
        if (value instanceof Byte || value instanceof Short || value instanceof Integer || value instanceof Long) {
            return typedLiteral("xsd:integer", value.toString());
        }
        if (value instanceof Float || value instanceof Double) {
            return typedLiteral("xsd:decimal", value.toString());
        }
        if (value instanceof ZonedDateTime) {
            return typedLiteral("xsd:dateTime", value.toString());
        }
        if (value instanceof List<?>) {
            List<Object> converted = new ArrayList<>();
            for (Object item : (List<Object>) value) {
                converted.add(convertValue(item));
            }
            return converted;
        }
        if (idMap.containsKey(value)) {
            Map<String, Object> ref = new LinkedHashMap<>();
            ref.put("@id", idMap.get(value));
            return ref;
        }
        try {
            value.getClass().getDeclaredField("CLASS_IRI");
            return toJsonLd(value, mintId(value));
        } catch (NoSuchFieldException ignored) {}
        return value;
    }

    private Map<String, String> typedLiteral(String xsdType, String value) {
        Map<String, String> literal = new LinkedHashMap<>();
        literal.put("@type", xsdType);
        literal.put("@value", value);
        return literal;
    }

    private String compactIri(String iri) {
        for (Map.Entry<String, String> entry : context.entrySet()) {
            if (iri.startsWith(entry.getValue())) {
                return entry.getKey() + ":" + iri.substring(entry.getValue().length());
            }
        }
        return iri;
    }

    private static String escapeJson(String s) {
        StringBuilder sb = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': sb.append("\\\\"); break;
                case '"':  sb.append("\\\""); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                default:
                    if (c < 0x20) {
                        sb.append(String.format("\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        return sb.toString();
    }

    private static Map<String, String> defaultContext() {
        Map<String, String> ctx = new LinkedHashMap<>();
        ctx.put("case-investigation", "https://ontology.caseontology.org/case/investigation/");
        ctx.put("kb", "http://example.org/kb/");
        ctx.put("uco-action", "https://ontology.unifiedcyberontology.org/uco/action/");
        ctx.put("uco-analysis", "https://ontology.unifiedcyberontology.org/uco/analysis/");
        ctx.put("uco-configuration", "https://ontology.unifiedcyberontology.org/uco/configuration/");
        ctx.put("uco-core", "https://ontology.unifiedcyberontology.org/uco/core/");
        ctx.put("uco-identity", "https://ontology.unifiedcyberontology.org/uco/identity/");
        ctx.put("uco-location", "https://ontology.unifiedcyberontology.org/uco/location/");
        ctx.put("uco-marking", "https://ontology.unifiedcyberontology.org/uco/marking/");
        ctx.put("uco-observable", "https://ontology.unifiedcyberontology.org/uco/observable/");
        ctx.put("uco-pattern", "https://ontology.unifiedcyberontology.org/uco/pattern/");
        ctx.put("uco-role", "https://ontology.unifiedcyberontology.org/uco/role/");
        ctx.put("uco-time", "https://ontology.unifiedcyberontology.org/uco/time/");
        ctx.put("uco-tool", "https://ontology.unifiedcyberontology.org/uco/tool/");
        ctx.put("uco-types", "https://ontology.unifiedcyberontology.org/uco/types/");
        ctx.put("uco-victim", "https://ontology.unifiedcyberontology.org/uco/victim/");
        ctx.put("uco-vocabulary", "https://ontology.unifiedcyberontology.org/uco/vocabulary/");
        ctx.put("xsd", "http://www.w3.org/2001/XMLSchema#");
        return ctx;
    }

    @SuppressWarnings("unchecked")
    private String toJsonString(Object obj, int indent) {
        String pad = "    ".repeat(indent);
        String pad1 = "    ".repeat(indent + 1);

        if (obj instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) obj;
            if (map.isEmpty()) return "{}";
            StringBuilder sb = new StringBuilder("{\n");
            Iterator<Map.Entry<String, Object>> it = map.entrySet().iterator();
            while (it.hasNext()) {
                Map.Entry<String, Object> e = it.next();
                sb.append(pad1).append("\"").append(e.getKey()).append("\": ");
                sb.append(toJsonString(e.getValue(), indent + 1));
                if (it.hasNext()) sb.append(",");
                sb.append("\n");
            }
            sb.append(pad).append("}");
            return sb.toString();
        } else if (obj instanceof List) {
            List<?> list = (List<?>) obj;
            if (list.isEmpty()) return "[]";
            StringBuilder sb = new StringBuilder("[\n");
            for (int i = 0; i < list.size(); i++) {
                sb.append(pad1).append(toJsonString(list.get(i), indent + 1));
                if (i < list.size() - 1) sb.append(",");
                sb.append("\n");
            }
            sb.append(pad).append("]");
            return sb.toString();
        } else if (obj instanceof String) {
            return "\"" + escapeJson(obj.toString()) + "\"";
        } else if (obj instanceof Number || obj instanceof Boolean) {
            return obj.toString();
        } else {
            return "\"" + obj.toString() + "\"";
        }
    }

    private static Object parseJsonValue(String json, int[] pos) {
        skipWhitespace(json, pos);
        char c = json.charAt(pos[0]);
        if (c == '{') return parseJsonObject(json, pos);
        if (c == '[') return parseJsonArray(json, pos);
        if (c == '"') return parseJsonString(json, pos);
        int start = pos[0];
        while (pos[0] < json.length() && ",}] \t\r\n".indexOf(json.charAt(pos[0])) == -1) pos[0]++;
        String token = json.substring(start, pos[0]);
        if ("true".equals(token)) return Boolean.TRUE;
        if ("false".equals(token)) return Boolean.FALSE;
        if ("null".equals(token)) return null;
        if (token.contains(".")) return Double.parseDouble(token);
        return Long.parseLong(token);
    }

    private static Map<String, Object> parseJsonObject(String json, int[] pos) {
        Map<String, Object> result = new LinkedHashMap<>();
        pos[0]++; // skip '{'
        skipWhitespace(json, pos);
        if (json.charAt(pos[0]) == '}') { pos[0]++; return result; }
        while (true) {
            skipWhitespace(json, pos);
            String key = parseJsonString(json, pos);
            skipWhitespace(json, pos);
            pos[0]++; // skip ':'
            Object value = parseJsonValue(json, pos);
            result.put(key, value);
            skipWhitespace(json, pos);
            if (json.charAt(pos[0]) == '}') { pos[0]++; return result; }
            pos[0]++; // skip ','
        }
    }

    private static List<Object> parseJsonArray(String json, int[] pos) {
        List<Object> result = new ArrayList<>();
        pos[0]++; // skip '['
        skipWhitespace(json, pos);
        if (json.charAt(pos[0]) == ']') { pos[0]++; return result; }
        while (true) {
            result.add(parseJsonValue(json, pos));
            skipWhitespace(json, pos);
            if (json.charAt(pos[0]) == ']') { pos[0]++; return result; }
            pos[0]++; // skip ','
        }
    }

    private static String parseJsonString(String json, int[] pos) {
        pos[0]++; // skip opening '"'
        StringBuilder sb = new StringBuilder();
        while (json.charAt(pos[0]) != '"') {
            if (json.charAt(pos[0]) == '\\') {
                pos[0]++;
                switch (json.charAt(pos[0])) {
                    case '"': sb.append('"'); break;
                    case '\\': sb.append('\\'); break;
                    case 'n': sb.append('\n'); break;
                    case 'r': sb.append('\r'); break;
                    case 't': sb.append('\t'); break;
                    default: sb.append(json.charAt(pos[0])); break;
                }
            } else {
                sb.append(json.charAt(pos[0]));
            }
            pos[0]++;
        }
        pos[0]++; // skip closing '"'
        return sb.toString();
    }

    private static void skipWhitespace(String json, int[] pos) {
        while (pos[0] < json.length() && Character.isWhitespace(json.charAt(pos[0]))) pos[0]++;
    }
}
