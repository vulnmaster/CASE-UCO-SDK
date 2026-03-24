//! Auto-generated uco-action types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

use crate::uco::core::UcoObject;
use crate::uco::location::Location;

/// An action is something that may be done or performed.
#[derive(Debug, Clone, Serialize)]
pub struct Action {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-action:actionCount")]
    pub action_count: Option<u64>,
    #[serde(rename = "uco-action:actionStatus")]
    pub action_status: Vec<String>,
    #[serde(rename = "uco-action:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-action:environment")]
    pub environment: Option<UcoObject>,
    #[serde(rename = "uco-action:error")]
    pub error: Vec<UcoObject>,
    #[serde(rename = "uco-action:instrument")]
    pub instrument: Vec<UcoObject>,
    #[serde(rename = "uco-action:location")]
    pub location: Vec<Location>,
    #[serde(rename = "uco-action:object")]
    pub object: Vec<UcoObject>,
    #[serde(rename = "uco-action:participant")]
    pub participant: Vec<UcoObject>,
    #[serde(rename = "uco-action:performer")]
    pub performer: Option<UcoObject>,
    #[serde(rename = "uco-action:result")]
    pub result: Vec<UcoObject>,
    #[serde(rename = "uco-action:startTime")]
    pub start_time: Option<String>,
    #[serde(rename = "uco-action:subaction")]
    pub subaction: Vec<Action>,
}

