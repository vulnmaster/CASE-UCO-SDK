// CaseGraph — main entry point for building and serializing CASE/UCO graphs in Java.
package org.caseontology;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.time.ZonedDateTime;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Deque;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.ServiceLoader;
import java.util.Comparator;
import java.lang.ref.WeakReference;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.UUID;

/**
 * Build a CASE/UCO JSON-LD graph with typed objects.
 */
public class CaseGraph {

    private static final ConcurrentHashMap<String, Class<?>> CLASS_REGISTRY_CACHE = new ConcurrentHashMap<>();
    private static final ConcurrentHashMap<Class<?>, List<FieldBinding>> FIELD_BINDING_CACHE = new ConcurrentHashMap<>();
    private static final Object CLASS_REGISTRY_LOCK = new Object();
    private static volatile boolean classRegistryBuilt = false;
    private static final ConcurrentHashMap<String, WeakReference<ClassRegistryProvider>>
        EXPLICIT_CLASS_PROVIDERS = new ConcurrentHashMap<>();
    private static volatile WeakReference<ClassLoader> providerClassLoader =
        new WeakReference<>(CaseGraph.class.getClassLoader());
    private static final AtomicLong CLASS_REGISTRY_HITS = new AtomicLong();
    private static final AtomicLong CLASS_REGISTRY_MISSES = new AtomicLong();
    private static final AtomicLong CLASS_REGISTRY_GENERATION = new AtomicLong();

    private final Map<String, String> context;
    private final List<Map<String, Object>> objects;
    private final Map<Object, String> idMap;
    private final Map<String, Integer> iriIndex = new LinkedHashMap<>();
    private final Set<String> usedPrefixSet = new HashSet<>();
    private String onDuplicate = "reject";
    private final List<DeserializationWarning> deserializationWarnings = new ArrayList<>();

    public CaseGraph() {
        this("http://example.org/kb/");
    }

    public CaseGraph(String kbPrefix) {
        this(kbPrefix, null);
    }

    public CaseGraph(String kbPrefix, Map<String, String> extraContext) {
        this.context = new LinkedHashMap<>(defaultContext());
        this.context.put("kb", kbPrefix);
        this.objects = new ArrayList<>();
        this.idMap = new IdentityHashMap<>();
        if (extraContext != null) {
            for (Map.Entry<String, String> e : extraContext.entrySet()) {
                mergeContextEntry(e.getKey(), e.getValue());
            }
        }
    }

    /** Named duplicate policy: reject | merge_identical | merge_compatible | replace. */
    public String getOnDuplicate() { return onDuplicate; }
    public void setOnDuplicate(String onDuplicate) {
        this.onDuplicate = normalizeDuplicatePolicy(onDuplicate);
    }

    /** Backward-compatible boolean view of {@link #getOnDuplicate()}. */
    public boolean isRejectDuplicates() {
        return "reject".equals(normalizeDuplicatePolicy(onDuplicate));
    }

    public void setRejectDuplicates(boolean rejectDuplicates) {
        this.onDuplicate = rejectDuplicates ? "reject" : "merge_compatible";
    }

    public List<DeserializationWarning> getDeserializationWarnings() {
        return Collections.unmodifiableList(deserializationWarnings);
    }

