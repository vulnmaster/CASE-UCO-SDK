// CaseGraph — main entry point for building and serializing CASE/UCO graphs in C#.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;

namespace CaseUco
{
    /// <summary>
    /// Build a CASE/UCO JSON-LD graph with typed objects.
    /// </summary>
    public class CaseGraph
    {
        private readonly Dictionary<string, string> _context;
        private readonly List<Dictionary<string, object>> _objects;
        private readonly Dictionary<object, string> _idMap;

        public CaseGraph(string kbPrefix = "http://example.org/kb/")
        {
            _context = new Dictionary<string, string>(DefaultContext);
            _context["kb"] = kbPrefix;
            _objects = new List<Dictionary<string, object>>();
            _idMap = new Dictionary<object, string>(new ReferenceEqualityComparer());
        }

        public void AddContext(string prefix, string iri)
        {
            _context[prefix] = iri;
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
            _objects.Add(jsonObj);
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

        /// <summary>Return the number of objects in the graph.</summary>
        public int Count => _objects.Count;

        /// <summary>Load a JSON-LD string into this graph, merging context and appending objects.</summary>
        public void Load(string json)
        {
            var doc = ParseJson(json);
            if (doc.TryGetValue("@context", out var ctxObj) && ctxObj is Dictionary<string, object> ctx)
            {
                foreach (var kv in ctx.Where(kv => kv.Value is string))
                {
                    _context[kv.Key] = (string)kv.Value;
                }
            }
            if (doc.TryGetValue("@graph", out var graphObj) && graphObj is List<object> graphList)
            {
                foreach (var item in graphList.OfType<Dictionary<string, object>>())
                {
                    _objects.Add(item);
                }
            }
        }

        /// <summary>Parse a JSON-LD string into typed objects where possible.
        /// Types are matched by scanning loaded assemblies for classes with a static ClassIri field.</summary>
        public static FromJsonLdResult FromJsonLd(string json)
        {
            var doc = ParseJson(json);
            var graph = new CaseGraph();

            if (doc.TryGetValue("@context", out var ctxObj) && ctxObj is Dictionary<string, object> ctx)
            {
                foreach (var kv in ctx.Where(kv => kv.Value is string))
                    graph._context[kv.Key] = (string)kv.Value;
            }

            var objects = new List<object>();

            if (doc.TryGetValue("@graph", out var graphObj) && graphObj is List<object> graphList)
            {
                foreach (var item in graphList.OfType<Dictionary<string, object>>())
                {
                    graph._objects.Add(item);
                    var typed = TryInstantiate(item, graph._context);
                    objects.Add(typed ?? (object)item);
                }
            }

            return new FromJsonLdResult { Graph = graph, Objects = objects };
        }

        private static string ExpandIri(string value, Dictionary<string, string> context)
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

        private static object TryInstantiate(Dictionary<string, object> obj, Dictionary<string, string> context)
        {
            if (!obj.TryGetValue("@type", out var typeObj) || !(typeObj is string typeStr))
                return null;

            var expandedIri = ExpandIri(typeStr, context);

            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                Type[] types;
                try { types = asm.GetTypes(); }
                catch (ReflectionTypeLoadException ex) { types = ex.Types.Where(t => t != null).ToArray(); }

                foreach (var type in types.Where(t =>
                    t.IsClass && !t.IsAbstract && t.Namespace != null &&
                    t.Namespace.StartsWith("CaseUco")))
                {
                    var field = type.GetField("ClassIri", BindingFlags.Public | BindingFlags.Static);
                    if (field == null || (string)field.GetValue(null) != expandedIri)
                        continue;

                    try
                    {
                        var instance = Activator.CreateInstance(type);
                        SetPropertiesFromJsonLd(instance, obj, context);
                        return instance;
                    }
                    catch (MemberAccessException) { return null; }
                    catch (TargetInvocationException) { return null; }
                }
            }

            return null;
        }

        private static void SetPropertiesFromJsonLd(object instance, Dictionary<string, object> obj, Dictionary<string, string> context)
        {
            var type = instance.GetType();
            foreach (var prop in type.GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Where(p => p.CanWrite))
            {
                string matchKey = null;

                var attr = prop.GetCustomAttribute<JsonLdPropertyAttribute>(inherit: true);
                if (attr != null && obj.ContainsKey(attr.Key))
                    matchKey = attr.Key;

                if (matchKey == null)
                {
                    var nsField = (prop.DeclaringType ?? type).GetField("NamespacePrefix");
                    var ns = nsField != null ? (string)nsField.GetValue(null) : "uco-core";
                    var camelName = char.ToLower(prop.Name[0]) + prop.Name.Substring(1);
                    var candidate = ns + ":" + camelName;
                    if (obj.ContainsKey(candidate))
                        matchKey = candidate;
                }

                if (matchKey == null) continue;

                try { prop.SetValue(instance, ConvertToClrType(obj[matchKey], prop.PropertyType)); }
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
                ["@context"] = _context,
                ["@graph"] = _objects,
            };
            return ToJsonString(doc, indented ? 0 : -1);
        }

        /// <summary>Write the graph to a file.</summary>
        public void Write(string path)
        {
            System.IO.File.WriteAllText(path, Serialize());
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
                if (kv.Key == "@type") { count++; continue; }
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

        /// <summary>Split the graph into smaller chunks of at most maxObjects each.</summary>
        public List<CaseGraph> Split(int maxObjects = 10000)
        {
            var chunks = new List<CaseGraph>();
            for (int i = 0; i < _objects.Count; i += maxObjects)
            {
                var chunk = new CaseGraph(_context["kb"]);
                foreach (var kv in _context)
                    chunk._context[kv.Key] = kv.Value;
                int end = Math.Min(i + maxObjects, _objects.Count);
                for (int j = i; j < end; j++)
                    chunk._objects.Add(_objects[j]);
                chunks.Add(chunk);
            }
            return chunks;
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

        private string ToJsonString(object value, int indent)
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

        private string SerializeDictionary(IDictionary dictionary, int indent)
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

        private string SerializeEnumerable(IEnumerable enumerable, int indent)
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

        private int NextIndent(int indent)
        {
            return indent < 0 ? -1 : indent + 1;
        }

        private string Escape(string value)
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

    /// <summary>Result type returned by <see cref="CaseGraph.FromJsonLd"/>.</summary>
    public class FromJsonLdResult
    {
        public CaseGraph Graph { get; set; }
        public List<object> Objects { get; set; }
    }
}

