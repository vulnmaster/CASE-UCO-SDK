// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-action

using System.Collections.Generic;

namespace CaseUco.Uco.Action
{
    /// <summary>An action is something that may be done or performed.</summary>
    public class Action : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/Action";
        public new const string NamespacePrefix = "uco-action";
        [global::CaseUco.JsonLdProperty("uco-action:actionCount")]
        public ulong? ActionCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:actionStatus")]
        public List<string> ActionStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:environment")]
        public CaseUco.Uco.Core.UcoObject Environment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:error")]
        public List<CaseUco.Uco.Core.UcoObject> Error { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:instrument")]
        public List<CaseUco.Uco.Core.UcoObject> Instrument { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:location")]
        public List<CaseUco.Uco.Location.Location> Location { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:object")]
        public List<CaseUco.Uco.Core.UcoObject> Object { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:participant")]
        public List<CaseUco.Uco.Core.UcoObject> Participant { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:performer")]
        public CaseUco.Uco.Core.UcoObject Performer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:result")]
        public List<CaseUco.Uco.Core.UcoObject> Result { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:startTime")]
        public System.DateTime? StartTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:subaction")]
        public List<CaseUco.Uco.Action.Action> Subaction { get; set; }
    }

    /// <summary>An action argument facet is a grouping of characteristics unique to a single parameter of an action.</summary>
    public class ActionArgumentFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/ActionArgumentFacet";
        public new const string NamespacePrefix = "uco-action";
        [global::CaseUco.JsonLdProperty("uco-action:argumentName")]
        public string ArgumentName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:value")]
        public string Value { get; set; }
    }

    /// <summary>An action estimation facet is a grouping of characteristics unique to decision-focused approximation aspects for an action that may potentially be performed.</summary>
    public class ActionEstimationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/ActionEstimationFacet";
        public new const string NamespacePrefix = "uco-action";
        [global::CaseUco.JsonLdProperty("uco-action:estimatedCost")]
        public string EstimatedCost { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:estimatedEfficacy")]
        public string EstimatedEfficacy { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:estimatedImpact")]
        public string EstimatedImpact { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:objective")]
        public string Objective { get; set; }
    }

    /// <summary>An action frequency facet is a grouping of characteristics unique to the frequency of occurrence for an action.</summary>
    public class ActionFrequencyFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/ActionFrequencyFacet";
        public new const string NamespacePrefix = "uco-action";
        [global::CaseUco.JsonLdProperty("uco-action:rate")]
        public decimal Rate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:scale")]
        public string Scale { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:trend")]
        public List<string> Trend { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:units")]
        public string Units { get; set; }
    }

    /// <summary>An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action lifecycles.</summary>
    public class ActionLifecycle : CaseUco.Uco.Action.Action
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/ActionLifecycle";
        public new const string NamespacePrefix = "uco-action";
        [global::CaseUco.JsonLdProperty("uco-action:actionCount")]
        public new List<ulong> ActionCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:endTime")]
        public new List<System.DateTime> EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:error")]
        public new List<CaseUco.Uco.Core.UcoObject> Error { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:phase")]
        public CaseUco.Uco.Action.ArrayOfAction Phase { get; set; }
        [global::CaseUco.JsonLdProperty("uco-action:startTime")]
        public new List<System.DateTime> StartTime { get; set; }
    }

    /// <summary>An action pattern is a grouping of characteristics unique to a combination of actions forming a consistent or characteristic arrangement.</summary>
    public class ActionPattern : CaseUco.Uco.Action.Action
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/ActionPattern";
        public new const string NamespacePrefix = "uco-action";
    }

    /// <summary>An array of action is an ordered list of references to things that may be done or performed.</summary>
    public class ArrayOfAction : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/action/ArrayOfAction";
        public new const string NamespacePrefix = "uco-action";
        [global::CaseUco.JsonLdProperty("uco-action:action")]
        public List<CaseUco.Uco.Action.Action> Action { get; set; }
    }

}