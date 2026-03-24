// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-types

using System.Collections.Generic;

namespace CaseUco.Uco.Types
{
    /// <summary>A controlled dictionary is a list of (term/key, value) pairs where each term/key exists no more than once and is constrained to an explicitly defined set of values.</summary>
    public class ControlledDictionary : CaseUco.Uco.Types.Dictionary
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary";
        public new const string NamespacePrefix = "uco-types";
        [global::CaseUco.JsonLdProperty("uco-types:entry")]
        public new List<CaseUco.Uco.Types.ControlledDictionaryEntry> Entry { get; set; }
    }

    /// <summary>A controlled dictionary entry is a single (term/key, value) pair where the term/key is constrained to an explicitly defined set of values.</summary>
    public class ControlledDictionaryEntry : CaseUco.Uco.Types.DictionaryEntry
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionaryEntry";
        public new const string NamespacePrefix = "uco-types";
    }

    /// <summary>A dictionary is list of (term/key, value) pairs with each term/key having an expectation to exist no more than once.  types:Dictionary alone does not validate this expectation, but validation is avail</summary>
    public class Dictionary : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/Dictionary";
        public new const string NamespacePrefix = "uco-types";
        [global::CaseUco.JsonLdProperty("uco-types:entry")]
        public List<CaseUco.Uco.Types.DictionaryEntry> Entry { get; set; }
    }

    /// <summary>A dictionary entry is a single (term/key, value) pair.</summary>
    public class DictionaryEntry : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/DictionaryEntry";
        public new const string NamespacePrefix = "uco-types";
        [global::CaseUco.JsonLdProperty("uco-types:key")]
        public string Key { get; set; }
        [global::CaseUco.JsonLdProperty("uco-types:value")]
        public string Value { get; set; }
    }

    /// <summary>A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm that maps data of arbitrary size to a bit string (the 'hash') and is a one-way function, that is, a fu</summary>
    public class Hash : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/Hash";
        public new const string NamespacePrefix = "uco-types";
        [global::CaseUco.JsonLdProperty("uco-types:hashMethod")]
        public List<string> HashMethod { get; set; }
        [global::CaseUco.JsonLdProperty("uco-types:hashValue")]
        public byte[] HashValue { get; set; }
    }

    /// <summary>ImproperDictionary</summary>
    public class ImproperDictionary : CaseUco.Uco.Types.Dictionary
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/ImproperDictionary";
        public new const string NamespacePrefix = "uco-types";
        [global::CaseUco.JsonLdProperty("uco-types:repeatsKey")]
        public List<string> RepeatsKey { get; set; }
    }

    /// <summary>A proper dictionary is list of (term/key, value) pairs with each term/key existing no more than once.</summary>
    public class ProperDictionary : CaseUco.Uco.Types.Dictionary
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/ProperDictionary";
        public new const string NamespacePrefix = "uco-types";
    }

    /// <summary>A semi-ordered array of items, that can be present in multiple copies.  Implemetation of a UCO Thread is similar to a Collections Ontology List, except a Thread may fork and merge - that is, one of it</summary>
    public class Thread : CaseUco.Uco.Core.UcoThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/Thread";
        public new const string NamespacePrefix = "uco-types";
    }

    /// <summary>A ThreadItem is a member of a thread.</summary>
    public class ThreadItem : CaseUco.Uco.Core.UcoThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/types/ThreadItem";
        public new const string NamespacePrefix = "uco-types";
    }

}