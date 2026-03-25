// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.action.Action;

/** An observation is a temporal perception of an observable. */
public class Observation extends Action {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/Observation";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    @org.caseontology.CaseRequired
    private String name;

    public Observation() {
    }

    public String getNameValue() { return this.name; }
    public Observation setNameValue(String value) { this.name = value; return this; }

}