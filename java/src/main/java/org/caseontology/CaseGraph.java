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
        validateRequiredFields(instance);
        idMap.put(instance, id);
        Map<String, Object> jsonObj = toJsonLd(instance, id);
        objects.add(jsonObj);
        return id;
    }

    private void validateRequiredFields(Object instance) {
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
     * Validate this graph against CASE/UCO SHACL constraints using case_validate.
     * Requires case-utils ({@code pip install case-utils}) on PATH.
     *
     * @param caseVersion the CASE built-version to validate against (e.g. "case-1.4.0")
     * @return the validation output on success
     * @throws IOException if the process cannot be started or temp file fails
     * @throws RuntimeException if validation fails or case_validate is not found
     */
    public String validate(String caseVersion) throws IOException {
        java.nio.file.Path tmp = java.nio.file.Files.createTempFile("case-uco-", ".jsonld");
        try {
            write(tmp.toAbsolutePath().toString());
            String caseValidateBin = resolveCommand("case_validate");
            ProcessBuilder pb = new ProcessBuilder(
                caseValidateBin, "--built-version", caseVersion, tmp.toAbsolutePath().toString());
            pb.redirectErrorStream(false);
            Process proc = pb.start();
            String stdout = new String(proc.getInputStream().readAllBytes());
            String stderr = new String(proc.getErrorStream().readAllBytes());
            int exitCode = proc.waitFor();
            if (exitCode != 0) {
                String msg = stderr.isBlank() ? stdout : stderr;
                throw new RuntimeException("Validation failed:\n" + msg.trim());
            }
            return stdout;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Validation interrupted", e);
        } finally {
            java.nio.file.Files.deleteIfExists(tmp);
        }
    }

    private static String resolveCommand(String command) {
        String pathEnv = System.getenv("PATH");
        if (pathEnv != null) {
            for (String dir : pathEnv.split(java.io.File.pathSeparator)) {
                java.io.File candidate = new java.io.File(dir, command);
                if (candidate.isFile() && candidate.canExecute()) {
                    return candidate.getAbsolutePath();
                }
            }
        }
        throw new RuntimeException(
            command + " not found on PATH. Install with: pip install case-utils");
    }

    /**
     * Validate this graph using the default CASE version (case-1.4.0).
     */
    public String validate() throws IOException {
        return validate("case-1.4.0");
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

    /**
     * Result of parsing a JSON-LD string into typed objects.
     */
    public static class FromJsonLdResult {
        private final CaseGraph graph;
        private final List<Object> objects;

        public FromJsonLdResult(CaseGraph graph, List<Object> objects) {
            this.graph = graph;
            this.objects = objects;
        }

        public CaseGraph getGraph() { return graph; }
        public List<Object> getObjects() { return objects; }
    }

    /**
     * Parse a JSON-LD string into typed objects where possible.
     * Types are matched by scanning for classes with CLASS_IRI static fields
     * in the org.caseontology packages.
     */
    @SuppressWarnings("unchecked")
    public static FromJsonLdResult fromJsonLd(String json) {
        Map<String, Object> doc = (Map<String, Object>) parseJsonValue(json.trim(), new int[]{0});
        CaseGraph graph = new CaseGraph();

        if (doc.containsKey("@context") && doc.get("@context") instanceof Map) {
            Map<String, Object> ctx = (Map<String, Object>) doc.get("@context");
            for (Map.Entry<String, Object> entry : ctx.entrySet()) {
                if (entry.getValue() instanceof String) {
                    graph.context.put(entry.getKey(), (String) entry.getValue());
                }
            }
        }

        List<Object> typedObjects = new ArrayList<>();

        if (doc.containsKey("@graph") && doc.get("@graph") instanceof List) {
            List<Object> graphList = (List<Object>) doc.get("@graph");
            for (Object item : graphList) {
                if (item instanceof Map) {
                    Map<String, Object> mapItem = (Map<String, Object>) item;
                    graph.objects.add(mapItem);
                    Object typed = tryInstantiate(mapItem, graph.context);
                    typedObjects.add(typed != null ? typed : mapItem);
                }
            }
        }

        return new FromJsonLdResult(graph, typedObjects);
    }

    private static String expandIri(String value, Map<String, String> context) {
        if (value == null) return null;
        int colonIdx = value.indexOf(':');
        if (colonIdx > 0) {
            String prefix = value.substring(0, colonIdx);
            String ns = context.get(prefix);
            if (ns != null) return ns + value.substring(colonIdx + 1);
        }
        return value;
    }

    private static Object tryInstantiate(Map<String, Object> obj, Map<String, String> context) {
        Object typeObj = obj.get("@type");
        if (!(typeObj instanceof String)) return null;

        String expandedIri = expandIri((String) typeObj, context);
        String localName = expandedIri.substring(expandedIri.lastIndexOf('/') + 1);

        List<String> candidates = new ArrayList<>();
        candidates.add("org.caseontology." + localName);
        int orgIdx = expandedIri.indexOf(".org/");
        if (orgIdx > 0) {
            String path = expandedIri.substring(orgIdx + 5);
            int lastSlash = path.lastIndexOf('/');
            if (lastSlash > 0) {
                String pkg = path.substring(0, lastSlash).replace('/', '.').replace('-', '_');
                candidates.add("org.caseontology." + pkg + "." + localName);
            }
        }

        for (String className : candidates) {
            try {
                Class<?> cls = Class.forName(className);
                Field classIriField = cls.getDeclaredField("CLASS_IRI");
                if (!expandedIri.equals(classIriField.get(null))) continue;

                Object instance = cls.getDeclaredConstructor().newInstance();
                setFieldsFromJsonLd(instance, obj);
                return instance;
            } catch (Exception ignored) {}
        }

        return null;
    }

    private static void setFieldsFromJsonLd(Object instance, Map<String, Object> obj) {
        Class<?> current = instance.getClass();
        while (current != null && current != Object.class) {
            for (Field field : current.getDeclaredFields()) {
                if (Modifier.isStatic(field.getModifiers())) continue;

                String nsPrefix = "uco-core";
                try {
                    Field nsPrefixField = field.getDeclaringClass().getDeclaredField("NAMESPACE_PREFIX");
                    nsPrefix = (String) nsPrefixField.get(null);
                } catch (Exception ignored) {}

                String propKey = nsPrefix + ":" + field.getName();
                if (!obj.containsKey(propKey)) continue;

                field.setAccessible(true);
                try {
                    Object value = convertFromJsonLd(obj.get(propKey), field.getType());
                    field.set(instance, value);
                } catch (Exception ignored) {}
            }
            current = current.getSuperclass();
        }
    }

    @SuppressWarnings("unchecked")
    private static Object convertFromJsonLd(Object value, Class<?> target) {
        if (value == null) return null;

        if (value instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) value;
            if (map.containsKey("@value")) {
                Object raw = map.get("@value");
                if (raw instanceof String) {
                    String s = (String) raw;
                    if (target == String.class) return s;
                    try {
                        if (target == int.class || target == Integer.class) return Integer.parseInt(s);
                        if (target == long.class || target == Long.class) return Long.parseLong(s);
                        if (target == double.class || target == Double.class) return Double.parseDouble(s);
                    } catch (NumberFormatException e) {
                        return s;
                    }
                    if (target == boolean.class || target == Boolean.class) return "true".equals(s);
                }
                return raw;
            }
        }

        if (target == String.class && value instanceof String) return value;
        if ((target == long.class || target == Long.class) && value instanceof Long) return value;
        if ((target == int.class || target == Integer.class) && value instanceof Long)
            return ((Long) value).intValue();
        if ((target == double.class || target == Double.class) && value instanceof Double) return value;
        if ((target == boolean.class || target == Boolean.class) && value instanceof Boolean) return value;

        return value;
    }

    /**
     * Estimate the number of RDF triples this graph will produce.
     */
    public int estimateTriples() {
        int total = 0;
        for (Map<String, Object> obj : objects) {
            total += countTriples(obj);
        }
        return total;
    }

    @SuppressWarnings("unchecked")
    private static int countTriples(Map<String, Object> obj) {
        int count = 0;
        for (Map.Entry<String, Object> entry : obj.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();
            if ("@id".equals(key)) continue;
            if ("@type".equals(key)) { count++; continue; }
            if (value instanceof List) {
                for (Object item : (List<Object>) value) {
                    if (item instanceof Map) {
                        count += 1 + countTriples((Map<String, Object>) item);
                    } else {
                        count++;
                    }
                }
            } else if (value instanceof Map) {
                Map<String, Object> map = (Map<String, Object>) value;
                if (map.containsKey("@value")) {
                    count++;
                } else {
                    count += 1 + countTriples(map);
                }
            } else {
                count++;
            }
        }
        return count;
    }

    /**
     * Split the graph into smaller chunks of at most maxObjects each.
     */
    public List<CaseGraph> split(int maxObjects) {
        List<CaseGraph> chunks = new ArrayList<>();
        for (int i = 0; i < objects.size(); i += maxObjects) {
            CaseGraph chunk = new CaseGraph(context.get("kb"));
            chunk.context.putAll(context);
            int end = Math.min(i + maxObjects, objects.size());
            for (int j = i; j < end; j++) {
                chunk.objects.add(objects.get(j));
            }
            chunks.add(chunk);
        }
        return chunks;
    }

    /**
     * Load and merge multiple JSON-LD files into a single graph.
     */
    public static CaseGraph mergeFiles(List<String> paths) throws IOException {
        return mergeFiles(paths, "http://example.org/kb/");
    }

    /**
     * Load and merge multiple JSON-LD files into a single graph.
     */
    public static CaseGraph mergeFiles(List<String> paths, String kbPrefix) throws IOException {
        CaseGraph merged = new CaseGraph(kbPrefix);
        for (String path : paths) {
            merged.loadFile(path);
        }
        return merged;
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
        try {
            if (token.contains(".")) return Double.parseDouble(token);
            return Long.parseLong(token);
        } catch (NumberFormatException e) {
            return token;
        }
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
