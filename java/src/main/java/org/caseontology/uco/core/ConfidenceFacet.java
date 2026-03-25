// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.core;

import java.util.ArrayList;
import java.util.List;

/** A confidence is a grouping of characteristics unique to an asserted level of certainty in the accuracy of some information. */
public class ConfidenceFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/core/ConfidenceFacet";
    public static final String NAMESPACE_PREFIX = "uco-core";

    @org.caseontology.CaseRequired
    private long confidence;

    public ConfidenceFacet() {
    }

    public long getConfidence() { return this.confidence; }
    public ConfidenceFacet setConfidence(long value) { this.confidence = value; return this; }

}