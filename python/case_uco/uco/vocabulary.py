"""Auto-generated UCO vocabularies for the CASE/UCO ontology.

Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain
strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string
literals checked against the vocabulary with sh:in, so pass the constants
directly rather than typing them with the vocabulary IRI.
"""

from __future__ import annotations

__all__ = [
    "AccountTypeVocab",
    "ActionArgumentNameVocab",
    "ActionNameVocab",
    "ActionRelationshipTypeVocab",
    "ActionStatusTypeVocab",
    "ActionTypeVocab",
    "BitnessVocab",
    "CharacterEncodingVocab",
    "ContactAddressScopeVocab",
    "ContactEmailScopeVocab",
    "ContactPhoneScopeVocab",
    "ContactSIPScopeVocab",
    "ContactURLScopeVocab",
    "DiskTypeVocab",
    "EndiannessTypeVocab",
    "HashNameVocab",
    "LibraryTypeVocab",
    "MemoryBlockTypeVocab",
    "NetworkSocketAddressFamily",
    "NetworkSocketProtocolFamily",
    "NetworkSocketType",
    "ObjectStatusVocab",
    "ObservableObjectRelationshipVocab",
    "ObservableObjectStateVocab",
    "PartitionTypeVocab",
    "ProcessorArchVocab",
    "RecoveredObjectStatusVocab",
    "RegionalRegistryTypeVocab",
    "RegistryDatatype",
    "RegistryDatatypeVocab",
    "SIMFormVocab",
    "SIMTypeVocab",
    "TaskActionTypeVocab",
    "TaskFlagVocab",
    "TaskPriorityVocab",
    "TaskStatusVocab",
    "ThreadRunningStatusVocab",
    "TimestampPrecisionVocab",
    "TrendVocab",
    "TriggerFrequencyVocab",
    "TriggerTypeVocab",
    "URLTransitionTypeVocab",
    "UnixProcessStateVocab",
    "WhoisContactTypeVocab",
    "WhoisDNSSECTypeVocab",
    "WhoisStatusTypeVocab",
    "WindowsDriveTypeVocab",
    "WindowsPEBinaryType",
    "WindowsServiceStartType",
    "WindowsServiceStatus",
    "WindowsServiceType",
    "WindowsVolumeAttributeVocab",
    "WirelessNetworkSecurityModeVocab",
    "VOCABULARIES",
]


class AccountTypeVocab:
    """Vocabulary: AccountTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/AccountTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"ldap", "nis", "openid", "radius", "tacacs", "unix", "windows_domain", "windows_local"})

    LDAP = "ldap"
    NIS = "nis"
    OPENID = "openid"
    RADIUS = "radius"
    TACACS = "tacacs"
    UNIX = "unix"
    WINDOWS_DOMAIN = "windows_domain"
    WINDOWS_LOCAL = "windows_local"


class ActionArgumentNameVocab:
    """Vocabulary: ActionArgumentNameVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionArgumentNameVocab"
    MEMBERS: frozenset[str] = frozenset({"APC Address", "APC Mode", "API", "Access Mode", "Application Name", "Base Address", "Callback Address", "Code Address", "Command", "Control Code", "Control Parameter", "Creation Flags", "Database Name", "Delay Time (ms)", "Destination Address", "Error Control", "File Information Class", "Flags", "Function Address", "Function Name", "Function Ordinal", "Hook Type", "Host Name", "Hostname", "Initial Owner", "Mapping Offset", "Number of Bytes Per Send", "Options", "Parameter Address", "Password", "Privilege Name", "Protection", "Proxy Bypass", "Proxy Name", "Reason", "Request Size", "Requested Version", "Server", "Service Name", "Service State", "Service Type", "Share Mode", "Shutdown Flag", "Size (bytes)", "Sleep Time (ms)", "Source Address", "Starting Address", "System Metric Index", "Target PID", "Transfer Flags", "Username"})

    APC_ADDRESS = "APC Address"
    APC_MODE = "APC Mode"
    API = "API"
    ACCESS_MODE = "Access Mode"
    APPLICATION_NAME = "Application Name"
    BASE_ADDRESS = "Base Address"
    CALLBACK_ADDRESS = "Callback Address"
    CODE_ADDRESS = "Code Address"
    COMMAND = "Command"
    CONTROL_CODE = "Control Code"
    CONTROL_PARAMETER = "Control Parameter"
    CREATION_FLAGS = "Creation Flags"
    DATABASE_NAME = "Database Name"
    DELAY_TIME_MS = "Delay Time (ms)"
    DESTINATION_ADDRESS = "Destination Address"
    ERROR_CONTROL = "Error Control"
    FILE_INFORMATION_CLASS = "File Information Class"
    FLAGS = "Flags"
    FUNCTION_ADDRESS = "Function Address"
    FUNCTION_NAME = "Function Name"
    FUNCTION_ORDINAL = "Function Ordinal"
    HOOK_TYPE = "Hook Type"
    HOST_NAME = "Host Name"
    HOSTNAME = "Hostname"
    INITIAL_OWNER = "Initial Owner"
    MAPPING_OFFSET = "Mapping Offset"
    NUMBER_OF_BYTES_PER_SEND = "Number of Bytes Per Send"
    OPTIONS = "Options"
    PARAMETER_ADDRESS = "Parameter Address"
    PASSWORD = "Password"
    PRIVILEGE_NAME = "Privilege Name"
    PROTECTION = "Protection"
    PROXY_BYPASS = "Proxy Bypass"
    PROXY_NAME = "Proxy Name"
    REASON = "Reason"
    REQUEST_SIZE = "Request Size"
    REQUESTED_VERSION = "Requested Version"
    SERVER = "Server"
    SERVICE_NAME = "Service Name"
    SERVICE_STATE = "Service State"
    SERVICE_TYPE = "Service Type"
    SHARE_MODE = "Share Mode"
    SHUTDOWN_FLAG = "Shutdown Flag"
    SIZE_BYTES = "Size (bytes)"
    SLEEP_TIME_MS = "Sleep Time (ms)"
    SOURCE_ADDRESS = "Source Address"
    STARTING_ADDRESS = "Starting Address"
    SYSTEM_METRIC_INDEX = "System Metric Index"
    TARGET_PID = "Target PID"
    TRANSFER_FLAGS = "Transfer Flags"
    USERNAME = "Username"


