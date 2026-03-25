// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.marking;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.MarkingDefinitionAbstraction;

/** A marking definition is a grouping of characteristics unique to the expression of a specific data marking conveying restrictions, permissions, and other guidance for how marked data can be used and sh */
public class MarkingDefinition extends MarkingDefinitionAbstraction {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/marking/MarkingDefinition";
    public static final String NAMESPACE_PREFIX = "uco-marking";

    private List<MarkingModel> definition;
    @org.caseontology.CaseRequired
    private String definitionType;

    public MarkingDefinition() {
        this.definition = new ArrayList<>();
    }

    public List<MarkingModel> getDefinition() { return this.definition; }
    public MarkingDefinition setDefinition(List<MarkingModel> value) { this.definition = value; return this; }

    public String getDefinitionType() { return this.definitionType; }
    public MarkingDefinition setDefinitionType(String value) { this.definitionType = value; return this; }

}