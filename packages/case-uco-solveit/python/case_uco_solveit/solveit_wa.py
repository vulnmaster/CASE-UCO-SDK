"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit_wa module (generated; do not edit)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Optional

import case_uco.uco.analysis as _uco_analysis
import case_uco.uco.core as _uco_core
from case_uco_solveit._context import NAMESPACES

__all__ = ["WeaknessEvaluation", "WeaknessEvaluationSet"]


@dataclass
class WeaknessEvaluation(_uco_analysis.AnalyticResult):
    """A risk assessment of a single SOLVE-IT weakness, capturing likelihood, impact, and optionally detectability ratings with computed scores."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/weakness-assessment/WeaknessEvaluation"
    NAMESPACE_PREFIX: str = "solveit-wa"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    detect_difficulty_rating: Optional[int] = field(default=None, metadata={'jsonld_key': 'solveit-wa:detectDifficultyRating', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    evaluates_weakness: Optional[Weakness] = field(default=None, metadata={'jsonld_key': 'solveit-wa:evaluatesWeakness', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'https://ontology.solveit-df.org/solveit/core/Weakness', 'alternate_range_iris': []})
    impact_rating: Optional[int] = field(default=None, metadata={'jsonld_key': 'solveit-wa:impactRating', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    li_impact_score: Optional[int] = field(default=None, metadata={'jsonld_key': 'solveit-wa:liImpactScore', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    likelihood_rating: Optional[int] = field(default=None, metadata={'jsonld_key': 'solveit-wa:likelihoodRating', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    rpn_score: Optional[int] = field(default=None, metadata={'jsonld_key': 'solveit-wa:rpnScore', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class WeaknessEvaluationSet(_uco_core.ContextualCompilation):
    """A collection of weakness evaluations scoped to a technique or context, with authorship and date metadata. Represents one assessment session."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/weakness-assessment/WeaknessEvaluationSet"
    NAMESPACE_PREFIX: str = "solveit-wa"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    evaluated_by: list[Identity] = field(default_factory=list, metadata={'jsonld_key': 'solveit-wa:evaluatedBy', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    has_evaluation: list[WeaknessEvaluation] = field(default_factory=list, metadata={'jsonld_key': 'solveit-wa:hasEvaluation', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/weakness-assessment/WeaknessEvaluation', 'alternate_range_iris': []})
    scoring_scheme: Optional[str] = field(default=None, metadata={'jsonld_key': 'solveit-wa:scoringScheme', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
