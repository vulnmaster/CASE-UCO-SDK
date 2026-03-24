//! Auto-generated uco-tool types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

use crate::uco::configuration::Configuration;
use crate::uco::identity::Identity;

/// An analytic tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of explanation, interpretation or logical reasoning.
#[derive(Debug, Clone, Serialize)]
pub struct AnalyticTool {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AnalyticTool {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/AnalyticTool";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> AnalyticToolBuilder {
        AnalyticToolBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AnalyticToolBuilder {
}

impl AnalyticToolBuilder {
    pub fn build(self) -> AnalyticTool {
        AnalyticTool {
            class_iri: AnalyticTool::CLASS_IRI,
        }
    }
}

impl CaseObject for AnalyticTool {
    fn class_iri() -> &'static str { AnalyticTool::CLASS_IRI }
    fn type_name() -> &'static str { "AnalyticTool" }
}

/// A build facet is a grouping of characteristics unique to a particular version of a software.
#[derive(Debug, Clone, Serialize)]
pub struct BuildFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-tool:buildInformation")]
    pub build_information: Option<BuildInformationType>,
}

impl BuildFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/BuildFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> BuildFacetBuilder {
        BuildFacetBuilder {
            build_information: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BuildFacetBuilder {
    build_information: Option<BuildInformationType>,
}

impl BuildFacetBuilder {
    pub fn build_information(mut self, value: BuildInformationType) -> Self {
        self.build_information = Some(value);
        self
    }

    pub fn build(self) -> BuildFacet {
        BuildFacet {
            class_iri: BuildFacet::CLASS_IRI,
            build_information: self.build_information,
        }
    }
}

impl CaseObject for BuildFacet {
    fn class_iri() -> &'static str { BuildFacet::CLASS_IRI }
    fn type_name() -> &'static str { "BuildFacet" }
}

/// A build information type is a grouping of characteristics that describe how a particular version of software was converted from source code to executable code.
#[derive(Debug, Clone, Serialize)]
pub struct BuildInformationType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-tool:buildConfiguration")]
    pub build_configuration: Option<Configuration>,
    #[serde(rename = "uco-tool:buildID")]
    pub build_id: Option<String>,
    #[serde(rename = "uco-tool:buildLabel")]
    pub build_label: Option<String>,
    #[serde(rename = "uco-tool:buildOutputLog")]
    pub build_output_log: Option<String>,
    #[serde(rename = "uco-tool:buildProject")]
    pub build_project: Option<String>,
    #[serde(rename = "uco-tool:buildScript")]
    pub build_script: Option<String>,
    #[serde(rename = "uco-tool:buildUtility")]
    pub build_utility: Option<BuildUtilityType>,
    #[serde(rename = "uco-tool:buildVersion")]
    pub build_version: Option<String>,
    #[serde(rename = "uco-tool:compilationDate")]
    pub compilation_date: Option<String>,
    #[serde(rename = "uco-tool:compilers")]
    pub compilers: Vec<CompilerType>,
    #[serde(rename = "uco-tool:libraries")]
    pub libraries: Vec<LibraryType>,
}

impl BuildInformationType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/BuildInformationType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> BuildInformationTypeBuilder {
        BuildInformationTypeBuilder {
            build_configuration: None,
            build_id: None,
            build_label: None,
            build_output_log: None,
            build_project: None,
            build_script: None,
            build_utility: None,
            build_version: None,
            compilation_date: None,
            compilers: Vec::new(),
            libraries: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BuildInformationTypeBuilder {
    build_configuration: Option<Configuration>,
    build_id: Option<String>,
    build_label: Option<String>,
    build_output_log: Option<String>,
    build_project: Option<String>,
    build_script: Option<String>,
    build_utility: Option<BuildUtilityType>,
    build_version: Option<String>,
    compilation_date: Option<String>,
    compilers: Vec<CompilerType>,
    libraries: Vec<LibraryType>,
}

impl BuildInformationTypeBuilder {
    pub fn build_configuration(mut self, value: Configuration) -> Self {
        self.build_configuration = Some(value);
        self
    }

    pub fn build_id(mut self, value: String) -> Self {
        self.build_id = Some(value);
        self
    }

    pub fn build_label(mut self, value: String) -> Self {
        self.build_label = Some(value);
        self
    }

    pub fn build_output_log(mut self, value: String) -> Self {
        self.build_output_log = Some(value);
        self
    }

    pub fn build_project(mut self, value: String) -> Self {
        self.build_project = Some(value);
        self
    }

    pub fn build_script(mut self, value: String) -> Self {
        self.build_script = Some(value);
        self
    }

    pub fn build_utility(mut self, value: BuildUtilityType) -> Self {
        self.build_utility = Some(value);
        self
    }

    pub fn build_version(mut self, value: String) -> Self {
        self.build_version = Some(value);
        self
    }

    pub fn compilation_date(mut self, value: String) -> Self {
        self.compilation_date = Some(value);
        self
    }

    pub fn compilers(mut self, value: Vec<CompilerType>) -> Self {
        self.compilers = value;
        self
    }

    pub fn libraries(mut self, value: Vec<LibraryType>) -> Self {
        self.libraries = value;
        self
    }

    pub fn build(self) -> BuildInformationType {
        BuildInformationType {
            class_iri: BuildInformationType::CLASS_IRI,
            build_configuration: self.build_configuration,
            build_id: self.build_id,
            build_label: self.build_label,
            build_output_log: self.build_output_log,
            build_project: self.build_project,
            build_script: self.build_script,
            build_utility: self.build_utility,
            build_version: self.build_version,
            compilation_date: self.compilation_date,
            compilers: self.compilers,
            libraries: self.libraries,
        }
    }
}

impl CaseObject for BuildInformationType {
    fn class_iri() -> &'static str { BuildInformationType::CLASS_IRI }
    fn type_name() -> &'static str { "BuildInformationType" }
}

/// A build utility type characterizes the tool used to convert from source code to executable code for a particular version of software.
#[derive(Debug, Clone, Serialize)]
pub struct BuildUtilityType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-tool:buildUtilityName")]
    pub build_utility_name: Option<String>,
    #[serde(rename = "uco-tool:cpeid")]
    pub cpeid: Option<String>,
    #[serde(rename = "uco-tool:swid")]
    pub swid: Option<String>,
}

impl BuildUtilityType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/BuildUtilityType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> BuildUtilityTypeBuilder {
        BuildUtilityTypeBuilder {
            build_utility_name: None,
            cpeid: None,
            swid: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BuildUtilityTypeBuilder {
    build_utility_name: Option<String>,
    cpeid: Option<String>,
    swid: Option<String>,
}

impl BuildUtilityTypeBuilder {
    pub fn build_utility_name(mut self, value: String) -> Self {
        self.build_utility_name = Some(value);
        self
    }

    pub fn cpeid(mut self, value: String) -> Self {
        self.cpeid = Some(value);
        self
    }

    pub fn swid(mut self, value: String) -> Self {
        self.swid = Some(value);
        self
    }

    pub fn build(self) -> BuildUtilityType {
        BuildUtilityType {
            class_iri: BuildUtilityType::CLASS_IRI,
            build_utility_name: self.build_utility_name,
            cpeid: self.cpeid,
            swid: self.swid,
        }
    }
}

impl CaseObject for BuildUtilityType {
    fn class_iri() -> &'static str { BuildUtilityType::CLASS_IRI }
    fn type_name() -> &'static str { "BuildUtilityType" }
}

/// A compiler type is a grouping of characteristics unique to a specific program that translates computer code written in one programming language (the source language) into another language (the target 
#[derive(Debug, Clone, Serialize)]
pub struct CompilerType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-tool:compilerInformalDescription")]
    pub compiler_informal_description: Option<String>,
    #[serde(rename = "uco-tool:cpeid")]
    pub cpeid: Option<String>,
    #[serde(rename = "uco-tool:swid")]
    pub swid: Option<String>,
}

impl CompilerType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/CompilerType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> CompilerTypeBuilder {
        CompilerTypeBuilder {
            compiler_informal_description: None,
            cpeid: None,
            swid: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CompilerTypeBuilder {
    compiler_informal_description: Option<String>,
    cpeid: Option<String>,
    swid: Option<String>,
}

impl CompilerTypeBuilder {
    pub fn compiler_informal_description(mut self, value: String) -> Self {
        self.compiler_informal_description = Some(value);
        self
    }

    pub fn cpeid(mut self, value: String) -> Self {
        self.cpeid = Some(value);
        self
    }

    pub fn swid(mut self, value: String) -> Self {
        self.swid = Some(value);
        self
    }

    pub fn build(self) -> CompilerType {
        CompilerType {
            class_iri: CompilerType::CLASS_IRI,
            compiler_informal_description: self.compiler_informal_description,
            cpeid: self.cpeid,
            swid: self.swid,
        }
    }
}

impl CaseObject for CompilerType {
    fn class_iri() -> &'static str { CompilerType::CLASS_IRI }
    fn type_name() -> &'static str { "CompilerType" }
}

/// A ConfiguredTool is a Tool that is known to be configured to run in a more specified manner than some unconfigured or less-configured Tool.
#[derive(Debug, Clone, Serialize)]
pub struct ConfiguredTool {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-configuration:isConfigurationOf")]
    pub is_configuration_of: Option<Tool>,
    #[serde(rename = "uco-configuration:usesConfiguration")]
    pub uses_configuration: Option<Configuration>,
}

impl ConfiguredTool {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/ConfiguredTool";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> ConfiguredToolBuilder {
        ConfiguredToolBuilder {
            is_configuration_of: None,
            uses_configuration: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ConfiguredToolBuilder {
    is_configuration_of: Option<Tool>,
    uses_configuration: Option<Configuration>,
}

impl ConfiguredToolBuilder {
    pub fn is_configuration_of(mut self, value: Tool) -> Self {
        self.is_configuration_of = Some(value);
        self
    }

    pub fn uses_configuration(mut self, value: Configuration) -> Self {
        self.uses_configuration = Some(value);
        self
    }

    pub fn build(self) -> ConfiguredTool {
        ConfiguredTool {
            class_iri: ConfiguredTool::CLASS_IRI,
            is_configuration_of: self.is_configuration_of,
            uses_configuration: self.uses_configuration,
        }
    }
}

impl CaseObject for ConfiguredTool {
    fn class_iri() -> &'static str { ConfiguredTool::CLASS_IRI }
    fn type_name() -> &'static str { "ConfiguredTool" }
}

/// A defensive tool is an artifact of hardware and/or software utilized to accomplish a task or purpose of guarding.
#[derive(Debug, Clone, Serialize)]
pub struct DefensiveTool {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DefensiveTool {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/DefensiveTool";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> DefensiveToolBuilder {
        DefensiveToolBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DefensiveToolBuilder {
}

impl DefensiveToolBuilder {
    pub fn build(self) -> DefensiveTool {
        DefensiveTool {
            class_iri: DefensiveTool::CLASS_IRI,
        }
    }
}

impl CaseObject for DefensiveTool {
    fn class_iri() -> &'static str { DefensiveTool::CLASS_IRI }
    fn type_name() -> &'static str { "DefensiveTool" }
}

/// A library type is a grouping of characteristics unique to a collection of resources incorporated into the build of a software.
#[derive(Debug, Clone, Serialize)]
pub struct LibraryType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-tool:libraryName")]
    pub library_name: Option<String>,
    #[serde(rename = "uco-tool:libraryVersion")]
    pub library_version: Option<String>,
}

impl LibraryType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/LibraryType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> LibraryTypeBuilder {
        LibraryTypeBuilder {
            library_name: None,
            library_version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LibraryTypeBuilder {
    library_name: Option<String>,
    library_version: Option<String>,
}

impl LibraryTypeBuilder {
    pub fn library_name(mut self, value: String) -> Self {
        self.library_name = Some(value);
        self
    }

    pub fn library_version(mut self, value: String) -> Self {
        self.library_version = Some(value);
        self
    }

    pub fn build(self) -> LibraryType {
        LibraryType {
            class_iri: LibraryType::CLASS_IRI,
            library_name: self.library_name,
            library_version: self.library_version,
        }
    }
}

impl CaseObject for LibraryType {
    fn class_iri() -> &'static str { LibraryType::CLASS_IRI }
    fn type_name() -> &'static str { "LibraryType" }
}

/// A malicious tool is an artifact of hardware and/or software utilized to accomplish a malevolent task or purpose.
#[derive(Debug, Clone, Serialize)]
pub struct MaliciousTool {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MaliciousTool {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/MaliciousTool";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> MaliciousToolBuilder {
        MaliciousToolBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MaliciousToolBuilder {
}

impl MaliciousToolBuilder {
    pub fn build(self) -> MaliciousTool {
        MaliciousTool {
            class_iri: MaliciousTool::CLASS_IRI,
        }
    }
}

impl CaseObject for MaliciousTool {
    fn class_iri() -> &'static str { MaliciousTool::CLASS_IRI }
    fn type_name() -> &'static str { "MaliciousTool" }
}

/// A tool is an element of hardware and/or software utilized to carry out a particular function.
#[derive(Debug, Clone, Serialize)]
pub struct Tool {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-tool:creator")]
    pub creator: Option<Identity>,
    #[serde(rename = "uco-tool:references")]
    pub references: Vec<String>,
    #[serde(rename = "uco-tool:servicePack")]
    pub service_pack: Option<String>,
    #[serde(rename = "uco-tool:toolType")]
    pub tool_type: Option<String>,
    #[serde(rename = "uco-tool:version")]
    pub version: Option<String>,
}

impl Tool {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/tool/Tool";
    pub const NAMESPACE_PREFIX: &'static str = "uco-tool";

    pub fn builder() -> ToolBuilder {
        ToolBuilder {
            creator: None,
            references: Vec::new(),
            service_pack: None,
            tool_type: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ToolBuilder {
    creator: Option<Identity>,
    references: Vec<String>,
    service_pack: Option<String>,
    tool_type: Option<String>,
    version: Option<String>,
}

impl ToolBuilder {
    pub fn creator(mut self, value: Identity) -> Self {
        self.creator = Some(value);
        self
    }

    pub fn references(mut self, value: Vec<String>) -> Self {
        self.references = value;
        self
    }

    pub fn service_pack(mut self, value: String) -> Self {
        self.service_pack = Some(value);
        self
    }

    pub fn tool_type(mut self, value: String) -> Self {
        self.tool_type = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> Tool {
        Tool {
            class_iri: Tool::CLASS_IRI,
            creator: self.creator,
            references: self.references,
            service_pack: self.service_pack,
            tool_type: self.tool_type,
            version: self.version,
        }
    }
}

impl CaseObject for Tool {
    fn class_iri() -> &'static str { Tool::CLASS_IRI }
    fn type_name() -> &'static str { "Tool" }
}