class ActionNameVocab:
    """Vocabulary: ActionNameVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionNameVocab"
    MEMBERS: frozenset[str] = frozenset({"Accept Socket Connection", "Add Connection to Network Share", "Add Network Share", "Add Scheduled Task", "Add System Call Hook", "Add User", "Add Windows Hook", "Allocate Virtual Memory in Process", "Bind Address to Socket", "Change Service Configuration", "Check for Remote Debugger", "Close Port", "Close Registry Key", "Close Socket", "Configure Service", "Connect to IP", "Connect to Named Pipe", "Connect to Network Share", "Connect to Socket", "Connect to URL", "Control Driver", "Control Service", "Copy File", "Create Dialog Box", "Create Directory", "Create Event", "Create File", "Create File Alternate Data Stream", "Create File Mapping", "Create File Symbolic Link", "Create Hidden File", "Create Mailslot", "Create Module", "Create Mutex", "Create Named Pipe", "Create Process", "Create Process as User", "Create Registry Key", "Create Registry Key Value", "Create Remote Thread in Process", "Create Service", "Create Socket", "Create Symbolic Link", "Create Thread", "Create Window", "Delete Directory", "Delete File", "Delete Named Pipe", "Delete Network Share", "Delete Registry Key", "Delete Registry Key Value", "Delete Service", "Delete User", "Disconnect from Named Pipe", "Disconnect from Network Share", "Disconnect from Socket", "Download File", "Enumerate DLLs", "Enumerate Network Shares", "Enumerate Processes", "Enumerate Protocols", "Enumerate Registry Key Subkeys", "Enumerate Registry Key Values", "Enumerate Services", "Enumerate System Handles", "Enumerate Threads", "Enumerate Threads in Process", "Enumerate Users", "Enumerate Windows", "Find File", "Find Window", "Flush Process Instruction Cache", "Free Library", "Free Process Virtual Memory", "Get Disk Free Space", "Get Disk Type", "Get Elapsed System Up Time", "Get File Attributes", "Get Function Address", "Get Host By Address", "Get Host By Name", "Get Host Name", "Get Library File Name", "Get Library Handle", "Get NetBIOS Name", "Get Process Current Directory", "Get Process Environment Variable", "Get Process Startup Information", "Get Processes Snapshot", "Get Registry Key Attributes", "Get Service Status", "Get System Global Flags", "Get System Host Name", "Get System Local Time", "Get System NetBIOS Name", "Get System Network Parameters", "Get System Time", "Get Thread Context", "Get Thread Username", "Get User Attributes", "Get Username", "Get Windows Directory", "Get Windows System Directory", "Get Windows Temporary Files Directory", "Hide Window", "Impersonate Process", "Impersonate Thread", "Inject Memory Page", "Kill Process", "Kill Thread", "Kill Window", "Listen on Port", "Listen on Socket", "Load Driver", "Load Library", "Load Module", "Load and Call Driver", "Lock File", "Logon as User", "Map File", "Map Library", "Map View of File", "Modify File", "Modify Named Pipe", "Modify Process", "Modify Registry Key", "Modify Registry Key Value", "Modify Service", "Monitor Registry Key", "Move File", "Open File", "Open File Mapping", "Open Mutex", "Open Port", "Open Process", "Open Registry Key", "Open Service", "Open Service Control Manager", "Protect Virtual Memory", "Query DNS", "Query Disk Attributes", "Query Process Virtual Memory", "Queue APC in Thread", "Read File", "Read From Named Pipe", "Read From Process Memory", "Read Registry Key Value", "Receive Data on Socket", "Receive Email Message", "Release Mutex", "Rename File", "Revert Thread to Self", "Send Control Code to File", "Send Control Code to Pipe", "Send Control Code to Service", "Send DNS Query", "Send Data on Socket", "Send Data to Address on Socket", "Send Email Message", "Send ICMP Request", "Send Reverse DNS Query", "Set File Attributes", "Set NetBIOS Name", "Set Process Current Directory", "Set Process Environment Variable", "Set System Global Flags", "Set System Host Name", "Set System Time", "Set Thread Context", "Show Window", "Shutdown System", "Sleep Process", "Sleep System", "Start Service", "Unload Driver", "Unload Module", "Unlock File", "Unmap File", "Upload File", "Write to File", "Write to Process Virtual Memory"})

    ACCEPT_SOCKET_CONNECTION = "Accept Socket Connection"
    ADD_CONNECTION_TO_NETWORK_SHARE = "Add Connection to Network Share"
    ADD_NETWORK_SHARE = "Add Network Share"
    ADD_SCHEDULED_TASK = "Add Scheduled Task"
    ADD_SYSTEM_CALL_HOOK = "Add System Call Hook"
    ADD_USER = "Add User"
    ADD_WINDOWS_HOOK = "Add Windows Hook"
    ALLOCATE_VIRTUAL_MEMORY_IN_PROCESS = "Allocate Virtual Memory in Process"
    BIND_ADDRESS_TO_SOCKET = "Bind Address to Socket"
    CHANGE_SERVICE_CONFIGURATION = "Change Service Configuration"
    CHECK_FOR_REMOTE_DEBUGGER = "Check for Remote Debugger"
    CLOSE_PORT = "Close Port"
    CLOSE_REGISTRY_KEY = "Close Registry Key"
    CLOSE_SOCKET = "Close Socket"
    CONFIGURE_SERVICE = "Configure Service"
    CONNECT_TO_IP = "Connect to IP"
    CONNECT_TO_NAMED_PIPE = "Connect to Named Pipe"
    CONNECT_TO_NETWORK_SHARE = "Connect to Network Share"
    CONNECT_TO_SOCKET = "Connect to Socket"
    CONNECT_TO_URL = "Connect to URL"
    CONTROL_DRIVER = "Control Driver"
    CONTROL_SERVICE = "Control Service"
    COPY_FILE = "Copy File"
    CREATE_DIALOG_BOX = "Create Dialog Box"
    CREATE_DIRECTORY = "Create Directory"
    CREATE_EVENT = "Create Event"
    CREATE_FILE = "Create File"
    CREATE_FILE_ALTERNATE_DATA_STREAM = "Create File Alternate Data Stream"
    CREATE_FILE_MAPPING = "Create File Mapping"
    CREATE_FILE_SYMBOLIC_LINK = "Create File Symbolic Link"
    CREATE_HIDDEN_FILE = "Create Hidden File"
    CREATE_MAILSLOT = "Create Mailslot"
    CREATE_MODULE = "Create Module"
    CREATE_MUTEX = "Create Mutex"
    CREATE_NAMED_PIPE = "Create Named Pipe"
    CREATE_PROCESS = "Create Process"
    CREATE_PROCESS_AS_USER = "Create Process as User"
    CREATE_REGISTRY_KEY = "Create Registry Key"
    CREATE_REGISTRY_KEY_VALUE = "Create Registry Key Value"
    CREATE_REMOTE_THREAD_IN_PROCESS = "Create Remote Thread in Process"
    CREATE_SERVICE = "Create Service"
    CREATE_SOCKET = "Create Socket"
    CREATE_SYMBOLIC_LINK = "Create Symbolic Link"
    CREATE_THREAD = "Create Thread"
    CREATE_WINDOW = "Create Window"
    DELETE_DIRECTORY = "Delete Directory"
    DELETE_FILE = "Delete File"
    DELETE_NAMED_PIPE = "Delete Named Pipe"
    DELETE_NETWORK_SHARE = "Delete Network Share"
    DELETE_REGISTRY_KEY = "Delete Registry Key"
    DELETE_REGISTRY_KEY_VALUE = "Delete Registry Key Value"
    DELETE_SERVICE = "Delete Service"
    DELETE_USER = "Delete User"
    DISCONNECT_FROM_NAMED_PIPE = "Disconnect from Named Pipe"
    DISCONNECT_FROM_NETWORK_SHARE = "Disconnect from Network Share"
    DISCONNECT_FROM_SOCKET = "Disconnect from Socket"
    DOWNLOAD_FILE = "Download File"
    ENUMERATE_DLLS = "Enumerate DLLs"
    ENUMERATE_NETWORK_SHARES = "Enumerate Network Shares"
    ENUMERATE_PROCESSES = "Enumerate Processes"
    ENUMERATE_PROTOCOLS = "Enumerate Protocols"
    ENUMERATE_REGISTRY_KEY_SUBKEYS = "Enumerate Registry Key Subkeys"
    ENUMERATE_REGISTRY_KEY_VALUES = "Enumerate Registry Key Values"
    ENUMERATE_SERVICES = "Enumerate Services"
    ENUMERATE_SYSTEM_HANDLES = "Enumerate System Handles"
    ENUMERATE_THREADS = "Enumerate Threads"
    ENUMERATE_THREADS_IN_PROCESS = "Enumerate Threads in Process"
    ENUMERATE_USERS = "Enumerate Users"
    ENUMERATE_WINDOWS = "Enumerate Windows"
    FIND_FILE = "Find File"
    FIND_WINDOW = "Find Window"
    FLUSH_PROCESS_INSTRUCTION_CACHE = "Flush Process Instruction Cache"
    FREE_LIBRARY = "Free Library"
    FREE_PROCESS_VIRTUAL_MEMORY = "Free Process Virtual Memory"
    GET_DISK_FREE_SPACE = "Get Disk Free Space"
    GET_DISK_TYPE = "Get Disk Type"
    GET_ELAPSED_SYSTEM_UP_TIME = "Get Elapsed System Up Time"
    GET_FILE_ATTRIBUTES = "Get File Attributes"
    GET_FUNCTION_ADDRESS = "Get Function Address"
    GET_HOST_BY_ADDRESS = "Get Host By Address"
    GET_HOST_BY_NAME = "Get Host By Name"
    GET_HOST_NAME = "Get Host Name"
    GET_LIBRARY_FILE_NAME = "Get Library File Name"
    GET_LIBRARY_HANDLE = "Get Library Handle"
    GET_NETBIOS_NAME = "Get NetBIOS Name"
    GET_PROCESS_CURRENT_DIRECTORY = "Get Process Current Directory"
    GET_PROCESS_ENVIRONMENT_VARIABLE = "Get Process Environment Variable"
    GET_PROCESS_STARTUP_INFORMATION = "Get Process Startup Information"
    GET_PROCESSES_SNAPSHOT = "Get Processes Snapshot"
    GET_REGISTRY_KEY_ATTRIBUTES = "Get Registry Key Attributes"
    GET_SERVICE_STATUS = "Get Service Status"
    GET_SYSTEM_GLOBAL_FLAGS = "Get System Global Flags"
    GET_SYSTEM_HOST_NAME = "Get System Host Name"
    GET_SYSTEM_LOCAL_TIME = "Get System Local Time"
    GET_SYSTEM_NETBIOS_NAME = "Get System NetBIOS Name"
    GET_SYSTEM_NETWORK_PARAMETERS = "Get System Network Parameters"
    GET_SYSTEM_TIME = "Get System Time"
    GET_THREAD_CONTEXT = "Get Thread Context"
    GET_THREAD_USERNAME = "Get Thread Username"
    GET_USER_ATTRIBUTES = "Get User Attributes"
    GET_USERNAME = "Get Username"
    GET_WINDOWS_DIRECTORY = "Get Windows Directory"
    GET_WINDOWS_SYSTEM_DIRECTORY = "Get Windows System Directory"
    GET_WINDOWS_TEMPORARY_FILES_DIRECTORY = "Get Windows Temporary Files Directory"
    HIDE_WINDOW = "Hide Window"
    IMPERSONATE_PROCESS = "Impersonate Process"
    IMPERSONATE_THREAD = "Impersonate Thread"
    INJECT_MEMORY_PAGE = "Inject Memory Page"
    KILL_PROCESS = "Kill Process"
    KILL_THREAD = "Kill Thread"
    KILL_WINDOW = "Kill Window"
    LISTEN_ON_PORT = "Listen on Port"
    LISTEN_ON_SOCKET = "Listen on Socket"
    LOAD_DRIVER = "Load Driver"
    LOAD_LIBRARY = "Load Library"
    LOAD_MODULE = "Load Module"
    LOAD_AND_CALL_DRIVER = "Load and Call Driver"
    LOCK_FILE = "Lock File"
    LOGON_AS_USER = "Logon as User"
    MAP_FILE = "Map File"
    MAP_LIBRARY = "Map Library"
    MAP_VIEW_OF_FILE = "Map View of File"
    MODIFY_FILE = "Modify File"
    MODIFY_NAMED_PIPE = "Modify Named Pipe"
    MODIFY_PROCESS = "Modify Process"
    MODIFY_REGISTRY_KEY = "Modify Registry Key"
    MODIFY_REGISTRY_KEY_VALUE = "Modify Registry Key Value"
    MODIFY_SERVICE = "Modify Service"
    MONITOR_REGISTRY_KEY = "Monitor Registry Key"
    MOVE_FILE = "Move File"
    OPEN_FILE = "Open File"
    OPEN_FILE_MAPPING = "Open File Mapping"
    OPEN_MUTEX = "Open Mutex"
    OPEN_PORT = "Open Port"
    OPEN_PROCESS = "Open Process"
    OPEN_REGISTRY_KEY = "Open Registry Key"
    OPEN_SERVICE = "Open Service"
    OPEN_SERVICE_CONTROL_MANAGER = "Open Service Control Manager"
    PROTECT_VIRTUAL_MEMORY = "Protect Virtual Memory"
    QUERY_DNS = "Query DNS"
    QUERY_DISK_ATTRIBUTES = "Query Disk Attributes"
    QUERY_PROCESS_VIRTUAL_MEMORY = "Query Process Virtual Memory"
    QUEUE_APC_IN_THREAD = "Queue APC in Thread"
    READ_FILE = "Read File"
    READ_FROM_NAMED_PIPE = "Read From Named Pipe"
    READ_FROM_PROCESS_MEMORY = "Read From Process Memory"
    READ_REGISTRY_KEY_VALUE = "Read Registry Key Value"
    RECEIVE_DATA_ON_SOCKET = "Receive Data on Socket"
    RECEIVE_EMAIL_MESSAGE = "Receive Email Message"
    RELEASE_MUTEX = "Release Mutex"
    RENAME_FILE = "Rename File"
    REVERT_THREAD_TO_SELF = "Revert Thread to Self"
    SEND_CONTROL_CODE_TO_FILE = "Send Control Code to File"
    SEND_CONTROL_CODE_TO_PIPE = "Send Control Code to Pipe"
    SEND_CONTROL_CODE_TO_SERVICE = "Send Control Code to Service"
    SEND_DNS_QUERY = "Send DNS Query"
    SEND_DATA_ON_SOCKET = "Send Data on Socket"
    SEND_DATA_TO_ADDRESS_ON_SOCKET = "Send Data to Address on Socket"
    SEND_EMAIL_MESSAGE = "Send Email Message"
    SEND_ICMP_REQUEST = "Send ICMP Request"
    SEND_REVERSE_DNS_QUERY = "Send Reverse DNS Query"
    SET_FILE_ATTRIBUTES = "Set File Attributes"
    SET_NETBIOS_NAME = "Set NetBIOS Name"
    SET_PROCESS_CURRENT_DIRECTORY = "Set Process Current Directory"
    SET_PROCESS_ENVIRONMENT_VARIABLE = "Set Process Environment Variable"
    SET_SYSTEM_GLOBAL_FLAGS = "Set System Global Flags"
    SET_SYSTEM_HOST_NAME = "Set System Host Name"
    SET_SYSTEM_TIME = "Set System Time"
    SET_THREAD_CONTEXT = "Set Thread Context"
    SHOW_WINDOW = "Show Window"
    SHUTDOWN_SYSTEM = "Shutdown System"
    SLEEP_PROCESS = "Sleep Process"
    SLEEP_SYSTEM = "Sleep System"
    START_SERVICE = "Start Service"
    UNLOAD_DRIVER = "Unload Driver"
    UNLOAD_MODULE = "Unload Module"
    UNLOCK_FILE = "Unlock File"
    UNMAP_FILE = "Unmap File"
    UPLOAD_FILE = "Upload File"
    WRITE_TO_FILE = "Write to File"
    WRITE_TO_PROCESS_VIRTUAL_MEMORY = "Write to Process Virtual Memory"


class ActionRelationshipTypeVocab:
    """Vocabulary: ActionRelationshipTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionRelationshipTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Dependent_On", "Equivalent_To", "Followed_By", "Initiated", "Initiated_By", "Preceded_By", "Related_To"})

    DEPENDENT_ON = "Dependent_On"
    EQUIVALENT_TO = "Equivalent_To"
    FOLLOWED_BY = "Followed_By"
    INITIATED = "Initiated"
    INITIATED_BY = "Initiated_By"
    PRECEDED_BY = "Preceded_By"
    RELATED_TO = "Related_To"


