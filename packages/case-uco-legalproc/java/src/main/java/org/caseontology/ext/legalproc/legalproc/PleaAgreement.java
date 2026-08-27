package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class PleaAgreement {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/PleaAgreement";

    private List<CriminalCharge> concernsCharge = new ArrayList<>();
    private String outcomeScope;
    private List<Plea> recordsPlea = new ArrayList<>();

    public List<CriminalCharge> getConcernsCharge() { return concernsCharge; }
    public String getOutcomeScope() { return outcomeScope; }
    public void setOutcomeScope(String outcomeScope) { this.outcomeScope = outcomeScope; }
    public List<Plea> getRecordsPlea() { return recordsPlea; }
}