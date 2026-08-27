package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class DisclosureObligation {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/DisclosureObligation";

    private List<CriminalCharge> concernsCharge = new ArrayList<>();
    private List<UcoObject> concernsEvidence = new ArrayList<>();
    private String disclosureKind;
    private String disclosureSourceCitation;
    private String disclosureStatus;

    public List<CriminalCharge> getConcernsCharge() { return concernsCharge; }
    public List<UcoObject> getConcernsEvidence() { return concernsEvidence; }
    public String getDisclosureKind() { return disclosureKind; }
    public void setDisclosureKind(String disclosureKind) { this.disclosureKind = disclosureKind; }
    public String getDisclosureSourceCitation() { return disclosureSourceCitation; }
    public void setDisclosureSourceCitation(String disclosureSourceCitation) { this.disclosureSourceCitation = disclosureSourceCitation; }
    public String getDisclosureStatus() { return disclosureStatus; }
    public void setDisclosureStatus(String disclosureStatus) { this.disclosureStatus = disclosureStatus; }
}