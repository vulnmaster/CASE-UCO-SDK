//! Auto-generated UCO vocabularies for the CASE/UCO ontology.
//!
//! Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.

/// Vocabulary: AccountTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct AccountTypeVocab;

impl AccountTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/AccountTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["ldap", "nis", "openid", "radius", "tacacs", "unix", "windows_domain", "windows_local"];
    pub const LDAP: &'static str = "ldap";
    pub const NIS: &'static str = "nis";
    pub const OPENID: &'static str = "openid";
    pub const RADIUS: &'static str = "radius";
    pub const TACACS: &'static str = "tacacs";
    pub const UNIX: &'static str = "unix";
    pub const WINDOWS_DOMAIN: &'static str = "windows_domain";
    pub const WINDOWS_LOCAL: &'static str = "windows_local";
}

/// Vocabulary: ActionArgumentNameVocab
#[derive(Debug, Clone, Copy)]
pub struct ActionArgumentNameVocab;

impl ActionArgumentNameVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionArgumentNameVocab";
    pub const MEMBERS: &'static [&'static str] = &["APC Address", "APC Mode", "API", "Access Mode", "Application Name", "Base Address", "Callback Address", "Code Address", "Command", "Control Code", "Control Parameter", "Creation Flags", "Database Name", "Delay Time (ms)", "Destination Address", "Error Control", "File Information Class", "Flags", "Function Address", "Function Name", "Function Ordinal", "Hook Type", "Host Name", "Hostname", "Initial Owner", "Mapping Offset", "Number of Bytes Per Send", "Options", "Parameter Address", "Password", "Privilege Name", "Protection", "Proxy Bypass", "Proxy Name", "Reason", "Request Size", "Requested Version", "Server", "Service Name", "Service State", "Service Type", "Share Mode", "Shutdown Flag", "Size (bytes)", "Sleep Time (ms)", "Source Address", "Starting Address", "System Metric Index", "Target PID", "Transfer Flags", "Username"];
    pub const APC_ADDRESS: &'static str = "APC Address";
    pub const APC_MODE: &'static str = "APC Mode";
    pub const API: &'static str = "API";
    pub const ACCESS_MODE: &'static str = "Access Mode";
    pub const APPLICATION_NAME: &'static str = "Application Name";
    pub const BASE_ADDRESS: &'static str = "Base Address";
    pub const CALLBACK_ADDRESS: &'static str = "Callback Address";
    pub const CODE_ADDRESS: &'static str = "Code Address";
    pub const COMMAND: &'static str = "Command";
    pub const CONTROL_CODE: &'static str = "Control Code";
    pub const CONTROL_PARAMETER: &'static str = "Control Parameter";
    pub const CREATION_FLAGS: &'static str = "Creation Flags";
    pub const DATABASE_NAME: &'static str = "Database Name";
    pub const DELAY_TIME_MS: &'static str = "Delay Time (ms)";
    pub const DESTINATION_ADDRESS: &'static str = "Destination Address";
    pub const ERROR_CONTROL: &'static str = "Error Control";
    pub const FILE_INFORMATION_CLASS: &'static str = "File Information Class";
    pub const FLAGS: &'static str = "Flags";
    pub const FUNCTION_ADDRESS: &'static str = "Function Address";
    pub const FUNCTION_NAME: &'static str = "Function Name";
    pub const FUNCTION_ORDINAL: &'static str = "Function Ordinal";
    pub const HOOK_TYPE: &'static str = "Hook Type";
    pub const HOST_NAME: &'static str = "Host Name";
    pub const HOSTNAME: &'static str = "Hostname";
    pub const INITIAL_OWNER: &'static str = "Initial Owner";
    pub const MAPPING_OFFSET: &'static str = "Mapping Offset";
    pub const NUMBER_OF_BYTES_PER_SEND: &'static str = "Number of Bytes Per Send";
    pub const OPTIONS: &'static str = "Options";
    pub const PARAMETER_ADDRESS: &'static str = "Parameter Address";
    pub const PASSWORD: &'static str = "Password";
    pub const PRIVILEGE_NAME: &'static str = "Privilege Name";
    pub const PROTECTION: &'static str = "Protection";
    pub const PROXY_BYPASS: &'static str = "Proxy Bypass";
    pub const PROXY_NAME: &'static str = "Proxy Name";
    pub const REASON: &'static str = "Reason";
    pub const REQUEST_SIZE: &'static str = "Request Size";
    pub const REQUESTED_VERSION: &'static str = "Requested Version";
    pub const SERVER: &'static str = "Server";
    pub const SERVICE_NAME: &'static str = "Service Name";
    pub const SERVICE_STATE: &'static str = "Service State";
    pub const SERVICE_TYPE: &'static str = "Service Type";
    pub const SHARE_MODE: &'static str = "Share Mode";
    pub const SHUTDOWN_FLAG: &'static str = "Shutdown Flag";
    pub const SIZE_BYTES: &'static str = "Size (bytes)";
    pub const SLEEP_TIME_MS: &'static str = "Sleep Time (ms)";
    pub const SOURCE_ADDRESS: &'static str = "Source Address";
    pub const STARTING_ADDRESS: &'static str = "Starting Address";
    pub const SYSTEM_METRIC_INDEX: &'static str = "System Metric Index";
    pub const TARGET_PID: &'static str = "Target PID";
    pub const TRANSFER_FLAGS: &'static str = "Transfer Flags";
    pub const USERNAME: &'static str = "Username";
}

/// Vocabulary: ActionNameVocab
#[derive(Debug, Clone, Copy)]
pub struct ActionNameVocab;

