// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-tool

using System.Collections.Generic;

namespace CaseUco.Uco.Tool
{
    /// <summary>An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of explanation, interpretation or logical reasoning.</summary>
    public class AnalyticTool : CaseUco.Uco.Tool.Tool
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/AnalyticTool";
        public new const string NamespacePrefix = "uco-tool";
    }

    /// <summary>A build facet is a grouping of characteristics unique to a particular version of a software.</summary>
    public class BuildFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/BuildFacet";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-tool:buildInformation")]
        public CaseUco.Uco.Tool.BuildInformationType BuildInformation { get; set; }
    }

    /// <summary>A build information type is a grouping of characteristics that describe how a particular version of software was converted from source code to executable code.</summary>
    public class BuildInformationType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/BuildInformationType";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-tool:buildConfiguration")]
        public CaseUco.Uco.Configuration.Configuration BuildConfiguration { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildID")]
        public string BuildID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildLabel")]
        public string BuildLabel { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildOutputLog")]
        public string BuildOutputLog { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildProject")]
        public string BuildProject { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildScript")]
        public string BuildScript { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildUtility")]
        public CaseUco.Uco.Tool.BuildUtilityType BuildUtility { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:buildVersion")]
        public string BuildVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:compilationDate")]
        public System.DateTime? CompilationDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:compilers")]
        public List<CaseUco.Uco.Tool.CompilerType> Compilers { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:libraries")]
        public List<CaseUco.Uco.Tool.LibraryType> Libraries { get; set; }
    }

    /// <summary>A build utility type characterizes the tool used to convert from source code to executable code for a particular version of software.</summary>
    public class BuildUtilityType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/BuildUtilityType";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-tool:buildUtilityName")]
        public string BuildUtilityName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:cpeid")]
        public string Cpeid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:swid")]
        public string Swid { get; set; }
    }

    /// <summary>A compiler type is a grouping of characteristics unique to a specific program that translates computer code written in one programming language (the source language) into another language (the target </summary>
    public class CompilerType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/CompilerType";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-tool:compilerInformalDescription")]
        public string CompilerInformalDescription { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:cpeid")]
        public string Cpeid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:swid")]
        public string Swid { get; set; }
    }

    /// <summary>A ConfiguredTool is a Tool that is known to be configured to run in a more specified manner than some unconfigured or less-configured Tool.</summary>
    public class ConfiguredTool : CaseUco.Uco.Tool.Tool
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/ConfiguredTool";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-configuration:isConfigurationOf")]
        public CaseUco.Uco.Tool.Tool IsConfigurationOf { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:usesConfiguration")]
        public CaseUco.Uco.Configuration.Configuration UsesConfiguration { get; set; }
    }

    /// <summary>A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of guarding.</summary>
    public class DefensiveTool : CaseUco.Uco.Tool.Tool
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/DefensiveTool";
        public new const string NamespacePrefix = "uco-tool";
    }

    /// <summary>A library type is a grouping of characteristics unique to a collection of resources incorporated into the build of a software.</summary>
    public class LibraryType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/LibraryType";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-tool:libraryName")]
        public string LibraryName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:libraryVersion")]
        public string LibraryVersion { get; set; }
    }

    /// <summary>A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent task or purpose.</summary>
    public class MaliciousTool : CaseUco.Uco.Tool.Tool
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/MaliciousTool";
        public new const string NamespacePrefix = "uco-tool";
    }

    /// <summary>A tool is an element of hardware and/or software utilized to carry out a particular function.</summary>
    public class Tool : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/tool/Tool";
        public new const string NamespacePrefix = "uco-tool";
        [global::CaseUco.JsonLdProperty("uco-tool:creator")]
        public CaseUco.Uco.Identity.Identity Creator { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:references")]
        public List<System.Uri> References { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:servicePack")]
        public string ServicePack { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:toolType")]
        public string ToolType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-tool:version")]
        public string Version { get; set; }
    }

}