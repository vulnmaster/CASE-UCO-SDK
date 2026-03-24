"""Auto-generated uco-role classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from case_uco.uco.core import UcoObject


@dataclass
class Role(UcoObject):
    """A role is a usual or customary function based on contextual perspective."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/role/Role"
    NAMESPACE_PREFIX: str = "uco-role"



@dataclass
class BenevolentRole(Role):
    """A benevolent role is a role with positive and/or beneficial intent."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/role/BenevolentRole"
    NAMESPACE_PREFIX: str = "uco-role"



@dataclass
class MaliciousRole(Role):
    """A malicious role is a role with malevolent intent."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/role/MaliciousRole"
    NAMESPACE_PREFIX: str = "uco-role"



@dataclass
class NeutralRole(Role):
    """A neutral role is a role with impartial intent."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/role/NeutralRole"
    NAMESPACE_PREFIX: str = "uco-role"


