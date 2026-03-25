// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.marking;

import java.util.ArrayList;
import java.util.List;

/** A terms of use marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to conv */
public class TermsOfUseMarking extends MarkingModel {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/marking/TermsOfUseMarking";
    public static final String NAMESPACE_PREFIX = "uco-marking";

    private List<String> definitionType;
    @org.caseontology.CaseRequired
    private String termsOfUse;

    public TermsOfUseMarking() {
        this.definitionType = new ArrayList<>();
    }

    public List<String> getDefinitionType() { return this.definitionType; }
    public TermsOfUseMarking setDefinitionType(List<String> value) { this.definitionType = value; return this; }

    public String getTermsOfUse() { return this.termsOfUse; }
    public TermsOfUseMarking setTermsOfUse(String value) { this.termsOfUse = value; return this; }

}