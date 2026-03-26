// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology._case.investigation;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.UcoObject;

/** An authorization is a grouping of characteristics unique to some form of authoritative permission identified for investigative action. */
public class Authorization extends UcoObject {
    public static final String CLASS_IRI = "https://ontology.caseontology.org/case/investigation/Authorization";
    public static final String NAMESPACE_PREFIX = "case-investigation";

    private List<String> authorizationIdentifier;
    private String authorizationType;
    private java.time.ZonedDateTime endTime;
    private java.time.ZonedDateTime startTime;

    public Authorization() {
        this.authorizationIdentifier = new ArrayList<>();
    }

    public List<String> getAuthorizationIdentifier() { return this.authorizationIdentifier; }
    public Authorization setAuthorizationIdentifier(List<String> value) { this.authorizationIdentifier = value; return this; }

    public String getAuthorizationType() { return this.authorizationType; }
    public Authorization setAuthorizationType(String value) { this.authorizationType = value; return this; }

    public java.time.ZonedDateTime getEndTime() { return this.endTime; }
    public Authorization setEndTime(java.time.ZonedDateTime value) { this.endTime = value; return this; }

    public java.time.ZonedDateTime getStartTime() { return this.startTime; }
    public Authorization setStartTime(java.time.ZonedDateTime value) { this.startTime = value; return this; }

}