// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.action;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** An action argument facet is a grouping of characteristics unique to a single parameter of an action. */
public class ActionArgumentFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/action/ActionArgumentFacet";
    public static final String NAMESPACE_PREFIX = "uco-action";

    @org.caseontology.CaseRequired
    private String argumentName;
    @org.caseontology.CaseRequired
    private String value;

    public ActionArgumentFacet() {
    }

    public String getArgumentName() { return this.argumentName; }
    public ActionArgumentFacet setArgumentName(String value) { this.argumentName = value; return this; }

    public String getValue() { return this.value; }
    public ActionArgumentFacet setValue(String value) { this.value = value; return this; }

}