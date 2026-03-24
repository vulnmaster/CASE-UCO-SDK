"""Auto-generated uco-observable classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from case_uco.uco.action import Action
from case_uco.uco.core import Facet
from case_uco.uco.core import Item
from case_uco.uco.core import Relationship
from case_uco.uco.core import UcoInherentCharacterizationThing
from case_uco.uco.core import UcoObject

if TYPE_CHECKING:
    from case_uco.uco.configuration import Configuration
    from case_uco.uco.core import UcoObject
    from case_uco.uco.identity import Identity
    from case_uco.uco.identity import Organization
    from case_uco.uco.location import Location
    from case_uco.uco.types import ControlledDictionary
    from case_uco.uco.types import Dictionary
    from case_uco.uco.types import Hash
    from case_uco.uco.types import Thread


class WhoisDNSSECTypeVocab:
    """Vocabulary: WhoisDNSSECTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab"

    SIGNED = "Signed"
    UNSIGNED = "Unsigned"


class WindowsVolumeAttributeVocab:
    """Vocabulary: WindowsVolumeAttributeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab"

    HIDDEN = "Hidden"
    NODEFAULTDRIVELETTER = "NoDefaultDriveLetter"
    READONLY = "ReadOnly"
    SHADOWCOPY = "ShadowCopy"


@dataclass
class Observable(UcoObject):
    """An observable is a characterizable item or action within the digital domain."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Observable"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ObservableObject(Item):
    """An observable object is a grouping of characteristics unique to a distinct article or unit within the digital domain."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject"
    NAMESPACE_PREFIX: str = "uco-observable"

    has_changed: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:hasChanged', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    state: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:state', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class API(ObservableObject):
    """An API (application programming interface) is a computing interface that defines interactions between multiple software or mixed hardware-software intermediaries. It defines the kinds of calls or requ"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/API"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ARPCache(ObservableObject):
    """An ARP cache is a collection of Address Resolution Protocol (ARP) entries (mostly dynamic) that are created when an IP address is resolved to a MAC address (so the computer can effectively communicate"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ARPCache"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ARPCacheEntry(ObservableObject):
    """An ARP cache entry is a single Address Resolution Protocol (ARP) response record that is created when an IP address is resolved to a MAC address (so the computer can effectively communicate with the I"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ARPCacheEntry"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Account(ObservableObject):
    """An account is an arrangement with an entity to enable and control the provision of some capability or service."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Account"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AccountAuthenticationFacet(Facet):
    """An account authentication facet is a grouping of characteristics unique to the mechanism of accessing an account."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AccountAuthenticationFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    password: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:password', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    password_last_changed: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:passwordLastChanged', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    password_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:passwordType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class AccountFacet(Facet):
    """An account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    account_identifier: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:accountIdentifier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    account_issuer: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:accountIssuer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    account_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:accountType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    expiration_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:expirationTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_active: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isActive', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    owner: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:owner', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})


@dataclass
class Device(ObservableObject):
    """A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.com/dictionary/device]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Device"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Adaptor(Device):
    """An adaptor is a device that physically converts the pin outputs but does not alter the underlying protocol (e.g. uSD to SD, CF to ATA, etc.)"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Adaptor"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Address(ObservableObject):
    """An address is an identifier assigned to enable routing and management of information."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Address"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AlternateDataStream(ObservableObject):
    """An alternate data stream is data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from access by default NTFS file viewing mechanisms."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStream"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AlternateDataStreamFacet(Facet):
    """An alternate data stream facet is a grouping of characteristics unique to data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from acce"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStreamFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    hashes: Optional[Hash] = field(default=None, metadata={'jsonld_key': 'uco-observable:hashes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:size', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class AndroidDevice(Device):
    """An Android device is a device running the Android operating system. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidDevice"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AndroidDeviceFacet(Facet):
    """An Android device facet is a grouping of characteristics unique to an Android device. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidDeviceFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    android_fingerprint: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:androidFingerprint', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    android_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:androidID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    android_version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:androidVersion', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_adb_root_enabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isADBRootEnabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_su_root_enabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isSURootEnabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})


@dataclass
class Computer(Device):
    """A computer is an electronic device for storing and processing data, typically in binary, according to instructions given to it in a variable program. [based on 'Computer.' Oxford English Dictionary, O"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Computer"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MobileDevice(Device):
    """A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobile_device]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileDevice"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MobilePhone(MobileDevice):
    """A mobile phone is a portable telephone that at least can make and receive calls over a radio frequency link while the user is moving within a telephone service area. This category encompasses all type"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MobilePhone"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SmartDevice(Device):
    """A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-based networks or via smartphone"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SmartDevice"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SmartPhone(Computer):
    """A smartphone is a portable device that combines mobile telephone and computing functions into one unit.  Examples include iPhone, Samsung Galaxy, Huawei, Blackberry. (Inferred by model and OperatingSy"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SmartPhone"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AndroidPhone(AndroidDevice):
    """An android phone is a smart phone that applies the Android mobile operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidPhone"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AntennaFacet(Facet):
    """An antenna alignment facet contains the metadata surrounding the cell tower's antenna position."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AntennaFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    antenna_height: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:antennaHeight', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    azimuth: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:azimuth', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    elevation: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:elevation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    horizontal_beam_width: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:horizontalBeamWidth', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    signal_strength: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:signalStrength', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    skew: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:skew', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})


@dataclass
class AppleDevice(Device):
    """An apple device is a smart device that applies either the MacOS or iOS operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AppleDevice"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Appliance(Device):
    """An appliance is a purpose-built computer with software or firmware that is designed to provide a specific computing capability or resource. [based on https://en.wikipedia.org/wiki/Computer_appliance]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Appliance"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Application(ObservableObject):
    """An application is a particular software program designed for end users."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Application"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DigitalAccount(Account):
    """A digital account is an arrangement with an entity to enable and control the provision of some capability or service within the digital domain."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ApplicationAccount(DigitalAccount):
    """An application account is an account within a particular software program designed for end users."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ApplicationAccountFacet(Facet):
    """An application account facet is a grouping of characteristics unique to an account within a particular software program designed for end users."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ApplicationFacet(Facet):
    """An application facet is a grouping of characteristics unique to a particular software program designed for end users."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application_identifier: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:applicationIdentifier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    installed_version_history: list[ApplicationVersion] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:installedVersionHistory', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ApplicationVersion', 'alternate_range_iris': []})
    number_of_launches: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:numberOfLaunches', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    operating_system: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:operatingSystem', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ApplicationVersion(UcoInherentCharacterizationThing):
    """An application version is a grouping of characteristics unique to a particular software program version."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationVersion"
    NAMESPACE_PREFIX: str = "uco-observable"

    install_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:installDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    uninstall_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:uninstallDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class FileSystemObject(ObservableObject):
    """A file system object is an informational object represented and managed within a file system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystemObject"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class File(FileSystemObject):
    """A file is a computer resource for recording data discretely on a computer storage device."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/File"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ArchiveFile(File):
    """An archive file is a file that is composed of one or more computer files along with metadata."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFile"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ArchiveFileFacet(Facet):
    """An archive file facet is a grouping of characteristics unique to a file that is composed of one or more computer files along with metadata."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    archive_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:archiveType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    comment: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:comment', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Audio(ObservableObject):
    """Audio is a digital representation of sound."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Audio"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AudioFacet(Facet):
    """An audio facet is a grouping of characteristics unique to a digital representation of sound."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AudioFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    audio_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:audioType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    bit_rate: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:bitRate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    duration: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:duration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    format: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:format', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class AutonomousSystem(ObservableObject):
    """An autonomous system is a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of a single administrative entity or domain that """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystem"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class AutonomousSystemFacet(Facet):
    """An autonomous system facet is a grouping of characteristics unique to a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystemFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    as_handle: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:asHandle', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    number: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:number', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    regional_internet_registry: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:regionalInternetRegistry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class BlackberryPhone(SmartPhone):
    """A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blackberry 10 re-introduces Blackberry OS, prior to that the OS was Android.)"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BlackberryPhone"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BlockDeviceNode(FileSystemObject):
    """A block device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing buffered randomly accesible input and output. Block device nodes are used to apply"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BlockDeviceNode"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DigitalAddress(Address):
    """A digital address is an identifier assigned to enable routing and management of digital communication."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MACAddress(DigitalAddress):
    """A MAC address is a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications at the data link layer of a network segment."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MACAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BluetoothAddress(MACAddress):
    """A Bluetooth address is a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards conformant communication to or from that device"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DigitalAddressFacet(Facet):
    """A digital address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of digital communication."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    address_value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:addressValue', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    display_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:displayName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MACAddressFacet(DigitalAddressFacet):
    """A MAC address facet is a grouping of characteristics unique to a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MACAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BluetoothAddressFacet(MACAddressFacet):
    """A Bluetooth address facet is a grouping of characteristics unique to a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards c"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BotConfiguration(ObservableObject):
    """A bot configuration is a set of contextual settings for a software application that runs automated tasks (scripts) over the Internet at a much higher rate than would be possible for a human alone."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BotConfiguration"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BrowserBookmark(ObservableObject):
    """A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on https://techterms.com/definition/bookmark]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmark"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BrowserBookmarkFacet(Facet):
    """A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on htt"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmarkFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    accessed_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:accessedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    bookmark_path: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:bookmarkPath', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    url_targeted: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:urlTargeted', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#anyURI', 'alternate_range_iris': []})
    visit_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:visitCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class BrowserCookie(ObservableObject):
    """A browser cookie is a piece of of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on https://en.wikipedia.org/wiki/HTTP_cookie]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookie"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class BrowserCookieFacet(Facet):
    """A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookieFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    accessed_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:accessedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    cookie_domain: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:cookieDomain', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    cookie_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cookieName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cookie_path: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cookiePath', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    expiration_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:expirationTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_secure: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isSecure', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class Calendar(ObservableObject):
    """A calendar is a collection of appointments, meetings, and events."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Calendar"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CalendarEntry(ObservableObject):
    """A calendar entry is an appointment, meeting or event within a collection of appointments, meetings and events."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntry"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CalendarEntryFacet(Facet):
    """A calendar entry facet is a grouping of characteristics unique to an appointment, meeting, or event within a collection of appointments, meetings, and events."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntryFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    attendant: list[Identity] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:attendant', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    duration: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:duration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    event_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    event_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_private: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isPrivate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    location: Optional[Location] = field(default=None, metadata={'jsonld_key': 'uco-observable:location', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    owner: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:owner', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    recurrence: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:recurrence', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    remind_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:remindTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    subject: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class CalendarFacet(Facet):
    """A calendar facet is a grouping of characteristics unique to a collection of appointments, meetings, and events."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    owner: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:owner', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})


@dataclass
class Call(ObservableObject):
    """A call is a connection as part of a realtime cyber communication between one or more parties."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Call"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CallFacet(Facet):
    """A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber communication between one or more parties."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CallFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    call_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:callType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    duration: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:duration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    from_: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:from', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    participant: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:participant', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    to: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:to', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class CapturedTelecommunicationsInformation(ObservableObject):
    """CapturedTelecommunicationsInformation"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformation"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CapturedTelecommunicationsInformationFacet(Facet):
    """A captured telecommunications information facet represents certain information within captured or intercepted telecommunications data."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformationFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    capture_cell_site: CellSite = field(default=None, metadata={'jsonld_key': 'uco-observable:captureCellSite', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/CellSite', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    intercepted_call_state: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:interceptedCallState', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class CellSite(ObservableObject):
    """CellSite"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CellSite"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CellSiteFacet(Facet):
    """A cell site facet contains the metadata surrounding the cell site."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CellSiteFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    cell_site_country_code: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cellSiteCountryCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cell_site_identifier: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cellSiteIdentifier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cell_site_location_area_code: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cellSiteLocationAreaCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cell_site_network_code: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cellSiteNetworkCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cell_site_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cellSiteType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class CharacterDeviceNode(FileSystemObject):
    """A character device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing only a serial stream of input or accepting a serial stream of output. Characte"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CharacterDeviceNode"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Code(ObservableObject):
    """Code is a direct representation (source, byte or binary) of a collection of computer instructions that form software which tell a computer how to work. [based on https://en.wikipedia.org/wiki/Software"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Code"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CompressedStreamFacet(Facet):
    """A compressed stream facet is a grouping of characteristics unique to the application of a size-reduction process to a body of data content."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CompressedStreamFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    compression_method: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:compressionMethod', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    compression_ratio: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:compressionRatio', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})