    public void addContext(String prefix, String iri) {
        mergeContextEntry(prefix, iri);
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
        appendObject(jsonObj);
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
     * Return a deep copy of the JSON-LD map for a node by compact or expanded {@code @id}.
     * Nested lists/maps are not shared with the graph.
     */
    public Map<String, Object> get(String id) {
        Map<String, Object> obj = findObject(id);
        if (obj == null) {
            return null;
        }
        return deepCopyMap(obj);
    }

    /**
     * Return true if a node with this {@code @id} (compact or expanded) exists.
     */
    public boolean contains(String id) {
        return findObject(id) != null;
    }

    /**
     * Expand a compact IRI using this graph's context.
     */
    public String expandIri(String id) {
        return expandCompactIri(id, context);
    }

    /**
     * Create or update a JSON-LD node by {@code @id}. Returns a deep copy.
     */
    public Map<String, Object> upsertNode(String id, Object types, Map<String, Object> properties) {
        Map<String, Object> obj = findObject(id);
        if (obj == null) {
            obj = new LinkedHashMap<>();
            obj.put("@id", id);
            if (types != null) {
                obj.put("@type", normalizeTypeValue(types));
            }
            if (properties != null) {
                for (Map.Entry<String, Object> entry : properties.entrySet()) {
                    applyProperty(obj, entry.getKey(), entry.getValue(), id, "merge_compatible");
                }
            }
            appendObject(obj);
            return deepCopyMap(obj);
        }

        if (types != null) {
            obj.put("@type", normalizeTypeValue(mergeTypes(obj.get("@type"), types)));
        }
        if (properties != null) {
            for (Map.Entry<String, Object> entry : properties.entrySet()) {
                applyProperty(obj, entry.getKey(), entry.getValue(), id, "merge_compatible");
            }
        }
        return deepCopyMap(obj);
    }

    public Map<String, Object> upsertNode(String id) {
        return upsertNode(id, null, null);
    }

    /**
     * Add an {@code rdf:type} to an existing node (same {@code @id}).
     */
    public void addType(String id, String typeIri) {
        Map<String, Object> obj = requireObject(id);
        obj.put("@type", normalizeTypeValue(mergeTypes(obj.get("@type"), typeIri)));
        trackPrefixesFor(Collections.singletonMap("@type", typeIri));
    }

    /**
     * Add or merge a property on an existing node (merge_compatible).
     */
    public void addProperty(String id, String key, Object value) {
        Map<String, Object> obj = requireObject(id);
        applyProperty(obj, key, value, id, "merge_compatible");
    }

    /** Replace a property value (replace / scalar overwrite mode). */
    public void setPropertyValue(String id, String key, Object value) {
        Map<String, Object> obj = requireObject(id);
        applyProperty(obj, key, value, id, "replace");
    }

    /**
     * Add a direct property edge source --predicate--> target.
     */
    public void link(String sourceId, String predicate, String targetId) {
        Map<String, Object> targetRef = new LinkedHashMap<>();
        targetRef.put("@id", targetId);
        addProperty(sourceId, predicate, targetRef);
    }

    /**
     * Create a uco-core:Relationship node with deterministic {@code @id}.
     */
    public Map<String, Object> createRelationship(
            String sourceId,
            String targetId,
            String kind,
            boolean directional,
            String description,
            String relationshipId) {
        if (!contains(sourceId)) {
            throw new IllegalArgumentException("Relationship source not in graph: " + sourceId);
        }
        if (!contains(targetId)) {
            throw new IllegalArgumentException("Relationship target not in graph: " + targetId);
        }
        if (kind == null || kind.isEmpty()) {
            throw new IllegalArgumentException("kindOfRelationship is required");
        }

        String relId = relationshipId != null ? relationshipId : deterministicRelationshipId(sourceId, targetId, kind);
        Map<String, Object> props = new LinkedHashMap<>();
        List<Map<String, Object>> sources = new ArrayList<>();
        Map<String, Object> sourceRef = new LinkedHashMap<>();
        sourceRef.put("@id", sourceId);
        sources.add(sourceRef);
        props.put("uco-core:source", sources);

        List<Map<String, Object>> targets = new ArrayList<>();
        Map<String, Object> targetRef = new LinkedHashMap<>();
        targetRef.put("@id", targetId);
        targets.add(targetRef);
        props.put("uco-core:target", targets);

        props.put("uco-core:kindOfRelationship", kind);
        props.put("uco-core:isDirectional", typedLiteral("xsd:boolean", directional ? "true" : "false"));
        if (description != null) {
            props.put("uco-core:description", description);
        }

        return upsertNode(relId, "uco-core:Relationship", props);
    }

    public Map<String, Object> createRelationship(
            String sourceId,
            String targetId,
            String kind,
            boolean directional,
            String description) {
        return createRelationship(sourceId, targetId, kind, directional, description, null);
    }

    public Map<String, Object> createRelationship(String sourceId, String targetId, String kind) {
        return createRelationship(sourceId, targetId, kind, true, null, null);
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
        doc.put("@context", prunedContext());
        doc.put("@graph", objects);
        return doc;
    }

    private Map<String, String> prunedContext() {
        Set<String> used = usedPrefixSet.isEmpty() ? usedPrefixes() : usedPrefixSet;
        if (used.isEmpty()) {
            used = usedPrefixes();
        }
        Map<String, String> pruned = new LinkedHashMap<>();
        for (Map.Entry<String, String> entry : context.entrySet()) {
            if (used.contains(entry.getKey())) {
                pruned.put(entry.getKey(), entry.getValue());
            }
        }
        return pruned;
    }

    private Set<String> usedPrefixes() {
        Set<String> prefixes = new HashSet<>();
        Set<String> contextKeys = context.keySet();
        for (Map<String, Object> obj : objects) {
            collectPrefixes(obj, contextKeys, prefixes);
        }
        return prefixes;
    }

    private void trackPrefixesFor(Object node) {
        collectPrefixes(node, context.keySet(), usedPrefixSet);
    }

    private static String extractPrefix(String value, Set<String> contextKeys) {
        if (value.contains("://")) return null;
        int colon = value.indexOf(':');
        if (colon > 0) {
            String prefix = value.substring(0, colon);
            if (contextKeys.contains(prefix)) return prefix;
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    private static void collectPrefixes(Object node, Set<String> contextKeys, Set<String> out) {
        if (node instanceof Map) {
            for (Map.Entry<String, Object> entry : ((Map<String, Object>) node).entrySet()) {
                String p = extractPrefix(entry.getKey(), contextKeys);
                if (p != null) out.add(p);
                Object val = entry.getValue();
                if (val instanceof String) {
                    p = extractPrefix((String) val, contextKeys);
                    if (p != null) out.add(p);
                } else {
                    collectPrefixes(val, contextKeys, out);
                }
            }
        } else if (node instanceof List) {
            for (Object item : (List<Object>) node) {
                if (item instanceof String) {
                    String p = extractPrefix((String) item, contextKeys);
                    if (p != null) out.add(p);
                } else {
                    collectPrefixes(item, contextKeys, out);
                }
            }
        }
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
        try (Writer writer = new OutputStreamWriter(Files.newOutputStream(Paths.get(path)), StandardCharsets.UTF_8)) {
            writer.write(serialize());
        }
    }

    /**
     * Stream JSON-LD to disk without building a second full-document string (#71).
     *
     * <p>Emits {@code @context} then each {@code @graph} element incrementally.
     * Writes via a temp file then atomic rename by default. Use
     * {@link #serialize()} when a complete string is needed.
     *
     * @return nodes written and UTF-8 bytes emitted
     */
    public StreamingWriteResult writeStreaming(String path) throws IOException {
        return writeStreaming(path, true);
    }

    /**
     * Stream JSON-LD to disk (#71).
     *
     * @param atomic when true, write through a temp file and rename into place
     */
    public StreamingWriteResult writeStreaming(String path, boolean atomic) throws IOException {
        java.nio.file.Path target = Paths.get(path);
        java.nio.file.Path outPath = target;
        java.nio.file.Path tmpPath = null;
        if (atomic) {
            java.nio.file.Path parent = target.toAbsolutePath().getParent();
            if (parent == null) {
                parent = Paths.get(".");
            }
            Files.createDirectories(parent);
            tmpPath = Files.createTempFile(parent, ".casegraph-", ".jsonld.tmp");
            outPath = tmpPath;
        }
        long bytesWritten = 0;
        try {
            try (CountingWriter writer = new CountingWriter(
                    new OutputStreamWriter(Files.newOutputStream(outPath), StandardCharsets.UTF_8))) {
                Map<String, String> ctx = prunedContext();
                writer.write("{\n");
                writer.write("  \"@context\": ");
                writer.write(toJsonString(ctx, 1));
                writer.write(",\n");
                writer.write("  \"@graph\": [\n");
                for (int i = 0; i < objects.size(); i++) {
                    writer.write(indentJsonLines(toJsonString(objects.get(i), 2), "    "));
                    if (i + 1 < objects.size()) {
                        writer.write(",\n");
                    } else {
                        writer.write("\n");
                    }
                }
                writer.write("  ]\n");
                writer.write("}\n");
                writer.flush();
                bytesWritten = writer.getBytesWritten();
            }
            if (atomic && tmpPath != null) {
                try {
                    Files.move(tmpPath, target, java.nio.file.StandardCopyOption.REPLACE_EXISTING,
                        java.nio.file.StandardCopyOption.ATOMIC_MOVE);
                } catch (java.nio.file.AtomicMoveNotSupportedException ex) {
                    Files.move(tmpPath, target, java.nio.file.StandardCopyOption.REPLACE_EXISTING);
                }
                tmpPath = null;
            }
            return new StreamingWriteResult(objects.size(), bytesWritten);
        } catch (IOException | RuntimeException ex) {
            if (tmpPath != null) {
                Files.deleteIfExists(tmpPath);
            }
            throw ex;
        }
    }

    /** Metrics from an atomic/incremental streaming write (#71). */
    public static final class StreamingWriteResult {
        private final int nodes;
        private final long bytesWritten;

        public StreamingWriteResult(int nodes, long bytesWritten) {
            this.nodes = nodes;
            this.bytesWritten = bytesWritten;
        }

        public int getNodes() { return nodes; }
        public long getBytesWritten() { return bytesWritten; }
    }

    private static final class CountingWriter extends Writer {
        private final Writer inner;
        private long bytesWritten;

        CountingWriter(Writer inner) {
            this.inner = inner;
        }

        long getBytesWritten() {
            return bytesWritten;
        }

        @Override
        public void write(char[] cbuf, int off, int len) throws IOException {
            inner.write(cbuf, off, len);
            bytesWritten += new String(cbuf, off, len).getBytes(StandardCharsets.UTF_8).length;
        }

        @Override
        public void write(String str) throws IOException {
            inner.write(str);
            bytesWritten += str.getBytes(StandardCharsets.UTF_8).length;
        }

        @Override
        public void flush() throws IOException {
            inner.flush();
        }

        @Override
        public void close() throws IOException {
            inner.close();
        }
    }

    /**
     * Invalidate the process-wide deserialization class registry (#70).
     */
    public static void clearClassRegistryCache() {
        synchronized (CLASS_REGISTRY_LOCK) {
            clearClassRegistryCacheLocked();
        }
    }

    private static void clearClassRegistryCacheLocked() {
        CLASS_REGISTRY_CACHE.clear();
        FIELD_BINDING_CACHE.clear();
        classRegistryBuilt = false;
        CLASS_REGISTRY_GENERATION.incrementAndGet();
    }

    /** Observable registry state for benchmarks and dynamic-loading tests (#82). */
    public static final class ClassRegistryCacheMetrics {
        private final long hits;
        private final long misses;
        private final long generation;
        private final int registeredProviders;
        private final int cachedClasses;

        public ClassRegistryCacheMetrics(
                long hits, long misses, long generation,
                int registeredProviders, int cachedClasses) {
            this.hits = hits;
            this.misses = misses;
            this.generation = generation;
            this.registeredProviders = registeredProviders;
            this.cachedClasses = cachedClasses;
        }
        public long getHits() { return hits; }
        public long getMisses() { return misses; }
        public long getGeneration() { return generation; }
        public int getRegisteredProviders() { return registeredProviders; }
        public int getCachedClasses() { return cachedClasses; }
    }

    /** Expose field-binding cache size for warm-path unit tests (#70). */
    public static int fieldBindingCacheCount() {
        return FIELD_BINDING_CACHE.size();
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
            String stdout = new String(proc.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
            String stderr = new String(proc.getErrorStream().readAllBytes(), StandardCharsets.UTF_8);
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
    public void load(String json) {
        load(json, null);
    }

    @SuppressWarnings("unchecked")
    public void load(String json, String onDuplicatePolicy) {
        String policy = normalizeDuplicatePolicy(onDuplicatePolicy != null ? onDuplicatePolicy : onDuplicate);
        Map<String, Object> doc = (Map<String, Object>) parseJsonValue(json.trim(), new int[]{0});
        Map<String, String> snapCtx = new LinkedHashMap<>(context);
        List<Map<String, Object>> snapObjects = new ArrayList<>();
        for (Map<String, Object> o : objects) snapObjects.add(deepCopyMap(o));
        Map<String, Integer> snapIndex = new LinkedHashMap<>(iriIndex);
        try {
            if (doc.containsKey("@context") && doc.get("@context") instanceof Map) {
                mergeContext((Map<String, Object>) doc.get("@context"));
            }
            if (doc.containsKey("@graph") && doc.get("@graph") instanceof List) {
                List<Object> graphList = (List<Object>) doc.get("@graph");
                for (Object item : graphList) {
                    if (item instanceof Map) {
                        ingestRawNode(deepCopyMap((Map<String, Object>) item), policy);
                    }
                }
            }
        } catch (RuntimeException ex) {
            context.clear();
            context.putAll(snapCtx);
            objects.clear();
            objects.addAll(snapObjects);
            iriIndex.clear();
            iriIndex.putAll(snapIndex);
            throw ex;
        }
    }

    /**
     * Read and load a JSON-LD file into this graph.
     */
    public void loadFile(String path) throws IOException {
        String json = Files.readString(Paths.get(path), StandardCharsets.UTF_8);
        load(json);
    }

    /**
     * Result of parsing a JSON-LD string into typed objects.
     */
    /** Typed diagnostic when a JSON-LD node falls back to a raw map. */
    public static class DeserializationWarning {
        private final String nodeId;
        private final String reason;
        private final String detail;
        public DeserializationWarning(String nodeId, String reason, String detail) {
            this.nodeId = nodeId;
            this.reason = reason;
            this.detail = detail == null ? "" : detail;
        }
        public String getNodeId() { return nodeId; }
        public String getReason() { return reason; }
        public String getDetail() { return detail; }
    }

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
     * in the org.caseontology packages. When {@code @type} is an array, the
     * most specific unambiguous registered class is chosen.
     */
    @SuppressWarnings("unchecked")
    public static FromJsonLdResult fromJsonLd(String json) {
        Map<String, Object> doc = (Map<String, Object>) parseJsonValue(json.trim(), new int[]{0});
        CaseGraph graph = new CaseGraph();

        if (doc.containsKey("@context") && doc.get("@context") instanceof Map) {
            graph.mergeContext((Map<String, Object>) doc.get("@context"));
        }

        List<Object> typedObjects = new ArrayList<>();

        if (doc.containsKey("@graph") && doc.get("@graph") instanceof List) {
            List<Object> graphList = (List<Object>) doc.get("@graph");
            for (Object item : graphList) {
                if (item instanceof Map) {
                    Map<String, Object> mapItem = (Map<String, Object>) item;
                    graph.ingestRawNode(deepCopyMap(mapItem), graph.onDuplicate);
                    DeserializationWarning[] warnOut = new DeserializationWarning[1];
                    Object typed = tryInstantiate(mapItem, graph.context, warnOut);
                    if (warnOut[0] != null) {
                        graph.deserializationWarnings.add(warnOut[0]);
                    }
                    typedObjects.add(typed != null ? typed : mapItem);
                }
            }
        }

        return new FromJsonLdResult(graph, typedObjects);
    }

    private void mergeContext(Map<String, Object> incoming) {
        for (Map.Entry<String, Object> entry : incoming.entrySet()) {
            if (!(entry.getValue() instanceof String)) {
                continue;
            }
            mergeContextEntry(entry.getKey(), (String) entry.getValue());
        }
    }

    private void mergeContextEntry(String prefix, String ns) {
        String existing = context.get(prefix);
        if (existing != null && !existing.equals(ns)) {
            throw new IllegalArgumentException(
                "Context prefix collision for '" + prefix +
                "': existing '" + existing + "' vs incoming '" + ns + "'");
        }
        context.put(prefix, ns);
    }

    private static String expandCompactIri(String value, Map<String, String> context) {
        if (value == null) return null;
        int colonIdx = value.indexOf(':');
        if (colonIdx > 0) {
            String prefix = value.substring(0, colonIdx);
            String ns = context.get(prefix);
            if (ns != null) return ns + value.substring(colonIdx + 1);
        }
        return value;
    }

    private static Object tryInstantiate(Map<String, Object> obj, Map<String, String> context, DeserializationWarning[] warningOut) {
        String nodeId = obj.get("@id") instanceof String ? (String) obj.get("@id") : null;
        Object typeObj = obj.get("@type");
        if (typeObj == null) {
            if (warningOut != null && warningOut.length > 0) {
                warningOut[0] = new DeserializationWarning(nodeId, "missing_type", "node has no @type");
            }
            return null;
        }

        List<String> typeStrings = asTypeList(typeObj);
        List<Class<?>> matched = new ArrayList<>();
        for (String typeStr : typeStrings) {
            Class<?> found = findClassByIri(expandCompactIri(typeStr, context));
            if (found != null && !matched.contains(found)) {
                matched.add(found);
            }
        }

        Class<?> selected = selectMostSpecificClass(matched);
        if (selected == null) {
            if (warningOut != null && warningOut.length > 0) {
                warningOut[0] = matched.isEmpty()
                    ? new DeserializationWarning(nodeId, "unregistered_type", "no registered class for @type")
                    : new DeserializationWarning(nodeId, "ambiguous_type", "multiple incomparable types matched");
            }
            return null;
        }

        try {
            Object instance = selected.getDeclaredConstructor().newInstance();
            setFieldsFromJsonLd(instance, obj);
            return instance;
        } catch (Exception ex) {
            if (warningOut != null && warningOut.length > 0) {
                warningOut[0] = new DeserializationWarning(nodeId, "constructor_failed", ex.getMessage());
            }
            return null;
        }
    }

    private static Class<?> findClassByIri(String expandedIri) {
        if (expandedIri == null) {
            return null;
        }
        ensureClassRegistryBuilt();
        Class<?> cached = CLASS_REGISTRY_CACHE.get(expandedIri);
        if (cached != null) {
            CLASS_REGISTRY_HITS.incrementAndGet();
            return cached;
        }

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
                if (!expandedIri.equals(classIriField.get(null))) {
                    continue;
                }
                CLASS_REGISTRY_CACHE.putIfAbsent(expandedIri, cls);
                CLASS_REGISTRY_MISSES.incrementAndGet();
                return cls;
            } catch (Exception ignored) {}
        }
        CLASS_REGISTRY_MISSES.incrementAndGet();
        return null;
    }

    private static void ensureClassRegistryBuilt() {
        if (classRegistryBuilt) {
            return;
        }
        synchronized (CLASS_REGISTRY_LOCK) {
            if (!classRegistryBuilt) {
                buildClassRegistry();
                classRegistryBuilt = true;
            }
        }
    }

    @SuppressWarnings("unchecked")
    private static void buildClassRegistry() {
        for (String className : OntologyRegistry.listClasses()) {
            Map<String, Object> meta = OntologyRegistry.getClass(className);
            if (meta == null) {
                continue;
            }
            Object iriObj = meta.get("iri");
            Object moduleObj = meta.get("module");
            if (!(iriObj instanceof String) || !(moduleObj instanceof String)) {
                continue;
            }
            String iri = (String) iriObj;
            String fqcn = moduleToPackage((String) moduleObj) + "." + className;
            try {
                Class<?> cls = Class.forName(fqcn);
                Field classIriField = cls.getDeclaredField("CLASS_IRI");
                String classIri = (String) classIriField.get(null);
                if (!iri.equals(classIri)) {
                    continue;
                }
                addRegistryClass(iri, cls);
            } catch (ClassNotFoundException | NoSuchFieldException | IllegalAccessException ignored) {
            }
        }

        List<ClassRegistryProvider> providers = new ArrayList<>();
        ClassLoader loader = providerClassLoader.get();
        if (loader == null) {
            loader = CaseGraph.class.getClassLoader();
            providerClassLoader = new WeakReference<>(loader);
        }
        for (ClassRegistryProvider provider : ServiceLoader.load(ClassRegistryProvider.class, loader)) {
            providers.add(provider);
        }
        for (Map.Entry<String, WeakReference<ClassRegistryProvider>> entry
                : EXPLICIT_CLASS_PROVIDERS.entrySet()) {
            ClassRegistryProvider provider = entry.getValue().get();
            if (provider != null) {
                providers.add(provider);
            } else {
                EXPLICIT_CLASS_PROVIDERS.remove(entry.getKey(), entry.getValue());
            }
        }
        providers.sort(Comparator
            .comparingInt(ClassRegistryProvider::priority).reversed()
            .thenComparing(ClassRegistryProvider::source));
        Set<String> loadedSources = new HashSet<>();
        for (ClassRegistryProvider provider : providers) {
            if (provider.source() == null || provider.source().trim().isEmpty()) {
                throw new IllegalArgumentException("ClassRegistryProvider source must be non-empty");
            }
            if (!loadedSources.add(provider.source())) {
                continue;
            }
            Collection<Class<?>> classes = provider.classes();
            if (classes == null) {
                throw new IllegalArgumentException(
                    "ClassRegistryProvider '" + provider.source() + "' returned null classes");
            }
            for (Class<?> cls : classes) {
                try {
                    Field iriField = cls.getDeclaredField("CLASS_IRI");
                    String iri = (String) iriField.get(null);
                    if (iri == null || iri.trim().isEmpty()) {
                        throw new IllegalArgumentException(
                            "Extension class " + cls.getName() + " has no CLASS_IRI");
                    }
                    addRegistryClass(iri, cls);
                } catch (NoSuchFieldException | IllegalAccessException ex) {
                    throw new IllegalArgumentException(
                        "Extension class " + cls.getName() + " has no accessible CLASS_IRI", ex);
                }
            }
        }
    }

    private static void addRegistryClass(String iri, Class<?> cls) {
        Class<?> existing = CLASS_REGISTRY_CACHE.putIfAbsent(iri, cls);
        if (existing != null && existing != cls) {
            throw new ClassRegistryConflictException(iri, existing, cls);
        }
    }

    /** Explicitly register a trusted provider and rebuild atomically (#82). */
    public static long registerClassRegistryProvider(ClassRegistryProvider provider) {
        Objects.requireNonNull(provider, "provider");
        String source = Objects.requireNonNull(provider.source(), "provider.source").trim();
        if (source.isEmpty()) {
            throw new IllegalArgumentException("ClassRegistryProvider source must be non-empty");
        }
        synchronized (CLASS_REGISTRY_LOCK) {
            WeakReference<ClassRegistryProvider> prior = EXPLICIT_CLASS_PROVIDERS.put(
                source, new WeakReference<>(provider));
            clearClassRegistryCacheLocked();
            try {
                buildClassRegistry();
                classRegistryBuilt = true;
                return CLASS_REGISTRY_GENERATION.get();
            } catch (RuntimeException ex) {
                if (prior == null) EXPLICIT_CLASS_PROVIDERS.remove(source);
                else EXPLICIT_CLASS_PROVIDERS.put(source, prior);
                CLASS_REGISTRY_CACHE.clear();
                FIELD_BINDING_CACHE.clear();
                classRegistryBuilt = false;
                throw ex;
            }
        }
    }

    /** Remove one explicitly registered provider and invalidate caches (#82). */
    public static long unregisterClassRegistryProvider(String source) {
        synchronized (CLASS_REGISTRY_LOCK) {
            if (EXPLICIT_CLASS_PROVIDERS.remove(source) != null) {
                clearClassRegistryCacheLocked();
            }
            return CLASS_REGISTRY_GENERATION.get();
        }
    }

    /** Select a new ServiceLoader class loader and invalidate without retaining it strongly. */
    public static long reloadClassRegistryProviders(ClassLoader loader) {
        Objects.requireNonNull(loader, "loader");
        synchronized (CLASS_REGISTRY_LOCK) {
            providerClassLoader = new WeakReference<>(loader);
            clearClassRegistryCacheLocked();
            return CLASS_REGISTRY_GENERATION.get();
        }
    }

    /** Process-wide class lookup counters and cache generation (#82). */
    public static ClassRegistryCacheMetrics classRegistryCacheMetrics() {
        return new ClassRegistryCacheMetrics(
            CLASS_REGISTRY_HITS.get(), CLASS_REGISTRY_MISSES.get(),
            CLASS_REGISTRY_GENERATION.get(), EXPLICIT_CLASS_PROVIDERS.size(),
            CLASS_REGISTRY_CACHE.size());
    }

    private static String moduleToPackage(String module) {
        if (module.startsWith("case.")) {
            return "org.caseontology._case." + module.substring("case.".length());
        }
        return "org.caseontology." + module;
    }

    private static Class<?> selectMostSpecificClass(List<Class<?>> classes) {
        if (classes == null || classes.isEmpty()) {
            return null;
        }
        if (classes.size() == 1) {
            return classes.get(0);
        }
        List<Class<?>> specific = new ArrayList<>();
        for (Class<?> c : classes) {
            boolean shadowed = false;
            for (Class<?> o : classes) {
                if (o != c && c.isAssignableFrom(o)) {
                    shadowed = true;
                    break;
                }
            }
            if (!shadowed) {
                specific.add(c);
            }
        }
        return specific.size() == 1 ? specific.get(0) : null;
    }

    private static final class FieldBinding {
        final Field field;
        final String propKey;

        FieldBinding(Field field, String propKey) {
            this.field = field;
            this.propKey = propKey;
        }
    }

    private static List<FieldBinding> getFieldBindings(Class<?> cls) {
        List<FieldBinding> cached = FIELD_BINDING_CACHE.get(cls);
        if (cached != null) {
            return cached;
        }
        List<FieldBinding> bindings = new ArrayList<>();
        Class<?> current = cls;
        while (current != null && current != Object.class) {
            for (Field field : current.getDeclaredFields()) {
                if (Modifier.isStatic(field.getModifiers())) continue;

                String nsPrefix = "uco-core";
                try {
                    Field nsPrefixField = field.getDeclaringClass().getDeclaredField("NAMESPACE_PREFIX");
                    nsPrefix = (String) nsPrefixField.get(null);
                } catch (Exception ignored) {}

                String propKey = nsPrefix + ":" + field.getName();
                field.setAccessible(true);
                bindings.add(new FieldBinding(field, propKey));
            }
            current = current.getSuperclass();
        }
        List<FieldBinding> immutable = Collections.unmodifiableList(bindings);
        List<FieldBinding> raced = FIELD_BINDING_CACHE.putIfAbsent(cls, immutable);
        return raced != null ? raced : immutable;
    }

    private static void setFieldsFromJsonLd(Object instance, Map<String, Object> obj) {
        for (FieldBinding binding : getFieldBindings(instance.getClass())) {
            if (!obj.containsKey(binding.propKey)) continue;
            try {
                Object value = convertFromJsonLd(obj.get(binding.propKey), binding.field.getType());
                binding.field.set(instance, value);
            } catch (Exception ignored) {}
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
            if ("@type".equals(key)) {
                if (value instanceof List) count += ((List<?>) value).size();
                else count++;
                continue;
            }
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
     *
     * <p><b>Warning:</b> Object-count splitting is only safe for independent
     * catalog-style graphs (hash lists, IoC feeds). For investigation graphs,
     * prefer {@link #partitionByRoots} at natural forensic boundaries
     * (per-volume, per-app, per-device).
     */
    public List<CaseGraph> split(int maxObjects) {
        if (maxObjects <= 0) {
            throw new IllegalArgumentException("split maxObjects must be a positive integer, got " + maxObjects);
        }
        List<CaseGraph> chunks = new ArrayList<>();
        for (int i = 0; i < objects.size(); i += maxObjects) {
            CaseGraph chunk = new CaseGraph(context.get("kb"));
            chunk.context.putAll(context);
            int end = Math.min(i + maxObjects, objects.size());
            for (int j = i; j < end; j++) {
                chunk.appendObject(deepCopyMap(objects.get(j)));
            }
            chunks.add(chunk);
        }
        return chunks;
    }

    /**
     * Experimental root closure (#72).
     *
     * <p>Each root IRI defines a partition. Top-level nodes reachable from that
     * root via nested {@code @id} references are included (outgoing). When
     * {@code includeIncoming} is true (default), reverse references from other
     * top-level objects (e.g. Relationships pointing at the root) are also
     * followed. Nodes reachable from multiple roots follow {@code sharedNodePolicy}:
     * {@code replicate-identical} (default) deep-copies shared nodes into every
     * partition that needs them; {@code isolate-shared} places multi-root nodes only
     * in a {@code _shared} partition.
     */
    public Map<String, CaseGraph> partitionByRoots(
            Collection<String> rootIris, String sharedNodePolicy, boolean includeIncoming) {
        return partitionByRootsWithManifest(
            rootIris,
            new PartitionOptions()
                .setSharedNodePolicy(sharedNodePolicy)
                .setIncludeIncoming(includeIncoming)).getPartitions();
    }

    /** Marking-safe root partitioning with reconstruction metadata (#79). */
    public PartitionResult partitionByRootsWithManifest(
            Collection<String> rootIris, PartitionOptions options) {
        if (rootIris == null || rootIris.isEmpty()) {
            throw new IllegalArgumentException("rootIris must be a non-empty collection");
        }
        if (options == null) {
            options = new PartitionOptions();
        }
        String requestedPolicy = options.getSharedNodePolicy();
        String policy = normalizeSharedNodePolicy(requestedPolicy);
        if (!"none".equals(options.getBoundaryPolicy())
                && !"marking-and-authorization".equals(options.getBoundaryPolicy())) {
            throw new IllegalArgumentException("Unknown boundaryPolicy: " + options.getBoundaryPolicy());
        }
        if (!"error-on-cross-boundary".equals(options.getCrossBoundaryPolicy())
                && !"home-partition-reference".equals(options.getCrossBoundaryPolicy())) {
            throw new IllegalArgumentException(
                "Unknown crossBoundaryPolicy: " + options.getCrossBoundaryPolicy());
        }
        if (!"full".equals(options.getManifestDetail())
                && !"safe".equals(options.getManifestDetail())) {
            throw new IllegalArgumentException("manifestDetail must be 'full' or 'safe'");
        }

        Map<String, Map<String, Object>> byExpandedId = buildExpandedIdIndex();
        Map<String, Set<String>> reverseIndex = buildReverseIdIndex(byExpandedId);
        Map<String, Set<String>> closures = new LinkedHashMap<>();
        for (String root : new LinkedHashSet<>(rootIris)) {
            String expanded = expandIri(root);
            if (byExpandedId.containsKey(expanded)) {
                closures.put(root, dependencyClosure(
                    root, byExpandedId, reverseIndex, options.isIncludeIncoming()));
            }
        }

        Map<String, BoundarySets> boundaries = new LinkedHashMap<>();
        for (Map.Entry<String, Map<String, Object>> entry : byExpandedId.entrySet()) {
            boundaries.put(entry.getKey(), extractPartitionBoundary(entry.getValue()));
        }
        Map<String, BoundarySets> declared = new LinkedHashMap<>();
        Map<String, Set<String>> omissions = new LinkedHashMap<>();
        for (String root : closures.keySet()) {
            omissions.put(root, new LinkedHashSet<>());
        }
        if ("marking-and-authorization".equals(options.getBoundaryPolicy())) {
            for (String root : closures.keySet()) {
                PartitionBoundary supplied = options.getRootBoundaries().get(root);
                if (supplied == null) {
                    declared.put(root, boundaries.get(expandIri(root)));
                } else {
                    Set<String> markings = new LinkedHashSet<>();
                    for (String value : supplied.getMarkings()) markings.add(expandIri(value));
                    Set<String> authorizations = new LinkedHashSet<>();
                    for (String value : supplied.getAuthorizations()) authorizations.add(expandIri(value));
                    declared.put(root, new BoundarySets(markings, authorizations));
                }
            }
            for (Map.Entry<String, Set<String>> entry : closures.entrySet()) {
                BoundarySets allowed = declared.get(entry.getKey());
                for (String nodeId : new ArrayList<>(entry.getValue())) {
                    BoundarySets required = boundaries.get(nodeId);
                    List<String> missingMarkings = sortedDifference(required.markings, allowed.markings);
                    List<String> missingAuthorizations = sortedDifference(
                        required.authorizations, allowed.authorizations);
                    if (missingMarkings.isEmpty() && missingAuthorizations.isEmpty()) continue;
                    if (expandIri(entry.getKey()).equals(nodeId)
                            || "error-on-cross-boundary".equals(options.getCrossBoundaryPolicy())) {
                        throw new PartitionBoundaryException(
                            entry.getKey(), originalId(byExpandedId.get(nodeId), nodeId),
                            missingMarkings, missingAuthorizations);
                    }
                    entry.getValue().remove(nodeId);
                    omissions.get(entry.getKey()).add(nodeId);
                }
            }
        }

        Map<String, String> boundaryHomes = new LinkedHashMap<>();
        Set<String> omittedNodes = new LinkedHashSet<>();
        for (Set<String> omitted : omissions.values()) omittedNodes.addAll(omitted);
        List<String> sortedOmitted = new ArrayList<>(omittedNodes);
        Collections.sort(sortedOmitted);
        for (String nodeId : sortedOmitted) {
            List<String> candidates = new ArrayList<>();
            for (Map.Entry<String, Set<String>> entry : closures.entrySet()) {
                if (entry.getValue().contains(nodeId)) candidates.add(entry.getKey());
            }
            Collections.sort(candidates);
            if (candidates.isEmpty()) {
                BoundarySets required = boundaries.get(nodeId);
                throw new PartitionBoundaryException(
                    "<no-authorized-home>", originalId(byExpandedId.get(nodeId), nodeId),
                    sorted(required.markings), sorted(required.authorizations));
            }
            boundaryHomes.put(nodeId, candidates.get(0));
        }

        Map<String, Set<String>> nodeOwners = new LinkedHashMap<>();
        for (Map.Entry<String, Set<String>> entry : closures.entrySet()) {
            for (String nodeId : entry.getValue()) {
                nodeOwners.computeIfAbsent(nodeId, ignored -> new LinkedHashSet<>()).add(entry.getKey());
            }
        }
        if ("error-on-cross-boundary".equals(policy)) {
            List<String> overlap = new ArrayList<>();
            for (Map.Entry<String, Set<String>> entry : nodeOwners.entrySet()) {
                if (entry.getValue().size() > 1) overlap.add(entry.getKey());
            }
            Collections.sort(overlap);
            if (!overlap.isEmpty()) {
                throw new IllegalStateException("shared nodes cross partition boundaries: " + overlap);
            }
        }
        Map<String, String> homes = new LinkedHashMap<>();
        if ("home-partition-reference".equals(policy)) {
            for (Map.Entry<String, Set<String>> entry : nodeOwners.entrySet()) {
                if (entry.getValue().size() <= 1) continue;
                List<String> owners = new ArrayList<>(entry.getValue());
                Collections.sort(owners);
                String compactNodeId = originalId(byExpandedId.get(entry.getKey()), entry.getKey());
                homes.put(entry.getKey(), owners.contains(compactNodeId) ? compactNodeId : owners.get(0));
            }
        }

        Map<String, CaseGraph> partitions = new LinkedHashMap<>();
        for (Map.Entry<String, Set<String>> entry : closures.entrySet()) {
            CaseGraph partition = newPartitionGraph();
            for (String nodeId : entry.getValue()) {
                int ownerCount = nodeOwners.get(nodeId).size();
                if (ownerCount > 1 && "support-graph".equals(policy)) continue;
                if (ownerCount > 1 && "home-partition-reference".equals(policy)
                        && !entry.getKey().equals(homes.get(nodeId))) continue;
                appendPartitionNode(partition, byExpandedId.get(nodeId));
            }
            partitions.put(entry.getKey(), partition);
        }
        if ("support-graph".equals(policy)) {
            CaseGraph support = newPartitionGraph();
            for (Map.Entry<String, Set<String>> entry : nodeOwners.entrySet()) {
                if (entry.getValue().size() > 1) appendPartitionNode(support, byExpandedId.get(entry.getKey()));
            }
            if (!support.objects.isEmpty()) {
                partitions.put("support-graph".equals(requestedPolicy) ? "_support" : "_shared", support);
            }
        }

        Map<String, Object> partitionMetadata = new LinkedHashMap<>();
        for (Map.Entry<String, CaseGraph> entry : partitions.entrySet()) {
            String hash = entry.getValue().graphFingerprint(entry.getValue().objects);
            Map<String, Object> metadata = new LinkedHashMap<>();
            metadata.put("partition_id", "urn:sha256:" + hash);
            metadata.put("node_count", entry.getValue().objects.size());
            metadata.put("triple_estimate", entry.getValue().estimateTriples());
            metadata.put("sha256", hash);
            BoundarySets scope = declared.get(entry.getKey());
            metadata.put("effective_markings", scope == null ? new ArrayList<>() : sorted(scope.markings));
            metadata.put("authorization_scope", scope == null ? new ArrayList<>() : sorted(scope.authorizations));
            if ("full".equals(options.getManifestDetail())) {
                List<String> nodeIds = new ArrayList<>();
                for (Map<String, Object> node : entry.getValue().objects) {
                    nodeIds.add(originalId(node, ""));
                }
                Collections.sort(nodeIds);
                metadata.put("node_ids", nodeIds);
            }
            partitionMetadata.put(entry.getKey(), metadata);
        }
        Map<String, String> routes = new LinkedHashMap<>();
        for (Map.Entry<String, String> entry : homes.entrySet()) {
            routes.put(originalId(byExpandedId.get(entry.getKey()), entry.getKey()), entry.getValue());
        }
        for (Map.Entry<String, String> entry : boundaryHomes.entrySet()) {
            routes.put(originalId(byExpandedId.get(entry.getKey()), entry.getKey()), entry.getValue());
        }
        boolean referenced = "support-graph".equals(policy)
            || "home-partition-reference".equals(policy) || !omittedNodes.isEmpty();
        String sourceHash = graphFingerprint(objects);
        Map<String, Object> manifest = new LinkedHashMap<>();
        manifest.put("schema_version", "2.0.0");
        manifest.put("dataset_id", "urn:sha256:" + sourceHash);
        manifest.put("source_graph_sha256", sourceHash);
        manifest.put("strategy", options.isIncludeIncoming()
            ? "outgoing_and_incoming_id_closure" : "outgoing_id_closure");
        manifest.put("roots", new ArrayList<>(closures.keySet()));
        manifest.put("shared_node_policy", policy);
        manifest.put("include_incoming", options.isIncludeIncoming());
        manifest.put("boundary_policy", options.getBoundaryPolicy());
        manifest.put("cross_boundary_policy", options.getCrossBoundaryPolicy());
        manifest.put("validation_mode", referenced ? "referenced-partition-set" : "self-contained");
        manifest.put("validation_bundle", options.getValidationBundle());
        manifest.put("partitions", partitionMetadata);
        manifest.put("home_partition_routes", "full".equals(options.getManifestDetail())
            ? routes : new LinkedHashMap<String, String>());
        manifest.put("home_partition_route_count", routes.size());
        Map<String, Object> omissionCounts = new LinkedHashMap<>();
        for (Map.Entry<String, Set<String>> entry : omissions.entrySet()) {
            omissionCounts.put(entry.getKey(), entry.getValue().size());
        }
        manifest.put("boundary_omission_counts", omissionCounts);
        Map<String, Object> reconstruction = new LinkedHashMap<>();
        reconstruction.put("operation", "rdf-union");
        reconstruction.put("deduplicate_by", "@id with identical assertions");
        reconstruction.put("requires_partitions", sorted(partitions.keySet()));
        manifest.put("reconstruction", reconstruction);
        return new PartitionResult(partitions, manifest);
    }

    /** Verify that the exact JSON-LD node union reconstructs this graph. */
    public PartitionUnionVerification verifyPartitionUnion(Map<String, CaseGraph> partitions) {
        if (partitions == null) throw new IllegalArgumentException("partitions is required");
        Map<String, String> source = new LinkedHashMap<>();
        for (Map<String, Object> node : objects) {
            source.put(expandIri(originalId(node, "")), toJsonString(node, 0));
        }
        Map<String, String> union = new LinkedHashMap<>();
        boolean conflict = false;
        for (CaseGraph partition : partitions.values()) {
            for (Map<String, Object> node : partition.objects) {
                String id = expandIri(originalId(node, ""));
                String value = toJsonString(node, 0);
                if (union.containsKey(id) && !union.get(id).equals(value)) conflict = true;
                else union.put(id, value);
            }
        }
        return new PartitionUnionVerification(
            !conflict && source.equals(union), source.size(), union.size());
    }

    public Map<String, CaseGraph> partitionByRoots(Collection<String> rootIris, String sharedNodePolicy) {
        return partitionByRoots(rootIris, sharedNodePolicy, true);
    }

    public Map<String, CaseGraph> partitionByRoots(Collection<String> rootIris) {
        return partitionByRoots(rootIris, "replicate-identical", true);
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

    private void appendObject(Map<String, Object> obj) {
        Object idObj = obj.get("@id");
        String nodeId = idObj instanceof String ? (String) idObj : null;
        if (nodeId != null && findObject(nodeId) != null) {
            throw new IllegalStateException(
                "Duplicate @id '" + nodeId + "': use addType/upsertNode or merge-compatible load instead of appending a second node");
        }
        objects.add(obj);
        if (nodeId != null) {
            indexNode(nodeId, objects.size() - 1);
        }
        trackPrefixesFor(obj);
    }

    private void indexNode(String nodeId, int index) {
        String expanded = expandIri(nodeId);
        iriIndex.put(expanded, index);
    }

    private Map<String, Object> findObject(String nodeId) {
        String expanded = expandIri(nodeId);
        Integer idx = iriIndex.get(expanded);
        if (idx != null && idx < objects.size()) {
            return objects.get(idx);
        }
        return null;
    }

    private Map<String, Object> requireObject(String nodeId) {
        Map<String, Object> obj = findObject(nodeId);
        if (obj == null) {
            throw new IllegalArgumentException("No node with @id '" + nodeId + "'");
        }
        return obj;
    }


    @SuppressWarnings("unchecked")
    private void ingestRawNode(Map<String, Object> raw, String policy) {
        policy = normalizeDuplicatePolicy(policy);
        Object idObj = raw.get("@id");
        if (!(idObj instanceof String)) {
            objects.add(raw);
            trackPrefixesFor(raw);
            return;
        }
        String nodeId = (String) idObj;

        Map<String, Object> existing = findObject(nodeId);
        if (existing == null) {
            appendObject(raw);
            return;
        }

        if ("reject".equals(policy)) {
            throw new IllegalStateException("Duplicate @id '" + nodeId + "': conflicting duplicate during load");
        }
        if ("replace".equals(policy)) {
            Object preserved = existing.containsKey("@id") ? existing.get("@id") : nodeId;
            existing.clear();
            for (Map.Entry<String, Object> e : raw.entrySet()) {
                existing.put(e.getKey(), deepCopyValue(e.getValue()));
            }
            existing.put("@id", preserved);
            trackPrefixesFor(existing);
            return;
        }
        if ("merge_identical".equals(policy)) {
            for (Map.Entry<String, Object> e : raw.entrySet()) {
                if ("@id".equals(e.getKey())) continue;
                if (!existing.containsKey(e.getKey())) {
                    existing.put(e.getKey(), deepCopyValue(e.getValue()));
                    continue;
                }
                if (!jsonLdValuesEqual(existing.get(e.getKey()), e.getValue())) {
                    throw new IllegalStateException(
                        "Duplicate @id '" + nodeId + "': merge_identical conflict on '" + e.getKey() + "'");
                }
            }
            trackPrefixesFor(raw);
            return;
        }
        // merge_compatible
        if (raw.containsKey("@type")) {
            existing.put("@type", normalizeTypeValue(mergeTypes(existing.get("@type"), raw.get("@type"))));
        }
        for (Map.Entry<String, Object> entry : raw.entrySet()) {
            String key = entry.getKey();
            if ("@id".equals(key) || "@type".equals(key)) {
                continue;
            }
            applyProperty(existing, key, entry.getValue(), nodeId, "merge_compatible");
        }
        trackPrefixesFor(raw);
    }

    private static String normalizeDuplicatePolicy(String policy) {
        if ("error".equals(policy)) policy = "reject";
        if (!("reject".equals(policy) || "merge_identical".equals(policy)
                || "merge_compatible".equals(policy) || "replace".equals(policy))) {
            throw new IllegalArgumentException(
                "Unknown duplicate policy: '" + policy +
                "'. Expected one of: reject, merge_identical, merge_compatible, replace");
        }
        return policy;
    }

    @SuppressWarnings("unchecked")
    private void applyProperty(Map<String, Object> obj, String key, Object value, String nodeId, String mode) {
        if ("replace".equals(mode)) {
            obj.put(key, deepCopyValue(value));
            trackPrefixesFor(Collections.singletonMap(key, obj.get(key)));
            return;
        }
        if (!obj.containsKey(key)) {
            obj.put(key, deepCopyValue(value));
            trackPrefixesFor(Collections.singletonMap(key, obj.get(key)));
            return;
        }
        Object existing = obj.get(key);
        if (jsonLdValuesEqual(existing, value)) {
            return;
        }
        if (existing instanceof List) {
            accumulateListValue((List<Object>) existing, value);
            trackPrefixesFor(Collections.singletonMap(key, obj.get(key)));
            return;
        }
        if (value instanceof List) {
            List<Object> merged = new ArrayList<>();
            merged.add(deepCopyValue(existing));
            accumulateListValue(merged, value);
            obj.put(key, merged);
            trackPrefixesFor(Collections.singletonMap(key, merged));
            return;
        }
        // Distinct JSON-LD node references are multi-valued, not scalar conflicts.
        if (existing instanceof Map && value instanceof Map) {
            Map<String, Object> ed = (Map<String, Object>) existing;
            Map<String, Object> vd = (Map<String, Object>) value;
            if (ed.containsKey("@id") && vd.containsKey("@id")) {
                if (jsonLdValuesEqual(existing, value)) {
                    return;
                }
                List<Object> multi = new ArrayList<>();
                multi.add(deepCopyValue(existing));
                multi.add(deepCopyValue(value));
                obj.put(key, multi);
                trackPrefixesFor(Collections.singletonMap(key, multi));
                return;
            }
        }
        throw new IllegalStateException(
            "merge_compatible scalar conflict on '" + key + "': existing and incoming values differ");
    }

    @SuppressWarnings("unchecked")
    private static void accumulateListValue(List<Object> existing, Object value) {
        List<Object> items = value instanceof List ? (List<Object>) value : List.of(value);
        for (Object item : items) {
            boolean found = false;
            for (Object x : existing) {
                if (jsonLdValuesEqual(x, item)) { found = true; break; }
            }
            if (!found) existing.add(deepCopyValue(item));
        }
    }

    @SuppressWarnings("unchecked")
    private static boolean jsonLdValuesEqual(Object a, Object b) {
        if (a == b) return true;
        if (a instanceof Map && b instanceof Map) {
            Map<String, Object> ad = (Map<String, Object>) a;
            Map<String, Object> bd = (Map<String, Object>) b;
            if (ad.containsKey("@value") || bd.containsKey("@value")) {
                if (!(ad.containsKey("@value") && bd.containsKey("@value"))) return false;
                return normalizeLiteralType(stringOrNull(ad.get("@type")))
                        .equals(normalizeLiteralType(stringOrNull(bd.get("@type"))))
                    && normalizeLiteralValue(ad.get("@value"), stringOrNull(ad.get("@type")))
                        .equals(normalizeLiteralValue(bd.get("@value"), stringOrNull(bd.get("@type"))));
            }
            if (ad.containsKey("@id") || bd.containsKey("@id")) {
                return Objects.equals(ad.get("@id"), bd.get("@id"));
            }
        }
        if (a instanceof List && b instanceof List) {
            List<Object> al = (List<Object>) a;
            List<Object> bl = (List<Object>) b;
            if (isIdRefList(al) && isIdRefList(bl)) {
                List<String> asort = new ArrayList<>();
                List<String> bsort = new ArrayList<>();
                for (Object x : al) asort.add(idOf(x));
                for (Object x : bl) bsort.add(idOf(x));
                Collections.sort(asort);
                Collections.sort(bsort);
                return asort.equals(bsort);
            }
            if (al.size() != bl.size()) return false;
            for (int i = 0; i < al.size(); i++) {
                if (!jsonLdValuesEqual(al.get(i), bl.get(i))) return false;
            }
            return true;
        }
        return Objects.equals(a, b);
    }

    private static String stringOrNull(Object o) { return o instanceof String ? (String) o : null; }

    private static String normalizeLiteralType(String typeIri) {
        if (typeIri == null) return "";
        if (typeIri.startsWith("xsd:")) return typeIri;
        if (typeIri.startsWith("http://www.w3.org/2001/XMLSchema#")) {
            return "xsd:" + typeIri.substring(typeIri.lastIndexOf('#') + 1);
        }
        return typeIri;
    }

    private static String normalizeLiteralValue(Object value, String typeIri) {
        if (value instanceof Boolean) return ((Boolean) value) ? "true" : "false";
        if (value instanceof String && normalizeLiteralType(typeIri).contains("boolean")) {
            return ((String) value).toLowerCase();
        }
        return String.valueOf(value);
    }

    @SuppressWarnings("unchecked")
    private static boolean isIdRefList(List<Object> items) {
        if (items.isEmpty()) return false;
        for (Object x : items) {
            if (!(x instanceof Map) || !((Map<?, ?>) x).containsKey("@id")) return false;
        }
        return true;
    }

    @SuppressWarnings("unchecked")
    private static String idOf(Object item) {
        if (item instanceof Map) {
            Object id = ((Map<String, Object>) item).get("@id");
            return id == null ? "" : String.valueOf(id);
        }
        return String.valueOf(item);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> deepCopyMap(Map<String, Object> src) {
        Map<String, Object> copy = new LinkedHashMap<>();
        for (Map.Entry<String, Object> e : src.entrySet()) {
            copy.put(e.getKey(), deepCopyValue(e.getValue()));
        }
        return copy;
    }

    @SuppressWarnings("unchecked")
    private static Object deepCopyValue(Object value) {
        if (value instanceof Map) {
            return deepCopyMap((Map<String, Object>) value);
        }
        if (value instanceof List) {
            List<Object> out = new ArrayList<>();
            for (Object item : (List<Object>) value) out.add(deepCopyValue(item));
            return out;
        }
        return value;
    }


    @SuppressWarnings("unchecked")
    private static List<String> asTypeList(Object types) {
        List<String> result = new ArrayList<>();
        if (types == null) {
            return result;
        }
        if (types instanceof String) {
            result.add((String) types);
            return result;
        }
        if (types instanceof List) {
            for (Object item : (List<Object>) types) {
                if (item != null) {
                    result.add(item.toString());
                }
            }
            return result;
        }
        result.add(types.toString());
        return result;
    }

    private static Object normalizeTypeValue(Object types) {
        List<String> list = asTypeList(types);
        if (list.size() == 1) {
            return list.get(0);
        }
        return list;
    }

    private static Object mergeTypes(Object existing, Object newTypes) {
        List<String> merged = asTypeList(existing);
        for (String typeIri : asTypeList(newTypes)) {
            if (!merged.contains(typeIri)) {
                merged.add(typeIri);
            }
        }
        return merged;
    }

    private static String safeKindSlug(String kind) {
        int maxLen = 64;
        StringBuilder sb = new StringBuilder();
        String trimmed = kind == null ? "" : kind.trim();
        for (int i = 0; i < trimmed.length(); i++) {
            char ch = trimmed.charAt(i);
            if (Character.isLetterOrDigit(ch) || ch == '.' || ch == '_' || ch == '-') {
                sb.append(ch);
            } else {
                sb.append('_');
            }
        }
        String slug = sb.toString().replaceAll("^[._-]+|[._-]+$", "");
        if (slug.isEmpty()) {
            slug = "rel";
        }
        if (slug.length() > maxLen) {
            slug = slug.substring(0, maxLen).replaceAll("[._-]+$", "");
            if (slug.isEmpty()) {
                slug = "rel";
            }
        }
        return slug;
    }

    private String deterministicRelationshipId(String sourceId, String targetId, String kind) {
        String payload = expandIri(sourceId) + "|" + expandIri(targetId) + "|" + kind;
        try {
            MessageDigest sha = MessageDigest.getInstance("SHA-256");
            byte[] hash = sha.digest(payload.getBytes(StandardCharsets.UTF_8));
            StringBuilder digest = new StringBuilder();
            for (int i = 0; i < 6; i++) {
                digest.append(String.format("%02x", hash[i]));
            }
            String safeKind = safeKindSlug(kind);
            return "kb:rel-" + safeKind + "-" + digest;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
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
    static String toJsonString(Object obj, int indent) {
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

    private static String indentJsonLines(String json, String prefix) {
        String[] lines = json.split("\n", -1);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < lines.length; i++) {
            if (i > 0) {
                sb.append('\n');
            }
            sb.append(prefix).append(lines[i]);
        }
        return sb.toString();
    }

    private static final class BoundarySets {
        private final Set<String> markings;
        private final Set<String> authorizations;

        private BoundarySets(Set<String> markings, Set<String> authorizations) {
            this.markings = markings;
            this.authorizations = authorizations;
        }
    }

    private BoundarySets extractPartitionBoundary(Map<String, Object> node) {
        Set<String> markings = new LinkedHashSet<>();
        Set<String> authorizations = new LinkedHashSet<>();
        for (Map.Entry<String, Object> entry : node.entrySet()) {
            String expanded = expandIri(entry.getKey());
            int split = Math.max(expanded.lastIndexOf('/'), expanded.lastIndexOf('#'));
            String local = expanded.substring(split + 1);
            if ("objectMarking".equals(local)) {
                collectBoundaryIds(entry.getValue(), markings);
            } else if ("relevantAuthorization".equals(local)
                    || "requiredAuthorization".equals(local)) {
                collectBoundaryIds(entry.getValue(), authorizations);
            }
        }
        return new BoundarySets(markings, authorizations);
    }

    @SuppressWarnings("unchecked")
    private void collectBoundaryIds(Object value, Set<String> output) {
        if (value instanceof String) {
            output.add(expandIri((String) value));
        } else if (value instanceof Map) {
            Object id = ((Map<String, Object>) value).get("@id");
            if (id instanceof String) output.add(expandIri((String) id));
        } else if (value instanceof Collection) {
            for (Object item : (Collection<?>) value) collectBoundaryIds(item, output);
        }
    }

    private static List<String> sorted(Collection<String> values) {
        List<String> result = new ArrayList<>(values);
        Collections.sort(result);
        return result;
    }

    private static List<String> sortedDifference(Set<String> required, Set<String> allowed) {
        Set<String> difference = new LinkedHashSet<>(required);
        difference.removeAll(allowed);
        return sorted(difference);
    }

    private String graphFingerprint(Collection<Map<String, Object>> nodes) {
        Map<String, Object> document = new LinkedHashMap<>();
        List<String> contextKeys = new ArrayList<>(context.keySet());
        Collections.sort(contextKeys);
        Map<String, Object> sortedContext = new LinkedHashMap<>();
        for (String key : contextKeys) sortedContext.put(key, context.get(key));
        document.put("@context", sortedContext);
        document.put("@graph", new ArrayList<>(nodes));
        try {
            byte[] digest = MessageDigest.getInstance("SHA-256")
                .digest(toJsonString(document, 0).getBytes(StandardCharsets.UTF_8));
            StringBuilder result = new StringBuilder();
            for (byte value : digest) result.append(String.format("%02x", value & 0xff));
            return result.toString();
        } catch (NoSuchAlgorithmException error) {
            throw new IllegalStateException("SHA-256 is unavailable", error);
        }
    }

    private static String originalId(Map<String, Object> node, String fallback) {
        if (node != null && node.get("@id") instanceof String) return (String) node.get("@id");
        return fallback;
    }

    private static String normalizeSharedNodePolicy(String policy) {
        if (policy == null || policy.isEmpty() || "replicate-identical".equals(policy)) {
            return "replicate-identical";
        }
        if ("shared".equals(policy) || "isolate-shared".equals(policy)
                || "_shared".equals(policy) || "support-graph".equals(policy)) {
            return "support-graph";
        }
        if ("home-partition-reference".equals(policy)
                || "error-on-cross-boundary".equals(policy)) {
            return policy;
        }
        throw new IllegalArgumentException(
            "Unknown sharedNodePolicy: '" + policy + "'. Expected replicate-identical, "
            + "support-graph, home-partition-reference, or error-on-cross-boundary");
    }

    private CaseGraph newPartitionGraph() {
        CaseGraph partition = new CaseGraph(context.get("kb"));
        partition.context.putAll(context);
        partition.setOnDuplicate("merge_compatible");
        return partition;
    }

    private void appendPartitionNode(CaseGraph partition, Map<String, Object> node) {
        if (partition == null) {
            return;
        }
        partition.ingestRawNode(deepCopyMap(node), "merge_compatible");
    }

    private Map<String, Map<String, Object>> buildExpandedIdIndex() {
        Map<String, Map<String, Object>> byExpandedId = new LinkedHashMap<>();
        for (Map<String, Object> obj : objects) {
            Object idObj = obj.get("@id");
            if (idObj instanceof String) {
                byExpandedId.put(expandIri((String) idObj), obj);
            }
        }
        return byExpandedId;
    }

    private Map<String, Set<String>> buildReverseIdIndex(Map<String, Map<String, Object>> byExpandedId) {
        Map<String, Set<String>> reverse = new LinkedHashMap<>();
        for (Map.Entry<String, Map<String, Object>> entry : byExpandedId.entrySet()) {
            String ownerExpanded = entry.getKey();
            Set<String> refs = new LinkedHashSet<>();
            collectIdRefs(entry.getValue(), refs);
            for (String ref : refs) {
                String expandedRef = expandIri(ref);
                if (expandedRef.equals(ownerExpanded)) {
                    continue;
                }
                reverse.computeIfAbsent(expandedRef, ignored -> new LinkedHashSet<>()).add(ownerExpanded);
            }
        }
        return reverse;
    }

    private Set<String> dependencyClosure(
            String rootId,
            Map<String, Map<String, Object>> byExpandedId,
            Map<String, Set<String>> reverseIndex,
            boolean includeIncoming) {
        String expandedRoot = expandIri(rootId);
        Set<String> visited = new LinkedHashSet<>();
        Deque<String> queue = new ArrayDeque<>();
        queue.add(expandedRoot);
        while (!queue.isEmpty()) {
            String current = queue.removeFirst();
            if (!visited.add(current)) {
                continue;
            }
            Map<String, Object> node = byExpandedId.get(current);
            if (node == null) {
                continue;
            }
            Set<String> refs = new LinkedHashSet<>();
            collectIdRefs(node, refs);
            for (String ref : refs) {
                String expandedRef = expandIri(ref);
                if (!visited.contains(expandedRef) && byExpandedId.containsKey(expandedRef)) {
                    queue.add(expandedRef);
                }
            }
            if (includeIncoming && reverseIndex != null) {
                Set<String> referrers = reverseIndex.get(current);
                if (referrers != null) {
                    for (String referrer : referrers) {
                        if (!visited.contains(referrer) && byExpandedId.containsKey(referrer)) {
                            queue.add(referrer);
                        }
                    }
                }
            }
        }
        return visited;
    }

    private Set<String> dependencyClosure(String rootId, Map<String, Map<String, Object>> byExpandedId) {
        return dependencyClosure(rootId, byExpandedId, buildReverseIdIndex(byExpandedId), true);
    }

    @SuppressWarnings("unchecked")
    private static void collectIdRefs(Object node, Set<String> out) {
        if (node instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) node;
            Object idObj = map.get("@id");
            if (idObj instanceof String) {
                out.add((String) idObj);
            }
            for (Object value : map.values()) {
                collectIdRefs(value, out);
            }
        } else if (node instanceof List) {
            for (Object item : (List<Object>) node) {
                collectIdRefs(item, out);
            }
        }
    }
}
