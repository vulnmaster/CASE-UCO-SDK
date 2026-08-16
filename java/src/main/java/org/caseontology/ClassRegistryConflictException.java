package org.caseontology;

/** Actionable duplicate CLASS_IRI registration diagnostic (#82). */
public final class ClassRegistryConflictException extends IllegalStateException {
    private static final long serialVersionUID = 1L;
    private final String classIri;
    private final Class<?> existingClass;
    private final Class<?> conflictingClass;

    public ClassRegistryConflictException(
            String classIri, Class<?> existingClass, Class<?> conflictingClass) {
        super("Duplicate CLASS_IRI '" + classIri + "': "
            + existingClass.getName() + " vs " + conflictingClass.getName());
        this.classIri = classIri;
        this.existingClass = existingClass;
        this.conflictingClass = conflictingClass;
    }

    public String getClassIri() { return classIri; }
    public Class<?> getExistingClass() { return existingClass; }
    public Class<?> getConflictingClass() { return conflictingClass; }
}