impl ActionNameVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionNameVocab";
    pub const MEMBERS: &'static [&'static str] = &["Accept Socket Connection", "Add Connection to Network Share", "Add Network Share", "Add Scheduled Task", "Add System Call Hook", "Add User", "Add Windows Hook", "Allocate Virtual Memory in Process", "Bind Address to Socket", "Change Service Configuration", "Check for Remote Debugger", "Close Port", "Close Registry Key", "Close Socket", "Configure Service", "Connect to IP", "Connect to Named Pipe", "Connect to Network Share", "Connect to Socket", "Connect to URL", "Control Driver", "Control Service", "Copy File", "Create Dialog Box", "Create Directory", "Create Event", "Create File", "Create File Alternate Data Stream", "Create File Mapping", "Create File Symbolic Link", "Create Hidden File", "Create Mailslot", "Create Module", "Create Mutex", "Create Named Pipe", "Create Process", "Create Process as User", "Create Registry Key", "Create Registry Key Value", "Create Remote Thread in Process", "Create Service", "Create Socket", "Create Symbolic Link", "Create Thread", "Create Window", "Delete Directory", "Delete File", "Delete Named Pipe", "Delete Network Share", "Delete Registry Key", "Delete Registry Key Value", "Delete Service", "Delete User", "Disconnect from Named Pipe", "Disconnect from Network Share", "Disconnect from Socket", "Download File", "Enumerate DLLs", "Enumerate Network Shares", "Enumerate Processes", "Enumerate Protocols", "Enumerate Registry Key Subkeys", "Enumerate Registry Key Values", "Enumerate Services", "Enumerate System Handles", "Enumerate Threads", "Enumerate Threads in Process", "Enumerate Users", "Enumerate Windows", "Find File", "Find Window", "Flush Process Instruction Cache", "Free Library", "Free Process Virtual Memory", "Get Disk Free Space", "Get Disk Type", "Get Elapsed System Up Time", "Get File Attributes", "Get Function Address", "Get Host By Address", "Get Host By Name", "Get Host Name", "Get Library File Name", "Get Library Handle", "Get NetBIOS Name", "Get Process Current Directory", "Get Process Environment Variable", "Get Process Startup Information", "Get Processes Snapshot", "Get Registry Key Attributes", "Get Service Status", "Get System Global Flags", "Get System Host Name", "Get System Local Time", "Get System NetBIOS Name", "Get System Network Parameters", "Get System Time", "Get Thread Context", "Get Thread Username", "Get User Attributes", "Get Username", "Get Windows Directory", "Get Windows System Directory", "Get Windows Temporary Files Directory", "Hide Window", "Impersonate Process", "Impersonate Thread", "Inject Memory Page", "Kill Process", "Kill Thread", "Kill Window", "Listen on Port", "Listen on Socket", "Load Driver", "Load Library", "Load Module", "Load and Call Driver", "Lock File", "Logon as User", "Map File", "Map Library", "Map View of File", "Modify File", "Modify Named Pipe", "Modify Process", "Modify Registry Key", "Modify Registry Key Value", "Modify Service", "Monitor Registry Key", "Move File", "Open File", "Open File Mapping", "Open Mutex", "Open Port", "Open Process", "Open Registry Key", "Open Service", "Open Service Control Manager", "Protect Virtual Memory", "Query DNS", "Query Disk Attributes", "Query Process Virtual Memory", "Queue APC in Thread", "Read File", "Read From Named Pipe", "Read From Process Memory", "Read Registry Key Value", "Receive Data on Socket", "Receive Email Message", "Release Mutex", "Rename File", "Revert Thread to Self", "Send Control Code to File", "Send Control Code to Pipe", "Send Control Code to Service", "Send DNS Query", "Send Data on Socket", "Send Data to Address on Socket", "Send Email Message", "Send ICMP Request", "Send Reverse DNS Query", "Set File Attributes", "Set NetBIOS Name", "Set Process Current Directory", "Set Process Environment Variable", "Set System Global Flags", "Set System Host Name", "Set System Time", "Set Thread Context", "Show Window", "Shutdown System", "Sleep Process", "Sleep System", "Start Service", "Unload Driver", "Unload Module", "Unlock File", "Unmap File", "Upload File", "Write to File", "Write to Process Virtual Memory"];
    pub const ACCEPT_SOCKET_CONNECTION: &'static str = "Accept Socket Connection";
    pub const ADD_CONNECTION_TO_NETWORK_SHARE: &'static str = "Add Connection to Network Share";
    pub const ADD_NETWORK_SHARE: &'static str = "Add Network Share";
    pub const ADD_SCHEDULED_TASK: &'static str = "Add Scheduled Task";
    pub const ADD_SYSTEM_CALL_HOOK: &'static str = "Add System Call Hook";
    pub const ADD_USER: &'static str = "Add User";
    pub const ADD_WINDOWS_HOOK: &'static str = "Add Windows Hook";
    pub const ALLOCATE_VIRTUAL_MEMORY_IN_PROCESS: &'static str = "Allocate Virtual Memory in Process";
    pub const BIND_ADDRESS_TO_SOCKET: &'static str = "Bind Address to Socket";
    pub const CHANGE_SERVICE_CONFIGURATION: &'static str = "Change Service Configuration";
    pub const CHECK_FOR_REMOTE_DEBUGGER: &'static str = "Check for Remote Debugger";
    pub const CLOSE_PORT: &'static str = "Close Port";
    pub const CLOSE_REGISTRY_KEY: &'static str = "Close Registry Key";
    pub const CLOSE_SOCKET: &'static str = "Close Socket";
    pub const CONFIGURE_SERVICE: &'static str = "Configure Service";
    pub const CONNECT_TO_IP: &'static str = "Connect to IP";
    pub const CONNECT_TO_NAMED_PIPE: &'static str = "Connect to Named Pipe";
    pub const CONNECT_TO_NETWORK_SHARE: &'static str = "Connect to Network Share";
    pub const CONNECT_TO_SOCKET: &'static str = "Connect to Socket";
    pub const CONNECT_TO_URL: &'static str = "Connect to URL";
    pub const CONTROL_DRIVER: &'static str = "Control Driver";
    pub const CONTROL_SERVICE: &'static str = "Control Service";
    pub const COPY_FILE: &'static str = "Copy File";
    pub const CREATE_DIALOG_BOX: &'static str = "Create Dialog Box";
    pub const CREATE_DIRECTORY: &'static str = "Create Directory";
    pub const CREATE_EVENT: &'static str = "Create Event";
    pub const CREATE_FILE: &'static str = "Create File";
    pub const CREATE_FILE_ALTERNATE_DATA_STREAM: &'static str = "Create File Alternate Data Stream";
    pub const CREATE_FILE_MAPPING: &'static str = "Create File Mapping";
    pub const CREATE_FILE_SYMBOLIC_LINK: &'static str = "Create File Symbolic Link";
    pub const CREATE_HIDDEN_FILE: &'static str = "Create Hidden File";
    pub const CREATE_MAILSLOT: &'static str = "Create Mailslot";
    pub const CREATE_MODULE: &'static str = "Create Module";
    pub const CREATE_MUTEX: &'static str = "Create Mutex";
    pub const CREATE_NAMED_PIPE: &'static str = "Create Named Pipe";
    pub const CREATE_PROCESS: &'static str = "Create Process";
    pub const CREATE_PROCESS_AS_USER: &'static str = "Create Process as User";
    pub const CREATE_REGISTRY_KEY: &'static str = "Create Registry Key";
    pub const CREATE_REGISTRY_KEY_VALUE: &'static str = "Create Registry Key Value";
    pub const CREATE_REMOTE_THREAD_IN_PROCESS: &'static str = "Create Remote Thread in Process";
    pub const CREATE_SERVICE: &'static str = "Create Service";
    pub const CREATE_SOCKET: &'static str = "Create Socket";
    pub const CREATE_SYMBOLIC_LINK: &'static str = "Create Symbolic Link";
    pub const CREATE_THREAD: &'static str = "Create Thread";
    pub const CREATE_WINDOW: &'static str = "Create Window";
    pub const DELETE_DIRECTORY: &'static str = "Delete Directory";
    pub const DELETE_FILE: &'static str = "Delete File";
    pub const DELETE_NAMED_PIPE: &'static str = "Delete Named Pipe";
    pub const DELETE_NETWORK_SHARE: &'static str = "Delete Network Share";
    pub const DELETE_REGISTRY_KEY: &'static str = "Delete Registry Key";
    pub const DELETE_REGISTRY_KEY_VALUE: &'static str = "Delete Registry Key Value";
    pub const DELETE_SERVICE: &'static str = "Delete Service";
    pub const DELETE_USER: &'static str = "Delete User";
    pub const DISCONNECT_FROM_NAMED_PIPE: &'static str = "Disconnect from Named Pipe";
    pub const DISCONNECT_FROM_NETWORK_SHARE: &'static str = "Disconnect from Network Share";
    pub const DISCONNECT_FROM_SOCKET: &'static str = "Disconnect from Socket";
    pub const DOWNLOAD_FILE: &'static str = "Download File";
    pub const ENUMERATE_DLLS: &'static str = "Enumerate DLLs";
    pub const ENUMERATE_NETWORK_SHARES: &'static str = "Enumerate Network Shares";
    pub const ENUMERATE_PROCESSES: &'static str = "Enumerate Processes";
    pub const ENUMERATE_PROTOCOLS: &'static str = "Enumerate Protocols";
    pub const ENUMERATE_REGISTRY_KEY_SUBKEYS: &'static str = "Enumerate Registry Key Subkeys";
    pub const ENUMERATE_REGISTRY_KEY_VALUES: &'static str = "Enumerate Registry Key Values";
    pub const ENUMERATE_SERVICES: &'static str = "Enumerate Services";
    pub const ENUMERATE_SYSTEM_HANDLES: &'static str = "Enumerate System Handles";
    pub const ENUMERATE_THREADS: &'static str = "Enumerate Threads";
    pub const ENUMERATE_THREADS_IN_PROCESS: &'static str = "Enumerate Threads in Process";
    pub const ENUMERATE_USERS: &'static str = "Enumerate Users";
    pub const ENUMERATE_WINDOWS: &'static str = "Enumerate Windows";
    pub const FIND_FILE: &'static str = "Find File";
    pub const FIND_WINDOW: &'static str = "Find Window";
    pub const FLUSH_PROCESS_INSTRUCTION_CACHE: &'static str = "Flush Process Instruction Cache";
    pub const FREE_LIBRARY: &'static str = "Free Library";
    pub const FREE_PROCESS_VIRTUAL_MEMORY: &'static str = "Free Process Virtual Memory";
    pub const GET_DISK_FREE_SPACE: &'static str = "Get Disk Free Space";
    pub const GET_DISK_TYPE: &'static str = "Get Disk Type";
    pub const GET_ELAPSED_SYSTEM_UP_TIME: &'static str = "Get Elapsed System Up Time";
    pub const GET_FILE_ATTRIBUTES: &'static str = "Get File Attributes";
    pub const GET_FUNCTION_ADDRESS: &'static str = "Get Function Address";
    pub const GET_HOST_BY_ADDRESS: &'static str = "Get Host By Address";
    pub const GET_HOST_BY_NAME: &'static str = "Get Host By Name";
    pub const GET_HOST_NAME: &'static str = "Get Host Name";
    pub const GET_LIBRARY_FILE_NAME: &'static str = "Get Library File Name";
    pub const GET_LIBRARY_HANDLE: &'static str = "Get Library Handle";
    pub const GET_NETBIOS_NAME: &'static str = "Get NetBIOS Name";
    pub const GET_PROCESS_CURRENT_DIRECTORY: &'static str = "Get Process Current Directory";
    pub const GET_PROCESS_ENVIRONMENT_VARIABLE: &'static str = "Get Process Environment Variable";
    pub const GET_PROCESS_STARTUP_INFORMATION: &'static str = "Get Process Startup Information";
    pub const GET_PROCESSES_SNAPSHOT: &'static str = "Get Processes Snapshot";
    pub const GET_REGISTRY_KEY_ATTRIBUTES: &'static str = "Get Registry Key Attributes";
    pub const GET_SERVICE_STATUS: &'static str = "Get Service Status";
    pub const GET_SYSTEM_GLOBAL_FLAGS: &'static str = "Get System Global Flags";
    pub const GET_SYSTEM_HOST_NAME: &'static str = "Get System Host Name";
    pub const GET_SYSTEM_LOCAL_TIME: &'static str = "Get System Local Time";
    pub const GET_SYSTEM_NETBIOS_NAME: &'static str = "Get System NetBIOS Name";
    pub const GET_SYSTEM_NETWORK_PARAMETERS: &'static str = "Get System Network Parameters";
    pub const GET_SYSTEM_TIME: &'static str = "Get System Time";
    pub const GET_THREAD_CONTEXT: &'static str = "Get Thread Context";
    pub const GET_THREAD_USERNAME: &'static str = "Get Thread Username";
    pub const GET_USER_ATTRIBUTES: &'static str = "Get User Attributes";
    pub const GET_USERNAME: &'static str = "Get Username";
    pub const GET_WINDOWS_DIRECTORY: &'static str = "Get Windows Directory";
    pub const GET_WINDOWS_SYSTEM_DIRECTORY: &'static str = "Get Windows System Directory";
    pub const GET_WINDOWS_TEMPORARY_FILES_DIRECTORY: &'static str = "Get Windows Temporary Files Directory";
    pub const HIDE_WINDOW: &'static str = "Hide Window";
    pub const IMPERSONATE_PROCESS: &'static str = "Impersonate Process";
    pub const IMPERSONATE_THREAD: &'static str = "Impersonate Thread";
    pub const INJECT_MEMORY_PAGE: &'static str = "Inject Memory Page";
    pub const KILL_PROCESS: &'static str = "Kill Process";
    pub const KILL_THREAD: &'static str = "Kill Thread";
    pub const KILL_WINDOW: &'static str = "Kill Window";
    pub const LISTEN_ON_PORT: &'static str = "Listen on Port";
    pub const LISTEN_ON_SOCKET: &'static str = "Listen on Socket";
    pub const LOAD_DRIVER: &'static str = "Load Driver";
    pub const LOAD_LIBRARY: &'static str = "Load Library";
    pub const LOAD_MODULE: &'static str = "Load Module";
    pub const LOAD_AND_CALL_DRIVER: &'static str = "Load and Call Driver";
    pub const LOCK_FILE: &'static str = "Lock File";
    pub const LOGON_AS_USER: &'static str = "Logon as User";
    pub const MAP_FILE: &'static str = "Map File";
    pub const MAP_LIBRARY: &'static str = "Map Library";
    pub const MAP_VIEW_OF_FILE: &'static str = "Map View of File";
    pub const MODIFY_FILE: &'static str = "Modify File";
    pub const MODIFY_NAMED_PIPE: &'static str = "Modify Named Pipe";
    pub const MODIFY_PROCESS: &'static str = "Modify Process";
    pub const MODIFY_REGISTRY_KEY: &'static str = "Modify Registry Key";
    pub const MODIFY_REGISTRY_KEY_VALUE: &'static str = "Modify Registry Key Value";
    pub const MODIFY_SERVICE: &'static str = "Modify Service";
    pub const MONITOR_REGISTRY_KEY: &'static str = "Monitor Registry Key";
    pub const MOVE_FILE: &'static str = "Move File";
    pub const OPEN_FILE: &'static str = "Open File";
    pub const OPEN_FILE_MAPPING: &'static str = "Open File Mapping";
    pub const OPEN_MUTEX: &'static str = "Open Mutex";
    pub const OPEN_PORT: &'static str = "Open Port";
    pub const OPEN_PROCESS: &'static str = "Open Process";
    pub const OPEN_REGISTRY_KEY: &'static str = "Open Registry Key";
    pub const OPEN_SERVICE: &'static str = "Open Service";
    pub const OPEN_SERVICE_CONTROL_MANAGER: &'static str = "Open Service Control Manager";
    pub const PROTECT_VIRTUAL_MEMORY: &'static str = "Protect Virtual Memory";
    pub const QUERY_DNS: &'static str = "Query DNS";
    pub const QUERY_DISK_ATTRIBUTES: &'static str = "Query Disk Attributes";
    pub const QUERY_PROCESS_VIRTUAL_MEMORY: &'static str = "Query Process Virtual Memory";
    pub const QUEUE_APC_IN_THREAD: &'static str = "Queue APC in Thread";
    pub const READ_FILE: &'static str = "Read File";
    pub const READ_FROM_NAMED_PIPE: &'static str = "Read From Named Pipe";
    pub const READ_FROM_PROCESS_MEMORY: &'static str = "Read From Process Memory";
    pub const READ_REGISTRY_KEY_VALUE: &'static str = "Read Registry Key Value";
    pub const RECEIVE_DATA_ON_SOCKET: &'static str = "Receive Data on Socket";
    pub const RECEIVE_EMAIL_MESSAGE: &'static str = "Receive Email Message";
    pub const RELEASE_MUTEX: &'static str = "Release Mutex";
    pub const RENAME_FILE: &'static str = "Rename File";
    pub const REVERT_THREAD_TO_SELF: &'static str = "Revert Thread to Self";
    pub const SEND_CONTROL_CODE_TO_FILE: &'static str = "Send Control Code to File";
    pub const SEND_CONTROL_CODE_TO_PIPE: &'static str = "Send Control Code to Pipe";
    pub const SEND_CONTROL_CODE_TO_SERVICE: &'static str = "Send Control Code to Service";
    pub const SEND_DNS_QUERY: &'static str = "Send DNS Query";
    pub const SEND_DATA_ON_SOCKET: &'static str = "Send Data on Socket";
    pub const SEND_DATA_TO_ADDRESS_ON_SOCKET: &'static str = "Send Data to Address on Socket";
    pub const SEND_EMAIL_MESSAGE: &'static str = "Send Email Message";
    pub const SEND_ICMP_REQUEST: &'static str = "Send ICMP Request";
    pub const SEND_REVERSE_DNS_QUERY: &'static str = "Send Reverse DNS Query";
    pub const SET_FILE_ATTRIBUTES: &'static str = "Set File Attributes";
    pub const SET_NETBIOS_NAME: &'static str = "Set NetBIOS Name";
    pub const SET_PROCESS_CURRENT_DIRECTORY: &'static str = "Set Process Current Directory";
    pub const SET_PROCESS_ENVIRONMENT_VARIABLE: &'static str = "Set Process Environment Variable";
    pub const SET_SYSTEM_GLOBAL_FLAGS: &'static str = "Set System Global Flags";
    pub const SET_SYSTEM_HOST_NAME: &'static str = "Set System Host Name";
    pub const SET_SYSTEM_TIME: &'static str = "Set System Time";
    pub const SET_THREAD_CONTEXT: &'static str = "Set Thread Context";
    pub const SHOW_WINDOW: &'static str = "Show Window";
    pub const SHUTDOWN_SYSTEM: &'static str = "Shutdown System";
    pub const SLEEP_PROCESS: &'static str = "Sleep Process";
    pub const SLEEP_SYSTEM: &'static str = "Sleep System";
    pub const START_SERVICE: &'static str = "Start Service";
    pub const UNLOAD_DRIVER: &'static str = "Unload Driver";
    pub const UNLOAD_MODULE: &'static str = "Unload Module";
    pub const UNLOCK_FILE: &'static str = "Unlock File";
    pub const UNMAP_FILE: &'static str = "Unmap File";
    pub const UPLOAD_FILE: &'static str = "Upload File";
    pub const WRITE_TO_FILE: &'static str = "Write to File";
    pub const WRITE_TO_PROCESS_VIRTUAL_MEMORY: &'static str = "Write to Process Virtual Memory";
}

