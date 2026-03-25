// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.analysis;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.UcoInherentCharacterizationThing;

/** An artifact classification is a single specific assertion that a particular class of a classification taxonomy applies to something. */
public class ArtifactClassification extends UcoInherentCharacterizationThing {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/analysis/ArtifactClassification";
    public static final String NAMESPACE_PREFIX = "uco-analysis";

    @org.caseontology.CaseRequired
    private List<String> _class;
    private java.math.BigDecimal classificationConfidence;

    public ArtifactClassification() {
        this._class = new ArrayList<>();
    }

    public List<String> getClassValue() { return this._class; }
    public ArtifactClassification setClassValue(List<String> value) { this._class = value; return this; }

    public java.math.BigDecimal getClassificationConfidence() { return this.classificationConfidence; }
    public ArtifactClassification setClassificationConfidence(java.math.BigDecimal value) { this.classificationConfidence = value; return this; }

}