// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.core;

import java.util.ArrayList;
import java.util.List;

/** An enclosing compilation is a container for a grouping of things. */
public class EnclosingCompilation extends Compilation {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/core/EnclosingCompilation";
    public static final String NAMESPACE_PREFIX = "uco-core";

    @org.caseontology.CaseRequired
    private List<UcoObject> object;

    public EnclosingCompilation() {
        this.object = new ArrayList<>();
    }

    public List<UcoObject> getObject() { return this.object; }
    public EnclosingCompilation setObject(List<UcoObject> value) { this.object = value; return this; }

}