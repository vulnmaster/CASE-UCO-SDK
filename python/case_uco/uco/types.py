"""Auto-generated uco-types classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from case_uco.uco.core import UcoInherentCharacterizationThing
from case_uco.uco.core import UcoThing


@dataclass
class Dictionary(UcoInherentCharacterizationThing):
    """A dictionary is list of (term/key, value) pairs with each term/key having an expectation to exist no more than once.  types:Dictionary alone does not validate this expectation, but validation is avail"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/Dictionary"
    NAMESPACE_PREFIX: str = "uco-types"

    entry: list[DictionaryEntry] = field(default_factory=list, metadata={'jsonld_key': 'uco-types:entry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/DictionaryEntry', 'alternate_range_iris': []})


@dataclass
class ControlledDictionary(Dictionary):
    """A controlled dictionary is a list of (term/key, value) pairs where each term/key exists no more than once and is constrained to an explicitly defined set of values."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary"
    NAMESPACE_PREFIX: str = "uco-types"

    entry: list[ControlledDictionaryEntry] = field(default_factory=list, metadata={'jsonld_key': 'uco-types:entry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionaryEntry', 'alternate_range_iris': []})


@dataclass
class DictionaryEntry(UcoInherentCharacterizationThing):
    """A dictionary entry is a single (term/key, value) pair."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/DictionaryEntry"
    NAMESPACE_PREFIX: str = "uco-types"

    key: str = field(default=None, metadata={'jsonld_key': 'uco-types:key', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    value: str = field(default=None, metadata={'jsonld_key': 'uco-types:value', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ControlledDictionaryEntry(DictionaryEntry):
    """A controlled dictionary entry is a single (term/key, value) pair where the term/key is constrained to an explicitly defined set of values."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionaryEntry"
    NAMESPACE_PREFIX: str = "uco-types"



@dataclass
class Hash(UcoInherentCharacterizationThing):
    """A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm that maps data of arbitrary size to a bit string (the 'hash') and is a one-way function, that is, a fu"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/Hash"
    NAMESPACE_PREFIX: str = "uco-types"

    hash_method: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-types:hashMethod', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    hash_value: str = field(default=None, metadata={'jsonld_key': 'uco-types:hashValue', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})


@dataclass
class ImproperDictionary(Dictionary):
    """ImproperDictionary"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/ImproperDictionary"
    NAMESPACE_PREFIX: str = "uco-types"

    repeats_key: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-types:repeatsKey', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ProperDictionary(Dictionary):
    """A proper dictionary is list of (term/key, value) pairs with each term/key existing no more than once."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/ProperDictionary"
    NAMESPACE_PREFIX: str = "uco-types"



@dataclass
class Thread(UcoThing):
    """A semi-ordered array of items, that can be present in multiple copies.  Implemetation of a UCO Thread is similar to a Collections Ontology List, except a Thread may fork and merge - that is, one of it"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/Thread"
    NAMESPACE_PREFIX: str = "uco-types"



@dataclass
class ThreadItem(UcoThing):
    """A ThreadItem is a member of a thread."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/types/ThreadItem"
    NAMESPACE_PREFIX: str = "uco-types"


