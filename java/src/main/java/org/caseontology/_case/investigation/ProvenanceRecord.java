// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology._case.investigation;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.ContextualCompilation;

/** A provenance record is a grouping of characteristics unique to the provenantial (chronology of the ownership, custody or location) connection between an investigative action and a set of observations  */
public class ProvenanceRecord extends ContextualCompilation {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/investigation/ProvenanceRecord";
    public static final String NAMESPACE_PREFIX = "case-investigation";

    private String exhibitNumber;
    private List<String> rootExhibitNumber;

    public ProvenanceRecord() {
        this.rootExhibitNumber = new ArrayList<>();
    }

    public String getExhibitNumber() { return this.exhibitNumber; }
    public ProvenanceRecord setExhibitNumber(String value) { this.exhibitNumber = value; return this; }

    public List<String> getRootExhibitNumber() { return this.rootExhibitNumber; }
    public ProvenanceRecord setRootExhibitNumber(List<String> value) { this.rootExhibitNumber = value; return this; }

}