class ActionStatusTypeVocab:
    """Vocabulary: ActionStatusTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionStatusTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Complete/Finish", "Error", "Fail", "Ongoing", "Pending", "Success", "Unknown"})

    COMPLETE_FINISH = "Complete/Finish"
    ERROR = "Error"
    FAIL = "Fail"
    ONGOING = "Ongoing"
    PENDING = "Pending"
    SUCCESS = "Success"
    UNKNOWN = "Unknown"


class ActionTypeVocab:
    """Vocabulary: ActionTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Accept", "Access", "Add", "Alert", "Allocate", "Archive", "Assign", "Audit", "Backup", "Bind", "Block", "Call", "Change", "Check", "Clean", "Click", "Close", "Compare", "Compress", "Configure", "Connect", "Control", "Copy/Duplicate", "Create", "Decode", "Decompress", "Decrypt", "Deny", "Depress", "Detect", "Disconnect", "Download", "Draw", "Drop", "Encode", "Encrypt", "Enumerate", "Execute", "Extract", "Filter", "Find", "Flush", "Fork", "Free", "Get", "Hide", "Hook", "Impersonate", "Initialize", "Inject", "Install", "Interleave", "Join", "Kill", "Listen", "Load", "Lock", "Login/Logon", "Logout/Logoff", "Map", "Merge", "Modify", "Monitor", "Move", "Open", "Pack", "Pause", "Press", "Protect", "Quarantine", "Query", "Queue", "Raise", "Read", "Receive", "Release", "Remove/Delete", "Rename", "Replicate", "Restore", "Resume", "Revert", "Run", "Save", "Scan", "Schedule", "Search", "Send", "Set", "Shutdown", "Sleep", "Snapshot", "Start", "Stop", "Suspend", "Synchronize", "Throw", "Transmit", "Unblock", "Unhide", "Unhook", "Uninstall", "Unload", "Unlock", "Unmap", "Unpack", "Update", "Upgrade", "Upload", "Wipe/Destroy/Purge", "Write"})

    ACCEPT = "Accept"
    ACCESS = "Access"
    ADD = "Add"
    ALERT = "Alert"
    ALLOCATE = "Allocate"
    ARCHIVE = "Archive"
    ASSIGN = "Assign"
    AUDIT = "Audit"
    BACKUP = "Backup"
    BIND = "Bind"
    BLOCK = "Block"
    CALL = "Call"
    CHANGE = "Change"
    CHECK = "Check"
    CLEAN = "Clean"
    CLICK = "Click"
    CLOSE = "Close"
    COMPARE = "Compare"
    COMPRESS = "Compress"
    CONFIGURE = "Configure"
    CONNECT = "Connect"
    CONTROL = "Control"
    COPY_DUPLICATE = "Copy/Duplicate"
    CREATE = "Create"
    DECODE = "Decode"
    DECOMPRESS = "Decompress"
    DECRYPT = "Decrypt"
    DENY = "Deny"
    DEPRESS = "Depress"
    DETECT = "Detect"
    DISCONNECT = "Disconnect"
    DOWNLOAD = "Download"
    DRAW = "Draw"
    DROP = "Drop"
    ENCODE = "Encode"
    ENCRYPT = "Encrypt"
    ENUMERATE = "Enumerate"
    EXECUTE = "Execute"
    EXTRACT = "Extract"
    FILTER = "Filter"
    FIND = "Find"
    FLUSH = "Flush"
    FORK = "Fork"
    FREE = "Free"
    GET = "Get"
    HIDE = "Hide"
    HOOK = "Hook"
    IMPERSONATE = "Impersonate"
    INITIALIZE = "Initialize"
    INJECT = "Inject"
    INSTALL = "Install"
    INTERLEAVE = "Interleave"
    JOIN = "Join"
    KILL = "Kill"
    LISTEN = "Listen"
    LOAD = "Load"
    LOCK = "Lock"
    LOGIN_LOGON = "Login/Logon"
    LOGOUT_LOGOFF = "Logout/Logoff"
    MAP = "Map"
    MERGE = "Merge"
    MODIFY = "Modify"
    MONITOR = "Monitor"
    MOVE = "Move"
    OPEN = "Open"
    PACK = "Pack"
    PAUSE = "Pause"
    PRESS = "Press"
    PROTECT = "Protect"
    QUARANTINE = "Quarantine"
    QUERY = "Query"
    QUEUE = "Queue"
    RAISE = "Raise"
    READ = "Read"
    RECEIVE = "Receive"
    RELEASE = "Release"
    REMOVE_DELETE = "Remove/Delete"
    RENAME = "Rename"
    REPLICATE = "Replicate"
    RESTORE = "Restore"
    RESUME = "Resume"
    REVERT = "Revert"
    RUN = "Run"
    SAVE = "Save"
    SCAN = "Scan"
    SCHEDULE = "Schedule"
    SEARCH = "Search"
    SEND = "Send"
    SET = "Set"
    SHUTDOWN = "Shutdown"
    SLEEP = "Sleep"
    SNAPSHOT = "Snapshot"
    START = "Start"
    STOP = "Stop"
    SUSPEND = "Suspend"
    SYNCHRONIZE = "Synchronize"
    THROW = "Throw"
    TRANSMIT = "Transmit"
    UNBLOCK = "Unblock"
    UNHIDE = "Unhide"
    UNHOOK = "Unhook"
    UNINSTALL = "Uninstall"
    UNLOAD = "Unload"
    UNLOCK = "Unlock"
    UNMAP = "Unmap"
    UNPACK = "Unpack"
    UPDATE = "Update"
    UPGRADE = "Upgrade"
    UPLOAD = "Upload"
    WIPE_DESTROY_PURGE = "Wipe/Destroy/Purge"
    WRITE = "Write"


