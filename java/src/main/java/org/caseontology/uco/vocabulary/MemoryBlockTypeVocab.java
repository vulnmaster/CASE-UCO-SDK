// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: MemoryBlockTypeVocab */
public final class MemoryBlockTypeVocab {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/MemoryBlockTypeVocab";
    public static final Set<String> MEMBERS = Set.of("Bit-mapped", "Byte-mapped", "Initialized", "Overlay", "Uninitialized");
    public static final String BIT_MAPPED = "Bit-mapped";
    public static final String BYTE_MAPPED = "Byte-mapped";
    public static final String INITIALIZED = "Initialized";
    public static final String OVERLAY = "Overlay";
    public static final String UNINITIALIZED = "Uninitialized";

    private MemoryBlockTypeVocab() {}
}
