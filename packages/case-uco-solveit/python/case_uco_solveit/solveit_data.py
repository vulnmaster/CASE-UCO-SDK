"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit_data module (generated; do not edit)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from case_uco_solveit import solveit_core as _solveit_core
from case_uco_solveit._context import NAMESPACES

__all__ = ["techniqueDFT_1001", "techniqueDFT_1002", "techniqueDFT_1003", "techniqueDFT_1004", "techniqueDFT_1005", "techniqueDFT_1006", "techniqueDFT_1007", "techniqueDFT_1008", "techniqueDFT_1009", "techniqueDFT_1010", "techniqueDFT_1011", "techniqueDFT_1012", "techniqueDFT_1013", "techniqueDFT_1014", "techniqueDFT_1015", "techniqueDFT_1016", "techniqueDFT_1017", "techniqueDFT_1018", "techniqueDFT_1019", "techniqueDFT_1020", "techniqueDFT_1021", "techniqueDFT_1022", "techniqueDFT_1023", "techniqueDFT_1024", "techniqueDFT_1025", "techniqueDFT_1026", "techniqueDFT_1027", "techniqueDFT_1028", "techniqueDFT_1029", "techniqueDFT_1030", "techniqueDFT_1031", "techniqueDFT_1032", "techniqueDFT_1033", "techniqueDFT_1034", "techniqueDFT_1035", "techniqueDFT_1036", "techniqueDFT_1037", "techniqueDFT_1038", "techniqueDFT_1039", "techniqueDFT_1040", "techniqueDFT_1041", "techniqueDFT_1042", "techniqueDFT_1043", "techniqueDFT_1044", "techniqueDFT_1045", "techniqueDFT_1046", "techniqueDFT_1047", "techniqueDFT_1048", "techniqueDFT_1049", "techniqueDFT_1050", "techniqueDFT_1051", "techniqueDFT_1052", "techniqueDFT_1053", "techniqueDFT_1054", "techniqueDFT_1055", "techniqueDFT_1056", "techniqueDFT_1057", "techniqueDFT_1058", "techniqueDFT_1059", "techniqueDFT_1060", "techniqueDFT_1061", "techniqueDFT_1062", "techniqueDFT_1063", "techniqueDFT_1064", "techniqueDFT_1065", "techniqueDFT_1066", "techniqueDFT_1067", "techniqueDFT_1068", "techniqueDFT_1069", "techniqueDFT_1070", "techniqueDFT_1071", "techniqueDFT_1072", "techniqueDFT_1073", "techniqueDFT_1074", "techniqueDFT_1075", "techniqueDFT_1076", "techniqueDFT_1077", "techniqueDFT_1078", "techniqueDFT_1079", "techniqueDFT_1080", "techniqueDFT_1081", "techniqueDFT_1082", "techniqueDFT_1083", "techniqueDFT_1084", "techniqueDFT_1085", "techniqueDFT_1086", "techniqueDFT_1087", "techniqueDFT_1088", "techniqueDFT_1089", "techniqueDFT_1090", "techniqueDFT_1091", "techniqueDFT_1092", "techniqueDFT_1093", "techniqueDFT_1094", "techniqueDFT_1095", "techniqueDFT_1096", "techniqueDFT_1097", "techniqueDFT_1098", "techniqueDFT_1099", "techniqueDFT_1100", "techniqueDFT_1101", "techniqueDFT_1102", "techniqueDFT_1103", "techniqueDFT_1104", "techniqueDFT_1105", "techniqueDFT_1106", "techniqueDFT_1107", "techniqueDFT_1108", "techniqueDFT_1109", "techniqueDFT_1110", "techniqueDFT_1111", "techniqueDFT_1112", "techniqueDFT_1113", "techniqueDFT_1114", "techniqueDFT_1115", "techniqueDFT_1116", "techniqueDFT_1117", "techniqueDFT_1118", "techniqueDFT_1119", "techniqueDFT_1120", "techniqueDFT_1121", "techniqueDFT_1122", "techniqueDFT_1123", "techniqueDFT_1124", "techniqueDFT_1125", "techniqueDFT_1126", "techniqueDFT_1127", "techniqueDFT_1128", "techniqueDFT_1129", "techniqueDFT_1130", "techniqueDFT_1131", "techniqueDFT_1132", "techniqueDFT_1133", "techniqueDFT_1134", "techniqueDFT_1137", "techniqueDFT_1138", "techniqueDFT_1139", "techniqueDFT_1140", "techniqueDFT_1141", "techniqueDFT_1142", "techniqueDFT_1143", "techniqueDFT_1144", "techniqueDFT_1145", "techniqueDFT_1146", "techniqueDFT_1147", "techniqueDFT_1148", "techniqueDFT_1149", "techniqueDFT_1150", "techniqueDFT_1151", "techniqueDFT_1153", "techniqueDFT_1154", "techniqueDFT_1155", "techniqueDFT_1156", "techniqueDFT_1157", "techniqueDFT_1158", "techniqueDFT_1159", "techniqueDFT_1160", "techniqueDFT_1161", "techniqueDFT_1162", "techniqueDFT_1163", "techniqueDFT_1164", "techniqueDFT_1165", "techniqueDFT_1166", "techniqueDFT_1167", "techniqueDFT_1168", "techniqueDFT_1169", "techniqueDFT_1170", "techniqueDFT_1171", "techniqueDFT_1172", "techniqueDFT_1173", "techniqueDFT_1174", "techniqueDFT_1175", "techniqueDFT_1176", "techniqueDFT_1177", "techniqueDFT_1178", "techniqueDFT_1179", "techniqueDFT_1180", "techniqueDFT_1181", "techniqueDFT_1182", "techniqueDFT_1184", "techniqueDFT_1185", "techniqueDFT_1186", "techniqueDFT_1187", "techniqueDFT_1190", "techniqueDFT_1191", "techniqueDFT_1192", "techniqueDFT_1193", "techniqueDFT_1194", "techniqueDFT_1195", "techniqueDFT_1196", "techniqueDFT_1197", "techniqueDFT_1198", "techniqueDFT_1199", "techniqueDFT_1200", "techniqueDFT_1202", "techniqueDFT_1203", "techniqueDFT_1204", "techniqueDFT_1205", "techniqueDFT_1206", "techniqueDFT_1207", "techniqueDFT_1208", "techniqueDFT_1209", "techniqueDFT_1210", "techniqueDFT_1211", "techniqueDFT_1212", "techniqueDFT_1213", "techniqueDFT_1215"]


