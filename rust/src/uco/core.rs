//! Auto-generated uco-core types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

use crate::uco::types::Dictionary;

/// An annotation is an assertion made in relation to one or more objects.
#[derive(Debug, Clone, Serialize)]
pub struct Annotation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:object")]
    pub object: Vec<UcoObject>,
}

impl Annotation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Annotation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> AnnotationBuilder {
        AnnotationBuilder {
            object: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AnnotationBuilder {
    object: Vec<UcoObject>,
}

impl AnnotationBuilder {
    pub fn object(mut self, value: Vec<UcoObject>) -> Self {
        self.object = value;
        self
    }

    pub fn build(self) -> Annotation {
        Annotation {
            class_iri: Annotation::CLASS_IRI,
            object: self.object,
        }
    }
}

impl CaseObject for Annotation {
    fn class_iri() -> &'static str { Annotation::CLASS_IRI }
    fn type_name() -> &'static str { "Annotation" }
}

/// An assertion is a statement declared to be true.
#[derive(Debug, Clone, Serialize)]
pub struct Assertion {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:statement")]
    pub statement: Vec<String>,
}

impl Assertion {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Assertion";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> AssertionBuilder {
        AssertionBuilder {
            statement: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AssertionBuilder {
    statement: Vec<String>,
}

impl AssertionBuilder {
    pub fn statement(mut self, value: Vec<String>) -> Self {
        self.statement = value;
        self
    }

    pub fn build(self) -> Assertion {
        Assertion {
            class_iri: Assertion::CLASS_IRI,
            statement: self.statement,
        }
    }
}

impl CaseObject for Assertion {
    fn class_iri() -> &'static str { Assertion::CLASS_IRI }
    fn type_name() -> &'static str { "Assertion" }
}

/// An attributed name is a name of an entity issued by some attributed naming authority.
#[derive(Debug, Clone, Serialize)]
pub struct AttributedName {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:namingAuthority")]
    pub naming_authority: Option<String>,
}

impl AttributedName {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/AttributedName";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> AttributedNameBuilder {
        AttributedNameBuilder {
            naming_authority: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AttributedNameBuilder {
    naming_authority: Option<String>,
}

impl AttributedNameBuilder {
    pub fn naming_authority(mut self, value: String) -> Self {
        self.naming_authority = Some(value);
        self
    }

    pub fn build(self) -> AttributedName {
        AttributedName {
            class_iri: AttributedName::CLASS_IRI,
            naming_authority: self.naming_authority,
        }
    }
}

impl CaseObject for AttributedName {
    fn class_iri() -> &'static str { AttributedName::CLASS_IRI }
    fn type_name() -> &'static str { "AttributedName" }
}

/// A bundle is a container for a grouping of UCO content with no presumption of shared context.
#[derive(Debug, Clone, Serialize)]
pub struct Bundle {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Bundle {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Bundle";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> BundleBuilder {
        BundleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BundleBuilder {
}

impl BundleBuilder {
    pub fn build(self) -> Bundle {
        Bundle {
            class_iri: Bundle::CLASS_IRI,
        }
    }
}

impl CaseObject for Bundle {
    fn class_iri() -> &'static str { Bundle::CLASS_IRI }
    fn type_name() -> &'static str { "Bundle" }
}

/// A compilation is a grouping of things.
#[derive(Debug, Clone, Serialize)]
pub struct Compilation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Compilation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Compilation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> CompilationBuilder {
        CompilationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CompilationBuilder {
}

impl CompilationBuilder {
    pub fn build(self) -> Compilation {
        Compilation {
            class_iri: Compilation::CLASS_IRI,
        }
    }
}

impl CaseObject for Compilation {
    fn class_iri() -> &'static str { Compilation::CLASS_IRI }
    fn type_name() -> &'static str { "Compilation" }
}

/// A confidence is a grouping of characteristics unique to an asserted level of certainty in the accuracy of some information.
#[derive(Debug, Clone, Serialize)]
pub struct ConfidenceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:confidence")]
    pub confidence: u64,
}

impl ConfidenceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/ConfidenceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> ConfidenceFacetBuilder {
        ConfidenceFacetBuilder {
            confidence: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ConfidenceFacetBuilder {
    confidence: Option<u64>,
}

impl ConfidenceFacetBuilder {
    pub fn confidence(mut self, value: u64) -> Self {
        self.confidence = Some(value);
        self
    }

    pub fn build(self) -> ConfidenceFacet {
        ConfidenceFacet {
            class_iri: ConfidenceFacet::CLASS_IRI,
            confidence: self.confidence.expect("missing required field: confidence"),
        }
    }
}

impl CaseObject for ConfidenceFacet {
    fn class_iri() -> &'static str { ConfidenceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ConfidenceFacet" }
}

/// A contextual compilation is a grouping of things sharing some context (e.g., a set of network connections observed on a given day, all accounts associated with a given person).
#[derive(Debug, Clone, Serialize)]
pub struct ContextualCompilation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:object")]
    pub object: Vec<UcoObject>,
}

impl ContextualCompilation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/ContextualCompilation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> ContextualCompilationBuilder {
        ContextualCompilationBuilder {
            object: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContextualCompilationBuilder {
    object: Vec<UcoObject>,
}

impl ContextualCompilationBuilder {
    pub fn object(mut self, value: Vec<UcoObject>) -> Self {
        self.object = value;
        self
    }

    pub fn build(self) -> ContextualCompilation {
        ContextualCompilation {
            class_iri: ContextualCompilation::CLASS_IRI,
            object: self.object,
        }
    }
}

impl CaseObject for ContextualCompilation {
    fn class_iri() -> &'static str { ContextualCompilation::CLASS_IRI }
    fn type_name() -> &'static str { "ContextualCompilation" }
}

/// A controlled vocabulary is an explicitly constrained set of string values.
#[derive(Debug, Clone, Serialize)]
pub struct ControlledVocabulary {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:constrainingVocabularyName")]
    pub constraining_vocabulary_name: Option<String>,
    #[serde(rename = "uco-core:constrainingVocabularyReference")]
    pub constraining_vocabulary_reference: Option<String>,
    #[serde(rename = "uco-core:value")]
    pub value: String,
}

impl ControlledVocabulary {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/ControlledVocabulary";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> ControlledVocabularyBuilder {
        ControlledVocabularyBuilder {
            constraining_vocabulary_name: None,
            constraining_vocabulary_reference: None,
            value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ControlledVocabularyBuilder {
    constraining_vocabulary_name: Option<String>,
    constraining_vocabulary_reference: Option<String>,
    value: Option<String>,
}

impl ControlledVocabularyBuilder {
    pub fn constraining_vocabulary_name(mut self, value: String) -> Self {
        self.constraining_vocabulary_name = Some(value);
        self
    }

    pub fn constraining_vocabulary_reference(mut self, value: String) -> Self {
        self.constraining_vocabulary_reference = Some(value);
        self
    }

    pub fn value(mut self, value: String) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> ControlledVocabulary {
        ControlledVocabulary {
            class_iri: ControlledVocabulary::CLASS_IRI,
            constraining_vocabulary_name: self.constraining_vocabulary_name,
            constraining_vocabulary_reference: self.constraining_vocabulary_reference,
            value: self.value.expect("missing required field: value"),
        }
    }
}

impl CaseObject for ControlledVocabulary {
    fn class_iri() -> &'static str { ControlledVocabulary::CLASS_IRI }
    fn type_name() -> &'static str { "ControlledVocabulary" }
}

/// An enclosing compilation is a container for a grouping of things.
#[derive(Debug, Clone, Serialize)]
pub struct EnclosingCompilation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:object")]
    pub object: Vec<UcoObject>,
}

impl EnclosingCompilation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/EnclosingCompilation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> EnclosingCompilationBuilder {
        EnclosingCompilationBuilder {
            object: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EnclosingCompilationBuilder {
    object: Vec<UcoObject>,
}

impl EnclosingCompilationBuilder {
    pub fn object(mut self, value: Vec<UcoObject>) -> Self {
        self.object = value;
        self
    }

    pub fn build(self) -> EnclosingCompilation {
        EnclosingCompilation {
            class_iri: EnclosingCompilation::CLASS_IRI,
            object: self.object,
        }
    }
}

impl CaseObject for EnclosingCompilation {
    fn class_iri() -> &'static str { EnclosingCompilation::CLASS_IRI }
    fn type_name() -> &'static str { "EnclosingCompilation" }
}

/// An Event is a noteworthy occurrence (something that happens or might happen).
#[derive(Debug, Clone, Serialize)]
pub struct Event {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:endTime")]
    pub end_time: Vec<String>,
    #[serde(rename = "uco-core:eventAttribute")]
    pub event_attribute: Vec<Dictionary>,
    #[serde(rename = "uco-core:eventContext")]
    pub event_context: Vec<UcoObject>,
    #[serde(rename = "uco-core:eventType")]
    pub event_type: Vec<String>,
    #[serde(rename = "uco-core:startTime")]
    pub start_time: Vec<String>,
}

impl Event {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Event";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> EventBuilder {
        EventBuilder {
            end_time: Vec::new(),
            event_attribute: Vec::new(),
            event_context: Vec::new(),
            event_type: Vec::new(),
            start_time: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EventBuilder {
    end_time: Vec<String>,
    event_attribute: Vec<Dictionary>,
    event_context: Vec<UcoObject>,
    event_type: Vec<String>,
    start_time: Vec<String>,
}

impl EventBuilder {
    pub fn end_time(mut self, value: Vec<String>) -> Self {
        self.end_time = value;
        self
    }

    pub fn event_attribute(mut self, value: Vec<Dictionary>) -> Self {
        self.event_attribute = value;
        self
    }

    pub fn event_context(mut self, value: Vec<UcoObject>) -> Self {
        self.event_context = value;
        self
    }

    pub fn event_type(mut self, value: Vec<String>) -> Self {
        self.event_type = value;
        self
    }

    pub fn start_time(mut self, value: Vec<String>) -> Self {
        self.start_time = value;
        self
    }

    pub fn build(self) -> Event {
        Event {
            class_iri: Event::CLASS_IRI,
            end_time: self.end_time,
            event_attribute: self.event_attribute,
            event_context: self.event_context,
            event_type: self.event_type,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for Event {
    fn class_iri() -> &'static str { Event::CLASS_IRI }
    fn type_name() -> &'static str { "Event" }
}

/// Characteristics of a reference to a resource outside of the UCO.
#[derive(Debug, Clone, Serialize)]
pub struct ExternalReference {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:definingContext")]
    pub defining_context: Option<String>,
    #[serde(rename = "uco-core:externalIdentifier")]
    pub external_identifier: Option<String>,
    #[serde(rename = "uco-core:referenceURL")]
    pub reference_url: Option<String>,
}

impl ExternalReference {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/ExternalReference";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> ExternalReferenceBuilder {
        ExternalReferenceBuilder {
            defining_context: None,
            external_identifier: None,
            reference_url: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ExternalReferenceBuilder {
    defining_context: Option<String>,
    external_identifier: Option<String>,
    reference_url: Option<String>,
}

impl ExternalReferenceBuilder {
    pub fn defining_context(mut self, value: String) -> Self {
        self.defining_context = Some(value);
        self
    }

    pub fn external_identifier(mut self, value: String) -> Self {
        self.external_identifier = Some(value);
        self
    }

    pub fn reference_url(mut self, value: String) -> Self {
        self.reference_url = Some(value);
        self
    }

    pub fn build(self) -> ExternalReference {
        ExternalReference {
            class_iri: ExternalReference::CLASS_IRI,
            defining_context: self.defining_context,
            external_identifier: self.external_identifier,
            reference_url: self.reference_url,
        }
    }
}

impl CaseObject for ExternalReference {
    fn class_iri() -> &'static str { ExternalReference::CLASS_IRI }
    fn type_name() -> &'static str { "ExternalReference" }
}

/// A facet is a grouping of characteristics singularly unique to a particular inherent aspect of a UCO domain object.
#[derive(Debug, Clone, Serialize)]
pub struct Facet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Facet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Facet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> FacetBuilder {
        FacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FacetBuilder {
}

impl FacetBuilder {
    pub fn build(self) -> Facet {
        Facet {
            class_iri: Facet::CLASS_IRI,
        }
    }
}

impl CaseObject for Facet {
    fn class_iri() -> &'static str { Facet::CLASS_IRI }
    fn type_name() -> &'static str { "Facet" }
}

/// A grouping is a compilation of referenced UCO content with a shared context.
#[derive(Debug, Clone, Serialize)]
pub struct Grouping {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:context")]
    pub context: Vec<String>,
}

impl Grouping {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Grouping";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> GroupingBuilder {
        GroupingBuilder {
            context: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GroupingBuilder {
    context: Vec<String>,
}

impl GroupingBuilder {
    pub fn context(mut self, value: Vec<String>) -> Self {
        self.context = value;
        self
    }

    pub fn build(self) -> Grouping {
        Grouping {
            class_iri: Grouping::CLASS_IRI,
            context: self.context,
        }
    }
}

impl CaseObject for Grouping {
    fn class_iri() -> &'static str { Grouping::CLASS_IRI }
    fn type_name() -> &'static str { "Grouping" }
}

/// An identity abstraction is a grouping of identifying characteristics unique to an individual or organization. This class is an ontological structural abstraction for this concept. Implementations of t
#[derive(Debug, Clone, Serialize)]
pub struct IdentityAbstraction {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IdentityAbstraction {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/IdentityAbstraction";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> IdentityAbstractionBuilder {
        IdentityAbstractionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IdentityAbstractionBuilder {
}

impl IdentityAbstractionBuilder {
    pub fn build(self) -> IdentityAbstraction {
        IdentityAbstraction {
            class_iri: IdentityAbstraction::CLASS_IRI,
        }
    }
}

impl CaseObject for IdentityAbstraction {
    fn class_iri() -> &'static str { IdentityAbstraction::CLASS_IRI }
    fn type_name() -> &'static str { "IdentityAbstraction" }
}

/// An item is a distinct article or unit.
#[derive(Debug, Clone, Serialize)]
pub struct Item {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Item {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Item";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> ItemBuilder {
        ItemBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ItemBuilder {
}

impl ItemBuilder {
    pub fn build(self) -> Item {
        Item {
            class_iri: Item::CLASS_IRI,
        }
    }
}

impl CaseObject for Item {
    fn class_iri() -> &'static str { Item::CLASS_IRI }
    fn type_name() -> &'static str { "Item" }
}

/// A marking definition abstraction is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be
#[derive(Debug, Clone, Serialize)]
pub struct MarkingDefinitionAbstraction {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MarkingDefinitionAbstraction {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/MarkingDefinitionAbstraction";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> MarkingDefinitionAbstractionBuilder {
        MarkingDefinitionAbstractionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MarkingDefinitionAbstractionBuilder {
}

impl MarkingDefinitionAbstractionBuilder {
    pub fn build(self) -> MarkingDefinitionAbstraction {
        MarkingDefinitionAbstraction {
            class_iri: MarkingDefinitionAbstraction::CLASS_IRI,
        }
    }
}

impl CaseObject for MarkingDefinitionAbstraction {
    fn class_iri() -> &'static str { MarkingDefinitionAbstraction::CLASS_IRI }
    fn type_name() -> &'static str { "MarkingDefinitionAbstraction" }
}

/// A modus operandi is a particular method of operation (how a particular entity behaves or the resources they use).
#[derive(Debug, Clone, Serialize)]
pub struct ModusOperandi {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ModusOperandi {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/ModusOperandi";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> ModusOperandiBuilder {
        ModusOperandiBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ModusOperandiBuilder {
}

impl ModusOperandiBuilder {
    pub fn build(self) -> ModusOperandi {
        ModusOperandi {
            class_iri: ModusOperandi::CLASS_IRI,
        }
    }
}

impl CaseObject for ModusOperandi {
    fn class_iri() -> &'static str { ModusOperandi::CLASS_IRI }
    fn type_name() -> &'static str { "ModusOperandi" }
}

/// A relationship is a grouping of characteristics unique to an assertion that one or more objects are related to another object in some way.
#[derive(Debug, Clone, Serialize)]
pub struct Relationship {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:endTime")]
    pub end_time: Vec<String>,
    #[serde(rename = "uco-core:isDirectional")]
    pub is_directional: bool,
    #[serde(rename = "uco-core:kindOfRelationship")]
    pub kind_of_relationship: Option<String>,
    #[serde(rename = "uco-core:source")]
    pub source: Vec<UcoObject>,
    #[serde(rename = "uco-core:startTime")]
    pub start_time: Vec<String>,
    #[serde(rename = "uco-core:target")]
    pub target: UcoObject,
}

impl Relationship {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/Relationship";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> RelationshipBuilder {
        RelationshipBuilder {
            end_time: Vec::new(),
            is_directional: None,
            kind_of_relationship: None,
            source: Vec::new(),
            start_time: Vec::new(),
            target: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RelationshipBuilder {
    end_time: Vec<String>,
    is_directional: Option<bool>,
    kind_of_relationship: Option<String>,
    source: Vec<UcoObject>,
    start_time: Vec<String>,
    target: Option<UcoObject>,
}

impl RelationshipBuilder {
    pub fn end_time(mut self, value: Vec<String>) -> Self {
        self.end_time = value;
        self
    }

    pub fn is_directional(mut self, value: bool) -> Self {
        self.is_directional = Some(value);
        self
    }

    pub fn kind_of_relationship(mut self, value: String) -> Self {
        self.kind_of_relationship = Some(value);
        self
    }

    pub fn source(mut self, value: Vec<UcoObject>) -> Self {
        self.source = value;
        self
    }

    pub fn start_time(mut self, value: Vec<String>) -> Self {
        self.start_time = value;
        self
    }

    pub fn target(mut self, value: UcoObject) -> Self {
        self.target = Some(value);
        self
    }

    pub fn build(self) -> Relationship {
        Relationship {
            class_iri: Relationship::CLASS_IRI,
            end_time: self.end_time,
            is_directional: self.is_directional.expect("missing required field: is_directional"),
            kind_of_relationship: self.kind_of_relationship,
            source: self.source,
            start_time: self.start_time,
            target: self.target.expect("missing required field: target"),
        }
    }
}

impl CaseObject for Relationship {
    fn class_iri() -> &'static str { Relationship::CLASS_IRI }
    fn type_name() -> &'static str { "Relationship" }
}

/// A UCO inherent characterization thing is a grouping of characteristics unique to a particular inherent aspect of a UCO domain object.
#[derive(Debug, Clone, Serialize)]
pub struct UcoInherentCharacterizationThing {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UcoInherentCharacterizationThing {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/UcoInherentCharacterizationThing";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> UcoInherentCharacterizationThingBuilder {
        UcoInherentCharacterizationThingBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UcoInherentCharacterizationThingBuilder {
}

impl UcoInherentCharacterizationThingBuilder {
    pub fn build(self) -> UcoInherentCharacterizationThing {
        UcoInherentCharacterizationThing {
            class_iri: UcoInherentCharacterizationThing::CLASS_IRI,
        }
    }
}

impl CaseObject for UcoInherentCharacterizationThing {
    fn class_iri() -> &'static str { UcoInherentCharacterizationThing::CLASS_IRI }
    fn type_name() -> &'static str { "UcoInherentCharacterizationThing" }
}

/// A UCO object is a representation of a fundamental concept either directly inherent to the cyber domain or indirectly related to the cyber domain and necessary for contextually characterizing cyber dom
#[derive(Debug, Clone, Serialize)]
pub struct UcoObject {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:createdBy")]
    pub created_by: Option<IdentityAbstraction>,
    #[serde(rename = "uco-core:description")]
    pub description: Vec<String>,
    #[serde(rename = "uco-core:externalReference")]
    pub external_reference: Vec<ExternalReference>,
    #[serde(rename = "uco-core:hasFacet")]
    pub has_facet: Vec<Facet>,
    #[serde(rename = "uco-core:modifiedTime")]
    pub modified_time: Vec<String>,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-core:objectCreatedTime")]
    pub object_created_time: Option<String>,
    #[serde(rename = "uco-core:objectMarking")]
    pub object_marking: Vec<MarkingDefinitionAbstraction>,
    #[serde(rename = "uco-core:objectStatus")]
    pub object_status: Option<String>,
    #[serde(rename = "uco-core:specVersion")]
    pub spec_version: Option<String>,
    #[serde(rename = "uco-core:tag")]
    pub tag: Vec<String>,
}

impl UcoObject {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/UcoObject";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> UcoObjectBuilder {
        UcoObjectBuilder {
            created_by: None,
            description: Vec::new(),
            external_reference: Vec::new(),
            has_facet: Vec::new(),
            modified_time: Vec::new(),
            name: None,
            object_created_time: None,
            object_marking: Vec::new(),
            object_status: None,
            spec_version: None,
            tag: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UcoObjectBuilder {
    created_by: Option<IdentityAbstraction>,
    description: Vec<String>,
    external_reference: Vec<ExternalReference>,
    has_facet: Vec<Facet>,
    modified_time: Vec<String>,
    name: Option<String>,
    object_created_time: Option<String>,
    object_marking: Vec<MarkingDefinitionAbstraction>,
    object_status: Option<String>,
    spec_version: Option<String>,
    tag: Vec<String>,
}

impl UcoObjectBuilder {
    pub fn created_by(mut self, value: IdentityAbstraction) -> Self {
        self.created_by = Some(value);
        self
    }

    pub fn description(mut self, value: Vec<String>) -> Self {
        self.description = value;
        self
    }

    pub fn external_reference(mut self, value: Vec<ExternalReference>) -> Self {
        self.external_reference = value;
        self
    }

    pub fn has_facet(mut self, value: Vec<Facet>) -> Self {
        self.has_facet = value;
        self
    }

    pub fn modified_time(mut self, value: Vec<String>) -> Self {
        self.modified_time = value;
        self
    }

    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn object_created_time(mut self, value: String) -> Self {
        self.object_created_time = Some(value);
        self
    }

    pub fn object_marking(mut self, value: Vec<MarkingDefinitionAbstraction>) -> Self {
        self.object_marking = value;
        self
    }

    pub fn object_status(mut self, value: String) -> Self {
        self.object_status = Some(value);
        self
    }

    pub fn spec_version(mut self, value: String) -> Self {
        self.spec_version = Some(value);
        self
    }

    pub fn tag(mut self, value: Vec<String>) -> Self {
        self.tag = value;
        self
    }

    pub fn build(self) -> UcoObject {
        UcoObject {
            class_iri: UcoObject::CLASS_IRI,
            created_by: self.created_by,
            description: self.description,
            external_reference: self.external_reference,
            has_facet: self.has_facet,
            modified_time: self.modified_time,
            name: self.name,
            object_created_time: self.object_created_time,
            object_marking: self.object_marking,
            object_status: self.object_status,
            spec_version: self.spec_version,
            tag: self.tag,
        }
    }
}

impl CaseObject for UcoObject {
    fn class_iri() -> &'static str { UcoObject::CLASS_IRI }
    fn type_name() -> &'static str { "UcoObject" }
}

/// UcoThing is the top-level class within UCO.
#[derive(Debug, Clone, Serialize)]
pub struct UcoThing {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UcoThing {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/UcoThing";
    pub const NAMESPACE_PREFIX: &'static str = "uco-core";

    pub fn builder() -> UcoThingBuilder {
        UcoThingBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UcoThingBuilder {
}

impl UcoThingBuilder {
    pub fn build(self) -> UcoThing {
        UcoThing {
            class_iri: UcoThing::CLASS_IRI,
        }
    }
}

impl CaseObject for UcoThing {
    fn class_iri() -> &'static str { UcoThing::CLASS_IRI }
    fn type_name() -> &'static str { "UcoThing" }
}
