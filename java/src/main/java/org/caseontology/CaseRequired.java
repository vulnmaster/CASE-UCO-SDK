package org.caseontology;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Marks a generated CASE/UCO field as required by the ontology.
 * CaseGraph validates these constraints before adding objects to the graph.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface CaseRequired {
}
