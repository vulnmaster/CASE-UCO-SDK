// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-victim

using System.Collections.Generic;

namespace CaseUco.Uco.Victim
{
    /// <summary>A victim is a role played by a person or organization that is/was the target of some malicious action.</summary>
    public class Victim : CaseUco.Uco.Role.NeutralRole
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/victim/Victim";
        public new const string NamespacePrefix = "uco-victim";
    }

    /// <summary>A victim targeting is a grouping of characteristics unique to people or organizations that are the target of some malicious activity.</summary>
    public class VictimTargeting : CaseUco.Uco.Victim.Victim
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/victim/VictimTargeting";
        public new const string NamespacePrefix = "uco-victim";
    }

}