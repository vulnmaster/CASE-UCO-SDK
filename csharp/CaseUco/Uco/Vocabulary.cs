// Auto-generated CASE/UCO vocabularies — do not edit manually.
// Every UCO vocabulary (owl:oneOf datatype) in one namespace. Members are plain strings: UCO 1.4.0 and later expect vocabulary-valued properties as xsd:string literals checked against the vocabulary with sh:in, so pass the constants directly rather than typing them with the vocabulary IRI.

using System.Collections.Generic;

namespace CaseUco.Uco.Vocabulary
{
    /// <summary>Vocabulary: AccountTypeVocab</summary>
    public static class AccountTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/AccountTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "ldap", "nis", "openid", "radius", "tacacs", "unix", "windows_domain", "windows_local" };
        public const string ldap = "ldap";
        public const string nis = "nis";
        public const string openid = "openid";
        public const string radius = "radius";
        public const string tacacs = "tacacs";
        public const string unix = "unix";
        public const string windows_domain = "windows_domain";
        public const string windows_local = "windows_local";
    }

    /// <summary>Vocabulary: ActionArgumentNameVocab</summary>
    public static class ActionArgumentNameVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionArgumentNameVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "APC Address", "APC Mode", "API", "Access Mode", "Application Name", "Base Address", "Callback Address", "Code Address", "Command", "Control Code", "Control Parameter", "Creation Flags", "Database Name", "Delay Time (ms)", "Destination Address", "Error Control", "File Information Class", "Flags", "Function Address", "Function Name", "Function Ordinal", "Hook Type", "Host Name", "Hostname", "Initial Owner", "Mapping Offset", "Number of Bytes Per Send", "Options", "Parameter Address", "Password", "Privilege Name", "Protection", "Proxy Bypass", "Proxy Name", "Reason", "Request Size", "Requested Version", "Server", "Service Name", "Service State", "Service Type", "Share Mode", "Shutdown Flag", "Size (bytes)", "Sleep Time (ms)", "Source Address", "Starting Address", "System Metric Index", "Target PID", "Transfer Flags", "Username" };
        public const string APC_Address = "APC Address";
        public const string APC_Mode = "APC Mode";
        public const string API = "API";
        public const string Access_Mode = "Access Mode";
        public const string Application_Name = "Application Name";
        public const string Base_Address = "Base Address";
        public const string Callback_Address = "Callback Address";
        public const string Code_Address = "Code Address";
        public const string Command = "Command";
        public const string Control_Code = "Control Code";
        public const string Control_Parameter = "Control Parameter";
        public const string Creation_Flags = "Creation Flags";
        public const string Database_Name = "Database Name";
        public const string Delay_Time_ms = "Delay Time (ms)";
        public const string Destination_Address = "Destination Address";
        public const string Error_Control = "Error Control";
        public const string File_Information_Class = "File Information Class";
        public const string Flags = "Flags";
        public const string Function_Address = "Function Address";
        public const string Function_Name = "Function Name";
        public const string Function_Ordinal = "Function Ordinal";
        public const string Hook_Type = "Hook Type";
        public const string Host_Name = "Host Name";
        public const string Hostname = "Hostname";
        public const string Initial_Owner = "Initial Owner";
        public const string Mapping_Offset = "Mapping Offset";
        public const string Number_of_Bytes_Per_Send = "Number of Bytes Per Send";
        public const string Options = "Options";
        public const string Parameter_Address = "Parameter Address";
        public const string Password = "Password";
        public const string Privilege_Name = "Privilege Name";
        public const string Protection = "Protection";
        public const string Proxy_Bypass = "Proxy Bypass";
        public const string Proxy_Name = "Proxy Name";
        public const string Reason = "Reason";
        public const string Request_Size = "Request Size";
        public const string Requested_Version = "Requested Version";
        public const string Server = "Server";
        public const string Service_Name = "Service Name";
        public const string Service_State = "Service State";
        public const string Service_Type = "Service Type";
        public const string Share_Mode = "Share Mode";
        public const string Shutdown_Flag = "Shutdown Flag";
        public const string Size_bytes = "Size (bytes)";
        public const string Sleep_Time_ms = "Sleep Time (ms)";
        public const string Source_Address = "Source Address";
        public const string Starting_Address = "Starting Address";
        public const string System_Metric_Index = "System Metric Index";
        public const string Target_PID = "Target PID";
        public const string Transfer_Flags = "Transfer Flags";
        public const string Username = "Username";
    }

    /// <summary>Vocabulary: ActionNameVocab</summary>
    public static class ActionNameVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionNameVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Accept Socket Connection", "Add Connection to Network Share", "Add Network Share", "Add Scheduled Task", "Add System Call Hook", "Add User", "Add Windows Hook", "Allocate Virtual Memory in Process", "Bind Address to Socket", "Change Service Configuration", "Check for Remote Debugger", "Close Port", "Close Registry Key", "Close Socket", "Configure Service", "Connect to IP", "Connect to Named Pipe", "Connect to Network Share", "Connect to Socket", "Connect to URL", "Control Driver", "Control Service", "Copy File", "Create Dialog Box", "Create Directory", "Create Event", "Create File", "Create File Alternate Data Stream", "Create File Mapping", "Create File Symbolic Link", "Create Hidden File", "Create Mailslot", "Create Module", "Create Mutex", "Create Named Pipe", "Create Process", "Create Process as User", "Create Registry Key", "Create Registry Key Value", "Create Remote Thread in Process", "Create Service", "Create Socket", "Create Symbolic Link", "Create Thread", "Create Window", "Delete Directory", "Delete File", "Delete Named Pipe", "Delete Network Share", "Delete Registry Key", "Delete Registry Key Value", "Delete Service", "Delete User", "Disconnect from Named Pipe", "Disconnect from Network Share", "Disconnect from Socket", "Download File", "Enumerate DLLs", "Enumerate Network Shares", "Enumerate Processes", "Enumerate Protocols", "Enumerate Registry Key Subkeys", "Enumerate Registry Key Values", "Enumerate Services", "Enumerate System Handles", "Enumerate Threads", "Enumerate Threads in Process", "Enumerate Users", "Enumerate Windows", "Find File", "Find Window", "Flush Process Instruction Cache", "Free Library", "Free Process Virtual Memory", "Get Disk Free Space", "Get Disk Type", "Get Elapsed System Up Time", "Get File Attributes", "Get Function Address", "Get Host By Address", "Get Host By Name", "Get Host Name", "Get Library File Name", "Get Library Handle", "Get NetBIOS Name", "Get Process Current Directory", "Get Process Environment Variable", "Get Process Startup Information", "Get Processes Snapshot", "Get Registry Key Attributes", "Get Service Status", "Get System Global Flags", "Get System Host Name", "Get System Local Time", "Get System NetBIOS Name", "Get System Network Parameters", "Get System Time", "Get Thread Context", "Get Thread Username", "Get User Attributes", "Get Username", "Get Windows Directory", "Get Windows System Directory", "Get Windows Temporary Files Directory", "Hide Window", "Impersonate Process", "Impersonate Thread", "Inject Memory Page", "Kill Process", "Kill Thread", "Kill Window", "Listen on Port", "Listen on Socket", "Load Driver", "Load Library", "Load Module", "Load and Call Driver", "Lock File", "Logon as User", "Map File", "Map Library", "Map View of File", "Modify File", "Modify Named Pipe", "Modify Process", "Modify Registry Key", "Modify Registry Key Value", "Modify Service", "Monitor Registry Key", "Move File", "Open File", "Open File Mapping", "Open Mutex", "Open Port", "Open Process", "Open Registry Key", "Open Service", "Open Service Control Manager", "Protect Virtual Memory", "Query DNS", "Query Disk Attributes", "Query Process Virtual Memory", "Queue APC in Thread", "Read File", "Read From Named Pipe", "Read From Process Memory", "Read Registry Key Value", "Receive Data on Socket", "Receive Email Message", "Release Mutex", "Rename File", "Revert Thread to Self", "Send Control Code to File", "Send Control Code to Pipe", "Send Control Code to Service", "Send DNS Query", "Send Data on Socket", "Send Data to Address on Socket", "Send Email Message", "Send ICMP Request", "Send Reverse DNS Query", "Set File Attributes", "Set NetBIOS Name", "Set Process Current Directory", "Set Process Environment Variable", "Set System Global Flags", "Set System Host Name", "Set System Time", "Set Thread Context", "Show Window", "Shutdown System", "Sleep Process", "Sleep System", "Start Service", "Unload Driver", "Unload Module", "Unlock File", "Unmap File", "Upload File", "Write to File", "Write to Process Virtual Memory" };
        public const string Accept_Socket_Connection = "Accept Socket Connection";
        public const string Add_Connection_to_Network_Share = "Add Connection to Network Share";
        public const string Add_Network_Share = "Add Network Share";
        public const string Add_Scheduled_Task = "Add Scheduled Task";
        public const string Add_System_Call_Hook = "Add System Call Hook";
        public const string Add_User = "Add User";
        public const string Add_Windows_Hook = "Add Windows Hook";
        public const string Allocate_Virtual_Memory_in_Process = "Allocate Virtual Memory in Process";
        public const string Bind_Address_to_Socket = "Bind Address to Socket";
        public const string Change_Service_Configuration = "Change Service Configuration";
        public const string Check_for_Remote_Debugger = "Check for Remote Debugger";
        public const string Close_Port = "Close Port";
        public const string Close_Registry_Key = "Close Registry Key";
        public const string Close_Socket = "Close Socket";
        public const string Configure_Service = "Configure Service";
        public const string Connect_to_IP = "Connect to IP";
        public const string Connect_to_Named_Pipe = "Connect to Named Pipe";
        public const string Connect_to_Network_Share = "Connect to Network Share";
        public const string Connect_to_Socket = "Connect to Socket";
        public const string Connect_to_URL = "Connect to URL";
        public const string Control_Driver = "Control Driver";
        public const string Control_Service = "Control Service";
        public const string Copy_File = "Copy File";
        public const string Create_Dialog_Box = "Create Dialog Box";
        public const string Create_Directory = "Create Directory";
        public const string Create_Event = "Create Event";
        public const string Create_File = "Create File";
        public const string Create_File_Alternate_Data_Stream = "Create File Alternate Data Stream";
        public const string Create_File_Mapping = "Create File Mapping";
        public const string Create_File_Symbolic_Link = "Create File Symbolic Link";
        public const string Create_Hidden_File = "Create Hidden File";
        public const string Create_Mailslot = "Create Mailslot";
        public const string Create_Module = "Create Module";
        public const string Create_Mutex = "Create Mutex";
        public const string Create_Named_Pipe = "Create Named Pipe";
        public const string Create_Process = "Create Process";
        public const string Create_Process_as_User = "Create Process as User";
        public const string Create_Registry_Key = "Create Registry Key";
        public const string Create_Registry_Key_Value = "Create Registry Key Value";
        public const string Create_Remote_Thread_in_Process = "Create Remote Thread in Process";
        public const string Create_Service = "Create Service";
        public const string Create_Socket = "Create Socket";
        public const string Create_Symbolic_Link = "Create Symbolic Link";
        public const string Create_Thread = "Create Thread";
        public const string Create_Window = "Create Window";
        public const string Delete_Directory = "Delete Directory";
        public const string Delete_File = "Delete File";
        public const string Delete_Named_Pipe = "Delete Named Pipe";
        public const string Delete_Network_Share = "Delete Network Share";
        public const string Delete_Registry_Key = "Delete Registry Key";
        public const string Delete_Registry_Key_Value = "Delete Registry Key Value";
        public const string Delete_Service = "Delete Service";
        public const string Delete_User = "Delete User";
        public const string Disconnect_from_Named_Pipe = "Disconnect from Named Pipe";
        public const string Disconnect_from_Network_Share = "Disconnect from Network Share";
        public const string Disconnect_from_Socket = "Disconnect from Socket";
        public const string Download_File = "Download File";
        public const string Enumerate_DLLs = "Enumerate DLLs";
        public const string Enumerate_Network_Shares = "Enumerate Network Shares";
        public const string Enumerate_Processes = "Enumerate Processes";
        public const string Enumerate_Protocols = "Enumerate Protocols";
        public const string Enumerate_Registry_Key_Subkeys = "Enumerate Registry Key Subkeys";
        public const string Enumerate_Registry_Key_Values = "Enumerate Registry Key Values";
        public const string Enumerate_Services = "Enumerate Services";
        public const string Enumerate_System_Handles = "Enumerate System Handles";
        public const string Enumerate_Threads = "Enumerate Threads";
        public const string Enumerate_Threads_in_Process = "Enumerate Threads in Process";
        public const string Enumerate_Users = "Enumerate Users";
        public const string Enumerate_Windows = "Enumerate Windows";
        public const string Find_File = "Find File";
        public const string Find_Window = "Find Window";
        public const string Flush_Process_Instruction_Cache = "Flush Process Instruction Cache";
        public const string Free_Library = "Free Library";
        public const string Free_Process_Virtual_Memory = "Free Process Virtual Memory";
        public const string Get_Disk_Free_Space = "Get Disk Free Space";
        public const string Get_Disk_Type = "Get Disk Type";
        public const string Get_Elapsed_System_Up_Time = "Get Elapsed System Up Time";
        public const string Get_File_Attributes = "Get File Attributes";
        public const string Get_Function_Address = "Get Function Address";
        public const string Get_Host_By_Address = "Get Host By Address";
        public const string Get_Host_By_Name = "Get Host By Name";
        public const string Get_Host_Name = "Get Host Name";
        public const string Get_Library_File_Name = "Get Library File Name";
        public const string Get_Library_Handle = "Get Library Handle";
        public const string Get_NetBIOS_Name = "Get NetBIOS Name";
        public const string Get_Process_Current_Directory = "Get Process Current Directory";
        public const string Get_Process_Environment_Variable = "Get Process Environment Variable";
        public const string Get_Process_Startup_Information = "Get Process Startup Information";
        public const string Get_Processes_Snapshot = "Get Processes Snapshot";
        public const string Get_Registry_Key_Attributes = "Get Registry Key Attributes";
        public const string Get_Service_Status = "Get Service Status";
        public const string Get_System_Global_Flags = "Get System Global Flags";
        public const string Get_System_Host_Name = "Get System Host Name";
        public const string Get_System_Local_Time = "Get System Local Time";
        public const string Get_System_NetBIOS_Name = "Get System NetBIOS Name";
        public const string Get_System_Network_Parameters = "Get System Network Parameters";
        public const string Get_System_Time = "Get System Time";
        public const string Get_Thread_Context = "Get Thread Context";
        public const string Get_Thread_Username = "Get Thread Username";
        public const string Get_User_Attributes = "Get User Attributes";
        public const string Get_Username = "Get Username";
        public const string Get_Windows_Directory = "Get Windows Directory";
        public const string Get_Windows_System_Directory = "Get Windows System Directory";
        public const string Get_Windows_Temporary_Files_Directory = "Get Windows Temporary Files Directory";
        public const string Hide_Window = "Hide Window";
        public const string Impersonate_Process = "Impersonate Process";
        public const string Impersonate_Thread = "Impersonate Thread";
        public const string Inject_Memory_Page = "Inject Memory Page";
        public const string Kill_Process = "Kill Process";
        public const string Kill_Thread = "Kill Thread";
        public const string Kill_Window = "Kill Window";
        public const string Listen_on_Port = "Listen on Port";
        public const string Listen_on_Socket = "Listen on Socket";
        public const string Load_Driver = "Load Driver";
        public const string Load_Library = "Load Library";
        public const string Load_Module = "Load Module";
        public const string Load_and_Call_Driver = "Load and Call Driver";
        public const string Lock_File = "Lock File";
        public const string Logon_as_User = "Logon as User";
        public const string Map_File = "Map File";
        public const string Map_Library = "Map Library";
        public const string Map_View_of_File = "Map View of File";
        public const string Modify_File = "Modify File";
        public const string Modify_Named_Pipe = "Modify Named Pipe";
        public const string Modify_Process = "Modify Process";
        public const string Modify_Registry_Key = "Modify Registry Key";
        public const string Modify_Registry_Key_Value = "Modify Registry Key Value";
        public const string Modify_Service = "Modify Service";
        public const string Monitor_Registry_Key = "Monitor Registry Key";
        public const string Move_File = "Move File";
        public const string Open_File = "Open File";
        public const string Open_File_Mapping = "Open File Mapping";
        public const string Open_Mutex = "Open Mutex";
        public const string Open_Port = "Open Port";
        public const string Open_Process = "Open Process";
        public const string Open_Registry_Key = "Open Registry Key";
        public const string Open_Service = "Open Service";
        public const string Open_Service_Control_Manager = "Open Service Control Manager";
        public const string Protect_Virtual_Memory = "Protect Virtual Memory";
        public const string Query_DNS = "Query DNS";
        public const string Query_Disk_Attributes = "Query Disk Attributes";
        public const string Query_Process_Virtual_Memory = "Query Process Virtual Memory";
        public const string Queue_APC_in_Thread = "Queue APC in Thread";
        public const string Read_File = "Read File";
        public const string Read_From_Named_Pipe = "Read From Named Pipe";
        public const string Read_From_Process_Memory = "Read From Process Memory";
        public const string Read_Registry_Key_Value = "Read Registry Key Value";
        public const string Receive_Data_on_Socket = "Receive Data on Socket";
        public const string Receive_Email_Message = "Receive Email Message";
        public const string Release_Mutex = "Release Mutex";
        public const string Rename_File = "Rename File";
        public const string Revert_Thread_to_Self = "Revert Thread to Self";
        public const string Send_Control_Code_to_File = "Send Control Code to File";
        public const string Send_Control_Code_to_Pipe = "Send Control Code to Pipe";
        public const string Send_Control_Code_to_Service = "Send Control Code to Service";
        public const string Send_DNS_Query = "Send DNS Query";
        public const string Send_Data_on_Socket = "Send Data on Socket";
        public const string Send_Data_to_Address_on_Socket = "Send Data to Address on Socket";
        public const string Send_Email_Message = "Send Email Message";
        public const string Send_ICMP_Request = "Send ICMP Request";
        public const string Send_Reverse_DNS_Query = "Send Reverse DNS Query";
        public const string Set_File_Attributes = "Set File Attributes";
        public const string Set_NetBIOS_Name = "Set NetBIOS Name";
        public const string Set_Process_Current_Directory = "Set Process Current Directory";
        public const string Set_Process_Environment_Variable = "Set Process Environment Variable";
        public const string Set_System_Global_Flags = "Set System Global Flags";
        public const string Set_System_Host_Name = "Set System Host Name";
        public const string Set_System_Time = "Set System Time";
        public const string Set_Thread_Context = "Set Thread Context";
        public const string Show_Window = "Show Window";
        public const string Shutdown_System = "Shutdown System";
        public const string Sleep_Process = "Sleep Process";
        public const string Sleep_System = "Sleep System";
        public const string Start_Service = "Start Service";
        public const string Unload_Driver = "Unload Driver";
        public const string Unload_Module = "Unload Module";
        public const string Unlock_File = "Unlock File";
        public const string Unmap_File = "Unmap File";
        public const string Upload_File = "Upload File";
        public const string Write_to_File = "Write to File";
        public const string Write_to_Process_Virtual_Memory = "Write to Process Virtual Memory";
    }

    /// <summary>Vocabulary: ActionRelationshipTypeVocab</summary>
    public static class ActionRelationshipTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionRelationshipTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Dependent_On", "Equivalent_To", "Followed_By", "Initiated", "Initiated_By", "Preceded_By", "Related_To" };
        public const string Dependent_On = "Dependent_On";
        public const string Equivalent_To = "Equivalent_To";
        public const string Followed_By = "Followed_By";
        public const string Initiated = "Initiated";
        public const string Initiated_By = "Initiated_By";
        public const string Preceded_By = "Preceded_By";
        public const string Related_To = "Related_To";
    }

    /// <summary>Vocabulary: ActionStatusTypeVocab</summary>
    public static class ActionStatusTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionStatusTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Complete/Finish", "Error", "Fail", "Ongoing", "Pending", "Success", "Unknown" };
        public const string Complete_Finish = "Complete/Finish";
        public const string Error = "Error";
        public const string Fail = "Fail";
        public const string Ongoing = "Ongoing";
        public const string Pending = "Pending";
        public const string Success = "Success";
        public const string Unknown = "Unknown";
    }

    /// <summary>Vocabulary: ActionTypeVocab</summary>
    public static class ActionTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ActionTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Accept", "Access", "Add", "Alert", "Allocate", "Archive", "Assign", "Audit", "Backup", "Bind", "Block", "Call", "Change", "Check", "Clean", "Click", "Close", "Compare", "Compress", "Configure", "Connect", "Control", "Copy/Duplicate", "Create", "Decode", "Decompress", "Decrypt", "Deny", "Depress", "Detect", "Disconnect", "Download", "Draw", "Drop", "Encode", "Encrypt", "Enumerate", "Execute", "Extract", "Filter", "Find", "Flush", "Fork", "Free", "Get", "Hide", "Hook", "Impersonate", "Initialize", "Inject", "Install", "Interleave", "Join", "Kill", "Listen", "Load", "Lock", "Login/Logon", "Logout/Logoff", "Map", "Merge", "Modify", "Monitor", "Move", "Open", "Pack", "Pause", "Press", "Protect", "Quarantine", "Query", "Queue", "Raise", "Read", "Receive", "Release", "Remove/Delete", "Rename", "Replicate", "Restore", "Resume", "Revert", "Run", "Save", "Scan", "Schedule", "Search", "Send", "Set", "Shutdown", "Sleep", "Snapshot", "Start", "Stop", "Suspend", "Synchronize", "Throw", "Transmit", "Unblock", "Unhide", "Unhook", "Uninstall", "Unload", "Unlock", "Unmap", "Unpack", "Update", "Upgrade", "Upload", "Wipe/Destroy/Purge", "Write" };
        public const string Accept = "Accept";
        public const string Access = "Access";
        public const string Add = "Add";
        public const string Alert = "Alert";
        public const string Allocate = "Allocate";
        public const string Archive = "Archive";
        public const string Assign = "Assign";
        public const string Audit = "Audit";
        public const string Backup = "Backup";
        public const string Bind = "Bind";
        public const string Block = "Block";
        public const string Call = "Call";
        public const string Change = "Change";
        public const string Check = "Check";
        public const string Clean = "Clean";
        public const string Click = "Click";
        public const string Close = "Close";
        public const string Compare = "Compare";
        public const string Compress = "Compress";
        public const string Configure = "Configure";
        public const string Connect = "Connect";
        public const string Control = "Control";
        public const string Copy_Duplicate = "Copy/Duplicate";
        public const string Create = "Create";
        public const string Decode = "Decode";
        public const string Decompress = "Decompress";
        public const string Decrypt = "Decrypt";
        public const string Deny = "Deny";
        public const string Depress = "Depress";
        public const string Detect = "Detect";
        public const string Disconnect = "Disconnect";
        public const string Download = "Download";
        public const string Draw = "Draw";
        public const string Drop = "Drop";
        public const string Encode = "Encode";
        public const string Encrypt = "Encrypt";
        public const string Enumerate = "Enumerate";
        public const string Execute = "Execute";
        public const string Extract = "Extract";
        public const string Filter = "Filter";
        public const string Find = "Find";
        public const string Flush = "Flush";
        public const string Fork = "Fork";
        public const string Free = "Free";
        public const string Get = "Get";
        public const string Hide = "Hide";
        public const string Hook = "Hook";
        public const string Impersonate = "Impersonate";
        public const string Initialize = "Initialize";
        public const string Inject = "Inject";
        public const string Install = "Install";
        public const string Interleave = "Interleave";
        public const string Join = "Join";
        public const string Kill = "Kill";
        public const string Listen = "Listen";
        public const string Load = "Load";
        public const string Lock = "Lock";
        public const string Login_Logon = "Login/Logon";
        public const string Logout_Logoff = "Logout/Logoff";
        public const string Map = "Map";
        public const string Merge = "Merge";
        public const string Modify = "Modify";
        public const string Monitor = "Monitor";
        public const string Move = "Move";
        public const string Open = "Open";
        public const string Pack = "Pack";
        public const string Pause = "Pause";
        public const string Press = "Press";
        public const string Protect = "Protect";
        public const string Quarantine = "Quarantine";
        public const string Query = "Query";
        public const string Queue = "Queue";
        public const string Raise = "Raise";
        public const string Read = "Read";
        public const string Receive = "Receive";
        public const string Release = "Release";
        public const string Remove_Delete = "Remove/Delete";
        public const string Rename = "Rename";
        public const string Replicate = "Replicate";
        public const string Restore = "Restore";
        public const string Resume = "Resume";
        public const string Revert = "Revert";
        public const string Run = "Run";
        public const string Save = "Save";
        public const string Scan = "Scan";
        public const string Schedule = "Schedule";
        public const string Search = "Search";
        public const string Send = "Send";
        public const string Set = "Set";
        public const string Shutdown = "Shutdown";
        public const string Sleep = "Sleep";
        public const string Snapshot = "Snapshot";
        public const string Start = "Start";
        public const string Stop = "Stop";
        public const string Suspend = "Suspend";
        public const string Synchronize = "Synchronize";
        public const string Throw = "Throw";
        public const string Transmit = "Transmit";
        public const string Unblock = "Unblock";
        public const string Unhide = "Unhide";
        public const string Unhook = "Unhook";
        public const string Uninstall = "Uninstall";
        public const string Unload = "Unload";
        public const string Unlock = "Unlock";
        public const string Unmap = "Unmap";
        public const string Unpack = "Unpack";
        public const string Update = "Update";
        public const string Upgrade = "Upgrade";
        public const string Upload = "Upload";
        public const string Wipe_Destroy_Purge = "Wipe/Destroy/Purge";
        public const string Write = "Write";
    }

    /// <summary>Vocabulary: BitnessVocab</summary>
    public static class BitnessVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/BitnessVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "32", "64" };
        public const string _32 = "32";
        public const string _64 = "64";
    }

    /// <summary>Vocabulary: CharacterEncodingVocab</summary>
    public static class CharacterEncodingVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/CharacterEncodingVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "ASCII", "UTF-16", "UTF-32", "UTF-8", "Windows-1250", "Windows-1251", "Windows-1252", "Windows-1253", "Windows-1254", "Windows-1255", "Windows-1256", "Windows-1257", "Windows-1258" };
        public const string ASCII = "ASCII";
        public const string UTF_16 = "UTF-16";
        public const string UTF_32 = "UTF-32";
        public const string UTF_8 = "UTF-8";
        public const string Windows_1250 = "Windows-1250";
        public const string Windows_1251 = "Windows-1251";
        public const string Windows_1252 = "Windows-1252";
        public const string Windows_1253 = "Windows-1253";
        public const string Windows_1254 = "Windows-1254";
        public const string Windows_1255 = "Windows-1255";
        public const string Windows_1256 = "Windows-1256";
        public const string Windows_1257 = "Windows-1257";
        public const string Windows_1258 = "Windows-1258";
    }

    /// <summary>Vocabulary: ContactAddressScopeVocab</summary>
    public static class ContactAddressScopeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactAddressScopeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "home", "school", "work" };
        public const string home = "home";
        public const string school = "school";
        public const string work = "work";
    }

    /// <summary>Vocabulary: ContactEmailScopeVocab</summary>
    public static class ContactEmailScopeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactEmailScopeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "cloud", "home", "school", "work" };
        public const string cloud = "cloud";
        public const string home = "home";
        public const string school = "school";
        public const string work = "work";
    }

    /// <summary>Vocabulary: ContactPhoneScopeVocab</summary>
    public static class ContactPhoneScopeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactPhoneScopeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "home", "home fax", "main", "mobile", "pager", "school", "work", "work fax" };
        public const string home = "home";
        public const string home_fax = "home fax";
        public const string main = "main";
        public const string mobile = "mobile";
        public const string pager = "pager";
        public const string school = "school";
        public const string work = "work";
        public const string work_fax = "work fax";
    }

    /// <summary>Vocabulary: ContactSIPScopeVocab</summary>
    public static class ContactSIPScopeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactSIPScopeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "home", "school", "work" };
        public const string home = "home";
        public const string school = "school";
        public const string work = "work";
    }

    /// <summary>Vocabulary: ContactURLScopeVocab</summary>
    public static class ContactURLScopeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ContactURLScopeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "home", "homepage", "school", "work" };
        public const string home = "home";
        public const string homepage = "homepage";
        public const string school = "school";
        public const string work = "work";
    }

    /// <summary>Vocabulary: DiskTypeVocab</summary>
    public static class DiskTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/DiskTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "CDRom", "Fixed", "RAMDisk", "Remote", "Removable" };
        public const string CDRom = "CDRom";
        public const string Fixed = "Fixed";
        public const string RAMDisk = "RAMDisk";
        public const string Remote = "Remote";
        public const string Removable = "Removable";
    }

    /// <summary>Vocabulary: EndiannessTypeVocab</summary>
    public static class EndiannessTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/EndiannessTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Big-endian", "Little-endian", "Middle-endian" };
        public const string Big_endian = "Big-endian";
        public const string Little_endian = "Little-endian";
        public const string Middle_endian = "Middle-endian";
    }

    /// <summary>Vocabulary: HashNameVocab</summary>
    public static class HashNameVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/HashNameVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "MD5", "MD6", "SHA1", "SHA224", "SHA256", "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512", "SHA384", "SHA512", "SSDEEP" };
        public const string MD5 = "MD5";
        public const string MD6 = "MD6";
        public const string SHA1 = "SHA1";
        public const string SHA224 = "SHA224";
        public const string SHA256 = "SHA256";
        public const string SHA3_224 = "SHA3-224";
        public const string SHA3_256 = "SHA3-256";
        public const string SHA3_384 = "SHA3-384";
        public const string SHA3_512 = "SHA3-512";
        public const string SHA384 = "SHA384";
        public const string SHA512 = "SHA512";
        public const string SSDEEP = "SSDEEP";
    }

    /// <summary>Vocabulary: LibraryTypeVocab</summary>
    public static class LibraryTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/LibraryTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Dynamic", "Other", "Remote", "Shared", "Static" };
        public const string Dynamic = "Dynamic";
        public const string Other = "Other";
        public const string Remote = "Remote";
        public const string Shared = "Shared";
        public const string Static = "Static";
    }

    /// <summary>Vocabulary: MemoryBlockTypeVocab</summary>
    public static class MemoryBlockTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/MemoryBlockTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Bit-mapped", "Byte-mapped", "Initialized", "Overlay", "Uninitialized" };
        public const string Bit_mapped = "Bit-mapped";
        public const string Byte_mapped = "Byte-mapped";
        public const string Initialized = "Initialized";
        public const string Overlay = "Overlay";
        public const string Uninitialized = "Uninitialized";
    }

    /// <summary>Vocabulary: NetworkSocketAddressFamily</summary>
    public static class NetworkSocketAddressFamily
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketAddressFamily";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "af_appletalk", "af_bth", "af_inet", "af_inet6", "af_ipx", "af_irda", "af_netbios", "af_unspec" };
        public const string af_appletalk = "af_appletalk";
        public const string af_bth = "af_bth";
        public const string af_inet = "af_inet";
        public const string af_inet6 = "af_inet6";
        public const string af_ipx = "af_ipx";
        public const string af_irda = "af_irda";
        public const string af_netbios = "af_netbios";
        public const string af_unspec = "af_unspec";
    }

    /// <summary>Vocabulary: NetworkSocketProtocolFamily</summary>
    public static class NetworkSocketProtocolFamily
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketProtocolFamily";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "pf_appletalk", "pf_ash", "pf_atmpvc", "pf_atmsvc", "pf_ax25", "pf_bluetooth", "pf_bridge", "pf_decnet", "pf_econet", "pf_inet", "pf_inet6", "pf_ipx", "pf_irda", "pf_key", "pf_netbeui", "pf_netlink", "pf_netrom", "pf_packet", "pf_pppox", "pf_rose", "pf_route", "pf_security", "pf_sna", "pf_wanpipe", "pf_x25" };
        public const string pf_appletalk = "pf_appletalk";
        public const string pf_ash = "pf_ash";
        public const string pf_atmpvc = "pf_atmpvc";
        public const string pf_atmsvc = "pf_atmsvc";
        public const string pf_ax25 = "pf_ax25";
        public const string pf_bluetooth = "pf_bluetooth";
        public const string pf_bridge = "pf_bridge";
        public const string pf_decnet = "pf_decnet";
        public const string pf_econet = "pf_econet";
        public const string pf_inet = "pf_inet";
        public const string pf_inet6 = "pf_inet6";
        public const string pf_ipx = "pf_ipx";
        public const string pf_irda = "pf_irda";
        public const string pf_key = "pf_key";
        public const string pf_netbeui = "pf_netbeui";
        public const string pf_netlink = "pf_netlink";
        public const string pf_netrom = "pf_netrom";
        public const string pf_packet = "pf_packet";
        public const string pf_pppox = "pf_pppox";
        public const string pf_rose = "pf_rose";
        public const string pf_route = "pf_route";
        public const string pf_security = "pf_security";
        public const string pf_sna = "pf_sna";
        public const string pf_wanpipe = "pf_wanpipe";
        public const string pf_x25 = "pf_x25";
    }

    /// <summary>Vocabulary: NetworkSocketType</summary>
    public static class NetworkSocketType
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSocketType";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "sock_dgram", "sock_raw", "sock_rdm", "sock_seqpacket", "sock_stream" };
        public const string sock_dgram = "sock_dgram";
        public const string sock_raw = "sock_raw";
        public const string sock_rdm = "sock_rdm";
        public const string sock_seqpacket = "sock_seqpacket";
        public const string sock_stream = "sock_stream";
    }

    /// <summary>Vocabulary: ObjectStatusVocab</summary>
    public static class ObjectStatusVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/core/ObjectStatusVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Deprecated", "Draft", "Final" };
        public const string Deprecated = "Deprecated";
        public const string Draft = "Draft";
        public const string Final = "Final";
    }

    /// <summary>Vocabulary: ObservableObjectRelationshipVocab</summary>
    public static class ObservableObjectRelationshipVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectRelationshipVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Allocated", "Allocated_By", "Attachment_Of", "Bound", "Bound_By", "Characterized_By", "Characterizes", "Child_Of", "Closed", "Closed_By", "Compressed", "Compressed_By", "Compressed_From", "Compressed_Into", "Connected_From", "Connected_To", "Contained_Within", "Contains", "Copied", "Copied_By", "Copied_From", "Copied_To", "Created", "Created_By", "Decoded", "Decoded_By", "Decompressed", "Decompressed_By", "Decrypted", "Decrypted_By", "Deleted", "Deleted_By", "Deleted_From", "Downloaded", "Downloaded_By", "Downloaded_From", "Downloaded_To", "Dropped", "Dropped_By", "Encoded", "Encoded_By", "Encrypted", "Encrypted_By", "Encrypted_From", "Encrypted_To", "Extracted_From", "FQDN_Of", "Freed", "Freed_By", "Had_Attachment", "Hooked", "Hooked_By", "Initialized_By", "Initialized_To", "Injected", "Injected_As", "Injected_By", "Injected_Into", "Installed", "Installed_By", "Joined", "Joined_By", "Killed", "Killed_By", "Listened_On", "Listened_On_By", "Loaded_From", "Loaded_Into", "Locked", "Locked_By", "Mapped_By", "Mapped_Into", "Merged", "Merged_By", "Modified_Properties_Of", "Monitored", "Monitored_By", "Moved", "Moved_By", "Moved_From", "Moved_To", "Opened", "Opened_By", "Packed", "Packed_By", "Packed_From", "Packed_Into", "Parent_Of", "Paused", "Paused_By", "Previously_Contained", "Properties_Modified_By", "Properties_Queried", "Properties_Queried_By", "Read_From", "Read_From_By", "Received", "Received_By", "Received_From", "Received_Via_Upload", "Redirects_To", "Related_To", "Renamed", "Renamed_By", "Renamed_From", "Renamed_To", "Resolved_To", "Resumed", "Resumed_By", "Root_Domain_Of", "Searched_For", "Searched_For_By", "Sent", "Sent_By", "Sent_To", "Sent_Via_Upload", "Set_From", "Set_To", "Signed_By", "Sub-domain_Of", "Supra-domain_Of", "Suspended", "Suspended_By", "Unhooked", "Unhooked_By", "Unlocked", "Unlocked_By", "Unpacked", "Unpacked_By", "Uploaded", "Uploaded_By", "Uploaded_From", "Uploaded_To", "Used", "Used_By", "Values_Enumerated", "Values_Enumerated_By", "Written_To_By", "Wrote_To" };
        public const string Allocated = "Allocated";
        public const string Allocated_By = "Allocated_By";
        public const string Attachment_Of = "Attachment_Of";
        public const string Bound = "Bound";
        public const string Bound_By = "Bound_By";
        public const string Characterized_By = "Characterized_By";
        public const string Characterizes = "Characterizes";
        public const string Child_Of = "Child_Of";
        public const string Closed = "Closed";
        public const string Closed_By = "Closed_By";
        public const string Compressed = "Compressed";
        public const string Compressed_By = "Compressed_By";
        public const string Compressed_From = "Compressed_From";
        public const string Compressed_Into = "Compressed_Into";
        public const string Connected_From = "Connected_From";
        public const string Connected_To = "Connected_To";
        public const string Contained_Within = "Contained_Within";
        public const string Contains = "Contains";
        public const string Copied = "Copied";
        public const string Copied_By = "Copied_By";
        public const string Copied_From = "Copied_From";
        public const string Copied_To = "Copied_To";
        public const string Created = "Created";
        public const string Created_By = "Created_By";
        public const string Decoded = "Decoded";
        public const string Decoded_By = "Decoded_By";
        public const string Decompressed = "Decompressed";
        public const string Decompressed_By = "Decompressed_By";
        public const string Decrypted = "Decrypted";
        public const string Decrypted_By = "Decrypted_By";
        public const string Deleted = "Deleted";
        public const string Deleted_By = "Deleted_By";
        public const string Deleted_From = "Deleted_From";
        public const string Downloaded = "Downloaded";
        public const string Downloaded_By = "Downloaded_By";
        public const string Downloaded_From = "Downloaded_From";
        public const string Downloaded_To = "Downloaded_To";
        public const string Dropped = "Dropped";
        public const string Dropped_By = "Dropped_By";
        public const string Encoded = "Encoded";
        public const string Encoded_By = "Encoded_By";
        public const string Encrypted = "Encrypted";
        public const string Encrypted_By = "Encrypted_By";
        public const string Encrypted_From = "Encrypted_From";
        public const string Encrypted_To = "Encrypted_To";
        public const string Extracted_From = "Extracted_From";
        public const string FQDN_Of = "FQDN_Of";
        public const string Freed = "Freed";
        public const string Freed_By = "Freed_By";
        public const string Had_Attachment = "Had_Attachment";
        public const string Hooked = "Hooked";
        public const string Hooked_By = "Hooked_By";
        public const string Initialized_By = "Initialized_By";
        public const string Initialized_To = "Initialized_To";
        public const string Injected = "Injected";
        public const string Injected_As = "Injected_As";
        public const string Injected_By = "Injected_By";
        public const string Injected_Into = "Injected_Into";
        public const string Installed = "Installed";
        public const string Installed_By = "Installed_By";
        public const string Joined = "Joined";
        public const string Joined_By = "Joined_By";
        public const string Killed = "Killed";
        public const string Killed_By = "Killed_By";
        public const string Listened_On = "Listened_On";
        public const string Listened_On_By = "Listened_On_By";
        public const string Loaded_From = "Loaded_From";
        public const string Loaded_Into = "Loaded_Into";
        public const string Locked = "Locked";
        public const string Locked_By = "Locked_By";
        public const string Mapped_By = "Mapped_By";
        public const string Mapped_Into = "Mapped_Into";
        public const string Merged = "Merged";
        public const string Merged_By = "Merged_By";
        public const string Modified_Properties_Of = "Modified_Properties_Of";
        public const string Monitored = "Monitored";
        public const string Monitored_By = "Monitored_By";
        public const string Moved = "Moved";
        public const string Moved_By = "Moved_By";
        public const string Moved_From = "Moved_From";
        public const string Moved_To = "Moved_To";
        public const string Opened = "Opened";
        public const string Opened_By = "Opened_By";
        public const string Packed = "Packed";
        public const string Packed_By = "Packed_By";
        public const string Packed_From = "Packed_From";
        public const string Packed_Into = "Packed_Into";
        public const string Parent_Of = "Parent_Of";
        public const string Paused = "Paused";
        public const string Paused_By = "Paused_By";
        public const string Previously_Contained = "Previously_Contained";
        public const string Properties_Modified_By = "Properties_Modified_By";
        public const string Properties_Queried = "Properties_Queried";
        public const string Properties_Queried_By = "Properties_Queried_By";
        public const string Read_From = "Read_From";
        public const string Read_From_By = "Read_From_By";
        public const string Received = "Received";
        public const string Received_By = "Received_By";
        public const string Received_From = "Received_From";
        public const string Received_Via_Upload = "Received_Via_Upload";
        public const string Redirects_To = "Redirects_To";
        public const string Related_To = "Related_To";
        public const string Renamed = "Renamed";
        public const string Renamed_By = "Renamed_By";
        public const string Renamed_From = "Renamed_From";
        public const string Renamed_To = "Renamed_To";
        public const string Resolved_To = "Resolved_To";
        public const string Resumed = "Resumed";
        public const string Resumed_By = "Resumed_By";
        public const string Root_Domain_Of = "Root_Domain_Of";
        public const string Searched_For = "Searched_For";
        public const string Searched_For_By = "Searched_For_By";
        public const string Sent = "Sent";
        public const string Sent_By = "Sent_By";
        public const string Sent_To = "Sent_To";
        public const string Sent_Via_Upload = "Sent_Via_Upload";
        public const string Set_From = "Set_From";
        public const string Set_To = "Set_To";
        public const string Signed_By = "Signed_By";
        public const string Sub_domain_Of = "Sub-domain_Of";
        public const string Supra_domain_Of = "Supra-domain_Of";
        public const string Suspended = "Suspended";
        public const string Suspended_By = "Suspended_By";
        public const string Unhooked = "Unhooked";
        public const string Unhooked_By = "Unhooked_By";
        public const string Unlocked = "Unlocked";
        public const string Unlocked_By = "Unlocked_By";
        public const string Unpacked = "Unpacked";
        public const string Unpacked_By = "Unpacked_By";
        public const string Uploaded = "Uploaded";
        public const string Uploaded_By = "Uploaded_By";
        public const string Uploaded_From = "Uploaded_From";
        public const string Uploaded_To = "Uploaded_To";
        public const string Used = "Used";
        public const string Used_By = "Used_By";
        public const string Values_Enumerated = "Values_Enumerated";
        public const string Values_Enumerated_By = "Values_Enumerated_By";
        public const string Written_To_By = "Written_To_By";
        public const string Wrote_To = "Wrote_To";
    }

    /// <summary>Vocabulary: ObservableObjectStateVocab</summary>
    public static class ObservableObjectStateVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ObservableObjectStateVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Active", "Closed", "Does Not Exist", "Exists", "Inactive", "Locked", "Open", "Started", "Stopped", "Unlocked" };
        public const string Active = "Active";
        public const string Closed = "Closed";
        public const string Does_Not_Exist = "Does Not Exist";
        public const string Exists = "Exists";
        public const string Inactive = "Inactive";
        public const string Locked = "Locked";
        public const string Open = "Open";
        public const string Started = "Started";
        public const string Stopped = "Stopped";
        public const string Unlocked = "Unlocked";
    }

    /// <summary>Vocabulary: PartitionTypeVocab</summary>
    public static class PartitionTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/PartitionTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "PARTITION_ENTRY_UNUSED", "PARTITION_EXTENDED", "PARTITION_FAT32", "PARTITION_FAT32_XINT13", "PARTITION_FAT_12", "PARTITION_FAT_16", "PARTITION_HUGE", "PARTITION_IFS", "PARTITION_LDM", "PARTITION_NTFT", "PARTITION_OS2BOOTMGR", "PARTITION_PREP", "PARTITION_UNIX", "PARTITION_XENIX_1", "PARTITION_XENIX_2", "PARTITION_XINT13", "PARTITION_XINT13_EXTENDED", "UNKNOWN", "VALID_NTFT" };
        public const string PARTITION_ENTRY_UNUSED = "PARTITION_ENTRY_UNUSED";
        public const string PARTITION_EXTENDED = "PARTITION_EXTENDED";
        public const string PARTITION_FAT32 = "PARTITION_FAT32";
        public const string PARTITION_FAT32_XINT13 = "PARTITION_FAT32_XINT13";
        public const string PARTITION_FAT_12 = "PARTITION_FAT_12";
        public const string PARTITION_FAT_16 = "PARTITION_FAT_16";
        public const string PARTITION_HUGE = "PARTITION_HUGE";
        public const string PARTITION_IFS = "PARTITION_IFS";
        public const string PARTITION_LDM = "PARTITION_LDM";
        public const string PARTITION_NTFT = "PARTITION_NTFT";
        public const string PARTITION_OS2BOOTMGR = "PARTITION_OS2BOOTMGR";
        public const string PARTITION_PREP = "PARTITION_PREP";
        public const string PARTITION_UNIX = "PARTITION_UNIX";
        public const string PARTITION_XENIX_1 = "PARTITION_XENIX_1";
        public const string PARTITION_XENIX_2 = "PARTITION_XENIX_2";
        public const string PARTITION_XINT13 = "PARTITION_XINT13";
        public const string PARTITION_XINT13_EXTENDED = "PARTITION_XINT13_EXTENDED";
        public const string UNKNOWN = "UNKNOWN";
        public const string VALID_NTFT = "VALID_NTFT";
    }

    /// <summary>Vocabulary: ProcessorArchVocab</summary>
    public static class ProcessorArchVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ProcessorArchVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "ARM", "Alpha", "IA-64", "MIPS", "Motorola 68k", "Other", "PowerPC", "SPARC", "eSi-RISC", "x86-32", "x86-64", "z/Architecture" };
        public const string ARM = "ARM";
        public const string Alpha = "Alpha";
        public const string IA_64 = "IA-64";
        public const string MIPS = "MIPS";
        public const string Motorola_68k = "Motorola 68k";
        public const string Other = "Other";
        public const string PowerPC = "PowerPC";
        public const string SPARC = "SPARC";
        public const string eSi_RISC = "eSi-RISC";
        public const string x86_32 = "x86-32";
        public const string x86_64 = "x86-64";
        public const string z_Architecture = "z/Architecture";
    }

    /// <summary>Vocabulary: RecoveredObjectStatusVocab</summary>
    public static class RecoveredObjectStatusVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RecoveredObjectStatusVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "overwritten", "partially recovered", "recovered", "unknown" };
        public const string overwritten = "overwritten";
        public const string partially_recovered = "partially recovered";
        public const string recovered = "recovered";
        public const string unknown = "unknown";
    }

    /// <summary>Vocabulary: RegionalRegistryTypeVocab</summary>
    public static class RegionalRegistryTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RegionalRegistryTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "APNIC", "ARIN", "AfriNIC", "LACNIC", "RIPE NCC" };
        public const string APNIC = "APNIC";
        public const string ARIN = "ARIN";
        public const string AfriNIC = "AfriNIC";
        public const string LACNIC = "LACNIC";
        public const string RIPE_NCC = "RIPE NCC";
    }

    /// <summary>Vocabulary: RegistryDatatype</summary>
    public static class RegistryDatatype
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/RegistryDatatype";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "reg_binary", "reg_dword", "reg_dword_big_endian", "reg_expand_sz", "reg_full_resource_descriptor", "reg_invalid_type", "reg_link", "reg_multi_sz", "reg_none", "reg_qword", "reg_resource_list", "reg_resource_requirements_list", "reg_sz" };
        public const string reg_binary = "reg_binary";
        public const string reg_dword = "reg_dword";
        public const string reg_dword_big_endian = "reg_dword_big_endian";
        public const string reg_expand_sz = "reg_expand_sz";
        public const string reg_full_resource_descriptor = "reg_full_resource_descriptor";
        public const string reg_invalid_type = "reg_invalid_type";
        public const string reg_link = "reg_link";
        public const string reg_multi_sz = "reg_multi_sz";
        public const string reg_none = "reg_none";
        public const string reg_qword = "reg_qword";
        public const string reg_resource_list = "reg_resource_list";
        public const string reg_resource_requirements_list = "reg_resource_requirements_list";
        public const string reg_sz = "reg_sz";
    }

    /// <summary>Vocabulary: RegistryDatatypeVocab</summary>
    public static class RegistryDatatypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/RegistryDatatypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "reg_binary", "reg_dword", "reg_dword_big_endian", "reg_expand_sz", "reg_full_resource_descriptor", "reg_invalid_type", "reg_link", "reg_multi_sz", "reg_none", "reg_qword", "reg_resource_list", "reg_resource_requirements_list", "reg_sz" };
        public const string reg_binary = "reg_binary";
        public const string reg_dword = "reg_dword";
        public const string reg_dword_big_endian = "reg_dword_big_endian";
        public const string reg_expand_sz = "reg_expand_sz";
        public const string reg_full_resource_descriptor = "reg_full_resource_descriptor";
        public const string reg_invalid_type = "reg_invalid_type";
        public const string reg_link = "reg_link";
        public const string reg_multi_sz = "reg_multi_sz";
        public const string reg_none = "reg_none";
        public const string reg_qword = "reg_qword";
        public const string reg_resource_list = "reg_resource_list";
        public const string reg_resource_requirements_list = "reg_resource_requirements_list";
        public const string reg_sz = "reg_sz";
    }

    /// <summary>Vocabulary: SIMFormVocab</summary>
    public static class SIMFormVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMFormVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Full-size SIM", "Micro SIM", "Nano SIM" };
        public const string Full_size_SIM = "Full-size SIM";
        public const string Micro_SIM = "Micro SIM";
        public const string Nano_SIM = "Nano SIM";
    }

    /// <summary>Vocabulary: SIMTypeVocab</summary>
    public static class SIMTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/SIMTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "SIM", "UICC", "USIM" };
        public const string SIM = "SIM";
        public const string UICC = "UICC";
        public const string USIM = "USIM";
    }

    /// <summary>Vocabulary: TaskActionTypeVocab</summary>
    public static class TaskActionTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskActionTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "TASK_ACTION_COM_HANDLER", "TASK_ACTION_EXEC", "TASK_ACTION_SEND_EMAIL", "TASK_ACTION_SHOW_MESSAGE" };
        public const string TASK_ACTION_COM_HANDLER = "TASK_ACTION_COM_HANDLER";
        public const string TASK_ACTION_EXEC = "TASK_ACTION_EXEC";
        public const string TASK_ACTION_SEND_EMAIL = "TASK_ACTION_SEND_EMAIL";
        public const string TASK_ACTION_SHOW_MESSAGE = "TASK_ACTION_SHOW_MESSAGE";
    }

    /// <summary>Vocabulary: TaskFlagVocab</summary>
    public static class TaskFlagVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskFlagVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "TASK_FLAG_DELETE_WHEN_DONE", "TASK_FLAG_DISABLED", "TASK_FLAG_DONT_START_IF_ON_BATTERIES", "TASK_FLAG_HIDDEN", "TASK_FLAG_INTERACTIVE", "TASK_FLAG_KILL_IF_GOING_ON_BATTERIES", "TASK_FLAG_KILL_ON_IDLE_END", "TASK_FLAG_RESTART_ON_IDLE_RESUME", "TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET", "TASK_FLAG_RUN_ONLY_IF_LOGGED_ON", "TASK_FLAG_START_ONLY_IF_IDLE", "TASK_FLAG_SYSTEM_REQUIRED", "TASK_FLAG_ZERO" };
        public const string TASK_FLAG_DELETE_WHEN_DONE = "TASK_FLAG_DELETE_WHEN_DONE";
        public const string TASK_FLAG_DISABLED = "TASK_FLAG_DISABLED";
        public const string TASK_FLAG_DONT_START_IF_ON_BATTERIES = "TASK_FLAG_DONT_START_IF_ON_BATTERIES";
        public const string TASK_FLAG_HIDDEN = "TASK_FLAG_HIDDEN";
        public const string TASK_FLAG_INTERACTIVE = "TASK_FLAG_INTERACTIVE";
        public const string TASK_FLAG_KILL_IF_GOING_ON_BATTERIES = "TASK_FLAG_KILL_IF_GOING_ON_BATTERIES";
        public const string TASK_FLAG_KILL_ON_IDLE_END = "TASK_FLAG_KILL_ON_IDLE_END";
        public const string TASK_FLAG_RESTART_ON_IDLE_RESUME = "TASK_FLAG_RESTART_ON_IDLE_RESUME";
        public const string TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET = "TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET";
        public const string TASK_FLAG_RUN_ONLY_IF_LOGGED_ON = "TASK_FLAG_RUN_ONLY_IF_LOGGED_ON";
        public const string TASK_FLAG_START_ONLY_IF_IDLE = "TASK_FLAG_START_ONLY_IF_IDLE";
        public const string TASK_FLAG_SYSTEM_REQUIRED = "TASK_FLAG_SYSTEM_REQUIRED";
        public const string TASK_FLAG_ZERO = "TASK_FLAG_ZERO";
    }

    /// <summary>Vocabulary: TaskPriorityVocab</summary>
    public static class TaskPriorityVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskPriorityVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "ABOVE_NORMAL_PRIORITY_CLASS", "BELOW_NORMAL_PRIORITY_CLASS", "HIGH_PRIORITY_CLASS", "IDLE_PRIORITY_CLASS", "NORMAL_PRIORITY_CLASS", "REALTIME_PRIORITY_CLASS" };
        public const string ABOVE_NORMAL_PRIORITY_CLASS = "ABOVE_NORMAL_PRIORITY_CLASS";
        public const string BELOW_NORMAL_PRIORITY_CLASS = "BELOW_NORMAL_PRIORITY_CLASS";
        public const string HIGH_PRIORITY_CLASS = "HIGH_PRIORITY_CLASS";
        public const string IDLE_PRIORITY_CLASS = "IDLE_PRIORITY_CLASS";
        public const string NORMAL_PRIORITY_CLASS = "NORMAL_PRIORITY_CLASS";
        public const string REALTIME_PRIORITY_CLASS = "REALTIME_PRIORITY_CLASS";
    }

    /// <summary>Vocabulary: TaskStatusVocab</summary>
    public static class TaskStatusVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TaskStatusVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "SCHED_E_ACCOUNT_DBASE_CORRUPT", "SCHED_E_ACCOUNT_INFORMATION_NOT_SET", "SCHED_E_ACCOUNT_NAME_NOT_FOUND", "SCHED_E_CANNOT_OPEN_TASK", "SCHED_E_INVALID_TASK", "SCHED_E_NO_SECURITY_SERVICES", "SCHED_E_SERVICE_NOT_INSTALLED", "SCHED_E_SERVICE_NOT_RUNNING", "SCHED_E_TASK_NOT_READY", "SCHED_E_TASK_NOT_RUNNING", "SCHED_E_TRIGGER_NOT_FOUND", "SCHED_E_UNKNOWN_OBJECT_VERSION", "SCHED_E_UNSUPPORTED_ACCOUNT_OPTION", "SCHED_S_EVENT_TRIGGER", "SCHED_S_TASK_DISABLED", "SCHED_S_TASK_HAS_NOT_RUN", "SCHED_S_TASK_NOT_SCHEDULED", "SCHED_S_TASK_NO_MORE_RUNS", "SCHED_S_TASK_NO_VALID_TRIGGERS", "SCHED_S_TASK_READY", "SCHED_S_TASK_RUNNING", "SCHED_S_TASK_TERMINATED", "TASK_STATE_QUEUED", "TASK_STATE_UNKNOWN" };
        public const string SCHED_E_ACCOUNT_DBASE_CORRUPT = "SCHED_E_ACCOUNT_DBASE_CORRUPT";
        public const string SCHED_E_ACCOUNT_INFORMATION_NOT_SET = "SCHED_E_ACCOUNT_INFORMATION_NOT_SET";
        public const string SCHED_E_ACCOUNT_NAME_NOT_FOUND = "SCHED_E_ACCOUNT_NAME_NOT_FOUND";
        public const string SCHED_E_CANNOT_OPEN_TASK = "SCHED_E_CANNOT_OPEN_TASK";
        public const string SCHED_E_INVALID_TASK = "SCHED_E_INVALID_TASK";
        public const string SCHED_E_NO_SECURITY_SERVICES = "SCHED_E_NO_SECURITY_SERVICES";
        public const string SCHED_E_SERVICE_NOT_INSTALLED = "SCHED_E_SERVICE_NOT_INSTALLED";
        public const string SCHED_E_SERVICE_NOT_RUNNING = "SCHED_E_SERVICE_NOT_RUNNING";
        public const string SCHED_E_TASK_NOT_READY = "SCHED_E_TASK_NOT_READY";
        public const string SCHED_E_TASK_NOT_RUNNING = "SCHED_E_TASK_NOT_RUNNING";
        public const string SCHED_E_TRIGGER_NOT_FOUND = "SCHED_E_TRIGGER_NOT_FOUND";
        public const string SCHED_E_UNKNOWN_OBJECT_VERSION = "SCHED_E_UNKNOWN_OBJECT_VERSION";
        public const string SCHED_E_UNSUPPORTED_ACCOUNT_OPTION = "SCHED_E_UNSUPPORTED_ACCOUNT_OPTION";
        public const string SCHED_S_EVENT_TRIGGER = "SCHED_S_EVENT_TRIGGER";
        public const string SCHED_S_TASK_DISABLED = "SCHED_S_TASK_DISABLED";
        public const string SCHED_S_TASK_HAS_NOT_RUN = "SCHED_S_TASK_HAS_NOT_RUN";
        public const string SCHED_S_TASK_NOT_SCHEDULED = "SCHED_S_TASK_NOT_SCHEDULED";
        public const string SCHED_S_TASK_NO_MORE_RUNS = "SCHED_S_TASK_NO_MORE_RUNS";
        public const string SCHED_S_TASK_NO_VALID_TRIGGERS = "SCHED_S_TASK_NO_VALID_TRIGGERS";
        public const string SCHED_S_TASK_READY = "SCHED_S_TASK_READY";
        public const string SCHED_S_TASK_RUNNING = "SCHED_S_TASK_RUNNING";
        public const string SCHED_S_TASK_TERMINATED = "SCHED_S_TASK_TERMINATED";
        public const string TASK_STATE_QUEUED = "TASK_STATE_QUEUED";
        public const string TASK_STATE_UNKNOWN = "TASK_STATE_UNKNOWN";
    }

    /// <summary>Vocabulary: ThreadRunningStatusVocab</summary>
    public static class ThreadRunningStatusVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/ThreadRunningStatusVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Initialized", "Ready", "Running", "Standby", "Terminated", "Transition", "Unknown", "Waiting" };
        public const string Initialized = "Initialized";
        public const string Ready = "Ready";
        public const string Running = "Running";
        public const string Standby = "Standby";
        public const string Terminated = "Terminated";
        public const string Transition = "Transition";
        public const string Unknown = "Unknown";
        public const string Waiting = "Waiting";
    }

    /// <summary>Vocabulary: TimestampPrecisionVocab</summary>
    public static class TimestampPrecisionVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TimestampPrecisionVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "day", "hour", "minute", "month", "second", "year" };
        public const string day = "day";
        public const string hour = "hour";
        public const string minute = "minute";
        public const string month = "month";
        public const string second = "second";
        public const string year = "year";
    }

    /// <summary>Vocabulary: TrendVocab</summary>
    public static class TrendVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TrendVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Decreasing", "Increasing" };
        public const string Decreasing = "Decreasing";
        public const string Increasing = "Increasing";
    }

    /// <summary>Vocabulary: TriggerFrequencyVocab</summary>
    public static class TriggerFrequencyVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerFrequencyVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "TASK_EVENT_TRIGGER_AT_LOGON", "TASK_EVENT_TRIGGER_AT_SYSTEMSTART", "TASK_EVENT_TRIGGER_ON_IDLE", "TASK_TIME_TRIGGER_DAILY", "TASK_TIME_TRIGGER_MONTHLYDATE", "TASK_TIME_TRIGGER_MONTHLYDOW", "TASK_TIME_TRIGGER_ONCE", "TASK_TIME_TRIGGER_WEEKLY" };
        public const string TASK_EVENT_TRIGGER_AT_LOGON = "TASK_EVENT_TRIGGER_AT_LOGON";
        public const string TASK_EVENT_TRIGGER_AT_SYSTEMSTART = "TASK_EVENT_TRIGGER_AT_SYSTEMSTART";
        public const string TASK_EVENT_TRIGGER_ON_IDLE = "TASK_EVENT_TRIGGER_ON_IDLE";
        public const string TASK_TIME_TRIGGER_DAILY = "TASK_TIME_TRIGGER_DAILY";
        public const string TASK_TIME_TRIGGER_MONTHLYDATE = "TASK_TIME_TRIGGER_MONTHLYDATE";
        public const string TASK_TIME_TRIGGER_MONTHLYDOW = "TASK_TIME_TRIGGER_MONTHLYDOW";
        public const string TASK_TIME_TRIGGER_ONCE = "TASK_TIME_TRIGGER_ONCE";
        public const string TASK_TIME_TRIGGER_WEEKLY = "TASK_TIME_TRIGGER_WEEKLY";
    }

    /// <summary>Vocabulary: TriggerTypeVocab</summary>
    public static class TriggerTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/TriggerTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "TASK_TRIGGER_BOOT", "TASK_TRIGGER_EVENT", "TASK_TRIGGER_IDLE", "TASK_TRIGGER_LOGON", "TASK_TRIGGER_REGISTRATION", "TASK_TRIGGER_SESSION_STATE_CHANGE", "TASK_TRIGGER_TIME" };
        public const string TASK_TRIGGER_BOOT = "TASK_TRIGGER_BOOT";
        public const string TASK_TRIGGER_EVENT = "TASK_TRIGGER_EVENT";
        public const string TASK_TRIGGER_IDLE = "TASK_TRIGGER_IDLE";
        public const string TASK_TRIGGER_LOGON = "TASK_TRIGGER_LOGON";
        public const string TASK_TRIGGER_REGISTRATION = "TASK_TRIGGER_REGISTRATION";
        public const string TASK_TRIGGER_SESSION_STATE_CHANGE = "TASK_TRIGGER_SESSION_STATE_CHANGE";
        public const string TASK_TRIGGER_TIME = "TASK_TRIGGER_TIME";
    }

    /// <summary>Vocabulary: URLTransitionTypeVocab</summary>
    public static class URLTransitionTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/URLTransitionTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "auto_bookmark", "auto_subframe", "auto_toplevel", "form_submit", "generated", "keyword", "keyword_generated", "link", "manual_subframe", "reload", "typed" };
        public const string auto_bookmark = "auto_bookmark";
        public const string auto_subframe = "auto_subframe";
        public const string auto_toplevel = "auto_toplevel";
        public const string form_submit = "form_submit";
        public const string generated = "generated";
        public const string keyword = "keyword";
        public const string keyword_generated = "keyword_generated";
        public const string link = "link";
        public const string manual_subframe = "manual_subframe";
        public const string reload = "reload";
        public const string typed = "typed";
    }

    /// <summary>Vocabulary: UnixProcessStateVocab</summary>
    public static class UnixProcessStateVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/UnixProcessStateVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Dead", "InterruptibleSleep", "Paging", "Running", "Stopped", "UninterruptibleSleep", "Zombie" };
        public const string Dead = "Dead";
        public const string InterruptibleSleep = "InterruptibleSleep";
        public const string Paging = "Paging";
        public const string Running = "Running";
        public const string Stopped = "Stopped";
        public const string UninterruptibleSleep = "UninterruptibleSleep";
        public const string Zombie = "Zombie";
    }

    /// <summary>Vocabulary: WhoisContactTypeVocab</summary>
    public static class WhoisContactTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisContactTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "ADMIN", "BILLING", "TECHNICAL" };
        public const string ADMIN = "ADMIN";
        public const string BILLING = "BILLING";
        public const string TECHNICAL = "TECHNICAL";
    }

    /// <summary>Vocabulary: WhoisDNSSECTypeVocab</summary>
    public static class WhoisDNSSECTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Signed", "Unsigned" };
        public const string Signed = "Signed";
        public const string Unsigned = "Unsigned";
    }

    /// <summary>Vocabulary: WhoisStatusTypeVocab</summary>
    public static class WhoisStatusTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisStatusTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "ADD_PERIOD", "AUTO_RENEW_PERIOD", "CLIENT_DELETE_PROHIBITED", "CLIENT_HOLD", "CLIENT_RENEW_PROHIBITED", "CLIENT_TRANSFER_PROHIBITED", "CLIENT_UPDATE_PROHIBITED", "DELETE_PROHIBITED", "HOLD", "INACTIVE", "OK", "PENDING_DELETE_RESTORABLE", "PENDING_DELETE_SCHEDULED_FOR_RELEASE", "PENDING_RESTORE", "RENEW_PERIOD", "RENEW_PROHIBITED", "TRANSFER_PERIOD", "TRANSFER_PROHIBITED", "UPDATE_PROHIBITED" };
        public const string ADD_PERIOD = "ADD_PERIOD";
        public const string AUTO_RENEW_PERIOD = "AUTO_RENEW_PERIOD";
        public const string CLIENT_DELETE_PROHIBITED = "CLIENT_DELETE_PROHIBITED";
        public const string CLIENT_HOLD = "CLIENT_HOLD";
        public const string CLIENT_RENEW_PROHIBITED = "CLIENT_RENEW_PROHIBITED";
        public const string CLIENT_TRANSFER_PROHIBITED = "CLIENT_TRANSFER_PROHIBITED";
        public const string CLIENT_UPDATE_PROHIBITED = "CLIENT_UPDATE_PROHIBITED";
        public const string DELETE_PROHIBITED = "DELETE_PROHIBITED";
        public const string HOLD = "HOLD";
        public const string INACTIVE = "INACTIVE";
        public const string OK = "OK";
        public const string PENDING_DELETE_RESTORABLE = "PENDING_DELETE_RESTORABLE";
        public const string PENDING_DELETE_SCHEDULED_FOR_RELEASE = "PENDING_DELETE_SCHEDULED_FOR_RELEASE";
        public const string PENDING_RESTORE = "PENDING_RESTORE";
        public const string RENEW_PERIOD = "RENEW_PERIOD";
        public const string RENEW_PROHIBITED = "RENEW_PROHIBITED";
        public const string TRANSFER_PERIOD = "TRANSFER_PERIOD";
        public const string TRANSFER_PROHIBITED = "TRANSFER_PROHIBITED";
        public const string UPDATE_PROHIBITED = "UPDATE_PROHIBITED";
    }

    /// <summary>Vocabulary: WindowsDriveTypeVocab</summary>
    public static class WindowsDriveTypeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsDriveTypeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "DRIVE_CDROM", "DRIVE_FIXED", "DRIVE_NO_ROOT_DIR", "DRIVE_RAMDISK", "DRIVE_REMOTE", "DRIVE_REMOVABLE", "DRIVE_UNKNOWN" };
        public const string DRIVE_CDROM = "DRIVE_CDROM";
        public const string DRIVE_FIXED = "DRIVE_FIXED";
        public const string DRIVE_NO_ROOT_DIR = "DRIVE_NO_ROOT_DIR";
        public const string DRIVE_RAMDISK = "DRIVE_RAMDISK";
        public const string DRIVE_REMOTE = "DRIVE_REMOTE";
        public const string DRIVE_REMOVABLE = "DRIVE_REMOVABLE";
        public const string DRIVE_UNKNOWN = "DRIVE_UNKNOWN";
    }

    /// <summary>Vocabulary: WindowsPEBinaryType</summary>
    public static class WindowsPEBinaryType
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryType";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "dll", "exe", "sys" };
        public const string dll = "dll";
        public const string exe = "exe";
        public const string sys = "sys";
    }

    /// <summary>Vocabulary: WindowsServiceStartType</summary>
    public static class WindowsServiceStartType
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStartType";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "service_auto_start", "service_boot_start", "service_demand_start", "service_disabled", "service_system_alert" };
        public const string service_auto_start = "service_auto_start";
        public const string service_boot_start = "service_boot_start";
        public const string service_demand_start = "service_demand_start";
        public const string service_disabled = "service_disabled";
        public const string service_system_alert = "service_system_alert";
    }

    /// <summary>Vocabulary: WindowsServiceStatus</summary>
    public static class WindowsServiceStatus
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceStatus";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "service_continue_pending", "service_pause_pending", "service_paused", "service_running", "service_start_pending", "service_stop_pending", "service_stopped" };
        public const string service_continue_pending = "service_continue_pending";
        public const string service_pause_pending = "service_pause_pending";
        public const string service_paused = "service_paused";
        public const string service_running = "service_running";
        public const string service_start_pending = "service_start_pending";
        public const string service_stop_pending = "service_stop_pending";
        public const string service_stopped = "service_stopped";
    }

    /// <summary>Vocabulary: WindowsServiceType</summary>
    public static class WindowsServiceType
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceType";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "service_file_system_driver", "service_kernel_driver", "service_win32_own_process", "service_win32_share_process" };
        public const string service_file_system_driver = "service_file_system_driver";
        public const string service_kernel_driver = "service_kernel_driver";
        public const string service_win32_own_process = "service_win32_own_process";
        public const string service_win32_share_process = "service_win32_share_process";
    }

    /// <summary>Vocabulary: WindowsVolumeAttributeVocab</summary>
    public static class WindowsVolumeAttributeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "Hidden", "NoDefaultDriveLetter", "ReadOnly", "ShadowCopy" };
        public const string Hidden = "Hidden";
        public const string NoDefaultDriveLetter = "NoDefaultDriveLetter";
        public const string ReadOnly = "ReadOnly";
        public const string ShadowCopy = "ShadowCopy";
    }

    /// <summary>Vocabulary: WirelessNetworkSecurityModeVocab</summary>
    public static class WirelessNetworkSecurityModeVocab
    {
        public const string IRI = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WirelessNetworkSecurityModeVocab";
        public static readonly IReadOnlyCollection<string> Members = new HashSet<string> { "None", "WEP", "WPA", "WPA2-Enterprise", "WPA2-PSK", "WPA3-Enterprise", "WPA3-PSK" };
        public const string None = "None";
        public const string WEP = "WEP";
        public const string WPA = "WPA";
        public const string WPA2_Enterprise = "WPA2-Enterprise";
        public const string WPA2_PSK = "WPA2-PSK";
        public const string WPA3_Enterprise = "WPA3-Enterprise";
        public const string WPA3_PSK = "WPA3-PSK";
    }
}
