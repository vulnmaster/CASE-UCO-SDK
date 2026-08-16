package org.caseontology;

/** Exact JSON-LD node-union verification evidence. */
public final class PartitionUnionVerification {
    private final boolean equivalent;
    private final int sourceNodes;
    private final int unionNodes;

    public PartitionUnionVerification(boolean equivalent, int sourceNodes, int unionNodes) {
        this.equivalent = equivalent;
        this.sourceNodes = sourceNodes;
        this.unionNodes = unionNodes;
    }

    public boolean isEquivalent() { return equivalent; }
    public int getSourceNodes() { return sourceNodes; }
    public int getUnionNodes() { return unionNodes; }
}
