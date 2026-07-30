// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler). [based on http://ms */
public class WindowsTaskFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTaskFacet";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    private ObservableObject account;
    private String accountLogonType;
    private String accountRunLevel;
    private List<TaskActionType> actionList;
    private ObservableObject application;
    private Long exitCode;
    private List<String> flags;
    private String imageName;
    private Long maxRunTime;
    private java.time.ZonedDateTime mostRecentRunTime;
    private java.time.ZonedDateTime nextRunTime;
    private java.time.ZonedDateTime observableCreatedTime;
    private String parameters;
    private Object priority;
    private String status;
    private String taskComment;
    private String taskCreator;
    private List<TriggerType> triggerList;
    private ObservableObject workItemData;
    private ObservableObject workingDirectory;

    public WindowsTaskFacet() {
        this.actionList = new ArrayList<>();
        this.flags = new ArrayList<>();
        this.triggerList = new ArrayList<>();
    }

    public ObservableObject getAccount() { return this.account; }
    public WindowsTaskFacet setAccount(ObservableObject value) { this.account = value; return this; }

    public String getAccountLogonType() { return this.accountLogonType; }
    public WindowsTaskFacet setAccountLogonType(String value) { this.accountLogonType = value; return this; }

    public String getAccountRunLevel() { return this.accountRunLevel; }
    public WindowsTaskFacet setAccountRunLevel(String value) { this.accountRunLevel = value; return this; }

    public List<TaskActionType> getActionList() { return this.actionList; }
    public WindowsTaskFacet setActionList(List<TaskActionType> value) { this.actionList = value; return this; }

    public ObservableObject getApplication() { return this.application; }
    public WindowsTaskFacet setApplication(ObservableObject value) { this.application = value; return this; }

    public Long getExitCode() { return this.exitCode; }
    public WindowsTaskFacet setExitCode(Long value) { this.exitCode = value; return this; }

    public List<String> getFlags() { return this.flags; }
    public WindowsTaskFacet setFlags(List<String> value) { this.flags = value; return this; }

    public String getImageName() { return this.imageName; }
    public WindowsTaskFacet setImageName(String value) { this.imageName = value; return this; }

    public Long getMaxRunTime() { return this.maxRunTime; }
    public WindowsTaskFacet setMaxRunTime(Long value) { this.maxRunTime = value; return this; }

    public java.time.ZonedDateTime getMostRecentRunTime() { return this.mostRecentRunTime; }
    public WindowsTaskFacet setMostRecentRunTime(java.time.ZonedDateTime value) { this.mostRecentRunTime = value; return this; }

    public java.time.ZonedDateTime getNextRunTime() { return this.nextRunTime; }
    public WindowsTaskFacet setNextRunTime(java.time.ZonedDateTime value) { this.nextRunTime = value; return this; }

    public java.time.ZonedDateTime getObservableCreatedTime() { return this.observableCreatedTime; }
    public WindowsTaskFacet setObservableCreatedTime(java.time.ZonedDateTime value) { this.observableCreatedTime = value; return this; }

    public String getParameters() { return this.parameters; }
    public WindowsTaskFacet setParameters(String value) { this.parameters = value; return this; }

    public Object getPriority() { return this.priority; }
    public WindowsTaskFacet setPriority(Object value) { this.priority = value; return this; }

    public String getStatus() { return this.status; }
    public WindowsTaskFacet setStatus(String value) { this.status = value; return this; }

    public String getTaskComment() { return this.taskComment; }
    public WindowsTaskFacet setTaskComment(String value) { this.taskComment = value; return this; }

    public String getTaskCreator() { return this.taskCreator; }
    public WindowsTaskFacet setTaskCreator(String value) { this.taskCreator = value; return this; }

    public List<TriggerType> getTriggerList() { return this.triggerList; }
    public WindowsTaskFacet setTriggerList(List<TriggerType> value) { this.triggerList = value; return this; }

    public ObservableObject getWorkItemData() { return this.workItemData; }
    public WindowsTaskFacet setWorkItemData(ObservableObject value) { this.workItemData = value; return this; }

    public ObservableObject getWorkingDirectory() { return this.workingDirectory; }
    public WindowsTaskFacet setWorkingDirectory(ObservableObject value) { this.workingDirectory = value; return this; }

}