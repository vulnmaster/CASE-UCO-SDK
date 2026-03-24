"""Auto-generated uco-identity classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from case_uco.uco.core import Facet
from case_uco.uco.core import IdentityAbstraction

if TYPE_CHECKING:
    from case_uco.uco.location import Location


@dataclass
class IdentityFacet(Facet):
    """An identity facet is a grouping of characteristics unique to a particular aspect of an identity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/IdentityFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class AddressFacet(IdentityFacet):
    """An address facet is a grouping of characteristics unique to an administrative identifier for a geolocation associated with a specific identity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/AddressFacet"
    NAMESPACE_PREFIX: str = "uco-identity"

    address: Optional[Location] = field(default=None, metadata={'jsonld_key': 'uco-identity:address', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})


@dataclass
class AffiliationFacet(IdentityFacet):
    """An affiliation is a grouping of characteristics unique to the established affiliations of an entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/AffiliationFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class BirthInformationFacet(IdentityFacet):
    """Birth information is a grouping of characteristics unique to information pertaining to the birth of an entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/BirthInformationFacet"
    NAMESPACE_PREFIX: str = "uco-identity"

    birthdate: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-identity:birthdate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class CountryOfResidenceFacet(IdentityFacet):
    """Country of residence is a grouping of characteristics unique to information related to the country, or countries, where an entity resides."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/CountryOfResidenceFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class EventsFacet(IdentityFacet):
    """Events is a grouping of characteristics unique to information related to specific relevant things that happen in the lifetime of an entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/EventsFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class IdentifierFacet(IdentityFacet):
    """Identifier is a grouping of characteristics unique to information that uniquely and specifically identities an entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/IdentifierFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class Identity(IdentityAbstraction):
    """An identity is a grouping of identifying characteristics unique to an individual or organization."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/Identity"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class LanguagesFacet(IdentityFacet):
    """Languages is a grouping of characteristics unique to specific syntactically and grammatically standardized forms of communication (human or computer) in which an entity has proficiency (comprehends, s"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/LanguagesFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class NationalityFacet(IdentityFacet):
    """Nationality is a grouping of characteristics unique to the condition of an entity belonging to a particular nation."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/NationalityFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class OccupationFacet(IdentityFacet):
    """Occupation is a grouping of characteristics unique to the job or profession of an entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/OccupationFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class Organization(Identity):
    """An organization is a grouping of identifying characteristics unique to a group of people who work together in an organized way for a shared purpose. [based on https://dictionary.cambridge.org/us/dicti"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/Organization"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class OrganizationDetailsFacet(IdentityFacet):
    """Organization details is a grouping of characteristics unique to an identity representing an administrative and functional structure."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/OrganizationDetailsFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class Person(Identity):
    """A person is a grouping of identifying characteristics unique to a human being regarded as an individual. [based on https://www.lexico.com/en/definition/person]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/Person"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class PersonalDetailsFacet(IdentityFacet):
    """Personal details is a grouping of characteristics unique to an identity representing an individual person."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/PersonalDetailsFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class PhysicalInfoFacet(IdentityFacet):
    """Physical info is a grouping of characteristics unique to the outwardly observable nature of an individual person."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/PhysicalInfoFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class QualificationFacet(IdentityFacet):
    """Qualification is a grouping of characteristics unique to particular skills, capabilities or their related achievements (educational, professional, etc.) of an entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/QualificationFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class RelatedIdentityFacet(IdentityFacet):
    """<Needs fleshed out from CIQ>"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/RelatedIdentityFacet"
    NAMESPACE_PREFIX: str = "uco-identity"



@dataclass
class SimpleNameFacet(IdentityFacet):
    """A simple name facet is a grouping of characteristics unique to the personal name (e.g., Dr. John Smith Jr.) held by an identity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/SimpleNameFacet"
    NAMESPACE_PREFIX: str = "uco-identity"

    family_name: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-identity:familyName', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    given_name: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-identity:givenName', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    honorific_prefix: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-identity:honorificPrefix', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    honorific_suffix: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-identity:honorificSuffix', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class VisaFacet(IdentityFacet):
    """Visa is a grouping of characteristics unique to information related to a person's ability to enter, leave, or stay for a specified period of time in a country."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/identity/VisaFacet"
    NAMESPACE_PREFIX: str = "uco-identity"


