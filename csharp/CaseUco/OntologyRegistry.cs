// OntologyRegistry — runtime introspection for CASE/UCO ontology classes, properties, and vocabularies.
//
// Loads the auto-generated _registry.json and exposes search, listing, and
// query methods so developers can discover the right classes without leaving
// their IDE or REPL.

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;

namespace CaseUco
{
    /// <summary>
    /// Provides runtime discovery of CASE/UCO ontology classes, properties, and
    /// vocabulary types. All methods are static and thread-safe after first load.
    /// </summary>
    public static class OntologyRegistry
    {
        private static volatile Dictionary<string, object> _registry;
        private static readonly object _lock = new object();

        private static Dictionary<string, object> Registry
        {
            get
            {
                if (_registry == null)
                {
                    lock (_lock)
                    {
                        if (_registry == null)
                            _registry = LoadRegistry();
                    }
                }
                return _registry;
            }
        }

        private static Dictionary<string, object> LoadRegistry()
        {
            var assembly = typeof(OntologyRegistry).Assembly;
            var dir = Path.GetDirectoryName(assembly.Location) ?? ".";
            var path = dir + Path.DirectorySeparatorChar + "_registry.json";

            if (!File.Exists(path))
            {
                var srcDir = Path.GetDirectoryName(
                    new Uri(assembly.CodeBase ?? assembly.Location).LocalPath) ?? ".";
                path = srcDir + Path.DirectorySeparatorChar + "_registry.json";
            }

            if (!File.Exists(path))
                throw new FileNotFoundException(
                    "Ontology registry not found. Run 'case-uco-generate generate' to produce it.",
                    path);

            var json = File.ReadAllText(path);
            return (Dictionary<string, object>)ParseJsonValue(json.Trim(), 0, out _);
        }

        /// <summary>Search for classes by keyword (case-insensitive substring match on name and description).</summary>
        public static List<Dictionary<string, object>> Search(string query)
        {
            var q = query.ToLowerInvariant();
            var classes = GetClassesDict();
            var results = new List<Dictionary<string, object>>();

            foreach (var kv in classes)
            {
                var name = kv.Key;
                var cls = (Dictionary<string, object>)kv.Value;
                object descObj;
                var desc = cls.TryGetValue("description", out descObj) ? descObj?.ToString() ?? "" : "";

                if (name.ToLowerInvariant().Contains(q) || desc.ToLowerInvariant().Contains(q))
                {
                    var entry = new Dictionary<string, object>(cls) { ["name"] = name };
                    results.Add(entry);
                }
            }

            results.Sort((a, b) =>
            {
                object maObj, mbObj;
                var ma = a.TryGetValue("module", out maObj) ? maObj?.ToString() ?? "" : "";
                var mb = b.TryGetValue("module", out mbObj) ? mbObj?.ToString() ?? "" : "";
                int cmp = string.Compare(ma, mb, StringComparison.Ordinal);
                if (cmp != 0) return cmp;
                return string.Compare(
                    a["name"]?.ToString() ?? "", b["name"]?.ToString() ?? "",
                    StringComparison.Ordinal);
            });

            return results;
        }

        /// <summary>List all module names (e.g. "uco.observable", "case.investigation").</summary>
        public static List<string> ListModules()
        {
            var modules = (List<object>)Registry["modules"];
            return modules.Select(m => m.ToString()).OrderBy(m => m).ToList();
        }

        /// <summary>List class names, optionally filtered by module (partial match).</summary>
        public static List<string> ListClasses(string module = null)
        {
            var classes = GetClassesDict();
            var results = new List<string>();

            foreach (var kv in classes)
            {
                if (module == null)
                {
                    results.Add(kv.Key);
                    continue;
                }
                var cls = (Dictionary<string, object>)kv.Value;
                object modObj;
                var mod = cls.TryGetValue("module", out modObj) ? modObj?.ToString() ?? "" : "";
                if (mod.IndexOf(module, StringComparison.OrdinalIgnoreCase) >= 0)
                    results.Add(kv.Key);
            }

            results.Sort();
            return results;
        }

        /// <summary>Get full details for a class by name (case-insensitive).</summary>
        public static Dictionary<string, object> GetClass(string name)
        {
            var classes = GetClassesDict();
            return classes
                .Where(kv => string.Equals(kv.Key, name, StringComparison.OrdinalIgnoreCase))
                .Select(kv => new Dictionary<string, object>((Dictionary<string, object>)kv.Value)
                {
                    ["name"] = kv.Key
                })
                .FirstOrDefault();
        }

