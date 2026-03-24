// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-identity

using System.Collections.Generic;

namespace CaseUco.Uco.Identity
{
    /// <summary>An address facet is a grouping of characteristics unique to an administrative identifier for a geolocation associated with a specific identity.</summary>
    public class AddressFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/AddressFacet";
        public new const string NamespacePrefix = "uco-identity";
        [global::CaseUco.JsonLdProperty("uco-identity:address")]
        public CaseUco.Uco.Location.Location Address { get; set; }
    }

    /// <summary>An affiliation is a grouping of characteristics unique to the established affiliations of an entity.</summary>
    public class AffiliationFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/AffiliationFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Birth information is a grouping of characteristics unique to information pertaining to the birth of an entity.</summary>
    public class BirthInformationFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/BirthInformationFacet";
        public new const string NamespacePrefix = "uco-identity";
        [global::CaseUco.JsonLdProperty("uco-identity:birthdate")]
        public System.DateTime? Birthdate { get; set; }
    }

    /// <summary>Country of residence is a grouping of characteristics unique to information related to the country, or countries, where an entity resides.</summary>
    public class CountryOfResidenceFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/CountryOfResidenceFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Events is a grouping of characteristics unique to information related to specific relevant things that happen in the lifetime of an entity.</summary>
    public class EventsFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/EventsFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Identifier is a grouping of characteristics unique to information that uniquely and specifically identities an entity.</summary>
    public class IdentifierFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/IdentifierFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>An identity is a grouping of identifying characteristics unique to an individual or organization.</summary>
    public class Identity : CaseUco.Uco.Core.IdentityAbstraction
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/Identity";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>An identity facet is a grouping of characteristics unique to a particular aspect of an identity.</summary>
    public class IdentityFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/IdentityFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Languages is a grouping of characteristics unique to specific syntactically and grammatically standardized forms of communication (human or computer) in which an entity has proficiency (comprehends, s</summary>
    public class LanguagesFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/LanguagesFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Nationality is a grouping of characteristics unique to the condition of an entity belonging to a particular nation.</summary>
    public class NationalityFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/NationalityFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Occupation is a grouping of characteristics unique to the job or profession of an entity.</summary>
    public class OccupationFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/OccupationFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>An organization is a grouping of identifying characteristics unique to a group of people who work together in an organized way for a shared purpose. [based on https://dictionary.cambridge.org/us/dicti</summary>
    public class Organization : CaseUco.Uco.Identity.Identity
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/Organization";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Organization details is a grouping of characteristics unique to an identity representing an administrative and functional structure.</summary>
    public class OrganizationDetailsFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/OrganizationDetailsFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>A person is a grouping of identifying characteristics unique to a human being regarded as an individual. [based on https://www.lexico.com/en/definition/person]</summary>
    public class Person : CaseUco.Uco.Identity.Identity
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/Person";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Personal details is a grouping of characteristics unique to an identity representing an individual person.</summary>
    public class PersonalDetailsFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/PersonalDetailsFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Physical info is a grouping of characteristics unique to the outwardly observable nature of an individual person.</summary>
    public class PhysicalInfoFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/PhysicalInfoFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>Qualification is a grouping of characteristics unique to particular skills, capabilities or their related achievements (educational, professional, etc.) of an entity.</summary>
    public class QualificationFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/QualificationFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary><Needs fleshed out from CIQ></summary>
    public class RelatedIdentityFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/RelatedIdentityFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

    /// <summary>A simple name facet is a grouping of characteristics unique to the personal name (e.g., Dr. John Smith Jr.) held by an identity.</summary>
    public class SimpleNameFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/SimpleNameFacet";
        public new const string NamespacePrefix = "uco-identity";
        [global::CaseUco.JsonLdProperty("uco-identity:familyName")]
        public List<string> FamilyName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-identity:givenName")]
        public List<string> GivenName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-identity:honorificPrefix")]
        public List<string> HonorificPrefix { get; set; }
        [global::CaseUco.JsonLdProperty("uco-identity:honorificSuffix")]
        public List<string> HonorificSuffix { get; set; }
    }

    /// <summary>Visa is a grouping of characteristics unique to information related to a person's ability to enter, leave, or stay for a specified period of time in a country.</summary>
    public class VisaFacet : CaseUco.Uco.Identity.IdentityFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/identity/VisaFacet";
        public new const string NamespacePrefix = "uco-identity";
    }

}