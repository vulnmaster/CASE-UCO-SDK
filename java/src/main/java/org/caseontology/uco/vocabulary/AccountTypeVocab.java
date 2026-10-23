// Auto-generated CASE/UCO vocabulary — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.
package org.caseontology.uco.vocabulary;

import java.util.Set;

/** Vocabulary: AccountTypeVocab */
public final class AccountTypeVocab {
    public static final String IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/AccountTypeVocab";
    public static final Set<String> MEMBERS = Set.of("ldap", "nis", "openid", "radius", "tacacs", "unix", "windows_domain", "windows_local");
    public static final String LDAP = "ldap";
    public static final String NIS = "nis";
    public static final String OPENID = "openid";
    public static final String RADIUS = "radius";
    public static final String TACACS = "tacacs";
    public static final String UNIX = "unix";
    public static final String WINDOWS_DOMAIN = "windows_domain";
    public static final String WINDOWS_LOCAL = "windows_local";

    private AccountTypeVocab() {}
}
