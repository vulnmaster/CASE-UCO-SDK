# CASE/UCO Domain Mapping Guide

This guide maps common digital forensics, cyber-investigation, and cyber-observable concepts to the right CASE/UCO classes. If you know what kind of data you have but don't know which CASE/UCO class to use, start here.

For the complete class reference with all properties, see [ONTOLOGY_REFERENCE.md](../ONTOLOGY_REFERENCE.md).

## Contents

- [Files and Filesystem](#files-and-filesystem)
- [Network Activity](#network-activity)
- [Devices and Hardware](#devices-and-hardware)
- [Applications and Software](#applications-and-software)
- [User Accounts and Identity](#user-accounts-and-identity)
- [Email and Messaging](#email-and-messaging)
- [Mobile Forensics](#mobile-forensics)
- [Actions and Events](#actions-and-events)
- [Investigation Metadata](#investigation-metadata)
- [Tool Information](#tool-information)
- [Time and Temporal Data](#time-and-temporal-data)
- [Marking and Access Control](#marking-and-access-control)
- [Extension Ontologies](#extension-ontologies)
- [Tips for Finding the Right Class](#tips-for-finding-the-right-class)

## Files and Filesystem

Classes for representing files, directories, file systems, and their metadata. Use these when your tool extracts or analyzes file-level artifacts.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **AlternateDataStream** | uco.observable | Class | An alternate data stream is data content stored within an NTFS file that is independent of the st... |
| **AlternateDataStreamFacet** | uco.observable | Facet | An alternate data stream facet is a grouping of characteristics unique to data content stored wit... |
| **ArchiveFile** | uco.observable | Class | An archive file is a file that is composed of one or more computer files along with metadata. |
| **ArchiveFileFacet** | uco.observable | Facet | An archive file facet is a grouping of characteristics unique to a file that is composed of one o... |
| **BlockDeviceNode** | uco.observable | Class | A block device node is a UNIX filesystem special file that serves as a conduit to communicate wit... |
| **BotConfiguration** | uco.observable | Class | A bot configuration is a set of contextual settings for a software application that runs automate... |
| **Bundle** | uco.core | Class | A bundle is a container for a grouping of UCO content with no presumption of shared context. |
| **CharacterDeviceNode** | uco.observable | Class | A character device node is a UNIX filesystem special file that serves as a conduit to communicate... |
| **CompressedStreamFacet** | uco.observable | Facet | A compressed stream facet is a grouping of characteristics unique to the application of a size-re... |
| **ContactProfile** | uco.observable | Class | A contact profile is a grouping of characteristics unique to details for contacting a contact ent... |
| **ContentData** | uco.observable | Class | Content data is a block of digital data. |
| **ContentDataFacet** | uco.observable | Facet | A content data facet is a grouping of characteristics unique to a block of digital data. |
| **ContextualCompilation** | uco.core | Class | A contextual compilation is a grouping of things sharing some context (e.g., a set of network con... |
| **CredentialDump** | uco.observable | Class | A credential dump is a collection (typically forcibly extracted from a system) of specific login ... |
| **Directory** | uco.observable | Class | A directory is a file system cataloging structure which contains references to other computer fil... |
| **Disk** | uco.observable | Class | A disk is a storage mechanism where data is recorded by various electronic, magnetic, optical, or... |
| **DiskFacet** | uco.observable | Facet | A disk facet is a grouping of characteristics unique to a storage mechanism where data is recorde... |
| **DiskPartition** | uco.observable | Class | A disk partition is a particular managed region on a storage mechanism where data is recorded by ... |
| **DiskPartitionFacet** | uco.observable | Facet | A disk partition facet is a grouping of characteristics unique to a particular managed region on ... |
| **EXIFFacet** | uco.observable | Facet | An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the for... |
| **EncodedStreamFacet** | uco.observable | Facet | An encoded stream facet is a grouping of characteristics unique to the conversion of a body of da... |
| **EncryptedStreamFacet** | uco.observable | Facet | An encrypted stream facet is a grouping of characteristics unique to the conversion of a body of ... |
| **EventRecord** | uco.observable | Class | An event record is something that happens in a digital context (e.g., operating system events). |
| **EventRecordFacet** | uco.observable | Facet | An event record facet is a grouping of characteristics unique to something that happens in a digi... |
| **ExtInodeFacet** | uco.observable | Facet | An extInode facet is a grouping of characteristics unique to a file system object (file, director... |
| **ExternalReference** | uco.core | Class | Characteristics of a reference to a resource outside of the UCO. |
| **ExtractedString** | uco.observable | Class | An extracted string is a grouping of characteristics unique to a series of characters pulled from... |
| **ExtractedStringsFacet** | uco.observable | Facet | An extracted strings facet is a grouping of characteristics unique to one or more sequences of ch... |
| **File** | uco.observable | Class | A file is a computer resource for recording data discretely on a computer storage device. |
| **FileFacet** | uco.observable | Facet | A file facet is a grouping of characteristics unique to the storage of a file (computer resource ... |
| **FilePermissionsFacet** | uco.observable | Facet | A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view... |
| **FileSystem** | uco.observable | Class | A file system is the process that manages how and where data on a storage medium is stored, acces... |
| **FileSystemFacet** | uco.observable | Facet | A file system facet is a grouping of characteristics unique to the process that manages how and w... |
| **FileSystemObject** | uco.observable | Class | A file system object is an informational object represented and managed within a file system. |
| **ForumPost** | uco.observable | Class | A forum post is message submitted by a user account to an online forum where the message content ... |
| **FragmentFacet** | uco.observable | Facet | A fragment facet is a grouping of characteristics unique to an individual piece of the content of... |
| **GUI** | uco.observable | Class | A GUI is a graphical user interface that allows users to interact with electronic devices through... |
| **GeoLocationTrack** | uco.observable | Class | A geolocation track is a set of contiguous geolocation entries representing a path/track taken. |
| **GeoLocationTrackFacet** | uco.observable | Facet | A geolocation track facet is a grouping of characteristics unique to a set of contiguous geolocat... |
| **Grouping** | uco.core | Class | A grouping is a compilation of referenced UCO content with a shared context. |
| **HTTPConnection** | uco.observable | Class | An HTTP connection is network connection that is conformant to the Hypertext Transfer Protocol (H... |
| **HTTPConnectionFacet** | uco.observable | Facet | An HTTP connection facet is a grouping of characteristics unique to portions of a network connect... |
| **Image** | uco.observable | Class | An image is a complete copy of a hard disk, memory, or other digital media. |
| **ImageFacet** | uco.observable | Facet | An image facet is a grouping of characteristics unique to a complete copy of a hard disk, memory,... |
| **InvestigativeAction** | case.investigation | Class | An investigative action is something that may be done or performed within the context of an inves... |
| **Junction** | uco.observable | Class | A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory ... |
| **MftRecordFacet** | uco.observable | Facet | An MFT record facet is a grouping of characteristics unique to the details of a single file as ma... |
| **NTFSFile** | uco.observable | Class | An NTFS file is a New Technology File System (NTFS) file. |
| **NTFSFileFacet** | uco.observable | Facet | An NTFS file facet is a grouping of characteristics unique to a file on an NTFS (new technology f... |
| **NTFSFilePermissionsFacet** | uco.observable | Facet | An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g.... |
| **NamedPipe** | uco.observable | Class | A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is pers... |
| **NetworkProtocol** | uco.observable | Class | A network protocol is an established set of structured rules that determine how data is transmitt... |
| **NetworkRoute** | uco.observable | Class | A network route is a specific path (of specific network nodes, connections and protocols) for tra... |
| **Note** | uco.observable | Class | A note is a brief textual record. |
| **NoteFacet** | uco.observable | Facet | A note facet is a grouping of characteristics unique to a brief textual record. |
| **PDFFile** | uco.observable | Class | A PDF file is a Portable Document Format (PDF) file. |
| **PDFFileFacet** | uco.observable | Facet | A PDF file facet is a grouping of characteristics unique to a PDF (Portable Document Format) file. |
| **PathRelationFacet** | uco.observable | Facet | A path relation facet is a grouping of characteristics unique to the location of one object withi... |
| **Pipe** | uco.observable | Class | A pipe is a mechanism for one-way inter-process communication using message passing where data wr... |
| **Profile** | uco.observable | Class | A profile is an explicit digital representation of identity and characteristics of the owner of a... |
| **ProfileFacet** | uco.observable | Facet | A profile facet is a grouping of characteristics unique to an explicit digital representation of ... |
| **RecoveredObjectFacet** | uco.observable | Facet | Recoverability status of name, metadata, and content. |
| **ReleaseToMarking** | uco.marking | Class | A release-to marking is a grouping of characteristics unique to the expression of data marking de... |
| **ReparsePoint** | uco.observable | Class | A reparse point is a type of NTFS (New Technology File System) object which is an optional attrib... |
| **Role** | uco.role | Class | A role is a usual or customary function based on contextual perspective. |
| **Snapshot** | uco.observable | Class | A snapshot is a file system object representing a snapshot of the contents of a part of a file sy... |
| **Socket** | uco.observable | Class | A socket is a special file used for inter-process communication, which enables communication betw... |
| **StatementMarking** | uco.marking | Class | A statement marking is a grouping of characteristics unique to the expression of data marking def... |
| **SymbolicLink** | uco.observable | Class | A symbolic link is a file that contains a reference to another file or directory in the form of a... |
| **SymbolicLinkFacet** | uco.observable | Facet | A symbolic link facet is a grouping of characteristics unique to a file that contains a reference... |
| **TermsOfUseMarking** | uco.marking | Class | A terms of use marking is a grouping of characteristics unique to the expression of data marking ... |
| **ToolCapability** | ext.toolcap | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |
| **TwitterProfileFacet** | uco.observable | Facet | A twitter profile facet is a grouping of characteristics unique to an explicit digital representa... |
| **UNIXFile** | uco.observable | Class | A UNIX file is a file pertaining to the UNIX operating system. |
| **UNIXFilePermissionsFacet** | uco.observable | Facet | A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g.,... |
| **UNIXVolumeFacet** | uco.observable | Facet | A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (... |
| **UcoObject** | uco.core | Class | A UCO object is a representation of a fundamental concept either directly inherent to the cyber d... |
| **Volume** | uco.observable | Class | A volume is a single accessible storage area (volume) with a single file system. [based on https:... |
| **VolumeFacet** | uco.observable | Facet | A volume facet is a grouping of characteristics unique to a single accessible storage area (volum... |
| **Wiki** | uco.observable | Class | A wiki is an online hypertext publication collaboratively edited and managed by its own audience ... |
| **WindowsActiveDirectoryAccount** | uco.observable | Class | A Windows Active Directory account is an account managed by directory-based identity-related serv... |
| **WindowsActiveDirectoryAccountFacet** | uco.observable | Facet | A Windows Active Directory account facet is a grouping of characteristics unique to an account ma... |
| **WindowsFilemapping** | uco.observable | Class | A Windows file mapping is the association of a file's contents with a portion of the virtual addr... |
| **WindowsHandle** | uco.observable | Class | A Windows handle is an abstract reference to a resource within the Windows operating system, such... |
| **WindowsMailslot** | uco.observable | Class | A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard ... |
| **WindowsPEBinaryFile** | uco.observable | Class | A Windows PE binary file is a Windows portable executable (PE) file. |
| **WindowsPEBinaryFileFacet** | uco.observable | Facet | A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable exec... |
| **WindowsPEFileHeader** | uco.observable | Class | A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE ... |
| **WindowsPEOptionalHeader** | uco.observable | Class | A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of ... |
| **WindowsPESection** | uco.observable | Class | A Windows PE section is a grouping of characteristics unique to a specific default or custom-defi... |
| **WindowsPrefetch** | uco.observable | Class | The Windows prefetch contains entries in a Windows prefetch file (used to speed up application st... |
| **WindowsPrefetchFacet** | uco.observable | Facet | A Windows prefetch facet is a grouping of characteristics unique to entries in the Windows prefet... |
| **WindowsSystemRestore** | uco.observable | Class | A Windows system restore is a capture of a Windows computer's state (including system files, inst... |
| **WindowsVolumeFacet** | uco.observable | Facet | A Windows volume facet is a grouping of characteristics unique to a single accessible storage are... |
| **X509V3ExtensionsFacet** | uco.observable | Facet | An X.509 v3 certificate extensions facet is a grouping of characteristics unique to a public key ... |

**AlternateDataStream** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ArchiveFile** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**BlockDeviceNode** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, FileFacet

graph.create(ObservableObject, has_facet=[
    FileFacet(file_name="evidence.dd", size_in_bytes=1073741824)
])
```

## Network Activity

Classes for network connections, IP addresses, DNS records, URLs, and related artifacts. Use these when modeling network traffic captures, connection logs, or web-related evidence.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **API** | uco.observable | Class | An API (application programming interface) is a computing interface that defines interactions bet... |
| **ARPCache** | uco.observable | Class | An ARP cache is a collection of Address Resolution Protocol (ARP) entries (mostly dynamic) that a... |
| **ARPCacheEntry** | uco.observable | Class | An ARP cache entry is a single Address Resolution Protocol (ARP) response record that is created ... |
| **ActionLifecycle** | uco.action | Class | An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subo... |
| **Adaptor** | uco.observable | Class | An adaptor is a device that physically converts the pin outputs but does not alter the underlying... |
| **AndroidDevice** | uco.observable | Class | An Android device is a device running the Android operating system. [based on https://en.wikipedi... |
| **AndroidDeviceFacet** | uco.observable | Facet | An Android device facet is a grouping of characteristics unique to an Android device. [based on h... |
| **Appliance** | uco.observable | Class | An appliance is a purpose-built computer with software or firmware that is designed to provide a ... |
| **AutonomousSystem** | uco.observable | Class | An autonomous system is a collection of connected Internet Protocol (IP) routing prefixes under t... |
| **AutonomousSystemFacet** | uco.observable | Facet | An autonomous system facet is a grouping of characteristics unique to a collection of connected I... |
| **BlockDeviceNode** | uco.observable | Class | A block device node is a UNIX filesystem special file that serves as a conduit to communicate wit... |
| **BotConfiguration** | uco.observable | Class | A bot configuration is a set of contextual settings for a software application that runs automate... |
| **BrowserBookmark** | uco.observable | Class | A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software progr... |
| **BrowserBookmarkFacet** | uco.observable | Facet | A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs... |
| **BrowserCookie** | uco.observable | Class | A browser cookie is a piece of of data sent from a website and stored on the user's computer by t... |
| **BrowserCookieFacet** | uco.observable | Facet | A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a web... |
| **Call** | uco.observable | Class | A call is a connection as part of a realtime cyber communication between one or more parties. |
| **CallFacet** | uco.observable | Facet | A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber ... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **CharacterDeviceNode** | uco.observable | Class | A character device node is a UNIX filesystem special file that serves as a conduit to communicate... |
| **Code** | uco.observable | Class | Code is a direct representation (source, byte or binary) of a collection of computer instructions... |
| **CompilerType** | uco.tool | Class | A compiler type is a grouping of characteristics unique to a specific program that translates com... |
| **ContactList** | uco.observable | Class | A contact list is a set of multiple individual contacts such as that found in a digital address b... |
| **ContactListFacet** | uco.observable | Facet | A contact list facet is a grouping of characteristics unique to a set of multiple individual cont... |
| **ContactSIP** | uco.observable | Class | A contact SIP is a grouping of characteristics unique to details for contacting a contact entity ... |
| **ContactURL** | uco.observable | Class | A contact URL is a grouping of characteristics unique to details for contacting a contact entity ... |
| **ContextualCompilation** | uco.core | Class | A contextual compilation is a grouping of things sharing some context (e.g., a set of network con... |
| **DNSCache** | uco.observable | Class | An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query ... |
| **DNSRecord** | uco.observable | Class | A DNS record is a single Domain Name System (DNS) artifact specifying information of a particular... |
| **Device** | uco.observable | Class | A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a ... |
| **DeviceFacet** | uco.observable | Facet | A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism des... |
| **DigitalAccount** | uco.observable | Class | A digital account is an arrangement with an entity to enable and control the provision of some ca... |
| **DigitalAccountFacet** | uco.observable | Facet | A digital account facet is a grouping of characteristics unique to an arrangement with an entity ... |
| **DigitalCamera** | uco.observable | Class | A digital camera is a camera that captures photographs in digital memory as opposed to capturing ... |
| **Directory** | uco.observable | Class | A directory is a file system cataloging structure which contains references to other computer fil... |
| **DiskPartition** | uco.observable | Class | A disk partition is a particular managed region on a storage mechanism where data is recorded by ... |
| **DomainName** | uco.observable | Class | A domain name is an identification string that defines a realm of administrative autonomy, author... |
| **DomainNameFacet** | uco.observable | Facet | A domain name facet is a grouping of characteristics unique to an identification string that defi... |
| **EXIFFacet** | uco.observable | Facet | An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the for... |
| **EmailAddress** | uco.observable | Class | An email address is an identifier for an electronic mailbox to which electronic mail messages (co... |
| **EmailAddressFacet** | uco.observable | Facet | An email address facet is a grouping of characteristics unique to an identifier for an electronic... |
| **EnvironmentVariable** | uco.observable | Class | An environment variable is a grouping of characteristics unique to a dynamic-named value that can... |
| **Facet** | uco.core | Facet | A facet is a grouping of characteristics singularly unique to a particular inherent aspect of a U... |
| **FileFacet** | uco.observable | Facet | A file facet is a grouping of characteristics unique to the storage of a file (computer resource ... |
| **FileSystem** | uco.observable | Class | A file system is the process that manages how and where data on a storage medium is stored, acces... |
| **FileSystemFacet** | uco.observable | Facet | A file system facet is a grouping of characteristics unique to the process that manages how and w... |
| **GUI** | uco.observable | Class | A GUI is a graphical user interface that allows users to interact with electronic devices through... |
| **GenericObservableObject** | uco.observable | Class | A generic observable object is an article or unit within the digital domain. |
| **GlobalFlagType** | uco.observable | Class | A global flag type is a grouping of characteristics unique to the Windows systemwide global varia... |
| **GranularMarking** | uco.marking | Class | A granular marking is a grouping of characteristics unique to specification of marking definition... |
| **HTTPConnection** | uco.observable | Class | An HTTP connection is network connection that is conformant to the Hypertext Transfer Protocol (H... |
| **HTTPConnectionFacet** | uco.observable | Facet | An HTTP connection facet is a grouping of characteristics unique to portions of a network connect... |
| **Hash** | uco.types | Class | A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm... |
| **Hostname** | uco.observable | Class | A hostname is a label that is assigned to a device connected to a computer network and that is us... |
| **ICMPConnection** | uco.observable | Class | An ICMP connection is a network connection that is conformant to the Internet Control Message Pro... |
| **ICMPConnectionFacet** | uco.observable | Facet | An ICMP connection facet is a grouping of characteristics unique to portions of a network connect... |
| **IComHandlerActionType** | uco.observable | Class | An IComHandler action type is a grouping of characteristics unique to a Windows Task-related acti... |
| **IExecActionType** | uco.observable | Class | An IExec action type is a grouping of characteristics unique to an action that executes a command... |
| **IPAddress** | uco.observable | Class | An IP address is an Internet Protocol (IP) standards conformant identifier assigned to a device t... |
| **IPAddressFacet** | uco.observable | Facet | An IP address facet is a grouping of characteristics unique to an Internet Protocol (IP) standard... |
| **IPNetmask** | uco.observable | Class | An IP netmask is a 32-bit 'mask' used to divide an IP address into subnets and specify the networ... |
| **IPhone** | uco.observable | Class | An iPhone is a smart phone that applies the iOS mobile operating system. |
| **IPv4Address** | uco.observable | Class | An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned... |
| **IPv4AddressFacet** | uco.observable | Facet | An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an... |
| **IPv6Address** | uco.observable | Class | An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned... |
| **IPv6AddressFacet** | uco.observable | Facet | An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an... |
| **IShowMessageActionType** | uco.observable | Class | An IShow message action type is a grouping of characteristics unique to an action that shows a me... |
| **Junction** | uco.observable | Class | A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory ... |
| **Laptop** | uco.observable | Class | A laptop, laptop computer, or notebook computer is a small, portable personal computer with a scr... |
| **Library** | uco.observable | Class | A library is a suite of data and programming code that is used to develop software programs and a... |
| **LibraryFacet** | uco.observable | Facet | A library facet is a grouping of characteristics unique to a suite of data and programming code t... |
| **MACAddress** | uco.observable | Class | A MAC address is a media access control standards conformant identifier assigned to a network int... |
| **MACAddressFacet** | uco.observable | Facet | A MAC address facet is a grouping of characteristics unique to a media access control standards c... |
| **Message** | uco.observable | Class | A message is a discrete unit of electronic communication intended by the source for consumption b... |
| **MessageFacet** | uco.observable | Facet | A message facet is a grouping of characteristics unique to a discrete unit of electronic communic... |
| **MftRecordFacet** | uco.observable | Facet | An MFT record facet is a grouping of characteristics unique to the details of a single file as ma... |
| **MobileAccount** | uco.observable | Class | A mobile account is an arrangement with an entity to enable and control the provision of some cap... |
| **MobileAccountFacet** | uco.observable | Facet | A mobile account facet is a grouping of characteristics unique to an arrangement with an entity t... |
| **MobileDevice** | uco.observable | Class | A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobil... |
| **MobileDeviceFacet** | uco.observable | Facet | A mobile device facet is a grouping of characteristics unique to a portable computing device. [ba... |
| **MobilePhone** | uco.observable | Class | A mobile phone is a portable telephone that at least can make and receive calls over a radio freq... |
| **Mutex** | uco.observable | Class | A mutex is a mechanism that enforces limits on access to a resource when there are many threads o... |
| **MutexFacet** | uco.observable | Facet | A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on acce... |
| **NamedPipe** | uco.observable | Class | A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is pers... |
| **NetworkAppliance** | uco.observable | Class | A network appliance is a purpose-built computer with software or firmware that is designed to pro... |
| **NetworkConnection** | uco.observable | Class | A network connection is a connection (completed or attempted) across a digital network (a group o... |
| **NetworkConnectionFacet** | uco.observable | Facet | A network connection facet is a grouping of characteristics unique to a connection (complete or a... |
| **NetworkFlow** | uco.observable | Class | A network flow is a sequence of data transiting one or more digital network (a group or two or mo... |
| **NetworkFlowFacet** | uco.observable | Facet | A network flow facet is a grouping of characteristics unique to a sequence of data transiting one... |
| **NetworkInterface** | uco.observable | Class | A network interface is a software or hardware interface between two pieces of equipment or protoc... |
| **NetworkInterfaceFacet** | uco.observable | Facet | A network interface facet is a grouping of characteristics unique to a software or hardware inter... |
| **NetworkProtocol** | uco.observable | Class | A network protocol is an established set of structured rules that determine how data is transmitt... |
| **NetworkRoute** | uco.observable | Class | A network route is a specific path (of specific network nodes, connections and protocols) for tra... |
| **NetworkSubnet** | uco.observable | Class | A network subnet is a logical subdivision of an IP network. [based on https://en.wikipedia.org/wi... |
| **Observable** | uco.observable | Class | An observable is a characterizable item or action within the digital domain. |
| **ObservableAction** | uco.observable | Class | An observable action is a grouping of characteristics unique to something that may be done or per... |
| **ObservableObject** | uco.observable | Class | An observable object is a grouping of characteristics unique to a distinct article or unit within... |
| **ObservableRelationship** | uco.observable | Class | An observable relationship is a grouping of characteristics unique to an assertion of an associat... |
| **OnlineService** | uco.observable | Class | An online service is a particular provision mechanism of information access, distribution or mani... |
| **OnlineServiceFacet** | uco.observable | Facet | An online service facet is a grouping of characteristics unique to a particular provision mechani... |
| **OperatingSystem** | uco.observable | Class | An operating system is the software that manages computer hardware, software resources, and provi... |
| **OperatingSystemFacet** | uco.observable | Facet | An operating system facet is a grouping of characteristics unique to the software that manages co... |
| **Organization** | uco.identity | Class | An organization is a grouping of identifying characteristics unique to a group of people who work... |
| **PDFFile** | uco.observable | Class | A PDF file is a Portable Document Format (PDF) file. |
| **PDFFileFacet** | uco.observable | Facet | A PDF file facet is a grouping of characteristics unique to a PDF (Portable Document Format) file. |
| **PaymentCard** | uco.observable | Class | A payment card is a physical token that is part of a payment system issued by financial instituti... |
| **Person** | uco.identity | Class | A person is a grouping of identifying characteristics unique to a human being regarded as an indi... |
| **Pipe** | uco.observable | Class | A pipe is a mechanism for one-way inter-process communication using message passing where data wr... |
| **ProcessThread** | uco.observable | Class | A process thread is the smallest sequence of programmed instructions that can be managed independ... |
| **Profile** | uco.observable | Class | A profile is an explicit digital representation of identity and characteristics of the owner of a... |
| **ProfileFacet** | uco.observable | Facet | A profile facet is a grouping of characteristics unique to an explicit digital representation of ... |
| **ProtocolConverter** | uco.observable | Class | A protocol converter is a device that converts from one protocol to another (e.g. SD to USB, SATA... |
| **ProvenanceRecord** | case.investigation | Class | A provenance record is a grouping of characteristics unique to the provenantial (chronology of th... |
| **Relationship** | uco.core | Class | A relationship is a grouping of characteristics unique to an assertion that one or more objects a... |
| **ReparsePoint** | uco.observable | Class | A reparse point is a type of NTFS (New Technology File System) object which is an optional attrib... |
| **SIMCard** | uco.observable | Class | A SIM card is a subscriber identification module card intended to securely store the internationa... |
| **SIMCardFacet** | uco.observable | Facet | A SIM card facet is a grouping of characteristics unique to a subscriber identification module ca... |
| **SIPAddress** | uco.observable | Class | A SIP address is an identifier for Session Initiation Protocol (SIP) communication. |
| **SIPAddressFacet** | uco.observable | Facet | A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP... |
| **SMSMessage** | uco.observable | Class | An SMS message is a message conformant to the short message service (SMS) communication protocol ... |
| **SMSMessageFacet** | uco.observable | Facet | A SMS message facet is a grouping of characteristics unique to a message conformant to the short ... |
| **SQLiteBlob** | uco.observable | Class | An SQLite blob is a blob (binary large object) of data within an SQLite database. [based on https... |
| **SQLiteBlobFacet** | uco.observable | Facet | An SQLite blob facet is a grouping of characteristics unique to a blob (binary large object) of d... |
| **SecurityAppliance** | uco.observable | Class | A security appliance is a purpose-built computer with software or firmware that is designed to pr... |
| **Semaphore** | uco.observable | Class | A semaphore is a variable or abstract data type used to control access to a common resource by mu... |
| **SmartDevice** | uco.observable | Class | A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-... |
| **SmartPhone** | uco.observable | Class | A smartphone is a portable device that combines mobile telephone and computing functions into one... |
| **Socket** | uco.observable | Class | A socket is a special file used for inter-process communication, which enables communication betw... |
| **SocketAddress** | uco.observable | Class | A socket address (combining and IP address and a port number) is a composite identifier for a net... |
| **Software** | uco.observable | Class | Software is a definitely scoped instance of a collection of data or computer instructions that te... |
| **SoftwareFacet** | uco.observable | Facet | A software facet is a grouping of characteristics unique to a software program (a definitively sc... |
| **StorageMediumFacet** | uco.observable | Facet | A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a... |
| **SubjectActionLifecycle** | case.investigation | Class | A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions ... |
| **SymbolicLink** | uco.observable | Class | A symbolic link is a file that contains a reference to another file or directory in the form of a... |
| **SymbolicLinkFacet** | uco.observable | Facet | A symbolic link facet is a grouping of characteristics unique to a file that contains a reference... |
| **TCPConnection** | uco.observable | Class | A TCP connection is a network connection that is conformant to the Transfer  |
| **TCPConnectionFacet** | uco.observable | Facet | A TCP connection facet is a grouping of characteristics unique to portions of a network connectio... |
| **Thread** | uco.types | Class | A semi-ordered array of items, that can be present in multiple copies.  Implemetation of a UCO Th... |
| **ToolCapability** | ext.toolcap | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |
| **TriggerType** | uco.observable | Class | A trigger type is a grouping of characterizes unique to a set of criteria that, when met, starts ... |
| **TwitterProfileFacet** | uco.observable | Facet | A twitter profile facet is a grouping of characteristics unique to an explicit digital representa... |
| **UNIXVolumeFacet** | uco.observable | Facet | A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (... |
| **URL** | uco.observable | Class | A URL is a uniform resource locator (URL) acting as a resolvable address to a particular WWW (Wor... |
| **URLFacet** | uco.observable | Facet | A URL facet is a grouping of characteristics unique to a uniform resource locator (URL) acting as... |
| **URLHistory** | uco.observable | Class | A URL history characterizes the stored URL history for a particular web browser |
| **URLHistoryEntry** | uco.observable | Class | A URL history entry is a grouping of characteristics unique to the properties of a single URL his... |
| **URLHistoryFacet** | uco.observable | Facet | A URL history facet is a grouping of characteristics unique to the stored URL history for a parti... |
| **URLVisit** | uco.observable | Class | A URL visit characterizes the properties of a visit of a URL within a particular browser. |
| **URLVisitFacet** | uco.observable | Facet | A URL visit facet is a grouping of characteristics unique to the properties of a visit of a URL w... |
| **UcoInherentCharacterizationThing** | uco.core | Class | A UCO inherent characterization thing is a grouping of characteristics unique to a particular inh... |
| **UcoObject** | uco.core | Class | A UCO object is a representation of a fundamental concept either directly inherent to the cyber d... |
| **UserAccount** | uco.observable | Class | A user account is an account controlling a user's access to a network, system or platform. |
| **UserAccountFacet** | uco.observable | Facet | A user account facet is a grouping of characteristics unique to an account controlling a user's a... |
| **UserSession** | uco.observable | Class | A user session is a temporary and interactive information interchange between two or more communi... |
| **UserSessionFacet** | uco.observable | Facet | A user session facet is a grouping of characteristics unique to a temporary and interactive infor... |
| **VictimActionLifecycle** | case.investigation | Class | A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions o... |
| **Volume** | uco.observable | Class | A volume is a single accessible storage area (volume) with a single file system. [based on https:... |
| **VolumeFacet** | uco.observable | Facet | A volume facet is a grouping of characteristics unique to a single accessible storage area (volum... |
| **WebPage** | uco.observable | Class | A web page is a specific collection of information provided by a website and displayed to a user ... |
| **WhoIs** | uco.observable | Class | WhoIs is a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https:... |
| **WhoIsFacet** | uco.observable | Facet | A whois facet is a grouping of characteristics unique to a response record conformant to the WHOI... |
| **WhoisContactFacet** | uco.observable | Facet | A Whois contact type is a grouping of characteristics unique to contact-related information prese... |
| **WhoisRegistrarInfoType** | uco.observable | Class | A Whois registrar info type is a grouping of characteristics unique to registrar-related informat... |
| **WifiAddress** | uco.observable | Class | A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a dev... |
| **WifiAddressFacet** | uco.observable | Facet | A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) sta... |
| **Wiki** | uco.observable | Class | A wiki is an online hypertext publication collaboratively edited and managed by its own audience ... |
| **WindowsCriticalSection** | uco.observable | Class | A Windows critical section is a Windows object that provides synchronization similar to that prov... |
| **WindowsEvent** | uco.observable | Class | A Windows event is a notification record of an occurance of interest (system, security, applicati... |
| **WindowsFilemapping** | uco.observable | Class | A Windows file mapping is the association of a file's contents with a portion of the virtual addr... |
| **WindowsHandle** | uco.observable | Class | A Windows handle is an abstract reference to a resource within the Windows operating system, such... |
| **WindowsHook** | uco.observable | Class | A Windows hook is a mechanism by which an application can intercept events, such as messages, mou... |
| **WindowsMailslot** | uco.observable | Class | A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard ... |
| **WindowsNetworkShare** | uco.observable | Class | A Windows network share is a Windows computer resource made available from one host to other host... |
| **WindowsPEBinaryFile** | uco.observable | Class | A Windows PE binary file is a Windows portable executable (PE) file. |
| **WindowsPEBinaryFileFacet** | uco.observable | Facet | A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable exec... |
| **WindowsPEFileHeader** | uco.observable | Class | A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE ... |
| **WindowsPEOptionalHeader** | uco.observable | Class | A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of ... |
| **WindowsPESection** | uco.observable | Class | A Windows PE section is a grouping of characteristics unique to a specific default or custom-defi... |
| **WindowsRegistryHive** | uco.observable | Class | The Windows registry hive is a particular logical group of keys, subkeys, and values in a Windows... |
| **WindowsRegistryHiveFacet** | uco.observable | Facet | A Windows registry hive facet is a grouping of characteristics unique to a particular logical gro... |
| **WindowsRegistryKey** | uco.observable | Class | A Windows registry key is a particular key within a Windows registry (a hierarchical database tha... |
| **WindowsRegistryKeyFacet** | uco.observable | Facet | A Windows registry key facet is a grouping of characteristics unique to a particular key within a... |
| **WindowsRegistryValue** | uco.observable | Class | A Windows registry value is a grouping of characteristics unique to a particular value within a W... |
| **WindowsService** | uco.observable | Class | A Windows service is a specific Windows service (a computer program that operates in the backgrou... |
| **WindowsServiceFacet** | uco.observable | Facet | A Windows service facet is a grouping of characteristics unique to a specific Windows service (a ... |
| **WindowsSystemRestore** | uco.observable | Class | A Windows system restore is a capture of a Windows computer's state (including system files, inst... |
| **WindowsTask** | uco.observable | Class | A Windows task is a process that is scheduled to execute on a Windows operating system by the Win... |
| **WindowsTaskFacet** | uco.observable | Facet | A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is... |
| **WindowsVolumeFacet** | uco.observable | Facet | A Windows volume facet is a grouping of characteristics unique to a single accessible storage are... |
| **WindowsWaitableTime** | uco.observable | Class | A Windows waitable timer is a synchronization object within the Windows operating system whose st... |
| **WirelessNetworkConnection** | uco.observable | Class | A wireless network connection is a connection (completed or attempted) across an IEEE 802.11 stan... |
| **WirelessNetworkConnectionFacet** | uco.observable | Facet | A wireless network connection facet is a grouping of characteristics unique to a connection (comp... |

**API** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ARPCache** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ARPCacheEntry** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, IPv4AddressFacet

graph.create(ObservableObject, has_facet=[
    IPv4AddressFacet(address_value="192.168.1.100")
])
```

## Devices and Hardware

Classes for physical and virtual devices, storage media, and hardware characteristics. Use these when documenting the devices involved in an investigation or the hardware from which data was extracted.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **API** | uco.observable | Class | An API (application programming interface) is a computing interface that defines interactions bet... |
| **ARPCache** | uco.observable | Class | An ARP cache is a collection of Address Resolution Protocol (ARP) entries (mostly dynamic) that a... |
| **ARPCacheEntry** | uco.observable | Class | An ARP cache entry is a single Address Resolution Protocol (ARP) response record that is created ... |
| **Adaptor** | uco.observable | Class | An adaptor is a device that physically converts the pin outputs but does not alter the underlying... |
| **AnalyticTool** | uco.tool | Class | An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purp... |
| **AndroidDevice** | uco.observable | Class | An Android device is a device running the Android operating system. [based on https://en.wikipedi... |
| **AndroidDeviceFacet** | uco.observable | Facet | An Android device facet is a grouping of characteristics unique to an Android device. [based on h... |
| **AndroidPhone** | uco.observable | Class | An android phone is a smart phone that applies the Android mobile operating system. |
| **AppleDevice** | uco.observable | Class | An apple device is a smart device that applies either the MacOS or iOS operating system. |
| **Appliance** | uco.observable | Class | An appliance is a purpose-built computer with software or firmware that is designed to provide a ... |
| **ArchiveFile** | uco.observable | Class | An archive file is a file that is composed of one or more computer files along with metadata. |
| **ArchiveFileFacet** | uco.observable | Facet | An archive file facet is a grouping of characteristics unique to a file that is composed of one o... |
| **BlackberryPhone** | uco.observable | Class | A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blac... |
| **BlockDeviceNode** | uco.observable | Class | A block device node is a UNIX filesystem special file that serves as a conduit to communicate wit... |
| **BluetoothAddress** | uco.observable | Class | A Bluetooth address is a Bluetooth standard conformant identifier assigned to a Bluetooth device ... |
| **BluetoothAddressFacet** | uco.observable | Facet | A Bluetooth address facet is a grouping of characteristics unique to a Bluetooth standard conform... |
| **BrowserCookie** | uco.observable | Class | A browser cookie is a piece of of data sent from a website and stored on the user's computer by t... |
| **BrowserCookieFacet** | uco.observable | Facet | A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a web... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **CharacterDeviceNode** | uco.observable | Class | A character device node is a UNIX filesystem special file that serves as a conduit to communicate... |
| **Code** | uco.observable | Class | Code is a direct representation (source, byte or binary) of a collection of computer instructions... |
| **CompilerType** | uco.tool | Class | A compiler type is a grouping of characteristics unique to a specific program that translates com... |
| **Computer** | uco.observable | Class | A computer is an electronic device for storing and processing data, typically in binary, accordin... |
| **ComputerSpecification** | uco.observable | Class | A computer specification is the hardware and software of a programmable electronic device that ca... |
| **ComputerSpecificationFacet** | uco.observable | Facet | A computer specificaiton facet is a grouping of characteristics unique to the hardware and softwa... |
| **ContactPhone** | uco.observable | Class | A contact phone is a grouping of characteristics unique to details for contacting a contact entit... |
| **DNSCache** | uco.observable | Class | An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query ... |
| **DefensiveTool** | uco.tool | Class | A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purp... |
| **Device** | uco.observable | Class | A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a ... |
| **DeviceFacet** | uco.observable | Facet | A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism des... |
| **Directory** | uco.observable | Class | A directory is a file system cataloging structure which contains references to other computer fil... |
| **Disk** | uco.observable | Class | A disk is a storage mechanism where data is recorded by various electronic, magnetic, optical, or... |
| **DiskFacet** | uco.observable | Facet | A disk facet is a grouping of characteristics unique to a storage mechanism where data is recorde... |
| **DiskPartition** | uco.observable | Class | A disk partition is a particular managed region on a storage mechanism where data is recorded by ... |
| **DiskPartitionFacet** | uco.observable | Facet | A disk partition facet is a grouping of characteristics unique to a particular managed region on ... |
| **EXIFFacet** | uco.observable | Facet | An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the for... |
| **EmbeddedDevice** | uco.observable | Class | An embedded device is a highly specialized microprocessor device meant for one or very few specif... |
| **EnvironmentVariable** | uco.observable | Class | An environment variable is a grouping of characteristics unique to a dynamic-named value that can... |
| **File** | uco.observable | Class | A file is a computer resource for recording data discretely on a computer storage device. |
| **FileFacet** | uco.observable | Facet | A file facet is a grouping of characteristics unique to the storage of a file (computer resource ... |
| **FileSystem** | uco.observable | Class | A file system is the process that manages how and where data on a storage medium is stored, acces... |
| **FileSystemFacet** | uco.observable | Facet | A file system facet is a grouping of characteristics unique to the process that manages how and w... |
| **GUI** | uco.observable | Class | A GUI is a graphical user interface that allows users to interact with electronic devices through... |
| **GamingConsole** | uco.observable | Class | A gaming console (video game console or game console) is an electronic system that connects to a ... |
| **Hostname** | uco.observable | Class | A hostname is a label that is assigned to a device connected to a computer network and that is us... |
| **IPAddress** | uco.observable | Class | An IP address is an Internet Protocol (IP) standards conformant identifier assigned to a device t... |
| **IPAddressFacet** | uco.observable | Facet | An IP address facet is a grouping of characteristics unique to an Internet Protocol (IP) standard... |
| **IPhone** | uco.observable | Class | An iPhone is a smart phone that applies the iOS mobile operating system. |
| **IPv4Address** | uco.observable | Class | An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned... |
| **IPv4AddressFacet** | uco.observable | Facet | An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an... |
| **IPv6Address** | uco.observable | Class | An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned... |
| **IPv6AddressFacet** | uco.observable | Facet | An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an... |
| **Image** | uco.observable | Class | An image is a complete copy of a hard disk, memory, or other digital media. |
| **ImageFacet** | uco.observable | Facet | An image facet is a grouping of characteristics unique to a complete copy of a hard disk, memory,... |
| **LanguagesFacet** | uco.identity | Facet | Languages is a grouping of characteristics unique to specific syntactically and grammatically sta... |
| **Laptop** | uco.observable | Class | A laptop, laptop computer, or notebook computer is a small, portable personal computer with a scr... |
| **MaliciousTool** | uco.tool | Class | A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent t... |
| **MarkingModel** | uco.marking | Class | A marking model is a grouping of characteristics unique to the expression of a particular form of... |
| **Memory** | uco.observable | Class | Memory is a particular region of temporary information storage (e.g., RAM (random access memory),... |
| **MemoryFacet** | uco.observable | Facet | A memory facet is a grouping of characteristics unique to a particular region of temporary inform... |
| **MobileAccount** | uco.observable | Class | A mobile account is an arrangement with an entity to enable and control the provision of some cap... |
| **MobileAccountFacet** | uco.observable | Facet | A mobile account facet is a grouping of characteristics unique to an arrangement with an entity t... |
| **MobileDevice** | uco.observable | Class | A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobil... |
| **MobileDeviceFacet** | uco.observable | Facet | A mobile device facet is a grouping of characteristics unique to a portable computing device. [ba... |
| **MobilePhone** | uco.observable | Class | A mobile phone is a portable telephone that at least can make and receive calls over a radio freq... |
| **Mutex** | uco.observable | Class | A mutex is a mechanism that enforces limits on access to a resource when there are many threads o... |
| **MutexFacet** | uco.observable | Facet | A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on acce... |
| **NetworkAppliance** | uco.observable | Class | A network appliance is a purpose-built computer with software or firmware that is designed to pro... |
| **NetworkConnection** | uco.observable | Class | A network connection is a connection (completed or attempted) across a digital network (a group o... |
| **NetworkConnectionFacet** | uco.observable | Facet | A network connection facet is a grouping of characteristics unique to a connection (complete or a... |
| **NetworkFlow** | uco.observable | Class | A network flow is a sequence of data transiting one or more digital network (a group or two or mo... |
| **NetworkFlowFacet** | uco.observable | Facet | A network flow facet is a grouping of characteristics unique to a sequence of data transiting one... |
| **NetworkInterface** | uco.observable | Class | A network interface is a software or hardware interface between two pieces of equipment or protoc... |
| **NetworkInterfaceFacet** | uco.observable | Facet | A network interface facet is a grouping of characteristics unique to a software or hardware inter... |
| **NetworkProtocol** | uco.observable | Class | A network protocol is an established set of structured rules that determine how data is transmitt... |
| **OperatingSystem** | uco.observable | Class | An operating system is the software that manages computer hardware, software resources, and provi... |
| **OperatingSystemFacet** | uco.observable | Facet | An operating system facet is a grouping of characteristics unique to the software that manages co... |
| **PhoneAccount** | uco.observable | Class | A phone account is an arrangement with an entity to enable and control the provision of a telepho... |
| **PhoneAccountFacet** | uco.observable | Facet | A phone account facet is a grouping of characteristics unique to an arrangement with an entity to... |
| **Process** | uco.observable | Class | A process is an instance of a computer program executed on an operating system. |
| **ProcessFacet** | uco.observable | Facet | A process facet is a grouping of characteristics unique to an instance of a computer program exec... |
| **ProcessThread** | uco.observable | Class | A process thread is the smallest sequence of programmed instructions that can be managed independ... |
| **ProtocolConverter** | uco.observable | Class | A protocol converter is a device that converts from one protocol to another (e.g. SD to USB, SATA... |
| **ReparsePoint** | uco.observable | Class | A reparse point is a type of NTFS (New Technology File System) object which is an optional attrib... |
| **SIMCard** | uco.observable | Class | A SIM card is a subscriber identification module card intended to securely store the internationa... |
| **SIMCardFacet** | uco.observable | Facet | A SIM card facet is a grouping of characteristics unique to a subscriber identification module ca... |
| **SIPAddressFacet** | uco.observable | Facet | A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP... |
| **SecurityAppliance** | uco.observable | Class | A security appliance is a purpose-built computer with software or firmware that is designed to pr... |
| **Server** | uco.observable | Class | A server is a server rack-mount based computer, minicomputer, supercomputer, etc. |
| **SmartDevice** | uco.observable | Class | A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-... |
| **SmartPhone** | uco.observable | Class | A smartphone is a portable device that combines mobile telephone and computing functions into one... |
| **Software** | uco.observable | Class | Software is a definitely scoped instance of a collection of data or computer instructions that te... |
| **SoftwareFacet** | uco.observable | Facet | A software facet is a grouping of characteristics unique to a software program (a definitively sc... |
| **StorageMedium** | uco.observable | Class | A storage medium is any digital storage device that applies electromagnetic or optical surfaces, ... |
| **StorageMediumFacet** | uco.observable | Facet | A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a... |
| **Tablet** | uco.observable | Class | A tablet is a mobile computer that is primarily operated by touching the screen. (Devices categor... |
| **Tool** | uco.tool | Class | A tool is an element of hardware and/or software utilized to carry out a particular function. |
| **ToolCapability** | ext.toolcap | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |
| **UNIXProcess** | uco.observable | Class | A UNIX process is an instance of a computer program executed on a UNIX operating system. |
| **UNIXProcessFacet** | uco.observable | Facet | A UNIX process facet is a grouping of characteristics unique to an instance of a computer program... |
| **UNIXVolumeFacet** | uco.observable | Facet | A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (... |
| **UserSession** | uco.observable | Class | A user session is a temporary and interactive information interchange between two or more communi... |
| **UserSessionFacet** | uco.observable | Facet | A user session facet is a grouping of characteristics unique to a temporary and interactive infor... |
| **Volume** | uco.observable | Class | A volume is a single accessible storage area (volume) with a single file system. [based on https:... |
| **VolumeFacet** | uco.observable | Facet | A volume facet is a grouping of characteristics unique to a single accessible storage area (volum... |
| **WearableDevice** | uco.observable | Class | A wearable device is an electronic device that is designed to be worn on a person's body. |
| **WifiAddress** | uco.observable | Class | A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a dev... |
| **WifiAddressFacet** | uco.observable | Facet | A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) sta... |
| **WindowsComputerSpecification** | uco.observable | Class | A Windows computer specification is the hardware ans software of a programmable electronic device... |
| **WindowsComputerSpecificationFacet** | uco.observable | Facet | A Windows computer specification facet is a grouping of characteristics unique to the hardware an... |
| **WindowsFilemapping** | uco.observable | Class | A Windows file mapping is the association of a file's contents with a portion of the virtual addr... |
| **WindowsMailslot** | uco.observable | Class | A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard ... |
| **WindowsNetworkShare** | uco.observable | Class | A Windows network share is a Windows computer resource made available from one host to other host... |
| **WindowsService** | uco.observable | Class | A Windows service is a specific Windows service (a computer program that operates in the backgrou... |
| **WindowsServiceFacet** | uco.observable | Facet | A Windows service facet is a grouping of characteristics unique to a specific Windows service (a ... |
| **WindowsSystemRestore** | uco.observable | Class | A Windows system restore is a capture of a Windows computer's state (including system files, inst... |
| **WindowsVolumeFacet** | uco.observable | Facet | A Windows volume facet is a grouping of characteristics unique to a single accessible storage are... |
| **WirelessNetworkConnection** | uco.observable | Class | A wireless network connection is a connection (completed or attempted) across an IEEE 802.11 stan... |
| **WirelessNetworkConnectionFacet** | uco.observable | Facet | A wireless network connection facet is a grouping of characteristics unique to a connection (comp... |
| **WriteBlocker** | uco.observable | Class | A write blocker is a device that allows read-only access to storage mediums in order to preserve ... |

**API** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ARPCache** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ARPCacheEntry** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, DeviceFacet

graph.create(ObservableObject, has_facet=[
    DeviceFacet(manufacturer="ExampleCorp", model="X1000")
])
```

## Applications and Software

Classes for installed applications, operating systems, software packages, and processes. Use these when modeling which software was present on a device or which processes were running.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **API** | uco.observable | Class | An API (application programming interface) is a computing interface that defines interactions bet... |
| **AnalyticTool** | uco.tool | Class | An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purp... |
| **AndroidDevice** | uco.observable | Class | An Android device is a device running the Android operating system. [based on https://en.wikipedi... |
| **AndroidPhone** | uco.observable | Class | An android phone is a smart phone that applies the Android mobile operating system. |
| **AppleDevice** | uco.observable | Class | An apple device is a smart device that applies either the MacOS or iOS operating system. |
| **Appliance** | uco.observable | Class | An appliance is a purpose-built computer with software or firmware that is designed to provide a ... |
| **Application** | uco.observable | Class | An application is a particular software program designed for end users. |
| **ApplicationAccount** | uco.observable | Class | An application account is an account within a particular software program designed for end users. |
| **ApplicationAccountFacet** | uco.observable | Facet | An application account facet is a grouping of characteristics unique to an account within a parti... |
| **ApplicationFacet** | uco.observable | Facet | An application facet is a grouping of characteristics unique to a particular software program des... |
| **ApplicationVersion** | uco.observable | Class | An application version is a grouping of characteristics unique to a particular software program v... |
| **BlackberryPhone** | uco.observable | Class | A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blac... |
| **BotConfiguration** | uco.observable | Class | A bot configuration is a set of contextual settings for a software application that runs automate... |
| **BrowserBookmark** | uco.observable | Class | A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software progr... |
| **BrowserBookmarkFacet** | uco.observable | Facet | A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs... |
| **BrowserCookie** | uco.observable | Class | A browser cookie is a piece of of data sent from a website and stored on the user's computer by t... |
| **BrowserCookieFacet** | uco.observable | Facet | A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a web... |
| **BuildFacet** | uco.tool | Facet | A build facet is a grouping of characteristics unique to a particular version of a software. |
| **BuildInformationType** | uco.tool | Class | A build information type is a grouping of characteristics that describe how a particular version ... |
| **BuildUtilityType** | uco.tool | Class | A build utility type characterizes the tool used to convert from source code to executable code f... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **Code** | uco.observable | Class | Code is a direct representation (source, byte or binary) of a collection of computer instructions... |
| **CompilerType** | uco.tool | Class | A compiler type is a grouping of characteristics unique to a specific program that translates com... |
| **CompressedStreamFacet** | uco.observable | Facet | A compressed stream facet is a grouping of characteristics unique to the application of a size-re... |
| **Computer** | uco.observable | Class | A computer is an electronic device for storing and processing data, typically in binary, accordin... |
| **ComputerSpecification** | uco.observable | Class | A computer specification is the hardware and software of a programmable electronic device that ca... |
| **ComputerSpecificationFacet** | uco.observable | Facet | A computer specificaiton facet is a grouping of characteristics unique to the hardware and softwa... |
| **Configuration** | uco.configuration | Class | A configuration is a grouping of characteristics unique to a set of parameters or initial setting... |
| **ConfigurationEntry** | uco.configuration | Class | A configuration entry is a grouping of characteristics unique to a particular parameter or initia... |
| **ConfiguredSoftware** | uco.observable | Class | A ConfiguredSoftware is a Software that is known to be configured to run in a more specified mann... |
| **CookieHistory** | uco.observable | Class | A cookie history is the stored web cookie history for a particular web browser. |
| **DefensiveTool** | uco.tool | Class | A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purp... |
| **Dependency** | uco.configuration | Class | A dependency is a grouping of characteristics unique to something that a tool or other software r... |
| **EmbeddedDevice** | uco.observable | Class | An embedded device is a highly specialized microprocessor device meant for one or very few specif... |
| **EnvironmentVariable** | uco.observable | Class | An environment variable is a grouping of characteristics unique to a dynamic-named value that can... |
| **EventRecord** | uco.observable | Class | An event record is something that happens in a digital context (e.g., operating system events). |
| **EventRecordFacet** | uco.observable | Facet | An event record facet is a grouping of characteristics unique to something that happens in a digi... |
| **FileFacet** | uco.observable | Facet | A file facet is a grouping of characteristics unique to the storage of a file (computer resource ... |
| **FileSystem** | uco.observable | Class | A file system is the process that manages how and where data on a storage medium is stored, acces... |
| **FileSystemFacet** | uco.observable | Facet | A file system facet is a grouping of characteristics unique to the process that manages how and w... |
| **GeoLocationEntry** | uco.observable | Class | A geolocation entry is a single application-specific geolocation entry. |
| **GeoLocationEntryFacet** | uco.observable | Facet | A geolocation entry facet is a grouping of characteristics unique to a single application-specifi... |
| **GlobalFlagType** | uco.observable | Class | A global flag type is a grouping of characteristics unique to the Windows systemwide global varia... |
| **IExecActionType** | uco.observable | Class | An IExec action type is a grouping of characteristics unique to an action that executes a command... |
| **IPhone** | uco.observable | Class | An iPhone is a smart phone that applies the iOS mobile operating system. |
| **Junction** | uco.observable | Class | A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory ... |
| **Library** | uco.observable | Class | A library is a suite of data and programming code that is used to develop software programs and a... |
| **LibraryFacet** | uco.observable | Facet | A library facet is a grouping of characteristics unique to a suite of data and programming code t... |
| **LibraryType** | uco.tool | Class | A library type is a grouping of characteristics unique to a collection of resources incorporated ... |
| **MaliciousTool** | uco.tool | Class | A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent t... |
| **Mutex** | uco.observable | Class | A mutex is a mechanism that enforces limits on access to a resource when there are many threads o... |
| **MutexFacet** | uco.observable | Facet | A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on acce... |
| **NamedPipe** | uco.observable | Class | A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is pers... |
| **NetworkAppliance** | uco.observable | Class | A network appliance is a purpose-built computer with software or firmware that is designed to pro... |
| **NetworkInterface** | uco.observable | Class | A network interface is a software or hardware interface between two pieces of equipment or protoc... |
| **NetworkInterfaceFacet** | uco.observable | Facet | A network interface facet is a grouping of characteristics unique to a software or hardware inter... |
| **NetworkProtocol** | uco.observable | Class | A network protocol is an established set of structured rules that determine how data is transmitt... |
| **OperatingSystem** | uco.observable | Class | An operating system is the software that manages computer hardware, software resources, and provi... |
| **OperatingSystemFacet** | uco.observable | Facet | An operating system facet is a grouping of characteristics unique to the software that manages co... |
| **Pipe** | uco.observable | Class | A pipe is a mechanism for one-way inter-process communication using message passing where data wr... |
| **Process** | uco.observable | Class | A process is an instance of a computer program executed on an operating system. |
| **ProcessFacet** | uco.observable | Facet | A process facet is a grouping of characteristics unique to an instance of a computer program exec... |
| **ProcessThread** | uco.observable | Class | A process thread is the smallest sequence of programmed instructions that can be managed independ... |
| **Profile** | uco.observable | Class | A profile is an explicit digital representation of identity and characteristics of the owner of a... |
| **ProfileFacet** | uco.observable | Facet | A profile facet is a grouping of characteristics unique to an explicit digital representation of ... |
| **PropertiesEnumeratedEffectFacet** | uco.observable | Facet | A properties enumerated effect facet is a grouping of characteristics unique to the effects of ac... |
| **PropertyReadEffectFacet** | uco.observable | Facet | A properties read effect facet is a grouping of characteristics unique to the effects of actions ... |
| **ReparsePoint** | uco.observable | Class | A reparse point is a type of NTFS (New Technology File System) object which is an optional attrib... |
| **SecurityAppliance** | uco.observable | Class | A security appliance is a purpose-built computer with software or firmware that is designed to pr... |
| **Semaphore** | uco.observable | Class | A semaphore is a variable or abstract data type used to control access to a common resource by mu... |
| **SendControlCodeEffectFacet** | uco.observable | Facet | A send control code effect facet is a grouping of characteristics unique to the effects of action... |
| **SmartDevice** | uco.observable | Class | A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-... |
| **Socket** | uco.observable | Class | A socket is a special file used for inter-process communication, which enables communication betw... |
| **Software** | uco.observable | Class | Software is a definitely scoped instance of a collection of data or computer instructions that te... |
| **SoftwareFacet** | uco.observable | Facet | A software facet is a grouping of characteristics unique to a software program (a definitively sc... |
| **Tool** | uco.tool | Class | A tool is an element of hardware and/or software utilized to carry out a particular function. |
| **ToolCapability** | ext.toolcap | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |
| **TriggerType** | uco.observable | Class | A trigger type is a grouping of characterizes unique to a set of criteria that, when met, starts ... |
| **UNIXAccount** | uco.observable | Class | A UNIX account is an account on a UNIX operating system. |
| **UNIXAccountFacet** | uco.observable | Facet | A UNIX account facet is a grouping of characteristics unique to an account on a UNIX operating sy... |
| **UNIXFile** | uco.observable | Class | A UNIX file is a file pertaining to the UNIX operating system. |
| **UNIXProcess** | uco.observable | Class | A UNIX process is an instance of a computer program executed on a UNIX operating system. |
| **UNIXProcessFacet** | uco.observable | Facet | A UNIX process facet is a grouping of characteristics unique to an instance of a computer program... |
| **URLHistory** | uco.observable | Class | A URL history characterizes the stored URL history for a particular web browser |
| **URLHistoryEntry** | uco.observable | Class | A URL history entry is a grouping of characteristics unique to the properties of a single URL his... |
| **URLHistoryFacet** | uco.observable | Facet | A URL history facet is a grouping of characteristics unique to the stored URL history for a parti... |
| **URLVisit** | uco.observable | Class | A URL visit characterizes the properties of a visit of a URL within a particular browser. |
| **URLVisitFacet** | uco.observable | Facet | A URL visit facet is a grouping of characteristics unique to the properties of a visit of a URL w... |
| **WebPage** | uco.observable | Class | A web page is a specific collection of information provided by a website and displayed to a user ... |
| **Wiki** | uco.observable | Class | A wiki is an online hypertext publication collaboratively edited and managed by its own audience ... |
| **WindowsAccount** | uco.observable | Class | A Windows account is a user account on a Windows operating system. |
| **WindowsAccountFacet** | uco.observable | Facet | A Windows account facet is a grouping of characteristics unique to a user account on a Windows op... |
| **WindowsActiveDirectoryAccount** | uco.observable | Class | A Windows Active Directory account is an account managed by directory-based identity-related serv... |
| **WindowsActiveDirectoryAccountFacet** | uco.observable | Facet | A Windows Active Directory account facet is a grouping of characteristics unique to an account ma... |
| **WindowsComputerSpecification** | uco.observable | Class | A Windows computer specification is the hardware ans software of a programmable electronic device... |
| **WindowsComputerSpecificationFacet** | uco.observable | Facet | A Windows computer specification facet is a grouping of characteristics unique to the hardware an... |
| **WindowsCriticalSection** | uco.observable | Class | A Windows critical section is a Windows object that provides synchronization similar to that prov... |
| **WindowsEvent** | uco.observable | Class | A Windows event is a notification record of an occurance of interest (system, security, applicati... |
| **WindowsFilemapping** | uco.observable | Class | A Windows file mapping is the association of a file's contents with a portion of the virtual addr... |
| **WindowsHandle** | uco.observable | Class | A Windows handle is an abstract reference to a resource within the Windows operating system, such... |
| **WindowsHook** | uco.observable | Class | A Windows hook is a mechanism by which an application can intercept events, such as messages, mou... |
| **WindowsNetworkShare** | uco.observable | Class | A Windows network share is a Windows computer resource made available from one host to other host... |
| **WindowsPEBinaryFile** | uco.observable | Class | A Windows PE binary file is a Windows portable executable (PE) file. |
| **WindowsPEBinaryFileFacet** | uco.observable | Facet | A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable exec... |
| **WindowsPEFileHeader** | uco.observable | Class | A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE ... |
| **WindowsPEOptionalHeader** | uco.observable | Class | A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of ... |
| **WindowsPESection** | uco.observable | Class | A Windows PE section is a grouping of characteristics unique to a specific default or custom-defi... |
| **WindowsPrefetch** | uco.observable | Class | The Windows prefetch contains entries in a Windows prefetch file (used to speed up application st... |
| **WindowsPrefetchFacet** | uco.observable | Facet | A Windows prefetch facet is a grouping of characteristics unique to entries in the Windows prefet... |
| **WindowsProcess** | uco.observable | Class | A Windows process is a program running on a Windows operating system. |
| **WindowsProcessFacet** | uco.observable | Facet | A Windows process facet is a grouping of characteristics unique to a program running on a Windows... |
| **WindowsRegistryHive** | uco.observable | Class | The Windows registry hive is a particular logical group of keys, subkeys, and values in a Windows... |
| **WindowsRegistryHiveFacet** | uco.observable | Facet | A Windows registry hive facet is a grouping of characteristics unique to a particular logical gro... |
| **WindowsRegistryKey** | uco.observable | Class | A Windows registry key is a particular key within a Windows registry (a hierarchical database tha... |
| **WindowsRegistryKeyFacet** | uco.observable | Facet | A Windows registry key facet is a grouping of characteristics unique to a particular key within a... |
| **WindowsRegistryValue** | uco.observable | Class | A Windows registry value is a grouping of characteristics unique to a particular value within a W... |
| **WindowsService** | uco.observable | Class | A Windows service is a specific Windows service (a computer program that operates in the backgrou... |
| **WindowsServiceFacet** | uco.observable | Facet | A Windows service facet is a grouping of characteristics unique to a specific Windows service (a ... |
| **WindowsSystemRestore** | uco.observable | Class | A Windows system restore is a capture of a Windows computer's state (including system files, inst... |
| **WindowsTask** | uco.observable | Class | A Windows task is a process that is scheduled to execute on a Windows operating system by the Win... |
| **WindowsTaskFacet** | uco.observable | Facet | A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is... |
| **WindowsThread** | uco.observable | Class | A Windows thread is a single thread of execution within a Windows process. |
| **WindowsThreadFacet** | uco.observable | Facet | A Windows thread facet is a grouping os characteristics unique to a single thread of execution wi... |
| **WindowsWaitableTime** | uco.observable | Class | A Windows waitable timer is a synchronization object within the Windows operating system whose st... |

**API** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**AnalyticTool** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 8 more* | | |

**AndroidDevice** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, ApplicationFacet

graph.create(ObservableObject, has_facet=[
    ApplicationFacet(application_identifier="com.example.app")
])
```

## User Accounts and Identity

Classes for user accounts, identities, organizations, and authentication artifacts. Use these when documenting who was involved, what accounts existed, or organizational relationships.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **Account** | uco.observable | Class | An account is an arrangement with an entity to enable and control the provision of some capabilit... |
| **AccountAuthenticationFacet** | uco.observable | Facet | An account authentication facet is a grouping of characteristics unique to the mechanism of acces... |
| **AccountFacet** | uco.observable | Facet | An account facet is a grouping of characteristics unique to an arrangement with an entity to enab... |
| **AddressFacet** | uco.identity | Facet | An address facet is a grouping of characteristics unique to an administrative identifier for a ge... |
| **AffiliationFacet** | uco.identity | Facet | An affiliation is a grouping of characteristics unique to the established affiliations of an entity. |
| **Application** | uco.observable | Class | An application is a particular software program designed for end users. |
| **ApplicationAccount** | uco.observable | Class | An application account is an account within a particular software program designed for end users. |
| **ApplicationAccountFacet** | uco.observable | Facet | An application account facet is a grouping of characteristics unique to an account within a parti... |
| **ApplicationFacet** | uco.observable | Facet | An application facet is a grouping of characteristics unique to a particular software program des... |
| **BirthInformationFacet** | uco.identity | Facet | Birth information is a grouping of characteristics unique to information pertaining to the birth ... |
| **BrowserCookie** | uco.observable | Class | A browser cookie is a piece of of data sent from a website and stored on the user's computer by t... |
| **BrowserCookieFacet** | uco.observable | Facet | A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a web... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **ContactAffiliation** | uco.observable | Class | A contact affiliation is a grouping of characteristics unique to details of an organizational aff... |
| **ContactProfile** | uco.observable | Class | A contact profile is a grouping of characteristics unique to details for contacting a contact ent... |
| **ContextualCompilation** | uco.core | Class | A contextual compilation is a grouping of things sharing some context (e.g., a set of network con... |
| **CountryOfResidenceFacet** | uco.identity | Facet | Country of residence is a grouping of characteristics unique to information related to the countr... |
| **Credential** | uco.observable | Class | A credential is a single specific login and password combination for authorization of access to a... |
| **CredentialDump** | uco.observable | Class | A credential dump is a collection (typically forcibly extracted from a system) of specific login ... |
| **DigitalAccount** | uco.observable | Class | A digital account is an arrangement with an entity to enable and control the provision of some ca... |
| **DigitalAccountFacet** | uco.observable | Facet | A digital account facet is a grouping of characteristics unique to an arrangement with an entity ... |
| **Directory** | uco.observable | Class | A directory is a file system cataloging structure which contains references to other computer fil... |
| **EmailAccount** | uco.observable | Class | An email account is an arrangement with an entity to enable and control the provision of electron... |
| **EmailAccountFacet** | uco.observable | Facet | An email account facet is a grouping of characteristics unique to an arrangement with an entity t... |
| **EmailAddress** | uco.observable | Class | An email address is an identifier for an electronic mailbox to which electronic mail messages (co... |
| **EmailAddressFacet** | uco.observable | Facet | An email address facet is a grouping of characteristics unique to an identifier for an electronic... |
| **EventsFacet** | uco.identity | Facet | Events is a grouping of characteristics unique to information related to specific relevant things... |
| **ForumPost** | uco.observable | Class | A forum post is message submitted by a user account to an online forum where the message content ... |
| **ForumPrivateMessage** | uco.observable | Class | A forum private message (aka PM or DM (direct message)) is a one-to-one message from one specific... |
| **GUI** | uco.observable | Class | A GUI is a graphical user interface that allows users to interact with electronic devices through... |
| **IdentifierFacet** | uco.identity | Facet | Identifier is a grouping of characteristics unique to information that uniquely and specifically ... |
| **Identity** | uco.identity | Class | An identity is a grouping of identifying characteristics unique to an individual or organization. |
| **IdentityAbstraction** | uco.core | Class | An identity abstraction is a grouping of identifying characteristics unique to an individual or o... |
| **IdentityFacet** | uco.identity | Facet | An identity facet is a grouping of characteristics unique to a particular aspect of an identity. |
| **LanguagesFacet** | uco.identity | Facet | Languages is a grouping of characteristics unique to specific syntactically and grammatically sta... |
| **Laptop** | uco.observable | Class | A laptop, laptop computer, or notebook computer is a small, portable personal computer with a scr... |
| **MobileAccount** | uco.observable | Class | A mobile account is an arrangement with an entity to enable and control the provision of some cap... |
| **MobileAccountFacet** | uco.observable | Facet | A mobile account facet is a grouping of characteristics unique to an arrangement with an entity t... |
| **MobilePhone** | uco.observable | Class | A mobile phone is a portable telephone that at least can make and receive calls over a radio freq... |
| **NationalityFacet** | uco.identity | Facet | Nationality is a grouping of characteristics unique to the condition of an entity belonging to a ... |
| **OccupationFacet** | uco.identity | Facet | Occupation is a grouping of characteristics unique to the job or profession of an entity. |
| **Organization** | uco.identity | Class | An organization is a grouping of identifying characteristics unique to a group of people who work... |
| **OrganizationDetailsFacet** | uco.identity | Facet | Organization details is a grouping of characteristics unique to an identity representing an admin... |
| **PaymentCard** | uco.observable | Class | A payment card is a physical token that is part of a payment system issued by financial instituti... |
| **Person** | uco.identity | Class | A person is a grouping of identifying characteristics unique to a human being regarded as an indi... |
| **PersonalDetailsFacet** | uco.identity | Facet | Personal details is a grouping of characteristics unique to an identity representing an individua... |
| **PhoneAccount** | uco.observable | Class | A phone account is an arrangement with an entity to enable and control the provision of a telepho... |
| **PhoneAccountFacet** | uco.observable | Facet | A phone account facet is a grouping of characteristics unique to an arrangement with an entity to... |
| **PhysicalInfoFacet** | uco.identity | Facet | Physical info is a grouping of characteristics unique to the outwardly observable nature of an in... |
| **Profile** | uco.observable | Class | A profile is an explicit digital representation of identity and characteristics of the owner of a... |
| **ProfileFacet** | uco.observable | Facet | A profile facet is a grouping of characteristics unique to an explicit digital representation of ... |
| **QualificationFacet** | uco.identity | Facet | Qualification is a grouping of characteristics unique to particular skills, capabilities or their... |
| **RelatedIdentityFacet** | uco.identity | Facet | <Needs fleshed out from CIQ> |
| **ReleaseToMarking** | uco.marking | Class | A release-to marking is a grouping of characteristics unique to the expression of data marking de... |
| **SIMCard** | uco.observable | Class | A SIM card is a subscriber identification module card intended to securely store the internationa... |
| **SIMCardFacet** | uco.observable | Facet | A SIM card facet is a grouping of characteristics unique to a subscriber identification module ca... |
| **SIPAddressFacet** | uco.observable | Facet | A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP... |
| **SimpleNameFacet** | uco.identity | Facet | A simple name facet is a grouping of characteristics unique to the personal name (e.g., Dr. John ... |
| **Tweet** | uco.observable | Class | A tweet is message submitted by a Twitter user account to the Twitter microblogging platform. |
| **TwitterProfileFacet** | uco.observable | Facet | A twitter profile facet is a grouping of characteristics unique to an explicit digital representa... |
| **UNIXAccount** | uco.observable | Class | A UNIX account is an account on a UNIX operating system. |
| **UNIXAccountFacet** | uco.observable | Facet | A UNIX account facet is a grouping of characteristics unique to an account on a UNIX operating sy... |
| **UserAccount** | uco.observable | Class | A user account is an account controlling a user's access to a network, system or platform. |
| **UserAccountFacet** | uco.observable | Facet | A user account facet is a grouping of characteristics unique to an account controlling a user's a... |
| **UserSession** | uco.observable | Class | A user session is a temporary and interactive information interchange between two or more communi... |
| **UserSessionFacet** | uco.observable | Facet | A user session facet is a grouping of characteristics unique to a temporary and interactive infor... |
| **Victim** | uco.victim | Class | A victim is a role played by a person or organization that is/was the target of some malicious ac... |
| **VictimTargeting** | uco.victim | Class | A victim targeting is a grouping of characteristics unique to people or organizations that are th... |
| **VisaFacet** | uco.identity | Facet | Visa is a grouping of characteristics unique to information related to a person's ability to ente... |
| **WearableDevice** | uco.observable | Class | A wearable device is an electronic device that is designed to be worn on a person's body. |
| **WebPage** | uco.observable | Class | A web page is a specific collection of information provided by a website and displayed to a user ... |
| **Wiki** | uco.observable | Class | A wiki is an online hypertext publication collaboratively edited and managed by its own audience ... |
| **WindowsAccount** | uco.observable | Class | A Windows account is a user account on a Windows operating system. |
| **WindowsAccountFacet** | uco.observable | Facet | A Windows account facet is a grouping of characteristics unique to a user account on a Windows op... |
| **WindowsActiveDirectoryAccount** | uco.observable | Class | A Windows Active Directory account is an account managed by directory-based identity-related serv... |
| **WindowsActiveDirectoryAccountFacet** | uco.observable | Facet | A Windows Active Directory account facet is a grouping of characteristics unique to an account ma... |
| **X509Certificate** | uco.observable | Class | A X.509 certificate is a public key digital identity certificate conformant to the X.509 PKI (Pub... |
| **X509CertificateFacet** | uco.observable | Facet | A X.509 certificate facet is a grouping of characteristics unique to a public key digital identit... |
| **X509V3Certificate** | uco.observable | Class | An X.509 v3 certificate is a public key digital identity certificate conformant to the X.509 v3 P... |
| **X509V3ExtensionsFacet** | uco.observable | Facet | An X.509 v3 certificate extensions facet is a grouping of characteristics unique to a public key ... |

**Account** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Application** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ApplicationAccount** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, AccountFacet

graph.create(ObservableObject, has_facet=[
    AccountFacet(account_identifier="user123")
])
```

## Email and Messaging

Classes for email messages, SMS/MMS, chat messages, and communication metadata. Use these when modeling extracted communications.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **AlternateDataStream** | uco.observable | Class | An alternate data stream is data content stored within an NTFS file that is independent of the st... |
| **AlternateDataStreamFacet** | uco.observable | Facet | An alternate data stream facet is a grouping of characteristics unique to data content stored wit... |
| **ContactEmail** | uco.observable | Class | A contact email is a grouping of characteristics unique to details for contacting a contact entit... |
| **DigitalSignatureInfo** | uco.observable | Class | A digital signature info is a value calculated via a mathematical scheme for demonstrating the au... |
| **DigitalSignatureInfoFacet** | uco.observable | Facet | A digital signature info facet is a grouping of characteristics unique to a value calculated via ... |
| **EmailAccount** | uco.observable | Class | An email account is an arrangement with an entity to enable and control the provision of electron... |
| **EmailAccountFacet** | uco.observable | Facet | An email account facet is a grouping of characteristics unique to an arrangement with an entity t... |
| **EmailAddress** | uco.observable | Class | An email address is an identifier for an electronic mailbox to which electronic mail messages (co... |
| **EmailAddressFacet** | uco.observable | Facet | An email address facet is a grouping of characteristics unique to an identifier for an electronic... |
| **EmailMessage** | uco.observable | Class | An email message is a message that is an instance of an electronic mail correspondence conformant... |
| **EmailMessageFacet** | uco.observable | Facet | An email message facet is a grouping of characteristics unique to a message that is an instance o... |
| **ForumPost** | uco.observable | Class | A forum post is message submitted by a user account to an online forum where the message content ... |
| **ForumPrivateMessage** | uco.observable | Class | A forum private message (aka PM or DM (direct message)) is a one-to-one message from one specific... |
| **GlobalFlagType** | uco.observable | Class | A global flag type is a grouping of characteristics unique to the Windows systemwide global varia... |
| **ICMPConnection** | uco.observable | Class | An ICMP connection is a network connection that is conformant to the Internet Control Message Pro... |
| **ICMPConnectionFacet** | uco.observable | Facet | An ICMP connection facet is a grouping of characteristics unique to portions of a network connect... |
| **IShowMessageActionType** | uco.observable | Class | An IShow message action type is a grouping of characteristics unique to an action that shows a me... |
| **Message** | uco.observable | Class | A message is a discrete unit of electronic communication intended by the source for consumption b... |
| **MessageFacet** | uco.observable | Facet | A message facet is a grouping of characteristics unique to a discrete unit of electronic communic... |
| **MessageThread** | uco.observable | Class | A message thread is a running commentary of electronic messages pertaining to one topic or question. |
| **MessageThreadFacet** | uco.observable | Facet | A message thread facet is a grouping of characteristics unique to a running commentary of electro... |
| **MimePartType** | uco.observable | Class | A mime part type is a grouping of characteristics unique to a component of a multi-part email body. |
| **Pipe** | uco.observable | Class | A pipe is a mechanism for one-way inter-process communication using message passing where data wr... |
| **Post** | uco.observable | Class | A post is message submitted to an online discussion/publishing site (forum, blog, etc.). |
| **SMSMessage** | uco.observable | Class | An SMS message is a message conformant to the short message service (SMS) communication protocol ... |
| **SMSMessageFacet** | uco.observable | Facet | A SMS message facet is a grouping of characteristics unique to a message conformant to the short ... |
| **Subject** | case.investigation | Class | Subject is a role whose conduct is within the scope of an investigation. |
| **SubjectActionLifecycle** | case.investigation | Class | A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions ... |
| **Tweet** | uco.observable | Class | A tweet is message submitted by a Twitter user account to the Twitter microblogging platform. |
| **Wiki** | uco.observable | Class | A wiki is an online hypertext publication collaboratively edited and managed by its own audience ... |
| **WindowsHook** | uco.observable | Class | A Windows hook is a mechanism by which an application can intercept events, such as messages, mou... |
| **WindowsMailslot** | uco.observable | Class | A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard ... |

**AlternateDataStream** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ContactEmail** key properties:

| Property | Type | Required |
|----------|------|----------|
| contactEmailScope | string | No |
| emailAddress | ObservableObject | No |

**DigitalSignatureInfo** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, EmailMessageFacet

graph.create(ObservableObject, has_facet=[
    EmailMessageFacet(subject="Important evidence")
])
```

## Mobile Forensics

Classes specific to mobile device forensics: SIM cards, contacts, call logs, calendar entries, and cellular network artifacts.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **API** | uco.observable | Class | An API (application programming interface) is a computing interface that defines interactions bet... |
| **Adaptor** | uco.observable | Class | An adaptor is a device that physically converts the pin outputs but does not alter the underlying... |
| **AddressFacet** | uco.identity | Facet | An address facet is a grouping of characteristics unique to an administrative identifier for a ge... |
| **AndroidPhone** | uco.observable | Class | An android phone is a smart phone that applies the Android mobile operating system. |
| **AntennaFacet** | uco.observable | Facet | An antenna alignment facet contains the metadata surrounding the cell tower's antenna position. |
| **BlackberryPhone** | uco.observable | Class | A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blac... |
| **BluetoothAddress** | uco.observable | Class | A Bluetooth address is a Bluetooth standard conformant identifier assigned to a Bluetooth device ... |
| **BluetoothAddressFacet** | uco.observable | Facet | A Bluetooth address facet is a grouping of characteristics unique to a Bluetooth standard conform... |
| **Calendar** | uco.observable | Class | A calendar is a collection of appointments, meetings, and events. |
| **CalendarEntry** | uco.observable | Class | A calendar entry is an appointment, meeting or event within a collection of appointments, meeting... |
| **CalendarEntryFacet** | uco.observable | Facet | A calendar entry facet is a grouping of characteristics unique to an appointment, meeting, or eve... |
| **CalendarFacet** | uco.observable | Facet | A calendar facet is a grouping of characteristics unique to a collection of appointments, meeting... |
| **Call** | uco.observable | Class | A call is a connection as part of a realtime cyber communication between one or more parties. |
| **CallFacet** | uco.observable | Facet | A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber ... |
| **CellSite** | uco.observable | Class |  |
| **CellSiteFacet** | uco.observable | Facet | A cell site facet contains the metadata surrounding the cell site. |
| **CompilerType** | uco.tool | Class | A compiler type is a grouping of characteristics unique to a specific program that translates com... |
| **Computer** | uco.observable | Class | A computer is an electronic device for storing and processing data, typically in binary, accordin... |
| **Contact** | uco.observable | Class | A contact is a set of identification and communication related details for a single entity. |
| **ContactAddress** | uco.observable | Class | A contact address is a grouping of characteristics unique to a geolocation address of a contact e... |
| **ContactAffiliation** | uco.observable | Class | A contact affiliation is a grouping of characteristics unique to details of an organizational aff... |
| **ContactEmail** | uco.observable | Class | A contact email is a grouping of characteristics unique to details for contacting a contact entit... |
| **ContactFacet** | uco.observable | Facet | A contact facet is a grouping of characteristics unique to a set of identification and communicat... |
| **ContactList** | uco.observable | Class | A contact list is a set of multiple individual contacts such as that found in a digital address b... |
| **ContactListFacet** | uco.observable | Facet | A contact list facet is a grouping of characteristics unique to a set of multiple individual cont... |
| **ContactMessaging** | uco.observable | Class | A contact messaging is a grouping of characteristics unique to details for contacting a contact e... |
| **ContactPhone** | uco.observable | Class | A contact phone is a grouping of characteristics unique to details for contacting a contact entit... |
| **ContactProfile** | uco.observable | Class | A contact profile is a grouping of characteristics unique to details for contacting a contact ent... |
| **ContactSIP** | uco.observable | Class | A contact SIP is a grouping of characteristics unique to details for contacting a contact entity ... |
| **ContactURL** | uco.observable | Class | A contact URL is a grouping of characteristics unique to details for contacting a contact entity ... |
| **CredentialDump** | uco.observable | Class | A credential dump is a collection (typically forcibly extracted from a system) of specific login ... |
| **DNSCache** | uco.observable | Class | An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query ... |
| **Drone** | uco.observable | Class | A drone, unmanned aerial vehicle (UAV), is an aircraft without a human pilot, crew, or passengers... |
| **EXIFFacet** | uco.observable | Facet | An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the for... |
| **EmailAddress** | uco.observable | Class | An email address is an identifier for an electronic mailbox to which electronic mail messages (co... |
| **EmailAddressFacet** | uco.observable | Facet | An email address facet is a grouping of characteristics unique to an identifier for an electronic... |
| **ForumPost** | uco.observable | Class | A forum post is message submitted by a user account to an online forum where the message content ... |
| **GPSCoordinatesFacet** | uco.location | Facet | A GPS coordinates facet is a grouping of characteristics unique to the expression of quantified d... |
| **GamingConsole** | uco.observable | Class | A gaming console (video game console or game console) is an electronic system that connects to a ... |
| **GeoLocationEntry** | uco.observable | Class | A geolocation entry is a single application-specific geolocation entry. |
| **GeoLocationEntryFacet** | uco.observable | Facet | A geolocation entry facet is a grouping of characteristics unique to a single application-specifi... |
| **GeoLocationLog** | uco.observable | Class | A geolocation log is a record containing geolocation tracks and/or geolocation entries. |
| **GeoLocationLogFacet** | uco.observable | Facet | A geolocation log facet is a grouping of characteristics unique to a record containing geolocatio... |
| **GeoLocationTrack** | uco.observable | Class | A geolocation track is a set of contiguous geolocation entries representing a path/track taken. |
| **GeoLocationTrackFacet** | uco.observable | Facet | A geolocation track facet is a grouping of characteristics unique to a set of contiguous geolocat... |
| **Hash** | uco.types | Class | A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm... |
| **IComHandlerActionType** | uco.observable | Class | An IComHandler action type is a grouping of characteristics unique to a Windows Task-related acti... |
| **IPhone** | uco.observable | Class | An iPhone is a smart phone that applies the iOS mobile operating system. |
| **IdentifierFacet** | uco.identity | Facet | Identifier is a grouping of characteristics unique to information that uniquely and specifically ... |
| **InvestigativeAction** | case.investigation | Class | An investigative action is something that may be done or performed within the context of an inves... |
| **Junction** | uco.observable | Class | A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory ... |
| **LanguagesFacet** | uco.identity | Facet | Languages is a grouping of characteristics unique to specific syntactically and grammatically sta... |
| **Laptop** | uco.observable | Class | A laptop, laptop computer, or notebook computer is a small, portable personal computer with a scr... |
| **LatLongCoordinatesFacet** | uco.location | Facet | A lat long coordinates facet is a grouping of characteristics unique to the expression of a geolo... |
| **Location** | uco.location | Class | A location is a geospatial place, site, or position. |
| **MobileAccount** | uco.observable | Class | A mobile account is an arrangement with an entity to enable and control the provision of some cap... |
| **MobileAccountFacet** | uco.observable | Facet | A mobile account facet is a grouping of characteristics unique to an arrangement with an entity t... |
| **MobileDevice** | uco.observable | Class | A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobil... |
| **MobileDeviceFacet** | uco.observable | Facet | A mobile device facet is a grouping of characteristics unique to a portable computing device. [ba... |
| **MobilePhone** | uco.observable | Class | A mobile phone is a portable telephone that at least can make and receive calls over a radio freq... |
| **NamedPipe** | uco.observable | Class | A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is pers... |
| **PathRelationFacet** | uco.observable | Facet | A path relation facet is a grouping of characteristics unique to the location of one object withi... |
| **PhoneAccount** | uco.observable | Class | A phone account is an arrangement with an entity to enable and control the provision of a telepho... |
| **PhoneAccountFacet** | uco.observable | Facet | A phone account facet is a grouping of characteristics unique to an arrangement with an entity to... |
| **ProcessThread** | uco.observable | Class | A process thread is the smallest sequence of programmed instructions that can be managed independ... |
| **ProvenanceRecord** | case.investigation | Class | A provenance record is a grouping of characteristics unique to the provenantial (chronology of th... |
| **SIMCard** | uco.observable | Class | A SIM card is a subscriber identification module card intended to securely store the internationa... |
| **SIMCardFacet** | uco.observable | Facet | A SIM card facet is a grouping of characteristics unique to a subscriber identification module ca... |
| **SimpleAddressFacet** | uco.location | Facet | A simple address facet is a grouping of characteristics unique to a geolocation expressed as an a... |
| **SimpleNameFacet** | uco.identity | Facet | A simple name facet is a grouping of characteristics unique to the personal name (e.g., Dr. John ... |
| **SmartDevice** | uco.observable | Class | A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-... |
| **SmartPhone** | uco.observable | Class | A smartphone is a portable device that combines mobile telephone and computing functions into one... |
| **Socket** | uco.observable | Class | A socket is a special file used for inter-process communication, which enables communication betw... |
| **StatementMarking** | uco.marking | Class | A statement marking is a grouping of characteristics unique to the expression of data marking def... |
| **Tablet** | uco.observable | Class | A tablet is a mobile computer that is primarily operated by touching the screen. (Devices categor... |
| **TermsOfUseMarking** | uco.marking | Class | A terms of use marking is a grouping of characteristics unique to the expression of data marking ... |
| **Thread** | uco.types | Class | A semi-ordered array of items, that can be present in multiple copies.  Implemetation of a UCO Th... |
| **WebPage** | uco.observable | Class | A web page is a specific collection of information provided by a website and displayed to a user ... |
| **WhoisContactFacet** | uco.observable | Facet | A Whois contact type is a grouping of characteristics unique to contact-related information prese... |
| **WindowsCriticalSection** | uco.observable | Class | A Windows critical section is a Windows object that provides synchronization similar to that prov... |
| **WindowsFilemapping** | uco.observable | Class | A Windows file mapping is the association of a file's contents with a portion of the virtual addr... |
| **WindowsService** | uco.observable | Class | A Windows service is a specific Windows service (a computer program that operates in the backgrou... |
| **WindowsServiceFacet** | uco.observable | Facet | A Windows service facet is a grouping of characteristics unique to a specific Windows service (a ... |
| **WriteBlocker** | uco.observable | Class | A write blocker is a device that allows read-only access to storage mediums in order to preserve ... |

**API** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Adaptor** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**AndroidPhone** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.observable import ObservableObject, SIMCardFacet

graph.create(ObservableObject, has_facet=[
    SIMCardFacet(icc_id="8901260123456789012")
])
```

## Actions and Events

Classes for modeling actions taken during an investigation or actions performed by software/users that are relevant to the case. Includes action lifecycle tracking and patterns.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **API** | uco.observable | Class | An API (application programming interface) is a computing interface that defines interactions bet... |
| **Action** | uco.action | Class | An action is something that may be done or performed. |
| **ActionArgumentFacet** | uco.action | Facet | An action argument facet is a grouping of characteristics unique to a single parameter of an action. |
| **ActionEstimationFacet** | uco.action | Facet | An action estimation facet is a grouping of characteristics unique to decision-focused approximat... |
| **ActionFrequencyFacet** | uco.action | Facet | An action frequency facet is a grouping of characteristics unique to the frequency of occurrence ... |
| **ActionLifecycle** | uco.action | Class | An action lifecycle is an action pattern consisting of an ordered set of multiple actions or subo... |
| **ActionPattern** | uco.action | Class | An action pattern is a grouping of characteristics unique to a combination of actions forming a c... |
| **AnalyticResultFacet** | uco.analysis | Facet | An analytic result facet is a grouping of characteristics unique to the results of an analysis ac... |
| **ArrayOfAction** | uco.action | Class | An array of action is an ordered list of references to things that may be done or performed. |
| **ArtifactClassificationResultFacet** | uco.analysis | Facet | An artifact classification result facet is a grouping of characteristics unique to the results of... |
| **Authorization** | case.investigation | Class | An authorization is a grouping of characteristics unique to some form of authoritative permission... |
| **Calendar** | uco.observable | Class | A calendar is a collection of appointments, meetings, and events. |
| **CalendarEntry** | uco.observable | Class | A calendar entry is an appointment, meeting or event within a collection of appointments, meeting... |
| **CalendarEntryFacet** | uco.observable | Facet | A calendar entry facet is a grouping of characteristics unique to an appointment, meeting, or eve... |
| **CalendarFacet** | uco.observable | Facet | A calendar facet is a grouping of characteristics unique to a collection of appointments, meeting... |
| **DNSCache** | uco.observable | Class | An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query ... |
| **DefinedEffectFacet** | uco.observable | Facet | A defined effect facet is a grouping of characteristics unique to the effect of an observable act... |
| **Device** | uco.observable | Class | A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a ... |
| **DeviceFacet** | uco.observable | Facet | A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism des... |
| **EnvironmentVariable** | uco.observable | Class | An environment variable is a grouping of characteristics unique to a dynamic-named value that can... |
| **Event** | uco.core | Class | An Event is a noteworthy occurrence (something that happens or might happen). |
| **EventLog** | uco.observable | Class | An event log is a collection of event records. |
| **EventRecord** | uco.observable | Class | An event record is something that happens in a digital context (e.g., operating system events). |
| **EventRecordFacet** | uco.observable | Facet | An event record facet is a grouping of characteristics unique to something that happens in a digi... |
| **EventsFacet** | uco.identity | Facet | Events is a grouping of characteristics unique to information related to specific relevant things... |
| **FilePermissionsFacet** | uco.observable | Facet | A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view... |
| **Hash** | uco.types | Class | A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm... |
| **IComHandlerActionType** | uco.observable | Class | An IComHandler action type is a grouping of characteristics unique to a Windows Task-related acti... |
| **IExecActionType** | uco.observable | Class | An IExec action type is a grouping of characteristics unique to an action that executes a command... |
| **IShowMessageActionType** | uco.observable | Class | An IShow message action type is a grouping of characteristics unique to an action that shows a me... |
| **IdentityAbstraction** | uco.core | Class | An identity abstraction is a grouping of identifying characteristics unique to an individual or o... |
| **InvestigativeAction** | case.investigation | Class | An investigative action is something that may be done or performed within the context of an inves... |
| **MarkingDefinitionAbstraction** | uco.core | Class | A marking definition abstraction is a grouping of characteristics unique to the expression of a s... |
| **NTFSFilePermissionsFacet** | uco.observable | Facet | An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g.... |
| **Observable** | uco.observable | Class | An observable is a characterizable item or action within the digital domain. |
| **ObservableAction** | uco.observable | Class | An observable action is a grouping of characteristics unique to something that may be done or per... |
| **ObservablePattern** | uco.observable | Class | An observable pattern is a grouping of characteristics unique to a logical pattern composed of ob... |
| **Process** | uco.observable | Class | A process is an instance of a computer program executed on an operating system. |
| **ProcessFacet** | uco.observable | Facet | A process facet is a grouping of characteristics unique to an instance of a computer program exec... |
| **PropertiesEnumeratedEffectFacet** | uco.observable | Facet | A properties enumerated effect facet is a grouping of characteristics unique to the effects of ac... |
| **PropertyReadEffectFacet** | uco.observable | Facet | A properties read effect facet is a grouping of characteristics unique to the effects of actions ... |
| **ProvenanceRecord** | case.investigation | Class | A provenance record is a grouping of characteristics unique to the provenantial (chronology of th... |
| **RecoveredObject** | uco.observable | Class | An observable object that was the result of a recovery operation. |
| **SendControlCodeEffectFacet** | uco.observable | Facet | A send control code effect facet is a grouping of characteristics unique to the effects of action... |
| **StateChangeEffectFacet** | uco.observable | Facet | A state change effect facet is a grouping of characteristics unique to the effects of actions upo... |
| **StorageMediumFacet** | uco.observable | Facet | A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a... |
| **SubjectActionLifecycle** | case.investigation | Class | A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions ... |
| **TaskActionType** | uco.observable | Class | A task action type is a grouping of characteristics for a scheduled action to be completed. |
| **UNIXFilePermissionsFacet** | uco.observable | Facet | A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g.,... |
| **UNIXProcess** | uco.observable | Class | A UNIX process is an instance of a computer program executed on a UNIX operating system. |
| **UNIXProcessFacet** | uco.observable | Facet | A UNIX process facet is a grouping of characteristics unique to an instance of a computer program... |
| **ValuesEnumeratedEffectFacet** | uco.observable | Facet | A values enumerated effect facet is a grouping of characteristics unique to the effects of action... |
| **Victim** | uco.victim | Class | A victim is a role played by a person or organization that is/was the target of some malicious ac... |
| **VictimActionLifecycle** | case.investigation | Class | A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions o... |
| **WindowsCriticalSection** | uco.observable | Class | A Windows critical section is a Windows object that provides synchronization similar to that prov... |
| **WindowsEvent** | uco.observable | Class | A Windows event is a notification record of an occurance of interest (system, security, applicati... |
| **WindowsHook** | uco.observable | Class | A Windows hook is a mechanism by which an application can intercept events, such as messages, mou... |
| **WindowsSystemRestore** | uco.observable | Class | A Windows system restore is a capture of a Windows computer's state (including system files, inst... |
| **WindowsTask** | uco.observable | Class | A Windows task is a process that is scheduled to execute on a Windows operating system by the Win... |
| **WindowsTaskFacet** | uco.observable | Facet | A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is... |

**API** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Action** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 16 more* | | |

**ActionLifecycle** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 17 more* | | |

**Example usage:**

```python
from case_uco.uco.action import Action

graph.create(Action, name="Disk Imaging", description="Created forensic image")
```

## Investigation Metadata

CASE-specific classes for structuring an investigation: cases, investigative actions, provenance records, and authorization.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **Attorney** | case.investigation | Class | Attorney is a role involved in preparing, interpreting, and applying law. |
| **Authorization** | case.investigation | Class | An authorization is a grouping of characteristics unique to some form of authoritative permission... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **Credential** | uco.observable | Class | A credential is a single specific login and password combination for authorization of access to a... |
| **CredentialDump** | uco.observable | Class | A credential dump is a collection (typically forcibly extracted from a system) of specific login ... |
| **Dictionary** | uco.types | Class | A dictionary is list of (term/key, value) pairs with each term/key having an expectation to exist... |
| **Examiner** | case.investigation | Class | Examiner is a role involved in providing scientific evaluations of evidence that are used to aid ... |
| **Investigation** | case.investigation | Class | An investigation is a grouping of characteristics unique to an exploration of the facts involved ... |
| **InvestigativeAction** | case.investigation | Class | An investigative action is something that may be done or performed within the context of an inves... |
| **Investigator** | case.investigation | Class | Investigator is a role involved in coordinating an investigation. |
| **ProvenanceRecord** | case.investigation | Class | A provenance record is a grouping of characteristics unique to the provenantial (chronology of th... |
| **Subject** | case.investigation | Class | Subject is a role whose conduct is within the scope of an investigation. |
| **SubjectActionLifecycle** | case.investigation | Class | A subject action lifecycle is an action pattern consisting of an ordered set of multiple actions ... |
| **ToolCapability** | ext.toolcap | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |
| **VictimActionLifecycle** | case.investigation | Class | A victim action lifecycle is an action pattern consisting of an ordered set of multiple actions o... |

**Attorney** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 3 more* | | |

**Authorization** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 7 more* | | |

**CapabilityMatrix** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 6 more* | | |

**Example usage:**

```python
from case_uco.case.investigation import Investigation, InvestigativeAction

graph.create(Investigation, name="Case 2024-001")
graph.create(InvestigativeAction, name="Device Acquisition")
```

## Tool Information

Classes for documenting forensic tools, their versions, build information, and configuration. Use these to record provenance about which tools produced the data.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **API** | uco.observable | Class | An API (application programming interface) is a computing interface that defines interactions bet... |
| **AnalyticTool** | uco.tool | Class | An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purp... |
| **Appliance** | uco.observable | Class | An appliance is a purpose-built computer with software or firmware that is designed to provide a ... |
| **Application** | uco.observable | Class | An application is a particular software program designed for end users. |
| **ApplicationAccount** | uco.observable | Class | An application account is an account within a particular software program designed for end users. |
| **ApplicationAccountFacet** | uco.observable | Facet | An application account facet is a grouping of characteristics unique to an account within a parti... |
| **ApplicationFacet** | uco.observable | Facet | An application facet is a grouping of characteristics unique to a particular software program des... |
| **ApplicationVersion** | uco.observable | Class | An application version is a grouping of characteristics unique to a particular software program v... |
| **BotConfiguration** | uco.observable | Class | A bot configuration is a set of contextual settings for a software application that runs automate... |
| **BrowserBookmark** | uco.observable | Class | A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software progr... |
| **BrowserBookmarkFacet** | uco.observable | Facet | A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs... |
| **BuildFacet** | uco.tool | Facet | A build facet is a grouping of characteristics unique to a particular version of a software. |
| **BuildInformationType** | uco.tool | Class | A build information type is a grouping of characteristics that describe how a particular version ... |
| **BuildUtilityType** | uco.tool | Class | A build utility type characterizes the tool used to convert from source code to executable code f... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **Code** | uco.observable | Class | Code is a direct representation (source, byte or binary) of a collection of computer instructions... |
| **CompilerType** | uco.tool | Class | A compiler type is a grouping of characteristics unique to a specific program that translates com... |
| **ComputerSpecification** | uco.observable | Class | A computer specification is the hardware and software of a programmable electronic device that ca... |
| **ComputerSpecificationFacet** | uco.observable | Facet | A computer specificaiton facet is a grouping of characteristics unique to the hardware and softwa... |
| **Configuration** | uco.configuration | Class | A configuration is a grouping of characteristics unique to a set of parameters or initial setting... |
| **ConfigurationEntry** | uco.configuration | Class | A configuration entry is a grouping of characteristics unique to a particular parameter or initia... |
| **ConfiguredSoftware** | uco.observable | Class | A ConfiguredSoftware is a Software that is known to be configured to run in a more specified mann... |
| **ConfiguredTool** | uco.tool | Class | A ConfiguredTool is a Tool that is known to be configured to run in a more specified manner than ... |
| **DefensiveTool** | uco.tool | Class | A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purp... |
| **Dependency** | uco.configuration | Class | A dependency is a grouping of characteristics unique to something that a tool or other software r... |
| **EncodedStreamFacet** | uco.observable | Facet | An encoded stream facet is a grouping of characteristics unique to the conversion of a body of da... |
| **EncryptedStreamFacet** | uco.observable | Facet | An encrypted stream facet is a grouping of characteristics unique to the conversion of a body of ... |
| **IPv4Address** | uco.observable | Class | An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned... |
| **IPv4AddressFacet** | uco.observable | Facet | An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an... |
| **IPv6Address** | uco.observable | Class | An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned... |
| **IPv6AddressFacet** | uco.observable | Facet | An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an... |
| **Library** | uco.observable | Class | A library is a suite of data and programming code that is used to develop software programs and a... |
| **LibraryFacet** | uco.observable | Facet | A library facet is a grouping of characteristics unique to a suite of data and programming code t... |
| **LibraryType** | uco.tool | Class | A library type is a grouping of characteristics unique to a collection of resources incorporated ... |
| **MaliciousTool** | uco.tool | Class | A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent t... |
| **NetworkAppliance** | uco.observable | Class | A network appliance is a purpose-built computer with software or firmware that is designed to pro... |
| **NetworkInterface** | uco.observable | Class | A network interface is a software or hardware interface between two pieces of equipment or protoc... |
| **NetworkInterfaceFacet** | uco.observable | Facet | A network interface facet is a grouping of characteristics unique to a software or hardware inter... |
| **OperatingSystem** | uco.observable | Class | An operating system is the software that manages computer hardware, software resources, and provi... |
| **OperatingSystemFacet** | uco.observable | Facet | An operating system facet is a grouping of characteristics unique to the software that manages co... |
| **SecurityAppliance** | uco.observable | Class | A security appliance is a purpose-built computer with software or firmware that is designed to pr... |
| **Software** | uco.observable | Class | Software is a definitely scoped instance of a collection of data or computer instructions that te... |
| **SoftwareFacet** | uco.observable | Facet | A software facet is a grouping of characteristics unique to a software program (a definitively sc... |
| **Tool** | uco.tool | Class | A tool is an element of hardware and/or software utilized to carry out a particular function. |
| **ToolCapability** | ext.toolcap | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |
| **WindowsComputerSpecification** | uco.observable | Class | A Windows computer specification is the hardware ans software of a programmable electronic device... |
| **WindowsComputerSpecificationFacet** | uco.observable | Facet | A Windows computer specification facet is a grouping of characteristics unique to the hardware an... |

**API** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**AnalyticTool** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 8 more* | | |

**Appliance** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.tool import Tool

graph.create(Tool, name="My Forensic Tool", version="3.0")
```

## Time and Temporal Data

Classes for representing timestamps, time intervals, and temporal relationships between events.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **Call** | uco.observable | Class | A call is a connection as part of a realtime cyber communication between one or more parties. |
| **CallFacet** | uco.observable | Facet | A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber ... |
| **CapabilityMatrix** | ext.toolcap | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **Dictionary** | uco.types | Class | A dictionary is list of (term/key, value) pairs with each term/key having an expectation to exist... |
| **EventsFacet** | uco.identity | Facet | Events is a grouping of characteristics unique to information related to specific relevant things... |
| **InstantMessagingAddress** | uco.observable | Class |  |
| **InstantMessagingAddressFacet** | uco.observable | Facet | An instant messaging address facet is a grouping of characteristics unique to an identifier assig... |
| **Observation** | uco.observable | Class | An observation is a temporal perception of an observable. |
| **ProcessThread** | uco.observable | Class | A process thread is the smallest sequence of programmed instructions that can be managed independ... |
| **Snapshot** | uco.observable | Class | A snapshot is a file system object representing a snapshot of the contents of a part of a file sy... |
| **VisaFacet** | uco.identity | Facet | Visa is a grouping of characteristics unique to information related to a person's ability to ente... |
| **WindowsCriticalSection** | uco.observable | Class | A Windows critical section is a Windows object that provides synchronization similar to that prov... |
| **WindowsSystemRestore** | uco.observable | Class | A Windows system restore is a capture of a Windows computer's state (including system files, inst... |
| **WindowsWaitableTime** | uco.observable | Class | A Windows waitable timer is a synchronization object within the Windows operating system whose st... |

**Call** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**CapabilityMatrix** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 6 more* | | |

**Dictionary** key properties:

| Property | Type | Required |
|----------|------|----------|
| entry | DictionaryEntry | No |

**Example usage:**

```python
from case_uco.uco.time import Instant

graph.create(Instant)
```

## Marking and Access Control

Classes for marking data with handling restrictions, classification levels, TLP designations, and license information.

| Class | Module | Type | Description |
|-------|--------|------|-------------|
| **AccountAuthenticationFacet** | uco.observable | Facet | An account authentication facet is a grouping of characteristics unique to the mechanism of acces... |
| **AlternateDataStream** | uco.observable | Class | An alternate data stream is data content stored within an NTFS file that is independent of the st... |
| **AlternateDataStreamFacet** | uco.observable | Facet | An alternate data stream facet is a grouping of characteristics unique to data content stored wit... |
| **ArtifactClassification** | uco.analysis | Class | An artifact classification is a single specific assertion that a particular class of a classifica... |
| **ArtifactClassificationResultFacet** | uco.analysis | Facet | An artifact classification result facet is a grouping of characteristics unique to the results of... |
| **BlockDeviceNode** | uco.observable | Class | A block device node is a UNIX filesystem special file that serves as a conduit to communicate wit... |
| **BrowserBookmark** | uco.observable | Class | A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software progr... |
| **BrowserBookmarkFacet** | uco.observable | Facet | A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs... |
| **CharacterDeviceNode** | uco.observable | Class | A character device node is a UNIX filesystem special file that serves as a conduit to communicate... |
| **Credential** | uco.observable | Class | A credential is a single specific login and password combination for authorization of access to a... |
| **CredentialDump** | uco.observable | Class | A credential dump is a collection (typically forcibly extracted from a system) of specific login ... |
| **EXIFFacet** | uco.observable | Facet | An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the for... |
| **EmbeddedDevice** | uco.observable | Class | An embedded device is a highly specialized microprocessor device meant for one or very few specif... |
| **FileFacet** | uco.observable | Facet | A file facet is a grouping of characteristics unique to the storage of a file (computer resource ... |
| **FilePermissionsFacet** | uco.observable | Facet | A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view... |
| **FileSystem** | uco.observable | Class | A file system is the process that manages how and where data on a storage medium is stored, acces... |
| **FileSystemFacet** | uco.observable | Facet | A file system facet is a grouping of characteristics unique to the process that manages how and w... |
| **GranularMarking** | uco.marking | Class | A granular marking is a grouping of characteristics unique to specification of marking definition... |
| **Junction** | uco.observable | Class | A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory ... |
| **LicenseMarking** | uco.marking | Class | A license marking is a grouping of characteristics unique to the expression of data marking defin... |
| **MACAddress** | uco.observable | Class | A MAC address is a media access control standards conformant identifier assigned to a network int... |
| **MACAddressFacet** | uco.observable | Facet | A MAC address facet is a grouping of characteristics unique to a media access control standards c... |
| **MarkingDefinition** | uco.marking | Class | A marking definition is a grouping of characteristics unique to the expression of a specific data... |
| **MarkingDefinitionAbstraction** | uco.core | Class | A marking definition abstraction is a grouping of characteristics unique to the expression of a s... |
| **MarkingModel** | uco.marking | Class | A marking model is a grouping of characteristics unique to the expression of a particular form of... |
| **Memory** | uco.observable | Class | Memory is a particular region of temporary information storage (e.g., RAM (random access memory),... |
| **MemoryFacet** | uco.observable | Facet | A memory facet is a grouping of characteristics unique to a particular region of temporary inform... |
| **Mutex** | uco.observable | Class | A mutex is a mechanism that enforces limits on access to a resource when there are many threads o... |
| **MutexFacet** | uco.observable | Facet | A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on acce... |
| **NTFSFilePermissionsFacet** | uco.observable | Facet | An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g.... |
| **OnlineService** | uco.observable | Class | An online service is a particular provision mechanism of information access, distribution or mani... |
| **OnlineServiceFacet** | uco.observable | Facet | An online service facet is a grouping of characteristics unique to a particular provision mechani... |
| **PaymentCard** | uco.observable | Class | A payment card is a physical token that is part of a payment system issued by financial instituti... |
| **ReleaseToMarking** | uco.marking | Class | A release-to marking is a grouping of characteristics unique to the expression of data marking de... |
| **ReparsePoint** | uco.observable | Class | A reparse point is a type of NTFS (New Technology File System) object which is an optional attrib... |
| **Semaphore** | uco.observable | Class | A semaphore is a variable or abstract data type used to control access to a common resource by mu... |
| **StatementMarking** | uco.marking | Class | A statement marking is a grouping of characteristics unique to the expression of data marking def... |
| **TermsOfUseMarking** | uco.marking | Class | A terms of use marking is a grouping of characteristics unique to the expression of data marking ... |
| **UNIXFilePermissionsFacet** | uco.observable | Facet | A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g.,... |
| **UNIXVolumeFacet** | uco.observable | Facet | A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (... |
| **URL** | uco.observable | Class | A URL is a uniform resource locator (URL) acting as a resolvable address to a particular WWW (Wor... |
| **URLFacet** | uco.observable | Facet | A URL facet is a grouping of characteristics unique to a uniform resource locator (URL) acting as... |
| **UserAccount** | uco.observable | Class | A user account is an account controlling a user's access to a network, system or platform. |
| **UserAccountFacet** | uco.observable | Facet | A user account facet is a grouping of characteristics unique to an account controlling a user's a... |
| **Volume** | uco.observable | Class | A volume is a single accessible storage area (volume) with a single file system. [based on https:... |
| **VolumeFacet** | uco.observable | Facet | A volume facet is a grouping of characteristics unique to a single accessible storage area (volum... |
| **WifiAddress** | uco.observable | Class | A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a dev... |
| **WifiAddressFacet** | uco.observable | Facet | A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) sta... |
| **WindowsCriticalSection** | uco.observable | Class | A Windows critical section is a Windows object that provides synchronization similar to that prov... |
| **WindowsFilemapping** | uco.observable | Class | A Windows file mapping is the association of a file's contents with a portion of the virtual addr... |
| **WindowsMailslot** | uco.observable | Class | A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard ... |
| **WindowsNetworkShare** | uco.observable | Class | A Windows network share is a Windows computer resource made available from one host to other host... |
| **WindowsVolumeFacet** | uco.observable | Facet | A Windows volume facet is a grouping of characteristics unique to a single accessible storage are... |
| **WriteBlocker** | uco.observable | Class | A write blocker is a device that allows read-only access to storage mediums in order to preserve ... |

**AlternateDataStream** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**ArtifactClassification** key properties:

| Property | Type | Required |
|----------|------|----------|
| class | string | Yes |
| classificationConfidence | decimal | No |

**BlockDeviceNode** key properties:

| Property | Type | Required |
|----------|------|----------|
| createdBy | IdentityAbstraction | No |
| description | string | No |
| externalReference | ExternalReference | No |
| hasFacet | Facet | No |
| modifiedTime | dateTime | No |
| name | string | No |
| objectCreatedTime | dateTime | No |
| objectMarking | MarkingDefinitionAbstraction | No |
| *... 5 more* | | |

**Example usage:**

```python
from case_uco.uco.marking import MarkingDefinition

graph.create(MarkingDefinition)
```

## Extension Ontologies

Extension ontologies add domain-specific classes beyond the core CASE/UCO specification. These are contributed by the community and may cover specialized forensic domains.

### toolcap

| Class | Type | Description |
|-------|------|-------------|
| **CapabilityMatrix** | Class | A capability matrix is a named, versioned collection of ToolCapability assertions that together r... |
| **ToolCapability** | Class | A tool capability is a formal assertion that a specific digital forensic tool can successfully pa... |

## Tips for Finding the Right Class

1. **Start with the domain category** above that matches your data type.

2. **Use the CLI explorer** to search by keyword:
   ```bash
   case-uco-explore search "browser"
   case-uco-explore class BrowserBookmarkFacet
   ```

3. **Use the Python registry** for programmatic discovery:
   ```python
   from case_uco.registry import search, get_class
   search("browser")  # find classes by keyword
   get_class("BrowserBookmarkFacet")  # get full details
   ```

4. **Most observable data uses `ObservableObject` + Facets.** The pattern is:
   - Create an `ObservableObject`
   - Attach one or more Facets (e.g., `FileFacet`, `ContentDataFacet`) to describe it
   - A single observable can have multiple facets

5. **Check the full reference** in [ONTOLOGY_REFERENCE.md](../ONTOLOGY_REFERENCE.md) for complete property tables and inheritance hierarchies.

6. **Browse the ontology modules** to understand how classes are organized:
   ```bash
   case-uco-explore modules              # list all modules
   case-uco-explore module observable     # browse a specific module
   ```
