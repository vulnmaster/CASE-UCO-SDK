// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology._case.investigation;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.action.Action;

/** An investigative action is something that may be done or performed within the context of an investigation, typically to examine or analyze evidence or other data. */
public class InvestigativeAction extends Action {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/investigation/InvestigativeAction";
    public static final String NAMESPACE_PREFIX = "case-investigation";

    private List<InvestigativeAction> wasInformedBy;

    public InvestigativeAction() {
        this.wasInformedBy = new ArrayList<>();
    }

    public List<InvestigativeAction> getWasInformedBy() { return this.wasInformedBy; }
    public InvestigativeAction setWasInformedBy(List<InvestigativeAction> value) { this.wasInformedBy = value; return this; }

}