using System;

namespace CaseUco
{
    [AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
    public sealed class JsonLdPropertyAttribute : Attribute
    {
        public JsonLdPropertyAttribute(string key)
        {
            Key = key;
        }

        public string Key { get; }
    }
}
