// CaseGraph — main entry point for building and serializing CASE/UCO graphs in C#.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Threading;

namespace CaseUco
{
    /// <summary>
    /// Build a CASE/UCO JSON-LD graph with typed objects.
    /// </summary>
    public class CaseGraph
    {
        private static readonly object RegistryLock = new object();
        private static volatile Dictionary<string, Type> _classRegistryCache;
        private static readonly Dictionary<string, ExtensionTypeRegistration> ExtensionTypes =
            new Dictionary<string, ExtensionTypeRegistration>(StringComparer.Ordinal);
        private static long _classRegistryHits;
        private static long _classRegistryMisses;
        private static long _classRegistryGeneration;

        /// <summary>
        /// Test hook: when non-null, invoked immediately before atomic replace.
        /// Returning a non-null exception aborts replacement so prior destination
        /// bytes must survive (induced replacement-failure tests).
        /// </summary>
        internal static Func<string, string, Exception> SimulateReplaceFailureForTests;
        private static Dictionary<Type, PropertyBinding[]> _propertyBindingCache;

        private readonly Dictionary<string, string> _context;
        private readonly List<Dictionary<string, object>> _objects;
        private readonly Dictionary<object, string> _idMap;
        private readonly Dictionary<string, int> _iriIndex = new Dictionary<string, int>();
        private readonly List<DeserializationWarning> _deserializationWarnings = new List<DeserializationWarning>();
        private readonly HashSet<string> _usedPrefixSet = new HashSet<string>();

        /// <summary>
        /// Named duplicate policy: reject | merge_identical | merge_compatible | replace.
        /// Alias <c>error</c> maps to <c>reject</c>. Default is <c>reject</c>.
        /// </summary>
        public string OnDuplicate { get; set; } = "reject";

        /// <summary>
        /// Backward-compatible boolean view of <see cref="OnDuplicate"/>.
        /// Prefer named policies for cross-language parity.
        /// </summary>
        public bool RejectDuplicates
        {
            get => NormalizeDuplicatePolicy(OnDuplicate) == "reject";
            set => OnDuplicate = value ? "reject" : "merge_compatible";
        }

        public IReadOnlyList<DeserializationWarning> DeserializationWarnings => _deserializationWarnings;

        public CaseGraph(string kbPrefix = "http://example.org/kb/", IDictionary<string, string> extraContext = null)
        {
            _context = new Dictionary<string, string>(DefaultContext);
            _context["kb"] = kbPrefix;
            _objects = new List<Dictionary<string, object>>();
            _idMap = new Dictionary<object, string>(new ReferenceEqualityComparer());
            if (extraContext != null)
            {
                foreach (var kv in extraContext)
                    MergeContextEntry(kv.Key, kv.Value);
            }
        }

        public void AddContext(string prefix, string iri)
        {
            MergeContextEntry(prefix, iri);
        }

        /// <summary>Add an object to the graph with an auto-generated UUID @id.</summary>
        public string Add(object instance)
        {
            var id = MintId(instance);
            return AddWithId(instance, id);
        }

        /// <summary>Add an object to the graph with a user-supplied @id for deterministic IRIs.</summary>
        public string AddWithId(object instance, string id)
        {
            Validate(instance);
            _idMap[instance] = id;
            var jsonObj = ToJsonLd(instance, id);
            AppendObject(jsonObj);
            return id;
        }

        /// <summary>Validate required fields on a CASE/UCO object before adding it.</summary>
        private void Validate(object instance)
        {
            if (instance == null) return;
            foreach (var prop in instance.GetType()
                .GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Where(p => p.GetCustomAttribute<CaseRequiredAttribute>(inherit: true) != null))
            {
                var value = prop.GetValue(instance);
                if (value == null)
                    throw new System.ArgumentException(
                        $"{instance.GetType().Name}.{prop.Name} is required but was not provided.");
                if (value is IList list && list.Count == 0)
                    throw new System.ArgumentException(
                        $"{instance.GetType().Name}.{prop.Name} requires at least one value.");
            }
        }

        /// <summary>Get the @id assigned to a previously-added instance.</summary>
        public string GetId(object instance)
        {
            return _idMap.TryGetValue(instance, out var id) ? id : null;
        }

        /// <summary>
        /// Return a deep copy of the JSON-LD dict for a node by compact or expanded @id.
        /// Nested lists/maps are not shared with the graph.
        /// </summary>
        public Dictionary<string, object> Get(string id)
        {
            var obj = FindObject(id);
            if (obj == null)
                return null;
            return DeepCopyDict(obj);
        }

        /// <summary>Return true if a node with this @id (compact or expanded) exists.</summary>
        public bool Contains(string id)
        {
            return FindObject(id) != null;
        }

        /// <summary>Expand a compact IRI using this graph's context.</summary>
        public string ExpandIri(string id)
        {
            return ExpandCompactIri(id, _context);
        }

        /// <summary>Create or update a JSON-LD node by @id. Returns a deep copy.</summary>
        public Dictionary<string, object> UpsertNode(
            string id,
            object types = null,
            Dictionary<string, object> properties = null)
        {
            var obj = FindObject(id);
            if (obj == null)
            {
                obj = new Dictionary<string, object> { ["@id"] = id };
                if (types != null)
                    obj["@type"] = NormalizeTypeValue(types);
                if (properties != null)
                {
                    foreach (var kv in properties)
                        ApplyProperty(obj, kv.Key, kv.Value, id, "merge_compatible");
                }
                AppendObject(obj);
                return DeepCopyDict(obj);
            }

            if (types != null)
            {
                object existingTypes = obj.TryGetValue("@type", out var typeVal) ? typeVal : null;
                obj["@type"] = NormalizeTypeValue(MergeTypes(existingTypes, types));
            }
            if (properties != null)
            {
                foreach (var kv in properties)
                    ApplyProperty(obj, kv.Key, kv.Value, id, "merge_compatible");
            }
            TrackPrefixesFor(obj);
            return DeepCopyDict(obj);
        }

        /// <summary>Add an rdf:type to an existing node (same @id).</summary>
        public void AddType(string id, string typeIri)
        {
            var obj = RequireObject(id);
            object existingTypes = obj.TryGetValue("@type", out var typeVal) ? typeVal : null;
            obj["@type"] = NormalizeTypeValue(MergeTypes(existingTypes, typeIri));
            TrackPrefixesFor(new Dictionary<string, object> { ["@type"] = typeIri });
        }

        /// <summary>Add or merge a property on an existing node (merge_compatible).</summary>
        public void AddProperty(string id, string key, object value)
        {
            var obj = RequireObject(id);
            ApplyProperty(obj, key, value, id, "merge_compatible");
            TrackPrefixesFor(new Dictionary<string, object> { [key] = value });
        }

        /// <summary>Replace a property value (replace / scalar overwrite mode).</summary>
        public void SetPropertyValue(string id, string key, object value)
        {
            var obj = RequireObject(id);
            ApplyProperty(obj, key, value, id, "replace");
            TrackPrefixesFor(new Dictionary<string, object> { [key] = value });
        }

        /// <summary>Add a direct property edge source --predicate--> target.</summary>
        public void Link(string sourceId, string predicate, string targetId)
        {
            AddProperty(sourceId, predicate, new Dictionary<string, object> { ["@id"] = targetId });
        }

        /// <summary>Create a uco-core:Relationship node with deterministic @id.</summary>
        public Dictionary<string, object> CreateRelationship(
            string sourceId,
            string targetId,
            string kind,
            bool directional = true,
            string description = null,
            string relationshipId = null)
        {
            if (!Contains(sourceId))
                throw new KeyNotFoundException($"Relationship source not in graph: {sourceId}");
            if (!Contains(targetId))
                throw new KeyNotFoundException($"Relationship target not in graph: {targetId}");
            if (string.IsNullOrEmpty(kind))
                throw new ArgumentException("kindOfRelationship is required", nameof(kind));

            var relId = relationshipId ?? DeterministicRelationshipId(sourceId, targetId, kind);
            var props = new Dictionary<string, object>
            {
                ["uco-core:source"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = sourceId },
                },
                ["uco-core:target"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = targetId },
                },
                ["uco-core:kindOfRelationship"] = kind,
                ["uco-core:isDirectional"] = TypedLiteral("xsd:boolean", directional ? "true" : "false"),
            };
            if (description != null)
                props["uco-core:description"] = description;