/// Vocabulary: ActionRelationshipTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct ActionRelationshipTypeVocab;

impl ActionRelationshipTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionRelationshipTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Dependent_On", "Equivalent_To", "Followed_By", "Initiated", "Initiated_By", "Preceded_By", "Related_To"];
    pub const DEPENDENT_ON: &'static str = "Dependent_On";
    pub const EQUIVALENT_TO: &'static str = "Equivalent_To";
    pub const FOLLOWED_BY: &'static str = "Followed_By";
    pub const INITIATED: &'static str = "Initiated";
    pub const INITIATED_BY: &'static str = "Initiated_By";
    pub const PRECEDED_BY: &'static str = "Preceded_By";
    pub const RELATED_TO: &'static str = "Related_To";
}

/// Vocabulary: ActionStatusTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct ActionStatusTypeVocab;

impl ActionStatusTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionStatusTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Complete/Finish", "Error", "Fail", "Ongoing", "Pending", "Success", "Unknown"];
    pub const COMPLETE_FINISH: &'static str = "Complete/Finish";
    pub const ERROR: &'static str = "Error";
    pub const FAIL: &'static str = "Fail";
    pub const ONGOING: &'static str = "Ongoing";
    pub const PENDING: &'static str = "Pending";
    pub const SUCCESS: &'static str = "Success";
    pub const UNKNOWN: &'static str = "Unknown";
}

/// Vocabulary: ActionTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct ActionTypeVocab;

impl ActionTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Accept", "Access", "Add", "Alert", "Allocate", "Archive", "Assign", "Audit", "Backup", "Bind", "Block", "Call", "Change", "Check", "Clean", "Click", "Close", "Compare", "Compress", "Configure", "Connect", "Control", "Copy/Duplicate", "Create", "Decode", "Decompress", "Decrypt", "Deny", "Depress", "Detect", "Disconnect", "Download", "Draw", "Drop", "Encode", "Encrypt", "Enumerate", "Execute", "Extract", "Filter", "Find", "Flush", "Fork", "Free", "Get", "Hide", "Hook", "Impersonate", "Initialize", "Inject", "Install", "Interleave", "Join", "Kill", "Listen", "Load", "Lock", "Login/Logon", "Logout/Logoff", "Map", "Merge", "Modify", "Monitor", "Move", "Open", "Pack", "Pause", "Press", "Protect", "Quarantine", "Query", "Queue", "Raise", "Read", "Receive", "Release", "Remove/Delete", "Rename", "Replicate", "Restore", "Resume", "Revert", "Run", "Save", "Scan", "Schedule", "Search", "Send", "Set", "Shutdown", "Sleep", "Snapshot", "Start", "Stop", "Suspend", "Synchronize", "Throw", "Transmit", "Unblock", "Unhide", "Unhook", "Uninstall", "Unload", "Unlock", "Unmap", "Unpack", "Update", "Upgrade", "Upload", "Wipe/Destroy/Purge", "Write"];
    pub const ACCEPT: &'static str = "Accept";
    pub const ACCESS: &'static str = "Access";
    pub const ADD: &'static str = "Add";
    pub const ALERT: &'static str = "Alert";
    pub const ALLOCATE: &'static str = "Allocate";
    pub const ARCHIVE: &'static str = "Archive";
    pub const ASSIGN: &'static str = "Assign";
    pub const AUDIT: &'static str = "Audit";
    pub const BACKUP: &'static str = "Backup";
    pub const BIND: &'static str = "Bind";
    pub const BLOCK: &'static str = "Block";
    pub const CALL: &'static str = "Call";
    pub const CHANGE: &'static str = "Change";
    pub const CHECK: &'static str = "Check";
    pub const CLEAN: &'static str = "Clean";
    pub const CLICK: &'static str = "Click";
    pub const CLOSE: &'static str = "Close";
    pub const COMPARE: &'static str = "Compare";
    pub const COMPRESS: &'static str = "Compress";
    pub const CONFIGURE: &'static str = "Configure";
    pub const CONNECT: &'static str = "Connect";
    pub const CONTROL: &'static str = "Control";
    pub const COPY_DUPLICATE: &'static str = "Copy/Duplicate";
    pub const CREATE: &'static str = "Create";
    pub const DECODE: &'static str = "Decode";
    pub const DECOMPRESS: &'static str = "Decompress";
    pub const DECRYPT: &'static str = "Decrypt";
    pub const DENY: &'static str = "Deny";
    pub const DEPRESS: &'static str = "Depress";
    pub const DETECT: &'static str = "Detect";
    pub const DISCONNECT: &'static str = "Disconnect";
    pub const DOWNLOAD: &'static str = "Download";
    pub const DRAW: &'static str = "Draw";
    pub const DROP: &'static str = "Drop";
    pub const ENCODE: &'static str = "Encode";
    pub const ENCRYPT: &'static str = "Encrypt";
    pub const ENUMERATE: &'static str = "Enumerate";
    pub const EXECUTE: &'static str = "Execute";
    pub const EXTRACT: &'static str = "Extract";
    pub const FILTER: &'static str = "Filter";
    pub const FIND: &'static str = "Find";
    pub const FLUSH: &'static str = "Flush";
    pub const FORK: &'static str = "Fork";
    pub const FREE: &'static str = "Free";
    pub const GET: &'static str = "Get";
    pub const HIDE: &'static str = "Hide";
    pub const HOOK: &'static str = "Hook";
    pub const IMPERSONATE: &'static str = "Impersonate";
    pub const INITIALIZE: &'static str = "Initialize";
    pub const INJECT: &'static str = "Inject";
    pub const INSTALL: &'static str = "Install";
    pub const INTERLEAVE: &'static str = "Interleave";
    pub const JOIN: &'static str = "Join";
    pub const KILL: &'static str = "Kill";
    pub const LISTEN: &'static str = "Listen";
    pub const LOAD: &'static str = "Load";
    pub const LOCK: &'static str = "Lock";
    pub const LOGIN_LOGON: &'static str = "Login/Logon";
    pub const LOGOUT_LOGOFF: &'static str = "Logout/Logoff";
    pub const MAP: &'static str = "Map";
    pub const MERGE: &'static str = "Merge";
    pub const MODIFY: &'static str = "Modify";
    pub const MONITOR: &'static str = "Monitor";
    pub const MOVE: &'static str = "Move";
    pub const OPEN: &'static str = "Open";
    pub const PACK: &'static str = "Pack";
    pub const PAUSE: &'static str = "Pause";
    pub const PRESS: &'static str = "Press";
    pub const PROTECT: &'static str = "Protect";
    pub const QUARANTINE: &'static str = "Quarantine";
    pub const QUERY: &'static str = "Query";
    pub const QUEUE: &'static str = "Queue";
    pub const RAISE: &'static str = "Raise";
    pub const READ: &'static str = "Read";
    pub const RECEIVE: &'static str = "Receive";
    pub const RELEASE: &'static str = "Release";
    pub const REMOVE_DELETE: &'static str = "Remove/Delete";
    pub const RENAME: &'static str = "Rename";
    pub const REPLICATE: &'static str = "Replicate";
    pub const RESTORE: &'static str = "Restore";
    pub const RESUME: &'static str = "Resume";
    pub const REVERT: &'static str = "Revert";
    pub const RUN: &'static str = "Run";
    pub const SAVE: &'static str = "Save";
    pub const SCAN: &'static str = "Scan";
    pub const SCHEDULE: &'static str = "Schedule";
    pub const SEARCH: &'static str = "Search";
    pub const SEND: &'static str = "Send";
    pub const SET: &'static str = "Set";
    pub const SHUTDOWN: &'static str = "Shutdown";
    pub const SLEEP: &'static str = "Sleep";
    pub const SNAPSHOT: &'static str = "Snapshot";
    pub const START: &'static str = "Start";
    pub const STOP: &'static str = "Stop";
    pub const SUSPEND: &'static str = "Suspend";
    pub const SYNCHRONIZE: &'static str = "Synchronize";
    pub const THROW: &'static str = "Throw";
    pub const TRANSMIT: &'static str = "Transmit";
    pub const UNBLOCK: &'static str = "Unblock";
    pub const UNHIDE: &'static str = "Unhide";
    pub const UNHOOK: &'static str = "Unhook";
    pub const UNINSTALL: &'static str = "Uninstall";
    pub const UNLOAD: &'static str = "Unload";
    pub const UNLOCK: &'static str = "Unlock";
    pub const UNMAP: &'static str = "Unmap";
    pub const UNPACK: &'static str = "Unpack";
    pub const UPDATE: &'static str = "Update";
    pub const UPGRADE: &'static str = "Upgrade";
    pub const UPLOAD: &'static str = "Upload";
    pub const WIPE_DESTROY_PURGE: &'static str = "Wipe/Destroy/Purge";
    pub const WRITE: &'static str = "Write";
}

/// Vocabulary: BitnessVocab
#[derive(Debug, Clone, Copy)]
pub struct BitnessVocab;

impl BitnessVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/BitnessVocab";
    pub const MEMBERS: &'static [&'static str] = &["32", "64"];
    pub const _32: &'static str = "32";
    pub const _64: &'static str = "64";
}

/// Vocabulary: CharacterEncodingVocab
#[derive(Debug, Clone, Copy)]
pub struct CharacterEncodingVocab;

