// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: WindowsServiceType */
public final class WindowsServiceType {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceType";
    public static final Set<String> MEMBERS = Set.of("service_file_system_driver", "service_kernel_driver", "service_win32_own_process", "service_win32_share_process");
    public static final String SERVICE_FILE_SYSTEM_DRIVER = "service_file_system_driver";
    public static final String SERVICE_KERNEL_DRIVER = "service_kernel_driver";
    public static final String SERVICE_WIN32_OWN_PROCESS = "service_win32_own_process";
    public static final String SERVICE_WIN32_SHARE_PROCESS = "service_win32_share_process";

    private WindowsServiceType() {}
}
