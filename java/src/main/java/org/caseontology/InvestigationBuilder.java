package org.caseontology;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Scenario + evidence → profile-aware CaseGraph with inline critique. */
public final class InvestigationBuilder {
    public static final class CritiqueFinding {
        public final String severity;
        public final String message;
        public final String path;

        public CritiqueFinding(String severity, String message, String path) {
            this.severity = severity;
            this.message = message;
            this.path = path;
        }
    }

    private final String scenario;
    private final String profileId;
    private final CaseGraph graph;
    private final List<CritiqueFinding> findings = new ArrayList<>();

    public InvestigationBuilder(String scenario) {
        this(scenario, null, "http://example.org/kb/");
    }

    public InvestigationBuilder(String scenario, String profileId) {
        this(scenario, profileId, "http://example.org/kb/");
    }

    public InvestigationBuilder(String scenario, String profileId, String kbPrefix) {
        this.scenario = scenario == null ? "" : scenario;
        this.profileId = CompositionProfiles.resolve(profileId, this.scenario);
        Map<String, String> extra = new LinkedHashMap<>();
        if (CompositionProfiles.requiresCac(this.profileId)) {
            extra.put("cac-core", "https://cacontology.projectvic.org/core#");
            extra.put("cacontology", "https://cacontology.projectvic.org#");
        }
        this.graph = extra.isEmpty() ? new CaseGraph(kbPrefix) : new CaseGraph(kbPrefix, extra);
    }

    public String getProfileId() { return profileId; }
    public CaseGraph getGraph() { return graph; }

    public Object addFile(String fileName, List<String[]> hashes) {
        List<String[]> list = hashes == null ? Collections.emptyList() : hashes;
        if (list.isEmpty()) {
            findings.add(new CritiqueFinding(
                "error", fileName + ": " + profileId + " requires ContentDataFacet hashes", fileName));
        }
        return CompositionHelpers.fileWithContentHashes(graph, fileName, list);
    }

    public CompositionHelpers.CsamEvidence addCsamEvidence(String fileName, List<String[]> hashes) {
        List<String[]> list = hashes == null ? Collections.emptyList() : hashes;
        if (list.isEmpty()) {
            findings.add(new CritiqueFinding(
                "error", fileName + ": CSAM evidence must carry hashes", fileName));
        }
        return CompositionHelpers.modelCsamEvidence(graph, fileName, list);
    }

    public CompositionHelpers.ToolRun addToolRun(String toolName, String actionName, String toolVersion) {
        if (toolVersion == null || toolVersion.isEmpty()) {
            findings.add(new CritiqueFinding("warning", "Tool " + toolName + " has no version", toolName));
        }
        return CompositionHelpers.modelToolRun(graph, toolName, actionName, toolVersion);
    }

    public CaseGraph build() { return graph; }

    public List<CritiqueFinding> critique() { return Collections.unmodifiableList(findings); }
}