@dataclass
class ComputerSpecification(ObservableObject):
    """A computer specification is the hardware and software of a programmable electronic device that can store, retrieve, and process data. {based on merriam-webster.com/dictionary/computer]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecification"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ComputerSpecificationFacet(Facet):
    """A computer specificaiton facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data. [based on merriam-we"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecificationFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    available_ram: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:availableRam', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    bios_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:biosDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    bios_manufacturer: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:biosManufacturer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    bios_release_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:biosReleaseDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    bios_serial_number: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:biosSerialNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    bios_version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:biosVersion', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cpu: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cpu', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cpu_family: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cpuFamily', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    current_system_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:currentSystemDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    gpu: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:gpu', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    gpu_family: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:gpuFamily', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    hostname: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:hostname', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    local_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:localTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    network_interface: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:networkInterface', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    processor_architecture: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:processorArchitecture', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    system_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:systemTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    timezone_dst: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:timezoneDST', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    timezone_standard: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:timezoneStandard', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    total_ram: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:totalRam', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    uptime: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:uptime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Software(ObservableObject):
    """Software is a definitely scoped instance of a collection of data or computer instructions that tell the computer how to work. [based on https://en.wikipedia.org/wiki/Software]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Software"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ConfiguredSoftware(Software):
    """A ConfiguredSoftware is a Software that is known to be configured to run in a more specified manner than some unconfigured or less-configured Software."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ConfiguredSoftware"
    NAMESPACE_PREFIX: str = "uco-observable"

    is_configuration_of: Optional[Software] = field(default=None, metadata={'jsonld_key': 'uco-configuration:isConfigurationOf', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/Software', 'alternate_range_iris': []})
    uses_configuration: Optional[Configuration] = field(default=None, metadata={'jsonld_key': 'uco-configuration:usesConfiguration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/configuration/Configuration', 'alternate_range_iris': []})


@dataclass
class Contact(ObservableObject):
    """A contact is a set of identification and communication related details for a single entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Contact"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ContactAddress(UcoInherentCharacterizationThing):
    """A contact address is a grouping of characteristics unique to a geolocation address of a contact entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_address_scope: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactAddressScope', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    geolocation_address: Optional[Location] = field(default=None, metadata={'jsonld_key': 'uco-observable:geolocationAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})


@dataclass
class ContactAffiliation(UcoInherentCharacterizationThing):
    """A contact affiliation is a grouping of characteristics unique to details of an organizational affiliation for a single contact entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactAffiliation"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_email: list[ContactEmail] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactEmail', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail', 'alternate_range_iris': []})
    contact_messaging: list[ContactMessaging] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactMessaging', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging', 'alternate_range_iris': []})
    contact_organization: Optional[Organization] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactOrganization', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Organization', 'alternate_range_iris': []})
    contact_phone: list[ContactPhone] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactPhone', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone', 'alternate_range_iris': []})
    contact_profile: list[ContactProfile] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactProfile', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactProfile', 'alternate_range_iris': []})
    contact_url: list[ContactURL] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactURL', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactURL', 'alternate_range_iris': []})
    organization_department: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:organizationDepartment', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    organization_location: list[ContactAddress] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:organizationLocation', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress', 'alternate_range_iris': []})
    organization_position: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:organizationPosition', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ContactEmail(UcoInherentCharacterizationThing):
    """A contact email is a grouping of characteristics unique to details for contacting a contact entity by email."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_email_scope: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactEmailScope', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    email_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:emailAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContactFacet(Facet):
    """A contact facet is a grouping of characteristics unique to a set of identification and communication related details for a single entity."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    birthdate: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-identity:birthdate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    contact_address: list[ContactAddress] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactAddress', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress', 'alternate_range_iris': []})
    contact_affiliation: list[ContactAffiliation] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactAffiliation', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactAffiliation', 'alternate_range_iris': []})
    contact_email: list[ContactEmail] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactEmail', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail', 'alternate_range_iris': []})
    contact_group: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactGroup', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    contact_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    contact_messaging: list[ContactMessaging] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactMessaging', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging', 'alternate_range_iris': []})
    contact_note: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactNote', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    contact_phone: list[ContactPhone] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactPhone', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone', 'alternate_range_iris': []})
    contact_profile: list[ContactProfile] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactProfile', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactProfile', 'alternate_range_iris': []})
    contact_sip: list[ContactSIP] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactSIP', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactSIP', 'alternate_range_iris': []})
    contact_url: list[ContactURL] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactURL', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactURL', 'alternate_range_iris': []})
    display_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:displayName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    first_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:firstName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    last_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:lastName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    last_time_contacted: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:lastTimeContacted', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    middle_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:middleName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    name_phonetic: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:namePhonetic', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    name_prefix: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:namePrefix', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    name_suffix: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:nameSuffix', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    nickname: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:nickname', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    number_times_contacted: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:numberTimesContacted', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    source_application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:sourceApplication', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContactList(ObservableObject):
    """A contact list is a set of multiple individual contacts such as that found in a digital address book."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactList"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ContactListFacet(Facet):
    """A contact list facet is a grouping of characteristics unique to a set of multiple individual contacts such as that found in a digital address book."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactListFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contact', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    source_application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:sourceApplication', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContactMessaging(UcoInherentCharacterizationThing):
    """A contact messaging is a grouping of characteristics unique to details for contacting a contact entity by digital messaging."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_messaging_platform: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactMessagingPlatform', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    messaging_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:messagingAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContactPhone(UcoInherentCharacterizationThing):
    """A contact phone is a grouping of characteristics unique to details for contacting a contact entity by telephone."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_phone_number: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactPhoneNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    contact_phone_scope: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactPhoneScope', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ContactProfile(UcoInherentCharacterizationThing):
    """A contact profile is a grouping of characteristics unique to details for contacting a contact entity by online service."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactProfile"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_profile_platform: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactProfilePlatform', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    profile: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profile', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContactSIP(UcoInherentCharacterizationThing):
    """A contact SIP is a grouping of characteristics unique to details for contacting a contact entity by Session Initiation Protocol (SIP)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactSIP"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_sip_scope: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactSIPScope', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    sip_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:sipAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContactURL(UcoInherentCharacterizationThing):
    """A contact URL is a grouping of characteristics unique to details for contacting a contact entity by Uniform Resource Locator (URL)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactURL"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_url_scope: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contactURLScope', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    url: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:url', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class ContentData(ObservableObject):
    """Content data is a block of digital data."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContentData"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ContentDataFacet(Facet):
    """A content data facet is a grouping of characteristics unique to a block of digital data."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ContentDataFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    byte_order: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:byteOrder', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    data_payload: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:dataPayload', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    data_payload_reference_url: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:dataPayloadReferenceURL', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    entropy: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:entropy', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    hash: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:hash', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    is_encrypted: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isEncrypted', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    magic_number: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:magicNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    mime_class: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:mimeClass', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    mime_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:mimeType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    size_in_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:sizeInBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class CookieHistory(ObservableObject):
    """A cookie history is the stored web cookie history for a particular web browser."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CookieHistory"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Credential(ObservableObject):
    """A credential is a single specific login and password combination for authorization of access to a digital account or system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Credential"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class CredentialDump(ObservableObject):
    """A credential dump is a collection (typically forcibly extracted from a system) of specific login and password combinations for authorization of access to a digital account or system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/CredentialDump"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DNSCache(ObservableObject):
    """An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query results (created when an domain name is resolved to a IP address) for a particular computer."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DNSCache"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DNSRecord(ObservableObject):
    """A DNS record is a single Domain Name System (DNS) artifact specifying information of a particular type (routing, authority, responsibility, security, etc.) for a specific Internet domain name."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DNSRecord"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DataRangeFacet(Facet):
    """A data range facet is a grouping of characteristics unique to a particular contiguous scope within a block of digital data."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DataRangeFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    range_offset: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:rangeOffset', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    range_offset_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:rangeOffsetType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    range_size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:rangeSize', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class DefinedEffectFacet(Facet):
    """A defined effect facet is a grouping of characteristics unique to the effect of an observable action in relation to one or more observable objects."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DefinedEffectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DeviceFacet(Facet):
    """A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.c"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DeviceFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    cpeid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cpeid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    device_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:deviceType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    manufacturer: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:manufacturer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    model: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:model', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    serial_number: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:serialNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class DigitalAccountFacet(Facet):
    """A digital account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service within the digital domain."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    account_login: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:accountLogin', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    display_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:displayName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    first_login_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:firstLoginTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_disabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isDisabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    last_login_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:lastLoginTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class DigitalCamera(Device):
    """A digital camera is a camera that captures photographs in digital memory as opposed to capturing images on photographic film."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalCamera"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DigitalSignatureInfo(ObservableObject):
    """A digital signature info is a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfo"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DigitalSignatureInfoFacet(Facet):
    """A digital signature info facet is a grouping of characteristics unique to a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfoFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    certificate_issuer: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:certificateIssuer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    certificate_subject: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:certificateSubject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    signature_description: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:signatureDescription', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    signature_exists: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:signatureExists', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    signature_verified: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:signatureVerified', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})


@dataclass
class Directory(FileSystemObject):
    """A directory is a file system cataloging structure which contains references to other computer files, and possibly other directories. On many computers, directories are known as folders, or drawers, an"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Directory"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Disk(ObservableObject):
    """A disk is a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating disks."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Disk"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DiskFacet(Facet):
    """A disk facet is a grouping of characteristics unique to a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rot"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DiskFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    disk_size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:diskSize', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    disk_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:diskType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    free_space: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:freeSpace', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    partition: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:partition', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class DiskPartition(ObservableObject):
    """A disk partition is a particular managed region on a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DiskPartition"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DiskPartitionFacet(Facet):
    """A disk partition facet is a grouping of characteristics unique to a particular managed region on a storage mechanism."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DiskPartitionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    disk_partition_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:diskPartitionType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    mount_point: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:mountPoint', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    partition_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:partitionID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    partition_length: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:partitionLength', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    partition_offset: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:partitionOffset', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    space_left: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:spaceLeft', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    space_used: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:spaceUsed', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    total_space: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:totalSpace', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class DomainName(ObservableObject):
    """A domain name is an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.wikipedia.org/wiki/Domain_name]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DomainName"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class DomainNameFacet(Facet):
    """A domain name facet is a grouping of characteristics unique to an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/DomainNameFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    is_tld: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isTLD', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:value', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Drone(MobileDevice):
    """A drone, unmanned aerial vehicle (UAV), is an aircraft without a human pilot, crew, or passengers that typically involve a ground-based controller and a system for communications with the UAV."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Drone"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EXIFFacet(Facet):
    """An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners an"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EXIFFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    exif_data: list[ControlledDictionary] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:exifData', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary', 'alternate_range_iris': []})


@dataclass
class EmailAccount(DigitalAccount):
    """An email account is an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EmailAccountFacet(Facet):
    """An email account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    email_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:emailAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class EmailAddress(DigitalAddress):
    """An email address is an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are sent from and delivered to."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EmailAddressFacet(DigitalAddressFacet):
    """An email address facet is a grouping of characteristics unique to an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Message(ObservableObject):
    """A message is a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https://en.wikipedia.org/wiki/Message]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Message"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EmailMessage(Message):
    """An email message is a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and related RFCs."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailMessage"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EmailMessageFacet(Facet):
    """An email message facet is a grouping of characteristics unique to a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailMessageFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    bcc: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:bcc', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    body: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:body', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    body_multipart: list[MimePartType] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:bodyMultipart', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/MimePartType', 'alternate_range_iris': []})
    body_raw: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:bodyRaw', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    categories: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:categories', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    cc: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:cc', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    content_disposition: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:contentDisposition', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    content_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:contentType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    from_: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:from', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    header_raw: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:headerRaw', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    in_reply_to: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:inReplyTo', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_mime_encoded: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isMimeEncoded', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_multipart: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isMultipart', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_read: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isRead', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    labels: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:labels', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    message_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:messageID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    other_headers: Optional[Dictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:otherHeaders', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    priority: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:priority', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    received_lines: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:receivedLines', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    received_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:receivedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    references: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:references', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    sender: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:sender', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    sent_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:sentTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    subject: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    to: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:to', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    x_mailer: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:xMailer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    x_originating_ip: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:xOriginatingIP', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class EmbeddedDevice(Device):
    """An embedded device is a highly specialized microprocessor device meant for one or very few specific purposes and is usually embedded or included within another object or as part of a larger system. Ex"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EmbeddedDevice"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EncodedStreamFacet(Facet):
    """An encoded stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another form."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EncodedStreamFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    encoding_method: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:encodingMethod', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class EncryptedStreamFacet(Facet):
    """An encrypted stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another obfuscated form in such a way that reversing the conversion to ob"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EncryptedStreamFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    encryption_iv: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:encryptionIV', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    encryption_key: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:encryptionKey', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    encryption_method: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:encryptionMethod', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    encryption_mode: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:encryptionMode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class EnvironmentVariable(UcoInherentCharacterizationThing):
    """An environment variable is a grouping of characteristics unique to a dynamic-named value that can affect the way running processes will behave on a computer. [based on https://en.wikipedia.org/wiki/En"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EnvironmentVariable"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:value', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class EventLog(ObservableObject):
    """An event log is a collection of event records."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EventLog"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EventRecord(ObservableObject):
    """An event record is something that happens in a digital context (e.g., operating system events)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EventRecord"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class EventRecordFacet(Facet):
    """An event record facet is a grouping of characteristics unique to something that happens in a digital context (e.g., operating system events)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/EventRecordFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    account: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:account', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    cyber_action: Optional[ObservableAction] = field(default=None, metadata={'jsonld_key': 'uco-observable:cyberAction', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableAction', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    event_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    event_record_device: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventRecordDevice', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    event_record_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventRecordID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    event_record_raw: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventRecordRaw', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    event_record_service_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventRecordServiceName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    event_record_text: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventRecordText', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    event_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:eventType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class ExtInodeFacet(Facet):
    """An extInode facet is a grouping of characteristics unique to a file system object (file, directory, etc.) conformant to the extended file system (EXT or related derivations) specification."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ExtInodeFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    ext_deletion_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:extDeletionTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    ext_file_type: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extFileType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ext_flags: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extFlags', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ext_hard_link_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extHardLinkCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ext_inode_change_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:extInodeChangeTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    ext_inode_id: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extInodeID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ext_permissions: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extPermissions', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ext_sgid: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extSGID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ext_suid: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:extSUID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class ExtractedString(UcoInherentCharacterizationThing):
    """An extracted string is a grouping of characteristics unique to a series of characters pulled from an observable object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ExtractedString"
    NAMESPACE_PREFIX: str = "uco-observable"

    byte_string_value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:byteStringValue', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#base64Binary', 'alternate_range_iris': []})
    encoding: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:encoding', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    english_translation: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:englishTranslation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    language: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:language', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    length: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:length', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    string_value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:stringValue', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ExtractedStringsFacet(Facet):
    """An extracted strings facet is a grouping of characteristics unique to one or more sequences of characters pulled from an observable object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ExtractedStringsFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    strings: list[ExtractedString] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:strings', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ExtractedString', 'alternate_range_iris': []})