class BitnessVocab:
    """Vocabulary: BitnessVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/BitnessVocab"
    MEMBERS: frozenset[str] = frozenset({"32", "64"})

    _32 = "32"
    _64 = "64"


class CharacterEncodingVocab:
    """Vocabulary: CharacterEncodingVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/CharacterEncodingVocab"
    MEMBERS: frozenset[str] = frozenset({"ASCII", "UTF-16", "UTF-32", "UTF-8", "Windows-1250", "Windows-1251", "Windows-1252", "Windows-1253", "Windows-1254", "Windows-1255", "Windows-1256", "Windows-1257", "Windows-1258"})

    ASCII = "ASCII"
    UTF_16 = "UTF-16"
    UTF_32 = "UTF-32"
    UTF_8 = "UTF-8"
    WINDOWS_1250 = "Windows-1250"
    WINDOWS_1251 = "Windows-1251"
    WINDOWS_1252 = "Windows-1252"
    WINDOWS_1253 = "Windows-1253"
    WINDOWS_1254 = "Windows-1254"
    WINDOWS_1255 = "Windows-1255"
    WINDOWS_1256 = "Windows-1256"
    WINDOWS_1257 = "Windows-1257"
    WINDOWS_1258 = "Windows-1258"


class ContactAddressScopeVocab:
    """Vocabulary: ContactAddressScopeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactAddressScopeVocab"
    MEMBERS: frozenset[str] = frozenset({"home", "school", "work"})

    HOME = "home"
    SCHOOL = "school"
    WORK = "work"


class ContactEmailScopeVocab:
    """Vocabulary: ContactEmailScopeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactEmailScopeVocab"
    MEMBERS: frozenset[str] = frozenset({"cloud", "home", "school", "work"})

    CLOUD = "cloud"
    HOME = "home"
    SCHOOL = "school"
    WORK = "work"


class ContactPhoneScopeVocab:
    """Vocabulary: ContactPhoneScopeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactPhoneScopeVocab"
    MEMBERS: frozenset[str] = frozenset({"home", "home fax", "main", "mobile", "pager", "school", "work", "work fax"})

    HOME = "home"
    HOME_FAX = "home fax"
    MAIN = "main"
    MOBILE = "mobile"
    PAGER = "pager"
    SCHOOL = "school"
    WORK = "work"
    WORK_FAX = "work fax"


class ContactSIPScopeVocab:
    """Vocabulary: ContactSIPScopeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactSIPScopeVocab"
    MEMBERS: frozenset[str] = frozenset({"home", "school", "work"})

    HOME = "home"
    SCHOOL = "school"
    WORK = "work"


class ContactURLScopeVocab:
    """Vocabulary: ContactURLScopeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactURLScopeVocab"
    MEMBERS: frozenset[str] = frozenset({"home", "homepage", "school", "work"})

    HOME = "home"
    HOMEPAGE = "homepage"
    SCHOOL = "school"
    WORK = "work"


class DiskTypeVocab:
    """Vocabulary: DiskTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/DiskTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"CDRom", "Fixed", "RAMDisk", "Remote", "Removable"})

    CDROM = "CDRom"
    FIXED = "Fixed"
    RAMDISK = "RAMDisk"
    REMOTE = "Remote"
    REMOVABLE = "Removable"


class EndiannessTypeVocab:
    """Vocabulary: EndiannessTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/EndiannessTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Big-endian", "Little-endian", "Middle-endian"})

    BIG_ENDIAN = "Big-endian"
    LITTLE_ENDIAN = "Little-endian"
    MIDDLE_ENDIAN = "Middle-endian"


class HashNameVocab:
    """Vocabulary: HashNameVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/HashNameVocab"
    MEMBERS: frozenset[str] = frozenset({"MD5", "MD6", "SHA1", "SHA224", "SHA256", "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512", "SHA384", "SHA512", "SSDEEP"})

    MD5 = "MD5"
    MD6 = "MD6"
    SHA1 = "SHA1"
    SHA224 = "SHA224"
    SHA256 = "SHA256"
    SHA3_224 = "SHA3-224"
    SHA3_256 = "SHA3-256"
    SHA3_384 = "SHA3-384"
    SHA3_512 = "SHA3-512"
    SHA384 = "SHA384"
    SHA512 = "SHA512"
    SSDEEP = "SSDEEP"


class LibraryTypeVocab:
    """Vocabulary: LibraryTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/LibraryTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Dynamic", "Other", "Remote", "Shared", "Static"})

    DYNAMIC = "Dynamic"
    OTHER = "Other"
    REMOTE = "Remote"
    SHARED = "Shared"
    STATIC = "Static"


class MemoryBlockTypeVocab:
    """Vocabulary: MemoryBlockTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/MemoryBlockTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Bit-mapped", "Byte-mapped", "Initialized", "Overlay", "Uninitialized"})

    BIT_MAPPED = "Bit-mapped"
    BYTE_MAPPED = "Byte-mapped"
    INITIALIZED = "Initialized"
    OVERLAY = "Overlay"
    UNINITIALIZED = "Uninitialized"


class NetworkSocketAddressFamily:
    """Vocabulary: NetworkSocketAddressFamily"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketAddressFamily"
    MEMBERS: frozenset[str] = frozenset({"af_appletalk", "af_bth", "af_inet", "af_inet6", "af_ipx", "af_irda", "af_netbios", "af_unspec"})

    AF_APPLETALK = "af_appletalk"
    AF_BTH = "af_bth"
    AF_INET = "af_inet"
    AF_INET6 = "af_inet6"
    AF_IPX = "af_ipx"
    AF_IRDA = "af_irda"
    AF_NETBIOS = "af_netbios"
    AF_UNSPEC = "af_unspec"


class NetworkSocketProtocolFamily:
    """Vocabulary: NetworkSocketProtocolFamily"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketProtocolFamily"
    MEMBERS: frozenset[str] = frozenset({"pf_appletalk", "pf_ash", "pf_atmpvc", "pf_atmsvc", "pf_ax25", "pf_bluetooth", "pf_bridge", "pf_decnet", "pf_econet", "pf_inet", "pf_inet6", "pf_ipx", "pf_irda", "pf_key", "pf_netbeui", "pf_netlink", "pf_netrom", "pf_packet", "pf_pppox", "pf_rose", "pf_route", "pf_security", "pf_sna", "pf_wanpipe", "pf_x25"})

    PF_APPLETALK = "pf_appletalk"
    PF_ASH = "pf_ash"
    PF_ATMPVC = "pf_atmpvc"
    PF_ATMSVC = "pf_atmsvc"
    PF_AX25 = "pf_ax25"
    PF_BLUETOOTH = "pf_bluetooth"
    PF_BRIDGE = "pf_bridge"
    PF_DECNET = "pf_decnet"
    PF_ECONET = "pf_econet"
    PF_INET = "pf_inet"
    PF_INET6 = "pf_inet6"
    PF_IPX = "pf_ipx"
    PF_IRDA = "pf_irda"
    PF_KEY = "pf_key"
    PF_NETBEUI = "pf_netbeui"
    PF_NETLINK = "pf_netlink"
    PF_NETROM = "pf_netrom"
    PF_PACKET = "pf_packet"
    PF_PPPOX = "pf_pppox"
    PF_ROSE = "pf_rose"
    PF_ROUTE = "pf_route"
    PF_SECURITY = "pf_security"
    PF_SNA = "pf_sna"
    PF_WANPIPE = "pf_wanpipe"
    PF_X25 = "pf_x25"


class NetworkSocketType:
    """Vocabulary: NetworkSocketType"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketType"
    MEMBERS: frozenset[str] = frozenset({"sock_dgram", "sock_raw", "sock_rdm", "sock_seqpacket", "sock_stream"})

    SOCK_DGRAM = "sock_dgram"
    SOCK_RAW = "sock_raw"
    SOCK_RDM = "sock_rdm"
    SOCK_SEQPACKET = "sock_seqpacket"
    SOCK_STREAM = "sock_stream"


class ObjectStatusVocab:
    """Vocabulary: ObjectStatusVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/core/ObjectStatusVocab"
    MEMBERS: frozenset[str] = frozenset({"Deprecated", "Draft", "Final"})

    DEPRECATED = "Deprecated"
    DRAFT = "Draft"
    FINAL = "Final"


