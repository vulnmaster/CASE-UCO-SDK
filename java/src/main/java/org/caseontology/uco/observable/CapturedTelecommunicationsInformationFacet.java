// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** A captured telecommunications information facet represents certain information within captured or intercepted telecommunications data. */
public class CapturedTelecommunicationsInformationFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformationFacet";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    @org.caseontology.CaseRequired
    private CellSite captureCellSite;
    private java.time.ZonedDateTime endTime;
    private String interceptedCallState;
    private java.time.ZonedDateTime startTime;

    public CapturedTelecommunicationsInformationFacet() {
    }

    public CellSite getCaptureCellSite() { return this.captureCellSite; }
    public CapturedTelecommunicationsInformationFacet setCaptureCellSite(CellSite value) { this.captureCellSite = value; return this; }

    public java.time.ZonedDateTime getEndTime() { return this.endTime; }
    public CapturedTelecommunicationsInformationFacet setEndTime(java.time.ZonedDateTime value) { this.endTime = value; return this; }

    public String getInterceptedCallState() { return this.interceptedCallState; }
    public CapturedTelecommunicationsInformationFacet setInterceptedCallState(String value) { this.interceptedCallState = value; return this; }

    public java.time.ZonedDateTime getStartTime() { return this.startTime; }
    public CapturedTelecommunicationsInformationFacet setStartTime(java.time.ZonedDateTime value) { this.startTime = value; return this; }

}