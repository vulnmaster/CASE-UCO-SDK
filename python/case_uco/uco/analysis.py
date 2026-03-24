"""Auto-generated uco-analysis classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from case_uco.uco.core import Facet
from case_uco.uco.core import UcoInherentCharacterizationThing


@dataclass
class AnalyticResultFacet(Facet):
    """An analytic result facet is a grouping of characteristics unique to the results of an analysis action."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/analysis/AnalyticResultFacet"
    NAMESPACE_PREFIX: str = "uco-analysis"



@dataclass
class ArtifactClassification(UcoInherentCharacterizationThing):
    """An artifact classification is a single specific assertion that a particular class of a classification taxonomy applies to something."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassification"
    NAMESPACE_PREFIX: str = "uco-analysis"

    class_: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-analysis:class', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    classification_confidence: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-analysis:classificationConfidence', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})


@dataclass
class ArtifactClassificationResultFacet(AnalyticResultFacet):
    """An artifact classification result facet is a grouping of characteristics unique to the results of an artifact classification analysis action."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassificationResultFacet"
    NAMESPACE_PREFIX: str = "uco-analysis"

    classification: list[ArtifactClassification] = field(default_factory=list, metadata={'jsonld_key': 'uco-analysis:classification', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassification', 'alternate_range_iris': []})

