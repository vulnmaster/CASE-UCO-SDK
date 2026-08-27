package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class PotentialPenalty {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/PotentialPenalty";

    private List<CriminalCharge> concernsCharge = new ArrayList<>();
    private String outcomeScope;
    private String potentialPenaltyKind;

    public List<CriminalCharge> getConcernsCharge() { return concernsCharge; }
    public String getOutcomeScope() { return outcomeScope; }
    public void setOutcomeScope(String outcomeScope) { this.outcomeScope = outcomeScope; }
    public String getPotentialPenaltyKind() { return potentialPenaltyKind; }
    public void setPotentialPenaltyKind(String potentialPenaltyKind) { this.potentialPenaltyKind = potentialPenaltyKind; }
}