class ObservableObjectRelationshipVocab:
    """Vocabulary: ObservableObjectRelationshipVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectRelationshipVocab"
    MEMBERS: frozenset[str] = frozenset({"Allocated", "Allocated_By", "Attachment_Of", "Bound", "Bound_By", "Characterized_By", "Characterizes", "Child_Of", "Closed", "Closed_By", "Compressed", "Compressed_By", "Compressed_From", "Compressed_Into", "Connected_From", "Connected_To", "Contained_Within", "Contains", "Copied", "Copied_By", "Copied_From", "Copied_To", "Created", "Created_By", "Decoded", "Decoded_By", "Decompressed", "Decompressed_By", "Decrypted", "Decrypted_By", "Deleted", "Deleted_By", "Deleted_From", "Downloaded", "Downloaded_By", "Downloaded_From", "Downloaded_To", "Dropped", "Dropped_By", "Encoded", "Encoded_By", "Encrypted", "Encrypted_By", "Encrypted_From", "Encrypted_To", "Extracted_From", "FQDN_Of", "Freed", "Freed_By", "Had_Attachment", "Hooked", "Hooked_By", "Initialized_By", "Initialized_To", "Injected", "Injected_As", "Injected_By", "Injected_Into", "Installed", "Installed_By", "Joined", "Joined_By", "Killed", "Killed_By", "Listened_On", "Listened_On_By", "Loaded_From", "Loaded_Into", "Locked", "Locked_By", "Mapped_By", "Mapped_Into", "Merged", "Merged_By", "Modified_Properties_Of", "Monitored", "Monitored_By", "Moved", "Moved_By", "Moved_From", "Moved_To", "Opened", "Opened_By", "Packed", "Packed_By", "Packed_From", "Packed_Into", "Parent_Of", "Paused", "Paused_By", "Previously_Contained", "Properties_Modified_By", "Properties_Queried", "Properties_Queried_By", "Read_From", "Read_From_By", "Received", "Received_By", "Received_From", "Received_Via_Upload", "Redirects_To", "Related_To", "Renamed", "Renamed_By", "Renamed_From", "Renamed_To", "Resolved_To", "Resumed", "Resumed_By", "Root_Domain_Of", "Searched_For", "Searched_For_By", "Sent", "Sent_By", "Sent_To", "Sent_Via_Upload", "Set_From", "Set_To", "Signed_By", "Sub-domain_Of", "Supra-domain_Of", "Suspended", "Suspended_By", "Unhooked", "Unhooked_By", "Unlocked", "Unlocked_By", "Unpacked", "Unpacked_By", "Uploaded", "Uploaded_By", "Uploaded_From", "Uploaded_To", "Used", "Used_By", "Values_Enumerated", "Values_Enumerated_By", "Written_To_By", "Wrote_To"})

    ALLOCATED = "Allocated"
    ALLOCATED_BY = "Allocated_By"
    ATTACHMENT_OF = "Attachment_Of"
    BOUND = "Bound"
    BOUND_BY = "Bound_By"
    CHARACTERIZED_BY = "Characterized_By"
    CHARACTERIZES = "Characterizes"
    CHILD_OF = "Child_Of"
    CLOSED = "Closed"
    CLOSED_BY = "Closed_By"
    COMPRESSED = "Compressed"
    COMPRESSED_BY = "Compressed_By"
    COMPRESSED_FROM = "Compressed_From"
    COMPRESSED_INTO = "Compressed_Into"
    CONNECTED_FROM = "Connected_From"
    CONNECTED_TO = "Connected_To"
    CONTAINED_WITHIN = "Contained_Within"
    CONTAINS = "Contains"
    COPIED = "Copied"
    COPIED_BY = "Copied_By"
    COPIED_FROM = "Copied_From"
    COPIED_TO = "Copied_To"
    CREATED = "Created"
    CREATED_BY = "Created_By"
    DECODED = "Decoded"
    DECODED_BY = "Decoded_By"
    DECOMPRESSED = "Decompressed"
    DECOMPRESSED_BY = "Decompressed_By"
    DECRYPTED = "Decrypted"
    DECRYPTED_BY = "Decrypted_By"
    DELETED = "Deleted"
    DELETED_BY = "Deleted_By"
    DELETED_FROM = "Deleted_From"
    DOWNLOADED = "Downloaded"
    DOWNLOADED_BY = "Downloaded_By"
    DOWNLOADED_FROM = "Downloaded_From"
    DOWNLOADED_TO = "Downloaded_To"
    DROPPED = "Dropped"
    DROPPED_BY = "Dropped_By"
    ENCODED = "Encoded"
    ENCODED_BY = "Encoded_By"
    ENCRYPTED = "Encrypted"
    ENCRYPTED_BY = "Encrypted_By"
    ENCRYPTED_FROM = "Encrypted_From"
    ENCRYPTED_TO = "Encrypted_To"
    EXTRACTED_FROM = "Extracted_From"
    FQDN_OF = "FQDN_Of"
    FREED = "Freed"
    FREED_BY = "Freed_By"
    HAD_ATTACHMENT = "Had_Attachment"
    HOOKED = "Hooked"
    HOOKED_BY = "Hooked_By"
    INITIALIZED_BY = "Initialized_By"
    INITIALIZED_TO = "Initialized_To"
    INJECTED = "Injected"
    INJECTED_AS = "Injected_As"
    INJECTED_BY = "Injected_By"
    INJECTED_INTO = "Injected_Into"
    INSTALLED = "Installed"
    INSTALLED_BY = "Installed_By"
    JOINED = "Joined"
    JOINED_BY = "Joined_By"
    KILLED = "Killed"
    KILLED_BY = "Killed_By"
    LISTENED_ON = "Listened_On"
    LISTENED_ON_BY = "Listened_On_By"
    LOADED_FROM = "Loaded_From"
    LOADED_INTO = "Loaded_Into"
    LOCKED = "Locked"
    LOCKED_BY = "Locked_By"
    MAPPED_BY = "Mapped_By"
    MAPPED_INTO = "Mapped_Into"
    MERGED = "Merged"
    MERGED_BY = "Merged_By"
    MODIFIED_PROPERTIES_OF = "Modified_Properties_Of"
    MONITORED = "Monitored"
    MONITORED_BY = "Monitored_By"
    MOVED = "Moved"
    MOVED_BY = "Moved_By"
    MOVED_FROM = "Moved_From"
    MOVED_TO = "Moved_To"
    OPENED = "Opened"
    OPENED_BY = "Opened_By"
    PACKED = "Packed"
    PACKED_BY = "Packed_By"
    PACKED_FROM = "Packed_From"
    PACKED_INTO = "Packed_Into"
    PARENT_OF = "Parent_Of"
    PAUSED = "Paused"
    PAUSED_BY = "Paused_By"
    PREVIOUSLY_CONTAINED = "Previously_Contained"
    PROPERTIES_MODIFIED_BY = "Properties_Modified_By"
    PROPERTIES_QUERIED = "Properties_Queried"
    PROPERTIES_QUERIED_BY = "Properties_Queried_By"
    READ_FROM = "Read_From"
    READ_FROM_BY = "Read_From_By"
    RECEIVED = "Received"
    RECEIVED_BY = "Received_By"
    RECEIVED_FROM = "Received_From"
    RECEIVED_VIA_UPLOAD = "Received_Via_Upload"
    REDIRECTS_TO = "Redirects_To"
    RELATED_TO = "Related_To"
    RENAMED = "Renamed"
    RENAMED_BY = "Renamed_By"
    RENAMED_FROM = "Renamed_From"
    RENAMED_TO = "Renamed_To"
    RESOLVED_TO = "Resolved_To"
    RESUMED = "Resumed"
    RESUMED_BY = "Resumed_By"
    ROOT_DOMAIN_OF = "Root_Domain_Of"
    SEARCHED_FOR = "Searched_For"
    SEARCHED_FOR_BY = "Searched_For_By"
    SENT = "Sent"
    SENT_BY = "Sent_By"
    SENT_TO = "Sent_To"
    SENT_VIA_UPLOAD = "Sent_Via_Upload"
    SET_FROM = "Set_From"
    SET_TO = "Set_To"
    SIGNED_BY = "Signed_By"
    SUB_DOMAIN_OF = "Sub-domain_Of"
    SUPRA_DOMAIN_OF = "Supra-domain_Of"
    SUSPENDED = "Suspended"
    SUSPENDED_BY = "Suspended_By"
    UNHOOKED = "Unhooked"
    UNHOOKED_BY = "Unhooked_By"
    UNLOCKED = "Unlocked"
    UNLOCKED_BY = "Unlocked_By"
    UNPACKED = "Unpacked"
    UNPACKED_BY = "Unpacked_By"
    UPLOADED = "Uploaded"
    UPLOADED_BY = "Uploaded_By"
    UPLOADED_FROM = "Uploaded_From"
    UPLOADED_TO = "Uploaded_To"
    USED = "Used"
    USED_BY = "Used_By"
    VALUES_ENUMERATED = "Values_Enumerated"
    VALUES_ENUMERATED_BY = "Values_Enumerated_By"
    WRITTEN_TO_BY = "Written_To_By"
    WROTE_TO = "Wrote_To"


class ObservableObjectStateVocab:
    """Vocabulary: ObservableObjectStateVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectStateVocab"
    MEMBERS: frozenset[str] = frozenset({"Active", "Closed", "Does Not Exist", "Exists", "Inactive", "Locked", "Open", "Started", "Stopped", "Unlocked"})

    ACTIVE = "Active"
    CLOSED = "Closed"
    DOES_NOT_EXIST = "Does Not Exist"
    EXISTS = "Exists"
    INACTIVE = "Inactive"
    LOCKED = "Locked"
    OPEN = "Open"
    STARTED = "Started"
    STOPPED = "Stopped"
    UNLOCKED = "Unlocked"


class PartitionTypeVocab:
    """Vocabulary: PartitionTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/PartitionTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"PARTITION_ENTRY_UNUSED", "PARTITION_EXTENDED", "PARTITION_FAT32", "PARTITION_FAT32_XINT13", "PARTITION_FAT_12", "PARTITION_FAT_16", "PARTITION_HUGE", "PARTITION_IFS", "PARTITION_LDM", "PARTITION_NTFT", "PARTITION_OS2BOOTMGR", "PARTITION_PREP", "PARTITION_UNIX", "PARTITION_XENIX_1", "PARTITION_XENIX_2", "PARTITION_XINT13", "PARTITION_XINT13_EXTENDED", "UNKNOWN", "VALID_NTFT"})

    PARTITION_ENTRY_UNUSED = "PARTITION_ENTRY_UNUSED"
    PARTITION_EXTENDED = "PARTITION_EXTENDED"
    PARTITION_FAT32 = "PARTITION_FAT32"
    PARTITION_FAT32_XINT13 = "PARTITION_FAT32_XINT13"
    PARTITION_FAT_12 = "PARTITION_FAT_12"
    PARTITION_FAT_16 = "PARTITION_FAT_16"
    PARTITION_HUGE = "PARTITION_HUGE"
    PARTITION_IFS = "PARTITION_IFS"
    PARTITION_LDM = "PARTITION_LDM"
    PARTITION_NTFT = "PARTITION_NTFT"
    PARTITION_OS2BOOTMGR = "PARTITION_OS2BOOTMGR"
    PARTITION_PREP = "PARTITION_PREP"
    PARTITION_UNIX = "PARTITION_UNIX"
    PARTITION_XENIX_1 = "PARTITION_XENIX_1"
    PARTITION_XENIX_2 = "PARTITION_XENIX_2"
    PARTITION_XINT13 = "PARTITION_XINT13"
    PARTITION_XINT13_EXTENDED = "PARTITION_XINT13_EXTENDED"
    UNKNOWN = "UNKNOWN"
    VALID_NTFT = "VALID_NTFT"


class ProcessorArchVocab:
    """Vocabulary: ProcessorArchVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ProcessorArchVocab"
    MEMBERS: frozenset[str] = frozenset({"ARM", "Alpha", "IA-64", "MIPS", "Motorola 68k", "Other", "PowerPC", "SPARC", "eSi-RISC", "x86-32", "x86-64", "z/Architecture"})

    ARM = "ARM"
    ALPHA = "Alpha"
    IA_64 = "IA-64"
    MIPS = "MIPS"
    MOTOROLA_68K = "Motorola 68k"
    OTHER = "Other"
    POWERPC = "PowerPC"
    SPARC = "SPARC"
    ESI_RISC = "eSi-RISC"
    X86_32 = "x86-32"
    X86_64 = "x86-64"
    Z_ARCHITECTURE = "z/Architecture"


