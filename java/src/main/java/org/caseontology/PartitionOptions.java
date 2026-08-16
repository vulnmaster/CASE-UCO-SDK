package org.caseontology;

import java.util.LinkedHashMap;
import java.util.Map;

/** Options for marking-safe dependency partitioning (#79). */
public final class PartitionOptions {
    private String sharedNodePolicy = "replicate-identical";
    private boolean includeIncoming = true;
    private String boundaryPolicy = "none";
    private String crossBoundaryPolicy = "error-on-cross-boundary";
    private Map<String, PartitionBoundary> rootBoundaries = new LinkedHashMap<>();
    private Map<String, Object> validationBundle = new LinkedHashMap<>();
    private String manifestDetail = "full";

    public String getSharedNodePolicy() { return sharedNodePolicy; }
    public PartitionOptions setSharedNodePolicy(String value) { sharedNodePolicy = value; return this; }
    public boolean isIncludeIncoming() { return includeIncoming; }
    public PartitionOptions setIncludeIncoming(boolean value) { includeIncoming = value; return this; }
    public String getBoundaryPolicy() { return boundaryPolicy; }
    public PartitionOptions setBoundaryPolicy(String value) { boundaryPolicy = value; return this; }
    public String getCrossBoundaryPolicy() { return crossBoundaryPolicy; }
    public PartitionOptions setCrossBoundaryPolicy(String value) { crossBoundaryPolicy = value; return this; }
    public Map<String, PartitionBoundary> getRootBoundaries() { return rootBoundaries; }
    public PartitionOptions setRootBoundaries(Map<String, PartitionBoundary> value) {
        rootBoundaries = value == null ? new LinkedHashMap<>() : new LinkedHashMap<>(value);
        return this;
    }
    public Map<String, Object> getValidationBundle() { return validationBundle; }
    public PartitionOptions setValidationBundle(Map<String, Object> value) {
        validationBundle = value == null ? new LinkedHashMap<>() : new LinkedHashMap<>(value);
        return this;
    }
    public String getManifestDetail() { return manifestDetail; }
    public PartitionOptions setManifestDetail(String value) { manifestDetail = value; return this; }
}
