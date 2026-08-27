package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class CriminalCharge {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/CriminalCharge";

    private List<ChargingInstrument> assertedIn = new ArrayList<>();
    private String chargeClassification;
    private List<String> chargeDisposition = new ArrayList<>();
    private String countLabel;
    private List<long> countNumber = new ArrayList<>();
    private List<CriminalCharge> objectOffense = new ArrayList<>();
    private String offenseForm;
    private List<String> statuteCitation = new ArrayList<>();

    public List<ChargingInstrument> getAssertedIn() { return assertedIn; }
    public String getChargeClassification() { return chargeClassification; }
    public void setChargeClassification(String chargeClassification) { this.chargeClassification = chargeClassification; }
    public List<String> getChargeDisposition() { return chargeDisposition; }
    public String getCountLabel() { return countLabel; }
    public void setCountLabel(String countLabel) { this.countLabel = countLabel; }
    public List<long> getCountNumber() { return countNumber; }
    public List<CriminalCharge> getObjectOffense() { return objectOffense; }
    public String getOffenseForm() { return offenseForm; }
    public void setOffenseForm(String offenseForm) { this.offenseForm = offenseForm; }
    public List<String> getStatuteCitation() { return statuteCitation; }
}