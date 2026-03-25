using System;

namespace CaseUco
{
    /// <summary>
    /// Marks a generated CASE/UCO property as required by the ontology.
    /// CaseGraph validates these constraints before adding objects to the graph.
    /// </summary>
    [AttributeUsage(AttributeTargets.Property, AllowMultiple = false)]
    public sealed class CaseRequiredAttribute : Attribute
    {
    }
}