@dataclass
class techniqueDFT_1001(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1001: Triage devices or media. Objective(s): Prioritize digital evidence sources. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1001"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1002(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1002: Copy sectors from storage media. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1002"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1003(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1003: Copy pages from physical memory. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1003"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1004(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1004: Collect logical files selectively. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1004"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1005(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1005: Search a crime scene for relevant physical evidence. Objective(s): Find potential digital evidence sources. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1005"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1006(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1006: Search a crime scene using digital sniffer dogs. Objective(s): Find potential digital evidence sources. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1006"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1007(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1007: Detect the potential existence of digital devices using a SyncTriage-based approach. Objective(s): Find potential digital evidence sources. See https://solveit-df.org for """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1007"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1008(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1008: Detect the potential existence of digital devices by profiling network traffic. Objective(s): Find potential digital evidence sources. See https://solveit-df.org for weakn"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1008"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1009(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1009: Locate potential digital evidence sources via cloud account identifiers. Objective(s): Find potential digital evidence sources. See https://solveit-df.org for weaknesses a"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1009"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1010(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1010: Place device in a faraday environment. Objective(s): Preserve digital evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1010"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1011(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1011: Store seized devices or media in evidence bags. Objective(s): Preserve digital evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1011"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1012(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1012: Write protect storage media using a hardware write blocker. Objective(s): Preserve digital evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1012"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1013(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1013: Write protect storage media using a software write blocker. Objective(s): Preserve digital evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1013"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1014(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1014: Document the chain of custody. Objective(s): Document digital forensic activities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1014"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1015(techniqueDFT_1004):
    """SOLVE-IT technique DFT-1015: Collect logical files selectively based on privacy preserving criteria. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1015"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1016(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1016: Collect specific pieces of information from a live running device. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1016"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1017(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1017: Capture network packets. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1017"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1018(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1018: Collect data from a remote networked device. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1018"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1157(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1157: Extract device data using exposed service. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1157"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1019(techniqueDFT_1157):
    """SOLVE-IT technique DFT-1019: Extract a backup from a mobile device. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1019"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1020(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1020: Extract the file system from a mobile device. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1020"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1021(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1021: Extract artifacts from a configuration file. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1021"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1022(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1022: Capture mobile device screenshots (manually). Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1022"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1023(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1023: Collect data from cloud service via a live web page using credentials. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1023"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1024(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1024: Collect data from cloud service via submission of request to service provider. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1024"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1025(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1025: Store bitstream data in a forensic image format. Objective(s): Store acquired data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1025"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1026(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1026: Store data in standard archive format. Objective(s): Store acquired data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1026"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1162(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1162: Read data from a device via In-System Programming (ISP). Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1162"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1027(techniqueDFT_1162):
    """SOLVE-IT technique DFT-1027: Read data from a device using JTAG. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1027"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1028(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1028: Physically remove a storage chip from a device (chip-off). Objective(s): Access device data for acquisition. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1028"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1029(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1029: Read data from a desoldered eMMC via a chip reader. Objective(s): Access device data for acquisition. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1029"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1030(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1030: Read data from unmanaged NAND. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1030"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1031(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1031: Recover encryption/decryption key from memory. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1031"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1032(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1032: Recover encryption/decryption key information using side channel attacks. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitig"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1032"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1033(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1033: Extract credential(s) from an accessible device to attempt access to a more secure device or service. Objective(s): Overcome protection mechanisms. See https://solveit-df."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1033"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1034(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1034: Attack a stored credential or device using a brute force approach. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1034"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1035(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1035: Attack a stored credential or device using a dictionary-based approach. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigat"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1035"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1036(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1036: Recover information about a potential device PIN or pattern lock using a smudge attack. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weakne"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1036"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1037(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1037: Obtain password from the device's owner. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1037"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1038(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1038: Attack a stored credential or device using a rainbow table-based approach. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and miti"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1038"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1039(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1039: Downgrade apps to facilitate data extraction. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1039"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1040(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1040: Exploit a mobile device to facilitate privileged access for data extraction. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mi"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1040"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1041(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1041: Gain access to a device via a Pin2Pwn approach. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1041"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1042(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1042: Verify hash of copied data matches the hash of the data read from source device. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1042"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1043(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1043: Read bitstream from forensic image container file(s). Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigati"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1043"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1044(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1044: Decode data stored in a mobile backup format. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1044"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1045(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1045: Read contents from standard archive file(s). Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1045"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1046(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1046: Redact digital forensic tool results to protect privileged material. Objective(s): Reduce data under consideration. See https://solveit-df.org for weaknesses and mitigatio"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1046"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1047(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1047: Filter files using a hashset to reduce files examined. Objective(s): Reduce data under consideration. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1047"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1048(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1048: Protect privacy by only partially processing data from a source. Objective(s): Reduce data under consideration. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1048"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1049(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1049: Keyword search. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1049"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1050(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1050: Locate relevant files using a hashset to identify files of interest. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitig"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1050"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1051(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1051: Locate potentially relevant files using fuzzy hash matching. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1051"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1052(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1052: Generate timeline. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1052"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1053(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1053: Extract 'entities' from a data source. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1053"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1054(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1054: Review artifacts or content manually for relevant material. Objective(s): Review content for relevance. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1054"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1055(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1055: Examine file and folder structure. Objective(s): Review content for relevance. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1055"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1056(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1056: Enumerate connections between artifacts. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1056"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1057(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1057: Search for indicators of steganography. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1057"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1058(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1058: Search for mismatched file extensions. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1058"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1059(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1059: Identify partitions. Objective(s): Access partitions, volumes and file systems data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1059"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1060(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1060: Enumerate allocated files and folders. Objective(s): Access partitions, volumes and file systems data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1060"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1061(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1061: Recover non-allocated files. Objective(s): Access partitions, volumes and file systems data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1061"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1062(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1062: Decrypt encrypted file systems/volumes. Objective(s): Access partitions, volumes and file systems data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1062"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1063(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1063: Identify file types. Objective(s): Access partitions, volumes and file systems data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1063"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1064(techniqueDFT_1061):
    """SOLVE-IT technique DFT-1064: Carve non-allocated files. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1064"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1065(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1065: Extract artifacts from operating system-level content indexer(s). Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1065"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1066(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1066: Extract artifacts from operating system log files. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigation"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1066"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1067(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1067: Extract artifacts from operating system cloud synchronization features. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weak"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1067"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1068(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1068: Extract operating system artifacts indicating recently used files. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesse"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1068"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1069(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1069: Extract artifacts from a web browser. Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1069"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1070(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1070: Extract artifacts from email client(s) or webmail access. Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1070"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1071(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1071: Extract data from SQLite database(s). Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1071"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1072(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1072: Extract artifacts from chat app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1072"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1073(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1073: Extract artifacts from calendar app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1073"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1074(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1074: Extract artifacts from social network app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1074"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1075(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1075: Extract artifacts from maps/travel app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1075"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1076(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1076: Extract artifacts from log files. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1076"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1077(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1077: Extract artifacts from photo management app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1077"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1078(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1078: Extract artifacts from cloud synchronization app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1078"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1079(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1079: Examine audio content. Objective(s): Review content for relevance. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1079"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1080(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1080: Examine video content. Objective(s): Review content for relevance. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1080"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1081(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1081: Examine image/picture content. Objective(s): Review content for relevance. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1081"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1082(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1082: Examine document content. Objective(s): Review content for relevance. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1082"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1083(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1083: Extract artifacts from operating system memory structures. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mi"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1083"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1084(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1084: Extract potentially user-identifying content from account information. Objective(s): Establish identities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1084"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1085(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1085: Conflate specific account identifiers to a single user identity. Objective(s): Establish identities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1085"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1086(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1086: Analyze timeline. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1086"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1087(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1087: Reconstruct the location-based properties of an event. Objective(s): Reconstruct events. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1087"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1088(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1088: Reconstruct relations between events or properties of events. Objective(s): Reconstruct events. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1088"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1089(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1089: Review source code of software. Objective(s): Conduct research. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1089"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1090(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1090: Experiment with software to ascertain forensic artifacts. Objective(s): Conduct research. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1090"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1091(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1091: Tag artifacts. Objective(s): Document digital forensic activities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1091"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1092(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1092: Generate tag-based automated report. Objective(s): Document digital forensic activities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1092"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1093(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1093: Write expert report. Objective(s): Document digital forensic activities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1093"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1094(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1094: Disclose investigation material to an authorized legal authority. Objective(s): Document digital forensic activities. See https://solveit-df.org for weaknesses and mitigat"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1094"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1095(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1095: Instrument a piece of running software. Objective(s): Conduct research. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1095"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1096(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1096: Extract operating system artifacts indicating program execution. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses """

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1096"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1097(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1097: Extract operating system artifacts indicating installed software. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1097"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1098(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1098: Enumerate operating system user accounts. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1098"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1099(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1099: Repair a damaged or incomplete file using `grafting`. Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1099"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1100(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1100: Extract metadata from within images. Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1100"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1101(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1101: Conduct cell site survey. Objective(s): Conduct research. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1101"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1102(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1102: Decode data extracted from unmanaged NAND. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1102"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1103(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1103: Virtualize suspect system for previewing. Objective(s): Create visualizations. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1103"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1104(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1104: Collect data using open source intelligence. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1104"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1105(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1105: Examine memory dump from an application. Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1105"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1106(techniqueDFT_1080):
    """SOLVE-IT technique DFT-1106: Classify if a video is potentially synthetically generated. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1106"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1107(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1107: Extract artifacts from health/fitness app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1107"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1108(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1108: Extract artifacts from reminders app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1108"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1109(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1109: Extract artifacts from payment app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1109"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1110(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1110: Preserve reference data. Objective(s): Prepare for a digital investigation. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1110"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1111(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1111: Record system clock offset. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1111"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1112(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1112: Locate and remove physical disks from a device. Objective(s): Access device data for acquisition. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1112"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1113(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1113: Access internal storage via bootable environment. Objective(s): Access device data for acquisition. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1113"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1114(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1114: Preserve memory contents via Cold Boot Attack. Objective(s): Preserve digital evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1114"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1115(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1115: Visualize geolocation information. Objective(s): Create visualizations. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1115"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1116(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1116: Extract references to connected devices. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1116"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1117(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1117: Reconstruct the time that an event may have occurred. Objective(s): Reconstruct events. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1117"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1118(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1118: Locate relevant files by path. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1118"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1119(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1119: Automatically scan for artifact changes caused by app updates. Objective(s): Conduct research. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1119"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1120(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1120: Extract artifacts from app data automatically. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1120"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1121(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1121: Index a data source for keyword searching. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1121"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1122(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1122: Keyword search (case-type wordlists). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1122"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1123(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1123: Keyword search (case-specific wordlists). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1123"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1124(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1124: Keyword search (indexed). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1124"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1125(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1125: Keyword search (live). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1125"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1126(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1126: Keyword search (live) (physical). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1126"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1127(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1127: Keyword search (live) (logical). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1127"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1128(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1128: Search for indicators of malware. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1128"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1129(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1129: Search for indicators of clock tampering. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1129"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1130(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1130: Search for indicators of encrypted data. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1130"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1131(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1131: Search for indicators of trail obfuscation. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1131"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1132(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1132: Search for indicators of artifact wiping. Objective(s): Detect anti-forensics and other anomalies. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1132"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1133(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1133: Extract artifacts from AI companion app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1133"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1134(techniqueDFT_1086):
    """SOLVE-IT technique DFT-1134: Use time anchors to estimate clock offset. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1134"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1137(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1137: Extract browser history artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1137"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1138(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1138: Extract browser cache artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1138"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1139(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1139: Extract browser session artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1139"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1140(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1140: Extract browser autofill artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1140"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1141(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1141: Extract browser bookmark artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1141"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1142(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1142: Extract browser download artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1142"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1143(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1143: Extract browser configuration artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1143"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1144(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1144: Enumerate browser profiles. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1144"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1145(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1145: Extract browser extensions artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1145"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1146(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1146: Extract browser synchronization artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1146"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1147(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1147: Extract browser cookie artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1147"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1148(techniqueDFT_1069):
    """SOLVE-IT technique DFT-1148: Extract browser web storage artifacts. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1148"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1149(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1149: Extract artifacts from the file versioning feature. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigatio"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1149"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1150(techniqueDFT_1061):
    """SOLVE-IT technique DFT-1150: Recover non-allocated files using residual file metadata. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1150"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1151(techniqueDFT_1049):
    """SOLVE-IT technique DFT-1151: Keyword search (over extracted artifacts). See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1151"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1153(techniqueDFT_1052):
    """SOLVE-IT technique DFT-1153: Apply offset to a timestamp. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1153"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1154(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1154: Reconstruct an identity associated with an event. Objective(s): Reconstruct events. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1154"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1155(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1155: Reconstruct that a specific event may have occurred. Objective(s): Reconstruct events. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1155"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1156(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1156: Reconstruct if an event could have functionally occurred on a system given its capabilities. Objective(s): Reconstruct events. See https://solveit-df.org for weaknesses an"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1156"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1158(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1158: Configure device to enable a service needed for data extraction. Objective(s): Overcome protection mechanisms. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1158"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1159(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1159: Extract mobile data via deployed agent. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1159"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1160(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1160: Collect data with 'cloud backup restore' approach. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1160"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1161(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1161: Collect data from cloud service via API using credentials. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1161"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1163(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1163: Capture mobile device screenshots (automatically). Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1163"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1164(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1164: Read data directly from a block device. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1164"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1165(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1165: Extract software configuration information. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1165"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1166(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1166: Connect directly to storage media. Objective(s): Access device data for acquisition. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1166"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1167(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1167: Extract search terms from URLs. Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1167"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1168(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1168: Identify volumes. Objective(s): Access partitions, volumes and file systems data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1168"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1169(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1169: Filter files related to an application. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1169"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1170(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1170: Read contents from logical forensic container file(s). Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigat"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1170"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1171(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1171: Access a file system via live operating system. Objective(s): Access device data for acquisition. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1171"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1172(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1172: Read bitstream from raw image file(s). Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1172"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1173(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1173: Extract data from captured screenshots. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1173"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1174(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1174: Read evidential files stored directly on local file system. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mi"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1174"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1175(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1175: Extract data from an Android device using content queries. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1175"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1176(techniqueDFT_1081):
    """SOLVE-IT technique DFT-1176: Classify if an image is potentially synthetically generated. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1176"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1177(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1177: Extract artifacts from multiplayer game app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1177"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1178(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1178: Store bitstream data in a raw image format. Objective(s): Store acquired data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1178"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1179(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1179: Extract artifacts from drone/UAV app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1179"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1180(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1180: Extract file(s) from a pre-deletion container. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1180"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1181(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1181: Extract artifacts from smart home app(s). Objective(s): Extract artifacts stored by applications. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1181"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1182(techniqueDFT_1086):
    """SOLVE-IT technique DFT-1182: Filter a timeline for relevant entries. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1182"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1184(techniqueDFT_1086):
    """SOLVE-IT technique DFT-1184: Sort a timeline so entries are ordered chronologically. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1184"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1185(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1185: Extract data from operating system notifications. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigations"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1185"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1186(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1186: Compute per-file hash values. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1186"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1187(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1187: Extract content from compound files. Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1187"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1190(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1190: Extract operating system version(s) from data source. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigat"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1190"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1191(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1191: Parse allocated structures in Windows HIVE files. Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1191"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1192(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1192: Disable connectivity using device configuration settings. Objective(s): Preserve digital evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1192"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1193(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1193: Read metadata from within a forensic image container. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigati"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1193"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1194(techniqueDFT_1079):
    """SOLVE-IT technique DFT-1194: Classify if audio is potentially synthetically generated. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1194"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1195(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1195: Generate Alternative Hypotheses. Objective(s): Evaluate evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1195"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1196(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1196: Extract operating system installation date. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1196"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1197(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1197: Determine mount point mappings within an operating system. Objective(s): Extract artifacts stored by the operating system. See https://solveit-df.org for weaknesses and mi"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1197"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1198(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1198: Compute hash of data read from source device. Objective(s): Acquire data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1198"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1199(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1199: Compute hash of stored bitstream data. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1199"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1200(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1200: Evaluate observations in light of hypotheses. Objective(s): Evaluate evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1200"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1202(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1202: Verify automated results manually. Objective(s): Evaluate evidence. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1202"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1203(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1203: Use an AI-based prompt for interrogating case data. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1203"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1204(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1204: Verify hash of stored bitstream data matches a stored hash. Objective(s): Read data from digital evidence storage formats. See https://solveit-df.org for weaknesses and mi"""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1204"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1205(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1205: Decode raw data into data value(s). Objective(s): Extract data from specific formats. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1205"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1206(techniqueDFT_1205):
    """SOLVE-IT technique DFT-1206: Decode a number from raw data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1206"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1207(techniqueDFT_1205):
    """SOLVE-IT technique DFT-1207: Decode a string from raw data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1207"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1208(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1208: Store acquisition metadata along with a forensic image format. Objective(s): Store acquired data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1208"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1209(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1209: Extract artifacts from data provided by a service provider. Objective(s): Extract specific artifact types. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1209"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1210(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1210: Obtain approval for a digital forensic activity. Objective(s): Document digital forensic activities. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1210"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1211(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1211: Create a case-type keyword list. Objective(s): Prepare for a digital investigation. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1211"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1212(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1212: Create a case-specific keyword list. Objective(s): Locate potentially relevant content. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1212"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1213(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1213: Generate reference data by performing and recording actions. Objective(s): Prepare for a digital investigation. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1213"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES


@dataclass
class techniqueDFT_1215(_solveit_core.SolveitInvestigativeAction):
    """SOLVE-IT technique DFT-1215: Store content in logical forensic container file(s). Objective(s): Store acquired data. See https://solveit-df.org for weaknesses and mitigations."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/data/techniqueDFT-1215"
    NAMESPACE_PREFIX: str = "solveit-data"
    JSONLD_CONTEXT: ClassVar[dict[str, str]] = NAMESPACES
