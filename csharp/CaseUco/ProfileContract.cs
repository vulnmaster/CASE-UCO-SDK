// Logical ProfileContract surface (v2). Check lists are synthesized, offline.

using System;
using System.Collections.Generic;

namespace CaseUco
{
    public sealed class ProfileContract
    {
        public string ProfileId { get; }
        public string ProfileVersion { get; }
        public string ContractSchemaVersion { get; }
        public IReadOnlyList<string> CheckIds { get; }

        public ProfileContract(string profileId, string profileVersion, string schemaVersion, IReadOnlyList<string> checkIds)
        {
            ProfileId = profileId;
            ProfileVersion = profileVersion;
            ContractSchemaVersion = schemaVersion;
            CheckIds = checkIds;
        }

        public static ProfileContract Load(string profileId)
        {
            var id = CompositionProfiles.Resolve(profileId, "");
            var checks = new List<string> { "PROF-FACET-001", "PROF-HASH-001", "PROF-TOOL-001", "PROF-SHACL-001" };
            if (id == CompositionProfiles.HashIntelligence)
            {
                checks.Add("PROF-HI-001");
                checks.Add("PROF-HI-002");
            }
            if (id == CompositionProfiles.FullCACLifecycle)
            {
                checks.Add("PROF-CAC-001");
                checks.Add("PROF-CAC-002");
                checks.Add("PROF-CAC-003");
                checks.Add("PROF-CAC-004");
            }
            if (id == CompositionProfiles.LegalProcess)
                checks.Add("PROF-LEGAL-001");
            if (id == CompositionProfiles.AirGappedFieldTriage)
                checks.Add("PROF-AIR-001");
            return new ProfileContract(id, "1.0.0", "1.0.0", checks);
        }
    }
}
