"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit_observable module (generated; do not edit)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import case_uco.uco.core as _uco_core
import case_uco.uco.observable as _uco_observable
from case_uco_solveit._context import NAMESPACES

__all__ = ["ADBPullData", "AFCExtractionData", "AcquiredData", "AcquisitionErrorRecord", "AcquisitionRecordFile", "AiChatAppFiles", "AndroidDeviceGeneratedBackup", "AppleUnifiedLogArchive", "ApplicationFiles", "ArtifactSet", "AudioFile", "Bitstream", "BitstreamRandomAccessed", "BrowserAppFiles", "BrowserCacheData", "CalendarAppFiles", "ChatAppFiles", "ClockOffsetCapture", "ClockOffsetMeasurement", "ClusterRun", "ContentQueryData", "DateTimeRange", "DateTimeStamp", "DecryptionKey", "DeviceGeneratedBackup", "DeviceInterface", "DeviceScreenshotCapture", "DeviceSet", "EmailAppFiles", "FileSet", "FileSystemExtraction", "FilteredFileSet", "ForensicImageContainer", "GamingAppFiles", "HashSet", "HashSetEntry", "HashVerificationResult", "HealthAppFiles", "ImplicitTimingInformation", "KeywordIndex", "KeywordIndexingConfiguration", "KeywordSearchResult", "KeywordSearchResultSet", "LiveDataCapture", "LiveOSDeviceInterface", "LogicalImageContainer", "MapsAppFiles", "NavigationAppFiles", "NetworkPacketCapture", "PaymentAppFiles", "PhotosAppFiles", "PhysicalImageContainer", "PrioritizedDeviceEntry", "PrioritizedDeviceSet", "RawImage", "RawImageInfoFile", "ReadWriteDeviceInterface", "RedactedArtifactSet", "RedactedFileSet", "RemindersAppFiles", "SQLiteDatabase", "SQLiteField", "SQLiteFieldDefinition", "SQLiteJournal", "SQLiteJournalPageImage", "SQLitePage", "SQLiteRecord", "SQLiteSchema", "SQLiteTable", "SQLiteWAL", "SQLiteWALFrame", "ServiceBasedExtractionData", "SmartHomeAppFiles", "SocialMediaAppFiles", "SortedTimeline", "SortedTimelineEntry", "Timeline", "TimelineEntry", "TimestampOffset", "UnlockPattern", "VideoFile", "VideoFrame", "VirtualizedComputer", "VirtualizedDevice", "Wordlist", "WriteProtectedDeviceInterface", "httpResponseHeader", "iOSDeviceGeneratedBackup"]


@dataclass
class AcquiredData(_uco_observable.ObservableObject):
    """Data that has been forensically collected from a source device or system. This is the parent class for all types of forensic data acquisition outputs."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AcquiredData"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ServiceBasedExtractionData(AcquiredData):
    """Data obtained by interacting with services provided by a device rather than direct storage access."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ServiceBasedExtractionData"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ADBPullData(ServiceBasedExtractionData):
    """Data obtained via Android Debug Bridge (ADB) pull operations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ADBPullData"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class AFCExtractionData(ServiceBasedExtractionData):
    """Data obtained via Apple File Conduit (AFC) service from iOS devices."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AFCExtractionData"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class AcquisitionErrorRecord(_uco_observable.ObservableObject):
    """A record of an error encountered during data acquisition such as a bad sector, read timeout, I/O error, CRC error, or media surface damage."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AcquisitionErrorRecord"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class AcquisitionRecordFile(_uco_observable.File):
    """A file containing records generated during a data acquisition process, such as error logs or acquisition status reports."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AcquisitionRecordFile"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class FileSet(_uco_core.ContextualCompilation):
    """A contextual compilation of files grouped together for some purpose, such as filtering, extraction, or association with an application."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/FileSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    has_file: list[File] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:hasFile', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/File', 'alternate_range_iris': []})


@dataclass
class ApplicationFiles(FileSet):
    """A contextual compilation of files associated with a specific application version. Groups the files belonging to a particular application (e.g. WhatsApp v13.2 database files) for forensic examination."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ApplicationFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    source_application: Optional[Application] = field(default=None, metadata={'jsonld_key': 'solveit-observable:sourceApplication', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/Application', 'alternate_range_iris': []})


