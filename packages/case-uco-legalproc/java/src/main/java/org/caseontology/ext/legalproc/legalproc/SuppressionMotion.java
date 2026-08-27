package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class SuppressionMotion {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/SuppressionMotion";

    private String disclosureSourceCitation;
    private String proceedingType;

    public String getDisclosureSourceCitation() { return disclosureSourceCitation; }
    public void setDisclosureSourceCitation(String disclosureSourceCitation) { this.disclosureSourceCitation = disclosureSourceCitation; }
    public String getProceedingType() { return proceedingType; }
    public void setProceedingType(String proceedingType) { this.proceedingType = proceedingType; }
}