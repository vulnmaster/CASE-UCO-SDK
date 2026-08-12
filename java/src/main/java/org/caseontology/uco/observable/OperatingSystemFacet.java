// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;
import org.caseontology.uco.identity.Identity;
import org.caseontology.uco.types.Dictionary;

/** An operating system facet is a grouping of characteristics unique to the software that manages computer hardware, software resources, and provides common services for computer programs. [based on http */
public class OperatingSystemFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystemFacet";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    private List<String> advertisingID;
    private String bitness;
    private Dictionary environmentVariables;
    private java.time.ZonedDateTime installDate;
    private Boolean isLimitAdTrackingEnabled;
    private Identity manufacturer;
    private String version;

    public OperatingSystemFacet() {
        this.advertisingID = new ArrayList<>();
    }

    public List<String> getAdvertisingID() { return this.advertisingID; }
    public OperatingSystemFacet setAdvertisingID(List<String> value) { this.advertisingID = value; return this; }

    public String getBitness() { return this.bitness; }
    public OperatingSystemFacet setBitness(String value) { this.bitness = value; return this; }

    public Dictionary getEnvironmentVariables() { return this.environmentVariables; }
    public OperatingSystemFacet setEnvironmentVariables(Dictionary value) { this.environmentVariables = value; return this; }

    public java.time.ZonedDateTime getInstallDate() { return this.installDate; }
    public OperatingSystemFacet setInstallDate(java.time.ZonedDateTime value) { this.installDate = value; return this; }

    public Boolean getIsLimitAdTrackingEnabled() { return this.isLimitAdTrackingEnabled; }
    public OperatingSystemFacet setIsLimitAdTrackingEnabled(Boolean value) { this.isLimitAdTrackingEnabled = value; return this; }

    public Identity getManufacturer() { return this.manufacturer; }
    public OperatingSystemFacet setManufacturer(Identity value) { this.manufacturer = value; return this; }

    public String getVersion() { return this.version; }
    public OperatingSystemFacet setVersion(String value) { this.version = value; return this; }

}