impl Action {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/Action";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ActionBuilder {
        ActionBuilder {
            action_count: None,
            action_status: Vec::new(),
            end_time: None,
            environment: None,
            error: Vec::new(),
            instrument: Vec::new(),
            location: Vec::new(),
            object: Vec::new(),
            participant: Vec::new(),
            performer: None,
            result: Vec::new(),
            start_time: None,
            subaction: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ActionBuilder {
    action_count: Option<u64>,
    action_status: Vec<String>,
    end_time: Option<String>,
    environment: Option<UcoObject>,
    error: Vec<UcoObject>,
    instrument: Vec<UcoObject>,
    location: Vec<Location>,
    object: Vec<UcoObject>,
    participant: Vec<UcoObject>,
    performer: Option<UcoObject>,
    result: Vec<UcoObject>,
    start_time: Option<String>,
    subaction: Vec<Action>,
}

impl ActionBuilder {
    pub fn action_count(mut self, value: u64) -> Self {
        self.action_count = Some(value);
        self
    }

    pub fn action_status(mut self, value: Vec<String>) -> Self {
        self.action_status = value;
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn environment(mut self, value: UcoObject) -> Self {
        self.environment = Some(value);
        self
    }

    pub fn error(mut self, value: Vec<UcoObject>) -> Self {
        self.error = value;
        self
    }

    pub fn instrument(mut self, value: Vec<UcoObject>) -> Self {
        self.instrument = value;
        self
    }

    pub fn location(mut self, value: Vec<Location>) -> Self {
        self.location = value;
        self
    }

    pub fn object(mut self, value: Vec<UcoObject>) -> Self {
        self.object = value;
        self
    }

    pub fn participant(mut self, value: Vec<UcoObject>) -> Self {
        self.participant = value;
        self
    }

    pub fn performer(mut self, value: UcoObject) -> Self {
        self.performer = Some(value);
        self
    }

    pub fn result(mut self, value: Vec<UcoObject>) -> Self {
        self.result = value;
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn subaction(mut self, value: Vec<Action>) -> Self {
        self.subaction = value;
        self
    }

    pub fn build(self) -> Action {
        Action {
            class_iri: Action::CLASS_IRI,
            action_count: self.action_count,
            action_status: self.action_status,
            end_time: self.end_time,
            environment: self.environment,
            error: self.error,
            instrument: self.instrument,
            location: self.location,
            object: self.object,
            participant: self.participant,
            performer: self.performer,
            result: self.result,
            start_time: self.start_time,
            subaction: self.subaction,
        }
    }
}

impl CaseObject for Action {
    fn class_iri() -> &'static str { Action::CLASS_IRI }
    fn type_name() -> &'static str { "Action" }
}

/// An action argument facet is a grouping of characteristics unique to a single parameter of an action.
#[derive(Debug, Clone, Serialize)]
pub struct ActionArgumentFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-action:argumentName")]
    pub argument_name: String,
    #[serde(rename = "uco-action:value")]
    pub value: String,
}

impl ActionArgumentFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/ActionArgumentFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ActionArgumentFacetBuilder {
        ActionArgumentFacetBuilder {
            argument_name: None,
            value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ActionArgumentFacetBuilder {
    argument_name: Option<String>,
    value: Option<String>,
}

impl ActionArgumentFacetBuilder {
    pub fn argument_name(mut self, value: String) -> Self {
        self.argument_name = Some(value);
        self
    }

    pub fn value(mut self, value: String) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> ActionArgumentFacet {
        ActionArgumentFacet {
            class_iri: ActionArgumentFacet::CLASS_IRI,
            argument_name: self.argument_name.expect("missing required field: argument_name"),
            value: self.value.expect("missing required field: value"),
        }
    }
}

impl CaseObject for ActionArgumentFacet {
    fn class_iri() -> &'static str { ActionArgumentFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ActionArgumentFacet" }
}

/// An action estimation facet is a grouping of characteristics unique to decision-focused approximation aspects for an action that may potentially be performed.
#[derive(Debug, Clone, Serialize)]
pub struct ActionEstimationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-action:estimatedCost")]
    pub estimated_cost: Option<String>,
    #[serde(rename = "uco-action:estimatedEfficacy")]
    pub estimated_efficacy: Option<String>,
    #[serde(rename = "uco-action:estimatedImpact")]
    pub estimated_impact: Option<String>,
    #[serde(rename = "uco-action:objective")]
    pub objective: Option<String>,
}

impl ActionEstimationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/ActionEstimationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ActionEstimationFacetBuilder {
        ActionEstimationFacetBuilder {
            estimated_cost: None,
            estimated_efficacy: None,
            estimated_impact: None,
            objective: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ActionEstimationFacetBuilder {
    estimated_cost: Option<String>,
    estimated_efficacy: Option<String>,
    estimated_impact: Option<String>,
    objective: Option<String>,
}

impl ActionEstimationFacetBuilder {
    pub fn estimated_cost(mut self, value: String) -> Self {
        self.estimated_cost = Some(value);
        self
    }

    pub fn estimated_efficacy(mut self, value: String) -> Self {
        self.estimated_efficacy = Some(value);
        self
    }

    pub fn estimated_impact(mut self, value: String) -> Self {
        self.estimated_impact = Some(value);
        self
    }

    pub fn objective(mut self, value: String) -> Self {
        self.objective = Some(value);
        self
    }

    pub fn build(self) -> ActionEstimationFacet {
        ActionEstimationFacet {
            class_iri: ActionEstimationFacet::CLASS_IRI,
            estimated_cost: self.estimated_cost,
            estimated_efficacy: self.estimated_efficacy,
            estimated_impact: self.estimated_impact,
            objective: self.objective,
        }
    }
}

impl CaseObject for ActionEstimationFacet {
    fn class_iri() -> &'static str { ActionEstimationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ActionEstimationFacet" }
}

/// An action frequency facet is a grouping of characteristics unique to the frequency of occurrence for an action.
#[derive(Debug, Clone, Serialize)]
pub struct ActionFrequencyFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-action:rate")]
    pub rate: f64,
    #[serde(rename = "uco-action:scale")]
    pub scale: String,
    #[serde(rename = "uco-action:trend")]
    pub trend: Vec<String>,
    #[serde(rename = "uco-action:units")]
    pub units: String,
}

impl ActionFrequencyFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/ActionFrequencyFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ActionFrequencyFacetBuilder {
        ActionFrequencyFacetBuilder {
            rate: None,
            scale: None,
            trend: Vec::new(),
            units: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ActionFrequencyFacetBuilder {
    rate: Option<f64>,
    scale: Option<String>,
    trend: Vec<String>,
    units: Option<String>,
}

impl ActionFrequencyFacetBuilder {
    pub fn rate(mut self, value: f64) -> Self {
        self.rate = Some(value);
        self
    }

    pub fn scale(mut self, value: String) -> Self {
        self.scale = Some(value);
        self
    }

    pub fn trend(mut self, value: Vec<String>) -> Self {
        self.trend = value;
        self
    }

    pub fn units(mut self, value: String) -> Self {
        self.units = Some(value);
        self
    }

    pub fn build(self) -> ActionFrequencyFacet {
        ActionFrequencyFacet {
            class_iri: ActionFrequencyFacet::CLASS_IRI,
            rate: self.rate.expect("missing required field: rate"),
            scale: self.scale.expect("missing required field: scale"),
            trend: self.trend,
            units: self.units.expect("missing required field: units"),
        }
    }
}

impl CaseObject for ActionFrequencyFacet {
    fn class_iri() -> &'static str { ActionFrequencyFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ActionFrequencyFacet" }
}

/// An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action lifecycles.
#[derive(Debug, Clone, Serialize)]
pub struct ActionLifecycle {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-action:actionCount")]
    pub action_count: Vec<u64>,
    #[serde(rename = "uco-action:endTime")]
    pub end_time: Vec<String>,
    #[serde(rename = "uco-action:error")]
    pub error: Vec<UcoObject>,
    #[serde(rename = "uco-action:phase")]
    pub phase: ArrayOfAction,
    #[serde(rename = "uco-action:startTime")]
    pub start_time: Vec<String>,
}

impl ActionLifecycle {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/ActionLifecycle";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ActionLifecycleBuilder {
        ActionLifecycleBuilder {
            action_count: Vec::new(),
            end_time: Vec::new(),
            error: Vec::new(),
            phase: None,
            start_time: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ActionLifecycleBuilder {
    action_count: Vec<u64>,
    end_time: Vec<String>,
    error: Vec<UcoObject>,
    phase: Option<ArrayOfAction>,
    start_time: Vec<String>,
}

impl ActionLifecycleBuilder {
    pub fn action_count(mut self, value: Vec<u64>) -> Self {
        self.action_count = value;
        self
    }

    pub fn end_time(mut self, value: Vec<String>) -> Self {
        self.end_time = value;
        self
    }

    pub fn error(mut self, value: Vec<UcoObject>) -> Self {
        self.error = value;
        self
    }

    pub fn phase(mut self, value: ArrayOfAction) -> Self {
        self.phase = Some(value);
        self
    }

    pub fn start_time(mut self, value: Vec<String>) -> Self {
        self.start_time = value;
        self
    }

    pub fn build(self) -> ActionLifecycle {
        ActionLifecycle {
            class_iri: ActionLifecycle::CLASS_IRI,
            action_count: self.action_count,
            end_time: self.end_time,
            error: self.error,
            phase: self.phase.expect("missing required field: phase"),
            start_time: self.start_time,
        }
    }
}

impl CaseObject for ActionLifecycle {
    fn class_iri() -> &'static str { ActionLifecycle::CLASS_IRI }
    fn type_name() -> &'static str { "ActionLifecycle" }
}

/// An action pattern is a grouping of characteristics unique to a combination of actions forming a consistent or characteristic arrangement.
#[derive(Debug, Clone, Serialize)]
pub struct ActionPattern {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ActionPattern {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/ActionPattern";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ActionPatternBuilder {
        ActionPatternBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ActionPatternBuilder {
}

impl ActionPatternBuilder {
    pub fn build(self) -> ActionPattern {
        ActionPattern {
            class_iri: ActionPattern::CLASS_IRI,
        }
    }
}

impl CaseObject for ActionPattern {
    fn class_iri() -> &'static str { ActionPattern::CLASS_IRI }
    fn type_name() -> &'static str { "ActionPattern" }
}

/// An array of action is an ordered list of references to things that may be done or performed.
#[derive(Debug, Clone, Serialize)]
pub struct ArrayOfAction {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-action:action")]
    pub action: Vec<Action>,
}

impl ArrayOfAction {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/action/ArrayOfAction";
    pub const NAMESPACE_PREFIX: &'static str = "uco-action";

    pub fn builder() -> ArrayOfActionBuilder {
        ArrayOfActionBuilder {
            action: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ArrayOfActionBuilder {
    action: Vec<Action>,
}

impl ArrayOfActionBuilder {
    pub fn action(mut self, value: Vec<Action>) -> Self {
        self.action = value;
        self
    }

    pub fn build(self) -> ArrayOfAction {
        ArrayOfAction {
            class_iri: ArrayOfAction::CLASS_IRI,
            action: self.action,
        }
    }
}

impl CaseObject for ArrayOfAction {
    fn class_iri() -> &'static str { ArrayOfAction::CLASS_IRI }
    fn type_name() -> &'static str { "ArrayOfAction" }
}
