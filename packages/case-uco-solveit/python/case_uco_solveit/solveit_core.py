"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit_core module (generated; do not edit)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import case_uco.case.investigation as _case_investigation
import case_uco.uco.action as _uco_action
import case_uco.uco.core as _uco_core
from case_uco_solveit._context import NAMESPACES

__all__ = ["ASTMErrorCategory", "Citation", "Mitigation", "Objective", "SolveitInvestigativeAction", "Technique", "Weakness"]


@dataclass
class ASTMErrorCategory:
    """An error category from ASTM E3016-18 used to classify weakness impacts."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/ASTMErrorCategory"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Citation(_uco_core.UcoObject):
    """An academic or professional reference cited by a Technique, Weakness or Mitigation. Each citation carries an identifier (DFCite-NNNN), a plain text form, and where available a BibTeX form."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Citation"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Mitigation(_case_investigation.InvestigativeAction):
    """An action that can be performed to prevent a weakness from occurring or to minimize its impact."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Mitigation"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Objective(_uco_core.UcoObject):
    """A goal or objective in a digital forensic investigation that can be achieved through one or more techniques."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Objective"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SolveitInvestigativeAction(_case_investigation.InvestigativeAction):
    """An investigative action, which may be done or performed, as an instance of one or more SOLVE-IT techniques, recording any mitigations applied on that occasion (0..n via appliedMitigation). The techniq"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/SolveitInvestigativeAction"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    applied_mitigation: list[Mitigation] = field(default_factory=list, metadata={'jsonld_key': 'solveit-core:appliedMitigation', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/core/Mitigation', 'alternate_range_iris': []})


@dataclass
class Technique(_uco_action.Technique):
    """A digital forensic technique representing how one might achieve an objective by performing an action. Based on the SOLVE-IT knowledge base. This class is a metaclass: its instances are owl:Class entit"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Technique"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    has_case_input_class: list[Any] = field(default_factory=list, metadata={'jsonld_key': 'solveit-core:hasCASEInputClass', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2002/07/owl#Class', 'alternate_range_iris': ['http://www.w3.org/2002/07/owl#DatatypeProperty', 'http://www.w3.org/2002/07/owl#ObjectProperty']})
    has_case_output_class: list[Any] = field(default_factory=list, metadata={'jsonld_key': 'solveit-core:hasCASEOutputClass', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2002/07/owl#Class', 'alternate_range_iris': ['http://www.w3.org/2002/07/owl#DatatypeProperty', 'http://www.w3.org/2002/07/owl#ObjectProperty']})


@dataclass
class Weakness(_uco_core.UcoObject):
    """A potential problem resulting from using a technique, classified according to ASTM E3016-18 error categories."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/core/Weakness"
    NAMESPACE_PREFIX: str = "solveit-core"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
