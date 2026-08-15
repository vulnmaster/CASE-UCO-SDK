// Composition Profile catalog — generated from topology/profiles/*.json.

using System;
using System.Collections.Generic;

namespace CaseUco
{
    /// <summary>Offline Composition Profile ids and keyword ranking.</summary>
    public static class CompositionProfiles
    {
        public const string MinimalForensics = "MinimalForensics";
        public const string AirGappedFieldTriage = "AirGappedFieldTriage";
        public const string HashIntelligence = "HashIntelligence";
        public const string ToolMapping = "ToolMapping";
        public const string LegalProcess = "LegalProcess";
        public const string FullCACLifecycle = "FullCACLifecycle";
        public const string CrossOntology = "CrossOntology";

        public static readonly string[] All =
        {
            MinimalForensics, AirGappedFieldTriage, HashIntelligence,
            ToolMapping, LegalProcess, FullCACLifecycle, CrossOntology,
        };

        public static bool RequiresCac(string profileId)
        {
            // Align with Python: "ext.cac" in required_modules only.
            return profileId == FullCACLifecycle || profileId == CrossOntology;
        }

        public static string Resolve(string profileId, string scenario)
        {
            if (!string.IsNullOrEmpty(profileId))
            {
                foreach (var id in All)
                {
                    if (string.Equals(id, profileId, StringComparison.OrdinalIgnoreCase))
                        return id;
                }
                throw new ArgumentException("Unknown composition profile: " + profileId, nameof(profileId));
            }
            var ranked = Recommend(scenario);
            return ranked.Count > 0 ? ranked[0] : MinimalForensics;
        }

        public static List<string> Recommend(string scenario)
        {
            var query = (scenario ?? "").ToLowerInvariant();
            var scored = new List<KeyValuePair<int, string>>();
            foreach (var id in All)
            {
                var hay = Keywords(id);
                var score = 0;
                if (query.IndexOf(id.ToLowerInvariant(), StringComparison.Ordinal) >= 0)
                    score += 8;
                foreach (var token in hay)
                {
                    if (query.IndexOf(token, StringComparison.Ordinal) >= 0)
                        score += 2;
                }
                if (score > 0)
                    scored.Add(new KeyValuePair<int, string>(score, id));
            }
            scored.Sort((a, b) => b.Key.CompareTo(a.Key));
            var result = new List<string>();
            foreach (var pair in scored)
                result.Add(pair.Value);
            return result;
        }

        static string[] Keywords(string id)
        {
            switch (id)
            {
                case HashIntelligence:
                    return new[] { "hash", "photodna", "vics", "csam", "sha256", "perceptual" };
                case FullCACLifecycle:
                    return new[] { "cac", "csam", "grooming", "trafficking", "cybertip", "ncmec", "child" };
                case AirGappedFieldTriage:
                    return new[] { "air", "offline", "field", "triage", "laptop" };
                case ToolMapping:
                    return new[] { "tool", "autopsy", "solve-it", "configured" };
                case LegalProcess:
                    return new[] { "charge", "indictment", "plea", "sentence", "pacer" };
                case CrossOntology:
                    return new[] { "gufo", "prov", "cross-ontology", "composition" };
                default:
                    return new[] { "file", "hash", "triage", "starter" };
            }
        }
    }
}
