// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-location

using System.Collections.Generic;

namespace CaseUco.Uco.Location
{
    /// <summary>A GPS coordinates facet is a grouping of characteristics unique to the expression of quantified dilution of precision (DOP) for an asserted set of geolocation coordinates typically associated with sat</summary>
    public class GPSCoordinatesFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/location/GPSCoordinatesFacet";
        public new const string NamespacePrefix = "uco-location";
        [global::CaseUco.JsonLdProperty("uco-location:hdop")]
        public decimal? Hdop { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:pdop")]
        public decimal? Pdop { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:tdop")]
        public decimal? Tdop { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:vdop")]
        public decimal? Vdop { get; set; }
    }

    /// <summary>A lat long coordinates facet is a grouping of characteristics unique to the expression of a geolocation as the intersection of specific latitude, longitude, and altitude values.</summary>
    public class LatLongCoordinatesFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/location/LatLongCoordinatesFacet";
        public new const string NamespacePrefix = "uco-location";
        [global::CaseUco.JsonLdProperty("uco-location:altitude")]
        public decimal? Altitude { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:latitude")]
        public decimal? Latitude { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:longitude")]
        public decimal? Longitude { get; set; }
    }

    /// <summary>A location is a geospatial place, site, or position.</summary>
    public class Location : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/location/Location";
        public new const string NamespacePrefix = "uco-location";
    }

    /// <summary>A simple address facet is a grouping of characteristics unique to a geolocation expressed as an administrative address.</summary>
    public class SimpleAddressFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/location/SimpleAddressFacet";
        public new const string NamespacePrefix = "uco-location";
        [global::CaseUco.JsonLdProperty("uco-location:addressType")]
        public string AddressType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:country")]
        public string Country { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:locality")]
        public string Locality { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:postalCode")]
        public string PostalCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:region")]
        public string Region { get; set; }
        [global::CaseUco.JsonLdProperty("uco-location:street")]
        public string Street { get; set; }
    }

}