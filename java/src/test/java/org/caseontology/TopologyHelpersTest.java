package org.caseontology;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import org.junit.Test;
import static org.junit.Assert.*;

public class TopologyHelpersTest {

    @Test
    public void fileWithContentHashesIsIndexed() {
        CaseGraph graph = new CaseGraph();
        CompositionHelpers.fileWithContentHashes(
            graph, "evidence.bin",
            Collections.singletonList(new String[] { "SHA256", "e3b0c44298fc1c149afbf4c8996fb924" }));
        List<HashHit> hits = graph.lookupHash("E3B0C44298FC1C149AFBF4C8996FB924");
        assertFalse(hits.isEmpty());
        assertEquals("SHA256", hits.get(0).method);
    }

    @Test
    public void modelCsamEvidenceHashIntelligenceShape() {
        CaseGraph graph = new CaseGraph();
        CompositionHelpers.CsamEvidence parts = CompositionHelpers.modelCsamEvidence(
            graph, "img.jpg",
            Arrays.asList(
                new String[] { "SHA256", "aa" },
                new String[] { "PhotoDNA", "bb" }));
        assertEquals("PhotoDNA", parts.tool.getName());
        assertTrue(graph.size() >= 3);
        String json = graph.serialize();
        assertTrue(json.contains("uco-observable:RasterPicture"));
        assertTrue(json.contains("SHA256"));
        assertTrue(json.contains("PhotoDNA"));
        assertTrue(json.contains("xsd:hexBinary"));
    }

    @Test
    public void investigationBuilderInlineCritique() {
        InvestigationBuilder builder = new InvestigationBuilder(
            "field triage of hashed images", CompositionProfiles.AIR_GAPPED_FIELD_TRIAGE);
        builder.addFile("nohash.txt", null);
        builder.addFile("ok.bin", Collections.singletonList(new String[] { "SHA256", "ab" }));
        builder.addToolRun("Triage Collector", "scan", null);
        boolean sawError = false;
        boolean sawVersion = false;
        for (InvestigationBuilder.CritiqueFinding f : builder.critique()) {
            if ("error".equals(f.severity)) sawError = true;
            if (f.message.contains("version")) sawVersion = true;
        }
        assertTrue(sawError);
        assertTrue(sawVersion);
        assertEquals(CompositionProfiles.AIR_GAPPED_FIELD_TRIAGE, builder.getProfileId());
        assertEquals("field triage of hashed images", builder.getScenario());
        assertTrue(builder.build().size() >= 2);
    }

    @Test
    public void partitionByProfileReturnsCore() {
        CaseGraph graph = new CaseGraph();
        CompositionHelpers.fileWithContentHashes(
            graph, "a.bin", Collections.singletonList(new String[] { "SHA256", "cc" }));
        Map<String, CaseGraph> parts = graph.partitionByProfile(CompositionProfiles.MINIMAL_FORENSICS);
        assertTrue(parts.containsKey("core"));
    }

    @Test
    public void profileContractLoadHashIntelligence() {
        ProfileContract contract = ProfileContract.load(CompositionProfiles.HASH_INTELLIGENCE);
        assertEquals(CompositionProfiles.HASH_INTELLIGENCE, contract.profileId);
        assertTrue(contract.checkIds.contains("PROF-HI-001"));
    }

    @Test
    public void requiresCacHashIntelligenceIsFalse() {
        assertFalse(CompositionProfiles.requiresCac(CompositionProfiles.HASH_INTELLIGENCE));
        assertTrue(CompositionProfiles.requiresCac(CompositionProfiles.FULL_CAC_LIFECYCLE));
    }

    @Test
    public void investigationWorkflowStepAndSave() throws Exception {
        Path dir = Files.createTempDirectory("case-uco-wf-");
        InvestigationWorkflow wf = new InvestigationWorkflow("field-triage", "seized laptop", dir, null);
        assertEquals("load", wf.step());
        assertTrue(Files.exists(dir.resolve("workflow-state.json")));
    }
}