impl CharacterEncodingVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/CharacterEncodingVocab";
    pub const MEMBERS: &'static [&'static str] = &["ASCII", "UTF-16", "UTF-32", "UTF-8", "Windows-1250", "Windows-1251", "Windows-1252", "Windows-1253", "Windows-1254", "Windows-1255", "Windows-1256", "Windows-1257", "Windows-1258"];
    pub const ASCII: &'static str = "ASCII";
    pub const UTF_16: &'static str = "UTF-16";
    pub const UTF_32: &'static str = "UTF-32";
    pub const UTF_8: &'static str = "UTF-8";
    pub const WINDOWS_1250: &'static str = "Windows-1250";
    pub const WINDOWS_1251: &'static str = "Windows-1251";
    pub const WINDOWS_1252: &'static str = "Windows-1252";
    pub const WINDOWS_1253: &'static str = "Windows-1253";
    pub const WINDOWS_1254: &'static str = "Windows-1254";
    pub const WINDOWS_1255: &'static str = "Windows-1255";
    pub const WINDOWS_1256: &'static str = "Windows-1256";
    pub const WINDOWS_1257: &'static str = "Windows-1257";
    pub const WINDOWS_1258: &'static str = "Windows-1258";
}

/// Vocabulary: ContactAddressScopeVocab
#[derive(Debug, Clone, Copy)]
pub struct ContactAddressScopeVocab;

impl ContactAddressScopeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactAddressScopeVocab";
    pub const MEMBERS: &'static [&'static str] = &["home", "school", "work"];
    pub const HOME: &'static str = "home";
    pub const SCHOOL: &'static str = "school";
    pub const WORK: &'static str = "work";
}

/// Vocabulary: ContactEmailScopeVocab
#[derive(Debug, Clone, Copy)]
pub struct ContactEmailScopeVocab;

impl ContactEmailScopeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactEmailScopeVocab";
    pub const MEMBERS: &'static [&'static str] = &["cloud", "home", "school", "work"];
    pub const CLOUD: &'static str = "cloud";
    pub const HOME: &'static str = "home";
    pub const SCHOOL: &'static str = "school";
    pub const WORK: &'static str = "work";
}

/// Vocabulary: ContactPhoneScopeVocab
#[derive(Debug, Clone, Copy)]
pub struct ContactPhoneScopeVocab;

impl ContactPhoneScopeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactPhoneScopeVocab";
    pub const MEMBERS: &'static [&'static str] = &["home", "home fax", "main", "mobile", "pager", "school", "work", "work fax"];
    pub const HOME: &'static str = "home";
    pub const HOME_FAX: &'static str = "home fax";
    pub const MAIN: &'static str = "main";
    pub const MOBILE: &'static str = "mobile";
    pub const PAGER: &'static str = "pager";
    pub const SCHOOL: &'static str = "school";
    pub const WORK: &'static str = "work";
    pub const WORK_FAX: &'static str = "work fax";
}

/// Vocabulary: ContactSIPScopeVocab
#[derive(Debug, Clone, Copy)]
pub struct ContactSIPScopeVocab;

impl ContactSIPScopeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactSIPScopeVocab";
    pub const MEMBERS: &'static [&'static str] = &["home", "school", "work"];
    pub const HOME: &'static str = "home";
    pub const SCHOOL: &'static str = "school";
    pub const WORK: &'static str = "work";
}

/// Vocabulary: ContactURLScopeVocab
#[derive(Debug, Clone, Copy)]
pub struct ContactURLScopeVocab;

impl ContactURLScopeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactURLScopeVocab";
    pub const MEMBERS: &'static [&'static str] = &["home", "homepage", "school", "work"];
    pub const HOME: &'static str = "home";
    pub const HOMEPAGE: &'static str = "homepage";
    pub const SCHOOL: &'static str = "school";
    pub const WORK: &'static str = "work";
}

/// Vocabulary: DiskTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct DiskTypeVocab;

impl DiskTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/DiskTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["CDRom", "Fixed", "RAMDisk", "Remote", "Removable"];
    pub const CDROM: &'static str = "CDRom";
    pub const FIXED: &'static str = "Fixed";
    pub const RAMDISK: &'static str = "RAMDisk";
    pub const REMOTE: &'static str = "Remote";
    pub const REMOVABLE: &'static str = "Removable";
}

/// Vocabulary: EndiannessTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct EndiannessTypeVocab;

impl EndiannessTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/EndiannessTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Big-endian", "Little-endian", "Middle-endian"];
    pub const BIG_ENDIAN: &'static str = "Big-endian";
    pub const LITTLE_ENDIAN: &'static str = "Little-endian";
    pub const MIDDLE_ENDIAN: &'static str = "Middle-endian";
}

/// Vocabulary: HashNameVocab
#[derive(Debug, Clone, Copy)]
pub struct HashNameVocab;

impl HashNameVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/HashNameVocab";
    pub const MEMBERS: &'static [&'static str] = &["MD5", "MD6", "SHA1", "SHA224", "SHA256", "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512", "SHA384", "SHA512", "SSDEEP"];
    pub const MD5: &'static str = "MD5";
    pub const MD6: &'static str = "MD6";
    pub const SHA1: &'static str = "SHA1";
    pub const SHA224: &'static str = "SHA224";
    pub const SHA256: &'static str = "SHA256";
    pub const SHA3_224: &'static str = "SHA3-224";
    pub const SHA3_256: &'static str = "SHA3-256";
    pub const SHA3_384: &'static str = "SHA3-384";
    pub const SHA3_512: &'static str = "SHA3-512";
    pub const SHA384: &'static str = "SHA384";
    pub const SHA512: &'static str = "SHA512";
    pub const SSDEEP: &'static str = "SSDEEP";
}

/// Vocabulary: LibraryTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct LibraryTypeVocab;

impl LibraryTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/LibraryTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Dynamic", "Other", "Remote", "Shared", "Static"];
    pub const DYNAMIC: &'static str = "Dynamic";
    pub const OTHER: &'static str = "Other";
    pub const REMOTE: &'static str = "Remote";
    pub const SHARED: &'static str = "Shared";
    pub const STATIC: &'static str = "Static";
}

/// Vocabulary: MemoryBlockTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct MemoryBlockTypeVocab;

impl MemoryBlockTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/MemoryBlockTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Bit-mapped", "Byte-mapped", "Initialized", "Overlay", "Uninitialized"];
    pub const BIT_MAPPED: &'static str = "Bit-mapped";
    pub const BYTE_MAPPED: &'static str = "Byte-mapped";
    pub const INITIALIZED: &'static str = "Initialized";
    pub const OVERLAY: &'static str = "Overlay";
    pub const UNINITIALIZED: &'static str = "Uninitialized";
}

/// Vocabulary: NetworkSocketAddressFamily
#[derive(Debug, Clone, Copy)]
pub struct NetworkSocketAddressFamily;

impl NetworkSocketAddressFamily {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketAddressFamily";
    pub const MEMBERS: &'static [&'static str] = &["af_appletalk", "af_bth", "af_inet", "af_inet6", "af_ipx", "af_irda", "af_netbios", "af_unspec"];
    pub const AF_APPLETALK: &'static str = "af_appletalk";
    pub const AF_BTH: &'static str = "af_bth";
    pub const AF_INET: &'static str = "af_inet";
    pub const AF_INET6: &'static str = "af_inet6";
    pub const AF_IPX: &'static str = "af_ipx";
    pub const AF_IRDA: &'static str = "af_irda";
    pub const AF_NETBIOS: &'static str = "af_netbios";
    pub const AF_UNSPEC: &'static str = "af_unspec";
}

/// Vocabulary: NetworkSocketProtocolFamily
#[derive(Debug, Clone, Copy)]
pub struct NetworkSocketProtocolFamily;

impl NetworkSocketProtocolFamily {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketProtocolFamily";
    pub const MEMBERS: &'static [&'static str] = &["pf_appletalk", "pf_ash", "pf_atmpvc", "pf_atmsvc", "pf_ax25", "pf_bluetooth", "pf_bridge", "pf_decnet", "pf_econet", "pf_inet", "pf_inet6", "pf_ipx", "pf_irda", "pf_key", "pf_netbeui", "pf_netlink", "pf_netrom", "pf_packet", "pf_pppox", "pf_rose", "pf_route", "pf_security", "pf_sna", "pf_wanpipe", "pf_x25"];
    pub const PF_APPLETALK: &'static str = "pf_appletalk";
    pub const PF_ASH: &'static str = "pf_ash";
    pub const PF_ATMPVC: &'static str = "pf_atmpvc";
    pub const PF_ATMSVC: &'static str = "pf_atmsvc";
    pub const PF_AX25: &'static str = "pf_ax25";
    pub const PF_BLUETOOTH: &'static str = "pf_bluetooth";
    pub const PF_BRIDGE: &'static str = "pf_bridge";
    pub const PF_DECNET: &'static str = "pf_decnet";
    pub const PF_ECONET: &'static str = "pf_econet";
    pub const PF_INET: &'static str = "pf_inet";
    pub const PF_INET6: &'static str = "pf_inet6";
    pub const PF_IPX: &'static str = "pf_ipx";
    pub const PF_IRDA: &'static str = "pf_irda";
    pub const PF_KEY: &'static str = "pf_key";
    pub const PF_NETBEUI: &'static str = "pf_netbeui";
    pub const PF_NETLINK: &'static str = "pf_netlink";
    pub const PF_NETROM: &'static str = "pf_netrom";
    pub const PF_PACKET: &'static str = "pf_packet";
    pub const PF_PPPOX: &'static str = "pf_pppox";
    pub const PF_ROSE: &'static str = "pf_rose";
    pub const PF_ROUTE: &'static str = "pf_route";
    pub const PF_SECURITY: &'static str = "pf_security";
    pub const PF_SNA: &'static str = "pf_sna";
    pub const PF_WANPIPE: &'static str = "pf_wanpipe";
    pub const PF_X25: &'static str = "pf_x25";
}

/// Vocabulary: NetworkSocketType
#[derive(Debug, Clone, Copy)]
pub struct NetworkSocketType;

impl NetworkSocketType {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketType";
    pub const MEMBERS: &'static [&'static str] = &["sock_dgram", "sock_raw", "sock_rdm", "sock_seqpacket", "sock_stream"];
    pub const SOCK_DGRAM: &'static str = "sock_dgram";
    pub const SOCK_RAW: &'static str = "sock_raw";
    pub const SOCK_RDM: &'static str = "sock_rdm";
    pub const SOCK_SEQPACKET: &'static str = "sock_seqpacket";
    pub const SOCK_STREAM: &'static str = "sock_stream";
}

/// Vocabulary: ObjectStatusVocab
#[derive(Debug, Clone, Copy)]
pub struct ObjectStatusVocab;

impl ObjectStatusVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/core/ObjectStatusVocab";
    pub const MEMBERS: &'static [&'static str] = &["Deprecated", "Draft", "Final"];
    pub const DEPRECATED: &'static str = "Deprecated";
    pub const DRAFT: &'static str = "Draft";
    pub const FINAL: &'static str = "Final";
}

/// Vocabulary: ObservableObjectRelationshipVocab
#[derive(Debug, Clone, Copy)]
pub struct ObservableObjectRelationshipVocab;

impl ObservableObjectRelationshipVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectRelationshipVocab";
    pub const MEMBERS: &'static [&'static str] = &["Allocated", "Allocated_By", "Attachment_Of", "Bound", "Bound_By", "Characterized_By", "Characterizes", "Child_Of", "Closed", "Closed_By", "Compressed", "Compressed_By", "Compressed_From", "Compressed_Into", "Connected_From", "Connected_To", "Contained_Within", "Contains", "Copied", "Copied_By", "Copied_From", "Copied_To", "Created", "Created_By", "Decoded", "Decoded_By", "Decompressed", "Decompressed_By", "Decrypted", "Decrypted_By", "Deleted", "Deleted_By", "Deleted_From", "Downloaded", "Downloaded_By", "Downloaded_From", "Downloaded_To", "Dropped", "Dropped_By", "Encoded", "Encoded_By", "Encrypted", "Encrypted_By", "Encrypted_From", "Encrypted_To", "Extracted_From", "FQDN_Of", "Freed", "Freed_By", "Had_Attachment", "Hooked", "Hooked_By", "Initialized_By", "Initialized_To", "Injected", "Injected_As", "Injected_By", "Injected_Into", "Installed", "Installed_By", "Joined", "Joined_By", "Killed", "Killed_By", "Listened_On", "Listened_On_By", "Loaded_From", "Loaded_Into", "Locked", "Locked_By", "Mapped_By", "Mapped_Into", "Merged", "Merged_By", "Modified_Properties_Of", "Monitored", "Monitored_By", "Moved", "Moved_By", "Moved_From", "Moved_To", "Opened", "Opened_By", "Packed", "Packed_By", "Packed_From", "Packed_Into", "Parent_Of", "Paused", "Paused_By", "Previously_Contained", "Properties_Modified_By", "Properties_Queried", "Properties_Queried_By", "Read_From", "Read_From_By", "Received", "Received_By", "Received_From", "Received_Via_Upload", "Redirects_To", "Related_To", "Renamed", "Renamed_By", "Renamed_From", "Renamed_To", "Resolved_To", "Resumed", "Resumed_By", "Root_Domain_Of", "Searched_For", "Searched_For_By", "Sent", "Sent_By", "Sent_To", "Sent_Via_Upload", "Set_From", "Set_To", "Signed_By", "Sub-domain_Of", "Supra-domain_Of", "Suspended", "Suspended_By", "Unhooked", "Unhooked_By", "Unlocked", "Unlocked_By", "Unpacked", "Unpacked_By", "Uploaded", "Uploaded_By", "Uploaded_From", "Uploaded_To", "Used", "Used_By", "Values_Enumerated", "Values_Enumerated_By", "Written_To_By", "Wrote_To"];
    pub const ALLOCATED: &'static str = "Allocated";
    pub const ALLOCATED_BY: &'static str = "Allocated_By";
    pub const ATTACHMENT_OF: &'static str = "Attachment_Of";
    pub const BOUND: &'static str = "Bound";
    pub const BOUND_BY: &'static str = "Bound_By";
    pub const CHARACTERIZED_BY: &'static str = "Characterized_By";
    pub const CHARACTERIZES: &'static str = "Characterizes";
    pub const CHILD_OF: &'static str = "Child_Of";
    pub const CLOSED: &'static str = "Closed";
    pub const CLOSED_BY: &'static str = "Closed_By";
    pub const COMPRESSED: &'static str = "Compressed";
    pub const COMPRESSED_BY: &'static str = "Compressed_By";
    pub const COMPRESSED_FROM: &'static str = "Compressed_From";
    pub const COMPRESSED_INTO: &'static str = "Compressed_Into";
    pub const CONNECTED_FROM: &'static str = "Connected_From";
    pub const CONNECTED_TO: &'static str = "Connected_To";
    pub const CONTAINED_WITHIN: &'static str = "Contained_Within";
    pub const CONTAINS: &'static str = "Contains";
    pub const COPIED: &'static str = "Copied";
    pub const COPIED_BY: &'static str = "Copied_By";
    pub const COPIED_FROM: &'static str = "Copied_From";
    pub const COPIED_TO: &'static str = "Copied_To";
    pub const CREATED: &'static str = "Created";
    pub const CREATED_BY: &'static str = "Created_By";
    pub const DECODED: &'static str = "Decoded";
    pub const DECODED_BY: &'static str = "Decoded_By";
    pub const DECOMPRESSED: &'static str = "Decompressed";
    pub const DECOMPRESSED_BY: &'static str = "Decompressed_By";
    pub const DECRYPTED: &'static str = "Decrypted";
    pub const DECRYPTED_BY: &'static str = "Decrypted_By";
    pub const DELETED: &'static str = "Deleted";
    pub const DELETED_BY: &'static str = "Deleted_By";
    pub const DELETED_FROM: &'static str = "Deleted_From";
    pub const DOWNLOADED: &'static str = "Downloaded";
    pub const DOWNLOADED_BY: &'static str = "Downloaded_By";
    pub const DOWNLOADED_FROM: &'static str = "Downloaded_From";
    pub const DOWNLOADED_TO: &'static str = "Downloaded_To";
    pub const DROPPED: &'static str = "Dropped";
    pub const DROPPED_BY: &'static str = "Dropped_By";
    pub const ENCODED: &'static str = "Encoded";
    pub const ENCODED_BY: &'static str = "Encoded_By";
    pub const ENCRYPTED: &'static str = "Encrypted";
    pub const ENCRYPTED_BY: &'static str = "Encrypted_By";
    pub const ENCRYPTED_FROM: &'static str = "Encrypted_From";
    pub const ENCRYPTED_TO: &'static str = "Encrypted_To";
    pub const EXTRACTED_FROM: &'static str = "Extracted_From";
    pub const FQDN_OF: &'static str = "FQDN_Of";
    pub const FREED: &'static str = "Freed";
    pub const FREED_BY: &'static str = "Freed_By";
    pub const HAD_ATTACHMENT: &'static str = "Had_Attachment";
    pub const HOOKED: &'static str = "Hooked";
    pub const HOOKED_BY: &'static str = "Hooked_By";
    pub const INITIALIZED_BY: &'static str = "Initialized_By";
    pub const INITIALIZED_TO: &'static str = "Initialized_To";
    pub const INJECTED: &'static str = "Injected";
    pub const INJECTED_AS: &'static str = "Injected_As";
    pub const INJECTED_BY: &'static str = "Injected_By";
    pub const INJECTED_INTO: &'static str = "Injected_Into";
    pub const INSTALLED: &'static str = "Installed";
    pub const INSTALLED_BY: &'static str = "Installed_By";
    pub const JOINED: &'static str = "Joined";
    pub const JOINED_BY: &'static str = "Joined_By";
    pub const KILLED: &'static str = "Killed";
    pub const KILLED_BY: &'static str = "Killed_By";
    pub const LISTENED_ON: &'static str = "Listened_On";
    pub const LISTENED_ON_BY: &'static str = "Listened_On_By";
    pub const LOADED_FROM: &'static str = "Loaded_From";
    pub const LOADED_INTO: &'static str = "Loaded_Into";
    pub const LOCKED: &'static str = "Locked";
    pub const LOCKED_BY: &'static str = "Locked_By";
    pub const MAPPED_BY: &'static str = "Mapped_By";
    pub const MAPPED_INTO: &'static str = "Mapped_Into";
    pub const MERGED: &'static str = "Merged";
    pub const MERGED_BY: &'static str = "Merged_By";
    pub const MODIFIED_PROPERTIES_OF: &'static str = "Modified_Properties_Of";
    pub const MONITORED: &'static str = "Monitored";
    pub const MONITORED_BY: &'static str = "Monitored_By";
    pub const MOVED: &'static str = "Moved";
    pub const MOVED_BY: &'static str = "Moved_By";
    pub const MOVED_FROM: &'static str = "Moved_From";
    pub const MOVED_TO: &'static str = "Moved_To";
    pub const OPENED: &'static str = "Opened";
    pub const OPENED_BY: &'static str = "Opened_By";
    pub const PACKED: &'static str = "Packed";
    pub const PACKED_BY: &'static str = "Packed_By";
    pub const PACKED_FROM: &'static str = "Packed_From";
    pub const PACKED_INTO: &'static str = "Packed_Into";
    pub const PARENT_OF: &'static str = "Parent_Of";
    pub const PAUSED: &'static str = "Paused";
    pub const PAUSED_BY: &'static str = "Paused_By";
    pub const PREVIOUSLY_CONTAINED: &'static str = "Previously_Contained";
    pub const PROPERTIES_MODIFIED_BY: &'static str = "Properties_Modified_By";
    pub const PROPERTIES_QUERIED: &'static str = "Properties_Queried";
    pub const PROPERTIES_QUERIED_BY: &'static str = "Properties_Queried_By";
    pub const READ_FROM: &'static str = "Read_From";
    pub const READ_FROM_BY: &'static str = "Read_From_By";
    pub const RECEIVED: &'static str = "Received";
    pub const RECEIVED_BY: &'static str = "Received_By";
    pub const RECEIVED_FROM: &'static str = "Received_From";
    pub const RECEIVED_VIA_UPLOAD: &'static str = "Received_Via_Upload";
    pub const REDIRECTS_TO: &'static str = "Redirects_To";
    pub const RELATED_TO: &'static str = "Related_To";
    pub const RENAMED: &'static str = "Renamed";
    pub const RENAMED_BY: &'static str = "Renamed_By";
    pub const RENAMED_FROM: &'static str = "Renamed_From";
    pub const RENAMED_TO: &'static str = "Renamed_To";
    pub const RESOLVED_TO: &'static str = "Resolved_To";
    pub const RESUMED: &'static str = "Resumed";
    pub const RESUMED_BY: &'static str = "Resumed_By";
    pub const ROOT_DOMAIN_OF: &'static str = "Root_Domain_Of";
    pub const SEARCHED_FOR: &'static str = "Searched_For";
    pub const SEARCHED_FOR_BY: &'static str = "Searched_For_By";
    pub const SENT: &'static str = "Sent";
    pub const SENT_BY: &'static str = "Sent_By";
    pub const SENT_TO: &'static str = "Sent_To";
    pub const SENT_VIA_UPLOAD: &'static str = "Sent_Via_Upload";
    pub const SET_FROM: &'static str = "Set_From";
    pub const SET_TO: &'static str = "Set_To";
    pub const SIGNED_BY: &'static str = "Signed_By";
    pub const SUB_DOMAIN_OF: &'static str = "Sub-domain_Of";
    pub const SUPRA_DOMAIN_OF: &'static str = "Supra-domain_Of";
    pub const SUSPENDED: &'static str = "Suspended";
    pub const SUSPENDED_BY: &'static str = "Suspended_By";
    pub const UNHOOKED: &'static str = "Unhooked";
    pub const UNHOOKED_BY: &'static str = "Unhooked_By";
    pub const UNLOCKED: &'static str = "Unlocked";
    pub const UNLOCKED_BY: &'static str = "Unlocked_By";
    pub const UNPACKED: &'static str = "Unpacked";
    pub const UNPACKED_BY: &'static str = "Unpacked_By";
    pub const UPLOADED: &'static str = "Uploaded";
    pub const UPLOADED_BY: &'static str = "Uploaded_By";
    pub const UPLOADED_FROM: &'static str = "Uploaded_From";
    pub const UPLOADED_TO: &'static str = "Uploaded_To";
    pub const USED: &'static str = "Used";
    pub const USED_BY: &'static str = "Used_By";
    pub const VALUES_ENUMERATED: &'static str = "Values_Enumerated";
    pub const VALUES_ENUMERATED_BY: &'static str = "Values_Enumerated_By";
    pub const WRITTEN_TO_BY: &'static str = "Written_To_By";
    pub const WROTE_TO: &'static str = "Wrote_To";
}

