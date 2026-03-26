# Location Modeling

> See [Recipe Index](INDEX.md) for all recipes.

Model geospatial locations with street addresses, GPS coordinates, and custom location facets. Based on [CASE-Examples/location](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/location).

## Key classes

| Class | Role |
|---|---|
| `Location` | A geospatial place, site, or position |
| `SimpleAddressFacet` | Street address (street, city, region, postal code, country) |
| `LatLongCoordinatesFacet` | GPS coordinates (latitude, longitude, altitude) |

## Pattern

A `Location` can carry multiple facets — a street address and GPS coordinates on the same object:

```python
from case_uco import CASEGraph
from case_uco.uco.location import Location, SimpleAddressFacet, LatLongCoordinatesFacet

graph = CASEGraph()

# Location with street address only
office = graph.create(Location, name="...",
    has_facet=[SimpleAddressFacet(
        street="...",       # from source
        locality="...",     # city
        region="...",       # state/province
        postal_code="...",  # from source
        country="...",      # ISO country code
        address_type="...", # e.g. "business", "residential"
    )],
)

# Location with GPS coordinates
gps_point = graph.create(Location, name="...",
    has_facet=[LatLongCoordinatesFacet(
        latitude=...,    # decimal degrees from source
        longitude=...,   # decimal degrees from source
        altitude=...,    # meters, if available
    )],
)

# Location with both address and coordinates
site = graph.create(Location, name="...",
    has_facet=[
        SimpleAddressFacet(
            street="...", locality="...", region="...",
            postal_code="...", country="...",
        ),
        LatLongCoordinatesFacet(
            latitude=..., longitude=...,
        ),
    ],
)

graph.write("location.jsonld")
```

## Notes

- `SimpleAddressFacet` fields are all `Optional[str]`: `street`, `locality`, `region`, `postal_code`, `country`, `address_type`.
- `LatLongCoordinatesFacet` fields are all `Optional[float]`: `latitude`, `longitude`, `altitude`.
- Locations are referenced by other objects via `location` fields on `Action`/`InvestigativeAction`, or linked via `Relationship` objects.
- For GPS coordinates extracted from device data, see also the [cell-site recipe](cell-site.md) and [EXIF recipe](exif-data.md).
