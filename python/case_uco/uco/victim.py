"""Auto-generated uco-victim classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass

from case_uco.uco.role import NeutralRole


@dataclass
class Victim(NeutralRole):
    """A victim is a role played by a person or organization that is/was the target of some malicious action."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/victim/Victim"
    NAMESPACE_PREFIX: str = "uco-victim"



@dataclass
class VictimTargeting(Victim):
    """A victim targeting is a grouping of characteristics unique to people or organizations that are the target of some malicious activity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/victim/VictimTargeting"
    NAMESPACE_PREFIX: str = "uco-victim"


