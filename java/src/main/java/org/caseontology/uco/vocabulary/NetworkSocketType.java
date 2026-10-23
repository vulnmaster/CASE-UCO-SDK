// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: NetworkSocketType */
public final class NetworkSocketType {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketType";
    public static final Set<String> MEMBERS = Set.of("sock_dgram", "sock_raw", "sock_rdm", "sock_seqpacket", "sock_stream");
    public static final String SOCK_DGRAM = "sock_dgram";
    public static final String SOCK_RAW = "sock_raw";
    public static final String SOCK_RDM = "sock_rdm";
    public static final String SOCK_SEQPACKET = "sock_seqpacket";
    public static final String SOCK_STREAM = "sock_stream";

    private NetworkSocketType() {}
}
