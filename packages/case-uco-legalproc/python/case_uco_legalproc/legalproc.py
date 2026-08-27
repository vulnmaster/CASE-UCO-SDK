"""Legal Process and Procedure Extension — legalproc module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChargingInstrument:
    """A charging instrument is a formal document that initiates or amends criminal charges against one or more defendants, such as a criminal complaint, indictment, superseding indictment, or information. S"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/ChargingInstrument"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    instrument_type: Optional[str] = field(default=None)


@dataclass
class CriminalCharge:
    """A criminal charge is a formal accusation, stated as one or more counts within a charging instrument, that a person committed a specific statutory offense. Inchoate and derivative offenses (conspiracy,"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/CriminalCharge"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    asserted_in: list[ChargingInstrument] = field(default_factory=list)
    charge_classification: Optional[str] = field(default=None)
    charge_disposition: list[str] = field(default_factory=list)
    count_label: Optional[str] = field(default=None)
    count_number: list[int] = field(default_factory=list)
    object_offense: list[CriminalCharge] = field(default_factory=list)
    offense_form: Optional[str] = field(default=None)
    statute_citation: list[str] = field(default_factory=list)


@dataclass
class CriminalProceeding:
    """A criminal proceeding is a formal event in a criminal case conducted before a tribunal, such as an arraignment, detention hearing, trial, plea hearing, sentencing hearing, or appeal."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/CriminalProceeding"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    proceeding_type: Optional[str] = field(default=None)


@dataclass
class DisclosureObligation:
    """A prosecutor's sourced duty to disclose specified information or evidence to the defense. Use disclosureKind to record the governing doctrine (Brady, Giglio, Jencks, or Federal Rule of Criminal Proced"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/DisclosureObligation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    concerns_evidence: list[UcoObject] = field(default_factory=list)
    disclosure_kind: Optional[str] = field(default=None)
    disclosure_source_citation: Optional[str] = field(default=None)
    disclosure_status: Optional[str] = field(default=None)


@dataclass
class DiscoveryProduction:
    """A sourced act of producing discovery material to the defense in satisfaction of a DisclosureObligation. See Federal Rule of Criminal Procedure 16 (https://www.law.cornell.edu/rules/frcrmp/rule_16)."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/DiscoveryProduction"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    disclosure_source_citation: Optional[str] = field(default=None)
    satisfies_obligation: list[DisclosureObligation] = field(default_factory=list)


@dataclass
class FederalCharge:
    """A criminal charge under federal or national law, used when the source establishes federal jurisdiction. Pair with a FederalJurisdiction (or equivalent) node via a registered uco-core:Relationship when"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/FederalCharge"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    asserted_in: list[ChargingInstrument] = field(default_factory=list)
    charge_classification: Optional[str] = field(default=None)
    charge_disposition: list[str] = field(default_factory=list)
    count_label: Optional[str] = field(default=None)
    count_number: list[int] = field(default_factory=list)
    object_offense: list[CriminalCharge] = field(default_factory=list)
    offense_form: Optional[str] = field(default=None)
    statute_citation: list[str] = field(default_factory=list)
    jurisdiction_kind: Optional[str] = field(default=None)


@dataclass
class FederalJurisdiction:
    """A federal or national criminal jurisdiction. Link charges and proceedings to this node with a registered uco-core:Relationship until a direct ontology property is adopted. Compatible with the CAC mult"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/FederalJurisdiction"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)


@dataclass
class ForfeitureOrder:
    """A forfeiture order is an order, or pre-conviction allegation, requiring surrender to the state of property involved in or traceable to an offense. See 18 U.S.C. §§ 981-982 (https://www.law.cornell.edu"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/ForfeitureOrder"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    currency_code: Optional[str] = field(default=None)
    monetary_amount: Optional[float] = field(default=None)


@dataclass
class Plea:
    """A plea is a defendant's formal answer to a criminal charge. See Federal Rule of Criminal Procedure 11 (https://www.law.cornell.edu/rules/frcrmp/rule_11)."""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/Plea"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    outcome_scope: Optional[str] = field(default=None)
    plea_type: Optional[str] = field(default=None)


