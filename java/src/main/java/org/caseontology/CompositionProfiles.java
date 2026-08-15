package org.caseontology;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Offline Composition Profile ids and keyword ranking. */
public final class CompositionProfiles {
    public static final String MINIMAL_FORENSICS = "MinimalForensics";
    public static final String AIR_GAPPED_FIELD_TRIAGE = "AirGappedFieldTriage";
    public static final String HASH_INTELLIGENCE = "HashIntelligence";
    public static final String TOOL_MAPPING = "ToolMapping";
    public static final String LEGAL_PROCESS = "LegalProcess";
    public static final String FULL_CAC_LIFECYCLE = "FullCACLifecycle";
    public static final String CROSS_ONTOLOGY = "CrossOntology";

    public static final String[] ALL = {
        MINIMAL_FORENSICS, AIR_GAPPED_FIELD_TRIAGE, HASH_INTELLIGENCE,
        TOOL_MAPPING, LEGAL_PROCESS, FULL_CAC_LIFECYCLE, CROSS_ONTOLOGY,
    };

    private CompositionProfiles() {}

    public static boolean requiresCac(String profileId) {
        return FULL_CAC_LIFECYCLE.equals(profileId) || CROSS_ONTOLOGY.equals(profileId);
    }

    public static String resolve(String profileId, String scenario) {
        if (profileId != null && !profileId.isEmpty()) {
            for (String id : ALL) {
                if (id.equalsIgnoreCase(profileId)) {
                    return id;
                }
            }
            throw new IllegalArgumentException("Unknown composition profile: " + profileId);
        }
        List<String> ranked = recommend(scenario);
        return ranked.isEmpty() ? MINIMAL_FORENSICS : ranked.get(0);
    }

    public static List<String> recommend(String scenario) {
        String query = scenario == null ? "" : scenario.toLowerCase(Locale.ROOT);
        List<int[]> scored = new ArrayList<>();
        for (int i = 0; i < ALL.length; i++) {
            int score = 0;
            if (query.contains(ALL[i].toLowerCase(Locale.ROOT))) {
                score += 8;
            }
            for (String token : keywords(ALL[i])) {
                if (query.contains(token)) {
                    score += 2;
                }
            }
            if (score > 0) {
                scored.add(new int[] { score, i });
            }
        }
        scored.sort((a, b) -> Integer.compare(b[0], a[0]));
        List<String> result = new ArrayList<>();
        for (int[] pair : scored) {
            result.add(ALL[pair[1]]);
        }
        return result;
    }

    static String[] keywords(String id) {
        switch (id) {
            case HASH_INTELLIGENCE:
                return new String[] { "hash", "photodna", "vics", "csam", "sha256", "perceptual" };
            case FULL_CAC_LIFECYCLE:
                return new String[] { "cac", "csam", "grooming", "trafficking", "cybertip", "ncmec", "child" };
            case AIR_GAPPED_FIELD_TRIAGE:
                return new String[] { "air", "offline", "field", "triage", "laptop" };
            case TOOL_MAPPING:
                return new String[] { "tool", "autopsy", "solve-it", "configured" };
            case LEGAL_PROCESS:
                return new String[] { "charge", "indictment", "plea", "sentence", "pacer" };
            case CROSS_ONTOLOGY:
                return new String[] { "gufo", "prov", "cross-ontology", "composition" };
            default:
                return new String[] { "file", "hash", "triage", "starter" };
        }
    }
}
