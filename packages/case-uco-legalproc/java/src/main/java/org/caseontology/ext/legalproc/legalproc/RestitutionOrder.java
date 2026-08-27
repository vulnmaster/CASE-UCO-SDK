package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class RestitutionOrder {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/RestitutionOrder";

    private String currencyCode;
    private java.math.BigDecimal monetaryAmount;

    public String getCurrencyCode() { return currencyCode; }
    public void setCurrencyCode(String currencyCode) { this.currencyCode = currencyCode; }
    public java.math.BigDecimal getMonetaryAmount() { return monetaryAmount; }
    public void setMonetaryAmount(java.math.BigDecimal monetaryAmount) { this.monetaryAmount = monetaryAmount; }
}