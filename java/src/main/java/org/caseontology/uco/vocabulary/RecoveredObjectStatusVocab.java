// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: RecoveredObjectStatusVocab */
public final class RecoveredObjectStatusVocab {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RecoveredObjectStatusVocab";
    public static final Set<String> MEMBERS = Set.of("overwritten", "partially recovered", "recovered", "unknown");
    public static final String OVERWRITTEN = "overwritten";
    public static final String PARTIALLY_RECOVERED = "partially recovered";
    public static final String RECOVERED = "recovered";
    public static final String UNKNOWN = "unknown";

    private RecoveredObjectStatusVocab() {}
}
