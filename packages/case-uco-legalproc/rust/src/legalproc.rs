//! Legal Process and Procedure Extension — legalproc module

use serde::Serialize;

/// A charging instrument is a formal document that initiates or amends criminal charges against one or more defendants, suc
#[derive(Debug, Clone, Serialize, Default)]
pub struct ChargingInstrument {
    pub instrument_type: Option<String>,
}

impl ChargingInstrument {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/ChargingInstrument" }
}

/// A criminal charge is a formal accusation, stated as one or more counts within a charging instrument, that a person commi
#[derive(Debug, Clone, Serialize, Default)]
pub struct CriminalCharge {
    pub asserted_in: Vec<ChargingInstrument>,
    pub charge_classification: Option<String>,
    pub charge_disposition: Vec<String>,
    pub count_label: Option<String>,
    pub count_number: Vec<u64>,
    pub object_offense: Vec<CriminalCharge>,
    pub offense_form: Option<String>,
    pub statute_citation: Vec<String>,
}

impl CriminalCharge {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/CriminalCharge" }
}

/// A criminal proceeding is a formal event in a criminal case conducted before a tribunal, such as an arraignment, detentio
#[derive(Debug, Clone, Serialize, Default)]
pub struct CriminalProceeding {
    pub proceeding_type: Option<String>,
}

impl CriminalProceeding {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/CriminalProceeding" }
}

/// A prosecutor's sourced duty to disclose specified information or evidence to the defense. Use disclosureKind to record t
#[derive(Debug, Clone, Serialize, Default)]
pub struct DisclosureObligation {
    pub concerns_charge: Vec<CriminalCharge>,
    pub concerns_evidence: Vec<UcoObject>,
    pub disclosure_kind: Option<String>,
    pub disclosure_source_citation: Option<String>,
    pub disclosure_status: Option<String>,
}

impl DisclosureObligation {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/DisclosureObligation" }
}

/// A sourced act of producing discovery material to the defense in satisfaction of a DisclosureObligation. See Federal Rule
#[derive(Debug, Clone, Serialize, Default)]
pub struct DiscoveryProduction {
    pub disclosure_source_citation: Option<String>,
    pub satisfies_obligation: Vec<DisclosureObligation>,
}

impl DiscoveryProduction {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/DiscoveryProduction" }
}

/// A criminal charge under federal or national law, used when the source establishes federal jurisdiction. Pair with a Fede
#[derive(Debug, Clone, Serialize, Default)]
pub struct FederalCharge {
    pub jurisdiction_kind: Option<String>,
}

impl FederalCharge {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/FederalCharge" }
}

/// A federal or national criminal jurisdiction. Link charges and proceedings to this node with a registered uco-core:Relati
#[derive(Debug, Clone, Serialize, Default)]
pub struct FederalJurisdiction {
}

impl FederalJurisdiction {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/FederalJurisdiction" }
}

/// A forfeiture order is an order, or pre-conviction allegation, requiring surrender to the state of property involved in o
#[derive(Debug, Clone, Serialize, Default)]
pub struct ForfeitureOrder {
    pub currency_code: Option<String>,
    pub monetary_amount: Option<f64>,
}

impl ForfeitureOrder {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/ForfeitureOrder" }
}

/// A plea is a defendant's formal answer to a criminal charge. See Federal Rule of Criminal Procedure 11 (https://www.law.c
#[derive(Debug, Clone, Serialize, Default)]
pub struct Plea {
    pub concerns_charge: Vec<CriminalCharge>,
    pub outcome_scope: Option<String>,
    pub plea_type: Option<String>,
}

impl Plea {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/Plea" }
}

/// A plea agreement is a negotiated agreement between the prosecution and a defendant concerning the plea that will be ente
#[derive(Debug, Clone, Serialize, Default)]
pub struct PleaAgreement {
    pub concerns_charge: Vec<CriminalCharge>,
    pub outcome_scope: Option<String>,
    pub records_plea: Vec<Plea>,
}

impl PleaAgreement {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/PleaAgreement" }
}

/// A potential penalty is a statutory maximum, mandatory minimum, or advisory guideline range that a source reports as poss
#[derive(Debug, Clone, Serialize, Default)]
pub struct PotentialPenalty {
    pub concerns_charge: Vec<CriminalCharge>,
    pub outcome_scope: Option<String>,
    pub potential_penalty_kind: Option<String>,
}

impl PotentialPenalty {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/PotentialPenalty" }
}

/// A pretrial release condition is a bail, bond, personal-recognizance, or detention-without-bond condition that governs li
#[derive(Debug, Clone, Serialize, Default)]
pub struct PretrialReleaseCondition {
    pub release_condition_kind: Option<String>,
}

impl PretrialReleaseCondition {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/PretrialReleaseCondition" }
}

/// A restitution order is an order or request that an offender compensate victims for losses caused by the offense, monetar
#[derive(Debug, Clone, Serialize, Default)]
pub struct RestitutionOrder {
    pub currency_code: Option<String>,
    pub monetary_amount: Option<f64>,
}

impl RestitutionOrder {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/RestitutionOrder" }
}

/// A sentence is a penalty recommended by a party or imposed by a tribunal upon conviction of a criminal charge. Use senten
#[derive(Debug, Clone, Serialize, Default)]
pub struct Sentence {
    pub outcome_scope: Option<String>,
    pub sentence_kind: Option<String>,
    pub sentence_status: Option<String>,
    pub sentence_term: Option<String>,
}

impl Sentence {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/Sentence" }
}

/// A criminal charge under the law of a constituent state, province, or equivalent subnational jurisdiction, used when the 
#[derive(Debug, Clone, Serialize, Default)]
pub struct StateCharge {
    pub jurisdiction_kind: Option<String>,
}

impl StateCharge {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/StateCharge" }
}

/// A state, provincial, or equivalent subnational criminal jurisdiction. Link charges and proceedings to this node with a r
#[derive(Debug, Clone, Serialize, Default)]
pub struct StateJurisdiction {
}

impl StateJurisdiction {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/StateJurisdiction" }
}

/// A defense motion to exclude evidence, typically under the Fourth Amendment or Federal Rule of Criminal Procedure 12. Mod
#[derive(Debug, Clone, Serialize, Default)]
pub struct SuppressionMotion {
    pub disclosure_source_citation: Option<String>,
    pub proceeding_type: Option<String>,
}

impl SuppressionMotion {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/SuppressionMotion" }
}

/// A verdict is a finder of fact's formal determination on a criminal charge, such as a jury's finding of guilty or not gui
#[derive(Debug, Clone, Serialize, Default)]
pub struct Verdict {
    pub concerns_charge: Vec<CriminalCharge>,
    pub verdict_type: Option<String>,
}

impl Verdict {
    pub fn class_iri() -> &'static str { "https://ontology.caseontology.org/case/criminal/Verdict" }
}
