package org.caseontology;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Logical InvestigationWorkflow: persist workflow-state.json and advance a step cursor. */
public final class InvestigationWorkflow {
    public final String workflowId;
    public final String profileId;
    public final Path workingDir;
    public final InvestigationBuilder builder;
    public final List<String> completedSteps = new ArrayList<String>();

    public InvestigationWorkflow(String workflowId, String scenario, Path workingDir, String profileId) {
        this.workflowId = workflowId;
        this.workingDir = workingDir;
        this.profileId = profileId != null ? profileId : defaultProfile(workflowId);
        this.builder = new InvestigationBuilder(scenario == null ? workflowId : scenario, this.profileId);
        try {
            Files.createDirectories(workingDir);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    public static InvestigationWorkflow resume(Path workingDir) {
        try {
            String text = Files.readString(workingDir.resolve("workflow-state.json"), StandardCharsets.UTF_8);
            String workflowId = extract(text, "workflow_id");
            String profileId = extract(text, "profile_id");
            String scenario = extract(text, "scenario");
            return new InvestigationWorkflow(
                workflowId == null ? "field-triage" : workflowId,
                scenario,
                workingDir,
                profileId
            );
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    public String step() {
        String next = nextStep();
        if (next == null) {
            return null;
        }
        if ("open".equals(next)) {
            builder.addToolRun("Triage Collector", "scan", "1.0");
        }
        completedSteps.add(next);
        save();
        return next;
    }

    public void save() {
        StringBuilder completed = new StringBuilder();
        for (int i = 0; i < completedSteps.size(); i++) {
            if (i > 0) completed.append(',');
            completed.append('"').append(completedSteps.get(i)).append('"');
        }
        String json = "{\"schema_version\":\"1.0.0\",\"workflow_id\":\"" + workflowId
            + "\",\"profile_id\":\"" + profileId
            + "\",\"status\":\"running\",\"cursor\":{\"completed_steps\":[" + completed + "]}}";
        try {
            Files.writeString(workingDir.resolve("workflow-state.json"), json, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    private String nextStep() {
        String[] order = {"load", "open", "tool", "ingest", "hash", "critique", "validate", "emit"};
        for (String step : order) {
            if (!completedSteps.contains(step)) {
                return step;
            }
        }
        return null;
    }

    private static String defaultProfile(String workflowId) {
        if ("hash-intelligence-vics".equals(workflowId) || "cac-csam-provenance".equals(workflowId)) {
            return CompositionProfiles.HASH_INTELLIGENCE;
        }
        if ("cac-grooming-chat".equals(workflowId)) {
            return CompositionProfiles.FULL_CAC_LIFECYCLE;
        }
        return CompositionProfiles.AIR_GAPPED_FIELD_TRIAGE;
    }

    private static String extract(String json, String key) {
        String needle = "\"" + key + "\"";
        int idx = json.indexOf(needle);
        if (idx < 0) return null;
        int colon = json.indexOf(':', idx);
        int first = json.indexOf('"', colon + 1);
        int second = json.indexOf('"', first + 1);
        if (first < 0 || second < 0) return null;
        return json.substring(first + 1, second);
    }
}
