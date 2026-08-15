// Logical InvestigationWorkflow surface: load/save workflow-state.json + step cursor.
// 2.1: full hash_media / adapter / partition handlers (Python-parity). This
// surface stays sequential. RegisterHandler is the extension point.

using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace CaseUco
{
    public interface IWorkflowStepHandler
    {
        string StepId { get; }
        void Execute(InvestigationWorkflow workflow);
    }

    public sealed class InvestigationWorkflow
    {
        static readonly Dictionary<string, IWorkflowStepHandler> ExtraHandlers =
            new Dictionary<string, IWorkflowStepHandler>(StringComparer.Ordinal);

        public string WorkflowId { get; }
        public string ProfileId { get; }
        public string WorkingDir { get; }
        public InvestigationBuilder Builder { get; }
        public List<string> CompletedSteps { get; } = new List<string>();

        public InvestigationWorkflow(string workflowId, string scenario, string workingDir, string profileId = null)
        {
            WorkflowId = workflowId ?? throw new ArgumentNullException(nameof(workflowId));
            WorkingDir = workingDir ?? throw new ArgumentNullException(nameof(workingDir));
            Directory.CreateDirectory(WorkingDir);
            ProfileId = profileId ?? DefaultProfile(workflowId);
            Builder = new InvestigationBuilder(scenario ?? workflowId, ProfileId);
        }

        /// <summary>2.1 extension point. Built-in steps still advance the cursor if no handler is registered.</summary>
        public static void RegisterHandler(IWorkflowStepHandler handler)
        {
            if (handler == null) throw new ArgumentNullException(nameof(handler));
            ExtraHandlers[handler.StepId] = handler;
        }

        public static void ClearHandlers()
        {
            ExtraHandlers.Clear();
        }

        public static InvestigationWorkflow Resume(string workingDir)
        {
            var statePath = Path.Combine(workingDir, "workflow-state.json");
            var text = File.ReadAllText(statePath, Encoding.UTF8);
            var workflowId = ExtractJsonString(text, "workflow_id") ?? "field-triage";
            var profileId = ExtractJsonString(text, "profile_id");
            var scenario = ExtractJsonString(text, "scenario") ?? workflowId;
            var wf = new InvestigationWorkflow(workflowId, scenario, workingDir, profileId);
            wf.CompletedSteps.AddRange(ExtractJsonStringArray(text, "completed_steps"));
            var graphPath = Path.Combine(workingDir, "default.jsonld");
            if (File.Exists(graphPath))
                wf.Builder.Graph.LoadFile(graphPath);
            return wf;
        }

        public string Step()
        {
            var next = NextStep();
            if (next == null)
                return null;
            IWorkflowStepHandler extra;
            if (ExtraHandlers.TryGetValue(next, out extra))
                extra.Execute(this);
            else if (next == "open")
                Builder.AddToolRun("Triage Collector", "scan", "1.0");
            CompletedSteps.Add(next);
            Save();
            return next;
        }

        public void Save()
        {
            var path = Path.Combine(WorkingDir, "workflow-state.json");
            var completed = string.Join("\",\"", CompletedSteps.ToArray());
            var json = "{\"schema_version\":\"1.0.0\",\"workflow_id\":\"" + WorkflowId +
                       "\",\"profile_id\":\"" + ProfileId +
                       "\",\"scenario\":\"" + Escape(Builder.Scenario) +
                       "\",\"status\":\"running\",\"cursor\":{\"completed_steps\":[" +
                       (CompletedSteps.Count > 0 ? "\"" + completed + "\"" : "") +
                       "]}}";
            File.WriteAllText(path, json, Encoding.UTF8);
            Builder.Graph.Write(Path.Combine(WorkingDir, "default.jsonld"));
        }

        string NextStep()
        {
            var order = new[] { "load", "open", "tool", "ingest", "hash", "critique", "validate", "emit" };
            foreach (var step in order)
            {
                if (!CompletedSteps.Contains(step))
                    return step;
            }
            return null;
        }

        static string DefaultProfile(string workflowId)
        {
            if (workflowId == "hash-intelligence-vics" || workflowId == "cac-csam-provenance")
                return CompositionProfiles.HashIntelligence;
            if (workflowId == "cac-grooming-chat")
                return CompositionProfiles.FullCACLifecycle;
            return CompositionProfiles.AirGappedFieldTriage;
        }

        static string Escape(string value)
        {
            return (value ?? "").Replace("\\", "\\\\").Replace("\"", "\\\"");
        }

        static string ExtractJsonString(string json, string key)
        {
            var needle = "\"" + key + "\"";
            var idx = json.IndexOf(needle, StringComparison.Ordinal);
            if (idx < 0)
                return null;
            var colon = json.IndexOf(':', idx);
            var first = json.IndexOf('"', colon + 1);
            var second = json.IndexOf('"', first + 1);
            if (first < 0 || second < 0)
                return null;
            return json.Substring(first + 1, second - first - 1);
        }

        static List<string> ExtractJsonStringArray(string json, string key)
        {
            var result = new List<string>();
            var needle = "\"" + key + "\"";
            var idx = json.IndexOf(needle, StringComparison.Ordinal);
            if (idx < 0)
                return result;
            var bracket = json.IndexOf('[', idx);
            var end = json.IndexOf(']', bracket + 1);
            if (bracket < 0 || end < 0)
                return result;
            var body = json.Substring(bracket + 1, end - bracket - 1);
            foreach (var part in body.Split(','))
            {
                var trimmed = part.Trim().Trim('"');
                if (trimmed.Length > 0)
                    result.Add(trimmed);
            }
            return result;
        }
    }
}
