package org.caseontology;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Bounded frozen-context JSON-LD node writer (#80). */
public final class JsonLdStreamWriter implements AutoCloseable {
    private static final Set<String> ABSOLUTE_SCHEMES = Set.of(
        "http", "https", "urn", "mailto", "file", "data", "did", "tag");

    private final Path target;
    private final Path output;
    private final Map<String, String> context;
    private final long maxNodeBytes;
    private final boolean atomic;
    private final boolean pretty;
    private FileOutputStream stream;
    private Writer writer;
    private boolean failed;
    private boolean complete;
    private int nodes;
    private long bytesWritten;
    private long maxNodeBytesWritten;

    public JsonLdStreamWriter(Path path, Map<String, String> context) throws IOException {
        this(path, context, 1_048_576L, true, true);
    }

    public JsonLdStreamWriter(
            Path path, Map<String, String> context, long maxNodeBytes,
            boolean atomic, boolean pretty) throws IOException {
        if (path == null) throw new IllegalArgumentException("path is required");
        if (context == null || context.isEmpty())
            throw new IllegalArgumentException("a non-empty frozen JSON-LD context is required");
        if (maxNodeBytes <= 0) throw new IllegalArgumentException("maxNodeBytes must be positive");
        this.target = path;
        this.context = Collections.unmodifiableMap(new LinkedHashMap<>(context));
        this.maxNodeBytes = maxNodeBytes;
        this.atomic = atomic;
        this.pretty = pretty;
        Path parent = path.toAbsolutePath().getParent();
        if (parent == null) parent = Paths.get(".");
        Files.createDirectories(parent);
        this.output = atomic
            ? Files.createTempFile(parent, "." + path.getFileName() + ".", ".jsonld.tmp")
            : path;
        this.stream = new FileOutputStream(output.toFile());
        this.writer = new OutputStreamWriter(stream, StandardCharsets.UTF_8);
        Map<String, Object> sorted = new java.util.TreeMap<>();
        sorted.putAll(this.context);
        emit("{\"@context\":" + (pretty ? " " : ""));
        emit(CaseGraph.toJsonString(sorted, pretty ? 0 : -1));
        emit(pretty ? ",\n\"@graph\": [\n" : ",\"@graph\":[");
    }

    public void writeNode(Map<String, Object> node) throws IOException {
        if (writer == null || complete) throw new IllegalStateException("writer is closed");
        if (failed) throw new IllegalStateException("writer is in a failed state");
        if (node == null) throw new IllegalArgumentException("node is required");
        try {
            validatePrefixes(node, null);
            if (jsonUpperBound(node) > maxNodeBytes) {
                throw new IllegalArgumentException("node exceeds maxNodeBytes=" + maxNodeBytes);
            }
            String json = CaseGraph.toJsonString(node, pretty ? 1 : -1);
            long actual = json.getBytes(StandardCharsets.UTF_8).length;
            if (actual > maxNodeBytes) {
                throw new IllegalArgumentException("node exceeds maxNodeBytes=" + maxNodeBytes);
            }
            if (nodes > 0) emit(pretty ? ",\n" : ",");
            emit(json);
            nodes++;
            maxNodeBytesWritten = Math.max(maxNodeBytesWritten, actual);
        } catch (IOException | RuntimeException ex) {
            failed = true;
            throw ex;
        }
    }

    public BoundedStreamingWriteResult complete() throws IOException {
        if (complete) return metrics();
        if (failed) {
            abort();
            throw new IllegalStateException("cannot complete a failed writer");
        }
        try {
            emit(pretty ? "\n]\n}\n" : "]}");
            writer.flush();
            stream.getChannel().force(true);
            writer.close();
            writer = null;
            stream = null;
            if (atomic) {
                try {
                    Files.move(output, target, StandardCopyOption.REPLACE_EXISTING,
                        StandardCopyOption.ATOMIC_MOVE);
                } catch (AtomicMoveNotSupportedException ex) {
                    Files.move(output, target, StandardCopyOption.REPLACE_EXISTING);
                }
            }
            complete = true;
            return metrics();
        } catch (IOException | RuntimeException ex) {
            failed = true;
            abort();
            throw ex;
        }
    }

    public BoundedStreamingWriteResult metrics() {
        return new BoundedStreamingWriteResult(nodes, bytesWritten, maxNodeBytesWritten);
    }

    @Override
    public void close() throws IOException {
        if (complete) return;
        if (failed) abort();
        else complete();
    }

    private void abort() throws IOException {
        IOException failure = null;
        if (writer != null) {
            try { writer.close(); } catch (IOException ex) { failure = ex; }
            writer = null;
            stream = null;
        }
        if (atomic) Files.deleteIfExists(output);
        if (failure != null) throw failure;
    }

    private void emit(String text) throws IOException {
        writer.write(text);
        bytesWritten += text.getBytes(StandardCharsets.UTF_8).length;
    }

    @SuppressWarnings("unchecked")
    private void validatePrefixes(Object value, String parentKey) {
        if (value instanceof Map) {
            for (Map.Entry<?, ?> entry : ((Map<?, ?>) value).entrySet()) {
                if (!(entry.getKey() instanceof String))
                    throw new IllegalArgumentException("JSON-LD object keys must be strings");
                String key = (String) entry.getKey();
                if (!key.startsWith("@")) checkIri(key);
                if (("@id".equals(key) || "@type".equals(key)) && entry.getValue() instanceof String)
                    checkIri((String) entry.getValue());
                validatePrefixes(entry.getValue(), key);
            }
        } else if (value instanceof Collection) {
            for (Object item : (Collection<Object>) value) {
                if (("@id".equals(parentKey) || "@type".equals(parentKey)) && item instanceof String)
                    checkIri((String) item);
                validatePrefixes(item, parentKey);
            }
        }
    }

    private void checkIri(String value) {
        int colon = value.indexOf(':');
        if (colon <= 0) return;
        String prefix = value.substring(0, colon);
        if (!context.containsKey(prefix) && !ABSOLUTE_SCHEMES.contains(prefix.toLowerCase()))
            throw new IllegalArgumentException("undeclared JSON-LD prefix '" + prefix + "'");
    }

    private static long jsonUpperBound(Object value) {
        if (value == null) return 4;
        if (value instanceof String)
            return 2L + 6L * ((String) value).getBytes(StandardCharsets.UTF_8).length;
        if (value instanceof Boolean) return 5;
        if (value instanceof Map) {
            long total = 2;
            for (Map.Entry<?, ?> entry : ((Map<?, ?>) value).entrySet())
                total += jsonUpperBound(String.valueOf(entry.getKey()))
                    + 1 + jsonUpperBound(entry.getValue()) + 1;
            return total;
        }
        if (value instanceof Collection) {
            long total = 2;
            for (Object item : (Collection<?>) value) total += jsonUpperBound(item) + 1;
            return total;
        }
        return 128;
    }

    /** Metrics returned by the bounded writer. */
    public static final class BoundedStreamingWriteResult {
        private final int nodes;
        private final long bytesWritten;
        private final long maxNodeBytesWritten;
        public BoundedStreamingWriteResult(int nodes, long bytesWritten, long maxNodeBytesWritten) {
            this.nodes = nodes;
            this.bytesWritten = bytesWritten;
            this.maxNodeBytesWritten = maxNodeBytesWritten;
        }
        public int getNodes() { return nodes; }
        public long getBytesWritten() { return bytesWritten; }
        public long getMaxNodeBytesWritten() { return maxNodeBytesWritten; }
    }
}
