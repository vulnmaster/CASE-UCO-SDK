// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: UnixProcessStateVocab */
public final class UnixProcessStateVocab {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/UnixProcessStateVocab";
    public static final Set<String> MEMBERS = Set.of("Dead", "InterruptibleSleep", "Paging", "Running", "Stopped", "UninterruptibleSleep", "Zombie");
    public static final String DEAD = "Dead";
    public static final String INTERRUPTIBLESLEEP = "InterruptibleSleep";
    public static final String PAGING = "Paging";
    public static final String RUNNING = "Running";
    public static final String STOPPED = "Stopped";
    public static final String UNINTERRUPTIBLESLEEP = "UninterruptibleSleep";
    public static final String ZOMBIE = "Zombie";

    private UnixProcessStateVocab() {}
}
