//! Auto-generated case-investigation types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// Attorney is a role involved in preparing, interpreting, and applying law.
#[derive(Debug, Clone, Serialize)]
pub struct Attorney {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Attorney {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/Attorney";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> AttorneyBuilder {
        AttorneyBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AttorneyBuilder {
}

impl AttorneyBuilder {
    pub fn build(self) -> Attorney {
        Attorney {
            class_iri: Attorney::CLASS_IRI,
        }
    }
}

impl CaseObject for Attorney {
    fn class_iri() -> &'static str { Attorney::CLASS_IRI }
    fn type_name() -> &'static str { "Attorney" }
}

/// An authorization is a grouping of characteristics unique to some form of authoritative permission identified for investigative action.
#[derive(Debug, Clone, Serialize)]
pub struct Authorization {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "case-investigation:authorizationIdentifier")]
    pub authorization_identifier: Vec<String>,
    #[serde(rename = "case-investigation:authorizationType")]
    pub authorization_type: Option<String>,
    #[serde(rename = "uco-core:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-core:startTime")]
    pub start_time: Option<String>,
}

impl Authorization {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/Authorization";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> AuthorizationBuilder {
        AuthorizationBuilder {
            authorization_identifier: Vec::new(),
            authorization_type: None,
            end_time: None,
            start_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AuthorizationBuilder {
    authorization_identifier: Vec<String>,
    authorization_type: Option<String>,
    end_time: Option<String>,
    start_time: Option<String>,
}

impl AuthorizationBuilder {
    pub fn authorization_identifier(mut self, value: Vec<String>) -> Self {
        self.authorization_identifier = value;
        self
    }

    pub fn authorization_type(mut self, value: String) -> Self {
        self.authorization_type = Some(value);
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn build(self) -> Authorization {
        Authorization {
            class_iri: Authorization::CLASS_IRI,
            authorization_identifier: self.authorization_identifier,
            authorization_type: self.authorization_type,
            end_time: self.end_time,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for Authorization {
    fn class_iri() -> &'static str { Authorization::CLASS_IRI }
    fn type_name() -> &'static str { "Authorization" }
}

/// Examiner is a role involved in providing scientific evaluations of evidence that are used to aid law enforcement investigations and court cases.
#[derive(Debug, Clone, Serialize)]
pub struct Examiner {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Examiner {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/Examiner";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> ExaminerBuilder {
        ExaminerBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ExaminerBuilder {
}

impl ExaminerBuilder {
    pub fn build(self) -> Examiner {
        Examiner {
            class_iri: Examiner::CLASS_IRI,
        }
    }
}

impl CaseObject for Examiner {
    fn class_iri() -> &'static str { Examiner::CLASS_IRI }
    fn type_name() -> &'static str { "Examiner" }
}

/// An investigation is a grouping of characteristics unique to an exploration of the facts involved in a cyber-relevant set of suspicious activity.
#[derive(Debug, Clone, Serialize)]
pub struct Investigation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "case-investigation:focus")]
    pub focus: Vec<String>,
    #[serde(rename = "case-investigation:investigationForm")]
    pub investigation_form: Vec<String>,
    #[serde(rename = "case-investigation:investigationStatus")]
    pub investigation_status: Option<String>,
    #[serde(rename = "case-investigation:relevantAuthorization")]
    pub relevant_authorization: Vec<Authorization>,
    #[serde(rename = "uco-core:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-core:startTime")]
    pub start_time: Option<String>,
}

impl Investigation {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/Investigation";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> InvestigationBuilder {
        InvestigationBuilder {
            focus: Vec::new(),
            investigation_form: Vec::new(),
            investigation_status: None,
            relevant_authorization: Vec::new(),
            end_time: None,
            start_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct InvestigationBuilder {
    focus: Vec<String>,
    investigation_form: Vec<String>,
    investigation_status: Option<String>,
    relevant_authorization: Vec<Authorization>,
    end_time: Option<String>,
    start_time: Option<String>,
}

impl InvestigationBuilder {
    pub fn focus(mut self, value: Vec<String>) -> Self {
        self.focus = value;
        self
    }

    pub fn investigation_form(mut self, value: Vec<String>) -> Self {
        self.investigation_form = value;
        self
    }

    pub fn investigation_status(mut self, value: String) -> Self {
        self.investigation_status = Some(value);
        self
    }

    pub fn relevant_authorization(mut self, value: Vec<Authorization>) -> Self {
        self.relevant_authorization = value;
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn build(self) -> Investigation {
        Investigation {
            class_iri: Investigation::CLASS_IRI,
            focus: self.focus,
            investigation_form: self.investigation_form,
            investigation_status: self.investigation_status,
            relevant_authorization: self.relevant_authorization,
            end_time: self.end_time,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for Investigation {
    fn class_iri() -> &'static str { Investigation::CLASS_IRI }
    fn type_name() -> &'static str { "Investigation" }
}

/// An investigative action is something that may be done or performed within the context of an investigation, typically to examine or analyze evidence or other data.
#[derive(Debug, Clone, Serialize)]
pub struct InvestigativeAction {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "case-investigation:wasInformedBy")]
    pub was_informed_by: Vec<InvestigativeAction>,
}

impl InvestigativeAction {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/InvestigativeAction";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> InvestigativeActionBuilder {
        InvestigativeActionBuilder {
            was_informed_by: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct InvestigativeActionBuilder {
    was_informed_by: Vec<InvestigativeAction>,
}

impl InvestigativeActionBuilder {
    pub fn was_informed_by(mut self, value: Vec<InvestigativeAction>) -> Self {
        self.was_informed_by = value;
        self
    }

    pub fn build(self) -> InvestigativeAction {
        InvestigativeAction {
            class_iri: InvestigativeAction::CLASS_IRI,
            was_informed_by: self.was_informed_by,
        }
    }
}

impl CaseObject for InvestigativeAction {
    fn class_iri() -> &'static str { InvestigativeAction::CLASS_IRI }
    fn type_name() -> &'static str { "InvestigativeAction" }
}

/// Investigator is a role involved in coordinating an investigation.
#[derive(Debug, Clone, Serialize)]
pub struct Investigator {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Investigator {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/Investigator";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> InvestigatorBuilder {
        InvestigatorBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct InvestigatorBuilder {
}

impl InvestigatorBuilder {
    pub fn build(self) -> Investigator {
        Investigator {
            class_iri: Investigator::CLASS_IRI,
        }
    }
}

impl CaseObject for Investigator {
    fn class_iri() -> &'static str { Investigator::CLASS_IRI }
    fn type_name() -> &'static str { "Investigator" }
}

/// A provenance record is a grouping of characteristics unique to the provenantial (chronology of the ownership, custody or location) connection between an investigative action and a set of observations 
#[derive(Debug, Clone, Serialize)]
pub struct ProvenanceRecord {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "case-investigation:exhibitNumber")]
    pub exhibit_number: Option<String>,
    #[serde(rename = "case-investigation:rootExhibitNumber")]
    pub root_exhibit_number: Vec<String>,
}

impl ProvenanceRecord {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/ProvenanceRecord";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> ProvenanceRecordBuilder {
        ProvenanceRecordBuilder {
            exhibit_number: None,
            root_exhibit_number: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProvenanceRecordBuilder {
    exhibit_number: Option<String>,
    root_exhibit_number: Vec<String>,
}

impl ProvenanceRecordBuilder {
    pub fn exhibit_number(mut self, value: String) -> Self {
        self.exhibit_number = Some(value);
        self
    }

    pub fn root_exhibit_number(mut self, value: Vec<String>) -> Self {
        self.root_exhibit_number = value;
        self
    }

    pub fn build(self) -> ProvenanceRecord {
        ProvenanceRecord {
            class_iri: ProvenanceRecord::CLASS_IRI,
            exhibit_number: self.exhibit_number,
            root_exhibit_number: self.root_exhibit_number,
        }
    }
}

impl CaseObject for ProvenanceRecord {
    fn class_iri() -> &'static str { ProvenanceRecord::CLASS_IRI }
    fn type_name() -> &'static str { "ProvenanceRecord" }
}

/// Subject is a role whose conduct is within the scope of an investigation.
#[derive(Debug, Clone, Serialize)]
pub struct Subject {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Subject {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/Subject";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> SubjectBuilder {
        SubjectBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SubjectBuilder {
}

impl SubjectBuilder {
    pub fn build(self) -> Subject {
        Subject {
            class_iri: Subject::CLASS_IRI,
        }
    }
}

impl CaseObject for Subject {
    fn class_iri() -> &'static str { Subject::CLASS_IRI }
    fn type_name() -> &'static str { "Subject" }
}

/// A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role whose conduct may be within th
#[derive(Debug, Clone, Serialize)]
pub struct SubjectActionLifecycle {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SubjectActionLifecycle {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/SubjectActionLifecycle";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> SubjectActionLifecycleBuilder {
        SubjectActionLifecycleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SubjectActionLifecycleBuilder {
}

impl SubjectActionLifecycleBuilder {
    pub fn build(self) -> SubjectActionLifecycle {
        SubjectActionLifecycle {
            class_iri: SubjectActionLifecycle::CLASS_IRI,
        }
    }
}

impl CaseObject for SubjectActionLifecycle {
    fn class_iri() -> &'static str { SubjectActionLifecycle::CLASS_IRI }
    fn type_name() -> &'static str { "SubjectActionLifecycle" }
}

/// A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action-lifecycles performed by an entity acting in a role characterized by its potential 
#[derive(Debug, Clone, Serialize)]
pub struct VictimActionLifecycle {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl VictimActionLifecycle {
    pub const CLASS_IRI: &'static str = "https://ontology.caseontology.org/case/investigation/VictimActionLifecycle";
    pub const NAMESPACE_PREFIX: &'static str = "case-investigation";

    pub fn builder() -> VictimActionLifecycleBuilder {
        VictimActionLifecycleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct VictimActionLifecycleBuilder {
}

impl VictimActionLifecycleBuilder {
    pub fn build(self) -> VictimActionLifecycle {
        VictimActionLifecycle {
            class_iri: VictimActionLifecycle::CLASS_IRI,
        }
    }
}

impl CaseObject for VictimActionLifecycle {
    fn class_iri() -> &'static str { VictimActionLifecycle::CLASS_IRI }
    fn type_name() -> &'static str { "VictimActionLifecycle" }
}
