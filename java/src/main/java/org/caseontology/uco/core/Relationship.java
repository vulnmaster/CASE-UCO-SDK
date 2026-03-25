// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.core;

import java.util.ArrayList;
import java.util.List;

/** A relationship is a grouping of characteristics unique to an assertion that one or more objects are related to another object in some way. */
public class Relationship extends UcoObject {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/core/Relationship";
    public static final String NAMESPACE_PREFIX = "uco-core";

    private List<java.time.ZonedDateTime> endTime;
    @org.caseontology.CaseRequired
    private boolean isDirectional;
    private String kindOfRelationship;
    @org.caseontology.CaseRequired
    private List<UcoObject> source;
    private List<java.time.ZonedDateTime> startTime;
    @org.caseontology.CaseRequired
    private UcoObject target;

    public Relationship() {
        this.endTime = new ArrayList<>();
        this.source = new ArrayList<>();
        this.startTime = new ArrayList<>();
    }

    public List<java.time.ZonedDateTime> getEndTime() { return this.endTime; }
    public Relationship setEndTime(List<java.time.ZonedDateTime> value) { this.endTime = value; return this; }

    public boolean getIsDirectional() { return this.isDirectional; }
    public Relationship setIsDirectional(boolean value) { this.isDirectional = value; return this; }

    public String getKindOfRelationship() { return this.kindOfRelationship; }
    public Relationship setKindOfRelationship(String value) { this.kindOfRelationship = value; return this; }

    public List<UcoObject> getSource() { return this.source; }
    public Relationship setSource(List<UcoObject> value) { this.source = value; return this; }

    public List<java.time.ZonedDateTime> getStartTime() { return this.startTime; }
    public Relationship setStartTime(List<java.time.ZonedDateTime> value) { this.startTime = value; return this; }

    public UcoObject getTarget() { return this.target; }
    public Relationship setTarget(UcoObject value) { this.target = value; return this; }

}