@dataclass
class AiChatAppFiles(ApplicationFiles):
    """Files associated with an AI chatbot or assistant application, including conversation histories, prompt logs, cached model responses, and user preference data (e.g. ChatGPT, Claude, Gemini)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AiChatAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class DeviceGeneratedBackup(ServiceBasedExtractionData):
    """Data produced by a device's built-in backup mechanism. Content is determined by the device's backup logic and structured in the backup's native format."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DeviceGeneratedBackup"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class AndroidDeviceGeneratedBackup(DeviceGeneratedBackup):
    """Data produced by Android's backup mechanism (e.g., adb backup). Potentially contains application data, shared storage, and system settings in the Android backup format (.ab file)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AndroidDeviceGeneratedBackup"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class AppleUnifiedLogArchive(ServiceBasedExtractionData):
    """Data obtained by collecting Apple Unified Logs from a macOS or iOS device."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AppleUnifiedLogArchive"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ArtifactSet(_uco_core.ContextualCompilation):
    """A contextual compilation of forensic artifacts grouped together for some purpose, such as filtering, redaction, or association with an investigation."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ArtifactSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    has_artifact: list[ObservableObject] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:hasArtifact', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject', 'alternate_range_iris': []})


@dataclass
class AudioFile(_uco_observable.File):
    """A file whose primary content is audio data (e.g. MP3, WAV, AAC, FLAC)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/AudioFile"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class Bitstream(_uco_observable.ObservableObject):
    """A sequential, complete bit-for-bit copy of a storage medium (LBA0 to LBAmax). Represents data in transit from a capture process to a storage format."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/Bitstream"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class BitstreamRandomAccessed(_uco_observable.ObservableObject):
    """Random access to sector-level data, whether from a live device or a decoded forensic image container. Enables partition parsing, filesystem traversal, and logical operations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/BitstreamRandomAccessed"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class BrowserAppFiles(ApplicationFiles):
    """Files associated with a web browser application, including browsing history, bookmarks, cookies, saved passwords, session data, and extensions."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/BrowserAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class BrowserCacheData(BrowserAppFiles):
    """The locally cached data stored by a web browser to improve performance. This may include cached web pages, images, scripts, and associated metadata. The storage format varies by browser (e.g. Chrome s"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/BrowserCacheData"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class CalendarAppFiles(ApplicationFiles):
    """Files associated with a calendar application, including events, appointments, invitations, recurring schedules, and attendee data (e.g. Apple Calendar, Google Calendar, Outlook Calendar)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/CalendarAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ChatAppFiles(ApplicationFiles):
    """Files associated with a messaging or chat application, including message databases, media attachments, contact lists, and encryption key material (e.g. WhatsApp, Signal, Telegram)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ChatAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ClockOffsetCapture(AcquiredData):
    """The acquisition of a clock offset measurement from a device. Contains the ClockOffsetMeasurement recording the measured difference between the device clock and a reference time source."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ClockOffsetCapture"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    contains: list[ClockOffsetMeasurement] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:contains', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/observable/ClockOffsetMeasurement', 'alternate_range_iris': []})


@dataclass
class ClockOffsetMeasurement(_uco_observable.ObservableObject):
    """The measured difference between a device clock and a reference time source. Records what was compared, the offset value, and when the comparison was made."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ClockOffsetMeasurement"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ClusterRun(_uco_observable.ObservableObject):
    """A contiguous run of clusters allocated to a file in a cluster-based file system (e.g., FAT, NTFS, exFAT). Multiple runs indicate file fragmentation."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ClusterRun"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class ContentQueryData(ServiceBasedExtractionData):
    """Data obtained from an Android device by querying content providers via an ADB shell connection (e.g., adb shell content query). Content providers expose structured data such as contacts, call logs, SM"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ContentQueryData"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class DateTimeRange(_uco_observable.ObservableObject):
    """A time interval with start and end boundaries. Exactly one start property (inclusive or exclusive) and exactly one end property (inclusive or exclusive) must be specified. See SHACL shapes for validat"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DateTimeRange"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class DateTimeStamp(_uco_observable.ObservableObject):
    """A timestamp observed in forensic analysis."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DateTimeStamp"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class DecryptionKey(_uco_observable.ObservableObject):
    """A cryptographic key intended for decryption."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DecryptionKey"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class DeviceInterface(_uco_observable.ObservableObject):
    """A logical interface representing a direct connection to a storage device, such as a USB, SATA."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DeviceInterface"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    provides_access_to: list[StorageMedium] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:providesAccessTo', 'required': False, 'cardinality': 'zero_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/StorageMedium', 'alternate_range_iris': []})


@dataclass
class DeviceScreenshotCapture(AcquiredData):
    """The acquisition of a screenshot from a device screen. Contains the captured image (RasterPicture)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DeviceScreenshotCapture"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    contains: list[RasterPicture] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:contains', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.unifiedcyberontology.org/uco/observable/RasterPicture', 'alternate_range_iris': []})


@dataclass
class DeviceSet(_uco_core.ContextualCompilation):
    """A contextual compilation of devices that are associated in some way, such as devices belonging to the same suspect, devices seized from the same location, or devices connected to the same network."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/DeviceSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class EmailAppFiles(ApplicationFiles):
    """Files associated with an email client application, including message stores, mailbox databases, attachments, contact data, and account configuration (e.g. Outlook, Apple Mail, Gmail app)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/EmailAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class FileSystemExtraction(AcquiredData):
    """Data obtained through direct access to a file system structure. Represents the files and folders as they existed on the device or storage, applicable to any device type (mobile, desktop, embedded). Li"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/FileSystemExtraction"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class FilteredFileSet(FileSet):
    """A subset of files selected from a larger collection by some filtering criteria, such as file type, path, date range, or relevance to an investigation."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/FilteredFileSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ForensicImageContainer(AcquiredData):
    """A forensic image in a container format that encapsulates acquired data, potentially compressed or encrypted, along with embedded metadata such as case information, examiner identity, acquisition times"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ForensicImageContainer"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    contains: list[Any] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:contains', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/observable/Bitstream', 'alternate_range_iris': ['https://ontology.solveit-df.org/solveit/observable/FileSet']})


