using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;

namespace CaseUco
{
    /// <summary>
    /// Bounded JSON-LD node writer using a frozen explicit context (#80).
    /// The conservative preflight guarantees the per-node serialization buffer
    /// cannot exceed MaxNodeBytes. Atomic mode preserves an existing destination.
    /// </summary>
    public sealed class JsonLdStreamWriter : IDisposable
    {
        private static readonly HashSet<string> AbsoluteSchemes = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        { "http", "https", "urn", "mailto", "file", "data", "did", "tag" };

        private readonly string _path;
        private readonly string _tmpPath;
        private readonly Dictionary<string, string> _context;
        private readonly bool _atomic;
        private readonly bool _pretty;
        private FileStream _stream;
        private StreamWriter _writer;
        private bool _failed;
        private bool _complete;
        private int _nodes;
        private long _bytes;
        private long _maxNode;

        public long MaxNodeBytes { get; }

        public JsonLdStreamWriter(
            string path,
            IDictionary<string, string> context,
            long maxNodeBytes = 1_048_576,
            bool atomic = true,
            bool pretty = true)
        {
            if (string.IsNullOrWhiteSpace(path)) throw new ArgumentException("Path is required", nameof(path));
            if (context == null || context.Count == 0)
                throw new ArgumentException("A non-empty frozen JSON-LD context is required", nameof(context));
            if (maxNodeBytes <= 0) throw new ArgumentOutOfRangeException(nameof(maxNodeBytes));
            _path = Path.GetFullPath(path);
            _context = new Dictionary<string, string>(context, StringComparer.Ordinal);
            if (_context.Any(kv => string.IsNullOrWhiteSpace(kv.Key) || kv.Value == null))
                throw new ArgumentException("Context prefixes and IRIs must be non-empty strings", nameof(context));
            MaxNodeBytes = maxNodeBytes;
            _atomic = atomic;
            _pretty = pretty;
            var directory = Path.GetDirectoryName(_path);
            if (string.IsNullOrEmpty(directory)) directory = ".";
            Directory.CreateDirectory(directory);
            var temporaryName = $".case-uco-{Guid.NewGuid():N}.jsonld.tmp";
            _tmpPath = atomic
                ? string.Concat(
                    directory.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar),
                    Path.DirectorySeparatorChar,
                    temporaryName)
                : _path;
            _stream = new FileStream(_tmpPath, FileMode.Create, FileAccess.Write, FileShare.None);
            _writer = new StreamWriter(_stream, new UTF8Encoding(false));
            var sortedContext = _context.OrderBy(kv => kv.Key, StringComparer.Ordinal)
                .ToDictionary(kv => kv.Key, kv => kv.Value);
            Emit("{\"@context\":" + (pretty ? " " : ""));
            Emit(CaseGraph.ToJsonString(sortedContext, pretty ? 0 : -1));
            Emit(pretty ? ",\n\"@graph\": [\n" : ",\"@graph\":[");
        }

        public void WriteNode(IDictionary<string, object> node)
        {
            if (_complete || _writer == null) throw new InvalidOperationException("Writer is closed");
            if (_failed) throw new InvalidOperationException("Writer is in a failed state");
            if (node == null) throw new ArgumentNullException(nameof(node));
            try
            {
                ValidatePrefixes(node);
                var upperBound = JsonUpperBound(node);
                if (upperBound > MaxNodeBytes)
                    throw new InvalidOperationException($"Node exceeds MaxNodeBytes={MaxNodeBytes}");
                var json = CaseGraph.ToJsonString(node, _pretty ? 1 : -1);
                var actual = Encoding.UTF8.GetByteCount(json);
                if (actual > MaxNodeBytes)
                    throw new InvalidOperationException($"Node exceeds MaxNodeBytes={MaxNodeBytes}");
                if (_nodes > 0) Emit(_pretty ? ",\n" : ",");
                Emit(json);
                _nodes++;
                _maxNode = Math.Max(_maxNode, actual);
            }
            catch
            {
                _failed = true;
                throw;
            }
        }

        public BoundedStreamingWriteResult Complete()
        {
            if (_complete) return Metrics;
            if (_failed)
            {
                Abort();
                throw new InvalidOperationException("Cannot complete a failed writer");
            }
            try
            {
                Emit(_pretty ? "\n]\n}\n" : "]}");
                _writer.Flush();
                _stream.Flush(true);
                _writer.Dispose();
                _writer = null;
                _stream = null;
                if (_atomic)
                {
                    if (File.Exists(_path))
                        File.Replace(_tmpPath, _path, null, true);
                    else
                        File.Move(_tmpPath, _path);
                }
                _complete = true;
                return Metrics;
            }
            catch
            {
                _failed = true;
                Abort();
                throw;
            }
        }

        public BoundedStreamingWriteResult Metrics =>
            new BoundedStreamingWriteResult(_nodes, _bytes, _maxNode);

        public void Dispose()
        {
            if (_complete) return;
            if (_failed) Abort();
            else Complete();
        }

        private void Abort()
        {
            _writer?.Dispose();
            _writer = null;
            _stream = null;
            if (_atomic && File.Exists(_tmpPath)) File.Delete(_tmpPath);
        }

        private void Emit(string value)
        {
            _writer.Write(value);
            _bytes += Encoding.UTF8.GetByteCount(value);
        }

        private void ValidatePrefixes(object value, string parentKey = null)
        {
            if (value is IDictionary dictionary)
            {
                foreach (DictionaryEntry entry in dictionary)
                {
                    if (!(entry.Key is string key))
                        throw new ArgumentException("JSON-LD object keys must be strings");
                    if (!key.StartsWith("@", StringComparison.Ordinal)) CheckIri(key);
                    if ((key == "@id" || key == "@type") && entry.Value is string iri) CheckIri(iri);
                    ValidatePrefixes(entry.Value, key);
                }
            }
            else if (!(value is string) && value is IEnumerable values)
            {
                foreach (var item in values)
                {
                    if ((parentKey == "@id" || parentKey == "@type") && item is string iri) CheckIri(iri);
                    ValidatePrefixes(item, parentKey);
                }
            }
        }

        private void CheckIri(string value)
        {
            var colon = value.IndexOf(':');
            if (colon <= 0) return;
            var prefix = value.Substring(0, colon);
            if (!_context.ContainsKey(prefix) && !AbsoluteSchemes.Contains(prefix))
                throw new ArgumentException($"Undeclared JSON-LD prefix '{prefix}'");
        }

        private static long JsonUpperBound(object value)
        {
            if (value == null) return 4;
            if (value is string text) return 2L + 6L * Encoding.UTF8.GetByteCount(text);
            if (value is bool) return 5;
            if (value is IDictionary dictionary)
            {
                long total = 2;
                foreach (DictionaryEntry entry in dictionary)
                    total += JsonUpperBound(Convert.ToString(entry.Key, CultureInfo.InvariantCulture))
                        + 1 + JsonUpperBound(entry.Value) + 1;
                return total;
            }
            if (value is IEnumerable sequence)
            {
                long total = 2;
                foreach (var item in sequence) total += JsonUpperBound(item) + 1;
                return total;
            }
            return 128;
        }
    }

    public sealed class BoundedStreamingWriteResult
    {
        public int Nodes { get; }
        public long BytesWritten { get; }
        public long MaxNodeBytesWritten { get; }
        public BoundedStreamingWriteResult(int nodes, long bytesWritten, long maxNodeBytesWritten)
        {
            Nodes = nodes;
            BytesWritten = bytesWritten;
            MaxNodeBytesWritten = maxNodeBytesWritten;
        }
    }
}
