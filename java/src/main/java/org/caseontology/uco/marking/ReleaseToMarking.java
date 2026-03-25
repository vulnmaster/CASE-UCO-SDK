// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.marking;

import java.util.ArrayList;
import java.util.List;

/** A release-to marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey */
public class ReleaseToMarking extends MarkingModel {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/marking/ReleaseToMarking";
    public static final String NAMESPACE_PREFIX = "uco-marking";

    @org.caseontology.CaseRequired
    private List<String> authorizedIdentities;
    private List<String> definitionType;

    public ReleaseToMarking() {
        this.authorizedIdentities = new ArrayList<>();
        this.definitionType = new ArrayList<>();
    }

    public List<String> getAuthorizedIdentities() { return this.authorizedIdentities; }
    public ReleaseToMarking setAuthorizedIdentities(List<String> value) { this.authorizedIdentities = value; return this; }

    public List<String> getDefinitionType() { return this.definitionType; }
    public ReleaseToMarking setDefinitionType(List<String> value) { this.definitionType = value; return this; }

}