            return UpsertNode(relId, "uco-core:Relationship", props);
        }

        /// <summary>Return the number of objects in the graph.</summary>
        public int Count => _objects.Count;

        /// <summary>Load a JSON-LD string into this graph (transactional; named OnDuplicate policy).</summary>
        public void Load(string json, string onDuplicate = null)
        {
            var policy = NormalizeDuplicatePolicy(onDuplicate ?? OnDuplicate);
            var doc = ParseJson(json);
            var snapCtx = new Dictionary<string, string>(_context);
            var snapObjects = _objects.Select(DeepCopyDict).ToList();
            var snapIndex = new Dictionary<string, int>(_iriIndex);
            try
            {
                if (doc.TryGetValue("@context", out var ctxObj) && ctxObj is Dictionary<string, object> ctx)
                    MergeContext(ctx);
                if (doc.TryGetValue("@graph", out var graphObj) && graphObj is List<object> graphList)
                {
                    foreach (var item in graphList.OfType<Dictionary<string, object>>())
                        IngestRawNode(DeepCopyDict(item), policy);
                }
            }
            catch
            {
                _context.Clear();
                foreach (var kv in snapCtx) _context[kv.Key] = kv.Value;
                _objects.Clear();
                _objects.AddRange(snapObjects);
                _iriIndex.Clear();
                foreach (var kv in snapIndex) _iriIndex[kv.Key] = kv.Value;
                throw;
            }
        }

        /// <summary>Parse a JSON-LD string into typed objects where possible.
        /// Types are matched by scanning loaded assemblies for classes with a static ClassIri field.
        /// When <c>@type</c> is an array, the most specific unambiguous registered class is chosen.
        /// </summary>
        public static FromJsonLdResult FromJsonLd(string json)
        {
            var doc = ParseJson(json);
            var graph = new CaseGraph();

            if (doc.TryGetValue("@context", out var ctxObj) && ctxObj is Dictionary<string, object> ctx)
            {
                graph.MergeContext(ctx);
            }

            var objects = new List<object>();

            if (doc.TryGetValue("@graph", out var graphObj) && graphObj is List<object> graphList)
            {
                foreach (var item in graphList.OfType<Dictionary<string, object>>())
                {
                    graph.IngestRawNode(DeepCopyDict(item), graph.OnDuplicate);
                    var typed = TryInstantiate(item, graph._context, out var warn);
                    if (warn != null)
                        graph._deserializationWarnings.Add(warn);
                    objects.Add(typed ?? (object)item);
                }
            }

            return new FromJsonLdResult { Graph = graph, Objects = objects };
        }

        private void MergeContext(Dictionary<string, object> incoming)
        {
            foreach (var kv in incoming.Where(kv => kv.Value is string))
                MergeContextEntry(kv.Key, (string)kv.Value);
        }

        private void MergeContextEntry(string prefix, string ns)
        {
            if (_context.TryGetValue(prefix, out var existing) && existing != ns)
            {
                throw new ArgumentException(
                    $"Context prefix collision for '{prefix}': existing '{existing}' vs incoming '{ns}'");
            }
            _context[prefix] = ns;
        }

        private static string ExpandCompactIri(string value, Dictionary<string, string> context)
        {
            if (value == null) return null;
            var colonIdx = value.IndexOf(':');
            if (colonIdx > 0)
            {
                var prefix = value.Substring(0, colonIdx);
                if (context.TryGetValue(prefix, out var ns))
                    return ns + value.Substring(colonIdx + 1);
            }
            return value;
        }

        private static object TryInstantiate(Dictionary<string, object> obj, Dictionary<string, string> context, out DeserializationWarning warning)
        {
            warning = null;
            string nodeId = obj.TryGetValue("@id", out var idObj) ? idObj as string : null;
            if (!obj.TryGetValue("@type", out var typeObj) || typeObj == null)
            {
                warning = new DeserializationWarning(nodeId, "missing_type", "node has no @type");
                return null;
            }

            var typeStrings = AsTypeList(typeObj);
            if (typeStrings.Count == 0)
            {
                warning = new DeserializationWarning(nodeId, "missing_type", "empty @type");
                return null;
            }

            var matched = typeStrings
                .Select(typeStr => FindTypeByClassIri(ExpandCompactIri(typeStr, context)))
                .Where(found => found != null)
                .Distinct()
                .ToList();

            var selected = SelectMostSpecificType(matched);
            if (selected == null)
            {
                warning = matched.Count == 0
                    ? new DeserializationWarning(nodeId, "unregistered_type", "no registered class for @type")
                    : new DeserializationWarning(nodeId, "ambiguous_type", "multiple incomparable types matched");
                return null;
            }

            try
            {
                var instance = Activator.CreateInstance(selected);
                SetPropertiesFromJsonLd(instance, obj, context);
                return instance;
            }
            catch (Exception ex) when (ex is MemberAccessException || ex is TargetInvocationException || ex is ArgumentException)
            {
                warning = new DeserializationWarning(nodeId, "constructor_failed", ex.Message);
                return null;
            }
        }

        private static Type FindTypeByClassIri(string expandedIri)
        {
            EnsureClassRegistryCache();
            if (_classRegistryCache.TryGetValue(expandedIri, out var type))
            {
                Interlocked.Increment(ref _classRegistryHits);
                return type;
            }
            Interlocked.Increment(ref _classRegistryMisses);
            return null;
        }

        private static void EnsureClassRegistryCache()
        {
            if (_classRegistryCache != null)
                return;
            lock (RegistryLock)
            {
                if (_classRegistryCache != null)
                    return;
                _classRegistryCache = BuildClassRegistryCache();
            }
        }

        private static Dictionary<string, Type> BuildClassRegistryCache()
        {
            var registry = new Dictionary<string, Type>(StringComparer.Ordinal);
            AddAssemblyTypes(registry, typeof(CaseGraph).Assembly);
            foreach (var registration in ExtensionTypes.Values.ToList())
            {
                foreach (var weakType in registration.Types)
                {
                    if (weakType.TryGetTarget(out var extensionType))
                        AddRegistryType(registry, extensionType);
                }
            }
            return registry;
        }

        private static void AddAssemblyTypes(Dictionary<string, Type> registry, Assembly assembly)
        {
            Type[] types;
            try { types = assembly.GetTypes(); }
            catch (ReflectionTypeLoadException ex) { types = ex.Types.Where(t => t != null).ToArray(); }

            foreach (var type in types.Where(t => t.IsClass && !t.IsAbstract))
            {
                AddRegistryType(registry, type);
            }
        }

        private static void AddRegistryType(Dictionary<string, Type> registry, Type type)
        {
            if (type == null || !type.IsClass || type.IsAbstract)
                return;
            var field = type.GetField("ClassIri", BindingFlags.Public | BindingFlags.Static);
            if (field == null || field.FieldType != typeof(string))
                return;
            var iri = (string)field.GetValue(null);
            if (string.IsNullOrWhiteSpace(iri))
                return;
            if (registry.TryGetValue(iri, out var existing) && existing != type)
                throw new ClassRegistryConflictException(iri, existing, type);
            registry[iri] = type;
        }

        /// <summary>
        /// Explicitly trust an extension assembly for typed deserialization (#82).
        /// Registration is atomic, uses weak assembly references, rejects duplicate
        /// ClassIri values, and invalidates the current cache generation.
        /// </summary>
        public static long RegisterExtensionAssembly(Assembly assembly, string source, int priority = 0)
        {
            if (assembly == null) throw new ArgumentNullException(nameof(assembly));
            Type[] types;
            try { types = assembly.GetTypes(); }
            catch (ReflectionTypeLoadException ex) { types = ex.Types.Where(t => t != null).ToArray(); }
            return RegisterExtensionTypes(types, source, priority);
        }

        /// <summary>
        /// Register an explicit trusted set of extension types (#82). Weak type
        /// references avoid pinning collectible extension assemblies.
        /// </summary>
        public static long RegisterExtensionTypes(IEnumerable<Type> types, string source, int priority = 0)
        {
            if (types == null) throw new ArgumentNullException(nameof(types));
            if (string.IsNullOrWhiteSpace(source))
                throw new ArgumentException("Extension source must be non-empty", nameof(source));
            var selected = types.Where(t => t != null).Distinct().ToList();
            if (selected.Count == 0)
                throw new ArgumentException("At least one extension type is required", nameof(types));
            lock (RegistryLock)
            {
                var hadPrior = ExtensionTypes.TryGetValue(source, out var prior);
                ExtensionTypes[source] = new ExtensionTypeRegistration(selected, priority);
                try
                {
                    var candidate = BuildClassRegistryCache();
                    _classRegistryCache = candidate;
                    _propertyBindingCache = null;
                    return ++_classRegistryGeneration;
                }
                catch
                {
                    if (hadPrior) ExtensionTypes[source] = prior;
                    else ExtensionTypes.Remove(source);
                    _classRegistryCache = null;
                    throw;
                }
            }
        }

        /// <summary>Remove one extension source and invalidate the registry (#82).</summary>
        public static long UnregisterExtensionAssembly(string source)
        {
            lock (RegistryLock)
            {
                if (!ExtensionTypes.Remove(source))
                    return _classRegistryGeneration;
                _classRegistryCache = null;
                _propertyBindingCache = null;
                return ++_classRegistryGeneration;
            }
        }

        /// <summary>Current cache generation and hit/miss counters (#82).</summary>
        public static ClassRegistryCacheMetrics GetClassRegistryCacheMetrics()
        {
            lock (RegistryLock)
            {
                return new ClassRegistryCacheMetrics(
                    Interlocked.Read(ref _classRegistryHits),
                    Interlocked.Read(ref _classRegistryMisses),
                    _classRegistryGeneration,
                    ExtensionTypes.Count,
                    _classRegistryCache?.Count ?? 0);
            }
        }

        /// <summary>Invalidate the process-wide deserialization class registry (#70).</summary>
        public static void ClearClassRegistryCache()
        {
            lock (RegistryLock)
            {
                _classRegistryCache = null;
                _propertyBindingCache = null;
                _classRegistryGeneration++;
            }
        }

        private sealed class ExtensionTypeRegistration
        {
            public List<WeakReference<Type>> Types { get; }
            public int Priority { get; }
            public ExtensionTypeRegistration(IEnumerable<Type> types, int priority)
            {
                Types = types.Select(t => new WeakReference<Type>(t)).ToList();
                Priority = priority;
            }
        }

        private static Type SelectMostSpecificType(List<Type> types)
        {
            if (types == null || types.Count == 0)
                return null;
            if (types.Count == 1)
                return types[0];
            var specific = types.Where(c => !types.Any(o => o != c && o.IsSubclassOf(c))).ToList();
            return specific.Count == 1 ? specific[0] : null;
        }

        /// <summary>Cached property → JSON-LD key bindings for typed deserialization (#70).</summary>
        private sealed class PropertyBinding
        {
            public PropertyInfo Property { get; }
            public string AttrKey { get; }
            public string InferredKey { get; }

            public PropertyBinding(PropertyInfo property, string attrKey, string inferredKey)
            {
                Property = property;
                AttrKey = attrKey;
                InferredKey = inferredKey;
            }
        }

        private static PropertyBinding[] GetPropertyBindings(Type type)
        {
            lock (RegistryLock)
            {
                if (_propertyBindingCache == null)
                    _propertyBindingCache = new Dictionary<Type, PropertyBinding[]>();
                if (_propertyBindingCache.TryGetValue(type, out var cached))
                    return cached;

                var bindings = new List<PropertyBinding>();
                foreach (var prop in type.GetProperties(BindingFlags.Public | BindingFlags.Instance)
                    .Where(p => p.CanWrite))
                {
                    var attr = prop.GetCustomAttribute<JsonLdPropertyAttribute>(inherit: true);
                    var nsField = (prop.DeclaringType ?? type).GetField("NamespacePrefix");
                    var ns = nsField != null ? (string)nsField.GetValue(null) : "uco-core";
                    var camelName = char.ToLower(prop.Name[0]) + prop.Name.Substring(1);
                    var inferred = ns + ":" + camelName;
                    bindings.Add(new PropertyBinding(prop, attr?.Key, inferred));
                }
                var arr = bindings.ToArray();
                _propertyBindingCache[type] = arr;
                return arr;
            }
        }

        /// <summary>Expose property-binding cache size for warm-path unit tests (#70).</summary>
        public static int PropertyBindingCacheCount
        {
            get
            {
                lock (RegistryLock)
                {
                    return _propertyBindingCache == null ? 0 : _propertyBindingCache.Count;
                }
            }
        }

        private static void SetPropertiesFromJsonLd(object instance, Dictionary<string, object> obj, Dictionary<string, string> context)
        {
            var type = instance.GetType();
            foreach (var binding in GetPropertyBindings(type))
            {
                string matchKey = null;
                if (binding.AttrKey != null && obj.ContainsKey(binding.AttrKey))
                    matchKey = binding.AttrKey;
                else if (obj.ContainsKey(binding.InferredKey))
                    matchKey = binding.InferredKey;

                if (matchKey == null) continue;

                try { binding.Property.SetValue(instance, ConvertToClrType(obj[matchKey], binding.Property.PropertyType)); }
                catch (ArgumentException) { /* skip: property type mismatch during deserialization */ }
                catch (TargetException) { /* skip: target object mismatch */ }
                catch (TargetInvocationException) { /* skip: setter threw */ }
            }
        }

        private static object ConvertToClrType(object value, Type target)
        {
            if (value == null) return null;

            if (value is Dictionary<string, object> dict && dict.TryGetValue("@value", out var raw))
            {
                if (raw is string rawStr)
                {
                    if (target == typeof(string)) return rawStr;
                    if (target == typeof(int)) return int.Parse(rawStr, CultureInfo.InvariantCulture);
                    if (target == typeof(long)) return long.Parse(rawStr, CultureInfo.InvariantCulture);
                    if (target == typeof(double)) return double.Parse(rawStr, CultureInfo.InvariantCulture);
                    if (target == typeof(bool)) return rawStr == "true";
                    if (target == typeof(DateTime)) return DateTime.Parse(rawStr, CultureInfo.InvariantCulture);
                }
                return raw;
            }

            if (target == typeof(string) && value is string s) return s;
            if (target == typeof(long) && value is long l) return l;
            if (target == typeof(int) && value is long li) return (int)li;
            if (target == typeof(double) && value is double d) return d;
            if (target == typeof(bool) && value is bool b) return b;

            return value;
        }

        /// <summary>Serialize the graph to a JSON-LD string.</summary>
        public string Serialize(bool indented = true)
        {
            var doc = new Dictionary<string, object>
            {
                ["@context"] = PrunedContext(),
                ["@graph"] = _objects,
            };
            return ToJsonString(doc, indented ? 0 : -1);
        }

        private Dictionary<string, string> PrunedContext()
        {
            var used = _usedPrefixSet.Count > 0
                ? new HashSet<string>(_usedPrefixSet)
                : UsedPrefixes();
            if (used.Count == 0)
                used = UsedPrefixes();
            return _context
                .Where(kv => used.Contains(kv.Key))
                .ToDictionary(kv => kv.Key, kv => kv.Value);
        }

        private void TrackPrefixesFor(object node)
        {
            CollectPrefixes(node, new HashSet<string>(_context.Keys), _usedPrefixSet);
        }

        private HashSet<string> UsedPrefixes()
        {
            var prefixes = new HashSet<string>();
            var contextKeys = new HashSet<string>(_context.Keys);
            foreach (var obj in _objects)
                CollectPrefixes(obj, contextKeys, prefixes);
            return prefixes;
        }

        private static string ExtractPrefix(string value, HashSet<string> contextKeys)
        {
            if (value.Contains("://")) return null;
            var colon = value.IndexOf(':');
            if (colon > 0)
            {
                var prefix = value.Substring(0, colon);
                if (contextKeys.Contains(prefix)) return prefix;
            }
            return null;
        }

        private static void CollectPrefixes(object node, HashSet<string> contextKeys, HashSet<string> output)
        {
            if (node is Dictionary<string, object> dict)
            {
                foreach (var kv in dict)
                {
                    var p = ExtractPrefix(kv.Key, contextKeys);
                    if (p != null) output.Add(p);
                    if (kv.Value is string strVal)
                    {
                        p = ExtractPrefix(strVal, contextKeys);
                        if (p != null) output.Add(p);
                    }
                    else
                    {
                        CollectPrefixes(kv.Value, contextKeys, output);
                    }
                }
            }
            else if (node is List<object> list)
            {
                foreach (var item in list)
                {
                    if (item is string strItem)
                    {
                        var p = ExtractPrefix(strItem, contextKeys);
                        if (p != null) output.Add(p);
                    }
                    else
                    {
                        CollectPrefixes(item, contextKeys, output);
                    }
                }
            }
        }

        /// <summary>Write the graph to a file.</summary>
        public void Write(string path)
        {
            System.IO.File.WriteAllText(path, Serialize());
        }

        /// <summary>
        /// Stream JSON-LD to disk without building a second full document string (#71).
        /// Emits @context then each @graph element incrementally with deterministic ordering.
        /// Writes via a temp file then rename when <paramref name="atomic"/> is true (default).
        /// </summary>
        /// <returns>Nodes written and UTF-8 bytes emitted.</returns>
        public StreamingWriteResult WriteStreaming(string path, int indent = 2, bool atomic = true)
        {
            var ctx = PrunedContext();
            var sortedContext = ctx.OrderBy(kv => kv.Key, StringComparer.Ordinal)
                .ToDictionary(kv => kv.Key, kv => kv.Value);

            string outPath = path;
            string tmpPath = null;
            if (atomic)
            {
                var dir = Path.GetDirectoryName(Path.GetFullPath(path));
                if (string.IsNullOrEmpty(dir))
                    dir = ".";
                Directory.CreateDirectory(dir);
                tmpPath = CombinePath(dir, $".casegraph-{Guid.NewGuid():N}.jsonld.tmp");
                outPath = tmpPath;
            }

            long bytesWritten = 0;
            try
            {
                using (var fileStream = new FileStream(outPath, FileMode.Create, FileAccess.Write, FileShare.None))
                using (var counting = new CountingStream(fileStream))
                using (var writer = new StreamWriter(counting, new UTF8Encoding(encoderShouldEmitUTF8Identifier: false)))
                {
                    if (indent < 0)
                    {
                        writer.Write("{\"@context\":");
                        writer.Write(ToJsonString(sortedContext, -1));
                        writer.Write(",\"@graph\":[");
                        for (var i = 0; i < _objects.Count; i++)
                        {
                            if (i > 0)
                                writer.Write(",");
                            writer.Write(ToJsonString(_objects[i], -1));
                        }
                        writer.Write("]}");
                    }
                    else
                    {
                        var pad = new string(' ', indent);
                        var grandChildPad = new string(' ', indent * 3);
                        writer.Write("{\n");
                        writer.Write(pad);
                        writer.Write("\"@context\": ");
                        writer.Write(ToJsonString(sortedContext, indent));
                        writer.Write(",\n");
                        writer.Write(pad);
                        writer.Write("\"@graph\": [\n");
                        for (var i = 0; i < _objects.Count; i++)
                        {
                            foreach (var line in ToJsonString(_objects[i], indent).Split('\n'))
                            {
                                writer.Write(grandChildPad);
                                writer.Write(line);
                                writer.Write("\n");
                            }
                            if (i + 1 < _objects.Count)
                                writer.Write(new string(' ', indent * 2));
                            writer.Write(i + 1 < _objects.Count ? ",\n" : "");
                        }
                        writer.Write(pad);
                        writer.Write("]\n");
                        writer.Write("}\n");
                    }
                    writer.Flush();
                    fileStream.Flush(true);
                    bytesWritten = counting.BytesWritten;
                }

                if (atomic && tmpPath != null)
                {
                    // Prefer atomic replace so a failed swap keeps the destination.
                    // Do NOT delete the destination before a successful replacement.
                    // netstandard2.0 has no File.Move(src, dest, overwrite: true).
                    var induced = SimulateReplaceFailureForTests;
                    if (induced != null)
                    {
                        var failure = induced(tmpPath, path);
                        if (failure != null)
                            throw failure;
                    }
                    try
                    {
                        if (File.Exists(path))
                        {
                            File.Replace(
                                tmpPath,
                                path,
                                destinationBackupFileName: null,
                                ignoreMetadataErrors: true);
                        }
                        else
                        {
                            File.Move(tmpPath, path);
                        }
                    }
                    catch (PlatformNotSupportedException)
                    {
                        // Documented safe fallback for hosts without File.Replace:
                        // Move only when the destination is absent. Never
                        // Delete-then-Move (old bytes must survive replace failure).
                        if (File.Exists(path))
                            throw;
                        File.Move(tmpPath, path);
                    }
                    tmpPath = null;
                }
                return new StreamingWriteResult(_objects.Count, bytesWritten);
            }
            catch
            {
                if (tmpPath != null && File.Exists(tmpPath))
                    File.Delete(tmpPath);
                throw;
            }
        }

        private sealed class CountingStream : Stream
        {
            private readonly Stream _inner;
            public long BytesWritten { get; private set; }

            public CountingStream(Stream inner) { _inner = inner; }
            public override bool CanRead => false;
            public override bool CanSeek => false;
            public override bool CanWrite => true;
            public override long Length => _inner.Length;
            public override long Position
            {
                get => _inner.Position;
                set => throw new NotSupportedException();
            }
            public override void Flush() => _inner.Flush();
            public override int Read(byte[] buffer, int offset, int count) => throw new NotSupportedException();
            public override long Seek(long offset, SeekOrigin origin) => throw new NotSupportedException();
            public override void SetLength(long value) => throw new NotSupportedException();
            public override void Write(byte[] buffer, int offset, int count)
            {
                _inner.Write(buffer, offset, count);
                BytesWritten += count;
            }
#if NETSTANDARD2_0
#else
            public override void Write(ReadOnlySpan<byte> buffer)
            {
                _inner.Write(buffer);
                BytesWritten += buffer.Length;
            }
#endif
            protected override void Dispose(bool disposing)
            {
                // Do not dispose inner; caller owns FileStream lifetime.
                base.Dispose(disposing);
            }
        }

        /// <summary>Validate this graph against CASE/UCO SHACL constraints using case_validate.
        /// Requires case-utils (pip install case-utils) to be installed and case_validate on PATH.</summary>
        /// <param name="caseVersion">The CASE built-version to validate against (default "case-1.4.0").</param>
        /// <returns>The validation output on success.</returns>
        /// <exception cref="InvalidOperationException">Thrown if validation fails or case_validate is not found.</exception>
        public string ValidateGraph(string caseVersion = "case-1.4.0")
        {
            var tmpPath = System.IO.Path.GetTempFileName() + ".jsonld";
            try
            {
                System.IO.File.WriteAllText(tmpPath, Serialize());
                var psi = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = "case_validate",
                    Arguments = $"--built-version {caseVersion} \"{tmpPath}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                };
                System.Diagnostics.Process process;
                try
                {
                    process = System.Diagnostics.Process.Start(psi);
                }
                catch (System.ComponentModel.Win32Exception)
                {
                    throw new InvalidOperationException(
                        "case_validate not found on PATH. Install with: pip install case-utils");
                }
                var stdout = process.StandardOutput.ReadToEnd();
                var stderr = process.StandardError.ReadToEnd();
                process.WaitForExit();
                if (process.ExitCode != 0)
                {
                    var msg = string.IsNullOrWhiteSpace(stderr) ? stdout : stderr;
                    throw new InvalidOperationException($"Validation failed:\n{msg.Trim()}");
                }
                return stdout;
            }
            finally
            {
                if (System.IO.File.Exists(tmpPath))
                    System.IO.File.Delete(tmpPath);
            }
        }

        /// <summary>Estimate the number of RDF triples this graph will produce.</summary>
        public int EstimateTriples()
        {
            int total = 0;
            foreach (var obj in _objects)
                total += CountTriples(obj);
            return total;
        }

        private static int CountTriples(Dictionary<string, object> obj)
        {
            int count = 0;
            foreach (var kv in obj.Where(kv => kv.Key != "@id"))
            {
                if (kv.Key == "@type")
                {
                    if (kv.Value is IList typeList) count += typeList.Count;
                    else count++;
                    continue;
                }
                if (kv.Value is List<object> list)
                {
                    foreach (var item in list)
                    {
                        if (item is Dictionary<string, object> nested)
                            count += 1 + CountTriples(nested);
                        else
                            count++;
                    }
                }
                else if (kv.Value is Dictionary<string, object> dict)
                {
                    if (dict.ContainsKey("@value"))
                        count++;
                    else
                        count += 1 + CountTriples(dict);
                }
                else
                {
                    count++;
                }
            }
            return count;
        }

        /// <summary>
        /// Split the graph into smaller chunks of at most maxObjects each.
        /// Catalog-style graphs only: object-count splits can break investigative
        /// relationships. Prefer <see cref="PartitionByRoots"/> or
        /// <see cref="PartitionByLabel"/> for CASE investigation graphs.
        /// </summary>
        public List<CaseGraph> Split(int maxObjects = 10000)
        {
            if (maxObjects <= 0)
                throw new ArgumentOutOfRangeException(nameof(maxObjects), maxObjects, "split maxObjects must be a positive integer");
            var chunks = new List<CaseGraph>();
            for (int i = 0; i < _objects.Count; i += maxObjects)
            {
                var chunk = new CaseGraph(_context["kb"]);
                foreach (var kv in _context)
                    chunk._context[kv.Key] = kv.Value;
                int end = Math.Min(i + maxObjects, _objects.Count);
                for (int j = i; j < end; j++)
                    chunk.AppendObject(DeepCopyDict(_objects[j]));
                chunks.Add(chunk);
            }
            return chunks;
        }

        /// <summary>
        /// Experimental root closure (#72). Follows nested <c>{"@id": ...}</c>
        /// references reachable from each root (outgoing). When
        /// <paramref name="includeIncoming"/> is true (default), also follows
        /// reverse references from other top-level objects (e.g. Relationships
        /// pointing at the root). Nodes reachable from multiple roots are
        /// replicated into each partition when
        /// <paramref name="sharedNodePolicy"/> is <c>replicate-identical</c>,
        /// or placed in a <c>_shared</c> partition when <c>shared</c>.
        /// </summary>
        public Dictionary<string, CaseGraph> PartitionByRoots(
            IEnumerable<string> rootIris,
            string sharedNodePolicy = "replicate-identical",
            bool includeIncoming = true)
        {
            return PartitionByRootsWithManifest(rootIris, new PartitionOptions
            {
                SharedNodePolicy = sharedNodePolicy,
                IncludeIncoming = includeIncoming,
            }).Partitions;
        }

        /// <summary>
        /// Marking-safe root partitioning with a reconstruction/validation manifest (#79).
        /// </summary>
        public PartitionResult PartitionByRootsWithManifest(
            IEnumerable<string> rootIris,
            PartitionOptions options = null)
        {
            if (rootIris == null)
                throw new ArgumentNullException(nameof(rootIris));
            options = options ?? new PartitionOptions();
            var requestedPolicy = options.SharedNodePolicy ?? "replicate-identical";
            var sharedPolicy = NormalizeSharedNodePolicy(requestedPolicy);
            if (options.BoundaryPolicy != "none"
                && options.BoundaryPolicy != "marking-and-authorization")
                throw new ArgumentException("Unknown boundary policy", nameof(options));
            if (options.CrossBoundaryPolicy != "error-on-cross-boundary"
                && options.CrossBoundaryPolicy != "home-partition-reference")
                throw new ArgumentException("Unknown cross-boundary policy", nameof(options));
            if (options.ManifestDetail != "full" && options.ManifestDetail != "safe")
                throw new ArgumentException("ManifestDetail must be 'full' or 'safe'", nameof(options));

            var byId = BuildNodeIndex();
            var reverseIndex = BuildReverseIdIndex(byId);
            var rootEntries = new List<(string Key, string Expanded)>();
            foreach (var root in rootIris.Where(r => !string.IsNullOrEmpty(r)))
            {
                var expanded = ExpandIri(root);
                if (!rootEntries.Any(entry => entry.Expanded == expanded))
                    rootEntries.Add((root, expanded));
            }
            if (rootEntries.Count == 0)
                throw new ArgumentException("rootIris must contain at least one root", nameof(rootIris));

            var closures = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
            foreach (var entry in rootEntries.Where(e => byId.ContainsKey(e.Expanded)))
                closures[entry.Expanded] = CollectReachable(
                    entry.Expanded, byId, reverseIndex, options.IncludeIncoming);

            var boundaries = byId.ToDictionary(
                pair => pair.Key,
                pair => ExtractPartitionBoundary(pair.Value),
                StringComparer.Ordinal);
            var declared = new Dictionary<string, PartitionBoundarySets>(StringComparer.Ordinal);
            var omissions = closures.Keys.ToDictionary(
                root => root,
                _ => new HashSet<string>(StringComparer.Ordinal),
                StringComparer.Ordinal);
            if (options.BoundaryPolicy == "marking-and-authorization")
            {
                foreach (var entry in rootEntries.Where(e => closures.ContainsKey(e.Expanded)))
                {
                    PartitionBoundary supplied = null;
                    options.RootBoundaries?.TryGetValue(entry.Key, out supplied);
                    declared[entry.Expanded] = supplied == null
                        ? boundaries[entry.Expanded]
                        : new PartitionBoundarySets(
                            new HashSet<string>((supplied.Markings ?? Array.Empty<string>()).Select(ExpandIri), StringComparer.Ordinal),
                            new HashSet<string>((supplied.Authorizations ?? Array.Empty<string>()).Select(ExpandIri), StringComparer.Ordinal));
                }
                foreach (var entry in closures)
                {
                    var allowed = declared[entry.Key];
                    foreach (var nodeId in entry.Value.ToList())
                    {
                        var required = boundaries[nodeId];
                        var missingMarkings = required.Markings.Except(allowed.Markings).OrderBy(x => x).ToList();
                        var missingAuthorizations = required.Authorizations.Except(allowed.Authorizations).OrderBy(x => x).ToList();
                        if (missingMarkings.Count == 0 && missingAuthorizations.Count == 0)
                            continue;
                        if (nodeId == entry.Key || options.CrossBoundaryPolicy == "error-on-cross-boundary")
                            throw new PartitionBoundaryException(
                                RootKeyForExpanded(rootEntries, entry.Key),
                                OriginalId(byId[nodeId], nodeId),
                                missingMarkings,
                                missingAuthorizations);
                        entry.Value.Remove(nodeId);
                        omissions[entry.Key].Add(nodeId);
                    }
                }
            }

            var boundaryHomes = new Dictionary<string, string>(StringComparer.Ordinal);
            foreach (var nodeId in omissions.Values.SelectMany(ids => ids).Distinct().OrderBy(x => x))
            {
                var candidates = closures
                    .Where(entry => entry.Value.Contains(nodeId))
                    .Select(entry => entry.Key)
                    .OrderBy(x => x)
                    .ToList();
                if (candidates.Count == 0)
                    throw new PartitionBoundaryException(
                        "<no-authorized-home>", OriginalId(byId[nodeId], nodeId),
                        boundaries[nodeId].Markings.OrderBy(x => x).ToList(),
                        boundaries[nodeId].Authorizations.OrderBy(x => x).ToList());
                boundaryHomes[nodeId] = candidates[0];
            }

            var nodeOwners = new Dictionary<string, List<string>>(StringComparer.Ordinal);
            foreach (var entry in closures)
                foreach (var nodeId in entry.Value)
                {
                    if (!nodeOwners.TryGetValue(nodeId, out var owners))
                        nodeOwners[nodeId] = owners = new List<string>();
                    owners.Add(entry.Key);
                }
            if (sharedPolicy == "error-on-cross-boundary")
            {
                var overlap = nodeOwners.Where(pair => pair.Value.Count > 1).Select(pair => pair.Key).OrderBy(x => x).ToList();
                if (overlap.Count > 0)
                    throw new InvalidOperationException(
                        $"shared nodes cross partition boundaries: {string.Join(", ", overlap.Take(5))}");
            }

            var homeByNode = new Dictionary<string, string>(StringComparer.Ordinal);
            if (sharedPolicy == "home-partition-reference")
                foreach (var entry in nodeOwners.Where(pair => pair.Value.Count > 1))
                    homeByNode[entry.Key] = entry.Value.Contains(entry.Key)
                        ? entry.Key
                        : entry.Value.OrderBy(x => x).First();

            var partitions = new Dictionary<string, CaseGraph>(StringComparer.Ordinal);
            foreach (var entry in rootEntries.Where(e => closures.ContainsKey(e.Expanded)))
            {
                var part = CreatePartitionShell();
                foreach (var nodeId in closures[entry.Expanded])
                {
                    var ownerCount = nodeOwners[nodeId].Count;
                    if (ownerCount > 1 && sharedPolicy == "support-graph")
                        continue;
                    if (ownerCount > 1 && sharedPolicy == "home-partition-reference"
                        && homeByNode[nodeId] != entry.Expanded)
                        continue;
                    IngestIntoPartition(part, byId[nodeId]);
                }
                partitions[entry.Key] = part;
            }
            if (sharedPolicy == "support-graph")
            {
                var support = CreatePartitionShell();
                foreach (var entry in nodeOwners.Where(pair => pair.Value.Count > 1))
                    IngestIntoPartition(support, byId[entry.Key]);
                if (support._objects.Count > 0)
                    partitions[requestedPolicy == "support-graph" ? "_support" : "_shared"] = support;
            }

            var sourceHash = GraphFingerprint(_objects);
            var partitionManifest = new Dictionary<string, object>(StringComparer.Ordinal);
            foreach (var entry in partitions)
            {
                var partHash = GraphFingerprint(entry.Value._objects);
                var detail = new Dictionary<string, object>(StringComparer.Ordinal)
                {
                    ["partition_id"] = $"urn:sha256:{partHash}",
                    ["node_count"] = entry.Value._objects.Count,
                    ["triple_estimate"] = entry.Value.EstimateTriples(),
                    ["sha256"] = partHash,
                    ["effective_markings"] = entry.Key.StartsWith("_", StringComparison.Ordinal)
                        ? new List<string>()
                        : declared.TryGetValue(ExpandIri(entry.Key), out var scope)
                            ? scope.Markings.OrderBy(x => x).ToList()
                            : new List<string>(),
                    ["authorization_scope"] = entry.Key.StartsWith("_", StringComparison.Ordinal)
                        ? new List<string>()
                        : declared.TryGetValue(ExpandIri(entry.Key), out var authScope)
                            ? authScope.Authorizations.OrderBy(x => x).ToList()
                            : new List<string>(),
                };
                if (options.ManifestDetail == "full")
                    detail["node_ids"] = entry.Value._objects
                        .Select(node => OriginalId(node, null))
                        .Where(id => id != null).OrderBy(id => id).ToList();
                partitionManifest[entry.Key] = detail;
            }
            var routes = homeByNode.Concat(boundaryHomes)
                .GroupBy(pair => pair.Key).ToDictionary(
                    group => OriginalId(byId[group.Key], group.Key),
                    group => RootKeyForExpanded(rootEntries, group.Last().Value),
                    StringComparer.Ordinal);
            var referenced = sharedPolicy == "support-graph"
                || sharedPolicy == "home-partition-reference"
                || omissions.Values.Any(ids => ids.Count > 0);
            var manifest = new Dictionary<string, object>(StringComparer.Ordinal)
            {
                ["schema_version"] = "2.0.0",
                ["dataset_id"] = $"urn:sha256:{sourceHash}",
                ["source_graph_sha256"] = sourceHash,
                ["strategy"] = options.IncludeIncoming ? "outgoing_and_incoming_id_closure" : "outgoing_id_closure",
                ["roots"] = rootEntries.Select(entry => entry.Key).ToList(),
                ["shared_node_policy"] = sharedPolicy,
                ["include_incoming"] = options.IncludeIncoming,
                ["boundary_policy"] = options.BoundaryPolicy,
                ["cross_boundary_policy"] = options.CrossBoundaryPolicy,
                ["validation_mode"] = referenced ? "referenced-partition-set" : "self-contained",
                ["validation_bundle"] = options.ValidationBundle,
                ["partitions"] = partitionManifest,
                ["home_partition_routes"] = options.ManifestDetail == "full" ? routes : new Dictionary<string, string>(),
                ["home_partition_route_count"] = routes.Count,
                ["boundary_omission_counts"] = omissions.ToDictionary(
                    entry => RootKeyForExpanded(rootEntries, entry.Key), entry => (object)entry.Value.Count),
                ["reconstruction"] = new Dictionary<string, object>
                {
                    ["operation"] = "rdf-union",
                    ["deduplicate_by"] = "@id with identical assertions",
                    ["requires_partitions"] = partitions.Keys.OrderBy(x => x).ToList(),
                },
            };
            return new PartitionResult(partitions, manifest);
        }

        /// <summary>Verify that the exact JSON-LD node union reconstructs this graph.</summary>
        public PartitionUnionVerification VerifyPartitionUnion(IDictionary<string, CaseGraph> partitions)
        {
            if (partitions == null)
                throw new ArgumentNullException(nameof(partitions));
            var source = _objects.ToDictionary(
                node => ExpandIri(OriginalId(node, "")),
                node => ToJsonString(node, -1),
                StringComparer.Ordinal);
            var union = new Dictionary<string, string>(StringComparer.Ordinal);
            var conflict = false;
            foreach (var partition in partitions.Values)
                foreach (var node in partition._objects)
                {
                    var id = ExpandIri(OriginalId(node, ""));
                    var value = ToJsonString(node, -1);
                    if (union.TryGetValue(id, out var existing) && existing != value)
                        conflict = true;
                    else
                        union[id] = value;
                }
            return new PartitionUnionVerification
            {
                Equivalent = !conflict && source.Count == union.Count
                    && source.All(pair => union.TryGetValue(pair.Key, out var value) && value == pair.Value),
                SourceNodes = source.Count,
                UnionNodes = union.Count,
            };
        }

        /// <summary>
        /// Experimental label partitioning by a caller-supplied boundary key.
        /// Not dependency-aware; prefer <see cref="PartitionByRoots"/> when closure matters.
        /// </summary>
        public Dictionary<string, CaseGraph> PartitionByLabel(Func<Dictionary<string, object>, string> boundaryKey)
        {
            return PartitionByLabel(boundaryKey, null, true);
        }

        /// <summary>
        /// Experimental label partitioning by a caller-supplied boundary key (#72).
        /// </summary>
        public Dictionary<string, CaseGraph> PartitionByLabel(
            Func<Dictionary<string, object>, string> boundaryKey,
            HashSet<string> sharedIds,
            bool includeDanglingRelationships = true)
        {
            if (boundaryKey == null)
                throw new ArgumentNullException(nameof(boundaryKey));
            sharedIds = sharedIds ?? new HashSet<string>();

            var partitions = new Dictionary<string, CaseGraph>(StringComparer.Ordinal);
            var membership = new Dictionary<string, string>(StringComparer.Ordinal);

            foreach (var obj in _objects.Where(
                o => o.TryGetValue("@id", out var idObj) && idObj is string))
            {
                var nodeId = (string)obj["@id"];
                var key = boundaryKey(obj);
                if (key == null)
                    continue;
                membership[nodeId] = key;
                if (!partitions.ContainsKey(key))
                    partitions[key] = CreatePartitionShell();
                IngestIntoPartition(partitions[key], obj);
            }

            var byId = BuildNodeIndex();
            foreach (var obj in _objects.Where(IsRelationshipNode))
            {
                var sourceId = FirstEndpointId(obj, "uco-core:source");
                var targetId = FirstEndpointId(obj, "uco-core:target");
                if (sourceId == null || targetId == null)
                    continue;
                membership.TryGetValue(sourceId, out var sourcePart);
                membership.TryGetValue(targetId, out var targetPart);
                if (sourcePart != null && targetPart != null && sourcePart == targetPart)
                    continue;
                if (!includeDanglingRelationships && sourcePart != targetPart)
                    continue;

                var partNames = new HashSet<string>();
                if (sourcePart != null) partNames.Add(sourcePart);
                if (targetPart != null) partNames.Add(targetPart);
                foreach (var partName in partNames)
                {
                    if (!partitions.ContainsKey(partName))
                        partitions[partName] = CreatePartitionShell();
                    foreach (var endpoint in new[] { sourceId, targetId }
                        .Where(id => id != null)
                        .Select(ExpandIri)
                        .Where(expanded => byId.ContainsKey(expanded))
                        .Select(expanded => byId[expanded]))
                    {
                        IngestIntoPartition(partitions[partName], endpoint);
                    }
                    IngestIntoPartition(partitions[partName], obj);
                }
            }

            foreach (var sharedNode in sharedIds
                .Select(ExpandIri)
                .Where(expanded => byId.ContainsKey(expanded))
                .Select(expanded => byId[expanded]))
            {
                foreach (var partition in partitions.Values)
                    IngestIntoPartition(partition, sharedNode);
            }

            return partitions;
        }

        private CaseGraph CreatePartitionShell()
        {
            var shell = new CaseGraph(_context["kb"]);
            foreach (var kv in _context)
                shell._context[kv.Key] = kv.Value;
            shell.OnDuplicate = "merge_compatible";
            return shell;
        }

        private static string RootKeyForExpanded(List<(string Key, string Expanded)> rootEntries, string expandedRoot)
        {
            foreach (var entry in rootEntries.Where(e => e.Expanded == expandedRoot))
                return entry.Key;
            return expandedRoot;
        }

        /// <summary>
        /// Joins a directory with a relative file name. If the second argument is
        /// already rooted, returns it unchanged (never silently drops the base).
        /// Implemented without <see cref="Path.Combine"/> to avoid cs/path-combine.
        /// </summary>
        private static string CombinePath(string basePath, string relativeOrAbsolute)
        {
            if (Path.IsPathRooted(relativeOrAbsolute))
                return relativeOrAbsolute;
            if (string.IsNullOrEmpty(basePath))
                return relativeOrAbsolute;
            var last = basePath[basePath.Length - 1];
            if (last == Path.DirectorySeparatorChar || last == Path.AltDirectorySeparatorChar)
                return basePath + relativeOrAbsolute;
            return basePath + Path.DirectorySeparatorChar + relativeOrAbsolute;
        }

        private sealed class PartitionBoundarySets
        {
            public PartitionBoundarySets(HashSet<string> markings, HashSet<string> authorizations)
            {
                Markings = markings;
                Authorizations = authorizations;
            }

            public HashSet<string> Markings { get; }
            public HashSet<string> Authorizations { get; }
        }

        private PartitionBoundarySets ExtractPartitionBoundary(Dictionary<string, object> node)
        {
            var markings = new HashSet<string>(StringComparer.Ordinal);
            var authorizations = new HashSet<string>(StringComparer.Ordinal);
            foreach (var entry in node)
            {
                var expanded = ExpandIri(entry.Key);
                var slash = expanded.LastIndexOf('/');
                var hash = expanded.LastIndexOf('#');
                var local = expanded.Substring(Math.Max(slash, hash) + 1);
                if (local == "objectMarking")
                    CollectBoundaryIds(entry.Value, markings);
                else if (local == "relevantAuthorization" || local == "requiredAuthorization")
                    CollectBoundaryIds(entry.Value, authorizations);
            }
            return new PartitionBoundarySets(markings, authorizations);
        }

        private void CollectBoundaryIds(object value, HashSet<string> output)
        {
            if (value is string text)
            {
                output.Add(ExpandIri(text));
                return;
            }
            if (value is Dictionary<string, object> dictionary)
            {
                if (dictionary.TryGetValue("@id", out var id) && id is string idText)
                    output.Add(ExpandIri(idText));
                return;
            }
            if (value is IList list)
                foreach (var item in list)
                    CollectBoundaryIds(item, output);
        }

        private string GraphFingerprint(IEnumerable<Dictionary<string, object>> nodes)
        {
            var sortedContext = _context.OrderBy(pair => pair.Key).ToDictionary(
                pair => pair.Key, pair => (object)pair.Value, StringComparer.Ordinal);
            var document = new Dictionary<string, object>(StringComparer.Ordinal)
            {
                ["@context"] = sortedContext,
                ["@graph"] = nodes.Cast<object>().ToList(),
            };
            var bytes = Encoding.UTF8.GetBytes(ToJsonString(document, -1));
            using (var sha256 = SHA256.Create())
                return string.Concat(sha256.ComputeHash(bytes).Select(
                    value => value.ToString("x2", CultureInfo.InvariantCulture)));
        }

        private static string OriginalId(Dictionary<string, object> node, string fallback)
        {
            return node != null && node.TryGetValue("@id", out var id) && id is string text
                ? text
                : fallback;
        }

        private static string NormalizeSharedNodePolicy(string policy)
        {
            if (string.IsNullOrEmpty(policy) || policy == "replicate-identical")
                return "replicate-identical";
            if (policy == "shared" || policy == "isolate-shared" || policy == "_shared"
                || policy == "support-graph")
                return "support-graph";
            if (policy == "home-partition-reference" || policy == "error-on-cross-boundary")
                return policy;
            throw new ArgumentException(
                $"Unknown sharedNodePolicy: '{policy}'. Expected replicate-identical, " +
                "support-graph, home-partition-reference, or error-on-cross-boundary.",
                nameof(policy));
        }

        private Dictionary<string, Dictionary<string, object>> BuildNodeIndex()
        {
            var byId = new Dictionary<string, Dictionary<string, object>>(StringComparer.Ordinal);
            foreach (var obj in _objects.Where(
                o => o.TryGetValue("@id", out var idObj) && idObj is string))
            {
                var nodeId = (string)obj["@id"];
                var expanded = ExpandIri(nodeId);
                byId[expanded] = obj;
                if (!byId.ContainsKey(nodeId))
                    byId[nodeId] = obj;
            }
            return byId;
        }

        private Dictionary<string, HashSet<string>> BuildReverseIdIndex(
            Dictionary<string, Dictionary<string, object>> byId)
        {
            var reverse = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
            foreach (var obj in _objects.Where(
                o => o.TryGetValue("@id", out var idObj) && idObj is string))
            {
                var ownerId = (string)obj["@id"];
                var ownerExpanded = ExpandIri(ownerId);
                foreach (var expanded in CollectReferencedIds(obj)
                    .Select(ExpandIri)
                    .Where(e => e != ownerExpanded && byId.ContainsKey(e)))
                {
                    if (!reverse.TryGetValue(expanded, out var owners))
                    {
                        owners = new HashSet<string>(StringComparer.Ordinal);
                        reverse[expanded] = owners;
                    }
                    owners.Add(ownerExpanded);
                }
            }
            return reverse;
        }

        private HashSet<string> CollectReachable(
            string rootExpanded,
            Dictionary<string, Dictionary<string, object>> byId,
            Dictionary<string, HashSet<string>> reverseIndex = null,
            bool includeIncoming = true)
        {
            var visited = new HashSet<string>(StringComparer.Ordinal);
            var queue = new Queue<string>();
            queue.Enqueue(rootExpanded);

            while (queue.Count > 0)
            {
                var current = queue.Dequeue();
                if (!visited.Add(current))
                    continue;
                if (!byId.TryGetValue(current, out var node))
                    continue;

                foreach (var expanded in CollectReferencedIds(node)
                    .Select(ExpandIri)
                    .Where(e => byId.ContainsKey(e) && !visited.Contains(e)))
                {
                    queue.Enqueue(expanded);
                }

                if (includeIncoming && reverseIndex != null
                    && reverseIndex.TryGetValue(current, out var referrers))
                {
                    foreach (var referrer in referrers.Where(
                        r => byId.ContainsKey(r) && !visited.Contains(r)))
                    {
                        queue.Enqueue(referrer);
                    }
                }
            }

            return visited;
        }

        private static IEnumerable<string> CollectReferencedIds(Dictionary<string, object> node)
        {
            foreach (var refId in WalkIdReferences(node))
                yield return refId;

            if (IsRelationshipNode(node))
            {
                var sourceId = FirstEndpointId(node, "uco-core:source");
                if (sourceId != null)
                    yield return sourceId;
                var targetId = FirstEndpointId(node, "uco-core:target");
                if (targetId != null)
                    yield return targetId;
            }
        }

        private static IEnumerable<string> WalkIdReferences(object value)
        {
            if (value is Dictionary<string, object> dict)
            {
                if (dict.TryGetValue("@id", out var idObj) && idObj is string id && id.Length > 0)
                    yield return id;
                foreach (var kv in dict.Where(pair => pair.Key != "@id"))
                {
                    foreach (var nested in WalkIdReferences(kv.Value))
                        yield return nested;
                }
                yield break;
            }

            if (value is List<object> list)
            {
                foreach (var item in list)
                {
                    foreach (var nested in WalkIdReferences(item))
                        yield return nested;
                }
                yield break;
            }

            if (value is IList ilist && !(value is string))
            {
                foreach (var item in ilist)
                {
                    foreach (var nested in WalkIdReferences(item))
                        yield return nested;
                }
            }
        }

        private static bool IsRelationshipNode(Dictionary<string, object> node)
        {
            if (!node.TryGetValue("@type", out var typeObj) || typeObj == null)
                return false;
            return AsTypeList(typeObj).Any(t =>
                t == "uco-core:Relationship"
                || t == "https://ontology.unifiedcyberontology.org/uco/core/Relationship");
        }

        private static string FirstEndpointId(Dictionary<string, object> node, string key)
        {
            if (!node.TryGetValue(key, out var value) || value == null)
                return null;
            if (value is Dictionary<string, object> dict && dict.TryGetValue("@id", out var idObj) && idObj is string id)
                return id;
            if (value is List<object> list && list.Count > 0
                && list[0] is Dictionary<string, object> first
                && first.TryGetValue("@id", out var listId) && listId is string lid)
            {
                return lid;
            }
            if (value is IList ilist && ilist.Count > 0 && ilist[0] is Dictionary<string, object> iFirst
                && iFirst.TryGetValue("@id", out var iidObj) && iidObj is string iid)
            {
                return iid;
            }
            return null;
        }

        private static void IngestIntoPartition(CaseGraph partition, Dictionary<string, object> node)
        {
            try
            {
                partition.IngestRawNode(DeepCopyDict(node), "merge_compatible");
            }
            catch (InvalidOperationException)
            {
                // merge_compatible may already contain the node.
            }
        }

        /// <summary>Load and merge multiple JSON-LD files into a single graph.</summary>
        public static CaseGraph MergeFiles(IEnumerable<string> paths, string kbPrefix = "http://example.org/kb/")
        {
            var merged = new CaseGraph(kbPrefix);
            foreach (var path in paths)
            {
                merged.Load(System.IO.File.ReadAllText(path));
            }
            return merged;
        }

        private void AppendObject(Dictionary<string, object> obj)
        {
            var nodeId = obj.TryGetValue("@id", out var idObj) ? idObj as string : null;
            if (nodeId != null && FindObject(nodeId) != null)
            {
                throw new InvalidOperationException(
                    $"Duplicate @id '{nodeId}': use AddType/UpsertNode or merge-compatible Load instead of appending a second node");
            }
            _objects.Add(obj);
            if (nodeId != null)
                IndexNode(nodeId, _objects.Count - 1);
            TrackPrefixesFor(obj);
        }

        private void IndexNode(string nodeId, int index)
        {
            var expanded = ExpandIri(nodeId);
            _iriIndex[expanded] = index;
        }

        private Dictionary<string, object> FindObject(string nodeId)
        {
            var expanded = ExpandIri(nodeId);
            if (_iriIndex.TryGetValue(expanded, out var idx) && idx < _objects.Count)
                return _objects[idx];
            return null;
        }

        private Dictionary<string, object> RequireObject(string nodeId)
        {
            var obj = FindObject(nodeId);
            if (obj == null)
                throw new KeyNotFoundException($"No node with @id '{nodeId}'");
            return obj;
        }

        
        private void IngestRawNode(Dictionary<string, object> raw, string policy)
        {
            policy = NormalizeDuplicatePolicy(policy);
            if (!raw.TryGetValue("@id", out var idObj) || !(idObj is string nodeId))
            {
                _objects.Add(raw);
                TrackPrefixesFor(raw);
                return;
            }

            var existing = FindObject(nodeId);
            if (existing == null)
            {
                AppendObject(raw);
                return;
            }

            if (policy == "reject")
            {
                throw new InvalidOperationException(
                    $"Duplicate @id '{nodeId}': conflicting duplicate during load");
            }
            if (policy == "replace")
            {
                var preserved = existing.TryGetValue("@id", out var pid) ? pid : nodeId;
                existing.Clear();
                foreach (var kv in raw)
                    existing[kv.Key] = DeepCopyValue(kv.Value);
                existing["@id"] = preserved;
                TrackPrefixesFor(existing);
                return;
            }
            if (policy == "merge_identical")
            {
                foreach (var kv in raw.Where(kv => kv.Key != "@id"))
                {
                    if (!existing.TryGetValue(kv.Key, out var existingVal))
                    {
                        existing[kv.Key] = DeepCopyValue(kv.Value);
                        continue;
                    }
                    if (!JsonLdValuesEqual(existingVal, kv.Value))
                        throw new InvalidOperationException(
                            $"Duplicate @id '{nodeId}': merge_identical conflict on '{kv.Key}'");
                }
                TrackPrefixesFor(raw);
                return;
            }
            // merge_compatible
            if (raw.TryGetValue("@type", out var rawType))
            {
                object existingTypes = existing.TryGetValue("@type", out var existingType) ? existingType : null;
                existing["@type"] = NormalizeTypeValue(MergeTypes(existingTypes, rawType));
            }
            foreach (var kv in raw.Where(kv => kv.Key != "@id" && kv.Key != "@type"))
            {
                ApplyProperty(existing, kv.Key, kv.Value, nodeId, "merge_compatible");
            }
            TrackPrefixesFor(raw);
        }

        private static string NormalizeDuplicatePolicy(string policy)
        {
            if (policy == "error") policy = "reject";
            if (policy != "reject" && policy != "merge_identical" && policy != "merge_compatible" && policy != "replace")
                throw new ArgumentException(
                    $"Unknown duplicate policy: '{policy}'. Expected one of: reject, merge_identical, merge_compatible, replace");
            return policy;
        }

        private static void ApplyProperty(Dictionary<string, object> obj, string key, object value, string nodeId, string mode)
        {
            if (mode == "replace")
            {
                obj[key] = DeepCopyValue(value);
                return;
            }
            if (!obj.TryGetValue(key, out var existing))
            {
                obj[key] = DeepCopyValue(value);
                return;
            }
            if (JsonLdValuesEqual(existing, value))
                return;
            if (existing is List<object> list)
            {
                AccumulateListValue(list, value);
                return;
            }
            if (value is List<object> || value is IList)
            {
                var merged = new List<object> { DeepCopyValue(existing) };
                AccumulateListValue(merged, value);
                obj[key] = merged;
                return;
            }
            // Distinct JSON-LD node references are multi-valued, not scalar conflicts.
            if (existing is Dictionary<string, object> ed
                && value is Dictionary<string, object> vd
                && ed.ContainsKey("@id") && vd.ContainsKey("@id"))
            {
                if (JsonLdValuesEqual(existing, value))
                    return;
                obj[key] = new List<object> { DeepCopyValue(existing), DeepCopyValue(value) };
                return;
            }
            throw new InvalidOperationException(
                $"merge_compatible scalar conflict on '{key}': existing and incoming values differ");
        }

        private static void AccumulateListValue(List<object> existing, object value)
        {
            var items = value is List<object> list ? list
                : value is IList ilist ? ilist.Cast<object>().ToList()
                : new List<object> { value };
            foreach (var item in items.Where(item => !existing.Any(x => JsonLdValuesEqual(x, item))))
            {
                existing.Add(DeepCopyValue(item));
            }
        }

        private static bool JsonLdValuesEqual(object a, object b)
        {
            if (ReferenceEquals(a, b)) return true;
            if (a is Dictionary<string, object> ad && b is Dictionary<string, object> bd)
            {
                bool hasAv = ad.TryGetValue("@value", out var av);
                bool hasBv = bd.TryGetValue("@value", out var bv);
                if (hasAv || hasBv)
                {
                    if (!(hasAv && hasBv)) return false;
                    return NormalizeLiteralType(ad.TryGetValue("@type", out var at) ? at as string : null)
                        == NormalizeLiteralType(bd.TryGetValue("@type", out var bt) ? bt as string : null)
                        && NormalizeLiteralValue(av, ad.TryGetValue("@type", out var at2) ? at2 as string : null)
                        == NormalizeLiteralValue(bv, bd.TryGetValue("@type", out var bt2) ? bt2 as string : null);
                }
                if (ad.ContainsKey("@id") || bd.ContainsKey("@id"))
                    return Equals(ad.TryGetValue("@id", out var ai) ? ai : null, bd.TryGetValue("@id", out var bi) ? bi : null);
            }
            if (a is List<object> al && b is List<object> bl)
            {
                if (IsIdRefList(al) && IsIdRefList(bl))
                {
                    var asort = al.Select(IdOf).OrderBy(x => x).ToList();
                    var bsort = bl.Select(IdOf).OrderBy(x => x).ToList();
                    return asort.SequenceEqual(bsort);
                }
                if (al.Count != bl.Count) return false;
                return al.Zip(bl, JsonLdValuesEqual).All(x => x);
            }
            return Equals(a, b);
        }

        private static string NormalizeLiteralType(string typeIri)
        {
            if (string.IsNullOrEmpty(typeIri)) return "";
            if (typeIri.StartsWith("xsd:")) return typeIri;
            if (typeIri.StartsWith("http://www.w3.org/2001/XMLSchema#"))
                return "xsd:" + typeIri.Substring(typeIri.LastIndexOf('#') + 1);
            return typeIri;
        }

        private static string NormalizeLiteralValue(object value, string typeIri)
        {
            if (value is bool b) return b ? "true" : "false";
            if (value is string s && NormalizeLiteralType(typeIri).Contains("boolean"))
                return s.ToLowerInvariant();
            return Convert.ToString(value, CultureInfo.InvariantCulture) ?? "";
        }

        private static bool IsIdRefList(List<object> items)
            => items.Count > 0 && items.All(x => x is Dictionary<string, object> d && d.ContainsKey("@id"));

        private static string IdOf(object item)
            => item is Dictionary<string, object> d && d.TryGetValue("@id", out var id) ? id?.ToString() ?? "" : item?.ToString() ?? "";

        private static Dictionary<string, object> DeepCopyDict(Dictionary<string, object> src)
        {
            var copy = new Dictionary<string, object>();
            foreach (var kv in src)
                copy[kv.Key] = DeepCopyValue(kv.Value);
            return copy;
        }

        private static object DeepCopyValue(object value)
        {
            if (value is Dictionary<string, object> dict)
                return DeepCopyDict(dict);
            if (value is List<object> list)
                return list.Select(DeepCopyValue).ToList();
            if (value is IList ilist && !(value is string))
                return ilist.Cast<object>().Select(DeepCopyValue).ToList();
            return value;
        }


        private static List<string> AsTypeList(object types)
        {
            if (types == null)
                return new List<string>();
            if (types is string s)
                return new List<string> { s };
            if (types is IEnumerable<string> seq)
                return seq.ToList();
            if (types is IEnumerable<object> objSeq)
                return objSeq.Select(o => o?.ToString()).Where(o => o != null).ToList();
            return new List<string> { types.ToString() };
        }

        private static object NormalizeTypeValue(object types)
        {
            var list = AsTypeList(types);
            if (list.Count == 1)
                return list[0];
            return list;
        }

        private static object MergeTypes(object existing, object newTypes)
        {
            var merged = AsTypeList(existing);
            merged.AddRange(AsTypeList(newTypes).Where(t => !merged.Contains(t)));
            return merged;
        }

        private static string SafeKindSlug(string kind, int maxLen = 64)
        {
            var sb = new StringBuilder();
            foreach (var ch in (kind ?? "").Trim())
            {
                if (char.IsLetterOrDigit(ch) || ch == '.' || ch == '_' || ch == '-')
                    sb.Append(ch);
                else
                    sb.Append('_');
            }
            var slug = sb.ToString().Trim('.', '_', '-');
            if (string.IsNullOrEmpty(slug)) slug = "rel";
            if (slug.Length > maxLen)
            {
                slug = slug.Substring(0, maxLen).TrimEnd('.', '_', '-');
                if (string.IsNullOrEmpty(slug)) slug = "rel";
            }
            return slug;
        }

        private string DeterministicRelationshipId(string sourceId, string targetId, string kind)
        {
            var payload = $"{ExpandIri(sourceId)}|{ExpandIri(targetId)}|{kind}";
            using var sha = SHA256.Create();
            var digest = BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(payload)))
                .Replace("-", "")
                .Substring(0, 12)
                .ToLowerInvariant();
            var safeKind = SafeKindSlug(kind);
            return $"kb:rel-{safeKind}-{digest}";
        }

        private string MintId(object instance)
        {
            var typeName = instance.GetType().Name;
            return $"kb:{typeName}-{Guid.NewGuid()}";
        }

        private Dictionary<string, object> ToJsonLd(object instance, string id)
        {
            var result = new Dictionary<string, object> { ["@id"] = id };
            var type = instance.GetType();

            var classIriField = type.GetField("ClassIri");
            if (classIriField != null)
            {
                var iri = (string)classIriField.GetValue(null);
                result["@type"] = CompactIri(iri);
            }

            foreach (var prop in type
                .GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Where(prop => prop.GetIndexParameters().Length == 0))
            {
                var value = prop.GetValue(instance);
                if (value == null)
                    continue;

                if (value is IList listValue && listValue.Count == 0)
                    continue;

                var attribute = prop.GetCustomAttribute<JsonLdPropertyAttribute>(inherit: true);
                var propKey = attribute != null ? attribute.Key : InferPropertyKey(prop, type);
                result[propKey] = ConvertValue(value);
            }

            return result;
        }

        private object ConvertValue(object value)
        {
            if (value == null)
                return null;

            if (value is string)
                return value;

            if (value is bool boolValue)
                return TypedLiteral("xsd:boolean", boolValue ? "true" : "false");

            if (value is sbyte || value is byte || value is short || value is ushort ||
                value is int || value is uint || value is long || value is ulong)
                return TypedLiteral("xsd:integer", Convert.ToString(value, CultureInfo.InvariantCulture));

            if (value is float || value is double || value is decimal)
                return TypedLiteral("xsd:decimal", Convert.ToString(value, CultureInfo.InvariantCulture));

            if (value is DateTime dateTime)
                return TypedLiteral("xsd:dateTime", dateTime.ToString("o", CultureInfo.InvariantCulture));

            if (!(value is string) && value is IEnumerable enumerable)
            {
                var items = new List<object>();
                foreach (var item in enumerable)
                    items.Add(ConvertValue(item));
                return items;
            }

            if (_idMap.TryGetValue(value, out var id))
                return new Dictionary<string, object> { ["@id"] = id };

            var nestedClassIri = value.GetType().GetField("ClassIri");
            if (nestedClassIri != null)
                return ToJsonLd(value, MintId(value));

            return value;
        }

        private Dictionary<string, string> TypedLiteral(string xsdType, string value)
        {
            return new Dictionary<string, string>
            {
                ["@type"] = xsdType,
                ["@value"] = value,
            };
        }

        private string CompactIri(string iri)
        {
            foreach (var kv in _context.Where(kv => iri.StartsWith(kv.Value)))
            {
                return $"{kv.Key}:{iri.Substring(kv.Value.Length)}";
            }
            return iri;
        }

        private string InferPropertyKey(PropertyInfo prop, Type fallbackType)
        {
            var declaringType = prop.DeclaringType ?? fallbackType;
            var nsField = declaringType.GetField("NamespacePrefix");
            var ns = nsField != null ? (string)nsField.GetValue(null) : "uco-core";
            return $"{ns}:{char.ToLower(prop.Name[0])}{prop.Name.Substring(1)}";
        }

        private static readonly Dictionary<string, string> DefaultContext = new Dictionary<string, string>
        {
            ["case-investigation"] = "https://ontology.caseontology.org/case/investigation/",
            ["kb"] = "http://example.org/kb/",
            ["uco-action"] = "https://ontology.unifiedcyberontology.org/uco/action/",
            ["uco-analysis"] = "https://ontology.unifiedcyberontology.org/uco/analysis/",
            ["uco-configuration"] = "https://ontology.unifiedcyberontology.org/uco/configuration/",
            ["uco-core"] = "https://ontology.unifiedcyberontology.org/uco/core/",
            ["uco-identity"] = "https://ontology.unifiedcyberontology.org/uco/identity/",
            ["uco-location"] = "https://ontology.unifiedcyberontology.org/uco/location/",
            ["uco-marking"] = "https://ontology.unifiedcyberontology.org/uco/marking/",
            ["uco-observable"] = "https://ontology.unifiedcyberontology.org/uco/observable/",
            ["uco-pattern"] = "https://ontology.unifiedcyberontology.org/uco/pattern/",
            ["uco-role"] = "https://ontology.unifiedcyberontology.org/uco/role/",
            ["uco-time"] = "https://ontology.unifiedcyberontology.org/uco/time/",
            ["uco-tool"] = "https://ontology.unifiedcyberontology.org/uco/tool/",
            ["uco-types"] = "https://ontology.unifiedcyberontology.org/uco/types/",
            ["uco-victim"] = "https://ontology.unifiedcyberontology.org/uco/victim/",
            ["uco-vocabulary"] = "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
            ["xsd"] = "http://www.w3.org/2001/XMLSchema#",
        };

        internal static string ToJsonString(object value, int indent)
        {
            if (value == null)
                return "null";

            if (value is string stringValue)
                return "\"" + Escape(stringValue) + "\"";

            if (value is bool || value is sbyte || value is byte || value is short || value is ushort ||
                value is int || value is uint || value is long || value is ulong ||
                value is float || value is double || value is decimal)
                return Convert.ToString(value, CultureInfo.InvariantCulture);

            if (value is IDictionary dictionary)
                return SerializeDictionary(dictionary, indent);

            if (!(value is string) && value is IEnumerable enumerable)
                return SerializeEnumerable(enumerable, indent);

            return "\"" + Escape(Convert.ToString(value, CultureInfo.InvariantCulture)) + "\"";
        }

        private static string SerializeDictionary(IDictionary dictionary, int indent)
        {
            var items = new List<string>();
            foreach (DictionaryEntry entry in dictionary)
            {
                items.Add($"\"{Escape(Convert.ToString(entry.Key, CultureInfo.InvariantCulture))}\": {ToJsonString(entry.Value, NextIndent(indent))}");
            }

            if (indent < 0)
                return "{" + string.Join(",", items) + "}";

            if (items.Count == 0)
                return "{}";

            var pad = new string(' ', indent * 4);
            var childPad = new string(' ', (indent + 1) * 4);
            return "{\n" + childPad + string.Join(",\n" + childPad, items) + "\n" + pad + "}";
        }

        private static string SerializeEnumerable(IEnumerable enumerable, int indent)
        {
            var items = new List<string>();
            foreach (var item in enumerable)
                items.Add(ToJsonString(item, NextIndent(indent)));

            if (indent < 0)
                return "[" + string.Join(",", items) + "]";

            if (items.Count == 0)
                return "[]";

            var pad = new string(' ', indent * 4);
            var childPad = new string(' ', (indent + 1) * 4);
            return "[\n" + childPad + string.Join(",\n" + childPad, items) + "\n" + pad + "]";
        }

        private static int NextIndent(int indent)
        {
            return indent < 0 ? -1 : indent + 1;
        }

        private static string Escape(string value)
        {
            return value
                .Replace("\\", "\\\\")
                .Replace("\"", "\\\"")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r")
                .Replace("\t", "\\t");
        }

        private static Dictionary<string, object> ParseJson(string json)
        {
            return (Dictionary<string, object>)ParseJsonValue(json.Trim(), 0, out _);
        }

        private static object ParseJsonValue(string json, int pos, out int end)
        {
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;

            if (json[pos] == '{')
                return ParseJsonObject(json, pos, out end);
            if (json[pos] == '[')
                return ParseJsonArray(json, pos, out end);
            if (json[pos] == '"')
                return ParseJsonString(json, pos, out end);

            int start = pos;
            while (pos < json.Length && json[pos] != ',' && json[pos] != '}' && json[pos] != ']' && !char.IsWhiteSpace(json[pos]))
                pos++;
            end = pos;
            var token = json.Substring(start, pos - start);
            if (token == "true") return true;
            if (token == "false") return false;
            if (token == "null") return null;
            if (token.Contains("."))
                return double.Parse(token, CultureInfo.InvariantCulture);
            return long.Parse(token, CultureInfo.InvariantCulture);
        }

        private static Dictionary<string, object> ParseJsonObject(string json, int pos, out int end)
        {
            var result = new Dictionary<string, object>();
            pos++; // skip '{'
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;

            if (json[pos] == '}') { end = pos + 1; return result; }

            while (true)
            {
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                var key = ParseJsonString(json, pos, out pos);
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                pos++; // skip ':'
                var value = ParseJsonValue(json, pos, out pos);
                result[key] = value;
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                if (json[pos] == '}') { end = pos + 1; return result; }
                pos++; // skip ','
            }
        }

        private static List<object> ParseJsonArray(string json, int pos, out int end)
        {
            var result = new List<object>();
            pos++; // skip '['
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;

            if (json[pos] == ']') { end = pos + 1; return result; }

            while (true)
            {
                var value = ParseJsonValue(json, pos, out pos);
                result.Add(value);
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                if (json[pos] == ']') { end = pos + 1; return result; }
                pos++; // skip ','
            }
        }

        private static string ParseJsonString(string json, int pos, out int end)
        {
            pos++; // skip opening '"'
            var sb = new System.Text.StringBuilder();
            while (json[pos] != '"')
            {
                if (json[pos] == '\\')
                {
                    pos++;
                    switch (json[pos])
                    {
                        case '"': sb.Append('"'); break;
                        case '\\': sb.Append('\\'); break;
                        case 'n': sb.Append('\n'); break;
                        case 'r': sb.Append('\r'); break;
                        case 't': sb.Append('\t'); break;
                        default: sb.Append(json[pos]); break;
                    }
                }
                else
                {
                    sb.Append(json[pos]);
                }
                pos++;
            }
            end = pos + 1; // skip closing '"'
            return sb.ToString();
        }
    }

    /// <summary>Metrics from an atomic/incremental streaming write (#71).</summary>
    public sealed class StreamingWriteResult
    {
        public int Nodes { get; }
        public long BytesWritten { get; }

        public StreamingWriteResult(int nodes, long bytesWritten)
        {
            Nodes = nodes;
            BytesWritten = bytesWritten;
        }
    }

    /// <summary>Observable process-wide typed registry state (#82).</summary>
    public sealed class ClassRegistryCacheMetrics
    {
        public long Hits { get; }
        public long Misses { get; }
        public long Generation { get; }
        public int RegisteredExtensions { get; }
        public int CachedClasses { get; }

        public ClassRegistryCacheMetrics(
            long hits, long misses, long generation,
            int registeredExtensions, int cachedClasses)
        {
            Hits = hits;
            Misses = misses;
            Generation = generation;
            RegisteredExtensions = registeredExtensions;
            CachedClasses = cachedClasses;
        }
    }

    /// <summary>Typed diagnostic when a JSON-LD node falls back to a raw dictionary.</summary>
    public class DeserializationWarning
    {
        public string NodeId { get; }
        public string Reason { get; }
        public string Detail { get; }
        public DeserializationWarning(string nodeId, string reason, string detail = "")
        {
            NodeId = nodeId;
            Reason = reason;
            Detail = detail ?? "";
        }
    }

    /// <summary>Result type returned by <see cref="CaseGraph.FromJsonLd"/>.</summary>
    public class FromJsonLdResult
    {
        public CaseGraph Graph { get; set; }
        public List<object> Objects { get; set; }
    }

    /// <summary>Raised when two registered types share the same ClassIri (#70).</summary>
    public class ClassRegistryConflictException : InvalidOperationException
    {
        public string ClassIri { get; }
        public Type ExistingType { get; }
        public Type ConflictingType { get; }

        public ClassRegistryConflictException(string classIri, Type existingType, Type conflictingType)
            : base($"Duplicate ClassIri '{classIri}' maps to incompatible types: {existingType.FullName} vs {conflictingType.FullName}")
        {
            ClassIri = classIri;
            ExistingType = existingType;
            ConflictingType = conflictingType;
        }
    }
}
