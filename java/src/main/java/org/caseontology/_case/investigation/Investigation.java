// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology._case.investigation;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.ContextualCompilation;

/** An investigation is a grouping of characteristics unique to an exploration of the facts involved in a cyber-relevant set of suspicious activity. */
public class Investigation extends ContextualCompilation {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/investigation/Investigation";
    public static final String NAMESPACE_PREFIX = "case-investigation";

    private List<String> focus;
    private List<String> investigationForm;
    private String investigationStatus;
    private List<Authorization> relevantAuthorization;
    private java.time.ZonedDateTime endTime;
    private java.time.ZonedDateTime startTime;

    public Investigation() {
        this.focus = new ArrayList<>();
        this.investigationForm = new ArrayList<>();
        this.relevantAuthorization = new ArrayList<>();
    }

    public List<String> getFocus() { return this.focus; }
    public Investigation setFocus(List<String> value) { this.focus = value; return this; }

    public List<String> getInvestigationForm() { return this.investigationForm; }
    public Investigation setInvestigationForm(List<String> value) { this.investigationForm = value; return this; }

    public String getInvestigationStatus() { return this.investigationStatus; }
    public Investigation setInvestigationStatus(String value) { this.investigationStatus = value; return this; }

    public List<Authorization> getRelevantAuthorization() { return this.relevantAuthorization; }
    public Investigation setRelevantAuthorization(List<Authorization> value) { this.relevantAuthorization = value; return this; }

    public java.time.ZonedDateTime getEndTime() { return this.endTime; }
    public Investigation setEndTime(java.time.ZonedDateTime value) { this.endTime = value; return this; }

    public java.time.ZonedDateTime getStartTime() { return this.startTime; }
    public Investigation setStartTime(java.time.ZonedDateTime value) { this.startTime = value; return this; }

}