@dataclass
class FileFacet(Facet):
    """A file facet is a grouping of characteristics unique to the storage of a file (computer resource for recording data discretely in a computer storage device) on a file system (process that manages how """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/FileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    accessed_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:accessedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    allocation_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:allocationStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    extension: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:extension', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    file_name: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:fileName', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    file_path: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:filePath', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_directory: list[bool] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:isDirectory', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    metadata_change_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:metadataChangeTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    size_in_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:sizeInBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class FilePermissionsFacet(Facet):
    """A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a file system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/FilePermissionsFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    owner: Optional[UcoObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:owner', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})


@dataclass
class FileSystem(ObservableObject):
    """A file system is the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/definition/5510/file-system]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystem"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class FileSystemFacet(Facet):
    """A file system facet is a grouping of characteristics unique to the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/def"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystemFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    cluster_size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:clusterSize', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    file_system_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:fileSystemType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ForumPost(Message):
    """A forum post is message submitted by a user account to an online forum where the message content (and typically metadata including who posted it and when) is viewable by any party with viewing permiss"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ForumPost"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ForumPrivateMessage(Message):
    """A forum private message (aka PM or DM (direct message)) is a one-to-one message from one specific user account to another specific user account on an online form where transmission is managed by the o"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ForumPrivateMessage"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class FragmentFacet(Facet):
    """A fragment facet is a grouping of characteristics unique to an individual piece of the content of a file."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/FragmentFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    fragment_index: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:fragmentIndex', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    total_fragments: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:totalFragments', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class GUI(ObservableObject):
    """A GUI is a graphical user interface that allows users to interact with electronic devices through graphical icons and audio indicators such as primary notation, instead of text-based user interfaces, """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GUI"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class GamingConsole(Device):
    """A gaming console (video game console or game console) is an electronic system that connects to a display, typically a TV or computer monitor, for the primary purpose of playing video games."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GamingConsole"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class GenericObservableObject(ObservableObject):
    """A generic observable object is an article or unit within the digital domain."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GenericObservableObject"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class GeoLocationEntry(ObservableObject):
    """A geolocation entry is a single application-specific geolocation entry."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntry"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class GeoLocationEntryFacet(Facet):
    """A geolocation entry facet is a grouping of characteristics unique to a single application-specific geolocation entry."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntryFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    location: Optional[Location] = field(default=None, metadata={'jsonld_key': 'uco-observable:location', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class GeoLocationLog(ObservableObject):
    """A geolocation log is a record containing geolocation tracks and/or geolocation entries."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLog"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class GeoLocationLogFacet(Facet):
    """A geolocation log facet is a grouping of characteristics unique to a record containing geolocation tracks and/or geolocation entries."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLogFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class GeoLocationTrack(ObservableObject):
    """A geolocation track is a set of contiguous geolocation entries representing a path/track taken."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrack"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class GeoLocationTrackFacet(Facet):
    """A geolocation track facet is a grouping of characteristics unique to a set of contiguous geolocation entries representing a path/track taken."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrackFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    geo_location_entry: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:geoLocationEntry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class GlobalFlagType(UcoInherentCharacterizationThing):
    """A global flag type is a grouping of characteristics unique to the Windows systemwide global variable named NtGlobalFlag that enables various internal debugging, tracing, and validation support in the """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/GlobalFlagType"
    NAMESPACE_PREFIX: str = "uco-observable"

    abbreviation: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:abbreviation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    destination: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:destination', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    hexadecimal_value: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:hexadecimalValue', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    symbolic_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:symbolicName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class NetworkConnection(ObservableObject):
    """A network connection is a connection (completed or attempted) across a digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.htm"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnection"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class HTTPConnection(NetworkConnection):
    """An HTTP connection is network connection that is conformant to the Hypertext Transfer Protocol (HTTP) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnection"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class HTTPConnectionFacet(Facet):
    """An HTTP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Hypertext Transfer Protocol (HTTP) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnectionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    http_mesage_body_length: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:httpMesageBodyLength', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    http_message_body_data: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:httpMessageBodyData', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    http_request_header: Optional[Dictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:httpRequestHeader', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    request_method: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:requestMethod', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    request_value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:requestValue', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    request_version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:requestVersion', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Hostname(ObservableObject):
    """A hostname is a label that is assigned to a device connected to a computer network and that is used to identify the device in various forms of electronic communication, such as the World Wide Web. A h"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Hostname"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ICMPConnection(NetworkConnection):
    """An ICMP connection is a network connection that is conformant to the Internet Control Message Protocol (ICMP) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnection"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ICMPConnectionFacet(Facet):
    """An ICMP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Internet Control Message Protocol (ICMP) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnectionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    icmp_code: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:icmpCode', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    icmp_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:icmpType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})


