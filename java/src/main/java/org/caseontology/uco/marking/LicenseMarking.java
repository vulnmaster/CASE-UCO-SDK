// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.marking;

import java.util.ArrayList;
import java.util.List;

/** A license marking is a grouping of characteristics unique to the expression of data marking definitions (restrictions, permissions, and other guidance for how data can be used and shared) to convey de */
public class LicenseMarking extends MarkingModel {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/marking/LicenseMarking";
    public static final String NAMESPACE_PREFIX = "uco-marking";

    private List<String> definitionType;
    @org.caseontology.CaseRequired
    private String license;

    public LicenseMarking() {
        this.definitionType = new ArrayList<>();
    }

    public List<String> getDefinitionType() { return this.definitionType; }
    public LicenseMarking setDefinitionType(List<String> value) { this.definitionType = value; return this; }

    public String getLicense() { return this.license; }
    public LicenseMarking setLicense(String value) { this.license = value; return this; }

}