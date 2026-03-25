// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.core;

import java.util.ArrayList;
import java.util.List;

/** An annotation is an assertion made in relation to one or more objects. */
public class Annotation extends Assertion {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/core/Annotation";
    public static final String NAMESPACE_PREFIX = "uco-core";

    @org.caseontology.CaseRequired
    private List<UcoObject> object;

    public Annotation() {
        this.object = new ArrayList<>();
    }

    public List<UcoObject> getObject() { return this.object; }
    public Annotation setObject(List<UcoObject> value) { this.object = value; return this; }

}