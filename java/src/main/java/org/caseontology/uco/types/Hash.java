// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.types;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.UcoInherentCharacterizationThing;

/** A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm that maps data of arbitrary size to a bit string (the 'hash') and is a one-way function, that is, a fu */
public class Hash extends UcoInherentCharacterizationThing {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/types/Hash";
    public static final String NAMESPACE_PREFIX = "uco-types";

    private List<String> hashMethod;
    @org.caseontology.CaseRequired
    private byte[] hashValue;

    public Hash() {
        this.hashMethod = new ArrayList<>();
    }

    public List<String> getHashMethod() { return this.hashMethod; }
    public Hash setHashMethod(List<String> value) { this.hashMethod = value; return this; }

    public byte[] getHashValue() { return this.hashValue; }
    public Hash setHashValue(byte[] value) { this.hashValue = value; return this; }

}