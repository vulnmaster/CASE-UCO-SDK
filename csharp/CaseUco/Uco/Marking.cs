// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-marking

using System.Collections.Generic;

namespace CaseUco.Uco.Marking
{
    /// <summary>A granular marking is a grouping of characteristics unique to specification of marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) that apply to par</summary>
    public class GranularMarking : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/GranularMarking";
        public new const string NamespacePrefix = "uco-marking";
        [global::CaseUco.JsonLdProperty("uco-marking:contentSelectors")]
        public List<string> ContentSelectors { get; set; }
        [global::CaseUco.JsonLdProperty("uco-marking:marking")]
        public List<CaseUco.Uco.Marking.MarkingDefinition> Marking { get; set; }
    }

    /// <summary>A license marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey de</summary>
    public class LicenseMarking : CaseUco.Uco.Marking.MarkingModel
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/LicenseMarking";
        public new const string NamespacePrefix = "uco-marking";
        [global::CaseUco.JsonLdProperty("uco-marking:definitionType")]
        public List<string> DefinitionType { get; set; }
        [global::CaseUco.CaseRequired]
        [global::CaseUco.JsonLdProperty("uco-marking:license")]
        public string License { get; set; }
    }

    /// <summary>A marking definition is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be used and sh</summary>
    public class MarkingDefinition : CaseUco.Uco.Core.MarkingDefinitionAbstraction
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingDefinition";
        public new const string NamespacePrefix = "uco-marking";
        [global::CaseUco.JsonLdProperty("uco-marking:definition")]
        public List<CaseUco.Uco.Marking.MarkingModel> Definition { get; set; }
        [global::CaseUco.CaseRequired]
        [global::CaseUco.JsonLdProperty("uco-marking:definitionType")]
        public string DefinitionType { get; set; }
    }

    /// <summary>A marking model is a grouping of characteristics unique to the expression of a particular form of data marking definitions (restrictions, permissions, and other guidance for how data can be used and s</summary>
    public class MarkingModel : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingModel";
        public new const string NamespacePrefix = "uco-marking";
    }

    /// <summary>A release-to marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey</summary>
    public class ReleaseToMarking : CaseUco.Uco.Marking.MarkingModel
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/ReleaseToMarking";
        public new const string NamespacePrefix = "uco-marking";
        [global::CaseUco.CaseRequired]
        [global::CaseUco.JsonLdProperty("uco-marking:authorizedIdentities")]
        public List<string> AuthorizedIdentities { get; set; }
        [global::CaseUco.JsonLdProperty("uco-marking:definitionType")]
        public List<string> DefinitionType { get; set; }
    }

    /// <summary>A statement marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey </summary>
    public class StatementMarking : CaseUco.Uco.Marking.MarkingModel
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/StatementMarking";
        public new const string NamespacePrefix = "uco-marking";
        [global::CaseUco.JsonLdProperty("uco-marking:definitionType")]
        public List<string> DefinitionType { get; set; }
        [global::CaseUco.CaseRequired]
        [global::CaseUco.JsonLdProperty("uco-marking:statement")]
        public string Statement { get; set; }
    }

    /// <summary>A terms of use marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to conv</summary>
    public class TermsOfUseMarking : CaseUco.Uco.Marking.MarkingModel
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/marking/TermsOfUseMarking";
        public new const string NamespacePrefix = "uco-marking";
        [global::CaseUco.JsonLdProperty("uco-marking:definitionType")]
        public List<string> DefinitionType { get; set; }
        [global::CaseUco.CaseRequired]
        [global::CaseUco.JsonLdProperty("uco-marking:termsOfUse")]
        public string TermsOfUse { get; set; }
    }

}