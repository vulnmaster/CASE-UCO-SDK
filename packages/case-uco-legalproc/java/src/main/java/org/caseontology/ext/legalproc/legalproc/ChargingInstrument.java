package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class ChargingInstrument {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/criminal/ChargingInstrument";

    private String instrumentType;

    public String getInstrumentType() { return instrumentType; }
    public void setInstrumentType(String instrumentType) { this.instrumentType = instrumentType; }
}