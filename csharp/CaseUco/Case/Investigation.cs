// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: case-investigation

using System.Collections.Generic;

namespace CaseUco.Case.Investigation
{
    /// <summary>Attorney is a role involved in preparing, interpreting, and applying law.</summary>
    public class Attorney : CaseUco.Uco.Role.Role
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/Attorney";
        public new const string NamespacePrefix = "case-investigation";
    }

    /// <summary>An authorization is a grouping of characteristics unique to some form of authoritative permission identified for investigative action.</summary>
    public class Authorization : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/Authorization";
        public new const string NamespacePrefix = "case-investigation";
        [global::CaseUco.JsonLdProperty("case-investigation:authorizationIdentifier")]
        public List<string> AuthorizationIdentifier { get; set; }
        [global::CaseUco.JsonLdProperty("case-investigation:authorizationType")]
        public string AuthorizationType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:startTime")]
        public System.DateTime? StartTime { get; set; }
    }

    /// <summary>Examiner is a role involved in providing scientific evaluations of evidence that are used to aid law enforcement investigations and court cases.</summary>
    public class Examiner : CaseUco.Uco.Role.Role
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/Examiner";
        public new const string NamespacePrefix = "case-investigation";
    }

    /// <summary>An investigation is a grouping of characteristics unique to an exploration of the facts involved in a cyber-relevant set of suspicious activity.</summary>
    public class Investigation : CaseUco.Uco.Core.ContextualCompilation
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/Investigation";
        public new const string NamespacePrefix = "case-investigation";
        [global::CaseUco.JsonLdProperty("case-investigation:focus")]
        public List<string> Focus { get; set; }
        [global::CaseUco.JsonLdProperty("case-investigation:investigationForm")]
        public List<string> InvestigationForm { get; set; }
        [global::CaseUco.JsonLdProperty("case-investigation:investigationStatus")]
        public string InvestigationStatus { get; set; }
        [global::CaseUco.JsonLdProperty("case-investigation:relevantAuthorization")]
        public List<CaseUco.Case.Investigation.Authorization> RelevantAuthorization { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:startTime")]
        public System.DateTime? StartTime { get; set; }
    }

    /// <summary>An investigative action is something that may be done or performed within the context of an investigation, typically to examine or analyze evidence or other data.</summary>
    public class InvestigativeAction : CaseUco.Uco.Action.Action
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/InvestigativeAction";
        public new const string NamespacePrefix = "case-investigation";
        [global::CaseUco.JsonLdProperty("case-investigation:wasInformedBy")]
        public List<CaseUco.Case.Investigation.InvestigativeAction> WasInformedBy { get; set; }
    }

    /// <summary>Investigator is a role involved in coordinating an investigation.</summary>
    public class Investigator : CaseUco.Uco.Role.Role
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/Investigator";
        public new const string NamespacePrefix = "case-investigation";
    }

    /// <summary>A provenance record is a grouping of characteristics unique to the provenantial (chronology of the ownership, custody or location) connection between an investigative action and a set of observations </summary>
    public class ProvenanceRecord : CaseUco.Uco.Core.ContextualCompilation
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/ProvenanceRecord";
        public new const string NamespacePrefix = "case-investigation";
        [global::CaseUco.JsonLdProperty("case-investigation:exhibitNumber")]
        public string ExhibitNumber { get; set; }
        [global::CaseUco.JsonLdProperty("case-investigation:rootExhibitNumber")]
        public List<string> RootExhibitNumber { get; set; }
    }

    /// <summary>Subject is a role whose conduct is within the scope of an investigation.</summary>
    public class Subject : CaseUco.Uco.Role.Role
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/Subject";
        public new const string NamespacePrefix = "case-investigation";
    }

    /// <summary>A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role whose conduct may be within th</summary>
    public class SubjectActionLifecycle : CaseUco.Uco.Action.ActionLifecycle
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/SubjectActionLifecycle";
        public new const string NamespacePrefix = "case-investigation";
    }

    /// <summary>A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role characterized by its potential </summary>
    public class VictimActionLifecycle : CaseUco.Uco.Action.ActionLifecycle
    {
        public new const string ClassIri = "https://ontology.caseontology.org/case/investigation/VictimActionLifecycle";
        public new const string NamespacePrefix = "case-investigation";
    }

}