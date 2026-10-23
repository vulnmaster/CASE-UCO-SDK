// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: WindowsServiceStatus */
public final class WindowsServiceStatus {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStatus";
    public static final Set<String> MEMBERS = Set.of("service_continue_pending", "service_pause_pending", "service_paused", "service_running", "service_start_pending", "service_stop_pending", "service_stopped");
    public static final String SERVICE_CONTINUE_PENDING = "service_continue_pending";
    public static final String SERVICE_PAUSE_PENDING = "service_pause_pending";
    public static final String SERVICE_PAUSED = "service_paused";
    public static final String SERVICE_RUNNING = "service_running";
    public static final String SERVICE_START_PENDING = "service_start_pending";
    public static final String SERVICE_STOP_PENDING = "service_stop_pending";
    public static final String SERVICE_STOPPED = "service_stopped";

    private WindowsServiceStatus() {}
}
