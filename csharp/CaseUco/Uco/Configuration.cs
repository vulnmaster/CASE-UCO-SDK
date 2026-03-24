// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-configuration

using System.Collections.Generic;

namespace CaseUco.Uco.Configuration
{
    /// <summary>A configuration is a grouping of characteristics unique to a set of parameters or initial settings for the use of a tool, application, software, or other cyber object.</summary>
    public class Configuration : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/configuration/Configuration";
        public new const string NamespacePrefix = "uco-configuration";
        [global::CaseUco.JsonLdProperty("uco-configuration:configurationEntry")]
        public List<CaseUco.Uco.Configuration.ConfigurationEntry> ConfigurationEntry { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:dependencies")]
        public List<CaseUco.Uco.Configuration.Dependency> Dependencies { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:usageContextAssumptions")]
        public List<string> UsageContextAssumptions { get; set; }
    }

    /// <summary>A configuration entry is a grouping of characteristics unique to a particular parameter or initial setting for the use of a tool, application, software, or other cyber object.</summary>
    public class ConfigurationEntry : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/configuration/ConfigurationEntry";
        public new const string NamespacePrefix = "uco-configuration";
        [global::CaseUco.JsonLdProperty("uco-configuration:itemDescription")]
        public string ItemDescription { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:itemName")]
        public string ItemName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:itemObject")]
        public List<CaseUco.Uco.Core.UcoObject> ItemObject { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:itemType")]
        public string ItemType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:itemValue")]
        public List<string> ItemValue { get; set; }
    }

    /// <summary>A dependency is a grouping of characteristics unique to something that a tool or other software relies on to function as intended.</summary>
    public class Dependency : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/configuration/Dependency";
        public new const string NamespacePrefix = "uco-configuration";
        [global::CaseUco.JsonLdProperty("uco-configuration:dependencyDescription")]
        public string DependencyDescription { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:dependencyType")]
        public string DependencyType { get; set; }
    }

}