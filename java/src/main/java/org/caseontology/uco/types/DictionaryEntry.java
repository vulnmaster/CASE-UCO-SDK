// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.types;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.UcoInherentCharacterizationThing;

/** A dictionary entry is a single (term/key, value) pair. */
public class DictionaryEntry extends UcoInherentCharacterizationThing {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/types/DictionaryEntry";
    public static final String NAMESPACE_PREFIX = "uco-types";

    @org.caseontology.CaseRequired
    private String key;
    @org.caseontology.CaseRequired
    private String value;

    public DictionaryEntry() {
    }

    public String getKey() { return this.key; }
    public DictionaryEntry setKey(String value) { this.key = value; return this; }

    public String getValue() { return this.value; }
    public DictionaryEntry setValue(String value) { this.value = value; return this; }

}