        /// <summary>Find classes that have a property of the given type (case-insensitive).</summary>
        public static List<Dictionary<string, object>> FindByPropertyType(string typeName)
        {
            var t = typeName.ToLowerInvariant();
            var classes = GetClassesDict();
            var results = new List<Dictionary<string, object>>();

            foreach (var kv in classes)
            {
                var cls = (Dictionary<string, object>)kv.Value;
                object propsObj;
                if (!cls.TryGetValue("properties", out propsObj)) continue;
                var props = (List<object>)propsObj;
                bool match = props.Any(p =>
                {
                    var prop = (Dictionary<string, object>)p;
                    object ptObj;
                    var pt = prop.TryGetValue("type", out ptObj) ? ptObj?.ToString() ?? "" : "";
                    return pt.ToLowerInvariant().Contains(t);
                });
                if (match)
                {
                    var entry = new Dictionary<string, object>(cls) { ["name"] = kv.Key };
                    results.Add(entry);
                }
            }

            results.Sort((a, b) => string.Compare(
                a["name"]?.ToString() ?? "", b["name"]?.ToString() ?? "",
                StringComparison.Ordinal));
            return results;
        }

        /// <summary>Find all Facet classes (is_facet == true).</summary>
        public static List<Dictionary<string, object>> FindFacets()
        {
            var classes = GetClassesDict();
            var results = new List<Dictionary<string, object>>();

            foreach (var kv in classes)
            {
                var cls = (Dictionary<string, object>)kv.Value;
                object facetObj;
                if (cls.TryGetValue("is_facet", out facetObj) && facetObj is bool isFacet && isFacet)
                {
                    var entry = new Dictionary<string, object>(cls) { ["name"] = kv.Key };
                    results.Add(entry);
                }
            }

            results.Sort((a, b) => string.Compare(
                a["name"]?.ToString() ?? "", b["name"]?.ToString() ?? "",
                StringComparison.Ordinal));
            return results;
        }

        /// <summary>List all vocabulary types with their members.</summary>
        public static List<Dictionary<string, object>> ListVocabs()
        {
            object vocabsObj;
            if (!Registry.TryGetValue("vocabs", out vocabsObj)) return new List<Dictionary<string, object>>();
            var vocabs = (Dictionary<string, object>)vocabsObj;
            var results = new List<Dictionary<string, object>>();

            foreach (var kv in vocabs)
            {
                var vocab = (Dictionary<string, object>)kv.Value;
                var entry = new Dictionary<string, object>(vocab) { ["name"] = kv.Key };
                results.Add(entry);
            }

            results.Sort((a, b) => string.Compare(
                a["name"]?.ToString() ?? "", b["name"]?.ToString() ?? "",
                StringComparison.Ordinal));
            return results;
        }

        private static Dictionary<string, object> GetClassesDict()
        {
            return (Dictionary<string, object>)Registry["classes"];
        }

        // --- Lightweight JSON parser (mirrors CaseGraph's parser) ---

        private static object ParseJsonValue(string json, int pos, out int end)
        {
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
            if (json[pos] == '{') return ParseJsonObject(json, pos, out end);
            if (json[pos] == '[') return ParseJsonArray(json, pos, out end);
            if (json[pos] == '"') return ParseJsonString(json, pos, out end);
            int start = pos;
            while (pos < json.Length && json[pos] != ',' && json[pos] != '}' && json[pos] != ']' && !char.IsWhiteSpace(json[pos])) pos++;
            end = pos;
            var token = json.Substring(start, pos - start);
            if (token == "true") return true;
            if (token == "false") return false;
            if (token == "null") return null;
            if (token.Contains(".")) return double.Parse(token, CultureInfo.InvariantCulture);
            return long.Parse(token, CultureInfo.InvariantCulture);
        }

        private static Dictionary<string, object> ParseJsonObject(string json, int pos, out int end)
        {
            var result = new Dictionary<string, object>();
            pos++;
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
            if (json[pos] == '}') { end = pos + 1; return result; }
            while (true)
            {
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                var key = ParseJsonString(json, pos, out pos);
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                pos++;
                var value = ParseJsonValue(json, pos, out pos);
                result[key] = value;
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                if (json[pos] == '}') { end = pos + 1; return result; }
                pos++;
            }
        }

        private static List<object> ParseJsonArray(string json, int pos, out int end)
        {
            var result = new List<object>();
            pos++;
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
            if (json[pos] == ']') { end = pos + 1; return result; }
            while (true)
            {
                var value = ParseJsonValue(json, pos, out pos);
                result.Add(value);
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                if (json[pos] == ']') { end = pos + 1; return result; }
                pos++;
            }
        }

        private static string ParseJsonString(string json, int pos, out int end)
        {
            pos++;
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
            end = pos + 1;
            return sb.ToString();
        }
    }
}
