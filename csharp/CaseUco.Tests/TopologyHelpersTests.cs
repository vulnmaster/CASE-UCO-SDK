using System.Collections.Generic;
using CaseUco;
using Xunit;

namespace CaseUco.Tests
{
    public class TopologyHelpersTests
    {
        [Fact]
        public void FileWithContentHashes_IsIndexed()
        {
            var graph = new CaseGraph();
            CompositionHelpers.FileWithContentHashes(
                graph,
                "evidence.bin",
                new[] { new KeyValuePair<string, string>("SHA256", "e3b0c44298fc1c149afbf4c8996fb924") });
            var hits = graph.LookupHash("E3B0C44298FC1C149AFBF4C8996FB924");
            Assert.NotEmpty(hits);
            Assert.Equal("SHA256", hits[0].Method);
        }

        [Fact]
        public void ModelCsamEvidence_HashIntelligenceShape()
        {
            var graph = new CaseGraph();
            var parts = CompositionHelpers.ModelCsamEvidence(
                graph,
                "img.jpg",
                new[]
                {
                    new KeyValuePair<string, string>("SHA256", "aa"),
                    new KeyValuePair<string, string>("PhotoDNA", "bb"),
                });
            Assert.Equal("PhotoDNA", parts.Tool.Name);
            Assert.True(graph.Count >= 3);
            var json = graph.Serialize();
            Assert.Contains("uco-observable:RasterPicture", json);
            Assert.Contains("SHA256", json);
            Assert.Contains("PhotoDNA", json);
            Assert.Contains("xsd:hexBinary", json);
        }

        [Fact]
        public void InvestigationBuilder_InlineCritique()
        {
            var builder = new InvestigationBuilder("field triage of hashed images", CompositionProfiles.AirGappedFieldTriage);
            builder.AddFile("nohash.txt");
            builder.AddFile("ok.bin", new[] { new KeyValuePair<string, string>("SHA256", "ab") });
            builder.AddToolRun("Triage Collector", "scan", null);
            Assert.Contains(builder.Critique(), f => f.Severity == "error");
            Assert.Contains(builder.Critique(), f => f.Message.Contains("version"));
            Assert.Equal(CompositionProfiles.AirGappedFieldTriage, builder.ProfileId);
            Assert.True(builder.Build().Count >= 2);
        }

        [Fact]
        public void PartitionByProfile_ReturnsCore()
        {
            var graph = new CaseGraph();
            CompositionHelpers.FileWithContentHashes(
                graph, "a.bin", new[] { new KeyValuePair<string, string>("SHA256", "cc") });
            var parts = graph.PartitionByProfile(CompositionProfiles.MinimalForensics);
            Assert.True(parts.ContainsKey("core"));
        }

        [Fact]
        public void ProfileContract_Load_HashIntelligence()
        {
            var contract = ProfileContract.Load(CompositionProfiles.HashIntelligence);
            Assert.Equal(CompositionProfiles.HashIntelligence, contract.ProfileId);
            Assert.Contains("PROF-HI-001", contract.CheckIds);
        }

        [Fact]
        public void RequiresCac_HashIntelligence_IsFalse()
        {
            Assert.False(CompositionProfiles.RequiresCac(CompositionProfiles.HashIntelligence));
            Assert.True(CompositionProfiles.RequiresCac(CompositionProfiles.FullCACLifecycle));
        }

        [Fact]
        public void InvestigationWorkflow_StepAndSave()
        {
            var dir = System.IO.Path.Combine(System.IO.Path.GetTempPath(), "case-uco-wf-" + System.Guid.NewGuid().ToString("N"));
            var wf = new InvestigationWorkflow("field-triage", "seized laptop", dir);
            Assert.Equal("load", wf.Step());
            Assert.True(System.IO.File.Exists(System.IO.Path.Combine(dir, "workflow-state.json")));
        }

        [Fact]
        public void InvestigationWorkflow_ResumeRestoresCompletedSteps()
        {
            var dir = System.IO.Path.Combine(System.IO.Path.GetTempPath(), "case-uco-wf-" + System.Guid.NewGuid().ToString("N"));
            var wf = new InvestigationWorkflow("field-triage", "seized laptop", dir);
            Assert.Equal("load", wf.Step());
            var resumed = InvestigationWorkflow.Resume(dir);
            Assert.Contains("load", resumed.CompletedSteps);
            Assert.Equal("open", resumed.Step());
        }

        [Fact]
        public void ProfileContract_Load_FullCacIncludesSpineChecks()
        {
            var contract = ProfileContract.Load(CompositionProfiles.FullCACLifecycle);
            Assert.Contains("PROF-CAC-003", contract.CheckIds);
            Assert.Contains("PROF-LEGAL-001", ProfileContract.Load(CompositionProfiles.LegalProcess).CheckIds);
        }
    }
}
