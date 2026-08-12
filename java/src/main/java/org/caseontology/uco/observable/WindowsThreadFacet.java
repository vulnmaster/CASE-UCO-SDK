// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** A Windows thread facet is a grouping os characteristics unique to a single thread of execution within a Windows process. */
public class WindowsThreadFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThreadFacet";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    private String context;
    private List<Long> creationFlags;
    private java.time.ZonedDateTime creationTime;
    private java.time.ZonedDateTime observableCreatedTime;
    private List<byte[]> parameterAddress;
    private Long priority;
    private String runningStatus;
    private String securityAttributes;
    private List<Long> stackSize;
    private List<byte[]> startAddress;
    private List<Long> threadID;

    public WindowsThreadFacet() {
        this.creationFlags = new ArrayList<>();
        this.parameterAddress = new ArrayList<>();
        this.stackSize = new ArrayList<>();
        this.startAddress = new ArrayList<>();
        this.threadID = new ArrayList<>();
    }

    public String getContext() { return this.context; }
    public WindowsThreadFacet setContext(String value) { this.context = value; return this; }

    public List<Long> getCreationFlags() { return this.creationFlags; }
    public WindowsThreadFacet setCreationFlags(List<Long> value) { this.creationFlags = value; return this; }

    public java.time.ZonedDateTime getCreationTime() { return this.creationTime; }
    public WindowsThreadFacet setCreationTime(java.time.ZonedDateTime value) { this.creationTime = value; return this; }

    public java.time.ZonedDateTime getObservableCreatedTime() { return this.observableCreatedTime; }
    public WindowsThreadFacet setObservableCreatedTime(java.time.ZonedDateTime value) { this.observableCreatedTime = value; return this; }

    public List<byte[]> getParameterAddress() { return this.parameterAddress; }
    public WindowsThreadFacet setParameterAddress(List<byte[]> value) { this.parameterAddress = value; return this; }

    public Long getPriority() { return this.priority; }
    public WindowsThreadFacet setPriority(Long value) { this.priority = value; return this; }

    public String getRunningStatus() { return this.runningStatus; }
    public WindowsThreadFacet setRunningStatus(String value) { this.runningStatus = value; return this; }

    public String getSecurityAttributes() { return this.securityAttributes; }
    public WindowsThreadFacet setSecurityAttributes(String value) { this.securityAttributes = value; return this; }

    public List<Long> getStackSize() { return this.stackSize; }
    public WindowsThreadFacet setStackSize(List<Long> value) { this.stackSize = value; return this; }

    public List<byte[]> getStartAddress() { return this.startAddress; }
    public WindowsThreadFacet setStartAddress(List<byte[]> value) { this.startAddress = value; return this; }

    public List<Long> getThreadID() { return this.threadID; }
    public WindowsThreadFacet setThreadID(List<Long> value) { this.threadID = value; return this; }

}