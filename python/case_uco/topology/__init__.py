"""Queryable semantic-core topology: Composition Profiles and the CAC/UCO spine.

This package is additive. It does not change generated classes or CaseGraph
public constructors. All data is loaded from local JSON shipped with the
repository (or the wheel) and never requires network access.
"""

from case_uco.topology.profiles import (
    CompositionProfile,
    FacetSet,
    get_profile,
    list_profiles,
    recommend_profile,
    recommend_facet_set,
)
from case_uco.topology.spine import (
    SpineKind,
    get_semantic_spine,
    list_spine_kinds,
    spine_kind_for_class,
)

__all__ = [
    "CompositionProfile",
    "FacetSet",
    "SpineKind",
    "get_profile",
    "get_semantic_spine",
    "list_profiles",
    "list_spine_kinds",
    "recommend_facet_set",
    "recommend_profile",
    "spine_kind_for_class",
]
