package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class FederalCharge {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/FederalCharge";

    private String jurisdictionKind;

    public String getJurisdictionKind() { return jurisdictionKind; }
    public void setJurisdictionKind(String jurisdictionKind) { this.jurisdictionKind = jurisdictionKind; }
}