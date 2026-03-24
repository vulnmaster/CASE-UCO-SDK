// Auto-generated CASE/UCO ontology classes — do not edit manually.
// Module: uco-observable

using System.Collections.Generic;

namespace CaseUco.Uco.Observable
{
    /// <summary>Vocabulary: WhoisDNSSECTypeVocab</summary>
    public static class WhoisDNSSECTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab";
        public const string Signed = "Signed";
        public const string Unsigned = "Unsigned";
    }

    /// <summary>Vocabulary: WindowsVolumeAttributeVocab</summary>
    public static class WindowsVolumeAttributeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab";
        public const string Hidden = "Hidden";
        public const string NoDefaultDriveLetter = "NoDefaultDriveLetter";
        public const string ReadOnly = "ReadOnly";
        public const string ShadowCopy = "ShadowCopy";
    }

    /// <summary>An API (application programming interface) is a computing interface that defines interactions between multiple software or mixed hardware-software intermediaries. It defines the kinds of calls or requ</summary>
    public class API : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/API";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An ARP cache is a collection of Address Resolution Protocol (ARP) entries (mostly dynamic) that are created when an IP address is resolved to a MAC address (so the computer can effectively communicate</summary>
    public class ARPCache : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ARPCache";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An ARP cache entry is a single Address Resolution Protocol (ARP) response record that is created when an IP address is resolved to a MAC address (so the computer can effectively communicate with the I</summary>
    public class ARPCacheEntry : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ARPCacheEntry";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An account is an arrangement with an entity to enable and control the provision of some capability or service.</summary>
    public class Account : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Account";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An account authentication facet is a grouping of characteristics unique to the mechanism of accessing an account.</summary>
    public class AccountAuthenticationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AccountAuthenticationFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:password")]
        public string Password { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:passwordLastChanged")]
        public System.DateTime? PasswordLastChanged { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:passwordType")]
        public string PasswordType { get; set; }
    }

    /// <summary>An account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service.</summary>
    public class AccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:accountIdentifier")]
        public string AccountIdentifier { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:accountIssuer")]
        public CaseUco.Uco.Core.UcoObject AccountIssuer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:accountType")]
        public List<string> AccountType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:expirationTime")]
        public System.DateTime? ExpirationTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isActive")]
        public bool? IsActive { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:owner")]
        public CaseUco.Uco.Core.UcoObject Owner { get; set; }
    }

    /// <summary>An adaptor is a device that physically converts the pin outputs but does not alter the underlying protocol (e.g. uSD to SD, CF to ATA, etc.)</summary>
    public class Adaptor : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Adaptor";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An address is an identifier assigned to enable routing and management of information.</summary>
    public class Address : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Address";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An alternate data stream is data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from access by default NTFS file viewing mechanisms.</summary>
    public class AlternateDataStream : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStream";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An alternate data stream facet is a grouping of characteristics unique to data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from acce</summary>
    public class AlternateDataStreamFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStreamFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:hashes")]
        public CaseUco.Uco.Types.Hash Hashes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:size")]
        public long? Size { get; set; }
    }

    /// <summary>An Android device is a device running the Android operating system. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]</summary>
    public class AndroidDevice : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidDevice";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An Android device facet is a grouping of characteristics unique to an Android device. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]</summary>
    public class AndroidDeviceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidDeviceFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:androidFingerprint")]
        public string AndroidFingerprint { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:androidID")]
        public byte[] AndroidID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:androidVersion")]
        public string AndroidVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isADBRootEnabled")]
        public bool? IsADBRootEnabled { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isSURootEnabled")]
        public bool? IsSURootEnabled { get; set; }
    }

    /// <summary>An android phone is a smart phone that applies the Android mobile operating system.</summary>
    public class AndroidPhone : CaseUco.Uco.Observable.AndroidDevice
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidPhone";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An antenna alignment facet contains the metadata surrounding the cell tower's antenna position.</summary>
    public class AntennaFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AntennaFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:antennaHeight")]
        public decimal? AntennaHeight { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:azimuth")]
        public decimal? Azimuth { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:elevation")]
        public decimal? Elevation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:horizontalBeamWidth")]
        public decimal? HorizontalBeamWidth { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:signalStrength")]
        public decimal? SignalStrength { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:skew")]
        public decimal? Skew { get; set; }
    }

    /// <summary>An apple device is a smart device that applies either the MacOS or iOS operating system.</summary>
    public class AppleDevice : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AppleDevice";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An appliance is a purpose-built computer with software or firmware that is designed to provide a specific computing capability or resource. [based on https://en.wikipedia.org/wiki/Computer_appliance]</summary>
    public class Appliance : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Appliance";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An application is a particular software program designed for end users.</summary>
    public class Application : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Application";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An application account is an account within a particular software program designed for end users.</summary>
    public class ApplicationAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An application account facet is a grouping of characteristics unique to an account within a particular software program designed for end users.</summary>
    public class ApplicationAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
    }

    /// <summary>An application facet is a grouping of characteristics unique to a particular software program designed for end users.</summary>
    public class ApplicationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:applicationIdentifier")]
        public string ApplicationIdentifier { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:installedVersionHistory")]
        public List<CaseUco.Uco.Observable.ApplicationVersion> InstalledVersionHistory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:numberOfLaunches")]
        public long? NumberOfLaunches { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:operatingSystem")]
        public CaseUco.Uco.Observable.ObservableObject OperatingSystem { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
    }

    /// <summary>An application version is a grouping of characteristics unique to a particular software program version.</summary>
    public class ApplicationVersion : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationVersion";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:installDate")]
        public System.DateTime? InstallDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:uninstallDate")]
        public System.DateTime? UninstallDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
    }

    /// <summary>An archive file is a file that is composed of one or more computer files along with metadata.</summary>
    public class ArchiveFile : CaseUco.Uco.Observable.File
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFile";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An archive file facet is a grouping of characteristics unique to a file that is composed of one or more computer files along with metadata.</summary>
    public class ArchiveFileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:archiveType")]
        public string ArchiveType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:comment")]
        public string Comment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
    }

    /// <summary>Audio is a digital representation of sound.</summary>
    public class Audio : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Audio";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An audio facet is a grouping of characteristics unique to a digital representation of sound.</summary>
    public class AudioFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AudioFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:audioType")]
        public string AudioType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bitRate")]
        public long? BitRate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:duration")]
        public long? Duration { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:format")]
        public string Format { get; set; }
    }

    /// <summary>An autonomous system is a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of a single administrative entity or domain that </summary>
    public class AutonomousSystem : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystem";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An autonomous system facet is a grouping of characteristics unique to a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of </summary>
    public class AutonomousSystemFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystemFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:asHandle")]
        public string AsHandle { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:number")]
        public long? Number { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:regionalInternetRegistry")]
        public List<string> RegionalInternetRegistry { get; set; }
    }

    /// <summary>A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blackberry 10 re-introduces Blackberry OS, prior to that the OS was Android.)</summary>
    public class BlackberryPhone : CaseUco.Uco.Observable.SmartPhone
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BlackberryPhone";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A block device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing buffered randomly accesible input and output. Block device nodes are used to apply</summary>
    public class BlockDeviceNode : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BlockDeviceNode";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Bluetooth address is a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards conformant communication to or from that device</summary>
    public class BluetoothAddress : CaseUco.Uco.Observable.MACAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Bluetooth address facet is a grouping of characteristics unique to a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards c</summary>
    public class BluetoothAddressFacet : CaseUco.Uco.Observable.MACAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A bot configuration is a set of contextual settings for a software application that runs automated tasks (scripts) over the Internet at a much higher rate than would be possible for a human alone.</summary>
    public class BotConfiguration : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BotConfiguration";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on https://techterms.com/definition/bookmark]</summary>
    public class BrowserBookmark : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmark";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on htt</summary>
    public class BrowserBookmarkFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmarkFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:accessedTime")]
        public System.DateTime? AccessedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bookmarkPath")]
        public string BookmarkPath { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:urlTargeted")]
        public List<System.Uri> UrlTargeted { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:visitCount")]
        public long? VisitCount { get; set; }
    }

    /// <summary>A browser cookie is a piece of of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on https://en.wikipedia.org/wiki/HTTP_cookie]</summary>
    public class BrowserCookie : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookie";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on </summary>
    public class BrowserCookieFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookieFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:accessedTime")]
        public System.DateTime? AccessedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cookieDomain")]
        public CaseUco.Uco.Observable.ObservableObject CookieDomain { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cookieName")]
        public string CookieName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cookiePath")]
        public string CookiePath { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:expirationTime")]
        public System.DateTime? ExpirationTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isSecure")]
        public bool? IsSecure { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
    }

    /// <summary>A calendar is a collection of appointments, meetings, and events.</summary>
    public class Calendar : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Calendar";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A calendar entry is an appointment, meeting or event within a collection of appointments, meetings and events.</summary>
    public class CalendarEntry : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntry";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A calendar entry facet is a grouping of characteristics unique to an appointment, meeting, or event within a collection of appointments, meetings, and events.</summary>
    public class CalendarEntryFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntryFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:attendant")]
        public List<CaseUco.Uco.Identity.Identity> Attendant { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:duration")]
        public long? Duration { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventStatus")]
        public string EventStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventType")]
        public string EventType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isPrivate")]
        public bool? IsPrivate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:location")]
        public CaseUco.Uco.Location.Location Location { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:owner")]
        public CaseUco.Uco.Core.UcoObject Owner { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:recurrence")]
        public string Recurrence { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:remindTime")]
        public System.DateTime? RemindTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startTime")]
        public System.DateTime? StartTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subject")]
        public string Subject { get; set; }
    }

    /// <summary>A calendar facet is a grouping of characteristics unique to a collection of appointments, meetings, and events.</summary>
    public class CalendarFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:owner")]
        public CaseUco.Uco.Core.UcoObject Owner { get; set; }
    }

    /// <summary>A call is a connection as part of a realtime cyber communication between one or more parties.</summary>
    public class Call : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Call";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber communication between one or more parties.</summary>
    public class CallFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CallFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:callType")]
        public string CallType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:duration")]
        public long? Duration { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:from")]
        public CaseUco.Uco.Observable.ObservableObject From { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:participant")]
        public List<CaseUco.Uco.Observable.ObservableObject> Participant { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startTime")]
        public System.DateTime? StartTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:to")]
        public List<CaseUco.Uco.Observable.ObservableObject> To { get; set; }
    }

    /// <summary>CapturedTelecommunicationsInformation</summary>
    public class CapturedTelecommunicationsInformation : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformation";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A captured telecommunications information facet represents certain information within captured or intercepted telecommunications data.</summary>
    public class CapturedTelecommunicationsInformationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformationFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:captureCellSite")]
        public CaseUco.Uco.Observable.CellSite CaptureCellSite { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:interceptedCallState")]
        public string InterceptedCallState { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startTime")]
        public System.DateTime? StartTime { get; set; }
    }

    /// <summary>CellSite</summary>
    public class CellSite : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CellSite";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A cell site facet contains the metadata surrounding the cell site.</summary>
    public class CellSiteFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CellSiteFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:cellSiteCountryCode")]
        public string CellSiteCountryCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cellSiteIdentifier")]
        public string CellSiteIdentifier { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cellSiteLocationAreaCode")]
        public string CellSiteLocationAreaCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cellSiteNetworkCode")]
        public string CellSiteNetworkCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cellSiteType")]
        public string CellSiteType { get; set; }
    }

    /// <summary>A character device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing only a serial stream of input or accepting a serial stream of output. Characte</summary>
    public class CharacterDeviceNode : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CharacterDeviceNode";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>Code is a direct representation (source, byte or binary) of a collection of computer instructions that form software which tell a computer how to work. [based on https://en.wikipedia.org/wiki/Software</summary>
    public class Code : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Code";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A compressed stream facet is a grouping of characteristics unique to the application of a size-reduction process to a body of data content.</summary>
    public class CompressedStreamFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CompressedStreamFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:compressionMethod")]
        public string CompressionMethod { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:compressionRatio")]
        public decimal? CompressionRatio { get; set; }
    }

    /// <summary>A computer is an electronic device for storing and processing data, typically in binary, according to instructions given to it in a variable program. [based on 'Computer.' Oxford English Dictionary, O</summary>
    public class Computer : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Computer";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A computer specification is the hardware and software of a programmable electronic device that can store, retrieve, and process data. {based on merriam-webster.com/dictionary/computer]</summary>
    public class ComputerSpecification : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecification";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A computer specificaiton facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data. [based on merriam-we</summary>
    public class ComputerSpecificationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecificationFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:availableRam")]
        public long? AvailableRam { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:biosDate")]
        public System.DateTime? BiosDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:biosManufacturer")]
        public string BiosManufacturer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:biosReleaseDate")]
        public System.DateTime? BiosReleaseDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:biosSerialNumber")]
        public string BiosSerialNumber { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:biosVersion")]
        public string BiosVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cpu")]
        public string Cpu { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cpuFamily")]
        public string CpuFamily { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:currentSystemDate")]
        public System.DateTime? CurrentSystemDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:gpu")]
        public string Gpu { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:gpuFamily")]
        public string GpuFamily { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:hostname")]
        public string Hostname { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:localTime")]
        public System.DateTime? LocalTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:networkInterface")]
        public List<CaseUco.Uco.Observable.ObservableObject> NetworkInterface { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:processorArchitecture")]
        public string ProcessorArchitecture { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:systemTime")]
        public System.DateTime? SystemTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:timezoneDST")]
        public string TimezoneDST { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:timezoneStandard")]
        public string TimezoneStandard { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:totalRam")]
        public long? TotalRam { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:uptime")]
        public string Uptime { get; set; }
    }

    /// <summary>A ConfiguredSoftware is a Software that is known to be configured to run in a more specified manner than some unconfigured or less-configured Software.</summary>
    public class ConfiguredSoftware : CaseUco.Uco.Observable.Software
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ConfiguredSoftware";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-configuration:isConfigurationOf")]
        public CaseUco.Uco.Observable.Software IsConfigurationOf { get; set; }
        [global::CaseUco.JsonLdProperty("uco-configuration:usesConfiguration")]
        public CaseUco.Uco.Configuration.Configuration UsesConfiguration { get; set; }
    }

    /// <summary>A contact is a set of identification and communication related details for a single entity.</summary>
    public class Contact : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Contact";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A contact address is a grouping of characteristics unique to a geolocation address of a contact entity.</summary>
    public class ContactAddress : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactAddressScope")]
        public List<string> ContactAddressScope { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:geolocationAddress")]
        public CaseUco.Uco.Location.Location GeolocationAddress { get; set; }
    }

    /// <summary>A contact affiliation is a grouping of characteristics unique to details of an organizational affiliation for a single contact entity.</summary>
    public class ContactAffiliation : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactAffiliation";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactEmail")]
        public List<CaseUco.Uco.Observable.ContactEmail> ContactEmail { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactMessaging")]
        public List<CaseUco.Uco.Observable.ContactMessaging> ContactMessaging { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactOrganization")]
        public CaseUco.Uco.Identity.Organization ContactOrganization { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactPhone")]
        public List<CaseUco.Uco.Observable.ContactPhone> ContactPhone { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactProfile")]
        public List<CaseUco.Uco.Observable.ContactProfile> ContactProfile { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactURL")]
        public List<CaseUco.Uco.Observable.ContactURL> ContactURL { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:organizationDepartment")]
        public string OrganizationDepartment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:organizationLocation")]
        public List<CaseUco.Uco.Observable.ContactAddress> OrganizationLocation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:organizationPosition")]
        public string OrganizationPosition { get; set; }
    }

    /// <summary>A contact email is a grouping of characteristics unique to details for contacting a contact entity by email.</summary>
    public class ContactEmail : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactEmailScope")]
        public List<string> ContactEmailScope { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:emailAddress")]
        public CaseUco.Uco.Observable.ObservableObject EmailAddress { get; set; }
    }

    /// <summary>A contact facet is a grouping of characteristics unique to a set of identification and communication related details for a single entity.</summary>
    public class ContactFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-identity:birthdate")]
        public System.DateTime? Birthdate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactAddress")]
        public List<CaseUco.Uco.Observable.ContactAddress> ContactAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactAffiliation")]
        public List<CaseUco.Uco.Observable.ContactAffiliation> ContactAffiliation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactEmail")]
        public List<CaseUco.Uco.Observable.ContactEmail> ContactEmail { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactGroup")]
        public List<string> ContactGroup { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactID")]
        public string ContactID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactMessaging")]
        public List<CaseUco.Uco.Observable.ContactMessaging> ContactMessaging { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactNote")]
        public List<string> ContactNote { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactPhone")]
        public List<CaseUco.Uco.Observable.ContactPhone> ContactPhone { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactProfile")]
        public List<CaseUco.Uco.Observable.ContactProfile> ContactProfile { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactSIP")]
        public List<CaseUco.Uco.Observable.ContactSIP> ContactSIP { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactURL")]
        public List<CaseUco.Uco.Observable.ContactURL> ContactURL { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:displayName")]
        public string DisplayName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:firstName")]
        public string FirstName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lastName")]
        public string LastName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lastTimeContacted")]
        public System.DateTime? LastTimeContacted { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:middleName")]
        public string MiddleName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:namePhonetic")]
        public string NamePhonetic { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:namePrefix")]
        public string NamePrefix { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:nameSuffix")]
        public string NameSuffix { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:nickname")]
        public List<string> Nickname { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:numberTimesContacted")]
        public long? NumberTimesContacted { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sourceApplication")]
        public CaseUco.Uco.Observable.ObservableObject SourceApplication { get; set; }
    }

    /// <summary>A contact list is a set of multiple individual contacts such as that found in a digital address book.</summary>
    public class ContactList : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactList";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A contact list facet is a grouping of characteristics unique to a set of multiple individual contacts such as that found in a digital address book.</summary>
    public class ContactListFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactListFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contact")]
        public List<CaseUco.Uco.Observable.ObservableObject> Contact { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sourceApplication")]
        public CaseUco.Uco.Observable.ObservableObject SourceApplication { get; set; }
    }

    /// <summary>A contact messaging is a grouping of characteristics unique to details for contacting a contact entity by digital messaging.</summary>
    public class ContactMessaging : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactMessagingPlatform")]
        public CaseUco.Uco.Observable.ObservableObject ContactMessagingPlatform { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:messagingAddress")]
        public CaseUco.Uco.Observable.ObservableObject MessagingAddress { get; set; }
    }

    /// <summary>A contact phone is a grouping of characteristics unique to details for contacting a contact entity by telephone.</summary>
    public class ContactPhone : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactPhoneNumber")]
        public CaseUco.Uco.Observable.ObservableObject ContactPhoneNumber { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactPhoneScope")]
        public List<string> ContactPhoneScope { get; set; }
    }

    /// <summary>A contact profile is a grouping of characteristics unique to details for contacting a contact entity by online service.</summary>
    public class ContactProfile : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactProfile";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactProfilePlatform")]
        public CaseUco.Uco.Observable.ObservableObject ContactProfilePlatform { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profile")]
        public CaseUco.Uco.Observable.ObservableObject Profile { get; set; }
    }

    /// <summary>A contact SIP is a grouping of characteristics unique to details for contacting a contact entity by Session Initiation Protocol (SIP).</summary>
    public class ContactSIP : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactSIP";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactSIPScope")]
        public List<string> ContactSIPScope { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sipAddress")]
        public CaseUco.Uco.Observable.ObservableObject SipAddress { get; set; }
    }

    /// <summary>A contact URL is a grouping of characteristics unique to details for contacting a contact entity by Uniform Resource Locator (URL).</summary>
    public class ContactURL : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContactURL";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactURLScope")]
        public List<string> ContactURLScope { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:url")]
        public CaseUco.Uco.Observable.ObservableObject Url { get; set; }
    }

    /// <summary>Content data is a block of digital data.</summary>
    public class ContentData : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContentData";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A content data facet is a grouping of characteristics unique to a block of digital data.</summary>
    public class ContentDataFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ContentDataFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:byteOrder")]
        public List<string> ByteOrder { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dataPayload")]
        public string DataPayload { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dataPayloadReferenceURL")]
        public CaseUco.Uco.Observable.ObservableObject DataPayloadReferenceURL { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:entropy")]
        public decimal? Entropy { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:hash")]
        public List<CaseUco.Uco.Types.Hash> Hash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isEncrypted")]
        public bool? IsEncrypted { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:magicNumber")]
        public string MagicNumber { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mimeClass")]
        public string MimeClass { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mimeType")]
        public List<string> MimeType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeInBytes")]
        public long? SizeInBytes { get; set; }
    }

    /// <summary>A cookie history is the stored web cookie history for a particular web browser.</summary>
    public class CookieHistory : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CookieHistory";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A credential is a single specific login and password combination for authorization of access to a digital account or system.</summary>
    public class Credential : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Credential";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A credential dump is a collection (typically forcibly extracted from a system) of specific login and password combinations for authorization of access to a digital account or system.</summary>
    public class CredentialDump : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/CredentialDump";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query results (created when an domain name is resolved to a IP address) for a particular computer.</summary>
    public class DNSCache : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DNSCache";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A DNS record is a single Domain Name System (DNS) artifact specifying information of a particular type (routing, authority, responsibility, security, etc.) for a specific Internet domain name.</summary>
    public class DNSRecord : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DNSRecord";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A data range facet is a grouping of characteristics unique to a particular contiguous scope within a block of digital data.</summary>
    public class DataRangeFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DataRangeFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:rangeOffset")]
        public long? RangeOffset { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:rangeOffsetType")]
        public string RangeOffsetType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:rangeSize")]
        public long? RangeSize { get; set; }
    }

    /// <summary>A defined effect facet is a grouping of characteristics unique to the effect of an observable action in relation to one or more observable objects.</summary>
    public class DefinedEffectFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DefinedEffectFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.com/dictionary/device]</summary>
    public class Device : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Device";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.c</summary>
    public class DeviceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DeviceFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:cpeid")]
        public string Cpeid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:deviceType")]
        public string DeviceType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:manufacturer")]
        public CaseUco.Uco.Identity.Identity Manufacturer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:model")]
        public string Model { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:serialNumber")]
        public string SerialNumber { get; set; }
    }

    /// <summary>A digital account is an arrangement with an entity to enable and control the provision of some capability or service within the digital domain.</summary>
    public class DigitalAccount : CaseUco.Uco.Observable.Account
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A digital account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service within the digital domain.</summary>
    public class DigitalAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:accountLogin")]
        public List<string> AccountLogin { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:displayName")]
        public string DisplayName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:firstLoginTime")]
        public System.DateTime? FirstLoginTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isDisabled")]
        public bool? IsDisabled { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lastLoginTime")]
        public System.DateTime? LastLoginTime { get; set; }
    }

    /// <summary>A digital address is an identifier assigned to enable routing and management of digital communication.</summary>
    public class DigitalAddress : CaseUco.Uco.Observable.Address
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A digital address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of digital communication.</summary>
    public class DigitalAddressFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:addressValue")]
        public string AddressValue { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:displayName")]
        public string DisplayName { get; set; }
    }

    /// <summary>A digital camera is a camera that captures photographs in digital memory as opposed to capturing images on photographic film.</summary>
    public class DigitalCamera : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalCamera";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A digital signature info is a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document.</summary>
    public class DigitalSignatureInfo : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfo";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A digital signature info facet is a grouping of characteristics unique to a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document.</summary>
    public class DigitalSignatureInfoFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfoFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:certificateIssuer")]
        public CaseUco.Uco.Identity.Identity CertificateIssuer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:certificateSubject")]
        public CaseUco.Uco.Core.UcoObject CertificateSubject { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:signatureDescription")]
        public string SignatureDescription { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:signatureExists")]
        public bool? SignatureExists { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:signatureVerified")]
        public bool? SignatureVerified { get; set; }
    }

    /// <summary>A directory is a file system cataloging structure which contains references to other computer files, and possibly other directories. On many computers, directories are known as folders, or drawers, an</summary>
    public class Directory : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Directory";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A disk is a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating disks.</summary>
    public class Disk : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Disk";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A disk facet is a grouping of characteristics unique to a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rot</summary>
    public class DiskFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DiskFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:diskSize")]
        public long? DiskSize { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:diskType")]
        public string DiskType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:freeSpace")]
        public long? FreeSpace { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:partition")]
        public List<CaseUco.Uco.Observable.ObservableObject> Partition { get; set; }
    }

    /// <summary>A disk partition is a particular managed region on a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating</summary>
    public class DiskPartition : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DiskPartition";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A disk partition facet is a grouping of characteristics unique to a particular managed region on a storage mechanism.</summary>
    public class DiskPartitionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DiskPartitionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:diskPartitionType")]
        public string DiskPartitionType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mountPoint")]
        public string MountPoint { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:partitionID")]
        public string PartitionID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:partitionLength")]
        public long? PartitionLength { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:partitionOffset")]
        public long? PartitionOffset { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:spaceLeft")]
        public long? SpaceLeft { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:spaceUsed")]
        public long? SpaceUsed { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:totalSpace")]
        public long? TotalSpace { get; set; }
    }

    /// <summary>A domain name is an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.wikipedia.org/wiki/Domain_name]</summary>
    public class DomainName : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DomainName";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A domain name facet is a grouping of characteristics unique to an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.</summary>
    public class DomainNameFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/DomainNameFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:isTLD")]
        public bool? IsTLD { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:value")]
        public string Value { get; set; }
    }

    /// <summary>A drone, unmanned aerial vehicle (UAV), is an aircraft without a human pilot, crew, or passengers that typically involve a ground-based controller and a system for communications with the UAV.</summary>
    public class Drone : CaseUco.Uco.Observable.MobileDevice
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Drone";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners an</summary>
    public class EXIFFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EXIFFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:exifData")]
        public List<CaseUco.Uco.Types.ControlledDictionary> ExifData { get; set; }
    }

    /// <summary>An email account is an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services.</summary>
    public class EmailAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An email account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services.</summary>
    public class EmailAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:emailAddress")]
        public CaseUco.Uco.Observable.ObservableObject EmailAddress { get; set; }
    }

    /// <summary>An email address is an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are sent from and delivered to.</summary>
    public class EmailAddress : CaseUco.Uco.Observable.DigitalAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An email address facet is a grouping of characteristics unique to an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are</summary>
    public class EmailAddressFacet : CaseUco.Uco.Observable.DigitalAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An email message is a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and related RFCs.</summary>
    public class EmailMessage : CaseUco.Uco.Observable.Message
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmailMessage";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An email message facet is a grouping of characteristics unique to a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and</summary>
    public class EmailMessageFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmailMessageFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bcc")]
        public List<CaseUco.Uco.Observable.ObservableObject> Bcc { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:body")]
        public string Body { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bodyMultipart")]
        public List<CaseUco.Uco.Observable.MimePartType> BodyMultipart { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bodyRaw")]
        public CaseUco.Uco.Observable.ObservableObject BodyRaw { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:categories")]
        public List<string> Categories { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cc")]
        public List<CaseUco.Uco.Observable.ObservableObject> Cc { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contentDisposition")]
        public string ContentDisposition { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contentType")]
        public string ContentType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:from")]
        public CaseUco.Uco.Observable.ObservableObject From { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:headerRaw")]
        public CaseUco.Uco.Observable.ObservableObject HeaderRaw { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:inReplyTo")]
        public string InReplyTo { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isMimeEncoded")]
        public bool? IsMimeEncoded { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isMultipart")]
        public bool? IsMultipart { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isRead")]
        public bool? IsRead { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:labels")]
        public List<string> Labels { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:messageID")]
        public string MessageID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:otherHeaders")]
        public CaseUco.Uco.Types.Dictionary OtherHeaders { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:priority")]
        public string Priority { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:receivedLines")]
        public List<string> ReceivedLines { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:receivedTime")]
        public System.DateTime? ReceivedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:references")]
        public List<CaseUco.Uco.Observable.ObservableObject> References { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sender")]
        public CaseUco.Uco.Observable.ObservableObject Sender { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sentTime")]
        public System.DateTime? SentTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subject")]
        public string Subject { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:to")]
        public List<CaseUco.Uco.Observable.ObservableObject> To { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:xMailer")]
        public string XMailer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:xOriginatingIP")]
        public CaseUco.Uco.Observable.ObservableObject XOriginatingIP { get; set; }
    }

    /// <summary>An embedded device is a highly specialized microprocessor device meant for one or very few specific purposes and is usually embedded or included within another object or as part of a larger system. Ex</summary>
    public class EmbeddedDevice : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EmbeddedDevice";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An encoded stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another form.</summary>
    public class EncodedStreamFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EncodedStreamFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:encodingMethod")]
        public string EncodingMethod { get; set; }
    }

    /// <summary>An encrypted stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another obfuscated form in such a way that reversing the conversion to ob</summary>
    public class EncryptedStreamFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EncryptedStreamFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:encryptionIV")]
        public List<string> EncryptionIV { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:encryptionKey")]
        public List<string> EncryptionKey { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:encryptionMethod")]
        public string EncryptionMethod { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:encryptionMode")]
        public string EncryptionMode { get; set; }
    }

    /// <summary>An environment variable is a grouping of characteristics unique to a dynamic-named value that can affect the way running processes will behave on a computer. [based on https://en.wikipedia.org/wiki/En</summary>
    public class EnvironmentVariable : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EnvironmentVariable";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:value")]
        public string Value { get; set; }
    }

    /// <summary>An event log is a collection of event records.</summary>
    public class EventLog : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EventLog";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An event record is something that happens in a digital context (e.g., operating system events).</summary>
    public class EventRecord : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EventRecord";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An event record facet is a grouping of characteristics unique to something that happens in a digital context (e.g., operating system events).</summary>
    public class EventRecordFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/EventRecordFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:account")]
        public CaseUco.Uco.Observable.ObservableObject Account { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:cyberAction")]
        public CaseUco.Uco.Observable.ObservableAction CyberAction { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventID")]
        public string EventID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventRecordDevice")]
        public CaseUco.Uco.Observable.ObservableObject EventRecordDevice { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventRecordID")]
        public string EventRecordID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventRecordRaw")]
        public string EventRecordRaw { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventRecordServiceName")]
        public string EventRecordServiceName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventRecordText")]
        public string EventRecordText { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:eventType")]
        public string EventType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startTime")]
        public System.DateTime? StartTime { get; set; }
    }

    /// <summary>An extInode facet is a grouping of characteristics unique to a file system object (file, directory, etc.) conformant to the extended file system (EXT or related derivations) specification.</summary>
    public class ExtInodeFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ExtInodeFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:extDeletionTime")]
        public System.DateTime? ExtDeletionTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extFileType")]
        public long? ExtFileType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extFlags")]
        public long? ExtFlags { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extHardLinkCount")]
        public long? ExtHardLinkCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extInodeChangeTime")]
        public System.DateTime? ExtInodeChangeTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extInodeID")]
        public long? ExtInodeID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extPermissions")]
        public long? ExtPermissions { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extSGID")]
        public long? ExtSGID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extSUID")]
        public long? ExtSUID { get; set; }
    }

    /// <summary>An extracted string is a grouping of characteristics unique to a series of characters pulled from an observable object.</summary>
    public class ExtractedString : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ExtractedString";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:byteStringValue")]
        public byte[] ByteStringValue { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:encoding")]
        public string Encoding { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:englishTranslation")]
        public string EnglishTranslation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:language")]
        public string Language { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:length")]
        public long? Length { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:stringValue")]
        public string StringValue { get; set; }
    }

    /// <summary>An extracted strings facet is a grouping of characteristics unique to one or more sequences of characters pulled from an observable object.</summary>
    public class ExtractedStringsFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ExtractedStringsFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:strings")]
        public List<CaseUco.Uco.Observable.ExtractedString> Strings { get; set; }
    }

    /// <summary>A file is a computer resource for recording data discretely on a computer storage device.</summary>
    public class File : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/File";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A file facet is a grouping of characteristics unique to the storage of a file (computer resource for recording data discretely in a computer storage device) on a file system (process that manages how </summary>
    public class FileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/FileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:accessedTime")]
        public System.DateTime? AccessedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:allocationStatus")]
        public string AllocationStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extension")]
        public string Extension { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:fileName")]
        public List<string> FileName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:filePath")]
        public List<string> FilePath { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isDirectory")]
        public List<bool> IsDirectory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:metadataChangeTime")]
        public System.DateTime? MetadataChangeTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeInBytes")]
        public long? SizeInBytes { get; set; }
    }

    /// <summary>A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a file system.</summary>
    public class FilePermissionsFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/FilePermissionsFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:owner")]
        public CaseUco.Uco.Core.UcoObject Owner { get; set; }
    }

    /// <summary>A file system is the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/definition/5510/file-system]</summary>
    public class FileSystem : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystem";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A file system facet is a grouping of characteristics unique to the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/def</summary>
    public class FileSystemFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystemFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:clusterSize")]
        public long? ClusterSize { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:fileSystemType")]
        public string FileSystemType { get; set; }
    }

    /// <summary>A file system object is an informational object represented and managed within a file system.</summary>
    public class FileSystemObject : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystemObject";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A forum post is message submitted by a user account to an online forum where the message content (and typically metadata including who posted it and when) is viewable by any party with viewing permiss</summary>
    public class ForumPost : CaseUco.Uco.Observable.Message
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ForumPost";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A forum private message (aka PM or DM (direct message)) is a one-to-one message from one specific user account to another specific user account on an online form where transmission is managed by the o</summary>
    public class ForumPrivateMessage : CaseUco.Uco.Observable.Message
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ForumPrivateMessage";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A fragment facet is a grouping of characteristics unique to an individual piece of the content of a file.</summary>
    public class FragmentFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/FragmentFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:fragmentIndex")]
        public List<long> FragmentIndex { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:totalFragments")]
        public List<long> TotalFragments { get; set; }
    }

    /// <summary>A GUI is a graphical user interface that allows users to interact with electronic devices through graphical icons and audio indicators such as primary notation, instead of text-based user interfaces, </summary>
    public class GUI : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GUI";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A gaming console (video game console or game console) is an electronic system that connects to a display, typically a TV or computer monitor, for the primary purpose of playing video games.</summary>
    public class GamingConsole : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GamingConsole";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A generic observable object is an article or unit within the digital domain.</summary>
    public class GenericObservableObject : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GenericObservableObject";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A geolocation entry is a single application-specific geolocation entry.</summary>
    public class GeoLocationEntry : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntry";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A geolocation entry facet is a grouping of characteristics unique to a single application-specific geolocation entry.</summary>
    public class GeoLocationEntryFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntryFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:location")]
        public CaseUco.Uco.Location.Location Location { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
    }

    /// <summary>A geolocation log is a record containing geolocation tracks and/or geolocation entries.</summary>
    public class GeoLocationLog : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLog";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A geolocation log facet is a grouping of characteristics unique to a record containing geolocation tracks and/or geolocation entries.</summary>
    public class GeoLocationLogFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLogFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
    }

    /// <summary>A geolocation track is a set of contiguous geolocation entries representing a path/track taken.</summary>
    public class GeoLocationTrack : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrack";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A geolocation track facet is a grouping of characteristics unique to a set of contiguous geolocation entries representing a path/track taken.</summary>
    public class GeoLocationTrackFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrackFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:geoLocationEntry")]
        public List<CaseUco.Uco.Observable.ObservableObject> GeoLocationEntry { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startTime")]
        public System.DateTime? StartTime { get; set; }
    }

    /// <summary>A global flag type is a grouping of characteristics unique to the Windows systemwide global variable named NtGlobalFlag that enables various internal debugging, tracing, and validation support in the </summary>
    public class GlobalFlagType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/GlobalFlagType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:abbreviation")]
        public string Abbreviation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:destination")]
        public string Destination { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:hexadecimalValue")]
        public List<byte[]> HexadecimalValue { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:symbolicName")]
        public string SymbolicName { get; set; }
    }

    /// <summary>An HTTP connection is network connection that is conformant to the Hypertext Transfer Protocol (HTTP) standard.</summary>
    public class HTTPConnection : CaseUco.Uco.Observable.NetworkConnection
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnection";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An HTTP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Hypertext Transfer Protocol (HTTP) standard.</summary>
    public class HTTPConnectionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnectionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:httpMesageBodyLength")]
        public long? HttpMesageBodyLength { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:httpMessageBodyData")]
        public CaseUco.Uco.Observable.ObservableObject HttpMessageBodyData { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:httpRequestHeader")]
        public CaseUco.Uco.Types.Dictionary HttpRequestHeader { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:requestMethod")]
        public string RequestMethod { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:requestValue")]
        public string RequestValue { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:requestVersion")]
        public string RequestVersion { get; set; }
    }

    /// <summary>A hostname is a label that is assigned to a device connected to a computer network and that is used to identify the device in various forms of electronic communication, such as the World Wide Web. A h</summary>
    public class Hostname : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Hostname";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An ICMP connection is a network connection that is conformant to the Internet Control Message Protocol (ICMP) standard.</summary>
    public class ICMPConnection : CaseUco.Uco.Observable.NetworkConnection
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnection";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An ICMP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Internet Control Message Protocol (ICMP) standard.</summary>
    public class ICMPConnectionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnectionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:icmpCode")]
        public List<byte[]> IcmpCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:icmpType")]
        public List<byte[]> IcmpType { get; set; }
    }

    /// <summary>An IComHandler action type is a grouping of characteristics unique to a Windows Task-related action that fires a Windows COM handler (smart code in the client address space that can optimize calls bet</summary>
    public class IComHandlerActionType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IComHandlerActionType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:comClassID")]
        public string ComClassID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:comData")]
        public string ComData { get; set; }
    }

    /// <summary>An IExec action type is a grouping of characteristics unique to an action that executes a command-line operation on a Windows operating system. [based on https://docs.microsoft.com/en-us/windows/win32</summary>
    public class IExecActionType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IExecActionType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:execArguments")]
        public string ExecArguments { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:execProgramHashes")]
        public List<CaseUco.Uco.Types.Hash> ExecProgramHashes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:execProgramPath")]
        public string ExecProgramPath { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:execWorkingDirectory")]
        public string ExecWorkingDirectory { get; set; }
    }

    /// <summary>An IP address is an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conformant communication to or from that device.</summary>
    public class IPAddress : CaseUco.Uco.Observable.DigitalAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IP address facet is a grouping of characteristics unique to an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conforman</summary>
    public class IPAddressFacet : CaseUco.Uco.Observable.DigitalAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IP netmask is a 32-bit 'mask' used to divide an IP address into subnets and specify the network's available hosts.</summary>
    public class IPNetmask : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPNetmask";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An iPhone is a smart phone that applies the iOS mobile operating system.</summary>
    public class IPhone : CaseUco.Uco.Observable.AppleDevice
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPhone";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 standards conformant communication to or from tha</summary>
    public class IPv4Address : CaseUco.Uco.Observable.IPAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPv4Address";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 sta</summary>
    public class IPv4AddressFacet : CaseUco.Uco.Observable.IPAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPv4AddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 standards conformant communication to or from tha</summary>
    public class IPv6Address : CaseUco.Uco.Observable.IPAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPv6Address";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 sta</summary>
    public class IPv6AddressFacet : CaseUco.Uco.Observable.IPAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IPv6AddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An IShow message action type is a grouping of characteristics unique to an action that shows a message box when a task is activate. [based on https://docs.microsoft.com/en-us/windows/win32/api/tasksch</summary>
    public class IShowMessageActionType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/IShowMessageActionType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:showMessageBody")]
        public string ShowMessageBody { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:showMessageTitle")]
        public string ShowMessageTitle { get; set; }
    }

    /// <summary>An image is a complete copy of a hard disk, memory, or other digital media.</summary>
    public class Image : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Image";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An image facet is a grouping of characteristics unique to a complete copy of a hard disk, memory, or other digital media.</summary>
    public class ImageFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ImageFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:imageType")]
        public string ImageType { get; set; }
    }

    /// <summary>InstantMessagingAddress</summary>
    public class InstantMessagingAddress : CaseUco.Uco.Observable.DigitalAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An instant messaging address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of instant messaging digital communication.</summary>
    public class InstantMessagingAddressFacet : CaseUco.Uco.Observable.DigitalAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory access to another directory which can be on the same volume or another volume. A junction is similar to</summary>
    public class Junction : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Junction";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A laptop, laptop computer, or notebook computer is a small, portable personal computer with a screen and alphanumeric keyboard. These typically have a clam shell form factor with the screen mounted on</summary>
    public class Laptop : CaseUco.Uco.Observable.Computer
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Laptop";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A library is a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definition/3828/software-library]</summary>
    public class Library : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Library";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A library facet is a grouping of characteristics unique to a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definit</summary>
    public class LibraryFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/LibraryFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:libraryType")]
        public string LibraryType { get; set; }
    }

    /// <summary>A MAC address is a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications at the data link layer of a network segment.</summary>
    public class MACAddress : CaseUco.Uco.Observable.DigitalAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MACAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A MAC address facet is a grouping of characteristics unique to a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications</summary>
    public class MACAddressFacet : CaseUco.Uco.Observable.DigitalAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MACAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>Memory is a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device.</summary>
    public class Memory : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Memory";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A memory facet is a grouping of characteristics unique to a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device.</summary>
    public class MemoryFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MemoryFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:blockType")]
        public List<string> BlockType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isInjected")]
        public bool? IsInjected { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isMapped")]
        public bool? IsMapped { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isProtected")]
        public bool? IsProtected { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isVolatile")]
        public bool? IsVolatile { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:regionEndAddress")]
        public List<byte[]> RegionEndAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:regionSize")]
        public long? RegionSize { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:regionStartAddress")]
        public List<byte[]> RegionStartAddress { get; set; }
    }

    /// <summary>A message is a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https://en.wikipedia.org/wiki/Message]</summary>
    public class Message : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Message";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A message facet is a grouping of characteristics unique to a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https:</summary>
    public class MessageFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MessageFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:from")]
        public CaseUco.Uco.Observable.ObservableObject From { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:messageID")]
        public string MessageID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:messageText")]
        public string MessageText { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:messageType")]
        public string MessageType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sentTime")]
        public System.DateTime? SentTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sessionID")]
        public string SessionID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:to")]
        public List<CaseUco.Uco.Observable.ObservableObject> To { get; set; }
    }

    /// <summary>A message thread is a running commentary of electronic messages pertaining to one topic or question.</summary>
    public class MessageThread : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MessageThread";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A message thread facet is a grouping of characteristics unique to a running commentary of electronic messages pertaining to one topic or question.</summary>
    public class MessageThreadFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MessageThreadFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:messageThread")]
        public CaseUco.Uco.Types.Thread MessageThread { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:participant")]
        public List<CaseUco.Uco.Observable.ObservableObject> Participant { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:visibility")]
        public bool? Visibility { get; set; }
    }

    /// <summary>An MFT record facet is a grouping of characteristics unique to the details of a single file as managed in an NTFS (new technology filesystem) master file table (which is a collection of information ab</summary>
    public class MftRecordFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MftRecordFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:mftFileID")]
        public long? MftFileID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftFileNameAccessedTime")]
        public System.DateTime? MftFileNameAccessedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftFileNameCreatedTime")]
        public System.DateTime? MftFileNameCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftFileNameLength")]
        public long? MftFileNameLength { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftFileNameModifiedTime")]
        public System.DateTime? MftFileNameModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftFileNameRecordChangeTime")]
        public System.DateTime? MftFileNameRecordChangeTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftFlags")]
        public long? MftFlags { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftParentID")]
        public long? MftParentID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mftRecordChangeTime")]
        public System.DateTime? MftRecordChangeTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ntfsHardLinkCount")]
        public long? NtfsHardLinkCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ntfsOwnerID")]
        public string NtfsOwnerID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ntfsOwnerSID")]
        public string NtfsOwnerSID { get; set; }
    }

    /// <summary>A mime part type is a grouping of characteristics unique to a component of a multi-part email body.</summary>
    public class MimePartType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MimePartType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:body")]
        public string Body { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bodyRaw")]
        public CaseUco.Uco.Observable.ObservableObject BodyRaw { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contentDisposition")]
        public string ContentDisposition { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contentType")]
        public string ContentType { get; set; }
    }

    /// <summary>A mobile account is an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based on https://www.lexico.com/definition/mobile_d</summary>
    public class MobileAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MobileAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A mobile account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based</summary>
    public class MobileAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MobileAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:IMSI")]
        public string IMSI { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:MSISDN")]
        public string MSISDN { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:MSISDNType")]
        public string MSISDNType { get; set; }
    }

    /// <summary>A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobile_device]</summary>
    public class MobileDevice : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MobileDevice";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A mobile device facet is a grouping of characteristics unique to a portable computing device. [based on https://www.lexico.com/definition/mobile_device]</summary>
    public class MobileDeviceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MobileDeviceFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:ESN")]
        public string ESN { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:IMEI")]
        public List<string> IMEI { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bluetoothDeviceName")]
        public string BluetoothDeviceName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:clockSetting")]
        public System.DateTime? ClockSetting { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:keypadUnlockCode")]
        public string KeypadUnlockCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mockLocationsAllowed")]
        public bool? MockLocationsAllowed { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:network")]
        public string Network { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:phoneActivationTime")]
        public System.DateTime? PhoneActivationTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:storageCapacityInBytes")]
        public long? StorageCapacityInBytes { get; set; }
    }

    /// <summary>A mobile phone is a portable telephone that at least can make and receive calls over a radio frequency link while the user is moving within a telephone service area. This category encompasses all type</summary>
    public class MobilePhone : CaseUco.Uco.Observable.MobileDevice
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MobilePhone";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A mutex is a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual exclusion concurrency control policy, and with a v</summary>
    public class Mutex : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Mutex";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual excl</summary>
    public class MutexFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/MutexFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:isNamed")]
        public bool? IsNamed { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mutexName")]
        public string MutexName { get; set; }
    }

    /// <summary>An NTFS file is a New Technology File System (NTFS) file.</summary>
    public class NTFSFile : CaseUco.Uco.Observable.File
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFile";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An NTFS file facet is a grouping of characteristics unique to a file on an NTFS (new technology filesystem) file system.</summary>
    public class NTFSFileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:alternateDataStreams")]
        public List<CaseUco.Uco.Observable.AlternateDataStream> AlternateDataStreams { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:entryID")]
        public long? EntryID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sid")]
        public string Sid { get; set; }
    }

    /// <summary>An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on an NTFS (new technology filesystem) file system.</summary>
    public class NTFSFilePermissionsFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFilePermissionsFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is persisted as a filesystem object (that can be deleted like any other file), can be written to or read from </summary>
    public class NamedPipe : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NamedPipe";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network appliance is a purpose-built computer with software or firmware that is designed to provide a specific network management function.</summary>
    public class NetworkAppliance : CaseUco.Uco.Observable.Appliance
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkAppliance";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network connection is a connection (completed or attempted) across a digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.htm</summary>
    public class NetworkConnection : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnection";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network connection facet is a grouping of characteristics unique to a connection (complete or attempted) accross a digital network (a group of two or more computer systems linked together). [based o</summary>
    public class NetworkConnectionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnectionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:destinationPort")]
        public long? DestinationPort { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dst")]
        public List<CaseUco.Uco.Observable.ObservableObject> Dst { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:endTime")]
        public System.DateTime? EndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isActive")]
        public bool? IsActive { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:protocols")]
        public CaseUco.Uco.Types.ControlledDictionary Protocols { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sourcePort")]
        public long? SourcePort { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:src")]
        public List<CaseUco.Uco.Core.UcoObject> Src { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startTime")]
        public System.DateTime? StartTime { get; set; }
    }

    /// <summary>A network flow is a sequence of data transiting one or more digital network (a group or two or more computer systems linked together) connections. [based on https://www.webopedia.com/TERM/N/network.ht</summary>
    public class NetworkFlow : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlow";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network flow facet is a grouping of characteristics unique to a sequence of data transiting one or more digital network (a group of two or more computer systems linked together) connections. [based </summary>
    public class NetworkFlowFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlowFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:dstBytes")]
        public long? DstBytes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dstPackets")]
        public long? DstPackets { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dstPayload")]
        public CaseUco.Uco.Observable.ObservableObject DstPayload { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ipfix")]
        public CaseUco.Uco.Types.Dictionary Ipfix { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:srcBytes")]
        public long? SrcBytes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:srcPackets")]
        public long? SrcPackets { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:srcPayload")]
        public CaseUco.Uco.Observable.ObservableObject SrcPayload { get; set; }
    }

    /// <summary>A network interface is a software or hardware interface between two pieces of equipment or protocol layers in a computer network.</summary>
    public class NetworkInterface : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterface";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network interface facet is a grouping of characteristics unique to a software or hardware interface between two pieces of equipment or protocol layers in a computer network.</summary>
    public class NetworkInterfaceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterfaceFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:adapterName")]
        public string AdapterName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dhcpLeaseExpires")]
        public System.DateTime? DhcpLeaseExpires { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dhcpLeaseObtained")]
        public System.DateTime? DhcpLeaseObtained { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dhcpServer")]
        public List<CaseUco.Uco.Observable.ObservableObject> DhcpServer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ip")]
        public List<CaseUco.Uco.Observable.ObservableObject> Ip { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ipGateway")]
        public List<CaseUco.Uco.Observable.ObservableObject> IpGateway { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:macAddress")]
        public CaseUco.Uco.Observable.ObservableObject MacAddress { get; set; }
    }

    /// <summary>A network protocol is an established set of structured rules that determine how data is transmitted between different devices in the same network. Essentially, it allows connected devices to communica</summary>
    public class NetworkProtocol : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkProtocol";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network route is a specific path (of specific network nodes, connections and protocols) for traffic in a network or between or across multiple networks.</summary>
    public class NetworkRoute : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkRoute";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A network subnet is a logical subdivision of an IP network. [based on https://en.wikipedia.org/wiki/Subnetwork]</summary>
    public class NetworkSubnet : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSubnet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A note is a brief textual record.</summary>
    public class Note : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Note";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A note facet is a grouping of characteristics unique to a brief textual record.</summary>
    public class NoteFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/NoteFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:text")]
        public string Text { get; set; }
    }

    /// <summary>An observable is a characterizable item or action within the digital domain.</summary>
    public class Observable : CaseUco.Uco.Core.UcoObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Observable";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An observable action is a grouping of characteristics unique to something that may be done or performed within the digital domain.</summary>
    public class ObservableAction : CaseUco.Uco.Action.Action
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableAction";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An observable object is a grouping of characteristics unique to a distinct article or unit within the digital domain.</summary>
    public class ObservableObject : CaseUco.Uco.Core.Item
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:hasChanged")]
        public bool? HasChanged { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:state")]
        public string State { get; set; }
    }

    /// <summary>An observable pattern is a grouping of characteristics unique to a logical pattern composed of observable object and observable action properties.</summary>
    public class ObservablePattern : CaseUco.Uco.Observable.Observable
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ObservablePattern";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An observable relationship is a grouping of characteristics unique to an assertion of an association between two observable objects.</summary>
    public class ObservableRelationship : CaseUco.Uco.Core.Relationship
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableRelationship";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:source")]
        public new List<CaseUco.Uco.Observable.Observable> Source { get; set; }
        [global::CaseUco.JsonLdProperty("uco-core:target")]
        public new List<CaseUco.Uco.Observable.Observable> Target { get; set; }
    }

    /// <summary>An observation is a temporal perception of an observable.</summary>
    public class Observation : CaseUco.Uco.Action.Action
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Observation";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public new string Name { get; set; }
    }

    /// <summary>An online service is a particular provision mechanism of information access, distribution or manipulation over the Internet.</summary>
    public class OnlineService : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/OnlineService";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An online service facet is a grouping of characteristics unique to a particular provision mechanism of information access, distribution or manipulation over the Internet.</summary>
    public class OnlineServiceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/OnlineServiceFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:inetLocation")]
        public List<CaseUco.Uco.Observable.ObservableObject> InetLocation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:location")]
        public List<CaseUco.Uco.Location.Location> Location { get; set; }
    }

    /// <summary>An operating system is the software that manages computer hardware, software resources, and provides common services for computer programs. [based on https://en.wikipedia.org/wiki/Operating_system]</summary>
    public class OperatingSystem : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystem";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An operating system facet is a grouping of characteristics unique to the software that manages computer hardware, software resources, and provides common services for computer programs. [based on http</summary>
    public class OperatingSystemFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystemFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:advertisingID")]
        public List<string> AdvertisingID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:bitness")]
        public string Bitness { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:environmentVariables")]
        public CaseUco.Uco.Types.Dictionary EnvironmentVariables { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:installDate")]
        public System.DateTime? InstallDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isLimitAdTrackingEnabled")]
        public bool? IsLimitAdTrackingEnabled { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:manufacturer")]
        public CaseUco.Uco.Identity.Identity Manufacturer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
    }

    /// <summary>A PDF file is a Portable Document Format (PDF) file.</summary>
    public class PDFFile : CaseUco.Uco.Observable.File
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PDFFile";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A PDF file facet is a grouping of characteristics unique to a PDF (Portable Document Format) file.</summary>
    public class PDFFileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PDFFileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:documentInformationDictionary")]
        public CaseUco.Uco.Types.ControlledDictionary DocumentInformationDictionary { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isOptimized")]
        public bool? IsOptimized { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pdfCreationDate")]
        public System.DateTime? PdfCreationDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pdfId0")]
        public List<string> PdfId0 { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pdfId1")]
        public string PdfId1 { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pdfModDate")]
        public System.DateTime? PdfModDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
    }

    /// <summary>A path relation facet is a grouping of characteristics unique to the location of one object within another containing object.</summary>
    public class PathRelationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PathRelationFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:path")]
        public List<string> Path { get; set; }
    }

    /// <summary>A payment card is a physical token that is part of a payment system issued by financial institutions, such as a bank, to a customer that enables its owner (the cardholder) to access the funds in the c</summary>
    public class PaymentCard : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PaymentCard";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A phone account is an arrangement with an entity to enable and control the provision of a telephony capability or service.</summary>
    public class PhoneAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A phone account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of a telephony capability or service.</summary>
    public class PhoneAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:phoneNumber")]
        public string PhoneNumber { get; set; }
    }

    /// <summary>A pipe is a mechanism for one-way inter-process communication using message passing where data written by one process is buffered by the operating system until it is read by the next process, and this</summary>
    public class Pipe : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Pipe";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A post is message submitted to an online discussion/publishing site (forum, blog, etc.).</summary>
    public class Post : CaseUco.Uco.Observable.Message
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Post";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A process is an instance of a computer program executed on an operating system.</summary>
    public class Process : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Process";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A process facet is a grouping of characteristics unique to an instance of a computer program executed on an operating system.</summary>
    public class ProcessFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ProcessFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:arguments")]
        public List<string> Arguments { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:binary")]
        public CaseUco.Uco.Observable.ObservableObject Binary { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:creatorUser")]
        public CaseUco.Uco.Observable.ObservableObject CreatorUser { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:currentWorkingDirectory")]
        public string CurrentWorkingDirectory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:environmentVariables")]
        public CaseUco.Uco.Types.Dictionary EnvironmentVariables { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:exitStatus")]
        public long? ExitStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:exitTime")]
        public System.DateTime? ExitTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isHidden")]
        public bool? IsHidden { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:parent")]
        public CaseUco.Uco.Observable.ObservableObject Parent { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pid")]
        public long? Pid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:status")]
        public string Status { get; set; }
    }

    /// <summary>A process thread is the smallest sequence of programmed instructions that can be managed independently by a scheduler on a computer, which is typically a part of the operating system. It is a componen</summary>
    public class ProcessThread : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ProcessThread";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A profile is an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or application. [based on https://en.wikipedia.o</summary>
    public class Profile : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Profile";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or</summary>
    public class ProfileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ProfileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactAddress")]
        public CaseUco.Uco.Observable.ContactAddress ContactAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactEmail")]
        public CaseUco.Uco.Observable.ContactEmail ContactEmail { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactMessaging")]
        public CaseUco.Uco.Observable.ContactMessaging ContactMessaging { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactPhone")]
        public CaseUco.Uco.Observable.ContactPhone ContactPhone { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:contactURL")]
        public CaseUco.Uco.Observable.ContactURL ContactURL { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:displayName")]
        public string DisplayName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileAccount")]
        public CaseUco.Uco.Observable.ObservableObject ProfileAccount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileCreated")]
        public System.DateTime? ProfileCreated { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileIdentity")]
        public CaseUco.Uco.Identity.Identity ProfileIdentity { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileLanguage")]
        public List<string> ProfileLanguage { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileService")]
        public CaseUco.Uco.Observable.ObservableObject ProfileService { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileWebsite")]
        public CaseUco.Uco.Observable.ObservableObject ProfileWebsite { get; set; }
    }

    /// <summary>A properties enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic of the observable object is enumerated. An example</summary>
    public class PropertiesEnumeratedEffectFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PropertiesEnumeratedEffectFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:properties")]
        public string Properties { get; set; }
    }

    /// <summary>A properties read effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic is read from an observable object. An example of this wo</summary>
    public class PropertyReadEffectFacet : CaseUco.Uco.Observable.DefinedEffectFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/PropertyReadEffectFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:propertyName")]
        public string PropertyName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:value")]
        public string Value { get; set; }
    }

    /// <summary>A protocol converter is a device that converts from one protocol to another (e.g. SD to USB, SATA to USB, etc.</summary>
    public class ProtocolConverter : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ProtocolConverter";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A raster picture is a raster (or bitmap) image.</summary>
    public class RasterPicture : CaseUco.Uco.Observable.File
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/RasterPicture";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A raster picture facet is a grouping of characteristics unique to a raster (or bitmap) image.</summary>
    public class RasterPictureFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/RasterPictureFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:bitsPerPixel")]
        public long? BitsPerPixel { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:camera")]
        public CaseUco.Uco.Observable.ObservableObject Camera { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:imageCompressionMethod")]
        public string ImageCompressionMethod { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pictureHeight")]
        public long? PictureHeight { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pictureType")]
        public string PictureType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pictureWidth")]
        public long? PictureWidth { get; set; }
    }

    /// <summary>An observable object that was the result of a recovery operation.</summary>
    public class RecoveredObject : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObject";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>Recoverability status of name, metadata, and content.</summary>
    public class RecoveredObjectFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObjectFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contentRecoveredStatus")]
        public List<string> ContentRecoveredStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:metadataRecoveredStatus")]
        public List<string> MetadataRecoveredStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:nameRecoveredStatus")]
        public List<string> NameRecoveredStatus { get; set; }
    }

    /// <summary>A reparse point is a type of NTFS (New Technology File System) object which is an optional attribute of files and directories meant to define some sort of preprocessing before accessing the said file </summary>
    public class ReparsePoint : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ReparsePoint";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A SIM card is a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its related key, which are used to identify and authenti</summary>
    public class SIMCard : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SIMCard";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A SIM card facet is a grouping of characteristics unique to a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its relate</summary>
    public class SIMCardFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SIMCardFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:ICCID")]
        public string ICCID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:IMSI")]
        public string IMSI { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:PIN")]
        public string PIN { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:PUK")]
        public string PUK { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:SIMForm")]
        public string SIMForm { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:SIMType")]
        public string SIMType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:carrier")]
        public CaseUco.Uco.Identity.Identity Carrier { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:storageCapacityInBytes")]
        public long? StorageCapacityInBytes { get; set; }
    }

    /// <summary>A SIP address is an identifier for Session Initiation Protocol (SIP) communication.</summary>
    public class SIPAddress : CaseUco.Uco.Observable.DigitalAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SIPAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP) standards conformant identifier assigned to a user to enable routing and management of SIP standards </summary>
    public class SIPAddressFacet : CaseUco.Uco.Observable.DigitalAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SIPAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An SMS message is a message conformant to the short message service (SMS) communication protocol standards.</summary>
    public class SMSMessage : CaseUco.Uco.Observable.Message
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SMSMessage";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A SMS message facet is a grouping of characteristics unique to a message conformant to the short message service (SMS) communication protocol standards.</summary>
    public class SMSMessageFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SMSMessageFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:isRead")]
        public bool? IsRead { get; set; }
    }

    /// <summary>An SQLite blob is a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]</summary>
    public class SQLiteBlob : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlob";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An SQLite blob facet is a grouping of characteristics unique to a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]</summary>
    public class SQLiteBlobFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlobFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:columnName")]
        public string ColumnName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:rowCondition")]
        public string RowCondition { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:rowIndex")]
        public List<ulong> RowIndex { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:tableName")]
        public string TableName { get; set; }
    }

    /// <summary>A security appliance is a purpose-built computer with software or firmware that is designed to provide a specific security function to protect computer networks.</summary>
    public class SecurityAppliance : CaseUco.Uco.Observable.Appliance
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SecurityAppliance";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A semaphore is a variable or abstract data type used to control access to a common resource by multiple processes and avoid critical section problems in a concurrent system such as a multitasking oper</summary>
    public class Semaphore : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Semaphore";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A send control code effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a control code, or other control-oriented communication signal, is sent</summary>
    public class SendControlCodeEffectFacet : CaseUco.Uco.Observable.DefinedEffectFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SendControlCodeEffectFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:controlCode")]
        public string ControlCode { get; set; }
    }

    /// <summary>A server is a server rack-mount based computer, minicomputer, supercomputer, etc.</summary>
    public class Server : CaseUco.Uco.Observable.Computer
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Server";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A shop listing is a listing of offered products on an online marketplace/shop.</summary>
    public class ShopListing : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ShopListing";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-based networks or via smartphone</summary>
    public class SmartDevice : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SmartDevice";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A smartphone is a portable device that combines mobile telephone and computing functions into one unit.  Examples include iPhone, Samsung Galaxy, Huawei, Blackberry. (Inferred by model and OperatingSy</summary>
    public class SmartPhone : CaseUco.Uco.Observable.Computer
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SmartPhone";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A snapshot is a file system object representing a snapshot of the contents of a part of a file system at a point in time.</summary>
    public class Snapshot : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Snapshot";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A socket is a special file used for inter-process communication, which enables communication between two processes. In addition to sending data, processes can send file descriptors across a Unix domai</summary>
    public class Socket : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Socket";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A socket address (combining and IP address and a port number) is a composite identifier for a network socket endpoint supporting internet protocol communications.</summary>
    public class SocketAddress : CaseUco.Uco.Observable.Address
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SocketAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>Software is a definitely scoped instance of a collection of data or computer instructions that tell the computer how to work. [based on https://en.wikipedia.org/wiki/Software]</summary>
    public class Software : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Software";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A software facet is a grouping of characteristics unique to a software program (a definitively scoped instance of a collection of data or computer instructions that tell the computer how to work). [ba</summary>
    public class SoftwareFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SoftwareFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:cpeid")]
        public string Cpeid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:language")]
        public string Language { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:manufacturer")]
        public CaseUco.Uco.Identity.Identity Manufacturer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:swid")]
        public string Swid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
    }

    /// <summary>A state change effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a state of the observable object is changed.</summary>
    public class StateChangeEffectFacet : CaseUco.Uco.Observable.DefinedEffectFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/StateChangeEffectFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:newObject")]
        public CaseUco.Uco.Observable.ObservableObject NewObject { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:oldObject")]
        public CaseUco.Uco.Observable.ObservableObject OldObject { get; set; }
    }

    /// <summary>A storage medium is any digital storage device that applies electromagnetic or optical surfaces, or depends solely on electronic circuits as solid state storage, for storing digital data. Examples inc</summary>
    public class StorageMedium : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/StorageMedium";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a piece of equipment or a mechanism designed to serve a special purpose or perform a special function.</summary>
    public class StorageMediumFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/StorageMediumFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:totalStorageCapacityInBytes")]
        public long? TotalStorageCapacityInBytes { get; set; }
    }

    /// <summary>A symbolic link is a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname resolution. [based on https://en.wikipedia.org/wi</summary>
    public class SymbolicLink : CaseUco.Uco.Observable.FileSystemObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLink";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A symbolic link facet is a grouping of characteristics unique to a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname res</summary>
    public class SymbolicLinkFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLinkFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:targetFile")]
        public CaseUco.Uco.Observable.ObservableObject TargetFile { get; set; }
    }

    /// <summary>A TCP connection is a network connection that is conformant to the Transfer </summary>
    public class TCPConnection : CaseUco.Uco.Observable.NetworkConnection
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TCPConnection";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A TCP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Transmission Control Protocl (TCP) standard.</summary>
    public class TCPConnectionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TCPConnectionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:destinationFlags")]
        public List<byte[]> DestinationFlags { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sourceFlags")]
        public List<byte[]> SourceFlags { get; set; }
    }

    /// <summary>A database table field and its associated value contained within a relational database.</summary>
    public class TableField : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TableField";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A database record facet contains properties associated with a specific table record value from a database.</summary>
    public class TableFieldFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TableFieldFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:recordFieldIsNull")]
        public bool? RecordFieldIsNull { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:recordFieldName")]
        public string RecordFieldName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:recordFieldValue")]
        public object RecordFieldValue { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:recordRowID")]
        public object RecordRowID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:tableName")]
        public string TableName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:tableSchema")]
        public string TableSchema { get; set; }
    }

    /// <summary>A tablet is a mobile computer that is primarily operated by touching the screen. (Devices categorized by their manufacturer as a Tablet)</summary>
    public class Tablet : CaseUco.Uco.Observable.Computer
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Tablet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A task action type is a grouping of characteristics for a scheduled action to be completed.</summary>
    public class TaskActionType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TaskActionType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:actionID")]
        public string ActionID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:actionType")]
        public List<string> ActionType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:iComHandlerAction")]
        public CaseUco.Uco.Observable.IComHandlerActionType IComHandlerAction { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:iEmailAction")]
        public CaseUco.Uco.Observable.ObservableObject IEmailAction { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:iExecAction")]
        public CaseUco.Uco.Observable.IExecActionType IExecAction { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:iShowMessageAction")]
        public CaseUco.Uco.Observable.IShowMessageActionType IShowMessageAction { get; set; }
    }

    /// <summary>A trigger type is a grouping of characterizes unique to a set of criteria that, when met, starts the execution of a task within a Windows operating system. [based on https://docs.microsoft.com/en-us/w</summary>
    public class TriggerType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TriggerType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:isEnabled")]
        public bool? IsEnabled { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerBeginTime")]
        public System.DateTime? TriggerBeginTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerDelay")]
        public string TriggerDelay { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerEndTime")]
        public System.DateTime? TriggerEndTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerFrequency")]
        public List<string> TriggerFrequency { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerMaxRunTime")]
        public string TriggerMaxRunTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerSessionChangeType")]
        public string TriggerSessionChangeType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerType")]
        public List<string> TriggerTypeValue { get; set; }
    }

    /// <summary>A tweet is message submitted by a Twitter user account to the Twitter microblogging platform.</summary>
    public class Tweet : CaseUco.Uco.Observable.Message
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Tweet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A twitter profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single Twitter user account. [based on https://e</summary>
    public class TwitterProfileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/TwitterProfileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:favoritesCount")]
        public ulong? FavoritesCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:followersCount")]
        public ulong? FollowersCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:friendsCount")]
        public ulong? FriendsCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:listedCount")]
        public long? ListedCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileBackgroundHash")]
        public List<CaseUco.Uco.Types.Hash> ProfileBackgroundHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileBackgroundLocation")]
        public CaseUco.Uco.Observable.ObservableObject ProfileBackgroundLocation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileBannerHash")]
        public List<CaseUco.Uco.Types.Hash> ProfileBannerHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileBannerLocation")]
        public CaseUco.Uco.Observable.ObservableObject ProfileBannerLocation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileImageHash")]
        public List<CaseUco.Uco.Types.Hash> ProfileImageHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileImageLocation")]
        public CaseUco.Uco.Observable.ObservableObject ProfileImageLocation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileIsProtected")]
        public bool? ProfileIsProtected { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:profileIsVerified")]
        public bool? ProfileIsVerified { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:statusesCount")]
        public ulong? StatusesCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:twitterHandle")]
        public string TwitterHandle { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:twitterId")]
        public string TwitterId { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:userLocationString")]
        public string UserLocationString { get; set; }
    }

    /// <summary>A UNIX account is an account on a UNIX operating system.</summary>
    public class UNIXAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A UNIX account facet is a grouping of characteristics unique to an account on a UNIX operating system.</summary>
    public class UNIXAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:gid")]
        public long? Gid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:shell")]
        public string Shell { get; set; }
    }

    /// <summary>A UNIX file is a file pertaining to the UNIX operating system.</summary>
    public class UNIXFile : CaseUco.Uco.Observable.File
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXFile";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a UNIX file system.</summary>
    public class UNIXFilePermissionsFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXFilePermissionsFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A UNIX process is an instance of a computer program executed on a UNIX operating system.</summary>
    public class UNIXProcess : CaseUco.Uco.Observable.Process
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcess";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A UNIX process facet is a grouping of characteristics unique to an instance of a computer program executed on a UNIX operating system.</summary>
    public class UNIXProcessFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcessFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:openFileDescriptor")]
        public List<long> OpenFileDescriptor { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ruid")]
        public List<ulong> Ruid { get; set; }
    }

    /// <summary>A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single UNIX file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]</summary>
    public class UNIXVolumeFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXVolumeFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:mountPoint")]
        public string MountPoint { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:options")]
        public string Options { get; set; }
    }

    /// <summary>A URL is a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource.</summary>
    public class URL : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URL";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A URL facet is a grouping of characteristics unique to a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource.</summary>
    public class URLFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URLFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:fragment")]
        public string Fragment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:fullValue")]
        public string FullValue { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:host")]
        public CaseUco.Uco.Observable.ObservableObject Host { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:password")]
        public string Password { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:path")]
        public string Path { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:port")]
        public long? Port { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:query")]
        public string Query { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:scheme")]
        public string Scheme { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:userName")]
        public string UserName { get; set; }
    }

    /// <summary>A URL history characterizes the stored URL history for a particular web browser</summary>
    public class URLHistory : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistory";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A URL history entry is a grouping of characteristics unique to the properties of a single URL history entry for a particular browser.</summary>
    public class URLHistoryEntry : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryEntry";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:browserUserProfile")]
        public string BrowserUserProfile { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:expirationTime")]
        public System.DateTime? ExpirationTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:firstVisit")]
        public System.DateTime? FirstVisit { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:hostname")]
        public string Hostname { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:keywordSearchTerm")]
        public List<string> KeywordSearchTerm { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lastVisit")]
        public System.DateTime? LastVisit { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:manuallyEnteredCount")]
        public ulong? ManuallyEnteredCount { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pageTitle")]
        public string PageTitle { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:referrerUrl")]
        public List<CaseUco.Uco.Observable.ObservableObject> ReferrerUrl { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:url")]
        public CaseUco.Uco.Observable.ObservableObject Url { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:visitCount")]
        public long? VisitCount { get; set; }
    }

    /// <summary>A URL history facet is a grouping of characteristics unique to the stored URL history for a particular web browser</summary>
    public class URLHistoryFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:browserInformation")]
        public CaseUco.Uco.Observable.ObservableObject BrowserInformation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:urlHistoryEntry")]
        public List<CaseUco.Uco.Observable.URLHistoryEntry> UrlHistoryEntry { get; set; }
    }

    /// <summary>A URL visit characterizes the properties of a visit of a URL within a particular browser.</summary>
    public class URLVisit : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URLVisit";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A URL visit facet is a grouping of characteristics unique to the properties of a visit of a URL within a particular browser.</summary>
    public class URLVisitFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/URLVisitFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:browserInformation")]
        public CaseUco.Uco.Observable.ObservableObject BrowserInformation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:fromURLVisit")]
        public CaseUco.Uco.Observable.ObservableObject FromURLVisit { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:url")]
        public CaseUco.Uco.Observable.ObservableObject Url { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:urlTransitionType")]
        public List<string> UrlTransitionType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:visitDuration")]
        public System.TimeSpan? VisitDuration { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:visitTime")]
        public System.DateTime? VisitTime { get; set; }
    }

    /// <summary>A user account is an account controlling a user's access to a network, system or platform.</summary>
    public class UserAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UserAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A user account facet is a grouping of characteristics unique to an account controlling a user's access to a network, system, or platform.</summary>
    public class UserAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UserAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:canEscalatePrivs")]
        public bool? CanEscalatePrivs { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:homeDirectory")]
        public string HomeDirectory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isPrivileged")]
        public bool? IsPrivileged { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:isServiceAccount")]
        public bool? IsServiceAccount { get; set; }
    }

    /// <summary>A user session is a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user. [based on https://en.wikipedia.org/wiki/Sessi</summary>
    public class UserSession : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UserSession";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A user session facet is a grouping of characteristics unique to a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user.</summary>
    public class UserSessionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/UserSessionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:effectiveGroup")]
        public string EffectiveGroup { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:effectiveGroupID")]
        public string EffectiveGroupID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:effectiveUser")]
        public CaseUco.Uco.Observable.ObservableObject EffectiveUser { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:loginTime")]
        public System.DateTime? LoginTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:logoutTime")]
        public System.DateTime? LogoutTime { get; set; }
    }

    /// <summary>A values enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a value of the observable object is enumerated. An example of this woul</summary>
    public class ValuesEnumeratedEffectFacet : CaseUco.Uco.Observable.DefinedEffectFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/ValuesEnumeratedEffectFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:values")]
        public string Values { get; set; }
    }

    /// <summary>A volume is a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]</summary>
    public class Volume : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Volume";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]</summary>
    public class VolumeFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/VolumeFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:sectorSize")]
        public long? SectorSize { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:volumeID")]
        public string VolumeID { get; set; }
    }

    /// <summary>A wearable device is an electronic device that is designed to be worn on a person's body.</summary>
    public class WearableDevice : CaseUco.Uco.Observable.SmartDevice
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WearableDevice";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A web page is a specific collection of information provided by a website and displayed to a user in a web browser. A website typically consists of many web pages linked together in a coherent fashion.</summary>
    public class WebPage : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WebPage";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>WhoIs is a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]</summary>
    public class WhoIs : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WhoIs";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A whois facet is a grouping of characteristics unique to a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]</summary>
    public class WhoIsFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WhoIsFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:creationDate")]
        public System.DateTime? CreationDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dnssec")]
        public string Dnssec { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:domainID")]
        public string DomainID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:domainName")]
        public CaseUco.Uco.Observable.ObservableObject DomainName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:expirationDate")]
        public System.DateTime? ExpirationDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ipAddress")]
        public CaseUco.Uco.Observable.ObservableObject IpAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lookupDate")]
        public System.DateTime? LookupDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:nameServer")]
        public List<CaseUco.Uco.Observable.ObservableObject> NameServer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:regionalInternetRegistry")]
        public List<string> RegionalInternetRegistry { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registrantContactInfo")]
        public CaseUco.Uco.Observable.ObservableObject RegistrantContactInfo { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registrantIDs")]
        public List<string> RegistrantIDs { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registrarInfo")]
        public CaseUco.Uco.Observable.WhoisRegistrarInfoType RegistrarInfo { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:remarks")]
        public string Remarks { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:serverName")]
        public CaseUco.Uco.Observable.ObservableObject ServerName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sponsoringRegistrar")]
        public string SponsoringRegistrar { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:status")]
        public List<string> Status { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:updatedDate")]
        public System.DateTime? UpdatedDate { get; set; }
    }

    /// <summary>A Whois contact type is a grouping of characteristics unique to contact-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wiki</summary>
    public class WhoisContactFacet : CaseUco.Uco.Observable.ContactFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WhoisContactFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:whoisContactType")]
        public List<string> WhoisContactType { get; set; }
    }

    /// <summary>A Whois registrar info type is a grouping of characteristics unique to registrar-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https:</summary>
    public class WhoisRegistrarInfoType : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WhoisRegistrarInfoType";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:contactPhoneNumber")]
        public CaseUco.Uco.Observable.ObservableObject ContactPhoneNumber { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:emailAddress")]
        public CaseUco.Uco.Observable.ObservableObject EmailAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:geolocationAddress")]
        public CaseUco.Uco.Location.Location GeolocationAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:referralURL")]
        public CaseUco.Uco.Observable.ObservableObject ReferralURL { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registrarGUID")]
        public string RegistrarGUID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registrarID")]
        public string RegistrarID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registrarName")]
        public string RegistrarName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:whoisServer")]
        public CaseUco.Uco.Observable.ObservableObject WhoisServer { get; set; }
    }

    /// <summary>A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a device network interface to enable routing and management of IEEE 802.11 standards-conformant communicatio</summary>
    public class WifiAddress : CaseUco.Uco.Observable.MACAddress
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WifiAddress";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) standards conformant identifier assigned to a device network interface to enable routing and management of</summary>
    public class WifiAddressFacet : CaseUco.Uco.Observable.MACAddressFacet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WifiAddressFacet";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A wiki is an online hypertext publication collaboratively edited and managed by its own audience directly using a web browser. A typical wiki contains multiple pages/articles for the subjects or scope</summary>
    public class Wiki : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/Wiki";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A wiki article is one or more pages in a wiki focused on characterizing a particular topic.</summary>
    public class WikiArticle : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WikiArticle";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows account is a user account on a Windows operating system.</summary>
    public class WindowsAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows account facet is a grouping of characteristics unique to a user account on a Windows operating system.</summary>
    public class WindowsAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:groups")]
        public List<string> Groups { get; set; }
    }

    /// <summary>A Windows Active Directory account is an account managed by directory-based identity-related services of a Windows operating system.</summary>
    public class WindowsActiveDirectoryAccount : CaseUco.Uco.Observable.DigitalAccount
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccount";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows Active Directory account facet is a grouping of characteristics unique to an account managed by directory-based identity-related services of a Windows operating system.</summary>
    public class WindowsActiveDirectoryAccountFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccountFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:activeDirectoryGroups")]
        public List<string> ActiveDirectoryGroups { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:objectGUID")]
        public string ObjectGUID { get; set; }
    }

    /// <summary>A Windows computer specification is the hardware ans software of a programmable electronic device that can store, retrieve, and process data running a Microsoft Windows operating system. [based on mer</summary>
    public class WindowsComputerSpecification : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecification";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows computer specification facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data running a Mic</summary>
    public class WindowsComputerSpecificationFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecificationFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:domain")]
        public List<string> Domain { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:globalFlagList")]
        public List<CaseUco.Uco.Observable.GlobalFlagType> GlobalFlagList { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lastShutdownDate")]
        public System.DateTime? LastShutdownDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:msProductID")]
        public string MsProductID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:msProductName")]
        public string MsProductName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:netBIOSName")]
        public string NetBIOSName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:osInstallDate")]
        public System.DateTime? OsInstallDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:osLastUpgradeDate")]
        public System.DateTime? OsLastUpgradeDate { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registeredOrganization")]
        public CaseUco.Uco.Identity.Identity RegisteredOrganization { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registeredOwner")]
        public CaseUco.Uco.Identity.Identity RegisteredOwner { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:windowsDirectory")]
        public CaseUco.Uco.Observable.ObservableObject WindowsDirectory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:windowsSystemDirectory")]
        public CaseUco.Uco.Observable.ObservableObject WindowsSystemDirectory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:windowsTempDirectory")]
        public CaseUco.Uco.Observable.ObservableObject WindowsTempDirectory { get; set; }
    }

    /// <summary>A Windows critical section is a Windows object that provides synchronization similar to that provided by a mutex object, except that a critical section can be used only by the threads of a single proc</summary>
    public class WindowsCriticalSection : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsCriticalSection";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows event is a notification record of an occurance of interest (system, security, application, etc.) on a Windows operating system.</summary>
    public class WindowsEvent : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsEvent";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows file mapping is the association of a file's contents with a portion of the virtual address space of a process within a Windows operating system. The system creates a file mapping object (als</summary>
    public class WindowsFilemapping : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsFilemapping";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows handle is an abstract reference to a resource within the Windows operating system, such as a window, memory, an open file or a pipe. It is the mechanism by which applications interact with s</summary>
    public class WindowsHandle : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsHandle";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows hook is a mechanism by which an application can intercept events, such as messages, mouse actions, and keystrokes within the Windows operating system. A function that intercepts a particular</summary>
    public class WindowsHook : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsHook";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard file functions. The data in a mailslot message can be in any form, but cannot be larger than 424 bytes </summary>
    public class WindowsMailslot : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsMailslot";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows network share is a Windows computer resource made available from one host to other hosts on a computer network. It is a device or piece of information on a computer that can be remotely acce</summary>
    public class WindowsNetworkShare : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsNetworkShare";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows PE binary file is a Windows portable executable (PE) file.</summary>
    public class WindowsPEBinaryFile : CaseUco.Uco.Observable.File
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFile";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable executable (PE) file.</summary>
    public class WindowsPEBinaryFileFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFileFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:characteristics")]
        public List<ushort> Characteristics { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:fileHeaderHashes")]
        public List<CaseUco.Uco.Types.Hash> FileHeaderHashes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:impHash")]
        public string ImpHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:machine")]
        public List<string> Machine { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:numberOfSections")]
        public long? NumberOfSections { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:numberOfSymbols")]
        public long? NumberOfSymbols { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:optionalHeader")]
        public CaseUco.Uco.Observable.WindowsPEOptionalHeader OptionalHeader { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:peType")]
        public string PeType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:pointerToSymbolTable")]
        public List<byte[]> PointerToSymbolTable { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sections")]
        public List<CaseUco.Uco.Observable.WindowsPESection> Sections { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfOptionalHeader")]
        public long? SizeOfOptionalHeader { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:timeDateStamp")]
        public System.DateTime? TimeDateStamp { get; set; }
    }

    /// <summary>A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the overall nature and structu</summary>
    public class WindowsPEFileHeader : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEFileHeader";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:timeDateStamp")]
        public System.DateTime? TimeDateStamp { get; set; }
    }

    /// <summary>A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the executable co</summary>
    public class WindowsPEOptionalHeader : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEOptionalHeader";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:addressOfEntryPoint")]
        public List<uint> AddressOfEntryPoint { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:baseOfCode")]
        public List<uint> BaseOfCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:checksum")]
        public List<uint> Checksum { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dllCharacteristics")]
        public List<ushort> DllCharacteristics { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:fileAlignment")]
        public List<uint> FileAlignment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:imageBase")]
        public List<uint> ImageBase { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:loaderFlags")]
        public List<uint> LoaderFlags { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:magic")]
        public List<ushort> Magic { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:majorImageVersion")]
        public List<ushort> MajorImageVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:majorLinkerVersion")]
        public List<sbyte> MajorLinkerVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:majorOSVersion")]
        public List<ushort> MajorOSVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:majorSubsystemVersion")]
        public List<ushort> MajorSubsystemVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:minorImageVersion")]
        public List<ushort> MinorImageVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:minorLinkerVersion")]
        public List<sbyte> MinorLinkerVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:minorOSVersion")]
        public List<ushort> MinorOSVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:minorSubsystemVersion")]
        public List<ushort> MinorSubsystemVersion { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:numberOfRVAAndSizes")]
        public List<uint> NumberOfRVAAndSizes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sectionAlignment")]
        public List<uint> SectionAlignment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfCode")]
        public List<uint> SizeOfCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfHeaders")]
        public List<uint> SizeOfHeaders { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfHeapCommit")]
        public List<uint> SizeOfHeapCommit { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfHeapReserve")]
        public List<uint> SizeOfHeapReserve { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfImage")]
        public List<uint> SizeOfImage { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfInitializedData")]
        public List<uint> SizeOfInitializedData { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfStackCommit")]
        public List<uint> SizeOfStackCommit { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfStackReserve")]
        public List<uint> SizeOfStackReserve { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:sizeOfUninitializedData")]
        public List<uint> SizeOfUninitializedData { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subsystem")]
        public List<ushort> Subsystem { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:win32VersionValue")]
        public List<uint> Win32VersionValue { get; set; }
    }

    /// <summary>A Windows PE section is a grouping of characteristics unique to a specific default or custom-defined region of a Windows PE (Portable Executable) file, consisting of an individual portion of the actua</summary>
    public class WindowsPESection : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPESection";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:entropy")]
        public decimal? Entropy { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:hashes")]
        public List<CaseUco.Uco.Types.Hash> Hashes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:size")]
        public long? Size { get; set; }
    }

    /// <summary>The Windows prefetch contains entries in a Windows prefetch file (used to speed up application startup starting with Windows XP).</summary>
    public class WindowsPrefetch : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetch";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows prefetch facet is a grouping of characteristics unique to entries in the Windows prefetch file (used to speed up application startup starting with Windows XP).</summary>
    public class WindowsPrefetchFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetchFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:accessedDirectory")]
        public List<CaseUco.Uco.Observable.ObservableObject> AccessedDirectory { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:accessedFile")]
        public List<CaseUco.Uco.Observable.ObservableObject> AccessedFile { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:applicationFileName")]
        public string ApplicationFileName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:firstRun")]
        public System.DateTime? FirstRun { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:lastRun")]
        public System.DateTime? LastRun { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:prefetchHash")]
        public string PrefetchHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:timesExecuted")]
        public long? TimesExecuted { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:volume")]
        public CaseUco.Uco.Observable.ObservableObject Volume { get; set; }
    }

    /// <summary>A Windows process is a program running on a Windows operating system.</summary>
    public class WindowsProcess : CaseUco.Uco.Observable.Process
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcess";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows process facet is a grouping of characteristics unique to a program running on a Windows operating system.</summary>
    public class WindowsProcessFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcessFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:aslrEnabled")]
        public bool? AslrEnabled { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:depEnabled")]
        public bool? DepEnabled { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ownerSID")]
        public string OwnerSID { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:priority")]
        public string Priority { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startupInfo")]
        public CaseUco.Uco.Types.Dictionary StartupInfo { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:windowTitle")]
        public string WindowTitle { get; set; }
    }

    /// <summary>The Windows registry hive is a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating s</summary>
    public class WindowsRegistryHive : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHive";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows registry hive facet is a grouping of characteristics unique to a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level se</summary>
    public class WindowsRegistryHiveFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHiveFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:hiveType")]
        public string HiveType { get; set; }
    }

    /// <summary>A Windows registry key is a particular key within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to</summary>
    public class WindowsRegistryKey : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKey";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows registry key facet is a grouping of characteristics unique to a particular key within a Windows registry (A hierarchical database that stores low-level settings for the Microsoft Windows ope</summary>
    public class WindowsRegistryKeyFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKeyFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:creator")]
        public CaseUco.Uco.Observable.ObservableObject Creator { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:key")]
        public string Key { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:modifiedTime")]
        public System.DateTime? ModifiedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:numberOfSubkeys")]
        public long? NumberOfSubkeys { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:registryValues")]
        public List<CaseUco.Uco.Observable.WindowsRegistryValue> RegistryValues { get; set; }
    }

    /// <summary>A Windows registry value is a grouping of characteristics unique to a particular value within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows opera</summary>
    public class WindowsRegistryValue : CaseUco.Uco.Core.UcoInherentCharacterizationThing
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryValue";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-core:name")]
        public string Name { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:data")]
        public string Data { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:dataType")]
        public string DataType { get; set; }
    }

    /// <summary>A Windows service is a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UNIX daemon runs on UNIX). [based on https://en.</summary>
    public class WindowsService : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsService";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows service facet is a grouping of characteristics unique to a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UN</summary>
    public class WindowsServiceFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:descriptions")]
        public List<string> Descriptions { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:displayName")]
        public string DisplayName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:groupName")]
        public string GroupName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:serviceName")]
        public string ServiceName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:serviceStatus")]
        public string ServiceStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:serviceType")]
        public string ServiceType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startCommandLine")]
        public string StartCommandLine { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startType")]
        public string StartType { get; set; }
    }

    /// <summary>A Windows system restore is a capture of a Windows computer's state (including system files, installed applications, Windows Registry, and system settings) at a particular point in time such that the </summary>
    public class WindowsSystemRestore : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsSystemRestore";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows task is a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler. [based on http://msdn.microsoft.com/en-us/library/windows/desktop/aa381311(v=vs.85</summary>
    public class WindowsTask : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTask";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler). [based on http://ms</summary>
    public class WindowsTaskFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTaskFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:account")]
        public CaseUco.Uco.Observable.ObservableObject Account { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:accountLogonType")]
        public string AccountLogonType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:accountRunLevel")]
        public string AccountRunLevel { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:actionList")]
        public List<CaseUco.Uco.Observable.TaskActionType> ActionList { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:application")]
        public CaseUco.Uco.Observable.ObservableObject Application { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:exitCode")]
        public long? ExitCode { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:flags")]
        public List<string> Flags { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:imageName")]
        public string ImageName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:maxRunTime")]
        public long? MaxRunTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:mostRecentRunTime")]
        public System.DateTime? MostRecentRunTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:nextRunTime")]
        public System.DateTime? NextRunTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:parameters")]
        public string Parameters { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:priority")]
        public List<object> Priority { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:status")]
        public List<string> Status { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:taskComment")]
        public string TaskComment { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:taskCreator")]
        public string TaskCreator { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:triggerList")]
        public List<CaseUco.Uco.Observable.TriggerType> TriggerList { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:workItemData")]
        public CaseUco.Uco.Observable.ObservableObject WorkItemData { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:workingDirectory")]
        public CaseUco.Uco.Observable.ObservableObject WorkingDirectory { get; set; }
    }

    /// <summary>A Windows thread is a single thread of execution within a Windows process.</summary>
    public class WindowsThread : CaseUco.Uco.Observable.ProcessThread
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThread";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A Windows thread facet is a grouping os characteristics unique to a single thread of execution within a Windows process.</summary>
    public class WindowsThreadFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThreadFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:context")]
        public string Context { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:creationFlags")]
        public List<uint> CreationFlags { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:creationTime")]
        public System.DateTime? CreationTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:observableCreatedTime")]
        public System.DateTime? ObservableCreatedTime { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:parameterAddress")]
        public List<byte[]> ParameterAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:priority")]
        public long? Priority { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:runningStatus")]
        public string RunningStatus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:securityAttributes")]
        public string SecurityAttributes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:stackSize")]
        public List<ulong> StackSize { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:startAddress")]
        public List<byte[]> StartAddress { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:threadID")]
        public List<ulong> ThreadID { get; set; }
    }

    /// <summary>A Windows volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single Windows file system. [based on https://en.wikipedia.org/wiki/Volume_(computing</summary>
    public class WindowsVolumeFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsVolumeFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:driveLetter")]
        public string DriveLetter { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:driveType")]
        public List<string> DriveType { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:windowsVolumeAttributes")]
        public List<string> WindowsVolumeAttributes { get; set; }
    }

    /// <summary>A Windows waitable timer is a synchronization object within the Windows operating system whose state is set to signaled when a specified due time arrives. There are two types of waitable timers that c</summary>
    public class WindowsWaitableTime : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsWaitableTime";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A wireless network connection is a connection (completed or attempted) across an IEEE 802.11 standards-confromant digital network (a group of two or more computer systems linked together). [based on h</summary>
    public class WirelessNetworkConnection : CaseUco.Uco.Observable.NetworkConnection
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnection";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A wireless network connection facet is a grouping of characteristics unique to a connection (completed or attempted) across an IEEE 802.11 standards-conformant digital network (a group of two or more </summary>
    public class WirelessNetworkConnectionFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnectionFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:baseStation")]
        public string BaseStation { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:password")]
        public string Password { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:ssid")]
        public string Ssid { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:wirelessNetworkSecurityMode")]
        public List<string> WirelessNetworkSecurityMode { get; set; }
    }

    /// <summary>A write blocker is a device that allows read-only access to storage mediums in order to preserve the integrity of the data being analyzed. Examples include Tableau, Cellibrite, Talon, etc.</summary>
    public class WriteBlocker : CaseUco.Uco.Observable.Device
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/WriteBlocker";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A X.509 certificate is a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard.</summary>
    public class X509Certificate : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/X509Certificate";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>A X.509 certificate facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard. </summary>
    public class X509CertificateFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/X509CertificateFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:isSelfSigned")]
        public bool? IsSelfSigned { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:issuer")]
        public string Issuer { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:issuerHash")]
        public CaseUco.Uco.Types.Hash IssuerHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:serialNumber")]
        public string SerialNumber { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:signature")]
        public string Signature { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:signatureAlgorithm")]
        public string SignatureAlgorithm { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subject")]
        public string Subject { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectHash")]
        public CaseUco.Uco.Types.Hash SubjectHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectPublicKeyAlgorithm")]
        public string SubjectPublicKeyAlgorithm { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectPublicKeyExponent")]
        public long? SubjectPublicKeyExponent { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectPublicKeyModulus")]
        public string SubjectPublicKeyModulus { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:thumbprintHash")]
        public CaseUco.Uco.Types.Hash ThumbprintHash { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:validityNotAfter")]
        public System.DateTime? ValidityNotAfter { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:validityNotBefore")]
        public System.DateTime? ValidityNotBefore { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:version")]
        public string Version { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:x509v3extensions")]
        public CaseUco.Uco.Observable.X509V3ExtensionsFacet X509v3extensions { get; set; }
    }

    /// <summary>An X.509 v3 certificate is a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard. </summary>
    public class X509V3Certificate : CaseUco.Uco.Observable.ObservableObject
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/X509V3Certificate";
        public new const string NamespacePrefix = "uco-observable";
    }

    /// <summary>An X.509 v3 certificate extensions facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard.</summary>
    public class X509V3ExtensionsFacet : CaseUco.Uco.Core.Facet
    {
        public new const string ClassIri = "https://ontology.unifiedcyberontology.org/uco/observable/X509V3ExtensionsFacet";
        public new const string NamespacePrefix = "uco-observable";
        [global::CaseUco.JsonLdProperty("uco-observable:authorityKeyIdentifier")]
        public string AuthorityKeyIdentifier { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:basicConstraints")]
        public string BasicConstraints { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:certificatePolicies")]
        public string CertificatePolicies { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:crlDistributionPoints")]
        public string CrlDistributionPoints { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:extendedKeyUsage")]
        public string ExtendedKeyUsage { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:inhibitAnyPolicy")]
        public string InhibitAnyPolicy { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:issuerAlternativeName")]
        public string IssuerAlternativeName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:keyUsage")]
        public string KeyUsage { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:nameConstraints")]
        public string NameConstraints { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:policyConstraints")]
        public string PolicyConstraints { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:policyMappings")]
        public string PolicyMappings { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:privateKeyUsagePeriodNotAfter")]
        public System.DateTime? PrivateKeyUsagePeriodNotAfter { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:privateKeyUsagePeriodNotBefore")]
        public System.DateTime? PrivateKeyUsagePeriodNotBefore { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectAlternativeName")]
        public string SubjectAlternativeName { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectDirectoryAttributes")]
        public string SubjectDirectoryAttributes { get; set; }
        [global::CaseUco.JsonLdProperty("uco-observable:subjectKeyIdentifier")]
        public string SubjectKeyIdentifier { get; set; }
    }

}