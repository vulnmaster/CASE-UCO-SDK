// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.action;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.UcoInherentCharacterizationThing;

/** An array of action is an ordered list of references to things that may be done or performed. */
public class ArrayOfAction extends UcoInherentCharacterizationThing {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/action/ArrayOfAction";
    public static final String NAMESPACE_PREFIX = "uco-action";

    @org.caseontology.CaseRequired
    private List<Action> action;

    public ArrayOfAction() {
        this.action = new ArrayList<>();
    }

    public List<Action> getAction() { return this.action; }
    public ArrayOfAction setAction(List<Action> value) { this.action = value; return this; }

}