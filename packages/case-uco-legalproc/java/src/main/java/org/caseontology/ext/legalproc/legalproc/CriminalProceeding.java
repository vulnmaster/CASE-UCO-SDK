package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class CriminalProceeding {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/CriminalProceeding";

    private String proceedingType;

    public String getProceedingType() { return proceedingType; }
    public void setProceedingType(String proceedingType) { this.proceedingType = proceedingType; }
}