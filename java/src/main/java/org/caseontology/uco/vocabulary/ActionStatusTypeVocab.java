// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: ActionStatusTypeVocab */
public final class ActionStatusTypeVocab {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionStatusTypeVocab";
    public static final Set<String> MEMBERS = Set.of("Complete/Finish", "Error", "Fail", "Ongoing", "Pending", "Success", "Unknown");
    public static final String COMPLETE_FINISH = "Complete/Finish";
    public static final String ERROR = "Error";
    public static final String FAIL = "Fail";
    public static final String ONGOING = "Ongoing";
    public static final String PENDING = "Pending";
    public static final String SUCCESS = "Success";
    public static final String UNKNOWN = "Unknown";

    private ActionStatusTypeVocab() {}
}