class RecoveredObjectStatusVocab:
    """Vocabulary: RecoveredObjectStatusVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RecoveredObjectStatusVocab"
    MEMBERS: frozenset[str] = frozenset({"overwritten", "partially recovered", "recovered", "unknown"})

    OVERWRITTEN = "overwritten"
    PARTIALLY_RECOVERED = "partially recovered"
    RECOVERED = "recovered"
    UNKNOWN = "unknown"


class RegionalRegistryTypeVocab:
    """Vocabulary: RegionalRegistryTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RegionalRegistryTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"APNIC", "ARIN", "AfriNIC", "LACNIC", "RIPE NCC"})

    APNIC = "APNIC"
    ARIN = "ARIN"
    AFRINIC = "AfriNIC"
    LACNIC = "LACNIC"
    RIPE_NCC = "RIPE NCC"


class RegistryDatatype:
    """Vocabulary: RegistryDatatype"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/RegistryDatatype"
    MEMBERS: frozenset[str] = frozenset({"reg_binary", "reg_dword", "reg_dword_big_endian", "reg_expand_sz", "reg_full_resource_descriptor", "reg_invalid_type", "reg_link", "reg_multi_sz", "reg_none", "reg_qword", "reg_resource_list", "reg_resource_requirements_list", "reg_sz"})

    REG_BINARY = "reg_binary"
    REG_DWORD = "reg_dword"
    REG_DWORD_BIG_ENDIAN = "reg_dword_big_endian"
    REG_EXPAND_SZ = "reg_expand_sz"
    REG_FULL_RESOURCE_DESCRIPTOR = "reg_full_resource_descriptor"
    REG_INVALID_TYPE = "reg_invalid_type"
    REG_LINK = "reg_link"
    REG_MULTI_SZ = "reg_multi_sz"
    REG_NONE = "reg_none"
    REG_QWORD = "reg_qword"
    REG_RESOURCE_LIST = "reg_resource_list"
    REG_RESOURCE_REQUIREMENTS_LIST = "reg_resource_requirements_list"
    REG_SZ = "reg_sz"


class RegistryDatatypeVocab:
    """Vocabulary: RegistryDatatypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RegistryDatatypeVocab"
    MEMBERS: frozenset[str] = frozenset({"reg_binary", "reg_dword", "reg_dword_big_endian", "reg_expand_sz", "reg_full_resource_descriptor", "reg_invalid_type", "reg_link", "reg_multi_sz", "reg_none", "reg_qword", "reg_resource_list", "reg_resource_requirements_list", "reg_sz"})

    REG_BINARY = "reg_binary"
    REG_DWORD = "reg_dword"
    REG_DWORD_BIG_ENDIAN = "reg_dword_big_endian"
    REG_EXPAND_SZ = "reg_expand_sz"
    REG_FULL_RESOURCE_DESCRIPTOR = "reg_full_resource_descriptor"
    REG_INVALID_TYPE = "reg_invalid_type"
    REG_LINK = "reg_link"
    REG_MULTI_SZ = "reg_multi_sz"
    REG_NONE = "reg_none"
    REG_QWORD = "reg_qword"
    REG_RESOURCE_LIST = "reg_resource_list"
    REG_RESOURCE_REQUIREMENTS_LIST = "reg_resource_requirements_list"
    REG_SZ = "reg_sz"


class SIMFormVocab:
    """Vocabulary: SIMFormVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMFormVocab"
    MEMBERS: frozenset[str] = frozenset({"Full-size SIM", "Micro SIM", "Nano SIM"})

    FULL_SIZE_SIM = "Full-size SIM"
    MICRO_SIM = "Micro SIM"
    NANO_SIM = "Nano SIM"


class SIMTypeVocab:
    """Vocabulary: SIMTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"SIM", "UICC", "USIM"})

    SIM = "SIM"
    UICC = "UICC"
    USIM = "USIM"


class TaskActionTypeVocab:
    """Vocabulary: TaskActionTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskActionTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"TASK_ACTION_COM_HANDLER", "TASK_ACTION_EXEC", "TASK_ACTION_SEND_EMAIL", "TASK_ACTION_SHOW_MESSAGE"})

    TASK_ACTION_COM_HANDLER = "TASK_ACTION_COM_HANDLER"
    TASK_ACTION_EXEC = "TASK_ACTION_EXEC"
    TASK_ACTION_SEND_EMAIL = "TASK_ACTION_SEND_EMAIL"
    TASK_ACTION_SHOW_MESSAGE = "TASK_ACTION_SHOW_MESSAGE"


class TaskFlagVocab:
    """Vocabulary: TaskFlagVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskFlagVocab"
    MEMBERS: frozenset[str] = frozenset({"TASK_FLAG_DELETE_WHEN_DONE", "TASK_FLAG_DISABLED", "TASK_FLAG_DONT_START_IF_ON_BATTERIES", "TASK_FLAG_HIDDEN", "TASK_FLAG_INTERACTIVE", "TASK_FLAG_KILL_IF_GOING_ON_BATTERIES", "TASK_FLAG_KILL_ON_IDLE_END", "TASK_FLAG_RESTART_ON_IDLE_RESUME", "TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET", "TASK_FLAG_RUN_ONLY_IF_LOGGED_ON", "TASK_FLAG_START_ONLY_IF_IDLE", "TASK_FLAG_SYSTEM_REQUIRED", "TASK_FLAG_ZERO"})

    TASK_FLAG_DELETE_WHEN_DONE = "TASK_FLAG_DELETE_WHEN_DONE"
    TASK_FLAG_DISABLED = "TASK_FLAG_DISABLED"
    TASK_FLAG_DONT_START_IF_ON_BATTERIES = "TASK_FLAG_DONT_START_IF_ON_BATTERIES"
    TASK_FLAG_HIDDEN = "TASK_FLAG_HIDDEN"
    TASK_FLAG_INTERACTIVE = "TASK_FLAG_INTERACTIVE"
    TASK_FLAG_KILL_IF_GOING_ON_BATTERIES = "TASK_FLAG_KILL_IF_GOING_ON_BATTERIES"
    TASK_FLAG_KILL_ON_IDLE_END = "TASK_FLAG_KILL_ON_IDLE_END"
    TASK_FLAG_RESTART_ON_IDLE_RESUME = "TASK_FLAG_RESTART_ON_IDLE_RESUME"
    TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET = "TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET"
    TASK_FLAG_RUN_ONLY_IF_LOGGED_ON = "TASK_FLAG_RUN_ONLY_IF_LOGGED_ON"
    TASK_FLAG_START_ONLY_IF_IDLE = "TASK_FLAG_START_ONLY_IF_IDLE"
    TASK_FLAG_SYSTEM_REQUIRED = "TASK_FLAG_SYSTEM_REQUIRED"
    TASK_FLAG_ZERO = "TASK_FLAG_ZERO"


