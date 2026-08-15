package org.caseontology;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Logical ProfileContract surface (v2). Offline, synthesized checks. */
public final class ProfileContract {
    public final String profileId;
    public final String profileVersion;
    public final String contractSchemaVersion;
    public final List<String> checkIds;

    public ProfileContract(String profileId, String profileVersion, String schemaVersion, List<String> checkIds) {
        this.profileId = profileId;
        this.profileVersion = profileVersion;
        this.contractSchemaVersion = schemaVersion;
        this.checkIds = Collections.unmodifiableList(new ArrayList<>(checkIds));
    }

    public static ProfileContract load(String profileId) {
        String id = CompositionProfiles.resolve(profileId, "");
        List<String> checks = new ArrayList<String>();
        checks.add("PROF-FACET-001");
        checks.add("PROF-HASH-001");
        checks.add("PROF-TOOL-001");
        checks.add("PROF-SHACL-001");
        if (CompositionProfiles.HASH_INTELLIGENCE.equals(id)) {
            checks.add("PROF-HI-001");
            checks.add("PROF-HI-002");
        }
        if (CompositionProfiles.FULL_CAC_LIFECYCLE.equals(id)) {
            checks.add("PROF-CAC-001");
        }
        if (CompositionProfiles.AIR_GAPPED_FIELD_TRIAGE.equals(id)) {
            checks.add("PROF-AIR-001");
        }
        return new ProfileContract(id, "1.0.0", "1.0.0", checks);
    }
}
