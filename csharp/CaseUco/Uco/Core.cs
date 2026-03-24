// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-core

using System.Collections.Generic;

namespace CaseUco.Uco.Core
{
    /// <summary>An annotation is an assertion made in relation to one or more objects.</summary>
    public class Annotation : CaseUco.Uco.Core.Assertion
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Annotation";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:object")]
        public List<CaseUco.Uco.Core.UcoObject> Object { get; set; }
    }

    /// <summary>An assertion is a statement declared to be true.</summary>
    public class Assertion : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Assertion";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:statement")]
        public List<string> Statement { get; set; }
    }

    /// <summary>An attributed name is a name of an entity issued by some attributed naming authority.</summary>
    public class AttributedName : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/AttributedName";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:namingAuthority")]
        public string NamingAuthority { get; set; }
    }

    /// <summary>A bundle is a container for a grouping of UCO content with no presumption of shared context.</summary>
    public class Bundle : CaseUco.Uco.Core.EnclosingCompilation
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Bundle";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A compilation is a grouping of things.</summary>
    public class Compilation : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Compilation";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A confidence is a grouping of characteristics unique to an asserted level of certainty in the accuracy of some information.</summary>
    public class ConfidenceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/ConfidenceFacet";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:confidence")]
        public ulong Confidence { get; set; }
    }

    /// <summary>A contextual compilation is a grouping of things sharing some context (e.g., a set of network connections observed on a given day, all accounts associated with a given person).</summary>
    public class ContextualCompilation : CaseUco.Uco.Core.Compilation
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/ContextualCompilation";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:object")]
        public List<CaseUco.Uco.Core.UcoObject> Object { get; set; }
    }

    /// <summary>A controlled vocabulary is an explicitly constrained set of string values.</summary>
    public class ControlledVocabulary : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/ControlledVocabulary";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:constrainingVocabularyName")]
        public string ConstrainingVocabularyName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:constrainingVocabularyReference")]
        public System.Uri ConstrainingVocabularyReference { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:value")]
        public string Value { get; set; }
    }

    /// <summary>An enclosing compilation is a container for a grouping of things.</summary>
    public class EnclosingCompilation : CaseUco.Uco.Core.Compilation
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/EnclosingCompilation";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:object")]
        public List<CaseUco.Uco.Core.UcoObject> Object { get; set; }
    }

    /// <summary>An Event is a noteworthy occurrence (something that happens or might happen).</summary>
    public class Event : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Event";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:endTime")]
        public List<System.DateTime> EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:eventAttribute")]
        public List<CaseUco.Uco.Types.Dictionary> EventAttribute { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:eventContext")]
        public List<CaseUco.Uco.Core.UcoObject> EventContext { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:eventType")]
        public List<string> EventType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:startTime")]
        public List<System.DateTime> StartTime { get; set; }
    }

    /// <summary>Characteristics of a reference to a resource outside of the UCO.</summary>
    public class ExternalReference : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/ExternalReference";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:definingContext")]
        public string DefiningContext { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:externalIdentifier")]
        public string ExternalIdentifier { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:referenceURL")]
        public System.Uri ReferenceURL { get; set; }
    }

    /// <summary>A facet is a grouping of characteristics singularly unique to a particular inherent aspect of a UCO domain object.</summary>
    public class Facet : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Facet";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A grouping is a compilation of referenced UCO content with a shared context.</summary>
    public class Grouping : CaseUco.Uco.Core.ContextualCompilation
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Grouping";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:context")]
        public List<string> Context { get; set; }
    }

    /// <summary>An identity abstraction is a grouping of identifying characteristics unique to an individual or organization. This class is an ontological structural abstraction for this concept. Implementations of t</summary>
    public class IdentityAbstraction : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/IdentityAbstraction";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>An item is a distinct article or unit.</summary>
    public class Item : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Item";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A marking definition abstraction is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be</summary>
    public class MarkingDefinitionAbstraction : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/MarkingDefinitionAbstraction";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A modus operandi is a particular method of operation (how a particular entity behaves or the resources they use).</summary>
    public class ModusOperandi : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/ModusOperandi";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A relationship is a grouping of characteristics unique to an assertion that one or more objects are related to another object in some way.</summary>
    public class Relationship : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/Relationship";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:endTime")]
        public List<System.DateTime> EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:isDirectional")]
        public bool IsDirectional { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:kindOfRelationship")]
        public string KindOfRelationship { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:source")]
        public List<CaseUco.Uco.Core.UcoObject> Source { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:startTime")]
        public List<System.DateTime> StartTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:target")]
        public CaseUco.Uco.Core.UcoObject Target { get; set; }
    }

    /// <summary>A UCO inherent characterization thing is a grouping of characteristics unique to a particular inherent aspect of a UCO domain object.</summary>
    public class UcoInherentCharacterizationThing : CaseUco.Uco.Core.UcoThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/UcoInherentCharacterizationThing";
        public new const string NamespacePrefix = "uco-core";
    }

    /// <summary>A UCO object is a representation of a fundamental concept either directly inherent to the cyber domain or indirectly related to the cyber domain and necessary for contextually characterizing cyber dom</summary>
    public class UcoObject : CaseUco.Uco.Core.UcoThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/UcoObject";
        public new const string NamespacePrefix = "uco-core";
        [global::CaseUco.JsonLdProperty("uco-core:createdBy")]
        public CaseUco.Uco.Core.IdentityAbstraction CreatedBy { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:description")]
        public List<string> Description { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:externalReference")]
        public List<CaseUco.Uco.Core.ExternalReference> ExternalReference { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:hasFacet")]
        public List<CaseUco.Uco.Core.Facet> HasFacet { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:modifiedTime")]
        public List<System.DateTime> ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:objectCreatedTime")]
        public System.DateTime? ObjectCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:objectMarking")]
        public List<CaseUco.Uco.Core.MarkingDefinitionAbstraction> ObjectMarking { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:objectStatus")]
        public string ObjectStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:specVersion")]
        public string SpecVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:tag")]
        public List<string> Tag { get; set; }
    }

    /// <summary>UcoThing is the top-level class within UCO.</summary>
    public class UcoThing
    {
        public const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/core/UcoThing";
        public const string NamespacePrefix = "uco-core";
    }

}