class TaskPriorityVocab:
    """Vocabulary: TaskPriorityVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskPriorityVocab"
    MEMBERS: frozenset[str] = frozenset({"ABOVE_NORMAL_PRIORITY_CLASS", "BELOW_NORMAL_PRIORITY_CLASS", "HIGH_PRIORITY_CLASS", "IDLE_PRIORITY_CLASS", "NORMAL_PRIORITY_CLASS", "REALTIME_PRIORITY_CLASS"})

    ABOVE_NORMAL_PRIORITY_CLASS = "ABOVE_NORMAL_PRIORITY_CLASS"
    BELOW_NORMAL_PRIORITY_CLASS = "BELOW_NORMAL_PRIORITY_CLASS"
    HIGH_PRIORITY_CLASS = "HIGH_PRIORITY_CLASS"
    IDLE_PRIORITY_CLASS = "IDLE_PRIORITY_CLASS"
    NORMAL_PRIORITY_CLASS = "NORMAL_PRIORITY_CLASS"
    REALTIME_PRIORITY_CLASS = "REALTIME_PRIORITY_CLASS"


class TaskStatusVocab:
    """Vocabulary: TaskStatusVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskStatusVocab"
    MEMBERS: frozenset[str] = frozenset({"SCHED_E_ACCOUNT_DBASE_CORRUPT", "SCHED_E_ACCOUNT_INFORMATION_NOT_SET", "SCHED_E_ACCOUNT_NAME_NOT_FOUND", "SCHED_E_CANNOT_OPEN_TASK", "SCHED_E_INVALID_TASK", "SCHED_E_NO_SECURITY_SERVICES", "SCHED_E_SERVICE_NOT_INSTALLED", "SCHED_E_SERVICE_NOT_RUNNING", "SCHED_E_TASK_NOT_READY", "SCHED_E_TASK_NOT_RUNNING", "SCHED_E_TRIGGER_NOT_FOUND", "SCHED_E_UNKNOWN_OBJECT_VERSION", "SCHED_E_UNSUPPORTED_ACCOUNT_OPTION", "SCHED_S_EVENT_TRIGGER", "SCHED_S_TASK_DISABLED", "SCHED_S_TASK_HAS_NOT_RUN", "SCHED_S_TASK_NOT_SCHEDULED", "SCHED_S_TASK_NO_MORE_RUNS", "SCHED_S_TASK_NO_VALID_TRIGGERS", "SCHED_S_TASK_READY", "SCHED_S_TASK_RUNNING", "SCHED_S_TASK_TERMINATED", "TASK_STATE_QUEUED", "TASK_STATE_UNKNOWN"})

    SCHED_E_ACCOUNT_DBASE_CORRUPT = "SCHED_E_ACCOUNT_DBASE_CORRUPT"
    SCHED_E_ACCOUNT_INFORMATION_NOT_SET = "SCHED_E_ACCOUNT_INFORMATION_NOT_SET"
    SCHED_E_ACCOUNT_NAME_NOT_FOUND = "SCHED_E_ACCOUNT_NAME_NOT_FOUND"
    SCHED_E_CANNOT_OPEN_TASK = "SCHED_E_CANNOT_OPEN_TASK"
    SCHED_E_INVALID_TASK = "SCHED_E_INVALID_TASK"
    SCHED_E_NO_SECURITY_SERVICES = "SCHED_E_NO_SECURITY_SERVICES"
    SCHED_E_SERVICE_NOT_INSTALLED = "SCHED_E_SERVICE_NOT_INSTALLED"
    SCHED_E_SERVICE_NOT_RUNNING = "SCHED_E_SERVICE_NOT_RUNNING"
    SCHED_E_TASK_NOT_READY = "SCHED_E_TASK_NOT_READY"
    SCHED_E_TASK_NOT_RUNNING = "SCHED_E_TASK_NOT_RUNNING"
    SCHED_E_TRIGGER_NOT_FOUND = "SCHED_E_TRIGGER_NOT_FOUND"
    SCHED_E_UNKNOWN_OBJECT_VERSION = "SCHED_E_UNKNOWN_OBJECT_VERSION"
    SCHED_E_UNSUPPORTED_ACCOUNT_OPTION = "SCHED_E_UNSUPPORTED_ACCOUNT_OPTION"
    SCHED_S_EVENT_TRIGGER = "SCHED_S_EVENT_TRIGGER"
    SCHED_S_TASK_DISABLED = "SCHED_S_TASK_DISABLED"
    SCHED_S_TASK_HAS_NOT_RUN = "SCHED_S_TASK_HAS_NOT_RUN"
    SCHED_S_TASK_NOT_SCHEDULED = "SCHED_S_TASK_NOT_SCHEDULED"
    SCHED_S_TASK_NO_MORE_RUNS = "SCHED_S_TASK_NO_MORE_RUNS"
    SCHED_S_TASK_NO_VALID_TRIGGERS = "SCHED_S_TASK_NO_VALID_TRIGGERS"
    SCHED_S_TASK_READY = "SCHED_S_TASK_READY"
    SCHED_S_TASK_RUNNING = "SCHED_S_TASK_RUNNING"
    SCHED_S_TASK_TERMINATED = "SCHED_S_TASK_TERMINATED"
    TASK_STATE_QUEUED = "TASK_STATE_QUEUED"
    TASK_STATE_UNKNOWN = "TASK_STATE_UNKNOWN"


class ThreadRunningStatusVocab:
    """Vocabulary: ThreadRunningStatusVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ThreadRunningStatusVocab"
    MEMBERS: frozenset[str] = frozenset({"Initialized", "Ready", "Running", "Standby", "Terminated", "Transition", "Unknown", "Waiting"})

    INITIALIZED = "Initialized"
    READY = "Ready"
    RUNNING = "Running"
    STANDBY = "Standby"
    TERMINATED = "Terminated"
    TRANSITION = "Transition"
    UNKNOWN = "Unknown"
    WAITING = "Waiting"


class TimestampPrecisionVocab:
    """Vocabulary: TimestampPrecisionVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TimestampPrecisionVocab"
    MEMBERS: frozenset[str] = frozenset({"day", "hour", "minute", "month", "second", "year"})

    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    MONTH = "month"
    SECOND = "second"
    YEAR = "year"


class TrendVocab:
    """Vocabulary: TrendVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TrendVocab"
    MEMBERS: frozenset[str] = frozenset({"Decreasing", "Increasing"})

    DECREASING = "Decreasing"
    INCREASING = "Increasing"


class TriggerFrequencyVocab:
    """Vocabulary: TriggerFrequencyVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerFrequencyVocab"
    MEMBERS: frozenset[str] = frozenset({"TASK_EVENT_TRIGGER_AT_LOGON", "TASK_EVENT_TRIGGER_AT_SYSTEMSTART", "TASK_EVENT_TRIGGER_ON_IDLE", "TASK_TIME_TRIGGER_DAILY", "TASK_TIME_TRIGGER_MONTHLYDATE", "TASK_TIME_TRIGGER_MONTHLYDOW", "TASK_TIME_TRIGGER_ONCE", "TASK_TIME_TRIGGER_WEEKLY"})

    TASK_EVENT_TRIGGER_AT_LOGON = "TASK_EVENT_TRIGGER_AT_LOGON"
    TASK_EVENT_TRIGGER_AT_SYSTEMSTART = "TASK_EVENT_TRIGGER_AT_SYSTEMSTART"
    TASK_EVENT_TRIGGER_ON_IDLE = "TASK_EVENT_TRIGGER_ON_IDLE"
    TASK_TIME_TRIGGER_DAILY = "TASK_TIME_TRIGGER_DAILY"
    TASK_TIME_TRIGGER_MONTHLYDATE = "TASK_TIME_TRIGGER_MONTHLYDATE"
    TASK_TIME_TRIGGER_MONTHLYDOW = "TASK_TIME_TRIGGER_MONTHLYDOW"
    TASK_TIME_TRIGGER_ONCE = "TASK_TIME_TRIGGER_ONCE"
    TASK_TIME_TRIGGER_WEEKLY = "TASK_TIME_TRIGGER_WEEKLY"


class TriggerTypeVocab:
    """Vocabulary: TriggerTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"TASK_TRIGGER_BOOT", "TASK_TRIGGER_EVENT", "TASK_TRIGGER_IDLE", "TASK_TRIGGER_LOGON", "TASK_TRIGGER_REGISTRATION", "TASK_TRIGGER_SESSION_STATE_CHANGE", "TASK_TRIGGER_TIME"})

    TASK_TRIGGER_BOOT = "TASK_TRIGGER_BOOT"
    TASK_TRIGGER_EVENT = "TASK_TRIGGER_EVENT"
    TASK_TRIGGER_IDLE = "TASK_TRIGGER_IDLE"
    TASK_TRIGGER_LOGON = "TASK_TRIGGER_LOGON"
    TASK_TRIGGER_REGISTRATION = "TASK_TRIGGER_REGISTRATION"
    TASK_TRIGGER_SESSION_STATE_CHANGE = "TASK_TRIGGER_SESSION_STATE_CHANGE"
    TASK_TRIGGER_TIME = "TASK_TRIGGER_TIME"


class URLTransitionTypeVocab:
    """Vocabulary: URLTransitionTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/URLTransitionTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"auto_bookmark", "auto_subframe", "auto_toplevel", "form_submit", "generated", "keyword", "keyword_generated", "link", "manual_subframe", "reload", "typed"})

    AUTO_BOOKMARK = "auto_bookmark"
    AUTO_SUBFRAME = "auto_subframe"
    AUTO_TOPLEVEL = "auto_toplevel"
    FORM_SUBMIT = "form_submit"
    GENERATED = "generated"
    KEYWORD = "keyword"
    KEYWORD_GENERATED = "keyword_generated"
    LINK = "link"
    MANUAL_SUBFRAME = "manual_subframe"
    RELOAD = "reload"
    TYPED = "typed"


class UnixProcessStateVocab:
    """Vocabulary: UnixProcessStateVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/UnixProcessStateVocab"
    MEMBERS: frozenset[str] = frozenset({"Dead", "InterruptibleSleep", "Paging", "Running", "Stopped", "UninterruptibleSleep", "Zombie"})

    DEAD = "Dead"
    INTERRUPTIBLESLEEP = "InterruptibleSleep"
    PAGING = "Paging"
    RUNNING = "Running"
    STOPPED = "Stopped"
    UNINTERRUPTIBLESLEEP = "UninterruptibleSleep"
    ZOMBIE = "Zombie"


class WhoisContactTypeVocab:
    """Vocabulary: WhoisContactTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisContactTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"ADMIN", "BILLING", "TECHNICAL"})

    ADMIN = "ADMIN"
    BILLING = "BILLING"
    TECHNICAL = "TECHNICAL"


