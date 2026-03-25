// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.action;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** An action frequency facet is a grouping of characteristics unique to the frequency of occurrence for an action. */
public class ActionFrequencyFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/action/ActionFrequencyFacet";
    public static final String NAMESPACE_PREFIX = "uco-action";

    @org.caseontology.CaseRequired
    private java.math.BigDecimal rate;
    @org.caseontology.CaseRequired
    private String scale;
    private List<String> trend;
    @org.caseontology.CaseRequired
    private String units;

    public ActionFrequencyFacet() {
        this.trend = new ArrayList<>();
    }

    public java.math.BigDecimal getRate() { return this.rate; }
    public ActionFrequencyFacet setRate(java.math.BigDecimal value) { this.rate = value; return this; }

    public String getScale() { return this.scale; }
    public ActionFrequencyFacet setScale(String value) { this.scale = value; return this; }

    public List<String> getTrend() { return this.trend; }
    public ActionFrequencyFacet setTrend(List<String> value) { this.trend = value; return this; }

    public String getUnits() { return this.units; }
    public ActionFrequencyFacet setUnits(String value) { this.units = value; return this; }

}