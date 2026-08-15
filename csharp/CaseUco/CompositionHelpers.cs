// Topology fluent helpers — generated from Composition Profiles (do not edit typed classes).
// Source: topology/profiles + generator helpers backend.

using System;
using System.Collections.Generic;
using CaseUco.Case;
using CaseUco.Uco.Core;
using CaseUco.Uco.Observable;
using CaseUco.Uco.Tool;
using CaseUco.Uco.Types;

namespace CaseUco
{
    /// <summary>Result of <see cref="CompositionHelpers.ModelCsamEvidence"/>.</summary>
    public sealed class CsamEvidence
    {
        public Tool Tool { get; set; }
        public RasterPicture Picture { get; set; }
        public InvestigativeAction Action { get; set; }
    }

    /// <summary>Result of <see cref="CompositionHelpers.ModelToolRun"/>.</summary>
    public sealed class ToolRun
    {
        public Tool Tool { get; set; }
        public InvestigativeAction Action { get; set; }
    }

    /// <summary>
    /// Fluent composition helpers (HashIntelligence / MinimalForensics / ToolMapping).
    /// Additive wrappers around generated classes.
    /// </summary>
    public static class CompositionHelpers
    {
        public static ObservableObject FileWithContentHashes(
            CaseGraph graph,
            string fileName,
            IEnumerable<KeyValuePair<string, string>> hashes,
            string filePath = null,
            long? sizeInBytes = null)
        {
            if (graph == null) throw new ArgumentNullException(nameof(graph));
            var fileFacet = new FileFacet
            {
                FileName = new List<string> { fileName },
                SizeInBytes = sizeInBytes,
            };
            if (filePath != null)
                fileFacet.FilePath = new List<string> { filePath };
            var content = new ContentDataFacet
            {
                Hash = ToHashes(hashes),
                SizeInBytes = sizeInBytes,
            };
            var obj = new ObservableObject
            {
                HasFacet = new List<Facet> { fileFacet, content },
            };
            graph.Add(obj);
            return obj;
        }

        public static RasterPicture RasterPictureWithHashes(
            CaseGraph graph,
            string fileName,
            IEnumerable<KeyValuePair<string, string>> hashes,
            string pictureType = null)
        {
            if (graph == null) throw new ArgumentNullException(nameof(graph));
            var picture = new RasterPicture
            {
                HasFacet = new List<Facet>
                {
                    new FileFacet { FileName = new List<string> { fileName } },
                    new ContentDataFacet { Hash = ToHashes(hashes) },
                    new RasterPictureFacet { PictureType = pictureType },
                },
            };
            graph.Add(picture);
            return picture;
        }

        public static CsamEvidence ModelCsamEvidence(
            CaseGraph graph,
            string fileName,
            IEnumerable<KeyValuePair<string, string>> hashes,
            string hashingToolName = "PhotoDNA",
            string hashingToolVersion = null)
        {
            if (graph == null) throw new ArgumentNullException(nameof(graph));
            var tool = new Tool
            {
                Name = hashingToolName,
                Version = hashingToolVersion,
                ToolType = "Content hashing",
            };
            graph.Add(tool);
            var picture = RasterPictureWithHashes(graph, fileName, hashes);
            var action = new InvestigativeAction
            {
                Name = hashingToolName + " hash of " + fileName,
                Instrument = new List<UcoObject> { tool },
                Object = new List<UcoObject> { picture },
                Result = new List<UcoObject> { picture },
            };
            graph.Add(action);
            return new CsamEvidence { Tool = tool, Picture = picture, Action = action };
        }

        public static ToolRun ModelToolRun(
            CaseGraph graph,
            string toolName,
            string actionName,
            string toolVersion = null)
        {
            if (graph == null) throw new ArgumentNullException(nameof(graph));
            var tool = new Tool { Name = toolName, Version = toolVersion };
            graph.Add(tool);
            var action = new InvestigativeAction
            {
                Name = actionName,
                Instrument = new List<UcoObject> { tool },
                Object = new List<UcoObject>(),
                Result = new List<UcoObject>(),
            };
            graph.Add(action);
            return new ToolRun { Tool = tool, Action = action };
        }

        internal static List<Hash> ToHashes(IEnumerable<KeyValuePair<string, string>> hashes)
        {
            var list = new List<Hash>();
            if (hashes == null)
                return list;
            foreach (var pair in hashes)
            {
                list.Add(new Hash
                {
                    HashMethod = pair.Key,
                    HashValue = HexToBytes(pair.Value),
                });
            }
            return list;
        }

        internal static byte[] HexToBytes(string lexical)
        {
            if (string.IsNullOrEmpty(lexical))
                return Array.Empty<byte>();
            var hex = lexical.Trim();
            if (hex.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
                hex = hex.Substring(2);
            if (hex.Length % 2 == 1)
                hex = "0" + hex;
            try
            {
                var bytes = new byte[hex.Length / 2];
                for (var i = 0; i < bytes.Length; i++)
                    bytes[i] = Convert.ToByte(hex.Substring(i * 2, 2), 16);
                return bytes;
            }
            catch (FormatException)
            {
                return System.Text.Encoding.UTF8.GetBytes(lexical);
            }
        }
    }
}
