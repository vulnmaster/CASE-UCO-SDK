// Profile-aware InvestigationBuilder — additive topology surface.

using System;
using System.Collections.Generic;

namespace CaseUco
{
    public sealed class CritiqueFinding
    {
        public string Severity { get; set; }
        public string Message { get; set; }
        public string Path { get; set; }
        public string RuleId { get; set; }
        public string FindingId { get; set; }
        public string RecommendedChange { get; set; }
        public string RepairHint { get; set; }
    }

    /// <summary>
    /// Scenario + evidence → profile-aware <see cref="CaseGraph"/> with inline critique.
    /// </summary>
    public sealed class InvestigationBuilder
    {
        public string Scenario { get; }
        public string ProfileId { get; }
        public CaseGraph Graph { get; }
        private readonly List<CritiqueFinding> _findings = new List<CritiqueFinding>();

        public InvestigationBuilder(string scenario, string profileId = null, string kbPrefix = "http://example.org/kb/")
        {
            Scenario = scenario ?? "";
            ProfileId = CompositionProfiles.Resolve(profileId, Scenario);
            var extra = new Dictionary<string, string>();
            if (CompositionProfiles.RequiresCac(ProfileId))
            {
                extra["cac-core"] = "https://cacontology.projectvic.org/core#";
                extra["cacontology"] = "https://cacontology.projectvic.org#";
            }
            Graph = new CaseGraph(kbPrefix, extra.Count > 0 ? extra : null);
        }

        public object AddFile(string fileName, IEnumerable<KeyValuePair<string, string>> hashes = null)
        {
            var list = hashes == null ? new List<KeyValuePair<string, string>>() : new List<KeyValuePair<string, string>>(hashes);
            if (list.Count == 0)
            {
                _findings.Add(new CritiqueFinding
                {
                    Severity = "error",
                    Message = fileName + ": " + ProfileId + " requires ContentDataFacet hashes",
                    Path = fileName,
                });
            }
            return CompositionHelpers.FileWithContentHashes(Graph, fileName, list);
        }

        public CsamEvidence AddCsamEvidence(string fileName, IEnumerable<KeyValuePair<string, string>> hashes)
        {
            var list = hashes == null ? new List<KeyValuePair<string, string>>() : new List<KeyValuePair<string, string>>(hashes);
            if (list.Count == 0)
            {
                _findings.Add(new CritiqueFinding
                {
                    Severity = "error",
                    Message = fileName + ": CSAM evidence must carry hashes",
                    Path = fileName,
                });
            }
            return CompositionHelpers.ModelCsamEvidence(Graph, fileName, list);
        }

        public ToolRun AddToolRun(string toolName, string actionName, string toolVersion = null)
        {
            if (string.IsNullOrEmpty(toolVersion))
            {
                _findings.Add(new CritiqueFinding
                {
                    Severity = "warning",
                    Message = "Tool " + toolName + " has no version",
                    Path = toolName,
                });
            }
            return CompositionHelpers.ModelToolRun(Graph, toolName, actionName, toolVersion);
        }

        public CaseGraph Build() => Graph;

        public IReadOnlyList<CritiqueFinding> Critique() => _findings;
    }
}
