using System;
using System.Collections.Generic;

namespace CaseUco
{
    /// <summary>Marking and authorization scope allowed for one partition root (#79).</summary>
    public sealed class PartitionBoundary
    {
        public IEnumerable<string> Markings { get; set; } = Array.Empty<string>();
        public IEnumerable<string> Authorizations { get; set; } = Array.Empty<string>();
    }

    /// <summary>Options for marking-safe dependency partitioning (#79).</summary>
    public sealed class PartitionOptions
    {
        public string SharedNodePolicy { get; set; } = "replicate-identical";
        public bool IncludeIncoming { get; set; } = true;
        public string BoundaryPolicy { get; set; } = "none";
        public string CrossBoundaryPolicy { get; set; } = "error-on-cross-boundary";
        public IDictionary<string, PartitionBoundary> RootBoundaries { get; set; }
            = new Dictionary<string, PartitionBoundary>(StringComparer.Ordinal);
        public IDictionary<string, object> ValidationBundle { get; set; }
            = new Dictionary<string, object>(StringComparer.Ordinal);
        public string ManifestDetail { get; set; } = "full";
    }

    /// <summary>A partition set plus its reconstruction and validation manifest.</summary>
    public sealed class PartitionResult
    {
        public PartitionResult(
            Dictionary<string, CaseGraph> partitions,
            Dictionary<string, object> manifest)
        {
            Partitions = partitions;
            Manifest = manifest;
        }

        public Dictionary<string, CaseGraph> Partitions { get; }
        public Dictionary<string, object> Manifest { get; }
    }

    /// <summary>A partition plan would widen marking or authorization access.</summary>
    public sealed class PartitionBoundaryException : InvalidOperationException
    {
        public PartitionBoundaryException(
            string rootId,
            string nodeId,
            IReadOnlyList<string> missingMarkings,
            IReadOnlyList<string> missingAuthorizations)
            : base(
                $"partition root '{rootId}' is not authorized for node '{nodeId}'; " +
                $"missing markings=[{string.Join(", ", missingMarkings)}], " +
                $"missing authorizations=[{string.Join(", ", missingAuthorizations)}]")
        {
            RootId = rootId;
            NodeId = nodeId;
            MissingMarkings = missingMarkings;
            MissingAuthorizations = missingAuthorizations;
        }

        public string RootId { get; }
        public string NodeId { get; }
        public IReadOnlyList<string> MissingMarkings { get; }
        public IReadOnlyList<string> MissingAuthorizations { get; }
    }

    /// <summary>Exact JSON-LD node-union verification evidence.</summary>
    public sealed class PartitionUnionVerification
    {
        public bool Equivalent { get; internal set; }
        public int SourceNodes { get; internal set; }
        public int UnionNodes { get; internal set; }
    }
}
