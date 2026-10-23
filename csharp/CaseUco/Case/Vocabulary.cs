// Auto-generated CASE/UCO vocabularies — do not edit manually.
// Every CASE vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.

using System.Collections.Generic;

namespace CaseUco.Case.Vocabulary
{
    /// <summary>Vocabulary: InvestigationFormVocab</summary>
    public static class InvestigationFormVocab
    {
        public const string IRI = "https://ontology.caseontology.org/case/vocabulary/InvestigationFormVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "case", "incident", "suspicious-activity" };
        public const string @case = "case";
        public const string incident = "incident";
        public const string suspicious_activity = "suspicious-activity";
    }
}
