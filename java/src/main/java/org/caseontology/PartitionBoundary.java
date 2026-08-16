package org.caseontology;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/** Marking and authorization scope allowed for one partition root (#79). */
public final class PartitionBoundary {
    private final List<String> markings;
    private final List<String> authorizations;

    public PartitionBoundary(Collection<String> markings, Collection<String> authorizations) {
        this.markings = markings == null ? new ArrayList<>() : new ArrayList<>(markings);
        this.authorizations = authorizations == null ? new ArrayList<>() : new ArrayList<>(authorizations);
    }

    public List<String> getMarkings() { return new ArrayList<>(markings); }
    public List<String> getAuthorizations() { return new ArrayList<>(authorizations); }
}
