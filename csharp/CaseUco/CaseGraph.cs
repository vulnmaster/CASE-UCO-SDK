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

        /// <summary>Add an object to the graph and assign it an @id.</summary>
        public string Add(object instance)
        {
            var id = MintId(instance);
            _idMap[instance] = id;
            var jsonObj = ToJsonLd(instance, id);
            _objects.Add(jsonObj);
            return id;
        }

        /// <summary>Get the @id assigned to a previously-added instance.</summary>
        public string GetId(object instance)
        {
            return _idMap.TryGetValue(instance, out var id) ? id : null;
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
            ["uco-core"] = "https://ontology.unifiedcyberontology.org/uco/core/",
            ["uco-identity"] = "https://ontology.unifiedcyberontology.org/uco/identity/",
            ["uco-location"] = "https://ontology.unifiedcyberontology.org/uco/location/",
            ["uco-observable"] = "https://ontology.unifiedcyberontology.org/uco/observable/",
            ["uco-tool"] = "https://ontology.unifiedcyberontology.org/uco/tool/",
            ["uco-types"] = "https://ontology.unifiedcyberontology.org/uco/types/",
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
    }
}
