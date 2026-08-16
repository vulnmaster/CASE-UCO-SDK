package org.caseontology;

import java.util.ArrayList;
import java.util.List;

/** A partition plan would widen marking or authorization access. */
public final class PartitionBoundaryException extends IllegalStateException {
    private static final long serialVersionUID = 1L;
    private final String rootId;
    private final String nodeId;
    private final ArrayList<String> missingMarkings;
    private final ArrayList<String> missingAuthorizations;

    public PartitionBoundaryException(
            String rootId,
            String nodeId,
            List<String> missingMarkings,
            List<String> missingAuthorizations) {
        super("partition root '" + rootId + "' is not authorized for node '" + nodeId
            + "'; missing markings=" + missingMarkings
            + ", missing authorizations=" + missingAuthorizations);
        this.rootId = rootId;
        this.nodeId = nodeId;
        this.missingMarkings = new ArrayList<>(missingMarkings);
        this.missingAuthorizations = new ArrayList<>(missingAuthorizations);
    }

    public String getRootId() { return rootId; }
    public String getNodeId() { return nodeId; }
    public List<String> getMissingMarkings() { return new ArrayList<>(missingMarkings); }
    public List<String> getMissingAuthorizations() { return new ArrayList<>(missingAuthorizations); }
}
