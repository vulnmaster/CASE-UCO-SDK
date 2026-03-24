//! Auto-generated uco-location types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// A GPS coordinates facet is a grouping of characteristics unique to the expression of quantified dilution of precision (DOP) for an asserted set of geolocation coordinates typically associated with sat
#[derive(Debug, Clone, Serialize)]
pub struct GPSCoordinatesFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-location:hdop")]
    pub hdop: Option<f64>,
    #[serde(rename = "uco-location:pdop")]
    pub pdop: Option<f64>,
    #[serde(rename = "uco-location:tdop")]
    pub tdop: Option<f64>,
    #[serde(rename = "uco-location:vdop")]
    pub vdop: Option<f64>,
}

impl GPSCoordinatesFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/location/GPSCoordinatesFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-location";

    pub fn builder() -> GPSCoordinatesFacetBuilder {
        GPSCoordinatesFacetBuilder {
            hdop: None,
            pdop: None,
            tdop: None,
            vdop: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GPSCoordinatesFacetBuilder {
    hdop: Option<f64>,
    pdop: Option<f64>,
    tdop: Option<f64>,
    vdop: Option<f64>,
}

impl GPSCoordinatesFacetBuilder {
    pub fn hdop(mut self, value: f64) -> Self {
        self.hdop = Some(value);
        self
    }

    pub fn pdop(mut self, value: f64) -> Self {
        self.pdop = Some(value);
        self
    }

    pub fn tdop(mut self, value: f64) -> Self {
        self.tdop = Some(value);
        self
    }

    pub fn vdop(mut self, value: f64) -> Self {
        self.vdop = Some(value);
        self
    }

    pub fn build(self) -> GPSCoordinatesFacet {
        GPSCoordinatesFacet {
            class_iri: GPSCoordinatesFacet::CLASS_IRI,
            hdop: self.hdop,
            pdop: self.pdop,
            tdop: self.tdop,
            vdop: self.vdop,
        }
    }
}

impl CaseObject for GPSCoordinatesFacet {
    fn class_iri() -> &'static str { GPSCoordinatesFacet::CLASS_IRI }
    fn type_name() -> &'static str { "GPSCoordinatesFacet" }
}

/// A lat long coordinates facet is a grouping of characteristics unique to the expression of a geolocation as the intersection of specific latitude, longitude, and altitude values.
#[derive(Debug, Clone, Serialize)]
pub struct LatLongCoordinatesFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-location:altitude")]
    pub altitude: Option<f64>,
    #[serde(rename = "uco-location:latitude")]
    pub latitude: Option<f64>,
    #[serde(rename = "uco-location:longitude")]
    pub longitude: Option<f64>,
}

impl LatLongCoordinatesFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/location/LatLongCoordinatesFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-location";

    pub fn builder() -> LatLongCoordinatesFacetBuilder {
        LatLongCoordinatesFacetBuilder {
            altitude: None,
            latitude: None,
            longitude: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LatLongCoordinatesFacetBuilder {
    altitude: Option<f64>,
    latitude: Option<f64>,
    longitude: Option<f64>,
}

impl LatLongCoordinatesFacetBuilder {
    pub fn altitude(mut self, value: f64) -> Self {
        self.altitude = Some(value);
        self
    }

    pub fn latitude(mut self, value: f64) -> Self {
        self.latitude = Some(value);
        self
    }

    pub fn longitude(mut self, value: f64) -> Self {
        self.longitude = Some(value);
        self
    }

    pub fn build(self) -> LatLongCoordinatesFacet {
        LatLongCoordinatesFacet {
            class_iri: LatLongCoordinatesFacet::CLASS_IRI,
            altitude: self.altitude,
            latitude: self.latitude,
            longitude: self.longitude,
        }
    }
}

impl CaseObject for LatLongCoordinatesFacet {
    fn class_iri() -> &'static str { LatLongCoordinatesFacet::CLASS_IRI }
    fn type_name() -> &'static str { "LatLongCoordinatesFacet" }
}

/// A location is a geospatial place, site, or position.
#[derive(Debug, Clone, Serialize)]
pub struct Location {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Location {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/location/Location";
    pub const NAMESPACE_PREFIX: &'static str = "uco-location";

    pub fn builder() -> LocationBuilder {
        LocationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LocationBuilder {
}

impl LocationBuilder {
    pub fn build(self) -> Location {
        Location {
            class_iri: Location::CLASS_IRI,
        }
    }
}

impl CaseObject for Location {
    fn class_iri() -> &'static str { Location::CLASS_IRI }
    fn type_name() -> &'static str { "Location" }
}

/// A simple address facet is a grouping of characteristics unique to a geolocation expressed as an administrative address.
#[derive(Debug, Clone, Serialize)]
pub struct SimpleAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-location:addressType")]
    pub address_type: Option<String>,
    #[serde(rename = "uco-location:country")]
    pub country: Option<String>,
    #[serde(rename = "uco-location:locality")]
    pub locality: Option<String>,
    #[serde(rename = "uco-location:postalCode")]
    pub postal_code: Option<String>,
    #[serde(rename = "uco-location:region")]
    pub region: Option<String>,
    #[serde(rename = "uco-location:street")]
    pub street: Option<String>,
}

impl SimpleAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/location/SimpleAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-location";

    pub fn builder() -> SimpleAddressFacetBuilder {
        SimpleAddressFacetBuilder {
            address_type: None,
            country: None,
            locality: None,
            postal_code: None,
            region: None,
            street: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SimpleAddressFacetBuilder {
    address_type: Option<String>,
    country: Option<String>,
    locality: Option<String>,
    postal_code: Option<String>,
    region: Option<String>,
    street: Option<String>,
}

impl SimpleAddressFacetBuilder {
    pub fn address_type(mut self, value: String) -> Self {
        self.address_type = Some(value);
        self
    }

    pub fn country(mut self, value: String) -> Self {
        self.country = Some(value);
        self
    }

    pub fn locality(mut self, value: String) -> Self {
        self.locality = Some(value);
        self
    }

    pub fn postal_code(mut self, value: String) -> Self {
        self.postal_code = Some(value);
        self
    }

    pub fn region(mut self, value: String) -> Self {
        self.region = Some(value);
        self
    }

    pub fn street(mut self, value: String) -> Self {
        self.street = Some(value);
        self
    }

    pub fn build(self) -> SimpleAddressFacet {
        SimpleAddressFacet {
            class_iri: SimpleAddressFacet::CLASS_IRI,
            address_type: self.address_type,
            country: self.country,
            locality: self.locality,
            postal_code: self.postal_code,
            region: self.region,
            street: self.street,
        }
    }
}

impl CaseObject for SimpleAddressFacet {
    fn class_iri() -> &'static str { SimpleAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SimpleAddressFacet" }
}
