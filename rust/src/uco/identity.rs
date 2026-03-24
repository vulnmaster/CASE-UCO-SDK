//! Auto-generated uco-identity types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

use crate::uco::location::Location;

/// An address facet is a grouping of characteristics unique to an administrative identifier for a geolocation associated with a specific identity.
#[derive(Debug, Clone, Serialize)]
pub struct AddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-identity:address")]
    pub address: Option<Location>,
}

impl AddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/AddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> AddressFacetBuilder {
        AddressFacetBuilder {
            address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AddressFacetBuilder {
    address: Option<Location>,
}

impl AddressFacetBuilder {
    pub fn address(mut self, value: Location) -> Self {
        self.address = Some(value);
        self
    }

    pub fn build(self) -> AddressFacet {
        AddressFacet {
            class_iri: AddressFacet::CLASS_IRI,
            address: self.address,
        }
    }
}

impl CaseObject for AddressFacet {
    fn class_iri() -> &'static str { AddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AddressFacet" }
}

/// An affiliation is a grouping of characteristics unique to the established affiliations of an entity.
#[derive(Debug, Clone, Serialize)]
pub struct AffiliationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AffiliationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/AffiliationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> AffiliationFacetBuilder {
        AffiliationFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AffiliationFacetBuilder {
}

impl AffiliationFacetBuilder {
    pub fn build(self) -> AffiliationFacet {
        AffiliationFacet {
            class_iri: AffiliationFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for AffiliationFacet {
    fn class_iri() -> &'static str { AffiliationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AffiliationFacet" }
}

/// Birth information is a grouping of characteristics unique to information pertaining to the birth of an entity.
#[derive(Debug, Clone, Serialize)]
pub struct BirthInformationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-identity:birthdate")]
    pub birthdate: Option<String>,
}

impl BirthInformationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/BirthInformationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> BirthInformationFacetBuilder {
        BirthInformationFacetBuilder {
            birthdate: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BirthInformationFacetBuilder {
    birthdate: Option<String>,
}

impl BirthInformationFacetBuilder {
    pub fn birthdate(mut self, value: String) -> Self {
        self.birthdate = Some(value);
        self
    }

    pub fn build(self) -> BirthInformationFacet {
        BirthInformationFacet {
            class_iri: BirthInformationFacet::CLASS_IRI,
            birthdate: self.birthdate,
        }
    }
}

impl CaseObject for BirthInformationFacet {
    fn class_iri() -> &'static str { BirthInformationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "BirthInformationFacet" }
}

/// Country of residence is a grouping of characteristics unique to information related to the country, or countries, where an entity resides.
#[derive(Debug, Clone, Serialize)]
pub struct CountryOfResidenceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CountryOfResidenceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/CountryOfResidenceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> CountryOfResidenceFacetBuilder {
        CountryOfResidenceFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CountryOfResidenceFacetBuilder {
}

impl CountryOfResidenceFacetBuilder {
    pub fn build(self) -> CountryOfResidenceFacet {
        CountryOfResidenceFacet {
            class_iri: CountryOfResidenceFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for CountryOfResidenceFacet {
    fn class_iri() -> &'static str { CountryOfResidenceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CountryOfResidenceFacet" }
}

/// Events is a grouping of characteristics unique to information related to specific relevant things that happen in the lifetime of an entity.
#[derive(Debug, Clone, Serialize)]
pub struct EventsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EventsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/EventsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> EventsFacetBuilder {
        EventsFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EventsFacetBuilder {
}

impl EventsFacetBuilder {
    pub fn build(self) -> EventsFacet {
        EventsFacet {
            class_iri: EventsFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for EventsFacet {
    fn class_iri() -> &'static str { EventsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EventsFacet" }
}

/// Identifier is a grouping of characteristics unique to information that uniquely and specifically identities an entity.
#[derive(Debug, Clone, Serialize)]
pub struct IdentifierFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IdentifierFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/IdentifierFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> IdentifierFacetBuilder {
        IdentifierFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IdentifierFacetBuilder {
}

impl IdentifierFacetBuilder {
    pub fn build(self) -> IdentifierFacet {
        IdentifierFacet {
            class_iri: IdentifierFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for IdentifierFacet {
    fn class_iri() -> &'static str { IdentifierFacet::CLASS_IRI }
    fn type_name() -> &'static str { "IdentifierFacet" }
}

/// An identity is a grouping of identifying characteristics unique to an individual or organization.
#[derive(Debug, Clone, Serialize)]
pub struct Identity {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Identity {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/Identity";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> IdentityBuilder {
        IdentityBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IdentityBuilder {
}

impl IdentityBuilder {
    pub fn build(self) -> Identity {
        Identity {
            class_iri: Identity::CLASS_IRI,
        }
    }
}

impl CaseObject for Identity {
    fn class_iri() -> &'static str { Identity::CLASS_IRI }
    fn type_name() -> &'static str { "Identity" }
}

/// An identity facet is a grouping of characteristics unique to a particular aspect of an identity.
#[derive(Debug, Clone, Serialize)]
pub struct IdentityFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IdentityFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/IdentityFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> IdentityFacetBuilder {
        IdentityFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IdentityFacetBuilder {
}

impl IdentityFacetBuilder {
    pub fn build(self) -> IdentityFacet {
        IdentityFacet {
            class_iri: IdentityFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for IdentityFacet {
    fn class_iri() -> &'static str { IdentityFacet::CLASS_IRI }
    fn type_name() -> &'static str { "IdentityFacet" }
}

/// Languages is a grouping of characteristics unique to specific syntactically and grammatically standardized forms of communication (human or computer) in which an entity has proficiency (comprehends, s
#[derive(Debug, Clone, Serialize)]
pub struct LanguagesFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl LanguagesFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/LanguagesFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> LanguagesFacetBuilder {
        LanguagesFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LanguagesFacetBuilder {
}

impl LanguagesFacetBuilder {
    pub fn build(self) -> LanguagesFacet {
        LanguagesFacet {
            class_iri: LanguagesFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for LanguagesFacet {
    fn class_iri() -> &'static str { LanguagesFacet::CLASS_IRI }
    fn type_name() -> &'static str { "LanguagesFacet" }
}

/// Nationality is a grouping of characteristics unique to the condition of an entity belonging to a particular nation.
#[derive(Debug, Clone, Serialize)]
pub struct NationalityFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NationalityFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/NationalityFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> NationalityFacetBuilder {
        NationalityFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NationalityFacetBuilder {
}

impl NationalityFacetBuilder {
    pub fn build(self) -> NationalityFacet {
        NationalityFacet {
            class_iri: NationalityFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for NationalityFacet {
    fn class_iri() -> &'static str { NationalityFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NationalityFacet" }
}

/// Occupation is a grouping of characteristics unique to the job or profession of an entity.
#[derive(Debug, Clone, Serialize)]
pub struct OccupationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl OccupationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/OccupationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> OccupationFacetBuilder {
        OccupationFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OccupationFacetBuilder {
}

impl OccupationFacetBuilder {
    pub fn build(self) -> OccupationFacet {
        OccupationFacet {
            class_iri: OccupationFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for OccupationFacet {
    fn class_iri() -> &'static str { OccupationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "OccupationFacet" }
}

/// An organization is a grouping of identifying characteristics unique to a group of people who work together in an organized way for a shared purpose. [based on https://dictionary.cambridge.org/us/dicti
#[derive(Debug, Clone, Serialize)]
pub struct Organization {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Organization {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/Organization";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> OrganizationBuilder {
        OrganizationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OrganizationBuilder {
}

impl OrganizationBuilder {
    pub fn build(self) -> Organization {
        Organization {
            class_iri: Organization::CLASS_IRI,
        }
    }
}

impl CaseObject for Organization {
    fn class_iri() -> &'static str { Organization::CLASS_IRI }
    fn type_name() -> &'static str { "Organization" }
}

/// Organization details is a grouping of characteristics unique to an identity representing an administrative and functional structure.
#[derive(Debug, Clone, Serialize)]
pub struct OrganizationDetailsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl OrganizationDetailsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/OrganizationDetailsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> OrganizationDetailsFacetBuilder {
        OrganizationDetailsFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OrganizationDetailsFacetBuilder {
}

impl OrganizationDetailsFacetBuilder {
    pub fn build(self) -> OrganizationDetailsFacet {
        OrganizationDetailsFacet {
            class_iri: OrganizationDetailsFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for OrganizationDetailsFacet {
    fn class_iri() -> &'static str { OrganizationDetailsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "OrganizationDetailsFacet" }
}

/// A person is a grouping of identifying characteristics unique to a human being regarded as an individual. [based on https://www.lexico.com/en/definition/person]
#[derive(Debug, Clone, Serialize)]
pub struct Person {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Person {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/Person";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> PersonBuilder {
        PersonBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PersonBuilder {
}

impl PersonBuilder {
    pub fn build(self) -> Person {
        Person {
            class_iri: Person::CLASS_IRI,
        }
    }
}

impl CaseObject for Person {
    fn class_iri() -> &'static str { Person::CLASS_IRI }
    fn type_name() -> &'static str { "Person" }
}

/// Personal details is a grouping of characteristics unique to an identity representing an individual person.
#[derive(Debug, Clone, Serialize)]
pub struct PersonalDetailsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl PersonalDetailsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/PersonalDetailsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> PersonalDetailsFacetBuilder {
        PersonalDetailsFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PersonalDetailsFacetBuilder {
}

impl PersonalDetailsFacetBuilder {
    pub fn build(self) -> PersonalDetailsFacet {
        PersonalDetailsFacet {
            class_iri: PersonalDetailsFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for PersonalDetailsFacet {
    fn class_iri() -> &'static str { PersonalDetailsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PersonalDetailsFacet" }
}

/// Physical info is a grouping of characteristics unique to the outwardly observable nature of an individual person.
#[derive(Debug, Clone, Serialize)]
pub struct PhysicalInfoFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl PhysicalInfoFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/PhysicalInfoFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> PhysicalInfoFacetBuilder {
        PhysicalInfoFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PhysicalInfoFacetBuilder {
}

impl PhysicalInfoFacetBuilder {
    pub fn build(self) -> PhysicalInfoFacet {
        PhysicalInfoFacet {
            class_iri: PhysicalInfoFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for PhysicalInfoFacet {
    fn class_iri() -> &'static str { PhysicalInfoFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PhysicalInfoFacet" }
}

/// Qualification is a grouping of characteristics unique to particular skills, capabilities or their related achievements (educational, professional, etc.) of an entity.
#[derive(Debug, Clone, Serialize)]
pub struct QualificationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl QualificationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/QualificationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> QualificationFacetBuilder {
        QualificationFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct QualificationFacetBuilder {
}

impl QualificationFacetBuilder {
    pub fn build(self) -> QualificationFacet {
        QualificationFacet {
            class_iri: QualificationFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for QualificationFacet {
    fn class_iri() -> &'static str { QualificationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "QualificationFacet" }
}

/// <Needs fleshed out from CIQ>
#[derive(Debug, Clone, Serialize)]
pub struct RelatedIdentityFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl RelatedIdentityFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/RelatedIdentityFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> RelatedIdentityFacetBuilder {
        RelatedIdentityFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RelatedIdentityFacetBuilder {
}

impl RelatedIdentityFacetBuilder {
    pub fn build(self) -> RelatedIdentityFacet {
        RelatedIdentityFacet {
            class_iri: RelatedIdentityFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for RelatedIdentityFacet {
    fn class_iri() -> &'static str { RelatedIdentityFacet::CLASS_IRI }
    fn type_name() -> &'static str { "RelatedIdentityFacet" }
}

/// A simple name facet is a grouping of characteristics unique to the personal name (e.g., Dr. John Smith Jr.) held by an identity.
#[derive(Debug, Clone, Serialize)]
pub struct SimpleNameFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-identity:familyName")]
    pub family_name: Vec<String>,
    #[serde(rename = "uco-identity:givenName")]
    pub given_name: Vec<String>,
    #[serde(rename = "uco-identity:honorificPrefix")]
    pub honorific_prefix: Vec<String>,
    #[serde(rename = "uco-identity:honorificSuffix")]
    pub honorific_suffix: Vec<String>,
}

impl SimpleNameFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/SimpleNameFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> SimpleNameFacetBuilder {
        SimpleNameFacetBuilder {
            family_name: Vec::new(),
            given_name: Vec::new(),
            honorific_prefix: Vec::new(),
            honorific_suffix: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SimpleNameFacetBuilder {
    family_name: Vec<String>,
    given_name: Vec<String>,
    honorific_prefix: Vec<String>,
    honorific_suffix: Vec<String>,
}

impl SimpleNameFacetBuilder {
    pub fn family_name(mut self, value: Vec<String>) -> Self {
        self.family_name = value;
        self
    }

    pub fn given_name(mut self, value: Vec<String>) -> Self {
        self.given_name = value;
        self
    }

    pub fn honorific_prefix(mut self, value: Vec<String>) -> Self {
        self.honorific_prefix = value;
        self
    }

    pub fn honorific_suffix(mut self, value: Vec<String>) -> Self {
        self.honorific_suffix = value;
        self
    }

    pub fn build(self) -> SimpleNameFacet {
        SimpleNameFacet {
            class_iri: SimpleNameFacet::CLASS_IRI,
            family_name: self.family_name,
            given_name: self.given_name,
            honorific_prefix: self.honorific_prefix,
            honorific_suffix: self.honorific_suffix,
        }
    }
}

impl CaseObject for SimpleNameFacet {
    fn class_iri() -> &'static str { SimpleNameFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SimpleNameFacet" }
}

/// Visa is a grouping of characteristics unique to information related to a person's ability to enter, leave, or stay for a specified period of time in a country.
#[derive(Debug, Clone, Serialize)]
pub struct VisaFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl VisaFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/identity/VisaFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-identity";

    pub fn builder() -> VisaFacetBuilder {
        VisaFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct VisaFacetBuilder {
}

impl VisaFacetBuilder {
    pub fn build(self) -> VisaFacet {
        VisaFacet {
            class_iri: VisaFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for VisaFacet {
    fn class_iri() -> &'static str { VisaFacet::CLASS_IRI }
    fn type_name() -> &'static str { "VisaFacet" }
}
