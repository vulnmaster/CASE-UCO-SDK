package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class Plea {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/Plea";

    private List<CriminalCharge> concernsCharge = new ArrayList<>();
    private String outcomeScope;
    private String pleaType;

    public List<CriminalCharge> getConcernsCharge() { return concernsCharge; }
    public String getOutcomeScope() { return outcomeScope; }
    public void setOutcomeScope(String outcomeScope) { this.outcomeScope = outcomeScope; }
    public String getPleaType() { return pleaType; }
    public void setPleaType(String pleaType) { this.pleaType = pleaType; }
}