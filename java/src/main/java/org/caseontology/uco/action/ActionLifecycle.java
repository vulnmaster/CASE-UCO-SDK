// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.action;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.UcoObject;

/** An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subordinate action lifecycles. */
public class ActionLifecycle extends Action {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/action/ActionLifecycle";
    public static final String NAMESPACE_PREFIX = "uco-action";

    private List<Long> actionCount;
    private List<java.time.ZonedDateTime> endTime;
    private List<UcoObject> error;
    @org.caseontology.CaseRequired
    private ArrayOfAction phase;
    private List<java.time.ZonedDateTime> startTime;

    public ActionLifecycle() {
        this.actionCount = new ArrayList<>();
        this.endTime = new ArrayList<>();
        this.error = new ArrayList<>();
        this.startTime = new ArrayList<>();
    }

    public List<Long> getActionCountValue() { return this.actionCount; }
    public ActionLifecycle setActionCountValue(List<Long> value) { this.actionCount = value; return this; }

    public List<java.time.ZonedDateTime> getEndTimeValue() { return this.endTime; }
    public ActionLifecycle setEndTimeValue(List<java.time.ZonedDateTime> value) { this.endTime = value; return this; }

    public List<UcoObject> getErrorValue() { return this.error; }
    public ActionLifecycle setErrorValue(List<UcoObject> value) { this.error = value; return this; }

    public ArrayOfAction getPhase() { return this.phase; }
    public ActionLifecycle setPhase(ArrayOfAction value) { this.phase = value; return this; }

    public List<java.time.ZonedDateTime> getStartTimeValue() { return this.startTime; }
    public ActionLifecycle setStartTimeValue(List<java.time.ZonedDateTime> value) { this.startTime = value; return this; }

}