// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: WindowsServiceStartType */
public final class WindowsServiceStartType {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStartType";
    public static final Set<String> MEMBERS = Set.of("service_auto_start", "service_boot_start", "service_demand_start", "service_disabled", "service_system_alert");
    public static final String SERVICE_AUTO_START = "service_auto_start";
    public static final String SERVICE_BOOT_START = "service_boot_start";
    public static final String SERVICE_DEMAND_START = "service_demand_start";
    public static final String SERVICE_DISABLED = "service_disabled";
    public static final String SERVICE_SYSTEM_ALERT = "service_system_alert";

    private WindowsServiceStartType() {}
}
