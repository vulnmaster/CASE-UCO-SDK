// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.marking;

import java.util.ArrayList;
import java.util.List;

/** A statement marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey  */
public class StatementMarking extends MarkingModel {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/marking/StatementMarking";
    public static final String NAMESPACE_PREFIX = "uco-marking";

    private List<String> definitionType;
    @org.caseontology.CaseRequired
    private String statement;

    public StatementMarking() {
        this.definitionType = new ArrayList<>();
    }

    public List<String> getDefinitionType() { return this.definitionType; }
    public StatementMarking setDefinitionType(List<String> value) { this.definitionType = value; return this; }

    public String getStatement() { return this.statement; }
    public StatementMarking setStatement(String value) { this.statement = value; return this; }

}