/// Vocabulary: ObservableObjectStateVocab
#[derive(Debug, Clone, Copy)]
pub struct ObservableObjectStateVocab;

impl ObservableObjectStateVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectStateVocab";
    pub const MEMBERS: &'static [&'static str] = &["Active", "Closed", "Does Not Exist", "Exists", "Inactive", "Locked", "Open", "Started", "Stopped", "Unlocked"];
    pub const ACTIVE: &'static str = "Active";
    pub const CLOSED: &'static str = "Closed";
    pub const DOES_NOT_EXIST: &'static str = "Does Not Exist";
    pub const EXISTS: &'static str = "Exists";
    pub const INACTIVE: &'static str = "Inactive";
    pub const LOCKED: &'static str = "Locked";
    pub const OPEN: &'static str = "Open";
    pub const STARTED: &'static str = "Started";
    pub const STOPPED: &'static str = "Stopped";
    pub const UNLOCKED: &'static str = "Unlocked";
}

/// Vocabulary: PartitionTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct PartitionTypeVocab;

impl PartitionTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/PartitionTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["PARTITION_ENTRY_UNUSED", "PARTITION_EXTENDED", "PARTITION_FAT32", "PARTITION_FAT32_XINT13", "PARTITION_FAT_12", "PARTITION_FAT_16", "PARTITION_HUGE", "PARTITION_IFS", "PARTITION_LDM", "PARTITION_NTFT", "PARTITION_OS2BOOTMGR", "PARTITION_PREP", "PARTITION_UNIX", "PARTITION_XENIX_1", "PARTITION_XENIX_2", "PARTITION_XINT13", "PARTITION_XINT13_EXTENDED", "UNKNOWN", "VALID_NTFT"];
    pub const PARTITION_ENTRY_UNUSED: &'static str = "PARTITION_ENTRY_UNUSED";
    pub const PARTITION_EXTENDED: &'static str = "PARTITION_EXTENDED";
    pub const PARTITION_FAT32: &'static str = "PARTITION_FAT32";
    pub const PARTITION_FAT32_XINT13: &'static str = "PARTITION_FAT32_XINT13";
    pub const PARTITION_FAT_12: &'static str = "PARTITION_FAT_12";
    pub const PARTITION_FAT_16: &'static str = "PARTITION_FAT_16";
    pub const PARTITION_HUGE: &'static str = "PARTITION_HUGE";
    pub const PARTITION_IFS: &'static str = "PARTITION_IFS";
    pub const PARTITION_LDM: &'static str = "PARTITION_LDM";
    pub const PARTITION_NTFT: &'static str = "PARTITION_NTFT";
    pub const PARTITION_OS2BOOTMGR: &'static str = "PARTITION_OS2BOOTMGR";
    pub const PARTITION_PREP: &'static str = "PARTITION_PREP";
    pub const PARTITION_UNIX: &'static str = "PARTITION_UNIX";
    pub const PARTITION_XENIX_1: &'static str = "PARTITION_XENIX_1";
    pub const PARTITION_XENIX_2: &'static str = "PARTITION_XENIX_2";
    pub const PARTITION_XINT13: &'static str = "PARTITION_XINT13";
    pub const PARTITION_XINT13_EXTENDED: &'static str = "PARTITION_XINT13_EXTENDED";
    pub const UNKNOWN: &'static str = "UNKNOWN";
    pub const VALID_NTFT: &'static str = "VALID_NTFT";
}

/// Vocabulary: ProcessorArchVocab
#[derive(Debug, Clone, Copy)]
pub struct ProcessorArchVocab;

impl ProcessorArchVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ProcessorArchVocab";
    pub const MEMBERS: &'static [&'static str] = &["ARM", "Alpha", "IA-64", "MIPS", "Motorola 68k", "Other", "PowerPC", "SPARC", "eSi-RISC", "x86-32", "x86-64", "z/Architecture"];
    pub const ARM: &'static str = "ARM";
    pub const ALPHA: &'static str = "Alpha";
    pub const IA_64: &'static str = "IA-64";
    pub const MIPS: &'static str = "MIPS";
    pub const MOTOROLA_68K: &'static str = "Motorola 68k";
    pub const OTHER: &'static str = "Other";
    pub const POWERPC: &'static str = "PowerPC";
    pub const SPARC: &'static str = "SPARC";
    pub const ESI_RISC: &'static str = "eSi-RISC";
    pub const X86_32: &'static str = "x86-32";
    pub const X86_64: &'static str = "x86-64";
    pub const Z_ARCHITECTURE: &'static str = "z/Architecture";
}

/// Vocabulary: RecoveredObjectStatusVocab
#[derive(Debug, Clone, Copy)]
pub struct RecoveredObjectStatusVocab;

impl RecoveredObjectStatusVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RecoveredObjectStatusVocab";
    pub const MEMBERS: &'static [&'static str] = &["overwritten", "partially recovered", "recovered", "unknown"];
    pub const OVERWRITTEN: &'static str = "overwritten";
    pub const PARTIALLY_RECOVERED: &'static str = "partially recovered";
    pub const RECOVERED: &'static str = "recovered";
    pub const UNKNOWN: &'static str = "unknown";
}

/// Vocabulary: RegionalRegistryTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct RegionalRegistryTypeVocab;

impl RegionalRegistryTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RegionalRegistryTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["APNIC", "ARIN", "AfriNIC", "LACNIC", "RIPE NCC"];
    pub const APNIC: &'static str = "APNIC";
    pub const ARIN: &'static str = "ARIN";
    pub const AFRINIC: &'static str = "AfriNIC";
    pub const LACNIC: &'static str = "LACNIC";
    pub const RIPE_NCC: &'static str = "RIPE NCC";
}

/// Vocabulary: RegistryDatatype
#[derive(Debug, Clone, Copy)]
pub struct RegistryDatatype;

impl RegistryDatatype {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/RegistryDatatype";
    pub const MEMBERS: &'static [&'static str] = &["reg_binary", "reg_dword", "reg_dword_big_endian", "reg_expand_sz", "reg_full_resource_descriptor", "reg_invalid_type", "reg_link", "reg_multi_sz", "reg_none", "reg_qword", "reg_resource_list", "reg_resource_requirements_list", "reg_sz"];
    pub const REG_BINARY: &'static str = "reg_binary";
    pub const REG_DWORD: &'static str = "reg_dword";
    pub const REG_DWORD_BIG_ENDIAN: &'static str = "reg_dword_big_endian";
    pub const REG_EXPAND_SZ: &'static str = "reg_expand_sz";
    pub const REG_FULL_RESOURCE_DESCRIPTOR: &'static str = "reg_full_resource_descriptor";
    pub const REG_INVALID_TYPE: &'static str = "reg_invalid_type";
    pub const REG_LINK: &'static str = "reg_link";
    pub const REG_MULTI_SZ: &'static str = "reg_multi_sz";
    pub const REG_NONE: &'static str = "reg_none";
    pub const REG_QWORD: &'static str = "reg_qword";
    pub const REG_RESOURCE_LIST: &'static str = "reg_resource_list";
    pub const REG_RESOURCE_REQUIREMENTS_LIST: &'static str = "reg_resource_requirements_list";
    pub const REG_SZ: &'static str = "reg_sz";
}

/// Vocabulary: RegistryDatatypeVocab
#[derive(Debug, Clone, Copy)]
pub struct RegistryDatatypeVocab;

impl RegistryDatatypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RegistryDatatypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["reg_binary", "reg_dword", "reg_dword_big_endian", "reg_expand_sz", "reg_full_resource_descriptor", "reg_invalid_type", "reg_link", "reg_multi_sz", "reg_none", "reg_qword", "reg_resource_list", "reg_resource_requirements_list", "reg_sz"];
    pub const REG_BINARY: &'static str = "reg_binary";
    pub const REG_DWORD: &'static str = "reg_dword";
    pub const REG_DWORD_BIG_ENDIAN: &'static str = "reg_dword_big_endian";
    pub const REG_EXPAND_SZ: &'static str = "reg_expand_sz";
    pub const REG_FULL_RESOURCE_DESCRIPTOR: &'static str = "reg_full_resource_descriptor";
    pub const REG_INVALID_TYPE: &'static str = "reg_invalid_type";
    pub const REG_LINK: &'static str = "reg_link";
    pub const REG_MULTI_SZ: &'static str = "reg_multi_sz";
    pub const REG_NONE: &'static str = "reg_none";
    pub const REG_QWORD: &'static str = "reg_qword";
    pub const REG_RESOURCE_LIST: &'static str = "reg_resource_list";
    pub const REG_RESOURCE_REQUIREMENTS_LIST: &'static str = "reg_resource_requirements_list";
    pub const REG_SZ: &'static str = "reg_sz";
}

/// Vocabulary: SIMFormVocab
#[derive(Debug, Clone, Copy)]
pub struct SIMFormVocab;

impl SIMFormVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMFormVocab";
    pub const MEMBERS: &'static [&'static str] = &["Full-size SIM", "Micro SIM", "Nano SIM"];
    pub const FULL_SIZE_SIM: &'static str = "Full-size SIM";
    pub const MICRO_SIM: &'static str = "Micro SIM";
    pub const NANO_SIM: &'static str = "Nano SIM";
}

/// Vocabulary: SIMTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct SIMTypeVocab;

impl SIMTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["SIM", "UICC", "USIM"];
    pub const SIM: &'static str = "SIM";
    pub const UICC: &'static str = "UICC";
    pub const USIM: &'static str = "USIM";
}

/// Vocabulary: TaskActionTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct TaskActionTypeVocab;

impl TaskActionTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskActionTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["TASK_ACTION_COM_HANDLER", "TASK_ACTION_EXEC", "TASK_ACTION_SEND_EMAIL", "TASK_ACTION_SHOW_MESSAGE"];
    pub const TASK_ACTION_COM_HANDLER: &'static str = "TASK_ACTION_COM_HANDLER";
    pub const TASK_ACTION_EXEC: &'static str = "TASK_ACTION_EXEC";
    pub const TASK_ACTION_SEND_EMAIL: &'static str = "TASK_ACTION_SEND_EMAIL";
    pub const TASK_ACTION_SHOW_MESSAGE: &'static str = "TASK_ACTION_SHOW_MESSAGE";
}

/// Vocabulary: TaskFlagVocab
#[derive(Debug, Clone, Copy)]
pub struct TaskFlagVocab;