@dataclass
class GamingAppFiles(ApplicationFiles):
    """Files associated with a gaming application, including save data, player profiles, in-app purchase records, chat logs, friend lists, and gameplay statistics (e.g. Steam, Xbox, PlayStation, Epic Games, """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/GamingAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class HashSet(_uco_core.ContextualCompilation):
    """A reference set of known file hashes used to match against files under examination, in order to reduce or flag the files examined (e.g. NSRL RDS). Composed of HashSetEntry instances."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/HashSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class HashSetEntry(_uco_observable.ObservableObject):
    """A single entry within a hash set. At minimum it carries a hash value; further details (e.g. file name, size, product or operating system, classification) may be added as required."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/HashSetEntry"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class HashVerificationResult(_uco_observable.ObservableObject):
    """The result of comparing hash values to verify data integrity, typically comparing a source hash against a computed hash of acquired or copied data."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/HashVerificationResult"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class HealthAppFiles(ApplicationFiles):
    """Files associated with a health or fitness tracking application, including activity logs, heart rate data, sleep records, workout history, and medical records (e.g. Apple Health, Google Fit, Fitbit)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/HealthAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ImplicitTimingInformation(_uco_observable.ObservableObject):
    """A relative or implicit temporal indicator such as a sequence number, counter value, or ordering index, used when absolute timestamps are not available."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ImplicitTimingInformation"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class KeywordIndex(_uco_observable.ObservableObject):
    """An index of keywords created during forensic analysis."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/KeywordIndex"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class KeywordIndexingConfiguration(_uco_observable.ObservableObject):
    """Configuration settings used for keyword indexing during forensic analysis."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/KeywordIndexingConfiguration"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class KeywordSearchResult(_uco_observable.ObservableObject):
    """A result from a keyword search operation during forensic analysis."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/KeywordSearchResult"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class KeywordSearchResultSet(ArtifactSet):
    """A collection of keyword search results from a search operation. Subsequent techniques may filter or reduce this set, for example by reviewing hits, discarding false positives, or redacting privileged """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/KeywordSearchResultSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class LiveDataCapture(AcquiredData):
    """Volatile or transient data captured from a running system at a specific point in time. Includes running processes, memory state, network connections, device interrogation data (e.g., ideviceinfo outpu"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/LiveDataCapture"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class LiveOSDeviceInterface(DeviceInterface):
    """Access to a block device via the operating system on a live, running system. Provides sector-level access to storage without relying on the OS for file system parsing."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/LiveOSDeviceInterface"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class LogicalImageContainer(ForensicImageContainer):
    """A forensic image container that encapsulates a logical collection of files rather than a bitstream copy, such as a logical image in L01 or ZIP format."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/LogicalImageContainer"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class MapsAppFiles(ApplicationFiles):
    """Files associated with a mapping application, including search history, saved locations, offline map tiles, and location history (e.g. Google Maps, Apple Maps, Waze)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/MapsAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class NavigationAppFiles(ApplicationFiles):
    """Files associated with a turn-by-turn navigation application, including route history, recent destinations, favourite locations, and trip logs (e.g. Waze, TomTom, Garmin)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/NavigationAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class NetworkPacketCapture(_uco_observable.ObservableObject):
    """A network packet capture file."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/NetworkPacketCapture"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class PaymentAppFiles(ApplicationFiles):
    """Files associated with a mobile payment or digital wallet application, including transaction history, linked accounts, merchant data, and receipts (e.g. Apple Pay, Google Pay, PayPal, Venmo)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/PaymentAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class PhotosAppFiles(ApplicationFiles):
    """Files associated with a photos or gallery management application, including image and video databases, album metadata, facial recognition data, location tags, and editing history (e.g. Apple Photos, G"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/PhotosAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class PhysicalImageContainer(ForensicImageContainer):
    """A forensic image container that encapsulates a bitstream (bit-for-bit) copy of a source medium, such as a full disk image in E01 or AFF4 format."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/PhysicalImageContainer"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class PrioritizedDeviceEntry:
    """An entry pairing a device with its triage priority classification."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/PrioritizedDeviceEntry"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class PrioritizedDeviceSet(DeviceSet):
    """A device set where each device has been triaged and assigned a priority classification. Contains PrioritizedDeviceEntry instances that pair each device with its priority."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/PrioritizedDeviceSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class RawImage(AcquiredData):
    """A raw forensic image containing a bitstream without container metadata. Unlike a ForensicImageContainer (e.g. E01, AFF4), a raw image has no embedded metadata. It may be stored across one or more file"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/RawImage"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    contains: list[Bitstream] = field(default_factory=list, metadata={'jsonld_key': 'solveit-observable:contains', 'required': True, 'cardinality': 'one_or_more', 'range_iri': 'https://ontology.solveit-df.org/solveit/observable/Bitstream', 'alternate_range_iris': []})


@dataclass
class RawImageInfoFile(AcquisitionRecordFile):
    """A sidecar file containing metadata for a raw/dd forensic image, including hash values, case information, evidence numbers, examiner details, and acquisition notes. Compensates for the lack of embedded"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/RawImageInfoFile"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class ReadWriteDeviceInterface(DeviceInterface):
    """A logical interface to a storage device that has been interfaced with in a read-write manner, as yet, without write protection."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/ReadWriteDeviceInterface"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class RedactedArtifactSet(ArtifactSet):
    """A collection of artifacts reduced by a redaction process to remove sensitive or privileged content before disclosure."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/RedactedArtifactSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class RedactedFileSet(FilteredFileSet):
    """A subset of files reduced by a redaction process to remove sensitive or privileged content before disclosure."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/RedactedFileSet"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class RemindersAppFiles(ApplicationFiles):
    """Files associated with a reminders or to-do list application, including task lists, due dates, recurring reminders, and completion history (e.g. Apple Reminders, Google Tasks, Todoist)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/RemindersAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class SQLiteDatabase(_uco_observable.File):
    """A SQLite database file stored on disk."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteDatabase"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteField(_uco_observable.ObservableObject):
    """A field (cell) within a SQLite record."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteField"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteFieldDefinition(_uco_observable.ObservableObject):
    """A column definition within a SQLite schema."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteFieldDefinition"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteJournal(_uco_observable.File):
    """A rollback journal file associated with a SQLite database, containing pre-modification page images."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteJournal"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteJournalPageImage(_uco_observable.ObservableObject):
    """A stored copy of a database page as it existed before modification, held in the rollback journal."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteJournalPageImage"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLitePage(_uco_observable.ObservableObject):
    """A physical storage page within a SQLite database file."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLitePage"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteRecord(_uco_observable.ObservableObject):
    """A record (row) within a SQLite table."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteRecord"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteSchema(_uco_observable.ObservableObject):
    """The schema definition for a SQLite table."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteSchema"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteTable(_uco_observable.ObservableObject):
    """A table within a SQLite database."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteTable"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteWAL(_uco_observable.File):
    """A Write-Ahead Log file associated with a SQLite database."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteWAL"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SQLiteWALFrame(_uco_observable.ObservableObject):
    """A single frame within a SQLite WAL, containing a version of a database page."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SQLiteWALFrame"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SmartHomeAppFiles(ApplicationFiles):
    """Files associated with a smart home or IoT control application, including device registries, automation routines, activity logs, sensor data, camera event histories, and network configuration (e.g. App"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SmartHomeAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class SocialMediaAppFiles(ApplicationFiles):
    """Files associated with a social media application, including posts, direct messages, friend/follower lists, media uploads, and notification data (e.g. Instagram, Facebook, TikTok, X)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SocialMediaAppFiles"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class Timeline(_uco_observable.ObservableObject):
    """A set of timeline entries extracted during forensic analysis."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/Timeline"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class SortedTimeline(Timeline):
    """A timeline whose entries have been ordered by position, as determined by a sorting process. Multiple entries may share the same position to indicate they are tied (indistinguishable in order)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SortedTimeline"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class SortedTimelineEntry(_uco_observable.ObservableObject):
    """An intermediary node that associates a TimelineEntry with its ordinal position within a SortedTimeline. This allows the same TimelineEntry to exist in both an unsorted Timeline and a SortedTimeline wi"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/SortedTimelineEntry"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    references_timeline_entry: Optional[TimelineEntry] = field(default=None, metadata={'jsonld_key': 'solveit-observable:referencesTimelineEntry', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'https://ontology.solveit-df.org/solveit/observable/TimelineEntry', 'alternate_range_iris': []})
    sort_position: Optional[int] = field(default=None, metadata={'jsonld_key': 'solveit-observable:sortPosition', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'alternate_range_iris': []})


@dataclass
class TimelineEntry(_uco_observable.ObservableObject):
    """A single entry in a forensic timeline."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/TimelineEntry"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})
    timeline_entry_value: Optional[Any] = field(default=None, metadata={'jsonld_key': 'solveit-observable:timelineEntryValue', 'required': True, 'cardinality': 'exactly_one', 'range_iri': 'https://ontology.solveit-df.org/solveit/observable/DateTimeStamp', 'alternate_range_iris': ['https://ontology.solveit-df.org/solveit/observable/DateTimeRange', 'https://ontology.solveit-df.org/solveit/observable/ImplicitTimingInformation']})