@dataclass
class IComHandlerActionType(UcoInherentCharacterizationThing):
    """An IComHandler action type is a grouping of characteristics unique to a Windows Task-related action that fires a Windows COM handler (smart code in the client address space that can optimize calls bet"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IComHandlerActionType"
    NAMESPACE_PREFIX: str = "uco-observable"

    com_class_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:comClassID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    com_data: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:comData', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class IExecActionType(UcoInherentCharacterizationThing):
    """An IExec action type is a grouping of characteristics unique to an action that executes a command-line operation on a Windows operating system. [based on https://docs.microsoft.com/en-us/windows/win32"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IExecActionType"
    NAMESPACE_PREFIX: str = "uco-observable"

    exec_arguments: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:execArguments', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    exec_program_hashes: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:execProgramHashes', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    exec_program_path: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:execProgramPath', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    exec_working_directory: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:execWorkingDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class IPAddress(DigitalAddress):
    """An IP address is an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conformant communication to or from that device."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPAddressFacet(DigitalAddressFacet):
    """An IP address facet is a grouping of characteristics unique to an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conforman"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPNetmask(ObservableObject):
    """An IP netmask is a 32-bit 'mask' used to divide an IP address into subnets and specify the network's available hosts."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPNetmask"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPhone(AppleDevice):
    """An iPhone is a smart phone that applies the iOS mobile operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPhone"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPv4Address(IPAddress):
    """An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 standards conformant communication to or from tha"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv4Address"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPv4AddressFacet(IPAddressFacet):
    """An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 sta"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv4AddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPv6Address(IPAddress):
    """An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 standards conformant communication to or from tha"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv6Address"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IPv6AddressFacet(IPAddressFacet):
    """An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 sta"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv6AddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class IShowMessageActionType(UcoInherentCharacterizationThing):
    """An IShow message action type is a grouping of characteristics unique to an action that shows a message box when a task is activate. [based on https://docs.microsoft.com/en-us/windows/win32/api/tasksch"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/IShowMessageActionType"
    NAMESPACE_PREFIX: str = "uco-observable"

    show_message_body: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:showMessageBody', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    show_message_title: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:showMessageTitle', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Image(ObservableObject):
    """An image is a complete copy of a hard disk, memory, or other digital media."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Image"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ImageFacet(Facet):
    """An image facet is a grouping of characteristics unique to a complete copy of a hard disk, memory, or other digital media."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ImageFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    image_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:imageType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class InstantMessagingAddress(DigitalAddress):
    """InstantMessagingAddress"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class InstantMessagingAddressFacet(DigitalAddressFacet):
    """An instant messaging address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of instant messaging digital communication."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Junction(FileSystemObject):
    """A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory access to another directory which can be on the same volume or another volume. A junction is similar to"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Junction"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Laptop(Computer):
    """A laptop, laptop computer, or notebook computer is a small, portable personal computer with a screen and alphanumeric keyboard. These typically have a clam shell form factor with the screen mounted on"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Laptop"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Library(ObservableObject):
    """A library is a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definition/3828/software-library]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Library"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class LibraryFacet(Facet):
    """A library facet is a grouping of characteristics unique to a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definit"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/LibraryFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    library_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:libraryType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Memory(ObservableObject):
    """Memory is a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Memory"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MemoryFacet(Facet):
    """A memory facet is a grouping of characteristics unique to a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MemoryFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    block_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:blockType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_injected: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isInjected', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_mapped: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isMapped', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_protected: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isProtected', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_volatile: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isVolatile', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    region_end_address: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:regionEndAddress', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    region_size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:regionSize', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    region_start_address: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:regionStartAddress', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})


@dataclass
class MessageFacet(Facet):
    """A message facet is a grouping of characteristics unique to a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https:"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MessageFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    from_: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:from', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    message_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:messageID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    message_text: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:messageText', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    message_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:messageType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    sent_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:sentTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    session_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:sessionID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    to: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:to', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class MessageThread(ObservableObject):
    """A message thread is a running commentary of electronic messages pertaining to one topic or question."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MessageThread"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MessageThreadFacet(Facet):
    """A message thread facet is a grouping of characteristics unique to a running commentary of electronic messages pertaining to one topic or question."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MessageThreadFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    message_thread: Optional[Thread] = field(default=None, metadata={'jsonld_key': 'uco-observable:messageThread', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Thread', 'alternate_range_iris': []})
    participant: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:participant', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    visibility: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:visibility', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})