impl TaskFlagVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskFlagVocab";
    pub const MEMBERS: &'static [&'static str] = &["TASK_FLAG_DELETE_WHEN_DONE", "TASK_FLAG_DISABLED", "TASK_FLAG_DONT_START_IF_ON_BATTERIES", "TASK_FLAG_HIDDEN", "TASK_FLAG_INTERACTIVE", "TASK_FLAG_KILL_IF_GOING_ON_BATTERIES", "TASK_FLAG_KILL_ON_IDLE_END", "TASK_FLAG_RESTART_ON_IDLE_RESUME", "TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET", "TASK_FLAG_RUN_ONLY_IF_LOGGED_ON", "TASK_FLAG_START_ONLY_IF_IDLE", "TASK_FLAG_SYSTEM_REQUIRED", "TASK_FLAG_ZERO"];
    pub const TASK_FLAG_DELETE_WHEN_DONE: &'static str = "TASK_FLAG_DELETE_WHEN_DONE";
    pub const TASK_FLAG_DISABLED: &'static str = "TASK_FLAG_DISABLED";
    pub const TASK_FLAG_DONT_START_IF_ON_BATTERIES: &'static str = "TASK_FLAG_DONT_START_IF_ON_BATTERIES";
    pub const TASK_FLAG_HIDDEN: &'static str = "TASK_FLAG_HIDDEN";
    pub const TASK_FLAG_INTERACTIVE: &'static str = "TASK_FLAG_INTERACTIVE";
    pub const TASK_FLAG_KILL_IF_GOING_ON_BATTERIES: &'static str = "TASK_FLAG_KILL_IF_GOING_ON_BATTERIES";
    pub const TASK_FLAG_KILL_ON_IDLE_END: &'static str = "TASK_FLAG_KILL_ON_IDLE_END";
    pub const TASK_FLAG_RESTART_ON_IDLE_RESUME: &'static str = "TASK_FLAG_RESTART_ON_IDLE_RESUME";
    pub const TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET: &'static str = "TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET";
    pub const TASK_FLAG_RUN_ONLY_IF_LOGGED_ON: &'static str = "TASK_FLAG_RUN_ONLY_IF_LOGGED_ON";
    pub const TASK_FLAG_START_ONLY_IF_IDLE: &'static str = "TASK_FLAG_START_ONLY_IF_IDLE";
    pub const TASK_FLAG_SYSTEM_REQUIRED: &'static str = "TASK_FLAG_SYSTEM_REQUIRED";
    pub const TASK_FLAG_ZERO: &'static str = "TASK_FLAG_ZERO";
}

/// Vocabulary: TaskPriorityVocab
#[derive(Debug, Clone, Copy)]
pub struct TaskPriorityVocab;

impl TaskPriorityVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskPriorityVocab";
    pub const MEMBERS: &'static [&'static str] = &["ABOVE_NORMAL_PRIORITY_CLASS", "BELOW_NORMAL_PRIORITY_CLASS", "HIGH_PRIORITY_CLASS", "IDLE_PRIORITY_CLASS", "NORMAL_PRIORITY_CLASS", "REALTIME_PRIORITY_CLASS"];
    pub const ABOVE_NORMAL_PRIORITY_CLASS: &'static str = "ABOVE_NORMAL_PRIORITY_CLASS";
    pub const BELOW_NORMAL_PRIORITY_CLASS: &'static str = "BELOW_NORMAL_PRIORITY_CLASS";
    pub const HIGH_PRIORITY_CLASS: &'static str = "HIGH_PRIORITY_CLASS";
    pub const IDLE_PRIORITY_CLASS: &'static str = "IDLE_PRIORITY_CLASS";
    pub const NORMAL_PRIORITY_CLASS: &'static str = "NORMAL_PRIORITY_CLASS";
    pub const REALTIME_PRIORITY_CLASS: &'static str = "REALTIME_PRIORITY_CLASS";
}

/// Vocabulary: TaskStatusVocab
#[derive(Debug, Clone, Copy)]
pub struct TaskStatusVocab;

impl TaskStatusVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskStatusVocab";
    pub const MEMBERS: &'static [&'static str] = &["SCHED_E_ACCOUNT_DBASE_CORRUPT", "SCHED_E_ACCOUNT_INFORMATION_NOT_SET", "SCHED_E_ACCOUNT_NAME_NOT_FOUND", "SCHED_E_CANNOT_OPEN_TASK", "SCHED_E_INVALID_TASK", "SCHED_E_NO_SECURITY_SERVICES", "SCHED_E_SERVICE_NOT_INSTALLED", "SCHED_E_SERVICE_NOT_RUNNING", "SCHED_E_TASK_NOT_READY", "SCHED_E_TASK_NOT_RUNNING", "SCHED_E_TRIGGER_NOT_FOUND", "SCHED_E_UNKNOWN_OBJECT_VERSION", "SCHED_E_UNSUPPORTED_ACCOUNT_OPTION", "SCHED_S_EVENT_TRIGGER", "SCHED_S_TASK_DISABLED", "SCHED_S_TASK_HAS_NOT_RUN", "SCHED_S_TASK_NOT_SCHEDULED", "SCHED_S_TASK_NO_MORE_RUNS", "SCHED_S_TASK_NO_VALID_TRIGGERS", "SCHED_S_TASK_READY", "SCHED_S_TASK_RUNNING", "SCHED_S_TASK_TERMINATED", "TASK_STATE_QUEUED", "TASK_STATE_UNKNOWN"];
    pub const SCHED_E_ACCOUNT_DBASE_CORRUPT: &'static str = "SCHED_E_ACCOUNT_DBASE_CORRUPT";
    pub const SCHED_E_ACCOUNT_INFORMATION_NOT_SET: &'static str = "SCHED_E_ACCOUNT_INFORMATION_NOT_SET";
    pub const SCHED_E_ACCOUNT_NAME_NOT_FOUND: &'static str = "SCHED_E_ACCOUNT_NAME_NOT_FOUND";
    pub const SCHED_E_CANNOT_OPEN_TASK: &'static str = "SCHED_E_CANNOT_OPEN_TASK";
    pub const SCHED_E_INVALID_TASK: &'static str = "SCHED_E_INVALID_TASK";
    pub const SCHED_E_NO_SECURITY_SERVICES: &'static str = "SCHED_E_NO_SECURITY_SERVICES";
    pub const SCHED_E_SERVICE_NOT_INSTALLED: &'static str = "SCHED_E_SERVICE_NOT_INSTALLED";
    pub const SCHED_E_SERVICE_NOT_RUNNING: &'static str = "SCHED_E_SERVICE_NOT_RUNNING";
    pub const SCHED_E_TASK_NOT_READY: &'static str = "SCHED_E_TASK_NOT_READY";
    pub const SCHED_E_TASK_NOT_RUNNING: &'static str = "SCHED_E_TASK_NOT_RUNNING";
    pub const SCHED_E_TRIGGER_NOT_FOUND: &'static str = "SCHED_E_TRIGGER_NOT_FOUND";
    pub const SCHED_E_UNKNOWN_OBJECT_VERSION: &'static str = "SCHED_E_UNKNOWN_OBJECT_VERSION";
    pub const SCHED_E_UNSUPPORTED_ACCOUNT_OPTION: &'static str = "SCHED_E_UNSUPPORTED_ACCOUNT_OPTION";
    pub const SCHED_S_EVENT_TRIGGER: &'static str = "SCHED_S_EVENT_TRIGGER";
    pub const SCHED_S_TASK_DISABLED: &'static str = "SCHED_S_TASK_DISABLED";
    pub const SCHED_S_TASK_HAS_NOT_RUN: &'static str = "SCHED_S_TASK_HAS_NOT_RUN";
    pub const SCHED_S_TASK_NOT_SCHEDULED: &'static str = "SCHED_S_TASK_NOT_SCHEDULED";
    pub const SCHED_S_TASK_NO_MORE_RUNS: &'static str = "SCHED_S_TASK_NO_MORE_RUNS";
    pub const SCHED_S_TASK_NO_VALID_TRIGGERS: &'static str = "SCHED_S_TASK_NO_VALID_TRIGGERS";
    pub const SCHED_S_TASK_READY: &'static str = "SCHED_S_TASK_READY";
    pub const SCHED_S_TASK_RUNNING: &'static str = "SCHED_S_TASK_RUNNING";
    pub const SCHED_S_TASK_TERMINATED: &'static str = "SCHED_S_TASK_TERMINATED";
    pub const TASK_STATE_QUEUED: &'static str = "TASK_STATE_QUEUED";
    pub const TASK_STATE_UNKNOWN: &'static str = "TASK_STATE_UNKNOWN";
}

/// Vocabulary: ThreadRunningStatusVocab
#[derive(Debug, Clone, Copy)]
pub struct ThreadRunningStatusVocab;

impl ThreadRunningStatusVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ThreadRunningStatusVocab";
    pub const MEMBERS: &'static [&'static str] = &["Initialized", "Ready", "Running", "Standby", "Terminated", "Transition", "Unknown", "Waiting"];
    pub const INITIALIZED: &'static str = "Initialized";
    pub const READY: &'static str = "Ready";
    pub const RUNNING: &'static str = "Running";
    pub const STANDBY: &'static str = "Standby";
    pub const TERMINATED: &'static str = "Terminated";
    pub const TRANSITION: &'static str = "Transition";
    pub const UNKNOWN: &'static str = "Unknown";
    pub const WAITING: &'static str = "Waiting";
}

/// Vocabulary: TimestampPrecisionVocab
#[derive(Debug, Clone, Copy)]
pub struct TimestampPrecisionVocab;

impl TimestampPrecisionVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TimestampPrecisionVocab";
    pub const MEMBERS: &'static [&'static str] = &["day", "hour", "minute", "month", "second", "year"];
    pub const DAY: &'static str = "day";
    pub const HOUR: &'static str = "hour";
    pub const MINUTE: &'static str = "minute";
    pub const MONTH: &'static str = "month";
    pub const SECOND: &'static str = "second";
    pub const YEAR: &'static str = "year";
}

/// Vocabulary: TrendVocab
#[derive(Debug, Clone, Copy)]
pub struct TrendVocab;

impl TrendVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TrendVocab";
    pub const MEMBERS: &'static [&'static str] = &["Decreasing", "Increasing"];
    pub const DECREASING: &'static str = "Decreasing";
    pub const INCREASING: &'static str = "Increasing";
}

/// Vocabulary: TriggerFrequencyVocab
#[derive(Debug, Clone, Copy)]
pub struct TriggerFrequencyVocab;

impl TriggerFrequencyVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerFrequencyVocab";
    pub const MEMBERS: &'static [&'static str] = &["TASK_EVENT_TRIGGER_AT_LOGON", "TASK_EVENT_TRIGGER_AT_SYSTEMSTART", "TASK_EVENT_TRIGGER_ON_IDLE", "TASK_TIME_TRIGGER_DAILY", "TASK_TIME_TRIGGER_MONTHLYDATE", "TASK_TIME_TRIGGER_MONTHLYDOW", "TASK_TIME_TRIGGER_ONCE", "TASK_TIME_TRIGGER_WEEKLY"];
    pub const TASK_EVENT_TRIGGER_AT_LOGON: &'static str = "TASK_EVENT_TRIGGER_AT_LOGON";
    pub const TASK_EVENT_TRIGGER_AT_SYSTEMSTART: &'static str = "TASK_EVENT_TRIGGER_AT_SYSTEMSTART";
    pub const TASK_EVENT_TRIGGER_ON_IDLE: &'static str = "TASK_EVENT_TRIGGER_ON_IDLE";
    pub const TASK_TIME_TRIGGER_DAILY: &'static str = "TASK_TIME_TRIGGER_DAILY";
    pub const TASK_TIME_TRIGGER_MONTHLYDATE: &'static str = "TASK_TIME_TRIGGER_MONTHLYDATE";
    pub const TASK_TIME_TRIGGER_MONTHLYDOW: &'static str = "TASK_TIME_TRIGGER_MONTHLYDOW";
    pub const TASK_TIME_TRIGGER_ONCE: &'static str = "TASK_TIME_TRIGGER_ONCE";
    pub const TASK_TIME_TRIGGER_WEEKLY: &'static str = "TASK_TIME_TRIGGER_WEEKLY";
}

/// Vocabulary: TriggerTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct TriggerTypeVocab;

