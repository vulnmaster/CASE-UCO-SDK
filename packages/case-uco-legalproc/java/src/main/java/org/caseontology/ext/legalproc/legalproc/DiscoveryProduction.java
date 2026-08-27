package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class DiscoveryProduction {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/DiscoveryProduction";

    private String disclosureSourceCitation;
    private List<DisclosureObligation> satisfiesObligation = new ArrayList<>();

    public String getDisclosureSourceCitation() { return disclosureSourceCitation; }
    public void setDisclosureSourceCitation(String disclosureSourceCitation) { this.disclosureSourceCitation = disclosureSourceCitation; }
    public List<DisclosureObligation> getSatisfiesObligation() { return satisfiesObligation; }
}