@dataclass
class MftRecordFacet(Facet):
    """An MFT record facet is a grouping of characteristics unique to the details of a single file as managed in an NTFS (new technology filesystem) master file table (which is a collection of information ab"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MftRecordFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    mft_file_id: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFileID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    mft_file_name_accessed_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFileNameAccessedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    mft_file_name_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFileNameCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    mft_file_name_length: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFileNameLength', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    mft_file_name_modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFileNameModifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    mft_file_name_record_change_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFileNameRecordChangeTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    mft_flags: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftFlags', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    mft_parent_id: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftParentID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    mft_record_change_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:mftRecordChangeTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    ntfs_hard_link_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:ntfsHardLinkCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ntfs_owner_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:ntfsOwnerID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    ntfs_owner_sid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:ntfsOwnerSID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MimePartType(UcoInherentCharacterizationThing):
    """A mime part type is a grouping of characteristics unique to a component of a multi-part email body."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MimePartType"
    NAMESPACE_PREFIX: str = "uco-observable"

    body: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:body', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    body_raw: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:bodyRaw', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    content_disposition: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:contentDisposition', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    content_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:contentType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MobileAccount(DigitalAccount):
    """A mobile account is an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based on https://www.lexico.com/definition/mobile_d"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MobileAccountFacet(Facet):
    """A mobile account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    imsi: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:IMSI', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    msisdn: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:MSISDN', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    msisdn_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:MSISDNType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class MobileDeviceFacet(Facet):
    """A mobile device facet is a grouping of characteristics unique to a portable computing device. [based on https://www.lexico.com/definition/mobile_device]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileDeviceFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    esn: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:ESN', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    imei: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:IMEI', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    bluetooth_device_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:bluetoothDeviceName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    clock_setting: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:clockSetting', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    keypad_unlock_code: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:keypadUnlockCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    mock_locations_allowed: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:mockLocationsAllowed', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    network: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:network', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    phone_activation_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:phoneActivationTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    storage_capacity_in_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:storageCapacityInBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class Mutex(ObservableObject):
    """A mutex is a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual exclusion concurrency control policy, and with a v"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Mutex"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class MutexFacet(Facet):
    """A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual excl"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/MutexFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    is_named: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isNamed', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    mutex_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:mutexName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class NTFSFile(File):
    """An NTFS file is a New Technology File System (NTFS) file."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFile"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NTFSFileFacet(Facet):
    """An NTFS file facet is a grouping of characteristics unique to a file on an NTFS (new technology filesystem) file system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    alternate_data_streams: list[AlternateDataStream] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:alternateDataStreams', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStream', 'alternate_range_iris': []})
    entry_id: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:entryID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    sid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:sid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class NTFSFilePermissionsFacet(Facet):
    """An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on an NTFS (new technology filesystem) file system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFilePermissionsFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NamedPipe(FileSystemObject):
    """A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is persisted as a filesystem object (that can be deleted like any other file), can be written to or read from """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NamedPipe"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NetworkAppliance(Appliance):
    """A network appliance is a purpose-built computer with software or firmware that is designed to provide a specific network management function."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkAppliance"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NetworkConnectionFacet(Facet):
    """A network connection facet is a grouping of characteristics unique to a connection (complete or attempted) accross a digital network (a group of two or more computer systems linked together). [based o"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnectionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    destination_port: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:destinationPort', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    dst: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:dst', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:endTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_active: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isActive', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    protocols: Optional[ControlledDictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:protocols', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary', 'alternate_range_iris': []})
    source_port: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:sourcePort', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    src: list[UcoObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:src', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/core/UcoObject', 'alternate_range_iris': []})
    start_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:startTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class NetworkFlow(ObservableObject):
    """A network flow is a sequence of data transiting one or more digital network (a group or two or more computer systems linked together) connections. [based on https://www.webopedia.com/TERM/N/network.ht"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlow"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NetworkFlowFacet(Facet):
    """A network flow facet is a grouping of characteristics unique to a sequence of data transiting one or more digital network (a group of two or more computer systems linked together) connections. [based """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlowFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    dst_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:dstBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    dst_packets: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:dstPackets', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    dst_payload: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:dstPayload', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    ipfix: Optional[Dictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:ipfix', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    src_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:srcBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    src_packets: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:srcPackets', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    src_payload: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:srcPayload', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class NetworkInterface(ObservableObject):
    """A network interface is a software or hardware interface between two pieces of equipment or protocol layers in a computer network."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterface"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NetworkInterfaceFacet(Facet):
    """A network interface facet is a grouping of characteristics unique to a software or hardware interface between two pieces of equipment or protocol layers in a computer network."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterfaceFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    adapter_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:adapterName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    dhcp_lease_expires: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:dhcpLeaseExpires', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    dhcp_lease_obtained: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:dhcpLeaseObtained', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    dhcp_server: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:dhcpServer', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    ip: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:ip', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    ip_gateway: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:ipGateway', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    mac_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:macAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class NetworkProtocol(ObservableObject):
    """A network protocol is an established set of structured rules that determine how data is transmitted between different devices in the same network. Essentially, it allows connected devices to communica"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkProtocol"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NetworkRoute(ObservableObject):
    """A network route is a specific path (of specific network nodes, connections and protocols) for traffic in a network or between or across multiple networks."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkRoute"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NetworkSubnet(ObservableObject):
    """A network subnet is a logical subdivision of an IP network. [based on https://en.wikipedia.org/wiki/Subnetwork]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSubnet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Note(ObservableObject):
    """A note is a brief textual record."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Note"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class NoteFacet(Facet):
    """A note facet is a grouping of characteristics unique to a brief textual record."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/NoteFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    text: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:text', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ObservableAction(Action):
    """An observable action is a grouping of characteristics unique to something that may be done or performed within the digital domain."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableAction"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ObservablePattern(Observable):
    """An observable pattern is a grouping of characteristics unique to a logical pattern composed of observable object and observable action properties."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservablePattern"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ObservableRelationship(Relationship):
    """An observable relationship is a grouping of characteristics unique to an assertion of an association between two observable objects."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableRelationship"
    NAMESPACE_PREFIX: str = "uco-observable"

    source: list[Observable] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:source', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/Observable', 'alternate_range_iris': []})
    target: list[Observable] = field(default_factory=list, metadata={'jsonld_key': 'uco-core:target', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/Observable', 'alternate_range_iris': []})


@dataclass
class Observation(Action):
    """An observation is a temporal perception of an observable."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Observation"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: str = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class OnlineService(ObservableObject):
    """An online service is a particular provision mechanism of information access, distribution or manipulation over the Internet."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/OnlineService"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class OnlineServiceFacet(Facet):
    """An online service facet is a grouping of characteristics unique to a particular provision mechanism of information access, distribution or manipulation over the Internet."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/OnlineServiceFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    inet_location: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:inetLocation', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    location: list[Location] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:location', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})


@dataclass
class OperatingSystem(ObservableObject):
    """An operating system is the software that manages computer hardware, software resources, and provides common services for computer programs. [based on https://en.wikipedia.org/wiki/Operating_system]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystem"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class OperatingSystemFacet(Facet):
    """An operating system facet is a grouping of characteristics unique to the software that manages computer hardware, software resources, and provides common services for computer programs. [based on http"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystemFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    advertising_id: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:advertisingID', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    bitness: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:bitness', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    environment_variables: Optional[Dictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:environmentVariables', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    install_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:installDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_limit_ad_tracking_enabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isLimitAdTrackingEnabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    manufacturer: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:manufacturer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class PDFFile(File):
    """A PDF file is a Portable Document Format (PDF) file."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PDFFile"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class PDFFileFacet(Facet):
    """A PDF file facet is a grouping of characteristics unique to a PDF (Portable Document Format) file."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PDFFileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    document_information_dictionary: Optional[ControlledDictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:documentInformationDictionary', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/ControlledDictionary', 'alternate_range_iris': []})
    is_optimized: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isOptimized', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    pdf_creation_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:pdfCreationDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    pdf_id0: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:pdfId0', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    pdf_id1: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:pdfId1', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    pdf_mod_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:pdfModDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class PathRelationFacet(Facet):
    """A path relation facet is a grouping of characteristics unique to the location of one object within another containing object."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PathRelationFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    path: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:path', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class PaymentCard(ObservableObject):
    """A payment card is a physical token that is part of a payment system issued by financial institutions, such as a bank, to a customer that enables its owner (the cardholder) to access the funds in the c"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PaymentCard"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class PhoneAccount(DigitalAccount):
    """A phone account is an arrangement with an entity to enable and control the provision of a telephony capability or service."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class PhoneAccountFacet(Facet):
    """A phone account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of a telephony capability or service."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    phone_number: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:phoneNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Pipe(ObservableObject):
    """A pipe is a mechanism for one-way inter-process communication using message passing where data written by one process is buffered by the operating system until it is read by the next process, and this"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Pipe"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Post(Message):
    """A post is message submitted to an online discussion/publishing site (forum, blog, etc.)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Post"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Process(ObservableObject):
    """A process is an instance of a computer program executed on an operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Process"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ProcessFacet(Facet):
    """A process facet is a grouping of characteristics unique to an instance of a computer program executed on an operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ProcessFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    arguments: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:arguments', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    binary: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:binary', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    creator_user: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:creatorUser', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    current_working_directory: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:currentWorkingDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    environment_variables: Optional[Dictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:environmentVariables', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    exit_status: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:exitStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    exit_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:exitTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    is_hidden: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isHidden', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    parent: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:parent', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    pid: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:pid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:status', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ProcessThread(ObservableObject):
    """A process thread is the smallest sequence of programmed instructions that can be managed independently by a scheduler on a computer, which is typically a part of the operating system. It is a componen"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ProcessThread"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Profile(ObservableObject):
    """A profile is an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or application. [based on https://en.wikipedia.o"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Profile"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ProfileFacet(Facet):
    """A profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ProfileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    contact_address: Optional[ContactAddress] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress', 'alternate_range_iris': []})
    contact_email: Optional[ContactEmail] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactEmail', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail', 'alternate_range_iris': []})
    contact_messaging: Optional[ContactMessaging] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactMessaging', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging', 'alternate_range_iris': []})
    contact_phone: Optional[ContactPhone] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactPhone', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone', 'alternate_range_iris': []})
    contact_url: Optional[ContactURL] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactURL', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ContactURL', 'alternate_range_iris': []})
    display_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:displayName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    profile_account: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileAccount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    profile_created: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileCreated', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    profile_identity: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileIdentity', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    profile_language: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:profileLanguage', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    profile_service: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileService', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    profile_website: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileWebsite', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class PropertiesEnumeratedEffectFacet(Facet):
    """A properties enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic of the observable object is enumerated. An example"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PropertiesEnumeratedEffectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    properties: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:properties', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class PropertyReadEffectFacet(DefinedEffectFacet):
    """A properties read effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic is read from an observable object. An example of this wo"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/PropertyReadEffectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    property_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:propertyName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:value', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ProtocolConverter(Device):
    """A protocol converter is a device that converts from one protocol to another (e.g. SD to USB, SATA to USB, etc."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ProtocolConverter"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class RasterPicture(File):
    """A raster picture is a raster (or bitmap) image."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/RasterPicture"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class RasterPictureFacet(Facet):
    """A raster picture facet is a grouping of characteristics unique to a raster (or bitmap) image."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/RasterPictureFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    bits_per_pixel: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:bitsPerPixel', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    camera: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:camera', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    image_compression_method: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:imageCompressionMethod', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    picture_height: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:pictureHeight', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    picture_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:pictureType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    picture_width: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:pictureWidth', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class RecoveredObject(ObservableObject):
    """An observable object that was the result of a recovery operation."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObject"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class RecoveredObjectFacet(Facet):
    """Recoverability status of name, metadata, and content."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObjectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    content_recovered_status: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:contentRecoveredStatus', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    metadata_recovered_status: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:metadataRecoveredStatus', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    name_recovered_status: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:nameRecoveredStatus', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ReparsePoint(FileSystemObject):
    """A reparse point is a type of NTFS (New Technology File System) object which is an optional attribute of files and directories meant to define some sort of preprocessing before accessing the said file """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ReparsePoint"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SIMCard(Device):
    """A SIM card is a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its related key, which are used to identify and authenti"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SIMCard"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SIMCardFacet(Facet):
    """A SIM card facet is a grouping of characteristics unique to a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its relate"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SIMCardFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    iccid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:ICCID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    imsi: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:IMSI', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    pin: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:PIN', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    puk: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:PUK', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    sim_form: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:SIMForm', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    sim_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:SIMType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    carrier: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:carrier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    storage_capacity_in_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:storageCapacityInBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class SIPAddress(DigitalAddress):
    """A SIP address is an identifier for Session Initiation Protocol (SIP) communication."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SIPAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SIPAddressFacet(DigitalAddressFacet):
    """A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP) standards conformant identifier assigned to a user to enable routing and management of SIP standards """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SIPAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SMSMessage(Message):
    """An SMS message is a message conformant to the short message service (SMS) communication protocol standards."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SMSMessage"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SMSMessageFacet(Facet):
    """A SMS message facet is a grouping of characteristics unique to a message conformant to the short message service (SMS) communication protocol standards."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SMSMessageFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    is_read: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isRead', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})


@dataclass
class SQLiteBlob(ObservableObject):
    """An SQLite blob is a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlob"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SQLiteBlobFacet(Facet):
    """An SQLite blob facet is a grouping of characteristics unique to a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlobFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    column_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:columnName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    row_condition: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:rowCondition', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    row_index: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:rowIndex', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#positiveInteger', 'alternate_range_iris': []})
    table_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:tableName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SecurityAppliance(Appliance):
    """A security appliance is a purpose-built computer with software or firmware that is designed to provide a specific security function to protect computer networks."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SecurityAppliance"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Semaphore(ObservableObject):
    """A semaphore is a variable or abstract data type used to control access to a common resource by multiple processes and avoid critical section problems in a concurrent system such as a multitasking oper"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Semaphore"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SendControlCodeEffectFacet(DefinedEffectFacet):
    """A send control code effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a control code, or other control-oriented communication signal, is sent"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SendControlCodeEffectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    control_code: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:controlCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Server(Computer):
    """A server is a server rack-mount based computer, minicomputer, supercomputer, etc."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Server"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class ShopListing(ObservableObject):
    """A shop listing is a listing of offered products on an online marketplace/shop."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ShopListing"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Snapshot(FileSystemObject):
    """A snapshot is a file system object representing a snapshot of the contents of a part of a file system at a point in time."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Snapshot"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Socket(FileSystemObject):
    """A socket is a special file used for inter-process communication, which enables communication between two processes. In addition to sending data, processes can send file descriptors across a Unix domai"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Socket"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SocketAddress(Address):
    """A socket address (combining and IP address and a port number) is a composite identifier for a network socket endpoint supporting internet protocol communications."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SocketAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SoftwareFacet(Facet):
    """A software facet is a grouping of characteristics unique to a software program (a definitively scoped instance of a collection of data or computer instructions that tell the computer how to work). [ba"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SoftwareFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    cpeid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:cpeid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    language: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:language', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    manufacturer: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:manufacturer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    swid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:swid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class StateChangeEffectFacet(DefinedEffectFacet):
    """A state change effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a state of the observable object is changed."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/StateChangeEffectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    new_object: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:newObject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    old_object: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:oldObject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class StorageMedium(Device):
    """A storage medium is any digital storage device that applies electromagnetic or optical surfaces, or depends solely on electronic circuits as solid state storage, for storing digital data. Examples inc"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/StorageMedium"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class StorageMediumFacet(Facet):
    """A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a piece of equipment or a mechanism designed to serve a special purpose or perform a special function."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/StorageMediumFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    total_storage_capacity_in_bytes: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:totalStorageCapacityInBytes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class SymbolicLink(FileSystemObject):
    """A symbolic link is a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname resolution. [based on https://en.wikipedia.org/wi"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLink"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class SymbolicLinkFacet(Facet):
    """A symbolic link facet is a grouping of characteristics unique to a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname res"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLinkFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    target_file: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:targetFile', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class TCPConnection(NetworkConnection):
    """A TCP connection is a network connection that is conformant to the Transfer """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TCPConnection"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class TCPConnectionFacet(Facet):
    """A TCP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Transmission Control Protocl (TCP) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TCPConnectionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    destination_flags: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:destinationFlags', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    source_flags: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sourceFlags', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})


@dataclass
class TableField(ObservableObject):
    """A database table field and its associated value contained within a relational database."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TableField"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class TableFieldFacet(Facet):
    """A database record facet contains properties associated with a specific table record value from a database."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TableFieldFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    record_field_is_null: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:recordFieldIsNull', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    record_field_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:recordFieldName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    record_field_value: Optional[Any] = field(default=None, metadata={'jsonld_key': 'uco-observable:recordFieldValue', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#base64Binary', 'alternate_range_iris': ['http://www.w3.org/2001/XMLSchema#decimal', 'http://www.w3.org/2001/XMLSchema#integer', 'http://www.w3.org/2001/XMLSchema#string']})
    record_row_id: Optional[Any] = field(default=None, metadata={'jsonld_key': 'uco-observable:recordRowID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': ['http://www.w3.org/2001/XMLSchema#string']})
    table_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:tableName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    table_schema: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:tableSchema', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Tablet(Computer):
    """A tablet is a mobile computer that is primarily operated by touching the screen. (Devices categorized by their manufacturer as a Tablet)"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Tablet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class TaskActionType(UcoInherentCharacterizationThing):
    """A task action type is a grouping of characteristics for a scheduled action to be completed."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TaskActionType"
    NAMESPACE_PREFIX: str = "uco-observable"

    action_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:actionID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    action_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:actionType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    i_com_handler_action: Optional[IComHandlerActionType] = field(default=None, metadata={'jsonld_key': 'uco-observable:iComHandlerAction', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/IComHandlerActionType', 'alternate_range_iris': []})
    i_email_action: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:iEmailAction', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    i_exec_action: Optional[IExecActionType] = field(default=None, metadata={'jsonld_key': 'uco-observable:iExecAction', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/IExecActionType', 'alternate_range_iris': []})
    i_show_message_action: Optional[IShowMessageActionType] = field(default=None, metadata={'jsonld_key': 'uco-observable:iShowMessageAction', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/IShowMessageActionType', 'alternate_range_iris': []})


@dataclass
class TriggerType(UcoInherentCharacterizationThing):
    """A trigger type is a grouping of characterizes unique to a set of criteria that, when met, starts the execution of a task within a Windows operating system. [based on https://docs.microsoft.com/en-us/w"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TriggerType"
    NAMESPACE_PREFIX: str = "uco-observable"

    is_enabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isEnabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    trigger_begin_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:triggerBeginTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    trigger_delay: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:triggerDelay', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    trigger_end_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:triggerEndTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    trigger_frequency: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:triggerFrequency', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    trigger_max_run_time: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:triggerMaxRunTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    trigger_session_change_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:triggerSessionChangeType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    trigger_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:triggerType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Tweet(Message):
    """A tweet is message submitted by a Twitter user account to the Twitter microblogging platform."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Tweet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class TwitterProfileFacet(Facet):
    """A twitter profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single Twitter user account. [based on https://e"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/TwitterProfileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    favorites_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:favoritesCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    followers_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:followersCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    friends_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:friendsCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    listed_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:listedCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    profile_background_hash: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:profileBackgroundHash', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    profile_background_location: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileBackgroundLocation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    profile_banner_hash: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:profileBannerHash', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    profile_banner_location: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileBannerLocation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    profile_image_hash: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:profileImageHash', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    profile_image_location: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileImageLocation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    profile_is_protected: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileIsProtected', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    profile_is_verified: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:profileIsVerified', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    statuses_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:statusesCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    twitter_handle: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:twitterHandle', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    twitter_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:twitterId', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    user_location_string: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:userLocationString', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class UNIXAccount(DigitalAccount):
    """A UNIX account is an account on a UNIX operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class UNIXAccountFacet(Facet):
    """A UNIX account facet is a grouping of characteristics unique to an account on a UNIX operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    gid: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:gid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    shell: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:shell', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class UNIXFile(File):
    """A UNIX file is a file pertaining to the UNIX operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXFile"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class UNIXFilePermissionsFacet(Facet):
    """A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a UNIX file system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXFilePermissionsFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class UNIXProcess(Process):
    """A UNIX process is an instance of a computer program executed on a UNIX operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcess"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class UNIXProcessFacet(Facet):
    """A UNIX process facet is a grouping of characteristics unique to an instance of a computer program executed on a UNIX operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcessFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    open_file_descriptor: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:openFileDescriptor', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    ruid: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:ruid', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})


@dataclass
class UNIXVolumeFacet(Facet):
    """A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single UNIX file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXVolumeFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    mount_point: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:mountPoint', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    options: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:options', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class URL(ObservableObject):
    """A URL is a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URL"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class URLFacet(Facet):
    """A URL facet is a grouping of characteristics unique to a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URLFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    fragment: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:fragment', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    full_value: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:fullValue', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    host: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:host', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    password: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:password', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    path: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:path', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    port: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:port', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    query: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:query', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    scheme: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:scheme', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    user_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:userName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class URLHistory(ObservableObject):
    """A URL history characterizes the stored URL history for a particular web browser"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistory"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class URLHistoryEntry(UcoInherentCharacterizationThing):
    """A URL history entry is a grouping of characteristics unique to the properties of a single URL history entry for a particular browser."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryEntry"
    NAMESPACE_PREFIX: str = "uco-observable"

    browser_user_profile: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:browserUserProfile', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    expiration_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:expirationTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    first_visit: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:firstVisit', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    hostname: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:hostname', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    keyword_search_term: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:keywordSearchTerm', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    last_visit: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:lastVisit', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    manually_entered_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:manuallyEnteredCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    page_title: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:pageTitle', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    referrer_url: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:referrerUrl', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    url: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:url', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    visit_count: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:visitCount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class URLHistoryFacet(Facet):
    """A URL history facet is a grouping of characteristics unique to the stored URL history for a particular web browser"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    browser_information: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:browserInformation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    url_history_entry: list[URLHistoryEntry] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:urlHistoryEntry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryEntry', 'alternate_range_iris': []})


@dataclass
class URLVisit(ObservableObject):
    """A URL visit characterizes the properties of a visit of a URL within a particular browser."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URLVisit"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class URLVisitFacet(Facet):
    """A URL visit facet is a grouping of characteristics unique to the properties of a visit of a URL within a particular browser."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/URLVisitFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    browser_information: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:browserInformation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    from_url_visit: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:fromURLVisit', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    url: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:url', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    url_transition_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:urlTransitionType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    visit_duration: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:visitDuration', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#duration', 'alternate_range_iris': []})
    visit_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:visitTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class UserAccount(DigitalAccount):
    """A user account is an account controlling a user's access to a network, system or platform."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UserAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class UserAccountFacet(Facet):
    """A user account facet is a grouping of characteristics unique to an account controlling a user's access to a network, system, or platform."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UserAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    can_escalate_privs: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:canEscalatePrivs', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    home_directory: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:homeDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    is_privileged: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isPrivileged', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    is_service_account: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isServiceAccount', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})


@dataclass
class UserSession(ObservableObject):
    """A user session is a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user. [based on https://en.wikipedia.org/wiki/Sessi"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UserSession"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class UserSessionFacet(Facet):
    """A user session facet is a grouping of characteristics unique to a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/UserSessionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    effective_group: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:effectiveGroup', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    effective_group_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:effectiveGroupID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    effective_user: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:effectiveUser', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    login_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:loginTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    logout_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:logoutTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class ValuesEnumeratedEffectFacet(DefinedEffectFacet):
    """A values enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a value of the observable object is enumerated. An example of this woul"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/ValuesEnumeratedEffectFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    values: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:values', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Volume(ObservableObject):
    """A volume is a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Volume"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class VolumeFacet(Facet):
    """A volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/VolumeFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    sector_size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:sectorSize', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    volume_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:volumeID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WearableDevice(SmartDevice):
    """A wearable device is an electronic device that is designed to be worn on a person's body."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WearableDevice"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WebPage(ObservableObject):
    """A web page is a specific collection of information provided by a website and displayed to a user in a web browser. A website typically consists of many web pages linked together in a coherent fashion."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WebPage"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WhoIs(ObservableObject):
    """WhoIs is a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoIs"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WhoIsFacet(Facet):
    """A whois facet is a grouping of characteristics unique to a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoIsFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    creation_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:creationDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    dnssec: Optional[WhoisDNSSECTypeVocab] = field(default=None, metadata={'jsonld_key': 'uco-observable:dnssec', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab', 'alternate_range_iris': []})
    domain_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:domainID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    domain_name: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:domainName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    expiration_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:expirationDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    ip_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:ipAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    lookup_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:lookupDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    name_server: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:nameServer', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    regional_internet_registry: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:regionalInternetRegistry', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    registrant_contact_info: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:registrantContactInfo', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    registrant_i_ds: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:registrantIDs', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    registrar_info: Optional[WhoisRegistrarInfoType] = field(default=None, metadata={'jsonld_key': 'uco-observable:registrarInfo', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/WhoisRegistrarInfoType', 'alternate_range_iris': []})
    remarks: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:remarks', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    server_name: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:serverName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    sponsoring_registrar: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:sponsoringRegistrar', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    status: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:status', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    updated_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:updatedDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class WhoisContactFacet(ContactFacet):
    """A Whois contact type is a grouping of characteristics unique to contact-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wiki"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoisContactFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    whois_contact_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:whoisContactType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WhoisRegistrarInfoType(UcoInherentCharacterizationThing):
    """A Whois registrar info type is a grouping of characteristics unique to registrar-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https:"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoisRegistrarInfoType"
    NAMESPACE_PREFIX: str = "uco-observable"

    contact_phone_number: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:contactPhoneNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    email_address: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:emailAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    geolocation_address: Optional[Location] = field(default=None, metadata={'jsonld_key': 'uco-observable:geolocationAddress', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/location/Location', 'alternate_range_iris': []})
    referral_url: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:referralURL', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    registrar_guid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:registrarGUID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    registrar_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:registrarID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    registrar_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:registrarName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    whois_server: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:whoisServer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class WifiAddress(MACAddress):
    """A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a device network interface to enable routing and management of IEEE 802.11 standards-conformant communicatio"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WifiAddress"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WifiAddressFacet(MACAddressFacet):
    """A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) standards conformant identifier assigned to a device network interface to enable routing and management of"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WifiAddressFacet"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class Wiki(ObservableObject):
    """A wiki is an online hypertext publication collaboratively edited and managed by its own audience directly using a web browser. A typical wiki contains multiple pages/articles for the subjects or scope"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/Wiki"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WikiArticle(ObservableObject):
    """A wiki article is one or more pages in a wiki focused on characterizing a particular topic."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WikiArticle"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsAccount(DigitalAccount):
    """A Windows account is a user account on a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsAccountFacet(Facet):
    """A Windows account facet is a grouping of characteristics unique to a user account on a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    groups: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:groups', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WindowsActiveDirectoryAccount(DigitalAccount):
    """A Windows Active Directory account is an account managed by directory-based identity-related services of a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccount"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsActiveDirectoryAccountFacet(Facet):
    """A Windows Active Directory account facet is a grouping of characteristics unique to an account managed by directory-based identity-related services of a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccountFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    active_directory_groups: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:activeDirectoryGroups', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    object_guid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:objectGUID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WindowsComputerSpecification(ObservableObject):
    """A Windows computer specification is the hardware ans software of a programmable electronic device that can store, retrieve, and process data running a Microsoft Windows operating system. [based on mer"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecification"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsComputerSpecificationFacet(Facet):
    """A Windows computer specification facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data running a Mic"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecificationFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    domain: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:domain', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    global_flag_list: list[GlobalFlagType] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:globalFlagList', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/GlobalFlagType', 'alternate_range_iris': []})
    last_shutdown_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:lastShutdownDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    ms_product_id: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:msProductID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    ms_product_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:msProductName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    net_bios_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:netBIOSName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    os_install_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:osInstallDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    os_last_upgrade_date: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:osLastUpgradeDate', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    registered_organization: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:registeredOrganization', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    registered_owner: Optional[Identity] = field(default=None, metadata={'jsonld_key': 'uco-observable:registeredOwner', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/identity/Identity', 'alternate_range_iris': []})
    windows_directory: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:windowsDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    windows_system_directory: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:windowsSystemDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    windows_temp_directory: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:windowsTempDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class WindowsCriticalSection(ObservableObject):
    """A Windows critical section is a Windows object that provides synchronization similar to that provided by a mutex object, except that a critical section can be used only by the threads of a single proc"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsCriticalSection"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsEvent(ObservableObject):
    """A Windows event is a notification record of an occurance of interest (system, security, application, etc.) on a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsEvent"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsFilemapping(ObservableObject):
    """A Windows file mapping is the association of a file's contents with a portion of the virtual address space of a process within a Windows operating system. The system creates a file mapping object (als"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsFilemapping"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsHandle(ObservableObject):
    """A Windows handle is an abstract reference to a resource within the Windows operating system, such as a window, memory, an open file or a pipe. It is the mechanism by which applications interact with s"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsHandle"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsHook(ObservableObject):
    """A Windows hook is a mechanism by which an application can intercept events, such as messages, mouse actions, and keystrokes within the Windows operating system. A function that intercepts a particular"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsHook"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsMailslot(ObservableObject):
    """A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard file functions. The data in a mailslot message can be in any form, but cannot be larger than 424 bytes """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsMailslot"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsNetworkShare(ObservableObject):
    """A Windows network share is a Windows computer resource made available from one host to other hosts on a computer network. It is a device or piece of information on a computer that can be remotely acce"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsNetworkShare"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsPEBinaryFile(File):
    """A Windows PE binary file is a Windows portable executable (PE) file."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFile"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsPEBinaryFileFacet(Facet):
    """A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable executable (PE) file."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFileFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    characteristics: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:characteristics', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    file_header_hashes: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:fileHeaderHashes', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    imp_hash: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:impHash', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    machine: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:machine', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    number_of_sections: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:numberOfSections', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    number_of_symbols: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:numberOfSymbols', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    optional_header: Optional[WindowsPEOptionalHeader] = field(default=None, metadata={'jsonld_key': 'uco-observable:optionalHeader', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEOptionalHeader', 'alternate_range_iris': []})
    pe_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:peType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    pointer_to_symbol_table: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:pointerToSymbolTable', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    sections: list[WindowsPESection] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sections', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/WindowsPESection', 'alternate_range_iris': []})
    size_of_optional_header: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:sizeOfOptionalHeader', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    time_date_stamp: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:timeDateStamp', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class WindowsPEFileHeader(UcoInherentCharacterizationThing):
    """A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the overall nature and structu"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEFileHeader"
    NAMESPACE_PREFIX: str = "uco-observable"

    time_date_stamp: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:timeDateStamp', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})


@dataclass
class WindowsPEOptionalHeader(UcoInherentCharacterizationThing):
    """A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the executable co"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEOptionalHeader"
    NAMESPACE_PREFIX: str = "uco-observable"

    address_of_entry_point: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:addressOfEntryPoint', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    base_of_code: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:baseOfCode', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    checksum: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:checksum', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    dll_characteristics: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:dllCharacteristics', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    file_alignment: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:fileAlignment', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    image_base: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:imageBase', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    loader_flags: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:loaderFlags', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    magic: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:magic', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    major_image_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:majorImageVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    major_linker_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:majorLinkerVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#byte', 'alternate_range_iris': []})
    major_os_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:majorOSVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    major_subsystem_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:majorSubsystemVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    minor_image_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:minorImageVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    minor_linker_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:minorLinkerVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#byte', 'alternate_range_iris': []})
    minor_os_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:minorOSVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    minor_subsystem_version: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:minorSubsystemVersion', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    number_of_rva_and_sizes: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:numberOfRVAAndSizes', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    section_alignment: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sectionAlignment', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_code: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfCode', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_headers: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfHeaders', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_heap_commit: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfHeapCommit', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_heap_reserve: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfHeapReserve', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_image: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfImage', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_initialized_data: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfInitializedData', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_stack_commit: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfStackCommit', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_stack_reserve: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfStackReserve', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    size_of_uninitialized_data: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:sizeOfUninitializedData', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    subsystem: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:subsystem', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedShort', 'alternate_range_iris': []})
    win32_version_value: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:win32VersionValue', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})


@dataclass
class WindowsPESection(UcoInherentCharacterizationThing):
    """A Windows PE section is a grouping of characteristics unique to a specific default or custom-defined region of a Windows PE (Portable Executable) file, consisting of an individual portion of the actua"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPESection"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    entropy: Optional[float] = field(default=None, metadata={'jsonld_key': 'uco-observable:entropy', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#decimal', 'alternate_range_iris': []})
    hashes: list[Hash] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:hashes', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    size: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:size', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})


@dataclass
class WindowsPrefetch(ObservableObject):
    """The Windows prefetch contains entries in a Windows prefetch file (used to speed up application startup starting with Windows XP)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetch"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsPrefetchFacet(Facet):
    """A Windows prefetch facet is a grouping of characteristics unique to entries in the Windows prefetch file (used to speed up application startup starting with Windows XP)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetchFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    accessed_directory: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:accessedDirectory', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    accessed_file: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:accessedFile', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    application_file_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:applicationFileName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    first_run: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:firstRun', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    last_run: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:lastRun', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    prefetch_hash: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:prefetchHash', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    times_executed: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:timesExecuted', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    volume: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:volume', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class WindowsProcess(Process):
    """A Windows process is a program running on a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcess"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsProcessFacet(Facet):
    """A Windows process facet is a grouping of characteristics unique to a program running on a Windows operating system."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcessFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    aslr_enabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:aslrEnabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    dep_enabled: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:depEnabled', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    owner_sid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:ownerSID', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    priority: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:priority', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    startup_info: Optional[Dictionary] = field(default=None, metadata={'jsonld_key': 'uco-observable:startupInfo', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Dictionary', 'alternate_range_iris': []})
    window_title: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:windowTitle', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WindowsRegistryHive(ObservableObject):
    """The Windows registry hive is a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating s"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHive"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsRegistryHiveFacet(Facet):
    """A Windows registry hive facet is a grouping of characteristics unique to a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level se"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHiveFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    hive_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:hiveType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WindowsRegistryKey(ObservableObject):
    """A Windows registry key is a particular key within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKey"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsRegistryKeyFacet(Facet):
    """A Windows registry key facet is a grouping of characteristics unique to a particular key within a Windows registry (A hierarchical database that stores low-level settings for the Microsoft Windows ope"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKeyFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    creator: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:creator', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    key: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:key', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    modified_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:modifiedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    number_of_subkeys: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:numberOfSubkeys', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    registry_values: list[WindowsRegistryValue] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:registryValues', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryValue', 'alternate_range_iris': []})


@dataclass
class WindowsRegistryValue(UcoInherentCharacterizationThing):
    """A Windows registry value is a grouping of characteristics unique to a particular value within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows opera"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryValue"
    NAMESPACE_PREFIX: str = "uco-observable"

    name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-core:name', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    data: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:data', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    data_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:dataType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WindowsService(ObservableObject):
    """A Windows service is a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UNIX daemon runs on UNIX). [based on https://en."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsService"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsServiceFacet(Facet):
    """A Windows service facet is a grouping of characteristics unique to a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UN"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    descriptions: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:descriptions', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    display_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:displayName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    group_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:groupName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    service_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:serviceName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    service_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:serviceStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    service_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:serviceType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    start_command_line: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:startCommandLine', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    start_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:startType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WindowsSystemRestore(ObservableObject):
    """A Windows system restore is a capture of a Windows computer's state (including system files, installed applications, Windows Registry, and system settings) at a particular point in time such that the """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsSystemRestore"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsTask(ObservableObject):
    """A Windows task is a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler. [based on http://msdn.microsoft.com/en-us/library/windows/desktop/aa381311(v=vs.85"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTask"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsTaskFacet(Facet):
    """A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler). [based on http://ms"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTaskFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    account: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:account', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    account_logon_type: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:accountLogonType', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    account_run_level: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:accountRunLevel', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    action_list: list[TaskActionType] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:actionList', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/TaskActionType', 'alternate_range_iris': []})
    application: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:application', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    exit_code: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:exitCode', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    flags: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:flags', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    image_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:imageName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    max_run_time: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:maxRunTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    most_recent_run_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:mostRecentRunTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    next_run_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:nextRunTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    parameters: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:parameters', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    priority: list[Any] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:priority', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': ['http://www.w3.org/2001/XMLSchema#string']})
    status: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:status', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    task_comment: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:taskComment', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    task_creator: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:taskCreator', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    trigger_list: list[TriggerType] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:triggerList', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/TriggerType', 'alternate_range_iris': []})
    work_item_data: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:workItemData', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})
    working_directory: Optional[ObservableObject] = field(default=None, metadata={'jsonld_key': 'uco-observable:workingDirectory', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class WindowsThread(ProcessThread):
    """A Windows thread is a single thread of execution within a Windows process."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThread"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WindowsThreadFacet(Facet):
    """A Windows thread facet is a grouping os characteristics unique to a single thread of execution within a Windows process."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThreadFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    context: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:context', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    creation_flags: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:creationFlags', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#unsignedInt', 'alternate_range_iris': []})
    creation_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:creationTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    observable_created_time: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:observableCreatedTime', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    parameter_address: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:parameterAddress', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    priority: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:priority', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    running_status: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:runningStatus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    security_attributes: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:securityAttributes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    stack_size: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:stackSize', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})
    start_address: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:startAddress', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#hexBinary', 'alternate_range_iris': []})
    thread_id: list[int] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:threadID', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})


@dataclass
class WindowsVolumeFacet(Facet):
    """A Windows volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single Windows file system. [based on https://en.wikipedia.org/wiki/Volume_(computing"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsVolumeFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    drive_letter: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:driveLetter', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    drive_type: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:driveType', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    windows_volume_attributes: list[WindowsVolumeAttributeVocab] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:windowsVolumeAttributes', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab', 'alternate_range_iris': []})


@dataclass
class WindowsWaitableTime(ObservableObject):
    """A Windows waitable timer is a synchronization object within the Windows operating system whose state is set to signaled when a specified due time arrives. There are two types of waitable timers that c"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsWaitableTime"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WirelessNetworkConnection(NetworkConnection):
    """A wireless network connection is a connection (completed or attempted) across an IEEE 802.11 standards-confromant digital network (a group of two or more computer systems linked together). [based on h"""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnection"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class WirelessNetworkConnectionFacet(Facet):
    """A wireless network connection facet is a grouping of characteristics unique to a connection (completed or attempted) across an IEEE 802.11 standards-conformant digital network (a group of two or more """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnectionFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    base_station: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:baseStation', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    password: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:password', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    ssid: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:ssid', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    wireless_network_security_mode: list[str] = field(default_factory=list, metadata={'jsonld_key': 'uco-observable:wirelessNetworkSecurityMode', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WriteBlocker(Device):
    """A write blocker is a device that allows read-only access to storage mediums in order to preserve the integrity of the data being analyzed. Examples include Tableau, Cellibrite, Talon, etc."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/WriteBlocker"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class X509Certificate(ObservableObject):
    """A X.509 certificate is a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/X509Certificate"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class X509CertificateFacet(Facet):
    """A X.509 certificate facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard. """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/X509CertificateFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    is_self_signed: Optional[bool] = field(default=None, metadata={'jsonld_key': 'uco-observable:isSelfSigned', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#boolean', 'alternate_range_iris': []})
    issuer: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:issuer', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    issuer_hash: Optional[Hash] = field(default=None, metadata={'jsonld_key': 'uco-observable:issuerHash', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    serial_number: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:serialNumber', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    signature: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:signature', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    signature_algorithm: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:signatureAlgorithm', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    subject: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subject', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    subject_hash: Optional[Hash] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectHash', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    subject_public_key_algorithm: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectPublicKeyAlgorithm', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    subject_public_key_exponent: Optional[int] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectPublicKeyExponent', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#integer', 'alternate_range_iris': []})
    subject_public_key_modulus: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectPublicKeyModulus', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    thumbprint_hash: Optional[Hash] = field(default=None, metadata={'jsonld_key': 'uco-observable:thumbprintHash', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/types/Hash', 'alternate_range_iris': []})
    validity_not_after: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:validityNotAfter', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    validity_not_before: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:validityNotBefore', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    version: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:version', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    x509v3extensions: Optional[X509V3ExtensionsFacet] = field(default=None, metadata={'jsonld_key': 'uco-observable:x509v3extensions', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/X509V3ExtensionsFacet', 'alternate_range_iris': []})


@dataclass
class X509V3Certificate(ObservableObject):
    """An X.509 v3 certificate is a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard. """

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/X509V3Certificate"
    NAMESPACE_PREFIX: str = "uco-observable"



@dataclass
class X509V3ExtensionsFacet(Facet):
    """An X.509 v3 certificate extensions facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/observable/X509V3ExtensionsFacet"
    NAMESPACE_PREFIX: str = "uco-observable"

    authority_key_identifier: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:authorityKeyIdentifier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    basic_constraints: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:basicConstraints', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    certificate_policies: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:certificatePolicies', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    crl_distribution_points: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:crlDistributionPoints', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    extended_key_usage: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:extendedKeyUsage', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    inhibit_any_policy: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:inhibitAnyPolicy', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    issuer_alternative_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:issuerAlternativeName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    key_usage: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:keyUsage', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    name_constraints: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:nameConstraints', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    policy_constraints: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:policyConstraints', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    policy_mappings: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:policyMappings', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    private_key_usage_period_not_after: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:privateKeyUsagePeriodNotAfter', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    private_key_usage_period_not_before: Optional[datetime] = field(default=None, metadata={'jsonld_key': 'uco-observable:privateKeyUsagePeriodNotBefore', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#dateTime', 'alternate_range_iris': []})
    subject_alternative_name: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectAlternativeName', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    subject_directory_attributes: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectDirectoryAttributes', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    subject_key_identifier: Optional[str] = field(default=None, metadata={'jsonld_key': 'uco-observable:subjectKeyIdentifier', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})

