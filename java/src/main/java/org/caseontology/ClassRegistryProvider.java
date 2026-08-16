package org.caseontology;

import java.util.Collection;

/**
 * ServiceLoader contract for trusted typed CASE/UCO extension classes (#82).
 *
 * <p>Extension JARs publish an implementation in
 * {@code META-INF/services/org.caseontology.ClassRegistryProvider}. Duplicate
 * class IRIs always fail closed; priority is diagnostic ordering, not an
 * override mechanism.</p>
 */
public interface ClassRegistryProvider {
    String source();
    Collection<Class<?>> classes();
    default int priority() { return 0; }
}
