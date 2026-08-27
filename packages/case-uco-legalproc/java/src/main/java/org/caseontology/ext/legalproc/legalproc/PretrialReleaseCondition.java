package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class PretrialReleaseCondition {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/PretrialReleaseCondition";

    private String releaseConditionKind;

    public String getReleaseConditionKind() { return releaseConditionKind; }
    public void setReleaseConditionKind(String releaseConditionKind) { this.releaseConditionKind = releaseConditionKind; }
}