@dataclass
class PleaAgreement:
    """A plea agreement is a negotiated agreement between the prosecution and a defendant concerning the plea that will be entered and any agreed dispositions or sentencing recommendations, as recognized by """

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/PleaAgreement"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    outcome_scope: Optional[str] = field(default=None)
    records_plea: list[Plea] = field(default_factory=list)


@dataclass
class PotentialPenalty:
    """A potential penalty is a statutory maximum, mandatory minimum, or advisory guideline range that a source reports as possible exposure, not as a sentence that a tribunal has imposed. See 18 U.S.C. § 35"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/PotentialPenalty"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    outcome_scope: Optional[str] = field(default=None)
    potential_penalty_kind: Optional[str] = field(default=None)


@dataclass
class PretrialReleaseCondition:
    """A pretrial release condition is a bail, bond, personal-recognizance, or detention-without-bond condition that governs liberty before conviction. See 18 U.S.C. § 3142 (https://www.law.cornell.edu/uscod"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/PretrialReleaseCondition"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    release_condition_kind: Optional[str] = field(default=None)


@dataclass
class RestitutionOrder:
    """A restitution order is an order or request that an offender compensate victims for losses caused by the offense, monetarily or in kind. See 18 U.S.C. § 3663A (https://www.law.cornell.edu/uscode/text/1"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/RestitutionOrder"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    currency_code: Optional[str] = field(default=None)
    monetary_amount: Optional[float] = field(default=None)


@dataclass
class Sentence:
    """A sentence is a penalty recommended by a party or imposed by a tribunal upon conviction of a criminal charge. Use sentenceKind to record the kind of imposed or recommended sentence (custodial term, su"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/Sentence"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    outcome_scope: Optional[str] = field(default=None)
    sentence_kind: Optional[str] = field(default=None)
    sentence_status: Optional[str] = field(default=None)
    sentence_term: Optional[str] = field(default=None)


@dataclass
class StateCharge:
    """A criminal charge under the law of a constituent state, province, or equivalent subnational jurisdiction, used when the source establishes that the charge is not federal. Pair with a StateJurisdiction"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/StateCharge"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    asserted_in: list[ChargingInstrument] = field(default_factory=list)
    charge_classification: Optional[str] = field(default=None)
    charge_disposition: list[str] = field(default_factory=list)
    count_label: Optional[str] = field(default=None)
    count_number: list[int] = field(default_factory=list)
    object_offense: list[CriminalCharge] = field(default_factory=list)
    offense_form: Optional[str] = field(default=None)
    statute_citation: list[str] = field(default_factory=list)
    jurisdiction_kind: Optional[str] = field(default=None)


@dataclass
class StateJurisdiction:
    """A state, provincial, or equivalent subnational criminal jurisdiction. Link charges and proceedings to this node with a registered uco-core:Relationship until a direct ontology property is adopted. Com"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/StateJurisdiction"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)


@dataclass
class SuppressionMotion:
    """A defense motion to exclude evidence, typically under the Fourth Amendment or Federal Rule of Criminal Procedure 12. Model only when a docket or filing establishes the motion. See Federal Rule of Crim"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/SuppressionMotion"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    proceeding_type: Optional[str] = field(default=None)
    disclosure_source_citation: Optional[str] = field(default=None)


@dataclass
class Verdict:
    """A verdict is a finder of fact's formal determination on a criminal charge, such as a jury's finding of guilty or not guilty on a count. See Federal Rule of Criminal Procedure 31 (https://www.law.corne"""

    CLASS_IRI: str = "https://ontology.caseontology.org/case/criminal/Verdict"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    verdict_type: Optional[str] = field(default=None)

