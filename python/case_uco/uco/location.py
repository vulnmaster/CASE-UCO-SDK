"""Auto-generated uco-location classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from case_uco.uco.core import Facet
from case_uco.uco.core import UcoObject


@dataclass
class GPSCoordinatesFacet(Facet):
    """A GPS coordinates facet is a grouping of characteristics unique to the expression of quantified dilution of precision (DOP) for an asserted set of geolocation coordinates typically associated with sat"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/location/GPSCoordinatesFacet"
    NAMESPACE_PREFIX: str = "uco-location"

    hdop: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:hdop', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    pdop: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:pdop', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    tdop: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:tdop', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    vdop: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:vdop', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})


@dataclass
class LatLongCoordinatesFacet(Facet):
    """A lat long coordinates facet is a grouping of characteristics unique to the expression of a geolocation as the intersection of specific latitude, longitude, and altitude values."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/location/LatLongCoordinatesFacet"
    NAMESPACE_PREFIX: str = "uco-location"

    altitude: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:altitude', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    latitude: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:latitude', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    longitude: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-location:longitude', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})


@dataclass
class Location(UcoObject):
    """A location is a geospatial place, site, or position."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/location/Location"
    NAMESPACE_PREFIX: str = "uco-location"



@dataclass
class SimpleAddressFacet(Facet):
    """A simple address facet is a grouping of characteristics unique to a geolocation expressed as an administrative address."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/location/SimpleAddressFacet"
    NAMESPACE_PREFIX: str = "uco-location"

    address_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-location:addressType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    country: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-location:country', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    locality: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-location:locality', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    postal_code: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-location:postalCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    region: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-location:region', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    street: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-location:street', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})

