// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.core;

import java.util.ArrayList;
import java.util.List;

/** A controlled vocabulary is an explicitly constrained set of string values. */
public class ControlledVocabulary extends UcoObject {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/core/ControlledVocabulary";
    public static final String NAMESPACE_PREFIX = "uco-core";

    private String constrainingVocabularyName;
    private java.net.URI constrainingVocabularyReference;
    @org.caseontology.CaseRequired
    private String value;

    public ControlledVocabulary() {
    }

    public String getConstrainingVocabularyName() { return this.constrainingVocabularyName; }
    public ControlledVocabulary setConstrainingVocabularyName(String value) { this.constrainingVocabularyName = value; return this; }

    public java.net.URI getConstrainingVocabularyReference() { return this.constrainingVocabularyReference; }
    public ControlledVocabulary setConstrainingVocabularyReference(java.net.URI value) { this.constrainingVocabularyReference = value; return this; }

    public String getValue() { return this.value; }
    public ControlledVocabulary setValue(String value) { this.value = value; return this; }

}