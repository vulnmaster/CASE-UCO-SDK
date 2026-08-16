package org.caseontology;

import java.util.Map;

/** A partition set plus its reconstruction and validation manifest. */
public final class PartitionResult {
    private final Map<String, CaseGraph> partitions;
    private final Map<String, Object> manifest;

    public PartitionResult(Map<String, CaseGraph> partitions, Map<String, Object> manifest) {
        this.partitions = partitions;
        this.manifest = manifest;
    }

    public Map<String, CaseGraph> getPartitions() { return partitions; }
    public Map<String, Object> getManifest() { return manifest; }
}
