// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: ThreadRunningStatusVocab */
public final class ThreadRunningStatusVocab {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ThreadRunningStatusVocab";
    public static final Set<String> MEMBERS = Set.of("Initialized", "Ready", "Running", "Standby", "Terminated", "Transition", "Unknown", "Waiting");
    public static final String INITIALIZED = "Initialized";
    public static final String READY = "Ready";
    public static final String RUNNING = "Running";
    public static final String STANDBY = "Standby";
    public static final String TERMINATED = "Terminated";
    public static final String TRANSITION = "Transition";
    public static final String UNKNOWN = "Unknown";
    public static final String WAITING = "Waiting";

    private ThreadRunningStatusVocab() {}
}
