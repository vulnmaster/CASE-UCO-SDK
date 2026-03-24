"""Auto-generated case-investigation classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from case_uco.uco.action import Action
from case_uco.uco.action import ActionLifecycle
from case_uco.uco.core import ContextualCompilation
from case_uco.uco.core import UcoObject
from case_uco.uco.role import Role


@dataclass
class Attorney(Role):
    """Attorney is a role involved in preparing, interpreting, and applying law."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/Attorney"
    NAMESPACE_PREFIX: str = "case-investigation"



@dataclass
class Authorization(UcoObject):
    """An authorization is a grouping of characteristics unique to some form of authoritative permission identified for investigative action."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/Authorization"
    NAMESPACE_PREFIX: str = "case-investigation"

    authorization_identifier: list[str] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:authorizationIdentifier', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    authorization_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'case-investigation:authorizationType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-core:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-core:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class Examiner(Role):
    """Examiner is a role involved in providing scientific evaluations of evidence that are used to aid law enforcement investigations and court cases."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/Examiner"
    NAMESPACE_PREFIX: str = "case-investigation"



@dataclass
class Investigation(ContextualCompilation):
    """An investigation is a grouping of characteristics unique to an exploration of the facts involved in a cyber-relevant set of suspicious activity."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/Investigation"
    NAMESPACE_PREFIX: str = "case-investigation"

    focus: list[str] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:focus', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    investigation_form: list[str] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:investigationForm', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    investigation_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'case-investigation:investigationStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    relevant_authorization: list[Authorization] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:relevantAuthorization', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.caseontology.org/case/investigation/Authorization', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-core:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-core:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class InvestigativeAction(Action):
    """An investigative action is something that may be done or performed within the context of an investigation, typically to examine or analyze evidence or other data."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/InvestigativeAction"
    NAMESPACE_PREFIX: str = "case-investigation"

    was_informed_by: list[InvestigativeAction] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:wasInformedBy', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.caseontology.org/case/investigation/InvestigativeAction', 'alternate_range_iris': []})


@dataclass
class Investigator(Role):
    """Investigator is a role involved in coordinating an investigation."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/Investigator"
    NAMESPACE_PREFIX: str = "case-investigation"



@dataclass
class ProvenanceRecord(ContextualCompilation):
    """A provenance record is a grouping of characteristics unique to the provenantial (chronology of the ownership, custody or location) connection between an investigative action and a set of observations """

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/ProvenanceRecord"
    NAMESPACE_PREFIX: str = "case-investigation"

    exhibit_number: Optional[str] = field(default=None, metadata={'jsonld_key': 'case-investigation:exhibitNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    root_exhibit_number: list[str] = field(default_factory=list, metadata={'jsonld_key': 'case-investigation:rootExhibitNumber', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Subject(Role):
    """Subject is a role whose conduct is within the scope of an investigation."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/Subject"
    NAMESPACE_PREFIX: str = "case-investigation"



@dataclass
class SubjectActionLifecycle(ActionLifecycle):
    """A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role whose conduct may be within th"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/SubjectActionLifecycle"
    NAMESPACE_PREFIX: str = "case-investigation"



@dataclass
class VictimActionLifecycle(ActionLifecycle):
    """A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role characterized by its potential """

    CLASS_IRI: str = "https://ontology.caseontology.org/case/investigation/VictimActionLifecycle"
    NAMESPACE_PREFIX: str = "case-investigation"