impl TriggerTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["TASK_TRIGGER_BOOT", "TASK_TRIGGER_EVENT", "TASK_TRIGGER_IDLE", "TASK_TRIGGER_LOGON", "TASK_TRIGGER_REGISTRATION", "TASK_TRIGGER_SESSION_STATE_CHANGE", "TASK_TRIGGER_TIME"];
    pub const TASK_TRIGGER_BOOT: &'static str = "TASK_TRIGGER_BOOT";
    pub const TASK_TRIGGER_EVENT: &'static str = "TASK_TRIGGER_EVENT";
    pub const TASK_TRIGGER_IDLE: &'static str = "TASK_TRIGGER_IDLE";
    pub const TASK_TRIGGER_LOGON: &'static str = "TASK_TRIGGER_LOGON";
    pub const TASK_TRIGGER_REGISTRATION: &'static str = "TASK_TRIGGER_REGISTRATION";
    pub const TASK_TRIGGER_SESSION_STATE_CHANGE: &'static str = "TASK_TRIGGER_SESSION_STATE_CHANGE";
    pub const TASK_TRIGGER_TIME: &'static str = "TASK_TRIGGER_TIME";
}

/// Vocabulary: URLTransitionTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct URLTransitionTypeVocab;

impl URLTransitionTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/URLTransitionTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["auto_bookmark", "auto_subframe", "auto_toplevel", "form_submit", "generated", "keyword", "keyword_generated", "link", "manual_subframe", "reload", "typed"];
    pub const AUTO_BOOKMARK: &'static str = "auto_bookmark";
    pub const AUTO_SUBFRAME: &'static str = "auto_subframe";
    pub const AUTO_TOPLEVEL: &'static str = "auto_toplevel";
    pub const FORM_SUBMIT: &'static str = "form_submit";
    pub const GENERATED: &'static str = "generated";
    pub const KEYWORD: &'static str = "keyword";
    pub const KEYWORD_GENERATED: &'static str = "keyword_generated";
    pub const LINK: &'static str = "link";
    pub const MANUAL_SUBFRAME: &'static str = "manual_subframe";
    pub const RELOAD: &'static str = "reload";
    pub const TYPED: &'static str = "typed";
}

/// Vocabulary: UnixProcessStateVocab
#[derive(Debug, Clone, Copy)]
pub struct UnixProcessStateVocab;

impl UnixProcessStateVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/UnixProcessStateVocab";
    pub const MEMBERS: &'static [&'static str] = &["Dead", "InterruptibleSleep", "Paging", "Running", "Stopped", "UninterruptibleSleep", "Zombie"];
    pub const DEAD: &'static str = "Dead";
    pub const INTERRUPTIBLESLEEP: &'static str = "InterruptibleSleep";
    pub const PAGING: &'static str = "Paging";
    pub const RUNNING: &'static str = "Running";
    pub const STOPPED: &'static str = "Stopped";
    pub const UNINTERRUPTIBLESLEEP: &'static str = "UninterruptibleSleep";
    pub const ZOMBIE: &'static str = "Zombie";
}

/// Vocabulary: WhoisContactTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct WhoisContactTypeVocab;

impl WhoisContactTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisContactTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["ADMIN", "BILLING", "TECHNICAL"];
    pub const ADMIN: &'static str = "ADMIN";
    pub const BILLING: &'static str = "BILLING";
    pub const TECHNICAL: &'static str = "TECHNICAL";
}

/// Vocabulary: WhoisDNSSECTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct WhoisDNSSECTypeVocab;

impl WhoisDNSSECTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Signed", "Unsigned"];
    pub const SIGNED: &'static str = "Signed";
    pub const UNSIGNED: &'static str = "Unsigned";
}

/// Vocabulary: WhoisStatusTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct WhoisStatusTypeVocab;

impl WhoisStatusTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisStatusTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["ADD_PERIOD", "AUTO_RENEW_PERIOD", "CLIENT_DELETE_PROHIBITED", "CLIENT_HOLD", "CLIENT_RENEW_PROHIBITED", "CLIENT_TRANSFER_PROHIBITED", "CLIENT_UPDATE_PROHIBITED", "DELETE_PROHIBITED", "HOLD", "INACTIVE", "OK", "PENDING_DELETE_RESTORABLE", "PENDING_DELETE_SCHEDULED_FOR_RELEASE", "PENDING_RESTORE", "RENEW_PERIOD", "RENEW_PROHIBITED", "TRANSFER_PERIOD", "TRANSFER_PROHIBITED", "UPDATE_PROHIBITED"];
    pub const ADD_PERIOD: &'static str = "ADD_PERIOD";
    pub const AUTO_RENEW_PERIOD: &'static str = "AUTO_RENEW_PERIOD";
    pub const CLIENT_DELETE_PROHIBITED: &'static str = "CLIENT_DELETE_PROHIBITED";
    pub const CLIENT_HOLD: &'static str = "CLIENT_HOLD";
    pub const CLIENT_RENEW_PROHIBITED: &'static str = "CLIENT_RENEW_PROHIBITED";
    pub const CLIENT_TRANSFER_PROHIBITED: &'static str = "CLIENT_TRANSFER_PROHIBITED";
    pub const CLIENT_UPDATE_PROHIBITED: &'static str = "CLIENT_UPDATE_PROHIBITED";
    pub const DELETE_PROHIBITED: &'static str = "DELETE_PROHIBITED";
    pub const HOLD: &'static str = "HOLD";
    pub const INACTIVE: &'static str = "INACTIVE";
    pub const OK: &'static str = "OK";
    pub const PENDING_DELETE_RESTORABLE: &'static str = "PENDING_DELETE_RESTORABLE";
    pub const PENDING_DELETE_SCHEDULED_FOR_RELEASE: &'static str = "PENDING_DELETE_SCHEDULED_FOR_RELEASE";
    pub const PENDING_RESTORE: &'static str = "PENDING_RESTORE";
    pub const RENEW_PERIOD: &'static str = "RENEW_PERIOD";
    pub const RENEW_PROHIBITED: &'static str = "RENEW_PROHIBITED";
    pub const TRANSFER_PERIOD: &'static str = "TRANSFER_PERIOD";
    pub const TRANSFER_PROHIBITED: &'static str = "TRANSFER_PROHIBITED";
    pub const UPDATE_PROHIBITED: &'static str = "UPDATE_PROHIBITED";
}

/// Vocabulary: WindowsDriveTypeVocab
#[derive(Debug, Clone, Copy)]
pub struct WindowsDriveTypeVocab;

impl WindowsDriveTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsDriveTypeVocab";
    pub const MEMBERS: &'static [&'static str] = &["DRIVE_CDROM", "DRIVE_FIXED", "DRIVE_NO_ROOT_DIR", "DRIVE_RAMDISK", "DRIVE_REMOTE", "DRIVE_REMOVABLE", "DRIVE_UNKNOWN"];
    pub const DRIVE_CDROM: &'static str = "DRIVE_CDROM";
    pub const DRIVE_FIXED: &'static str = "DRIVE_FIXED";
    pub const DRIVE_NO_ROOT_DIR: &'static str = "DRIVE_NO_ROOT_DIR";
    pub const DRIVE_RAMDISK: &'static str = "DRIVE_RAMDISK";
    pub const DRIVE_REMOTE: &'static str = "DRIVE_REMOTE";
    pub const DRIVE_REMOVABLE: &'static str = "DRIVE_REMOVABLE";
    pub const DRIVE_UNKNOWN: &'static str = "DRIVE_UNKNOWN";
}

/// Vocabulary: WindowsPEBinaryType
#[derive(Debug, Clone, Copy)]
pub struct WindowsPEBinaryType;

impl WindowsPEBinaryType {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryType";
    pub const MEMBERS: &'static [&'static str] = &["dll", "exe", "sys"];
    pub const DLL: &'static str = "dll";
    pub const EXE: &'static str = "exe";
    pub const SYS: &'static str = "sys";
}

/// Vocabulary: WindowsServiceStartType
#[derive(Debug, Clone, Copy)]
pub struct WindowsServiceStartType;

impl WindowsServiceStartType {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStartType";
    pub const MEMBERS: &'static [&'static str] = &["service_auto_start", "service_boot_start", "service_demand_start", "service_disabled", "service_system_alert"];
    pub const SERVICE_AUTO_START: &'static str = "service_auto_start";
    pub const SERVICE_BOOT_START: &'static str = "service_boot_start";
    pub const SERVICE_DEMAND_START: &'static str = "service_demand_start";
    pub const SERVICE_DISABLED: &'static str = "service_disabled";
    pub const SERVICE_SYSTEM_ALERT: &'static str = "service_system_alert";
}

/// Vocabulary: WindowsServiceStatus
#[derive(Debug, Clone, Copy)]
pub struct WindowsServiceStatus;

impl WindowsServiceStatus {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStatus";
    pub const MEMBERS: &'static [&'static str] = &["service_continue_pending", "service_pause_pending", "service_paused", "service_running", "service_start_pending", "service_stop_pending", "service_stopped"];
    pub const SERVICE_CONTINUE_PENDING: &'static str = "service_continue_pending";
    pub const SERVICE_PAUSE_PENDING: &'static str = "service_pause_pending";
    pub const SERVICE_PAUSED: &'static str = "service_paused";
    pub const SERVICE_RUNNING: &'static str = "service_running";
    pub const SERVICE_START_PENDING: &'static str = "service_start_pending";
    pub const SERVICE_STOP_PENDING: &'static str = "service_stop_pending";
    pub const SERVICE_STOPPED: &'static str = "service_stopped";
}

/// Vocabulary: WindowsServiceType
#[derive(Debug, Clone, Copy)]
pub struct WindowsServiceType;

impl WindowsServiceType {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceType";
    pub const MEMBERS: &'static [&'static str] = &["service_file_system_driver", "service_kernel_driver", "service_win32_own_process", "service_win32_share_process"];
    pub const SERVICE_FILE_SYSTEM_DRIVER: &'static str = "service_file_system_driver";
    pub const SERVICE_KERNEL_DRIVER: &'static str = "service_kernel_driver";
    pub const SERVICE_WIN32_OWN_PROCESS: &'static str = "service_win32_own_process";
    pub const SERVICE_WIN32_SHARE_PROCESS: &'static str = "service_win32_share_process";
}

/// Vocabulary: WindowsVolumeAttributeVocab
#[derive(Debug, Clone, Copy)]
pub struct WindowsVolumeAttributeVocab;

impl WindowsVolumeAttributeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab";
    pub const MEMBERS: &'static [&'static str] = &["Hidden", "NoDefaultDriveLetter", "ReadOnly", "ShadowCopy"];
    pub const HIDDEN: &'static str = "Hidden";
    pub const NODEFAULTDRIVELETTER: &'static str = "NoDefaultDriveLetter";
    pub const READONLY: &'static str = "ReadOnly";
    pub const SHADOWCOPY: &'static str = "ShadowCopy";
}

/// Vocabulary: WirelessNetworkSecurityModeVocab
#[derive(Debug, Clone, Copy)]
pub struct WirelessNetworkSecurityModeVocab;

impl WirelessNetworkSecurityModeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WirelessNetworkSecurityModeVocab";
    pub const MEMBERS: &'static [&'static str] = &["None", "WEP", "WPA", "WPA2-Enterprise", "WPA2-PSK", "WPA3-Enterprise", "WPA3-PSK"];
    pub const NONE: &'static str = "None";
    pub const WEP: &'static str = "WEP";
    pub const WPA: &'static str = "WPA";
    pub const WPA2_ENTERPRISE: &'static str = "WPA2-Enterprise";
    pub const WPA2_PSK: &'static str = "WPA2-PSK";
    pub const WPA3_ENTERPRISE: &'static str = "WPA3-Enterprise";
    pub const WPA3_PSK: &'static str = "WPA3-PSK";
}
