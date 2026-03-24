//! Auto-generated uco-pattern types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

/// A logical pattern is a grouping of characteristics unique to an informational pattern expressed via a structured pattern expression following the rules of logic.
#[derive(Debug, Clone, Serialize)]
pub struct LogicalPattern {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-pattern:patternExpression")]
    pub pattern_expression: Option<PatternExpression>,
}

impl LogicalPattern {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/pattern/LogicalPattern";
    pub const NAMESPACE_PREFIX: &'static str = "uco-pattern";

    pub fn builder() -> LogicalPatternBuilder {
        LogicalPatternBuilder {
            pattern_expression: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LogicalPatternBuilder {
    pattern_expression: Option<PatternExpression>,
}

impl LogicalPatternBuilder {
    pub fn pattern_expression(mut self, value: PatternExpression) -> Self {
        self.pattern_expression = Some(value);
        self
    }

    pub fn build(self) -> LogicalPattern {
        LogicalPattern {
            class_iri: LogicalPattern::CLASS_IRI,
            pattern_expression: self.pattern_expression,
        }
    }
}

impl CaseObject for LogicalPattern {
    fn class_iri() -> &'static str { LogicalPattern::CLASS_IRI }
    fn type_name() -> &'static str { "LogicalPattern" }
}

/// A pattern is a combination of properties, acts, tendencies, etc., forming a consistent or characteristic arrangement.
#[derive(Debug, Clone, Serialize)]
pub struct Pattern {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Pattern {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/pattern/Pattern";
    pub const NAMESPACE_PREFIX: &'static str = "uco-pattern";

    pub fn builder() -> PatternBuilder {
        PatternBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PatternBuilder {
}

impl PatternBuilder {
    pub fn build(self) -> Pattern {
        Pattern {
            class_iri: Pattern::CLASS_IRI,
        }
    }
}

impl CaseObject for Pattern {
    fn class_iri() -> &'static str { Pattern::CLASS_IRI }
    fn type_name() -> &'static str { "Pattern" }
}

/// A pattern expression is a grouping of characteristics unique to an explicit logical expression defining a pattern (e.g., regular expression, SQL Select expression, etc.).
#[derive(Debug, Clone, Serialize)]
pub struct PatternExpression {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl PatternExpression {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression";
    pub const NAMESPACE_PREFIX: &'static str = "uco-pattern";

    pub fn builder() -> PatternExpressionBuilder {
        PatternExpressionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PatternExpressionBuilder {
}

impl PatternExpressionBuilder {
    pub fn build(self) -> PatternExpression {
        PatternExpression {
            class_iri: PatternExpression::CLASS_IRI,
        }
    }
}

impl CaseObject for PatternExpression {
    fn class_iri() -> &'static str { PatternExpression::CLASS_IRI }
    fn type_name() -> &'static str { "PatternExpression" }
}