class WhoisDNSSECTypeVocab:
    """Vocabulary: WhoisDNSSECTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"Signed", "Unsigned"})

    SIGNED = "Signed"
    UNSIGNED = "Unsigned"


class WhoisStatusTypeVocab:
    """Vocabulary: WhoisStatusTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisStatusTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"ADD_PERIOD", "AUTO_RENEW_PERIOD", "CLIENT_DELETE_PROHIBITED", "CLIENT_HOLD", "CLIENT_RENEW_PROHIBITED", "CLIENT_TRANSFER_PROHIBITED", "CLIENT_UPDATE_PROHIBITED", "DELETE_PROHIBITED", "HOLD", "INACTIVE", "OK", "PENDING_DELETE_RESTORABLE", "PENDING_DELETE_SCHEDULED_FOR_RELEASE", "PENDING_RESTORE", "RENEW_PERIOD", "RENEW_PROHIBITED", "TRANSFER_PERIOD", "TRANSFER_PROHIBITED", "UPDATE_PROHIBITED"})

    ADD_PERIOD = "ADD_PERIOD"
    AUTO_RENEW_PERIOD = "AUTO_RENEW_PERIOD"
    CLIENT_DELETE_PROHIBITED = "CLIENT_DELETE_PROHIBITED"
    CLIENT_HOLD = "CLIENT_HOLD"
    CLIENT_RENEW_PROHIBITED = "CLIENT_RENEW_PROHIBITED"
    CLIENT_TRANSFER_PROHIBITED = "CLIENT_TRANSFER_PROHIBITED"
    CLIENT_UPDATE_PROHIBITED = "CLIENT_UPDATE_PROHIBITED"
    DELETE_PROHIBITED = "DELETE_PROHIBITED"
    HOLD = "HOLD"
    INACTIVE = "INACTIVE"
    OK = "OK"
    PENDING_DELETE_RESTORABLE = "PENDING_DELETE_RESTORABLE"
    PENDING_DELETE_SCHEDULED_FOR_RELEASE = "PENDING_DELETE_SCHEDULED_FOR_RELEASE"
    PENDING_RESTORE = "PENDING_RESTORE"
    RENEW_PERIOD = "RENEW_PERIOD"
    RENEW_PROHIBITED = "RENEW_PROHIBITED"
    TRANSFER_PERIOD = "TRANSFER_PERIOD"
    TRANSFER_PROHIBITED = "TRANSFER_PROHIBITED"
    UPDATE_PROHIBITED = "UPDATE_PROHIBITED"


class WindowsDriveTypeVocab:
    """Vocabulary: WindowsDriveTypeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsDriveTypeVocab"
    MEMBERS: frozenset[str] = frozenset({"DRIVE_CDROM", "DRIVE_FIXED", "DRIVE_NO_ROOT_DIR", "DRIVE_RAMDISK", "DRIVE_REMOTE", "DRIVE_REMOVABLE", "DRIVE_UNKNOWN"})

    DRIVE_CDROM = "DRIVE_CDROM"
    DRIVE_FIXED = "DRIVE_FIXED"
    DRIVE_NO_ROOT_DIR = "DRIVE_NO_ROOT_DIR"
    DRIVE_RAMDISK = "DRIVE_RAMDISK"
    DRIVE_REMOTE = "DRIVE_REMOTE"
    DRIVE_REMOVABLE = "DRIVE_REMOVABLE"
    DRIVE_UNKNOWN = "DRIVE_UNKNOWN"


class WindowsPEBinaryType:
    """Vocabulary: WindowsPEBinaryType"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryType"
    MEMBERS: frozenset[str] = frozenset({"dll", "exe", "sys"})

    DLL = "dll"
    EXE = "exe"
    SYS = "sys"


class WindowsServiceStartType:
    """Vocabulary: WindowsServiceStartType"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStartType"
    MEMBERS: frozenset[str] = frozenset({"service_auto_start", "service_boot_start", "service_demand_start", "service_disabled", "service_system_alert"})

    SERVICE_AUTO_START = "service_auto_start"
    SERVICE_BOOT_START = "service_boot_start"
    SERVICE_DEMAND_START = "service_demand_start"
    SERVICE_DISABLED = "service_disabled"
    SERVICE_SYSTEM_ALERT = "service_system_alert"


class WindowsServiceStatus:
    """Vocabulary: WindowsServiceStatus"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStatus"
    MEMBERS: frozenset[str] = frozenset({"service_continue_pending", "service_pause_pending", "service_paused", "service_running", "service_start_pending", "service_stop_pending", "service_stopped"})

    SERVICE_CONTINUE_PENDING = "service_continue_pending"
    SERVICE_PAUSE_PENDING = "service_pause_pending"
    SERVICE_PAUSED = "service_paused"
    SERVICE_RUNNING = "service_running"
    SERVICE_START_PENDING = "service_start_pending"
    SERVICE_STOP_PENDING = "service_stop_pending"
    SERVICE_STOPPED = "service_stopped"


class WindowsServiceType:
    """Vocabulary: WindowsServiceType"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceType"
    MEMBERS: frozenset[str] = frozenset({"service_file_system_driver", "service_kernel_driver", "service_win32_own_process", "service_win32_share_process"})

    SERVICE_FILE_SYSTEM_DRIVER = "service_file_system_driver"
    SERVICE_KERNEL_DRIVER = "service_kernel_driver"
    SERVICE_WIN32_OWN_PROCESS = "service_win32_own_process"
    SERVICE_WIN32_SHARE_PROCESS = "service_win32_share_process"


class WindowsVolumeAttributeVocab:
    """Vocabulary: WindowsVolumeAttributeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab"
    MEMBERS: frozenset[str] = frozenset({"Hidden", "NoDefaultDriveLetter", "ReadOnly", "ShadowCopy"})

    HIDDEN = "Hidden"
    NODEFAULTDRIVELETTER = "NoDefaultDriveLetter"
    READONLY = "ReadOnly"
    SHADOWCOPY = "ShadowCopy"


class WirelessNetworkSecurityModeVocab:
    """Vocabulary: WirelessNetworkSecurityModeVocab"""
    IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WirelessNetworkSecurityModeVocab"
    MEMBERS: frozenset[str] = frozenset({"None", "WEP", "WPA", "WPA2-Enterprise", "WPA2-PSK", "WPA3-Enterprise", "WPA3-PSK"})

    NONE = "None"
    WEP = "WEP"
    WPA = "WPA"
    WPA2_ENTERPRISE = "WPA2-Enterprise"
    WPA2_PSK = "WPA2-PSK"
    WPA3_ENTERPRISE = "WPA3-Enterprise"
    WPA3_PSK = "WPA3-PSK"


VOCABULARIES: dict[str, type] = {
    "AccountTypeVocab": AccountTypeVocab,
    "ActionArgumentNameVocab": ActionArgumentNameVocab,
    "ActionNameVocab": ActionNameVocab,
    "ActionRelationshipTypeVocab": ActionRelationshipTypeVocab,
    "ActionStatusTypeVocab": ActionStatusTypeVocab,
    "ActionTypeVocab": ActionTypeVocab,
    "BitnessVocab": BitnessVocab,
    "CharacterEncodingVocab": CharacterEncodingVocab,
    "ContactAddressScopeVocab": ContactAddressScopeVocab,
    "ContactEmailScopeVocab": ContactEmailScopeVocab,
    "ContactPhoneScopeVocab": ContactPhoneScopeVocab,
    "ContactSIPScopeVocab": ContactSIPScopeVocab,
    "ContactURLScopeVocab": ContactURLScopeVocab,
    "DiskTypeVocab": DiskTypeVocab,
    "EndiannessTypeVocab": EndiannessTypeVocab,
    "HashNameVocab": HashNameVocab,
    "LibraryTypeVocab": LibraryTypeVocab,
    "MemoryBlockTypeVocab": MemoryBlockTypeVocab,
    "NetworkSocketAddressFamily": NetworkSocketAddressFamily,
    "NetworkSocketProtocolFamily": NetworkSocketProtocolFamily,
    "NetworkSocketType": NetworkSocketType,
    "ObjectStatusVocab": ObjectStatusVocab,
    "ObservableObjectRelationshipVocab": ObservableObjectRelationshipVocab,
    "ObservableObjectStateVocab": ObservableObjectStateVocab,
    "PartitionTypeVocab": PartitionTypeVocab,
    "ProcessorArchVocab": ProcessorArchVocab,
    "RecoveredObjectStatusVocab": RecoveredObjectStatusVocab,
    "RegionalRegistryTypeVocab": RegionalRegistryTypeVocab,
    "RegistryDatatype": RegistryDatatype,
    "RegistryDatatypeVocab": RegistryDatatypeVocab,
    "SIMFormVocab": SIMFormVocab,
    "SIMTypeVocab": SIMTypeVocab,
    "TaskActionTypeVocab": TaskActionTypeVocab,
    "TaskFlagVocab": TaskFlagVocab,
    "TaskPriorityVocab": TaskPriorityVocab,
    "TaskStatusVocab": TaskStatusVocab,
    "ThreadRunningStatusVocab": ThreadRunningStatusVocab,
    "TimestampPrecisionVocab": TimestampPrecisionVocab,
    "TrendVocab": TrendVocab,
    "TriggerFrequencyVocab": TriggerFrequencyVocab,
    "TriggerTypeVocab": TriggerTypeVocab,
    "URLTransitionTypeVocab": URLTransitionTypeVocab,
    "UnixProcessStateVocab": UnixProcessStateVocab,
    "WhoisContactTypeVocab": WhoisContactTypeVocab,
    "WhoisDNSSECTypeVocab": WhoisDNSSECTypeVocab,
    "WhoisStatusTypeVocab": WhoisStatusTypeVocab,
    "WindowsDriveTypeVocab": WindowsDriveTypeVocab,
    "WindowsPEBinaryType": WindowsPEBinaryType,
    "WindowsServiceStartType": WindowsServiceStartType,
    "WindowsServiceStatus": WindowsServiceStatus,
    "WindowsServiceType": WindowsServiceType,
    "WindowsVolumeAttributeVocab": WindowsVolumeAttributeVocab,
    "WirelessNetworkSecurityModeVocab": WirelessNetworkSecurityModeVocab,
}
