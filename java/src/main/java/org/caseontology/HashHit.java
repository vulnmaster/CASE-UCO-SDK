package org.caseontology;

/** One hit from {@link CaseGraph#lookupHash(String)}. */
public final class HashHit {
    public final String id;
    public final String method;

    public HashHit(String id, String method) {
        this.id = id;
        this.method = method;
    }
}