@dataclass
class TimestampOffset(_uco_observable.ObservableObject):
    """The computed difference between two timestamps, expressed in seconds. Positive values indicate the first timestamp is ahead of the second, negative values indicate it is behind."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/TimestampOffset"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class UnlockPattern(_uco_observable.ObservableObject):
    """A pattern used to unlock a device, i.e. screen lock pattern."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/UnlockPattern"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class VideoFile(_uco_observable.File):
    """A file whose primary content is video data (e.g. MP4, MOV, AVI, MKV)."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/VideoFile"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class VideoFrame(_uco_observable.ObservableObject):
    """A single frame extracted from a video file during forensic analysis."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/VideoFrame"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class VirtualizedDevice(_uco_observable.ObservableObject):
    """A device or system that exists as a virtual machine, defined by virtualization configuration and one or more virtual disks rather than running on dedicated physical hardware. A virtualized device may """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/VirtualizedDevice"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class VirtualizedComputer(VirtualizedDevice):
    """A computer (desktop, laptop, or server) that exists as a virtual machine rather than running on physical hardware. The most common form is a server running as a virtual machine in a datacentre or clou"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/VirtualizedComputer"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class Wordlist(_uco_observable.ObservableObject):
    """A list of words or terms used as input to techniques such as keyword searching or dictionary-based password attacks. May be a case-type wordlist (standard terms for a category of investigation), a cas"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/Wordlist"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class WriteProtectedDeviceInterface(DeviceInterface):
    """A logical interface to a storage device that has been interfaced with in a write-protected manner, either via a hardware write blocker, software write blocking, or a read-only boot environment."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/WriteProtectedDeviceInterface"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class httpResponseHeader(_uco_observable.ObservableObject):
    """An HTTP response header containing multiple header fields from an HTTP server response."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/httpResponseHeader"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
    label: Optional[str] = field(default=None, metadata={'jsonld_key': 'rdfs:label', 'required': False, 'cardinality': 'zero_or_one', 'range_iri': 'http://www.w3.org/2001/XMLSchema#string', 'alternate_range_iris': []})


@dataclass
class iOSDeviceGeneratedBackup(DeviceGeneratedBackup):
    """Data produced by the iOS backup mechanism via iTunes, Finder, or libimobiledevice. Contains a manifest database (Manifest.db), file blobs identified by domain-path hashes, and metadata plists includin"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/observable/iOSDeviceGeneratedBackup"
    NAMESPACE_PREFIX: str = "solveit-observable"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
